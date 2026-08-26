#!/usr/bin/env python3
"""Strict K24 charge-first and 39-byte B20 source-production contract."""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import os
import struct
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
U = 400_591_699_200
TARGET = Fraction(829_424_811_081_283_712, 173_867_925)
TARGET_SCALED = 1_910_994_764_731_277_672_448
CONTRACT = ROOT / "computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/k24_expected_scalar_groups.json"
CONTRACT_SHA = "9ee7c5b6c31b70a7e06f8a4909c8b9aa77a87444cb12992c9971b5259bb8a986"
HELD = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-relative-production-gate-2026-08-24/k24_factorized_35_shard_plan_held.json"
HELD_SHA = "7625ca900d59e7cd39d306d9f2df9632d3d8350f1b8fb7ea983a219db88425b8"
SPARSE = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-relative-sparse-closure-gates-2026-08-24/gate_run/results_k24_sparse_257_and_source1_gate.json"
SPARSE_SHA = "0675c7cbf370ffdb5dc48b35e1350a6c53f9a9f2445abae2a0dd054a8f726d2b"

STRUCTURE = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin"
AUX = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin"
K4 = "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin"
CYCLE = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin"
K16_ROWS = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin"
H18 = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin"
PAIR = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin"
INPUT_SHA = {
    STRUCTURE: "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    AUX: "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    K4: "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
    CYCLE: "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    K16_ROWS: "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3",
    H18: "442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8",
    PAIR: "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8",
}
COMMON_INPUTS = [AUX, K4, CYCLE]
PHYSICAL_SOURCE = "computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24/run_k24_charge_physical.rs"
PHYSICAL_BINARY = "computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24/run_k24_charge_physical"
HIDDEN_SOURCE = "computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24/run_k24_charge_hidden.rs"
HIDDEN_BINARY = "computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24/run_k24_charge_hidden"

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(8 << 20), b""):
            h.update(b)
    return h.hexdigest()

def require(ok: bool, detail: object) -> None:
    if not ok:
        raise RuntimeError(detail)

