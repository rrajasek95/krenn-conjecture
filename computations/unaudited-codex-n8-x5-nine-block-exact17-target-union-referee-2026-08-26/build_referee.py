#!/usr/bin/env python3
"""Independent static exact-17 degree-four target-union referee."""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
NINE = REPO / "computations/unaudited-codex-n8-x5-nine-block-induction-census-design-2026-08-26"
RESIDUAL = REPO / "computations/unaudited-codex-n8-x5-nine-block-residual538-max17-held-design-2026-08-26"
EIGHT = REPO / "computations/unaudited-codex-n8-x5-eight-block-first-induction-interface-2026-08-26"
SAT_SOURCE = CROSS / "claims/finite/n08/eight_vertex_local_degree4_support.py"

EXPECTED_LEDGER_SHA256 = "f280c2b3223a9673c80d2aa7bfed7f97c0558fbc2dcb80f4ecac88f16c4b9dd8"
PINS = {
    "residual_manifest": (RESIDUAL / "MANIFEST.sha256", "b5494d96a6850f44891c8d23503b06c04d758e5332a1008a75d0233fa8bd0f91"),
    "residual_result": (RESIDUAL / "results_residual538_design.json", "412b54923e54cc284e0787e03e603b51fbf67af1d6b90e39b656aab206072d5b"),
    "residual_builder": (RESIDUAL / "build_design.py", "e83c9ceea89ebbe48aab11b6f390b6215309503a1c0b1e98e2167add89b16566"),
    "nine_census_manifest": (NINE / "MANIFEST.sha256", "edd2a501351e72fa58b4fc1d60bf473693b1dafe7ad46d45941ffca28bafdbcb"),
    "nine_census_builder": (NINE / "build_census.py", "cef3c47198dfbe1ec4d5204a1cebee9fb42bd51602639906d9d16ae17019e08a"),
    "eight_source": (EIGHT / "build_interface.py", "3467f0b2b5997d1739d76a50d7ec0ae0734b4f099608a511d893309a488e5894"),
    "current_sat_source": (SAT_SOURCE, "83996bdb4da059de2490549ed07fbb225b024e21763a8db4cf871fb0228cb0bb"),
}


def need(value, detail="validation failure"):
    if not value:
        raise RuntimeError(detail)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def canonical_graph(edges):
    edges = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    degree = {v: sum(v in edge for edge in edges) for v in range(8)}
    cells = tuple(tuple(v for v in range(8) if degree[v] == d) for d in sorted(set(degree.values())))
    best = None
    for choices in itertools.product(*(itertools.permutations(cell) for cell in cells)):
        order = tuple(itertools.chain.from_iterable(choices))
        position = {old: new for new, old in enumerate(order)}
        key = tuple(sorted((min(position[a], position[b]), max(position[a], position[b])) for a, b in edges))
        if best is None or key < best:
            best = key
    need(best is not None)
    return best


def import_algorithms():
    path = PINS["eight_source"][0]
    spec = importlib.util.spec_from_file_location("exact17_referee_eight", path)
    need(spec is not None and spec.loader is not None)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.five, module.seven


def rebuild_exact17(five, seven):
    additions = tuple(itertools.combinations(five.OFF_FAMILY, 9))
    need(len(additions) == 167960)
    evaders = tuple(added for added in additions if five.fixed_cap_certificate(set(five.FAMILY) | set(added)) is None)
    need(len(evaders) == 110652)
    stable = []
    reduction = Counter()
    for added in evaders:
        reduced, _ = five.guard_reduce(added)
        reduction[len(reduced)] += 1
        if len(reduced) == 9:
            stable.append(added)
    need(reduction == {3: 131, 4: 3430, 5: 18920, 6: 38596, 7: 33744, 8: 13502, 9: 2329})

    variable_order = tuple(sorted(five.VARIABLE))
    classification = Counter()
    essential_histogram = Counter()
    exact17_records = []
    exact16_no_degree4 = []
    graphs = {}
    graph_members = defaultdict(list)
    unresolved_index = 0
    for added in stable:
        for mask in range(16):
            variables = frozenset(variable_order[i] for i in range(4) if mask & (1 << i))
            support = set(five.FIXED) | set(variables) | set(added)
            if five.fixed_cap_certificate(support) is not None:
                classification["fixed_identity_cap"] += 1
                continue
            if seven.nonidentity_certificates(support):
                classification["nonidentity_hyperplane_cap"] += 1
                continue
            classification["unresolved_coefficient_locus"] += 1
            matchings = tuple(matching for matching in five.core.PM8 if set(matching) <= support)
            essential = tuple(sorted(set(edge for matching in matchings for edge in matching)))
            degree = Counter(v for edge in essential for v in edge)
            need(set(degree) == set(range(8)))
            essential_histogram[len(essential)] += 1
            if len(essential) == 17 and 4 in degree.values():
                key = canonical_graph(essential)
                gid = canonical_hash(key)
                graphs[gid] = key
                graph_members[gid].append(unresolved_index)
                exact17_records.append(unresolved_index)
            if len(essential) == 16 and 4 not in degree.values():
                exact16_no_degree4.append({
                    "record_index": unresolved_index,
                    "degree_sequence": sorted(degree.values()),
                    "essential_edges": [f"{a}{b}" for a, b in essential],
                })
            unresolved_index += 1
    need(classification == {
        "fixed_identity_cap": 26380,
        "nonidentity_hyperplane_cap": 7408,
        "unresolved_coefficient_locus": 3476,
    })
    need(unresolved_index == 3476)
    need(essential_histogram == {12: 224, 13: 472, 14: 358, 15: 780, 16: 1108, 17: 534})
    need(len(exact17_records) == 534 and len(graphs) == 50)
    need([row["record_index"] for row in exact16_no_degree4] == [1114, 1978, 2014, 2036])
    need(all(row["degree_sequence"] == [3, 3, 3, 3, 5, 5, 5, 5] for row in exact16_no_degree4))
    return tuple((gid, graphs[gid]) for gid in sorted(graphs)), {
        "classification": dict(classification),
        "essential_histogram": dict(essential_histogram),
        "record_indices": exact17_records,
        "graph_members": {gid: indices for gid, indices in sorted(graph_members.items())},
        "exceptions": exact16_no_degree4,
    }


