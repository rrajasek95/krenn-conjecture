#!/usr/bin/env python3
"""Independent zero-run referee for the conditional rep5 torus-smallest Q lane."""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PKG = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-exact-q-conditional-held-2026-08-26"
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26"
DREF = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26"
MOD = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-modular-held-2026-08-26"
MREF = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-modular-held-referee-2026-08-26"
TIMEOUT = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(manifest: Path) -> int:
    seen: set[Path] = set()
    for raw in manifest.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw)
        assert match, (manifest, raw)
        digest, relative = match.groups()
        assert not relative.startswith("/")
        local = (manifest.parent / relative).resolve(strict=True)
        assert ROOT == local or ROOT in local.parents
        assert local not in seen
        seen.add(local)
        assert local.is_file() and sha(local) == digest, (local, sha(local), digest)
    return len(seen)


PINS = {
    PKG / "MANIFEST.sha256": "c96e75382cddb667f96a68d18b6a3e231614059c47ef0cd712eb372175ade686",
    PKG / "rep5_k2_t1_torus_smallest_Q_base.sing": "13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0",
    PKG / "rep5_k2_t1_torus_smallest_Q.sing": "4c788634af62bf0a98a2e8ddc2ab337baca292081ecc48f955c3622b87aff637",
    PKG / "run_one_lane.py": "e44b4168a689c0d08ea591a93312ade4955b18925fdd76e9ede3be9fea7165dd",
    PKG / "future_dependency_contract.json": "abcb8c058926d10bb7ecb711ca41441e72cfb9853239a1e20e6cf7ae82abe2fe",
    PKG / "results_validation.json": "90f471b3aa62f2750917bc441d12d57fe5f6f50e01610348f6f37dcfbdaea38c",
    PKG / "results_hostiles.json": "15ffebf88cb5e1752fd68433b4285d0aea587666d3060ae70a514cff6d8b1f91",
    DESIGN / "MANIFEST.sha256": "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e",
    DESIGN / "results_design.json": "9a42d532e2b007001d0411e470867fc31195ceb67d39633dd1a6da9bee83d916",
    DREF / "MANIFEST.sha256": "20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff",
    DREF / "results_referee.json": "5accedda0a7d8b5061a46dbf7b4a5988993802afffb4123e2996e639f0b3ef99",
    MOD / "MANIFEST.sha256": "21df0017be41a8ec9e4035b0902649cf9c8ed97d43c65c88a93d1db7f8bf6d72",
    MREF / "MANIFEST.sha256": "16a32d07221def48a9e8388ca1e8b716cd71dfb44c2dc0cbea0bb22ab91203ab",
    MREF / "results_referee.json": "b08a77edc8ed12c53df9673baabc33650afab7c8c1a80d8bf55324488b40223d",
    TIMEOUT / "FINAL_MANIFEST.sha256": "0cb2ba3080ddda143ac01e4fd9f8714876c070ee86e7e574415c22cae4cac4ff",
    TIMEOUT / "results_referee.json": "e41849050e8486c061970cd342b68d4b6d6855b606548d4ca09d456f61f59d7a",
}
for path, digest in PINS.items():
    assert path.is_file() and sha(path) == digest, (path, sha(path), digest)
manifest_counts = {
    "producer": replay(PKG / "MANIFEST.sha256"),
    "torus_design": replay(DESIGN / "MANIFEST.sha256"),
    "torus_referee": replay(DREF / "MANIFEST.sha256"),
    "modular_held": replay(MOD / "MANIFEST.sha256"),
    "modular_held_referee": replay(MREF / "MANIFEST.sha256"),
    "prior_timeout_referee": replay(TIMEOUT / "FINAL_MANIFEST.sha256"),
}

