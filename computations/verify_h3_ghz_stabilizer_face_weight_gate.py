#!/usr/bin/env python3
"""Exact character audit for the five h=3 denominator-face polars.

The calculation is deliberately dependency free.  Characters are integer
rows on the diagonal Lie algebra.  Restriction to the diagonal stabilizer of
the five-site ternary GHZ tensor is quotient by the three colour-sum rows.
"""

from fractions import Fraction


WORD = (1, 2, 1, 1, 2)
SITES = range(5)
COLOURS = range(3)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(rows):
    matrix = [[Fraction(x) for x in row] for row in rows if any(row)]
    if not matrix:
        return 0
    number_rows = len(matrix)
    number_columns = len(matrix[0])
    pivot_row = 0
    for column in range(number_columns):
        pivot = next(
            (row for row in range(pivot_row, number_rows)
             if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(number_rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == number_rows:
            break
    return pivot_row


def coordinate(site, colour):
    return 3 * site + colour


def colour_sum_rows(number_sites=5):
    rows = []
    for colour in COLOURS:
        row = [0] * (3 * number_sites)
        for site in range(number_sites):
            row[coordinate(site, colour)] = 1
        rows.append(row)
    return rows


def local_trace_rows(number_sites=5):
    rows = []
    for site in range(number_sites):
        row = [0] * (3 * number_sites)
        for colour in COLOURS:
            row[coordinate(site, colour)] = 1
        rows.append(row)
    return rows


def face_character(deleted, include_exposed_output=False, number_sites=5):
    """Weight of e_0^(deleted) h_{m|F} Y_{0^F}.

    Without the spectator this is the End(W_F) connection character.
    With it this is the character of the literal five-site output term.
    """
    row = [0] * (3 * number_sites)
    for site in SITES:
        if site == deleted:
            if include_exposed_output:
                row[coordinate(site, 0)] += 1
            continue
        row[coordinate(site, 0)] += 1
        row[coordinate(site, WORD[site])] -= 1
    return row


def denominator_character(deleted, exposed_colour, number_sites=5):
    row = [0] * (3 * number_sites)
    row[coordinate(deleted, exposed_colour)] = 1
    return row


def restricted_rank(characters, constraints):
    return rank(constraints + characters) - rank(constraints)


def equivalent_mod_constraints(left, right, constraints):
    difference = [a - b for a, b in zip(left, right)]
    return rank(constraints + [difference]) == rank(constraints)


def audit(number_sites=5, impose_local_trace=False):
    constraints = colour_sum_rows(number_sites)
    if impose_local_trace:
        constraints += local_trace_rows(number_sites)

    bare = [face_character(v, False, number_sites) for v in SITES]
    physical = [face_character(v, True, number_sites) for v in SITES]
    expected_constraint_rank = 3 if not impose_local_trace else number_sites + 2
    require(rank(constraints) == expected_constraint_rank,
            "unexpected stabilizer constraint rank")
    require(restricted_rank(bare, constraints) == 5,
            "the five face characters are not independent")
    require(restricted_rank(physical, constraints) == 5,
            "the five physical face characters are not independent")

    old = [
        denominator_character(site, colour, number_sites)
        for site in SITES for colour in COLOURS
    ]
    for character in bare + physical:
        require(restricted_rank([character], constraints) == 1,
                "a face polar became stabilizer invariant")
        require(not any(
            equivalent_mod_constraints(character, candidate, constraints)
            for candidate in old
        ), "a face polar collided with an old denominator weight")

    return {
        "number_sites": number_sites,
        "sl_restriction": impose_local_trace,
        "stabilizer_dimension": 3 * number_sites - rank(constraints),
        "bare_face_rank": restricted_rank(bare, constraints),
        "physical_face_rank": restricted_rank(physical, constraints),
    }


def main():
    ledgers = [
        audit(5, False),
        audit(5, True),
        audit(8, False),
        audit(8, True),
    ]
    print("h3 GHZ-stabilizer face-weight gate: PASS")
    for ledger in ledgers:
        print(ledger)


if __name__ == "__main__":
    main()
