#!/usr/bin/env python3
"""Audit a no-singleton completion of the rainbow valuation plateau.

Starting from ``verify_valuation_rainbow_descent_cycle.py``, add eighteen
aggregate cells.  Every nonempty mixed fibre then has exactly two terms.
Exact rational weights normalize all three constant fibres and cancel the
original selected fibre together with all four former singleton errors.
No entry except 04_00 has negative 2-adic valuation, so none of the new
rewrites lies below the old valuation minimum.

The script also checks two parity facts:

* the complete 336-state binomial replacement graph is bipartite, so it has
  no odd replacement-cycle obstruction; and
* three binomial fibres have an exact odd Laurent dependency, which is a
  genuinely global obstruction not visible as an odd state cycle.

Finally it maps the original four minimum states into the saved integral
degree-nine residual and verifies that the residual coefficients evaluate
consistently to 1/2 rather than giving a local parity contradiction.
"""

from __future__ import annotations

import gzip
import importlib.util
import pickle
from collections import Counter, deque
from fractions import Fraction
from itertools import product
from pathlib import Path

import verify_valuation_rainbow_descent_cycle as base


HERE = Path(__file__).resolve().parent
EPSILON = Fraction(16)
D = 1 + EPSILON**2  # 257, a 2-adic unit.

# An exact MaxSAT minimization finds that eighteen is the least number of
# cells which can be added to the fixed thirteen-cell support while removing
# every mixed singleton.  The separate search script reconstructs that
# optimization.  This verifier only trusts and audits the resulting support.
ADDITIONS = {
    (0, 1, 1, 1),
    (0, 1, 2, 1),
    (0, 2, 1, 2),
    (0, 2, 2, 2),
    (0, 3, 1, 2),
    (0, 5, 2, 1),
    (1, 3, 0, 1),
    (1, 4, 1, 2),
    (1, 5, 2, 0),
    (2, 3, 1, 0),
    (2, 4, 2, 1),
    (2, 5, 0, 2),
    (3, 4, 2, 1),
    (3, 4, 2, 2),
    (3, 5, 0, 2),
    (3, 5, 1, 0),
    (4, 5, 1, 1),
    (4, 5, 2, 1),
}

FORMER_ERRORS = (
    (0, 0, 0, 1, 0, 2),
    (0, 2, 1, 0, 0, 0),
    (1, 0, 2, 0, 2, 1),
    (2, 1, 0, 2, 1, 0),
)

LAURENT_COLORINGS = (
    (1, 0, 0, 2, 1, 1),
    (1, 1, 0, 2, 1, 0),
    (1, 1, 1, 0, 1, 1),
)


def completed_entries():
    """Return the exact 31-cell weighted completion."""
    entries = dict(base.ENTRIES)
    entries.update({occurrence: EPSILON for occurrence in ADDITIONS})

    # The new diagonal matchings contribute epsilon^2 times the old one.
    # These two unit pivots restore F_111111=F_222222=1 exactly.
    entries[(2, 3, 1, 1)] = Fraction(1, D)
    entries[(1, 5, 2, 2)] = Fraction(1, D)

    # Restore the original selected mixed binomial after the two preceding
    # normalizations.
    entries[(1, 2, 2, 1)] = Fraction(-1, D**2)

    # Unit companions and pivots cancel the four former singleton errors.
    entries[(2, 5, 0, 2)] = Fraction(1)
    entries[(2, 3, 1, 0)] = Fraction(1)
    entries[(4, 5, 2, 1)] = Fraction(1)
    entries[(3, 4, 2, 1)] = Fraction(1)
    entries[(1, 3, 0, 1)] = Fraction(-1)
    entries[(1, 5, 2, 0)] = Fraction(1, D**2)
    entries[(0, 2, 1, 2)] = Fraction(-1)
    entries[(0, 1, 2, 1)] = Fraction(-1)

    assert len(entries) == 31
    assert all(entries.values())
    return entries


def fibre_terms(entries, coloring):
    answer = []
    for matching in base.perfect_matchings():
        decorated = frozenset(
            (u, v, coloring[u], coloring[v]) for u, v in matching
        )
        if not decorated <= entries.keys():
            continue
        value = Fraction(1)
        for occurrence in decorated:
            value *= entries[occurrence]
        answer.append((decorated, value))
    return answer


