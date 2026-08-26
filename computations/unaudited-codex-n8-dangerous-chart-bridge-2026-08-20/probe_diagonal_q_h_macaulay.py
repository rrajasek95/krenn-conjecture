#!/usr/bin/env python3
"""Low-degree modular Macaulay probe for H in I_branch+(Q_s).

This is a discovery tool.  A positive modular answer is only a candidate for
exact-Q reconstruction; a negative answer at a cutoff is only cutoff-relative.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations_with_replacement
import importlib.util
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
CORE = HERE / "audit_diagonal_cofactor_branch_orbits.py"
SPEC = importlib.util.spec_from_file_location("cofactor_core", CORE)
core = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(core)


def max_degree(poly):
    return max(map(len, poly), default=0)


def multipliers(variable_count, degree):
    for current in range(degree + 1):
        yield from combinations_with_replacement(range(variable_count), current)


def multiply(poly, monomial, prime):
    return {tuple(sorted(term + monomial)): coefficient % prime
            for term, coefficient in poly.items() if coefficient % prime}


def add_scaled(left, right, scale, prime):
    for row, coefficient in right.items():
        value = (left.get(row, 0) - scale * coefficient) % prime
        if value:
            left[row] = value
        elif row in left:
            del left[row]


def generators(mask, q_indices, rabinowitsch=False):
    rows = [(f"per{edge}", core.permanent_poly(edge)) for edge in range(6)]
    rows += [(f"tau{''.join(map(str, triple))}", core.triangle_poly(*triple))
             for triple in core.TRIPLES]
    for edge, (i, j) in enumerate(core.EDGES):
        entries = (((0, 1), (1, 0)) if (mask >> edge) & 1
                   else ((0, 0), (1, 1)))
        for x, y in entries:
            rows.append((f"C{2*i+x}{2*j+y}",
                         core.cofactor_poly(2 * i + x, 2 * j + y)))
    rows.extend((f"Q{q_index}", core.q_poly(q_index)) for q_index in q_indices)
    if rabinowitsch:
        hafnian = core.matching_poly(tuple(range(8)))
        rows.append(("uH_minus_1", core.normalize_poly(
            tuple((coefficient, monomial + (24,))
                  for monomial, coefficient in hafnian.items())
            + ((-1, ()),))))
    return rows


def solve(mask, q_indices, cutoff, prime, rabinowitsch=False):
    source_generators = generators(mask, q_indices, rabinowitsch)
    variable_count = 25 if rabinowitsch else 24
    columns = []
    for name, poly in source_generators:
        budget = cutoff - max_degree(poly)
        if budget < 0:
            continue
        for monomial in multipliers(variable_count, budget):
            columns.append((name, monomial, multiply(poly, monomial, prime)))
    # Highest-degree grevlex-like tuple pivot first; degree filtration is
    # preserved because the row key includes the entire commutative monomial.
    pivots = {}
    dependent = 0
    started = time.monotonic()
    for column_index, (_, _, raw) in enumerate(columns):
        vector = dict(raw)
        while vector:
            pivot = max(vector, key=lambda row: (len(row), row))
            if pivot not in pivots:
                inverse = pow(vector[pivot], -1, prime)
                vector = {row: coefficient * inverse % prime
                          for row, coefficient in vector.items()}
                pivots[pivot] = (column_index, vector)
                break
            factor = vector[pivot]
            add_scaled(vector, pivots[pivot][1], factor, prime)
        else:
            dependent += 1
    target_poly = ({(): 1} if rabinowitsch
                   else core.matching_poly(tuple(range(8))))
    target = {row: coefficient % prime for row, coefficient
              in target_poly.items() if coefficient % prime}
    reduction_steps = 0
    while target:
        pivot = max(target, key=lambda row: (len(row), row))
        if pivot not in pivots:
            break
        factor = target[pivot]
        add_scaled(target, pivots[pivot][1], factor, prime)
        reduction_steps += 1
    return {
        "mask": mask,
        "q_indices": list(q_indices),
        "cutoff": cutoff,
        "prime": prime,
        "rabinowitsch_target_one": rabinowitsch,
        "generator_count": len(source_generators),
        "column_count": len(columns),
        "rank": len(pivots),
        "dependent_columns": dependent,
        "target_in_span": not target,
        "target_residual_size": len(target),
        "target_reduction_steps": reduction_steps,
        "elapsed_seconds": time.monotonic() - started,
        "first_residual_rows": [list(row) for row in sorted(
            target, key=lambda row: (len(row), row), reverse=True)[:8]],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask", type=int, default=0)
    parser.add_argument("--cutoff", type=int, default=4)
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--q", type=int, nargs="*", default=list(range(16)))
    parser.add_argument("--together", action="store_true")
    parser.add_argument("--rabinowitsch", action="store_true")
    args = parser.parse_args()
    groups = [tuple(args.q)] if args.together else [(q_index,) for q_index in args.q]
    for q_indices in groups:
        result = solve(args.mask, q_indices, args.cutoff, args.prime,
                       args.rabinowitsch)
        print(result, flush=True)


if __name__ == "__main__":
    main()
