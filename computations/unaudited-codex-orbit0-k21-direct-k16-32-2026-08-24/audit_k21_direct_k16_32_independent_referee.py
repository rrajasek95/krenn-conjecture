#!/usr/bin/env python3
"""Independent no-full-rerun referee for grouped D16 R:3-2 at K21."""
from __future__ import annotations
import hashlib,json
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
IDS=[f"D16:{x}|R:3-2" for x in ("224","233","242","323","332","422")]
U=400_591_699_200
SOURCE=HERE/"run_k21_direct_k16_32.rs";RESULT=HERE/"results_k21_direct_k16_32.json";MANIFEST=HERE/"MANIFEST.sha256";ORIGINAL_AUDIT=HERE/"results_k21_direct_k16_32_audit.json"
REPLAY_SOURCE=HERE/"referee_nonzero_k19_k21.rs";REPLAY=HERE/"results_nonzero_k19_k21_referee.json"
DAG=ROOT/"computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
OUT=HERE/"results_k21_direct_k16_32_independent_referee.json"
EXPECTED={"source":"b4f0c4ae64d2d29d1febb2bd6beb4b2e745f944701404620c41cd591d781f73a","result":"92a6a9a27dbf0fc3c82f1dd6b71155cf81118f5e1bf9ff7b1fbb38ab313793ca","manifest":"7c4e12c74af5ab0c376dd880b2100c8aca233b08fe28d50fbba4ee709a607a8a","original_audit":"c216dfffd3e80df12a9362c7a39d7929cb03ede03db04c277f3d1f97f12e0bc8","replay_source":"ae712514d14b109997c64336c46acd93b6045fe4a41ddd102fb5a9c7d9c278e9","replay":"cef1800368019f2d10844fd7e30004cc320320fec2c3707cf26a3d521dfda2f7"}
def sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def strict(ids:list[str])->None:assert ids==IDS
def logical(x)->str:return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main()->None:
 observed={"source":sha(SOURCE),"result":sha(RESULT),"manifest":sha(MANIFEST),"original_audit":sha(ORIGINAL_AUDIT),"replay_source":sha(REPLAY_SOURCE),"replay":sha(REPLAY)};assert observed==EXPECTED
 for line in MANIFEST.read_text().splitlines():
  digest,name=line.split(maxsplit=1);assert sha(HERE/name)==digest
 dag=json.loads(DAG.read_text());required=dag["required_reachable_lineage_ids_by_degree"]["21"];assert len(required)==len(set(required))==52 and all(x in required for x in IDS)
 r=json.loads(RESULT.read_text());strict(r["ids"]);assert r["covered_ids"]==6 and r["individual_id_charges"] is None
 for hostile in ([],IDS[:5],IDS+[IDS[0]],[IDS[1],IDS[0],*IDS[2:]]):
  try:strict(hostile)
  except AssertionError:pass
  else:raise AssertionError("hostile grouped interface accepted")
 assert r["status"]=="PASS_COMPLETE_GROUPED_SIX_D16_R_3_2_K21_CHARGE" and int(r["scale_U"])==U
 expected={"records_consumed":24_097_095,"records_declared":24_097_095,"source_rows":24_097_095,"signed_source_coefficient":1_464_625_152,"l1_source_coefficient":13_978_655_136,"pivotable_K16_rows":24_003_767,"selected_p1_uses":129_939_187,"K19_child_occurrences":4_158_053_984,"pivotable_K19_child_occurrences":1_295_008_880,"selected_p2_uses":2_041_782_688,"K21_terminal_occurrences":24_501_392_256}
 for k,v in expected.items():assert int(r[k])==v,(k,r[k],v)
 assert r["K19_child_occurrences"]==32*r["selected_p1_uses"]
 assert r["K21_terminal_occurrences"]==12*r["selected_p2_uses"]==r["full_occurrences"]==r["irreducible_occurrences"]
 charge=-643_522_419_678_967_234_560;assert int(r["full_charge_scaled_U"])==int(r["irreducible_charge_scaled_U"])==charge and Fraction(charge,U)==Fraction(-618_475_450_368,385)
 hist=r["m1_m2_occurrence_hist"];assert sum(hist.values())==r["pivotable_K19_child_occurrences"]
 assert sum(int(k.split("_")[1])*v for k,v in hist.items())==r["selected_p2_uses"]
 assert all(U%(int(k.split("_")[0])*int(k.split("_")[1]))==0 for k in hist)
 cache=r["terminal_profile_cache"];assert cache["hits"]+cache["misses"]==r["selected_p2_uses"] and cache["peak_keys_per_100k_chunk"]<=cache["misses"]
 src=SOURCE.read_text()
 for fragment in ["let k19 = replace(row, &e.anchors[p1], t1);","let ps2 = avail(s2, e);","assert_eq!(U21 % ((m1 * m2) as i128), 0);","let unit_weight = U21 / ((m1 * m2) as i128);","sum.charge += coefficient * z.charge_per_source_coefficient_scaled;","assert_eq!((full_n, irreducible_n), (12, 12));","assert_eq!(full_q, irreducible_q);"]:assert fragment in src
 replay=json.loads(REPLAY.read_text());assert replay["status"]=="PASS_INDEPENDENT_DISTRIBUTED_NONZERO_K19_K21_REPLAY"
 assert replay["source_grid_records"]==257 and replay["nonzero_continuation_witnesses"]==91 and (replay["first_record_index"],replay["last_record_index"])==(0,24_002_964)
 assert replay["K3_tails_replayed"]==32*91 and replay["pivotable_K19_children"]==1264 and replay["p2_uses"]==1336
 assert replay["literal_terminal_K21_children"]==12*replay["p2_uses"]==replay["literal_child_signature_and_charge_checks"]==16_032
 assert replay["all_U_divisions_exact"] is replay["all_K21_children_terminal"] is replay["producer_ledger_continuation_fields_match"] is True
 assert sum(replay["m1_m2_hist"].values())==replay["pivotable_K19_children"] and sum(int(k.split("_")[1])*v for k,v in replay["m1_m2_hist"].items())==replay["p2_uses"]
 out={"status":"PASS_INDEPENDENT_GROUPED_SIX_D16_R_3_2_K21_TERMINAL_REFEREE","strict_covered_lineage_ids":IDS,"individual_id_charges":None,
  "charge":{"scale_U":U,"full_scaled":str(charge),"irreducible_scaled":str(charge),"full_equals_irreducible":True,"reduced":"-618475450368/385"},"counts":expected,
  "arithmetic_guards":{"two_response_sign":"+v/(m1*m2)","all_histogram_U_divisions_exact":True,"K19_children_equal_32_times_p1":True,"K21_children_equal_12_times_p2":True,"cache_queries_equal_p2_uses":True},
  "distributed_nonzero_continuation_replay":{"source_grid_records":257,"nonzero_witnesses":91,"index_span":[0,24_002_964],"K3_tails":2912,"pivotable_K19_children":1264,"p2_uses":1336,"literal_terminal_K21_children":16032,"producer_continuation_fields_match":True},
  "hostile_interface_guard":{"missing_rejected":True,"duplicate_rejected":True,"reordered_rejected":True,"exact_members_of_52_ID_K21_DAG":True},
  "sha256":{**observed,"recurrence_dag":sha(DAG)},"scope":"No full replay; exact grouped six-ID package and distributed nonzero K19-to-K21 continuations only; no individual ID or other path inferred."}
 out["logical_sha256"]=logical(out);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
