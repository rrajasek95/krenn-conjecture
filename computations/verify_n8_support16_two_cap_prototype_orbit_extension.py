#!/usr/bin/env python3
"""Classify support-16 orbits reached by the shared20 two-cap prototype.

A prototype-compatible cap face has, after expanding every response factor
into oriented source-star contractions, exactly two monomials through the
chosen directed nonanchor and exactly two companion monomials.  The companion
pair is a crossed 2x2 permanent on two source-star edges at each cap endpoint.

If the target endpoint has at most one other non-prototype edge, the three
anchor colours force two prototype caps to have distinct direct colours.
The shared20 rank construction then lands every noncoordinate near vector.
For every residual stabilizer orbit this checker constructs a full graph
edge-colouring (target nonanchor, every other edge a coordinate anchor) in
which all prototype direct colours coincide.  Thus the residual is a genuine
global anchor-completion guard, not only a local star possibility.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "cb0f94826af7d3119eb11f4b59022797951b18767efae1095d417426d8d89be2"
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


ORBIT = load_local(
    "n8_support16_source_orbits_for_prototype_extension",
    "verify_n8_support16_directed_incidence_response_orbits.py",
)
LANDING = load_local(
    "n8_support16_shared20_for_prototype_extension",
    "verify_n8_support16_shared20_two_cap_rank_landing.py",
)


def cap_shape(adjacency, edges, incidence, cap_edge):
    expanded = ORBIT.expanded_response_monomials(
        adjacency, edges, cap_edge
    )
    through = tuple(
        item for item in expanded
        if ORBIT.contains_directed_star(item, incidence)
    )
    residue = tuple(
        item for item in expanded
        if not ORBIT.contains_directed_star(item, incidence)
    )
    return through, residue


def endpoint_star_set(orientations, endpoint):
    return tuple(sorted(
        tuple(sorted((site, external)))
        for star_pair in orientations
        for site, external in star_pair if site == endpoint
    ))


def audit_prototype_crossed_shape(cap_edge, residue):
    """Check the two residues use the same two stars on both shores."""
    require(len(residue) == 2,
            ("prototype residue count changed", cap_edge, residue))
    p, q = cap_edge
    shore_ledgers = tuple(
        (
            endpoint_star_set(item[-1], p),
            endpoint_star_set(item[-1], q),
        )
        for item in residue
    )
    require(len(set(shore_ledgers)) == 1,
            ("prototype residue is not a crossed pairing",
             cap_edge, shore_ledgers))
    require(all(len(stars) == 2 for stars in shore_ledgers[0]),
            ("prototype shore did not retain two stars",
             cap_edge, shore_ledgers))
    return shore_ledgers[0]


def collision_completion(edges, target_edge, prototype_caps):
    """Find a full mutual-coordinate completion with one prototype colour.

    The target edge is the sole declared nonanchor.  Every other support edge
    receives one coordinate colour, every vertex sees all three colours, and
    all prototype cap edges are fixed to colour zero.
    """
    prototype_caps = tuple(prototype_caps)
    states = {target_edge: NONANCHOR}
    for edge in prototype_caps:
        states[edge] = 0
    incident = {
        vertex: tuple(edge for edge in edges
                      if vertex in edge and edge != target_edge)
        for vertex in range(8)
    }

    def recurse():
        for vertex in range(8):
            seen = {states[edge] for edge in incident[vertex]
                    if edge in states and states[edge] >= 0}
            remaining = sum(edge not in states for edge in incident[vertex])
            if 3 - len(seen) > remaining:
                return None
        if all(edge in states for edge in edges):
            if all({states[edge] for edge in incident[vertex]}
                   == set(COLORS) for vertex in range(8)):
                return tuple(sorted(states.items()))
            return None

        unassigned = tuple(edge for edge in edges if edge not in states)

        def pressure(edge):
            return sum(
                3 - len({states[item] for item in incident[vertex]
                         if item in states and states[item] >= 0})
                for vertex in edge
            )

        edge = max(unassigned, key=pressure)
        for colour in COLORS:
            states[edge] = colour
            answer = recurse()
            if answer is not None:
                return answer
        del states[edge]
        return None

    answer = recurse()
    if answer is not None:
        direct_colours = {
            dict(answer)[edge] for edge in prototype_caps
        }
        require(len(direct_colours) <= 1,
                ("collision completion split prototype colours", answer))
    return answer


def audit_all_orbits():
    # Import the exact rank theorem rather than restating its construction.
    rank_charts = LANDING.audit_symbolic_rank_construction()
    require(len(rank_charts) == 12,
            ("imported two-cap rank charts changed", len(rank_charts)))

    orbit_audit = ORBIT.audit_orbits()
    prototype_orbit_histogram = Counter()
    prototype_incidence_histogram = Counter()
    route_orbits = Counter()
    route_incidences = Counter()
    forced_role_orbits = Counter()
    forced_role_incidences = Counter()
    compatible_cap_count = 0
    graph_ledgers = []

    for graph_index, orbit, edges in orbit_audit["all_orbits"]:
        adjacency = ORBIT.adjacency_from_edges(edges)
        incidence = orbit["representative"]
        endpoint = incidence[0]
        shapes = []
        prototypes = []
        private_faces = []
        for cap_edge in edges:
            if endpoint not in cap_edge:
                continue
            through, residue = cap_shape(
                adjacency, edges, incidence, cap_edge
            )
            if not through:
                continue
            shape = (len(through), len(residue))
            shapes.append((cap_edge, *shape))
            if not residue:
                private_faces.append(cap_edge)
            if shape == (2, 2):
                shore_stars = audit_prototype_crossed_shape(
                    cap_edge, residue
                )
                prototypes.append((cap_edge, shore_stars))
                compatible_cap_count += 1

        prototype_count = len(prototypes)
        prototype_orbit_histogram[prototype_count] += 1
        prototype_incidence_histogram[prototype_count] += orbit["size"]
        near_degree = adjacency[endpoint].bit_count()
        other_nonprototype_edges = near_degree - 1 - prototype_count
        forced_distinct = other_nonprototype_edges <= 1
        collision = collision_completion(
            edges, incidence[1], tuple(item[0] for item in prototypes)
        )
        if forced_distinct:
            require(prototype_count >= 2,
                    ("forced route lost its two cap tests", graph_index,
                     incidence, prototype_count))
            require(collision is None,
                    ("forced distinct route acquired collision colouring",
                     graph_index, incidence, collision))
            route = "forced-distinct-two-cap"
            forced_role_orbits[orbit["role"]] += 1
            forced_role_incidences[orbit["role"]] += orbit["size"]
        else:
            require(collision is not None,
                    ("residual orbit lacks global collision completion",
                     graph_index, incidence, prototypes))
            route = "same-colour-completion-guard"

        route_orbits[route] += 1
        route_incidences[route] += orbit["size"]
        graph_ledgers.append({
            "graph_index": graph_index,
            "orbit_size": orbit["size"],
            "incidence": incidence,
            "role": orbit["role"],
            "near_degree": near_degree,
            "all_source_response_shapes": tuple(shapes),
            "private_face_count": len(private_faces),
            "prototype_faces": tuple(prototypes),
            "other_nonprototype_edges": other_nonprototype_edges,
            "route": route,
            "collision_completion": collision,
        })

    require(compatible_cap_count == 144,
            ("prototype-compatible cap count changed", compatible_cap_count))
    require(prototype_orbit_histogram == Counter({
        0: 162, 1: 96, 2: 21, 3: 2,
    }), ("prototype orbit histogram changed", prototype_orbit_histogram))
    require(prototype_incidence_histogram == Counter({
        0: 216, 1: 134, 2: 24, 3: 2,
    }), ("prototype incidence histogram changed",
         prototype_incidence_histogram))
    require(route_orbits == Counter({
        "forced-distinct-two-cap": 22,
        "same-colour-completion-guard": 259,
    }), ("prototype route orbit totals changed", route_orbits))
    require(route_incidences == Counter({
        "forced-distinct-two-cap": 25,
        "same-colour-completion-guard": 351,
    }), ("prototype route incidence totals changed", route_incidences))
    require(forced_role_orbits == Counter({
        "shared": 1, "never-private": 21,
    }), ("forced role orbit split changed", forced_role_orbits))
    require(forced_role_incidences == Counter({
        "shared": 1, "never-private": 24,
    }), ("forced role incidence split changed", forced_role_incidences))

    residual_two_test_orbits = sum(
        item["route"] == "same-colour-completion-guard"
        and len(item["prototype_faces"]) >= 2
        for item in graph_ledgers
    )
    residual_two_test_incidences = sum(
        item["orbit_size"]
        for item in graph_ledgers
        if item["route"] == "same-colour-completion-guard"
        and len(item["prototype_faces"]) >= 2
    )
    require((residual_two_test_orbits, residual_two_test_incidences) == (1, 1),
            ("same-colour two-test residual changed",
             residual_two_test_orbits, residual_two_test_incidences))

    return {
        "prototype_compatible_cap_count": compatible_cap_count,
        "prototype_orbit_histogram": tuple(
            sorted(prototype_orbit_histogram.items())
        ),
        "prototype_incidence_histogram": tuple(
            sorted(prototype_incidence_histogram.items())
        ),
        "route_orbits": tuple(sorted(route_orbits.items())),
        "route_incidences": tuple(sorted(route_incidences.items())),
        "forced_role_orbits": tuple(sorted(forced_role_orbits.items())),
        "forced_role_incidences": tuple(
            sorted(forced_role_incidences.items())
        ),
        "residual_with_two_prototype_tests": (
            residual_two_test_orbits, residual_two_test_incidences,
        ),
        "graph_ledgers": tuple(graph_ledgers),
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
    ledger = canonical(audit_all_orbits())
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("two-cap prototype orbit ledger changed", digest))

    print("N=8 support-16 two-cap prototype orbit extension: PASS")
    print("  stabilizer orbits / directed incidences: 281 / 376")
    print("  forced distinct two-cap cover: 22 / 25")
    print("  global same-colour completion guards: 259 / 351")
    print("  residual guards retaining two tests: 1 / 1")
    print("  prototype-compatible representative caps: 144")


if __name__ == "__main__":
    main()
