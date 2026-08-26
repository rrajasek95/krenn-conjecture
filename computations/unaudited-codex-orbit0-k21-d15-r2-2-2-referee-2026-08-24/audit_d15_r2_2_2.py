#!/usr/bin/env python3
"""Independent bounded referee for grouped D15 R2-2-2 at K21."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import csv
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCER = ROOT / "computations/unaudited-codex-orbit0-k21-d15-r2-2-2-charge-2026-08-24"
SOURCE = PRODUCER / "run_k21_d15_r2_2_2_charge.rs"
RESULT = PRODUCER / "results_k21_d15_r2_2_2.json"
PSOURCE = PRODUCER / "referee_k21_d15_r2_2_2_samples.rs"
PRESULT = PRODUCER / "results_k21_d15_r2_2_2_samples.json"
PSAMPLES = PRODUCER / "k21_d15_r2_2_2_samples.tsv"
STRUCTURE = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin"
AUX = STRUCTURE.with_name("filtered_k17_aux.bin")
CYCLE = STRUCTURE.with_name("filtered_k17_cycle_aux.bin")
PROVIDER = ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs"
OURS = HERE / "results_d15_r2_2_2_literal_referee.json"
OUR_SAMPLES = HERE / "samples_d15_r2_2_2_literal.tsv"
OUT = HERE / "results_d15_r2_2_2_independent_audit.json"
U = 400_591_699_200
IDS = ["D15:223|R:2-2-2", "D15:232|R:2-2-2", "D15:322|R:2-2-2"]
PINS = {
    SOURCE: "e13ab8c548756015167f53e4bcc0f6584001a7681fb22545fd8cd0a1443d1517",
    RESULT: "c6879b6605dc58e28418487b258018ef45c029aa4881f422c467ed73c3f6798e",
    PSOURCE: "b5fce248a10226e646e1fff06cf247b4fa7dcfd8005f7a019b9993cd3209c7d4",
    PRESULT: "fa2ab9b8e31b0212c37dc053a30573f245a42d3f9025b8226c30bfbf24b5f5de",
    PSAMPLES: "2007ba5efde2076de213bc1f3bbbfd958bdf8b74d63e4e0cada88cb021b5a9a8",
    STRUCTURE: "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    AUX: "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    CYCLE: "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    PROVIDER: "24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
}


def require(ok, detail):
    if not ok:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def records():
    b = STRUCTURE.read_bytes()
    require(b[:11] == b"K16DIRECT1\0", b[:11])
    q = 11
    nt, nr, np, na = struct.unpack_from("<IIII", b, q); q += 16
    require((nt, nr, np, na) == (384, 485, 78, 12), (nt, nr, np, na))
    q += 12 + nt * (252 + 12)
    out = []
    for _ in range(nr):
        row = bytes(b[q:q+12]); size, coefficient = struct.unpack_from("<Iq", b, q+12)
        q += 24; out.append((row, size, coefficient))
    return out


def result_guards(r, source_records):
    require(r["status"] == "PASS_COMPLETE_GROUPED_D15_R_2_2_2_K21_CHARGE", r)
    require(r["ids"] == IDS and r["individual_id_charges"] is None, r)
    require(r["slice_interval"] == [0, 485] and r["source_slices"] == 485 and r["workers"] == 8, r)
    require(int(r["scale_U"]) == U, r)
    signed = -13_824 * sum(size * coefficient for _, size, coefficient in source_records)
    l1 = 13_824 * sum(abs(size * coefficient) for _, size, coefficient in source_records)
    require((r["source_heads"], int(r["source_coefficient"]), int(r["l1_source_coefficient"])) ==
            (6_704_640, signed, l1) == (6_704_640, 322_486_272, 3_085_516_800),
            (signed, l1, r))
    require((r["p1_uses"], r["K17_children"], r["pivotable_K17_children"],
             r["p2_uses"], r["K19_children"]) ==
            (55_934_080, 671_208_960, 451_445_760, 1_876_057_600, 22_512_691_200), r)
    require(r["K17_children"] == 12*r["p1_uses"], r)
    require(r["K19_children"] == 12*r["p2_uses"], r)
    require(r["K21_terminal_occurrences"] == 12*r["p3_uses"], r)
    require(r["K21_terminal_occurrences"] == r["full_occurrences"] ==
            r["irreducible_occurrences"] == 137_254_410_240, r)
    scaled = int(r["full_charge_scaled_U"])
    require(scaled == int(r["irreducible_charge_scaled_U"]) == -2_089_490_736_287_288_328_192, scaled)
    require(Fraction(scaled, U) == Fraction(-4_849_716_689_615_104, 929_775), scaled)
    hist = {}
    for key, value in r["m1_m2_m3_occurrence_hist"].items():
        triple = tuple(map(int, key.split("_")))
        require(len(triple) == 3 and U % (triple[0]*triple[1]*triple[2]) == 0, key)
        hist[triple] = int(value)
    require(sum(hist.values()) == r["pivotable_K19_children"], r)
    require(sum(m3*n for (_, _, m3), n in hist.items()) == r["p3_uses"], r)
    cache = r["terminal_cache"]
    require(cache["hits"] + cache["misses"] == r["p3_uses"] and cache["peak_keys_per_slice"] > 0, cache)
    diagnostics = list(r["representative_packet_diagnostics"].values())
    for field, total in (("source_heads", r["source_heads"]),
                         ("source_coefficient", int(r["source_coefficient"])),
                         ("l1_source_coefficient", int(r["l1_source_coefficient"])),
                         ("p1_uses", r["p1_uses"]), ("K17_children", r["K17_children"]),
                         ("pivotable_K17_children", r["pivotable_K17_children"]),
                         ("p2_uses", r["p2_uses"]), ("K19_children", r["K19_children"]),
                         ("pivotable_K19_children", r["pivotable_K19_children"]),
                         ("p3_uses", r["p3_uses"]), ("K21_children", r["K21_terminal_occurrences"]),
                         ("charge_scaled_U", scaled)):
        require(sum(int(x[field]) for x in diagnostics) == total, (field, total, diagnostics))
    return scaled


def prefix_guards():
    checked = []
    for n in (1, 8, 32):
        path = PRODUCER / f"results_prefix{n}.json"
        x = json.loads(path.read_text())
        require(x["status"] == "PASS_BOUNDED_D15_R_2_2_2_SLICE_GATE", x)
        require(x["slice_interval"] == [0, n] and x["source_slices"] == n, x)
        require(x["source_heads"] == n*13_824, x)
        require(x["K17_children"] == 12*x["p1_uses"] and
                x["K19_children"] == 12*x["p2_uses"] and
                x["K21_terminal_occurrences"] == 12*x["p3_uses"], x)
        require(x["full_occurrences"] == x["irreducible_occurrences"] and
                x["full_charge_scaled_U"] == x["irreducible_charge_scaled_U"], x)
        require(x["terminal_cache"]["hits"] + x["terminal_cache"]["misses"] == x["p3_uses"], x)
        checked.append({"interval": [0, n], "sha256": digest(path)})
    return checked


def producer_sample_guards():
    p = json.loads(PRESULT.read_text())
    require(p["status"] == "PASS_INDEPENDENT_257_DISTRIBUTED_NONZERO_LITERAL_D15_R_2_2_2_K21_REPLAY", p)
    require(p["strict_grouped_ids"] == IDS and p["source_slices"] == 257 and
            (p["first_slice"], p["last_slice"]) == (0, 484), p)
    require(p["packet_witness_counts"] == {"322": 86, "232": 86, "223": 85}, p)
    with PSAMPLES.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    require(len(rows) == 257, len(rows))
    children = 0
    for j, row in enumerate(rows):
        require(int(row["ordinal"]) == j and int(row["source_slice"]) == j*484//256, row)
        packet = j % 3
        require(int(row["packet"]) == packet and row["lineage_witness"] == ("322", "232", "223")[packet], row)
        m1, m2, m3 = map(int, (row["m1"], row["m2"], row["m3"]))
        require(U % (m1*m2*m3) == 0, row)
        require(int(row["K21_children"]) == 12*m3, row)
        children += int(row["K21_children"])
    require(children == p["literal_terminal_K21_children"] == 4_116, children)
    return children


def own_sample_guards():
    p = json.loads(OURS.read_text())
    require(p["status"] == "PASS_INDEPENDENT_257_NONZERO_LITERAL_D15_R2_2_2_REFEREE", p)
    require(p["samples"] == p["sample_bins"] == 257 and p["source_grid_heads"] == 6_704_640, p)
    require(p["literal_terminal_children"] == 3_084 and p["packet_sample_counts"] ==
            {"322": 86, "232": 86, "223": 85}, p)
    require(all(p[k] is True for k in ("all_terminal_children_irreducible",
            "all_denominator_products_divide_U", "all_sample_contributions_nonzero")), p)
    with OUR_SAMPLES.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    require(len(rows) == 257 and {int(x["sample_bin"]) for x in rows} == set(range(257)), len(rows))
    for x in rows:
        index = int(x["head_index"]); bin_id = int(x["sample_bin"])
        require(bin_id == index*257//6_704_640, x)
        require(int(x["terminal_q"]) != 0 and int(x["nonzero_contribution_scaled_U"]) != 0, x)
        require(U % (int(x["m1"])*int(x["m2"])*int(x["m3"])) == 0, x)
    return p["literal_terminal_children"]


def main():
    for path, expected in PINS.items():
        require(digest(path) == expected, (path, digest(path), expected))
    source_records = records()
    result = json.loads(RESULT.read_text())
    scaled = result_guards(result, source_records)
    prefixes = prefix_guards()
    producer_children = producer_sample_guards()
    own_children = own_sample_guards()
    source = SOURCE.read_text()
    for token in ("assert_eq!(z.k17,12*z.p1)", "assert_eq!(z.k19,12*z.p2)",
                  "assert_eq!(z.k21,12*z.p3)", "assert_eq!(z.hits+z.misses,z.p3)",
                  "assert_eq!(U21%((m1*m2*m3)as i128),0)",
                  "assert_eq!((z.2,z.3),(12,12))", "assert_eq!(z.0,z.1)"):
        require(token in source, token)
    report = {
        "status": "PASS_INDEPENDENT_D15_R2_2_2_SOURCE_COUNT_SAMPLE_TERMINAL_REFEREE",
        "strict_grouped_ids": IDS,
        "individual_id_charges": None,
        "scale_U": str(U),
        "charge_scaled_U": str(scaled),
        "charge": "-4849716689615104/929775",
        "counts": {
            "source_slices": 485, "source_heads": result["source_heads"],
            "p1_uses": result["p1_uses"], "K17_children": result["K17_children"],
            "pivotable_K17": result["pivotable_K17_children"], "p2_uses": result["p2_uses"],
            "K19_children": result["K19_children"], "pivotable_K19": result["pivotable_K19_children"],
            "p3_uses": result["p3_uses"], "K21_terminal": result["K21_terminal_occurrences"],
        },
        "guards": {
            "atomic_full_interval_0_485": True, "prefix_intervals": prefixes,
            "source_mass_rederived": True, "packet_diagnostics_sum_to_group": True,
            "three_response_sign": "direct -positive -> terminal +positive/(m1*m2*m3)",
            "all_U_products_exact": True, "full_equals_irreducible": True,
            "terminal_signature_mass_3_below_pivot_mass_4": True,
            "producer_distributed_literal_children": producer_children,
            "independent_distributed_nonzero_literal_children": own_children,
            "no_full_fold_rerun": True, "no_K22": True,
        },
        "scope": "Exact grouped three-ID scalar only; H-orbit masses do not support individual packet charges.",
        "pinned": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    }
    logical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
