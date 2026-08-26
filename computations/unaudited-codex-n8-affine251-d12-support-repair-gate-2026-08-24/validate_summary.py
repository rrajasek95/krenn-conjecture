#!/usr/bin/env python3
"""Fail-closed acceptance validator for the sealed repair gate summaries."""
import argparse,json
from pathlib import Path
def ck(x,m):
 if not x:raise ValueError(m)
def validate(raw,audit):
 ck(raw["schema"]=="KRENN_AFF251_D12_SUPPORT_REPAIR_GATE_V1" and raw["status"]=="PASS_BOUNDED_GATE","raw schema")
 ck((raw["round730_columns"],raw["round731_columns"],raw["new_columns"],raw["round730_support"],raw["reference_support"],raw["reference_frontier"])==(314080,315301,1221,484,499,1268),"raw census")
 ck(raw["elapsed_seconds"]<120 and raw["peak_rss_kib"]<8*1024*1024 and raw["continued_beyond_round731"] is False,"resource/scope gate")
 ck(len(raw["outcomes"])==2 and {x["label"] for x in raw["outcomes"]}=={"previous_plus_new_only","previous_plus_new_union"},"outcome scope")
 for x in raw["outcomes"]:ck(x["consistent"] is True and x["full_violations"]==0 and x["support"]==1688 and x["frontier"]==10466 and raw["baseline_solve_seconds"]/x["solve_seconds"]>2,"outcome mismatch")
 ck(audit["schema"]=="KRENN_AFF251_D12_SUPPORT_REPAIR_AUDIT_V1" and audit["status"]=="PASS","audit schema")
 ck(audit["equations_replayed"]==315301 and audit["vector_entries_replayed"]==31973746 and audit["repair_violations"]==audit["reference_violations"]==0,"replay mismatch")
 ck(audit["candidate_variants_equal"] is True and audit["frontier_variants_equal"] is True,"variant mismatch")
 ck(audit["frontier_ratio"]>1 and audit["promotion"] is False and audit["verdict"]=="REJECT_FRONTIER_REGRESSION" and audit["continued_beyond_round731"] is False,"verdict mismatch")
 return {"status":"PASS","exact_equations":315301,"exact_vector_entries":31973746,"promotion":False,"verdict":"REJECT_FRONTIER_REGRESSION","active_computation":False}
def main():
 p=argparse.ArgumentParser();p.add_argument("--raw",required=True);p.add_argument("--audit",required=True);p.add_argument("--output");a=p.parse_args();out=validate(json.load(open(a.raw)),json.load(open(a.audit)))
 if a.output:Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
