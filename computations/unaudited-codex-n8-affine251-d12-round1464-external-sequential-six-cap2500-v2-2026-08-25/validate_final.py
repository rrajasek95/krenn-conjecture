#!/usr/bin/env python3
"""Independent final audit of the external r1464 portfolio lifecycle."""
import hashlib,json,os
from pathlib import Path
if not __debug__: raise RuntimeError("fail closed: assertions required")
H=Path(__file__).resolve().parent; S=json.loads((H/"SCHEDULE.json").read_text()); summary=json.loads((H/"runner_summary.json").read_text())
def sha(p):
 d=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(8<<20),b""): d.update(b)
 return d.hexdigest()
assert summary["status"]=="PASS_SIX_LANES_FIXED_REPLAY_AND_CONDITIONAL_CAP_EQUIVALENCE"
records=[]
for task in S["ordered_tasks"]:
 label=f"lane{task['index']:02d}_{task['strategy']}_{task['pivot']}"; d=H/label; ev=json.loads((d/"lane_evidence.json").read_text())
 assert ev["status"]=="PASS_SEALED_BEFORE_PRUNE" and ev["task_index"]==task["index"] and ev["strategy"]==task["strategy"] and ev["pivot"]==task["pivot"]
 assert sha(d/"result.json")==ev["result_sha256"] and sha(d/"watchdog.json")==ev["watchdog_sha256"] and sha(d/"frontier_score.json")==ev["frontier_score_sha256"]
 records.append((tuple(ev["selector_key"]),label,ev))
winner=min(records,key=lambda x:x[0]); assert winner[1]==summary["winner"]["label"] and list(winner[0])==summary["winner"]["selector_key"]
fixed=json.loads((H/"fixed_winner/lane_evidence.json").read_text()); assert fixed["checkpoint_sha256"]==winner[2]["checkpoint_sha256"] and fixed["vectors_sha256"]==winner[2]["vectors_sha256"] and fixed["round_record"]==winner[2]["round_record"]
final=H/summary["final_retained_payload"]; final_ev=json.loads((final/"lane_evidence.json").read_text()); assert not final_ev["pruned"]
assert sha(final/"checkpoint.bin")==final_ev["checkpoint_sha256"] and sha(final/"vectors.bin")==final_ev["vectors_sha256"]
if summary["conditional_cap_run"]:
 assert summary["winner"]["strategy"]=="cold" and summary["winner"]["pivot"]=="rare" and summary["final_retained_payload"]=="cap2500_candidate"
 assert final_ev["checkpoint_sha256"]==fixed["checkpoint_sha256"] and final_ev["vectors_sha256"]==fixed["vectors_sha256"]
 assert json.loads((H/"fixed_winner/lane_evidence.json").read_text())["pruned"] is True
value={"schema":"KRENN_AFFINE251_D12_R1464_EXTERNAL_FINAL_AUDIT_V1","status":"PASS_EXACT_EXTERNAL_SIX_SELECTOR_FIXED_AND_CAP","winner":summary["winner"],"six_lane_set_exact":True,"stable_selector_replayed":True,"final_checkpoint_sha256":final_ev["checkpoint_sha256"],"final_vectors_sha256":final_ev["vectors_sha256"],"continued_beyond_round1464":False}
t=H/"results_final_audit.json.tmp"; t.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n"); os.replace(t,H/"results_final_audit.json"); print(json.dumps(value,sort_keys=True))
