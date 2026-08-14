#!/usr/bin/env python3
"""Audit the trapped-coloop chart-submatching contraction shortcut.

At an evaluated normalized coloop, the three matching occurrences through
q01 have coefficient sum one, so their Koszul vector is a coefficientwise
contraction.  This audit separates that fact from the two further inputs
needed by the proposed shortcut: a chart-specific physical operation tag
and a unit/saturated *full capped core*.  It also records the exact one-line
Rees/Tor remainder when the latter is not available.

This is a source-typing theorem/counterguard, not a full-source computation.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/uniform-chart-odd-matching-exchange-operation-tag-tor-gate.md":
        "050191376b790ec1f7092f3ff3ef3f1f20f44bdcc9403e96048c598a27ce9493",
    "computations/verify_uniform_chart_odd_matching_exchange_operation_tag_tor_gate.py":
        "a835e816347b15f8c88c7f9995374468cd421cd68a64650bda128eda75ae8f39",
    "notes/h3-active-coloop-three-tail-localization-partition-guard.md":
        "5e8d56b79c0d1f6bdfc3919363f5ad533f1df7affec41db71f6a708b7c2dd8f3",
    "computations/verify_h3_active_coloop_three_tail_localization_partition_guard.py":
        "8fc6a7f112d9614beba202072f76a3e97c7f5c67177862d1ee552fb0d6381d09",
    "notes/h3-generic-symmetric-c4-core-saturation-tor-gate.md":
        "d0ea7112c33c94de2063e754e70dde9a6671d5fcd5213d4f2f1b62c51aa102bd",
    "computations/verify_h3_generic_symmetric_c4_core_saturation_tor_gate.py":
        "7307cb245996376f9847ff4852a4fdcd0a774152b4011ed92822022f93af03e5",
    "notes/h3-h2-chart-scalar-capped-c4-augmented-gate.md":
        "baee4965bcb9315fc7e9f51693aebcf3cfb6c8a147c76144eb287f7c9c74c998",
    "computations/verify_h3_h2_chart_scalar_capped_c4_augmented_gate.py":
        "18cb73805ffca0a080bc061c88cb42f6c0c83d57efd60c574455b757009785b4",
    "notes/h3-gate-ii-uniform-response-relative-carrier-landing-gate.md":
        "e1d0b1185cd72ff4d0d915abb1db25835f2848f65f1509458aee9f2325699084",
    "computations/verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py":
        "9b9c05a6789d2ade9359934f279eeb429591b2e85651ebaba8485195050417eb",
}
EXPECTED_LEDGER_SHA256 = "62a758fc868a853ecb33f88d6f7cfc4303e05119658ce8eb90fcc4af876b5232"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remaining):
            yield ((min(first, second), max(first, second)),) + tail


def rank(columns: list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    rows = len(matrix)
    cols = len(matrix[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][col]:
                continue
            factor = matrix[row][col]
            matrix[row] = [left - factor * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


# Laurent polynomials in one symbol A.  Negative exponents appear only in
# the explicitly localized audit.
Poly = dict[int, Q]


def poly(*terms: tuple[int, Q]) -> Poly:
    answer: Poly = {}
    for exponent, coefficient in terms:
        answer[exponent] = answer.get(exponent, Q(0)) + Q(coefficient)
        if not answer[exponent]:
            answer.pop(exponent)
    return answer


ZERO: Poly = {}
ONE = poly((0, Q(1)))
A = poly((1, Q(1)))
AINV = poly((-1, Q(1)))


def padd(left: Poly, right: Poly) -> Poly:
    return poly(*(tuple(left.items()) + tuple(right.items())))


def pscale(coefficient: Q, value: Poly) -> Poly:
    return poly(*((exponent, Q(coefficient) * scalar)
                  for exponent, scalar in value.items()))


def pmul(left: Poly, right: Poly) -> Poly:
    terms = []
    for left_exponent, left_scalar in left.items():
        for right_exponent, right_scalar in right.items():
            terms.append((left_exponent + right_exponent,
                          left_scalar * right_scalar))
    return poly(*terms)


def vadd(left: tuple[Poly, ...], right: tuple[Poly, ...]) \
        -> tuple[Poly, ...]:
    return tuple(padd(a, b) for a, b in zip(left, right, strict=True))


def vscale(coefficient: Poly, value: tuple[Poly, ...]) \
        -> tuple[Poly, ...]:
    return tuple(pmul(coefficient, entry) for entry in value)


def active_coloop_matching_audit() -> dict[str, object]:
    matchings = tuple(perfect_matchings(tuple(range(6))))
    sector = tuple(index for index, matching in enumerate(matchings)
                   if (0, 1) in matching)
    complement = tuple(index for index in range(len(matchings))
                       if index not in sector)
    require(len(matchings) == 15 and len(sector) == 3
            and len(complement) == 12,
            "six-site matching/coloop-sector census changed")

    # q01=2 and tail values (1/10,1/5,1/5) give q01*H2345=1.
    # Every complement matching is zero on the evaluated active-coloop
    # support.  The nonuniform choice prevents a symmetry-only pass.
    sector_weights = (Q(1, 5), Q(2, 5), Q(2, 5))
    weights = [Q(0)] * len(matchings)
    for index, weight in zip(sector, sector_weights, strict=True):
        weights[index] = weight
    require(sum(weights) == sum(weights[index] for index in sector) == 1,
            "active-coloop sector stopped being normalized")

    # Pure normalization alone does not normalize a proper sector.  The
    # split row (A,1-A) is the universal two-block counterguard.
    generic_sector_sum = Q(2, 5)
    generic_complement_sum = 1 - generic_sector_sum
    require(generic_sector_sum + generic_complement_sum == 1
            and generic_sector_sum != 1,
            "pure normalization accidentally forced the chosen sector")
    return {
        "six_site_perfect_matchings": len(matchings),
        "q01_sector_occurrences": len(sector),
        "complement_occurrences": len(complement),
        "evaluated_coloop_weights": [str(weight) for weight in sector_weights],
        "full_contraction_boundary": "1",
        "sector_contraction_boundary_on_coloop_locus": "q01*H2345=1",
        "pure_normalization_without_coloop": "A+(1-A)=1; A need not be 1",
        "scope": (
            "coefficient/Koszul normalization; it does not assign a physical "
            "restriction-operation tag to the submatching vector"
        ),
    }


def operation_tag_and_tor_audit() -> dict[str, object]:
    # Rows are (pq,pr).  U is the granted global contraction.  X is a
    # hypothetical source-valid pq-tagged sector chain with dX=A*e_pq.
    global_diagonal = (ONE, ONE)
    sector_diagonal = (A, A)
    sector_pq = (A, ZERO)
    chart_sign = (ONE, pscale(-1, ONE))

    require(vadd(vscale(poly((0, Q(2))), sector_pq),
                 vscale(pscale(-1, A), global_diagonal))
            == vscale(A, chart_sign),
            "d(2X-AU)=A*t changed")
    require(vadd(vscale(poly((0, Q(2))), vscale(AINV, sector_pq)),
                 vscale(poly((0, Q(-1))), global_diagonal))
            == chart_sign,
            "localized primitive dEta=t changed")
    require(vadd(sector_diagonal, vscale(pscale(-1, A), global_diagonal))
            == (ZERO, ZERO),
            "a diagonal sector unexpectedly acquired chart sign")

    # Over Q at any A != 0, a true chart-tagged sector column raises rank.
    # A diagonal sector never does.  On the fibre A=0 only the diagonal
    # global column remains, so the sign class survives as R/(A).
    eplus = (Q(1), Q(1))
    epq_nonzero = (Q(3), Q(0))
    diagonal_nonzero = (Q(3), Q(3))
    require(rank([eplus]) == rank([eplus, diagonal_nonzero]) == 1
            and rank([eplus, epq_nonzero]) == 2,
            "operation-tag rank dichotomy changed")
    require(rank([eplus, (Q(0), Q(0))]) == 1,
            "A=0 fibre stopped retaining the sign quotient")
    return {
        "global_boundary": "dU=e_pq+e_pr=e_+",
        "diagonal_sector_boundary": "A*e_+; no odd component even on D(A)",
        "hypothetical_chart_sector_boundary": "dX=A*e_pq",
        "undivided_identity": "d(2X-AU)=A*(e_pq-e_pr)=A*t",
        "localized_identity": "Eta=2*A^-1*X-U; dEta=t",
        "boundary_matrix": "[[1,A],[1,0]]",
        "maximal_minor": "-A",
        "global_rank": 1,
        "rank_with_diagonal_sector": 1,
        "rank_with_chart_sector_on_D(A)": 2,
        "residual_before_unit_or_saturation": "(R/(A))*t",
        "meaning": (
            "a unit or A-saturation removes the scalar core only after the "
            "pq-tagged physical chain X has independently been constructed"
        ),
    }


def capped_core_and_proper_face_audit() -> dict[str, object]:
    # On the pure active-coloop locus q01*H=1.  The direct response core is
    # nevertheless D*q01*H=D.  D=0 is compatible with the stated coloop
    # equation, so those hypotheses do not make the capped core a unit.
    for direction in (Q(0), Q(2), Q(-3)):
        q01 = Q(2)
        tail = Q(1, 2)
        require(q01 * tail == 1
                and direction * q01 * tail == direction,
                "direct core did not reduce to D on the coloop locus")
    require(Q(0) * Q(2) * Q(1, 2) == 0,
            "D=0 guard stopped killing the direct core")

    # Formal PP output coordinates are top, delta-D, delta-q01.  They are
    # distinct typed faces.  A top-only subtraction cannot cancel the two
    # Leibniz companions.
    top = (Q(1), Q(0), Q(0))
    delta_d = (Q(0), Q(1), Q(0))
    delta_q = (Q(0), Q(0), Q(1))
    require(rank([top, delta_d, delta_q]) == 3
            and rank([top]) == 1,
            "capped-core proper faces ceased to be independent")
    return {
        "lower_pure_core": "a=q01*H2345=1 on the active-coloop locus",
        "direct_response_core": "A=D*q01*H2345=D on that locus",
        "D_forced_unit_by_coloop": False,
        "literal_guard": "q01=2, H2345=1/2, D=0",
        "lower_unit_consequence": (
            "the three-term pure sector contracts coefficientwise"
        ),
        "direct_unit_consequence": (
            "only after a same-grade inverse for the full capped core D*q01*H2345"
        ),
        "cap_Leibniz_faces": [
            "D*q01*dU",
            "(delta D)*q01*U",
            "D*(delta q01)*U",
        ],
        "proper_face_rank": 3,
        "complete_response_debt": (
            "the direct nine-term Dq01 block is not the complete 105-term "
            "response; occurrence-block isolation remains independent"
        ),
    }


def exact_hypothesis_ladder() -> dict[str, object]:
    return {
        "H0_pure_normalization": {
            "gives": "absolute global matching contraction U",
            "does_not_give": "normalization of an arbitrary proper sector",
        },
        "active_coloop_q01_H2345_equals_1": {
            "gives": "coefficientwise normalized three-occurrence pure sector",
            "does_not_give": (
                "a physical pq-only restriction tag, occurrence projector, "
                "or capped D insertion"
            ),
        },
        "chart_diagonal_submatching_chain": {
            "gives": "another multiple of e_+",
            "does_not_give": "any boundary multiple of t",
        },
        "source_valid_pq_tagged_unnormalized_chain_X": {
            "gives": "A*t=d(2X-AU)",
            "does_not_give": "t unless A is a unit or the image is A-saturated",
        },
        "full_core_unit_or_saturation": {
            "gives": "dEta=t, conditional on X and all proper-face cancellations",
            "does_not_give": (
                "X itself; using this alone merely restates the previously "
                "isolated common-core colon theorem"
            ),
        },
        "physical_completion_required": [
            "pq/pr restriction-operation label before contraction",
            "word/fine/repeated and response-head landing",
            "delta-D and delta-q01 reinsertion faces",
            "nine-of-105 occurrence-block projector or a combined pointed cell",
            "target, anchor/ainc, physical q, W, labelled residue/ridge, eta, sigma",
        ],
    }


def mutation_guards() -> dict[str, object]:
    # If the sector is silently retagged diagonally, determinant/rank cannot
    # rise.  If A is silently cancelled, the A=0 fibre catches it.  If the
    # capped direction is silently declared a unit, D=0 catches it.
    require(rank([(Q(1), Q(1)), (Q(2), Q(2))]) == 1,
            "diagonal-tag mutation escaped")
    require(rank([(Q(1), Q(1)), (Q(0), Q(0))]) == 1,
            "silent A cancellation escaped")
    require(Q(0) * Q(3) == 0, "silent D-unit mutation escaped")
    return {
        "diagonal_tag_mutation_detected": True,
        "silent_core_cancellation_detected": True,
        "silent_D_unit_mutation_detected": True,
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 trapped-coloop chart-submatching contraction gate",
        "pins": PINS,
        "active_coloop_matching_sector": active_coloop_matching_audit(),
        "operation_tag_and_one_line_Tor": operation_tag_and_tor_audit(),
        "capped_core_and_proper_faces": capped_core_and_proper_face_audit(),
        "exact_hypothesis_ladder": exact_hypothesis_ladder(),
        "mutation_guards": mutation_guards(),
        "verdict": (
            "The active-coloop equation normalizes q01*H2345 and therefore "
            "the selected pure matching sector at coefficient/Koszul level. "
            "It does not make that contraction chart-specific.  Every "
            "currently source-provenant global/submatching lift remains "
            "diagonal and leaves t.  If a new pq-tagged chain X is supplied, "
            "the exact identity is d(2X-AU)=A*t; cancelling A is precisely a "
            "full-core unit/saturation step.  For the capped Dq01 sector, "
            "A=D on the coloop locus, and neither D nor the cap's proper "
            "faces nor the nine-term response projector is currently forced."
        ),
        "scope": (
            "Exact canonical h=3 coefficient, matching-Koszul, operation-tag, "
            "unit/colon, and capped-principal-parts audit.  The coloop example "
            "is an evaluated physical pure-word coefficient packet, not a new "
            "complete GHZ tensor or an exhaustive decorated source complex."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("trapped-coloop submatching ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 trapped-coloop chart-submatching contraction gate: PASS")
    print("pure q01*H2345 sector: COEFFICIENTWISE NORMALIZED")
    print("source-provenant operation tag: STILL DIAGONAL")
    print("conditional exact identity: d(2X-AU)=A*t")
    print("direct capped core on coloop locus: A=D, NOT FORCED UNIT")
    print("shortcut dEta=t: REQUIRES NEW CHART LIFT + FULL-CORE CANCELLATION")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
