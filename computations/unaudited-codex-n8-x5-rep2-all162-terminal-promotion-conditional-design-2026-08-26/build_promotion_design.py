#!/usr/bin/env python3
"""Build the conditional rep2 all-162 ledger; never run an ideal solver."""
from __future__ import annotations
import hashlib, json, os
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def P(rel): return ROOT/rel
PINS={
 "computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25/MANIFEST.sha256":"ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2",
 "computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25/results_rep2_corrected_contraction_design.json":"ed37c2e0da8088e08fb6891e60768d98fbbbf031935f752b4e4af280dfe27b26",
 "computations/unaudited-codex-n8-x5-rep2-corrected-contraction-modular-held-referee-2026-08-25/FINAL_MANIFEST.sha256":"986f819fcb4bcaa17bebaa60047624b16187f755d94897397acc372db6328692",
 "computations/unaudited-codex-n8-x5-rep2-corrected-contraction-modular-held-referee-2026-08-25/results_referee.json":"ff67c84c8882f3ee8b404319b737a773ac89dca0977f289f6c119aa0f08c9892",
 "computations/unaudited-codex-n8-x5-seven-block-rep2-exhaustive-carrier-closure-2026-08-25/MANIFEST.sha256":"8fe367273a44dd33c485d5c80976226138c920f64fe412245067b5fdc429b966",
 "computations/unaudited-codex-n8-x5-seven-block-rep2-exhaustive-carrier-closure-2026-08-25/results_rep2_exhaustive_carrier.json":"6ad0d0c171ffebf8825cd12b71ffca9dc8abbe8ecd26956c02b90ebcad53d7da",
 "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-run-2026-08-25/FINAL_MANIFEST.sha256":"c9298394d37022b384e8117280bfcdc39422ca24f57173da699a39dac11fb62a",
 "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-run-2026-08-25/results_independent_referee.json":"a3d3738b22c98c23ffaad2d5cd6c94b4ad9724acbcfeeebfbe4d89c98b39f39c",
 "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-second-referee-2026-08-25/FINAL_MANIFEST.sha256":"c856fae641e355a94684c1c9304ead831d213ecc90f579c0a751c93002c10562",
 "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-second-referee-2026-08-25/results_referee.json":"806e5b7b0ef72ca39fe725248cca1055342c0ea64577af6944945ab48702e9a2",
 "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25/MANIFEST.sha256":"d694841e71b7982f50449b033ae21fb5798bd0ae765f75a9d655909a8c61022c",
 "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25/canonical_census.json":"5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a",
 "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25/source_ledger.json":"20737fd8197335f98214222bc5caa4c3d8c1ba2b2fcc283065d865befcf6389e",
 "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-referee-2026-08-26/FINAL_MANIFEST.sha256":"63052b073a025dae732102cb5efe5636aae3c9a5c16811d53440278f5879599a",
 "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-referee-2026-08-26/results_referee.json":"0276814e2f1aa9f7f8a6c4b8cac0f76305ae241bb66576041c3deb58b28da2af",
 "computations/unaudited-codex-n8-x5-rep2-groups26-75-exact-q-conditional-held-2026-08-26/MANIFEST.sha256":"07c356ff169a8586add38bb8cb808977570a1ad83f001fb4918c5da163ef0f38",
 "computations/unaudited-codex-n8-x5-rep2-groups26-75-exact-q-conditional-held-2026-08-26/source_ledger.json":"0a9ad8dfb140d8e601c88429c13945d1182ac6dffe2c7dcc022a1b353a1005e7",
 "computations/unaudited-codex-n8-x5-rep2-groups26-75-exact-q-conditional-held-referee-2026-08-26/FINAL_MANIFEST.sha256":"3ec13a27f9a92ace66338e0161a7987f71dc01f7cf9866f9d08cd42e406e90fd",
 "computations/unaudited-codex-n8-x5-rep2-groups26-75-exact-q-conditional-held-referee-2026-08-26/results_referee.json":"442f34d365e5954f5984b4780113c949e761488f2c27a8e782a9c70998b7cbba",
 "computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-v2-2026-08-26/MANIFEST.sha256":"f62e7a7ee38ca747dfd2ac88774d9ee4251f73ef514e2410ddba092da9830d6b",
 "computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-v2-2026-08-26/source_reference_ledger.json":"6f44241c35e197d557238a405c7549348a39e0f60d8f03f4d092eb3945ca9083",
 "computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-v2-referee-2026-08-26/FINAL_MANIFEST.sha256":"f98201582c3c506cbf08a68428e3d018bb51ecae33850c971be9545c677d0f7b",
 "computations/unaudited-codex-n8-x5-rep2-groups76-125-exact-q-conditional-held-v2-referee-2026-08-26/results_referee.json":"d95ba0dc421d8967d99bd05df4887440788f54acb9c6cbd3684ede7b68fa6ef0",
 "computations/unaudited-codex-n8-x5-rep2-groups126-161-exact-q-conditional-held-2026-08-26/MANIFEST.sha256":"83c87103e2414b48d37724ce803c747ee0d2c9a9f757353c172bb17226477147",
 "computations/unaudited-codex-n8-x5-rep2-groups126-161-exact-q-conditional-held-2026-08-26/source_ledger.json":"c34b3616bef36d49c63904e676c540208a24dd2057eb176153ad03034db0b8a6",
 "computations/unaudited-codex-n8-x5-rep2-groups126-161-exact-q-conditional-held-referee-2026-08-26/FINAL_MANIFEST.sha256":"d877c2a7a27767bd7dd67657102bb58585ce11a7202ea502f084c3e84fee3d10",
 "computations/unaudited-codex-n8-x5-rep2-groups126-161-exact-q-conditional-held-referee-2026-08-26/results_referee.json":"223b1b2a344f5e8b11b804e084673c407bca91cd976a0d1150dbdb7c7e6577da",
}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(rel): return json.loads(P(rel).read_text())
for rel,digest in PINS.items(): assert sha(P(rel))==digest,(rel,sha(P(rel)),digest)
design=load("computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25/results_rep2_corrected_contraction_design.json")
assert design["status"]=="PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN"
assert design["chart_census"]=={"S3_orbits":162,"orbit_size":6,"raw":972,"y_orbits":81,"z_orbits":81}
assert design["counts"]["new_variables"]==91 and design["counts"]["new_generators"]==6577
census=load("computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25/canonical_census.json")
assert census["counts"]=={"canonical_groups":162,"members_each":6,"raw":972,"y_groups":81,"z_groups":81}
records=census["groups"]; assert [x["group_id"] for x in records]==list(range(162))
transport=[]; raw=[]
for x in records:
 members=[tuple(v) for v in x["raw_members"]]
 assert len(members)==len(set(members))==x["raw_member_count"]==6
 raw.extend(members)
 transport.append({"group_id":x["group_id"],"family":x["family"],"canonical_chart":x["canonical_chart"],"raw_s3_members":x["raw_members"],"raw_member_count":6,"exact_Q_source_sha256":x["exact_Q_source_sha256"]})