def coefficient(entries, coloring):
    return sum(
        (value for _, value in fibre_terms(entries, coloring)), Fraction()
    )


def endpoints(occurrence):
    u, v, a, b = occurrence
    return frozenset({(u, a), (v, b)})


def rainbow_states(entries):
    all_stubs = frozenset(
        (vertex, color)
        for vertex in range(base.N)
        for color in base.COLORS
    )
    by_stub = {stub: [] for stub in all_stubs}
    for occurrence in entries:
        for stub in endpoints(occurrence):
            by_stub[stub].append(occurrence)

    answer = []

    def visit(remaining, chosen):
        if not remaining:
            answer.append(frozenset(chosen))
            return

        def available(stub):
            return [
                occurrence
                for occurrence in by_stub[stub]
                if endpoints(occurrence) <= remaining
            ]

        stub = min(remaining, key=lambda item: (len(available(item)), item))
        for occurrence in available(stub):
            visit(remaining - endpoints(occurrence), chosen + [occurrence])

    visit(all_stubs, [])
    return answer


def monomial(entries, state):
    answer = Fraction(1)
    for occurrence in state:
        answer *= entries[occurrence]
    return answer


def binomial_fibres(entries):
    answer = {}
    for coloring in product(base.COLORS, repeat=base.N):
        if len(set(coloring)) == 1:
            continue
        terms = fibre_terms(entries, coloring)
        if terms:
            assert len(terms) == 2
            answer[coloring] = tuple(network for network, _ in terms)
    return answer


def replacement_graph(states, fibres):
    lookup = {state: index for index, state in enumerate(states)}
    adjacency = [dict() for _ in states]
    for index, state in enumerate(states):
        for coloring, (left, right) in fibres.items():
            if left <= state:
                replacement = (state - left) | right
            elif right <= state:
                replacement = (state - right) | left
            else:
                continue
            other = lookup[frozenset(replacement)]
            adjacency[index][other] = coloring
            adjacency[other][index] = coloring
    return adjacency


def assert_bipartite(adjacency):
    colors = {}
    for root in range(len(adjacency)):
        if root in colors:
            continue
        colors[root] = 0
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
                else:
                    assert colors[neighbor] != colors[vertex]
    return colors


def exponent_difference(entries, terms):
    ordered = tuple(sorted(entries))
    index = {occurrence: position for position, occurrence in enumerate(ordered)}
    answer = [0] * len(ordered)
    for occurrence in terms[0]:
        answer[index[occurrence]] += 1
    for occurrence in terms[1]:
        answer[index[occurrence]] -= 1
    return tuple(answer)


def degree9_row_data(states):
    """Return saved residual coefficients on the four original states."""
    module_path = HERE / "test_degree9_source_ideal_char2.py"
    spec = importlib.util.spec_from_file_location("degree9_char2", module_path)
    degree9 = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(degree9)

    with (HERE / "degree9_source_ideal_char2_h27.pkl").open("rb") as stream:
        parity = pickle.load(stream)
    with gzip.open(
        HERE / "degree9_char2_first_integral_residual.pkl.gz", "rb"
    ) as stream:
        residual = pickle.load(stream)["coefficients"]

    actions = degree9.group_actions()
    row_lookup = {code: row for row, code in enumerate(parity["row_codes"])}

    def row_of(state):
        code = degree9.matching_code(
            (3 * u + a, 3 * v + b) for u, v, a, b in state
        )
        canonical = min(
            degree9.transform_code(code, edge_map)
            for _, _, edge_map in actions
        )
        return row_lookup[canonical]

    rows = tuple(row_of(state) for state in states)
    return rows, tuple(residual[row] for row in rows)


