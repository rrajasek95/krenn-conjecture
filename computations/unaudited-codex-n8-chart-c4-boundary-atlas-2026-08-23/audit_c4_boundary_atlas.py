#!/usr/bin/env python3
"""Exact marked-boundary orbit census for the 31-chart C4 atlas.

The datum being quotiented is a source pure-matching chart, a labelled
one-colour C4 flip, and either one or both entering cells marked zero.  The
quotient is by the full stabilizer of the source chart in S8 x S3.  This is
the precise divisor missed by the Laurent transition; it makes no assertion
that the mixed-zero scheme meets that divisor.
"""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TRANSITION_PATH = (
    ROOT / "computations/unaudited-codex-n8-chart-c4-transition-2026-08-23"
    / "audit_chart_c4_transition.py"
)
RESULT = HERE / "results_c4_boundary_atlas.json"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


ATLAS = load(TRANSITION_PATH, "c4_transition_authority")
SOURCE = ATLAS.CHART.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def enumerate_vertex_isomorphisms(source, target):
    """List vertex maps carrying a colour-fixed port matching to target."""
    mapping = {}
    used = set()
    answer = []

    def search():
        if len(mapping) == 8:
            answer.append(tuple(mapping[index] for index in range(8)))
            return
        source_root = min(set(range(8)) - set(mapping))
        for target_root in sorted(set(range(8)) - used):
            added = SOURCE.propagate_component(
                source, target, source_root, target_root, mapping, used
            )
            if added is not None:
                search()
                for left, right in reversed(added):
                    mapping.pop(left)
                    used.remove(right)

    search()
    return tuple(answer)


def stabilizer(key):
    mate = SOURCE.decode_key(key)
    answer = []
    for colour_permutation in SOURCE.COLOUR_PERMUTATIONS:
        changed = SOURCE.colour_transform(mate, colour_permutation)
        for vertex_permutation in enumerate_vertex_isomorphisms(changed, mate):
            answer.append((vertex_permutation, colour_permutation))
    require(len(answer) == SOURCE.stabilizer_order(key),
            "explicit stabilizer disagrees with certified order")
    return tuple(answer)


def transform_edge(edge, group_element):
    vp, cp = group_element
    answer = []
    for port in edge:
        vertex, colour = divmod(port, 3)
        answer.append(3 * vp[vertex] + cp[colour])
    return tuple(sorted(answer))


def flip_records(triple):
    source_support = ATLAS.support(triple)
    answer = []
    for colour, matching in enumerate(triple):
        for left in range(4):
            for right in range(left + 1, 4):
                (a, b), (c, d) = matching[left], matching[right]
                for replacement in (((a, c), (b, d)), ((a, d), (b, c))):
                    changed = list(matching)
                    changed[left] = tuple(sorted(replacement[0]))
                    changed[right] = tuple(sorted(replacement[1]))
                    updated = list(triple)
                    updated[colour] = tuple(sorted(changed))
                    target = tuple(updated)
                    target_support = ATLAS.support(target)
                    entering = tuple(sorted(target_support - source_support))
                    leaving = tuple(sorted(source_support - target_support))
                    require(len(entering) == len(leaving) == 2,
                            "labelled move is not a C4 flip")
                    answer.append({
                        "target": target,
                        "entering": entering,
                        "leaving": leaving,
                    })
    require(len(answer) == 36, "source chart lost a labelled flip")
    require(len({(item["entering"], item["leaving"]) for item in answer}) == 36,
            "labelled flips unexpectedly repeat")
    return tuple(answer)


def state_key(record, zero, group_element=None):
    if group_element is None:
        leaving = record["leaving"]
        entering = record["entering"]
        marked = zero
    else:
        leaving = tuple(sorted(transform_edge(e, group_element)
                               for e in record["leaving"]))
        entering = tuple(sorted(transform_edge(e, group_element)
                                for e in record["entering"]))
        marked = tuple(sorted(transform_edge(e, group_element) for e in zero))
    return leaving, entering, marked


def canonical_state(record, zero, group):
    return min(state_key(record, zero, element) for element in group)


def component_sizes_from_triple(triple):
    return ATLAS.CHART.component_sizes(ATLAS.support(triple))


