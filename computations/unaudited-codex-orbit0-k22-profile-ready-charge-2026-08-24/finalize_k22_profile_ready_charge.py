#!/usr/bin/env python3
"""Independent coverage/arithmetic/hash finalizer for the K22 profile 16."""

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = HERE / "results_k22_profile_ready_charge.raw.json"
FINAL = HERE / "results_k22_profile_ready_charge.json"
AUDIT = HERE / "results_k22_profile_ready_charge_audit.json"
SAMPLE = HERE / "results_k22_profile_literal_sample_referee.json"
SOURCE = HERE / "run_k22_profile_ready_charge.rs"
SAMPLE_SOURCE = HERE / "referee_k22_profile_samples.rs"
U = 400_591_699_200

EXPECTED_IDS = (
    "D14:222|R:4-4",
    "D15:223|R:3-4", "D15:232|R:3-4", "D15:322|R:3-4",
    "D16:224|R:2-4", "D16:233|R:2-4", "D16:242|R:2-4",
    "D16:323|R:2-4", "D16:332|R:2-4", "D16:422|R:2-4",
    "D18:244|R:4", "D18:334|R:4", "D18:343|R:4",
    "D18:424|R:4", "D18:433|R:4", "D18:442|R:4",
)

GROUPS = (
    {
        "name": "direct_D18_R4", "ids": EXPECTED_IDS[10:16],
        "path": "computations/unaudited-codex-orbit0-direct-k18-profile-census-2026-08-23/direct_k18_enriched_profiles.bin",
        "format": "D18MRG1", "header": 256, "record": 72,
        "records": 979_091, "uses": 252_631_784, "tails": 58_745_460,
        "occurrences": 15_157_907_040, "weight": -2_655_476_097_643_708_416_000,
        "charge": 142_345_959_558_237_388_800, "size": 70_494_808,
        "sha256": "d77f2a84f220aad9f52fe81547ab730a6b834005b27e6f47172bb80cf5850da2",
    },
    {
        "name": "D14_R4_4", "ids": EXPECTED_IDS[0:1],
        "path": "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/k14_k4_enriched_profiles.bin",
        "format": "K14MRG1", "header": 256, "record": 104,
        "records": 18_217_226, "uses": 886_145_203, "tails": 1_093_033_560,
        "occurrences": 53_168_712_180, "weight": 496_321_127_773_883_596_800,
        "charge": 31_117_156_531_545_047_040, "size": 1_894_591_760,
        "sha256": "5cc8c15b2333937ddfaefac1ec056b2f2fd899f5b89ea5b0276d374b05d92d7f",
    },
    {
        "name": "grouped_D15_R3_4", "ids": EXPECTED_IDS[1:4],
        "path": "computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/checkpoint_k15_k3_profiles_merged.bin",
        "format": "K15MRG1", "header": 128, "record": 104,
        "records": 25_564_391, "uses": 2_311_887_188, "tails": 1_533_863_460,
        "occurrences": 138_713_231_280, "weight": 1_865_098_870_468_588_339_200,
        "charge": 410_673_513_772_236_718_080, "size": 2_658_696_792,
        "sha256": "8b05f3fb8edcda062111d20089309abb85d4ccd8675d289947178b437139c1db",
    },
    {
        "name": "grouped_D16_R2_4", "ids": EXPECTED_IDS[4:10],
        "path": "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/checkpoint_k16_k2_profiles_merged.bin",
        "format": "K16MRG1", "header": 128, "record": 104,
        "records": 6_876_260, "uses": 1_604_299_948, "tails": 412_575_600,
        "occurrences": 96_257_996_880, "weight": 3_218_269_567_887_566_438_400,
        "charge": 820_249_074_943_630_295_040, "size": 715_131_168,
        "sha256": "d23271184b8258634cbf6f0942c4b1068e04c505e206b08fd3638e1c9b03be03",
    },
)

