#!/usr/bin/env python3
"""Independent lower-cap exhaustion control referee; no candidate access."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
P=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-design-2026-08-25"
CONTRACT=ROOT/"computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-design-audit-2026-08-25"
CHAIN=ROOT/"computations/unaudited-codex-n8-affine251-d12-v4-1-round1639-cap4000-audit-2026-08-25"
D=P/"control_cap4000"
PIN={"design":"1a111b26b76eb3d931143f9d9d794c6b2c650a096f3af008be6740cd7dc4a9da","contract":"109d7654df0692e6ff906ff1c13ea724fb0133a83d39324b6580710750b5d711","contract_manifest":"c14b6c3d836fcbf5d035aa01b3337164d7666556be9c94dd3b07361c0f291e94","chain":"a99a307f99bd88f8b363ca73bbc3af631a333bab228fbdb43c3e604382150387","chain_manifest":"de3d1a5e390e0545d5f4c5bca7b7f20fa9205056a772bbd8d1ca841e7ae98b0c","launch":"9237b6c8209fa6fb13b75644c5ade3b9673342a5c44cff75f61a42f5d78b3f5d","validation":"597ab7cb617d722eaf3d6eb3c2e6f80d60037ea5fe13af57753bb2721a0928f2","report":"8985cea386aaf1635410a3081f558a7765113861384f43a0630811df8c56b6be","manifest":"8b27c0935950fbb68eb4eaabd8b7abd5492e0e65747b47c7344ef4a34ea14bb7","result":"8a4afd389656d2d3ecdcaee3edfa249ce5490d3abc581cb0f6d33273ba6f4064","watchdog":"f5352bf6f7d5639196c57627b4d9aca286f67aaab20143dca192c20960a797e4","cp":"ab63c22095dd44d771525af9ba218ee36c9e6f4236a80addbc15692165c531a5","vec":"4d342801fa9e6d25aff95d7b1172f5bff803e8436c01f9237b79e5a42bf6999e"}
def need(x,m):
    if not x: raise AssertionError(m)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()
def pin(path,d):need(path.is_file() and sha(path)==d,f"pin {path}")
def load(path):return json.loads(path.read_text())
for path,key in [(P/"MANIFEST.sha256","design"),(CONTRACT/"results_contract_referee.json","contract"),(CONTRACT/"FINAL_MANIFEST.sha256","contract_manifest"),(CHAIN/"results_round1639_chain_audit.json","chain"),(CHAIN/"FINAL_MANIFEST.sha256","chain_manifest"),(P/"LAUNCH_RECORD_CONTROL.json","launch"),(P/"results_control_validation.json","validation"),(P/"CONTROL_REPORT.md","report"),(P/"CONTROL_MANIFEST.sha256","manifest"),(D/"result.json","result"),(D/"watchdog.json","watchdog")]:pin(path,PIN[key])

# Replay producer control manifest without rereading the two multi-GiB files.
large=dict(line.split(maxsplit=1)[::-1] for line in (HERE/"INDEPENDENT_CONTROL_HASHES.sha256").read_text().splitlines())
need(large=={"checkpoint.bin":PIN["cp"],"vectors.bin":PIN["vec"]},"independent large hashes")
for line in (P/"CONTROL_MANIFEST.sha256").read_text().splitlines():
    digest,name=line.split(maxsplit=1)
    if name=="control_cap4000/checkpoint.bin":need(digest==large["checkpoint.bin"],"manifest cp")
    elif name=="control_cap4000/vectors.bin":need(digest==large["vectors.bin"],"manifest cache")
    else:pin(P/name,digest)

r,w,v,launch=load(D/"result.json"),load(D/"watchdog.json"),load(P/"results_control_validation.json"),load(P/"LAUNCH_RECORD_CONTROL.json")
need((r["status"],r["incomplete_reason"],r["rounds_completed"],r["column_orbits_exposed"],r["dual_support"])==("INCOMPLETE_SEARCH_CAP","COLUMN_CAP",1639,3968369,32704),"control result")
need(r["rounds"]==[] and r["cached_vectors_loaded"]==3968369 and r["vectors_materialized_on_restore"]==0,"zero rounds/restore")
need(r["vector_cache_write_seconds"]==0 and r["global_annihilation"] is None and r["target_pairing"] is None,"no output arithmetic")
need((r["prime"],r["column_cap"],r["wall_limit_seconds"],r["workers"],r["strategy"],r["pivot_mode"],r["elimination_kernel"],r["incremental_basis"])==(1073741827,4000000,150,16,"cold","rare","hierarchical",False),"frozen mode")
need(w["status"]=="PASS" and w["returncode"]==0 and w["breach"] is None and w["atomic_outputs_clean"],"watchdog")
need(w["elapsed_seconds"]==72.368616<180 and w["peak_rss_kib"]==20924976<37748736,"resource")
need((w["source_sha256"],w["binary_sha256"],w["watchdog_sha256"],w["result_sha256"])==("3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59","79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048","75bccbb64d2c9110707bc498fdb71791abe60d7ac3bdf1df942c5a2f63c5c997",PIN["result"]),"provenance")
cmd=w["command"]; need(cmd[cmd.index("--column-cap")+1]=="4000000" and cmd[cmd.index("--round-cap")+1]=="1640","sole cap4m command")
need(cmd[cmd.index("--wall-seconds")+1]=="150" and cmd[cmd.index("--rss-gib")+1]=="36" and cmd[cmd.index("--workers")+1]=="16","command resource")
need(sha(D/"stdout.log")==sha(D/"stderr.log")=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","empty logs")
need({x.name for x in D.iterdir()}=={"checkpoint.bin","vectors.bin","result.json","watchdog.json","stdout.log","stderr.log"},"atomic file set")
need(not (P/"candidate_cap4250").exists(),"candidate absent")
need(v["status"]=="PASS_PRODUCER_LOWER_CAP_EXHAUSTION_WITNESS" and v["control"]["checkpoint_byte_equal_input"] and v["control"]["vector_cache_byte_equal_input"] and v["control"]["round1640_absent"],"producer validation")
need(launch["candidate_guard"]["status"]=="FORBIDDEN_PENDING_CONTROL_TERMINAL_VALIDATION" and not launch["candidate_cleared"],"launch guard")

out={"schema":"KRENN_AFFINE251_D12_R1640_CAP4000_CONTROL_INDEPENDENT_REFEREE_V1","status":"PASS_LOWER_CAP_EXHAUSTION_CONTROL","scope":"Cap-4.0m control only; no candidate state or r1640 arithmetic accepted.","input":{"round":1639,"columns":3968369,"support":32704,"audit_sha256":PIN["chain"],"manifest_sha256":PIN["chain_manifest"],"checkpoint_sha256":PIN["cp"],"vector_cache_sha256":PIN["vec"]},"contract":{"referee_sha256":PIN["contract"],"referee_manifest_sha256":PIN["contract_manifest"],"producer_control_manifest_sha256":PIN["manifest"]},"control":{"result_sha256":PIN["result"],"watchdog_sha256":PIN["watchdog"],"checkpoint_sha256":PIN["cp"],"vector_cache_sha256":PIN["vec"],"status":"COLUMN_CAP","round":1639,"round_records":0,"columns":3968369,"support":32704,"cached_vectors_loaded":3968369,"checkpoint_byte_equal_input":True,"vector_cache_byte_equal_input":True,"no_tmp_or_dual":True,"atomic_watchdog_pass":True,"elapsed_seconds":72.368616,"peak_rss_kib":20924976},"proof":{"deterministic_r1640_whole_set_exceeds_31631_remaining_slots":True,"guard_returned_before_column_arithmetic":True,"accepted_state_unchanged":True,"lower_cap_exhausted":True},"candidate":{"directory_absent":True,"launch_authorized_by_this_referee":False,"next_requirement":"manager clearance; then fresh cap4.25 lane under the approved contract"},"no_round1641":True}
tmp=HERE/"results_control_referee.json.tmp";tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");os.replace(tmp,HERE/"results_control_referee.json")
print("PASS cap4m exhaustion control; candidate absent")
