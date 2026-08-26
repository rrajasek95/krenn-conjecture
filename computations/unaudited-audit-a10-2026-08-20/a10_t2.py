#!/usr/bin/env python3
"""A10 TARGET 2 -- independent re-derivation + re-verification of W30-X.

UNAUDITED AUDIT LANE.  Exact only.  Own engine (a10_lib); W30/W26 supply
DATA (stored block matrices) only.

A10's re-derivation (see the report) replaces W30's "S" by the AUGMENTED
slice matrix S'(tau) whose columns are indexed by ALL Gamma-neighbours of
v (the sigma-partner column being d).  Then

  (1) ROWS[t] = P . S'(tau)[t] with P the 3 x |N(v)| matrix whose column
      at a present R-neighbour s_j is sc*e_j and whose column at the
      sigma-partner is u.  The transfer of rank / span-membership needs P
      INJECTIVE, i.e. |N(v)| <= 3 together with u[j0] != 0 at the absent
      slice column j0 (automatic when all Gamma cells are nonzero, since
      u[j0] = d_{q0} * l_{ij}).
  (2) two index choices at a COMMON tau with |fire| = 1 and DISTINCT
      firing letters, both non-delivering  =>  rank S'(tau) = 3, unless
      the doubly-clean row S'_{t3} vanishes -- excluded by all-Gamma-
      cells-nonzero.
  (3) hafnian expansion along v (no signs, hafnians are permanent-like):
      Phi(w|v=t) = <S'(tau)_t, Q(w)>, Q_s = haf_{Gamma-{v,s}}(w).
      Three clean letters => S'Q = 0 => (Q != 0) det S' = 0 for |N| = 3,
      rank S' <= 1 for |N| = 2.

Checks (manifest asserted):
  S3_identity   the cofactor identity, RANDOM blocks (an identity, not a
                property of clean points) and at every audited point
  S1_transfer   P injective <=> |N|<=3 & u[j0]!=0; and the delivery
                predicate computed through S' agrees with the one
                computed through ROWS, at every index choice
  S2_implication  two-firing-letter non-delivery => rank S' = 3
  S3_detS       hypothesis-(H) taus have det S' = 0 (|N|=3) / rank <=1
  THM           (H) met at some tau  =>  the vertex DELIVERS
  PROT          the protected vertices never fail, on every point on disk
  HGAP          (H) census + what the delivery actually buys (pure row?)
  MUT           mutation control: the step-(2)/(3) checkers must be able
                to fail (perturbed blocks break the cofactor identity)
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import defaultdict
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a10_lib as A                                                # noqa: E402

W30DIR = os.path.join(os.path.dirname(HERE),
                      "unaudited-exclusion-w30-2026-08-19")
RES = os.path.join(HERE, "results_t2.json")
DECL = ["S3_identity", "S1_transfer", "S2_implication", "S3_detS", "THM",
        "PROT", "HGAP", "MUT"]
OUT = {"_header": "UNAUDITED A10 target-2 audit of Theorem W30-X",
       "_controls_declared": DECL, "_controls_run": []}
PROTECTED = {25: ['R6'], 26: ['R5', 'R6'], 27: ['R5'], 28: []}


def ck():
    json.dump(OUT, open(RES, "w"), indent=1, default=str)


# ------------------------------------------------------------ S' and Q
def nbrs(m, v):
    st = A.S(m)
    return sorted(s for s in range(8) if (min(s, v), max(s, v)) in st.gs)


def Sprime(m, bl, v, tau, ns, K):
    """S'(tau)[t][col] = A_{v,s}[t][tau_col] over ALL Gamma-neighbours."""
    st = A.S(m)
    return [[A.cell(bl, st.gs, v, s, t, tau[j], K)
             for j, s in enumerate(ns)] for t in range(3)]


