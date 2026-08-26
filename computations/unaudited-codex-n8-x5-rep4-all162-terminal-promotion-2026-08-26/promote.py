#!/usr/bin/env python3
"""Promote the sealed rep4 batches through the authoritative 972-to-162 census."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-conditional-design-2026-08-26"
DESIGN_REF = ROOT / "computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-conditional-design-referee-2026-08-26"
BATCHES = [
    (ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26", "FINAL_MANIFEST.sha256", "results_referee.json"),
    (ROOT / "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26", "FINAL_MANIFEST.sha256", "results_referee.json"),
    (ROOT / "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-terminal-referee-2026-08-26", "FINAL_MANIFEST.sha256", "results_referee.json"),
    (ROOT / "computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-terminal-referee-v2-2026-08-26", "FINAL_MANIFEST.sha256", "results_referee.json"),
]
PINS = {
    DESIGN / "MANIFEST.sha256": "933016a415b1bf3b1d1ec851514461184097b25ed578f1a5e83488ffc075b237",
    DESIGN / "results_terminal_promotion_design.json": "ced7906cb327337ec86b0a87738c955d7542fb58652ea0885409754a9915ca39",
    DESIGN_REF / "FINAL_MANIFEST.sha256": "17260b24984a7e6a8fa91556bfe43c544f645ba586ed61480e7274ac6080b211",
    DESIGN_REF / "results_referee.json": "de0940fafa13cd517e248038fd614879f7355a84119491e813ffffd2442506ed",
    BATCHES[0][0] / BATCHES[0][1]: "429d12d4135cc4cbe136481a6cd75fd5f254e4b646cfe3142b3dbe2f2f043b1d",
    BATCHES[0][0] / BATCHES[0][2]: "c2d13bbcf896321715c17353dd9970198eb3bce944e01b36dff24f9d3c5893fd",
    BATCHES[1][0] / BATCHES[1][1]: "76cbf6f8ec9759cfb8f3ba7abc7d27b5e2aa13b24fce0201a6e17299fcd318e1",
    BATCHES[1][0] / BATCHES[1][2]: "611d09abe73ef7032abf6280af3d9428e64d08db6aa731d1fde67ea004322e13",
    BATCHES[2][0] / BATCHES[2][1]: "a579852ac80f4fe77001f0dc61da2d42804b1188d2cf0c5badb4583cbca000a8",
    BATCHES[2][0] / BATCHES[2][2]: "71ec7e0d92710f224ccc676358faf9f7024cee1e74cd578577614279ecc1ee14",
    BATCHES[3][0] / BATCHES[3][1]: "e88ecfed7a51cf65e7d3c74428cd392a996253ef29825fb8928e66dca025c60c",
    BATCHES[3][0] / BATCHES[3][2]: "f1c2252c1852bcfca24223745539fc252e344bf11b2ee846270959006c980272",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(path):
    count = 0
    for line in path.read_text().splitlines():
        digest, name = line.split(None, 1)
        target = (path.parent / name.strip()).resolve()
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert target.is_file() and sha(target) == digest
        count += 1
    return count


def atomic(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


for path, digest in PINS.items():
    assert path.is_file() and sha(path) == digest, (path, sha(path), digest)
manifest_counts = {
    "design": replay(DESIGN / "MANIFEST.sha256"),
    "design_referee": replay(DESIGN_REF / "FINAL_MANIFEST.sha256"),
}
for index, (directory, manifest_name, _) in enumerate(BATCHES):
    manifest_counts[f"batch_{index}"] = replay(directory / manifest_name)

design_ref = json.loads((DESIGN_REF / "results_referee.json").read_text())
assert design_ref["status"] == "PASS_DESIGN_ONLY_GROUP0_SEALED_FUTURE_1_161_REQUIRED"
census = design_ref["authoritative_contraction"]
assert census == {"canonical_groups": 162, "forward_reverse_localization": True, "generators_each": 6577, "members_per_group": 6, "raw_charts": 972, "variables_each": 91, "y_groups": 81, "y_raw": 486, "z_groups": 81, "z_raw": 486}
assert design_ref["sealed_group0"]["group_id"] == 0
assert design_ref["sealed_group0"]["independent_q_seals"] == 2
assert design_ref["sealed_group0"]["unit_remainder"] == 0
rank0 = design_ref["rank_zero_clause"]
assert rank0["scope"] == [0] and rank0["nonzero_rank_claims_used"] is False
assert "A47=0 forces A46=0" in rank0["carrier_implication"]

results = [json.loads((directory / result_name).read_text()) for directory, _, result_name in BATCHES]
assert results[0]["status"] == "PASS_EXACT_GROUPS_1_25_UNIT"
assert results[0]["unit_groups_closed"] == list(range(1, 26))
assert results[1]["status"] == "PASS_ALL_50_EXACT_Q_UNIT_IDEALS" and results[1]["groups_closed"] == list(range(26, 76))
assert results[2]["status"] == "PASS_ALL_50_EXACT_Q_UNIT_IDEALS" and results[2]["groups_closed"] == list(range(76, 126))
assert results[3]["status"] == "PASS_ALL_36_EXACT_Q_UNIT_IDEALS" and results[3]["groups_closed"] == list(range(126, 162))
closed = [0] + results[0]["unit_groups_closed"] + results[1]["groups_closed"] + results[2]["groups_closed"] + results[3]["groups_closed"]
assert closed == list(range(162)) and len(closed) == len(set(closed)) == 162
assert census["raw_charts"] == census["canonical_groups"] * census["members_per_group"]
assert census["y_raw"] + census["z_raw"] == census["raw_charts"]

out = {
    "schema": "KRENN_X5_REP4_ALL162_TERMINAL_PROMOTION_V1",
    "status": "PASS_REP4_ALL_162_CANONICAL_972_RAW_CHARTS",
    "representative": 4,
    "canonical_groups_closed": closed,
    "canonical_group_count": 162,
    "raw_charts_closed": 972,
    "members_per_group": 6,
    "y_groups": 81,
    "z_groups": 81,
    "forward_reverse_localization": True,
    "rank_zero_structural_clause": rank0,
    "batch_result_sha256": [sha(directory / result_name) for directory, _, result_name in BATCHES],
    "manifest_counts": manifest_counts,
    "rep4_closed": True,
    "cross_representative_promotion": False,
    "full_conjecture_closed": False,
    "new_solver_runs": 0,
}
atomic(HERE / "results_promotion.json", out)
print(json.dumps({"status": out["status"], "canonical": 162, "raw": 972}, sort_keys=True))
