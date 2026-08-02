#!/usr/bin/env python3
"""Exact h=3 audit of the augmented second-jet polar criterion.

The first half independently reconstructs the five mixed second polars in
the direct-free eight-site chart.  The second half checks the smallest
target/ordinary-residue augmented module in which those polar symbols could
be lifted after the connection/normal/curvature contraction.
"""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json


Q = Fraction
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
X = 0
P = 6
Q_SITE = 7
R = 3
MIXED = (1, 2, 1, 1, 2)
DIRECT_FREE = frozenset((P, R))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(u, v, a, b):
    return (u, v, a, b) if u < v else (v, u, b, a)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def monomial(matching, word):
    return tuple(sorted(edge(u, v, word[u], word[v]) for u, v in matching))


def full_row(word):
    answer = []
    for matching in matchings(SITES):
        if any(frozenset(pair) == DIRECT_FREE for pair in matching):
            continue
        answer.append(monomial(matching, word))
    require(len(answer) == 90 and len(set(answer)) == 90, "full row")
    return tuple(answer)


def derivative(polynomial, variables):
    answer = {}
    for term in polynomial:
        remainder = list(term)
        for variable in variables:
            if variable not in remainder:
                break
            remainder.remove(variable)
        else:
            remainder = tuple(sorted(remainder))
            answer[remainder] = answer.get(remainder, 0) + 1
    return answer


def face_hafnian(deleted):
    face = tuple(site for site in ODD if site != deleted)
    colors = {site: MIXED[site - 1] for site in face}
    return {
        tuple(sorted(edge(u, v, colors[u], colors[v]) for u, v in matching)): 1
        for matching in matchings(face)
    }


def chart_sector(polynomial, pair):
    pair = frozenset(pair)
    direct, stars = [], []
    for term in polynomial:
        selected = any(frozenset((u, v)) == pair for u, v, _a, _b in term)
        (direct if selected else stars).append(term)
    return tuple(direct), tuple(stars)


def polar_ledger():
    records = []
    supports = []
    for deleted in ODD:
        word = [0] * 8
        for site in ODD:
            if site != deleted:
                word[site] = MIXED[site - 1]
        word = tuple(word)
        row = full_row(word)
        variables = (edge(X, deleted, 0, 0), edge(P, Q_SITE, 0, 0))
        polar = derivative(row, variables)
        expected = face_hafnian(deleted)
        require(polar == expected, f"face {deleted}: second polar")

        pq_direct, pq_stars = chart_sector(row, (P, Q_SITE))
        pr_direct, pr_stars = chart_sector(row, (P, R))
        require(derivative(pq_direct, variables) == expected,
                f"face {deleted}: pq direct polar")
        require(not derivative(pq_stars, variables),
                f"face {deleted}: pq star polar")
        require(not derivative(pr_direct, variables),
                f"face {deleted}: pr direct polar")
        require(derivative(pr_stars, variables) == expected,
                f"face {deleted}: pr star polar")

        supports.append(set(polar))
        records.append({
            "deleted": deleted,
            "global_word": "".join(map(str, word)),
            "face_word": "".join(str(MIXED[site - 1])
                                   for site in ODD if site != deleted),
            "polar_terms": len(polar),
            "pq_sector": "direct",
            "pr_sector": "two_star",
        })
    require(all(supports[i].isdisjoint(supports[j])
                for i in range(5) for j in range(i + 1, 5)),
            "face polar supports are not independent")
    return records


def rank(columns):
    if not columns:
        return 0
    rows = len(columns[0])
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(rows)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def in_span(vector, columns):
    return rank(columns + [vector]) == rank(columns)


def direct_sum_columns(block_columns, copies):
    block_rows = len(block_columns[0])
    answer = []
    for copy in range(copies):
        for column in block_columns:
            extended = [Q(0)] * (block_rows * copies)
            extended[copy * block_rows:(copy + 1) * block_rows] = column
            answer.append(extended)
    return answer


