#!/usr/bin/env python3
"""Freeze a source-labelled grade split of the K6 multiplicity-two circuit.

The physical support-11 circuit has one matching with coefficient two.  It
does not follow that the two occurrences collide after endpoint colours and
row words are restored.  This checker gives a minimal six-binomial
polarization in six distinct mixed top words.  On its 28 decorated cells,
each of the six complete word fibres consists of exactly the prescribed two
matchings.  The two copies of the doubled physical matching are disjoint
decorated monomials, and the six decorated exponent differences have rank
six even though their physical projections sum to zero.

Putting weight -1 on one private cell in each negative monomial and weight 1
elsewhere is an exact rational torus point of all six source rows.  Thus the
physical multiplicity-two relation alone forces neither an odd character nor
a parallel/translated-target unit.  Additional full-packet target rows may
still exclude this source support; no GHZ point is claimed.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_n8_one_bad_global_debt_circuit_quotient.py"
DEPENDENCY_SHA256 = (
    "85353d137c38c66e6c93918c44521293d9e2caa6e304d587ca88533a4feff320"
)
EXPECTED_LEDGER_SHA256 = (
    "ee0ecabaa208943f448e862c5d5528c7a2ef7c36d19af6272d9adafa5bab43f6"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


path = ROOT / DEPENDENCY
require(sha256(path.read_bytes()).hexdigest() == DEPENDENCY_SHA256,
        "the pinned global-debt circuit theorem changed")
spec = spec_from_file_location("one_bad_global_debt", path)
G = module_from_spec(spec)
spec.loader.exec_module(G)


# The canonical support-11 representative.  Positive multiplicity is six:
# the first matching occurs twice, followed by four unit terms.
COEFFICIENT = {
    0: 2,
    1: -1,
    2: -1,
    3: -1,
    4: 1,
    6: -1,
    8: 1,
    10: 1,
    11: -1,
    12: 1,
    14: -1,
}
POSITIVE = (0, 0, 4, 8, 10, 12)
NEGATIVE = (1, 2, 3, 6, 11, 14)

# All six are mixed target words.  They were chosen so that the union of the
# twelve decorated matching terms introduces no third matching in any of
# these six complete top fibres.
WORDS = (
    (1, 0, 2, 0, 2, 0),
    (2, 0, 0, 1, 0, 1),
    (0, 0, 0, 2, 1, 0),
    (0, 2, 0, 1, 1, 1),
    (1, 2, 1, 0, 2, 1),
    (1, 0, 0, 0, 1, 2),
)


def decorated_term(matching_index, word):
    return tuple(sorted(
        ((left, right), (word[left], word[right]))
        for left, right in G.MATCHINGS[matching_index]
    ))


def term_value(term, weights):
    value = Fraction(1)
    for cell in term:
        value *= weights[cell]
    return value


def physical_circuit_audit():
    require(len(COEFFICIENT) == 11,
            "the canonical physical support stopped having size eleven")
    require(Counter(abs(value) for value in COEFFICIENT.values())
            == Counter({1: 10, 2: 1}),
            "the primitive coefficient pattern changed")
    require(tuple(index for index, value in COEFFICIENT.items()
                  for repetition in range(max(value, 0))) == POSITIVE,
            "the expanded positive side changed")
    require(tuple(index for index, value in COEFFICIENT.items()
                  for repetition in range(max(-value, 0))) == NEGATIVE,
            "the expanded negative side changed")

    physical_sum = Counter()
    for index, coefficient in COEFFICIENT.items():
        for edge in G.MATCHINGS[index]:
            physical_sum[edge] += coefficient
    require(not +physical_sum and not -physical_sum,
            "the physical endpoint-incidence debt stopped telescoping")

    incidence = sp.Matrix([
        [int(edge in G.MATCHINGS[index]) for index in COEFFICIENT]
        for edge in G.EDGES
    ])
    require(incidence.rank() == 10 and len(incidence.nullspace()) == 1,
            "the canonical support stopped being a primitive circuit")

    matching_index = {
        frozenset(matching): index
        for index, matching in enumerate(G.MATCHINGS)
    }
    representative = tuple(sorted(COEFFICIENT.items()))
    orbit = set()
    doubled = Counter()
    for permutation in itertools.permutations(G.SITES):
        transformed = []
        for index, coefficient in representative:
            matching = frozenset(
                tuple(sorted((permutation[left], permutation[right])))
                for left, right in G.MATCHINGS[index]
            )
            transformed.append((matching_index[matching], coefficient))
        transformed = dict(transformed)
        first = transformed[min(transformed)]
        if first < 0:
            transformed = {index: -value
                           for index, value in transformed.items()}
        normalized = tuple(sorted(transformed.items()))
        orbit.add(normalized)

    require(len(orbit) == 30,
            "the transported multiplicity-two orbit changed")
    for coefficient_map in orbit:
        doubled_index = next(index for index, value in coefficient_map
                             if abs(value) == 2)
        doubled[frozenset(G.MATCHINGS[doubled_index])] += 1
    require(set(doubled.values()) == {2} and len(doubled) == 15,
            "the doubled matching stopped indexing the orbit two-to-one")

    distinguished = frozenset({(0, 1), (2, 4), (3, 5)})
    relative = Counter()
    for matching, count in doubled.items():
        relative[len(matching & distinguished)] += count
    require(relative == Counter({3: 2, 1: 12, 0: 16}),
            "the relative doubled-matching split changed")
    return {
        "physical_support": len(COEFFICIENT),
        "positive_negative_multiplicity": [len(POSITIVE), len(NEGATIVE)],
        "physical_incidence_rank": incidence.rank(),
        "physical_nullity": len(incidence.nullspace()),
        "orbit_size": len(orbit),
        "per_sharp_star_relative_split": {
            "equal": relative[3],
            "share_one_edge": relative[1],
            "disjoint": relative[0],
        },
    }


def source_provenance_audit():
    require(len(set(WORDS)) == 6
            and all(len(set(word)) >= 2 for word in WORDS),
            "the six row grades stopped being distinct mixed words")
    positive_terms = tuple(
        decorated_term(index, word)
        for index, word in zip(POSITIVE, WORDS)
    )
    negative_terms = tuple(
        decorated_term(index, word)
        for index, word in zip(NEGATIVE, WORDS)
    )
    all_terms = tuple(
        term for pair in zip(positive_terms, negative_terms) for term in pair
    )
    require(len(set(all_terms)) == 12,
            "two polarized matching occurrences unexpectedly collided")

    support = frozenset(cell for term in all_terms for cell in term)
    require(len(support) == 28,
            "the frozen polarized support changed")

    fibre_indices = []
    for row, word in enumerate(WORDS):
        live = tuple(index for index in range(len(G.MATCHINGS))
                     if set(decorated_term(index, word)) <= support)
        expected = tuple(sorted((POSITIVE[row], NEGATIVE[row])))
        require(live == expected,
                f"polarized row {row} acquired an uncontrolled tail: {live}")
        fibre_indices.append(list(live))

    # Each negative term has a cell occurring in no other prescribed term.
    # These private cells give both an independence pivot and a rational
    # coefficient solution.
    occurrence = Counter(cell for term in all_terms for cell in term)
    private_cells = []
    for term in negative_terms:
        private = tuple(cell for cell in term if occurrence[cell] == 1)
        require(private,
                "a negative polarized term lost all private source cells")
        private_cells.append(private[0])
    require(len(set(private_cells)) == 6,
            "two private coefficient pivots collided")

    weights = {cell: Fraction(1) for cell in support}
    for cell in private_cells:
        weights[cell] = Fraction(-1)
    row_values = []
    for positive, negative in zip(positive_terms, negative_terms):
        values = (term_value(positive, weights),
                  term_value(negative, weights))
        require(values == (Fraction(1), Fraction(-1))
                and sum(values) == 0,
                "the rational polarized binomial point changed")
        row_values.append([str(value) for value in values])

    # Guard the scope honestly: this rational point solves the six polarized
    # circuit rows, not the complete top tensor on the 28-cell union.  Record
    # the first other mixed word whose coefficient survives.
    extra_mixed = []
    full_live_histogram = Counter()
    for word in itertools.product(range(3), repeat=6):
        live = tuple(decorated_term(index, word)
                     for index in range(len(G.MATCHINGS))
                     if set(decorated_term(index, word)) <= support)
        if not live:
            continue
        full_live_histogram[len(live)] += 1
        coefficient = sum((term_value(term, weights) for term in live),
                          Fraction(0))
        if coefficient and len(set(word)) >= 2:
            extra_mixed.append((word, coefficient, live))
    require(extra_mixed,
            "the six-row counterpacket unexpectedly became a full top source")
    first_extra_word, first_extra_coefficient, first_extra_terms = extra_mixed[0]

    columns = tuple(sorted(support))
    exponent_rows = []
    for positive, negative in zip(positive_terms, negative_terms):
        exponent_rows.append([
            int(cell in positive) - int(cell in negative)
            for cell in columns
        ])
    decorated_matrix = sp.Matrix(exponent_rows)
    require(decorated_matrix.rank() == 6,
            "source provenance stopped splitting the physical circuit")
    require(any(sum(decorated_matrix[row, column] for row in range(6))
                for column in range(len(columns))),
            "the decorated rows unexpectedly recovered physical holonomy")

    doubled_occurrences = positive_terms[:2]
    require(set(doubled_occurrences[0]).isdisjoint(doubled_occurrences[1]),
            "the two doubled-matching grades stopped being disjoint")
    return {
        "row_words": [list(word) for word in WORDS],
        "all_rows_mixed_target": True,
        "complete_fibre_matching_indices": fibre_indices,
        "decorated_support_cells": len(support),
        "decorated_matching_occurrences": len(all_terms),
        "doubled_physical_matching": [list(edge)
                                       for edge in G.MATCHINGS[POSITIVE[0]]],
        "doubled_decorated_occurrences_disjoint": True,
        "private_negative_cells": [
            [list(edge), list(colours)] for edge, colours in private_cells
        ],
        "decorated_exponent_rank": decorated_matrix.rank(),
        "rational_row_values": row_values,
        "full_support_scope_guard": {
            "live_fibre_histogram": dict(sorted(full_live_histogram.items())),
            "nonzero_other_mixed_rows": len(extra_mixed),
            "first_nonzero_other_mixed_word": list(first_extra_word),
            "first_nonzero_other_mixed_coefficient": str(
                first_extra_coefficient
            ),
            "first_nonzero_other_mixed_terms": len(first_extra_terms),
        },
        "minimal_binomial_rows": 6,
        "verdict": (
            "the six physical moves lift to six independent source-labelled "
            "characters with an exact nonzero rational solution"
        ),
    }


def main():
    physical = physical_circuit_audit()
    provenance = source_provenance_audit()
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "physical_circuit": physical,
        "polarized_source_provenance": provenance,
        "verdict": (
            "the doubled physical matching does not force an ordinary "
            "parallel-collision or translated-target unit under arbitrary "
            "endpoint decorations: a minimal six-binomial mixed-word lift "
            "is coefficient-feasible and has no decorated character cycle"
        ),
        "scope": (
            "six complete mixed top fibres realizing the primitive physical "
            "circuit; this is a source-provenance counterpacket, not a full "
            "GHZ source.  The checker explicitly records surviving other "
            "mixed top rows on its support"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"multiplicity grade-split ledger changed: {digest}")

    print("N=8 one-bad multiplicity polarized grade split: PASS")
    print("physical support/rank/nullity: 11 / 10 / 1")
    print("source rows/cells/decorated rank: 6 / 28 / 6")
    print("six complete mixed fibres: exact binomials, rational torus point")
    print("doubled-grade-only collision/target forcing: FALSE")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
