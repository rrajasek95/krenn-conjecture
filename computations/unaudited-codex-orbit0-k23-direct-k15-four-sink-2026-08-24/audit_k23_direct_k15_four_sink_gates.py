#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
U=400_591_699_200; SLICES=485; HPS=13_824
NAMES=["D15:{223,232,322}|R:2-2-4","D15:{223,232,322}|R:2-3-3","D15:{223,232,322}|R:3-2-3","D15:{223,232,322}|R:4-4"]
PATHS=[[2,2,4],[2,3,3],[3,2,3],[4,4]]
IDS={NAMES[k]:[f"D15:{p}|R:{'-'.join(map(str,PATHS[k]))}" for p in (223,232,322)] for k in range(4)}
SCHEDULE=ROOT/"computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/results_k23_availability_schedule.json"
STRUCTURE=ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin"
ENGINE=ROOT/"computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs"
AUX=ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin"
CYCLE=ROOT/"computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin"
K4=ROOT/"computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin"

def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(Path(p).read_text())

assert sha(SCHEDULE)=="45550f92ea0cae4d988e1cc1c13117134a6c78a66d68c3e4950d3ec24e2dbb15"
schedule=load(SCHEDULE); artifact=schedule["artifacts"]["orbit0_structure"]
assert artifact["sha256"]==sha(STRUCTURE)=="55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b"
assert sha(AUX)=="f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab"
assert sha(CYCLE)=="8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7"
assert sha(K4)=="4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3"
family=next(x for x in schedule["physical_folds"] if x["family_id"]=="grouped_direct_k15_source")
intervals=[[0,60],[60,121],[121,181],[181,242],[242,303],[303,363],[363,424],[424,485]]
assert family["planned_intervals"]==intervals
assert family["group_ids"]==["source_D15_R2_2_4","source_D15_R2_3_3","source_D15_R3_2_3","source_D15_R4_4"]

gate_rows=[]
for fn,count in [("results_prefix1.json",1),("results_prefix8.json",8),("results_prefix32.json",32)]:
 x=load(HERE/fn); assert x["status"]=="PASS_BOUNDED_GROUPED_DIRECT_K15_FOUR_SINK_K23_GATE"
 assert int(x["scale_U"])==U and x["slice_interval"]==[0,count] and x["source_slices"]==count
 assert x["source_heads_per_slice"]==HPS and set(x["sinks"])==set(NAMES)
 flat=[]
 for k,name in enumerate(NAMES):
  z=x["sinks"][name]; assert z["ids"]==IDS[name] and z["degrees"]==PATHS[k]
  flat+=z["ids"]; assert z["individual_id_charges"] is None
  assert z["source_heads"]==count*HPS
  assert z["full_occurrences"]==z["irreducible_occurrences"]==z["terminal_K23_occurrences"]
  assert z["full_charge_scaled_U"]==z["irreducible_charge_scaled_U"]
  terminal_degree=PATHS[k][-1]; terminal_count={2:12,3:32,4:60}[terminal_degree]
  assert z["terminal_K23_occurrences"]==terminal_count*sum(z["denominator_product_hist"].values())
  assert all(U%int(d)==0 for d in z["denominator_product_hist"])
  last=2 if len(PATHS[k])==3 else 1
  assert z["terminal_K23_occurrences"]==z["stage_tail_candidates"][last]
  if len(PATHS[k])==2: assert z["stage_pivot_uses"][2]==z["stage_tail_candidates"][2]==0
 assert len(flat)==12 and len(set(flat))==12
 assert len({x["sinks"][n]["source_mass"] for n in NAMES})==1
 assert len({x["sinks"][n]["source_l1"] for n in NAMES})==1
 gate_rows.append({"slices":count,"elapsed_seconds":x["elapsed_seconds"],"linear_full_projection_seconds":x["projected_full_seconds"],"result_sha256":sha(HERE/fn),"charges_scaled_U":{n:x["sinks"][n]["full_charge_scaled_U"] for n in NAMES}})

