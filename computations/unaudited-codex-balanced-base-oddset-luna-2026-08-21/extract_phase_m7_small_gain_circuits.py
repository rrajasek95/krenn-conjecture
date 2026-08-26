#!/usr/bin/env python3
"""Enumerate every deletion-minimal inconsistent binomial circuit of size <= 3.

The input is one exported CEGAR coefficient target.  A binomial row is written
as ``x^v = c`` over Q(w), w^2+w+1=0.  We enumerate all one-, two-, and
three-row integer dependencies among the exponent vectors and retain exactly
those whose product of constants is not one.  For three rows, pairwise
independence is precisely deletion minimality.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import reduce
from itertools import combinations
import json
from math import gcd
from pathlib import Path

from audit_phase_m7_1222_k4_toric import parse_q
from cegar_phase_m7_1222_k4_support import qdiv, qinv, qlabel, qmul, qneg


HERE = Path(__file__).resolve().parent


def qpow(value, exponent):
    if exponent < 0:
        return qpow(qinv(value), -exponent)
    answer = (Fraction(1), Fraction(0))
    base = value
    while exponent:
        if exponent & 1:
            answer = qmul(answer, base)
        base = qmul(base, base)
        exponent //= 2
    return answer


def primitive(values):
    common = reduce(gcd, (abs(value) for value in values if value), 0)
    values = tuple(value // common for value in values)
    first = next(value for value in values if value)
    return tuple(-value for value in values) if first < 0 else values


def sparse_vector(row, positions):
    vector = {}
    left, right = row["terms"]
    for name in left["monomial"]:
        index = positions[name]
        vector[index] = vector.get(index, 0) + 1
    for name in right["monomial"]:
        index = positions[name]
        vector[index] = vector.get(index, 0) - 1
    return {index: value for index, value in vector.items() if value}


def pair_relation(left, right):
    """Return a primitive relation a*left+b*right=0, else None."""
    if not left or not right:
        return None
    pivot = next(iter(left))
    if not right.get(pivot):
        return None
    relation = primitive((right[pivot], -left[pivot]))
    if all(relation[0] * left.get(index, 0)
           + relation[1] * right.get(index, 0) == 0
           for index in left.keys() | right.keys()):
        return relation
    return None


def pair_minor(left, right):
    """Return coordinates of a nonzero 2x2 minor, else None."""
    support = sorted(left.keys() | right.keys())
    for p_index, p in enumerate(support):
        for q in support[p_index + 1:]:
            if left.get(p, 0) * right.get(q, 0) != left.get(q, 0) * right.get(p, 0):
                return p, q
    return None


def triple_relation(left, middle, right, minor):
    p, q = minor
    relation = primitive((
        middle.get(p, 0) * right.get(q, 0) - middle.get(q, 0) * right.get(p, 0),
        right.get(p, 0) * left.get(q, 0) - right.get(q, 0) * left.get(p, 0),
        left.get(p, 0) * middle.get(q, 0) - left.get(q, 0) * middle.get(p, 0),
    ))
    if not all(relation):
        return None
    if all(relation[0] * left.get(index, 0)
           + relation[1] * middle.get(index, 0)
           + relation[2] * right.get(index, 0) == 0
           for index in left.keys() | middle.keys() | right.keys()):
        return relation
    return None


def det3(left, middle, right, p, q, r):
    return (
        left.get(p, 0) * (middle.get(q, 0) * right.get(r, 0)
                          - middle.get(r, 0) * right.get(q, 0))
        - middle.get(p, 0) * (left.get(q, 0) * right.get(r, 0)
                              - left.get(r, 0) * right.get(q, 0))
        + right.get(p, 0) * (left.get(q, 0) * middle.get(r, 0)
                             - left.get(r, 0) * middle.get(q, 0))
    )


def triple_pivots(left, middle, right, minor):
    p, q = minor
    for r in sorted((left.keys() | middle.keys() | right.keys()) - {p, q}):
        if det3(left, middle, right, p, q, r):
            return p, q, r
    return None


def four_relation(first, second, third, fourth, pivots):
    p, q, r = pivots
    relation = primitive((
        det3(second, third, fourth, p, q, r),
        -det3(first, third, fourth, p, q, r),
        det3(first, second, fourth, p, q, r),
        -det3(first, second, third, p, q, r),
    ))
    if not all(relation):
        return None
    if all(relation[0] * first.get(index, 0)
           + relation[1] * second.get(index, 0)
           + relation[2] * third.get(index, 0)
           + relation[3] * fourth.get(index, 0) == 0
           for index in first.keys() | second.keys() | third.keys() | fourth.keys()):
        return relation
    return None


def inconsistent(constants, powers):
    product = (Fraction(1), Fraction(0))
    for constant, power in zip(constants, powers):
        product = qmul(product, qpow(constant, power))
    return product if product != (Fraction(1), Fraction(0)) else None


def atom_name(label):
    edge, rest = label.split(":")
    colours, degree = rest.split("@")
    return f"x_{edge[0]}_{edge[1]}_{colours[0]}_{colours[1]}_{degree}"


def descriptor(row):
    return {
        "word": row["word"],
        "degree": row["degree"],
        "active_monomials": [
            [atom_name(label) for label in term["monomial"]]
            for term in row["terms"]
        ],
        "equation_terms": row["terms"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--size4-cap", type=int, default=0,
        help="Probe size-4 circuits until cap+1; zero disables the probe.",
    )
    args = parser.parse_args()

    system = json.loads(args.input.read_text())["coefficient_system"]
    positions = {name: index for index, name in enumerate(system["variables"])}
    rows = [row for row in system["equations"] if len(row["terms"]) == 2]
    vectors = [sparse_vector(row, positions) for row in rows]
    constants = [qneg(qdiv(parse_q(row["terms"][1]["coefficient"]),
                            parse_q(row["terms"][0]["coefficient"])))
                 for row in rows]

    circuits = []
    by_size = {1: 0, 2: 0, 3: 0}

    for index, vector in enumerate(vectors):
        if not vector:
            failure = inconsistent((constants[index],), (1,))
            if failure is not None:
                circuits.append(((index,), (1,), failure))

    dependent_pairs = set()
    independent_minors = {}
    for left, right in combinations(range(len(rows)), 2):
        relation = pair_relation(vectors[left], vectors[right])
        if relation is not None:
            dependent_pairs.add((left, right))
            failure = inconsistent((constants[left], constants[right]), relation)
            if failure is not None:
                circuits.append(((left, right), relation, failure))
        else:
            minor = pair_minor(vectors[left], vectors[right])
            if minor is not None:
                independent_minors[(left, right)] = minor

    for left, middle, right in combinations(range(len(rows)), 3):
        if ((left, middle) in dependent_pairs or (left, right) in dependent_pairs
                or (middle, right) in dependent_pairs):
            continue
        minor = independent_minors.get((left, middle))
        if minor is None:
            continue
        relation = triple_relation(vectors[left], vectors[middle], vectors[right], minor)
        if relation is None:
            continue
        failure = inconsistent(
            (constants[left], constants[middle], constants[right]), relation)
        if failure is not None:
            circuits.append(((left, middle, right), relation, failure))

    size4_probe = []
    size4_threshold_exceeded = False
    if args.size4_cap:
        pivot_cache = {}
        for first, second, third, fourth in combinations(range(len(rows)), 4):
            if ((first, second) in dependent_pairs
                    or (first, third) in dependent_pairs
                    or (second, third) in dependent_pairs):
                continue
            triple = (first, second, third)
            if triple not in pivot_cache:
                minor = independent_minors.get((first, second))
                pivot_cache[triple] = (
                    triple_pivots(vectors[first], vectors[second], vectors[third], minor)
                    if minor is not None else None
                )
            pivots = pivot_cache[triple]
            if pivots is None:
                continue
            relation = four_relation(
                vectors[first], vectors[second], vectors[third], vectors[fourth], pivots)
            if relation is None:
                continue
            failure = inconsistent(
                (constants[first], constants[second], constants[third], constants[fourth]),
                relation,
            )
            if failure is None:
                continue
            size4_probe.append({
                "row_indices": [first, second, third, fourth],
                "powers": list(relation),
                "product_constant": qlabel(failure),
                "rows": [descriptor(rows[index])
                         for index in (first, second, third, fourth)],
            })
            if len(size4_probe) > args.size4_cap:
                size4_threshold_exceeded = True
                break

    output_circuits = []
    for indices, powers, failure in circuits:
        by_size[len(indices)] += 1
        output_circuits.append({
            "kind": f"deletion-minimal {len(indices)}-binomial constant-failure circuit",
            "row_indices": list(indices),
            "powers": list(powers),
            "product_constant": qlabel(failure),
            "contradiction_scalar": qlabel((failure[0] - 1, failure[1])),
            "rows": [descriptor(rows[index]) for index in indices],
        })

    output = {
        "scope": "all deletion-minimal inconsistent binomial circuits with <=3 rows",
        "field": "Q(omega), omega^2+omega+1=0",
        "binomial_rows": len(rows),
        "counts_by_size": by_size,
        "circuit_count": len(output_circuits),
        "seed_stabilizer_order": 1,
        "distinct_circuit_orbits": len(output_circuits),
        "circuits": output_circuits,
        "size4_probe_cap": args.size4_cap,
        "size4_probe_count": len(size4_probe),
        "size4_threshold_exceeded": size4_threshold_exceeded,
        "size4_probe": size4_probe,
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: output[key] for key in (
        "binomial_rows", "counts_by_size", "circuit_count",
        "distinct_circuit_orbits",
    )}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
