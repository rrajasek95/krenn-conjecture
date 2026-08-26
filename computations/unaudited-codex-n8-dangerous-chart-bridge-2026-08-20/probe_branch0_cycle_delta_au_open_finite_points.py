#!/usr/bin/env python3
"""Lift the nine basic-open p1009 norm-triple points to the full packet."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_branch0_cycle_delta_au_open_generic.py"
PRIME = 1009
PARAMETER_POINTS = ((55, 10), (70, 167), (382, 384), (459, 101),
                    (532, 101), (589, 1008), (603, 1008), (626, 628),
                    (754, 10))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("n8_cycle_delta_finite_point_audit", AUDIT_PATH)
sp = AUDIT.sp
SOURCE = AUDIT.SOURCE


def mod_value(value, substitutions):
    numerator, denominator = sp.cancel(value.subs(substitutions)).as_numer_denom()
    n = int(numerator) % PRIME
    d = int(denominator) % PRIME
    if not d:
        raise ZeroDivisionError
    return n * pow(d, -1, PRIME) % PRIME


def coefficient_vector(poly, variable, substitutions):
    value = sp.Poly(poly, variable)
    return np.array([mod_value(coefficient, substitutions)
                     for coefficient in value.all_coeffs()], dtype=np.int64)


def evaluate_all(coefficients):
    arguments = np.arange(PRIME, dtype=np.int64)
    values = np.zeros(PRIME, dtype=np.int64)
    for coefficient in coefficients:
        values = (values*arguments + coefficient) % PRIME
    return values


def rank_mod(matrix):
    matrix = [list(map(lambda value: int(value) % PRIME, row))
              for row in matrix]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, PRIME)
        matrix[rank] = [value*inverse % PRIME for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [(left-scale*right) % PRIME
                           for left, right in zip(matrix[row], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank, matrix


def determinant_mod(matrix, rows):
    value = 0
    for permutation in itertools.permutations(range(4)):
        inversions = sum(permutation[left] > permutation[right]
                         for left in range(4)
                         for right in range(left+1, 4))
        term = 1
        for row, column in zip(rows, permutation):
            term = term*matrix[row][column] % PRIME
        value += (-1 if inversions % 2 else 1)*term
    return value % PRIME


def selected_solution(augmented):
    _, rref = rank_mod(augmented)
    pivots = {}
    for row in rref:
        pivot = next((column for column in range(3) if row[column]), None)
        if pivot is not None:
            pivots[pivot] = row
    free = [column for column in range(3) if column not in pivots]
    for selected_column in (0, 1):
        if selected_column not in pivots:
            continue
        row = pivots[selected_column]
        if all(row[column] == 0 for column in free) and row[3] == 1:
            return None
    # The forbidden p1=-1 and p2=-1 hyperplanes cannot cover the affine
    # solution space over F_1009.  The product of their two nonzero affine
    # linear forms has degree at most two in each free variable, hence cannot
    # vanish on the entire grid {0,1,2}^dim (the usual grid interpolation
    # lemma).  Searching that grid is therefore deterministic and complete.
    for trial in itertools.product(range(3), repeat=len(free)):
        values = [None, None, None]
        for column, value in zip(free, trial):
            values[column] = value
        for pivot, row in pivots.items():
            values[pivot] = (-row[3]-sum(
                row[column]*values[column] for column in free)) % PRIME
        if (values[0]+1) % PRIME and (values[1]+1) % PRIME:
            return tuple(values)
    raise AssertionError("two affine hyperplanes covered a 3-grid")


def third_minor(rows, derived):
    b0, b1, _, d1, _, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    normalized = AUDIT.INTERFACE.derive(rows)[6]
    live_row_factors = (b1**2*d1**2*x, 1, 1,
                        d4**2*x, b1*x, d1*d4)
    matrix = [[sp.cancel(entry/live_row_factors[row])
               for entry in entries]
              for row, entries in enumerate(normalized)]
    return AUDIT.minor_core(
        matrix, (1, 2, 3, 4), d4, derived["d4_value"], derived["q"],
        b0, b1, x, d1)


def main():
    rows = {label: SOURCE.expression(poly)
            for label, poly, _ in SOURCE.SOURCE.data()[0]}
    derived = AUDIT.derive(rows)
    interface = AUDIT.INTERFACE.derive(rows)
    normalized = interface[6]
    p3_p4 = interface[3]
    third = third_minor(rows, derived)
    b0, b1, _, d1, _, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    pair_polys = (derived["left"], derived["right"], third)
    fibre_candidates = []
    packet_candidates = []
    rejection = {"denominator": 0, "live": 0, "rank": 0,
                 "selected_linear": 0, "selected_p34": 0}
    live_reasons = {}
    rank_points = []
    for d1_value, x_value in PARAMETER_POINTS:
        base = {d1: d1_value, x: x_value}
        b0_roots = [value for value in range(PRIME)
                    if mod_value(derived["q"], {**base, b0: value}) == 0]
        for b0_value in b0_roots:
            partial = {**base, b0: b0_value}
            common = np.ones(PRIME, dtype=bool)
            for poly in pair_polys:
                common &= evaluate_all(
                    coefficient_vector(poly, b1, partial)) == 0
            for b1_value in np.flatnonzero(common):
                point = {**partial, b1: int(b1_value)}
                fibre_candidates.append((d1_value, x_value, b0_value,
                                         int(b1_value)))
                try:
                    d4_value = mod_value(derived["d4_value"], point)
                    full = {**point, d4: d4_value}
                    live = {
                        "b0": b0_value, "b1": int(b1_value),
                        "d1": d1_value, "x": x_value,
                        "B0": (int(b1_value)+d1_value) % PRIME,
                        "x-1": (x_value-1) % PRIME,
                        "Au": mod_value(derived["au"], point),
                        "d4": d4_value, "A": mod_value(derived["a"], base),
                    }
                    if not all(live.values()):
                        rejection["live"] += 1
                        reason = tuple(label for label, value in live.items()
                                       if not value)
                        live_reasons[reason] = live_reasons.get(reason, 0) + 1
                        continue
                    matrix = [[mod_value(entry, full) for entry in row]
                              for row in normalized]
                except ZeroDivisionError:
                    rejection["denominator"] += 1
                    continue
                rank_coeff, _ = rank_mod([row[:3] for row in matrix])
                rank_aug, _ = rank_mod(matrix)
                if rank_coeff != rank_aug:
                    rejection["rank"] += 1
                    firing = tuple(selected for selected in
                                   itertools.combinations(range(6), 4)
                                   if determinant_mod(matrix, selected))
                    rank_points.append((d1_value, x_value, b0_value,
                                        int(b1_value), d4_value,
                                        rank_coeff, rank_aug, firing))
                    continue
                solution = selected_solution(matrix)
                if solution is None:
                    rejection["selected_linear"] += 1
                    continue
                p1, p2, a5 = solution
                p3 = mod_value(p3_p4[SOURCE.P[2]], full)
                p4 = mod_value(p3_p4[SOURCE.P[3]], full)
                selected = ((p1+1) % PRIME, (p2+1) % PRIME,
                            (p3+1) % PRIME, (p4+1) % PRIME)
                if all(selected):
                    packet_candidates.append({
                        "d1": d1_value, "x": x_value,
                        "b0": b0_value, "b1": int(b1_value),
                        "d4": d4_value, "p1": p1, "p2": p2,
                        "p3": p3, "p4": p4, "a5": a5,
                    })
                else:
                    rejection["selected_p34"] += 1
    print("pair-minor fibre candidates", len(fibre_candidates))
    fibres = {}
    for d1_value, x_value, b0_value, _ in fibre_candidates:
        key = (d1_value, x_value, b0_value)
        fibres[key] = fibres.get(key, 0) + 1
    for point, count in sorted(fibres.items()):
        print("fibre", *point, "b1_count", count)
    print("rejection", rejection)
    print("live rejection reasons", sorted(live_reasons.items()))
    for point in rank_points:
        print("inconsistent packet point", point)
    print("full selected-live packet candidates", len(packet_candidates))
    for point in packet_candidates:
        print("packet", point)


if __name__ == "__main__":
    main()
