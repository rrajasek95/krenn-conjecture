#!/usr/bin/env python3
"""Independent exact validation for K23 D14 source-three shard [243,485)."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "results_shard1.json"
SAMPLES = HERE / "results_shard1.json.samples.tsv"
REFEREE = HERE / "results_shard1_literal_referee.json"
U = 400_591_699_200
START, END = 243, 485
IDS = ["D14:222|R:3-2-4", "D14:222|R:3-3-3", "D14:222|R:4-2-3"]
DEGREES = [(3, 2, 4, 60), (3, 3, 3, 32), (4, 2, 3, 32)]
PINS = {
    RESULT: "eafce67dce352d559b4b6e364e105633a07e6c168f771a3a9a10308c75026c52",
    SAMPLES: "d752947b49655fe17a985cca394a7cc490ede14c4194339c6e8d62a725041a28",
    REFEREE: "192bfb3b6ad2a03711cce29b9d4296a120af8f27d79b17b3f1a775e0edd79f31",
    HERE / "run_k23_d14_source_three.rs": "32a23e26bced387be2ce348b1bb41de126f5f17e2f5ee2adeccc9320d69f116b",
    HERE / "run_k23_d14_source_three": "5ecb715d1861280495d92a9d970b4c50db6cc32ba78577ecbc97a5837b66373f",
    HERE / "referee_k23_d14_source_three_literals.rs": "64bc0cd19c859f57a9fb01c6a8a66a54a4d798de6dc524e1459b5015395bd6d4",
    HERE / "referee_k23_d14_source_three_literals": "8ea90ad3caa491833ad214a2df2d5a17367addc6b78353be25b200e84eb199b6",
}

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""): h.update(block)
    return h.hexdigest()

def load(path): return json.loads(Path(path).read_text())
def weighted(hist): return sum(int(key) * value for key, value in hist.items())

def main():
    for path, digest in PINS.items(): assert sha(path) == digest, path
    pins = load(HERE / "input_pins.json")
    for entry in pins.values(): assert sha(ROOT / entry["path"]) == entry["sha256"]
    raw = (ROOT / pins["physical_source"]["path"]).read_bytes()
    assert raw[:11] == b"K16DIRECT1\0"
    nt, nr, np, na = [int.from_bytes(raw[a:b], "little") for a, b in ((11,15),(15,19),(19,23),(23,27))]
    assert (nt, nr, np, na) == (384, 485, 78, 12)
    offset = 27 + 12 + nt * 264
    masses = []
    for index in range(nr):
        rec = raw[offset + 24 * index:offset + 24 * (index + 1)]
        masses.append(int.from_bytes(rec[12:16], "little") * int.from_bytes(rec[16:24], "little", signed=True))

    result = load(RESULT)
    assert result["status"] == "PASS_BOUNDED_D14_222_K23_SOURCE_THREE_EVALUATOR"
    assert result["covered_lineage_ids"] == IDS and int(result["scale_U"]) == U
    assert result["R8_record_interval"] == [START, END] and not result["distributed_record_mode"]
    assert (result["R8_records_consumed"], result["R8_records_declared"], result["source_heads"]) == (242, 485, 418_176)
    assert int(result["source_mass_sum"]) == sum(masses[START:END]) * 1728
    assert int(result["source_mass_l1"]) == sum(abs(x) for x in masses[START:END]) * 1728
    assert result["all_realized_cached_K23_responses_terminal"] is True
    guard = result["terminal_cache_resource_guard"]
    assert guard["hard_cap_keys_per_worker"] == 3_000_000 and guard["peak_keys_per_worker"] <= 3_000_000
    assert result["workers"] == 8 and result["elapsed_seconds"] < 600
    assert result["sign_rule"].startswith("direct D14 coefficient=-M; three normalized response flips")
    structural = {}
    for lineage, (d1, d2, d3, terminal_tails) in zip(IDS, DEGREES, strict=True):
        sink = result["sinks"][lineage]
        assert (sink["first_response_degree"],sink["second_response_degree"],sink["terminal_response_degree"]) == (d1,d2,d3)
        assert sink["first_children"] == {2:12,3:32,4:60}[d1] * sink["selected_p1_uses"]
        assert sink["second_children"] == {2:12,3:32,4:60}[d2] * sink["selected_p2_uses"]
        assert sink["K23_terminal_occurrences"] == terminal_tails * sink["selected_p3_uses"]
        assert sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["K23_terminal_occurrences"]
        assert sink["full_charge_scaled_U"] == sink["irreducible_charge_scaled_U"]
        h1,h2,h3,hp = [sink[x] for x in ("first_denominator_hist","second_denominator_hist","third_denominator_hist","product_denominator_hist")]
        assert sum(h1.values()) == result["source_heads"] and weighted(h1) == sink["selected_p1_uses"]
        assert sum(h2.values()) == sink["pivotable_first_children"] and weighted(h2) == sink["selected_p2_uses"]
        assert sum(h3.values()) == sink["pivotable_second_children"] and weighted(h3) == sink["selected_p3_uses"]
        assert sum(hp.values()) == sink["pivotable_second_children"]
        assert all(int(key) > 0 and U % int(key) == 0 and value > 0 for key,value in hp.items())
        assert sink["plan_cache"]["first_hits"] + sink["plan_cache"]["first_misses"] == sink["selected_p1_uses"]
        assert sink["plan_cache"]["second_hits"] + sink["plan_cache"]["second_misses"] == sink["selected_p2_uses"]
        assert sink["literal_preterminal_cache"]["hits"] + sink["literal_preterminal_cache"]["misses"] == sink["pivotable_second_children"]
        assert sink["terminal_profile_cache"]["hard_cap_keys_per_worker"] == 3_000_000
        assert sink["literal_samples"] == 129
        structural[lineage] = {"selected_p1_uses":sink["selected_p1_uses"],"selected_p2_uses":sink["selected_p2_uses"],"selected_p3_uses":sink["selected_p3_uses"],"terminal_K23_occurrences":sink["K23_terminal_occurrences"],"full_charge_scaled_U":sink["full_charge_scaled_U"],"denominator_product_bins":len(hp)}

    lines = SAMPLES.read_text().splitlines(); assert len(lines) == 388
    counts = {x:0 for x in IDS}; bins = {x:[] for x in IDS}
    for line in lines[1:]:
        c=line.split("\t"); assert len(c)==28 and c[0] in counts
        counts[c[0]]+=1; bins[c[0]].append(int(c[1])); head=int(c[2]); r8=int(c[3])
        assert int(c[1]) == head*257//(485*1728) and r8==head//1728 and START<=r8<END
        assert U % (int(c[20])*int(c[21])*int(c[22])) == 0
    assert list(counts.values()) == [129,129,129]
    assert all(values == list(range(128,257)) for values in bins.values())
    referee=load(REFEREE)
    assert referee["status"] == "PASS_INDEPENDENT_K23_D14_SOURCE_THREE_LITERAL_REFEREE"
    assert referee["samples_per_sink"] == [129,129,129]
    assert referee["literal_terminal_children_checked"] == 83_750_464 and referee["witness_terminal_children_checked"] == 15_996
    for field in ("source_heads_reconstructed_from_frozen_R8","all_literal_path_counts_and_charges_equal","all_U_divisions_exact","all_terminal_K23_children_nonpivotable","all_abstract_literal_cycle_keys_equal"): assert referee[field] is True

    payload={"status":"PASS_INDEPENDENT_K23_D14_SOURCE_THREE_SHARD1_VALIDATION","degree":23,"strict_ids":IDS,"interval":[START,END],"records":242,"source_heads":result["source_heads"],"input_pins":{k:{"path":v["path"],"sha256":v["sha256"]} for k,v in pins.items()},"producer":{"source_sha256":sha(HERE/"run_k23_d14_source_three.rs"),"binary_sha256":sha(HERE/"run_k23_d14_source_three")},"result":{"sha256":sha(RESULT),"samples_sha256":sha(SAMPLES),"elapsed_seconds":result["elapsed_seconds"],"structural":structural},"guards":{"source_mass_independently_reparsed":True,"count_and_tail_ratios_exact":True,"denominator_histogram_sums_and_weighted_sums_exact":True,"all_product_denominators_divide_U":True,"three_flip_sign_rule_exact":True,"terminal_cache_caps_respected":True,"full_equals_irreducible":True},"literal_referee":{"source_sha256":sha(HERE/"referee_k23_d14_source_three_literals.rs"),"binary_sha256":sha(HERE/"referee_k23_d14_source_three_literals"),"result_sha256":sha(REFEREE),"source_head_replays":387,"full_literal_terminal_children_checked":referee["literal_terminal_children_checked"],"witness_terminal_children_checked":referee["witness_terminal_children_checked"],"bins_per_sink":[129,129,129]},"scope":"independent shard1 validation only; no scalar rerun, aggregate inference, K24, membership, or conjecture claim"}
    logical=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest();payload["logical_sha256"]=logical
    out=HERE/"results_shard1_validation.json";tmp=Path(str(out)+".tmp");tmp.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n");tmp.replace(out)
    print(json.dumps({"status":payload["status"],"logical_sha256":logical},indent=2))

if __name__ == "__main__": main()
