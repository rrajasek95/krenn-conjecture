#!/usr/bin/env python3
import hashlib, json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
SRC=ROOT/"computations/unaudited-codex-orbit0-k23-direct23-source-fold-2026-08-24"
SCHED=ROOT/"computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24"
DAG=ROOT/"computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
U=400_591_699_200

def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(Path(p).read_text())

pins={
 "result":"e84a39d027e07ad56d1c4d67dd9cab733ef25575aa324c892157deb80272767f",
 "samples":"5968ec8c82678f79887cc208420108ec2878d9ab820793e818dd4c16402a804f",
 "source_manifest":"57cdec4a6445c52bd7d35e1a97d37ef5f476f85e6c1de5b598d8c354b5db2d3b",
 "v1":"d60c5f3545963baa87b48c0d302648725b32e95469aa11112303f8597b712c10",
 "v2":"d0f92693b39f37d378a58a5dc1890704d9c1381b6a1bbb6e4857fa3bb8fc1d02",
 "dag":"469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
 "assembler":"b189ddf195af4e5e896aee495bf7adbc074af0108a4f026ae852fbbabaacbaaf",
 "contract":"6d59f1a24771e3a5e595ab79d8d0309881edea085da62c34b8e70cf93757c9ab",
}
assert sha(SRC/"results_k23_direct23.json")==pins["result"]
assert sha(SRC/"results_k23_direct23.json.samples.tsv")==pins["samples"]
assert sha(SRC/"k23_direct23_fragment_manifest.json")==pins["source_manifest"]
assert sha(SRC/"run_k23_direct23_source_fold_v1.rs")==pins["v1"]
assert sha(SRC/"run_k23_direct23_source_fold.rs")==pins["v2"]
assert sha(DAG)==pins["dag"]
assert sha(SCHED/"assemble_k23_59_exact.py")==pins["assembler"]
assert sha(SCHED/"k23_expected_scalar_groups.json")==pins["contract"]

dag=load(DAG); required=dag["required_reachable_lineage_ids_by_degree"]["23"]
assert len(required)==len(set(required))==59
contract=load(SCHED/"k23_expected_scalar_groups.json")
expected={g["group_id"]:g["ids"] for g in contract["groups"]}
source_manifest=load(SRC/"k23_direct23_fragment_manifest.json")
manifest=load(HERE/"k23_manifest_direct23_23_of_59.json")
assert manifest["source_fragment_manifest_sha256"]==pins["source_manifest"]
assert manifest["groups"]==source_manifest["groups"]
assert [g["group_id"] for g in manifest["groups"]]==["source_D17_R2_4","source_D17_R3_3","source_D18_R2_3","source_D19_R4"]
flat=[]
for g in manifest["groups"]:
 assert g["ids"]==expected[g["group_id"]]
 flat.extend(g["ids"])
 assert g["evidence_sha256"]==pins["result"] and sha(ROOT/g["evidence_path"])==pins["result"]
 assert int(g["full_scaled_U"])==int(g["irreducible_scaled_U"])
 assert Fraction(int(g["full_scaled_U"]),U)==Fraction(g["full"])==Fraction(g["irreducible"])
assert len(flat)==len(set(flat))==23 and set(flat)<=set(required)
assert [x for x in required if x not in set(flat)]==load(HERE/"results_k23_direct23_23_of_59_partial.json")["missing_paths"]

result=load(SRC/"results_k23_direct23.json")
assert result["status"]=="PASS_COMPLETE_K23_DIRECT_D17_D19_23_ID_SOURCE_FOLD"
assert result["source_selection"]=={"mode":"strict_three_shard_merge","intervals":[[0,161],[161,323],[323,485]],"record_count":485}
assert result["covered_ids"]==23 and result["scalar_groups"]==4 and "rows" not in result
assert [g["group_id"] for g in result["groups"]]==[g["group_id"] for g in manifest["groups"]]

