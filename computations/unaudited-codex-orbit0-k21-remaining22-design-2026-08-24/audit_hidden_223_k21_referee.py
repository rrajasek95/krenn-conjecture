#!/usr/bin/env python3
"""Independent retained-path referee for the singleton hidden K21 scalar.

This intentionally does not stream the 158,439,965-record input.  The Rust
companion performs 257 distributed random-access literal replays and proves
terminality at signature level; this layer pins the landed artifacts and
checks their complete grouped arithmetic and strict lineage interface.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "run_k21_hidden_223_charge.rs"
RESULT = HERE / "results_hidden_223_k21_charge.json"
SAMPLES = HERE / "results_hidden_223_k21_charge.json.samples.tsv"
RUST_AUDIT = HERE / "audit_hidden_223_k21_referee.rs"
RUST_RESULT = HERE / "results_hidden_223_k21_referee_samples.json"
OUTPUT = HERE / "results_hidden_223_k21_referee.json"
DAG = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
INPUT = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin"
INPUT_PINS = INPUT.with_name("CHECKPOINTS.sha256")
INPUT_REFEREE = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-final-referee-2026-08-23/results_final_merge_referee_final.json"

LINEAGE = "D14:222|R:2-2-3"
U = 400_591_699_200
PARENTS = 158_439_965
MASS = 724_159_651_336_720_220_160
PIVOTS = 399_275_484
CHILDREN = 12_776_815_488
CHARGE = -1_965_744_419_617_576_058_880
REDUCED = Fraction(-511_912_609_275_410_432, 104_320_755)

EXPECTED_SHA256 = {
    "producer_source": "3a9d6f821e72d9782311b3e96378134df203099f3ef04d4c9f4b741d07c7062a",
    "producer_result": "3bff6d8b0bcb7fc2c3508ab69f18d8df60f5d5ffa0aead0db33d3b40c677313d",
    "producer_samples": "768e8e877e2d278be14563cf4ae78f7e4599c1e6a197389447f24763ce01be33",
    "input": "442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8",
    "input_referee": "14e636d297847c850f1417601a396e73fc9514c2eb8810ffe42367a38776a23a",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def logical_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def require_strict_singleton(ids: list[str]) -> None:
    assert ids == [LINEAGE], f"not the exact singleton interface: {ids!r}"


def main() -> None:
    assert sha256(SOURCE) == EXPECTED_SHA256["producer_source"]
    assert sha256(RESULT) == EXPECTED_SHA256["producer_result"]
    assert sha256(SAMPLES) == EXPECTED_SHA256["producer_samples"]
    assert sha256(INPUT_REFEREE) == EXPECTED_SHA256["input_referee"]

    pins = {
        name: digest
        for digest, name in (
            line.split(maxsplit=1) for line in INPUT_PINS.read_text().splitlines()
        )
    }
    assert pins[INPUT.name] == EXPECTED_SHA256["input"]
    # The 12.7 GB input is not rehashed or restreamed here: this exact pin was
    # previously frozen and independently full-scan refereed.
    assert INPUT.stat().st_size == 80 + 80 * PARENTS
    input_referee = json.loads(INPUT_REFEREE.read_text())
    assert input_referee["status"] == "PASS_INDEPENDENT_FINAL_K18_REFEREE"
    assert input_referee["logical_sha256"] == "9b2ab638c40cb0145814e86e55520884abc9ef0ea55d80bb76174fe4b094bca2"

    dag = json.loads(DAG.read_text())
    required_k21 = dag["required_reachable_lineage_ids_by_degree"]["21"]
    assert len(required_k21) == len(set(required_k21)) == 52
    assert LINEAGE in required_k21

    source = SOURCE.read_text()
    required_source_fragments = [
        "assert_eq!(U % ((x.m2 as i128) * m3), 0);",
        "assert_eq!(x.weight_before_p3 % m3, 0);",
        "(pivots, -x.weight_before_p3 / m3)",
        "profile: path_profile(&x.row, p3, e, c)",
        "sig,",
        "pivot: p3 as u8",
        "out.value += w3 * z.full_q as i128;",
        "assert_eq!(z.full_n, 32);",
        "z.irr_n = z.full_n;",
        "z.irr_q = z.full_q;",
    ]
    for fragment in required_source_fragments:
        assert fragment in source, fragment

    result = json.loads(RESULT.read_text())
    require_strict_singleton([result["lineage_id"]])
    # Hostile guard: missing, duplicate, or adjacent lineage IDs must fail.
    hostile = [[], [LINEAGE, LINEAGE], ["D14:222|R:2-3"]]
    for ids in hostile:
        try:
            require_strict_singleton(ids)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"hostile singleton interface accepted: {ids!r}")

    assert result["status"] == "PASS_COMPLETE_D14_222_R_2_2_3_K21_CHARGE"
    assert int(result["scale_U"]) == U
    assert result["input_records_consumed"] == result["input_records_declared"] == PARENTS
    assert int(result["input_weight_sum_scaled"]) == MASS
    assert result["selected_p3_uses"] == PIVOTS
    assert result["K3_tail_occurrences"] == CHILDREN == 32 * PIVOTS
    assert result["full_occurrences"] == result["irreducible_occurrences"] == CHILDREN
    assert int(result["full_charge_scaled"]) == int(result["irreducible_charge_scaled"]) == CHARGE

    grouped = result["m2_m3_provenance"]
    assert len(grouped) == 33
    sums = {"parents": 0, "mass": 0, "pivots": 0, "children": 0, "charge": 0}
    for key, group in grouped.items():
        m2, m3 = map(int, key.split("_"))
        assert m2 > 0 and m3 > 0
        assert U % (m2 * m3) == 0
        assert group["pivot_uses"] == group["parents"] * m3
        assert group["K3_children"] == 32 * group["pivot_uses"]
        sums["parents"] += group["parents"]
        sums["mass"] += int(group["signed_parent_mass_scaled"])
        sums["pivots"] += group["pivot_uses"]
        sums["children"] += group["K3_children"]
        sums["charge"] += int(group["charge_scaled"])
    assert sums == {
        "parents": PARENTS,
        "mass": MASS,
        "pivots": PIVOTS,
        "children": CHILDREN,
        "charge": CHARGE,
    }

    cache = result["response_cache"]
    assert cache["misses"] == cache["distinct_keys"] == 5_173_958
    assert cache["hits"] + cache["misses"] == PIVOTS
    assert Fraction(CHARGE, U) == REDUCED

    literal = json.loads(RUST_RESULT.read_text())
    assert literal["status"] == "PASS_INDEPENDENT_257_LITERAL_HIDDEN_223_K21_REFEREE"
    require_strict_singleton([literal["lineage_id"]])
    assert literal["input_header"] == {
        "magic": "H18PIV2",
        "scale_U": str(U),
        "record_bytes": 80,
        "pair_orbits": 101_545_723,
        "prior_K2_children": 1_218_548_676,
        "records": PARENTS,
        "flag": 1,
        "signed_mass_scaled": str(MASS),
        "exact_file_size": 80 + 80 * PARENTS,
    }
    theorem = literal["universal_terminality"]
    assert theorem == {
        "pivot_signatures": 78,
        "pivot_anchor_sum": 4,
        "K3_tail_families": 78,
        "K3_tails_checked": 2_496,
        "K3_tail_anchor_sum": 1,
        "K18_parent_anchor_sum": 6,
        "K21_child_anchor_sum": 3,
        "all_K21_children_nonpivotable": True,
    }
    sample = literal["literal_sample"]
    assert sample["parents"] == sample["witness_to_canonical_K18_replays"] == 257
    assert (sample["first_index"], sample["last_index"]) == (0, PARENTS - 1)
    assert sample["K3_children"] == sample["literal_abstract_cycle_key_matches"]
    assert sample["K3_children"] == sample["child_signature_terminality_checks"]
    assert sample["K3_children"] == 32 * sample["pivots"]
    sample_cache = literal["sample_cache"]
    assert sample_cache["query_identity_pass"] is True
    assert sample_cache["hits"] + sample_cache["misses"] == sample["pivots"]
    assert sample_cache["misses"] == sample_cache["distinct_keys"]

    referee = {
        "status": "PASS_INDEPENDENT_TERMINAL_REFEREE_D14_222_R_2_2_3_K21_CHARGE",
        "strict_covered_lineage_ids": [LINEAGE],
        "strict_singleton_hostile_guard": {
            "missing_rejected": True,
            "duplicate_rejected": True,
            "adjacent_id_rejected": True,
            "member_of_exact_52_id_K21_DAG": True,
        },
        "charge": {
            "scale_U": U,
            "full_scaled": str(CHARGE),
            "irreducible_scaled": str(CHARGE),
            "full_equals_irreducible": True,
            "reduced": str(REDUCED),
            "reduced_numerator": REDUCED.numerator,
            "reduced_denominator": REDUCED.denominator,
        },
        "complete_grouped_arithmetic": {
            "m2_m3_groups": len(grouped),
            "input_parent_orbits": PARENTS,
            "signed_input_mass_scaled": str(MASS),
            "selected_p3_uses": PIVOTS,
            "K3_tail_occurrences": CHILDREN,
            "all_U_mod_m2_m3_zero": True,
            "all_group_pivot_uses_equal_parents_times_m3": True,
            "all_group_children_equal_32_times_pivots": True,
            "group_charge_sum_scaled": str(CHARGE),
        },
        "recurrence_and_cache_audit": {
            "third_response_sign": "w3=-w2/m3",
            "input_w2_already_signed": True,
            "cache_key": ["profile29", "signature12", "pivot"],
            "cached_value_is_unweighted": True,
            "parent_w3_applied_after_lookup": True,
            "distinct_keys": cache["distinct_keys"],
            "hits": cache["hits"],
            "misses": cache["misses"],
            "hits_plus_misses_equal_selected_p3_uses": True,
        },
        "terminality_proof": {
            "identity": "K21 anchor sum = K18 anchor sum 6 - pivot sum 4 + K3 tail sum 1 = 3",
            "K0_pivots_all_have_anchor_sum": 4,
            "universal_pivot_signatures_checked": 78,
            "universal_K3_tails_checked": 2496,
            "therefore_all_K21_outputs_terminal": True,
        },
        "independent_literal_replay": {
            "sampling": "257 evenly distributed random-access checkpoint records including both endpoints",
            **sample,
            "sample_cache": sample_cache,
        },
        "input_header": literal["input_header"],
        "sha256": {
            **EXPECTED_SHA256,
            "recurrence_dag": sha256(DAG),
            "rust_referee_source": sha256(RUST_AUDIT),
            "rust_referee_result": sha256(RUST_RESULT),
        },
        "scope": "Exact retained singleton only; no full 158439965-parent replay, no inference to the other 21 missing K21 lineages, no residual/conjecture verdict.",
    }
    referee["logical_sha256"] = logical_sha256(referee)
    OUTPUT.write_text(json.dumps(referee, indent=2, sort_keys=True) + "\n")
    print(json.dumps(referee, sort_keys=True))


if __name__ == "__main__":
    main()
