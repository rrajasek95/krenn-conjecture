#!/usr/bin/env python3
"""Exact orbit/weight audit for holonomy H versus carrier 8x3 minors."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
from functools import lru_cache


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_holonomy_orbit_carrier_alignment.json"
TRIANGLE_AUDIT = (ROOT / "computations/unaudited-codex-triangle-crossword-observation-2026-08-22"
                  / "audit_triangle_crossword_observation.py")
STABILIZER_RESULT = (ROOT / "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22"
                     / "results_joint_semigroup_target_stabilizer.json")
PINS = {
    TRIANGLE_AUDIT: "b20e0eba85fbebc62ea089549349ce0724b71dee902359576ad9362906fe46b7",
    STABILIZER_RESULT: "ad94371c18d89ac767ecd3acc6ff8d28e40c3e752e8a4b8d31ce1f012dd8f828",
}

SITES = tuple(range(8))
COLOURS = tuple(range(3))
T_EDGES = ((0, 1), (0, 2), (1, 2))
SLICES = (
    (0, 1, 2, 1, 1, 2, 2, 2),
    (0, 1, 2, 0, 0, 0, 0, 0),
    (0, 1, 2, 1, 1, 1, 1, 1),
)
CONE = ((0, 1, 0, 0), (2, 3, 0, 0), (4, 5, 0, 0), (6, 7, 0, 0))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def load_triangle_audit():
    spec = importlib.util.spec_from_file_location("frozen_triangle_audit", TRIANGLE_AUDIT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_cell(u, v, a, b):
    return (u, v, a, b) if u < v else (v, u, b, a)


def transform_word(word, site_perm, colour_perm):
    out = [None] * 8
    for site, colour in enumerate(word):
        out[site_perm[site]] = colour_perm[colour]
    return tuple(out)


def transform_edge(edge, site_perm):
    return tuple(sorted((site_perm[edge[0]], site_perm[edge[1]])))


def transform_cell(cell, site_perm, colour_perm):
    u, v, a, b = cell
    return canonical_cell(site_perm[u], site_perm[v],
                          colour_perm[a], colour_perm[b])


def datum_key(words, edges):
    # Row and column reordering changes only the determinant sign.
    return tuple(sorted(words)), tuple(sorted(edges))


def fine_weight(words, edges):
    triangle = set(site for edge in edges for site in edge)
    require(len(triangle) == 3 and len(edges) == 3, (words, edges))
    out = []
    for site in SITES:
        if site in triangle:
            colours = {word[site] for word in words}
            require(len(colours) == 1, (site, words))
            row = [0, 0, 0]
            row[colours.pop()] = 1
        else:
            row = [sum(word[site] == colour for word in words)
                   for colour in COLOURS]
        out.append(tuple(row))
    require(sum(sum(row) for row in out) == 18, out)
    return tuple(out)


def orbit_audit():
    h_keys = set()
    h_weights = set()
    paired_keys = set()
    cone_to_h = defaultdict(set)
    h_to_cone = defaultdict(set)
    base_cone = tuple(CONE)
    for site_perm in permutations(SITES):
        edges = tuple(transform_edge(edge, site_perm) for edge in T_EDGES)
        for colour_perm in permutations(COLOURS):
            words = tuple(transform_word(word, site_perm, colour_perm)
                          for word in SLICES)
            h_key = datum_key(words, edges)
            h_keys.add(h_key)
            h_weights.add(fine_weight(words, edges))
            cone = tuple(sorted(transform_cell(cell, site_perm, colour_perm)
                                for cell in CONE))
            paired_keys.add((cone, h_key))
            cone_to_h[cone].add(h_key)
            h_to_cone[h_key].add(cone)

    group_order = 40320 * 6
    require(len(h_keys) == 20160, len(h_keys))
    require(len(h_weights) == len(h_keys), (len(h_weights), len(h_keys)))
    require(len(paired_keys) == 120960, len(paired_keys))
    require(len(cone_to_h) == 315, len(cone_to_h))
    require(set(map(len, cone_to_h.values())) == {384},
            Counter(map(len, cone_to_h.values())))
    require(set(map(len, h_to_cone.values())) == {6},
            Counter(map(len, h_to_cone.values())))
    require(len(cone_to_h[base_cone]) == 384, len(cone_to_h[base_cone]))
    return {
        "group_order": group_order,
        "unconed_orbit": len(h_keys),
        "unconed_datum_stabilizer": group_order // len(h_keys),
        "unconed_distinct_fine_weights": len(h_weights),
        "unconed_span_rank_from_distinct_weights": len(h_weights),
        "coned_pair_orbit": len(paired_keys),
        "coned_pair_stabilizer": group_order // len(paired_keys),
        "pure_cones": len(cone_to_h),
        "H_rows_on_one_live_cone_chart": len(cone_to_h[base_cone]),
        "cones_paired_with_each_H": next(iter(set(map(len, h_to_cone.values())))),
        "h_weights": h_weights,
    }


def cofactor_value(module, source, edge, word):
    total = Fraction(0)
    for matching in module.MATCHINGS:
        if edge not in matching:
            continue
        term = Fraction(1)
        for u, v in matching:
            if (u, v) == edge:
                continue
            term *= module.source_cell(source, u, v, word[u], word[v])
        total += term
    return total


def determinant3(rows):
    return (
        rows[0][0] * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1])
        - rows[0][1] * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0])
        + rows[0][2] * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0])
    )


def matrix_rank(rows):
    work = [[Fraction(value) for value in row] for row in rows]
    pivot = 0
    for column in range(len(work[0])):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        scale = work[pivot][column]
        work[pivot] = [value / scale for value in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [value - scale * base
                         for value, base in zip(work[row], work[pivot])]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def coned_pure_open_counterguard(module):
    """Literal source killing the complete coned orbit but not one minor."""
    cells = {}

    def put(u, v, a, b, value=Fraction(1)):
        if u > v:
            u, v, a, b = v, u, b, a
        cells[u, v, a, b] = Fraction(value)

    layers = (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 5), (6, 7)),
        ((0, 3), (1, 2), (4, 5), (6, 7)),
    )
    for colour, matching in enumerate(layers):
        for u, v in matching:
            put(u, v, colour, colour)
    # Three private cap-star paths make rows 01,11,21 of C_0 triangular.
    put(2, 6, 0, 0)
    put(1, 6, 0, 1)
    put(0, 6, 0, 2)
    put(3, 7, 0, 1)

    def cell_value(cell):
        u, v, a, b = cell
        if u > v:
            u, v, a, b = v, u, b, a
        return cells.get((u, v, a, b), Fraction(0))

    @lru_cache(None)
    def cofactor(edge, word):
        total = Fraction(0)
        for matching in module.MATCHINGS:
            if edge not in matching:
                continue
            term = Fraction(1)
            for selected in matching:
                if selected == edge:
                    continue
                u, v = selected
                term *= cell_value((u, v, word[u], word[v]))
            total += term
        return total

    seen_pairs = set()
    live_cones = set()
    live_pair_evaluations = 0
    nonzero_coned_values = 0
    for site_perm in permutations(SITES):
        edges = tuple(transform_edge(edge, site_perm) for edge in T_EDGES)
        for colour_perm in permutations(COLOURS):
            words = tuple(transform_word(word, site_perm, colour_perm)
                          for word in SLICES)
            h_key = datum_key(words, edges)
            cone = tuple(sorted(transform_cell(cell, site_perm, colour_perm)
                                for cell in CONE))
            pair_key = cone, h_key
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)
            cone_value = Fraction(1)
            for cell in cone:
                cone_value *= cell_value(cell)
            if not cone_value:
                continue
            live_cones.add(cone)
            live_pair_evaluations += 1
            h_value = determinant3(tuple(
                tuple(cofactor(edge, word) for edge in edges)
                for word in words
            ))
            nonzero_coned_values += bool(cone_value * h_value)

    require(len(seen_pairs) == 120960, len(seen_pairs))
    require(len(live_cones) == 3, live_cones)
    require(live_pair_evaluations == 3 * 384, live_pair_evaluations)
    require(nonzero_coned_values == 0, nonzero_coned_values)

    pure_amplitudes = []
    for colour in COLOURS:
        word = (colour,) * 8
        amplitude = Fraction(0)
        for matching in module.MATCHINGS:
            term = Fraction(1)
            for u, v in matching:
                term *= cell_value((u, v, colour, colour))
            amplitude += term
        pure_amplitudes.append(amplitude)
    require(pure_amplitudes == [1, 1, 1], pure_amplitudes)
    mixed_nonzero = 0
    mixed_value_histogram = Counter()
    for word in product(COLOURS, repeat=8):
        if word in ((0,) * 8, (1,) * 8, (2,) * 8):
            continue
        amplitude = Fraction(0)
        for matching in module.MATCHINGS:
            term = Fraction(1)
            for u, v in matching:
                term *= cell_value((u, v, word[u], word[v]))
            amplitude += term
        if amplitude:
            mixed_nonzero += 1
            mixed_value_histogram[str(amplitude)] += 1

    pure_cofactors = [cofactor((6, 7), (colour,) * 8)
                      for colour in COLOURS]
    require(pure_cofactors == [1, 1, 1], pure_cofactors)
    carrier = []
    mixed_pairs = tuple(pair for pair in product(COLOURS, repeat=2)
                        if pair != (0, 0))
    for i, j in mixed_pairs:
        word = (0,) * 6 + (i, j)
        carrier.append(tuple(cofactor(edge, word) for edge in T_EDGES))
    rank = matrix_rank(carrier)
    selected_pairs = ((0, 1), (1, 1), (2, 1))
    selected_rows = tuple(carrier[mixed_pairs.index(pair)]
                          for pair in selected_pairs)
    selected_minor = determinant3(selected_rows)
    require(rank == 3 and selected_minor == 1,
            (carrier, rank, selected_minor))

    source_cells = [list(label) + [str(value)]
                    for label, value in sorted(cells.items())]
    return {
        "source_cells": source_cells,
        "source_cell_count": len(source_cells),
        "pure_amplitudes": [str(value) for value in pure_amplitudes],
        "mixed_nonzero_amplitudes": mixed_nonzero,
        "mixed_nonzero_value_histogram": dict(sorted(mixed_value_histogram.items())),
        "pure_cofactors_P0_P1_P2": [str(value) for value in pure_cofactors],
        "pure_cofactor_product_D": str(
            pure_cofactors[0] * pure_cofactors[1] * pure_cofactors[2]),
        "nonzero_pure_cones": len(live_cones),
        "coned_orbit_polynomials_checked": len(seen_pairs),
        "live_cone_H_evaluations_checked": live_pair_evaluations,
        "nonzero_coned_orbit_values": nonzero_coned_values,
        "canonical_C0_rows_in_mixed_pair_order": [
            {"pair": f"{pair[0]}{pair[1]}",
             "row": [str(value) for value in row]}
            for pair, row in zip(mixed_pairs, carrier)
        ],
        "canonical_C0_rank": rank,
        "selected_minor_pairs": [f"{i}{j}" for i, j in selected_pairs],
        "selected_minor_value": str(selected_minor),
        "scope": (
            "Literal rational source with pure amplitudes normalized and D=1. "
            "It is not a full-X5 point; it proves only that the coned holonomy "
            "orbit ideal (even with pure normalization and D inverted) does not "
            "force carrier rank at most two."
        ),
    }


def carrier_audit(module, h_weights):
    source = module.dense_rational_source(1)
    carrier_weights = []
    determinants = []
    by_colour = []
    for colour in COLOURS:
        rows = {}
        for i, j in product(COLOURS, repeat=2):
            word = (colour,) * 6 + (i, j)
            rows[i, j] = tuple(cofactor_value(module, source, edge, word)
                               for edge in T_EDGES)
        mixed = tuple(pair for pair in product(COLOURS, repeat=2)
                      if pair != (colour, colour))
        colour_determinants = []
        for triple in combinations(mixed, 3):
            words = tuple((colour,) * 6 + pair for pair in triple)
            weight = fine_weight(words, T_EDGES)
            carrier_weights.append(weight)
            value = determinant3(tuple(rows[pair] for pair in triple))
            colour_determinants.append(value)
            determinants.append(value)
        require(len(colour_determinants) == 56
                and all(colour_determinants), (colour, colour_determinants))
        by_colour.append({
            "colour": colour,
            "min_abs_dense_witness_minor": str(min(map(abs, colour_determinants))),
            "max_abs_dense_witness_minor": str(max(map(abs, colour_determinants))),
            "nonzero_dense_witness_minors": sum(bool(x) for x in colour_determinants),
        })

    carrier_weight_set = set(carrier_weights)
    require(len(carrier_weights) == 168, len(carrier_weights))
    require(len(carrier_weight_set) == 123, len(carrier_weight_set))
    require(not (carrier_weight_set & h_weights),
            carrier_weight_set & h_weights)

    # The open product D=P0 P1 P2 has one port of every colour at residual
    # sites 0,...,5 and none at cap sites 6,7.  At the first saturation layer
    # the elementary componentwise weight obstruction already disappears.
    d_weight = tuple((1, 1, 1) if site < 6 else (0, 0, 0)
                     for site in SITES)
    candidate_counts = []
    for weight in carrier_weights:
        target = tuple(tuple(weight[site][colour] + d_weight[site][colour]
                             for colour in COLOURS)
                       for site in SITES)
        candidates = sum(all(
            h_weight[site][colour] <= target[site][colour]
            for site in SITES for colour in COLOURS
        ) for h_weight in h_weights)
        require(candidates, (weight, target))
        candidate_counts.append(candidates)

    pure_cofactors = []
    for colour in COLOURS:
        word = (colour,) * 8
        value = cofactor_value(module, source, (6, 7), word)
        require(value, (colour, value))
        pure_cofactors.append(value)

    det_digest = sha256(json.dumps(
        [str(value) for value in determinants], separators=(",", ":")
    ).encode()).hexdigest()
    return {
        "carrier_minors_per_colour": 56,
        "carrier_minors_all_colours": len(carrier_weights),
        "carrier_distinct_fine_weights": len(carrier_weight_set),
        "intersection_with_H_weights": 0,
        "all_carrier_minors_nonzero_as_polynomials": True,
        "dense_exact_source_seed": 1,
        "dense_exact_pure_cofactors_67": [str(value) for value in pure_cofactors],
        "dense_exact_minor_digest": det_digest,
        "by_colour": by_colour,
        "first_D_saturation_candidate_H_weights": {
            "minimum": min(candidate_counts),
            "maximum": max(candidate_counts),
            "histogram": {str(key): value
                          for key, value in sorted(Counter(candidate_counts).items())},
        },
    }


def base_h_witness(module):
    source = module.dense_rational_source(1)
    rows = tuple(tuple(cofactor_value(module, source, edge, word)
                       for edge in T_EDGES) for word in SLICES)
    value = determinant3(rows)
    require(value, value)
    return str(value)


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-carrier-colour", action="store_true")
    args = parser.parse_args()
    pins = {}
    for path, expected in PINS.items():
        actual = file_sha(path)
        require(actual == expected, (str(path), actual, expected))
        pins[str(path.relative_to(ROOT))] = actual
    frozen_stabilizer = json.loads(STABILIZER_RESULT.read_text())
    require(frozen_stabilizer["literal_target_stabilizer_order"] == 2,
            frozen_stabilizer)
    module = load_triangle_audit()
    orbit = orbit_audit()
    h_weights = orbit.pop("h_weights")
    carrier = carrier_audit(module, h_weights)
    counterguard = coned_pure_open_counterguard(module)
    if args.mutate_carrier_colour:
        carrier["intersection_with_H_weights"] = 1
    require(carrier["intersection_with_H_weights"] == 0, carrier)
    payload = {
        "status": "PASS exact H-orbit nonmembership and pure-open coned counterguard",
        "pins": pins,
        "selected_H_dense_exact_value": base_h_witness(module),
        "orbit": orbit,
        "carrier": carrier,
        "pure_open_coned_counterguard": counterguard,
        "theorem": (
            "The unconed S8xS3 orbit of H has 20160 nonzero polynomials in "
            "20160 distinct site-colour fine degrees, hence exact span rank 20160. "
            "Every carrier minor has the three degree-one triangle ports in one "
            "common colour, whereas every orbit H has them in three distinct "
            "colours. Thus all 168 carrier minors, including the fixed 56, lie "
            "outside the orbit span and outside its unlocalized degree-nine ideal."
        ),
        "coned_scope_guard": (
            "The literal orbit of M*H has 120960 pairs over 315 pure cones. "
            "On one nonzero cone chart it yields only 384 unconed H equations, "
            "not all 20160. Pure normalization guarantees some cone is live but "
            "does not make all paired cones live."
        ),
        "localized_scope_guard": (
            "The literal 16-cell counterguard has pure amplitudes (1,1,1), "
            "P0=P1=P2=1, annihilates all 120960 coned orbit polynomials, and has "
            "canonical carrier rank three with minor Delta_(01,11,21)=1. Thus "
            "even pure-cofactor localization does not make the coned orbit ideal "
            "force carrier rank. Full X5 rows beyond the coned identities remain "
            "load-bearing. For the artificially stronger unconed all-H ideal, "
            "localization is a separate unresolved saturation problem."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        HERE.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("orbit", orbit)
    print("carrier weight intersection", carrier["intersection_with_H_weights"])
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
