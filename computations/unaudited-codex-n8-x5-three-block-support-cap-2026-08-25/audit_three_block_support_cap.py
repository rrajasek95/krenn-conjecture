#!/usr/bin/env python3
"""Graph-theoretic fixed-cap theorem and complete three-block classification."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-two-block-cap-classification-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "139a5270a384a36d6a1b3312dd6e1a0efba0cafe76912a179c973039e1464297"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-two-block-cap-classification-2026-08-25/results_two_block_cap_classification.json"
PARENT_RESULT_SHA256 = "87bdde155fbded9f39821b6023fe1d2939ec27a101f671d5bd9e289003e4ccb0"
CORE = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/audit_two_cell_dichotomy.py"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT) == PARENT_SHA256
assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
assert sha256(CORE) == CORE_SHA256
spec = importlib.util.spec_from_file_location("x5_core", CORE)
assert spec is not None and spec.loader is not None
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (3, 5), (1, 2), (6, 7)))
FAMILY = FIXED | VARIABLE
ALL_EDGES = frozenset(itertools.combinations(range(8), 2))
OFF_FAMILY = tuple(sorted(ALL_EDGES - FAMILY))
SWAP = (0, 2, 1, 3, 4, 5, 7, 6)


def edge_string(edge):
    return "".join(map(str, edge))


def apply_edge(edge, permutation=SWAP):
    return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))


def apply_support(support, permutation=SWAP):
    return tuple(sorted(apply_edge(edge, permutation) for edge in support))


def neighbours(support, vertex):
    return {
        other for edge in support if vertex in edge
        for other in edge if other != vertex
    }


def response_edges(support, p, q):
    residual = tuple(site for site in range(8) if site not in (p, q))
    answer = []
    for a, b in itertools.combinations(residual, 2):
        direct = tuple(sorted((p, a))) in support and tuple(sorted((q, b))) in support
        switched = tuple(sorted((p, b))) in support and tuple(sorted((q, a))) in support
        if direct or switched:
            answer.append((a, b))
    return tuple(answer)


def response_vertices(edges):
    return frozenset(site for edge in edges for site in edge)


def triangle_containing(edges, residual):
    vertices = response_vertices(edges)
    if len(vertices) > 3:
        return None
    triangle = list(sorted(vertices))
    triangle.extend(site for site in residual if site not in vertices and len(triangle) < 3)
    assert len(triangle) == 3
    return tuple(triangle)


def star_containing(edges, residual):
    if not edges:
        return residual[0]
    return next((centre for centre in residual if all(centre in edge for edge in edges)), None)


def fixed_cap_certificate(support):
    for p, q in sorted(FIXED):
        residual = tuple(site for site in range(8) if site not in (p, q))
        edges = response_edges(support, p, q)
        triangle = triangle_containing(edges, residual)
        if triangle is not None:
            external_union = (neighbours(support, p) - {q}) | (neighbours(support, q) - {p})
            return {
                "cap": edge_string((p, q)),
                "triangle": "".join(map(str, triangle)),
                "possible_response_edges": list(map(edge_string, edges)),
                "external_neighbour_union": sorted(external_union),
                "external_neighbour_union_size": len(external_union),
                "forbidden_response_rank": 0,
                "kernel_dimension": 9,
                "K": "I3",
                "kappa": [1, 1, 1],
                "s_pairing": 3,
            }
    return None


def fixed_star_or_triangle_certificate(support):
    for p, q in sorted(FIXED):
        residual = tuple(site for site in range(8) if site not in (p, q))
        edges = response_edges(support, p, q)
        triangle = triangle_containing(edges, residual)
        if triangle is not None:
            return "triangle", edge_string((p, q)), "".join(map(str, triangle))
        centre = star_containing(edges, residual)
        if centre is not None:
            return "star", edge_string((p, q)), str(centre)
    return None


def fixed_cap_loads(added):
    cap_of_site = {site: edge_string(cap) for cap in FIXED for site in cap}
    loads = {edge_string(cap): 0 for cap in FIXED}
    for u, v in added:
        assert cap_of_site[u] != cap_of_site[v]
        loads[cap_of_site[u]] += 1
        loads[cap_of_site[v]] += 1
    return dict(sorted(loads.items()))


def identity_matrix():
    return [[int(row == column) for column in core.COLORS] for row in core.COLORS]


def dense_matrix(seed):
    return [
        [Fraction(seed + 1 + 3 * row + 5 * column, 19 + seed + row + column)
         for column in core.COLORS]
        for row in core.COLORS
    ]


def install_block(source, edge, matrix):
    for left, right in itertools.product(core.COLORS, repeat=2):
        core.put(source, *edge, left, right, matrix[left][right])


def main():
    assert len(OFF_FAMILY) == 20
    triples = tuple(itertools.combinations(OFF_FAMILY, 3))
    assert len(triples) == 1140

    # Pigeonhole proof ledger.  Each new edge contributes one endpoint to two
    # distinct fixed matching edges, so total load is six.  Some one of four
    # fixed caps has load <=1; its two old external neighbours plus that load
    # fit in a triangle.
    certificate_records = []
    certificate_cap_census = {}
    for added in triples:
        loads = fixed_cap_loads(added)
        assert sum(loads.values()) == 6
        assert min(loads.values()) <= 1
        support = set(FAMILY) | set(added)
        certificate = fixed_cap_certificate(support)
        assert certificate is not None
        assert certificate["external_neighbour_union_size"] <= 3
        assert certificate["forbidden_response_rank"] == 0
        certificate_cap_census[certificate["cap"]] = certificate_cap_census.get(certificate["cap"], 0) + 1
        certificate_records.append({
            "added": list(map(edge_string, added)),
            "loads": loads,
            "certificate": certificate,
        })
    assert len(certificate_records) == 1140

    # Exact order-two orbit classification of all triples.
    triple_set = set(triples)
    seen = set()
    orbits = []
    for triple in triples:
        if triple in seen:
            continue
        orbit = sorted({triple, apply_support(triple)})
        assert set(orbit) <= triple_set
        seen.update(orbit)
        orbits.append({
            "orbit_id": len(orbits),
            "representative": list(map(edge_string, orbit[0])),
            "members": [list(map(edge_string, member)) for member in orbit],
            "orbit_size": len(orbit),
            "representative_certificate": fixed_cap_certificate(set(FAMILY) | set(orbit[0])),
        })
    assert seen == triple_set
    assert len(orbits) == 579
    assert sum(record["orbit_size"] == 1 for record in orbits) == 18
    assert sum(record["orbit_size"] == 2 for record in orbits) == 561

    # Distributed literal source replay.  Structural enumeration above is
    # exhaustive; these arbitrary dense rational matrices independently guard
    # the source orientation and response implementation.
    literal_records = []
    for sample in range(257):
        added = triples[(sample * 37) % len(triples)]
        support = set(FAMILY) | set(added)
        certificate = fixed_cap_certificate(support)
        assert certificate is not None
        source = {}
        for edge in FIXED:
            install_block(source, edge, identity_matrix())
        for index, edge in enumerate(sorted(VARIABLE | set(added))):
            install_block(source, edge, dense_matrix(13 + sample + 11 * index))
        p, q = tuple(map(int, certificate["cap"]))
        triangle = frozenset(map(int, certificate["triangle"]))
        residual = tuple(site for site in range(8) if site not in (p, q))
        forbidden = tuple(
            edge for edge in itertools.combinations(residual, 2)
            if not set(edge) <= triangle
        )
        K = identity_matrix()
        assert all(core.response(source, p, q, *edge, K) == [[0] * 3 for _ in range(3)]
                   for edge in forbidden)
        assert [K[colour][colour] for colour in core.COLORS] == [1, 1, 1]
        assert sum(K[i][j] * core.get(source, p, q, i, j)
                   for i, j in itertools.product(core.COLORS, repeat=2)) == 3
        literal_records.append({
            "sample": sample,
            "added": list(map(edge_string, added)),
            "cap": certificate["cap"],
            "triangle": certificate["triangle"],
        })

    # Sharp next boundary diagnostic only.  Four additions are the first time
    # all four cap loads can equal two.  Enumerate supports escaping fixed
    # identity triangle certificates, and the smaller subset escaping fixed
    # identity star certificates as well.  No coefficient solve is attempted.
    quadruples = tuple(itertools.combinations(OFF_FAMILY, 4))
    triangle_evaders = []
    fixed_carrier_evaders = []
    for added in quadruples:
        support = set(FAMILY) | set(added)
        if fixed_cap_certificate(support) is None:
            triangle_evaders.append(added)
            if fixed_star_or_triangle_certificate(support) is None:
                fixed_carrier_evaders.append(added)
    assert len(quadruples) == 4845
    assert len(triangle_evaders) == 264
    assert len(fixed_carrier_evaders) == 24
    assert all(fixed_cap_loads(added) == {"03": 2, "16": 2, "27": 2, "45": 2}
               for added in fixed_carrier_evaders)
    evader_set = set(fixed_carrier_evaders)
    evader_seen = set()
    evader_orbits = []
    for added in fixed_carrier_evaders:
        if added in evader_seen:
            continue
        orbit = sorted({added, apply_support(added)})
        assert len(orbit) == 2 and set(orbit) <= evader_set
        evader_seen.update(orbit)
        representative = orbit[0]
        support = set(FAMILY) | set(representative)
        response_graphs = {
            edge_string(cap): list(map(edge_string, response_edges(support, *cap)))
            for cap in sorted(FIXED)
        }
        evader_orbits.append({
            "orbit_id": len(evader_orbits),
            "representative": list(map(edge_string, representative)),
            "members": [list(map(edge_string, member)) for member in orbit],
            "fixed_cap_response_graphs": response_graphs,
        })
    assert evader_seen == evader_set and len(evader_orbits) == 12

    result = {
        "schema": "KRENN_X5_THREE_BLOCK_SUPPORT_CAP_CLASSIFICATION_V1",
        "status": "PASS_ALL_1140_THREE_BLOCK_SUPPORTS_HAVE_FIXED_IDENTITY_ACTIVE_CAP",
        "parent_manifest_sha256": PARENT_SHA256,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "core_sha256": CORE_SHA256,
        "graph_theorem": {
            "fixed_identity_caps": list(map(edge_string, sorted(FIXED))),
            "criterion": (
                "if the possible response-edge graph for fixed cap pq uses at most "
                "three residual vertices, choose a triangle containing them; K=I3 "
                "has zero forbidden responses, kappa=(1,1,1), and s=3"
            ),
            "load_proof": (
                "each off-family edge loads two distinct fixed caps; with m<=3 the "
                "total load is <=6, so one of four caps has load <=1; its two base "
                "external neighbours plus new load use at most three vertices"
            ),
            "coefficient_field": "characteristic zero",
            "same_source": True,
        },
        "three_block_classification": {
            "supports": len(triples),
            "exact_guard_symmetry": {"order": 2, "generator": "(1 2)(6 7)"},
            "orbits": len(orbits),
            "singleton_orbits": 18,
            "doubleton_orbits": 561,
            "fixed_cap_triangle_evaders": 0,
            "certificate_cap_census": dict(sorted(certificate_cap_census.items())),
            "orbit_records": orbits,
            "certificate_records_sha256": hashlib.sha256(
                json.dumps(certificate_records, sort_keys=True).encode()
            ).hexdigest(),
        },
        "literal_replay": {
            "dense_rational_samples": len(literal_records),
            "records_sha256": hashlib.sha256(json.dumps(literal_records, sort_keys=True).encode()).hexdigest(),
            "forbidden_responses_zero": True,
            "activity": "K=I3, kappa=(1,1,1), s=3",
        },
        "sharp_four_block_boundary_diagnostic": {
            "supports": len(quadruples),
            "fixed_triangle_certificate_evaders": len(triangle_evaders),
            "fixed_triangle_or_star_certificate_evaders": len(fixed_carrier_evaders),
            "exact_guard_orbits_of_fixed_carrier_evaders": len(evader_orbits),
            "orbit_records": evader_orbits,
            "interpretation": (
                "these 24 supports are not cap-free; only the coefficient-independent "
                "fixed-identity star/triangle certificate fails, so response rank/minor "
                "and activity equations become coefficient-dependent"
            ),
            "coefficient_conditions_solved": False,
        },
        "scope": {
            "all_zero_one_two_three_block_layers_closed": True,
            "all_three_block_supports": True,
            "three_block_inactive_common_zero_family": None,
            "four_block_coefficient_classification": False,
            "full_support_dichotomy": False,
            "full_conjecture_claim": False,
            "broad_cegar": False,
            "degree_twelve_read": False,
        },
    }
    temporary = HERE / "results_three_block_support_cap.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_three_block_support_cap.json")
    print(json.dumps({
        "status": result["status"],
        "three_supports": len(triples),
        "three_orbits": len(orbits),
        "three_evaders": 0,
        "four_fixed_carrier_evaders": len(fixed_carrier_evaders),
        "four_evader_orbits": len(evader_orbits),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
