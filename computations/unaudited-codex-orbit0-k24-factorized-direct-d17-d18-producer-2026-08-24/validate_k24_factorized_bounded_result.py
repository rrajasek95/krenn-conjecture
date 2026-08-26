#!/usr/bin/env python3
"""Fail-closed structural, hash, arithmetic, and ledger validator for prefix1."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys


U24 = 400_591_699_200
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OLD_SCHEMA = (ROOT / "computations/unaudited-codex-orbit0-k24-residual-direct-d17-d18-gate-2026-08-24"
              / "factorized_k24_residual_interface.schema.json")
SCHEMA = HERE / "factorized_k24_bounded_result.schema.json"
IDS17 = ["D17:234|R:3-4", "D17:243|R:3-4", "D17:324|R:3-4",
         "D17:333|R:3-4", "D17:342|R:3-4", "D17:423|R:3-4",
         "D17:432|R:3-4"]
IDS18 = ["D18:244|R:2-4", "D18:334|R:2-4", "D18:343|R:2-4",
         "D18:424|R:2-4", "D18:433|R:2-4", "D18:442|R:2-4"]
GIDS = ["source_D17_R3_4", "source_D18_R2_4"]
P2 = {GIDS[0]: 1_736_704, GIDS[1]: 476_160}
FIXED_COUNTS = {
    GIDS[0]: {
        "source_heads": 171_008, "pivotable_source_heads": 167_168,
        "p1_uses": 551_680, "intermediate_children": 17_653_760,
        "pivotable_intermediate_children": 1_736_704,
    },
    GIDS[1]: {
        "source_heads": 313_920, "pivotable_source_heads": 284_160,
        "p1_uses": 537_600, "intermediate_children": 6_451_200,
        "pivotable_intermediate_children": 476_160,
    },
}
INPUTS = {
    "orbit0_structure": (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin",
                         "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b"),
    "response_aux": (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin",
                     "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab"),
    "response_k4": (ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin",
                    "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3"),
    "cycle_aux": (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin",
                  "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7"),
    "factorized_provider": (ROOT / "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23/k24_factorized_gram_provider.py",
                            "29075c59bdc72237c9e88cd8df360dfcb5184968c4824556032b437f8fb8112d"),
    "interface_schema": (OLD_SCHEMA,
                         "dd93eab99a72b9464ef35f3793d0068fdd86842fa2da33da9b02b986cf3e3dbe"),
}
TOP_KEYS = {
    "status", "format", "degree", "covered_lineage_ids", "recurrence_policy",
    "source_interval", "source_slices", "workers", "scale_U",
    "column_orbit_runs", "groups", "literal_samples", "H_collection_cache",
    "input_sha256", "engine_sha256", "exact_H_collection",
    "raw_labelled_column_runs_retained", "canonical_column_runs_retained",
    "all_K24_children_terminal", "compression", "resource_gates",
    "timings_seconds", "production_mode", "scope",
}
RUN_KEYS = {
    "group_id", "source_interval", "input_sha256", "engine_sha256",
    "content_sha256", "selected_pivot_occurrences", "nonzero_column_orbits",
    "exact_zero_cancellations", "all_orbit_divisions_exact", "record_format",
}
GROUP_KEYS = {
    "group_id", "ids", "source_heads", "pivotable_source_heads", "p1_uses",
    "intermediate_children", "pivotable_intermediate_children",
    "selected_pivot_occurrences", "K24_terminal_occurrences",
    "raw_sorted_runs", "exact_labelled_nonzero_columns",
    "exact_labelled_zero_cancellations", "H_canonical_sorted_runs",
    "nonzero_column_orbits", "canonical_zero_cancellations",
    "all_orbit_divisions_exact", "orbit_size_histogram",
    "orbit_total_mass_scaled_U", "derived_row_mass_scaled_U",
    "derived_charge_scaled_U", "derived_charge",
    "on_demand_60_output_checks", "top_self_pairing_checks", "content_path",
    "content_sha256", "content_bytes",
}
RECORD_FORMAT = ("canonical_column_key<TAB>column_orbit_size<TAB>"
                 "orbit_total_mass_numerator<TAB>orbit_total_mass_denominator<TAB>"
                 "per_labelled_column_coefficient_numerator<TAB>"
                 "per_labelled_column_coefficient_denominator")
WITNESS_HEADER = (
    "group_id\tlineage_id\tsample_bin\tglobal_selected_pivot_rank\t"
    "source_cursor\tp1\tt1\tp2\tm1\tm2\tsource_row\tK20_parent_row\t"
    "mixed_word\tU20_multiplier\tcanonical_column_key\tcolumn_orbit_size\t"
    "H_action_to_canonical\texact_coefficient_numerator\t"
    "exact_coefficient_denominator\tliteral_K24_row\ttop_output_count\t"
    "top_charge_sum\ttop_self_pairing\tliteral_K24_terminal"
)


class ValidationError(RuntimeError):
    pass


def require(condition, detail):
    if not condition:
        raise ValidationError(detail)


def exact_keys(value, expected, where):
    require(type(value) is dict, f"{where}: expected object")
    got = set(value)
    require(got == expected,
            f"{where}: key mismatch missing={sorted(expected-got)} extra={sorted(got-expected)}")


def integer(value, where, minimum=0):
    require(type(value) is int and value >= minimum, f"{where}: bad integer")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha_text(value, where):
    require(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value),
            f"{where}: not sha256")


def resolve_artifact(raw, result_path):
    require(type(raw) is str and raw, "artifact path missing")
    path = Path(raw)
    if not path.is_absolute():
        cwd_path = ROOT / path
        path = cwd_path if cwd_path.exists() else result_path.parent / path
    return path.resolve()


def validate_tsv(path, expected_sha, expected_bytes, expected_count, expected_hist):
    """Validate every exact orbit division; exposed for hostile unit tests."""
    require(path.is_file(), f"missing TSV {path}")
    require(path.stat().st_size == expected_bytes, f"TSV byte count {path}")
    require(sha256(path) == expected_sha, f"TSV hash {path}")
    count = 0
    mass = 0
    histogram = {}
    previous = None
    with path.open("rt", encoding="ascii", newline="") as stream:
        for line_number, raw in enumerate(stream, 1):
            require(raw.endswith("\n"), f"TSV line {line_number}: missing LF")
            fields = raw[:-1].split("\t")
            require(len(fields) == 6, f"TSV line {line_number}: field count")
            key, orbit_s, wn_s, wd_s, an_s, ad_s = fields
            require(re.fullmatch(r"[0-2]{8}:[0-9a-f]{40}", key) is not None,
                    f"TSV line {line_number}: key")
            require(previous is None or previous < key,
                    f"TSV line {line_number}: not strict sorted unique")
            previous = key
            try:
                orbit = int(orbit_s)
                w = Fraction(int(wn_s), int(wd_s))
                alpha = Fraction(int(an_s), int(ad_s))
            except (ValueError, ZeroDivisionError) as exc:
                raise ValidationError(f"TSV line {line_number}: fraction") from exc
            require(orbit > 0 and 384 % orbit == 0,
                    f"TSV line {line_number}: invalid H orbit")
            require(w != 0, f"TSV line {line_number}: zero retained mass")
            require(alpha * orbit == w,
                    f"TSV line {line_number}: inexact orbit division")
            scaled = w * U24
            require(scaled.denominator == 1,
                    f"TSV line {line_number}: mass not on U24 lattice")
            mass += scaled.numerator
            histogram[str(orbit)] = histogram.get(str(orbit), 0) + 1
            count += 1
    require(count == expected_count, f"TSV count {path}: {count} != {expected_count}")
    require(histogram == expected_hist, f"TSV orbit histogram {path}")
    return mass


def validate_witness(path, metadata):
    exact_keys(metadata, {"count", "path", "sha256",
                           "all_replay_top_60_charge_mass_pairing_and_terminality"},
               "literal_samples")
    require(metadata["count"] == 257, "literal sample count metadata")
    require(metadata["all_replay_top_60_charge_mass_pairing_and_terminality"] is True,
            "literal replay assertion")
    require(path.is_file() and sha256(path) == metadata["sha256"], "witness hash")
    lines = path.read_text(encoding="ascii").splitlines()
    require(len(lines) == 258 and lines[0] == WITNESS_HEADER, "witness schema/count")
    seen = []
    prior_rank = -1
    for number, line in enumerate(lines[1:], 1):
        fields = line.split("\t")
        require(len(fields) == 24, f"witness {number}: field count")
        group, lineage = fields[:2]
        require(group in GIDS, f"witness {number}: group")
        require(lineage in (IDS17 if group == GIDS[0] else IDS18),
                f"witness {number}: lineage")
        try:
            sample_bin, rank = int(fields[2]), int(fields[3])
            p1, tail, p2, m1, m2 = map(int, fields[5:10])
            orbit, action = int(fields[15]), int(fields[16])
            coefficient = Fraction(int(fields[17]), int(fields[18]))
            outputs, _charge, pairing, terminal = map(int, fields[20:24])
        except (ValueError, ZeroDivisionError) as exc:
            raise ValidationError(f"witness {number}: integer/fraction") from exc
        require(sample_bin == number - 1, f"witness {number}: bin distribution")
        require(rank > prior_rank, f"witness {number}: rank order")
        prior_rank = rank
        require(0 <= p1 < 78 and 0 <= p2 < 78 and tail >= 0 and m1 > 0 and m2 > 0,
                f"witness {number}: pivot/divisor fields")
        require(orbit > 0 and 384 % orbit == 0 and 0 <= action < 384,
                f"witness {number}: H fields")
        require(coefficient != 0, f"witness {number}: zero coefficient")
        require(re.fullmatch(r"[0-9a-f]{48}", fields[10]) is not None and
                re.fullmatch(r"[0-9a-f]{48}", fields[11]) is not None and
                re.fullmatch(r"[0-9a-f]{48}", fields[19]) is not None,
                f"witness {number}: row encoding")
        require(re.fullmatch(r"[0-2]{8}", fields[12]) is not None and
                re.fullmatch(r"[0-9a-f]{40}", fields[13]) is not None and
                re.fullmatch(r"[0-2]{8}:[0-9a-f]{40}", fields[14]) is not None,
                f"witness {number}: factorized column encoding")
        require((outputs, pairing, terminal) == (60, 60, 1),
                f"witness {number}: output/pairing/terminal guard")
        seen.append(sample_bin)
    require(seen == list(range(257)), "witness bins not exact 0..256")


def validate_contract_schema():
    schema = json.loads(SCHEMA.read_text())
    require(schema["$id"] == "factorized-k24-direct-d17-d18-bounded-source-result-v2",
            "production-result schema id")
    require(schema.get("additionalProperties") is False, "schema top level not closed")
    require(set(schema["required"]) == TOP_KEYS and set(schema["properties"]) == TOP_KEYS,
            "schema/validator top-level key drift")
    require(set(schema["$defs"]["column_run"]["required"]) == RUN_KEYS and
            set(schema["$defs"]["column_run"]["properties"]) == RUN_KEYS and
            schema["$defs"]["column_run"]["additionalProperties"] is False,
            "schema/validator column-run drift")
    require(set(schema["$defs"]["group"]["required"]) == GROUP_KEYS and
            set(schema["$defs"]["group"]["properties"]) == GROUP_KEYS and
            schema["$defs"]["group"]["additionalProperties"] is False,
            "schema/validator group drift")
    require(schema["$defs"]["literal_samples"]["additionalProperties"] is False,
            "literal-sample schema not closed")
    require(schema["x-supersedes"]["sha256"] == INPUTS["interface_schema"][1],
            "old schema supersession hash")
    return schema


def validate(result_path, engine_source):
    validate_contract_schema()
    data = json.loads(result_path.read_text())
    exact_keys(data, TOP_KEYS, "result")
    require(data["status"] == "PASS_BOUNDED_FACTORIZED_K24_DIRECT_D17_D18_PREFIX",
            "status")
    require(data["format"] == "factorized-k24-H-column-orbit-residual-v1", "format")
    require(data["degree"] == 24, "degree")
    require(data["covered_lineage_ids"] == IDS17 + IDS18, "strict 13-ID coverage/order")
    require(data["recurrence_policy"] ==
            "all_literal_dividing_pivots_occurrencewise_average_v1", "recurrence")
    interval = data["source_interval"]
    require(type(interval) is list and len(interval) == 2 and
            all(type(x) is int for x in interval), "bounded source interval")
    slices = interval[1] - interval[0]
    require(interval[0] == 0 and slices in (1, 8) and data["source_slices"] == slices,
            "sealed prefix1/prefix8 interval")
    require(type(data["workers"]) is int and 1 <= data["workers"] <= min(8, slices),
            "bounded workers")
    require(data["scale_U"] == U24, "U24")
    require(data["production_mode"] is False, "prefix1 must not claim production")
    require(data["exact_H_collection"] is True and
            data["raw_labelled_column_runs_retained"] is True and
            data["canonical_column_runs_retained"] is True and
            data["all_K24_children_terminal"] is True, "global exact guards")
    require(type(data["scope"]) is str and "no 61/full run" in data["scope"], "scope")
    exact_keys(data["literal_samples"], {"count", "path", "sha256",
               "all_replay_top_60_charge_mass_pairing_and_terminality"},
               "literal_samples")

    sha_text(data["engine_sha256"], "engine_sha256")
    require(engine_source.is_file() and sha256(engine_source) == data["engine_sha256"],
            "engine source hash")
    exact_keys(data["input_sha256"], set(INPUTS), "input_sha256")
    for name, (path, expected) in INPUTS.items():
        require(path.is_file() and sha256(path) == expected, f"pinned input file {name}")
        require(data["input_sha256"][name] == expected, f"pinned input result {name}")
    exact_keys(data["H_collection_cache"],
               {"hits", "misses", "clears_at_cap", "peak_keys", "hard_cap"}, "cache")
    for key in data["H_collection_cache"]:
        integer(data["H_collection_cache"][key], f"cache.{key}")
    require(data["H_collection_cache"]["peak_keys"] <=
            data["H_collection_cache"]["hard_cap"], "cache hard cap")

    runs = data["column_orbit_runs"]
    groups = data["groups"]
    require(type(runs) is list and type(groups) is list and len(runs) == len(groups) == 2,
            "two strict group records")
    require([x.get("group_id") for x in runs] == GIDS and
            [x.get("group_id") for x in groups] == GIDS, "strict group order")
    total_p2 = 0
    total_terminal = 0
    for index, (run, group) in enumerate(zip(runs, groups)):
        gid = GIDS[index]
        exact_keys(run, RUN_KEYS, f"run.{gid}")
        exact_keys(group, GROUP_KEYS, f"group.{gid}")
        require(run["source_interval"] == interval, f"run interval {gid}")
        exact_keys(run["input_sha256"], {"orbit0_structure", "response_aux", "response_k4", "cycle_aux"},
                   f"run inputs {gid}")
        for name in run["input_sha256"]:
            require(run["input_sha256"][name] == INPUTS[name][1], f"run input {gid}.{name}")
        require(run["engine_sha256"] == data["engine_sha256"], f"run engine {gid}")
        require(run["record_format"] == RECORD_FORMAT, f"run record format {gid}")
        require(run["all_orbit_divisions_exact"] is True and
                group["all_orbit_divisions_exact"] is True, f"orbit assertion {gid}")
        require(group["ids"] == (IDS17 if index == 0 else IDS18), f"group IDs {gid}")
        for name, expected in FIXED_COUNTS[gid].items():
            require(group[name] == slices * expected, f"fixed source count {gid}.{name}")
        expected_p2 = slices * P2[gid]
        require(run["selected_pivot_occurrences"] == group["selected_pivot_occurrences"] == expected_p2,
                f"p2 count {gid}")
        require(group["K24_terminal_occurrences"] == 60 * expected_p2, f"K24 fan {gid}")
        for name in ("raw_sorted_runs", "exact_labelled_nonzero_columns",
                     "exact_labelled_zero_cancellations", "H_canonical_sorted_runs",
                     "nonzero_column_orbits", "canonical_zero_cancellations",
                     "on_demand_60_output_checks", "top_self_pairing_checks", "content_bytes"):
            integer(group[name], f"group.{gid}.{name}")
        require(run["nonzero_column_orbits"] == group["nonzero_column_orbits"],
                f"orbit count {gid}")
        require(run["exact_zero_cancellations"] ==
                group["exact_labelled_zero_cancellations"] + group["canonical_zero_cancellations"],
                f"zero count {gid}")
        require(group["on_demand_60_output_checks"] == group["nonzero_column_orbits"] and
                group["top_self_pairing_checks"] == 60 * group["nonzero_column_orbits"],
                f"on-demand checks {gid}")
        sha_text(run["content_sha256"], f"run content sha {gid}")
        require(run["content_sha256"] == group["content_sha256"], f"content hash join {gid}")
        require(type(group["orbit_size_histogram"]) is dict and
                all(re.fullmatch(r"[1-9][0-9]*", key) and type(value) is int and value >= 0
                    for key, value in group["orbit_size_histogram"].items()),
                f"orbit histogram schema {gid}")
        path = resolve_artifact(group["content_path"], result_path)
        mass = validate_tsv(path, group["content_sha256"], group["content_bytes"],
                            group["nonzero_column_orbits"], group["orbit_size_histogram"])
        require(mass == int(group["orbit_total_mass_scaled_U"]), f"orbit mass {gid}")
        require(int(group["derived_row_mass_scaled_U"]) == 60 * mass, f"row mass {gid}")
        charge = Fraction(group["derived_charge"])
        require(charge * U24 == int(group["derived_charge_scaled_U"]), f"charge/U {gid}")
        total_p2 += expected_p2
        total_terminal += group["K24_terminal_occurrences"]

    witness = resolve_artifact(data["literal_samples"]["path"], result_path)
    validate_witness(witness, data["literal_samples"])

    exact_keys(data["compression"], {"row_fan_avoided", "materialized_row_logical_bytes",
               "factorized_raw_logical_bytes", "logical_byte_ratio",
               "retained_tree_bytes_before_result", "empirical_materialized_to_retained_ratio"},
               "compression")
    compression = data["compression"]
    require(compression["row_fan_avoided"] == 60, "row fan")
    require(compression["materialized_row_logical_bytes"] == total_terminal * 40,
            "materialized logical bytes")
    require(compression["factorized_raw_logical_bytes"] == total_p2 * 37,
            "factor raw logical bytes")
    require(abs(compression["logical_byte_ratio"] -
                compression["materialized_row_logical_bytes"] /
                compression["factorized_raw_logical_bytes"]) < 1e-6,
            "logical compression ratio")

    exact_keys(data["resource_gates"], {"hard_wall_seconds", "disk_cap_bytes",
               "theoretical_raw_column_bytes", "actual_tree_bytes_before_result"},
               "resource_gates")
    gates = data["resource_gates"]
    require(gates["hard_wall_seconds"] == 540 and gates["disk_cap_bytes"] > 0,
            "wall/disk gates")
    require(gates["theoretical_raw_column_bytes"] == total_p2 * 37,
            "theoretical raw bytes")
    require(gates["actual_tree_bytes_before_result"] ==
            compression["retained_tree_bytes_before_result"] <= gates["disk_cap_bytes"],
            "retained disk gate")
    require(abs(compression["empirical_materialized_to_retained_ratio"] -
                compression["materialized_row_logical_bytes"] /
                compression["retained_tree_bytes_before_result"]) < 1e-6,
            "empirical compression ratio")

    exact_keys(data["timings_seconds"], {"source_emit", "exact_labelled_merge_and_H_collection",
               "canonical_merge_and_on_demand_checks", "total", "linear_projected_full"},
               "timings")
    timing = data["timings_seconds"]
    require(all(type(value) in (int, float) and value >= 0 for value in timing.values()),
            "timing values")
    require(abs(timing["total"] - timing["source_emit"] -
                timing["exact_labelled_merge_and_H_collection"] -
                timing["canonical_merge_and_on_demand_checks"]) < 0.01, "timing sum")
    require(abs(timing["linear_projected_full"] - timing["total"] * 485 / slices) < 0.01,
            "linear projection")
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--engine-source", type=Path, required=True)
    args = parser.parse_args()
    try:
        data = validate(args.result.resolve(), args.engine_source.resolve())
    except (ValidationError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps({
        "status": "PASS_FAIL_CLOSED_K24_FACTORIZED_BOUNDED_RESULT",
        "result": str(args.result),
        "source_interval": data["source_interval"],
        "groups": [x["group_id"] for x in data["groups"]],
        "column_orbits": sum(x["nonzero_column_orbits"] for x in data["groups"]),
        "literal_witnesses": data["literal_samples"]["count"],
        "all_record_orbit_divisions_replayed": True,
        "all_content_and_source_hashes_replayed": True,
    }, indent=2))


if __name__ == "__main__":
    main()