# The selected Q body is literally the independently audited member of the exact 16-chart cover.
design = json.loads((DESIGN / "results_design.json").read_text())
dref = json.loads((DREF / "results_referee.json").read_text())
assert design["status"] == "PASS_EXACT_16_CHART_73_VARIABLE_COVER_ZERO_SOLVES"
assert dref["status"] == "PASS_EXACT_16_CHART_TORUS_COVER_REFEREE_ZERO_SOLVES"
assignment = {"t0": 1, "t2": 0, "yn1": 1, "yn2": 1}
selected = [x for x in dref["residual_cover"]["sources"] if x["assignment"] == assignment]
assert len(selected) == 1 and selected[0] == {
    "assignment": assignment,
    "path": "sources/rep5_k2_t1_gauge_yn11_yn21_t01_t20_Q_design.sing",
    "removed_identifiers_absent": True,
    "sha256": PINS[PKG / "rep5_k2_t1_torus_smallest_Q_base.sing"],
}
design_source = DESIGN / selected[0]["path"]
base = PKG / "rep5_k2_t1_torus_smallest_Q_base.sing"
runtime = PKG / "rep5_k2_t1_torus_smallest_Q.sing"
assert design_source.read_bytes() == base.read_bytes()

# The runtime source differs only by the strong, proof-producing transcript epilogue.
base_bytes = base.read_bytes()
runtime_bytes = runtime.read_bytes()
old = b'print("INPUT_GENERATORS="+string(size(I)));\nquit;\n'
strong = (
    b'print("INPUT_GENERATORS="+string(size(I)));\n'
    b"ideal G=slimgb(I);\n"
    b'print("GROEBNER_SIZE="+string(size(G)));\n'
    b"poly remainder=reduce(1,G);\n"
    b'print("UNIT_REMAINDER="+string(remainder));\n'
    b'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\n'
    b"quit;\n"
)
assert base_bytes.count(old) == 1 and runtime_bytes == base_bytes.replace(old, strong, 1)
source_text = runtime_bytes.decode()
ring = re.search(r"ring r=0,\(([^\n]+)\),dp;", source_text)
assert ring and len(ring.group(1).split(",")) == 73
ideal_body = source_text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
assert ideal_body.count(",\n") + 1 == 6561
assert source_text.count("quit;") == 1

plan = json.loads((PKG / "held_plan.json").read_text())
contract = json.loads((PKG / "future_dependency_contract.json").read_text())
validation = json.loads((PKG / "results_validation.json").read_text())
pack_hostiles = json.loads((PKG / "results_hostiles.json").read_text())
mref = json.loads((MREF / "results_referee.json").read_text())
timeout = json.loads((TIMEOUT / "results_referee.json").read_text())
assert mref["status"] == "PASS_APPROVED_HELD_ZERO_RUN" and mref["selected_Q_sha256"] == sha(base)
assert mref["modular_source_sha256"] == contract["required_modular_source_sha256"]
assert timeout["status"] == "PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE"
assert timeout["attempt_consumed"] is True and timeout["mathematical_coverage"] is False
assert timeout["automatic_relaunch"] is False and plan["scope"]["prior_timeout_reused"] is False
assert plan["pins"] == {
    "modular_held_manifest_sha256": sha(MOD / "MANIFEST.sha256"),
    "modular_held_referee_manifest_sha256": sha(MREF / "MANIFEST.sha256"),
    "prior_timeout_referee_manifest_sha256": sha(TIMEOUT / "FINAL_MANIFEST.sha256"),
    "torus_producer_manifest_sha256": sha(DESIGN / "MANIFEST.sha256"),
    "torus_referee_manifest_sha256": sha(DREF / "MANIFEST.sha256"),
}
assert validation["status"] == "PASS_ZERO_RUN_FAIL_CLOSED"
assert plan["scope"] == {"attempts": 0, "mathematical_coverage": False, "other_charts": 0, "prior_timeout_reused": False, "solver_runs": 0}

