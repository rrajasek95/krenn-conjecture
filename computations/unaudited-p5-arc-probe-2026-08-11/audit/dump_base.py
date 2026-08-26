#!/usr/bin/env python3
"""Audit-side loader: run the committed F2 chain once and freeze the source
data (with its own frozen ledger checks) into a pickle for reuse.

This calls the committed modules only; nothing here re-derives equations.
"""
import importlib.util
import pickle
import sys
import time
from pathlib import Path

COMP = Path("/Users/rishi/workplace/krenn-conjecture/computations")
OUT = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, COMP / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    t0 = time.time()
    F2 = load_module("audit_f2", "verify_n8_p5_schur_generic_L_f2_center.py")
    base = F2.audit(return_data=True)
    print(f"[{time.time()-t0:.1f}s] F2.audit ok (frozen ledger checks passed)")
    SCHUR = F2.F1.CENTER.SCHUR
    schur = SCHUR.audit(return_data=True)
    print(f"[{time.time()-t0:.1f}s] SCHUR.audit ok")
    layout = base["layout"]
    payload = {
        "layout_a": dict(layout["a"]),
        "layout_y": dict(layout["y"]),
        "layout_n": dict(layout["n"]),
        "variable_count": layout["variable_count"],
        "tau": base["tau"],
        "normal": base["normal"],
        "transverse": base["transverse"],
        "obstruction": base["obstruction"],
        "pure": schur["pure_stricts"],
        "pivots": list(base["pivots"]),
        "local_variables": set(base["local_variables"]),
        "first_bend": base["first_bend"],
        "second_bend": base["second_bend"],
        "first_relation": base["first_relation"],
        "second_relation": base["second_relation"],
        "P5_NORMAL_VARIABLES": list(F2.F1.CENTER.P5.P5_NORMAL_VARIABLES),
    }
    with (OUT / "base.pkl").open("wb") as handle:
        pickle.dump(payload, handle)
    print("rows:", len(payload["normal"]), len(payload["transverse"]),
          len(payload["obstruction"]), len(payload["pure"]))
    print("term counts obstruction:",
          [len(r) for r in payload["obstruction"]][:8], "...")
    print("term counts normal max:", max(len(r) for r in payload["normal"]))
    print("term counts transverse:", [len(r) for r in payload["transverse"]])
    print("pure terms:", [len(r) for r in payload["pure"]])
    print("first_bend", payload["first_bend"], "second_bend",
          payload["second_bend"], "tau", payload["tau"])
    print(f"[{time.time()-t0:.1f}s] done")


if __name__ == "__main__":
    main()
