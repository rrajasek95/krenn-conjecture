#!/usr/bin/env python3
"""Strict no-gap assembly of the atomic D15 R4-2 K21 charge shards."""
from __future__ import annotations
import hashlib, json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent
IDS=["D15:223|R:4-2","D15:232|R:4-2","D15:322|R:4-2"]
U=400_591_699_200
N=5_311_211
OUT=HERE/"results_k21_d15_r4_2_charge.json"

def sha(p:Path)->str:
 h=hashlib.sha256();h.update(p.read_bytes());return h.hexdigest()
def strict(ids:list[str])->None: assert ids==IDS
def addhist(dst:dict[int,int],src:dict[str,int])->None:
 for k,v in src.items():dst[int(k)]+=v

def main()->None:
 files=[HERE/f"results_shard_{i:02d}.json" for i in range(11)]
 assert all(p.is_file() for p in files)
 rows=[json.loads(p.read_text()) for p in files]
 expected=[]
 for i in range(10):expected.append([i*524_288,(i+1)*524_288])
 expected.append([5_242_880,N])
 assert [x["input_interval"] for x in rows]==expected
 assert all(x["status"]=="PASS_ATOMIC_INTERVAL_GROUPED_D15_R4_2_K21_CHARGE" for x in rows)
 assert all(x["input_records_declared"]==N and int(x["scale_U"])==U for x in rows)
 for x in rows:
  strict(x["strict_covered_lineage_ids"]);assert x["individual_id_charges"] is None
  a,b=x["input_interval"];assert x["input_records_consumed"]==b-a
  assert x["K4_tail_candidates"]==60*x["first_pivot_uses"]
  assert x["K2_tail_occurrences"]==12*x["second_pivot_uses"]
  assert x["full_occurrences"]==x["irreducible_occurrences"]==x["K2_tail_occurrences"]
  assert int(x["full_charge_scaled_U"])==int(x["irreducible_charge_scaled_U"])
  assert x["K2_response_cache"]["hits"]+x["K2_response_cache"]["misses"]==x["second_pivot_uses"]
 for hostile in ([],IDS[:2],IDS+[IDS[-1]],[IDS[1],IDS[0],IDS[2]]):
  try:strict(hostile)
  except AssertionError:pass
  else:raise AssertionError(f"accepted hostile ID interface {hostile}")
 keys=["input_records_consumed","first_pivot_uses","K4_tail_candidates","retained_pivotable_K19_children","second_pivot_uses","K2_tail_occurrences","full_occurrences","irreducible_occurrences"]
 totals={k:sum(x[k] for x in rows) for k in keys}
 totals["input_weight_sum"]=sum(int(x["input_weight_sum"]) for x in rows)
 totals["full_charge_scaled_U"]=sum(int(x["full_charge_scaled_U"]) for x in rows)
 totals["irreducible_charge_scaled_U"]=sum(int(x["irreducible_charge_scaled_U"]) for x in rows)
 assert totals=={
  "input_records_consumed":N,"first_pivot_uses":44_342_881,"K4_tail_candidates":2_660_572_860,
  "retained_pivotable_K19_children":972_495_600,"second_pivot_uses":1_549_305_840,
  "K2_tail_occurrences":18_591_670_080,"full_occurrences":18_591_670_080,
  "irreducible_occurrences":18_591_670_080,"input_weight_sum":322_486_272,
  "full_charge_scaled_U":-105_580_126_744_994_119_680,
  "irreducible_charge_scaled_U":-105_580_126_744_994_119_680,
 }
 h1,h2,hp=defaultdict(int),defaultdict(int),defaultdict(int)
 for x in rows:
  addhist(h1,x["first_denominator_hist"]);addhist(h2,x["second_denominator_hist"]);addhist(hp,x["product_denominator_hist"])
 assert sum(h1.values())==N and sum(k*v for k,v in h1.items())==totals["first_pivot_uses"]
 assert sum(h2.values())==totals["retained_pivotable_K19_children"]
 assert sum(k*v for k,v in h2.items())==totals["second_pivot_uses"]
 assert sum(hp.values())==totals["retained_pivotable_K19_children"]
 assert all(U%k==0 for k in hp)
 reduced=Fraction(totals["full_charge_scaled_U"],U)
 assert reduced==Fraction(-2_333_827_745_792,8_855)
 out={
  "status":"PASS_COMPLETE_GROUPED_D15_R4_2_K21_CHARGE",
  "strict_covered_lineage_ids":IDS,"individual_id_charges":None,"scale_U":str(U),
  "atomic_interval_coverage":{"shards":11,"intervals":expected,"no_gap":True,"no_overlap":True,"records":N},
  **{k:(str(v) if k in {"input_weight_sum","full_charge_scaled_U","irreducible_charge_scaled_U"} else v) for k,v in totals.items()},
  "full_equals_irreducible":True,
  "reduced_exact_scalar":str(reduced),
  "first_denominator_hist":{str(k):v for k,v in sorted(h1.items())},
  "second_denominator_hist":{str(k):v for k,v in sorted(h2.items())},
  "product_denominator_hist":{str(k):v for k,v in sorted(hp.items())},
  "all_U_divisions_exact":True,
  "sign_rule":"w19=-w15*U/m1; w21=-w19/m2=+w15*U/(m1*m2)",
  "terminality":"all realized K21 signatures have anchor sum 3, below every K0 pivot's anchor sum 4",
  "shard_cache_accounting":{"hits":sum(x["K2_response_cache"]["hits"] for x in rows),"misses":sum(x["K2_response_cache"]["misses"] for x in rows),"literal_tail_guards_on_miss":sum(x["K2_response_cache"]["literal_tail_guards_on_miss"] for x in rows),"note":"shard-local caches; misses are not a global distinct-key census"},
  "runtime_guard":{"sum_shard_elapsed_seconds":sum(x["elapsed_seconds"] for x in rows),"max_shard_elapsed_seconds":max(x["elapsed_seconds"] for x in rows),"observed_live_RSS_peak_sample_KiB":4_430_144,"per_shard_limit_seconds":180,"per_shard_limit_bytes":8*(1<<30)},
  "sha256":{"shards":{p.name:sha(p) for p in files}},
  "scope":"strict grouped three-ID scalar only; the retained checkpoint combines the three source IDs, so no individual-ID scalar or other K21 path is inferred",
 }
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
