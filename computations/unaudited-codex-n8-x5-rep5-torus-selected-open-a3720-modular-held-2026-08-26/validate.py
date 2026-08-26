#!/usr/bin/env python3
"""Fail-closed replay of the held package without invoking Singular."""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
Q = ROOT / "computations/unaudited-codex-n8-x5-rep5-torus-selected-further-reduction-design-2026-08-26/sources/stage0_a37_201_Q_design.sing"
P = H / "rep5_torus_selected_open_a37_201_p32003.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(Q) == "1e49c2b4127f1a185f50dbacbc63a51b97c210cb5dd9bd16a97f914c897fac1f"
assert sha(P) == "0fab67ef88a8674a161814094c6b553857e685ce311c5a42419812c71a939003"
assert sha(H / "source_derivation.json") == "3b14df5d70220330c768bcaefbaebbd5c679367badf3237604b9c2bb6d90a75e"
assert sha(H / "run_one_lane.py") == "2dfb2af4dfd6458692c564bec3da9104abde0af3f8ae5b885ba7b4e1dab0df6d"
q, p = Q.read_bytes(), P.read_bytes()
strong = b'''ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
'''
assert p.replace(b"ring r=32003,(", b"ring r=0,(", 1)[:-len(strong)] + b"quit;\n" == q
assert p.count(b"ring r=32003,(") == 1 and b"a37_20" not in p.split(b"ring r=32003,(", 1)[1].split(b"),dp;", 1)[0]
assert b'print("INPUT_VARIABLES="+string(nvars(r)));' in p and b'print("INPUT_GENERATORS="+string(size(I)));' in p
derivation = json.loads((H / "source_derivation.json").read_text())
held = json.loads((H / "held_pilot.json").read_text())
assert derivation["status"] == "PASS_SOLE_Q_TO_P_RING_PLUS_STRONG_EPILOGUE_ZERO_RUN"
assert derivation["input"]["sha256"] == sha(Q) and derivation["output"]["sha256"] == sha(P)
assert derivation["input"]["variables"] == derivation["output"]["variables"] == 72 and derivation["input"]["generators"] == derivation["output"]["generators"] == 6561
assert derivation["transformation"] == {"Q_body_otherwise_byte_identical": True, "inverse_byte_replay": True, "ring_replacements": 1, "strong_epilogue_appended": True}
assert derivation["scope"] == {"attempts": 0, "automatic_relaunch_authorized": False, "closed_branch_authorized": False, "exact_Q_authorized": False, "launch_authorized": False, "solver_runs": 0}
assert held["status"] == "HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE"
assert held["source"]["sha256"] == sha(P) and held["source"]["variables"] == 72 and held["source"]["generators"] == 6561
assert held["execution"] == {"atomic_result": True, "direct_libproc_group_rss": True, "exclusive_attempt_marker": True, "fresh_libproc_process_census": True, "maximum_lane_count": 1, "native_wall_seconds": 240, "rss_cap_bytes": 8589934592, "strict_stop_after_any_outcome": True, "wrapper_wall_seconds": 255}
assert held["authorization"] == {"automatic_relaunch_authorized": False, "closed_branch_authorized": False, "exact_Q_authorized": False, "fresh_clearance_present": False, "independent_acceptance_present": False}
assert held["scope"] == {"attempts": 0, "mathematical_coverage": False, "prior_timeout_reused": False, "rep5_closed": False, "results": 0, "solver_runs": 0}
assert not (H / "independent_referee_acceptance.json").exists() and not (H / "launch_clearance.json").exists()
for name in ("ATTEMPT.json", "result.json", "stdout.log", "stderr.log", "watchdog.json", "RUN_EXCLUSIVE.lock"):
    assert not (H / name).exists()
assert not list(H.glob("*.tmp")) and not list(H.rglob("__pycache__"))
runner = (H / "run_one_lane.py").read_text()
ast.parse(runner)
for literal in ("NATIVE = 240", "WRAPPER = 255", "RSS_CAP = 8 * 1024**3", "census()", "grouprss(process.pid)", 'exclusive(H / "ATTEMPT.json"', '"exact_Q_launched": False', '"closed_branch_launched": False', '"automatic_relaunch": False'):
    assert literal in runner, literal
for name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
    schema = json.loads((H / name).read_text())
    assert schema["additionalProperties"] is False and set(schema["required"]) == set(schema["properties"])
completed = subprocess.run([sys.executable, str(H / "hostile_tests.py")], cwd=H, env={"PYTHONDONTWRITEBYTECODE": "1"}, text=True, capture_output=True, timeout=10)
assert completed.returncode == 0, completed.stderr
hostiles = json.loads((H / "results_hostiles.json").read_text())
assert hostiles["status"] == "PASS_ALL_12_HOSTILES" and len(hostiles["tests"]) == 12 and hostiles["solver_runs"] == 0
if (H / "MANIFEST.sha256").exists():
    for line in (H / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (H / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest
print(json.dumps({"status": "PASS_REP5_OPEN_A3720_MODULAR_HELD_ZERO_RUN", "source": sha(P), "shape": [72, 6561], "hostiles": 12, "attempts": 0, "solver_runs": 0}, sort_keys=True))
