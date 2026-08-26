#!/usr/bin/env python3
"""Fail-closed validator for grouped six-ID K24 direct-K16 R4-4."""
import argparse,copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
U=400_591_699_200
IDS=[f"D16:{p}|R:4-4" for p in ["224","233","242","323","332","422"]]
SOURCE_SHA="1ed9ef5a9b4450f55f2259a11a88a2f370259a6373af6b4b735361f928cdf1e1"
BINARY_SHA="3a1b5e716ff4f781a5e523e990d8f209975b34231faf55cce8e8dd72e4f88ef9"
INPUT_SHA="93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(x,full=False):
 assert x["group_id"]=="source_D16_R4_4" and x["degree"]==24 and int(x["scale_U"])==U
 assert x["ids"]==IDS and x["covered_ids"]==6 and x["individual_id_charges"] is None
 lo,hi=x["record_interval"];assert 0<=lo<hi<=24097095 and x["records_declared"]==24097095
 if full:assert [lo,hi]==[0,24097095] and x["distributed_prefix"] is False
 assert x["K24_terminal_occurrences"]==60*x["p2_uses"]
 assert x["full_occurrences"]==x["irreducible_occurrences"]==x["K24_terminal_occurrences"]
 assert int(x["full_charge_scaled_U"])==int(x["irreducible_charge_scaled_U"])
 h={tuple(map(int,k.split("_"))):v for k,v in x["m1_m2_hist"].items()}
 assert sum(h.values())==x["pivotable_intermediate_children"]
 assert sum(m2*n for (_,m2),n in h.items())==x["p2_uses"]
 assert all(U%(m1*m2)==0 for m1,m2 in h)
 c=x["terminal_cache"];assert c["hits"]+c["misses"]==x["p2_uses"]
 if full:assert x["literal_samples"]==257
 ledger=Path(x["sample_ledger"]);assert ledger.is_file() and len(ledger.read_text().splitlines())==x["literal_samples"]+1
 assert "active-anchor mass 0" in x["terminality"]
 assert "grouped six-ID scalar is source-faithful" in x["packet_grouping_guard"]
 return {"ids":6,"group":"source_D16_R4_4","interval":[lo,hi],"literal_samples":x["literal_samples"]}
def hostile(g):
 out=[]
 def reject(n,fn):
  x=copy.deepcopy(g);fn(x)
  try:validate(x)
  except (AssertionError,KeyError,ValueError,TypeError):out.append(n);return
  raise AssertionError(n)
 reject("missing_id",lambda x:x["ids"].pop())
 reject("duplicate_id",lambda x:x["ids"].__setitem__(1,x["ids"][0]))
 reject("wrong_group",lambda x:x.__setitem__("group_id","source_D16_R2_2_4"))
 reject("wrong_U",lambda x:x.__setitem__("scale_U","1"))
 reject("bad_occurrence",lambda x:x.__setitem__("full_occurrences",0))
 reject("bad_scalar",lambda x:x.__setitem__("irreducible_charge_scaled_U","0"))
 return out
def main():
 a=argparse.ArgumentParser();a.add_argument("result");a.add_argument("--require-full",action="store_true");a.add_argument("--audit-out");z=a.parse_args()
 assert sha(HERE/"run_k24_charge_k16_r44.rs")==SOURCE_SHA and sha(HERE/"run_k24_charge_k16_r44")==BINARY_SHA
 x=json.loads(Path(z.result).read_text());summary=validate(x,z.require_full)
 out={"status":"PASS_INDEPENDENT_K24_GROUPED_D16_R44_CHARGE_ONLY_VALIDATOR","source_sha256":SOURCE_SHA,"binary_sha256":BINARY_SHA,"checkpoint_sha256_expected":INPUT_SHA,"result_sha256":sha(Path(z.result)),"summary":summary,"hostile_rejections":hostile(x)}
 text=json.dumps(out,indent=2,sort_keys=True)+"\n"
 if z.audit_out:Path(z.audit_out).write_text(text)
 print(text,end="")
if __name__=="__main__":main()

