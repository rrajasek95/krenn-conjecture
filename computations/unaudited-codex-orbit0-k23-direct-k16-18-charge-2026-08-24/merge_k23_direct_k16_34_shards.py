#!/usr/bin/env python3
"""Fail-closed exact merge for the bounded grouped direct-K16 R:3-4 K23 shards."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import json

N = 24_097_095
U = 400_591_699_200
SUM_FIELDS = (
    "source_rows", "signed_source_coefficient", "l1_source_coefficient",
    "pivotable_K16_rows", "p1_uses", "first_children",
    "pivotable_intermediate_children", "p2_uses", "K23_terminal_occurrences",
    "full_occurrences", "irreducible_occurrences", "full_charge_scaled_U",
    "irreducible_charge_scaled_U",
)


def atomic(path, text):
    path = Path(path)
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("shards", nargs="+")
    args = parser.parse_args()
    docs = []
    for name in args.shards:
        path = Path(name)
        doc = json.loads(path.read_text())
        assert doc["status"] == "PASS_BOUNDED_GROUPED_SIX_D16_K23_TWO_RESPONSE_GATE"
        assert (
            doc["group_id"], doc["degree"], int(doc["scale_U"]),
            doc["records_declared"], doc["distributed_prefix"],
        ) == ("source_D16_R3_4", 23, U, N, False)
        docs.append((path, doc))
    docs.sort(key=lambda item: item[1]["record_interval"])
    cursor = 0
    for _, doc in docs:
        lo, hi = doc["record_interval"]
        assert lo == cursor and hi > lo
        cursor = hi
    assert cursor == N
    ids = docs[0][1]["ids"]
    assert len(ids) == len(set(ids)) == 6
    assert all(doc["ids"] == ids for _, doc in docs)
    sums = {key: sum(int(doc[key]) for _, doc in docs) for key in SUM_FIELDS}
    assert (
        sums["source_rows"], sums["signed_source_coefficient"],
        sums["l1_source_coefficient"],
    ) == (N, 1_464_625_152, 13_978_655_136)
    assert (sums["pivotable_K16_rows"], sums["p1_uses"]) == (24_003_767, 129_939_187)
    assert sums["first_children"] == 32 * sums["p1_uses"]
    assert (
        sums["pivotable_intermediate_children"], sums["p2_uses"],
    ) == (1_295_008_880, 2_041_782_688)
    assert sums["K23_terminal_occurrences"] == 60 * sums["p2_uses"]
    assert sums["K23_terminal_occurrences"] == sums["full_occurrences"] == sums["irreducible_occurrences"]
    assert sums["full_charge_scaled_U"] == sums["irreducible_charge_scaled_U"]
    hist = Counter()
    for _, doc in docs:
        hist.update({key: int(value) for key, value in doc["m1_m2_hist"].items()})
    assert sum(hist.values()) == sums["pivotable_intermediate_children"]
    assert sum(int(key.rsplit("_", 1)[1]) * value for key, value in hist.items()) == sums["p2_uses"]
    samples = {}
    header = None
    for _, doc in docs:
        lines = Path(doc["sample_ledger"]).read_text().splitlines()
        if header is None:
            header = lines[0]
        assert lines[0] == header
        for line in lines[1:]:
            fields = line.split("\t")
            ordinal = int(fields[0])
            index = int(fields[1])
            assert 0 <= ordinal <= 256 and int(fields[12]) != 0
            if ordinal not in samples or index < int(samples[ordinal].split("\t")[1]):
                samples[ordinal] = line
    assert sorted(samples) == list(range(257))
    sample_path = Path(str(args.output) + ".samples.tsv")
    atomic(sample_path, header + "\n" + "\n".join(samples[j] for j in range(257)) + "\n")
    charge = Fraction(sums["full_charge_scaled_U"], U)
    result = {
        "status": "PASS_COMPLETE_MERGED_GROUPED_SIX_D16_R_3_4_K23",
        "group_id": "source_D16_R3_4", "degree": 23, "scale_U": str(U),
        "ids": ids, "covered_ids": 6, "individual_id_charges": None,
        "record_interval": [0, N], "records_declared": N,
        "shard_count": len(docs),
        "shards": [
            {"path": str(path), "record_interval": doc["record_interval"],
             "elapsed_seconds": doc["elapsed_seconds"]}
            for path, doc in docs
        ],
        **{key: str(value) if "coefficient" in key or "charge" in key else value
           for key, value in sums.items()},
        "m1_m2_hist": dict(sorted(hist.items())),
        "terminal_cache": {
            "hits": sum(int(doc["terminal_cache"]["hits"]) for _, doc in docs),
            "misses": sum(int(doc["terminal_cache"]["misses"]) for _, doc in docs),
            "peak_keys_per_piece": max(int(doc["terminal_cache"]["peak_keys_per_piece"]) for _, doc in docs),
        },
        "full": {"numerator": charge.numerator, "denominator": charge.denominator, "text": str(charge)},
        "irreducible": {"numerator": charge.numerator, "denominator": charge.denominator, "text": str(charge)},
        "literal_samples": 257, "sample_ledger": str(sample_path),
        "packet_grouping_guard": "checkpoint retains collected canonical rows and coefficients but not packet labels; only the grouped six-ID scalar is source-faithful",
        "sign_rule": "stored v is the direct coefficient in P; two normalized response flips give +v/(m1*m2)",
        "terminality": "literal terminal K4 response asserts every child has no available frozen pivot and full equals irreducible",
        "scope": "strict complete grouped six-ID K23 R3-4 sink only; exact no-gap shard merge, no individual reconstruction or membership claim",
    }
    atomic(args.output, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "shards": len(docs), "charge": str(charge), "samples": 257}, sort_keys=True))


if __name__ == "__main__":
    main()
