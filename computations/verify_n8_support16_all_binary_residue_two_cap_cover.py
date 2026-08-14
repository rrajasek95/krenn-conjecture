#!/usr/bin/env python3
"""Test all crossed two-monomial cap residues, not only (2,2) faces.

A cap response through a directed noncoordinate block X is binary-compatible
when its star-zero residue consists of two crossed oriented monomials.  The
number of X-containing monomials is irrelevant: a left/right kernel through
X kills all of them.  If the cap edge and both residue shores carry the three
distinct anchor colours and the direct coordinate of X is nonzero, the
already proved rank-two matrix kills the crossed permanent with active
diagonal readouts.

This checker searches the full mutual-coordinate anchor CSP for a colouring
and a noncoordinate support chart which avoids every such cap.  Absence of a
guard is an exact two-cap landing theorem; a returned guard is the finite
obstruction for the next response layer.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "7c3e00333001f5beb18b0f5538ac96885e556f153ca3459d02873221b132d20c"
COLORS = (0, 1, 2)
NONANCHOR = -1


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROTOTYPE = load_local(
    "n8_support16_prototype_for_all_binary_residues",
    "verify_n8_support16_two_cap_prototype_orbit_extension.py",
)
ORBIT = PROTOTYPE.ORBIT
LANDING = PROTOTYPE.LANDING


def source_edge(star):
    endpoint, external = star
    return tuple(sorted((endpoint, external)))


def binary_faces(adjacency, edges, incidence, shapes):
    faces = []
    for cap_edge, through_count, residue_count in shapes:
        if residue_count != 2:
            continue
        through, residue = PROTOTYPE.cap_shape(
            adjacency, edges, incidence, cap_edge
        )
        require(len(through) == through_count and len(residue) == 2,
                ("binary face split changed", cap_edge, through_count,
                 residue_count, through, residue))
        p_stars, q_stars = PROTOTYPE.audit_prototype_crossed_shape(
            cap_edge, residue
        )
        p_edges = tuple(source_edge(star) for star in p_stars)
        q_edges = tuple(source_edge(star) for star in q_stars)
        require(len(set(p_edges)) == len(set(q_edges)) == 2,
                ("binary shore repeated a source edge", cap_edge,
                 p_edges, q_edges))
        require(incidence[1] not in p_edges + q_edges,
                ("binary residue retained target edge", incidence,
                 cap_edge, p_edges, q_edges))
        side = "left" if cap_edge[0] == incidence[0] else "right"
        faces.append({
            "cap_edge": cap_edge,
            "through_count": through_count,
            "residue_count": residue_count,
            "kernel_side": side,
            "p_shore_edges": p_edges,
            "q_shore_edges": q_edges,
        })
    return tuple(faces)


def face_lands(face, states, zero_coordinate):
    relevant = ((face["cap_edge"],)
                + face["p_shore_edges"] + face["q_shore_edges"])
    if not all(edge in states for edge in relevant):
        return False
    direct = states[face["cap_edge"]]
    require(direct >= 0, ("binary direct edge is noncoordinate", face))
    if zero_coordinate is not None and direct == zero_coordinate:
        return False
    complement = set(COLORS) - {direct}
    return (
        {states[edge] for edge in face["p_shore_edges"]} == complement
        and {states[edge] for edge in face["q_shore_edges"]} == complement
    )


def avoiding_completion(edges, target_edge, faces, zero_coordinate):
    """Find a complete anchor chart in which no binary face lands.

    `zero_coordinate=0` represents all two-coordinate nonanchor charts up to
    global colour permutation.  `None` represents full support.  For the
    latter we fix one anchor edge to colour zero, again by global symmetry.
    """
    require(zero_coordinate in (None, 0),
            ("unsupported noncoordinate chart", zero_coordinate))
    states = {target_edge: NONANCHOR}
    anchor_edges = tuple(edge for edge in edges if edge != target_edge)
    if zero_coordinate is None:
        states[anchor_edges[0]] = 0
    incident = {
        vertex: tuple(edge for edge in anchor_edges if vertex in edge)
        for vertex in range(8)
    }
    face_frequency = Counter(
        edge
        for face in faces
        for edge in ((face["cap_edge"],)
                     + face["p_shore_edges"] + face["q_shore_edges"])
    )
    visited = 0

    def recurse():
        nonlocal visited
        visited += 1
        for vertex in range(8):
            seen = {states[edge] for edge in incident[vertex]
                    if edge in states}
            remaining = sum(edge not in states for edge in incident[vertex])
            if 3 - len(seen) > remaining:
                return None
        if any(face_lands(face, states, zero_coordinate) for face in faces):
            return None
        if all(edge in states for edge in anchor_edges):
            if all({states[edge] for edge in incident[vertex]}
                   == set(COLORS) for vertex in range(8)):
                return tuple(sorted(states.items()))
            return None

        unassigned = tuple(edge for edge in anchor_edges if edge not in states)

        def pressure(edge):
            vertex_pressure = sum(
                3 - len({states[item] for item in incident[vertex]
                         if item in states})
                for vertex in edge
            )
            return (face_frequency[edge], vertex_pressure)

        edge = max(unassigned, key=pressure)
        for colour in COLORS:
            states[edge] = colour
            answer = recurse()
            if answer is not None:
                return answer
        del states[edge]
        return None

    answer = recurse()
    return answer, visited


def matching_word_histogram(edges, target_edge, states, target_support):
    """Count literal decorated perfect-matching occurrences by site word."""
    edge_set = set(edges)
    words = Counter()
    for raw_matching in ORBIT.BASE.perfect_matchings(tuple(range(8))):
        matching = tuple(tuple(sorted(edge)) for edge in raw_matching)
        if not all(edge in edge_set for edge in matching):
            continue
        choices = tuple(
            target_support if edge == target_edge else (states[edge],)
            for edge in matching
        )
        for colours in product(*choices):
            word = [None] * 8
            for edge, colour in zip(matching, colours):
                word[edge[0]] = colour
                word[edge[1]] = colour
            require(None not in word,
                    ("matching occurrence left a site blank", matching,
                     colours, word))
            words[tuple(word)] += 1
    return words


def exact_source_guard_completion(edges, target_edge, faces,
                                  zero_coordinate):
    """Seek an avoiding chart with pure support and no mixed singleton.

    This is a necessary, coefficient-independent test for an exact source:
    a mixed fibre containing one literal matching occurrence cannot cancel
    because every live anchor and every declared target component is nonzero.
    """
    require(zero_coordinate in (None, 0),
            ("unsupported exact-source chart", zero_coordinate))
    target_support = ((1, 2) if zero_coordinate == 0 else COLORS)
    states = {target_edge: NONANCHOR}
    anchor_edges = tuple(edge for edge in edges if edge != target_edge)
    if zero_coordinate is None:
        states[anchor_edges[0]] = 0
    incident = {
        vertex: tuple(edge for edge in anchor_edges if vertex in edge)
        for vertex in range(8)
    }
    support_matchings = tuple(
        tuple(tuple(sorted(edge)) for edge in raw_matching)
        for raw_matching in ORBIT.BASE.perfect_matchings(tuple(range(8)))
        if all(tuple(sorted(edge)) in set(edges) for edge in raw_matching)
    )
    face_frequency = Counter(
        edge
        for face in faces
        for edge in ((face["cap_edge"],)
                     + face["p_shore_edges"] + face["q_shore_edges"])
    )
    counts = Counter()

    def recurse():
        counts["nodes"] += 1
        for vertex in range(8):
            seen = {states[edge] for edge in incident[vertex]
                    if edge in states}
            remaining = sum(edge not in states for edge in incident[vertex])
            if 3 - len(seen) > remaining:
                return None
        # Pure normalization is already impossible if some colour has no
        # still-compatible support matching.  This exact monotone prune is
        # substantially cheaper than waiting for a complete colouring.
        for colour in COLORS:
            if not any(all(
                    (edge == target_edge and colour in target_support)
                    or edge not in states
                    or states[edge] == colour
                    for edge in matching
            ) for matching in support_matchings):
                counts["pure_support_prunes"] += 1
                return None
        if any(face_lands(face, states, zero_coordinate) for face in faces):
            return None
        if all(edge in states for edge in anchor_edges):
            if not all({states[edge] for edge in incident[vertex]}
                       == set(COLORS) for vertex in range(8)):
                return None
            counts["avoiding_completions"] += 1
            words = matching_word_histogram(
                edges, target_edge, states, target_support
            )
            pure = tuple(words[(colour,) * 8] for colour in COLORS)
            if not all(pure):
                return None
            counts["pure_supported_completions"] += 1
            singleton_words = tuple(sorted(
                word for word, multiplicity in words.items()
                if len(set(word)) > 1 and multiplicity == 1
            ))
            if singleton_words:
                counts["pure_supported_with_singleton"] += 1
                counts["minimum_singletons"] = min(
                    counts.get("minimum_singletons", len(singleton_words)),
                    len(singleton_words),
                )
                return None
            counts["singleton_free_completions"] += 1
            return {
                "completion": tuple(sorted(states.items())),
                "pure_support": pure,
                "word_histogram": tuple(sorted(words.items())),
            }

        unassigned = tuple(edge for edge in anchor_edges if edge not in states)

        def pressure(edge):
            vertex_pressure = sum(
                3 - len({states[item] for item in incident[vertex]
                         if item in states})
                for vertex in edge
            )
            return (face_frequency[edge], vertex_pressure)

        edge = max(unassigned, key=pressure)
        # In the support-two chart the transposition 1<->2 fixes the missing
        # colour 0.  On the first anchor edge, colour 2 is equivalent to 1.
        colour_choices = ((0, 1) if zero_coordinate == 0
                          and edge == anchor_edges[0] else COLORS)
        for colour in colour_choices:
            states[edge] = colour
            answer = recurse()
            if answer is not None:
                return answer
        del states[edge]
        return None

    witness = recurse()
    return witness, tuple(sorted(counts.items()))


def audit_rank_authorization():
    """Recheck both endpoint sides of the imported binary rank theorem."""
    imported = LANDING.audit_symbolic_rank_construction()
    require(len(imported) == 12,
            ("imported rank chart count changed", len(imported)))
    right_charts = []
    w = tuple(LANDING.variable(index) for index in COLORS)
    for chart in imported:
        direct = chart["direct_colour"]
        first, second = chart["complementary_colours"]
        coordinate = chart["chart_coordinate"]
        matrix, denominator = LANDING.rank_two_matrix(
            direct, first, second, coordinate
        )
        transpose = tuple(tuple(matrix[column][row] for column in COLORS)
                          for row in COLORS)
        right_kernel = tuple(
            LANDING.add(*(LANDING.multiply(
                transpose[row][column], w[column]
            ) for column in COLORS))
            for row in COLORS
        )
        require(right_kernel == (LANDING.zero(),) * 3,
                ("transposed rank chart lost right kernel", chart,
                 right_kernel))
        require(tuple(transpose[index][index] for index in COLORS)
                == (denominator,) * 3,
                ("transposed rank chart lost active diagonal", chart))
        permanent = LANDING.add(
            LANDING.multiply(
                transpose[first][first], transpose[second][second]
            ),
            LANDING.multiply(
                transpose[first][second], transpose[second][first]
            ),
        )
        require(permanent == LANDING.zero(),
                ("transposed rank chart lost permanent zero", chart,
                 permanent))
        right_charts.append({
            "direct_colour": direct,
            "complementary_colours": (first, second),
            "chart_coordinate": coordinate,
            "denominator": denominator,
            "right_kernel": right_kernel,
            "permanent": permanent,
        })
    return {
        "left_charts": imported,
        "right_charts": tuple(right_charts),
        "face_criterion": (
            "all target-containing expansions are killed by the X-kernel; "
            "the two residue monomials are killed when cap direct colour a "
            "and both residue shores use the complementary colours b,c"
        ),
    }


def audit_binary_cover():
    terminal_records = ORBIT.terminal_two_rrx_records()
    ORBIT.terminal_two_rrx_records = lambda: terminal_records
    prototype_audit = PROTOTYPE.audit_all_orbits()
    route_orbits = Counter()
    route_incidences = Counter()
    binary_face_count = Counter()
    solver_nodes = Counter()
    guard_chart_count = Counter()
    exact_guard_chart_count = Counter()
    exact_guard_totals = Counter()
    final_route_orbits = Counter()
    final_route_incidences = Counter()
    ledgers = []

    for item in prototype_audit["graph_ledgers"]:
        if item["route"] == "forced-distinct-two-cap":
            route = "original-two-cap"
            route_orbits[route] += 1
            route_incidences[route] += item["orbit_size"]
            final_route_orbits[route] += 1
            final_route_incidences[route] += item["orbit_size"]
            continue
        if item["private_face_count"]:
            route = "complete-private-cap"
            route_orbits[route] += 1
            route_incidences[route] += item["orbit_size"]
            final_route_orbits[route] += 1
            final_route_incidences[route] += item["orbit_size"]
            continue
        if len(item["prototype_faces"]) >= 2:
            route = "pure-normalization-collision-exit"
            route_orbits[route] += 1
            route_incidences[route] += item["orbit_size"]
            final_route_orbits[route] += 1
            final_route_incidences[route] += item["orbit_size"]
            continue

        record = terminal_records[item["graph_index"]]
        edges = tuple(record["representative_edges"])
        adjacency = ORBIT.adjacency_from_edges(edges)
        faces = binary_faces(
            adjacency, edges, item["incidence"],
            item["all_source_response_shapes"]
        )
        binary_face_count[len(faces)] += 1
        guards = {}
        exact_guards = {}
        exact_counts = {}
        for chart_name, zero_coordinate in (
                ("support-two", 0), ("support-three", None)):
            guard, visited = avoiding_completion(
                edges, item["incidence"][1], faces, zero_coordinate
            )
            solver_nodes[chart_name] += visited
            guards[chart_name] = guard
            if guard is not None:
                guard_chart_count[chart_name] += 1
            exact_guard, source_counts = exact_source_guard_completion(
                edges, item["incidence"][1], faces, zero_coordinate
            )
            exact_guards[chart_name] = exact_guard
            exact_counts[chart_name] = source_counts
            exact_guard_totals.update(dict(source_counts))
            if exact_guard is not None:
                exact_guard_chart_count[chart_name] += 1
        if all(guard is None for guard in guards.values()):
            route = "all-binary-residue-two-cap"
        else:
            route = "binary-residue-anchor-guard"
        route_orbits[route] += 1
        route_incidences[route] += item["orbit_size"]
        if all(exact_guard is None for exact_guard in exact_guards.values()):
            final_route = "binary-cap-or-normalization/singleton"
        else:
            final_route = "exact-source-necessary-counterguard"
        final_route_orbits[final_route] += 1
        final_route_incidences[final_route] += item["orbit_size"]
        ledgers.append({
            "graph_index": item["graph_index"],
            "orbit_size": item["orbit_size"],
            "incidence": item["incidence"],
            "role": item["role"],
            "near_degree": item["near_degree"],
            "all_source_response_shapes": item[
                "all_source_response_shapes"
            ],
            "binary_faces": faces,
            "guard_support_two": guards["support-two"],
            "guard_support_three": guards["support-three"],
            "exact_guard_support_two": exact_guards["support-two"],
            "exact_guard_support_three": exact_guards["support-three"],
            "exact_guard_counts_support_two": exact_counts["support-two"],
            "exact_guard_counts_support_three": exact_counts["support-three"],
            "route": route,
            "final_route": final_route,
        })

    require(exact_guard_chart_count == Counter(),
            ("an exact-source necessary binary guard survived",
             exact_guard_chart_count))
    require(final_route_orbits == Counter({
        "original-two-cap": 22,
        "complete-private-cap": 110,
        "pure-normalization-collision-exit": 1,
        "binary-cap-or-normalization/singleton": 148,
    }), ("final directed-orbit route partition changed",
         final_route_orbits))
    require(final_route_incidences == Counter({
        "original-two-cap": 25,
        "complete-private-cap": 153,
        "pure-normalization-collision-exit": 1,
        "binary-cap-or-normalization/singleton": 197,
    }), ("final directed-incidence route partition changed",
         final_route_incidences))

    # Freeze the smallest local obstruction to both private and binary-cap
    # landing: it has only two cap occurrences, and both residues have four
    # monomials.  Its displayed anchor guard is nevertheless killed by twelve
    # singleton mixed fibres, so it is not an exact source counterexample.
    local_guard = next(
        item for item in ledgers
        if item["graph_index"] == 11
        and item["incidence"] == (2, (0, 2))
    )
    require(local_guard["orbit_size"] == 2
            and local_guard["role"] == "shared"
            and local_guard["near_degree"] == 4
            and local_guard["binary_faces"] == ()
            and local_guard["all_source_response_shapes"]
            == (((2, 4), 12, 4), ((2, 5), 4, 4)),
            ("smallest four-residue local guard changed", local_guard))
    local_edges = tuple(
        terminal_records[local_guard["graph_index"]]["representative_edges"]
    )
    local_states = dict(local_guard["guard_support_two"])
    local_words = matching_word_histogram(
        local_edges, local_guard["incidence"][1], local_states, (1, 2)
    )
    local_pure = tuple(local_words[(colour,) * 8] for colour in COLORS)
    local_singletons = tuple(sorted(
        word for word, multiplicity in local_words.items()
        if len(set(word)) > 1 and multiplicity == 1
    ))
    require(local_pure == (1, 1, 1) and len(local_singletons) == 12,
            ("smallest guard row profile changed", local_pure,
             local_singletons, local_words))
    adjacency = ORBIT.adjacency_from_edges(local_edges)
    local_response_faces = tuple(
        (
            cap_edge,
            tuple(ORBIT.monomial_names(term) for term in ORBIT.response_terms(
                adjacency, local_edges, cap_edge
            )),
        )
        for cap_edge, _through, _residue in (
            local_guard["all_source_response_shapes"]
        )
    )
    smallest_local_guard = {
        "graph_index": local_guard["graph_index"],
        "orbit_size": local_guard["orbit_size"],
        "representative_edges": local_edges,
        "incidence": local_guard["incidence"],
        "role": local_guard["role"],
        "response_shapes": local_guard["all_source_response_shapes"],
        "factor_level_response_faces": local_response_faces,
        "support_two_anchor_guard": local_guard["guard_support_two"],
        "pure_occurrence_counts": local_pure,
        "singleton_mixed_words": local_singletons,
        "higher_support_warning": (
            "the four-monomial local residues persist under adding terms to "
            "these faces, but any higher-support exact source must add a mate "
            "for every displayed singleton or create a new cap landing"
        ),
    }

    return {
        "route_orbits": tuple(sorted(route_orbits.items())),
        "route_incidences": tuple(sorted(route_incidences.items())),
        "final_route_orbits": tuple(sorted(final_route_orbits.items())),
        "final_route_incidences": tuple(
            sorted(final_route_incidences.items())
        ),
        "binary_face_count_on_148": tuple(sorted(binary_face_count.items())),
        "guard_chart_count": tuple(sorted(guard_chart_count.items())),
        "exact_guard_chart_count": tuple(
            sorted(exact_guard_chart_count.items())
        ),
        "exact_guard_totals": tuple(sorted(exact_guard_totals.items())),
        "solver_nodes": tuple(sorted(solver_nodes.items())),
        "smallest_local_guard": smallest_local_guard,
        "candidate_ledgers": tuple(ledgers),
    }


def canonical(value):
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    ledger = canonical({
        "rank_authorization": audit_rank_authorization(),
        "binary_cover": audit_binary_cover(),
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("all-binary-residue cover ledger changed", digest))
    cover = dict(ledger["binary_cover"]["route_orbits"])
    guards = cover.get("binary-residue-anchor-guard", 0)
    exits = cover.get("all-binary-residue-two-cap", 0)
    print("N=8 support-16 all-binary-residue two-cap cover: PASS")
    print("  new binary-residue exits:", exits)
    print("  finite anchor guards:", guards)
    print("  exact-source necessary guards:",
          ledger["binary_cover"]["exact_guard_chart_count"])
    print("  exact-source completion totals:",
          ledger["binary_cover"]["exact_guard_totals"])
    print("  binary faces on prior 148:",
          ledger["binary_cover"]["binary_face_count_on_148"])


if __name__ == "__main__":
    main()
