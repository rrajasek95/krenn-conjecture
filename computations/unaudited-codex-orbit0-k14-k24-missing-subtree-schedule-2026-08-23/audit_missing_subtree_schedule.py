#!/usr/bin/env python3
"""Read-only execution schedule for the discarded K14/K2 K16 subtree."""

from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FILES = {
    "dag": ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json",
    "k16_literal": ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json",
    "arithmetic": ROOT / "computations/unaudited-codex-orbit0-k19-k24-arithmetic-plan-2026-08-23/results_k19_k24_arithmetic.json",
    "supersession": ROOT / "computations/unaudited-codex-orbit0-hidden-k14-charge-supersession-2026-08-23/results_hidden_k14_charge_supersession.json",
    "reducer_design": ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/results_filtered_k24_reducer_design.json",
}
OUT = HERE / "results_missing_subtree_schedule.json"

TAIL_COUNTS = {2: 12, 3: 32, 4: 60}
ROOT_PARENT = "D14:222|R:2"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def build(mutate=False):
    data = {name: json.loads(path.read_text()) for name, path in FILES.items()}
    dag = data["dag"]
    require(dag["logical_sha256"] ==
            "ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66",
            dag["logical_sha256"])
    require(data["supersession"]["status"] ==
            "RETRACT_FULL_K18_K19_CHARGES_AND_CUMULATIVE_LEDGERS",
            data["supersession"]["status"])
    root_raw = data["k16_literal"]["collection"]["reducible_K16_tail_occurrences"]
    root_pivot_uses = data["k16_literal"]["collection"]["literal_pivot_uses"]
    root_irreducible = data["k16_literal"]["collection"][
        "irreducible_K16_tail_occurrences_before_collection"]
    root_pairs = data["k16_literal"]["input"]["factored_H_slice_pairs"]
    require((root_pairs, root_pivot_uses, root_raw, root_irreducible) ==
            (838_080, 6_619_280, 75_691_040, 3_740_320),
            (root_pairs, root_pivot_uses, root_raw, root_irreducible))
    require(root_pivot_uses * 12 == root_raw + root_irreducible,
            (root_pivot_uses, root_raw, root_irreducible))

    nodes = {node["id"]: node for node in dag["nodes"]}
    missing = {
        node_id for node_id, node in nodes.items()
        if node["reachable"] and
        node["current_provenance"]["state"] ==
        "MISSING_DISCARDED_K14_K2_PIVOTABLE_PARENT"
    }
    require(len(missing) == 15, len(missing))
    if mutate:
        missing.remove("D14:222|R:2-2-2")

    required_missing = {
        "D14:222|R:2-2", "D14:222|R:2-3", "D14:222|R:2-4",
        "D14:222|R:2-2-2", "D14:222|R:2-2-3", "D14:222|R:2-2-4",
        "D14:222|R:2-3-2", "D14:222|R:2-3-3", "D14:222|R:2-3-4",
        "D14:222|R:2-4-2", "D14:222|R:2-4-3", "D14:222|R:2-4-4",
        "D14:222|R:2-2-2-2", "D14:222|R:2-2-2-3",
        "D14:222|R:2-2-2-4",
    }
    require(missing == required_missing,
            {"missing": sorted(required_missing - missing),
             "unexpected": sorted(missing - required_missing)})

    edge_map = defaultdict(list)
    for edge in dag["edges"]:
        if edge["parent"] == ROOT_PARENT or edge["parent"] in missing:
            if edge["child"] in missing:
                edge_map[edge["parent"]].append(edge)
    for edges in edge_map.values():
        edges.sort(key=lambda row: row["shift"])

    materialized = [
        ROOT_PARENT,
        "D14:222|R:2-2",
        "D14:222|R:2-3",
        "D14:222|R:2-4",
        "D14:222|R:2-2-2",
    ]
    require(set(edge_map) == set(materialized), sorted(edge_map))
    terminal = sorted(missing - set(materialized),
                      key=lambda node_id: (nodes[node_id]["degree"], node_id))
    # The root is a prerequisite, not one of the 15 missing descendants.
    require(len(materialized) == 5 and len(terminal) == 11,
            (materialized, terminal))

    max_pivots = {
        int(degree): max(map(int, histogram))
        for degree, histogram in data["arithmetic"][
            "all_pivot_count_histogram_by_parent_degree"].items()
    }
    require({degree: max_pivots[degree] for degree in (16, 18, 19, 20)} ==
            {16: 16, 18: 4, 19: 2, 20: 1}, max_pivots)

    parent_pages = []
    for parent in materialized:
        node = nodes[parent]
        children = []
        for edge in edge_map[parent]:
            children.append({
                "lineage_id": edge["child"],
                "degree": nodes[edge["child"]]["degree"],
                "shift": edge["shift"],
                "tail_terms_per_pivot": edge["tail_terms_per_pivot"],
                "must_materialize_as_parent": edge["child"] in materialized,
                "terminal_profile_only_allowed": edge["child"] in terminal,
            })
        parent_pages.append({
            "lineage_id": parent,
            "degree": node["degree"],
            "reachable_anchor_signatures": node["reachable_anchor_signatures"],
            "maximum_dividing_pivots_per_labelled_row": max_pivots[node["degree"]],
            "denominator_product_class": node["denominator_product_class"],
            "children": children,
            "exact_work_formula": (
                "For merged parent H-orbits r, let L=SUM |H.r| and "
                "V=SUM |H.r|*pivots(r). Child tail evaluations are "
                "12V, 32V, 60V; V<=(maximum_dividing_pivots)*L."
            ),
        })

    record_bytes = 24 + 16  # total-degree-24 row + signed scaled i128
    root_payload = root_raw * record_bytes
    root_merge_peak = 2 * root_payload
    root_labelled_upper = root_raw * 384
    root_pivot_visit_upper = root_labelled_upper * max_pivots[16]

    stages = [
        {
            "order": 0,
            "name": "replay_and_retain_discarded_K16_parent",
            "input": "frozen K14 direct packet 222 and valid-K14 pivot policy",
            "output_checkpoint": ROOT_PARENT,
            "exact_known_work": {
                "factored_H_slice_pairs": root_pairs,
                "K14_pivot_uses": root_pivot_uses,
                "K2_tail_evaluations": root_pivot_uses * 12,
                "discarded_pivotable_K16_occurrences_to_retain": root_raw,
                "simultaneous_irreducible_control_occurrences": root_irreducible,
            },
            "disk_bound": {
                "fixed_scale_record_bytes": record_bytes,
                "unmerged_payload_bytes_upper": root_payload,
                "unmerged_payload_GiB_upper": root_payload / 2**30,
                "two_generation_merge_payload_bytes_upper": root_merge_peak,
                "two_generation_merge_payload_GiB_upper": root_merge_peak / 2**30,
                "qualification": "payload only; excludes hash index, allocator, and run metadata",
            },
        },
        {
            "order": 1,
            "name": "reduce_merged_K16_parent_once",
            "input_checkpoint": ROOT_PARENT,
            "outputs": [edge["child"] for edge in edge_map[ROOT_PARENT]],
            "action": (
                "Expand each complete H-orbit, average over all dividing K0 pivots, "
                "and emit K2/K3/K4 children together so the orbit traversal is shared."
            ),
            "hostile_only_upper_bound": {
                "labelled_parent_visits": root_labelled_upper,
                "pivot_visits": root_pivot_visit_upper,
                "K18_tail_evaluations": root_pivot_visit_upper * 12,
                "K19_tail_evaluations": root_pivot_visit_upper * 32,
                "K20_tail_evaluations": root_pivot_visit_upper * 60,
                "qualification": (
                    "Uses 384 orbit size and 16 pivots for every surviving parent; "
                    "do not use as an expected cost. The merged checkpoint must publish exact L and V before expansion."
                ),
            },
        },
        {
            "order": 2,
            "name": "consume_terminal_first_level_parents_before_K18",
            "inputs": ["D14:222|R:2-3", "D14:222|R:2-4"],
            "reason": (
                "Their children are all terminal. Processing and deleting these two "
                "buckets before K18 prevents the new K20 [2,2,2] bucket from overlapping them on disk."
            ),
        },
        {
            "order": 3,
            "name": "reduce_K18_and_materialize_its_K20_child",
            "input": "D14:222|R:2-2",
            "materialized_output": "D14:222|R:2-2-2",
            "profile_only_outputs": ["D14:222|R:2-2-3", "D14:222|R:2-2-4"],
        },
        {
            "order": 4,
            "name": "reduce_final_K20_parent",
            "input": "D14:222|R:2-2-2",
            "profile_only_outputs": [
                "D14:222|R:2-2-2-2", "D14:222|R:2-2-2-3",
                "D14:222|R:2-2-2-4",
            ],
        },
        {
            "order": 5,
            "name": "coverage_and_charge_reconciliation",
            "condition": (
                "All 15 lineage IDs have accepted manifests; only then may their exact "
                "profile charges be added to the previously visible partial subtotals."
            ),
        },
    ]

    result = {
        "status": "PASS_MINIMAL_PROVENANCE_COMPLETE_MISSING_SUBTREE_SCHEDULE_NO_RUN",
        "scope": (
            "Execution plan for the 15 missing descendants of the discarded K14/K2 "
            "K16 subtree under the frozen valid-K14/all-dividing-later pivot policy. "
            "No residual or charge was computed."
        ),
        "coverage": {
            "missing_descendant_count": len(missing),
            "missing_lineage_ids": sorted(missing),
            "by_degree": {
                str(degree): sorted(node_id for node_id in missing
                                    if nodes[node_id]["degree"] == degree)
                for degree in range(18, 25)
            },
        },
        "checkpoint_policy": {
            "full_row_parent_checkpoints": materialized,
            "full_row_parent_count": len(materialized),
            "terminal_response_lineages": terminal,
            "terminal_response_count": len(terminal),
            "record": (
                "24-byte canonical H-row plus signed i128 coefficient per labelled row "
                "at U=400591699200; lineage is encoded by the file/manifest, not per record"
            ),
            "lifecycle": (
                "A parent checkpoint may be deleted only after every child manifest, "
                "terminal 77-bin profile, and replay digest named by its DAG edges is accepted."
            ),
            "fused_stream_exception": (
                "A full parent file may be replaced by a transactionally journaled source-linear "
                "stream only if its upstream SHA/cursor, complete row support, exact pivot histogram, "
                "and all child manifests are sufficient to replay that page independently."
            ),
        },
        "profile_only_scope": {
            "sufficient_for": (
                "the frozen 77-cycle functional: every terminal K>=21 child and every "
                "irreducible normal at K18/K19/K20 may be accumulated as a signed 77-bin "
                "cycle-partition histogram plus scalar pairing"
            ),
            "not_sufficient_for": (
                "literal residual reconstruction, a different quotient, or cross-lineage row support; "
                "those goals require retaining the corresponding full H-row checkpoint"
            ),
            "terminal_profile_payload": "77 signed i128 bins = 1232 bytes per lineage, before metadata",
        },
        "parent_pages": parent_pages,
        "stages": stages,
        "exact_stop_replay_assertions": [
            "Pin every upstream byte/logical digest and the DAG logical digest before opening an output run.",
            "The root replay must reproduce 838080 pairs, 6619280 K14 pivot uses, 79431360 K2 evaluations, split exactly 75691040 pivotable plus 3740320 irreducible.",
            "Every stored row has total degree 24, the declared K-degree and lineage, is H-canonical, and has nonzero exact scaled coefficient only after signed merge.",
            "At every pivot assert U mod accumulated_denominator_product == 0; the observed product must belong to that DAG node's exact product set.",
            "For each parent publish H-orbit count, labelled support L, pivot histogram, V=sum orbit_size*pivot_count, and assert child evaluation counts 12V/32V/60V before launching children.",
            "Use parent c -> child -c/pivot_count and assert the child sign equals the DAG sign; abort on the first sign or exact-division mismatch.",
            "Atomic checkpoints contain upstream SHA, byte cursor with no gaps/overlap, run SHAs, exact counts/mass/L1, and a completed flag; incomplete runs are never accepted as parents.",
            "Every K>=21 terminal child must have zero literal K0 pivots; every retained K18/K19/K20 normal row must also be K0-irreducible.",
            "The interface verifier must see exactly all 15 missing lineage IDs with evidence digests; a missing [2,2,2] path is the hostile must-fail mutation.",
            "Do not restore a full K18/K19/cumulative charge claim until all 15 manifests and terminal profiles pass exact replay.",
        ],
        "known_costs_and_bounds": {
            "root_replay": stages[0]["exact_known_work"],
            "root_checkpoint_disk": stages[0]["disk_bound"],
            "later_exact_cost_formula": (
                "For parent checkpoint d with V_d=sum |H.r|*pivots(r), raw child "
                "evaluations are 12V_d,32V_d,60V_d. Collected disk is 40*N_child "
                "bytes where N_child is the nonzero H-orbit count after exact merge."
            ),
            "later_counts_currently_unknown": True,
            "reason": (
                "The discarded K16 parent coefficients/orbits were never collected; signature "
                "reachability does not determine coefficient cancellations or H-orbit counts."
            ),
        },
        "pinned": {str(path.relative_to(ROOT)): digest(path)
                   for path in FILES.values()},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--hostile", action="store_true")
    args = parser.parse_args()
    result = build(mutate=args.hostile)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "coverage": result["coverage"],
        "full_row_parent_checkpoints": result["checkpoint_policy"]["full_row_parent_checkpoints"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

