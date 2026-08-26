#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep1-group15-direct-libproc-held-runner-2026-08-25"
ATT = PROD / "attempt_group15"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

expected = {
    PROD / "HELD_RUNNER_MANIFEST.sha256": "4a378a50b8fc0cad4b6c078f31988923c783d2ea1bbf04afce41c2bdc8309924",
    PROD / "rep1_group15_Q.sing": "1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04",
    PROD / "run_group15_direct_libproc.py": "c539f6f47e824a536271a3e4700a5d2b86408c39c0850602e37db14bbad748d4",
    ATT / "rep1_group15_Q.sing": "1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04",
    ATT / "preflight.json": "7b633a24bf19c9b553a008014f26fe77ba47ce7228fbbce088b917a7df275a71",
    ATT / "stdout.log": "5a900740eb82dcf02edea777207e560fffe1e9b631c62c95018b0a2d0f4fd946",
    ATT / "stderr.log": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ATT / "watchdog.json": "716b087a9afc178cbee36063505affc9631050e04cfe08cde01d56c1bb02ad98",
    ATT / "result.json": "fc54aef1f58c39863a09e35e45d441363e82443b32538813d931da3e12bff1e3",
}
for path, digest in expected.items():
    assert path.is_file() and sha(path) == digest, (path, sha(path) if path.exists() else None)

assert sorted(p.name for p in PROD.glob("attempt*")) == ["attempt_group15"]
assert not list(PROD.rglob("*.tmp"))
pre = json.loads((ATT / "preflight.json").read_text())
wd = json.loads((ATT / "watchdog.json").read_text())
res = json.loads((ATT / "result.json").read_text())
clearance = json.loads((PROD / "FRESH_CLEARANCE.json").read_text())
assert pre["census"]["pass"] and pre["census"]["matches"] == []
assert pre["clearance_sha256"] == sha(PROD / "FRESH_CLEARANCE.json") == res["clearance_sha256"]
assert clearance["held_runner_manifest_sha256"] == sha(PROD / "HELD_RUNNER_MANIFEST.sha256")
assert clearance["expires_unix_seconds"] - clearance["issued_unix_seconds"] == 600
assert wd["status"] == "PASS" and wd["returncode"] == 0 and wd["breach"] is None
assert wd["native_wall_seconds"] == 240 and wd["wrapper_wall_seconds"] == 250
assert wd["rss_limit_kib"] == 8 * 1024 * 1024 and wd["peak_rss_kib"] == 675840
assert wd["elapsed_seconds"] == 41.258946 and wd["logs_atomic"]
assert wd["automatic_relaunch"] is False and wd["second_lane"] is False
assert wd["stdout_sha256"] == expected[ATT / "stdout.log"]
assert wd["stderr_sha256"] == expected[ATT / "stderr.log"]
parsed = {line.split("=",1)[0]: line.split("=",1)[1] for line in (ATT / "stdout.log").read_text().splitlines()}
assert parsed == {"INPUT_GENERATORS":"6577", "GROEBNER_SIZE":"1", "UNIT_REMAINDER":"0", "STATUS":"UNIT_IDEAL"}
assert res["status"] == "UNIT_IDEAL_EXACT_Q_GROUP15" and res["unit_ideal"] and res["group_closed"]
assert res["group_id"] == 15 and res["field"] == "Q" and res["returncode"] == 0 and res["breach"] is None
assert res["source_bytes"] == 1841468 and res["source_sha256"] == expected[ATT / "rep1_group15_Q.sing"]
assert res["automatic_relaunch"] is False and res["second_lane"] is False and res["group17_or_group25"] is False
assert res["representative_1_closed"] is False
source = (ATT / "rep1_group15_Q.sing").read_text()
assert "ring r=0," in source and source.count("ideal G=slimgb(I);") == 1 and source.rstrip().endswith("quit;")

out = {
  "schema": "KRENN_X5_REP1_GROUP15_EXACT_Q_TERMINAL_REFEREE_V1",
  "status": "PASS_UNIT_IDEAL_EXACT_Q_GROUP15_ONLY",
  "producer_result_sha256": expected[ATT / "result.json"],
  "source_sha256": expected[ATT / "rep1_group15_Q.sing"],
  "input_variables": 91,
  "input_generators": 6577,
  "groebner_basis_size": 1,
  "unit_remainder": 0,
  "elapsed_seconds": wd["elapsed_seconds"],
  "peak_rss_kib": wd["peak_rss_kib"],
  "resource_contract": "PASS_240_250_8GIB",
  "preflight_no_overlap": True,
  "atomic_no_tmp": True,
  "only_attempt": "attempt_group15",
  "automatic_relaunch": False,
  "other_groups_run": False,
  "scope": "group15 only; closed refined orbits are 0,13,15 (3/162); representative 1 remains open",
  "resource_clear": True
}
path = Path(__file__).with_name("results_referee.json")
payload = json.dumps(out, indent=2, sort_keys=True) + "\n"
assert path.read_text() == payload
print(json.dumps({"status": out["status"], "result_sha256": hashlib.sha256(payload.encode()).hexdigest()}))
