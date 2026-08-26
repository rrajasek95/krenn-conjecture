#!/usr/bin/env python3
"""W24 -- LEMMA W24-C (the three-coefficient identity) and the ROW-ISOLATING
sub-systems.  UNAUDITED.  Exact only.

LEMMA W24-C.  Let i in L = {0,1,2,3}, L \\ {i} = {p1,p2,p3}, sigma the cross
matching (0->7, 1->4, 2->5, 3->6).  For a word w = (x,y) put
    G_ab = A_ab[x_a][x_b]           (a,b in L; Gamma|_L = K_4, always present)
    D_a  = A_{a,sigma a}[x_a][y_{sigma a}]     (0 if that matching edge is
                                                absent -- m=25 has no (3,6))
    F_a  = A_{sigma a, sigma i}[y_{sigma a}][y_{sigma i}]   (0 if absent)
    c_(i,j) = haf_Gamma(V - i - j)(w)   -- the residual-system coefficient of
                                           the single (i,j),  j = sigma(p)
Then, with c_k := c_{(i, sigma p_k)},
    (I1)   F_p1 c_1 - F_p2 c_2 + F_p3 c_3 = 2 G_{p1 p3} D_p2 F_p1 F_p3
    (I2)  -F_p1 c_1 + F_p2 c_2 + F_p3 c_3 = 2 G_{p2 p3} D_p1 F_p2 F_p3
    (I3)   F_p1 c_1 + F_p2 c_2 - F_p3 c_3 = 2 G_{p1 p2} D_p3 F_p1 F_p2
at EVERY word, with NO hypothesis (no clean layer, no factoring).

ROW-ISOLATING L-WORDS.  x isolates row i if the only singles that can be
active at (x,y) are the three (i,*).  Verified below per m.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402

L = (0, 1, 2, 3)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}


def cell(bl, gam_set, u, v, a, b):
    """A_uv[a][b] with u,v in either order; 0 if the edge is not in Gamma."""
    if u < v:
        return bl[(u, v)][a][b] if (u, v) in gam_set else Fraction(0)
    return bl[(v, u)][b][a] if (v, u) in gam_set else Fraction(0)


def coeff(bl, gam_set, e, w):
    """c_e(w) = haf_Gamma(V - endpoints of e)(w), from the definition."""
    rest = tuple(v for v in range(8) if v not in e)
    return C.haf_on(bl, gam_set, rest, w)


def identity_check(bl, gam_set, w):
    """returns [(i, k, lhs, rhs)] for the three identities at each i."""
    x, y = w[:4], w[4:]
    out = []
    for i in L:
        ps = [p for p in L if p != i]
        F = {a: cell(bl, gam_set, SIG[a], SIG[i], y[SIG[a] - 4],
                     y[SIG[i] - 4]) for a in ps}
        D = {a: cell(bl, gam_set, a, SIG[a], x[a], y[SIG[a] - 4]) for a in ps}
        G = {}
        for a in ps:
            for b in ps:
                if a < b:
                    G[(a, b)] = cell(bl, gam_set, a, b, x[a], x[b])
        p1, p2, p3 = ps
        c = {}
        for k, p in enumerate(ps, 1):
            j = SIG[p]
            c[k] = coeff(bl, gam_set, (i, j), w)
        gg = lambda a, b: G[(min(a, b), max(a, b))]
        out.append((i, 1,
                    F[p1] * c[1] - F[p2] * c[2] + F[p3] * c[3],
                    2 * gg(p1, p3) * D[p2] * F[p1] * F[p3]))
        out.append((i, 2,
                    -F[p1] * c[1] + F[p2] * c[2] + F[p3] * c[3],
                    2 * gg(p2, p3) * D[p1] * F[p2] * F[p3]))
        out.append((i, 3,
                    F[p1] * c[1] + F[p2] * c[2] - F[p3] * c[3],
                    2 * gg(p1, p2) * D[p3] * F[p1] * F[p2]))
    return out


def isolating_words(m):
    """{i: [x-words isolating row i]} and the singles they can activate."""
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    gam_set = set(C.gamma_edges(T))
    live = [e for e in sing
            if C.has_pm(gam_set, tuple(v for v in range(8) if v not in e))]
    out = {}
    for i in L:
        ws = []
        for x in product(range(3), repeat=4):
            can = {e for e in live if x[e[0]] == sing[e][0]}
            if can and all(e[0] == i for e in can):
                ws.append((x, tuple(sorted(can))))
        out[i] = ws
    return out, live


def sub_verdict(m, bl, xwords, targets):
    """the residual sub-system restricted to the given x-words, in the
    unknowns `targets` only.

    DEAD singles (those e for which Gamma restricted to V - e has no perfect
    matching) are dropped: no partial matching containing such an e is ever
    completable -- if V-e-f had a Gamma perfect matching, adding f would give
    one for V-e -- so a dead single contributes to NO monomial of any H_w."""
    T = C.TEMPLATES[m]
    gam_set = set(C.gamma_edges(T))
    sing = C.single_edges(T)
    live = {e for e in sing
            if C.has_pm(gam_set, tuple(v for v in range(8) if v not in e))}
    idx = {e: k for k, e in enumerate(targets)}
    n = len(targets)
    rows = []
    for x in xwords:
        for y in product(range(3), repeat=4):
            w = tuple(x) + tuple(y)
            if len(set(w)) == 1:
                continue
            act = [e for e in sing
                   if e in live
                   and w[e[0]] == sing[e][0] and w[e[1]] == sing[e][1]]
            if any(e not in idx for e in act):
                return None                       # not isolated: bail
            v = [Fraction(0)] * n
            for e in act:
                v[idx[e]] = coeff(bl, gam_set, e, w)
            cst = C.phi(bl, gam_set, w)
            if any(v) or cst != 0:
                rows.append(v + [-cst])
    if not rows:
        return dict(n_rows=0, inconsistent=False, forced=[], killed=False)
    R, piv = C.rref(rows, n + 1)
    if n in piv:
        return dict(n_rows=len(rows), rank=len(piv), inconsistent=True,
                    forced=[], killed=True)
    sol = [Fraction(0)] * n
    for k, pc in enumerate(piv):
        if pc < n:
            sol[pc] = R[k][n]
    ker = C.kernel_basis([r[:n] for r in rows], n)
    forced = [str(targets[k]) for k in range(n)
              if sol[k] == 0 and all(b[k] == 0 for b in ker)]
    return dict(n_rows=len(rows), rank=len(piv), inconsistent=False,
                solution_dim=len(ker), forced=forced, killed=bool(forced),
                solution=[str(s) for s in sol])


def main():
    res = {"_header": "UNAUDITED W24 identity W24-C + row-isolating systems."}
    # ---------- (1) the identity, at RANDOM exact points (it is an identity)
    rng = random.Random(24024)
    bad = 0
    tot = 0
    for m in (25, 26, 27, 28):
        gam = C.gamma_edges(C.TEMPLATES[m])
        gam_set = set(gam)
        for _ in range(3):
            bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in gam}
            for _k in range(40):
                w = tuple(rng.randrange(3) for _ in range(8))
                for i, k, lhs, rhs in identity_check(bl, gam_set, w):
                    tot += 1
                    if lhs != rhs:
                        bad += 1
    print("IDENTITY W24-C: %d/%d mismatches at random exact points" % (bad, tot))
    res["identity_mismatches"] = bad
    res["identity_tests"] = tot
    # MUTATION CONTROL.  W24-C is an IDENTITY in the block entries, so
    # perturbing the POINT cannot break it (and a control that did would be
    # meaningless).  The correct mutation is to the ASSERTED IDENTITY: each
    # deliberately wrong variant must FAIL at random exact points.
    gam = C.gamma_edges(C.TEMPLATES[28])
    gam_set = set(gam)
    muts = {"sign +--": (1, 1, -1, 1), "sign +++": (1, 1, 1, 1),
            "factor 3 not 2": (1, -1, 1, Fraction(3, 2)),
            "correct (+ - +, 2)": (1, -1, 1, 1)}
    mres = {}
    for name, (s1, s2, s3, sc) in muts.items():
        fails = 0
        tot = 0
        for _ in range(4):
            bl = {e: [[Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in gam}
            for _k in range(15):
                w = tuple(rng.randrange(3) for _ in range(8))
                x, y = w[:4], w[4:]
                for i in L:
                    ps = [p for p in L if p != i]
                    p1, p2, p3 = ps
                    F = {a: cell(bl, gam_set, SIG[a], SIG[i],
                                 y[SIG[a] - 4], y[SIG[i] - 4]) for a in ps}
                    D2 = cell(bl, gam_set, p2, SIG[p2], x[p2],
                              y[SIG[p2] - 4])
                    G13 = cell(bl, gam_set, min(p1, p3), max(p1, p3),
                               x[min(p1, p3)], x[max(p1, p3)])
                    c = [coeff(bl, gam_set, (i, SIG[p]), w) for p in ps]
                    lhs = s1 * F[p1] * c[0] + s2 * F[p2] * c[1] \
                        + s3 * F[p3] * c[2]
                    rhs = 2 * sc * G13 * D2 * F[p1] * F[p3]
                    tot += 1
                    fails += (lhs != rhs)
        mres[name] = "%d/%d" % (fails, tot)
        print("MUTATION control, variant %-20s fails %d/%d %s"
              % (name, fails, tot,
                 "(want 0)" if name.startswith("correct") else "(want > 0)"))
    res["identity_mutation_variants"] = mres

    # ---------- (2) row-isolating L-words
    for m in (25, 26, 27, 28):
        iso, live = isolating_words(m)
        res["m%d_isolating" % m] = {
            str(i): [[list(x), [str(e) for e in can]] for x, can in v]
            for i, v in iso.items()}
        print("m=%d live singles %s" % (m, [str(e) for e in live]))
        for i in L:
            print("   row %d isolated by %d L-words, e.g. %s"
                  % (i, len(iso[i]), iso[i][:2]))

    # ---------- (3) do the row-isolating sub-systems already kill?
    rows = []
    for m, tag, bl in P.stored_points():
        iso, live = isolating_words(m)
        gam_set = set(C.gamma_edges(C.TEMPLATES[m]))
        rec = dict(m=m, tag=tag)
        for i in L:
            grp = {}
            for x, can in iso[i]:
                grp.setdefault(can, []).append(x)
            best = None
            for can, xs in grp.items():
                v = sub_verdict(m, bl, xs, list(can))
                if v is None:
                    continue
                lab = "%s|%s" % (i, ",".join(str(e) for e in can))
                rec[lab] = (v["killed"], v["inconsistent"], v["forced"],
                            v["n_rows"])
            # noqa
        rows.append(rec)
        print("m=%d %-26s %s" % (m, tag[:26],
                                 {k: v for k, v in rec.items()
                                  if k not in ("m", "tag")}), flush=True)
    res["subsystem_rows"] = rows
    nk = sum(1 for r in rows
             if any(isinstance(v, tuple) and v[0]
                    for k, v in r.items() if k not in ("m", "tag")))
    print("points where SOME row-isolating sub-system already kills: %d/%d"
          % (nk, len(rows)))
    res["n_killed_by_subsystem"] = nk
    json.dump(res, open(os.path.join(HERE, "results_ident.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
