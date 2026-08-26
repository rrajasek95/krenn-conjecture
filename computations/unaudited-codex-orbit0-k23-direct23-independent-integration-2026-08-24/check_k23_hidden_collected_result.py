#!/usr/bin/env python3
"""Independent source/header/evidence/sample checker for a merged hidden K23 result."""
import argparse, hashlib, json, os
from pathlib import Path
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[2]
U=400_591_699_200;TOTAL=158_439_965;HEADER=80;RECORD=80
ID="D14:222|R:2-2-2-3"
SOURCE=ROOT/"computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin"
SOURCE_SHA="442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8"
SAMPLE_HEADER="input_index\tK18_row\tretained_K16_pair_witness\tweight_before_p3_scaled_U\tp2\tt2\tpair_uses\torbit\tstabilizer\tm2\tm3\tselected_p3_uses\tpivotable_K20_children\tselected_p4_uses\tterminal_K3_children\tliteral_charge_scaled_U"

def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def resolve(p):
 p=Path(p);return p if p.is_absolute() else ROOT/p

def main():
 ap=argparse.ArgumentParser();ap.add_argument("result");ap.add_argument("output");a=ap.parse_args()
 result_path=resolve(a.result);x=json.loads(result_path.read_text())
 assert x["status"]=="PASS_COMPLETE_HIDDEN_COLLECTED_K18_K23_SINGLETON_CHARGE" and x["degree"]==23 and int(x["scale_U"])==U
 assert x["strict_id"]==ID and x["input_interval"]==[0,TOTAL] and x["input_records"]==TOTAL
 assert x["full_equals_irreducible"] and x["full_occurrences"]==x["irreducible_occurrences"]==x["terminal_K3_tails"]==18_249_002_176
 assert x["selected_K18_p3_uses"]==399_275_484 and x["pivotable_K20_children"]==x["selected_K20_p4_uses"]==570_281_318
 assert x["terminal_K3_tails"]==32*x["selected_K20_p4_uses"] and x["full_charge_scaled_U"]==x["irreducible_charge_scaled_U"]
 assert Fraction(int(x["full_charge_scaled_U"]),U)==Fraction(x["exact_charge"])
 assert sum(x["m2_m3_m4_hist"].values())==x["selected_K20_p4_uses"]
 for key in x["m2_m3_m4_hist"]:
  m2,m3,m4=map(int,key.split("_"));assert m4==1 and U%(m2*m3*m4)==0
 assert len(x["shard_evidence"])==3 and [z["interval"] for z in x["shard_evidence"]]==[[0,52_813_321],[52_813_321,105_626_643],[105_626_643,TOTAL]]
 for z in x["shard_evidence"]:
  assert sha(resolve(z["result"]))==z["result_sha256"] and sha(resolve(z["samples"]))==z["samples_sha256"]
 assert SOURCE.stat().st_size==HEADER+RECORD*TOTAL and sha(SOURCE)==SOURCE_SHA
 with open(SOURCE,"rb") as f:h=f.read(HEADER)
 assert h[:8]==b"H18PIV2\0" and int.from_bytes(h[8:24],"little",signed=True)==U
 assert int.from_bytes(h[28:30],"little")==RECORD and int.from_bytes(h[48:56],"little")==TOTAL
 assert int.from_bytes(h[56:64],"little")==1 and int.from_bytes(h[64:80],"little",signed=True)==724_159_651_336_720_220_160
 sample_path=resolve(x["literal_sample_ledger"]);assert sha(sample_path)==x["literal_sample_ledger_sha256"]
 lines=sample_path.read_text().splitlines();assert lines[0]==SAMPLE_HEADER and len(lines)==772 and x["literal_sample_source_records"]==771
 seen=set();charge_sum=0
 with open(SOURCE,"rb") as f:
  for line in lines[1:]:
   c=line.split("\t");assert len(c)==16;idx=int(c[0]);assert idx not in seen;seen.add(idx)
   f.seek(HEADER+RECORD*idx);rec=f.read(RECORD);assert len(rec)==RECORD
   assert c[1]==rec[:24].hex() and c[2]==rec[40:64].hex()
   assert int(c[3])==int.from_bytes(rec[24:40],"little",signed=True)
   assert int(c[4])==rec[64] and int(c[5])==rec[65] and int(c[6])==int.from_bytes(rec[66:74],"little")
   orbit=int.from_bytes(rec[74:76],"little");stab=int.from_bytes(rec[76:78],"little")
   assert int(c[7])==orbit and int(c[8])==stab and orbit*stab==384
   assert rec[78]==1 and int(c[9])==rec[79]
   assert int(c[10])==int(c[11])>0 and int(c[12])==int(c[13]) and int(c[14])==32*int(c[13])
   charge_sum+=int(c[15])
 assert len(seen)==771
 assert not any(k in x for k in ("rows","K24","row_output","residual"))
 audit={"status":"PASS_INDEPENDENT_COMPLETE_K23_HIDDEN_COLLECTED_MERGE_CHECK","degree":23,"strict_id":ID,"result_sha256":sha(result_path),"source_sha256":SOURCE_SHA,"shard_evidence_rehashed":3,"literal_source_records_seek_replayed":771,"sample_charge_sum_scaled_U":str(charge_sum),"exact_charge":x["exact_charge"],"full_equals_irreducible":True,"no_rows_or_K24":True,"scope":"merged singleton scalar/source/sample audit only; no membership or conjecture verdict"}
 output=resolve(a.output);tmp=Path(str(output)+".tmp");tmp.write_text(json.dumps(audit,indent=2,sort_keys=True)+"\n");os.replace(tmp,output);print(json.dumps(audit,indent=2,sort_keys=True))
if __name__=="__main__":main()
