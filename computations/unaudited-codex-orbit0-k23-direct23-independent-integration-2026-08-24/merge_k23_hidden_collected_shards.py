#!/usr/bin/env python3
"""Strict no-gap merger for the held K23 hidden-collected H18PIV2 singleton."""
import argparse, hashlib, json, os
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
U=400_591_699_200; TOTAL=158_439_965
ID="D14:222|R:2-2-2-3"
INPUT="computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin"
INPUT_SHA="442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8"
INTERVALS=[[0,52_813_321],[52_813_321,105_626_643],[105_626_643,TOTAL]]
SAMPLE_HEADER="input_index\tK18_row\tretained_K16_pair_witness\tweight_before_p3_scaled_U\tp2\tt2\tpair_uses\torbit\tstabilizer\tm2\tm3\tselected_p3_uses\tpivotable_K20_children\tselected_p4_uses\tterminal_K3_children\tliteral_charge_scaled_U"

def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def resolve(p):
 p=Path(p); return p if p.is_absolute() else ROOT/p
def exact_text(n):return str(Fraction(n,U))

def validate_one(x,interval):
 assert x["status"]=="PASS_BOUNDED_HIDDEN_COLLECTED_K18_K23_GATE"
 assert x["degree"]==23 and int(x["scale_U"])==U and x["input"]==INPUT
 assert x["input_interval"]==interval and x["input_records"]==interval[1]-interval[0]
 assert x["strict_id"]==ID and x["full_equals_irreducible"] is True
 assert x["pivotable_K20_children"]==x["selected_K20_p4_uses"]
 assert x["terminal_K3_tails"]==32*x["selected_K20_p4_uses"]
 assert x["full_occurrences"]==x["irreducible_occurrences"]==x["terminal_K3_tails"]
 assert x["full_charge_scaled_U"]==x["irreducible_charge_scaled_U"]
 assert sum(x["m2_m3_m4_hist"].values())==x["selected_K20_p4_uses"]
 for key in x["m2_m3_m4_hist"]:
  m2,m3,m4=map(int,key.split("_")); assert m4==1 and U%(m2*m3*m4)==0
 c=x["cache"]
 assert c["K18_keys"]==c["K18_misses"] and c["K18_hits"]+c["K18_misses"]==x["selected_K18_p3_uses"]
 assert c["K20_K3_keys"]==c["K20_K3_misses"] and c["K20_K3_hits"]+c["K20_K3_misses"]==x["selected_K20_p4_uses"]

