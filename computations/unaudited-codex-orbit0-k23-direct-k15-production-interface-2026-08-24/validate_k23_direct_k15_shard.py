#!/usr/bin/env python3
"""Fail-closed validator for one sealed K23 direct-K15 production shard."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys

import k23_direct_k15_contract as C


def reject(label, action):
    try:
        action()
    except C.ContractError:
        return label
    raise RuntimeError(f"hostile mutation accepted: {label}")


def self_test():
    prefix = C.GATE / "results_prefix32.json"
    good, _digest = C.validate_result(prefix, (0, 32), production=False)
    rejected = []
    mutation = copy.deepcopy(good); mutation["hostile_extra"] = True
    rejected.append(reject("extra_top_property", lambda: C.validate_result_data(mutation, production=False)))
    mutation = copy.deepcopy(good); mutation.pop("scale_U")
    rejected.append(reject("missing_scale_U", lambda: C.validate_result_data(mutation, production=False)))
    mutation = copy.deepcopy(good); mutation["scale_U"] = str(C.U + 1)
    rejected.append(reject("wrong_U", lambda: C.validate_result_data(mutation, production=False)))
    mutation = copy.deepcopy(good); mutation["sinks"][C.NAMES[0]]["ids"].reverse()
    rejected.append(reject("regrouped_or_reordered_ids", lambda: C.validate_result_data(mutation, production=False)))
    mutation = copy.deepcopy(good); mutation["sinks"][C.NAMES[0]]["individual_id_charges"] = [0, 0, 0]
    rejected.append(reject("individual_scalar_split", lambda: C.validate_result_data(mutation, production=False)))
    mutation = copy.deepcopy(good); mutation["sinks"][C.NAMES[0]]["irreducible_charge_scaled_U"] = "0"
    rejected.append(reject("full_irreducible_mismatch", lambda: C.validate_result_data(mutation, production=False)))
    mutation = copy.deepcopy(good); mutation["sinks"][C.NAMES[0]]["denominator_product_hist"]["13"] = 1
    rejected.append(reject("nondividing_denominator", lambda: C.validate_result_data(mutation, production=False)))
    rejected.append(reject("gap_interval_ledger", lambda: C.validate_interval_set([
        (0, 60), (61, 121), *C.INTERVALS[2:]
    ])))
    rejected.append(reject("overlap_interval_ledger", lambda: C.validate_interval_set([
        (0, 61), *C.INTERVALS[1:]
    ])))
    rejected.append(reject("missing_interval", lambda: C.validate_interval_set(C.INTERVALS[:-1])))
    return {
        "status": "PASS_K23_DIRECT_K15_SHARD_VALIDATOR_HOSTILE_SELFTEST",
        "positive_gate_result": str(prefix.relative_to(C.ROOT)),
        "rejected": rejected,
        "sealed_production_intervals": [list(value) for value in C.INTERVALS],
        "source_binary_and_input_hashes_replayed": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path, nargs="?")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            answer = self_test()
        else:
            if args.result is None or args.start is None or args.end is None:
                parser.error("result, --start, and --end are required")
            data, digest = C.validate_result(args.result.resolve(),
                                             (args.start, args.end), production=True)
            answer = {
                "status": "PASS_K23_DIRECT_K15_PRODUCTION_SHARD",
                "path": str(args.result),
                "sha256": digest,
                "slice_interval": data["slice_interval"],
                "source_slices": data["source_slices"],
                "strict_groups": C.GROUP_IDS,
                "strict_ids": [item for name in C.NAMES for item in C.IDS[name]],
                "all_divisions_full_irreducible_terminality_guards": True,
                "engine_and_input_pins": {name: digest for name, (_path, digest) in C.PINS.items()},
            }
    except (C.ContractError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps(answer, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
