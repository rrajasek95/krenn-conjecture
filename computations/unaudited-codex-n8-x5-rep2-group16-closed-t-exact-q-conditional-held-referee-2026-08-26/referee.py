#!/usr/bin/env python3
"""Independent zero-run referee for the rep2 group16 closed-t exact-Q gate."""
from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PKG = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-closed-t-exact-q-conditional-held-2026-08-26"
BASE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/rep2_group016_67_Vt0_Vt1_Vt2_Q.sing"
RUNTIME = PKG / "rep2_group016_62_Vt0_Vt1_Vt2_Q_strong.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(manifest: Path, required: Path) -> None:
    seen: set[Path] = set()
    for line in manifest.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        assert match, line
        digest, relative = match.groups()
        target = (manifest.parent / relative).resolve(strict=True)
        assert ROOT in target.parents and target not in seen
        assert sha(target) == digest
        seen.add(target)
    assert required.resolve() in seen


assert sha(PKG / "MANIFEST.sha256") == "122fd1c6ef07f9955d2b4e8f908478d05e45aa8a9b5d8505f2b8e44ba89ae771"
assert sha(BASE) == "43beb317cb0bc59b24f1d4c5613ef6baccd7ec064651e004c1f8eb4657d538fc"
assert sha(RUNTIME) == "53fc0b26c52c5f55505c101c72ed0a7a73159092667edde4cdf1c573e4bd6795"
assert sha(PKG / "modular_unit_dependency.json") == "1366ccf2f49d0f8c149f590d79ccbf810933de8496a44bcd857b5f26f385141c"
assert sha(PKG / "run_one_lane.py") == "0eeb4b6e56474a4ab451e6f5d006c00c1b0618e2cde14ab6bd152e7f3f8c5f92"

old = b'print("INPUT_GENERATORS="+string(size(I)));\nquit;\n'
strong = (
    b'print("INPUT_GENERATORS="+string(size(I)));\nideal G=slimgb(I);\n'
    b'print("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\n'
    b'print("UNIT_REMAINDER="+string(remainder));\n'
    b'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'
)
base = BASE.read_bytes()
runtime = RUNTIME.read_bytes()
assert base.count(old) == 1 and runtime.count(strong) == 1
assert runtime.replace(strong, old, 1) == base
ring_line = runtime.splitlines()[2].decode()
variables = ring_line.split("(", 1)[1].rsplit("),dp;", 1)[0].split(",")
assert len(variables) == 62
source_lines = runtime.splitlines()
assert source_lines[3].startswith(b"ideal I=")
assert len(source_lines[3:6571]) == 6568

dependency = json.loads((PKG / "modular_unit_dependency.json").read_text())
assert dependency["status"] == "INDEPENDENTLY_SEALED_SAME_CHART_MODULAR_UNIT"
assert (dependency["variables"], dependency["generators"]) == (62, 6568)
assert dependency["field"] == "F_32003"
assert dependency["chart"] == "V(A67,A12,t0,t1,t2) intersect D(b0)"
for manifest_key, result_key in (
    ("producer_terminal_manifest_path", "producer_result_path"),
    ("referee_terminal_manifest_path", "referee_result_path"),
):
    manifest = ROOT / dependency[manifest_key]
    result = ROOT / dependency[result_key]
    assert sha(manifest) == dependency[manifest_key.replace("_path", "_sha256")]
    assert sha(result) == dependency[result_key.replace("_path", "_sha256")]
    replay(manifest, result)

producer = json.loads((ROOT / dependency["producer_result_path"]).read_text())
assert producer["status"] == "UNIT_IDEAL_MODULAR_DIAGNOSTIC"
assert producer["termination"] is None and producer["returncode"] == 0
assert producer["source_sha256"] == dependency["modular_source_sha256"]
assert {"INPUT_VARIABLES=62", "INPUT_GENERATORS=6568", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"} <= set(producer["stdout"].splitlines())
modular_referee = json.loads((ROOT / dependency["referee_result_path"]).read_text())
assert modular_referee["status"] == "PASS_UNIT_IDEAL_MODULAR_DIAGNOSTIC_CHART_ONLY"
assert modular_referee["mathematical_coverage_promoted"] is False

runner = (PKG / "run_one_lane.py").read_text()
ast.parse(runner)
for token in (
    "NATIVE_WALL = 480", "WRAPPER_WALL = 510", "RSS_CAP = 8 * 1024**3",
    "proc_listallpids", "proc_pidpath", "proc_listpgrppids", "proc_pid_rusage",
    "exclusive_json(HERE / \"RUN_EXCLUSIVE.lock\"", "exclusive_json(HERE / \"ATTEMPT.json\"",
    '"automatic_relaunch": False', '"other_chart_launched": False',
):
    assert token in runner, token

hostiles = json.loads((PKG / "results_hostiles.json").read_text())
validation = json.loads((PKG / "results_validation.json").read_text())
assert hostiles["status"] == "PASS" and hostiles["hostile_count"] == 16 and hostiles["solver_runs"] == 0
assert len(hostiles["tests"]) == 16 and all(hostiles["tests"].values())
assert validation["status"] == "PASS_ZERO_RUN_MODULAR_UNIT_BOUND_FAIL_CLOSED"
assert validation["scope"]["attempts"] == validation["scope"]["solver_runs"] == 0
for absent in (
    "independent_referee_acceptance.json", "launch_clearance.json", "ATTEMPT.json", "result.json",
    "result.json.tmp", "RUN_EXCLUSIVE.lock", "stdout.log", "stderr.log", "watchdog.json",
):
    assert not (PKG / absent).exists(), absent
assert not list(PKG.glob("*.tmp"))

acceptance = json.loads((HERE / "independent_referee_acceptance.json").read_text())
assert acceptance == {
    "schema": "KRENN_X5_REP2_GROUP16_CLOSED_T_EXACT_Q_INDEPENDENT_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_ONE_CLOSED_T_EXACT_Q_ONLY",
    "held_manifest_sha256": sha(PKG / "MANIFEST.sha256"),
    "dependency_sha256": sha(PKG / "modular_unit_dependency.json"),
    "source_sha256": sha(RUNTIME),
    "runner_sha256": sha(PKG / "run_one_lane.py"),
    "variables": 62, "generators": 6568, "maximum_lane_count": 1,
    "exact_Q_authorized": True, "other_chart_authorized": False,
    "automatic_relaunch_authorized": False,
}

print(json.dumps({
    "status": "PASS_APPROVE_HELD_ONE_CLOSED_T_EXACT_Q_ZERO_RUNS",
    "source_sha256": sha(RUNTIME),
    "dependency_sha256": sha(PKG / "modular_unit_dependency.json"),
    "runner_sha256": sha(PKG / "run_one_lane.py"),
    "hostiles": 16,
}, sort_keys=True))
