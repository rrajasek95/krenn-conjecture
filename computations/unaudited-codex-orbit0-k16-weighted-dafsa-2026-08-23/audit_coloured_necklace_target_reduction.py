#!/usr/bin/env python3
"""Target-rooted coloured-necklace reduction for structured a*T.

Rows are multisets of dihedral colour necklaces.  A reduction cuts one edge
in each of four cycles whose eight endpoints are not monochromatic and uses
the 105 endpoint perfect matchings.  The original four-cycle completion is
the unique maximal-cycle term, so it is solved into terms with fewer cycles.

This first implementation is deliberately target-rooted and capped.  It also
records whether alternative cut choices give the same recursively reduced
right hand side on every reached state; a nonzero normal form is called sound
only after that local all-choice guard succeeds.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_coloured_necklace_target_reduction.json"
NF = HERE / "coloured_necklace_aT_normal_form.tsv"
BASE = ((0, 1), (2, 3), (4, 5), (6, 7))
TIME_CAP = 285.0
STATE_CAP = 500_000
SUPPORT_CAP = 500_000
RELATION_CHECK_CAP = 2_000_000


class CapExceeded(RuntimeError):
    pass


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


@lru_cache(None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for index, v in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((u, v),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))
ORIGINAL = tuple((2 * index, 2 * index + 1) for index in range(4))


def canonical_necklace(word):
    word = tuple(word)
    require(len(word) >= 2, word)
    candidates = []
    for oriented in (word, tuple(reversed(word))):
        candidates.extend(oriented[index:] + oriented[:index]
                          for index in range(len(word)))
    return min(candidates)


def canonical_state(necklaces):
    return tuple(sorted((canonical_necklace(word) for word in necklaces),
                        key=lambda word: (len(word), word)))


def necklace_text(word):
    return "".join(map(str, word))


def state_text(state):
    return ".".join(necklace_text(word) for word in state)


def retain_nonzero(counter):
    """Return an exact signed Counter without Counter's positive-part cleanup."""
    return Counter({key: value for key, value in counter.items() if value != 0})


def union_cycle_partition(left, right):
    adjacency = [[] for _ in range(8)]
    edges = left + right
    for edge_id, (u, v) in enumerate(edges):
        adjacency[u].append(edge_id)
        adjacency[v].append(edge_id)
    used = set()
    parts = []
    for seed in range(8):
        if seed in used:
            continue
        stack = [seed]
        vertices = set()
        while stack:
            edge_id = stack.pop()
            if edge_id in used:
                continue
            used.add(edge_id)
            u, v = edges[edge_id]
            vertices.update((u, v))
            for vertex in (u, v):
                stack.extend(other for other in adjacency[vertex]
                             if other not in used)
        parts.append(len(vertices))
    require(sum(parts) == 8, parts)
    return tuple(sorted(parts))


def initial_target():
    types = Counter(union_cycle_partition(BASE, matching) for matching in PM8)
    require(sum(types.values()) == 105 and len(types) == 5, types)
    answer = Counter()
    for p0, n0 in types.items():
        for p1, n1 in types.items():
            for p2, n2 in types.items():
                state = canonical_state(
                    [tuple([0] * length) for length in p0]
                    + [tuple([1] * length) for length in p1]
                    + [tuple([2] * length) for length in p2])
                answer[state] += n0 * n1 * n2
    require(sum(answer.values()) == 105 ** 3 and len(answer) == 125,
            (len(answer), sum(answer.values())))
    return answer


def cut_path(cycle, cut):
    # Delete edge (cut-1,cut); the remaining path runs cut,...,cut-1.
    return cycle[cut:] + cycle[:cut]


@lru_cache(None)
def completed_cycles(paths, matching):
    offsets = []
    colours = []
    for path in paths:
        offsets.append(len(colours))
        colours.extend(path)
    edges = []
    endpoint_vertices = []
    for index, path in enumerate(paths):
        start = offsets[index]
        for position in range(len(path) - 1):
            edges.append((start + position, start + position + 1))
        endpoint_vertices.extend((start, start + len(path) - 1))
    for left, right in matching:
        edges.append((endpoint_vertices[left], endpoint_vertices[right]))
    adjacency = [[] for _ in colours]
    for edge_id, (left, right) in enumerate(edges):
        adjacency[left].append((edge_id, right))
        adjacency[right].append((edge_id, left))
    require(all(len(row) == 2 for row in adjacency), (paths, matching, adjacency))
    used_edges = set()
    cycles = []
    for seed_edge in range(len(edges)):
        if seed_edge in used_edges:
            continue
        left, _ = edges[seed_edge]
        current_vertex = left
        current_edge = seed_edge
        word = []
        while True:
            require(current_edge not in used_edges, (paths, matching, current_edge))
            used_edges.add(current_edge)
            word.append(colours[current_vertex])
            u, v = edges[current_edge]
            next_vertex = v if current_vertex == u else u
            choices = [edge_id for edge_id, _ in adjacency[next_vertex]
                       if edge_id != current_edge]
            require(len(choices) == 1, (next_vertex, adjacency[next_vertex]))
            next_edge = choices[0]
            current_vertex, current_edge = next_vertex, next_edge
            if current_edge == seed_edge:
                require(current_vertex == left, (current_vertex, left))
                break
        cycles.append(canonical_necklace(word))
    require(sum(map(len, cycles)) == sum(map(len, paths)), (cycles, paths))
    return tuple(sorted(cycles, key=lambda word: (len(word), word)))


