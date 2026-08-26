#!/usr/bin/env python3
"""Exact read-only K21 recurrence/interface and artifact-availability audit."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("results_k21_availability.json")

DAG = "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
DIRECT_RESULT = "computations/unaudited-codex-orbit0-k21-direct-charge-2026-08-24/results_k21_direct_charge.json"
DIRECT_REFEREE = "computations/unaudited-codex-orbit0-k21-direct-charge-2026-08-24/results_k21_direct_plan_referee.json"
DIRECT_TERMINAL_REFEREE = "computations/unaudited-codex-orbit0-k21-direct-charge-2026-08-24/results_k21_direct_terminal_referee.json"
PROFILE_RESULT = "computations/unaudited-codex-orbit0-k21-profile-ready-charge-2026-08-24/results_k21_profile_ready_charge.json"
PROFILE_AUDIT = "computations/unaudited-codex-orbit0-k21-profile-ready-charge-2026-08-24/results_k21_profile_ready_charge_audit.json"
ASSEMBLY_MANIFEST = "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/k21_manifest_direct16_profile14_partial.json"
ASSEMBLY_RESULT = "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/results_k21_direct16_profile14_22_gap.json"
K19_RESULT = "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json"
K18_DIRECT_REPLAY = "computations/unaudited-codex-orbit0-direct-k18-profile-census-2026-08-23/results_direct_k18_profile_census_replay.json"
K14_K4_REPLAY = "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/results_k14_k4_full_replay.json"
K15_K3_MERGE = "computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/results_k15_k3_profile_merge.json"
K16_K2_MERGE = "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/results_k16_profile_merge.json"
K16_K2_STREAM_REFEREE = "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/results_k16_merge_full_stream_referee.json"
HIDDEN_22_RESULT = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/results_full_hidden_k16_k2_orbits.json"
HIDDEN_22_PINS = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/CHECKPOINTS.sha256"
HIDDEN_PARENT_RESULT = "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/results_full_hidden_k16_parent_recovery.json"
FILTERED_K16_RESULT = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/results_filtered_k16_run.json"


SMALL_PINS = {
    DAG: "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
    DIRECT_RESULT: "3fb99bdf3e8f230bcc8fe61936de5cb9020623d628efc4f5bcefac9e73fe5899",
    DIRECT_REFEREE: "6af4880ca1b398160d6a6e96dd0ecafe723e06c218c42052b62dfe93acd41300",
    DIRECT_TERMINAL_REFEREE: "e1cf26c84a29705c77621618588a4cb8afd1968adbb307ec715aaaef33305f66",
    PROFILE_RESULT: "fb6ffb58271d96498d8219f4c23dc55664031ab279d589211e17e65d75392452",
    PROFILE_AUDIT: "b3fab7f3f959f0aaa473549965e5e509ca6c8fe49299e54f37c34b6410a6649f",
    ASSEMBLY_MANIFEST: "9fb204274586314293585315512835297fdece287d0e03f8388155e118c22392",
    ASSEMBLY_RESULT: "7e554478542dd2daf470352ac3dee8481218a1edc8b69f878c0fd6725669f4ba",
    K19_RESULT: "8af5f43965fa6ab53d857dfea6b2b0241634783e744c100d85c24b3403f96e5a",
    K18_DIRECT_REPLAY: "3d3a0c0c6dd534ba22b1fffd1b41ff3a28929011be22b15d6f223d590aa7eeae",
    K14_K4_REPLAY: "8c3c0a602e469522d8a2cae39440f7b9532d1ac01fbd967b7ff91cbf0670238a",
    K15_K3_MERGE: "7033bbff3bd353ef306de165e94bf11911f65d9570da6079eee7b382a4181c9b",
    K16_K2_MERGE: "ae6d6814ec8d78a36c5dce75e09f5e7306b15b47ad8c4c14bfd3bc6a42c6fe8c",
    K16_K2_STREAM_REFEREE: "02148afcd7465cea95f23a905121c0fe3c1bac2f703b88004a03939720ea4a50",
    HIDDEN_22_RESULT: "54946037ec9d96a5c3509e4f057350601aaaa34764aad84753cea7b03d2944a4",
    HIDDEN_22_PINS: "3a8f14e7daf0620c5f4e09e1928f286857d8c3d77c6051570135aa8f13134c85",
    HIDDEN_PARENT_RESULT: "a55412f5103ae4bf9a4e3a272d0fc751d9d5da15a3f6c00d15e1c016fd438060",
    FILTERED_K16_RESULT: "ff4505a44cc76894ede59f4c642d385cf21ecffd5ac0aae875f7652c4966b861",
    "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/run_k19_weight_runs.rs": "dd3d885aa780bc99a4e8420bb84669141a14ea2df9cf097e11832b40830387b3",
    "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/stream_hidden_k16_children.rs": "338218736e1e414199580c1d1058e0ca9957c9fcb02ed7abd262fad24a44fd99",
}


ARTIFACTS = {
    "k17_direct_terminal_profiles": {
        "path": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/weights_k17_direct_k2.bin",
        "sha256": "4fa59665dcbec7fbd4c5a7682bc02d1094f8c4a64a712f1c451453b1644bf5ec",
        "bytes": 157036363,
        "kind": "source-compressed terminal-parent profile/signature/pivot weights",
        "scope": "sufficient for a terminal K4 charge; not sufficient to materialize or prolong K21 rows",
        "pin_via": K19_RESULT,
    },
    "k17_k14_r3_terminal_profiles": {
        "path": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/weights_k17_k14_k2.bin",
        "sha256": "34fdbffd1331035831dc86f2eb5ddf0183f5adba1300868248c4023916feee66",
        "bytes": 816801444,
        "kind": "source-compressed terminal-parent profile/signature/pivot weights",
        "scope": "sufficient for the grouped terminal K4 charge; not a K17 row checkpoint",
        "pin_via": K19_RESULT,
    },
    "k17_k15_r2_terminal_profiles": {
        "path": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/weights_k17_k15_k2.bin",
        "sha256": "864b3cac1230047db3200a4560d5ce3240747c9e89d0f4cfd5a8fe1236235b1d",
        "bytes": 950477803,
        "kind": "source-compressed terminal-parent profile/signature/pivot weights",
        "scope": "sufficient for the grouped terminal K4 charge; not a K17 row checkpoint",
        "pin_via": K19_RESULT,
    },
    "k18_direct_terminal_profiles": {
        "path": "computations/unaudited-codex-orbit0-direct-k18-profile-census-2026-08-23/direct_k18_enriched_profiles.bin",
        "sha256": "d77f2a84f220aad9f52fe81547ab730a6b834005b27e6f47172bb80cf5850da2",
        "bytes": 70494808,
        "kind": "source-compressed terminal-parent profile/signature/pivot weights with witness",
        "scope": "sufficient for grouped terminal K3 charge; exact-zero signed profiles omitted",
        "pin_via": K18_DIRECT_REPLAY,
    },
    "k18_k14_r4_terminal_profiles": {
        "path": "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/k14_k4_enriched_profiles.bin",
        "sha256": "5cc8c15b2333937ddfaefac1ec056b2f2fd899f5b89ea5b0276d374b05d92d7f",
        "bytes": 1894591760,
        "kind": "source-compressed terminal-parent profile/signature/pivot weights with witness",
        "scope": "sufficient for terminal K3 charge; exact-zero signed profiles omitted",
        "pin_via": K14_K4_REPLAY,
    },
    "k18_k15_r3_terminal_profiles": {
        "path": "computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/checkpoint_k15_k3_profiles_merged.bin",
        "sha256": "8b05f3fb8edcda062111d20089309abb85d4ccd8675d289947178b437139c1db",
        "bytes": 2658696792,
        "kind": "source-compressed terminal-parent profile/signature/pivot weights with witness",
        "scope": "sufficient for grouped terminal K3 charge; not a K18 row checkpoint",
        "pin_via": K15_K3_MERGE,
    },
    "k18_k16_r2_terminal_profiles": {
        "path": "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/checkpoint_k16_k2_profiles_merged.bin",
        "sha256": "d23271184b8258634cbf6f0942c4b1068e04c505e206b08fd3638e1c9b03be03",
        "bytes": 715131168,
        "kind": "source-compressed terminal-parent profile/signature/pivot weights with witness",
        "scope": "sufficient for grouped terminal K3 charge; not a K18 row checkpoint",
        "pin_via": K16_K2_STREAM_REFEREE,
        "full_hash_checked_by_this_audit": True,
    },
    "k18_hidden_22_pivotable_rows": {
        "path": "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin",
        "sha256": "442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8",
        "bytes": 12675197280,
        "kind": "literal canonical K18 pivotable-row checkpoint with exact orbit mass and provenance",
        "scope": "sufficient for terminal K3 charge and stronger than a profile-only interface",
        "pin_via": HIDDEN_22_PINS,
    },
    "direct_k15_rows": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k15.bin",
        "sha256": "e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f",
        "bytes": 169958768,
        "kind": "literal canonical direct-K15 rows and coefficients",
        "scope": "source checkpoint from which K19 parents on response K4 can be regenerated",
        "pin_via": FILTERED_K16_RESULT,
        "full_hash_checked_by_this_audit": True,
    },
    "direct_k16_rows": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin",
        "sha256": "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3",
        "bytes": 771107056,
        "kind": "literal canonical direct-K16 rows and coefficients",
        "scope": "source checkpoint from which K19 parents on response K3 can be regenerated",
        "pin_via": FILTERED_K16_RESULT,
        "full_hash_checked_by_this_audit": True,
    },
    "orbit0_source_structure": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin",
        "sha256": "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
        "bytes": 115275,
        "kind": "frozen R8prime orbit/factor/anchor source structure",
        "scope": "literal source replay for direct and K14/K15-derived parents",
        "pin_via": DIRECT_REFEREE,
        "full_hash_checked_by_this_audit": True,
    },
    "k19_source_replay_blueprint": {
        "path": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/run_k19_weight_runs.rs",
        "sha256": SMALL_PINS["computations/unaudited-codex-orbit0-k19-charge-2026-08-23/run_k19_weight_runs.rs"],
        "kind": "audited source-linear K15/K16/K17 parent replay implementation",
        "scope": "blueprint only: it emits terminal charge profiles, not the missing prolongable K19 checkpoint",
        "pin_via": K19_RESULT,
    },
    "hidden_k16_parent_provider": {
        "path": "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/results_full_hidden_k16_parent_recovery.json",
        "sha256": SMALL_PINS[HIDDEN_PARENT_RESULT],
        "kind": "complete 31-run hidden K16 literal-parent recovery ledger and restartable child-provider contract",
        "scope": "can regenerate K3 K19 parents for D14:222|R:2-3; no K19 checkpoint is retained",
        "pin_via": HIDDEN_PARENT_RESULT,
    },
}


def packet_ids(degree: int, packets: tuple[str, ...], responses: tuple[int, ...]) -> list[str]:
    suffix = "-".join(map(str, responses))
    return [f"D{degree}:{packet}|R:{suffix}" for packet in packets]


GROUPS = [
    {
        "group_id": "direct_D17_R4",
        "ids": packet_ids(17, ("234", "243", "324", "333", "342", "423", "432"), (4,)),
        "availability": "DIRECT_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_REFEREED",
        "artifact_keys": ["k17_direct_terminal_profiles", "orbit0_source_structure"],
        "gap": "charge is group-aggregated; no individual-ID scalar or K21 row checkpoint",
    },
    {
        "group_id": "direct_D18_R3",
        "ids": packet_ids(18, ("244", "334", "343", "424", "433", "442"), (3,)),
        "availability": "DIRECT_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_REFEREED",
        "artifact_keys": ["k18_direct_terminal_profiles", "orbit0_source_structure"],
        "gap": "charge is group-aggregated; no individual-ID scalar or K21 row checkpoint",
    },
    {
        "group_id": "direct_D19_R2",
        "ids": packet_ids(19, ("344", "434", "443"), (2,)),
        "availability": "DIRECT_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_REFEREED",
        "artifact_keys": ["orbit0_source_structure"],
        "gap": "direct source was replayed factorwise; no retained K19 terminal profile, individual-ID scalar, or K21 row checkpoint",
    },
    {
        "group_id": "derived_D14_R3_R4",
        "ids": packet_ids(14, ("222",), (3, 4)),
        "availability": "PROFILE_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_AUDITED",
        "artifact_keys": ["k17_k14_r3_terminal_profiles"],
        "gap": "single-ID scalar is exact; no K21 row checkpoint or later-tail interface was retained",
    },
    {
        "group_id": "derived_D14_R4_R3",
        "ids": packet_ids(14, ("222",), (4, 3)),
        "availability": "PROFILE_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_AUDITED",
        "artifact_keys": ["k18_k14_r4_terminal_profiles"],
        "gap": "single-ID scalar is exact; no K21 row checkpoint or later-tail interface was retained",
    },
    {
        "group_id": "derived_D15_R2_R4",
        "ids": packet_ids(15, ("223", "232", "322"), (2, 4)),
        "availability": "PROFILE_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_AUDITED",
        "artifact_keys": ["k17_k15_r2_terminal_profiles"],
        "gap": "three-ID scalar is group-aggregated; no individual-ID scalars or K21 row checkpoint",
    },
    {
        "group_id": "derived_D15_R3_R3",
        "ids": packet_ids(15, ("223", "232", "322"), (3, 3)),
        "availability": "PROFILE_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_AUDITED",
        "artifact_keys": ["k18_k15_r3_terminal_profiles"],
        "gap": "three-ID scalar is group-aggregated; no individual-ID scalars or K21 row checkpoint",
    },
    {
        "group_id": "derived_D15_R4_R2",
        "ids": packet_ids(15, ("223", "232", "322"), (4, 2)),
        "availability": "K19_PARENT_RECONSTRUCTION_FROM_LITERAL_SOURCE_REQUIRED",
        "artifact_keys": ["direct_k15_rows", "k19_source_replay_blueprint"],
        "gap": "K19 parent coefficients/profiles were not retained; reconstruct and signed-collect them before the terminal K2 response",
    },
    {
        "group_id": "derived_D16_R2_R3",
        "ids": packet_ids(16, ("224", "233", "242", "323", "332", "422"), (2, 3)),
        "availability": "PROFILE_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_AUDITED",
        "artifact_keys": ["k18_k16_r2_terminal_profiles"],
        "gap": "six-ID scalar is group-aggregated; no individual-ID scalars or K21 row checkpoint",
    },
    {
        "group_id": "derived_D16_R3_R2",
        "ids": packet_ids(16, ("224", "233", "242", "323", "332", "422"), (3, 2)),
        "availability": "K19_PARENT_RECONSTRUCTION_FROM_LITERAL_SOURCE_REQUIRED",
        "artifact_keys": ["direct_k16_rows", "k19_source_replay_blueprint"],
        "gap": "K19 parent coefficients/profiles were not retained; reconstruct and signed-collect them before the terminal K2 response",
    },
    {
        "group_id": "derived_D17_R2_R2",
        "ids": packet_ids(17, ("234", "243", "324", "333", "342", "423", "432"), (2, 2)),
        "availability": "K19_PARENT_RECONSTRUCTION_FROM_SOURCE_FORMULA_REQUIRED",
        "artifact_keys": ["orbit0_source_structure", "k17_direct_terminal_profiles", "k19_source_replay_blueprint"],
        "gap": "the K17 profile file is terminal-only and cannot be prolonged; replay direct K17 parents and signed-collect their K2 K19 children",
    },
    {
        "group_id": "derived_D14_R2_R2_R3",
        "ids": packet_ids(14, ("222",), (2, 2, 3)),
        "availability": "TERMINAL_LITERAL_PARENT_CHECKPOINT_RETAINED_K21_CHARGE_MISSING",
        "artifact_keys": ["k18_hidden_22_pivotable_rows"],
        "gap": "stream the retained literal pivotable K18 checkpoint through terminal K3 charge; no reconstruction is needed",
    },
    {
        "group_id": "derived_D14_R2_R3_R2",
        "ids": packet_ids(14, ("222",), (2, 3, 2)),
        "availability": "K19_PARENT_RECONSTRUCTION_FROM_LITERAL_SOURCE_REQUIRED",
        "artifact_keys": ["hidden_k16_parent_provider"],
        "gap": "the hidden K16 parent runs/provider survive, but their K3 K19 children were evaluated only terminally and never retained",
    },
    {
        "group_id": "derived_D14_R3_R2_R2",
        "ids": packet_ids(14, ("222",), (3, 2, 2)),
        "availability": "K19_PARENT_RECONSTRUCTION_FROM_SOURCE_FORMULA_REQUIRED",
        "artifact_keys": ["orbit0_source_structure", "k17_k14_r3_terminal_profiles", "k19_source_replay_blueprint"],
        "gap": "the K17 profile file is terminal-only and cannot be prolonged; replay the K14/R3 K17 source and collect its K2 K19 children",
    },
    {
        "group_id": "derived_D15_R2_R2_R2",
        "ids": packet_ids(15, ("223", "232", "322"), (2, 2, 2)),
        "availability": "K19_PARENT_RECONSTRUCTION_FROM_SOURCE_FORMULA_REQUIRED",
        "artifact_keys": ["orbit0_source_structure", "k17_k15_r2_terminal_profiles", "k19_source_replay_blueprint"],
        "gap": "the K17 profile file is terminal-only and cannot be prolonged; replay the K15/R2 K17 source and collect its K2 K19 children",
    },
]


def load(rel: str):
    return json.loads((ROOT / rel).read_text())


def sha(rel: str) -> str:
    h = hashlib.sha256()
    with (ROOT / rel).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def logical_digest(value) -> str:
    clean = dict(value)
    clean.pop("logical_sha256", None)
    return hashlib.sha256(json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def parse_responses(lineage: str) -> tuple[int, ...]:
    return tuple(map(int, lineage.split("|R:", 1)[1].split("-")))


def entry_ids(entry: dict) -> list[str]:
    if ("id" in entry) == ("ids" in entry):
        raise ValueError("exactly one of id/ids is required")
    ids = [entry["id"]] if "id" in entry else entry["ids"]
    if not isinstance(ids, list) or not ids or not all(isinstance(x, str) for x in ids):
        raise ValueError("invalid ID group")
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate within scalar group")
    return ids


def independent_assemble(entries: list[dict], required: set[str], require_complete: bool) -> dict:
    """Independent exact-Q grouped-scalar gate used for hostile checks too."""
    flat = [lineage for entry in entries for lineage in entry_ids(entry)]
    duplicates = sorted(lineage for lineage, count in Counter(flat).items() if count != 1)
    extra = sorted(set(flat) - required)
    missing = sorted(required - set(flat))
    if duplicates:
        raise ValueError(f"duplicate IDs: {duplicates}")
    if extra:
        raise ValueError(f"extra IDs: {extra}")
    if require_complete and missing:
        raise ValueError(f"missing IDs: {missing}")
    return {
        "covered": set(flat),
        "missing": missing,
        # A scalar is attached to one entry/group and is deliberately summed
        # once, irrespective of the number of IDs certified by that group.
        "full": sum((Fraction(entry["full"]) for entry in entries), Fraction()),
        "irreducible": sum((Fraction(entry["irreducible"]) for entry in entries), Fraction()),
        "scalar_groups": len(entries),
    }


def main() -> None:
    for rel, digest in SMALL_PINS.items():
        assert sha(rel) == digest, rel

    dag = load(DAG)
    assert dag["logical_sha256"] == "ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66"
    required = set(dag["required_reachable_lineage_ids_by_degree"]["21"])
    assert len(required) == 52
    nodes = {node["id"]: node for node in dag["nodes"] if node["id"] in required}
    assert set(nodes) == required

    grouped_ids = [lineage for group in GROUPS for lineage in group["ids"]]
    assert len(grouped_ids) == len(set(grouped_ids)) == 52
    assert set(grouped_ids) == required

    # Validate publisher pins without rehashing multi-gigabyte files.  Three
    # smaller source/checkpoint files whose publishers did not freeze a byte
    # digest are hashed explicitly below.
    k19 = load(K19_RESULT)
    replay18 = load(K18_DIRECT_REPLAY)
    replay14 = load(K14_K4_REPLAY)
    merge15 = load(K15_K3_MERGE)
    hidden_pins = {}
    for line in (ROOT / HIDDEN_22_PINS).read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        hidden_pins[name] = digest
    assert k19["pinned"][ARTIFACTS["k17_direct_terminal_profiles"]["path"]] == ARTIFACTS["k17_direct_terminal_profiles"]["sha256"]
    assert k19["pinned"][ARTIFACTS["k17_k14_r3_terminal_profiles"]["path"]] == ARTIFACTS["k17_k14_r3_terminal_profiles"]["sha256"]
    assert k19["pinned"][ARTIFACTS["k17_k15_r2_terminal_profiles"]["path"]] == ARTIFACTS["k17_k15_r2_terminal_profiles"]["sha256"]
    assert replay18["merged_sha256"] == ARTIFACTS["k18_direct_terminal_profiles"]["sha256"]
    assert replay14["merged_sha256"] == ARTIFACTS["k18_k14_r4_terminal_profiles"]["sha256"]
    assert merge15["checkpoint_sha256"] == ARTIFACTS["k18_k15_r3_terminal_profiles"]["sha256"]
    assert hidden_pins["checkpoint_k18_22_pivotable.bin"] == ARTIFACTS["k18_hidden_22_pivotable_rows"]["sha256"]

    for key, artifact in ARTIFACTS.items():
        p = ROOT / artifact["path"]
        assert p.is_file(), key
        if "bytes" in artifact:
            assert p.stat().st_size == artifact["bytes"], key
        if artifact.get("full_hash_checked_by_this_audit"):
            assert sha(artifact["path"]) == artifact["sha256"], key

    direct_result = load(DIRECT_RESULT)
    direct_referee = load(DIRECT_REFEREE)
    direct_terminal_referee = load(DIRECT_TERMINAL_REFEREE)
    profile_result = load(PROFILE_RESULT)
    profile_audit = load(PROFILE_AUDIT)
    direct_ids = {lineage for group in direct_result["groups"] for lineage in group["ids"]}
    referee_ids = set(direct_referee["coverage"]["covered_direct_response_K21_ids"])
    depth_one = {lineage for lineage in required if len(parse_responses(lineage)) == 1}
    assert direct_result["status"] == "PASS_COMPLETE_16_DIRECT_ID_K21_CHARGE"
    assert direct_referee["status"] == "PASS_EXACT_SIGNATURE_LEVEL_DIRECT_K21_PLAN_REFEREE"
    assert direct_terminal_referee["status"] == "PASS_INDEPENDENT_TERMINAL_REFEREE_DIRECT16_K21_CHARGE"
    assert direct_ids == referee_ids == depth_one
    assert {lineage for group in direct_terminal_referee["terminal_result"]["groups"] for lineage in group["ids"]} == depth_one
    assert direct_terminal_referee["terminal_result"]["totals"]["full_and_irreducible_charge"]["text"] == "-55230881792/35"
    assert direct_result["individual_id_charges"] is None
    profile_ids = set(profile_result["coverage"]["covered_ids"])
    profile_group_ids = {
        lineage
        for group in GROUPS
        if group["availability"] == "PROFILE_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_AUDITED"
        for lineage in group["ids"]
    }
    assert profile_result["status"] == "PASS_EXACT_K21_14_PROFILE_READY_77_CHARGE_SUBTOTAL"
    assert profile_audit["status"] == "PASS_INDEPENDENT_K21_PROFILE_READY_COVERAGE_ARITHMETIC_HASH_AUDIT"
    assert profile_audit["logical_sha256"] == "97bcd555f7f65d45f46b85c669cc361c01cd6d9aac65c95e610c63f529afc207"
    assert profile_ids == set(profile_audit["covered_ids"]) == profile_group_ids
    assert profile_ids.isdisjoint(direct_ids)
    assert profile_result["subtotal"]["full_77_charge_reduced"] == "-24730854875640832/2258025"
    assert profile_result["subtotal"]["full_77_charge_scaled_U"] == profile_result["subtotal"]["irreducible_77_charge_scaled_U"]

    # Independently validate the strict 30/52 grouped-scalar manifest and its
    # rejected-incomplete result; do not call or import the producer assembler.
    assembly_manifest = load(ASSEMBLY_MANIFEST)
    assembly_result = load(ASSEMBLY_RESULT)
    entries = assembly_manifest["groups"]
    expected_groups = {}
    for group in direct_terminal_referee["terminal_result"]["groups"]:
        scalar = group["full_and_irreducible_charge"]["text"]
        expected_groups[frozenset(group["ids"])] = (Fraction(scalar), Fraction(scalar), SMALL_PINS[DIRECT_RESULT])
    for group in profile_result["groups"]:
        expected_groups[frozenset(group["ids"])] = (
            Fraction(group["full_77_charge_reduced"]),
            Fraction(group["irreducible_77_charge_reduced"]),
            SMALL_PINS[PROFILE_RESULT],
        )
    assert len(expected_groups) == len(entries) == 8
    seen_groups = set()
    for entry in entries:
        key = frozenset(entry_ids(entry))
        assert key in expected_groups and key not in seen_groups
        full, irreducible, evidence = expected_groups[key]
        assert Fraction(entry["full"]) == full
        assert Fraction(entry["irreducible"]) == irreducible
        assert entry["evidence_sha256"] == evidence
        seen_groups.add(key)
    assert seen_groups == set(expected_groups)

    assembled = independent_assemble(entries, required, require_complete=False)
    assert assembled["covered"] == direct_ids | profile_ids
    assert assembled["full"] == assembled["irreducible"] == Fraction(-28294075214451712, 2258025)
    assert assembled["scalar_groups"] == 8 and len(assembled["covered"]) == 30 and len(assembled["missing"]) == 22
    assert assembly_result["status"] == "REJECT_INCOMPLETE_K21_52_ID_GATE"
    assert assembly_result["complete_K21_claim"] is False
    assert set(assembly_result["covered_ids"]) == assembled["covered"]
    assert assembly_result["covered_paths"] == 30 and assembly_result["required_paths"] == 52
    assert assembly_result["scalar_groups"] == 8
    assert assembly_result["duplicate_paths"] == [] and assembly_result["extra_paths"] == []
    assert set(assembly_result["missing_paths"]) == set(assembled["missing"])
    assert Fraction(assembly_result["full"]["text"]) == assembled["full"]
    assert Fraction(assembly_result["irreducible"]["text"]) == assembled["irreducible"]
    manifest_logical = hashlib.sha256(json.dumps(assembly_manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert assembly_result["manifest_sha256"] == manifest_logical == "01e091c613d52d0e1e68c040954b60f07704ac4fe2a45877a2ce3721c045f6a4"

    # Hostile complete-gate audit: one grouped scalar must be counted once,
    # while a missing ID or an ID duplicated across groups must be rejected.
    required_sorted = sorted(required)
    synthetic = [{
        "ids": required_sorted[:4],
        "full": "7/3",
        "irreducible": "11/5",
    }] + [{"id": lineage, "full": "0", "irreducible": "0"} for lineage in required_sorted[4:]]
    synthetic_result = independent_assemble(synthetic, required, require_complete=True)
    assert synthetic_result["full"] == Fraction(7, 3) and synthetic_result["irreducible"] == Fraction(11, 5)
    missing_rejected = duplicate_rejected = False
    try:
        independent_assemble(synthetic[:-1], required, require_complete=True)
    except ValueError as exc:
        missing_rejected = "missing IDs" in str(exc)
    try:
        independent_assemble(synthetic + [synthetic[-1]], required, require_complete=True)
    except ValueError as exc:
        duplicate_rejected = "duplicate IDs" in str(exc)
    assert missing_rejected and duplicate_rejected
    hostile_guards = {
        "missing_ID_rejected": True,
        "duplicate_ID_rejected": True,
        "group_scalar_counted_once": True,
        "synthetic_four_ID_group_full": "7/3",
        "synthetic_four_ID_group_irreducible": "11/5",
    }

    lineages = []
    for group in GROUPS:
        for lineage in group["ids"]:
            node = nodes[lineage]
            responses = tuple(node["response_shifts"])
            depth = len(responses)
            assert responses == parse_responses(lineage)
            assert node["denominator_product_class"]["pivot_depth"] == depth
            assert node["degree"] == 21
            recurrence_class = "DIRECT_ONE_PIVOT" if depth == 1 else "DERIVED"
            lineages.append({
                "lineage_id": lineage,
                "group_id": group["group_id"],
                "recurrence_class": recurrence_class,
                "pivot_depth": depth,
                "direct_packet_degree": node["direct_packet"]["degree"],
                "direct_packet_shifts": node["direct_packet"]["ordered_factor_shifts"],
                "response_shifts": list(responses),
                "terminal_parent_degree": 21 - responses[-1],
                "terminal_response_shift": responses[-1],
                "sign_relative_to_unsigned_R8prime": node["sign_relative_to_unsigned_R8prime"],
                "availability": group["availability"],
                "artifact_keys": group["artifact_keys"],
                "gap": group["gap"],
            })

    depth_counts = Counter(line["pivot_depth"] for line in lineages)
    class_counts = Counter(line["recurrence_class"] for line in lineages)
    availability_counts = Counter(line["availability"] for line in lineages)
    assert depth_counts == {1: 16, 2: 30, 3: 6}
    assert class_counts == {"DIRECT_ONE_PIVOT": 16, "DERIVED": 36}
    assert availability_counts == {
        "DIRECT_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_REFEREED": 16,
        "PROFILE_GROUPED_K21_CHARGE_COMPUTED_INDEPENDENTLY_AUDITED": 14,
        "TERMINAL_LITERAL_PARENT_CHECKPOINT_RETAINED_K21_CHARGE_MISSING": 1,
        "K19_PARENT_RECONSTRUCTION_FROM_LITERAL_SOURCE_REQUIRED": 10,
        "K19_PARENT_RECONSTRUCTION_FROM_SOURCE_FORMULA_REQUIRED": 11,
    }

    group_rows = []
    for group in GROUPS:
        sample = next(line for line in lineages if line["group_id"] == group["group_id"])
        group_rows.append({
            "group_id": group["group_id"],
            "count": len(group["ids"]),
            "ids": group["ids"],
            "recurrence_class": sample["recurrence_class"],
            "pivot_depth": sample["pivot_depth"],
            "terminal_parent_degree": sample["terminal_parent_degree"],
            "terminal_response_shift": sample["terminal_response_shift"],
            "availability": group["availability"],
            "artifact_keys": group["artifact_keys"],
            "gap": group["gap"],
        })

    result = {
        "status": "PASS_EXACT_K21_52_ID_RECURRENCE_AND_AVAILABILITY_AUDIT",
        "scope": "Read-only recurrence, provenance, and artifact-availability audit over pinned K21 charge results. No new charge evaluation, parent reconstruction, row collection, or later tail generation.",
        "dag": {
            "artifact": DAG,
            "sha256": SMALL_PINS[DAG],
            "logical_sha256": dag["logical_sha256"],
            "required_K21_ids": 52,
            "coverage_equal": True,
            "missing": [],
            "extra": [],
            "duplicates": [],
        },
        "classification_counts": {
            "DIRECT_ONE_PIVOT": class_counts["DIRECT_ONE_PIVOT"],
            "DERIVED": class_counts["DERIVED"],
            "pivot_depth_1": depth_counts[1],
            "pivot_depth_2": depth_counts[2],
            "pivot_depth_3": depth_counts[3],
        },
        "availability_counts": dict(sorted(availability_counts.items())),
        "current_charge_coverage": {
            "grouped_K21_charge_ids_present": 30,
            "remaining_K21_charge_ids": 22,
            "individual_id_charges_present": 2,
            "direct_group_interface_referee": DIRECT_REFEREE,
            "direct_group_terminal_referee": DIRECT_TERMINAL_REFEREE,
            "direct_group_scalar_independently_replayed": True,
            "direct_16_grouped_full_and_irreducible_charge": "-55230881792/35",
            "profile_14_result": PROFILE_RESULT,
            "profile_14_independent_audit": PROFILE_AUDIT,
            "profile_14_grouped_full_and_irreducible_charge": "-24730854875640832/2258025",
            "combined_30_grouped_full_and_irreducible_charge": "-28294075214451712/2258025",
            "guard": "The 30-ID coverage consists of eight exact group scalars. Only the two singleton D14 groups are individual-ID scalars; this is not a complete K21 page.",
        },
        "strict_30_of_52_assembly_audit": {
            "manifest": ASSEMBLY_MANIFEST,
            "manifest_byte_sha256": SMALL_PINS[ASSEMBLY_MANIFEST],
            "manifest_logical_sha256": manifest_logical,
            "result": ASSEMBLY_RESULT,
            "result_byte_sha256": SMALL_PINS[ASSEMBLY_RESULT],
            "status": assembly_result["status"],
            "scalar_groups": 8,
            "covered_ids": 30,
            "missing_ids": 22,
            "full_and_irreducible": str(assembled["full"]),
            "missing": assembled["missing"],
            "hostile_guards": hostile_guards,
        },
        "groups": group_rows,
        "lineages": sorted(lineages, key=lambda line: line["lineage_id"]),
        "artifacts": ARTIFACTS,
        "explicit_gaps": [
            "Exactly 22 required K21 IDs remain outside the pinned 30-ID charge results: one terminal-ready hidden [2,2,3] path and 21 K19-parent reconstruction paths.",
            "For 21 IDs the terminal parent is K19 and no prolongable K19 coefficient/profile checkpoint exists. Earlier K19 charge scalars and source-compressed terminal profiles cannot be prolonged.",
            "The raw checkpoint_k17_*.bin files are irreducible normals, not the pivotable K17 parent feeds needed for K19 reconstruction.",
            "Profile checkpoints omit exact-zero signed aggregate keys and retain only single-pivot terminal data; they support the named terminal charge, not later row collection or K22 tails.",
            "The direct 16-ID charge result is independently terminal-refereed but group-aggregated; it supplies three group scalars, not sixteen individual-ID scalars.",
            "No K21 coefficient checkpoint, K22 tail stream, residual assembly, terminal-span test, or conjecture conclusion follows from this availability audit.",
        ],
        "minimal_next_interface_work": [
            {"ids": 1, "action": "Evaluate the retained hidden literal K18 [2,2] pivotable checkpoint at terminal K3."},
            {"ids": 21, "action": "Reconstruct and signed-collect the seven disjoint K19-parent source groups, then evaluate one terminal K2 response per group."},
            {"ids": 52, "action": "Assemble group scalars over Q only after literal 52-ID coverage equality; keep aggregate groups distinct from per-ID scalar claims."},
        ],
        "pinned_metadata": SMALL_PINS,
    }
    result["logical_sha256"] = logical_digest(result)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "classification_counts": result["classification_counts"],
        "availability_counts": result["availability_counts"],
        "logical_sha256": result["logical_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
