#!/usr/bin/env python3
"""Audit when a P_f-dark kernel really lowers occupied scalar support.

The source coefficients are matching-multiaffine.  Consequently a tangent
xi integrates along the literal affine line x+t*xi precisely when every
higher matching/Hasse coefficient on that line vanishes.  This is automatic
when the varied scalar cells are pairwise occurrence-incompatible (for
example q-cells in one site star, or cells in one endpoint row).  If xi is
also supported on already occupied non-anchor cells, choosing t to kill a
marked coordinate is an exact minimum-support contradiction.

P_f-darkness alone gives none of the two extra clauses.  A literal six-site
target/response packet exhibits the first nonlinear alternative.  Its
redistribution tangent preserves both rows to first order and is visible to
the marked occurrence, but the affine line has a pure-target quadratic
residual.  The tangent integrates only through the torus family

    q01=q23=a, q45=a^-2,

which never reaches a=0.  This is exactly pure-target coloop saturation, not
an offdiagonal fan/four-good carrier.  Thus the remaining positive theorem
must confine the full-source kernel to an occupied occurrence-incompatible
support, or route its first nonzero Hasse face with its actual labels.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_affine_pointed_pf_coloop_pivot_gate.py":
        "c5fdf06fb372ec748d2b98398f2968246e2c839dba9282cec29f675a5ca8684e",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py":
        "f4139b38728165240d1b033852aba2189e8f1a721d90d2f997755be0a077e6d0",
    "computations/verify_h3_active_fan_coloop_direct_normalization_axis_pure_no_shortcut.py":
        "4e6c486db07d623bc897f13a98d36a45377c34773311efe94afa55551a6a97b7",
    "computations/verify_h3_trapped_carrier_actual_endpoint_map_boundary.py":
        "1735de099eeaec04a2197c613350fba4bd52d8955873c8a032894d8653087a0a",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
}
EXPECTED_LEDGER_SHA256 = (
    "66e4cc6dfec20bcbc9b4a12496fd6e829cba4e655288b8e6c87835789f6f11ee"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append((tuple(sorted((first, second))),) + tail)
    return tuple(answer)


def multiply_polynomials(left, right):
    answer = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return answer


def line_coefficients(monomials, point, direction):
    """Expand sum coefficient*product(variable) on point+t*direction."""
    degree = max((len(variables) for _coefficient, variables in monomials),
                 default=0)
    answer = [Q(0)] * (degree + 1)
    for coefficient, variables in monomials:
        term = [Q(coefficient)]
        for variable in variables:
            term = multiply_polynomials(
                term, [Q(point[variable]), Q(direction.get(variable, 0))])
        for power, value in enumerate(term):
            answer[power] += value
    while len(answer) > 1 and answer[-1] == 0:
        answer.pop()
    return tuple(answer)


def matching_affine_line_criterion():
    matchings = perfect_matchings(range(6))
    require(len(matchings) == 15, "K6 matching count changed")
    star = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)}
    maximum_star_use = max(len(set(matching) & star)
                           for matching in matchings)
    require(maximum_star_use == 1,
            "a perfect matching used two cells in one site star")

    # A representative complete matching polynomial restricted to three
    # directions in one star has degree at most one on every affine line.
    point = {f"q{u}{v}": Q(1)
             for u in range(6) for v in range(u + 1, 6)}
    direction = {"q01": Q(2), "q02": Q(-3), "q03": Q(5)}
    monomials = [(Q(1), tuple(f"q{u}{v}" for u, v in matching))
                 for matching in matchings]
    expansion = line_coefficients(monomials, point, direction)
    require(len(expansion) <= 2, expansion)

    return {
        "K6_perfect_matchings": len(matchings),
        "maximum_cells_from_one_site_star_per_occurrence": maximum_star_use,
        "representative_full_matching_line_degree": len(expansion) - 1,
        "endpoint_analogue": (
            "each response occurrence uses exactly one component of a fixed "
            "p_i row and exactly one component of a fixed s_j row"
        ),
        "exact_affine_line_lemma": (
            "if xi is a full-source Jacobian kernel and every physical "
            "source monomial contains at most one scalar cell from supp(xi), "
            "then F(x+t*xi)=F(x) identically"
        ),
        "minimum_support_clause": (
            "if supp(xi) is contained in the occupied non-anchor support and "
            "xi_e is nonzero at the marked occupied cell e, t=-x_e/xi_e "
            "deletes e without activating a new cell"
        ),
    }


def literal_target_response_coloop_packet():
    # Residual sites are 0,...,5.  These are literal matching occurrences:
    # T=q01*q23*q45 and
    # R=p0*s1*q23*q45 + p2*s3*q01*q45.
    # At the displayed point T=1 and R=0.
    target = [(Q(1), ("q01", "q23", "q45"))]
    first = [(Q(1), ("p0", "s1", "q23", "q45"))]
    second = [(Q(1), ("p2", "s3", "q01", "q45"))]
    response = first + second
    point = {
        "q01": Q(1), "q23": Q(1), "q45": Q(1),
        "p0": Q(1), "s1": Q(1), "p2": Q(1), "s3": Q(-1),
    }
    direction = {"q01": Q(1), "q23": Q(1), "q45": Q(-2)}
    target_line = line_coefficients(target, point, direction)
    response_line = line_coefficients(response, point, direction)
    first_line = line_coefficients(first, point, direction)
    second_line = line_coefficients(second, point, direction)
    require(target_line == (Q(1), Q(0), Q(-3), Q(-2)), target_line)
    require(response_line == (Q(0),), response_line)
    require(first_line == (Q(1), Q(-1), Q(-2)), first_line)
    require(second_line == (Q(-1), Q(1), Q(2)), second_line)

    # Exact torus integration: q01=q23=a and q45=a^-2.  Record Laurent
    # exponents and coefficients instead of introducing a CAS.
    target_laurent = (Q(1), 1 + 1 - 2)
    first_laurent = (Q(1), 1 - 2)
    second_laurent = (Q(-1), 1 - 2)
    require(target_laurent == (Q(1), 0)
            and first_laurent[0] + second_laurent[0] == 0
            and first_laurent[1] == second_laurent[1] == -1,
            (target_laurent, first_laurent, second_laurent))

    return {
        "literal_pure_target_occurrence": "q01^00*q23^00*q45^00=1",
        "literal_zero_response": (
            "p_i[0,0]s_j[1,0]q23^00q45^00 + "
            "p_i[2,0]s_j[3,0]q01^00q45^00 = 1-1=0"
        ),
        "affine_tangent": {
            "dq01": 1, "dq23": 1, "dq45": -2,
            "d_target": int(target_line[1]),
            "d_response": 0,
            "d_marked_first_occurrence": int(first_line[1]),
        },
        "affine_line_target_coefficients": [str(value)
                                             for value in target_line],
        "first_nonlinear_face": "-3*t^2 in the pure-000000 target row",
        "response_on_affine_line": "identically zero",
        "exact_integrating_family": (
            "q01=q23=a, q45=a^-2; target=1 and response=0 on D(a)"
        ),
        "why_no_support_deletion": (
            "q01*q23*q45=1 makes all three cells units; a=0 is absent from "
            "the affine source chart"
        ),
        "landing": (
            "pure-target coloop saturation; the first side effect has no "
            "offdiagonal fan cell and is not a four-good carrier"
        ),
        "scope": (
            "a literal complete target/response word block and exact torus "
            "family, not a standalone full nine-row GHZ source"
        ),
    }


def support_and_side_effect_frontier():
    # If a direction activates z previously zero while deleting occupied x,
    # the generic support count stays unchanged: this is why confinement to
    # occupied columns is logically independent of Jacobian darkness.
    occupied_before = {"x", "y"}
    direction_support = {"x", "z"}
    killed = "x"
    generic_after = (occupied_before - {killed}) | (
        direction_support - occupied_before)
    require(len(generic_after) == len(occupied_before), generic_after)
    return {
        "support_confinement_guard": {
            "occupied_before": sorted(occupied_before),
            "direction_support": sorted(direction_support),
            "generic_after_killing_x": sorted(generic_after),
            "support_before_after": [2, 2],
        },
        "first_Hasse_face_formula": (
            "H_r(xi) is the sum over r pairwise co-occurring varied scalar "
            "cells, multiplied by their literal complementary matching "
            "cofactors; h=3 target and fixed-right responses need r<=3"
        ),
        "conditional_existing_routes": [
            "an activated offdiagonal cell with a nonzero private-site cofactor enters the active-fan route",
            "an outside endpoint hole with its complete common tail enters finite Hall/four-good saturation",
            "a unique normalized pure-target matching face is coloop saturation",
        ],
        "not_automatic": (
            "P_f-darkness specifies only a Jacobian kernel.  It does not "
            "confine that kernel to occupied cells, kill its H_2/H_3 faces, "
            "or force a nonlinear face to be offdiagonal rather than pure"
        ),
        "smallest_remaining_incidence": (
            "for every P_f-visible full-source kernel, find an occupied, "
            "anchor-safe occurrence-incompatible representative, or show "
            "that its first nonzero labelled Hasse face has a nonzero "
            "private-site/outside-hole/coloop landing"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": (
            "h3 P_f-dark full-source kernel support-lowering criterion and "
            "pure-target coloop Hasse counterguard"
        ),
        "pins": PINS,
        "matching_affine_line": matching_affine_line_criterion(),
        "literal_nonlinear_packet": literal_target_response_coloop_packet(),
        "support_and_side_effect_frontier": support_and_side_effect_frontier(),
        "verdict": (
            "A P_f-visible full-source kernel contradicts minimum occupied "
            "scalar support only after two extra source statements: its "
            "direction is confined to occupied non-anchor cells and all "
            "higher matching/Hasse faces vanish.  Pairwise occurrence-"
            "incompatible support makes the second clause automatic and the "
            "affine line deletes the marked cell exactly.  Without it, a "
            "literal two-occurrence response redistribution can have a pure-"
            "target quadratic face and integrate only on a torus; normalized "
            "target then gives coloop saturation, not support deletion or an "
            "offdiagonal active-fan/four-good carrier."
        ),
        "scope": (
            "exact matching-multiaffine lemma plus a literal six-site target/"
            "response block; this is not a full GHZ counterexample and does "
            "not assert that every nonlinear side effect is a coloop"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("occupied occurrence-incompatible kernel: EXACT AFFINE DELETION")
    print("bare P_f-dark kernel -> support lowering: NOT IMPLIED")
    print("literal nonlinear redistribution: PURE-TARGET COLOOP SATURATION")
    print("automatic offdiagonal fan/four-good landing: FALSE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
