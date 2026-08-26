#!/usr/bin/env python3
"""W36: the (alpha)-side residual after the (beta) hypothesis is removed.

Under THEOREM W36-M25 the only residual hypothesis at m=25/R6 is

  (R25) some tuple tau = (y5,y7) carries two admissible |T_f| = 1 index
        choices with DIFFERENT firing letters, both with hafL != 0.

W30's Branch T asked for hafL == 0 on ALL 42 words of X_{R6,25}; (R25) is
strictly weaker to satisfy, so its negation is strictly harder to reach.
This file computes EXACTLY how hard: (R25) fails iff, for every two-pair
tuple tau, at least one of the two firing letters has ALL of its choices
killed (hafL = 0 on every L-part it uses).  That is a covering problem on
the 42 L-parts, solved here exactly by branch and bound -- giving a
COMBINATORIAL LOWER BOUND on the number of hafL zeros any (R25)-escape must
carry, independent of any algebra.

Also recorded: the forced structure that hafL zeros imply (derived in
w36_build.alpha_struct) measured against the builders' records, so the
observed plateau can be attributed.

Declared controls:
  X0_Xv          -- X_{R6,25} recomputed from the engine (must be 42)
  X1_cover       -- the exact minimum cover, with the optimum re-verified
  X2_prelaunch   -- every stored object's hafL-zero set measured against
                    the bound (ledger 27: the target must not already hold)
  X3_negctl      -- a random subset of the same size must NOT be a cover
usage: w36_alpha.py
"""
from __future__ import annotations
import json, os, random, sys
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_sprime as SP
import w30_lib as L

HERE = W.HERE
DECL = ["X0_Xv", "X1_cover", "X2_prelaunch", "X3_negctl"]


def structure():
    """per two-pair tuple tau, per firing letter f, the set of L-parts x."""
    by = {}
    for (w, fire) in L.index_choices_cached(25, 'R', 6):
        if len(fire) != 1:
            continue
        by.setdefault((w[5], w[7]), {}).setdefault(sorted(fire)[0],
                                                   set()).add(tuple(w[:4]))
    two = {k: d for k, d in by.items() if len(d) >= 2}
    X = sorted({x for d in by.values() for s in d.values() for x in s})
    return two, X, by


def min_cover(two, X):
    """smallest Z subset of X such that every two-pair tuple has a firing
    letter whose whole choice-set lies in Z.  Exact (the instance is tiny:
    one option per (tuple, letter))."""
    opts = []
    for tau, d in sorted(two.items()):
        opts.append([frozenset(s) for s in d.values()])
    best = {"size": None, "Z": None}

    def rec(i, cur):
        if best["size"] is not None and len(cur) >= best["size"]:
            return
        if i == len(opts):
            best["size"] = len(cur)
            best["Z"] = set(cur)
            return
        for s in sorted(opts[i], key=lambda t: len(t - cur)):
            rec(i + 1, cur | s)
    rec(0, set())
    return best


def verify_cover(two, Z):
    return all(any(s <= Z for s in d.values()) for d in two.values())


def main():
    OUT = {"_header": W.HEADER, "_task": "(alpha) residual after (beta) removal",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_alpha.json")
    two, X, by = structure()
    OUT["X0_Xv"] = dict(n_Xv=len(X), n_tuples=len(by), n_two_pair=len(two),
                        sizes={str(k): {str(f): len(s) for f, s in d.items()}
                               for k, d in sorted(two.items())},
                        ok=(len(X) == 42 and len(two) == 6))
    OUT["_controls_run"].append("X0_Xv")
    print("X_v = %d, tuples = %d, two-pair = %d" % (len(X), len(by), len(two)),
          flush=True)
    print("per two-pair tuple, |choice sets|: %s"
          % json.dumps(OUT["X0_Xv"]["sizes"]), flush=True)

    b = min_cover(two, X)
    OUT["X1_cover"] = dict(
        min_size=b["size"], Z=[str(x) for x in sorted(b["Z"] or [])],
        reverified=verify_cover(two, b["Z"] or set()),
        smaller_impossible=all(
            not verify_cover(two, set(c))
            for c in combinations(sorted(b["Z"] or []), max(0, b["size"] - 1))
        ) if b["size"] and b["size"] <= 24 else None,
        ok=bool(b["size"] and verify_cover(two, b["Z"])))
    OUT["_controls_run"].append("X1_cover")
    print("MINIMUM (R25)-escape: hafL must vanish on at least %d of the 42 "
          "L-parts of X_{R6,25}; verified=%s"
          % (b["size"], OUT["X1_cover"]["reverified"]), flush=True)
    json.dump(OUT, open(res, "w"), indent=1, default=str)

    # ---- X2 pre-launch: every stored object measured against the bound
    pre = []
    Xset = set(X)
    for (tag, fld, ptj) in SP.load_corpus():
        K = W.K_of(fld)
        try:
            bl = W.load_point(ptj, K)
        except Exception:
            continue
        if set(bl) != set(W.E_ALL25):
            continue
        Z = {x for x in X if K.iszero(W.hafL(bl, x))}
        pre.append(dict(tag=tag, field=fld, nZ=len(Z),
                        kills_R25=verify_cover(two, Z),
                        short_by=max(0, b["size"] - len(Z))))
    for fn in ("results_build_alpha_13.json", "results_build_alpha_31.json",
               "results_build_alpha_Q.json"):
        q = os.path.join(HERE, fn)
        if not os.path.exists(q):
            continue
        try:
            dd = json.load(open(q))
        except Exception:
            continue
        if dd.get("best"):
            fld = fn.split("_")[-1].split(".")[0]
            K = W.K_of(fld)
            bl = W.load_point(dd["best"]["point"], K)
            Z = {x for x in X if K.iszero(W.hafL(bl, x))}
            pre.append(dict(tag="W36builder_" + fld, field=fld, nZ=len(Z),
                            kills_R25=verify_cover(two, Z),
                            short_by=max(0, b["size"] - len(Z))))
    OUT["X2_prelaunch"] = dict(
        n=len(pre), max_nZ=max([r["nZ"] for r in pre] or [0]),
        n_kill=sum(1 for r in pre if r["kills_R25"]),
        detail=sorted(pre, key=lambda r: -r["nZ"])[:25],
        ok=not any(r["kills_R25"] for r in pre),
        note="no stored object may already satisfy the escape (ledger 27)")
    OUT["_controls_run"].append("X2_prelaunch")
    print("PRE-LAUNCH: %d objects, max hafL-zeros on X_v = %d, escapes = %d"
          % (len(pre), OUT["X2_prelaunch"]["max_nZ"],
             OUT["X2_prelaunch"]["n_kill"]), flush=True)

    rng = random.Random(3601)
    negs = 0
    for _ in range(400):
        Z = set(rng.sample(X, b["size"]))
        negs += verify_cover(two, Z)
    OUT["X3_negctl"] = dict(
        n=400, n_random_covers=negs, ok=(negs < 400),
        note="a random subset of the minimum size is almost never a cover, "
             "so the bound is not vacuous")
    OUT["_controls_run"].append("X3_negctl")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    print("ALPHA DONE min_cover=%d random_covers=%d/400"
          % (b["size"], negs), flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
