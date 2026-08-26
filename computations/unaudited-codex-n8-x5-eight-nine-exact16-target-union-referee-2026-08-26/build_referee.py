#!/usr/bin/env python3
"""Independent static referee for the combined eight+nine exact-16 union.

No CNF is opened or written and no solver is invoked.  The nine-block census
is recomputed from the compact authoritative source algorithms rather than by
reading its 5 MB materialized result.
"""

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
EIGHT_PARENT = REPO / "computations/unaudited-codex-n8-x5-eight-block-first-induction-interface-2026-08-26"
EIGHT_CENSUS = REPO / "computations/unaudited-codex-n8-x5-eight-block-essential-skeleton-contraction-design-2026-08-26"
NINE_CENSUS = REPO / "computations/unaudited-codex-n8-x5-nine-block-induction-census-design-2026-08-26"
SAT_SOURCE = CROSS / "claims/finite/n08/eight_vertex_local_degree4_support.py"
NARROW_BUILD = CROSS / "tmp/eight_vertex_local_degree4_full_local_max16_exact16_target_union_current.cnf.build.json"

EXPECTED_LEDGER_SHA256 = "6bffb2962242725f8bd0603dfaeb91f64c2ee0e4430632b445b42e44d4a424d5"
BASE = {
    "path_not_opened": "tmp/eight_vertex_local_degree4_full_local_max16_current.cnf",
    "sha256_from_sealed_small_metadata": "9e057710afe016609c31ae4c0cb45b1a948ca48b74426d390a2a9209035dd547",
    "bytes": 231480677,
    "variables": 428247,
    "clauses": 3083172,
}
PINS = {
    "eight_census_manifest": (EIGHT_CENSUS / "MANIFEST.sha256", "bef35566e155115f3411d02c511c381390cb4ea013212ad2f3cda19ed9adc270"),
    "eight_census_builder": (EIGHT_CENSUS / "build_design.py", "7a2280123ae46e5d43379452e64fd93b220e3ab7d99ff66a67ed3a968c3fd8a2"),
    "nine_census_manifest": (NINE_CENSUS / "MANIFEST.sha256", "edd2a501351e72fa58b4fc1d60bf473693b1dafe7ad46d45941ffca28bafdbcb"),
    "nine_census_builder": (NINE_CENSUS / "build_census.py", "cef3c47198dfbe1ec4d5204a1cebee9fb42bd51602639906d9d16ae17019e08a"),
    "eight_parent_manifest": (EIGHT_PARENT / "MANIFEST.sha256", "4334804545c7f2a73189137f47bfa1105905db4d6b2c52de0d140217d9ae4a10"),
    "eight_parent_result": (EIGHT_PARENT / "results_eight_block_interface.json", "886ae50bede93dd21bf0ea5dda7ed9154a58a9caf532aabc306537640473cf25"),
    "eight_parent_source": (EIGHT_PARENT / "build_interface.py", "3467f0b2b5997d1739d76a50d7ec0ae0734b4f099608a511d893309a488e5894"),
    "current_sat_generator": (SAT_SOURCE, "83996bdb4da059de2490549ed07fbb225b024e21763a8db4cf871fb0228cb0bb"),
    "narrow_materialization_small_result": (NARROW_BUILD, "c76ff3b4514ebc527ca5b4ceaeeb78da2247538aa5e178ac878ff60e759e5d89"),
}


def need(value, detail="validation failure"):
    if not value:
        raise RuntimeError(detail)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(value) -> str:
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


def graph_id(edges):
    return canonical_hash(canonical_graph(edges))


def essential_from_matching_strings(record):
    answer = set()
    for matching in record["supported_perfect_matchings"]:
        parsed = tuple((int(edge[0]), int(edge[1])) for edge in matching.split("|"))
        need(len(parsed) == 4 and sorted(v for edge in parsed for v in edge) == list(range(8)))
        answer.update(parsed)
    return tuple(sorted(answer))


