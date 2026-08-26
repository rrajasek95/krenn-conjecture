#!/usr/bin/env python3
"""Independent exact audit of the eight-shard direct-K15 K23 merge.

This deliberately does not import the producer/merger contract.  It replays the
interval partition, scalar aggregation, grouped-ID semantics, and the sealed
257-source/1028-witness literal ledger directly from the retained artifacts.
"""

from collections import Counter
from fractions import Fraction
import argparse
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GATE = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k15-four-sink-2026-08-24"
U = 400_591_699_200
INTERVALS = [(0, 60), (60, 121), (121, 181), (181, 242),
             (242, 303), (303, 363), (363, 424), (424, 485)]
NAMES = [
    "D15:{223,232,322}|R:2-2-4",
    "D15:{223,232,322}|R:2-3-3",
    "D15:{223,232,322}|R:3-2-3",
    "D15:{223,232,322}|R:4-4",
]
PATHS = [[2, 2, 4], [2, 3, 3], [3, 2, 3], [4, 4]]
GROUPS = ["source_D15_R2_2_4", "source_D15_R2_3_3",
          "source_D15_R3_2_3", "source_D15_R4_4"]
IDS = {
    name: [f"D15:{packet}|R:{'-'.join(map(str, path))}"
           for packet in (223, 232, 322)]
    for name, path in zip(NAMES, PATHS)
}
MERGED = HERE / "results_k23_direct_k15_four_sink.json"
FRAGMENT = HERE / "k23_direct_k15_fragment_manifest.json"
LEDGER = GATE / "k23_direct_k15_literal_samples.tsv"
LITERAL_RESULT = GATE / "results_k23_direct_k15_literal_referee.json"
PINS = {
    GATE / "run_k23_direct_k15_four_sink.rs": "c3ea65b5ac1221e1b0020e2f0a9753bd774826059ae16e24c05cd4f6f5706e8c",
    GATE / "run_k23_direct_k15_four_sink": "a6bc9f1f1b217a4cfc8dc662ea1358e4c3ac012f40c49e6c07cf05b1e52faa04",
    GATE / "referee_k23_direct_k15_literal.rs": "0678d51c89228109f62a141d8e9f39637686124101155df0b10842e733e5e6ca",
    GATE / "referee_k23_direct_k15_literal": "b53f0733f4e549633b072d4df688b20c90feccfefea6d2d03311a7deb296b5c4",
    LEDGER: "9a685bc1d1ead2bb92f6757cc7dcf1f27c4ab90594d9e297e6e11562290158da",
    LITERAL_RESULT: "da28e1d4402ef0903b25e1048bfbc5e614128a3bcc8d7623c7de975e3394ebb6",
}
HEADER = ("ordinal\tsource_slice\tpacket\tpacket_label\tsink\tsource_positive\t"
          "a\tb\tc\tintermediate_pivot_tail\tpivot_counts\tterminal_K23_children\t"
          "literal_charge\tweighted_charge_scaled_U")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            h.update(block)
    return h.hexdigest()


def add_lists(rows, key):
    return [sum(row[key][i] for row in rows) for i in range(len(rows[0][key]))]


