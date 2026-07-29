#!/usr/bin/env python3
"""Finite-field reconnaissance for the colour-diagonal pure-square branch.

This is deliberately an explorer, not a characteristic-zero certificate.
It searches triples of scalar square-free quadratics f_0,f_1,f_2 on six
sites such that

    f_i f_j = 0 (i != j),   f_i^[2] != 0,   f_i^[3] = 0.

Such a triple gives a quadratic q whose endpoint-colour blocks are diagonal
and whose second matching power is pure monochromatic.  The script records
the support patterns of the three square vectors and tests whether localized
coordinate star rows can satisfy all nine product equations.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
from math import prod
import random


U = tuple(range(6))
EDGES = tuple(combinations(U, 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}
FOUR_SETS = tuple(combinations(U, 4))
PAIRINGS4 = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    u = vertices[0]
    out = []
    for j in range(1, len(vertices)):
        v = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for matching in perfect_matchings(rest):
            out.append(((min(u, v), max(u, v)),) + matching)
    return tuple(out)


MATCHINGS6 = perfect_matchings(U)


def inv(a, p):
    return pow(a % p, p - 2, p)


def rref_nullspace(rows, p, ncols=15):
    rows = [[x % p for x in row] for row in rows]
    pivot_cols = []
    r = 0
    for c in range(ncols):
        pivot = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        scale = inv(rows[r][c], p)
        rows[r] = [(scale * x) % p for x in rows[r]]
        for i in range(len(rows)):
            if i == r or not rows[i][c]:
                continue
            scale = rows[i][c]
            rows[i] = [(x - scale * y) % p for x, y in zip(rows[i], rows[r])]
        pivot_cols.append(c)
        r += 1
        if r == len(rows):
            break
    free = [c for c in range(ncols) if c not in pivot_cols]
    basis = []
    for c in free:
        v = [0] * ncols
        v[c] = 1
        for i, pc in enumerate(pivot_cols):
            v[pc] = -rows[i][c] % p
        basis.append(tuple(v))
    return tuple(basis), len(pivot_cols)


def product_matrix(f, p):
    """Matrix g -> coefficient vector of f*g in degree four."""
    rows = []
    for sites in FOUR_SETS:
        row = [0] * len(EDGES)
        for a, b, c, d in PAIRINGS4:
            e = tuple(sorted((sites[a], sites[b])))
            h = tuple(sorted((sites[c], sites[d])))
            row[EDGE_INDEX[h]] = (row[EDGE_INDEX[h]] + f[EDGE_INDEX[e]]) % p
            row[EDGE_INDEX[e]] = (row[EDGE_INDEX[e]] + f[EDGE_INDEX[h]]) % p
        rows.append(row)
    return rows


def multiply(f, g, p):
    return tuple(
        sum(a * b for a, b in zip(row, g)) % p
        for row in product_matrix(f, p)
    )


def square(f, p):
    # Matching-power convention omits the polarization factor two.
    out = []
    for sites in FOUR_SETS:
        value = 0
        for a, b, c, d in PAIRINGS4:
            e = tuple(sorted((sites[a], sites[b])))
            h = tuple(sorted((sites[c], sites[d])))
            value += f[EDGE_INDEX[e]] * f[EDGE_INDEX[h]]
        out.append(value % p)
    return tuple(out)


def cube(f, p):
    return sum(
        prod(f[EDGE_INDEX[e]] for e in matching)
        for matching in MATCHINGS6
    ) % p


def random_span(basis, p, rng):
    coefficients = [rng.randrange(p) for _ in basis]
    return tuple(
        sum(a * v[j] for a, v in zip(coefficients, basis)) % p
        for j in range(len(EDGES))
    )


def support(v):
    return tuple(EDGES[i] for i, x in enumerate(v) if x)


def localized_rows(squares, p):
    """Find oriented endpoint pairs giving the literal coordinate response."""
    lambdas = [dict(zip((tuple(sorted(set(U) - set(S))) for S in FOUR_SETS), sq))
               for sq in squares]
    oriented = tuple((u, v) for u in U for v in U if u != v)
    for rows in product(oriented, repeat=3):
        if any(lambdas[i][tuple(sorted(rows[i]))] == 0 for i in range(3)):
            continue
        if any(
            lambdas[c][tuple(sorted(rows[i]))] != 0
            for i in range(3) for c in range(3) if c != i
        ):
            continue
        good = True
        for i in range(3):
            for j in range(3):
                if i == j or rows[i][0] == rows[j][1]:
                    continue
                pair = tuple(sorted((rows[i][0], rows[j][1])))
                if any(lambdas[c][pair] for c in range(3)):
                    good = False
                    break
            if not good:
                break
        if good:
            return rows
    return None


def solve_affine(rows, rhs, p, ncols=6):
    matrix = [[x % p for x in row] + [b % p] for row, b in zip(rows, rhs)]
    pivot_cols = []
    r = 0
    for c in range(ncols):
        pivot = next((i for i in range(r, len(matrix)) if matrix[i][c]), None)
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        scale = inv(matrix[r][c], p)
        matrix[r] = [(scale * x) % p for x in matrix[r]]
        for i in range(len(matrix)):
            if i == r or not matrix[i][c]:
                continue
            scale = matrix[i][c]
            matrix[i] = [(x - scale * y) % p for x, y in zip(matrix[i], matrix[r])]
        pivot_cols.append(c)
        r += 1
    if any(not any(row[:ncols]) and row[ncols] for row in matrix):
        return None
    answer = [0] * ncols
    for i, c in enumerate(pivot_cols):
        answer[c] = matrix[i][ncols]
    return tuple(answer)


def solve_axis_separated_stars(squares, p, rng, trials=200):
    """Try p_i on colour i and s_j on colour j, with arbitrary site support."""
    missing = tuple(tuple(sorted(set(U) - set(S))) for S in FOUR_SETS)
    terms = tuple(
        (c, missing[k], value)
        for c, sq in enumerate(squares)
        for k, value in enumerate(sq)
        if value
    )
    for _ in range(trials):
        avecs = tuple(tuple(rng.randrange(p) for _ in U) for _ in range(3))
        bvecs = []
        for j in range(3):
            equations = {}
            for i in range(3):
                for c, (u, v), value in terms:
                    word = [c] * 6
                    word[u], word[v] = i, j
                    row = equations.setdefault((i, tuple(word)), [0] * 6)
                    row[v] = (row[v] + value * avecs[i][u]) % p
                    word[u], word[v] = j, i
                    row = equations.setdefault((i, tuple(word)), [0] * 6)
                    row[u] = (row[u] + value * avecs[i][v]) % p
            targets = {(i, (i,) * 6): int(i == j) for i in range(3)}
            keys = set(equations) | set(targets)
            rows = [equations.get(key, [0] * 6) for key in keys]
            rhs = [targets.get(key, 0) for key in keys]
            b = solve_affine(rows, rhs, p)
            if b is None:
                break
            bvecs.append(b)
        if len(bvecs) == 3:
            return avecs, tuple(bvecs)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=5)
    parser.add_argument("--trials", type=int, default=200000)
    parser.add_argument("--seed", type=int, default=20260727)
    parser.add_argument("--samples-per-kernel", type=int, default=40)
    parser.add_argument("--star-trials", type=int, default=100)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--seek-full-union", action="store_true")
    parser.add_argument("--seek-private-squares", action="store_true")
    parser.add_argument("--seek-private-full-union", action="store_true")
    args = parser.parse_args()
    p = args.prime
    rng = random.Random(args.seed)
    seen = set()
    found = 0
    localized = 0
    for trial in range(1, args.trials + 1):
        # Bias toward sparse f: large annihilators are rare for dense forms.
        f = tuple(rng.randrange(p) if rng.random() < 0.35 else 0 for _ in EDGES)
        sf = square(f, p)
        if not any(sf) or cube(f, p):
            continue
        ann_f, rank_f = rref_nullspace(product_matrix(f, p), p)
        if not ann_f:
            continue
        for _ in range(args.samples_per_kernel):
            g = random_span(ann_f, p, rng)
            sg = square(g, p)
            if not any(sg) or cube(g, p):
                continue
            rows = product_matrix(f, p) + product_matrix(g, p)
            common, _ = rref_nullspace(rows, p)
            if not common:
                continue
            for __ in range(args.samples_per_kernel):
                h = random_span(common, p, rng)
                sh = square(h, p)
                if not any(sh) or cube(h, p):
                    continue
                key = tuple(sorted((tuple(sorted(map(str, support(x)))) for x in (f, g, h))))
                if key in seen:
                    continue
                seen.add(key)
                found += 1
                union_vertices = {
                    u for x in (f, g, h) for edge_ in support(x) for u in edge_
                }
                if args.seek_private_full_union:
                    sq_supports = [
                        {i for i, value in enumerate(sq) if value}
                        for sq in (sf, sg, sh)
                    ]
                    private = [
                        sq_supports[i] - set().union(*(
                            sq_supports[j] for j in range(3) if j != i
                        ))
                        for i in range(3)
                    ]
                    if union_vertices == set(U) and all(private):
                        print("private-square full-union finite-field candidate")
                        print(" f", tuple(zip(EDGES, f)))
                        print(" g", tuple(zip(EDGES, g)))
                        print(" h", tuple(zip(EDGES, h)))
                        print(" squares", sf, sg, sh)
                        print(" private indices", private)
                        return
                    continue
                if args.seek_full_union:
                    if union_vertices == set(U):
                        print("full-union finite-field exception")
                        print(" f", tuple(zip(EDGES, f)))
                        print(" g", tuple(zip(EDGES, g)))
                        print(" h", tuple(zip(EDGES, h)))
                        print(" squares", sf, sg, sh)
                        return
                    continue
                if args.seek_private_squares:
                    sq_supports = [
                        {i for i, value in enumerate(sq) if value}
                        for sq in (sf, sg, sh)
                    ]
                    private = [
                        sq_supports[i] - set().union(*(
                            sq_supports[j] for j in range(3) if j != i
                        ))
                        for i in range(3)
                    ]
                    if all(private):
                        print("private-square finite-field candidate")
                        print(" f", tuple(zip(EDGES, f)))
                        print(" g", tuple(zip(EDGES, g)))
                        print(" h", tuple(zip(EDGES, h)))
                        print(" squares", sf, sg, sh)
                        print(" private indices", private)
                        return
                    continue
                stars = localized_rows((sf, sg, sh), p)
                axis_stars = solve_axis_separated_stars(
                    (sf, sg, sh), p, rng, args.star_trials
                )
                if stars is not None:
                    localized += 1
                if args.verbose or stars is not None or axis_stars is not None:
                    print(
                        f"solution {found}: edge-support sizes "
                        f"{tuple(len(support(x)) for x in (f,g,h))}; "
                        f"square-support sizes {tuple(sum(bool(y) for y in x) for x in (sf,sg,sh))}; "
                        f"localized={stars}; axis-separated={axis_stars}"
                    )
                    print(" f", tuple(zip(EDGES, f)))
                    print(" g", tuple(zip(EDGES, g)))
                    print(" h", tuple(zip(EDGES, h)))
                if stars is not None or axis_stars is not None:
                    print("finite-field response witness found")
                    return
        if trial % 10000 == 0:
            print(f"trial {trial}: {found} triples, {localized} localized")
    print(f"done: {found} triples, {localized} localized")


if __name__ == "__main__":
    main()
