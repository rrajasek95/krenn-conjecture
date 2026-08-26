#!/usr/bin/env python3
"""Fail-closed audit of the bounded D10 result and D11 closure-only control."""
import argparse,hashlib,json,os
from pathlib import Path

PINS={
 "base_source":"241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0",
 "production_source":"7a2f5e6c23535e005ac4a6ebc63c50d35a57dedc173103b1c120a8dff9afa628",
 "repeated_probe_source":"b42a41e97e52117c2d115fe253c3a620c94e52fa41c34d34ebd7dd9367dda60f",
 "binary":"2d7b1925a90ba6e90ba9a4f9d17374096fc6814bb1d276a446a03211a84e4d18",
 "input":"75a82d82a979d75507e682fd339e83d4ae35949653d624fb541148bd3957dcff",
 "d10_closure":"2a05d97ce8d58d9d25ac8fddd01eba2ff87b2367949f6d573c0923ea653e4fa2",
 "d10_dual":"27b47b61238044c739daa5941ad80782d249cdea4e115e07043472b507eb0d87",
 "d11_closure":"2d9c7b2907b813834ed226c258a7f681fdd6cb8836cff9ad74c148eb1e76ef6f",
 "d11_interrupted":"ba6219b5c99c0caa39798113bbb6cfef1667833918af3e63a32a37e29d88dc28",
}
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()
def ck(x,m):
 if not x:raise ValueError(m)
def fields(r,names):return {k:r[k] for k in names}
def main():
 p=argparse.ArgumentParser()
 for x in ["base_source","source","control_source","binary","input","d10_result","d10_closure","d10_dual","d10_reference_result","d10_reference_closure","d10_reference_dual","d11_result","d11_closure","d11_reference_result","d11_reference_closure","d11_interrupted"]:p.add_argument("--"+x.replace('_','-'),dest=x,required=True)
 p.add_argument("--output");a=p.parse_args()
 for name,path in [("base_source",a.base_source),("production_source",a.source),("repeated_probe_source",a.control_source),("binary",a.binary),("input",a.input),("d10_closure",a.d10_closure),("d10_dual",a.d10_dual),("d11_closure",a.d11_closure),("d11_interrupted",a.d11_interrupted)]:ck(sha(path)==PINS[name],name+" pin mismatch")
 ck(sha(a.d10_reference_closure)==PINS["d10_closure"] and sha(a.d10_reference_dual)==PINS["d10_dual"],"D10 reference mismatch")
 ck(sha(a.d11_reference_closure)==PINS["d11_closure"],"D11 reference mismatch")
 ck(os.path.getsize(a.d11_closure)==os.path.getsize(a.d11_reference_closure)==51_332_134,"D11 complete checkpoint size mismatch")
 d10=json.load(open(a.d10_result));r10=json.load(open(a.d10_reference_result));d11=json.load(open(a.d11_result));r11=json.load(open(a.d11_reference_result))
 algebra=["status","degree","prime","closure_complete","row_orbits","column_orbits","rank","matrix_nnz","target_residual_nnz","target_pairing","member_mod_prime"]
 ck(fields(d10,algebra)==fields(r10,algebra),"D10 algebraic result mismatch");ck(d10["status"]=="COMPLETE_NONMEMBER_MOD_PRIME","D10 not terminal");ck(d10["elapsed_seconds"]<300 and d10["peak_rss_kib"]<8*1024*1024,"D10 resource gate failed")
 ck(d10["memo_probe_candidates"]==0 and d10["memo_global_state"]==0,"D10 memo should remain ineligible")
 ck(d11["status"]=="INCOMPLETE_RESOURCE_GATE" and d11["incomplete_reason"]=="WALL_CAP" and d11["closure_complete"] is True,"D11 control scope mismatch")
 ck((d11["row_orbits"],d11["column_orbits"])==(r11["row_orbits"],r11["column_orbits"])==(3_722_556,195_924),"D11 closure counts mismatch")
 ck(all(d11[k]==-1 for k in ["rank","matrix_nnz","target_residual_nnz","target_pairing"]) and d11["member_mod_prime"] is None,"D11 linear fields improperly accepted")
 ck(d11["elapsed_seconds"]<300 and d11["peak_rss_kib"]<8*1024*1024,"D11 resource gate failed")
 ck(d11["memo_enabled_workers"]==0 and d11["memo_fallback_workers"]==400 and d11["memo_probe_hits"]*10<d11["memo_probe_candidates"]*9,"D11 repeated-probe rejection mismatch")
 ck(PINS["d11_interrupted"]!=PINS["d11_closure"] and os.path.getsize(a.d11_interrupted)!=51_332_134,"interrupted checkpoint confused with complete checkpoint")
 out={"status":"PASS","d10":{"scope":"complete_degree_result","closure_sha_equal":True,"dual_sha_equal":True,"algebra_equal":True,"elapsed_seconds":d10["elapsed_seconds"],"peak_rss_kib":d10["peak_rss_kib"],"reference_elapsed_seconds":r10["elapsed_seconds"],"reference_peak_rss_kib":r10["peak_rss_kib"]},"d11":{"scope":"closure_only","closure_sha_equal":True,"closure_size":51_332_134,"counts_equal":True,"process_elapsed_seconds":d11["elapsed_seconds"],"peak_rss_kib":d11["peak_rss_kib"],"linear_result_accepted":False,"dual_accepted":False,"verdict":"NONPROMOTION_FULL_DEGREE"},"production_verdict":"D10_PROMOTABLE_GATE_D11_CLOSURE_ONLY_NO_BROAD_D12","broad_d12_authorized":False}
 if a.output:Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
