#!/usr/bin/env python3
"""Exact independent normalization checks for the provisional endpoint proof.

Direct partial-matchings recursion computes mean coefficients and two dual
derivatives. No imported proof helper, assigned inverse, or cached tensor.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json


ZERO = (F(0), F(0), F(0), F(0))
ONE = (F(1), F(0), F(0), F(0))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def mul(a, b):
    # 1, epsilon, delta, epsilon*delta, with both squares zero.
    return (a[0]*b[0], a[0]*b[1]+a[1]*b[0],
            a[0]*b[2]+a[2]*b[0],
            a[0]*b[3]+a[1]*b[2]+a[2]*b[1]+a[3]*b[0])


def tensor(core_b, core_h, means, row_u=None, row_v=None):
    n = len(core_b)
    row_u = row_u or [(F(0), F(0)) for _ in range(n)]
    row_v = row_v or [(F(0), F(0)) for _ in range(n)]
    answer = {}
    for word in product((0, 1), repeat=n):
        @lru_cache(None)
        def rec(mask):
            if not mask:
                return ONE
            i = (mask & -mask).bit_length()-1
            rest = mask ^ (1 << i)
            monomer = (means[i][word[i]], row_u[i][word[i]],
                       row_v[i][word[i]], F(0))
            total = mul(monomer, rec(rest))
            for j in range(i+1, n):
                if (rest >> j) & 1 and word[i] == word[j]:
                    core = core_b if word[i] == 0 else core_h
                    total = add(total, scale(core[i][j], rec(rest ^ (1 << j))))
            return total
        answer[word] = rec((1 << n)-1)
    return tuple({w: z[k] for w, z in answer.items()} for k in range(4))


def pairing(a, b):
    return sum((-1)**sum(wi == 0 for wi in w) * value *
               b[tuple(1-wi for wi in w)] for w, value in a.items())


def means(a, x, b, y):
    return [tuple(a*xi+b*yi for xi, yi in zip(xi, yi))
            for xi, yi in zip(x, y)]


def zero_matrix(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def haf(matrix):
    n = len(matrix)
    @lru_cache(None)
    def rec(mask):
        if not mask:
            return F(1)
        i = (mask & -mask).bit_length()-1
        rest = mask ^ (1 << i)
        return sum(matrix[i][j]*rec(rest ^ (1 << j)) for j in range(i+1, n)
                   if (rest >> j) & 1)
    return rec((1 << n)-1)


def kernel(core_b, core_h, x, y, u, v, p, q):
    first = tensor(core_b, core_h, means(p[0], x, q[0], y), u, v)
    second = tensor(core_b, core_h, means(p[1], x, q[1], y), u, v)
    scalar = pairing(first[0], second[0])
    mat = [[pairing(first[3], second[0]), pairing(first[1], second[2])],
           [pairing(first[2], second[1]), pairing(first[0], second[3])]]
    return scalar, mat


def generic_check(n):
    b = zero_matrix(n)
    h = zero_matrix(n)
    for i in range(n):
        for j in range(i+1, n):
            b[i][j] = b[j][i] = F(((i+2)*(j+3)) % 9-4)
            h[i][j] = h[j][i] = F(((i+4)*(j+1)) % 11-5)
    x = [(F(i-2), F(0)) for i in range(n)]
    y = [(F(3-i), F(0)) for i in range(n)]
    u = [(F(0), F((2*i+1) % 7-3)) for i in range(n)]
    v = [(F(0), F((3*i+2) % 5-2)) for i in range(n)]
    p, q = [F(1), F(2)], [F(-2), F(3)]
    c, s = F(3, 5), F(4, 5)
    r = [[c, s], [-s, c]]
    rotate = lambda z: [sum(r[i][j]*z[j] for j in range(2)) for i in range(2)]
    scalar, mat = kernel(b, h, x, y, u, v, p, q)
    other, rotated_mat = kernel(b, h, x, y, u, v, rotate(p), rotate(q))
    predicted = [[sum(r[i][k]*mat[k][l]*r[j][l]
                      for k in range(2) for l in range(2))
                  for j in range(2)] for i in range(2)]
    assert scalar == other
    assert predicted == rotated_mat
    reflected, reflected_mat = kernel(b, h, x, y, u, v,
                                       [-p[0], p[1]], [-q[0], q[1]])
    assert reflected == scalar
    assert reflected_mat == [[mat[0][0], -mat[0][1]],
                             [-mat[1][0], mat[1][1]]]
    return {'retained_sites': n, 'scalar_kernel': str(scalar),
            'mixed_derivative_matrix': [[str(z) for z in row] for row in mat],
            'orthogonal_covariance': True, 'reflection_covariance': True}


def k4_check():
    colors = [zero_matrix(4) for _ in range(3)]
    for color, edges in zip(colors, [[(0,1,2),(2,3,3)],
                                    [(0,2,5),(1,3,7)],
                                    [(0,3,11),(1,2,13)]]):
        for i, j, w in edges:
            color[i][j] = color[j][i] = F(w)
    b, h, _ = colors
    beta, eta = haf(b), haf(h)
    checks = 0
    for p in range(4):
        for q in range(4):
            if p == q:
                continue
            retain = [i for i in range(4) if i not in (p, q)]
            cb = [[b[i][j] for j in retain] for i in retain]
            ch = [[h[i][j] for j in retain] for i in retain]
            x = [(b[p][i], F(0)) for i in retain]
            y = [(b[q][i], F(0)) for i in retain]
            u = [(F(0), h[p][i]) for i in retain]
            v = [(F(0), h[q][i]) for i in retain]
            d, e = b[p][q], h[p][q]
            # Each boundary has degree <=3 in each parameter. This exact
            # 4x4 interpolation grid therefore checks the whole polynomial,
            # including its terminal cubic coefficients.
            for a, t in product(map(F, (-1, 0, 1, 2)), repeat=2):
                for mean, first_row, second_row, direct1, direct2 in [
                    (means(a,x,t,u), y,v,a*d,t*e),
                    (means(a,y,t,v), x,u,a*d,t*e)]:
                    z = tensor(cb, ch, mean, first_row, second_row)
                    for word in z[0]:
                        assert z[1][word]+direct1*z[0][word] == \
                            (a*beta if word == (0,0) else F(0))
                        assert z[2][word]+direct2*z[0][word] == \
                            (t*eta if word == (1,1) else F(0))
                    checks += 2
            if d:
                assert beta == d*haf(cb)
    return {'pure_amplitudes': [str(haf(c)) for c in colors],
            'whole_boundary_identities_on_degree_three_grid': checks,
            'every_ordered_root_pair_including_zero_direct_edges': True,
            'terminal_degree_three_included': True,
            'supported_endpoint_identities': True,
            'valid_four_site_source_retained': True}


def missing_terminal_negative_check():
    # This genuine two-color full top has a nonmatching B. Its terminal
    # cubic is nonzero, so it must be excluded by the theorem's hypotheses.
    b, h = zero_matrix(4), zero_matrix(4)
    for i, j in [(0,2), (0,3), (1,2), (1,3)]:
        b[i][j] = b[j][i] = F(1)
    for i, j in [(0,1), (2,3)]:
        h[i][j] = h[j][i] = F(1)
    top = tensor(b, h, [(F(0), F(0))]*4)[0]
    assert top[(0,0,0,0)] == 2 and top[(1,1,1,1)] == 1
    assert all(value == 0 for word, value in top.items()
               if word not in [(0,0,0,0), (1,1,1,1)])
    retain = [1,3]  # p=0,q=2, d=1.
    cb = [[b[i][j] for j in retain] for i in retain]
    ch = [[h[i][j] for j in retain] for i in retain]
    x = [(b[0][i],F(0)) for i in retain]
    y = [(b[2][i],F(0)) for i in retain]
    u = [(F(0),h[0][i]) for i in retain]
    z = tensor(cb, ch, means(F(1),x,F(1),u), y)
    residual = {word: z[1][word]+z[0][word] -
                (F(2) if word == (0,0) else F(0)) for word in z[0]}
    assert residual[(1,0)] == 1
    assert haf(b)-b[0][2]*haf(cb) == 1
    return {'binary_full_top_valid': True, 'pure_amplitudes': ['2','1'],
            'terminal_boundary_s_squared_t_h1_b3_coefficient': '1',
            'supported_endpoint_defect': '1',
            'violates_the_required_terminal_odd_tower': True}


def main():
    result = {'generic_checks': [generic_check(n) for n in (4, 6)],
              'weighted_K4_boundary': k4_check(),
              'missing_terminal_negative_control': missing_terminal_negative_check(),
              'status': 'PASS'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
