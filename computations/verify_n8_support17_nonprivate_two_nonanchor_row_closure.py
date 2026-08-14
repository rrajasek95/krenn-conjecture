#!/usr/bin/env python3
"""Pure/singleton row closure with target and inserted edge noncoordinate.

Use the 502 directed nonprivate support-17 types.  Treat both the inherited
target edge and the inserted edge as noncoordinate, enumerate all mutual-
coordinate anchor completions of the other fifteen edges, and test all eight
support pairs (target support size two/three; inserted support 01/02/12/012).
No cap formula is used.  A survivor must support all three pure words and
have no singleton mixed matching fibre.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
import os
from pathlib import Path
import shutil
import tempfile
import traceback


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "c49c81ae5f96e9655c9990e2cb4fb0c7c64f8d8c3b8826f7176ef876bab481e0"
COLORS = (0, 1, 2)
TARGET_SUPPORTS = ((1, 2), (0, 1, 2))
INSERTED_SUPPORTS = ((0, 1), (0, 2), (1, 2), (0, 1, 2))
N = 8


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


ANCHOR = load_local(
    "n8_support17_anchor_closure_for_two_nonanchors",
    "verify_n8_support17_hard_landed_parent_anchor_closure.py",
)
ORBIT = ANCHOR.ORBIT


def matching_word_histogram(matchings, states, target_edge, target_support,
                            new_edge, new_support):
    words = Counter()
    for matching in matchings:
        choices = []
        for edge in matching:
            if edge == target_edge:
                choices.append(target_support)
            elif edge == new_edge:
                choices.append(new_support)
            else:
                choices.append((states[edge],))
        for colours in product(*choices):
            word = [None] * N
            for edge, colour in zip(matching, colours):
                word[edge[0]] = colour
                word[edge[1]] = colour
            require(None not in word,
                    ("two-nonanchor matching left blank site", matching,
                     colours, word))
            words[tuple(word)] += 1
    return words


def audit_one_type(task):
    index, item = task
    edges = tuple(tuple(edge) for edge in item["augmented_edges"])
    edge_set = set(edges)
    target_edge = tuple(item["incidence"][1])
    new_edge = tuple(item["new_edge"])
    require(target_edge != new_edge and target_edge in edge_set
            and new_edge in edge_set,
            ("bad two-nonanchor edge pair", item))
    coordinate_edges = tuple(
        edge for edge in edges if edge not in (target_edge, new_edge)
    )
    incident = {
        vertex: tuple(edge for edge in coordinate_edges if vertex in edge)
        for vertex in range(N)
    }
    require(all(len(incident[vertex]) >= 3 for vertex in range(N)),
            ("two-nonanchor chart lacks three anchor slots", index, item,
             incident))
    matchings = tuple(
        matching
        for raw_matching in ORBIT.BASE.perfect_matchings(tuple(range(N)))
        for matching in (
            tuple(tuple(sorted(edge)) for edge in raw_matching),
        )
        if all(edge in edge_set for edge in matching)
    )
    require(matchings, ("support17 type has no perfect matching", item))
    support_pairs = tuple(
        (target_support, new_support)
        for target_support in TARGET_SUPPORTS
        for new_support in INSERTED_SUPPORTS
    )
    witnesses = {}
    witness_words = {}
    states = {coordinate_edges[0]: 0}
    counts = Counter()

    def recurse():
        counts["nodes"] += 1
        for vertex in range(N):
            seen = {states[edge] for edge in incident[vertex]
                    if edge in states}
            remaining = sum(edge not in states for edge in incident[vertex])
            if 3 - len(seen) > remaining:
                return
        # Even giving both nonanchors full support, each pure row needs some
        # still-compatible perfect matching.
        for colour in COLORS:
            if not any(all(
                    edge in (target_edge, new_edge)
                    or edge not in states
                    or states[edge] == colour
                    for edge in matching
            ) for matching in matchings):
                counts["pure_feasibility_prunes"] += 1
                return
        if all(edge in states for edge in coordinate_edges):
            if not all({states[edge] for edge in incident[vertex]}
                       == set(COLORS) for vertex in range(N)):
                return
            counts["anchor_completions"] += 1
            completion = tuple(sorted(states.items()))
            for target_support, new_support in support_pairs:
                pair = (target_support, new_support)
                if pair in witnesses:
                    continue
                words = matching_word_histogram(
                    matchings, states, target_edge, target_support,
                    new_edge, new_support,
                )
                pure = tuple(words[(colour,) * N] for colour in COLORS)
                if not all(pure):
                    counts["support_pair_missing_pure"] += 1
                    continue
                counts["support_pair_pure_supported"] += 1
                singletons = tuple(sorted(
                    word for word, multiplicity in words.items()
                    if len(set(word)) > 1 and multiplicity == 1
                ))
                if singletons:
                    counts["support_pair_singleton_exit"] += 1
                    continue
                witnesses[pair] = {
                    "completion": completion,
                    "pure_occurrence_counts": pure,
                }
                witness_words[pair] = tuple(sorted(words.items()))
                counts["support_pair_necessary_guard"] += 1
            return

        unassigned = tuple(
            edge for edge in coordinate_edges if edge not in states
        )

        def pressure(edge):
            return sum(
                3 - len({states[item] for item in incident[vertex]
                         if item in states})
                for vertex in edge
            )

        edge = max(unassigned, key=pressure)
        for colour in COLORS:
            states[edge] = colour
            recurse()
        del states[edge]

    recurse()
    witness_ledger = tuple(
        {
            "target_support": pair[0],
            "inserted_support": pair[1],
            **witness,
            "word_histogram": witness_words[pair],
        }
        for pair, witness in sorted(witnesses.items())
    )
    return {
        "directed_type_index": index,
        "parent_route": item["parent_route"],
        "graph_index": item["graph_index"],
        "incidence": item["incidence"],
        "new_edge": item["new_edge"],
        "augmented_edges": item["augmented_edges"],
        "search_counts": tuple(sorted(counts.items())),
        "necessary_guards": witness_ledger,
    }


def parallel_results(representatives, worker_count):
    temporary = Path(tempfile.mkdtemp(
        prefix="n8-support17-two-nonanchor-row-"
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
                        audit_one_type((index, item))
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
                    ("two-nonanchor worker failed", shard,
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


def audit_two_nonanchor_closure():
    representatives = ANCHOR.hard_directed_types()
    require(len(representatives) == 502,
            ("two-nonanchor directed type count changed",
             len(representatives)))
    worker_count = min(8, len(representatives))
    results = parallel_results(representatives, worker_count)
    totals = Counter()
    route_types = Counter()
    guards = []
    for result in results:
        totals.update(dict(result["search_counts"]))
        route_types[result["parent_route"]] += 1
        for guard in result["necessary_guards"]:
            if len(guards) < 16:
                guards.append({
                    "directed_type_index": result["directed_type_index"],
                    "parent_route": result["parent_route"],
                    "graph_index": result["graph_index"],
                    "incidence": result["incidence"],
                    "new_edge": result["new_edge"],
                    "augmented_edges": result["augmented_edges"],
                    **guard,
                })
    require(route_types == Counter({
        "complete-private-cap": 322,
        "original-two-cap": 173,
        "collision-normalization": 7,
    }), ("two-nonanchor parent-route split changed", route_types))
    require(totals == Counter({
        "nodes": 13033162,
        "pure_feasibility_prunes": 589566,
        "anchor_completions": 245530,
        "support_pair_missing_pure": 320608,
        "support_pair_pure_supported": 1643632,
        "support_pair_singleton_exit": 1643632,
    }), ("two-nonanchor search totals changed", totals))
    require(not guards,
            ("two-nonanchor necessary counterguard survived", guards))
    return {
        "directed_type_count": len(representatives),
        "directed_types_by_parent_route": tuple(sorted(route_types.items())),
        "support_pairs_per_type": 8,
        "search_totals": tuple(sorted(totals.items())),
        "necessary_counterguards": tuple(guards),
        "type_ledgers": results,
        "worker_count": worker_count,
        "criterion": (
            "necessary guard has two simultaneous noncoordinate blocks, a "
            "mutual-coordinate completion of all other edges, all pure rows, "
            "and no singleton mixed matching fibre; no cap test is imposed"
        ),
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
    ledger = canonical(audit_two_nonanchor_closure())
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("two-nonanchor row closure ledger changed", digest))
    print("N=8 support-17 nonprivate two-nonanchor row closure: PASS")
    print("  directed types / support pairs: 502 / 8")
    print("  search totals:", ledger["search_totals"])
    print("  necessary counterguards:",
          len(ledger["necessary_counterguards"]))


if __name__ == "__main__":
    main()
