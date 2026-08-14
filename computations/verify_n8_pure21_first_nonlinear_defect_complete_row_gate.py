#!/usr/bin/env python3
"""Complete-row chase of the first nonlinear pure-21 dual defect.

The first symbolic defect in the endpoint-fixed octagon audit is the DQ
monomial ``-D*c*g*q45`` at word/head 121222:01.  This checker restores its
complete three-matching row, verifies that the rational torus witness does
cancel that row, and then replays all 6561 residual rows.  The witness has 24
nonzero changes.  The lexicographically first is the unique PS_00 monomial
``P0*S0*a*q45`` at 000022:00, which is a unit after the inherited
normalization and the active-q45 localization.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


PARENT_PATH = Path(__file__).with_name(
    "verify_n8_pure21_octagon_nonlinear_completion_gate.py"
)
SPEC = spec_from_file_location("nonlinear_octagon_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
N = module_from_spec(SPEC)
SPEC.loader.exec_module(N)
B = N.B
M = N.M


DEFECT_ROW = ((1, 2, 1, 2, 2, 2), 0, 1)
NEXT_ROW = ((0, 0, 0, 0, 2, 2), 0, 0)
ROWS = tuple(
    (word, row, column)
    for word in product(B.COLORS, repeat=6)
    for row in B.COLORS
    for column in B.COLORS
)


def witness():
    values = dict(M.P.NORMALIZATION)
    values.update({
        "z0": Q(1), "z1": Q(1), "z3": Q(1), "z4": Q(-2),
        "q01": Q(1), "q03": Q(-1), "q05": Q(1), "q14": Q(1),
        "q15": Q(1), "q34": Q(1), "q35": Q(1), "q45": Q(-2),
    })
    require(all(values[name] for name in N.NAMES), "witness left the source torus")
    return values


WITNESS = witness()


def symbolic_differences():
    M.reset_tables()
    base = {
        key: B.residual(key[1], key[2], key[0])
        for key in ROWS
    }
    N.adjoin_symbolic()
    differences = {
        key: B.subtract(B.residual(key[1], key[2], key[0]), base[key])
        for key in ROWS
    }
    return base, differences


def audit_complete_defect_row():
    base, differences = symbolic_differences()
    expected = N.polynomial((
        (("D", "c", "g", "q45"), 1),
        (("D", "c", "q14", "q35"), 1),
        (("D", "c", "q15", "q34"), 1),
    ))
    require(not base[DEFECT_ROW], "the inherited defect row was not zero")
    require(differences[DEFECT_ROW] == expected,
            ("complete first-defect row changed", differences[DEFECT_ROW]))
    term_values = tuple(
        N.evaluate_at({monomial: coefficient}, WITNESS)
        for monomial, coefficient in sorted(expected.items())
    )
    require(term_values == (Q(-2), Q(1), Q(1)),
            ("complete-row mate values moved", term_values))
    require(N.evaluate_at(expected, WITNESS) == 0,
            "rational torus witness no longer cancels the complete defect row")

    typed = (
        ("121222", "01", "DQ", "67|02|13|45", "D*c*g*q45", -2),
        ("121222", "01", "DQ", "67|02|14|35", "D*c*q14*q35", 1),
        ("121222", "01", "DQ", "67|02|15|34", "D*c*q15*q34", 1),
    )
    M.reset_tables()
    return typed


EXPECTED_LEDGER = (
    ("000022", "00", -2),
    ("002222", "20", 1),
    ("012212", "21", 1),
    ("020000", "01", 1),
    ("020022", "01", -4),
    ("022122", "21", 1),
    ("101221", "10", 1),
    ("111211", "11", 1),
    ("111212", "01", 1),
    ("111212", "02", -1),
    ("121121", "11", 1),
    ("202200", "20", -1),
    ("202222", "20", 4),
    ("210011", "11", 1),
    ("210012", "01", 1),
    ("210012", "02", -1),
    ("212112", "21", 1),
    ("212212", "21", 3),
    ("212212", "22", -1),
    ("220000", "01", 1),
    ("220000", "02", -1),
    ("222100", "21", 1),
    ("222200", "21", 1),
    ("222222", "21", 2),
)


def audit_full_row_replay():
    base, differences = symbolic_differences()
    ledger = tuple(
        ("".join(map(str, key[0])), f"{key[1]}{key[2]}", int(value))
        for key in ROWS
        if (value := N.evaluate_at(differences[key], WITNESS))
    )
    require(ledger == EXPECTED_LEDGER, ("full 6561-row ledger changed", ledger))
    require(N.evaluate_at(differences[DEFECT_ROW], WITNESS) == 0,
            "the complete-row constraint reopened")
    require(ledger[0] == ("000022", "00", -2),
            ("first surviving row moved", ledger[0]))

    expected_next = N.polynomial(((('P0', 'S0', 'a', 'q45'), 1),))
    require(not base[NEXT_ROW], "the inherited next row was not zero")
    require(differences[NEXT_ROW] == expected_next,
            ("first surviving polynomial changed", differences[NEXT_ROW]))
    M.reset_tables()
    return ledger


def audit_localized_unit_certificate():
    variables = {name: B.variable(name) for name in ("P0", "S0", "a", "q45")}
    one = B.constant(1)
    p0_minus = B.subtract(variables["P0"], one)
    s0_minus = B.subtract(variables["S0"], one)
    a_minus = B.subtract(variables["a"], one)
    normalization_error = B.add(
        B.multiply(p0_minus, B.multiply(variables["S0"], variables["a"])),
        B.add(B.multiply(s0_minus, variables["a"]), a_minus),
    )
    p0s0a_minus_one = B.subtract(
        B.product_polynomials((variables["P0"], variables["S0"], variables["a"])),
        one,
    )
    require(normalization_error == p0s0a_minus_one,
            ("normalization telescope changed", normalization_error))

    residual = B.product_polynomials((
        variables["P0"], variables["S0"], variables["a"], variables["q45"],
    ))
    require(
        residual == B.multiply(
            variables["q45"], B.add(one, normalization_error)
        ),
        "localized unit identity changed",
    )
    # Dividing this identity by active q45 gives the Laurent certificate
    # 1=q45^{-1}*residual-normalization_error.
    require(N.evaluate_at(residual, WITNESS) == Q(-2),
            "unit row stopped detecting the rational torus witness")
    return {
        "identity": "1=q45^-1*(P0*S0*a*q45)-[(P0-1)S0a+(S0-1)a+(a-1)]",
        "operation": "PS",
        "word_head": "000022:00",
        "fine_matching": "60|71|23|45",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "complete-row", "replay", "unit"), default="all"
    )
    args = parser.parse_args()

    typed = ledger = unit = None
    if args.mode in ("all", "complete-row"):
        typed = audit_complete_defect_row()
    if args.mode in ("all", "replay"):
        ledger = audit_full_row_replay()
    if args.mode in ("all", "unit"):
        unit = audit_localized_unit_certificate()

    report = {
        "mode": args.mode,
        "complete_defect_row_terms": None if typed is None else len(typed),
        "complete_defect_row_witness_values": [-2, 1, 1],
        "full_rows_replayed": 6561,
        "nonzero_witness_rows": None if ledger is None else len(ledger),
        "first_surviving_typed_face": unit,
        "rational_torus_counterguard_survives": False,
        "scope": "first endpoint-fixed 12-cell nonlinear torus fibre",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 first nonlinear defect complete-row gate: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
