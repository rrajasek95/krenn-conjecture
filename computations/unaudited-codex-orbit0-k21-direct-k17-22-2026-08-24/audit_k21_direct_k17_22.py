#!/usr/bin/env python3
"""Strict terminal referee for the seven D17:*|R:2-2 K21 charges."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "run_k21_direct_k17_22.rs"
RESULT = HERE / "results_k21_direct_k17_22.json"
SAMPLES = HERE / "results_k21_direct_k17_22.json.samples.tsv"
STRUCTURE = (ROOT / "computations" /
             "unaudited-codex-orbit0-filtered-k16-run-2026-08-23" /
             "filtered_k16_structure.bin")
AUX = STRUCTURE.with_name("filtered_k17_aux.bin")
CYCLE = STRUCTURE.with_name("filtered_k17_cycle_aux.bin")
PROVIDER = (ROOT / "computations" /
            "unaudited-codex-orbit0-filtered-k18-charge-2026-08-23" /
            "run_k18_charge.rs")
OUT = HERE / "results_k21_direct_k17_22_audit.json"

U = 400_591_699_200
IDS = [f"D17:{word}|R:2-2" for word in
       ("234", "243", "324", "333", "342", "423", "432")]
EXPECTED = {
    "D17:234|R:2-2": (11_174_400, 11_174_400, 33_523_200,
                       402_278_400, 124_780_800, 173_203_200,
                       2_078_438_400, 70_934_137_393_854_873_600),
    "D17:243|R:2-2": (11_174_400, 10_243_200, 25_142_400,
                       301_708_800, 83_808_000, 119_193_600,
                       1_430_323_200, -45_168_328_354_893_004_800),
    "D17:324|R:2-2": (11_174_400, 11_174_400, 50_284_800,
                       603_417_600, 201_139_200, 312_883_200,
                       3_754_598_400, 30_050_670_438_012_026_880),
    "D17:333|R:2-2": (15_892_480, 15_892_480, 49_664_000,
                       595_968_000, 158_924_800, 238_387_200,
                       2_860_646_400, -92_006_616_648_776_417_280),
    "D17:342|R:2-2": (11_174_400, 11_174_400, 50_284_800,
                       603_417_600, 201_139_200, 312_883_200,
                       3_754_598_400, -59_746_518_632_624_947_200),
    "D17:423|R:2-2": (11_174_400, 10_243_200, 25_142_400,
                       301_708_800, 83_808_000, 119_193_600,
                       1_430_323_200, -94_894_366_563_208_396_800),
    "D17:432|R:2-2": (11_174_400, 11_174_400, 33_523_200,
                       402_278_400, 124_780_800, 173_203_200,
                       2_078_438_400, -5_374_075_265_184_890_880),
}
EXPECTED_HASHES = {
    "filtered_k16_structure.bin":
        "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    "filtered_k17_aux.bin":
        "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    "filtered_k17_cycle_aux.bin":
        "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    "run_k18_charge.rs":
        "24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
    "run_k21_direct_k17_22.rs":
        "7999b1797e3103f254977b17f60ff42088f4eee6726ba4e7006b86f08cff05b7",
    "results_k21_direct_k17_22.json":
        "9c217ea0a646ae8f7bceec1c1dd946d54b991b454046496fd7280127096a758c",
    "results_k21_direct_k17_22.json.samples.tsv":
        "7e37f02831ae227e96f0f4f64cadc774dcadb274650b9c9aa4fb727f878cbc5d",
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


def parse_structure():
    data = STRUCTURE.read_bytes()
    require(data[:11] == b"K16DIRECT1\0", data[:11])
    position = 11
    nt, nr, np, na = struct.unpack_from("<IIII", data, position)
    position += 16
    require((nt, nr, np, na) == (384, 485, 78, 12), (nt, nr, np, na))
    anchors = data[position:position + 12]
    position += 12 + nt * (252 + 12)
    records = []
    for _ in range(nr):
        row = data[position:position + 12]
        size, coefficient = struct.unpack_from("<Iq", data, position + 12)
        position += 24
        records.append((row, size, coefficient))
    pivots = []
    for _ in range(np):
        pivots.append(data[position:position + 12])
        position += 12
    factors = [[None] * 3 for _ in range(3)]
    for factor in range(3):
        for degree_index in range(3):
            count = struct.unpack_from("<I", data, position)[0]
            position += 4
            values = set()
            for _ in range(count):
                values.add(data[position:position + 4])
                position += 4
            require(count == (12, 32, 60)[degree_index],
                    (factor, degree_index, count))
            factors[factor][degree_index] = values
    require(position == len(data), (position, len(data)))
    return anchors, records, pivots, factors


def available_count(row, anchors, pivots):
    positions = {cell: index for index, cell in enumerate(anchors)}
    signature = [0] * 12
    for cell in row:
        if cell in positions:
            signature[positions[cell]] += 1
    available = [index for index, pivot in enumerate(pivots)
                 if all(signature[i] >= pivot[i] for i in range(12))]
    return available


def audit_samples(anchors, records, pivots, factors):
    lines = SAMPLES.read_text().splitlines()
    expected_header = (
        "id\tr8_index\tK17_row\tfactor0\tfactor1\tfactor2\tsource_mass\t"
        "m1\tp1\tpivotable_K19_children\tp2_uses\tK21_children\t"
        "charge_per_source_mass_scaled_U"
    )
    require(lines[0] == expected_header, lines[0])
    require(len(lines) == 258, len(lines))
    expected_indices = {j * 484 // 256 for j in range(257)}
    observed_indices = set()
    for line in lines[1:]:
        fields = line.split("\t")
        require(len(fields) == 13, fields)
        lineage, ri_text, row_hex, *rest = fields
        require(lineage in IDS, lineage)
        ri = int(ri_text)
        observed_indices.add(ri)
        row = bytes.fromhex(row_hex)
        tails = [bytes.fromhex(rest[j]) for j in range(3)]
        source_mass, m1, p1 = map(int, rest[3:6])
        require(len(row) == 24 and list(row) == sorted(row), row_hex)
        word = lineage.split(":", 1)[1].split("|", 1)[0]
        for factor, (digit, tail) in enumerate(zip(word, tails, strict=True)):
            require(tail in factors[factor][int(digit) - 2],
                    (lineage, factor, digit, tail.hex()))
        source_row, size, coefficient = records[ri]
        require(row == bytes(sorted(source_row + b"".join(tails))),
                (lineage, ri, row_hex))
        require(source_mass == size * coefficient,
                (lineage, ri, source_mass, size * coefficient))
        available = available_count(row, anchors, pivots)
        require(m1 == len(available) and p1 in available,
                (lineage, ri, m1, p1, available))
        pivotable_k19, p2_uses, k21_children = map(int, rest[6:9])
        require(0 <= pivotable_k19 <= 12 and p2_uses >= pivotable_k19,
                (lineage, ri, pivotable_k19, p2_uses))
        require(k21_children == 12 * p2_uses,
                (lineage, ri, k21_children, p2_uses))
        int(rest[9])
    require(observed_indices == expected_indices,
            (sorted(observed_indices), sorted(expected_indices)))
    return {
        "samples": 257,
        "distinct_R8_indices": len(observed_indices),
        "minimum_R8_index": min(observed_indices),
        "maximum_R8_index": max(observed_indices),
        "spacing_rule": "floor(j*484/256), j=0..256",
        "literal_row_and_factor_reconstruction": True,
        "source_mass_reconstruction": True,
        "first_pivot_availability_reconstruction": True,
    }


def main():
    paths = [STRUCTURE, AUX, CYCLE, PROVIDER, SOURCE, RESULT, SAMPLES]
    hashes = {path.name: digest(path) for path in paths}
    require(hashes == EXPECTED_HASHES, (hashes, EXPECTED_HASHES))
    result = json.loads(RESULT.read_text())
    require(result["status"] ==
            "PASS_COMPLETE_SEVEN_D17_R_2_2_K21_CHARGE", result["status"])
    require(int(result["scale_U"]) == U, result["scale_U"])
    require((result["records_consumed"], result["records_declared"],
             result["workers"], result["covered_ids"]) == (485, 485, 8, 7),
            result)
    require(0 < result["elapsed_seconds"] < 600, result["elapsed_seconds"])
    require(result["all_K21_children_irreducible"] is True, result)
    require([row["id"] for row in result["ids"]] == IDS,
            [row["id"] for row in result["ids"]])
    require(set(row["id"] for row in result["ids"]) == set(IDS), result["ids"])

    fields = ("raw_K17_heads", "pivotable_K17_heads", "selected_p1_uses",
              "K19_child_occurrences", "pivotable_K19_child_occurrences",
              "selected_p2_uses", "K21_terminal_occurrences")
    per_id = []
    total_charge_scaled = 0
    totals = {field: 0 for field in fields}
    for row in result["ids"]:
        expected = EXPECTED[row["id"]]
        observed = tuple(row[field] for field in fields) + (
            int(row["full_charge_scaled_U"]),)
        require(observed == expected, (row["id"], observed, expected))
        require(row["K19_child_occurrences"] == 12 * row["selected_p1_uses"], row)
        require(row["K21_terminal_occurrences"] == 12 * row["selected_p2_uses"], row)
        require(row["full_occurrences"] == row["irreducible_occurrences"] ==
                row["K21_terminal_occurrences"], row)
        require(row["full_charge_scaled_U"] == row["irreducible_charge_scaled_U"], row)
        for field in fields:
            totals[field] += row[field]
        scaled = int(row["full_charge_scaled_U"])
        total_charge_scaled += scaled
        per_id.append({
            "id": row["id"],
            "terminal_occurrences": row["K21_terminal_occurrences"],
            "charge_scaled_U": str(scaled),
            "charge": fraction_record(Fraction(scaled, U)),
        })

    expected_totals = {
        "raw_K17_heads": 82_938_880,
        "pivotable_K17_heads": 81_076_480,
        "selected_p1_uses": 267_564_800,
        "K19_child_occurrences": 3_210_777_600,
        "pivotable_K19_child_occurrences": 978_380_800,
        "selected_p2_uses": 1_448_947_200,
        "K21_terminal_occurrences": 17_387_366_400,
    }
    require(totals == expected_totals, (totals, expected_totals))
    require(total_charge_scaled == -196_205_097_632_820_756_480,
            total_charge_scaled)
    histogram = result["m1_m2_occurrence_hist"]
    require(sum(histogram.values()) == totals["pivotable_K19_child_occurrences"],
            histogram)
    require(sum(int(key.split("_")[1]) * value
                for key, value in histogram.items()) == totals["selected_p2_uses"],
            histogram)
    require(result["literal_first_compression"]["lookups"] ==
            totals["selected_p1_uses"], result["literal_first_compression"])
    require(result["literal_first_compression"]["peak_keys_per_R8_record"] ==
            551_680, result["literal_first_compression"])
    require(result["terminal_profile_cache"] ==
            {"hits": 1_362_609_882, "misses": 86_337_318},
            result["terminal_profile_cache"])

    anchors, records, pivots, factors = parse_structure()
    sample_audit = audit_samples(anchors, records, pivots, factors)
    source_text = SOURCE.read_text()
    source_guards = {
        "exact_literal_first_key": "row: Row,\n        p1: u8" in source_text,
        "second_pivot_from_literal_K19": "let ps2 = avail(s2, e);" in source_text,
        "terminal_literal_nonpivotability":
            "assert_eq!((full_n, irreducible_n), (12, 12));" in source_text,
        "exact_denominator_division":
            "assert_eq!(U21 % ((m1 * m2) as i128), 0);" in source_text,
        "second_response_sign":
            "let unit_weight = -U21 / ((m1 * m2) as i128);" in source_text,
        "record_bounded_caches":
            "Both caches are intentionally record-bounded" in source_text,
        "atomic_final_result": "rename(tmp, output).unwrap();" in source_text,
        "hard_runtime_gate": "assert!(elapsed < 600.0" in source_text,
    }
    require(all(source_guards.values()), source_guards)

    total_charge = Fraction(total_charge_scaled, U)
    audit = {
        "schema": "orbit0-k21-direct-k17-22-terminal-audit-v1",
        "status": "PASS_STRICT_SEVEN_ID_D17_R_2_2_TERMINAL_AUDIT",
        "scope": ("Exactly the seven requested direct-K17 R:2-2 lineage IDs; "
                  "no other K21 ID, row collection, or membership claim."),
        "coverage": {
            "expected_ids": IDS,
            "observed_ids": [row["id"] for row in result["ids"]],
            "strict_exact_set_and_order": True,
            "covered_ids": 7,
        },
        "per_id": per_id,
        "totals": {
            **totals,
            "full_and_irreducible_occurrences":
                totals["K21_terminal_occurrences"],
            "full_and_irreducible_charge_scaled_U": str(total_charge_scaled),
            "full_and_irreducible_charge": fraction_record(total_charge),
        },
        "terminal_guard": {
            "all_K21_children_irreducible": True,
            "proof_method": ("Every literal terminal response was evaluated by resp; "
                             "full_n=irreducible_n=12 and full_q=irreducible_q "
                             "were asserted for every second-pivot profile miss."),
        },
        "compression_guard": {
            "second_pivot_input": "complete literal sorted K17 row plus p1",
            "terminal_cache_key": "path profile, literal anchor signature, p2, degree=2",
            "terminal_cache_is_after_second_pivot": True,
            "peak_literal_keys_per_R8_record": 551_680,
            "no_row_checkpoint": True,
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
        "covered_ids": 7,
        "terminal_occurrences": totals["K21_terminal_occurrences"],
        "charge": str(total_charge),
        "logical_sha256": audit["logical_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
