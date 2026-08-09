#!/usr/bin/env python3
"""Exact structural counterguard to the flat-wedge selector shortcut."""

from fractions import Fraction as F


SITES = ("p", "q", "r", "u", "v", "w", "x", "y")
ORDER = {site: index for index, site in enumerate(SITES)}
COLORS = range(3)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def canonical_cell(a, b, i, j):
    if ORDER[a] < ORDER[b]:
        return a, b, i, j
    return b, a, j, i


def add_cell(blocks, a, b, i, j, value=1):
    key = canonical_cell(a, b, i, j)
    blocks[key] = blocks.get(key, F(0)) + F(value)


def entry(blocks, a, b, i, j):
    return blocks.get(canonical_cell(a, b, i, j), F(0))


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


def direct_matrix(blocks, a, b):
    return [[entry(blocks, a, b, i, j) for j in COLORS] for i in COLORS]


def star_rank(blocks, endpoint, deleted_neighbor):
    residual = [site for site in SITES if site not in (endpoint, deleted_neighbor)]
    columns = [(site, colour) for site in residual for colour in COLORS]
    rows = [
        [entry(blocks, endpoint, site, row, colour) for site, colour in columns]
        for row in COLORS
    ]
    return rational_rank(rows)


def local_star_map(blocks, endpoint, site):
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
    j = [[F(0) for _ in COLORS] for _ in COLORS]
    other = [colour for colour in COLORS if colour != target]
    i, k = other
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
    # Independent shared-p factors and distinct outgoing coordinate heads.
    add_cell(blocks, "p", "q", 0, 0)
    add_cell(blocks, "p", "r", 1, 1)

    # The opposite chord is invertible.
    for colour in COLORS:
        add_cell(blocks, "q", "r", colour, colour)

    # These two p-arms make the p-star injective after deleting either q or r.
    add_cell(blocks, "p", "u", 2, 0)
    add_cell(blocks, "p", "v", 0, 0)
    add_cell(blocks, "p", "v", 1, 0)
    return blocks


def main():
    blocks = build_packet()
    ranks = (
        star_rank(blocks, "p", "q"),
        star_rank(blocks, "q", "p"),
        star_rank(blocks, "p", "r"),
        star_rank(blocks, "r", "p"),
    )
    require(ranks == (3, 3, 3, 3), "good-arm star ranks changed")
    require(rational_rank(direct_matrix(blocks, "p", "q")) == 1, "pq rank changed")
    require(rational_rank(direct_matrix(blocks, "p", "r")) == 1, "pr rank changed")
    require(rational_rank(direct_matrix(blocks, "q", "r")) == 3, "qr chord rank changed")

    # On K_{qr}=B\{p,q,r}, both q and r have zero restricted stars, so all
    # canonical transitions between the two arms vanish exactly.
    common = [site for site in SITES if site not in ("p", "q", "r")]
    require(
        all(
            local_star_map(blocks, endpoint, site)
            == [[F(0) for _ in COLORS] for _ in COLORS]
            for endpoint in ("q", "r") for site in common
        ),
        "flat restricted stars changed",
    )

    # In the qr chart d=I.  Since every N_{x,e} has rank <=2,
    # N_{x,e} lies in C*d exactly when it is zero.
    t_sets = {}
    residual = [site for site in SITES if site not in ("q", "r")]
    for target in COLORS:
        aligned = []
        for site in residual:
            matrix = wedge_matrix(blocks, ("q", "r"), site, target)
            if not any(any(row) for row in matrix):
                aligned.append(site)
        t_sets[target] = tuple(aligned)
    require(
        {target: len(sites) for target, sites in t_sets.items()} == {0: 6, 1: 6, 2: 5},
        "rank-three selector T-set census changed",
    )
    require("p" not in t_sets[2], "shared-centre target-2 wedge vanished")

    print("flat good-wedge rank-three selector counterguard: PASS")
    print(f"good-arm star ranks={ranks}; opposite chord rank=3")
    print("restricted q/r stars on K_qr vanish, so the arm transition is flat")
    print("rank-three chord alignment sizes:", {e: len(t_sets[e]) for e in COLORS})


if __name__ == "__main__":
    main()
