#!/usr/bin/env python3
"""Independent integer census of the PR4359 mixed-flow classes.

This verifies counts beyond the native examples' depth-zero cases. It does
not replace the original ownership, operator, or chronological proofs.
Apache-2.0; the mixed-flow construction is attributed to PR4268, and its
native compiler and tariffs to PR4359.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from math import factorial
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMIT = "da637c87c89482bc4c86be36bd0071b3d400dbed"
PINS = {
    "research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz":
        "facfc6d6ecde151afb7e6a167776f3fdaac1c816e785a21a39f7f0bfd9140f3f",
    "research/kappa-rebuild/bit/MIXED-PRODUCTIVE-BIT.json":
        "2f69a19f417c0e0d141c180f9b2fae3d358391b9a230f5848ee07c45450e70bf",
    "research/kappa-rebuild/transfer-audit/finite_dag_audit.py":
        "f842f0e07ca40a181782a565a381b0ee20c6a4b08b8c2b8a4d5d630381bd1e8e",
}


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


class Census:
    """Count literal classes by dilation without materializing their fields."""

    def __init__(self, targets, paid):
        self.targets = dict(sorted(targets.items()))
        self.paid = dict(sorted(paid.items()))
        self.types = tuple(self.targets)
        self.m = max(self.targets)
        self.minimum = min(self.targets)
        need(max(paid) < self.minimum, "strict target/paid separation")
        self.rank_margin = sum(k*n for k, n in targets.items()) - sum(k*n for k, n in paid.items())
        need(self.rank_margin > 0, "positive rank-one surplus")

    @lru_cache(None)
    def points(self, degree):
        """Return column products and multinomial multiplicities independently."""
        result = []

        def visit(index, remaining, column, weight, denominator):
            if index == len(self.types):
                if remaining == 0:
                    result.append((column, factorial(degree)*weight//denominator))
                return
            k = self.types[index]
            for exponent in range(remaining+1):
                visit(index+1, remaining-exponent, column*k**exponent,
                      weight*self.targets[k]**exponent, denominator*factorial(exponent))

        visit(0, degree, 1, 1, 1)
        return tuple(result)

    @lru_cache(None)
    def flow(self, rank):
        need(rank >= self.m, "at least one base unit fits")
        generations = 0
        while self.m*self.minimum**(generations+1) <= rank:
            generations += 1
        classes = Counter({1: 1})
        targets, interior, exits = Counter(), Counter(), Counter()
        units = weighted_units = actual_classes = 0
        for depth in range(generations+1):
            next_classes = Counter()
            for dilation, class_count in classes.items():
                points = [(dilation*column, count) for column, count in self.points(generations-depth)
                          if self.m*dilation*column <= rank]
                # Empty classes contribute no field or event, but their ordered
                # descendants still belong to the mathematical class indexing.
                if points:
                    actual_classes += class_count
                for column, count in points:
                    copies = class_count*count
                    units += copies
                    weighted_units += copies*column
                    for k, number in self.targets.items():
                        targets[column*k] += copies*number
                    destination = interior if depth < generations else exits
                    for k, number in self.paid.items():
                        destination[column*k] += copies*number
                for k, number in self.paid.items():
                    next_classes[dilation*k] += class_count*number
            classes = next_classes
        sources = targets.copy()
        sources.subtract(interior)
        need(all(n >= 0 for n in sources.values()), "all internal calls cancel against target slots")
        sources = +sources
        need(sources and min(sources)*self.m > rank and max(sources) <= rank,
             "all source jobs are in the proved source band")
        need(exits and max(exits) < rank, "all exits have strictly smaller rank")
        surplus = sum(k*n for k, n in sources.items()) - sum(k*n for k, n in exits.items())
        need(surplus == self.rank_margin*weighted_units, "exact rank-potential cancellation")
        return {"rank": rank, "generations": generations, "classes": actual_classes,
                "units": units, "column_weighted_units": weighted_units,
                "sources": sources, "exits": exits, "rank_potential_surplus": surplus}

    @lru_cache(None)
    def leaves_per_array(self, rank):
        if rank < self.m:
            return Fraction(rank)
        row = self.flow(rank)
        numerator = sum((n*self.leaves_per_array(rank-s) for s, n in row["sources"].items()), Fraction(0))
        numerator += sum((n*self.leaves_per_array(e) for e, n in row["exits"].items()), Fraction(0))
        result = numerator/sum(row["sources"].values())
        need(0 < result <= rank, "complete paid-leaf count includes all source complements")
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    source_paths = [source_root/relative for relative in PINS]
    for path in source_paths:
        need(digest(path) == PINS[str(path.relative_to(source_root))], "unchanged PR4359 source bytes")
    # Only the independently written census above is used for the new native
    # counts; the original explicit graph is used as a separate small oracle.
    spec = importlib.util.spec_from_file_location("pr4359_explicit_graph", source_paths[2])
    explicit = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = explicit
    spec.loader.exec_module(explicit)
    toy = explicit.Rule((("a", 3), ("b", 3), ("c", 4)),
                        ((1, "a"), (1, "owned-C0"), (1, "b"), (1, "a"), (2, "c"), (2, "owned-C0")))
    reference = explicit.Compiler(toy)
    independent = Census({3: 2, 4: 1}, {1: 4, 2: 2})
    small = []
    for rank in (4, 7, 12, 16, 28, 40):
        original = reference.compile(rank)
        row = independent.flow(rank)
        tree = reference.trees[rank]
        original_exits = Counter(job["rank"] for batch in tree.exits for job in batch)
        need(row["sources"] == tree.source_counter and row["exits"] == original_exits,
             "independent census agrees with materialized sources and ordered exits")
        need(row["units"] == len(tree.units), "independent native unit count agrees")
        need(independent.leaves_per_array(rank) == original["per_array"],
             "independent complete-leaf recurrence agrees with integral batch compiler")
        small.append({"rank": rank, "generations": row["generations"],
                      "leaves_per_array": str(independent.leaves_per_array(rank))})
    complex_profile = read(source_paths[0])["cover"]
    bit_profile = next(row for row in read(source_paths[1])["candidates"]
                       if row["pairs"] == 3 and row["keep_idle_mask"] == 43)
    native = []
    for family, profile in (("complex", complex_profile), ("BIT", bit_profile)):
        model = Census({int(k): int(n) for k, n in profile["targets"].items()},
                       {int(k): int(n) for k, n in profile["paid"].items()})
        for generations in range(4):
            rank = model.m*model.minimum**generations
            row = dict(model.flow(rank))
            need(row["generations"] == generations, "native case exercises intended generation")
            row.update(family=family, source_fields=sum(row["sources"].values()),
                       exit_jobs=sum(row["exits"].values()))
            if generations <= 1:
                leaf_count = model.leaves_per_array(rank)
                row["leaves_per_array"] = str(leaf_count)
                row["rank_one_gain_per_array"] = str(rank-leaf_count)
            native.append(row)
    # Mutating a source count must break the independently derived conservation
    # identity; this does not pretend to test an arbitrary altered native word.
    corrupted = dict(native[1])
    bad_sources = corrupted["sources"].copy()
    bad_sources[min(bad_sources)] += 1
    changed = sum(k*n for k, n in bad_sources.items()) - sum(k*n for k, n in corrupted["exits"].items())
    need(changed != corrupted["rank_potential_surplus"], "unearned source credit is rejected")
    result = {"schema": "independent-native-multilevel-count-census/1",
              "status": "PASS_INTEGER_CENSUS_TO_THREE_GENERATIONS",
              "source_commit": COMMIT,
              "source_sha256": {str(p.relative_to(source_root)): digest(p) for p in source_paths},
              "generator_sha256": digest(Path(__file__)),
              "materialized_toy_crosschecks": small, "native_cases": native,
              "unearned_source_control_rejected": True,
              "scope": "Exact aggregate integer counts and complete-leaf recurrence; not a materialized native depth-positive word or an independent physical-ownership proof."}
    serialized = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(serialized)
    else:
        need((HERE/"MULTILEVEL-COUNTS.json").read_text() == serialized,
             "exact deterministic integer census replay")
    print(json.dumps({"status": result["status"], "toy_cases": len(small),
                      "native_cases": len(native), "maximum_generations": 3}))


if __name__ == "__main__":
    main()
