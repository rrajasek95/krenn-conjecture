#!/usr/bin/env python3
"""Exact source/guard-proven nine-added-block induction census."""

from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
EIGHT = REPO / "computations/unaudited-codex-n8-x5-eight-block-first-induction-interface-2026-08-26"
SKELETON = REPO / "computations/unaudited-codex-n8-x5-eight-block-essential-skeleton-contraction-design-2026-08-26"
PINS = {
    "corrected_eight_manifest": (EIGHT / "MANIFEST.sha256", "4334804545c7f2a73189137f47bfa1105905db4d6b2c52de0d140217d9ae4a10"),
    "corrected_eight_result": (EIGHT / "results_eight_block_interface.json", "886ae50bede93dd21bf0ea5dda7ed9154a58a9caf532aabc306537640473cf25"),
    "corrected_eight_source": (EIGHT / "build_interface.py", "3467f0b2b5997d1739d76a50d7ec0ae0734b4f099608a511d893309a488e5894"),
    "eight_skeleton_manifest": (SKELETON / "MANIFEST.sha256", "bef35566e155115f3411d02c511c381390cb4ea013212ad2f3cda19ed9adc270"),
    "eight_skeleton_result": (SKELETON / "results_essential_skeleton_contraction_design.json", "81e48158bb12bb9d44389fe68178b4f4a01b9d824bd96af0f7fdb09184fcd02c"),
}


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


for name, (path, expected) in PINS.items():
    require(path.is_file(), (name, "missing"))
    require(sha(path) == expected, (name, sha(path), expected))

spec = importlib.util.spec_from_file_location("corrected_eight", EIGHT / "build_interface.py")
require(spec is not None and spec.loader is not None)
eight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eight)
five = eight.five
seven = eight.seven


def es(edge):
    return five.edge_string(edge)


def essential_skeleton(support):
    matchings = tuple(matching for matching in five.core.PM8 if set(matching) <= support)
    edges = tuple(sorted(set(edge for matching in matchings for edge in matching)))
    degree = Counter(vertex for edge in edges for vertex in edge)
    require(set(degree) == set(range(8)))
    return matchings, edges, degree


def canonical_graph(edges):
    """Exhaustive unlabelled key using invariant degree cells."""
    degree = {vertex: sum(vertex in edge for edge in edges) for vertex in range(8)}
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


