#!/usr/bin/env python3
"""Independent bounded referee for the full hidden K14->K16 recovery."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import ast
import importlib.util
import json
import mmap
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKET = ROOT / "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23"
FINAL = PACKET / "results_full_hidden_k16_parent_recovery.json"
MERGED = PACKET / "hidden_k16_second_pivot_profiles_full.bin"
MERGE_REFEREE = HERE / "results_profile_merge_referee.json"
DESIGN = ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/filtered_k24_reducer.py"
COVER = ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21/results_k16_anchor_cover.json"
FROZEN = ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json"
OUT = HERE / "results_hidden_parent_full_referee.json"
U = 400_591_699_200


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path):
    spec = importlib.util.spec_from_file_location("hidden_parent_full_design", path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


D = load(DESIGN)


def file_sha(path):
    digest = sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            digest.update(block)
    return digest.hexdigest()


def valid_pivots(signature, cover):
    valid = []
    for pivot in D.CTX.pivots(signature):
        base = tuple(a - b for a, b in
                     zip(signature, D.CTX.vectors[pivot], strict=True))
        survivors = set()
        for tail in D.CTX.tails[pivot][2]:
            counts = Counter(tail)
            child = tuple(a + counts[cell] for a, cell in
                          zip(base, D.CTX.anchor_cells, strict=True))
            if not D.CTX.pivots(child):
                survivors.add(D.CTX.canonical_signature(child))
        if survivors <= cover:
            valid.append(pivot)
    require(valid, signature)
    return tuple(valid)


def subtract(row, anchor):
    value = Counter(row)
    value.subtract(anchor)
    require(all(x >= 0 for x in value.values()), (row.hex(), anchor.hex()))
    return bytes(sorted(cell for cell, count in value.items()
                        for _ in range(count)))


def parse_parent(item):
    require(len(item) == 64, len(item))
    return {
        "row": item[:24],
        "weight": int.from_bytes(item[24:40], "little", signed=True),
        "signature": tuple(item[40:52]),
        "ri": int.from_bytes(item[52:54], "little"),
        "fields": tuple(item[54:64]),
    }


def main():
    final = json.loads(FINAL.read_text())
    merge_referee = json.loads(MERGE_REFEREE.read_text())
    frozen = json.loads(FROZEN.read_text())
    require(final["status"] == "PASS_FULL_HIDDEN_K16_PARENT_RECOVERY",
            final["status"])
    require(merge_referee["status"] == "PASS_INDEPENDENT_EXACT_PROFILE_MERGE"
            and merge_referee["exact_zero_keys"] == 355_738
            and merge_referee["output_nonzero_keys"] == 6_229_700,
            merge_referee)
    require(frozen["collection"]["reducible_K16_tail_occurrences"]
            == 75_691_040, "frozen count changed")
    cover_raw = json.loads(COVER.read_text())
    cover = frozenset(ast.literal_eval(row) for row in cover_raw
                      ["single_pivot_cover"]["minimum_cover_orbit_representatives"])
    source_records = D.r8_h_records()
    factor_words = tuple(D.F.word_from_pair_colours(row)
                         for row in D.F.PAIR_COLOURS)
    factor_pivots = tuple(D.CTX.anchor_to_pivot[
        D.F.BASE.term_ids(word, D.F.M0)] for word in factor_words)
    factor_tails = tuple(D.CTX.tails[pivot][2] for pivot in factor_pivots)

    manifests = [json.loads(path.read_text())
                 for path in sorted(PACKET.glob("run_*.json"))]
    expected_intervals = [(start, min(start + 16, 485))
                          for start in range(0, 485, 16)]
    require([(row["start"], row["end"]) for row in manifests]
            == expected_intervals, "slice partition")
    require(len(manifests) == 31, len(manifests))
    ledger = {(row["start"], row["end"]): row for row in final["run_ledger"]}

    totals = Counter()
    parent_sum = 0
    profile_sum = 0
    sampled = 0
    first_parent = None
    profile_maps = []
    for manifest in manifests:
        start, end = manifest["start"], manifest["end"]
        parent_path = PACKET / manifest["parent_file"]
        profile_path = PACKET / manifest["profile_file"]
        parent_count = manifest["hidden_parent_occurrences"]
        profile_count = manifest["unique_nonzero_profiles"]
        with parent_path.open("rb") as stream:
            header = stream.read(40)
            require(header[:8] == b"H16RUN2\0", header[:8])
            require(int.from_bytes(header[8:24], "little", signed=True) == U,
                    "parent scale")
            require(struct.unpack_from("<HHH", header, 24) == (start, end, 64),
                    (start, header))
            require(int.from_bytes(header[32:40], "little") == parent_count,
                    (start, parent_count))
            require(parent_path.stat().st_size == 40 + 64 * parent_count,
                    (parent_path, parent_path.stat().st_size, parent_count))
            positions = sorted({0, parent_count // 2, parent_count - 1})
            for position in positions:
                stream.seek(40 + 64 * position)
                record = parse_parent(stream.read(64))
                row = record["row"]
                weight = record["weight"]
                signature = record["signature"]
                ri = record["ri"]
                ia, ib, ic, p1, t1, m1, m2, z0, z1, z2 = record["fields"]
                require(start <= ri < end and (z0, z1, z2) == (0, 0, 0),
                        (start, position, ri, record["fields"]))
                r8, orbit_size, coefficient = source_records[ri]
                head = bytes(sorted(r8 + factor_tails[0][ia] +
                                    factor_tails[1][ib] + factor_tails[2][ic]))
                head_signature = tuple(Counter(head)[cell]
                                       for cell in D.CTX.anchor_cells)
                first = valid_pivots(head_signature, cover)
                require(p1 in first and len(first) == m1,
                        (start, position, p1, first, m1))
                expected_row = bytes(sorted(subtract(head, D.CTX.anchors[p1]) +
                                            D.CTX.tails[p1][2][t1]))
                require(row == expected_row, (start, position, row.hex()))
                expected_signature = tuple(Counter(row)[cell]
                                           for cell in D.CTX.anchor_cells)
                second = D.CTX.pivots(expected_signature)
                require(signature == expected_signature and len(second) == m2 and m2,
                        (start, position, signature, second, m2))
                mass = Fraction(orbit_size) * coefficient
                require(mass.denominator == 1 and mass.numerator * U % m1 == 0,
                        (start, position, mass, m1))
                require(weight == mass.numerator * U // m1,
                        (start, position, weight, mass, m1))
                for pivot in second:
                    quotient = subtract(row, D.CTX.anchors[pivot])
                    require(len(quotient) == 20, (start, position, pivot))
                    require(tuple(len(D.CTX.tails[pivot][degree])
                                  for degree in (2, 3, 4)) == (12, 32, 60),
                            (start, position, pivot))
                if first_parent is None:
                    first_parent = record
                sampled += 1

        with profile_path.open("rb") as stream:
            header = stream.read(40)
            require(header[:8] == b"H16PF2\0\0", header[:8])
            require(int.from_bytes(header[8:24], "little", signed=True) == U,
                    "profile scale")
            require(struct.unpack_from("<HHH", header, 24) == (start, end, 59),
                    (start, header))
            require(int.from_bytes(header[32:40], "little") == profile_count,
                    (start, profile_count))
            require(profile_path.stat().st_size == 40 + 59 * profile_count,
                    (profile_path, profile_path.stat().st_size, profile_count))

        hashes = ledger[(start, end)]
        require(file_sha(parent_path) == hashes["parent_sha256"], parent_path)
        require(file_sha(profile_path) == hashes["profile_sha256"], profile_path)
        totals["heads"] += manifest["heads"]
        totals["parents"] += parent_count
        totals["outgoing"] += manifest["outgoing_second_pivot_uses"]
        totals["profiles"] += profile_count
        totals["parent_bytes"] += parent_path.stat().st_size
        totals["profile_bytes"] += profile_path.stat().st_size
        parent_sum += int(manifest["parent_weight_sum_scaled"])
        require(manifest["profile_raw_weight_sum_scaled"]
                == manifest["profile_weight_sum_scaled"], manifest)
        profile_sum += int(manifest["profile_weight_sum_scaled"])
        profile_maps.append((profile_path, profile_count))

    require(totals["heads"] == 838_080, totals)
    require(totals["parents"] == final["hidden_parent_occurrences"]
            == 75_691_040, totals)
    require(totals["outgoing"] == final["outgoing_second_pivot_uses"]
            == 511_477_120, totals)
    require(parent_sum == int(final["parent_weight_sum_scaled"])
            == -146_230_609_431_055_564_800, parent_sum)
    require(profile_sum == int(final["input_profile_weight_sum_scaled"])
            == -parent_sum, profile_sum)

    # Scan the merged output independently for sort/nonzero/tag/sum and retain
    # evenly spread records for a source-run binary-search aggregation replay.
    merged_hash = file_sha(MERGED)
    require(merged_hash == final["sha256"]["merged_profiles"], merged_hash)
    merged_count = final["merged_profile_records"]
    selected_positions = sorted({0, merged_count - 1} |
                                {i * (merged_count - 1) // 256
                                 for i in range(257)})
    selected = {}
    merged_sum = 0
    prior = None
    with MERGED.open("rb") as stream:
        header = stream.read(32)
        require(header[:8] == b"H16MER2\0", header[:8])
        require(int.from_bytes(header[8:24], "little", signed=True) == U,
                "merged scale")
        require(int.from_bytes(header[24:32], "little") == merged_count,
                "merged count")
        require(MERGED.stat().st_size == 32 + 59 * merged_count,
                MERGED.stat().st_size)
        selected_set = set(selected_positions)
        for index in range(merged_count):
            record = stream.read(59)
            key, value = record[:43], int.from_bytes(record[43:], "little", signed=True)
            require(key[42] == 0 and value and (prior is None or prior < key),
                    (index, prior, key, value))
            if index in selected_set:
                selected[key] = value
            prior = key
            merged_sum += value
        require(not stream.read(1), "merged trailing byte")
    require(merged_sum == profile_sum, (merged_sum, profile_sum))

    # For each sampled merged key, independently sum its value across all 31
    # sorted run files by binary search.
    mapped = []
    try:
        for path, count in profile_maps:
            stream = path.open("rb")
            mm = mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ)
            mapped.append((stream, mm, count))
        for key, expected in selected.items():
            actual = 0
            for _stream, mm, count in mapped:
                lo, hi = 0, count
                while lo < hi:
                    mid = (lo + hi) // 2
                    found = mm[40 + 59 * mid:40 + 59 * mid + 43]
                    if found < key:
                        lo = mid + 1
                    else:
                        hi = mid
                if lo < count and mm[40 + 59 * lo:40 + 59 * lo + 43] == key:
                    actual += int.from_bytes(mm[40 + 59 * lo + 43:
                                               40 + 59 * lo + 59],
                                             "little", signed=True)
            require(actual == expected, (key.hex(), actual, expected))
    finally:
        for stream, mm, _count in mapped:
            mm.close()
            stream.close()

    # Byte-for-byte provider guards from the first recovered parent.
    require(first_parent is not None, "no first parent")
    provider_hashes = {}
    row = first_parent["row"]
    signature = first_parent["signature"]
    weight = first_parent["weight"]
    second = D.CTX.pivots(signature)
    m2 = first_parent["fields"][6]
    require(len(second) == m2 and weight % m2 == 0, first_parent)
    child_weight = -weight // m2
    for degree in (2, 3, 4):
        expected = bytearray()
        for pivot in second:
            for tail_index, tail in enumerate(D.CTX.tails[pivot][degree]):
                child = bytes(sorted(subtract(row, D.CTX.anchors[pivot]) + tail))
                expected += child
                expected += child_weight.to_bytes(16, "little", signed=True)
                expected += (0).to_bytes(8, "little")
                expected += bytes((pivot, tail_index, m2, degree))
        path = PACKET / f"provider_guard_k{degree}.bin"
        raw = path.read_bytes()
        count = len(expected) // 52
        require(raw[:8] == b"H16CHD2\0" and
                int.from_bytes(raw[8:24], "little", signed=True) == U and
                raw[24] == degree, (degree, raw[:25]))
        require(int.from_bytes(raw[25:27], "little") == 0 and
                int.from_bytes(raw[32:40], "little") == 0 and
                int.from_bytes(raw[40:48], "little") == 1 and
                int.from_bytes(raw[48:56], "little") == count and
                int.from_bytes(raw[56:58], "little") == 52,
                (degree, count, raw[:64].hex()))
        require(raw[64:] == expected, degree)
        digest = file_sha(path)
        require(digest == final["child_provider"]["guard_runs"][str(degree)]
                ["sha256"], (degree, digest))
        provider_hashes[str(degree)] = digest

    result = {
        "status": "PASS_INDEPENDENT_FULL_HIDDEN_PARENT_REFEREE",
        "partition": {"atomic_runs": 31, "H_slices": 485,
                      "intervals_exact_and_disjoint": True},
        "counts": {"heads": totals["heads"],
                   "hidden_parent_occurrences": totals["parents"],
                   "outgoing_second_pivot_uses": totals["outgoing"],
                   "input_profile_records": totals["profiles"],
                   "merged_nonzero_profiles": merged_count,
                   "exact_zero_profiles_from_merge": final["exact_zero_profile_keys"]},
        "masses": {"parent_weight_sum_scaled": str(parent_sum),
                   "input_and_merged_profile_weight_sum_scaled": str(profile_sum)},
        "source_replay": {"sampled_parent_records": sampled,
                          "sampling": "first/middle/last of every atomic run",
                          "K2_K3_K4_tail_counts": [12, 32, 60]},
        "merge_replay": {"all_output_records_sorted_nonzero_tag0": True,
                         "independent_exact_hash_aggregate": True,
                         "exact_zero_keys_recomputed": merge_referee["exact_zero_keys"],
                         "sampled_cross_run_key_sums": len(selected),
                         "merged_sha256": merged_hash},
        "provider_byte_replay": provider_hashes,
        "scope": "Full parent/profile recovery referee; no bulk child emission or charge computation.",
        "pinned_final_result_sha256": file_sha(FINAL),
        "pinned_merge_referee_sha256": file_sha(MERGE_REFEREE),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
