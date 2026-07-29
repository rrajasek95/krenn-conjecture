#!/usr/bin/env python3
"""Discover direct-free maximal-minor covers on the CCE and CCB cells."""

from __future__ import annotations

import argparse
import subprocess

import numpy as np
import sympy as sp

import explore_live_three_zero_minimal_three_extra_response as response
import verify_live_three_zero_minimal_three_extra_boundary_low_cells as low


DEFAULT_PRIME = 1_000_003
R = sp.Rational

FOUR_POINTS = (
    (0, 0, 0, 0),
    (-1, -1, -1, -1),
    (-2, -2, -2, -2),
    (-3, -3, -3, -3),
    (1, 1, 1, 1),
    (R(-1, 2), R(-1, 2), R(-1, 2), R(-1, 2)),
    (0, -1, -2, -3),
    (-3, -2, -1, 0),
    (1, -1, 1, -1),
    (-1, 1, -1, 1),
) + tuple(
    tuple(value if index == axis else 0 for index in range(4))
    for axis in range(4)
    for value in (-1, -2, -3, R(-1, 2), 1)
)

FIVE_POINTS = (
    (0, 0, 0, 0, 0),
    (-1, -1, -1, -1, -1),
    (-2, -2, -2, -2, -2),
    (-3, -3, -3, -3, -3),
    (1, 1, 1, 1, 1),
    (R(-1, 2),) * 5,
    (0, -1, -2, -3, 1),
    (-3, -2, -1, 0, 1),
) + tuple(
    tuple(value if index == axis else 0 for index in range(5))
    for axis in range(5)
    for value in (-1, -2, -3, R(-1, 2), 1)
)


def modular_value(value, prime):
    value = R(value)
    return int(value.p) * pow(int(value.q), prime - 2, prime) % prime


def selected_support(
    cell, point, tie_seed=None, prime=DEFAULT_PRIME, raw_modular=False
):
    charts, substitutions, ordered_indices, variables = low.cell_data(cell)
    values = [0] * 6
    for index, value in zip(ordered_indices, point):
        values[index] = (
            int(value) % prime if raw_modular else modular_value(value, prime)
        )
    response.PRIME = prime
    selected = response.select_labels(
        charts,
        tuple(values),
        excluded_sources=((0, 1),),
        tie_seed=tie_seed,
    )
    assert len(selected) == 19
    labels = tuple(label for _row_support, label in selected)
    assert all(label[1:] != (0, 1) for label in labels)
    return exact_support(charts, substitutions, variables, labels)


def exact_support(charts, substitutions, variables, labels):
    determinant = response.flint_restricted_determinant(
        charts, labels, substitutions
    )
    return low.squarefree_support(determinant, variables)


def modular_rank(charts, labels, actual_values, prime):
    response.PRIME = prime
    row = response.numeric_row_engine(
        response.numeric_matrices(charts, actual_values)
    )
    matrix = [row(label) for label in labels]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (index for index in range(rank, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], prime - 2, prime)
        matrix[rank] = [value*inverse % prime for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or not matrix[index][column]:
                continue
            scale = matrix[index][column]
            matrix[index] = [
                (value-scale*pivot_value) % prime
                for value, pivot_value in zip(matrix[index], matrix[rank])
            ]
        rank += 1
    return rank


def generically_selected_modular_labels(cell, point, target_prime):
    charts, substitutions, ordered_indices, variables = low.cell_data(cell)
    target_values = [0] * 6
    for index, value in zip(ordered_indices, point):
        target_values[index] = int(value) % target_prime

    # Lift the same finite-field point to several ordinary integer points and
    # select the sparse basis over the large default prime.  Retain only a
    # basis whose reduction is still nonsingular at the target point.
    for lift in range(1):
        lifted_values = target_values[:]
        for position, index in enumerate(ordered_indices):
            lifted_values[index] += target_prime*lift*(position + 1)
        response.PRIME = DEFAULT_PRIME
        selected = response.select_labels(
            charts,
            tuple(value % DEFAULT_PRIME for value in lifted_values),
            excluded_sources=((0, 1),),
        )
        if len(selected) != 19:
            continue
        labels = tuple(label for _row_support, label in selected)
        if modular_rank(
            charts, labels, tuple(target_values), target_prime
        ) == 19:
            return sum(row_support for row_support, _label in selected), labels
    return None


def selected_modular_cut(cell, zeros, target_prime):
    charts, substitutions, _ordered_indices, variables = low.cell_data(cell)
    sample_indices = np.linspace(
        0, len(zeros) - 1, min(128, len(zeros)), dtype=int
    )
    candidates = []
    for index in sample_indices:
        point = tuple(map(int, zeros[index]))
        result = generically_selected_modular_labels(
            cell, point, target_prime
        )
        if result is not None:
            complexity, labels = result
            candidates.append((complexity, point, labels))
    if candidates:
        complexity, point, labels = min(candidates, key=lambda item: item[0])
        print(
            cell, "generic cut", target_prime, point,
            "row complexity", complexity, flush=True,
        )
        return point, exact_support(charts, substitutions, variables, labels)
    point = tuple(map(int, zeros[0]))
    print(cell, "small-prime cut", target_prime, point, flush=True)
    return point, selected_support(
        cell, point, prime=target_prime, raw_modular=True
    )


def values_at_points(polynomial, variables, points, prime):
    integral = sp.Poly(
        polynomial, *variables, domain=sp.QQ
    ).clear_denoms()[1]
    modular = sp.Poly(integral.as_expr(), *variables, modulus=prime)
    values = np.zeros(len(points), dtype=np.int64)
    for monomial, coefficient in modular.terms():
        term = np.full(len(points), int(coefficient) % prime, dtype=np.int64)
        for index, degree in enumerate(monomial):
            for _power in range(degree):
                term = term * points[:, index] % prime
        values = (values + term) % prime
    return values


def finite_field_zeros(polynomials, variables, prime):
    grid = np.indices((prime,) * len(variables), dtype=np.int64)
    points = grid.reshape(len(variables), -1).T
    mask = np.ones(len(points), dtype=bool)
    for polynomial in polynomials:
        mask &= values_at_points(polynomial, variables, points, prime) == 0
        if not mask.any():
            break
    return points[mask]


def singular_unit(polynomials, variables):
    generators = []
    for polynomial in polynomials:
        integral = sp.Poly(
            polynomial, *variables, domain=sp.QQ
        ).clear_denoms()[1].as_expr()
        generators.append(str(sp.expand(integral)).replace("**", "^"))
    names = ",".join(map(str, variables))
    script = (
        f"ring r=0,({names}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "ideal G=std(I);\n"
        'if (size(G)==1 && G[1]==1) { "UNIT"; } '
        'else { "NONUNIT"; dim(G); size(G); }\n'
    )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        capture_output=True, check=True, timeout=600,
    )
    if "?" in result.stdout:
        raise RuntimeError(result.stdout)
    return result.stdout.strip()


