#!/usr/bin/env python3
"""Small-file provenance audit for the sealed round1262 cap1500 gate."""
import hashlib, json, os
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PKG=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1262-internal-sequential-portfolio-cap1500-2026-08-25"
MANIFEST=PKG/"MANIFEST.sha256"

def need(value,message):
    if not value: raise SystemExit("REJECT: "+message)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def load(path): return json.loads(path.read_text())

need(sha(MANIFEST)=="716bf4dada464da6b8a04a453db516ed3db839ad4f3ab83d662ffcce72bc9c64","manifest pin")
entries={}
for line in MANIFEST.read_text().splitlines():
    digest,name=line.split("  ",1)
    need(len(digest)==64 and name not in entries,"manifest syntax/duplicate")
    entries[name]=digest
need(entries["results_round1262_audit.json"]=="29d0b05b2ebca3c686a90276d9b881eb8c6c8f583169322b74bcef2dce0c0c1f","audit entry")
need(sha(PKG/"results_round1262_audit.json")==entries["results_round1262_audit.json"],"audit artifact")
audit=load(PKG/"results_round1262_audit.json")
need(audit["status"]=="PASS_EXACT_INTERNAL_SIX_PORTFOLIO_AND_CAP1500_EQUIVALENCE","audit status")
cp="2d9f65c918f2eac295c8e642f60d57d43458fe98efd40aed325062c10254225e"
vc="00437f95d845567b9082a25a97be738fd4a94d14e20e1afec556f9f95c726a9e"
need(audit["output_checkpoint_sha256"]==cp and audit["output_vectors_sha256"]==vc,"output pins")
for label in ("portfolio","selected_control","cap1500_candidate"):
    need(entries[label+"/checkpoint.bin"]==cp and entries[label+"/vectors.bin"]==vc,"manifest state equivalence "+label)
    need(sha(PKG/label/"result.json")==entries[label+"/result.json"],"small result "+label)
    need(sha(PKG/label/"watchdog.json")==entries[label+"/watchdog.json"],"small watchdog "+label)
    result=load(PKG/label/"result.json"); watch=load(PKG/label/"watchdog.json")
    need((result["rounds_completed"],result["column_orbits_exposed"],result["dual_support"])==(1262,1240851,1098),"state header "+label)
    need(result["rounds"][0]["selected_strategy"]=="cold" and result["rounds"][0]["selected_pivot"]=="rare","selection "+label)
    need(watch["status"]=="PASS" and watch["breach"] is None and watch["atomic_outputs_clean"],"watchdog "+label)
need(load(PKG/"cap1500_candidate/result.json")["column_cap"]==1500000,"cap1500 command")
need(audit["cap1500"]["state_byte_identical"] and audit["fixed_replay"]["state_byte_identical"],"sealed equivalence")
out={
 "schema":"KRENN_AFFINE251_D12_ROUND1262_GATE_METADATA_AUDIT_V1",
 "status":"PASS_LIGHTWEIGHT_ROUND1262_CAP1500_PROVENANCE",
 "scope":"Small manifest/result/watchdog metadata only; checkpoint and cache payloads deliberately not opened.",
 "sealed_manifest_sha256":sha(MANIFEST),
 "sealed_audit_sha256":sha(PKG/"results_round1262_audit.json"),
 "selected":{"round":1262,"columns":1240851,"support":1098,"strategy":"cold","pivot":"rare","checkpoint_sha256":cp,"vectors_sha256":vc},
 "equivalence":{"portfolio_selected_control_cap1500_manifest_state_hashes_equal":True,"sealed_audit_reports_byte_identical":True},
 "production_contract":{"source_sha256":"3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59","binary_sha256":"79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048","column_cap":1500000,"native_wall_seconds":90,"wrapper_wall_seconds":110,"rss_limit_kib":36*1024*1024},
 "large_reads_performed":False,
 "next":"Hold descendant/cache replay until producer FINAL_REPLAY_CLEAR."
}
tmp=HERE/"results_round1262_gate_metadata_audit.json.tmp"
tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
os.replace(tmp,HERE/"results_round1262_gate_metadata_audit.json")
