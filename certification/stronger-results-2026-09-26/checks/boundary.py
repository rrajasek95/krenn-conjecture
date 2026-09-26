"""Exact scope controls; the all-order component proof is in the sibling note."""
import argparse
from functools import lru_cache
from itertools import combinations, product
from math import prod
import json
from pathlib import Path


def hafnians(matrix):
    n = len(matrix)

    @lru_cache(None)
    def haf(vertices):
        if not vertices:
            return 1
        if len(vertices) % 2:
            return 0
        p = vertices[0]
        return sum(matrix[p][q] * haf(vertices[1:i] + vertices[i + 1 :])
                   for i, q in enumerate(vertices[1:], 1))

    return haf


def cofactor(matrix):
    n = len(matrix)
    haf = hafnians(matrix)
    return [[haf(tuple(v for v in range(n) if v not in (i, j))) if i != j else 0
             for j in range(n)] for i in range(n)]


def weighted_matching(n, edges):
    matrix = [[0] * n for _ in range(n)]
    for u, v, weight in edges:
        matrix[u][v] = matrix[v][u] = weight
    return matrix


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    matrices = [weighted_matching(4, [(0, 1, 2), (2, 3, 3)]),
                weighted_matching(4, [(0, 2, 5), (1, 3, 7)]),
                weighted_matching(4, [(0, 3, 11), (1, 2, 13)])]
    hafs = [hafnians(matrix) for matrix in matrices]
    amplitudes = [6, 35, 143]
    for word in product(range(3), repeat=4):
        value = prod(hafs[h](tuple(v for v in range(4) if word[v] == h)) for h in range(3))
        assert value == (amplitudes[word[0]] if len(set(word)) == 1 else 0)
    boundary_blocks = []
    for k in (1, 2):
        c = cofactor(matrices[k])
        assert all(c[u][v] == 0 for u in (0, 1) for v in (0, 1))
        boundary = [[c[u][v] for v in (2, 3)] for u in (0, 1)]
        assert boundary[0][0] * boundary[1][1] - boundary[0][1] * boundary[1][0] != 0
        boundary_blocks.append(boundary)

    w = [[0, 1, 1, 1], [1, 0, 1, -1], [1, -1, 0, 1], [1, 1, -1, 0]]
    scalar = [[0] * 10 for _ in range(10)]
    for u in range(4):
        for t in range(4):
            scalar[u][4 + t] = scalar[4 + t][u] = w[u][t]
    scalar[8][9] = scalar[9][8] = 5
    haf = hafnians(scalar)
    c = cofactor(scalar)
    assert haf(tuple(range(10))) == 15
    for i in range(10):
        for j in range(10):
            assert sum(scalar[i][v] * c[v][j] for v in range(10)) == 15 * (i == j)
    stars = 0
    for p in range(10):
        for r in range(1, 5):
            value = sum(prod(scalar[p][u] for u in occupied)
                        * haf(tuple(v for v in range(10) if v != p and v not in occupied))
                        for occupied in combinations([v for v in range(10) if v != p], 2 * r + 1))
            assert value == 0
            stars += 1
    result = {'status': 'PASS', 'scope': 'exact finite scope controls only',
              'K4_full_coefficients_checked': 81, 'K4_other_cofactor_boundary_blocks': boundary_blocks,
              'crown_plus_edge_scalar_hafnian': 15, 'scalar_cofactor_inverse_entries_checked': 100,
              'higher_single_color_star_sums_checked': stars,
              'scalar_color_degrees': [sum(bool(x) for x in row) for row in scalar]}
    output = json.dumps(result, indent=2) + '\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(output)
    print(output, end='')


if __name__ == '__main__':
    main()
