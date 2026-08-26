#!/usr/bin/env python3
"""Complete reachable third Bockstein for the six surviving chart classes.

The previous page has 17,915 literal second-shell columns and 201 inherited
first-kernel tails.  Its exact modular rank is 16,704, so all 1,412 kernel
directions must be carried to the third page.  This checker reconstructs
those source coordinates, forms their literal third tails, and then explores
the *complete* row/column incidence component reached by the six nonzero
critical third tails.  Unreached components cannot affect membership.

This is a modular discovery/census checker.  A zero remainder is not promoted
to characteristic zero until its sparse source identity is lifted and
replayed over Q.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
import argparse
import hashlib
import importlib.util
import json
import pickle
from pathlib import Path


HERE = Path(__file__).resolve().parent
SECOND_PATH = HERE / "audit_seven_critical_second_bockstein.py"
CACHE = HERE / "second_bockstein_state_p1009.pkl"
OUT = HERE / "results_six_critical_third_bockstein_p1009.json"

SPEC = importlib.util.spec_from_file_location("second_bockstein", SECOND_PATH)
SECOND = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(SECOND)
SOURCE = SECOND.SOURCE
PRIME = 1009


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_scaled(target, source, scale):
    for key, coefficient in source.items():
        value = (target.get(key, 0) + scale * coefficient) % PRIME
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def counter_mod(column, allowed):
    return {
        row: coefficient % PRIME
        for row, coefficient in Counter(SOURCE.column_outputs(column)).items()
        if row in allowed and coefficient % PRIME
    }


def content_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_state(rebuild=False):
    pin = content_hash(SECOND_PATH)
    if CACHE.exists() and not rebuild:
        payload = pickle.loads(CACHE.read_bytes())
        require(payload["prime"] == PRIME, "state-cache prime changed")
        require(payload["second_script_sha256"] == pin,
                "state cache was made by a different second-page checker")
        return payload["state"], payload["summary"]
    SECOND.PRIME = PRIME
    result = SECOND.audit(return_state=True)
    state = result.pop("_state")
    payload = {
        "prime": PRIME,
        "second_script_sha256": pin,
        "summary": result,
        "state": state,
    }
    CACHE.write_bytes(pickle.dumps(payload, protocol=pickle.HIGHEST_PROTOCOL))
    return state, result


def back_substitute(basis_coordinates, basis_order, basis_origin,
                    basis_scale, basis_reductions):
    coordinates = dict(basis_coordinates)
    source = {}
    for pivot in reversed(basis_order):
        coefficient = coordinates.pop(pivot, 0)
        if not coefficient:
            continue
        scaled = coefficient * pow(basis_scale[pivot], -1, PRIME) % PRIME
        origin = basis_origin[pivot]
        source[origin] = (source.get(origin, 0) + scaled) % PRIME
        if not source[origin]:
            source.pop(origin)
        for earlier, value in basis_reductions[pivot]:
            updated = (coordinates.get(earlier, 0) - scaled * value) % PRIME
            if updated:
                coordinates[earlier] = updated
            else:
                coordinates.pop(earlier, None)
    require(not coordinates, ("unexpanded basis coordinates", len(coordinates)))
    return source


def audit(rebuild=False, progress=25000):
    state, second_summary = load_state(rebuild)
    second_columns = state["second_columns"]
    third_set = frozenset(state["third_rows"])
    third_tails = state["third_tails"]
    second_kernels = state["second_correction_kernels"]
    used_columns = (
        set(state["support_columns"])
        | set(state["first_columns"])
        | set(second_columns)
    )

    # Only actual second-shell columns can have third-row output.  The 201
    # inherited first-kernel origins have exhausted their literal outputs in
    # the second row shell by construction.
    second_column_tail_cache = {}
    kernel_tails = []
    for number, kernel in enumerate(second_kernels):
        tail = {}
        for correction_number, coefficient in kernel.items():
            if correction_number >= len(second_columns):
                continue
            if correction_number not in second_column_tail_cache:
                second_column_tail_cache[correction_number] = counter_mod(
                    second_columns[correction_number], third_set
                )
            add_scaled(tail, second_column_tail_cache[correction_number], coefficient)
        kernel_tails.append(tail)

    row_to_kernels = defaultdict(list)
    for number, tail in enumerate(kernel_tails):
        for row in tail:
            row_to_kernels[row].append(number)

    active_targets = tuple(index for index, tail in enumerate(third_tails) if tail)
    queue = deque()
    reached_rows = set()

    def add_row(row):
        if row not in reached_rows:
            reached_rows.add(row)
            queue.append(row)

    for target in active_targets:
        for row in third_tails[target]:
            add_row(row)

    basis = {}
    basis_origin = {}
    basis_scale = {}
    basis_reductions = {}
    basis_order = []
    dependent = []
    origins = []
    origin_vectors = []
    seen_columns = set()
    seen_kernels = set()

    def insert(origin, vector):
        number = len(origins)
        origins.append(origin)
        origin_vectors.append(vector)
        work = dict(vector)
        reductions = []
        while work:
            pivot = min(work)
            value = work[pivot]
            if pivot not in basis:
                basis_origin[pivot] = number
                basis_scale[pivot] = value
                basis_reductions[pivot] = tuple(reductions)
                basis_order.append(pivot)
                inverse = pow(value, -1, PRIME)
                basis[pivot] = {
                    row: coefficient * inverse % PRIME
                    for row, coefficient in work.items()
                }
                return
            reductions.append((pivot, value))
            add_scaled(work, basis[pivot], -value)
        dependent.append((number, tuple(reductions)))

    while queue:
        row = queue.popleft()
        for kernel_number in row_to_kernels.get(row, ()):
            if kernel_number in seen_kernels:
                continue
            seen_kernels.add(kernel_number)
            vector = kernel_tails[kernel_number]
            for other in vector:
                add_row(other)
            insert(("second_kernel", kernel_number), vector)
        for column in SOURCE.incident_columns(row):
            if column in used_columns or column in seen_columns:
                continue
            seen_columns.add(column)
            vector = counter_mod(column, third_set)
            require(row in vector, ("incident column lost seed row", row, column))
            for other in vector:
                add_row(other)
            insert(("third_column", column), vector)
        if progress and len(reached_rows) % progress == 0:
            print(
                "progress",
                "rows", len(reached_rows),
                "columns", len(seen_columns),
                "kernels", len(seen_kernels),
                "rank", len(basis),
                flush=True,
            )

    target_remainders = []
    target_solutions = []
    for target, tail in enumerate(third_tails):
        if not tail:
            target_remainders.append(0)
            target_solutions.append({})
            continue
        work = dict(tail)
        coordinates = {}
        while work:
            pivot = min(work)
            value = work[pivot]
            if pivot not in basis:
                break
            coordinates[pivot] = (coordinates.get(pivot, 0) + value) % PRIME
            add_scaled(work, basis[pivot], -value)
        target_remainders.append(len(work))
        if work:
            target_solutions.append(None)
            continue
        source = back_substitute(
            coordinates, basis_order, basis_origin, basis_scale,
            basis_reductions,
        )
        replay = {}
        for origin_number, coefficient in source.items():
            add_scaled(replay, origin_vectors[origin_number], coefficient)
        require(replay == tail, ("third target replay failed", target))
        target_solutions.append(source)

    # Exact modular kernel coordinates of the reachable correction matrix.
    correction_kernels = []
    for number, reductions in dependent:
        source = back_substitute(
            dict(reductions), basis_order, basis_origin, basis_scale,
            basis_reductions,
        )
        kernel = {number: 1}
        add_scaled(kernel, source, -1)
        replay = {}
        for origin_number, coefficient in kernel.items():
            add_scaled(replay, origin_vectors[origin_number], coefficient)
        require(not replay, ("third correction kernel failed", number))
        correction_kernels.append(kernel)

    result = {
        "prime": PRIME,
        "second_page": {
            key: value for key, value in second_summary.items()
            if key in ("correction_rank", "second_correction_kernel",
                       "critical_third_tail_terms")
        },
        "third_global_rows": len(third_set),
        "active_target_indices": active_targets,
        "reachable_rows": len(reached_rows),
        "reachable_literal_columns": len(seen_columns),
        "reachable_inherited_kernel_tails": len(seen_kernels),
        "correction_vectors": len(origins),
        "correction_rank": len(basis),
        "correction_nullity": len(correction_kernels),
        "target_remainders": tuple(target_remainders),
        "target_solution_terms": tuple(
            None if solution is None else len(solution)
            for solution in target_solutions
        ),
        "kernel_third_tail_nonzero": sum(bool(tail) for tail in kernel_tails),
        "kernel_third_tail_terms": sum(map(len, kernel_tails)),
        "complete_reachable_component": True,
        "scope": (
            "modular membership over GF(1009); characteristic-zero lifting "
            "requires sparse rational reconstruction and exact replay"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--progress", type=int, default=25000)
    args = parser.parse_args()
    result = audit(args.rebuild, args.progress)
    for key, value in result.items():
        print(f"{key}: {value}", flush=True)


if __name__ == "__main__":
    main()
