#!/usr/bin/env python3
"""Exact-support four-parameter integration of the 22-cell descent branch."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import product
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
import integrate_global_normal_counterfamily as old  # noqa: E402
import certify_current_multiray_counterdirection as counter  # noqa: E402


PARAMETERS = ("v", "w", "x", "y")
LEAKS = {
    "v": {cell: Fraction(value) for cell, value in old.BOUNDARY.items()},
    "w": dict(old.DIRECTION),
    "x": dict(counter.LEFT),
    "y": dict(counter.RIGHT),
}
SUPPORT = set(family.BASE)
for packet in LEAKS.values():
    SUPPORT.update(packet)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def energy_coefficients():
    degree = {name: defaultdict(Fraction) for name in PARAMETERS}
    for name, packet in LEAKS.items():
        for (u, v, a, b), value in packet.items():
            degree[name][u, a] += value * value
            degree[name][v, b] += value * value
    answer = {}
    for colour, layer in family.LAYERS.items():
        rows = []
        for u, v in layer:
            row = []
            for name in PARAMETERS:
                require(degree[name][u, colour] == degree[name][v, colour],
                        (name, colour, u, v, degree[name]))
                row.append(degree[name][u, colour])
            rows.append(tuple(row))
        answer[colour] = tuple(rows)
    return answer


ENERGY_COEFFICIENTS = energy_coefficients()


def energies(colour, parameters):
    return tuple(sum(float(coefficient) * value
                     for coefficient, value in zip(row, parameters))
                 for row in ENERGY_COEFFICIENTS[colour])


def rho_root(values):
    lo, hi = max(values), max(1.0, max(values) + 1.0)
    def equation(rho):
        result = 1.0
        for value in values:
            result *= rho - value
        return result - 1.0
    while equation(hi) < 0:
        hi *= 2
    for _ in range(80):
        middle = (lo + hi) / 2
        if equation(middle) < 0:
            lo = middle
        else:
            hi = middle
    return (lo + hi) / 2


def source_jets(parameters):
    n = len(PARAMETERS)
    source = {}
    for colour, layer in family.LAYERS.items():
        e = energies(colour, parameters)
        rho = rho_root(e)
        gaps = [rho - value for value in e]
        rows = [[float(value) for value in row]
                for row in ENERGY_COEFFICIENTS[colour]]
        denominator = sum(1 / gap for gap in gaps)
        rho_i = [sum(row[i] / gap for row, gap in zip(rows, gaps)) / denominator
                 for i in range(n)]
        rho_ij = [[sum((rho_i[i] - row[i]) * (rho_i[j] - row[j]) / gap ** 2
                           for row, gap in zip(rows, gaps)) / denominator
                   for j in range(n)] for i in range(n)]
        for edge, gap, row in zip(layer, gaps, rows):
            value = math.sqrt(gap)
            gradient = [(rho_i[i] - row[i]) / (2 * value) for i in range(n)]
            hessian = [[rho_ij[i][j] / (2 * value)
                        - (rho_i[i] - row[i]) * (rho_i[j] - row[j])
                        / (4 * value ** 3)
                        for j in range(n)] for i in range(n)]
            source[edge + (colour, colour)] = value, gradient, hessian
    for index, name in enumerate(PARAMETERS):
        root = math.sqrt(parameters[index])
        for cell, coefficient in LEAKS[name].items():
            scalar = float(coefficient)
            gradient = [0.0] * n
            gradient[index] = scalar / (2 * root)
            hessian = [[0.0] * n for _ in range(n)]
            hessian[index][index] = -scalar / (4 * root ** 3)
            source[cell] = scalar * root, gradient, hessian
    return source


def term_ledger():
    edge_cells = defaultdict(list)
    for cell in SUPPORT:
        edge_cells[cell[:2]].append(cell)
    answer = defaultdict(list)
    for matching in family.PM8:
        choices = [edge_cells[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [None] * 8
            for u, v, a, b in picked:
                word[u], word[v] = a, b
            answer[tuple(word)].append(tuple(picked))
    return answer


TERMS = term_ledger()


def product_jets(factors):
    n = len(PARAMETERS)
    value = math.prod(factor[0] for factor in factors)
    gradient = [0.0] * n
    hessian = [[0.0] * n for _ in range(n)]
    for at, factor in enumerate(factors):
        other = math.prod(factors[k][0] for k in range(len(factors)) if k != at)
        for i in range(n):
            gradient[i] += factor[1][i] * other
            for j in range(n):
                hessian[i][j] += factor[2][i][j] * other
    for left in range(len(factors)):
        for right in range(left + 1, len(factors)):
            other = math.prod(factors[k][0] for k in range(len(factors))
                              if k not in (left, right))
            for i in range(n):
                for j in range(n):
                    hessian[i][j] += (factors[left][1][i] * factors[right][1][j]
                                      + factors[left][1][j] * factors[right][1][i]) * other
    return value, gradient, hessian


def p_jets(parameters):
    n = len(PARAMETERS)
    source = source_jets(parameters)
    p = 0.0
    gradient = [0.0] * n
    hessian = [[0.0] * n for _ in range(n)]
    for word, monomials in TERMS.items():
        if len(set(word)) == 1:
            continue
        amplitude = 0.0
        first = [0.0] * n
        second = [[0.0] * n for _ in range(n)]
        for monomial in monomials:
            value, row, matrix = product_jets([source[cell] for cell in monomial])
            amplitude += value
            for i in range(n):
                first[i] += row[i]
                for j in range(n):
                    second[i][j] += matrix[i][j]
        p += amplitude * amplitude
        for i in range(n):
            gradient[i] += 2 * amplitude * first[i]
            for j in range(n):
                hessian[i][j] += 2 * (first[i] * first[j]
                                       + amplitude * second[i][j])
    return p, gradient, hessian


def solve_linear(matrix, vector):
    n = len(vector)
    work = [list(row) + [value] for row, value in zip(matrix, vector)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(work[row][col]))
        require(abs(work[pivot][col]) > 1e-12, (matrix, vector))
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [value / scale for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            scale = work[row][col]
            work[row] = [left - scale * right
                         for left, right in zip(work[row], work[col])]
    return [work[row][-1] for row in range(n)]


def optimize(start):
    point = list(start)
    for iteration in range(50):
        p, gradient, hessian = p_jets(point)
        if max(abs(value) for value in gradient) < 1e-8:
            return point, p, gradient, hessian, iteration
        step = solve_linear(hessian, [-value for value in gradient])
        scale = 1.0
        while min(point[i] + scale * step[i] for i in range(4)) <= 1e-10:
            scale /= 2
        while p_jets([point[i] + scale * step[i] for i in range(4)])[0] >= p:
            scale /= 2
            require(scale > 2 ** -40, (point, p, gradient, step))
        point = [point[i] + scale * step[i] for i in range(4)]
    raise RuntimeError((point, p_jets(point)))


def symbolic_outputs():
    labels = {cell: f"d{cell[0]}{cell[1]}_{cell[2]}" for cell in family.BASE}
    for name, packet in LEAKS.items():
        for cell, coefficient in packet.items():
            labels[cell] = f"({coefficient})*sqrt({name})"
    answer = {}
    for word, monomials in TERMS.items():
        answer["".join(map(str, word))] = ["*".join(labels[cell] for cell in monomial)
                                               for monomial in monomials]
    return answer


def main():
    source = {cell: None for cell in SUPPORT}
    stars, triangles = family.carrier_witnesses(source)
    require((len(stars), len(triangles)) == (168, 560),
            (len(stars), len(triangles)))
    # L+5R means squared-amplitude ratio y/x=25; a small positive start is
    # enough for joint Newton continuation.
    point, p, gradient, hessian, iterations = optimize(
        (0.2052415678447232, 0.1929534886934304, 0.001, 0.025)
    )
    print("energy coefficients", ENERGY_COEFFICIENTS)
    for colour in range(3):
        print("rho equation", colour, "product_k(rho-energy_k)=1")
    print("support", len(SUPPORT), "outputs", len(TERMS),
          "mixed", sum(len(set(word)) > 1 for word in TERMS))
    print("minimum", dict(zip(PARAMETERS, point)), "P", p,
          "gradient", gradient, "iterations", iterations)
    print("Hessian")
    for row in hessian:
        print(row)
    print("carrier blockers", len(stars), len(triangles))
    for word, monomials in sorted(symbolic_outputs().items()):
        print("OUTPUT", word, monomials)


if __name__ == "__main__":
    main()
