#!/usr/bin/env python3
"""A5 / claim 1: THEOREM W13.1 (configuration expansion).

Route A = raw eq. (4) of the descent note (square-free algebra powers of r and
x, honest factorial denominators, full-support component).
Route B = my own configuration expansion (partial matchings J + permanents).
Route C = W13's own two implementations (imported ONLY here, for a
convention/agreement cross-check; never used for a verdict).

Zero tolerance, exact integers.
"""
from __future__ import annotations

import json
import random
import sys
import time
from itertools import product

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-induction-w13-2026-08-15")

import a5_core as A
import w13_core as W


def w13_vec(source, h, word, mode):
    if mode == "direct":
        f = W.error_poly_direct(source, h, word)
    else:
        f = W.graded_to_poly(source, h, W.graded_error(source, h, word))
    return W.poly_vector(f, W.NCAP, h)


def mine_vec(f, h):
    return A.poly_vec(f, h)


def run():
    res = {"agree": [], "mismatch": [], "controls": []}
    rng = random.Random(20260815)
    for h in (2, 3, 4):
        nsrc = 4 if h < 4 else 2
        nwords = 40 if h < 4 else 12
        for si in range(nsrc):
            src = A.random_source(h, rng, lo=-4, hi=4,
                                  zero_prob=(0.25 if si % 2 else 0.0))
            words = [tuple(rng.choice(A.C3) for _ in range(2 * h)) for _ in range(nwords)]
            if h == 2:
                words = list(product(A.C3, repeat=4))
            t0 = time.time()
            for w in words:
                fa = A.cap_error_raw(src, h, w)
                fb = A.cap_error_config(src, h, w)
                va, vb = A.poly_vec(fa, h), A.poly_vec(fb, h)
                vc = w13_vec(src, h, w, "direct")
                vd = w13_vec(src, h, w, "graded")
                # W13 uses sorted-index monomial keys, mine uses exponent
                # tuples: compare via a canonical map.
                vc2 = remap_w13(vc, h)
                vd2 = remap_w13(vd, h)
                ok = (va == vb == vc2 == vd2)
                rec = {"h": h, "src": si, "word": list(w),
                       "raw_eq_equals_config": va == vb,
                       "mine_equals_w13_direct": va == vc2,
                       "mine_equals_w13_graded": va == vd2,
                       "nonzero": any(va)}
                (res["agree"] if ok else res["mismatch"]).append(rec)
            print(f"h={h} src={si} words={len(words)} {time.time()-t0:.1f}s "
                  f"mismatches={len(res['mismatch'])}", flush=True)
    # ---- mutation controls: each must be DETECTED (i.e. produce a mismatch)
    rng2 = random.Random(7)
    h = 3
    src = A.random_source(h, rng2)
    w = (0, 1, 2, 0, 1, 2)
    base = A.poly_vec(A.cap_error_raw(src, h, w), h)
    ctl = []

    # C1: drop the k=h term of eq. (4)
    def raw_truncated(source, hh, word):
        f = A.cap_error_raw_partial(source, hh, word, kmax=hh - 1)
        return A.poly_vec(f, hh)
    ctl.append(("C1 drop k=h term", base != raw_truncated(src, h, w)))

    # C2: wrong factorial (use 1/k! only)
    ctl.append(("C2 wrong factorials",
                base != A.poly_vec(A.cap_error_raw_badfact(src, h, w), h)))
    # C3: R with only one of the two orientations
    ctl.append(("C3 one-sided R",
                base != A.poly_vec(A.cap_error_config_oneR(src, h, w), h)))
    # C4: |J| allowed up to h-1 in the config expansion
    ctl.append(("C4 J up to h-1",
                base != A.poly_vec(A.cap_error_config(src, h, w, jmax=h - 1), h)))
    # C5: perturb one source entry
    src2 = {k: [row[:] for row in v] for k, v in src.items()}
    src2[(2, 3)][0][0] += 1
    ctl.append(("C5 perturbed source",
                base != A.poly_vec(A.cap_error_raw(src2, h, w), h)))
    for name, detected in ctl:
        print("CONTROL", name, "DETECTED" if detected else "*** NOT DETECTED ***")
        res["controls"].append({"control": name, "detected": bool(detected)})
    res["n_agree"] = len(res["agree"])
    res["n_mismatch"] = len(res["mismatch"])
    res["agree"] = res["agree"][:5]
    with open("/Users/rishi/workplace/krenn-conjecture/computations/"
              "unaudited-audit-a5-w13-2026-08-15/results_t1_expansion.json", "w") as fh:
        json.dump(res, fh, indent=1)
    print("TOTAL agree", res["n_agree"], "mismatch", res["n_mismatch"])


_REMAP = {}


def remap_w13(vec, h):
    """Translate a W13 degree-h coefficient vector into my monomial order."""
    if h not in _REMAP:
        w13_ms = W.monomials(W.NCAP, h)
        idx = A.monom_index(h)
        perm = []
        for m in w13_ms:
            e = [0] * 9
            for v in m:
                e[v] += 1
            perm.append(idx[tuple(e)])
        _REMAP[h] = perm
    out = [0] * len(A.deg_monoms(h))
    for i, c in enumerate(vec):
        out[_REMAP[h][i]] += c
    return out


if __name__ == "__main__":
    run()