shard_names=["results_k23_direct23_shard0.json","results_k23_direct23_shard1.json","results_k23_direct23_shard2.json"]
shard_pins=["65c1591ee95042ccdca29617e43e75a86c1bead4a4faf2454a65d6833d36975d","a819ca879bbfb4227bf797066791201fcd82fa7c0d754d8a672d4d89d7e7f9cb","4266db2f9e3833ae7c63498987f18d792b5aa1340b4cd5b8faca505bf1834503"]
shards=[]
for name,pin in zip(shard_names,shard_pins):assert sha(SRC/name)==pin;shards.append(load(SRC/name))
assert [x["source_selection"]["indices"] for x in shards]==[list(range(0,161)),list(range(161,323)),list(range(323,485))]
add_fields=["source_heads","pivotable_source_heads","p1_uses","intermediate_children","pivotable_intermediate_children","p2_uses","K23_terminal_occurrences","full_occurrences","irreducible_occurrences","full_charge_scaled_U","irreducible_charge_scaled_U"]
for gi,g in enumerate(result["groups"]):
 assert g["ids"]==expected[g["group_id"]]
 parts=[x["groups"][gi] for x in shards]; assert all(p["group_id"]==g["group_id"] and p["ids"]==g["ids"] for p in parts)
 for field in add_fields: assert int(g[field])==sum(int(p[field]) for p in parts)
 hist=defaultdict(int)
 for p in parts:
  for k,v in p["denominator_hist"].items():hist[k]+=v
 assert dict(sorted(hist.items()))==g["denominator_hist"]
 assert g["full_occurrences"]==g["irreducible_occurrences"]==g["K23_terminal_occurrences"]
 assert g["full_charge_scaled_U"]==g["irreducible_charge_scaled_U"]
 entry=manifest["groups"][gi];assert int(entry["full_scaled_U"])==int(g["full_charge_scaled_U"])
 assert Fraction(g["exact_charge"])==Fraction(entry["full"])
ratio_fields=[("p2_uses",60),("p2_uses",32),("p2_uses",32),("p1_uses",60)]
for g,(base,n) in zip(result["groups"],ratio_fields):assert g["K23_terminal_occurrences"]==n*g[base]

scalar_once=sum(int(g["full_scaled_U"]) for g in manifest["groups"])
hostile_id_multiplied=sum(int(g["full_scaled_U"])*len(g["ids"]) for g in manifest["groups"])
assert scalar_once==-941_830_361_301_612_625_920 and Fraction(scalar_once,U)==Fraction(-82_288_431_616,35)
assert hostile_id_multiplied!=scalar_once
partial=load(HERE/"results_k23_direct23_23_of_59_partial.json")
assert partial["status"]=="REJECT_INCOMPLETE_K23_59_ID_GATE" and not partial["complete_K23_claim"]
assert partial["covered_paths"]==23 and partial["scalar_groups"]==4 and len(partial["missing_paths"])==36
assert partial["duplicate_paths"]==partial["extra_paths"]==[]
assert int(partial["full_scaled_U"])==int(partial["irreducible_scaled_U"])==scalar_once
assert Fraction(partial["full"]["text"])==Fraction(partial["irreducible"]["text"])==Fraction(scalar_once,U)

v1=(SRC/"run_k23_direct23_source_fold_v1.rs").read_text();v2=(SRC/"run_k23_direct23_source_fold.rs").read_text()
old='if let Some((_,g))=tar{let line=slots[g].take().unwrap_or_else(||panic!("no nonzero sample ri={} group={}",ri,g));samples.lock().unwrap().push(format!("{}\\t{}",g,line))}'
new='if let Some((_,preferred))=tar{let(g,line)=(0..4).map(|delta|(preferred+delta)%4).find_map(|g|slots[g].take().map(|line|(g,line))).unwrap_or_else(||panic!("no nonzero sample in any group at ri={}",ri));samples.lock().unwrap().push(format!("{}\\t{}",g,line))}'
assert old in v1 and new not in v1 and new in v2 and old not in v2 and v1.replace(old,new)==v2

