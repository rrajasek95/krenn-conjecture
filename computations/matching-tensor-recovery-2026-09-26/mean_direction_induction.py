#!/usr/bin/env python3
"""Exact checks for all-orders recovery of local mean directions.

The theorem is analytic; these checks certify its five-site base, all nine
projective charts of the two-site lemma, the first-order attachment formula,
and tangent ranks at explicit five-, seven-, and nine-site sources.
The nine-site tangent check is not a global uniqueness certificate.

Requires numpy, sympy, and python-flint. Prints JSON, writes no files.
"""

import itertools
import json
import random

import sympy as sp
from flint import nmod_mat

import single_source as single
from audit_pair_observation import moments
from audit_single_source import exterior_matrix

P, base = single.P, single.base
SLOTS = [(0, 1, 0, 0), (0, 2, 0, 1), (1, 1, 0, 2),
         (1, 2, 1, 1), (2, 1, 1, 2)]


def pair_matrices():
    matrices = []
    for _, _, side, colour in SLOTS:
        matrix = sp.zeros(3)
        matrix[colour, 0] = 1 if side == 0 else 0
        if side == 1:
            matrix[0, colour] = 1
        matrices.append(matrix)
    return matrices


def quotient(pivot, coordinates):
    other = [i for i in range(3) if i != pivot]
    matrix = sp.zeros(2, 3)
    for row, (i, value) in enumerate(zip(other, coordinates)):
        matrix[row, i], matrix[row, pivot] = 1, -value
    return matrix


def symbolic_pair_check():
    variables = sp.symbols("u1 u2 v1 v2")
    matrices = pair_matrices()
    assert sp.Matrix.hstack(*[m.reshape(9, 1) for m in matrices]).rank() == 5
    charts = []
    for a, b in itertools.product(range(3), repeat=2):
        left, right = quotient(a, variables[:2]), quotient(b, variables[2:])
        covariance = list(left * right.T)
        equations = []
        for matrix in matrices:
            image = list(left * matrix * right.T)
            equations.extend(sp.expand(covariance[i] * image[j] - covariance[j] * image[i])
                             for i, j in itertools.combinations(range(4), 2))
        groebner = sp.groebner(equations, *variables, domain=sp.QQ)
        expected = list(variables) if (a, b) == (0, 0) else [sp.Integer(1)]
        assert list(groebner) == expected
        charts.append({"line_pivots": [a, b], "reduced_groebner_basis": [str(g) for g in groebner]})
    # At the true lines, quotient a two-by-two matrix by the line C I_2.
    left, right = quotient(0, variables[:2]), quotient(0, variables[2:])
    residuals = []
    for matrix in matrices:
        image = left * matrix * right.T
        residuals.extend([image[0, 1], image[1, 0], image[0, 0] - image[1, 1]])
    jacobian = sp.Matrix(residuals).jacobian(variables).subs(dict.fromkeys(variables, 0))
    rows = list(jacobian.T.rref()[1])
    assert len(rows) == 4
    determinant = jacobian[rows, :].det()
    assert abs(determinant) == 1
    return {"arithmetic": "rational", "matrix_span_dimension": 5,
            "projective_charts": charts, "reduced_pair_jacobian_rank": 4,
            "selected_pair_jacobian_rows": rows,
            "selected_pair_jacobian_determinant": int(determinant)}


