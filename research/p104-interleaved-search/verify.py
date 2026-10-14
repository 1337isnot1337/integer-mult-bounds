#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Replay the bounded P104 checkpoint; never assert an improved exponent."""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name):
    spec = importlib.util.spec_from_file_location("p104_checkpoint_" + name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def construct():
    sources = json.loads((HERE / "SOURCES.json").read_text())
    for source in sources["files"]:
        if source["usage"] == "input":
            require(hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest() == source["sha256"],
                    "source drift: " + source["path"])
    scalar = load("scalar_surgery").verify()
    delivery = load("delivery").verify()
    budget = load("budget").verify(include_copy_table=True)

    require(scalar["removed_selected_positions"] == delivery["removed_selected_positions"],
            "scalar and delivery punctures differ")
    by_pair = {tuple(row["pair_hamming_root_indices"]): row for row in delivery["chains"]}
    require(len(by_pair) == 2, "expected two independently replayed delivery fragments")
    query_scales = dict(zip(map(tuple, scalar["decoder_hamming_root_pairs"]),
                            scalar["query_scale_for_delivery_output_dot_a"]))
    require(set(by_pair) <= set(query_scales), "delivery and scalar decoder orientations differ")
    require(all(Fraction(query_scales[pair]) == Fraction(1, 8) for pair in by_pair),
            "delivery source normalization changed")
    for row in budget["chain_profile_inputs"]:
        actual = by_pair[(row["a_root"], row["b_root"])]
        require(row["injections"] == actual["contact_count"], "budget injection count drift")
        require(row["descent"] == actual["private_descent_profile"], "budget descent profile drift")
        require(row["local_tail_cleanup_delta"] == actual["local_B_tail_endpoint_cleanup_profile_delta"],
                "budget local profile differs from actual delivery replay")
        require(row["residual_width_delta"] == actual["residual_width_profile_delta"],
                "budget residual profile differs from actual delivery replay")
    joint = delivery["combined_two_query_channel"]
    for source_key, joint_key in (
        ("local_tail_cleanup_delta", "local_B_tail_endpoint_cleanup_profile_delta"),
        ("residual_width_delta", "residual_width_profile_delta"),
    ):
        total = Counter()
        for row in budget["chain_profile_inputs"]:
            total.update(row[source_key])
        total = {key: count for key, count in total.items() if count}
        require(total == joint[joint_key], "priced sum differs from joint chronological replay")
    require(joint["query_count"] == joint["peak_simultaneous_private_copies"] == 2,
            "simultaneous private-copy contract changed")
    require(not joint["global_owner_hosting_verified"], "this checkpoint must not assert global hosting")
    centres = budget["selected_private_centre_stock"]["selected_private_centre_families"]
    require(joint["peak_simultaneous_private_copies"] <= centres, "fragment exceeds selected private-centre stock")

    return {
        "schema_version": 1,
        "status": "VERIFIED_PARTIAL_CHECKPOINT_NOT_A_SUPPLIER",
        "requested_verified_kappa_gain_achieved": False,
        "base_commit": sources["base_commit"],
        "selected_kappa_unchanged": budget["selected_kappa"],
        "chain_input_sha256": hashlib.sha256((HERE / "CHAINS.json").read_bytes()).hexdigest(),
        "scalar_surgery": scalar,
        "delivery": delivery,
        "budget": budget,
        "cross_checks": {
            "same_exact_104_port_puncture": True,
            "delivery_pairs_belong_to_scalar_decoder": True,
            "retained_delivery_sources_need_raw_query_divided_by_eight": True,
            "priced_single_chain_deltas_equal_replayed_deltas": True,
            "priced_sum_equals_joint_chronological_replay": True,
            "private_copy_peak_fits_selected_eight_centre_stock": True,
            "no_oracle_or_optimistic_ceiling_claimed_as_supplier": True,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true", help="explicitly regenerate the checked receipt")
    args = parser.parse_args()
    result = construct()
    path = HERE / "RESULT.json"
    if args.write_result:
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        require(result == json.loads(path.read_text()), "recorded result differs from exact replay")
    print("PASS_P104_INTERLEAVED_CHECKPOINT: exact partial constructions and conditional cost screens; no improved kappa")


if __name__ == "__main__":
    main()
