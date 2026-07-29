#!/usr/bin/env python3
"""Re-run the six-vertex support CEGAR with deletion certificates over F_2.

The main support audit searches for diagonal infinitesimal stabilizers over
Q.  This discovery variant replaces only those affine-consistency tests by
exact bit Gaussian elimination.  It tests whether the same support proof is
available in characteristic two; it is not by itself a proof over the
algebraic closure.
"""

from __future__ import annotations

import argparse

import verify_color_sensitive_support_obstruction as base


def affine_consistent_f2(supports, killed, fixed=()):
    rows = []
    rhs = []
    for u, v in killed:
        for a, b in supports[u, v]:
            rows.append(base.equation_row(u, v, a, b))
            rhs.append(0)
    for (u, v), value in fixed:
        for a, b in supports[u, v]:
            rows.append(base.equation_row(u, v, a, b))
            rhs.append(value & 1)
    rows.extend(base.SUM_ROWS)
    rhs.extend((1, 1, 1))

    packed = []
    for row, value in zip(rows, rhs):
        mask = sum((coefficient & 1) << index for index, coefficient in enumerate(row))
        packed.append(mask | ((value & 1) << 18))

    pivot_row = 0
    for column in range(18):
        pivot = next(
            (index for index in range(pivot_row, len(packed)) if (packed[index] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        packed[pivot_row], packed[pivot] = packed[pivot], packed[pivot_row]
        for index in range(len(packed)):
            if index != pivot_row and ((packed[index] >> column) & 1):
                packed[index] ^= packed[pivot_row]
        pivot_row += 1
    coefficient_mask = (1 << 18) - 1
    return not any((row & coefficient_mask) == 0 and ((row >> 18) & 1) for row in packed)


def main():
    cases = (
        ("C3+3P1", {(0, 1), (0, 2), (1, 2)}),
        ("P4+2P1", {(0, 1), (1, 2), (2, 3)}),
        ("P3+P2+P1", {(0, 1), (1, 2), (3, 4)}),
        ("2P2+2P1", {(0, 1), (2, 3)}),
        ("P3+3P1", {(0, 1), (1, 2)}),
        ("P2+4P1", {(0, 1)}),
        ("empty", set()),
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=tuple(name for name, _ in cases))
    args = parser.parse_args()
    base.affine_consistent = affine_consistent_f2
    for name, exceptional in cases:
        if args.only is None or args.only == name:
            if not base.audit(name, exceptional):
                raise SystemExit(1)


if __name__ == "__main__":
    main()
