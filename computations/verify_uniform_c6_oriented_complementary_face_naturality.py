#!/usr/bin/env python3
"""Audit oriented complementary-face naturality for the six C6 debts.

Starting from the sharp terminal-C6 support in commit 844c121, this checker
retains the physical cap, four-site window, common tail, output word, fine
matching occurrence, and operation labels.  It proves that every local mate
is monochromatic on its C4 window.  Colour-swapped mates can share geometry,
but they belong to different output words and hence cannot be assembled into
one source response without an additional word-changing comparison map.

It also verifies a uniform cap-sector identity and the smallest diagonal
three-direct counterguard: adding a live third-colour cell on the retained
cap forces a new word and a common monochromatic residual; mixed vanishing
kills that residual, so pure normalization must use a cap-avoiding escape.
"""

from __future__ import annotations

from collections import Counter
from itertools import product


COLOURS = tuple(range(3))
VERTICES = tuple(range(6))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(VERTICES)))
A_CHANNEL = tuple(sorted((edge(0, 1), edge(2, 3), edge(4, 5))))
B_CHANNEL = tuple(sorted((edge(0, 5), edge(1, 2), edge(3, 4))))


def occurrence_cells(matching, word):
    if any(word[left] != word[right] for left, right in matching):
        return None
    return frozenset((endpoints, word[endpoints[0]])
                     for endpoints in matching)


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def word_name(word):
    return "".join(map(str, word))


def word_on_matching(matching, assignment):
    word = [None] * len(VERTICES)
    for endpoints, colour in zip(matching, assignment, strict=True):
        for vertex in endpoints:
            word[vertex] = colour
    return tuple(word)


def compatible_matchings(word):
    return tuple(matching for matching in MATCHINGS
                 if occurrence_cells(matching, word) is not None)


def make_debt(assignment):
    word = word_on_matching(B_CHANNEL, assignment)
    counts = Counter(assignment)
    require(sorted(counts.values()) == [1, 2], (assignment, counts))
    minority = next(colour for colour, count in counts.items() if count == 1)
    majority = next(colour for colour, count in counts.items() if count == 2)
    cap = next(endpoints for endpoints, colour
               in zip(B_CHANNEL, assignment, strict=True)
               if colour == minority)
    window = tuple(vertex for vertex in VERTICES if vertex not in cap)
    residual_core = tuple(endpoints for endpoints in B_CHANNEL
                          if endpoints != cap)
    alternatives = tuple(matching for matching in compatible_matchings(word)
                         if matching != B_CHANNEL)
    require(len(alternatives) == 2, (word, alternatives))
    mate_residuals = tuple(
        tuple(endpoints for endpoints in matching if endpoints != cap)
        for matching in alternatives
    )
    require(all(cap in matching for matching in alternatives),
            (word, cap, alternatives))
    require(all(set(residual).isdisjoint(set(residual_core))
                for residual in mate_residuals),
            (word, residual_core, mate_residuals))
    third = next(iter(set(COLOURS) - {minority, majority}))
    return {
        "word": word,
        "word_label": f"word:{word_name(word)}",
        "cap": cap,
        "window": window,
        "tail_label": "tail:T",
        "operation_label": f"coefficient:{word_name(word)}",
        "minority": minority,
        "majority": majority,
        "third": third,
        "core_matching": B_CHANNEL,
        "core_fine": f"fine:{matching_name(B_CHANNEL)}",
        "residual_core": residual_core,
        "mate_matchings": alternatives,
        "mate_fines": tuple(f"fine:{matching_name(matching)}"
                            for matching in alternatives),
        "mate_residuals": mate_residuals,
    }


