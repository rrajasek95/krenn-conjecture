#!/usr/bin/env python3
"""Audit the rejected row gate and the exact factorized K24 replacement."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DIAGNOSTIC = HERE / "results_prefix1_materialized_rejection.json"
WITNESSES = HERE / "prefix1/literal_witnesses.tsv"
SCHEMA = HERE / "factorized_k24_residual_interface.schema.json"
PRODUCER = HERE / "run_k24_residual_direct_d17_d18_gate.rs"
PROVIDER = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23/k24_factorized_gram_provider.py"
EXPECTED_IDS = {
    "source_D17_R3_4": [f"D17:{packet}|R:3-4" for packet in ("234", "243", "324", "333", "342", "423", "432")],
    "source_D18_R2_4": [f"D18:{packet}|R:2-4" for packet in ("244", "334", "343", "424", "433", "442")],
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def tree_geometry(path: Path) -> tuple[int, int]:
    files = [item for item in path.rglob("*") if item.is_file()]
    return len(files), sum(item.stat().st_size for item in files)


def remove_multiset(row: bytes, anchor: bytes) -> bytes:
    values = list(row)
    for cell in anchor:
        values.remove(cell)
    require(len(values) == 20, (row.hex(), anchor.hex()))
    return bytes(sorted(values))


def main() -> None:
    diagnostic = json.loads(DIAGNOSTIC.read_text())
    schema = json.loads(SCHEMA.read_text())
    require(schema["$id"] == "factorized-k24-H-column-orbit-residual-v1", schema.get("$id"))
    require(diagnostic["status"] == "REJECT_MATERIALIZED_K24_ROW_INTERFACE_RESOURCE_GATE", diagnostic)
    require(not diagnostic["accepted_residual_claim"] and not diagnostic["accepted_charge_claim"], diagnostic)
    require(digest(PRODUCER) == diagnostic["producer_source_sha256"], "producer source drift")
    require(digest(WITNESSES) == diagnostic["literal_witness_ledger_sha256"], "witness drift")
    file_count, total_bytes = tree_geometry(HERE / "prefix1")
    require(total_bytes == diagnostic["diagnostic_directory_bytes"], (total_bytes, diagnostic["diagnostic_directory_bytes"]))
    require(diagnostic["linear_disk_projections"]["full485_bytes"] > 10**12, diagnostic)
    require(diagnostic["linear_disk_projections"]["prefix61_bytes"] > diagnostic["filesystem_available_bytes_at_gate"], diagnostic)
    require(not diagnostic["prefix8_launched"] and not diagnostic["prefix61_launched"] and not diagnostic["full_launched"], diagnostic)

    gram = load("k24_factorized_gate_provider", PROVIDER)
    words = []
    anchors = []
    for colours in itertools.product(range(3), repeat=4):
        if len(set(colours)) == 1:
            continue
        word = gram.F.word_from_pair_colours(colours)
        words.append(word)
        anchors.append(gram.F.BASE.term_ids(word, gram.F.M0))
    require(len(words) == len(anchors) == 78, (len(words), len(anchors)))

    records = list(csv.DictReader(WITNESSES.open(), delimiter="\t"))
    require(len(records) == 2, len(records))
    proof = []
    for record in records:
        group = record["group_id"]
        require(group in EXPECTED_IDS and record["lineage_id"] in EXPECTED_IDS[group], record)
        p2 = int(record["p2"])
        parent = bytes.fromhex(record["intermediate_row"])
        literal = bytes.fromhex(record["literal_K24_row"])
        canonical = bytes.fromhex(record["H_canonical_row"])
        require(len(parent) == len(literal) == len(canonical) == 24, record)
        require(list(parent) == sorted(parent) and list(literal) == sorted(literal), record)
        multiplier = remove_multiset(parent, anchors[p2])
        column = (words[p2], multiplier)
        representative = gram.canonical_column(column)
        outputs = gram.top_outputs(column)
        require(len(outputs) == 60 and literal in outputs, (group, len(outputs)))
        require(all(gram.D24.row_k_degree(row) == 24 for row in outputs), group)
        require(gram.canonical_row(literal) == canonical, group)
        orbit_size = len(gram.row_orbit(literal))
        require(orbit_size == int(record["orbit_size"]), (group, orbit_size))
        action = int(record["H_action_or_witness"].split("=", 1)[1])
        require(gram.F.move_row(literal, gram.H[action]) == canonical, (group, action))
        coefficient = Fraction(record["exact_signed_fraction"])
        require(coefficient < 0, (group, coefficient))
        vector = gram.orbit_column_vector(representative)
        require(vector and all(mass % size == 0 for _row, mass, size in vector), group)
        require(sum(mass for _row, mass, _size in vector) == len(gram.column_orbit(representative)) * 60, group)
        proof.append({
            "group_id": group,
            "lineage_witness": record["lineage_id"],
            "selected_pivot": p2,
            "canonical_column_key": gram.column_key(representative),
            "column_orbit_size": len(gram.column_orbit(representative)),
            "top_outputs_per_labelled_column": len(outputs),
            "H_row_orbit_coordinates": len(vector),
            "literal_output_in_provider_top": True,
            "producer_H_canonical_row_replayed": True,
            "exact_signed_coefficient": str(coefficient),
        })

    full_p2 = {"source_D17_R3_4": 842_301_440, "source_D18_R2_4": 230_937_600}
    total_p2 = sum(full_p2.values())
    result = {
        "status": "PASS_REJECT_MATERIALIZED_ROWS_AND_ACCEPT_EXACT_FACTORIZED_K24_INTERFACE_DESIGN",
        "materialized_prefix": {
            "accepted": False,
            "elapsed_seconds_at_interrupt": diagnostic["elapsed_seconds_at_interrupt"],
            "bytes_at_interrupt": total_bytes,
            "files_at_interrupt": file_count,
            "phase": diagnostic["phase_at_interrupt"],
            "full_linear_projection_bytes": diagnostic["linear_disk_projections"]["full485_bytes"],
            "partial_runs_are_diagnostic_only": True,
        },
        "factorized_interface": {
            "schema": str(SCHEMA.relative_to(ROOT)),
            "schema_sha256": digest(SCHEMA),
            "provider": str(PROVIDER.relative_to(ROOT)),
            "provider_sha256": digest(PROVIDER),
            "strict_groups": EXPECTED_IDS,
            "full_selected_K20_pivot_occurrences": full_p2,
            "full_selected_K20_pivot_occurrences_total": total_p2,
            "raw_record_bytes": 37,
            "raw_full_upper_bound_bytes": total_p2 * 37,
            "row_fan_avoided_per_record": 60,
            "literal_witness_provider_replays": proof,
        },
        "exact_formulas": {
            "record": "canonical H-column orbit C, orbit-total weight W_C, orbit size o_C, alpha_C=W_C/o_C",
            "row_orbit_mass_on_demand": "m_R(r)=sum_C alpha_C*m_C(r)",
            "target_pairing_on_demand": "<v_D,R>=sum_C alpha_C*G_D,C",
            "target_norm_on_demand": "||R||^2=sum_C,E alpha_C*alpha_E*G_C,E, evaluated componentwise",
            "charge_on_demand": "Q(R)=sum_C alpha_C*sum_r m_C(r)*q(r)",
            "constructive_span": "the alpha_C ledger is itself an exact rational source vector x with R=A*x",
        },
        "production_schedule": {
            "source_intervals": [[485 * index // 8, 485 * (index + 1) // 8] for index in range(8)],
            "prefixes_before_any_shard": [1, 8, 61],
            "launch_gate": "factorized producer only: <=540s, <=8GiB family RSS, measured raw/canonical column output below available disk",
            "hard_wall_seconds": 600,
            "materialized_row_mode_forbidden": True,
            "resource_clearance_required": True,
        },
        "scope": "design and two literal/provider proof witnesses only; no factorized full producer run, K24 charge, complete residual, terminal-span verdict, or conjecture claim",
    }
    logical = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    output = HERE / "results_k24_factorized_residual_gate.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({
        "status": result["status"],
        "materialized_bytes": total_bytes,
        "factorized_raw_full_upper_bound_bytes": total_p2 * 37,
        "witnesses": len(proof),
        "logical_sha256": logical,
    }, indent=2))


if __name__ == "__main__":
    main()
