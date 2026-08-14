#!/usr/bin/env python3
"""Uniform two-RRX tensor theorem and coordinate mixed-fibre closure.

The support-16 census leaves 22 residual orbits with a minimum face having
exactly two RRX matchings and no RRR matching.  This checker proves that all
22 faces have the same overlap-one tensor geometry as the support-15 edge-37
map, imports/rechecks its tensor-rank and anchor-placement classification,
and exhausts the remaining mutual-coordinate exceptional branch.

For that branch, an edge state is either a nonzero scalar coordinate anchor
of colour 0,1,2 or an unrestricted 3x3 wildcard block.  Every vertex must see
all three coordinate anchor colours.  All wildcard cells are granted, so a
unique mixed matching remains unique for every actual specialization.

Most completions have an immediate anchor-only Laurent unit.  In every other
completion, one or two two-term mixed fibres propagate nonvanishing from an
anchor monomial into wildcard cells, after which a one-term mixed fibre forces
their nonzero product to vanish.  This is an exact field argument, independent
of the rank of the exceptional wildcard response block.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "b469342acee94774030bc1b106edefff713b8bff036efb7458eebe6547edc7d2"


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


SUPPORT16 = load_local(
    "n8_support16_for_two_rrx_closure",
    "verify_n8_support16_clean_terminal_census.py",
)
EDGE37 = load_local(
    "n8_edge37_for_two_rrx_closure",
    "verify_n8_support15_edge37_anchor_rank_strata.py",
)

N = 8
COLORS = (0, 1, 2)
NONANCHOR = -1
UNASSIGNED = -2

EXPECTED_TOTALS = (
    1104, 998, 1280, 1296, 998, 1034, 1052, 1034, 1650, 1502, 1660,
    1391, 998, 1034, 1780, 1970, 1966, 1958, 2298, 2011, 1892, 2322,
)
EXPECTED_PROPAGATED = (
    0, 2, 0, 0, 1, 0, 0, 2, 2, 0, 0, 1, 1, 1, 0, 0, 4, 1, 13,
    4, 7, 3,
)


def adjacency_from_edges(edges):
    adjacency = [0] * N
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return tuple(adjacency)


def support_matchings(edges):
    edge_set = set(edges)
    return tuple(
        tuple(tuple(sorted(edge)) for edge in matching)
        for matching in SUPPORT16.BASE.perfect_matchings(tuple(range(N)))
        if all(tuple(sorted(edge)) in edge_set for edge in matching)
    )


def two_rrx_geometry(adjacency, edges, cap_edge):
    """Return the canonical overlap-one roles of a minimum two-RRX face."""
    p, q = cap_edge
    if adjacency[p].bit_count() != 3:
        p, q = q, p
    require((adjacency[p].bit_count(), adjacency[q].bit_count()) == (3, 4),
            ("minimum two-RRX face is not cubic/high", cap_edge))
    p_external = {
        vertex for vertex in range(N)
        if (adjacency[p] >> vertex) & 1
    } - {q}
    q_external = {
        vertex for vertex in range(N)
        if (adjacency[q] >> vertex) & 1
    } - {p}
    overlap = p_external & q_external
    require(len(overlap) == 1,
            ("two-RRX shores lost their common vertex", cap_edge,
             p_external, q_external))
    shared = next(iter(overlap))
    p_private = next(iter(p_external - overlap))
    q_privates = tuple(sorted(q_external - overlap))
    require(len(q_privates) == 2,
            ("high endpoint did not retain two private roles", cap_edge))
    leftover = tuple(sorted(
        set(range(N))
        - {p, q, shared, p_private, *q_privates}
    ))
    require(len(leftover) == 2 and tuple(leftover) in set(edges),
            ("two-RRX common x multiplier changed", cap_edge, leftover))

    response_edges = {
        tuple(sorted((left, right)))
        for left in p_external for right in q_external if left != right
    }
    rows = []
    residual = tuple(v for v in range(N) if v not in (p, q))
    for matching in SUPPORT16.BASE.perfect_matchings(residual):
        matching = tuple(tuple(sorted(edge)) for edge in matching)
        tags = tuple(
            edge for edge in matching
            if edge in set(edges)
            and all(other in response_edges
                    for other in matching if other != edge)
        )
        if tags:
            rows.append((matching, tags))
    require(len(rows) == 2
            and all(tags == (tuple(leftover),) for _matching, tags in rows),
            ("two-RRX matching shape changed", cap_edge, rows))

    expected_response_pairs = {
        frozenset((
            tuple(sorted((shared, q_privates[0]))),
            tuple(sorted((p_private, q_privates[1]))),
        )),
        frozenset((
            tuple(sorted((shared, q_privates[1]))),
            tuple(sorted((p_private, q_privates[0]))),
        )),
    }
    actual_response_pairs = {
        frozenset(edge for edge in matching if edge != tuple(leftover))
        for matching, _tags in rows
    }
    require(actual_response_pairs == expected_response_pairs,
            ("two-RRX crossed pairing changed", cap_edge, rows))
    return {
        "cap_endpoints": (p, q),
        "shared_external": shared,
        "cubic_private": p_private,
        "high_privates": q_privates,
        "common_x_edge": leftover,
        "RRX_rows": rows,
        "tensor_formula": "a0 tensor b1 + a1 tensor b0",
    }


def monomial_for(matching, word, states):
    monomial = []
    for edge in matching:
        state = states[edge]
        if state >= 0:
            if (word[edge[0]], word[edge[1]]) != (state, state):
                return None
            monomial.append(("anchor", edge))
        else:
            monomial.append(
                ("wildcard", edge, word[edge[0]], word[edge[1]])
            )
    return tuple(sorted(monomial, key=str))


def immediate_anchor_unit(matchings, states):
    """Find a mixed anchor matching unique even with all wildcard cells."""
    for matching in matchings:
        if any(states[edge] < 0 for edge in matching):
            continue
        word = [None] * N
        for edge in matching:
            for vertex in edge:
                word[vertex] = states[edge]
        require(all(value is not None for value in word),
                ("matching stopped covering vertices", matching))
        if len(set(word)) == 1:
            continue
        compatible = tuple(
            other for other in matchings
            if all(
                states[edge] < 0
                or (word[edge[0]], word[edge[1]])
                   == (states[edge], states[edge])
                for edge in other
            )
        )
        if len(compatible) == 1:
            require(compatible[0] == matching,
                    ("unique matching changed identity", matching, compatible))
            return {
                "word": "".join(map(str, word)),
                "matching": matching,
                "laurent_unit": tuple(
                    "t" + "".join(map(str, edge)) for edge in matching
                ),
            }
    return None


def sparse_mixed_rows(matchings, states):
    rows = []
    for word in product(COLORS, repeat=N):
        if len(set(word)) == 1:
            continue
        monomials = tuple(
            monomial for matching in matchings
            if (monomial := monomial_for(matching, word, states)) is not None
        )
        if len(monomials) in (1, 2):
            rows.append(("".join(map(str, word)), monomials))
    return tuple(rows)


def binomial_singleton_certificate(matchings, states):
    """Propagate nonzero monomials until a singleton row contradicts them."""
    rows = sparse_mixed_rows(matchings, states)
    known_nonzero = {
        ("anchor", edge) for edge, state in states.items() if state >= 0
    }
    used_words = set()
    propagation = []
    while True:
        singleton = next((
            (word, monomials[0]) for word, monomials in rows
            if len(monomials) == 1
            and all(variable in known_nonzero for variable in monomials[0])
        ), None)
        if singleton is not None:
            require(1 <= len(propagation) <= 2,
                    ("mixed propagation length changed", propagation,
                     singleton))
            return {
                "binomial_nonzero_propagation": tuple(propagation),
                "singleton_zero_contradiction": singleton,
            }

        next_row = next((
            (word, monomials) for word, monomials in rows
            if len(monomials) == 2 and word not in used_words
            and any(
                all(variable in known_nonzero for variable in monomial)
                for monomial in monomials
            )
        ), None)
        require(next_row is not None,
                ("coordinate completion escaped mixed propagation",
                 tuple(sorted(states.items())), propagation))
        word, monomials = next_row
        used_words.add(word)
        known_nonzero.update(monomials[0])
        known_nonzero.update(monomials[1])
        propagation.append(next_row)


def enumerate_coordinate_completions(edges, geometry):
    adjacency_edges = {
        vertex: tuple(edge for edge in edges if vertex in edge)
        for vertex in range(N)
    }
    p, q = geometry["cap_endpoints"]
    shared = geometry["shared_external"]
    p_private = geometry["cubic_private"]
    high0, high1 = geometry["high_privates"]
    matchings = support_matchings(edges)

    variants = []
    immediate_count = 0
    propagated_count = 0
    propagation_lengths = Counter()
    sample_propagation = None
    for anchored_high, wildcard_high in ((high0, high1), (high1, high0)):
        for anchored_colour in (0, 1):
            fixed = {
                tuple(sorted((p, q))): 2,
                tuple(sorted((p, shared))): 0,
                tuple(sorted((p, p_private))): 1,
                tuple(sorted((q, anchored_high))): anchored_colour,
                tuple(sorted((q, shared))): 1 - anchored_colour,
                tuple(sorted((q, wildcard_high))): NONANCHOR,
            }
            require(len(fixed) == 6 and set(fixed) <= set(edges),
                    ("exceptional local role collision", geometry, fixed))
            states = {edge: UNASSIGNED for edge in edges}
            states.update(fixed)
            free_edges = tuple(edge for edge in edges
                               if states[edge] == UNASSIGNED)
            completion_count = 0
            immediate_variant = 0
            propagated_variant = 0

            def recurse(index):
                nonlocal completion_count, immediate_count, propagated_count
                nonlocal immediate_variant, propagated_variant
                nonlocal sample_propagation
                for vertex in range(N):
                    incident = adjacency_edges[vertex]
                    seen = {states[edge] for edge in incident
                            if states[edge] >= 0}
                    remaining = sum(states[edge] == UNASSIGNED
                                    for edge in incident)
                    if 3 - len(seen) > remaining:
                        return
                if index == len(free_edges):
                    require(all(states[edge] != UNASSIGNED for edge in edges),
                            "completed state retained an unassigned edge")
                    if any(
                        {states[edge] for edge in adjacency_edges[vertex]
                         if states[edge] >= 0} != set(COLORS)
                        for vertex in range(N)
                    ):
                        return
                    completion_count += 1
                    unit = immediate_anchor_unit(matchings, states)
                    if unit is not None:
                        immediate_count += 1
                        immediate_variant += 1
                        return
                    certificate = binomial_singleton_certificate(
                        matchings, states
                    )
                    propagated_count += 1
                    propagated_variant += 1
                    length = len(certificate["binomial_nonzero_propagation"])
                    propagation_lengths[length] += 1
                    if sample_propagation is None:
                        sample_propagation = {
                            "states": tuple(sorted(states.items())),
                            "certificate": certificate,
                        }
                    return

                edge = free_edges[index]
                for state in (NONANCHOR, *COLORS):
                    states[edge] = state
                    recurse(index + 1)
                states[edge] = UNASSIGNED

            recurse(0)
            variants.append({
                "anchored_high_vertex": anchored_high,
                "anchored_colour": anchored_colour,
                "completion_count": completion_count,
                "immediate_anchor_units": immediate_variant,
                "propagated_mixed_contradictions": propagated_variant,
            })

    return {
        "support_matching_count": len(matchings),
        "variants": tuple(variants),
        "completion_count": sum(item["completion_count"] for item in variants),
        "immediate_anchor_units": immediate_count,
        "propagated_mixed_contradictions": propagated_count,
        "propagation_lengths": dict(propagation_lengths),
        "sample_propagation": sample_propagation,
    }


def three_rrx_geometry(adjacency, edges, cap_edge):
    p, q = cap_edge
    require(adjacency[p].bit_count() == adjacency[q].bit_count() == 4,
            ("seal-three cap stopped being degree four/four", cap_edge))
    p_external = {
        v for v in range(N) if (adjacency[p] >> v) & 1
    } - {q}
    q_external = {
        v for v in range(N) if (adjacency[q] >> v) & 1
    } - {p}
    require(len(p_external & q_external) == 2,
            ("seal-three overlap changed", cap_edge, p_external, q_external))
    leftover = tuple(sorted(
        set(range(N)) - {p, q} - p_external - q_external
    ))
    require(len(leftover) == 2 and tuple(leftover) in set(edges),
            ("seal-three common x changed", cap_edge, leftover))
    response = {
        tuple(sorted((u, v)))
        for u in p_external for v in q_external if u != v
    }
    rows = []
    residual = tuple(v for v in range(N) if v not in cap_edge)
    for matching in SUPPORT16.BASE.perfect_matchings(residual):
        matching = tuple(tuple(sorted(edge)) for edge in matching)
        tags = tuple(
            edge for edge in matching
            if edge in set(edges)
            and all(other in response for other in matching if other != edge)
        )
        if tags:
            rows.append((matching, tags))
    require(len(rows) == 3
            and all(tags == (tuple(leftover),) for _matching, tags in rows),
            ("seal-three RRX rows changed", cap_edge, rows))
    return {
        "cap_edge": cap_edge,
        "external_shores": (tuple(sorted(p_external)),
                            tuple(sorted(q_external))),
        "overlap": tuple(sorted(p_external & q_external)),
        "common_x_edge": leftover,
        "RRX_rows": rows,
        "next_map": "x times the three matching quadratic on four vertices",
    }


def audit_uniform_closure():
    support16 = SUPPORT16.audit_census_and_orbits()
    two_faces = tuple(
        record for record in support16["terminal_orbits"]
        if record["route"] == "unresolved"
        and record["exit_data"]["minimum_response"][0] == 2
    )
    three_faces = tuple(
        record for record in support16["terminal_orbits"]
        if record["route"] == "unresolved"
        and record["exit_data"]["minimum_response"][0] == 3
    )
    require((len(two_faces), len(three_faces)) == (22, 4),
            ("support-16 residual split changed", len(two_faces),
             len(three_faces)))

    two_ledger = []
    totals = []
    propagated = []
    for record in two_faces:
        edges = tuple(record["representative_edges"])
        adjacency = adjacency_from_edges(edges)
        cap_edge = record["exit_data"]["minimum_response"][-1]
        geometry = two_rrx_geometry(adjacency, edges, cap_edge)
        closure = enumerate_coordinate_completions(edges, geometry)
        totals.append(closure["completion_count"])
        propagated.append(closure["propagated_mixed_contradictions"])
        two_ledger.append({
            "degree_sequence": record["degree_sequence"],
            "orbit_size": record["orbit_size"],
            "triangles": record["triangles"],
            "squares": record["squares"],
            "representative_edges": edges,
            "geometry": geometry,
            "coordinate_closure": closure,
        })
    require(tuple(totals) == EXPECTED_TOTALS,
            ("coordinate completion totals changed", totals))
    require(tuple(propagated) == EXPECTED_PROPAGATED,
            ("mixed propagation counts changed", propagated))
    require(sum(totals) == 33228
            and sum(propagated) == 42
            and sum(totals) - sum(propagated) == 33186,
            ("coordinate closure grand totals changed", sum(totals),
             sum(propagated)))
    propagation_histogram = Counter()
    for item in two_ledger:
        propagation_histogram.update(
            item["coordinate_closure"]["propagation_lengths"]
        )
    require(propagation_histogram == Counter({1: 39, 2: 3}),
            ("mixed propagation length histogram changed",
             propagation_histogram))

    # The two genuinely new degree-sequence-minimal orbits do not have an
    # edge deletion into the support-15 terminal, so their closure above is
    # not borrowed from the old theorem.
    first_two = tuple(
        (item["orbit_size"], item["coordinate_closure"]["completion_count"],
         item["coordinate_closure"]["propagated_mixed_contradictions"])
        for item in two_ledger
        if item["degree_sequence"] == (6, 4, 4, 4, 4, 4, 3, 3)
    )
    require(first_two == ((60, 1104, 0), (240, 998, 2)),
            ("first two orbit closure changed", first_two))
    require(all(
        record["exit_data"]["support15_terminal_deletions"] == 0
        for record in two_faces
        if record["degree_sequence"] == (6, 4, 4, 4, 4, 4, 3, 3)
    ), "first support-16 residual unexpectedly acquired support-15 deletion")

    three_ledger = []
    for record in three_faces:
        edges = tuple(record["representative_edges"])
        adjacency = adjacency_from_edges(edges)
        cap_edge = record["exit_data"]["minimum_response"][-1]
        three_ledger.append({
            "degree_sequence": record["degree_sequence"],
            "orbit_size": record["orbit_size"],
            "triangles": record["triangles"],
            "squares": record["squares"],
            "representative_edges": edges,
            "geometry": three_rrx_geometry(adjacency, edges, cap_edge),
        })
    signatures = {
        (item["degree_sequence"], item["orbit_size"],
         item["triangles"], item["squares"])
        for item in three_ledger
    }
    require(signatures == {
        ((5, 4, 4, 4, 4, 4, 4, 3), 360, 6, 16),
        ((4, 4, 4, 4, 4, 4, 4, 4), 840, 8, 12),
        ((4, 4, 4, 4, 4, 4, 4, 4), 2520, 8, 10),
        ((4, 4, 4, 4, 4, 4, 4, 4), 10080, 6, 14),
    }, ("seal-three residual signatures changed", signatures))

    return {
        "two_rrx_orbits": two_ledger,
        "coordinate_completion_total": sum(totals),
        "immediate_anchor_unit_total": sum(totals) - sum(propagated),
        "binomial_singleton_total": sum(propagated),
        "propagation_length_histogram": dict(propagation_histogram),
        "first_two_new_orbits": first_two,
        "three_rrx_residuals": three_ledger,
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
    tensor_rank = EDGE37.audit_tensor_rank_classification()
    rank_one = EDGE37.audit_rank_one_cap_and_saturation()
    anchor_strata = EDGE37.audit_anchor_placement_and_rank_strata()
    require(tensor_rank["zero_tensor_cases"] == 417,
            "imported tensor-rank classification changed")
    require(rank_one["saturation_certificate"].startswith("2*(K00*K11)^2"),
            "imported exceptional saturation certificate changed")
    require(len(anchor_strata["anchor_placements"]) == 5,
            "imported degree-four anchor-placement count changed")

    ledger = canonical({
        "imported_tensor_rank": tensor_rank,
        "imported_rank_one_and_saturation": rank_one,
        "imported_anchor_strata": anchor_strata,
        "uniform_support16_closure": audit_uniform_closure(),
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("support-16 two-RRX closure ledger changed", digest))

    print("N=8 support-16 two-RRX coordinate mixed closure: PASS")
    print("  uniform two-RRX tensor faces: 22")
    print("  normalized coordinate completions: 33228")
    print("  immediate mixed Laurent units: 33186")
    print("  binomial-to-singleton contradictions: 42")
    print("  binomial propagation lengths 1 / 2: 39 / 3")
    print("  first (6,4^5,3^2) orbits closed: 2 / 2")
    print("  remaining seal-three graph orbits: 4")


if __name__ == "__main__":
    main()
