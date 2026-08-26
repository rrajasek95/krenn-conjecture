#!/usr/bin/env python3
"""Independent terminal referee for grouped D15:{223,232,322}|R:4-2."""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = (ROOT / "computations" /
        "unaudited-codex-orbit0-filtered-k16-run-2026-08-23")
CHECKPOINT = BASE / "checkpoint_direct_k15.bin"
PRODUCER = BASE / "run_filtered_k16.rs"
STRUCTURE = BASE / "filtered_k16_structure.bin"
AUX = BASE / "filtered_k17_aux.bin"
CYCLE = BASE / "filtered_k17_cycle_aux.bin"
K4 = (ROOT / "computations" /
      "unaudited-codex-orbit0-filtered-k18-charge-2026-08-23" /
      "filtered_k18_k4.bin")
FOLD_SOURCE = HERE / "run_k21_d15_r4_2_charge.rs"
ASSEMBLER = HERE / "assemble_k21_d15_r4_2_charge.py"
RESULT = HERE / "results_k21_d15_r4_2_charge.json"
SAMPLE_SOURCE = HERE / "referee_k21_d15_r4_2_samples.rs"
SAMPLE_RESULT = HERE / "results_k21_d15_r4_2_samples.json"
SAMPLE_TSV = HERE / "results_k21_d15_r4_2_samples.tsv"
OUT = HERE / "results_k21_d15_r4_2_independent_referee.json"

U = 400_591_699_200
N = 5_311_211
IDS = ["D15:223|R:4-2", "D15:232|R:4-2", "D15:322|R:4-2"]
EXPECTED_HASHES = {
    "checkpoint_direct_k15.bin":
        "e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f",
    "run_filtered_k16.rs":
        "85f9a3f1c18491bab52d06a0b25c9c88cc191ea55cb8eb666a70a62a36555432",
    "filtered_k16_structure.bin":
        "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    "filtered_k17_aux.bin":
        "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    "filtered_k17_cycle_aux.bin":
        "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    "filtered_k18_k4.bin":
        "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
    "run_k21_d15_r4_2_charge.rs":
        "e63cdfe040fb12a7ab093e69c7bac7834dea51c5cd704cb76686dc36b61af98c",
    "assemble_k21_d15_r4_2_charge.py":
        "1baec7f311f70f28423a15fe3b954e88b695b105bcc3a3be77dcd5c7e44bfa5a",
    "results_k21_d15_r4_2_charge.json":
        "af8c0943ce6b50961eb6cf3fa49e54a94a9e6bd488d5bed786ca71e7b4a5229d",
    "referee_k21_d15_r4_2_samples.rs":
        "974bdaa8003a9351cd81eb134c1dceb1f28913127079ac7d1ed0b553d0c46a2c",
    "results_k21_d15_r4_2_samples.json":
        "0395179b3766479cfb1e3f347c04f401012f0cb02285b01c15aa6d846f47e59c",
    "results_k21_d15_r4_2_samples.tsv":
        "a32c5634bb818656b8c0315df61639d937e8af7f4fe4fee7255ed5788a346412",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    h = sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20):
            h.update(block)
    return h.hexdigest()


def fraction_record(value):
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": str(value),
    }


def add_histogram(target, source):
    for key, value in source.items():
        target[int(key)] += value


def parse_anchor_pivots():
    data = STRUCTURE.read_bytes()
    require(data[:11] == b"K16DIRECT1\0", data[:11])
    position = 11
    nt, nr, np, na = struct.unpack_from("<IIII", data, position)
    position += 16
    require((nt, nr, np, na) == (384, 485, 78, 12), (nt, nr, np, na))
    anchors = data[position:position + 12]
    position += 12 + nt * (252 + 12) + nr * 24
    pivots = []
    for _ in range(np):
        pivots.append(data[position:position + 12])
        position += 12
    require(all(sum(pivot) == 4 for pivot in pivots), "K0 pivot anchor sums")
    return anchors, pivots


def available(row, anchors, pivots):
    positions = {cell: index for index, cell in enumerate(anchors)}
    signature = [0] * 12
    for cell in row:
        if cell in positions:
            signature[positions[cell]] += 1
    return signature, [index for index, pivot in enumerate(pivots)
                       if all(signature[i] >= pivot[i] for i in range(12))]


