#!/usr/bin/env python3
"""W22 T1d -- the INCIDENCE FORMALISM: transfer maps, 4-cycle holonomies, the
cocycle relation, and the complementary-diagonal conjugacy.

DEFINITIONS (all star blocks invertible).
  transfer   T_a^{pq} = (A_qa^T)^{-1} A_pa^T : V_p -> V_q     (a != p,q)
  holonomy   H_{pq}^{ab} = (T_b^{pq})^{-1} T_a^{pq} in GL(V_p)
             = (A_pb^T)^{-1} A_qb^T (A_qa^T)^{-1} A_pa^T
             -- the holonomy of the 4-CYCLE p-a-q-b based at p.

THEOREM W22-T (h = 2 transfer form of W17.1).  Site a is degenerate for the
cap u (x) v iff T_a u is parallel to v.  Hence with invertible stars:
   witness  <=>  exists u (all u_c != 0) with either
     (i)  all four T_a u parallel, with scalars rho (T_a u = rho_a v)
          satisfying e_2(rho) = 0;                       [4-fold coincidence]
     (ii) exactly three parallel, with rho in the ratio 1 : omega : omega^2
          (omega^3 = 1, omega != 1);                     [3-fold + cube roots]
   plus admissibility (v_c != 0, u^T A_pq v != 0).
The |I| >= 2 branches are empty when the stars are invertible.

THEOREM W22-COC (cocycle).  T_a = G_a means H^{ab} = G_b^{-1} G_a, so
   H^{ca} H^{bc} H^{ab} = id  for any three sites a,b,c.
THEOREM W22-C (complementary-diagonal transpose-conjugacy).  The 4-cycle
p-a-q-b is read by BOTH pairs (p,q) and (a,b).  With psi(x->y) = A_xy^T and
psi(y->x) = psi(x->y)^T (backwards through a block is the INVERSE, not the
transpose),
   H_{ab}^{pq} = [ psi(p->a) H_{pq}^{ab} psi(p->a)^{-1} ]^T .
So the two diagonals are ISOSPECTRAL (same characteristic polynomial) but the
eigenvectors of one are the LEFT eigenvectors of the other.  (The naive
conjugacy form -- without the transpose -- is FALSE: refuted 176/176 by the
control in this file's first run.)
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-induction2-w22-2026-08-15")
sys.path.insert(0, BASE)
import w22_core as W                                        # noqa: E402

RES = {}


def mat_mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def mat_T(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A))]


def mat_inv(A):
    n = len(A)
    M = [[Fraction(A[i][j]) for j in range(n)] + [Fraction(int(i == j))
                                                  for j in range(n)]
         for i in range(n)]
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        inv = Fraction(1) / M[c][c]
        M[c] = [x * inv for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return [row[n:] for row in M]


def mat_vec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def parallel(x, y):
    return all(a == 0 for a in W.cross(x, y))


def ratio(x, y):
    """scalar t with x = t y (y != 0, x parallel to y)."""
    for i in range(3):
        if y[i] != 0:
            return Fraction(x[i], 1) / y[i]
    return None


def transfer(src, p, q, a):
    Apa = mat_T(W.oriented(src, p, a))
    Aqa = mat_T(W.oriented(src, q, a))
    inv = mat_inv(Aqa)
    if inv is None:
        return None
    return mat_mul(inv, Apa)


def main():
    rng = random.Random(88999)

    # ---- C-a: the degeneracy dictionary  (site degenerate <=> T_a u || v) --
    tot = bad = 0
    for _ in range(400):
        n = 6
        src = {e: [[rng.randint(-4, 4) for _ in range(3)] for _ in range(3)]
               for e in combinations(range(n), 2)}
        p, q = rng.sample(range(n), 2)
        U = tuple(x for x in range(n) if x not in (p, q))
        if any(mat_inv(W.oriented(src, x, a)) is None
               for x in (p, q) for a in U):
            continue
        u = [rng.randint(-3, 3) for _ in range(3)]
        v = [rng.randint(-3, 3) for _ in range(3)]
        if all(x == 0 for x in u) or all(x == 0 for x in v):
            continue
        alpha, beta = W.alpha_beta(src, p, q, u, v, U)
        for a in U:
            deg = W.site_rank(alpha[a], beta[a]) <= 1
            Ta = transfer(src, p, q, a)
            pred = parallel(mat_vec(Ta, u), v)
            tot += 1
            bad += int(deg != pred)
    RES["degeneracy_dictionary"] = {"checked": tot, "violations": bad}
    print(f"[W22-T a] site degenerate <=> T_a u || v : {tot} checked, "
          f"{bad} violations")

    # ---- C-b: the h=2 witness criterion in transfer form ------------------
    tot = bad = 0
    stats = {"n_deg_hist": {}}
    for _ in range(3000):
        n = 6
        src = {e: [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
               for e in combinations(range(n), 2)}
        p, q = rng.sample(range(n), 2)
        U = tuple(x for x in range(n) if x not in (p, q))
        Ts = {a: transfer(src, p, q, a) for a in U}
        if any(t is None for t in Ts.values()):
            continue
        u = [rng.randint(-3, 3) for _ in range(3)]
        v = [rng.randint(-3, 3) for _ in range(3)]
        if all(x == 0 for x in u) or all(x == 0 for x in v):
            continue
        D = [a for a in U if parallel(mat_vec(Ts[a], u), v)]
        stats["n_deg_hist"][len(D)] = stats["n_deg_hist"].get(len(D), 0) + 1
        # transfer-form prediction of E = 0
        if len(D) == 4:
            rho = [ratio(mat_vec(Ts[a], u), v) for a in D]
            pred = (W.ehom(rho, [Fraction(1)] * 4, 2) == 0)
        elif len(D) == 3:
            rho = [ratio(mat_vec(Ts[a], u), v) for a in D]
            pred = (W.ehom(rho, [Fraction(1)] * 3, 1) == 0
                    and W.ehom(rho, [Fraction(1)] * 3, 2) == 0)
        else:
            pred = False
        got = (len(W.cap_error_direct(src, p, q, W.outer_K(u, v), U)) == 0)
        tot += 1
        bad += int(pred != got)
    RES["transfer_criterion"] = {"checked": tot, "violations": bad,
                                 **stats}
    print(f"[W22-T b] transfer-form h=2 criterion: {tot} checked, "
          f"{bad} violations; degeneracy-count histogram "
          f"{stats['n_deg_hist']}")

    # ---- C-c: the cocycle relation ---------------------------------------
    tot = bad = 0
    for _ in range(200):
        n = 8
        src = {e: [[rng.randint(-4, 4) for _ in range(3)] for _ in range(3)]
               for e in combinations(range(n), 2)}
        p, q = rng.sample(range(n), 2)
        U = [x for x in range(n) if x not in (p, q)]
        Ts = {a: transfer(src, p, q, a) for a in U}
        if any(t is None for t in Ts.values()):
            continue
        a, b, c = rng.sample(U, 3)
        if any(mat_inv(Ts[x]) is None for x in (a, b, c)):
            continue

        def H(x, y):
            return mat_mul(mat_inv(Ts[y]), Ts[x])
        prod = mat_mul(mat_mul(H(c, a), H(b, c)), H(a, b))
        tot += 1
        if any(prod[i][j] != (1 if i == j else 0)
               for i in range(3) for j in range(3)):
            bad += 1
    RES["cocycle"] = {"checked": tot, "violations": bad}
    print(f"[W22-COC] H^ca H^bc H^ab = id : {tot} checked, {bad} violations")

    # ---- C-d: complementary-diagonal TRANSPOSE-conjugacy -----------------
    # CORRECTED (the naive conjugacy form was refuted by this control):
    #   psi(x->y) := A_xy^T : V_x -> V_y,  and psi(y->x) = psi(x->y)^T
    #   (going backwards through a block is the INVERSE, not the transpose),
    # whence   H^{pq}_{ab} = [ psi(p->a) H^{ab}_{pq} psi(p->a)^{-1} ]^T .
    # So the two complementary diagonals of a 4-cycle are ISOSPECTRAL; the
    # eigenvectors of one are the LEFT eigenvectors of the other.
    tot = bad = badnaive = 0
    for _ in range(200):
        n = 8
        src = {e: [[rng.randint(-4, 4) for _ in range(3)] for _ in range(3)]
               for e in combinations(range(n), 2)}
        p, q, a, b = rng.sample(range(n), 4)
        Tpq_a, Tpq_b = transfer(src, p, q, a), transfer(src, p, q, b)
        Tab_p, Tab_q = transfer(src, a, b, p), transfer(src, a, b, q)
        if None in (Tpq_a, Tpq_b, Tab_p, Tab_q):
            continue
        if mat_inv(Tpq_b) is None or mat_inv(Tab_q) is None:
            continue
        Hpq = mat_mul(mat_inv(Tpq_b), Tpq_a)         # in GL(V_p)
        Hab = mat_mul(mat_inv(Tab_q), Tab_p)         # in GL(V_a)
        S = mat_T(W.oriented(src, p, a))             # psi(p->a) : V_p -> V_a
        Si = mat_inv(S)
        if Si is None:
            continue
        conj = mat_mul(mat_mul(S, Hpq), Si)
        pred = mat_T(conj)
        tot += 1
        if any(pred[i][j] != Hab[i][j] for i in range(3) for j in range(3)):
            bad += 1
        if all(conj[i][j] == Hab[i][j] for i in range(3) for j in range(3)):
            badnaive += 1
    RES["conjugacy"] = {"checked": tot, "violations_transpose_form": bad,
                        "naive_conjugacy_also_true": badnaive}
    print(f"[W22-C] H^pq_ab = (S H^ab_pq S^-1)^T : {tot} checked, {bad} "
          f"violations; naive (non-transposed) form held in {badnaive} "
          f"(control: must be 0)")

    # ---- C-e: incidence counts at general N ------------------------------
    inc = []
    for n in (6, 8, 10, 12, 14):
        pairs = n * (n - 1) // 2
        cycles_per_pair = (n - 2) * (n - 3) // 2
        blocks_per_pair = 2 * (n - 2) + 1
        # two pairs sharing a vertex share |star(p)| + 1 blocks
        share_vertex = (n - 1) + 1
        share_none = 4
        inc.append({"N": n, "h": n // 2 - 1, "pairs": pairs,
                    "blocks": pairs,
                    "4cycles_read_by_a_pair": cycles_per_pair,
                    "blocks_in_a_pair_criterion": blocks_per_pair,
                    "shared_blocks_pairs_meeting": share_vertex,
                    "shared_blocks_pairs_disjoint": share_none,
                    "block_appears_in_n_pair_criteria": 2 * (n - 2),
                    "criterion_dof_projective": 8,
                    "h2_conditions_per_pair": None})
    RES["incidence_counts"] = inc
    print("[incidence] counts:", json.dumps(inc[:3]))

    with open(f"{BASE}/results_t1d_incidence.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