def all_valid_choices(state):
    for indices in combinations(range(len(state)), 4):
        cycles = tuple(state[index] for index in indices)
        for cuts in product(*(range(len(cycle)) for cycle in cycles)):
            paths = tuple(cut_path(cycle, cut)
                          for cycle, cut in zip(cycles, cuts, strict=True))
            endpoints = tuple(colour for path in paths
                              for colour in (path[0], path[-1]))
            if len(set(endpoints)) > 1:
                yield indices, cuts, paths


@lru_cache(None)
def relation_children(state, indices, cuts):
    selected = tuple(state[index] for index in indices)
    paths = tuple(cut_path(cycle, cut)
                  for cycle, cut in zip(selected, cuts, strict=True))
    untouched = tuple(cycle for index, cycle in enumerate(state)
                      if index not in indices)
    outputs = Counter()
    for matching in PM8:
        child = canonical_state(untouched + completed_cycles(paths, matching))
        outputs[child] += 1
    require(outputs[state] == 1, (state, indices, cuts, outputs[state]))
    del outputs[state]
    require(sum(outputs.values()) == 104, sum(outputs.values()))
    require(all(len(child) < len(state) for child in outputs),
            (len(state), max(map(len, outputs))))
    return tuple(sorted(outputs.items(), key=lambda item: state_text(item[0])))


class Reducer:
    def __init__(self):
        self.start = time.monotonic()
        self.memo = {}
        self.order = []
        self.choices = {}
        self.max_depth = 0
        self.relations = 0
        self.raw_children = 0

    def guard(self):
        if time.monotonic() - self.start > TIME_CAP:
            raise CapExceeded("time")
        if len(self.memo) > STATE_CAP:
            raise CapExceeded("states")

    def normal(self, state, depth=0):
        if state in self.memo:
            return self.memo[state]
        self.guard()
        self.max_depth = max(self.max_depth, depth)
        if len(state) <= 3:
            answer = Counter({state: 1})
            self.memo[state] = answer
            self.order.append(state)
            return answer
        choice = next(all_valid_choices(state), None)
        require(choice is not None, ("no mixed four-cycle choice", state_text(state)))
        indices, cuts, _ = choice
        self.choices[state] = (indices, cuts)
        children = relation_children(state, indices, cuts)
        self.relations += 1
        self.raw_children += sum(count for _, count in children)
        answer = Counter()
        for child, count in children:
            child_normal = self.normal(child, depth + 1)
            for terminal, coefficient in child_normal.items():
                answer[terminal] -= count * coefficient
        answer = retain_nonzero(answer)
        if len(answer) > SUPPORT_CAP:
            raise CapExceeded("normal support")
        self.memo[state] = answer
        self.order.append(state)
        return answer


