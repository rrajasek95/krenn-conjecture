#!/usr/bin/env python3
"""A6-B9 / MUTATION CONTROLS.

Every checker used in b9_c1_detlaw.py / b9_c2_phi.py is deliberately broken
here; each mutation MUST flip the verdict.  A checker that cannot fail is not
evidence.  All arithmetic exact (int / Fraction).
"""

from __future__ import annotations

import json
import random
import sys
import time

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-audit-a6-w15w14-2026-08-15")
import b9_core as B                                            # noqa: E402

HERE = "/Users/rishi/workplace/krenn-conjecture/computations/" \
       "unaudited-audit-a6-w15w14-2026-08-15"

A_MAIN = [[3, -7, 2], [5, 1, -4], [-6, 8, 9]]          # full rank, det 362
A_ALT = [[1, 0, 0], [0, 2, 0], [0, 0, -3]]             # a different full-rank A
LEDGER = []


def note(mid, desc, expect, got, fired):
    LEDGER.append({"id": mid, "mutation": desc, "expected": expect,
                   "observed": got, "FIRED": bool(fired)})
    print(f"  [{'FIRED' if fired else 'DID NOT FIRE'}] {mid}: {desc}\n"
          f"        expected: {expect}\n        observed: {got}")


def codim(gens, d):
    amb = len(B.expos(d))
    E = B.IntEchelon(amb)
    for g in gens:
        E.add(B.to_vec(g, d))
        if E.rank() == amb:
            break
    return amb - E.rank()


