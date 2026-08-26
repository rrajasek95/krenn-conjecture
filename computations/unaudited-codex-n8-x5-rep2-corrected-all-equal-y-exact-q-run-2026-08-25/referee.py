#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ATT = HERE / "attempt_exact_q"
REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-modular-terminal-referee-2026-08-25"
DES = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""): h.update(block)
    return h.hexdigest()

def replay(path, base):
    for line in path.read_text().splitlines():
        digest, name = line.split(None, 1)
        target = Path(name.strip()); target = target if target.is_absolute() else base / target
        assert sha(target) == digest, (target, sha(target), digest)

assert sha(REF / "EXACT_Q_SAME_CHART_HELD_PLAN.json") == "f5f2942a59a810cacd369bc1d82cbafc663b579baf804148e488399ce95f9118"
assert sha(REF / "FINAL_MANIFEST.sha256") == "0409a7bccf9440470a6bc44f4a93b888f603509568c8a31055d8fb77eefbb84e"
replay(REF / "FINAL_MANIFEST.sha256", REF)
replay(HERE / "ATTEMPT_MANIFEST.sha256", HERE)

design = (DES / "rep2_corrected_guard_minor_tiny_y_Q.sing").read_text()
epilogue = "\n".join([
    "ideal G=slimgb(I);", 'print("GROEBNER_SIZE="+string(size(G)));',
    "poly remainder=reduce(1,G);", 'print("UNIT_REMAINDER="+string(remainder));',
    'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }', "quit;",
])
derived = design.replace("quit;", epilogue, 1).encode()
assert len(derived) == 1861246 and hashlib.sha256(derived).hexdigest() == "5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf"
assert (HERE / "rep2_corrected_all_equal_y_Q.sing").read_bytes() == derived
assert (ATT / "rep2_corrected_all_equal_y_Q.sing").read_bytes() == derived

pre = json.loads((ATT / "preflight.json").read_text())
assert pre["census"] == {"observer": "Darwin libproc", "matches": [], "pass": True}
wd = json.loads((ATT / "watchdog.json").read_text())
assert wd["status"] == "PASS" and wd["returncode"] == 0 and wd["breach"] is None
assert wd["native_wall_seconds"] == 480 and wd["wrapper_wall_seconds"] == 510 and wd["rss_limit_kib"] == 8388608
assert wd["elapsed_seconds"] == 6.891222 and wd["peak_rss_kib"] == 230588 and wd["logs_atomic"]
assert not wd["automatic_relaunch"] and not wd["second_lane"]
assert sha(ATT / "stderr.log") == hashlib.sha256(b"").hexdigest()
stdout = (ATT / "stdout.log").read_text().splitlines()
assert stdout == ["INPUT_VARIABLES=91", "INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"]
result = json.loads((ATT / "result.json").read_text())
assert result["status"] == "UNIT_IDEAL_EXACT_Q_REP2_SAME_CHART" and result["unit_ideal"] and result["same_chart_closed"]
assert not result["rep2_closed"] and not result["family_closed"] and not result["automatic_relaunch"] and not result["second_lane"]
assert result["parsed_stdout"] == {"INPUT_VARIABLES":"91", "INPUT_GENERATORS":"6577", "GROEBNER_SIZE":"1", "UNIT_REMAINDER":"0", "STATUS":"UNIT_IDEAL"}
assert not list(HERE.glob("attempt_exact_q_*")) and not list(HERE.glob("attempt2*"))

audit = {
    "schema": "KRENN_X5_REP2_SAME_CHART_EXACT_Q_INDEPENDENT_REFEREE_V1",
    "status": "PASS_EXACT_Q_ONE_REFINED_CHART_ONLY",
    "chart": "all-equal-y/i0/p00/x0/y0/d01",
    "variables": 91, "generators": 6577, "groebner_basis_size": 1, "unit_remainder": 0,
    "source_sha256": sha(HERE / "rep2_corrected_all_equal_y_Q.sing"),
    "attempt_result_sha256": sha(ATT / "result.json"), "watchdog_sha256": sha(ATT / "watchdog.json"),
    "elapsed_seconds": wd["elapsed_seconds"], "peak_rss_bytes": wd["peak_rss_kib"] * 1024,
    "second_lane_launched": False, "automatic_relaunch": False,
    "same_chart_closed": True, "rep2_closed": False, "seven_block_family_closed": False, "conjecture_closed": False,
}
(HERE / "results_independent_referee.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "audit_sha256": sha(HERE / "results_independent_referee.json")}, sort_keys=True))