def singular_minimal_primes(polynomials, variables):
    generators = []
    for polynomial in polynomials:
        integral = sp.Poly(
            polynomial, *variables, domain=sp.QQ
        ).clear_denoms()[1].as_expr()
        generators.append(str(sp.expand(integral)).replace("**", "^"))
    names = ",".join(map(str, variables))
    script = (
        'LIB "primdec.lib";\n'
        f"ring r=0,({names}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "list P=minAssGTZ(I);\n"
        '"MINIMAL_PRIMES"; size(P); P;\n'
    )
    result = subprocess.run(
        ("Singular", "-q"), input=script, text=True,
        capture_output=True, check=True, timeout=1200,
    )
    if "?" in result.stdout:
        raise RuntimeError(result.stdout)
    return result.stdout.strip()


def modular_close(cell, maximum_new=80):
    _charts, _substitutions, _indices, variables = low.cell_data(cell)
    points = FOUR_POINTS if len(variables) == 4 else FIVE_POINTS
    base_points = points if len(variables) == 4 else points[:8]
    polynomials = []
    for index, point in enumerate(base_points):
        print(cell, "base", index + 1, point, flush=True)
        polynomial = selected_support(cell, point)
        if polynomial not in polynomials:
            polynomials.append(polynomial)
    print(cell, "base supports", len(polynomials), flush=True)

    primes = (
        (17, 19, 23, 29, 31, 37, 41, 43)
        if len(variables) == 4
        else (7, 11, 13, 17, 19, 23)
    )
    new_points = []
    for prime in primes:
        zeros = finite_field_zeros(polynomials, variables, prime)
        print(cell, "prime", prime, "zeros", len(zeros), flush=True)
        exhausted = True
        while len(zeros):
            point, polynomial = selected_modular_cut(cell, zeros, prime)
            values = values_at_points(polynomial, variables, zeros, prime)
            if polynomial not in polynomials:
                polynomials.append(polynomial)
            target_value = values_at_points(
                polynomial,
                variables,
                np.asarray((point,), dtype=np.int64),
                prime,
            )[0]
            if target_value == 0:
                print(
                    cell, "bad squarefree reduction", prime, point,
                    "supports", len(polynomials), flush=True,
                )
                exhausted = False
                break
            zeros = zeros[values == 0]
            new_points.append((prime, point))
            print(
                cell, "add", prime, point, "remaining", len(zeros),
                "supports", len(polynomials), flush=True,
            )
            if len(new_points) >= maximum_new:
                raise AssertionError("too many modular points")
        if not exhausted:
            continue
        status = singular_unit(polynomials, variables)
        print(cell, "exact", status, flush=True)
        if "UNIT" in status and "NONUNIT" not in status:
            print(cell, "MODULAR_POINTS", tuple(new_points), flush=True)
            return
    print(cell, "MODULAR_POINTS", tuple(new_points), flush=True)
    raise AssertionError(cell)


def explore(cell, decompose=False):
    _charts, _substitutions, _indices, variables = low.cell_data(cell)
    points = FOUR_POINTS if len(variables) == 4 else FIVE_POINTS
    polynomials = []
    for index, point in enumerate(points):
        polynomial = selected_support(cell, point)
        if polynomial not in polynomials:
            polynomials.append(polynomial)
        if index % 5 == 4 or index + 1 == len(points):
            status = singular_unit(polynomials, variables)
            print(cell, index + 1, len(polynomials), status, flush=True)
            if "UNIT" in status and "NONUNIT" not in status:
                return

    if decompose:
        print(singular_minimal_primes(polynomials, variables), flush=True)
        return

    # Deterministic tie shuffles at the origin expose additional minors
    # without expanding the point grid.
    for seed in range(1, 41):
        polynomial = selected_support(cell, points[0], tie_seed=seed)
        if polynomial not in polynomials:
            polynomials.append(polynomial)
        if seed % 5 == 0:
            status = singular_unit(polynomials, variables)
            print(cell, "seed", seed, len(polynomials), status, flush=True)
            if "UNIT" in status and "NONUNIT" not in status:
                return
    raise AssertionError(cell)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cell", choices=("CCE", "CEC", "ECC", "CCB", "CBC", "BCC"))
    parser.add_argument("--decompose", action="store_true")
    parser.add_argument("--modular", action="store_true")
    args = parser.parse_args()
    try:
        if args.modular:
            modular_close(args.cell)
        else:
            explore(args.cell, decompose=args.decompose)
    finally:
        response.PRIME = DEFAULT_PRIME


if __name__ == "__main__":
    main()