def main():
    t0 = time.time()
    rng = random.Random(31337)
    dp = B.det_poly()
    print("== B9 mutation controls ==\n")

    # ---------------------------------------------------------------- M1
    # perturb one coefficient of phi_A -> must leave the perp of J_4
    phi = B.phi_form(A_MAIN)
    J4 = B.J_gens(3, 1, A_MAIN)
    base_ok = all(B.apolar(phi, g) == 0 for g in J4)
    fails = 0
    trials = 0
    for m in list(phi)[:12] + [e for e in B.expos(4)[:8] if e not in phi]:
        trials += 1
        mut = dict(phi)
        mut[m] = mut.get(m, 0) + 1
        if any(B.apolar(mut, g) != 0 for g in J4):
            fails += 1
    note("M1", "phi_A with one coefficient shifted by +1 (20 positions, "
                "12 present terms + 8 absent monomials)",
         "every perturbation leaves perp(J_4)",
         f"unperturbed phi in perp: {base_ok}; perturbations that left the "
         f"perp: {fails}/{trials}", base_ok and fails == trials)

    # ---------------------------------------------------------------- M2
    # permanent instead of determinant at h = 2.  Swept over a battery,
    # because on the 20 L-monomials the two operators can coincide: they
    # differ first on s^2 k_c, where det(d) gives 2 cof_cc(A) and perm(d)
    # gives 2 (A_aa A_bb + A_ab A_ba).
    J3 = B.J_gens(2, 1, A_MAIN)
    E3 = B.IntEchelon(165)
    for g in J3:
        E3.add(B.to_vec(g, 3))
    pp = B.perm_poly()
    sweep = [("main", A_MAIN),
             ("cof_00 = 0 (new)", [[1, 2, 3], [4, 2, 1], [7, 4, 2]]),
             ("cof_00 = 0 (W14)", [[2, 4, 6], [1, 15, 5], [5, 3, 1]]),
             ("identity", [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
             ("permutation", [[0, 1, 0], [0, 0, 1], [1, 0, 0]])]
    det_bad, perm_bad, wit = 0, 0, {}
    for lab, A in sweep:
        Ej = B.IntEchelon(165)
        for g in B.J_gens(2, 1, A):
            Ej.add(B.to_vec(g, 3))
        for a, b in B.l_monomials(3):
            m = B.lmono_poly(a, b, A)
            truth = True if not m else Ej.contains(B.to_vec(m, 3))
            if (B.apply_op(dp, m) == {}) != truth:
                det_bad += 1
            if (B.apply_op(pp, m) == {}) != truth:
                perm_bad += 1
                wit.setdefault(lab, []).append(B.lmono_name(a, b))
    note("M2", "replace det(d/dK) by the PERMANENT operator in the h=2 law "
                "(5-matrix sweep)",
         "the permanent criterion must disagree with true membership on some "
         "(A, m)",
         f"det criterion disagreements: {det_bad}/100; permanent criterion "
         f"disagreements: {perm_bad}/100, witnesses {wit}",
         det_bad == 0 and perm_bad > 0)
    # and the permanent must NOT be apolar-perp to J_3
    note("M2b", "test whether the permanent (not det) lies in perp(J_3)",
         "permanent is NOT orthogonal to all J_3 generators",
         f"nonzero pairings: {sum(1 for g in J3 if B.apolar(pp, g) != 0)}"
         f"/{len(J3)}", any(B.apolar(pp, g) != 0 for g in J3))

    # ---------------------------------------------------------------- M3
    # random quartics: must not be in the perp, must be in the layer
    notperp = inlayer = 0
    E4 = B.IntEchelon(495)
    for g in J4:
        E4.add(B.to_vec(g, 4))
    for _ in range(10):
        f = {m: rng.randint(-9, 9) for m in B.expos(4)}
        f = {m: c for m, c in f.items() if c}
        if any(B.apolar(f, g) != 0 for g in J4):
            notperp += 1
        if E4.contains(B.to_vec(f, 4)):
            inlayer += 1
    note("M3", "feed 10 random quartics to the perp checker and to the "
                "membership checker",
         "none lies in perp(J_4); and (J_4 being a codim-1 hyperplane) a "
         "random quartic must MISS the layer",
         f"outside the perp: {notperp}/10; inside J_4: {inlayer}/10",
         notperp == 10 and inlayer == 0)
    # positive control: random elements OF the layer must be members and must
    # pair to zero against phi
    pos_in = pos_perp = 0
    for _ in range(10):
        f = {}
        for _ in range(12):
            f = B.padd(f, B.pscale(J4[rng.randrange(len(J4))],
                                   rng.randint(-9, 9)))
        if E4.contains(B.to_vec(f, 4)):
            pos_in += 1
        if B.apolar(phi, f) == 0:
            pos_perp += 1
    note("M3c", "positive control: 10 random integer combinations of J_4 "
                "generators",
         "all 10 must be reported IN the layer and all must pair to 0 with phi",
         f"in the layer: {pos_in}/10; <phi, .> = 0: {pos_perp}/10",
         pos_in == 10 and pos_perp == 10)
    # random cubic vs perp(J_3)
    nc = 0
    for _ in range(10):
        f = {m: rng.randint(-9, 9) for m in B.expos(3)}
        f = {m: c for m, c in f.items() if c}
        if any(B.apolar(f, g) != 0 for g in J3):
            nc += 1
    note("M3b", "feed 10 random cubics to the h=2 perp checker",
         "none lies in perp(J_3) = span{det}", f"outside the perp: {nc}/10",
         nc == 10)

    # ---------------------------------------------------------------- M4
    # drop generator families from J_4 -> codim must change
    L3 = B.L_gens(3, A_MAIN)
    c_full = codim(J4, 4)
    only3 = [g for g in L3 if B.pdeg(g) == 3 and g in
             [dict(B.iota(3, mu, nu)) for mu, nu in B.sigma_basis(3)]]
    sp = B.s_poly(A_MAIN)
    fam_k3 = [dict(B.iota(3, mu, nu)) for mu, nu in B.sigma_basis(3)]
    fam_k2 = [B.pmul(dict(B.iota(2, mu, nu)), sp)
              for mu, nu in B.sigma_basis(2)]
    c_no_k2 = codim(B.J_gens(3, 1, A_MAIN, gens=fam_k3), 4)
    c_no_k3 = codim(B.J_gens(3, 1, A_MAIN, gens=fam_k2), 4)
    part = [B.pmul({m: 1}, g) for m in B.expos(1)[1:] for g in L3]   # 8 of 9
    c_8vars = codim(part, 4)
    note("M4", "drop a generator family from J_4 = S^1 * (s*iota_2 + iota_3)",
         "codim must move away from 1 in each case",
         f"full {c_full}; without the k=2 family {c_no_k2}; without the k=3 "
         f"family {c_no_k3}; with only 8 of the 9 S^1 multipliers {c_8vars}",
         c_full == 1 and c_no_k2 != 1 and c_no_k3 != 1 and c_8vars != 1)

    # ---------------------------------------------------------------- M5
    # corrupt iota: keep only the identity permutation
    def iota_bad(k, mu, nu):
        e = [0] * B.NV
        for t in range(k):
            e[B.vidx(mu[t], nu[t])] += 1
        return {tuple(e): 1}
    bad2 = [iota_bad(2, mu, nu) for mu, nu in B.sigma_basis(2)]
    badJ3 = [B.pmul({m: 1}, g) for m in B.expos(1) for g in bad2]
    c_bad3 = codim(badJ3, 3)
    bad3 = [iota_bad(3, mu, nu) for mu, nu in B.sigma_basis(3)]
    badL3 = bad3 + [B.pmul(g, sp) for g in bad2]
    c_bad4 = codim([B.pmul({m: 1}, g) for m in B.expos(1) for g in badL3], 4)
    # the corrupted h=2 layer happens to keep codim 1, so test the LAW, not
    # just the dimension: det must stop being the perp, and the membership
    # table must move.
    det_ok_bad = all(B.apolar(dp, g) == 0 for g in badJ3)
    Eb = B.IntEchelon(165)
    for g in badJ3:
        Eb.add(B.to_vec(g, 3))
    moved = []
    for a, b in B.l_monomials(3):
        m = B.lmono_poly(a, b, A_MAIN)
        t_true = True if not m else E3.contains(B.to_vec(m, 3))
        t_bad = True if not m else Eb.contains(B.to_vec(m, 3))
        if t_true != t_bad:
            moved.append(B.lmono_name(a, b))
    note("M5", "corrupt the Cauchy map iota (identity permutation only, no "
                "sum over S_k)",
         "det must leave the perp of the corrupted h=2 layer, the h=2 "
         "membership table must move, and codim(J_4) must change at h=3",
         f"det still perp to corrupted J_3: {det_ok_bad}; membership entries "
         f"that moved: {len(moved)} {moved}; codim deg3 (h=2) {c_bad3} "
         f"(true 1); codim deg4 (h=3) {c_bad4} (true {c_full})",
         (not det_ok_bad) and moved and c_bad4 != c_full)

    # ---------------------------------------------------------------- M6
    # drop the alpha! weights from the apolar pairing
    def naive(f, g):
        return sum(c * g.get(m, 0) for m, c in f.items())
    bad = sum(1 for g in J4 if naive(phi, g) != 0)
    bad3n = sum(1 for g in J3 if naive(dp, g) != 0)
    nm_moved = []
    for a, b in B.l_monomials(4):
        m = B.lmono_poly(a, b, A_MAIN)
        if (naive(phi, m) == 0) != (B.apolar(phi, m) == 0):
            nm_moved.append(B.lmono_name(a, b))
    note("M6", "drop the prod(alpha_n!) weights from the apolar pairing",
         "the unweighted pairing must break the phi checker (it is not "
         "expected to break the det checker: det is orthogonal to J_3 "
         "coefficientwise as well)",
         f"phi vs J_4: {bad}/{len(J4)} nonzero; det vs J_3: {bad3n}/{len(J3)} "
         f"nonzero; degree-4 exclusion-table entries that move: "
         f"{len(nm_moved)} {nm_moved}", bad > 0)

    # ---------------------------------------------------------------- M7
    # perturb det K -> must leave perp(J_3)
    left = 0
    keys = list(dp) + [e for e in B.expos(3)[:6] if e not in dp]
    for m in keys:
        mut = dict(dp)
        mut[m] = mut.get(m, 0) + 1
        if any(B.apolar(mut, g) != 0 for g in J3):
            left += 1
    note("M7", "perturb one coefficient of det K by +1 (12 positions)",
         "every perturbation leaves perp(J_3)", f"left the perp: {left}/"
         f"{len(keys)}", left == len(keys))

    # ---------------------------------------------------------------- M8
    # phi of the WRONG matrix
    phi_alt = B.phi_form(A_ALT)
    n_alt = sum(1 for g in J4 if B.apolar(phi_alt, g) != 0)
    note("M8", "test phi_{A'} for a different A' against perp(J_4(A))",
         "phi of the wrong matrix must NOT be orthogonal to J_4(A)",
         f"nonzero pairings: {n_alt}/{len(J4)}", n_alt > 0)

    # ---------------------------------------------------------------- M9
    # the two membership engines must disagree when one ideal is truncated
    lines = [f'ring R=0,({",".join(B.SVARS)}),dp;',
             "ideal I=" + ",".join(B.sing_poly(g) for g in L3[:-10]) + ";",
             "ideal G=std(I);"]
    names = []
    for a, b in B.l_monomials(4):
        p = B.lmono_poly(a, b, A_MAIN)
        names.append(B.lmono_name(a, b))
        lines.append(f'"MEM {B.lmono_name(a, b)} "'
                     f"+string(reduce({B.sing_poly(p)},G)==0);")
    out = B.run_singular("\n".join(lines))
    trunc = {}
    for line in out.splitlines():
        f = line.split()
        if f and f[0] == "MEM":
            trunc[f[1]] = (f[2] == "1")
    diff = []
    for a, b in B.l_monomials(4):
        nm = B.lmono_name(a, b)
        m = B.lmono_poly(a, b, A_MAIN)
        truth = True if not m else E4.contains(B.to_vec(m, 4))
        if trunc[nm] != truth:
            diff.append(nm)
    note("M9", "give Singular a TRUNCATED ideal (10 of the 136 L_3 generators "
                "removed) and re-run the membership query",
         "the Singular engine must now disagree with the exact row-reduction "
         "engine", f"disagreements: {len(diff)} {diff[:6]}", len(diff) > 0)

    # ---------------------------------------------------------------- M10
    # sign flip inside the closed form: q^2 + 4 shat det, and q^2 - 3 shat det
    for tag, coef in (("+4", 4), ("-3", -3), ("-5", -5)):
        mut = B.padd(B.pmul(B.q_form(A_MAIN), B.q_form(A_MAIN)),
                     B.pscale(B.pmul(B.shat_form(A_MAIN), dp), coef))
        n = sum(1 for g in J4 if B.apolar(mut, g) != 0)
        note(f"M10{tag}", f"replace phi = q^2 - 4 shat det by q^2 {tag} shat det",
             "must leave perp(J_4)", f"nonzero pairings: {n}/{len(J4)}", n > 0)

    # ---------------------------------------------------------------- M11
    # index-convention mutations inside the closed form (A_MAIN is not
    # symmetric, so transposing genuinely changes the form)
    qA = B.q_form(A_MAIN)
    q_T = {}
    for i in B.COL:
        for j in B.COL:
            if A_MAIN[i][j]:
                q_T = B.padd(q_T, B.pscale(B.cof_poly(j, i), A_MAIN[i][j]))
    shat_T = B.plin([B.cof_num(A_MAIN, j, i) for i in B.COL for j in B.COL])
    q_uns = {}
    for i in B.COL:
        for j in B.COL:
            if A_MAIN[i][j]:
                c = B.cof_poly(i, j)
                if (i + j) % 2:
                    c = B.pscale(c, -1)
                q_uns = B.padd(q_uns, B.pscale(c, A_MAIN[i][j]))
    variants = {
        "shat via adj A (transposed cofactors)":
            B.padd(B.pmul(qA, qA), B.pscale(B.pmul(shat_T, dp), -4)),
        "q via cof_ji(K) (transposed)":
            B.padd(B.pmul(q_T, q_T),
                   B.pscale(B.pmul(B.shat_form(A_MAIN), dp), -4)),
        "q with UNSIGNED 2x2 minors":
            B.padd(B.pmul(q_uns, q_uns),
                   B.pscale(B.pmul(B.shat_form(A_MAIN), dp), -4))}
    for tag, f in variants.items():
        n = sum(1 for g in J4 if B.apolar(f, g) != 0)
        note("M11", f"closed form with {tag}",
             "must leave perp(J_4) (the index convention is load-bearing)",
             f"nonzero pairings: {n}/{len(J4)}", n > 0)

    # ------------------------------------------------- M12 (informational)
    # e_i(K adj A) vs e_i(adj A K): AB and BA are cospectral, so the
    # discriminant identity cannot see the side.  Recorded, not a control.
    adjA = B.adj_num(A_MAIN)
    Nr = B.matmul_poly(True, adjA)                       # K * adj(A)
    Nl = [[B.plin([adjA[i][t] if n == B.vidx(t, j) else 0
                   for t in B.COL for n2 in [0] for n in [B.vidx(t, j)]])
           for j in B.COL] for i in B.COL]               # placeholder
    Nl = [[{} for _ in B.COL] for _ in B.COL]
    for i in B.COL:
        for j in B.COL:
            acc = {}
            for t in B.COL:
                if adjA[i][t]:
                    acc = B.padd(acc, {B.unit(B.vidx(t, j)): adjA[i][t]})
            Nl[i][j] = acc
    dr = B.padd(B.pmul(B.char_e(Nr, 2), B.char_e(Nr, 2)),
                B.pscale(B.pmul(B.char_e(Nr, 1), B.char_e(Nr, 3)), -4))
    dl = B.padd(B.pmul(B.char_e(Nl, 2), B.char_e(Nl, 2)),
                B.pscale(B.pmul(B.char_e(Nl, 1), B.char_e(Nl, 3)), -4))
    d2 = B.det_num(A_MAIN) ** 2
    LEDGER.append({"id": "M12", "mutation": "N = adj(A) K instead of K adj(A)",
                   "expected": "no change (AB and BA are cospectral)",
                   "observed": f"K adj(A) form == det(A)^2 phi: "
                               f"{dr == {m: c * d2 for m, c in phi.items()}}; "
                               f"adj(A) K form identical: {dl == dr}",
                   "FIRED": None, "informational": True})
    print(f"  [INFO] M12: N = adj(A)K vs K adj(A): identical discriminant "
          f"{dl == dr}; equals det(A)^2 phi_A "
          f"{dr == {m: c * d2 for m, c in phi.items()}}")

    # ---------------------------------------------------------------- M13
    # corrupt the L-monomial family: kappa_c := K_{c, c+1 mod 3}
    def lmono_bad(a, b, A):
        p = B.ppow(B.s_poly(A), a)
        for c in B.COL:
            for _ in range(b[c]):
                p = B.pmul(p, {B.unit(B.vidx(c, (c + 1) % 3)): 1})
        return p
    moved = {}
    for lab, Ax in (("A_MAIN", A_MAIN),
                    ("permutation", [[0, 1, 0], [0, 0, 1], [1, 0, 0]]),
                    ("W14 rand#2", [[-5, 0, 5], [1, 0, 1], [-2, 4, 0]]),
                    ("identity", [[1, 0, 0], [0, 1, 0], [0, 0, 1]])):
        Ex = B.IntEchelon(495)
        for g in B.J_gens(3, 1, Ax):
            Ex.add(B.to_vec(g, 4))
        for a, b in B.l_monomials(4):
            m0 = B.lmono_poly(a, b, Ax)
            m1 = lmono_bad(a, b, Ax)
            u0 = True if not m0 else Ex.contains(B.to_vec(m0, 4))
            u1 = True if not m1 else Ex.contains(B.to_vec(m1, 4))
            if u0 != u1:
                moved.setdefault(lab, []).append(B.lmono_name(a, b))
    note("M13", "corrupt the L-monomial family (kappa_c := K_{c,c+1 mod 3}), "
                "4-matrix sweep",
         "the degree-4 exclusion table must change for some A (it need not "
         "move for a generic A, whose table is the generic one)",
         f"entries that move: {json.dumps(moved)}", bool(moved))

    fired = sum(1 for e in LEDGER if e["FIRED"])
    total = sum(1 for e in LEDGER if e["FIRED"] is not None)
    print(f"\n  LEDGER: {fired}/{total} controls fired "
          f"(+{len(LEDGER)-total} informational) [{time.time()-t0:.0f}s]")
    with open(HERE + "/b9_mutations.json", "w") as fh:
        json.dump({"fired": fired, "controls": total,
                   "informational": len(LEDGER) - total, "ledger": LEDGER},
                  fh, indent=1)
    print("  wrote b9_mutations.json")


if __name__ == "__main__":
    main()
