#!/usr/bin/env python3
"""Dynamic referee for the v4.1 parser-bound patch."""
import hashlib, json, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROD = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
CONTROL, CANDIDATE = PROD / "bound_control_v4", PROD / "bound_candidate_v4_1"
V4S = "c83c6801ec2c09683c81773607fcf3babb538e34354dfd8f27d03aae0e22f102"
V4B = "191eb08843466e263149ccd5688b57a5f5352cbb2dfbc5e1081fca856b2e5c0b"
V41S = "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
V41B = "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def load(p): return json.loads(p.read_text())
def need(x,m):
    if not x: raise SystemExit("REJECT: "+m)
def semantic(v):
    v=json.loads(json.dumps(v))
    for k in ("elapsed_seconds","peak_rss_kib","restore_seconds","vector_cache_write_seconds","checkpoint","vector_cache","dual"): v.pop(k,None)
    for r in v["rounds"]:
        for k in ("incident_seconds","materialize_seconds","solve_seconds"): r.pop(k,None)
    return v
def watchdog(path, source, binary):
    w=load(path); limit=36*1024*1024
    need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],"watchdog")
    need(w["source_sha256"]==source and w["binary_sha256"]==binary,"watchdog pins")
    need(w["rss_limit_kib"]==limit and w["peak_rss_kib"]<limit and all(s["rss_kib"]<limit for s in w["samples"]),"RSS")
    return {"sha256":sha(path),"peak_rss_kib":w["peak_rss_kib"]}

static=load(HERE/"results_v4_1_static_audit.json")
need(static["status"]=="PASS_EXACT_SOLE_ROUND_CAP_BOUND_PATCH","static")
r0,r1=load(CONTROL/"result.json"),load(CANDIDATE/"result.json")
for r in (r0,r1):
    need(r["status"]=="INCOMPLETE_SEARCH_CAP" and r["rounds_completed"]==961 and [x["round"] for x in r["rounds"]]==[961],"chain")
    need(r["column_orbits_exposed"]==577645 and r["dual_support"]==523 and r["rounds"][0]["new_columns"]==1244,"census")
need(semantic(r0)==semantic(r1),"non-timing result equality")
cp0,cp1=sha(CONTROL/"checkpoint.bin"),sha(CANDIDATE/"checkpoint.bin")
vc0,vc1=sha(CONTROL/"vectors.bin"),sha(CANDIDATE/"vectors.bin")
need(cp0==cp1=="2fac10fb7b77f145e67a51a9f6ae4328fa31187d05f8d670fdc9d2564d5592cd","checkpoint equality")
need(vc0==vc1=="8bce26efb055cd9ea8aaf3f31b10d149eeff96816a0be58d5fef6f5254c5ca35","cache equality")
host=load(PROD/"results_hostiles.json")
need(host["status"]=="PASS" and host["source_sha256"]==V41S and host["binary_sha256"]==V41B,"hostile pins")
need(host["cases"]["round_cap_10001"]=={"returncode":2,"status":"PASS_REJECTED"},"10001 rejection")
refused=PROD/"production_from_round960/stage01_refused_cap1060"
need("bad sparse search cap" in (refused/"stderr.log").read_text() and not (refused/"result.json").exists(),"preserved v4 cap1060 refusal")
order=load(HERE/"results_round961_external_order_gate.json"); final=order["round850"]
need(order["status"]=="PASS_EXACT_ROUND849_850_ORDER_EQUIVALENCE" and final["records"]==577645 and final["terms"]==58743477 and final["ranked_rows"]==32534680,"order census")
need(final["order_sha256_baseline"]==final["order_sha256_index"],"canonical order")
replay=load(HERE/"results_round961_all_column_replay.json")
need(replay["status"]=="PASS_ALL_COLUMNS" and replay["round"]==961 and replay["columns_replayed"]==577645 and replay["terms_replayed"]==58743477 and replay["verification_failures"]==0,"replay")
out={"schema":"KRENN_AFFINE251_D12_V4_1_BOUND_REFEREE_V1","status":"PASS_EXACT_V4_1_ROUND_CAP_BOUND_PATCH",
 "source_diff":{"baseline_sha256":V4S,"v4_1_sha256":V41S,"v4_1_binary_sha256":V41B,"only_change":"round_cap > 1000 -> round_cap > 10_000"},
 "exactness":{"round":961,"columns":577645,"new_columns":1244,"support":523,"terms":58743477,"checkpoint_sha256":cp0,"vectors_sha256":vc0,"order_rows":32534680,"order_sha256":final["order_sha256_index"],"pairing_failures":0},
 "guards":{"round_cap_10001_rejected":True,"old_v4_cap1060_refusal_preserved":True,"modes_unchanged":True,"schema_unchanged":True},
 "resources":{"v4":watchdog(CONTROL/"watchdog.json",V4S,V4B),"v4_1":watchdog(CANDIDATE/"watchdog.json",V41S,V41B)},
 "pins":{"contract_sha256":sha(HERE/"AUDIT_CONTRACT.json"),"static_audit_sha256":sha(HERE/"results_v4_1_static_audit.json"),"control_result_sha256":sha(CONTROL/"result.json"),"candidate_result_sha256":sha(CANDIDATE/"result.json"),"hostiles_sha256":sha(PROD/"results_hostiles.json"),"order_gate_sha256":sha(HERE/"results_round961_external_order_gate.json"),"replay_sha256":sha(HERE/"results_round961_all_column_replay.json")},
 "scope":"Parser bound and matched round960->961 only; no broad continuation."}
tmp=HERE/"results_v4_1_referee.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_v4_1_referee.json")