def audit_checkpoint():
    count = signed = l1 = 0
    prior = None
    with CHECKPOINT.open("rb") as stream:
        require(stream.read(8) == b"K15CHK1\0", "checkpoint magic")
        require(struct.unpack("<Q", stream.read(8))[0] == N,
                "checkpoint declared records")
        while record := stream.read(32):
            require(len(record) == 32, len(record))
            row = record[:24]
            coefficient = struct.unpack_from("<q", record, 24)[0]
            require(list(row) == sorted(row) and coefficient != 0,
                    (count, row.hex(), coefficient))
            require(prior is None or prior < row, (count, prior, row))
            prior = row
            count += 1
            signed += coefficient
            l1 += abs(coefficient)
    require((count, signed, l1) == (N, 322_486_272, 3_083_240_448),
            (count, signed, l1))
    require(CHECKPOINT.stat().st_size == 16 + 32 * N,
            CHECKPOINT.stat().st_size)
    producer_text = PRODUCER.read_text()
    require("w.write_all(&r.0).unwrap();w.write_all(&v.to_le_bytes()).unwrap()"
            in producer_text, "checkpoint record writer")
    return {
        "magic": "K15CHK1\\0",
        "record_bytes": 32,
        "records": count,
        "bytes": CHECKPOINT.stat().st_size,
        "signed_coefficient_sum": signed,
        "l1_coefficient_sum": l1,
        "strictly_increasing_literal_rows": True,
        "nonzero_coefficients": True,
        "packet_labels_retained": False,
    }


def audit_shards(result):
    shard_paths = [HERE / f"results_shard_{index:02d}.json"
                   for index in range(11)]
    shards = [json.loads(path.read_text()) for path in shard_paths]
    expected_intervals = [[index * 524_288, (index + 1) * 524_288]
                          for index in range(10)] + [[5_242_880, N]]
    require([shard["input_interval"] for shard in shards] == expected_intervals,
            [shard["input_interval"] for shard in shards])
    cursor = 0
    for index, shard in enumerate(shards):
        begin, end = shard["input_interval"]
        require(begin == cursor and end > begin, (index, cursor, begin, end))
        cursor = end
        require(shard["status"] ==
                "PASS_ATOMIC_INTERVAL_GROUPED_D15_R4_2_K21_CHARGE",
                (index, shard["status"]))
        require(shard["strict_covered_lineage_ids"] == IDS and
                shard["individual_id_charges"] is None,
                (index, shard["strict_covered_lineage_ids"]))
        require(int(shard["scale_U"]) == U and
                shard["input_records_declared"] == N and
                shard["input_records_consumed"] == end - begin,
                (index, shard))
        require(shard["K4_tail_candidates"] == 60 * shard["first_pivot_uses"],
                index)
        require(shard["K2_tail_occurrences"] == 12 * shard["second_pivot_uses"],
                index)
        require(shard["full_occurrences"] == shard["irreducible_occurrences"] ==
                shard["K2_tail_occurrences"], index)
        require(int(shard["full_charge_scaled_U"]) ==
                int(shard["irreducible_charge_scaled_U"]), index)
        require(shard["K2_response_cache"]["hits"] +
                shard["K2_response_cache"]["misses"] ==
                shard["second_pivot_uses"], index)
    require(cursor == N, cursor)

    scalar_fields = [
        "input_records_consumed", "first_pivot_uses", "K4_tail_candidates",
        "retained_pivotable_K19_children", "second_pivot_uses",
        "K2_tail_occurrences", "full_occurrences", "irreducible_occurrences",
    ]
    totals = {field: sum(shard[field] for shard in shards)
              for field in scalar_fields}
    for field in ("input_weight_sum", "full_charge_scaled_U",
                  "irreducible_charge_scaled_U"):
        totals[field] = sum(int(shard[field]) for shard in shards)
    expected_totals = {
        "input_records_consumed": N,
        "input_weight_sum": 322_486_272,
        "first_pivot_uses": 44_342_881,
        "K4_tail_candidates": 2_660_572_860,
        "retained_pivotable_K19_children": 972_495_600,
        "second_pivot_uses": 1_549_305_840,
        "K2_tail_occurrences": 18_591_670_080,
        "full_occurrences": 18_591_670_080,
        "irreducible_occurrences": 18_591_670_080,
        "full_charge_scaled_U": -105_580_126_744_994_119_680,
        "irreducible_charge_scaled_U": -105_580_126_744_994_119_680,
    }
    require(totals == expected_totals, (totals, expected_totals))

    h1, h2, hp = defaultdict(int), defaultdict(int), defaultdict(int)
    for shard in shards:
        add_histogram(h1, shard["first_denominator_hist"])
        add_histogram(h2, shard["second_denominator_hist"])
        add_histogram(hp, shard["product_denominator_hist"])
    require(sum(h1.values()) == N and
            sum(key * count for key, count in h1.items()) ==
            totals["first_pivot_uses"], h1)
    require(sum(h2.values()) == totals["retained_pivotable_K19_children"] and
            sum(key * count for key, count in h2.items()) ==
            totals["second_pivot_uses"], h2)
    require(sum(hp.values()) == totals["retained_pivotable_K19_children"] and
            all(U % denominator == 0 for denominator in hp), hp)
    require(result["atomic_interval_coverage"] == {
        "shards": 11,
        "intervals": expected_intervals,
        "no_gap": True,
        "no_overlap": True,
        "records": N,
    }, result["atomic_interval_coverage"])
    for field, expected in expected_totals.items():
        require(int(result[field]) == expected, (field, result[field], expected))
    require(result["first_denominator_hist"] ==
            {str(key): value for key, value in sorted(h1.items())}, "h1")
    require(result["second_denominator_hist"] ==
            {str(key): value for key, value in sorted(h2.items())}, "h2")
    require(result["product_denominator_hist"] ==
            {str(key): value for key, value in sorted(hp.items())}, "hp")
    computed_shard_hashes = {path.name: digest(path) for path in shard_paths}
    require(result["sha256"]["shards"] == computed_shard_hashes,
            (result["sha256"]["shards"], computed_shard_hashes))
    return {
        "intervals": expected_intervals,
        "no_gap": True,
        "no_overlap": True,
        "records": N,
        "totals": expected_totals,
        "first_denominator_hist": dict(sorted(h1.items())),
        "second_denominator_hist": dict(sorted(h2.items())),
        "product_denominator_hist": dict(sorted(hp.items())),
        "shard_sha256": computed_shard_hashes,
    }


