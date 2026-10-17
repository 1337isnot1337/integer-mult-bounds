#!/usr/bin/env python3
"""CP-SAT upper screen for exact operator equality on 73 coordinate characters.

This is an optional discovery/relaxation run, not the registered admission check.
For each of the 112 owner-replica-zero port contexts, it allows every reassignment
of the four 48-axis residual multisets, fixes hosted axes, requires orthonormal
final child bases and rank <= 51, and asks whether any rank-changing assignment
can preserve the exact eight-stream operator on all 73 coordinate characters.
It deliberately omits per-axis translation/commuting restrictions, making the
assignment model a superset of physically eligible moves.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
import time
from pathlib import Path

from ortools.sat.python import cp_model
import ortools

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
CHILDREN = (8, 10, 12, 13)
CHARACTER_BITS = 73
MAX_RANK = 51
TABLE_SIZE = 10**12
TIME_LIMIT = 30.0


def load_screen():
    spec = importlib.util.spec_from_file_location("idle_axis_ortools", PACKAGE / "ortools_screen.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def phase_delta_table(v, context, blocks, character):
    """All 4^4 child phase shifts that preserve the exact matrix at character."""
    baseline = v.replay(context, context["residual"], character, blocks)
    probe_axis = character & -character
    allowed = []
    for delta in itertools.product(range(4), repeat=len(CHILDREN)):
        trial = {child: list(axes) for child, axes in context["residual"].items()}
        for child, amount in zip(CHILDREN, delta, strict=True):
            # Replay consumes only dot-products; repeating this probe axis changes
            # that child's phase exponent by `amount` without changing any input.
            trial[child].extend([probe_axis] * amount)
        if v.replay(context, trial, character, blocks) == baseline:
            allowed.append(list(delta))
    return allowed


def build_model(cp_model_module, context, coordinate_tables, port):
    model = cp_model_module.CpModel()
    tokens = [(source, axis) for source in CHILDREN for axis in context["residual"][source]]
    if len(tokens) != 192 or any(len(context["residual"][c]) != 48 for c in CHILDREN):
        raise ValueError(f"port {port}: expected four 48-axis residual bases")

    x = {(t, dest): model.NewBoolVar(f"p{port}_x_{t}_{dest}")
         for t in range(len(tokens)) for dest in CHILDREN}
    hosted = {child: context["hosted_axes"].get(child, []) for child in CHILDREN}
    dot = lambda a, b: (int(a) & int(b)).bit_count() & 1

    for t, (_, axis) in enumerate(tokens):
        model.AddExactlyOne(x[t, child] for child in CHILDREN)
        for child in CHILDREN:
            if any(dot(axis, fixed) for fixed in hosted[child]):
                model.Add(x[t, child] == 0)

    # Every final residual+hosted child basis must remain orthonormal. This is
    # the only assignment-geometry restriction beyond fixed hosted axes.
    for i, (_, left) in enumerate(tokens):
        for j in range(i + 1, len(tokens)):
            right = tokens[j][1]
            if dot(left, right):
                for child in CHILDREN:
                    model.Add(x[i, child] + x[j, child] <= 1)

    ranks = {}
    for child in CHILDREN:
        ranks[child] = model.NewIntVar(len(hosted[child]), MAX_RANK, f"p{port}_rank_{child}")
        model.Add(ranks[child] == len(hosted[child]) + sum(x[t, child] for t in range(len(tokens))))

    # Any non-uniform rank vector with conserved total 192 has a rank >= 49.
    high = model.NewIntVar(0, MAX_RANK, f"p{port}_high")
    model.AddMaxEquality(high, list(ranks.values()))
    model.Add(high >= 49)

    # Exact necessary equality at each coordinate character. A character's
    # matrix depends on the four new residual phase counts modulo 4. The allowed
    # tuples below were exhaustively replayed over all 4^4 possibilities.
    for bit, allowed in enumerate(coordinate_tables):
        character = 1 << bit
        phase_deltas = []
        for child in CHILDREN:
            old_count = sum(dot(character, axis) for axis in context["residual"][child])
            new_count = model.NewIntVar(0, 192, f"p{port}_count_{bit}_{child}")
            model.Add(new_count == sum(
                dot(character, axis) * x[t, child]
                for t, (_, axis) in enumerate(tokens)
            ))
            delta = model.NewIntVar(0, 3, f"p{port}_delta_{bit}_{child}")
            # 192 is divisible by four and keeps the modulo input nonnegative.
            model.AddModuloEquality(delta, new_count - old_count + 192, 4)
            phase_deltas.append(delta)
        if allowed:
            model.AddAllowedAssignments(phase_deltas, allowed)
        else:
            model.Add(phase_deltas[0] == -1)

    model.Minimize(0)
    return model, tokens, x, ranks


def screen_feasible(v, context, blocks, tokens, x, solver):
    destinations = [next(c for c in CHILDREN if solver.Value(x[t, c])) for t in range(len(tokens))]
    trial = {child: list(axes) for child, axes in context["residual"].items()}
    for child in CHILDREN:
        trial[child] = []
    for (_, axis), destination in zip(tokens, destinations, strict=True):
        trial[destination].append(axis)
    moved = [axis for (source, axis), dest in zip(tokens, destinations, strict=True) if source != dest]
    characters = {1 << bit for bit in range(CHARACTER_BITS)}
    characters.update(moved)
    characters.update(a ^ b for i, a in enumerate(moved) for b in moved[i + 1:])
    mismatches = []
    for character in sorted(characters):
        if v.replay(context, context["residual"], character, blocks) != v.replay(context, trial, character, blocks):
            mismatches.append(character)
            break
    ranks = {str(c): len(trial[c]) + len(context["hosted_axes"].get(c, [])) for c in CHILDREN}
    moved_payload = [[source, dest, axis]
                     for (source, axis), dest in zip(tokens, destinations, strict=True)
                     if source != dest]
    return {
        "rank_vector": ranks,
        "moved_tokens": len(moved_payload),
        "assignment_sha256": hashlib.sha256(
            json.dumps(moved_payload, separators=(",", ":")).encode("ascii")
        ).hexdigest(),
        "finite_screen_characters": len(characters),
        "first_screen_mismatch": mismatches[0] if mismatches else None,
    }


def run(output: Path, port_limit: int | None = None):
    screen = load_screen()
    v = screen.load_verifier()
    contexts, blocks = screen.prepare(v)
    if port_limit is not None:
        contexts = contexts[:port_limit]
    rows = []
    total_start = time.time()
    for port, context in enumerate(contexts):
        port_start = time.time()
        tables = [phase_delta_table(v, context, blocks, 1 << bit) for bit in range(CHARACTER_BITS)]
        table_bytes = json.dumps(tables, separators=(",", ":")).encode("ascii")
        model, tokens, x, ranks = build_model(cp_model, context, tables, port)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = TIME_LIMIT
        solver.parameters.num_search_workers = 1
        solver.parameters.random_seed = 0
        status = solver.Solve(model)
        row = {
            "port": port,
            "coordinate_characters": CHARACTER_BITS,
            "accepted_phase_tuple_counts": {str(k): sum(len(t) == k for t in tables) for k in sorted({len(t) for t in tables})},
            "phase_table_sha256": hashlib.sha256(table_bytes).hexdigest(),
            "solver_status": solver.StatusName(status),
            "solver_seconds": round(solver.WallTime(), 6),
            "wall_seconds": round(time.time() - port_start, 3),
        }
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            row["candidate"] = screen_feasible(v, context, blocks, tokens, x, solver)
        rows.append(row)
        progress = {
            "progress": f"{port + 1}/{len(contexts)}",
            "elapsed_seconds": round(time.time() - total_start, 1),
            "statuses": {s: sum(r["solver_status"] == s for r in rows) for s in sorted({r["solver_status"] for r in rows})},
        }
        print(json.dumps(progress, sort_keys=True), flush=True)

    status_counts = {s: sum(r["solver_status"] == s for r in rows) for s in sorted({r["solver_status"] for r in rows})}
    result = {
        "status": "PASS_NO_RANK_CHANGING_ASSIGNMENT_AT_73_COORDINATE_CHARACTERS"
            if status_counts == {"INFEASIBLE": len(contexts)}
            else "COORDINATE_CHARACTER_RELAXATION_REMAINS_OPEN",
        "base_main": v.BASE_MAIN,
        "fill_payload_sha256": v.FILL_SHA256,
        "solver": "OR-Tools CP-SAT",
        "ortools_version": ortools.__version__,
        "python": sys.version.split()[0],
        "scope": "owner-replica-zero; four residual rank-48 children (8,10,12,13); exact equality at all 73 coordinate Fourier characters; arbitrary token assignment, fixed hosted axes, orthonormal final bases, rank cap 51; per-axis translation and other physical gates omitted, so this is a super-relaxation",
        "model": {
            "tokens_per_port": 192,
            "coordinate_characters_per_port": 73,
            "phase_delta_domain_per_character": 256,
            "rank_change_constraint": "max(child ranks) >= 49",
            "threads": 1,
            "seed": 0,
            "time_limit_seconds_per_port": TIME_LIMIT,
        },
        "status_counts": status_counts,
        "ports": rows,
        "elapsed_seconds": round(time.time() - total_start, 3),
        "selected_frontier_changed": False,
        "new_kappa": None,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"result": result["status"], "ports": len(rows), "statuses": status_counts,
                      "elapsed_seconds": result["elapsed_seconds"], "output": str(output)}, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PACKAGE / "OPERATOR-ORTOOLS-RESULT.json")
    parser.add_argument("--port-limit", type=int, help="pilot on the first N port contexts")
    args = parser.parse_args()
    run(args.output, args.port_limit)


if __name__ == "__main__":
    main()