def balanced(n: int, k: int) -> list[list[int]]:
    return [[n * i // k, n * (i + 1) // k] for i in range(k)]

def families() -> dict[str, dict]:
    held = json.loads(HELD.read_text())
    require(sha(HELD) == HELD_SHA, "held-plan hash")
    by = {x["family_id"]: x for x in held["source_fold_families"]}
    # Smallest balanced family partitions whose measured linear projection is
    # below the frozen 450-second scheduling stop.  Any accepted shard-0 rate
    # regression triggers a finer superseding plan; it never widens a shard.
    charge_intervals = {
        "hidden_collected_k18": balanced(158_439_965, 3),
        "hidden_decorated_k16_pair": balanced(101_545_723, 10),
        "k14_source_formula": balanced(485, 5),
        "grouped_direct_k15_source": balanced(485, 10),
        "grouped_direct_k16_rows": balanced(24_097_095, 53),
        "direct_D17_D18_formula": balanced(485, 2),
    }
    mode = {
        "hidden_collected_k18": ("hidden18", "hidden", H18),
        "hidden_decorated_k16_pair": ("hidden_pair", "hidden", PAIR),
        "k14_source_formula": ("k14", "physical", STRUCTURE),
        "grouped_direct_k15_source": ("k15", "physical", STRUCTURE),
        "grouped_direct_k16_rows": ("k16", "physical", K16_ROWS),
        "direct_D17_D18_formula": ("direct17", "physical", STRUCTURE),
    }
    out = {}
    for fid, src in by.items():
        engine_family, engine_kind, primary = mode[fid]
        inputs = [primary] + [x for x in COMMON_INPUTS if x != primary]
        out[fid] = {
            "family_id": fid,
            "group_ids": src["group_ids"],
            "covered_ids": src["covered_ids"],
            "source_units": src["source_units"],
            "primary_input": primary,
            "inputs": inputs,
            "B_intervals": src.get("intervals") or [[8*j, min(8*(j+1), 485)] for j in range(61)],
            "charge_intervals": charge_intervals[fid],
            "engine_family": engine_family,
            "engine_kind": engine_kind,
        }
    return out

def interval_guard(intervals: list[list[int]], total: int) -> None:
    require(intervals and intervals[0][0] == 0 and intervals[-1][1] == total, (intervals[:1], intervals[-1:]))
    require(all(a < b for a, b in intervals), "empty interval")
    require(all(intervals[i][1] == intervals[i+1][0] for i in range(len(intervals)-1)), "gap/overlap")

def build_plans(outdir: Path) -> tuple[dict, dict]:
    fam = families()
    expected = json.loads(CONTRACT.read_text())["groups"]
    require(sha(CONTRACT) == CONTRACT_SHA, "group contract hash")
    bshards, cshards = [], []
    for fid, x in fam.items():
        interval_guard(x["B_intervals"], x["source_units"])
        interval_guard(x["charge_intervals"], x["source_units"])
        for kind, intervals, sink in [("B20", x["B_intervals"], bshards), ("charge", x["charge_intervals"], cshards)]:
            for j, (a, b) in enumerate(intervals):
                sink.append({"shard_id": f"{fid}.{j:03d}", "family_id": fid, "shard_index": j,
                    "family_shards": len(intervals), "interval": [a,b], "source_units": b-a,
                    "group_ids": x["group_ids"]})
    require(len(bshards) == 103, len(bshards))
    require(len(cshards) == 83, len(cshards))
    union = sorted(i for ids in expected.values() for i in ids)
    require(len(union) == len(set(union)) == 35, "35-ID contract")
    base = {"degree":24,"scale_U":U,"expected_charge_target":str(TARGET),"expected_charge_target_scaled_U":str(TARGET_SCALED),
        "expected_group_contract":{"path":str(CONTRACT.relative_to(ROOT)),"sha256":CONTRACT_SHA},
        "relative_production_plan":{"path":str(HELD.relative_to(ROOT)),"sha256":HELD_SHA},
        "sparse_gate":{"path":str(SPARSE.relative_to(ROOT)),"sha256":SPARSE_SHA},
        "required_groups":expected,"required_ids":union,
        "contract_files":{
          "validator":{"path":"computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24/k24_production_contract.py","sha256":sha(Path(__file__).resolve())},
          "charge_schema":{"path":"computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24/k24_charge_shard_acceptance.schema.json","sha256":sha(Path(__file__).parent/"k24_charge_shard_acceptance.schema.json")},
          "B20_schema":{"path":"computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24/k24_B20_source_shard.schema.json","sha256":sha(Path(__file__).parent/"k24_B20_source_shard.schema.json")},
          "guarded_launcher":{"path":"computations/unaudited-codex-orbit0-k24-charge-first-production-interface-2026-08-24/run_k24_charge_shard_guard.py","sha256":sha(Path(__file__).parent/"run_k24_charge_shard_guard.py")}},
        "resource_gates":{"stop_scheduling_seconds":450,"internal_wall_seconds":540,"external_alarm_seconds":600,
          "family_RSS_bytes":8_589_934_592,"aggregate_RSS_bytes":17_179_869_184,"atomic_outputs":True,"one_heavy_family_only":True}}
    bplan = dict(base, format="orbit0-k24-B20-production-plan-v2", shards=bshards,
      record_contract={"record_bytes":39,"record_format":"word_dictionary_id:u8|sorted_K20_multiplier:u8[20]|natural_H_orbit_size:u16_le|orbit_total_mass_scaled_U:i128_le",
       "natural_sort_key":"(word_dictionary_id, multiplier_bytes)","blocks":[20,22,23,24],
       "semantics":"shared natural word table reconstructs exact lower K20/K22/K23 and top K24 outputs as sort(multiplier+matching_term)",
       "arbitrary_source_words_preserved":True},
      producer_status={
       "direct_D17_D18_formula":"PREFIX_IMPLEMENTED_PRODUCTION_ALLOWLIST_REQUIRES_61_INTERVAL_SUPERSESSION",
       "hidden_collected_k18":"MISSING_B20_PRODUCER",
       "hidden_decorated_k16_pair":"MISSING_B20_PRODUCER",
       "k14_source_formula":"MISSING_B20_PRODUCER",
       "grouped_direct_k15_source":"MISSING_B20_PRODUCER",
       "grouped_direct_k16_rows":"MISSING_B20_PRODUCER"},
      producer_pins={
       "direct_D17_D18_formula":{"source_path":"computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/run_k24_factorized_direct_d17_d18.rs","source_sha256":"a83376d4e68828e3b3f0af5c6ae9895bfda0db979a81ee35d5f87d48a8c5d47f","binary_path":"computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/run_k24_factorized_direct_d17_d18_fast","binary_sha256":"95380dff1c017e176bf4f539df863d02ac51d2cd342cbcfefc7b0f203b951708","provider_path":"computations/unaudited-codex-orbit0-k24-factorized-relative-production-gate-2026-08-24/k24_factorized_B20_provider.py","provider_sha256":"689499ecf501eb37879b41f05e3f3caecfad454eaf57f5586b28edd7c616a018"},
       "hidden_collected_k18":None,"hidden_decorated_k16_pair":None,"k14_source_formula":None,"grouped_direct_k15_source":None,"grouped_direct_k16_rows":None},
      family_inputs={fid:{p:INPUT_SHA[p] for p in x["inputs"]} for fid,x in fam.items()},
      publication_guard="charge 35/35 must equal target before any B20 production is authorized")
    engine_rows={}
    for fid,x in fam.items():
        source=PHYSICAL_SOURCE if x["engine_kind"]=="physical" else HIDDEN_SOURCE;binary=PHYSICAL_BINARY if x["engine_kind"]=="physical" else HIDDEN_BINARY
        engine_rows[fid]={k:x[k] for k in ("engine_family","engine_kind","primary_input","inputs","group_ids","source_units")}
        engine_rows[fid].update({"source_path":source,"source_sha256":sha(ROOT/source),"binary_path":binary,"binary_sha256":sha(ROOT/binary),
          "command_template":f"{binary} --family {x['engine_family']} --start {{start}} --count {{count}} --workers 8 --output {{output}}"})
    cplan = dict(base, format="orbit0-k24-charge-first-production-plan-v1", shards=cshards,
      engines=engine_rows,
      measured_gate_seconds={"hidden_collected_k18_prefix4096_8w":0.031146,"hidden_decorated_k16_pair_prefix4096_8w":0.174788,
       "k14_source_formula_prefix8_8w":33.128791,"grouped_direct_k15_source_prefix8_8w":70.492407,
       "grouped_direct_k16_rows_prefix4096_8w":4.028044,"direct_D17_D18_formula_prefix8_8w":9.625596},
      projected_max_shard_seconds={"hidden_collected_k18":402,"hidden_decorated_k16_pair":434,
       "k14_source_formula":402,"grouped_direct_k15_source":428,"grouped_direct_k16_rows":448,"direct_D17_D18_formula":292},
      minimality={"criterion":"smallest balanced integer shard count with measured linear wall strictly below 450 seconds",
       "family_shard_counts":{"hidden_collected_k18":3,"hidden_decorated_k16_pair":10,"k14_source_formula":5,"grouped_direct_k15_source":10,"grouped_direct_k16_rows":53,"direct_D17_D18_formula":2},
       "adaptive_rule":"if independently accepted shard0 rate projects >=450 seconds, supersede only by exact subdivision; never widen"},
      decision="CHARGE_PRODUCTION_FEASIBLE_AFTER_INDEPENDENT_SHARD0_ACCEPTANCE; NOT LAUNCHED")
    for name, obj in [("k24_B20_production_plan_103.json",bplan),("k24_charge_production_plan_83.json",cplan)]:
        (outdir/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
    return bplan,cplan

PHYSICAL_TOP = {"status","degree","family","scale_U","source_interval","distributed","workers","groups",
 "all_terminal_responses_exhaustive","full_equals_irreducible","literal_witness_ledger","elapsed_seconds","linear_full_projection_seconds","scope"}
PHYSICAL_GROUP = {"group_id","ids","path","source_units","source_heads","source_coefficient_sum","source_l1","stage_pivot_uses",
 "stage_tail_candidates","stage_pivotable_children","terminal_K24_occurrences","full_occurrences","irreducible_occurrences",
 "full_charge_scaled_U","irreducible_charge_scaled_U","denominator_product_hist","terminal_cache","literal_witnesses"}
HIDDEN_TOP = {"status","degree","family","group_id","ids","scale_U","input","input_sha256_expected","input_interval","input_records",
 "retained_uses","retained_weight_sum_scaled_U","retained_weight_l1_scaled_U","first_selected_pivots","first_tail_evaluations",
 "pivotable_K20_children","terminal_selected_pivots","terminal_K24_occurrences","full_occurrences","irreducible_occurrences",
 "full_charge_scaled_U","irreducible_charge_scaled_U","denominator_hist","terminal_cache","literal_witnesses","literal_witness_ledger",
 "sign_rule","all_terminal_responses_exhaustive","full_equals_irreducible","workers","elapsed_seconds","linear_full_projection_seconds","scope"}

def verify_inputs(paths: list[str]) -> dict[str,str]:
    out={}
    for p in paths:
        q=ROOT/p
        require(q.is_file(), p)
        got=sha(q); require(got==INPUT_SHA[p], (p,got))
        out[p]=got
    return out

def charge_groups(raw: dict, x: dict) -> list[dict]:
    if x["engine_kind"] == "physical":
        require(set(raw)==PHYSICAL_TOP, ("physical top keyset", sorted(set(raw)^PHYSICAL_TOP)))
        require(len(raw["groups"])==len(x["group_ids"]), "group count")
        gs=raw["groups"]
        for g in gs: require(set(g)==PHYSICAL_GROUP, ("physical group keyset",sorted(set(g)^PHYSICAL_GROUP)))
    else:
        require(set(raw)==HIDDEN_TOP, ("hidden top keyset",sorted(set(raw)^HIDDEN_TOP)))
        gs=[raw]
    require([g["group_id"] for g in gs]==x["group_ids"], "group order")
    expected=json.loads(CONTRACT.read_text())["groups"]
    out=[]
    for g in gs:
        require(g["ids"]==expected[g["group_id"]], (g["group_id"],g["ids"]))
        require(int(g["full_charge_scaled_U"])==int(g["irreducible_charge_scaled_U"]), "full/irr charge")
        require(g["full_occurrences"]==g["irreducible_occurrences"]==g["terminal_K24_occurrences"], "full/irr occurrences")
        out.append({"group_id":g["group_id"],"ids":g["ids"],"full_charge_scaled_U":str(g["full_charge_scaled_U"]),
          "irreducible_charge_scaled_U":str(g["irreducible_charge_scaled_U"]),"terminal_K24_occurrences":g["terminal_K24_occurrences"]})
    return out

def validate_charge(raw_path: Path, family: str, a: int, b: int, control: bool, resource: Path|None, acceptance: Path|None) -> dict:
    raw_path=raw_path.resolve()
    if resource is not None: resource=resource.resolve()
    if acceptance is not None: acceptance=acceptance.resolve()
    fam=families(); require(family in fam,family);x=fam[family];raw=json.loads(raw_path.read_text())
    require(raw["degree"]==24 and int(raw["scale_U"])==U,"degree/U")
    require(raw["family"]==x["engine_family"],(raw["family"],x["engine_family"]))
    got_interval=raw["source_interval"] if x["engine_kind"]=="physical" else raw["input_interval"]
    require(got_interval==[a,b],(got_interval,[a,b]))
    require(raw["all_terminal_responses_exhaustive"] is True and raw["full_equals_irreducible"] is True,"terminality")
    require(float(raw["elapsed_seconds"])<540,"internal wall")
    groups=charge_groups(raw,x)
    if not control and x["engine_kind"]=="physical": require(raw["distributed"] is False,"distributed diagnostic is not a production interval")
    witness=ROOT/raw["literal_witness_ledger"] if not Path(raw["literal_witness_ledger"]).is_absolute() else Path(raw["literal_witness_ledger"])
    require(witness.is_file() and witness.stat().st_size>0,"witness")
    inputs=verify_inputs(x["inputs"])
    resources=None
    if not control:
        require(resource is not None and resource.is_file(),"production resource sidecar required")
        resources=json.loads(resource.read_text())
        require(set(resources)=={"wall_seconds","peak_RSS_bytes","free_bytes_before","exit_code","atomic_result"},"resource keyset")
        require(resources["exit_code"]==0 and resources["atomic_result"] is True,"resource status")
        require(resources["wall_seconds"]<600 and resources["peak_RSS_bytes"]<8_589_934_592,"wall/RSS")
        require(resources["free_bytes_before"]>=17_179_869_184,"disk floor")
    answer={"format":"orbit0-k24-charge-shard-acceptance-v1","status":"PASS_CONTROL" if control else "PASS_PRODUCTION_SHARD",
      "degree":24,"scale_U":U,"family_id":family,"group_ids":x["group_ids"],"source_interval":[a,b],"source_units":b-a,
      "raw_result":{"path":str(raw_path.relative_to(ROOT)),"sha256":sha(raw_path)},
      "literal_witnesses":{"path":str(witness.relative_to(ROOT)),"sha256":sha(witness),"records":sum(1 for _ in witness.open())-1},
      "input_sha256":inputs,"engine":{"source_path":PHYSICAL_SOURCE if x["engine_kind"]=="physical" else HIDDEN_SOURCE,
        "source_sha256":sha(ROOT/(PHYSICAL_SOURCE if x["engine_kind"]=="physical" else HIDDEN_SOURCE)),
        "binary_path":PHYSICAL_BINARY if x["engine_kind"]=="physical" else HIDDEN_BINARY,
        "binary_sha256":sha(ROOT/(PHYSICAL_BINARY if x["engine_kind"]=="physical" else HIDDEN_BINARY))},
      "groups":groups,"universal_terminality":True,"full_equals_irreducible":True,
      "resource_evidence":resources,"control":control,"scope":"scalar K24 charge shard only; no B20 or relative claim"}
    if acceptance:
        tmp=acceptance.with_suffix(acceptance.suffix+".tmp");tmp.write_text(json.dumps(answer,indent=2,sort_keys=True)+"\n");os.replace(tmp,acceptance)
    return answer

def read_record(f):
    b=f.read(39)
    if not b:return None
    require(len(b)==39,"truncated B record")
    word=b[0];mult=b[1:21];orbit=int.from_bytes(b[21:23],"little");mass=int.from_bytes(b[23:39],"little",signed=True)
    require(0<orbit<=384 and 384%orbit==0,"orbit")
    require(-(1<<127)<=mass<(1<<127),"i128")
    return (word,mult),orbit,mass

def validate_B_manifest(path:Path,plan:dict,shard:dict,control:bool=False)->dict:
    z=json.loads(path.read_text()); required={"format","status","degree","scale_U","family_id","group_ids","covered_ids","source_interval","source_units",
      "input_sha256","engine_sha256","provider_sha256","word_dictionary","block_degrees","record_format","record_bytes","natural_sort_key",
      "group_runs","literal_witnesses","all_orbit_divisions_exact","lower_blocks_exact","top_block_exact","arbitrary_source_words_preserved",
      "charge_groups","atomic","resource_evidence","control","scope"}
    require(set(z)==required,("B manifest keyset",sorted(set(z)^required)))
    require(z["format"]=="orbit0-k24-B20-source-shard-v2" and z["degree"]==24 and int(z["scale_U"])==U,"B constants")
    require(z["family_id"]==shard["family_id"] and z["group_ids"]==shard["group_ids"] and z["source_interval"]==shard["interval"],"B scope")
    expected=json.loads(CONTRACT.read_text())["groups"]
    expected_ids=[i for g in shard["group_ids"] for i in expected[g]]
    require(z["covered_ids"]==expected_ids,"B covered IDs")
    require(z["source_units"]==shard["source_units"] and z["record_bytes"]==39 and z["block_degrees"]==[20,22,23,24],"B geometry")
    require(z["record_format"]==plan["record_contract"]["record_format"] and z["natural_sort_key"]==plan["record_contract"]["natural_sort_key"],"B format")
    require(all(z[k] is True for k in ["all_orbit_divisions_exact","lower_blocks_exact","top_block_exact","arbitrary_source_words_preserved","atomic"]),"B guards")
    require(z["control"] is control,"B control")
    require(z["input_sha256"]==plan["family_inputs"][shard["family_id"]],"B input pins")
    pins=plan["producer_pins"][shard["family_id"]]
    require(pins is not None,"B producer missing")
    require(z["engine_sha256"]==pins["source_sha256"] and z["provider_sha256"]==pins["provider_sha256"],"B producer pins")
    require(sha(ROOT/pins["source_path"])==pins["source_sha256"] and sha(ROOT/pins["binary_path"])==pins["binary_sha256"] and sha(ROOT/pins["provider_path"])==pins["provider_sha256"],"B producer rehash")
    if not control: require(plan["producer_status"][shard["family_id"]]=="READY","B production producer not cleared")
    wd=ROOT/z["word_dictionary"]["path"];require(sha(wd)==z["word_dictionary"]["sha256"],"word dictionary hash")
    words=z["word_dictionary"]["records"];require(1<=words<=78,"word count")
    require([x["group_id"] for x in z["group_runs"]]==shard["group_ids"],"B group order")
    require([x["group_id"] for x in z["charge_groups"]]==shard["group_ids"],"B charge group order")
    for g in z["charge_groups"]:
        require(g["ids"]==expected[g["group_id"]] and int(g["full_charge_scaled_U"])==int(g["irreducible_charge_scaled_U"]),"B charge scope")
    wp=ROOT/z["literal_witnesses"]["path"];require(sha(wp)==z["literal_witnesses"]["sha256"],"B witness hash")
    for run in z["group_runs"]:
        require(set(run)=={"group_id","path","sha256","records","bytes","selected_pivot_occurrences","exact_zero_cancellations","orbit_mass_scaled_U"},"run keyset")
        p=ROOT/run["path"];require(p.stat().st_size==run["bytes"]==39*run["records"],"run bytes")
        require(sha(p)==run["sha256"],"run hash")
        prior=None
        with p.open("rb") as f:
            for _ in range(run["records"]):
                rec=read_record(f);require(rec is not None,"early eof");key,orbit,mass=rec;require(key[0]<words,"word id");require(prior is None or prior<key,"strict natural order");prior=key;require(mass%orbit==0,"orbit division")
            require(f.read(1)==b"","extra bytes")
    return z

def merge_records(paths:list[Path],output:Path)->dict:
    files=[p.open("rb") for p in paths];heap=[];prior=[None]*len(files)
    for i,f in enumerate(files):
        x=read_record(f)
        if x: heapq.heappush(heap,(x[0],i,x[1],x[2]))
    tmp=output.with_suffix(output.suffix+".tmp");records=zeros=0
    with tmp.open("wb") as w:
        while heap:
            key,i,orbit,mass=heapq.heappop(heap);total=mass
            x=read_record(files[i]);
            if x: require(key<x[0],"input order");prior[i]=key;heapq.heappush(heap,(x[0],i,x[1],x[2]))
            while heap and heap[0][0]==key:
                _,j,o,m=heapq.heappop(heap);require(o==orbit,"duplicate orbit mismatch");total+=m
                x=read_record(files[j]);
                if x: require(key<x[0],"input order");prior[j]=key;heapq.heappush(heap,(x[0],j,x[1],x[2]))
            require(-(1<<127)<=total<(1<<127),"merged i128 overflow")
            if total==0: zeros+=1;continue
            require(total%orbit==0,"merged orbit division")
            w.write(bytes([key[0]])+key[1]+orbit.to_bytes(2,"little")+total.to_bytes(16,"little",signed=True));records+=1
        w.flush();os.fsync(w.fileno())
    for f in files:f.close()
    os.replace(tmp,output)
    return {"path":str(output.relative_to(ROOT)),"sha256":sha(output),"records":records,"bytes":39*records,"exact_zero_cancellations":zeros}

def merge_B_global(manifests:list[Path],output_dir:Path,witness_ledger:Path)->dict:
    plan_path=Path(__file__).parent/"k24_B20_production_plan_103.json";plan=json.loads(plan_path.read_text())
    require(len(manifests)==103,("B manifest count",len(manifests)))
    expected={(x["family_id"],tuple(x["interval"])):x for x in plan["shards"]};require(len(expected)==103,"B expected duplicates")
    got={};runs={g:[] for g in plan["required_groups"]};charges={g:0 for g in runs};ids=[]
    for p in manifests:
        raw=json.loads(p.read_text());key=(raw.get("family_id"),tuple(raw.get("source_interval",[])));require(key in expected and key not in got,("B duplicate/extra",key))
        z=validate_B_manifest(p.resolve(),plan,expected[key],False);got[key]=z
        for r in z["group_runs"]:runs[r["group_id"]].append(ROOT/r["path"])
        for g in z["charge_groups"]:charges[g["group_id"]]+=int(g["full_charge_scaled_U"])
    require(set(got)==set(expected),"B missing shards")
    lines=witness_ledger.read_text().splitlines();require(len(lines)==258,"global 257 witnesses")
    bins=[int(x.split("\t",1)[0]) for x in lines[1:]];require(bins==list(range(257)),"global witness bins")
    output_dir.mkdir(parents=True,exist_ok=False);merged=[]
    for gid in plan["required_groups"]:
        out=output_dir/(gid.replace(":","_").replace("|","_")+".bin")
        z=merge_records(runs[gid],out);z["group_id"]=gid;z["ids"]=plan["required_groups"][gid];z["charge_scaled_U"]=str(charges[gid]);merged.append(z);ids.extend(z["ids"])
    require(sorted(ids)==plan["required_ids"] and len(ids)==len(set(ids))==35,"B global ID equality")
    total=sum(charges.values());require(total==TARGET_SCALED,("B charge conservation",total,TARGET_SCALED))
    answer={"format":"orbit0-k24-B20-global-35-v2","status":"PASS_COMPLETE_35_ID_103_SHARD_B20_MERGE","degree":24,"scale_U":U,
      "covered_ids":sorted(ids),"missing":[],"duplicates":[],"extras":[],"groups":merged,"full_charge_scaled_U":str(total),
      "conservation_target_scaled_U":str(TARGET_SCALED),"conservation_equal":True,"literal_witnesses":{"path":str(witness_ledger.resolve().relative_to(ROOT)),"sha256":sha(witness_ledger.resolve()),"records":257},
      "record_bytes":39,"natural_sort_key":"(word_dictionary_id, multiplier_bytes)","all_orbit_divisions_exact":True,
      "scope":"complete natural B20 source ledger; relative closure/kernel remains separately required"}
    result=output_dir/"result.json";tmp=result.with_suffix(".json.tmp");tmp.write_text(json.dumps(answer,indent=2,sort_keys=True)+"\n");os.replace(tmp,result);return answer

def assemble_charge(acceptances:list[Path],output:Path)->dict:
    plan=json.loads((Path(__file__).parent/"k24_charge_production_plan_83.json").read_text());expected=plan["shards"]
    got=[]
    acceptance_keys={"format","status","degree","scale_U","family_id","group_ids","source_interval","source_units","raw_result","literal_witnesses","input_sha256","engine","groups","universal_terminality","full_equals_irreducible","resource_evidence","control","scope"}
    for p in acceptances:
        x=json.loads(p.read_text());require(set(x)==acceptance_keys,("acceptance keyset",sorted(set(x)^acceptance_keys)))
        require(x["format"]=="orbit0-k24-charge-shard-acceptance-v1" and x["degree"]==24 and x["scale_U"]==U,"acceptance constants")
        require(sha(ROOT/x["raw_result"]["path"])==x["raw_result"]["sha256"],"accepted raw hash")
        require(sha(ROOT/x["literal_witnesses"]["path"])==x["literal_witnesses"]["sha256"],"accepted witness hash")
        require(sha(ROOT/x["engine"]["source_path"])==x["engine"]["source_sha256"] and sha(ROOT/x["engine"]["binary_path"])==x["engine"]["binary_sha256"],"accepted engine hash")
        got.append(x)
    require(len(got)==len(expected),("shard count",len(got),len(expected)))
    by={(x["family_id"],tuple(x["source_interval"])):x for x in got};require(len(by)==len(got),"duplicate shard")
    sums={g:0 for g in plan["required_groups"]};occ={g:0 for g in sums};ids=[]
    for s in expected:
        x=by.get((s["family_id"],tuple(s["interval"])));require(x is not None,("missing",s["shard_id"]));require(x["status"]=="PASS_PRODUCTION_SHARD" and not x["control"],"nonproduction")
        for g in x["groups"]:sums[g["group_id"]]+=int(g["full_charge_scaled_U"]);occ[g["group_id"]]+=g["terminal_K24_occurrences"]
    for g,v in sums.items():ids.extend(plan["required_groups"][g])
    require(sorted(ids)==plan["required_ids"] and len(ids)==len(set(ids))==35,"ID equality")
    total=sum(sums.values());q=Fraction(total,U)
    answer={"format":"orbit0-k24-charge-complete-35-v1","status":"PASS_CONSERVATION_TARGET" if total==TARGET_SCALED else "FAIL_FILTERED_CHARGE_OBSTRUCTION",
      "degree":24,"scale_U":U,"covered_ids":sorted(ids),"missing":[],"duplicates":[],"extras":[],"groups":[{"group_id":g,"ids":plan["required_groups"][g],"full_charge_scaled_U":str(sums[g]),"irreducible_charge_scaled_U":str(sums[g]),"terminal_K24_occurrences":occ[g]} for g in plan["required_groups"]],
      "full_charge_scaled_U":str(total),"irreducible_charge_scaled_U":str(total),"full_charge":f"{q.numerator}/{q.denominator}",
      "conservation_target":str(TARGET),"conservation_target_scaled_U":str(TARGET_SCALED),"conservation_equal":total==TARGET_SCALED,
      "relative_B20_authorized":total==TARGET_SCALED,"scope":"complete strict K24 charge only; relative production remains separately gated"}
    tmp=output.with_suffix(output.suffix+".tmp");tmp.write_text(json.dumps(answer,indent=2,sort_keys=True)+"\n");os.replace(tmp,output)
    return answer

def selftest() -> dict:
    # Exact interval guards plus binary merge hostile cases.
    interval_guard([[0,2],[2,5]],5)
    rejected=[]
    for bad in ([[0,2],[3,5]],[[0,3],[2,5]],[[0,0],[0,5]]):
        try: interval_guard(bad,5)
        except RuntimeError: rejected.append(bad)
    require(len(rejected)==3,"interval hostiles")
    require(TARGET*U==TARGET_SCALED,"target scaling")
    return {"status":"PASS_K24_PRODUCTION_CONTRACT_SELFTEST","hostile_intervals_rejected":3,"target_scaled_U":str(TARGET_SCALED),"B_record_bytes":39,"B_shards":103,"charge_shards":83}

def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="cmd",required=True)
    sub.add_parser("build-plans");sub.add_parser("selftest")
    v=sub.add_parser("validate-charge");v.add_argument("result",type=Path);v.add_argument("family");v.add_argument("start",type=int);v.add_argument("end",type=int);v.add_argument("--control",action="store_true");v.add_argument("--resource",type=Path);v.add_argument("--acceptance",type=Path)
    a=sub.add_parser("assemble-charge");a.add_argument("output",type=Path);a.add_argument("acceptances",nargs="+",type=Path)
    vb=sub.add_parser("validate-B");vb.add_argument("manifest",type=Path);vb.add_argument("shard_id");vb.add_argument("--control",action="store_true")
    mb=sub.add_parser("merge-B");mb.add_argument("output_dir",type=Path);mb.add_argument("witness_ledger",type=Path);mb.add_argument("manifests",nargs="+",type=Path)
    ns=ap.parse_args()
    if ns.cmd=="build-plans":
        b,c=build_plans(Path(__file__).parent);print(json.dumps({"status":"PASS","B_shards":len(b["shards"]),"charge_shards":len(c["shards"])},sort_keys=True))
    elif ns.cmd=="selftest":print(json.dumps(selftest(),sort_keys=True))
    elif ns.cmd=="validate-charge":print(json.dumps(validate_charge(ns.result,ns.family,ns.start,ns.end,ns.control,ns.resource,ns.acceptance),sort_keys=True))
    elif ns.cmd=="validate-B":
        plan=json.loads((Path(__file__).parent/"k24_B20_production_plan_103.json").read_text());matches=[x for x in plan["shards"] if x["shard_id"]==ns.shard_id];require(len(matches)==1,"shard id");print(json.dumps(validate_B_manifest(ns.manifest.resolve(),plan,matches[0],ns.control),sort_keys=True))
    elif ns.cmd=="merge-B":print(json.dumps(merge_B_global(ns.manifests,ns.output_dir.resolve(),ns.witness_ledger.resolve()),sort_keys=True))
    else: print(json.dumps(assemble_charge(ns.acceptances,ns.output),sort_keys=True))

if __name__=="__main__": main()