def main():
    entries = completed_entries()

    # Exact normalizations and exact repairs.
    assert tuple(
        coefficient(entries, (color,) * base.N) for color in base.COLORS
    ) == (1, 1, 1)
    repaired = (base.MIXED_COLORING,) + FORMER_ERRORS
    assert all(coefficient(entries, coloring) == 0 for coloring in repaired)
    assert all(len(fibre_terms(entries, coloring)) == 2 for coloring in repaired)

    # Every supported fibre has two terms.  This removes every singleton,
    # not merely the original four.
    fibre_size_distribution = Counter(
        len(fibre_terms(entries, coloring))
        for coloring in product(base.COLORS, repeat=base.N)
    )
    assert fibre_size_distribution == Counter({0: 665, 2: 64})
    fibres = binomial_fibres(entries)
    assert len(fibres) == 61

    zero_mixed = {
        coloring
        for coloring in product(base.COLORS, repeat=base.N)
        if len(set(coloring)) > 1 and coefficient(entries, coloring) == 0
    }
    assert len(zero_mixed) == 688
    assert sum(coloring in fibres for coloring in zero_mixed) == 23

    # There is still no lower balanced/rainbow monomial.  Exactly one entry
    # has negative valuation, so every stub matching can use it at most once.
    entry_valuations = Counter(
        base.valuation_two(value) for value in entries.values()
    )
    assert entry_valuations == Counter({0: 20, 4: 10, -1: 1})
    assert {
        occurrence
        for occurrence, value in entries.items()
        if base.valuation_two(value) < 0
    } == {(0, 4, 0, 0)}

    states = rainbow_states(entries)
    assert len(states) == 336
    state_valuations = Counter(
        base.valuation_two(monomial(entries, state)) for state in states
    )
    assert state_valuations == Counter(
        {-1: 36, 3: 16, 7: 148, 11: 64, 15: 52, 19: 16, 23: 4}
    )

    selected = frozenset(base.P0 | base.P1 | base.P2)
    replacement = frozenset((selected - base.R) | base.MATE)
    assert selected in states and replacement in states
    assert coefficient(entries, base.MIXED_COLORING) == 0
    assert monomial(entries, selected) == Fraction(1, 2 * D**2)
    assert monomial(entries, replacement) == Fraction(-1, 2 * D**2)
    assert base.valuation_two(monomial(entries, selected)) == -1
    assert base.valuation_two(monomial(entries, replacement)) == -1

    # No odd replacement-cycle parity obstruction exists, even after the
    # no-singleton completion: the entire graph is bipartite.
    adjacency = replacement_graph(states, fibres)
    assert sum(map(len, adjacency)) // 2 == 736
    assert_bipartite(adjacency)

    # Nevertheless the binomial equations have a three-fibre Laurent sign
    # obstruction.  With d_i = exponent(term_0)-exponent(term_1),
    # d_3=d_1+d_2.  Each equation would impose x^d_i=-1, hence the third
    # would say both -1 and (+1).
    differences = []
    for coloring in LAURENT_COLORINGS:
        terms = tuple(network for network, _ in fibre_terms(entries, coloring))
        assert len(terms) == 2
        differences.append(exponent_difference(entries, terms))
    assert tuple(
        differences[0][index] + differences[1][index]
        for index in range(len(entries))
    ) == differences[2]

    # The original four-state plateau consists of the P0/S0 choice crossed
    # with the R/N choice.
    selected_alt = frozenset(base.S0 | base.P1 | base.P2)
    replacement_alt = frozenset((selected_alt - base.R) | base.MATE)
    original_states = (
        selected,
        replacement,
        selected_alt,
        replacement_alt,
    )
    rows, residual_coefficients = degree9_row_data(original_states)
    assert len(set(rows)) == 4
    assert residual_coefficients == (0, -1, -1, -1)
    original_values = tuple(
        monomial(base.ENTRIES, state) for state in original_states
    )
    assert original_values == (
        Fraction(1, 2),
        Fraction(-1, 2),
        Fraction(1, 2),
        Fraction(-1, 2),
    )
    assert sum(
        coefficient * value
        for coefficient, value in zip(residual_coefficients, original_values)
    ) == Fraction(1, 2)

    print(
        "verified 31-cell no-singleton plateau: fibre sizes 0/2, five "
        "displayed mixed fibres cancel exactly, 336 rainbow states with "
        "36 minima of v2=-1 and no lower state"
    )
    print(
        "verified parity diagnosis: 736-edge replacement graph is "
        "bipartite; a separate three-fibre Laurent dependency has odd sign"
    )
    print(
        "verified degree-nine residual on original plateau: rows="
        f"{rows}, coefficients=(0,-1,-1,-1), evaluation=1/2 (consistent)"
    )


if __name__ == "__main__":
    main()
