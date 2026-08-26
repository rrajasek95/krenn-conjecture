#!/usr/bin/env python3
"""Exact compact unit excluding a forced mate of a one-y axis.

The one-y axes in the branch-51 d=0 normal form have nonzero cofactors at
cells {3,7,9,10,13,14,19,23}.  Cross 6+2 rows therefore force those eight
cells of a putative mate to zero.  Its unique Q-compatible support also has
Q3=Q5=0.  On that coordinate section the identity checked here reads

  2 = x15*x16*x21*e01 + x15*x17*x20*e02 + e12+e13+e23 - t123
      - x6*x15*x20*Q3 - x2*x15*x16*Q5.

Thus the mate's own pair/triangle/Q rows generate the unit.  The calculation
is in the literal raw 24-variable polynomial ring.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "audit_polarized_superpair_core_identity.py"
OUT = HERE / "results_one_y_forced_mate_unit.json"
FORCED_ZERO_CELLS = frozenset((3, 7, 9, 10, 13, 14, 19, 23))


def load_core():
    spec = importlib.util.spec_from_file_location("n8_one_y_unit_core",
                                                  CORE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_core()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def raw_variable(index):
    return Counter({(index,): 1})


def q_index(index):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    return CORE.q_orientation(bits)


def specialize_zero(poly, zero_cells):
    return Counter({monomial: coefficient
                    for monomial, coefficient in poly.items()
                    if not set(monomial) & zero_cells})


def main():
    x = raw_variable
    rhs_minus_two = CORE.add(
        CORE.multiply(x(15), x(16), x(21), CORE.e_pair(0, 1)),
        CORE.multiply(x(15), x(17), x(20), CORE.e_pair(0, 2)),
        CORE.e_pair(1, 2), CORE.e_pair(1, 3), CORE.e_pair(2, 3),
        CORE.scale(CORE.t_triple(1, 2, 3), -1),
        CORE.scale(CORE.multiply(x(6), x(15), x(20), q_index(3)), -1),
        CORE.scale(CORE.multiply(x(2), x(15), x(16), q_index(5)), -1),
        CORE.scale(CORE.ONE, -2),
    )
    require(rhs_minus_two,
            "unspecialized identity unexpectedly became literal zero")
    residual = specialize_zero(rhs_minus_two, FORCED_ZERO_CELLS)
    require(not residual, "forced-mate unit identity failed")

    restore_controls = {}
    for restored in sorted(FORCED_ZERO_CELLS):
        restored_residual = specialize_zero(
            rhs_minus_two, FORCED_ZERO_CELLS - {restored})
        restore_controls[str(restored)] = {
            "residual_term_count": len(restored_residual),
            "fires": bool(restored_residual),
        }
    essential_cells = tuple(index for index in sorted(FORCED_ZERO_CELLS)
                            if restore_controls[str(index)]["fires"])
    require(essential_cells == (3, 7, 13, 14, 19, 23),
            "identity essential-cell control changed")

    result = {
        "status": "UNAUDITED exact raw-polynomial unit identity",
        "forced_zero_cells": sorted(FORCED_ZERO_CELLS),
        "forced_Q_zeros": [3, 5],
        "identity": (
            "2=x15*x16*x21*e01+x15*x17*x20*e02+e12+e13+e23-t123"
            "-x6*x15*x20*Q3-x2*x15*x16*Q5"
        ),
        "unspecialized_residual_term_count": len(rhs_minus_two),
        "specialized_residual_term_count": len(residual),
        "essential_zero_cells_for_this_identity": list(essential_cells),
        "restore_one_cell_controls": restore_controls,
        "consequence": (
            "If the eight forced cells and e01,e02,e12,e13,e23,t123,Q3,Q5 "
            "vanish, then 2=0; hence no characteristic-zero forced mate."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("one-y forced-mate unit: PASS")
    print("unspecialized / specialized terms:", len(rhs_minus_two),
          len(residual))
    print("essential restored-cell controls:", essential_cells)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
