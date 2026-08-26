#!/usr/bin/env python3
"""Small-file provenance audit for the sealed round1363 cap2000 gate."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
PKG=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1363-internal-sequential-portfolio-cap2000-design-2026-08-25"; MANIFEST=PKG/"MANIFEST.sha256"
def need(x,m):
 if not x: raise SystemExit("REJECT: "+m)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""): h.update(b)
 return h.hexdigest()
def load(p): return json.loads(p.read_text())
need(sha(MANIFEST)=="bc359255b558a91a02fee4fc76aee9394b3a91d08aa24dd4ef96652bf1e80fd6","manifest pin")
entries={}
for line in MANIFEST.read_text().splitlines():
 d,n=line.split("  ",1); need(len(d)==64 and n not in entries,"manifest syntax/duplicate"); entries[n]=d
need(entries["results_round1363_audit.json"]=="8c55b66916dcfc14fc27a51cb7337bfe37e4ef32b65cb9bf3ca8ccba01d1ee11","audit entry")
need(sha(PKG/"results_round1363_audit.json")==entries["results_round1363_audit.json"],"audit artifact")
a=load(PKG/"results_round1363_audit.json"); need(a["status"]=="PASS_EXACT_INTERNAL_SIX_PORTFOLIO_AND_FIXED_REPLAY" and a["cap_equivalence"]["status"]=="PASS_EXACT_CAP1750_TO_CAP2000_EQUIVALENCE","audit status")
cp="91d573bcfbb2e43f0832a595c899b7c5bd411845cb8323cbcff1c5d7728f92e1"; vc="5c39cf56b3504a44f8e002f9ad3e42b533855d6217e5e5f9967543f6d77e0e5e"
need(a["output_checkpoint_sha256"]==cp and a["output_vectors_sha256"]==vc,"output pins")
for label in ("portfolio","selected_control","cap2000_candidate"):
 need(entries[label+"/checkpoint.bin"]==cp and entries[label+"/vectors.bin"]==vc,"manifest state equivalence")
 need(sha(PKG/label/"result.json")==entries[label+"/result.json"] and sha(PKG/label/"watchdog.json")==entries[label+"/watchdog.json"],"small artifacts "+label)
 r=load(PKG/label/"result.json"); w=load(PKG/label/"watchdog.json")
 need((r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"])==(1363,1587266,2161),"state header")
 need(r["rounds"][0]["selected_strategy"]=="cold" and r["rounds"][0]["selected_pivot"]=="rare","selection")
 need(w["status"]=="PASS" and w["breach"] is None and w["atomic_outputs_clean"],"watchdog")
need(load(PKG/"cap2000_candidate/result.json")["column_cap"]==2000000,"cap2000 command")
out={"schema":"KRENN_AFFINE251_D12_ROUND1363_GATE_METADATA_AUDIT_V1","status":"PASS_LIGHTWEIGHT_ROUND1363_CAP2000_PROVENANCE","scope":"Small manifest/result/watchdog metadata only; checkpoint/cache payloads deliberately not opened.","sealed_manifest_sha256":sha(MANIFEST),"sealed_audit_sha256":sha(PKG/"results_round1363_audit.json"),"selected":{"round":1363,"columns":1587266,"support":2161,"strategy":"cold","pivot":"rare","checkpoint_sha256":cp,"vectors_sha256":vc},"equivalence":{"portfolio_selected_control_cap2000_manifest_state_hashes_equal":True,"sealed_audit_reports_cap_only_equivalence":a["cap_equivalence"]["sole_normalized_difference_is_cap"]},"production_contract":{"source_sha256":"3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59","binary_sha256":"79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048","column_cap":2000000,"native_wall_seconds":90,"wrapper_wall_seconds":110,"rss_limit_kib":36*1024*1024},"large_reads_performed":False,"next":"Hold descendant/cache replay until FINAL_REPLAY_CLEAR."}
tmp=HERE/"results_round1363_gate_metadata_audit.json.tmp"; tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); os.replace(tmp,HERE/"results_round1363_gate_metadata_audit.json")
