#!/usr/bin/env python3
"""Independent static/result referee for the sole approved exact-Q rep1 lane."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROD = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-exact-q-2026-08-25"
QUOT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
PLAN = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-diagnostic-referee-2026-08-25/EXACT_Q_HELD_PLAN.json"
OUT = Path(__file__).resolve().parent / "results_referee.json"

EXPECTED = {
    PROD / "MANIFEST.sha256": "58c112efd1b889796337030bc08965c98195ef3b927bce257db82fe220e8d809",
    PROD / "result.json": "668c36e5e6248c369424787a919013c32cde6b7c0aaa35ae81b7100469e7aab9",
    PROD / "rep1_minor_i0_p00_x0_y0_d01_Q.sing": "53f741ca9173877ef1bc21dba2546a82102a32140221068de1301d0b4635dadb",
    QUOT / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing": "edd174ccbc75a563fd67e0515b6dde2c54e5469b742629953080290fe7d1fb49",
    PLAN: "a7841d169a1d07c43785eaf498b502f2aff54b4745646173756ab47ea74551fd",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_manifest(path):
    checked = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        target = path.parent / rel.strip()
        assert sha(target) == digest, (path, target)
        checked += 1
    return checked


def top_level_count(body):
    depth = 0
    count = 1 if body.strip() else 0
    for char in body:
        if char == "(": depth += 1
        elif char == ")":
            depth -= 1
            assert depth >= 0
        elif char == "," and depth == 0: count += 1
    assert depth == 0
    return count


for path, digest in EXPECTED.items():
    assert sha(path) == digest, (path, sha(path), digest)
manifest_entries = replay_manifest(PROD / "MANIFEST.sha256")
prelaunch_entries = replay_manifest(PROD / "PRELAUNCH_MANIFEST.sha256")

source_q = (PROD / "rep1_minor_i0_p00_x0_y0_d01_Q.sing").read_text()
source_p = (QUOT / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing").read_text()
assert source_p.count("ring r=32003,") == 1 and "ring r=0," not in source_p
assert source_q == source_p.replace("ring r=32003,", "ring r=0,", 1)
assert source_q.count("ring r=0,") == 1 and "ring r=32003," not in source_q

ring_start = source_q.index("ring r=0,(") + len("ring r=0,(")
ring_end = source_q.index("),dp;", ring_start)
variables = [x.strip() for x in source_q[ring_start:ring_end].split(",")]
assert len(variables) == len(set(variables)) == 91
ideal_start = source_q.index("ideal I=(") + len("ideal I=")
ideal_end = source_q.index(";\nprint(\"INPUT_GENERATORS=", ideal_start)
generators = top_level_count(source_q[ideal_start:ideal_end])
assert generators == 6577
assert source_q.count("ideal G=slimgb(I);") == 1
assert source_q.count("poly remainder=reduce(1,G);") == 1

plan = json.loads(PLAN.read_text())
clearance = json.loads((PROD / "clearance.json").read_text())
result = json.loads((PROD / "result.json").read_text())
assert plan["status"] == "APPROVE_HELD_NOT_RUN"
assert plan["limits"]["maximum_exact_Q_lane_count"] == 1
assert clearance["status"] == "EXPLICIT_MANAGER_CLEARANCE"
assert clearance["held_plan_sha256"] == EXPECTED[PLAN]
assert clearance["maximum_exact_q_lanes"] == 1
assert clearance["no_second_lane"] is True and clearance["no_relaunch"] is True
assert result["schema"] == "KRENN_X5_REP1_GUARD_MINOR_EXACT_Q_ONE_LANE_V1"
assert result["status"] == "UNIT_IDEAL_EXACT_Q_LOCALIZED_CHART"
assert result["field"] == "Q" and result["chart"] == "all-equal-y/i0/p00/x0/y0/d01"
assert result["source_Q_sha256"] == EXPECTED[PROD / "rep1_minor_i0_p00_x0_y0_d01_Q.sing"]
assert result["termination"] is None and result["returncode"] == 0 and result["stderr"] == ""
assert result["wall_seconds"] == 9.307639292092063
assert result["observed_peak_rss_bytes"] == 267988992
assert result["wall_seconds"] < 240 and result["observed_peak_rss_bytes"] < 8 * 1024**3
for token in ("INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"):
    assert result["stdout"].count(token) == 1, token
assert result["localized_chart_closed"] is True
assert result["representative_closed"] is False
assert result["second_lane_launched"] is False
assert result["modular_relaunch"] is False
assert result["automatic_relaunch"] is False

siblings = sorted(p.name for p in (ROOT / "computations").glob("*rep1-guard-minor-exact-q-2026-08-25"))
assert siblings == [PROD.name]

audit = {
    "schema": "KRENN_X5_REP1_GUARD_MINOR_EXACT_Q_ONE_LANE_REFEREE_V1",
    "status": "PASS_EXACT_Q_UNIT_IDEAL_ONE_REFINED_ORBIT_ONLY",
    "producer_manifest_sha256": EXPECTED[PROD / "MANIFEST.sha256"],
    "producer_result_sha256": EXPECTED[PROD / "result.json"],
    "source_Q_sha256": EXPECTED[PROD / "rep1_minor_i0_p00_x0_y0_d01_Q.sing"],
    "source_derivation": "byte-identical to pinned p32003 source after its unique ring token is changed to r=0",
    "manifest_entries_replayed": manifest_entries,
    "prelaunch_entries_replayed": prelaunch_entries,
    "variables": 91,
    "input_generators": generators,
    "groebner_basis_size": 1,
    "unit_remainder": 0,
    "wall_seconds": result["wall_seconds"],
    "peak_rss_bytes": result["observed_peak_rss_bytes"],
    "approved_exact_q_lane_count": 1,
    "observed_second_lane_or_relaunch": False,
    "scope": {
        "localized_chart": "all-equal-y/i0/p00/x0/y0/d01",
        "localized_chart_closed": True,
        "refined_orbits_closed": 1,
        "refined_orbits_total": 162,
        "representative_1_closed": False,
        "seven_block_family_closed": False,
    },
    "no_singular_rerun_by_referee": True,
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "result_sha256": sha(OUT)}, sort_keys=True))
