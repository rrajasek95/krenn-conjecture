#!/usr/bin/env python3
"""Independent terminal referee for the rep1 final groups 138..161 batch."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups138-161-exact-q-conditional-held-2026-08-25"
HELD_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups138-161-exact-q-conditional-held-referee-2026-08-25"
BIND = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups138-161-satisfied-dependency-binding-v2-2026-08-26"
ALIAS = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-terminal-referee-2026-08-25"
AUDITED_137 = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-terminal-referee-2026-08-26"
IDS = list(range(138, 162))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(path: Path, base: Path) -> int:
    count = 0
    for raw in path.read_text().splitlines():
        digest, name = raw.split(None, 1)
        target = Path(name.strip())
        target = target if target.is_absolute() else (base / target).resolve()
        assert target.is_file(), target
        assert sha(target) == digest, (target, sha(target), digest)
        count += 1
    return count


# Frozen final-24 design and original independent held approval.
assert sha(RUN / "MANIFEST.sha256") == "25a708451a790a3984052519a5fd129182a54b3fbe65dbc85279b998d0667bf5"
replay(RUN / "MANIFEST.sha256", RUN)
assert sha(RUN / "run_groups138_161.py") == "a942eb6a12512f334bc6bdbf1b023c1428c8372fda46032dbddfb84dcf554f8b"
assert sha(RUN / "source_ledger.json") == "ed416a9cc138abae890447995f04e084223fccfe0629da47c9e234e5c02e76be"
assert sha(RUN / "normalize_future_dependency.py") == "907519564535bc533e060dbef4545ccf2635234041af5d7e0a320db503991568"
assert sha(RUN / "future_groups88_137_dependency.json") == "f7750d13c571ef20341dc022f22bc15db94bb9eb2c279f9b3d53e6bb6036463d"
assert sha(HELD_REF / "results_referee.json") == "0a95f1d61729180393c58f457abf91239c9665f0c127a4721a896a1211c8291b"
assert sha(HELD_REF / "FINAL_MANIFEST.sha256") == "27ef2e78a85a7f9a9fd89576da782c300d3734158212e27e990e42bc7435b414"
replay(HELD_REF / "FINAL_MANIFEST.sha256", HELD_REF)

# Satisfied-v2 binding connects the compatibility alias to the independently
# audited 0..137 terminal seal from this session.
assert sha(BIND / "results_referee.json") == "b8529f9026af64c20325b6c05fbd649ddfd7a9d5a1e8009fe9a598242c40a5f7"
assert sha(BIND / "FINAL_MANIFEST.sha256") == "7e52cbe891eb28812730f35e125bb66fde548e07406d6dd992a37cccbf0eec73"
assert sha(BIND / "HELD_ACCEPTANCE_V2.json") == "7004526b14842c7efed72fb4f266aae5741a3f530dfad0b2b98d7386872eaef6"
replay(BIND / "FINAL_MANIFEST.sha256", BIND)
assert sha(AUDITED_137 / "results_referee.json") == "1de758a809cc4563313d872413f8e505153754b96df57499d11057e45e8f8789"
assert sha(AUDITED_137 / "FINAL_MANIFEST.sha256") == "23d2a55826b7f211298f9dd9a071aae1e17e6e95df3964b3d3825b98c2e8b32e"
replay(AUDITED_137 / "FINAL_MANIFEST.sha256", AUDITED_137)
assert sha(ALIAS / "results_referee.json") == "fd0c8ecb6b8ea1939819094b0f7734fc80fee7782754ff4df6c7f4a652c0cbb8"
assert sha(ALIAS / "FINAL_MANIFEST.sha256") == "128c3a39832cabe100a5e11ae09417ed6a73cf7197a515dee6831fcdf510809e"
replay(ALIAS / "FINAL_MANIFEST.sha256", ALIAS)

# Runner acceptance is an exact semantic instance of the sealed satisfied-v2
# acceptance; the runner then reopens and normalizes the pinned alias.
acceptance = json.loads((RUN / "independent_referee_acceptance.json").read_text())
bound_acceptance = json.loads((BIND / "HELD_ACCEPTANCE_V2.json").read_text())
assert acceptance == bound_acceptance
assert acceptance["future_terminal_manifest_sha256"] == sha(ALIAS / "FINAL_MANIFEST.sha256")
assert acceptance["future_terminal_result_sha256"] == sha(ALIAS / "results_referee.json")
spec = importlib.util.spec_from_file_location("rep1_final24_adapter", RUN / "normalize_future_dependency.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
normalized = module.load_and_normalize(
    acceptance["future_terminal_manifest_sha256"], acceptance["future_terminal_result_sha256"]
)
assert normalized["status"] == "PASS_DERIVED_EXACT_CLOSED_UNION_0_137"
assert normalized["closed_union"] == list(range(138))

# Terminal producer replay, exact launch authorization, and single-use attempt.
terminal_entries = replay(RUN / "TERMINAL_MANIFEST.sha256", RUN)
assert terminal_entries == 28
assert sha(RUN / "independent_referee_acceptance.json") == "127b2dc51266b49c5771fd97df4a3393bd9158da8af38ec2d93eb58b77095a91"
assert sha(RUN / "launch_clearance.json") == "6b2685541955f67fd8bf93e8dc8e9a67c51a1db84fa81d31b75e9b01b95968b1"
clearance = json.loads((RUN / "launch_clearance.json").read_text())
assert clearance["selected_group_ids"] == IDS and clearance["no_overlap_confirmed"] is True
assert clearance["native_wall_seconds_each"] == 240 and clearance["wrapper_wall_seconds_each"] == 250
assert clearance["rss_cap_bytes_each"] == 8 * 1024**3
assert clearance["parallel_authorized"] is False and clearance["skip_reorder_relaunch_authorized"] is False
attempt = json.loads((RUN / "BATCH_ATTEMPT.json").read_text())
assert attempt["status"] == "CONSUMED_SINGLE_USE" and attempt["group_ids"] == IDS
assert attempt["acceptance_sha256"] == sha(RUN / "independent_referee_acceptance.json")
assert attempt["clearance_sha256"] == sha(RUN / "launch_clearance.json")
assert attempt["future_terminal_manifest_sha256"] == sha(ALIAS / "FINAL_MANIFEST.sha256")
assert attempt["future_terminal_result_sha256"] == sha(ALIAS / "results_referee.json")

ledger = json.loads((RUN / "source_ledger.json").read_text())
lanes = ledger["lanes"]
assert [x["group_id"] for x in lanes] == IDS
assert [x["ordinal"] for x in lanes] == list(range(1, 25))
assert all(x["variables"] == 91 and x["generators"] == 6577 for x in lanes)
batch = json.loads((RUN / "batch_result.json").read_text())
assert batch["status"] == "PASS_ALL_24_UNIT" and batch["stop"] is None
assert batch["strict_order"] == IDS and batch["skipped_after_stop"] == []
assert batch["parallel"] is False and batch["relaunch"] is False
assert len(batch["completed"]) == 24

tail = [
    "INPUT_GENERATORS=6577",
    "GROEBNER_SIZE=1",
    "UNIT_REMAINDER=0",
    "STATUS=UNIT_IDEAL",
    "Auf Wiedersehen.",
]
walls = []
peaks = []
for ordinal, (gid, lane, item) in enumerate(zip(IDS, lanes, batch["completed"]), 1):
    path = RUN / f"results/group{gid:03d}.json"
    result = json.loads(path.read_text())
    assert item == {"group_id": gid, "status": "UNIT_IDEAL_EXACT_Q", "result_sha256": sha(path)}
    assert result["schema"] == "KRENN_X5_REP1_GROUPS138_161_LANE_RESULT_V1"
    assert result["group_id"] == gid and result["ordinal"] == ordinal
    assert result["chart"] == lane["canonical_chart"] and result["source_sha256"] == lane["source_sha256"]
    source = RUN / lane["source_path"]
    assert sha(source) == lane["source_sha256"] and source.stat().st_size == lane["source_bytes"]
    assert result["status"] == "UNIT_IDEAL_EXACT_Q" and result["termination"] is None
    assert result["wrapper_returncode"] == 0 and result["stderr"] == ""
    assert result["stdout"].splitlines()[-5:] == tail
    assert result["diagnostic_scope_one_group"] is True and result["automatic_relaunch"] is False
    assert result["wall_seconds"] < 240 and result["peak_group_rss_bytes"] < 8 * 1024**3
    walls.append(result["wall_seconds"])
    peaks.append(result["peak_group_rss_bytes"])

files = sorted((RUN / "results").glob("group*.json"))
assert len(files) == 24
assert [json.loads(path.read_text())["group_id"] for path in files] == IDS
assert not list(RUN.rglob("*.tmp"))
assert not any((RUN / "results" / f"group{gid:03d}.json").exists() for gid in range(162, 200))

out = {
    "schema": "KRENN_X5_REP1_GROUPS138_161_EXACT_Q_TERMINAL_REFEREE_V1",
    "status": "PASS_ALL_24_EXACT_Q_UNIT_IDEALS",
    "groups_closed": IDS,
    "dependency_closed_union_before_batch": list(range(138)),
    "closed_union_after_batch": list(range(162)),
    "remaining_groups": [],
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
    "groups_beyond_161_launched": False,
    "new_groups_closed": 24,
    "rep1_closed_count": 162,
    "rep1_total_groups": 162,
    "rep1_canonical_census_closed": True,
    "rep1_representative_closed_within_sealed_reduction": True,
    "rep1_all162_terminal_promotion_candidate": True,
    "seven_block_family_closed": False,
    "conjecture_closed": False,
    "batch_result_sha256": sha(RUN / "batch_result.json"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "held_referee_manifest_sha256": sha(HELD_REF / "FINAL_MANIFEST.sha256"),
    "satisfied_dependency_result_sha256": sha(BIND / "results_referee.json"),
    "satisfied_dependency_manifest_sha256": sha(BIND / "FINAL_MANIFEST.sha256"),
    "compatibility_alias_result_sha256": sha(ALIAS / "results_referee.json"),
    "compatibility_alias_manifest_sha256": sha(ALIAS / "FINAL_MANIFEST.sha256"),
}
(HERE / "results_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
