#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/"results_isomorphism_census.json").read_text())
assert r["schema"]=="KRENN_X5_REFINED91_CROSS_REPRESENTATIVE_ISOMORPHISM_CENSUS_V1"
assert r["status"]=="PASS_NO_CROSS_REPRESENTATIVE_ISOMORPHISMS"
assert r["census"]=={"representatives":4,"raw_charts":3888,"within_representative_S3_classes":648,"cross_representative_equivalences":0,"final_equivalence_classes":648}
assert r["site_permutation_isomorphism_counts"]=={str(a):{str(b):(1 if a==b else 0) for b in (1,2,4,5)} for a in (1,2,4,5)}
assert all(v["automorphisms"]==v["canonicalizers"]==1 for v in r["support_graphs"].values())
audit=r["positive_bijection_audit"];assert audit["full_word_generator_maps_checked"]==157464
assert audit["chart_maps"]=={"explicit_chart_bijections":3888,"generator_family_bijections":25571376,"minor_sign_census":{"-1":1944,"1":1944}}
ledger_path=HERE/r["class_ledger"]["path"];assert sha(ledger_path)==r["class_ledger"]["sha256"]
ledger=json.loads(ledger_path.read_text());assert len(ledger["classes"])==648
assert all(x["raw_member_count"]==len(x["raw_members"])==6 and x["cross_representative_members"]==[] for x in ledger["classes"])
assert r["scope"]=={"solver_runs":0,"generator_claims_beyond_verified_bijections":0,"mathematical_closure":False}
assert all(r["hostile_tests"].values())
print(json.dumps({"status":"PASS","result_sha256":sha(HERE/"results_isomorphism_census.json"),"ledger_sha256":sha(ledger_path)},sort_keys=True))
