#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/"results_referee.json").read_text())
assert r["status"]=="PASS_EXACT_TRANSPORT_WITH_SELECTED_CARRIER_SCOPE_AND_CURRENT_CLOSURE_LEDGER"
assert r["producer"]=={"manifest_sha256":"afb6b789c12670b81078ff9adda4343b1ba600f2dd9c8a29abd5c09629b5feec","result_sha256":"06f5ce489fe736d080af817c093adc0c3a3dc6b8ba699504fb53722ede4bfa3e","ledger_sha256":"14dcbdd7a2ab777d1012459ca95187965dcc6a833b947d422a6220870346d837"}
s=r["support_census"];assert s["classes"]==[[0,1,4,5,8,9],[2,3,6,7,10,11]] and s["site_maps_tested"]==5806080 and s["unique_within_class"] and s["cross_class_maps"]==0
assert r["literal_transport"]["word_transports"]==472392 and r["literal_transport"]["guard_equations_literal"] and r["literal_transport"]["selected_identity_carrier_literal"]
a=r["A12_reduced_ideal_audit"];assert a["reduced_rank_ideal_A12_free"] and not a["entire_alternative_carrier_catalogue_A12_free"]
c=r["closure_ledger"];assert c["rank3"]["transported_closed_records"]==12
assert c["rank1"]["closed_orbits"]==[0] and c["rank1"]["pending_orbits"]==[1,2,3,4] and c["rank1"]["orbit0_transported_closed_records"]==12
assert c["rank2"]["closed_orbits"]==[] and c["rank2"]["pending_orbits"]==[0,1,2,3,4]
assert c["nonrectangle_records_excluded"]==[12,13,14,15] and not c["full_conjecture_closed"]
assert r["scope"]["solver_runs_by_this_referee"]==0 and not r["scope"]["full_conjecture"]
print(json.dumps({"status":"PASS","result_sha256":h(HERE/"results_referee.json")},sort_keys=True))