assert len(raw)==len(set(raw))==972
assert sum(x["family"]=="y" for x in records)==sum(x["family"]=="z" for x in records)==81
rank0=load("computations/unaudited-codex-n8-x5-seven-block-rep2-exhaustive-carrier-closure-2026-08-25/results_rep2_exhaustive_carrier.json")
assert rank0["proof"]["closed_rank_scope"]==[0] and rank0["scope"]["rank_zero_closed"] is True
assert rank0["proof"]["pairing_only_rank_scope"]==[1,2,3]
group0=load("computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-run-2026-08-25/results_independent_referee.json")
group0b=load("computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-exact-q-second-referee-2026-08-25/results_referee.json")
assert group0["status"]=="PASS_EXACT_Q_ONE_REFINED_CHART_ONLY" and group0b["status"]=="PASS_EXACT_Q_ONE_REFINED_REP2_CHART_ONLY"
assert census["closed_group_identification"]["group_id"]==0 and census["closed_group_identification"]["source_sha256"]=="5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf"
future=json.loads((HERE/"future_dependencies.json").read_text())
assert future["satisfied"] is False and all(x["manifest_sha256"] is x["result_sha256"] is None for x in future["dependencies"])
shards=[[0]]+[x["group_ids"] for x in future["dependencies"]]
flat=[v for s in shards for v in s]; assert len(flat)==len(set(flat))==162 and sorted(flat)==list(range(162))
result={
 "schema":"KRENN_X5_REP2_ALL162_TERMINAL_PROMOTION_CONDITIONAL_DESIGN_V1",
 "status":"HELD_PROMOTION_FOUR_FUTURE_PASS_SEALS_ABSENT",
 "authoritative_contraction":{"raw_charts":972,"canonical_s3_charts":162,"members_per_chart":6,"variables_each":91,"generators_each":6577,"y_groups":81,"z_groups":81,"y_raw":486,"z_raw":486,"corrected_carrier":"A06^T*K*[A23^T|A35]","forward_reverse_localization":True},
 "rank_zero_structural_branch":{"outside_factor":"A57","closed_rank_scope":[0],"implications":rank0["proof"]["zero_A57"],"nonzero_rank_scope_not_claimed":[1,2,3],"source_pin_scope":"rank-zero clause only; nonzero pairing-only scope is not promoted"},
 "sealed_group0":{"group_id":0,"canonical_chart":records[0]["canonical_chart"],"exact_Q_source_sha256":records[0]["exact_Q_source_sha256"],"independent_q_seals":2,"status":"SEALED_EXACT_Q_CLOSED"},
 "closure_shards":[{"group_ids":[0],"status":"SEALED_EXACT_Q_CLOSED","dependency_hashes_null":False}]+[{"group_ids":x["group_ids"],"status":"FUTURE_INDEPENDENT_PASS_REQUIRED","dependency_hashes_null":True} for x in future["dependencies"]],
 "prospective_union_proof":{"group_count":162,"union":list(range(162)),"duplicates":[],"missing":[],"extra":[],"all_four_future_batches_required":True},
 "raw_s3_transport":transport,
 "held_readiness_bindings":{"batches":["1..25","26..75","76..125-v2","126..161"],"all_producer_and_referee_packages_pinned":True,"terminal_closure_results_present":False,"held_approval_is_not_closure":True},
 "scope":{"representative":"rep2 only","full_family":"rank-zero structural branch plus all 972 localized nonzero raw charts of rep2","transport":"simultaneous S3 color renaming only within each source-labelled rep2 chart","cross_representative_transport":False,"other_representatives_closed":[],"full_conjecture":False,"promotion_currently_authorized":False,"solver_runs":0},
 "pins":PINS,
}
tmp=HERE/"results_terminal_promotion_design.json.tmp"; tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); os.replace(tmp,HERE/"results_terminal_promotion_design.json")
print(json.dumps({"status":result["status"],"groups":162,"raw":972,"future_hash_pairs_null":4},sort_keys=True))
