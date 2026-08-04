#!/usr/bin/env python3
"""Explore the second minimally coupled n=8 localized chart (chart 25)."""

import argparse
from collections import Counter, defaultdict
from itertools import permutations, product
import importlib.util
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHARTS = load("n8_charts", "verify_n8_target_triple_localization_orbits.py")
FULL = load("n8_full_source", "verify_n8_full_source_cycle_product_membership.py")
DUAL = load("n8_chart25_dual", "verify_n8_chart25_boundary_dual.py")


def configure_chart25():
    row = tuple(sorted(CHARTS.SOURCE.target_orbit_rows()))[24]
    mate = CHARTS.SOURCE.decode_key(row)
    support = []
    for first, second in CHARTS.SOURCE.mate_edges(mate):
        left, left_colour = divmod(first, 3)
        right, right_colour = divmod(second, 3)
        support.append(FULL.edge(left, right, left_colour, right_colour))
    FULL.SUPPORT_PRODUCT = tuple(sorted(support))
    FULL.SUPPORT_SET = frozenset(support)
    stabilizer = []
    for vertex_permutation in permutations(range(8)):
        for colour_permutation in permutations(range(3)):
            element = vertex_permutation, colour_permutation
            if frozenset(FULL.transform_variable(variable, element)
                         for variable in support) == FULL.SUPPORT_SET:
                stabilizer.append(element)
    if len(stabilizer) != 8:
        raise RuntimeError("chart 25 stabilizer changed")
    FULL.SUPPORT_STABILIZER = tuple(stabilizer)


def first_target_dual(prime, maximum_degree=4):
    rows, columns, layers = FULL.truncated_orbit_component(maximum_degree)
    row_index = {row: index for index, row in enumerate(rows)}
    matrix_columns = []
    pivots = {}
    for position, column in enumerate(columns, 1):
        entries = {
            index: value % prime for index, value in
            FULL.invariant_column_entries(
                column, row_index, maximum_degree
            ).items() if value % prime
        }
        matrix_columns.append(entries)
        vector = dict(entries)
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = pow(value, -1, prime)
                pivots[pivot] = {
                    index: coefficient * inverse % prime
                    for index, coefficient in vector.items()
                }
                break
            for index, coefficient in pivots[pivot].items():
                new = (vector.get(index, 0) - value * coefficient) % prime
                if new:
                    vector[index] = new
                else:
                    vector.pop(index, None)
        if position % 2000 == 0:
            print("columns", position, "/", len(columns),
                  "rank", len(pivots), flush=True)

    target_index = row_index[FULL.SUPPORT_PRODUCT]
    remainder = {target_index: 1}
    while remainder:
        pivot = min(remainder)
        if pivot not in pivots:
            break
        value = remainder[pivot]
        for index, coefficient in pivots[pivot].items():
            new = (remainder.get(index, 0) - value * coefficient) % prime
            if new:
                remainder[index] = new
            else:
                remainder.pop(index, None)
    if not remainder:
        raise RuntimeError("chart 25 boundary entered the truncated span")

    for free_row in sorted(remainder):
        functional = {free_row: 1}
        for pivot in sorted(pivots, reverse=True):
            value = -sum(
                coefficient * functional.get(index, 0)
                for index, coefficient in pivots[pivot].items()
                if index != pivot
            ) % prime
            if value:
                functional[pivot] = value
        target_value = functional.get(target_index, 0)
        if not target_value:
            continue
        inverse = pow(target_value, -1, prime)
        functional = {index: value * inverse % prime
                      for index, value in functional.items()
                      if value * inverse % prime}
        for entries in matrix_columns:
            if sum(functional.get(index, 0) * coefficient
                   for index, coefficient in entries.items()) % prime:
                raise RuntimeError("chart 25 modular dual replay failed")
        break
    else:
        raise RuntimeError("no chart 25 target dual found")

    union = set()
    for index in functional:
        union.update(rows[index])
    signed = Counter(value if value <= prime // 2 else value - prime
                     for value in functional.values())
    return {
        "prime": prime,
        "rows": len(rows),
        "columns": len(columns),
        "rank": len(pivots),
        "left_nullity": len(rows) - len(pivots),
        "layers": layers,
        "free_row": free_row,
        "dual_support": len(functional),
        "dual_union_coordinates": len(union),
        "signed_values": dict(sorted(signed.items())),
        "functional": functional,
        "row_keys": rows,
    }


