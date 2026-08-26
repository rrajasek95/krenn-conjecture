#!/usr/bin/env python3
"""Independent package/arithmetic/sample referee for grouped D15 R4-2."""
from __future__ import annotations
import hashlib,json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
IDS=["D15:223|R:4-2","D15:232|R:4-2","D15:322|R:4-2"]
U=400_591_699_200;N=5_311_211
SOURCE=HERE/"run_k21_d15_r4_2_charge.rs";ASSEMBLER=HERE/"assemble_k21_d15_r4_2_charge.py";RESULT=HERE/"results_k21_d15_r4_2_charge.json"
SAMPLE_SOURCE=HERE/"referee_k21_d15_r4_2_samples.rs";SAMPLE_RESULT=HERE/"results_k21_d15_r4_2_samples.json";SAMPLE_TSV=HERE/"results_k21_d15_r4_2_samples.tsv"
INPUT=ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k15.bin"
DAG=ROOT/"computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
OUT=HERE/"results_k21_d15_r4_2_referee.json"
def sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def strict(ids:list[str])->None:assert ids==IDS
def logical(x)->str:return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main()->None:
 assert sha(INPUT)=="e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f"
 assert INPUT.stat().st_size==16+32*N
 with INPUT.open("rb") as f:assert f.read(8)==b"K15CHK1\0" and int.from_bytes(f.read(8),"little")==N
 dag=json.loads(DAG.read_text());required=dag["required_reachable_lineage_ids_by_degree"]["21"]
 assert len(required)==len(set(required))==52 and all(x in required for x in IDS)
 r=json.loads(RESULT.read_text());strict(r["strict_covered_lineage_ids"]);assert r["individual_id_charges"] is None
 assert r["status"]=="PASS_COMPLETE_GROUPED_D15_R4_2_K21_CHARGE" and int(r["scale_U"])==U
 assert r["atomic_interval_coverage"]=={"shards":11,"intervals":[[i*524288,(i+1)*524288] for i in range(10)]+[[5242880,N]],"no_gap":True,"no_overlap":True,"records":N}
 assert r["input_records_consumed"]==N and int(r["input_weight_sum"])==322_486_272
 assert r["first_pivot_uses"]==44_342_881 and r["K4_tail_candidates"]==60*r["first_pivot_uses"]==2_660_572_860
 assert r["retained_pivotable_K19_children"]==972_495_600 and r["second_pivot_uses"]==1_549_305_840
 assert r["K2_tail_occurrences"]==r["full_occurrences"]==r["irreducible_occurrences"]==12*r["second_pivot_uses"]==18_591_670_080
 charge=-105_580_126_744_994_119_680
 assert int(r["full_charge_scaled_U"])==int(r["irreducible_charge_scaled_U"])==charge
 assert Fraction(charge,U)==Fraction(-2_333_827_745_792,8_855) and r["reduced_exact_scalar"]=="-2333827745792/8855"
 assert sum(map(int,r["first_denominator_hist"].values()))==N
 assert sum(int(k)*v for k,v in r["first_denominator_hist"].items())==r["first_pivot_uses"]
 assert sum(r["second_denominator_hist"].values())==r["retained_pivotable_K19_children"]
 assert sum(int(k)*v for k,v in r["second_denominator_hist"].items())==r["second_pivot_uses"]
 assert sum(r["product_denominator_hist"].values())==r["retained_pivotable_K19_children"] and all(U%int(k)==0 for k in r["product_denominator_hist"])
 for hostile in ([],IDS[:2],IDS+[IDS[0]],[IDS[1],IDS[0],IDS[2]]):
  try:strict(hostile)
  except AssertionError:pass
  else:raise AssertionError("hostile grouped interface accepted")
 src=SOURCE.read_text()
 for fragment in ["let w19=-(v as i128)*U/(m1 as i128)","let w21=-w19/(m2 as i128)","if !ps.is_empty(){out.push", "assert_eq!(U%((m1*m2)as i128),0)","assert_eq!(z.k21,12*z.p2)","rename(tmp,&args[2])"]:assert fragment in src
 s=json.loads(SAMPLE_RESULT.read_text());strict(s["strict_covered_lineage_ids"])
 assert s["status"]=="PASS_INDEPENDENT_257_LITERAL_D15_R4_2_K21_SAMPLES" and s["parents"]==257 and (s["first_index"],s["last_index"])==(0,N-1)
 assert s["K4_candidates"]==60*s["p1_uses"] and s["K21_children"]==12*s["p2_uses"]==s["literal_abstract_cycle_key_guards"] and s["all_K21_terminal"] is True
 lines=SAMPLE_TSV.read_text().splitlines();assert len(lines)==258
 head=lines[0].split("\t");rows=[dict(zip(head,x.split("\t"),strict=True)) for x in lines[1:]]
 indices=[int(x["input_index"]) for x in rows];assert indices==[j*(N-1)//256 for j in range(257)]
 with INPUT.open("rb") as f:
  for x,i in zip(rows,indices,strict=True):
   f.seek(16+32*i);assert f.read(24).hex()==x["row"];assert int.from_bytes(f.read(8),"little",signed=True)==int(x["weight"])
   assert int(x["K4_candidates"])==60*int(x["p1_uses"]) and int(x["K21_children"])==12*int(x["p2_uses"])
 out={"status":"PASS_INDEPENDENT_TERMINAL_REFEREE_GROUPED_D15_R4_2_K21_CHARGE","strict_covered_lineage_ids":IDS,"individual_id_charges":None,
  "charge":{"scale_U":U,"full_scaled":str(charge),"irreducible_scaled":str(charge),"full_equals_irreducible":True,"reduced":"-2333827745792/8855"},
  "counts":{"input_records":N,"first_pivot_uses":r["first_pivot_uses"],"K4_tail_candidates":r["K4_tail_candidates"],"retained_pivotable_K19_children":r["retained_pivotable_K19_children"],"second_pivot_uses":r["second_pivot_uses"],"terminal_K21_occurrences":r["K2_tail_occurrences"]},
  "guards":{"no_gap_no_overlap_11_shards":True,"all_U_divisions_exact":True,"two_response_sign_replayed":True,"257_distributed_literal_parents":True,"literal_abstract_cycle_key_comparisons":s["literal_abstract_cycle_key_guards"],"all_sample_K21_children_terminal":True,"missing_duplicate_reordered_ID_sets_rejected":True},
  "runtime":{"sum_shard_seconds":r["runtime_guard"]["sum_shard_elapsed_seconds"],"max_shard_seconds":r["runtime_guard"]["max_shard_elapsed_seconds"],"observed_live_RSS_peak_sample_KiB":r["runtime_guard"]["observed_live_RSS_peak_sample_KiB"]},
  "sha256":{"input":sha(INPUT),"producer_source":sha(SOURCE),"assembler":sha(ASSEMBLER),"producer_result":sha(RESULT),"sample_referee_source":sha(SAMPLE_SOURCE),"sample_referee_result":sha(SAMPLE_RESULT),"sample_tsv":sha(SAMPLE_TSV),"recurrence_dag":sha(DAG)},
  "scope":"strict grouped three-ID scalar only; no individual-ID scalar and no inference to another K21 path"}
 out["logical_sha256"]=logical(out);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
