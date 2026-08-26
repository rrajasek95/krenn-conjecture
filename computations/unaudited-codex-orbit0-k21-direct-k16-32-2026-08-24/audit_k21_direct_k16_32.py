#!/usr/bin/env python3
"""Strict grouped terminal referee for the six D16:*|R:3-2 K21 IDs."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = (ROOT / "computations" /
        "unaudited-codex-orbit0-filtered-k16-run-2026-08-23")
CHECKPOINT = BASE / "checkpoint_direct_k16.bin"
STRUCTURE = BASE / "filtered_k16_structure.bin"
AUX = BASE / "filtered_k17_aux.bin"
CYCLE = BASE / "filtered_k17_cycle_aux.bin"
PRODUCER = BASE / "run_filtered_k16.rs"
PROVIDER = (ROOT / "computations" /
            "unaudited-codex-orbit0-filtered-k18-charge-2026-08-23" /
            "run_k18_charge.rs")
SOURCE = HERE / "run_k21_direct_k16_32.rs"
RESULT = HERE / "results_k21_direct_k16_32.json"
SAMPLES = HERE / "results_k21_direct_k16_32.json.samples.tsv"
OUT = HERE / "results_k21_direct_k16_32_audit.json"

U = 400_591_699_200
N = 24_097_095
IDS = [f"D16:{word}|R:3-2" for word in
       ("224", "233", "242", "323", "332", "422")]
EXPECTED_HASHES = {
    "checkpoint_direct_k16.bin":
        "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3",
    "filtered_k16_structure.bin":
        "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    "filtered_k17_aux.bin":
        "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    "filtered_k17_cycle_aux.bin":
        "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    "run_filtered_k16.rs":
        "85f9a3f1c18491bab52d06a0b25c9c88cc191ea55cb8eb666a70a62a36555432",
    "run_k18_charge.rs":
        "24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
    "run_k21_direct_k16_32.rs":
        "b4f0c4ae64d2d29d1febb2bd6beb4b2e745f944701404620c41cd591d781f73a",
    "results_k21_direct_k16_32.json":
        "92a6a9a27dbf0fc3c82f1dd6b71155cf81118f5e1bf9ff7b1fbb38ab313793ca",
    "results_k21_direct_k16_32.json.samples.tsv":
        "1f49343a31183ea787960dff69faaf7e5b48c939475f9521918c0dc22908c6ac",
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


def parse_pivots():
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
    return anchors, pivots


def available(row, anchors, pivots):
    positions = {cell: index for index, cell in enumerate(anchors)}
    signature = [0] * 12
    for cell in row:
        if cell in positions:
            signature[positions[cell]] += 1
    return [index for index, pivot in enumerate(pivots)
            if all(signature[i] >= pivot[i] for i in range(12))]


def checkpoint_record(stream, index):
    stream.seek(16 + 32 * index)
    record = stream.read(32)
    require(len(record) == 32, (index, len(record)))
    return record[:24], struct.unpack_from("<q", record, 24)[0]


def audit_samples(anchors, pivots):
    lines = SAMPLES.read_text().splitlines()
    header = (
        "sample_ordinal\trecord_index\tK16_row\tcoefficient\tm1\tp1\t"
        "pivotable_K19_children\tp2_uses\tK21_children\t"
        "charge_per_source_coefficient_scaled_U"
    )
    require(lines[0] == header, lines[0])
    require(len(lines) == 258, len(lines))
    seen = set()
    with CHECKPOINT.open("rb") as stream:
        require(stream.read(8) == b"K16DIR1\0", "checkpoint magic")
        require(struct.unpack("<Q", stream.read(8))[0] == N, "checkpoint count")
        for line in lines[1:]:
            fields = line.split("\t")
            require(len(fields) == 10, fields)
            ordinal, index = map(int, fields[:2])
            require(ordinal not in seen and 0 <= ordinal <= 256, ordinal)
            seen.add(ordinal)
            require(index == ordinal * (N - 1) // 256,
                    (ordinal, index, ordinal * (N - 1) // 256))
            row = bytes.fromhex(fields[2])
            coefficient = int(fields[3])
            require(len(row) == 24 and list(row) == sorted(row), fields[2])
            expected_row, expected_coefficient = checkpoint_record(stream, index)
            require((row, coefficient) == (expected_row, expected_coefficient),
                    (ordinal, index, coefficient, expected_coefficient))
            ps1 = available(row, anchors, pivots)
            m1, p1 = map(int, fields[4:6])
            require(m1 == len(ps1) and p1 == ps1[0],
                    (ordinal, index, m1, p1, ps1))
            pivotable_k19, p2_uses, k21_children = map(int, fields[6:9])
            require(0 <= pivotable_k19 <= 32 and p2_uses >= pivotable_k19,
                    (ordinal, pivotable_k19, p2_uses))
            require(k21_children == 12 * p2_uses,
                    (ordinal, k21_children, p2_uses))
            int(fields[9])
    require(seen == set(range(257)), sorted(seen))
    return {
        "samples": 257,
        "spacing_rule": "floor(j*(24097095-1)/256), j=0..256",
        "minimum_record_index": 0,
        "maximum_record_index": N - 1,
        "literal_checkpoint_row_and_coefficient_match": True,
        "first_pivot_availability_recomputed": True,
    }


def main():
    paths = [CHECKPOINT, STRUCTURE, AUX, CYCLE, PRODUCER, PROVIDER,
             SOURCE, RESULT, SAMPLES]
    hashes = {path.name: digest(path) for path in paths}
    require(hashes == EXPECTED_HASHES, (hashes, EXPECTED_HASHES))

    result = json.loads(RESULT.read_text())
    require(result["status"] ==
            "PASS_COMPLETE_GROUPED_SIX_D16_R_3_2_K21_CHARGE",
            result["status"])
    require(int(result["scale_U"]) == U, result["scale_U"])
    require(result["ids"] == IDS and result["covered_ids"] == 6,
            (result["ids"], result["covered_ids"]))
    require(result["individual_id_charges"] is None,
            result["individual_id_charges"])
    require("not packet labels" in result["packet_grouping_guard"],
            result["packet_grouping_guard"])
    require((result["records_consumed"], result["records_declared"],
             result["source_rows"], result["workers"]) == (N, N, N, 8), result)
    require(0 < result["elapsed_seconds"] < 600, result["elapsed_seconds"])

    expected = {
        "signed_source_coefficient": 1_464_625_152,
        "l1_source_coefficient": 13_978_655_136,
        "pivotable_K16_rows": 24_003_767,
        "selected_p1_uses": 129_939_187,
        "K19_child_occurrences": 4_158_053_984,
        "pivotable_K19_child_occurrences": 1_295_008_880,
        "selected_p2_uses": 2_041_782_688,
        "K21_terminal_occurrences": 24_501_392_256,
    }
    for field, value in expected.items():
        observed = int(result[field])
        require(observed == value, (field, observed, value))
    require(result["K19_child_occurrences"] ==
            32 * result["selected_p1_uses"], result)
    require(result["K21_terminal_occurrences"] ==
            12 * result["selected_p2_uses"], result)
    require(result["full_occurrences"] == result["irreducible_occurrences"] ==
            result["K21_terminal_occurrences"], result)
    require(result["full_charge_scaled_U"] ==
            result["irreducible_charge_scaled_U"], result)
    scaled = int(result["full_charge_scaled_U"])
    require(scaled == -643_522_419_678_967_234_560, scaled)
    require(result["all_K21_children_irreducible"] is True, result)

    histogram = result["m1_m2_occurrence_hist"]
    require(sum(histogram.values()) ==
            result["pivotable_K19_child_occurrences"], histogram)
    require(sum(int(key.split("_")[1]) * count
                for key, count in histogram.items()) ==
            result["selected_p2_uses"], histogram)
    require(result["terminal_profile_cache"] == {
        "hits": 1_958_648_097,
        "misses": 83_134_591,
        "peak_keys_per_100k_chunk": 1_282_417,
    }, result["terminal_profile_cache"])

    checkpoint_size = CHECKPOINT.stat().st_size
    require(checkpoint_size == 16 + 32 * N, checkpoint_size)
    producer_text = PRODUCER.read_text()
    packet_guard = {
        "checkpoint_record_bytes": 32,
        "checkpoint_fields": ["canonical_row[24]", "collected_coefficient_i64"],
        "producer_write_has_only_row_and_coefficient":
            "w.write_all(&r.0).unwrap();w.write_all(&v.to_le_bytes()).unwrap()"
            in producer_text,
        "packet_label_present": False,
        "individual_charge_reconstruction_authorized": False,
    }
    require(packet_guard["producer_write_has_only_row_and_coefficient"],
            packet_guard)
    anchors, pivots = parse_pivots()
    sample_audit = audit_samples(anchors, pivots)

    source_text = SOURCE.read_text()
    source_guards = {
        "literal_K3_child_before_second_pivot":
            "let k19 = replace(row, &e.anchors[p1], t1);" in source_text,
        "literal_second_pivot_set": "let ps2 = avail(s2, e);" in source_text,
        "terminal_full_equals_irreducible":
            "assert_eq!((full_n, irreducible_n), (12, 12));" in source_text,
        "exact_two_denominator_division":
            "assert_eq!(U21 % ((m1 * m2) as i128), 0);" in source_text,
        "two_response_sign":
            "let unit_weight = U21 / ((m1 * m2) as i128);" in source_text,
        "bounded_cache": "terminal.clear();" in source_text,
        "balanced_256_ranges": "let pieces = workers * 32;" in source_text,
        "hard_600_second_gate": "assert!(elapsed < 600.0" in source_text,
        "atomic_final_write": "rename(tmp, output).unwrap();" in source_text,
    }
    require(all(source_guards.values()), source_guards)

    charge = Fraction(scaled, U)
    audit = {
        "schema": "orbit0-k21-direct-k16-32-grouped-terminal-audit-v1",
        "status": "PASS_STRICT_GROUPED_SIX_ID_D16_R_3_2_TERMINAL_AUDIT",
        "scope": ("Exactly one grouped scalar for the six requested IDs; "
                  "no individual reconstruction, other K21 ID, row "
                  "checkpoint, or membership claim."),
        "coverage": {
            "expected_ids": IDS,
            "observed_ids": result["ids"],
            "strict_exact_set_and_order": True,
            "covered_ids": 6,
            "individual_id_charges": None,
        },
        "grouped_result": {
            **expected,
            "full_and_irreducible_occurrences":
                result["K21_terminal_occurrences"],
            "full_and_irreducible_charge_scaled_U": str(scaled),
            "full_and_irreducible_charge": fraction_record(charge),
        },
        "packet_grouping_guard": packet_guard,
        "terminal_guard": {
            "all_K21_children_irreducible": True,
            "method": ("Literal K19 children determine p2; every terminal "
                       "profile miss asserts full_n=irreducible_n=12 and "
                       "full_q=irreducible_q before exact-key reuse."),
        },
        "compression_guard": {
            "compression_begins_after_second_pivot": True,
            "terminal_key": "path profile, literal anchor signature, p2, degree=2",
            "peak_keys_per_range": 1_282_417,
            "no_bulk_row_output": True,
        },
        "sample_audit": sample_audit,
        "source_guards": source_guards,
        "pinned_sha256": {
            str(path.relative_to(ROOT)): hashes[path.name] for path in paths
        },
    }
    logical = json.dumps(audit, sort_keys=True,
                         separators=(",", ":")).encode()
    audit["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": audit["status"],
        "covered_ids": 6,
        "individual_id_charges": None,
        "terminal_occurrences": result["K21_terminal_occurrences"],
        "charge": str(charge),
        "logical_sha256": audit["logical_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
