#!/usr/bin/env python3
"""Fail-closed gate/full validator for the pinned fast hidden-collected K24 singleton."""
from __future__ import annotations
import argparse, csv, hashlib, json, struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FAST=ROOT/"computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24"
INPUT=ROOT/"computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin"
SOURCE=FAST/"run_k24_charge_hidden_collected.rs"
BINARY=Path(__file__).with_name("run_k24_charge_hidden_collected_final")
TOTAL=158_439_965; U=400_591_699_200
PINS={
 SOURCE:"190ced047293e7ca67daefabe100a39be9d7d48f8ed8e1241c6b1171dcd5b056",
 BINARY:"9aa75453a54bba56cf28e8e763037f5202bbc8f943b96bbb1b4c8ceab7c93b61",
 INPUT:"442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8",
 FAST/"k24_hidden_base.rs":"ec68ac205d1737778d7fe1c23d1f2108fc2b274c8c54cb29716915ec8ba17c08",
 FAST/"k24_hidden_base_run_filtered_k17.rs":"5b0b5a467c6418b2bf042b47a89636c0135d93cdea656fd864fb5708f7682056",
}
HEADER=["input_index","K18_row","retained_K16_pair_witness","weight_before_p3_scaled_U","p2","t2","pair_uses","orbit","stabilizer","m2","m3","selected_p3_uses","pivotable_K20_children","selected_p4_uses","terminal_K4_children","literal_charge_scaled_U"]
KEYS={"status","degree","scale_U","input","input_interval","input_records","strict_id","input_weight_sum_scaled_U","input_weight_l1_scaled_U","selected_K18_p3_uses","pivotable_K20_children","selected_K20_p4_uses","terminal_K4_tails","full_occurrences","irreducible_occurrences","full_charge_scaled_U","irreducible_charge_scaled_U","sign_rule","m2_m3_m4_hist","cache","literal_sample_source_records","literal_sample_ledger","terminality","full_equals_irreducible","elapsed_seconds","projected_full_seconds","scope"}
def req(x,m):
 if not x: raise ValueError(m)
def sha(p):
 h=hashlib.sha256();
 with p.open("rb") as f:
  while b:=f.read(1<<20): h.update(b)
 return h.hexdigest()
def num(x,n):
 req(not isinstance(x,bool),n)
 try:return int(x)
 except:raise ValueError(n)
