#!/usr/bin/env python3
"""Independent terminal referee for strict rep4 groups 26..75."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26"
HELD_REF = ROOT / "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-referee-2026-08-26"
BIND = ROOT / "computations/unaudited-codex-n8-x5-rep4-groups26-75-satisfied-dependency-binding-v2-2026-08-26"
DEP = ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26"
IDS = list(range(26, 76))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(manifest):
    count = 0
    for raw in manifest.read_text().splitlines():
        digest, name = raw.split(None, 1)
        target = Path(name.strip())
        target = target if target.is_absolute() else (manifest.parent / target).resolve()
        assert target.is_file() and sha(target) == digest, (target, digest)
        count += 1
    return count

assert sha(RUN / "MANIFEST.sha256") == "c79cf415a4dc6327dcaefa7f9f002a1f1f2b5af5afef2a80bab16d8cfc9ccbb6"
replay(RUN / "MANIFEST.sha256")
assert sha(RUN / "run_groups26_75.py") == "b29a78c495517ddb9c43147c5c9ec1091c921a63e4a8285cf7549d0926d721aa"
assert sha(RUN / "source_ledger.json") == "48e9fb104efd69a1267f5ff1015a2142af33d481a430bebab2f794442afa8341"
assert sha(HELD_REF / "results_referee.json") == "6b2d15c8c0b27ef3e6d931bcba44b3471691baad913230cb03a9c6993b6587e4"
assert sha(HELD_REF / "FINAL_MANIFEST.sha256") == "55d13a229ecf359351e8f66a36fae944d14889f4212866eaafa25c83c151962c"
replay(HELD_REF / "FINAL_MANIFEST.sha256")
assert sha(BIND / "results_binding.json") == "fb2ac032afdb3a031862e47e173569a01a10f83966b0c4c313c0252749201f76"
assert sha(BIND / "results_referee.json") == "c99d16f728168c6736df6336b72eba79ba78bd7856cffb22ff5f951e8f8de243"
assert sha(BIND / "normalized_dependency.json") == "694b48641949b7dd971a7dce4ec269fc8d912a20e23b936176f5c46fccd6842e"
assert sha(BIND / "independent_referee_acceptance.json") == "57d56d89878809b2b47a07c36c5525fdfbcee5b58bdee3650c495fac0385bfee"
assert sha(BIND / "FINAL_MANIFEST.sha256") == "99a22438dcd1e0f7caf0a3dd30f3b35180bafda297acdfa3f4734567dee582c2"
replay(BIND / "FINAL_MANIFEST.sha256")
assert sha(DEP / "results_referee.json") == "c2d13bbcf896321715c17353dd9970198eb3bce944e01b36dff24f9d3c5893fd"
assert sha(DEP / "FINAL_MANIFEST.sha256") == "429d12d4135cc4cbe136481a6cd75fd5f254e4b646cfe3142b3dbe2f2f043b1d"
replay(DEP / "FINAL_MANIFEST.sha256")
assert (RUN / "normalized_dependency.json").read_bytes() == (BIND / "normalized_dependency.json").read_bytes()
assert (RUN / "independent_referee_acceptance.json").read_bytes() == (BIND / "independent_referee_acceptance.json").read_bytes()

assert replay(RUN / "TERMINAL_MANIFEST.sha256") == 55
assert sha(RUN / "TERMINAL_MANIFEST.sha256") == "b8ba01dcfb43cdf92244fe85703c5423a9186c6d44c73a73df2ea694f585ff98"
terminal_names = [line.split(None, 1)[1].strip() for line in (RUN / "TERMINAL_MANIFEST.sha256").read_text().splitlines()]
assert terminal_names[:5] == ["normalized_dependency.json", "independent_referee_acceptance.json", "launch_clearance.json", "BATCH_ATTEMPT.json", "batch_result.json"]
assert terminal_names[5:] == [f"results/group{gid:03d}.json" for gid in IDS]
assert len(set(terminal_names)) == 55
assert sha(RUN / "independent_referee_acceptance.json") == "57d56d89878809b2b47a07c36c5525fdfbcee5b58bdee3650c495fac0385bfee"
assert sha(RUN / "launch_clearance.json") == "935854d5a57b57b26b0e7b08624a9b18f4aae0a11b57d4b627667110e67965a2"
acceptance = json.loads((RUN / "independent_referee_acceptance.json").read_text())
clearance = json.loads((RUN / "launch_clearance.json").read_text())
assert acceptance["required_closed_union"] == clearance["required_closed_union"] == list(range(26))
assert acceptance["selected_group_ids"] == clearance["selected_group_ids"] == IDS
assert acceptance["exact_Q_authorized"] is True and clearance["no_overlap_confirmed"] is True
assert clearance["native_wall_seconds_each"] == 240 and clearance["wrapper_wall_seconds_each"] == 250
assert clearance["rss_cap_bytes_each"] == 8 * 1024**3
assert clearance["parallel_authorized"] is False and clearance["skip_reorder_relaunch_authorized"] is False

attempt = json.loads((RUN / "BATCH_ATTEMPT.json").read_text())
assert attempt["status"] == "CONSUMED_SINGLE_USE" and attempt["group_ids"] == IDS
assert attempt["dependency_sha256"] == sha(RUN / "normalized_dependency.json")
assert attempt["acceptance_sha256"] == sha(RUN / "independent_referee_acceptance.json")
assert attempt["clearance_sha256"] == sha(RUN / "launch_clearance.json")
ledger = json.loads((RUN / "source_ledger.json").read_text())
lanes = ledger["lanes"]
assert [x["group_id"] for x in lanes] == IDS
assert [x["ordinal"] for x in lanes] == list(range(1, 51))
assert all(x["variables"] == 91 and x["generators"] == 6577 for x in lanes)

batch = json.loads((RUN / "batch_result.json").read_text())
assert batch["status"] == "PASS_ALL_50_UNIT" and batch["stop"] is None
assert batch["required_closed_union"] == list(range(26))
assert batch["strict_order"] == IDS and batch["skipped_after_stop"] == []
assert batch["parallel"] is False and batch["relaunch"] is False
assert len(batch["completed"]) == 50

tail = ["INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL", "Auf Wiedersehen."]
walls = []
peaks = []
for ordinal, (gid, lane, item) in enumerate(zip(IDS, lanes, batch["completed"]), 1):
    path = RUN / f"results/group{gid:03d}.json"
    result = json.loads(path.read_text())
    assert item == {"group_id": gid, "status": "UNIT_IDEAL_EXACT_Q", "result_sha256": sha(path)}
    assert result["schema"] == "KRENN_X5_REP4_GROUPS26_75_LANE_RESULT_V1"
    assert result["group_id"] == gid and result["ordinal"] == ordinal
    assert result["chart"] == lane["canonical_chart"] and result["source_sha256"] == lane["source_sha256"]
    assert result["normalized_dependency_sha256"] == sha(RUN / "normalized_dependency.json")
    source = RUN / lane["source_path"]
    assert sha(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
    assert result["status"] == "UNIT_IDEAL_EXACT_Q" and result["termination"] is None
    assert result["returncode"] == 0 and result["stderr"] == ""
    assert result["stdout"].splitlines()[-5:] == tail
    assert result["automatic_relaunch"] is False
    assert result["wall_seconds"] < 240 and result["peak_group_rss_bytes"] < 8 * 1024**3
    walls.append(result["wall_seconds"])
    peaks.append(result["peak_group_rss_bytes"])

files = sorted((RUN / "results").glob("group*.json"))
assert len(files) == 50 and [json.loads(path.read_text())["group_id"] for path in files] == IDS
assert not list(RUN.rglob("*.tmp"))
assert not any((RUN / "results" / f"group{gid:03d}.json").exists() for gid in range(76, 162))

out = {
    "schema": "KRENN_X5_REP4_GROUPS26_75_EXACT_Q_TERMINAL_REFEREE_V1",
    "status": "PASS_ALL_50_EXACT_Q_UNIT_IDEALS",
    "groups_closed": IDS,
    "dependency_closed_union_before_batch": list(range(26)),
    "closed_union_after_batch": list(range(76)),
    "remaining_groups": list(range(76, 162)),
    "variables_each": 91,
    "generators_each": 6577,
    "groebner_basis_size_each": 1,
    "unit_remainder_each": 0,
    "aggregate_lane_wall_seconds": sum(walls),
    "maximum_lane_wall_seconds": max(walls),
    "maximum_peak_rss_bytes": max(peaks),
    "strict_order": True,
    "parallel": False,
    "relaunch": False,
    "skipped": False,
    "groups_beyond_75_launched": False,
    "new_groups_closed": 50,
    "rep4_closed_count": 76,
    "rep4_total_groups": 162,
    "rep4_representative_closed": False,
    "seven_block_family_closed": False,
    "conjecture_closed": False,
    "resource_clear": True,
    "batch_result_sha256": sha(RUN / "batch_result.json"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "held_referee_manifest_sha256": sha(HELD_REF / "FINAL_MANIFEST.sha256"),
    "satisfied_dependency_manifest_sha256": sha(BIND / "FINAL_MANIFEST.sha256"),
}
(HERE / "results_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
