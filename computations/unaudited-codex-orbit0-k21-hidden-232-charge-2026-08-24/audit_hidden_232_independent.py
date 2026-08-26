#!/usr/bin/env python3
"""Independent package/count/sample referee for D14:222|R:2-3-2."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "run_k21_hidden_232_charge.rs"
BINARY = HERE / "run_k21_hidden_232_charge"
RESULT = HERE / "results_hidden_232_k21_charge.json"
SAMPLES = HERE / "results_hidden_232_k21_charge.json.samples.tsv"
PAIR = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin"
STRUCTURE = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin"
AUX = STRUCTURE.with_name("filtered_k17_aux.bin")
CYCLE = STRUCTURE.with_name("filtered_k17_cycle_aux.bin")
PAIR_RESULT = PAIR.with_name("results_full_hidden_k16_k2_orbits.json")
PAIR_REFEREE = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-final-referee-2026-08-23/results_final_merge_referee_final.json"
OUT = HERE / "results_hidden_232_independent_referee.json"

U = 400_591_699_200
N = 101_545_723
HEADER = 80
RECORD = 53
EXPECTED_HASHES = {
    SOURCE: "4228a7ca6380329bae6c1351e32605bfad2cf04b0c7c5261c877e913cff0fe5c",
    BINARY: "38d3e3e728af10e4632877e4f0a657ae076a2da9af1355e8738ba10fec4e65e4",
    RESULT: "a58fa70195e5bb42ddad9b971a05145d15043f35af044c5339b1779ea56f3bae",
    SAMPLES: "113acc594bb35e2ab19a511f75b0dbb73e728806d08aa1566bca994d4074dd3d",
    PAIR: "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8",
    STRUCTURE: "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    AUX: "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    CYCLE: "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    PAIR_RESULT: "54946037ec9d96a5c3509e4f057350601aaaa34764aad84753cea7b03d2944a4",
    PAIR_REFEREE: "14e636d297847c850f1417601a396e73fc9514c2eb8810ffe42367a38776a23a",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    h = sha256()
    with path.open("rb") as stream:
        while block := stream.read(16 << 20):
            h.update(block)
    return h.hexdigest()


def parse_pair_header():
    with PAIR.open("rb") as stream:
        h = stream.read(HEADER)
    require(len(h) == HEADER and h[:8] == b"H16ORM1\0", h[:8])
    values = {
        "scale_U": int.from_bytes(h[8:24], "little", signed=True),
        "start": struct.unpack_from("<H", h, 24)[0],
        "end": struct.unpack_from("<H", h, 26)[0],
        "record_bytes": struct.unpack_from("<H", h, 28)[0],
        "reserved": struct.unpack_from("<H", h, 30)[0],
        "orbit_chunks": struct.unpack_from("<Q", h, 32)[0],
        "zero_orbit_keys": struct.unpack_from("<Q", h, 40)[0],
        "records": struct.unpack_from("<Q", h, 48)[0],
        "before": struct.unpack_from("<Q", h, 56)[0],
        "weight_sum_scaled": int.from_bytes(h[64:80], "little", signed=True),
    }
    require(values == {
        "scale_U": U, "start": 0, "end": 0, "record_bytes": RECORD,
        "reserved": 0, "orbit_chunks": 246, "zero_orbit_keys": 305,
        "records": N, "before": 0,
        "weight_sum_scaled": 146_230_609_431_055_564_800,
    }, values)
    require(PAIR.stat().st_size == HEADER + RECORD * N, PAIR.stat().st_size)
    return values


def decode_pair(rec):
    require(len(rec) == RECORD, len(rec))
    return {
        "row": rec[:24],
        "p2": rec[24],
        "weight": int.from_bytes(rec[25:41], "little", signed=True),
        "uses": int.from_bytes(rec[41:49], "little"),
        "orbit": int.from_bytes(rec[49:51], "little"),
        "stabilizer": int.from_bytes(rec[51:53], "little"),
    }


def read_pair(index, stream):
    stream.seek(HEADER + RECORD * index)
    return decode_pair(stream.read(RECORD))


def parse_structure():
    b = STRUCTURE.read_bytes()
    require(b[:11] == b"K16DIRECT1\0", b[:11])
    q = 11
    nt, nr, np, na = struct.unpack_from("<IIII", b, q)
    q += 16
    require((nt, nr, np, na) == (384, 485, 78, 12), (nt, nr, np, na))
    anchor_cells = b[q:q + 12]
    q += 12 + nt * (252 + 12) + nr * 24
    pivots = [b[q + 12 * j:q + 12 * j + 12] for j in range(np)]
    q += 12 * np
    for _factor in range(3):
        for expected in (12, 32, 60):
            n = struct.unpack_from("<I", b, q)[0]
            q += 4 + 4 * n
            require(n == expected, n)
    require(q == len(b), (q, len(b)))
    return anchor_cells, pivots


def parse_aux():
    b = AUX.read_bytes()
    require(b[:8] == b"K17AUX1\0", b[:8])
    q = 8
    scale = struct.unpack_from("<Q", b, q)[0]
    q += 8
    nc, npa = struct.unpack_from("<II", b, q)
    q += 8
    require((scale, nc, npa) == (281_801_520, 25, 78), (scale, nc, npa))
    q += 12 * nc
    anchors, k2, k3 = [], [], []
    for _ in range(npa):
        anchors.append(b[q:q + 4]); q += 4
        k2.append([b[q + 4 * j:q + 4 * j + 4] for j in range(12)]); q += 48
        k3.append([b[q + 4 * j:q + 4 * j + 4] for j in range(32)]); q += 128
    require(q == len(b), (q, len(b)))
    return anchors, k2, k3


def parse_cycle():
    b = CYCLE.read_bytes()
    require(b[:8] == b"K17CYC1\0", b[:8])
    q = 8
    cells = [tuple(b[q + 4 * j:q + 4 * j + 4]) for j in range(252)]
    q += 4 * 252
    nd = struct.unpack_from("<I", b, q)[0]; q += 4
    dual = {}
    for _ in range(nd):
        key = b[q:q + 13]
        dual[key] = struct.unpack_from("<q", b, q + 13)[0]
        q += 21
    require(q == len(b), (q, len(b)))
    return cells, dual


def signature(row, positions):
    out = [0] * 12
    for cell in row:
        if cell in positions:
            out[positions[cell]] += 1
    return out


def tail_signature(tail, positions):
    out = [0] * 12
    for cell in tail:
        if cell in positions:
            out[positions[cell]] += 1
    return out


def available(sig, pivots):
    return [j for j, p in enumerate(pivots)
            if all(sig[i] >= p[i] for i in range(12))]


def child_signature(sig, pivot, tail, positions):
    add = tail_signature(tail, positions)
    out = [sig[i] - pivot[i] + add[i] for i in range(12)]
    require(all(x >= 0 for x in out), out)
    return out


def replace(row, anchor, tail):
    counts = Counter(row)
    counts.subtract(anchor)
    require(all(x >= 0 for x in counts.values()), (row.hex(), anchor.hex()))
    out = []
    for cell, n in counts.items():
        out.extend([cell] * n)
    out.extend(tail)
    out.sort()
    require(len(out) == 24, len(out))
    return bytes(out)


def charge(row, cells, dual):
    adj = [[] for _ in range(24)]
    for cell in row:
        u, v, a, b = cells[cell]
        x, y = 3 * u + a, 3 * v + b
        adj[x].append(y); adj[y].append(x)
    require(all(len(x) == 2 for x in adj), [len(x) for x in adj])
    seen, parts = set(), []
    for start in range(24):
        if start in seen:
            continue
        stack, size = [start], 0
        seen.add(start)
        while stack:
            vertex = stack.pop(); size += 1
            for nxt in adj[vertex]:
                if nxt not in seen:
                    seen.add(nxt); stack.append(nxt)
        parts.append(size)
    parts.sort()
    key = bytes([len(parts)] + parts + [0] * (12 - len(parts)))
    return dual.get(key, 0)


def replay_pair(pair, anchor_cells, pivots, anchors, k2, k3, cells, dual):
    positions = {cell: j for j, cell in enumerate(anchor_cells)}
    require(pair["row"] == bytes(sorted(pair["row"])), pair["row"].hex())
    require(pair["weight"] != 0 and pair["uses"] > 0, pair)
    require(pair["orbit"] * pair["stabilizer"] == 384, pair)
    s16 = signature(pair["row"], positions)
    ps2 = available(s16, pivots)
    require(pair["p2"] in ps2, (pair["p2"], ps2))
    m2 = len(ps2)
    pivotable = p3_uses = k21_children = 0
    k21_weight = total_charge = 0
    for tail3 in k3[pair["p2"]]:
        row19 = replace(pair["row"], anchors[pair["p2"]], tail3)
        s19 = child_signature(s16, pivots[pair["p2"]], tail3, positions)
        require(s19 == signature(row19, positions), "K19 literal/signature mismatch")
        ps3 = available(s19, pivots)
        if not ps3:
            continue
        pivotable += 1
        m3 = len(ps3)
        require(U % (m2 * m3) == 0, (m2, m3))
        require(pair["weight"] % m3 == 0, (pair["weight"], m3))
        w3 = -pair["weight"] // m3
        for p3 in ps3:
            p3_uses += 1
            for tail2 in k2[p3]:
                row21 = replace(row19, anchors[p3], tail2)
                s21 = child_signature(s19, pivots[p3], tail2, positions)
                require(s21 == signature(row21, positions), "K21 literal/signature mismatch")
                require(not available(s21, pivots), (pair["p2"], p3, s21))
                k21_children += 1
                k21_weight += w3
                total_charge += w3 * charge(row21, cells, dual)
    require(k21_children == 12 * p3_uses, (k21_children, p3_uses))
    return {
        "m2": m2,
        "K19_children": 32,
        "pivotable_K19_children": pivotable,
        "selected_p3_uses": p3_uses,
        "K21_children": k21_children,
        "K21_weight_sum_scaled": k21_weight,
        "charge_scaled": total_charge,
        "nonzero_continuation": int(p3_uses > 0),
    }


def audit_samples(anchor_cells, pivots, anchors, k2, k3, cells, dual):
    lines = SAMPLES.read_text().splitlines()
    require(len(lines) == 258, len(lines))
    expected_header = "input_index\tK16_row\tp2\tweight_after_p2\tpair_uses\torbit\tstabilizer\tm2\tK19_children\tpivotable_K19_children\tselected_p3_uses\tK21_children\tK21_weight_sum_scaled\tcharge_scaled\tnonzero_continuation"
    require(lines[0] == expected_header, lines[0])
    expected_indices = [j * (N - 1) // 256 for j in range(257)]
    total_terminal = nonzero = 0
    with PAIR.open("rb") as stream:
        for expected_index, line in zip(expected_indices, lines[1:], strict=True):
            f = line.split("\t")
            require(len(f) == 15 and int(f[0]) == expected_index, (expected_index, f))
            pair = read_pair(expected_index, stream)
            require(pair == {
                "row": bytes.fromhex(f[1]), "p2": int(f[2]), "weight": int(f[3]),
                "uses": int(f[4]), "orbit": int(f[5]), "stabilizer": int(f[6]),
            }, (expected_index, pair, f))
            replay = replay_pair(pair, anchor_cells, pivots, anchors, k2, k3, cells, dual)
            observed = {
                "m2": int(f[7]), "K19_children": int(f[8]),
                "pivotable_K19_children": int(f[9]), "selected_p3_uses": int(f[10]),
                "K21_children": int(f[11]), "K21_weight_sum_scaled": int(f[12]),
                "charge_scaled": int(f[13]), "nonzero_continuation": int(f[14]),
            }
            require(replay == observed, (expected_index, replay, observed))
            total_terminal += replay["K21_children"]
            nonzero += replay["nonzero_continuation"]
    require(nonzero == 212, nonzero)
    return {
        "records": 257,
        "spacing": "floor(j*(101545723-1)/256), j=0..256",
        "source_records_seek_replayed": 257,
        "nonzero_continuations": nonzero,
        "literal_terminal_K21_children_replayed": total_terminal,
        "all_exact_U_divisions_hold": True,
        "all_literal_signature_updates_match": True,
        "all_literal_K21_children_nonpivotable": True,
        "all_literal_cycle_charges_match_producer_samples": True,
    }


def main():
    hashes = {}
    for path, expected in EXPECTED_HASHES.items():
        actual = digest(path)
        require(actual == expected, (path, actual, expected))
        hashes[str(path.relative_to(ROOT))] = actual
    header = parse_pair_header()
    anchor_cells, pivots = parse_structure()
    anchors, k2, k3 = parse_aux()
    cells, dual = parse_cycle()
    sample_audit = audit_samples(anchor_cells, pivots, anchors, k2, k3, cells, dual)

    result = json.loads(RESULT.read_text())
    require(result["status"] == "PASS_COMPLETE_D14_222_R_2_3_2_K21_CHARGE", result["status"])
    require(result["lineage_id"] == "D14:222|R:2-3-2", result["lineage_id"])
    require(int(result["scale_U"]) == U, result["scale_U"])
    require(result["input_interval"] == [0, N], result["input_interval"])
    require(result["input_records_declared"] == result["input_records_consumed"] == N, result)
    require(result["upstream_labelled_p2_uses_before_zero"] == 511_477_120, result)
    require(result["retained_nonzero_pair_witness_uses"] == 511_214_060, result)
    require(int(result["pair_weight_sum_scaled"]) == header["weight_sum_scaled"], result)
    require(result["K3_to_K19_tail_evaluations"] == 32 * N == 3_249_463_136, result)
    require(result["K21_terminal_occurrences"] == 12 * result["selected_p3_uses"], result)
    require(result["full_occurrences"] == result["irreducible_occurrences"] == result["K21_terminal_occurrences"], result)
    require(result["full_charge_scaled"] == result["irreducible_charge_scaled"], result)
    require(int(result["normalized_p3_weight_sum_scaled"]) == -int(result["pivotable_K19_weight_sum_scaled"]), result)
    require(int(result["K21_weight_sum_scaled"]) == 12 * int(result["normalized_p3_weight_sum_scaled"]), result)
    require(result["response_cache"]["hits"] + result["response_cache"]["misses"] == result["selected_p3_uses"], result["response_cache"])
    require(result["response_cache"]["peak_keys_per_worker_chunk"] <= 400_000, result["response_cache"])
    require(result["elapsed_seconds"] < 600, result["elapsed_seconds"])
    require(result["literal_sample_guard"]["records"] == 257 and result["literal_sample_guard"]["nonzero_continuations"] == 212, result["literal_sample_guard"])

    prov = result["m2_m3_provenance"].values()
    require(sum(x["pivotable_K19_children"] for x in prov) == result["pivotable_K19_children"], "provenance pivotable")
    require(sum(int(x["signed_K19_weight_scaled"]) for x in result["m2_m3_provenance"].values()) == int(result["pivotable_K19_weight_sum_scaled"]), "provenance weight")
    require(sum(x["selected_p3_uses"] for x in result["m2_m3_provenance"].values()) == result["selected_p3_uses"], "provenance p3")
    require(sum(x["K21_children"] for x in result["m2_m3_provenance"].values()) == result["K21_terminal_occurrences"], "provenance K21")
    require(sum(int(x["charge_scaled"]) for x in result["m2_m3_provenance"].values()) == int(result["full_charge_scaled"]), "provenance charge")
    require(result["stabilizer_histogram"] == {"1": 99_314_228, "2": 2_212_958, "4": 16_210, "8": 2_099, "16": 224, "32": 4}, result["stabilizer_histogram"])
    require(sum(result["stabilizer_histogram"].values()) == N, result["stabilizer_histogram"])

    scaled_charge = int(result["full_charge_scaled"])
    require(scaled_charge == -879_849_881_597_204_692_992, scaled_charge)
    reduced = Fraction(scaled_charge, U)
    require(reduced == Fraction(-381_879_288_887_675_648, 173_867_925), reduced)

    source = SOURCE.read_text()
    source_guards = {
        "strict_singleton": '\\"lineage_id\\":\\"D14:222|R:2-3-2' in source,
        "decorated_pair_schema": "row: Row(row), pivot: rec[24]" in source,
        "representative_K3_family": "for tail3 in &e.all_k3[p2]" in source,
        "literal_K19_pivots": "let pivots3 = available(sig19, e);" in source,
        "exact_prior_and_terminal_divisions": "assert_eq!(U % ((m2 as i128) * (m3 as i128)), 0);" in source and "assert_eq!(x.weight_after_p2 % (m3 as i128), 0);" in source,
        "third_response_sign": "let w3 = -x.weight_after_p2 / (m3 as i128);" in source,
        "universal_realized_key_terminality": "realized abstract terminal-K2 response remained pivotable at K21" in source,
        "literal_sample_terminality": "assert!(!pivotable_sig(sig21, e));" in source,
        "literal_abstract_cycle_equality": "assert_eq!(abstracted, literal);" in source,
        "atomic_result": "rename(tmp, output).unwrap();" in source,
        "hard_600_second_gate": "assert!(elapsed < FULL_GATE_SECONDS" in source,
        "no_child_row_output": "K19/K21 row collection unnecessary" in source,
    }
    require(all(source_guards.values()), source_guards)
    abstract_terminal_checks = 12 * result["response_cache"]["misses"]

    audit = {
        "schema": "orbit0-independent-hidden-d14-r2-3-2-k21-referee-v1",
        "status": "PASS_INDEPENDENT_D14_222_R_2_3_2_K21_SOURCE_COUNT_SAMPLE_TERMINAL_REFEREE",
        "scope": "Strict singleton immediate K21 scalar; independent package/source/count and 257 literal-sample replay, not a second 101,545,723-record charge evaluation.",
        "lineage_id": "D14:222|R:2-3-2",
        "charge": {
            "scale_U": U,
            "scaled_full_and_irreducible": str(scaled_charge),
            "reduced_full_and_irreducible": str(reduced),
        },
        "counts": {
            "decorated_pair_orbits": N,
            "K3_to_K19_tail_evaluations": result["K3_to_K19_tail_evaluations"],
            "pivotable_K19_children": result["pivotable_K19_children"],
            "selected_p3_uses": result["selected_p3_uses"],
            "terminal_K21_occurrences": result["K21_terminal_occurrences"],
        },
        "pair_header": header,
        "provenance_zero_boundary": {
            "upstream_labelled_p2_uses_before_exact_zero_removal": 511_477_120,
            "retained_nonzero_pair_witness_uses": 511_214_060,
            "difference": 263_060,
            "coefficient_authority": "retained record weight_i128 and header weight sum; uses_u64 is witness provenance only",
        },
        "terminality": {
            "realized_terminal_cache_keys": result["response_cache"]["misses"],
            "abstract_K2_children_checked": abstract_terminal_checks,
            "cache_hits_reusing_identical_terminal_keys": result["response_cache"]["hits"],
            "full_equals_irreducible": True,
        },
        "sample_audit": sample_audit,
        "source_guards": source_guards,
        "resource_gate": {
            "prefix10m_elapsed_seconds": 24.263656,
            "prefix10m_observed_RSS_KiB": 602_928,
            "prefix10m_projected_full_seconds": 246.387054,
            "full_elapsed_seconds": result["elapsed_seconds"],
            "full_gate_seconds": 600,
            "RSS_gate_bytes": 16 * (1 << 30),
            "no_bulk_row_output": True,
        },
        "pinned_sha256": hashes,
    }
    logical = json.dumps(audit, sort_keys=True, separators=(",", ":")).encode()
    audit["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": audit["status"],
        "charge": str(reduced),
        "terminal_K21_occurrences": result["K21_terminal_occurrences"],
        "literal_sample_terminal_children": sample_audit["literal_terminal_K21_children_replayed"],
        "logical_sha256": audit["logical_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
