#!/usr/bin/env python3
"""Strict exact-Q assembler for the frozen grouped 35-ID K24 interface."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DAG_PATH = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
U = 400_591_699_200
HEX64 = re.compile(r"^[0-9a-f]{64}$")
BASES = {
    14: ["222"],
    15: ["223", "232", "322"],
    16: ["224", "233", "242", "323", "332", "422"],
    17: ["234", "243", "324", "333", "342", "423", "432"],
    18: ["244", "334", "343", "424", "433", "442"],
}


def ids(degree: int, response: str) -> list[str]:
    return [f"D{degree}:{packet}|R:{response}" for packet in BASES[degree]]


EXPECTED_GROUPS = {
    "source_D14_R2_2_2_4": ids(14, "2-2-2-4"),
    "source_D14_R2_4_4": ids(14, "2-4-4"),
    "source_D14_R3_3_4": ids(14, "3-3-4"),
    "source_D14_R4_2_4": ids(14, "4-2-4"),
    "source_D15_R2_3_4": ids(15, "2-3-4"),
    "source_D15_R3_2_4": ids(15, "3-2-4"),
    "source_D16_R2_2_4": ids(16, "2-2-4"),
    "source_D16_R4_4": ids(16, "4-4"),
    "source_D17_R3_4": ids(17, "3-4"),
    "source_D18_R2_4": ids(18, "2-4"),
}


def rational(value) -> Fraction:
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, dict):
        return Fraction(int(value["numerator"]), int(value["denominator"]))
    raise TypeError(value)


def rendered(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator, "text": str(value)}


def check_evidence(entry: dict) -> None:
    digest = entry.get("evidence_sha256", "")
    if not HEX64.fullmatch(digest):
        raise ValueError(f"bad evidence digest for {entry.get('group_id')}")
    relative = entry.get("evidence_path")
    if not isinstance(relative, str):
        raise ValueError(f"missing evidence path for {entry.get('group_id')}")
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise ValueError(f"evidence escapes workspace for {entry.get('group_id')}") from error
    if not path.is_file():
        raise ValueError(f"missing evidence file for {entry.get('group_id')}: {relative}")
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError(f"evidence hash mismatch for {entry.get('group_id')}")


def validate_groups(entries: list[dict]) -> tuple[list[str], list[str]]:
    seen = Counter(entry.get("group_id") for entry in entries)
    duplicate_groups = sorted(str(key) for key, count in seen.items() if count != 1)
    unknown_groups = sorted(str(key) for key in seen if key not in EXPECTED_GROUPS)
    if duplicate_groups or unknown_groups:
        raise ValueError(f"duplicate_group={duplicate_groups} unknown_group={unknown_groups}")
    flat: list[str] = []
    for entry in entries:
        group_id = entry.get("group_id")
        observed = entry.get("ids")
        if group_id not in EXPECTED_GROUPS or observed != EXPECTED_GROUPS[group_id]:
            raise ValueError(f"group partition/order mismatch for {group_id}")
        flat.extend(observed)
    return flat, [group for group in EXPECTED_GROUPS if group not in seen]


def assemble(manifest: dict, allow_partial: bool = False) -> dict:
    dag = json.loads(DAG_PATH.read_text())
    required = dag["required_reachable_lineage_ids_by_degree"]["24"]
    if len(required) != len(set(required)) or len(required) != 35:
        raise ValueError("frozen K24 interface is not 35 unique IDs")
    if manifest.get("degree") != 24 or int(manifest.get("scale_U", 0)) != U:
        raise ValueError("manifest degree/U mismatch")
    entries = manifest.get("groups")
    if not isinstance(entries, list):
        raise ValueError("manifest groups must be a list")
    flat, missing_groups = validate_groups(entries)
    counts = Counter(flat)
    duplicate = sorted(item for item, count in counts.items() if count != 1)
    extra = sorted(set(flat) - set(required))
    missing = [item for item in required if item not in set(flat)]
    if duplicate or extra:
        raise ValueError(f"duplicate={duplicate} extra={extra}")
    if missing and not allow_partial:
        raise ValueError(f"missing {len(missing)} K24 IDs: {missing}")

    full_scaled = 0
    irreducible_scaled = 0
    for entry in entries:
        check_evidence(entry)
        full_integer = int(entry["full_scaled_U"])
        irreducible_integer = int(entry["irreducible_scaled_U"])
        full = rational(entry["full"])
        irreducible = rational(entry["irreducible"])
        if Fraction(full_integer, U) != full or Fraction(irreducible_integer, U) != irreducible:
            raise ValueError(f"scaled/rational mismatch for {entry['group_id']}")
        if full_integer != irreducible_integer or full != irreducible:
            raise ValueError(f"K24 terminal full!=irreducible for {entry['group_id']}")
        full_scaled += full_integer
        irreducible_scaled += irreducible_integer

    complete = not missing
    return {
        "status": "PASS_COMPLETE_K24_35_ID_EXACT_Q" if complete else "REJECT_INCOMPLETE_K24_35_ID_GATE",
        "complete_K24_charge_claim": complete,
        "terminal_span_ready": False,
        "terminal_span_note": "charge assembly never substitutes for the separately validated literal H-row-orbit residual",
        "degree": 24,
        "scale_U": U,
        "required_paths": 35,
        "covered_paths": len(flat),
        "scalar_groups": len(entries),
        "required_scalar_groups": len(EXPECTED_GROUPS),
        "missing_scalar_groups": missing_groups,
        "missing_paths": missing,
        "duplicate_paths": duplicate,
        "extra_paths": extra,
        "full_scaled_U": str(full_scaled),
        "irreducible_scaled_U": str(irreducible_scaled),
        "full": rendered(Fraction(full_scaled, U)),
        "irreducible": rendered(Fraction(irreducible_scaled, U)),
        "covered_ids": flat,
        "full_equals_irreducible": full_scaled == irreducible_scaled,
        "dag_logical_sha256": dag["logical_sha256"],
        "manifest_logical_sha256": hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
    }


def self_test() -> dict:
    here = Path(__file__)
    relative = str(here.relative_to(ROOT))
    digest = hashlib.sha256(here.read_bytes()).hexdigest()
    entries = []
    for index, (group_id, group_ids) in enumerate(EXPECTED_GROUPS.items()):
        scalar = U * 7 // 3 if index == 0 else 0
        value = "7/3" if index == 0 else "0"
        entries.append({
            "group_id": group_id,
            "ids": group_ids,
            "full_scaled_U": scalar,
            "irreducible_scaled_U": scalar,
            "full": value,
            "irreducible": value,
            "evidence_path": relative,
            "evidence_sha256": digest,
        })
    good = {"degree": 24, "scale_U": U, "groups": entries}
    result = assemble(good)
    if not result["complete_K24_charge_claim"] or result["covered_paths"] != 35 or result["scalar_groups"] != 10 or result["full"]["text"] != "7/3":
        raise AssertionError("complete/group-once test failed")

    mutations = []
    missing = json.loads(json.dumps(good)); missing["groups"].pop(); mutations.append((missing, "missing 6"))
    duplicate = json.loads(json.dumps(good)); duplicate["groups"].append(duplicate["groups"][-1]); mutations.append((duplicate, "duplicate_group"))
    extra = json.loads(json.dumps(good)); extra["groups"][-1]["group_id"] = "hostile_extra"; mutations.append((extra, "unknown_group"))
    regrouped = json.loads(json.dumps(good)); regrouped["groups"][0]["ids"] += regrouped["groups"][1]["ids"]; mutations.append((regrouped, "partition/order"))
    reordered = json.loads(json.dumps(good)); reordered["groups"][4]["ids"].reverse(); mutations.append((reordered, "partition/order"))
    bad_u = json.loads(json.dumps(good)); bad_u["scale_U"] = U + 1; mutations.append((bad_u, "degree/U"))
    bad_terminal = json.loads(json.dumps(good)); bad_terminal["groups"][0]["irreducible_scaled_U"] = 0; bad_terminal["groups"][0]["irreducible"] = "0"; mutations.append((bad_terminal, "full!=irreducible"))
    bad_rational = json.loads(json.dumps(good)); bad_rational["groups"][0]["full"] = "0"; mutations.append((bad_rational, "scaled/rational"))
    bad_hash = json.loads(json.dumps(good)); bad_hash["groups"][0]["evidence_sha256"] = "0" * 64; mutations.append((bad_hash, "hash mismatch"))
    for mutation, expected in mutations:
        try:
            assemble(mutation)
        except ValueError as error:
            if expected not in str(error):
                raise
        else:
            raise AssertionError(f"hostile mutation accepted: {expected}")
    return {
        "status": "PASS_K24_35_ID_STRICT_ASSEMBLER_HOSTILE_SELFTEST",
        "required_ids": 35,
        "required_scalar_groups": 10,
        "group_scalar_once": True,
        "terminal_span_guard": "charge result always declares terminal_span_ready=false",
        "missing_duplicate_extra_regroup_reorder_U_terminality_rational_hash_rejected": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--self-test-output")
    parser.add_argument("--audit-incomplete", action="store_true")
    parser.add_argument("manifest", nargs="?")
    parser.add_argument("output", nargs="?")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
        if args.self_test_output:
            output = Path(args.self_test_output)
            temporary = Path(str(output) + ".tmp")
            temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
            temporary.replace(output)
        print(json.dumps(result, sort_keys=True))
        return
    if args.manifest is None or args.output is None:
        parser.error("manifest and output are required")
    try:
        result = assemble(json.loads(Path(args.manifest).read_text()), args.audit_incomplete)
    except ValueError as error:
        print(f"REJECT: {error}")
        raise SystemExit(2)
    output = Path(args.output)
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({key: result[key] for key in ("status", "covered_paths", "missing_paths", "full", "irreducible")}, indent=2))


if __name__ == "__main__":
    main()
