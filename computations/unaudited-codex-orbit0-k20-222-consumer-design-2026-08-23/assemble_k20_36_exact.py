#!/usr/bin/env python3
"""Exact-Q K20 assembler with a strict 36-ID gate.

Default mode refuses to emit a total unless the manifest covers every DAG ID
exactly once.  `--audit-incomplete` emits a diagnostic partial and still makes
an explicit `complete_K20_claim: false` statement.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[2]
DAGP = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

def q(x):
    if isinstance(x, int): return Fraction(x)
    if isinstance(x, str): return Fraction(x)
    if isinstance(x, dict): return Fraction(int(x["numerator"]), int(x["denominator"]))
    raise TypeError(x)

def fq(x): return {"numerator": x.numerator, "denominator": x.denominator, "text": str(x)}

def entry_ids(entry):
    """Return the DAG IDs covered by one scalar entry.

    A grouped entry is one exact aggregate scalar over a disjoint set of IDs;
    its scalar must therefore be summed once, while every ID participates in
    the coverage/duplicate gate.
    """
    has_id = "id" in entry
    has_ids = "ids" in entry
    if has_id == has_ids:
        raise ValueError("each scalar entry must have exactly one of id/ids")
    ids = [entry["id"]] if has_id else entry["ids"]
    if not isinstance(ids, list) or not ids or not all(isinstance(x, str) for x in ids):
        raise ValueError("ids must be a nonempty string list")
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate ID inside grouped entry: {ids}")
    return ids

def assemble(manifest, permit_incomplete=False):
    dag = json.loads(DAGP.read_text())
    required = dag["required_reachable_lineage_ids_by_degree"]["20"]
    assert len(required) == len(set(required)) == 36
    entries = manifest.get("paths", [])
    ids = [lineage for entry in entries for lineage in entry_ids(entry)]
    dup = sorted(k for k,v in Counter(ids).items() if v != 1)
    extra = sorted(set(ids) - set(required))
    missing = [x for x in required if x not in set(ids)]
    for x in entries:
        if not HEX64.fullmatch(x.get("evidence_sha256", "")):
            raise ValueError(f"bad evidence digest for {entry_ids(x)}")
    if dup or extra:
        raise ValueError(f"duplicate={dup} extra={extra}")
    full = sum((q(x["full"]) for x in entries), Fraction())
    irr = sum((q(x["irreducible"]) for x in entries), Fraction())
    if missing and not permit_incomplete:
        raise ValueError(f"missing {len(missing)} K20 IDs: {missing}")
    return {
        "status": "PASS_COMPLETE_K20_36_ID_EXACT_Q" if not missing else "REJECT_INCOMPLETE_K20_36_ID_GATE",
        "complete_K20_claim": not missing,
        "required_paths": 36,
        "covered_paths": len(ids),
        "scalar_entries": len(entries),
        "missing_paths": missing,
        "duplicate_paths": dup,
        "extra_paths": extra,
        "full": fq(full),
        "irreducible": fq(irr),
        "covered_ids": ids,
        "dag_logical_sha256": dag["logical_sha256"],
        "manifest_sha256": hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",",":")).encode()).hexdigest(),
    }

def self_test():
    ids = json.loads(DAGP.read_text())["required_reachable_lineage_ids_by_degree"]["20"]
    z = "0"*64
    good = {"paths":[{"id":x,"full":"0","irreducible":"0","evidence_sha256":z} for x in ids]}
    assert assemble(good)["complete_K20_claim"]
    grouped = {"paths":[
        {"ids":ids[:3],"full":"7","irreducible":"11","evidence_sha256":z},
        *[{"id":x,"full":"0","irreducible":"0","evidence_sha256":z} for x in ids[3:]],
    ]}
    gr = assemble(grouped)
    assert gr["complete_K20_claim"] and gr["covered_paths"] == 36
    assert gr["scalar_entries"] == 34 and gr["full"]["text"] == "7"
    try: assemble({"paths":good["paths"][:-1]})
    except ValueError as e: assert "missing 1" in str(e)
    else: raise AssertionError("missing-ID mutation accepted")
    try: assemble({"paths":good["paths"]+[good["paths"][0]]})
    except ValueError as e: assert "duplicate" in str(e)
    else: raise AssertionError("duplicate-ID mutation accepted")
    print(json.dumps({"status":"PASS_36_ID_ASSEMBLER_SELF_TEST","grouped_scalar_counted_once":True,"missing_rejected":True,"duplicate_rejected":True}))

if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test(); raise SystemExit
    permit = False
    args = sys.argv[1:]
    if args and args[0] == "--audit-incomplete": permit=True; args=args[1:]
    if len(args) != 2: raise SystemExit("usage: assemble_k20_36_exact.py [--audit-incomplete] MANIFEST.json OUTPUT.json")
    manifest = json.loads(Path(args[0]).read_text())
    try:
        result = assemble(manifest, permit)
    except ValueError as e:
        print(f"REJECT: {e}", file=sys.stderr)
        raise SystemExit(2)
    out = Path(args[1]); tmp=Path(str(out)+".tmp")
    tmp.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n"); tmp.replace(out)
    print(json.dumps({k:result[k] for k in ("status","covered_paths","missing_paths","full","irreducible")}, indent=2))
