#!/usr/bin/env python3
"""Build the conditional all-162 rep1 promotion ledger; no ideals or transport beyond rep1."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
QUOTIENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
QUOTIENT_REF = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-referee-2026-08-25"
CENSUS = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25"
CENSUS_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25"
RANK0 = ROOT / "computations/unaudited-codex-n8-x5-seven-block-reps1-4-5-low-rank-carrier-2026-08-25"
CLOSED37 = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25"
CLOSED37_REF = ROOT / "computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-referee-2026-08-25"
HELD_88 = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups88-137-exact-q-conditional-held-2026-08-25"
HELD_138 = ROOT / "computations/unaudited-codex-n8-x5-rep1-groups138-161-exact-q-conditional-held-2026-08-25"
PINS = {
    QUOTIENT / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    QUOTIENT / "results_design_audit.json": "abe37d5ae4555fc2df64a3778b6d8a84e316613afbed72d61fb820d8f64bdabb",
    QUOTIENT / "minor_quotient_metadata.json": "1a8c5bb3c105d8d87b2eab58a52934a44d7768c537cc33a1542d7d06402d317c",
    QUOTIENT_REF / "FINAL_MANIFEST.sha256": "16226d5f15d9f0d2d419095ec3842a7122ad77b40c1abe83bc9afe1b45b7800c",
    QUOTIENT_REF / "results_referee.json": "904c8143c647a8e36a3d94389923e979bf4d965ff6fc455dc72dbf3ef609d37e",
    CENSUS / "MANIFEST.sha256": "6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1",
    CENSUS / "results_canonical_census.json": "5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161",
    CENSUS_REF / "FINAL_MANIFEST.sha256": "f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a",
    CENSUS_REF / "results_referee.json": "36ce4421dcf73f816514664000d1889ce85c32cbf11cf38684f8cdb71a934b29",
    RANK0 / "MANIFEST.sha256": "9a3cec1a39422d2c3d7a6b40f6acdec0b04b19b893c0a1fb657c69d3b50bb8fe",
    RANK0 / "results_remaining_reps_low_rank_carrier.json": "359aa45545d85378dd9e945eb82be3adb98922648025fe853f930feac2b5f458",
    CLOSED37 / "MANIFEST.sha256": "7b66f582d1edf79e1e75c4ca328808f3f77548f840f5c42cc082dcd0f53764da",
    CLOSED37 / "normalized_next25_dependency.json": "29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76",
    CLOSED37_REF / "FINAL_MANIFEST.sha256": "950e504da1e64a4056cce58b0440165f5f8e5be4c159e2431f5010c5e06fbdc2",
    CLOSED37_REF / "results_referee.json": "1b303cb18146e5cadb4da5bf765fc9c2dd03f6593742652f34f5808691194a87",
    HELD_88 / "MANIFEST.sha256": "07ab0d198fc80b91025df7c892081f2aaaa94158014052246d7700095c054450",
    HELD_88 / "source_ledger.json": "2d111140f7508cd2548f8d26f73352b454e8dd80d2fbe4056f55819b62dd239b",
    HELD_138 / "MANIFEST.sha256": "25a708451a790a3984052519a5fd129182a54b3fbe65dbc85279b998d0667bf5",
    HELD_138 / "source_ledger.json": "ed416a9cc138abae890447995f04e084223fccfe0629da47c9e234e5c02e76be",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
design = json.loads((QUOTIENT / "results_design_audit.json").read_text())
qref = json.loads((QUOTIENT_REF / "results_referee.json").read_text())
census = json.loads((CENSUS / "results_canonical_census.json").read_text())
cref = json.loads((CENSUS_REF / "results_referee.json").read_text())
assert design["chart_union"] == {"all_equal_y_orbits": 1, "complete": True, "orbits": 162, "raw": 972, "y_orbits": 81, "z_orbits": 81}
assert qref["status"] == "PASS_EXACT_DESIGN_ONLY_NO_CLOSURE" and qref["census"]["raw"] == 972 and qref["census"]["s3_orbits"] == 162
assert cref["status"] == "PASS_EXACT_972_TO_162_CENSUS_NO_IDEALS" and cref["members_per_group"] == 6
records = census["enumeration"]["records"]
assert [record["group_id"] for record in records] == list(range(162))
raw_members = []
transport = []
for record in records:
    assert record["raw_member_count"] == len(record["raw_members"]) == 6
    members = [tuple(member) for member in record["raw_members"]]
    assert len(set(members)) == 6
    raw_members.extend(members)
    transport.append({"group_id": record["group_id"], "family": record["canonical_chart"][4], "canonical_chart": record["canonical_chart"], "raw_s3_members": record["raw_members"], "raw_member_count": 6, "exact_Q_source_sha256": record["exact_Q_source_sha256"]})
assert len(raw_members) == len(set(raw_members)) == 972
assert sum(entry["family"] == "y" for entry in transport) == 81
assert sum(entry["family"] == "z" for entry in transport) == 81
assert sum(member[4] == "y" for member in raw_members) == 486
assert sum(member[4] == "z" for member in raw_members) == 486
rank0_data = json.loads((RANK0 / "results_remaining_reps_low_rank_carrier.json").read_text())
rep1 = next(record for record in rank0_data["representatives"] if record["representative_id"] == 1)
assert rep1["proof"]["closed_rank_scope"] == [0]
assert "L67=0" in rep1["proof"]["zero_outside_factor"]
closed37 = json.loads((CLOSED37 / "normalized_next25_dependency.json").read_text())
assert closed37["closed_union"] == list(range(38))
future = json.loads((HERE / "future_dependencies.json").read_text())
assert future["satisfied"] is False and all(item["manifest_sha256"] is item["result_sha256"] is None for item in future["dependencies"])
shards = [list(range(38))] + [item["group_ids"] for item in future["dependencies"]]
flat = [group for shard in shards for group in shard]
assert len(flat) == len(set(flat)) == 162 and sorted(flat) == list(range(162))
result = {
    "schema": "KRENN_X5_REP1_ALL162_TERMINAL_PROMOTION_CONDITIONAL_DESIGN_V1",
    "status": "HELD_PROMOTION_THREE_FUTURE_PASS_SEALS_ABSENT",
    "authoritative_contraction": {"raw_charts": 972, "canonical_s3_charts": 162, "members_per_chart": 6, "variables_each": 91, "generators_each": 6577, "y_groups": 81, "z_groups": 81, "y_raw": 486, "z_raw": 486, "forward_reverse_localization": True, "two_minor_cover": True},
    "rank_zero_structural_branch": {"representative_id": 1, "scope": [0], "outside_zero_implication": rep1["proof"]["zero_outside_factor"], "source_pin_scope": "rank-zero clause only; retracted/nonzero pairing-only claims are not used"},
    "closure_shards": [
        {"group_ids": list(range(38)), "status": "SEALED_EXACT_Q_CLOSED", "dependency_hashes_null": False},
        {"group_ids": list(range(38, 88)), "status": "FUTURE_INDEPENDENT_PASS_REQUIRED", "dependency_hashes_null": True},
        {"group_ids": list(range(88, 138)), "status": "FUTURE_INDEPENDENT_PASS_REQUIRED", "dependency_hashes_null": True},
        {"group_ids": list(range(138, 162)), "status": "FUTURE_INDEPENDENT_PASS_REQUIRED", "dependency_hashes_null": True},
    ],
    "prospective_union_proof": {"group_count": 162, "union": list(range(162)), "duplicates": [], "missing": [], "extra": [], "all_future_required": True},
    "raw_s3_transport": transport,
    "scope": {"representative": "rep1 only", "full_family": "all 972 localized raw charts of rep1 across both y/z partner-pivot families", "transport": "only common simultaneous S3 color renaming within each source-labelled rep1 chart", "cross_representative_transport": False, "other_representatives_closed": [], "full_conjecture": False, "promotion_currently_authorized": False, "solver_runs": 0},
    "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
}
atomic_json(HERE / "results_terminal_promotion_design.json", result)
print(json.dumps({"status": result["status"], "groups": 162, "raw": 972, "y_z": [81, 81], "future_hash_pairs_null": 3}, sort_keys=True))
