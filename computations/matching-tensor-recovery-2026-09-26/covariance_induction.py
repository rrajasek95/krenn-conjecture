#!/usr/bin/env python3
"""Exact supporting checks for the all-orders covariance-rank induction.

The all-orders argument is analytic. This program checks its fixed pair
algebra over Q, its local-row witness in finite examples, a seven-site
base and auxiliary ranks, and two orders of the attachment deformation.
Requires numpy, sympy, and python-flint. Prints JSON, writes no files.
"""

from functools import lru_cache
import itertools
import json
import math

import sympy as sp
from flint import nmod_mat

import single_kernel_probes as probes
import single_source as single
from audit_pair_observation import moments

P, base = single.P, single.base
ANCHORS = [(i, 1) for i in range(4)]


def submatrix(matrix, rows, columns):
    return nmod_mat([[int(matrix[i, j]) for j in columns] for i in rows], P)


def epsilon(a, b, c):
    if len({a, b, c}) < 3:
        return 0
    return 1 if (a, b, c) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)] else -1


def pair_operator(matrix):
    words = list(itertools.product(range(3), repeat=2))
    return sp.Matrix([[sum(matrix[c, d] * epsilon(a, e, c) * epsilon(b, f, d)
                           for c, d in words) for e, f in words] for a, b in words])


def rational_minor(matrix):
    columns = list(matrix.rref()[1])
    rows = list(matrix[:, columns].T.rref()[1])
    determinant = matrix[rows, columns].det()
    assert determinant
    return {"rank": len(rows), "rows": rows, "columns": columns,
            "determinant": str(determinant)}


def pair_algebra():
    identity = sp.eye(3)
    terminal, edge = sp.diag(1, 0, 0), sp.diag(0, 1, 1)
    matrices = []
    for a, b in [(1, 0), (2, 0), (0, 1), (0, 2)]:
        matrix = sp.zeros(3)
        matrix[a, b] = 1
        matrices.append(matrix)
    d = pair_operator(identity)
    operators = [pair_operator(matrix) for matrix in matrices]
    inverse = d.inv()
    h_basis = [terminal] + matrices
    constraints = sp.Matrix.vstack(*[
        sp.Matrix.hstack(*[(inverse * op * h.reshape(9, 1))[1:, :] for h in h_basis])
        for op in operators])
    assert constraints.rank() == 4
    commutators = sp.Matrix.vstack(*[
        operators[i] * inverse * operators[j] - operators[j] * inverse * operators[i]
        for i, j in itertools.combinations(range(4), 2)])
    kernel = commutators.nullspace()
    assert commutators.rank() == 7
    assert sp.Matrix.hstack(terminal.reshape(9, 1), edge.reshape(9, 1), *kernel).rank() == 2
    reduced, _ = commutators.rref()
    last_obstruction = inverse * operators[0] * matrices[3].reshape(9, 1)
    assert last_obstruction == sp.Matrix([0, 0, 0, 0, 0, -1, 0, 0, 0])
    for op, matrix in zip(operators, matrices):
        assert inverse * op * terminal.reshape(9, 1) == sp.zeros(9, 1)
        assert inverse * op * edge.reshape(9, 1) == matrix.reshape(9, 1)
    return {"arithmetic": "rational", "first_pair_minor": rational_minor(constraints),
            "commutator_minor": rational_minor(commutators),
            "commutator_reduced_rows": [[str(a) for a in reduced.row(i)] for i in range(7)],
            "last_obstruction": [str(a) for a in last_obstruction]}


