#!/usr/bin/env python3
"""Bounded Hamming-two Fredholm test over the exact chi=-12 H1 guard.

The final literal three-row unit is frozen by
``verify_h3_h1_guard_h2_three_row_unit.py``.
"""

from fractions import Fraction as Q
from itertools import combinations, product

import verify_h3_hamming_two_sum_clean_tail_boundary as B


SITES = B.SITES
COLORS = B.COLORS
EDGES = tuple(combinations(SITES, 2))
CROSS_KEYS = tuple(
    (x, y, a, b)
    for x, y in EDGES
    for a, b in product(COLORS, repeat=2)
    if a != b
)
PURE = {
    (x, y, c, c): Q(1)
    for x, y in B.PURE_MATCHING
    for c in COLORS
}


def add(left, right):
    answer = dict(left)
    for monomial, value in right.items():
        answer[monomial] = answer.get(monomial, Q(0)) + value
        if not answer[monomial]:
            del answer[monomial]
    return answer


def scale(value, polynomial):
    return {monomial: value * coefficient for monomial, coefficient in polynomial.items()
            if value * coefficient}


def multiply(left, right):
    answer = {}
    for first, first_value in left.items():
        for second, second_value in right.items():
            monomial = tuple(sorted(first + second))
            answer[monomial] = answer.get(monomial, Q(0)) + first_value * second_value
            if not answer[monomial]:
                del answer[monomial]
    return answer


def q_entry(cross, x, y, a, b):
    if x > y:
        x, y, a, b = y, x, b, a
    if a == b:
        return {(): PURE.get((x, y, a, b), Q(0))}
    return cross[(x, y, a, b)]


def hafnian(cross, word, vertices=SITES):
    answer = {}
    for matching in B.matchings(tuple(vertices)):
        term = {(): Q(1)}
        for x, y in matching:
            term = multiply(term, q_entry(cross, x, y, word[x], word[y]))
        answer = add(answer, term)
    return answer


def residual(cross, row, column, word):
    answer = scale(B.DIRECT.get((row, column), Q(0)), hafnian(cross, word))
    for x, y in EDGES:
        coefficient = (
            B.FIRST.get((row, x, word[x]), Q(0))
            * B.SECOND.get((column, y, word[y]), Q(0))
            + B.FIRST.get((row, y, word[y]), Q(0))
            * B.SECOND.get((column, x, word[x]), Q(0))
        )
        if not coefficient:
            continue
        complement = tuple(site for site in SITES if site not in (x, y))
        answer = add(answer, scale(coefficient, hafnian(cross, word, complement)))
    if row == column and all(color == row for color in word):
        answer = add(answer, {(): Q(-1)})
    return answer


def hamming_words(distance):
    answer = set()
    for base in COLORS:
        for changed in combinations(SITES, distance):
            for defects in product(tuple(c for c in COLORS if c != base), repeat=distance):
                word = [base] * len(SITES)
                for site, color in zip(changed, defects, strict=True):
                    word[site] = color
                answer.add(tuple(word))
    return tuple(sorted(answer))


