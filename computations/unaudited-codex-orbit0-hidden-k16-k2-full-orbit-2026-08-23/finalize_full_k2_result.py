#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_full_hidden_k16_k2_orbits.json"
j = json.loads(RESULT.read_text())
assert j["status"] == "PASS_FULL_ORBIT_AWARE_K18_22_COLLECTION"
assert (j["K18_pivotable_support"], j["K18_irreducible_support"], j["K18_cross_chunk_exact_zero_rows"]) == (158439965, 110465931, 3346)
assert int(j["pivotable_weight_sum_scaled"]) + int(j["irreducible_weight_sum_scaled"]) == int(j["total_K18_weight_sum_scaled"]) == 1754767313172666777600
j["checkpoint_sha256"] = {
    "pivotable": "442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8",
    "irreducible": "c60fd9763d604f27213542a3bec9376849e046be06edf4e68035c849b097e111",
}
j["merge_source_sha256"] = hashlib.sha256((HERE / "run_full_hidden_k16_k2_orbits.rs").read_bytes()).hexdigest()
j["child_chunks_retained"] = len(list(HERE.glob("pchild_chunk_*.bin")))
assert j["child_chunks_retained"] == 291
core = {k: v for k, v in j.items() if k not in ("elapsed_seconds", "logical_sha256")}
j["logical_sha256"] = hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
tmp = RESULT.with_suffix(".json.tmp")
tmp.write_text(json.dumps(j, indent=2, sort_keys=True) + "\n")
tmp.replace(RESULT)
print(json.dumps({k: j[k] for k in ("status", "logical_sha256", "checkpoint_sha256", "child_chunks_retained")}, indent=2))
