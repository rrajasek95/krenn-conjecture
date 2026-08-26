#!/usr/bin/env python3
"""Independent result referee for the sole rank1/orbit0 modular pilot."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROD = ROOT / "computations/unaudited-codex-n8-x5-rectangle-rank1-orbit0-p32003-pilot-2026-08-25"
SUPER = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-rank1-orbit0-solver-source-supersession-2026-08-25"
OUT = HERE / "results_referee.json"
PLAN = HERE / "EXACT_Q_SAME_CHART_HELD_PLAN.json"
EXPECTED = {
    PROD / "MANIFEST.sha256": "6e7f7683a40b2dc1d81939d13b4079da732a0921aea16998caa50eaeb4989858",
    PROD / "result.json": "17e1ded6a6f42929f3ac8feb92874bc1c1b72725a57fecf3c8e84f23eac9df9a",
    PROD / "rank1_orbit0_p32003_execute.sing": "7c34d1efbf74220f01a6ea150ede232b9f51f9168f15dd997ed2b204e8aacf9c",
    PROD / "run_pilot.py": "bf92688cdf807776971834dcd3d3a84c90de738145edf3f618c09e7798640b19",
    PROD / "SUPERSEDING_RESOURCE_CLEAR.json": "dd1583583bb950484116113525a477595f99e3f5594093c206ed93b5e0e03edc",
    PROD / "LAUNCH_BINDING.json": "6b4ce0d85bf5387bc9900f3678af575cb3048299c2fe5f150637524f5e24520c",
    PROD / "RUN_PROVENANCE.json": "81cf32f3814ecb8c7c07ee29023addd31efd88aac7475e54e672e42a978c93b7",
    SUPER / "FINAL_MANIFEST.sha256": "304ec4a83b5ff1c09894e5e17d100b581b849de360b1cb3242bba3e653fe095b",
    SUPER / "SUPERSEDING_STAGED_HELD_PLAN.json": "3d7f1018e313ecae9eaa14f57bd07a4eb4243bb8009920dd76732c888c8ccd40",
}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(path):
    count = 0
    for line in path.read_text().splitlines():
        if line.strip():
            digest, rel = line.split(None, 1)
            assert sha(path.parent / rel.strip()) == digest
            count += 1
    return count


def top_count(body):
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


for path, digest in EXPECTED.items(): assert sha(path) == digest, (path, sha(path), digest)
entries = replay(PROD / "MANIFEST.sha256")
source = (PROD / "rank1_orbit0_p32003_execute.sing").read_text()
assert source.count("ring r=32003,") == 1 and "ring r=0," not in source
rs = source.index("ring r=32003,(") + len("ring r=32003,(")
re = source.index("),dp;", rs)
variables = source[rs:re].split(",")
assert len(variables) == len(set(variables)) == 76
gs = source.index("ideal I=(") + len("ideal I=")
ge = source.index(";\nprint(\"INPUT_VARIABLES=", gs)
assert top_count(source[gs:ge]) == 6571
for token in ("ideal G=slimgb(I);", "poly remainder=reduce(1,G);", "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED"):
    assert source.count(token) == 1
clear = json.loads((PROD / "SUPERSEDING_RESOURCE_CLEAR.json").read_text())
binding = json.loads((PROD / "LAUNCH_BINDING.json").read_text())
assert clear["status"] == binding["status"] == "EXPLICIT_SUPERSEDING_RESOURCE_CLEAR"
assert clear["execution_source_sha256"] == binding["execution_source_sha256"] == EXPECTED[PROD / "rank1_orbit0_p32003_execute.sing"]
assert clear["one_p32003_lane_only"] is True and clear["no_overlap_confirmed"] is True
assert binding["independent_manifest_sha256"] == EXPECTED[SUPER / "FINAL_MANIFEST.sha256"]
assert binding["superseding_plan_sha256"] == EXPECTED[SUPER / "SUPERSEDING_STAGED_HELD_PLAN.json"]
assert binding["runner_sha256"] == EXPECTED[PROD / "run_pilot.py"]
assert binding["process_census"] == "PASS_NO_HEAVY_SOLVER"
assert binding["one_modular_lane_only"] is True and binding["no_exact_Q_or_second_chart_or_relaunch"] is True
result = json.loads((PROD / "result.json").read_text())
assert result["status"] == "UNIT_IDEAL_P32003_RANK1_ORBIT0"
assert result["field"] == "F_32003" and result["rank"] == 1 and result["orbit"] == 0
assert result["chart"] == {"diagonal": 0, "I": [0], "J": [0]}
assert result["source_sha256"] == EXPECTED[PROD / "rank1_orbit0_p32003_execute.sing"]
assert result["source_bytes"] == 519401
assert result["returncode"] == 0 and result["termination"] is None and result["stderr"] == ""
assert result["wall_seconds"] == 14.562766416929662 and result["observed_peak_rss_bytes"] == 468594688
assert result["native_wall_cap_seconds"] == 180 and result["wrapper_wall_cap_seconds"] == 195
assert result["rss_cap_bytes"] == 8589934592
for token in ("INPUT_VARIABLES=76", "INPUT_GENERATORS=6571", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"):
    assert result["stdout"].count(token) == 1
assert result["orbit_closed_mod_p"] is True and result["exact_Q_closed"] is False
assert result["exact_Q_launched"] is result["second_lane_launched"] is result["automatic_relaunch"] is False
assert result["representative_closed"] is False
assert not list(PROD.glob("*.tmp"))
runner = (PROD / "run_pilot.py").read_text()
assert "atomic(HERE/\"result.json\"" in runner
assert runner.count("subprocess.Popen") == 1
provenance = json.loads((PROD / "RUN_PROVENANCE.json").read_text())
assert provenance["status"] == "TERMINAL_UNIT_IDEAL"
assert provenance["runner_sha256"] == EXPECTED[PROD / "run_pilot.py"]
assert provenance["scope"] == "One modular F_32003 rank1/orbit0 lane only; no exact-Q, second chart, or relaunch."
plan = json.loads(PLAN.read_text())
assert plan["status"] == "HELD_NOT_RUN_REQUIRES_EXPLICIT_CLEARANCE"
assert plan["launch_authorized"] is False
assert plan["source"]["expected_sha256"] == "c062396aa8835e9c31d0e845a997d89f3b1d151f6494d36d5ba990cdadf9c44f"
assert plan["modular_audit_prerequisite"] == "this referee result and final manifest must PASS"
audit = {
    "schema": "KRENN_X5_RECTANGLE_RANK1_ORBIT0_P32003_REFEREE_V1",
    "status": "PASS_MODULAR_UNIT_IDEAL_ORBIT0_ONLY",
    "producer_manifest_sha256": EXPECTED[PROD / "MANIFEST.sha256"],
    "producer_result_sha256": EXPECTED[PROD / "result.json"],
    "source_sha256": EXPECTED[PROD / "rank1_orbit0_p32003_execute.sing"],
    "runner_sha256": EXPECTED[PROD / "run_pilot.py"],
    "manifest_entries_replayed": entries,
    "counts": {"variables": 76, "generators": 6571, "groebner_basis_size": 1, "unit_remainder": 0},
    "wall_seconds": result["wall_seconds"], "peak_rss_bytes": result["observed_peak_rss_bytes"],
    "atomic_no_tmp": True, "exact_Q_second_relaunch": False,
    "scope": "rank1/orbit0 over F_32003 only; no characteristic-zero or family closure",
    "exact_Q_held_plan_sha256": sha(PLAN),
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "result_sha256": sha(OUT)}, sort_keys=True))
