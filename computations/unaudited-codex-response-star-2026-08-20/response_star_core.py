#!/usr/bin/env python3
"""Raw endpoint-coordinate utilities for the N=8 response-star test.

There is deliberately no import from the W22/W25 cap engines.  A source is
the literal dictionary ``(u,v) -> 3 x 3`` for ``u<v`` and every formula below
is rebuilt from that convention.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations


SITES = tuple(range(8))
COLOURS = tuple(range(3))


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


def parse_fraction(value):
    return value if isinstance(value, Fraction) else Fraction(str(value))


def source_from_json_blocks(blocks):
    source = {}
    for key, matrix in blocks.items():
        clean = key.strip().strip("()")
        u, v = (int(piece.strip()) for piece in clean.split(","))
        if not u < v:
            raise ValueError((key, "source keys must have u<v"))
        source[(u, v)] = [
            [parse_fraction(entry) for entry in row] for row in matrix
        ]
    expected = set(combinations(SITES, 2))
    if set(source) != expected:
        raise ValueError(("edge set mismatch", sorted(expected - set(source))))
    return source


def cell(source, u, v, cu, cv):
    """Literal endpoint-ordered cell, also for a reversed site request."""
    if u < v:
        return source[(u, v)][cu][cv]
    return source[(v, u)][cv][cu]


def hafnian(source, word, vertices=SITES):
    total = Fraction(0)
    for matching in perfect_matchings(tuple(vertices)):
        term = Fraction(1)
        for u, v in matching:
            term *= cell(source, u, v, word[u], word[v])
            if not term:
                break
        total += term
    return total


def off_count(word):
    return 8 - max(word.count(colour) for colour in COLOURS)


def response_row(source, p, q, a, b, alpha, beta, *, mutant=False):
    """Coefficient row of R_ab^{alpha,beta}(K), in K_(i,j) order.

    Here K's first index belongs to endpoint p and its second to q, even if
    p>q.  The formula is

      A_pa[i,alpha] A_qb[j,beta] + A_pb[i,beta] A_qa[j,alpha].

    The optional mutant intentionally swaps the residual colours in the
    second summand; it is used only by a must-fire endpoint-order control.
    """
    if not (p != q and a != b and {p, q}.isdisjoint({a, b})):
        raise ValueError((p, q, a, b))
    row = []
    for i in COLOURS:
        for j in COLOURS:
            first = cell(source, p, a, i, alpha) * cell(
                source, q, b, j, beta
            )
            if mutant:
                second = cell(source, p, b, i, alpha) * cell(
                    source, q, a, j, beta
                )
            else:
                second = cell(source, p, b, i, beta) * cell(
                    source, q, a, j, alpha
                )
            row.append(first + second)
    return row


def response_star_matrix(source, p, q, centre, *, mutant=False):
    residual = tuple(site for site in SITES if site not in (p, q))
    if centre not in residual:
        raise ValueError((p, q, centre))
    rows = []
    labels = []
    for a, b in combinations(residual, 2):
        if centre in (a, b):
            continue
        for alpha in COLOURS:
            for beta in COLOURS:
                labels.append(f"{a}{b}:{alpha}{beta}")
                rows.append(response_row(
                    source, p, q, a, b, alpha, beta, mutant=mutant
                ))
    if len(rows) != 90:
        raise AssertionError(len(rows))
    return labels, rows


def response_triangle_matrix(source, p, q, triangle, *, mutant=False):
    """Rows killing every response edge outside a residual triangle."""
    residual = tuple(site for site in SITES if site not in (p, q))
    triangle = tuple(sorted(triangle))
    if len(triangle) != 3 or not set(triangle).issubset(residual):
        raise ValueError((p, q, triangle))
    allowed = set(combinations(triangle, 2))
    rows = []
    labels = []
    for a, b in combinations(residual, 2):
        if (a, b) in allowed:
            continue
        for alpha in COLOURS:
            for beta in COLOURS:
                labels.append(f"{a}{b}:{alpha}{beta}")
                rows.append(response_row(
                    source, p, q, a, b, alpha, beta, mutant=mutant
                ))
    if len(rows) != 108:
        raise AssertionError(len(rows))
    return labels, rows


def activity_rows(source, p, q):
    answer = []
    for colour in COLOURS:
        row = [Fraction(0)] * 9
        row[3 * colour + colour] = Fraction(1)
        answer.append(row)
    answer.append([
        cell(source, p, q, i, j) for i in COLOURS for j in COLOURS
    ])
    return answer


def rref(rows, ncols=9):
    work = [list(map(parse_fraction, row)) for row in rows]
    pivots = []
    lead = 0
    for row_index in range(len(work)):
        while lead < ncols:
            pivot = next(
                (r for r in range(row_index, len(work)) if work[r][lead]),
                None,
            )
            if pivot is not None:
                break
            lead += 1
        if lead >= ncols:
            break
        work[row_index], work[pivot] = work[pivot], work[row_index]
        scale = work[row_index][lead]
        work[row_index] = [value / scale for value in work[row_index]]
        for other in range(len(work)):
            if other == row_index or not work[other][lead]:
                continue
            scale = work[other][lead]
            work[other] = [
                x - scale * y
                for x, y in zip(work[other], work[row_index])
            ]
        pivots.append(lead)
        lead += 1
    nonzero = [row for row in work if any(row)]
    return nonzero, tuple(pivots)


def rank(rows, ncols=9):
    return len(rref(rows, ncols=ncols)[0])


def nullspace(rows, ncols=9):
    reduced, pivots = rref(rows, ncols=ncols)
    free = [column for column in range(ncols) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Fraction(0)] * ncols
        vector[free_column] = Fraction(1)
        for row, pivot in zip(reduced, pivots):
            vector[pivot] = -row[free_column]
        basis.append(vector)
    return basis


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def add(left, right, scale=Fraction(1)):
    return [a + scale * b for a, b in zip(left, right)]


def avoiding_kernel_vector(rows, functionals):
    """Construct K in ker(rows) avoiding finitely many hyperplanes."""
    basis = nullspace(rows)
    if not basis:
        return None
    for functional in functionals:
        if all(dot(functional, vector) == 0 for vector in basis):
            return None
    current = [Fraction(0)] * 9
    processed = []
    for functional in functionals:
        processed.append(functional)
        if dot(functional, current):
            continue
        direction = next(vector for vector in basis if dot(functional, vector))
        # At most len(processed)-1 nonzero linear forms exclude one t each.
        for integer in range(1, len(processed) + 2):
            candidate = add(current, direction, Fraction(integer))
            if all(dot(prior, candidate) for prior in processed):
                current = candidate
                break
        else:
            raise AssertionError("finite-hyperplane construction failed")
    if any(dot(row, current) for row in rows):
        raise AssertionError("constructed vector is not in kernel")
    if not all(dot(functional, current) for functional in functionals):
        raise AssertionError("constructed vector is inactive")
    return current


def response_star_record(source, p, q, centre):
    labels, rows = response_star_matrix(source, p, q, centre)
    functionals = activity_rows(source, p, q)
    base_rank = rank(rows)
    augmented_ranks = [rank(rows + [functional]) for functional in functionals]
    memberships = [value == base_rank for value in augmented_ranks]
    vector = avoiding_kernel_vector(rows, functionals)
    passes = not any(memberships)
    if passes != (vector is not None):
        raise AssertionError((p, q, centre, memberships, vector))
    return {
        "pair": [p, q],
        "centre": centre,
        "row_labels": labels,
        "rows": rows,
        "rank": base_rank,
        "kernel_dimension": 9 - base_rank,
        "activity_augmented_ranks": augmented_ranks,
        "activity_in_rowspan": memberships,
        "passes": passes,
        "cap": vector,
    }


def response_triangle_record(source, p, q, triangle):
    labels, rows = response_triangle_matrix(source, p, q, triangle)
    functionals = activity_rows(source, p, q)
    base_rank = rank(rows)
    augmented_ranks = [rank(rows + [functional]) for functional in functionals]
    memberships = [value == base_rank for value in augmented_ranks]
    vector = avoiding_kernel_vector(rows, functionals)
    passes = not any(memberships)
    if passes != (vector is not None):
        raise AssertionError((p, q, triangle, memberships, vector))
    return {
        "pair": [p, q],
        "triangle": list(triangle),
        "row_labels": labels,
        "rows": rows,
        "rank": base_rank,
        "kernel_dimension": 9 - base_rank,
        "activity_augmented_ranks": augmented_ranks,
        "activity_in_rowspan": memberships,
        "passes": passes,
        "cap": vector,
    }


def stringify(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, list):
        return [stringify(item) for item in value]
    if isinstance(value, tuple):
        return [stringify(item) for item in value]
    if isinstance(value, dict):
        return {key: stringify(item) for key, item in value.items()}
    return value
