#!/usr/bin/env python3
"""Independent K2-prefix and full K3/K4 hidden-child charge referee."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKET = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23"
PARENTS = ROOT / "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/parents_000_016.bin"
CHECKPOINT = PACKET / "k18_k2_canonical_prefix.bin"
PROFILE_LEDGER = PACKET / "hidden_child_profiles_prefix.bin"
RESULT = PACKET / "results_hidden_children_prefix.json"
CHARGE_REFEREE = PACKET / "results_hidden_profile_charge_referee.json"
SOURCE = PACKET / "run_hidden_children_prefix.rs"
DESIGN = ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/filtered_k24_reducer.py"
FULL_DIR = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-full-charge-2026-08-23"
FULL_SOURCE = FULL_DIR / "run_full_hidden_k3_k4_charge.rs"
FULL_RESULT = FULL_DIR / "results_full_hidden_k3_k4_charge.json"
MERGED_PROFILES = ROOT / "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/hidden_k16_second_pivot_profiles_full.bin"
VISIBLE_K19 = ROOT / "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json"
OUT = HERE / "results_hidden_children_prefix_referee.json"
U = 400_591_699_200


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path):
    spec = importlib.util.spec_from_file_location("hidden_children_design", path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


D = load(DESIGN)


def subtract(row, anchor):
    value = Counter(row)
    value.subtract(anchor)
    require(all(x >= 0 for x in value.values()), (row.hex(), anchor.hex()))
    return bytes(sorted(cell for cell, count in value.items()
                        for _ in range(count)))


def canonical(row):
    signature = D.CTX.signature(row)
    images = [(D.CTX.move_signature(signature, action), action)
              for action in D.H]
    best_signature = min(item[0] for item in images)
    return min(D.F.move_row(row, action) for moved, action in images
               if moved == best_signature)


def main():
    result = json.loads(RESULT.read_text())
    charge = json.loads(CHARGE_REFEREE.read_text())
    full = json.loads(FULL_RESULT.read_text())
    visible_k19 = json.loads(VISIBLE_K19.read_text())
    require(result["status"] == "PASS_MEASURED_CHILD_PREFIX", result["status"])
    require(charge["status"] == "PASS_INDEPENDENT_HIDDEN_PROFILE_CHARGES",
            charge["status"])
    require(full["status"] == "PASS_FULL_HIDDEN_K3_K4_IMMEDIATE_CHARGE",
            full["status"])

    raw = CHECKPOINT.read_bytes()
    require(raw[:8] == b"H18K2P1\0", raw[:8])
    require(int.from_bytes(raw[8:24], "little", signed=True) == U, "scale")
    require(int.from_bytes(raw[24:32], "little") == 0, "slice")
    parents = int.from_bytes(raw[32:40], "little")
    raw_children = int.from_bytes(raw[40:48], "little")
    support = int.from_bytes(raw[48:56], "little")
    record_size = int.from_bytes(raw[56:58], "little")
    require((parents, raw_children, support, record_size) ==
            (156_064, 12_655_104, 694_172, 76),
            (parents, raw_children, support, record_size))
    require(len(raw) == 64 + record_size * support ==
            result["K18_22"]["checkpoint_bytes"], len(raw))

    sample_positions = sorted({0, support - 1} |
                              {i * (support - 1) // 256 for i in range(257)})
    sample_set = set(sample_positions)
    sampled_records = {}
    prior = None
    weight_sum = 0
    pivotable_support = 0
    for index in range(support):
        item = raw[64 + 76 * index:64 + 76 * (index + 1)]
        row = item[:24]
        weight = int.from_bytes(item[24:40], "little", signed=True)
        pivotable = bool(item[40])
        require(item[40] in (0, 1) and weight and
                (prior is None or prior < row), (index, prior, row, weight))
        expected_pivotable = bool(D.CTX.pivots(D.CTX.signature(row)))
        require(pivotable == expected_pivotable, (index, pivotable, row.hex()))
        prior = row
        weight_sum += weight
        pivotable_support += pivotable
        if index in sample_set:
            sampled_records[index] = item
    require(weight_sum == int(result["K18_22"]["canonical_weight_sum_scaled"])
            == 12 * int(result["profile_weight_sum_scaled"]), weight_sum)
    require(pivotable_support == result["K18_22"]["canonical_pivotable_support"]
            == 408_972, pivotable_support)
    require(support - pivotable_support ==
            result["K18_22"]["canonical_irreducible_support"] == 285_200,
            support - pivotable_support)

    with PARENTS.open("rb") as parent_stream:
        header = parent_stream.read(40)
        require(header[:8] == b"H16RUN2\0" and
                int.from_bytes(header[8:24], "little", signed=True) == U,
                header[:24])
        for index, item in sampled_records.items():
            canonical_row = item[:24]
            aggregate_weight = int.from_bytes(item[24:40], "little", signed=True)
            pivotable = bool(item[40])
            parent = int.from_bytes(item[41:49], "little")
            pivot, tail_index, m2 = item[49:52]
            raw_child = item[52:76]
            require(parent < parents and pivot < 78 and tail_index < 12 and m2,
                    (index, parent, pivot, tail_index, m2))
            parent_stream.seek(40 + 64 * parent)
            source = parent_stream.read(64)
            parent_row = source[:24]
            parent_weight = int.from_bytes(source[24:40], "little", signed=True)
            parent_signature = tuple(source[40:52])
            second = D.CTX.pivots(parent_signature)
            require(len(second) == m2 and pivot in second and
                    parent_weight % m2 == 0,
                    (index, parent, pivot, second, m2))
            expected_raw = bytes(sorted(subtract(parent_row, D.CTX.anchors[pivot]) +
                                        D.CTX.tails[pivot][2][tail_index]))
            require(raw_child == expected_raw, (index, raw_child.hex(), expected_raw.hex()))
            require(canonical(raw_child) == canonical_row,
                    (index, raw_child.hex(), canonical_row.hex()))
            require(bool(D.CTX.pivots(D.CTX.signature(raw_child))) == pivotable,
                    (index, pivotable, raw_child.hex()))
            contribution = -parent_weight // m2
            require(parent_weight % m2 == 0 and contribution * aggregate_weight > 0,
                    (index, contribution, aggregate_weight))

    # Compact profile header/size and independent Rust charge replay already
    # establish every one of its 62,678 records and 5,766,376 tail guards.
    with PROFILE_LEDGER.open("rb") as stream:
        header = stream.read(64)
    require(header[:8] == b"HCPROF1\0" and
            int.from_bytes(header[8:24], "little", signed=True) == U and
            int.from_bytes(header[24:32], "little") == 0 and
            int.from_bytes(header[32:40], "little") == 62_678 and
            int.from_bytes(header[40:42], "little") == 90,
            header.hex())
    require(PROFILE_LEDGER.stat().st_size == 64 + 90 * 62_678,
            PROFILE_LEDGER.stat().st_size)
    require(charge["uses"] == result["outgoing_profile_uses"] == 1_054_592 and
            charge["abstract_literal_guards"] ==
            result["abstract_literal_cycle_guards"] == 5_766_376,
            charge)

    # The full charge program consumes the exact globally merged profile
    # stream.  Its source asserts strict PKey order, wildcard degree byte,
    # nonzero weights, EOF, common U, and the merged weight sum.  The prefix
    # literal replay independently validates both abstract response maps.
    with MERGED_PROFILES.open("rb") as stream:
        merged_header = stream.read(32)
    require(merged_header[:8] == b"H16MER2\0" and
            int.from_bytes(merged_header[8:24], "little", signed=True) == U and
            int.from_bytes(merged_header[24:32], "little") == 6_229_700,
            merged_header.hex())
    require(MERGED_PROFILES.stat().st_size == 32 + 59 * 6_229_700,
            MERGED_PROFILES.stat().st_size)
    require(full["scale"] == U and full["merged_profiles"] == 6_229_700 and
            full["merged_weight_sum_scaled"] == "146230609431055564800",
            full)
    require(full["literal_guard"]["keys"] == 62_678 and
            full["literal_guard"]["tail_checks"] == 5_766_376 and
            full["literal_guard"]["prefix_charges_scaled"] == [
                charge["K3"]["full_charge_scaled"],
                charge["K3"]["irreducible_charge_scaled"],
                charge["K4"]["full_charge_scaled"],
                charge["K4"]["irreducible_charge_scaled"],
            ], full["literal_guard"])
    hidden_k19 = Fraction(
        int(full["K19_path_23"]["irreducible_charge_scaled"]), U)
    hidden_k20 = Fraction(
        int(full["K20_path_24"]["irreducible_charge_scaled"]), U)
    require(hidden_k19 == Fraction(-45_729_991_456_828_928, 24_838_275),
            hidden_k19)
    require(hidden_k20 == Fraction(1_850_432_653_709_056, 10_227_525),
            hidden_k20)
    old_k19 = Fraction(
        visible_k19["combined"]["K19_irreducible_charge"]["numerator"],
        visible_k19["combined"]["K19_irreducible_charge"]["denominator"])
    corrected_k19 = old_k19 + hidden_k19
    require(corrected_k19 ==
            Fraction(-2_117_855_228_554_753_792, 173_867_925), corrected_k19)

    output = {
        "status": "PASS_INDEPENDENT_HIDDEN_CHILD_REFEREE",
        "K2": {
            "parent_occurrences": parents,
            "raw_children": raw_children,
            "canonical_nonzero": support,
            "canonical_pivotable_support": pivotable_support,
            "canonical_irreducible_support": support - pivotable_support,
            "canonical_weight_sum_scaled": str(weight_sum),
            "sampled_witnesses_source_replayed": len(sampled_records),
        },
        "K3": charge["K3"],
        "K4": charge["K4"],
        "profile": {
            "keys": charge["profile_keys"],
            "uses": charge["uses"],
            "weight_sum_scaled": charge["weight_sum_scaled"],
            "abstract_literal_guards": charge["abstract_literal_guards"],
        },
        "full_hidden_charge": {
            "profiles": full["merged_profiles"],
            "merged_weight_sum_scaled": full["merged_weight_sum_scaled"],
            "K19_path_23_irreducible_scaled":
                full["K19_path_23"]["irreducible_charge_scaled"],
            "K19_path_23_irreducible": str(hidden_k19),
            "corrected_K19_aggregate": str(corrected_k19),
            "K20_path_24_irreducible_scaled":
                full["K20_path_24"]["irreducible_charge_scaled"],
            "K20_path_24_irreducible": str(hidden_k20),
            "K20_scope": "This repairs path [2,4] only; the K20 aggregate remains incomplete.",
        },
        "sign_and_counts": {
            "outgoing_weight": "w2=-w1/m2",
            "tail_counts": {"K2": 12, "K3": 32, "K4": 60},
            "scale": U,
        },
        "scope": ("K2 is a one-H-slice measured prefix. K3/K4 charges are "
                  "complete over the globally merged hidden profiles. No full "
                  "K2 collection or downstream reduction."),
        "pinned": {
            str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in (SOURCE, RESULT, CHECKPOINT, PROFILE_LEDGER,
                         CHARGE_REFEREE, DESIGN, PARENTS, FULL_SOURCE,
                         FULL_RESULT, MERGED_PROFILES, VISIBLE_K19)
        },
    }
    logical = json.dumps(output, sort_keys=True, separators=(",", ":"))
    output["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
