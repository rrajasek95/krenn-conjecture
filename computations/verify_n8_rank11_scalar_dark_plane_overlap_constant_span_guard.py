#!/usr/bin/env python3
"""Exact low-degree source guard for the dark-plane overlap caps.

Keep the endpoint stars/direct block of the fixed-dark rational normal form,
but replace its internal six-site quadratic by all 135 independent decorated
cells.  This checker builds every nonzero coefficient of the original nine
source rows and the homogeneous clean errors of the two nontrivial overlap
caps found by the all-pair audit.  Exact sparse elimination over QQ shows
that constant source-row combinations do not imply either clean cap.  A
three-term repeated-site quadratic coefficient additionally proves that no
source identity with multiplier degree at most one can imply the first cap.
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path


Q = Fraction
ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "computations/verify_n8_rank11_scalar_dark_plane_second_chart_line_audit.py"
EXPECTED_DIGEST = "770d44910eafc2b7ed8d6d5bd71bc1d0b6ef99a3f5f9430108e063491bc11e03"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_audit():
    spec = importlib.util.spec_from_file_location("dark_pair_audit", AUDIT)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "failed to load the all-pair audit")
    spec.loader.exec_module(module)
    return module


def padd(*polynomials):
    out = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] = out.get(monomial, Q(0)) + coefficient
            if not out[monomial]:
                del out[monomial]
    return out


def pscale(scalar, polynomial):
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def pmultiply(left, right):
    out = {}
    for first, a in left.items():
        for second, b in right.items():
            monomial = tuple(sorted(first + second))
            out[monomial] = out.get(monomial, Q(0)) + a * b
            if not out[monomial]:
                del out[monomial]
    return out


def eadd(*elements):
    out = {}
    for element in elements:
        for word, polynomial in element.items():
            out[word] = padd(out.get(word, {}), polynomial)
            if not out[word]:
                del out[word]
    return out


def escale(polynomial, element):
    return {word: pmultiply(polynomial, coefficient)
            for word, coefficient in element.items()
            if pmultiply(polynomial, coefficient)}


def emultiply(left, right):
    out = {}
    for u, a in left.items():
        for v, b in right.items():
            if any(x != -1 and y != -1 for x, y in zip(u, v)):
                continue
            word = tuple(x if x != -1 else y for x, y in zip(u, v))
            out[word] = padd(out.get(word, {}), pmultiply(a, b))
            if not out[word]:
                del out[word]
    return out


AUDIT_MODULE = load_audit()
BASE_BLOCKS = AUDIT_MODULE.build_blocks()
Q_CELLS = tuple(
    (u, v, a, b)
    for u, v in combinations(range(6), 2)
    for a, b in product(range(3), repeat=2)
)
VARIABLE_INDEX = {cell: index for index, cell in enumerate(Q_CELLS)}


def coefficient(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    key = (u, v, a, b)
    if u < 6 and v < 6:
        return {(VARIABLE_INDEX[key],): Q(1)}
    value = BASE_BLOCKS.get(key, Q(0))
    return {(): value} if value else {}


def pair_data(endpoints, labels):
    residual = tuple(site for site in range(8) if site not in endpoints)
    cap = {
        (i, j): Q(int((i, j) == labels) + int(i == j))
        for i, j in product(range(3), repeat=2)
    }
    direct = {}
    for i, j in product(range(3), repeat=2):
        direct = padd(
            direct,
            pscale(cap[i, j], coefficient(*endpoints, i, j)),
        )
    internal = {}
    response = {}
    for u, v in combinations(residual, 2):
        for c, d in product(range(3), repeat=2):
            word = [-1] * 6
            word[residual.index(u)] = c
            word[residual.index(v)] = d
            word = tuple(word)
            value = coefficient(u, v, c, d)
            if value:
                internal[word] = value
            response_value = {}
            for i, j in product(range(3), repeat=2):
                response_value = padd(
                    response_value,
                    pscale(cap[i, j], padd(
                        pmultiply(coefficient(endpoints[0], u, i, c),
                                  coefficient(endpoints[1], v, j, d)),
                        pmultiply(coefficient(endpoints[0], v, i, d),
                                  coefficient(endpoints[1], u, j, c)),
                    )),
                )
            if response_value:
                response[word] = response_value
    return direct, internal, response


def clean_error(endpoints, labels):
    direct, internal, response = pair_data(endpoints, labels)
    response2 = emultiply(response, response)
    return eadd(
        escale(pscale(Q(3), direct), emultiply(response2, internal)),
        emultiply(response2, response),
    )


def source_rows():
    internal = {}
    for u, v in combinations(range(6), 2):
        for a, b in product(range(3), repeat=2):
            word = [-1] * 6
            word[u], word[v] = a, b
            internal[tuple(word)] = coefficient(u, v, a, b)
    internal2 = emultiply(internal, internal)
    internal3 = emultiply(internal2, internal)
    rows = []
    for i, j in product(range(3), repeat=2):
        direct = coefficient(6, 7, i, j)
        response = {}
        for u, v in combinations(range(6), 2):
            for a, b in product(range(3), repeat=2):
                word = [-1] * 6
                word[u], word[v] = a, b
                value = padd(
                    pmultiply(coefficient(6, u, i, a),
                              coefficient(7, v, j, b)),
                    pmultiply(coefficient(6, v, i, b),
                              coefficient(7, u, j, a)),
                )
                if value:
                    response[tuple(word)] = value
        equation = eadd(
            escale(pscale(Q(1, 6), direct), internal3),
            escale({(): Q(1, 2)}, emultiply(response, internal2)),
        )
        if i == j:
            target = tuple([i] * 6)
            equation[target] = padd(
                equation.get(target, {}), {(): Q(-1)})
        rows.extend(equation.values())
    return rows


def reduce_exact(polynomial, basis, insert=False):
    row = dict(polynomial)
    while row:
        pivot = min(row, key=lambda monomial: (len(monomial), monomial))
        if pivot not in basis:
            if not insert:
                return row
            inverse = Q(1) / row[pivot]
            row = {monomial: coefficient * inverse
                   for monomial, coefficient in row.items()}
            basis[pivot] = row
            return {}
        factor = row[pivot]
        for monomial, coefficient in basis[pivot].items():
            value = row.get(monomial, Q(0)) - factor * coefficient
            if value:
                row[monomial] = value
            else:
                row.pop(monomial, None)
    return {}


def exact_span_audit(rows, target_groups):
    basis = {}
    for row in rows:
        reduce_exact(row, basis, insert=True)
    group_records = []
    all_remainders = []
    for endpoints, targets in target_groups:
        zero = 0
        nonzero_sizes = []
        for target in targets:
            remainder = reduce_exact(target, basis)
            if remainder:
                nonzero_sizes.append(len(remainder))
                all_remainders.append(len(remainder))
            else:
                zero += 1
        group_records.append((endpoints, zero, len(targets),
                              min(nonzero_sizes), max(nonzero_sizes)))
    return len(basis), group_records, min(all_remainders), max(all_remainders)


def disjoint_edge_monomial(monomial):
    endpoints = []
    for index in monomial:
        u, v, _a, _b = Q_CELLS[index]
        endpoints.extend((u, v))
    return len(endpoints) == len(set(endpoints))


def main():
    rows = source_rows()
    target_errors = [
        (endpoints, clean_error(endpoints, labels))
        for endpoints, labels in (
            ((1, 7), (0, 2)),
            ((2, 7), (0, 1)),
        )
    ]
    target_groups = [(endpoints, list(error.values()))
                     for endpoints, error in target_errors]
    rank_value, groups, minimum, maximum = exact_span_audit(rows, target_groups)

    # The physical residual sites of cap 17 are (0,2,3,4,5,6).  At output
    # 000122 its clean error is a nonzero quadratic supported on two q-edges
    # which meet at site 1.  In contrast, every degree-two monomial in an
    # original source coefficient is a two-edge matching and hence disjoint.
    # Source coefficients have no degree-one monomial.  Consequently, after
    # multiplying source coefficients by arbitrary polynomials of q-degree at
    # most one, the repeated-site degree-two projection is still zero.  This
    # excludes the target independently of every possible quartic-tail
    # cancellation among the linear multiples.
    obstruction_word = (0, 0, 0, 1, 2, 2)
    obstruction = target_errors[0][1][obstruction_word]
    index = VARIABLE_INDEX
    expected_obstruction = {
        tuple(sorted((index[(0, 1, 0, 1)], index[(1, 3, 1, 0)]))): Q(48),
        tuple(sorted((index[(0, 1, 0, 1)], index[(1, 3, 2, 0)]))): Q(24),
        tuple(sorted((index[(0, 1, 0, 2)], index[(1, 3, 1, 0)]))): Q(24),
    }
    require(obstruction == expected_obstruction,
            ("the degree-one obstruction coefficient changed", obstruction))
    source_linear_terms = sum(1 for row in rows for monomial in row
                              if len(monomial) == 1)
    source_quadratic_terms = [monomial for row in rows for monomial in row
                              if len(monomial) == 2]
    require(source_linear_terms == 0, "a source coefficient gained a linear term")
    require(all(disjoint_edge_monomial(monomial)
                for monomial in source_quadratic_terms),
            "a source quadratic monomial reused a physical site")
    require(all(not disjoint_edge_monomial(monomial)
                for monomial in obstruction),
            "the obstruction lost its repeated physical site")

    ledger = {
        "variable_count": len(Q_CELLS),
        "source_rows": len(rows),
        "source_terms": sum(map(len, rows)),
        "source_rank": rank_value,
        "target_rows": sum(len(group) for _, group in target_groups),
        "target_terms": sum(len(row) for _, group in target_groups for row in group),
        "groups": groups,
        "remainder_range": (minimum, maximum),
        "degree_le_one_guard": {
            "word": obstruction_word,
            "terms": tuple(sorted(obstruction.items())),
            "source_linear_terms": source_linear_terms,
            "source_quadratic_occurrences": len(source_quadratic_terms),
            "source_quadratic_unique": len(set(source_quadratic_terms)),
        },
    }
    require(ledger == {
        "variable_count": 135,
        "source_rows": 4737,
        "source_terms": 63183,
        "source_rank": 1579,
        "target_rows": 828,
        "target_terms": 35433,
        "groups": [((1, 7), 54, 339, 3, 227),
                   ((2, 7), 48, 489, 3, 348)],
        "remainder_range": (3, 348),
        "degree_le_one_guard": {
            "word": (0, 0, 0, 1, 2, 2),
            "terms": tuple(sorted(expected_obstruction.items())),
            "source_linear_terms": 0,
            "source_quadratic_occurrences": 30375,
            "source_quadratic_unique": 3645,
        },
    }, ("constant-span ledger changed", ledger))
    digest = sha256(repr(ledger).encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, ("ledger digest changed", digest))
    print("N=8 dark-plane overlap constant-row-span guard: passed")
    print(f"  variables / source rows / rank : 135 / 4737 / {rank_value}")
    print(f"  cap-17 zero/total              : {groups[0][1]} / {groups[0][2]}")
    print(f"  cap-27 zero/total              : {groups[1][1]} / {groups[1][2]}")
    print(f"  surviving remainder range      : {minimum} .. {maximum}")
    print("  source multiplier degree <= 1  : excluded by repeated-site q^2")
    print(f"  ledger sha256                  : {digest}")


if __name__ == "__main__":
    main()