def audit_literal_ledger():
    for path, digest in PINS.items():
        require(path.is_file() and sha(path) == digest, f"literal/source pin: {path.name}")
    result = json.loads(LITERAL_RESULT.read_text())
    require(result["status"] == "PASS_INDEPENDENT_257_DISTRIBUTED_LITERAL_DIRECT_K15_FOUR_SINK_K23_REPLAY",
            "literal result status")
    require(result["source_samples"] == 257 and result["first_slice"] == 0 and
            result["last_slice"] == 484, "literal distribution")
    require(result["all_divisions_exact"] is True and
            result["all_literal_K23_children_terminal"] is True and
            result["terminal_anchor_signature_mass"] == 1 and
            result["source_provenance_preserved_through_all_pivots"] is True and
            result["cache_abstraction_used"] is False, "literal global assertions")
    lines = LEDGER.read_text().splitlines()
    require(len(lines) == 1029 and lines[0] == HEADER, "literal ledger schema/count")
    aggregates = {name: {"children": 0, "charge": 0, "scaled": 0,
                         "packets": Counter()} for name in NAMES}
    for ordinal in range(257):
        rows = [line.split("\t") for line in lines[1 + 4 * ordinal:1 + 4 * (ordinal + 1)]]
        expected_slice = ordinal * 484 // 256
        expected_packet = ordinal % 3
        expected_label = ["322", "232", "223"][expected_packet]
        require([row[4] for row in rows] == NAMES, f"literal sink order {ordinal}")
        for name, degrees, row in zip(NAMES, PATHS, rows):
            require(len(row) == 14, f"literal fields {ordinal}/{name}")
            require((int(row[0]), int(row[1]), int(row[2]), row[3]) ==
                    (ordinal, expected_slice, expected_packet, expected_label),
                    f"literal provenance {ordinal}/{name}")
            positive = int(row[5])
            require(positive != 0, f"literal nonzero source {ordinal}/{name}")
            require(all(int(value) >= 0 for value in row[6:9]),
                    f"literal factor ordinal {ordinal}/{name}")
            steps = [] if not row[9] else [tuple(map(int, item.split(":")))
                                           for item in row[9].split(",")]
            require(len(steps) == len(degrees) - 1 and
                    all(0 <= pivot < 78 and tail >= 0 for pivot, tail in steps),
                    f"literal steps {ordinal}/{name}")
            divisors = list(map(int, row[10].split(",")))
            require(len(divisors) == len(degrees) and all(value > 0 for value in divisors),
                    f"literal divisors {ordinal}/{name}")
            product = math.prod(divisors)
            require(U % product == 0, f"literal nonexact division {ordinal}/{name}")
            children, charge, scaled = map(int, row[11:14])
            fan = {2: 12, 3: 32, 4: 60}[degrees[-1]]
            require(children > 0 and children % fan == 0,
                    f"literal terminal fan {ordinal}/{name}")
            sign = -positive if len(degrees) % 2 == 0 else positive
            require(scaled == sign * (U // product) * charge,
                    f"literal signed scalar {ordinal}/{name}")
            aggregate = aggregates[name]
            aggregate["children"] += children
            aggregate["charge"] += charge
            aggregate["scaled"] += scaled
            aggregate["packets"][expected_label] += 1
    for name, degrees in zip(NAMES, PATHS):
        sink = result["sinks"][name]
        aggregate = aggregates[name]
        require(sink["strict_grouped_ids"] == IDS[name] and sink["degrees"] == degrees,
                f"literal strict group {name}")
        require(sink["samples"] == 257 and sink["packet_witness_counts"] ==
                {"322": 86, "232": 86, "223": 85}, f"literal packets {name}")
        require((sink["literal_terminal_K23_children"], int(sink["literal_charge_sum"]),
                 int(sink["sample_weighted_charge_scaled_U"])) ==
                (aggregate["children"], aggregate["charge"], aggregate["scaled"]),
                f"literal aggregate {name}")


def audit():
    shards = []
    for path in sorted(HERE.glob("results_shard_??.json")):
        data = json.loads(path.read_text())
        shards.append((tuple(data["slice_interval"]), path, sha(path), data))
    shards.sort()
    require(len(shards) == 8, "exactly eight shards")
    require([row[0] for row in shards] == INTERVALS, "exact no-gap/no-overlap intervals")
    merged = json.loads(MERGED.read_text())
    require(merged["status"] == "PASS_COMPLETE_GROUPED_DIRECT_K15_FOUR_SINK_K23_CHARGE",
            "merged status")
    require(int(merged["scale_U"]) == U and merged["slice_interval"] == [0, 485] and
            merged["source_slices"] == 485, "merged U/interval")
    require(set(merged["sinks"]) == set(NAMES), "merged sink set")
    totals = {}
    for name, degrees in zip(NAMES, PATHS):
        rows = [row[3]["sinks"][name] for row in shards]
        target = merged["sinks"][name]
        require(target["ids"] == IDS[name] and target["degrees"] == degrees and
                target["individual_id_charges"] is None, f"group-once semantics {name}")
        histogram = Counter()
        for row in rows:
            histogram.update(row["denominator_product_hist"])
        expected = {
            "source_heads": sum(row["source_heads"] for row in rows),
            "source_mass": str(sum(int(row["source_mass"]) for row in rows)),
            "source_l1": str(sum(int(row["source_l1"]) for row in rows)),
            "stage_pivot_uses": add_lists(rows, "stage_pivot_uses"),
            "stage_tail_candidates": add_lists(rows, "stage_tail_candidates"),
            "stage_pivotable_children": add_lists(rows, "stage_pivotable_children"),
            "terminal_response_keys_evaluated": sum(row["terminal_response_keys_evaluated"] for row in rows),
            "terminal_K23_occurrences": sum(row["terminal_K23_occurrences"] for row in rows),
            "full_occurrences": sum(row["full_occurrences"] for row in rows),
            "irreducible_occurrences": sum(row["irreducible_occurrences"] for row in rows),
            "full_charge_scaled_U": str(sum(int(row["full_charge_scaled_U"]) for row in rows)),
            "irreducible_charge_scaled_U": str(sum(int(row["irreducible_charge_scaled_U"]) for row in rows)),
            "denominator_product_hist": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        }
        for key, value in expected.items():
            require(target[key] == value, f"independent merged {name}.{key}")
        require((target["source_heads"], int(target["source_mass"]), int(target["source_l1"])) ==
                (6_704_640, 322_486_272, 3_085_516_800), f"full source census {name}")
        require(target["terminal_K23_occurrences"] == target["full_occurrences"] ==
                target["irreducible_occurrences"], f"terminal occurrence identity {name}")
        require(target["full_charge_scaled_U"] == target["irreducible_charge_scaled_U"],
                f"terminal charge identity {name}")
        totals[name] = int(target["full_charge_scaled_U"])
    merged_hash = sha(MERGED)
    fragment = json.loads(FRAGMENT.read_text())
    require(fragment["degree"] == 23 and int(fragment["scale_U"]) == U and
            len(fragment["groups"]) == 4, "fragment header")
    flat_ids = []
    for index, entry in enumerate(fragment["groups"]):
        name = NAMES[index]
        require(entry["group_id"] == GROUPS[index] and entry["ids"] == IDS[name],
                f"fragment partition {index}")
        require(entry["evidence_path"] == str(MERGED.relative_to(ROOT)) and
                entry["evidence_sha256"] == merged_hash, f"fragment evidence {index}")
        scaled = totals[name]
        require(int(entry["full_scaled_U"]) == scaled == int(entry["irreducible_scaled_U"]),
                f"fragment scaled {index}")
        require(Fraction(entry["full"]) == Fraction(scaled, U) == Fraction(entry["irreducible"]),
                f"fragment rational {index}")
        flat_ids.extend(entry["ids"])
    require(len(flat_ids) == len(set(flat_ids)) == 12, "exact 12 singleton IDs")
    audit_literal_ledger()
    payload = {
        "status": "PASS_INDEPENDENT_K23_DIRECT_K15_FINAL_EIGHT_SHARD_REFEREE",
        "degree": 23,
        "scale_U": U,
        "intervals": [list(row[0]) for row in shards],
        "no_gap_no_overlap": True,
        "shards": [{"path": str(row[1].relative_to(ROOT)), "sha256": row[2],
                    "interval": list(row[0])} for row in shards],
        "merged": {"path": str(MERGED.relative_to(ROOT)), "sha256": merged_hash},
        "fragment": {"path": str(FRAGMENT.relative_to(ROOT)), "sha256": sha(FRAGMENT)},
        "strict_groups": GROUPS,
        "strict_ids": flat_ids,
        "group_scalars_scaled_U": {group: str(totals[name])
                                    for group, name in zip(GROUPS, NAMES)},
        "group_scalar_counted_once": True,
        "full_equals_irreducible": True,
        "literal_referee": {
            "distributed_sources": 257,
            "sink_witnesses": 1028,
            "first_slice": 0,
            "last_slice": 484,
            "ledger_sha256": PINS[LEDGER],
            "result_sha256": PINS[LITERAL_RESULT],
            "all_signed_U_divisions_and_aggregates_replayed": True,
            "all_literal_K23_children_terminal": True,
            "cache_abstraction_used": False,
        },
        "no_scalar_rerun": True,
    }
    payload["logical_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = audit()
    if arguments.output:
        require(not arguments.output.exists(), f"refuse overwrite: {arguments.output}")
        temporary = Path(str(arguments.output) + ".tmp")
        temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        temporary.replace(arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))