ref=load(HERE/"results_k23_direct_k15_literal_referee.json")
assert ref["status"]=="PASS_INDEPENDENT_257_DISTRIBUTED_LITERAL_DIRECT_K15_FOUR_SINK_K23_REPLAY"
assert ref["source_samples"]==257 and ref["first_slice"]==0 and ref["last_slice"]==484
assert ref["all_divisions_exact"] and ref["all_literal_K23_children_terminal"] and ref["terminal_anchor_signature_mass"]==1
for k,n in enumerate(NAMES):
 z=ref["sinks"][n]; assert z["strict_grouped_ids"]==IDS[n] and z["degrees"]==PATHS[k]
 assert z["samples"]==257 and z["packet_witness_counts"]=={"322":86,"232":86,"223":85}
 assert z["literal_terminal_K23_children"]>0
tsv=(HERE/"k23_direct_k15_literal_samples.tsv").read_text().splitlines()
assert len(tsv)==1+4*257
for j in range(257):
 rows=[line.split("\t") for line in tsv[1+4*j:1+4*(j+1)]]
 ri=j*484//256; packet=j%3
 assert [r[4] for r in rows]==NAMES
 for k,r in enumerate(rows):
  assert int(r[0])==j and int(r[1])==ri and int(r[2])==packet
  assert r[3]==["322","232","223"][packet]
  ms=[int(v) for v in r[10].split(",")]; assert len(ms)==len(PATHS[k]) and all(v>0 for v in ms)
  assert U%__import__("math").prod(ms)==0
  assert int(r[11])%{2:12,3:32,4:60}[PATHS[k][-1]]==0

assert intervals[0][0]==0 and intervals[-1][1]==SLICES and all(intervals[i][1]==intervals[i+1][0] for i in range(7))
projection=gate_rows[-1]["linear_full_projection_seconds"]
max_shard=projection*61/SLICES*2
assert max_shard<540
assert not (HERE/"results_k23_direct_k15_four_sink.json").exists()
payload={
 "status":"PASS_K23_GROUPED_DIRECT_K15_12_ID_PREFIX_GATES_FULL_HELD","degree":23,
 "strict_ids":[x for n in NAMES for x in IDS[n]],"groups":{n:IDS[n] for n in NAMES},"scale_U":U,
 "source":{"path":str(STRUCTURE.relative_to(ROOT)),"sha256":sha(STRUCTURE),"slices":SLICES,"heads_per_slice":HPS,"source_linear_reconstruction":True},
 "engine_pins":{"run_k18_charge.rs":sha(ENGINE),"response_aux":sha(AUX),"cycle_aux":sha(CYCLE),"K4_aux":sha(K4)},
 "prefix_gates":gate_rows,
 "literal_referee":{"status":ref["status"],"sha256":sha(HERE/"results_k23_direct_k15_literal_referee.json"),"ledger_sha256":sha(HERE/"k23_direct_k15_literal_samples.tsv"),"distributed_source_slices":257,"literal_sink_witnesses":1028},
 "recurrence":{"paths":dict(zip(NAMES,PATHS)),"sign":"direct K15 head is -positive; each selected pivot flips sign and divides occurrencewise","all_divisions_exact":True,"terminal_anchor_signature_mass":1,"full_equals_irreducible":True},
 "production_schedule":{"atomic_intervals":intervals,"gap_free_no_overlap":True,"shards":8,"prefix32_linear_full_projection_seconds":projection,"cache_reset_safety_multiplier":2,"conservative_max_shard_seconds":max_shard,"launch_projection_limit_seconds":540,"hard_wall_seconds":600,"family_RSS_limit_GiB":8,"aggregate_RSS_limit_GiB":16,"memory_basis":"per-worker plan plus per-source-slice terminal response cache; cache is dropped each slice; no row output","atomic_results_and_exact_merge_required":True},
 "full_production":{"launched":False,"result_absent":True,"held_pending_explicit_clearance":True},
 "scope":"twelve strict grouped scalar K23 IDs and prefix/referee gates only; no full charge, rows, K24, membership, or conjecture claim"}
logical=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest();payload["logical_sha256"]=logical
(HERE/"results_k23_direct_k15_four_sink_gate_audit.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":payload["status"],"logical_sha256":logical,"conservative_max_shard_seconds":max_shard},indent=2))
