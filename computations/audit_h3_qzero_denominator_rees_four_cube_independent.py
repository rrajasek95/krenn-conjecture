#!/usr/bin/env python3
"""Independent audit of the h=3 q-zero denominator/Rees four-cube.

The script independently reconstructs the polynomial principal-parts data
and then audits the implementation of the augmented readout claim.  It does
not import the primary checker.  Exact rational arithmetic is used.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path


Q = Fraction
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
MIXED = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, R, P, QSITE = 0, 3, 6, 7
PRIMARY = Path(__file__).with_name(
    "verify_h3_qzero_denominator_rees_four_cube.py"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def cell(left, right, left_colour=0, right_colour=0):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def decorated(matching, colouring):
    return tuple(sorted(
        cell(left, right, colouring[left], colouring[right])
        for left, right in matching
    ))


def differentiate(polynomial, variables):
    answer = defaultdict(Q)
    for monomial, coefficient in polynomial.items():
        remainder = list(monomial)
        for variable in variables:
            if variable not in remainder:
                break
            remainder.remove(variable)
        else:
            answer[tuple(sorted(remainder))] += coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def contains_pair(monomial, pair):
    target = frozenset(pair)
    return any(frozenset((left, right)) == target
               for left, right, _a, _b in monomial)


def mixed_word(deleted):
    word = [0] * 8
    for site in ODD:
        if site != deleted:
            word[site] = MIXED[site]
    return tuple(word)


def full_row(deleted):
    word = mixed_word(deleted)
    colouring = dict(enumerate(word))
    answer = {}
    for matching in perfect_matchings(SITES):
        if any(frozenset(pair) == frozenset((P, R)) for pair in matching):
            continue
        answer[decorated(matching, colouring)] = Q(1)
    require(len(answer) == 90, "direct-free row size")
    return answer


def face_polynomial(deleted):
    sites = tuple(site for site in ODD if site != deleted)
    colouring = {site: MIXED[site] for site in sites}
    return {
        decorated(matching, colouring): Q(1)
        for matching in perfect_matchings(sites)
    }


def rank(columns):
    pivots = {}
    for source in columns:
        column = {row: Q(value) for row, value in enumerate(source) if value}
        while column:
            pivot = min(column)
            value = column[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in column.items()
                }
                break
            for row, coefficient in pivots[pivot].items():
                new = column.get(row, Q(0)) - value * coefficient
                if new:
                    column[row] = new
                else:
                    column.pop(row, None)
    return len(pivots)


def in_span(vector, rows):
    return rank(list(rows) + [vector]) == rank(rows)


def audit_literal_polars_and_derivative_cubes():
    records = 0
    labelled_columns = []
    for deleted_index, deleted in enumerate(ODD):
        row = full_row(deleted)
        u = cell(X, deleted)
        t = cell(P, QSITE)
        h = face_polynomial(deleted)
        require(differentiate(row, (u, t)) == h, "external polar")

        pq_direct = {
            monomial: value for monomial, value in row.items()
            if contains_pair(monomial, (P, QSITE))
        }
        pq_star = {monomial: value for monomial, value in row.items()
                   if monomial not in pq_direct}
        pr_direct = {
            monomial: value for monomial, value in row.items()
            if contains_pair(monomial, (P, R))
        }
        pr_star = {monomial: value for monomial, value in row.items()
                   if monomial not in pr_direct}
        require(differentiate(pq_direct, (u, t)) == h, "pq direct face")
        require(not differentiate(pq_star, (u, t)), "pq star leakage")
        require(not differentiate(pr_direct, (u, t)), "pr direct leakage")
        require(differentiate(pr_star, (u, t)) == h, "pr star face")

        for matching in perfect_matchings(tuple(
                site for site in ODD if site != deleted)):
            internal = decorated(
                matching,
                {site: MIXED[site] for site in ODD if site != deleted},
            )
            directions = (u, t) + internal
            require(differentiate(row, directions) == {(): Q(1)},
                    "four-polar is not one")

            # Every square in the literal 4-direction derivative cube
            # commutes.  This is the actual functorial PP assertion.
            for first, second in combinations(range(4), 2):
                remaining = tuple(
                    directions[index] for index in range(4)
                    if index not in (first, second)
                )
                base = differentiate(row, remaining)
                left = differentiate(
                    differentiate(base, (directions[first],)),
                    (directions[second],),
                )
                right = differentiate(
                    differentiate(base, (directions[second],)),
                    (directions[first],),
                )
                require(left == right, "principal-parts square failed")

            support = []
            for site in ODD:
                for colour in range(3):
                    reset = face_polynomial(site) if colour == MIXED[site] else {}
                    value = differentiate(reset, internal)
                    if value:
                        support.append((site, colour, value))
            require(support == [(deleted, MIXED[deleted], {(): Q(1)})],
                    "denominator reset leaks to another column")

            column = [Q(0)] * 5
            column[deleted_index] = Q(1)
            labelled_columns.append(column)
            records += 1

    require(records == 15, "four-polar count")
    require(rank(labelled_columns) == 5, "labelled face rank")
    require(records - rank(labelled_columns) == 10,
            "matching-choice kernel")
    return records


def oriented_boundary(state):
    free = [index for index, value in enumerate(state) if value is None]
    answer = defaultdict(int)
    for local_index, coordinate in enumerate(free):
        sign = -1 if local_index % 2 else 1
        upper = list(state)
        lower = list(state)
        upper[coordinate] = 1
        lower[coordinate] = 0
        answer[tuple(upper)] += sign
        answer[tuple(lower)] -= sign
    return {face: coefficient for face, coefficient in answer.items()
            if coefficient}


def audit_abstract_cube_signs():
    first = oriented_boundary((None,) * 4)
    second = defaultdict(int)
    appearances = defaultdict(int)
    for facet, coefficient in first.items():
        for ridge, face_coefficient in oriented_boundary(facet).items():
            second[ridge] += coefficient * face_coefficient
            appearances[ridge] += 1
    require(len(first) == 8, "facet count")
    require(len(appearances) == 24, "ridge count")
    require(set(appearances.values()) == {2}, "ridge multiplicity")
    require(not any(second.values()), "cubical boundary does not square zero")


def stabilizer_constraints():
    rows = []
    # Vanishing of the sum over sites for each colour.
    for colour in range(3):
        row = [Q(0)] * 15
        for site_index in range(5):
            row[3 * site_index + colour] = Q(1)
        rows.append(row)
    # Tracelessness at each site.  The eight rows have one dependency.
    for site_index in range(5):
        row = [Q(0)] * 15
        for colour in range(3):
            row[3 * site_index + colour] = Q(1)
        rows.append(row)
    require(rank(rows) == 7, "stabilizer constraint rank")
    return rows


def jet_character(remaining_sites):
    character = [Q(0)] * 15
    for site_index, site in enumerate(ODD):
        character[3 * site_index] += Q(1)
        if site in remaining_sites:
            character[3 * site_index + MIXED[site]] -= Q(1)
    return character


def audit_stabilizer_ladder():
    constraints = stabilizer_constraints()
    initial = []
    for deleted in ODD:
        face = tuple(site for site in ODD if site != deleted)
        weight_two = jet_character(face)
        require(not in_span(weight_two, constraints), "q-degree-two weight")
        initial.append(weight_two)

        collisions = []
        for word in product(range(3), repeat=4):
            trial_colours = dict(zip(face, word))
            trial = [Q(0)] * 15
            for site_index, site in enumerate(ODD):
                trial[3 * site_index] += Q(1)
                if site in trial_colours:
                    trial[3 * site_index + trial_colours[site]] -= Q(1)
            difference = [left - right
                          for left, right in zip(trial, weight_two)]
            if in_span(difference, constraints):
                collisions.append(word)
        require(collisions == [tuple(MIXED[site] for site in face)],
                "mixed face is not the unique restricted weight word")

        for matching in perfect_matchings(face):
            first, second = matching
            require(not in_span(jet_character(set(first)), constraints),
                    "q-degree-one weight vanished")
            require(not in_span(jet_character(set(second)), constraints),
                    "q-degree-one weight vanished")
            require(in_span(jet_character(set()), constraints),
                    "q-degree-zero weight is not invariant")
    require(rank(constraints + initial) - rank(constraints) == 5,
            "five initial face weights are not independent")


def uncoloured_face(odd_sites, deleted):
    vertices = tuple(site for site in odd_sites if site != deleted)
    return {
        tuple(sorted(tuple(sorted(pair)) for pair in matching)): Q(1)
        for matching in perfect_matchings(vertices)
    }


def double_factorial(value):
    answer = 1
    while value > 0:
        answer *= value
        value -= 2
    return answer


def audit_reynolds_duality():
    # Finite reconstruction; the same support argument is uniform in r.
    instances = []
    for r in range(1, 6):
        odd_sites = tuple(range(2 * r + 1))
        normalization = double_factorial(2 * r - 1)
        matrix = []
        for deleted in odd_sites:
            face = tuple(site for site in odd_sites if site != deleted)
            row = []
            for other in odd_sites:
                polynomial = uncoloured_face(odd_sites, other)
                total = Q(0)
                for matching in perfect_matchings(face):
                    variables = tuple(sorted(
                        tuple(sorted(pair)) for pair in matching
                    ))
                    total += Q(1, normalization) * differentiate(
                        polynomial, variables
                    ).get((), Q(0))
                row.append(total)
            matrix.append(row)
        identity = [
            [Q(left == right) for right in range(len(odd_sites))]
            for left in range(len(odd_sites))
        ]
        require(matrix == identity, f"Reynolds duality at r={r}")
        instances.append((len(odd_sites), normalization))
    return instances


def audit_augmented_typing_ambiguity():
    # The verified polynomial/target projection forgets ordinary residue.
    declared = (Q(1), Q(0), Q(0))
    response = (Q(1), Q(0), Q(1))
    require(declared[:2] == response[:2], "typing ambiguity disappeared")
    require(declared != response, "ordinary residue was accidentally fixed")

    # This missing coordinate changes the split-cap conclusion itself.
    for kappa, y in ((Q(1), Q(1)), (Q(-5, 2), Q(7, 3))):
        target = (-y, Q(1), Q(0))
        rho = (Q(1), Q(0), Q(1))
        desired = (kappa * y, Q(0), Q(0))
        graph = (kappa * y, Q(0), kappa * y)
        require(desired[:2] == graph[:2], "same evidenced coordinates")
        require(rank((target, rho)) == 2, "old split-cap rank")
        require(rank((target, rho, desired)) == 3,
                "boundary-only lift should be new")
        require(rank((target, rho, graph)) == 2,
                "response lift should remain old")


def audit_primary_implementation_scope():
    source = PRIMARY.read_text()
    require("readout = [Q(1), Q(0), Q(0)]" not in source,
            "primary has restored the unsupported literal readout")
    require('"cap_boundary": "not constructed"' in source,
            "primary no longer marks the cap boundary unconstructed")
    require('"ordinary_residue": "not defined"' in source,
            "primary no longer marks ordinary residue undefined")
    require("conditional_column = [kappa * y, Q(0), Q(0)]" in source,
            "primary conditional typing test changed; reaudit needed")
    require("Conditional typing only" in source,
            "primary rank test is no longer explicitly conditional")
    require("def ordinary_residue" not in source,
            "primary now defines an ordinary-residue map; reaudit needed")
    require("def comparison_map" not in source,
            "primary now defines a comparison map; reaudit needed")
    require("def augmented_differential" not in source,
            "primary now defines an augmented differential; reaudit needed")


def main():
    records = audit_literal_polars_and_derivative_cubes()
    audit_abstract_cube_signs()
    audit_stabilizer_ladder()
    reynolds = audit_reynolds_duality()
    audit_augmented_typing_ambiguity()
    audit_primary_implementation_scope()
    print(
        f"literal audit: four_polars={records} labelled_rank=5 "
        "matching_kernel=10 no_leakage=PASS"
    )
    print(f"Reynolds duality instances={reynolds}")
    print("principal-parts squares, cube signs, and stabilizer ladder: PASS")
    print("augmented typing: boundary/target do not determine ordinary residue")
    print("corrected primary marks cap boundary unconstructed and ores undefined")
    print("PASS with correction: polynomial four-cube valid, cap readout unproved")


if __name__ == "__main__":
    main()
