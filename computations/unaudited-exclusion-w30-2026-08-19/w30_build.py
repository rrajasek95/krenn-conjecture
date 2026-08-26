#!/usr/bin/env python3
"""W30 ADVERSARIAL BUILDER (ledger 20).  UNAUDITED.  EXACT ONLY.

TARGET: construct a clean point, OFF the vanishing stratum, with every Gamma
cell nonzero, at which BOTH L2 and R5 fail (and separately L2 and R6) --
i.e. REFUTE the residual exclusion W26 left open.

THE LEVER.  Every R-vertex's master relation carries the scale hafL(x); the
index choice is discarded when hafL(x) = 0 (w26_disj.analyse: `if h==0:
nzero_scale+=1; continue`).  So

    hafL == 0 identically  ==>  ALL FOUR R-vertices fail (vacuously),
    hafR == 0 identically  ==>  ALL FOUR L-vertices fail (vacuously),
    both                   ==>  the DISJUNCTION itself is refuted.

hafL(x) = l01 l23 + l02 l13 + l03 l12 is linear in each L-L block, so the
rank-one ansatz  A_ij[a][b] = u_i(a) u_j(b) c_ij  gives
hafL = (prod_a u_a(x_a)) * (c01c23 + c02c13 + c03c12); pick the c's with
hafnian 0 and hafL vanishes identically with every cell nonzero.
Phi = haf_Gamma is MULTILINEAR in the blocks, and the blocks incident to a
single vertex t never co-occur in a matching, so w26_fast.site_solve at
t in R re-solves ONLY R-R and sigma blocks -- hafL == 0 is preserved.

CONTROLS
  B1 positive control: the same descent with UNCONSTRAINED L-blocks must
     still produce clean points (else the pipeline is broken).
  B2 the constructed object is re-verified by an INDEPENDENT route:
     C.H_word over all 105 matchings at every mixed word.
  B3 mutation: perturb one cell of a hit; cleanliness must break.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w26_core as C                                              # noqa: E402
import w26_fast as FA                                             # noqa: E402

F = Fraction
RES = os.path.join(HERE, "results_build.json")
OUT = {"_header": "UNAUDITED W30 adversarial builder (hafL/hafR annihilation)",
       "_controls_declared": ["B1_positive_control", "B2_independent_verify",
                              "B3_mutation"],
       "_controls_run": []}


def ck():
    json.dump(OUT, open(RES, "w"), indent=1, default=str)


HAFZERO_C = {(0, 1): 1, (2, 3): 1, (0, 2): 1, (1, 3): 1,
             (0, 3): 1, (1, 2): -2}          # 1*1 + 1*1 + 1*(-2) = 0


def hafzero_L(rng, lo=-6, hi=6):
    """6 L-L blocks with hafL == 0 identically and all cells nonzero."""
    u = {}
    for a in range(4):
        u[a] = [F(rng.randint(lo, hi) or 3, rng.randint(1, 3))
                for _ in range(3)]
    bl = {}
    for i, j in combinations(range(4), 2):
        c = F(HAFZERO_C[(i, j)])
        bl[(i, j)] = [[u[i][a] * u[j][b] * c for b in range(3)]
                      for a in range(3)]
    return bl


def hafzero_R(m, rng, lo=-6, hi=6):
    """R-R blocks with hafR == 0 identically and all cells nonzero.
    hafR = r45 r67 + r46 r57 + r47 r56 over the PRESENT R-edges."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    red = [e for e in gs if e[0] >= 4]
    v = {}
    for a in range(4, 8):
        v[a] = [F(rng.randint(lo, hi) or 3, rng.randint(1, 3))
                for _ in range(3)]
    # constants on the three pairings of {4,5,6,7}
    pair = [((4, 5), (6, 7)), ((4, 6), (5, 7)), ((4, 7), (5, 6))]
    present = [all(e in gs for e in pr) for pr in pair]
    cc = {}
    if sum(present) == 2:
        i0, i1 = [k for k in range(3) if present[k]]
        for e in pair[i0]:
            cc[e] = F(1)
        cc[pair[i1][0]] = F(1)
        cc[pair[i1][1]] = F(-1)
    elif sum(present) == 3:
        cc[(4, 5)] = cc[(6, 7)] = F(1)
        cc[(4, 6)] = cc[(5, 7)] = F(1)
        cc[(4, 7)] = F(1)
        cc[(5, 6)] = F(-2)
    else:
        return None
    bl = {}
    for e in red:
        bl[e] = [[v[e[0]][a] * v[e[1]][b] * cc[e] for b in range(3)]
                 for a in range(3)]
    return bl


