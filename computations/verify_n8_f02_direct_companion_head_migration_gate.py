#!/usr/bin/env python3
"""Audit the smallest DQ companion of the F_02(010012) selector.

Starting from the support-minimal fibre certified in
``verify_n8_full_nine_minimal_apolar_hall_saturation.py``, add the mixed
internal cell q_05(0,2)=H and the direct head a_02=T.  Their DQ term can
cancel the selected PS term, but the same q^[3] monomial then appears under
the already active head 01.  This checker retains word, head, operation,
and fine matching labels and verifies the exact localized unit certificate.
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


BASE_PATH = Path(__file__).with_name(
    "verify_n8_full_nine_minimal_apolar_hall_saturation.py"
)
SPEC = spec_from_file_location("minimal_apolar_saturation", BASE_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load base audit")
B = module_from_spec(SPEC)
SPEC.loader.exec_module(B)


H = B.variable("H")
T = B.variable("T")
B.Q_EDGE[(0, 5, 0, 2)] = H
B.DIRECT[(0, 2)] = T

WORD = (0, 1, 0, 0, 1, 2)
WORD_TEXT = "010012"


def monomial(*names):
    return B.product_polynomials(B.variable(name) for name in names)


PS_02 = monomial("P0", "S2", "a", "e")
DQ_02 = monomial("T", "H", "a", "e")
C_02 = B.add(PS_02, DQ_02)
LEAK_01 = monomial("D", "H", "a", "e")


NORMALIZATION = {
    "a": Q(1), "b": Q(1), "c": Q(1), "e": Q(1),
    "f": Q(1), "g": Q(1),
    "P0": Q(1), "S0": Q(1), "P1": Q(1), "S1": Q(1),
    "P2": Q(1), "S2": Q(1), "D": Q(1), "H": Q(1), "T": Q(-1),
}


def evaluate(polynomial):
    answer = Q(0)
    for variables, coefficient in polynomial.items():
        term = coefficient
        for name in variables:
            term *= NORMALIZATION[name]
        answer += term
    return answer


def audit_typed_corner():
    typed = (
        {
            "word": WORD_TEXT,
            "head": "02",
            "operation": "PS",
            "fine_matching": "60|75|14|23",
            "coefficient": evaluate(PS_02),
        },
        {
            "word": WORD_TEXT,
            "head": "02",
            "operation": "DQ",
            "fine_matching": "67|05|14|23",
            "coefficient": evaluate(DQ_02),
        },
        {
            "word": WORD_TEXT,
            "head": "01",
            "operation": "DQ",
            "fine_matching": "67|05|14|23",
            "coefficient": evaluate(LEAK_01),
        },
    )
    require(
        tuple(entry["coefficient"] for entry in typed) == (Q(1), Q(-1), Q(1)),
        ("typed corner changed", typed),
    )
    require(evaluate(C_02) == 0, "the 02 selector did not cancel")
    require(evaluate(LEAK_01) == 1, "the 01 head leak vanished")
    return typed


def audit_source_ledger():
    nonzero = []
    for word in product(B.COLORS, repeat=6):
        for row, column in product(B.COLORS, repeat=2):
            value = evaluate(B.residual(row, column, word))
            if value:
                nonzero.append(("".join(map(str, word)), f"{row}{column}", value))
    expected = [
        ("010012", "01", Q(1)),
        ("012112", "21", Q(1)),
        ("121200", "01", Q(1)),
        ("121200", "02", Q(-1)),
        ("200021", "10", Q(1)),
    ]
    require(nonzero == expected, ("normalized full-row ledger changed", nonzero))
    require(evaluate(B.residual(0, 2, WORD)) == 0, "selected row is not exact")
    require(
        B.residual(0, 2, WORD) == C_02,
        "symbolic selected row lost its two fine summands",
    )
    require(
        B.residual(0, 1, WORD) == LEAK_01,
        "symbolic head leak changed",
    )
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
    require(
        tangent == {(colour,) * 6: Q(-1) for colour in B.COLORS},
        ("contracted common-power identity changed", tangent),
    )
    return tangent


def audit_head_migration_certificate():
    # The exact two-head identity before imposing either row is
    # T*F_01-D*F_02=-D*PS_02.
    left = B.subtract(
        B.multiply(T, LEAK_01),
        B.multiply(B.V["D"], C_02),
    )
    require(left == B.negate(B.multiply(B.V["D"], PS_02)),
            ("two-head migration identity changed", left))

    # PS_02 is a unit modulo the three pure anchors.  Reuse the degree-eight
    # monomial inverse from the minimal-fibre certificate.
    inverse = B.product_polynomials((
        B.V["S0"], B.V["b"],
        B.V["P2"], B.V["f"], B.V["g"],
        B.V["P1"], B.V["S1"], B.V["c"],
    ))
    require(
        B.multiply(inverse, PS_02) == B.multiply(B.A0, B.multiply(B.A1, B.A2)),
        "selected PS monomial lost its anchor inverse",
    )

    # Ordinary Nullstellensatz certificate on the normalized D=1 chart:
    # 1 = inverse*(D*C_02-T*LEAK_01)
    #     -(D-1)A0A1A2-(A0-1)A1A2-(A1-1)A2-(A2-1).
    dc_minus_tl = B.subtract(
        B.multiply(B.V["D"], C_02),
        B.multiply(T, LEAK_01),
    )
    correction = B.add(
        B.multiply(
            B.subtract(B.V["D"], B.constant(1)),
            B.multiply(B.A0, B.multiply(B.A1, B.A2)),
        ),
        B.add(
            B.multiply(B.ANCHORS[0], B.multiply(B.A1, B.A2)),
            B.add(B.multiply(B.ANCHORS[1], B.A2), B.ANCHORS[2]),
        ),
    )
    certificate = B.subtract(B.multiply(inverse, dc_minus_tl), correction)
    require(certificate == B.constant(1),
            ("normalized head-migration unit certificate changed", certificate))
    return inverse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "typed", "source", "apolar", "colon"),
        default="all",
    )
    args = parser.parse_args()

    typed = ledger = tangent = inverse = None
    if args.mode in ("all", "typed"):
        typed = audit_typed_corner()
    if args.mode in ("all", "source"):
        ledger = audit_source_ledger()
    if args.mode in ("all", "apolar"):
        tangent = audit_apolar_invariance()
    if args.mode in ("all", "colon"):
        inverse = audit_head_migration_certificate()

    report = {
        "mode": args.mode,
        "selected_word": WORD_TEXT,
        "selected_head": "02",
        "selected_row_after_companion": 0,
        "first_surviving_head": "01",
        "first_surviving_operation": "DQ",
        "first_surviving_fine_matching": "67|05|14|23",
        "first_surviving_value": 1,
        "typed_terms": None if typed is None else len(typed),
        "normalized_residual_rows": None if ledger is None else len(ledger),
        "contracted_cube_support": None if tangent is None else 0,
        "contracted_tangent_support": None if tangent is None else len(tangent),
        "anchor_inverse_degree": None if inverse is None else len(next(iter(inverse))),
        "scope": "one added DQ companion cell and head; general PS_01 transport open",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 F_02 direct-companion head migration: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
