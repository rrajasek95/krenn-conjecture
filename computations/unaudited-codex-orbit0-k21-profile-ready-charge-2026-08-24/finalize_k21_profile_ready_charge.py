#!/usr/bin/env python3
"""Coverage/arithmetic/hash referee for the exact 14-path K21 charge run.

This deliberately does not regenerate rows or reevaluate the 3.4 billion
profile tails.  The Rust producer performs exhaustive key/witness guards and
literal profile/cycle comparisons; this referee independently pins its five
frozen inputs and checks the complete result ledger exactly.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = HERE / "results_k21_profile_ready_charge.raw.json"
FINAL = HERE / "results_k21_profile_ready_charge.json"
AUDIT = HERE / "results_k21_profile_ready_charge_audit.json"
SOURCE = HERE / "run_k21_profile_ready_charge.rs"
U = 400_591_699_200

EXPECTED_IDS = (
    "D14:222|R:3-4", "D14:222|R:4-3",
    "D15:223|R:2-4", "D15:232|R:2-4", "D15:322|R:2-4",
    "D15:223|R:3-3", "D15:232|R:3-3", "D15:322|R:3-3",
    "D16:224|R:2-3", "D16:233|R:2-3", "D16:242|R:2-3",
    "D16:323|R:2-3", "D16:332|R:2-3", "D16:422|R:2-3",
)

GROUPS = (
    {
        "name": "D14_R3_to_K4",
        "ids": EXPECTED_IDS[0:1],
        "path": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/weights_k17_k14_k2.bin",
        "format": "K19SUM1", "stored": 2, "target": 4,
        "records": 13_844_092, "full": 830_645_520,
        "charge": -79_090_847_743_946_784_768,
        "sha256": "34fdbffd1331035831dc86f2eb5ddf0183f5adba1300868248c4023916feee66",
        "size": 816_801_444,
    },
    {
        "name": "D14_R4_to_K3",
        "ids": EXPECTED_IDS[1:2],
        "path": "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/k14_k4_enriched_profiles.bin",
        "format": "K14MRG1", "stored": 4, "target": 3,
        "records": 18_217_226, "full": 582_951_232,
        "charge": -91_407_703_075_561_635_840,
        "sha256": "5cc8c15b2333937ddfaefac1ec056b2f2fd899f5b89ea5b0276d374b05d92d7f",
        "size": 1_894_591_760,
    },
    {
        "name": "D15_R2_to_K4",
        "ids": EXPECTED_IDS[2:5],
        "path": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/weights_k17_k15_k2.bin",
        "format": "K19SUM1", "stored": 2, "target": 4,
        "records": 16_109_793, "full": 966_587_580,
        "charge": -257_936_332_936_328_183_808,
        "sha256": "864b3cac1230047db3200a4560d5ce3240747c9e89d0f4cfd5a8fe1236235b1d",
        "size": 950_477_803,
    },
    {
        "name": "D15_R3_to_K3",
        "ids": EXPECTED_IDS[5:8],
        "path": "computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/checkpoint_k15_k3_profiles_merged.bin",
        "format": "K15MRG1", "stored": 3, "target": 3,
        "records": 25_564_391, "full": 818_060_512,
        "charge": -1_658_448_665_087_993_856_000,
        "sha256": "8b05f3fb8edcda062111d20089309abb85d4ccd8675d289947178b437139c1db",
        "size": 2_658_696_792,
    },
    {
        "name": "D16_R2_to_K3",
        "ids": EXPECTED_IDS[8:14],
        "path": "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/checkpoint_k16_k2_profiles_merged.bin",
        "format": "K16MRG1", "stored": 2, "target": 3,
        "records": 6_876_260, "full": 220_040_320,
        "charge": -2_300_567_952_933_858_263_040,
        "sha256": "d23271184b8258634cbf6f0942c4b1068e04c505e206b08fd3638e1c9b03be03",
        "size": 715_131_168,
    },
)

AUXILIARY = {
    "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin":
        "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin":
        "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin":
        "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20):
            h.update(block)
    return h.hexdigest()


def rational(value: int) -> str:
    q = Fraction(value, U)
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def check_header(spec: dict) -> None:
    path = ROOT / spec["path"]
    require(path.stat().st_size == spec["size"], (path, path.stat().st_size))
    with path.open("rb") as stream:
        header = stream.read(256)
    if spec["format"] == "K19SUM1":
        require(header[:8] == b"K19SUM1\0", header[:8])
        require(struct.unpack_from("<Q", header, 8)[0] == spec["records"], spec["name"])
        require(spec["size"] == 16 + 59 * spec["records"], spec["name"])
    elif spec["format"] == "K14MRG1":
        require(header[:8] == b"K14MRG1\0", header[:8])
        require(struct.unpack_from("<Q", header, 8)[0] == U, spec["name"])
        require(struct.unpack_from("<Q", header, 56)[0] == spec["records"], spec["name"])
        require(spec["size"] == 256 + 104 * spec["records"], spec["name"])
    else:
        require(header[:8] == spec["format"].encode() + b"\0", header[:8])
        require(struct.unpack_from("<q", header, 16)[0] == U, spec["name"])
        require(struct.unpack_from("<Q", header, 56)[0] == spec["records"], spec["name"])
        require(spec["size"] == 128 + 104 * spec["records"], spec["name"])


def main() -> None:
    raw = json.loads(RAW.read_text())
    require(raw["status"] == "PASS_EXACT_K21_14_PROFILE_READY_77_CHARGE_SUBTOTAL", raw["status"])
    require(int(raw["scale_U"]) == U, raw["scale_U"])
    require(int(raw["old_weight_scale"]) == 281_801_520 ** 2, raw["old_weight_scale"])
    require(raw["weight_scale_ratio"] == 198_237, raw["weight_scale_ratio"])
    coverage = raw["coverage"]
    require(coverage["covered_count"] == len(EXPECTED_IDS) == 14, coverage)
    require(tuple(coverage["covered_ids"]) == EXPECTED_IDS, coverage["covered_ids"])
    require(len(set(coverage["covered_ids"])) == 14 and coverage["strict_exact_set_guard"] is True, coverage)
    require(len(raw["groups"]) == len(GROUPS) == 5, len(raw["groups"]))

    input_hashes = {}
    for actual, expected in zip(raw["groups"], GROUPS, strict=True):
        require(actual["name"] == expected["name"], actual["name"])
        require(tuple(actual["ids"]) == expected["ids"], actual["ids"])
        require(actual["source_profile"] == expected["path"], actual["source_profile"])
        require(actual["source_format"] == expected["format"], actual["source_format"])
        require((actual["stored_degree"], actual["target_degree"]) ==
                (expected["stored"], expected["target"]), actual)
        require(actual["profile_records"] == expected["records"], actual["profile_records"])
        require(actual["profile_tail_evaluations"] == expected["full"], actual["profile_tail_evaluations"])
        require(actual["irreducible_profile_tail_evaluations"] == expected["full"], actual)
        require(int(actual["full_77_charge_scaled_U"]) == expected["charge"], actual)
        require(int(actual["irreducible_77_charge_scaled_U"]) == expected["charge"], actual)
        require(actual["exhaustive_key_guards"] == expected["records"], actual)
        check_header(expected)
        actual_hash = digest(ROOT / expected["path"])
        require(actual_hash == expected["sha256"], (expected["path"], actual_hash))
        input_hashes[expected["path"]] = actual_hash

    for relative, expected_hash in AUXILIARY.items():
        actual_hash = digest(ROOT / relative)
        require(actual_hash == expected_hash, (relative, actual_hash))
        input_hashes[relative] = actual_hash

    subtotal = raw["subtotal"]
    sums = {
        "profile_records": sum(group["profile_records"] for group in raw["groups"]),
        "profile_tail_evaluations": sum(group["profile_tail_evaluations"] for group in raw["groups"]),
        "irreducible_profile_tail_evaluations": sum(group["irreducible_profile_tail_evaluations"] for group in raw["groups"]),
        "full_77_charge_scaled_U": sum(int(group["full_77_charge_scaled_U"]) for group in raw["groups"]),
        "irreducible_77_charge_scaled_U": sum(int(group["irreducible_77_charge_scaled_U"]) for group in raw["groups"]),
        "exhaustive_key_guards": sum(group["exhaustive_key_guards"] for group in raw["groups"]),
        "literal_witness_profile_replays": sum(group["literal_witness_profile_replays"] for group in raw["groups"]),
        "literal_profile_cycle_comparisons": sum(group["literal_profile_cycle_comparisons"] for group in raw["groups"]) + raw["global_literal_profile_cycle_selftest"],
    }
    for key, expected in sums.items():
        actual = int(subtotal[key])
        require(actual == expected, (key, actual, expected))
    require(subtotal["covered_DAG_paths"] == 14, subtotal)
    require(subtotal["profile_records"] == 80_611_762, subtotal)
    require(subtotal["profile_tail_evaluations"] == 3_418_285_164, subtotal)
    require(subtotal["irreducible_profile_tail_evaluations"] == 3_418_285_164, subtotal)
    require(int(subtotal["full_77_charge_scaled_U"]) == -4_387_451_501_777_688_723_456, subtotal)
    require(subtotal["full_77_charge_scaled_U"] == subtotal["irreducible_77_charge_scaled_U"], subtotal)
    require(subtotal["exhaustive_key_guards"] == 80_611_762, subtotal)
    require(subtotal["literal_witness_profile_replays"] == 50_657_877, subtotal)
    require(subtotal["literal_profile_cycle_comparisons"] == 86_733, subtotal)

    source_hash = digest(SOURCE)
    require(source_hash == "cb0fc33783de0777ee65a9405e082b23baff222b7b08bd4faccca4b1853754ed", source_hash)
    raw_hash = digest(RAW)
    final = deepcopy(raw)
    for group in final["groups"]:
        group["full_77_charge_reduced"] = rational(int(group["full_77_charge_scaled_U"]))
        group["irreducible_77_charge_reduced"] = rational(int(group["irreducible_77_charge_scaled_U"]))
    final["subtotal"]["full_77_charge_reduced"] = rational(int(subtotal["full_77_charge_scaled_U"]))
    final["subtotal"]["irreducible_77_charge_reduced"] = rational(int(subtotal["irreducible_77_charge_scaled_U"]))
    logical = {
        "scale_U": U,
        "covered_ids": list(EXPECTED_IDS),
        "groups": [
            {key: group[key] for key in (
                "name", "ids", "stored_degree", "target_degree", "profile_records",
                "profile_tail_evaluations", "irreducible_profile_tail_evaluations",
                "full_77_charge_scaled_U", "irreducible_77_charge_scaled_U")}
            for group in final["groups"]
        ],
        "subtotal": final["subtotal"],
        "input_sha256": input_hashes,
        "producer_source_sha256": source_hash,
    }
    logical_hash = sha256(json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    final["provenance"] = {
        "raw_result_sha256": raw_hash,
        "producer_source_sha256": source_hash,
        "input_sha256": input_hashes,
        "logical_sha256": logical_hash,
    }
    atomic_json(FINAL, final)
    final_hash = digest(FINAL)
    audit = {
        "status": "PASS_INDEPENDENT_K21_PROFILE_READY_COVERAGE_ARITHMETIC_HASH_AUDIT",
        "covered_count": 14,
        "covered_ids": list(EXPECTED_IDS),
        "group_count": 5,
        "profile_records": subtotal["profile_records"],
        "profile_tail_evaluations": subtotal["profile_tail_evaluations"],
        "all_K21_tails_irreducible": True,
        "full_77_charge_scaled_U": subtotal["full_77_charge_scaled_U"],
        "irreducible_77_charge_scaled_U": subtotal["irreducible_77_charge_scaled_U"],
        "full_77_charge_reduced": final["subtotal"]["full_77_charge_reduced"],
        "irreducible_77_charge_reduced": final["subtotal"]["irreducible_77_charge_reduced"],
        "raw_result_sha256": raw_hash,
        "final_result_sha256": final_hash,
        "producer_source_sha256": source_hash,
        "logical_sha256": logical_hash,
        "input_sha256": input_hashes,
        "checks": [
            "strict ordered 14-ID set equality and uniqueness",
            "five source-interface path/degree assignments",
            "frozen source sizes, headers, and SHA-256 hashes",
            "per-group pinned counts and signed charges",
            "exact group-to-subtotal arithmetic",
            "full equals irreducible for every group and subtotal",
            "exhaustive key/replay/comparison counters",
        ],
        "scope": "independent coverage/arithmetic/header/hash audit; the 3.4-billion-tail charge evaluation and literal profile/cycle guards are performed by the pinned Rust producer",
    }
    atomic_json(AUDIT, audit)
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