def validate_samples(x,interval):
 assert x["literal_sample_source_records"]==257 and isinstance(x["literal_sample_ledger"],str)
 path=resolve(x["literal_sample_ledger"]); lines=path.read_text().splitlines();assert lines[0]==SAMPLE_HEADER and len(lines)==258
 expected=[interval[0]+j*(interval[1]-interval[0]-1)//256 for j in range(257)]
 indices=[]
 for line in lines[1:]:
  c=line.split("\t");assert len(c)==16;idx=int(c[0]);indices.append(idx)
  assert interval[0]<=idx<interval[1] and int(c[11])==int(c[10])
  assert int(c[12])==int(c[13]) and int(c[14])==32*int(c[13])
 assert indices==expected
 return path,lines[1:]

def merge(shard_paths,output):
 assert len(shard_paths)==3
 shards=[]; evidence=[]; combined=[]
 for supplied,interval in zip(shard_paths,INTERVALS):
  path=resolve(supplied);x=json.loads(path.read_text());validate_one(x,interval);sample_path,lines=validate_samples(x,interval)
  shards.append(x);combined.extend(lines);evidence.append({"result":str(path.relative_to(ROOT)),"result_sha256":sha(path),"samples":str(sample_path.relative_to(ROOT)),"samples_sha256":sha(sample_path),"interval":interval})
 assert len(combined)==771 and len({int(x.split("\t",1)[0]) for x in combined})==771
 combined.sort(key=lambda x:int(x.split("\t",1)[0]))
 sums=lambda field:sum(int(x[field]) for x in shards)
 hist=defaultdict(int)
 for x in shards:
  for k,v in x["m2_m3_m4_hist"].items():hist[k]+=v
 p3=sums("selected_K18_p3_uses");p4=sums("selected_K20_p4_uses");terminal=sums("terminal_K3_tails");charge=sums("full_charge_scaled_U")
 assert sums("input_records")==TOTAL and sums("input_weight_sum_scaled_U")==724_159_651_336_720_220_160
 assert p3==399_275_484 and sums("pivotable_K20_children")==p4==570_281_318 and terminal==18_249_002_176==32*p4
 assert sum(hist.values())==p4
 out_path=resolve(output);sample_path=Path(str(out_path)+".samples.tsv")
 sample_tmp=Path(str(sample_path)+".tmp");sample_tmp.write_text(SAMPLE_HEADER+"\n"+"\n".join(combined)+"\n");os.replace(sample_tmp,sample_path)
 result={
  "status":"PASS_COMPLETE_HIDDEN_COLLECTED_K18_K23_SINGLETON_CHARGE","degree":23,"scale_U":str(U),"strict_id":ID,
  "input":INPUT,"input_sha256_expected":INPUT_SHA,"input_interval":[0,TOTAL],"input_records":TOTAL,
  "input_weight_sum_scaled_U":str(sums("input_weight_sum_scaled_U")),"input_weight_l1_scaled_U":str(sums("input_weight_l1_scaled_U")),
  "selected_K18_p3_uses":p3,"pivotable_K20_children":p4,"selected_K20_p4_uses":p4,"terminal_K3_tails":terminal,
  "full_occurrences":terminal,"irreducible_occurrences":terminal,"full_charge_scaled_U":str(charge),"irreducible_charge_scaled_U":str(charge),
  "exact_charge":exact_text(charge),"sign_rule":"H18 weight w; K2 response gives -w/m3; terminal K3 response gives +w/(m3*m4)",
  "m2_m3_m4_hist":dict(sorted(hist.items())),
  "cache_shard_sums":{"K18_keys":sum(x["cache"]["K18_keys"] for x in shards),"K18_hits":sum(x["cache"]["K18_hits"] for x in shards),"K18_misses":sum(x["cache"]["K18_misses"] for x in shards),"K20_K3_keys":sum(x["cache"]["K20_K3_keys"] for x in shards),"K20_K3_hits":sum(x["cache"]["K20_K3_hits"] for x in shards),"K20_K3_misses":sum(x["cache"]["K20_K3_misses"] for x in shards)},
  "literal_sample_source_records":771,"literal_sample_ledger":str(sample_path.relative_to(ROOT)),"literal_sample_ledger_sha256":sha(sample_path),
  "shard_evidence":evidence,"terminality":"every K23 K3 child has active-anchor mass 1, below frozen pivot mass 4","full_equals_irreducible":True,
  "scope":"strict singleton D14:222|R:2-2-2-3 scalar only; exact three-shard merge; no rows, K24, membership, or conjecture verdict"}
 tmp=Path(str(out_path)+".tmp");tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");os.replace(tmp,out_path)
 print(json.dumps({"status":result["status"],"strict_id":ID,"full_charge_scaled_U":str(charge),"exact_charge":result["exact_charge"],"witnesses":771},indent=2))

def self_test():
 x={"status":"PASS_BOUNDED_HIDDEN_COLLECTED_K18_K23_GATE","degree":23,"scale_U":str(U),"input":INPUT,"input_interval":[0,1],"input_records":1,"strict_id":ID,"pivotable_K20_children":1,"selected_K20_p4_uses":1,"terminal_K3_tails":32,"full_occurrences":32,"irreducible_occurrences":32,"full_charge_scaled_U":"7","irreducible_charge_scaled_U":"7","m2_m3_m4_hist":{"3_1_1":1},"cache":{"K18_keys":1,"K18_hits":0,"K18_misses":1,"K20_K3_keys":1,"K20_K3_hits":0,"K20_K3_misses":1},"selected_K18_p3_uses":1,"full_equals_irreducible":True}
 validate_one(x,[0,1]);rejected=0
 for mutate in (lambda z:z.update(strict_id="hostile"),lambda z:z.update(irreducible_charge_scaled_U="8"),lambda z:z.update(terminal_K3_tails=31),lambda z:z.update(m2_m3_m4_hist={"3_1_1":2})):
  y=json.loads(json.dumps(x));mutate(y)
  try:validate_one(y,[0,1])
  except AssertionError:rejected+=1
  else:raise AssertionError("hostile merger mutation accepted")
 assert rejected==4;print(json.dumps({"status":"PASS_K23_HIDDEN_COLLECTED_MERGER_HOSTILE_SELFTEST","hostile_mutations_rejected":rejected},indent=2))

def main():
 p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");p.add_argument("--output");p.add_argument("shards",nargs="*");a=p.parse_args()
 if a.self_test:self_test();return
 if a.output is None or len(a.shards)!=3:p.error("--output and exactly three shards are required")
 merge(a.shards,a.output)
if __name__=="__main__":main()
