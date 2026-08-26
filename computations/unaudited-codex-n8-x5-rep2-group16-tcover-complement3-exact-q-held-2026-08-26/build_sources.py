#!/usr/bin/env python3
"""Materialize the three exact-Q charts complementary to the closed-t chart."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-referee-2026-08-26"
CLOSED = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-closed-t-exact-q-terminal-referee-2026-08-26"
PINS = {
    DESIGN / "MANIFEST.sha256": "3d4d6fbc89f5adcc45032c37b1b038780761f479313575c59e4e8bd760da75fd",
    DESIGN / "results_design.json": "10c7c360683bfc780645ccb16d7a9d5f50500cc3af8272b5f49f1f8c2451bf00",
    REFEREE / "MANIFEST.sha256": "e41de381875869a6ac206454b57e091b7ed1093f76aad4a9b71ed30929d3b3cd",
    REFEREE / "results_referee.json": "43c1b39cf444c39a3a25f58cd9fb42d94d4295147ae2f03ef50484e517530b88",
    CLOSED / "FINAL_MANIFEST.sha256": "429371c829f37109afb425cd48f9b6266045c640e8349cb96063692f42a28d6a",
    CLOSED / "results_referee.json": "68033149d757c699a36309aea03c02055305fcc2b3a38f7d7d4089d259ab35eb",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path: Path, value: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


for path, digest in PINS.items():
    assert path.is_file() and sha(path) == digest, (path, sha(path), digest)
referee = json.loads((REFEREE / "results_referee.json").read_text())
closed = json.loads((CLOSED / "results_referee.json").read_text())
assert referee["status"] == "PASS_EXACT_FOUR_STRATUM_REDUCTION_REFEREE_ZERO_SOLVES"
assert referee["prior_57_comparison"]["resulting_global_chart_count"] == 60
assert closed["status"] == "PASS_UNIT_IDEAL_EXACT_Q_CLOSED_T_CHART_ONLY"
assert closed["single_chart_closes_group16"] is False

source_by_name = {
    "Dt1": "rep2_group016_67_Dt1_Q.sing",
    "Vt1_Dt2": "rep2_group016_67_Vt1_Dt2_Q.sing",
    "Vt1_Vt2_Dt0": "rep2_group016_67_Vt1_Vt2_Dt0_Q.sing",
}
strata = {row["name"]: row for row in referee["t_cover"]["strata"]}
epilogue = '''ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
'''
lanes = []
for ordinal, name in enumerate(sorted(source_by_name, key=lambda x: (strata[x]["variables"], x)), 1):
    source_name = source_by_name[name]
    design_source = DESIGN / source_name
    assert sha(design_source) == strata[name]["source_sha256"]
    text = design_source.read_text()
    assert text.count("quit;\n") == 1
    assert "ideal G=slimgb(I);" not in text
    runtime = text[: -len("quit;\n")] + epilogue
    target = HERE / "sources" / source_name.replace("_Q.sing", "_runtime_Q.sing")
    target.write_text(runtime)
    assert runtime.count("ideal G=slimgb(I);") == 1
    lanes.append(
        {
            "ordinal": ordinal,
            "name": name,
            "logical_stratum": referee["t_cover"]["partition"][
                ["Dt1", "Vt1_Dt2", "Vt1_Vt2_Dt0", "Vt0_Vt1_Vt2"].index(name)
            ],
            "design_source": str(design_source.relative_to(ROOT)),
            "design_source_sha256": sha(design_source),
            "source_path": str(target.relative_to(HERE)),
            "source_sha256": sha(target),
            "source_bytes": target.stat().st_size,
            "variables": strata[name]["variables"],
            "generators": strata[name]["generators"],
        }
    )

ledger = {
    "schema": "KRENN_X5_REP2_GROUP16_TCOVER_COMPLEMENT3_EXACT_Q_LEDGER_V1",
    "status": "PASS_MATERIALIZED_THREE_COMPLEMENTARY_CHARTS_ZERO_RUNS",
    "closed_stratum": "V(t0,t1,t2)",
    "closed_stratum_exact_q_manifest_sha256": PINS[CLOSED / "FINAL_MANIFEST.sha256"],
    "partition": referee["t_cover"]["partition"],
    "lanes": lanes,
    "cover_implication": "the prior V(A67,A12) intersect D(b0) chart is closed iff these three charts and the already closed V(t0,t1,t2) chart are unit",
    "single_chart_closes_group16": False,
    "solver_runs": 0,
}
atomic(HERE / "source_ledger.json", ledger)
print(json.dumps({"status": ledger["status"], "lanes": len(lanes), "shapes": [[x["variables"], x["generators"]] for x in lanes]}, sort_keys=True))
