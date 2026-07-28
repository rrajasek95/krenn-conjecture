#!/usr/bin/env python3
"""Independent certification layer for the round-1 four-extra-cell search.

Three separate exact verifications, all in rational arithmetic:

1. Cancellation witnesses.  For every one of the 10,611 cancellation
   families found by the census, substitute the recorded rational witness
   into Q = q + sum t_i e_i and expand z*Q^[3] literally in the square-zero
   algebra (all disjoint choices of one z cell and three distinct weighted
   cells, exact Fractions).  The result must equal Delta_{8,3} on the nose.
   This certifies constructively that every family really satisfies the
   polarized target identity at a nonzero parameter point, independently of
   the Laurent-debt bookkeeping.

2. Compatible quadruples.  For a deterministic sample of the 1,222,812
   identically compatible quadruples, the same expansion is checked at
   pseudorandom nonzero rational parameters, certifying the identical
   preservation of the identity on the sampled orbits.

3. Empty aggregate census, constructively.  The direct aggregate system
   (q + sum t_i e_i)^[4] = Delta_{8,3} needs, for each colour c, at least
   one Laurent monomial hitting the pure word c^8.  A matching term hits
   c^8 only if every participating cell is coloured (c,c), so objects of
   different colours share no cells; with only four extra cells the object
   sizes must be (1,1,1) with one free cell or (2,1,1).  The script derives
   from the aggregate debts that the only size-one objects are the three
   z cells and enumerates every size-two object, so the candidate list

       { z0,z1,z2,x : x any other cell }  union
       { pure-c pair object + the two other z cells }

   is provably complete.  Every candidate is then rejected by the exact
   support test (padding words 11000000 and 22212111 cannot be cancelled,
   or a hit word has a single Laurent monomial).  Together with the
   exhaustive C scan (search_n8_varied_q_round_1_exhaustive_scan.c), which
   reports zero aggregate support survivors among all 141,722,460
   quadruples, this proves by two independent routes that no four-cell
   variation of q at this seed satisfies the unrestricted aggregate system
   H_8(A) = Delta_{8,3} with nonzero coefficients.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
import os
import random

SITES = tuple(range(8))
COLOURS = (0, 1, 2)
EDGES = tuple(combinations(SITES, 2))
ALL_CELLS = tuple(
    (left, right, left_colour, right_colour)
    for left, right in EDGES
    for left_colour, right_colour in product(COLOURS, repeat=2)
)
BASE_Q = (
    (2, 3, 0, 0), (4, 5, 0, 0), (6, 7, 0, 0),
    (0, 1, 1, 1), (3, 6, 1, 1), (5, 7, 1, 1),
    (0, 2, 2, 2), (1, 4, 2, 2), (5, 6, 2, 2),
)
DISPLAYED_Z = ((0, 1, 0, 0), (2, 4, 1, 1), (3, 7, 2, 2))
PURE_WORDS = tuple((colour,) * 8 for colour in COLOURS)
PADDING_WORDS = ((1, 1, 0, 0, 0, 0, 0, 0), (2, 2, 2, 1, 2, 1, 1, 1))
EXTRAS = tuple(cell for cell in ALL_CELLS if cell not in BASE_Q)
DELTA = {word: Fraction(1) for word in PURE_WORDS}


def cells_are_disjoint(cells):
    endpoints = tuple(site for cell in cells for site in cell[:2])
    return len(endpoints) == len(set(endpoints))


def partial_word(cells):
    word = [-1] * 8
    for left, right, left_colour, right_colour in cells:
        word[left] = left_colour
        word[right] = right_colour
    return tuple(word)


def polarized_value(weighted):
    """z * Q^[3] for Q = sum coeff*cell, as an exact word dictionary."""
    result = {}
    for z_cell in DISPLAYED_Z:
        for chosen in combinations(weighted, 3):
            cells = (z_cell,) + tuple(cell for cell, _coeff in chosen)
            if not cells_are_disjoint(cells):
                continue
            coefficient = Fraction(1)
            for _cell, coeff in chosen:
                coefficient *= coeff
            word = partial_word(cells)
            result[word] = result.get(word, Fraction(0)) + coefficient
    return {word: value for word, value in result.items() if value}


def aggregate_value(weighted):
    """Q^[4], as an exact word dictionary."""
    result = {}
    for chosen in combinations(weighted, 4):
        cells = tuple(cell for cell, _coeff in chosen)
        if not cells_are_disjoint(cells):
            continue
        coefficient = Fraction(1)
        for _cell, coeff in chosen:
            coefficient *= coeff
        word = partial_word(cells)
        result[word] = result.get(word, Fraction(0)) + coefficient
    return {word: value for word, value in result.items() if value}


def weighted_source(quad_cells, parameters):
    return tuple((cell, Fraction(1)) for cell in BASE_Q) + tuple(
        (cell, parameter) for cell, parameter in zip(quad_cells, parameters)
    )


def aggregate_debt_rows(quad):
    """word -> set of Laurent-monomial masks of (q + sum t_i e_i)^[4]."""
    weighted = tuple((cell, 0) for cell in BASE_Q) + tuple(
        (EXTRAS[index], 1 << position) for position, index in enumerate(quad)
    )
    rows = {}
    for chosen in combinations(weighted, 4):
        cells = tuple(cell for cell, _tag in chosen)
        if not cells_are_disjoint(cells):
            continue
        tag = 0
        for _cell, item_tag in chosen:
            tag |= item_tag
        if tag == 0:
            continue
        rows.setdefault(partial_word(cells), set()).add(tag)
    return rows


def aggregate_support_test(quad):
    rows = aggregate_debt_rows(quad)
    for word in PURE_WORDS:
        if word not in rows:
            return "reject_pure_uncovered"
    for word in PADDING_WORDS:
        if word not in rows:
            return "reject_padding_uncancellable"
    for word, tags in rows.items():
        if word in DELTA or word in PADDING_WORDS:
            continue
        if len(tags) == 1:
            return "reject_singleton"
    return "aggregate_support_survivor"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scratch-dir",
        default=os.environ.get("N8_ROUND1_SCRATCH", "/tmp"),
    )
    parser.add_argument("--compatible-sample", type=int, default=2000)
    args = parser.parse_args()
    scratch = args.scratch_dir

    assert len(EXTRAS) == 243
    base = tuple((cell, Fraction(1)) for cell in BASE_Q)
    assert polarized_value(base) == DELTA

    # 1. Witness certification of every cancellation family.
    with open(os.path.join(scratch, "n8_round1_survivors_full.json")) as handle:
        records = json.load(handle)
    assert len(records) == 10_710
    checked = 0
    for record in records:
        if record["status"] != "cancellation_family":
            continue
        witness = tuple(Fraction(value) for value in record["witness"])
        assert all(witness)
        quad_cells = tuple(tuple(cell) for cell in record["cells"])
        assert all(cell not in BASE_Q for cell in quad_cells)
        value = polarized_value(weighted_source(quad_cells, witness))
        assert value == DELTA, (record["indices"], witness)
        checked += 1
    assert checked == 10_611
    print("cancellation families witness-certified:", checked)

    # 1b. Structure of the 99 torus-inconsistent support survivors: each is
    # the exceptional z triple extended by one compatible invisible cell,
    # and its system is t_a+t_b, t_b+t_c, t_a t_b+t_a t_c+t_b t_c in the
    # three z-cell parameters, which forces -t_b^2 = 0.
    inconsistent = [
        record for record in records if record["status"] == "torus_inconsistent"
    ]
    assert len(inconsistent) == 99
    z_cells = [list(cell) for cell in DISPLAYED_Z]
    for record in inconsistent:
        positions = [record["cells"].index(cell) for cell in z_cells]
        z_masks = sorted(1 << position for position in positions)
        pair_masks = sorted(
            z_masks[a] | z_masks[b] for a, b in combinations(range(3), 2)
        )
        system = sorted(
            tuple(sorted(equation["masks"])) for equation in record["system"]
        )
        assert system == sorted((
            (z_masks[0], z_masks[1]),
            (z_masks[1], z_masks[2]),
            tuple(pair_masks),
        )), record["indices"]
    print("torus-inconsistent survivors are the 99 z-triple extensions: PASS")

    # 2. Sampled certification of identically compatible quadruples.
    quads = []
    with open(os.path.join(scratch, "n8_round1_compatible_quads.txt")) as handle:
        for line in handle:
            quads.append(tuple(int(part) for part in line.split()))
    assert len(quads) == 1_222_812
    rng = random.Random(20260727)
    sample = rng.sample(quads, args.compatible_sample)
    for quad in sample:
        parameters = tuple(
            Fraction(rng.randint(1, 60), rng.randint(1, 60))
            * (1 if rng.random() < 0.5 else -1)
            for _ in range(4)
        )
        assert all(parameters)
        quad_cells = tuple(EXTRAS[index] for index in quad)
        value = polarized_value(weighted_source(quad_cells, parameters))
        assert value == DELTA, (quad, parameters)
    print("compatible quadruples certified at random parameters:", len(sample))

    # 3. Constructive emptiness of the aggregate census.
    z_set = set(DISPLAYED_Z)
    singles_by_colour = {colour: [] for colour in COLOURS}
    for index, cell in enumerate(EXTRAS):
        value = aggregate_value(base + ((cell, Fraction(1)),))
        for colour in COLOURS:
            if PURE_WORDS[colour] in value:
                singles_by_colour[colour].append(cell)
    for colour in COLOURS:
        assert singles_by_colour[colour] == [DISPLAYED_Z[colour]], colour
    print("size-one pure objects are exactly the z cells: PASS")

    pairs_by_colour = {colour: [] for colour in COLOURS}
    same_colour_cells = {
        colour: [cell for cell in EXTRAS if cell[2] == cell[3] == colour]
        for colour in COLOURS
    }
    for colour in COLOURS:
        for left, right in combinations(same_colour_cells[colour], 2):
            value = aggregate_value(
                base + ((left, Fraction(1)), (right, Fraction(1)))
            )
            if PURE_WORDS[colour] in value:
                pairs_by_colour[colour].append((left, right))
    pair_counts = {colour: len(pairs_by_colour[colour]) for colour in COLOURS}
    print("size-two pure objects by colour:", pair_counts)

    # A pure-word matching term forces every participating cell to carry the
    # pure colour at both endpoints, so pure objects of different colours are
    # cell-disjoint and the candidate list below is complete.
    for colour in COLOURS:
        for left, right in pairs_by_colour[colour]:
            assert left[2] == left[3] == colour and right[2] == right[3] == colour

    cell_index = {cell: position for position, cell in enumerate(EXTRAS)}
    candidates = set()
    z_indices = tuple(sorted(cell_index[cell] for cell in DISPLAYED_Z))
    for index in range(len(EXTRAS)):
        if index not in z_indices:
            candidates.add(tuple(sorted(z_indices + (index,))))
    for colour in COLOURS:
        others = tuple(
            cell_index[DISPLAYED_Z[other]] for other in COLOURS if other != colour
        )
        for left, right in pairs_by_colour[colour]:
            quad = tuple(sorted(
                (cell_index[left], cell_index[right]) + others
            ))
            assert len(set(quad)) == 4
            candidates.add(quad)
    print("complete aggregate candidate quadruples:", len(candidates))

    outcome = Counter(aggregate_support_test(quad) for quad in sorted(candidates))
    print("aggregate candidate outcomes:", dict(sorted(outcome.items())))
    assert outcome.get("aggregate_support_survivor", 0) == 0

    print("aggregate census constructively empty: PASS")


if __name__ == "__main__":
    main()
