#!/usr/bin/env python3
"""Independent static/result referee for rep1 canonical group 13 over Q."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep1-group13-exact-q-pilot-2026-08-25"
CENSUS = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
CENSUS_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25"
RECT = ROOT / "computations/unaudited-codex-n8-x5-rectangle-rank3-adjugate-ideal-referee-2026-08-25/modular_p32003_run"
OUT = HERE / "results_referee.json"
PLAN = HERE / "NEXT3_EXACT_Q_HELD_PLAN.json"

EXPECTED = {
    PROD / "MANIFEST.sha256": "4cf21dec8926b66934fecf998616a31bc06f990b35662a2c48a67d3343dcb5a8",
    PROD / "result.json": "66b92e09f73ec629cf09bd235000d64298d4d7987987b95d5f2be088d499e77b",
    PROD / "rep1_group13_Q.sing": "336bc28a4affecb31ce32fa468eadb1317efea5fb3ee2d5acbd24fc5f320790a",
    PROD / "run_group13.py": "733d257e93cc8d59ce4da62b5183a4cc9bda568f12c752d13f38c1988f41f69d",
    PROD / "clearance.json": "9432ae58b944d79620c5f9f359eef8a8b03a4b0977c7fdaeec590fbd70d7a37f",
    PROD / "RESOURCE_CLEAR.json": "e766106af4a9a30f39a3e0eee293773c726186e14798f68e45e24f5ec969ee8f",
    PROD / "RESOURCE_CLEAR_BINDING.json": "83d97fe4d4d68f51f0a99ee6cce7e6d74d095f8a4f8f006d950d5457d2bfecae",
    CENSUS / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    CENSUS / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    CENSUS_REF / "FINAL_MANIFEST.sha256": "f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a",
    RECT / "MANIFEST.sha256": "922604a9b3ae34f8fded694eb28a6d0c2736e463839bd7381740f0a9327742c4",
    RECT / "RESULT.json": "1c67f97a20ba88964b5f6d82d34eebc9cd221cb8ecda7e0c42f12d4e001dd346",
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def replay_manifest(path):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        assert sha(path.parent / rel.strip()) == digest, (path, rel)
        count += 1
    return count


def top_level_count(body):
    depth = 0
    count = 1 if body.strip() else 0
    for char in body:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            assert depth >= 0
        elif char == "," and depth == 0:
            count += 1
    assert depth == 0
    return count


for path, digest in EXPECTED.items():
    assert sha(path) == digest, (path, sha(path), digest)
manifest_entries = replay_manifest(PROD / "MANIFEST.sha256")

source = (PROD / "rep1_group13_Q.sing").read_text()
assert source.count("ring r=0,") == 1 and "ring r=32003," not in source
ring_start = source.index("ring r=0,(") + len("ring r=0,(")
ring_end = source.index("),dp;", ring_start)
variables = [x.strip() for x in source[ring_start:ring_end].split(",")]
assert len(variables) == len(set(variables)) == 91
ideal_start = source.index("ideal I=(") + len("ideal I=")
ideal_end = source.index(";\nprint(\"INPUT_GENERATORS=", ideal_start)
generators = top_level_count(source[ideal_start:ideal_end])
assert generators == 6577
assert source.count("ideal G=slimgb(I);") == 1
assert source.count("poly remainder=reduce(1,G);") == 1

census = json.loads((CENSUS / "results_canonical_census.json").read_text())
records = census["enumeration"]["records"]
record = records[13]
assert record["group_id"] == 13
assert record["canonical_chart"] == [0, 0, 0, 1, "z", 0, 0, 2]
assert record["exact_Q_source_sha256"] == EXPECTED[PROD / "rep1_group13_Q.sing"]
assert record["exact_Q_source_bytes"] == len(source.encode()) == 1841468

clearance = json.loads((PROD / "clearance.json").read_text())
resource = json.loads((PROD / "RESOURCE_CLEAR.json").read_text())
binding = json.loads((PROD / "RESOURCE_CLEAR_BINDING.json").read_text())
assert clearance["status"] == "SCOPE_CLEARED_BUT_RESOURCE_HOLD_ACTIVE"
assert clearance["group_id"] == 13 and clearance["maximum_lanes"] == 1
assert clearance["no_optional_microbatch"] is True and clearance["no_relaunch"] is True
assert resource == {"status": "EXPLICIT_RESOURCE_CLEAR", "group_id": 13, "no_overlap_confirmed": True}
assert binding["status"] == "RESOURCE_CLEAR_BOUND_TO_TERMINAL_SEAL"
assert binding["resource_clear_sha256"] == EXPECTED[PROD / "RESOURCE_CLEAR.json"]
assert binding["terminal_rectangle_manifest_sha256"] == EXPECTED[RECT / "MANIFEST.sha256"]
assert binding["terminal_rectangle_result_sha256"] == EXPECTED[RECT / "RESULT.json"]
assert binding["group_id"] == 13 and binding["no_overlap_confirmed"] is True

result = json.loads((PROD / "result.json").read_text())
assert result["schema"] == "KRENN_X5_REP1_GROUP13_EXACT_Q_PILOT_V1"
assert result["status"] == "UNIT_IDEAL_EXACT_Q_GROUP13"
assert result["group_id"] == 13 and result["chart"] == record["canonical_chart"]
assert result["field"] == "Q" and result["source_sha256"] == EXPECTED[PROD / "rep1_group13_Q.sing"]
assert result["source_bytes"] == 1841468
assert result["termination"] is None and result["returncode"] == 0 and result["stderr"] == ""
assert result["wall_seconds"] == 24.033887499943376
assert result["observed_peak_rss_bytes"] == 497045504
assert result["wall_seconds"] < result["native_wall_cap_seconds"] == 240
assert result["wrapper_wall_cap_seconds"] == 250
assert result["observed_peak_rss_bytes"] < result["rss_cap_bytes"] == 8 * 1024**3
for token in ("INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"):
    assert result["stdout"].count(token) == 1, token
assert result["group_closed"] is True and result["representative_closed"] is False
assert result["second_lane_launched"] is False
assert result["optional_microbatch_launched"] is False
assert result["automatic_relaunch"] is False
assert not list(PROD.glob("*.tmp"))

# The producer package is the only group-specific exact-Q package.  Thus no
# later three-lane batch or relaunch has landed under the frozen naming scope.
group_packages = sorted(
    p.name for p in (ROOT / "computations").glob("*rep1-group*-exact-q*")
    if p.resolve() != HERE.resolve()
)
assert group_packages == [PROD.name], group_packages

eligible = [r for r in records if r["group_id"] not in (0, 13)]
eligible.sort(key=lambda r: (-r["exact_Q_source_bytes"], r["group_id"]))
selected = eligible[:3]
assert [r["group_id"] for r in selected] == [15, 17, 25]
plan = json.loads(PLAN.read_text())
assert plan["status"] == "HELD_NOT_RUN_REQUIRES_EXPLICIT_CLEARANCE"
assert plan["launch_authorized"] is False
assert plan["selection_rule"] == "remaining maximum-source-size groups in canonical group-id order"
assert [lane["group_id"] for lane in plan["lanes"]] == [15, 17, 25]
for lane, expected in zip(plan["lanes"], selected):
    assert lane["canonical_chart"] == expected["canonical_chart"]
    assert lane["source_sha256"] == expected["exact_Q_source_sha256"]
    assert lane["source_bytes"] == expected["exact_Q_source_bytes"] == 1841468

audit = {
    "schema": "KRENN_X5_REP1_GROUP13_EXACT_Q_REFEREE_V1",
    "status": "PASS_EXACT_Q_UNIT_IDEAL_GROUP13_ONLY",
    "producer_manifest_sha256": EXPECTED[PROD / "MANIFEST.sha256"],
    "producer_result_sha256": EXPECTED[PROD / "result.json"],
    "source_Q_sha256": EXPECTED[PROD / "rep1_group13_Q.sing"],
    "manifest_entries_replayed": manifest_entries,
    "variables": len(variables),
    "input_generators": generators,
    "groebner_basis_size": 1,
    "unit_remainder": 0,
    "wall_seconds": result["wall_seconds"],
    "peak_rss_bytes": result["observed_peak_rss_bytes"],
    "clearance_and_resource_binding": "PASS",
    "atomic_no_tmp": True,
    "observed_later_three_lane_batch_or_relaunch": False,
    "closed_groups": [0, 13],
    "closed_group_count": 2,
    "total_group_count": 162,
    "representative_1_closed": False,
    "next3_held_plan_sha256": sha(PLAN),
    "next3_group_ids": [15, 17, 25],
    "no_singular_run_by_referee": True,
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "result_sha256": sha(OUT)}, sort_keys=True))
