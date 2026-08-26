#!/usr/bin/env python3
"""Independent hostile audit of the grouped direct-K15 four-sink K22 fragment."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter, defaultdict
from fractions import Fraction
from math import prod
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
NAMES = (
    "D15:{223,232,322}|R:4-3",
    "D15:{223,232,322}|R:2-2-3",
    "D15:{223,232,322}|R:2-3-2",
    "D15:{223,232,322}|R:3-2-2",
)
PATHS = {
    NAMES[0]: (4, 3),
    NAMES[1]: (2, 2, 3),
    NAMES[2]: (2, 3, 2),
    NAMES[3]: (3, 2, 2),
}
IDS = {
    name: [f"D15:{packet}|R:{name.rsplit(':', 1)[1]}" for packet in ("223", "232", "322")]
    for name in NAMES
}
EXPECTED = {
    NAMES[0]: {
        "piv": [55_934_080, 1_951_795_200, 0],
        "cand": [3_356_044_800, 62_457_446_400, 0],
        "pivable": [1_225_459_200, 0],
        "terminal": 62_457_446_400,
        "scaled": 208_523_010_296_453_529_600,
        "charge": "921871950848/1771",
    },
    NAMES[1]: {
        "piv": [55_934_080, 1_876_057_600, 11_437_867_520],
        "cand": [671_208_960, 22_512_691_200, 366_011_760_640],
        "pivable": [451_445_760, 6_774_666_240],
        "terminal": 366_011_760_640,
        "scaled": 2_213_434_782_746_883_514_368,
        "charge": "29111884242777824/5268725",
    },
    NAMES[2]: {
        "piv": [55_934_080, 1_876_057_600, 5_972_592_640],
        "cand": [671_208_960, 60_033_843_200, 71_671_111_680],
        "pivable": [451_445_760, 5_972_592_640],
        "terminal": 71_671_111_680,
        "scaled": 397_889_178_859_017_584_640,
        "charge": "1046636097587904/1053745",
    },
    NAMES[3]: {
        "piv": [55_934_080, 2_358_046_720, 3_220_213_760],
        "cand": [1_789_890_560, 28_296_560_640, 38_642_565_120],
        "pivable": [923_253_760, 3_220_213_760],
        "terminal": 38_642_565_120,
        "scaled": 397_229_342_071_225_466_880,
        "charge": "19470194083264/19635",
    },
}
PINS = {
    "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs": "24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin": "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin": "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin": "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin": "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    f"{HERE.relative_to(ROOT)}/run_k22_direct_k15_four_sink.rs": "9a5599da22dbac007e80da8b3d38062257aad6084e9dbe8bfa14c0b62c0b6f3b",
    f"{HERE.relative_to(ROOT)}/assemble_k22_direct_k15_four_sink.py": "defeca4fcd48ae6815cb2d3346eb38dcc5de3a940fe6de7785cfa123f6a5b7be",
    f"{HERE.relative_to(ROOT)}/referee_k22_direct_k15_literal.rs": "7bdc222bff5c9b0047bc05415e7071f523fc83842a3927b4efd66512211a4b87",
    f"{HERE.relative_to(ROOT)}/results_shard_00.json": "4a071a49705c89375343628e1889de2892e9ebe90d28be304ffed33ca1962163",
    f"{HERE.relative_to(ROOT)}/results_shard_01.json": "e4ca50de6df955e68afd487f7046bdabb1dac9d0afdbdf9c432d2c218bb8d09e",
    f"{HERE.relative_to(ROOT)}/results_shard_02.json": "a9a920f6ca2a9f92cb48403c8a66cee451cd053de93082c65ce79c7bee7aabe4",
    f"{HERE.relative_to(ROOT)}/results_shard_03.json": "ea26f855b4e78bc2545d64f5d7ae28814a5dacf75f13db31b96f02c3e9bb212e",
    f"{HERE.relative_to(ROOT)}/results_k22_direct_k15_four_sink.json": "50ea88f5da6921db8017f9e2e7e143cc6d0426ddaeb2a6daf8050a07ac33e5da",
    f"{HERE.relative_to(ROOT)}/results_k22_direct_k15_literal_referee.json": "c989e6804c0bc74ccda92999d9976824e85e6484c0747c28f56068c9fb3498de",
    f"{HERE.relative_to(ROOT)}/k22_direct_k15_literal_samples.tsv": "ab93c4e9c4b3718ea248098ed56572712e3c863e96c13fa823857dfb05303dd6",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for rel, expected in PINS.items():
        assert sha(ROOT / rel) == expected, rel

    result = json.loads((HERE / "results_k22_direct_k15_four_sink.json").read_text())
    referee = json.loads((HERE / "results_k22_direct_k15_literal_referee.json").read_text())
    assert result["status"] == "PASS_COMPLETE_GROUPED_DIRECT_K15_FOUR_SINK_K22_CHARGE"
    assert result["scale_U"] == str(U)
    assert result["source_slice_interval"] == [0, 485] and result["source_slices"] == 485
    assert [x["slice_interval"] for x in result["shards"]] == [[0, 122], [122, 244], [244, 365], [365, 485]]
    assert list(result["sinks"]) == list(NAMES)
    all_ids = []
    for name in NAMES:
        sink = result["sinks"][name]
        expected = EXPECTED[name]
        assert sink["ids"] == IDS[name]
        assert sink["individual_id_charges"] is None
        assert (sink["source_heads"], int(sink["source_mass"]), int(sink["source_l1"])) == (6_704_640, 322_486_272, 3_085_516_800)
        assert sink["stage_pivot_uses"] == expected["piv"]
        assert sink["stage_tail_candidates"] == expected["cand"]
        assert sink["stage_pivotable_children"] == expected["pivable"]
        assert sink["terminal_K22_occurrences"] == sink["full_occurrences"] == sink["irreducible_occurrences"] == expected["terminal"]
        assert int(sink["full_charge_scaled_U"]) == int(sink["irreducible_charge_scaled_U"]) == expected["scaled"]
        assert sink["full_charge"] == sink["irreducible_charge"] == expected["charge"]
        assert Fraction(expected["scaled"], U) == Fraction(expected["charge"])
        assert all(U % int(d) == 0 for d in sink["denominator_product_hist"])
        all_ids.extend(sink["ids"])
    assert len(all_ids) == len(set(all_ids)) == 12
    expected_ids = [x for name in NAMES for x in IDS[name]]
    assert all_ids == expected_ids
    guard = result["strict_id_guard"]
    assert guard["expected_ordered_ids"] == guard["observed_ordered_ids"] == expected_ids
    assert guard["expected_count"] == guard["observed_count"] == 12
    assert guard["missing"] == guard["unexpected"] == guard["duplicates"] == []

    assert referee["status"] == "PASS_INDEPENDENT_257_DISTRIBUTED_LITERAL_DIRECT_K15_FOUR_SINK_K22_REPLAY"
    assert referee["source_samples"] == 257 and referee["first_slice"] == 0 and referee["last_slice"] == 484
    assert referee["all_divisions_exact"] and referee["all_literal_K22_children_terminal"]
    assert referee["source_provenance_preserved_through_all_pivots"]
    assert referee["cache_abstraction_used"] is False

    rows = list(csv.DictReader((HERE / "k22_direct_k15_literal_samples.tsv").open(), delimiter="\t"))
    assert len(rows) == 257 * 4
    aggregate = defaultdict(lambda: {"samples": 0, "children": 0, "q": 0, "scaled": 0, "packets": Counter()})
    scalar_checks = 0
    terminal_checks = 0
    for index, row in enumerate(rows):
        ordinal, k = divmod(index, 4)
        name = NAMES[k]
        path = PATHS[name]
        assert int(row["ordinal"]) == ordinal
        assert int(row["source_slice"]) == ordinal * 484 // 256
        assert int(row["packet"]) == ordinal % 3
        assert row["packet_label"] == ("322", "232", "223")[ordinal % 3]
        assert row["sink"] == name
        counts = [int(x) for x in row["pivot_counts"].split(",")]
        steps = row["intermediate_pivot_tail"].split(",") if row["intermediate_pivot_tail"] else []
        assert len(counts) == len(path) and len(steps) == len(path) - 1
        assert all(x > 0 for x in counts)
        denominator = prod(counts)
        assert U % denominator == 0
        terminal = int(row["terminal_K22_children"])
        q = int(row["literal_charge"])
        scaled = int(row["weighted_charge_scaled_U"])
        positive = int(row["source_positive"])
        final_tail_count = 32 if path[-1] == 3 else 12
        assert terminal == counts[-1] * final_tail_count > 0
        sign = -1 if len(path) % 2 == 0 else 1
        assert scaled == sign * positive * (U // denominator) * q
        scalar_checks += 1
        terminal_checks += terminal
        a = aggregate[name]
        a["samples"] += 1
        a["children"] += terminal
        a["q"] += q
        a["scaled"] += scaled
        a["packets"][row["packet_label"]] += 1

    for name in NAMES:
        observed = aggregate[name]
        published = referee["sinks"][name]
        assert published["strict_grouped_ids"] == IDS[name]
        assert observed["samples"] == published["samples"] == 257
        assert dict(observed["packets"]) == published["packet_witness_counts"] == {"322": 86, "232": 86, "223": 85}
        assert observed["children"] == published["literal_terminal_K22_children"]
        assert observed["q"] == int(published["literal_charge_sum"])
        assert observed["scaled"] == int(published["sample_weighted_charge_scaled_U"])
        assert observed["children"] > 0 and observed["q"] != 0 and observed["scaled"] != 0

    audit = {
        "status": "PASS_INDEPENDENT_STRICT_GROUPED_DIRECT_K15_FOUR_SINK_K22_AUDIT",
        "scale_U": str(U),
        "pinned_files": PINS,
        "shard_coverage": [[0, 122], [122, 244], [244, 365], [365, 485]],
        "strict_ordered_ids": expected_ids,
        "strict_id_count": 12,
        "missing_ids": [],
        "unexpected_ids": [],
        "duplicate_ids": [],
        "sink_summary": {
            name: {
                "response_path": list(PATHS[name]),
                "recurrence_sign": -1 if len(PATHS[name]) % 2 == 0 else 1,
                "terminal_K22_occurrences": EXPECTED[name]["terminal"],
                "charge_scaled_U": str(EXPECTED[name]["scaled"]),
                "charge": EXPECTED[name]["charge"],
            }
            for name in NAMES
        },
        "literal_referee": {
            "distributed_source_slices": 257,
            "source_sink_witnesses": len(rows),
            "occurrencewise_sign_U_scalar_checks": scalar_checks,
            "literal_terminal_K22_children": terminal_checks,
            "packet_witness_counts_per_sink": {"322": 86, "232": 86, "223": 85},
            "cache_abstraction_used": False,
        },
        "terminality_proof": "each response path removes total anchor mass 7 from a K15 signature of mass 9; every output has anchor mass 2, strictly below pivot mass 4",
        "packet_grouping_guard": "223/232/322 remain grouped source witness classes; individual scalar splitting is forbidden and null",
        "scope": "exactly four grouped sinks / 12 K22 IDs; no row output, K23, or K24",
    }
    logical = hashlib.sha256(json.dumps(audit, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    audit["logical_sha256"] = logical
    out = HERE / "results_k22_direct_k15_four_sink_audit.json"
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text(json.dumps(audit, indent=2) + "\n")
    os.replace(tmp, out)
    print(json.dumps({"status": audit["status"], "logical_sha256": logical, "audit_sha256": sha(out)}, indent=2))


if __name__ == "__main__":
    main()
