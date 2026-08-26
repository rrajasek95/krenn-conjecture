#!/usr/bin/env python3
"""Project literal two-cut critical pairs to Generic's 28 c6 boundary rows."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C6_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-c6-schur-boundary-2026-08-23"
C6_SCRIPT = C6_DIR / "audit_k16_c6_schur_boundary.py"
C6_RESULT = C6_DIR / "results_k16_c6_schur_boundary.json"
INTERFACE = C6_DIR / "boundary_incident_interface.json"
OUT = HERE / "results_c6_boundary_literal_critical_pairs.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def rank_q(vectors):
    basis = {}
    for vector in vectors:
        value = {index: Fraction(coefficient)
                 for index, coefficient in enumerate(vector) if coefficient}
        while value:
            pivot = min(value)
            if pivot not in basis:
                scale = value[pivot]
                basis[pivot] = {index: coefficient / scale
                                for index, coefficient in value.items()}
                break
            scale = value[pivot]
            for index, coefficient in basis[pivot].items():
                updated = value.get(index, 0) - scale * coefficient
                if updated:
                    value[index] = updated
                else:
                    value.pop(index, None)
    return len(basis)


def primitive(vector):
    divisor = 0
    for value in vector:
        divisor = gcd(divisor, abs(value))
    require(divisor, vector)
    value = tuple(entry // divisor for entry in vector)
    first = next(entry for entry in value if entry)
    return tuple(-entry for entry in value) if first < 0 else value


def main():
    started = time.monotonic()
    C6 = load("literal_pair_c6", C6_SCRIPT)
    HQ, D24 = C6.HQ, C6.D24
    seed = json.loads(C6_RESULT.read_text())
    page = json.loads(INTERFACE.read_text())
    literal_blockers = tuple(bytes.fromhex(record["row"])
                             for record in seed["blockers"])
    blockers = tuple(HQ.canonical_row(row) for row in literal_blockers)
    blocker_index = {row: index for index, row in enumerate(blockers)}
    require(len(blockers) == len(blocker_index) == 28, len(blockers))
    require(all(literal != canonical for literal, canonical in
                zip(literal_blockers, blockers, strict=True)),
            "expected the 28 WD representatives to require H canonicalization")
    target = tuple(Fraction(*record["target_mass"])
                   for record in seed["blockers"])

    column_vectors = {}
    high_parents = set()
    for record in page["columns"]:
        orbit_size = record["orbit_size"]
        vector = [0] * 28
        for row_hex, mass in record["entries"]:
            row = bytes.fromhex(row_hex)
            if row in blocker_index:
                require(mass % orbit_size == 0, (record["key"], row_hex, mass,
                                                   orbit_size))
                vector[blocker_index[row]] += mass // orbit_size
            if D24.row_k_degree(row) == 16 and len(C6.graph_data(row)[0]) >= 7:
                high_parents.add(row)
        column_vectors[record["key"]] = tuple(vector)
    require(len(column_vectors) == 1_114, len(column_vectors))
    require(len(high_parents) == 374, len(high_parents))

    zero = (0,) * 28
    pair_vectors = {}
    literal_columns_examined = 0
    literal_pairs_examined = 0
    parent_with_pair = 0
    parents_touching_boundary = 0
    for parent_ordinal, parent in enumerate(sorted(high_parents), 1):
        raw_columns = sorted(set(D24.incident_degree24_columns(parent)),
                             key=lambda column: (column[0], column[1]))
        descriptors = []
        touches = False
        for column in raw_columns:
            literal_columns_examined += 1
            outputs = D24.degree24_column_rows(column)
            parent_coefficient = sum(row == parent for row in outputs)
            require(parent_coefficient > 0, (parent.hex(), column,
                                              parent_coefficient))
            key = HQ.column_key(HQ.canonical_column(column))
            vector = column_vectors.get(key, zero)
            touches |= vector != zero
            descriptors.append((parent_coefficient, vector, key))
        if touches:
            parents_touching_boundary += 1
        found = False
        for left_index, (left_coefficient, left, left_key) in enumerate(descriptors):
            for right_coefficient, right, right_key in descriptors[left_index + 1:]:
                literal_pairs_examined += 1
                vector = tuple(right_coefficient * x - left_coefficient * y
                               for x, y in zip(left, right, strict=True))
                if vector == zero:
                    continue
                found = True
                normalized = primitive(vector)
                pair_vectors.setdefault(normalized, {
                    "parent": parent.hex(),
                    "left_column": left_key,
                    "right_column": right_key,
                    "left_parent_coefficient": left_coefficient,
                    "right_parent_coefficient": right_coefficient,
                })
        parent_with_pair += found
        require(time.monotonic() - started < 115,
                ("time cap", parent_ordinal, len(pair_vectors)))

    vectors = tuple(sorted(pair_vectors))
    rank = rank_q(vectors)
    augmented_rank = rank_q(vectors + (target,))
    covered = tuple(index for index in range(28)
                    if any(vector[index] for vector in vectors))
    target_support = tuple(index for index, value in enumerate(target) if value)
    digest_payload = "\n".join(
        ",".join(map(str, vector)) for vector in vectors) + "\n"
    result = {
        "schema": "orbit0-k16-c6-literal-critical-pair-projection-v1",
        "status": "EXACT_28_COORDINATE_PROJECTION_ONLY",
        "boundary_coordinates": 28,
        "high_cycle_K16_parent_orbits": len(high_parents),
        "parents_touching_boundary": parents_touching_boundary,
        "parents_with_nonzero_critical_pair": parent_with_pair,
        "literal_source_columns_examined": literal_columns_examined,
        "literal_two_cut_pairs_examined": literal_pairs_examined,
        "distinct_primitive_projected_pair_vectors": len(vectors),
        "covered_boundary_coordinates": list(covered),
        "coverage": len(covered),
        "rank_over_Q": rank,
        "target_support": list(target_support),
        "target_augmented_rank_over_Q": augmented_rank,
        "target_in_projected_span": augmented_rank == rank,
        "pair_vector_sha256": sha256(digest_payload.encode()).hexdigest(),
        "lex_first_provenance": pair_vectors[vectors[0]] if vectors else None,
        "scope": (
            "Each vector is the 28-coordinate H-orbit projection of an exact "
            "difference of two literal mixed degree24 source columns incident "
            "to the same K16 parent, scaled to cancel that literal parent. "
            "This is only the frozen c6 boundary projection; it is not global "
            "membership, Schur closure, or a K16 theorem."
        ),
        "pinned": {
            "boundary_seed_logical": seed["logical_sha256"],
            "incident_interface_logical": page["logical_sha256"],
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "high_cycle_K16_parent_orbits",
        "literal_source_columns_examined", "literal_two_cut_pairs_examined",
        "distinct_primitive_projected_pair_vectors", "coverage", "rank_over_Q",
        "target_augmented_rank_over_Q", "target_in_projected_span",
        "logical_sha256", "elapsed_seconds")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
