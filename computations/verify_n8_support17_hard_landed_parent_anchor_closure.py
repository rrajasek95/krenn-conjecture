#!/usr/bin/env python3
"""Exact anchor closure for every nonprivate landed-parent augmentation.

The structural persistence register has 667 representative augmentations
with no literal private cap.  Quotient them by directed support isomorphism,
then enumerate both
noncoordinate target-support charts.  A chart is accepted only if it avoids
every complementary binary cap, supports all three pure rows, and has no
singleton mixed matching fibre.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
import os
from pathlib import Path
import shutil
import tempfile
import traceback


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "2a5e85d8b4863bcf9c9f2a95229642b9f6531cdfd7e8bc7e5b8f6fdfd03dceb0"


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


PERSIST = load_local(
    "n8_support17_persistence_for_hard_anchor_closure",
    "verify_n8_support17_landed_parent_persistence_register.py",
)
PROTOTYPE = PERSIST.PROTOTYPE
ORBIT = PERSIST.ORBIT
BINARY = load_local(
    "n8_support16_binary_cover_for_hard_anchor_closure",
    "verify_n8_support16_all_binary_residue_two_cap_cover.py",
)


def hard_directed_types():
    persistence = PERSIST.audit_persistence_register()
    terminal_records = ORBIT.terminal_two_rrx_records()
    representatives = {}
    multiplicities = Counter()
    route_multiplicities = Counter()
    for item in persistence["augmentations"]:
        if item["private_caps"]:
            continue
        parent_edges = tuple(
            terminal_records[item["graph_index"]]["representative_edges"]
        )
        augmented = tuple(sorted(parent_edges + (item["new_edge"],)))
        key = PERSIST.canonical_directed_key(augmented, item["incidence"])
        multiplicities[key] += 1
        route_multiplicities[(key, item["parent_route"])] += 1
        representatives.setdefault(key, {
            "parent_route": item["parent_route"],
            "graph_index": item["graph_index"],
            "parent_orbit_size": item["parent_orbit_size"],
            "incidence": item["incidence"],
            "new_edge": item["new_edge"],
            "augmented_edges": augmented,
            "response_shapes": item["response_shapes"],
            "canonical_key": key,
        })
    require(sum(multiplicities.values()) == 667,
            ("nonprivate augmentation entry count changed", multiplicities))
    require(len(representatives) == 502,
            ("nonprivate directed type count changed", len(representatives)))
    require(Counter(multiplicities.values()) == Counter({
        1: 372, 2: 103, 3: 21, 4: 4, 5: 2,
    }), ("nonprivate directed multiplicity histogram changed", multiplicities))
    return tuple(
        {
            **representative,
            "hard_entry_multiplicity": multiplicities[key],
            "parent_route_multiplicity": tuple(sorted(
                (route, count)
                for (route_key, route), count
                in route_multiplicities.items()
                if route_key == key
            )),
        }
        for key, representative in sorted(representatives.items())
    )


def audit_one_directed_type(task):
    index, item = task
    edges = item["augmented_edges"]
    adjacency = ORBIT.adjacency_from_edges(edges)
    faces = BINARY.binary_faces(
        adjacency, edges, item["incidence"], item["response_shapes"]
    )
    charts = []
    counterguards = []
    search_totals = Counter()
    chart_outcomes = Counter()
    for chart_name, zero_coordinate in (
            ("support-two", 0), ("support-three", None)):
        witness, counts = BINARY.exact_source_guard_completion(
            edges, item["incidence"][1], faces, zero_coordinate
        )
        search_totals.update(dict(counts))
        if witness is None:
            outcome = "cap/pure/singleton-exit"
        else:
            outcome = "necessary-counterguard"
            counterguards.append({
                "directed_type_index": index,
                "parent_route": item["parent_route"],
                "graph_index": item["graph_index"],
                "incidence": item["incidence"],
                "new_edge": item["new_edge"],
                "augmented_edges": edges,
                "chart": chart_name,
                "binary_faces": faces,
                "witness": witness,
            })
        chart_outcomes[(chart_name, outcome)] += 1
        charts.append({
            "chart": chart_name,
            "outcome": outcome,
            "search_counts": counts,
            "witness": witness,
        })
    return {
        "route": item["parent_route"],
        "chart_outcomes": tuple(sorted(chart_outcomes.items())),
        "search_totals": tuple(sorted(search_totals.items())),
        "counterguards": tuple(counterguards),
        "ledger": {
            **item,
            "binary_faces": faces,
            "charts": tuple(charts),
        },
    }


def parallel_type_results(representatives, worker_count):
    """Run deterministic fork shards without semaphore-backed pools."""
    temporary = Path(tempfile.mkdtemp(
        prefix="n8-support17-hard-anchor-closure-"
    ))
    children = []
    try:
        for shard in range(worker_count):
            output_path = temporary / f"worker-{shard}.json"
            error_path = temporary / f"worker-{shard}.error"
            pid = os.fork()
            if pid == 0:
                try:
                    results = tuple(
                        audit_one_directed_type((index, item))
                        for index, item in enumerate(representatives)
                        if index % worker_count == shard
                    )
                    with output_path.open("w", encoding="utf-8") as handle:
                        json.dump(canonical(results), handle,
                                  sort_keys=True, separators=(",", ":"))
                    os._exit(0)
                except BaseException:
                    with error_path.open("w", encoding="utf-8") as handle:
                        handle.write(traceback.format_exc())
                    os._exit(1)
            children.append((pid, shard, output_path, error_path))

        for pid, shard, _output_path, error_path in children:
            _waited, status = os.waitpid(pid, 0)
            require(os.waitstatus_to_exitcode(status) == 0,
                    ("hard-anchor worker failed", shard,
                     error_path.read_text(encoding="utf-8")
                     if error_path.exists() else "no traceback"))

        by_shard = {}
        for _pid, shard, output_path, _error_path in children:
            with output_path.open(encoding="utf-8") as handle:
                by_shard[shard] = json.load(handle)
        offsets = Counter()
        ordered = []
        for index in range(len(representatives)):
            shard = index % worker_count
            ordered.append(by_shard[shard][offsets[shard]])
            offsets[shard] += 1
        return tuple(ordered)
    finally:
        for pid, _shard, _output_path, _error_path in children:
            try:
                os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:
                pass
        shutil.rmtree(temporary, ignore_errors=True)


def audit_hard_anchor_closure():
    representatives = hard_directed_types()
    route_types = Counter()
    chart_outcomes = Counter()
    search_totals = Counter()
    counterguards = []
    ledgers = []

    worker_count = min(8, len(representatives))
    results = parallel_type_results(representatives, worker_count)
    for result in results:
        route_types[result["route"]] += 1
        chart_outcomes.update({
            tuple(key): value for key, value in result["chart_outcomes"]
        })
        search_totals.update(dict(result["search_totals"]))
        for guard in result["counterguards"]:
            if len(counterguards) < 16:
                counterguards.append(guard)
        ledgers.append(result["ledger"])

    require(route_types == Counter({
        "complete-private-cap": 322,
        "original-two-cap": 173,
        "collision-normalization": 7,
    }), ("nonprivate directed parent-route split changed", route_types))
    require(chart_outcomes == Counter({
        ("support-two", "cap/pure/singleton-exit"): 502,
        ("support-three", "cap/pure/singleton-exit"): 502,
    }), ("nonprivate anchor chart outcomes changed", chart_outcomes))
    require(not counterguards,
            ("nonprivate coordinate anchor counterguard survived",
             counterguards))

    return {
        "nonprivate_entry_count": 667,
        "directed_type_count": len(representatives),
        "directed_types_by_selected_parent_route": tuple(
            sorted(route_types.items())
        ),
        "chart_outcomes": tuple(sorted(chart_outcomes.items())),
        "search_totals": tuple(sorted(search_totals.items())),
        "necessary_counterguards": tuple(counterguards),
        "directed_type_ledgers": tuple(ledgers),
        "criterion": (
            "a surviving witness has a mutual-coordinate anchor completion, "
            "all three pure matching supports, no complementary binary cap, "
            "and no singleton mixed matching fibre"
        ),
        "worker_count": worker_count,
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
    ledger = canonical(audit_hard_anchor_closure())
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("hard landed-parent anchor closure ledger changed", digest))
    print("N=8 support-17 nonprivate landed-parent anchor closure: PASS")
    print("  nonprivate entries / directed types: 667 / 502")
    print("  chart outcomes:", ledger["chart_outcomes"])
    print("  necessary counterguards:",
          len(ledger["necessary_counterguards"]))


if __name__ == "__main__":
    main()
