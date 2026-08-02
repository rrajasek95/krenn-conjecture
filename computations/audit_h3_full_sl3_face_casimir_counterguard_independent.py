#!/usr/bin/env python3
"""Independent exact audit of the full-sitewise sl3 face counterguard.

No code or computed data are imported from the primary checker.  This audit
uses an explicit traceless sl3 basis, inverts its trace-form Gram matrix,
computes the CE degree-zero Casimir homotopy in the correct direction, and
finds the full exact and projective GHZ stabilizers by rational nullspaces.
"""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


Q = Fraction
COLOURS = (0, 1, 2)
SITES = tuple(range(4))
MIXED = (1, 2, 1, 1, 2)
EXPECTED_DIGEST = "c69a488e752e02cb993978f06da7b44793a5eeb341bdc49a79cb03d8e915f1db"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def unit(row, column):
    return tuple(Q(int(i == row and j == column))
                 for i in COLOURS for j in COLOURS)


ZERO = (Q(0),) * 9
IDENTITY = tuple(Q(int(i == j)) for i in COLOURS for j in COLOURS)


def add(*matrices):
    return tuple(sum((matrix[index] for matrix in matrices), Q(0))
                 for index in range(9))


def scale(scalar, matrix):
    return tuple(scalar * entry for entry in matrix)


def multiply(left, right):
    return tuple(
        sum((left[3 * i + k] * right[3 * k + j] for k in COLOURS), Q(0))
        for i in COLOURS for j in COLOURS
    )


def bracket(left, right):
    return add(multiply(left, right), scale(-1, multiply(right, left)))


def trace(matrix):
    return sum((matrix[3 * i + i] for i in COLOURS), Q(0))


def trace_form(left, right):
    return trace(multiply(left, right))


def sl3_basis():
    labels = []
    basis = []
    for row in COLOURS:
        for column in COLOURS:
            if row == column:
                continue
            labels.append(f"E{row}{column}")
            basis.append(unit(row, column))
    labels.extend(("H01", "H12"))
    basis.extend((
        add(unit(0, 0), scale(-1, unit(1, 1))),
        add(unit(1, 1), scale(-1, unit(2, 2))),
    ))
    require(len(basis) == 8 and all(trace(item) == 0 for item in basis),
            "sl3 basis")
    return tuple(labels), tuple(basis)


