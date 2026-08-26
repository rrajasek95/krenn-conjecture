#!/usr/bin/env python3
import hashlib,json
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];U=400_591_699_200
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb")as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def load(n):return json.loads((HERE/n).read_text())
for mf in ["MANIFEST.sha256","SHARD0_MANIFEST.sha256","SHARD1_MANIFEST.sha256","SHARD2_MANIFEST.sha256"]:
 for line in (HERE/mf).read_text().splitlines():
  digest,name=line.split("  ",1);assert sha(HERE/name)==digest
x=load("results_k23_hidden_collected_k18.json");assert x["status"]=="PASS_COMPLETE_HIDDEN_COLLECTED_K18_K23_SINGLETON_CHARGE"
assert x["strict_id"]=="D14:222|R:2-2-2-3" and x["input_interval"]==[0,158439965] and x["input_records"]==158439965
assert x["selected_K18_p3_uses"]==399275484 and x["selected_K20_p4_uses"]==x["pivotable_K20_children"]==570281318
assert x["terminal_K3_tails"]==x["full_occurrences"]==x["irreducible_occurrences"]==18249002176
assert x["full_charge_scaled_U"]==x["irreducible_charge_scaled_U"]=="-1992801869625330597888"
assert Fraction(int(x["full_charge_scaled_U"]),U)==Fraction(x["exact_charge"])==Fraction(-288310455674961024,57955975)
assert sum(x["m2_m3_m4_hist"].values())==570281318 and len(x["shard_evidence"])==3
check=load("results_k23_hidden_collected_k18_independent_audit.json");assert check["status"]=="PASS_INDEPENDENT_COMPLETE_K23_HIDDEN_COLLECTED_MERGE_CHECK"
assert check["source_sha256"]=="442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8" and check["literal_source_records_seek_replayed"]==771
ref=load("results_k23_hidden_collected_k18_literal_referee.json");assert ref["status"]=="PASS_INDEPENDENT_771_LITERAL_H18PIV2_K23_SINGLETON_FULL_REFEREE"
assert ref["distributed_parents"]==771 and ref["literal_terminal_K23_children"]==92608 and ref["sample_charge_scaled_U"]==check["sample_charge_sum_scaled_U"]
assert ref["all_divisions_exact"] and ref["all_K23_children_terminal"] and ref["cache_abstraction_used"] is False
frag=load("k23_hidden_collected_singleton_fragment_manifest.json");assert len(frag["groups"])==1 and frag["groups"][0]["ids"]==[x["strict_id"]]
assert frag["groups"][0]["evidence_sha256"]==sha(HERE/"results_k23_hidden_collected_k18.json")
partial=load("results_k23_hidden_collected_singleton_assembler_partial.json");assert partial["status"]=="REJECT_INCOMPLETE_K23_59_ID_GATE" and not partial["complete_K23_claim"]
assert partial["covered_paths"]==1 and partial["scalar_groups"]==1 and len(partial["missing_paths"])==58 and partial["duplicate_paths"]==partial["extra_paths"]==[]
payload={"status":"PASS_COMPLETE_K23_HIDDEN_COLLECTED_SINGLETON_PACKAGE_AUDIT","degree":23,"strict_id":x["strict_id"],"result_sha256":sha(HERE/"results_k23_hidden_collected_k18.json"),"samples_sha256":sha(HERE/"results_k23_hidden_collected_k18.json.samples.tsv"),"source_sha256":check["source_sha256"],"source_records":158439965,"shard_intervals":[z["interval"] for z in x["shard_evidence"]],"shard_evidence_rehashed":3,"literal_source_seek_replays":771,"literal_recurrence_replays":771,"literal_terminal_children":92608,"scaled_charge":x["full_charge_scaled_U"],"exact_charge":x["exact_charge"],"full_equals_irreducible":True,"strict_assembler_coverage":1,"strict_assembler_remaining":58,"no_rows_or_K24":True,"scope":"one strict K23 singleton fragment; no membership or conjecture verdict"}
logical=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest();payload["logical_sha256"]=logical
(HERE/"results_k23_hidden_collected_complete_package_audit.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n");print(json.dumps({"status":payload["status"],"logical_sha256":logical,"exact_charge":payload["exact_charge"]},indent=2))