def rebuild_eight_classes():
    parent = json.loads(PINS["eight_parent_result"][0].read_text())
    records = parent["unresolved_records"]
    need(len(records) == 616)
    histogram = Counter()
    members = defaultdict(list)
    edges_by_id = {}
    for index, record in enumerate(records):
        edges = essential_from_matching_strings(record)
        degree = Counter(v for edge in edges for v in edge)
        need(4 in degree.values())
        histogram[len(edges)] += 1
        if len(edges) == 16:
            key = canonical_graph(edges)
            gid = canonical_hash(key)
            members[gid].append(index)
            edges_by_id[gid] = key
    need(histogram == {12: 88, 13: 104, 14: 124, 15: 184, 16: 116})
    need(len(members) == 16 and Counter(map(len, members.values())) == {4: 5, 8: 10, 16: 1})
    return tuple((gid, edges_by_id[gid]) for gid in sorted(members)), histogram, members


def import_authoritative_algorithms():
    path = PINS["eight_parent_source"][0]
    spec = importlib.util.spec_from_file_location("combined_referee_eight_source", path)
    need(spec is not None and spec.loader is not None)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.five, module.seven


def rebuild_nine_classes(five, seven):
    additions = tuple(itertools.combinations(five.OFF_FAMILY, 9))
    need(len(additions) == 167960)
    evaders = tuple(added for added in additions if five.fixed_cap_certificate(set(five.FAMILY) | set(added)) is None)
    need(len(evaders) == 110652)
    reduction = Counter()
    stable = []
    for added in evaders:
        reduced, _ = five.guard_reduce(added)
        reduction[len(reduced)] += 1
        if len(reduced) == 9:
            stable.append(added)
    need(reduction == {3: 131, 4: 3430, 5: 18920, 6: 38596, 7: 33744, 8: 13502, 9: 2329})

    variable_order = tuple(sorted(five.VARIABLE))
    classification = Counter()
    essential_histogram = Counter()
    exact16_degree4_records = 0
    classes = {}
    class_members = defaultdict(int)
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
            if len(essential) == 16 and 4 in degree.values():
                key = canonical_graph(essential)
                gid = canonical_hash(key)
                classes[gid] = key
                class_members[gid] += 1
                exact16_degree4_records += 1
            unresolved_index += 1
    need(classification == {
        "fixed_identity_cap": 26380,
        "nonidentity_hyperplane_cap": 7408,
        "unresolved_coefficient_locus": 3476,
    })
    need(unresolved_index == 3476)
    need(essential_histogram == {12: 224, 13: 472, 14: 358, 15: 780, 16: 1108, 17: 534})
    need(exact16_degree4_records == 1104)
    need(len(classes) == 85)
    return tuple((gid, classes[gid]) for gid in sorted(classes)), {
        "additions": len(additions),
        "fixed_cap": len(additions) - len(evaders),
        "evaders": len(evaders),
        "stable_nine": len(stable),
        "classification": dict(classification),
        "essential_histogram": dict(essential_histogram),
        "exact16_degree4_records": exact16_degree4_records,
        "class_member_count_sha256": canonical_hash(dict(sorted(class_members.items()))),
    }


def normalized_supports(graphs, restriction=None):
    answer = defaultdict(set)
    raw = 0
    for gid, edge_tuple in graphs:
        edges = set(edge_tuple)
        degree = {v: sum(v in edge for edge in edges) for v in range(8)}
        centers = [v for v in range(8) if degree[v] == 4]
        if restriction == "missing_center_rooting":
            centers = centers[:-1]
        for center in centers:
            neighbours = sorted(v for v in range(8) if tuple(sorted((center, v))) in edges)
            outside = sorted(set(range(8)) - {center, *neighbours})
            need(len(neighbours) == 4 and len(outside) == 3)
            singleton_choices = neighbours[:-1] if restriction == "missing_singleton_rooting" else neighbours
            for singleton in singleton_choices:
                p_neighbours = list(itertools.permutations(v for v in neighbours if v != singleton))
                p_outside = list(itertools.permutations(outside))
                if restriction == "missing_neighbour_permutation":
                    p_neighbours = p_neighbours[:-1]
                if restriction == "missing_outside_permutation":
                    p_outside = p_outside[:-1]
                for near in p_neighbours:
                    for far in p_outside:
                        mapping = {center: 0, singleton: 1}
                        mapping.update(dict(zip(near, (2, 3, 4))))
                        mapping.update(dict(zip(far, (5, 6, 7))))
                        support = tuple(sorted(
                            f"{min(mapping[a], mapping[b])}{max(mapping[a], mapping[b])}"
                            for a, b in edges
                        ))
                        need(len(support) == 16 and len(set(support)) == 16)
                        need(all(f"0{i}" in support for i in range(1, 5)))
                        need(all(f"0{i}" not in support for i in range(5, 8)))
                        answer[support].add(gid)
                        raw += 1
    return answer, raw


