#!/usr/bin/env python3
"""Find the balanced degree-nine dual; all final identities checked over Q.

Python 3.10+, standard library. Prints a deterministic JSON certificate.
The independent verify.py does not use the modular elimination or this graph
enumerator. No modular nonmembership conclusion is trusted by either script.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import gcd, isqrt, lcm
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


@lru_cache(None)
def graphs(degrees):
    """Loopless multigraphs by allocating all neighbors of the first vertex."""
    if not any(degrees):
        return ((),)
    p = next(i for i, value in enumerate(degrees) if value)
    out = []

    def row(q, left, remaining, edges):
        if q == 6:
            if left == 0:
                for rest in graphs(tuple(remaining)):
                    out.append(tuple(edges) + rest)
            return
        for multiplicity in range(min(left, remaining[q]) + 1):
            updated = list(remaining)
            updated[q] -= multiplicity
            row(q + 1, left - multiplicity, updated,
                edges + [(p, q)] * multiplicity)

    remaining = list(degrees)
    remaining[p] = 0
    row(p + 1, degrees[p], remaining, [])
    return tuple(out)


def monomials(pattern):
    return product(*(graphs((k,) * 6) for k in pattern))


def combine(a, b):
    return tuple(tuple(sorted(x + y)) for x, y in zip(a, b))


def mixed_columns():
    for pattern in product(range(4), repeat=3):
        if sum(pattern) != 3:
            continue
        for word in product(range(3), repeat=6):
            if len(set(word)) == 1:
                continue
            degrees = [tuple(pattern[c] - int(word[i] == c) for i in range(6))
                       for c in range(3)]
            if any(min(d) < 0 or sum(d) % 2 for d in degrees):
                continue
            generator = list(product(*(graphs(tuple(int(word[i] == c)
                                                     for i in range(6)))
                                       for c in range(3))))
            for multiplier in product(*(graphs(d) for d in degrees)):
                yield Counter(combine(g, multiplier) for g in generator)


def balance_columns():
    pure = graphs((1,) * 6)
    for pattern in product(range(3), repeat=3):
        if sum(pattern) != 2:
            continue
        for multiplier in monomials(pattern):
            for c in (1, 2):
                column = Counter()
                for matching in pure:
                    a, b = [(), (), ()], [(), (), ()]
                    a[0] = matching
                    b[c] = matching
                    column[combine(multiplier, a)] += 1
                    column[combine(multiplier, b)] -= 1
                yield {m: value for m, value in column.items() if value}


def rational_lift(value, prime):
    bound = isqrt(prime // 2)
    u, v = (prime, 0), (value, 1)
    while abs(v[0]) > bound:
        quotient = u[0] // v[0]
        u, v = v, (u[0] - quotient * v[0], u[1] - quotient * v[1])
    numerator, denominator = v
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    require(0 < denominator <= bound and abs(numerator) <= bound
            and (value * denominator - numerator) % prime == 0,
            "rational reconstruction failed")
    return Fraction(numerator, denominator)


def build():
    rows = {}
    for pattern in product(range(4), repeat=3):
        if sum(pattern) == 3:
            for monomial in monomials(pattern):
                rows[monomial] = len(rows)
    require(len(rows) == 17355, "degree-nine sector size")
    prime = 2 ** 61 - 1
    pivots = {}

    def reduce(column, save=True):
        vector = {rows[m]: value % prime for m, value in column.items() if value % prime}
        while vector:
            k = min(vector)
            if k not in pivots:
                if save:
                    inverse = pow(vector[k], -1, prime)
                    pivots[k] = {i: a * inverse % prime for i, a in vector.items()}
                return vector
            coefficient = vector[k]
            for i, value in pivots[k].items():
                updated = (vector.get(i, 0) - coefficient * value) % prime
                if updated:
                    vector[i] = updated
                elif i in vector:
                    del vector[i]
        return {}

    for column in mixed_columns():
        reduce(column)
    for column in balance_columns():
        reduce(column)
    target = Counter(product(graphs((1,) * 6), repeat=3))
    residual = reduce(target, save=False)
    require(bool(residual), "target unexpectedly in modular span")
    modular = {min(residual): 1}
    for k in sorted(pivots, reverse=True):
        value = -sum(a * modular.get(i, 0)
                     for i, a in pivots[k].items() if i != k) % prime
        if value:
            modular[k] = value
    exact = {monomial: rational_lift(modular[i], prime)
             for monomial, i in rows.items() if i in modular}
    # Candidate discovery ends here. These exact rational identities justify it.
    for columns in (mixed_columns(), balance_columns()):
        for column in columns:
            require(sum(a * exact.get(m, 0) for m, a in column.items()) == 0,
                    "candidate does not annihilate an exact integer column")
    target_value = sum(a * exact.get(m, 0) for m, a in target.items())
    require(target_value != 0, "candidate does not separate the target")
    denominator = lcm(*(a.denominator for a in exact.values()))
    integer = {m: int(a * denominator) for m, a in exact.items()}
    divisor = gcd(*integer.values())
    integer = {m: a // divisor for m, a in integer.items()}
    target_value = int(target_value * denominator / divisor)
    edges = list(combinations(range(6), 2))
    edge_id = {edge: i for i, edge in enumerate(edges)}
    functional = []
    for monomial, value in integer.items():
        encoded = [c * 15 + edge_id[edge] for c, graph in enumerate(monomial) for edge in graph]
        functional.append([encoded, value])
    functional.sort()
    return {"format": "diagonal-edge-cell-ids-v1", "edge_order": edges,
            "target": "tau_a * tau_b * tau_c",
            "target_evaluation": target_value, "functional": functional}


def render(certificate):
    """One functional entry per line keeps a 1,296-entry certificate readable."""
    keys = ["format", "edge_order", "target", "target_evaluation"]
    prefix = ",\n".join("  " + json.dumps(key) + ": " + json.dumps(certificate[key])
                         for key in keys)
    entries = ",\n".join("    " + json.dumps(row) for row in certificate["functional"])
    return "{\n" + prefix + ',\n  "functional": [\n' + entries + "\n  ]\n}\n"


if __name__ == "__main__":
    print(render(build()), end="")
