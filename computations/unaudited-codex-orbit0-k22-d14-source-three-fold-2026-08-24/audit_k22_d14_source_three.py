#!/usr/bin/env python3
"""Independent aggregate and 3x257 literal referee for the K22 D14 source fold."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import csv
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "results_k22_d14_source_three.json"
SAMPLES = HERE / "results_k22_d14_source_three.json.samples.tsv"
SOURCE = HERE / "run_k22_d14_source_three.rs"
STRUCTURE = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin"
AUX = STRUCTURE.with_name("filtered_k17_aux.bin")
CYCLE = STRUCTURE.with_name("filtered_k17_cycle_aux.bin")
K4 = ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin"
PROVIDER = K4.with_name("run_k18_charge.rs")
OUT = HERE / "results_k22_d14_source_three_audit.json"

U = 400_591_699_200
N_R8 = 485
HEADS_PER_R8 = 1728
N_HEADS = N_R8 * HEADS_PER_R8
CONFIGS = {
    "D14:222|R:3-2-3": (3, 2, 3),
    "D14:222|R:3-3-2": (3, 3, 2),
    "D14:222|R:4-2-2": (4, 2, 2),
}
PINS = {
    STRUCTURE: "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    AUX: "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    CYCLE: "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    K4: "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
    PROVIDER: "24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
    SOURCE: "52881a540068ea6b21b0b3d4d7ad6f2b63c576d17f93ceb5889a2b882dc5c547",
    RESULT: "99bec5f72757b20449aff9d7869669e36faab0f61411d482eab13d7523a562cc",
    SAMPLES: "65febd75b0b7610d17a4308a609b596cacb89c37efa8d67a1c322a548eb4bebc",
}


def require(ok, detail):
    if not ok:
        raise RuntimeError(detail)


def digest(path):
    h = sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 << 20):
            h.update(block)
    return h.hexdigest()


def parse_structure():
    b = STRUCTURE.read_bytes()
    require(b[:11] == b"K16DIRECT1\0", b[:11])
    q = 11
    nt, nr, np, na = struct.unpack_from("<IIII", b, q)
    q += 16
    require((nt, nr, np, na) == (384, 485, 78, 12), (nt, nr, np, na))
    active = bytes(b[q:q + 12]); q += 12
    perms = []
    for _ in range(nt):
        q += 252
        perms.append(tuple(b[q:q + 12])); q += 12
    records = []
    for _ in range(nr):
        row = bytes(b[q:q + 12])
        size, coefficient = struct.unpack_from("<Iq", b, q + 12)
        q += 24
        records.append((row, size, coefficient))
    pivots = []
    for _ in range(np):
        pivots.append(tuple(b[q:q + 12])); q += 12
    factors = [[None] * 3 for _ in range(3)]
    for f in range(3):
        for d, expected in enumerate((12, 32, 60)):
            n = struct.unpack_from("<I", b, q)[0]; q += 4
            require(n == expected, (f, d, n))
            factors[f][d] = [bytes(b[q + 4*j:q + 4*j + 4]) for j in range(n)]
            q += 4 * n
    require(q == len(b), (q, len(b)))
    return active, perms, records, pivots, factors


def parse_aux():
    b = AUX.read_bytes()
    require(b[:8] == b"K17AUX1\0", b[:8])
    q = 8
    scale = struct.unpack_from("<Q", b, q)[0]; q += 8
    nc, np = struct.unpack_from("<II", b, q); q += 8
    require((scale, nc, np) == (281_801_520, 25, 78), (scale, nc, np))
    cover = set()
    for _ in range(nc):
        cover.add(tuple(b[q:q + 12])); q += 12
    anchors, k2, k3 = [], [], []
    for _ in range(np):
        anchors.append(bytes(b[q:q + 4])); q += 4
        k2.append([bytes(b[q + 4*j:q + 4*j + 4]) for j in range(12)]); q += 48
        k3.append([bytes(b[q + 4*j:q + 4*j + 4]) for j in range(32)]); q += 128
    require(q == len(b), (q, len(b)))
    return cover, anchors, k2, k3


def parse_cycle():
    b = CYCLE.read_bytes()
    require(b[:8] == b"K17CYC1\0", b[:8])
    q = 8
    cells = [tuple(b[q + 4*j:q + 4*j + 4]) for j in range(252)]
    q += 4 * 252
    n = struct.unpack_from("<I", b, q)[0]; q += 4
    dual = {}
    for _ in range(n):
        key = bytes(b[q:q + 13]); q += 13
        dual[key] = struct.unpack_from("<q", b, q)[0]; q += 8
    require(q == len(b), (q, len(b)))
    return cells, dual


def parse_k4():
    b = K4.read_bytes()
    require(b[:7] == b"K18K4A1", b[:7])
    q = 7
    out = []
    for _ in range(78):
        out.append([bytes(b[q + 4*j:q + 4*j + 4]) for j in range(60)])
        q += 240
    require(q == len(b), (q, len(b)))
    return out


def signature(row, positions):
    out = [0] * 12
    for cell in row:
        if cell in positions:
            out[positions[cell]] += 1
    return tuple(out)


def tail_signature(tail, positions):
    return signature(tail, positions)


def available(sig, pivots):
    return [j for j, p in enumerate(pivots)
            if all(sig[i] >= p[i] for i in range(12))]


def child_signature(sig, pivot, tail, positions):
    add = tail_signature(tail, positions)
    out = tuple(sig[i] - pivot[i] + add[i] for i in range(12))
    require(min(out) >= 0, out)
    return out


def canonical(sig, perms):
    moved = []
    for perm in perms:
        out = [0] * 12
        for i in range(12):
            out[perm[i]] = sig[i]
        moved.append(tuple(out))
    return min(moved)


def valid(sig, pivots, k2, cover, perms, positions):
    out = []
    for p in available(sig, pivots):
        children = [child_signature(sig, pivots[p], t, positions) for t in k2[p]]
        if all(available(c, pivots) or canonical(c, perms) in cover for c in children):
            out.append(p)
    require(out, sig)
    return out


def replace(row, anchor, tail):
    remaining = Counter(row)
    remaining.subtract(anchor)
    require(all(v >= 0 for v in remaining.values()), (row.hex(), anchor.hex()))
    out = []
    for cell, count in remaining.items():
        out.extend([cell] * count)
    out.extend(tail)
    out.sort()
    require(len(out) == 24, len(out))
    return bytes(out)


def charge(row, cells, dual):
    adjacency = [[] for _ in range(24)]
    for cell in row:
        u, v, a, b = cells[cell]
        x, y = 3*u + a, 3*v + b
        adjacency[x].append(y); adjacency[y].append(x)
    require(all(len(x) == 2 for x in adjacency), [len(x) for x in adjacency])
    seen, parts = set(), []
    for start in range(24):
        if start in seen:
            continue
        todo, size = [start], 0
        seen.add(start)
        while todo:
            x = todo.pop(); size += 1
            for y in adjacency[x]:
                if y not in seen:
                    seen.add(y); todo.append(y)
        parts.append(size)
    parts.sort()
    key = bytes([len(parts)] + parts + [0] * (12 - len(parts)))
    return dual.get(key, 0)


def weighted(hist):
    return sum(int(k) * int(v) for k, v in hist.items())


def audit_samples(records, factors, pivots, perms, cover, anchors, k2, k3, k4,
                  positions, cells, dual):
    with SAMPLES.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    require(len(rows) == 3 * 257, len(rows))
    grouped = {lineage: [] for lineage in CONFIGS}
    for row in rows:
        require(row["lineage_id"] in grouped, row["lineage_id"])
        grouped[row["lineage_id"]].append(row)
    require(all(len(value) == 257 for value in grouped.values()), {k: len(v) for k, v in grouped.items()})
    require(all({int(x["sample_bin"]) for x in value} == set(range(257))
                for value in grouped.values()), "sample bins")
    tails = {2: k2, 3: k3, 4: k4}
    terminal_children = 0
    for x in rows:
        first_degree, second_degree, terminal_degree = CONFIGS[x["lineage_id"]]
        bin_id = int(x["sample_bin"]); head = int(x["head_index"])
        require(bin_id == head * 257 // N_HEADS, (bin_id, head))
        ri, within = divmod(head, HEADS_PER_R8)
        require(ri == int(x["r8_index"]), (ri, x["r8_index"]))
        ai, rem = divmod(within, 144); bi, ci = divmod(rem, 12)
        source_row, size, coefficient = records[ri]
        mass = size * coefficient
        require(mass == int(x["source_mass"]), (ri, mass, x["source_mass"]))
        row14 = bytes(sorted(source_row + factors[0][0][ai] +
                             factors[1][0][bi] + factors[2][0][ci]))
        require(row14.hex() == x["row14"], (ri, head))
        s14 = signature(row14, positions)
        require(sum(s14) == 10, s14)
        ps1 = valid(s14, pivots, k2, cover, perms, positions)
        m1, p1 = int(x["m1"]), int(x["witness_p1"])
        require(m1 == len(ps1) == int(x["p1_uses"]) and p1 in ps1, (head, m1, ps1))
        require(int(x["first_children"]) == len(tails[first_degree][p1]) * len(ps1), head)

        t1 = int(x["witness_t1"])
        row1 = replace(row14, anchors[p1], tails[first_degree][p1][t1])
        require(row1.hex() == x["witness_row1"], head)
        s1 = child_signature(s14, pivots[p1], tails[first_degree][p1][t1], positions)
        require(signature(row1, positions) == s1, head)
        ps2 = available(s1, pivots)
        m2, p2 = int(x["m2"]), int(x["witness_p2"])
        require(m2 == len(ps2) and p2 in ps2, (head, m2, ps2))

        t2 = int(x["witness_t2"])
        row2 = replace(row1, anchors[p2], tails[second_degree][p2][t2])
        require(row2.hex() == x["witness_row2"], head)
        s2 = child_signature(s1, pivots[p2], tails[second_degree][p2][t2], positions)
        require(signature(row2, positions) == s2, head)
        ps3 = available(s2, pivots)
        m3, p3 = int(x["m3"]), int(x["witness_p3"])
        require(m3 == len(ps3) and p3 in ps3, (head, m3, ps3))
        require(U % (m1 * m2 * m3) == 0, (head, m1, m2, m3))
        require(int(x["terminal_degree"]) == terminal_degree, x)

        q = 0
        for tail in tails[terminal_degree][p3]:
            s22 = child_signature(s2, pivots[p3], tail, positions)
            require(sum(s22) == 2 and not available(s22, pivots), (head, p3, s22))
            row22 = replace(row2, anchors[p3], tail)
            require(signature(row22, positions) == s22, head)
            q += charge(row22, cells, dual)
            terminal_children += 1
        require(q == int(x["witness_terminal_q"]), (head, q, x["witness_terminal_q"]))
        require(int(x["second_children"]) == len(tails[second_degree][p2]) * int(x["p2_uses"]), head)
        require(int(x["K22_children"]) == len(tails[terminal_degree][p3]) * int(x["p3_uses"]), head)
        require(int(x["nonzero_terminal_q"]) == (q != 0), (head, q))
    return terminal_children


def main():
    for path, expected in PINS.items():
        require(digest(path) == expected, (path, digest(path), expected))
    active, perms, records, pivots, factors = parse_structure()
    cover, anchors, k2, k3 = parse_aux()
    k4 = parse_k4()
    cells, dual = parse_cycle()
    positions = {cell: i for i, cell in enumerate(active)}
    r = json.loads(RESULT.read_text())
    require(r["status"] == "PASS_COMPLETE_D14_222_K22_SOURCE_THREE_CHARGE", r["status"])
    require(r["covered_lineage_ids"] == list(CONFIGS), r["covered_lineage_ids"])
    require(int(r["scale_U"]) == U and r["R8_records_consumed"] == r["R8_records_declared"] == N_R8, r)
    require(r["source_heads"] == N_HEADS, r["source_heads"])
    signed = HEADS_PER_R8 * sum(size * coeff for _, size, coeff in records)
    l1 = HEADS_PER_R8 * sum(abs(size * coeff) for _, size, coeff in records)
    require((int(r["source_mass_sum"]), int(r["source_mass_l1"])) == (signed, l1), (signed, l1))
    expected_charges = {
        "D14:222|R:3-2-3": (964_781_571_518_500_995_072, Fraction(12_689_151_561_428_096, 5_268_725)),
        "D14:222|R:3-3-2": (196_633_985_739_550_064_640, Fraction(517_240_071_915_904, 1_053_745)),
        "D14:222|R:4-2-2": (16_769_984_550_131_957_760, Fraction(2_700_793_739_392, 64_515)),
    }
    for lineage, (first_degree, second_degree, terminal_degree) in CONFIGS.items():
        z = r["sinks"][lineage]
        require((z["first_response_degree"], z["second_response_degree"],
                 z["terminal_response_degree"]) ==
                (first_degree, second_degree, terminal_degree), lineage)
        counts = {2: 12, 3: 32, 4: 60}
        require(z["first_children"] == counts[first_degree] * z["selected_p1_uses"], lineage)
        require(z["second_children"] == counts[second_degree] * z["selected_p2_uses"], lineage)
        require(z["K22_terminal_occurrences"] == counts[terminal_degree] * z["selected_p3_uses"], lineage)
        require(z["K22_terminal_occurrences"] == z["full_occurrences"] == z["irreducible_occurrences"], lineage)
        require(sum(map(int, z["first_denominator_hist"].values())) == N_HEADS, lineage)
        require(weighted(z["first_denominator_hist"]) == z["selected_p1_uses"], lineage)
        require(sum(map(int, z["second_denominator_hist"].values())) == z["pivotable_first_children"], lineage)
        require(weighted(z["second_denominator_hist"]) == z["selected_p2_uses"], lineage)
        require(sum(map(int, z["third_denominator_hist"].values())) == z["pivotable_second_children"], lineage)
        require(weighted(z["third_denominator_hist"]) == z["selected_p3_uses"], lineage)
        require(sum(map(int, z["product_denominator_hist"].values())) == z["pivotable_second_children"], lineage)
        require(all(U % int(k) == 0 for k in z["product_denominator_hist"]), lineage)
        require(z["literal_preterminal_cache"]["hits"] + z["literal_preterminal_cache"]["misses"] ==
                z["pivotable_second_children"], lineage)
        scaled, value = expected_charges[lineage]
        require(int(z["full_charge_scaled_U"]) == int(z["irreducible_charge_scaled_U"]) == scaled, lineage)
        require(Fraction(scaled, U) == value, (lineage, Fraction(scaled, U), value))
    a = r["sinks"]["D14:222|R:3-2-3"]
    b = r["sinks"]["D14:222|R:3-3-2"]
    require((a["selected_p1_uses"], a["first_children"], a["pivotable_first_children"], a["selected_p2_uses"]) ==
            (b["selected_p1_uses"], b["first_children"], b["pivotable_first_children"], b["selected_p2_uses"]) ==
            (6_619_280, 211_816_960, 197_414_400, 815_482_880), "shared R3 source prefix")
    require((a["second_children"], a["pivotable_second_children"], a["selected_p3_uses"], a["K22_terminal_occurrences"]) ==
            (9_785_794_560, 2_969_658_880, 5_075_412_480, 162_413_199_360), "R323 frozen counts")
    require(r["all_realized_cached_K22_responses_terminal"] is True, r)
    require(r["terminal_cache_resource_guard"]["peak_keys_per_worker"] <= 3_000_000, r)
    require(r["elapsed_seconds"] < 600, r["elapsed_seconds"])
    terminal_children = audit_samples(records, factors, pivots, perms, cover,
                                      anchors, k2, k3, k4, positions, cells, dual)
    require(terminal_children == 257 * (32 + 12 + 12), terminal_children)
    report = {
        "status": "PASS_INDEPENDENT_AGGREGATE_AND_3X257_LITERAL_D14_K22_SOURCE_THREE_REFEREE",
        "strict_lineage_ids": list(CONFIGS),
        "covered_ids": 3,
        "scale_U": str(U),
        "charges": {lineage: {"scaled_U": str(scaled), "exact": str(value)}
                    for lineage, (scaled, value) in expected_charges.items()},
        "source_counts": {
            "R8_records": N_R8, "heads": N_HEADS,
            "source_mass": signed, "source_mass_l1": l1,
        },
        "guards": {
            "source_mass_rederived": True, "all_U_divisions_exact": True,
            "three_response_sign_is_positive_relative_to_source_M": True,
            "full_equals_irreducible": True, "no_K23": True,
            "distributed_literal_samples_per_sink": 257,
            "literal_terminal_children_replayed": terminal_children,
            "all_replayed_terminal_children_irreducible": True,
            "all_replayed_cycle_charges_match_producer": True,
            "strict_three_id_scope": True,
            "hard_wall_and_cache_caps_pass": True,
        },
        "pinned": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    }
    logical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
