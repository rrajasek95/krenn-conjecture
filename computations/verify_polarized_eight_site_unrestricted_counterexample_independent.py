#!/usr/bin/env python3
"""Clean-room audit of the eight-site unrestricted polarized model.

This checker deliberately does not import the discovery checker.  It uses
two independent expansions:

* four-edge subsets of K_8 (rather than recursive matching generation) for
  the divided-power coefficient calculation; and
* ordered multiplication in the site-square-zero algebra to recover the
  factor 3! before normalization.

It also proves the rank obstruction symbolically by expanding the generic
3-by-3 determinant of p_R s_C^T+s_R p_C^T as a polynomial.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from math import factorial


SITES = range(8)
COLOURS = range(3)
UNDERLYING_EDGES = tuple(combinations(SITES, 2))

# Cells are literal triples (smaller site, larger site, endpoint colour).
# Writing the lists directly avoids reconstructing them from the three
# advertised perfect matchings.
Q = frozenset(
    {
        (2, 3, 0),
        (4, 5, 0),
        (6, 7, 0),
        (0, 1, 1),
        (3, 6, 1),
        (5, 7, 1),
        (0, 2, 2),
        (1, 4, 2),
        (5, 6, 2),
    }
)
Z = frozenset({(0, 1, 0), (2, 4, 1), (3, 7, 2)})


def check_cells(cells):
    for i, j, colour in cells:
        assert 0 <= i < j < 8
        assert colour in COLOURS


def perfect_matchings_as_edge_subsets():
    """Enumerate matchings by filtering the C(28,4) edge subsets."""
    result = []
    for candidate in combinations(UNDERLYING_EDGES, 4):
        endpoints = tuple(vertex for edge in candidate for vertex in edge)
        if len(set(endpoints)) == 8:
            result.append(candidate)
    return tuple(result)


def cells_by_edge(cells):
    table = defaultdict(list)
    for i, j, colour in cells:
        table[(i, j)].append(colour)
    return {edge: tuple(sorted(values)) for edge, values in table.items()}


def word_from_decorated_edges(decorated_edges):
    word = [None] * 8
    for i, j, colour in decorated_edges:
        assert word[i] is None and word[j] is None
        word[i] = word[j] = colour
    assert all(colour is not None for colour in word)
    return tuple(word)


def divided_power_expansion(matchings, q_by_edge, z_by_edge):
    """Expand z*q^[3] by all 4*105 choices of its z-position."""
    coefficients = Counter()
    witnesses = []
    choices_examined = 0
    for matching in matchings:
        for distinguished in matching:
            choices_examined += 1
            other_edges = tuple(edge for edge in matching if edge != distinguished)
            for z_colour in z_by_edge.get(distinguished, ()):
                q_options = tuple(q_by_edge.get(edge, ()) for edge in other_edges)
                for q_colours in product(*q_options):
                    decorated = ((distinguished[0], distinguished[1], z_colour),) + tuple(
                        (edge[0], edge[1], colour)
                        for edge, colour in zip(other_edges, q_colours)
                    )
                    word = word_from_decorated_edges(decorated)
                    coefficients[word] += 1
                    witnesses.append((matching, distinguished, decorated, word))
    assert choices_examined == 105 * 4
    return coefficients, tuple(witnesses)


def ordered_site_square_zero_expansion():
    """Expand z*q*q*q before division by 3!, retaining edge order."""
    raw = Counter()
    surviving_ordered_tuples = 0
    for z_cell in Z:
        for ordered_q_cells in product(Q, repeat=3):
            decorated = (z_cell,) + ordered_q_cells
            endpoints = tuple(site for i, j, _ in decorated for site in (i, j))
            if len(set(endpoints)) != 8:
                continue
            surviving_ordered_tuples += 1
            raw[word_from_decorated_edges(decorated)] += 1
    return raw, surviving_ordered_tuples


def ordinary_fourth_divided_power(matchings, q_by_edge):
    """Compute q^[4], solely to separate this model from Krenn's target."""
    coefficients = Counter()
    for matching in matchings:
        options = tuple(q_by_edge.get(edge, ()) for edge in matching)
        for colours in product(*options):
            decorated = tuple(
                (edge[0], edge[1], colour) for edge, colour in zip(matching, colours)
            )
            coefficients[word_from_decorated_edges(decorated)] += 1
    return coefficients


def coefficient(cells, left_mode, right_mode):
    i, left_colour = left_mode
    j, right_colour = right_mode
    if left_colour != right_colour:
        return 0
    edge = (min(i, j), max(i, j), left_colour)
    return int(edge in cells)