def normalize(graphs, restriction=None):
    supports = set()
    raw = 0
    class_stats = []
    for gid, edge_tuple in graphs:
        edges = set(edge_tuple)
        degree = {v: sum(v in edge for edge in edges) for v in range(8)}
        centers = [v for v in range(8) if degree[v] == 4]
        if restriction == "missing_center_rooting":
            centers = centers[:-1]
        local = set()
        local_raw = 0
        for center in centers:
            neighbours = sorted(v for v in range(8) if tuple(sorted((center, v))) in edges)
            outside = sorted(set(range(8)) - {center, *neighbours})
            need(len(neighbours) == 4 and len(outside) == 3)
            singletons = neighbours[:-1] if restriction == "missing_singleton_rooting" else neighbours
            for singleton in singletons:
                near_perms = list(itertools.permutations(v for v in neighbours if v != singleton))
                far_perms = list(itertools.permutations(outside))
                if restriction == "missing_neighbour_permutation":
                    near_perms = near_perms[:-1]
                if restriction == "missing_outside_permutation":
                    far_perms = far_perms[:-1]
                for near in near_perms:
                    for far in far_perms:
                        mapping = {center: 0, singleton: 1}
                        mapping.update(dict(zip(near, (2, 3, 4))))
                        mapping.update(dict(zip(far, (5, 6, 7))))
                        support = tuple(sorted(
                            f"{min(mapping[a], mapping[b])}{max(mapping[a], mapping[b])}"
                            for a, b in edges
                        ))
                        need(len(support) == 17 and len(set(support)) == 17)
                        need(all(f"0{i}" in support for i in range(1, 5)))
                        need(all(f"0{i}" not in support for i in range(5, 8)))
                        supports.add(support)
                        local.add(support)
                        raw += 1
                        local_raw += 1
        class_stats.append({
            "graph_id": gid,
            "degree_four_centers": len([v for v in range(8) if degree[v] == 4]),
            "raw_embeddings": local_raw,
            "distinct_masks_within_class": len(local),
        })
    return supports, raw, class_stats