def main():
    rows = tuple(sorted(SOURCE.target_orbit_rows()))
    row_index = {row: index for index, row in enumerate(rows, 1)}
    per_chart = []
    graph = defaultdict(set)
    global_states = []
    edge_labelled_multiplicity = Counter()

    for chart_id, row in enumerate(rows, 1):
        triple = ATLAS.chart_triple(row)
        group = stabilizer(row)
        raw = []
        for record in flip_records(triple):
            destination = row_index[ATLAS.chart_key(record["target"])]
            graph[chart_id].add(destination)
            graph[destination].add(chart_id)
            edge_labelled_multiplicity[tuple(sorted((chart_id, destination)))] += 1
            for edge in record["entering"]:
                raw.append((record, (edge,), destination))
            raw.append((record, record["entering"], destination))

        orbits = {}
        for record, zero, destination in raw:
            key = canonical_state(record, zero, group)
            prior = orbits.setdefault(key, {
                "destinations": set(),
                "raw_count": 0,
            })
            prior["destinations"].add(destination)
            prior["raw_count"] += 1

        orbit_records = []
        for orbit_id, (key, metadata) in enumerate(sorted(orbits.items()), 1):
            leaving, entering, zero = key
            destinations = sorted(metadata["destinations"])
            require(len(destinations) == 1,
                    "source stabilizer changed destination chart orbit")
            orbit_records.append({
                "boundary_orbit": orbit_id,
                "destination_chart": destinations[0],
                "zero_count": len(zero),
                "leaving_cells": [list(edge) for edge in leaving],
                "entering_cells": [list(edge) for edge in entering],
                "zero_cells": [list(edge) for edge in zero],
                "labelled_state_count": metadata["raw_count"],
                "library_match": "NONE_FROM_BOUNDARY_ANTECEDENT_ALONE",
            })
            global_states.append((chart_id, key))

        per_chart.append({
            "chart": chart_id,
            "source_component_sizes": list(component_sizes_from_triple(triple)),
            "stabilizer_order": len(group),
            "adjacent_chart_orbits": sorted(graph[chart_id]),
            "labelled_flips": 36,
            "raw_marked_states": len(raw),
            "boundary_orbits": len(orbit_records),
            "singleton_orbits": sum(item["zero_count"] == 1
                                    for item in orbit_records),
            "double_orbits": sum(item["zero_count"] == 2
                                 for item in orbit_records),
            "records": orbit_records,
        })

    require(set(graph) == set(range(1, 32)), "chart graph lost a vertex")

    edge_pairs = {
        tuple(sorted((source, target)))
        for source, targets in graph.items() for target in targets
    }
    self_loops = sorted(source for source, target in edge_pairs
                        if source == target)
    inter_chart_edges = sorted(edge for edge in edge_pairs
                               if edge[0] != edge[1])
    half_degree_statistic = sum(len(values) for values in graph.values()) // 2
    require(len(inter_chart_edges) == 114 and len(self_loops) == 21
            and half_degree_statistic == 124,
            "frozen C4 adjacency census changed")

    # Minimum singleton-boundary arborescence. Parent->child overlap transport
    # leaves the inverse divisor in the child. The radical split for uv needs
    # the singleton branches (u) and (v); their intersection needs no separate
    # double-zero certificate. Root 19 attains the exact lower bound 31.
    singleton_cost = {}
    for source, record in enumerate(per_chart, 1):
        for target in record["adjacent_chart_orbits"]:
            if target == source:
                continue
            singleton_cost[source, target] = sum(
                item["destination_chart"] == target and item["zero_count"] == 1
                for item in record["records"]
            )
    minimum_incoming = {
        child: min(cost for (source, _target), cost in singleton_cost.items()
                   if source == child)
        for child in range(1, 32)
    }
    require(minimum_incoming[20] == 2
            and all(cost == 1 for child, cost in minimum_incoming.items()
                    if child != 20),
            "singleton incoming lower-bound profile changed")

    def cost_one_reachable(start):
        reached = {start}
        frontier = deque([start])
        while frontier:
            current = frontier.popleft()
            for child in range(1, 32):
                if (child not in reached
                        and singleton_cost.get((child, current)) == 1):
                    reached.add(child)
                    frontier.append(child)
        return reached

    require(set(range(1, 32)) - cost_one_reachable(20) == {19, 27},
            "root-20 cost-one cut certificate changed")

    root = 19
    parent = {root: None}
    queue = deque([root])
    while queue:
        current = queue.popleft()
        for child in range(1, 32):
            if (child not in parent and child != current
                    and singleton_cost.get((child, current)) == 1):
                parent[child] = current
                queue.append(child)
    require(set(range(1, 32)) - set(parent) == {20},
            "cost-one reachability from root 19 changed")
    best_parent = min(
        (singleton_cost[20, candidate], candidate)
        for candidate in parent if (20, candidate) in singleton_cost
    )
    require(best_parent[0] == 2, "chart 20 minimum incoming cost changed")
    parent[20] = best_parent[1]
    require(len(parent) == 31, "minimum propagation tree lost a chart")
    propagation = []
    for child in sorted(set(range(1, 32)) - {root}):
        old = parent[child]
        candidates = [item for item in per_chart[child - 1]["records"]
                      if item["destination_chart"] == old
                      and item["zero_count"] == 1]
        require(candidates, "tree edge has no reverse marked-boundary record")
        propagation.append({
            "parent": old,
            "child": child,
            "child_boundary_orbits": [item["boundary_orbit"]
                                      for item in candidates],
            "singleton_orbits": len(candidates),
        })
    require(sum(len(item["child_boundary_orbits"]) for item in propagation) == 31,
            "optimal singleton burden changed")
    require(sum(singleton_cost[child, old] for child, old in parent.items()
                if old is not None) == 31,
            "displayed arborescence cost changed")

    first = per_chart[0]["records"][0]
    payload = {
        "format": "n8-chart-c4-marked-boundary-atlas-v1",
        "status": "EXACT_BOUNDARY_ORBIT_CENSUS_LIBRARY_GAP",
        "census": {
            "chart_orbits": 31,
            "frozen_half_degree_statistic_previously_called_undirected_edges": 124,
            "distinct_inter_chart_transition_orbits": len(inter_chart_edges),
            "self_transition_orbits": len(self_loops),
            "total_transition_orbit_pairs_including_loops": len(edge_pairs),
            "labelled_directed_flips": 31 * 36,
            "raw_marked_boundary_states": 31 * 108,
            "stabilizer_quotient_boundary_orbits": len(global_states),
            "singleton_boundary_orbits": sum(
                item["singleton_orbits"] for item in per_chart),
            "double_boundary_orbits": sum(
                item["double_orbits"] for item in per_chart),
            "per_chart_orbit_histogram": dict(sorted(Counter(
                item["boundary_orbits"] for item in per_chart
            ).items())),
            "edge_labelled_flip_multiplicity_histogram": dict(sorted(Counter(
                edge_labelled_multiplicity.values()
            ).items())),
            "inter_chart_boundary_orbits": sum(
                item["destination_chart"] != chart["chart"]
                for chart in per_chart for item in chart["records"]
            ),
            "inter_chart_singleton_boundary_orbits": sum(
                item["destination_chart"] != chart["chart"]
                and item["zero_count"] == 1
                for chart in per_chart for item in chart["records"]
            ),
            "inter_chart_double_boundary_orbits_redundant_for_radical_split": sum(
                item["destination_chart"] != chart["chart"]
                and item["zero_count"] == 2
                for chart in per_chart for item in chart["records"]
            ),
        },
        "library_audit": {
            "matched_boundary_orbits": 0,
            "unmatched_boundary_orbits": len(global_states),
            "reason": (
                "A marked divisor sets only one or two off-support pure cells to zero while "
                "the twelve source-chart anchor cells remain live. It does not imply zero "
                "cross-colour tail/block diagonality, a matching-hole zero-cross mask, any "
                "frozen k4 cycle or triangle-pendant cofactor antecedent, or one of the "
                "support-6/support-8 arbitrary-mate component equations."
            ),
            "hostile_generic_support_guard": (
                "Set exactly the marked entering cells to zero and every other non-anchor "
                "cell to an independent nonzero symbol. This satisfies the divisor support "
                "condition but none of the listed sparse/zero-tail/cofactor antecedents. "
                "It is an antecedent guard, not an X5 solution."
            ),
        },
        "first_uncovered_representative": {
            "source_chart": 1,
            **{key: value for key, value in first.items()
               if key != "library_match"},
            "conclusion": "no frozen closure theorem is triggered by this one-cell zero",
        },
        "propagation_checklist": {
            "root_chart": root,
            "tree_edges": 30,
            "records": propagation,
            "missing_boundary_orbits_on_tree": sum(
                len(item["child_boundary_orbits"]) for item in propagation
            ),
            "double_zero_certificates_required": 0,
            "radical_split": (
                "Set-theoretically V(I+(uv)) = V(I+(u)) union V(I+(v)); "
                "closing the two singleton branches closes their double-zero intersection."
            ),
            "optimality_certificate": (
                "Every nonroot chart costs at least one singleton orbit. If the root is not "
                "20, chart 20 costs at least two, giving 31. If the root is 20, the cost-one "
                "directed graph cannot reach charts 19 and 27, so an entering arc costs at "
                "least two, again giving 31. Root 19 and the displayed tree attain 31."
            ),
            "scope": (
                "This minimum spanning arborescence is sufficient for vertex-by-vertex "
                "propagation if every listed child singleton boundary is separately closed. "
                "Current completion is zero."
            ),
        },
        "charts": per_chart,
        "theorem": (
            "The exact C4 overlap atlas has a finite marked-boundary quotient. The earlier "
            "124-edge wording was a half-degree statistic that mishandled 21 self-loops: "
            "there are 114 distinct inter-chart edges. The minimum singleton-boundary "
            "propagation burden is 31. The "
            "existing block-diagonal/mate/local chart library covers none of its strata from "
            "the one/two entering-cell vanishing antecedent alone. Connectedness therefore "
            "does not yet reduce the 31-chart certificate checklist."
        ),
        "scope": (
            "Finite support/orbit and antecedent-implication audit only; no claim that any "
            "boundary meets X5, and no polynomial membership or emptiness claim."
        ),
        "source_sha256": {
            str(TRANSITION_PATH.relative_to(ROOT)): sha256(
                TRANSITION_PATH.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "census": payload["census"],
        "first_uncovered_representative": payload["first_uncovered_representative"],
        "tree_missing": payload["propagation_checklist"]["missing_boundary_orbits_on_tree"],
        "logical_sha256": payload["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
