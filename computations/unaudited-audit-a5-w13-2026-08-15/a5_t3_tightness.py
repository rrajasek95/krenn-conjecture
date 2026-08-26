#!/usr/bin/env python3
"""A5 / claims 2+3: membership E_w in L_h(A), and the tightness claim
span{E_w} = L_h at h=2,3,4.

Protocol:
 * the fast evaluator is CERTIFIED against a5_core.cap_error_raw (raw eq. (4))
   on a random sample of words for every source used;
 * membership is exact over Q (Fraction reduction against an exact integer
   echelon of my Sigma-power basis of L_h);
 * the span dimension uses rank over F_p at two primes together with the
   proved structural upper bound dim span{E_w} <= dim L_h (established
   exactly, by the membership test), which pins the rational rank exactly.
"""
from __future__ import annotations
import json, random, sys, time
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A
import a5_fast as F
import numpy as np

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"
P1, P2 = (1 << 61) - 1, 2147483647
res = {"certify": [], "membership": [], "tightness": [], "controls": []}
rng = random.Random(31337)

HS = [int(x) for x in sys.argv[1:]] or [2, 3]

for h in HS:
    for si, (tag, kw) in enumerate([("dense", {}), ("sparse", {"zero_prob": 0.3}),
                                    ("wide", {"lo": -9, "hi": 9})]):
        src = A.random_source(h, rng, **kw)
        svec = A.s_vector(src)
        bmats = F.block_matrices(h, svec)
        # --- certify the fast route against the raw definitional route
        t0 = time.time()
        nsample = 25 if h < 4 else 8
        words_all = A.all_words(h)
        sample = [rng.choice(words_all) for _ in range(nsample)]
        bad = 0
        for w in sample:
            v1 = A.poly_vec(A.cap_error_raw(src, h, w), h)
            v2 = F.error_vec_fast(src, h, w, bmats)
            if v1 != v2:
                bad += 1
        print(f"h={h} src={tag}: fast-vs-raw mismatches {bad}/{nsample} "
              f"[{time.time()-t0:.1f}s]", flush=True)
        res["certify"].append({"h": h, "src": tag, "sample": nsample, "mismatch": bad})
        assert bad == 0

        # --- all E_w
        t0 = time.time()
        words, M = F.all_error_vectors(src, h, bmats)
        print(f"  built {M.shape} error vectors [{time.time()-t0:.1f}s]", flush=True)

        # --- exact membership in L_h
        Lr = A.L_rows(h, svec, rng)
        ech, piv = A.int_echelon(Lr)
        dimL = len(piv)
        t0 = time.time()
        nfail, checked = 0, 0
        idxs = range(len(words)) if h <= 3 else rng.sample(range(len(words)), 150)
        for i in idxs:
            v = [int(x) for x in M[i]]
            if not any(v):
                continue
            checked += 1
            if not A.in_span_exact(ech, piv, v):
                nfail += 1
                if nfail < 3:
                    print("   *** NOT IN L_h:", words[i])
        print(f"  exact membership: {checked} nonzero E_w checked, {nfail} failures "
              f"[{time.time()-t0:.1f}s]", flush=True)
        res["membership"].append({"h": h, "src": tag, "dimL": dimL,
                                  "checked": checked, "failures": nfail,
                                  "exhaustive": h <= 3})

        # --- tightness: rank of span{E_w}
        rows = [[int(x) for x in M[i]] for i in range(M.shape[0])]
        r1 = A.rank_mod_p(rows, P2)
        r2 = A.rank_mod_p(rows, 1000003)
        print(f"  rank span(E_w) mod {P2} = {r1}; mod 1000003 = {r2}; dim L_h = {dimL}",
              flush=True)
        res["tightness"].append({"h": h, "src": tag, "rank_p1": r1, "rank_p2": r2,
                                 "dimL": dimL, "fills": r1 == dimL and r2 == dimL})

        # --- controls
        if h >= 3:
            # truncated law: drop the last (k=2) summand -> membership must FAIL
            Lt = A.L_rows(h, svec, rng, kmin=3)
            et, pt = A.int_echelon(Lt)
            fails = 0
            for i in list(idxs)[:60]:
                v = [int(x) for x in M[i]]
                if any(v) and not A.in_span_exact(et, pt, v):
                    fails += 1
            print(f"  CONTROL truncated law (kmin=3): {fails} of 60 rejected "
                  f"(want > 0)", flush=True)
            res["controls"].append({"h": h, "src": tag, "control": "truncated law kmin=3",
                                    "rejected": fails, "want_positive": True})
        # sign mutation: negate one E_w coordinate -> should leave L_h
        i0 = next(i for i in range(M.shape[0]) if any(M[i]))
        v = [int(x) for x in M[i0]]
        j0 = next(j for j in range(len(v)) if v[j])
        v2 = list(v); v2[j0] = -v2[j0]
        left = not A.in_span_exact(ech, piv, v2)
        print(f"  CONTROL sign-flip one coefficient leaves L_h: {left}", flush=True)
        res["controls"].append({"h": h, "src": tag, "control": "sign flip one coeff",
                                "left_L": left, "want": True})

json.dump(res, open(OUT + f"results_t3_tightness_h{'_'.join(map(str,HS))}.json", "w"), indent=1)
print("DONE")
