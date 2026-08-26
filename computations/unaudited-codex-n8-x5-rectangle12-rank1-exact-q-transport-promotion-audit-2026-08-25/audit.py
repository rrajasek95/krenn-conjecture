#!/usr/bin/env python3
"""Bind exact-Q rank-one seals to the rectangle-12 transport theorem."""
import hashlib,json,os
from pathlib import Path
if not __debug__:raise RuntimeError("assertions required")
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];C=ROOT/"computations"
O0=C/"unaudited-codex-n8-x5-rectangle-rank1-orbit0-exact-q-run-2026-08-25"
R4=C/"unaudited-codex-n8-x5-rectangle-rank1-remaining4-exact-q-run-2026-08-25"
T=C/"unaudited-codex-n8-x5-rectangle12-transport-census-referee-2026-08-25"
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
PINS={O0/"FINAL_MANIFEST.sha256":"b129fdc2775a1fadb5659409ed9f953351cb47d591cef4fc50f5a09276bfbc07",O0/"AUDIT_RESULT.json":"4da4bf9c09cf10480eb8b79aa4d24a29a5c6d75749ae9d652e1b9eb9b1377b07",R4/"FINAL_MANIFEST.sha256":"1a5997c4ea599c8c25777e24027b9b90e4259aa7a0f72cc7c4ed93da3cb6626f",R4/"FINAL_AUDIT.json":"6e6c47fa91de6e26e089c1af63d2d5091609a5e9c4e8fca2a44f51576e613ec7",R4/"BATCH_RESULT.json":"f49758f2522ab427542706df07775f54d0d2a3c04a537776f6623cb9d0a23ab2",T/"MANIFEST.sha256":"fa72101042aa2d179745f3e17475dae3c654c0445bc7433ab5ae4e22df3e5e5d",T/"results_referee.json":"e1660ab4671b8de68acdc4fe2a32e90e68ed1a489accf62d6961f9e6bc094fd7"}
def write(p,x):
 q=p.with_suffix('.json.tmp');q.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');os.replace(q,p)
def main():
 for p,w in PINS.items():assert sha(p)==w,(p,sha(p),w)
 o=json.loads((O0/"AUDIT_RESULT.json").read_text());a=json.loads((R4/"FINAL_AUDIT.json").read_text());b=json.loads((R4/"BATCH_RESULT.json").read_text());t=json.loads((T/"results_referee.json").read_text())
 assert o["status"]=="PASS_UNIT_IDEAL_EXACT_Q_RANK1_ORBIT0_ONLY" and o["field"]=="Q" and o["unit_remainder"]==0 and o["chart"]["orbit"]==0
 assert a["status"]=="PASS_ALL_FOUR_EXACT_Q_UNIT_IDEALS" and a["exact_order"]==[1,2,3,4] and a["rank1_canonical_family_closed"] and not a["rank2_closed"]
 assert b["status"]=="PASS_ALL_FOUR_UNIT_IDEALS" and b["attempted_orbits"]==[1,2,3,4] and b["unattempted_orbits"]==[] and b["rank1_family_closed_with_orbit0"]
 assert [x["orbit"] for x in a["lanes"]]==[1,2,3,4] and all(x["status"]=="UNIT_IDEAL" for x in a["lanes"])
 assert t["status"]=="PASS_EXACT_TRANSPORT_WITH_SELECTED_CARRIER_SCOPE_AND_CURRENT_CLOSURE_LEDGER"
 s=t["support_census"];assert s["classes"]==[[0,1,4,5,8,9],[2,3,6,7,10,11]] and s["unique_within_class"] and s["cross_class_maps"]==0
 assert t["A12_reduced_ideal_audit"]["reduced_rank_ideal_A12_free"] and t["literal_transport"]["word_transports"]==472392
 result={"schema":"KRENN_X5_RECTANGLE12_RANK1_EXACT_Q_TRANSPORT_PROMOTION_AUDIT_V1","status":"PASS_ALL_RANK1_ORBITS_EXACT_Q_CLOSED_ACROSS_12_RECTANGLE_RECORDS","exact_Q_orbits":[0,1,2,3,4],"canonical_orbits":5,"raw_charts_per_record":27,"rectangle_records":list(range(12)),"canonical_record_orbit_cases":60,"raw_chart_record_cases":324,"A12_lifts":{"present_records":[0,1,4,5,8,9],"absent_records":[2,3,6,7,10,11],"selected_reduced_ideal_A12_free":True,"both_lifts_closed":True},"theorem":"Exact-Q unit ideals for all five canonical rank-one charts are preserved by the sealed literal source/ring transports. The selected reduced ideal is A12-free, so the two A12 lifts are identical at the ideal level and all twelve rectangle records close in rank one.","scope":{"rank1_rectangle12_closed":True,"rank2_closed":False,"nonrectangle_records_excluded":[12,13,14,15],"full_conjecture":False,"new_solver_runs":0},"pins":{str(p.relative_to(ROOT)):w for p,w in PINS.items()}}
 write(HERE/"results_promotion_audit.json",result);print(json.dumps({"status":result["status"],"orbits":5,"records":12,"raw_cases":324,"solves":0},sort_keys=True))
if __name__=='__main__':main()
