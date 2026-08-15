#!/usr/bin/env python3
"""Minimum unspecialized EqSystem S-chain for the C6 parent anti-diagonal.

Work in the literal six-site, three-colour coefficient system with all 135
ordered endpoint-colour variables.  For each of the two mixed words
111001 and 111221, the parent anti-diagonal M0-M1 has no degree-three
coefficient-row lift.  In degree four, however, a missing endpoint-colour
cell on any edge of M0 triangle M1 gives a two-row Macaulay S-chain.  After
deleting that cell the chain is +1 on M0, -1 on M1, and has thirteen fully
labelled outside matching exits.

The checker also exhausts every one-variable multigrade (135 per word),
retains pure-row lower terms, and constructs the first symmetric two-word
degree-five packet.  No missing pure anchor is specialized to a unit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c6_nine_cell_toric_exchange_parent_antidiagonal_nonlift.py":
        "586b67e0dfdee266cd16731ac22eb1d5560721c71b05a55603e3245d2322622f",
    "notes/2026-08-14-c6-nine-cell-toric-exchange-parent-antidiagonal-nonlift.md":
        "5e038f383da171baf36d5fe7a974cc5b9bdfe0ab348016e045aecfcca732350e",
}

N = 6
COLOURS = tuple(range(3))
SITES = tuple(range(N))
WORDS = tuple(product(COLOURS, repeat=N))
EDGES = tuple(combinations(SITES, 2))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))
M0 = tuple(sorted(((0, 5), (1, 2), (3, 4))))
M1 = tuple(sorted(((0, 1), (2, 5), (3, 4))))
WORDS_OF_INTEREST = ((1, 1, 1, 0, 0, 1), (1, 1, 1, 2, 2, 1))

# A variable is a_uv^(alpha,beta), with u<v and the colours in endpoint
# order.  This is the unspecialized 15*9=135-variable source ring.
VARIABLES = tuple((left, right, alpha, beta)
                  for left, right in EDGES
                  for alpha, beta in product(COLOURS, repeat=2))
VARIABLE_INDEX = {variable: index
                  for index, variable in enumerate(VARIABLES)}


def word_name(word):
    return "".join(map(str, word))


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def variable_name(index):
    left, right, alpha, beta = VARIABLES[index]
    return f"a{left}{right}^{alpha}{beta}"


def monomial_name(monomial):
    return "*".join(variable_name(index) for index in monomial) or "1"


def variable_for(edge, word):
    left, right = edge
    return VARIABLE_INDEX[(left, right, word[left], word[right])]


def matching_monomial(matching, word):
    return tuple(sorted(variable_for(edge, word) for edge in matching))


def word_grade(word):
    return tuple(int(colour == word[site])
                 for site in SITES for colour in COLOURS)


def variable_grade(index):
    left, right, alpha, beta = VARIABLES[index]
    grade = [0] * (N * len(COLOURS))
    grade[3 * left + alpha] += 1
    grade[3 * right + beta] += 1
    return tuple(grade)


VARIABLE_GRADES = tuple(variable_grade(index)
                        for index in range(len(VARIABLES)))
VARIABLE_BY_GRADE = {grade: index
                     for index, grade in enumerate(VARIABLE_GRADES)}


def add_grades(first, second):
    return tuple(left + right for left, right in zip(first, second,
                                                     strict=True))


def subtract_grades(first, second):
    return tuple(left - right for left, right in zip(first, second,
                                                     strict=True))


def add_polynomials(*scaled_polynomials):
    answer = defaultdict(Fraction)
    for scale, polynomial in scaled_polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += Fraction(scale) * coefficient
    return {monomial: coefficient
            for monomial, coefficient in answer.items() if coefficient}


def multiply_by_variable(polynomial, variable):
    return {tuple(sorted(monomial + (variable,))): coefficient
            for monomial, coefficient in polynomial.items()}


def differentiate(polynomial, variable):
    answer = defaultdict(Fraction)
    for monomial, coefficient in polynomial.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        reduced = list(monomial)
        reduced.remove(variable)
        answer[tuple(reduced)] += multiplicity * coefficient
    return {monomial: coefficient
            for monomial, coefficient in answer.items() if coefficient}


def coefficient_row(word):
    row = {matching_monomial(matching, word): Fraction(1)
           for matching in MATCHINGS}
    # Retain the affine target term.  In particular, never replace an absent
    # pure anchor by -1 after a support specialization.
    if len(set(word)) == 1:
        row[()] = Fraction(-1)
    return row


def macaulay_column(word, multiplier):
    return multiply_by_variable(coefficient_row(word), multiplier)


def degree_four_candidates(word, multiplier):
    grade = add_grades(word_grade(word), VARIABLE_GRADES[multiplier])
    candidates = []
    for companion_word in WORDS:
        needed = subtract_grades(grade, word_grade(companion_word))
        companion_multiplier = VARIABLE_BY_GRADE.get(needed)
        if companion_multiplier is not None:
            candidates.append((companion_word, companion_multiplier))
    return tuple(candidates)


def rank_two(vectors):
    nonzero = [tuple(map(Fraction, vector)) for vector in vectors
               if any(vector)]
    if not nonzero:
        return 0
    first = nonzero[0]
    if all(first[0] * vector[1] == first[1] * vector[0]
           for vector in nonzero[1:]):
        return 1
    return 2


def parent_projection(polynomial, leading):
    return tuple(polynomial.get(monomial, Fraction(0))
                 for monomial in leading)


def degree_three_gate():
    records = {}
    for word in WORDS_OF_INTEREST:
        leading = (matching_monomial(M0, word),
                   matching_monomial(M1, word))
        projection = parent_projection(coefficient_row(word), leading)
        require(projection == (1, 1), (word, projection))
        delta = projection[0] - projection[1]
        require(delta == 0, (word, delta))
        records[word_name(word)] = {
            "only_row_in_squarefree_word_grade": f"F_{word_name(word)}",
            "parent_projection": tuple(map(int, projection)),
            "primitive_dual": "delta=c[M0]-c[M1]",
            "dual_on_row": int(delta),
            "dual_on_desired_face": 2,
        }
    require(word_grade(WORDS_OF_INTEREST[0]) !=
            word_grade(WORDS_OF_INTEREST[1]), "word grades collapsed")
    return {
        "minimum_degree_lower_bound": 4,
        "two_word_grades_are_distinct": True,
        "records": records,
    }


def expected_restricted_sign(edge, matching):
    # Choose the global sign so that M0 has +1 and M1 has -1.
    orientation = 1 if edge in set(M1) - set(M0) else -1
    return Fraction(orientation * (1 - 2 * int(edge in matching)))


def construct_spair(word, edge, alternate_pair):
    left, right = edge
    original_pair = (word[left], word[right])
    require(alternate_pair != original_pair,
            (word, edge, alternate_pair, original_pair))
    missing = VARIABLE_INDEX[edge + alternate_pair]
    original = VARIABLE_INDEX[edge + original_pair]
    companion = list(word)
    companion[left], companion[right] = alternate_pair
    companion = tuple(companion)
    orientation = 1 if edge in set(M1) - set(M0) else -1
    chain = add_polynomials(
        (orientation, macaulay_column(word, missing)),
        (-2 * orientation, macaulay_column(companion, original)),
    )
    restricted = differentiate(chain, missing)
    expected = {
        matching_monomial(matching, word):
            expected_restricted_sign(edge, matching)
        for matching in MATCHINGS
    }
    require(restricted == expected,
            (word, edge, alternate_pair, restricted, expected))
    leading = (matching_monomial(M0, word),
               matching_monomial(M1, word))
    require(parent_projection(restricted, leading) == (1, -1),
            (word, edge, alternate_pair,
             parent_projection(restricted, leading)))
    exits = tuple((matching, expected[matching_monomial(matching, word)])
                  for matching in MATCHINGS if matching not in (M0, M1))
    require(len(chain) == 27, (word, edge, alternate_pair, len(chain)))
    require(len(restricted) == 15 and len(exits) == 13,
            (len(restricted), len(exits)))
    require(not any(len(monomial) < 4 for monomial in chain),
            "mixed-row chain unexpectedly acquired an affine target term")
    return {
        "word": companion,
        "missing_variable": missing,
        "original_variable": original,
        "orientation": orientation,
        "chain": chain,
        "restricted": restricted,
        "exits": exits,
    }


def exit_ledger(word, restricted):
    records = []
    for matching in MATCHINGS:
        if matching in (M0, M1):
            continue
        monomial = matching_monomial(matching, word)
        records.append({
            "matching": matching_name(matching),
            "coefficient": str(restricted[monomial]),
            "decorated_monomial": monomial_name(monomial),
            "status": "outside nine-cell word fibre",
        })
    return tuple(records)


def degree_four_census():
    symmetric_edges = tuple(sorted(set(M0) ^ set(M1)))
    require(symmetric_edges == ((0, 1), (0, 5), (1, 2), (2, 5)),
            symmetric_edges)
    word_records = {}
    complete_records = []
    for word in WORDS_OF_INTEREST:
        candidate_histogram = Counter()
        projection_rank_histogram = Counter()
        chain_grades = []
        pure_candidates = []
        for multiplier in range(len(VARIABLES)):
            candidates = degree_four_candidates(word, multiplier)
            columns = tuple(macaulay_column(companion_word,
                                             companion_multiplier)
                            for companion_word, companion_multiplier
                            in candidates)
            leading = (
                tuple(sorted(matching_monomial(M0, word) + (multiplier,))),
                tuple(sorted(matching_monomial(M1, word) + (multiplier,))),
            )
            projections = tuple(parent_projection(column, leading)
                                for column in columns)
            projection_rank = rank_two(projections)
            candidate_histogram[len(candidates)] += 1
            projection_rank_histogram[projection_rank] += 1
            for companion_word, companion_multiplier in candidates:
                if len(set(companion_word)) == 1:
                    pure_candidates.append((companion_word,
                                            companion_multiplier))
                    column = macaulay_column(companion_word,
                                             companion_multiplier)
                    require(column.get((companion_multiplier,)) == -1,
                            (companion_word, companion_multiplier, column))

            left, right, alpha, beta = VARIABLES[multiplier]
            edge = (left, right)
            original_pair = (word[left], word[right])
            expected_rank = (2 if edge in symmetric_edges and
                             (alpha, beta) != original_pair else 1)
            require(projection_rank == expected_rank,
                    (word, VARIABLES[multiplier], projections,
                     projection_rank, expected_rank))
            if projection_rank == 2:
                packet = construct_spair(word, edge, (alpha, beta))
                chain_grades.append(VARIABLES[multiplier])
                require(packet["missing_variable"] == multiplier,
                        (packet, multiplier))

            complete_records.append({
                "word": word_name(word),
                "multiplier": variable_name(multiplier),
                "candidate_count": len(candidates),
                "candidate_labels": tuple(
                    (word_name(companion_word),
                     variable_name(companion_multiplier))
                    for companion_word, companion_multiplier in candidates
                ),
                "parent_projections": tuple(
                    tuple(map(str, projection)) for projection in projections
                ),
                "projection_rank": projection_rank,
            })

        require(candidate_histogram == Counter({1: 15, 2: 60, 4: 60}),
                (word, candidate_histogram))
        require(projection_rank_histogram == Counter({1: 103, 2: 32}),
                (word, projection_rank_histogram))
        require(len(chain_grades) == 32, (word, chain_grades))
        require(tuple((word_name(pure), variable_name(multiplier))
                      for pure, multiplier in pure_candidates) ==
                (("111111", "a34^00" if word[3] == 0 else "a34^22"),),
                (word, pure_candidates))
        word_records[word_name(word)] = {
            "all_endpoint_colour_multipliers": len(VARIABLES),
            "candidate_count_histogram": dict(sorted(candidate_histogram.items())),
            "parent_projection_rank_histogram":
                dict(sorted(projection_rank_histogram.items())),
            "oriented_spair_grades": len(chain_grades),
            "classification": (
                "four edges in M0 triangle M1 times eight non-original "
                "ordered endpoint-colour pairs"
            ),
            "retained_pure_candidate": tuple(
                (word_name(pure), variable_name(multiplier),
                 f"-{variable_name(multiplier)}")
                for pure, multiplier in pure_candidates
            ),
        }

    payload = json.dumps(complete_records, sort_keys=True,
                         separators=(",", ":"))
    return {
        "all_words_in_source_inventory": len(WORDS),
        "all_endpoint_colour_variables": len(VARIABLES),
        "target_words": word_records,
        "full_270_grade_record_sha256": sha256(payload.encode()).hexdigest(),
    }


def representative_chains():
    edge = (0, 1)
    alternate = (0, 0)
    records = {}
    packets = {}
    for word in WORDS_OF_INTEREST:
        packet = construct_spair(word, edge, alternate)
        packets[word] = packet
        records[word_name(word)] = {
            "chain": (
                f"a01^00 F_{word_name(word)} - "
                f"2 a01^11 F_{word_name(packet['word'])}"
            ),
            "degree_four_term_count_before_deletion": len(packet["chain"]),
            "restriction": "set a01^00=0 after d/da01^00",
            "restricted_matching_term_count": len(packet["restricted"]),
            "leading_face": {matching_name(M0): "+1",
                             matching_name(M1): "-1"},
            "all_surviving_outside_exits":
                exit_ledger(word, packet["restricted"]),
        }

    # The first common multigrade containing both output words is the cap
    # K2,2 square.  All four coefficient rows remain diagonal on M0,M1.
    word0, word2 = WORDS_OF_INTEREST
    cap00 = VARIABLE_INDEX[(3, 4, 0, 0)]
    cap22 = VARIABLE_INDEX[(3, 4, 2, 2)]
    cap_candidates = degree_four_candidates(word0, cap22)
    require(cap_candidates == (
        ((1, 1, 1, 0, 0, 1), VARIABLE_INDEX[(3, 4, 2, 2)]),
        ((1, 1, 1, 0, 2, 1), VARIABLE_INDEX[(3, 4, 2, 0)]),
        ((1, 1, 1, 2, 0, 1), VARIABLE_INDEX[(3, 4, 0, 2)]),
        ((1, 1, 1, 2, 2, 1), VARIABLE_INDEX[(3, 4, 0, 0)]),
    ), cap_candidates)
    leading0 = (
        tuple(sorted(matching_monomial(M0, word0) + (cap22,))),
        tuple(sorted(matching_monomial(M1, word0) + (cap22,))),
    )
    leading2 = (
        tuple(sorted(matching_monomial(M0, word2) + (cap00,))),
        tuple(sorted(matching_monomial(M1, word2) + (cap00,))),
    )
    require(leading0 == leading2, (leading0, leading2))
    cap_projections = tuple(
        parent_projection(macaulay_column(word, multiplier), leading0)
        for word, multiplier in cap_candidates
    )
    require(cap_projections == ((1, 1), (0, 0), (0, 0), (1, 1)),
            cap_projections)

    # Multiplying the two one-word chains by the complementary cap cells
    # puts them in a single common degree-five multigrade.  Their even
    # average retains both root/output words and the same oriented face.
    synchronized = add_polynomials(
        (Fraction(1, 2), multiply_by_variable(packets[word0]["chain"], cap22)),
        (Fraction(1, 2), multiply_by_variable(packets[word2]["chain"], cap00)),
    )
    synchronized_restriction = differentiate(
        synchronized, VARIABLE_INDEX[(0, 1, 0, 0)])
    require(parent_projection(synchronized_restriction, leading0) == (1, -1),
            parent_projection(synchronized_restriction, leading0))
    synchronized_exits = tuple(
        {"coefficient": str(coefficient),
         "decorated_monomial": monomial_name(monomial)}
        for monomial, coefficient in sorted(synchronized_restriction.items())
        if monomial not in leading0
    )
    require((len(synchronized), len(synchronized_restriction),
             len(synchronized_exits)) == (49, 27, 25),
            (len(synchronized), len(synchronized_restriction),
             len(synchronized_exits)))
    return {
        "one_word_minimum_degree_four_chains": records,
        "first_common_cap_offdiagonal_grade": {
            "grade_identity": (
                "grade(111001)+grade(a34^22)="
                "grade(111221)+grade(a34^00)"
            ),
            "four_columns": tuple(
                (word_name(word), variable_name(multiplier))
                for word, multiplier in cap_candidates
            ),
            "parent_projections": tuple(tuple(map(int, projection))
                                        for projection in cap_projections),
            "primitive_dual": "delta=c[a34^22*M0]-c[a34^22*M1]",
            "verdict": (
                "the complete endpoint-colour K2,2 coefficient square has "
                "rank one on the parent face; an operation-changing "
                "offdiagonal companion must have nonzero delta"
            ),
        },
        "synchronized_two_word_degree_five_chain": {
            "formula": "(a34^22*G_111001+a34^00*G_111221)/2",
            "pre_deletion_term_count": len(synchronized),
            "post_deletion_term_count": len(synchronized_restriction),
            "leading_projection": (1, -1),
            "all_25_outside_exits": synchronized_exits,
        },
    }


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    return {
        "theorem": (
            "minimum unspecialized C6 EqSystem Macaulay S-chain for the "
            "parent anti-diagonal"
        ),
        "pins": PINS,
        "degree_three_primitive_dual": degree_three_gate(),
        "complete_degree_four_multigrade_census": degree_four_census(),
        "explicit_chains_and_exits": representative_chains(),
        "scope": (
            "literal six-site 135-variable EqSystem, all 729 word rows, both "
            "mixed output words, and every one-variable Macaulay grade. "
            "Affine pure-row lower terms are retained; no absent pure anchor "
            "is specialized to -1.  The degree-four construction gives a "
            "restricted parent face with outside exits, not an exact full "
            "GHZ source completion or support-deleting move."
        ),
    }


EXPECTED_LEDGER_SHA256 = "8ae3440c5925625e521b1801b77a202290f617f226b2b67c54978d7ab9c29283"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                ("unspecialized S-chain ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("C6 unspecialized EqSystem parent anti-diagonal S-chain: PASS")
    print("mode", arguments.mode)
    print("ledger_sha256", digest)
    print("minimum degree: 4 (two rows, 13 surviving outside exits)")
    print("first common two-word cap grade: rank 1; delta survives")


if __name__ == "__main__":
    main()
