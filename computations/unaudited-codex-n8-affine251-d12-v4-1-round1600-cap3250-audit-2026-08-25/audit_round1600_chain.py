#!/usr/bin/env python3
"""Seal the independent one-pass r1588→r1600 descendant/replay audit."""
import hashlib, json, os
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
PLAN=json.loads((HERE/"AUDIT_PLAN.json").read_text())
PROD=ROOT/PLAN["production_root"]
LARGE=json.loads((HERE/"results_round1600_large_sha_audit.json").read_text())
REPLAY=json.loads((HERE/"results_round1600_single_pass_replay.json").read_text())

def need(value,message):
    if not value: raise SystemExit("REJECT: "+message)
def load(path): return json.loads(path.read_text())
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(8<<20),b""): h.update(block)
    return h.hexdigest()
def arg(command,flag):
    need(command.count(flag)==1,"command "+flag); return command[command.index(flag)+1]

for key,name in (("cap_audit_sha256","cap_audit"),("cap_manifest_sha256","cap_manifest"),("compaction_record_sha256","compaction_record")):
    need(sha(ROOT/PLAN["input"][name])==PLAN["input"][key],key)
cap=load(ROOT/PLAN["input"]["cap_audit"])
need(cap["status"]=="PASS_EXACT_DIRECT_CAP3000_TO_CAP3250_EQUIVALENCE" and cap["accepted_candidate"]=="candidate_cap3250","input cap audit status")
need(cap["checkpoint_sha256"]==PLAN["input"]["checkpoint_sha256"] and cap["vectors_sha256"]==PLAN["input"]["vectors_sha256"],"input cap pins")
for name,key in (("PLAN.json","plan_sha256"),("PRODUCER_LEDGER.json","ledger_sha256"),("REPORT.md","report_sha256"),("MANIFEST.sha256","manifest_sha256")):
    need(sha(PROD/name)==PLAN["producer"][key],"producer "+name)

ledger=load(PROD/"PRODUCER_LEDGER.json"); contract=PLAN["contract"]
need(ledger["status"]=="PASS_PRODUCER_HELD_FOR_INDEPENDENT_AUDIT","producer status")
need((ledger["contract"]["source_sha256"],ledger["contract"]["binary_sha256"],ledger["contract"]["watchdog_sha256"])==(contract["source_sha256"],contract["binary_sha256"],contract["watchdog_sha256"]),"producer pins")
need(LARGE["status"]=="PASS_ALL_14_CHECKPOINT_CACHE_SHA256","large SHA status")
need(LARGE["artifacts"]["input_checkpoint"]==PLAN["input"]["checkpoint_sha256"] and LARGE["artifacts"]["input_vectors"]==PLAN["input"]["vectors_sha256"],"large input SHA")

