#!/usr/bin/env python3
"""Add the sealed D14 source-three fragment to the corrected K23 44/59 baseline."""

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-orbit0-k23-hidden-decorated-pair-2026-08-24/k23_manifest_current_44_of_59.json"
FRAGMENT = HERE / "k23_d14_source_three_fragment_manifest.json"
ASSEMBLER = ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/assemble_k23_59_exact.py"
PINS = {
    BASE: "c612ea42d449e2a170c7ecfb0200fd5c8d855ea30584ba699ef08a3bb720de00",
    FRAGMENT: "396619051874eb4ca976eebd8b8cee00c33b1eb4f29ea0bb4048f35668da07a7",
    ASSEMBLER: "b189ddf195af4e5e896aee495bf7adbc074af0108a4f026ae852fbbabaacbaaf",
}

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    for path, digest in PINS.items(): assert sha(path) == digest
    base = json.loads(BASE.read_text()); fragment = json.loads(FRAGMENT.read_text())
    assert len(base["groups"]) == 10 and sum(len(x["ids"]) for x in base["groups"]) == 44
    assert [x["group_id"] for x in fragment["groups"]] == ["source_D14_R3_2_4","source_D14_R3_3_3","source_D14_R4_2_3"]
    manifest = {
        "degree": 23,
        "scale_U": 400_591_699_200,
        "fragment_inputs": base["fragment_inputs"] + [{
            "path": str(FRAGMENT.relative_to(ROOT)), "sha256": sha(FRAGMENT), "scalar_groups": 3,
        }],
        "groups": base["groups"] + fragment["groups"],
        "scope": "strict current K23 47/59 grouped-scalar manifest; incomplete input never authorizes a complete K23 charge claim",
    }
    output = HERE / "k23_manifest_current_47_of_59.json"
    tmp = Path(str(output)+".tmp"); tmp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n"); tmp.replace(output)
    spec=importlib.util.spec_from_file_location("assembler",ASSEMBLER);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=module.assemble(manifest,allow_partial=True)
    result["fragment_inputs"] = manifest["fragment_inputs"]
    result["scope"] = "strict current K23 partial ledger after sealed D14 source-three integration; no complete claim unless all 59 frozen IDs pass"
    result_output=HERE/"results_k23_current_47_of_59_partial.json"
    tmp=Path(str(result_output)+".tmp");tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");tmp.replace(result_output)
    print(json.dumps({"status":result["status"],"covered_paths":result["covered_paths"],"missing_paths":len(result["missing_paths"]),"scalar_groups":result["scalar_groups"],"full":result["full"]["text"]},indent=2))

if __name__ == "__main__": main()
