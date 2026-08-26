#!/usr/bin/env python3
"""Independent terminal replay of the stopped rep2 first-25 batch."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25"
HELD_REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-referee-2026-08-26"
GROUP0 = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-run-2026-08-25"
GROUP0_REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-second-referee-2026-08-25"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(manifest):
    count = 0
    for line in manifest.read_text().splitlines():
        digest, name = line.split(None, 1)
        path = (manifest.parent / name.strip()).resolve()
        assert path.is_file() and sha(path) == digest, (path, digest)
        count += 1
    return count


assert sha(RUN / "MANIFEST.sha256") == "d694841e71b7982f50449b033ae21fb5798bd0ae765f75a9d655909a8c61022c"
replay(RUN / "MANIFEST.sha256")
assert sha(RUN / "run_first25.py") == "0727e5e5961f90cd14d3d79f836634bf7df9fff1b8d44bd463678db1f8f72ff2"
assert sha(RUN / "source_ledger.json") == "20737fd8197335f98214222bc5caa4c3d8c1ba2b2fcc283065d865befcf6389e"
assert sha(HELD_REF / "results_referee.json") == "0276814e2f1aa9f7f8a6c4b8cac0f76305ae241bb66576041c3deb58b28da2af"
assert sha(HELD_REF / "FINAL_MANIFEST.sha256") == "63052b073a025dae732102cb5efe5636aae3c9a5c16811d53440278f5879599a"
replay(HELD_REF / "FINAL_MANIFEST.sha256")
assert sha(GROUP0 / "FINAL_MANIFEST.sha256") == "c9298394d37022b384e8117280bfcdc39422ca24f57173da699a39dac11fb62a"
assert sha(GROUP0_REF / "FINAL_MANIFEST.sha256") == "c856fae641e355a94684c1c9304ead831d213ecc90f579c0a751c93002c10562"
replay(GROUP0 / "FINAL_MANIFEST.sha256")
replay(GROUP0_REF / "FINAL_MANIFEST.sha256")

terminal_entries = replay(RUN / "TERMINAL_MANIFEST.sha256")
assert terminal_entries == 20
assert sha(RUN / "independent_referee_acceptance.json") == "1cce5379045e082546710dca26b4f13c46ececa14b3de7d8eed8e569d6e6bff8"
assert sha(RUN / "launch_clearance.json") == "37030bfdcc8aa3e97369c9010d95943a8046f0e9b2259604e0bcbcf313000bba"
acceptance = json.loads((RUN / "independent_referee_acceptance.json").read_text())
clearance = json.loads((RUN / "launch_clearance.json").read_text())
assert acceptance["already_closed_group_id"] == clearance["already_closed_group_id"] == 0
assert acceptance["closed_manifest_sha256"] == clearance["closed_manifest_sha256"] == sha(GROUP0 / "FINAL_MANIFEST.sha256")
assert acceptance["closed_second_referee_manifest_sha256"] == clearance["closed_second_referee_manifest_sha256"] == sha(GROUP0_REF / "FINAL_MANIFEST.sha256")
assert acceptance["selected_group_ids"] == clearance["selected_group_ids"] == list(range(1, 26))
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
assert batch["status"] == "STOPPED_FAIL_CLOSED"
assert batch["strict_order"] == list(range(1, 26))
assert batch["stop"] == {"group_id": 16, "status": "FAIL_CLOSED_RESOURCE"}
assert batch["skipped_after_stop"] == list(range(17, 26))
assert batch["parallel"] is False and batch["relaunch"] is False
assert [x["group_id"] for x in batch["completed"]] == list(range(1, 17))

tail = [
    "INPUT_GENERATORS=6577",
    "GROEBNER_SIZE=1",
    "UNIT_REMAINDER=0",
    "STATUS=UNIT_IDEAL",
    "Auf Wiedersehen.",
]
walls = []
peaks = []
for gid, lane, item in zip(range(1, 16), lanes[:15], batch["completed"][:15]):
    path = RUN / f"results/group{gid:03d}.json"
    result = json.loads(path.read_text())
    assert item == {"group_id": gid, "status": "UNIT_IDEAL_EXACT_Q", "result_sha256": sha(path)}
    assert result["schema"] == "KRENN_X5_REP2_FIRST25_LANE_RESULT_V1"
    assert result["status"] == "UNIT_IDEAL_EXACT_Q" and result["group_id"] == gid and result["ordinal"] == gid
    assert result["chart"] == lane["canonical_chart"] and result["source_sha256"] == lane["source_sha256"]
    source = RUN / lane["source_path"]
    assert sha(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
    assert result["termination"] is None and result["wrapper_returncode"] == 0 and result["stderr"] == ""
    assert result["stdout"].splitlines()[-5:] == tail
    assert result["diagnostic_scope_one_group"] is True and result["automatic_relaunch"] is False
    assert result["wall_seconds"] < 240 and result["peak_group_rss_bytes"] < 8 * 1024**3
    walls.append(result["wall_seconds"])
    peaks.append(result["peak_group_rss_bytes"])

failure_path = RUN / "results/group016.json"
failure = json.loads(failure_path.read_text())
assert batch["completed"][15] == {"group_id": 16, "status": "FAIL_CLOSED_RESOURCE", "result_sha256": sha(failure_path)}
assert failure["schema"] == "KRENN_X5_REP2_FIRST25_LANE_RESULT_V1"
assert failure["status"] == "FAIL_CLOSED_RESOURCE" and failure["group_id"] == failure["ordinal"] == 16
assert failure["termination"] == "NATIVE_WALL_CAP_240"
assert 240 <= failure["wall_seconds"] < 250
assert failure["peak_group_rss_bytes"] < 8 * 1024**3
assert failure["stderr"] == "" and "INPUT_GENERATORS=6577" in failure["stdout"]
assert "GROEBNER_SIZE=" not in failure["stdout"] and "STATUS=UNIT_IDEAL" not in failure["stdout"]
assert failure["diagnostic_scope_one_group"] is True and failure["automatic_relaunch"] is False
assert sha(RUN / lanes[15]["source_path"]) == failure["source_sha256"] == lanes[15]["source_sha256"]

files = sorted((RUN / "results").glob("group*.json"))
assert len(files) == 16
assert [json.loads(path.read_text())["group_id"] for path in files] == list(range(1, 17))
assert all(not (RUN / f"results/group{gid:03d}.json").exists() for gid in range(17, 26))
assert not list(RUN.rglob("*.tmp"))

result = {
    "schema": "KRENN_X5_REP2_FIRST25_EXACT_Q_STOPPED_TERMINAL_REFEREE_V1",
    "status": "PASS_EXACT_PREFIX_1_15_GROUP16_NATIVE_WALL_STOP",
    "sealed_group0": True,
    "unit_groups_closed": list(range(1, 16)),
    "closed_union": list(range(16)),
    "closed_count": 16,
    "rep2_total_groups": 162,
    "failed_group_id": 16,
    "failed_group_coverage_added": False,
    "failure_classification": "NATIVE_WALL_CAP_240_ZERO_MATHEMATICAL_COVERAGE",
    "failure_wall_seconds": failure["wall_seconds"],
    "failure_peak_rss_bytes": failure["peak_group_rss_bytes"],
    "skipped_groups": list(range(17, 26)),
    "relaunch": False,
    "parallel": False,
    "aggregate_unit_wall_seconds": sum(walls),
    "maximum_unit_wall_seconds": max(walls),
    "maximum_unit_peak_rss_bytes": max(peaks),
    "batch_result_sha256": sha(RUN / "batch_result.json"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "rep2_closed": False,
    "conjecture_closed": False,
}
(HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
