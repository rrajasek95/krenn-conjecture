#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,math,os
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def req(x,d):
 if not x:raise RuntimeError(d)

ap=argparse.ArgumentParser();ap.add_argument("--output",type=Path);ns=ap.parse_args()
bplan=json.loads((HERE/"k24_B20_production_plan_103.json").read_text());cplan=json.loads((HERE/"k24_charge_production_plan_83.json").read_text())
req(len(bplan["shards"])==103 and len(cplan["shards"])==83,"shard counts")
req(bplan["required_groups"]==cplan["required_groups"] and bplan["required_ids"]==cplan["required_ids"],"contracts")
req(len(cplan["required_ids"])==len(set(cplan["required_ids"]))==35,"35 IDs")
for plan in (bplan,cplan):
 for x in plan["contract_files"].values():req(sha(ROOT/x["path"])==x["sha256"],x["path"])
 by={}
 for s in plan["shards"]:by.setdefault(s["family_id"],[]).append(s["interval"])
 for fid,z in by.items():
  total=(cplan["engines"][fid]["source_units"] if plan is cplan else next(v for v in bplan["shards"] if v["family_id"]==fid)["interval"][1] if False else None)
  z.sort();req(z[0][0]==0 and all(z[i][1]==z[i+1][0] for i in range(len(z)-1)),("gap",fid))
  source_total=cplan["engines"][fid]["source_units"];req(z[-1][1]==source_total,(fid,z[-1],source_total))

controls={
 "hidden_collected_k18":"acceptance_control_hidden18.json","hidden_decorated_k16_pair":"acceptance_control_hidden_pair.json",
 "k14_source_formula":"acceptance_control_k14.json","grouped_direct_k15_source":"acceptance_control_k15.json",
 "grouped_direct_k16_rows":"acceptance_control_k16.json","direct_D17_D18_formula":"acceptance_control_direct17.json"}
covered=[];acceptance_hashes={}
charge_schema=json.loads((HERE/"k24_charge_shard_acceptance.schema.json").read_text())
req(set(charge_schema["required"])==set(charge_schema["properties"]),"charge schema keyset")
for fid,name in controls.items():
 p=HERE/name;z=json.loads(p.read_text());acceptance_hashes[fid]=sha(p)
 req(set(z)==set(charge_schema["required"]),("charge schema/result",fid))
 req(z["format"]=="orbit0-k24-charge-shard-acceptance-v1" and z["status"]=="PASS_CONTROL" and z["control"] is True,fid)
 req(z["family_id"]==fid and z["group_ids"]==cplan["engines"][fid]["group_ids"],fid)
 req(sha(ROOT/z["raw_result"]["path"])==z["raw_result"]["sha256"],fid)
 req(sha(ROOT/z["literal_witnesses"]["path"])==z["literal_witnesses"]["sha256"],fid)
 req(sha(ROOT/z["engine"]["source_path"])==z["engine"]["source_sha256"] and sha(ROOT/z["engine"]["binary_path"])==z["engine"]["binary_sha256"],fid)
 req(z["universal_terminality"] and z["full_equals_irreducible"],fid)
 for g in z["groups"]:covered.extend(g["ids"])
req(sorted(covered)==cplan["required_ids"] and len(covered)==len(set(covered))==35,"control ID equality")
b_schema=json.loads((HERE/"k24_B20_source_shard.schema.json").read_text())
req(set(b_schema["required"])==set(b_schema["properties"]),"B schema keyset")

# Cross-referee the exact direct D17/D18 prefix against the sealed factorized producer.
new=json.loads((HERE/"control_v2_direct17_prefix1.json").read_text())
old=json.loads((ROOT/"computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/prefix1_fast/result.json").read_text())
ng={x["group_id"]:int(x["full_charge_scaled_U"]) for x in new["groups"]};og={x["group_id"]:int(x["derived_charge_scaled_U"]) for x in old["groups"]}
req(ng==og=={"source_D17_R3_4":825_568_674_132_787_200,"source_D18_R2_4":-85_322_827_196_006_400},(ng,og))

full_projection={
 "hidden_collected_k18":1204.789369,"hidden_decorated_k16_pair":4333.254861,"k14_source_formula":2008.432985,
 "grouped_direct_k15_source":4273.602192,"grouped_direct_k16_rows":23697.305650,"direct_D17_D18_formula":583.551783}
counts=cplan["minimality"]["family_shard_counts"]
req(all(counts[k]==math.ceil(v/450) for k,v in full_projection.items()),("not minimal",counts))
req(all(v/counts[k]<450 for k,v in full_projection.items()),"450 projection")

target=Fraction(829_424_811_081_283_712,173_867_925);scaled=target*400_591_699_200
req(scaled.denominator==1 and scaled.numerator==1_910_994_764_731_277_672_448,"target scale")
req(bplan["producer_status"]=={
 "direct_D17_D18_formula":"PREFIX_IMPLEMENTED_PRODUCTION_ALLOWLIST_REQUIRES_61_INTERVAL_SUPERSESSION",
 "hidden_collected_k18":"MISSING_B20_PRODUCER","hidden_decorated_k16_pair":"MISSING_B20_PRODUCER","k14_source_formula":"MISSING_B20_PRODUCER",
 "grouped_direct_k15_source":"MISSING_B20_PRODUCER","grouped_direct_k16_rows":"MISSING_B20_PRODUCER"},"B blockers")

result={"status":"PASS_K24_CHARGE_FIRST_PRODUCTION_INTERFACE","degree":24,"scale_U":400_591_699_200,
 "charge_target":f"{target.numerator}/{target.denominator}","charge_target_scaled_U":str(scaled.numerator),
 "charge_plan":{"path":str((HERE/"k24_charge_production_plan_83.json").relative_to(ROOT)),"sha256":sha(HERE/"k24_charge_production_plan_83.json"),"shards":83,"minimum_under_450_second_linear_gate":True},
 "B20_plan":{"path":str((HERE/"k24_B20_production_plan_103.json").relative_to(ROOT)),"sha256":sha(HERE/"k24_B20_production_plan_103.json"),"shards":103,"record_bytes":39},
 "coverage":{"groups":10,"ids":35,"missing":[],"duplicates":[],"extras":[]},"control_acceptance_sha256":acceptance_hashes,
 "direct_D17_D18_scalar_vs_factorized_prefix_equal":True,"universal_terminal_K4_guards":True,"all_controls_pass":True,
 "strict_schema_keysets_match_executable_validators":True,
 "charge_production_launched":False,"B20_production_launched":False,
 "launch_readiness":"CHARGE_SHARD0_READY_FOR_EXTERNAL_CLEARANCE; B20_BLOCKED",
 "B20_blockers":bplan["producer_status"],
 "scope":"charge-first and B20 source-production interfaces only; no complete K24 charge, relative closure, membership, or conjecture verdict"}
text=json.dumps(result,indent=2,sort_keys=True)+"\n"
if ns.output:
 out=ns.output.resolve();tmp=out.with_suffix(out.suffix+".tmp");tmp.write_text(text);os.replace(tmp,out)
print(json.dumps(result,sort_keys=True))
