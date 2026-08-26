#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
local=["REPORT.md","build_acceptance_schema.py","build_promotion_design.py","future_dependencies.json","results_hostile_tests.json","results_terminal_promotion_design.json","seal_manifest.py","terminal_promotion_acceptance.schema.json","test_promotion_contract.py","validate.py"]
r=json.loads((H/"results_terminal_promotion_design.json").read_text()); entries=[]
for name in local: entries.append((sha(H/name),name))
for rel,digest in sorted(r["pins"].items()): assert sha(ROOT/rel)==digest; entries.append((digest,os.path.relpath(ROOT/rel,H)))
t=H/"MANIFEST.sha256.tmp"; t.write_text("".join(f"{d}  {p}\n" for d,p in entries)); os.replace(t,H/"MANIFEST.sha256")
print(json.dumps({"status":"SEALED_EXPLICIT_REP2_CONDITIONAL_SCOPE","local":len(local),"external":len(r["pins"]),"lines":len(entries),"manifest_sha256":sha(H/"MANIFEST.sha256")},sort_keys=True))
