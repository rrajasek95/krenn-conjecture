#!/usr/bin/env python3
"""Read-only second referee for the sealed rep2 exact-Q one-chart run."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-run-2026-08-25"
ATT = RUN / "attempt_exact_q"

PINS = {
    RUN / "FINAL_MANIFEST.sha256": "c9298394d37022b384e8117280bfcdc39422ca24f57173da699a39dac11fb62a",
    RUN / "ATTEMPT_MANIFEST.sha256": "8c77bb11a6f39ca119e61cb7dfbd145a9cc3cc4d0627f9efcaa8d7d310f00ecb",
    RUN / "FRESH_CLEARANCE.json": "f1075be53078e7ecfe232798fcbc6862095b47920f459d8b325b94fed0e1b088",
    RUN / "run_exact_q.py": "b882a6e6f1473b665fd85f71d20e1758ecdd964da94cac4fdb3802da35bec2a2",
    RUN / "rep2_corrected_all_equal_y_Q.sing": "5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf",
    ATT / "preflight.json": "2d90ca20f27b8187cc937916f84d637ac1337f0b4cb70b0621fb5a2471552366",
    ATT / "rep2_corrected_all_equal_y_Q.sing": "5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf",
    ATT / "stdout.log": "8cb451abdbc87e04e229ff326723f30f9931e00465ecea39747cbe8af26b9526",
    ATT / "stderr.log": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ATT / "watchdog.json": "0a92a7c8288935109ab0c4d0ffe8f328c24fa718f7f46a32c92a7207d40d3aa6",
    ATT / "result.json": "043bb1fb15fec4291248c62036ed6594b34c8322207b93b6160c6c846c8d25a3",
    RUN / "results_independent_referee.json": "a3d3738b22c98c23ffaad2d5cd6c94b4ad9724acbcfeeebfbe4d89c98b39f39c",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def replay(path: Path, base: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, raw = line.split(None, 1)
        target = Path(raw.strip())
        if not target.is_absolute():
            target = base / target
        assert target.is_file() and sha(target) == digest, target
        count += 1
    return count


def top_level_count(body: str) -> int:
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


for path, expected in PINS.items():
    assert sha(path) == expected, (path, sha(path), expected)
final_entries = replay(RUN / "FINAL_MANIFEST.sha256", RUN)
attempt_entries = replay(RUN / "ATTEMPT_MANIFEST.sha256", RUN)
assert (RUN / "rep2_corrected_all_equal_y_Q.sing").read_bytes() == (ATT / "rep2_corrected_all_equal_y_Q.sing").read_bytes()
source = (ATT / "rep2_corrected_all_equal_y_Q.sing").read_text()
assert len(source.encode()) == 1861246
assert source.count("ring r=0,(") == 1 and "ring r=32003," not in source
ring_start = source.index("ring r=0,(") + len("ring r=0,(")
ring_end = source.index("),dp;", ring_start)
variables = [item.strip() for item in source[ring_start:ring_end].split(",")]
assert len(variables) == len(set(variables)) == 91
ideal_start = source.index("ideal I=") + len("ideal I=")
ideal_end = source.index(';\nprint("INPUT_VARIABLES=', ideal_start)
assert top_level_count(source[ideal_start:ideal_end]) == 6577
for token in ("ideal G=slimgb(I);", "poly remainder=reduce(1,G);", "STATUS=UNIT_IDEAL", "STATUS=NONUNIT_OR_UNRESOLVED", "quit;"):
    assert source.count(token) == 1

expected_stdout = (
    "INPUT_VARIABLES=91\nINPUT_GENERATORS=6577\nGROEBNER_SIZE=1\n"
    "UNIT_REMAINDER=0\nSTATUS=UNIT_IDEAL\n"
)
assert (ATT / "stdout.log").read_text() == expected_stdout
assert (ATT / "stderr.log").read_bytes() == b""
result = json.loads((ATT / "result.json").read_text())
watchdog = json.loads((ATT / "watchdog.json").read_text())
preflight = json.loads((ATT / "preflight.json").read_text())
clearance = json.loads((RUN / "FRESH_CLEARANCE.json").read_text())
assert preflight["census"] == {"matches": [], "observer": "Darwin libproc", "pass": True}
assert preflight["clearance_sha256"] == PINS[RUN / "FRESH_CLEARANCE.json"]
assert clearance["manager_clearance"] is clearance["resource_clearance"] is True
assert clearance["no_overlap_confirmed"] is clearance["launch_exactly_once"] is True
assert clearance["expires_unix_seconds"] - clearance["issued_unix_seconds"] == 600
assert result["status"] == "UNIT_IDEAL_EXACT_Q_REP2_SAME_CHART"
assert result["parsed_stdout"] == {
    "GROEBNER_SIZE": "1", "INPUT_GENERATORS": "6577", "INPUT_VARIABLES": "91",
    "STATUS": "UNIT_IDEAL", "UNIT_REMAINDER": "0",
}
assert result["unit_ideal"] is result["same_chart_closed"] is True
assert result["rep2_closed"] is result["family_closed"] is False
assert result["returncode"] == 0 and result["breach"] is None
assert result["automatic_relaunch"] is result["second_lane"] is False
assert result["preflight_sha256"] == PINS[ATT / "preflight.json"]
assert result["watchdog_sha256"] == PINS[ATT / "watchdog.json"]
assert watchdog["status"] == "PASS" and watchdog["returncode"] == 0 and watchdog["breach"] is None
assert watchdog["elapsed_seconds"] == 6.891222 and watchdog["peak_rss_kib"] == 230588
assert watchdog["native_wall_seconds"] == 480 and watchdog["wrapper_wall_seconds"] == 510
assert watchdog["rss_limit_kib"] == 8388608 and watchdog["logs_atomic"] is True
assert watchdog["automatic_relaunch"] is watchdog["second_lane"] is False
assert watchdog["stdout_sha256"] == PINS[ATT / "stdout.log"] and watchdog["stderr_sha256"] == PINS[ATT / "stderr.log"]
assert max(sample["rss_kib"] for sample in watchdog["samples"]) == 230588
assert all(sample["members"] in (1, 2) for sample in watchdog["samples"])
assert all(a["elapsed_seconds"] < b["elapsed_seconds"] for a, b in zip(watchdog["samples"], watchdog["samples"][1:]))
assert not list(RUN.rglob("*.tmp"))
attempt_dirs = [path for path in RUN.iterdir() if path.is_dir() and path.name.startswith("attempt")]
assert attempt_dirs == [ATT]

print(json.dumps({
    "status": "PASS_EXACT_Q_ONE_REFINED_REP2_CHART_ONLY",
    "source_sha256": sha(ATT / "rep2_corrected_all_equal_y_Q.sing"),
    "variables": len(variables), "generators": 6577,
    "groebner_basis_size": 1, "unit_remainder": 0,
    "elapsed_seconds": watchdog["elapsed_seconds"], "peak_rss_kib": watchdog["peak_rss_kib"],
    "attempt_manifest_entries": attempt_entries, "final_manifest_entries": final_entries,
}, sort_keys=True))
