#!/usr/bin/env python3
"""Small-file-only launch-readiness audit; never opens r1463 cp/cache."""
import ast,hashlib,json,os,shutil
from pathlib import Path
if not __debug__: raise RuntimeError("fail closed: assertions required")
H=Path(__file__).resolve().parent; R=H.parents[1]; S=json.loads((H/"SCHEDULE.json").read_text()); P=json.loads((H/"INPUT_PINS.json").read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert S["status"]=="FROZEN_READY_HELD_FOR_EXPLICIT_LAUNCH_CLEARANCE" and P["status"]=="PASS_PINNED_FROM_INDEPENDENT_ROUND1463_FINAL_REPLAY_CLEAR"
assert not (H/"LAUNCH_CLEARANCE.json").exists()
for name in ("run_external.py","validate_final.py","preflight.py"):
 ast.parse((H/name).read_text(),filename=name)
tasks=[(x["strategy"],x["pivot"]) for x in S["ordered_tasks"]]
assert tasks==[("repair","first"),("repair","last"),("repair","rare"),("cold","first"),("cold","last"),("cold","rare")]
assert S["lane_geometry"]["one_process_at_a_time"] and S["lane_geometry"]["native_wall_seconds"]==135 and S["lane_geometry"]["wrapper_wall_seconds"]==150 and S["lane_geometry"]["rss_gib"]==36
assert S["selector"]["key"]==["unseen_incident_frontier_count","support","task_index"]
assert S["disk_lifecycle"]["minimum_free_bytes_before_first_clone"]==30<<30 and S["disk_lifecycle"]["compaction_record_sha256"].startswith("14e32d19")
for rel,key in [(S["engine"]["source"],"source_sha256"),(S["engine"]["binary"],"binary_sha256"),(S["engine"]["watchdog"],"watchdog_sha256"),(S["engine"]["provider"],"provider_sha256")]: assert sha(R/rel)==S["engine"][key]
assert sha(H/S["scorer"]["source"])==S["scorer"]["source_sha256"] and sha(H/S["scorer"]["binary"])==S["scorer"]["binary_sha256"]
assert sha(R/P["audit_result"])==P["audit_result_sha256"] and sha(R/P["audit_manifest"])==P["audit_manifest_sha256"]
audit=json.loads((R/P["audit_result"]).read_text()); assert audit["status"]=="PASS_EXACT_FULLY_TELEMETERED_ROUND1463_CAP2250_CHAIN" and audit["final"]=={"columns":2049529,"new_columns":74921,"round":1463,"support":2389,"target_coefficient":1}
assert audit["artifact_sha256"]["stage04_checkpoint"]==P["checkpoint_sha256"] and audit["artifact_sha256"]["stage04_vectors"]==P["vectors_sha256"] and audit["all_column_replay"]["verification_failures"]==0
free=shutil.disk_usage(H).free; assert free>=30<<30
assert not any((H/f"lane{i:02d}_{s}_{p}").exists() for i,(s,p) in enumerate(tasks)) and not (H/"fixed_winner").exists() and not (H/"cap2500_candidate").exists()
text=(H/"run_external.py").read_text(); assert 'atomic(d/"lane_evidence.json",ev); return ev' in text and 'for name in ("checkpoint.bin","vectors.bin")' in text and text.index('atomic(d/"lane_evidence.json",ev); return ev')<text.index('def prune(label)')
value={"schema":"KRENN_AFFINE251_D12_R1464_EXTERNAL_PREFLIGHT_V1","status":"PASS_LAUNCH_READY_HELD_EXPLICIT_CLEARANCE","free_gib_floor":free//(1<<30),"minimum_free_bytes":30<<30,"six_lane_set_exact":True,"stable_selector_frozen":True,"evidence_before_prune":True,"large_checkpoint_or_cache_opened":False,"clone_or_solve":False,"launch_clearance_absent":True}
t=H/"results_preflight.json.tmp"; t.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n"); os.replace(t,H/"results_preflight.json"); print(json.dumps(value,sort_keys=True))