def local_row_witness(s):
    # p_i = 1 + (i+1)/(s+1), r_i = 1/p_i; the proof uses these as real rationals.
    p = [(s + 2 + i) * pow(s + 1, -1, P) % P for i in range(s)]
    r = [pow(value, -1, P) for value in p]
    rows = []
    for word in itertools.product(range(2), repeat=s):
        @lru_cache(None)
        def hafnian(sites):
            if not sites:
                return 1
            first, *tail = sites
            value = 0
            for j in tail:
                if word[first] == word[j]:
                    weight = 1 if word[j] == 0 else r[first] * r[j]
                    value += weight * hafnian(tuple(k for k in tail if k != j))
            return value % P
        row = []
        for kind in [0, 1]:
            for i in range(s):
                for colour in range(2):
                    value = 0
                    if word[i] == colour:
                        for j in range(s):
                            if j == i or word[j] != 1 - kind:
                                continue
                            remaining = tuple(k for k in range(s) if k not in (i, j))
                            ys = [k for k in remaining if word[k] == 1]
                            xs = len(remaining) - len(ys)
                            closed = (math.prod(range(1, len(ys), 2)) * math.prod(range(1, xs, 2))
                                      * math.prod(r[k] for k in ys)) % P if len(ys) % 2 == xs % 2 == 0 else 0
                            assert hafnian(remaining) == closed
                            value += (1 if kind == 0 else -1) * closed
                    row.append(value % P)
        rows.append(row)
    matrix = nmod_mat(rows, P)
    assert matrix.rank() == 4 * s - 1
    identity = [int(kind == colour) for kind in [0, 1] for _ in range(s) for colour in range(2)]
    assert (matrix * base.columns([identity])).rank() == 0
    return {"even_sites": s, "p_values": p, "minor": base.full_rank_minor(matrix),
            "hafnian_coefficients_checked_by_recursion": True}


def base_case():
    n = 7
    means, edges = probes.source(n, "outside_complete", 271941)
    tensor = moments(means, edges, P)
    words = list(itertools.product(range(3), repeat=n))
    index = {word: i for i, word in enumerate(words)}
    f3 = [word for word in words if sum(a != 0 for a in word) <= 3]
    matrix = probes.exterior_columns(tensor, n, f3)
    minor = base.full_rank_minor(matrix)
    assert minor["rank"] == len(f3) - 2
    local = []
    for j in range(n):
        rows = [i for i, word in enumerate(words) if word[j] == 0 and word.count(0) == 1]
        cols = [k for k, word in enumerate(f3) if word[j] and sum(a != 0 for a in word) == 2]
        block = submatrix(matrix, rows, cols)
        assert block.rank() == 4 * (n - 1) - 1
        local.append({"site": j, "minor": base.full_rank_minor(block)})
    # The degree-three parts of the four derivatives of the one-edge response.
    vrows = []
    for word in f3:
        sites = [i for i, a in enumerate(word) if a]
        if len(sites) != 3:
            continue
        row = []
        for i, colour in ANCHORS:
            if i not in sites or word[i] != colour:
                row.append(0)
            else:
                j, k = [site for site in sites if site != i]
                row.append(edges[j, k][word[j]][word[k]])
        vrows.append(row)
    v = nmod_mat(vrows, P)
    assert v.rank() == 4
    # Antisymmetric classes modulo A(T)F_2; parity identifies the same classes
    # modulo A(T)F_3 for this outside-only source.
    row_indices = [i for i, word in enumerate(words) if word.count(0) == 1]
    col_indices = [j for j, word in enumerate(f3) if sum(a != 0 for a in word) == 2]
    even_image = submatrix(matrix, row_indices, col_indices)
    pivots = base.pivot_columns(even_image)
    project, _, _ = base.projector([[int(even_image[i, j]) for i in range(len(row_indices))] for j in pivots])
    omega = []
    for alpha, beta in itertools.combinations(range(4), 2):
        i, colour = ANCHORS[alpha]
        derivative_top = [0] * len(words)
        for word in itertools.product([1, 2], repeat=n):
            if word[i] == colour:
                changed = word[:i] + (0,) + word[i + 1:]
                derivative_top[index[word]] = tensor[index[changed]]
        h = [0] * n
        j, b = ANCHORS[beta]
        h[j] = b
        vector = probes.exterior_columns(derivative_top, n, [tuple(h)])
        omega.append([int(vector[k, 0]) for k in row_indices])
    projected = project(base.columns(omega))
    assert projected.rank() == 6
    return {"sites": n, "seed": 271941, "source_means": means,
            "source_edges": [{"sites": list(e), "weights": block} for e, block in edges.items()],
            "f3_minor": minor, "local_row_minors": local,
            "four_response_derivative_minor": base.full_rank_minor(v),
            "six_antisymmetric_classes_minor": base.full_rank_minor(projected)}