def validate(result_path,samples_path,mode):
 for p,h in PINS.items(): req(p.is_file() and sha(p)==h,f"pin mismatch {p}")
 r=json.loads(result_path.read_text()); req(set(r)==KEYS,"result schema keyset")
 full=mode=="full"; interval=[0,TOTAL] if full else [0,1_000_000]
 req(r["status"]==( "PASS_COMPLETE_HIDDEN_COLLECTED_K18_K24_SINGLETON_CHARGE" if full else "PASS_BOUNDED_HIDDEN_COLLECTED_K18_K24_GATE"),"status")
 req(num(r["degree"],"degree")==24 and num(r["scale_U"],"U")==U,"degree/U")
 req(r["input"]==str(INPUT.relative_to(ROOT)) and r["input_interval"]==interval and num(r["input_records"],"records")==interval[1],"input scope")
 req(r["strict_id"]=="D14:222|R:2-2-2-4","strict ID")
 if full:
  req(num(r["input_weight_sum_scaled_U"],"mass")==724_159_651_336_720_220_160,"mass pin")
  req(num(r["selected_K18_p3_uses"],"p3")==399_275_484,"p3 pin")
  req(num(r["pivotable_K20_children"],"K20")==num(r["selected_K20_p4_uses"],"p4")==570_281_318,"K20/p4 pin")
  req(num(r["terminal_K4_tails"],"tails")==34_216_879_080,"K4 tail pin")
 p4=num(r["selected_K20_p4_uses"],"p4"); tails=num(r["terminal_K4_tails"],"tails")
 req(tails==60*p4==num(r["full_occurrences"],"full")==num(r["irreducible_occurrences"],"irr"),"terminal identity")
 req(num(r["full_charge_scaled_U"],"charge")==num(r["irreducible_charge_scaled_U"],"irr charge"),"charge equality")
 req(r["full_equals_irreducible"] is True and r["terminality"]=="every K24 K4 child has active-anchor mass 0, hence no frozen pivot","terminality")
 req(r["sign_rule"]=="H18 weight w; K2 response gives -w/m3; terminal K4 response gives +w/(m3*m4)","sign")
 hist=r["m2_m3_m4_hist"]; req(isinstance(hist,dict) and hist,"hist")
 hs=0
 for k,v in hist.items():
  a=k.split("_"); req(len(a)==3,"hist key"); m2,m3,m4=map(int,a); req(m4==1 and m2>0 and m3>0 and U%(m2*m3*m4)==0,"hist denominator"); hs+=num(v,"hist value")
 req(hs==p4,"hist sum")
 c=r["cache"]; req(set(c)=={"K18_keys","K18_hits","K18_misses","K20_K4_keys","K20_K4_hits","K20_K4_misses"},"cache schema")
 req(num(c["K18_hits"],"hit")+num(c["K18_misses"],"miss")==num(r["selected_K18_p3_uses"],"p3"),"K18 cache")
 req(num(c["K20_K4_hits"],"hit")+num(c["K20_K4_misses"],"miss")==p4,"K20 cache")
 req(num(r["literal_sample_source_records"],"samples")==257 and Path(r["literal_sample_ledger"]).name==samples_path.name,"sample declaration")
 req(num(r["elapsed_seconds"],"elapsed")<600,"wall gate")
 req(r["scope"]=="strict singleton D14:222|R:2-2-2-4 scalar only; no rows/columns, K25, membership, or conjecture verdict","scope")
 with samples_path.open(newline="") as f: rows=list(csv.DictReader(f,delimiter="\t")); req(f.closed or True,"")
 req(rows and list(rows[0])==HEADER and len(rows)==257,"sample schema/count")
 expected=[j*(interval[1]-1)//256 for j in range(257)]; req([num(x["input_index"],"index") for x in rows]==expected,"distributed indices")
 with INPUT.open("rb") as f:
  for x,index in zip(rows,expected):
   f.seek(80+80*index); b=f.read(80); req(len(b)==80,"source seek")
   req(bytes.fromhex(x["K18_row"])==b[:24] and bytes.fromhex(x["retained_K16_pair_witness"])==b[40:64],"source-backed rows")
   req(num(x["weight_before_p3_scaled_U"],"weight")==int.from_bytes(b[24:40],"little",signed=True),"source weight")
   req(num(x["p2"],"p2")==b[64] and num(x["t2"],"t2")==b[65],"source p2/t2")
   uses=struct.unpack("<Q",b[66:74])[0]; orbit,stab=struct.unpack("<HH",b[74:78]); req(num(x["pair_uses"],"uses")==uses>0,"source uses"); req(num(x["orbit"],"orbit")==orbit and num(x["stabilizer"],"stab")==stab and orbit*stab==384,"orbit")
   req(b[78]==1 and num(x["m2"],"m2")==b[79]>0,"flag/m2")
   req(num(x["m3"],"m3")==num(x["selected_p3_uses"],"p3")>0,"m3/p3")
   req(num(x["pivotable_K20_children"],"K20")==num(x["selected_p4_uses"],"p4"),"sample K20/p4")
   req(num(x["terminal_K4_children"],"tails")==60*num(x["selected_p4_uses"],"p4"),"sample tails")
 return {"status":"PASS_HIDDEN_COLLECTED_FAST_"+mode.upper()+"_STRUCTURE","mode":mode,"result_sha256":sha(result_path),"samples_sha256":sha(samples_path),"source_sha256":PINS[SOURCE],"binary_sha256":PINS[BINARY],"input_sha256":PINS[INPUT],"witnesses":257}
def main():
 a=argparse.ArgumentParser();a.add_argument("--result",type=Path,required=True);a.add_argument("--samples",type=Path,required=True);a.add_argument("--mode",choices=["gate","full"],required=True);a.add_argument("--output",type=Path,required=True);z=a.parse_args();o=validate(z.result,z.samples,z.mode);z.output.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n");print(json.dumps(o,sort_keys=True))
if __name__=="__main__":main()