def permutation_sign(perm):
    inversions = sum(
        perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm))
    )
    return -1 if inversions % 2 else 1


def generic_two_outer_product_determinant():
    """Return det(p_R*s_C^T+s_R*p_C^T) as an exact sparse polynomial.

    A monomial is a sorted tuple of variable labels.  The labels 0..2 are
    p_R, 3..5 are s_R, 6..8 are p_C, and 9..11 are s_C.
    """
    entries = {}
    for i in range(3):
        for j in range(3):
            entries[(i, j)] = ((i, 9 + j), (3 + i, 6 + j))

    determinant = Counter()
    for perm in permutations(range(3)):
        sign = permutation_sign(perm)
        for summand_choices in product(range(2), repeat=3):
            factors = []
            for row, which_summand in enumerate(summand_choices):
                factors.extend(entries[(row, perm[row])][which_summand])
            determinant[tuple(sorted(factors))] += sign
    return {monomial: value for monomial, value in determinant.items() if value}


def main():
    check_cells(Q)
    check_cells(Z)
    assert len(Q) == 9 and len(Z) == 3
    assert Q.isdisjoint(Z)
    # The common physical edge 01 still has two distinct endpoint-colour cells.
    assert (0, 1, 0) in Z and (0, 1, 1) in Q

    matchings = perfect_matchings_as_edge_subsets()
    assert len(matchings) == 105
    assert len(set(matchings)) == 105
    for matching in matchings:
        assert sorted(vertex for edge in matching for vertex in edge) == list(SITES)

    q_by_edge = cells_by_edge(Q)
    z_by_edge = cells_by_edge(Z)
    normalized, witnesses = divided_power_expansion(matchings, q_by_edge, z_by_edge)
    delta = Counter({tuple([colour] * 8): 1 for colour in COLOURS})
    assert normalized == delta
    assert len(witnesses) == 3

    expected_decorated_supports = {
        frozenset({(0, 1, 0), (2, 3, 0), (4, 5, 0), (6, 7, 0)}),
        frozenset({(2, 4, 1), (0, 1, 1), (3, 6, 1), (5, 7, 1)}),
        frozenset({(3, 7, 2), (0, 2, 2), (1, 4, 2), (5, 6, 2)}),
    }
    assert {frozenset(witness[2]) for witness in witnesses} == expected_decorated_supports

    raw, surviving_ordered_tuples = ordered_site_square_zero_expansion()
    assert surviving_ordered_tuples == 3 * factorial(3)
    assert raw == Counter({word: factorial(3) for word in delta})
    assert Counter({word: value // factorial(3) for word, value in raw.items()}) == normalized

    # This particular q is visibly not an ordinary matching-power solution:
    # q^[4] has two mixed words and no pure word.
    ordinary = ordinary_fourth_divided_power(matchings, q_by_edge)
    assert ordinary == Counter(
        {
            (1, 1, 0, 0, 0, 0, 0, 0): 1,
            (2, 2, 2, 1, 2, 1, 1, 1): 1,
        }
    )
    assert ordinary != delta

    row_modes = ((0, 0), (2, 1), (3, 2))
    column_modes = ((1, 0), (4, 1), (7, 2))
    q_cross = tuple(
        tuple(coefficient(Q, row, column) for column in column_modes)
        for row in row_modes
    )
    z_cross = tuple(
        tuple(coefficient(Z, row, column) for column in column_modes)
        for row in row_modes
    )
    zero = ((0, 0, 0),) * 3
    identity = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    assert q_cross == zero
    assert z_cross == identity

    # This is an exact formal verification that every cross matrix of ps has
    # determinant zero.  Hence its rank is at most two over every field; over
    # C this contradicts the constant determinant-one block of z-aq.
    assert generic_two_outer_product_determinant() == {}

    print("independent polarized eight-site audit: PASS")
    print("C(28,4) filtering gives 105 perfect matchings: PASS")
    print("all 420 matching/distinguished-edge positions checked: PASS")
    print("9 q-cells + 3 z-cells give exactly 3 divided-power terms: PASS")
    print("ordered expansion gives coefficient 3!=6 before normalization: PASS")
    print("q^4/4! has two mixed words, so this is not a Krenn counterexample: PASS")
    print("constant I_3 cross block and symbolic rank<=2 pair-cap test: PASS")


if __name__ == "__main__":
    main()
