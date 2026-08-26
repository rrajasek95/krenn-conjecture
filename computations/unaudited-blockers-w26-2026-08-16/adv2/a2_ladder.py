#!/usr/bin/env python3
"""adv2 -- THE SEPARABILITY LADDER.  UNAUDITED.  EXACT ONLY (Fraction).

Rung |T| = k:  vertices outside T are separable, so Phi depends only on
the T-letters and the only singles that can survive are those with BOTH
endpoints in T.  We look for  H_w = 0 at every mixed word  with z
supported on (and NONZERO on) the T-singles.

  k=3, T={1,2,6}    2 singles     (previous lane's record)
  k=3, other T                    -> secondary target S2 (R-vertex != 6)
  k=4, T={1,2,5,6}  3 singles     -> secondary target S1
  k=5..8                          -> towards the PRIMARY target (k=8)

SEED RECIPE (generic, replaces adv/'s hand tensor ansatz).  Let
T = {a,b,j} with a,b in L, j in R and (a,j),(b,j) both singles firing at
the SAME letter of j.  Every Gamma neighbour of j is separable, so
   Phi(tau) = N[tau_j] . V(tau_a, tau_b),
   N[c]_u = A_{ju}[c][.],   V_u = haf(Gamma - j - u).
Fix N[c] = mu_c * n on the two DEACTIVATING letters of j and
N[active] = cp*n + cc*mvec.  Then site-solving at vertex a for
"H = 0 at every representative word" is a homogeneous linear system whose
kernel is large precisely because the j-blocks were fixed degenerately.
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
import a2sep as SP                                                # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- separability ladder"}
RAN = []


def nbrs_gamma(sp, t):
    return sorted({u for e in sp.gam for u in e if t in e} - {t})


def set_vertex_j(sp, th, j, n, mvec, mu, cp, cc):
    """write the degenerate N-form into vertex j's Gamma blocks."""
    nb = nbrs_gamma(sp, j)
    assert len(nb) == len(n), (nb, n)
    # RUNG-LOCAL deactivating letters at j: only the T-singles matter,
    # because z vanishes on every other single.
    fires = {sp.sing[e][1 if e[1] == j else 0] for e in sp.tsing if j in e}
    dea = [c for c in range(3) if c not in fires]
    assert len(dea) == 2 and len(fires) == 1, (j, fires, dea)
    act = fires.pop()
    d0, d1 = dea
    N = {}
    N[d0] = [mu * x for x in n]
    N[d1] = list(n)
    N[act] = [cp * n[i] + cc * mvec[i] for i in range(len(n))]
    for i, u in enumerate(nb):
        e = (min(j, u), max(j, u))
        for c in range(3):
            k = (e, c if e[0] == j else -1, c if e[1] == j else -1)
            if k not in sp.pidx:              # u is in T: index not collapsed
                for dd in range(3):
                    k2 = (e, c if e[0] == j else dd, c if e[1] == j else dd)
                    th[sp.pidx[k2]] = N[c][i]
            else:
                th[sp.pidx[k]] = N[c][i]


def seed_rung3(m, a, b, j, rng, tries=40):
    """a rung-3 point for T = {a,b,j}."""
    S = [v for v in range(8) if v not in (a, b, j)]
    sp = SP.Sep(m, S)
    assert sorted(sp.tsing) == sorted([(min(a, j), max(a, j)),
                                       (min(b, j), max(b, j))]), sp.tsing
    nb = nbrs_gamma(sp, j)
    for _ in range(tries):
        th = sp.rand_theta(rng)
        n = [F(rng.randint(1, 5)) for _ in nb]
        mv = [F(rng.randint(-4, 4)) for _ in nb]
        set_vertex_j(sp, th, j, n, mv, F(rng.randint(2, 4)),
                     F(rng.randint(1, 3)), F(rng.randint(1, 3)))
        z = {e: F(0) for e in sp.tsing}
        ok = True
        for _p in range(6):
            for t in (a, b, a, b):
                if not sp.site_solve(th, z, t, rng):
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue
        if sp.defect(th, z) != 0:
            continue
        bl = sp.blocks(th)
        if not A.all_cells_nonzero(bl, A.Geo(m)):
            continue
        if A.on_stratum(m, bl):
            continue
        return sp, th, z, bl
    return None