def attach(edges, n, t):
    result = {e: [row[:] for row in edges.get(e, [[0] * 3 for _ in range(3)])]
              for e in itertools.combinations(range(n + 2), 2)}
    result[n, n + 1] = [[int(a == b and a != 0) for b in range(3)] for a in range(3)]
    for i, (site, colour) in enumerate([(n, 1), (n, 2), (n + 1, 1), (n + 1, 2)]):
        result[i, site][1][colour] = t % P
    return result


def deformation_check(old_n):
    _, edges = probes.source(old_n, "outside_complete", 271941)
    n = old_n + 2
    means = [[1, 0, 0] for _ in range(n)]
    tensors = {t: moments(means, attach(edges, old_n, t), P) for t in [0, 1, P - 1, 2]}
    t0 = tensors[0]
    t1 = [(a - b) * pow(2, -1, P) % P for a, b in zip(tensors[1], tensors[P - 1])]
    t2 = [((a + b) * pow(2, -1, P) - c) % P for a, b, c in zip(tensors[1], tensors[P - 1], t0)]
    assert [(a + 2 * b + 4 * c) % P for a, b, c in zip(t0, t1, t2)] == tensors[2]
    words = [word for word in itertools.product(range(3), repeat=n) if sum(a != 0 for a in word) <= 3]
    matrices = [probes.exterior_columns(tensor, n, words) for tensor in [t0, t1, t2]]
    minor = base.full_rank_minor(matrices[0])
    selected_rows, selected_columns = minor["rows"], minor["columns"]
    other_columns = [j for j in range(len(words)) if j not in selected_columns]
    assert len(other_columns) == 14
    rows = list(range(3**n))
    c = [submatrix(a, rows, selected_columns) for a in matrices]
    d = [submatrix(a, selected_rows, selected_columns) for a in matrices]
    h = [submatrix(a, rows, other_columns) for a in matrices]
    g = [submatrix(a, selected_rows, other_columns) for a in matrices]
    inverse = d[0].inv()
    k0 = inverse * g[0]
    k1 = inverse * (g[1] - d[1] * k0)
    k2 = inverse * (g[2] - d[1] * k1 - d[2] * k0)
    assert (h[0] - c[0] * k0).rank() == 0
    e1 = h[1] - c[1] * k0 - c[0] * k1
    e2 = h[2] - c[2] * k0 - c[1] * k1 - c[0] * k2
    kernel = base.kernel_columns(e1)
    pivots = base.pivot_columns(e1)
    project, _, _ = base.projector([[int(e1[i, j]) for i in rows] for j in pivots])
    second = project(e2 * base.columns(kernel))
    assert e1.rank() == 4 and second.rank() == 8
    rank_at_one = (matrices[0] + matrices[1] + matrices[2]).rank()
    assert len(words) - rank_at_one == 2
    return {"old_sites": old_n, "new_sites": n, "seed": 271941,
            "zeroth_minor": minor, "zeroth_kernel_dimension": 14,
            "first_obstruction_minor": base.full_rank_minor(e1),
            "second_obstruction_minor": base.full_rank_minor(second),
            "kernel_at_parameter_one": 2, "quadratic_tensor_dependence_checked": True}


if __name__ == "__main__":
    print(json.dumps({"prime": P, "pair_algebra": pair_algebra(),
                      "local_row_witnesses": [local_row_witness(s) for s in [6, 8, 10]],
                      "base": base_case(),
                      "attachment_checks": [deformation_check(n) for n in [5, 7]],
                      "scope": "Exact support for the analytic induction, not finite-order extrapolation."}, indent=2))
