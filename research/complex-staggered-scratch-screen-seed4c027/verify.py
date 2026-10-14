#!/usr/bin/env python3
"""Exact optimistic screen for staggered same-register rank-three packets."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
ARCHIVE = "research/community-frontier1094-audit/selected-replay.tar.gz"
MANIFEST = "research/community-frontier1094-audit/SELECTED-SOURCE.json"
MEMBER = "candidate/strict/global/base/providers/gauge44/LOCAL-PROGRAMS.json.gz"
MEMBER_SHA256 = "241fde27d4e43f5a9cb6b128f9f76c5131a53d09f0371676163f914d0b0fef3a"
BASE_PROFILE = {1: 2412, 2: 418, 3: 432, 4: 142, 5: 82, 8: 8}
BASE_CEILING = "1690054109089/1000000000000000"


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_ceiling_engine():
    path = ROOT / "research/complex-local-word-ceiling/ceiling.py"
    spec = importlib.util.spec_from_file_location("pinned_complex_ceiling", path)
    need(spec is not None and spec.loader is not None, "cannot load pinned ceiling engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_events():
    sources = json.loads((PACKAGE / "SOURCES.json").read_text())
    base = sources["base_commit"]
    for record in sources["files"]:
        data = (ROOT / record["path"]).read_bytes()
        need(sha256(data) == record["sha256"], f"source SHA256 mismatch: {record['path']}")
        blob = __import__("subprocess").check_output(
            ["git", "rev-parse", f"{base}:{record['path']}"], cwd=ROOT, text=True
        ).strip()
        need(blob == record["git_blob"], f"source blob mismatch: {record['path']}")

    # The selected archive member has its own compressed-byte pin. The selected
    # source manifest is also pinned in SOURCES.json for provenance.
    json.loads((ROOT / MANIFEST).read_text())
    with tarfile.open(ROOT / ARCHIVE, "r:gz") as archive:
        entry = archive.getmember(MEMBER)
        compressed = archive.extractfile(entry).read()
    need(sha256(compressed) == MEMBER_SHA256, "selected LOCAL-PROGRAMS member hash mismatch")
    return json.loads(gzip.decompress(compressed))


def candidate_intervals(events):
    """Chunk each (phase, register) rank-one stream into disjoint triples."""
    grouped = {}
    for index, event in enumerate(events):
        if event[0] == "climb" and event[5] == 1 and event[1] in ("A", "B"):
            grouped.setdefault((event[1], event[2]), []).append(index)
    intervals = []
    for (phase, register), indexes in sorted(grouped.items()):
        for ordinal in range(len(indexes) // 3):
            triple = indexes[3 * ordinal : 3 * ordinal + 3]
            intervals.append((triple[0], triple[-1], phase, register, ordinal))
    return intervals


def _add_edge(graph, source, target, capacity, cost, tag=None):
    forward = [target, len(graph[target]), capacity, cost, capacity, tag]
    reverse = [source, len(graph[source]), 0, -cost, 0, None]
    graph[source].append(forward)
    graph[target].append(reverse)
    return forward


def maximum_interval_schedule(intervals, capacity):
    """Maximum-cardinality interval subset with at most `capacity` overlaps.

    This is integral min-cost flow on a time-line DAG. An interval edge has cost
    -1; each of `capacity` units of flow is one reusable scratch packet.
    Intervals are inclusive event-index ranges, converted to [start, end+1).
    """
    need(isinstance(capacity, int) and capacity >= 0, "capacity must be a nonnegative integer")
    if capacity == 0 or not intervals:
        return []
    for start, end, *_ in intervals:
        need(isinstance(start, int) and isinstance(end, int) and start < end,
             "interval must contain at least two distinct event positions")
    times = sorted({t for start, end, *_ in intervals for t in (start, end + 1)})
    index = {t: i for i, t in enumerate(times)}
    graph = [[] for _ in times]
    for i in range(len(times) - 1):
        _add_edge(graph, i, i + 1, capacity, 0)
    interval_edges = []
    for interval_id, interval in enumerate(intervals):
        start, end = interval[:2]
        edge = _add_edge(graph, index[start], index[end + 1], 1, -1, interval_id)
        interval_edges.append(edge)

    sent = 0
    total_cost = 0
    node_count = len(graph)
    source, sink = 0, node_count - 1
    while sent < capacity:
        distance = [10**12] * node_count
        previous = [None] * node_count
        distance[source] = 0
        for _ in range(node_count - 1):
            changed = False
            for u, edges in enumerate(graph):
                if distance[u] == 10**12:
                    continue
                for edge_index, edge in enumerate(edges):
                    v, _rev, residual, cost, _initial, _tag = edge
                    if residual and distance[v] > distance[u] + cost:
                        distance[v] = distance[u] + cost
                        previous[v] = (u, edge_index)
                        changed = True
            if not changed:
                break
        need(previous[sink] is not None, "time-line flow unexpectedly disconnected")
        amount = capacity - sent
        v = sink
        while v != source:
            u, edge_index = previous[v]
            amount = min(amount, graph[u][edge_index][2])
            v = u
        v = sink
        while v != source:
            u, edge_index = previous[v]
            edge = graph[u][edge_index]
            edge[2] -= amount
            graph[v][edge[1]][2] += amount
            v = u
        sent += amount
        total_cost += amount * distance[sink]

    chosen = [edge[5] for edge in interval_edges if edge[5] is not None and edge[2] == 0]
    need(total_cost == -len(chosen), "flow objective and chosen interval count disagree")
    check_capacity([intervals[i] for i in chosen], capacity)
    return chosen


def check_capacity(intervals, capacity):
    points = []
    for start, end, *_ in intervals:
        points.append((start, 1))
        points.append((end, -1))
    active = 0
    for _index, delta in sorted(points, key=lambda point: (point[0], -point[1])):
        active += delta
        need(active <= capacity, "selected intervals exceed scratch-packet capacity")
        need(active >= 0, "invalid interval endpoint ordering")
    need(active == 0, "unclosed interval census")


def profile_for_batches(batch_count, scratch_rank1_overhead=0):
    need(batch_count >= 0 and scratch_rank1_overhead >= 0, "negative profile input")
    profile = dict(BASE_PROFILE)
    profile[1] += scratch_rank1_overhead - 3 * batch_count
    profile[3] += batch_count
    need(profile[1] >= 0, "batch schedule removes too many rank-one events")
    return profile


def compute():
    events = load_events()
    forward = events["forward"]
    backward = events["backward"]
    forward_climbs = [(i, *event[1:]) for i, event in enumerate(forward) if event[0] == "climb"]
    backward_climbs = [(i, *event[1:]) for i, event in enumerate(backward) if event[0] == "climb"]
    need(forward_climbs == backward_climbs, "orientations do not share the same climb itinerary")
    intervals = candidate_intervals(forward)
    need(len(intervals) == 369, "rank-one triple candidate census changed")

    engine = load_ceiling_engine()
    from fractions import Fraction as Q

    summaries = []
    for packet_capacity in (1, 3, 5):
        chosen = maximum_interval_schedule(intervals, packet_capacity)
        profile = profile_for_batches(len(chosen))
        model = engine.model(profile, 73, 896, 9, 64)
        bracket = engine.ceiling(profile, 73, 896, 9, 64, grid=Q(1, 10**6))
        summaries.append({
            "simultaneous_packets": packet_capacity,
            "scratch_arrays": 3 * packet_capacity,
            "selected_triples": len(chosen),
            "replaced_rank1_children": 3 * len(chosen),
            "rank_profile_zero_scratch_cost": {str(k): int(v) for k, v in sorted(profile.items())},
            "local_mass": str(model["local_mass"]),
            "idle_mass": str(model["idle_mass"]),
            "ceiling_grid_bracket": [str(x) for x in bracket],
            "certificate_batch_indices_sha256": sha256(",".join(map(str, chosen)).encode()),
        })

    max_case = summaries[-1]
    target = Q(BASE_CEILING) * Q(105, 100)
    target_interval = engine.relax(profile_for_batches(max_case["selected_triples"]),
                                   73, 896, 9, 64, target)
    need(target_interval[0] > 1, "favorable K=5 profile reaches the 5 percent target")
    need(Q(max_case["ceiling_grid_bracket"][1]) < target,
         "ceiling bracket does not certify failure of the 5 percent gate")

    return {
        "status": "PASS_STAGGERED_SCRATCH_SCREEN",
        "seed": "4c02737e0fc701ea05e30cbadaa396a9",
        "track": "complex-mechanisms",
        "task_id": "complex-new-helper-inventory",
        "priority_revision": 3,
        "base_commit": "0b1cccf86e2f5132ed286a26ef0a681a495740ea",
        "selected_record_sha256": "10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32",
        "archive_sha256": sha256((ROOT / ARCHIVE).read_bytes()),
        "member": MEMBER,
        "member_sha256": MEMBER_SHA256,
        "candidate_triples": len(intervals),
        "interval_convention": "inclusive local-program event indexes; buffers release after the last event",
        "packet_outputs": 3,
        "scratch_initialization_frame_cost_dirty_restoration_hosting": "all omitted (zero-cost favorable relaxation)",
        "baseline_profile": BASE_PROFILE,
        "baseline_ceiling_upper": BASE_CEILING,
        "five_percent_target_a": str(target),
        "target_relaxation_interval": [str(x) for x in target_interval],
        "capacities": summaries,
        "conclusion": "With at most 15 scratch arrays, even zero-cost scratch accounting leaves the exact per-call ceiling below the required 5 percent gain.",
        "limitations": [
            "The interval model assumes each selected triple can be served by a rank-three packet; no scalar endpoint construction is claimed.",
            "Scratch access, arbitrary dirty-state closure, frame transitions, restoration, hosting, precision and controller compatibility are omitted, all favorably.",
            "The result is only the finite source-pinned same-register triple family and packet capacities one through five.",
            "No new kappa, supplier admission, universal impossibility or PR is claimed.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the deterministic RESULT.json")
    args = parser.parse_args()
    result = compute()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        (PACKAGE / "RESULT.json").write_text(encoded)
    print(encoded, end="")
    cases = {item["simultaneous_packets"]: item for item in result["capacities"]}
    print("PASS_STAGGERED_SCRATCH_SCREEN "
          f"triples={result['candidate_triples']} "
          f"K1={cases[1]['selected_triples']} K3={cases[3]['selected_triples']} "
          f"K5={cases[5]['selected_triples']} arrays5={cases[5]['scratch_arrays']} "
          f"ceiling5<={cases[5]['ceiling_grid_bracket'][1]} gate=FAIL")


if __name__ == "__main__":
    main()
