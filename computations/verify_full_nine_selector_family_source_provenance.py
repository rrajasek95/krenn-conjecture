#!/usr/bin/env python3
"""Lightweight exact checks for the full-nine selector provenance class."""

from itertools import product


if not __debug__:
    raise RuntimeError("run without -O: this exact checker uses assertions")


def add(left, right):
    return tuple(x + y for x, y in zip(left, right))


def sub(left, right):
    return tuple(x - y for x, y in zip(left, right))


def scale(scalar, matrix):
    return tuple(scalar * x for x in matrix)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def outer(left, right):
    return (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )


def rank_mod(vectors, prime):
    rows = [[x % prime for x in vector] for vector in vectors]
    if not rows:
        return 0
    rank = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, prime)
        rows[rank] = [(inverse * x) % prime for x in rows[rank]]
        for row in range(len(rows)):
            if row != rank and rows[row][column]:
                factor = rows[row][column]
                rows[row] = [
                    (x - factor * y) % prime
                    for x, y in zip(rows[row], rows[rank])
                ]
        rank += 1
    return rank


def omega(direct, response, prime=None):
    # d=(a,b,c,e), F=(f11,f12,f21,f22): c*f12-b*f21.
    value = direct[2] * response[1] - direct[1] * response[2]
    return value if prime is None else value % prime


def brute_diag_plus_direct(direct, response, prime):
    # The diagonal correction is free, so only the two off-diagonal cells
    # need to be matched by one multiple of d.
    return any(
        (response[1] - scalar * direct[1]) % prime == 0
        and (response[2] - scalar * direct[2]) % prime == 0
        for scalar in range(prime)
    )


def check_missing_square_criterion():
    prime = 3
    matrices = list(product(range(prime), repeat=4))
    checked = 0
    crossed = 0
    diagonal_basis = ((1, 0, 0, 0), (0, 0, 0, 1))

    for direct in matrices:
        off_direct = (direct[1], direct[2])
        base_rank = rank_mod((*diagonal_basis, direct), prime)
        assert base_rank == (3 if off_direct != (0, 0) else 2)

        for response in matrices:
            brute = brute_diag_plus_direct(direct, response, prime)
            if off_direct == (0, 0):
                closed_form = response[1] == response[2] == 0
            else:
                closed_form = omega(direct, response, prime) == 0
            assert brute == closed_form
            checked += 1

        if off_direct != (0, 0):
            for row in matrices:
                augmented_rank = rank_mod(
                    (*diagonal_basis, direct, row), prime
                )
                assert (augmented_rank == 4) == (
                    omega(direct, row, prime) != 0
                )
                crossed += 1

    return checked, crossed


def check_guard():
    # Row-major matrices.
    direct = (1, 1, 1, 2)
    h_forward = (0, 1, 0, 0)
    h_backward = (0, 0, -1, 0)
    edge = add(h_forward, h_backward)
    crossed = sub(h_forward, h_backward)
    diagonal = (1, 0, 0, 2)

    assert direct[0] * direct[3] - direct[1] * direct[2] == 1
    assert h_forward == outer((1, 0), (0, 1))
    assert h_backward == outer((0, -1), (1, 0))
    assert crossed == sub(direct, diagonal)
    assert omega(direct, crossed) == 0
    assert omega(direct, edge) == 2

    k_forward = sub(direct, h_forward)
    k_backward = sub(direct, h_backward)
    assert add(sub(k_forward, k_backward), crossed) == (0, 0, 0, 0)
    assert sub(scale(2, direct), add(k_forward, k_backward)) == edge

    # A direct-zero, zero-target selector killed by the crossed row but
    # detected by the desired edge coefficient.
    witness = (0, 1, -1, 0)
    assert dot(witness, direct) == 0
    assert witness[0] == witness[3] == 0
    assert dot(witness, crossed) == 0
    assert dot(witness, edge) == 2

    # Rank-one target-active selector from eta=(1,1), xi=(3,-2).
    selector = outer((3, -2), (1, 1))
    assert selector == (3, 3, -2, -2)
    assert selector[0] * selector[3] - selector[1] * selector[2] == 0
    assert dot(selector, direct) == 0
    assert (selector[0], selector[3]) == (3, -2)
    assert dot(selector, edge) == 5
    assert -dot(selector, add(k_forward, k_backward)) == 5

    # Formal full rows M(v_ij)=delta_ij X_i-d_ij Q in coordinates
    # (Q,X_1,X_2).  Every direct-zero selector cancels the Q coordinate.
    top_rows = (
        (-1, 1, 0),
        (-1, 0, 0),
        (-1, 0, 0),
        (-2, 0, 1),
    )
    for contraction in (selector, witness):
        image = tuple(
            sum(contraction[index] * top_rows[index][coordinate]
                for index in range(4))
            for coordinate in range(3)
        )
        assert image == (0, contraction[0], contraction[3])

    return selector, witness


def main():
    checked, crossed = check_missing_square_criterion()
    selector, witness = check_guard()
    print(f"2x2 source criterion: PASS ({checked} matrix pairs over F_3)")
    print(f"one-crossed-row criterion: PASS ({crossed} cases over F_3)")
    print(f"two-anchor/Bianchi guard: PASS (selector={selector}, witness={witness})")


if __name__ == "__main__":
    main()