def climb(sp0, th0, z0, m, Tnew, rng, passes=8, want=None):
    """embed a solution into the LARGER ansatz S' = V - Tnew and site-solve
    to switch on the new singles' z's."""
    Snew = [v for v in range(8) if v not in Tnew]
    sp = SP.Sep(m, Snew)
    bl = sp0.blocks(th0)
    th = [None] * len(sp.params)
    for k in sp.params:
        e, aa, bb = k
        i = 0 if aa == -1 else aa
        jj = 0 if bb == -1 else bb
        th[sp.pidx[k]] = bl[e][i][jj]
    z = {e: z0.get(e, F(0)) for e in sp.tsing}
    assert sp.defect(th, z) == 0, "embedded seed is not a solution"
    order = list(Tnew) + [v for v in range(8) if v not in Tnew]
    best = None
    for _p in range(passes):
        for t in order:
            sv = list(th), dict(z)
            if not sp.site_solve(th, z, t, rng):
                th, z = sv[0], dict(sv[1])
                continue
            if sp.defect(th, z) != 0:
                th, z = sv[0], dict(sv[1])
                continue
            bl2 = sp.blocks(th)
            if not A.all_cells_nonzero(bl2, A.Geo(m)):
                th, z = sv[0], dict(sv[1])
                continue
            nz = [e for e in sp.tsing if z[e] != 0]
            if best is None or len(nz) > len(best[2]):
                best = (list(th), dict(z), nz)
            if want and all(z[e] != 0 for e in want):
                return sp, list(th), dict(z), nz
    if best:
        return sp, best[0], best[1], best[2]
    return None