def build():
    target = initial_target()
    reducer = Reducer()
    normal = Counter()
    status = "PASS_NONZERO_DETERMINISTIC_NORMAL_FORM"
    cap_reason = None
    try:
        for ordinal, (state, multiplicity) in enumerate(
                sorted(target.items(), key=lambda item: state_text(item[0])), 1):
            row = reducer.normal(state)
            for terminal, coefficient in row.items():
                normal[terminal] += multiplicity * coefficient
            normal = retain_nonzero(normal)
            if len(normal) > SUPPORT_CAP:
                raise CapExceeded("target normal support")
            if ordinal % 10 == 0:
                reducer.guard()
    except CapExceeded as error:
        status = "UNRESOLVED_CAP"
        cap_reason = str(error)

    confluence_status = "NOT_RUN_DUE_TO_REDUCTION_CAP"
    relation_choices_checked = 0
    distinct_relation_vectors_checked = 0
    confluence_states_checked = 0
    first_mismatch = None
    if cap_reason is None:
        confluence_status = "PASS_TARGET_ROOTED_ALL_CHOICE_CLOSURE"
        cursor = 0
        try:
            while cursor < len(reducer.order):
                reducer.guard()
                state = reducer.order[cursor]
                cursor += 1
                if len(state) <= 3:
                    confluence_states_checked += 1
                    continue
                expected = reducer.normal(state)
                seen_relations = set()
                for indices, cuts, _ in all_valid_choices(state):
                    relation_choices_checked += 1
                    children = relation_children(state, indices, cuts)
                    if children in seen_relations:
                        continue
                    seen_relations.add(children)
                    distinct_relation_vectors_checked += 1
                    right = Counter()
                    for child, count in children:
                        child_normal = reducer.normal(child)
                        for terminal, coefficient in child_normal.items():
                            right[terminal] -= count * coefficient
                    right = retain_nonzero(right)
                    if right != expected:
                        first_mismatch = {
                            "state": state_text(state),
                            "indices": list(indices),
                            "cuts": list(cuts),
                            "expected": [[state_text(row), coefficient]
                                         for row, coefficient in sorted(
                                             expected.items(), key=lambda item: state_text(item[0]))],
                            "alternative": [[state_text(row), coefficient]
                                            for row, coefficient in sorted(
                                                right.items(), key=lambda item: state_text(item[0]))],
                        }
                        confluence_status = "FAIL_ALTERNATIVE_CUT_DIAMOND"
                        status = "FAIL_ALTERNATIVE_CUT_DIAMOND"
                        raise StopIteration
                    if distinct_relation_vectors_checked > RELATION_CHECK_CAP:
                        raise CapExceeded("relation checks")
                confluence_states_checked += 1
        except StopIteration:
            pass
        except CapExceeded as error:
            confluence_status = "UNRESOLVED_CONFLUENCE_CAP"
            status = "UNRESOLVED_CONFLUENCE_CAP"
            cap_reason = str(error)

    rows = sorted(normal.items(), key=lambda item: state_text(item[0]))
    nf_lines = ["necklace_state\tcoefficient"]
    nf_lines.extend(f"{state_text(state)}\t{coefficient}"
                    for state, coefficient in rows)
    nf_payload = "\n".join(nf_lines) + "\n"
    result = {
        "schema": "orbit0-coloured-necklace-target-reduction-v1",
        "status": status,
        "cap_reason": cap_reason,
        "time_cap_seconds": TIME_CAP,
        "state_cap": STATE_CAP,
        "support_cap": SUPPORT_CAP,
        "relation_check_cap": RELATION_CHECK_CAP,
        "initial_target_states": len(target),
        "initial_target_terms": sum(target.values()),
        "memoized_states": len(reducer.memo),
        "pivot_relations_used": reducer.relations,
        "raw_nonleading_completion_terms": reducer.raw_children,
        "maximum_recursion_depth": reducer.max_depth,
        "terminal_normal_form_support": len(normal),
        "terminal_normal_form_nonzero": bool(normal),
        "terminal_coefficient_l1": sum(abs(value) for value in normal.values()),
        "terminal_max_abs_coefficient": max(map(abs, normal.values()), default=0),
        "confluence_status": confluence_status,
        "confluence_states_checked": confluence_states_checked,
        "relation_cut_choices_checked": relation_choices_checked,
        "distinct_relation_vectors_checked": distinct_relation_vectors_checked,
        "first_confluence_mismatch": first_mismatch,
        "normal_form_sha256": sha256(nf_payload.encode()).hexdigest(),
        "elapsed_seconds": round(time.monotonic() - reducer.start, 6),
        "soundness_status": (
            "NO_SEPARATOR: the deterministic reduction is choice-dependent; the exported "
            "second distinct relation vector gives a nonzero terminal diamond. Even without "
            "this failure, forward closure alone would not replace inverse-parent closure."
            if first_mismatch else
            "TARGET_ROOTED_ALL_CHOICE_CONFLUENCE_ONLY; even a pass checks every downward "
            "alternative relation reached from a*T but is not an inverse-parent closure or a "
            "universal confluence theorem"
        ),
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(
        json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return result, nf_payload


def main():
    result, nf_payload = build()
    result_payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--verify" in sys.argv:
        require(NF.read_text() == nf_payload, "normal form differs")
        stored = json.loads(OUT.read_text())
        for key, value in result.items():
            if key != "elapsed_seconds":
                require(stored[key] == value, (key, stored[key], value))
    else:
        NF.write_text(nf_payload)
        OUT.write_text(result_payload)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
