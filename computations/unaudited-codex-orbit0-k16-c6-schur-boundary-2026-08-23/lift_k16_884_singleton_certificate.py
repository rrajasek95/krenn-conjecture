#!/usr/bin/env python3
"""Construct and lift a deterministic exact-Q certificate for the 884 boundary."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from math import lcm
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
AUDIT_PATH = HERE / "audit_k16_884_boundary_projection.py"
CYCLE = ROOT / "computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23"
GENERAL_RESULT = CYCLE / "results_general_cycle_pivot_page.json"
GENERAL_RESIDUAL = CYCLE / "general_cycle_pivot_final_residual.tsv"
OUT = HERE / "results_k16_884_singleton_lift.json"
LEDGER = HERE / "k16_884_singleton_certificate.tsv"
RESIDUAL = HERE / "k16_884_singleton_lift_residual.tsv"
TIME_CAP = 150.0
ROW_CAP = 100_000

def require(condition, detail):
    if not condition: raise RuntimeError(detail)

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module

def retain(counter):
    return Counter({key: value for key, value in counter.items() if value})

def add_scaled(left, right, scale):
    for key, value in right.items():
        updated = left.get(key, 0) + scale * value
        if updated: left[key] = updated
        else: left.pop(key, None)

def residual_text(residual):
    return "\n".join(f"{row.hex()}\t{coefficient}"
                     for row, coefficient in sorted(residual.items())) + "\n"

def read_residual(path):
    answer = Counter()
    for line in path.read_text().splitlines():
        row, value = line.split("\t")
        if row == "row":
            require(value == "coefficient", (row, value))
            continue
        answer[bytes.fromhex(row)] = Fraction(value)
    return retain(answer)

def build(mutate=False):
    started = time.monotonic()
    audit = load("k16_884_lift_audit", AUDIT_PATH)
    provider = audit.load_provider()
    c6 = json.loads(audit.C6_RESULT.read_text())
    c7 = json.loads(audit.C7_RESULT.read_text())
    general = json.loads(GENERAL_RESULT.read_text())
    residual = Counter({bytes.fromhex(record["row"]): Fraction(record["coefficient"])
                        for record in c6["uncertified_high_rows"]})
    projection_cache = {}
    def full_vector(column):
        key = provider.HQ.column_key(column)
        found = projection_cache.get(key)
        if found is not None: return found
        vector = Counter()
        for output in provider.D24.degree24_column_rows(column):
            if provider.D24.row_k_degree(output) <= 16:
                vector[provider.HQ.canonical_row(output)] += 1
        vector = retain(vector)
        projection_cache[key] = vector
        return vector
    for line in audit.C7_LEDGER.read_text().splitlines()[1:]:
        kind, coefficient_text, key = line.split("\t")
        require(kind in ("pair-left", "pair-right", "c>7-pivot"), kind)
        add_scaled(residual, full_vector(audit.parse_column(key)), -Fraction(coefficient_text))
    residual = retain(residual)
    target_payload = residual_text(residual)
    require(len(residual) == 884 and sha256(target_payload.encode()).hexdigest() ==
            c7["remaining_residual_sha256"], "target replay")
    if mutate:
        residual[min(residual)] += 1
        target_payload = residual_text(residual)
    require(sha256(target_payload.encode()).hexdigest() ==
            "69af8c7ceec28a7e2add37f7177fde19d8d58771796998a07bc34ae222d44aac",
            "hostile target mutation or drift")
    rows = tuple(sorted(residual))
    row_index = {row: index for index, row in enumerate(rows)}
    source_columns = set()
    for position, row in enumerate(rows, 1):
        source_columns.update(provider.HQ.canonical_column(column)
                              for column in provider.D24.incident_degree24_columns(row))
        require(len(source_columns) <= 100_000, len(source_columns))
        require(time.monotonic() - started < TIME_CAP, ("incidence time cap", position))
    source_columns = tuple(sorted(source_columns, key=provider.HQ.column_key))
    orbit_lookup = {}
    for index, row in enumerate(rows):
        for image in {provider.F.move_row(row, action) for action in provider.H}:
            old = orbit_lookup.setdefault(image, index)
            require(old == index, (old, index))
    singleton = {}
    projection_histogram = Counter()
    for position, column in enumerate(source_columns, 1):
        vector = Counter()
        for output in provider.D24.degree24_column_rows(column):
            index = orbit_lookup.get(output)
            if index is not None: vector[index] += 1
        vector = retain(vector)
        projection_histogram[len(vector)] += 1
        if len(vector) == 1:
            index, coefficient = next(iter(vector.items()))
            singleton.setdefault(index, (column, coefficient))
        require(time.monotonic() - started < TIME_CAP, ("projection time cap", position))
    require(len(singleton) == 884, ("singleton coverage", len(singleton)))

    certificate = []
    lifted = Counter()
    for index in range(884):
        column, boundary_coefficient = singleton[index]
        coefficient = residual[rows[index]] / boundary_coefficient
        orbit_size = provider.HQ.COLUMN_ORBIT_SIZE[column]
        certificate.append((index, column, boundary_coefficient, orbit_size, coefficient))
        add_scaled(lifted, full_vector(column), coefficient)
    require(all(lifted.get(row, 0) == residual[row] for row in rows),
            "singleton certificate failed on target")
    exterior = Counter(residual)
    add_scaled(exterior, lifted, -1)
    exterior = retain(exterior)
    require(all(row not in exterior for row in rows), "boundary survived lift")
    require(len(exterior) <= ROW_CAP, len(exterior))

    ledger_lines = ["boundary_index\tboundary_row\tcolumn\tboundary_coefficient\tcolumn_H_orbit_size\tnormalized_coefficient\tsource_orbit_mass_coefficient"]
    for index, column, boundary_coefficient, orbit_size, coefficient in certificate:
        ledger_lines.append(f"{index}\t{rows[index].hex()}\t{provider.HQ.column_key(column)}\t{boundary_coefficient}\t{orbit_size}\t{coefficient}\t{coefficient/orbit_size}")
    ledger_payload = "\n".join(ledger_lines) + "\n"
    LEDGER.write_text(ledger_payload)
    exterior_payload = residual_text(exterior)
    RESIDUAL.write_text(exterior_payload)

    core4568 = read_residual(GENERAL_RESIDUAL)
    require(len(core4568) == 4568 and sha256(GENERAL_RESIDUAL.read_bytes()).hexdigest() ==
            general["final_residual_tsv_sha256"], "4568 core drift")
    overlap884 = set(exterior) & set(residual)
    overlap4568 = set(exterior) & set(core4568)
    profile = Counter((provider.D24.row_k_degree(row), len(provider.graph_data(row)[0]))
                      for row in exterior)
    result = {
        "schema": "orbit0-k16-884-singleton-certificate-lift-v1",
        "status": "EXACT_884_COLUMN_BOUNDARY_LIFT_WITH_EXTERIOR",
        "source_column_H_orbits_scanned": len(source_columns),
        "projection_support_size_histogram": dict(sorted(projection_histogram.items())),
        "singleton_row_coverage": len(singleton),
        "certificate_columns": len(certificate),
        "certificate_max_numerator": max(abs(item[4].numerator) for item in certificate),
        "certificate_lcm_denominator": lcm(*(item[4].denominator for item in certificate)),
        "certificate_ledger_sha256": sha256(ledger_payload.encode()).hexdigest(),
        "exterior_support": len(exterior),
        "exterior_profile_K_degree_cycle_count": {
            f"{degree},{cycles}": count for (degree, cycles), count in sorted(profile.items())},
        "exterior_coefficient_l1": str(sum(abs(value) for value in exterior.values())),
        "exterior_max_numerator": max((abs(value.numerator) for value in exterior.values()), default=0),
        "exterior_lcm_denominator": lcm(*(value.denominator for value in exterior.values())) if exterior else 1,
        "exterior_residual_sha256": sha256(exterior_payload.encode()).hexdigest(),
        "comparison": {
            "original_boundary_support": 884,
            "normalized_core_support": 4568,
            "exterior_vs_original_difference": len(exterior) - 884,
            "exterior_vs_normalized_core_difference": len(exterior) - 4568,
            "exterior_overlap_original_boundary": len(overlap884),
            "exterior_overlap_normalized_core": len(overlap4568),
            "exterior_smaller_than_normalized_core": len(exterior) < 4568,
        },
        "scope_guard": "One exact singleton certificate lift through all K<=16 outputs; exterior tails are collected but not reduced or closed.",
        "pinned": {"boundary_projection_logical": "c9972e5253426b0db6ebaa470f5e4bcaaf86939d2b5136520f89897391e3b993",
                   "target_residual_sha256": c7["remaining_residual_sha256"],
                   "normalized4568_logical": general["logical_sha256"]},
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(result); logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(logical, sort_keys=True,
                                                  separators=(",", ":")).encode()).hexdigest()
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build(args.mutate)
    if not args.verify: OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in
                      ("status", "certificate_columns", "exterior_support",
                       "comparison", "logical_sha256", "elapsed_seconds")}, sort_keys=True))

if __name__ == "__main__":
    main()
