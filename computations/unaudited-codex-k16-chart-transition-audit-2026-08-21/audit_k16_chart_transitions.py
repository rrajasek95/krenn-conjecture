#!/usr/bin/env python3
"""Literal-support chart transitions for the orbit-zero K16 singleton tail."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import ast
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K16_DIR = ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
K14_PATH = K16_DIR / "audit_orbit0_k14_interface.py"
COVER_PATH = K16_DIR / "results_k16_anchor_cover.json"
CHART_PATH = ROOT / "computations/verify_n8_target_triple_localization_orbits.py"
OUT = HERE / "results_k16_chart_transitions.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


K14 = load("k14_transition", K14_PATH)
F = K14.FROZEN
CHARTS = load("n8_charts_transition", CHART_PATH)
SOURCE = CHARTS.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def divides(row, divisor):
    multiplicity = Counter(row)
    return all(multiplicity[cell] >= count
               for cell, count in Counter(divisor).items())


def subtract(row, divisor):
    multiplicity = Counter(row)
    multiplicity.subtract(divisor)
    require(all(value >= 0 for value in multiplicity.values()), "nondivisor")
    return bytes(sorted(cell for cell, value in multiplicity.items()
                        for _ in range(value)))


def build():
    cover = json.loads(COVER_PATH.read_text())
    selected_signatures = frozenset(
        ast.literal_eval(row) for row in
        cover["single_pivot_cover"]["minimum_cover_orbit_representatives"]
    )
    require(len(selected_signatures) == 25, len(selected_signatures))

    raw = json.loads(F.R8P.read_text())
    residual = tuple(bytes.fromhex(row) for row, _n, _d in raw["residual"])
    words3 = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    three_anchors = tuple(F.BASE.term_ids(word, F.M0) for word in words3)
    errors = tuple(Counter({term: 1 for term in F.BASE.word_terms(word)
                            if term != anchor and F.row_k_degree(term) == 2})
                   for word, anchor in zip(words3, three_anchors, strict=True))
    packet = F.polynomial_product(F.polynomial_product(errors[0], errors[1]), errors[2])
    factor_set = frozenset(three_anchors)
    stabilizer = tuple(action for action in range(len(F.EXPORT.STABILIZER))
                       if frozenset(F.move_row(term, action) for term in three_anchors)
                       == factor_set)
    require(len(stabilizer) == 384, len(stabilizer))
    h_representatives = []
    for representative in residual:
        unseen = set(F.EXPORT.row_orbit(representative))
        while unseen:
            seed = min(unseen)
            orbit = F.orbit_under(seed, stabilizer)
            h_representatives.append(seed)
            unseen.difference_update(orbit)
    require(len(h_representatives) == 485, len(h_representatives))

    anchor_cells = tuple(sorted(F.A))
    anchor_position = {cell: index for index, cell in enumerate(anchor_cells)}
    mixed_anchor_terms = []
    mixed_vectors = []
    mixed_tails = []
    for colours in product(range(3), repeat=4):
        if len(set(colours)) == 1:
            continue
        word = F.word_from_pair_colours(colours)
        anchor = F.BASE.term_ids(word, F.M0)
        mixed_anchor_terms.append(anchor)
        mixed_vectors.append(tuple(Counter(anchor)[cell] for cell in anchor_cells))
        mixed_tails.append(tuple(term for term in F.BASE.word_terms(word)
                                 if F.row_k_degree(term) == 2))
    require(len(mixed_anchor_terms) == 78, len(mixed_anchor_terms))
    pivot_cache = {}

    def pivots(signature):
        if signature not in pivot_cache:
            pivot_cache[signature] = tuple(
                index for index, vector in enumerate(mixed_vectors)
                if all(a >= b for a, b in zip(signature, vector, strict=True))
            )
        return pivot_cache[signature]

    permutations = []
    for action in stabilizer:
        transform = F.EXPORT.TRANSFORMS[action]
        permutations.append(tuple(anchor_position[transform[cell]]
                                  for cell in anchor_cells))

    canonical_cache = {}

    def canonical_signature(signature):
        if signature not in canonical_cache:
            images = []
            for permutation in permutations:
                moved = [0] * 12
                for old, new in enumerate(permutation):
                    moved[new] = signature[old]
                images.append(tuple(moved))
            canonical_cache[signature] = min(images)
        return canonical_cache[signature]

    def anchor_signature(row):
        count = Counter(row)
        return tuple(count[cell] for cell in anchor_cells)

    # All 31 chart types and the exact orbit-zero product.
    chart_rows = tuple(sorted(SOURCE.target_orbit_rows()))
    chart_index = {row: index + 1 for index, row in enumerate(chart_rows)}
    require(len(chart_rows) == 31, len(chart_rows))
    vertex_matchings = tuple(F.BASE.perfect_matchings(tuple(range(8))))
    physical_edges = tuple(combinations(range(8), 2))
    physical_edge_index = {edge: index for index, edge in enumerate(physical_edges)}
    matching_masks = []
    matching_cells = {colour: [] for colour in range(3)}
    for matching in vertex_matchings:
        mask = 0
        for u, v in matching:
            mask |= 1 << physical_edge_index[(u, v)]
        matching_masks.append(mask)
        for colour in range(3):
            matching_cells[colour].append(frozenset(
                F.BASE.CELL_ID[(u, v, colour, colour)] for u, v in matching
            ))
    source_anchor_set = frozenset(F.A)
    source_matching = tuple(F.M0)
    source_key = SOURCE.canonical_key(SOURCE.row_from_matching_triple(
        (source_matching, source_matching, source_matching)))
    source_chart = chart_index[source_key]

    transition_cache = {}

    def destinations(row):
        pure_masks = [0, 0, 0]
        support = frozenset(row)
        for cell in support:
            u, v, a, b = F.BASE.CELLS[cell]
            if a == b:
                pure_masks[a] |= 1 << physical_edge_index[(u, v)]
        cache_key = tuple(pure_masks)
        if cache_key in transition_cache:
            return transition_cache[cache_key]
        supported = [tuple(index for index, mask in enumerate(matching_masks)
                           if mask & ~pure_masks[colour] == 0)
                     for colour in range(3)]
        output = set()
        for indices in product(*supported):
            triple = tuple(vertex_matchings[index] for index in indices)
            key = SOURCE.canonical_key(SOURCE.row_from_matching_triple(triple))
            destination = chart_index[key]
            destination_cells = frozenset().union(*(
                matching_cells[colour][indices[colour]] for colour in range(3)
            ))
            require(len(destination_cells) == 12 and destination_cells <= support,
                    (destination, destination_cells - support))
            overlap = len(destination_cells & source_anchor_set)
            positive = tuple(sorted(destination_cells - source_anchor_set))
            negative = tuple(sorted(source_anchor_set - destination_cells))
            require(len(positive) == len(negative) == 12 - overlap,
                    (overlap, positive, negative))
            output.add((destination, overlap, positive, negative))
        answer = tuple(sorted(output))
        transition_cache[cache_key] = answer
        return answer

    # Choose, for every literal K14 anchor signature, the lex-first pivot
    # whose survivor tail-orbits lie in the exact 25-orbit minimum single-pivot
    # cover. This reconstructs a literal K16 packet; it is distinct from the
    # 25-orbit affine relaxation and from the earlier locally-minimal 50-orbit
    # packet.
    chosen_pivot = {}
    for r8 in h_representatives:
        for packet_row in packet:
            target = bytes(sorted(r8 + packet_row))
            signature = anchor_signature(target)
            if signature in chosen_pivot:
                continue
            candidates = []
            for pivot in pivots(signature):
                base_vector = tuple(a - b for a, b
                                    in zip(signature, mixed_vectors[pivot], strict=True))
                survivor_orbits = set()
                for tail in mixed_tails[pivot]:
                    counts = Counter(tail)
                    new = tuple(a + counts[cell] for a, cell
                                in zip(base_vector, anchor_cells, strict=True))
                    if not pivots(new):
                        survivor_orbits.add(canonical_signature(new))
                if survivor_orbits <= selected_signatures:
                    candidates.append((pivot, tuple(sorted(survivor_orbits))))
            require(candidates, (signature, canonical_signature(signature)))
            chosen_pivot[signature] = min(candidates)
    require(len(chosen_pivot) == 216, len(chosen_pivot))

    occurrence_count = 0
    exact_rows = Counter()
    signature_destination_sets = defaultdict(set)
    signature_examples = defaultdict(dict)
    transition_counts = Counter()
    ratio_profiles = defaultdict(Counter)
    identity_ratio_edges = 0
    rows_without_chart = 0
    for r8 in h_representatives:
        for packet_row in packet:
            target = bytes(sorted(r8 + packet_row))
            signature = anchor_signature(target)
            pivot, _survivor_orbits = chosen_pivot[signature]
            quotient = subtract(target, mixed_anchor_terms[pivot])
            for tail in mixed_tails[pivot]:
                row = bytes(sorted(quotient + tail))
                new_signature = anchor_signature(row)
                if pivots(new_signature):
                    continue
                orbit_signature = canonical_signature(new_signature)
                require(orbit_signature in selected_signatures,
                        (orbit_signature, "outside chosen cover"))
                occurrence_count += 1
                exact_rows[row] += 1
                rows = destinations(row)
                destination_types = tuple(sorted({item[0] for item in rows}))
                signature_destination_sets[orbit_signature].add(destination_types)
                signature_examples[orbit_signature].setdefault(destination_types,
                                                               row.hex())
                if not rows:
                    rows_without_chart += 1
                for destination, overlap, positive, negative in rows:
                    transition_counts[destination] += 1
                    ratio_profiles[destination][overlap] += 1
                    identity_ratio_edges += int(not positive and not negative)

    require(set(signature_destination_sets) == selected_signatures,
            (len(signature_destination_sets), len(selected_signatures)))
    collision = None
    for signature in sorted(signature_destination_sets):
        profiles = sorted(signature_destination_sets[signature])
        if len(profiles) > 1:
            left, right = profiles[:2]
            collision = {
                "anchor_signature_orbit": str(signature),
                "first_destination_types": list(left),
                "first_literal_row_hex": signature_examples[signature][left],
                "second_destination_types": list(right),
                "second_literal_row_hex": signature_examples[signature][right],
            }
            break

    destinations_seen = tuple(sorted(transition_counts))
    self_edge = source_chart in transition_counts
    # This graph only contains the source chart and observed destinations;
    # without recentered K16 packets it has no composable non-source edges.
    # The only possible nontrivial/equality SCC would therefore be a self-loop.
    sccs = [[source_chart]] + [[chart] for chart in destinations_seen
                              if chart != source_chart]
    strict_potential = (not self_edge)
    result = {
        "status": "PASS literal K16 chart-transition provenance audit",
        "packet": {
            "construction": (
                "lex-first literal singleton pivot per one of 216 K14 anchor "
                "signatures, constrained to the exact 25-orbit minimum "
                "single-pivot cover"
            ),
            "literal_occurrences": occurrence_count,
            "distinct_literal_rows": len(exact_rows),
            "relaxed_anchor_orbits": len(selected_signatures),
            "rows_without_any_dividing_pure_chart_product": rows_without_chart,
            "literal_completion_collision": collision,
            "scope_guard": (
                "The frozen 25 signatures alone do not determine chart "
                "divisibility. This packet is a new source-faithful single-"
                "pivot lift; it is not the affine 25-orbit combination and "
                "not a collected K16 residual with coefficients."
            ),
        },
        "transition_graph": {
            "source_chart": source_chart,
            "destination_chart_types": list(destinations_seen),
            "node_count": 1 + len(set(destinations_seen) - {source_chart}),
            "edge_type_count": len(destinations_seen),
            "literal_transition_count_by_destination": {
                str(chart): transition_counts[chart] for chart in destinations_seen
            },
            "ratio_source_anchor_overlap_histogram_by_destination": {
                str(chart): {str(overlap): count for overlap, count
                             in sorted(ratio_profiles[chart].items())}
                for chart in destinations_seen
            },
            "ratio_formula": (
                "P_destination/P_source has +1 on destination\\source cells, "
                "-1 on source\\destination anchors, and zero elsewhere; "
                "both supports have size 12-overlap."
            ),
            "source_self_edge": self_edge,
            "strict_two_level_potential_exists": strict_potential,
            "potential": ({str(source_chart): 0,
                           **{str(chart): 1 for chart in destinations_seen
                              if chart != source_chart}}
                          if strict_potential else None),
            "minimal_SCCs_in_observed_two_level_graph": sccs,
            "source_chart_type_self_edges": transition_counts[source_chart],
            "literal_identity_ratio_edges": identity_ratio_edges,
            "source_chart_type_self_edge_overlap_histogram": {
                str(overlap): count for overlap, count
                in sorted(ratio_profiles[source_chart].items())
            },
            "analytic_guard": (
                "The two-level potential is purely combinatorial. No modulus "
                "inequality follows for the Laurent ratios, and edges cannot "
                "be iterated without independently recentering the K16 packet "
                "on every destination chart."
            ),
        },
        "pinned": {
            str(K14_PATH.relative_to(ROOT)): sha256(K14_PATH.read_bytes()).hexdigest(),
            str(COVER_PATH.relative_to(ROOT)): sha256(COVER_PATH.read_bytes()).hexdigest(),
            str(CHART_PATH.relative_to(ROOT)): sha256(CHART_PATH.read_bytes()).hexdigest(),
        },
    }
    return result


def main(write_results=False):
    result = build()
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": logical,
        "packet": result["packet"],
        "transition_graph": result["transition_graph"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
