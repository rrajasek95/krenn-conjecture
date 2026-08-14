#!/usr/bin/env python3
"""Exact PS_01 mate and its forced pure-head migration at n=8.

The direct-companion audit leaves the cross-head relation
``a_02 M_01-a_01 M_02=0``.  On the same fine matching its unique smallest
PS_01 mate is a new coefficient s_1(site 5, colour 2)=Y.  This checker
verifies that the mate repairs both mixed heads but is reused by p_2 in the
pure 21 row, where the colour-two anchor makes it a unit obstruction.
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
    "verify_n8_f02_direct_companion_head_migration_gate.py"
)
SPEC = spec_from_file_location("f02_direct_migration", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
P = module_from_spec(SPEC)
SPEC.loader.exec_module(P)
B = P.B


Y = B.variable("Y")
B.SECOND[(1, 5, 2)] = Y

WORD = P.WORD
PURE_TWO = (2,) * 6


def monomial(*names):
    return B.product_polynomials(B.variable(name) for name in names)


MATE_01 = monomial("P0", "Y", "a", "e")
C_01 = B.add(P.LEAK_01, MATE_01)
PURE_LEAK_21 = monomial("P2", "Y", "f", "g")


NORMALIZATION = dict(P.NORMALIZATION)
NORMALIZATION["Y"] = Q(-1)


def evaluate(polynomial):
    answer = Q(0)
    for variables, coefficient in polynomial.items():
        term = coefficient
        for name in variables:
            term *= NORMALIZATION[name]
        answer += term
    return answer


def audit_same_fine_classification():
    # On 60|75|14|23, head 01 fixes p_0 at site 0 and s_1 at site 5.
    # The residual word fixes their physical colours to 0 and 2.  Hence Y is
    # the unique new endpoint coefficient on this exact fine matching.
    candidates = []
    for p_site in B.SITES:
        for s_site in B.SITES:
            fine_edges = frozenset((tuple(sorted((6, p_site))), tuple(sorted((7, s_site)))))
            if fine_edges == frozenset(((0, 6), (5, 7))):
                candidates.append((p_site, WORD[p_site], s_site, WORD[s_site]))
    require(candidates == [(0, 0, 5, 2)],
            ("same-fine endpoint classification changed", candidates))
    require(B.FIRST[(0, 0, 0)] == B.V["P0"], "fixed p_0 endpoint moved")
    require(B.SECOND[(1, 5, 2)] == Y, "unique s_1 mate moved")
    return candidates


def audit_typed_migrations():
    typed = (
        {
            "word": "010012", "head": "02", "operation": "PS",
            "fine_matching": "60|75|14|23", "coefficient": Q(1),
        },
        {
            "word": "010012", "head": "02", "operation": "DQ",
            "fine_matching": "67|05|14|23", "coefficient": Q(-1),
        },
        {
            "word": "010012", "head": "01", "operation": "DQ",
            "fine_matching": "67|05|14|23", "coefficient": Q(1),
        },
        {
            "word": "010012", "head": "01", "operation": "PS",
            "fine_matching": "60|75|14|23", "coefficient": Q(-1),
        },
        {
            "word": "222222", "head": "21", "operation": "PS",
            "fine_matching": "62|75|04|13", "coefficient": Q(-1),
        },
        {
            "word": "222222", "head": "22", "operation": "PS",
            "fine_matching": "62|75|04|13", "coefficient": Q(1),
        },
    )
    require(evaluate(P.C_02) == 0, "mixed head 02 reopened")
    require(evaluate(C_01) == 0, "PS_01 mate did not repair mixed head 01")
    require(evaluate(PURE_LEAK_21) == -1, "pure head 21 did not fire")
    require(evaluate(B.A2) == 1, "pure head 22 anchor moved")
    require(B.residual(0, 1, WORD) == C_01, "symbolic mixed head 01 changed")
    require(B.residual(2, 1, PURE_TWO) == PURE_LEAK_21,
            "symbolic pure head 21 changed")
    return typed


def audit_cross_head_relation():
    # F_02=T*F+M_02 and F_01=D*F+M_01.  Eliminating F gives
    # T*M_01-D*M_02 whenever both rows vanish.
    eliminated_rows = B.subtract(
        B.multiply(P.T, C_01),
        B.multiply(B.V["D"], P.C_02),
    )
    response_relation = B.subtract(
        B.multiply(P.T, MATE_01),
        B.multiply(B.V["D"], P.PS_02),
    )
    require(eliminated_rows == response_relation,
            ("cross-head elimination identity changed", eliminated_rows))
    require(evaluate(response_relation) == 0,
            "normalized PS_01 mate missed the required cross-head relation")
    return response_relation


def audit_source_ledger():
    nonzero = []
    for word in product(B.COLORS, repeat=6):
        for row, column in product(B.COLORS, repeat=2):
            value = evaluate(B.residual(row, column, word))
            if value:
                nonzero.append(("".join(map(str, word)), f"{row}{column}", value))
    expected = [
        ("012112", "21", Q(1)),
        ("121200", "01", Q(1)),
        ("121200", "02", Q(-1)),
        ("200021", "10", Q(1)),
        ("222222", "21", Q(-1)),
    ]
    require(nonzero == expected, ("normalized all-word ledger changed", nonzero))
    return nonzero


def audit_apolar_invariance():
    cube = {}
    tangent = {}
    for word in product(B.COLORS, repeat=6):
        cube_value = evaluate(B.contracted_cube(word))
        tangent_value = evaluate(B.contracted_tangent(word))
        if cube_value:
            cube[word] = cube_value
        if tangent_value:
            tangent[word] = tangent_value
    require(cube == {}, ("contracted cube acquired support", cube))
    require(tangent == {(colour,) * 6: Q(-1) for colour in B.COLORS},
            ("contracted tangent identity changed", tangent))
    return tangent


def audit_pure_unit_certificate():
    # G*U_21=A2*M_01, hence A2*C_01-G*U_21=A2*D*H*a*e.
    left = B.subtract(
        B.multiply(B.A2, C_01),
        B.multiply(P.PS_02, PURE_LEAK_21),
    )
    right = monomial("P2", "S2", "f", "g", "D", "H", "a", "e")
    require(left == right, ("pure-head migration identity changed", left))

    inverse = B.product_polynomials((
        B.V["P0"], B.V["S0"], B.V["b"],
        B.V["P1"], B.V["S1"], B.V["c"],
    ))
    require(
        B.multiply(inverse, right)
        == B.multiply(
            B.multiply(B.A0, B.multiply(B.A1, B.A2)),
            B.multiply(B.V["D"], P.H),
        ),
        "pure-leak inverse identity changed",
    )

    # Exact polynomial unit certificate on D=H=1 and the three anchors.
    correction = B.add(
        B.multiply(
            B.subtract(P.H, B.constant(1)),
            B.multiply(
                B.V["D"], B.multiply(B.A0, B.multiply(B.A1, B.A2))
            ),
        ),
        B.add(
            B.multiply(
                B.subtract(B.V["D"], B.constant(1)),
                B.multiply(B.A0, B.multiply(B.A1, B.A2)),
            ),
            B.add(
                B.multiply(B.ANCHORS[0], B.multiply(B.A1, B.A2)),
                B.add(B.multiply(B.ANCHORS[1], B.A2), B.ANCHORS[2]),
            ),
        ),
    )
    certificate = B.subtract(B.multiply(inverse, left), correction)
    require(certificate == B.constant(1),
            ("pure-head Nullstellensatz certificate changed", certificate))
    return inverse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "classification", "typed", "relation", "source", "apolar", "unit"),
        default="all",
    )
    args = parser.parse_args()

    classification = typed = relation = ledger = tangent = inverse = None
    if args.mode in ("all", "classification"):
        classification = audit_same_fine_classification()
    if args.mode in ("all", "typed"):
        typed = audit_typed_migrations()
    if args.mode in ("all", "relation"):
        relation = audit_cross_head_relation()
    if args.mode in ("all", "source"):
        ledger = audit_source_ledger()
    if args.mode in ("all", "apolar"):
        tangent = audit_apolar_invariance()
    if args.mode in ("all", "unit"):
        inverse = audit_pure_unit_certificate()

    report = {
        "mode": args.mode,
        "same_fine_mates": None if classification is None else len(classification),
        "mixed_heads_exact": ["02", "01"],
        "cross_head_relation_value": None if relation is None else int(evaluate(relation)),
        "typed_terms": None if typed is None else len(typed),
        "next_word": "222222",
        "next_head": "21",
        "next_operation": "PS",
        "next_fine_matching": "62|75|04|13",
        "next_value": -1,
        "normalized_residual_rows": None if ledger is None else len(ledger),
        "contracted_cube_support": None if tangent is None else 0,
        "contracted_tangent_support": None if tangent is None else len(tangent),
        "unit_inverse_degree": None if inverse is None else len(next(iter(inverse))),
        "scope": "unique same-fine PS_01 mate; further pure 21 companions open",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 F_02 PS_01 mate / pure-head migration: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
