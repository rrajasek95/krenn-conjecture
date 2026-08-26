#!/usr/bin/env python3
"""Lift the Rust third-page sources and replay them exactly over Q.

All modular coordinates used by pages one through three have a unique
rational representative with |numerator|, denominator <= 22 because
2*22^2 < 1009.  The final test does not rely on that bound heuristically:
after reconstruction it expands the literal 105-matching columns and checks
the seven third tails coefficient-by-coefficient over Fraction.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
import importlib.util
import json
import math
import pickle
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
CACHE = HERE / "second_bockstein_state_p1009.pkl"
SOLUTION = HERE / "third_bockstein_p1009.rsol"
SOURCE_PATH = HERE.parent / "analyze_n8_full_s8s3_pure_product_membership.py"
OUT = HERE / "results_six_critical_third_bockstein_q.json"
PRIME = 1009
BOUND = 22


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load_module("n8_orbit_source_q", SOURCE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(maxsize=None)
def rational_lift(residue):
    residue %= PRIME
    answers = set()
    for denominator in range(1, BOUND + 1):
        numerator = residue * denominator % PRIME
        if numerator > PRIME // 2:
            numerator -= PRIME
        if abs(numerator) <= BOUND and math.gcd(numerator, denominator) == 1:
            answers.add(Fraction(numerator, denominator))
    require(len(answers) == 1, ("rational reconstruction not unique", residue, answers))
    answer = next(iter(answers))
    require(
        answer.numerator * pow(answer.denominator, -1, PRIME) % PRIME == residue,
        ("rational reconstruction replay failed", residue, answer),
    )
    return answer


def lift_vector(vector):
    return {key: rational_lift(value) for key, value in vector.items()}


def add_scaled(target, source, scale):
    for key, coefficient in source.items():
        value = target.get(key, Fraction()) + scale * coefficient
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def parse_solutions():
    data = SOLUTION.read_bytes()
    offset = 0
    require(data[:8] == b"BCK3S001", "solution magic changed")
    offset = 8
    prime, count = struct.unpack_from("<II", data, offset)
    offset += 8
    require(prime == PRIME and count == 7, ("solution header changed", prime, count))
    answers = []
    for _target in range(count):
        terms, = struct.unpack_from("<I", data, offset)
        offset += 4
        answer = []
        for _ in range(terms):
            coefficient, = struct.unpack_from("<H", data, offset)
            offset += 2
            tag = data[offset]
            offset += 1
            if tag == 0:
                mate = struct.unpack_from("<24b", data, offset)
                offset += 24
                origin = ("column", SOURCE.canonical_key(tuple(mate)))
            elif tag == 1:
                kernel, = struct.unpack_from("<I", data, offset)
                offset += 4
                origin = ("kernel", kernel)
            else:
                raise RuntimeError(("unknown solution tag", tag))
            answer.append((origin, rational_lift(coefficient)))
        answers.append(tuple(answer))
    require(offset == len(data), ("solution trailing bytes", len(data) - offset))
    return tuple(answers)


def audit():
    payload = pickle.loads(CACHE.read_bytes())
    require(payload["prime"] == PRIME, "cache prime changed")
    state = payload["state"]
    third_set = frozenset(state["third_rows"])

    # This is a theorem guard, not merely a check on the few final sources:
    # every coordinate stored by the preceding pages must lift uniquely.
    coordinate_families = (
        state["first_solutions"],
        state["first_kernels"],
        state["second_solutions"],
        state["second_correction_kernels"],
    )
    coordinate_count = 0
    for family in coordinate_families:
        for vector in family:
            for residue in vector.values():
                rational_lift(residue)
                coordinate_count += 1

    @lru_cache(maxsize=None)
    def full_counter(column):
        return {
            row: Fraction(coefficient)
            for row, coefficient in Counter(SOURCE.column_outputs(column)).items()
            if coefficient
        }

    @lru_cache(maxsize=None)
    def third_counter(column):
        return {row: coefficient for row, coefficient in full_counter(column).items()
                if row in third_set}

    first_solutions = tuple(map(lift_vector, state["first_solutions"]))
    first_kernels = tuple(map(lift_vector, state["first_kernels"]))
    second_solutions = tuple(map(lift_vector, state["second_solutions"]))
    second_kernels = tuple(map(lift_vector, state["second_correction_kernels"]))
    rust_solutions = parse_solutions()

    exact_tails = []
    for leading, first_solution, second_solution in zip(
        state["representatives"], first_solutions, second_solutions
    ):
        vector = {}
        for column_number, coefficient in leading.items():
            add_scaled(vector, third_counter(state["support_columns"][column_number]), coefficient)
        for column_number, coefficient in first_solution.items():
            add_scaled(vector, third_counter(state["first_columns"][column_number]), -coefficient)
        for correction_number, coefficient in second_solution.items():
            if correction_number < len(state["second_columns"]):
                add_scaled(
                    vector,
                    third_counter(state["second_columns"][correction_number]),
                    -coefficient,
                )
            else:
                inherited = first_kernels[correction_number - len(state["second_columns"])]
                for column_number, kernel_coefficient in inherited.items():
                    add_scaled(
                        vector,
                        third_counter(state["first_columns"][column_number]),
                        -coefficient * kernel_coefficient,
                    )
        exact_tails.append(vector)

    kernel_tail_cache = {}
    first_kernel_full_cache = {}
    second_kernel_full_cache = {}

    def first_kernel_full(kernel_number):
        if kernel_number not in first_kernel_full_cache:
            vector = {}
            for column_number, coefficient in first_kernels[kernel_number].items():
                add_scaled(vector, full_counter(state["first_columns"][column_number]),
                           coefficient)
            first_kernel_full_cache[kernel_number] = vector
        return first_kernel_full_cache[kernel_number]

    def second_kernel_full(kernel_number):
        if kernel_number not in second_kernel_full_cache:
            vector = {}
            for correction_number, coefficient in second_kernels[kernel_number].items():
                if correction_number < len(state["second_columns"]):
                    source = full_counter(state["second_columns"][correction_number])
                else:
                    source = first_kernel_full(
                        correction_number - len(state["second_columns"])
                    )
                add_scaled(vector, source, coefficient)
            second_kernel_full_cache[kernel_number] = vector
        return second_kernel_full_cache[kernel_number]

    def kernel_tail(kernel_number):
        if kernel_number not in kernel_tail_cache:
            vector = {}
            for correction_number, coefficient in second_kernels[kernel_number].items():
                if correction_number < len(state["second_columns"]):
                    add_scaled(
                        vector,
                        third_counter(state["second_columns"][correction_number]),
                        coefficient,
                    )
                else:
                    inherited = first_kernels[
                        correction_number - len(state["second_columns"])
                    ]
                    for column_number, inherited_coefficient in inherited.items():
                        add_scaled(
                            vector,
                            third_counter(state["first_columns"][column_number]),
                            coefficient * inherited_coefficient,
                        )
            kernel_tail_cache[kernel_number] = vector
        return kernel_tail_cache[kernel_number]

    replay_terms = []
    used_kernels = set()
    for target, (tail, solution) in enumerate(zip(exact_tails, rust_solutions)):
        replay = {}
        for (kind, origin), coefficient in solution:
            if kind == "column":
                source = third_counter(origin)
            else:
                used_kernels.add(origin)
                source = kernel_tail(origin)
            add_scaled(replay, source, coefficient)
        require(replay == tail, ("exact third-page replay failed", target,
                                 len(replay), len(tail)))
        replay_terms.append(len(solution))

    # Unfiltered theorem replay.  The signs below assemble the original
    # leading kernel, the first and second corrections, and the Rust third
    # correction into one literal global column relation.
    global_relation_terms = []
    for target, (leading, first_solution, second_solution, rust_solution) in enumerate(zip(
        state["representatives"], first_solutions, second_solutions, rust_solutions
    )):
        relation = {}
        for column_number, coefficient in leading.items():
            add_scaled(relation, full_counter(state["support_columns"][column_number]),
                       coefficient)
        for column_number, coefficient in first_solution.items():
            add_scaled(relation, full_counter(state["first_columns"][column_number]),
                       -coefficient)
        for correction_number, coefficient in second_solution.items():
            if correction_number < len(state["second_columns"]):
                source = full_counter(state["second_columns"][correction_number])
            else:
                source = first_kernel_full(
                    correction_number - len(state["second_columns"])
                )
            add_scaled(relation, source, -coefficient)
        for (kind, origin), coefficient in rust_solution:
            source = full_counter(origin) if kind == "column" else second_kernel_full(origin)
            add_scaled(relation, source, -coefficient)
        require(not relation, ("global rational syzygy replay failed", target,
                               len(relation)))
        global_relation_terms.append(
            len(leading) + len(first_solution) + len(second_solution) + len(rust_solution)
        )

    result = {
        "prime_used_for_unique_reconstruction": PRIME,
        "rational_bound": BOUND,
        "uniqueness_guard": f"2*{BOUND}^2 < {PRIME}",
        "reconstructed_preceding_coordinates": coordinate_count,
        "third_tail_terms_over_q": tuple(map(len, exact_tails)),
        "source_terms_over_q": tuple(replay_terms),
        "second_kernel_sources": tuple(sorted(used_kernels)),
        "exact_remainders": (0,) * 7,
        "global_unfiltered_relation_remainders": (0,) * 7,
        "global_unfiltered_relation_source_terms_before_collection": tuple(
            global_relation_terms
        ),
        "literal_column_cache": full_counter.cache_info().currsize,
        "solution_sha256": hashlib.sha256(SOLUTION.read_bytes()).hexdigest(),
        "scope": (
            "seven exact global Q syzygies lifting the leading 31-chart "
            "kernel; the unfiltered literal column images vanish identically"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    result = audit()
    for key, value in result.items():
        print(f"{key}: {value}", flush=True)


if __name__ == "__main__":
    main()
