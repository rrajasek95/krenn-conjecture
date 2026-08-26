#!/usr/bin/env python3
"""W23 T2e -- independent re-decision of the T2b headline.

T2b decided the 56 iso-classes of X_2 cap D6(1) with W22's decider (over Q
only).  This runner re-decides EVERY live pair of EVERY class with the W23
decider, over Q AND modulo 32003 and 1000003, and cross-checks the two
deciders pair by pair.  It also re-derives the detachment table from the
re-decided verdicts.
"""
from __future__ import annotations

import json
import sys
from itertools import combinations, permutations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-induction2-w22-2026-08-15")
import w23_core as C                                          # noqa: E402
import w23_decide as DEC                                      # noqa: E402
import run_t2b_diag6 as D6                                    # noqa: E402
import w22_n6 as N6                                           # noqa: E402

N = 6
RES = {}


def main():
    with open(f"{BASE}/results_t2b_diag6.json") as fh:
        T2B = json.load(fh)
    triples = [tuple(r["triple"]) for r in T2B["X2_blocking"]["rows"]]
    print(f"classes to re-decide: {len(triples)}", flush=True)
    tally = {}
    disagree = modp_bad = 0
    tot_live = tot_wit = 0
    per_class = []
    allb = 0
    for k, t in enumerate(triples):
        src = D6.source_of(t)
        nlive = nwit = 0
        for p, q in combinations(range(N), 2):
            if not DEC.live(src, p, q):
                continue
            U = tuple(x for x in range(N) if x not in (p, q))
            v, d, mp = DEC.decide_pair(src, p, q, U, f"R{k}{p}{q}",
                                       primes=(32003, 1000003))
            v2, d2 = N6.decide_pair_general(src, p, q, U, f"S{k}{p}{q}")
            if v != v2:
                disagree += 1
                print(f"   DISAGREEMENT class {k} pair ({p},{q}): {v} vs {v2}")
            for ch, dd in mp.items():
                if (dd == -1) != (d == -1):
                    modp_bad += 1
            nlive += 1
            nwit += int(v == "WITNESS")
            dp = sum(1 for a in U
                     if all(x == 0 for r in C.oriented(src, p, a) for x in r))
            dq = sum(1 for a in U
                     if all(x == 0 for r in C.oriented(src, q, a) for x in r))
            tally[(v, dp, dq)] = tally.get((v, dp, dq), 0) + 1
        tot_live += nlive
        tot_wit += nwit
        allb += int(nlive > 0 and nwit == 0)
        per_class.append({"triple": list(t), "live": nlive, "witness": nwit})
        if (k + 1) % 10 == 0:
            print(f"   ... {k+1}/{len(triples)} classes re-decided", flush=True)
    print(f"\nlive pairs {tot_live}, witnesses {tot_wit}, "
          f"ALL-BLOCKED classes {allb}")
    print(f"witness count per class: min "
          f"{min(c['witness'] for c in per_class)}, max "
          f"{max(c['witness'] for c in per_class)}")
    print(f"decider disagreements (W23 vs W22): {disagree}")
    print(f"mod-p verdict mismatches (32003, 1000003): {modp_bad}")
    print("\ndetachment table from the re-decided verdicts:")
    for key in sorted(tally, key=lambda x: (-tally[x], str(x))):
        print(f"   {key} -> {tally[key]}")
    RES = {"classes": len(triples), "live_pairs": tot_live,
           "witness_pairs": tot_wit, "all_blocked": allb,
           "min_witness": min(c["witness"] for c in per_class),
           "max_witness": max(c["witness"] for c in per_class),
           "decider_disagreements": disagree, "modp_mismatches": modp_bad,
           "detachment": {str(k): v for k, v in tally.items()},
           "per_class": per_class}
    with open(f"{BASE}/results_t2e_recheck.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("\nwrote results_t2e_recheck.json")


if __name__ == "__main__":
    main()
