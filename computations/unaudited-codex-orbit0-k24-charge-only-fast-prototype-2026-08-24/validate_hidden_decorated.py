#!/usr/bin/env python3
"""Fail-closed validator for K24 hidden decorated D14 R2-4-4 charge-only intervals."""
import argparse,copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
U=400_591_699_200
ID="D14:222|R:2-4-4"
INPUT_SHA="22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8"
PINS={"run_k24_charge_hidden_decorated.rs":"cd3777be520f5d4d77d6da72a4b54ef1a0e7eff91fb923b037b447b730276deb","k24_hidden_decorated_impl.rs":"fb879aee3d8d7ba0ee17f3d0289c037e99d2f191b27567ff2603b8c5e2b226bb","k24_hidden_base.rs":"ec68ac205d1737778d7fe1c23d1f2108fc2b274c8c54cb29716915ec8ba17c08","k24_hidden_base_run_filtered_k17.rs":"5b0b5a467c6418b2bf042b47a89636c0135d93cdea656fd864fb5708f7682056","run_k24_charge_hidden_decorated":"fc65915201e0378f6e9f68857907c3e48041aa207c10513319ac353723db4e71"}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(x,full=False):
 assert x["degree"]==24 and int(x["scale_U"])==U and x["covered_lineage_ids"]==[ID]
 assert x["input_sha256_expected"]==INPUT_SHA and x["input_records_declared"]==101545723
 lo,hi=x["input_interval"];assert 0<=lo<hi<=101545723 and x["input_records_consumed"]==hi-lo
 if full:assert [lo,hi]==[0,101545723]
 s=x["sink"];assert [s["first_tail_degree"],s["intermediate_degree"],s["terminal_tail_degree"]]==[4,20,4]
 assert s["first_tail_evaluations"]==60*x["input_records_consumed"]
 assert s["terminal_K24_occurrences"]==60*s["selected_p3"]
 assert s["full_occurrences"]==s["irreducible_occurrences"]==s["terminal_K24_occurrences"]
 assert int(s["full_charge_scaled_U"])==int(s["irreducible_charge_scaled_U"])
 assert s["cache_hits"]+s["cache_misses"]==s["selected_p3"]
 hist={tuple(map(int,k.split("_"))):v for k,v in s["m2_m3_histogram"].items()}
 assert sum(hist.values())==s["pivotable_intermediate_children"]
 assert sum(m3*n for (_,m3),n in hist.items())==s["selected_p3"]
 assert all(U%(m2*m3)==0 for m2,m3 in hist)
 assert x["literal_witness_records"]==257
 ledger=Path(x["sample_ledger"]);assert ledger.is_file() and len(ledger.read_text().splitlines())==258
 assert "active-anchor mass 0" in x["universal_terminality"]
 return {"id":ID,"interval":[lo,hi],"literal_records":257}
def hostile(g):
 out=[]
 def reject(n,fn):
  x=copy.deepcopy(g);fn(x)
  try:validate(x)
  except (AssertionError,KeyError,ValueError,TypeError):out.append(n);return
  raise AssertionError(n)
 reject("wrong_id",lambda x:x["covered_lineage_ids"].__setitem__(0,"bad"))
 reject("wrong_U",lambda x:x.__setitem__("scale_U","1"))
 reject("bad_input_hash",lambda x:x.__setitem__("input_sha256_expected","0"*64))
 reject("bad_occurrence",lambda x:x["sink"].__setitem__("full_occurrences",0))
 reject("bad_scalar",lambda x:x["sink"].__setitem__("irreducible_charge_scaled_U","0"))
 reject("missing_samples",lambda x:x.__setitem__("literal_witness_records",0))
 return out
def main():
 a=argparse.ArgumentParser();a.add_argument("result");a.add_argument("--require-full",action="store_true");a.add_argument("--audit-out");z=a.parse_args()
 for n,h in PINS.items():assert sha(HERE/n)==h
 x=json.loads(Path(z.result).read_text());summary=validate(x,z.require_full)
 out={"status":"PASS_INDEPENDENT_K24_HIDDEN_DECORATED_R244_CHARGE_ONLY_VALIDATOR","pins":PINS,"result_sha256":sha(Path(z.result)),"summary":summary,"hostile_rejections":hostile(x)}
 text=json.dumps(out,indent=2,sort_keys=True)+"\n"
 if z.audit_out:Path(z.audit_out).write_text(text)
 print(text,end="")
if __name__=="__main__":main()

