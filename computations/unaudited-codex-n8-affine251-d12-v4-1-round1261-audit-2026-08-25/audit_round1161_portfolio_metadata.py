#!/usr/bin/env python3
"""Lightweight, no-cache-read referee of sealed round1161 portfolio/cap gate."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PKG=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1161-portfolio-cap1250-gate-2026-08-25"
MANIFEST="d05e1ff544bae130ca960fd1fc6c454f96bb137953d21a3d27628026dc2f44f0";CP="e7d53052997394ee43d110ead3b74d72cba97773df9076a5eff7dab8033d143a";VEC="0df2928faf351531f04b936afc06d6a7d8a105f9330ef7200322ca78f257e6c3";SOURCE="2cf629054e1b5e2350617b71114544b7d0c7a47f811b67b6dea4483e5e911230";BINARY="ade47c27a96314bb4391241a60a372c79e643a44b8a62a00054fffc576ccc7ce";WATCH="53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(x,m):
 if not x:raise SystemExit("REJECT: "+m)
need(sha(PKG/"MANIFEST.sha256")==MANIFEST,"manifest pin")
audit=load(PKG/"results_round1161_audit.json");need(audit["schema"]=="KRENN_AFFINE251_D12_ROUND1161_PORTFOLIO_CAP1250_AUDIT_V1" and audit["status"]=="PASS_EXACT_ROUND1161_PORTFOLIO_AND_CONDITIONAL_CAP_EQUIVALENCE","audit status")
need(audit["production_source_mutated"] is False and audit["continued_beyond_round1161"] is False,"scope")
need((audit["output"]["round"],audit["output"]["columns"],audit["output"]["support"],audit["output"]["new_columns"],audit["output"]["new_support_rows"])==(1161,961803,998,2297,522),"output census")
need(audit["output_checkpoint_sha256"]==CP and audit["output_vectors_sha256"]==VEC,"output pins")
need(audit["input"]["poincare_manifest_sha256"]=="e56759b60118d50402af20041477c93a2e0ac317556c7fd94b0cdf4d490e2c42" and audit["input"]["checkpoint_sha256"].startswith("23d91d21") and audit["input"]["vectors_sha256"].startswith("e622054e"),"input provenance")
control,candidate=load(PKG/"selected_control/result.json"),load(PKG/"cap1250_candidate/result.json")
def semantic(v):
 v=json.loads(json.dumps(v))
 for k in ("elapsed_seconds","peak_rss_kib","restore_seconds","vector_cache_write_seconds","checkpoint","vector_cache","dual","column_cap"):v.pop(k,None)
 for r in v["rounds"]:
  for k in ("incident_seconds","materialize_seconds","solve_seconds"):r.pop(k,None)
 return v
need(semantic(control)==semantic(candidate),"cap semantic equality")
need((control["column_cap"],candidate["column_cap"])==(1000000,1250000),"cap values")
def normcmd(c):
 c=list(c);c[0]="<binary>"
 for flag in ("--output","--checkpoint","--vector-cache","--dual"):
  c[c.index(flag)+1]="<artifact>"
 return c
cw,kw=load(PKG/"selected_control/watchdog.json"),load(PKG/"cap1250_candidate/watchdog.json")
for w in (cw,kw):need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"] and (w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"])==(SOURCE,BINARY,WATCH),"watchdog")
c1,c2=normcmd(cw["command"]),normcmd(kw["command"]);i=c1.index("--column-cap")+1;need(c1[:i]+c1[i+1:]==c2[:i]+c2[i+1:] and (c1[i],c2[i])==("1000000","1250000"),"only cap command difference")
need(audit["artifact_sha256"]["selected_control/checkpoint.bin"]==audit["artifact_sha256"]["cap1250_candidate/checkpoint.bin"]==CP and audit["artifact_sha256"]["selected_control/vectors.bin"]==audit["artifact_sha256"]["cap1250_candidate/vectors.bin"]==VEC,"ledger equality")
out={"schema":"KRENN_AFFINE251_D12_ROUND1161_PORTFOLIO_METADATA_REFEREE_V1","status":"PASS_LIGHTWEIGHT_ROUND1161_PORTFOLIO_CAP_PROVENANCE","scope":"Small manifests/JSON/logs only; checkpoint/cache payloads deliberately not opened during active production.","input":{"round":1160,"checkpoint_sha256":audit["input"]["checkpoint_sha256"],"vectors_sha256":audit["input"]["vectors_sha256"],"sealed_manifest_sha256":audit["input"]["poincare_manifest_sha256"]},"output":{"round":1161,"columns":961803,"support":998,"checkpoint_sha256":CP,"vectors_sha256":VEC},"selection":{"pivot":"rare","strategy":"cold","portfolio_tasks":6},"cap_gate":{"baseline":1000000,"promoted":1250000,"only_normalized_command_difference":True,"semantic_result_equal":True,"producer_ledger_reports_checkpoint_cache_byte_equal":True},"pins":{"manifest_sha256":MANIFEST,"audit_result_sha256":sha(PKG/"results_round1161_audit.json"),"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog_sha256":WATCH},"large_io_performed":False,"payload_equality_scope":"Deferred independent payload hashing to final chain audit after FINAL_REPLAY_CLEAR."}
tmp=HERE/"results_round1161_portfolio_metadata_audit.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_round1161_portfolio_metadata_audit.json")
