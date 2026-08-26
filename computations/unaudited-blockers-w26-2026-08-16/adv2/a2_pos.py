#!/usr/bin/env python3
"""adv2 -- POSITIVE CONTROL + independent re-verification.  UNAUDITED.
EXACT ONLY (fractions.Fraction).

(P1) I re-derive, FROM SCRATCH and by a different route than adv/, a
     clean m=26 point off the vanishing stratum whose (2,6)-solo family
     SURVIVES, and verify it with C.H_word (raw 105-matching definition).

     MY DERIVATION (independent of adv/adv_solo.py's tensor ansatz).
     Call a vertex v SEPARABLE if, after the gauge
        A_uv[a][b] -> t_u(a) t_v(b) A_uv[a][b]      (H_w -> prod_v t_v(w_v) H_w)
     every Gamma block at v is constant in v's own index.  Then Phi does
     not depend on w_v at all.
     Each vertex has a DEACTIVATING letter c_v that switches off every
     single at v:  c_0 in {1,2}, c_1 = 2, c_2 = 0, c_3 in {0,1},
     c_4 in {1,2}, c_5 = 2, c_6 = 0, c_7 in {0,1}.
     Hence if S is separable and S covers every single edge, Phi == 0.
     Take S = {0,3,4,5,7} (T = {1,2,6}); the only singles inside T are
     (1,6) and (2,6).  Writing
        A01 = b(x1), A02 = c(x2), A03 = g, A07 = v0, A13 = h(x1),
        A23 = k(x2), A14 = r(x1), A25 = s(x2), A12 = M(x1,x2),
        A45 = alpha, A47 = beta, A36 = f(y6), A56 = t(y6), A67 = q(y6)
     the L-subset expansion gives  Phi = f X + q Y + t Z  with
        X = s(v0 r + beta b) + alpha v0 M
        Y = g r s + alpha hafL,   Z = v0 r k + beta hafL,
        hafL = b k + c h + g M.
     Put N[y6] = (f,q,t)(y6).  Choosing N[0] = mu*n, N[2] = n with
     n = (phi,1,1) and n.(X,Y,Z) = 0 identically makes Phi vanish for
     y6 in {0,2}; N[1] = cp*n + cc*(-1,1,0) then gives
        Phi(w) = cc * (Y - X)(x1,x2)      at y6 = 1,  0 elsewhere.
     n.(X,Y,Z) = 0 solves linearly for M.  Specialising g = v0 collapses
        (Y - X)(x1,x2) = b(x1) p(x2) + h(x1) q2(x2),
        p = alpha k - beta s,   q2 = alpha c,
     and the whole problem becomes 2x2 linear algebra:
        (Y-X) = 0 on x1 in {0,2} x x2 in {0,1}   [cleanliness at y6=1]
        p(2) = 0                                  [constant (2,6) ratio]
     because c_{(2,6)} = v0 alpha h(x1) there.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- positive control + re-verification"}
RAN = []


# ------------------------------------------------------------ construction
def build_T126(pr, m=26):
    """my own S={0,3,4,5,7}-separable point (T = {1,2,6})."""
    v0, g, al, be = pr["v0"], pr["g"], pr["alpha"], pr["beta"]
    mu, ph, cp, cc = pr["mu"], pr["phi"], pr["cp"], pr["cc"]
    b, h, r = pr["b"], pr["h"], pr["r"]
    c, k, s = pr["c"], pr["k"], pr["s"]
    den = ph * al * v0 + (al + be) * g
    assert den != 0, "degenerate: phi*alpha*v0 + (alpha+beta)*g = 0"
    M = [[-(s[x2] * ((ph * v0 + g) * r[x1] + ph * be * b[x1])
            + k[x2] * (v0 * r[x1] + (al + be) * b[x1])
            + (al + be) * c[x2] * h[x1]) / den
          for x2 in range(3)] for x1 in range(3)]
    n = [ph, F(1), F(1)]
    N = {0: [mu * t for t in n], 2: list(n),
         1: [cp * n[0] - cc, cp * n[1] + cc, cp * n[2]]}
    f = [N[y6][0] for y6 in range(3)]
    q = [N[y6][1] for y6 in range(3)]
    t = [N[y6][2] for y6 in range(3)]
    bl = {}
    bl[(0, 1)] = [[b[x1] for x1 in range(3)] for _ in range(3)]
    bl[(0, 2)] = [[c[x2] for x2 in range(3)] for _ in range(3)]
    bl[(0, 3)] = [[g] * 3 for _ in range(3)]
    bl[(0, 7)] = [[v0] * 3 for _ in range(3)]
    bl[(1, 2)] = M
    bl[(1, 3)] = [[h[x1]] * 3 for x1 in range(3)]
    bl[(1, 4)] = [[r[x1]] * 3 for x1 in range(3)]
    bl[(2, 3)] = [[k[x2]] * 3 for x2 in range(3)]
    bl[(2, 5)] = [[s[x2]] * 3 for x2 in range(3)]
    bl[(3, 6)] = [[f[y6] for y6 in range(3)] for _ in range(3)]
    bl[(4, 5)] = [[al] * 3 for _ in range(3)]
    bl[(4, 7)] = [[be] * 3 for _ in range(3)]
    bl[(5, 6)] = [[t[y6] for y6 in range(3)] for _ in range(3)]
    bl[(6, 7)] = [[q[y6]] * 3 for y6 in range(3)]
    if m == 27:
        bl[(4, 6)] = [[pr["d46"][y6] for y6 in range(3)] for _ in range(3)]
    if m == 28:
        bl[(4, 6)] = [[pr["d46"][y6] for y6 in range(3)] for _ in range(3)]
        bl[(5, 7)] = [[pr["e57"][y5]] * 3 for y5 in range(3)]
    assert sorted(bl) == sorted(A.Geo(m).gam), (sorted(bl),
                                                sorted(A.Geo(m).gam))
    return bl


PARAMS26 = dict(v0=F(1), g=F(1), alpha=F(1), beta=F(1),
                mu=F(2), phi=F(1), cp=F(1), cc=F(2),
                b=[F(1), F(1), F(2)], h=[F(1), F(2), F(2)],
                r=[F(1), F(2), F(3)],
                c=[F(-1), F(-2), F(3)], k=[F(2), F(3), F(1)],
                s=[F(1), F(1), F(1)])


def report(tag, m, bl, want_survive=None):
    rec = dict(tag=tag, m=m)
    rec["all_cells_nonzero"] = A.all_cells_nonzero(bl, A.Geo(m))
    rec["clean"] = A.is_clean(m, bl)
    rec["stratum"] = A.on_stratum(m, bl)
    sup = A.phi_support(m, bl)
    rec["n_phi_nonzero_of_6561"] = len(sup)
    sv = {}
    for e in A.Geo(m).live:
        sv[str(e)] = A.solo_verdict(m, bl, e)
    rec["solo"] = sv
    rec["solo_survivors"] = [k for k, v in sv.items() if v["survives"]]
    v = A.full_verdict(m, bl)
    rec["full_verdict"] = {k: v[k] for k in
                           ("n_unknowns", "n_rows", "rank", "inconsistent",
                            "killed")}
    rec["forced_zero"] = v.get("forced_zero")
    rec["point"] = A.dump(bl)
    print("  %-28s cells!=0=%s clean=%s stratum=%s |supp Phi|=%d"
          % (tag, rec["all_cells_nonzero"], rec["clean"], rec["stratum"],
             len(sup)))
    print("      solo survivors: %s" % rec["solo_survivors"])
    print("      full verdict: killed=%s inconsistent=%s rank=%s"
          % (v["killed"], v.get("inconsistent"), v["rank"]))
    if want_survive is not None:
        assert set(rec["solo_survivors"]) >= set(want_survive), \
            "POSITIVE CONTROL FAILED: wanted %s got %s" % (
                want_survive, rec["solo_survivors"])
    return rec


def raw_reverify(m, bl, e, kappa):
    """re-derive the e-solo verdict entirely from C.H_word."""
    T = C.TEMPLATES[m]
    z0 = {f_: F(0) for f_ in C.single_edges(T)}
    zk = dict(z0)
    zk[e] = kappa
    sol = A.Geo(m).solo[e]
    nbad = sum(1 for w in sol if C.H_word(bl, T, zk, w) != 0)
    ncl = sum(1 for w in A.Geo(m).clean if C.H_word(bl, T, z0, w) != 0)
    nz = sum(1 for w in C.WORDS if C.H_word(bl, T, z0, w) != 0)
    cons = [str(C.H_word(bl, T, zk, (cc,) * 8)) for cc in range(3)]
    print("      [RAW C.H_word] clean words with Phi!=0: %d/%d ; "
          "Phi!=0 at %d/6561 words ; z_%s=%s kills H on %d/%d solo words "
          "(bad %d) ; H at constants=%s"
          % (ncl, len(A.Geo(m).clean), nz, e, kappa, len(sol) - nbad,
             len(sol), nbad, cons))
    return dict(clean_bad=ncl, n_phi_nonzero=nz, solo_bad=nbad,
                n_solo=len(sol), H_constants=cons)


def main():
    # ------------------------------------------------------------- (P1)
    print("=" * 74)
    print("(P1) POSITIVE CONTROL -- my own from-scratch (2,6)-solo survivor")
    print("=" * 74)
    RAN.append("P1_own_solo26")
    bl = build_T126(PARAMS26, 26)
    rec = report("adv2 T={1,2,6} m=26", 26, bl, want_survive=["(2, 6)"])
    kap = F(A.solo_verdict(26, bl, (2, 6))["ratio"])
    rec["raw"] = raw_reverify(26, bl, (2, 6), kap)
    assert rec["clean"] and not rec["stratum"]
    assert rec["raw"]["clean_bad"] == 0 and rec["raw"]["solo_bad"] == 0
    OUT["P1"] = rec

    # ------------------------------------------------------------- (P2)
    print()
    print("=" * 74)
    print("(P2) independent re-verification of adv/'s three stored objects")
    print("=" * 74)
    RAN.append("P2_reverify_adv")
    P2 = {}
    for fn, key, m in (("results_solo.json", "m26", 26),
                       ("results_solo.json", "m27", 27),
                       ("results_case2b.json", "main", 25)):
        p = os.path.join(os.path.dirname(HERE), "adv", fn)
        d = json.load(open(p))
        node = d[key]
        pt = node.get("point")
        if pt is None:
            print("  %s/%s: no point" % (fn, key))
            continue
        b2 = A.load(pt)
        r = report("adv %s/%s" % (fn, key), m, b2)
        P2["%s/%s" % (fn, key)] = {k: r[k] for k in
                                   ("clean", "stratum", "solo_survivors",
                                    "full_verdict", "n_phi_nonzero_of_6561")}
        print("      adv claimed solo_survives=%s"
              % node.get("solo_survives", node.get("solo_survivors")))
    OUT["P2"] = P2

    # ------------------------------------------------------------- (P3)
    print()
    print("=" * 74)
    print("(P3) MUTATION control on my P1 point")
    print("=" * 74)
    RAN.append("P3_mutation")
    nb_ok = nb_tot = 0
    still_clean = []
    for e in sorted(bl):
        for i in range(3):
            for j in range(3):
                nb = {f_: [rw[:] for rw in bl[f_]] for f_ in bl}
                nb[e][i][j] = nb[e][i][j] + F(1)
                nb_tot += 1
                if A.is_clean(26, nb):
                    still_clean.append("%s[%d][%d]" % (e, i, j))
                else:
                    nb_ok += 1
    print("  %d/%d single-cell (+1) perturbations destroy cleanliness"
          % (nb_ok, nb_tot))
    print("  survivors (still clean): %s" % still_clean)
    surv_solo = []
    for lab in still_clean:
        es, ij = lab.split("[")[0], lab.split("[")[1:]
        e = tuple(int(t) for t in es.strip("()").split(","))
        i, j = int(ij[0][0]), int(ij[1][0])
        nb = {f_: [rw[:] for rw in bl[f_]] for f_ in bl}
        nb[e][i][j] = nb[e][i][j] + F(1)
        if A.solo_verdict(26, nb, (2, 6))["survives"]:
            surv_solo.append(lab)
    print("  of those, still (2,6)-solo surviving: %s" % surv_solo)
    OUT["P3"] = dict(broke=nb_ok, total=nb_tot, still_clean=still_clean,
                     still_solo=surv_solo)
    assert nb_ok > 0, "mutation control vacuous"

    # ------------------------------------------------------------- (P4)
    print()
    print("=" * 74)
    print("(P4) OUT-OF-LOCUS control: predicates are not vacuously false")
    print("=" * 74)
    RAN.append("P4_out_of_locus")
    # a NON-clean point whose (2,6)-solo family nevertheless SURVIVES
    import random
    rng = random.Random(20260817)
    # (a) a NON-clean point whose (2,6)-solo family nevertheless SURVIVES.
    #     Construction: take my P1 point and break ONE Gamma cell that does
    #     not enter c_(2,6) nor the y6=1 slice -- cleanliness dies, the solo
    #     predicate lives.  (Random junk almost never survives, so a
    #     construction, not a search, is the honest non-vacuity witness.)
    found = None
    cand = [((0, 1), i, j) for i in range(3) for j in range(3)] + \
           [((0, 2), i, j) for i in range(3) for j in range(3)] + \
           [((1, 2), i, j) for i in range(3) for j in range(3)] + \
           [((2, 3), i, j) for i in range(3) for j in range(3)] + \
           [((1, 4), i, j) for i in range(3) for j in range(3)]
    for (e, i, j) in cand:
        nb = {f_: [rw[:] for rw in bl[f_]] for f_ in bl}
        nb[e][i][j] = nb[e][i][j] + F(1)
        if A.is_clean(26, nb):
            continue
        if A.solo_verdict(26, nb, (2, 6))["survives"]:
            found = (e, i, j, nb)
            break
    print("  NON-clean point with (2,6)-solo SURVIVING: %s"
          % (str(found[:3]) if found else "NOT FOUND"))
    OUT["P4"] = dict(nonclean_solo_survivor=(A.dump(found[3])
                                             if found else None),
                     nonclean_solo_witness=(str(found[:3]) if found else None))
    # (b) a point (necessarily NOT clean) whose FULL residual verdict is
    #     killed=False -- proves the primary predicate is not vacuously
    #     false as a test.
    #     Explicit construction: zero out every R-block and the sigma block
    #     (0,7).  Then D0 = 0 so Phi == 0, and every c_e carries an R-block
    #     factor so every c_e == 0: the residual system has NO rows at all,
    #     hence killed=False and z = (1,...,1) is a full-support solution.
    #     This point is of course NOT clean (it has zero Gamma cells).
    wit = {e: [[F(rng.randint(1, 7)) for _ in range(3)] for _ in range(3)]
           for e in A.Geo(26).gam}
    for e in A.Geo(26).gam:
        if (e[0] >= 4 and e[1] >= 4) or e == (0, 7):
            wit[e] = [[F(0)] * 3 for _ in range(3)]
    v2 = A.full_verdict(26, wit)
    ok2 = (not v2["killed"])
    found2 = (wit, v2) if ok2 else None
    print("  point with FULL residual verdict killed=False: %s "
          "(n_rows=%d rank=%d dim=%s clean=%s)"
          % (ok2, v2["n_rows"], v2["rank"], v2.get("solution_dim"),
             A.is_clean(26, wit)))
    if found2:
        zall = {str(e): "1" for e in A.Geo(26).live}
        print("     full-support solution z = %s" % zall)
        OUT["P4"]["nonclean_full_survivor"] = dict(
            point=A.dump(found2[0]), z=zall, clean=A.is_clean(26, found2[0]),
            verdict={k: v2[k] for k in ("n_unknowns", "n_rows", "rank",
                                        "inconsistent", "killed")})
    assert found is not None, "OUT-OF-LOCUS control failed for solo predicate"
    assert found2 is not None, "OUT-OF-LOCUS control failed for full verdict"

    declared = ["P1_own_solo26", "P2_reverify_adv", "P3_mutation",
                "P4_out_of_locus"]
    missing = [d for d in declared if d not in RAN]
    print("\nCONTROL MANIFEST declared=%s ran=%s" % (declared, RAN))
    assert not missing, "CONTROL DID NOT RUN: %s" % missing
    OUT["control_manifest"] = dict(declared=declared, ran=RAN)
    json.dump(OUT, open(os.path.join(HERE, "results_pos.json"), "w"),
              indent=1, default=str)
    print("wrote results_pos.json")


if __name__ == "__main__":
    main()
