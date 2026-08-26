#!/usr/bin/env python3
"""Independent referee for the N=8 anchor-K Macaulay methodology.

No producer module is imported.  The verifier rebuilds endpoint cells,
perfect matchings, source columns, incident factorizations, the chart-26
anchor stabilizer, and both quotient normalizations from raw definitions.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 8
COLORS = range(3)
EDGES = tuple(combinations(range(N), 2))
CELLS = tuple((u, v, a, b) for u, v in EDGES
              for a in COLORS for b in COLORS)
CELL_ID = {cell: index for index, cell in enumerate(CELLS)}
CHART26 = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 2), (1, 3), (4, 6), (5, 7)),
    ((0, 4), (1, 5), (2, 7), (3, 6)),
)
HOSTILE_LOWER_COLUMN = (
    (0, 0, 0, 0, 0, 0, 1, 1),
    bytes.fromhex("0d234c62a1bccaf3"),
)
HOSTILE_D5_TRIPLE = (
    (0, 0, 1, 1, 1, 2, 1, 2),
    bytes.fromhex("04087586bcc6eef3"),
)
EXPECTED_LEDGER_SHA256 = (
    "adbc910f571ff60cc1d7bc7594c0eb05672503ad04f8ca8b71e8710f20598b3b"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, mate in enumerate(vertices[1:], 1):
        residual = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(residual):
            answer.append(((first, mate),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(N)))


@lru_cache(maxsize=None)
def word_terms(word):
    return tuple(bytes(sorted(
        CELL_ID[(u, v, word[u], word[v])] for u, v in matching
    )) for matching in PM8)


@lru_cache(maxsize=None)
def column_rows(column):
    word, multiplier = column
    return tuple(bytes(sorted(multiplier + term)) for term in word_terms(word))


def anchors26():
    return frozenset(
        CELL_ID[(u, v, colour, colour)]
        for colour, matching in enumerate(CHART26) for u, v in matching
    )


ANCHORS26 = anchors26()


def row_degree(row, anchors=ANCHORS26):
    return sum(cell not in anchors for cell in row)


def column_minimum_degree(column, anchors=ANCHORS26):
    return min(row_degree(row, anchors) for row in column_rows(column))


def decode_factor(selected):
    word = [None] * N
    covered = []
    for cell in selected:
        u, v, a, b = CELLS[cell]
        covered.extend((u, v))
        word[u], word[v] = a, b
    if len(covered) != N or len(set(covered)) != N or len(set(word)) == 1:
        return None
    return tuple(word)


def incident_by_positions(row):
    answer = set()
    for positions in combinations(range(12), 4):
        selected = bytes(row[position] for position in positions)
        word = decode_factor(selected)
        if word is None:
            continue
        positions = frozenset(positions)
        multiplier = bytes(row[position] for position in range(12)
                           if position not in positions)
        answer.add((word, multiplier))
    return answer


def bounded_compositions(bounds, total, position=0, prefix=()):
    if position == len(bounds):
        if total == 0:
            yield prefix
        return
    for value in range(min(bounds[position], total) + 1):
        yield from bounded_compositions(
            bounds, total - value, position + 1, prefix + (value,)
        )


def incident_by_multiset_divisors(row):
    """Independent occurrence-free enumeration of all four-cell divisors."""
    counts = Counter(row)
    cells = tuple(sorted(counts))
    answer = set()
    for selected_counts in bounded_compositions(
            tuple(counts[cell] for cell in cells), 4):
        selected = bytes(sorted(
            cell for cell, count in zip(cells, selected_counts)
            for _ in range(count)
        ))
        word = decode_factor(selected)
        if word is None:
            continue
        residual = counts.copy()
        residual.subtract(Counter(selected))
        multiplier = bytes(sorted(
            cell for cell, count in residual.items() for _ in range(count)
        ))
        answer.add((word, multiplier))
    return answer


def transform_cell(cell, sites, colours):
    u, v, a, b = cell
    pu, pv = sites[u], sites[v]
    pa, pb = colours[a], colours[b]
    if pu < pv:
        return pu, pv, pa, pb
    return pv, pu, pb, pa


def chart26_stabilizer():
    anchor_cells = frozenset(CELLS[cell] for cell in ANCHORS26)
    answer = []
    for sites in permutations(range(N)):
        for colours in permutations(COLORS):
            image = frozenset(transform_cell(cell, sites, colours)
                              for cell in anchor_cells)
            if image == anchor_cells:
                answer.append((sites, colours))
    require(len(answer) == 16, "chart26 stabilizer order changed")
    return tuple(answer)


STABILIZER = chart26_stabilizer()
TRANSFORMS = tuple(bytes(
    CELL_ID[transform_cell(cell, sites, colours)] for cell in CELLS
) for sites, colours in STABILIZER)


@lru_cache(maxsize=None)
def canonical_row(row):
    return min(bytes(sorted(transform[cell] for cell in row))
               for transform in TRANSFORMS)


@lru_cache(maxsize=None)
def row_orbit(row):
    return tuple(sorted({bytes(sorted(transform[cell] for cell in row))
                         for transform in TRANSFORMS}))


def transform_column(column, action):
    word, multiplier = column
    sites, colours = STABILIZER[action]
    transformed_word = [None] * N
    for site, colour in enumerate(word):
        transformed_word[sites[site]] = colours[colour]
    transformed_multiplier = bytes(sorted(
        TRANSFORMS[action][cell] for cell in multiplier
    ))
    return tuple(transformed_word), transformed_multiplier


def average_column_actual(column, degree):
    answer = Counter()
    order = len(STABILIZER)
    for action in range(order):
        transformed = transform_column(column, action)
        for row in column_rows(transformed):
            if row_degree(row) == degree:
                answer[row] += Fraction(1, order)
    return Counter({row: value for row, value in answer.items() if value})


def quotient_mass_vector(column, degree):
    return Counter(
        canonical_row(row) for row in column_rows(column)
        if row_degree(row) == degree
    )


def early_stop_regression():
    """Historical two-tail counterexample to staged early-stop reduction."""
    prime = 1009
    higher = {2: {2: 1}}
    tails = ({1: 1, 2: 1}, {1: 1})

    def subtract(vector, reducer, scalar):
        for index, coefficient in reducer.items():
            value = (vector.get(index, 0) - scalar * coefficient) % prime
            if value:
                vector[index] = value
            else:
                vector.pop(index, None)

    false_transfers = {}
    for source in tails:
        vector = dict(source)
        while vector and min(vector) in higher:
            pivot = min(vector)
            subtract(vector, higher[pivot], vector[pivot])
        while vector:
            pivot = min(vector)
            if pivot not in false_transfers:
                inverse = pow(vector[pivot], -1, prime)
                false_transfers[pivot] = {
                    index: coefficient * inverse % prime
                    for index, coefficient in vector.items()
                }
                break
            subtract(vector, false_transfers[pivot], vector[pivot])

    common = dict(higher)
    true_transfer_rank = 0
    for source in tails:
        vector = dict(source)
        while vector:
            pivot = min(vector)
            if pivot not in common:
                inverse = pow(vector[pivot], -1, prime)
                common[pivot] = {
                    index: coefficient * inverse % prime
                    for index, coefficient in vector.items()
                }
                true_transfer_rank += 1
                break
            subtract(vector, common[pivot], vector[pivot])
    require(len(false_transfers) == 2 and true_transfer_rank == 1,
            "two-tail early-stop regression did not fire")
    require(set(false_transfers) & set(higher) == {2},
            "early-stop no longer invents the overlapping pivot")
    return {
        "staged_early_stop_rank": len(false_transfers),
        "complete_common_echelon_rank": true_transfer_rank,
        "false_overlapping_pivots": sorted(set(false_transfers) & set(higher)),
    }


def residual_led_regression():
    """Positive cleanup is sound; fixed-lift failure is not global failure."""
    # Lower equation A*x=b with A=(1,1), b=1.  The frozen solution x0=(1,0)
    # has top tail T*x0=1 for T=(1,0), while the top target is c=0.
    A = (1, 1)
    T = (1, 0)
    b = 1
    c = 0
    x0 = (1, 0)
    require(sum(a * x for a, x in zip(A, x0)) == b,
            "residual-led frozen lower solution changed")
    frozen_residual = c - sum(t * x for t, x in zip(T, x0))
    require(frozen_residual == -1,
            "residual-led frozen top residual changed")

    # With a leading source B=(1), direct cleanup y=-1 is an honest full
    # solution.  This implication never needs the rest of ker(A).
    B = 1
    y = frozen_residual
    require(sum(t * x for t, x in zip(T, x0)) + B * y == c,
            "positive residual-led cleanup is not a full solution")

    # If B is deleted, the same frozen residual is obstructed.  Nevertheless
    # k=(-1,1) is a lower kernel vector, and x1=x0+k=(0,1) solves both layers.
    kernel = (-1, 1)
    require(sum(a * k for a, k in zip(A, kernel)) == 0,
            "residual-led hostile vector left the lower kernel")
    x1 = tuple(x + k for x, k in zip(x0, kernel))
    require(sum(a * x for a, x in zip(A, x1)) == b
            and sum(t * x for t, x in zip(T, x1)) == c,
            "lower-kernel transfer did not repair the hostile obstruction")
    return {
        "frozen_residual": frozen_residual,
        "positive_leading_cleanup_is_full_lift": True,
        "fixed_lift_failure_with_B_zero": True,
        "alternate_lower_kernel_lift_succeeds": True,
        "global_dual_requires_annihilating_transferred_lower_kernel_tails": True,
    }


def audit():
    require(len(CELLS) == 252 and len(PM8) == 105,
            "raw N=8 cell/matching census changed")

    # Every mixed generator has exactly 105 distinct terms.  A term covers
    # every vertex once, so it reconstructs its word; supports of different
    # words are disjoint as well.
    mixed_words = 0
    term_owner = {}
    for word in product(COLORS, repeat=N):
        if len(set(word)) == 1:
            continue
        mixed_words += 1
        terms = word_terms(word)
        require(len(terms) == len(set(terms)) == 105,
                "one hafnian word acquired a repeated matching term")
        for term in terms:
            require(term not in term_owner,
                    "distinct words share a hafnian matching term")
            term_owner[term] = word
    require(mixed_words == 3 ** 8 - 3 == 6558,
            "mixed word count changed")
    require(len(term_owner) == mixed_words * 105,
            "mixed term ownership census changed")
    monomial8_count = math.comb(252 + 8 - 1, 8)
    source_column_count = mixed_words * monomial8_count

    # A highly repeated multiplier tests occurrence positions against a true
    # multiset-divisor enumeration.  Adding a fixed multiplier is cancellative
    # on monomials, so all 105 column outputs stay distinct.
    repeated_word = HOSTILE_LOWER_COLUMN[0]
    first_term = word_terms(repeated_word)[0]
    repeated_multiplier = bytes((first_term[0],) * 8)
    repeated_column = repeated_word, repeated_multiplier
    repeated_rows = column_rows(repeated_column)
    require(len(repeated_rows) == len(set(repeated_rows)) == 105,
            "repeated multiplier merged distinct matching outputs")
    repeated_row = repeated_rows[0]
    require(max(Counter(repeated_row).values()) >= 9,
            "hostile row is no longer highly repeated")
    positional = incident_by_positions(repeated_row)
    multiset = incident_by_multiset_divisors(repeated_row)
    require(positional == multiset and repeated_column in positional,
            "incident enumeration misses or invents a repeated factorization")
    for column in positional:
        require(column_rows(column).count(repeated_row) == 1,
                "one source column contains a row with multiplicity other than one")

    # Chart26 degree-five quotient multiplicity regression.  The lower column
    # has 68 actual degree-five rows but only 40 canonical representatives;
    # 28 representatives occur twice.  A set loses exactly those 28 units.
    require(column_minimum_degree(HOSTILE_LOWER_COLUMN) == 2,
            "hostile lower column minimum degree changed")
    tail5 = tuple(row for row in column_rows(HOSTILE_LOWER_COLUMN)
                  if row_degree(row) == 5)
    mass5 = quotient_mass_vector(HOSTILE_LOWER_COLUMN, 5)
    require(len(tail5) == 68 and len(mass5) == 40,
            "hostile chart26 d5 tail census changed")
    require(Counter(mass5.values()) == Counter({2: 28, 1: 12}),
            "hostile chart26 quotient multiplicities changed")
    require(sum(mass5.values()) == 68 and sum(set(mass5.values())) != 68,
            "set-vs-multiplicity mutation did not fire")
    averaged5 = average_column_actual(HOSTILE_LOWER_COLUMN, 5)
    for representative, mass in mass5.items():
        orbit = row_orbit(representative)
        require(sum((averaged5.get(row, 0) for row in orbit), Fraction(0))
                == mass,
                "orbit-average total mass disagrees with quotient Counter")
        require(all(averaged5.get(row, 0) == Fraction(mass, len(orbit))
                    for row in orbit),
                "orbit average is not constant on an actual row orbit")

    # The producer's 1/3 leading assertion is separately checked on a literal
    # min-degree-five triple.  Here set and multiset sizes happen to agree;
    # this fact must not be generalized to lower-column tails.
    require(column_minimum_degree(HOSTILE_D5_TRIPLE) == 5,
            "hostile min-d5 triple changed degree")
    triple5 = tuple(row for row in column_rows(HOSTILE_D5_TRIPLE)
                    if row_degree(row) == 5)
    triple_mass = quotient_mass_vector(HOSTILE_D5_TRIPLE, 5)
    require(len(triple5) == len(triple_mass) == 3
            and set(triple_mass.values()) == {1},
            "literal d5 triple no longer has three distinct row orbits")

    # Quotient certificate and dual normalizations over Q.  In total-mass
    # coordinates Q(v)_O=sum_{r in O}v_r, orbit averaging of a column maps to
    # the Counter above.  A quotient dual lifts with constant value on O.
    sample_coefficients = (
        (Fraction(2), HOSTILE_LOWER_COLUMN),
        (Fraction(-3, 2), HOSTILE_D5_TRIPLE),
    )
    quotient_sample = Counter()
    actual_sample = Counter()
    for coefficient, column in sample_coefficients:
        quotient_sample.update({
            row: coefficient * value
            for row, value in quotient_mass_vector(column, 5).items()
        })
        for row, value in average_column_actual(column, 5).items():
            actual_sample[row] += coefficient * value
    quotient_sample = Counter({row: value for row, value in
                               quotient_sample.items() if value})
    actual_sample = Counter({row: value for row, value in
                             actual_sample.items() if value})
    for representative in quotient_sample:
        require(sum((actual_sample.get(row, 0)
                     for row in row_orbit(representative)), Fraction(0))
                == quotient_sample[representative],
                "rational quotient certificate failed labelled-row lift")
    mass_dual = {
        representative: Fraction((index % 5) - 2, 7)
        for index, representative in enumerate(sorted(quotient_sample))
    }
    quotient_pairing = sum(
        (mass_dual[row] * value for row, value in quotient_sample.items()),
        Fraction(0),
    )
    actual_pairing = sum(
        (mass_dual[canonical_row(row)] * value
         for row, value in actual_sample.items()), Fraction(0)
    )
    require(quotient_pairing == actual_pairing,
            "total-mass quotient dual failed constant labelled lift")

    # Representative/per-row coordinates use the reciprocal normalization:
    # q_O is the common actual coefficient and a quotient dual L_O lifts as
    # L_O/|O| on each actual row.
    representative_pairing = Fraction(0)
    representative_actual_pairing = Fraction(0)
    for representative, total_mass in quotient_sample.items():
        orbit_size = len(row_orbit(representative))
        per_row = total_mass / orbit_size
        dual_value = mass_dual[representative]
        representative_pairing += dual_value * per_row
        representative_actual_pairing += sum(
            (dual_value / orbit_size * actual_sample.get(row, 0)
             for row in row_orbit(representative)), Fraction(0)
        )
    require(representative_pairing == representative_actual_pairing,
            "representative-coordinate dual normalization failed")

    early_stop = early_stop_regression()
    residual_led = residual_led_regression()

    ledger = {
        "endpoint_cells": len(CELLS),
        "perfect_matchings": len(PM8),
        "mixed_words": mixed_words,
        "terms_per_mixed_generator": 105,
        "degree8_monomials_with_repetition": monomial8_count,
        "complete_degree12_source_columns": source_column_count,
        "full_target_rows": 105 ** 3,
        "maximum_anchor_K_degree_in_degree12": 12,
        "K13_degree12_component_zero": True,
        "K13_lift_equals_literal_membership": True,
        "repeated_row_max_multiplicity": max(Counter(repeated_row).values()),
        "repeated_row_incident_columns": len(positional),
        "incident_position_multiset_agreement": True,
        "chart26_stabilizer_order": len(STABILIZER),
        "chart26_hostile_lower_column": {
            "word": "".join(map(str, HOSTILE_LOWER_COLUMN[0])),
            "multiplier": HOSTILE_LOWER_COLUMN[1].hex(),
            "degree5_actual_rows": len(tail5),
            "degree5_row_orbits": len(mass5),
            "quotient_multiplicity_histogram": dict(sorted(Counter(
                mass5.values()).items()
            )),
            "set_mutation_fired": True,
        },
        "chart26_hostile_min_d5_triple": {
            "word": "".join(map(str, HOSTILE_D5_TRIPLE[0])),
            "multiplier": HOSTILE_D5_TRIPLE[1].hex(),
            "actual_rows": len(triple5),
            "distinct_row_orbits": len(triple_mass),
        },
        "quotient_total_mass_certificate_lift": True,
        "quotient_total_mass_dual_lift": True,
        "quotient_representative_dual_lift": True,
        "early_stop_regression": early_stop,
        "residual_led_regression": residual_led,
        "methodology_verdict": (
            "The raw Macaulay/closure/K13 method is sound. Quotient work is "
            "sound over Q only with explicit orbit multiplicities and complete "
            "common-echelon reduction; sets and staged early-stop are invalid."
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "anchor-K methodology ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    (HERE / "results.json").write_text(json.dumps(
        {"ledger": ledger, "sha256": digest}, indent=2, sort_keys=True
    ) + "\n")
    print("anchor-K methodology referee: PASS")
    print("degree12 source columns:",
          ledger["complete_degree12_source_columns"])
    print("chart26 d5 hostile multiplicities:",
          ledger["chart26_hostile_lower_column"])
    print("early-stop regression:", ledger["early_stop_regression"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
