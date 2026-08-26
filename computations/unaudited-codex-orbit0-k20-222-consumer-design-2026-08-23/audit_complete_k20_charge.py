#!/usr/bin/env python3
"""Independent exact-Q closure audit for the final six K20 lineages."""
from fractions import Fraction
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K16 = ROOT / "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23"
U = 400_591_699_200
IDS = [f"D16:{packet}|R:2-2" for packet in ("224", "233", "242", "323", "332", "422")]

def load(path): return json.loads(path.read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

spec = importlib.util.spec_from_file_location("assembler", HERE / "assemble_k20_36_exact.py")
assembler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assembler)

old_manifest = load(HERE / "k20_path_manifest_30_partial.json")
old_result = load(HERE / "results_partial_k20_30path_6_gap.json")
charge_path = K16 / "results_k16_k2_group_charge.json"
sample_path = K16 / "results_k16_group_charge_sample_referee.json"
merge_path = K16 / "results_k16_merge_full_stream_referee.json"
charge = load(charge_path)
sample = load(sample_path)
merge = load(merge_path)
manifest = load(HERE / "k20_path_manifest_complete.json")
frozen = load(HERE / "results_complete_k20_36path_charge.json")

assert old_result["status"] == "REJECT_INCOMPLETE_K20_36_ID_GATE"
assert old_result["missing_paths"] == IDS
assert old_result["covered_paths"] == 30
assert old_result["full"]["text"] == "10272051610665334912/521603775"
assert old_result["irreducible"]["text"] == "10006754474458470016/521603775"

assert sha(charge_path) == "f308af113d523dfab36841acf703bf410eb7b73ea852d69397549af1746af46e"
assert sha(sample_path) == "6ed2bb7c4a9d0d529db6b51cd3226f0b2f6e0e049b56f4d7e1a64705f0ba8e0f"
assert sha(merge_path) == "02148afcd7465cea95f23a905121c0fe3c1bac2f703b88004a03939720ea4a50"
assert charge["status"] == "PASS_K16_K2_GROUPED_OCCURRENCEWISE_K20_CHARGE"
assert sample["status"] == "PASS_ALL_276_LITERAL_K16_K2_CHARGE_SAMPLE_REPLAY"
assert merge["status"] == "PASS_FULL_281_WAY_K16_STREAM_AND_BYTE_REPLAY"
assert charge["profile_records"] == merge["output_records"] == 6_876_260
assert charge["input_profile_uses"] == merge["output_uses"] == 1_604_299_948

full_add = Fraction(int(charge["full_77_charge_scaled"]), U)
irr_add = Fraction(int(charge["irreducible_77_charge_scaled"]), U)
assert full_add == Fraction(1_635_956_577_664, 385)
assert irr_add == Fraction(1_590_977_133_056, 385)

new_entry = manifest["paths"][-1]
assert manifest["paths"][:-1] == old_manifest["paths"]
assert new_entry == {
    "ids": IDS,
    "full": str(full_add),
    "irreducible": str(irr_add),
    "evidence_sha256": sha(charge_path),
}
result = assembler.assemble(manifest)
assert result == frozen
assert result["status"] == "PASS_COMPLETE_K20_36_ID_EXACT_Q"
assert result["full"]["text"] == "12488470121433187072/521603775"
assert result["irreducible"]["text"] == "12162234158979734656/521603775"
assert not result["missing_paths"] and result["covered_paths"] == 36

try:
    assembler.assemble({"paths": manifest["paths"][:-1]})
except ValueError as exc:
    assert "missing 6" in str(exc)
else:
    raise AssertionError("hostile deletion of the last six lineages passed")

out = {
    "status": "PASS_INDEPENDENT_COMPLETE_K20_36_PATH_CHARGE_AUDIT",
    "covered_paths": 36,
    "full": result["full"],
    "irreducible": result["irreducible"],
    "last_six_ids": IDS,
    "charge_sha256": sha(charge_path),
    "sample_referee_sha256": sha(sample_path),
    "merge_referee_sha256": sha(merge_path),
    "complete_result_sha256": sha(HERE / "results_complete_k20_36path_charge.json"),
    "hostile_six_path_deletion_rejected": True,
}
dest = HERE / "results_complete_k20_independent_audit.json"
dest.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps(out, sort_keys=True))
