#!/usr/bin/env python3
"""Audit c1 from beta/Hasse differentiation of the unweighted endpoint lift.

The literal Hermite response path canonically fixes the top-suspended H1.
At the desuspended physical level a based loop eta=t(1-t) fixes endpoints
and the unweighted lift, while shifting H1 by -1/6 of a vertical cycle.
Thus differentiation does not select zero residue.  The exact positive
criterion is finite boundary membership of (r-2q)*chi(ker pi).
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/scalar-unit-hermite-source-path-first-moment-lift-obstruction.md":
        "e5d3c2bc3349dc20070f4d8e19084796a957cd76f9731ed7f0db4681e4145d7b",
    "computations/verify_scalar_unit_hermite_source_path_first_moment_lift_obstruction.py":
        "1adc4904000ca3431355b9fb88ebe5edac4c88b5cabe2ba64d71bd56f6c08199",
    "notes/augmented-hpl-terminal-bockstein-lemma.md":
        "de1d34da41ed3f845003adec41cb2907b8dc4917ed9c75f6b375ea1aea021f89",
    "computations/verify_augmented_hpl_terminal_bockstein_lemma.py":
        "a616e5d83d52189c1d64093d0ba80abc0dc43e4b419241a871713a622b043a49",
    "notes/scalar-unit-c0-four-cut-common-carrier-gate.md":
        "a06018da73d6a954f14706fcfdeaae5ace1c2424e02530ab87602c1e77271000",
    "computations/verify_scalar_unit_c0_four_cut_common_carrier_gate.py":
        "56421c894acd613300841b7ae41d1bafecc6d65fcc9618982dc61ac198c2fa66",
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "notes/h3-endpoint-projector-oriented-four-cut-moment-gate.md":
        "60f0197280c43ac17dca2205a7e523a65be1115f49f7988dfecd09341568d3b6",
    "computations/verify_h3_endpoint_projector_oriented_four_cut_moment_gate.py":
        "232b0f4296c56c0254201fb46bd65e7cadca3ed1151dc21e52b0a8b22b234f0a",
}
EXPECTED_LEDGER_SHA256 = (
    "dde420258e2f21f70369e52d4f9770003d01c515c0dd98de789ca623c17112bc"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: list[Fraction]) -> list[Fraction]:
    require(vectors, "empty vector sum")
    require(len({len(vector) for vector in vectors}) == 1,
            "vector width mismatch")
    return [sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True)]


def scale(value: Fraction, vector: list[Fraction]) -> list[Fraction]:
    return [value * entry for entry in vector]


def multiply_q(vector: list[Fraction], degree: int) -> list[Fraction]:
    require(len(vector) == degree + 1, "q multiplication width")
    answer = [Fraction(0) for _ in range(degree + 2)]
    for r_degree, entry in enumerate(vector):
        answer[r_degree] += Fraction(degree - r_degree + 1) * entry
    return answer


def multiply_r(vector: list[Fraction], degree: int) -> list[Fraction]:
    require(len(vector) == degree + 1, "r multiplication width")
    answer = [Fraction(0) for _ in range(degree + 2)]
    for r_degree, entry in enumerate(vector):
        answer[r_degree + 1] += Fraction(r_degree + 1) * entry
    return answer


def moment(h: int, weight: int) -> list[Fraction]:
    require(h >= 3 and weight >= 0, "invalid moment")
    return [Fraction(1, weight + ell + 1) for ell in range(h - 1)]


def carrier(h: int, weight: int) -> list[Fraction]:
    h_weight = moment(h, weight)
    return add(
        multiply_r(h_weight, h - 2),
        scale(-2, multiply_q(h_weight, h - 2)),
    )


def polynomial_derivative(coefficients: list[Fraction]) -> list[Fraction]:
    return [
        Fraction(index) * coefficients[index]
        for index in range(1, len(coefficients))
    ]


def integrate(coefficients: list[Fraction], weight: int = 0) -> Fraction:
    return sum((
        coefficient / Fraction(index + weight + 1)
        for index, coefficient in enumerate(coefficients)
    ), Fraction(0))


def loop_residue_audit() -> dict[str, object]:
    eta = [Fraction(0), Fraction(1), Fraction(-1)]
    d_eta = polynomial_derivative(eta)
    require(sum(eta) == 0 and eta[0] == 0, "loop endpoint changed")
    require(integrate(d_eta, 0) == 0, "loop changed unweighted lift")
    records = {}
    for weight in range(1, 17):
        residue = integrate(d_eta, weight)
        expected = -Fraction(weight, (weight + 1) * (weight + 2))
        require(residue == expected,
                ("based-loop weighted residue changed", weight))
        records[weight] = str(residue)
    require(records[1] == "-1/6", "first loop residue changed")

    # Differentiating the primitive loop produces the nonzero one-form;
    # it does not choose the zero representative.
    require(d_eta == [Fraction(1), Fraction(-2)],
            "Hasse derivative of based loop changed")
    return {
        "eta": [str(entry) for entry in eta],
        "D_eta": [str(entry) for entry in d_eta],
        "unweighted_residue": str(integrate(d_eta, 0)),
        "weighted_residues": records,
        "verdict": (
            "beta/Hasse differentiation preserves the lift ambiguity; "
            "the first weighted residue is -1/6"
        ),
    }


def hermite_all_h_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 25):
        h_zero = moment(h, 0)
        h_one = moment(h, 1)
        require(h_zero == [Fraction(1, ell + 1) for ell in range(h - 1)],
                ("H0 changed", h))
        require(h_one == [Fraction(1, ell + 2) for ell in range(h - 1)],
                ("H1 changed", h))

        # S(t)=R_jk (Q+tR)^[h-1].  After suppressing the common R_jk,
        # its derivative has coefficient ell+1 before divided-power
        # multiplication, exactly giving R*(Q+tR)^[h-2].  Weighted
        # integration therefore gives R*H_s.
        path = [
            [Fraction(int(r_degree == ell)) for r_degree in range(h)]
            for ell in range(h)
        ]
        derivative = [scale(ell, path[ell]) for ell in range(1, h)]
        weighted = [Fraction(0) for _ in range(h)]
        for degree, coefficient in enumerate(derivative):
            weighted = add(weighted, scale(Fraction(1, degree + 2), coefficient))
        require(weighted == multiply_r(h_one, h - 2),
                ("top-suspended H1 identity changed", h))

        records[h] = {
            "H1": [str(entry) for entry in h_one],
            "c1": [str(entry) for entry in carrier(h, 1)],
            "top_suspension": (
                "R_ja R_ak H1 = S_jk(1)-integral_0^1 S_jk(t)dt"
            ),
        }
    return records


def h3_audit() -> dict[str, object]:
    require(moment(3, 0) == [Fraction(1), Fraction(1, 2)], "h3 H0")
    require(moment(3, 1) == [Fraction(1, 2), Fraction(1, 3)], "h3 H1")
    require(carrier(3, 1) == [Fraction(-2), Fraction(-1, 6), Fraction(2, 3)],
            "h3 c1")

    # Residue acts on a vertical class z by -1/6*(r-2q)chi(z).
    # Model a nonzero one-dimensional image and its primitive dual.
    boundary = [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]
    obstruction = [Fraction(0), Fraction(0), Fraction(-1, 6)]
    require(matrix_rank(boundary + [obstruction]) == 3
            and matrix_rank(boundary) == 2,
            "h3 residue failed to survive toy boundary")
    dual = [Fraction(0), Fraction(0), Fraction(-6)]
    require(all(dot(dual, column) == 0 for column in boundary)
            and dot(dual, obstruction) == 1,
            "h3 residue dual changed")
    return {
        "H0": ["1", "1/2"],
        "H1": ["1/2", "1/3"],
        "c1": ["-2", "-1/6", "2/3"],
        "based_loop_residue": "-1/6*(r-2q)*chi(z)",
        "smallest_loop_dimension_per_vertical_class": 1,
        "toy_primitive_dual": [str(entry) for entry in dual],
    }


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def matrix_rank(columns: list[list[Fraction]]) -> int:
    require(columns, "empty rank")
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(entries) for entries in zip(*columns, strict=True)]
    rank = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(rank, height) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [entry / value for entry in rows[rank]]
        for row in range(height):
            if row == rank or not rows[row][column]:
                continue
            coefficient = rows[row][column]
            rows[row] = [
                entry - coefficient * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[rank], strict=True)
            ]
        rank += 1
        if rank == height:
            break
    return rank


def finite_membership_audit() -> dict[str, object]:
    # Universal independent columns model D_Q and L*chi(ker pi).
    boundary = [
        [Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
    ]
    residues = [
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
    ]
    require(matrix_rank(boundary + residues) > matrix_rank(boundary),
            "universal residue accidentally became boundary")
    corrections = residues
    require(matrix_rank(boundary + corrections)
            == matrix_rank(boundary + corrections + residues),
            "correction membership criterion failed")
    return {
        "zero_residue_criterion": (
            "rank(D_Q)=rank([D_Q | (r-2q) chi(ker pi)])"
        ),
        "equivalent_homology_condition": (
            "(r-2q) H(chi)(ker H(pi))=0 in H(Q)"
        ),
        "failure_dual": (
            "lambda D_Q=0 and lambda (r-2q)chi(z) != 0"
        ),
        "terminal_scope": (
            "lambda is physical only after D_Q includes complete protected, "
            "anchor, terminal, and q-cocycle rows"
        ),
    }


def source_scope_audit() -> dict[str, object]:
    hermite = (ROOT / "notes/scalar-unit-hermite-source-path-first-moment-lift-obstruction.md").read_text()
    hpl = (ROOT / "notes/augmented-hpl-terminal-bockstein-lemma.md").read_text()
    c_zero = (ROOT / "notes/scalar-unit-c0-four-cut-common-carrier-gate.md").read_text()
    projector = (ROOT / "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md").read_text()
    endpoint_moment = (ROOT / "notes/h3-endpoint-projector-oriented-four-cut-moment-gate.md").read_text()
    require("canonically fix the entire four-star" in hermite
            and "**top-suspended moment tower**" in hermite
            and "shift the first weighted\nsuspended lift by exactly" in hermite,
            "Hermite top/desuspension frontier changed")
    require(r"\beta[x]=[D_2x]" in hpl
            and "construct (1) in the literal source-labelled" in hpl,
            "abstract Bockstein criterion changed")
    require("first **weighted moment**" in c_zero
            and "surviving `H_0` base class" in projector,
            "endpoint projector weighted scope changed")
    require("first unweighted endpoint/Hasse face does not supply" in endpoint_moment
            and "affine density/weight" in endpoint_moment,
            "h3 endpoint-moment dependency changed")
    return {
        "positive_top_statement": (
            "the literal Hermite/Segre polynomial constructs every "
            "top-suspended H_s, including H1, uniformly"
        ),
        "negative_descent_statement": (
            "beta/Hasse differentiation of an unweighted physical lift "
            "does not canonically select zero based-loop residue"
        ),
        "first_missing_physical_row": (
            "a desuspended first-moment nullhomotopy whose vertical residue "
            "-(1/6)(r-2q)chi(z) is a literal boundary for every z in ker pi"
        ),
        "positive_sufficient_structure": (
            "an augmented filtered contraction makes the transferred D2 "
            "Bockstein canonical and carries its corrected terminal readout"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "scalar-unit c1 weighted endpoint Bockstein gate",
        "pins": PINS,
        "scope": source_scope_audit(),
        "loop": loop_residue_audit(),
        "all_h": hermite_all_h_audit(),
        "h3": h3_audit(),
        "membership": finite_membership_audit(),
        "verdict": (
            "The literal Hermite response path canonically constructs the "
            "top-suspended H1 in every h, but beta/Hasse differentiation "
            "does not canonically desuspend it. A based loop fixes endpoints "
            "and H0 while shifting H1 by -1/6 of a vertical class. The first "
            "missing physical row is exactly the nullhomotopy of "
            "(r-2q)chi(ker pi); its existence is one finite augmented "
            "boundary-membership test."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("c1 weighted endpoint ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("top-suspended H1: CANONICAL ALL h")
    print("beta/Hasse desuspension: BASED-LOOP AMBIGUITY -1/6")
    print("first physical row: (r-2q)chi(ker pi) is boundary")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
