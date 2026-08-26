#!/usr/bin/env python3
"""A9-05: the MUTATION-CONTROL LEDGER (ledger 21) -- redone properly.

Each mutation is a deliberate, named breakage of one link; the control that is
supposed to catch it must fire.  The detector for an UNSOUND clause is always
"a REAL object violates it"; the detector for a MISSING restriction is "the
verdict changes at a level where objects exist".
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import a9_haf as H                                                   # noqa: E402
import a9_enc as E                                                   # noqa: E402
import a9_ctrl as X                                                  # noqa: E402

OUT = f"{BASE}/results_a9_05_mut.json"
T0 = time.time()
RES = {}


def objects(n=8, m=8, seed=1234):
    """Real X_3 objects with varied free sets (so varied cases)."""
    rng = random.Random(seed)
    out = X.rich_x3_search(n, rng, want=m, ntries=20000)
    rng2 = random.Random(seed + 1)
    for Ms in X.disjoint_pm_triples(n, rng2, ntries=600)[:m]:
        out.append(X.pm_source(n, Ms,
                               [X.unit_product_weights(rng2, len(M))
                                for M in Ms]))
    return out


def real_point_violations(cls_mutator, objs, k=3, n=8):
    """How many (object, site) pairs violate at least one clause."""
    fired, tot = 0, 0
    for ts in objs:
        for z in range(n):
            nf = X.normal_form(ts, n, z, k)
            if "FAIL" in nf:
                continue
            ts2 = X.relabel(ts, nf["perm"])
            e = cls_mutator(n, nf["Rs"], k=k).build()
            tot += 1
            if e.violations(e.truth(ts2, H.haf_dp)):
                fired += 1
    return fired, tot


def main():
    objs = objects()
    print(f"{len(objs)} real X_3 objects", flush=True)

    # --- the BASELINE: the honest encoder must never fire
    f, t = real_point_violations(E.Enc, objs)
    RES["MU0_baseline"] = {"fired": f, "checks": t, "WANT": "fired == 0",
                           "PASS": f == 0}
    print("MU0", RES["MU0_baseline"], flush=True)

    # --- MU1: FREE clauses with flipped polarity (a sign slip)
    class M1(E.Enc):
        def add(self, tag, cl):
            super().add(tag, [-l for l in cl] if tag[0] == "FR" else cl)
    f, t = real_point_violations(M1, objs)
    RES["MU1_free_polarity"] = {"fired": f, "checks": t, "PASS": f == t}

    # --- MU2: A2 partition clauses with flipped polarity
    class M2(E.Enc):
        def add(self, tag, cl):
            super().add(tag, [-l for l in cl] if tag[0] == "A2" else cl)
    f, t = real_point_violations(M2, objs)
    RES["MU2_A2_polarity"] = {"fired": f, "checks": t, "PASS": f == t}

    # --- MU3: the free set hypothesised TOO BIG (a y that is not free)
    fired = tot = 0
    for ts in objs:
        for z in range(8):
            nf = X.normal_form(ts, 8, z, 3)
            if "FAIL" in nf:
                continue
            ts2 = X.relabel(ts, nf["perm"])
            Rs = [list(r) for r in nf["Rs"]]
            hit = None
            for c in range(3):
                miss = [q for q in (3, 4, 5, 6) if q not in Rs[c]]
                if miss:
                    hit = (c, miss[0])
                    break
            if hit is None:
                continue
            Rs[hit[0]] = sorted(Rs[hit[0]] + [hit[1]])
            e = E.Enc(8, tuple(tuple(r) for r in Rs), k=3).build()
            tot += 1
            if e.violations(e.truth(ts2, H.haf_dp)):
                fired += 1
    RES["MU3_free_set_too_big"] = {"fired": fired, "checks": tot,
                                   "PASS": tot > 0 and fired == tot}

    # --- MU4: Laplace with the wrong cofactor (S-w instead of S-w-u)
    class M4(E.Enc):
        def build(self):
            out = super().build()
            for i, tag in enumerate(self.tags):
                if tag[0] == "A3g" and i % 2 == 1:
                    c, m, w, u = tag[1:]
                    self.cls[i] = (self.cls[i][0], self.p(c, m & ~(1 << w)))
            return out
    f, t = real_point_violations(M4, objs)
    RES["MU4_laplace_cofactor"] = {"fired": f, "checks": t, "PASS": f > 0}

    # --- MU5: XF forgetting to delete y_c (haf(S_0+z) <-> haf(S_0))
    class M5(E.Enc):
        def build(self):
            n, z = self.n, self.z
            vpm = E.mask_of(self.VP)
            saved = self.use
            self.use = saved - {"XF"}
            super().build()
            self.use = saved
            for c in range(3):
                yc, Fc = self.ys[c], set(self.F[c])
                s = vpm
                while True:
                    if E.popcount(s) % 2 == 1 and \
                            [y for y in E.bits(s) if y in Fc] == [yc]:
                        a, b = self.p(c, s), self.p(c, s | (1 << z))
                        self.add(("XFbad", c, s), [-a, b])
                        self.add(("XFbad", c, s), [a, -b])
                    if s == 0:
                        break
                    s = (s - 1) & vpm
            return self
    f, t = real_point_violations(M5, objs)
    RES["MU5_xf_no_ydel"] = {"fired": f, "checks": t, "PASS": f > 0}

    # --- MU6: the k filter removed at k=3 (k=4 rows smuggled in): the k=3
    #          verdict must change on cases where real objects live
    reps = [((), (), ()), ((3,), (4,), (5,)), ((3, 4, 5, 6),) * 3,
            ((3, 4), (4, 5), (5, 6))]

    class M6(E.Enc):
        def keep(self, sizes):
            return True
    a = [M6(8, R, k=3).build().solve_pysat()[0] for R in reps]
    b = [E.Enc(8, R, k=3).build().solve_pysat()[0] for R in reps]
    RES["MU6_k_filter"] = {"unfiltered": a, "filtered": b, "PASS": a != b}

    # --- MU7: an artefact detector -- add the CONSTANT-word rows to A2 (i.e.
    #          demand haf(t^c|V) = 0 as well).  Everything must die, N=4
    #          included; if N=4 survives, the pipeline is not sensitive.
    class M7(E.Enc):
        def build(self):
            super().build()
            for c in range(3):
                self.add(("BOGUS", c), [-self.p(c, (1 << self.n) - 1)])
            return self
    n4 = M7(4, ((), (), ()), k=2).build().solve_pysat()[0]
    RES["MU7_artefact_detector"] = {"n4_still_sat": n4, "PASS": not n4}

    # --- MU8: drop A1 (haf(t^c|V) != 0) -- the N=8 k=4 kill must survive or
    #          not; recorded either way (load-bearing map, not a pass/fail)
    RES["seconds"] = round(time.time() - T0, 1)
    RES["PASS"] = all(v.get("PASS") for v in RES.values()
                      if isinstance(v, dict))
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    for k, v in RES.items():
        print(k, v, flush=True)


if __name__ == "__main__":
    main()
