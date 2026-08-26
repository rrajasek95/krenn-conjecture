#!/usr/bin/env python3
"""Literal support propagation audit for the remote tail branch.

This is deliberately a support-only audit.  It expands the B4 x S3 orbit of
F_02222212, records its cofactor and quadratic support implications, and
classifies the smallest propagation cycles.  It makes no inference from a
live monomial to a nonzero polynomial coefficient.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_tail_remote_support_propagation.json"
DIAGONAL_SUPPORT_RESULT = (HERE.parent /
    "unaudited-codex-tail-polar-source-lift-2026-08-21" /
    "results_tail_support_boundary_orbits.json")
V = tuple(range(8))
COLORS = (0, 1, 2)
ANCHORS = frozenset(((0, 1), (2, 3), (4, 5), (6, 7)))
PHYSICAL_EDGES = tuple(combinations(V, 2))
CROSS_BLOCK_EDGES = tuple(e for e in PHYSICAL_EDGES if e[0] // 2 != e[1] // 2)
SAME_BLOCK_EDGES = tuple(sorted(ANCHORS))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def vertex_actions():
    answer = set()
    for block_perm in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            action = []
            for vertex in V:
                block, clone = divmod(vertex, 2)
                action.append(2 * block_perm[block] + (clone ^ flips[block]))
            answer.add(tuple(action))
    require(len(answer) == 384, "B4 order changed")
    return tuple(sorted(answer))


def color_actions():
    return tuple(permutations(COLORS))


def act_word(word, va, ca):
    image = [None] * 8
    for old in V:
        image[va[old]] = ca[word[old]]
    return tuple(image)


def cell(u, v, cu, cv):
    if u < v:
        return (u, v, cu, cv)
    return (v, u, cv, cu)


def cell_label(atom):
    u, v, cu, cv = atom
    return f"a_{u}{v}_{cu}{cv}"


def act_cell(atom, va, ca):
    u, v, cu, cv = atom
    return cell(va[u], va[v], ca[cu], ca[cv])


def word_label(word):
    return "F_" + "".join(map(str, word))


def row_record(word):
    counts = Counter(word)
    majority = next(c for c in COLORS if counts[c] == 6)
    exceptional = [v for v in V if word[v] != majority]
    require(len(exceptional) == 2, "not a 611 word")
    u, v = sorted(exceptional)
    require((u, v) in CROSS_BLOCK_EDGES, "transport left cross-block orbit")
    source = cell(u, v, word[u], word[v])
    linear = []
    quadratic = []
    for matching in perfect_matchings(V):
        variables = tuple(sorted(
            (cell_label(cell(a, b, word[a], word[b])) for a, b in matching)
        ))
        if tuple(sorted((u, v))) in tuple(tuple(sorted(e)) for e in matching):
            linear.append({
                "matching": [list(e) for e in matching],
                "variables": list(variables),
            })
        else:
            cross_factors = tuple(sorted(
                cell(a, b, word[a], word[b])
                for a, b in matching if word[a] != word[b]
            ))
            diag_edges = tuple(sorted(
                tuple(sorted((a, b))) for a, b in matching
                if word[a] == word[b]
            ))
            require(len(cross_factors) == 2 and len(diag_edges) == 2,
                    "quadratic term shape changed")
            quadratic.append({
                "matching": [list(e) for e in matching],
                "variables": list(variables),
                "cross_factors": [list(x) for x in cross_factors],
                "diagonal_edges": [list(x) for x in diag_edges],
            })
    require(len(linear) == 15 and len(quadratic) == 90,
            "611 15+90 split changed")
    residual = tuple(x for x in V if x not in (u, v))
    return {
        "source_label": word_label(word),
        "word": list(word),
        "exceptional_edge": [u, v],
        "exceptional_endpoint_colours": [word[u], word[v]],
        "majority_colour": majority,
        "source_cell": list(source),
        "cofactor_atom": f"h{majority}_{u}{v}",
        "cofactor_witnesses": [
            [list(e) for e in matching]
            for matching in perfect_matchings(residual)
        ],
        "linear_terms": linear,
        "quadratic_terms": quadratic,
    }


def sink_332_record(word):
    """The X5 row whose anchor matching contains one same-block mixed cell."""
    require(sorted(Counter(word).values(), reverse=True) == [3, 3, 2],
            "sink row is not 332")
    anchor_cross = [cell(a, b, word[a], word[b])
                    for a, b in ANCHORS if word[a] != word[b]]
    require(len(anchor_cross) == 1, "sink row anchor term is not linear")
    terms = []
    for matching in perfect_matchings(V):
        cross_factors = tuple(sorted(
            cell(a, b, word[a], word[b])
            for a, b in matching if word[a] != word[b]
        ))
        diagonal_edges = tuple(sorted(
            (tuple(sorted((a, b))), word[a]) for a, b in matching
            if word[a] == word[b]
        ))
        terms.append({
            "matching": [list(e) for e in matching],
            "cross_factors": [list(x) for x in cross_factors],
            "diagonal_factors": [[list(e), colour]
                                 for e, colour in diagonal_edges],
        })
    anchor_index = next(index for index, matching in
                        enumerate(perfect_matchings(V))
                        if frozenset(map(tuple, matching)) == ANCHORS)
    require(len(terms[anchor_index]["cross_factors"]) == 1,
            "anchor term changed")
    return {
        "source_label": word_label(word),
        "word": list(word),
        "sink_cell": list(anchor_cross[0]),
        "anchor_term_index": anchor_index,
        "alternative_terms": [term for index, term in enumerate(terms)
                              if index != anchor_index],
        "term_cross_degree_histogram": dict(sorted(Counter(
            len(term["cross_factors"]) for term in terms
        ).items())),
    }


def tarjan(nodes, adjacency):
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    low = {}
    components = []

    def visit(v):
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in adjacency.get(v, ()):
            if w not in indices:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == v:
                    break
            components.append(tuple(sorted(component)))

    for node in nodes:
        if node not in indices:
            visit(node)
    return tuple(components)


def orbit_records(objects, act):
    unseen = set(objects)
    records = []
    while unseen:
        rep = min(unseen)
        orbit = {act(rep, va, ca)
                 for va in vertex_actions() for ca in color_actions()}
        orbit &= set(objects)
        require(orbit, "empty orbit")
        unseen -= orbit
        records.append((rep, len(orbit)))
    return tuple(records)


def act_pair(pair, va, ca):
    return tuple(sorted((act_cell(pair[0], va, ca),
                         act_cell(pair[1], va, ca))))


def act_support(support, va, ca):
    return tuple(sorted(act_cell(atom, va, ca) for atom in support))


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def minimum_sink_rescues(base_support, sink_rows_by_cell, sink_cells):
    """Exact minimum cross-factor supports for the twelve first-shell clauses."""
    clauses = []
    for sink in sorted(set(base_support) & sink_cells):
        for record in sorted(sink_rows_by_cell[sink],
                             key=lambda item: item["source_label"]):
            options = {
                frozenset(map(tuple, term["cross_factors"])) - set(base_support)
                for term in record["alternative_terms"]
            }
            options.discard(frozenset())
            options = {option for option in options
                       if not any(other < option for other in options)}
            clauses.append((record, options))
    require(len(clauses) == 12, "terminal shell should have twelve sink clauses")
    universe = sorted(set().union(*(
        set().union(*options) for _, options in clauses
    )))
    atom_index = {atom: index for index, atom in enumerate(universe)}
    clause_masks = []
    for _, options in clauses:
        clause_masks.append(tuple(sorted({
            sum(1 << atom_index[atom] for atom in option)
            for option in options
        }, key=lambda mask: (mask.bit_count(), mask))))
    all_clauses = (1 << len(clauses)) - 1

    def covered(chosen):
        mask = 0
        for index, options in enumerate(clause_masks):
            if any(not option & ~chosen for option in options):
                mask |= 1 << index
        return mask

    def search(limit, collect):
        seen = set()
        solutions = set()

        def recurse(chosen):
            if chosen in seen:
                return False
            seen.add(chosen)
            cover = covered(chosen)
            if cover == all_clauses:
                solutions.add(chosen)
                return not collect
            candidates = []
            for index, options in enumerate(clause_masks):
                if (cover >> index) & 1:
                    continue
                valid = [chosen | option for option in options
                         if (chosen | option).bit_count() <= limit]
                if not valid:
                    return False
                candidates.append((len(valid), index, valid))
            _, _, valid = min(candidates,
                              key=lambda item: (item[0], item[1]))
            for new_chosen in valid:
                if recurse(new_chosen) and not collect:
                    return True
            return False

        exists = recurse(0)
        return exists, solutions, len(seen)

    lower_search_states = {}
    for limit in range(1, 6):
        exists, _, states = search(limit, False)
        require(not exists, f"unexpected sink rescue below six cells: {limit}")
        lower_search_states[str(limit)] = states
    _, solution_masks, states6 = search(6, True)
    solutions = {
        frozenset(universe[index] for index in range(len(universe))
                  if (mask >> index) & 1)
        for mask in solution_masks
    }
    require(len(solutions) == 484 and all(len(s) == 6 for s in solutions),
            "minimum sink rescue census changed")
    return clauses, solutions, lower_search_states, states6


def main(write_results=False):
    vas = vertex_actions()
    cas = color_actions()
    seed = tuple(map(int, "02222212"))
    orbit_words = {act_word(seed, va, ca) for va in vas for ca in cas}
    require(len(orbit_words) == 144, "seed orbit is not 144")
    require(sum(act_word(seed, va, ca) == seed for va in vas for ca in cas) == 16,
            "seed stabilizer is not 16")
    rows = tuple(row_record(word) for word in sorted(orbit_words))
    require(len({r["source_label"] for r in rows}) == 144,
            "source labels collided")

    sink_seed = tuple(map(int, "00112212"))
    sink_words = {act_word(sink_seed, va, ca) for va in vas for ca in cas}
    require(len(sink_words) == 144, "sink 332 orbit is not 144")
    require(sum(act_word(sink_seed, va, ca) == sink_seed
                for va in vas for ca in cas) == 16,
            "sink 332 stabilizer is not 16")
    sink_rows = tuple(sink_332_record(word) for word in sorted(sink_words))
    require(Counter(tuple(r["sink_cell"]) for r in sink_rows) ==
            Counter({cell(u, v, i, j): 6 for u, v in SAME_BLOCK_EDGES
                     for i in COLORS for j in COLORS if i != j}),
            "each sink cell should have six X5 rows")

    # Conditional hyperedges: source cell AND the displayed six-site
    # cofactor -> OR of the ninety displayed quadratic monomials.
    all_cells = tuple(cell(u, v, i, j)
                      for u, v in PHYSICAL_EDGES
                      for i in COLORS for j in COLORS if i != j)
    source_cells = {tuple(r["source_cell"]) for r in rows}
    require(len(all_cells) == 168 and len(source_cells) == 144,
            "cross-colour cell census changed")
    require(all((a[0], a[1]) in CROSS_BLOCK_EDGES for a in source_cells),
            "source-cell orbit is not exactly cross-block")

    consequence_pairs = {}
    adjacency = {a: set() for a in all_cells}
    for record in rows:
        source = tuple(record["source_cell"])
        pairs = set()
        for term in record["quadratic_terms"]:
            pair = tuple(sorted(tuple(x) for x in term["cross_factors"]))
            pairs.add(pair)
            adjacency[source].update(pair)
        require(len(pairs) == 30, "quadratic cross-factor pairs changed")
        consequence_pairs[source] = tuple(sorted(pairs))

    edge_count = sum(len(v) for v in adjacency.values())
    components = tarjan(all_cells, adjacency)
    scc_hist = Counter(map(len, components))

    mutual_pairs = set()
    for source in source_cells:
        for target in adjacency[source]:
            if target in source_cells and source in adjacency[target]:
                mutual_pairs.add(tuple(sorted((source, target))))
    pair_orbits = orbit_records(mutual_pairs, act_pair)

    # Add the exact X5 clauses based at the same-block sinks.  The live
    # anchor monomial is nonzero on the four-anchor chart, so its 332 row
    # forces at least one of the other 104 literal matching monomials live.
    combined_adjacency = {a: set(targets)
                          for a, targets in adjacency.items()}
    for record in sink_rows:
        sink = tuple(record["sink_cell"])
        for term in record["alternative_terms"]:
            combined_adjacency[sink].update(map(tuple,
                                                term["cross_factors"]))
    combined_edge_count = sum(map(len, combined_adjacency.values()))
    combined_components = tarjan(all_cells, combined_adjacency)
    combined_scc_hist = Counter(map(len, combined_components))
    combined_self_loops = {source for source in all_cells
                           if source in combined_adjacency[source]}
    combined_self_loop_orbits = orbit_records(
        {tuple((source,)) for source in combined_self_loops}, act_support)
    combined_mutual_pairs = set()
    for source in all_cells:
        for target in combined_adjacency[source]:
            if source != target and source in combined_adjacency[target]:
                combined_mutual_pairs.add(tuple(sorted((source, target))))
    combined_pair_orbits = orbit_records(combined_mutual_pairs, act_pair)

    # Hypergraph-faithful smallest closed supports.  Same-block cells have no
    # outgoing transported 611 clause.  A terminal support chooses the two
    # same-block factors.  A two-source support chooses mutually rescuing
    # source factors and one same-block sink in each direction.
    sink_cells = set(all_cells) - source_cells
    terminal_supports = set()
    for source in source_cells:
        for pair in consequence_pairs[source]:
            if set(pair) <= sink_cells:
                terminal_supports.add(tuple(sorted((source,) + pair)))
    require(len(terminal_supports) == 144,
            "one terminal support per transported source expected")

    sink_rows_by_cell = {}
    for record in sink_rows:
        sink_rows_by_cell.setdefault(tuple(record["sink_cell"]), []).append(record)
    terminal_internal_sink_rescues = 0
    terminal_unresolved_sink_clauses = 0
    for support_tuple in terminal_supports:
        support = set(support_tuple)
        for sink in support & sink_cells:
            for record in sink_rows_by_cell[sink]:
                internally_rescued = any(
                    set(map(tuple, term["cross_factors"])) <= support
                    for term in record["alternative_terms"]
                )
                terminal_internal_sink_rescues += int(internally_rescued)
                terminal_unresolved_sink_clauses += int(not internally_rescued)
    require(terminal_internal_sink_rescues == 0 and
            terminal_unresolved_sink_clauses == 144 * 2 * 6,
            "a terminal support unexpectedly rescues an X5 sink clause")

    two_source_supports = set()
    for source in source_cells:
        for pair in consequence_pairs[source]:
            source_part = [x for x in pair if x in source_cells]
            sink_part = [x for x in pair if x in sink_cells]
            if len(source_part) != 1 or len(sink_part) != 1:
                continue
            target = source_part[0]
            for back in consequence_pairs[target]:
                if source in back and len(set(back) & sink_cells) == 1:
                    support = tuple(sorted(set((source, target) + pair + back)))
                    live_sources = set(support) & source_cells
                    if live_sources == {source, target}:
                        two_source_supports.add(support)

    terminal_orbits = orbit_records(terminal_supports, act_support)
    two_source_orbits = orbit_records(two_source_supports, act_support)

    # For the representative terminal support, classify the three literal
    # diagonal Q witnesses.  The anchor Q witness is forced-compatible with
    # every four-anchor chart; the other two require two cross-block edges.
    representative_source = cell(0, 6, 0, 1)
    representative_terminal = next(
        s for s in terminal_supports if representative_source in s)
    rep_row = next(r for r in rows
                   if tuple(r["source_cell"]) == representative_source)
    rep_terms = []
    terminal_other = set(representative_terminal) - {representative_source}
    for term in rep_row["quadratic_terms"]:
        if set(map(tuple, term["cross_factors"])) == terminal_other:
            rep_terms.append(term)
    require(len(rep_terms) == 3, "terminal pair should have three Q witnesses")
    witness_hist = Counter(
        "anchor_pair" if set(map(tuple, term["diagonal_edges"])) <= ANCHORS
        else "cross_pair"
        for term in rep_terms
    )
    require(witness_hist == Counter({"anchor_pair": 1, "cross_pair": 2}),
            "terminal diagonal witness types changed")

    canonical_terminal = frozenset((
        cell(0, 6, 0, 1), cell(0, 1, 0, 2), cell(6, 7, 1, 2)
    ))
    require(frozenset(representative_terminal) == canonical_terminal,
            "canonical terminal support changed")
    rescue_clauses, rescue_additions, lower_states, states6 = (
        minimum_sink_rescues(canonical_terminal, sink_rows_by_cell, sink_cells)
    )
    terminal_stabilizer = [
        (va, ca) for va in vas for ca in cas
        if frozenset(act_cell(atom, va, ca) for atom in canonical_terminal)
        == canonical_terminal
    ]
    require(len(terminal_stabilizer) == 16,
            "canonical terminal stabilizer changed")
    unseen_rescues = set(rescue_additions)
    rescue_orbits = []
    while unseen_rescues:
        representative = min(unseen_rescues,
                             key=lambda value: tuple(sorted(value)))
        orbit = {
            frozenset(act_cell(atom, va, ca) for atom in representative)
            for va, ca in terminal_stabilizer
        } & rescue_additions
        unseen_rescues -= orbit
        rescue_orbits.append((representative, len(orbit)))
    require(len(rescue_orbits) == 75 and sum(size for _, size in rescue_orbits) == 484,
            "minimum rescue orbit census changed")

    # Freeze a coefficient-unit seed for every orbit: a literal source label
    # and one matching whose cross factors lie in the nine-cell support.
    rescue_ledger = []
    for representative, orbit_size in rescue_orbits:
        total_support = canonical_terminal | representative
        witnesses = []
        for record, _ in rescue_clauses:
            candidates = [term for term in record["alternative_terms"]
                          if set(map(tuple, term["cross_factors"])) <= total_support]
            require(candidates, "minimum rescue ceased to cover a sink clause")
            selected = min(candidates, key=lambda term: (
                len(term["cross_factors"]), term["cross_factors"],
                term["diagonal_factors"], term["matching"]))
            witnesses.append({
                "source_label": record["source_label"],
                "matching": selected["matching"],
                "cross_factors": [cell_label(tuple(atom))
                                  for atom in selected["cross_factors"]],
                "diagonal_factors": selected["diagonal_factors"],
            })
        rescue_ledger.append({
            "orbit_size": orbit_size,
            "added_cells": [cell_label(atom) for atom in sorted(representative)],
            "total_cross_support": [cell_label(atom)
                                    for atom in sorted(total_support)],
            "literal_sink_witnesses": witnesses,
        })

    # Exact aligned support-6 compatibility filter.  This is support routing,
    # not a claim that the displayed witness coefficients cancel correctly.
    diagonal_result = json.loads(DIAGONAL_SUPPORT_RESULT.read_text())
    support6_graphs = [
        frozenset(ANCHORS | {tuple(map(int, edge)) for edge in record["cross_edges"]})
        for record in diagonal_result["diagonal_three_colour_structural_scan"]["deficient"]
    ]
    require(len(support6_graphs) == 8, "support6 graph census changed")

    def term_live_on_aligned_graph(term, graph, cross_support):
        return (set(map(tuple, term["cross_factors"])) <= cross_support and
                all(tuple(factor[0]) in graph
                    for factor in term["diagonal_factors"]))

    aligned_support6_compatible = 0
    aligned_support6_orbit_indices = []
    for orbit_index, (representative, _) in enumerate(rescue_orbits):
        total_support = canonical_terminal | representative
        compatible = False
        for graph in support6_graphs:
            h_live = any(all(tuple(sorted(edge)) in graph for edge in matching)
                         for matching in perfect_matchings((1, 2, 3, 4, 5, 7)))
            q_live = any(all(tuple(edge) in graph
                             for edge in term["diagonal_edges"])
                         for term in rep_terms)
            sinks_live = all(any(
                term_live_on_aligned_graph(term, graph, total_support)
                for term in record["alternative_terms"]
            ) for record, _ in rescue_clauses)
            if h_live and q_live and sinks_live:
                compatible = True
                break
        aligned_support6_compatible += int(compatible)
        if compatible:
            aligned_support6_orbit_indices.append(orbit_index)

    # The requested fixed-point closure is stopped at the prescribed 500
    # orbit guard.  Orbit 56 is a non-support6 first-shell survivor.  On the
    # dense diagonal support (which passes the literal support form of all
    # pure/permanent/triangle rows), four newly live cross-block cells have
    # live cofactors and unsatisfied 611 implications.  After removing
    # factors already live, each has ten inclusion-minimal cross-pair
    # rescues.  Their Cartesian unions are all distinct and inclusion-minimal.
    explosion_index = 56
    require(explosion_index not in aligned_support6_orbit_indices,
            "explosion control unexpectedly routed to support6")
    explosion_base = canonical_terminal | rescue_orbits[explosion_index][0]
    row_by_source = {tuple(record["source_cell"]): record for record in rows}
    explosion_clauses = []
    for source in sorted(explosion_base & source_cells):
        pairs = {
            frozenset(map(tuple, term["cross_factors"]))
            for term in row_by_source[source]["quadratic_terms"]
        }
        if any(pair <= explosion_base for pair in pairs):
            continue
        options = {pair - explosion_base for pair in pairs}
        options = {option for option in options
                   if not any(other < option for other in options)}
        explosion_clauses.append((source, options))
    require(len(explosion_clauses) == 4 and
            all(len(options) == 10 for _, options in explosion_clauses),
            "second-round four-by-ten branch certificate changed")
    explosion_universe = sorted(set().union(*(
        set().union(*options) for _, options in explosion_clauses
    )))
    explosion_index_of = {atom: index for index, atom in
                          enumerate(explosion_universe)}
    explosion_masks = []
    for _, options in explosion_clauses:
        explosion_masks.append({
            sum(1 << explosion_index_of[atom] for atom in option)
            for option in options
        })
    unions = {0}
    for options in explosion_masks:
        unions = {old | option for old in unions for option in options}

    def covers_explosion(mask):
        return all(any(not option & ~mask for option in options)
                   for options in explosion_masks)

    minimal_unions = {
        mask for mask in unions
        if all(not covers_explosion(mask ^ (1 << bit))
               for bit in range(len(explosion_universe))
               if (mask >> bit) & 1)
    }
    require(len(unions) == len(minimal_unions) == 10000,
            "second-round minimum union count changed")
    explosion_size_hist = Counter(mask.bit_count() for mask in minimal_unions)
    require(explosion_size_hist == Counter({
        4: 625, 5: 2500, 6: 3750, 7: 2500, 8: 625,
    }), "second-round size histogram changed")
    explosion_orbit_lower_bound = (
        len(minimal_unions) + len(terminal_stabilizer) - 1
    ) // len(terminal_stabilizer)
    require(explosion_orbit_lower_bound == 625,
            "second-round orbit lower bound changed")

    compact_rows = []
    for record in rows:
        compact_rows.append({
            "source_label": record["source_label"],
            "word": record["word"],
            "source_cell": cell_label(tuple(record["source_cell"])),
            "cofactor_atom": record["cofactor_atom"],
            "cofactor_witness_count": len(record["cofactor_witnesses"]),
            "quadratic_consequent_count": len(record["quadratic_terms"]),
            "quadratic_cross_pair_count": len(consequence_pairs[tuple(record["source_cell"])])
        })

    result = {
        "status": "PASS literal conditional support propagation audit",
        "source_scope": {
            "seed": "F_02222212",
            "group": "B4 x S3",
            "group_order": 2304,
            "orbit_size": 144,
            "stabilizer_order": 16,
            "covered_611_rows": "24 cross-block exceptional edges x 6 ordered exceptional colours",
            "not_in_orbit": "24 rows on the four same-block exceptional edges",
        },
        "literal_implication_hypergraph": {
            "conditional_hyperedges": 144,
            "antecedent": "live source cell a_uv_ij AND nonzero h^k_uv",
            "cofactor_support_witnesses_per_edge": 15,
            "quadratic_monomial_consequents_per_edge": 90,
            "distinct_cross_factor_pairs_per_edge": 30,
            "literal_quadratic_consequent_occurrences": 12960,
            "cofactor_witness_occurrences": 2160,
            "source_rows": compact_rows,
        },
        "X5_same_block_sink_hypergraph": {
            "seed": "F_00112212",
            "orbit_size": 144,
            "stabilizer_order": 16,
            "same_block_sink_atoms": 24,
            "rows_per_sink_atom": 6,
            "antecedent": (
                "live same-block cross-colour cell times the three live "
                "same-colour anchor entries"
            ),
            "alternative_matching_consequents_per_row": 104,
            "literal_alternative_occurrences": 14976,
            "term_cross_degree_histogram_per_row": {
                "1": 9, "2": 18, "3": 42, "4": 36
            },
            "source_labels": [r["source_label"] for r in sink_rows],
        },
        "projected_dependency_graph": {
            "cross_colour_cell_atoms": 168,
            "source_atoms_cross_block": 144,
            "same_block_sink_atoms": 24,
            "directed_edges": edge_count,
            "scc_size_histogram": {str(k): v for k, v in sorted(scc_hist.items())},
            "mutual_two_cycles": len(mutual_pairs),
            "mutual_two_cycle_orbits": len(pair_orbits),
            "mutual_two_cycle_orbit_ledger": [
                {"representative": [cell_label(x) for x in rep],
                 "orbit_size": size}
                for rep, size in pair_orbits
            ],
        },
        "smallest_hypergraph_closed_cell_supports": {
            "terminal_size3_count": len(terminal_supports),
            "terminal_size3_orbits": len(terminal_orbits),
            "terminal_orbit_ledger": [
                {"representative": [cell_label(x) for x in rep],
                 "orbit_size": size}
                for rep, size in terminal_orbits
            ],
            "two_source_count": len(two_source_supports),
            "two_source_size_histogram": dict(sorted(Counter(map(len, two_source_supports)).items())),
            "two_source_orbits": len(two_source_orbits),
            "two_source_orbit_ledger": [
                {"representative": [cell_label(x) for x in rep],
                 "support_size": len(rep), "orbit_size": size}
                for rep, size in two_source_orbits
            ],
            "representative_terminal_source": cell_label(representative_source),
            "representative_terminal_support": [cell_label(x) for x in representative_terminal],
            "representative_Q_diagonal_witness_types": dict(witness_hist),
            "X5_verdict": (
                "None of the size-3 terminal supports is closed after the "
                "six F_00112212-orbit clauses based at each of its two "
                "same-block sink cells; direct literal enumeration finds "
                "zero alternative term whose cross-factor set is contained "
                "in that size-3 support."
            ),
            "terminal_internal_sink_rescues": terminal_internal_sink_rescues,
            "terminal_unresolved_sink_clauses": terminal_unresolved_sink_clauses,
        },
        "combined_611_plus_sink_332_projection": {
            "directed_edges": combined_edge_count,
            "scc_size_histogram": {str(k): v
                                   for k, v in sorted(combined_scc_hist.items())},
            "projected_self_loops": len(combined_self_loops),
            "projected_self_loop_orbits": len(combined_self_loop_orbits),
            "projected_self_loop_orbit_ledger": [
                {"representative": [cell_label(x) for x in rep],
                 "orbit_size": size}
                for rep, size in combined_self_loop_orbits
            ],
            "mutual_two_cycles": len(combined_mutual_pairs),
            "mutual_two_cycle_orbits": len(combined_pair_orbits),
            "mutual_two_cycle_orbit_ledger": [
                {"representative": [cell_label(x) for x in rep],
                 "orbit_size": size}
                for rep, size in combined_pair_orbits
            ],
        },
        "minimum_first_shell_rescue_antichain": {
            "scope": (
                "Cross-factor projection for the canonical terminal 611 "
                "support.  It covers all twelve sink 332 clauses; diagonal "
                "factors are retained in the witness ledger and all later "
                "X5 clauses remain to be imposed."
            ),
            "minimum_added_cross_cells": 6,
            "lower_bound_exhaustive_search_states": lower_states,
            "minimum_search_states": states6,
            "labelled_minimum_supports": 484,
            "terminal_stabilizer_order": 16,
            "minimum_support_orbits": len(rescue_orbits),
            "orbit_size_histogram": dict(sorted(Counter(
                size for _, size in rescue_orbits).items())),
            "total_cross_cells_per_support": 9,
            "aligned_support6_compatible_orbits": aligned_support6_compatible,
            "aligned_support6_compatible_orbit_indices": aligned_support6_orbit_indices,
            "support8_filter": (
                "not applied: no source-labelled support8 support-signature "
                "interface is frozen in the tail package"
            ),
            "active_carrier_filter": (
                "not decidable from support alone: activity is a rank/row-span "
                "condition, and no orbit has a termwise support certificate"
            ),
            "orbit_ledger": rescue_ledger,
        },
        "second_round_stop_certificate": {
            "status": "STOP: prescribed 500-orbit guard exceeded",
            "first_shell_orbit_index": explosion_index,
            "base_cross_support": [cell_label(atom)
                                   for atom in sorted(explosion_base)],
            "not_aligned_support6_compatible": True,
            "diagonal_support_feasibility": (
                "The all-live diagonal support satisfies the literal support "
                "conditions from pure/permanent/triangle rows and makes every "
                "displayed cofactor/diagonal matching factor live.  This is a "
                "support-feasibility witness only, not coefficient existence."
            ),
            "new_must_fire_611_sources": [cell_label(source)
                                         for source, _ in explosion_clauses],
            "minimum_options_per_source": [len(options)
                                           for _, options in explosion_clauses],
            "distinct_inclusion_minimal_labelled_branches": len(minimal_unions),
            "added_cell_size_histogram": dict(sorted(explosion_size_hist.items())),
            "terminal_stabilizer_order": len(terminal_stabilizer),
            "orbit_count_lower_bound": explosion_orbit_lower_bound,
            "conclusion": (
                "Even one of the 69 non-support6 first-shell orbit representatives "
                "produces at least 625 terminal-stabilizer orbits at the next 611 "
                "round.  Therefore the requested <=500 orbit guard fires before a "
                "fixed point; no coefficient solve or support-only cap claim follows."
            ),
        },
        "exact_scope_guard": (
            "Every implication is conditional on the displayed cofactor being nonzero. "
            "The SCC graph projects a two-factor disjunction to ordinary arcs and is "
            "discovery only.  The closed cell supports retain both cross factors but "
            "do not solve coefficients, impose every X5 row, or prove cap activity."
        ),
        "routing_checkpoint": (
            "The 611-only terminal size-3 orbit a_06_01,a_01_02,a_67_12 "
            "is killed as a closed model by the transported F_00112212 "
            "sink clauses.  The combined projected graph is recurrent, but "
            "a coefficient/unit conclusion still requires enumerating the "
            "higher support antichain with the diagonal monomial factors retained."
        ),
    }
    result["logical_sha256"] = logical_hash(result)
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "source_orbit": 144,
        "scc_histogram": result["projected_dependency_graph"]["scc_size_histogram"],
        "two_cycles": len(mutual_pairs),
        "two_cycle_orbits": len(pair_orbits),
        "terminal_orbits": len(terminal_orbits),
        "two_source_orbits": len(two_source_orbits),
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
