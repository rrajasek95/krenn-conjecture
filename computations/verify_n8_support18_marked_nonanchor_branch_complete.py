#!/usr/bin/env python3
"""Branch-complete restricted-support audit for marked support-18 blocks.

The support graph carries a directed target incidence and two added-edge
marks.  The marks are ordered when their GHZ-frame supports differ and may be
interchanged exactly when those supports agree.  Fifteen support-pattern
orbits cover target support 12/012 and added supports 01/02/12/012.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations
import json
import os
from pathlib import Path
import shutil
import tempfile
import traceback


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "a6ae147b913999ae4cf4f12f70d57139b5ee7342fdf7f8f4049a313084e9cb73"
N = 8
FULL = (0, 1, 2)
PAIR0 = (1, 2)
PAIR1 = (0, 2)
PAIR2 = (0, 1)


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


THEOREM = load_local(
    "n8_support18_coordinate_theorem_for_marked_branches",
    "verify_n8_support18_multi_edge_persistence_theorem.py",
)
ANCHOR = THEOREM.ANCHOR
ORBIT = THEOREM.ORBIT


def support_pattern_orbits():
    """Return the 15 ordered added-support patterns modulo target stabilizer."""
    # Full target: S3 is transitive on a missing colour and on ordered pairs
    # of equal/distinct missing colours.
    full_target = (
        (FULL, FULL, FULL),
        (FULL, FULL, PAIR0),
        (FULL, PAIR0, FULL),
        (FULL, PAIR0, PAIR0),
        (FULL, PAIR0, PAIR1),
    )
    # Target PAIR0 fixes missing colour 0 and has stabilizer (1 2).
    tags = (FULL, PAIR0, PAIR1, PAIR2)
    swap = {FULL: FULL, PAIR0: PAIR0, PAIR1: PAIR2, PAIR2: PAIR1}
    pair_target = []
    seen = set()
    for first in tags:
        for second in tags:
            pair = (first, second)
            if pair in seen:
                continue
            orbit = {pair, (swap[first], swap[second])}
            seen.update(orbit)
            pair_target.append((PAIR0, first, second))
    require(len(full_target) == 5 and len(pair_target) == 10,
            ("support-pattern orbit count changed", full_target,
             pair_target))
    return full_target + tuple(pair_target)


def mapped_edge(edge, mapping):
    return tuple(sorted((mapping[edge[0]], mapping[edge[1]])))


def canonical_marked_key(edges, incidence, first_edge, second_edge,
                         interchangeable):
    endpoint, target_edge = incidence
    other = target_edge[0] if target_edge[1] == endpoint else target_edge[1]
    remaining = tuple(
        vertex for vertex in range(N) if vertex not in (endpoint, other)
    )
    best = None
    for images in permutations(range(2, N)):
        mapping = {endpoint: 0, other: 1}
        mapping.update(dict(zip(remaining, images)))
        mapped_support = tuple(sorted(
            mapped_edge(edge, mapping) for edge in edges
        ))
        first = mapped_edge(first_edge, mapping)
        second = mapped_edge(second_edge, mapping)
        marks = tuple(sorted((first, second))) if interchangeable else (
            first, second
        )
        key = (mapped_support, marks)
        if best is None or key < best:
            best = key
    require(best is not None,
            ("failed marked canonicalization", edges, incidence,
             first_edge, second_edge, interchangeable))
    return best


def marked_descendant_register():
    parents = ANCHOR.hard_directed_types()
    require(len(parents) == 502,
            ("support17 directed type count changed", len(parents)))
    all_edges = {
        (left, right)
        for left in range(N) for right in range(left + 1, N)
    }
    ordered = {}
    unordered = {}
    ordered_multiplicity = Counter()
    unordered_multiplicity = Counter()
    entry_count = 0
    for parent_index, item in enumerate(parents):
        parent_edges = tuple(tuple(edge) for edge in item["augmented_edges"])
        incidence = tuple(item["incidence"])
        first_edge = tuple(item["new_edge"])
        for second_edge in sorted(all_edges - set(parent_edges)):
            entry_count += 1
            edges = tuple(sorted(parent_edges + (second_edge,)))
            record = {
                "parent_type_index": parent_index,
                "parent_route": item["parent_route"],
                "edges": edges,
                "incidence": incidence,
                "first_added_edge": first_edge,
                "second_added_edge": second_edge,
            }
            ordered_key = canonical_marked_key(
                edges, incidence, first_edge, second_edge, False
            )
            unordered_key = canonical_marked_key(
                edges, incidence, first_edge, second_edge, True
            )
            ordered_multiplicity[ordered_key] += 1
            unordered_multiplicity[unordered_key] += 1
            ordered.setdefault(ordered_key, record)
            unordered.setdefault(unordered_key, record)
    require(entry_count == 502 * 11,
            ("marked descendant entry count changed", entry_count))
    return {
        "entry_count": entry_count,
        "ordered_types": tuple(
            {**record, "marked_key": key,
             "ancestry_multiplicity": ordered_multiplicity[key]}
            for key, record in sorted(ordered.items())
        ),
        "unordered_types": tuple(
            {**record, "marked_key": key,
             "ancestry_multiplicity": unordered_multiplicity[key]}
            for key, record in sorted(unordered.items())
        ),
        "ordered_multiplicity_histogram": tuple(sorted(Counter(
            ordered_multiplicity.values()
        ).items())),
        "unordered_multiplicity_histogram": tuple(sorted(Counter(
            unordered_multiplicity.values()
        ).items())),
    }


def first_occurrence_guard(register, limit_per_pattern=None):
    outcomes = Counter()
    for pattern_index, pattern in enumerate(support_pattern_orbits()):
        target_support, first_support, second_support = pattern
        interchangeable = first_support == second_support
        records = (register["unordered_types"] if interchangeable
                   else register["ordered_types"])
        if limit_per_pattern is not None:
            records = records[:limit_per_pattern]
        for type_index, item in enumerate(records):
            edges = tuple(item["edges"])
            incidence = tuple(item["incidence"])
            first_edge = tuple(item["first_added_edge"])
            second_edge = tuple(item["second_added_edge"])
            shapes, private_caps, faces = THEOREM.response_data(
                edges, incidence
            )
            require(not private_caps,
                    ("marked nonprivate type acquired private cap", item,
                     private_caps))
            supports = {
                incidence[1]: target_support,
                first_edge: first_support,
                second_edge: second_support,
            }
            status, witness, statistics = (
                THEOREM.exact_smt_occurrence_completion(
                    edges, faces, supports,
                    0 if target_support == PAIR0 else None,
                    "none",
                )
            )
            outcomes[(pattern_index, status)] += 1
            require(status != "unknown",
                    ("marked occurrence solver timed out", pattern_index,
                     type_index, statistics))
            if witness is None:
                continue
            words = dict(witness["word_histogram"])
            mixed = Counter(
                multiplicity for word, multiplicity in words.items()
                if len(set(word)) > 1
            )
            return {
                "outcomes_before_guard": tuple(sorted(outcomes.items())),
                "guard": {
                    "pattern_index": pattern_index,
                    "support_pattern": pattern,
                    "marked_type_index": type_index,
                    "interchangeable_added_marks": interchangeable,
                    "edges": edges,
                    "incidence": incidence,
                    "first_added_edge": first_edge,
                    "second_added_edge": second_edge,
                    "nonanchor_supports": tuple(sorted(supports.items())),
                    "response_shapes": shapes,
                    "binary_faces": faces,
                    "mixed_multiplicity_histogram": tuple(sorted(
                        mixed.items()
                    )),
                    **witness,
                    "solver_statistics": tuple(sorted(statistics.items())),
                    "status": (
                        "exact occurrence guard only; coefficient and pure "
                        "normalization equations remain to be solved"
                    ),
                },
            }
    return {
        "outcomes_before_guard": tuple(sorted(outcomes.items())),
        "guard": None,
    }


def audit_pattern_record(task):
    pattern_index, type_index, pattern, item = task
    target_support, first_support, second_support = pattern
    edges = tuple(item["edges"])
    incidence = tuple(item["incidence"])
    first_edge = tuple(item["first_added_edge"])
    second_edge = tuple(item["second_added_edge"])
    shapes, private_caps, faces = THEOREM.response_data(edges, incidence)
    require(not private_caps,
            ("marked nonprivate type acquired private cap", item,
             private_caps))
    supports = {
        incidence[1]: target_support,
        first_edge: first_support,
        second_edge: second_support,
    }
    status, witness, statistics = THEOREM.exact_smt_occurrence_completion(
        edges, faces, supports,
        0 if target_support == PAIR0 else None,
        "none",
    )
    require(status != "unknown",
            ("marked occurrence solver timed out", pattern_index,
             type_index, statistics))
    guard = None
    if witness is not None:
        words = dict(witness["word_histogram"])
        mixed = Counter(
            multiplicity for word, multiplicity in words.items()
            if len(set(word)) > 1
        )
        guard = {
            "pattern_index": pattern_index,
            "support_pattern": pattern,
            "marked_type_index": type_index,
            "interchangeable_added_marks": first_support == second_support,
            "edges": edges,
            "incidence": incidence,
            "first_added_edge": first_edge,
            "second_added_edge": second_edge,
            "nonanchor_supports": tuple(sorted(supports.items())),
            "response_shapes": shapes,
            "binary_faces": faces,
            "mixed_multiplicity_histogram": tuple(sorted(mixed.items())),
            **witness,
            "solver_statistics": tuple(sorted(statistics.items())),
            "status": (
                "exact occurrence guard; coefficient and pure "
                "normalization equations require solving"
            ),
        }
    return {
        "outcome": (pattern_index, status),
        "solver_statistics": statistics,
        "guard": guard,
    }


def all_pattern_tasks(register):
    tasks = []
    counts = Counter()
    for pattern_index, pattern in enumerate(support_pattern_orbits()):
        interchangeable = pattern[1] == pattern[2]
        records = (register["unordered_types"] if interchangeable
                   else register["ordered_types"])
        counts[(pattern_index,
                "unordered" if interchangeable else "ordered")] = len(records)
        tasks.extend(
            (pattern_index, type_index, pattern, item)
            for type_index, item in enumerate(records)
        )
    require(len(tasks) == 5 * len(register["unordered_types"])
            + 10 * len(register["ordered_types"]),
            ("marked branch task count changed", len(tasks), counts))
    return tuple(tasks), tuple(sorted(counts.items()))


def parallel_branch_results(tasks, worker_count):
    temporary = Path(tempfile.mkdtemp(
        prefix="n8-support18-marked-branches-"
    ))
    children = []
    try:
        for shard in range(worker_count):
            output_path = temporary / f"worker-{shard}.json"
            error_path = temporary / f"worker-{shard}.error"
            pid = os.fork()
            if pid == 0:
                try:
                    outcomes = Counter()
                    statistics = Counter()
                    guards = []
                    for index in range(shard, len(tasks), worker_count):
                        result = audit_pattern_record(tasks[index])
                        outcomes[tuple(result["outcome"])] += 1
                        for key, value in result["solver_statistics"].items():
                            statistics[key] += value
                        if result["guard"] is not None:
                            guards.append(result["guard"])
                    payload = canonical({
                        "outcomes": tuple(sorted(outcomes.items())),
                        "solver_statistics": tuple(sorted(statistics.items())),
                        "guards": tuple(guards),
                    })
                    with output_path.open("w", encoding="utf-8") as handle:
                        json.dump(payload, handle, sort_keys=True,
                                  separators=(",", ":"))
                    os._exit(0)
                except BaseException:
                    with error_path.open("w", encoding="utf-8") as handle:
                        handle.write(traceback.format_exc())
                    os._exit(1)
            children.append((pid, shard, output_path, error_path))

        for pid, shard, _output_path, error_path in children:
            _waited, status = os.waitpid(pid, 0)
            require(os.waitstatus_to_exitcode(status) == 0,
                    ("marked branch worker failed", shard,
                     error_path.read_text(encoding="utf-8")
                     if error_path.exists() else "no traceback"))

        outcomes = Counter()
        statistics = Counter()
        guards = []
        for _pid, _shard, output_path, _error_path in children:
            with output_path.open(encoding="utf-8") as handle:
                payload = json.load(handle)
            for key, value in payload["outcomes"]:
                outcomes[tuple(key)] += value
            statistics.update(dict(payload["solver_statistics"]))
            guards.extend(payload["guards"])
        return {
            "outcomes": tuple(sorted(outcomes.items())),
            "solver_statistics": tuple(sorted(statistics.items())),
            "guards": tuple(sorted(
                guards,
                key=lambda item: (item["pattern_index"],
                                  item["marked_type_index"]),
            )),
        }
    finally:
        for pid, _shard, _output_path, _error_path in children:
            try:
                os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:
                pass
        shutil.rmtree(temporary, ignore_errors=True)


def audit_all_marked_branches(register):
    tasks, task_counts = all_pattern_tasks(register)
    worker_count = min(8, len(tasks))
    audit = parallel_branch_results(tasks, worker_count)
    require(sum(value for _key, value in audit["outcomes"]) == len(tasks),
            ("marked branch outcome count incomplete", len(tasks),
             audit["outcomes"]))
    unordered_patterns = {0, 3, 5, 9, 13}
    expected = Counter({
        (pattern_index, "unsat"):
            (len(register["unordered_types"])
             if pattern_index in unordered_patterns
             else len(register["ordered_types"]))
        for pattern_index in range(15)
    })
    require(Counter(dict(audit["outcomes"])) == expected,
            ("marked branch exact outcome split changed", audit["outcomes"],
             tuple(sorted(expected.items()))))
    require(not audit["guards"],
            ("marked support18 occurrence guard survived", audit["guards"][:4]))
    return {
        "task_count": len(tasks),
        "task_counts_by_pattern_and_marking": task_counts,
        "worker_count": worker_count,
        **audit,
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
    require(THEOREM.EXPECTED_SHA256
            == "ca0c641fb16ef47aa1cb6a3220556b1e34a95de5f5e413324217f969f2a9eabb",
            ("support18 coordinate theorem pin changed",
             THEOREM.EXPECTED_SHA256))
    patterns = support_pattern_orbits()
    register = marked_descendant_register()
    full_audit = audit_all_marked_branches(register)
    ledger = canonical({
        "dependency_pin": THEOREM.EXPECTED_SHA256,
        "support_pattern_orbits": patterns,
        "marked_register": register,
        "full_marked_branch_audit": full_audit,
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("marked support18 ledger changed", digest))
    print("N=8 support-18 marked branch register: PASS")
    print("  support patterns:", len(patterns))
    print("  entries:", register["entry_count"])
    print("  ordered/unordered marked types:",
          len(register["ordered_types"]), len(register["unordered_types"]))
    print("  full tasks / guards:", full_audit["task_count"],
          len(full_audit["guards"]))


if __name__ == "__main__":
    main()
