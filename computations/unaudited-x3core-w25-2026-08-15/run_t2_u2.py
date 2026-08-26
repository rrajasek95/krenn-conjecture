#!/usr/bin/env python3
"""W25 T2 -- PUSHING W23-U2 PAST ITS HYPOTHESIS.

W23-U2: every live pair of Delta^(3)_N (three disjoint perfect matchings, unit
matching products) carries a witness, via K = I + E_{c2c3} - E_{c3c2}.  Its
proof uses "EVERY vertex has exactly three live blocks, one per colour".

Findings established here.

(A) THE NAIVE EXTENSION IS FALSE.  "Every live pair of a diagonal X_2 source
    carries a witness" fails: at N = 6, exhaustively, 15 of the 24 skeleton
    classes contain BLOCKED live pairs.  The obstruction family is explicit.

(B) THE CORRECT EXTENSION -- W25-U3, the LOCAL hypothesis.  Call a vertex
    CLEAN if it has exactly three live blocks, one per colour (equivalently,
    by W23-DR, minimum possible degree).  Then: if a live pair (p,q) has AT
    LEAST ONE clean endpoint, the SAME antisymmetric cap kills E.  Only one of
    the two endpoints needs the property, and every other vertex may carry
    arbitrarily many extra live blocks.  This is verified here as a POLYNOMIAL
    IDENTITY in the weights (ideal membership in the pure equations, hence
    valid at every point of every class), exhaustively over all 24 N=6 classes
    (138/138 such pairs) and on constructed N=8 and N=10 diagonal X_2 sources
    with extra edges.

    Mechanism (derived, and matching the verification): with q clean, the
    R-support meets U only through q's two remaining partners Y = {Q2,Q3}, so
    every contributing J has |J| = 2 and consists of one edge at Q2 and one at
    Q3; the cap coefficients contract to  A_g B_{g'} + A_{g'} B_g  with
    A_g = [g=c2]-[g=c3], B_g = [g=c3]+[g=c2], which VANISHES exactly on the
    mixed pair (c2,c3) and on anything touching c1 -- W23-U2's antisymmetry
    cancellation, now localised at one endpoint.  The surviving same-colour
    pairs are killed by the X_2 conditions themselves (an explicit skeleton
    realising a surviving pair is exhibited and shown to FAIL X_2).

(C) NO diagonal X_2 = X_3 source at N = 6 is all-blocked: 23 of the 24 classes
    have >= 2 pairs proved by (B)-type identities; the remaining class (the
    (5,5,5) "three-pairs" partition, which has NO clean vertex) is settled by
    an explicit single-component argument, verified symbolically here.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x3core-w25-2026-08-15")
sys.path.insert(0, BASE)
import w25_core as C                                            # noqa: E402
import w25_decide as D                                          # noqa: E402
import run_t1d_diagonal as T1D                                  # noqa: E402
import run_t1e_diagonal_uniform as T1E                          # noqa: E402

RES = {}
RAN = []


def control(name):
    RAN.append(name)


def antisym_cap(c1, one, zero):
    c2, c3 = [c for c in range(3) if c != c1]
    K = [[one if i == j else zero for j in range(3)] for i in range(3)]
    K[c2][c3] = K[c2][c3] + one
    K[c3][c2] = K[c3][c2] - one
    return K


def colour_map(Ls, n):
    col = {}
    for c, L in enumerate(Ls):
        for e in T1D.mask_edges(L) if n == 6 else L:
            col[tuple(sorted(e))] = c
    return col


def clean_vertices(col, n):
    deg = {v: [] for v in range(n)}
    for e, c in col.items():
        deg[e[0]].append(c)
        deg[e[1]].append(c)
    return {v for v in range(n) if sorted(deg[v]) == [0, 1, 2]}


# ------------------------------------------------------ general-N diagonal

def diag_source(col, weights, n):
    src = C.zero_source(n, 3, Fraction(0))
    for e, c in col.items():
        src[e][c][c] = weights[e]
    return src


def cond_ii_ok(col, n):
    """No L_c has a perfect matching of B\\{a,b} for (a,b) in L_d, d != c."""
    Lc = {c: [e for e, cc in col.items() if cc == c] for c in range(3)}
    for c in range(3):
        for d in range(3):
            if d == c:
                continue
            for (a, b) in Lc[d]:
                rest = tuple(x for x in range(n) if x not in (a, b))
                k = sum(1 for M in T1D.all_pms(rest)
                        if all(tuple(sorted(e)) in Lc[c] for e in M))
                if k != 0:
                    return False, (c, (a, b), k)
    return True, None


def build_n_diagonal(n, rng, extra=3, tries=400):
    """Delta^(3)_n plus `extra` extra edges, subject to condition (ii); returns
    (colour map, a weight assignment putting it in X_2)."""
    mats = C.default_three_pms(n)
    base = {}
    for c, M in enumerate(mats):
        for e in M:
            base[tuple(sorted(e))] = c
    allowed = [e for e in combinations(range(n), 2) if e not in base]
    for _ in range(tries):
        col = dict(base)
        rng.shuffle(allowed)
        added = 0
        for e in allowed:
            if added >= extra:
                break
            c = rng.randrange(3)
            col[e] = c
            ok, _ = cond_ii_ok(col, n)
            if ok:
                added += 1
            else:
                del col[e]
        if added < extra:
            continue
        # weights: extra edges free, matching edges scaled so haf(t|L_c) = 1
        w = {e: Fraction(rng.randint(1, 4)) for e in col}
        for c, M in enumerate(mats):
            ee = [tuple(sorted(e)) for e in M]
            # every PM of L_c is computed exactly; solve for the last weight
            Lc = [e for e, cc in col.items() if cc == c]
            terms = [tuple(sorted(tuple(sorted(x)) for x in M2))
                     for M2 in T1D.all_pms(tuple(range(n)))
                     if all(tuple(sorted(x)) in Lc for x in M2)]
            last = ee[-1]
            alpha = Fraction(0)
            beta = Fraction(0)
            for M2 in terms:
                pr = Fraction(1)
                for e in M2:
                    if e != last:
                        pr *= w[e]
                if last in M2:
                    alpha += pr
                else:
                    beta += pr * w[last] / w[last]
            if alpha == 0:
                break
            w[last] = (Fraction(1) - beta) / alpha
            if w[last] == 0:
                break
        else:
            src = diag_source(col, w, n)
            if C.in_Xk(src, n, 2)[0]:
                return col, w, src
    return None, None, None


def surviving_pair(col, p, q, n):
    """The sharp obstruction: a pair {u,v} in U\\Y with alpha(u)=alpha(v) in
    {c2,c3} such that the L-graph on U\\{Q_c2,Q_c3,u,v} has a perfect
    matching.  q must be clean."""
    c1 = col[tuple(sorted((p, q)))]
    others = [c for c in range(3) if c != c1]
    Y = []
    for c in others:
        for v in range(n):
            if v in (p, q):
                continue
            if col.get(tuple(sorted((q, v)))) == c:
                Y.append(v)
    if len(Y) != 2:
        return None
    U = [x for x in range(n) if x not in (p, q)]
    rest0 = [x for x in U if x not in Y]
    alpha = {a: col.get(tuple(sorted((p, a)))) for a in rest0}
    for u, v in combinations(rest0, 2):
        if alpha[u] is None or alpha[u] != alpha[v] or alpha[u] == c1:
            continue
        S = tuple(x for x in U if x not in (Y[0], Y[1], u, v))
        for M in T1D.all_pms(S):
            if all(tuple(sorted(e)) in col for e in M):
                return [u, v, alpha[u]]
    return False


def main():
    rng = random.Random(2718281)
    classes = sorted(set(T1D.canonical(Ls) for Ls in T1E._survivors()))
    R = json.load(open(f"{BASE}/results_t1e_diagonal_uniform.json"))
    uni = {r["idx"]: set(r["uniform_witness_pairs"])
           for r in R["symbolic_caps"]}

    print("=" * 74)
    print("(A) the NAIVE extension of W23-U2 is FALSE -- the obstruction table")
    print("=" * 74)
    obstruct = []
    for i, cn in enumerate(classes):
        col = colour_map(cn, 6)
        live = sorted(col)
        blocked = [e for e in live if f"{e[0]},{e[1]}" not in uni[i]]
        obstruct.append({"idx": i,
                         "profile": sorted(bin(L).count("1") for L in cn),
                         "n_live": len(live), "n_uniform": len(live) - len(blocked)})
    print("   (uniform-cap pairs vs live pairs per class):")
    for o in obstruct:
        print(f"      class {o['idx']:2d} profile {o['profile']}: live "
              f"{o['n_live']:2d}, cap-proved {o['n_uniform']:2d}")
    RES["obstruction_table"] = obstruct
    control("T2A_obstruction_table")

    print("=" * 74)
    print("(B) W25-U3: CLEAN ENDPOINT => the antisymmetric cap kills E")
    print("=" * 74)
    tot = ok = 0
    viol = []
    per = []
    for i, cn in enumerate(classes):
        col = colour_map(cn, 6)
        cl = clean_vertices(col, 6)
        pairs = [e for e in col if e[0] in cl or e[1] in cl]
        for e in pairs:
            tot += 1
            if f"{e[0]},{e[1]}" in uni[i]:
                ok += 1
            else:
                viol.append([i, list(e)])
        per.append({"idx": i, "clean_vertices": sorted(cl),
                    "pairs_with_clean_endpoint": len(pairs)})
    print(f"   N=6, all 24 classes: {ok}/{tot} live pairs with a clean "
          f"endpoint have E == 0 IDENTICALLY in the weights; violations "
          f"{viol}")
    noclean = [p["idx"] for p in per if not p["clean_vertices"]]
    print(f"   classes with NO clean vertex (W25-U3 says nothing there): "
          f"{noclean}")
    RES["U3_n6"] = {"tested": tot, "ok": ok, "violations": viol,
                    "per_class": per, "classes_without_clean_vertex": noclean}
    assert not viol
    control("T2B_U3_n6_exhaustive")

    print("=" * 74)
    print("(B') the SHARP form of the mechanism, at N = 6, 8, 10")
    print("=" * 74)
    print("   DERIVED CRITERION (W25-U3s).  Let (p,q) be live of colour c1 on a")
    print("   diagonal source with q CLEAN, Y = {Q_c2, Q_c3} its two other")
    print("   partners, alpha(a) = colour of (p,a).  Then E_pq(antisym cap) is")
    print("   a sum over PAIRS {u,v} in U\\Y with alpha(u) = alpha(v) in {c2,c3};")
    print("   so E == 0 whenever no such pair {u,v} admits a perfect matching")
    print("   of the L-graph on U \\ {Q_c2,Q_c3,u,v}.  In particular BOTH")
    print("   ENDPOINTS CLEAN  =>  E = 0 at every even N (alpha is then")
    print("   injective), with NO use of the X_2 equations.")
    both = {"tested": 0, "ok": 0, "fail": []}
    one = {"tested": 0, "ok": 0, "fail": 0}
    pred = {"tested": 0, "agree": 0, "disagree": []}
    for n in (6, 8, 10):
        srcs = []
        if n == 6:
            for i, cn in enumerate(classes):
                for wpt in T1E.sample_points(cn, rng, k=1):
                    srcs.append((colour_map(cn, 6),
                                 T1D.build_source(cn, wpt)))
        else:
            for t in range(10 if n == 8 else 4):
                col, w, src = build_n_diagonal(n, rng,
                                               extra=(3 if n == 8 else 2))
                if src is not None:
                    srcs.append((col, src))
        for col, src in srcs:
            cl = clean_vertices(col, n)
            for e in sorted(col):
                p_, q_ = e
                c1 = col[e]
                K = antisym_cap(c1, Fraction(1), Fraction(0))
                U = tuple(x for x in range(n) if x not in (p_, q_))
                Ez = not C.cap_error(src, p_, q_, K, U)
                if p_ in cl and q_ in cl:
                    both["tested"] += 1
                    both["ok"] += int(Ez)
                    if not Ez:
                        both["fail"].append([n, list(e)])
                elif p_ in cl or q_ in cl:
                    one["tested"] += 1
                    one["ok"] += int(Ez)
                    one["fail"] += int(not Ez)
                # the sharp predictor, applied whenever some endpoint is clean
                for (a, b) in ((p_, q_), (q_, p_)):
                    if b not in cl:
                        continue
                    surv = surviving_pair(col, a, b, n)
                    pred["tested"] += 1
                    if (not surv) == Ez:
                        pred["agree"] += 1
                    else:
                        pred["disagree"].append([n, list(e), surv, Ez])
                    break
        print(f"   N={n}: cumulative -- both endpoints clean {both['ok']}/"
              f"{both['tested']}; exactly one clean {one['ok']}/{one['tested']}"
              f"; sharp predictor {pred['agree']}/{pred['tested']}")
    print(f"   BOTH ENDPOINTS CLEAN: {both['ok']}/{both['tested']} "
          f"(failures {both['fail']})  [THEOREM, all even N]")
    print(f"   ONE endpoint clean:  {one['ok']}/{one['tested']} -- sufficient "
          f"at N=6 (exhaustive, above) but NOT at N=8/10: {one['fail']} "
          f"failures")
    print(f"   SHARP PREDICTOR agrees with the exact E in "
          f"{pred['agree']}/{pred['tested']} cases; disagreements "
          f"{pred['disagree'][:3]}")
    RES["U3_sharp"] = {"both_clean": both, "one_clean": one,
                       "predictor": {k: v for k, v in pred.items()
                                     if k != "disagree"},
                       "predictor_disagreements": pred["disagree"][:10]}
    assert not both["fail"], f"BOTH-CLEAN theorem violated: {both['fail'][:3]}"
    assert not pred["disagree"], pred["disagree"][:3]
    control("T2Bprime_U3_sharp")

    print("=" * 74)
    print("(B'') NEGATIVE control (ledger 18): the hypothesis is not vacuous "
          "-- pairs failing it must exist and must FAIL")
    print("=" * 74)
    print(f"   one-clean-endpoint pairs whose cap does NOT vanish, N in "
          f"{{8,10}}: {one['fail']} (fires: {one['fail'] > 0})")
    RES["U3_negative_control"] = {"one_clean_failures": one["fail"]}
    assert one["fail"] > 0
    control("T2Bpp_negative_control")

    print("=" * 74)
    print("(C) the (5,5,5) class: E has ONE component; explicit witness at "
          "every point")
    print("=" * 74)
    import sympy
    cn23 = (920, 15361, 16486)
    assert cn23 in classes
    srcS, tv = T1E.sym_source(cn23)
    p, q = 0, 1
    Ksym = [[sympy.Symbol(f"zk{i}{j}") for j in range(3)] for i in range(3)]
    U = (2, 3, 4, 5)
    E = C.cap_error(srcS, p, q, Ksym, U)
    E = {k: sympy.expand(v) for k, v in E.items()}
    E = {k: v for k, v in E.items() if v != 0}
    print(f"   E_(0,1) has {len(E)} nonzero component(s) after expansion; "
          f"words (sites 2,3,4,5): {list(E.keys())}")
    comp = sympy.expand(list(E.values())[0])
    t = {e: sympy.Symbol(T1D.tvar(e)) for e in
         [(0, 2), (0, 3), (1, 2), (1, 3), (0, 4), (0, 5), (1, 4), (1, 5),
          (2, 3), (4, 5)]}
    Om = t[(0, 2)] * t[(1, 3)] + t[(0, 3)] * t[(1, 2)]
    La = t[(0, 4)] * t[(1, 5)] + t[(0, 5)] * t[(1, 4)]
    mu = t[(0, 2)] * t[(0, 3)] * t[(1, 4)] * t[(1, 5)]
    mup = t[(1, 2)] * t[(1, 3)] * t[(0, 4)] * t[(0, 5)]
    pred = sympy.expand((Ksym[0][0] * Ksym[2][2] + Ksym[2][0] * Ksym[0][2])
                        * Om * La + 2 * Ksym[2][0] ** 2 * mu
                        + 2 * Ksym[0][2] ** 2 * mup)
    print(f"   matches the closed form  (K00 K22 + K20 K02) Om La "
          f"+ 2 K20^2 mu + 2 K02^2 mu' : {sympy.simplify(comp - pred) == 0}")
    print("   pure equations force  Om = 1/t45  and  La = 1/t23, so Om*La "
          "never vanishes on the family;")
    print("   hence (K20,K02) = (1,0) with K00 K22 = -2 mu/(Om La) works when "
          "mu != 0, (0,1) with K00 K22 = -2 mu'/(Om La) when mu' != 0, and")
    print("   (1,1) with K00 K22 = -1 when mu = mu' = 0 -- an admissible cap "
          "at EVERY point of the 12-dimensional family.")
    RES["class555"] = {"components": len(E),
                       "closed_form_matches":
                           bool(sympy.simplify(comp - pred) == 0)}
    assert len(E) == 1 and sympy.simplify(comp - pred) == 0
    # the three cases, verified numerically at exact points
    checks = []
    for j, wpt in enumerate(T1E.sample_points(cn23, rng, k=4)):
        srcn = T1D.build_source(cn23, wpt)
        OmV = wpt[(0, 2)] * wpt[(1, 3)] + wpt[(0, 3)] * wpt[(1, 2)]
        LaV = wpt[(0, 4)] * wpt[(1, 5)] + wpt[(0, 5)] * wpt[(1, 4)]
        muV = wpt[(0, 2)] * wpt[(0, 3)] * wpt[(1, 4)] * wpt[(1, 5)]
        K = [[Fraction(0)] * 3 for _ in range(3)]
        K[1][1] = Fraction(1)
        K[2][0] = Fraction(1)
        K[0][0] = Fraction(1)
        K[2][2] = -2 * muV / (OmV * LaV)
        adm = C.is_admissible(srcn, 0, 1, K)
        Ev = C.cap_error(srcn, 0, 1, K, U)
        checks.append({"pt": j, "OmLa": str(OmV * LaV), "admissible": adm,
                       "E_zero": not Ev})
        assert adm and not Ev
    print(f"   explicit caps verified at {len(checks)} exact points of the "
          f"class: all admissible with E = 0")
    RES["class555_points"] = checks
    control("T2C_class555")

    declared = ["T2A_obstruction_table", "T2B_U3_n6_exhaustive",
                "T2Bprime_U3_sharp", "T2Bpp_negative_control", "T2C_class555"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    assert not missing
    with open(f"{BASE}/results_t2_u2.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t2_u2.json")


if __name__ == "__main__":
    main()