def base_source():
    rng = random.Random(90127)
    means = [[rng.randrange(P) for _ in range(3)] for _ in range(5)]
    edges = {e: [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
             for e in itertools.combinations(range(5), 2)}
    inverses = []
    for mean in means:
        pivot = next(i for i, value in enumerate(mean) if value)
        vectors = [mean] + [[int(a == b) for a in range(3)] for b in range(3) if b != pivot]
        inverses.append(base.columns(vectors).inv())
    normalized = {}
    for (i, j), block in edges.items():
        changed = inverses[i] * nmod_mat(block, P) * inverses[j].transpose()
        normalized[i, j] = [[int(value) for value in row] for row in changed.tolist()]
    return normalized


def attach(edges, old_n, parameter):
    result = {e: [row[:] for row in edges.get(e, [[0] * 3 for _ in range(3)])]
              for e in itertools.combinations(range(old_n + 2), 2)}
    result[old_n, old_n + 1] = [[int(a == b and a != 0) for b in range(3)] for a in range(3)]
    for i, a, side, colour in SLOTS:
        result[i, old_n + side][a][colour] = parameter % P
    return result


def direction_matrix(tensor, n):
    words = list(itertools.product(range(3), repeat=n))
    index = {word: i for i, word in enumerate(words)}
    # Minus this matrix is the Jacobian of the all-quotient tensor at e_0.
    rows = [[tensor[index[word[:i] + (0,) + word[i + 1:]]] if word[i] == a else 0
             for i in range(n) for a in [1, 2]]
            for word in itertools.product([1, 2], repeat=n)]
    return nmod_mat(rows, P)


def attachment_formula(old_edges, old_n, old_tensor):
    n = old_n + 2
    tensors = {t: moments([[1, 0, 0] for _ in range(n)], attach(old_edges, old_n, t), P)
               for t in [0, 1, P - 1]}
    inv_two = pow(2, -1, P)
    first = [(a - b) * inv_two % P for a, b in zip(tensors[1], tensors[P - 1])]
    f = direction_matrix(old_tensor, old_n)
    pair = pair_matrices()
    entries = 0
    for row, word in enumerate(itertools.product([1, 2], repeat=old_n)):
        index = sum(a * 3**(old_n - 1 - i) for i, a in enumerate(word))
        for a, b in itertools.product(range(3), repeat=2):
            wanted = sum(int(f[row, 2 * i + colour - 1]) * int(matrix[a, b])
                         for (i, colour, _, _), matrix in zip(SLOTS, pair)) % P
            actual_index = 9 * index + 3 * a + b
            assert first[actual_index] == wanted
            # After projecting all old sites, the identity is exactly linear.
            assert tensors[0][actual_index] == 0
            assert tensors[1][actual_index] == wanted
            assert tensors[P - 1][actual_index] == -wanted % P
            entries += 1
    return tensors[1], {"old_sites": old_n, "new_sites": n,
                        "old_quotient_entries_checked": entries,
                        "first_order_identity_passed": True,
                        "old_projection_is_exactly_linear": True}


def direction_report(tensor, n, global_check):
    matrix = direction_matrix(tensor, n)
    assert matrix.rank() == 2 * n
    report = {"sites": n, "direction_jacobian_minor": base.full_rank_minor(matrix)}
    if global_check:
        words = list(itertools.product(range(3), repeat=n))
        exterior = nmod_mat(exterior_matrix(tensor, n, P).tolist(), P)
        kernel = base.kernel_columns(exterior)
        terminal, recovered = single.many.recover_terminal(kernel, words, 1, all_sites=True)
        assert terminal[0][0] and not any(terminal[0][1:])
        report.update({"exterior_kernel_dimension": len(kernel),
                       "unique_reduced_product_certificate": recovered})
    else:
        report["scope"] = "Local simplicity only; no full exterior kernel computed."
    return report


def run():
    symbolic = symbolic_pair_check()
    edges = base_source()
    tensor = moments([[1, 0, 0] for _ in range(5)], edges, P)
    source = [{"sites": list(e), "weights": block} for e, block in edges.items()]
    reports = [direction_report(tensor, 5, True)]
    attachments = []
    for old_n in [5, 7]:
        tensor, report = attachment_formula(edges, old_n, tensor)
        attachments.append(report)
        edges = attach(edges, old_n, 1)
        reports.append(direction_report(tensor, old_n + 2, old_n == 5))
    return {"prime": P, "base_seed": 90127, "base_means": [[1, 0, 0]] * 5,
            "base_edges": source, "attachment_parameter": 1,
            "coupling_slots": [list(slot) for slot in SLOTS],
            "symbolic_pair_lemma": symbolic, "attachment_checks": attachments,
            "direction_checks": reports,
            "all_orders_scope": "The proof uses analytic induction; finite checks do not extrapolate global uniqueness."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
