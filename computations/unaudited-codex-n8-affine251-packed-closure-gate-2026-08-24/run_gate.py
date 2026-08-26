#!/usr/bin/env python3
"""Isolated-process benchmark orchestrator with direct RSS sampling."""
import argparse, hashlib, json, platform, statistics, subprocess
from pathlib import Path

def run_sampled(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode: raise RuntimeError({"cmd":cmd,"returncode":proc.returncode,"stderr":proc.stderr})
    value=json.loads(proc.stdout); value["command"]=cmd
    return value

def run_repeated(cmd, timing_field, repetitions):
    values=[run_sampled(cmd) for _ in range(repetitions)]
    signature={(x["output_count"],x["sorted_sha256"]) for x in values}
    if len(signature)!=1: raise RuntimeError("nondeterministic repeated output")
    answer=dict(values[0]); answer[timing_field]=statistics.median(x[timing_field] for x in values)
    answer["timing_repetitions_seconds"]=[x[timing_field] for x in values]
    answer["peak_rss_kib"]=max(x["peak_rss_kib"] for x in values)
    answer["repetitions"]=repetitions
    return answer

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(8<<20),b""):h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument("--binary",required=True);p.add_argument("--checkpoint",required=True);p.add_argument("--output",required=True);p.add_argument("--workers",type=int,default=8);a=p.parse_args()
    binary=str(Path(a.binary).resolve()); checkpoint=str(Path(a.checkpoint).resolve()); runs=[]
    selftest=subprocess.run([binary,"selftest"],capture_output=True,text=True,check=True);selftest=json.loads(selftest.stdout)
    for n in (100_000,1_000_000):
        stage=[]
        for kind in ("row","column"):
            old=run_repeated([binary,"bench",checkpoint,kind,"hashset",str(n),"1"],"dedup_seconds",7)
            new=run_repeated([binary,"bench",checkpoint,kind,"packed",str(n),str(a.workers)],"dedup_seconds",7)
            if (old["output_count"],old["sorted_sha256"]) != (new["output_count"],new["sorted_sha256"]): raise RuntimeError("exact backend mismatch")
            new["throughput_ratio_vs_hashset"]=old["dedup_seconds"]/new["dedup_seconds"]
            new["rss_ratio_vs_hashset"]=new["peak_rss_kib"]/old["peak_rss_kib"]
            stage += [old,new]
        runs += stage
        if n==100_000 and (max(x["peak_rss_kib"] for x in stage)>2*1024*1024 or max(x["dedup_seconds"] for x in stage)>120): break
    canon=[]
    for n in (10_000,100_000):
        old=run_repeated([binary,"canon",checkpoint,"exact_cache",str(n)],"seconds",3)
        new=run_repeated([binary,"canon",checkpoint,"orbit_memo",str(n)],"seconds",3)
        if (old["output_count"],old["sorted_sha256"]) != (new["output_count"],new["sorted_sha256"]): raise RuntimeError("canonical backend mismatch")
        new["throughput_ratio_vs_exact_cache"]=old["seconds"]/new["seconds"]
        canon += [old,new]
        if n==10_000 and (max(old["seconds"],new["seconds"])>120 or max(old["peak_rss_kib"],new["peak_rss_kib"])>2*1024*1024): break
    result={"status":"PASS","scope":"bounded_optimization_gate_only","checkpoint":{"path":checkpoint,"sha256":sha(checkpoint)},"binary":{"path":binary,"sha256":sha(binary)},"host":platform.platform(),"workers":a.workers,"workload":{"distributed_blocks":16,"unique_fraction":"4/5","duplicate_fraction":"1/5"},"selftest":selftest,"dedup_runs":runs,"canonicalization":{"gap_available":False,"alternative":"exact_full_orbit_memo","runs":canon},"promotion_rule":{"required":"exact equality and (>2x throughput or material RSS win)","broad_run_authorized":False}}
    Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","output":a.output,"dedup_runs":len(runs),"canonical_runs":len(canon)}))
if __name__=="__main__":main()
