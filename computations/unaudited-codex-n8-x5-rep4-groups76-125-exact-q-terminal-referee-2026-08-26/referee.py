#!/usr/bin/env python3
"""Independent terminal referee for strict rep4 groups76..125 exact-Q."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
C = ROOT / "computations"
RUN = C / "unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26"
HELD_REF = C / "unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-referee-2026-08-26"
COMPAT = C / "unaudited-codex-n8-x5-rep4-groups76-125-satisfied-dependency-binding-v3-compatible-2026-08-26"
IDS = list(range(76, 126))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(manifest: Path) -> int:
    count = 0
    seen: set[Path] = set()
    for raw in manifest.read_text().splitlines():
        digest, name = raw.split(None, 1)
        target = Path(name.strip())
        target = target if target.is_absolute() else (manifest.parent / target).resolve()
        assert target.is_file() and target not in seen and sha(target) == digest
        seen.add(target)
        count += 1
    return count


assert sha(RUN / "MANIFEST.sha256") == "0d2d7cfce0ed9e862b573e4fdc5791b3384c7bd21fbd6e9ff9e663c79f387115"
assert replay(RUN / "MANIFEST.sha256") == 70
assert sha(RUN / "run_groups76_125.py") == "3e5a744b6017dc0ba4a4d9789039bb4697d20fd1b42332195dc015cfd1e91abd"
assert sha(RUN / "source_ledger.json") == "b311e566fab04932f0c49a285ac3190ae4ac7a02f102799a9a2c6b34a949e4bb"
assert sha(HELD_REF / "results_referee.json") == "ce1105db2dedaa71bd7639df4cd758561500ad0430d9d2c55b12beaac40e928c"
assert sha(HELD_REF / "FINAL_MANIFEST.sha256") == "50e6f9aa6e7a5751c324393d7a158b63d535bd63999070fe46f85b5c7fb75118"
assert replay(HELD_REF / "FINAL_MANIFEST.sha256") == 15
assert sha(COMPAT / "results_compatibility.json") == "4ce9fbf5a321d79236b0c994c44c3805538bf62e5e4a0ef2143050fa4d0eafef"
assert sha(COMPAT / "results_referee.json") == "6bba5b6c0c512e46883c2ed4e159cf2b33a26888b59738e86283ad93159dd77b"
assert sha(COMPAT / "FINAL_MANIFEST.sha256") == "ccc4802efd390847c5bfe2f0194f4baf1903ebb57f0872472517afe48c311032"
assert replay(COMPAT / "FINAL_MANIFEST.sha256") == 21

assert (RUN / "normalized_dependencies.json").read_bytes() == (COMPAT / "normalized_dependencies.json").read_bytes()
assert (RUN / "independent_referee_acceptance.json").read_bytes() == (COMPAT / "independent_referee_acceptance.json").read_bytes()
assert sha(RUN / "normalized_dependencies.json") == "81147cd1397417119b1095ceae8da84f8e3f0bf0b4392a60c32206b2e739ee15"
assert sha(RUN / "independent_referee_acceptance.json") == "3026fa04d3638ca28c8ab1e36cbe7a4885878b20f246199d77099dec06a3362d"
assert sha(RUN / "launch_clearance.json") == "78d055014a84160786f21d5b8ab65bbbca533ca42c632ab4ba0c290f73cd27d7"

assert replay(RUN / "TERMINAL_MANIFEST.sha256") == 55
assert sha(RUN / "TERMINAL_MANIFEST.sha256") == "3e8624c75864fc4bf0bd34843a52b375089d570f172002fd3b550fb56cb4598a"
terminal_names = [line.split(None, 1)[1].strip() for line in (RUN / "TERMINAL_MANIFEST.sha256").read_text().splitlines()]
assert terminal_names[:5] == [
    "normalized_dependencies.json", "independent_referee_acceptance.json", "launch_clearance.json",
    "BATCH_ATTEMPT.json", "batch_result.json",
]
assert terminal_names[5:] == [f"results/group{gid:03d}.json" for gid in IDS]
assert len(terminal_names) == len(set(terminal_names)) == 55

dependency = json.loads((RUN / "normalized_dependencies.json").read_text())
acceptance = json.loads((RUN / "independent_referee_acceptance.json").read_text())
clearance = json.loads((RUN / "launch_clearance.json").read_text())
assert dependency["schema"] == "KRENN_X5_REP4_GROUPS76_125_NORMALIZED_DEPENDENCIES_V1"
assert dependency["closed_union"] == list(range(76))
assert dependency["duplicates"] == dependency["missing"] == dependency["extra"] == []
assert acceptance["required_closed_union"] == clearance["required_closed_union"] == list(range(76))
assert acceptance["selected_group_ids"] == clearance["selected_group_ids"] == IDS
assert acceptance["exact_Q_authorized"] is True and clearance["no_overlap_confirmed"] is True
assert (clearance["native_wall_seconds_each"], clearance["wrapper_wall_seconds_each"]) == (240, 250)
assert clearance["rss_cap_bytes_each"] == 8 * 1024**3
assert clearance["parallel_authorized"] is False and clearance["skip_reorder_relaunch_authorized"] is False

attempt = json.loads((RUN / "BATCH_ATTEMPT.json").read_text())
assert attempt["status"] == "CONSUMED_SINGLE_USE" and attempt["group_ids"] == IDS
assert attempt["dependencies_sha256"] == sha(RUN / "normalized_dependencies.json")
assert attempt["acceptance_sha256"] == sha(RUN / "independent_referee_acceptance.json")
assert attempt["clearance_sha256"] == sha(RUN / "launch_clearance.json")

ledger = json.loads((RUN / "source_ledger.json").read_text())
lanes = ledger["lanes"]
assert [lane["group_id"] for lane in lanes] == IDS
assert [lane["ordinal"] for lane in lanes] == list(range(1, 51))
assert all(lane["variables"] == 91 and lane["generators"] == 6577 for lane in lanes)

batch = json.loads((RUN / "batch_result.json").read_text())
assert sha(RUN / "batch_result.json") == "fd965d3e314b974fa031d2949075017fb9f1a76ea9bd15044861193b2fee034e"
assert batch["status"] == "PASS_ALL_50_UNIT" and batch["stop"] is None
assert batch["required_closed_union"] == list(range(76))
assert batch["strict_order"] == IDS and batch["skipped_after_stop"] == []
assert batch["parallel"] is False and batch["relaunch"] is False
assert len(batch["completed"]) == 50

tail = ["INPUT_VARIABLES=91", "INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL", "Auf Wiedersehen."]
walls: list[float] = []
peaks: list[int] = []
for ordinal, (gid, lane, item) in enumerate(zip(IDS, lanes, batch["completed"]), 1):
    path = RUN / f"results/group{gid:03d}.json"
    result = json.loads(path.read_text())
    assert item == {"group_id": gid, "status": "UNIT_IDEAL_EXACT_Q", "result_sha256": sha(path)}
    assert result["schema"] == "KRENN_X5_REP4_GROUPS76_125_LANE_RESULT_V1"
    assert result["group_id"] == gid and result["ordinal"] == ordinal
    assert result["chart"] == lane["canonical_chart"] and result["source_sha256"] == lane["source_sha256"]
    assert result["normalized_dependencies_sha256"] == sha(RUN / "normalized_dependencies.json")
    source = RUN / lane["source_path"]
    assert sha(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
    assert result["status"] == "UNIT_IDEAL_EXACT_Q" and result["termination"] is None
    assert result["returncode"] == 0 and result["stderr"] == ""
    assert result["stdout"].splitlines()[-6:] == tail
    assert result["automatic_relaunch"] is False
    assert result["wall_seconds"] < 240 and result["peak_group_rss_bytes"] < 8 * 1024**3
    walls.append(result["wall_seconds"])
    peaks.append(result["peak_group_rss_bytes"])

files = sorted((RUN / "results").glob("group*.json"))
assert len(files) == 50 and [json.loads(path.read_text())["group_id"] for path in files] == IDS
assert not list(RUN.rglob("*.tmp"))
assert not any((RUN / "results" / f"group{gid:03d}.json").exists() for gid in range(126, 162))

out = {
    "schema": "KRENN_X5_REP4_GROUPS76_125_EXACT_Q_TERMINAL_REFEREE_V1",
    "status": "PASS_ALL_50_EXACT_Q_UNIT_IDEALS",
    "groups_closed": IDS,
    "dependency_closed_union_before_batch": list(range(76)),
    "closed_union_after_batch": list(range(126)),
    "remaining_groups": list(range(126, 162)),
    "variables_each": 91, "generators_each": 6577,
    "groebner_basis_size_each": 1, "unit_remainder_each": 0,
    "aggregate_lane_wall_seconds": sum(walls),
    "maximum_lane_wall_seconds": max(walls),
    "maximum_peak_rss_bytes": max(peaks),
    "strict_order": True, "parallel": False, "relaunch": False, "skipped": False,
    "groups_beyond_125_launched": False,
    "new_groups_closed": 50, "rep4_closed_count": 126, "rep4_total_groups": 162,
    "rep4_representative_closed": False, "seven_block_family_closed": False, "conjecture_closed": False,
    "resource_clear": True,
    "batch_result_sha256": sha(RUN / "batch_result.json"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "held_referee_manifest_sha256": sha(HELD_REF / "FINAL_MANIFEST.sha256"),
    "compatible_binding_manifest_sha256": sha(COMPAT / "FINAL_MANIFEST.sha256"),
}
(HERE / "results_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
