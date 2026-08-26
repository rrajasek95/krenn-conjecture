#!/usr/bin/env python3
"""Fail-closed semantic audit for the bounded packed-closure gate."""
import argparse, hashlib, json
from pathlib import Path

EXPECTED_CHECKPOINT="d9f3a71525b2a5070d9e911b12f313a0d20e0d1763c3e3adfaa1294cb638f241"
TOP={"binary","canonicalization","checkpoint","host","promotion_rule","scope","selftest","status","workers","workload","dedup_runs"}

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(8<<20),b""):h.update(block)
    return h.hexdigest()

def check(cond,msg):
    if not cond: raise ValueError(msg)

def audit(r,h,binary,checkpoint):
    check(set(r)==TOP,"top-level schema mismatch")
    check(r["status"]=="PASS" and r["scope"]=="bounded_optimization_gate_only","status/scope mismatch")
    check(r["checkpoint"]["sha256"]==EXPECTED_CHECKPOINT==sha(checkpoint),"checkpoint hash mismatch")
    check(r["binary"]["sha256"]==sha(binary),"binary hash mismatch")
    check(r["workers"]==8 and r["workload"]=={"distributed_blocks":16,"duplicate_fraction":"1/5","unique_fraction":"4/5"},"workload contract mismatch")
    check(r["promotion_rule"]["broad_run_authorized"] is False,"broad run improperly authorized")
    check(r["selftest"]["status"]=="PASS" and len(r["selftest"]["cases"])==7 and "legacy_layout_13_16" in r["selftest"]["cases"],"engine selftest mismatch")
    runs=r["dedup_runs"];check(len(runs)==8,"dedup run cardinality mismatch")
    promoted=[]
    for n in (100_000,1_000_000):
      for kind in ("row","column"):
        pair=[x for x in runs if x["candidates"]==n and x["kind"]==kind]
        check(len(pair)==2,"missing/duplicate dedup backend")
        old=next(x for x in pair if x["backend"]=="hashset");new=next(x for x in pair if x["backend"]=="packed_parallel_sort")
        check(old["output_count"]==new["output_count"]==n*4//5,"dedup count mismatch")
        check(old["sorted_sha256"]==new["sorted_sha256"] and len(old["sorted_sha256"])==64,"dedup digest mismatch")
        check(old["repetitions"]==new["repetitions"]==7 and len(old["timing_repetitions_seconds"])==len(new["timing_repetitions_seconds"])==7,"timing repetition mismatch")
        ratio=old["dedup_seconds"]/new["dedup_seconds"]
        check(abs(ratio-new["throughput_ratio_vs_hashset"])<1e-12,"throughput ratio mismatch")
        check(abs(new["peak_rss_kib"]/old["peak_rss_kib"]-new["rss_ratio_vs_hashset"])<1e-12,"RSS ratio mismatch")
        if ratio>2 or new["peak_rss_kib"]<=old["peak_rss_kib"]*.8: promoted.append(f"{kind}:{n}")
    c=r["canonicalization"];check(c["gap_available"] is False and c["alternative"]=="exact_full_orbit_memo","canonical method mismatch")
    check(len(c["runs"])==4,"canonical run cardinality mismatch")
    for n in (10_000,100_000):
        pair=[x for x in c["runs"] if x["candidates"]==n];check(len(pair)==2,"canonical pair mismatch")
        old=next(x for x in pair if x["backend"]=="exact_cache");new=next(x for x in pair if x["backend"]=="orbit_memo")
        check(old["actions"]==new["actions"]==1440 and old["base_orbits"]==new["base_orbits"]==256,"canonical scope mismatch")
        check(old["output_count"]==new["output_count"]==n and old["sorted_sha256"]==new["sorted_sha256"],"canonical exact equality mismatch")
        check(old["repetitions"]==new["repetitions"]==3,"canonical repetition mismatch")
        check(abs(old["seconds"]/new["seconds"]-new["throughput_ratio_vs_exact_cache"])<1e-12,"canonical ratio mismatch")
    check(h["status"]=="PASS" and h["fail_closed"] is True and len(h["cases"])==7 and all(h["cases"].values()),"hostile suite mismatch")
    check(set(promoted)=={"row:100000","column:100000","row:1000000","column:1000000"},"promotion threshold outcome changed")
    return {"status":"PASS","checkpoint_sha256":EXPECTED_CHECKPOINT,"binary_sha256":r["binary"]["sha256"],"exact_pairs":6,"promotion":"bounded_integration_only","promoted_dedup_gates":sorted(promoted),"orbit_memo":"exact_but_cap_required","broad_run_authorized":False}

def main():
    p=argparse.ArgumentParser();p.add_argument("--results",required=True);p.add_argument("--hostiles",required=True);p.add_argument("--binary",required=True);p.add_argument("--checkpoint",required=True);p.add_argument("--output");a=p.parse_args()
    out=audit(json.load(open(a.results)),json.load(open(a.hostiles)),a.binary,a.checkpoint)
    if a.output:Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
