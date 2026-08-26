#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location("contract",HERE/"k24_production_contract.py");c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
rejected=[]
def reject(name,fn):
 try:fn()
 except Exception:rejected.append(name)
 else:raise RuntimeError(("hostile accepted",name))

raw=json.loads((HERE/"prefix8_direct17.json").read_text());x=c.families()["direct_D17_D18_formula"]
c.charge_groups(raw,x)
z=json.loads(json.dumps(raw));z["extra"]=1;reject("charge_extra_top",lambda:c.charge_groups(z,x))
z=json.loads(json.dumps(raw));z.pop("scope");reject("charge_missing_top",lambda:c.charge_groups(z,x))
z=json.loads(json.dumps(raw));z["groups"][0]["full_charge_scaled_U"]="1";reject("charge_full_irr",lambda:c.charge_groups(z,x))
z=json.loads(json.dumps(raw));z["groups"][0]["ids"]=["wrong"];reject("charge_wrong_ids",lambda:c.charge_groups(z,x))
reject("interval_gap",lambda:c.interval_guard([[0,1],[2,3]],3));reject("interval_overlap",lambda:c.interval_guard([[0,2],[1,3]],3))

def rec(word,mult,orbit,mass):return bytes([word])+mult+orbit.to_bytes(2,"little")+mass.to_bytes(16,"little",signed=True)
with tempfile.TemporaryDirectory(dir=HERE) as td:
 d=Path(td);m=bytes(20);a=d/"a.bin";b=d/"b.bin";out=d/"out.bin"
 a.write_bytes(rec(0,m,384,384));b.write_bytes(rec(0,m,384,768)+rec(1,m,384,384))
 q=c.merge_records([a,b],out);assert q["records"]==2 and q["exact_zero_cancellations"]==0
 bad=d/"bad.bin";bad.write_bytes(rec(1,m,384,384)+rec(0,m,384,384));reject("B_unsorted",lambda:c.merge_records([bad],d/"u.bin"))
 bad.write_bytes(rec(0,m,192,192));reject("B_orbit_mismatch",lambda:c.merge_records([a,bad],d/"o.bin"))
 bad.write_bytes(rec(0,m,384,1));reject("B_inexact_orbit_division",lambda:c.merge_records([bad],d/"i.bin"))
 bad.write_bytes(rec(0,m,0,384));reject("B_zero_orbit",lambda:c.merge_records([bad],d/"z.bin"))

 plan=json.loads((HERE/"k24_B20_production_plan_103.json").read_text());shard=[s for s in plan["shards"] if s["family_id"]=="direct_D17_D18_formula"][0];pins=plan["producer_pins"][shard["family_id"]]
 wd=d/"words.tsv";wd.write_text("word_id\tnatural_word\n0\t00000022\n");wit=d/"w.tsv";wit.write_text("sample_bin\twitness\n0\tx\n")
 run=d/"run.bin";run.write_bytes(rec(0,m,384,384))
 rel=lambda p:str(p.resolve().relative_to(ROOT))
 expected=json.loads(c.CONTRACT.read_text())["groups"]
 manifest={"format":"orbit0-k24-B20-source-shard-v2","status":"PASS_CONTROL","degree":24,"scale_U":c.U,"family_id":shard["family_id"],"group_ids":shard["group_ids"],"covered_ids":[i for g in shard["group_ids"] for i in expected[g]],"source_interval":shard["interval"],"source_units":shard["source_units"],"input_sha256":plan["family_inputs"][shard["family_id"]],"engine_sha256":pins["source_sha256"],"provider_sha256":pins["provider_sha256"],"word_dictionary":{"path":rel(wd),"sha256":c.sha(wd),"records":1},"block_degrees":[20,22,23,24],"record_format":plan["record_contract"]["record_format"],"record_bytes":39,"natural_sort_key":plan["record_contract"]["natural_sort_key"],"group_runs":[],"literal_witnesses":{"path":rel(wit),"sha256":c.sha(wit),"records":1},"all_orbit_divisions_exact":True,"lower_blocks_exact":True,"top_block_exact":True,"arbitrary_source_words_preserved":True,"charge_groups":[],"atomic":True,"resource_evidence":None,"control":True,"scope":"synthetic schema control"}
 for gid in shard["group_ids"]:
  manifest["group_runs"].append({"group_id":gid,"path":rel(run),"sha256":c.sha(run),"records":1,"bytes":39,"selected_pivot_occurrences":1,"exact_zero_cancellations":0,"orbit_mass_scaled_U":"384"})
  manifest["charge_groups"].append({"group_id":gid,"ids":expected[gid],"full_charge_scaled_U":"0","irreducible_charge_scaled_U":"0"})
 mp=d/"manifest.json";mp.write_text(json.dumps(manifest));c.validate_B_manifest(mp,plan,shard,True)
 z=json.loads(json.dumps(manifest));z["extra"]=1;(d/"extra.json").write_text(json.dumps(z));reject("B_manifest_extra",lambda:c.validate_B_manifest(d/"extra.json",plan,shard,True))
 z=json.loads(json.dumps(manifest));z["covered_ids"][0]="wrong";(d/"ids.json").write_text(json.dumps(z));reject("B_manifest_wrong_ids",lambda:c.validate_B_manifest(d/"ids.json",plan,shard,True))
 reject("B_production_allowlist_not_ready",lambda:c.validate_B_manifest(mp,plan,shard,False))

assert len(rejected)==13,rejected
print(json.dumps({"status":"PASS_HOSTILE_K24_CHARGE_B20_CONTRACT","rejected":rejected,"count":len(rejected)},sort_keys=True))
