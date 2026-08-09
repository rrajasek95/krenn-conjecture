#!/usr/bin/env python3
"""Symbolic radical Fitting witness on the first w=0 five-cross support."""

from __future__ import annotations

import argparse
import concurrent.futures
import subprocess
import sys
from collections import Counter
from fractions import Fraction

import verify_n10_occupied_modulus_zero_stratum as zero_stratum
import verify_n8_three_cut_exactness_tangent as tangent


Q = Fraction
SUPPORTS = (
    (
        (0, 8, 1, 0),
        (0, 8, 1, 2),
        (5, 9, 1, 0),
        (5, 9, 1, 2),
        (6, 9, 0, 0),
    ),
    (
        (0, 8, 1, 0),
        (5, 8, 1, 2),
        (0, 9, 1, 2),
        (5, 9, 1, 0),
        (6, 9, 0, 0),
    ),
    (
        (0, 8, 1, 2),
        (5, 8, 1, 0),
        (0, 9, 1, 0),
        (5, 9, 1, 2),
        (6, 9, 0, 2),
    ),
)
LOST_SUPPORTS = (
    ((0, 8, 1, 0), (0, 8, 1, 2), (5, 9, 1, 0), (5, 9, 1, 2), (6, 9, 0, 0)),
    ((0, 8, 1, 0), (0, 8, 1, 2), (5, 9, 1, 0), (5, 9, 1, 2), (6, 9, 0, 2)),
    ((0, 8, 1, 0), (0, 8, 1, 2), (5, 9, 1, 0), (5, 9, 1, 2), (6, 9, 1, 0)),
    ((0, 8, 1, 0), (0, 8, 1, 2), (5, 9, 1, 0), (5, 9, 1, 2), (6, 9, 1, 2)),
    ((0, 8, 1, 0), (0, 8, 1, 2), (5, 9, 1, 0), (5, 9, 1, 2), (6, 9, 2, 0)),
    ((0, 8, 1, 0), (0, 8, 1, 2), (5, 9, 1, 0), (5, 9, 1, 2), (6, 9, 2, 2)),
    ((0, 8, 1, 0), (5, 8, 1, 2), (0, 9, 1, 2), (5, 9, 1, 0), (6, 9, 0, 0)),
    ((0, 8, 1, 0), (5, 8, 1, 2), (0, 9, 1, 2), (5, 9, 1, 0), (6, 9, 1, 0)),
    ((0, 8, 1, 0), (5, 8, 1, 2), (0, 9, 1, 2), (5, 9, 1, 0), (6, 9, 2, 0)),
    ((0, 8, 1, 2), (5, 8, 1, 0), (0, 9, 1, 0), (5, 9, 1, 2), (6, 9, 0, 2)),
    ((0, 8, 1, 2), (5, 8, 1, 0), (0, 9, 1, 0), (5, 9, 1, 2), (6, 9, 1, 2)),
    ((0, 8, 1, 2), (5, 8, 1, 0), (0, 9, 1, 0), (5, 9, 1, 2), (6, 9, 2, 2)),
)
CUT = 2
VARIABLES = ("a", "b", "c", "d", "e")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def raw_cut_data(data, cells):
    module = data["module"]
    forced_pair = data["forced_pair"]
    vertices = data["provenance"].B10
    u_set = tuple(vertex for vertex in module.S if vertex != CUT) + (8, 9)
    columns = forced_pair.insertion_columns(module, u_set, cells)
    tensor = module.matching_tensor(vertices, cells)
    residual = forced_pair.tensor_difference(
        tensor, forced_pair.delta_tensor(vertices)
    )
    rows = forced_pair.flatten_rows(
        residual, vertices, (CUT, 6, 7), u_set
    )
    return columns, rows


def selected_column_labels(module, columns):
    selected = []
    basis = {}
    for label, column in sorted(columns.items()):
        candidate = module.rational_basis(list(basis.values()) + [column])
        if len(candidate) > len(basis):
            selected.append(label)
            basis = candidate
    return tuple(selected), basis


def mobius_coefficients(values):
    coefficients = list(map(Q, values))
    for bit in range(5):
        for mask in range(32):
            if mask & (1 << bit):
                coefficients[mask] -= coefficients[mask ^ (1 << bit)]
    return tuple(coefficients)


def rational_string(value):
    value = Q(value)
    return str(value.numerator) if value.denominator == 1 else f"({value.numerator}/{value.denominator})"


