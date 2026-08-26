#!/usr/bin/env python3
"""Small-file provenance audit for the sealed round1343 cap1750 gate."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
PKG=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1343-cap1750-gate-2026-08-25"; MANIFEST=PKG/"MANIFEST.sha256"
def need(x,m):
 if not x: raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""): h.update(b)
 return h.hexdigest()
def load(p): return json.loads(p.read_text())
need(sha(MANIFEST)=="c07168d65ba9caa604bf38235b4ff9f5442b217fd82934c84f18f4f0c9665e9b","manifest pin")
entries={}
for line in MANIFEST.read_text().splitlines():
 d,n=line.split("  ",1); need(len(d)==64 and n not in entries,"manifest syntax/duplicate"); entries[n]=d
need(entries["results_round1343_cap_audit.json"]=="05dfa9b53820ebd916f79f17f5a0800dd49e4eff7b4407ed00b5e1ac53304c62","audit entry")
need(sha(PKG/"results_round1343_cap_audit.json")==entries["results_round1343_cap_audit.json"],"audit artifact")
a=load(PKG/"results_round1343_cap_audit.json"); need(a["status"]=="PASS_EXACT_CAP1500_TO_CAP1750_EQUIVALENCE","audit status")
cp="d2dbdee814cecca8f8528d84d2f386d3f042a54b62039a0350a834b5a1949dcf"; vc="d5517dfdc00cb7c2e0844b2459385576dd84211eceebe3a0cb94815a1cd7a2c6"
need(a["checkpoint_sha256"]==cp and a["vectors_sha256"]==vc,"selected state pins")
for label in ("cap1500_control","cap1750_candidate"):
 need(entries[label+"/checkpoint.bin"]==cp and entries[label+"/vectors.bin"]==vc,"manifest state equivalence")
 need(sha(PKG/label/"result.json")==entries[label+"/result.json"] and sha(PKG/label/"watchdog.json")==entries[label+"/watchdog.json"],"small artifacts "+label)
 r=load(PKG/label/"result.json"); w=load(PKG/label/"watchdog.json")
 need((r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"])==(1343,1496171,1949),"state header")
 need(r["rounds"][0]["selected_strategy"]=="cold" and r["rounds"][0]["selected_pivot"]=="rare","selection")
 need(w["status"]=="PASS" and w["breach"] is None and w["atomic_outputs_clean"],"watchdog")
need(load(PKG/"cap1750_candidate/result.json")["column_cap"]==1750000,"cap1750 command")
out={"schema":"KRENN_AFFINE251_D12_ROUND1343_GATE_METADATA_AUDIT_V1","status":"PASS_LIGHTWEIGHT_ROUND1343_CAP1750_PROVENANCE","scope":"Small manifest/result/watchdog metadata only; checkpoint/cache payloads deliberately not opened.","sealed_manifest_sha256":sha(MANIFEST),"sealed_audit_sha256":sha(PKG/"results_round1343_cap_audit.json"),"selected":{"round":1343,"columns":1496171,"support":1949,"strategy":"cold","pivot":"rare","checkpoint_sha256":cp,"vectors_sha256":vc},"equivalence":{"cap1500_cap1750_manifest_state_hashes_equal":True,"sealed_audit_reports_only_normalized_command_difference_is_cap":a["only_normalized_command_difference_is_cap"]},"production_contract":{"source_sha256":"3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59","binary_sha256":"79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048","column_cap":1750000,"native_wall_seconds":90,"wrapper_wall_seconds":110,"rss_limit_kib":36*1024*1024},"large_reads_performed":False,"next":"Hold descendant/cache replay until FINAL_REPLAY_CLEAR."}
tmp=HERE/"results_round1343_gate_metadata_audit.json.tmp"; tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); os.replace(tmp,HERE/"results_round1343_gate_metadata_audit.json")
