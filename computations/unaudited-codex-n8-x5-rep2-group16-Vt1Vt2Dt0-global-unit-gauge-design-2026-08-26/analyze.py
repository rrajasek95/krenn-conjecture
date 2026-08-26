#!/usr/bin/env python3
"""Replay the audited exact analyzer on the unlaunched V(t1,t2) intersect D(t0) chart."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/analyze.py"
TEMPLATE_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26/MANIFEST.sha256"
UPSTREAM = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(TEMPLATE_MANIFEST) == "aab19d2f51693fed67f587d83fe0d2e108888d626d788e4d00a9362a3be978be"
assert sha(UPSTREAM / "sources/rep2_group016_67_Vt1_Vt2_Dt0_runtime_Q.sing") == "819ba657d4e7ad27e0348613b72c84bfca517376bfab6158b50c07a09e87509b"
assert sha(UPSTREAM / "batch_result.json") == "5b3250c4ee21d1392e148f4094bf6095bd39e94a835799cc6b3d643a79e6b510"
batch = json.loads((UPSTREAM / "batch_result.json").read_text())
assert batch["status"] == "STOPPED_FAIL_CLOSED" and batch["skipped_after_stop"] == ["Vt1_Vt2_Dt0"]

# The full parser, exact Fraction echelon, primitive-minor search,
# specialization, byte replay, and source serializer are pinned by the sealed
# D(t1) design.  Only the source identity and package output root differ.
program = TEMPLATE.read_text()
program = program.replace(
    "HERE = Path(__file__).resolve().parent",
    f"HERE = Path({str(HERE)!r})",
    1,
).replace(
    "ROOT = HERE.parents[1]",
    f"ROOT = Path({str(ROOT)!r})",
    1,
).replace(
    "rep2_group016_67_Dt1_runtime_Q.sing",
    "rep2_group016_67_Vt1_Vt2_Dt0_runtime_Q.sing",
).replace(
    "f0212ca6edfec2941b68a0161d8a4f81c9455f3729d94150e16eafb057043244",
    "819ba657d4e7ad27e0348613b72c84bfca517376bfab6158b50c07a09e87509b",
)
namespace = {"__name__": "__rep2_exact_analyzer_replay__", "__file__": str(HERE / "_pinned_template_replay.py")}
exec(compile(program, namespace["__file__"], "exec"), namespace)

result_path = HERE / "results_design.json"
result = json.loads(result_path.read_text())
assert result["status"] == "PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE"
result["schema"] = "KRENN_X5_REP2_GROUP16_VT1VT2DT0_GLOBAL_UNIT_GAUGE_DESIGN_V1"
old_binding = result.pop("timeout_binding")
assert old_binding["rerun"] is False
result["batch_stop_binding"] = {
    "batch_result_sha256": sha(UPSTREAM / "batch_result.json"),
    "terminal_manifest_sha256": sha(UPSTREAM / "TERMINAL_MANIFEST.sha256"),
    "strict_order": batch["strict_order"],
    "skipped_after_stop": batch["skipped_after_stop"],
    "this_chart_previously_launched": False,
}
result["conclusion"] = {
    "singular_runs": 0,
    "mathematical_coverage": False,
    "prior_batch_stop_preserved": True,
    "this_chart_previously_launched": False,
}
temporary = result_path.with_suffix(".json.tmp")
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, result_path)
print(json.dumps({
    "status": result["status"],
    "shape": [result["cover"]["sources"][0]["variables"], result["cover"]["sources"][0]["generators"]],
    "terms": result["cover"]["sources"][0]["total_terms"],
    "solver_runs": 0,
}, sort_keys=True))
