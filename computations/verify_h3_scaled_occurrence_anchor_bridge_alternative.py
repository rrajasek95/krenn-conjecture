#!/usr/bin/env python3
"""Reduce the anchor bridge to one centered occurrence descent.

For N=90 occurrence graph coordinates z_M and global target u, the full
formal occurrence simplex plus B=sum z_M-u does not kill z_f-u.  It does
kill the unit-scaled bridge

    N z_f-u = (N z_f-sum z_M)+(sum z_M-u).

The first parenthesis is a saturated augmentation-zero star boundary.  In
characteristic zero this scaled identity is sufficient for anchor
visibility.  Its physical descent is not supplied by complete source bars:
those remain in the trivial occurrence representation.  Maximum-anchor /
minimum-support extremality also does not force it, as a torus-curve guard
shows.  Thus one centered occurrence descent-or-terminal clause is the
smallest exact addition to the master comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
N = 90
PINS = {
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "computations/verify_h3_reduced_eq_full_occurrence_simplex_symmetrization_gate.py":
        "5150fa94137a07062092b32328af63f4e188823d6ca06160a10e4b1c040786d3",
    "computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py":
        "403819751753802f4bb01b07cca2540fc6abf0479b9be5569ee74f414ea667ad",
    "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py":
        "f4139b38728165240d1b033852aba2189e8f1a721d90d2f997755be0a077e6d0",
}
EXPECTED_LEDGER_SHA256 = (
    "91b63b6f603bcf6fc98854d3ae4cbe00b21d9536028a98c6f265d935ad1e0afb"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def unit(index, size=N + 1):
    answer = [Q(0)] * size
    answer[index] = Q(1)
    return tuple(answer)


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(vectors):
    basis = {}
    for original in vectors:
        values = [Q(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [left - coefficient * right for left, right in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def formal_occurrence_target_quotient_audit():
    occurrences = tuple(unit(index) for index in range(N))
    u = unit(N)
    # Orient the star from every other occurrence toward the marked one.
    star = tuple(add(occurrences[0], scale(-1, occurrences[index]))
                 for index in range(1, N))
    ones = add(*occurrences)
    b_normal = add(ones, scale(-1, u))
    exact_bridge = add(occurrences[0], scale(-1, u))
    centered = add(scale(N, occurrences[0]), scale(-1, ones))
    scaled_bridge = add(scale(N, occurrences[0]), scale(-1, u))

    require(add(*star) == centered
            and add(centered, b_normal) == scaled_bridge,
            "the centered-star/normal decomposition changed")
    require(rank(star) == N - 1
            and rank(star + (b_normal,)) == N,
            "the formal occurrence/target quotient rank changed")

    # The one remaining primitive dual has common occurrence coefficient 1
    # and target coefficient N.  It kills every star edge and B, but reads
    # 1-N on the unscaled bridge.  Thus z_f-u is genuinely not a formal
    # boundary, while N*z_f-u is.
    primitive_dual = (Q(1),) * N + (Q(N),)
    require(all(dot(primitive_dual, edge) == 0 for edge in star)
            and dot(primitive_dual, b_normal) == 0
            and dot(primitive_dual, exact_bridge) == 1 - N
            and dot(primitive_dual, scaled_bridge) == 0,
            "the primitive scaling dual changed")
    require(rank(star + (b_normal, exact_bridge)) == N + 1
            and rank(star + (b_normal, scaled_bridge)) == N,
            "the exact/scaled bridge membership changed")

    # Equivalently the simplex identifies a marked occurrence with the
    # average target, not with the whole target.
    normalized = add(occurrences[0], scale(Q(-1, N), u))
    require(scale(N, normalized) == scaled_bridge,
            "the normalized marked/target law changed")
    return {
        "occurrences": N,
        "formal_star_rank": N - 1,
        "target_normal": "B=sum_M z_M-u",
        "centered_marked_boundary": "c_f=N*z_f-sum_M z_M",
        "scaled_bridge": "N*z_f-u=c_f+B",
        "unscaled_bridge_in_formal_image": False,
        "scaled_bridge_in_formal_image": True,
        "normalized_law": "[dz_f]=[du]/N",
        "primitive_unscaled_detector": {
            "occurrence_coefficients": "all 1",
            "target_coefficient": N,
            "value_on_d(z_f-u)": 1 - N,
        },
        "characteristic_requirement": f"{N} is a unit",
    }


def scaled_anchor_visibility_audit():
    # Small exact model: A kills xi, H sees it, and N*H-h*Phi lies in row A.
    # The central readout must then see Phi(xi).  Exact equality at scale one
    # is unnecessary for the landing.
    A = (Q(1), Q(0), Q(0))
    xi = (Q(0), Q(1), Q(0))
    H = (Q(0), Q(1), Q(0))
    h_phi = (Q(7), Q(N), Q(0))
    difference = add(scale(N, H), scale(-1, h_phi))
    require(difference == scale(-7, A)
            and dot(A, xi) == 0 and dot(H, xi) == 1
            and dot(h_phi, xi) == N,
            "the scaled anchor-visibility identity changed")
    return {
        "sufficient_row_law": "N*H-h_Eq*Phi in row(A)",
        "kernel_evaluation": "h_Eq(Phi xi)=N*H(xi)",
        "noncollapse_if_H_visible": True,
        "exact_scale_one_law_needed": False,
    }


def physical_descent_scope_audit():
    splitter = (ROOT / (
        "computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py"
    )).read_text()
    euler = (ROOT / (
        "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py"
    )).read_text()
    require("complete physical source row is the orbit sum" in splitter
            and "remain in the trivial matching representation" in splitter
            and '"formal_occurrence_bar_rank"' in splitter,
            "the physical/formal occurrence-bar distinction changed")
    require("all 90 terms" in euler
            and '"first_source_validity_defect": "f(x), normalized here to 1"'
            in euler
            and '"conclusion": "Euler returns 3R, not the marked polar df"'
            in euler,
            "the pinned Euler/source-validity obstruction changed")
    return {
        "formal_occurrence_simplex": "spans c_f integrally",
        "committed_complete_physical_bars": (
            "remain in the trivial occurrence/matching representation"
        ),
        "raw_marked_Euler_projector": (
            "has nonzero scalar zero-face f(x), so is not source-valid"
        ),
        "target_compatible_Euler": "returns aggregate 3R, not df",
        "centered_bar_physically_constructed": False,
    }


def extremal_selection_counterguard_audit():
    # The smooth torus curve xy=1 has constant support and one active marked
    # function f=x, yet df is nonzero on its tangent at (1,1).  Thus maximum
    # active-anchor count followed by minimum scalar support does not force
    # infinitesimal occurrence rigidity or a support deletion.
    point = (Q(1), Q(1))
    d_source = (Q(1), Q(1))  # d(xy-1) at (1,1)
    tangent = (Q(1), Q(-1))
    d_f = (Q(1), Q(0))
    require(dot(d_source, tangent) == 0 and dot(d_f, tangent) == 1,
            "the extremal torus tangent guard changed")
    samples = ((Q(1), Q(1)), (Q(2), Q(1, 2)), (Q(1, 2), Q(2)))
    require(all(x * y == 1 and x and y for x, y in samples),
            "the constant-support torus samples changed")
    return {
        "source_curve": "x*y=1",
        "marked_anchor_function": "f=x",
        "base_point": tuple(map(str, point)),
        "tangent": tuple(map(str, tangent)),
        "df_on_tangent": "1",
        "occupied_scalar_support_along_curve": 2,
        "active_marked_anchor_count_along_curve": 1,
        "support_deletion_forced": False,
        "scope": (
            "an exact extremal-selection logic guard, not a complete Krenn source"
        ),
    }


def rank_one_comparison_alternative_audit():
    # Once the formal star and B have been promoted into a complete physical
    # augmented comparison cone, only one candidate c_f remains to test.
    # Freeze the elementary membership/cokernel alternative on sample maps.
    cases = []
    for columns, candidate in (
        (((Q(1), Q(0)),), (Q(2), Q(0))),
        (((Q(1), Q(0)),), (Q(0), Q(1))),
        (((Q(1), Q(1)),), (Q(1), Q(-1))),
    ):
        old = rank(columns)
        new = rank(columns + (candidate,))
        if old == new:
            cases.append("physical_boundary")
            continue
        # In dimension two, solve an explicit left-null detector.
        column = columns[0]
        dual = (column[1], -column[0])
        require(dot(dual, column) == 0 and dot(dual, candidate),
                "the comparison-cokernel detector changed")
        cases.append("cokernel_dual")
    require(cases == ["physical_boundary", "cokernel_dual", "cokernel_dual"],
            "the rank-one comparison alternatives changed")
    return {
        "candidate": "centered occurrence class c_f=N*du_f-sum_M du_M",
        "after_target_normalization": "gamma_f=N*du_f-du",
        "exact_linear_alternative": (
            "gamma_f is a complete physical comparison boundary, or a "
            "complete augmented cokernel covector detects it"
        ),
        "terminal_typing_warning": (
            "the detecting covector is terminal only if the comparison cone "
            "retains the literal q/ainc/target/word/fine/repeated/eta/sigma rows"
        ),
        "sample_outcomes": cases,
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "scaled occurrence-anchor bridge reduction",
        "pins": PINS,
        "formal_all_occurrence_identity": formal_occurrence_target_quotient_audit(),
        "scaled_visibility": scaled_anchor_visibility_audit(),
        "physical_descent_scope": physical_descent_scope_audit(),
        "maximum_anchor_minimum_support_guard": extremal_selection_counterguard_audit(),
        "rank_one_comparison_alternative": rank_one_comparison_alternative_audit(),
        "shortest_master_clause": (
            "Promote the centered star class c_f=N*du_f-sum_M du_M to the "
            "complete augmented physical comparison cone.  Either it is a "
            "physical boundary, and B=sum_M du_M-du gives N[H]=Phi^*[h_Eq] "
            "mod row(A), or its first nonzero augmented cokernel dual is a "
            "typed existing exchange/relative-generator/Fredholm terminal"
        ),
        "frontier": (
            "all-occurrence algebra reduces the anchor lane to one rank-one "
            "centered descent.  It does not prove the unscaled bridge, and "
            "neither complete physical bars, Euler homogeneity, nor extremal "
            "selection currently supplies the centered descent"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("scaled occurrence-anchor ledger changed", digest))
    return ledger, digest


def main():
    _, digest = audit()
    print("h3 scaled occurrence-anchor bridge: PASS")
    print("formal all-occurrence law: 90[du_f]=[du]")
    print("exact unscaled law [du_f]=[du]: FALSE in formal quotient")
    print("scaled law is sufficient for anchor visibility")
    print("physical centered occurrence descent or typed dual: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
