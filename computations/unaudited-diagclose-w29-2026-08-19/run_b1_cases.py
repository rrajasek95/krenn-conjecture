#!/usr/bin/env python3
"""W29 B1 -- decide the T1i free-set-triple cases with Singular.

argv: <lo> <hi> [char_screen] [timeout] [tag]
Cases are the 87 orbit representatives of (R_0,R_1,R_2) (see w29_t1i), sorted
by |R_0|+|R_1|+|R_2| so the singleton case (the main one) runs first.

Per case: escalate over generator subsets (sparsest first) in the screening
characteristic; the FIRST subset that returns the unit ideal is then re-decided
in char 0 and at TWO 1-mod-3 primes (ledger 19).  Every step is checkpointed.
"""
from __future__ import annotations

import json
import sys
import time

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
W28 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-x4empty-w28-2026-08-18")
for p in (BASE, W28):
    if p not in sys.path:
        sys.path.insert(0, p)
import w29_t1i as T                                                 # noqa: E402

PRIMES_1MOD3 = (32029, 1000003)
RES, RAN = {}, []
OUT = None


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def sorted_cases():
    reps = T.case_orbit_reps()
    reps.sort(key=lambda r: (sum(len(x) for x in r[0]),
                             tuple(len(x) for x in r[0]), r[0]))
    return reps


def run_case(Rs, orbsz, screen, tmo, kmax=4):
    t0 = time.time()
    case = T.Case(Rs, kmax=kmax)
    gens = case.build()
    polys = [g for _, g in gens]
    polys.sort(key=lambda p: (len(p.t), p.deg()))
    polys, names = T.compress(polys, case.names)
    rec = {"R": [list(r) for r in Rs], "orbit_size": orbsz, "kmax": kmax,
           "nv": len(names), "n_gens": len(polys),
           "steps": []}
    print(f"--- R={Rs} (orbit {orbsz}): {len(polys)} gens, {len(names)} vars",
          flush=True)
    budget = [b for b in (48, 96, 192, 384, len(polys)) if b <= len(polys)]
    if budget[-1] != len(polys):
        budget.append(len(polys))
    hit = None
    for b in budget:
        t1 = time.time()
        try:
            r = T.decide(polys[:b], names, screen, "std", timeout=tmo)
        except Exception as exc:
            r = {"error": str(exc)[:200], "char": screen}
        r["ngens_used"] = b
        r["secs"] = round(time.time() - t1, 1)
        rec["steps"].append(r)
        print(f"    [char {screen}] {b} gens -> {r.get('isunit')} "
              f"dim {r.get('dim')} ({r['secs']}s) {r.get('error','')}",
              flush=True)
        ck(f"{Rs}_b{b}")
        if r.get("isunit") == "1":
            hit = b
            break
        if "error" in r:
            break
    rec["screen_unit_at"] = hit
    if hit is not None:
        conf = {}
        for ch in (0,) + PRIMES_1MOD3:
            t1 = time.time()
            try:
                r = T.decide(polys[:hit], names, ch, "std", timeout=tmo)
            except Exception as exc:
                r = {"error": str(exc)[:200]}
            r["secs"] = round(time.time() - t1, 1)
            conf[str(ch)] = r
            print(f"    [confirm char {ch}] {r.get('isunit')} "
                  f"({r['secs']}s) {r.get('error','')}", flush=True)
            ck(f"{Rs}_confirm{ch}")
        rec["confirm"] = conf
        rec["VERDICT"] = ("UNIT (char 0 + two 1-mod-3 primes)"
                          if conf["0"].get("isunit") == "1" and
                          all(conf[str(p)].get("isunit") == "1"
                              for p in PRIMES_1MOD3)
                          else "unit in the screen only -- NOT confirmed")
    else:
        rec["VERDICT"] = "UNDECIDED"
    rec["secs"] = round(time.time() - t0, 1)
    print(f"    >>> {Rs}: {rec['VERDICT']} ({rec['secs']}s)", flush=True)
    return rec


def main():
    global OUT
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    screen = int(sys.argv[3]) if len(sys.argv) > 3 else 32003
    tmo = int(sys.argv[4]) if len(sys.argv) > 4 else 1200
    tag = sys.argv[5] if len(sys.argv) > 5 else f"{lo}_{hi}"
    kmax = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    OUT = f"{BASE}/results_b1_cases_{tag}_k{kmax}.json"
    reps = sorted_cases()
    RES["setup"] = {"lo": lo, "hi": hi, "screen": screen, "timeout": tmo,
                    "n_orbits": len(reps), "kmax": kmax}
    ck("setup")
    t0 = time.time()
    for i in range(lo, min(hi, len(reps))):
        Rs, sz = reps[i]
        rec = run_case(Rs, sz, screen, tmo, kmax)
        RES.setdefault("cases", {})[str(i)] = rec
        RAN.append(f"case{i}")
        ck(f"case{i}")
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
