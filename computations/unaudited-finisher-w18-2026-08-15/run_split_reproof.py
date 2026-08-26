#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- cube-and-conquer re-derivation of one class.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

Purpose: give a class a SECOND, checker-independent UNSAT derivation when its
monolithic proof will not replay.  A complete case split on cell literals is
sound (every template satisfies each branch's assumption or its negation), and
each branch's proof is small enough to be replayed by this lane's own checkers.

    run(mask, m, depth) :  branch on the `depth` cell variables that the base
    encoding sees first, run the ordinary CEGAR on each of the 2^depth cubes
    with the cube added as unit clauses, and emit + replay a proof per cube.
    Every cube UNSAT  =>  the class is UNSAT.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C          # noqa: E402
import w18_sweep as SW        # noqa: E402


def run(mask, m, depth=3, seconds=1800, outdir=None, cells=None):
    enc0 = SW.S.ClassEncoder(mask)
    if cells is None:
        # branch on the first `depth` cells of the lowest-index edges
        cells = [(e, k) for e in enc0.edges for k in range(9)][:depth]
    rows = []
    t0 = time.time()
    for bits in product((True, False), repeat=len(cells)):
        cube = [(e, k, b) for (e, k), b in zip(cells, bits)]
        row = SW.run_class(mask, m, seconds=seconds, outdir=outdir,
                           store_certs=False, sing_batch=24, exact_after=1,
                           sing_orbit_cap=1, orbit_cap=48,
                           extra_units=cube)
        row["cube"] = [[e, k, bool(b)] for (e, k, b) in cube]
        rows.append(row)
        pr = row.get("proof", {})
        print(f"[{time.time()-t0:7.1f}s] cube {bits} {row['status']:<12s} "
              f"rounds={row['rounds']:6d} lemmas={pr.get('proof_lemmas')} "
              f"replay_rc={pr.get('rup18_rc')} {row['seconds']:8.1f}s",
              flush=True)
    ok = all(r["status"] in ("UNSAT", "TRIVIAL-UNSAT") for r in rows)
    allreplay = all(r.get("proof", {}).get("rup18_rc") == 0
                    for r in rows if "proof" in r)
    out = {"mask": mask, "m": m, "cells": [list(c) for c in cells],
           "cubes": len(rows), "all_unsat": ok, "all_proofs_replayed": allreplay,
           "rows": rows}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mask", type=int, required=True)
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--seconds", type=float, default=1800.0)
    a = ap.parse_args()
    outdir = os.path.join(HERE, "certificates", "split_m%d_g%d" % (a.m, a.mask))
    res = run(a.mask, a.m, a.depth, a.seconds, outdir)
    name = os.path.join(HERE, "results_split_m%d_g%d.json" % (a.m, a.mask))
    json.dump(res, open(name, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
    print("wrote", name)
    return 0 if res["all_unsat"] and res["all_proofs_replayed"] else 1


if __name__ == "__main__":
    sys.exit(main())
