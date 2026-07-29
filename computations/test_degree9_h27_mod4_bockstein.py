#!/usr/bin/env python3
"""Construct the degree-nine H27 Bockstein obstruction modulo powers of two.

Let ``Abar`` denote the integral H-orbit Macaulay matrix after multiplying
row ``r`` by its (odd) orbit size.  Thus an entry represented in the compact
integer cache is

    Abar[r,j] = column_size[j] * multiplicity[r,j],

and the target has coefficient ``row_size[r]`` on a target row.  These odd
row scalings are units modulo every power of two.

The saved characteristic-two certificate gives ``b = Abar*x0 (mod 2)``.
For ``r = (b-Abar*x0)/2``, the saved dual ``y`` satisfies

    y*Abar = 0 (mod 2),       y*r = 1 (mod 2).

We solve the Bockstein equation

    Abar^T*u = (y*Abar/2)^T (mod 2)

and obtain ``lambda = y + 2*u``.  It obeys

    lambda*Abar = 0 (mod 4), lambda*b = 2 (mod 4),

which rules out integral source-ideal membership even modulo four.  The
same transpose factorization is retained and reused to lift lambda through
further powers of two.  If Abar^T has full row rank, this also proves that
the lift exists through every 2-adic precision, not merely those tested.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import heapq
import pickle
import time
from array import array
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_pickle(path: Path):
    opener = gzip.open if path.suffix == ".gz" else path.open
    if path.suffix == ".gz":
        with opener(path, "rb") as stream:
            return pickle.load(stream)
    with opener("rb") as stream:
        return pickle.load(stream)


class TransposeFactorization:
    """Exact sparse GF(2) factorization of A^T, reusable for many RHSs."""

    def __init__(self, columns, number_variables: int):
        started = time.time()
        equations = [set(column) for column in columns]
        number_equations = len(equations)
        adjacency = [set() for _ in range(number_variables)]
        for equation, variables in enumerate(equations):
            for variable in variables:
                adjacency[variable].add(equation)

        active = bytearray(b"\x01") * number_equations
        remaining = number_equations
        heap = [
            (len(adjacency[variable]), variable)
            for variable in range(number_variables)
            if adjacency[variable]
        ]
        heapq.heapify(heap)

        # Replaying target_rhs[t] ^= target_rhs[s] for these pairs applies
        # exactly the row operations used by the structural elimination.
        operation_targets = array("I")
        operation_sources = array("I")
        records = []
        dependent_equations = []

        while remaining:
            while heap:
                degree, variable = heapq.heappop(heap)
                if degree and degree == len(adjacency[variable]):
                    break
            else:
                raise AssertionError(
                    f"{remaining} active nonzero equations contain no variable"
                )

            pivot_equation = min(
                adjacency[variable],
                key=lambda equation: (len(equations[equation]), equation),
            )
            pivot_variables = equations[pivot_equation]
            records.append(
                (
                    variable,
                    tuple(value for value in pivot_variables if value != variable),
                    pivot_equation,
                )
            )

            for equation in sorted(adjacency[variable] - {pivot_equation}):
                variables = equations[equation]
                for value in pivot_variables:
                    if value in variables:
                        variables.remove(value)
                        adjacency[value].remove(equation)
                    else:
                        variables.add(value)
                        adjacency[value].add(equation)
                    heapq.heappush(heap, (len(adjacency[value]), value))
                operation_targets.append(equation)
                operation_sources.append(pivot_equation)
                if not variables:
                    active[equation] = 0
                    remaining -= 1
                    dependent_equations.append(equation)

            active[pivot_equation] = 0
            remaining -= 1
            for value in pivot_variables:
                adjacency[value].remove(pivot_equation)
                heapq.heappush(heap, (len(adjacency[value]), value))

            if len(records) % 10_000 == 0:
                print(
                    f"factor pivots={len(records)} remaining={remaining} "
                    f"minimum-degree={degree} operations={len(operation_targets)} "
                    f"seconds={time.time()-started:.2f}",
                    flush=True,
                )

        self.columns = columns
        self.number_variables = number_variables
        self.number_equations = number_equations
        self.records = records
        self.operation_targets = operation_targets
        self.operation_sources = operation_sources
        self.dependent_equations = tuple(dependent_equations)
        self.last_obstruction = None
        print(
            f"factor complete: rank={len(records)}/{number_equations}, "
            f"operations={len(operation_targets)}, "
            f"dependent={len(dependent_equations)}, "
            f"seconds={time.time()-started:.2f}",
            flush=True,
        )

    @property
    def full_row_rank(self):
        return len(self.records) == self.number_equations

    def solve(self, original_rhs, audit=True):
        """Solve A^T*x=rhs, or return None if this RHS is inconsistent."""
        assert len(original_rhs) == self.number_equations
        rhs = bytearray(original_rhs)
        for target, source in zip(self.operation_targets, self.operation_sources):
            rhs[target] ^= rhs[source]
        bad_equation = next(
            (
                equation
                for equation in self.dependent_equations
                if rhs[equation]
            ),
            None,
        )
        if bad_equation is not None:
            # Recover the exact combination of original equations yielding
            # the inconsistent transformed equation 0=1.
            marks = bytearray(self.number_equations)
            marks[bad_equation] = 1
            for target, source in zip(
                reversed(self.operation_targets), reversed(self.operation_sources)
            ):
                if marks[target]:
                    marks[source] ^= 1
            obstruction = tuple(
                equation for equation, value in enumerate(marks) if value
            )
            audit = set()
            for equation in obstruction:
                audit.symmetric_difference_update(self.columns[equation])
            assert not audit
            assert sum(original_rhs[equation] for equation in obstruction) & 1
            self.last_obstruction = obstruction
            return None

        self.last_obstruction = None

        values = bytearray(self.number_variables)
        for variable, other_variables, pivot_equation in reversed(self.records):
            value = rhs[pivot_equation]
            for other in other_variables:
                value ^= values[other]
            values[variable] = value

        if audit:
            for equation, column in enumerate(self.columns):
                assert (
                    sum(values[row] for row in column) & 1
                ) == original_rhs[equation]
        return values


def save_character(path: Path, values, modulus: int, shape, target_pairing: int):
    support = array("I")
    coefficients = array("Q")
    for row, value in enumerate(values):
        value %= modulus
        if value:
            support.append(row)
            coefficients.append(value)
    payload = {
        "version": 1,
        "ring": f"Z/{modulus}Z",
        "group_order": 27,
        "shape": shape,
        "modulus": modulus,
        "support": support,
        "coefficients": coefficients,
        "target_pairing": target_pairing % modulus,
    }
    path.parent.mkdir(exist_ok=True)
    with gzip.open(path, "wb") as stream:
        pickle.dump(payload, stream, protocol=pickle.HIGHEST_PROTOCOL)
    print(
        f"saved {path}: support={len(support)} target={target_pairing % modulus}",
        flush=True,
    )


def save_lift_obstruction(path, equation_support, shape, base_character_path):
    digest = hashlib.sha256(base_character_path.read_bytes()).hexdigest()
    payload = {
        "version": 1,
        "field": "GF(2)",
        "group_order": 27,
        "shape": shape,
        "base_modulus": 4,
        "base_character_sha256": digest,
        "equation_support": tuple(equation_support),
    }
    with gzip.open(path, "wb") as stream:
        pickle.dump(payload, stream, protocol=pickle.HIGHEST_PROTOCOL)
    print(
        f"saved {path}: dependency support={len(equation_support)}",
        flush=True,
    )


def column_dot(integral, column: int, vector):
    offsets = integral["offsets"]
    rows = integral["row_indices"]
    coefficients = integral["coefficients"]
    column_size = integral["column_sizes"][column]
    return column_size * sum(
        vector[rows[position]] * coefficients[position]
        for position in range(offsets[column], offsets[column + 1])
    )


def target_dot(parity, integral, vector):
    return sum(
        vector[row] * integral["row_sizes"][row]
        for row, is_target in enumerate(parity["rhs"])
        if is_target
    )


def validate_first_residual(parity, integral, residual, selected_columns):
    """Audit bbar-Abar*x0 = 2*diag(row_size)*r exactly over Z."""
    number_rows, number_columns = integral["shape"]
    selected = bytearray(number_columns)
    for column in selected_columns:
        assert not selected[column]
        selected[column] = 1
    accumulated = array("i", [0]) * number_rows
    offsets = integral["offsets"]
    rows = integral["row_indices"]
    coefficients = integral["coefficients"]
    for column in selected_columns:
        column_size = integral["column_sizes"][column]
        for position in range(offsets[column], offsets[column + 1]):
            accumulated[rows[position]] += column_size * coefficients[position]
    for row in range(number_rows):
        row_size = integral["row_sizes"][row]
        target = row_size * parity["rhs"][row]
        assert target - accumulated[row] == 2 * row_size * residual[row]
    print("audited exact first integral residual identity", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-power",
        type=int,
        default=16,
        help="lift and verify through modulus 2^POWER (default: 16)",
    )
    args = parser.parse_args()
    assert args.max_power >= 2

    parity = load_pickle(HERE / "degree9_source_ideal_char2_h27.pkl")
    integral = load_pickle(HERE / "degree9_source_ideal_h27_integer.pkl")
    residual_payload = load_pickle(
        HERE / "degree9_char2_first_integral_residual.pkl.gz"
    )
    membership = load_pickle(
        HERE / "certificates" / "degree9_char2_h27_membership.pkl.gz"
    )
    residual_dual = load_pickle(
        HERE
        / "certificates"
        / "degree9_char2_first_residual_dual.pkl.gz"
    )

    shape = integral["shape"]
    number_rows, number_columns = shape
    assert shape == (len(parity["row_codes"]), len(parity["columns"]))
    assert membership["shape"] == residual_dual["shape"] == shape
    residual = residual_payload["coefficients"]
    assert len(residual) == number_rows
    validate_first_residual(
        parity, integral, residual, membership["selected_columns"]
    )

    y = bytearray(number_rows)
    for row in residual_dual["support"]:
        assert not y[row]
        y[row] = 1
    for column in parity["columns"]:
        assert sum(y[row] for row in column) % 2 == 0
    assert sum(y[row] * residual[row] for row in range(number_rows)) % 2 == 1
    print(
        f"audited residual dual: support={sum(y)}, pairing=1 mod 2",
        flush=True,
    )

    bockstein_rhs = bytearray(number_columns)
    for column in range(number_columns):
        value = column_dot(integral, column, y)
        assert value % 2 == 0
        bockstein_rhs[column] = (value // 2) & 1
    print(
        f"first Bockstein RHS support={sum(bockstein_rhs)}/{number_columns}",
        flush=True,
    )

    factor = TransposeFactorization(parity["columns"], number_rows)
    u = factor.solve(bockstein_rhs)
    if u is None:
        print("FIRST BOCKSTEIN EQUATION IS INCONSISTENT", flush=True)
        raise SystemExit(2)

    lam = [y[row] + 2 * u[row] for row in range(number_rows)]
    modulus = 4
    for column in range(number_columns):
        assert column_dot(integral, column, lam) % modulus == 0
    pairing = target_dot(parity, integral, lam) % modulus
    assert pairing == 2
    output4 = (
        HERE / "certificates" / "degree9_h27_integral_dual_mod4.pkl.gz"
    )
    save_character(output4, lam, modulus, shape, pairing)

    for power in range(2, args.max_power):
        next_rhs = bytearray(number_columns)
        for column in range(number_columns):
            value = column_dot(integral, column, lam)
            assert value % modulus == 0
            next_rhs[column] = (value // modulus) & 1
        correction = factor.solve(next_rhs)
        if correction is None:
            assert modulus == 4  # named certificate below is specifically mod 8
            obstruction_path = (
                HERE
                / "certificates"
                / "degree9_h27_mod8_lift_obstruction.pkl.gz"
            )
            save_lift_obstruction(
                obstruction_path,
                factor.last_obstruction,
                shape,
                output4,
            )
            print(
                f"lift fails from modulus {modulus} to {2*modulus}; "
                f"RHS support={sum(next_rhs)}",
                flush=True,
            )
            break
        for row, value in enumerate(correction):
            if value:
                lam[row] += modulus
        modulus *= 2
        for column in range(number_columns):
            assert column_dot(integral, column, lam) % modulus == 0
        pairing = target_dot(parity, integral, lam) % modulus
        assert pairing % 4 == 2
        print(
            f"lifted to modulus={modulus}: correction support={sum(correction)}, "
            f"character support={sum(value != 0 for value in lam)}, "
            f"target pairing={pairing}",
            flush=True,
        )

    highest = (
        HERE
        / "certificates"
        / f"degree9_h27_integral_dual_mod{modulus}.pkl.gz"
    )
    if modulus != 4:
        save_character(highest, lam, modulus, shape, pairing)
    if factor.full_row_rank:
        print(
            "Abar^T has full row rank over GF(2), so the character lifts "
            "inductively to every 2-adic precision.",
            flush=True,
        )


if __name__ == "__main__":
    main()
