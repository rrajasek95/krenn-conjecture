#!/usr/bin/env python3
import ast,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();p=json.loads((H/'HELD_PLAN.json').read_text());i=json.loads((H/'results_invariants.json').read_text());h=json.loads((H/'results_hostiles.json').read_text());c=json.loads((H/'CLEARANCE_TEMPLATE.json').read_text())
for script in ('factor_tree_driver.py','run_held.py','prove_invariants.py','build_held.py','validate_held.py','seal_manifest.py'):ast.parse((H/script).read_text())
assert p['status']=='APPROVED_HELD_ZERO_RUN' and p['artifacts']['driver']['sha256']==sha(H/'factor_tree_driver.py') and p['artifacts']['watchdog']['sha256']==sha(H/'run_held.py') and p['artifacts']['invariant_proof']['sha256']==sha(H/'results_invariants.json')
assert i['status']=='PASS_TOY_EXHAUSTIVE_CANONICAL_STATE_INVARIANTS' and i['finite_assignments_checked']==i['unique_state_keys']==27 and i['rep5_nodes_expanded']==i['singular_runs']==0
assert h['status']=='PASS_18_HELD_HOSTILES' and all(h['tests'].values()) and h['rep5_nodes_expanded']==h['launches']==0 and c['approved'] is False and c['nonce']=='REPLACE_ME'
assert not any((H/x).exists() for x in ('CLEARANCE.json','result.json','watchdog.json','stdout.log','stderr.log','checkpoint/CURRENT.json')) and p['scope']['rep5_nodes_expanded']==p['scope']['launches']==p['scope']['singular_runs']==0 and p['scope']['closure_claim'] is False
text=(H/'factor_tree_driver.py').read_text();assert "3^64" not in text and "global_node_cap!=2000000" in text and "args.max_new_nodes<=25000" in text and "PARTIAL_FRONTIER_SEALED" in text and "PASS_EXACT_ALL_18_ROOTS_STRUCTURAL_UNIT" in text
watch=(H/'run_held.py').read_text();assert "libproc.dylib" in watch and "rss_gib')!=8" in watch and "wrapper_wall_seconds')!=510" in watch and "O_EXCL" in watch
print(json.dumps({'status':'PASS_HELD_STATIC_VALIDATION','roots':18,'toy_assignments':27,'hostiles':18,'rep5_nodes':0,'launches':0},sort_keys=True))