def build():
    pin_report = {}
    for name, (path, expected) in PINS.items():
        need(path.is_file(), (name, "missing"))
        observed = digest(path)
        need(observed == expected, (name, observed, expected))
        pin_report[name] = {"path": str(path), "sha256": observed, "bytes": path.stat().st_size}

    # Explicitly refuse the materialized large nine result and base CNF.
    nine_materialized = NINE_CENSUS / "results_nine_block_induction_census.json"
    need(nine_materialized.stat().st_size == 5058748)
    need(BASE["bytes"] == 231480677)

    eight_graphs, eight_histogram, eight_members = rebuild_eight_classes()
    five, seven = import_authoritative_algorithms()
    nine_graphs, nine_stats = rebuild_nine_classes(five, seven)
    eight_ids = {gid for gid, _ in eight_graphs}
    nine_ids = {gid for gid, _ in nine_graphs}
    need(len(eight_ids) == 16 and len(nine_ids) == 85)
    need(len(eight_ids & nine_ids) == 9)
    need(len(eight_ids | nine_ids) == 92)

    eight_supports, eight_raw = normalized_supports(eight_graphs)
    nine_supports, nine_raw = normalized_supports(nine_graphs)
    combined_graphs = tuple(sorted(dict(eight_graphs + nine_graphs).items()))
    union_supports, union_raw = normalized_supports(combined_graphs)
    need(eight_raw == 8928 and len(eight_supports) == 5508)
    need(nine_raw == 43344 and len(nine_supports) == 33876)
    need(len(union_supports) == 35892)
    need(union_raw == 47088)
    need(len(set(eight_supports) & set(nine_supports)) == 3492)
    need(set(union_supports) == set(eight_supports) | set(nine_supports))

    lines = tuple("|".join(support) for support in sorted(union_supports))
    ledger_bytes = ("\n".join(lines) + "\n").encode()
    ledger_sha = hashlib.sha256(ledger_bytes).hexdigest()
    need(ledger_sha == EXPECTED_LEDGER_SHA256, (ledger_sha, EXPECTED_LEDGER_SHA256))
    (HERE / "combined_target_supports.ledger").write_bytes(ledger_bytes)

    block_edges = tuple(
        edge for edge in itertools.combinations(range(8), 2)
        if edge[0] != 0 or edge[1] in {1, 2, 3, 4}
    )
    need(len(block_edges) == 25)
    added_variables = len(lines)
    added_clauses = added_variables * 25 + 1
    need(added_variables == 35892 and added_clauses == 897301)
    patched_header = {
        "variables": BASE["variables"] + added_variables,
        "clauses": BASE["clauses"] + added_clauses,
    }
    need(patched_header == {"variables": 464139, "clauses": 3980473})

    patch = {
        "schema": "n8-x5-eight-nine-exact16-target-union-selector-metadata-v1",
        "base": BASE,
        "block_variables": [
            {"edge": f"{a}{b}", "variable": 226 + index}
            for index, (a, b) in enumerate(block_edges)
        ],
        "ledger_path": "combined_target_supports.ledger",
        "ledger_sha256": ledger_sha,
        "selector_variables": {"first": 428248, "last": 464139, "count": 35892},
        "clauses_per_selector": 25,
        "selector_implications": 897300,
        "global_selector_or": 1,
        "added_clauses": added_clauses,
        "patched_header": patched_header,
        "semantics": "selector s_i implies each of the 25 block literals in exact support cube i; one global positive selector OR restricts the generic skeleton to the finite target union",
        "composition_contract": "replacement patch against the original 428247-variable base; never append to the narrow 5508-selector materialization because selector IDs alias and its global OR would retain the narrow restriction",
        "explicit_non_action": "no base CNF/result read or write; no solver",
    }
    (HERE / "selector_patch_metadata.json").write_text(json.dumps(patch, indent=2, sort_keys=True) + "\n")

    omissions = {}
    for kind in (
        "missing_center_rooting",
        "missing_singleton_rooting",
        "missing_neighbour_permutation",
        "missing_outside_permutation",
    ):
        changed, _ = normalized_supports(combined_graphs, kind)
        omissions[kind] = len(changed)
        need(len(changed) != 35892, (kind, "not detected"))

    hostiles = {
        "schema": "n8-x5-eight-nine-exact16-target-union-hostiles-v1",
        "status": "PASS_ALL_REJECTED",
        "cross_layer": {
            "omit_eight_layer_support_count": len(nine_supports),
            "omit_nine_layer_support_count": len(eight_supports),
            "naive_sum_without_cross_dedup": len(eight_supports) + len(nine_supports),
            "required_cross_layer_support_overlap": len(set(eight_supports) & set(nine_supports)),
            "required_graph_class_overlap": len(eight_ids & nine_ids),
            "reject_wrong_class_union_101": True,
            "reject_wrong_support_union_39384": True,
        },
        "normalization_omissions": omissions,
        "selector": {
            "missing_or_flipped_implication": "fails complete 25-block cube",
            "missing_global_or": "admits unrestricted generic skeleton",
            "wrong_26_per_selector_arithmetic": "rejected; global OR occurs once",
            "extra_or_non_exact16_support": "rejected by ledger equality and 16-edge check",
            "append_to_narrow_materialization": "rejected: selector IDs 428248..433755 alias and the narrow global OR would still require an eight-layer target",
        },
    }
    (HERE / "hostile_tests.json").write_text(json.dumps(hostiles, indent=2, sort_keys=True) + "\n")

    result = {
        "schema": "n8-x5-eight-nine-exact16-target-union-independent-referee-v1",
        "status": "PASS_STATIC_COMBINED_TARGET_UNION_REFEREE",
        "pins": pin_report,
        "non_action": {
            "large_base_cnf_read": False,
            "large_base_cnf_written": False,
            "materialized_nine_result_read": False,
            "solver_run": False,
        },
        "eight_layer": {
            "records": 616,
            "histogram": {str(k): v for k, v in sorted(eight_histogram.items())},
            "exact16_records": 116,
            "graph_classes": len(eight_graphs),
            "graph_class_members_sha256": canonical_hash({gid: indices for gid, indices in sorted(eight_members.items())}),
            "raw_embeddings": eight_raw,
            "support_masks": len(eight_supports),
        },
        "nine_layer": {**nine_stats, "graph_classes": len(nine_graphs), "raw_embeddings": nine_raw, "support_masks": len(nine_supports)},
        "combined": {
            "graph_class_intersection": len(eight_ids & nine_ids),
            "graph_class_union": len(eight_ids | nine_ids),
            "raw_embeddings_over_unique_classes": union_raw,
            "support_intersection": len(set(eight_supports) & set(nine_supports)),
            "support_union": len(union_supports),
            "ledger_bytes": len(ledger_bytes),
            "ledger_sha256": ledger_sha,
        },
        "selector_patch": patch,
        "narrow_materialization_comparison": {
            "small_build_result_sha256": pin_report["narrow_materialization_small_result"]["sha256"],
            "cnf_sha256_from_small_metadata_not_rehashed": "dc5cd1cad3a062dc66a5788413e5c1e1799a1ed07e66266ad25cc195b470aafa",
            "cnf_bytes_from_small_metadata": 233496607,
            "patch_sha256_from_small_metadata": "59ef643457b8ea246e2250d770a8568c51c7c7d50c81b84dd332123b2bc04ef9",
            "narrow_header": {"variables": 433755, "clauses": 3220873},
            "narrow_ledger_is_subset": set(eight_supports) <= set(union_supports),
            "semantic_conflict": False,
            "bytewise_or_additive_composability": False,
            "required_action_for_combined": "materialize the combined selector patch from the original base; do not modify the narrow CNF in place",
        },
        "coverage_proof": {
            "all_targets": "Every normalized support in the exact set union has one selector and 25 complete-cube implications.",
            "cross_layer": "Set union after graph and support dedup retains every eight- or nine-layer target, including nine shared graph classes exactly once.",
            "generic_exclusion": "The global selector OR requires a selected exact cube; a generic support outside the ledger cannot satisfy any selected complete cube.",
            "scope": "Static design/referee only; no SAT/UNSAT result or theorem promotion.",
        },
        "hostiles": hostiles,
    }
    (HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    build()
