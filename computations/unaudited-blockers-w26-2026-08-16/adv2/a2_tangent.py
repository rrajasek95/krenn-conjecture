#!/usr/bin/env python3
"""adv2 -- TANGENT-SPACE SURVEY of the solution variety
      W = { (Gamma blocks, z) : H_w = 0 for all 6558 mixed words }.

UNAUDITED.  Points are EXACT rationals; the tangent computation is exact
integer linear algebra mod a large prime (a mod-p kernel can only be
BIGGER, so a coordinate that is dead mod p is dead over Q as well).

Two families of base points:
  (A) the STRATUM points  (Phi == 0 identically, every Gamma cell
      nonzero, z = 0).  These are the most singular points of W -- every
      branch of W that reaches "all singles switched on" has to pass
      near one -- so the set of z's that are LIVE in the tangent space
      there upper-bounds what any first-order deformation can switch on.
  (B) the solutions produced by the refinement climb.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import a2jac as J                                                 # noqa: E402
import a2seed as SD                                               # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- tangent-space survey"}


def stratum_point(m, a, b, j, rng, tries=25):
    """a clean point with Phi == 0 identically and all Gamma cells != 0:
    take the seed-3 construction and set cc = 0, i.e. ALL THREE rows of
    vertex j's blocks proportional to the same n with n.V == 0."""
    r = SD.seed3(m, a, b, j, rng, tries=tries)
    if r is None:
        return None
    sp, th, z, bl, info = r
    n = [F(x) for x in info["n"]]
    nbj = info["nbj"]
    mu, cp = F(info["mu"]), F(info["cp"])
    for i, u in enumerate(nbj):
        e = (min(j, u), max(j, u))
        for c in range(3):
            fac = {0: mu, 1: F(1), 2: cp}[c] if False else None
        for c in range(3):
            fac = [mu, F(1), cp][c]
            for d in range(3):
                k = (e, c if e[0] == j else (-1 if u in sp.S else d),
                     c if e[1] == j else (-1 if u in sp.S else d))
                if k in sp.pidx:
                    th[sp.pidx[k]] = fac * n[i]
    bl2 = sp.blocks(th)
    if not A.all_cells_nonzero(bl2, A.Geo(m)):
        return None
    if not A.on_stratum(m, bl2):
        return None
    return bl2


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    rng = random.Random(999 + m)
    OUT["m"] = m
    fn = os.path.join(HERE, "results_tangent_m%d.json" % m)
    recs = []

    print("=" * 74)
    print("(A) STRATUM base points at m=%d (Phi == 0, all cells != 0, z=0)"
          % m)
    print("=" * 74)
    G = A.Geo(m)
    cands = []
    for j in (4, 5, 6, 7):
        Ls = [p for p in range(4) if (p, j) in G.live]
        for i1 in range(len(Ls)):
            for i2 in range(i1 + 1, len(Ls)):
                if G.sing[(Ls[i1], j)][1] == G.sing[(Ls[i2], j)][1]:
                    cands.append((Ls[i1], Ls[i2], j))
    for (a, b, j) in cands:
        for rep in range(2):
            bl = stratum_point(m, a, b, j, rng)
            if bl is None:
                print("  (a,b,j)=(%d,%d,%d) rep%d: no stratum point"
                      % (a, b, j, rep))
                continue
            z0 = {e: F(0) for e in G.live}
            # sanity: H_w == 0 at every mixed word, from the raw definition
            T = C.TEMPLATES[m]
            zz = {e: F(0) for e in C.single_edges(T)}
            nbad = sum(1 for w in C.MIXED if C.H_word(bl, T, zz, w) != 0)
            t = J.tangent(m, bl, z0, 10007, sample=500,
                          rng=random.Random(5))
            t2 = J.tangent(m, bl, z0, 100003, sample=500,
                           rng=random.Random(5))
            print("  (a,b,j)=(%d,%d,%d) rep%d  rawH!=0 at %d words ; "
                  "ker=%d/%d ; z LIVE = %s"
                  % (a, b, j, rep, nbad, t["ker_dim"], t["n_unknowns"],
                     t["z_live"]))
            if sorted(t["z_live"]) != sorted(t2["z_live"]):
                print("      (p-dependence! p=100003 gives %s)"
                      % t2["z_live"])
            recs.append(dict(kind="stratum", abj=[a, b, j], rep=rep,
                             raw_mixed_nonzero=nbad, tangent=t,
                             tangent_p2=t2, point=A.dump(bl)))
            OUT["records"] = recs
            json.dump(OUT, open(fn, "w"), indent=1, default=str)

    print()
    print("=" * 74)
    print("(B) climb solutions")
    print("=" * 74)
    for f in sorted(os.listdir(HERE)):
        if not f.startswith("results_climb_m%d" % m):
            continue
        d = json.load(open(os.path.join(HERE, f)))
        for r in d.get("rungs", []):
            if not r.get("point") or not r.get("z"):
                continue
            bl = A.load(r["point"])
            z = {tuple(int(t) for t in k.strip("()").split(",")): F(v)
                 for k, v in r["z"].items()}
            t = J.tangent(m, bl, z, 10007, sample=500,
                          rng=random.Random(5))
            print("  %-28s z!=0 %s ; ker=%d ; z LIVE = %s"
                  % (r["step"], r["z_nonzero"], t["ker_dim"], t["z_live"]))
            recs.append(dict(kind="climb", file=f, step=r["step"],
                             z_nonzero=r["z_nonzero"], tangent=t))
    OUT["records"] = recs
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print("\nwrote %s" % fn)


if __name__ == "__main__":
    main()
