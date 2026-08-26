#!/usr/bin/env python3
"""Independent terminal referee for the strict rep1 groups 88..137 batch."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25"
HELD_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-referee-2026-08-25"
BIND = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups88-137-satisfied-dependency-binding-v2-2026-08-26"
IDS = list(range(88, 138))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(path: Path, base: Path) -> None:
    for raw in path.read_text().splitlines():
        digest, name = raw.split(None, 1)
        target = Path(name.strip())
        target = target if target.is_absolute() else (base / target).resolve()
        assert target.is_file(), target
        assert sha(target) == digest, (target, sha(target), digest)


# Frozen held design and its independent approval.
assert sha(RUN / "MANIFEST.sha256") == "07ab0d198fc80b91025df7c892081f2aaaa94158014052246d7700095c054450"
replay(RUN / "MANIFEST.sha256", RUN)
assert sha(RUN / "run_groups88_137.py") == "604b0b938389e44506d627eba8652d74cfe3d3ba10a932efcb6c4dbfeee987e5"
assert sha(RUN / "source_ledger.json") == "2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b"
assert sha(RUN / "normalize_future_dependency.py") == "87ef24aa0e88434fa01d336e86736e0d6d60925323f08b2ae7fdec9b3bb7a64a"
assert sha(RUN / "future_groups38_87_dependency.json") == "1374fb5ed562ac0fd6b28ace616e09fbf011509555b02cb98996281d7188b380"
assert sha(HELD_REF / "FINAL_MANIFEST.sha256") == "f664aa999331fa81309a5df1b69d17d3b32d2d3783d44e833b856bc803c60e39"
replay(HELD_REF / "FINAL_MANIFEST.sha256", HELD_REF)
assert sha(HELD_REF / "results_referee.json") == "cb9e28e03a6f3449cec78d344e7964c0fd90bd20bb4668ffa0bab1b156fe0bbf"
assert sha(HELD_REF / "HELD_APPROVAL.json") == "e2bcfd41206c316487d8372bf5ccd56439381909fe3ff3cf50b4ca3c5238a519"

# Exact satisfied dependency and its independent acceptance instance.
assert sha(BIND / "FINAL_MANIFEST.sha256") == "4294a7fcc432dc7221b28b207332011f4d6ceb668946c50da9f0ae3584129366"
replay(BIND / "FINAL_MANIFEST.sha256", BIND)
assert sha(BIND / "results_referee.json") == "940b1f491393e94137041e6c3991f7dc4f98275f17e053f131ef65a21df172ea"
assert sha(BIND / "HELD_ACCEPTANCE_V2.json") == "8de2f95e00304c2a1afb79438103e126c84f3c6edea5c31a33a2152104785cfa"
assert sha(RUN / "satisfied_dependency_acceptance_v2.json") == "8de2f95e00304c2a1afb79438103e126c84f3c6edea5c31a33a2152104785cfa"
assert (RUN / "satisfied_dependency_acceptance_v2.json").read_bytes() == (BIND / "HELD_ACCEPTANCE_V2.json").read_bytes()
acceptance = json.loads((RUN / "satisfied_dependency_acceptance_v2.json").read_text())
assert acceptance["required_closed_union"] == list(range(88))
assert acceptance["selected_group_ids"] == IDS
assert acceptance["exact_Q_authorized"] is True and acceptance["solver_runs"] == 0

# Re-run the frozen normalizer against the exact terminal dependency pins.
spec = importlib.util.spec_from_file_location("rep1_future_adapter", RUN / "normalize_future_dependency.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
normalized = module.load_and_normalize(
    "e6987baa4abf37de21e0466932f554ab9272da8a775ae89e5e25cfadd7ba17fc",
    "42e13d3e2103283e80f4f91af4d8433e21dc482435b945b3c252fa13452e7763",
)
assert normalized["status"] == "PASS_DERIVED_EXACT_CLOSED_UNION_0_87"
assert normalized["closed_union"] == list(range(88))

# Replay the terminal producer seal and launch authorization.
replay(RUN / "TERMINAL_MANIFEST.sha256", RUN)
terminal_names = [line.split(None, 1)[1].strip() for line in (RUN / "TERMINAL_MANIFEST.sha256").read_text().splitlines()]
assert terminal_names[:5] == [
    "satisfied_dependency_acceptance_v2.json",
    "independent_referee_acceptance.json",
    "launch_clearance.json",
    "BATCH_ATTEMPT.json",
    "batch_result.json",
]
assert terminal_names[5:] == [f"results/group{gid:03d}.json" for gid in IDS]
assert len(terminal_names) == 55 and len(set(terminal_names)) == 55
assert sha(RUN / "independent_referee_acceptance.json") == "9d75486579fda95346ea9584e475a1b7ad91d46b6cb1816e96299b50a972dfee"
assert sha(RUN / "launch_clearance.json") == "d3e96679b852930921a7a712b3b2222c616935e46d6b1eea324ee9e87c071f79"
clearance = json.loads((RUN / "launch_clearance.json").read_text())
assert clearance["selected_group_ids"] == IDS and clearance["no_overlap_confirmed"] is True
assert clearance["native_wall_seconds_each"] == 240 and clearance["wrapper_wall_seconds_each"] == 250
assert clearance["rss_cap_bytes_each"] == 8 * 1024**3
assert clearance["parallel_authorized"] is False and clearance["skip_reorder_relaunch_authorized"] is False

attempt = json.loads((RUN / "BATCH_ATTEMPT.json").read_text())
assert attempt["status"] == "CONSUMED_SINGLE_USE" and attempt["group_ids"] == IDS
assert attempt["acceptance_sha256"] == "9d75486579fda95346ea9584e475a1b7ad91d46b6cb1816e96299b50a972dfee"
assert attempt["clearance_sha256"] == "d3e96679b852930921a7a712b3b2222c616935e46d6b1eea324ee9e87c071f79"
assert attempt["future_terminal_manifest_sha256"] == "e6987baa4abf37de21e0466932f554ab9272da8a775ae89e5e25cfadd7ba17fc"
assert attempt["future_terminal_result_sha256"] == "42e13d3e2103283e80f4f91af4d8433e21dc482435b945b3c252fa13452e7763"

ledger = json.loads((RUN / "source_ledger.json").read_text())
lanes = ledger["lanes"]
assert [x["group_id"] for x in lanes] == IDS
assert [x["ordinal"] for x in lanes] == list(range(1, 51))
assert all(x["variables"] == 91 and x["generators"] == 6577 for x in lanes)

batch = json.loads((RUN / "batch_result.json").read_text())
assert batch["status"] == "PASS_ALL_50_UNIT" and batch["stop"] is None
assert batch["strict_order"] == IDS and batch["skipped_after_stop"] == []
assert batch["parallel"] is False and batch["relaunch"] is False
assert len(batch["completed"]) == 50

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
    assert result["schema"] == "KRENN_X5_REP1_GROUPS88_137_LANE_RESULT_V1"
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

result_files = sorted((RUN / "results").glob("group*.json"))
assert len(result_files) == 50
assert [json.loads(path.read_text())["group_id"] for path in result_files] == IDS
assert not list(RUN.rglob("*.tmp"))
assert not any((RUN / "results" / f"group{gid:03d}.json").exists() for gid in range(138, 162))

out = {
    "schema": "KRENN_X5_REP1_GROUPS88_137_EXACT_Q_TERMINAL_REFEREE_V1",
    "status": "PASS_ALL_50_EXACT_Q_UNIT_IDEALS",
    "groups_closed": IDS,
    "dependency_closed_union_before_batch": list(range(88)),
    "closed_union_after_batch": list(range(138)),
    "remaining_groups": list(range(138, 162)),
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
    "groups_beyond_137_launched": False,
    "new_groups_closed": 50,
    "rep1_closed_count": 138,
    "rep1_total_groups": 162,
    "rep1_representative_closed": False,
    "seven_block_family_closed": False,
    "conjecture_closed": False,
    "batch_result_sha256": sha(RUN / "batch_result.json"),
    "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "held_referee_manifest_sha256": sha(HELD_REF / "FINAL_MANIFEST.sha256"),
    "satisfied_dependency_manifest_sha256": sha(BIND / "FINAL_MANIFEST.sha256"),
}
(HERE / "results_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
