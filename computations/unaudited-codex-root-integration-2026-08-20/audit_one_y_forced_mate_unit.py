#!/usr/bin/env python3
"""Exact seven-row unit excluding mates for every nonzero-y low-Q stratum.

For every one-y axis and every two-y/Q0=0 conic in
``audit_weight0_dzero_low_support_normal_form.py``, the six cofactors used
below are nonzero.  The ordered 6+2 mixed equations therefore force those
six cells of any prospective mate to zero.  The universally live left
coordinates Q10,Q12 force mate Q5,Q3 to zero.  On that coordinate face, five
pair rows, one triangle row and Q3,Q5 give the constant two by a literal
polynomial identity.

The identity is characteristic-zero theorem data.  It is not a claim in
characteristic two.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "audit_polarized_superpair_core_identity.py")
NORMAL_FORM_RESULT = HERE / "results_weight0_dzero_low_support_normal_form.json"
OUT = HERE / "results_one_y_forced_mate_unit.json"
LEFT_NONZERO_COFACTORS = frozenset((3, 7, 9, 10, 13, 14, 19, 23))
# The full left signature forces all eight cells above to zero in a mate, but
# the compact identity itself needs only this minimal six-cell subset.
ZERO_CELLS = frozenset((3, 7, 13, 14, 19, 23))
FORCED_MATE_SUPPORT = frozenset((0, 1, 2, 4, 7, 8, 11, 13))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load("root_one_y_unit_core", CORE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def raw_variable(index):
    return Counter({(index,): 1})


def specialize(poly):
    return CORE.clean(Counter({monomial: coefficient
                               for monomial, coefficient in poly.items()
                               if not any(variable in ZERO_CELLS
                                          for variable in monomial)}))


def q_poly(index):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    return CORE.q_orientation(bits)


def serialize(poly):
    return [{"variables": list(monomial), "coefficient": coefficient}
            for monomial, coefficient in sorted(poly.items())]


def main():
    normal_form = json.loads(NORMAL_FORM_RESULT.read_text())
    q1_record = next(record for record in normal_form["one_y_signatures"]
                     if record["coordinate"] == "Q1")
    require(frozenset(q1_record["cofactor_nonzero_indices"])
            == LEFT_NONZERO_COFACTORS,
            "left Q1 cofactor support changed")
    require(ZERO_CELLS < LEFT_NONZERO_COFACTORS,
            "the compact zero-cell subset changed")
    require(all(frozenset(record["cofactor_nonzero_indices"])
                == LEFT_NONZERO_COFACTORS
                for record in normal_form["one_y_signatures"]),
            "the four one-y axes no longer have one cofactor signature")
    conic_resultants = normal_form["two_y_Q0_conic_cofactor_resultants"]
    require(len(conic_resultants) == 6
            and all(len(record) == 4 for record in conic_resultants.values()),
            "the two-y cofactor resultant table is incomplete")
    left_support = frozenset(q1_record["Q_nonzero_indices"])
    universe = frozenset(range(16))
    forced_mate = frozenset(15 - index for index in universe - left_support)
    require(forced_mate == FORCED_MATE_SUPPORT,
            "unique complementary mate support changed")
    require(3 not in forced_mate and 5 not in forced_mate,
            "Q3 or Q5 entered the forced mate support")

    rows = {
        "e01": CORE.e_pair(0, 1),
        "e02": CORE.e_pair(0, 2),
        "e12": CORE.e_pair(1, 2),
        "e13": CORE.e_pair(1, 3),
        "e23": CORE.e_pair(2, 3),
        "t123": CORE.t_triple(1, 2, 3),
        "Q3": q_poly(3),
        "Q5": q_poly(5),
    }
    multipliers = {
        "e01": CORE.multiply(raw_variable(15), raw_variable(16),
                              raw_variable(21)),
        "e02": CORE.multiply(raw_variable(15), raw_variable(17),
                              raw_variable(20)),
        "e12": CORE.ONE,
        "e13": CORE.ONE,
        "e23": CORE.ONE,
        "t123": CORE.scale(CORE.ONE, -1),
        "Q3": CORE.scale(CORE.multiply(raw_variable(6), raw_variable(15),
                                        raw_variable(20)), -1),
        "Q5": CORE.scale(CORE.multiply(raw_variable(2), raw_variable(15),
                                        raw_variable(16)), -1),
    }
    rhs = CORE.add(*(CORE.multiply(multipliers[name], rows[name])
                     for name in rows))
    two = CORE.scale(CORE.ONE, 2)
    require(specialize(rhs) == two,
            "the specialized seven-row unit identity failed")

    # Lift the face identity back to the full polynomial ring explicitly:
    # every term of 2-rhs is assigned to its least zero-cell divisor.
    residual = CORE.add(two, CORE.scale(rhs, -1))
    zero_multipliers = {variable: Counter() for variable in ZERO_CELLS}
    for monomial, coefficient in residual.items():
        divisors = sorted(variable for variable in ZERO_CELLS
                          if variable in monomial)
        require(divisors, "a residual term has no zero-cell divisor")
        divisor = divisors[0]
        quotient = list(monomial)
        quotient.remove(divisor)
        zero_multipliers[divisor][tuple(quotient)] += coefficient
    lifted = CORE.add(rhs, *(CORE.multiply(raw_variable(variable), multiplier)
                             for variable, multiplier
                             in zero_multipliers.items()))
    require(lifted == two, "the full-ring zero-cell lift failed")

    # Every displayed source row is load-bearing for this particular compact
    # identity.  The face mutation also guards the cell convention.
    for omitted in rows:
        mutated = CORE.add(*(CORE.multiply(multipliers[name], rows[name])
                             for name in rows if name != omitted))
        require(specialize(mutated) != two,
                f"row-deletion mutation did not fire for {omitted}")
    for omitted in ZERO_CELLS:
        remaining = ZERO_CELLS - {omitted}
        require(any(not any(variable in remaining for variable in monomial)
                    for monomial in residual),
                f"zero-cell deletion did not fire for x{omitted}")

    result = {
        "status": "UNAUDITED exact one-y forced-mate unit",
        "left_class": (
            "all one-y axes and all two-y/Q0=0 conics on the weight-zero "
            "d=0 normal form"
        ),
        "Q1_axis_control": "representative used for the displayed masks",
        "left_Q_support": sorted(left_support),
        "left_nonzero_cofactor_cells": sorted(LEFT_NONZERO_COFACTORS),
        "minimal_zero_cells_used_by_identity": sorted(ZERO_CELLS),
        "forced_mate_Q_support": sorted(FORCED_MATE_SUPPORT),
        "identity_on_forced_cell_face": (
            "2=x15*x16*x21*e01+x15*x17*x20*e02+e12+e13+e23-t123"
            "-x6*x15*x20*Q3-x2*x15*x16*Q5"
        ),
        "source_rows": list(rows),
        "zero_cell_multiplier_term_counts": {
            str(variable): len(CORE.clean(poly))
            for variable, poly in sorted(zero_multipliers.items())
        },
        "full_ring_residual_term_count": len(residual),
        "characteristic_scope": "valid whenever 2 is nonzero; in particular over C",
        "conclusion": (
            "No point in any cofactor branch can be a diagonal-packet mate "
            "for any nonzero-y support-at-most-eight point on the chart.  "
            "Together with the separate support-six certificate this "
            "closes the entire localized chart against arbitrary mates."
        ),
        "scope": (
            "This closes arbitrary mates for the nonzero-y normal-form "
            "classes.  It does not classify unrelated low-support left "
            "components outside the localized weight-zero d=0 chart."
        ),
        "zero_cell_multipliers": {
            str(variable): serialize(CORE.clean(poly))
            for variable, poly in sorted(zero_multipliers.items()) if poly
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("one-y forced-mate unit: PASS")
    print("rows/residual terms:", len(rows), len(residual))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
