#!/usr/bin/env python3
"""Exact checks for the odd monomer-dimer exterior-rank obstruction.

Standard-library only. Run from any directory; JSON is printed to stdout.
No files are written. The all-orders proof is in the accompanying note.
"""

import argparse
import itertools
import json
import random


def words(n):
    return list(itertools.product(range(3), repeat=n))


def epsilon(a, b, c):
    if len({a, b, c}) < 3:
        return 0
    return 1 if (a, b, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


def exterior_sparse(tensor, ws, prime):
    """A(T)[a,b] = sum_c T[c] product_i epsilon(a_i,b_i,c_i)."""
    index = {w: i for i, w in enumerate(ws)}
    result = []
    for a in ws:
        row = []
        for steps in itertools.product((1, 2), repeat=len(a)):
            b = tuple((x + step) % 3 for x, step in zip(a, steps))
            c = tuple((x - step) % 3 for x, step in zip(a, steps))
            sign = (-1) ** steps.count(2)
            row.append((index[b], sign * tensor[index[c]] % prime))
        result.append(row)
    return result


def dense(rows):
    result = [[0] * len(rows) for _ in rows]
    for i, row in enumerate(rows):
        for j, value in row:
            result[i][j] = value
    return result


def determinant(matrix, prime):
    """Ordinary row elimination, independent of the Pfaffian routine."""
    a = [row[:] for row in matrix]
    result = 1
    for k in range(len(a)):
        pivot_row = next((i for i in range(k, len(a)) if a[i][k] % prime), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            result = -result
        pivot = a[k][k] % prime
        result = result * pivot % prime
        inverse = pow(pivot, -1, prime)
        for i in range(k + 1, len(a)):
            factor = a[i][k] * inverse % prime
            if factor:
                for j in range(k + 1, len(a)):
                    a[i][j] = (a[i][j] - factor * a[k][j]) % prime
            a[i][k] = 0
    return result % prime


def pfaffian(matrix, prime):
    """Skew Schur-complement elimination, using paired row/column swaps."""
    a = [row[:] for row in matrix]
    assert len(a) % 2 == 0
    result = 1
    for k in range(0, len(a), 2):
        pivot_column = next((j for j in range(k + 1, len(a)) if a[k][j] % prime), None)
        if pivot_column is None:
            return 0
        if pivot_column != k + 1:
            a[k + 1], a[pivot_column] = a[pivot_column], a[k + 1]
            for row in a:
                row[k + 1], row[pivot_column] = row[pivot_column], row[k + 1]
            result = -result
        pivot = a[k][k + 1] % prime
        result = result * pivot % prime
        inverse = pow(pivot, -1, prime)
        for i in range(k + 2, len(a)):
            for j in range(i + 1, len(a)):
                a[i][j] = (
                    a[i][j]
                    - (a[k][i] * a[k + 1][j] - a[k][j] * a[k + 1][i]) * inverse
                ) % prime
                a[j][i] = -a[i][j] % prime
    return result % prime


def rank(matrix, prime):
    a = [[x % prime for x in row] for row in matrix]
    r = 0
    for j in range(len(a[0])):
        pivot_row = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot_row is None:
            continue
        a[r], a[pivot_row] = a[pivot_row], a[r]
        inverse = pow(a[r][j], -1, prime)
        a[r] = [x * inverse % prime for x in a[r]]
        for i in range(r + 1, len(a)):
            factor = a[i][j]
            if factor:
                a[i] = [(x - factor * y) % prime for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def matchings(vertices):
    """Enumerate each partition into singleton vertices and pairs once."""
    if not vertices:
        yield (), ()
        return
    first, *tail = vertices
    for singletons, pairs in matchings(tail):
        yield (first,) + singletons, pairs
    for j, partner in enumerate(tail):
        for singletons, pairs in matchings(tail[:j] + tail[j + 1 :]):
            yield singletons, ((first, partner),) + pairs


def monomer_layers(n, prime, rng):
    ws = words(n)
    monomers = [[rng.randrange(prime) for _ in range(3)] for _ in range(n)]
    edges = {
        (i, j): [[rng.randrange(prime) for _ in range(3)] for _ in range(3)]
        for i, j in itertools.combinations(range(n), 2)
    }
    layers = {k: [0] * len(ws) for k in range(1, n + 1, 2)}
    for singletons, pairs in matchings(list(range(n))):
        layer = layers[len(singletons)]
        for index, w in enumerate(ws):
            value = 1
            for i in singletons:
                value = value * monomers[i][w[i]] % prime
            for i, j in pairs:
                value = value * edges[i, j][w[i]][w[j]] % prime
            layer[index] = (layer[index] + value) % prime
    return ws, layers


def potts_tensor():
    ws = words(5)
    es = list(itertools.combinations(range(5), 2))
    result = []
    for w in ws:
        value = 1
        for coupling, (i, j) in enumerate(es, 1):
            if w[i] == w[j]:
                value *= 1 + coupling
        result.append(value)
    return ws, result


def certificate():
    ws, tensor = potts_tensor()
    output = []
    expected = {101: (6, 39), 1009: (817, 62), 10007: (3946, 2213)}
    for prime, pair in expected.items():
        matrix = dense(exterior_sparse(tensor, ws, prime))
        assert all((matrix[i][j] + matrix[j][i]) % prime == 0
                   for i in range(len(ws)) for j in range(len(ws)))
        assert all(sum(x * y for x, y in zip(row, tensor)) % prime == 0
                   for row in matrix)
        # Check the sparse construction directly against the epsilon definition.
        for a in (ws[0], ws[17], ws[121], ws[-1]):
            ia = ws.index(a)
            for ib, b in enumerate(ws):
                if any(x == y for x, y in zip(a, b)):
                    direct = 0
                else:
                    c = tuple(3 - x - y for x, y in zip(a, b))
                    direct = tensor[ws.index(c)]
                    for x, y, z in zip(a, b, c):
                        direct *= epsilon(x, y, z)
                assert matrix[ia][ib] == direct % prime
        minor = [row[1:] for row in matrix[1:]]
        d, f = determinant(minor, prime), pfaffian(minor, prime)
        assert (d, f) == pair
        assert d != 0 and f * f % prime == d
        output.append({"prime": prime, "determinant": d, "pfaffian": f})
    return {
        "sites": 5,
        "local_dimension": 3,
        "edge_order_zero_based": list(itertools.combinations(range(5), 2)),
        "couplings": list(range(1, 11)),
        "tensor_formula": "product_(i<j) (1 + J_ij * [a_i = a_j])",
        "matrix_order": 243,
        "omitted_word": [0, 0, 0, 0, 0],
        "principal_minor_order": 242,
        "exact_complex_rank": 242,
        "proven_model_rank_upper_bound": 240,
        "modular_certificates": output,
        "all_entries_positive": min(tensor) > 0,
        "maximum_tensor_entry": max(tensor),
    }


def sanity_checks(extended):
    prime = 1009
    rng = random.Random(20260926)
    reports = []
    for n in ([3, 5, 7] if extended else [3, 5]):
        ws, layers = monomer_layers(n, prime, rng)
        assert rank(list(layers.values()), prime) == len(layers)
        for t in layers.values():
            a = exterior_sparse(t, ws, prime)
            for u in layers.values():
                assert all(sum(value * u[j] for j, value in row) % prime == 0 for row in a)
        entry = {"sites": n, "layer_span_dimension": len(layers),
                 "ordered_pair_checks": len(layers) ** 2, "all_products_zero": True}
        if n <= 5:
            loop_tensor = [sum(coefficients) % prime for coefficients in zip(*layers.values())]
            actual_rank = rank(dense(exterior_sparse(loop_tensor, ws, prime)), prime)
            bound = 3**n - (2 * ((n + 1) // 4) + 1)
            assert actual_rank <= bound
            entry.update({"loop_tensor_rank_mod_prime": actual_rank, "rank_upper_bound": bound})
        reports.append(entry)
    # The diagonal three-term tensor is locally inequivalent to the Potts tensor.
    ws = words(5)
    diagonal = [int(len(set(w)) == 1) for w in ws]
    assert rank(dense(exterior_sparse(diagonal, ws, prime)), prime) == 92
    return {"prime": prime, "samples": reports,
            "diagonal_five_site_rank_mod_prime": 92,
            "warning": "Samples check implementation; they do not prove the all-orders theorem."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extended", action="store_true", help="also check all seven-site layer pairs")
    args = parser.parse_args()
    print(json.dumps({"potts_certificate": certificate(), "sanity_checks": sanity_checks(args.extended)}, indent=2))
