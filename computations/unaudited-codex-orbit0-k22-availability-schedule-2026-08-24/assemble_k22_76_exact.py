#!/usr/bin/env python3
"""Strict exact-Q assembler for the frozen 76-ID K22 interface."""

from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import re


ROOT = Path(__file__).resolve().parents[2]
DAG_PATH = ROOT / (
    "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/"
    "results_recurrence_dag.json"
)
U = 400_591_699_200
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def rational(value):
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, dict):
        return Fraction(int(value["numerator"]), int(value["denominator"]))
    raise TypeError(value)


def rendered(value):
    return {"numerator": value.numerator, "denominator": value.denominator, "text": str(value)}


def entry_ids(entry):
    if ("id" in entry) == ("ids" in entry):
        raise ValueError("exactly one of id/ids is required")
    values = [entry["id"]] if "id" in entry else entry["ids"]
    if not isinstance(values, list) or not values or not all(isinstance(item, str) for item in values) or len(values) != len(set(values)):
        raise ValueError(f"bad IDs {values}")
    return values


def evidence(entry):
    digest = entry.get("evidence_sha256", "")
    if not HEX64.fullmatch(digest):
        raise ValueError(f"bad evidence digest for {entry_ids(entry)}")
    relative = entry.get("evidence_path")
    if not isinstance(relative, str):
        raise ValueError(f"missing evidence path for {entry_ids(entry)}")
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        raise ValueError(f"evidence escapes workspace for {entry_ids(entry)}")
    if not path.is_file():
        raise ValueError(f"missing evidence file for {entry_ids(entry)}: {relative}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != digest:
        raise ValueError(f"evidence hash mismatch for {entry_ids(entry)}")


def assemble(manifest, allow_partial=False):
    dag = json.loads(DAG_PATH.read_text())
    required = dag["required_reachable_lineage_ids_by_degree"]["22"]
    if len(required) != len(set(required)) or len(required) != 76:
        raise ValueError("frozen K22 interface is not 76 unique IDs")
    if manifest.get("degree") != 22 or int(manifest.get("scale_U", 0)) != U:
        raise ValueError("manifest degree/U mismatch")
    entries = manifest.get("groups")
    if not isinstance(entries, list):
        raise ValueError("manifest groups must be a list")
    flat = [item for entry in entries for item in entry_ids(entry)]
    counts = Counter(flat)
    duplicate = sorted(item for item, count in counts.items() if count != 1)
    extra = sorted(set(flat) - set(required))
    missing = [item for item in required if item not in set(flat)]
    if duplicate or extra:
        raise ValueError(f"duplicate={duplicate} extra={extra}")
    if missing and not allow_partial:
        raise ValueError(f"missing {len(missing)} K22 IDs: {missing}")

    full_scaled = 0
    irreducible_scaled = 0
    for entry in entries:
        evidence(entry)
        fs = int(entry["full_scaled_U"])
        ins = int(entry["irreducible_scaled_U"])
        full = rational(entry["full"])
        irreducible = rational(entry["irreducible"])
        if Fraction(fs, U) != full or Fraction(ins, U) != irreducible:
            raise ValueError(f"scaled/rational mismatch for {entry_ids(entry)}")
        if fs != ins or full != irreducible:
            raise ValueError(f"K22 terminal full!=irreducible for {entry_ids(entry)}")
        full_scaled += fs
        irreducible_scaled += ins

    manifest_logical = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    complete = not missing
    return {
        "status": "PASS_COMPLETE_K22_76_ID_EXACT_Q" if complete else "REJECT_INCOMPLETE_K22_76_ID_GATE",
        "complete_K22_claim": complete,
        "degree": 22,
        "scale_U": U,
        "required_paths": 76,
        "covered_paths": len(flat),
        "scalar_groups": len(entries),
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
        "manifest_logical_sha256": manifest_logical,
    }


def self_test():
    dag = json.loads(DAG_PATH.read_text())
    required = dag["required_reachable_lineage_ids_by_degree"]["22"]
    here = Path(__file__)
    relative = str(here.relative_to(ROOT))
    digest = hashlib.sha256(here.read_bytes()).hexdigest()
    seven_thirds_scaled = U * 7 // 3
    good = {
        "degree": 22, "scale_U": U,
        "groups": [
            {"ids": required[:4], "full_scaled_U": seven_thirds_scaled, "irreducible_scaled_U": seven_thirds_scaled, "full": "7/3", "irreducible": "7/3", "evidence_path": relative, "evidence_sha256": digest},
            *({"id": item, "full_scaled_U": 0, "irreducible_scaled_U": 0, "full": "0", "irreducible": "0", "evidence_path": relative, "evidence_sha256": digest} for item in required[4:]),
        ],
    }
    result = assemble(good)
    if not result["complete_K22_claim"] or result["covered_paths"] != 76 or result["full"]["text"] != "7/3":
        raise AssertionError("complete/group-once test failed")
    mutations = []
    missing = json.loads(json.dumps(good)); missing["groups"].pop(); mutations.append((missing, "missing 1"))
    duplicate = json.loads(json.dumps(good)); duplicate["groups"].append(duplicate["groups"][-1]); mutations.append((duplicate, "duplicate"))
    extra = json.loads(json.dumps(good)); extra["groups"][-1]["id"] = "D99:hostile|R:2"; mutations.append((extra, "extra"))
    bad_u = json.loads(json.dumps(good)); bad_u["scale_U"] = U + 1; mutations.append((bad_u, "degree/U"))
    bad_terminal = json.loads(json.dumps(good)); bad_terminal["groups"][0]["irreducible_scaled_U"] = 0; bad_terminal["groups"][0]["irreducible"] = "0"; mutations.append((bad_terminal, "full!=irreducible"))
    bad_hash = json.loads(json.dumps(good)); bad_hash["groups"][0]["evidence_sha256"] = "0" * 64; mutations.append((bad_hash, "hash mismatch"))
    for mutation, expected in mutations:
        try:
            assemble(mutation)
        except ValueError as error:
            if expected not in str(error):
                raise
        else:
            raise AssertionError(f"hostile mutation accepted: {expected}")
    print(json.dumps({"status": "PASS_K22_76_ID_ASSEMBLER_SELFTEST", "group_scalar_once": True, "missing_duplicate_extra_U_terminality_hash_rejected": True}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--audit-incomplete", action="store_true")
    parser.add_argument("manifest", nargs="?")
    parser.add_argument("output", nargs="?")
    args = parser.parse_args()
    if args.self_test:
        self_test()
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
