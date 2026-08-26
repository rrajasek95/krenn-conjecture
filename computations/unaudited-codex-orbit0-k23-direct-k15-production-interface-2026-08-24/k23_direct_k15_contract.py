#!/usr/bin/env python3
"""Strict shared contract for K23 grouped direct-K15 production shards."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k15-four-sink-2026-08-24"
U = 400_591_699_200
SLICES = 485
HEADS_PER_SLICE = 13_824
INTERVALS = [(0, 60), (60, 121), (121, 181), (181, 242),
             (242, 303), (303, 363), (363, 424), (424, 485)]
NAMES = [
    "D15:{223,232,322}|R:2-2-4",
    "D15:{223,232,322}|R:2-3-3",
    "D15:{223,232,322}|R:3-2-3",
    "D15:{223,232,322}|R:4-4",
]
PATHS = [[2, 2, 4], [2, 3, 3], [3, 2, 3], [4, 4]]
GROUP_IDS = ["source_D15_R2_2_4", "source_D15_R2_3_3",
             "source_D15_R3_2_3", "source_D15_R4_4"]
IDS = {
    name: [f"D15:{packet}|R:{'-'.join(map(str, path))}"
           for packet in (223, 232, 322)]
    for name, path in zip(NAMES, PATHS)
}
PINS = {
    "producer_source": (GATE / "run_k23_direct_k15_four_sink.rs",
                        "c3ea65b5ac1221e1b0020e2f0a9753bd774826059ae16e24c05cd4f6f5706e8c"),
    "producer_binary": (GATE / "run_k23_direct_k15_four_sink",
                        "a6bc9f1f1b217a4cfc8dc662ea1358e4c3ac012f40c49e6c07cf05b1e52faa04"),
    "structure": (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin",
                  "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b"),
    "response_aux": (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin",
                     "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab"),
    "cycle_aux": (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin",
                  "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7"),
    "K4_aux": (ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin",
               "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3"),
    "included_engine": (ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs",
                        "24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045"),
}
TOP_KEYS = {
    "status", "scale_U", "slice_interval", "source_slices",
    "source_heads_per_slice", "workers", "sinks", "packet_grouping_guard",
    "sign_rule", "terminality", "scope", "elapsed_seconds",
    "projected_full_seconds",
}
SINK_KEYS = {
    "ids", "individual_id_charges", "degrees", "source_heads",
    "source_mass", "source_l1", "stage_pivot_uses",
    "stage_tail_candidates", "stage_pivotable_children",
    "terminal_response_keys_evaluated", "terminal_K23_occurrences",
    "full_occurrences", "irreducible_occurrences", "full_charge_scaled_U",
    "irreducible_charge_scaled_U", "denominator_product_hist",
}
PACKET_GUARD = "packet witnesses 322/232/223 retained only as grouped source classes; no individual scalar split"
SIGN_RULE = "direct K15 head is -positive; every selected pivot flips sign and divides by its occurrencewise multiplicity; U is exactly divisible by every recorded denominator product"
TERMINALITY = "every realized final response key is exhaustively expanded; all K23 outputs have anchor-signature mass 1 below pivot mass 4, so full equals irreducible"
SCOPE = "four separate grouped scalar K23 sinks covering exactly 12 IDs; no rows, K24, membership, or conjecture verdict"


class ContractError(RuntimeError):
    pass


def require(condition, detail):
    if not condition:
        raise ContractError(detail)


def exact_keys(value, expected, where):
    require(type(value) is dict, f"{where}: expected object")
    actual = set(value)
    require(actual == expected,
            f"{where}: missing={sorted(expected-actual)} extra={sorted(actual-expected)}")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_pins():
    for name, (path, expected) in PINS.items():
        require(path.is_file(), f"missing pinned {name}: {path}")
        require(sha256(path) == expected, f"hash drift in {name}")


def parse_integer(value, where):
    require(type(value) in (str, int) and type(value) is not bool, f"{where}: integer encoding")
    try:
        return int(value)
    except ValueError as error:
        raise ContractError(f"{where}: bad integer") from error


def validate_interval_set(intervals):
    normalized = [tuple(value) for value in intervals]
    require(normalized == INTERVALS, f"interval ledger mismatch: {normalized}")
    require(normalized[0][0] == 0 and normalized[-1][1] == SLICES,
            "interval endpoints")
    require(all(left[1] == right[0] for left, right in zip(normalized, normalized[1:])),
            "interval gap/overlap")
    return normalized


def validate_result_data(data, expected_interval=None, production=True):
    exact_keys(data, TOP_KEYS, "result")
    interval = data["slice_interval"]
    require(type(interval) is list and len(interval) == 2 and
            all(type(value) is int for value in interval), "slice interval schema")
    begin, end = interval
    count = end - begin
    require(0 <= begin < end <= SLICES, "slice interval range")
    if expected_interval is not None:
        require((begin, end) == tuple(expected_interval), "wrong named interval")
    if production:
        require((begin, end) in INTERVALS, "not a sealed production interval")
        require(data["status"] == "PASS_BOUNDED_GROUPED_DIRECT_K15_FOUR_SINK_K23_GATE",
                "production shard status")
        require(data["workers"] == 8, "production workers")
    else:
        require(data["status"] in {
            "PASS_BOUNDED_GROUPED_DIRECT_K15_FOUR_SINK_K23_GATE",
            "PASS_COMPLETE_GROUPED_DIRECT_K15_FOUR_SINK_K23_CHARGE"}, "result status")
    require(parse_integer(data["scale_U"], "scale_U") == U, "U23")
    require(data["source_slices"] == count and
            data["source_heads_per_slice"] == HEADS_PER_SLICE, "source slice/head counts")
    require(type(data["workers"]) is int and 1 <= data["workers"] <= 8, "workers")
    require(data["packet_grouping_guard"] == PACKET_GUARD, "packet grouping guard")
    require(data["sign_rule"] == SIGN_RULE, "sign rule")
    require(data["terminality"] == TERMINALITY, "terminality theorem")
    require(data["scope"] == SCOPE, "scope")
    require(type(data["elapsed_seconds"]) in (int, float) and
            0 <= data["elapsed_seconds"] < 600, "elapsed wall gate")
    require(type(data["projected_full_seconds"]) in (int, float) and
            abs(data["projected_full_seconds"] - data["elapsed_seconds"] * SLICES / count) < 0.02,
            "full wall projection")
    exact_keys(data["sinks"], set(NAMES), "sinks")
    common_mass = set()
    common_l1 = set()
    for name, degrees in zip(NAMES, PATHS):
        sink = data["sinks"][name]
        exact_keys(sink, SINK_KEYS, name)
        require(sink["ids"] == IDS[name] and sink["degrees"] == degrees,
                f"{name}: strict IDs/path")
        require(sink["individual_id_charges"] is None,
                f"{name}: forbidden individual scalar split")
        require(sink["source_heads"] == count * HEADS_PER_SLICE, f"{name}: source heads")
        mass = parse_integer(sink["source_mass"], f"{name}.source_mass")
        l1 = parse_integer(sink["source_l1"], f"{name}.source_l1")
        require(l1 >= abs(mass), f"{name}: source l1")
        common_mass.add(mass)
        common_l1.add(l1)
        for key, length in (("stage_pivot_uses", 3), ("stage_tail_candidates", 3),
                            ("stage_pivotable_children", 2)):
            values = sink[key]
            require(type(values) is list and len(values) == length and
                    all(type(value) is int and value >= 0 for value in values),
                    f"{name}.{key}")
        for key in ("terminal_response_keys_evaluated", "terminal_K23_occurrences",
                    "full_occurrences", "irreducible_occurrences"):
            require(type(sink[key]) is int and sink[key] >= 0, f"{name}.{key}")
        terminal = sink["terminal_K23_occurrences"]
        require(terminal == sink["full_occurrences"] == sink["irreducible_occurrences"],
                f"{name}: full != irreducible occurrence")
        final_stage = 2 if len(degrees) == 3 else 1
        require(terminal == sink["stage_tail_candidates"][final_stage],
                f"{name}: terminal tail census")
        if len(degrees) == 2:
            require(sink["stage_pivot_uses"][2] == sink["stage_tail_candidates"][2] == 0,
                    f"{name}: phantom third stage")
        full_charge = parse_integer(sink["full_charge_scaled_U"], f"{name}.full_charge")
        irreducible = parse_integer(sink["irreducible_charge_scaled_U"], f"{name}.irreducible")
        require(full_charge == irreducible, f"{name}: full != irreducible charge")
        histogram = sink["denominator_product_hist"]
        require(type(histogram) is dict and histogram, f"{name}: denominator histogram")
        total_final_pivots = 0
        for denominator, occurrences in histogram.items():
            try:
                divisor = int(denominator)
            except ValueError as error:
                raise ContractError(f"{name}: denominator key") from error
            require(str(divisor) == denominator and divisor > 0 and U % divisor == 0,
                    f"{name}: nondividing denominator {denominator}")
            require(type(occurrences) is int and occurrences > 0,
                    f"{name}: histogram occurrence")
            total_final_pivots += occurrences
        tails = {2: 12, 3: 32, 4: 60}[degrees[-1]]
        require(terminal == tails * total_final_pivots,
                f"{name}: final pivot/tail identity")
    require(len(common_mass) == len(common_l1) == 1, "sink source mass/l1 mismatch")
    return data


def validate_result(path, expected_interval=None, production=True):
    verify_pins()
    require(path.is_file(), f"missing shard result {path}")
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise ContractError(f"invalid JSON {path}") from error
    validate_result_data(data, expected_interval, production)
    return data, sha256(path)
