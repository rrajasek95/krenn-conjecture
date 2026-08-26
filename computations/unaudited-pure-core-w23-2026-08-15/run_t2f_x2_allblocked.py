#!/usr/bin/env python3
"""W23 T2f -- ESCALATION CHECK: are there ALL-BLOCKED points of X_2 among
GENERAL (non-diagonal) N = 6 sources?

The exhaustive T2b result says NO on the all-1 DIAGONAL stratum.  The T2c walk
reported 2/6 walked X_2 objects as all-blocked.  This runner re-derives such
objects from scratch and subjects each to the full control battery:

  (1) membership in X_2 re-verified against the RAW word definition (all 219
      2-near-constant words), not against the solver that produced it;
  (2) pures re-computed;
  (3) liveness of every pair re-computed;
  (4) every live pair re-decided by BOTH deciders (W23 and W22), over Q and
      modulo 32003 and 1000003;
  (5) the block ranks and the detachment profile recorded;
  (6) an explicit-point control: the same battery applied to a KNOWN-witness
      object (the near-exact source) to show the battery can report WITNESS.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-induction2-w22-2026-08-15")
import w23_core as C                                          # noqa: E402
import w23_walk as WK                                         # noqa: E402
import w23_decide as DEC                                      # noqa: E402
import w22_n6 as N6                                           # noqa: E402

N = 6
PAIRS = list(combinations(range(N), 2))
RES = {}


def full_battery(src, tag):
    words2 = WK.near_constant_words(N, 3, 2)
    ok2, badw = WK.in_Xk(src, N, words2)
    pu = C.pures(src, N)
    rows = []
    for p, q in PAIRS:
        live = any(x != 0 for r in C.oriented(src, p, q) for x in r)
        row = {"pair": [p, q], "live": live,
               "rank": C.matrix_rank(C.oriented(src, p, q))}
        if live:
            U = tuple(x for x in range(N) if x not in (p, q))
            v1, d1, mp = DEC.decide_pair(src, p, q, U, f"{tag}A{p}{q}",
                                         primes=(32003, 1000003))
            isrc, _ = DEC.clear_denominators(src)
            v2, d2 = N6.decide_pair_general(isrc, p, q, U, f"{tag}B{p}{q}")
            row.update({"w23": v1, "dimQ": d1, "modp": mp, "w22": v2,
                        "agree": v1 == v2,
                        "det_p": sum(1 for a in U if all(
                            x == 0 for r in C.oriented(src, p, a) for x in r)),
                        "det_q": sum(1 for a in U if all(
                            x == 0 for r in C.oriented(src, q, a) for x in r))})
        rows.append(row)
    live = [r for r in rows if r["live"]]
    return {"in_X2": ok2, "first_bad_word": None if ok2 else list(badw),
            "pures": [str(pu[c]) for c in range(3)],
            "n_live": len(live),
            "n_witness": sum(1 for r in live if r["w23"] == "WITNESS"),
            "n_blocked": sum(1 for r in live if r["w23"] == "BLOCKED"),
            "all_blocked": bool(live) and all(r["w23"] == "BLOCKED"
                                              for r in live),
            "decider_disagreements": sum(1 for r in live if not r["agree"]),
            "modp_mismatch": sum(1 for r in live for ch, dd in r["modp"].items()
                                 if (dd == -1) != (r["dimQ"] == -1)),
            "ranks": sorted(r["rank"] for r in rows),
            "rows": rows}


def main():
    rng = random.Random(31337)
    words2 = WK.near_constant_words(N, 3, 2)
    ne = C.near_exact_six_site()

    # ---- (6) explicit-point control FIRST: the battery must find witnesses --
    print("[control] the battery on the committed near-exact source "
          "(known: 9 witnesses)", flush=True)
    ctrl = full_battery(ne, "CTL")
    print(f"   in X_2 {ctrl['in_X2']}, pures {ctrl['pures']}, live "
          f"{ctrl['n_live']}, witness {ctrl['n_witness']}, blocked "
          f"{ctrl['n_blocked']}, decider disagreements "
          f"{ctrl['decider_disagreements']}, mod-p mismatches "
          f"{ctrl['modp_mismatch']}", flush=True)
    RES["control_near_exact"] = {k: v for k, v in ctrl.items() if k != "rows"}

    # ---- build walked X_2 objects and look for all-blocked ones ------------
    found = []
    examined = 0
    while examined < 40 and len(found) < 4:
        src = ne
        steps = rng.randint(2, 8)
        okwalk = True
        for t in range(steps):
            new, dims = WK.walk_step(src, t % N, N, words2, rng, spread=2)
            if new is None:
                okwalk = False
                break
            src = new
        if not okwalk:
            continue
        examined += 1
        bat = full_battery(src, f"W{examined}")
        if bat["all_blocked"]:
            blocks = {f"{a},{b}": [[str(x) for x in row]
                                   for row in src[(a, b)]] for a, b in PAIRS}
            found.append({"battery": {k: v for k, v in bat.items()
                                      if k != "rows"},
                          "rows": bat["rows"], "blocks": blocks})
            print(f"\n   >>> ALL-BLOCKED X_2 OBJECT #{len(found)} "
                  f"(walked object {examined})", flush=True)
            print(f"       in X_2 (raw words) {bat['in_X2']}; pures "
                  f"{bat['pures']}; live {bat['n_live']}; ranks {bat['ranks']}",
                  flush=True)
            print(f"       decider disagreements "
                  f"{bat['decider_disagreements']}; mod-p mismatches "
                  f"{bat['modp_mismatch']}", flush=True)
            print(f"       per-pair: "
                  f"{[(r['pair'], r['w23'], r['dimQ']) for r in bat['rows'] if r['live']]}",
                  flush=True)
        else:
            print(f"   walked object {examined}: live {bat['n_live']}, witness "
                  f"{bat['n_witness']}, ranks {bat['ranks']}", flush=True)
    RES["examined"] = examined
    RES["all_blocked_found"] = found
    print(f"\n{examined} walked X_2 objects examined; ALL-BLOCKED: "
          f"{len(found)}")

    with open(f"{BASE}/results_t2f_x2_allblocked.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t2f_x2_allblocked.json")


if __name__ == "__main__":
    main()
