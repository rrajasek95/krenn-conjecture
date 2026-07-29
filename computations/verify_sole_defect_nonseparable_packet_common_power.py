#!/usr/bin/env python3
"""Primary exact replay for all 157 sole-defect packet obstructions.

The support census retains only projected packet systems having no locally
separable SDR.  Of the resulting 157 canonical orbits, 145 have all
coefficients normalizable to one and twelve have one nonzero full-packet
invariant.  This driver reconstructs both classes and checks every exact
common-power ideal through their dedicated builders.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib

from explore_sole_defect_nonseparable_packet_orbits import (
    TYPES,
    census,
    nonseparable_only_representatives,
)
import verify_sole_defect_nonseparable_normalizable_packets as normalized
import verify_sole_defect_nonseparable_parameter_packets as parameter


EXPECTED_COUNTS = {
    "circuit_k2": (294, 6, 6, 0),
    "coincident_k1": (85, 14, 14, 0),
    "coincident_k2": (560, 64, 58, 6),
    "rank1_k1": (51, 9, 9, 0),
    "rank1_k2": (294, 64, 58, 6),
}

# Ordered stream ``class:type:case:per-case-ledger-sha256``.
EXPECTED_GLOBAL = "7e766f3e56aee47b3b623dcbc1c5db60ac145deaa735c543746507a5fe1295f4"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--ledger-only", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    global_ledger = hashlib.sha256()
    status_counts = Counter()
    total_initial = total_residual = total_normalized = total_parameter = 0

    for name, kind, killed in TYPES:
        initial = len(census(name))
        residual = len(nonseparable_only_representatives(name))
        normalized_reps = normalized.representatives(name)
        parameter_reps = parameter.representatives(name)
        counts = (initial, residual, len(normalized_reps), len(parameter_reps))
        assert counts == EXPECTED_COUNTS[name]
        print(
            name,
            {"initial": initial, "residual": residual,
             "normalized": len(normalized_reps),
             "parameter": len(parameter_reps)},
            flush=True,
        )
        total_initial += initial
        total_residual += residual
        total_normalized += len(normalized_reps)
        total_parameter += len(parameter_reps)

        normalized_combined = hashlib.sha256()
        for case in range(len(normalized_reps)):
            result = normalized.run(
                case, name, kind, args.timeout, not args.ledger_only
            )
            if args.verbose:
                print(result, flush=True)
            status_counts[result["status"]] += 1
            if not args.ledger_only:
                assert result["status"] == "UNIT", result
            normalized_combined.update(
                f'{case}:{result["sha256"]}\n'.encode("ascii")
            )
            global_ledger.update(
                f'N:{name}:{case}:{result["sha256"]}\n'.encode("ascii")
            )
        assert normalized_combined.hexdigest() == normalized.EXPECTED_COMBINED[name]

        if parameter_reps:
            parameter_combined = hashlib.sha256()
            for case in range(len(parameter_reps)):
                result = parameter.run(
                    case, name, kind, args.timeout, not args.ledger_only
                )
                if args.verbose:
                    print(result, flush=True)
                status_counts[result["status"]] += 1
                if not args.ledger_only:
                    assert result["status"] == "UNIT", result
                parameter_combined.update(
                    f'{case}:{result["sha256"]}\n'.encode("ascii")
                )
                global_ledger.update(
                    f'P:{name}:{case}:{result["sha256"]}\n'.encode("ascii")
                )
            assert parameter_combined.hexdigest() == parameter.EXPECTED_COMBINED[name]

    assert (total_initial, total_residual, total_normalized, total_parameter) == (
        1284, 157, 145, 12
    )
    global_digest = global_ledger.hexdigest()
    print("totals", {
        "initial": total_initial,
        "residual": total_residual,
        "normalized": total_normalized,
        "parameter": total_parameter,
        "statuses": dict(status_counts),
    }, flush=True)
    print("global ledger sha256:", global_digest, flush=True)
    assert global_digest == EXPECTED_GLOBAL
    print("all 157 sole-defect nonseparable packet ideals: PASS")


if __name__ == "__main__":
    main()
