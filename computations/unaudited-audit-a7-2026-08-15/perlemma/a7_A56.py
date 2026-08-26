#!/usr/bin/env python3
"""A7 SUB-AUDIT -- ITEM A5 (hidden hypotheses) and A6 (Lemma W20-P4c).

A5 asks, adversarially:
  (1) does LEMMA W20-P need characteristic 0?
  (2) does it need the hyperplanes to pass through the ORIGIN?
  (3) is "coordinate hyperplane" really {x : x_k = 0} for a single fixed k,
      and must the SAME k serve all n hyperplanes?  (and: does a common
      NON-coordinate hyperplane work?)

A6 audits, as stated in w20_c8rank.check_P4c:
  LEMMA W20-P4c.  Let u in C^4 have ALL FOUR coordinates nonzero and let
  V_1,V_2,V_3 be hyperplanes through the origin of C^4.  Then
      per(u, v^1, v^2, v^3)  is NOT identically zero on V_1 x V_2 x V_3.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations_with_replacement, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from a7_core import (per, kernel_basis, kernel_basis_modp,          # noqa: E402
                     is_common_coordinate, per_vanishes_on_product,
                     sign_reps)


# ------------------------------------------------------------ GF(p) tools --
def proj_points(n, p):
    """one normal per hyperplane of F_p^n: vectors whose first nonzero
    coordinate is 1 -- exactly the points of P^{n-1}(F_p)."""
    out = []
    for v in product(range(p), repeat=n):
        nz = [i for i in range(n) if v[i]]
        if nz and v[nz[0]] == 1:
            out.append(v)
    return out


def per_vanishes_modp(bases, p):
    n = len(bases)
    for cs in ((1, 2, 3, 4, 5, 6), (1, 3, 4, 9, 2, 5)):
        pt = []
        for j in range(n):
            B = bases[j]
            pt.append([sum(cs[k] * B[k][i] for k in range(len(B))) % p
                       for i in range(len(B[0]))])
        if per(pt) % p:
            return False
    for idx in product(*[range(len(b)) for b in bases]):
        if per([bases[j][idx[j]] for j in range(n)]) % p:
            return False
    return True


def sweep_modp(n, p, limit_random=None, seed=5):
    cand = proj_points(n, p)
    bases = [kernel_basis_modp(nv, p) for nv in cand]
    tested = 0
    vanishing = []
    violations = []
    if limit_random is None:
        it = combinations_with_replacement(range(len(cand)), n)
    else:
        rng = random.Random(seed)
        it = (tuple(sorted(rng.randrange(len(cand)) for _ in range(n)))
              for _ in range(limit_random))
    for combo in it:
        tested += 1
        if per_vanishes_modp([bases[k] for k in combo], p):
            normals = [cand[k] for k in combo]
            vanishing.append([list(x) for x in normals])
            if not is_common_coordinate(normals):
                violations.append([list(x) for x in normals])
    return dict(n=n, p=p, n_hyperplanes=len(cand), exhaustive=(limit_random is None),
                n_tested=tested, n_vanishing=len(vanishing),
                n_violations=len(violations), violations=violations[:6],
                vanishing_sample=vanishing[:3])


# ------------------------------------------------------------ affine test --
def affine_vanishes(normals, consts):
    """per == 0 identically on prod_j {x : <nv_j,x> = c_j}.

    per(p_1+w_1,...,p_n+w_n) is multilinear; splitting each column into its
    base point and its direction, the identity holds iff per vanishes on
    every tuple whose j-th entry is either the base point p_j or one of the
    n-1 basis directions of ker(nv_j)."""
    n = len(normals)
    opts = []
    for nv, c in zip(normals, consts):
        piv = max(i for i in range(n) if nv[i])
        p0 = [Fraction(0)] * n
        p0[piv] = Fraction(c, nv[piv])
        opts.append([p0] + [[Fraction(x) for x in b]
                            for b in kernel_basis(nv)])
    for pick in product(*[range(len(o)) for o in opts]):
        if per([opts[j][pick[j]] for j in range(n)]):
            return False
    return True


def affine_sweep(n=3, vals=(-1, 0, 1), consts=(0, 1)):
    cand = [v for v in product(vals, repeat=n) if any(v)]
    out = []
    tested = 0
    for combo in combinations_with_replacement(
            [(nv, c) for nv in cand for c in consts], n):
        normals = [x[0] for x in combo]
        cs = [x[1] for x in combo]
        tested += 1
        if affine_vanishes(normals, cs):
            out.append(dict(normals=[list(x) for x in normals], consts=cs,
                            all_through_origin=all(c == 0 for c in cs),
                            is_common_coordinate=is_common_coordinate(normals)))
    genuinely_affine = [o for o in out if not o["all_through_origin"]]
    return dict(n=n, n_tested=tested, n_vanishing=len(out),
                n_vanishing_with_a_translated_hyperplane=len(genuinely_affine),
                affine_witnesses=genuinely_affine[:8],
                linear_vanishing_sample=[o for o in out
                                         if o["all_through_origin"]][:6])


# -------------------------------------------------------- coordinate-k Q ---
def coordinate_k_probes():
    out = {}
    def e(n, k):
        v = [0] * n
        v[k] = 1
        return tuple(v)
    for n in (3, 4, 5):
        rec = {}
        same = [e(n, 0)] * n
        rec["all_same_coordinate_k0_vanishes"] = per_vanishes_on_product(
            [kernel_basis(x) for x in same])
        mixed = [e(n, i % n) for i in range(n)]     # all different k
        rec["all_different_coordinates_vanishes"] = per_vanishes_on_product(
            [kernel_basis(x) for x in mixed])
        wit = None
        if not rec["all_different_coordinates_vanishes"]:
            bs = [kernel_basis(x) for x in mixed]
            for idx in product(*[range(len(b)) for b in bs]):
                cols = [bs[j][idx[j]] for j in range(n)]
                if per(cols):
                    wit = dict(normals=[list(x) for x in mixed],
                               vectors=[list(c) for c in cols],
                               per=per(cols))
                    break
        rec["different_k_witness"] = wit
        oneoff = [e(n, 0)] * (n - 1) + [e(n, 1)]
        rec["n_minus_1_same_one_different_vanishes"] = per_vanishes_on_product(
            [kernel_basis(x) for x in oneoff])
        allones = [tuple([1] * n)] * n              # a COMMON NON-coordinate
        rec["common_non_coordinate_hyperplane_vanishes"] = \
            per_vanishes_on_product([kernel_basis(x) for x in allones])
        gen = [tuple([1, 2] + [0] * (n - 2))] * n
        rec["common_non_coordinate_hyperplane2_vanishes"] = \
            per_vanishes_on_product([kernel_basis(x) for x in gen])
        out["n%d" % n] = rec
    return out


# ============================================================ A6: P4c ======
def p4c_vanishes(u, normals):
    """is per(u, v^1, ..., v^k) identically zero on prod ker(normals)?"""
    bases = [kernel_basis(nv) for nv in normals]
    for idx in product(*[range(len(b)) for b in bases]):
        if per([list(u)] + [bases[j][idx[j]] for j in range(len(bases))]):
            return False
    return True


def p4c_exhaustive(n=4):
    """u over an explicit all-nonzero stratum, (V_1,V_2,V_3) over ALL
    multisets of {-1,0,1} sign-representative normals."""
    cand = sign_reps(n)
    us = [u for u in product((1, -1), repeat=n) if u[0] == 1]
    us += [(1, 2, 3, 4), (1, 1, 2, 3), (2, -1, 3, -5), (1, -1, 1, 6),
           (6, 3, 2, 1)][:5 if n == 4 else 0]
    tested = 0
    bad = []
    for u in us:
        for combo in combinations_with_replacement(range(len(cand)), n - 1):
            tested += 1
            normals = [cand[k] for k in combo]
            if p4c_vanishes(u, normals):
                bad.append(dict(u=list(u),
                                normals=[list(x) for x in normals]))
    return dict(n=n, n_u=len(us), n_normal_multisets=len(list(
        combinations_with_replacement(range(len(cand)), n - 1))),
        n_tested=tested, n_vanishing_with_all_nonzero_u=len(bad),
        witnesses=bad[:6])


def p4c_random(n=4, trials=3000, seed=77):
    rng = random.Random(seed)
    tested = 0
    bad = []
    while tested < trials:
        u = tuple(Fraction(rng.randint(-9, 9) or 5, rng.randint(1, 6))
                  for _ in range(n))
        normals = [tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 6))
                         for _ in range(n)) for _ in range(n - 1)]
        if not all(any(x) for x in normals):
            continue
        tested += 1
        if p4c_vanishes(u, normals):
            bad.append(dict(u=[str(x) for x in u],
                            normals=[[str(x) for x in nv] for nv in normals]))
    return dict(n=n, trials=tested, n_vanishing=len(bad), witnesses=bad[:5])


def p4c_random_sparse(n=4, trials=3000, seed=78, pzero=0.3):
    rng = random.Random(seed)
    tested = 0
    bad = []
    while tested < trials:
        u = tuple(rng.randint(1, 9) * rng.choice((1, -1)) for _ in range(n))
        normals = [tuple(0 if rng.random() < pzero else rng.randint(-9, 9)
                         for _ in range(n)) for _ in range(n - 1)]
        if not all(any(x) for x in normals):
            continue
        tested += 1
        if p4c_vanishes(u, normals):
            bad.append(dict(u=list(u), normals=[list(x) for x in normals]))
    return dict(n=n, trials=tested, n_vanishing=len(bad), witnesses=bad[:5])


def p4c_mutation_controls():
    """the detector must FIRE where the statement is genuinely false."""
    out = {}
    # (M1) u with a ZERO coordinate: exhaustive over the same stratum, count
    #      how many configurations DO vanish (must be > 0).
    cand = sign_reps(4)
    fires = 0
    sample = []
    for u in [(0, 1, 1, 1), (0, 1, -1, 2), (1, 0, 2, 3)]:
        for combo in combinations_with_replacement(range(len(cand)), 3):
            normals = [cand[k] for k in combo]
            if p4c_vanishes(u, normals):
                fires += 1
                if len(sample) < 5:
                    sample.append(dict(u=list(u),
                                       normals=[list(x) for x in normals]))
    out["M1_zero_coordinate_u_vanishing_configs"] = fires
    out["M1_samples"] = sample
    out["M1_fires"] = fires > 0
    # (M2) n = 2 analogue is FALSE: u all-nonzero, one line.
    w = []
    for u in ((1, 1), (2, 3), (1, -5)):
        for nv in sign_reps(2):
            if p4c_vanishes(u, [nv]):
                w.append(dict(u=list(u), normal=list(nv),
                              line=[list(b) for b in kernel_basis(nv)]))
    out["M2_n2_analogue_false"] = dict(n_witnesses=len(w), witnesses=w[:4])
    # (M3) n = 3 analogue (two planes + all-nonzero u): claimed impossible.
    cand3 = sign_reps(3)
    bad3 = []
    for u in [u for u in product((1, -1), repeat=3) if u[0] == 1] + \
             [(1, 2, 3), (3, -1, 2)]:
        for combo in combinations_with_replacement(range(len(cand3)), 2):
            normals = [cand3[k] for k in combo]
            if p4c_vanishes(u, normals):
                bad3.append(dict(u=list(u),
                                 normals=[list(x) for x in normals]))
    out["M3_n3_analogue_vanishing_configs"] = len(bad3)
    out["M3_samples"] = bad3[:5]
    # (M4) characteristic 2: P4c FAILS (per = det in char 2).
    p = 2
    u = (1, 1, 1, 1)
    nv = (1, 1, 1, 1)
    bases = [kernel_basis_modp(nv, p)] * 3
    van = True
    for idx in product(*[range(len(b)) for b in bases]):
        if per([list(u)] + [bases[j][idx[j]] for j in range(3)]) % p:
            van = False
    out["M4_char2_P4c_fails"] = dict(u=list(u), normal=list(nv),
                                     vanishes_mod_2=van,
                                     reason="per == det in char 2 and u lies "
                                            "in ker(1,1,1,1) over F_2")
    return out


def lemma_char2_witness():
    """explicit char-2 refutation of LEMMA W20-P itself."""
    out = {}
    for n in (3, 4, 5):
        nv = tuple([1] * n)
        bases = [kernel_basis_modp(nv, 2)] * n
        van = per_vanishes_modp(bases, 2)
        out["n%d" % n] = dict(
            normals=[list(nv)] * n, vanishes_mod2=van,
            is_common_coordinate=is_common_coordinate([nv] * n),
            refutes_lemma=(van and not is_common_coordinate([nv] * n)))
    out["reason"] = ("in characteristic 2, per = det, so per vanishes on "
                     "V x ... x V for ANY single hyperplane V (n vectors in "
                     "an (n-1)-dimensional space are dependent)")
    return out


def main():
    res = {"_header": "A7 SUB-AUDIT -- A5 hidden hypotheses, A6 Lemma "
                      "W20-P4c.  Exact arithmetic only."}
    res["A5_char2_witness"] = lemma_char2_witness()
    print("A5 char-2 witness:", res["A5_char2_witness"], flush=True)
    res["A5_modp"] = {}
    for (n, p, lim) in [(3, 2, None), (3, 3, None), (3, 5, None),
                        (3, 7, None), (3, 11, None), (3, 13, None),
                        (4, 2, None), (4, 3, None), (4, 5, 200000),
                        (5, 2, None), (5, 3, 300000)]:
        k = "n%d_p%d" % (n, p)
        res["A5_modp"][k] = sweep_modp(n, p, lim)
        print("A5 GF(%d) n=%d:" % (p, n), res["A5_modp"][k], flush=True)
    res["A5_affine_n3"] = affine_sweep(3)
    print("A5 affine n=3:", json.dumps(res["A5_affine_n3"], indent=1,
                                       default=str)[:2500], flush=True)
    res["A5_coordinate_k"] = coordinate_k_probes()
    print("A5 coordinate-k:", res["A5_coordinate_k"], flush=True)

    res["A6_P4c_exhaustive"] = p4c_exhaustive(4)
    print("A6 P4c exhaustive:", res["A6_P4c_exhaustive"], flush=True)
    res["A6_P4c_random"] = p4c_random()
    print("A6 P4c random:", res["A6_P4c_random"], flush=True)
    res["A6_P4c_random_sparse"] = p4c_random_sparse()
    print("A6 P4c random sparse:", res["A6_P4c_random_sparse"], flush=True)
    res["A6_mutation_controls"] = p4c_mutation_controls()
    print("A6 mutation controls:", json.dumps(res["A6_mutation_controls"],
                                              indent=1, default=str)[:3000],
          flush=True)
    json.dump(res, open(os.path.join(HERE, "a7_results_A56.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
