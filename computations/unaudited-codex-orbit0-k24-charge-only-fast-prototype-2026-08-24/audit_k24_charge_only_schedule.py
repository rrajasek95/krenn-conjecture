#!/usr/bin/env python3
"""Independent fail-closed audit of the exact K24 charge-only schedule."""
import copy, hashlib, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SCHEDULE=HERE/"results_k24_charge_only_fast_schedule.json"
AVAIL=ROOT/"computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/results_k24_availability_schedule.json"
U=400_591_699_200

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def frozen_groups(av):
    out={}
    for x in av["lineages"]:
        out.setdefault(x["group_id"],[]).append(x["id"])
    return out

def no_gap(intervals, total):
    assert intervals and intervals[0][0]==0 and intervals[-1][1]==total
    assert all(a < b for a,b in intervals)
    assert all(intervals[i][1]==intervals[i+1][0] for i in range(len(intervals)-1))

def gate_validate(f, expected):
    names=f.get("gate_results",[f.get("gate_result")])
    hashes=f["gate_sha256"] if isinstance(f["gate_sha256"],list) else [f["gate_sha256"]]
    assert len(names)==len(hashes)
    seen=[]
    for name,h in zip(names,hashes):
        p=HERE/name; assert sha(p)==h
        x=json.loads(p.read_text()); assert x["degree"]==24 and int(x["scale_U"])==U
        if "groups" in x:
            for g in x["groups"]:
                seen += g["ids"]
                assert g["full_occurrences"]==g["irreducible_occurrences"]==g["K24_terminal_occurrences"]
                assert int(g["full_charge_scaled_U"])==int(g["irreducible_charge_scaled_U"])
        elif "sinks" in x:
            for key,s in x["sinks"].items():
                if "ids" in s: seen += s["ids"]
                elif key.startswith("D14:"): seen.append(key)
                assert s["full_occurrences"]==s["irreducible_occurrences"]
                assert int(s["full_charge_scaled_U"])==int(s["irreducible_charge_scaled_U"])
        elif "ids" in x:
            seen += x["ids"]
            assert x["full_occurrences"]==x["irreducible_occurrences"]
            assert int(x["full_charge_scaled_U"])==int(x["irreducible_charge_scaled_U"])
        elif "covered_lineage_ids" in x:
            seen += x["covered_lineage_ids"]
            s=x.get("sink")
            if s:
                assert s["full_occurrences"]==s["irreducible_occurrences"]==s["terminal_K24_occurrences"]
                assert int(s["full_charge_scaled_U"])==int(s["irreducible_charge_scaled_U"])
        elif "strict_id" in x:
            seen.append(x["strict_id"])
            assert x["full_occurrences"]==x["irreducible_occurrences"]==x["terminal_K4_tails"]
            assert int(x["full_charge_scaled_U"])==int(x["irreducible_charge_scaled_U"])
    assert sorted(seen)==sorted(expected)

def validate(d,av,check_hashes=True):
    assert d["degree"]==24 and int(d["scale_U"])==U
    assert d["required_ids"]==35 and d["scalar_groups"]==10 and d["physical_families"]==6
    expected=frozen_groups(av)
    got={x["group_id"]:x["ids"] for x in d["groups"]}
    assert got==expected and len(got)==10
    flat=[x for ids in got.values() for x in ids]
    assert len(flat)==len(set(flat))==35
    fam_groups=[g for f in d["families"] for g in f["group_ids"]]
    assert len(fam_groups)==len(set(fam_groups))==10 and set(fam_groups)==set(got)
    totals={"direct_D17_D18_formula":485,"k14_source_formula":485,
            "grouped_direct_k15_source":485,"grouped_direct_k16_rows":24097095,
            "hidden_collected_k18":158439965,"hidden_decorated_k16_pair":101545723}
    for f in d["families"]:
        no_gap(f["planned_intervals"],totals[f["family_id"]])
        assert f["workers"] in range(1,9) and f["wall_seconds"]==600
        if "projected_max_shard_seconds" in f: assert f["projected_max_shard_seconds"] < 540
        if "projected_max_shard_seconds_each" in f: assert max(f["projected_max_shard_seconds_each"]) < 540
        gate_validate(f,[x for g in f["group_ids"] for x in expected[g]])
    assert d["terminality"]["all_35_terminal"] and d["terminality"]["k24_child_anchor_mass"]==0
    assert d["charge_only_compression"]["column_or_row_output_required"] is False
    assert "never multiplied" in d["existing_strict_assembler"]["group_scalar_semantics"]
    assert d["exact_coverage_contract"]["missing_ids"]==[] and d["exact_coverage_contract"]["extra_ids"]==[]
    if check_hashes:
        assert sha(AVAIL)==d["authoritative_availability"]["sha256"]
        assert sha(ROOT/d["existing_strict_assembler"]["path"])==d["existing_strict_assembler"]["sha256"]
        for f in d["families"]:
            engines=f.get("engines",[f.get("engine")])
            ss=f["source_sha256"] if isinstance(f["source_sha256"],list) else [f["source_sha256"]]
            bs=f["binary_sha256"] if isinstance(f["binary_sha256"],list) else [f["binary_sha256"]]
            assert len(engines)==len(ss)==len(bs)
            for name,h1,h2 in zip(engines,ss,bs):
                assert sha(HERE/(name+".rs"))==h1 and sha(HERE/name)==h2
            for name,h in f.get("supporting_sources",{}).items():
                assert sha(HERE/name)==h
    return {"groups":10,"ids":35,"families":6}

def hostile(d,av):
    accepted=[]
    def reject(name,mut):
        x=copy.deepcopy(d); mut(x)
        try: validate(x,av,False)
        except (AssertionError,KeyError,TypeError,ValueError): accepted.append(name); return
        raise AssertionError("hostile schedule accepted: "+name)
    reject("missing_group",lambda x:x["groups"].pop())
    reject("duplicate_lineage",lambda x:x["groups"][0]["ids"].__setitem__(0,x["groups"][1]["ids"][0]))
    reject("wrong_group",lambda x:x["groups"][0].__setitem__("group_id","source_D18_R2_4"))
    reject("interval_gap",lambda x:x["families"][2]["planned_intervals"][1].__setitem__(0,31))
    reject("interval_overlap",lambda x:x["families"][4]["planned_intervals"][1].__setitem__(0,52813320))
    reject("unsafe_shard",lambda x:x["families"][2].__setitem__("projected_max_shard_seconds",541))
    reject("row_required",lambda x:x["charge_only_compression"].__setitem__("column_or_row_output_required",True))
    reject("bad_U",lambda x:x.__setitem__("scale_U","1"))
    reject("multiply_group_scalar",lambda x:x["existing_strict_assembler"].__setitem__("group_scalar_semantics","multiply by ID count"))
    return accepted

def main():
    d=json.loads(SCHEDULE.read_text()); av=json.loads(AVAIL.read_text())
    summary=validate(d,av); tests=hostile(d,av)
    out={"status":"PASS_INDEPENDENT_EXACT_K24_CHARGE_ONLY_35_ID_SCHEDULE_AUDIT",
         "schedule_sha256":sha(SCHEDULE),"availability_sha256":sha(AVAIL),
         "summary":summary,"hostile_rejections":tests,
         "production_charge_complete":False}
    p=HERE/"results_k24_charge_only_fast_schedule_audit.json"
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
