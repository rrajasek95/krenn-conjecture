#!/usr/bin/env python3
"""Extract P0 from R8' and test the compact complementary binary span."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
EXPORT_PATH = BRIDGE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
BASE = EXPORT.BASE
R8P = BRIDGE / "results_orbit0_cutoff9_sparse_r8.json"
OUT = HERE / "results_r8prime_p0_binary_packet_span.json"

H_ACTIONS = tuple(index for index, (_sites, colours)
                  in enumerate(EXPORT.STABILIZER) if colours[0] == 0)
M0_SET = frozenset(EXPORT.M0)
A0 = bytes(sorted(BASE.CELL_ID[(left, right, 0, 0)]
                  for left, right in EXPORT.M0))
PM_AVOID_M0 = tuple(matching for matching in BASE.PM8
                    if not any(edge in M0_SET for edge in matching))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def transform_row(row, action):
    transform = EXPORT.TRANSFORMS[action]
    return bytes(sorted(transform[cell] for cell in row))


@lru_cache(maxsize=None)
def h_orbit(row):
    return frozenset(transform_row(row, action) for action in H_ACTIONS)


@lru_cache(maxsize=None)
def canonical_row(row):
    return min(h_orbit(row))


def subtract(row, term):
    answer = Counter(row)
    answer.subtract(term)
    if any(value < 0 for value in answer.values()):
        return None
    return bytes(sorted(cell for cell, value in answer.items()
                        for _ in range(value)))


def audit_p0_row(row):
    require(len(row) == 8, "P0 row does not have degree 8")
    ports = Counter()
    for cell in row:
        u, v, a, b = BASE.CELLS[cell]
        require((u, v) not in M0_SET,
                "P0 unexpectedly uses a physical M0 edge")
        require(a in (1, 2) and b in (1, 2),
                "P0 unexpectedly uses colour zero")
        ports[(u, a)] += 1
        ports[(v, b)] += 1
    require(all(ports[(site, colour)] == 1
                for site in range(BASE.N) for colour in (1, 2)),
            "P0 row is not degree one at every binary port")


def extract_p0(raw):
    actual = Counter()
    selected_labelled = 0
    for row_hex, numerator, denominator in raw["residual"]:
        representative = bytes.fromhex(row_hex)
        orbit = EXPORT.row_orbit(representative)
        coefficient = Fraction(numerator, denominator) / len(orbit)
        for row in orbit:
            residual = subtract(row, A0)
            if residual is None:
                continue
            require(sum(cell in EXPORT.ANCHORS for cell in row) == 4,
                    "A0 sector row has extra anchors")
            audit_p0_row(residual)
            actual[residual] += coefficient
            selected_labelled += 1
    actual = Counter({row: value for row, value in actual.items() if value})
    unseen = set(actual)
    quotient = Counter()
    while unseen:
        seed = min(unseen)
        orbit = h_orbit(seed)
        require(orbit <= set(actual), "P0 support is not H-invariant")
        coefficients = {actual[row] for row in orbit}
        require(len(coefficients) == 1, "P0 coefficient is not H-invariant")
        quotient[min(orbit)] = next(iter(coefficients)) * len(orbit)
        unseen.difference_update(orbit)
    return actual, quotient, selected_labelled


def complement(word):
    return tuple(3 - colour for colour in word)


def canonical_word_pair(word):
    mate = complement(word)
    candidates = []
    for action in H_ACTIONS:
        sites, colours = EXPORT.STABILIZER[action]
        moved = [None] * BASE.N
        for site, colour in enumerate(word):
            moved[sites[site]] = colours[colour]
        moved = tuple(moved)
        candidates.append(min(moved, complement(moved)))
    return min(candidates)


def word_pair_orbits():
    pairs = {min(tuple(word), complement(tuple(word)))
             for word in product((1, 2), repeat=BASE.N)}
    by_rep = Counter(canonical_word_pair(word) for word in pairs)
    return tuple(sorted(by_rep)), by_rep


def packet_column(word):
    mate = complement(word)
    left = tuple(BASE.term_ids(word, matching) for matching in PM_AVOID_M0)
    right = tuple(BASE.term_ids(mate, matching) for matching in PM_AVOID_M0)
    answer = Counter()
    for first in left:
        for second in right:
            answer[canonical_row(bytes(sorted(first + second)))] += 1
    return answer


def exact_solve(columns, target):
    count = len(columns)
    rows = sorted(set(target).union(*(set(column) for column in columns)))
    pivots = {}
    inconsistent = None
    for row in rows:
        equation = [Fraction(column.get(row, 0)) for column in columns]
        rhs = Fraction(target.get(row, 0))
        for pivot in sorted(pivots):
            if equation[pivot]:
                scale = equation[pivot]
                pivot_row, pivot_rhs = pivots[pivot]
                equation = [left - scale * right
                            for left, right in zip(equation, pivot_row)]
                rhs -= scale * pivot_rhs
        pivot = next((index for index, value in enumerate(equation) if value),
                     None)
        if pivot is None:
            if rhs:
                inconsistent = (row, rhs)
                break
            continue
        scale = equation[pivot]
        equation = [value / scale for value in equation]
        rhs /= scale
        pivots[pivot] = (equation, rhs)
    if inconsistent is not None:
        return None, len(pivots), inconsistent
    solution = [Fraction(0) for _ in range(count)]
    for pivot in sorted(pivots, reverse=True):
        equation, rhs = pivots[pivot]
        solution[pivot] = rhs - sum(equation[index] * solution[index]
                                    for index in range(pivot + 1, count))
    replay = Counter()
    for coefficient, column in zip(solution, columns):
        if not coefficient:
            continue
        for row, value in column.items():
            replay[row] += coefficient * value
    replay = Counter({row: value for row, value in replay.items() if value})
    require(replay == target, "exact compact-span solution did not replay")
    return solution, len(pivots), None


def main():
    require(len(H_ACTIONS) == 768, "factor stabilizer changed")
    require(len(PM_AVOID_M0) == 60, "M0-avoiding matching census changed")
    raw = json.loads(R8P.read_text())
    actual, target, selected_labelled = extract_p0(raw)
    representatives, orbit_sizes = word_pair_orbits()
    columns = [packet_column(word) for word in representatives]
    solution, rank, inconsistent = exact_solve(columns, target)
    records = []
    if solution is not None:
        for word, coefficient, column in zip(representatives, solution, columns):
            records.append({
                "word": "".join(map(str, word)),
                "complement": "".join(map(str, complement(word))),
                "word_pair_orbit_size": orbit_sizes[word],
                "coefficient": [coefficient.numerator, coefficient.denominator],
                "column_rows": len(column),
                "column_mass": sum(column.values()),
            })
    result = {
        "status": "UNAUDITED exact binary packet span audit",
        "input_r8prime_sha256": sha256(R8P.read_bytes()).hexdigest(),
        "factor": "A0=x01_00*x23_00*x45_00*x67_00",
        "factor_stabilizer_order": len(H_ACTIONS),
        "p0_selected_labelled_rows_before_collection": selected_labelled,
        "p0_labelled_support": len(actual),
        "p0_quotient_row_orbits": len(target),
        "p0_quotient_mass": [sum(target.values()).numerator,
                             sum(target.values()).denominator],
        "binary_word_pairs": 128,
        "binary_word_pair_orbits": len(representatives),
        "M0_avoiding_terms_per_Gw": len(PM_AVOID_M0),
        "packet_product_columns": len(columns),
        "packet_span_rank": rank,
        "target_in_packet_span": solution is not None,
        "first_inconsistent_row": None if inconsistent is None else
            [inconsistent[0].hex(), inconsistent[1].numerator,
             inconsistent[1].denominator],
        "solution": records,
        "implication_scope": (
            "G_w is the 60-term projection of H_w to physical matchings "
            "avoiding M0. A positive identity is an exact projected binary "
            "packet identity; by itself it does not put P0 in I_mix until "
            "the omitted 45 matching terms are reinserted or killed."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R8' P0 complementary binary packet span: PASS")
    print("P0 labelled/orbits:", len(actual), len(target))
    print("word-pair orbits/rank/in-span:",
          len(representatives), rank, solution is not None)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