# Future prerequisite and every execution authority remain deliberately absent.
assert contract["status"] == "HELD_FUTURE_HASHES_NULL_AND_BINDING_ABSENT"
assert set(contract["future_hashes"].values()) == {None}
assert set(contract["future_paths"].values()) == {None}
absent = (
    "future_modular_unit_dependency.json", "independent_referee_acceptance.json", "launch_clearance.json",
    "ATTEMPT.json", "result.json", "result.json.tmp", "RUN_EXCLUSIVE.lock", "stdout.log", "stderr.log", "watchdog.json",
)
for name in absent:
    assert not (PKG / name).exists(), name
assert not list(PKG.glob("*.tmp")) and not list(PKG.rglob("__pycache__"))

# Independently reconstruct the package's 16 fail-closed interface tests.
spec = importlib.util.spec_from_file_location("future_dependency", PKG / "verify_future_dependency.py")
assert spec and spec.loader
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
zero = "0" * 64
valid_shape = {
    "schema": "KRENN_X5_REP5_TORUS_SMALLEST_FUTURE_MODULAR_UNIT_DEPENDENCY_V1",
    "status": "INDEPENDENTLY_SEALED_SAME_CHART_MODULAR_UNIT",
    "held_manifest_sha256": sha(MOD / "MANIFEST.sha256"),
    "held_referee_manifest_sha256": sha(MREF / "MANIFEST.sha256"),
    "producer_manifest_path": "future/producer/MANIFEST.sha256", "producer_manifest_sha256": zero,
    "producer_result_path": "future/producer/result.json", "producer_result_sha256": zero,
    "referee_manifest_path": "future/referee/FINAL_MANIFEST.sha256", "referee_manifest_sha256": zero,
    "referee_result_path": "future/referee/results_referee.json", "referee_result_sha256": zero,
    "modular_source_sha256": contract["required_modular_source_sha256"],
    "field": "F_32003", "assignment": assignment, "variables": 73, "generators": 6561,
}
verifier.validate_shape(valid_shape)
hostiles: dict[str, bool] = {}
for key, wrong in (
    ("status", "PASS"), ("held_manifest_sha256", zero), ("held_referee_manifest_sha256", zero),
    ("modular_source_sha256", zero), ("field", "Q"), ("assignment", {"yn1": 0, "yn2": 1, "t0": 1, "t2": 0}),
    ("variables", 74), ("generators", 6562), ("producer_manifest_sha256", None), ("referee_result_sha256", "bad"),
):
    hostile = copy.deepcopy(valid_shape)
    hostile[key] = wrong
    try:
        verifier.validate_shape(hostile)
    except (AssertionError, KeyError, TypeError):
        hostiles[key] = True
    else:
        hostiles[key] = False
missing = copy.deepcopy(valid_shape)
del missing["producer_result_path"]
try:
    verifier.validate_shape(missing)
except (AssertionError, KeyError, TypeError):
    hostiles["missing"] = True
else:
    hostiles["missing"] = False
extra = copy.deepcopy(valid_shape)
extra["extra"] = True
try:
    verifier.validate_shape(extra)
except (AssertionError, KeyError, TypeError):
    hostiles["extra"] = True
else:
    hostiles["extra"] = False
hostiles.update({
    "binding_absent": not (PKG / absent[0]).exists(),
    "acceptance_absent": not (PKG / absent[1]).exists(),
    "clearance_absent": not (PKG / absent[2]).exists(),
})
attempt = subprocess.run(
    [sys.executable, str(PKG / "run_one_lane.py")], cwd=PKG, capture_output=True, text=True,
    timeout=15, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
)
hostiles["runner_refuses_before_attempt"] = (
    attempt.returncode != 0 and "future modular UNIT seal" in attempt.stderr and
    not (PKG / "ATTEMPT.json").exists() and not (PKG / "RUN_EXCLUSIVE.lock").exists()
)
assert len(hostiles) == 16 and all(hostiles.values()), hostiles
assert pack_hostiles == {
    "hostile_count": 16,
    "runner_refused_before_attempt": True,
    "schema": "KRENN_X5_REP5_TORUS_SMALLEST_SAME_CHART_EXACT_Q_HOSTILES_V1",
    "solver_runs": 0,
    "status": "PASS",
}