def build():
    pins = {}
    for name, (path, expected) in PINS.items():
        need(path.is_file(), (name, "missing"))
        observed = digest(path)
        need(observed == expected, (name, observed, expected))
        pins[name] = {"path": str(path), "sha256": observed, "bytes": path.stat().st_size}

    sealed = json.loads(PINS["residual_result"][0].read_text())
    sealed17 = sealed["exact17_degree4"]
    need(sealed17["records"] == 534 and sealed17["unlabelled_graph_classes"] == 50)
    need(sealed["exact16_no_degree4"]["records"] == 4)

    five, seven = import_algorithms()
    graphs, rebuilt = rebuild_exact17(five, seven)
    rebuilt_ids = [gid for gid, _ in graphs]
    sealed_class_map = {row["graph_id"]: row["record_indices"] for row in sealed17["graph_classes"]}
    need(rebuilt_ids == sorted(sealed_class_map))
    need(rebuilt["graph_members"] == dict(sorted(sealed_class_map.items())))
    need(rebuilt["record_indices"] == sealed17["record_indices"])
    need([row["record_index"] for row in rebuilt["exceptions"]] == [1114, 1978, 2014, 2036])

    supports, raw, class_stats = normalize(graphs)
    need(raw == 24048 and len(supports) == 18180)
    lines = tuple("|".join(support) for support in sorted(supports))
    ledger_bytes = ("\n".join(lines) + "\n").encode()
    ledger_sha = hashlib.sha256(ledger_bytes).hexdigest()
    need(ledger_sha == EXPECTED_LEDGER_SHA256, (ledger_sha, EXPECTED_LEDGER_SHA256))
    (HERE / "exact17_target_supports.ledger").write_bytes(ledger_bytes)

    omissions = {}
    for hostile in (
        "missing_center_rooting",
        "missing_singleton_rooting",
        "missing_neighbour_permutation",
        "missing_outside_permutation",
    ):
        changed, _, _ = normalize(graphs, hostile)
        omissions[hostile] = len(changed)
        need(len(changed) != 18180, (hostile, "not detected"))

    block_edges = tuple(
        edge for edge in itertools.combinations(range(8), 2)
        if edge[0] != 0 or edge[1] in {1, 2, 3, 4}
    )
    need(len(block_edges) == 25)
    selector_count = len(lines)
    implication_clauses = selector_count * 25
    added_clauses = implication_clauses + 1
    need(selector_count == 18180 and implication_clauses == 454500 and added_clauses == 454501)
    patch = {
        "schema": "n8-x5-nine-block-exact17-future-base-selector-patch-v1",
        "future_base": {
            "path": None,
            "sha256": None,
            "variables": None,
            "clauses": None,
            "required_before_materialization": True,
            "source_sha256": PINS["current_sat_source"][1],
            "required_generation_options": {"center_degree": 4, "maximum_edges": 17},
        },
        "block_variables": [
            {"edge": f"{a}{b}", "variable": 226 + index}
            for index, (a, b) in enumerate(block_edges)
        ],
        "ledger_path": "exact17_target_supports.ledger",
        "ledger_sha256": ledger_sha,
        "selector_count": selector_count,
        "selector_variable_formula": "base_variables+1 through base_variables+18180",
        "implication_clauses": implication_clauses,
        "global_selector_or": 1,
        "added_variables": selector_count,
        "added_clauses": added_clauses,
        "patched_header_formula": {
            "variables": "base_variables+18180",
            "clauses": "base_clauses+454501",
        },
        "semantics": "each selector implies all 25 block literals of one exact17 mask; one global positive OR selects at least one mask",
        "replacement_only": "materialize from the future pinned current max17 base; do not append to any max16 or earlier target-union CNF",
        "status": "STATIC_PATCH_READY__FUTURE_BASE_UNBOUND",
    }
    (HERE / "selector_patch_metadata.json").write_text(json.dumps(patch, indent=2, sort_keys=True) + "\n")

    hostiles = {
        "schema": "n8-x5-nine-block-exact17-target-union-hostiles-v1",
        "status": "PASS_ALL_REJECTED",
        "normalization_omissions": omissions,
        "scope_rejections": {
            "include_exact16_no_degree4_records": "rejected: records1114,1978,2014,2036 have 16 edges and degree sequence(3^4,5^4), hence no eligible degree-four rooting",
            "omit_any_of_534_records_or_50_classes": "rejected by exact sealed class/member equality",
            "historical_11051_roles_as_mask_ledger": "rejected: historical role catalogue is diagnostic and is not this 18,180-mask normalized ledger",
            "bind_numeric_header_before_future_base": "rejected: future current max17 base hash/header are null",
            "append_to_max16_target_union": "rejected: wrong base semantics and selector-variable aliasing",
            "use_26_clauses_per_selector": "rejected: 25 implications per selector plus one global OR",
            "missing_global_or": "rejects no generic skeleton",
            "malformed_16_or_18_edge_mask": "not exact17",
        },
    }
    (HERE / "hostile_tests.json").write_text(json.dumps(hostiles, indent=2, sort_keys=True) + "\n")

    result = {
        "schema": "n8-x5-nine-block-exact17-target-union-independent-referee-v1",
        "status": "PASS_STATIC_EXACT17_TARGET_UNION_REFEREE__FUTURE_BASE_HELD",
        "pins": pins,
        "non_action": {
            "large_cnf_read": False,
            "large_cnf_written": False,
            "solver_run": False,
            "future_base_materialized_here": False,
        },
        "sealed_census_replay": {
            "exact17_degree4_records": len(rebuilt["record_indices"]),
            "unlabelled_graph_classes": len(graphs),
            "record_indices_sha256": canonical_hash(rebuilt["record_indices"]),
            "graph_members_sha256": canonical_hash(rebuilt["graph_members"]),
            "class_statistics": class_stats,
        },
        "normalization": {
            "raw_rooted_permuted_embeddings": raw,
            "deduplicated_support_masks": len(supports),
            "ledger_bytes": len(ledger_bytes),
            "ledger_sha256": ledger_sha,
        },
        "exceptions_outside_scope": {
            "records": [1114, 1978, 2014, 2036],
            "essential_edges": 16,
            "degree_sequence": [3, 3, 3, 3, 5, 5, 5, 5],
            "reason": "no degree-four vertex; outside exact17 degree-four target union",
            "closed_here": False,
        },
        "selector_patch": patch,
        "coverage_proof": {
            "targets": "all 50 sealed exact17 graph classes are exhaustively rooted and every one of the 18,180 distinct normalized masks receives a complete selector cube",
            "generic_exclusion": "the global selector OR requires one complete exact17 target cube, excluding unrestricted generic supports",
            "scope": "static future-base replacement patch only; no SAT/UNSAT/theorem promotion",
        },
        "hostiles": hostiles,
    }
    (HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    build()
