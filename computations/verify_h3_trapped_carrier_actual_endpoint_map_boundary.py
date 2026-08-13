#!/usr/bin/env python3
r"""Expose the actual fixed-q endpoint map and its sharp bordered duality.

At h=3, fix the common residual two-form q and the two right endpoint
rows s_1,s_2.  The derivative in the two left endpoint rows p_1,p_2 of

    p_i s_j q^[2] = delta_ij X_i

is a 4*3^6 by 36 matrix.  This checker constructs that matrix twice over
the universal decorated coefficient ring: once by enumerating physical
matching occurrences and once from the closed cofactor formula.  The two
constructions agree coefficient by coefficient.

The unary row q^[3]=X_0 has zero derivative in every endpoint column.  It
selects the fixed-q fibre before this map is formed; it cannot increase its
endpoint rank.  Word, response-head, and orientation data are literal row
and variable labels.  A selected marked anchor occurrence is a nonzero
scalar multiple of one endpoint coordinate selector, but that selector is
a protection constraint, not a physical source equation unless a separate
source row realizing it has been proved.

Consequently the four-way complete-fibre alternative needs one refinement.
A selector in row([R;H]) is a genuine physical dual only when it already
lies in row(R), where R is the four-response map and H is the protection
border.  The checker gives sharp rational guards for physical transverse
rank, anchor-safe dependence, protection-only rank, physical dual, and a
surviving protection-only covector.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_h3_active_fan_coloop_saturation_boundary.py":
        "35658ebed521b93387fc00aa7d2600d703f57b3e5e5deca67a11a1ab155d6c56",
    "computations/verify_n8_one_bad_affine_guard_full_packet_unit.py":
        "3ecada544805a3ab25206973f8a29395f8d2df34a1b6066460eb85462c24c2b1",
    "computations/verify_uniform_one_bad_third_cofactor_pure_carrier_gate.py":
        "9f346fd63964802c1286d76a27d6f9dfa2d1382545b44f31f976054310cbcaaf",
}
EXPECTED_LEDGER_SHA256 = (
    "e3ec6fc86bb0b50ad42b8a24bc77c49d67e15954abebf151e0ddab17270f5355"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
WORDS = tuple(product(COLOURS, repeat=6))
P_COLUMNS = tuple((i, u, a) for i in range(2)
                  for u in SITES for a in COLOURS)
Monomial = tuple[tuple[object, ...], ...]
Polynomial = Counter[Monomial]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def q_variable(u: int, v: int, a: int, b: int):
    if u > v:
        u, v, a, b = v, u, b, a
    return ("q", u, v, a, b)


def s_variable(j: int, v: int, b: int):
    return ("s", j, v, b)


def monomial(*variables):
    return tuple(sorted(variables))


def direct_column(i: int, u: int, a: int):
    """Enumerate every physical occurrence containing p_i[u,a]."""
    rows = defaultdict(Counter)
    for j in range(2):
        for v in SITES:
            if v == u:
                continue
            complement = tuple(site for site in SITES if site not in (u, v))
            for b in COLOURS:
                for matching in perfect_matchings(complement):
                    for q_word in product(COLOURS, repeat=4):
                        assignment = dict(zip(complement, q_word, strict=True))
                        word = [None] * 6
                        word[u], word[v] = a, b
                        for site in complement:
                            word[site] = assignment[site]
                        q_factors = tuple(q_variable(
                            left, right, assignment[left], assignment[right]
                        ) for left, right in matching)
                        rows[(i, j, tuple(word))][monomial(
                            s_variable(j, v, b), *q_factors
                        )] += Q(1)
    return {row: polynomial for row, polynomial in rows.items()
            if any(polynomial.values())}


def formula_column(i: int, u: int, a: int):
    r"""Use delta_{ik} delta_{a,w_u} sum_v s_j[v,w_v] Haf(q)."""
    rows = {}
    for j in range(2):
        for word in WORDS:
            if word[u] != a:
                continue
            polynomial = Counter()
            for v in SITES:
                if v == u:
                    continue
                complement = tuple(site for site in SITES
                                   if site not in (u, v))
                for matching in perfect_matchings(complement):
                    q_factors = tuple(q_variable(
                        left, right, word[left], word[right]
                    ) for left, right in matching)
                    polynomial[monomial(
                        s_variable(j, v, word[v]), *q_factors
                    )] += Q(1)
            rows[(i, j, word)] = polynomial
    return rows


def polynomial_stream_digest(columns):
    digest = sha256()
    nonzero_entries = 0
    monomial_terms = 0
    for column, rows in columns:
        for row in sorted(rows):
            polynomial = rows[row]
            nonzero_entries += 1
            monomial_terms += len(polynomial)
            record = [column, row, [
                [list(map(list, term)), str(coefficient)]
                for term, coefficient in sorted(polynomial.items())
            ]]
            digest.update(json.dumps(record, separators=(",", ":")).encode())
    return digest.hexdigest(), nonzero_entries, monomial_terms


def audit_universal_left_map():
    audited = []
    for column in P_COLUMNS:
        direct = direct_column(*column)
        formula = formula_column(*column)
        require(direct == formula,
                ("endpoint cofactor formula changed", column))
        audited.append((column, formula))
    stream, entries, terms = polynomial_stream_digest(audited)
    require(entries == 4 * (3 ** 6) * 6,
            ("nonzero response-entry count changed", entries))
    require(terms == entries * 15,
            ("generic response monomial count changed", terms))

    # Each response head uses only the matching left endpoint row.  The
    # target constants are X_1 in 11, X_2 in 22, and zero in 12/21.
    rhs = {
        "11:" + "1" * 6: "1",
        "22:" + "2" * 6: "1",
    }
    return {
        "domain_columns": len(P_COLUMNS),
        "conceptual_response_rows": 4 * (3 ** 6),
        "generic_nonzero_entries": entries,
        "generic_monomial_terms": terms,
        "terms_per_nonzero_entry": 15,
        "universal_matrix_stream_sha256": stream,
        "response_rhs_nonzero_rows": rhs,
        "block_sparsity": (
            "column (i,u,a) occurs only in response heads (i,1),(i,2)"
        ),
    }


def rref(matrix, width=None):
    work = [list(map(Q, row)) for row in matrix]
    if width is None:
        width = len(work[0]) if work else 0
    require(all(len(row) == width for row in work), "ragged matrix")
    pivots = []
    row = 0
    for column in range(width):
        pivot = next((index for index in range(row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            value = work[index][column]
            work[index] = [left - value * right for left, right in
                           zip(work[index], work[row], strict=True)]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    return tuple(tuple(item) for item in work), tuple(pivots)


def rank(matrix, width=None):
    return len(rref(matrix, width)[1])


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in zip(row, vector, strict=True))
                 for row in matrix)


def columns(matrix):
    return tuple(tuple(column) for column in zip(*matrix, strict=True))


def column_matrix(selected):
    if not selected:
        return ()
    return tuple(tuple(column[row] for column in selected)
                 for row in range(len(selected[0])))


def solve(matrix, rhs):
    rows = len(matrix)
    variables = len(matrix[0]) if rows else 0
    augmented = tuple(tuple(map(Q, row)) + (Q(value),)
                      for row, value in zip(matrix, rhs, strict=True))
    reduced, pivots = rref(augmented, variables + 1)
    if any(not any(row[:variables]) and row[variables] for row in reduced):
        return None
    require(variables not in pivots, "consistent solve pivoted in rhs")
    answer = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        if pivot < variables:
            answer[pivot] = reduced[row][variables]
    require(mat_vec(matrix, answer) == tuple(map(Q, rhs)),
            "solution reconstruction failed")
    return tuple(answer)


def minimum_support_solution(matrix, target):
    all_columns = columns(matrix)
    effective = tuple(index for index, column in enumerate(all_columns)
                      if any(column))
    for size in range(1, len(effective) + 1):
        for support in combinations(effective, size):
            restricted = column_matrix(tuple(all_columns[index]
                                             for index in support))
            coefficients = solve(restricted, target)
            if coefficients is None or any(value == 0 for value in coefficients):
                continue
            return support, coefficients, effective
    return None


def in_span(selected, candidate):
    return solve(column_matrix(selected), candidate) is not None if selected \
        else not any(candidate)


def classify_bordered(response, protection, response_rhs, protection_rhs):
    """Classify a complete fixed-q endpoint fibre without conflating rows."""
    response = tuple(tuple(map(Q, row)) for row in response)
    protection = tuple(tuple(map(Q, row)) for row in protection)
    complete = response + protection
    target = tuple(map(Q, response_rhs)) + tuple(map(Q, protection_rhs))
    require(complete and complete[0] and len(complete) == len(target),
            "empty bordered fibre")
    minimum = minimum_support_solution(complete, target)
    require(minimum is not None and any(target), "fibre must be nonempty")
    support, coefficients, effective = minimum
    complete_columns = columns(complete)
    response_columns = columns(response)
    basis_complete = tuple(complete_columns[index] for index in support)
    basis_response = tuple(response_columns[index] for index in support)
    require(rank(column_matrix(basis_complete)) == len(support),
            "minimum bordered support is not independent")

    if len(support) == 1:
        return {"outcome": "constrained_coordinate_access",
                "support": list(support)}

    outside = tuple(index for index in effective if index not in support)
    physical_transverse = next((index for index in outside
        if not in_span(basis_response, response_columns[index])), None)
    if physical_transverse is not None:
        return {"outcome": "physical_response_rank_exit",
                "support": list(support), "column": physical_transverse}

    dependent = next((index for index in outside
        if in_span(basis_complete, complete_columns[index])), None)
    if dependent is not None:
        coefficients = solve(column_matrix(basis_complete),
                             complete_columns[dependent])
        require(coefficients is not None, "lost fundamental circuit")
        relation = [Q(0)] * len(complete_columns)
        relation[dependent] = Q(1)
        for index, coefficient in zip(support, coefficients, strict=True):
            relation[index] = -coefficient
        require(not any(mat_vec(response, relation))
                and not any(mat_vec(protection, relation)),
                "complete dependence lost response/protection safety")
        return {"outcome": "anchor_safe_complete_column_dependence",
                "support": list(support), "column": dependent,
                "relation": list(map(str, relation))}

    if outside:
        # Physical response images are already dependent, but the border
        # detects every such relation.  This is a protection obstruction,
        # not a response/Fitting rank increase.
        return {"outcome": "protection_only_rank_exit",
                "support": list(support), "column": outside[0]}

    coordinate = support[0]
    selector = tuple(Q(index == coordinate)
                     for index in range(len(complete_columns)))
    physical_dual = solve(tuple(zip(*response, strict=True)), selector)
    if physical_dual is not None:
        return {"outcome": "genuine_physical_response_dual",
                "support": list(support), "coordinate": coordinate,
                "dual": list(map(str, physical_dual))}
    bordered_dual = solve(tuple(zip(*complete, strict=True)), selector)
    require(bordered_dual is not None, "full bordered rank lost selector")
    response_multiplier_count = len(response)
    require(any(bordered_dual[response_multiplier_count:]),
            "nonphysical selector unexpectedly avoided protection rows")
    return {"outcome": "surviving_protection_covector",
            "support": list(support), "coordinate": coordinate,
            "bordered_dual": list(map(str, bordered_dual))}


def audit_refined_alternative():
    empty = ()
    named = {
        "coordinate": classify_bordered(
            ((1, 0),), empty, (1,), empty),
        "physical_rank": classify_bordered(
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)), empty,
            (1, 1, 0), empty),
        "dependence": classify_bordered(
            ((1, 0, 1), (0, 1, -1)), empty, (1, 1), empty),
        "protection_rank": classify_bordered(
            ((1, 0, 1), (0, 1, 1)),
            ((1, 0, 0), (0, 1, 0)),
            (1, 1), (1, 1)),
        "physical_dual": classify_bordered(
            ((1, 0), (0, 1)), empty, (1, 1), empty),
        "protection_covector": classify_bordered(
            ((1, 1),), ((1, 0),), (2,), (1,)),
    }
    expected = {
        "coordinate": "constrained_coordinate_access",
        "physical_rank": "physical_response_rank_exit",
        "dependence": "anchor_safe_complete_column_dependence",
        "protection_rank": "protection_only_rank_exit",
        "physical_dual": "genuine_physical_response_dual",
        "protection_covector": "surviving_protection_covector",
    }
    require({name: record["outcome"] for name, record in named.items()}
            == expected, ("refined branch guards changed", named))
    return named


def audit_anchor_occurrence():
    # Mark the physical occurrence
    # p_1[0,1] s_1[1,1] q_23[0,0] q_45[0,0].  On the fixed q,s fibre its
    # coefficient is the scalar tail times the literal p coordinate.  It is
    # one summand of response row (11,110000), not that aggregate row.
    selected_column = P_COLUMNS.index((0, 0, 1))
    tail = monomial(
        s_variable(0, 1, 1), q_variable(2, 3, 0, 0),
        q_variable(4, 5, 0, 0),
    )
    row = formula_column(0, 0, 1)[(0, 0, (1, 1, 0, 0, 0, 0))]
    require(row[tail] == 1 and len(row) == 15,
            "selected occurrence lost its aggregate response row")
    protection = [Q(0)] * len(P_COLUMNS)
    protection[selected_column] = Q(1)
    return {
        "marked_occurrence": "p1[0,1] s1[1,1] q23[0,0] q45[0,0]",
        "response_row": "11:110000",
        "aggregate_response_monomials": len(row),
        "fixed_tail_protection_row": (
            "the coordinate selector e_(p1[0,1]) after division by the "
            "chosen nonzero s*q*q tail"
        ),
        "selector_nonzero_entries": sum(bool(value) for value in protection),
        "typing_warning": (
            "the divided marked-occurrence selector is not the aggregate "
            "physical response equation and cannot support a physical dual "
            "without an independent source-row realization"
        ),
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    universal = audit_universal_left_map()
    anchors = audit_anchor_occurrence()
    alternatives = audit_refined_alternative()
    ledger = {
        "theorem": "actual fixed-common-q endpoint map boundary",
        "pins": PINS,
        "left_endpoint_map": universal,
        "right_endpoint_map": (
            "the identical formula with p and s interchanged; after a left "
            "move it must be rebuilt using the new p rows"
        ),
        "unary_block": {
            "equation": "q^[3]=X0",
            "endpoint_derivative_rows": 3 ** 6,
            "all_endpoint_entries": "zero",
            "role": (
                "select a unary-compatible q fibre before endpoint rank; a "
                "nonzero unary residual is the already pinned ordinary unit"
            ),
        },
        "protected_labels": (
            "response head (ij), six-letter output word, endpoint site/colour, "
            "orientation, and common-q grade are literal indices of the map; "
            "no projection or unlabelled occurrence quotient is taken"
        ),
        "selected_anchor_entry": anchors,
        "refined_support_minimal_alternative": alternatives,
        "physical_dual_criterion": (
            "for an occupied coordinate j, e_j^* is a genuine fixed-q "
            "physical response dual iff e_j^* lies in row(R), equivalently "
            "rank(R)=rank([R;e_j^*]); membership only in row([R;H_A]) gives "
            "a constrained-fibre protection covector"
        ),
        "remaining_relative_gate": (
            "evaluate this universal R at the unary-compatible trapped source "
            "and either obtain coordinate access, physical response rank, or "
            "an H_A-safe circuit.  If only the protection covector survives, "
            "prove its anchor selector is an actual source row or extend the "
            "map by simultaneous q-deformation columns and rerun the rank "
            "alternative"
        ),
        "known_guard_status": (
            "the frozen X1+Y,-Y affine guard is not unary-compatible and is "
            "removed by q^[3][000000]-1=-1; it supplies no survivor here"
        ),
        "scope": (
            "universal exact fixed-q endpoint Jacobian and sharp bordered "
            "linear alternative; not a uniform rank evaluation at every "
            "unknown source, not a physical realization of marked anchor "
            "selectors, and not a dual against simultaneous q motion"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("actual endpoint-map ledger changed", digest))
    print("h3 trapped carrier actual fixed-q endpoint map: PASS")
    print("unary endpoint block: 729x36 zero")
    print("four-response block: 2916x36, 17496 generic nonzero entries")
    print("support alternatives: coordinate / physical rank / dependence")
    print("sharp survivor: protection-only covector, not yet physical")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