AUXILIARY = {
    "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin": "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin": "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin": "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    value = sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20):
            value.update(block)
    return value.hexdigest()


def rational(value):
    result = Fraction(value, U)
    return str(result.numerator) if result.denominator == 1 else f"{result.numerator}/{result.denominator}"


def atomic_json(path, value):
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def check_header(spec):
    path = ROOT / spec["path"]
    require(path.stat().st_size == spec["size"] == spec["header"] + spec["record"] * spec["records"], spec["name"])
    with path.open("rb") as stream:
        header = stream.read(spec["header"])
    require(header[:8] == spec["format"].encode() + b"\0", (spec["name"], header[:8]))
    if spec["format"] == "D18MRG1":
        require(int.from_bytes(header[8:24], "little", signed=True) == U, spec["name"])
        require(struct.unpack_from("<HHH", header, 24) == (0, 485, 72), spec["name"])
        require(struct.unpack_from("<Q", header, 176)[0] == spec["records"], spec["name"])
        require(int.from_bytes(header[184:200], "little", signed=True) == spec["weight"], spec["name"])
        require(struct.unpack_from("<Q", header, 200)[0] == spec["uses"], spec["name"])
    elif spec["format"] == "K14MRG1":
        require(struct.unpack_from("<Q", header, 8)[0] == U, spec["name"])
        require(struct.unpack_from("<Q", header, 56)[0] == spec["records"], spec["name"])
        require(struct.unpack_from("<Q", header, 72)[0] == spec["uses"], spec["name"])
        require(int.from_bytes(header[80:96], "little", signed=True) == spec["weight"], spec["name"])
    else:
        require(struct.unpack_from("<IHH", header, 8) == (1, 104, 0), spec["name"])
        require(int.from_bytes(header[16:32], "little", signed=True) == U, spec["name"])
        require(struct.unpack_from("<Q", header, 56)[0] == spec["records"], spec["name"])
        require(struct.unpack_from("<Q", header, 72)[0] == spec["uses"], spec["name"])
        require(int.from_bytes(header[96:112], "little", signed=True) == spec["weight"], spec["name"])


def main():
    raw = json.loads(RAW.read_text())
    require(raw["status"] == "PASS_EXACT_K22_16_PROFILE_READY_77_CHARGE_SUBTOTAL", raw["status"])
    require(int(raw["scale_U"]) == U and raw["workers"] == 8, raw)
    require(raw["coverage"] == {"covered_count": 16, "covered_ids": list(EXPECTED_IDS), "strict_exact_set_guard": True}, raw["coverage"])

    availability = json.loads((ROOT / "computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/results_k22_availability_schedule.json").read_text())
    available_ids = [item["id"] for item in availability["lineages"] if item["availability"] == "TERMINAL_READY_PROFILE_INTERFACE"]
    require(available_ids == list(EXPECTED_IDS), available_ids)
    dag = json.loads((ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json").read_text())
    dag_subset = [item for item in dag["required_reachable_lineage_ids_by_degree"]["22"] if item in set(EXPECTED_IDS)]
    require(dag_subset == list(EXPECTED_IDS), dag_subset)

    input_hashes = {}
    require(len(raw["groups"]) == len(GROUPS) == 4, len(raw["groups"]))
    for actual, expected in zip(raw["groups"], GROUPS, strict=True):
        require(actual["name"] == expected["name"], actual["name"])
        require(tuple(actual["ids"]) == expected["ids"], actual["ids"])
        require(actual["source_profile"] == expected["path"], actual["source_profile"])
        require(actual["source_format"] == expected["format"], actual["source_format"])
        require(actual["target_degree"] == 4, actual)
        require(actual["profile_records"] == expected["records"], actual)
        require(actual["profile_tail_evaluations"] == expected["tails"] == 60 * expected["records"], actual)
        require(actual["irreducible_profile_tail_evaluations"] == expected["tails"], actual)
        require(actual["input_profile_uses"] == expected["uses"], actual)
        require(actual["source_occurrences"] == expected["occurrences"] == 60 * expected["uses"], actual)
        require(int(actual["input_weight_scaled_U"]) == expected["weight"], actual)
        require(int(actual["full_77_charge_scaled_U"]) == expected["charge"], actual)
        require(actual["full_77_charge_scaled_U"] == actual["irreducible_77_charge_scaled_U"], actual)
        require(actual["exhaustive_key_guards"] == expected["records"], actual)
        require(actual["universal_terminal_guards"] == expected["records"], actual)
        require(actual["literal_witness_profile_replays"] == expected["records"], actual)
        require(actual["literal_profile_cycle_comparisons"] > 0, actual)
        check_header(expected)
        actual_hash = digest(ROOT / expected["path"])
        require(actual_hash == expected["sha256"], (expected["path"], actual_hash))
        input_hashes[expected["path"]] = actual_hash

    for relative, expected_hash in AUXILIARY.items():
        actual_hash = digest(ROOT / relative)
        require(actual_hash == expected_hash, (relative, actual_hash))
        input_hashes[relative] = actual_hash

    subtotal = raw["subtotal"]
    expected_charge = sum(group["charge"] for group in GROUPS)
    require(subtotal["covered_DAG_paths"] == 16, subtotal)
    require(subtotal["profile_records"] == sum(group["records"] for group in GROUPS) == 51_636_968, subtotal)
    require(subtotal["profile_tail_evaluations"] == sum(group["tails"] for group in GROUPS) == 3_098_218_080, subtotal)
    require(subtotal["irreducible_profile_tail_evaluations"] == subtotal["profile_tail_evaluations"], subtotal)
    require(int(subtotal["full_77_charge_scaled_U"]) == expected_charge == 1_404_385_704_805_649_448_960, subtotal)
    require(subtotal["full_77_charge_scaled_U"] == subtotal["irreducible_77_charge_scaled_U"], subtotal)
    for field in ("exhaustive_key_guards", "universal_terminal_guards", "literal_witness_profile_replays"):
        require(subtotal[field] == subtotal["profile_records"], (field, subtotal[field]))
    require(subtotal["literal_profile_cycle_comparisons"] == 5_202, subtotal)
    require(raw["elapsed_seconds"] < 600, raw["elapsed_seconds"])

    sample = json.loads(SAMPLE.read_text())
    require(sample["status"] == "PASS_INDEPENDENT_DISTRIBUTED_LITERAL_K22_PROFILE_REFEREE", sample["status"])
    require(sample["samples_per_group"] == 257 and sample["total_distributed_records"] == 1028, sample)
    require(sample["total_literal_K4_tail_checks"] == 61_680, sample)
    require(sample["all_profile_signature_pivot_witnesses_replayed"] is True, sample)
    require(sample["all_sample_children_anchor_sum_2_and_nonpivotable"] is True, sample)
    require([group["name"] for group in sample["groups"]] == [group["name"] for group in GROUPS], sample)
    for group in sample["groups"]:
        require(group["profile_vs_row_checks"] == 257, group)
        require(group["literal_K4_tail_checks"] == group["terminal_child_checks"] == 15_420, group)

    source_hash = digest(SOURCE)
    sample_source_hash = digest(SAMPLE_SOURCE)
    require(source_hash == "b114ac1d48675de3650d69176ac3d44fd723dec84766a8d3ce5ab67576ea6b73", source_hash)
    require(sample_source_hash == "324afefdeedba16f0a904e658a803902038fd15920579a777d6e97c638545215", sample_source_hash)
    raw_hash = digest(RAW)
    sample_hash = digest(SAMPLE)
    require(raw_hash == "b63ef0b563ffc17504a02f6ef10e2ffc4f35b55a9ae68966854bb75726aaf0a5", raw_hash)
    require(sample_hash == "7f67bd8731ac60a32a58142b202e18c019d01d0653101e6b63291e5da744008b", sample_hash)

    final = deepcopy(raw)
    for group in final["groups"]:
        group["full_77_charge_reduced"] = rational(int(group["full_77_charge_scaled_U"]))
        group["irreducible_77_charge_reduced"] = group["full_77_charge_reduced"]
    final["subtotal"]["full_77_charge_reduced"] = rational(expected_charge)
    final["subtotal"]["irreducible_77_charge_reduced"] = final["subtotal"]["full_77_charge_reduced"]
    logical = {
        "scale_U": U,
        "covered_ids": list(EXPECTED_IDS),
        "groups": [{key: group[key] for key in ("name", "ids", "profile_records", "profile_tail_evaluations", "full_77_charge_scaled_U", "irreducible_77_charge_scaled_U")} for group in final["groups"]],
        "subtotal": final["subtotal"],
        "dag_logical_sha256": dag["logical_sha256"],
        "input_sha256": input_hashes,
        "producer_source_sha256": source_hash,
        "sample_referee_sha256": sample_hash,
    }
    logical_hash = sha256(json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    final["provenance"] = {
        "raw_result_sha256": raw_hash,
        "producer_source_sha256": source_hash,
        "sample_referee_source_sha256": sample_source_hash,
        "sample_referee_result_sha256": sample_hash,
        "input_sha256": input_hashes,
        "dag_logical_sha256": dag["logical_sha256"],
        "availability_logical_sha256": availability["logical_sha256"],
        "logical_sha256": logical_hash,
    }
    atomic_json(FINAL, final)
    final_hash = digest(FINAL)

    manifest_groups = []
    final_relative = str(FINAL.relative_to(ROOT))
    for group in final["groups"]:
        manifest_groups.append({
            "ids": group["ids"],
            "full_scaled_U": group["full_77_charge_scaled_U"],
            "irreducible_scaled_U": group["irreducible_77_charge_scaled_U"],
            "full": group["full_77_charge_reduced"],
            "irreducible": group["irreducible_77_charge_reduced"],
            "evidence_path": final_relative,
            "evidence_sha256": final_hash,
        })
    manifest = {"degree": 22, "scale_U": U, "groups": manifest_groups}
    manifest_path = HERE / "k22_manifest_profile16_partial.json"
    atomic_json(manifest_path, manifest)

    assembler_path = ROOT / "computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/assemble_k22_76_exact.py"
    spec = importlib.util.spec_from_file_location("k22_assembler", assembler_path)
    assembler = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(assembler)
    assembled = assembler.assemble(manifest, allow_partial=True)
    require(assembled["status"] == "REJECT_INCOMPLETE_K22_76_ID_GATE", assembled)
    require(assembled["covered_paths"] == 16 and len(assembled["missing_paths"]) == 60, assembled)
    require(assembled["full_scaled_U"] == str(expected_charge), assembled)
    atomic_json(HERE / "results_k22_profile16_60_gap.json", assembled)

    audit = {
        "status": "PASS_INDEPENDENT_K22_PROFILE16_COVERAGE_ARITHMETIC_HASH_LITERAL_AUDIT",
        "covered_count": 16,
        "remaining_K22_ids": 60,
        "covered_ids": list(EXPECTED_IDS),
        "group_count": 4,
        "profile_records": subtotal["profile_records"],
        "profile_tail_evaluations": subtotal["profile_tail_evaluations"],
        "all_K22_tails_irreducible": True,
        "full_77_charge_scaled_U": subtotal["full_77_charge_scaled_U"],
        "irreducible_77_charge_scaled_U": subtotal["irreducible_77_charge_scaled_U"],
        "full_77_charge_reduced": final["subtotal"]["full_77_charge_reduced"],
        "irreducible_77_charge_reduced": final["subtotal"]["irreducible_77_charge_reduced"],
        "raw_result_sha256": raw_hash,
        "final_result_sha256": final_hash,
        "producer_source_sha256": source_hash,
        "literal_sample_referee_sha256": sample_hash,
        "logical_sha256": logical_hash,
        "input_sha256": input_hashes,
        "checks": [
            "exact ordered equality with the 16 profile-ready IDs in the sealed K22 availability ledger and frozen DAG",
            "four source headers, geometries, complete SHA-256 pins, signs, U, weights, uses, record and tail counts",
            "per-group and subtotal exact scaled/rational arithmetic; grouped scalars counted once",
            "full equals irreducible by universal anchor-sum 2<4 terminality",
            "exhaustive producer witness/profile/signature/pivot guards on all 51,636,968 records and 5,202 literal cycle comparisons",
            "independent 257 distributed literal rows per group, all 60 K4 tails each: 61,680 literal charge and terminal-child checks",
            "strict K22 assembler accepts the exact 16-ID partial and reports exactly 60 missing without a complete claim",
        ],
    }
    atomic_json(AUDIT, audit)
    print(json.dumps({"status": audit["status"], "final_result_sha256": final_hash, "logical_sha256": logical_hash, "charge": audit["full_77_charge_reduced"]}, indent=2))


if __name__ == "__main__":
    main()
