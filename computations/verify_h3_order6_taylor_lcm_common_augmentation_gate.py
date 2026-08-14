#!/usr/bin/env python3
"""Classify the rank-77 response complement as Taylor versus divided faces.

The ordinary Taylor resolution on the 180 labelled matching occurrences has
one degree-two cell for each pair of occurrence parents, with squarefree lcm.
An off-diagonal coloured-cell pair can occur in such an lcm.  A diagonal
pair (a,a), however, asks for the second divided derivative in one cell; the
squarefree lcm contains a only once and its ordinary second Hasse face is
zero.  Such rows require a divided-power/Tate diagonal enlargement.

This checker reconstructs the fixed rank-153 response image at the first
pinned prime, its rank-76 seed subspace, and the canonical 77-pivot quotient.
It tests every full and quotient pivot against the literal 180 occurrence
parents, then records the smallest common Taylor--Spencer augmentation module
suggested by the calculation.  The cap augmentation remains a typed open map.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order6_seed_source_automorphism_orbit_gate.py":
        "d140995b0b35b84f052662595a0a68bcd2b47db826d8e559bb99a96b0eb9b61e",
    "computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py":
        "0c3367ab48327bfbe308dc81191019d094eec054a04c3d1f2bd38f0e69faa2e9",
    "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py":
        "f1bc7a9f8fdb9148fde5c4d79a4b7f59a3bd03cd6ff00dc1c2fb3c0e7f511ea9",
}
EXPECTED_LEDGER_SHA256 = "9f7c1d2949410714ed0e4ebaf0c2056bd74d832ed020f8f047b328ecaddfe50d"

PURE_WORD = (1,) * 8
MIXED_WORD = (1, 1, 2, 1, 1, 2, 1, 1)
FIRST_ROW = (2, ((0, 1, 1, 1), (0, 7, 1, 1)))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        require(expected != "TO_BE_PINNED", ("unfrozen pin", relative))
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank_vectors(site, vectors, prime):
    basis = {}
    for vector in vectors:
        site.insert(dict(vector), basis, prime)
    return len(basis)


def projected_bases_by_shift(site, columns, shifts, direct_free_pair, prime):
    grouped = defaultdict(list)
    shift_values = {}
    for column, shift in zip(columns, shifts, strict=True):
        key = repr(shift)
        grouped[key].append(column)
        shift_values[key] = shift
    constrained_all = []
    by_shift = {}
    for key in sorted(grouped):
        lower_basis = {}
        constrained = []
        for column in grouped[key]:
            added, pivot = site.insert(dict(column), lower_basis, prime)
            if added and pivot[0] == 2:
                require(all(row[0] == 2 for row in lower_basis[pivot]),
                        ("constrained vector retained a lower row", pivot))
                constrained.append(lower_basis[pivot])
                constrained_all.append(lower_basis[pivot])
        shadow_basis = {}
        for vector in constrained:
            site.insert(dict(vector), shadow_basis, prime)
        projected = {}
        hit = set()
        for vector in shadow_basis.values():
            nonphysical = {
                row: value for row, value in vector.items()
                if not site.physical_pair(row[1], direct_free_pair)
            }
            hit.update(nonphysical)
            site.insert(nonphysical, projected, prime)
        by_shift[key] = {
            "shift": shift_values[key],
            "shadow_basis": shadow_basis,
            "projected_basis": projected,
            "hit": hit,
        }
    aggregate_shadow = {}
    for vector in constrained_all:
        site.insert(dict(vector), aggregate_shadow, prime)
    aggregate_projected = {}
    aggregate_hit = set()
    for vector in aggregate_shadow.values():
        nonphysical = {
            row: value for row, value in vector.items()
            if not site.physical_pair(row[1], direct_free_pair)
        }
        aggregate_hit.update(nonphysical)
        site.insert(nonphysical, aggregate_projected, prime)
    return aggregate_projected, aggregate_hit, len(aggregate_shadow), by_shift


def canonical_complement(site, seed_basis, full_basis, prime):
    combined = {}
    for vector in seed_basis.values():
        site.insert(dict(vector), combined, prime)
    pivots = []
    vectors = []
    for pivot in sorted(full_basis, key=repr):
        added, new_pivot = site.insert(dict(full_basis[pivot]), combined, prime)
        if added:
            pivots.append(new_pivot)
            vectors.append(combined[new_pivot])
    require(len(seed_basis) == 76 and len(pivots) == 77
            and len(combined) == 153,
            (len(seed_basis), len(pivots), len(combined)))
    return tuple(pivots), tuple(vectors)


def occurrence_parents(base):
    answer = []
    for word_name, word in (("pure", PURE_WORD), ("mixed", MIXED_WORD)):
        for index, monomial in enumerate(base.full_row(word)):
            answer.append((word_name, index, frozenset(monomial)))
    require(len(answer) == 180, len(answer))
    return tuple(answer)


def parent_indices_by_cell(parents):
    result = defaultdict(list)
    for index, (_word, _number, monomial) in enumerate(parents):
        for cell in monomial:
            result[cell].append(index)
    return result


def lcm_graph_topology(left_monomial, right_monomial):
    left_edges = {frozenset(cell[:2]) for cell in left_monomial}
    right_edges = {frozenset(cell[:2]) for cell in right_monomial}
    common = left_edges & right_edges
    symmetric = left_edges ^ right_edges
    adjacency = defaultdict(set)
    for edge in symmetric:
        a, b = tuple(edge)
        adjacency[a].add(b)
        adjacency[b].add(a)
    cycles = []
    unseen = set(adjacency)
    while unseen:
        start = min(unseen)
        stack = [start]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex] - component)
        unseen -= component
        require(all(len(adjacency[vertex]) == 2 for vertex in component),
                ("matching symmetric difference stopped being cycles",
                 left_edges, right_edges, component))
        cycles.append(len(component))
    parts = ["K2"] * len(common) + [f"C{size}" for size in sorted(cycles)]
    return "+".join(parts) if parts else "identical"


def pair_taylor_record(pair, parents, by_cell):
    left, right = pair
    diagonal = left == right
    candidates = []
    for left_parent in by_cell[left]:
        for right_parent in by_cell[right]:
            if left_parent == right_parent:
                continue
            left_word, _left_number, left_monomial = parents[left_parent]
            right_word, _right_number, right_monomial = parents[right_parent]
            lcm = left_monomial | right_monomial
            candidates.append((len(lcm), left_word + "/" + right_word,
                               lcm_graph_topology(left_monomial,
                                                  right_monomial),
                               left_parent, right_parent, lcm))
    require(candidates, ("pair has no two matching parents", pair))
    minimum = min(candidates, key=lambda item: (item[0], item[1],
                                                item[2], item[3], item[4]))
    lcm_multiplicity = int(left in minimum[5])
    ordinary_second_face = (not diagonal and left in minimum[5]
                            and right in minimum[5])
    return {
        "diagonal_decorated_pair": diagonal,
        "two_parent_realisations": len(candidates),
        "minimum_lcm_cell_degree": minimum[0],
        "minimum_parent_word_type": minimum[1],
        "minimum_lcm_graph_topology": minimum[2],
        "ordinary_squarefree_taylor_second_face": ordinary_second_face,
        "cell_multiplicity_in_lcm_if_diagonal": (
            lcm_multiplicity if diagonal else None
        ),
        "requires_divided_power_diagonal": diagonal,
    }


def classify_rows(rows, parents, by_cell, shift_support):
    records = {row: pair_taylor_record(row[1], parents, by_cell)
               for row in rows}
    for row, record in records.items():
        record["coordinate_word_fine_shift_support"] = shift_support[row]
    histograms = {
        "diagonal_vs_offdiagonal": Counter(
            "diagonal" if record["diagonal_decorated_pair"] else "offdiagonal"
            for record in records.values()),
        "minimum_lcm_cell_degree": Counter(
            str(record["minimum_lcm_cell_degree"])
            for record in records.values()),
        "minimum_parent_word_type": Counter(
            record["minimum_parent_word_type"]
            for record in records.values()),
        "minimum_lcm_graph_topology": Counter(
            record["minimum_lcm_graph_topology"]
            for record in records.values()),
        "coordinate_word_fine_shift_support": Counter(
            record["coordinate_word_fine_shift_support"]
            for record in records.values()),
        "ordinary_vs_divided": Counter(
            "ordinary_Taylor" if record[
                "ordinary_squarefree_taylor_second_face"]
            else "divided_diagonal"
            for record in records.values()),
    }
    return records, {name: dict(sorted(histogram.items()))
                     for name, histogram in histograms.items()}


def projected_rank_by_pair_kind(site, basis, prime):
    offdiagonal = []
    diagonal = []
    for vector in basis.values():
        offdiagonal.append({row: value for row, value in vector.items()
                            if row[1][0] != row[1][1]})
        diagonal.append({row: value for row, value in vector.items()
                         if row[1][0] == row[1][1]})
    return {
        "offdiagonal_projection_rank": rank_vectors(site, offdiagonal, prime),
        "diagonal_projection_rank": rank_vectors(site, diagonal, prime),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    orbit = load(
        "computations/verify_h3_order6_seed_source_automorphism_orbit_gate.py",
        "taylor_lcm_orbit",
    )
    site = load(
        "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py",
        "taylor_lcm_site",
    )
    loaded = site.modules()
    columns, shifts = site.build_operator_columns(loaded)
    prime = site.PRIMES[0]
    direct_free_pair = loaded["base"].DIRECT_FREE_PAIR
    full_basis, full_hit, full_shadow_rank, full_by_shift = (
        projected_bases_by_shift(
            site, columns, shifts, direct_free_pair, prime)
    )
    seed_indices = tuple(index for index, column in enumerate(columns)
                         if column.get(FIRST_ROW))
    seed_basis, seed_hit, seed_shadow_rank, seed_by_shift = projected_bases_by_shift(
        site,
        [columns[index] for index in seed_indices],
        [shifts[index] for index in seed_indices],
        direct_free_pair,
        prime,
    )
    require((full_shadow_rank, len(full_hit), len(full_basis))
            == (488, 159, 153)
            and (seed_shadow_rank, len(seed_hit), len(seed_basis))
            == (178, 84, 76),
            (full_shadow_rank, len(full_hit), len(full_basis),
             seed_shadow_rank, len(seed_hit), len(seed_basis)))
    complement_pivots, complement_vectors = canonical_complement(
        site, seed_basis, full_basis, prime)

    parents = occurrence_parents(loaded["base"])
    by_cell = parent_indices_by_cell(parents)
    require(len(full_by_shift) == len(seed_by_shift) == 2,
            (full_by_shift.keys(), seed_by_shift.keys()))

    def shift_name(shift):
        word = []
        for site_index in range(8):
            block = shift[3 * site_index:3 * site_index + 3]
            require(block.count(-1) == 1 and block.count(0) == 2,
                    (site_index, block))
            word.append(str(block.index(-1)))
        return "".join(word)

    shift_hits = {
        shift_name(record["shift"]): record["hit"]
        for record in full_by_shift.values()
    }
    require(set(shift_hits) == {"11111111", "11211211"}, shift_hits)

    def coordinate_shift_support(row):
        names = [name for name, hit in sorted(shift_hits.items()) if row in hit]
        require(names, ("coordinate absent from both shifts", row))
        return "+".join(names)

    shift_support = {row: coordinate_shift_support(row) for row in full_hit}
    _full_records, full_histograms = classify_rows(
        tuple(sorted(full_hit, key=repr)), parents, by_cell, shift_support)
    complement_records, complement_histograms = classify_rows(
        complement_pivots, parents, by_cell, shift_support)

    full_kind_ranks = projected_rank_by_pair_kind(site, full_basis, prime)
    seed_kind_ranks = projected_rank_by_pair_kind(site, seed_basis, prime)
    complement_kind_ranks = {
        "offdiagonal_projection_rank": rank_vectors(site, (
            {row: value for row, value in vector.items()
             if row[1][0] != row[1][1]}
            for vector in complement_vectors
        ), prime),
        "diagonal_projection_rank": rank_vectors(site, (
            {row: value for row, value in vector.items()
             if row[1][0] == row[1][1]}
            for vector in complement_vectors
        ), prime),
    }

    diagonal_complement = [row for row in complement_pivots
                           if row[1][0] == row[1][1]]
    offdiagonal_complement = [row for row in complement_pivots
                              if row[1][0] != row[1][1]]
    require(all(complement_records[row][
                    "ordinary_squarefree_taylor_second_face"]
                for row in offdiagonal_complement)
            and all(complement_records[row][
                    "requires_divided_power_diagonal"]
                and complement_records[row][
                    "cell_multiplicity_in_lcm_if_diagonal"] == 1
                for row in diagonal_complement),
            "Taylor/divided classification changed")

    ledger = {
        "theorem": "h3 order-six Taylor-lcm common augmentation gate",
        "pins": PINS,
        "prime": prime,
        "response_occurrence_parents": {
            "pure": 90,
            "mixed": 90,
            "total": len(parents),
        },
        "fixed_response_image": {
            "full_coordinate_support_rank": [len(full_hit), len(full_basis)],
            "seed_coordinate_support_rank": [len(seed_hit), len(seed_basis)],
            "canonical_complement_pivots": len(complement_pivots),
            "full_pair_kind_ranks": full_kind_ranks,
            "seed_pair_kind_ranks": seed_kind_ranks,
            "complement_pair_kind_ranks": complement_kind_ranks,
        },
        "full159_taylor_classification": full_histograms,
        "complement77_taylor_classification": complement_histograms,
        "complement_pivot_digest": sha256(json.dumps(
            [repr(row) for row in complement_pivots],
            separators=(",", ":"),
        ).encode()).hexdigest(),
        "diagonal_complement_rows": [repr(row)
                                     for row in diagonal_complement],
        "first_ten_offdiagonal_complement_rows": [
            repr(row) for row in offdiagonal_complement[:10]
        ],
        "ordinary_Taylor_test": {
            "every_offdiagonal_full_row_has_two_matching_parents": True,
            "ordinary_lcm_is_squarefree_in_decorated_cells": True,
            "diagonal_pair_second_face_in_ordinary_lcm": 0,
            "consequence": (
                "ordinary degree-two Taylor cells cover the offdiagonal "
                "pair labels but cannot represent (a,a) divided-Hasse rows"
            ),
        },
        "seed_transport_test": {
            "internal_seed_naturality_rank": 76,
            "full_response_rank": 153,
            "remaining_rank": 77,
            "two_seed_types_generate_all_relative_Taylor_syzygies": False,
            "reason": (
                "their committed internal word/fine orbit has rank 76; the "
                "complement contains additional offdiagonal Taylor pivots "
                "and diagonal divided-power pivots"
            ),
        },
        "smallest_common_response_augmentation_module": {
            "name": "DivTaylorSpencer_rep",
            "offdiagonal_part": (
                "ordinary degree-two Taylor lcm cells on the 180 labelled "
                "pure/mixed matching parents"
            ),
            "diagonal_part": (
                "divided-power gamma_2(iota_a) cells for every diagonal "
                "pair used by the constrained response image"
            ),
            "fixed_image_quotient": (
                "take the source-derived rank-153 constrained image, with "
                "the frozen rank-76 seed submodule and rank-77 complement"
            ),
            "response_augmentation": (
                "Taylor boundary to the two occurrence parents plus the "
                "literal Spencer D0/D1/D2 faces"
            ),
            "cap_P3K2_AugP2_augmentation_constructed": False,
            "missing_cap_map": (
                "a word/fine/repeated-labelled dg-bimodule augmentation "
                "DivTaylorSpencer_rep -> C_AugP2 carrying the selected "
                "P3+K2 faces and r0/E incidence"
            ),
        },
        "verdict": (
            "The rank-77 complement is not an ordinary Taylor family alone. "
            "Every offdiagonal pivot is realized by a degree-two lcm of two "
            "literal matching parents, but diagonal (a,a) pivots have only "
            "one copy of a in the squarefree lcm and require divided-power "
            "Tate cells.  The two first-face seed types retain rank 76 under "
            "legal full-word transport and do not generate the complement. "
            "The smallest common response object is therefore a divided "
            "Taylor--Spencer module.  Its augmentation to the P3+K2/AugP2 "
            "cap, including the response-to-cap operation idempotent, remains open"
        ),
        "scope": (
            "one-prime reconstruction at 1000003 of the already two-prime-"
            "stable complement pivot set, followed by exact combinatorial "
            "parent/lcm tests on all 180 literal occurrences.  It does not "
            "promote modular ranks to Q or construct the cap augmentation"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Taylor-lcm ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("full", "structural"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    if arguments.mode == "structural":
        pin_dependencies()
        print("h3 order-six Taylor-lcm structural gate: PASS")
        return
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        print("h3 order-six Taylor-lcm common augmentation gate: PASS")
        print("full", ledger["full159_taylor_classification"])
        print("complement", ledger["complement77_taylor_classification"])
        print("kind ranks", ledger["fixed_response_image"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
