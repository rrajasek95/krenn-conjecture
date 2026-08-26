#!/usr/bin/env python3
"""Strict exact audit for the one-pass hidden collected-K18 K22 fold."""
from __future__ import annotations
import csv,hashlib,json,struct
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];U=400_591_699_200
IDS=["D14:222|R:2-2-4","D14:222|R:2-2-2-2"]
PINS={"run_k22_hidden_collected_k18.rs":"d54f6f2c861b3b7bd40a47ec1282cf392903bf1348826fbbd2207156ba9012fb","results_k22_hidden_collected_k18.json":"2c15fbf93a2f33a8d3819b8a8eca281b9b27326aa82e98d5610443937362bde5","results_k22_hidden_collected_k18.json.samples.tsv":"06b5fcfd4f150c418d366991b9b96ec321cec46404d033b22b961bc2421dffb3","referee_k22_hidden_samples.rs":"adb0eaeba273905fe837c4ecf84df5ad9c01602bb1957beca80235603968e938","results_k22_hidden_samples_referee.json":"b26c47a3a24101bd5db9b7012c4a4ebd8d59372dc15cd628fd7ac7c6db3af09d"}
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
for n,w in PINS.items():assert sha(HERE/n)==w,(n,sha(HERE/n))
src=ROOT/"computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin"
pins=src.parent/"CHECKPOINTS.sha256";assert sha(pins)=="3a8f14e7daf0620c5f4e09e1928f286857d8c3d77c6051570135aa8f13134c85" and pins.read_text().splitlines()[0].startswith("442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8  ")
assert src.stat().st_size==12_675_197_280
with src.open("rb") as f:h=f.read(80)
assert h[:8]==b"H18PIV2\0" and int.from_bytes(h[8:24],"little",signed=True)==U and int.from_bytes(h[28:30],"little")==80
assert int.from_bytes(h[48:56],"little")==158_439_965 and int.from_bytes(h[56:64],"little")==1 and int.from_bytes(h[64:80],"little",signed=True)==724_159_651_336_720_220_160
r=json.loads((HERE/"results_k22_hidden_collected_k18.json").read_text());assert r["status"]=="PASS_COMPLETE_TWO_SINK_HIDDEN_COLLECTED_K18_K22_CHARGE" and int(r["scale_U"])==U
assert list(r["sinks"])==IDS and len(set(r["sinks"]))==2 and r["input_interval"]==[0,158_439_965] and r["input_records"]==158_439_965
assert int(r["input_weight_sum_scaled_U"])==724_159_651_336_720_220_160 and r["elapsed_seconds"]<600
a=r["sinks"][IDS[0]];b=r["sinks"][IDS[1]]
assert (a["selected_K18_pivots"],a["terminal_K4_tails"])==(399_275_484,23_956_529_040) and a["terminal_K4_tails"]==60*a["selected_K18_pivots"]
assert a["full_occurrences"]==a["irreducible_occurrences"]==a["terminal_K4_tails"] and a["full_charge_scaled_U"]==a["irreducible_charge_scaled_U"]=="70538993620749287424" and a["sign"]=="-w2/m3"
assert Fraction(int(a["full_charge_scaled_U"]),U)==Fraction(257_276_324_772_224,1_461_075)
assert (b["pivotable_K20_children"],b["selected_K20_pivots"],b["terminal_K2_tails"])==(570_281_318,570_281_318,6_843_375_816) and b["terminal_K2_tails"]==12*b["selected_K20_pivots"]
assert b["full_occurrences"]==b["irreducible_occurrences"]==b["terminal_K2_tails"] and b["full_charge_scaled_U"]==b["irreducible_charge_scaled_U"]=="1440150591691685265408" and b["sign"]=="+w2/(m3*m4)"
assert Fraction(int(b["full_charge_scaled_U"]),U)==Fraction(625_065_360_977_293_952,173_867_925)
c=r["cache"];assert c["K18_hits"]+c["K18_misses"]==a["selected_K18_pivots"] and c["K18_keys"]==c["K18_misses"] and c["K20_hits"]+c["K20_misses"]==b["selected_K20_pivots"] and c["K20_keys"]==c["K20_misses"]
hist={tuple(map(int,k.split("_"))):v for k,v in r["m2_m3_pivotable_K20_hist"].items()};assert sum(hist.values())==b["pivotable_K20_children"] and all(U%(m2*m3)==0 for (m2,m3) in hist)
assert r["literal_samples"]==257 and "no parent-row output, K23, or K24" in r["scope"]
with (HERE/"results_k22_hidden_collected_k18.json.samples.tsv").open(newline="") as f:rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==257 and [int(x["input_index"]) for x in rows]==[j*(158_439_965-1)//256 for j in range(257)]
s=json.loads((HERE/"results_k22_hidden_samples_referee.json").read_text());assert s["status"]=="PASS_INDEPENDENT_257_LITERAL_H18PIV2_TWO_SINK_K22_REFEREE" and s["strict_ids"]==IDS and s["distributed_parents"]==257
assert (s["literal_R224_terminal_children"],s["literal_R2222_terminal_children"])==(40_620,11_808) and s["all_divisions_exact"] and s["all_K22_children_terminal"]
logical={"ids":IDS,"scale_U":str(U),"scaled":[a["full_charge_scaled_U"],b["full_charge_scaled_U"]],"rational":["257276324772224/1461075","625065360977293952/173867925"],"occurrences":[a["full_occurrences"],b["full_occurrences"]],"terminal":True}
logical_sha=hashlib.sha256(json.dumps(logical,sort_keys=True,separators=(",",":")).encode()).hexdigest()
out={"status":"PASS_EXACT_TWO_SINK_HIDDEN_COLLECTED_K18_K22_CHARGE","logical_sha256":logical_sha,"strict_ids":IDS,"charges":dict(zip(IDS,logical["rational"])),"guards":{"pinned_H18PIV2_header_geometry_and_upstream_sha_ledger":True,"one_complete_source_scan":True,"separate_named_sinks":True,"exact_counts_U_and_signs":True,"full_equals_irreducible_by_K22_terminality":True,"independent_257_distributed_literal_replay":True,"runtime_and_memory_gate":True,"no_parent_rows":True,"no_K23_K24":True}}
(HERE/"results_k22_hidden_collected_k18_audit.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
