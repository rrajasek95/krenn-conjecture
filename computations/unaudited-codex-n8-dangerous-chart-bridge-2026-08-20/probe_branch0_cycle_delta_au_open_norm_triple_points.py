#!/usr/bin/env python3
"""Enumerate F_1009-rational points of the three pair-norm factors."""

from __future__ import annotations

from pathlib import Path
import re

import numpy as np


HERE = Path(__file__).resolve().parent
PRIME = 1009


def parse_sparse(value):
    terms = []
    for token in value.strip().replace("-", "+-").split("+"):
        if not token:
            continue
        coefficient = -1 if token.startswith("-") else 1
        token = token.removeprefix("-")
        d_degree = 0
        x_degree = 0
        for factor in token.split("*"):
            if factor == "d1":
                d_degree += 1
            elif factor.startswith("d1^"):
                d_degree += int(factor[3:])
            elif factor == "x":
                x_degree += 1
            elif factor.startswith("x^"):
                x_degree += int(factor[2:])
            else:
                coefficient *= int(factor)
        terms.append((d_degree, x_degree, coefficient % PRIME))
    return terms


def power_table(max_degree):
    values = np.arange(PRIME, dtype=np.int64)
    table = np.ones((PRIME, max_degree + 1), dtype=np.int64)
    for degree in range(1, max_degree + 1):
        table[:, degree] = table[:, degree-1] * values % PRIME
    return table


def evaluate(terms, d_powers, x_powers):
    coefficients = np.zeros((d_powers.shape[1], x_powers.shape[1]),
                            dtype=np.int64)
    for d_degree, x_degree, coefficient in terms:
        coefficients[d_degree, x_degree] = (
            coefficients[d_degree, x_degree] + coefficient) % PRIME
    return ((d_powers @ coefficients % PRIME) @ x_powers.T) % PRIME


def main():
    sparse = {}
    for pair in ("LR", "LT", "RT"):
        path = HERE / f"branch0_cycle_delta_au_open_norm_{pair}_p1009.factor"
        sparse[pair] = parse_sparse(path.read_text())
    max_d = max(term[0] for terms in sparse.values() for term in terms)
    max_x = max(term[1] for terms in sparse.values() for term in terms)
    d_powers = power_table(max_d)
    x_powers = power_table(max_x)
    masks = {}
    for pair, terms in sparse.items():
        values = evaluate(terms, d_powers, x_powers)
        masks[pair] = values == 0
        print(pair, "terms", len(terms), "rational zeros",
              int(masks[pair].sum()))
    common = masks["LR"] & masks["LT"] & masks["RT"]
    points = np.argwhere(common)
    print("common rational points", len(points))
    for d1, x in points[:100]:
        print(int(d1), int(x))
    open_points = []
    for d1_value, x_value in points:
        d1 = int(d1_value)
        x = int(x_value)
        a = ((d1-1)**2*x-(d1+1)**2) % PRIME
        c = (-d1**2*x**3+d1**2*x**2+2*d1*x**2
             +2*d1*x-x+1) % PRIME
        if d1 and x and x != 1 and a and c:
            open_points.append((d1, x))
    print("basic parameter-open points", len(open_points))
    for point in open_points:
        print("open", *point)


if __name__ == "__main__":
    main()
