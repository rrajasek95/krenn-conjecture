#!/usr/bin/env python3
"""UNAUDITED PROBE -- W5 task A: THE SCALAR MONOCHROME-SLICE THEORY.

Pinned HEAD: 181a4c084a91f1518c2bdfe2f574b9a7df1b1830

Question (Lemma J.1b, scalar half).  For a single scalar weighting w on K_8
(h = 3) with haf(w) = 1 -- the monochrome PURE normalisation -- can the
clean-cap slice error E_pq be nonvanishing at every one of the 28 pairs?

Blocks:
  A0  identity controls (three evaluators; P1 cross-check; multilinearity;
      the exact contraction identity (16); gauge covariance).
  A1  the closed form and its consequences (support criterion, positivity).
  A2  genericity census: how many of the 28 pairs are slice-clean?
  A3  the gauge theorem => an EXPLICIT exact witness: haf(w) = 1, every
      w_pq != 0, and all 28 slice errors nonzero.  (Scalar J.1b is FALSE.)
  A4  the identity hunt: (i) an explicit invariant-space search for a sum
      rule sum_pq c_pq E_pq = f(haf, minors); (ii) the DEFINITIVE test --
      the Jacobian rank of w |-> (haf, E_1, ..., E_28).

Run: python3 run_a_scalar_theory.py [--samples 40]
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from fractions import Fraction
from itertools import combinations

import slice_core as sc
from slice_core import ekey, haf, require

B8 = tuple(range(8))
B6 = tuple(range(6))
PAIRS8 = list(combinations(B8, 2))
PAIRS6 = list(combinations(B6, 2))
P1DIR = ("/Users/rishi/workplace/krenn-conjecture/computations/"
         "unaudited-witness-splitting-p1-2026-08-15")


def U_of(pair, sites=B8):
    return tuple(a for a in sites if a not in pair)


def slice_errors(w, sites=B8):
    return {e: sc.slice_error(w, e[0], e[1], U_of(e, sites))
            for e in combinations(sites, 2)}


# ------------------------------------------------------------ exact rank / LA


def rank_exact(rows, ncols):
    mat = [[Fraction(c) for c in row] for row in rows]
    rank = 0
    piv = 0
    for col in range(ncols):
        sel = None
        for i in range(piv, len(mat)):
            if mat[i][col]:
                sel = i
                break
        if sel is None:
            continue
        mat[piv], mat[sel] = mat[sel], mat[piv]
        pr = mat[piv]
        for i in range(piv + 1, len(mat)):
            if mat[i][col]:
                f = mat[i][col] / pr[col]
                mat[i] = [a - f * b for a, b in zip(mat[i], pr)]
        piv += 1
        rank += 1
        if piv == len(mat):
            break
    return rank


def nullspace(rows, ncols):
    mat = [[Fraction(c) for c in row] for row in rows]
    pivots = []
    r = 0
    for col in range(ncols):
        sel = None
        for i in range(r, len(mat)):
            if mat[i][col]:
                sel = i
                break
        if sel is None:
            continue
        mat[r], mat[sel] = mat[sel], mat[r]
        inv = Fraction(1, 1) / mat[r][col]
        mat[r] = [v * inv for v in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][col]:
                f = mat[i][col]
                mat[i] = [a - f * b for a, b in zip(mat[i], mat[r])]
        pivots.append(col)
        r += 1
        if r == len(mat):
            break
    basis = []
    for fc in [c for c in range(ncols) if c not in pivots]:
        vec = [Fraction(0)] * ncols
        vec[fc] = Fraction(1)
        for i, pc in enumerate(pivots):
            vec[pc] = -mat[i][fc]
        basis.append(vec)
    return r, basis


# ------------------------------------------------------------------ A0 controls


def block_a0(rng, out):
    print("== A0  identity controls ==")
    checks = {}

    # I1: three independent evaluators agree, h = 2 and h = 3, dense+sparse.
    n = 0
    for sites in (B8, B6):
        for zp in (None, 0.35, 0.6):
            for _ in range(12):
                w = sc.random_weighting(rng, sites, -6, 6, zp)
                for p, q in combinations(sites, 2):
                    U = U_of((p, q), sites)
                    d = sc.slice_error_direct(w, p, q, U)
                    r2 = sc.slice_error_rank2(w, p, q, U)
                    require(d == r2, ("evaluator 1 != 3", p, q, d, r2))
                    if w[ekey(p, q)] != 0:
                        c2 = sc.slice_error_contract(w, p, q, U)
                        require(d == c2, ("evaluator 1 != 2", p, q, d, c2))
                    n += 1
    checks["I1_evaluators_agree_pairs"] = n
    print(f"  I1 three evaluators agree on {n} (weighting, pair) instances")

    # I2: the scalar slice error IS the K_cc^3-coefficient of E_{c^6} in the
    #     ternary h=3 machinery of the P1 probe (independent implementation).
    if P1DIR not in sys.path:
        sys.path.insert(0, P1DIR)
    import wsplit_core as p1core          # noqa: E402
    hits = 0
    for _ in range(6):
        src = p1core.random_source(rng)
        for c in (0, 1, 2):
            w = sc.monochrome_slice(src, c)
            row = p1core.error_row(src, (c,) * 6)
            key = tuple(sorted((p1core.kidx(c, c),) * 3))
            require(row.get(key, 0)
                    == sc.slice_error(w, 0, 1, tuple(range(2, 8))),
                    ("I2 mismatch", c))
            hits += 1
    checks["I2_p1_crosschecks"] = hits
    print(f"  I2 scalar E^(c) == coeff of K_cc^3 in E_(c^6): {hits}/{hits} "
          f"(P1 wsplit_core.error_row)")

    # I3: E_pq and haf are MULTILINEAR (square-free) in the 28 edge variables.
    ml = 0
    for _ in range(4):
        w = sc.random_weighting(rng, B8)
        for e in PAIRS8:
            w0 = sc.set_edge(w, e, 0)
            for target in (haf, ):
                require(target(w, B8)
                        == target(w0, B8) + w[e] * sc.partial(
                            lambda z: haf(z, B8), w, e), "haf not multilinear")
            for pair in [(0, 1), (2, 5), (4, 7)]:
                U = U_of(pair)
                f = (lambda z, pr=pair, UU=U:
                     sc.slice_error_direct(z, pr[0], pr[1], UU))
                require(f(w) == f(w0) + w[e] * sc.partial(f, w, e),
                        ("E not multilinear", e, pair))
                ml += 1
    checks["I3_multilinearity_checks"] = ml
    print(f"  I3 multilinearity of haf and E in every edge variable: "
          f"{ml} checks pass")

    # I4: gauge covariance.  Scaling every edge at site a by lam multiplies
    #     haf by lam and E_pq by lam^3 (a in {p,q}) or lam (a in U).
    lam = Fraction(7, 3)
    gauge = []
    for _ in range(3):
        w = sc.random_weighting(rng, B8)
        for a in B8:
            wl = dict(w)
            for b in B8:
                if b != a:
                    wl[ekey(a, b)] = Fraction(w[ekey(a, b)]) * lam
            require(haf(wl, B8) == lam * haf(w, B8), "haf gauge")
            for pair in PAIRS8:
                U = U_of(pair)
                e0 = sc.slice_error(w, pair[0], pair[1], U)
                e1 = sc.slice_error(wl, pair[0], pair[1], U)
                power = 3 if a in pair else 1
                require(e1 == lam ** power * e0, ("E gauge", a, pair))
            gauge.append(a)
    checks["I4_gauge_sites_checked"] = len(gauge)
    print("  I4 gauge covariance: haf -> lam*haf, E_pq -> lam^{3 or 1} E_pq "
          f"({len(gauge)} site scalings, all 28 pairs)")

    # I5: eq. (16): E_pq = 0  <=>  haf_U(x + r/s) = haf_B(w)/s   (s != 0).
    iff = 0
    for _ in range(30):
        w = sc.random_weighting(rng, B8, -3, 3)
        for pair in PAIRS8:
            s = w[ekey(*pair)]
            if s == 0:
                continue
            U = U_of(pair)
            rr = {ekey(a, b): w[ekey(pair[0], a)] * w[ekey(pair[1], b)]
                  + w[ekey(pair[0], b)] * w[ekey(pair[1], a)]
                  for a, b in combinations(U, 2)}
            y = {e: Fraction(w[e]) + Fraction(rr[e], s) for e in rr}
            lhs = sc.slice_error(w, pair[0], pair[1], U) == 0
            rhs = haf(y, U) == Fraction(haf(w, B8), s)
            require(lhs == rhs, ("I5 failed", pair))
            iff += 1
    checks["I5_contraction_iff"] = iff
    print(f"  I5 contraction identity (16) as an iff: {iff} pair instances")
    out["A0_controls"] = checks


# ------------------------------------------------------- A1 the closed form


def block_a1(rng, out):
    print("== A1  closed form, support criterion, positivity ==")
    rec = {}
    # Closed form (evaluator 3) is the statement
    #   E_pq = sum_{k=2}^h s^{h-k} k! sum_{|S|=2k} e_{S,k}(u,v) haf(w|_{U\S}),
    # verified in A0/I1.  Two immediate corollaries, checked here.

    # (a) SUPPORT CRITERION: if |supp(w_p.) cap U| <= 1 or |supp(w_q.)| <= 1
    #     then E_pq = 0 identically.  More sharply E_pq = 0 whenever no two
    #     disjoint "attachments" exist.
    hits = 0
    for _ in range(40):
        w = sc.random_weighting(rng, B8, -4, 4)
        p, q = 0, 1
        U = U_of((p, q))
        keep = rng.choice(U)
        wk = dict(w)
        for a in U:
            if a != keep:
                wk[ekey(p, a)] = 0
        require(sc.slice_error(wk, p, q, U) == 0, "support criterion (p)")
        wk2 = dict(w)
        for a in U:
            if a != keep:
                wk2[ekey(q, a)] = 0
        require(sc.slice_error(wk2, p, q, U) == 0, "support criterion (q)")
        hits += 2
    rec["support_criterion_checks"] = hits
    print(f"  degree(p in colour slice) <= 1  =>  E_pq = 0: {hits} checks")

    # (b) POSITIVITY: E = sum_k s^{h-k} haf(clone_k)/k! is a positive
    #     combination of monomials, so w >= 0 => E >= 0 and w > 0 => E > 0.
    pos = {"nonneg": 0, "strict": 0}
    for _ in range(20):
        w = {e: rng.randint(0, 5) for e in PAIRS8}
        for pair in PAIRS8:
            val = sc.slice_error(w, pair[0], pair[1], U_of(pair))
            require(val >= 0, ("positivity", pair, val))
            pos["nonneg"] += 1
        wp = {e: rng.randint(1, 5) for e in PAIRS8}
        for pair in PAIRS8:
            val = sc.slice_error(wp, pair[0], pair[1], U_of(pair))
            require(val > 0, ("strict positivity", pair, val))
            pos["strict"] += 1
    rec["positivity"] = pos
    print(f"  w >= 0 => E_pq >= 0 ({pos['nonneg']} checks); "
          f"w > 0 => E_pq > 0 ({pos['strict']} checks): cleanliness needs "
          f"cancellation or support collapse")

    # (c) the h=2 specialisation: E_pq = 2 e_{U,2}(u,v); INDEPENDENT of
    #     w_pq and of the internal edges of U.
    indep = 0
    for _ in range(20):
        w = sc.random_weighting(rng, B6, -5, 5)
        for pair in PAIRS6:
            U = U_of(pair, B6)
            u = {a: w[ekey(pair[0], a)] for a in U}
            v = {a: w[ekey(pair[1], a)] for a in U}
            base = sc.slice_error(w, pair[0], pair[1], U)
            require(base == 2 * sc.elem_uv(u, v, U, 2), "h=2 closed form")
            w2 = dict(w)
            w2[ekey(*pair)] = w[ekey(*pair)] + 17
            for a, b in combinations(U, 2):
                w2[ekey(a, b)] = w[ekey(a, b)] - 5
            require(sc.slice_error(w2, pair[0], pair[1], U) == base,
                    "h=2 independence")
            indep += 1
    rec["h2_closed_form_checks"] = indep
    print(f"  h=2: E_pq = 2 e_(U,2)(u,v), independent of w_pq and of w|_U "
          f"({indep} checks)")
    out["A1_closed_form"] = rec


# --------------------------------------------------------- A2 the census


def block_a2(rng, out, samples):
    print("== A2  genericity census: clean pairs per weighting ==")
    families = {
        "dense int [-6,6]": lambda: sc.random_weighting(rng, B8, -6, 6),
        "dense int [-40,40]": lambda: sc.random_weighting(rng, B8, -40, 40),
        "sparse 35% zeros": lambda: sc.random_weighting(rng, B8, -6, 6, 0.35),
        "sparse 60% zeros": lambda: sc.random_weighting(rng, B8, -6, 6, 0.6),
        "positive int [1,6]": lambda: {e: rng.randint(1, 6) for e in PAIRS8},
        "0/1": lambda: {e: rng.randint(0, 1) for e in PAIRS8},
    }
    rec = {}
    for name, gen in families.items():
        hist = {}
        haf_nonzero = 0
        by_support = 0
        by_cancel = 0
        for _ in range(samples):
            w = gen()
            if haf(w, B8) == 0:
                continue
            haf_nonzero += 1
            wn = sc.normalize_haf(w, B8)
            require(haf(wn, B8) == 1, "normalisation")
            clean = 0
            for pair in PAIRS8:
                U = U_of(pair)
                if sc.slice_error(wn, pair[0], pair[1], U) == 0:
                    clean += 1
                    if sc.slice_error_abs(wn, pair[0], pair[1], U) == 0:
                        by_support += 1
                    else:
                        by_cancel += 1
            hist[clean] = hist.get(clean, 0) + 1
        rec[name] = {"samples_with_haf_nonzero": haf_nonzero,
                     "clean_pair_histogram": hist,
                     "clean_by_support": by_support,
                     "clean_by_cancellation": by_cancel}
        print(f"  {name:22s} haf!=0 {haf_nonzero:3d}  clean-pair histogram "
              f"{dict(sorted(hist.items()))}  (support {by_support}, "
              f"cancellation {by_cancel})")
    out["A2_census"] = rec


# ------------------------------------------------------ A3 the exact witness


def block_a3(rng, out):
    print("== A3  explicit exact witness: haf = 1, all 28 pairs DIRTY ==")
    found = None
    for _ in range(400):
        w = sc.random_weighting(rng, B8, -6, 6)
        if haf(w, B8) == 0:
            continue
        if any(w[e] == 0 for e in PAIRS8):
            continue
        wn = sc.normalize_haf(w, B8)
        errs = slice_errors(wn)
        if all(v != 0 for v in errs.values()):
            found = (wn, errs)
            break
    require(found is not None, "no all-dirty witness found")
    wn, errs = found
    rec = {"weighting": {f"{a}-{b}": str(wn[(a, b)]) for a, b in PAIRS8},
           "haf": str(haf(wn, B8)),
           "all_w_pq_nonzero": all(wn[e] != 0 for e in PAIRS8),
           "slice_errors": {f"{a}-{b}": str(errs[(a, b)]) for a, b in PAIRS8},
           "n_dirty": sum(1 for v in errs.values() if v != 0)}
    print(f"  witness found: haf = {rec['haf']}, all 28 w_pq != 0, "
          f"{rec['n_dirty']}/28 pairs dirty")
    print("  => the SCALAR half of J.1b is FALSE: a hafnian-normalised "
          "scalar weighting can be slice-dirty at every pair.")
    out["A3_witness"] = rec


# ------------------------------------------------------- A4 the identity hunt


def invariants(w):
    """S_8-invariant, torus-weight-(3,...,3), degree-12 quantities."""
    H = haf(w, B8)
    C = {e: sc.cofactor(w, B8, *e) for e in PAIRS8}
    E = slice_errors(w)
    wc = {e: w[e] * C[e] for e in PAIRS8}
    w2 = {e: w[e] * w[e] for e in PAIRS8}
    Q = {e: haf(w2, U_of(e)) for e in PAIRS8}          # haf of squared entries
    R = {}
    for e in PAIRS8:                                   # sum of squared matchings
        R[e] = sum(v * v for v in [
            haf(w, U_of(e))])
    inv = {
        "H^3": H ** 3,
        "sum_pq C^2 E": sum(C[e] ** 2 * E[e] for e in PAIRS8),
        "sum_pq Q E": sum(Q[e] * E[e] for e in PAIRS8),
        "sum_pq (w C)^3": sum(wc[e] ** 3 for e in PAIRS8),
        "H * sum_pq (w C)^2": H * sum(wc[e] ** 2 for e in PAIRS8),
        "H * sum_pq w^2 C Cbar": H * sum(
            w[e] ** 2 * C[e] * haf(w, U_of(e)) for e in PAIRS8),
        "sum_pq w^3 C^2 Cbar": sum(
            w[e] ** 3 * C[e] ** 2 * haf(w, U_of(e)) for e in PAIRS8),
        "H * sum_{e<f disjoint} (wC)_e (wC)_f": H * sum(
            wc[e] * wc[f] for e, f in combinations(PAIRS8, 2)
            if not set(e) & set(f)),
        "H * sum_{e<f meeting} (wC)_e (wC)_f": H * sum(
            wc[e] * wc[f] for e, f in combinations(PAIRS8, 2)
            if set(e) & set(f)),
        "sum_pq C^2 E over full-support pairs only": sum(
            C[e] ** 2 * E[e] for e in PAIRS8 if w[e] != 0),
    }
    del R
    return inv


def block_a4(rng, out, points):
    print("== A4  the identity hunt ==")
    rec = {}

    # (i) invariant-space search.
    rows = []
    names = None
    for _ in range(points):
        w = sc.random_weighting(rng, B8, -5, 5)
        inv = invariants(w)
        if names is None:
            names = list(inv)
        rows.append([inv[n] for n in names])
    rank, basis = nullspace(rows, len(names))
    rels = []
    for vec in basis:
        rel = {names[i]: str(vec[i]) for i in range(len(names)) if vec[i]}
        rels.append(rel)
    involves_E = [r for r in rels
                  if any("E" in k for k in r) and len(r) > 1]
    rec["invariant_search"] = {"names": names, "points": points,
                               "rank": rank, "relations": rels,
                               "relations_involving_E": involves_E}
    print(f"  (i) span of {len(names)} invariants at {points} random points: "
          f"rank {rank}; {len(rels)} relations")
    for r in rels:
        print(f"      {r}")
    print(f"      relations that couple sum(C^2 E) to haf-data: "
          f"{len(involves_E)}")

    # (ii) the DEFINITIVE test: Jacobian of w -> (haf, E_1, ..., E_28).
    #      All 29 functions are multilinear, so d/dw_e is exact and cheap.
    jac_rank = []
    for _ in range(3):
        w = sc.random_weighting(rng, B8, -9, 9)
        grad_h = [sc.partial(lambda z: haf(z, B8), w, e) for e in PAIRS8]
        rows_e = []
        for pair in PAIRS8:
            U = U_of(pair)
            f = (lambda z, pr=pair, UU=U:
                 sc.slice_error_direct(z, pr[0], pr[1], UU))
            rows_e.append([sc.partial(f, w, e) for e in PAIRS8])
        r_e = rank_exact(rows_e, 28)
        r_all = rank_exact([grad_h] + rows_e, 28)
        # rank of dE restricted to the tangent space of {haf = const}
        _, ker = nullspace([grad_h], 28)
        restricted = [[sum(row[i] * k[i] for i in range(28)) for k in ker]
                      for row in rows_e]
        r_restricted = rank_exact(restricted, len(ker))
        # the UNIQUE linear dependency among the 29 covectors
        # (dE_1, ..., dE_28, d haf): the infinitesimal sum rule.
        cols = rows_e + [grad_h]
        T = [[cols[i][j] for i in range(29)] for j in range(28)]
        rr, kbasis = nullspace(T, 29)
        entry = {"rank_dE": r_e, "rank_dE_and_dhaf": r_all,
                 "rank_dE_on_T{haf=1}": r_restricted,
                 "dim_T{haf=1}": len(ker),
                 "covector_rank": rr, "dependency_dim": len(kbasis)}
        if len(kbasis) == 1:
            lam = kbasis[0]
            mu = lam[28]
            entry["mu_haf_coefficient_zero"] = (mu == 0)
            entry["all_lambda_nonzero"] = all(lam[i] != 0 for i in range(28))
            # does lambda have a closed form?  the torus grading forces
            # weight(lambda_pq) = (-2 at p, -2 at q, 0 on U); test the
            # candidates of that weight.
            C = {e: sc.cofactor(w, B8, *e) for e in PAIRS8}
            Ev = slice_errors(w)
            cand = {
                "lambda * w_pq^2": [lam[i] * w[PAIRS8[i]] ** 2
                                    for i in range(28)],
                "lambda * C_pq^2": [lam[i] * C[PAIRS8[i]] ** 2
                                    for i in range(28)],
                "lambda * w_pq C_pq": [lam[i] * w[PAIRS8[i]] * C[PAIRS8[i]]
                                       for i in range(28)],
                "lambda * E_pq": [lam[i] * Ev[PAIRS8[i]] for i in range(28)],
            }
            entry["closed_form_probe"] = {
                name: (len(set(vals)) == 1) for name, vals in cand.items()}
        jac_rank.append(entry)
        print(f"  (ii) Jacobian at a random point: rank d(E) = {r_e}/28, "
              f"rank d(haf,E) = {r_all}/28, "
              f"rank dE on T(haf=1) = {r_restricted}/{len(ker)}")
        print(f"       unique dependency: dim {len(kbasis)}, all 28 lambda_pq "
              f"nonzero = {entry.get('all_lambda_nonzero')}, "
              f"closed-form probe {entry.get('closed_form_probe')}")
    rec["jacobian"] = jac_rank
    out["A4_identity_hunt"] = rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=40)
    ap.add_argument("--points", type=int, default=24)
    args = ap.parse_args()
    rng = random.Random(20260815)
    out = {"note": "UNAUDITED PROBE W5 task A",
           "head": "181a4c084a91f1518c2bdfe2f574b9a7df1b1830"}
    block_a0(rng, out)
    block_a1(rng, out)
    block_a2(rng, out, args.samples)
    block_a3(rng, out)
    block_a4(rng, out, args.points)
    with open("results_a_scalar.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=str)
    print("wrote results_a_scalar.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