def six_debt_labelled_ledger():
    assignments = tuple(assignment
                        for assignment in product((1, 2), repeat=3)
                        if len(set(assignment)) == 2)
    debts = tuple(sorted((make_debt(assignment) for assignment in assignments),
                         key=lambda debt: debt["word"]))
    require(tuple(word_name(debt["word"]) for debt in debts) == (
        "111221", "122111", "122221",
        "211112", "211222", "222112",
    ), debts)

    expected = {
        "111221": (edge(3, 4), 1, 2,
                   ((edge(0, 1), edge(2, 5)),
                    (edge(0, 2), edge(1, 5)))),
        "122111": (edge(1, 2), 1, 2,
                   ((edge(0, 3), edge(4, 5)),
                    (edge(0, 4), edge(3, 5)))),
        "122221": (edge(0, 5), 2, 1,
                   ((edge(1, 3), edge(2, 4)),
                    (edge(1, 4), edge(2, 3)))),
        "211112": (edge(0, 5), 1, 2,
                   ((edge(1, 3), edge(2, 4)),
                    (edge(1, 4), edge(2, 3)))),
        "211222": (edge(1, 2), 2, 1,
                   ((edge(0, 3), edge(4, 5)),
                    (edge(0, 4), edge(3, 5)))),
        "222112": (edge(3, 4), 2, 1,
                   ((edge(0, 1), edge(2, 5)),
                    (edge(0, 2), edge(1, 5)))),
    }
    for debt in debts:
        cap, majority, minority, mates = expected[word_name(debt["word"])]
        require((debt["cap"], debt["majority"], debt["minority"],
                 debt["mate_residuals"]) ==
                (cap, majority, minority, mates), debt)
        # Every residual edge in the core and both mates is forced to the
        # one majority colour by the fixed output word.
        for flat in ((debt["residual_core"],)
                     + debt["mate_residuals"]):
            require(all(debt["word"][left] == debt["majority"]
                        and debt["word"][right] == debt["majority"]
                        for left, right in flat), (debt, flat))

    swapped_pairs = []
    for cap in B_CHANNEL:
        pair = tuple(debt for debt in debts if debt["cap"] == cap)
        require(len(pair) == 2, (cap, pair))
        first, second = pair
        require((first["majority"], first["minority"]) ==
                (second["minority"], second["majority"]), pair)
        require(first["window"] == second["window"]
                and first["mate_residuals"] == second["mate_residuals"]
                and first["tail_label"] == second["tail_label"], pair)
        require(first["word_label"] != second["word_label"]
                and first["operation_label"] != second["operation_label"],
                pair)
        swapped_pairs.append((first, second))
    return debts, tuple(swapped_pairs)


def complementary_face_lands(direct, p_colours, q_colours):
    complement = set(COLOURS) - {direct}
    return set(p_colours) == complement and set(q_colours) == complement


def oriented_naturality_no_go(debts, swapped_pairs):
    audited_faces = 0
    for debt in debts:
        # A coefficient C4 term has the same majority colour on every
        # residual role.  No choice of a distinct direct colour turns either
        # shore into the required complementary pair.
        monochrome_shore = (debt["majority"], debt["majority"])
        for direct in COLOURS:
            require(not complementary_face_lands(
                direct, monochrome_shore, monochrome_shore
            ), (debt, direct, monochrome_shore))
            audited_faces += 1

        # A third-colour diagonal cap cell is incompatible with the original
        # word.  Recolouring the cap endpoints creates a different word.
        third_word = list(debt["word"])
        for vertex in debt["cap"]:
            third_word[vertex] = debt["third"]
        third_word = tuple(third_word)
        require(third_word != debt["word"], (debt, third_word))
        require(word_name(third_word) not in (
            word_name(item["word"]) for item in debts
            if item["cap"] == debt["cap"]
        ), (debt, third_word))

    # Equal mate choices in a colour-swapped pair line up the physical C4,
    # but never the word/operation object.  Count the exact geometry-only
    # coincidences among the 2^6 first-mate selections.
    debt_index = {word_name(debt["word"]): index
                  for index, debt in enumerate(debts)}
    pair_indices = tuple(
        (debt_index[word_name(first["word"])],
         debt_index[word_name(second["word"])])
        for first, second in swapped_pairs
    )
    histogram = Counter()
    for choices in product((0, 1), repeat=len(debts)):
        paired = sum(choices[left] == choices[right]
                     for left, right in pair_indices)
        histogram[paired] += 1
    require(histogram == Counter({0: 8, 1: 24, 2: 24, 3: 8}), histogram)
    return {
        "monochromatic_direct_tests": audited_faces,
        "colour_swapped_physical_pairs": len(swapped_pairs),
        "geometry_only_pairing_histogram": tuple(sorted(histogram.items())),
        "same_word_paired_faces": 0,
    }


def poly_monomial(*variables):
    return {tuple(sorted(variables)): 1}