def audit_samples(anchors, pivots):
    sample_result = json.loads(SAMPLE_RESULT.read_text())
    require(sample_result["status"] ==
            "PASS_INDEPENDENT_257_LITERAL_D15_R4_2_K21_SAMPLES",
            sample_result["status"])
    require(sample_result["strict_covered_lineage_ids"] == IDS,
            sample_result["strict_covered_lineage_ids"])
    expected_sample_totals = {
        "parents": 257,
        "first_index": 0,
        "last_index": N - 1,
        "p1_uses": 2_137,
        "K4_candidates": 128_220,
        "pivotable_K19_children": 47_280,
        "p2_uses": 74_160,
        "K21_children": 889_920,
        "charge_scaled_U": 9_921_235_611_893_760,
        "literal_abstract_cycle_key_guards": 889_920,
    }
    for key, expected in expected_sample_totals.items():
        require(int(sample_result[key]) == expected,
                (key, sample_result[key], expected))
    require(sample_result["all_K21_terminal"] is True, sample_result)

    lines = SAMPLE_TSV.read_text().splitlines()
    require(lines[0] == ("input_index\trow\tweight\tm1\tp1_uses\tK4_candidates\t"
                         "pivotable_K19\tp2_uses\tK21_children\tcharge_scaled_U"),
            lines[0])
    require(len(lines) == 258, len(lines))
    totals = [0] * 7
    with CHECKPOINT.open("rb") as checkpoint:
        for ordinal, line in enumerate(lines[1:]):
            fields = line.split("\t")
            require(len(fields) == 10, fields)
            index = int(fields[0])
            require(index == ordinal * (N - 1) // 256,
                    (ordinal, index, ordinal * (N - 1) // 256))
            checkpoint.seek(16 + 32 * index)
            record = checkpoint.read(32)
            row = bytes.fromhex(fields[1])
            coefficient = int(fields[2])
            require(row == record[:24] and
                    coefficient == struct.unpack_from("<q", record, 24)[0],
                    (ordinal, index, coefficient))
            signature, ps1 = available(row, anchors, pivots)
            require(sum(signature) == 9, (ordinal, index, signature))
            (m1, p1_uses, k4_candidates, pivotable_k19,
             p2_uses, k21_children) = map(int, fields[3:9])
            require(m1 == p1_uses == len(ps1), (ordinal, m1, ps1))
            require(k4_candidates == 60 * p1_uses, ordinal)
            require(0 <= pivotable_k19 <= k4_candidates, ordinal)
            require(k21_children == 12 * p2_uses, ordinal)
            charge = int(fields[9])
            for position, value in enumerate(
                    (p1_uses, k4_candidates, pivotable_k19,
                     p2_uses, k21_children, charge)):
                totals[position] += value
    require(totals[:5] == [2_137, 128_220, 47_280, 74_160, 889_920], totals)
    require(totals[5] == 9_921_235_611_893_760, totals)

    sample_source = SAMPLE_SOURCE.read_text()
    literal_guards = {
        "distributed_257_indices":
            "(0..257).map(|j|j*(N-1)/256)" in sample_source,
        "literal_first_response":
            "let row19=replace_anchor(&row,&e.anchors[p1],t4)" in sample_source,
        "literal_second_response":
            "let row21=replace_anchor(&row19,&e.anchors[p2],t2)" in sample_source,
        "terminal_signature_sum_3":
            "assert_eq!(s21.iter().map(|&x|x as usize).sum::<usize>(),3)"
            in sample_source,
        "literal_nonpivotability": "assert!(available(s21,&e).is_empty())"
                                  in sample_source,
        "abstract_equals_literal_cycle_key": "assert_eq!(a,l)" in sample_source,
    }
    require(all(literal_guards.values()), literal_guards)
    return {
        **expected_sample_totals,
        "indices_match_floor_rule": True,
        "checkpoint_rows_and_coefficients_match": True,
        "first_pivot_sets_recomputed": True,
        "literal_replay_source_guards": literal_guards,
        "rerun_status": sample_result["status"],
    }


def main():
    paths = [CHECKPOINT, PRODUCER, STRUCTURE, AUX, CYCLE, K4, FOLD_SOURCE,
             ASSEMBLER, RESULT, SAMPLE_SOURCE, SAMPLE_RESULT, SAMPLE_TSV]
    hashes = {path.name: digest(path) for path in paths}
    require(hashes == EXPECTED_HASHES, (hashes, EXPECTED_HASHES))

    result = json.loads(RESULT.read_text())
    require(result["status"] == "PASS_COMPLETE_GROUPED_D15_R4_2_K21_CHARGE",
            result["status"])
    require(result["strict_covered_lineage_ids"] == IDS and
            result["individual_id_charges"] is None,
            (result["strict_covered_lineage_ids"],
             result["individual_id_charges"]))
    require(int(result["scale_U"]) == U, result["scale_U"])
    require(result["full_equals_irreducible"] is True and
            result["all_U_divisions_exact"] is True, result)
    charge = Fraction(int(result["full_charge_scaled_U"]), U)
    require(charge == Fraction(-2_333_827_745_792, 8_855), charge)
    require(result["reduced_exact_scalar"] == str(charge),
            result["reduced_exact_scalar"])
    require("grouped three-ID scalar only" in result["scope"] and
            "no individual-ID scalar" in result["scope"], result["scope"])

    checkpoint_audit = audit_checkpoint()
    shard_audit = audit_shards(result)
    anchors, pivots = parse_anchor_pivots()
    sample_audit = audit_samples(anchors, pivots)

    fold_source = FOLD_SOURCE.read_text()
    sign_and_scope_guards = {
        "U_exact": "const U: i128 = 400_591_699_200" in
                   (ROOT / "computations" /
                    "unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23" /
                    "run_hidden_children_prefix.rs").read_text(),
        "first_sign_flip": "let w19=-(v as i128)*U/(m1 as i128)" in fold_source,
        "second_sign_flip": "let w21=-w19/(m2 as i128)" in fold_source,
        "exact_U_product_division":
            "assert_eq!(U%((m1*m2)as i128),0)" in fold_source,
        "strict_three_ID_literal": all(lineage in fold_source for lineage in IDS),
        "null_individual_charges":
            "individual_id_charges\\\":null" in fold_source,
        "terminal_signature_sum_3": "predicted.iter().map(|&x|x as usize).sum::<usize>(),3"
                                   in fold_source,
        "terminal_literal_nonpivotability":
            "assert!(available(predicted,e).is_empty())" in fold_source,
    }
    require(all(sign_and_scope_guards.values()), sign_and_scope_guards)

    referee = {
        "schema": "orbit0-k21-d15-r4-2-independent-terminal-referee-v1",
        "status": "PASS_INDEPENDENT_GROUPED_D15_R4_2_K21_REFEREE",
        "scope": ("Read-only/referee validation of exactly the grouped three "
                  "requested IDs; no full fold rerun and no other K21 path."),
        "coverage": {
            "expected_ids": IDS,
            "observed_ids": result["strict_covered_lineage_ids"],
            "strict_exact_set_and_order": True,
            "individual_id_charges": None,
        },
        "checkpoint_audit": checkpoint_audit,
        "atomic_merge_audit": shard_audit,
        "charge": {
            "scale_U": U,
            "scaled": result["full_charge_scaled_U"],
            "reduced": fraction_record(charge),
            "full_equals_irreducible": True,
        },
        "sign_U_scope_guards": sign_and_scope_guards,
        "literal_sample_audit": sample_audit,
        "terminality": {
            "all_sampled_K21_children_terminal": True,
            "anchor_sum_argument": "K21 anchor sum 3 < every K0 pivot anchor sum 4",
            "literal_abstract_cycle_key_comparisons": 889_920,
        },
        "pinned_sha256": {
            str(path.relative_to(ROOT)): hashes[path.name] for path in paths
        },
    }
    logical = json.dumps(referee, sort_keys=True,
                         separators=(",", ":")).encode()
    referee["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(referee, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": referee["status"],
        "intervals": 11,
        "records": N,
        "charge": str(charge),
        "literal_sample_children": 889_920,
        "logical_sha256": referee["logical_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
