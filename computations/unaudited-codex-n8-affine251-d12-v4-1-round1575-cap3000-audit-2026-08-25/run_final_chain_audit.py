#!/usr/bin/env python3
"""Execute the pinned six-edge referee with audited r1575 substitutions."""
import hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
T=H.parent/"unaudited-codex-n8-affine251-d12-v4-1-round1538-cap2750-audit-2026-08-25/run_final_chain_audit.py"
raw=T.read_bytes();assert hashlib.sha256(raw).hexdigest()=="e4d15771f336a4997fa705192bd001fad250b8611d2f6f3ce75614b41f8ec8ff"
s=raw.decode()
old='ia=load(R/P["input_audit"]);need(ia["status"]=="PASS_EXACT_DIRECT_CAP2500_TO_CAP2750_EQUIVALENCE" and ia["accepted_candidate"]=="candidate_cap2750" and ia["checkpoint_sha256"]==P["input_checkpoint_sha256"] and ia["vectors_sha256"]==P["input_vectors_sha256"],"input audit")'
new='ia=load(R/P["input_audit"]);need(ia["status"]=="PASS_EXACT_DIRECT_CAP2750_TO_CAP3000_EQUIVALENCE" and ia["accepted_candidate"]=="candidate_cap3000" and ia["checkpoint_sha256"]==P["input_checkpoint_sha256"] and ia["vectors_sha256"]==P["input_vectors_sha256"],"input audit")'
assert s.count(old)==1
replacements={
 'range(1528,1539)':'range(1564,1576)',
 'results_round1538_all_column_replay.json':'results_round1575_all_column_replay.json',
 'replay["round"]==1538':'replay["round"]==1575',
 'KRENN_AFFINE251_D12_V4_1_ROUND1538_CAP2750_CHAIN_AUDIT_V1':'KRENN_AFFINE251_D12_V4_1_ROUND1575_CAP3000_CHAIN_AUDIT_V1',
 'PASS_EXACT_FULLY_TELEMETERED_ROUND1538_CAP2750_CHAIN':'PASS_EXACT_FULLY_TELEMETERED_ROUND1575_CAP3000_CHAIN',
 'Accepted r1527 cap2.75m state through exact rounds1528..1538; no r1539 or closure claim.':'Accepted r1563 cap3.0m state through exact rounds1564..1575; no r1576 or closure claim.',
 '"input":{"round":1527':'"input":{"round":1563',
 '"final":{"round":1538':'"final":{"round":1575',
 'Round1538 is exact and resumable, not a terminal global dual.':'Round1575 is exact and resumable, not a terminal global dual.',
 'results_round1538_chain_audit.json':'results_round1575_chain_audit.json'
}
for a,b in replacements.items():assert s.count(a)>=1,(a,s.count(a));s=s.replace(a,b)
s=s.replace(old,new)
exec(compile(s,str(H/"run_final_chain_audit.py"),"exec"),{"__file__":str(H/"run_final_chain_audit.py"),"__name__":"__main__"})
