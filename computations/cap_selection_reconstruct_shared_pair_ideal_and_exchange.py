#!/usr/bin/env python3
"""Independent reconstruction: nine shared-pair ideal, exchange charts,
prism guard families, and the boundary-silent decomposition.

This is the reconstruction layer demanded by the Priority-1 method
expectations.  It re-derives, with fresh code (cap_selection_lib):

1. the nine shared-pair tensor system  R^{pq}_{ij} = a_{ij} Q + p_i s_j F
   for one deleted pair of an arbitrary exact ten-site family, against a
   literal matching enumeration;
2. the pair-slice exchange chart: the redecomposition formulas for the
   overlapping deleted pair reproduce the literal second pair chart, and
   the triple-slice exchange identity holds coefficientwise;
3. the maximal transverse prism cap-slice countermodel: rank-nine top
   map, the 75/73-dimensional maximal slices, the four-parameter prism
   cofactor image with mixed discrepancy (z0 z1 z2), unit active
   saturation witness h = s z0 z1 z2, the all-nonzero adjugate cofactor
   matrix of the eight-site core, and the eight explicit transverse rows;
4. the four-parameter prism barrier family: same relocation failure;
5. the boundary-silent slice decomposition
       G_i = theta_i * HW + sum_{jk} M^{(i)}_{jk} e_j e_k (x) A_rs
   for random exact families whose extra capped pair {r, s} has no
   boundary edges (the exact hypothesis class of both guard families).

Every check is exact over Q; failures raise AssertionError.
"""

from __future__ import annotations

import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])

import sympy as sp

from cap_selection_lib import (
    alg_add,
    alg_equal,
    alg_mul,
    alg_scale,
    alg_zero,
    block_element,
    cap_contract,
    cofactor_family,
    contract_pure_boundary,
    divided_power,
    hafnian,
    pair_chart,
    pair_slice,
    perfect_matchings,
    pure_word,
    tensor_coefficients,
)

RNG = random.Random(20260728)


def random_family(sites, density=2, zero_pairs=(), span=5):
    fam = {}
    slist = list(sites)
    for i, u in enumerate(slist):
        for v in slist[i + 1 :]:
            if (u, v) in zero_pairs or (v, u) in zero_pairs:
                continue
            cells = {}
            for _ in range(density):
                cu, cv = RNG.randrange(3), RNG.randrange(3)
                coeff = RNG.randint(-span, span)
                if coeff:
                    cells[(cu, cv)] = cells.get((cu, cv), 0) + coeff
            cells = {k: c for k, c in cells.items() if c != 0}
            if cells:
                fam[(u, v)] = cells
    return fam


# ---------------------------------------------------------------------------
# 1 + 2: shared-pair system and exchange chart on random exact data
# ---------------------------------------------------------------------------


