#!/usr/bin/env python3
"""Independent, small-file referee for the rep4 all-162 promotion."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROMOTION = ROOT / "computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-2026-08-26"
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-conditional-design-2026-08-26"
DESIGN_REF = ROOT / "computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-conditional-design-referee-2026-08-26"
CENSUS_PATH = ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26/canonical_census.json"

EXPECTED = {
    PROMOTION / "results_promotion.json": "424689d9a7ca6c5c9a70b6365d0c0a4e2176adb07d5b671b8537569fd07fbcec",
    PROMOTION / "FINAL_MANIFEST.sha256": "91a23cc3e90a45fe0bfc40efd661ce9639ddd84f51e6da411fc2a18ad3e14993",
    DESIGN / "results_terminal_promotion_design.json": "ced7906cb327337ec86b0a87738c955d7542fb58652ea0885409754a9915ca39",
    DESIGN / "MANIFEST.sha256": "933016a415b1bf3b1d1ec851514461184097b25ed578f1a5e83488ffc075b237",
    DESIGN_REF / "results_referee.json": "de0940fafa13cd517e248038fd614879f7355a84119491e813ffffd2442506ed",
    DESIGN_REF / "FINAL_MANIFEST.sha256": "17260b24984a7e6a8fa91556bfe43c544f645ba586ed61480e7274ac6080b211",
    CENSUS_PATH: "12773aacfd9fa702ce4202a5da64c356d0451be8b904ebcf9848bcbf99913261",
}

BATCHES = [
    ("first25", "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26", "429d12d4135cc4cbe136481a6cd75fd5f254e4b646cfe3142b3dbe2f2f043b1d", "c2d13bbcf896321715c17353dd9970198eb3bce944e01b36dff24f9d3c5893fd", list(range(1, 26))),
    ("groups26_75", "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26", "76cbf6f8ec9759cfb8f3ba7abc7d27b5e2aa13b24fce0201a6e17299fcd318e1", "611d09abe73ef7032abf6280af3d9428e64d08db6aa731d1fde67ea004322e13", list(range(26, 76))),
    ("groups76_125", "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-terminal-referee-2026-08-26", "a579852ac80f4fe77001f0dc61da2d42804b1188d2cf0c5badb4583cbca000a8", "71ec7e0d92710f224ccc676358faf9f7024cee1e74cd578577614279ecc1ee14", list(range(76, 126))),
    ("groups126_161", "computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-terminal-referee-v2-2026-08-26", "e88ecfed7a51cf65e7d3c74428cd392a996253ef29825fb8928e66dca025c60c", "f1c2252c1852bcfca24223745539fc252e344bf11b2ee846270959006c980272", list(range(126, 162))),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(path: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        digest, name = line.split(None, 1)
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        entry = name.strip()
        local_target = (path.parent / entry).resolve()
        root_target = (ROOT / entry).resolve()
        target = local_target if local_target.is_file() else root_target
        assert target.is_file(), target
        assert sha(target) == digest, target
        count += 1
    return count


for path, digest in EXPECTED.items():
    assert path.is_file() and sha(path) == digest, path

manifest_replays = {
    "promotion": replay(PROMOTION / "FINAL_MANIFEST.sha256"),
    "design": replay(DESIGN / "MANIFEST.sha256"),
    "design_referee": replay(DESIGN_REF / "FINAL_MANIFEST.sha256"),
}

design = json.loads((DESIGN / "results_terminal_promotion_design.json").read_text())
design_ref = json.loads((DESIGN_REF / "results_referee.json").read_text())
promotion = json.loads((PROMOTION / "results_promotion.json").read_text())

# Replay every dependency manifest pinned by the conditional design and check
# every non-manifest pin byte-for-byte.  This is independent of promote.py's
# shorter six-manifest replay.
nested_manifest_replays: dict[str, int] = {}
for relative, digest in design["pins"].items():
    path = ROOT / relative
    assert path.is_file() and sha(path) == digest, path
    if path.name.endswith("MANIFEST.sha256"):
        nested_manifest_replays[relative] = replay(path)

batch_results = []
closed = [0]
for name, relative, manifest_hash, result_hash, expected_groups in BATCHES:
    directory = ROOT / relative
    manifest = directory / "FINAL_MANIFEST.sha256"
    result_path = directory / "results_referee.json"
    assert sha(manifest) == manifest_hash
    assert sha(result_path) == result_hash
    manifest_replays[name] = replay(manifest)
    result = json.loads(result_path.read_text())
    groups = result.get("unit_groups_closed", result.get("groups_closed"))
    assert groups == expected_groups
    assert result["status"].startswith("PASS")
    closed.extend(groups)
    batch_results.append({"name": name, "result_sha256": result_hash, "groups": groups})

assert closed == list(range(162))
assert len(closed) == len(set(closed)) == 162

# Regenerate the authoritative orbit census from its raw member lists rather
# than accepting the summary counters.
census = json.loads(CENSUS_PATH.read_text())
groups = census["groups"]
assert [record["group_id"] for record in groups] == list(range(162))
assert all(record["raw_member_count"] == len(record["raw_members"]) == 6 for record in groups)
assert all(record["canonical_chart"] in record["raw_members"] for record in groups)
raw_members = [tuple(member) for record in groups for member in record["raw_members"]]
assert len(raw_members) == len(set(raw_members)) == 972
families = {family: sum(record["family"] == family for record in groups) for family in ("y", "z")}
raw_families = {family: sum(member[4] == family for member in raw_members) for family in ("y", "z")}
assert families == {"y": 81, "z": 81}
assert raw_families == {"y": 486, "z": 486}
assert len({record["exact_Q_source_sha256"] for record in groups}) == 162

contract = design_ref["authoritative_contraction"]
assert contract == {
    "canonical_groups": 162,
    "forward_reverse_localization": True,
    "generators_each": 6577,
    "members_per_group": 6,
    "raw_charts": 972,
    "variables_each": 91,
    "y_groups": 81,
    "y_raw": 486,
    "z_groups": 81,
    "z_raw": 486,
}

rank0 = design_ref["rank_zero_clause"]
assert rank0["scope"] == [0]
assert rank0["outside_pair"] == "47"
assert rank0["nonzero_rank_claims_used"] is False
assert rank0["carrier_implication"] == "A47=0 forces A46=0 by the third guard equation; then L67=0 and nonzero A67 makes cap67/triangle012 active."

assert promotion["status"] == "PASS_REP4_ALL_162_CANONICAL_972_RAW_CHARTS"
assert promotion["representative"] == 4
assert promotion["canonical_groups_closed"] == list(range(162))
assert promotion["canonical_group_count"] == 162 and promotion["raw_charts_closed"] == 972
assert promotion["rank_zero_structural_clause"] == rank0
assert promotion["rep4_closed"] is True
assert promotion["cross_representative_promotion"] is False
assert promotion["full_conjecture_closed"] is False
assert promotion["new_solver_runs"] == 0

result = {
    "schema": "KRENN_X5_REP4_ALL162_TERMINAL_PROMOTION_INDEPENDENT_REFEREE_V1",
    "status": "PASS_REP4_ALL162_PROMOTION_EXACT_SCOPE",
    "producer": {
        "result_sha256": EXPECTED[PROMOTION / "results_promotion.json"],
        "manifest_sha256": EXPECTED[PROMOTION / "FINAL_MANIFEST.sha256"],
    },
    "dependency_replay": {
        "direct_manifest_counts": manifest_replays,
        "nested_manifest_counts": nested_manifest_replays,
        "all_pins_rehashed": len(design["pins"]),
    },
    "orbit_census": {
        "canonical_groups": len(groups),
        "raw_members": len(raw_members),
        "members_each": 6,
        "canonical_families": families,
        "raw_families": raw_families,
        "forward_reverse_localization": True,
    },
    "closed_union": closed,
    "batch_results": batch_results,
    "rank_zero_scope": rank0,
    "scope": {
        "representative": 4,
        "rep4_closed": True,
        "rank0_group_ids": [0],
        "nonzero_groups_closed_by_exact_q": list(range(1, 162)),
        "cross_representative_promotion": False,
        "full_conjecture_closed": False,
        "solver_runs": 0,
    },
}

temporary = HERE / "results_referee.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_referee.json")
print(json.dumps({"status": result["status"], "canonical": 162, "raw": 972}, sort_keys=True))
