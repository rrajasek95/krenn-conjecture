#!/usr/bin/env python3
"""Independent, fail-closed audit of the fast K14 K24 charge-only engine.

This does not authorize a full run.  It validates the raw-result contract,
crosschecks exact source record zero against the sealed physical consumer, and
records why the raw fast ledger alone is not a production acceptance envelope.
"""

import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FAST = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24"
SEALED = ROOT / "computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24"

U = 400_591_699_200
IDS = ["D14:222|R:3-3-4", "D14:222|R:4-2-4"]
DEGREES = {IDS[0]: (3, 3, 4), IDS[1]: (4, 2, 4)}
TAILS = {2: 12, 3: 32, 4: 60}

PINS = {
    "fast_source": (FAST / "run_k24_charge_k14_source.rs", "dd9510f3324b160a3b496ba6d0b5bdfb9335699a1fc99cd75c18dadaf8eeca6d"),
    "fast_binary": (FAST / "run_k24_charge_k14_source", "4049688d492ee604ead3b43e1bb3f42efb42e9da7758c8128b08f67377469853"),
    "legacy_validator": (FAST / "validate_k14_source.py", "28bcd5552d43adaf800514ba6acdab89abb0ed143d3a598b6e84567c87bc891a"),
    "fast_prefix1": (FAST / "results_k14_source_prefix1.json", "1fd01ee42e4e0b8548794a58a8de7702791c59afeb8ad16e39ee0b5e37781083"),
    "fast_prefix8": (FAST / "results_k14_source_prefix8.json", "2dbbd7c0633c0719336dbb8f2b164f6cec522afdbc04da879e58ac379f714013"),
    "fast_full_result": (FAST / "results_k14_source_complete.json", "f188ec896a6782cff185c91b369b9e71fcbe661bbafbe61d625cdc51e02ba442"),
    "fast_full_samples": (FAST / "results_k14_source_complete.json.samples.tsv", "5d881350559aa3253e9aa60545bf6b8af62d9db7e8d5b9871f69ccea735554cf"),
    "fast_full_legacy_validation": (FAST / "results_k14_source_complete_validation.json", "dfcce3bb5c8aebf6b9f41245a3caa754bd6181b5917ac3a9556244b4daf5a747"),
    "raw_result_schema": (HERE / "k24_fast_k14_result.schema.json", "1eab6b6678f9a8f84381b113cb980f88949a1d65c63f388b23f67ceaabe9840d"),
    "sealed_source": (SEALED / "run_k24_charge_physical.rs", "10670f0687168d4383cfeb679ce8521d4c8b1b5621092b7600a3ef1b6ee79f51"),
    "sealed_binary": (SEALED / "run_k24_charge_physical", "21ef771613369867a4bb0bad7257cd7e04da11dffad68061b6f4c56dff231c8a"),
    "sealed_record0": (SEALED / "tiny_k14.json", "7e3533bac7eb87ba07af6d0238a13f06ade67aef59014a77724e40fe67f6ba5d"),
    "structure": (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin", "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b"),
    "aux": (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin", "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab"),
    "k4": (ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin", "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3"),
    "cycle": (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin", "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7"),
}

TOP_KEYS = {
    "status", "degree", "covered_lineage_ids", "scale_U", "R8_record_interval",
    "distributed_record_mode", "R8_records_consumed", "R8_records_declared",
    "source_heads", "source_mass_sum", "source_mass_l1", "sinks",
    "all_realized_cached_K24_responses_terminal", "literal_sample_guard", "sign_rule",
    "compression_proof", "shared_fold_scope", "terminal_cache_resource_guard", "workers",
    "elapsed_seconds", "projected_full_seconds_from_consumed_records", "scope",
}
SINK_KEYS = {
    "first_response_degree", "second_response_degree", "terminal_response_degree",
    "selected_p1_uses", "first_children", "pivotable_first_children", "selected_p2_uses",
    "second_children", "pivotable_second_children", "selected_p3_uses",
    "K24_terminal_occurrences", "full_occurrences", "irreducible_occurrences",
    "full_charge_scaled_U", "irreducible_charge_scaled_U", "first_denominator_hist",
    "second_denominator_hist", "third_denominator_hist", "product_denominator_hist",
    "plan_cache", "literal_preterminal_cache", "terminal_profile_cache", "literal_samples",
}
PLAN_KEYS = {"first_hits", "first_misses", "second_hits", "second_misses"}
LITERAL_CACHE_KEYS = {"hits", "misses", "scope"}
TERMINAL_CACHE_KEYS = {"hits", "misses", "clears_at_hard_cap", "hard_cap_keys_per_worker"}
SAMPLE_GUARD_KEYS = {
    "records", "records_per_sink", "all_literal_K24_children_terminal",
    "all_abstract_literal_cycle_keys_equal", "ledger",
}
RESOURCE_KEYS = {"hard_cap_keys_per_worker", "peak_keys_per_worker"}
SAMPLE_HEADER = [
    "lineage_id", "sample_bin", "head_index", "r8_index", "row14", "source_mass",
    "p1_uses", "first_children", "pivotable_first", "p2_uses", "second_children",
    "pivotable_second", "p3_uses", "K23_children", "charge_scaled_U", "witness_p1",
    "witness_t1", "witness_p2", "witness_t2", "witness_p3", "m1", "m2", "m3",
    "terminal_degree", "witness_terminal_q", "witness_row1", "witness_row2",
    "nonzero_terminal_q",
]


def fail(message):
    raise RuntimeError(message)


def need(condition, message):
    if not condition:
        fail(message)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(8 << 20)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def exact_keys(obj, expected, label):
    need(type(obj) is dict, label + " is not an object")
    got = set(obj)
    need(got == expected, f"{label} key mismatch: missing={sorted(expected-got)} extra={sorted(got-expected)}")


def integer_string(value, label):
    need(type(value) is str, label + " must be a string")
    try:
        parsed = int(value)
    except ValueError:
        fail(label + " is not an integer string")
    need(str(parsed) == value or (value == "-0" and parsed == 0), label + " is not canonical")
    return parsed


def histogram(obj, label):
    need(type(obj) is dict and obj, label + " must be a nonempty object")
    out = {}
    for key, value in obj.items():
        need(type(key) is str and key.isdigit() and int(key) > 0 and str(int(key)) == key, label + " bad key")
        need(type(value) is int and value >= 0, label + " bad value")
        out[int(key)] = value
    return out


def source_record_masses():
    data = PINS["structure"][0].read_bytes()
    need(data[:11] == b"K16DIRECT1\0", "structure magic")
    p = 11
    nt, nr, npiv, nanchors = struct.unpack_from("<4I", data, p)
    p += 16
    need((nt, nr, npiv, nanchors) == (384, 485, 78, 12), "structure header counts")
    p += 12 + nt * (252 + 12)
    masses = []
    for _ in range(nr):
        p += 12
        size = struct.unpack_from("<I", data, p)[0]
        p += 4
        coefficient = struct.unpack_from("<q", data, p)[0]
        p += 8
        masses.append(size * coefficient)
    return masses


_ENV = None


def load_environment():
    global _ENV
    if _ENV is not None:
        return _ENV
    data = PINS["structure"][0].read_bytes()
    need(data[:11] == b"K16DIRECT1\0", "structure magic")
    p = 11
    nt, nr, npiv, nanchors = struct.unpack_from("<4I", data, p)
    p += 16
    need((nt, nr, npiv, nanchors) == (384, 485, 78, 12), "structure header")
    anchor_cells = tuple(data[p:p+12])
    p += 12
    positions = {cell: index for index, cell in enumerate(anchor_cells)}
    permutations = []
    for _ in range(nt):
        p += 252
        permutations.append(tuple(data[p:p+12]))
        p += 12
    records = []
    for _ in range(nr):
        base = tuple(data[p:p+12])
        p += 12
        size = struct.unpack_from("<I", data, p)[0]
        p += 4
        coefficient = struct.unpack_from("<q", data, p)[0]
        p += 8
        records.append((base, size, coefficient))
    pivots = []
    for _ in range(npiv):
        pivots.append(tuple(data[p:p+12]))
        p += 12
    factors = [[None for _ in range(3)] for _ in range(3)]
    for factor in range(3):
        for degree_index in range(3):
            count = struct.unpack_from("<I", data, p)[0]
            p += 4
            values = []
            for _ in range(count):
                values.append(tuple(data[p:p+4]))
                p += 4
            factors[factor][degree_index] = values
    need(p == len(data), "structure trailing bytes")

    aux = PINS["aux"][0].read_bytes()
    q = 8
    scale = struct.unpack_from("<Q", aux, q)[0]
    q += 8
    cover_count, aux_pivots = struct.unpack_from("<2I", aux, q)
    q += 8
    need(scale == 281_801_520 and aux_pivots == npiv, "aux header")
    cover = set()
    for _ in range(cover_count):
        cover.add(tuple(aux[q:q+12]))
        q += 12
    anchors = []
    tails = [[[] for _ in range(3)] for _ in range(npiv)]
    for pivot_index in range(npiv):
        anchors.append(tuple(aux[q:q+4]))
        q += 4
        for _ in range(12):
            tails[pivot_index][0].append(tuple(aux[q:q+4]))
            q += 4
        for _ in range(32):
            tails[pivot_index][1].append(tuple(aux[q:q+4]))
            q += 4
    need(q == len(aux), "aux trailing bytes")

    k4 = PINS["k4"][0].read_bytes()
    need(k4[:7] == b"K18K4A1", "K4 magic")
    q = 7
    for pivot_index in range(npiv):
        for _ in range(60):
            tails[pivot_index][2].append(tuple(k4[q:q+4]))
            q += 4
    need(q == len(k4), "K4 trailing bytes")

    cycle = PINS["cycle"][0].read_bytes()
    q = 8
    cells = []
    for _ in range(252):
        cells.append(tuple(cycle[q:q+4]))
        q += 4
    dual_count = struct.unpack_from("<I", cycle, q)[0]
    q += 4
    dual = {}
    for _ in range(dual_count):
        key = bytes(cycle[q:q+13])
        q += 13
        value = struct.unpack_from("<q", cycle, q)[0]
        q += 8
        dual[key] = value
    need(q == len(cycle), "cycle trailing bytes")
    _ENV = {
        "positions": positions, "permutations": permutations, "records": records,
        "pivots": pivots, "factors": factors, "cover": cover, "anchors": anchors,
        "tails": tails, "cells": cells, "dual": dual, "valid_cache": {},
    }
    return _ENV


def row_signature(row, env):
    signature = [0] * 12
    for cell in row:
        if cell in env["positions"]:
            signature[env["positions"][cell]] += 1
    return tuple(signature)


def available(signature, env):
    return [index for index, pivot in enumerate(env["pivots"])
            if all(signature[i] >= pivot[i] for i in range(12))]


def tail_signature(tail, env):
    return row_signature(tail, env)


def child_signature(signature, pivot_index, tail, env):
    tail_sig = tail_signature(tail, env)
    pivot = env["pivots"][pivot_index]
    return tuple(signature[i] - pivot[i] + tail_sig[i] for i in range(12))


def canonical_signature(signature, env):
    candidates = []
    for permutation in env["permutations"]:
        moved = [0] * 12
        for i in range(12):
            moved[permutation[i]] = signature[i]
        candidates.append(tuple(moved))
    return min(candidates)


def valid_first_pivots(signature, env):
    if signature in env["valid_cache"]:
        return env["valid_cache"][signature]
    result = []
    for pivot_index in available(signature, env):
        good = True
        for tail in env["tails"][pivot_index][0]:
            child = child_signature(signature, pivot_index, tail, env)
            if not available(child, env) and canonical_signature(child, env) not in env["cover"]:
                good = False
                break
        if good:
            result.append(pivot_index)
    need(result, "valid-first pivot set is empty")
    env["valid_cache"][signature] = result
    return result


def replace_anchor(row, anchor, tail):
    remaining = list(row)
    for cell in anchor:
        try:
            remaining.remove(cell)
        except ValueError:
            fail("anchor is not contained in literal row")
    need(len(remaining) == 20, "anchor removal size")
    return tuple(sorted(remaining + list(tail)))


def cycle_key(row, env):
    adjacency = [[] for _ in range(24)]
    for cell_index in row:
        u, v, a, b = env["cells"][cell_index]
        x, y = 3 * u + a, 3 * v + b
        adjacency[x].append(y)
        adjacency[y].append(x)
    need(all(len(neighbors) == 2 for neighbors in adjacency), "terminal row is not 2-regular")
    seen = [False] * 24
    parts = []
    for start in range(24):
        if seen[start]:
            continue
        stack = [start]
        seen[start] = True
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in adjacency[vertex]:
                if not seen[neighbor]:
                    seen[neighbor] = True
                    stack.append(neighbor)
        parts.append(size)
    parts.sort()
    key = bytearray(13)
    key[0] = len(parts)
    key[1:1+len(parts)] = bytes(parts)
    return bytes(key)


def replay_literal_sample(data, env):
    lineage_id = data["lineage_id"]
    d1, d2, d3 = DEGREES[lineage_id]
    record_index = int(data["r8_index"])
    head_index = int(data["head_index"])
    need(head_index // 1728 == record_index, "sample head/record index")
    local = head_index % 1728
    a_index, remainder = divmod(local, 144)
    b_index, c_index = divmod(remainder, 12)
    base, size, coefficient = env["records"][record_index]
    row14 = tuple(sorted(base + env["factors"][0][0][a_index] +
                         env["factors"][1][0][b_index] + env["factors"][2][0][c_index]))
    need(row14 == tuple(bytes.fromhex(data["row14"])), "source-faithful row14")
    mass = size * coefficient
    need(int(data["source_mass"]) == mass, "sample source mass")
    need(int(data["sample_bin"]) == head_index * 257 // (485 * 1728), "sample bin formula")

    p1, t1 = int(data["witness_p1"]), int(data["witness_t1"])
    p2, t2 = int(data["witness_p2"]), int(data["witness_t2"])
    p3 = int(data["witness_p3"])
    signature0 = row_signature(row14, env)
    pivots1 = valid_first_pivots(signature0, env)
    need(p1 in pivots1 and int(data["m1"]) == len(pivots1), "first pivot/divisor")
    need(0 <= t1 < TAILS[d1], "first tail index")
    row1 = replace_anchor(row14, env["anchors"][p1], env["tails"][p1][d1-2][t1])
    need(row1 == tuple(bytes.fromhex(data["witness_row1"])), "literal row1")
    signature1 = child_signature(signature0, p1, env["tails"][p1][d1-2][t1], env)
    need(signature1 == row_signature(row1, env), "row1 signature")
    pivots2 = available(signature1, env)
    need(p2 in pivots2 and int(data["m2"]) == len(pivots2), "second pivot/divisor")
    need(0 <= t2 < TAILS[d2], "second tail index")
    row2 = replace_anchor(row1, env["anchors"][p2], env["tails"][p2][d2-2][t2])
    need(row2 == tuple(bytes.fromhex(data["witness_row2"])), "literal row2")
    signature2 = child_signature(signature1, p2, env["tails"][p2][d2-2][t2], env)
    need(signature2 == row_signature(row2, env), "row2 signature")
    pivots3 = available(signature2, env)
    need(p3 in pivots3 and int(data["m3"]) == len(pivots3), "third pivot/divisor")
    need(int(data["terminal_degree"]) == d3, "terminal degree")
    denominator = len(pivots1) * len(pivots2) * len(pivots3)
    need(U % denominator == 0, "sample exact U division")
    terminal_q = 0
    for tail in env["tails"][p3][d3-2]:
        child_sig = child_signature(signature2, p3, tail, env)
        need(not available(child_sig, env), "sample K24 child is pivotable")
        child_row = replace_anchor(row2, env["anchors"][p3], tail)
        terminal_q += env["dual"].get(cycle_key(child_row, env), 0)
    need(terminal_q == int(data["witness_terminal_q"]), "literal terminal charge replay")
    return terminal_q


def validate_raw(x, result_path, require_full=False):
    exact_keys(x, TOP_KEYS, "top")
    is_full = not x["distributed_record_mode"] and x["R8_record_interval"] == [0, 485] and x["R8_records_consumed"] == 485
    expected_status = "PASS_COMPLETE_D14_222_K24_CHARGE_ONLY" if is_full else "PASS_BOUNDED_D14_222_K24_CHARGE_ONLY_GATE"
    need(x["status"] == expected_status, "status/full-scope mismatch")
    need(x["degree"] == 24 and x["covered_lineage_ids"] == IDS, "degree/IDs")
    need(integer_string(x["scale_U"], "scale_U") == U, "U")
    interval = x["R8_record_interval"]
    need(type(interval) is list and len(interval) == 2 and all(type(v) is int for v in interval), "interval shape")
    start, end = interval
    need(0 <= start < end <= 485, "interval bounds")
    need(type(x["distributed_record_mode"]) is bool, "distributed flag")
    consumed = x["R8_records_consumed"]
    need(type(consumed) is int and 1 <= consumed <= 485 and x["R8_records_declared"] == 485, "record counts")
    if x["distributed_record_mode"]:
        need(interval == [0, 485], "distributed interval")
        indices = [242] if consumed == 1 else [sample * 484 // (consumed - 1) for sample in range(consumed)]
    else:
        need(consumed == end - start, "contiguous count")
        indices = list(range(start, end))
    if require_full:
        need(not x["distributed_record_mode"] and interval == [0, 485] and consumed == 485, "not a full exact interval")
    need(x["source_heads"] == 1728 * consumed, "source head count")
    masses = source_record_masses()
    expected_mass = 1728 * sum(masses[index] for index in indices)
    expected_l1 = 1728 * sum(abs(masses[index]) for index in indices)
    need(integer_string(x["source_mass_sum"], "source_mass_sum") == expected_mass, "source mass sum")
    need(integer_string(x["source_mass_l1"], "source_mass_l1") == expected_l1, "source l1")
    need(type(x["sinks"]) is dict and list(x["sinks"]) == IDS, "sink ordering/equality")
    for lineage_id in IDS:
        s = x["sinks"][lineage_id]
        exact_keys(s, SINK_KEYS, "sink " + lineage_id)
        degrees = DEGREES[lineage_id]
        need(tuple(s[k] for k in ("first_response_degree", "second_response_degree", "terminal_response_degree")) == degrees, "response degrees")
        need(s["first_children"] == TAILS[degrees[0]] * s["selected_p1_uses"], "first tail count")
        need(s["second_children"] == TAILS[degrees[1]] * s["selected_p2_uses"], "second tail count")
        need(s["K24_terminal_occurrences"] == TAILS[degrees[2]] * s["selected_p3_uses"], "terminal tail count")
        need(s["full_occurrences"] == s["irreducible_occurrences"] == s["K24_terminal_occurrences"], "full/irr occurrences")
        need(integer_string(s["full_charge_scaled_U"], "full charge") == integer_string(s["irreducible_charge_scaled_U"], "irr charge"), "full/irr charge")
        h1 = histogram(s["first_denominator_hist"], "first denominator histogram")
        h2 = histogram(s["second_denominator_hist"], "second denominator histogram")
        h3 = histogram(s["third_denominator_hist"], "third denominator histogram")
        hp = histogram(s["product_denominator_hist"], "product denominator histogram")
        need(sum(h1.values()) == x["source_heads"], "first histogram cardinality")
        need(sum(k*v for k, v in h1.items()) == s["selected_p1_uses"], "first histogram weighted sum")
        need(sum(h2.values()) == s["pivotable_first_children"], "second histogram cardinality")
        need(sum(k*v for k, v in h2.items()) == s["selected_p2_uses"], "second histogram weighted sum")
        need(sum(h3.values()) == s["pivotable_second_children"], "third histogram cardinality")
        need(sum(k*v for k, v in h3.items()) == s["selected_p3_uses"], "third histogram weighted sum")
        need(sum(hp.values()) == s["pivotable_second_children"], "product histogram cardinality")
        need(all(U % d == 0 for d in hp), "inexact U/product division")
        exact_keys(s["plan_cache"], PLAN_KEYS, "plan cache")
        exact_keys(s["literal_preterminal_cache"], LITERAL_CACHE_KEYS, "literal cache")
        exact_keys(s["terminal_profile_cache"], TERMINAL_CACHE_KEYS, "terminal cache")
        need(s["literal_preterminal_cache"]["hits"] + s["literal_preterminal_cache"]["misses"] == s["pivotable_second_children"], "literal cache accounting")
        need(type(s["terminal_profile_cache"]["clears_at_hard_cap"]) is int and s["terminal_profile_cache"]["clears_at_hard_cap"] >= 0, "terminal cache clear count")
        need(s["terminal_profile_cache"]["hard_cap_keys_per_worker"] == 3_000_000, "terminal cache cap")
        need(type(s["literal_samples"]) is int and 0 <= s["literal_samples"] <= 257, "literal sample count")
    need(x["all_realized_cached_K24_responses_terminal"] is True, "universal terminality")
    guard = x["literal_sample_guard"]
    exact_keys(guard, SAMPLE_GUARD_KEYS, "sample guard")
    need(guard["all_literal_K24_children_terminal"] is True, "literal terminal guard")
    need(guard["all_abstract_literal_cycle_keys_equal"] is True, "abstract/literal key guard")
    need(guard["records_per_sink"] == [x["sinks"][i]["literal_samples"] for i in IDS], "sample per-sink counts")
    need(guard["records"] == sum(guard["records_per_sink"]), "sample total")
    expected_ledger = Path(str(result_path) + ".samples.tsv").resolve()
    reported_ledger = Path(guard["ledger"])
    if not reported_ledger.is_absolute():
        reported_ledger = ROOT / reported_ledger
    need(reported_ledger.resolve() == expected_ledger, "sample path is not result-adjacent")
    need(expected_ledger.is_file(), "sample ledger missing")
    lines = expected_ledger.read_text().splitlines()
    need(lines and lines[0].split("\t") == SAMPLE_HEADER, "sample header")
    rows = [line.split("\t") for line in lines[1:]]
    need(len(rows) == guard["records"] and all(len(row) == len(SAMPLE_HEADER) for row in rows), "sample row count/width")
    nonzero = 0
    per_sink = {i: 0 for i in IDS}
    environment = load_environment()
    for row in rows:
        data = dict(zip(SAMPLE_HEADER, row))
        need(data["lineage_id"] in per_sink, "sample lineage")
        per_sink[data["lineage_id"]] += 1
        need(0 <= int(data["sample_bin"]) <= 256, "sample bin")
        record_index = int(data["r8_index"])
        if not x["distributed_record_mode"]:
            need(start <= record_index < end, "sample outside interval")
        need(len(data["row14"]) == len(data["witness_row1"]) == len(data["witness_row2"]) == 48, "literal row width")
        need(int(data["terminal_degree"]) == 4, "sample terminal degree")
        terminal_q = replay_literal_sample(data, environment)
        flag = int(data["nonzero_terminal_q"])
        need(flag in (0, 1) and flag == int(terminal_q != 0), "sample nonzero flag")
        nonzero += flag
    need([per_sink[i] for i in IDS] == guard["records_per_sink"], "ledger per-sink counts")
    resource = x["terminal_cache_resource_guard"]
    exact_keys(resource, RESOURCE_KEYS, "resource guard")
    need(resource["hard_cap_keys_per_worker"] == 3_000_000, "resource cap")
    need(0 <= resource["peak_keys_per_worker"] <= 3_000_000, "resource peak")
    need(type(x["workers"]) is int and 1 <= x["workers"] <= 8, "workers")
    need(type(x["elapsed_seconds"]) in (int, float) and 0 <= x["elapsed_seconds"] < 600, "elapsed")
    need("no intermediate or terminal row/column output" in x["scope"], "scope")
    return {"records": consumed, "sample_rows": len(rows), "nonzero_sample_rows": nonzero}


def compare_record0(fast, physical):
    need(fast["R8_record_interval"] == [0, 1] and not fast["distributed_record_mode"], "fast control interval")
    need(physical["source_interval"] == [0, 1] and not physical["distributed"], "physical control interval")
    need(fast["source_heads"] == physical["groups"][0]["source_heads"], "source heads differ")
    need(int(fast["source_mass_sum"]) == -int(physical["groups"][0]["source_coefficient_sum"]), "source sign normalization differs")
    need(int(fast["source_mass_l1"]) == int(physical["groups"][0]["source_l1"]), "source l1 differs")
    by_id = {group["ids"][0]: group for group in physical["groups"]}
    fields = {
        "selected_p1_uses": ("stage_pivot_uses", 0),
        "first_children": ("stage_tail_candidates", 0),
        "pivotable_first_children": ("stage_pivotable_children", 0),
        "selected_p2_uses": ("stage_pivot_uses", 1),
        "second_children": ("stage_tail_candidates", 1),
        "pivotable_second_children": ("stage_pivotable_children", 1),
        "selected_p3_uses": ("stage_pivot_uses", 2),
        "K24_terminal_occurrences": ("terminal_K24_occurrences", None),
        "full_occurrences": ("full_occurrences", None),
        "irreducible_occurrences": ("irreducible_occurrences", None),
        "full_charge_scaled_U": ("full_charge_scaled_U", None),
        "irreducible_charge_scaled_U": ("irreducible_charge_scaled_U", None),
        "product_denominator_hist": ("denominator_product_hist", None),
    }
    for lineage_id in IDS:
        a, b = fast["sinks"][lineage_id], by_id[lineage_id]
        for fast_key, (physical_key, index) in fields.items():
            value = b[physical_key] if index is None else b[physical_key][index]
            need(a[fast_key] == value, f"record0 mismatch {lineage_id} {fast_key}")


def check_schema_keysets():
    schema = json.loads(PINS["raw_result_schema"][0].read_text())
    need(schema.get("additionalProperties") is False, "schema top is not closed")
    need(set(schema.get("required", [])) == TOP_KEYS, "schema top required mismatch")
    need(set(schema.get("properties", {})) == TOP_KEYS, "schema top properties mismatch")
    sink = schema["$defs"]["sink"]
    need(sink.get("additionalProperties") is False, "schema sink is not closed")
    need(set(sink.get("required", [])) == SINK_KEYS, "schema sink required mismatch")
    need(set(sink.get("properties", {})) == SINK_KEYS, "schema sink properties mismatch")
    sample = schema["$defs"]["sampleGuard"]
    need(sample.get("additionalProperties") is False, "schema sample guard is not closed")
    need(set(sample.get("required", [])) == SAMPLE_GUARD_KEYS, "schema sample guard mismatch")
    need(set(sample.get("properties", {})) == SAMPLE_GUARD_KEYS, "schema sample properties mismatch")


def main():
    pin_hashes = {}
    for name, (path, expected) in PINS.items():
        got = sha(path)
        need(got == expected, f"pin mismatch {name}: {got}")
        pin_hashes[name] = got
    check_schema_keysets()
    fast_path = HERE / "fast_exact_record0.json"
    physical_path = SEALED / "tiny_k14.json"
    fast = json.loads(fast_path.read_text())
    physical = json.loads(physical_path.read_text())
    raw_summary = validate_raw(fast, fast_path)
    compare_record0(fast, physical)
    prefix8_path = FAST / "results_k14_source_prefix8.json"
    prefix8 = json.loads(prefix8_path.read_text())
    prefix8_summary = validate_raw(prefix8, prefix8_path)
    full_path = FAST / "results_k14_source_complete.json"
    full = json.loads(full_path.read_text())
    full_summary = validate_raw(full, full_path, require_full=True)
    need(full["literal_sample_guard"]["records_per_sink"] == [257, 257], "full witness coverage")
    blockers = [
        "raw result contains no input source hashes",
        "raw result contains no engine source or binary hash",
        "raw result contains no result or sample-ledger hash",
        "legacy validation predicates are assert-based; under python -O the core checks disappear and the CLI fails only inside its hostile selftest",
        "legacy validator does not enforce exact keysets or parse/replay the sample TSV",
        "raw result has no independently measured RSS/resource acceptance evidence",
        "sample selection does not require nonzero charge continuations (record0 has zero nonzero samples)",
    ]
    out = {
        "status": "PASS_INDEPENDENT_FAST_K14_SEMANTICS_RAW_LEDGER_NOT_FULL_ACCEPTANCE",
        "degree": 24,
        "lineage_ids": IDS,
        "source_binary_input_schema_pins": pin_hashes,
        "fast_exact_record0": {
            "result_sha256": sha(fast_path),
            "samples_sha256": sha(Path(str(fast_path) + ".samples.tsv")),
            "raw_validation": raw_summary,
            "semantic_scalar_count_histogram_equality_to_sealed_physical": True,
        },
        "fast_distributed8": {
            "result_sha256": sha(prefix8_path),
            "samples_sha256": sha(Path(str(prefix8_path) + ".samples.tsv")),
            "raw_validation": prefix8_summary,
            "scope": "distributed diagnostic only; not an exact production interval",
        },
        "fast_full_result": {
            "result_sha256": sha(full_path),
            "samples_sha256": sha(Path(str(full_path) + ".samples.tsv")),
            "raw_validation_and_514_literal_replay": full_summary,
            "interval": full["R8_record_interval"],
            "elapsed_seconds": full["elapsed_seconds"],
            "charges_scaled_U": {lineage_id: full["sinks"][lineage_id]["full_charge_scaled_U"] for lineage_id in IDS},
            "structural_scalar_acceptance": "PASS",
            "resource_acceptance": "WITHHELD_NO_INDEPENDENT_RSS_EVIDENCE",
        },
        "full_raw_result_available": True,
        "raw_output_ledger_sufficient_for_full_acceptance": False,
        "blockers": blockers,
        "required_acceptance_supersession": "strict external envelope pinning all four inputs, source, binary, result, sample ledger, exact [0,485) interval, non-distributed mode, resource evidence, and independently replayed distributed literal witnesses",
        "full_run_launched_by_this_audit": False,
        "external_full_result_observed": True,
    }
    output = json.dumps(out, indent=2, sort_keys=True) + "\n"
    (HERE / "results_fast_k14_independent_audit.json").write_text(output)
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
