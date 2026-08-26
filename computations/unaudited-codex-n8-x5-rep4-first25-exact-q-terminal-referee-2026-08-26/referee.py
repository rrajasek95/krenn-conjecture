#!/usr/bin/env python3
"""Independent terminal replay of the rep4 first-25 exact-Q batch."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26"
HELD_REF = ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-referee-2026-08-26"
GROUP0 = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-held-plan-2026-08-25"
GROUP0_REF1 = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-terminal-referee-2026-08-25"
GROUP0_REF2 = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-terminal-second-referee-2026-08-25"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(manifest):
    count = 0
    for line in manifest.read_text().splitlines():
        digest, name = line.split(None, 1)
        path = Path(name.strip())
        path = path if path.is_absolute() else (manifest.parent / path).resolve()
        assert path.is_file() and sha(path) == digest, (path, digest)
        count += 1
    return count

assert sha(RUN / "MANIFEST.sha256") == "d6c098fb885ad9faac566b6f01a9e94f01aa6a8b4a61562ec4fa14f66b44a029"
replay(RUN / "MANIFEST.sha256")
assert sha(RUN / "run_first25.py") == "0f85a651c70da8582451987fd56801fb44bdb6c2c611361f4a399d1d1034809e"
assert sha(RUN / "source_ledger.json") == "59cbe8e6464be1774bbf9310cacae4ef4c9cf076f6185926716881b376718587"
assert sha(HELD_REF / "results_referee.json") == "62d4bcd4edcae051ee0637adf4f3e2d685730b34fc65a54ae92890db3d0edbc8"
assert sha(HELD_REF / "FINAL_MANIFEST.sha256") == "09f0c6fa97eaa0300ef41981ff9134331163236a6d869fc0e2fbb524ca0701ba"
replay(HELD_REF / "FINAL_MANIFEST.sha256")
assert sha(GROUP0 / "TERMINAL_MANIFEST.sha256") == "ff3178d7b546d4afadeeb8659001685d7d5bd3bb78c73b06b33ed539184e6d5d"
assert sha(GROUP0_REF1 / "FINAL_MANIFEST.sha256") == "a8280c98344eb62f6df89ffec125e6cdba33a7dae63f47061c71114f7aabe805"
assert sha(GROUP0_REF2 / "FINAL_MANIFEST.sha256") == "b2a543e59df1edf32df414f44938b418e35ea4ed258354642aff3d2b45e522b4"
replay(GROUP0 / "TERMINAL_MANIFEST.sha256")
replay(GROUP0_REF1 / "FINAL_MANIFEST.sha256")
replay(GROUP0_REF2 / "FINAL_MANIFEST.sha256")

assert replay(RUN / "TERMINAL_MANIFEST.sha256") == 29
assert sha(RUN / "TERMINAL_MANIFEST.sha256") == "8310384d0b26473fec57134cbb5f1b7c2c606e7b6a1af5dcefd5c5dfb3054260"
assert sha(RUN / "independent_referee_acceptance.json") == "fd7060dd619ad222be668c27aa53cc61d82e8c9f95356681e2ddfdb5a7c49f80"
assert sha(RUN / "launch_clearance.json") == "0ec48f69ec2160baf121afb83582cbbb05266b6c7dfbc13781f6c7f5a6c64fba"
acceptance = json.loads((RUN / "independent_referee_acceptance.json").read_text())
clearance = json.loads((RUN / "launch_clearance.json").read_text())
assert acceptance["already_closed_group_id"] == clearance["already_closed_group_id"] == 0
assert acceptance["first_referee_manifest_sha256"] == clearance["first_referee_manifest_sha256"] == sha(GROUP0_REF1 / "FINAL_MANIFEST.sha256")
assert acceptance["second_referee_manifest_sha256"] == clearance["second_referee_manifest_sha256"] == sha(GROUP0_REF2 / "FINAL_MANIFEST.sha256")
assert acceptance["selected_group_ids"] == clearance["selected_group_ids"] == list(range(1, 26))
assert acceptance["exact_Q_authorized"] is True
assert clearance["native_wall_seconds_each"] == 240 and clearance["wrapper_wall_seconds_each"] == 250
assert clearance["rss_cap_bytes_each"] == 8 * 1024**3 and clearance["no_overlap_confirmed"] is True
assert clearance["parallel_authorized"] is False and clearance["skip_reorder_relaunch_authorized"] is False

attempt = json.loads((RUN / "BATCH_ATTEMPT.json").read_text())
assert attempt["status"] == "CONSUMED_SINGLE_USE" and attempt["group_ids"] == list(range(1, 26))
assert attempt["acceptance_sha256"] == sha(RUN / "independent_referee_acceptance.json")
assert attempt["clearance_sha256"] == sha(RUN / "launch_clearance.json")
ledger = json.loads((RUN / "source_ledger.json").read_text())
lanes = ledger["lanes"]
assert [x["group_id"] for x in lanes] == list(range(1, 26))
assert [x["ordinal"] for x in lanes] == list(range(1, 26))
assert all(x["variables"] == 91 and x["generators"] == 6577 for x in lanes)

batch = json.loads((RUN / "batch_result.json").read_text())
assert batch["status"] == "PASS_ALL_25_UNIT"
assert batch["strict_order"] == list(range(1, 26))
assert batch["stop"] is None and batch["skipped_after_stop"] == []
assert batch["parallel"] is False and batch["relaunch"] is False
assert [x["group_id"] for x in batch["completed"]] == list(range(1, 26))

tail = ["INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL", "Auf Wiedersehen."]
walls = []
peaks = []
for gid, lane, item in zip(range(1, 26), lanes, batch["completed"]):
    path = RUN / f"results/group{gid:03d}.json"
    result = json.loads(path.read_text())
    assert item == {"group_id": gid, "status": "UNIT_IDEAL_EXACT_Q", "result_sha256": sha(path)}
    assert result["schema"] == "KRENN_X5_REP4_FIRST25_LANE_RESULT_V1"
    assert result["status"] == "UNIT_IDEAL_EXACT_Q" and result["group_id"] == gid and result["ordinal"] == gid
    assert result["chart"] == lane["canonical_chart"] and result["source_sha256"] == lane["source_sha256"]
    source = RUN / lane["source_path"]
    assert sha(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
    assert result["termination"] is None and result["returncode"] == 0 and result["stderr"] == ""
    assert result["stdout"].splitlines()[-5:] == tail
    assert result["automatic_relaunch"] is False
    assert result["wall_seconds"] < 240 and result["peak_group_rss_bytes"] < 8 * 1024**3
    walls.append(result["wall_seconds"])
    peaks.append(result["peak_group_rss_bytes"])

files = sorted((RUN / "results").glob("group*.json"))
assert len(files) == 25
assert [json.loads(path.read_text())["group_id"] for path in files] == list(range(1, 26))
assert not list(RUN.rglob("*.tmp"))

result = {
    "schema": "KRENN_X5_REP4_FIRST25_EXACT_Q_TERMINAL_REFEREE_V1",
    "status": "PASS_EXACT_GROUPS_1_25_UNIT",
    "sealed_group0": True,
    "unit_groups_closed": list(range(1, 26)),
    "closed_union": list(range(26)),
    "closed_count": 26,
    "rep4_total_groups": 162,
    "aggregate_wall_seconds": sum(walls),
    "maximum_wall_seconds": max(walls),
    "maximum_peak_rss_bytes": max(peaks),
    "batch_result_sha256": sha(RUN / "batch_result.json"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "strict_sequential": True,
    "parallel": False,
    "relaunch": False,
    "resource_clear": True,
    "rep4_closed": False,
    "conjecture_closed": False,
}
(HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
