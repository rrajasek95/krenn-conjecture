#!/usr/bin/env python3
"""W27 T2c -- TEST THE SKELETON WITNESS LAW AT N = 8.

THE LAW (W27-S1), read off exhaustively from all 279 live pairs of all 24
diagonal skeleton classes at N = 6 (perfect separation, no exception):

    Let e = pq be a live pair of colour c1, and for a vertex v write
    d_c(v) = the number of colour-c edges at v.  Call v
        c1-SIMPLE      if d_{c1}(v) = 1  (e is the only c1-edge at v);
        ALMOST-CLEAN   if d_{c1}(v) = 2 and d_{c2}(v) = d_{c3}(v) = 1.
    Then  (p,q) carries a WITNESS  <=>  some endpoint is c1-simple,
                                        OR both endpoints are almost-clean.

This runner tests it on the diagonal stratum at N = 8:
  * Delta^3_8 (every vertex clean -> the law predicts witness everywhere);
  * ENLARGED diagonal X_3 = X_2 skeletons at N = 8 (extra edges added subject
    to the (6,2,0) filter), which produce endpoints of every degree type.
Predicted WITNESS is confirmed by an EXPLICIT exact cap (a sufficient test);
predicted BLOCKED must be confirmed by the full Rabinowitsch decision (the
expensive direction), so those are run in full and checkpointed one by one.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
W25BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-x3core-w25-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W25BASE)
import w27_core as W                                              # noqa: E402
import w25_decide as D                                            # noqa: E402
import run_t3c_n8_rungs as T3C                                    # noqa: E402
C = W.C

N = 8
G = W.Graph(N)
RES = {"objects": []}
RAN = []
OUT = f"{BASE}/results_t2c_n8law.json"


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


# ------------------------------------------------------------------- the law

def degvec(Ls, v):
    return [sum(1 for e in Ls[c] if v in e) for c in range(3)]


def predict(Ls, p, q):
    e = tuple(sorted((p, q)))
    c1 = [c for c in range(3) if e in Ls[c]]
    assert len(c1) == 1
    c1 = c1[0]
    others = [c for c in range(3) if c != c1]
    dp, dq = degvec(Ls, p), degvec(Ls, q)

    def simple(d):
        return d[c1] == 1

    def almost(d):
        return d[c1] == 2 and all(d[c] == 1 for c in others)

    w = simple(dp) or simple(dq) or (almost(dp) and almost(dq))
    return ("WITNESS" if w else "BLOCKED"), c1, dp, dq


# ------------------------------------------------------------- skeleton gen

def rand_disjoint_pms(rng):
    used, Ms = set(), []
    for _ in range(3):
        for _ in range(600):
            pp = list(range(N))
            rng.shuffle(pp)
            M = W.pm_norm([(pp[2 * i], pp[2 * i + 1]) for i in range(N // 2)])
            if not (set(M) & used):
                break
        else:
            return None
        used |= set(M)
        Ms.append(list(M))
    return Ms


def x2_ok(Ls):
    """The diagonal X_2 = X_3 filter at N=8, no-cancellation form:
    for c != d and every edge ab in L_d, L_c has NO perfect matching on
    V - {a,b}."""
    for c in range(3):
        mk = G.mask(Ls[c])
        for d in range(3):
            if d == c:
                continue
            for (a, b) in Ls[d]:
                rest = [x for x in range(N) if x not in (a, b)]
                if G.npm_on(mk, rest) > 0:
                    return False
    return True


def enlarge(Ms, rng, tries=14):
    Ls = [list(M) for M in Ms]
    used = set().union(*[set(x) for x in Ls])
    pool = [e for e in G.E if e not in used]
    rng.shuffle(pool)
    for e in pool[:tries]:
        c = rng.randrange(3)
        cand = [list(x) for x in Ls]
        cand[c] = sorted(cand[c] + [e])
        if x2_ok(cand):
            Ls = cand
    return Ls


def weights(Ls, rng):
    """Weights with every pure hafnian equal to 1 (solve the last edge of each
    colour linearly -- the hafnian is multilinear)."""
    wts = {}
    for c, L in enumerate(Ls):
        mk = G.mask(L)
        pms = [M for M in G.PMS if all((mk >> G.EI[f]) & 1 for f in M)]
        if not pms:
            return None
        last = L[rng.randrange(len(L))]
        w = {f: Fraction(rng.choice([1, -1, 2, -2, 3])) for f in L if f != last}
        alpha = Fraction(0)
        beta = Fraction(0)
        for M in pms:
            if last in M:
                pr = Fraction(1)
                for f in M:
                    if f != last:
                        pr *= w[f]
                alpha += pr
            else:
                pr = Fraction(1)
                for f in M:
                    pr *= w[f]
                beta += pr
        if alpha == 0:
            return None
        w[last] = (Fraction(1) - beta) / alpha
        if w[last] == 0:
            return None
        for f, v in w.items():
            wts[(c, f)] = v
    return wts


def main():
    t0 = time.time()
    rng = random.Random(4242)

    # --- assemble the objects: Delta^3_8 and enlarged skeletons
    objs = []
    for t in range(200):
        Ms = rand_disjoint_pms(rng)
        if Ms is None:
            continue
        Ls = [list(M) for M in Ms] if t % 3 == 0 else enlarge(Ms, rng)
        if not x2_ok(Ls):
            continue
        wts = weights(Ls, rng)
        if wts is None:
            continue
        src = W.build_diag(N, Ls, wts)
        if not C.in_Xk(src, N, 3)[0]:
            continue
        preds = {}
        for c in range(3):
            for e in Ls[c]:
                preds[f"{e[0]},{e[1]}"] = predict(Ls, *e)
        nB = sum(1 for v in preds.values() if v[0] == "BLOCKED")
        objs.append({"Ls": Ls, "wts": wts, "src": src, "preds": preds,
                     "nB": nB, "sizes": [len(L) for L in Ls]})
        if len(objs) >= 26:
            break
    objs.sort(key=lambda o: -o["nB"])
    print(f"objects built: {len(objs)}; predicted-blocked pairs per object: "
          f"{[o['nB'] for o in objs]}")
    RES["n_objects"] = len(objs)
    control("T2c0_objects")
    ck("objects")

    print("=" * 74)
    print("(1) FULL EXACT DECISION of EVERY live pair of EVERY object")
    print("=" * 74)
    rows = []
    agree = 0
    dis = []
    for oi, o in enumerate(objs):
        src = o["src"]
        for k, pr in sorted(o["preds"].items()):
            p, q = (int(x) for x in k.split(","))
            U = tuple(x for x in range(N) if x not in (p, q))
            t1 = time.time()
            v, d, mp = D.decide_pair(src, p, q, U, f"L{oi}_{p}{q}", primes=())
            ok = (v == pr[0])
            agree += int(ok)
            if not ok:
                dis.append({"obj": oi, "pair": k, "predicted": pr[0],
                            "decided": v, "deg_p": pr[2], "deg_q": pr[3],
                            "colour": pr[1], "sizes": o["sizes"]})
            rows.append({"obj": oi, "sizes": o["sizes"], "pair": k,
                         "colour": pr[1], "deg_p": pr[2], "deg_q": pr[3],
                         "predicted": pr[0], "decided": v, "dim": d,
                         "agree": ok, "seconds": round(time.time() - t1, 2)})
        nb = sum(1 for r in rows if r["obj"] == oi
                 and r["predicted"] == "BLOCKED")
        na = sum(1 for r in rows if r["obj"] == oi and r["agree"])
        nt = sum(1 for r in rows if r["obj"] == oi)
        print(f"   object {oi:2d} sizes {o['sizes']}: {nt} live pairs "
              f"({nb} predicted BLOCKED); law agrees on {na}/{nt}", flush=True)
        RES["decisions"] = rows
        RES["disagreements"] = dis
        ck(f"obj{oi}")
    print(f"   TOTAL pairs decided {len(rows)}; law correct {agree}; "
          f"DISAGREEMENTS {len(dis)}")
    for x in dis[:12]:
        print(f"      *** {x}")
    RES["totals"] = {"pairs": len(rows), "agree": agree,
                     "disagreements": len(dis)}
    control("T2c1_witness_side")
    control("T2c2_blocked_side")
    ck("decisions")

    declared = ["T2c0_objects", "T2c1_witness_side", "T2c2_blocked_side"]
    missing = [x for x in declared if x not in RAN]
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
