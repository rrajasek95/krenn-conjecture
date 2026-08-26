#!/usr/bin/env python3
"""Build a strict partial K23 manifest from sealed fragment manifests."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ASSEMBLER = ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/assemble_k23_59_exact.py"
DIRECT23 = ROOT / "computations/unaudited-codex-orbit0-k23-direct23-source-fold-2026-08-24/k23_direct23_fragment_manifest.json"
DIRECT16 = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k16-18-charge-2026-08-24/k23_direct_k16_18_fragment_manifest.json"
DIRECT16_RESULT = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k16-18-charge-2026-08-24/results_k23_direct_k16_18.json"
PINS = {
    ASSEMBLER: "b189ddf195af4e5e896aee495bf7adbc074af0108a4f026ae852fbbabaacbaaf",
    DIRECT23: "57cdec4a6445c52bd7d35e1a97d37ef5f476f85e6c1de5b598d8c354b5db2d3b",
    DIRECT16: "9c37703f0c4e5c32f8993caf486eca18b8ed9d2bf46dab8a0192abc5af1397a1",
    DIRECT16_RESULT: "ba05ebd7bdd28528b6ff6ed78df60b776e43a7b0fcc19597d8023bad5ca403f0",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path, payload):
    path = Path(path)
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def load_assembler():
    spec = importlib.util.spec_from_file_location("k23_exact", ASSEMBLER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_fragment(path, id_to_group):
    doc = json.loads(path.read_text())
    if doc.get("degree") != 23 or int(doc.get("scale_U", 0)) != 400_591_699_200:
        raise ValueError(f"fragment degree/U mismatch: {path}")
    groups = []
    for raw in doc.get("groups", []):
        entry = dict(raw)
        ids = tuple(entry.get("ids", []))
        group_id = entry.get("group_id") or id_to_group.get(ids)
        if group_id is None:
            raise ValueError(f"fragment group lacks a schedule-exact group_id: {path} {ids}")
        entry["group_id"] = group_id
        groups.append(entry)
    return groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fragment", action="append", default=[])
    parser.add_argument("--manifest-output", default=str(HERE / "k23_manifest_current_41_of_59.json"))
    parser.add_argument("--result-output", default=str(HERE / "results_k23_current_41_of_59_partial.json"))
    args = parser.parse_args()
    for path, digest in PINS.items():
        if sha(path) != digest:
            raise SystemExit(f"REJECT pinned input hash: {path}")
    exact = load_assembler()
    id_to_group = {tuple(ids): group_id for group_id, ids in exact.EXPECTED_GROUPS.items()}
    direct16_result = json.loads(DIRECT16_RESULT.read_text())
    for group in direct16_result["groups"]:
        if id_to_group.get(tuple(group["ids"])) != group["group_id"]:
            raise SystemExit("REJECT direct-K16 result grouping")
    paths = [DIRECT23, DIRECT16] + [Path(name).resolve() for name in args.fragment]
    entries = []
    fragment_pins = []
    for path in paths:
        groups = normalize_fragment(path, id_to_group)
        entries.extend(groups)
        fragment_pins.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path), "scalar_groups": len(groups)})
    manifest = {
        "degree": 23,
        "scale_U": 400_591_699_200,
        "groups": entries,
        "fragment_inputs": fragment_pins,
        "scope": "strict partial K23 grouped-scalar manifest; incomplete input never authorizes a complete K23 charge claim",
    }
    result = exact.assemble(manifest, allow_partial=True)
    result["fragment_inputs"] = fragment_pins
    result["scope"] = "strict current K23 partial ledger; no complete claim unless all 59 frozen IDs pass the exact assembler"
    if not args.fragment:
        if (result["status"], result["complete_K23_claim"], result["covered_paths"], result["scalar_groups"], len(result["missing_paths"])) != ("REJECT_INCOMPLETE_K23_59_ID_GATE", False, 41, 7, 18):
            raise SystemExit("REJECT default current ledger is not exactly 41/59")
    atomic(args.manifest_output, manifest)
    atomic(args.result_output, result)
    print(json.dumps({"status": result["status"], "covered_paths": result["covered_paths"], "missing_paths": len(result["missing_paths"]), "scalar_groups": result["scalar_groups"], "full": result["full"]["text"]}, sort_keys=True))


if __name__ == "__main__":
    main()
