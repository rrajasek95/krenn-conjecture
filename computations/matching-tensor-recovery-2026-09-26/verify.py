#!/usr/bin/env python3
"""Exact recovery and auxiliary-vertex certificates; requires python-flint.

Run with .venv/bin/python. Output is JSON; no files are written by this script.
The recovery algorithm sees only the output tensor, not its generating source.
"""

import itertools
import json
from pathlib import Path
import random
import sys

from flint import nmod_mat

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "matching-tensor-exterior-2026-09-26"))
import verify as exterior

P = 1009


def source(n, seed):
    rng = random.Random(seed)
    monomers = [[rng.randrange(P) for _ in range(3)] for _ in range(n)]
    edges = {
        (i, j): [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
        for i, j in itertools.combinations(range(n), 2)
    }
    return monomers, edges


def layers_from_source(monomers, edges):
    n = len(monomers)
    ws = exterior.words(n)
    layers = {k: [0] * len(ws) for k in range(1, n + 1, 2)}
    for unmatched, matching in exterior.matchings(list(range(n))):
        layer = layers[len(unmatched)]
        for z, w in enumerate(ws):
            value = 1
            for i in unmatched:
                value = value * monomers[i][w[i]] % P
            for i, j in matching:
                value = value * edges[i, j][w[i]][w[j]] % P
            layer[z] = (layer[z] + value) % P
    return ws, layers


def recover_product(tensor, ws):
    """Use an exterior kernel and quadratic minors to recover its product point."""
    a = nmod_mat(exterior.dense(exterior.exterior_sparse(tensor, ws, P)), P)
    kernel, dimension = a.nullspace()
    basis = [[int(kernel[i, j]) for i in range(len(ws))] for j in range(dimension)]
    monomials = list(itertools.combinations_with_replacement(range(dimension), 2))
    index = {w: i for i, w in enumerate(ws)}
    columns = list(itertools.product(range(3), repeat=len(ws[0]) - 1))
    selected, labels = [], []
    # A product tensor has rank one across the first site versus the rest.
    # In these examples this necessary condition alone isolates the product point.
    for i, j in itertools.combinations(range(3), 2):
        for c, d in itertools.combinations(columns, 2):
            ix = [index[(i,) + c], index[(i,) + d], index[(j,) + c], index[(j,) + d]]
            coefficients = []
            for h, k in monomials:
                value = basis[h][ix[0]] * basis[k][ix[3]] - basis[h][ix[1]] * basis[k][ix[2]]
                if h != k:
                    value += basis[k][ix[0]] * basis[h][ix[3]] - basis[k][ix[1]] * basis[h][ix[2]]
                coefficients.append(value % P)
            if exterior.rank(selected + [coefficients], P) > len(selected):
                selected.append(coefficients)
                labels.append([i, j, list(c), list(d)])
            if len(selected) == len(monomials) - 1:
                break
        if len(selected) == len(monomials) - 1:
            break
    assert len(selected) == len(monomials) - 1
    quadratic_kernel, quadratic_nullity = nmod_mat(selected, P).nullspace()
    assert quadratic_nullity == 1
    q = [int(quadratic_kernel[i, 0]) for i in range(len(monomials))]
    symmetric = [[0] * dimension for _ in range(dimension)]
    for value, (i, j) in zip(q, monomials):
        symmetric[i][j] = symmetric[j][i] = value
    assert nmod_mat(symmetric, P).rank() == 1
    column = next(j for j in range(dimension) if symmetric[j][j])
    coordinates = [row[column] for row in symmetric]
    product = [sum(coordinates[j] * basis[j][i] for j in range(dimension)) % P for i in range(len(ws))]
    nonzero = next(i for i, x in enumerate(product) if x)
    inverse = pow(product[nonzero], -1, P)
    product = [x * inverse % P for x in product]
    base = ws[nonzero]
    factors = []
    for i in range(len(base)):
        factor = []
        for colour in range(3):
            w = list(base)
            w[i] = colour
            factor.append(product[index[tuple(w)]])
        factors.append(factor)
    for z, w in enumerate(ws):
        value = 1
        for i, c in enumerate(w):
            value = value * factors[i][c] % P
        assert value == product[z]
    omitted = next(i for i, x in enumerate(q) if x)
    square_minor = [row[:omitted] + row[omitted + 1 :] for row in selected]
    determinant = exterior.determinant(square_minor, P)
    assert determinant
    return factors, {
        "exterior_rank": len(ws) - dimension,
        "kernel_dimension": dimension,
        "quadratic_monomial_order": monomials,
        "selected_flattening_minors": labels,
        "selected_coefficient_rows": selected,
        "coefficient_rank": len(selected),
        "omitted_coefficient_column": omitted,
        "coefficient_minor_determinant": determinant,
        "quadratic_kernel_dimension": quadratic_nullity,
        "quadratic_kernel_lift_rank": 1,
        "recovered_factors": factors,
    }


def recovery_witness(n):
    monomers, edges = source(n, 90127)
    ws, layers = layers_from_source(monomers, edges)
    tensor = [sum(values) % P for values in zip(*layers.values())]
    # The source data are used only to construct input and validate the answer.
    factors, report = recover_product(tensor, ws)
    assert all(exterior.rank([x, y], P) == 1 for x, y in zip(factors, monomers))
    expected_rank = 3**n - (2 * ((n + 1) // 4) + 1)
    assert report["exterior_rank"] == expected_rank
    report.update({
        "sites": n, "seed": 90127, "prime": P,
        "all_monomer_directions_recovered": True,
        "source_monomers": monomers,
        "source_edges": [{"sites": list(edge), "weights": value} for edge, value in edges.items()],
    })
    return report


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first, *tail = vertices
    for j, second in enumerate(tail):
        for rest in perfect_matchings(tail[:j] + tail[j + 1 :]):
            yield ((first, second),) + rest


def auxiliary_witness():
    rng = random.Random(403)
    n, h = 5, 3
    ws = exterior.words(n)
    edges = {
        (i, j): [[rng.randrange(P) for _ in range(3)] for _ in range(3)]
        for i, j in itertools.combinations(range(n), 2)
    }
    hidden_edges = {edge: rng.randrange(P) for edge in itertools.combinations(range(h), 2)}
    row_basis = [[[rng.randrange(P) for _ in range(3)] for _ in range(n)] for _ in range(3)]
    matchings = list(perfect_matchings(list(range(n + h))))
    reports = []
    for r in (1, 2):
        coefficients = [[rng.randrange(P) for _ in range(r)] for _ in range(h)]
        coupling = [
            [[sum(coefficients[z][q] * row_basis[q][i][a] for q in range(r)) % P for a in range(3)]
             for i in range(n)] for z in range(h)
        ]
        tensor = []
        for w in ws:
            total = 0
            for matching in matchings:
                value = 1
                for i, j in matching:
                    if j < n:
                        factor = edges[i, j][w[i]][w[j]]
                    elif i < n:
                        factor = coupling[j - n][i][w[i]]
                    else:
                        factor = hidden_edges[i - n, j - n]
                    value = value * factor % P
                total = (total + value) % P
            tensor.append(total)
        matrix = exterior.dense(exterior.exterior_sparse(tensor, ws, P))
        rank = nmod_mat(matrix, P).rank()
        minor = [row[1:] for row in matrix[1:]]
        determinant = int(nmod_mat(minor, P).det())
        if r == 1:
            assert rank == 240 and determinant == 0
        else:
            assert rank == 242 and determinant == 350
            assert exterior.pfaffian(minor, P) ** 2 % P == determinant
        assert exterior.rank([sum(row, []) for row in coupling], P) == r
        reports.append({"coupling_rank": r, "exterior_rank": rank,
                        "principal_minor_order": 242, "omitted_word": [0] * 5,
                        "principal_minor_determinant": determinant,
                        "coupling_coefficients": coefficients})
    return {
        "prime": P, "seed": 403, "visible_sites": n, "hidden_sites": h,
        "source_visible_edges": [{"sites": list(edge), "weights": value} for edge, value in edges.items()],
        "source_hidden_edges": [{"sites": list(edge), "weight": value} for edge, value in hidden_edges.items()],
        "coupling_basis": row_basis,
        "cases": reports,
        "lifting_note": "Over the integers, form coupling rows as unreduced sums of basis rows with the listed coefficients. Reductions occur only in certificate arithmetic.",
    }


if __name__ == "__main__":
    print(json.dumps({
        "recovery": [recovery_witness(5), recovery_witness(7)],
        "auxiliary_vertices": auxiliary_witness(),
        "status": "Exact finite-field witnesses plus proofs in the accompanying note; no Lean formalization.",
    }, indent=2))
