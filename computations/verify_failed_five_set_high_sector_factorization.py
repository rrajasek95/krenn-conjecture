#!/usr/bin/env python3
"""Exact audits for ``failed-five-set-high-sector-factorization.md``.

The first audit constructs, for |C|=7,9,11, a five-shore contraction with
q_U=0, beta in ker(F_1), all three entries of delta(beta) nonzero, and

    q_C^k/k! * p_5 = Delta_C(b),       k=(|C|-5)/2.

It also checks that the rank-three block graph of q_C is connected and
nonbipartite.  The second audit gives an integer seven-site q for which
multiplication R_5 -> R_7 has full row rank, certified modulo two.
"""

from __future__ import annotations

import itertools
from collections import defaultdict
from fractions import Fraction as F


COLORS = range(3)
BETA_VALUES = (F(2), F(-3), F(5))


def monomial(n, entries):
    """A site-square-free monomial; -1 denotes an unoccupied site."""
    word = [-1] * n
    for site, color in entries.items():
        assert word[site] == -1
        word[site] = color
    return tuple(word)


def product(left, right):
    """Multiply sparse polynomials in the site-square-zero algebra."""
    out = defaultdict(F)
    for u, a in left.items():
        for v, b in right.items():
            if any(x != -1 and y != -1 for x, y in zip(u, v)):
                continue
            w = tuple(y if x == -1 else x for x, y in zip(u, v))
            out[w] += a * b
    return {w: a for w, a in out.items() if a}


def matching_power(terms, power):
    """Return q^power/power! from the monomial terms of q."""
    if power == 0:
        n = len(terms[0][0]) if terms else 0
        return {(-1,) * n: F(1)}
    out = defaultdict(F)
    for chosen in itertools.combinations(terms, power):
        word = [-1] * len(chosen[0][0])
        value = F(1)
        good = True
        for term, coeff in chosen:
            for site, color in enumerate(term):
                if color == -1:
                    continue
                if word[site] != -1:
                    good = False
                    break
                word[site] = color
            if not good:
                break
            value *= coeff
        if good:
            out[tuple(word)] += value
    return {w: a for w, a in out.items() if a}