def Qvec(m, bl, v, w, ns, K):
    """Q_s = haf_Gamma(V - {v,s})(w), by RAW enumeration of the 15 perfect
    matchings of the remaining six vertices."""
    st = A.S(m)
    out = []
    for s in ns:
        rest = tuple(z for z in range(8) if z not in (v, s))
        tot = K.zero
        for M in A._perfect_matchings(rest):
            pr = K.one
            for (a, b) in M:
                e = (a, b) if a < b else (b, a)
                if e not in st.gs:
                    pr = K.zero
                    break
                pr = K.mul(pr, K.z(bl[e][w[e[0]]][w[e[1]]]))
                if K.isz(pr):
                    break
            tot = K.add(tot, pr)
        out.append(tot)
    return out


def Pmatrix(m, bl, v, kind, w, K):
    """the 3 x |N| transfer matrix P with ROWS[t] = P . S'[t]."""
    sd = A.slice_rows(m, bl, kind, v, w, K)
    if sd is None:
        return None
    rows, Mmat, d, u, sc = sd
    ns = nbrs(m, v)
    if kind == 'R':
        p = A.SGI[v]
        slice_s = [A.SG[q] for q in A.LSIDE if q != p]
    else:
        p = v
        slice_s = [a for a in A.LSIDE if a != p]
        p = A.SG[v]                       # the sigma partner of an L-vertex
    P = [[K.zero] * len(ns) for _ in range(3)]
    for col, s in enumerate(ns):
        if s in slice_s:
            j = slice_s.index(s)
            P[j][col] = sc
        elif s == p:
            for j in range(3):
                P[j][col] = u[j]
        else:
            return "BADCOL"
    return P, rows, Mmat, d, u, sc, ns, slice_s


def matvec(P, x, K):
    return [K.z(sum(K.mul(P[i][j], x[j]) for j in range(len(x))))
            if K.p == 0 else
            sum(K.mul(P[i][j], x[j]) for j in range(len(x))) % K.p
            for i in range(len(P))]


def in_span(vecs, x, K):
    return A.rank(vecs + [x], K) == A.rank(vecs, K)


