#!/usr/bin/env python3
"""Choose and materialize one smallest rep5 open84 modular source; never solve."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-referee-2026-08-25"
PRIOR = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-pivot-k0-modular-terminal-referee-2026-08-25"
PINS = {
    PRODUCER / "MANIFEST.sha256": "50ed9510e2278f136cbfe28ee0df12a0139e6ef5ad6cfeda9d3b2a589aa16fe1",
    PRODUCER / "results_design_v2.json": "4d572fc359430eab8a55ee80ffe98993521e510f9eb48c37ab185742ad19bf00",
    REFEREE / "FINAL_MANIFEST.sha256": "3eef6a5bec2f260625189285cdaf171dbfa36530a1f67086528583e4f96db4c6",
    REFEREE / "results_referee.json": "c6216de12f0df50704a52695edf598d004ffb6d7307877e4f16b17ba20f0225a",
    PRIOR / "FINAL_MANIFEST.sha256": "a5dcd93bc79154bce1af90557c8496ca5aa38052f9e6b6206266e498c198e9cf",
    PRIOR / "results_referee.json": "37358baa478e6d220a19cdf955effab940c8b560bc93242e1ed52511c5db31c8",
}
PRIOR_Q_SHA = "d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1"
PRIOR_P_SHA = "dc04c72252144d1a8ff798f49aa1130b1742fff342f21eaf02146b889e3370c1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def generator_count(text: str) -> int:
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    depth = 0
    count = 1
    for character in body:
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            assert depth >= 0
        elif character == "," and depth == 0:
            count += 1
    assert depth == 0
    return count


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
producer = json.loads((PRODUCER / "results_design_v2.json").read_text())
referee = json.loads((REFEREE / "results_referee.json").read_text())
prior = json.loads((PRIOR / "results_referee.json").read_text())
assert producer["status"] == "PASS_SUPERSEDING_CORRECTED_NINE_STRATA_ZERO_SOLVES"
assert referee["status"] == "PASS_SUPERSEDING_LITERAL_SAFE_NINE_STRATA_DESIGN_ZERO_SOLVES"
assert prior["status"] == "PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE"
assert prior["attempt_consumed"] is True and prior["automatic_relaunch"] is False and prior["mathematical_coverage"] is False

candidates = []
for record in producer["sources"]:
    if record["rank_branch"] != "rank2_open":
        continue
    source = PRODUCER / record["path"]
    assert sha256(source) == record["sha256"] and source.stat().st_size == record["bytes"]
    text = source.read_text()
    generators = generator_count(text)
    assert generators == record["generators"] == 6562 and record["variables"] == 84
    # The exact lexical operator count is a deterministic factored-source term metric.
    operator_tokens = len(re.findall(r"[+*()-]", text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]))
    candidates.append({"pivot_k": record["pivot_k"], "t_open": record["t_open"], "path": record["path"], "source_sha256": record["sha256"], "bytes": record["bytes"], "generators": generators, "factored_operator_tokens": operator_tokens})
assert len(candidates) == 6
ordered = sorted(candidates, key=lambda item: (item["bytes"], item["generators"], item["factored_operator_tokens"], item["source_sha256"]))
selected = ordered[0]
assert len({(item["bytes"], item["generators"], item["factored_operator_tokens"]) for item in candidates}) == 1
assert (selected["pivot_k"], selected["t_open"], selected["source_sha256"]) == (2, 1, "1e2f72c9b4fda5e87fbec18469a6378cc7430f7b06676bd69db215055d8b1c7e")
assert selected["source_sha256"] != PRIOR_Q_SHA
q_source = PRODUCER / selected["path"]
q_text = q_source.read_text()
assert q_text.count("ring r=0,(") == 1 and "ring r=32003,(" not in q_text
for token in ("ideal G=slimgb(I);", "poly remainder=reduce(1,G);", 'print("GROEBNER_SIZE=', 'print("UNIT_REMAINDER=', "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED"):
    assert q_text.count(token) == 1, token
p_text = q_text.replace("ring r=0,(", "ring r=32003,(", 1)
assert p_text.replace("ring r=32003,(", "ring r=0,(", 1) == q_text
source_path = HERE / "rep5_rank2_k2_t1_p32003.sing"
atomic(source_path, p_text)
assert sha256(source_path) != PRIOR_P_SHA
result = {
    "schema": "KRENN_X5_REP5_RANK2_OPEN_SMALLEST_MODULAR_SOURCE_V1",
    "status": "PASS_DETERMINISTIC_SOURCE_DERIVATION_ZERO_RUN",
    "selection": {"ordered_key": ["source_bytes", "generator_count", "factored_operator_token_count", "source_sha256"], "all_six_tied_on_first_three_metrics": True, "candidates": candidates, "selected": selected},
    "derivation": {"Q_path": str(q_source.relative_to(ROOT)), "Q_sha256": sha256(q_source), "p_path": source_path.name, "p_sha256": sha256(source_path), "sole_change": "exactly one ring r=0,( token replaced by ring r=32003,(; solver/reduce/status epilogue byte-preserved", "reverse_byte_identity": True},
    "counts": {"variables": 84, "generators": 6562, "bytes_Q": len(q_text.encode()), "bytes_p": len(p_text.encode()), "factored_operator_tokens": selected["factored_operator_tokens"]},
    "prior_consumed_k0": {"terminal_manifest_sha256": PINS[PRIOR / "FINAL_MANIFEST.sha256"], "status": prior["status"], "attempt_consumed": True, "mathematical_coverage": False, "Q_sha256": PRIOR_Q_SHA, "p_sha256": PRIOR_P_SHA, "source_reused": False, "relaunch_authorized": False},
    "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    "scope": {"source_materialized": 1, "solver_runs": 0, "results": 0, "clearances": 0, "exact_Q_authorized": False, "other_strata_authorized": False, "automatic_relaunch_authorized": False, "mathematical_coverage": False},
}
atomic(HERE / "source_derivation.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "selected": [2, 1], "p_sha256": sha256(source_path), "solver_runs": 0}, sort_keys=True))
