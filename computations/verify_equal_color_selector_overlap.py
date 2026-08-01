#!/usr/bin/env python3
"""Exact combinatorial audit of the selector overlap formulas (8b)--(8j)."""

from itertools import permutations, product


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


P, Q, S, T = 0, 1, 2, 3
W = (4, 5, 6, 7)
C = (P, Q, S)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def matrices():
    out = {}
    for u in range(8):
        for v in range(u + 1, 8):
            out[u, v] = tuple(tuple(
                ((u + 2) * (i + 1) + (v + 3) * (j + 2) + 2 * i * j + 1) % 7 - 3
                for j in range(3)) for i in range(3))
    return out


A = matrices()
THETA = {(i, j, k): ((2 * i + 3 * j + 5 * k + i * j + 1) % 7 - 3)
         for i, j, k in product(range(3), repeat=3)}
R_COLOR = 1


def edge_value(u, v, cu, cv):
    if u < v:
        return A[u, v][cu][cv]
    return A[v, u][cv][cu]


def h_value(vertices, coloring):
    total = 0
    for matching in perfect_matchings(vertices):
        value = 1
        for u, v in matching:
            value *= edge_value(u, v, coloring[u], coloring[v])
        total += value
    return total


def p_value(sites, coloring):
    """The capped three-cross permanent P_s(sites)."""
    sites = tuple(sites)
    total = 0
    for cword in product(range(3), repeat=3):
        theta = THETA[cword]
        for image in permutations(sites):
            value = theta
            for index, vertex in enumerate(C):
                value *= edge_value(vertex, image[index], cword[index], coloring[image[index]])
            total += value
    return total


def l_value(u, color_u):
    total = 0
    for cp, cq, cs in product(range(3), repeat=3):
        theta = THETA[cp, cq, cs]
        total += theta * (
            edge_value(P, Q, cp, cq) * edge_value(S, u, cs, color_u)
            + edge_value(P, S, cp, cs) * edge_value(Q, u, cq, color_u)
            + edge_value(Q, S, cq, cs) * edge_value(P, u, cp, color_u)
        )
    return total


def direct_sector(crossing_number, w_word):
    coloring = {vertex: color for vertex, color in zip(W, w_word)}
    coloring[T] = R_COLOR
    total = 0
    for cword in product(range(3), repeat=3):
        for vertex, color in zip(C, cword):
            coloring[vertex] = color
        theta = THETA[cword]
        for matching in perfect_matchings(range(8)):
            crossing = sum((u in C) != (v in C) for u, v in matching)
            if crossing != crossing_number:
                continue
            value = theta
            for u, v in matching:
                value *= edge_value(u, v, coloring[u], coloring[v])
            total += value
    return total


def formula_three(w_word):
    coloring = {vertex: color for vertex, color in zip(W, w_word)}
    coloring[T] = R_COLOR
    total = 0
    # t is a cross partner; {a,b} are the other two cross partners and the
    # complementary W-pair is the residual internal edge.
    for a_index in range(len(W)):
        for b_index in range(a_index + 1, len(W)):
            a, b = W[a_index], W[b_index]
            complement = tuple(w for w in W if w not in (a, b))
            total += p_value((T, a, b), coloring) * h_value(complement, coloring)
    # t lies on the residual internal edge tw.
    for w in W:
        d_tw = edge_value(T, w, R_COLOR, coloring[w])
        total += d_tw * p_value(tuple(a for a in W if a != w), coloring)
    return total


def formula_one(w_word):
    coloring = {vertex: color for vertex, color in zip(W, w_word)}
    coloring[T] = R_COLOR
    lam = l_value(T, R_COLOR)
    total = lam * h_value(W, coloring)
    for a_index in range(len(W)):
        for b_index in range(a_index + 1, len(W)):
            a, b = W[a_index], W[b_index]
            d_ta = edge_value(T, a, R_COLOR, coloring[a])
            d_tb = edge_value(T, b, R_COLOR, coloring[b])
            z_ab = l_value(a, coloring[a]) * d_tb + d_ta * l_value(b, coloring[b])
            complement = tuple(w for w in W if w not in (a, b))
            total += z_ab * h_value(complement, coloring)
    return total


def main():
    for w_word in product(range(3), repeat=4):
        require(
            direct_sector(3, w_word) == formula_three(w_word),
            "direct_sector(3, w_word) == formula_three(w_word)",
        )
        require(
            direct_sector(1, w_word) == formula_one(w_word),
            "direct_sector(1, w_word) == formula_one(w_word)",
        )
    # Audit the unavoidable augmented vertex-gauge kernel (8n).
    gauges = {4: 2, 5: -3, 6: 5, 7: 1}
    lam = -sum(gauges.values())
    for w_word in product(range(3), repeat=4):
        coloring = {vertex: color for vertex, color in zip(W, w_word)}
        value = lam * h_value(W, coloring)
        for a_index in range(len(W)):
            for b_index in range(a_index + 1, len(W)):
                a, b = W[a_index], W[b_index]
                z_ab = ((gauges[a] + gauges[b])
                        * edge_value(a, b, coloring[a], coloring[b]))
                complement = tuple(w for w in W if w not in (a, b))
                value += z_ab * h_value(complement, coloring)
        require(
            value == 0,
            "value == 0",
        )
    print("PASS: equal-color selector crossing-sector decompositions audited")


if __name__ == "__main__":
    main()
