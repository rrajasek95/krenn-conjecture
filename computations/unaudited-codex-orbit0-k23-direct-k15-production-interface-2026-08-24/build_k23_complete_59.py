#!/usr/bin/env python3
"""Integrate the sealed K23 47/59 baseline with the final direct-K15 fragment."""

import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-orbit0-k23-d14-source-three-fold-2026-08-24/k23_manifest_current_47_of_59.json"
FRAGMENT = HERE / "k23_direct_k15_fragment_manifest.json"
ASSEMBLER = ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/assemble_k23_59_exact.py"
PINS = {
    BASE: "35089c36f649a5942c3203ce0f6b1c612aef9ce9dd741e159edeb946074b13b1",
    FRAGMENT: "7b16c53e372282a02aaa054fcd1abc3bf45159c2e9c190ab7d1ed47ca6ec10b5",
    ASSEMBLER: "b189ddf195af4e5e896aee495bf7adbc074af0108a4f026ae852fbbabaacbaaf",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path, value):
    if path.exists():
        raise RuntimeError(f"refuse overwrite: {path}")
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main():
    for path, digest in PINS.items():
        assert path.is_file() and sha(path) == digest, path
    base = json.loads(BASE.read_text())
    fragment = json.loads(FRAGMENT.read_text())
    assert base["degree"] == fragment["degree"] == 23
    assert int(base["scale_U"]) == int(fragment["scale_U"]) == 400_591_699_200
    assert len(base["groups"]) == 13
    assert sum(len(entry["ids"]) for entry in base["groups"]) == 47
    assert [entry["group_id"] for entry in fragment["groups"]] == [
        "source_D15_R2_2_4", "source_D15_R2_3_3",
        "source_D15_R3_2_3", "source_D15_R4_4",
    ]
    assert sum(len(entry["ids"]) for entry in fragment["groups"]) == 12
    manifest = {
        "degree": 23,
        "scale_U": 400_591_699_200,
        "fragment_inputs": base["fragment_inputs"] + [{
            "path": str(FRAGMENT.relative_to(ROOT)),
            "sha256": sha(FRAGMENT),
            "scalar_groups": 4,
        }],
        "groups": base["groups"] + fragment["groups"],
        "scope": "strict complete K23 59-ID grouped-scalar manifest; each of 17 frozen source scalars counted exactly once",
    }
    spec = importlib.util.spec_from_file_location("k23_assembler", ASSEMBLER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    hostile = module.self_test()
    result = module.assemble(manifest, allow_partial=False)
    assert hostile["status"] == "PASS_K23_59_ID_STRICT_ASSEMBLER_HOSTILE_SELFTEST"
    assert result["status"] == "PASS_COMPLETE_K23_59_ID_EXACT_Q"
    assert result["complete_K23_claim"] is True
    assert result["covered_paths"] == result["required_paths"] == 59
    assert result["scalar_groups"] == result["required_scalar_groups"] == 17
    assert result["missing_paths"] == result["duplicate_paths"] == result["extra_paths"] == []
    assert result["missing_scalar_groups"] == [] and result["full_equals_irreducible"] is True
    result["fragment_inputs"] = manifest["fragment_inputs"]
    result["scope"] = "complete exact K23 charge assembly only; no K24 or conjecture verdict"
    atomic(HERE / "k23_manifest_complete_59_of_59.json", manifest)
    atomic(HERE / "results_k23_complete_59_of_59.json", result)
    atomic(HERE / "results_k23_final_assembler_hostile_selftest.json", hostile)
    print(json.dumps({
        "status": result["status"],
        "covered_paths": result["covered_paths"],
        "scalar_groups": result["scalar_groups"],
        "full": result["full"]["text"],
        "irreducible": result["irreducible"]["text"],
    }, indent=2))


if __name__ == "__main__":
    main()