def analyse(m, bl, z, tag):
    rec = dict(tag=tag, m=m)
    rec["all_cells_nonzero"] = A.all_cells_nonzero(bl, A.Geo(m))
    rec["clean"] = A.is_clean(m, bl)
    rec["stratum"] = A.on_stratum(m, bl)
    rec["n_phi_nonzero"] = len(A.phi_support(m, bl))
    sv = {str(e): A.solo_verdict(m, bl, e) for e in A.Geo(m).live}
    rec["solo_survivors"] = sorted(k for k, v in sv.items() if v["survives"])
    rec["z_nonzero"] = sorted(str(e) for e in z if z[e] != 0)
    rec["z"] = {str(e): str(v) for e, v in z.items()}
    v = A.full_verdict(m, bl)
    rec["full_verdict"] = {k: v[k] for k in ("n_unknowns", "n_rows", "rank",
                                             "inconsistent", "killed")}
    # RAW re-verification straight from C.H_word
    T = C.TEMPLATES[m]
    zz = {e: z.get(e, F(0)) for e in C.single_edges(T)}
    bad = [w for w in C.MIXED if C.H_word(bl, T, zz, w) != 0]
    rec["raw_mixed_nonzero"] = len(bad)
    rec["raw_first_bad"] = list(bad[0]) if bad else None
    rec["raw_H_constants"] = [str(C.H_word(bl, T, zz, (c,) * 8))
                              for c in range(3)]
    rec["point"] = A.dump(bl)
    print("  %-34s clean=%s stratum=%s survivors=%s"
          % (tag, rec["clean"], rec["stratum"], rec["solo_survivors"]))
    print("       z nonzero on %s ; raw H!=0 at %d/6558 mixed words ; "
          "H(const)=%s" % (rec["z_nonzero"], len(bad), rec["raw_H_constants"]))
    return rec


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    rng = random.Random(4242 + m)
    OUT["m"] = m

    # ------------------------------------------------ rung 3, every choice
    print("=" * 74)
    print("RUNG 3 (|T|=3) at m=%d : every (a,b,j) with two singles into j" % m)
    print("=" * 74)
    RAN.append("rung3")
    rung3 = {}
    seeds = {}
    G = A.Geo(m)
    cands = []
    for j in (4, 5, 6, 7):
        Ls = [p for p in range(4) if (p, j) in G.live]
        for i1 in range(len(Ls)):
            for i2 in range(i1 + 1, len(Ls)):
                a, b = Ls[i1], Ls[i2]
                if G.sing[(a, j)][1] == G.sing[(b, j)][1]:
                    cands.append((a, b, j))
    print("  candidate T's: %s" % [str(c) for c in cands])
    for (a, b, j) in cands:
        r = seed_rung3(m, a, b, j, rng)
        key = "T={%d,%d,%d}" % (a, b, j)
        if r is None:
            print("  %-14s NO SEED" % key)
            rung3[key] = None
            continue
        sp, th, z, bl = r
        rec = analyse(m, bl, z, key)
        rung3[key] = {k: rec[k] for k in
                      ("clean", "stratum", "solo_survivors", "z_nonzero",
                       "raw_mixed_nonzero", "raw_H_constants",
                       "n_phi_nonzero", "full_verdict")}
        rung3[key]["point"] = rec["point"]
        rung3[key]["z"] = rec["z"]
        seeds[(a, b, j)] = (sp, th, z)
    OUT["rung3"] = rung3
    json.dump(OUT, open(os.path.join(HERE, "results_ladder_m%d.json" % m),
                        "w"), indent=1, default=str)
    print("  checkpointed.")

    # ------------------------------------------------------------- rung 4+
    print()
    print("=" * 74)
    print("CLIMBING: rung 4 and beyond")
    print("=" * 74)
    RAN.append("climb")
    climbs = {}
    plans = []
    if (1, 2, 6) in seeds:
        plans.append(((1, 2, 6), (1, 2, 5, 6), [(1, 5), (1, 6), (2, 6)]))
        plans.append(((1, 2, 6), (0, 1, 2, 6), [(0, 6), (1, 6), (2, 6)]))
        plans.append(((1, 2, 6), (1, 2, 6, 7), [(1, 6), (2, 6), (1, 7),
                                                (2, 7)]))
    if (0, 2, 4) in seeds:
        plans.append(((0, 2, 4), (0, 2, 3, 4), [(0, 4), (2, 4), (3, 4)]))
    for (base, Tnew, want) in plans:
        sp0, th0, z0 = seeds[base]
        key = "T=%s" % (Tnew,)
        r = climb(sp0, th0, z0, m, Tnew, rng, want=want)
        if r is None:
            print("  %-16s CLIMB FAILED" % key)
            climbs[key] = None
            continue
        sp, th, z, nz = r
        bl = sp.blocks(th)
        rec = analyse(m, bl, z, key)
        rec["target_singles"] = [str(e) for e in want]
        climbs[key] = {k: rec[k] for k in
                       ("clean", "stratum", "solo_survivors", "z_nonzero",
                        "raw_mixed_nonzero", "raw_H_constants",
                        "n_phi_nonzero", "full_verdict", "target_singles")}
        climbs[key]["point"] = rec["point"]
        climbs[key]["z"] = rec["z"]
        OUT["climb"] = climbs
        json.dump(OUT, open(os.path.join(HERE,
                                         "results_ladder_m%d.json" % m), "w"),
                  indent=1, default=str)
    OUT["climb"] = climbs

    declared = ["rung3", "climb"]
    missing = [d for d in declared if d not in RAN]
    print("\nCONTROL MANIFEST declared=%s ran=%s" % (declared, RAN))
    assert not missing, "CONTROL DID NOT RUN: %s" % missing
    OUT["control_manifest"] = dict(declared=declared, ran=RAN)
    json.dump(OUT, open(os.path.join(HERE, "results_ladder_m%d.json" % m),
                        "w"), indent=1, default=str)
    print("wrote results_ladder_m%d.json" % m)


if __name__ == "__main__":
    main()