# Static runner audit: single Popen, hardened group observer, atomic result, exact resource geometry.
runner_text = (PKG / "run_one_lane.py").read_text()
ast.parse(runner_text)
for token in (
    "NATIVE_WALL = 480", "WRAPPER_WALL = 510", "RSS_CAP = 8 * 1024**3",
    "proc_listallpids", "proc_pidpath", "proc_listpgrppids", "proc_pid_rusage",
    "start_new_session=True", 'exclusive_json(HERE / "RUN_EXCLUSIVE.lock"',
    'exclusive_json(HERE / "ATTEMPT.json"', 'atomic_json(HERE / "result.json"',
):
    assert token in runner_text, token
assert runner_text.count("subprocess.Popen(") == 1
assert plan["execution"] == {
    "atomic_single_result": True, "direct_libproc_group_rss": True, "fresh_libproc_process_census": True,
    "maximum_lane_count": 1, "native_wall_seconds": 480, "rss_cap_bytes": 8589934592,
    "strict_stop_after_any_outcome": True, "wrapper_wall_seconds": 510,
}
assert plan["authorization"] == {
    "automatic_relaunch_authorized": False, "exact_Q_authorized": False, "fresh_clearance_present": False,
    "future_modular_unit_binding_present": False, "independent_acceptance_present": False, "other_chart_authorized": False,
}

result = {
    "schema": "KRENN_X5_REP5_TORUS_SMALLEST_SAME_CHART_EXACT_Q_CONDITIONAL_HELD_REFEREE_V1",
    "status": "PASS_HELD_ONLY_PENDING_INDEPENDENT_MODULAR_UNIT",
    "producer_manifest_sha256": sha(PKG / "MANIFEST.sha256"),
    "source": {
        "assignment": assignment, "base_Q_sha256": sha(base), "runtime_Q_sha256": sha(runtime),
        "identity_to_torus_cover_member": True, "sole_strong_transcript_append": True,
        "variables": 73, "generators": 6561,
    },
    "dependency": {
        "future_hashes_null": 4, "future_paths_null": 4, "binding_absent": True,
        "required_modular_source_sha256": contract["required_modular_source_sha256"],
        "independently_sealed_same_chart_modular_unit_required": True,
    },
    "provenance": {
        "torus_design_manifest_sha256": sha(DESIGN / "MANIFEST.sha256"),
        "torus_referee_manifest_sha256": sha(DREF / "MANIFEST.sha256"),
        "modular_held_manifest_sha256": sha(MOD / "MANIFEST.sha256"),
        "modular_held_referee_manifest_sha256": sha(MREF / "MANIFEST.sha256"),
        "prior_timeout_referee_manifest_sha256": sha(TIMEOUT / "FINAL_MANIFEST.sha256"),
        "prior_timeout_reused": False,
    },
    "runner": {
        "native_wall_seconds": 480, "wrapper_wall_seconds": 510, "rss_cap_bytes": 8589934592,
        "maximum_lane_count": 1, "hardened_direct_libproc": True, "atomic": True, "stop_any": True,
    },
    "hostile_tests": hostiles,
    "hostiles_passed": 16,
    "manifest_counts": manifest_counts,
    "scope": {
        "held_approval_only": True, "exact_Q_authorized": False, "launch_authorized": False,
        "mathematical_coverage": False, "rep5_closed": False, "solver_runs": 0,
        "other_chart_authorized": False, "automatic_relaunch_authorized": False,
    },
}
temporary = HERE / "results_referee.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_referee.json")
print(json.dumps({"status": result["status"], "hostiles": 16, "solver_runs": 0}, sort_keys=True))