def module_packet(A, B, F, U, Y):
    A, B, F, U, Y = map(Q, (A, B, F, U, Y))
    kappa = A * U - B * F
    require(kappa and Y, "active packet")

    # Exact selected connection/normal/curvature contraction.
    c1, c2 = (A, F), (B, U)
    lam, eta = (-F, A), (U, -B)
    dot = lambda left, right: sum((left[i] * right[i] for i in range(2)), Q(0))
    require(dot(lam, c1) == dot(eta, c2) == 0, "adjugate kernels")
    require(dot(lam, c2) == dot(eta, c1) == kappa, "curvature contraction")

    # Coordinates are (selected cap boundary w, physical target, ordinary
    # residue).  T and rho are the complete existing split-cap columns.
    target_column = [-Y, Q(1), Q(0)]
    residue_column = [Q(1), Q(0), Q(1)]
    existing = [target_column, residue_column]
    polar_column = [kappa * Y, Q(0), Q(0)]

    boundary_only = [[column[0]] for column in existing]
    target_augmented = [column[:2] for column in existing]
    require(in_span([polar_column[0]], boundary_only),
            "unaugmented Hessian membership failed")
    require(in_span(polar_column[:2], target_augmented),
            "target-invisible membership failed")
    require(not in_span(polar_column, existing),
            "ordinary-residue augmented membership unexpectedly held")
    require(rank(existing) == 2 and rank(existing + [polar_column]) == 3,
            "single-face augmented rank jump")

    # The actual overlap response is the cap graph.  It is a cycle but is
    # killed by the equal and opposite common anchor; it supplies no new
    # augmented correction column.
    graph_coefficients = [Q(1), Y]
    graph_image = [
        graph_coefficients[0] * target_column[row]
        + graph_coefficients[1] * residue_column[row]
        for row in range(3)
    ]
    require(graph_image == [Q(0), Q(1), Y], "cap graph")
    overlap_image = [-kappa * entry for entry in graph_image]
    anchor_image = [kappa * entry for entry in graph_image]
    require([overlap_image[i] + anchor_image[i] for i in range(3)]
            == [Q(0)] * 3, "common anchor did not kill overlap graph")

    # Keeping only the target-zero residue chain hits the boundary but has
    # the forbidden ordinary residue.  A new invisible n-column is exactly
    # what promotes it to a cycle with the wanted associated response.
    relative_response = [-kappa * Y * residue_column[row] for row in range(3)]
    require(relative_response == [-kappa * Y, Q(0), -kappa * Y],
            "relative response")
    hypothetical_n = polar_column
    promoted_cycle = [hypothetical_n[i] + relative_response[i] for i in range(3)]
    require(promoted_cycle == [Q(0), Q(0), -kappa * Y], "promoted cycle")

    # The five disjoint face rows give five independent copies of the same
    # obstruction: adding the five polar columns raises rank by exactly five.
    existing_five = direct_sum_columns(existing, 5)
    polar_five = direct_sum_columns([polar_column], 5)
    require(rank(existing_five) == 10, "five-face existing rank")
    require(rank(existing_five + polar_five) == 15,
            "five polar obstructions are not independent")

    return {
        "A": str(A), "B": str(B), "F": str(F), "U": str(U),
        "Y": str(Y), "kappa": str(kappa), "direct_free": B == 0,
        "boundary_membership": True,
        "target_augmented_membership": True,
        "target_residue_augmented_membership": False,
        "single_face_ranks": [rank(existing), rank(existing + [polar_column])],
        "five_face_ranks": [rank(existing_five),
                            rank(existing_five + polar_five)],
        "overlap_graph": [str(value) for value in overlap_image],
        "relative_response_defect": str(relative_response[0]),
    }


def main():
    polars = polar_ledger()
    samples = (
        (Q(2), Q(3), Q(5), Q(11), Q(7, 5)),
        (Q(3), Q(0), Q(2), Q(5), Q(-4, 9)),
        (Q(-2), Q(7), Q(3), Q(-5), Q(13, 6)),
        (Q(5, 3), Q(-7, 4), Q(11, 5), Q(2, 9), Q(-8, 7)),
    )
    packets = [module_packet(*sample) for sample in samples]
    ledger = {"polars": polars, "packets": packets}
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == "b9c1d442dac415ebde2fca5d97922fbda7060657c0bcd1d907c584a466fa136e",
            f"ledger digest changed: {digest}")

    print("h=3 augmented second-jet polar membership: PASS")
    print("five exact two-edge polars: pq-direct / pr-two-star")
    print("boundary and target-only memberships hold; ordinary-residue augmentation fails")
    print("five-face augmented rank jump: 10 -> 15")
    print("a new invisible n_v column is necessary and sufficient facewise")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