def rand_block(rng, lo=-6, hi=6):
    return [[F(rng.randint(lo, hi) or 3, rng.randint(1, 3))
             for _ in range(3)] for _ in range(3)]


def haf_all_zero(m, bl, side):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))

    def cl(u, v, a, b):
        e = (u, v) if u < v else (v, u)
        if e not in gs:
            return F(0)
        return bl[e][a][b] if u < v else bl[e][b][a]
    if side == 'L':
        for x in product(range(3), repeat=4):
            ll = {(a, b): cl(a, b, x[a], x[b])
                  for a, b in combinations(range(4), 2)}
            if (ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
                    + ll[(0, 3)] * ll[(1, 2)]) != 0:
                return False
        return True
    for y in product(range(3), repeat=4):
        def r(a, b):
            return cl(a, b, y[a - 4], y[b - 4])
        if r(4, 5) * r(6, 7) + r(4, 6) * r(5, 7) + r(4, 7) * r(5, 6) != 0:
            return False
    return True


def try_build(m, seed, mode, passes=6):
    """mode in {'L0','R0','BOTH','FREE'}: which hafnian is annihilated."""
    rng = random.Random(seed)
    mdl = FA.Model(m)
    gam = mdl.gam
    bl = {e: rand_block(rng) for e in gam}
    if mode in ('L0', 'BOTH'):
        for e, v in hafzero_L(rng).items():
            bl[e] = v
    if mode in ('R0', 'BOTH'):
        hz = hafzero_R(m, rng)
        if hz is None:
            return None
        for e, v in hz.items():
            bl[e] = v
    # which sites may be re-solved without destroying the annihilated side?
    if mode == 'L0':
        sites = [4, 5, 6, 7]
    elif mode == 'R0':
        sites = [0, 1, 2, 3]
    elif mode == 'FREE':
        sites = [0, 1, 2, 3, 4, 5, 6, 7]
    else:
        sites = []
    for _ in range(passes):
        order = list(sites)
        rng.shuffle(order)
        for t in order:
            FA.site_solve(mdl, bl, t, rng)
        if mdl.clean_ok(bl) and mdl.allnz(bl):
            break
    if mode == 'BOTH':
        # only the four sigma blocks are free; Phi is linear (inhomogeneous)
        # in each one separately.
        for _ in range(passes * 4):
            ok = solve_sigma(mdl, bl, rng)
            if not ok:
                break
            if mdl.clean_ok(bl):
                break
    if not (mdl.clean_ok(bl) and mdl.allnz(bl)):
        return None
    return bl


def solve_sigma(mdl, bl, rng):
    """inhomogeneous exact solve of ONE sigma block from the clean words."""
    gs = mdl.gs
    sig = [(p, C.SIG[p]) for p in range(4) if (p, C.SIG[p]) in gs]
    if not sig:
        return False
    e = sig[rng.randrange(len(sig))]
    rows, rhs = [], []
    for w in mdl.clean:
        r = [F(0)] * 9
        rest = tuple(v for v in range(8) if v not in e)
        c = C.haf_on(bl, gs, rest, w)
        r[3 * w[e[0]] + w[e[1]]] = c
        # constant part: Phi with this block zeroed
        save = [rr[:] for rr in bl[e]]
        bl[e] = [[F(0)] * 3 for _ in range(3)]
        const = C.haf_on(bl, gs, tuple(range(8)), w)
        bl[e] = save
        if any(r) or const != 0:
            rows.append(r)
            rhs.append(-const)
    aug = [rows[i] + [rhs[i]] for i in range(len(rows))]
    Rw, piv = C.rref(aug, 10)
    if 9 in piv:
        return False
    sol = [F(0)] * 9
    for i, pc in enumerate(piv):
        if pc < 9:
            sol[pc] = Rw[i][9]
    ker = C.kernel_basis(rows, 9)
    for _ in range(400):
        v = list(sol)
        for b in ker:
            co = F(rng.randint(-5, 5))
            v = [a + co * bb for a, bb in zip(v, b)]
        if all(z != 0 for z in v):
            bl[e] = [[v[3 * i + j] for j in range(3)] for i in range(3)]
            return True
    return False


