#!/usr/bin/env python3
"""Exact referee for the corrected canonical 28-row Schur projection."""

from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROVIDER = HERE / "audit_k16_c6_schur_boundary.py"
SEED = HERE / "results_k16_c6_schur_boundary.json"
SCHUR = HERE / "boundary_schur_interface.json"
OUT = HERE / "results_k16_c6_signed_projection.json"

def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)

def load_provider():
    spec = importlib.util.spec_from_file_location("k16_c6_signed_provider", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, PROVIDER)
    spec.loader.exec_module(module)
    return module

def build(mutate=False):
    provider = load_provider()
    seed = json.loads(SEED.read_text())
    schur = json.loads(SCHUR.read_text())
    require(seed["logical_sha256"] == "1d893557e556b967d1ab123de8027d320c3f736161606972d9a2e2fbf4a21826", seed["logical_sha256"])
    require(schur["logical_sha256"] == "260dd9e763c906816c109bbcf06e1f607bec4c144c9023ea97bbf9a3ae69a03e", schur["logical_sha256"])
    raw = [bytes.fromhex(record["row"]) for record in seed["blockers"]]
    true_canonical = [provider.HQ.canonical_row(row) for row in raw]
    canonical = raw if mutate else true_canonical
    require(len(set(canonical)) == 28, len(set(canonical)))
    noncanonical_raw = sum(left != right for left, right in zip(raw, true_canonical, strict=True))
    require(noncanonical_raw == 28, noncanonical_raw)
    blocker_index = {row: index for index, row in enumerate(canonical)}
    vectors = []
    nonzero_columns = incidence = 0
    for record in schur["columns"]:
        vector = {}
        for row_hex, value in record["entries"]:
            row = bytes.fromhex(row_hex)
            if row in blocker_index and value:
                vector[blocker_index[row]] = Fraction(value)
        if vector:
            nonzero_columns += 1
            incidence += len(vector)
        vectors.append(vector)
    basis = {}
    for column_index, source in enumerate(vectors):
        value = dict(source)
        combination = {column_index: Fraction(1)}
        while value:
            pivot = min(value)
            if pivot not in basis:
                scale = value[pivot]
                value = {row: coefficient / scale for row, coefficient in value.items()}
                combination = {index: coefficient / scale for index, coefficient in combination.items()}
                basis[pivot] = (value, combination)
                break
            scale = value[pivot]
            old_value, old_combination = basis[pivot]
            for row, coefficient in old_value.items():
                updated = value.get(row, 0) - scale * coefficient
                if updated: value[row] = updated
                else: value.pop(row, None)
            for index, coefficient in old_combination.items():
                updated = combination.get(index, 0) - scale * coefficient
                if updated: combination[index] = updated
                else: combination.pop(index, None)
    target = {index: Fraction(*record["target_mass"]) for index, record in enumerate(seed["blockers"])}
    remainder = dict(target)
    solution = {}
    while remainder:
        pivot = min(remainder)
        require(pivot in basis, ("target outside projected span", pivot, len(basis)))
        scale = remainder[pivot]
        value, combination = basis[pivot]
        for row, coefficient in value.items():
            updated = remainder.get(row, 0) - scale * coefficient
            if updated: remainder[row] = updated
            else: remainder.pop(row, None)
        for index, coefficient in combination.items():
            updated = solution.get(index, 0) + scale * coefficient
            if updated: solution[index] = updated
            else: solution.pop(index, None)
    replay = {row: sum(solution.get(index, 0) * vectors[index].get(row, 0) for index in solution) for row in range(28)}
    require(replay == target, (replay, target))
    payload = {
        "schema": "orbit0-k16-c6-canonical-signed-projection-v1",
        "status": "EXACT_RELATIVE_BOUNDARY_FILL",
        "blocker_coordinates": 28,
        "raw_frozen_representatives_noncanonical_under_H": noncanonical_raw,
        "incident_schur_columns": len(vectors),
        "projected_nonzero_columns": nonzero_columns,
        "projected_nonzero_entries": incidence,
        "projected_rank_over_Q": len(basis),
        "target_augmented_rank_over_Q": len(basis),
        "target_in_projected_span": True,
        "target_solution_nonzero_columns": len(solution),
        "target_solution": [{"column_index": index, "column": schur["columns"][index]["key"], "coefficient": [coefficient.numerator, coefficient.denominator]} for index, coefficient in sorted(solution.items())],
        "representation_guard": "All 28 frozen collector representatives must be transported through HQ.canonical_row before comparison with canonical interface rows.",
        "scope_guard": "Exact 28-coordinate projection of the corrected signed 1,114-column one-page Schur interface; exterior rows and backward critical-pair feeds are not solved here.",
        "pinned": {"boundary_seed_logical": seed["logical_sha256"], "signed_schur_logical": schur["logical_sha256"]},
    }
    payload["logical_sha256"] = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return payload

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    payload = build(args.mutate)
    if not args.verify:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in ("status", "projected_rank_over_Q", "target_augmented_rank_over_Q", "target_solution_nonzero_columns", "logical_sha256")}, sort_keys=True))

if __name__ == "__main__":
    main()
