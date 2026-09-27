"""Integer Gram-matrix verification of the complex star norm identity."""

from itertools import combinations, product
from algebra import (E, ZERO, ONE, cell, require, cells, star, four_derivative,
                     four_outputs, norm2)


def gram(rows, dimension):
    result = [[0]*dimension for _ in range(dimension)]
    for row in rows:
        for i, x in row.items():
            for j, y in row.items():
                result[i][j] += x*y
    return result


def check_case(k, q):
    leaf_cells = [(i, j, a, b) for i, j in combinations(range(1, k+1), 2)
                  for a, b in product(range(q), repeat=2)]
    ix = {c: j for j, c in enumerate(leaf_cells)}
    columns, rows = four_derivative(star(k+1, q), k+1, q)
    indices = [columns.index(c) for c in leaf_cells]
    response_rows = []
    for (vertices, word), row in rows.items():
        if 0 in vertices:
            sparse = {}
            for j, col in enumerate(indices):
                z = row[col]
                require(z.b == 0 and z.a.denominator == 1, "Integer response matrix")
                if z:
                    sparse[j] = int(z.a)
            response_rows.append(sparse)
    sum_rows = []
    for i in range(1, k+1):
        for a, b in product(range(q), repeat=2):
            sum_rows.append({ix[cell(i, j, a, b)]: 1
                             for j in range(1, k+1) if j != i})
    G, R = gram(response_rows, len(ix)), gram(sum_rows, len(ix))
    gamma = q*(k-2)-2
    require(all(G[i][j]-R[i][j] == (gamma if i == j else 0)
                for i in range(len(ix)) for j in range(len(ix))),
            "Every coefficient of the Hermitian norm identity")

    B = {c: E((c[0]+2*c[1]+3*c[2]+c[3]) % 5-2,
              (c[0]+c[1]+c[2]+2*c[3]) % 3-1) for c in leaf_cells}
    observed = {key: z for key, z in four_outputs(star(k+1, q) | B, k+1, q).items()
                if 0 in key[0]}
    row_norm = sum(sum((B[cell(i, j, a, b)] for j in range(1, k+1) if j != i),
                       ZERO).abs2() for i in range(1, k+1)
                   for a, b in product(range(q), repeat=2))
    require(norm2(observed) == gamma*norm2(B)+row_norm, "Independent complex expansion")
    if q >= 2:
        sharp = {}
        for i, j, sign in ((1, 2, 1), (2, 3, 1), (1, 3, -1)):
            sharp[i, j, 0, 1] = E(sign)
            sharp[i, j, 1, 0] = E(-sign)
    elif k >= 4:
        sharp = {(1, 2, 0, 0): ONE, (2, 3, 0, 0): -ONE,
                 (3, 4, 0, 0): ONE, (1, 4, 0, 0): -ONE}
    else:
        sharp = None
    if sharp is not None:
        actual = {key: z for key, z in four_outputs(star(k+1, q) | sharp, k+1, q).items()
                  if 0 in key[0]}
        require(norm2(actual) == gamma*norm2(sharp), "Sharp cycle attains the coefficient")
        require(norm2(actual) != (gamma+1)*norm2(sharp), "Larger coefficient rejected")
    return dict(leaves=k, colors=q, coefficient=gamma, gram_dimension=len(ix),
                complex_fixture_norm=str(norm2(observed)), sharp_cycle=sharp is not None)


def check():
    return [check_case(k, q) for k, q in ((3, 1), (3, 2), (3, 3), (4, 1),
                                         (4, 2), (5, 1), (5, 2), (5, 3))]
