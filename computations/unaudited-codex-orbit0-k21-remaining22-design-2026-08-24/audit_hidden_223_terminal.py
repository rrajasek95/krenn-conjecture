#!/usr/bin/env python3
"""Independent package/arithmetic referee for D14:222|R:2-2-3 at K21."""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "run_k21_hidden_223_charge.rs"
RESULT = HERE / "results_hidden_223_k21_charge.json"
SAMPLES = HERE / "results_hidden_223_k21_charge.json.samples.tsv"
OUT = HERE / "results_hidden_223_terminal_referee.json"
INPUT = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin"
PINS = INPUT.with_name("CHECKPOINTS.sha256")
LANDED = ROOT / "computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23/results_landed_checkpoint_validation.json"

EXPECTED = {
    "source": "3a9d6f821e72d9782311b3e96378134df203099f3ef04d4c9f4b741d07c7062a",
    "result": "3bff6d8b0bcb7fc2c3508ab69f18d8df60f5d5ffa0aead0db33d3b40c677313d",
    "samples": "768e8e877e2d278be14563cf4ae78f7e4599c1e6a197389447f24763ce01be33",
    "pins": "3a8f14e7daf0620c5f4e09e1928f286857d8c3d77c6051570135aa8f13134c85",
    "landed": "6b75445fbfcca74c7d5017c17de95a8ec7af2acd07db9ecf0ad764a9bd810a5f",
    "input": "442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8",
}
U = 400_591_699_200
N = 158_439_965
PIVOTS = 399_275_484
CHILDREN = 12_776_815_488
MASS = 724_159_651_336_720_220_160
CHARGE = -1_965_744_419_617_576_058_880


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def logical_digest(value) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def main() -> None:
    assert sha(SOURCE) == EXPECTED["source"]
    assert sha(RESULT) == EXPECTED["result"]
    assert sha(SAMPLES) == EXPECTED["samples"]
    assert sha(PINS) == EXPECTED["pins"]
    assert sha(LANDED) == EXPECTED["landed"]
    assert INPUT.stat().st_size == 80 + 80 * N
    pin_map = {
        name: digest
        for digest, name in (line.split(maxsplit=1) for line in PINS.read_text().splitlines())
    }
    assert pin_map[INPUT.name] == EXPECTED["input"]

    landed = json.loads(LANDED.read_text())
    assert landed["status"] == "PASS_H18_CHECKPOINT_CONSUMER_SCHEMA"
    assert landed["pivotable"]["count"] == N
    assert int(landed["pivotable"]["weight_sum_scaled"]) == MASS
    assert landed["full_order_scan"] is True
    assert landed["full_mass_recomputed"] is True

    source = SOURCE.read_text()
    assert "response3_abstract_k21" in source
    assert "!pivotable_sig(" in source and "child_sig(" in source
    assert "realized abstract K21 response key remained pivotable" in source
    assert "assert_eq!(x.weight_before_p3 % m3, 0)" in source
    assert "assert_eq!(total.pivot_uses, EXPECTED_PIVOT_USES)" in source

    result = json.loads(RESULT.read_text())
    assert result["status"] == "PASS_COMPLETE_D14_222_R_2_2_3_K21_CHARGE"
    assert result["lineage_id"] == "D14:222|R:2-2-3"
    assert int(result["scale_U"]) == U
    assert result["input_records_consumed"] == result["input_records_declared"] == N
    assert int(result["input_weight_sum_scaled"]) == MASS
    assert result["selected_p3_uses"] == PIVOTS
    assert result["K3_tail_occurrences"] == 32 * PIVOTS == CHILDREN
    assert result["full_occurrences"] == result["irreducible_occurrences"] == CHILDREN
    assert int(result["full_charge_scaled"]) == int(result["irreducible_charge_scaled"]) == CHARGE
    cache = result["response_cache"]
    assert cache["hits"] + cache["misses"] == PIVOTS
    assert cache["distinct_keys"] == cache["misses"] == 5_173_958

    prov = list(result["m2_m3_provenance"].items())
    assert sum(v["parents"] for _, v in prov) == N
    assert sum(int(v["signed_parent_mass_scaled"]) for _, v in prov) == MASS
    assert sum(v["pivot_uses"] for _, v in prov) == PIVOTS
    assert sum(v["K3_children"] for _, v in prov) == CHILDREN
    assert sum(int(v["charge_scaled"]) for _, v in prov) == CHARGE
    for key, value in prov:
        m2, m3 = map(int, key.split("_"))
        assert U % (m2 * m3) == 0
        assert value["K3_children"] == 32 * value["pivot_uses"]

    rows = SAMPLES.read_text().splitlines()
    assert len(rows) == 258
    header = rows[0].split("\t")
    records = [dict(zip(header, row.split("\t"), strict=True)) for row in rows[1:]]
    indices = [int(row["input_index"]) for row in records]
    assert indices == [j * (N - 1) // 256 for j in range(257)]
    for row in records:
        assert len(row["row"]) == len(row["witness_pair"]) == 48
        assert int(row["pivot_uses"]) == int(row["m3"])
        assert int(row["K3_children"]) == 32 * int(row["m3"])
        assert int(row["pair_uses"]) > 0
        assert int(row["orbit"]) * int(row["stabilizer"]) == 384
        assert U % (int(row["m2"]) * int(row["m3"])) == 0

    reduced = Fraction(CHARGE, U)
    assert math.gcd(abs(reduced.numerator), reduced.denominator) == 1
    assert (reduced.numerator, reduced.denominator) == (
        -511_912_609_275_410_432,
        104_320_755,
    )
    referee = {
        "status": "PASS_INDEPENDENT_D14_222_R_2_2_3_K21_TERMINAL_REFEREE",
        "lineage_id": result["lineage_id"],
        "scale_U": U,
        "full_equals_irreducible": True,
        "exhaustive_abstract_terminality_guard": {
            "realized_cache_keys": cache["distinct_keys"],
            "K3_tails_checked_per_key": 32,
            "abstract_child_signature_checks": 32 * cache["distinct_keys"],
            "source_assertion_pinned": True,
        },
        "literal_sample_guard": {
            "parents": len(records),
            "spaced_first_index": indices[0],
            "spaced_last_index": indices[-1],
            "source_reports_literal_abstract_key_equality": True,
            "source_reports_all_literal_K21_children_nonpivotable": True,
        },
        "counts": {
            "input_parent_orbits": N,
            "selected_p3_uses": PIVOTS,
            "K3_tail_occurrences": CHILDREN,
            "response_cache_keys": cache["distinct_keys"],
        },
        "charge": {
            "scaled": str(CHARGE),
            "reduced_numerator": reduced.numerator,
            "reduced_denominator": reduced.denominator,
            "reduced": str(reduced),
        },
        "input_authority": {
            "path": str(INPUT.relative_to(ROOT)),
            "bytes": INPUT.stat().st_size,
            "sha256_from_independently_frozen_manifest": EXPECTED["input"],
            "manifest_sha256": EXPECTED["pins"],
            "prior_full_scan_referee": str(LANDED.relative_to(ROOT)),
            "prior_full_scan_referee_sha256": EXPECTED["landed"],
        },
        "package_sha256": {
            "source": EXPECTED["source"],
            "result": EXPECTED["result"],
            "samples": EXPECTED["samples"],
        },
        "scope": "Independent package, exact arithmetic, terminality-source, and sample-ledger audit; does not independently reevaluate all cycle-profile keys.",
    }
    referee["logical_sha256"] = logical_digest(referee)
    OUT.write_text(json.dumps(referee, indent=2, sort_keys=True) + "\n")
    print(json.dumps(referee, sort_keys=True))


if __name__ == "__main__":
    main()
