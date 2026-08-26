#!/usr/bin/env python3
"""A11 -- the (beta)-escape, fully reduced, and the exact distance to it at
the live round-10 points.  UNAUDITED.

HAND DERIVATION (each identity it uses is machine-checked in results_t1/t4).
Let the escape hold on a word set that (i) covers, at a fixed x1, all three
y4 for each y5 and each y7, and (ii) contains, for some fixed (x0,x1,x3), two
values of x2, and for some fixed (x1,x2,x3), two values of x0.  Write
A45 = v (x) a, A47 = v (x) b, A14[x1][.] = c*v (target 3(a)).  The pinning
becomes, for every escaped word,

    hafL(x) * a[y5]  =  -c * A03[x0][x3] * A25[x2][y5]           (E1)
    hafL(x) * b[y7]  =  -c * A23[x2][x3] * A07[x0][y7]           (E2)

Dividing (E1) at two y5 values (legal: every cell is nonzero and a[.] != 0
because A45's cells are nonzero) gives a[u]/a[w] = A25[x2][u]/A25[x2][w] for
every reached x2, i.e. every 2x2 minor of A25 vanishes: **A25 is rank one**.
(E2) gives **A07 rank one** the same way.  And the right-hand sides of (E1)
and (E2) do not contain x1, so **hafL(x) is independent of x1** on the
escaped L-parts.  Eliminating hafL between (E1) and (E2) returns round 8's
(CELL) binomial in factored form.

So the escape needs SEVEN things, not two.  This file measures each of them
at the live round-10 build points, which is the exact answer to "how far has
the adversarial side got".
"""
from __future__ import annotations

import json
import os
import sys
import time
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W30 = os.path.join(os.path.dirname(HERE), "unaudited-exclusion-w30-2026-08-19")
sys.path.insert(0, HERE)
import a11_lib as A      # noqa: E402
import a11_m25 as M      # noqa: E402

DECL = ["R1_requirement_census", "R2_control_requirements_are_independent"]

REQ = ["A45 rank one", "A47 rank one", "A14 rank one",
       "A45/A47 share the column direction", "A25 rank one", "A07 rank one",
       "hafL independent of x1", "the scalar system (E1)/(E2) itself"]


def main():
    t0 = time.time()
    man = A.Manifest(DECL)
    tm = A.T(25)
    unt_t = M.untriggered_template(25, 6)
    out = {}
    for fn, fld in (("results_r10_beta_13.json", 13),
                    ("results_r10_beta_31.json", 31),
                    ("results_r10_beta_Q.json", 0),
                    ("results_r10_alpha_13.json", 13),
                    ("results_r10_alpha_Q.json", 0)):
        path = os.path.join(W30, fn)
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        if not d.get("best"):
            continue
        K = A.Rat if fld == 0 else A.Modp(fld)
        bl = A.load_point(d["best"]["point"], K)
        cols45 = [[bl[(4, 5)][y4][y5] for y4 in range(3)] for y5 in range(3)]
        cols47 = [[bl[(4, 7)][y4][y7] for y4 in range(3)] for y7 in range(3)]
        x1dep = 0
        for x0, x2, x3 in product(range(3), repeat=3):
            vals = {str(A.hafL(tm, bl, (x0, x1, x2, x3, 0, 0, 0, 0), K))
                    for x1 in range(3)}
            if len(vals) > 1:
                x1dep += 1
        # the scalar system, over the point-level untriggered set
        phi = {w: A.phi_gpm(tm, bl, w, K) for w in A.WORDS}
        other = [u for u in range(8) if u != 6]
        nB = nC = nQ = ntot = 0
        for vals in product(range(3), repeat=7):
            w = [0] * 8
            for u, aa in zip(other, vals):
                w[u] = aa
            if not all(K.iszero(phi[tuple(w[:6] + [t] + w[7:])])
                       for t in range(3)):
                continue
            ntot += 1
            B, C = M.BC_closed(tm, bl, tuple(w), K)
            nB += 1 if K.iszero(B) else 0
            nC += 1 if K.iszero(C) else 0
            nQ += 1 if (K.iszero(B) and K.iszero(C)) else 0
        out[fn] = dict(
            rank_A45=A.rank(bl[(4, 5)], K), rank_A47=A.rank(bl[(4, 7)], K),
            rank_A14=A.rank(bl[(1, 4)], K), rank_A25=A.rank(bl[(2, 5)], K),
            rank_A07=A.rank(bl[(0, 7)], K), rank_A03=A.rank(bl[(0, 3)], K),
            rank_A23=A.rank(bl[(2, 3)], K),
            common_direction=(A.rank(cols45 + cols47, K) == 1),
            hafL_x1_dependent_triples=x1dep, n_x_triples=27,
            n_untriggered_point=ntot, n_B_zero=nB, n_C_zero=nC, n_Q_zero=nQ,
            n_Q_zero_template=sum(
                1 for w in unt_t
                if all(K.iszero(z) for z in M.BC_closed(tm, bl, w, K))),
            requirements_met=dict(
                A45_rank_one=(A.rank(bl[(4, 5)], K) == 1),
                A47_rank_one=(A.rank(bl[(4, 7)], K) == 1),
                A14_rank_one=(A.rank(bl[(1, 4)], K) == 1),
                common_direction=(A.rank(cols45 + cols47, K) == 1),
                A25_rank_one=(A.rank(bl[(2, 5)], K) == 1),
                A07_rank_one=(A.rank(bl[(0, 7)], K) == 1),
                hafL_free_of_x1=(x1dep == 0),
                scalar_system=(nQ == ntot and ntot > 0)))
        print("[%s] %s" % (fn, out[fn]['requirements_met']), flush=True)
        print("    Q=0 at %d of %d point-level untriggered words"
              % (out[fn]['n_Q_zero'], out[fn]['n_untriggered_point']),
              flush=True)
    man.record("R1_requirement_census", dict(
        requirements=REQ, per_point=out, ok=True,
        note="the escape needs ALL of these; the round-10 target names only "
             "the first four"))
    # control: the requirements are not all equivalent -- at least one point
    # must meet some and miss others, else the census would be vacuous
    mixed = [fn for fn, r in out.items()
             if 0 < sum(1 for v in r['requirements_met'].values() if v)
             < len(r['requirements_met'])]
    man.record("R2_control_requirements_are_independent", dict(
        points_meeting_some_but_not_all=mixed, ok=len(mixed) > 0,
        note="if every point met all or none, the decomposition would carry "
             "no information"))
    man.finish(os.path.join(HERE, "results_t9.json"),
               extra={"_header": "UNAUDITED A11: the (beta) escape reduced to "
                                 "seven requirements, measured at the live "
                                 "round-10 points",
                      "elapsed_s": round(time.time() - t0, 1)})
    print("T9 DONE in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
