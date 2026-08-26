#!/usr/bin/env python3
"""Bind the frozen rep1 all-162 design to its three exact terminal shards."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep1-all162-terminal-promotion-conditional-design-2026-08-25"
DESIGN_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-all162-terminal-promotion-conditional-design-referee-2026-08-26"
SHARDS = [
    (
        ROOT / "computations/unaudited-codex-n8-x5-rep1-groups38-87-exact-q-terminal-referee-2026-08-25",
        "e6987baa4abf37de21e0466932f554ab9272da8a775ae89e5e25cfadd7ba17fc",
        "42e13d3e2103283e80f4f91af4d8433e21dc482435b945b3c252fa13452e7763",
        list(range(38, 88)),
        "KRENN_X5_REP1_GROUPS38_87_EXACT_Q_TERMINAL_REFEREE_V1",
        "PASS_ALL_50_EXACT_Q_UNIT_IDEALS",
    ),
    (
        ROOT / "computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-terminal-referee-2026-08-25",
        "128c3a39832cabe100a5e11ae09417ed6a73cf7197a515dee6831fcdf510809e",
        "fd0c8ecb6b8ea1939819094b0f7734fc80fee7782754ff4df6c7f4a652c0cbb8",
        list(range(88, 138)),
        "KRENN_X5_REP1_GROUPS88_137_EXACT_Q_TERMINAL_REFEREE_V1",
        "PASS_ALL_50_EXACT_Q_UNIT_IDEALS",
    ),
    (
        ROOT / "computations/unaudited-codex-n8-x5-rep1-groups138-161-exact-q-terminal-referee-2026-08-25",
        "2a4bd523463940e09b39367aeafa45f615bbdb3c6bfac6124f2c9c0cc496472e",
        "c283fb15b540054570b01011ea7c78d0d80976223e2b7cde87bb411baf407f55",
        list(range(138, 162)),
        "KRENN_X5_REP1_GROUPS138_161_EXACT_Q_TERMINAL_REFEREE_V1",
        "PASS_ALL_24_EXACT_Q_UNIT_IDEALS",
    ),
]


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


assert sha(DESIGN / "MANIFEST.sha256") == "df566e74f8048648605ab54b2ced3a513c6ff107310fca599384c2702df159d4"
assert sha(DESIGN / "results_terminal_promotion_design.json") == "5ea7e89aab44a62e8a89d4ebc41bdaeb9826098be420dc1f3ed14ab4b2cba2a2"
assert sha(DESIGN / "future_dependencies.json") == "cfaac79b9a04d37e32abd13b1a976af5e6c9b6f559ac3366893626652152769a"
replay(DESIGN / "MANIFEST.sha256")
assert sha(DESIGN_REF / "results_referee.json") == "6260209348c4732005f7067cfd25ef1b19bc6376b24664ea0cf31b9ba9e9af3c"
assert sha(DESIGN_REF / "FINAL_MANIFEST.sha256") == "52e45110f78987331b8bb56ea64f4b345219d2a5c532685b268b41c8b7bbed4c"
replay(DESIGN_REF / "FINAL_MANIFEST.sha256")
design = json.loads((DESIGN / "results_terminal_promotion_design.json").read_text())
design_ref = json.loads((DESIGN_REF / "results_referee.json").read_text())
assert design["status"] == "HELD_PROMOTION_THREE_FUTURE_PASS_SEALS_ABSENT"
assert design_ref["status"] == "PASS_DESIGN_ONLY_CURRENT_0_87_SEALED_FUTURE_88_161_REQUIRED"
contraction = design_ref["authoritative_contraction"]
assert contraction == {
    "canonical_groups": 162,
    "forward_reverse_localization": True,
    "members_per_group": 6,
    "raw_charts": 972,
    "two_minor_cover": True,
    "y_groups": 81,
    "y_raw": 486,
    "z_groups": 81,
    "z_raw": 486,
}
assert all(design_ref["hostile_tests"].values()) and len(design_ref["hostile_tests"]) == 12
assert design_ref["rank_zero_clause"]["nonzero_rank_claims_used"] is False

future = json.loads((DESIGN / "future_dependencies.json").read_text())
assert future["status"] == "UNSATISFIED_THREE_NULL_HASH_PAIRS" and future["satisfied"] is False
assert [d["group_ids"] for d in future["dependencies"]] == [shard[3] for shard in SHARDS]
assert all(d["manifest_sha256"] is None and d["result_sha256"] is None for d in future["dependencies"])

manifest_counts = []
shard_groups = []
for dependency, (directory, manifest_pin, result_pin, groups, schema, status) in zip(future["dependencies"], SHARDS):
    manifest = directory / "FINAL_MANIFEST.sha256"
    result_path = directory / "results_referee.json"
    assert sha(manifest) == manifest_pin and sha(result_path) == result_pin
    manifest_counts.append(replay(manifest))
    assert f"{result_pin}  results_referee.json" in manifest.read_text().splitlines()
    result = json.loads(result_path.read_text())
    assert result["schema"] == dependency["required_schema"] == schema
    assert result["status"] == dependency["required_status"] == status
    assert result["groups_closed"] == dependency["group_ids"] == groups
    assert result["strict_order"] is True and result["parallel"] is False
    assert result["skipped"] is False and result["relaunch"] is False
    shard_groups.extend(groups)

baseline = list(range(38))
closed = baseline + shard_groups
assert closed == list(range(162)) and len(closed) == len(set(closed)) == 162
assert 162 * contraction["members_per_group"] == contraction["raw_charts"] == 972
assert contraction["y_groups"] + contraction["z_groups"] == 162

acceptance = {
    "schema": "KRENN_X5_REP1_ALL162_TERMINAL_PROMOTION_ACCEPTANCE_V1",
    "status": "PASS_PROMOTE_REP1_ALL_162_CANONICAL_GROUPS_ONLY",
    "held_design_manifest_sha256": sha(DESIGN / "MANIFEST.sha256"),
    "promotion_design_sha256": sha(DESIGN / "results_terminal_promotion_design.json"),
    "future_dependencies_sha256": sha(DESIGN / "future_dependencies.json"),
    "groups38_87_manifest_sha256": SHARDS[0][1],
    "groups38_87_result_sha256": SHARDS[0][2],
    "groups88_137_manifest_sha256": SHARDS[1][1],
    "groups88_137_result_sha256": SHARDS[1][2],
    "groups138_161_manifest_sha256": SHARDS[2][1],
    "groups138_161_result_sha256": SHARDS[2][2],
    "closed_group_ids": closed,
    "raw_charts_closed": 972,
    "canonical_groups_closed": 162,
    "y_groups_closed": 81,
    "z_groups_closed": 81,
    "representative": "rep1",
    "cross_representative_transport": False,
    "full_conjecture": False,
}
(HERE / "TERMINAL_PROMOTION_ACCEPTANCE.json").write_text(json.dumps(acceptance, indent=2, sort_keys=True) + "\n")
result = {
    "schema": "KRENN_X5_REP1_ALL162_TERMINAL_PROMOTION_THEOREM_V1",
    "status": "PASS_REP1_ALL_162_CANONICAL_GROUPS_TERMINAL",
    "theorem": "Within the sealed rep1 guard-minor contraction and its forward/reverse two-minor localization, all 162 canonical exact-Q group ideals are unit; hence all 972 raw rep1 charts are empty.",
    "closed_group_ids": closed,
    "canonical_groups_closed": 162,
    "raw_charts_closed": 972,
    "members_per_group": 6,
    "y_groups_closed": 81,
    "z_groups_closed": 81,
    "forward_reverse_localization": True,
    "two_minor_cover": True,
    "rank_zero_clause_included": True,
    "shard_manifest_entries": manifest_counts,
    "terminal_acceptance_sha256": sha(HERE / "TERMINAL_PROMOTION_ACCEPTANCE.json"),
    "design_manifest_sha256": sha(DESIGN / "MANIFEST.sha256"),
    "design_result_sha256": sha(DESIGN / "results_terminal_promotion_design.json"),
    "design_referee_manifest_sha256": sha(DESIGN_REF / "FINAL_MANIFEST.sha256"),
    "design_referee_result_sha256": sha(DESIGN_REF / "results_referee.json"),
    "representative": "rep1",
    "cross_representative_transport": False,
    "other_representatives_closed_by_this_theorem": [],
    "seven_block_family_closed": False,
    "full_conjecture": False,
    "solver_runs_added": 0,
}
(HERE / "results_terminal_theorem.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "result_sha256": sha(HERE / "results_terminal_theorem.json"), "acceptance_sha256": result["terminal_acceptance_sha256"]}, sort_keys=True))
