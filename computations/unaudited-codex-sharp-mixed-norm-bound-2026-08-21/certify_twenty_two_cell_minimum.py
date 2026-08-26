#!/usr/bin/env python3
"""Outward interval/Krawczyk certificate for the 22-cell strict minimum."""

from __future__ import annotations

from itertools import product, permutations
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_twenty_two_cell_branch as branch  # noqa: E402
from certify_negative_family_global_min import I, down, up  # noqa: E402


CENTER = (0.22235570199505403, 0.10692046095948153,
          0.02918848455871847, 0.17124569877870893)
RADIUS = (2e-7, 2e-7, 2e-7, 2e-7)
BOX = tuple(I(down(value-radius), up(value+radius))
            for value, radius in zip(CENTER, RADIUS))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def root_point(energies):
    lo, hi = max(energies), max(1.0, max(energies) + 1.0)
    def equation(rho):
        value = 1.0
        for energy in energies:
            value *= rho - energy
        return value - 1
    while equation(hi) < 0:
        hi *= 2
    for _ in range(80):
        middle = (lo + hi) / 2
        if equation(middle) < 0:
            lo = middle
        else:
            hi = middle
    return down(lo), up(hi)


def source_intervals():
    n = len(branch.PARAMETERS)
    source = {}
    for colour, layer in branch.family.LAYERS.items():
        energies = [sum((float(coefficient) * parameter
                         for coefficient, parameter in zip(row, BOX)), I(0))
                    for row in branch.ENERGY_COEFFICIENTS[colour]]
        root_lo = root_point([energy.lo for energy in energies])[0]
        root_hi = root_point([energy.hi for energy in energies])[1]
        rho = I(root_lo, root_hi)
        gaps = [rho - energy for energy in energies]
        rows = [[float(value) for value in row]
                for row in branch.ENERGY_COEFFICIENTS[colour]]
        denominator = sum((I(1) / gap for gap in gaps), I(0))
        rho_i = [sum((row[i] / gap for row, gap in zip(rows, gaps)), I(0))
                 / denominator for i in range(n)]
        rho_ij = [[sum((((rho_i[i] - row[i]) * (rho_i[j] - row[j]))
                        / gap.square() for row, gap in zip(rows, gaps)), I(0))
                   / denominator for j in range(n)] for i in range(n)]
        for edge, gap, row in zip(layer, gaps, rows):
            value = gap.sqrt()
            cube = value * value * value
            gradient = [(rho_i[i] - row[i]) / (2 * value) for i in range(n)]
            hessian = [[rho_ij[i][j] / (2 * value)
                        - (rho_i[i] - row[i]) * (rho_i[j] - row[j]) / (4 * cube)
                        for j in range(n)] for i in range(n)]
            source[edge + (colour, colour)] = value, gradient, hessian
    for index, name in enumerate(branch.PARAMETERS):
        root = BOX[index].sqrt()
        cube = root * root * root
        for cell, coefficient in branch.LEAKS[name].items():
            scalar = float(coefficient)
            gradient = [I(0) for _ in range(n)]
            gradient[index] = scalar / (2 * root)
            hessian = [[I(0) for _ in range(n)] for _ in range(n)]
            hessian[index][index] = -scalar / (4 * cube)
            source[cell] = scalar * root, gradient, hessian
    return source


def product_jets(factors):
    n = len(branch.PARAMETERS)
    def multiply(indices, selections=None):
        selections = selections or {}
        value = I(1)
        for index in indices:
            value = value * selections.get(index, factors[index][0])
        return value
    indices = tuple(range(len(factors)))
    value = multiply(indices)
    gradient = [I(0) for _ in range(n)]
    hessian = [[I(0) for _ in range(n)] for _ in range(n)]
    for at, factor in enumerate(factors):
        for i in range(n):
            gradient[i] = gradient[i] + multiply(indices, {at: factor[1][i]})
            for j in range(n):
                hessian[i][j] = hessian[i][j] + multiply(
                    indices, {at: factor[2][i][j]})
    for left in range(len(factors)):
        for right in range(left + 1, len(factors)):
            for i in range(n):
                for j in range(n):
                    hessian[i][j] = hessian[i][j] + multiply(
                        indices, {left: factors[left][1][i],
                                  right: factors[right][1][j]})
                    hessian[i][j] = hessian[i][j] + multiply(
                        indices, {left: factors[left][1][j],
                                  right: factors[right][1][i]})
    return value, gradient, hessian


def p_jets_interval():
    n = len(branch.PARAMETERS)
    source = source_intervals()
    p = I(0)
    gradient = [I(0) for _ in range(n)]
    hessian = [[I(0) for _ in range(n)] for _ in range(n)]
    for word, monomials in branch.TERMS.items():
        if len(set(word)) == 1:
            continue
        amplitude = I(0)
        first = [I(0) for _ in range(n)]
        second = [[I(0) for _ in range(n)] for _ in range(n)]
        for monomial in monomials:
            value, row, matrix = product_jets([source[cell] for cell in monomial])
            amplitude = amplitude + value
            for i in range(n):
                first[i] = first[i] + row[i]
                for j in range(n):
                    second[i][j] = second[i][j] + matrix[i][j]
        p = p + amplitude.square()
        for i in range(n):
            gradient[i] = gradient[i] + 2 * amplitude * first[i]
            for j in range(n):
                hessian[i][j] = hessian[i][j] + 2 * (
                    first[i] * first[j] + amplitude * second[i][j])
    return p, gradient, hessian


def inverse(matrix):
    n = len(matrix)
    work = [list(row) + [1.0 if i == j else 0.0 for j in range(n)]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(work[row][col]))
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [value / scale for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            scale = work[row][col]
            work[row] = [left - scale * right
                         for left, right in zip(work[row], work[col])]
    return [row[n:] for row in work]


def determinant(matrix):
    n = len(matrix)
    answer = I(0)
    for permutation in permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(n) for j in range(i + 1, n))
        term = I(-1 if inversions % 2 else 1)
        for i, j in enumerate(permutation):
            term = term * matrix[i][j]
        answer = answer + term
    return answer


def main():
    p, gradient, hessian = p_jets_interval()
    point_p, point_gradient, point_hessian = branch.p_jets(CENTER)
    right_inverse = inverse(point_hessian)
    n = len(CENTER)
    krawczyk = []
    for i in range(n):
        shifted = CENTER[i] - sum(right_inverse[i][j] * point_gradient[j]
                                  for j in range(n))
        correction = I(0)
        for j in range(n):
            residual = I(1 if i == j else 0)
            residual = residual - sum((right_inverse[i][k] * hessian[k][j]
                                       for k in range(n)), I(0))
            correction = correction + residual * I(-RADIUS[j], RADIUS[j])
        image = I(shifted) + correction
        require(BOX[i].lo < image.lo and image.hi < BOX[i].hi,
                (i, BOX[i], image))
        krawczyk.append(image)
    minors = [determinant([row[:size] for row in hessian[:size]])
              for size in range(1, n + 1)]
    require(all(value.lo > 0 for value in minors), minors)
    print("box", BOX)
    print("point", CENTER, "P", point_p, "gradient", point_gradient)
    print("interval P", p)
    print("Krawczyk image", krawczyk)
    print("leading Hessian minors", minors)


if __name__ == "__main__":
    main()
