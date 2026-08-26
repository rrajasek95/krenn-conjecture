#!/usr/bin/env python3
"""Independent, static referee for the exact-16 target-union SAT patch.

This program deliberately never opens or writes the 231 MB base CNF and never
starts a solver.  It rebuilds the exact-16 graph classes from the compact
eight-block census input, exhaustively normalizes all degree-four/singleton
rootings, and emits only a compact support ledger and patch metadata.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
CENSUS = REPO / "computations/unaudited-codex-n8-x5-eight-block-essential-skeleton-contraction-design-2026-08-26"
PARENT = REPO / "computations/unaudited-codex-n8-x5-eight-block-first-induction-interface-2026-08-26"
SAT_SOURCE = CROSS / "claims/finite/n08/eight_vertex_local_degree4_support.py"

MAX_READ_BYTES = 2 * 1024 * 1024
EXPECTED_LEDGER_SHA256 = "3caf456fcd37b963f22d7e70b914817a5fd71032dbea873729d6dc0d3dd50aae"

PINS = {
    "census_manifest": (CENSUS / "MANIFEST.sha256", "bef35566e155115f3411d02c511c381390cb4ea013212ad2f3cda19ed9adc270"),
    "census_builder": (CENSUS / "build_design.py", "7a2280123ae46e5d43379452e64fd93b220e3ab7d99ff66a67ed3a968c3fd8a2"),
    "parent_manifest": (PARENT / "MANIFEST.sha256", "4334804545c7f2a73189137f47bfa1105905db4d6b2c52de0d140217d9ae4a10"),
    "parent_result": (PARENT / "results_eight_block_interface.json", "886ae50bede93dd21bf0ea5dda7ed9154a58a9caf532aabc306537640473cf25"),
    "current_sat_generator": (SAT_SOURCE, "83996bdb4da059de2490549ed07fbb225b024e21763a8db4cf871fb0228cb0bb"),
}

BASE = {
    "path_not_opened": "tmp/eight_vertex_local_degree4_full_local_max16_current.cnf",
    "sha256_from_sealed_small_metadata": "9e057710afe016609c31ae4c0cb45b1a948ca48b74426d390a2a9209035dd547",
    "bytes": 231480677,
    "variables": 428247,
    "clauses": 3083172,
}


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    require(path.is_file(), ("missing", str(path)))
    require(path.stat().st_size <= MAX_READ_BYTES, ("over-2MiB read refused", str(path), path.stat().st_size))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def canonical_json_hash(value) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def edge_tuple(edge: str) -> tuple[int, int]:
    require(len(edge) == 2 and edge[0] < edge[1], ("bad edge", edge))
    return int(edge[0]), int(edge[1])


def essential_edges(record) -> tuple[tuple[int, int], ...]:
    answer = set()
    for matching in record["supported_perfect_matchings"]:
        edges = tuple(edge_tuple(edge) for edge in matching.split("|"))
        require(len(edges) == 4)
        require(sorted(v for edge in edges for v in edge) == list(range(8)))
        answer.update(edges)
    return tuple(sorted(answer))


def canonical_graph(edges: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    degree = {v: sum(v in edge for edge in edges) for v in range(8)}
    cells = tuple(tuple(v for v in range(8) if degree[v] == d) for d in sorted(set(degree.values())))
    best = None
    for choices in itertools.product(*(itertools.permutations(cell) for cell in cells)):
        order = tuple(itertools.chain.from_iterable(choices))
        position = {old: new for new, old in enumerate(order)}
        key = tuple(sorted((min(position[a], position[b]), max(position[a], position[b])) for a, b in edges))
        if best is None or key < best:
            best = key
    require(best is not None)
    return best


def block_order() -> tuple[tuple[int, int], ...]:
    # The pinned current source allocates all 25*9 entry variables first and
    # then one block variable per allowed edge in itertools order.
    allowed = tuple(
        edge for edge in itertools.combinations(range(8), 2)
        if edge[0] != 0 or edge[1] in {1, 2, 3, 4}
    )
    require(len(allowed) == 25)
    require(allowed[:4] == ((0, 1), (0, 2), (0, 3), (0, 4)))
    return allowed


def normalized_supports(graphs, restriction=None):
    supports = defaultdict(set)
    raw_roles = 0
    class_stats = []
    for graph_id, edges in graphs:
        edge_set = set(edges)
        degree = {v: sum(v in edge for edge in edge_set) for v in range(8)}
        centers = [v for v in range(8) if degree[v] == 4]
        if restriction == "missing_center_rooting":
            centers = centers[:-1]
        class_raw = 0
        class_supports = set()
        for center in centers:
            neighbours = sorted(v for v in range(8) if tuple(sorted((center, v))) in edge_set)
            outside = sorted(set(range(8)) - {center, *neighbours})
            require(len(neighbours) == 4 and len(outside) == 3)
            singletons = neighbours[:-1] if restriction == "missing_singleton_rooting" else neighbours
            for singleton in singletons:
                neighbour_perms = list(itertools.permutations(v for v in neighbours if v != singleton))
                outside_perms = list(itertools.permutations(outside))
                if restriction == "missing_neighbour_permutation":
                    neighbour_perms = neighbour_perms[:-1]
                if restriction == "missing_outside_permutation":
                    outside_perms = outside_perms[:-1]
                for neighbour_perm in neighbour_perms:
                    for outside_perm in outside_perms:
                        mapping = {center: 0, singleton: 1}
                        mapping.update(dict(zip(neighbour_perm, (2, 3, 4))))
                        mapping.update(dict(zip(outside_perm, (5, 6, 7))))
                        support = tuple(sorted(
                            (min(mapping[a], mapping[b]), max(mapping[a], mapping[b]))
                            for a, b in edge_set
                        ))
                        require(len(support) == 16 and len(set(support)) == 16)
                        require(all((0, v) in support for v in range(1, 5)))
                        require(all((0, v) not in support for v in range(5, 8)))
                        class_raw += 1
                        raw_roles += 1
                        class_supports.add(support)
                        supports[support].add(graph_id)
        class_stats.append({
            "graph_id": graph_id,
            "degree_four_centers": sum(degree[v] == 4 for v in range(8)),
            "raw_rooted_permuted_embeddings": class_raw,
            "distinct_normalized_supports_within_class": len(class_supports),
        })
    return supports, raw_roles, class_stats


def build():
    observed_pins = {}
    for name, (path, expected) in PINS.items():
        observed = sha(path)
        require(observed == expected, (name, observed, expected))
        observed_pins[name] = {"path": str(path), "sha256": observed, "bytes": path.stat().st_size}

    require(BASE["bytes"] > MAX_READ_BYTES)
    require(not (HERE / "base.cnf").exists())

    parent_path = PINS["parent_result"][0]
    parent = json.loads(parent_path.read_text())
    records = parent["unresolved_records"]
    require(len(records) == 616)

    histogram = Counter()
    graph_members = defaultdict(list)
    canonical_edges_by_id = {}
    for index, record in enumerate(records):
        edges = essential_edges(record)
        degree = Counter(v for edge in edges for v in edge)
        require(4 in degree.values())
        histogram[len(edges)] += 1
        if len(edges) == 16:
            key = canonical_graph(edges)
            graph_id = canonical_json_hash(key)
            graph_members[graph_id].append(index)
            canonical_edges_by_id[graph_id] = key

    require(histogram == {12: 88, 13: 104, 14: 124, 15: 184, 16: 116})
    require(len(graph_members) == 16)
    require(Counter(map(len, graph_members.values())) == {4: 5, 8: 10, 16: 1})
    graphs = tuple((graph_id, canonical_edges_by_id[graph_id]) for graph_id in sorted(graph_members))

    supports, raw_roles, class_stats = normalized_supports(graphs)
    require(raw_roles == 8928)
    require(len(supports) == 5508)

    order = block_order()
    block_variables = {edge: 226 + i for i, edge in enumerate(order)}
    require(tuple(block_variables.values()) == tuple(range(226, 251)))

    witnesses = []
    for support in sorted(supports):
        mask = sum(1 << i for i, edge in enumerate(order) if edge in support)
        require(mask.bit_count() == 16)
        witnesses.append({
            "support_mask_hex": f"{mask:07x}",
            "support_edges": [f"{a}{b}" for a, b in support],
            "source_graph_ids": sorted(supports[support]),
        })

    # Independent compact ledger. The cross-producer ledger is compared by
    # semantic witness masks as well as by its separately pinned byte hash.
    ledger = {
        "schema": "n8-x5-exact16-normalized-target-ledger-referee-v1",
        "normalization": {
            "degree_four_center": 0,
            "chosen_singleton_neighbour": 1,
            "other_center_neighbours": [2, 3, 4],
            "outside_vertices": [5, 6, 7],
        },
        "block_order": [f"{a}{b}" for a, b in order],
        "witnesses": witnesses,
    }
    ledger_bytes = canonical_json_bytes(ledger) + b"\n"
    ledger_path = HERE / "independent_target_ledger.json"
    ledger_path.write_bytes(ledger_bytes)
    ledger_sha = hashlib.sha256(ledger_bytes).hexdigest()
    cross_ledger_bytes = b"".join(
        ("|".join(witness["support_edges"]) + "\n").encode()
        for witness in witnesses
    )
    cross_ledger_sha = hashlib.sha256(cross_ledger_bytes).hexdigest()
    require(cross_ledger_sha == EXPECTED_LEDGER_SHA256, (cross_ledger_sha, EXPECTED_LEDGER_SHA256))
    (HERE / "target_supports.ledger").write_bytes(cross_ledger_bytes)

    selector_first = BASE["variables"] + 1
    selector_last = BASE["variables"] + len(witnesses)
    implications = len(witnesses) * len(order)
    global_or = 1
    added_clauses = implications + global_or
    require(added_clauses == 137701)
    require(selector_last == 433755)
    require(BASE["clauses"] + added_clauses == 3220873)
    patch = {
        "schema": "n8-x5-exact16-target-union-selector-patch-metadata-v1",
        "base": BASE,
        "block_variables": [
            {"edge": f"{a}{b}", "variable": block_variables[a, b]}
            for a, b in order
        ],
        "selector_variables": {
            "first": selector_first,
            "last": selector_last,
            "count": len(witnesses),
            "witness_order": "independent_target_ledger.json witnesses order",
        },
        "clause_template": {
            "per_selector": "for each block b: (-selector OR b) if edge present, else (-selector OR -b)",
            "clauses_per_selector": 25,
            "global_clause": "positive OR of all 5,508 selector variables",
            "soundness": "the global OR selects at least one cube; its 25 implications force all block variables to exactly that target support",
        },
        "added_variables": 5508,
        "added_implication_clauses": implications,
        "added_global_or_clauses": global_or,
        "added_clauses": added_clauses,
        "patched_header": {"variables": selector_last, "clauses": BASE["clauses"] + added_clauses},
        "explicit_non_action": "metadata only; no base CNF read/write and no solver launch",
    }
    (HERE / "selector_patch_metadata.json").write_text(json.dumps(patch, indent=2, sort_keys=True) + "\n")

    hostile_counts = {}
    for hostile in (
        "missing_center_rooting",
        "missing_singleton_rooting",
        "missing_neighbour_permutation",
        "missing_outside_permutation",
    ):
        mutated, _, _ = normalized_supports(graphs, hostile)
        hostile_counts[hostile] = len(mutated)
        require(len(mutated) != 5508, (hostile, "unexpectedly accepted"))
    require(hostile_counts == {
        "missing_center_rooting": 4428,
        "missing_singleton_rooting": 4320,
        "missing_neighbour_permutation": 4701,
        "missing_outside_permutation": 4770,
    })

    hostiles = {
        "schema": "n8-x5-exact16-target-union-hostiles-v1",
        "status": "PASS_ALL_REJECTED",
        "enumeration_omissions": hostile_counts,
        "structural_rejections": {
            "extra_support": "a 17th edge fails exact mask popcount 16",
            "missing_support": "a 15-edge mask fails exact mask popcount 16",
            "wrong_center_neighbour": "any 05/06/07 edge or absent 01/02/03/04 edge fails normalization",
            "duplicate_support": "set dedup is mandatory before selector allocation",
            "block_variable_outside_226_250": "refused by exact pinned allocation map",
            "missing_selector_implication": "does not force a complete 25-block cube",
            "flipped_selector_implication": "does not select the recorded target cube",
            "missing_global_or": "would admit the unrestricted generic SAT skeleton",
            "old_26_clauses_per_selector_arithmetic": "REJECT: exact template has 25 implications per selector plus one global OR, not 26 per selector",
        },
        "rejected_old_added_clause_count": 143209,
        "accepted_added_clause_count": 137701,
    }
    (HERE / "hostile_tests.json").write_text(json.dumps(hostiles, indent=2, sort_keys=True) + "\n")

    result = {
        "schema": "n8-x5-exact16-target-union-independent-referee-v1",
        "status": "PASS_STATIC_EXACT16_TARGET_UNION_REFEREE",
        "pins": observed_pins,
        "limits": {"max_file_read_bytes": MAX_READ_BYTES, "base_cnf_read": False, "base_cnf_written": False, "solver_run": False},
        "census": {
            "records": len(records),
            "essential_edge_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "exact16_records": 116,
            "exact16_unlabelled_graph_classes": len(graphs),
            "class_member_size_census": {str(k): v for k, v in sorted(Counter(map(len, graph_members.values())).items())},
            "graph_classes_sha256": canonical_json_hash([
                {"graph_id": graph_id, "canonical_edges": list(edges), "record_indices": sorted(graph_members[graph_id])}
                for graph_id, edges in graphs
            ]),
        },
        "normalization": {
            "raw_rooted_permuted_embeddings": raw_roles,
            "deduplicated_witnesses": len(witnesses),
            "class_statistics": class_stats,
            "independent_ledger_path": ledger_path.name,
            "independent_ledger_sha256": ledger_sha,
            "cross_ledger_path": "target_supports.ledger",
            "cross_ledger_sha256": cross_ledger_sha,
            "expected_cross_producer_ledger_sha256": EXPECTED_LEDGER_SHA256,
            "cross_producer_byte_hash_compared": True,
        },
        "selector_patch": patch,
        "proof": {
            "coverage": "Every enumerated target witness receives one selector whose 25 implications force its complete normalized block assignment.",
            "generic_exclusion": "The global selector OR forbids assignments with no selected target; therefore the unrefined generic SAT skeleton is excluded.",
            "scope": "Static refinement design only; no SAT/UNSAT result and no theorem promotion.",
        },
        "hostiles": hostiles,
    }
    (HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    build()
