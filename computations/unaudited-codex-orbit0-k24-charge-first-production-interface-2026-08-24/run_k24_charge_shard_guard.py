#!/usr/bin/env python3
"""Launch exactly one sealed charge shard with wall/address-space/disk guards."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, resource, shutil, subprocess, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PLAN=HERE/"k24_charge_production_plan_83.json"
PHYS=HERE/"run_k24_charge_physical"
HIDDEN=HERE/"run_k24_charge_hidden"
LIMIT=8_589_934_592

def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument("shard_id");ap.add_argument("output",type=Path);ap.add_argument("resource",type=Path);ns=ap.parse_args()
 plan=json.loads(PLAN.read_text());match=[x for x in plan["shards"] if x["shard_id"]==ns.shard_id]
 if len(match)!=1:raise RuntimeError("unknown/duplicate shard id")
 s=match[0];eng=plan["engines"][s["family_id"]];binary=PHYS if eng["engine_kind"]=="physical" else HIDDEN
 if ns.output.exists() or ns.resource.exists():raise RuntimeError("refuse overwrite")
 free=shutil.disk_usage(ROOT).free
 if free<17_179_869_184:raise RuntimeError(("disk floor",free))
 a,b=s["interval"]
 cmd=[str(binary),"--family",eng["engine_family"],"--start",str(a),"--count",str(b-a),"--workers","8","--output",str(ns.output)]
 def limit():
  resource.setrlimit(resource.RLIMIT_AS,(LIMIT,LIMIT))
 begun=time.monotonic();ok=False
 try:
  z=subprocess.run(cmd,cwd=ROOT,timeout=600,check=False,preexec_fn=limit)
  ok=z.returncode==0 and ns.output.is_file() and not ns.output.with_suffix(ns.output.suffix+".tmp").exists()
 except subprocess.TimeoutExpired as e:
  raise RuntimeError("hard 600-second timeout") from e
 wall=time.monotonic()-begun
 rss=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
 if platform.system()!="Darwin":rss*=1024
 evidence={"wall_seconds":wall,"peak_RSS_bytes":rss,"free_bytes_before":free,"exit_code":z.returncode,"atomic_result":ok}
 if not ok or wall>=600 or rss>=LIMIT:raise RuntimeError(evidence)
 tmp=ns.resource.with_suffix(ns.resource.suffix+".tmp");tmp.write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n");os.replace(tmp,ns.resource)
 print(json.dumps({"status":"PASS_GUARDED_SHARD","shard_id":ns.shard_id,"result_sha256":sha(ns.output),"resource":evidence},sort_keys=True))
if __name__=="__main__":main()
