#!/usr/bin/env python3
"""A7 SUB-AUDIT -- ITEM A, parts A1/A2/A3 of LEMMA W20-P.  Exact only.

STATEMENT AUDITED (recovered from w20_perlemma.py and restated in my words)

  LEMMA W20-P(n), n >= 3.  Let V_1,...,V_n be hyperplanes THROUGH THE ORIGIN
  in C^n, V_j = ker(nv_j), nv_j != 0.  Then

      per(v^1,...,v^n) = 0  for every (v^1,...,v^n) in V_1 x ... x V_n
   <=>
      there is a single coordinate r such that every nv_j is a nonzero
      multiple of e_r, i.e. all n hyperplanes are the SAME coordinate
      hyperplane {v_r = 0}.

  Here per is the permanent of the n x n matrix whose columns are the v^j.

A1  re-derivation of the two proof steps.
A2  my own exhaustive sweeps at n = 3 and n = 4.
A3  the two claimed counterexamples (n = 2; general proper subspaces).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations_with_replacement, permutations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from a7_core import (per, per_bruteforce, kernel_basis, is_common_coordinate,  # noqa: E402
                     per_vanishes_on_product, per_vanishes_normals,
                     sign_reps, support)

RES = {}


# =========================================================== self-controls ==
def self_controls():
    rng = random.Random(20260815)
    out = {}
    bad = 0
    for _ in range(300):
        n = rng.randint(1, 5)
        cols = [[rng.randint(-6, 6) for _ in range(n)] for _ in range(n)]
        if per(cols) != per_bruteforce(cols):
            bad += 1
    out["dp_vs_bruteforce_mismatches_over_300"] = bad
    out["per_identity_4x4_is_1"] = per([[1, 0, 0, 0], [0, 1, 0, 0],
                                        [0, 0, 1, 0], [0, 0, 0, 1]]) == 1
    out["per_allones_4x4_is_24"] = per([[1] * 4] * 4) == 24
    out["per_allones_5x5_is_120"] = per([[1] * 5] * 5) == 120
    # multilinearity test used by per_vanishes_on_product
    okml = True
    for _ in range(50):
        n = 4
        bs = [[[rng.randint(-4, 4) for _ in range(n)] for _ in range(n - 1)]
              for _ in range(n)]
        cs = [[rng.randint(-3, 3) for _ in range(n - 1)] for _ in range(n)]
        pt = [[sum(cs[j][k] * bs[j][k][i] for k in range(n - 1))
               for i in range(n)] for j in range(n)]
        lhs = per(pt)
        rhs = 0
        for idx in product(range(n - 1), repeat=n):
            c = 1
            for j in range(n):
                c *= cs[j][idx[j]]
            rhs += c * per([bs[j][idx[j]] for j in range(n)])
        if lhs != rhs:
            okml = False
    out["multilinear_expansion_ok"] = okml
    # kernel basis really spans the kernel
    okk = True
    for _ in range(200):
        n = rng.randint(2, 5)
        nv = [rng.randint(-5, 5) for _ in range(n)]
        if not any(nv):
            continue
        B = kernel_basis(nv)
        if len(B) != n - 1:
            okk = False
        for b in B:
            if sum(nv[i] * b[i] for i in range(n)) != 0:
                okk = False
        # independence: rank n-1 over Q
        M = [row[:] for row in B]
        r = 0
        for c in range(n):
            piv = None
            for i in range(r, len(M)):
                if M[i][c]:
                    piv = i
                    break
            if piv is None:
                continue
            M[r], M[piv] = M[piv], M[r]
            for i in range(len(M)):
                if i != r and M[i][c]:
                    f = Fraction(M[i][c], M[r][c])
                    M[i] = [a - f * b for a, b in zip(M[i], M[r])]
            r += 1
        if r != n - 1:
            okk = False
    out["kernel_basis_ok"] = okk
    return out


# ================================================================== A1 =====
def A1_stepA_symbolic(n):
    """STEP (A), verified by my own exact symbolic expansion.

    Hypothesis of step (A): some coordinate r lies in the support of EVERY
    normal.  Take r = n-1.  On V_j the r-entry of column j is determined:
        U[r][j] = -sum_{i != r} m[j][i] U[i][j],   m[j][i] = nv_j[i]/nv_j[r].
    The remaining n(n-1) entries U[i][j] (i != r) are FREE and independent, so
    "per == 0 on the product" is exactly "per(U) == 0 as a polynomial".

    We expand per(U) exactly (sympy, rational coefficients) and check
      (a) every monomial of per(U) uses each column once and has exactly one
          repeated row i, occurring in exactly two columns j < j';
      (b) its coefficient is exactly -(m[j][i] + m[j'][i]);
      (c) every (i, {j,j'}) actually occurs (so no equation is missing);
      (d) the resulting linear system on the m's has ONLY the zero solution
          when n >= 3, and a nonzero solution space when n = 2.
    """
    import sympy as sp
    r = n - 1
    U = {(i, j): sp.Symbol("U_%d_%d" % (i, j))
         for i in range(n) for j in range(n) if i != r}
    m = {(j, i): sp.Symbol("m_%d_%d" % (j, i))
         for j in range(n) for i in range(n) if i != r}
    cols = []
    for j in range(n):
        col = []
        for i in range(n):
            if i == r:
                col.append(-sum(m[(j, i2)] * U[(i2, j)]
                                for i2 in range(n) if i2 != r))
            else:
                col.append(U[(i, j)])
        cols.append(col)
    P = sp.expand(per_bruteforce(cols))
    Uvars = sorted(U.values(), key=lambda s: s.name)
    poly = sp.Poly(P, *Uvars)
    shape_ok = True
    coeff_ok = True
    seen_pairs = set()
    nmon = 0
    for mono, coef in poly.terms():
        nmon += 1
        used = [Uvars[k] for k in range(len(Uvars)) for _ in range(mono[k])]
        idx = []
        for s in used:
            _, i, j = s.name.split("_")
            idx.append((int(i), int(j)))
        colcnt = {}
        rowcnt = {}
        for (i, j) in idx:
            colcnt[j] = colcnt.get(j, 0) + 1
            rowcnt[i] = rowcnt.get(i, 0) + 1
        if sorted(colcnt.values()) != [1] * n or len(colcnt) != n:
            shape_ok = False
        rep = [i for i, c in rowcnt.items() if c == 2]
        if len(rep) != 1 or sorted(rowcnt.values()) != [1] * (n - 2) + [2]:
            shape_ok = False
            continue
        i0 = rep[0]
        js = sorted(j for (i, j) in idx if i == i0)
        seen_pairs.add((i0, tuple(js)))
        want = sp.expand(-(m[(js[0], i0)] + m[(js[1], i0)]))
        if sp.simplify(coef - want) != 0:
            coeff_ok = False
    want_pairs = {(i, (j, jj)) for i in range(n - 1)
                  for j, jj in combinations_with_replacement(range(n), 2)
                  if j < jj}
    # (d) solve the linear system
    eqs = [m[(j, i)] + m[(jj, i)] for i in range(n - 1)
           for j, jj in combinations_with_replacement(range(n), 2) if j < jj]
    Msys = sp.Matrix([[sp.diff(e, v) for v in sorted(m.values(),
                                                     key=lambda s: s.name)]
                      for e in eqs]) if eqs else sp.zeros(0, len(m))
    nullity = len(m) - Msys.rank() if eqs else len(m)
    return dict(n=n, n_monomials=nmon, monomial_shape_ok=shape_ok,
                coefficients_are_minus_mji_plus_mjpi=coeff_ok,
                all_pairs_realised=(seen_pairs == want_pairs),
                n_pairs_expected=len(want_pairs), n_pairs_seen=len(seen_pairs),
                n_m_unknowns=len(m), solution_space_dim=int(nullity),
                only_zero_solution=(nullity == 0))


def A1_stepB_probes():
    """STEP (B): the written justification contains a FALSE assertion.

    The docstring of w20_perlemma.py says: substituting e_a into a full
    projection "gives per_{n-2} == 0 on two further projections, which (for
    n = 4) forces one of them to be 0 -- impossible, since a hyperplane of
    C^4 projects onto at least a plane."

    Probe 1  per_2 == 0 on A x B does NOT force A = 0 or B = 0.
    Probe 2  more generally a FULL factor does not force a zero factor:
             per_3 == 0 on C^3 x <e_1> x <e_1>.
    Probe 3  the dimension excuse fails: after the FIRST projection a
             hyperplane of C^4 is >= 2-dimensional, but after the SECOND
             projection (the one used) it can be 1-dimensional.  Explicit
             hyperplane of C^4 whose r-then-a projection is a line.
    Probe 4  the case really occurs inside step (B): explicit hyperplanes of
             C^4 where the substitution of step (B) leaves two LINES.
    """
    out = {}
    A = [[1, 0]]              # <e_1>
    B = [[1, 0]]              # <e_1>
    out["probe1_per2_zero_on_two_lines"] = dict(
        A="<e_1>", B="<e_1>", per2=per([A[0], B[0]]),
        vanishes=per_vanishes_on_product([A, B]),
        both_nonzero=True,
        refutes="per_2 == 0 forces one factor to be 0")
    full3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    line = [[1, 0, 0]]
    out["probe2_per3_zero_with_full_factor"] = dict(
        X="C^3", Y="<e_1>", Z="<e_1>",
        vanishes=per_vanishes_on_product([full3, line, line]),
        refutes="a full factor forces a zero factor")
    # probe 3: V = ker(1,0,0,0) = span{e_2,e_3,e_4}; project out r = 2 then
    # a = 3 (0-indexed).  dim stays 2 then drops to ... compute honestly.
    V = kernel_basis([1, 1, 0, 0])   # hyperplane of C^4
    def proj(vecs, k):
        return [[v[i] for i in range(len(v)) if i != k] for v in vecs]
    def dim(vecs):
        M = [[Fraction(x) for x in v] for v in vecs]
        r, nc = 0, len(M[0]) if M else 0
        for c in range(nc):
            piv = None
            for i in range(r, len(M)):
                if M[i][c]:
                    piv = i
                    break
            if piv is None:
                continue
            M[r], M[piv] = M[piv], M[r]
            for i in range(len(M)):
                if i != r and M[i][c]:
                    f = M[i][c] / M[r][c]
                    M[i] = [a - f * b for a, b in zip(M[i], M[r])]
            r += 1
        return r
    P1 = proj(V, 3)                 # project out coordinate r = 3
    P2 = proj(P1, 2)                # then coordinate a = 2 of C^3
    out["probe3_double_projection_can_be_a_line"] = dict(
        hyperplane="ker(1,1,0,0) < C^4", dim_V=dim(V),
        dim_after_first_projection=dim(P1),
        dim_after_second_projection=dim(P2),
        note="step (B) applies per_2 to spaces of THIS kind; the quoted "
             "reason 'a hyperplane of C^4 projects onto at least a plane' "
             "only bounds the FIRST projection")
    # probe 4: exhibit hyperplanes of C^4 realising the configuration that
    # step (B)'s sub-argument declares impossible: after e_r and then e_a,
    # two LINES on which per_2 vanishes identically.
    V2 = kernel_basis([0, 0, 1, 0])   # = span{e_1,e_2,e_4}
    V3 = kernel_basis([0, 0, 1, 0])
    Q2, Q3 = proj(proj(V2, 3), 2), proj(proj(V3, 3), 2)
    out["probe4_two_lines_with_per2_vanishing"] = dict(
        V="ker(0,0,1,0) twice", dim_each=[dim(Q2), dim(Q3)],
        per2_vanishes=per_vanishes_on_product(
            [[q for q in Q2 if any(q)][:1], [q for q in Q3 if any(q)][:1]]))
    out["verdict"] = ("step (A) valid; step (B) as written uses a FALSE "
                      "intermediate claim (per_2 == 0 forces a zero factor)")
    return out


def A1_corrected_proof_checks():
    """the CORRECTED induction I supply, with its ingredients checked exactly.

    L(n) for n >= 3:  if per_n == 0 on X_1 x ... x X_n with dim X_j >= n-1 for
    every j, then all X_j are one and the same coordinate hyperplane.

    ingredient (i)   per_2 == 0 on A x B, dim A = 2  =>  B = 0.
    ingredient (ii)  substituting e_i in slot j gives
                     per_{n-1} == 0 on the i-projections of the other X_k.
    ingredient (iii) dim pi_i(X) >= dim X - 1, with equality iff e_i in X.
    ingredient (iv)  no X_j can be all of C^n (else L(n-1) gives one common
                     coordinate hyperplane s(a) for every deleted a, forcing
                     s(a) = s for all a, contradicting s(a) != a at a = s).
    ingredient (v)   if all X_j are hyperplanes and some nv_j[i] = 0 then
                     L(n-1) forces X_k = {v_s = 0} for all k != j, s != i;
                     with an empty common support that repeats at (j,s) and
                     contradicts itself.
    """
    out = {}
    # (i) exact check on all A with dim 2
    ok = True
    A = [[1, 0], [0, 1]]
    for B in ([[1, 0]], [[0, 1]], [[1, 1]], [[2, -3]]):
        if per_vanishes_on_product([A, B]):
            ok = False
    out["ingredient_i_full_factor_kills_partner_at_n2"] = ok
    # (ii) substitution identity, exact, random check at n = 4 and n = 5
    rng = random.Random(7)
    ok2 = True
    for n in (3, 4, 5):
        for _ in range(200):
            cols = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
            i = rng.randrange(n)
            j = rng.randrange(n)
            e = [0] * n
            e[i] = 1
            cols[j] = e
            sub = [[c[k] for k in range(n) if k != i]
                   for jj, c in enumerate(cols) if jj != j]
            if per(cols) != per(sub):
                ok2 = False
    out["ingredient_ii_substitution_identity"] = ok2
    # (iv)/(v) are combinatorial; the sweeps below are their numerical test.
    out["note"] = ("the corrected induction is stated in the final report; "
                   "its base case n = 3 and step are exercised by A2/A4")
    return out


# ================================================================== A2 =====
def sweep_multisets(n, cand, tag, report_every=None):
    """EXHAUSTIVE sweep over MULTISETS of n normals drawn from `cand`.

    Complete coverage argument: per is symmetric under permuting the columns
    v^j, and V_j = ker(nv_j) = ker(c*nv_j); hence sweeping multisets of
    sign-representatives covers EVERY ordered tuple of hyperplanes whose
    normals lie in the underlying value set."""
    bases = [kernel_basis(nv) for nv in cand]
    tested = 0
    vanishing = []
    violations = []
    for combo in combinations_with_replacement(range(len(cand)), n):
        tested += 1
        normals = [cand[k] for k in combo]
        v = per_vanishes_on_product([bases[k] for k in combo])
        c = is_common_coordinate(normals)
        if v:
            vanishing.append(normals)
        if v != c:
            violations.append(dict(normals=[list(x) for x in normals],
                                   per_vanishes=v, is_common_coordinate=c))
    return dict(tag=tag, n=n, n_candidate_normals=len(cand),
                n_multisets_tested=tested,
                equivalent_ordered_configs=len(cand) ** n,
                equivalent_unreduced_configs=(2 * len(cand)) ** n,
                n_vanishing=len(vanishing),
                vanishing=[[list(x) for x in v] for v in vanishing[:10]],
                n_violations=len(violations), violations=violations[:5])


def sweep_ordered_full(n, cand, tag):
    """ordered (unreduced by column symmetry) sweep -- used at n = 3 where it
    is cheap, as a control on the multiset reduction."""
    bases = [kernel_basis(nv) for nv in cand]
    tested = 0
    nv_ = 0
    violations = []
    for combo in product(range(len(cand)), repeat=n):
        tested += 1
        normals = [cand[k] for k in combo]
        v = per_vanishes_on_product([bases[k] for k in combo])
        c = is_common_coordinate(normals)
        if v:
            nv_ += 1
        if v != c:
            violations.append([list(x) for x in normals])
    return dict(tag=tag, n=n, n_tested=tested, n_vanishing=nv_,
                n_violations=len(violations), violations=violations[:5])


def random_battery(n, trials, seed, lo=-6, hi=6):
    rng = random.Random(seed)
    tested = 0
    bad = []
    nvan = 0
    while tested < trials:
        normals = [tuple(rng.randint(lo, hi) for _ in range(n))
                   for _ in range(n)]
        if not all(any(x) for x in normals):
            continue
        tested += 1
        v = per_vanishes_normals(normals)
        c = is_common_coordinate(normals)
        if v:
            nvan += 1
        if v != c:
            bad.append([list(x) for x in normals])
    return dict(n=n, trials=tested, n_vanishing=nvan, n_violations=len(bad),
                violations=bad[:5])


# ================================================================== A3 =====
def A3_counterexamples():
    out = {}
    # (a) the lemma is FALSE at n = 2.  My own witnesses, found exhaustively.
    cand2 = sign_reps(2)
    wit = []
    for a in cand2:
        for b in cand2:
            if per_vanishes_normals([a, b]) and not is_common_coordinate([a, b]):
                wit.append(dict(normals=[list(a), list(b)],
                                V1=[list(x) for x in kernel_basis(a)],
                                V2=[list(x) for x in kernel_basis(b)],
                                per_on_basis=per([kernel_basis(a)[0],
                                                  kernel_basis(b)[0]])))
    out["n2_false"] = dict(n_witnesses_in_pm1_stratum=len(wit),
                           witnesses=wit[:6],
                           general_family="V_1 = <(p,q)>, V_2 = <(s,t)> with "
                                          "p*t + q*s = 0; e.g. V_1 = <(1,1)>, "
                                          "V_2 = <(1,-1)>")
    # explicit check of the general family: per_2((p,q),(p,-q)) = -pq + qp = 0
    p, q = 3, 5
    fam = per([[p, q], [p, -q]])
    out["n2_false"]["family_check"] = dict(
        v1=[p, q], v2=[p, -q], per=fam, zero=(fam == 0),
        normals=[list(kn) for kn in ([q, p], [-q, p])])
    # (b) FALSE without the hyperplane hypothesis (proper subspaces of C^4)
    #     witness 1 (trivial): two copies of the LINE <e_1> and anything.
    L1 = [[1, 0, 0, 0]]
    W = [[0, 1, 0, 0], [0, 0, 1, 0]]
    out["nonhyperplane_witness_trivial"] = dict(
        spaces="<e_1>, <e_1>, span{e_2,e_3}, span{e_2,e_3}",
        dims=[1, 1, 2, 2],
        vanishes=per_vanishes_on_product([L1, L1, W, W]),
        is_common_coordinate_hyperplane=False)
    #     witness 2 (no zero entries anywhere): all four spaces spanned by
    #     vectors with every coordinate nonzero.
    u = [1, 1, 1, 1]
    P = [[1, 1, -1, -1], [1, -1, 1, -1]]
    Qs = [[1, 1, 1, 1], [1, -1, -1, 1]]
    out["nonhyperplane_witness_all_nonzero"] = dict(
        spaces="<u>, <u>, span{(1,1,-1,-1),(1,-1,1,-1)}, "
               "span{(1,1,1,1),(1,-1,-1,1)}",
        dims=[1, 1, 2, 2],
        vanishes=per_vanishes_on_product([[u], [u], P, Qs]),
        all_basis_permanents=[per([u, u, a, b]) for a in P for b in Qs])
    #     witness 3: my own, found by exhaustive search over 2-dim subspaces
    #     spanned by {-1,0,1} vectors, with no repeated space.
    found = []
    vecs = [v for v in product((-1, 0, 1), repeat=4) if any(v)]
    small = [v for v in vecs if v[0] == 1]
    # deterministic search: pairs of 2-dim spaces X, Y with per == 0 on
    # X x X x Y x Y and X != Y, no space a coordinate hyperplane
    cnt = 0
    for a, b in combinations_with_replacement(small, 2):
        if a == b:
            continue
        X = [list(a), list(b)]
        for c, d in combinations_with_replacement(small, 2):
            if c == d:
                continue
            Y = [list(c), list(d)]
            if per_vanishes_on_product([X, X, Y, Y]):
                cnt += 1
                if len(found) < 4 and X != Y:
                    found.append(dict(X=X, Y=Y))
        if cnt > 200:
            break
    out["nonhyperplane_search"] = dict(n_found_pairs=cnt, samples=found)
    return out


def main():
    RES["_header"] = ("A7 SUB-AUDIT of W20 LEMMA W20-P -- items A1/A2/A3. "
                      "Exact integer/Fraction arithmetic only. UNAUDITED "
                      "AUDIT ARTEFACT, independent re-implementation.")
    RES["self_controls"] = self_controls()
    print("self controls:", RES["self_controls"], flush=True)

    RES["A1_stepA_symbolic"] = {}
    for n in (2, 3, 4, 5):
        RES["A1_stepA_symbolic"]["n%d" % n] = A1_stepA_symbolic(n)
        print("A1 step (A) n=%d:" % n,
              RES["A1_stepA_symbolic"]["n%d" % n], flush=True)
    RES["A1_stepB_probes"] = A1_stepB_probes()
    print("A1 step (B) probes:", json.dumps(RES["A1_stepB_probes"], indent=1,
                                            default=str), flush=True)
    RES["A1_corrected_proof_checks"] = A1_corrected_proof_checks()
    print("A1 corrected proof ingredients:",
          RES["A1_corrected_proof_checks"], flush=True)

    cand3 = sign_reps(3)
    cand4 = sign_reps(4)
    RES["A2_n3_ordered"] = sweep_ordered_full(3, cand3, "n3 ordered {-1,0,1}")
    print("A2 n=3 ordered sweep:", RES["A2_n3_ordered"], flush=True)
    RES["A2_n3_multiset"] = sweep_multisets(3, cand3, "n3 multiset {-1,0,1}")
    print("A2 n=3 multiset sweep:", RES["A2_n3_multiset"], flush=True)
    RES["A2_n4_multiset"] = sweep_multisets(4, cand4, "n4 multiset {-1,0,1}")
    print("A2 n=4 multiset sweep:", RES["A2_n4_multiset"], flush=True)
    RES["A2_random_n3"] = random_battery(3, 3000, 11)
    RES["A2_random_n4"] = random_battery(4, 3000, 13)
    print("A2 random:", RES["A2_random_n3"], RES["A2_random_n4"], flush=True)

    RES["A3"] = A3_counterexamples()
    print("A3:", json.dumps(RES["A3"], indent=1, default=str), flush=True)

    json.dump(RES, open(os.path.join(HERE, "a7_results_A123.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
