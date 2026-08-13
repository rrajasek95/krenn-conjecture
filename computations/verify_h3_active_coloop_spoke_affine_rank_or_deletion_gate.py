#!/usr/bin/env python3
"""Prove the active-coloop spoke rank-or-exact-deletion dichotomy.

Fix the coloop edge 01 and write the residual cofactor as

    C=x1*y1+x2*y2+x3*y3,

with x=(q23,q24,q25) and y=(q45,q35,q34).  No perfect matching
occurrence contains two x_i.  Therefore the complete GHZ source map,
including any protected matching/occurrence readouts, is affine-linear in x
when all other cells are fixed.

Let M be the evaluated restriction matrix on the occupied x columns and let
y be the normalized target row.  For three occupied tails, either

    rank(M/<y>)=2,

so two source rows plus the target span all three tail selectors, or M has a
nonzero kernel direction.  The latter integrates on an exact affine source
line and kills an occupied x_i without activating any new coordinate.  At
minimum occupied support it is impossible, so the rank-two alternative is
forced.

This is not yet entry to the special processor of 93cf9ae: row-span
selectors may combine different output words/heads and need not make any of
its three named target-zero response rows occurrence-private.  A finite
rank-three counterguard freezes this typing gap.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_three_tail_localization_partition_guard.py":
        "8fc6a7f112d9614beba202072f76a3e97c7f5c67177862d1ee552fb0d6381d09",
    "notes/h3-active-coloop-three-tail-localization-partition-guard.md":
        "5e8d56b79c0d1f6bdfc3919363f5ad533f1df7affec41db71f6a708b7c2dd8f3",
    "computations/verify_h3_active_coloop_literal_packet_termination_scope.py":
        "ad369a692aa2a7bde3b30a0a4cba5e401b6e61afc62dd752a4f51781a9e6485e",
    "notes/h3-active-coloop-literal-packet-termination-scope.md":
        "1201ea94d8faafefefeaff81a47987e41a817c4775fc98057294ed80fdfe51c5",
    "computations/verify_h3_pf_dark_kernel_support_lowering_hasse_coloop_gate.py":
        "5feb07c35c4e5ce304a305f0146441de7af5a9dc2d5466a794d315d99b626e48",
    "notes/h3-pf-dark-kernel-support-lowering-hasse-coloop-gate.md":
        "bff81dd6a7d920db178418d9509dd1dd47f426a35d48a156be9941344683659c",
    "computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py":
        "fe60edcc44c33e660b50f7e8d627b506c5bd81c1d97f15e66b9e8a35e9f3c4ad",
    "notes/h3-active-coloop-closed-shore-complete-row-response-gate.md":
        "1470ffc55dff20f0919b4be884ca8d54efe7a15e90117d1610aef067c82b44b2",
}
EXPECTED_LEDGER_SHA256 = (
    "b7c82bc00b27218730dd26ee5de77b9398b1b5de74bb81cda3f7baad8c646569"
)
SITES = tuple(range(6))
X_EDGES = frozenset(((2, 3), (2, 4), (2, 5)))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def rank(rows) -> int:
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    width = len(work[0])
    require(all(len(row) == width for row in work), "ragged matrix")
    pivot = 0
    for column in range(width):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        value = work[pivot][column]
        work[pivot] = [entry / value for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right
                         in zip(work[row], work[pivot], strict=True)]
        pivot += 1
    return pivot


def null_vector(rows):
    work = [list(map(Q, row)) for row in rows]
    width = len(work[0])
    pivot_columns = []
    pivot = 0
    for column in range(width):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        value = work[pivot][column]
        work[pivot] = [entry / value for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right
                         in zip(work[row], work[pivot], strict=True)]
        pivot_columns.append(column)
        pivot += 1
    free = next((column for column in range(width)
                 if column not in pivot_columns), None)
    if free is None:
        return None
    vector = [Q(0)] * width
    vector[free] = 1
    for row, column in reversed(tuple(enumerate(pivot_columns))):
        vector[column] = -sum(work[row][index] * vector[index]
                              for index in range(column + 1, width))
    require(any(vector)
            and all(sum(left * right for left, right
                        in zip(row, vector, strict=True)) == 0
                    for row in rows),
            (rows, vector))
    return tuple(vector)


def matching_affinity_audit() -> dict[str, object]:
    target_matchings = tuple(perfect_matchings(SITES))
    require(len(target_matchings) == 15, len(target_matchings))
    target_histogram = {
        used: sum(sum(edge_value in X_EDGES for edge_value in matching) == used
                  for matching in target_matchings)
        for used in (0, 1)
    }
    require(target_histogram == {0: 6, 1: 9}, target_histogram)

    # A response occurrence chooses ordered endpoints p,s and a perfect
    # matching of the four residual sites.  If site 2 is exposed, it contains
    # no x edge; otherwise the residual perfect matching contains at most one.
    response = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            residual = tuple(site for site in SITES
                             if site not in (p_site, s_site))
            for matching in perfect_matchings(residual):
                response.append((p_site, s_site, matching))
    require(len(response) == 90, len(response))
    response_histogram = {
        used: sum(sum(edge_value in X_EDGES for edge_value in matching) == used
                  for _p, _s, matching in response)
        for used in (0, 1)
    }
    require(response_histogram == {0: 54, 1: 36}, response_histogram)
    require(all(sum(edge_value in X_EDGES for edge_value in matching) <= 1
                for matching in target_matchings)
            and all(sum(edge_value in X_EDGES for edge_value in matching) <= 1
                    for _p, _s, matching in response),
            "a complete occurrence used two selected spokes")
    return {
        "selected_spokes": [repr(value) for value in sorted(X_EDGES)],
        "target_occurrences": len(target_matchings),
        "target_spoke_use_histogram": target_histogram,
        "response_occurrences_per_head_word": len(response),
        "response_spoke_use_histogram": response_histogram,
        "maximum_selected_spokes_per_complete_occurrence": 1,
        "exact_consequence": (
            "after fixing every other decorated scalar cell, every complete "
            "target/response coefficient and every matching-derived protected "
            "readout is b_r+sum_i M_ri*x_i"
        ),
    }


def rank_or_deletion_audit() -> dict[str, object]:
    values = (Q(-1), Q(0), Q(1))
    tested = 0
    full = 0
    deficient = 0
    for target in itertools.product((Q(-1), Q(1)), repeat=3):
        for first in itertools.product(values, repeat=3):
            for second in itertools.product(values, repeat=3):
                matrix = (target, first, second)
                matrix_rank = rank(matrix)
                quotient_rank = matrix_rank - 1
                require(quotient_rank in (0, 1, 2), matrix)
                kernel = null_vector(matrix)
                require((quotient_rank == 2) == (kernel is None),
                        (matrix, quotient_rank, kernel))
                full += int(quotient_rank == 2)
                deficient += int(quotient_rank < 2)
                tested += 1
    require(tested == 8 * 27 * 27 and full and deficient,
            (tested, full, deficient))

    # Exact affine deletion on one deficient example.  Constants are chosen
    # so x=(1,2,3) lies in the fibre.  The kernel direction kills x1 while
    # every row remains constant for all t.
    point = (Q(1), Q(2), Q(3))
    matrix = (
        (Q(1), Q(1), Q(1)),
        (Q(1), Q(1), Q(1)),
        (Q(1), Q(-1), Q(0)),
    )
    direction = null_vector(matrix)
    require(direction is not None, matrix)
    selected = next(index for index, value in enumerate(direction) if value)
    parameter = -point[selected] / direction[selected]
    endpoint = tuple(left + parameter * right for left, right
                     in zip(point, direction, strict=True))
    constants = tuple(-sum(left * right for left, right
                           in zip(row, point, strict=True)) for row in matrix)
    for test_parameter in (Q(-3), Q(0), Q(2), parameter):
        moved = tuple(left + test_parameter * right for left, right
                      in zip(point, direction, strict=True))
        require(all(constant + sum(left * right for left, right
                                   in zip(row, moved, strict=True)) == 0
                    for constant, row in zip(constants, matrix, strict=True)),
                (test_parameter, moved))
    require(endpoint[selected] == 0
            and sum(value != 0 for value in endpoint)
                < sum(value != 0 for value in point),
            (direction, parameter, endpoint))

    return {
        "finite_rank_checks": tested,
        "rank_two_mod_target_cases": full,
        "kernel_cases": deficient,
        "general_linear_algebra": (
            "for k occupied spokes, rank(M)=1+rank(M/<target>); if the "
            "quotient rank is below k-1, rank-nullity gives nonzero ker(M)"
        ),
        "affine_integration": (
            "F(x+t*xi)=F(x)+t*M*xi=F(x) identically, because there are no "
            "quadratic or cubic spoke terms"
        ),
        "deletion_example": {
            "point": [str(value) for value in point],
            "kernel_direction": [str(value) for value in direction],
            "deletion_parameter": str(parameter),
            "endpoint": [str(value) for value in endpoint],
        },
        "protected_rows": (
            "include every anchor/readout required to stay fixed as rows of "
            "M; their spoke restrictions are affine by the same occurrence "
            "argument.  A nonzero kernel coordinate is then automatically "
            "unprotected."
        ),
        "minimum_support_consequence": (
            "on the full three-spoke occupied branch, minimum occupied scalar "
            "support forbids ker(M)!=0, so rank(M/<target>)=2"
        ),
        "smaller_support_version": (
            "for k=1,2 occupied spokes the same proof forces quotient rank "
            "k-1 or deletes an occupied spoke"
        ),
    }


def typed_selector_counterguard() -> dict[str, object]:
    # A target row and two complete rows span all coordinate selectors, but
    # no literal row is private.  Label the rows by distinct output objects;
    # Gaussian elimination can isolate e_i only by mixing their labels.
    target = (Q(1), Q(1), Q(1))
    response_left = (Q(1, 2), Q(1, 2), Q(0))
    response_right = (Q(0), Q(1, 2), Q(1, 2))
    matrix = (target, response_left, response_right)
    require(rank(matrix) == 3
            and all(sum(value != 0 for value in row) >= 2 for row in matrix),
            matrix)

    # Explicit row-span coordinate selectors.
    selectors = (
        tuple(target[index] - 2 * response_right[index]
              for index in range(3)),
        tuple(-target[index] + 2 * response_left[index]
              + 2 * response_right[index] for index in range(3)),
        tuple(target[index] - 2 * response_left[index]
              for index in range(3)),
    )
    require(selectors == (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    ), selectors)
    # Gaussian elimination gives all three coordinate selectors exactly,
    # but only by combining differently labelled physical rows.
    standard = ((Q(1), Q(0), Q(0)),
                (Q(0), Q(1), Q(0)),
                (Q(0), Q(0), Q(1)))
    require(rank(matrix + standard) == 3,
            "the rank-three packet stopped spanning coordinate selectors")

    point = (Q(1), Q(1), Q(1))
    rhs = tuple(sum(left * right for left, right
                    in zip(row, point, strict=True)) for row in matrix)
    require(rhs == (Q(3), Q(1), Q(1)), rhs)
    return {
        "row_labels": [
            "pure target T[cccccc]",
            "response R11[word_left]",
            "response R12[word_right]",
        ],
        "restriction_matrix": [[str(value) for value in row] for row in matrix],
        "rank": rank(matrix),
        "rank_mod_target": rank(matrix) - 1,
        "literal_singleton_rows": 0,
        "coordinate_selectors_in_ungraded_row_span": True,
        "point": [str(value) for value in point],
        "row_values_at_point": [str(value) for value in rhs],
        "counterguard_scope": (
            "an exact affine restriction packet, not asserted to be a full "
            "GHZ source; it proves that rank two modulo target does not imply "
            "a labelled private response coefficient"
        ),
        "why_93cf9ae_does_not_follow": (
            "its processor needs the literal target-zero rows "
            "R11[110000], R11[110011], R11[111100], each with one selected "
            "occurrence before a mate is forced.  Row reduction here mixes a "
            "pure target normal, response heads, and output words; it has no "
            "single physical word/fine/repeated grade and supplies no Boolean "
            "privacy statement."
        ),
        "positive_content": (
            "the rank-two branch does give a local ungraded Fitting/coordinate "
            "selector and eliminates further affine-accessibility obstruction"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 active-coloop spoke-affine rank or exact deletion gate",
        "pins": PINS,
        "complete_multilinearity": matching_affinity_audit(),
        "rank_or_exact_deletion": rank_or_deletion_audit(),
        "rank_two_typing_counterguard": typed_selector_counterguard(),
        "shortest_remaining_theorem": (
            "upgrade the forced ungraded rank-two selector to a homogeneous, "
            "source-labelled private-tail packet: either the three named "
            "target-zero response coefficients of 93cf9ae are triangular on "
            "the selected tail, or failure yields a typed outside-shore/"
            "four-good/terminal dual.  No further nonlinear integration "
            "theorem is needed for the spoke branch."
        ),
        "frontier_effect": (
            "minimum support closes the affine-accessibility half: every "
            "full three-tail arbitrary coloop has rank two modulo its target "
            "row.  The sole remaining arbitrary-entry gap is promotion from "
            "that evaluated cross-row span to literal word/fine/private "
            "response rows; rank alone does not enter the special processor."
        ),
        "scope": (
            "exact canonical h=3 matching multilinearity and linear algebra, "
            "conditional on including all protected rows in the restriction "
            "matrix.  The typing counterguard is an affine row quotient, not "
            "a complete GHZ source."
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
    print("complete source in q2* spokes: AFFINE-LINEAR")
    print("minimum full spoke support: RANK 2 MOD TARGET FORCED")
    print("rank-deficient branch: EXACT AFFINE SUPPORT DELETION")
    print("rank-two selector -> 93cf9ae private rows: NOT IMPLIED")
    print("remaining: HOMOGENEOUS WORD/FINE PRIVATE-TAIL PROMOTION")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
