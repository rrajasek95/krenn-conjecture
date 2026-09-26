#!/usr/bin/env python3
"""Bounded exact checks of actual-cofactor identities in the triangle proof."""

from __future__ import annotations

import argparse
from functools import lru_cache
import json
from pathlib import Path


def hafnians(matrix):
    n = len(matrix)

    @lru_cache(None)
    def hf(mask):
        if not mask:
            return 1
        if mask.bit_count() % 2:
            return 0
        p = (mask & -mask).bit_length() - 1
        return sum(matrix[p][q] * hf(mask ^ (1 << p) ^ (1 << q))
                   for q in range(p + 1, n) if mask & (1 << q))

    return hf


def cofactors(matrix):
    n = len(matrix)
    full = (1 << n) - 1
    hf = hafnians(matrix)
    return [[hf(full ^ (1 << i) ^ (1 << j)) if i != j else 0
             for j in range(n)] for i in range(n)]


def edge(matrix, i, j, value):
    matrix[i][j] = matrix[j][i] = value


def background(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(2, n):
        for j in range(i + 1, n):
            value = ((3*i + 5*j) % 11) - 5
            edge(matrix, i, j, value or 7)
    return matrix


def deleted_haf(matrix, removed):
    mask = (1 << len(matrix)) - 1
    for p in removed:
        mask ^= 1 << p
    return hafnians(matrix)(mask)


def mc(matrix, cof, i, j):
    return sum(matrix[i][r] * cof[r][j] for r in range(len(matrix)))


def check_two_cubic(n, same_external=False):
    # p=0,q=1,r=2,s=3,t=4 (or t=s). The common neighbor r
    # keeps arbitrary dense background edges, testing its unrestricted degree.
    matrix = background(n)
    p, q, r, s = 0, 1, 2, 3
    t = s if same_external else 4
    edge(matrix, p, q, 2)
    edge(matrix, p, r, 3)
    edge(matrix, p, s, 5)
    edge(matrix, q, r, 7)
    edge(matrix, q, t, 11)
    c = cofactors(matrix)
    checks = 0
    for root, neighbors in [(p, [q, r, s]), (q, [p, r, t])]:
        h = deleted_haf(matrix, [root] + neighbors)
        for omitted_index in range(3):
            deleted = neighbors[omitted_index]
            other = [v for v in neighbors if v != deleted]
            expected = 2 * matrix[root][other[0]] * matrix[root][other[1]] * h
            assert mc(matrix, c, root, deleted) == expected
            checks += 1
        for i, j, other in [(neighbors[0], neighbors[1], neighbors[2]),
                            (neighbors[0], neighbors[2], neighbors[1]),
                            (neighbors[1], neighbors[2], neighbors[0])]:
            assert c[i][j] == matrix[root][other] * h
            checks += 1
    if not same_external:
        assert mc(matrix, c, p, t) == 2 * matrix[p][q] * c[q][t]
        assert mc(matrix, c, q, s) == 2 * matrix[p][q] * c[p][s]
        checks += 2
    return checks


def check_three_cubic(n):
    # Triangle 0,1,2 has distinct spokes 3,4,5. Everything outside
    # the triangle is arbitrary, so no cubic premise is imposed there.
    matrix = background(n)
    for j in range(3, n):
        edge(matrix, 2, j, 0)
    for i, j, w in [(0, 1, 2), (0, 2, 3), (1, 2, 5),
                    (0, 3, 7), (1, 4, 11), (2, 5, 13)]:
        edge(matrix, i, j, w)
    c = cofactors(matrix)
    h = deleted_haf(matrix, range(6))
    h34 = deleted_haf(matrix, [0, 1, 2, 5])
    h35 = deleted_haf(matrix, [0, 1, 2, 4])
    h45 = deleted_haf(matrix, [0, 1, 2, 3])
    assert c[3][4] == 2 * 13 * h
    assert c[3][5] == 3 * 11 * h
    assert c[4][5] == 5 * 7 * h
    assert c[0][3] == 11 * 13 * h + 5 * h45
    assert c[1][4] == 7 * 13 * h + 3 * h35
    assert c[2][5] == 7 * 11 * h + 2 * h34
    expected = 7*11*13*h + 7*5*h45 + 11*3*h35 + 13*2*h34
    assert hafnians(matrix)((1 << n) - 1) == expected
    return 7


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = []
    for n in [6, 8, 10, 12]:
        results.append({"order": n,
                        "distinct_spokes_identity_checks": check_two_cubic(n),
                        "coincident_spokes_identity_checks": check_two_cubic(n, True),
                        "forced_triangle_checks": check_three_cubic(n)})
    report = {"status": "PASS", "scope": "bounded exact identity controls; not a census or a source-existence test",
              "cases": results, "total_identities": sum(
                  r["distinct_spokes_identity_checks"] + r["coincident_spokes_identity_checks"]
                  + r["forced_triangle_checks"] for r in results)}
    output = json.dumps(report, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as stream:
            stream.write(output)
    print(output, end="")


if __name__ == "__main__":
    main()