def polynomial_string(values):
    terms = []
    for mask, coefficient in enumerate(mobius_coefficients(values)):
        if not coefficient:
            continue
        monomial = "*".join(
            VARIABLES[index] for index in range(5) if mask & (1 << index)
        ) or "1"
        terms.append(f"({rational_string(coefficient)})*{monomial}")
    return "+".join(terms).replace("+-", "-") or "0"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, choices=range(len(SUPPORTS)), default=0)
    parser.add_argument("--support-index", type=int, choices=range(len(LOST_SUPPORTS)))
    parser.add_argument("--all", action="store_true")
    arguments = parser.parse_args()
    if arguments.all:
        def run_support(index):
            process = subprocess.run(
                [sys.executable, __file__, "--support-index", str(index)],
                text=True,
                capture_output=True,
                check=True,
            )
            line = next(
                line
                for line in process.stdout.splitlines()
                if line.startswith("torus monomial:")
            )
            return line.split(":", 1)[1].strip()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            monomials = tuple(executor.map(run_support, range(len(LOST_SUPPORTS))))
        census = Counter(monomials)
        require(
            tuple(census.values()) == (6, 3, 3),
            "lost-support monomial orbit census changed",
        )
        print("N=10 w=0 symbolic radical witness family: PASS")
        print(f"lost supports: {len(LOST_SUPPORTS)}")
        print(f"torus-monomial census: {dict(census)}")
        return
    support = (
        LOST_SUPPORTS[arguments.support_index]
        if arguments.support_index is not None
        else SUPPORTS[arguments.orbit]
    )
    boundary_shear = tangent.load_boundary_shear()
    dependence = boundary_shear.load_dependence()
    quotient = dependence.load_quotient()
    cached = quotient.load_cached_blocks()
    matrix_cache = cached.load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    module = data["module"]
    sample = tuple(map(Q, matrix_cache.SAMPLE))
    deleted_old = zero_stratum.incidence.add_weighted_old_coordinates(
        module,
        data["base"],
        ((zero_stratum.incidence.OCCUPIED_MODULUS, Q(-1)),),
    )
    sample_cells = zero_stratum.full_source(data, deleted_old, support, sample)
    sample_columns, sample_rows = raw_cut_data(data, sample_cells)
    labels, basis = selected_column_labels(module, sample_columns)
    require(len(labels) == 21, "sample cofactor rank changed")
    boundary_word = next(
        word
        for word, row in sorted(sample_rows.items())
        if not module.rational_member(row, basis)
    )
    residual = sample_rows[boundary_word]
    remainder = data["two_cell"].quotient_remainder(residual, basis)
    require(remainder, "sample radical row entered the cofactor cylinder")
    pivot_rows = tuple(sorted(basis))
    extra_row = min(remainder)
    require(extra_row not in pivot_rows, "radical pivot already belongs to base frame")
    rows = pivot_rows + (extra_row,)

    corner_matrices = []
    for mask in range(32):
        weights = tuple(Q(bool(mask & (1 << index))) for index in range(5))
        cells = zero_stratum.full_source(data, deleted_old, support, weights)
        columns, residual_rows = raw_cut_data(data, cells)
        residual_column = residual_rows.get(boundary_word, {})
        corner_matrices.append(
            tuple(
                tuple(
                    (
                        columns[labels[column]].get(row, Q(0))
                        if column < len(labels)
                        else residual_column.get(row, Q(0))
                    )
                    for column in range(len(labels) + 1)
                )
                for row in rows
            )
        )

    entries = []
    for row in range(22):
        for column in range(22):
            entries.append(
                polynomial_string(
                    tuple(matrix[row][column] for matrix in corner_matrices)
                )
            )
    script = "\n".join(
        (
            f"ring r=0,({','.join(VARIABLES)}),dp;",
            f"matrix A[22][22]={','.join(entries)};",
            'print("FACTORS");',
            "factorize(det(A));",
        )
    )
    process = subprocess.run(
        ["Singular", "-q"],
        input=script,
        text=True,
        capture_output=True,
        check=True,
    )
    output = tuple(line.strip() for line in process.stdout.splitlines() if line.strip())
    require(output and output[0] == "FACTORS", "Singular factor marker changed")
    multiplicity_marker = output.index("[2]:")
    factors = tuple(line.split("=", 1)[1] for line in output[2:multiplicity_marker])
    multiplicities = tuple(map(int, output[multiplicity_marker + 1].split(",")))
    require(len(factors) == len(multiplicities), "factor multiplicities changed")
    require(
        all(factor in ("-1", "1") + VARIABLES for factor in factors),
        "radical determinant acquired a non-torus factor",
    )
    monomial = tuple(
        sorted(
            (factor, exponent)
            for factor, exponent in zip(factors, multiplicities)
            if factor not in ("-1", "1")
        )
    )
    print("N=10 w=0 first symbolic radical witness: exact frontier")
    print(f"orbit/support-index/support: {arguments.orbit} / {arguments.support_index} / {support}")
    print(f"boundary word / quotient pivot: {boundary_word} / {extra_row}")
    print(f"selected cofactor labels: {labels}")
    print("factorization:")
    print("\n".join(output[1:]))
    print(f"torus monomial: {monomial}")


if __name__ == "__main__":
    main()