lines=(SRC/"results_k23_direct23.json.samples.tsv").read_text().splitlines();assert len(lines)==258
seen=set();counts=[0]*4;fallback=[]
for line in lines[1:]:
 c=line.split("\t");assert len(c)==20;g,o,ri=map(int,c[:3]);assert o not in seen;seen.add(o);counts[g]+=1
 assert ri==o*484//256 and int(c[15])!=0 and int(c[18])!=0
 if g!=o%4:fallback.append((o,ri,o%4,g))
assert seen==set(range(257)) and counts==[66,64,64,63] and fallback==[(227,429,3,0)]
independent=load(HERE/"results_k23_direct23_samples_independent.json")
assert independent["status"]=="PASS_INDEPENDENT_K23_DIRECT23_LITERAL_SAMPLE_REPLAY"
assert independent["witnesses"]==independent["source_membership_replays"]==independent["literal_terminal_replays"]==257
assert independent["literal_intermediate_replays"]==194 and independent["terminal_children_exhaustively_checked"]==11836
assert independent["group_counts"]==counts and len(independent["fallbacks"])==1

payload={
 "status":"PASS_INDEPENDENT_K23_DIRECT23_23_OF_59_INTEGRATION_REFEREE","degree":23,"covered_ids":23,"required_ids":59,"remaining_ids":36,"scalar_groups":4,
 "dag":{"path":str(DAG.relative_to(ROOT)),"sha256":sha(DAG),"logical_sha256":dag["logical_sha256"],"exact_id_equality":True},
 "evidence":{"result_sha256":sha(SRC/"results_k23_direct23.json"),"samples_sha256":sha(SRC/"results_k23_direct23.json.samples.tsv"),"source_manifest_sha256":sha(SRC/"k23_direct23_fragment_manifest.json"),"shard_sha256":dict(zip(shard_names,shard_pins)),"all_rehashed":True},
 "arithmetic":{"subtotal_scaled_U":str(scalar_once),"subtotal":"-82288431616/35","group_scalar_once":True,"hostile_per_id_multiplication_rejected":True,"full_equals_irreducible":True,"shard_additivity_rechecked":True},
 "revision_boundary":{"v1_sha256":sha(SRC/"run_k23_direct23_source_fold_v1.rs"),"v2_sha256":sha(SRC/"run_k23_direct23_source_fold.rs"),"only_sample_selection_line_changed":True,"scalar_path_unchanged":True,"single_fallback":[227,429,3,0]},
 "witness_referee":{"result_path":str((HERE/"results_k23_direct23_samples_independent.json").relative_to(ROOT)),"result_sha256":sha(HERE/"results_k23_direct23_samples_independent.json"),"source_membership_replays":257,"terminal_tails_checked":11836,"scope":"sample-only independent physical source membership and literal recurrence replay; not a second 485-record scalar pass"},
 "strict_partial":{"manifest_path":str((HERE/"k23_manifest_direct23_23_of_59.json").relative_to(ROOT)),"manifest_sha256":sha(HERE/"k23_manifest_direct23_23_of_59.json"),"result_path":str((HERE/"results_k23_direct23_23_of_59_partial.json").relative_to(ROOT)),"result_sha256":sha(HERE/"results_k23_direct23_23_of_59_partial.json"),"official_assembler_sha256":sha(SCHED/"assemble_k23_59_exact.py"),"complete_K23_claim":False},
 "scope":"independent direct23 evidence, sample boundary, and strict partial integration only; no heavy scalar rerun, no additional K23 IDs, rows, K24, membership, or conjecture claim"}
logical=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest();payload["logical_sha256"]=logical
(HERE/"results_k23_direct23_independent_integration_audit.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":payload["status"],"logical_sha256":logical,"subtotal":payload["arithmetic"]["subtotal"]},indent=2))
