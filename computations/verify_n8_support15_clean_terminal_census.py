#!/usr/bin/env python3
"""Exact support-15 clean-cap terminal census at N=8.

This continues the generalized RRR/RRX support test from
``verify_n8_support_rank_minimal_projective_cap_error_counterguard.py``.
All 40,288 labelled graphs in the nine minimum-degree-three degree sequences
are generated.  The support-clean terminals are quotiented by their literal
degree-preserving permutation groups.

Every terminal orbit is then routed by source-valid data:

* an independent four-shore reduces to a previously checked complete mixed
  bipartite obstruction;
* a degree-three--degree-three edge has the forced-anchor 2x2-permanent
  active zero proved at support 14; or
* it is the unique remaining orbit recorded below.

Standard library only; all checks survive ``python -O`` and ``python -I -S``.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "e2e82232d82107a844c228c9ed0c4a5e2ed072dd814b9736c46ffacb2e8e8b05"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load audit dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_local(
    "n8_support_base",
    "verify_n8_support_rank_minimal_projective_cap_error_counterguard.py",
)
NO_INDEPENDENT = load_local(
    "n8_no_independent_four",
    "verify_no_independent_four_set_at_eight.py",
)

N = 8
IDENTITY_PERMUTATION = tuple(range(N))

DEGREE_SEQUENCES = (
    (7, 5, 3, 3, 3, 3, 3, 3),
    (7, 4, 4, 3, 3, 3, 3, 3),
    (6, 6, 3, 3, 3, 3, 3, 3),
    (6, 5, 4, 3, 3, 3, 3, 3),
    (6, 4, 4, 4, 3, 3, 3, 3),
    (5, 5, 5, 3, 3, 3, 3, 3),
    (5, 5, 4, 4, 3, 3, 3, 3),
    (5, 4, 4, 4, 4, 3, 3, 3),
    (4, 4, 4, 4, 4, 4, 3, 3),
)

# labelled count, distribution by number of support-clean edges, terminals
EXPECTED_CENSUS = {
    DEGREE_SEQUENCES[0]: (270, {4: 270}, 0),
    DEGREE_SEQUENCES[1]: (
        460, {2: 60, 4: 60, 5: 300, 6: 30, 8: 10}, 0,
    ),
    DEGREE_SEQUENCES[2]: (615, {1: 60, 3: 375, 4: 180}, 0),
    DEGREE_SEQUENCES[3]: (
        1830, {1: 30, 2: 390, 3: 690, 4: 600, 5: 120}, 0,
    ),
    DEGREE_SEQUENCES[4]: (
        3148, {0: 96, 2: 756, 3: 1194, 4: 882, 5: 72, 6: 144, 9: 4}, 96,
    ),
    DEGREE_SEQUENCES[5]: (
        3211, {0: 120, 1: 60, 2: 900, 3: 1500, 4: 630, 15: 1}, 120,
    ),
    DEGREE_SEQUENCES[6]: (
        5570, {0: 168, 1: 392, 2: 2274, 3: 2172,
               4: 408, 5: 96, 6: 60}, 168,
    ),
    DEGREE_SEQUENCES[7]: (
        9444, {0: 540, 1: 2196, 2: 3870, 3: 2214,
               4: 504, 6: 84, 7: 36}, 540,
    ),
    DEGREE_SEQUENCES[8]: (
        15740, {0: 2180, 1: 6480, 2: 4500, 3: 2460, 6: 120}, 2180,
    ),
}

# orbit size, bipartite, triangles, squares, independent 4-sets,
# edges with an RRR witness, maximum RRR matching count at one edge
EXPECTED_ORBIT_SIGNATURES = {
    DEGREE_SEQUENCES[4]: (
        (24, False, 6, 12, 1, 3, 6),
        (72, False, 6, 14, 1, 1, 6),
    ),
    DEGREE_SEQUENCES[5]: (
        (120, False, 7, 12, 1, 0, 0),
    ),
    DEGREE_SEQUENCES[6]: (
        (24, False, 6, 11, 0, 1, 10),
        (48, False, 6, 10, 1, 1, 10),
        (96, False, 5, 15, 1, 1, 6),
    ),
    DEGREE_SEQUENCES[7]: (
        (36, False, 6, 11, 0, 0, 0),
        (72, False, 4, 14, 1, 1, 6),
        (72, False, 5, 12, 1, 1, 6),
        (72, False, 7, 8, 0, 0, 0),
        (144, False, 6, 9, 0, 1, 6),
        (144, False, 6, 10, 0, 1, 6),
    ),
    DEGREE_SEQUENCES[8]: (
        (20, True, 0, 27, 2, 9, 6),
        (720, False, 5, 9, 0, 0, 0),
        (720, False, 5, 10, 0, 0, 0),
        (720, False, 6, 9, 0, 1, 6),
    ),
}

UNRESOLVED_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 2), (1, 3), (1, 6),
    (2, 4), (2, 7),
    (3, 5), (3, 7),
    (4, 5), (4, 6),
    (5, 6), (5, 7),
)


def preserving_group(target):
    cells = tuple(
        tuple(vertex for vertex, degree in enumerate(target) if degree == d)
        for d in sorted(set(target), reverse=True)
    )
    answer = []
    for images_by_cell in product(*(tuple(permutations(cell)) for cell in cells)):
        permutation = list(range(N))
        for cell, images in zip(cells, images_by_cell, strict=True):
            for old, new in zip(cell, images, strict=True):
                permutation[old] = new
        answer.append(tuple(permutation))
    return tuple(answer)


def independent_four_sets(adjacency):
    return tuple(
        tuple(vertices)
        for vertices in combinations(range(N), 4)
        if not any(
            (adjacency[u] >> v) & 1
            for u, v in combinations(vertices, 2)
        )
    )


def response_counts(adjacency, edge):
    p, q = edge
    residual = tuple(vertex for vertex in range(N) if vertex not in edge)
    p_external = {v for v in residual if (adjacency[p] >> v) & 1}
    q_external = {v for v in residual if (adjacency[q] >> v) & 1}
    response_edges = {
        tuple(sorted((left, right)))
        for left in p_external for right in q_external if left != right
    }
    source_edges = set(BASE.graph_edges(adjacency))
    rrr = 0
    rrx = 0
    rrx_matchings = 0
    for matching in BASE.perfect_matchings(residual):
        matching = tuple(tuple(sorted(pair)) for pair in matching)
        rrr += int(all(pair in response_edges for pair in matching))
        tags = sum(
            matching[index] in source_edges
            and all(
                matching[j] in response_edges
                for j in range(3) if j != index
            )
            for index in range(3)
        )
        rrx += tags
        rrx_matchings += int(tags > 0)
    return rrr, rrx, rrx_matchings, p_external, q_external


def audit_unresolved_quadratic_map():
    """Retain every coefficient in the first two-matching vector output.

    At edge 37, the cubic external anchors are on 72 and 75.  The two RRX
    matchings use the complete degree-four blocks M0=A30 and M1=A31.  This
    expands the nine components of

      (u0^T K M0) tensor (u1^T K M1)
        + (u1^T K M0) tensor (u0^T K M1).

    A coordinate specialization gives a sharp local guard: its zero ideal
    contains (K00*K11)^2, so this particular vector output has no active
    zero.  This is not asserted to satisfy the other full-source rows.
    """
    adjacency = [0] * N
    for u, v in UNRESOLVED_EDGES:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    adjacency = tuple(adjacency)
    rrr, rrx, rrx_matchings, p_external, q_external = response_counts(
        adjacency, (3, 7)
    )
    require((rrr, rrx, rrx_matchings) == (0, 2, 2),
            ("selected unresolved response changed", rrr, rrx, rrx_matchings))
    require(p_external == {0, 1, 5} and q_external == {2, 5},
            ("selected unresolved external sets changed",
             p_external, q_external))
    require((4, 6) in set(UNRESOLVED_EDGES),
            "selected unresolved x multiplier disappeared")

    def add(left, right):
        answer = dict(left)
        for monomial, coefficient in right.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
            if answer[monomial] == 0:
                del answer[monomial]
        return answer

    def scale(polynomial, scalar):
        return {
            monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient
        }

    def multiply(left, right):
        answer = {}
        for left_monomial, left_coefficient in left.items():
            for right_monomial, right_coefficient in right.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                answer[monomial] = (
                    answer.get(monomial, 0)
                    + left_coefficient * right_coefficient
                )
        return answer

    def row_component(vector_tag, matrix_tag, output_colour):
        return {
            tuple(sorted((f"{vector_tag}{i}", f"K{i}{j}",
                          f"{matrix_tag}{j}{output_colour}"))): 1
            for i in range(3) for j in range(3)
        }

    components = {}
    for a in range(3):
        for b in range(3):
            components[a, b] = add(
                multiply(row_component("u0_", "M0_", a),
                         row_component("u1_", "M1_", b)),
                multiply(row_component("u1_", "M0_", a),
                         row_component("u0_", "M1_", b)),
            )
    term_counts = {key: len(polynomial) for key, polynomial in components.items()}
    require(set(term_counts.values()) == {117},
            ("unresolved formal component support changed", term_counts))
    formal_digest = sha256(
        json.dumps(
            [
                [list(key), [[list(monomial), coefficient]
                             for monomial, coefficient in sorted(polynomial.items())]]
                for key, polynomial in sorted(components.items())
            ],
            separators=(",", ":"),
        ).encode()
    ).hexdigest()

    # Coordinate specialization u0=e0, u1=e1, M0=M1=I.  With
    # a=K00,b=K01,d=K10,e=K11, three output entries are
    # F00=2ad, F11=2be, F01=ae+bd.  The following exact ideal certificate
    # proves 4(ae)^2 = 4(ae)F01-F00F11.
    def variable(name):
        return {(name,): 1}

    a, b, d, e = map(variable, ("a", "b", "d", "e"))
    ae = multiply(a, e)
    f00 = scale(multiply(a, d), 2)
    f11 = scale(multiply(b, e), 2)
    f01 = add(ae, multiply(b, d))
    certificate_left = add(
        scale(multiply(ae, f01), 4),
        scale(multiply(f00, f11), -1),
    )
    certificate_right = scale(multiply(ae, ae), 4)
    require(certificate_left == certificate_right,
            "unresolved local saturation certificate changed")

    return {
        "cap_edge": (3, 7),
        "cubic_external_anchor_edges": ((2, 7), (5, 7)),
        "degree_four_blocks_retained": ((0, 3), (1, 3)),
        "active_x_multiplier": (4, 6),
        "formal_component_term_counts": term_counts,
        "formal_map_digest": formal_digest,
        "coordinate_guard": "4*(K00*K11)^2=4*(K00*K11)*F01-F00*F11",
        "coordinate_guard_is_full_source": False,
    }


def audit_census_and_orbits():
    census_ledger = []
    orbit_ledger = []
    independent_exit_count = 0
    permanent_exit_count = 0
    unresolved = []
    independent_cross_counts = {}

    for target in DEGREE_SEQUENCES:
        distribution = {}
        terminals = []
        labelled_count = 0
        for adjacency in BASE.generate_degree_sequence_graphs(target):
            labelled_count += 1
            require(len(BASE.graph_edges(adjacency)) == 15,
                    ("support-15 edge count changed", target))
            clean_count = sum(
                BASE.response_support_clean_edge(adjacency, *edge)
                for edge in BASE.graph_edges(adjacency)
            )
            distribution[clean_count] = distribution.get(clean_count, 0) + 1
            if clean_count == 0:
                terminals.append(adjacency)
        expected_count, expected_distribution, expected_terminals = (
            EXPECTED_CENSUS[target]
        )
        require((labelled_count, distribution, len(terminals))
                == (expected_count, expected_distribution, expected_terminals),
                ("support-15 census changed", target, labelled_count,
                 distribution, len(terminals)))
        census_ledger.append(
            {
                "degree_sequence": target,
                "labelled_count": labelled_count,
                "clean_edge_distribution": distribution,
                "terminal_count": len(terminals),
            }
        )
        if not terminals:
            continue

        group = preserving_group(target)
        remaining = {
            BASE.permuted_edge_mask(graph, IDENTITY_PERMUTATION): graph
            for graph in terminals
        }
        signatures = []
        while remaining:
            representative_mask = min(remaining)
            adjacency = remaining[representative_mask]
            orbit = {
                BASE.permuted_edge_mask(adjacency, permutation)
                for permutation in group
            }
            require(representative_mask in orbit,
                    "orbit lost its representative")
            require(orbit <= set(remaining) | {
                BASE.permuted_edge_mask(graph, IDENTITY_PERMUTATION)
                for graph in terminals
            }, "degree-preserving orbit left the terminal set")
            for mask in orbit:
                remaining.pop(mask, None)

            edges = BASE.graph_edges(adjacency)
            independent_sets = independent_four_sets(adjacency)
            rrr_counts = tuple(response_counts(adjacency, edge)[0] for edge in edges)
            signature = (
                len(orbit), BASE.is_bipartite(adjacency),
                BASE.triangle_count(adjacency), BASE.square_count(adjacency),
                len(independent_sets), sum(value > 0 for value in rrr_counts),
                max(rrr_counts),
            )
            signatures.append(signature)

            exit_kind = None
            exit_data = None
            if independent_sets:
                shore = frozenset(min(independent_sets))
                complement = frozenset(range(N)) - shore
                all_cross = {
                    tuple(sorted((left, right)))
                    for left in shore for right in complement
                }
                live_cross = all_cross & set(edges)
                dead_cross = all_cross - live_cross
                dead_degrees = {
                    vertex: sum(vertex in edge for edge in dead_cross)
                    for vertex in range(N)
                }
                require(len(live_cross) in (12, 13, 15),
                        ("independent reduction left a new support", edges))
                require(all(value <= 1 for value in dead_degrees.values()),
                        ("dead cross set stopped being a matching", dead_cross))
                independent_cross_counts[len(live_cross)] = (
                    independent_cross_counts.get(len(live_cross), 0) + 1
                )
                independent_exit_count += 1
                exit_kind = "complete mixed independent-shore exclusion"
                exit_data = {
                    "shore": tuple(sorted(shore)),
                    "live_cross_edges": len(live_cross),
                    "dead_cross_matching": tuple(sorted(dead_cross)),
                    "zeroed_internal_edges": tuple(sorted(set(edges) - live_cross)),
                }
            else:
                cubic_edges = tuple(
                    edge for edge in edges
                    if all(adjacency[vertex].bit_count() == 3 for vertex in edge)
                )
                if cubic_edges:
                    cap_edge = cubic_edges[0]
                    rrr, _rrx, _rrx_matchings, p_external, q_external = (
                        response_counts(adjacency, cap_edge)
                    )
                    require(rrr == 0 and len(p_external) == len(q_external) == 2
                            and not (p_external & q_external),
                            ("cubic-edge permanent geometry changed", cap_edge))
                    leftover = (
                        set(range(N)) - set(cap_edge) - p_external - q_external
                    )
                    require(len(leftover) == 2,
                            ("cubic-edge leftover changed", cap_edge, leftover))
                    leftover_edge = tuple(sorted(leftover))
                    require(leftover_edge in set(edges),
                            ("cubic-edge x multiplier disappeared", cap_edge))
                    permanent_exit_count += 1
                    exit_kind = "forced-anchor permanent active zero"
                    exit_data = {
                        "cap_edge": cap_edge,
                        "external_sets": (tuple(sorted(p_external)),
                                          tuple(sorted(q_external))),
                        "active_x_edge": leftover_edge,
                    }
                else:
                    unresolved.append((target, orbit, adjacency, signature))
                    exit_kind = "unresolved"

            orbit_ledger.append(
                {
                    "degree_sequence": target,
                    "signature": signature,
                    "representative_edges": edges,
                    "exit_kind": exit_kind,
                    "exit_data": exit_data,
                }
            )

        expected_signatures = tuple(sorted(
            EXPECTED_ORBIT_SIGNATURES.get(target, ()), key=str
        ))
        require(tuple(sorted(signatures, key=str)) == expected_signatures,
                ("support-15 orbit signatures changed", target, signatures))

    require(sum(item["labelled_count"] for item in census_ledger) == 40288,
            "support-15 total labelled census changed")
    require(sum(item["terminal_count"] for item in census_ledger) == 3104,
            "support-15 total terminal census changed")
    require(len(orbit_ledger) == 16,
            ("support-15 terminal orbit count changed", len(orbit_ledger)))
    require(independent_exit_count == 8,
            ("support-15 independent exits changed", independent_exit_count))
    require(independent_cross_counts == {12: 3, 13: 4, 15: 1},
            ("support-15 bipartite reductions changed", independent_cross_counts))
    require(permanent_exit_count == 7,
            ("support-15 permanent exits changed", permanent_exit_count))
    require(len(unresolved) == 1,
            ("support-15 unresolved orbit count changed", len(unresolved)))

    target, orbit, adjacency, signature = unresolved[0]
    unresolved_adjacency = [0] * N
    for u, v in UNRESOLVED_EDGES:
        unresolved_adjacency[u] |= 1 << v
        unresolved_adjacency[v] |= 1 << u
    unresolved_adjacency = tuple(unresolved_adjacency)
    require(target == DEGREE_SEQUENCES[8]
            and BASE.permuted_edge_mask(unresolved_adjacency,
                                        IDENTITY_PERMUTATION) in orbit,
            "pinned unresolved graph left the unique orbit")
    require(signature == (720, False, 5, 9, 0, 0, 0),
            ("unresolved signature changed", signature))
    require(not independent_four_sets(unresolved_adjacency),
            "unresolved graph acquired an independent shore")
    degree_three_vertices = tuple(
        vertex for vertex in range(N)
        if unresolved_adjacency[vertex].bit_count() == 3
    )
    require(degree_three_vertices == (6, 7)
            and not ((unresolved_adjacency[6] >> 7) & 1),
            ("unresolved cubic pair changed", degree_three_vertices))

    rrx_distribution = {}
    for edge in UNRESOLVED_EDGES:
        rrr, rrx, rrx_matchings, _p_external, _q_external = response_counts(
            unresolved_adjacency, edge
        )
        degree_pair = tuple(sorted(
            (unresolved_adjacency[edge[0]].bit_count(),
             unresolved_adjacency[edge[1]].bit_count()), reverse=True
        ))
        key = (degree_pair, rrr, rrx, rrx_matchings)
        rrx_distribution[key] = rrx_distribution.get(key, 0) + 1
    require(
        rrx_distribution
        == {
            ((4, 4), 0, 3, 3): 2,
            ((4, 4), 0, 6, 6): 2,
            ((4, 4), 0, 8, 8): 5,
            ((4, 3), 0, 4, 4): 2,
            ((4, 3), 0, 2, 2): 4,
        },
        ("unresolved RRX distribution changed", rrx_distribution),
    )

    return {
        "census": census_ledger,
        "terminal_orbits": orbit_ledger,
        "independent_exit_count": independent_exit_count,
        "independent_cross_counts": independent_cross_counts,
        "permanent_exit_count": permanent_exit_count,
        "unresolved": {
            "degree_sequence": target,
            "orbit_size": len(orbit),
            "signature": signature,
            "representative_edges": UNRESOLVED_EDGES,
            "degree_three_vertices": degree_three_vertices,
            "RRX_distribution": rrx_distribution,
        },
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
    # Re-run the exact imported exits, not merely their prose statements.
    anchor_landing = BASE.audit_fourteen_terminal_anchor_clean_landing()
    require(anchor_landing["active_zero_over_C"],
            "imported permanent active-zero theorem changed")
    cube_rows = BASE.audit_cube_full_source_mixed_no_go()
    require(cube_rows["factorisations"] == 24
            and cube_rows["unique_mixed_per_factorisation"] == 6,
            "imported cube full-mixed theorem changed")
    dead_cross_rows = NO_INDEPENDENT.check_step3b_dead_edge_case()
    require(len(dead_cross_rows) == 8,
            "imported dead-cross full-mixed theorem changed")

    ledger = canonical(
        {
            "census_and_orbits": audit_census_and_orbits(),
            "unresolved_quadratic_map": audit_unresolved_quadratic_map(),
        }
    )
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("support-15 ledger changed", digest))

    print("N=8 support-15 clean terminal census: PASS")
    print("  labelled graphs / support terminals: 40288 / 3104")
    print("  terminal graph orbits: 16")
    print("  complete mixed independent-shore exits: 8")
    print("  forced-anchor permanent active-zero exits: 7")
    print("  first unresolved orbits: 1")
    print("  unresolved: (4^6,3^2), orbit 720, cubic vertices nonadjacent")
    print("  all 15 seals are RRX; r^[3]=0 at every edge")


if __name__ == "__main__":
    main()