def poly_add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def poly_scale(scalar, polynomial):
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def poly_multiply(*polynomials):
    answer = {(): 1}
    for polynomial in polynomials:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                updated[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = {monomial: coefficient
                  for monomial, coefficient in updated.items() if coefficient}
    return answer


def common_residual_escape_identity():
    """Verify z_a F_b-z_b F_a=z_a E_b-z_b E_a termwise."""
    tail = poly_monomial("common_tail")
    residual = poly_add(
        poly_monomial("residual_core"),
        poly_monomial("residual_mate_1"),
        poly_monomial("residual_mate_2"),
    )
    cap_sector = {
        colour: poly_multiply(poly_monomial(f"cap_{colour}"), tail, residual)
        for colour in COLOURS
    }
    escapes = {colour: poly_monomial(f"escape_{colour}")
               for colour in COLOURS}
    full = {colour: poly_add(cap_sector[colour], escapes[colour])
            for colour in COLOURS}
    identities = []
    for majority in COLOURS:
        for mixed in set(COLOURS) - {majority}:
            left = poly_add(
                poly_multiply(poly_monomial(f"cap_{mixed}"), full[majority]),
                poly_scale(-1, poly_multiply(
                    poly_monomial(f"cap_{majority}"), full[mixed]
                )),
            )
            right = poly_add(
                poly_multiply(poly_monomial(f"cap_{mixed}"), escapes[majority]),
                poly_scale(-1, poly_multiply(
                    poly_monomial(f"cap_{majority}"), escapes[mixed]
                )),
            )
            require(left == right, (majority, mixed, left, right))
            identities.append((majority, mixed))
    require(len(identities) == 6, identities)
    return {
        "residual_terms_allowed": len(residual),
        "pure_mixed_elimination_identities": len(identities),
        "terminal_consequence": "mixed zero + no mixed escape => pure escape = 1",
    }


def minimal_three_direct_counterguard():
    cap = edge(3, 4)
    residual_core = (edge(0, 5), edge(1, 2))
    residual_mate = (edge(0, 1), edge(2, 5))
    support = frozenset(
        ((cap, colour) for colour in COLOURS)
    ) | frozenset(
        (endpoints, 1) for endpoints in residual_core + residual_mate
    )
    require(len(support) == 7, support)

    rows = {}
    for word in product(COLOURS, repeat=6):
        occurrences = []
        for matching in MATCHINGS:
            cells = occurrence_cells(matching, word)
            if cells is not None and cells <= support:
                occurrences.append((matching, cells))
        if occurrences:
            rows[word] = tuple(occurrences)
    expected_words = {
        (1, 1, 1, colour, colour, 1) for colour in COLOURS
    }
    require(set(rows) == expected_words, rows)
    require(all(len(occurrences) == 2 for occurrences in rows.values()), rows)
    for colour in COLOURS:
        word = (1, 1, 1, colour, colour, 1)
        expected_matchings = (
            tuple(sorted((cap,) + residual_mate)),
            tuple(sorted((cap,) + residual_core)),
        )
        require(tuple(item[0] for item in rows[word]) == expected_matchings,
                (word, rows[word], expected_matchings))

    # Three live direct cells plus two distinct four-site matchings require
    # 3+4 cells, so seven is minimal in this diagonal cap-sector model.
    require(len(set(residual_core) | set(residual_mate)) == 4,
            (residual_core, residual_mate))
    return {
        "cells": len(support),
        "cap": "34",
        "live_direct_colours": COLOURS,
        "nonzero_words": tuple(sorted(word_name(word) for word in rows)),
        "terms_per_word": tuple(sorted({len(value) for value in rows.values()})),
        "shore_colour_profile": (1, 1, 1, 1),
        "complementary_clean_cap_faces": 0,
        "first_full_source_obligation": "pure 111111 needs cap-avoiding escape",
    }


def main():
    require(len(MATCHINGS) == 15, len(MATCHINGS))
    debts, swapped_pairs = six_debt_labelled_ledger()
    naturality = oriented_naturality_no_go(debts, swapped_pairs)
    escape = common_residual_escape_identity()
    counterguard = minimal_three_direct_counterguard()
    print("uniform C6 oriented complementary-face naturality audit: PASS")
    print("six labelled debts", tuple({
        "word": word_name(debt["word"]),
        "cap": f"{debt['cap'][0]}{debt['cap'][1]}",
        "window": "".join(map(str, debt["window"])),
        "majority/minority/third": (
            debt["majority"], debt["minority"], debt["third"]
        ),
        "core_fine": debt["core_fine"],
        "mate_fines": debt["mate_fines"],
        "tail": debt["tail_label"],
        "operation": debt["operation_label"],
    } for debt in debts))
    print("oriented naturality no-go", naturality)
    print("common residual escape identity", escape)
    print("minimal three-direct counterguard", counterguard)
    print("missing bridge: a word-changing typed response with complementary shores")


if __name__ == "__main__":
    main()
