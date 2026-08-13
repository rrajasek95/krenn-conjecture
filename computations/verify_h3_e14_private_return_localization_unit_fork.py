#!/usr/bin/env python3
"""Separate the E14 private-return localization from physical row typing.

For the canonical unary S-pair put ``a=1-v04`` and write

    B = U + a*g.

The V(a) branch has B=U and v04=1, hence is already target-trivial and
response-bright.  On D(a), multiplication by a is invertible, so landing the
return is equivalent to landing g.  Splitting D(a) by v04 leaves either the
same response-bright route or the silent fibre v04=0, where a=1 and the
missing theorem is literally the same-grade primitive occurrence placement.

The pinned E14 unit theorems close a fully typed row in the canonical fibre
with at most two new internal cells.  They cannot be applied to the bare
coefficient equality B=U+a*g before word/fine/repeated-grade and all proper
faces of the physical placement have been supplied.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
    "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py":
        "754038f33ae07329e0fc6a8825df9f1695664a40df91afbb77e52dedb1e1aae1",
    "notes/h3-e14-cplus-keq-companion-assembly-gate.md":
        "8548c1db8ec362fce0876c0f67d77efc96f141ebd4c82b6564069e3a089eff3a",
    "computations/verify_h3_four_base_silent_c6_response_lock.py":
        "dc4daa2d200f184b5d00d29c4db175320935a189f5590836afa0c724d3fdac8a",
    "notes/h3-four-base-silent-c6-response-lock.md":
        "54d7278e49e8195ed2262fa37cc89936f718b3bcd192884c6473c736a68354b8",
    "computations/verify_h3_c6_e14_minimal_enlargement_unit.py":
        "d5682f9134ff3dafddb4908707e5ceaacb25ff8b37632e57d9f9f3a4b62f84a8",
    "notes/h3-c6-e14-minimal-enlargement-unit.md":
        "552adf8a24410d4b8a09e61809c9a40c40274ad9c49a7ffe01b7ceb0d5ea22a7",
    "computations/verify_h3_c6_e14_pure11_unary_unit.py":
        "07160a67a4a16885fe481265ce67a372117b323dea82819e220cbe79e131df2d",
    "notes/h3-c6-e14-pure11-unary-unit.md":
        "cc9603e2f63e5b3de3b80dbf144a4f559f6e21f168fd9dfe9d5f95c4c7467ec4",
    "computations/verify_h3_c6_e14_two_cell_unit_frontier.py":
        "b5a2609b64f5a0bf1720a3c571c6c4d28aa316df00129f5b4574e0f32b8c3971",
    "notes/h3-c6-e14-two-cell-unit-frontier.md":
        "07593c3ebeb95b76461792c9835810f2b81e2b2ba701a9c910ea75c2b63809f1",
}
EXPECTED_LEDGER_SHA256 = (
    "a805413bad45f999f08c183984432ca242d3ba8462da7b1f1aed14ad0fc91425"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(scalar: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(scalar) * entry for entry in vector)


def exact_spair_localization() -> dict[str, object]:
    # Coordinates are (U,g,v*g).  This is the exact sparse S-pair identity.
    unary = (Q(1), Q(0), Q(0))
    private = (Q(0), Q(1), Q(-1))
    target = add(unary, private)
    require(target == (Q(1), Q(1), Q(-1)), "B=U+(1-v)g changed")

    def specialize_v(vector: tuple[Q, ...], value: Q) -> tuple[Q, Q]:
        # Return coordinates (U,g) after v -> value.
        return vector[0], vector[1] + value * vector[2]

    at_v0 = {
        "U": specialize_v(unary, Q(0)),
        "R": specialize_v(private, Q(0)),
        "B": specialize_v(target, Q(0)),
    }
    at_v1 = {
        "U": specialize_v(unary, Q(1)),
        "R": specialize_v(private, Q(1)),
        "B": specialize_v(target, Q(1)),
    }
    require(at_v0 == {"U": (Q(1), Q(0)),
                      "R": (Q(0), Q(1)),
                      "B": (Q(1), Q(1))}
            and at_v1 == {"U": (Q(1), Q(0)),
                          "R": (Q(0), Q(0)),
                          "B": (Q(1), Q(0))},
            ("private-return specializations changed", at_v0, at_v1))

    # Bezout/comaximal certificate for the exhaustive pointwise cover by
    # q04 bright and q04 zero: v + (1-v) = 1.  V(1-v) is contained in D(v).
    require(add((Q(0), Q(1)), (Q(1), Q(-1))) == (Q(1), Q(0)),
            "v+(1-v)=1 changed")

    return {
        "coefficient_coordinates": ["U", "g", "v04*g"],
        "identity": "B_E14=U+(1-v04_00)g",
        "R_E14": "(1-v04_00)g",
        "g": "(p1_0_1*s1_1_1)u35_11*v24_11",
        "V_1_minus_v04": {
            "specialization": "v04_00=1",
            "R": 0,
            "B_equals_U": True,
            "contained_in_q04_bright_locus": True,
        },
        "D_1_minus_v04": {
            "return_membership_equivalent_to_g_membership": True,
            "split": [
                "D(1-v04) intersect D(v04): q04-bright response route",
                "D(1-v04) intersect V(v04): v04=0, R_E14=g",
            ],
        },
        "exhaustivity_certificate": "v04+(1-v04)=1",
    }


def pinned_physical_interfaces() -> dict[str, object]:
    positive = load(
        "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py",
        "private_return_positive",
    )
    positive_ledger, positive_digest = positive.audit()
    require(positive_digest == positive.EXPECTED_LEDGER_SHA256
            and positive_ledger["conditional_physical_assembly"]
            ["missing_occurrence_map"] == {
                "F=H0-u": "1-v04_00",
                "e_Eq": "(p1_0_1*s1_1_1)*u35_11*v24_11",
                "image": "R_E14",
                "source_labelled_map_constructed": False,
            }, "private-return source scope changed")

    response = load(
        "computations/verify_h3_four_base_silent_c6_response_lock.py",
        "private_return_response",
    )
    cycle = response.audit_augmented_cycle()
    rows = response.audit_literal_rows()
    require("O11--C21(q04)--O22" in cycle["crossed_paths"]
            and rows["G21_q04_chord"]["target"] == 0,
            ("q04 crossed response route changed", cycle, rows))

    minimal = load(
        "computations/verify_h3_c6_e14_minimal_enlargement_unit.py",
        "private_return_minimal_unit",
    )
    minimal_ledger, minimal_digest = minimal.audit()
    require(minimal_digest == minimal.EXPECTED_LEDGER_SHA256
            and len(minimal_ledger["records"]) == 9,
            "minimal E14 complete-row unit changed")

    one = load(
        "computations/verify_h3_c6_e14_pure11_unary_unit.py",
        "private_return_one_unit",
    )
    one_ledger, one_digest = one.audit()
    require(one_digest == one.EXPECTED_LEDGER_SHA256
            and one_ledger["complete_first_extra_internal_cell_count"] == 1020
            and one_ledger["complete_first_extra_internal_cell_units"] == 1020,
            "one-cell E14 unit layer changed")

    two = load(
        "computations/verify_h3_c6_e14_two_cell_unit_frontier.py",
        "private_return_two_unit",
    )
    two_ledger, two_digest = two.audit()
    require(two_digest == two.EXPECTED_LEDGER_SHA256
            and two_ledger["two_cell_extension_count"] == 57291
            and two_ledger["ordinary_source_unit_count"] == 57291,
            "two-cell E14 unit layer changed")

    return {
        "q04_bright": {
            "literal_complete_response_path": "O11--C21(q04)--O22",
            "target_on_crossed_row": 0,
            "unconditional_conclusion": (
                "typed crossed-response landing; not by itself a global "
                "terminal outside the pinned local E14 fibres"
            ),
        },
        "same_grade_complete_E14_unit_envelope": {
            "minimal_chart_count": 9,
            "one_new_internal_cell_units": 1020,
            "two_new_internal_cell_units": 57291,
            "hypotheses": (
                "canonical minimal E14 coefficient fibre, complete rows, "
                "core endpoints, identical word/fine/repeated grade, and "
                "at most two new internal cells"
            ),
        },
        "missing_from_coefficient_placement": [
            "source-labelled map rather than coefficient pushforward",
            "word/fine/repeated-grade agreement",
            "complete proper faces and endpoint support",
            "a proof that contamination stays in the zero/one/two-cell envelope",
        ],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    algebra = exact_spair_localization()
    physical = pinned_physical_interfaces()
    ledger = {
        "theorem": "E14 private-return localization and unit fork",
        "pins": PINS,
        "exact_localization": algebra,
        "physical_interfaces": physical,
        "fork": {
            "V_1_minus_v04": (
                "B_E14=U and q04 is nonzero; the target class is already "
                "old and the literal q04 crossed-response path is present"
            ),
            "D_1_minus_v04_and_D_v04": (
                "q04 is nonzero, so the same crossed-response path is present"
            ),
            "D_1_minus_v04_and_V_v04": (
                "v04=0 and R_E14=g; the exact missing datum is the primitive "
                "same-word/fine occurrence placement (H0-u)e_Eq -> g"
            ),
        },
        "ordering": (
            "word/fine/repeated-grade placement is logically prior to using "
            "the E14 unit theorem.  Once a complete physical placement in "
            "the pinned zero/one/two-cell envelope is proved, the complete "
            "response/unary/G22 collision gives an ordinary source unit.  "
            "A coefficient-only map to R_E14 does not meet those hypotheses."
        ),
        "shortest_remaining_theorem": (
            "on the silent fibre v04=0, construct the complete same-grade "
            "physical row with primitive occurrence boundary g and all forced "
            "proper faces; otherwise extend the first full-row nonlift to the "
            "typed crossed-response/terminal alternative"
        ),
        "scope": (
            "canonical chart-(1,1), word-000101 E14 S-pair.  The localization "
            "fork is exact over the coefficient ring.  Local unit promotion "
            "is conditional on the explicitly pinned E14 word/fine/support "
            "envelope and does not cover arbitrary multisite contamination."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("private-return localization ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("E14 private return D/V fork: PASS (exact)")
    print("V(1-v04): B=U, q04-bright crossed response")
    print("D(1-v04) & D(v04): q04-bright crossed response")
    print("D(1-v04) & V(v04): R=g, primitive same-grade placement OPEN")
    print("complete E14 unit: CONDITIONAL ON FULL WORD/FINE ROW")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
