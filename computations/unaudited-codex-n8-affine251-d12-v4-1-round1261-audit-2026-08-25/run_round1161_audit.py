#!/usr/bin/env python3
"""Independent exact ten-stage audit from accepted round1161 through round1261."""
import hashlib, importlib.util, json, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
PROD = PARENT / "production_from_round1161_portfolio_cap1250"
INPUTPKG = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1161-portfolio-cap1250-gate-2026-08-25"
INPUT = INPUTPKG / "portfolio"
FORMAT = ROOT / "computations/unaudited-codex-n8-affine251-d12-stage01-audit-2026-08-24/audit_stage01.py"
SOURCE = "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
BINARY = "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
WATCH = "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97"
LIMIT = 36 * 1024 * 1024
SPECS = [
    ("stage01",1161,961803,1174,996306,1172,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
    ("stage02",1174,996306,1186,1030890,940,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
    ("stage03",1186,1030890,1199,1064196,1250,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
    ("stage04",1199,1064196,1210,1090756,1235,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
    ("stage05",1210,1090756,1220,1122323,1383,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
    ("stage06",1220,1122323,1230,1155058,1357,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
    ("stage07",1230,1155058,1240,1181627,1203,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
    ("stage08",1240,1181627,1250,1208961,1287,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
    ("stage09",1250,1208961,1260,1236201,1045,"INCOMPLETE_RESOURCE_GATE","WALL_CAP"),
    ("stage10",1260,1236201,1261,1238541,1065,"INCOMPLETE_SEARCH_CAP","ROUND_CAP"),
]

def need(x, message):
    if not x:
        raise SystemExit("REJECT: " + message)

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8 << 20), b""):
            h.update(block)
    return h.hexdigest()

def load(path):
    return json.loads(path.read_text())

need(sha(INPUTPKG / "MANIFEST.sha256") == "d05e1ff544bae130ca960fd1fc6c454f96bb137953d21a3d27628026dc2f44f0", "input manifest pin")
need(sha(INPUT / "checkpoint.bin") == "e7d53052997394ee43d110ead3b74d72cba97773df9076a5eff7dab8033d143a", "input checkpoint")
need(sha(INPUT / "vectors.bin") == "0df2928faf351531f04b936afc06d6a7d8a105f9330ef7200322ca78f257e6c3", "input vectors")
ia = load(INPUTPKG / "results_round1161_audit.json")
need(ia["status"].startswith("PASS") and ia["output_checkpoint_sha256"].startswith("e7d53052") and ia["output_vectors_sha256"].startswith("0df2928f"), "input audit")
need(sha(FORMAT) == "976dba4bb45d5ae59d9e1350f5231b487f7a2bfb9495db9de0f7585666051b67", "format parser")
sp = importlib.util.spec_from_file_location("fmt", FORMAT)
fmt = importlib.util.module_from_spec(sp)
sp.loader.exec_module(fmt)

def edge(oldp, newp, oldn, newn):
    with oldp.open("rb") as a, newp.open("rb") as b:
        ah, bh = fmt.vector_header(a, "old"), fmt.vector_header(b, "new")
        need((ah["count"], bh["count"]) == (oldn, newn), "cache counts")
        need(ah["provider_fingerprint"] == bh["provider_fingerprint"], "cache provider")
        x, y = fmt.vector_record(a, "old record"), fmt.vector_record(b, "new record")
        matched = extra = 0
        while x is not None:
            need(y is not None, "lost cache suffix")
            if y[0] < x[0]:
                extra += 1
                y = fmt.vector_record(b, "new record")
            elif y[0] == x[0]:
                need(y[1] == x[1], "inherited vector changed")
                matched += 1
                x = fmt.vector_record(a, "old record")
                y = fmt.vector_record(b, "new record")
            else:
                need(False, "inherited vector omitted")
        while y is not None:
            extra += 1
            y = fmt.vector_record(b, "new record")
        need(a.read(1) == b"" and b.read(1) == b"", "cache trailing bytes")
    need((matched, extra) == (oldn, newn - oldn), "cache edge census")
    return {"preserved_byte_identically": matched, "new_records": extra,
            "input_fingerprint": ah["vector_fingerprint"], "output_fingerprint": bh["vector_fingerprint"],
            "provider_fingerprint": bh["provider_fingerprint"]}

checkpoints = [fmt.parse_checkpoint(INPUT / "checkpoint.bin")] + [fmt.parse_checkpoint(PROD / s[0] / "checkpoint.bin") for s in SPECS]
headers = [(1161,961803,998)] + [(s[3],s[4],s[5]) for s in SPECS]
for c, h in zip(checkpoints, headers):
    need((c["round"],len(c["columns"]),c["support"],c["target_coefficient"]) == (*h,1), "checkpoint header")
cpedges = []
for a, b in zip(checkpoints, checkpoints[1:]):
    aa, bb = set(a["columns"]), set(b["columns"])
    need(aa <= bb, "checkpoint descendant")
    cpedges.append({"input_round":a["round"], "output_round":b["round"], "preserved":len(aa), "new_columns":len(bb-aa)})

rounds=[]; stages=[]; hashes={}; walls=[]; maxrss=0
for name, ir, ic, orr, oc, sup, status, reason in SPECS:
    d=PROD/name; r=load(d/"result.json"); w=load(d/"watchdog.json")
    need((r["status"],r["incomplete_reason"],r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"],r["cached_vectors_loaded"],r["vectors_materialized_on_restore"]) == (status,reason,orr,oc,sup,ic,0), name+" result")
    need((r["workers"],r["pivot_mode"],r["strategy"],r["elimination_kernel"],r["incremental_basis"],r["column_cap"]) == (16,"rare","cold","hierarchical",False,1250000), name+" mode")
    need([x["round"] for x in r["rounds"]] == list(range(ir+1,orr+1)), name+" no gap")
    cols=ic
    for x in r["rounds"]:
        need(x["new_columns"]>0 and x["selected_pivot"]=="rare" and x["selected_strategy"]=="cold", name+" record")
        cols += x["new_columns"]
        need(cols == x["columns"], name+" recurrence")
    need(cols==oc and r["rounds"][-1]["dual_support"]==sup, name+" final")
    rounds += r["rounds"]
    need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"], name+" watchdog")
    need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"]) == (SOURCE,BINARY,WATCH), name+" pins")
    need(w["rss_limit_kib"]==LIMIT and w["peak_rss_kib"]<LIMIT and all(s["rss_kib"]<LIMIT for s in w["samples"]), name+" RSS")
    need(w["sample_count"]==len(w["samples"]) and w["last_successful_rss_sample"]==w["samples"][-1] and w["elapsed_seconds"]-w["samples"][-1]["elapsed_seconds"]<=.35, name+" telemetry")
    need(not any((d/(f+".tmp")).exists() for f in ("result.json","checkpoint.bin","vectors.bin","stdout.log","stderr.log")), name+" tmp")
    walls.append(w["elapsed_seconds"]); maxrss=max(maxrss,w["peak_rss_kib"])
    stages.append({"stage":name,"rounds":[ir+1,orr],"input_columns":ic,"output_columns":oc,"support":sup,"watchdog_elapsed_seconds":w["elapsed_seconds"],"peak_rss_kib":w["peak_rss_kib"]})
    for k,f in (("result","result.json"),("checkpoint","checkpoint.bin"),("vectors","vectors.bin"),("watchdog","watchdog.json"),("stderr","stderr.log")):
        hashes[name+"_"+k]=sha(d/f)

need([x["round"] for x in rounds] == list(range(1162,1262)), "global rounds")
cols=961803
for x in rounds:
    cols += x["new_columns"]
    need(cols==x["columns"], "global columns")
need(cols==1238541 and len(rounds)==100, "global final")
blockA=sum(walls[:5]); blockB=sum(walls[5:])
need(abs(blockA-496.679810)<1e-6 and abs(blockB-428.310805)<1e-6 and blockA<540 and blockB<540 and maxrss==14755360, "resource blocks")

paths=[INPUT/"vectors.bin"] + [PROD/s[0]/"vectors.bin" for s in SPECS]
counts=[961803] + [s[4] for s in SPECS]
edges=[{"input_round":headers[i][0],"output_round":headers[i+1][0],**edge(paths[i],paths[i+1],counts[i],counts[i+1])} for i in range(10)]
replay=load(HERE/"results_round1261_all_column_replay.json")
need((replay["status"],replay["round"],replay["columns_replayed"],replay["terms_replayed"],replay["verification_failures"]) == ("PASS_ALL_COLUMNS",1261,1238541,126329382,0), "final replay")
need(hashes["stage10_result"].startswith("2eb3788e") and hashes["stage10_checkpoint"].startswith("6fb20b1c") and hashes["stage10_watchdog"].startswith("6881434c"), "final pins")

out={"schema":"KRENN_AFFINE251_D12_V4_1_ROUND1261_CHAIN_AUDIT_V1","status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1261_CHAIN","scope":"Accepted round1161 portfolio through exact rounds1162..1261; no round1262 continuation.","input":{"round":1161,"columns":961803,"support":998,"checkpoint_sha256":"e7d53052997394ee43d110ead3b74d72cba97773df9076a5eff7dab8033d143a","vectors_sha256":"0df2928faf351531f04b936afc06d6a7d8a105f9330ef7200322ca78f257e6c3"},"final":{"round":1261,"columns":1238541,"new_columns":276738,"support":1065,"target_coefficient":1},"stage_summaries":stages,"checkpoint_edges":cpedges,"cache_edges":edges,"resources":{"blockA_watchdog_seconds":blockA,"blockB_watchdog_seconds":blockB,"each_block_required_less_than":540,"maximum_peak_rss_kib":maxrss,"rss_limit_kib":LIMIT},"all_column_replay":replay,"artifact_sha256":hashes,"pins":{"source_sha256":SOURCE,"binary_sha256":BINARY,"watchdog_sha256":WATCH,"input_manifest_sha256":sha(INPUTPKG/"MANIFEST.sha256"),"replay_sha256":sha(HERE/"results_round1261_all_column_replay.json")},"verdict_note":"Round1261 remains INCOMPLETE_SEARCH_CAP/ROUND_CAP: exact resumable state, not a terminal global dual."}
tmp=HERE/"results_round1261_chain_audit.json.tmp"
tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
os.replace(tmp,HERE/"results_round1261_chain_audit.json")
