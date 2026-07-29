#!/usr/bin/env python3
"""Exact finite audit for distinct-missing-pair-common-power-obstruction.md.

The arbitrary-tensor steps in the note are hand proofs.  This checker
audits every finite support classification, reconstructs the matching
equations, and checks the two elimination identities in the star quotient
over exact rational arithmetic.  It imports no project module.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
import random


U = tuple(range(6))
EDGES = tuple(combinations(U, 2))


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def perfect_matchings_4(sites):
    a, b, c, d = tuple(sorted(sites))
    return (
        (edge(a, b), edge(c, d)),
        (edge(a, c), edge(b, d)),
        (edge(a, d), edge(b, c)),
    )


def graph_type(es):
    degree = [0] * 6
    used = set()
    for u, v in es:
        degree[u] += 1
        degree[v] += 1
        used.update((u, v))
    shape = tuple(sorted((d for d in degree if d), reverse=True))
    if shape == (1, 1, 1, 1, 1, 1):
        return "3K2"
    if shape == (2, 1, 1, 1, 1):
        return "P3+K2"
    if shape == (2, 2, 1, 1):
        return "P4"
    if shape == (3, 1, 1, 1):
        return "K1,3"
    if shape == (2, 2, 2) and len(used) == 3:
        return "K3"
    raise AssertionError((es, shape))


def audit_graphs_and_word_separation():
    counts = {name: 0 for name in ("3K2", "P3+K2", "P4", "K1,3", "K3")}
    for triple in combinations(EDGES, 3):
        counts[graph_type(triple)] += 1

        # q_{P_i}F_i has arbitrary colors on P_i and fixed color i off it.
        word_sets = []
        for color, pair in enumerate(triple):
            words = set()
            for inside_colors in product(range(3), repeat=2):
                word = [color] * 6
                word[pair[0]], word[pair[1]] = inside_colors
                words.add(tuple(word))
            word_sets.append(words)
        for i, j in combinations(range(3), 2):
            assert word_sets[i].isdisjoint(word_sets[j])

    assert counts == {
        "3K2": 15,
        "P3+K2": 180,
        "P4": 180,
        "K1,3": 60,
        "K3": 20,
    }
    assert sum(counts.values()) == 455
    return counts


def matching_product_count(mask: int, sites, edge_index):
    return sum(
        bool(mask & (1 << edge_index[e])) and bool(mask & (1 << edge_index[f]))
        for e, f in perfect_matchings_4(sites)
    )


def audit_p4_support():
    # a,b,c,d,e,f = 0,...,5 and P_i=ab,bc,cd.
    missing = (edge(0, 1), edge(1, 2), edge(2, 3))
    targets = {
        tuple(sorted(set(U) - set(pair)))
        for pair in missing
    }
    edge_index = {e: i for i, e in enumerate(EDGES)}
    survivors = []
    for mask in range(1 << len(EDGES)):
        if any(mask & (1 << edge_index[e]) for e in missing):
            continue
        admissible = True
        for sites in combinations(U, 4):
            count = matching_product_count(mask, sites, edge_index)
            if sites in targets:
                # A nonzero target needs at least one nonzero matching term.
                if count == 0:
                    admissible = False
                    break
            elif count == 1:
                # One nonzero tensor product cannot cancel to zero.
                admissible = False
                break
        if admissible:
            survivors.append(mask)

    # q_ef is free at the support level; all six core blocks vanish and all
    # eight core-to-{e,f} blocks are nonzero.
    assert len(survivors) == 2
    core = tuple(combinations(range(4), 2))
    spokes = tuple((x, y) for x in range(4) for y in (4, 5))
    for mask in survivors:
        assert all(not (mask & (1 << edge_index[e])) for e in core)
        assert all(mask & (1 << edge_index[e]) for e in spokes)
    assert {bool(mask & (1 << edge_index[(4, 5)])) for mask in survivors} == {False, True}

    # A zero bracket allows only equal nonempty row states.  The connected
    # zero graph then leaves the all-both state as the unique possibility.
    states = ((1, 0), (0, 1), (1, 1))
    nonzero_pairs = ((0, 1), (0, 3), (2, 3))
    zero_pairs = ((0, 2), (1, 2), (1, 3))
    state_survivors = []
    for rows in product(states, repeat=4):
        if any(not (rows[x][0] * rows[y][1] or rows[x][1] * rows[y][0])
               for x, y in nonzero_pairs):
            continue
        if any(rows[x][0] * rows[y][1] != rows[x][1] * rows[y][0]
               for x, y in zero_pairs):
            continue
        state_survivors.append(rows)
    assert state_survivors == [((1, 1),) * 4]
    return len(survivors)


def audit_k3_support():
    cols = frozenset(range(3))
    nonempty = [frozenset(s) for r in range(1, 4) for s in combinations(cols, r)]
    allowed = []
    for left in nonempty:
        for right in nonempty:
            good = all(
                ((u in left and v in right) == (v in left and u in right))
                for u, v in combinations(cols, 2)
            )
            if good:
                allowed.append((left, right))
    assert len(allowed) == 7
    assert all(left == right for left, right in allowed)

    # Exact scalar contradictions used after crossing factorization.
    # Full support: rho0=-rho1=-rho2 conflicts with rho1=-rho2.
    rho0 = Fraction(7, 5)
    rho1 = -rho0
    rho2 = -rho0
    assert rho1 + rho2 == -2 * rho0 != 0

    # Two-column support: w=(r,-s) spans v^perp but is not self-orthogonal.
    r, s = Fraction(3, 2), Fraction(5, 7)
    w = (r, -s)
    self_pairing = 2 * w[0] * w[1]
    assert self_pairing == -2 * r * s != 0
    return len(allowed)


def outer(x, y):
    return tuple(tuple(a * b for b in y) for a in x)


def madd(*matrices):
    return tuple(
        tuple(sum(matrix[i][j] for matrix in matrices) for j in range(3))
        for i in range(3)
    )


def mscale(a, matrix):
    return tuple(tuple(a * x for x in row) for row in matrix)


def vadd(*vectors):
    return tuple(sum(vector[i] for vector in vectors) for i in range(3))


def vscale(a, vector):
    return tuple(a * x for x in vector)


def random_vector(rng):
    return tuple(Fraction(rng.randrange(-7, 8), rng.randrange(1, 8)) for _ in range(3))


def random_nonzero(rng):
    while True:
        x = Fraction(rng.randrange(-7, 8), rng.randrange(1, 8))
        if x:
            return x


def audit_star_matching_and_elimination():
    # On sites b,c,d,e,f = 0,...,4 the target four-sets are cdef, bdef,
    # bcef, while bcde and bcdf are zero.  Reconstruct their matchings.
    expected = {
        (1, 2, 3, 4): (((1, 2), (3, 4)), ((1, 3), (2, 4)), ((1, 4), (2, 3))),
        (0, 2, 3, 4): (((0, 2), (3, 4)), ((0, 3), (2, 4)), ((0, 4), (2, 3))),
        (0, 1, 3, 4): (((0, 1), (3, 4)), ((0, 3), (1, 4)), ((0, 4), (1, 3))),
        (0, 1, 2, 3): (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))),
        (0, 1, 2, 4): (((0, 1), (2, 4)), ((0, 2), (1, 4)), ((0, 4), (1, 2))),
    }
    for sites, matchings in expected.items():
        assert perfect_matchings_4(sites) == matchings

    # Audit identities (23) over exact rationals for many deterministic
    # inputs satisfying the two linear relations (21).
    rng = random.Random(20260727)
    for _ in range(64):
        A, B, C = (random_nonzero(rng) for _ in range(3))
        Xc, Xd, Yc, Yd = (random_vector(rng) for _ in range(4))
        H_rows = tuple(random_vector(rng) for _ in range(3))
        H = tuple(tuple(row) for row in H_rows)
        Xb = vscale(-1 / A, vadd(vscale(C, Xd), vscale(B, Xc)))
        Yb = vscale(-1 / A, vadd(vscale(C, Yd), vscale(B, Yc)))
        M = madd(outer(Xc, Yd), outer(Xd, Yc))
        T0 = madd(mscale(A, H), M)
        T1 = madd(mscale(B, H), outer(Xb, Yd), outer(Xd, Yb))
        T2 = madd(mscale(C, H), outer(Xb, Yc), outer(Xc, Yb))
        lhs1 = mscale(2, madd(mscale(B, M), mscale(C, outer(Xd, Yd))))
        rhs1 = madd(mscale(B, T0), mscale(-A, T1))
        lhs2 = mscale(2, madd(mscale(C, M), mscale(B, outer(Xc, Yc))))
        rhs2 = madd(mscale(C, T0), mscale(-A, T2))
        assert lhs1 == rhs1
        assert lhs2 == rhs2

    # Audit identity (25) in the A=0, B*C!=0 branch.
    for _ in range(64):
        B, C = random_nonzero(rng), random_nonzero(rng)
        Xb, Xc, Yb, Yc = (random_vector(rng) for _ in range(4))
        Xd, Yd = vscale(-B / C, Xc), vscale(-B / C, Yc)
        H = tuple(random_vector(rng) for _ in range(3))
        N = madd(outer(Xb, Yc), outer(Xc, Yb))
        T1 = madd(mscale(B, H), outer(Xb, Yd), outer(Xd, Yb))
        T2 = madd(mscale(C, H), N)
        assert mscale(2 * B / C, N) == madd(mscale(B / C, T2), mscale(-1, T1))

    # In the A=B=C=0 branch, every assignment of an X/Y dependence mark
    # to the three triangle edges repeats a mark on two incident edges.
    triangle_edges = ((0, 1), (0, 2), (1, 2))
    for marks in product(("X", "Y"), repeat=3):
        found = False
        for i, j in combinations(range(3), 2):
            if marks[i] == marks[j] and set(triangle_edges[i]) & set(triangle_edges[j]):
                found = True
        assert found
    return 128


def main():
    counts = audit_graphs_and_word_separation()
    p4 = audit_p4_support()
    k3 = audit_k3_support()
    star = audit_star_matching_and_elimination()
    print("distinct missing-pair common-power obstruction: PASS")
    print("three-edge graph census:", counts)
    print("P4 necessary support survivors:", p4, "(q_ef absent/present)")
    print("K3 allowed nonempty support pairs:", k3, "(all equal)")
    print("star exact rational elimination identity trials:", star)
    print("scope: P4, K1,3, K3; arbitrary endpoint tensors; characteristic != 2")


if __name__ == "__main__":
    main()