def exact_expanded_dual(result):
    prime = result["prime"]
    signed = {
        index: value if value <= prime // 2 else value - prime
        for index, value in result["functional"].items()
    }
    rows = result["row_keys"]
    row_index = {row: index for index, row in enumerate(rows)}
    _rows, columns, _layers = FULL.truncated_orbit_component(4)
    for column in columns:
        entries = FULL.invariant_column_entries(column, row_index, 4)
        if sum(signed.get(index, 0) * value
               for index, value in entries.items()):
            raise RuntimeError("chart 25 integer dual does not replay")
    certificate = [
        {
            "sign": signed[index],
            "row": [list(variable) for variable in rows[index]],
        }
        for index in sorted(signed)
    ]
    functional = FULL.expanded_rational_functional(certificate)
    if functional[FULL.SUPPORT_PRODUCT] != 1:
        raise RuntimeError("chart 25 expanded dual lost its target value")
    for column in columns:
        if sum(functional.get(row, 0) for row in FULL.column_rows(column)):
            raise RuntimeError("chart 25 expanded dual does not replay")
    return functional, certificate


def frozen_expanded_dual():
    certificate = [
        {"sign": value, "row": [list(variable) for variable in row]}
        for value, row in DUAL.EXACT_DUAL
    ]
    return FULL.expanded_rational_functional(certificate), certificate


def add_polynomial(target, source, scalar=1):
    for monomial, coefficient in source.items():
        value = target.get(monomial, 0) + scalar * coefficient
        if value:
            target[monomial] = value
        else:
            target.pop(monomial, None)


def multiply(left, right):
    answer = defaultdict(int)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return dict(answer)


def restricted_chart(functional):
    allowed = frozenset(variable for row in functional for variable in row)
    extras = tuple(sorted(allowed - FULL.SUPPORT_SET))
    extra_index = {variable: index for index, variable in enumerate(extras)}

    def coefficient(word):
        answer = defaultdict(int)
        for term in FULL.word_terms(word):
            if any(variable not in allowed for variable in term):
                continue
            monomial = tuple(sorted(
                extra_index[variable] for variable in term
                if variable not in FULL.SUPPORT_SET
            ))
            answer[monomial] += 1
        return dict(answer)

    mixed_by_polynomial = {}
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        polynomial = tuple(sorted(coefficient(word).items()))
        if polynomial:
            mixed_by_polynomial.setdefault(polynomial, word)
    mixed = tuple(dict(polynomial) for polynomial in sorted(mixed_by_polynomial))
    pure = tuple(coefficient((colour,) * 8) for colour in range(3))
    target = {(): 1}
    for polynomial in pure:
        target = multiply(target, polynomial)
    return extras, mixed, pure, target


def singular_polynomial(polynomial, names):
    terms = []
    for monomial, coefficient in sorted(polynomial.items()):
        factors = "*".join(names[index] for index in monomial) or "1"
        terms.append(f"{coefficient}*{factors}")
    return "+".join(terms) or "0"


def singular_membership(extras, mixed, target):
    names = tuple(f"x{index + 1}" for index in range(len(extras)))
    source = [
        f"ring r=0,({','.join(names)}),dp;",
        "option(redSB);",
        "ideal I=" + ",\n".join(
            singular_polynomial(polynomial, names) for polynomial in mixed
        ) + ";",
        "ideal G=std(I);",
        'print("GBSIZE");',
        "size(G);",
        "poly T=" + singular_polynomial(target, names) + ";",
        "poly R=reduce(T,G);",
        'print("REMAINDER_TERMS");',
        "size(R);",
        "R;",
        "matrix L=lift(I,ideal(T));",
        'print("LIFT");',
        "L;",
        "quit;",
    ]
    completed = subprocess.run(
        ["Singular", "-q"], input="\n".join(source), text=True,
        capture_output=True, timeout=600, check=False,
    )
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr)
    if completed.returncode:
        raise RuntimeError(f"Singular exited {completed.returncode}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--singular", action="store_true")
    parser.add_argument("--rediscover-dual", action="store_true")
    args = parser.parse_args()
    configure_chart25()
    print("chart25 support", FULL.SUPPORT_PRODUCT, flush=True)
    if args.rediscover_dual:
        result = first_target_dual(1009)
        print({key: value for key, value in result.items()
               if key not in ("functional", "row_keys")})
        functional, certificate = exact_expanded_dual(result)
    else:
        functional, certificate = frozen_expanded_dual()
    extras, mixed, pure, target = restricted_chart(functional)
    print("exact dual orbit rows", len(certificate),
          "expanded rows", len(functional),
          "allowed coordinates", len(FULL.SUPPORT_SET) + len(extras),
          "chart variables", len(extras),
          "mixed polynomials", len(mixed),
          "pure terms", tuple(len(item) for item in pure),
          "target terms", len(target), flush=True)
    if args.singular:
        singular_membership(extras, mixed, target)


if __name__ == "__main__":
    main()
