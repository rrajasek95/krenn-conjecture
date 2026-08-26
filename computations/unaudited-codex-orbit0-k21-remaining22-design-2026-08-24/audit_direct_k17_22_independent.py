#!/usr/bin/env python3
"""Independent bounded referee for D17:*|R:2-2; no full producer replay."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUN = ROOT / "computations/unaudited-codex-orbit0-k21-direct-k17-22-2026-08-24"
SOURCE = RUN / "run_k21_direct_k17_22.rs"
RESULT = RUN / "results_k21_direct_k17_22.json"
SAMPLES = RUN / "results_k21_direct_k17_22.json.samples.tsv"
STRUCTURE = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin"
AUX = STRUCTURE.with_name("filtered_k17_aux.bin")
CYCLE = STRUCTURE.with_name("filtered_k17_cycle_aux.bin")
CENSUS = ROOT / "computations/unaudited-codex-orbit0-k19-profile-census-2026-08-23/results_k19_profile_census.json"
OUT = HERE / "results_direct_k17_22_independent_referee.json"

U = 400_591_699_200
IDS = [f"D17:{x}|R:2-2" for x in ("234", "243", "324", "333", "342", "423", "432")]
PINS = {
    SOURCE: "7999b1797e3103f254977b17f60ff42088f4eee6726ba4e7006b86f08cff05b7",
    RESULT: "9c217ea0a646ae8f7bceec1c1dd946d54b991b454046496fd7280127096a758c",
    SAMPLES: "7e37f02831ae227e96f0f4f64cadc774dcadb274650b9c9aa4fb727f878cbc5d",
    STRUCTURE: "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    AUX: "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    CYCLE: "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    CENSUS: "2554ddf0698c3001a765a40e9af34af3bfbefb3c76e9aa18068487c16a7155bd",
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


def parse_structure():
    b = STRUCTURE.read_bytes()
    require(b[:11] == b"K16DIRECT1\0", b[:11])
    q = 11
    nt, nr, np, na = struct.unpack_from("<IIII", b, q)
    q += 16
    require((nt, nr, np, na) == (384, 485, 78, 12), (nt, nr, np, na))
    anchor_cells = b[q:q + 12]
    q += 12 + nt * (252 + 12)
    records = []
    for _ in range(nr):
        row = b[q:q + 12]
        size, coefficient = struct.unpack_from("<Iq", b, q + 12)
        q += 24
        records.append((row, size, coefficient))
    pivots = []
    for _ in range(np):
        pivots.append(b[q:q + 12])
        q += 12
    factors = [[None] * 3 for _ in range(3)]
    for factor in range(3):
        for degree_index, expected in enumerate((12, 32, 60)):
            n = struct.unpack_from("<I", b, q)[0]
            q += 4
            require(n == expected, (factor, degree_index, n))
            factors[factor][degree_index] = {
                b[q + 4 * j:q + 4 * j + 4] for j in range(n)
            }
            q += 4 * n
    require(q == len(b), (q, len(b)))
    return anchor_cells, records, pivots, factors


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
    anchors, tails = [], []
    for _ in range(npa):
        anchors.append(b[q:q + 4])
        q += 4
        k2 = [b[q + 4 * j:q + 4 * j + 4] for j in range(12)]
        q += 48
        q += 32 * 4
        tails.append(k2)
    require(q == len(b), (q, len(b)))
    return anchors, tails


def parse_cycle():
    b = CYCLE.read_bytes()
    q = 8
    cells = []
    for _ in range(252):
        cells.append(tuple(b[q:q + 4]))
        q += 4
    nd = struct.unpack_from("<I", b, q)[0]
    q += 4
    dual = {}
    for _ in range(nd):
        key = b[q:q + 13]
        value = struct.unpack_from("<q", b, q + 13)[0]
        q += 21
        dual[key] = value
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
    return [j for j, pivot in enumerate(pivots)
            if all(sig[i] >= pivot[i] for i in range(12))]


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


def child_signature(sig, pivot, tail, positions):
    add = tail_signature(tail, positions)
    out = [sig[i] - pivot[i] + add[i] for i in range(12)]
    require(all(x >= 0 for x in out), out)
    return out


def charge(row, cells, dual):
    adjacency = [[] for _ in range(24)]
    for cell in row:
        u, v, a, b = cells[cell]
        x, y = 3 * u + a, 3 * v + b
        adjacency[x].append(y)
        adjacency[y].append(x)
    require(all(len(x) == 2 for x in adjacency), [len(x) for x in adjacency])
    seen, parts = set(), []
    for start in range(24):
        if start in seen:
            continue
        todo, size = [start], 0
        seen.add(start)
        while todo:
            vertex = todo.pop()
            size += 1
            for nxt in adjacency[vertex]:
                if nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
        parts.append(size)
    parts.sort()
    key = bytes([len(parts)] + parts + [0] * (12 - len(parts)))
    require(len(key) == 13, key)
    return dual.get(key, 0)


def audit_samples(anchor_cells, records, pivots, factors, anchors, tails, cells, dual):
    lines = SAMPLES.read_text().splitlines()
    require(len(lines) == 258, len(lines))
    expected_indices = {j * 484 // 256 for j in range(257)}
    observed = set()
    total_terminal_children = 0
    for line in lines[1:]:
        fields = line.split("\t")
        require(len(fields) == 13, fields)
        lineage, ri_text, row_hex = fields[:3]
        require(lineage == "D17:234|R:2-2", lineage)
        ri = int(ri_text)
        observed.add(ri)
        row = bytes.fromhex(row_hex)
        factor_tails = [bytes.fromhex(x) for x in fields[3:6]]
        source_mass, m1, p1 = map(int, fields[6:9])
        reported_pivotable, reported_p2, reported_k21, reported_charge = map(int, fields[9:13])
        source_row, size, coefficient = records[ri]
        require(source_mass == size * coefficient, (ri, source_mass, size * coefficient))
        for factor, (digit, tail) in enumerate(zip("234", factor_tails)):
            require(tail in factors[factor][int(digit) - 2], (factor, digit, tail.hex()))
        require(row == bytes(sorted(source_row + b"".join(factor_tails))), (ri, row.hex()))
        positions = {cell: j for j, cell in enumerate(anchor_cells)}
        s1 = signature(row, positions)
        ps1 = available(s1, pivots)
        require(m1 == len(ps1) and p1 in ps1, (ri, m1, p1, ps1))

        pivotable = p2_uses = k21_children = 0
        charge_per_mass = 0
        for tail1 in tails[p1]:
            k19 = replace(row, anchors[p1], tail1)
            s2 = child_signature(s1, pivots[p1], tail1, positions)
            require(s2 == signature(k19, positions), (ri, p1, tail1.hex()))
            ps2 = available(s2, pivots)
            if not ps2:
                continue
            pivotable += 1
            m2 = len(ps2)
            require(U % (m1 * m2) == 0, (ri, m1, m2))
            unit = -U // (m1 * m2)
            for p2 in ps2:
                p2_uses += 1
                for tail2 in tails[p2]:
                    s3 = child_signature(s2, pivots[p2], tail2, positions)
                    require(not available(s3, pivots), (ri, p1, p2, tail2.hex(), s3))
                    k21 = replace(k19, anchors[p2], tail2)
                    require(s3 == signature(k21, positions), (ri, p1, p2))
                    charge_per_mass += unit * charge(k21, cells, dual)
                    k21_children += 1
        require((pivotable, p2_uses, k21_children, charge_per_mass) ==
                (reported_pivotable, reported_p2, reported_k21, reported_charge),
                (ri, (pivotable, p2_uses, k21_children, charge_per_mass),
                 (reported_pivotable, reported_p2, reported_k21, reported_charge)))
        total_terminal_children += k21_children
    require(observed == expected_indices, (observed, expected_indices))
    require(total_terminal_children == 0,
            "producer samples unexpectedly changed from source-only witnesses")
    return {
        "samples": 257,
        "spacing": "floor(j*484/256), j=0..256",
        "literal_source_rows_rebuilt": 257,
        "first_response_witnesses_rebuilt": 257,
        "sample_terminal_K21_children_rebuilt": total_terminal_children,
        "producer_sample_scope": "Source row, factor membership, signed mass, and selected first-pivot availability only; every stored selected p1 has zero K19 continuation.",
        "terminal_tail_claim_from_producer_samples": False,
    }


def independent_nonzero_witnesses(anchor_cells, records, pivots, factors,
                                  anchors, tails, cells, dual):
    """Find and fully replay one nonzero continuation for each requested ID."""
    positions = {cell: j for j, cell in enumerate(anchor_cells)}
    words = ("234", "243", "324", "333", "342", "423", "432")
    # Fixed source indices span both endpoints and the full 485-record range.
    record_indices = (0, 80, 160, 242, 322, 403, 484)
    witnesses = []
    total_terminal = 0
    for word, ri in zip(words, record_indices, strict=True):
        source_row, size, coefficient = records[ri]
        choices = [sorted(factors[f][int(word[f]) - 2]) for f in range(3)]
        found = None
        attempts = 0
        for factor_tails in product(*choices):
            attempts += 1
            row = bytes(sorted(source_row + b"".join(factor_tails)))
            s1 = signature(row, positions)
            ps1 = available(s1, pivots)
            for p1 in ps1:
                if any(available(child_signature(s1, pivots[p1], tail1, positions), pivots)
                       for tail1 in tails[p1]):
                    found = (factor_tails, row, s1, ps1, p1)
                    break
            if found is not None:
                break
        require(found is not None, (word, ri, attempts))
        factor_tails, row, s1, ps1, p1 = found
        m1 = len(ps1)
        pivotable = p2_uses = k21_children = 0
        charge_per_source_mass = 0
        m2_hist = Counter()
        for tail1 in tails[p1]:
            k19 = replace(row, anchors[p1], tail1)
            s2 = child_signature(s1, pivots[p1], tail1, positions)
            require(s2 == signature(k19, positions), (word, ri, p1))
            ps2 = available(s2, pivots)
            if not ps2:
                continue
            pivotable += 1
            m2 = len(ps2)
            m2_hist[m2] += 1
            require(U % (m1 * m2) == 0, (word, ri, m1, m2))
            unit = -U // (m1 * m2)
            for p2 in ps2:
                p2_uses += 1
                for tail2 in tails[p2]:
                    s3 = child_signature(s2, pivots[p2], tail2, positions)
                    require(not available(s3, pivots),
                            (word, ri, p1, p2, tail2.hex(), s3))
                    k21 = replace(k19, anchors[p2], tail2)
                    require(s3 == signature(k21, positions), (word, ri, p1, p2))
                    charge_per_source_mass += unit * charge(k21, cells, dual)
                    k21_children += 1
        require(pivotable > 0 and p2_uses > 0, (word, ri, pivotable, p2_uses))
        require(k21_children == 12 * p2_uses, (word, ri, k21_children, p2_uses))
        total_terminal += k21_children
        witnesses.append({
            "id": f"D17:{word}|R:2-2",
            "R8_record_index": ri,
            "factor_search_attempts": attempts,
            "factor_tails_hex": [x.hex() for x in factor_tails],
            "literal_K17_row_hex": row.hex(),
            "source_mass": size * coefficient,
            "m1": m1,
            "selected_p1": p1,
            "pivotable_K19_children": pivotable,
            "m2_hist": {str(k): v for k, v in sorted(m2_hist.items())},
            "selected_p2_uses": p2_uses,
            "terminal_K21_children": k21_children,
            "all_terminal_K21_children_nonpivotable": True,
            "charge_per_source_mass_scaled_U": str(charge_per_source_mass),
        })
    require([x["id"] for x in witnesses] == IDS, witnesses)
    return {
        "method": "Independent deterministic bounded search and literal two-response replay; not read from the producer sample TSV.",
        "record_indices": list(record_indices),
        "witnesses": witnesses,
        "covered_ids": 7,
        "total_nonzero_terminal_K21_children_replayed": total_terminal,
        "all_terminal_K21_children_nonpivotable": True,
        "all_literal_signature_updates_match": True,
        "all_exact_U_divisions_hold": True,
    }


def main():
    actual_pins = {str(path.relative_to(ROOT)): digest(path) for path in PINS}
    for path, expected in PINS.items():
        require(actual_pins[str(path.relative_to(ROOT))] == expected,
                (path, actual_pins[str(path.relative_to(ROOT))], expected))

    anchor_cells, records, pivots, factors = parse_structure()
    anchors, tails = parse_aux()
    cells, dual = parse_cycle()
    require(len(anchors) == len(tails) == len(pivots) == 78, "78 pivot families")
    require(all(len(x) == 12 for x in tails), "12 K2 tails per pivot")

    result = json.loads(RESULT.read_text())
    require(result["status"] == "PASS_COMPLETE_SEVEN_D17_R_2_2_K21_CHARGE", result["status"])
    require(result["records_consumed"] == result["records_declared"] == len(records) == 485, result)
    require([x["id"] for x in result["ids"]] == IDS, result["ids"])
    require(result["covered_ids"] == 7 and result["all_K21_children_irreducible"] is True, result)

    # These head counts are independently derived solely from the frozen
    # source dimensions: 485 * product of the three requested factor sectors.
    derived_heads = {
        f"D17:{word}|R:2-2": len(records) *
        factors[0][int(word[0]) - 2].__len__() *
        factors[1][int(word[1]) - 2].__len__() *
        factors[2][int(word[2]) - 2].__len__()
        for word in ("234", "243", "324", "333", "342", "423", "432")
    }

    total_fields = [
        "raw_K17_heads", "pivotable_K17_heads", "selected_p1_uses",
        "K19_child_occurrences", "pivotable_K19_child_occurrences",
        "selected_p2_uses", "K21_terminal_occurrences",
    ]
    totals = {field: 0 for field in total_fields}
    total_charge = 0
    by_id = {x["id"]: x for x in result["ids"]}
    for row in result["ids"]:
        require(row["raw_K17_heads"] == derived_heads[row["id"]], (row["id"], row["raw_K17_heads"], derived_heads[row["id"]]))
        require(row["K19_child_occurrences"] == 12 * row["selected_p1_uses"], row["id"])
        require(row["K21_terminal_occurrences"] == 12 * row["selected_p2_uses"], row["id"])
        require(row["full_occurrences"] == row["irreducible_occurrences"] == row["K21_terminal_occurrences"], row["id"])
        require(row["full_charge_scaled_U"] == row["irreducible_charge_scaled_U"], row["id"])
        for field in total_fields:
            totals[field] += row[field]
        total_charge += int(row["full_charge_scaled_U"])

    # Reflection symmetry gives equal structural counts for these pairs.  The
    # charges need not agree because the fixed 77-cycle functional is oriented.
    structural = total_fields
    for left, right in (("234", "432"), ("243", "423"), ("324", "342")):
        a, b = by_id[f"D17:{left}|R:2-2"], by_id[f"D17:{right}|R:2-2"]
        require(all(a[x] == b[x] for x in structural), (left, right))

    census = json.loads(CENSUS.read_text())["lineages"]["direct"]
    independent_census_equalities = {
        "raw_K17_heads": (totals["raw_K17_heads"], census["heads"]),
        "pivotable_K17_heads": (totals["pivotable_K17_heads"], census["pivotable_children"]),
        "selected_p1_uses": (totals["selected_p1_uses"], census["outgoing_pivot_uses"]),
        "K19_child_occurrences": (totals["K19_child_occurrences"], census["K19_K2_tail_operations"]),
    }
    require(all(a == b for a, b in independent_census_equalities.values()), independent_census_equalities)

    hist = result["m1_m2_occurrence_hist"]
    require(sum(hist.values()) == totals["pivotable_K19_child_occurrences"], hist)
    require(sum(int(k.split("_")[1]) * n for k, n in hist.items()) == totals["selected_p2_uses"], hist)
    require(sum(result["terminal_profile_cache"].values()) == totals["selected_p2_uses"], result["terminal_profile_cache"])
    require(result["literal_first_compression"] == {
        "lookups": totals["selected_p1_uses"],
        "misses": totals["selected_p1_uses"],
        "hits": 0,
        "peak_keys_per_R8_record": 551680,
        "proof": result["literal_first_compression"]["proof"],
    }, result["literal_first_compression"])
    require(total_charge == -196_205_097_632_820_756_480, total_charge)
    reduced = Fraction(total_charge, U)
    require(reduced == Fraction(-17_142_587_904, 35), reduced)

    sample_audit = audit_samples(anchor_cells, records, pivots, factors, anchors, tails, cells, dual)
    nonzero_witness_audit = independent_nonzero_witnesses(
        anchor_cells, records, pivots, factors, anchors, tails, cells, dual)
    source = SOURCE.read_text()
    source_guards = {
        "complete_literal_first_key": "struct LiteralFirstKey" in source and "row: Row" in source and "p1: u8" in source,
        "literal_second_pivot": "let ps2 = avail(s2, e);" in source,
        "exact_U_division": "assert_eq!(U21 % ((m1 * m2) as i128), 0);" in source,
        "correct_two_response_sign": "let unit_weight = -U21 / ((m1 * m2) as i128);" in source,
        "literal_terminal_full_equals_irreducible": "assert_eq!((full_n, irreducible_n), (12, 12));" in source and "assert_eq!(full_q, irreducible_q);" in source,
        "record_bounded_cache": "let mut first = HashMap::new();" in source and "let mut terminal = HashMap::new();" in source,
        "atomic_result": "rename(tmp, output).unwrap();" in source,
    }
    require(all(source_guards.values()), source_guards)

    audit = {
        "schema": "orbit0-independent-d17-r2-2-k21-referee-v1",
        "status": "PASS_INDEPENDENT_SEVEN_D17_R_2_2_K21_SOURCE_FORMULA_COUNT_SAMPLE_REFEREE",
        "scope": "Pinned source/formula/count and 257-sample literal replay; no second 485-record full charge run and no claim for other K21 IDs.",
        "coverage": {"expected_ids": IDS, "exact_set_and_order": True, "count": 7},
        "derived_head_counts_from_frozen_factor_dimensions": derived_heads,
        "independent_prior_census_equalities": {k: {"result": a, "prior_census": b, "equal": a == b} for k, (a, b) in independent_census_equalities.items()},
        "totals": {**totals, "full_and_irreducible_charge_scaled_U": str(total_charge), "reduced_charge": str(reduced)},
        "histogram_arithmetic": {"pivotable_K19_occurrences": True, "selected_p2_uses": True},
        "cache_arithmetic": {"terminal_hits_plus_misses_equals_selected_p2_uses": True, "literal_first_hits": 0},
        "source_guards": source_guards,
        "sample_audit": sample_audit,
        "independent_nonzero_literal_witness_audit": nonzero_witness_audit,
        "pinned_sha256": actual_pins,
    }
    logical = json.dumps(audit, sort_keys=True, separators=(",", ":")).encode()
    audit["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": audit["status"],
        "covered_ids": 7,
        "terminal_occurrences": totals["K21_terminal_occurrences"],
        "charge": str(reduced),
        "producer_sample_terminal_children": sample_audit["sample_terminal_K21_children_rebuilt"],
        "independent_nonzero_witness_terminal_children": nonzero_witness_audit["total_nonzero_terminal_K21_children_replayed"],
        "logical_sha256": audit["logical_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
