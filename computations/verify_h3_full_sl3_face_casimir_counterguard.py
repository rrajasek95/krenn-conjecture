#!/usr/bin/env python3
"""Exact q-degree-2 counterguard for full sitewise sl3 face contraction.

The four-site coefficient/output module is identified with End(Q^3)^tensor4.
The denominator matching tensor is the identity tensor, while every desired
mixed-to-pure face polar is an off-diagonal tensor in sl3^tensor4.  Exact
trace projectors and Casimirs separate them.  The checker also computes the
Lie algebra stabilizer of four-site ternary GHZ and finds only the expected
six-dimensional abelian diagonal algebra.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json


Q = Fraction
COLORS = (0, 1, 2)
MIXED = (1, 2, 1, 1, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matrix_unit(row, column):
    return tuple(Q(int(i == row and j == column)) for i in COLORS for j in COLORS)


IDENTITY = tuple(Q(int(i == j)) for i in COLORS for j in COLORS)
ZERO_MATRIX = (Q(0),) * 9


def matrix_add(*matrices):
    return tuple(sum((matrix[index] for matrix in matrices), Q(0))
                 for index in range(9))


def matrix_scale(scalar, matrix):
    return tuple(scalar * entry for entry in matrix)


def matrix_multiply(left, right):
    return tuple(
        sum((left[3 * i + k] * right[3 * k + j] for k in COLORS), Q(0))
        for i in COLORS for j in COLORS
    )


def commutator(left, right):
    return matrix_add(matrix_multiply(left, right),
                      matrix_scale(-1, matrix_multiply(right, left)))


def trace(matrix):
    return sum((matrix[3 * i + i] for i in COLORS), Q(0))


def adjoint_projector(matrix):
    return matrix_add(matrix, matrix_scale(-trace(matrix) / 3, IDENTITY))


def casimir(matrix):
    # The central gl3 direction acts trivially by commutator, so the dual
    # matrix-unit sum equals the sl3 quadratic Casimir for the trace form.
    terms = []
    for a in COLORS:
        for b in COLORS:
            terms.append(commutator(matrix_unit(a, b),
                                    commutator(matrix_unit(b, a), matrix)))
    return matrix_add(*terms)


def sparse_add(target, source, scale=Q(1)):
    for basis, coefficient in source.items():
        target[basis] = target.get(basis, Q(0)) + scale * coefficient
        if target[basis] == 0:
            del target[basis]


def local_projector_on_unit(row, column):
    if row != column:
        return {(row, column): Q(1)}
    answer = {(row, row): Q(1)}
    for color in COLORS:
        answer[color, color] = answer.get((color, color), Q(0)) - Q(1, 3)
        if answer[color, color] == 0:
            del answer[color, color]
    return answer


def tensor_projector(tensor):
    answer = {}
    for basis, coefficient in tensor.items():
        local = [local_projector_on_unit(row, column) for row, column in basis]
        for choices in product(*(tuple(item.items()) for item in local)):
            output_basis = tuple(choice[0] for choice in choices)
            output_coefficient = coefficient
            for _unit, factor in choices:
                output_coefficient *= factor
            answer[output_basis] = answer.get(output_basis, Q(0)) + output_coefficient
            if answer[output_basis] == 0:
                del answer[output_basis]
    return answer


def identity_tensor():
    return {
        tuple((color, color) for color in word): Q(1)
        for word in product(COLORS, repeat=4)
    }


def desired_tensor(face_word):
    basis = tuple((0, color) for color in face_word)
    return {basis: Q(1)}


def face_matching_supports():
    pairings = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    all_terms = set()
    by_word = {}
    for word in product(COLORS, repeat=4):
        terms = set()
        for matching in pairings:
            term = tuple(sorted((u, v, word[u], word[v]) for u, v in matching))
            terms.add(term)
        require(len(terms) == 3, "face hafnian term collision")
        require(all_terms.isdisjoint(terms), "two words share a fine-color monomial")
        all_terms.update(terms)
        by_word[word] = terms
    require(len(by_word) == 81 and len(all_terms) == 243, "face coefficient space")
    return by_word


def rational_rank(columns, row_basis):
    matrix = [[Q(column.get(row, 0)) for column in columns] for row in row_basis]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def sl3_basis():
    basis = []
    labels = []
    for row in COLORS:
        for column in COLORS:
            if row != column:
                basis.append(matrix_unit(row, column))
                labels.append(f"E{row}{column}")
    basis.append(matrix_add(matrix_unit(0, 0), matrix_scale(-1, matrix_unit(1, 1))))
    labels.append("H01")
    basis.append(matrix_add(matrix_unit(1, 1), matrix_scale(-1, matrix_unit(2, 2))))
    labels.append("H12")
    return labels, basis


def action_on_delta(site, matrix):
    vector = {}
    for color in COLORS:
        for output in COLORS:
            coefficient = matrix[3 * output + color]
            if not coefficient:
                continue
            word = [color] * 4
            word[site] = output
            word = tuple(word)
            vector[word] = vector.get(word, Q(0)) + coefficient
            if vector[word] == 0:
                del vector[word]
    return vector


def target_stabilizer_audit():
    labels, basis = sl3_basis()
    columns = []
    column_labels = []
    for site in range(4):
        for label, matrix in zip(labels, basis):
            columns.append(action_on_delta(site, matrix))
            column_labels.append((site, label))
    words = tuple(product(COLORS, repeat=4))
    full_rank = rational_rank(columns, words)
    require(len(columns) == 32 and full_rank == 26, "four-site GHZ stabilizer rank")

    off_diagonal = [column for column, (_site, label) in zip(columns, column_labels)
                    if label.startswith("E")]
    diagonal = [column for column, (_site, label) in zip(columns, column_labels)
                if label.startswith("H")]
    require(len(off_diagonal) == 24 and rational_rank(off_diagonal, words) == 24,
            "off-diagonal generator unexpectedly stabilizes GHZ")
    require(len(diagonal) == 8 and rational_rank(diagonal, words) == 2,
            "diagonal stabilizer dimension")
    return {
        "full_sl3_dimension": 32,
        "orbit_tangent_rank": full_rank,
        "stabilizer_dimension": 32 - full_rank,
        "off_diagonal_rank": 24,
        "diagonal_action_rank": 2,
        "stabilizer_type": "abelian diagonal",
    }


def main():
    hafnians = face_matching_supports()

    # Local Casimir normalization and End=1+adj decomposition.
    require(adjoint_projector(IDENTITY) == ZERO_MATRIX, "projector did not kill identity")
    local_checks = 0
    for row in COLORS:
        for column in COLORS:
            unit = matrix_unit(row, column)
            projected = adjoint_projector(unit)
            require(casimir(unit) == matrix_scale(6, projected), "Casimir formula")
            local_checks += 1

    denominator = identity_tensor()
    require(tensor_projector(denominator) == {},
            "adjoint-fourfold projector did not kill denominator identity")

    face_records = []
    for deleted in range(1, 6):
        face_word = tuple(MIXED[site - 1] for site in range(1, 6) if site != deleted)
        desired = desired_tensor(face_word)
        require(tensor_projector(desired) == desired,
                f"face {deleted}: desired polar left adjoint-fourfold component")
        require(face_word in hafnians and len(hafnians[face_word]) == 3,
                f"face {deleted}: missing exact quadratic")
        # Each local factor is off diagonal E_(0,m), hence local Casimir 6
        # and total sitewise Casimir 24.
        for color in face_word:
            require(color in (1, 2), "face word acquired zero")
            require(casimir(matrix_unit(0, color))
                    == matrix_scale(6, matrix_unit(0, color)), "polar Casimir")
        face_records.append({
            "deleted": deleted,
            "face_word": "".join(map(str, face_word)),
            "hafnian_terms": 3,
            "denominator_component": "trivial",
            "polar_component": "adjoint^4",
            "local_casimir_eigenvalue": 6,
            "total_casimir_eigenvalue": 24,
            "equivariant_hom_dimension": 0,
        })

    stabilizer = target_stabilizer_audit()
    ledger = {
        "face_coefficient_words": len(hafnians),
        "face_q_degree_two_monomials": sum(len(value) for value in hafnians.values()),
        "end_dimension": 9 ** 4,
        "adjoint_fourfold_dimension": 8 ** 4,
        "local_casimir_checks": local_checks,
        "denominator_projector_zero": True,
        "faces": face_records,
        "target_stabilizer": stabilizer,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == "56e193d6341ac45638ae5f85a01f2f17053e4addc0d05b536534ef1f2bc9a655",
            f"ledger digest changed: {digest}")

    print("h=3 full sitewise sl3 face-Casimir counterguard: PASS")
    print("q-degree-2 coefficient module: 81 words, 243 disjoint monomials")
    print("denominator identity is trivial; five polars lie in adjoint^4")
    print("Casimir eigenvalues: denominator 0, each polar 24 total")
    print("GHZ stabilizer in sl3^4: dimension 6, abelian diagonal")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