def check_shared_pair_and_exchange():
    sites = ("r", "t", 0, 1, 2, 3, 4, 5, 6, 7)
    boundary = sites[2:]
    fam = random_family(sites, density=2)
    # make sure some blocks vanish to exercise degeneracies
    fam.pop(("r", 0), None)
    fam.pop((2, 5), None)

    a, ell, mrow, x = pair_chart(fam, "r", "t", boundary, sites)
    Q = divided_power(x, 4)
    F = divided_power(x, 3)

    for i in range(3):
        for j in range(3):
            lhs = pair_slice(fam, "r", "t", i, j, boundary, sites)
            rhs = alg_add(alg_scale(Q, a[i][j]), alg_mul(alg_mul(ell[i], mrow[j]), F))
            assert alg_equal(lhs, rhs), f"pair equation failed at {(i, j)}"
    print("[1] nine shared-pair rows  R^{rt}_{ij} = a_ij Q + p_i s_j F : exact")

    # overlapping pair {r, 0}: literal second chart
    boundary2 = ("t", 1, 2, 3, 4, 5, 6, 7)
    b, ell2, mrow2, x2 = pair_chart(fam, "r", 0, boundary2, sites)
    Q2 = divided_power(x2, 4)
    F2 = divided_power(x2, 3)
    for i in range(3):
        for al in range(3):
            lhs = pair_slice(fam, "r", 0, i, al, boundary2, sites)
            rhs = alg_add(
                alg_scale(Q2, b[i][al]), alg_mul(alg_mul(ell2[i], mrow2[al]), F2)
            )
            assert alg_equal(lhs, rhs), f"second chart failed at {(i, al)}"
    print("[2a] overlapping-pair chart  R^{r0}_{i a} = b_ia Q' + ~p_i ~s_a F' : exact")

    # redecomposition formulas (5) of the exchange note, rebuilt from chart 1
    #   q^(0) = q|_{1..7} + sum_j e_j^(t) (s_j restricted off site 0)
    #   b_{i a} = p_{i,0,a};  ~p_i = sum_j a_ij e_j^(t) + p_i off site 0
    #   ~s_a = sum_j s_{j,0,a} e_j^(t) + (e_a^(0)* ⌟ q_{0v}) summed over v
    def restrict_off(form, site):
        return {k: c for k, c in form.items() if all(s != site for s, _ in k)}

    def component_at(form, site):
        out = [0, 0, 0]
        for k, c in form.items():
            kd = dict(k)
            if site in kd:
                out[kd[site]] = out[kd[site]] + c
        return out

    q_only = alg_zero()
    for idx, u in enumerate(boundary):
        for v in boundary[idx + 1 :]:
            if u == 0 or v == 0:
                continue
            q_only = alg_add(q_only, block_element(fam, u, v, sites))
    rebuilt_q0 = dict(q_only)
    for j in range(3):
        s_off = restrict_off(mrow[j], 0)
        rebuilt_q0 = alg_add(
            rebuilt_q0, alg_mul({frozenset({("t", j)}): 1}, s_off)
        )
    assert alg_equal(rebuilt_q0, x2), "q^(0) redecomposition failed"

    for i in range(3):
        for al in range(3):
            assert b[i][al] == component_at(ell[i], 0)[al], "b_ia != p_{i,0,a}"
    for i in range(3):
        rebuilt = restrict_off(ell[i], 0)
        for j in range(3):
            rebuilt = alg_add(rebuilt, {frozenset({("t", j)}): a[i][j]})
        rebuilt = {k: c for k, c in rebuilt.items() if c != 0}
        assert alg_equal(rebuilt, ell2[i]), "~p_i redecomposition failed"
    for al in range(3):
        rebuilt = alg_zero()
        for j in range(3):
            sval = component_at(mrow[j], 0)[al]
            if sval:
                rebuilt = alg_add(rebuilt, {frozenset({("t", j)}): sval})
        for v in boundary:
            if v == 0:
                continue
            blk = block_element(fam, 0, v, sites)
            for k, c in blk.items():
                kd = dict(k)
                if kd[0] != al:
                    continue
                rebuilt = alg_add(rebuilt, {frozenset({(v, kd[v])}): c})
        rebuilt = {k: c for k, c in rebuilt.items() if c != 0}
        assert alg_equal(rebuilt, mrow2[al]), "~s_a redecomposition failed"
    print("[2b] exchange redecomposition (q^(0), b, ~p, ~s) from chart one : exact")

    # triple-slice exchange identity, all 27 colour triples
    for i in range(3):
        for j in range(3):
            for al in range(3):
                lhs_full = pair_slice(fam, "r", "t", i, j, boundary, sites)
                lhs = {}
                for key, coeff in lhs_full.items():
                    kd = dict(key)
                    if kd.get(0) != al:
                        continue
                    stripped = frozenset(
                        (s2, c2) for s2, c2 in key if s2 != 0
                    )
                    lhs[stripped] = lhs.get(stripped, 0) + coeff
                rhs_full = pair_slice(fam, "r", 0, i, al, boundary2, sites)
                rhs = {}
                for key, coeff in rhs_full.items():
                    kd = dict(key)
                    if kd.get("t") != j:
                        continue
                    stripped = frozenset(
                        (s2, c2) for s2, c2 in key if s2 != "t"
                    )
                    rhs[stripped] = rhs.get(stripped, 0) + coeff
                assert alg_equal(lhs, rhs), f"exchange identity failed {(i, j, al)}"
    print("[2c] triple-slice exchange  i_{0a} R^{rt}_{ij} = i_{tj} R^{r0}_{ia} : exact")


