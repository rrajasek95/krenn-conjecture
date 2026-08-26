#!/usr/bin/env python3
"""Exact exhaustive 884-coordinate source projection and modular rank audit."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROVIDER = HERE / "audit_k16_c6_schur_boundary.py"
CYCLE = ROOT / "computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23"
C6_RESULT = CYCLE / "results_c6_boundary_schur_lift.json"
C7_RESULT = CYCLE / "results_c7_certified_reduction.json"
C7_LEDGER = CYCLE / "c7_certified_reduction_coefficients.tsv"
OUT = HERE / "results_k16_884_boundary_projection.json"
TIME_CAP = 150.0
COLUMN_CAP = 100_000

def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)

def load_provider():
    spec = importlib.util.spec_from_file_location("k16_884_provider", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, PROVIDER)
    spec.loader.exec_module(module)
    return module

def retain(counter):
    return Counter({key: value for key, value in counter.items() if value})

def add_scaled(left, right, scale):
    for key, value in right.items():
        updated = left.get(key, 0) + scale * value
        if updated: left[key] = updated
        else: left.pop(key, None)

def parse_column(key):
    word, multiplier = key.split(":", 1)
    return tuple(map(int, word)), bytes.fromhex(multiplier)

def residual_text(residual):
    return "\n".join(f"{row.hex()}\t{coefficient}"
                     for row, coefficient in sorted(residual.items())) + "\n"

def modular_rank(vectors, target, prime):
    basis = {}
    pivot_order = {}
    max_nnz = 0
    for source in vectors:
        vector = {row: value % prime for row, value in source.items() if value % prime}
        while vector:
            old = [(pivot_order[row], row) for row in vector if row in basis]
            if not old:
                pivot = min(vector)
                inverse = pow(vector[pivot], prime - 2, prime)
                vector = {row: value * inverse % prime for row, value in vector.items()}
                basis[pivot] = vector
                pivot_order[pivot] = len(pivot_order)
                max_nnz = max(max_nnz, len(vector))
                break
            _, pivot = min(old)
            scale = vector[pivot]
            for row, value in basis[pivot].items():
                updated = (vector.get(row, 0) - scale * value) % prime
                if updated: vector[row] = updated
                else: vector.pop(row, None)
    remainder = {row: (value.numerator * pow(value.denominator, prime-2, prime)) % prime
                 for row, value in target.items() if value}
    for pivot in sorted(basis, key=pivot_order.get):
        if pivot not in remainder:
            continue
        scale = remainder[pivot]
        for row, value in basis[pivot].items():
            updated = (remainder.get(row, 0) - scale * value) % prime
            if updated: remainder[row] = updated
            else: remainder.pop(row, None)
    return len(basis), len(basis) + bool(remainder), len(remainder), max_nnz

def build(mutate=False):
    started = time.monotonic()
    provider = load_provider()
    c6 = json.loads(C6_RESULT.read_text())
    c7 = json.loads(C7_RESULT.read_text())
    require(c6["logical_sha256"] == "d53aad470b3db200ee0c9311548e237b7a748bfd9e5f25dd501ac902a75b73ff", c6["logical_sha256"])
    require(c7["logical_sha256"] == "e596e36bb447d354a94e60f11e1e291b729615763d9abff48122ae1035c38ecb", c7["logical_sha256"])
    column_projection_cache = {}
    def full_projection(key):
        found = column_projection_cache.get(key)
        if found is not None: return found
        vector = Counter()
        for row in provider.D24.degree24_column_rows(parse_column(key)):
            if provider.D24.row_k_degree(row) <= 16:
                vector[provider.HQ.canonical_row(row)] += 1
        vector = retain(vector)
        column_projection_cache[key] = vector
        return vector
    residual = Counter({bytes.fromhex(record["row"]): Fraction(record["coefficient"])
                        for record in c6["uncertified_high_rows"]})
    for line in C7_LEDGER.read_text().splitlines()[1:]:
        kind, coefficient_text, key = line.split("\t")
        require(kind in ("pair-left", "pair-right", "c>7-pivot"), kind)
        add_scaled(residual, full_projection(key), -Fraction(coefficient_text))
    residual = retain(residual)
    payload_text = residual_text(residual)
    require(len(residual) == 884, len(residual))
    require(sha256(payload_text.encode()).hexdigest() == c7["remaining_residual_sha256"],
            "884 residual replay mismatch")
    if mutate:
        residual[min(residual)] += 1
        payload_text = residual_text(residual)
    require(sha256(payload_text.encode()).hexdigest() ==
            "69af8c7ceec28a7e2add37f7177fde19d8d58771796998a07bc34ae222d44aac",
            "hostile target mutation or drift")
    rows = tuple(sorted(residual))
    row_index = {row: index for index, row in enumerate(rows)}

    source_columns = set()
    raw_incidence = 0
    per_row = []
    for position, row in enumerate(rows, 1):
        raw = provider.D24.incident_degree24_columns(row)
        canonical = {provider.HQ.canonical_column(column) for column in raw}
        raw_incidence += len(raw)
        source_columns.update(canonical)
        per_row.append(len(canonical))
        require(len(source_columns) <= COLUMN_CAP, len(source_columns))
        require(time.monotonic() - started < TIME_CAP, ("time cap during incidence", position))
        if position % 100 == 0:
            print(f"INCIDENCE rows={position}/884 columns={len(source_columns)} elapsed={time.monotonic()-started:.1f}", flush=True)
    source_columns = tuple(sorted(source_columns, key=provider.HQ.column_key))

    orbit_lookup = {}
    orbit_sizes = Counter()
    for index, row in enumerate(rows):
        images = {provider.F.move_row(row, action) for action in provider.H}
        orbit_sizes[len(images)] += 1
        for image in images:
            prior = orbit_lookup.setdefault(image, index)
            require(prior == index, (row.hex(), prior, index))

    vectors = []
    projected_nonzero = 0
    projected_entries = 0
    coverage = Counter()
    for position, column in enumerate(source_columns, 1):
        vector = Counter()
        for output in provider.D24.degree24_column_rows(column):
            index = orbit_lookup.get(output)
            if index is not None:
                vector[index] += 1
        vector = retain(vector)
        if vector:
            projected_nonzero += 1
            projected_entries += len(vector)
            coverage.update(vector)
        vectors.append(dict(vector))
        require(time.monotonic() - started < TIME_CAP, ("time cap during projection", position))
    target = {row_index[row]: value for row, value in residual.items()}
    ranks = {}
    for prime in (32003, 32009):
        rank, augmented, remainder, max_nnz = modular_rank(vectors, target, prime)
        ranks[str(prime)] = {"rank": rank, "augmented_rank": augmented,
                             "target_remainder_entries": remainder,
                             "max_echelon_column_nnz": max_nnz}
    exact_rank = min(record["rank"] for record in ranks.values())
    require(all(record["rank"] == exact_rank for record in ranks.values()), ranks)
    require(exact_rank == 884, exact_rank)
    result = {
        "schema": "orbit0-k16-884-boundary-projection-v1",
        "status": "EXACT_FULL_ROW_RANK_BOUNDARY_FILL",
        "boundary_rows": len(rows),
        "literal_incident_occurrences": raw_incidence,
        "source_column_H_orbits": len(source_columns),
        "projected_nonzero_columns": projected_nonzero,
        "projected_nonzero_entries": projected_entries,
        "row_incident_column_min": min(per_row),
        "row_incident_column_max": max(per_row),
        "projected_row_coverage": len(coverage),
        "H_orbit_size_histogram": dict(sorted(orbit_sizes.items())),
        "ranks_modular": ranks,
        "rank_over_Q": exact_rank,
        "target_augmented_rank_over_Q": exact_rank,
        "target_in_span_over_Q": True,
        "exact_rank_argument": "Rank 884 modulo either prime gives rank_Q>=884, while the row dimension gives rank_Q<=884.",
        "scope_guard": "Complete 884-coordinate projection only; exterior outputs were not expanded into a next closure.",
        "pinned": {"c6_lift_logical": c6["logical_sha256"],
                   "c7_certified_logical": c7["logical_sha256"],
                   "target_residual_sha256": sha256(payload_text.encode()).hexdigest()},
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(logical, sort_keys=True,
                                                  separators=(",", ":")).encode()).hexdigest()
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build(args.mutate)
    if not args.verify:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in
                      ("status", "boundary_rows", "source_column_H_orbits",
                       "projected_nonzero_columns", "rank_over_Q",
                       "target_augmented_rank_over_Q", "logical_sha256",
                       "elapsed_seconds")}, sort_keys=True))

if __name__ == "__main__":
    main()
