#!/usr/bin/env python3
"""Exact smallest middle-word enlargement of the h=3 H2 cokernel.

The response cubic T=Q3 and the literal binary midpoint coordinates are
kept separate.  The checker proves that adjoining every midpoint row leaves
one terminal cokernel and identifies the primitive missing attaching row.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json


EXPECTED_DIGEST = "634149cd4f887e29d5ca1a6ad20551e2c264e54f11c8a5b5cc6217e61279c5cb"
SITES = tuple(range(6))
LABELS = tuple(range(3))
SELECTED = (0, 1)
MIDDLE_SUBSETS = tuple(combinations(SITES, 3))
MIDDLE_WORDS = tuple(
    tuple(1 if site in subset else 0 for site in SITES)
    for subset in MIDDLE_SUBSETS
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(rows):
    work = [list(map(F, row)) for row in rows]
    if not work:
        return 0
    answer = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(answer, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right
                         for left, right in zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def determinant(rows):
    work = [list(map(F, row)) for row in rows]
    require(all(len(row) == len(work) for row in work), "determinant is not square")
    answer = F(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            scale = work[row][column] / value
            work[row] = [left - scale * right
                         for left, right in zip(work[row], work[column], strict=True)]
    return answer


def dot(left, right):
    return sum((F(x) * F(y) for x, y in zip(left, right, strict=True)), F(0))


def endpoint_degree(pairs):
    left = [0, 0, 0]
    right = [0, 0, 0]
    for row, column in pairs:
        left[row] += 1
        right[column] += 1
    return tuple(left), tuple(right)


def direct_sum(left, right):
    left_width = len(left[0])
    right_width = len(right[0])
    return (
        [list(row) + [F(0)] * right_width for row in left]
        + [[F(0)] * left_width + list(row) for row in right]
    )


def main():
    require(len(MIDDLE_WORDS) == 20 and len(set(MIDDLE_WORDS)) == 20,
            "binary midpoint basis changed")
    require(all(word.count(0) == word.count(1) == 3 and word.count(2) == 0
                for word in MIDDLE_WORDS),
            "a binary midpoint word left count type (3,3,0)")
    require(all(min(sum(value != colour for value in word) for colour in LABELS) == 3
                for word in MIDDLE_WORDS),
            "a midpoint word entered the Hamming-two ball")

    # At response grade three a starting full-nine row plus three endpoint
    # tags reaches 4(e_0^L,e_1^R) only through four selected label pairs.
    selected_degree_four = endpoint_degree((SELECTED,) * 4)
    routes = []
    for labels in product(LABELS, repeat=8):
        pairs = tuple(zip(labels[::2], labels[1::2], strict=True))
        if endpoint_degree(pairs) == selected_degree_four:
            routes.append(pairs)
    require(routes == [(SELECTED,) * 4],
            ("response-grade-three acquired another label route", routes))

    # The static block is copied literally from commit 87304b5.
    static = [
        [F(1), F(0), F(1), F(0)],
        [F(0), F(0), F(1), F(1)],
        [F(0), F(0), F(1), F(-2)],
        [F(0), F(1), F(2), F(0)],
    ]
    require(determinant(static) == -3, "two-chart static determinant moved")

    records = []
    for alpha in (F(1), F(2), F(-3, 2)):
        # Coordinates are Q0,Q1,Q2,T=Q3, followed by the 20 literal
        # midpoint coordinates m_S in lexicographic three-subset order.
        width = 4 + len(MIDDLE_WORDS)
        e0 = [alpha, F(1), F(0), F(0)] + [F(0)] * len(MIDDLE_WORDS)
        e1 = [F(0), alpha, F(2), F(0)] + [F(0)] * len(MIDDLE_WORDS)
        e2 = [F(0), F(0), alpha, F(3)] + [F(0)] * len(MIDDLE_WORDS)
        middle_rows = []
        for index in range(len(MIDDLE_WORDS)):
            row = [F(0)] * width
            row[4 + index] = F(1)
            middle_rows.append(row)
        honest = [e0, e1, e2] + middle_rows
        require(rank(honest) == width - 1,
                ("honest middle enlargement lost its one-dimensional cokernel", alpha))

        terminal = [F(-6), 6 * alpha, -3 * alpha**2, alpha**3] + [F(0)] * len(MIDDLE_WORDS)
        require(all(dot(row, terminal) == 0 for row in honest),
                ("terminal stopped killing honest rows", alpha))
        q3_target = [F(0), F(0), F(0), F(1)] + [F(0)] * len(MIDDLE_WORDS)
        chi4_target = [F(0), F(0), 4 * alpha, F(4)] + [F(0)] * len(MIDDLE_WORDS)
        require(dot(q3_target, terminal) == alpha**3,
                "Q3 target stopped detecting the cokernel")
        require(dot(chi4_target, terminal) == -8 * alpha**3,
                "4chi target stopped detecting the cokernel")

        # The primitive missing source relation.  If m_S denotes the
        # literal middle coefficient, the twenty-cut normalization gives
        # 8chi.  Modulo e2, its source-faithful landing is precisely
        # A = 16*T + sum_S m_S.  Equivalently, with
        # M=-(1/16)sum m_S, this is 16(T-M).
        attaching = [F(0), F(0), F(0), F(16)] + [F(1)] * len(MIDDLE_WORDS)
        require(dot(attaching, terminal) == 16 * alpha**3,
                "attaching row stopped detecting the terminal line")
        require(rank(honest + [attaching]) == width,
                "attaching row did not close the dynamic module")

        # Exact integral identity: 8chi = 8e2 - A + sum_S m_S.
        middle_sum = [sum((row[column] for row in middle_rows), F(0))
                      for column in range(width)]
        identity = [8 * e2[column] - attaching[column] + middle_sum[column]
                    for column in range(width)]
        chi8_target = [F(0), F(0), 8 * alpha, F(8)] + [F(0)] * len(MIDDLE_WORDS)
        require(identity == chi8_target, "integral 8chi identity moved")

        combined_honest = direct_sum(static, honest)
        combined_closed = direct_sum(static, honest + [attaching])
        require(rank(combined_honest) == 4 + width - 1,
                "static block changed the attaching cokernel")
        require(rank(combined_closed) == 4 + width,
                "static block prevented attaching closure")

        # Collapse the twenty literal middle coordinates to their normalized
        # aggregate M.  The smallest quotient has coordinates Q0,Q1,Q2,T,M.
        collapsed = [
            [alpha, F(1), F(0), F(0), F(0)],
            [F(0), alpha, F(2), F(0), F(0)],
            [F(0), F(0), alpha, F(3), F(0)],
            [F(0), F(0), F(0), F(0), F(1)],
        ]
        collapsed_attach = [F(0), F(0), F(0), F(1), F(-1)]
        require(rank(collapsed) == 4 and rank(collapsed + [collapsed_attach]) == 5,
                "collapsed T-M obstruction moved")
        records.append({
            "alpha": str(alpha),
            "honest_dynamic_rank": rank(honest),
            "honest_dynamic_cokernel": width - rank(honest),
            "q3_separator_value": str(dot(q3_target, terminal)),
            "four_chi_separator_value": str(dot(chi4_target, terminal)),
            "attaching_separator_value": str(dot(attaching, terminal)),
            "combined_honest_rank": rank(combined_honest),
            "combined_closed_rank": rank(combined_closed),
        })

    # At alpha=1 the full 24-dimensional dynamic attaching determinant is
    # primitive up to the canonical factor 16.
    alpha = F(1)
    dynamic_square = [
        [alpha, F(1), F(0), F(0)] + [F(0)] * 20,
        [F(0), alpha, F(2), F(0)] + [F(0)] * 20,
        [F(0), F(0), alpha, F(3)] + [F(0)] * 20,
    ]
    for index in range(20):
        row = [F(0)] * 24
        row[4 + index] = F(1)
        dynamic_square.append(row)
    dynamic_square.append([F(0), F(0), F(0), F(16)] + [F(1)] * 20)
    require(determinant(dynamic_square) == 16,
            "normalized attaching determinant moved")

    ledger = {
        "scope": "selected endpoint fine degree; literal binary midpoint rows",
        "selected_labels": list(SELECTED),
        "response_grade_three_routes": len(routes),
        "literal_middle_basis": ["".join(map(str, word)) for word in MIDDLE_WORDS],
        "literal_middle_dimension": len(MIDDLE_WORDS),
        "static_determinant": str(determinant(static)),
        "records": records,
        "normalized_dynamic_attaching_determinant": str(determinant(dynamic_square)),
        "missing_relation": "16*T+sum(m_S), equivalently T-M",
        "integral_target_identity": "8*chi=8*e2-A+sum(m_S)",
        "verdict": "middle_rows_leave_one_attaching_cokernel",
    }
    digest = sha256(json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, ("ledger changed", digest, ledger))
    print("h=3 H2 plus middle-word attaching obstruction: PASS")
    print("literal binary midpoint rows: 20")
    print("honest dynamic cokernel: 1")
    print("missing primitive row: 16*T+sum(m_S), equivalently T-M")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