# ---------------------------------------------------------------------------
# 3: the maximal transverse prism cap-slice countermodel
# ---------------------------------------------------------------------------

WSITES = ("p", "q", "r", "s")
USITES = ("x0", "x1", "x2", "y0", "y1", "y2")
ORDER10 = WSITES + USITES
AMAT = [[1, 2, 3], [4, 5, 7], [8, 11, 13]]


def guard_family(dense_pq):
    fam = {}

    def put(u, v, cu, cv, coeff=1):
        u_, v_ = (u, v) if ORDER10.index(u) < ORDER10.index(v) else (v, u)
        cu_, cv_ = (cu, cv) if ORDER10.index(u) < ORDER10.index(v) else (cv, cu)
        fam.setdefault((u_, v_), {})[(cu_, cv_)] = coeff

    for i in range(3):
        put("p", f"x{i}", i, i)
        put("q", f"y{i}", i, i)
        j, k = [t for t in range(3) if t != i]
        put(f"x{j}", f"x{k}", i, i)
        put(f"y{j}", f"y{k}", i, i)
    if dense_pq:
        for i in range(3):
            for j in range(3):
                put("p", "q", i, j, AMAT[i][j])
    else:
        put("p", "q", 0, 0)
    put("r", "s", 0, 0)
    put("p", "r", 1, 1)
    put("q", "s", 2, 2)
    return fam