def graph_is_connected(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        v = stack.pop()
        for w in adjacency[v] - seen:
            seen.add(w)
            stack.append(w)
    return len(seen) == len(vertices)


def routing_instance(k):
    """Construct q_C, q_X, beta, and p_5 for one routing example."""
    assert 1 <= k <= 5
    n = 2 * k + 5
    A = tuple(range(0, k))
    D = tuple(range(k, 2 * k))
    Ep = tuple(range(2 * k, 3 * k))
    E = tuple(range(3 * k, n))
    assert len(E) == 5 - k

    matchings = (
        tuple(zip(A, D)),
        tuple(zip(A, Ep)),
        tuple(zip(D, Ep)),
    )
    residuals = (Ep + E, D + E, A + E)
    assert all(len(z) == 5 for z in residuals)

    q0_terms = []
    q_blocks = defaultdict(lambda: [[F(0) for _ in COLORS] for _ in COLORS])
    for color, matching in enumerate(matchings):
        for i, j in matching:
            edge = (min(i, j), max(i, j))
            q_blocks[edge][color][color] += 1
            q0_terms.append((monomial(n, {i: color, j: color}), F(1)))

    # Every added block meets the common occupied set E and hence annihilates
    # every monomial of p_5.  Identity blocks make the rank-three graph the
    # split graph with clique E joined to all remaining vertices.
    h_terms = []
    h_edges = []
    for i, j in itertools.combinations(range(n), 2):
        if i not in E and j not in E:
            continue
        h_edges.append((i, j))
        for color in COLORS:
            q_blocks[i, j][color][color] += 1
            h_terms.append((monomial(n, {i: color, j: color}), F(1)))

    p5 = {}
    for color, (z, value) in enumerate(zip(residuals, BETA_VALUES)):
        p5[monomial(n, {v: color for v in z})] = value

    return {
        "n": n,
        "A": A,
        "D": D,
        "Ep": Ep,
        "E": E,
        "matchings": matchings,
        "residuals": residuals,
        "q0_terms": q0_terms,
        "h_terms": h_terms,
        "h_edges": h_edges,
        "q_blocks": q_blocks,
        "p5": p5,
    }


def audit_routing_instance(k):
    data = routing_instance(k)
    n = data["n"]
    p5 = data["p5"]

    # h*p_5=0 term by term, so the binomial expansion proves that h cannot
    # alter q_C^k p_5.
    for hword, _ in data["h_terms"]:
        hsupp = {i for i, c in enumerate(hword) if c != -1}
        for zword in p5:
            zsupp = {i for i, c in enumerate(zword) if c != -1}
            assert hsupp & zsupp

    q0k = matching_power(data["q0_terms"], k)
    got0 = product(q0k, p5)
    qfullk = matching_power(data["q0_terms"] + data["h_terms"], k)
    got = product(qfullk, p5)
    expected = {
        tuple([color] * n): value
        for color, value in enumerate(BETA_VALUES)
    }
    assert got0 == expected
    assert got == expected

    # The h blocks are identity matrices and hence precisely rank three.
    rank_three_edges = set(data["h_edges"])
    if data["E"]:
        assert graph_is_connected(tuple(range(n)), rank_three_edges)
    if len(data["E"]) >= 2:
        e0, e1 = data["E"][:2]
        outside = data["A"][0]
        assert {
            tuple(sorted((e0, e1))),
            tuple(sorted((e0, outside))),
            tuple(sorted((e1, outside))),
        } <= rank_three_edges

    # Realize p_5 as beta contraction of q_X^5/5!.  For each color, zip U
    # with the corresponding residual five-set.  There are 15 cross terms.
    total_sites = n + 5
    U = tuple(range(n, n + 5))
    qx_terms = []
    for color, residual in enumerate(data["residuals"]):
        for u, c in zip(U, residual):
            qx_terms.append(
                (monomial(total_sites, {u: color, c: color}), F(1))
            )

    contracted = defaultdict(F)
    for chosen in itertools.combinations(qx_terms, 5):
        word = [-1] * total_sites
        good = True
        for term, _ in chosen:
            for site, color in enumerate(term):
                if color == -1:
                    continue
                if word[site] != -1:
                    good = False
                    break
                word[site] = color
            if not good:
                break
        if not good or any(word[u] == -1 for u in U):
            continue
        uword = tuple(word[u] for u in U)
        beta = F(0)
        if len(set(uword)) == 1:
            beta = BETA_VALUES[uword[0]]
        if beta:
            cword = tuple(word[c] for c in range(n))
            contracted[cword] += beta
    assert {w: a for w, a in contracted.items() if a} == p5

    # The local datum is not a full GHZ source.  Start with the color-zero
    # perfect matching M_0 together with its five crossing edges, then switch
    # the crossing edge landing at the last common E vertex from color 0 to
    # color 1.  The two bijections agree there (all E vertices occur last in
    # the ordered residuals), so this is a supported mixed perfect matching.
    mixed_word_string = "n/a"
    if data["E"]:
        common = data["E"][-1]
        position0 = data["residuals"][0].index(common)
        position1 = data["residuals"][1].index(common)
        assert position0 == position1
        mixed_word = [0] * total_sites
        mixed_word[common] = 1
        mixed_word[U[position0]] = 1
        assert len(set(mixed_word)) == 2

        supported_edges = {
            (tuple(i for i, c in enumerate(word) if c != -1),
             tuple(c for c in word if c != -1))
            for word, _ in data["q0_terms"] + data["h_terms"]
        }
        for word, _ in qx_terms:
            sites = tuple(i for i, c in enumerate(word) if c != -1)
            colors = tuple(c for c in word if c != -1)
            supported_edges.add((sites, colors))
        witness_edges = list(data["matchings"][0])
        for position, (u, c) in enumerate(zip(U, data["residuals"][0])):
            color = 1 if position == position0 else 0
            witness_edges.append((c, u, color))
        for edge in witness_edges[:k]:
            i, j = edge
            sites = tuple(sorted((i, j)))
            assert (sites, (0, 0)) in supported_edges
        for c, u, color in witness_edges[k:]:
            sites = tuple(sorted((c, u)))
            assert (sites, (color, color)) in supported_edges
        mixed_word_string = "".join(map(str, mixed_word))

    # q_U=0 makes p_1=p_3=0 identically, so F_1 beta=0.  The definition of
    # beta above gives delta_U(beta)=BETA_VALUES, all of them nonzero.
    assert all(BETA_VALUES)

    return len(data["q0_terms"]), len(data["h_edges"]), mixed_word_string


# Each 3x3 matrix is stored row-major as nine bits.  These are the matrices
# printed in Section 5's deterministic certificate, with vertices 0,...,6.
SEVEN_SITE_Q_BITS = {
    (0, 1): "100111000",
    (0, 2): "100101011",
    (0, 3): "110101011",
    (0, 4): "100010001",
    (0, 5): "000110000",
    (0, 6): "110011010",
    (1, 2): "101101011",
    (1, 3): "111101011",
    (1, 4): "111110000",
    (1, 5): "101001110",
    (1, 6): "001111111",
    (2, 3): "001110011",
    (2, 4): "100101100",
    (2, 5): "010011110",
    (2, 6): "100100010",
    (3, 4): "000101101",
    (3, 5): "000111101",
    (3, 6): "001011011",
    (4, 5): "001000100",
    (4, 6): "110010011",
    (5, 6): "011101010",
}


def audit_seven_site_surjectivity():
    """Exact Gaussian elimination over GF(2), using Python ints as rows."""
    n = 7
    powers = tuple(3**i for i in range(n))
    pivots = {}
    rank = 0

    # A degree-five basis monomial leaves a unique pair {i,j}.  Multiplying
    # by q inserts one of the nonzero cells of q_ij in that pair.
    for support_tuple in itertools.combinations(range(n), 5):
        support = set(support_tuple)
        i, j = (v for v in range(n) if v not in support)
        bits = SEVEN_SITE_Q_BITS[i, j]
        for colors in itertools.product(COLORS, repeat=5):
            base = sum(c * powers[v] for v, c in zip(support_tuple, colors))
            vector = 0
            for a, b in itertools.product(COLORS, repeat=2):
                if bits[3 * a + b] == "1":
                    output_index = base + a * powers[i] + b * powers[j]
                    vector ^= 1 << output_index

            while vector:
                pivot = vector.bit_length() - 1
                if pivot in pivots:
                    vector ^= pivots[pivot]
                else:
                    pivots[pivot] = vector
                    rank += 1
                    break

    assert rank == 3**n
    return rank


def main():
    for k in (1, 2, 3, 4, 5):
        q0_cells, rank_three_blocks, mixed_word = audit_routing_instance(k)
        graph_label = (
            "connected nonbipartite rank-three graph"
            if k <= 3
            else "routing identity"
        )
        print(
            f"|C|={2*k+5}: exact failed-cut routing PASS "
            f"(q0 cells={q0_cells}, rank-three blocks={rank_three_blocks}, "
            f"{graph_label}, mixed full word={mixed_word})"
        )
    rank = audit_seven_site_surjectivity()
    print(f"|C|=7: multiplication R_5 -> R_7 has GF(2) rank {rank}=3^7")
    print("all exact audits: PASS")


if __name__ == "__main__":
    main()