# ------------------------------------------------------------- analysis
def analyse_vertex(m, bl, lab, K, want_escape=False):
    kind, v = A.vsplit(lab)
    ns = nbrs(m, v)
    idx = A.admissible_cached(m, kind, v, False)
    st = A.S(m)

    bytau = defaultdict(list)
    n_transfer_bad = n_P_not_injective = n_u_zero = 0
    n_single = 0
    for (w, Tf, Tc) in idx:
        if len(Tf) != 1:
            continue
        pk = Pmatrix(m, bl, v, kind, w, K)
        if pk is None:
            continue                       # zero scale
        n_single += 1
        P, rows, Mmat, d, u, sc, ns2, slice_s = pk
        tau = tuple(w[s] for s in ns)
        Sp = Sprime(m, bl, v, tau, ns, K)
        # (1a) ROWS[t] == P . S'[t]
        for t in range(3):
            if matvec(P, Sp[t], K) != [K.z(z) for z in rows[t]]:
                n_transfer_bad += 1
        inj = (A.rank([[P[i][j] for i in range(3)] for j in range(len(ns))],
                      K) == len(ns))
        if not inj:
            n_P_not_injective += 1
        # (1b) the delivery predicate through S' must agree when injective
        tf = Tf[0]
        viaR = in_span([rows[t] for t in Tc], rows[tf], K)
        viaS = in_span([Sp[t] for t in Tc], Sp[tf], K)
        if inj and viaR != viaS:
            n_transfer_bad += 1
        # u[j0] at the absent slice column
        absent = [j for j, s in enumerate(slice_s) if s not in ns]
        if len(absent) == 1 and K.isz(u[absent[0]]):
            n_u_zero += 1
        bytau[tau].append(dict(w=w, t=tf, delivers=viaR, rankS=A.rank(Sp, K)))

    # untriggered words (all three letters clean), grouped by tau
    unt = defaultdict(list)
    others = [c for c in range(8) if c != v]
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for c, a in zip(others, vals):
            w[c] = a
        ok = True
        for t in range(3):
            ww = list(w)
            ww[v] = t
            if len(set(ww)) == 1 or st.active_live(tuple(ww)):
                ok = False
                break
        if ok:
            unt[tuple(w[s] for s in ns)].append(tuple(w))

    n_two = n_H = n_esc = 0
    s2_bad = s3_bad = 0
    escapes = []
    for tau, lst in bytau.items():
        letters = set(x['t'] for x in lst)
        if len(letters) < 2:
            continue
        n_two += 1
        Sp = Sprime(m, bl, v, tau, ns, K)
        rk = A.rank(Sp, K)
        # STEP 2: pick two non-delivering choices with distinct letters
        nd = {}
        for x in lst:
            if not x['delivers']:
                nd.setdefault(x['t'], x)
        if len(nd) >= 2 and rk != 3:
            s2_bad += 1
        # STEP 3: an untriggered word at this tau with Q != 0
        qw = None
        for w in unt.get(tau, []):
            Q = Qvec(m, bl, v, w, ns, K)
            # S'.Q must vanish (three clean letters)
            for t in range(3):
                z = K.zero
                for j in range(len(ns)):
                    z = K.add(z, K.mul(Sp[t][j], Q[j]))
                if not K.isz(z):
                    s3_bad += 1
            if any(not K.isz(z) for z in Q):
                qw = (w, Q)
                break
        if qw is not None:
            if len(ns) == 3 and A.rank(Sp, K) > 2:
                s3_bad += 1
            if len(ns) == 2 and A.rank(Sp, K) > 1:
                s3_bad += 1
            n_H += 1
        else:
            n_esc += 1
            if want_escape:
                escapes.append(dict(tau=list(tau),
                                    n_untriggered=len(unt.get(tau, [])),
                                    rankS=rk))
    ver = A.vertex_verdict(m, bl, kind, v, K, detail=True)
    # what does delivery actually buy?  a genuine PURE ROW needs exactly one
    # active live single at the firing word and c_e != 0
    n_del_pure = 0
    for (w, Tf, Tc) in ver['detail']:
        for t in Tf:
            ww = list(w)
            ww[v] = t
            act = st.active_live(tuple(ww))
            if len(act) == 1 and not K.isz(
                    A.coeff_single(m, bl, act[0], tuple(ww), K)):
                n_del_pure += 1
                break
    return dict(vertex=lab, n_neighbours=len(ns), neighbours=ns,
                n_single_fire_choices=n_single,
                n_two_letter_taus=n_two, n_H_taus=n_H, n_escape_taus=n_esc,
                transfer_violations=n_transfer_bad,
                P_not_injective=n_P_not_injective, u_absent_zero=n_u_zero,
                step2_violations=s2_bad, step3_violations=s3_bad,
                DELIVERS=ver['DELIVERS'], n_deliver=ver['n_deliver'],
                n_deliver_with_pure_row=n_del_pure,
                THEOREM_APPLIES=n_H > 0,
                THEOREM_CONSISTENT=(n_H == 0 or ver['DELIVERS']),
                escapes=escapes[:6])


# ------------------------------------------------------------- point IO
def load_all():
    pts = []
    d = json.load(open(os.path.join(W30DIR, "results_verify_hunt.json")))
    for e in d["verified"]:
        pts.append((e["m"], e["p"], "verify#%d" % d["verified"].index(e),
                    {eval(k): [[int(z) for z in r] for r in v]
                     for k, v in e["point"].items()}))
    d = json.load(open(os.path.join(W30DIR, "points_hunt.json")))
    for e in d["points"]:
        if e.get("van"):
            continue
        cv = (lambda z: int(z)) if e["p"] else (lambda z: Fraction(z))
        pts.append((e["m"], e["p"], "hunt|" + str(e["tag"])[:40],
                    {eval(k): [[cv(z) for z in r] for r in v]
                     for k, v in e["point"].items()}))
    for m in (25, 26, 27, 28):
        f = os.path.join(W30DIR, "points_m%d_wide.json" % m)
        if os.path.exists(f):
            d = json.load(open(f))
            for e in d["points"]:
                if e.get("van"):
                    continue
                pts.append((m, 0, "wide%d|s%s" % (m, e.get("seed")),
                            {eval(k): [[Fraction(z) for z in r] for r in v]
                             for k, v in e["point"].items()}))
    f = os.path.join(W30DIR, "points_stored.json")
    if os.path.exists(f):
        d = json.load(open(f))
        for e in d["points"]:
            if e.get("van"):
                continue
            pts.append((e["m"], 0, "stored|" + str(e.get("tag"))[:30],
                        {eval(k): [[Fraction(z) for z in r] for r in v]
                         for k, v in e["point"].items()}))
    return pts


