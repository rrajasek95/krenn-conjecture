#!/usr/bin/env python3
r"""Append all q columns and classify the sole protection-only branch.

For h=3, the fixed-right physical differential has 171 columns: 36 left
endpoint coordinates and 135 decorated common-q coordinates.  The q block
contains all 729 unary derivatives and all 2916 four-response derivatives.
This checker constructs the q columns both by differentiating literal
matching occurrences and by the closed cofactor formulas.

Let A be this complete physical map after evaluation, H one selected marked
anchor differential, e the selector left by the fixed-q protection branch,
and Lambda the physically typed six-term readout.  Exact row-space duality
gives the exhaustive refinement:

* e is visible on ker[A;H]: anchor-safe kernel exchange;
* e is in row(A): physical response/source dual;
* Lambda is visible on ker[A;H]: the six-term relative generator;
* otherwise e=lambda A+cH, Lambda=nu A+mu H.  If mu is nonzero, eliminate H
  and transport [e] to the physical six-term row.  If mu=0, Lambda already
  lies in row(A) while [H] survives: this is the single sharp counterguard.

Thus adding q columns introduces no Hall branch.  It reduces the remaining
physical theorem to excluding that last coefficient-zero case (or realizing
the anchor row directly).
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trapped_carrier_actual_endpoint_map_boundary.py":
        "1735de099eeaec04a2197c613350fba4bd52d8955873c8a032894d8653087a0a",
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
}
EXPECTED_LEDGER_SHA256 = (
    "e515f5987ce2d716699f76842ea897ef5ddfae4248d0c51791b90323d5113a10"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
WORDS = tuple(product(COLOURS, repeat=6))
Q_COLUMNS = tuple((u, v, a, b)
                  for u in SITES for v in SITES if u < v
                  for a in COLOURS for b in COLOURS)


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


def p_variable(i: int, u: int, a: int):
    return ("p", i, u, a)


def s_variable(j: int, v: int, b: int):
    return ("s", j, v, b)


def monomial(*variables):
    return tuple(sorted(variables))


def unary_q_column_formula(u: int, v: int, a: int, b: int):
    rows = {}
    complement = tuple(site for site in SITES if site not in (u, v))
    for word in WORDS:
        if (word[u], word[v]) != (a, b):
            continue
        polynomial = Counter()
        for matching in perfect_matchings(complement):
            polynomial[monomial(*(q_variable(
                left, right, word[left], word[right]
            ) for left, right in matching))] += Q(1)
        rows[word] = polynomial
    return rows


def unary_q_column_direct(u: int, v: int, a: int, b: int):
    rows = defaultdict(Counter)
    selected_edge = (u, v)
    for matching in perfect_matchings(SITES):
        if selected_edge not in matching:
            continue
        others = tuple(edge for edge in matching if edge != selected_edge)
        remaining_sites = tuple(site for edge in others for site in edge)
        for colours in product(COLOURS, repeat=4):
            assignment = {u: a, v: b}
            assignment.update(dict(zip(remaining_sites, colours, strict=True)))
            word = tuple(assignment[site] for site in SITES)
            rows[word][monomial(*(q_variable(
                left, right, assignment[left], assignment[right]
            ) for left, right in others))] += Q(1)
    return dict(rows)


def response_q_column_formula(u: int, v: int, a: int, b: int):
    rows = {}
    available = tuple(site for site in SITES if site not in (u, v))
    for i in range(2):
        for j in range(2):
            for word in WORDS:
                if (word[u], word[v]) != (a, b):
                    continue
                polynomial = Counter()
                for left_site in available:
                    for right_site in available:
                        if right_site == left_site:
                            continue
                        remaining = tuple(site for site in available
                                          if site not in (left_site, right_site))
                        require(len(remaining) == 2,
                                "response complement stopped being one edge")
                        polynomial[monomial(
                            p_variable(i, left_site, word[left_site]),
                            s_variable(j, right_site, word[right_site]),
                            q_variable(remaining[0], remaining[1],
                                       word[remaining[0]], word[remaining[1]]),
                        )] += Q(1)
                rows[(i, j, word)] = polynomial
    return rows


def response_q_column_direct(u: int, v: int, a: int, b: int):
    rows = defaultdict(Counter)
    selected_edge = (u, v)
    for i in range(2):
        for j in range(2):
            for left_site in SITES:
                for right_site in SITES:
                    if left_site == right_site:
                        continue
                    complement = tuple(site for site in SITES
                                       if site not in (left_site, right_site))
                    for matching in perfect_matchings(complement):
                        if selected_edge not in matching:
                            continue
                        other_edge = next(edge for edge in matching
                                          if edge != selected_edge)
                        for left_colour, right_colour in product(COLOURS, repeat=2):
                            for other_colours in product(COLOURS, repeat=2):
                                assignment = {
                                    left_site: left_colour,
                                    right_site: right_colour,
                                    u: a, v: b,
                                    other_edge[0]: other_colours[0],
                                    other_edge[1]: other_colours[1],
                                }
                                require(len(assignment) == 6,
                                        "selected q edge collided with endpoint")
                                word = tuple(assignment[site] for site in SITES)
                                rows[(i, j, word)][monomial(
                                    p_variable(i, left_site, left_colour),
                                    s_variable(j, right_site, right_colour),
                                    q_variable(other_edge[0], other_edge[1],
                                               *other_colours),
                                )] += Q(1)
    return dict(rows)


def polynomial_stream_digest(columns):
    digest = sha256()
    nonzero_entries = 0
    terms = 0
    for label, unary, response in columns:
        for block, rows in (("U", unary), ("R", response)):
            for row in sorted(rows):
                polynomial = rows[row]
                nonzero_entries += 1
                terms += len(polynomial)
                digest.update(json.dumps(
                    [label, block, row, [
                        [list(map(list, term)), str(coefficient)]
                        for term, coefficient in sorted(polynomial.items())
                    ]], separators=(",", ":")
                ).encode())
    return digest.hexdigest(), nonzero_entries, terms


def audit_q_jacobian():
    columns = []
    unary_entries = response_entries = 0
    unary_terms = response_terms = 0
    for label in Q_COLUMNS:
        unary = unary_q_column_formula(*label)
        response = response_q_column_formula(*label)
        require(unary == unary_q_column_direct(*label),
                ("unary q derivative formula changed", label))
        require(response == response_q_column_direct(*label),
                ("response q derivative formula changed", label))
        unary_entries += len(unary)
        unary_terms += sum(len(polynomial) for polynomial in unary.values())
        response_entries += len(response)
        response_terms += sum(len(polynomial)
                              for polynomial in response.values())
        columns.append((label, unary, response))
    require((unary_entries, unary_terms) == (10935, 32805),
            ("unary q block count changed", unary_entries, unary_terms))
    require((response_entries, response_terms) == (43740, 524880),
            ("response q block count changed", response_entries,
             response_terms))
    stream, entries, terms = polynomial_stream_digest(columns)
    require((entries, terms) == (54675, 557685),
            "combined q Jacobian count changed")
    return {
        "q_columns": len(Q_COLUMNS),
        "endpoint_columns_carried_from_1fe8dce": 36,
        "full_fixed_right_domain_columns": 171,
        "unary": {
            "rows": 3 ** 6,
            "generic_nonzero_entries": unary_entries,
            "monomial_terms": unary_terms,
            "formula": (
                "delta_((w_u,w_v),(a,b))*"
                "Haf_q(R\\{u,v};w restricted)"
            ),
        },
        "four_responses": {
            "rows": 4 * (3 ** 6),
            "generic_nonzero_entries": response_entries,
            "monomial_terms": response_terms,
            "terms_per_nonzero_entry": 12,
            "formula": (
                "delta_((w_u,w_v),(a,b))*sum_(x!=y outside uv) "
                "p_i[x,w_x]s_j[y,w_y]q_[remaining pair]"
            ),
        },
        "universal_q_column_stream_sha256": stream,
    }


def marked_anchor_gradient():
    # One literal occurrence inside response row 11:110000.
    p = p_variable(0, 0, 1)
    s = s_variable(0, 1, 1)
    q23 = q_variable(2, 3, 0, 0)
    q45 = q_variable(4, 5, 0, 0)
    gradient = {
        p: monomial(s, q23, q45),
        q23: monomial(p, s, q45),
        q45: monomial(p, s, q23),
    }
    require(len(gradient) == 3,
            "marked matching occurrence gradient changed")
    return {
        "occurrence": "p1[0,1]s1[1,1]q23[0,0]q45[0,0]",
        "fixed_q_border": "after tail localization, e_(p1[0,1])",
        "full_pq_differential_nonzero_coordinates": [repr(key)
                                                       for key in gradient],
        "full_differential": {
            repr(key): repr(value) for key, value in gradient.items()
        },
        "consequence": (
            "once q moves, the selected-anchor row is the complete product-"
            "rule differential, not the old endpoint coordinate selector"
        ),
    }


def rref(rows, width=None):
    work = [list(map(Q, row)) for row in rows]
    if width is None:
        width = len(work[0]) if work else 0
    require(all(len(row) == width for row in work), "ragged matrix")
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def nullspace(rows, width):
    if not rows:
        return tuple(tuple(Q(index == free) for index in range(width))
                     for free in range(width))
    reduced, pivots = rref(rows, width)
    free = tuple(column for column in range(width) if column not in pivots)
    basis = []
    for column in free:
        vector = [Q(0)] * width
        vector[column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][column]
        basis.append(tuple(vector))
    return tuple(basis)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def solve_row(rows, target):
    if not rows:
        return () if not any(target) else None
    variables = len(rows)
    equations = [tuple(column) + (Q(value),) for column, value in
                 zip(zip(*rows, strict=True), target, strict=True)]
    reduced, pivots = rref(equations, variables + 1)
    if any(not any(row[:variables]) and row[variables] for row in reduced):
        return None
    solution = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        if pivot < variables:
            solution[pivot] = reduced[row][variables]
    require(all(sum(solution[row] * Q(rows[row][column])
                    for row in range(variables)) == Q(target[column])
                for column in range(len(target))),
            "row solution failed reconstruction")
    return tuple(solution)


def classify(physical_rows, anchor, selector, six_term):
    physical_rows = tuple(tuple(map(Q, row)) for row in physical_rows)
    anchor = tuple(map(Q, anchor))
    selector = tuple(map(Q, selector))
    six_term = tuple(map(Q, six_term))
    width = len(anchor)
    require(all(len(row) == width for row in physical_rows)
            and len(selector) == len(six_term) == width,
            "classification width changed")
    protected = physical_rows + (anchor,)
    kernel = nullspace(protected, width)
    exchange = next((vector for vector in kernel if dot(selector, vector)), None)
    if exchange is not None:
        normalized = tuple(value / dot(selector, exchange)
                           for value in exchange)
        require(all(not dot(row, normalized) for row in protected)
                and dot(selector, normalized) == 1,
                "anchor-safe exchange normalization changed")
        return {"outcome": "anchor_safe_kernel_exchange",
                "witness": list(map(str, normalized))}

    protected_factor = solve_row(protected, selector)
    require(protected_factor is not None,
            "selector killed protected kernel but did not factor")
    physical_factor = solve_row(physical_rows, selector)
    if physical_factor is not None:
        return {"outcome": "physical_response_source_dual",
                "factor": list(map(str, physical_factor))}

    anchor_coefficient = protected_factor[-1]
    require(anchor_coefficient,
            "protection-only selector acquired zero anchor coefficient")

    six_visible = next((vector for vector in kernel
                        if dot(six_term, vector)), None)
    if six_visible is not None:
        normalized = tuple(value / dot(six_term, six_visible)
                           for value in six_visible)
        require(all(not dot(row, normalized) for row in protected)
                and dot(six_term, normalized) == 1,
                "six-term generator normalization changed")
        return {"outcome": "physical_six_term_relative_generator",
                "selector_anchor_coefficient": str(anchor_coefficient),
                "witness": list(map(str, normalized))}

    six_factor = solve_row(protected, six_term)
    require(six_factor is not None,
            "six-term row killed protected kernel but did not factor")
    six_anchor_coefficient = six_factor[-1]
    if six_anchor_coefficient:
        # e = l*A+cH and Lambda=n*A+mu*H; eliminate H.
        physical_part = tuple(
            protected_factor[index]
            - anchor_coefficient * six_factor[index] / six_anchor_coefficient
            for index in range(len(physical_rows))
        )
        six_coefficient = anchor_coefficient / six_anchor_coefficient
        reconstructed = tuple(
            sum(physical_part[row] * physical_rows[row][column]
                for row in range(len(physical_rows)))
            + six_coefficient * six_term[column]
            for column in range(width)
        )
        require(reconstructed == selector,
                "six-term quotient transport reconstruction changed")
        return {"outcome": "six_term_quotient_transport_separator",
                "selector_anchor_coefficient": str(anchor_coefficient),
                "six_term_anchor_coefficient": str(six_anchor_coefficient),
                "selector_in_row_A_plus_Lambda": True}

    require(solve_row(physical_rows, six_term) is not None,
            "zero H coefficient did not put six-term row in physical span")
    return {"outcome": "independent_protection_quotient_counterguard",
            "selector_anchor_coefficient": str(anchor_coefficient),
            "six_term_anchor_coefficient": "0",
            "six_term_in_physical_row_span": True,
            "selector_in_physical_row_span": False}


def audit_named_branches():
    cases = {
        "exchange": classify(((1, 0),), (0, 0), (0, 1), (0, 0)),
        "physical_dual": classify(((1, 0),), (0, 1), (1, 0), (0, 0)),
        "six_term_generator": classify(
            ((1, 0, 0),), (0, 1, 0), (0, 1, 0), (0, 0, 1)),
        "transport": classify(
            ((1, 0),), (0, 1), (0, 1), (1, 2)),
        "sharp_survivor": classify(
            ((1, 0, 0),), (0, 1, 0), (0, 1, 0), (1, 0, 0)),
    }
    expected = {
        "exchange": "anchor_safe_kernel_exchange",
        "physical_dual": "physical_response_source_dual",
        "six_term_generator": "physical_six_term_relative_generator",
        "transport": "six_term_quotient_transport_separator",
        "sharp_survivor": "independent_protection_quotient_counterguard",
    }
    require({name: record["outcome"] for name, record in cases.items()}
            == expected, ("extension branch guards changed", cases))
    return cases


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    q_jacobian = audit_q_jacobian()
    anchor = marked_anchor_gradient()
    branches = audit_named_branches()
    ledger = {
        "theorem": "trapped-carrier full-q six-term extension alternative",
        "pins": PINS,
        "actual_full_fixed_right_Jacobian": q_jacobian,
        "actual_anchor_product_rule": anchor,
        "row_space_alternative": branches,
        "notation": {
            "A": (
                "evaluated 3645-row unary plus four-response physical map "
                "on 36 endpoint plus 135 q columns, together with any other "
                "already physical protected-zero rows"
            ),
            "H": "complete product-rule differential of the selected anchor",
            "e": "selector isolated by the support-minimal fixed-q branch",
            "Lambda": (
                "physical six-term row sum(m_1,...,m_6)-ainc in the same "
                "labelled repeated relative grade"
            ),
        },
        "exact_exhaustion": (
            "first test e on ker[A;H], then row(A).  In the sole protection "
            "case e=lambda A+cH with c nonzero.  Test Lambda on ker[A;H].  "
            "A visible Lambda is the pinned relative generator.  Otherwise "
            "Lambda=nu A+mu H.  Nonzero mu eliminates H and transports e "
            "to row(A,Lambda); mu=0 is the only surviving quotient class"
        ),
        "sharp_remaining_physical_statement": (
            "on the actual unary-compatible trapped source, prove that the "
            "six-term row is visible on the protected full-q kernel or that "
            "its factorization through [A;H] has nonzero H coefficient.  "
            "Equivalently exclude Lambda in row(A) while H is nonzero in "
            "X^*/row(A), or construct H as a physical source row"
        ),
        "why_not_Hall": (
            "all alternatives are row/kernel statements on the explicit "
            "common-q coefficient Jacobian; no endpoint-hole closure or "
            "finite Hall concept is used"
        ),
        "scope": (
            "universal coefficient-level q-Jacobian and exact structural "
            "Fredholm alternative.  It does not prove the final nonzero-mu "
            "physical comparison at every unknown trapped source and does "
            "not identify an occurrence marker with Lambda"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("full-q six-term ledger changed", digest))
    print("h3 trapped carrier full-q six-term extension: PASS")
    print("physical columns: endpoint 36 + q 135 = 171")
    print("q derivatives: unary 10935 entries; responses 43740 entries")
    print("outcomes: exchange / physical dual / six-term generator / transport")
    print("sharp survivor: Lambda in row(A), H nonzero modulo row(A)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