def check_prism_countermodel():
    fam = guard_family(dense_pq=True)
    h10 = hafnian(fam, ORDER10, ORDER10)

    # top tensor = sum_{ij} e_i^p e_j^q e_0^r e_0^s E_ij
    expected = alg_zero()
    for i in range(3):
        for j in range(3):
            key = {("p", i), ("q", j), ("r", 0), ("s", 0)}
            key |= {(f"x{t}", i) for t in range(3)}
            key |= {(f"y{t}", j) for t in range(3)}
            expected = alg_add(expected, {frozenset(key): 1})
    assert alg_equal(h10, expected), "H10 of the guard family is wrong"
    print("[3a] H10 = sum_ij e_i^p e_j^q e_0^r e_0^s E_ij : exact (rank-9 top map)")

    # eight transverse rows, read off from H10 directly:
    coeffs = tensor_coefficients(h10, ORDER10)
    offdiag = 0
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            word = (i, j, 0, 0) + (i,) * 3 + (j,) * 3
            assert coeffs.get(word) == 1
            offdiag += 1
    assert offdiag == 6
    for c in (1, 2):
        bad = (c, c, 0, 0) + (c,) * 6
        good = (c,) * 10
        assert coeffs.get(bad) == 1 and good not in coeffs
    print("[3b] eight transverse rows: six off-diagonal c_ij present,")
    print("     colour-1/2 diagonal words sit at (c,c,0,0), not (c,c,c,c)")

    # pure-boundary-word slices G_i (the relocation content)
    for i in range(3):
        gi = contract_pure_boundary(fam, WSITES, USITES, i, ORDER10)
        expect = {frozenset({("p", i), ("q", i), ("r", 0), ("s", 0)}): AMAT[0][0] if False else 1}
        expect = {frozenset({("p", i), ("q", i), ("r", 0), ("s", 0)}): 1}
        assert alg_equal(gi, expect), f"G_{i} wrong"
        matches_ghz = alg_equal(gi, pure_word(WSITES, i))
        assert matches_ghz == (i == 0)
    print("[3c] pure-word slices G_i = e_i e_i e_0 e_0 : relocation fails for i=1,2")

    # symbolic cap on the 81 W-words
    wwords = [
        (a_, b_, c_, d_)
        for a_ in range(3)
        for b_ in range(3)
        for c_ in range(3)
        for d_ in range(3)
    ]
    kvars = {w: sp.Symbol("K_" + "".join(map(str, w))) for w in wwords}

    cof = cofactor_family(fam, WSITES, USITES, kvars, ORDER10)
    s_expr = sp.expand(
        sum(AMAT[i][j] * kvars[(i, j, 0, 0)] for i in range(3) for j in range(3))
        + kvars[(1, 2, 1, 2)]
    )
    for i in range(3):
        jk = [t for t in range(3) if t != i]
        for shore in ("x", "y"):
            cell = cof[(f"{shore}{jk[0]}", f"{shore}{jk[1]}")]
            assert set(cell) == {(i, i)} and sp.expand(cell[(i, i)] - s_expr) == 0
    for i in range(3):
        for j in range(3):
            cell = cof[(f"x{i}", f"y{j}")]
            assert set(cell) <= {(i, j)}
            got = cell.get((i, j), 0)
            assert sp.expand(got - kvars[(i, j, 0, 0)]) == 0
    for pair, cell in cof.items():
        u, v = pair
        same_shore = u[0] == v[0]
        cross = u[0] == "x" and v[0] == "y"
        if not same_shore and not cross:
            assert not cell
    print("[3d] full cofactor map: six triangle edges x s(K), cross blocks c_ij e_i e_j")
    print("     s(K) = sum a_ij c_ij + K_1212 : exact on all 81 cap coordinates")

    # maximal slices and effective rank
    top_functionals = [kvars[(i, j, 0, 0)] for i in range(3) for j in range(3)]
    lgz_extra = [
        kvars[(1, 1, 0, 0)] - kvars[(1, 1, 1, 1)],
        kvars[(2, 2, 0, 0)] - kvars[(2, 2, 2, 2)],
    ]
    allsyms = [kvars[w] for w in wwords]

    def rank_of(functionals):
        mat = sp.Matrix(
            [[sp.diff(f, v) for v in allsyms] for f in functionals]
        )
        return mat.rank()

    assert rank_of(top_functionals) == 9
    offd = [kvars[(i, j, 0, 0)] for i in range(3) for j in range(3) if i != j]
    assert rank_of(offd) == 6  # dim L_img = 81 - 6 = 75
    assert rank_of(offd + lgz_extra) == 8  # dim L_GHZ = 81 - 8 = 73
    eff = [s_expr] + [kvars[(i, i, 0, 0)] for i in range(3)]
    assert rank_of(eff + offd + lgz_extra) == 12  # 4 effective + 8 cut
    print("[3e] dim L_img = 75, dim L_GHZ = 73, effective top+cofactor rank on")
    print("     L_GHZ = 4, common kernel dimension = 69 : exact")

    # prism discrepancy on L_img: substitute off-diagonals by zero
    subs = {kvars[(i, j, 0, 0)]: 0 for i in range(3) for j in range(3) if i != j}
    zsyms = [sp.Symbol(f"z{i}") for i in range(3)]
    for i in range(3):
        subs[kvars[(i, i, 0, 0)]] = zsyms[i]
    cap_limg = {w: sp.expand(kvars[w].subs(subs)) for w in wwords}
    cof2 = cofactor_family(fam, WSITES, USITES, cap_limg, ORDER10)
    fam6 = {}
    for pair, cell in cof2.items():
        if cell:
            fam6[pair] = cell
    h6 = hafnian(fam6, USITES, USITES)
    svar = sp.expand(s_expr.subs(subs))
    expect6 = alg_zero()
    for i in range(3):
        expect6 = alg_add(
            expect6, alg_scale(pure_word(USITES, i), sp.expand(svar**2 * zsyms[i]))
        )
    mixedword = frozenset(
        {(f"x{i}", i) for i in range(3)} | {(f"y{i}", i) for i in range(3)}
    )
    expect6 = alg_add(expect6, {mixedword: zsyms[0] * zsyms[1] * zsyms[2]})
    diff = alg_add(h6, alg_scale(expect6, -1))
    diff = {k: sp.expand(c) for k, c in diff.items() if sp.expand(c) != 0}
    assert not diff, "prism hafnian formula failed"
    print("[3f] H6(A^K) on L_img = s^2 sum z_i X_i + z0 z1 z2 e_012012 :")
    print("     mixed discrepancy ideal (z0 z1 z2), h = s z0 z1 z2 in I (root cover)")

    # eight-site core adjugate identity
    core_sites = ("p", "q") + USITES
    fam8 = {k: v for k, v in fam.items() if all(s in core_sites for s in k)}
    a8, ell8, m8, x8 = pair_chart(fam8, "p", "q", USITES, core_sites)
    bmat = [
        [
            alg_add(alg_scale(x8, a8[i][j]), alg_mul(ell8[i], m8[j]))
            for j in range(3)
        ]
        for i in range(3)
    ]
    det = alg_zero()
    from itertools import permutations

    def perm_sign(perm):
        inv = sum(
            1
            for i_ in range(len(perm))
            for j_ in range(i_ + 1, len(perm))
            if perm[i_] > perm[j_]
        )
        return -1 if inv % 2 else 1

    for perm in permutations(range(3)):
        sign = perm_sign(perm)
        term = {frozenset(): 1}
        for i in range(3):
            term = alg_mul(term, bmat[i][perm[i]])
        det = alg_add(det, alg_scale(term, sign))
    amat_m = sp.Matrix(AMAT)
    cofmat = amat_m.adjugate().T
    expect_det = alg_zero()
    for i in range(3):
        for j in range(3):
            eij = {
                frozenset(
                    {(f"x{t}", i) for t in range(3)}
                    | {(f"y{t}", j) for t in range(3)}
                ): 2 * cofmat[i, j]
            }
            expect_det = alg_add(expect_det, eij)
    assert alg_equal(det, expect_det), "adjugate identity failed"
    assert all(cofmat[i, j] != 0 for i in range(3) for j in range(3))
    print("[3g] det(B_ij) = 2 sum Cof_ij(a) E_ij with all nine cofactors nonzero:")
    print("     the six omitted off-diagonal rows are adjugate-visible")