def verify(m, bl):
    """B2: independent verification via C.H_word over all 105 matchings."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    z = {e: F(0) for e in C.single_edges(C.TEMPLATES[m])}
    bad = 0
    for w in C.clean_words(m):
        if C.H_word(bl, C.TEMPLATES[m], z, w) != 0:
            bad += 1
    nonvan = sum(1 for w in C.WORDS
                 if C.phi(bl, gs, w) != 0)
    return dict(clean_violations=bad, n_words_phi_nonzero=nonvan)


def report(m, bl, tag):
    rec = L.full_report(m, bl)
    rec2 = dict(m=m, tag=tag,
                fails=rec['fails'],
                disj=rec['DISJUNCTION_holds'],
                nidx={l: rec[l]['n_idx'] for l in L.VERTS},
                nzero={l: rec[l]['n_zero_scale'] for l in L.VERTS},
                ndel={l: rec[l]['n_deliver'] for l in L.VERTS},
                hafL_zero=haf_all_zero(m, bl, 'L'),
                hafR_zero=haf_all_zero(m, bl, 'R'),
                allnz=L.all_cells_nonzero(m, bl))
    rec2.update(verify(m, bl))
    rec2['vanishing_stratum'] = (rec2['n_words_phi_nonzero'] == 0)
    return rec2


def main():
    t0 = time.time()
    modes = sys.argv[1].split(",") if len(sys.argv) > 1 else \
        ["FREE", "L0", "R0", "BOTH"]
    ms = [int(z) for z in sys.argv[2].split(",")] if len(sys.argv) > 2 else \
        [25, 26, 27, 28]
    ntry = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    OUT["hits"] = []
    OUT["summary"] = {}
    for mode in modes:
        for m in ms:
            hits = 0
            tried = 0
            for s in range(ntry):
                tried += 1
                try:
                    bl = try_build(m, 77_000_000 + 1000 * m + s, mode)
                except Exception as ex:                      # noqa: BLE001
                    print("  EXC", mode, m, s, ex, flush=True)
                    continue
                if bl is None:
                    continue
                r = report(m, bl, "%s_m%d_s%d" % (mode, m, s))
                r['point'] = {str(k): [[str(z) for z in row] for row in v]
                              for k, v in bl.items()}
                hits += 1
                OUT["hits"].append(r)
                print("HIT %-5s m=%d s=%-3d hafL0=%-5s hafR0=%-5s van=%-5s "
                      "allnz=%-5s fails=%s"
                      % (mode, m, s, r['hafL_zero'], r['hafR_zero'],
                         r['vanishing_stratum'], r['allnz'],
                         ",".join(r['fails']) or "-"), flush=True)
                ck()
                if hits >= 6:
                    break
            OUT["summary"]["%s_m%d" % (mode, m)] = dict(tried=tried,
                                                        hits=hits)
            print("== %-5s m=%d : %d hits / %d tries  (%.0fs)"
                  % (mode, m, hits, tried, time.time() - t0), flush=True)
            ck()
    # ---- controls
    pos = [k for k, v in OUT["summary"].items()
           if k.startswith("FREE") and v["hits"] > 0]
    OUT["B1_positive_control"] = dict(free_modes_with_hits=pos,
                                      ok=len(pos) > 0)
    OUT["_controls_run"].append("B1_positive_control")
    OUT["B2_independent_verify"] = dict(
        n=len(OUT["hits"]),
        all_clean_by_H_word=all(h['clean_violations'] == 0
                                for h in OUT["hits"]),
        ok=all(h['clean_violations'] == 0 for h in OUT["hits"]))
    OUT["_controls_run"].append("B2_independent_verify")
    mut = []
    for h in OUT["hits"][:4]:
        m = h['m']
        bl = {eval(k): [[F(z) for z in row] for row in v]
              for k, v in h['point'].items()}
        gam = list(C.gamma_edges(C.TEMPLATES[m]))
        e = gam[0]
        bl[e][0][0] += F(1)
        v = verify(m, bl)
        mut.append(dict(tag=h['tag'], edge=str(e),
                        clean_violations_after=v['clean_violations']))
    OUT["B3_mutation"] = dict(records=mut,
                              ok=all(x['clean_violations_after'] > 0
                                     for x in mut) if mut else None)
    OUT["_controls_run"].append("B3_mutation")
    missing = [c for c in OUT["_controls_declared"]
               if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["_manifest_missing"] = missing
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("MANIFEST OK %s   DONE %.0fs" % (OUT["_controls_run"],
                                           time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
