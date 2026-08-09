#!/usr/bin/env python3
"""Exact doubly-good curved-OO counterguard to the one-anchor atom."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product


SITES = ("p", "q", "r", "a", "b", "c", "d", "s")
ORDER = {site: index for index, site in enumerate(SITES)}
COLORS = range(3)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def canonical_cell(u, v, i, j):
    if ORDER[u] < ORDER[v]:
        return u, v, i, j
    return v, u, j, i


def add_cell(blocks, u, v, i, j, value=1):
    key = canonical_cell(u, v, i, j)
    blocks[key] = blocks.get(key, F(0)) + F(value)
    if not blocks[key]:
        del blocks[key]


def entry(blocks, u, v, i, j):
    return blocks.get(canonical_cell(u, v, i, j), F(0))


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def matching_tensor(blocks):
    answer = defaultdict(F)
    vertices = tuple(SITES)
    for matching in perfect_matchings(vertices):
        choices = []
        for u, v in matching:
            cells = [
                (i, j, value)
                for i in COLORS
                for j in COLORS
                if (value := entry(blocks, u, v, i, j))
            ]
            if not cells:
                choices = []
                break
            choices.append(cells)
        for selected in product(*choices) if choices else ():
            word = [None] * len(SITES)
            coefficient = F(1)
            for (u, v), (i, j, value) in zip(matching, selected, strict=True):
                word[ORDER[u]] = i
                word[ORDER[v]] = j
                coefficient *= value
            answer[tuple(word)] += coefficient
    return {word: value for word, value in answer.items() if value}


def supported_cofactor_matchings(blocks, deleted_pair):
    residual = tuple(site for site in SITES if site not in deleted_pair)
    return tuple(
        matching
        for matching in perfect_matchings(residual)
        if all(
            any(entry(blocks, u, v, i, j) for i in COLORS for j in COLORS)
            for u, v in matching
        )
    )


def rational_rank(rows):
    matrix = [[F(value) for value in row] for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot
                for value, pivot in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
    return rank


def direct_matrix(blocks, u, v):
    return [[entry(blocks, u, v, i, j) for j in COLORS] for i in COLORS]


def star_rank(blocks, endpoint, deleted_neighbor):
    residual = [site for site in SITES if site not in (endpoint, deleted_neighbor)]
    columns = [(site, colour) for site in residual for colour in COLORS]
    rows = [
        [entry(blocks, endpoint, site, row, colour) for site, colour in columns]
        for row in COLORS
    ]
    return rational_rank(rows)


def local_star_map(blocks, endpoint, site):
    # Physical-colour rows, endpoint-row columns.
    return [
        [entry(blocks, endpoint, site, endpoint_colour, physical_colour)
         for endpoint_colour in COLORS]
        for physical_colour in COLORS
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix, strict=True)]


def matmul(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def wedge_matrix(blocks, endpoints, site, target):
    first = local_star_map(blocks, endpoints[0], site)
    second = local_star_map(blocks, endpoints[1], site)
    # u^T J_target v = det(u,v,e_target).
    j = [[F(0) for _ in COLORS] for _ in COLORS]
    other = [colour for colour in COLORS if colour != target]
    i, k = other
    # The sign is irrelevant for the ruling audit, but retain orientation.
    permutation = (i, k, target)
    inversions = sum(
        permutation[a] > permutation[b]
        for a in range(3) for b in range(a + 1, 3)
    )
    sign = -1 if inversions % 2 else 1
    j[i][k] = F(sign)
    j[k][i] = F(-sign)
    return matmul(matmul(transpose(first), j), second)


def build_packet():
    blocks = {}
    # Distinct-head OO direct arms.
    add_cell(blocks, "p", "q", 0, 0)
    add_cell(blocks, "p", "r", 0, 1)

    # Remaining p-star rows in the pq chart:
    #   P0=e1^r+e0^d, P1=e1^c, P2=e2^a.
    add_cell(blocks, "p", "d", 0, 0)
    add_cell(blocks, "p", "c", 1, 1)
    add_cell(blocks, "p", "a", 2, 2)

    # Remaining q-star rows:
    #   S0=e0^r+e0^c, S1=e1^r, S2=e2^b.
    add_cell(blocks, "q", "r", 0, 0)
    add_cell(blocks, "q", "c", 0, 0)
    add_cell(blocks, "q", "r", 1, 1)
    add_cell(blocks, "q", "b", 2, 2)

    # The two internal colour-2 edges in the pq chart.
    add_cell(blocks, "r", "c", 2, 2)
    add_cell(blocks, "d", "s", 2, 2)
    return blocks


def audit_ruling(blocks, endpoints, head):
    residual = [site for site in SITES if site not in endpoints]
    nonzero_sites = []
    for site in residual:
        matrix = wedge_matrix(blocks, endpoints, site, 2)
        for row in COLORS:
            for column in COLORS:
                if column != head:
                    require(
                        matrix[row][column] == 0,
                        f"target-2 RR alignment failed at {endpoints}, {site}",
                    )
        if any(matrix[row][head] for row in COLORS):
            nonzero_sites.append(site)
    return tuple(nonzero_sites)


def main():
    blocks = build_packet()
    tensor = matching_tensor(blocks)
    x2 = (2,) * len(SITES)
    require(tensor == {x2: F(1)}, "guard matching tensor is no longer exactly X2")

    pq = direct_matrix(blocks, "p", "q")
    pr = direct_matrix(blocks, "p", "r")
    require(rational_rank(pq) == rational_rank(pr) == 1, "direct arm rank changed")
    require(
        {column for row in COLORS for column in COLORS if pq[row][column]} == {0},
        "pq head changed",
    )
    require(
        {column for row in COLORS for column in COLORS if pr[row][column]} == {1},
        "pr head changed",
    )

    ranks = (
        star_rank(blocks, "p", "q"),
        star_rank(blocks, "q", "p"),
        star_rank(blocks, "p", "r"),
        star_rank(blocks, "r", "p"),
    )
    require(ranks == (3, 3, 3, 3), "doubly-good star ranks changed")

    curvature = (
        entry(blocks, "p", "q", 0, 0) * entry(blocks, "r", "c", 1, 0)
        - entry(blocks, "p", "r", 0, 1) * entry(blocks, "q", "c", 0, 0)
    )
    require(curvature == -1, "curvature minor changed")

    activity = {
        "pq": supported_cofactor_matchings(blocks, ("p", "q")),
        "pr": supported_cofactor_matchings(blocks, ("p", "r")),
    }
    require(activity == {"pq": (), "pr": ()}, "inactive-arm cofactor ledger changed")

    pq_nonzero = audit_ruling(blocks, ("p", "q"), 0)
    pr_nonzero = audit_ruling(blocks, ("p", "r"), 1)
    require(pq_nonzero == ("r", "c"), "pq aligned-site support changed")
    require(pr_nonzero == ("q",), "pr aligned-site support changed")

    # Because the complete global tensor is X2, the 22 slice is X2 and
    # every off-diagonal slice vanishes in both pair presentations.
    residual_pq = tuple(site for site in SITES if site not in ("p", "q"))
    residual_pr = tuple(site for site in SITES if site not in ("p", "r"))
    slice_pq_22 = {
        tuple(word[ORDER[site]] for site in residual_pq): value
        for word, value in tensor.items() if word[ORDER["p"]] == word[ORDER["q"]] == 2
    }
    slice_pr_22 = {
        tuple(word[ORDER[site]] for site in residual_pr): value
        for word, value in tensor.items() if word[ORDER["p"]] == word[ORDER["r"]] == 2
    }
    require(slice_pq_22 == {(2,) * 6: F(1)}, "pq 22 anchor changed")
    require(slice_pr_22 == {(2,) * 6: F(1)}, "pr 22 anchor changed")
    require(
        not any(word[ORDER["p"]] == 2 and word[ORDER["q"]] == 1 for word in tensor),
        "pq 21 row became nonzero",
    )
    require(
        not any(word[ORDER["p"]] == 2 and word[ORDER["r"]] == 0 for word in tensor),
        "pr 20 row became nonzero",
    )

    # The proposed transport ratio O = kappa*D fails as 0 != -1.
    require(F(0) - curvature * F(1) == 1, "transport-ratio countervalue changed")

    print("doubly-good curved OO one-anchor counterguard: PASS")
    print(f"matching tensor=X2; star ranks={ranks}; curvature={curvature}")
    print("both selected-arm cofactor tensors vanish (no supported residual matching)")
    print(f"target-2 RR nonzero sites: pq={pq_nonzero}, pr={pr_nonzero}")
    print("22 anchors hold in both charts; pq-21 and pr-20 rows vanish")
    print("candidate transport O=kappa*D fails: 0 != -1")


if __name__ == "__main__":
    main()
