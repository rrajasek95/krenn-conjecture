#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- band decision with the constant-witness case split.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

Same CEGAR as w8_close.py, but split over the 31 orbits of ordered triples of
perfect matchings under S_8 x S_3 (w8_triples.py).  Every admissible template
supports a perfect matching in each diagonal graph G_c, so after relabelling
its witness triple is one of the 31 representatives; forcing that triple's 12
diagonal cells is therefore a sound and COMPLETE case split, and it removes
almost all of the symmetry that makes the unsplit search slow.

mode 'nosingleton' : is there an admissible zero-singleton template?
mode 'closure'     : is there an admissible template that also survives the
                     exact value-level closure engine?

UNSAT in every orbit  =>  the answer is no at that support, i.e. the band
point is closed (by O2 alone, resp. by O2 + closure), with certificates.

Run: python3 w8_band.py --m 15 --mode nosingleton --seconds 240
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter

import numpy as np

import w8_core as C
import w8_cert as K
from w8_sat import Encoding, near_constant_words
from w8_triples import orbits


def solve_orbit(geo, m, triple, mode, seconds, seed_radius, solver_name,
                style="counter", verbose=False, diagonal=False):
    enc = Encoding(geo, m, solver_name, style)
    if diagonal:
        for e in range(len(geo.edges)):
            for k in range(9):
                if k % 4:
                    enc.add([-enc.cell[e][k]])
    for colour, matching in enumerate(triple):
        for u, v in geo.matchings[matching]:
            enc.add([enc.cell_lit(geo.index[(u, v)], colour, colour)])
    for w in near_constant_words(geo, seed_radius):
        enc.word_constraint(w)
    start = time.time()
    verdicts = Counter()
    rounds = 0
    survivors = []
    status = "timeout"
    while time.time() - start < seconds:
        if enc.solver.solve() is False:
            status = "UNSAT"
            break
        rounds += 1
        template = enc.decode(enc.solver.get_model())
        compat = C.compat_matrix(geo, template)
        sizes = compat.sum(axis=0, dtype=np.int64)
        bad = np.nonzero((sizes == 1) & geo.mixed)[0]
        if len(bad):
            verdicts["O2-literal-singleton"] += 1
            for w in sorted(int(x) for x in bad)[:32]:
                enc.word_constraint(w)
            continue
        if mode == "nosingleton":
            survivors.append(list(template))
            status = "SAT"
            break
        cert = K.certify(geo, template, compat=compat)
        verdicts[cert["verdict"]] += 1
        if cert["verdict"] == "survivor":
            survivors.append(list(template))
            status = "SURVIVOR"
            break
        ok, notes = K.verify(geo, template, cert)
        if not ok:
            status = "certificate-failure"
            survivors.append(list(template))
            break
        enc.fibre_nogood(K.certificate_words(cert))
        if verbose and rounds % 50 == 0:
            print(f"    round {rounds}: {dict(verdicts)} "
                  f"[{time.time() - start:.0f}s]", flush=True)
    enc.solver.delete()
    return {"status": status, "rounds": rounds, "verdicts": dict(verdicts),
            "seconds": round(time.time() - start, 1),
            "survivors": survivors}


def solve_orbit_recording(geo, m, triple, mode, seconds, seed_radius=2,
                          solver_name="cadical153", style="counter"):
    """Same CEGAR, returning the full accumulated clause list for DRUP."""
    enc = Encoding(geo, m, solver_name, style)
    for colour, matching in enumerate(triple):
        for u, v in geo.matchings[matching]:
            enc.add([enc.cell_lit(geo.index[(u, v)], colour, colour)])
    for w in near_constant_words(geo, seed_radius):
        enc.word_constraint(w)
    start = time.time()
    verdicts = Counter()
    rounds = 0
    status = "timeout"
    while time.time() - start < seconds:
        if enc.solver.solve() is False:
            status = "UNSAT"
            break
        rounds += 1
        template = enc.decode(enc.solver.get_model())
        compat = C.compat_matrix(geo, template)
        sizes = compat.sum(axis=0, dtype=np.int64)
        bad = np.nonzero((sizes == 1) & geo.mixed)[0]
        if len(bad):
            verdicts["O2-literal-singleton"] += 1
            for w in sorted(int(x) for x in bad)[:32]:
                enc.word_constraint(w)
            continue
        if mode == "nosingleton":
            status = "SAT"
            break
        cert = K.certify(geo, template, compat=compat)
        verdicts[cert["verdict"]] += 1
        if cert["verdict"] == "survivor":
            status = "SURVIVOR"
            break
        ok, _ = K.verify(geo, template, cert)
        if not ok:
            status = "certificate-failure"
            break
        enc.fibre_nogood(K.certificate_words(cert))
    clauses = enc.all_clauses()
    top = enc.pool.top
    enc.solver.delete()
    return ({"status": status, "rounds": rounds, "verdicts": dict(verdicts),
             "seconds": round(time.time() - start, 1)}, clauses, top)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=15)
    parser.add_argument("--mode", default="closure",
                        choices=("nosingleton", "closure"))
    parser.add_argument("--seconds", type=float, default=300.0,
                        help="per-orbit budget")
    parser.add_argument("--seed-radius", type=int, default=2)
    parser.add_argument("--solver", default="cadical153")
    parser.add_argument("--only", type=int, default=None)
    parser.add_argument("--style", default="counter")
    parser.add_argument("--diagonal", action="store_true")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    geo = C.geometry(8)
    reps = sorted(orbits(geo))
    canonical = geo.matchings.index(tuple((2 * k, 2 * k + 1) for k in range(4)))
    triples = [(canonical, a, b) for (a, b) in reps]
    print(f"UNAUDITED PROBE (W8) -- band m<={args.m}, mode {args.mode}, "
          f"{len(triples)} constant-witness orbits", flush=True)
    rows = []
    tally = Counter()
    for number, triple in enumerate(triples):
        if args.only is not None and number != args.only:
            continue
        row = solve_orbit(geo, args.m, triple, args.mode, args.seconds,
                          args.seed_radius, args.solver, args.style,
                          verbose=True, diagonal=args.diagonal)
        row["orbit"] = number
        row["triple"] = [list(geo.matchings[t]) for t in triple]
        rows.append(row)
        tally[row["status"]] += 1
        print(f"  orbit {number:2d}: {row['status']:<20} rounds "
              f"{row['rounds']:5d}  {row['seconds']:7.1f}s  {row['verdicts']}",
              flush=True)
    print("\nstatus tally:", dict(tally))
    closed = all(r["status"] == "UNSAT" for r in rows)
    print("BAND POINT CLOSED" if closed else "NOT CLOSED (see rows)")
    name = args.out or f"results_band_m{args.m}_{args.mode}.json"
    json.dump({"m": args.m, "mode": args.mode, "orbits": len(rows),
               "tally": dict(tally), "closed": closed, "rows": rows},
              open(name, "w"), indent=1)
    print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
