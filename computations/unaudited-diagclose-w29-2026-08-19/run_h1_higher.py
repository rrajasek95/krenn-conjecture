#!/usr/bin/env python3
"""W29 H1 -- the same machine at HIGHER EVEN ORDERS (N = 10, 12, ...).

Nothing in W29-B1/B2 or in the vanishing-pattern abstraction is special to
N = 8: for any even n, deleting a site z leaves V' of odd size n-1, the three
witness sites y_0,y_1,y_2 are distinct, and F_c is contained in {y_c} + Q with
Q = V' - {y_0,y_1,y_2} of size n-4.  So the ledger is the set of triples
(R_0,R_1,R_2) of subsets of Q.

ORBIT ENUMERATION.  A triple of subsets of Q is a map Q -> 2^{0,1,2}; the
residual symmetry is S_Q x S_3 (site relabelling inside Q, and permuting the
three colour/site pairs together).  So an orbit is exactly a PROFILE: the
multiset of the eight region sizes n_T = #{q in Q : {c : q in R_c} = T}, taken
up to the S_3 action on the labels.  That is C(|Q|+7,7) profiles before the
S_3 quotient -- 330 at n = 8 (giving the 87 orbits found by brute force),
1716 at n = 10, 6435 at n = 12.

argv: [n ...]
"""
from __future__ import annotations

import json
import sys
import time
from itertools import combinations, permutations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import run_c2_unified as U                                          # noqa: E402

RES, RAN = {}, []
OUT = (f"{BASE}/results_h1_higher_"
       + "_".join(sys.argv[1:] or ["8", "10", "12"]) + ".json")


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


SUBS = [frozenset(S) for k in range(4) for S in combinations((0, 1, 2), k)]


def profiles(m):
    """All (n_T) with sum m, one representative triple each, up to S_3."""
    out, seen = [], set()

    def rec(i, left, acc):
        if i == len(SUBS) - 1:
            acc2 = acc + [left]
            key = canon(acc2)
            if key not in seen:
                seen.add(key)
                out.append(acc2)
            return
        for v in range(left + 1):
            rec(i + 1, left - v, acc + [v])
    rec(0, m, [])
    return out


def canon(prof):
    best = None
    for pi in permutations(range(3)):
        m = {}
        for T, v in zip(SUBS, prof):
            m[frozenset(pi[c] for c in T)] = v
        key = tuple(m[T] for T in SUBS)
        if best is None or key < best:
            best = key
    return best


def triple_of(prof, Q):
    """A representative (R_0,R_1,R_2) with the given region profile."""
    Rs = [[], [], []]
    i = 0
    for T, v in zip(SUBS, prof):
        for _ in range(v):
            q = Q[i]
            i += 1
            for c in T:
                Rs[c].append(q)
    return tuple(tuple(sorted(r)) for r in Rs)


def orbit_size(prof, m):
    """#triples in this orbit = (multinomial) x (S_3 orbit of the profile)."""
    import math
    mult = math.factorial(m)
    for v in prof:
        mult //= math.factorial(v)
    labs = {canon([prof[SUBS.index(frozenset(pi[c] for c in T))]
                   for T in SUBS]) for pi in permutations(range(3))}
    forms = set()
    for pi in permutations(range(3)):
        forms.add(tuple(prof[SUBS.index(frozenset(
            [x for x in range(3) if pi[x] in T]))] for T in SUBS))
    return mult * len(forms)


def run_order(n, kmax=None, verbose=200):
    Q = tuple(range(3, n - 1))
    m = len(Q)
    profs = profiles(m)
    t0 = time.time()
    nsat, tot, sats = 0, 0, []
    for i, pr in enumerate(profs):
        Rs = triple_of(pr, Q)
        van = U.build_van(n, Rs, kmax=kmax, z=n - 1)
        tot += 1
        if not van.is_unsat():
            nsat += 1
            sats.append([list(r) for r in Rs])
        if verbose and (i + 1) % verbose == 0:
            print(f"    ... {i+1}/{len(profs)} orbits, {nsat} SAT "
                  f"({round(time.time()-t0,1)}s)", flush=True)
    return {"n": n, "kmax": kmax, "Q_size": m, "n_orbits": len(profs),
            "n_sat_orbits": nsat, "sat_examples": sats[:20],
            "secs": round(time.time() - t0, 1)}


def main():
    ns = [int(a) for a in sys.argv[1:]] or [8, 10, 12]
    # cross-check the orbit machinery against the n=8 brute force (87 orbits)
    RES["orbit_selfcheck"] = {"n8_profiles": len(profiles(4)),
                              "expected_87": len(profiles(4)) == 87}
    print(f"[selfcheck] |Q|=4 gives {len(profiles(4))} orbits "
          f"(brute force found 87)", flush=True)
    RAN.append("orbit_selfcheck")
    ck("selfcheck")
    for n in ns:
        print(f"=== H1 order n = {n} ===", flush=True)
        if n <= 10:
            r3 = run_order(n, kmax=3, verbose=0)
            print(f"  k=3 calibration: {r3['n_sat_orbits']}/"
                  f"{r3['n_orbits']} orbits SAT (must be > 0)", flush=True)
            RES.setdefault("orders", {}).setdefault(str(n), {})["k3"] = r3
            ck(f"n{n}_k3")
        r = run_order(n)
        RES.setdefault("orders", {}).setdefault(str(n), {})["k_full"] = r
        print(f"  >>> n={n}: {r['n_sat_orbits']}/{r['n_orbits']} orbits "
              f"satisfiable ({r['secs']}s)", flush=True)
        RAN.append(f"order{n}")
        ck(f"n{n}")
    RES["CONCLUSION"] = {
        str(n): ("no diagonal exact source at N=%d [PROVED-HERE]" % n
                 if RES["orders"][str(n)]["k_full"]["n_sat_orbits"] == 0
                 else "not decided")
        for n in ns}
    ck("final")
    print(">>> " + json.dumps(RES["CONCLUSION"]))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
