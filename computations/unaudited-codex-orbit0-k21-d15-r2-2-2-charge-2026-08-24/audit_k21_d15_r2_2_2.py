#!/usr/bin/env python3
"""Strict aggregate, provenance, and independent-sample audit for D15 R2-2-2."""
from __future__ import annotations
import csv, hashlib, json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
IDS=["D15:223|R:2-2-2","D15:232|R:2-2-2","D15:322|R:2-2-2"]
PINS={
 "run_k21_d15_r2_2_2_charge.rs":"e13ab8c548756015167f53e4bcc0f6584001a7681fb22545fd8cd0a1443d1517",
 "results_k21_d15_r2_2_2.json":"c6879b6605dc58e28418487b258018ef45c029aa4881f422c467ed73c3f6798e",
 "referee_k21_d15_r2_2_2_samples.rs":"b5fce248a10226e646e1fff06cf247b4fa7dcfd8005f7a019b9993cd3209c7d4",
 "results_k21_d15_r2_2_2_samples.json":"fa2ab9b8e31b0212c37dc053a30573f245a42d3f9025b8226c30bfbf24b5f5de",
 "k21_d15_r2_2_2_samples.tsv":"2007ba5efde2076de213bc1f3bbbfd958bdf8b74d63e4e0cada88cb021b5a9a8",
}
INPUT_PINS={
 ROOT/"computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs":"24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
 ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin":"55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
 ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin":"f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
 ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin":"8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
 ROOT/"computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin":"4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
}
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def exact_ids(x:list[str])->bool:return x==IDS and len(x)==len(set(x))
for name,want in PINS.items(): assert sha(HERE/name)==want,(name,sha(HERE/name))
for path,want in INPUT_PINS.items(): assert sha(path)==want,(path,sha(path))
r=json.loads((HERE/"results_k21_d15_r2_2_2.json").read_text())
assert r["status"]=="PASS_COMPLETE_GROUPED_D15_R_2_2_2_K21_CHARGE"
assert exact_ids(r["ids"]);assert not exact_ids(IDS[:-1]);assert not exact_ids(IDS+[IDS[0]]);assert not exact_ids(list(reversed(IDS)))
assert r["individual_id_charges"] is None and r["slice_interval"]==[0,485] and r["source_slices"]==485 and r["workers"]==8
assert (r["source_heads"],int(r["source_coefficient"]),int(r["l1_source_coefficient"]))==(6_704_640,322_486_272,3_085_516_800)
assert (r["p1_uses"],r["K17_children"],r["pivotable_K17_children"])==(55_934_080,671_208_960,451_445_760)
assert (r["p2_uses"],r["K19_children"])==(1_876_057_600,22_512_691_200)
assert r["K17_children"]==12*r["p1_uses"] and r["K19_children"]==12*r["p2_uses"]
assert r["K21_terminal_occurrences"]==r["full_occurrences"]==r["irreducible_occurrences"]==137_254_410_240==12*r["p3_uses"]
assert r["p3_uses"]==11_437_867_520 and r["pivotable_K19_children"]==6_774_666_240
assert r["full_charge_scaled_U"]==r["irreducible_charge_scaled_U"]=="-2089490736287288328192"
assert Fraction(int(r["full_charge_scaled_U"]),int(r["scale_U"]))==Fraction(-4_849_716_689_615_104,929_775)
hist={tuple(map(int,k.split("_"))):v for k,v in r["m1_m2_m3_occurrence_hist"].items()}
assert sum(hist.values())==r["pivotable_K19_children"] and sum(k[2]*v for k,v in hist.items())==r["p3_uses"]
assert all(int(r["scale_U"])%(a*b*c)==0 for (a,b,c) in hist)
tc=r["terminal_cache"];assert tc["hits"]+tc["misses"]==r["p3_uses"] and tc["peak_keys_per_slice"]<500_000
packets=list(r["representative_packet_diagnostics"].values())
for key in ["source_heads","source_coefficient","l1_source_coefficient","p1_uses","K17_children","pivotable_K17_children","p2_uses","K19_children","pivotable_K19_children","p3_uses","K21_children","charge_scaled_U"]:
 assert sum(int(p[key]) for p in packets)==int({"K21_children":r["K21_terminal_occurrences"],"charge_scaled_U":r["full_charge_scaled_U"]}.get(key,r.get(key)))
assert "only the grouped three-ID scalar" in r["packet_grouping_guard"] and "no K21 rows, K22" in r["scope"]
s=json.loads((HERE/"results_k21_d15_r2_2_2_samples.json").read_text())
assert s["status"]=="PASS_INDEPENDENT_257_DISTRIBUTED_NONZERO_LITERAL_D15_R_2_2_2_K21_REPLAY" and exact_ids(s["strict_grouped_ids"])
assert (s["source_slices"],s["first_slice"],s["last_slice"],s["nonzero_K19_to_K21_continuations"])==(257,0,484,257)
assert s["packet_witness_counts"]=={"322":86,"232":86,"223":85} and s["all_divisions_exact"] and s["all_K21_children_terminal"]
with (HERE/"k21_d15_r2_2_2_samples.tsv").open(newline="") as f: rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==257
for j,x in enumerate(rows):
 assert int(x["ordinal"])==j and int(x["source_slice"])==j*484//256 and int(x["packet"])==j%3
 assert x["lineage_witness"]==["322","232","223"][j%3]
 assert min(int(x[k]) for k in ["m1","m2","m3"])>0 and int(x["K21_children"])==12*int(x["m3"])
assert sum(int(x["K21_children"]) for x in rows)==s["literal_terminal_K21_children"]==4116
guard=json.loads((HERE/"hostile_l1_guard_evidence.json").read_text());assert guard["partial_result_published"] is False and guard["observed_literal_precollection"]["l1_source_coefficient"]=="3085516800"
logical={"ids":IDS,"scale_U":r["scale_U"],"scaled":r["full_charge_scaled_U"],"rational":"-4849716689615104/929775","occurrences":r["K21_terminal_occurrences"],"samples":257,"terminal":True}
logical_sha=hashlib.sha256(json.dumps(logical,sort_keys=True,separators=(",",":")).encode()).hexdigest()
out={"status":"PASS_STRICT_GROUPED_D15_R_2_2_2_K21_CHARGE_AND_INDEPENDENT_257_LITERAL_REFEREE","logical_sha256":logical_sha,"exact_charge":logical["rational"],"guards":{"pinned_source_and_results":True,"exact_ordered_singleton_free_group_scope":True,"missing_duplicate_reordered_ids_rejected":True,"packet_outputs_not_misrepresented_as_individual_scalars":True,"literal_precollection_l1_distinguished_from_collected_l1":True,"recurrence_counts_and_exact_U_divisions":True,"full_equals_irreducible_by_terminal_K21":True,"independent_257_distributed_nonzero_literal_continuations":True,"no_K22":True}}
(HERE/"results_k21_d15_r2_2_2_audit.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
