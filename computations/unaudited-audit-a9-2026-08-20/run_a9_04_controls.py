#!/usr/bin/env python3
"""A9-04: clause-family validity against REAL objects + identity tests + the
mutation ledger (link 3, link 5, ledger 18/21).

  P1  the N=4 exceptional source: normal form at every site, 0 violations,
      system SAT.
  P2  X_3 diagonal sources at N=8 (disjoint PM triples, random weights):
      normal form at all 8 sites, 0 violations at k=3; and at k=4 the SAME
      object MUST violate something (firing negative).
  P3  RICHER X_3 sources (support beyond one matching) -> other cases.
  P4  identity tests of the two non-trivial clause derivations (A3 Laplace,
      XF collapse) on random weights, plus the W28-FREE support claim and
      W29-B1/B2 on real X_3 objects.
  P5  MUTATION CONTROLS: five deliberate breakages, each must be caught.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import a9_haf as H                                                   # noqa: E402
import a9_enc as E                                                   # noqa: E402
import a9_ctrl as X                                                  # noqa: E402

RES = {}
OUT = f"{BASE}/results_a9_04_controls.json"
T0 = time.time()


def ck(tag=""):
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"   [ck {tag}] {round(time.time() - T0, 1)}s", flush=True)


# ------------------------------------------------------------------- P1
def p1_n4():
    n = 4
    pms = H.perfect_matchings(tuple(range(n)))
    ts = X.pm_source(n, pms)                       # all three PMs of K_4
    out = {"n_pms": len(pms),
           "exact_violations": len(H.exact_violations_raw(ts, n)),
           "sites": {}}
    for z in range(n):
        for k in (2, None):
            r = X.check_point(ts, n, z, k)
            out["sites"][f"z{z}_k{k}"] = r
    out["PASS"] = (out["exact_violations"] == 0 and
                   all(v["PASS"] for v in out["sites"].values()))
    return out


# ------------------------------------------------------------------- P2/P3
def p2_x3(nobj=60, n=8, seed=990):
    rng = random.Random(seed)
    trips = X.disjoint_pm_triples(n, rng, ntries=3000)
    out = {"objects": 0, "site_checks": 0, "violations": 0,
           "normal_form_failures": 0, "cases": {}, "k4_fires": 0,
           "k4_checked": 0, "examples": []}
    for Ms in trips[:nobj]:
        ws = [X.unit_product_weights(rng, len(M)) for M in Ms]
        ts = X.pm_source(n, Ms, ws)
        if X.x3_violations(ts, n):
            out["examples"].append("BAD X3 CONSTRUCTION")
            continue
        out["objects"] += 1
        for z in range(n):
            r = X.check_point(ts, n, z, 3)
            out["site_checks"] += 1
            if not r.get("PASS"):
                if "normal_form" in r:
                    out["normal_form_failures"] += 1
                else:
                    out["violations"] += r["n_violations"]
                if len(out["examples"]) < 5:
                    out["examples"].append(r)
            else:
                key = str(r["Rs"])
                out["cases"][key] = out["cases"].get(key, 0) + 1
        # firing negative: the same object at k=4 must be caught
        r4 = X.check_point(ts, n, 0, 4)
        out["k4_checked"] += 1
        if not r4.get("PASS"):
            out["k4_fires"] += 1
    out["PASS"] = (out["violations"] == 0 and
                   out["normal_form_failures"] == 0 and
                   out["objects"] > 0 and
                   out["k4_fires"] == out["k4_checked"])
    return out


def p3_rich(nobj=40, n=8, seed=4242):
    rng = random.Random(seed)
    objs = X.rich_x3_search(n, rng, want=nobj, ntries=20000)
    out = {"objects": len(objs), "site_checks": 0, "violations": 0,
           "normal_form_failures": 0, "cases": {}, "examples": []}
    for ts in objs:
        for z in range(n):
            r = X.check_point(ts, n, z, 3)
            out["site_checks"] += 1
            if not r.get("PASS"):
                if "normal_form" in r:
                    out["normal_form_failures"] += 1
                else:
                    out["violations"] += r["n_violations"]
                if len(out["examples"]) < 5:
                    out["examples"].append(r)
            else:
                key = str(r["Rs"])
                out["cases"][key] = out["cases"].get(key, 0) + 1
    out["distinct_cases"] = len(out["cases"])
    out["PASS"] = (out["violations"] == 0 and
                   out["normal_form_failures"] == 0)
    return out


# ------------------------------------------------------------------- P4
def p4_identities(trials=400, seed=31):
    rng = random.Random(seed)
    res = {}
    # --- A3: haf(S) != 0  =>  some u with t_{wu} != 0 and haf(S-w-u) != 0
    bad_a3, checked_a3 = 0, 0
    for _ in range(trials):
        n = rng.choice([6, 8])
        V = tuple(range(n))
        t = {}
        for e in combinations(V, 2):
            if rng.random() < rng.choice([0.25, 0.5, 0.9]):
                t[e] = Fraction(rng.randint(-4, 4), rng.randint(1, 3))
        m = rng.choice([4, 6, 8])
        if m > n:
            continue
        S = tuple(sorted(rng.sample(V, m)))
        w = rng.choice(S)
        checked_a3 += 1
        if H.haf_dp(t, S) != 0:
            ok = any(t.get(H.ek(w, u), 0) != 0 and
                     H.haf_dp(t, tuple(x for x in S if x not in (w, u))) != 0
                     for u in S if u != w)
            if not ok:
                bad_a3 += 1
    res["A3_laplace"] = {"checked": checked_a3, "failures": bad_a3,
                         "PASS": bad_a3 == 0}
    # --- XF: if t_{z,y} = 0 for all y in S_0 - y_c then
    #         haf(t|S_0+z) = t_{z,y_c} haf(t|S_0-y_c)  (exact identity)
    bad_xf, checked_xf = 0, 0
    for _ in range(trials):
        n = 8
        V = tuple(range(n))
        z = n - 1
        VP = tuple(range(n - 1))
        S0 = tuple(sorted(rng.sample(VP, rng.choice([1, 3, 5, 7]))))
        yc = rng.choice(S0)
        t = {}
        for e in combinations(V, 2):
            if rng.random() < 0.7:
                t[e] = Fraction(rng.randint(-4, 4), rng.randint(1, 3))
        for y in S0:
            if y != yc:
                t.pop(H.ek(z, y), None)
        lhs = H.haf_dp(t, tuple(sorted(S0 + (z,))))
        rhs = t.get(H.ek(z, yc), Fraction(0)) * \
            H.haf_dp(t, tuple(x for x in S0 if x != yc))
        checked_xf += 1
        if lhs != rhs:
            bad_xf += 1
    res["XF_identity"] = {"checked": checked_xf, "failures": bad_xf,
                          "PASS": bad_xf == 0}
    # --- W28-FREE support + B1 + B2 on real X_3 objects
    rng2 = random.Random(77)
    trips = X.disjoint_pm_triples(8, rng2, ntries=800)[:25]
    bad_supp = bad_b1 = bad_b2 = 0
    nchk = 0
    for Ms in trips:
        ws = [X.unit_product_weights(rng2, len(M)) for M in Ms]
        ts = X.pm_source(8, Ms, ws)
        for z in range(8):
            VP = [x for x in range(8) if x != z]
            F = [X.free_set(ts, c, 8, z, 3) for c in range(3)]
            nchk += 1
            for c in range(3):
                for y in VP:
                    if y not in F[c] and ts[c].get(H.ek(z, y), 0) != 0:
                        bad_supp += 1           # W28-FREE would be violated
                for y in F[c]:
                    for d in range(3):
                        if d != c and H.haf_dp(
                                ts[d], tuple(x for x in VP if x != y)) != 0:
                            bad_b1 += 1         # W29-B1 would be violated
            nf = X.normal_form(ts, 8, z, 3)
            if "FAIL" in nf or not nf["B1_inside"]:
                bad_b2 += 1
    res["FREE_support_B1_B2"] = {"site_checks": nchk,
                                 "support_failures": bad_supp,
                                 "B1_failures": bad_b1,
                                 "B2_failures": bad_b2,
                                 "PASS": not (bad_supp or bad_b1 or bad_b2)}
    res["PASS"] = all(v["PASS"] for v in res.values() if isinstance(v, dict))
    return res


# ------------------------------------------------------------------- P5
def p5_mutations():
    """Each mutation must CHANGE the verdict or FIRE a violation.  If a
    mutation is silent, the corresponding control is not load-bearing."""
    out = {}
    reps8 = [((), (), ()), ((3,), (4,), (5,)), ((3, 4, 5, 6),) * 3,
             ((3, 4), (4, 5), (5, 6))]

    # M1: flip the polarity of the FREE clauses (should turn UNSAT into SAT
    #     or otherwise disagree) -- detects a sign slip in the encoder.
    class FlipFR(E.Enc):
        def add(self, tag, cl):
            if tag[0] == "FR":
                cl = [-l for l in cl]
            super().add(tag, cl)

    m1 = []
    for Rs in reps8:
        e = FlipFR(8, Rs, k=4).build()
        m1.append(e.solve_pysat()[0])
    out["M1_flip_FREE_polarity"] = {"sat": m1, "CAUGHT": any(m1)}

    # M2: drop the off-count filter at k=3 (imports k=4 rows) -- the k=3
    #     system must then become UNSAT somewhere, i.e. the filter matters.
    class NoFilter(E.Enc):
        def keep(self, sizes):
            return True

    m2 = [NoFilter(8, Rs, k=3).build().solve_pysat()[0] for Rs in reps8]
    m2ref = [E.Enc(8, Rs, k=3).build().solve_pysat()[0] for Rs in reps8]
    out["M2_kfilter"] = {"unfiltered_sat": m2, "filtered_sat": m2ref,
                         "CAUGHT": m2 != m2ref}

    # M3: perturb the case hypothesis -- assert C0 for a y that IS free
    #     (an UNSOUND extra clause).  A real X_3 object must then violate it.
    rng = random.Random(5)
    trips = X.disjoint_pm_triples(8, rng, ntries=600)[:5]
    fired = 0
    for Ms in trips:
        ts = X.pm_source(8, Ms, [X.unit_product_weights(rng, len(M))
                                 for M in Ms])
        nf = X.normal_form(ts, 8, 0, 3)
        ts2 = X.relabel(ts, nf["perm"])
        Rs = tuple(tuple(r) for r in nf["Rs"])
        bad = tuple((tuple(x for x in R if x != 3) if i == 0 else R)
                    for i, R in enumerate(Rs))       # shrink F_0 wrongly
        e = E.Enc(8, bad, k=3).build()
        viol = e.violations(e.truth(ts2, H.haf_dp))
        if viol:
            fired += 1
    out["M3_wrong_case"] = {"objects": len(trips), "fired": fired,
                            "CAUGHT": fired == len(trips)}

    # M4: corrupt the source (one weight) and check the X_3 test catches it.
    fired4 = 0
    for Ms in trips:
        ts = X.pm_source(8, Ms, [X.unit_product_weights(rng, len(M))
                                 for M in Ms])
        c = rng.randrange(3)
        e0 = list(ts[c])[0]
        ts[c][e0] = ts[c][e0] + 1
        if X.x3_violations(ts, 8):
            fired4 += 1
    out["M4_corrupt_source"] = {"objects": len(trips), "fired": fired4,
                                "CAUGHT": fired4 == len(trips)}

    # M5: a DIFFERENT normalisation choice (pick=1 among the y_c witnesses)
    #     must give the same verdict -- the normal form must not depend on
    #     which witness is picked.
    same = 0
    tot = 0
    for Ms in trips:
        ts = X.pm_source(8, Ms, [X.unit_product_weights(rng, len(M))
                                 for M in Ms])
        for z in range(8):
            r0 = X.check_point(ts, 8, z, 3, pick=0)
            r1 = X.check_point(ts, 8, z, 3, pick=1)
            tot += 1
            if r0.get("PASS") and r1.get("PASS"):
                same += 1
    out["M5_witness_choice"] = {"checks": tot, "both_pass": same,
                                "CAUGHT": same == tot}
    out["PASS"] = all(v["CAUGHT"] for v in out.values() if isinstance(v, dict))
    return out


def main():
    what = sys.argv[1:] or ["p1", "p4", "p5", "p2", "p3"]
    for w in what:
        RES[w] = {"p1": p1_n4, "p2": p2_x3, "p3": p3_rich,
                  "p4": p4_identities, "p5": p5_mutations}[w]()
        print(f"== {w}: {json.dumps(RES[w], default=str)[:600]}", flush=True)
        ck(w)
    RES["seconds"] = round(time.time() - T0, 1)
    ck("final")


if __name__ == "__main__":
    main()
