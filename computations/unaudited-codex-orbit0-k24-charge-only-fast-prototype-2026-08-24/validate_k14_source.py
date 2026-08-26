#!/usr/bin/env python3
"""Fail-closed validator for exact K24 D14 R3-3-4 and R4-2-4 charge-only folds."""
import argparse,copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
U=400_591_699_200
IDS=["D14:222|R:3-3-4","D14:222|R:4-2-4"]
DEGREES={"D14:222|R:3-3-4":[3,3,4],"D14:222|R:4-2-4":[4,2,4]}
TAILS={2:12,3:32,4:60}
SOURCE_SHA="dd9510f3324b160a3b496ba6d0b5bdfb9335699a1fc99cd75c18dadaf8eeca6d"
BINARY_SHA="4049688d492ee604ead3b43e1bb3f42efb42e9da7758c8128b08f67377469853"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(x,full=False):
 assert x["degree"]==24 and int(x["scale_U"])==U and x["covered_lineage_ids"]==IDS
 assert x["R8_records_declared"]==485
 if full:
  assert x["distributed_record_mode"] is False and x["R8_record_interval"]==[0,485] and x["R8_records_consumed"]==485
 assert list(x["sinks"])==IDS
 for name,s in x["sinks"].items():
  d=DEGREES[name]
  assert [s["first_response_degree"],s["second_response_degree"],s["terminal_response_degree"]]==d
  assert s["first_children"]==TAILS[d[0]]*s["selected_p1_uses"]
  assert s["second_children"]==TAILS[d[1]]*s["selected_p2_uses"]
  assert s["K24_terminal_occurrences"]==TAILS[d[2]]*s["selected_p3_uses"]
  assert s["full_occurrences"]==s["irreducible_occurrences"]==s["K24_terminal_occurrences"]
  assert int(s["full_charge_scaled_U"])==int(s["irreducible_charge_scaled_U"])
  assert s["literal_preterminal_cache"]["hits"]+s["literal_preterminal_cache"]["misses"]==s["pivotable_second_children"]
  assert sum(s["first_denominator_hist"].values())==x["source_heads"]
  assert sum(int(k)*v for k,v in s["first_denominator_hist"].items())==s["selected_p1_uses"]
  assert sum(s["second_denominator_hist"].values())==s["pivotable_first_children"]
  assert sum(int(k)*v for k,v in s["second_denominator_hist"].items())==s["selected_p2_uses"]
  assert sum(s["third_denominator_hist"].values())==s["pivotable_second_children"]
  assert sum(int(k)*v for k,v in s["third_denominator_hist"].items())==s["selected_p3_uses"]
  assert all(U%int(k)==0 for k in s["product_denominator_hist"])
 assert x["all_realized_cached_K24_responses_terminal"] is True
 assert x["literal_sample_guard"]["all_literal_K24_children_terminal"] is True
 assert "no intermediate or terminal row/column output" in x["scope"]
 return {"ids":2,"groups":2,"records":x["R8_records_consumed"]}
def hostile(good):
 out=[]
 def reject(n,fn):
  x=copy.deepcopy(good);fn(x)
  try:validate(x)
  except (AssertionError,KeyError,ValueError,TypeError):out.append(n);return
  raise AssertionError("hostile accepted "+n)
 reject("missing_sink",lambda x:x["sinks"].pop(IDS[1]))
 reject("duplicate_id",lambda x:x["covered_lineage_ids"].__setitem__(1,IDS[0]))
 reject("wrong_U",lambda x:x.__setitem__("scale_U","1"))
 reject("bad_occurrence",lambda x:x["sinks"][IDS[0]].__setitem__("full_occurrences",0))
 reject("bad_scalar",lambda x:x["sinks"][IDS[0]].__setitem__("irreducible_charge_scaled_U","0"))
 reject("nonterminal",lambda x:x.__setitem__("all_realized_cached_K24_responses_terminal",False))
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument("result");p.add_argument("--require-full",action="store_true");p.add_argument("--audit-out");a=p.parse_args()
 assert sha(HERE/"run_k24_charge_k14_source.rs")==SOURCE_SHA
 assert sha(HERE/"run_k24_charge_k14_source")==BINARY_SHA
 x=json.loads(Path(a.result).read_text());summary=validate(x,a.require_full)
 out={"status":"PASS_INDEPENDENT_K24_K14_TWO_SINGLETON_CHARGE_ONLY_VALIDATOR","source_sha256":SOURCE_SHA,"binary_sha256":BINARY_SHA,"result_sha256":sha(Path(a.result)),"summary":summary,"hostile_rejections":hostile(x)}
 text=json.dumps(out,indent=2,sort_keys=True)+"\n"
 if a.audit_out:Path(a.audit_out).write_text(text)
 print(text,end="")
if __name__=="__main__":main()
