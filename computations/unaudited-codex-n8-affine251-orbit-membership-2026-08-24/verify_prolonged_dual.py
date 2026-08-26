#!/usr/bin/env python3
"""Exact D8 dual prolongation and stable-incidence referee.

For lambda_D(r*t^(D-8)) = lambda_8(r), zero elsewhere, verify every
incident orbit column exactly for D=8..13.  At D=12 all seven support rows
contain at least four t's, so the D12->D13 incidence shift is the stable
pattern for every later degree.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from audit_affine251_orbit import (
    T, IndependentEngine, build_actions, lift_rational_dual, parse_dual,
    parse_provider, read_checkpoint, sha256,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--checkpoint-d8", type=Path, required=True)
    parser.add_argument("--dual-primary", type=Path, required=True)
    parser.add_argument("--dual-secondary", type=Path, required=True)
    parser.add_argument("--prime-primary", type=int, default=1073741827)
    parser.add_argument("--prime-secondary", type=int, default=1073741789)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows8, _ = read_checkpoint(args.checkpoint_d8, 8)
    sorted_rows8 = sorted(rows8)
    modular1, pairing1 = parse_dual(args.dual_primary, args.prime_primary, sorted_rows8)
    modular2, pairing2 = parse_dual(args.dual_secondary, args.prime_secondary, sorted_rows8)
    assert pairing1 == pairing2 == 1
    rational_by_id = lift_rational_dual(
        modular1, modular2, args.prime_primary, args.prime_secondary
    )
    rational8 = {sorted_rows8[row]: value for row, value in rational_by_id.items()}
    assert len(rational8) == 7 and max(x.denominator for x in rational8.values()) == 2
    assert rational8[(T,) * 8] == 1

    header, polynomials, term_index = parse_provider(args.input)
    engine = IndependentEngine(build_actions(header), polynomials, term_index)
    records = []
    degree_columns = {}
    degree_support = {}
    failure = None
    for degree in range(8, 14):
        shift = (T,) * (degree - 8)
        support = {tuple(sorted(row + shift)): value for row, value in rational8.items()}
        assert len(support) == 7 and support[(T,) * degree] == 1
        columns = set()
        for row in support:
            columns.update(engine.incident(row))
        bad = None
        for column in sorted(columns):
            values = engine.invariant_column_integer(column)
            pairing = sum(coefficient * support.get(row, Fraction(0))
                          for row, coefficient in values.items())
            if pairing != 0:
                bad = (column, pairing)
                break
        degree_columns[degree] = columns
        degree_support[degree] = support
        records.append({
            "degree": degree,
            "support": len(support),
            "incident_column_orbits_checked": len(columns),
            "target_pairing": "1",
            "all_column_pairings_zero": bad is None,
            "minimum_t_multiplicity_in_support": min(row.count(T) for row in support),
        })
        if bad is not None:
            failure = {
                "degree": degree,
                "word": bad[0][0],
                "multiplier": "".join(f"{value:02x}" for value in bad[0][1]),
                "exact_pairing": str(bad[1]),
            }
            break

    assert failure is not None and failure["degree"] == 12

    result = {
        "schema": "KRENN_AFFINE251_PROLONGED_RATIONAL_DUAL_V1",
        "status": "PASS_D8_D11_PROLONGATION_D12_COUNTERWITNESS",
        "input_sha256": sha256(args.input),
        "checkpoint_d8_sha256": sha256(args.checkpoint_d8),
        "dual_primary_sha256": sha256(args.dual_primary),
        "dual_secondary_sha256": sha256(args.dual_secondary),
        "rational_dual_support": len(rational8),
        "maximum_denominator": 2,
        "degrees": records,
        "prolongation_valid_degrees": [8, 9, 10, 11],
        "first_failure": failure,
        "all_degrees_at_least_8_nonmembership": False,
        "conclusion": "the seven-entry D8 dual cannot replace the D12 solve",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
