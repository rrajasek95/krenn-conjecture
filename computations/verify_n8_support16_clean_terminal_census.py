#!/usr/bin/env python3
"""Exact support-16 clean-cap terminal census at N=8.

This is the next support layer after the support-15 census.  It enumerates
all labelled simple graphs of minimum degree at least three, applies the
coefficient-independent RRR/RRX clean test, quotients the terminals by their
literal degree-preserving permutation groups, and applies two already proved
exits:

* an independent four-shore is impossible for an exact ternary source;
* a degree-three--degree-three cap edge has the forced-anchor 2x2 permanent
  active zero whenever its two external shores are disjoint and the leftover
  pair is live.

No coefficient specialization is used on the remaining orbits.  Their exact
response-support profiles and representatives are frozen for the next layer.
Standard library only; all checks survive python -O and python -I -S.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "9c5822cf40b770a60c76470f51887033c708e174e1cb1bacd6e729f073b6f4ae"


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


BASE = load_local(
    "n8_support_base_for_support16",
    "verify_n8_support_rank_minimal_projective_cap_error_counterguard.py",
)
SUPPORT15 = load_local(
    "n8_support15_for_support16",
    "verify_n8_support15_clean_terminal_census.py",
)
NO_INDEPENDENT = load_local(
    "n8_no_independent_four_for_support16",
    "verify_no_independent_four_set_at_eight.py",
)

N = 8
IDENTITY = tuple(range(N))


def excess_partitions(total, length, maximum, upper=None):
    """Nonincreasing partitions, padded with zeroes to exact length."""
    if upper is None:
        upper = maximum
    if length == 0:
        return ((),) if total == 0 else ()
    answer = []
    for head in range(min(upper, maximum, total), -1, -1):
        for tail in excess_partitions(
                total - head, length - 1, maximum, head):
            answer.append((head,) + tail)
    return tuple(answer)


DEGREE_SEQUENCES = tuple(
    tuple(3 + excess for excess in partition)
    for partition in excess_partitions(8, N, 4)
)

# labelled count, clean-edge distribution, support-terminal count
EXPECTED_CENSUS = {
    (7, 7, 3, 3, 3, 3, 3, 3): (15, {3: 15}, 0),
    (7, 6, 4, 3, 3, 3, 3, 3): (100, {1: 10, 3: 60, 4: 30}, 0),
    (7, 5, 5, 3, 3, 3, 3, 3): (170, {1: 20, 2: 90, 4: 60}, 0),
    (7, 5, 4, 4, 3, 3, 3, 3): (
        312, {2: 60, 3: 126, 4: 102, 5: 24}, 0,
    ),
    (7, 4, 4, 4, 4, 3, 3, 3): (
        553, {0: 24, 2: 144, 3: 204, 4: 144, 6: 36, 9: 1}, 24,
    ),
    (6, 6, 5, 3, 3, 3, 3, 3): (
        381, {1: 50, 2: 180, 3: 120, 4: 30, 15: 1}, 0,
    ),
    (6, 6, 4, 4, 3, 3, 3, 3): (
        710, {1: 44, 2: 180, 3: 420, 4: 18, 5: 48}, 0,
    ),
    (6, 5, 5, 4, 3, 3, 3, 3): (
        1262, {0: 48, 1: 32, 2: 624, 3: 498, 4: 60}, 48,
    ),
    (6, 5, 4, 4, 4, 3, 3, 3): (
        2265, {0: 108, 1: 387, 2: 1080, 3: 612,
               4: 36, 5: 12, 6: 30}, 108,
    ),
    (6, 4, 4, 4, 4, 4, 3, 3): (
        3920, {0: 480, 1: 1320, 2: 1290, 3: 780, 6: 50}, 480,
    ),
    (5, 5, 5, 5, 3, 3, 3, 3): (
        2286, {0: 144, 1: 360, 2: 1206, 3: 576}, 144,
    ),
    (5, 5, 5, 4, 4, 3, 3, 3): (
        4078, {0: 390, 1: 1378, 2: 1809, 3: 486, 4: 15}, 390,
    ),
    (5, 5, 4, 4, 4, 4, 3, 3): (
        7012, {0: 1416, 1: 3332, 2: 1878, 3: 318,
               4: 48, 6: 20}, 1416,
    ),
    (5, 4, 4, 4, 4, 4, 4, 3): (
        11760, {0: 4860, 1: 4740, 2: 1980, 3: 180}, 4860,
    ),
    (4, 4, 4, 4, 4, 4, 4, 4): (
        19355, {0: 13475, 1: 3360, 2: 2520}, 13475,
    ),
}

# independent-shore, cubic-permanent, unresolved orbit counts
EXPECTED_ROUTES = {
    (7, 4, 4, 4, 4, 3, 3, 3): (1, 0, 0),
    (6, 5, 5, 4, 3, 3, 3, 3): (2, 0, 0),
    (6, 5, 4, 4, 4, 3, 3, 3): (3, 1, 0),
    (6, 4, 4, 4, 4, 4, 3, 3): (1, 1, 2),
    (5, 5, 5, 5, 3, 3, 3, 3): (1, 1, 0),
    (5, 5, 5, 4, 4, 3, 3, 3): (3, 5, 0),
    (5, 5, 4, 4, 4, 4, 3, 3): (3, 8, 12),
    (5, 4, 4, 4, 4, 4, 4, 3): (0, 0, 9),
    (4, 4, 4, 4, 4, 4, 4, 4): (1, 0, 3),
}

FIRST_RESIDUALS = (
    (
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 6), (0, 7),
        (1, 4), (1, 5), (1, 7), (2, 3), (2, 5), (2, 7),
        (3, 5), (3, 6), (4, 5), (4, 6),
    ),
    (
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 7),
        (1, 4), (1, 6), (1, 7), (2, 3), (2, 5), (2, 7),
        (3, 5), (3, 6), (4, 5), (4, 6),
    ),
)


def support15_unresolved_masks():
    adjacency = [0] * N
    for u, v in SUPPORT15.UNRESOLVED_EDGES:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    adjacency = tuple(adjacency)
    return frozenset(
        BASE.permuted_edge_mask(adjacency, permutation)
        for permutation in permutations(range(N))
    )


def delete_edge(adjacency, edge):
    u, v = edge
    answer = list(adjacency)
    answer[u] &= ~(1 << v)
    answer[v] &= ~(1 << u)
    return tuple(answer)


def response_profile(adjacency, edges):
    rows = []
    for edge in edges:
        rrr, rrx, rrx_matchings, _p_external, _q_external = (
            SUPPORT15.response_counts(adjacency, edge)
        )
        degree_pair = tuple(sorted(
            (adjacency[edge[0]].bit_count(), adjacency[edge[1]].bit_count())
        ))
        rows.append((degree_pair, rrr, rrx, rrx_matchings))
    return tuple(sorted(Counter(rows).items(), key=str))


def minimum_response(adjacency, edges):
    rows = []
    for edge in edges:
        rrr, rrx, rrx_matchings, _p_external, _q_external = (
            SUPPORT15.response_counts(adjacency, edge)
        )
        degree_pair = tuple(sorted(
            (adjacency[edge[0]].bit_count(), adjacency[edge[1]].bit_count())
        ))
        rows.append((rrr + rrx_matchings, rrr, rrx_matchings,
                     rrx, degree_pair, edge))
    return min(rows)


def independent_exit(adjacency, edges, independent_sets):
    shore = frozenset(min(independent_sets))
    complement = frozenset(range(N)) - shore
    cross = {
        tuple(sorted((left, right)))
        for left in shore for right in complement
    }
    live_cross = set(edges) & cross
    dead_cross = cross - live_cross
    internal = set(edges) - live_cross
    return {
        "shore": tuple(sorted(shore)),
        "live_cross": tuple(sorted(live_cross)),
        "dead_cross": tuple(sorted(dead_cross)),
        "zeroed_complement_internal": tuple(sorted(internal)),
    }


def permanent_exit(adjacency, edges):
    cubic_edges = tuple(
        edge for edge in edges
        if adjacency[edge[0]].bit_count() == adjacency[edge[1]].bit_count() == 3
    )
    for edge in cubic_edges:
        rrr, rrx, rrx_matchings, p_external, q_external = (
            SUPPORT15.response_counts(adjacency, edge)
        )
        leftover = (
            set(range(N)) - set(edge) - p_external - q_external
        )
        if (rrr == 0 and not (p_external & q_external)
                and len(leftover) == 2
                and tuple(sorted(leftover)) in set(edges)):
            require((rrx, rrx_matchings) == (2, 2),
                    ("cubic permanent acquired extra seals", edge, rrx,
                     rrx_matchings))
            return {
                "cap_edge": edge,
                "external_shores": (
                    tuple(sorted(p_external)), tuple(sorted(q_external)),
                ),
                "active_x_edge": tuple(sorted(leftover)),
            }
    return None


def audit_census_and_orbits():
    require(len(DEGREE_SEQUENCES) == 15,
            ("degree-sequence partition count changed", DEGREE_SEQUENCES))
    census = []
    orbits = []
    route_counter = Counter()
    route_by_sequence = Counter()
    unresolved_by_sequence = Counter()
    independent_cross_histogram = Counter()
    unresolved_minimum_histogram = Counter()
    unresolved_support15_extension_orbits = 0
    unresolved_support15_deletion_directions = 0
    unresolved_records = []
    old_terminal_masks = support15_unresolved_masks()

    for target in DEGREE_SEQUENCES:
        labelled_count = 0
        distribution = Counter()
        terminals = []
        for adjacency in BASE.generate_degree_sequence_graphs(target):
            labelled_count += 1
            edges = BASE.graph_edges(adjacency)
            require(len(edges) == 16,
                    ("support-16 edge count changed", target, edges))
            clean_count = sum(
                BASE.response_support_clean_edge(adjacency, *edge)
                for edge in edges
            )
            distribution[clean_count] += 1
            if clean_count == 0:
                terminals.append(adjacency)

        expected_count, expected_distribution, expected_terminals = (
            EXPECTED_CENSUS[target]
        )
        require(
            (labelled_count, dict(distribution), len(terminals))
            == (expected_count, expected_distribution, expected_terminals),
            ("support-16 labelled census changed", target, labelled_count,
             distribution, len(terminals)),
        )
        census.append({
            "degree_sequence": target,
            "labelled_count": labelled_count,
            "clean_edge_distribution": dict(distribution),
            "terminal_count": len(terminals),
        })
        if not terminals:
            continue

        group = SUPPORT15.preserving_group(target)
        all_masks = {
            BASE.permuted_edge_mask(graph, IDENTITY): graph
            for graph in terminals
        }
        terminal_mask_set = frozenset(all_masks)
        local_routes = Counter()
        while all_masks:
            representative_mask = min(all_masks)
            adjacency = all_masks[representative_mask]
            orbit = frozenset(
                BASE.permuted_edge_mask(adjacency, permutation)
                for permutation in group
            )
            require(orbit <= terminal_mask_set,
                    ("degree-preserving orbit left terminal set", target))
            for mask in orbit:
                all_masks.pop(mask, None)

            edges = BASE.graph_edges(adjacency)
            independent_sets = SUPPORT15.independent_four_sets(adjacency)
            exit_data = None
            if independent_sets:
                route = "independent four-shore full-row exclusion"
                exit_data = independent_exit(adjacency, edges, independent_sets)
                cross_key = (
                    len(exit_data["live_cross"]),
                    len(exit_data["dead_cross"]),
                    len(exit_data["zeroed_complement_internal"]),
                )
                independent_cross_histogram[cross_key] += 1
            else:
                exit_data = permanent_exit(adjacency, edges)
                if exit_data is not None:
                    route = "cubic-cubic forced-anchor permanent zero"
                else:
                    route = "unresolved"
                    unresolved_by_sequence[target] += 1
                    minimum = minimum_response(adjacency, edges)
                    unresolved_minimum_histogram[minimum[0]] += 1
                    deletion_count = sum(
                        BASE.permuted_edge_mask(
                            delete_edge(adjacency, edge), IDENTITY
                        ) in old_terminal_masks
                        for edge in edges
                    )
                    if deletion_count:
                        unresolved_support15_extension_orbits += 1
                        unresolved_support15_deletion_directions += deletion_count
                    exit_data = {
                        "minimum_response": minimum,
                        "response_profile": response_profile(adjacency, edges),
                        "support15_terminal_deletions": deletion_count,
                    }

            route_counter[route] += 1
            local_routes[route] += 1
            record = {
                "degree_sequence": target,
                "orbit_size": len(orbit),
                "triangles": BASE.triangle_count(adjacency),
                "squares": BASE.square_count(adjacency),
                "independent_four_sets": len(independent_sets),
                "representative_edges": edges,
                "route": route,
                "exit_data": exit_data,
            }
            orbits.append(record)
            if route == "unresolved":
                unresolved_records.append(record)

        expected_routes = EXPECTED_ROUTES[target]
        actual_routes = (
            local_routes["independent four-shore full-row exclusion"],
            local_routes["cubic-cubic forced-anchor permanent zero"],
            local_routes["unresolved"],
        )
        require(actual_routes == expected_routes,
                ("support-16 orbit routes changed", target, actual_routes))
        route_by_sequence[target] = actual_routes

    require(sum(item["labelled_count"] for item in census) == 54179,
            "support-16 labelled total changed")
    require(sum(item["terminal_count"] for item in census) == 20945,
            "support-16 terminal total changed")
    require(len(orbits) == 57, ("terminal orbit total changed", len(orbits)))
    require(route_counter == Counter({
        "unresolved": 26,
        "cubic-cubic forced-anchor permanent zero": 16,
        "independent four-shore full-row exclusion": 15,
    }), ("support-16 route totals changed", route_counter))
    require(independent_cross_histogram == Counter({
        (13, 3, 3): 6,
        (14, 2, 2): 6,
        (12, 4, 4): 2,
        (16, 0, 0): 1,
    }), ("independent-shore cross reductions changed",
         independent_cross_histogram))
    require(unresolved_by_sequence == Counter({
        (6, 4, 4, 4, 4, 4, 3, 3): 2,
        (5, 5, 4, 4, 4, 4, 3, 3): 12,
        (5, 4, 4, 4, 4, 4, 4, 3): 9,
        (4, 4, 4, 4, 4, 4, 4, 4): 3,
    }), ("residual degree-sequence distribution changed",
         unresolved_by_sequence))
    require(unresolved_minimum_histogram == Counter({2: 22, 3: 4}),
            ("residual minimum response complexity changed",
             unresolved_minimum_histogram))
    require((unresolved_support15_extension_orbits,
             unresolved_support15_deletion_directions) == (8, 12),
            ("support-15 extension count changed",
             unresolved_support15_extension_orbits,
             unresolved_support15_deletion_directions))

    first_degree = (6, 4, 4, 4, 4, 4, 3, 3)
    first_residuals = tuple(
        record for record in unresolved_records
        if record["degree_sequence"] == first_degree
    )
    require(len(first_residuals) == 2,
            ("first residual orbit count changed", first_residuals))
    require(
        {tuple(record["representative_edges"]) for record in first_residuals}
        == set(FIRST_RESIDUALS),
        ("first residual representatives changed", first_residuals),
    )
    require({record["orbit_size"] for record in first_residuals} == {60, 240},
            ("first residual orbit sizes changed", first_residuals))

    return {
        "degree_sequences": DEGREE_SEQUENCES,
        "census": census,
        "terminal_orbits": orbits,
        "route_totals": dict(route_counter),
        "route_by_sequence": dict(route_by_sequence),
        "independent_cross_histogram": dict(independent_cross_histogram),
        "unresolved_by_sequence": dict(unresolved_by_sequence),
        "unresolved_minimum_response_histogram":
            dict(unresolved_minimum_histogram),
        "unresolved_support15_extension_orbits":
            unresolved_support15_extension_orbits,
        "unresolved_support15_deletion_directions":
            unresolved_support15_deletion_directions,
        "first_residuals": first_residuals,
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
    # Re-run exact portions of the imported exits.  The complete K4,4 branch
    # of the independent-shore theorem remains its explicitly cited theorem.
    anchor_landing = BASE.audit_fourteen_terminal_anchor_clean_landing()
    require(anchor_landing["active_zero_over_C"],
            "imported forced-anchor permanent theorem changed")
    require(NO_INDEPENDENT.check_step1_parity() == 70 * 105,
            "imported independent-shore parity theorem changed")
    require(NO_INDEPENDENT.check_step2_invisibility(),
            "imported independent-shore invisibility theorem changed")
    dead_cross = NO_INDEPENDENT.check_step3b_dead_edge_case()
    require(len(dead_cross) == 8,
            "imported independent-shore dead-cross theorem changed")

    ledger = canonical(audit_census_and_orbits())
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("support-16 terminal ledger changed", digest))

    print("N=8 support-16 clean terminal census: PASS")
    print("  labelled graphs / support terminals: 54179 / 20945")
    print("  terminal graph orbits: 57")
    print("  independent-shore exits: 15")
    print("  cubic-cubic permanent exits: 16")
    print("  residual orbits: 26 across 4 degree sequences")
    print("  residual minimum seal size 2 / 3: 22 / 4")
    print("  first residual degree sequence: (6,4^5,3^2), two orbits")


if __name__ == "__main__":
    main()
