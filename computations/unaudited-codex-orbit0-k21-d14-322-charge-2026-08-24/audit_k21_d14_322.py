#!/usr/bin/env python3
"""Independent aggregate and 257-witness referee for D14:222|R:3-2-2."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import csv
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "results_k21_d14_322_charge.json"
SAMPLES = HERE / "results_k21_d14_322_charge.json.samples.tsv"
SOURCE = HERE / "run_k21_d14_322_charge.rs"
STRUCTURE = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin"
AUX = STRUCTURE.with_name("filtered_k17_aux.bin")
CYCLE = STRUCTURE.with_name("filtered_k17_cycle_aux.bin")
K4 = ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin"
PROVIDER = K4.with_name("run_k18_charge.rs")
OUT = HERE / "results_k21_d14_322_audit.json"

U = 400_591_699_200
N_R8 = 485
HEADS_PER_R8 = 1728
N_HEADS = N_R8 * HEADS_PER_R8
LINEAGE = "D14:222|R:3-2-2"
PINS = {
    STRUCTURE: "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    AUX: "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    CYCLE: "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    K4: "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
    PROVIDER: "24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
    SOURCE: "9667311ff4c870eee1f6a8e7f881bb9082f01f1b6bceee7947404901a8003e72",
    RESULT: "46065e0c432be6b37ca4044998a8cada8a0e83527699581ff2040735cdd7f7aa",
    SAMPLES: "5791b75e9412cca4eb0cdcea2ae262f91a1fb7e2f02d0891b82446c16ef872be",
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


def audit_samples(records, factors, pivots, perms, cover, anchors, k2, k3,
                  positions, cells, dual):
    with SAMPLES.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    require(len(rows) == 257, len(rows))
    require({int(x["sample_bin"]) for x in rows} == set(range(257)), "sample bins")
    terminal_children = 0
    for x in rows:
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
        require(int(x["K17_candidates"]) == 32 * len(ps1), head)

        t3 = int(x["witness_t3"])
        row17 = replace(row14, anchors[p1], k3[p1][t3])
        require(row17.hex() == x["witness_row17"], head)
        s17 = child_signature(s14, pivots[p1], k3[p1][t3], positions)
        require(signature(row17, positions) == s17 and sum(s17) == 7, head)
        ps2 = available(s17, pivots)
        m2, p2 = int(x["m2"]), int(x["witness_p2"])
        require(m2 == len(ps2) and p2 in ps2, (head, m2, ps2))

        t2 = int(x["witness_t2"])
        row19 = replace(row17, anchors[p2], k2[p2][t2])
        require(row19.hex() == x["witness_row19"], head)
        s19 = child_signature(s17, pivots[p2], k2[p2][t2], positions)
        require(signature(row19, positions) == s19 and sum(s19) == 5, head)
        ps3 = available(s19, pivots)
        m3, p3 = int(x["m3"]), int(x["witness_p3"])
        require(m3 == len(ps3) and p3 in ps3, (head, m3, ps3))
        require(U % (m1 * m2 * m3) == 0, (head, m1, m2, m3))

        q = 0
        for tail in k2[p3]:
            s21 = child_signature(s19, pivots[p3], tail, positions)
            require(sum(s21) == 3 and not available(s21, pivots), (head, p3, s21))
            row21 = replace(row19, anchors[p3], tail)
            require(signature(row21, positions) == s21, head)
            q += charge(row21, cells, dual)
            terminal_children += 1
        require(q == int(x["witness_terminal_q"]), (head, q, x["witness_terminal_q"]))
        require(int(x["K19_candidates"]) == 12 * int(x["p2_uses"]), head)
        require(int(x["K21_children"]) == 12 * int(x["p3_uses"]), head)
        require(int(x["charge_scaled_U"]) != 0, head)
    return terminal_children


def main():
    for path, expected in PINS.items():
        require(digest(path) == expected, (path, digest(path), expected))
    active, perms, records, pivots, factors = parse_structure()
    cover, anchors, k2, k3 = parse_aux()
    cells, dual = parse_cycle()
    positions = {cell: i for i, cell in enumerate(active)}
    r = json.loads(RESULT.read_text())
    require(r["status"] == "PASS_COMPLETE_SINGLETON_D14_222_R_3_2_2_K21_CHARGE", r["status"])
    require(r["lineage_id"] == LINEAGE and r["covered_ids"] == 1, r)
    require(int(r["scale_U"]) == U and r["R8_records_consumed"] == r["R8_records_declared"] == N_R8, r)
    require(r["source_heads"] == N_HEADS, r["source_heads"])
    signed = HEADS_PER_R8 * sum(size * coeff for _, size, coeff in records)
    l1 = HEADS_PER_R8 * sum(abs(size * coeff) for _, size, coeff in records)
    require((int(r["source_mass_sum"]), int(r["source_mass_l1"])) == (signed, l1), (signed, l1))
    require((r["selected_p1_uses"], r["K17_candidates"], r["pivotable_K17_children"],
             r["selected_p2_uses"], r["K19_candidates"]) ==
            (6_619_280, 211_816_960, 197_414_400, 815_482_880, 9_785_794_560), r)
    require(r["K17_candidates"] == 32 * r["selected_p1_uses"], r)
    require(r["K19_candidates"] == 12 * r["selected_p2_uses"], r)
    require(r["K21_terminal_occurrences"] == 12 * r["selected_p3_uses"], r)
    require(r["K21_terminal_occurrences"] == r["full_occurrences"] ==
            r["irreducible_occurrences"] == 60_904_949_760, r)
    require(r["all_K21_children_irreducible"] is True, r)
    require(sum(map(int, r["first_denominator_hist"].values())) == N_HEADS, r)
    require(weighted(r["first_denominator_hist"]) == r["selected_p1_uses"], r)
    require(sum(map(int, r["second_denominator_hist"].values())) == r["pivotable_K17_children"], r)
    require(weighted(r["second_denominator_hist"]) == r["selected_p2_uses"], r)
    require(sum(map(int, r["third_denominator_hist"].values())) == r["pivotable_K19_children"], r)
    require(weighted(r["third_denominator_hist"]) == r["selected_p3_uses"], r)
    require(sum(map(int, r["product_denominator_hist"].values())) == r["pivotable_K19_children"], r)
    require(all(U % int(k) == 0 for k in r["product_denominator_hist"]), r)
    scaled = int(r["full_charge_scaled_U"])
    require(scaled == int(r["irreducible_charge_scaled_U"]) == -832_152_508_704_647_184_384, scaled)
    value = Fraction(scaled, U)
    require(value == Fraction(-32_834_300_375_025_536, 15_806_175), value)
    terminal_children = audit_samples(records, factors, pivots, perms, cover,
                                      anchors, k2, k3, positions, cells, dual)
    require(terminal_children == 257 * 12, terminal_children)
    report = {
        "status": "PASS_INDEPENDENT_AGGREGATE_AND_257_LITERAL_D14_322_K21_REFEREE",
        "strict_lineage_id": LINEAGE,
        "covered_ids": 1,
        "scale_U": str(U),
        "charge_scaled_U": str(scaled),
        "charge": f"{value.numerator}/{value.denominator}",
        "source_counts": {
            "R8_records": N_R8, "heads": N_HEADS,
            "p1_uses": r["selected_p1_uses"], "K17_candidates": r["K17_candidates"],
            "pivotable_K17": r["pivotable_K17_children"], "p2_uses": r["selected_p2_uses"],
            "K19_candidates": r["K19_candidates"], "pivotable_K19": r["pivotable_K19_children"],
            "p3_uses": r["selected_p3_uses"], "K21_terminal": r["K21_terminal_occurrences"],
        },
        "guards": {
            "source_mass_rederived": True, "all_U_divisions_exact": True,
            "three_response_sign_is_positive_relative_to_source_M": True,
            "full_equals_irreducible": True, "no_K22": True,
            "distributed_nonzero_literal_samples": 257,
            "literal_terminal_children_replayed": terminal_children,
            "all_replayed_terminal_children_irreducible": True,
            "strict_singleton_scope": True,
        },
        "pinned": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    }
    logical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