def make_result():
    parent = json.loads((EIGHT / "results_eight_block_interface.json").read_text())
    require(parent["enumeration"]["unresolved_strata"] == 616)
    eight_unresolved = {
        (
            tuple(tuple(map(int, edge)) for edge in record["added"]),
            frozenset(tuple(map(int, edge)) for edge in record["nonzero_variable_blocks"]),
        )
        for record in parent["unresolved_records"]
    }
    require(len(eight_unresolved) == 616)

    additions = tuple(itertools.combinations(five.OFF_FAMILY, 9))
    fixed_count = 0
    evaders = []
    for added in additions:
        if five.fixed_cap_certificate(set(five.FAMILY) | set(added)) is None:
            evaders.append(added)
        else:
            fixed_count += 1
    require(len(additions) == 167960)
    require(fixed_count == 57308 and len(evaders) == 110652)

    reduction = Counter()
    stable = []
    for added in evaders:
        reduced, _steps = five.guard_reduce(added)
        reduction[len(reduced)] += 1
        if len(reduced) == 9:
            stable.append(added)
    require(dict(sorted(reduction.items())) == {3: 131, 4: 3430, 5: 18920, 6: 38596, 7: 33744, 8: 13502, 9: 2329})

    variable_order = tuple(sorted(five.VARIABLE))
    classification = Counter()
    unresolved = []
    for added in stable:
        for mask in range(16):
            variables = frozenset(variable_order[i] for i in range(4) if mask & (1 << i))
            support = set(five.FIXED) | set(variables) | set(added)
            if five.fixed_cap_certificate(support) is not None:
                kind = "fixed_identity_cap"
            elif seven.nonidentity_certificates(support):
                kind = "nonidentity_hyperplane_cap"
            else:
                kind = "unresolved_coefficient_locus"
                unresolved.append((added, variables, support))
            classification[kind] += 1
    require(classification == {
        "fixed_identity_cap": 26380,
        "nonidentity_hyperplane_cap": 7408,
        "unresolved_coefficient_locus": 3476,
    })

    details = []
    parent_count = Counter()
    essential_histogram = Counter()
    matching_histogram = Counter()
    raw_histogram = Counter()
    degree_histogram = Counter()
    degree_four_count = 0
    graph_cache = {}
    graph_members = {}
    keys = set()
    for index, (added, variables, support) in enumerate(unresolved):
        key = (added, variables)
        require(key not in keys)
        keys.add(key)
        parents = []
        for edge in added:
            parent_added = tuple(item for item in added if item != edge)
            if (parent_added, variables) in eight_unresolved:
                parents.append({"deleted_edge": es(edge), "eight_added": list(map(es, parent_added))})
        parent_count[len(parents)] += 1
        matchings, essential, degree = essential_skeleton(support)
        essential_histogram[len(essential)] += 1
        matching_histogram[len(matchings)] += 1
        raw_histogram[len(support)] += 1
        degree_histogram[tuple(sorted(degree.values()))] += 1
        has_degree_four = 4 in degree.values()
        degree_four_count += int(has_degree_four)
        if essential not in graph_cache:
            graph_cache[essential] = canonical_graph(essential)
        graph_id = canonical_hash(graph_cache[essential])
        graph_members.setdefault(graph_id, {"canonical": graph_cache[essential], "members": []})["members"].append(index)
        details.append({
            "record_index": index,
            "added": list(map(es, added)),
            "nonzero_variable_blocks": list(map(es, sorted(variables))),
            "raw_support_count": len(support),
            "supported_perfect_matching_count": len(matchings),
            "essential_edges": list(map(es, essential)),
            "essential_edge_count": len(essential),
            "degree_sequence": list(sorted(degree.values())),
            "degree_four_vertices": sorted(v for v, d in degree.items() if d == 4),
            "has_degree_four_vertex": has_degree_four,
            "unresolved_eight_deletion_parents": parents,
            "unlabelled_graph_id": graph_id,
        })

    require(parent_count == {0: 920, 1: 732, 2: 1412, 3: 364, 4: 48})
    require(essential_histogram == {12: 224, 13: 472, 14: 358, 15: 780, 16: 1108, 17: 534})
    require(matching_histogram == {8: 236, 9: 56, 10: 460, 11: 528, 12: 602, 13: 510, 14: 474, 15: 150, 16: 208, 17: 152, 18: 90, 20: 10})
    require(raw_histogram == {13: 32, 14: 264, 15: 1148, 16: 1474, 17: 558})
    require(len(graph_members) == 191)
    require(degree_four_count == 3472)

    # Exact order-two source/guard symmetry.  Unlike the eight layer, fixed
    # records occur and must remain singleton orbits.
    seen = set()
    guard_orbits = []
    for key in sorted(keys, key=lambda item: (item[0], sorted(item[1]))):
        if key in seen:
            continue
        mate = (five.permute_support(key[0]), seven.permute_variables(key[1]))
        require(mate in keys, ("missing guard mate", key))
        members = tuple(sorted({key, mate}, key=lambda item: (item[0], sorted(item[1]))))
        seen.update(members)
        member_indices = []
        for member in members:
            # Deterministic lookup is small enough and keeps the source plain.
            member_indices.append(next(i for i, triple in enumerate(unresolved) if (triple[0], triple[1]) == member))
        guard_orbits.append({"orbit_id": len(guard_orbits), "record_indices": member_indices})
    require(seen == keys)
    require(len(guard_orbits) == 1778)
    require(Counter(map(lambda orbit: len(orbit["record_indices"]), guard_orbits)) == {1: 80, 2: 1698})

    new_indices = {detail["record_index"] for detail in details if not detail["unresolved_eight_deletion_parents"]}
    parented_indices = set(range(len(details))) - new_indices
    require(len(new_indices) == 920 and len(parented_indices) == 2556)
    new_graphs = {details[i]["unlabelled_graph_id"] for i in new_indices}
    parented_graphs = {details[i]["unlabelled_graph_id"] for i in parented_indices}
    require(len(new_graphs) == 83 and len(parented_graphs) == 163)

    def subset_summary(indices):
        edge_hist = Counter(details[i]["essential_edge_count"] for i in indices)
        max15 = sum(details[i]["has_degree_four_vertex"] and details[i]["essential_edge_count"] <= 15 for i in indices)
        exact16 = sum(details[i]["has_degree_four_vertex"] and details[i]["essential_edge_count"] == 16 for i in indices)
        outside = len(indices) - max15 - exact16
        return {
            "records": len(indices),
            "essential_edge_histogram": {str(k): v for k, v in sorted(edge_hist.items())},
            "with_degree_four_vertex": sum(details[i]["has_degree_four_vertex"] for i in indices),
            "without_degree_four_vertex": sum(not details[i]["has_degree_four_vertex"] for i in indices),
            "at_most15_eligible": max15,
            "exact16_additional_eligible": exact16,
            "max16_cumulative_eligible": max15 + exact16,
            "remaining_exact17": edge_hist[17],
            "remaining_after_max16": outside,
            "unlabelled_graph_classes": len({details[i]["unlabelled_graph_id"] for i in indices}),
        }

    all_indices = set(range(len(details)))
    all_summary = subset_summary(all_indices)
    new_summary = subset_summary(new_indices)
    parented_summary = subset_summary(parented_indices)
    require(all_summary["at_most15_eligible"] == 1834)
    require(all_summary["exact16_additional_eligible"] == 1104)
    require(all_summary["remaining_exact17"] == 534)
    require(new_summary["at_most15_eligible"] == 598 and new_summary["exact16_additional_eligible"] == 242 and new_summary["remaining_exact17"] == 80)

    return {
        "schema": "n8-x5-nine-block-induction-census-design-v1",
        "status": "PASS_EXACT_CENSUS_ZERO_SOLVER",
        "pins": {name: {"path": str(path), "sha256": expected} for name, (path, expected) in PINS.items()},
        "enumeration": {
            "nine_added_supports": len(additions),
            "fixed_identity_closed": fixed_count,
            "fixed_identity_evaders": len(evaders),
            "guard_reduced_size_census": {str(k): v for k, v in sorted(reduction.items())},
            "stable_nine_supports": len(stable),
            "stable_variable_strata": len(stable) * 16,
            "classification_census": dict(classification),
            "unresolved_records": len(details),
            "unresolved_record_sha256": canonical_hash(details),
        },
        "deletion_parent_census": {
            "unresolved_eight_parent_count_histogram": {str(k): v for k, v in sorted(parent_count.items())},
            "with_at_least_one_unresolved_eight_parent": len(parented_indices),
            "genuinely_new_minimal_records": len(new_indices),
            "new_record_indices_sha256": canonical_hash(sorted(new_indices)),
            "scope": "parent relation only; no deletion-monotonicity implication",
        },
        "matching_essential_census": {
            "definition": "union of edges occurring in a supported perfect matching",
            "with_degree_four_vertex": degree_four_count,
            "without_degree_four_vertex": len(details) - degree_four_count,
            "essential_edge_histogram": {str(k): v for k, v in sorted(essential_histogram.items())},
            "supported_matching_histogram": {str(k): v for k, v in sorted(matching_histogram.items())},
            "raw_support_histogram": {str(k): v for k, v in sorted(raw_histogram.items())},
            "degree_sequence_histogram": {str(k): v for k, v in sorted(degree_histogram.items())},
            "unlabelled_graph_classes": len(graph_members),
            "literal_guard_orbits": len(guard_orbits),
            "guard_orbit_size_census": {str(k): v for k, v in sorted(Counter(len(o["record_indices"]) for o in guard_orbits).items())},
            "unique_labelled_essential_skeletons": len(graph_cache),
        },
        "frontier_interface_test": {
            "all_unresolved": all_summary,
            "genuinely_new": new_summary,
            "with_unresolved_eight_parent": parented_summary,
            "max15_status": "CONDITIONAL_ONLY_PENDING_TERMINAL_CURRENT_CNF_DRAT_SEAL",
            "max16_status": "HYPOTHESIS_ONLY_NOT_IMPORTED_OR_REPLAYED",
            "accepted_coverage_now": 0,
            "conditional_if_max15_terminal": 1834,
            "conditional_if_max15_and_max16_terminal": 2938,
            "still_open_after_max16": 538,
            "still_open_breakdown": {"exact17_with_degree4": 534, "exact16_without_degree4": 4},
            "exact17_note": "separate upstream interface; not requested, imported, or promoted here",
        },
        "unlabelled_graph_classes": [
            {
                "graph_id": graph_id,
                "canonical_edges": [list(edge) for edge in value["canonical"]],
                "record_indices": value["members"],
            }
            for graph_id, value in sorted(graph_members.items())
        ],
        "literal_guard_orbits": guard_orbits,
        "records": details,
        "scope": {
            "source_and_guard_provenance_only": True,
            "heavy_solver_runs": 0,
            "singular_runs": 0,
            "external_frontier_theorem_promoted": False,
            "deletion_monotonicity_claim": False,
            "nine_block_layer_closed": False,
            "full_conjecture_claim": False,
        },
    }


if __name__ == "__main__":
    result = make_result()
    (HERE / "results_nine_block_induction_census.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "unresolved": result["enumeration"]["unresolved_records"],
        "parented": result["deletion_parent_census"]["with_at_least_one_unresolved_eight_parent"],
        "new": result["deletion_parent_census"]["genuinely_new_minimal_records"],
        "essential": result["matching_essential_census"]["essential_edge_histogram"],
        "graph_classes": result["matching_essential_census"]["unlabelled_graph_classes"],
        "guard_orbits": result["matching_essential_census"]["literal_guard_orbits"],
        "frontier": result["frontier_interface_test"],
    }, indent=2, sort_keys=True))