producer_manifest={line.split(maxsplit=1)[1]:line.split(maxsplit=1)[0] for line in (PROD/"MANIFEST.sha256").read_text().splitlines() if line.strip()}
stages=[]; all_rounds=[]; columns=PLAN["input"]["columns"]; small_hashes={}
for spec,declared in zip(PLAN["stages"],ledger["accepted_stages"],strict=True):
    directory=PROD/spec["name"]; result=load(directory/"result.json"); watchdog=load(directory/"watchdog.json"); records=result["rounds"]
    need([record["round"] for record in records]==spec["rounds"] and declared["name"]==spec["name"],spec["name"]+" rounds")
    need(result["rounds_completed"]==spec["rounds"][-1] and result["cached_vectors_loaded"]==columns and result["vectors_materialized_on_restore"]==0,spec["name"]+" restore")
    need((result["workers"],result["pivot_mode"],result["strategy"],result["elimination_kernel"],result["incremental_basis"],result["column_cap"])==(16,"rare","cold","hierarchical",False,3250000),spec["name"]+" mode")
    need((result["status"],result["incomplete_reason"])==("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),spec["name"]+" status")
    for record in records:
        need(record["new_columns"]>0 and (record["selected_strategy"],record["selected_pivot"])==("cold","rare"),spec["name"]+" record")
        columns+=record["new_columns"]; need(record["columns"]==columns,spec["name"]+" column recurrence")
    need((result["column_orbits_exposed"],result["dual_support"])==(columns,records[-1]["dual_support"]),spec["name"]+" census")
    need(watchdog["status"]=="PASS" and watchdog["returncode"]==0 and watchdog["breach"] is None and watchdog["atomic_outputs_clean"],spec["name"]+" watchdog")
    need((watchdog["source_sha256"],watchdog["binary_sha256"],watchdog["watchdog_sha256"])==(contract["source_sha256"],contract["binary_sha256"],contract["watchdog_sha256"]),spec["name"]+" watchdog pins")
    need(watchdog["elapsed_seconds"]<150 and watchdog["peak_rss_kib"]<contract["rss_limit_kib"] and all(sample["rss_kib"]<contract["rss_limit_kib"] for sample in watchdog["samples"]),spec["name"]+" resources")
    for flag,value in (("--round-cap",str(spec["rounds"][-1])),("--column-cap","3250000"),("--wall-seconds","120"),("--workers","16"),("--pivot","rare"),("--strategy","cold"),("--elimination","hierarchical"),("--incremental","no")):
        need(arg(watchdog["command"],flag)==value,spec["name"]+" "+flag)
    need(not list(directory.glob("*.tmp")),spec["name"]+" tmp")
    for suffix,filename in (("result","result.json"),("watchdog","watchdog.json"),("stderr","stderr.log")):
        digest=sha(directory/filename); small_hashes[spec["name"]+"_"+suffix]=digest
        if suffix in ("result","watchdog"): need(producer_manifest[spec["name"]+"/"+filename]==digest,spec["name"]+" manifest "+suffix)
    for suffix in ("checkpoint","vectors"):
        digest=LARGE["artifacts"][spec["name"]+"_"+suffix]
        need(producer_manifest[spec["name"]+"/"+("checkpoint.bin" if suffix=="checkpoint" else "vectors.bin")]==digest,spec["name"]+" large manifest "+suffix)
        need(digest==declared[("checkpoint_sha256" if suffix=="checkpoint" else "vector_cache_sha256")],spec["name"]+" ledger "+suffix)
    stages.append({"stage":spec["name"],"input_round":spec["rounds"][0]-1,"output_round":spec["rounds"][-1],"input_columns":result["cached_vectors_loaded"],"output_columns":columns,"support":result["dual_support"],"watchdog_elapsed_seconds":watchdog["elapsed_seconds"],"peak_rss_kib":watchdog["peak_rss_kib"]})
    all_rounds+=records
need([record["round"] for record in all_rounds]==list(range(1589,1601)),"global round coverage")
blocks=[sum(next(stage["watchdog_elapsed_seconds"] for stage in stages if stage["stage"]==name) for name in block) for block in PLAN["blocks"]]
need(all(value<540 for value in blocks) and blocks==[352.461833,353.115636],"block walls")
need((columns,stages[-1]["support"])==(PLAN["target"]["columns"],PLAN["target"]["support"]),"endpoint")

need(REPLAY["status"]=="PASS_SIX_DESCENDANT_EDGES_AND_ALL_COLUMNS" and REPLAY["rounds"]==[1588,1590,1592,1594,1596,1598,1600],"replay status/rounds")
need(REPLAY["columns"]==[PLAN["input"]["columns"]]+[stage["output_columns"] for stage in stages] and REPLAY["supports"]==[PLAN["input"]["support"]]+[stage["support"] for stage in stages],"replay census")
need(REPLAY["checkpoint_descendant_edges"]==REPLAY["cache_descendant_edges"]==6 and REPLAY["inherited_vectors_byte_identical"] and REPLAY["verification_failures"]==0 and REPLAY["target_terms"]==2 and REPLAY["candidate_hit_terms"]>0,"replay exactness")

output={
 "schema":"KRENN_AFFINE251_D12_V4_1_ROUND1600_CAP3250_CHAIN_AUDIT_V1",
 "status":"PASS_EXACT_FULLY_TELEMETERED_ROUND1600_CAP3250_CHAIN",
 "scope":"Accepted independently cap-equivalent r1588 state through exact rounds1589..1600; no r1601 continuation or closure claim.",
 "input":{"round":1588,"columns":PLAN["input"]["columns"],"support":PLAN["input"]["support"],"checkpoint_sha256":PLAN["input"]["checkpoint_sha256"],"vectors_sha256":PLAN["input"]["vectors_sha256"]},
 "final":{"round":1600,"columns":columns,"new_columns":columns-PLAN["input"]["columns"],"support":stages[-1]["support"],"target_coefficient":1,"checkpoint_sha256":LARGE["artifacts"]["stage06_cap1600_checkpoint"],"vectors_sha256":LARGE["artifacts"]["stage06_cap1600_vectors"]},
 "stage_summaries":stages,
 "checkpoint_edges":[{"input_round":REPLAY["rounds"][i],"output_round":REPLAY["rounds"][i+1],"preserved":REPLAY["columns"][i],"new_columns":REPLAY["columns"][i+1]-REPLAY["columns"][i]} for i in range(6)],
 "cache_edges":[{"input_round":REPLAY["rounds"][i],"output_round":REPLAY["rounds"][i+1],"preserved_byte_identically":REPLAY["columns"][i],"new_records":REPLAY["columns"][i+1]-REPLAY["columns"][i],"provider_fingerprint":REPLAY["provider_fingerprint"]} for i in range(6)],
 "resources":{"aggregate_block_watchdog_seconds":blocks,"each_required_less_than":540,"maximum_peak_rss_kib":max(stage["peak_rss_kib"] for stage in stages),"rss_limit_kib":contract["rss_limit_kib"]},
 "all_column_replay":REPLAY,
 "large_artifact_sha256":LARGE["artifacts"],
 "small_artifact_sha256":small_hashes,
 "pins":{"input_cap_audit_sha256":PLAN["input"]["cap_audit_sha256"],"input_cap_manifest_sha256":PLAN["input"]["cap_manifest_sha256"],"compaction_record_sha256":PLAN["input"]["compaction_record_sha256"],"producer_manifest_sha256":PLAN["producer"]["manifest_sha256"],"producer_ledger_sha256":PLAN["producer"]["ledger_sha256"],"source_sha256":contract["source_sha256"],"binary_sha256":contract["binary_sha256"],"watchdog_sha256":contract["watchdog_sha256"],"single_pass_scanner_source_sha256":sha(HERE/"scan_chain_once.rs"),"single_pass_scanner_binary_sha256":sha(HERE/"scan_chain_once")},
 "verdict_note":"Round1600 is an exact resumable ROUND_CAP state, not a terminal global dual; the CEGAR search remains open."
}
temporary=HERE/"results_round1600_chain_audit.json.tmp"; temporary.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n"); os.replace(temporary,HERE/"results_round1600_chain_audit.json")
print(json.dumps({"status":output["status"],"round":1600,"columns":columns,"terms":REPLAY["terms_replayed"],"failures":0,"blocks":blocks},sort_keys=True))
