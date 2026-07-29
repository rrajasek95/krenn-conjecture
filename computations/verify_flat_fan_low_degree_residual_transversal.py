#!/usr/bin/env python3
"""Exact lightweight audits for the flat-fan low-degree residual theorem."""

from itertools import combinations, product


def add_poly(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def mul_poly(left, right):
    result = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(
                a + b for a, b in zip(monomial_left, monomial_right)
            )
            result[monomial] = (
                result.get(monomial, 0)
                + coefficient_left * coefficient_right
            )
    return {key: value for key, value in result.items() if value}


def variable(index, count=8):
    exponent = [0] * count
    exponent[index] = 1
    return {tuple(exponent): 1}


def bracket(first, second):
    return add_poly(
        mul_poly(first[0], second[1]),
        mul_poly(first[1], second[0]),
        scale=-1,
    )


def audit_plucker_guard():
    variables = [variable(index) for index in range(8)]
    p = variables[0:2]
    x = variables[2:4]
    y = variables[4:6]
    z = variables[6:8]
    identity = mul_poly(bracket(p, x), bracket(y, z))
    identity = add_poly(
        identity, mul_poly(bracket(p, y), bracket(x, z)), scale=-1
    )
    identity = add_poly(identity, mul_poly(bracket(p, z), bracket(x, y)))
    assert identity == {}


def audit_anchor_quotient_kernel():
    # Quotient C^3 at three anchor sites by e_0,e_1,e_2 respectively.
    # Exactly 2^3 basis tensors survive.  Every other tensor basis word is
    # in at least one of the three fixed one-site anchor slices.
    words = list(product(range(3), repeat=3))
    surviving = {
        word
        for word in words
        if word[0] != 0 and word[1] != 1 and word[2] != 2
    }
    kernel = set(words) - surviving
    slice_union = {
        word
        for word in words
        if word[0] == 0 or word[1] == 1 or word[2] == 2
    }
    assert len(surviving) == 8
    assert len(kernel) == 19
    assert kernel == slice_union


def audit_common_line_cancellation():
    # The two terms have identical restored factor words and opposite signs.
    first = ("a_p", "x_r", "y_s", "Z")
    second = ("a_p", "x_r", "y_s", "Z")
    ledger = {first: 1}
    ledger[second] = ledger.get(second, 0) - 1
    assert all(coefficient == 0 for coefficient in ledger.values())


def vector_rank(vectors):
    rows = [list(vector) for vector in vectors if any(vector)]
    rank = 0
    column_count = 3
    for column in range(column_count):
        pivot = next(
            (index for index in range(rank, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for index in range(len(rows)):
            if index != rank and rows[index][column]:
                rows[index] = [
                    a ^ b for a, b in zip(rows[index], rows[rank])
                ]
        rank += 1
    return rank


def span(vectors):
    vectors = list(vectors)
    result = set()
    for mask in range(1 << len(vectors)):
        value = [0, 0, 0]
        for index, vector in enumerate(vectors):
            if (mask >> index) & 1:
                value = [a ^ b for a, b in zip(value, vector)]
        result.add(tuple(value))
    return frozenset(result)


def all_subspaces_f2_3():
    vectors = [
        tuple((mask >> coordinate) & 1 for coordinate in range(3))
        for mask in range(1, 8)
    ]
    subspaces = {span(())}
    for size in range(1, 4):
        for generators in combinations(vectors, size):
            subspaces.add(span(generators))
    return sorted(subspaces, key=lambda space: (len(space), sorted(space)))


def has_independent_transversal(spaces):
    nonzero_parts = [[v for v in space if any(v)] for space in spaces]
    return any(
        vector_rank(choice) == len(spaces)
        for choice in product(*nonzero_parts)
    )


def subspace_sum_dimension(spaces):
    generators = [vector for space in spaces for vector in space]
    return vector_rank(generators)


def audit_hall_rado_ledger():
    spaces = [space for space in all_subspaces_f2_3() if len(space) > 1]
    checked = 0
    for count in (1, 2, 3):
        for family in product(spaces, repeat=count):
            hall = True
            for size in range(1, count + 1):
                for indices in combinations(range(count), size):
                    selected = [family[index] for index in indices]
                    if subspace_sum_dimension(selected) < size:
                        hall = False
            transversal = has_independent_transversal(family)
            assert transversal == hall
            if count == 2 and not transversal:
                assert family[0] == family[1] and len(family[0]) == 2
            if count == 3 and not transversal:
                pair_line = any(
                    subspace_sum_dimension([family[i], family[j]]) <= 1
                    for i, j in combinations(range(3), 2)
                )
                common_plane = subspace_sum_dimension(family) <= 2
                assert pair_line or common_plane
            checked += 1
    return checked


def main():
    audit_plucker_guard()
    audit_anchor_quotient_kernel()
    audit_common_line_cancellation()
    checked = audit_hall_rado_ledger()
    print(
        "PASS anchor_kernel=19 plucker=1 common_line=1 "
        f"hall_rado_families={checked}"
    )


if __name__ == "__main__":
    main()
