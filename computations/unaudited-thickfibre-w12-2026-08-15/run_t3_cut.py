#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- TASK 2/3: the CUT EXTRACTION kill over all targets."""
from __future__ import annotations
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w12_core as C            # noqa: E402
import w12_cutdecide as CD      # noqa: E402
import w12_targets as TG        # noqa: E402
from run_t4_calibration import load_immunity, load_survivor  # noqa: E402


def run(geo, name, template, timeout=600, want_all=False):
    t = time.time()
    a = C.audit(geo, template)
    v, recs = CD.cut_kill(geo, template, timeout=timeout, want_all=want_all)
    k = [r for r in recs if r["verdict"] == "killed"]
    cert = k[0] if k else None
    print(f"{name:22s} m={a['m']:2d} S={a['sigma']:3d} minfib={a['min_mixed_fibre']:2d}"
          f" -> {v:8s} cuts={len(recs):3d} ({round(time.time()-t,1)}s)"
          + (f"  L={cert['cut_L']} side={cert['side']} :: {cert['reason']}"
             if cert else ""), flush=True)
    return {"name": name, "audit": a, "verdict": v, "certificate": cert,
            "records": recs if want_all else recs[-3:],
            "seconds": round(time.time() - t, 2)}


def main():
    geo = C.geometry()
    which = sys.argv[1] if len(sys.argv) > 1 else "core"
    out = []
    if which in ("core", "all"):
        out.append(run(geo, "survivor_m20", load_survivor()))
        for m, tmpl, _ in load_immunity():
            out.append(run(geo, f"immunity_m{m}", tmpl))
    if which in ("w11", "all"):
        for name, tmpl in TG.load_w11_witnesses():
            out.append(run(geo, name, tmpl))
    if which in ("m17", "all"):
        for name, tmpl, w8v in TG.load_w8_m17_classes():
            out.append(run(geo, name, tmpl))
    stem = "results_t3_cut_" + which
    with open(os.path.join(HERE, stem + ".json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote", stem + ".json")


if __name__ == "__main__":
    main()