def invert(matrix):
    size = len(matrix)
    work = [
        [Q(value) for value in row]
        + [Q(int(i == j)) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        require(pivot is not None, "singular matrix")
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * pivot_entry
                         for entry, pivot_entry
                         in zip(work[row], work[column])]
    return tuple(tuple(row[size:]) for row in work)


LABELS, BASIS = sl3_basis()
GRAM = tuple(tuple(trace_form(left, right) for right in BASIS) for left in BASIS)
GRAM_INVERSE = invert(GRAM)


def casimir(matrix):
    answer = ZERO
    for i, left in enumerate(BASIS):
        for j, right in enumerate(BASIS):
            coefficient = GRAM_INVERSE[i][j]
            if coefficient:
                answer = add(answer, scale(
                    coefficient, bracket(left, bracket(right, matrix))
                ))
    return answer


def adjoint_part(matrix):
    return add(matrix, scale(-trace(matrix) / 3, IDENTITY))


def rref(rows):
    work = [[Q(value) for value in row] for row in rows]
    width = len(work[0]) if work else 0
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * pivot_entry
                         for entry, pivot_entry
                         in zip(work[row], work[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(rows):
    return len(rref(rows)[1])


def nullspace(rows):
    reduced, pivots = rref(rows)
    width = len(rows[0]) if rows else 0
    free = tuple(column for column in range(width) if column not in pivots)
    vectors = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        vectors.append(tuple(vector))
    return tuple(vectors)


@lru_cache(maxsize=None)
def pairings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in pairings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def face_module_audit():
    coefficient_supports = {}
    all_monomials = set()
    for word in product(COLOURS, repeat=4):
        support = {
            tuple(sorted((left, right, word[left], word[right])
                         for left, right in matching))
            for matching in pairings(SITES)
        }
        require(len(support) == 3, "face hafnian support size")
        require(all_monomials.isdisjoint(support),
                "two coefficient words share a monomial")
        all_monomials.update(support)
        coefficient_supports[word] = support
    require(len(coefficient_supports) == 81 and len(all_monomials) == 243,
            "face coefficient module dimension")

    # The map (coefficient word c, output word d) -> tensor matrix units
    # (E_{d_x,c_x}) is checked as a literal bijection of the 6561 bases.
    end_bases = {
        tuple(zip(output, coefficient))
        for coefficient in coefficient_supports
        for output in product(COLOURS, repeat=4)
    }
    require(len(end_bases) == 9 ** 4 == 6561,
            "End(V)^tensor4 basis identification is not bijective")

    denominator_basis = {
        tuple((colour, colour) for colour in word)
        for word in product(COLOURS, repeat=4)
    }
    require(len(denominator_basis) == 81,
            "identity tensor expansion changed")

    faces = []
    for deleted in range(1, 6):
        word = tuple(MIXED[site - 1] for site in range(1, 6)
                     if site != deleted)
        tensor_basis = tuple((0, colour) for colour in word)
        require(tensor_basis in end_bases, "polar left the End basis")
        require(all(row != column for row, column in tensor_basis),
                "polar acquired a non-adjoint local factor")
        require(len(coefficient_supports[word]) == 3,
                "polar coefficient lost a matching term")
        faces.append({
            "deleted": deleted,
            "word": "".join(map(str, word)),
            "matching_terms": 3,
            "all_four_factors_off_diagonal": True,
        })

    return {
        "coefficient_words": len(coefficient_supports),
        "coefficient_monomials": len(all_monomials),
        "end_tensor_basis": len(end_bases),
        "denominator_identity_terms": len(denominator_basis),
        "faces": faces,
    }


def sparse_add(target, source, factor=Q(1)):
    for key, value in source.items():
        target[key] = target.get(key, Q(0)) + factor * value
        if not target[key]:
            del target[key]


def act_on_tensor(site, matrix, tensor):
    answer = {}
    for basis, coefficient in tensor.items():
        row, column = basis[site]
        for output in COLOURS:
            left_coefficient = matrix[3 * output + row]
            if left_coefficient:
                changed = list(basis)
                changed[site] = (output, column)
                answer[tuple(changed)] = (
                    answer.get(tuple(changed), Q(0))
                    + coefficient * left_coefficient
                )
            right_coefficient = matrix[3 * column + output]
            if right_coefficient:
                changed = list(basis)
                changed[site] = (row, output)
                answer[tuple(changed)] = (
                    answer.get(tuple(changed), Q(0))
                    - coefficient * right_coefficient
                )
    return {key: value for key, value in answer.items() if value}


def total_casimir(tensor):
    answer = {}
    for site in SITES:
        for i, left in enumerate(BASIS):
            for j, right in enumerate(BASIS):
                coefficient = GRAM_INVERSE[i][j]
                if coefficient:
                    sparse_add(
                        answer,
                        act_on_tensor(site, left,
                                      act_on_tensor(site, right, tensor)),
                        coefficient,
                    )
    return answer


def representation_and_ce_audit():
    local_checks = 0
    for row in COLOURS:
        for column in COLOURS:
            matrix = unit(row, column)
            require(casimir(matrix) == scale(6, adjoint_part(matrix)),
                    "explicit sl3-dual Casimir normalization")
            local_checks += 1

    denominator = {
        tuple((colour, colour) for colour in word): Q(1)
        for word in product(COLOURS, repeat=4)
    }
    require(total_casimir(denominator) == {},
            "total Casimir did not kill the identity tensor")
    for site in SITES:
        for generator in BASIS:
            require(act_on_tensor(site, generator, denominator) == {},
                    "denominator is not sitewise trivial")

    polar_basis = ((0, 1), (0, 2), (0, 1), (0, 2))
    polar = {polar_basis: Q(1)}
    polar_casimir = total_casimir(polar)
    require(polar_casimir == {polar_basis: Q(24)},
            "four-site polar Casimir eigenvalue")

    # A local adjoint has no invariant vector: stack [B_i,X] for all eight
    # B_i, with X expressed in the traceless basis, and obtain rank eight.
    invariant_rows = []
    for generator in BASIS:
        commutator_columns = [bracket(generator, candidate) for candidate in BASIS]
        invariant_rows.extend([
            [column[coordinate] for column in commutator_columns]
            for coordinate in range(9)
        ])
    local_invariant_rank = rank(invariant_rows)
    require(local_invariant_rank == 8,
            "adjoint unexpectedly has a local invariant")

    # CE direction at degree zero.  With dz(X)=rho(X)z, the standard
    # Casimir numerator sum rho(x_i)dz(x^i) is 24z.  Dividing by 24 gives
    # h_CE(dz)=z.  There is no C^{-1}, so this is not z=d_CE(previous).
    nonzero_orbit_directions = sum(
        bool(act_on_tensor(site, generator, polar))
        for site in SITES for generator in BASIS
    )
    require(nonzero_orbit_directions > 0, "polar became invariant")
    h_d_z = {basis: coefficient / 24
             for basis, coefficient in polar_casimir.items()}
    require(h_d_z == polar, "CE Casimir homotopy has the wrong direction")

    return {
        "trace_form_gram_rank": rank(GRAM),
        "local_matrix_unit_checks": local_checks,
        "local_adjoint_eigenvalue": 6,
        "total_polar_eigenvalue": 24,
        "denominator_total_eigenvalue": 0,
        "local_adjoint_invariant_dimension": 8 - local_invariant_rank,
        "hom_trivial_to_adjoint_external_fourfold": 0,
        "polar_nonzero_orbit_directions": nonzero_orbit_directions,
        "ce_degree_minus_one_dimension": 0,
        "ce_degree_zero_boundary": False,
        "ce_homotopy_identity": "h_CE(d_CE z)=z",
    }


def ghz_action(site, matrix):
    answer = {}
    for colour in COLOURS:
        for output in COLOURS:
            coefficient = matrix[3 * output + colour]
            if not coefficient:
                continue
            word = [colour] * 4
            word[site] = output
            word = tuple(word)
            answer[word] = answer.get(word, Q(0)) + coefficient
            if not answer[word]:
                del answer[word]
    return answer


def columns_to_rows(columns, row_basis):
    return [[column.get(row, Q(0)) for column in columns] for row in row_basis]


def coefficient_matrices(vector):
    matrices = []
    for site in SITES:
        matrix = ZERO
        for basis_index, generator in enumerate(BASIS):
            matrix = add(matrix, scale(vector[8 * site + basis_index], generator))
        matrices.append(matrix)
    return tuple(matrices)


def stabilizer_audit():
    words = tuple(product(COLOURS, repeat=4))
    columns = [
        ghz_action(site, generator)
        for site in SITES for generator in BASIS
    ]
    action_rows = columns_to_rows(columns, words)
    orbit_rank = rank(action_rows)
    kernel = nullspace(action_rows)
    require(orbit_rank == 26 and len(kernel) == 6,
            "exact GHZ stabilizer dimension")

    off_diagonal_indices = tuple(
        8 * site + basis_index
        for site in SITES for basis_index in range(6)
    )
    require(all(all(vector[index] == 0 for index in off_diagonal_indices)
                for vector in kernel),
            "GHZ stabilizer acquired an off-diagonal direction")

    stabilizer_matrices = [coefficient_matrices(vector) for vector in kernel]
    for matrices in stabilizer_matrices:
        require(all(matrix[3 * i + j] == 0
                    for matrix in matrices
                    for i in COLOURS for j in COLOURS if i != j),
                "stabilizer basis is not diagonal")
        require(all(trace(matrix) == 0 for matrix in matrices),
                "stabilizer basis left sl3")
    for left in stabilizer_matrices:
        for right in stabilizer_matrices:
            require(all(bracket(left[site], right[site]) == ZERO for site in SITES),
                    "GHZ stabilizer is not abelian")

    off_columns = [columns[8 * site + index]
                   for site in SITES for index in range(6)]
    diagonal_columns = [columns[8 * site + index]
                        for site in SITES for index in (6, 7)]
    require(rank(columns_to_rows(off_columns, words)) == 24,
            "off-diagonal GHZ action rank")
    require(rank(columns_to_rows(diagonal_columns, words)) == 2,
            "diagonal GHZ action rank")

    # Independent diagonal-parameter count: 12 lambdas, four site traces
    # and three colour sums.  The seven displayed equations have rank six.
    diagonal_constraints = []
    for site in SITES:
        diagonal_constraints.append([
            Q(int(variable_site == site))
            for variable_site in SITES for _colour in COLOURS
        ])
    for colour in COLOURS:
        diagonal_constraints.append([
            Q(int(variable_colour == colour))
            for _site in SITES for variable_colour in COLOURS
        ])
    constraint_rank = rank(diagonal_constraints)
    require(constraint_rank == 6 and 12 - constraint_rank == len(kernel),
            "diagonal constraint count disagrees with action kernel")

    # The exact and projective infinitesimal stabilizers coincide in sl3^4.
    # Adjoin -Delta as a possible scalar direction; it raises orbit rank by
    # one, and every augmented-kernel vector has scalar coefficient zero.
    delta = {tuple([colour] * 4): Q(1) for colour in COLOURS}
    augmented_rows = columns_to_rows(columns + [
        {word: -value for word, value in delta.items()}
    ], words)
    projective_rank = rank(augmented_rows)
    projective_kernel = nullspace(augmented_rows)
    require(projective_rank == 27 and len(projective_kernel) == 6,
            "projective GHZ stabilizer dimension")
    require(all(vector[-1] == 0 for vector in projective_kernel),
            "a nonzero infinitesimal GHZ scaling appeared")

    return {
        "ambient_sl3_fourfold_dimension": len(columns),
        "orbit_tangent_rank": orbit_rank,
        "exact_stabilizer_dimension": len(kernel),
        "off_diagonal_action_rank": 24,
        "diagonal_action_rank": 2,
        "diagonal_constraint_rank": constraint_rank,
        "pairwise_brackets_zero": True,
        "stabilizer_type": "abelian diagonal",
        "projective_augmented_rank": projective_rank,
        "projective_stabilizer_dimension": len(projective_kernel),
        "projective_scaling_direction": False,
    }


def main():
    ledger = {
        "module": face_module_audit(),
        "representation_and_ce": representation_and_ce_audit(),
        "ghz_stabilizer": stabilizer_audit(),
        "scope": {
            "fixed_q_degree_two_face_denominator_only": True,
            "rules_out_full_source_complex": False,
            "rules_out_non_equivariant_cross_word_repairs": False,
            "rules_out_relative_or_spencer_lifts": False,
        },
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST,
            f"independent ledger changed: {digest}")
    print("independent h=3 full-sitewise sl3 face-Casimir audit: PASS")
    print("End(V)^tensor4 basis 6561; denominator trivial, five polars in ad^4")
    print("explicit sl3 trace-dual Casimir: local 6, four-site polar 24")
    print("CE direction: h_CE(d_CE z)=z; degree-zero z is not a CE boundary")
    print("exact/projective GHZ stabilizer: dimension 6, abelian diagonal")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
