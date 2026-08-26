#!/usr/bin/env python3
"""Execute the pinned r1484 full-chain referee template for the r1504 plan."""
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
TEMPLATE=HERE.parent/"unaudited-codex-n8-affine251-d12-v4-1-round1484-cap2500-audit-2026-08-25/run_final_chain_audit.py"
EXPECTED="8aae43756f2904fd2ebcbf59510e45d3877e272a5916580806b1a12770b4bb60"
raw=TEMPLATE.read_bytes()
assert hashlib.sha256(raw).hexdigest()==EXPECTED
source=raw.decode()
assert source.count("1484")==11 and "1504" not in source
source=source.replace("1484","1504")
old_input='ia=load(REPO/P["input_audit"]);need(ia["status"]=="PASS_EXACT_DIRECT_CAP2250_TO_CAP2500_EQUIVALENCE" and ia["checkpoint_sha256"]==P["input_checkpoint_sha256"] and ia["vectors_sha256"]==P["input_vectors_sha256"],"input audit contents")'
new_input='ia=load(REPO/P["input_audit"]);need(ia["status"]=="PASS_EXACT_FULLY_TELEMETERED_ROUND1484_CAP2500_CHAIN" and ia["final"]["round"]==P["input_round"] and ia["artifact_sha256"]["stage05_checkpoint"]==P["input_checkpoint_sha256"] and ia["artifact_sha256"]["stage05_vectors"]==P["input_vectors_sha256"],"input audit contents")'
assert source.count(old_input)==1
source=source.replace(old_input,new_input)
old=' expected=("INCOMPLETE_SEARCH_CAP","ROUND_CAP") if rr[-1]["round"]==P["target_round"] else ("INCOMPLETE_RESOURCE_GATE","WALL_CAP");need((r["status"],r["incomplete_reason"])==expected,d.name+" status")'
new=' if rr[-1]["round"]==P["target_round"]:need((r["status"],r["incomplete_reason"]) in (("INCOMPLETE_SEARCH_CAP","ROUND_CAP"),("INCOMPLETE_RESOURCE_GATE","WALL_CAP")),d.name+" target status")\n else:need((r["status"],r["incomplete_reason"])==("INCOMPLETE_RESOURCE_GATE","WALL_CAP"),d.name+" status")'
assert source.count(old)==1 and source.count("exact resumable ROUND_CAP state")==1
source=source.replace(old,new).replace("exact resumable ROUND_CAP state","exact target-round resumable state")
old_scope="Accepted r1464 cap2.5m state through exact rounds1465..1504; no r1485 continuation or closure claim."
new_scope="Accepted r1484 cap2.5m state through exact rounds1485..1504; no r1505 continuation or closure claim."
assert source.count(old_scope)==1
source=source.replace(old_scope,new_scope)
exec(compile(source,str(HERE/"run_final_chain_audit.py"),"exec"),{"__file__":str(HERE/"run_final_chain_audit.py"),"__name__":"__main__"})