def h1_affine_graph():
    raw_cross = {key: {(index,): Q(1)} for index, key in enumerate(CROSS_KEYS)}
    equations = []
    for word in hamming_words(1):
        for row, column in product(COLORS, repeat=2):
            polynomial = residual(raw_cross, row, column, word)
            if polynomial:
                equations.append([
                    polynomial.get((index,), Q(0)) for index in range(len(CROSS_KEYS))
                ] + [-polynomial.get((), Q(0))])

    work = [row[:] for row in equations]
    pivot_row = 0
    pivots = []
    for column in range(len(CROSS_KEYS)):
        pivot = next((row for row in range(pivot_row, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right
                         for left, right in zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1

    free = tuple(index for index in range(len(CROSS_KEYS)) if index not in pivots)
    free_index = {column: index for index, column in enumerate(free)}
    graph = {}
    for column in free:
        graph[CROSS_KEYS[column]] = {(free_index[column],): Q(1)}
    for row, column in enumerate(pivots):
        polynomial = {(): work[row][-1]}
        for free_column in free:
            value = -work[row][free_column]
            if value:
                polynomial[(free_index[free_column],)] = value
        graph[CROSS_KEYS[column]] = polynomial
    return graph, len(equations), len(pivots), len(free)


def modular_unit(rows, prime=32003):
    monomials = sorted(
        {monomial for row in rows for monomial in row if monomial},
        key=lambda monomial: (len(monomial), monomial),
    )
    column = {monomial: index for index, monomial in enumerate(monomials)}
    constant_column = len(monomials)
    pivots = {}
    for row_number, polynomial in enumerate(rows):
        current = {}
        for monomial, rational in polynomial.items():
            index = constant_column if not monomial else column[monomial]
            value = rational.numerator * pow(rational.denominator, -1, prime) % prime
            if value:
                current[index] = value
        while current:
            lead = min(current)
            if lead not in pivots:
                inverse = pow(current[lead], -1, prime)
                current = {key: value * inverse % prime for key, value in current.items()}
                pivots[lead] = current
                if lead == constant_column:
                    return True, len(pivots), row_number + 1, len(monomials)
                break
            factor = current[lead]
            for key, value in pivots[lead].items():
                updated = (current.get(key, 0) - factor * value) % prime
                if updated:
                    current[key] = updated
                else:
                    current.pop(key, None)
    return False, len(pivots), len(rows), len(monomials)


def exact_unit(rows):
    monomials = sorted(
        {monomial for row in rows for monomial in row if monomial},
        key=lambda monomial: (len(monomial), monomial),
    )
    column = {monomial: index for index, monomial in enumerate(monomials)}
    constant_column = len(monomials)
    pivots = {}
    pivot_provenance = {}
    for row_number, polynomial in enumerate(rows):
        current = {
            constant_column if not monomial else column[monomial]: value
            for monomial, value in polynomial.items()
            if value
        }
        provenance = {row_number: Q(1)}
        while current:
            lead = min(current)
            if lead not in pivots:
                inverse = Q(1) / current[lead]
                current = {key: value * inverse for key, value in current.items()}
                provenance = {key: value * inverse for key, value in provenance.items()}
                pivots[lead] = current
                pivot_provenance[lead] = provenance
                if lead == constant_column:
                    return provenance
                break
            factor = current[lead]
            for key, value in pivots[lead].items():
                updated = current.get(key, Q(0)) - factor * value
                if updated:
                    current[key] = updated
                else:
                    current.pop(key, None)
            for key, value in pivot_provenance[lead].items():
                updated = provenance.get(key, Q(0)) - factor * value
                if updated:
                    provenance[key] = updated
                else:
                    provenance.pop(key, None)
    return None


def main():
    graph, h1_rows, h1_rank, h1_nullity = h1_affine_graph()
    h2_rows = []
    labels = []
    maximum_degree = 0
    for word in hamming_words(2):
        for row, column in product(COLORS, repeat=2):
            polynomial = residual(graph, row, column, word)
            if polynomial:
                h2_rows.append(polynomial)
                labels.append((row, column, word))
                maximum_degree = max(maximum_degree, max(map(len, polynomial)))
    unit, rank, processed, monomials = modular_unit(h2_rows)
    certificate = exact_unit(h2_rows[:processed]) if unit else None
    print("h3 chi=-12 H1 guard / H2 Fredholm analysis")
    print(f"H1 rows/rank/nullity: {h1_rows}/{h1_rank}/{h1_nullity}")
    print(f"H2 rows/monomials/max-degree: {len(h2_rows)}/{monomials}/{maximum_degree}")
    print(f"mod-32003 rank/processed/unit: {rank}/{processed}/{unit}")
    if certificate is not None:
        print("exact quotient certificate:")
        for index, weight in certificate.items():
            print(weight, labels[index])


if __name__ == "__main__":
    main()