def check_barrier_family():
    fam = guard_family(dense_pq=False)
    for i in range(3):
        gi = contract_pure_boundary(fam, WSITES, USITES, i, ORDER10)
        expect = {frozenset({("p", i), ("q", i), ("r", 0), ("s", 0)}): 1}
        assert alg_equal(gi, expect)
    print("[4] four-parameter barrier family: G_i = e_i e_i e_0 e_0, same relocation")
    print("    failure; both guard families are boundary-silent at {r, s}")


# ---------------------------------------------------------------------------
# 5: the boundary-silent decomposition identity on random exact data
# ---------------------------------------------------------------------------


def check_silent_decomposition(trial):
    sites = ORDER10
    zero_pairs = [("r", u) for u in USITES] + [("s", u) for u in USITES]
    fam = random_family(sites, density=3, zero_pairs=zero_pairs, span=4)
    if trial == 1:
        # exercise degeneracies: kill the direct block and one star row
        fam.pop(("p", "q"), None)
        fam.pop(("p", "x1"), None)
    a, ell, mrow, x = pair_chart(fam, "p", "q", USITES, sites)
    hw = hafnian(fam, WSITES, sites)
    x3 = divided_power(x, 3)
    x2 = divided_power(x, 2)
    for i in range(3):
        gi = contract_pure_boundary(fam, WSITES, USITES, i, sites)
        theta_i = x3.get(frozenset((u, i) for u in USITES), 0)
        rhs = alg_scale(hw, theta_i)
        rs_block = block_element(fam, "r", "s", sites)
        for j in range(3):
            for k in range(3):
                mjk = alg_mul(alg_mul(ell[j], mrow[k]), x2).get(
                    frozenset((u, i) for u in USITES), 0
                )
                if mjk == 0:
                    continue
                term = alg_mul(
                    {frozenset({("p", j), ("q", k)}): mjk}, rs_block
                )
                rhs = alg_add(rhs, term)
        assert alg_equal(gi, rhs), f"silent decomposition failed, colour {i}"
    print(
        f"[5.{trial}] boundary-silent decomposition "
        "G_i = theta_i HW + sum M^i_jk e_j e_k (x) A_rs : exact"
    )


def main():
    check_shared_pair_and_exchange()
    check_prism_countermodel()
    check_barrier_family()
    for trial in range(2):
        check_silent_decomposition(trial)
    print("ALL RECONSTRUCTION CHECKS PASSED")


if __name__ == "__main__":
    main()
