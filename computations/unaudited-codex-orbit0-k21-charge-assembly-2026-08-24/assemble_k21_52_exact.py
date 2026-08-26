#!/usr/bin/env python3
"""Strict exact-Q K21 charge assembler with grouped-scalar support."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[2]
DAGP = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
def q(x):
    if isinstance(x,int): return Fraction(x)
    if isinstance(x,str): return Fraction(x)
    if isinstance(x,dict): return Fraction(int(x["numerator"]),int(x["denominator"]))
    raise TypeError(x)
def fq(x): return {"numerator":x.numerator,"denominator":x.denominator,"text":str(x)}
def ids(entry):
    if ("id" in entry)==("ids" in entry): raise ValueError("exactly one of id/ids is required")
    out=[entry["id"]] if "id" in entry else entry["ids"]
    if not isinstance(out,list) or not out or not all(isinstance(x,str) for x in out) or len(out)!=len(set(out)): raise ValueError(f"bad IDs {out}")
    return out
def assemble(manifest,allow_partial=False):
    dag=json.loads(DAGP.read_text()); required=dag["required_reachable_lineage_ids_by_degree"]["21"]
    assert len(required)==len(set(required))==52
    entries=manifest.get("groups",[]); flat=[x for e in entries for x in ids(e)]
    duplicate=sorted(k for k,v in Counter(flat).items() if v!=1); extra=sorted(set(flat)-set(required)); missing=[x for x in required if x not in set(flat)]
    for e in entries:
        if not HEX64.fullmatch(e.get("evidence_sha256","")): raise ValueError(f"bad digest {ids(e)}")
    if duplicate or extra: raise ValueError(f"duplicate={duplicate} extra={extra}")
    if missing and not allow_partial: raise ValueError(f"missing {len(missing)} K21 IDs: {missing}")
    full=sum((q(e["full"]) for e in entries),Fraction()); irr=sum((q(e["irreducible"]) for e in entries),Fraction())
    return {
      "status":"PASS_COMPLETE_K21_52_ID_EXACT_Q" if not missing else "REJECT_INCOMPLETE_K21_52_ID_GATE",
      "complete_K21_claim":not missing,"required_paths":52,"covered_paths":len(flat),"scalar_groups":len(entries),
      "missing_paths":missing,"duplicate_paths":duplicate,"extra_paths":extra,"full":fq(full),"irreducible":fq(irr),"covered_ids":flat,
      "dag_logical_sha256":dag["logical_sha256"],"manifest_sha256":hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
    }
def selftest():
    required=json.loads(DAGP.read_text())["required_reachable_lineage_ids_by_degree"]["21"]; z="0"*64
    good={"groups":[{"ids":required[:4],"full":"7/3","irreducible":"11/5","evidence_sha256":z},*({"id":x,"full":"0","irreducible":"0","evidence_sha256":z} for x in required[4:])]}
    r=assemble(good);assert r["complete_K21_claim"] and r["covered_paths"]==52 and r["full"]["text"]=="7/3"
    try: assemble({"groups":good["groups"][:-1]})
    except ValueError as e: assert "missing 1" in str(e)
    else: raise AssertionError("missing mutation accepted")
    try: assemble({"groups":good["groups"]+[good["groups"][-1]]})
    except ValueError as e: assert "duplicate" in str(e)
    else: raise AssertionError("duplicate mutation accepted")
    print(json.dumps({"status":"PASS_K21_52_ID_ASSEMBLER_SELFTEST","group_scalar_once":True,"missing_rejected":True,"duplicate_rejected":True}))
if __name__=="__main__":
    if sys.argv[1:]==["--self-test"]: selftest();raise SystemExit
    args=sys.argv[1:];partial=False
    if args and args[0]=="--audit-incomplete":partial=True;args=args[1:]
    if len(args)!=2:raise SystemExit("usage: assemble_k21_52_exact.py [--audit-incomplete] manifest.json output.json")
    try:r=assemble(json.loads(Path(args[0]).read_text()),partial)
    except ValueError as e:print(f"REJECT: {e}",file=sys.stderr);raise SystemExit(2)
    out=Path(args[1]);tmp=Path(str(out)+".tmp");tmp.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n");tmp.replace(out)
    print(json.dumps({k:r[k] for k in ("status","covered_paths","missing_paths","full","irreducible")},indent=2))
