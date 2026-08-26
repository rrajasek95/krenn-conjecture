#!/usr/bin/env python3
"""Does the refutation survive when Laplace expansion is only ever at the HEAD?

WHY THIS MATTERS
----------------
In Lean, `haf W c L` is defined on a LIST, and `haf_cons` gives the Laplace
expansion at the list's HEAD only. Expanding at an arbitrary interior site `w`
needs the hafnian to be invariant under permuting `L`, which is FALSE for a
general `WeightsN` (the registry's `W` need not satisfy
`W (u,v,i,j) = W (v,u,j,i)`) and would therefore cost a symmetrization layer
plus a symmetric-function induction: the expensive half of risk 2.

Two clause families expand: A3 (at every `w in S`) and XF (at the solve site
`z`). Both become head expansions if

  * A3 is restricted to `w = min S`, and
  * the solve site is `z = 0` rather than `z = n - 1`,

since every set is carried as a sorted list. Restricting A3 only REMOVES
clauses, so UNSAT under the restriction still implies UNSAT of the full system
-- the abstraction stays a relaxation and soundness is untouched. The question
is purely whether enough refutational strength survives.

Run: python3 head_laplace_probe.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/rishi/workplace/krenn-conjecture"
PKG = f"{ROOT}/computations/unaudited-promotion-diag-2026-08-20/certified_package"
CAD = f"{ROOT}/computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical"
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "encoders"))
sys.path.insert(0, PKG)
import a9_enc as A  # noqa: E402
import l1_enc as L1  # noqa: E402
import orbit_ledger as LED  # noqa: E402


class HeadEnc(L1.CanonEnc):
    """Canonical encoder with A3 restricted to the least element of each set."""

    def build(self):
        evens = L1.even_masks(self.n)
        self.even_masks = evens
        self.rank = {m: i for i, m in enumerate(evens)}
        for c in range(3):
            for m in evens:
                self.p(c, m)
        self.n_base = self.nv
        # replicate a9_enc.Enc.build, but A3 only at w = min(S)
        n, V, z, VP = self.n, self.V, self.z, self.VP
        full = (1 << n) - 1
        for c in range(3):
            self.add(("A0", c), [self.p(c, 0)])
            self.add(("A1", c), [self.p(c, full)])
        for c in range(3):
            for m in evens:
                if A.popcount(m) < 4:
                    continue
                el = A.bits(m)
                for w in [min(el)]:                      # <-- head only
                    big = [-self.p(c, m)]
                    for u in el:
                        if u == w:
                            continue
                        gv = self.g(c, m, w, u)
                        self.add(("A3g", c, m, w, u),
                                 [-gv, self.p(c, (1 << w) | (1 << u))])
                        self.add(("A3g", c, m, w, u),
                                 [-gv, self.p(c, m & ~((1 << w) | (1 << u)))])
                        big.append(gv)
                    self.add(("A3", c, m, w), big)
        # A2, C0, Cnz, Ch, FR, XF: identical to the audit encoder
        saved_use = self.use
        self.use = {"A2", "C0", "Cnz", "Ch", "FR", "XF"}
        A.Enc.build(self)
        self.use = saved_use
        return self


def solve(enc):
    d = tempfile.mkdtemp()
    cnf = os.path.join(d, "c.cnf")
    with open(cnf, "w") as f:
        f.write(enc.dimacs())
    r = subprocess.run([CAD, cnf, "--no-binary"], capture_output=True, text=True)
    os.unlink(cnf)
    return {10: "SAT", 20: "UNSAT"}.get(r.returncode, f"rc{r.returncode}")


def sweep(n, z, ys, label):
    reps = [t for t, _ in LED.orbit_reps(n)]
    # the ledger's Q is V' - {y0,y1,y2}; re-map a rep's site labels to the
    # actual Q for this (z, ys) choice
    VP = [x for x in range(n) if x != z]
    Q = [x for x in VP if x not in ys]
    Qold = [x for x in range(3, n - 1)]
    ren = dict(zip(Qold, Q))
    bad = []
    for i, Rs in enumerate(reps):
        Rs2 = tuple(tuple(sorted(ren[q] for q in R)) for R in Rs)
        e = HeadEnc(n, Rs2, k=4, z=z, ys=ys).build()
        v = solve(e)
        if v != "UNSAT":
            bad.append((i, Rs2, v))
    print(f"{label}: {len(reps)-len(bad)}/{len(reps)} UNSAT"
          + (f"  NOT-UNSAT: {bad[:5]}" if bad else "  ALL UNSAT"), flush=True)
    return not bad


if __name__ == "__main__":
    ok6 = sweep(6, 0, (1, 2, 3), "N=6 head-only A3, z=0, 13 orbits")
    ok8 = sweep(8, 0, (1, 2, 3), "N=8 head-only A3, z=0, 87 orbits")
    print("VERDICT:", "head-Laplace SUFFICES" if (ok6 and ok8)
          else "head-Laplace INSUFFICIENT -- permutation invariance needed")
