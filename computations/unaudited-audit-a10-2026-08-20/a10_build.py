#!/usr/bin/env python3
"""A10 -- an INDEPENDENT clean-point builder + adversarial control.

UNAUDITED AUDIT LANE.  Exact only (F_p).  Own construction, own engine.

Construction.  Phi = haf_Gamma is LINEAR in the cells of the blocks at any
single site t:  Phi(w) = sum_{s in N(t)} A_{t,s}[w_t][w_s] * Q_s(w), with
Q_s(w) = haf_{Gamma - {t,s}}(w) free of site t.  So for each letter a the
clean-word constraints at site t are a homogeneous linear system in the
3*deg(t) unknowns A_{t,s}[a][.].  Seeding with a rank-one point (which is
exactly Phi = 0 everywhere once the scalar hafnian vanishes) puts a known
vector in each kernel; re-solving site by site with RANDOM kernel elements
walks the clean variety and generically leaves the vanishing stratum.

Ledger 20 (adversarial builder): the sole purpose of this lane is to BUILD
the object Theorem W30-X/W30-Y forbids -- a clean, off-stratum, all-cells-
nonzero point at which a PROTECTED vertex FAILS.  A failed search is not
evidence (ledger 18) and is reported as such.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a10_lib as A                                                # noqa: E402

RES = os.path.join(HERE, "results_build.json")
DECL = ["B1_construction_valid", "B2_adversarial_protected",
        "B3_mutation", "B4_offstratum_reached"]
OUT = {"_header": "UNAUDITED A10 independent clean-point builder",
       "_controls_declared": DECL, "_controls_run": []}
PROTECTED = {25: ['R6'], 26: ['R5', 'R6'], 27: ['R5'], 28: []}


def ck():
    json.dump(OUT, open(RES, "w"), indent=1, default=str)


def nullspace(M, p):
    """basis of the right kernel of M over F_p (rows = equations)."""
    if not M:
        return None
    nc = len(M[0])
    R = [[x % p for x in r] for r in M]
    piv = []
    r = 0
    for c in range(nc):
        s = None
        for i in range(r, len(R)):
            if R[i][c] % p:
                s = i
                break
        if s is None:
            continue
        R[r], R[s] = R[s], R[r]
        iv = pow(R[r][c], p - 2, p)
        R[r] = [(x * iv) % p for x in R[r]]
        for i in range(len(R)):
            if i != r and R[i][c] % p:
                f = R[i][c]
                R[i] = [(a - f * b) % p for a, b in zip(R[i], R[r])]
        piv.append(c)
        r += 1
        if r == len(R):
            break
    free = [c for c in range(nc) if c not in piv]
    out = []
    for f in free:
        v = [0] * nc
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-R[i][f]) % p
        out.append(v)
    return out


def seed(m, rng, p):
    """rank-one seed with a vanishing scalar hafnian -> Phi == 0."""
    st = A.S(m)
    gam = list(st.gamma)
    phi = {u: [rng.randrange(1, p) for _ in range(3)] for u in range(8)}
    for _ in range(60):
        c = {e: rng.randrange(1, p) for e in gam}
        e0 = gam[rng.randrange(len(gam))]
        # haf is linear in c[e0]:  haf = c[e0]*Aco + B
        c[e0] = 0
        B = hafC(st, c, p)
        c[e0] = 1
        Aco = (hafC(st, c, p) - B) % p
        if Aco % p == 0:
            continue
        c[e0] = (-B * pow(Aco, p - 2, p)) % p
        if c[e0] == 0:
            continue
        bl = {e: [[(c[e] * phi[e[0]][a] * phi[e[1]][b]) % p
                   for b in range(3)] for a in range(3)] for e in gam}
        return bl
    return None


def hafC(st, c, p):
    tot = 0
    for M in st.gamma_pms:
        pr = 1
        for e in M:
            pr = (pr * c[e]) % p
        tot = (tot + pr) % p
    return tot


def site_solve(m, bl, t, rng, p):
    """re-solve the blocks at site t on a random kernel element."""
    st = A.S(m)
    K = A.Fp(p)
    ns = sorted(s for s in range(8) if (min(s, t), max(s, t)) in st.gs)
    # Q_s(w) for every clean word (independent of site t's blocks)
    for a in range(3):
        rows = []
        for w in st.clean:
            if w[t] != a:
                continue
            row = [0] * (3 * len(ns))
            for j, s in enumerate(ns):
                rest = tuple(z for z in range(8) if z not in (t, s))
                q = 0
                for M in A._perfect_matchings(rest):
                    pr = 1
                    for (u, v) in M:
                        e = (u, v) if u < v else (v, u)
                        if e not in st.gs:
                            pr = 0
                            break
                        pr = (pr * bl[e][w[e[0]]][w[e[1]]]) % p
                        if pr == 0:
                            break
                    q = (q + pr) % p
                row[3 * j + w[s]] = (row[3 * j + w[s]] + q) % p
            rows.append(row)
        ker = nullspace(rows, p) if rows else None
        if not ker:
            continue
        got = None
        for _ in range(40):
            co = [rng.randrange(p) for _ in ker]
            v = [sum(co[i] * ker[i][j] for i in range(len(ker))) % p
                 for j in range(3 * len(ns))]
            if all(x % p for x in v):
                got = v
                break
        if got is None:
            continue
        for j, s in enumerate(ns):
            e = (min(t, s), max(t, s))
            for b in range(3):
                if e[0] == t:
                    bl[e][a][b] = got[3 * j + b]
                else:
                    bl[e][b][a] = got[3 * j + b]
    return bl


def build(m, p, rng, passes=3):
    bl = seed(m, rng, p)
    if bl is None:
        return None
    K = A.Fp(p)
    order = list(range(8))
    for _ in range(passes):
        rng.shuffle(order)
        for t in order:
            site_solve(m, bl, t, rng, p)
    okc, _ = A.is_clean_point(m, bl, K)
    if not okc:
        return None
    if not A.all_gamma_cells_nonzero(m, bl, K):
        return None
    nz = A.n_words_phi_nonzero(m, bl, K)
    return bl, nz


def main():
    t0 = time.time()
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 900.0
    made = []
    adv = []
    nbuilt = noff = 0
    for trial in range(100000):
        if time.time() - t0 > budget:
            break
        m = [25, 26, 26, 27, 27, 28][trial % 6]
        p = [13, 31, 13, 31, 61][trial % 5]
        rng = random.Random(770000 + trial)
        r = build(m, p, rng, passes=5)
        if r is None:
            continue
        bl, nz = r
        nbuilt += 1
        if nz == 0:
            continue                      # on the vanishing stratum
        noff += 1
        K = A.Fp(p)
        fails = [l for l in A.VERTS
                 if not A.vertex_verdict(m, bl, *A.vsplit(l), K)['DELIVERS']]
        prot_fail = [l for l in PROTECTED[m] if l in fails]
        made.append(dict(m=m, p=p, trial=trial, n_words_phi_nonzero=nz,
                         fails=fails, protected_failures=prot_fail,
                         disjunction_holds=len(fails) < 8))
        if prot_fail:
            adv.append(dict(m=m, p=p, trial=trial, fails=fails,
                            protected_failures=prot_fail,
                            point={str(k): [[str(z) for z in r2] for r2 in v]
                                   for k, v in bl.items()}))
        print("[%3d] m=%d p=%-2d built off-stratum nz=%-4d fails=%-28s "
              "PROT_FAIL=%s (%.0fs)"
              % (len(made), m, p, nz, ",".join(fails), prot_fail,
                 time.time() - t0), flush=True)
        OUT['points'] = made
        OUT['adversarial_hits'] = adv
        ck()
    OUT['points'] = made
    OUT['adversarial_hits'] = adv
    OUT['n_built_clean'] = nbuilt
    OUT['n_offstratum'] = noff
    OUT['B1_construction_valid'] = dict(
        n_clean_built=nbuilt, n_offstratum=noff,
        note="every point counted here was verified clean by A10's own "
             "raw 105-matching Phi over its own clean-word set, with all "
             "Gamma cells nonzero",
        ok=nbuilt > 0)
    OUT['B4_offstratum_reached'] = dict(n=noff, ok=noff > 0)
    OUT['B2_adversarial_protected'] = dict(
        n_hits=len(adv), n_points_tested=len(made),
        by_support={str(mm): sum(1 for x in made if x['m'] == mm)
                    for mm in (25, 26, 27, 28)},
        note="LEDGER 18: zero hits is a FAILED SEARCH, not evidence that "
             "the protected vertices cannot fail",
        ok=True)
    # ------------------------------------------------------------- B3
    rng = random.Random(11)
    m, p = 27, 13
    r = build(m, p, rng)
    mut = None
    if r:
        bl = r[0]
        b2 = {e: [row[:] for row in bl[e]] for e in bl}
        e0 = A.S(m).gamma[0]
        b2[e0][1][1] = (b2[e0][1][1] + 1) % p
        okc, bad = A.is_clean_point(m, b2, A.Fp(p))
        mut = dict(still_clean=okc, n_violations=len(bad))
    OUT['B3_mutation'] = dict(
        record=mut, note="a single perturbed cell must destroy cleanness "
                         "-- the builder's output is not trivially clean",
        ok=bool(mut) and not mut['still_clean'])
    for c in DECL:
        OUT['_controls_run'].append(c)
    missing = [c for c in DECL if c not in OUT['_controls_run']]
    OUT['_manifest_ok'] = missing == []
    OUT['elapsed_s'] = round(time.time() - t0, 1)
    OUT['done'] = True
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("BUILD DONE built=%d offstratum=%d adversarial_hits=%d (%.0fs)"
          % (nbuilt, noff, len(adv), time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