def main():
    t0 = time.time()
    rng = random.Random(20260820)

    # ------------------------------------------------------ S3_identity
    bad = []
    for m in (25, 26, 27, 28):
        for p in (0, 13, 31):
            K = A.Rat() if p == 0 else A.Fp(p)
            bl = {e: [[(Fraction(rng.randrange(-9, 10)) if p == 0
                        else rng.randrange(0, p)) for _ in range(3)]
                      for _ in range(3)] for e in A.S(m).gamma}
            for v in range(8):
                ns = nbrs(m, v)
                for _ in range(8):
                    w = [rng.randrange(3) for _ in range(8)]
                    tau = tuple(w[s] for s in ns)
                    Sp = Sprime(m, bl, v, tau, ns, K)
                    Q = Qvec(m, bl, v, tuple(w), ns, K)
                    for t in range(3):
                        ww = list(w)
                        ww[v] = t
                        lhs = A.phi_raw(m, bl, tuple(ww), K)
                        rhs = K.zero
                        for j in range(len(ns)):
                            rhs = K.add(rhs, K.mul(Sp[t][j], Q[j]))
                        if not K.isz(K.add(lhs, -rhs)):
                            bad.append((m, p, v, tuple(ww)))
    OUT["S3_identity"] = dict(tests=4 * 3 * 8 * 8 * 3, violations=len(bad),
                              sample=bad[:4], ok=not bad,
                              note="cofactor identity on RANDOM blocks -- "
                                   "an identity, no cleanness assumed")
    OUT["_controls_run"].append("S3_identity")
    print("S3 identity on random blocks: violations=%d" % len(bad),
          flush=True)
    ck()

    # ------------------------------------------------------------- MUT
    m, p = 27, 31
    K = A.Fp(p)
    bl = {e: [[rng.randrange(1, p) for _ in range(3)] for _ in range(3)]
          for e in A.S(m).gamma}
    v = 5
    ns = nbrs(m, v)
    w = tuple(rng.randrange(3) for _ in range(8))
    tau = tuple(w[s] for s in ns)
    base_ok = True
    Sp = Sprime(m, bl, v, tau, ns, K)
    Q = Qvec(m, bl, v, w, ns, K)
    for t in range(3):
        ww = list(w)
        ww[v] = t
        lhs = A.phi_raw(m, bl, tuple(ww), K)
        rhs = sum(Sp[t][j] * Q[j] for j in range(len(ns))) % p
        base_ok &= (lhs - rhs) % p == 0
    b2 = {e: [r[:] for r in bl[e]] for e in bl}
    e0 = (min(v, ns[0]), max(v, ns[0]))
    b2[e0][0][0] = (b2[e0][0][0] + 1) % p
    Sp2 = Sprime(m, b2, v, tau, ns, K)
    Q2 = Qvec(m, b2, v, w, ns, K)
    mut_detected = False
    for t in range(3):
        ww = list(w)
        ww[v] = t
        lhs = A.phi_raw(m, bl, tuple(ww), K)      # UNMUTATED Phi
        rhs = sum(Sp2[t][j] * Q2[j] for j in range(len(ns))) % p
        if (lhs - rhs) % p:
            mut_detected = True
    OUT["MUT"] = dict(baseline_identity_holds=base_ok,
                      mutation_breaks_identity=mut_detected,
                      ok=base_ok and mut_detected,
                      note="one perturbed cell must make the cofactor "
                           "identity fail against the unperturbed Phi")
    OUT["_controls_run"].append("MUT")
    print("MUT: base=%s detected=%s" % (base_ok, mut_detected), flush=True)
    ck()

    # ------------------------------------- the per-point audit of W30-X
    pts = load_all()
    print("loaded %d off-stratum points" % len(pts), flush=True)
    recs = []
    agg = dict(transfer_violations=0, P_not_injective=0, u_absent_zero=0,
               step2_violations=0, step3_violations=0,
               theorem_inconsistent=0, protected_failures=0,
               n_points=0, n_H_zero=0, n_deliver_no_pure=0)
    for (m, p, tag, bl) in pts:
        if not PROTECTED.get(m):
            continue
        K = A.Rat() if p == 0 else A.Fp(p)
        okc, badw = A.is_clean_point(m, bl, K)
        allnz = A.all_gamma_cells_nonzero(m, bl, K)
        if not okc:
            continue
        agg['n_points'] += 1
        out = dict(m=m, p=p, tag=tag, clean=okc, allnz=allnz, vert={})
        for lab in PROTECTED[m]:
            r = analyse_vertex(m, bl, lab, K, want_escape=True)
            out['vert'][lab] = r
            agg['transfer_violations'] += r['transfer_violations']
            agg['P_not_injective'] += r['P_not_injective']
            agg['u_absent_zero'] += r['u_absent_zero']
            agg['step2_violations'] += r['step2_violations']
            agg['step3_violations'] += r['step3_violations']
            agg['theorem_inconsistent'] += (0 if r['THEOREM_CONSISTENT']
                                            else 1)
            agg['protected_failures'] += (0 if r['DELIVERS'] else 1)
            agg['n_H_zero'] += (1 if r['n_H_taus'] == 0 else 0)
            agg['n_deliver_no_pure'] += (
                1 if (r['DELIVERS'] and r['n_deliver_with_pure_row'] == 0)
                else 0)
        recs.append(out)
        if len(recs) % 5 == 0 or len(recs) < 6:
            print("[%3d] m=%d p=%-2d %-30s %s (%.0fs)"
                  % (len(recs), m, p, tag[:30],
                     {l: (out['vert'][l]['n_H_taus'],
                          out['vert'][l]['n_escape_taus'],
                          out['vert'][l]['DELIVERS'],
                          out['vert'][l]['n_deliver_with_pure_row'])
                      for l in out['vert']}, time.time() - t0), flush=True)
            OUT['points'] = recs
            OUT['aggregate'] = agg
            ck()
    OUT['points'] = recs
    OUT['aggregate'] = agg
    OUT["S1_transfer"] = dict(violations=agg['transfer_violations'],
                              P_not_injective=agg['P_not_injective'],
                              u_absent_zero=agg['u_absent_zero'],
                              ok=agg['transfer_violations'] == 0)
    OUT["S2_implication"] = dict(violations=agg['step2_violations'],
                                 ok=agg['step2_violations'] == 0)
    OUT["S3_detS"] = dict(violations=agg['step3_violations'],
                          ok=agg['step3_violations'] == 0)
    OUT["THM"] = dict(inconsistencies=agg['theorem_inconsistent'],
                      ok=agg['theorem_inconsistent'] == 0)
    OUT["PROT"] = dict(protected_vertex_failures=agg['protected_failures'],
                       n_points=agg['n_points'],
                       ok=agg['protected_failures'] == 0)
    OUT["HGAP"] = dict(points_with_no_H_tau=agg['n_H_zero'],
                       delivering_without_pure_row=agg['n_deliver_no_pure'])
    for c in ["S1_transfer", "S2_implication", "S3_detS", "THM", "PROT",
              "HGAP"]:
        OUT["_controls_run"].append(c)
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = missing == []
    OUT["_manifest_missing"] = missing
    OUT["elapsed_s"] = round(time.time() - t0, 1)
    OUT["done"] = True
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("T2 DONE %s (%.0fs)" % (agg, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
