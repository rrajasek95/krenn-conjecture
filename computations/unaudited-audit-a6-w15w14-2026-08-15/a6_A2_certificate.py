#!/usr/bin/env python3
"""A6 / TARGET A step 3: the seven-word certificate, re-derived.

Everything here is built from a6_engine's fibre computation; the
normal forms are re-derived, the hand chain is re-derived by A6 (a
SHORTER chain than W15's is found), and an explicit cofactor identity
    mult * H_{0^8} = sum_i lambda_i H_{w_i}      in Z[full-block cells]
is verified by exact expansion.
"""
from __future__ import annotations

import json

import a6_engine as E

T = E.M24
V = E.Vars(T)
GM = set(E.gamma_matchings(T))
out = {}

W = [(1, 0, 0, 0, 0, 2, 0, 0),
     (1, 0, 0, 0, 1, 2, 0, 0),
     (1, 2, 0, 0, 0, 2, 0, 0),
     (1, 2, 0, 0, 1, 2, 0, 0),
     (0, 0, 0, 0, 1, 2, 0, 0),
     (1, 2, 0, 0, 0, 0, 0, 0)]
Z = (0,) * 8

singles = E.audit(T)["singles"]


def active_singles(w):
    return [e for e, c in singles.items() if w[e[0]] == c // 3 and w[e[1]] == c % 3]


out["words"] = []
for i, w in enumerate(W, 1):
    out["words"].append(dict(i=i, w="".join(map(str, w)),
                             mixed=len(set(w)) > 1,
                             fibre=len(E.fibre(T, w)),
                             fibre_is_FGamma=(set(E.fibre(T, w)) == GM),
                             active_single_cells=[list(e) for e in
                                                  active_singles(w)]))

Hs = [E.Hpoly(T, V, w) for w in W]
G = E.Hpoly(T, V, Z)


# ---------------------------------------------------------- named quantities
def c(u, v, i, j):
    return {(V.v(E.EIDX[(u, v)], 3 * i + j),): 1}


def mon(*ps):
    r = {(): 1}
    for p in ps:
        r = E.pmul(r, p)
    return r


U0, U1 = c(0, 7, 0, 0), c(0, 7, 1, 0)
V00, V01, V20, V21 = c(1, 4, 0, 0), c(1, 4, 0, 1), c(1, 4, 2, 0), c(1, 4, 2, 1)
C = c(2, 3, 0, 0)
S00, S20 = c(5, 6, 0, 0), c(5, 6, 2, 0)


def PL(x):
    return E.padd(E.padd(mon(c(0, 1, x[0], x[1]), c(2, 3, x[2], x[3])),
                         mon(c(0, 2, x[0], x[2]), c(1, 3, x[1], x[3]))),
                  mon(c(0, 3, x[0], x[3]), c(1, 2, x[1], x[2])))


def PR(y):
    return E.padd(mon(c(4, 5, y[0], y[1]), c(6, 7, y[2], y[3])),
                  mon(c(4, 7, y[0], y[3]), c(5, 6, y[1], y[2])))


L0, L1, L2 = PL((0, 0, 0, 0)), PL((1, 0, 0, 0)), PL((1, 2, 0, 0))
R0, Ra, Rb = PR((0, 0, 0, 0)), PR((0, 2, 0, 0)), PR((1, 2, 0, 0))
K, Kp, J, Jp = mon(U1, C, S20), mon(U0, C, S20), mon(U1, C, S00), mon(U0, C, S00)

NF = [("w1", Hs[0], E.padd(E.pmul(L1, Ra), E.pmul(K, V00))),
      ("w2", Hs[1], E.padd(E.pmul(L1, Rb), E.pmul(K, V01))),
      ("w3", Hs[2], E.padd(E.pmul(L2, Ra), E.pmul(K, V20))),
      ("w4", Hs[3], E.padd(E.pmul(L2, Rb), E.pmul(K, V21))),
      ("w5", Hs[4], E.padd(E.pmul(L0, Rb), E.pmul(Kp, V01))),
      ("w6", Hs[5], E.padd(E.pmul(L2, R0), E.pmul(J, V20))),
      ("0^8", G, E.padd(E.pmul(L0, R0), E.pmul(Jp, V00)))]
out["normal_forms_match"] = {n: (a == b) for n, a, b in NF}

M = E.psub(E.pmul(V00, V21), E.pmul(V01, V20))          # 2x2 minor of A14

# ---- identity (1): K^2 M = E1E4 - E2E3 - L2Rb E1 + L2Ra E2 + L1Rb E3 - L1Ra E4
E1, E2, E3, E4, E5, E6 = Hs
id1_lhs = E.pmul(E.pmul(K, K), M)
id1_rhs = E.padd(
    E.padd(E.psub(E.pmul(E1, E4), E.pmul(E2, E3)),
           E.psub(E.pmul(E.pmul(L2, Ra), E2), E.pmul(E.pmul(L2, Rb), E1))),
    E.psub(E.pmul(E.pmul(L1, Rb), E3), E.pmul(E.pmul(L1, Ra), E4)))
out["identity1_K2_minor"] = (id1_lhs == id1_rhs)

# ---- A6's OWN chain (shorter).  L2 Rb G  =  [E5E6 - K'V01 E6 - J V20 E5
#      + J'V00 E4] - J K' M      and   L2 Rb = E4 - K V21, so
#      K V21 G = E4 G - L2 Rb G, giving K^3 V21 G in the ideal.
lhsA = E.pmul(E.pmul(L2, Rb), G)
rhsA = E.psub(E.padd(E.padd(E.pmul(E5, E6),
                            E.pneg({m: c for m, c in
                                    E.pmul(E.pmul(Kp, V01), E6).items()})),
                     E.padd(E.pneg({m: c for m, c in
                                    E.pmul(E.pmul(J, V20), E5).items()}),
                            E.pmul(E.pmul(Jp, V00), E4))),
              E.pmul(E.pmul(J, Kp), M))
out["A6_identity_L2Rb_G"] = (lhsA == rhsA)

# assemble:  K^3 V21 G = K^2 (E4 G) - K^2*[E5E6 - K'V01E6 - JV20E5 + J'V00E4]
#                        + J K' * (K^2 M)   with K^2 M replaced by id1_rhs
mult_A6 = E.pmul(E.pmul(E.pmul(K, K), K), V21)
lhsB = E.pmul(mult_A6, G)
brack = E.padd(E.padd(E.pmul(E5, E6),
                      E.pneg(E.pmul(E.pmul(Kp, V01), E6))),
               E.padd(E.pneg(E.pmul(E.pmul(J, V20), E5)),
                      E.pmul(E.pmul(Jp, V00), E4)))
rhsB = E.padd(E.psub(E.pmul(E.pmul(K, K), E.pmul(E4, G)),
                     E.pmul(E.pmul(K, K), brack)),
              E.pmul(E.pmul(J, Kp), id1_rhs))
out["A6_multiplier_K3_V21_membership"] = (lhsB == rhsB)
out["A6_multiplier"] = "A07[1][0]^3*A23[0][0]^3*A56[2][0]^3*A14[2][1]"
out["W15_multiplier"] = "A07[1][0]^4*A23[0][0]^3*A56[2][0]^3*A14[2][1]^2"

# W15's multiplier follows: multiply A6's identity by U1*V21
multW = E.pmul(E.pmul(E.pmul(E.pmul(K, K), K), U1), E.pmul(V21, V21))
out["W15_multiplier_equals_A6_times_U1V21"] = (
    multW == E.pmul(mult_A6, E.pmul(U1, V21)))

# ------------------------------------------------- explicit cofactor witness
# Collect lambda_i explicitly from rhsB, then re-verify by expansion.
lam = {i: {} for i in range(6)}


def addlam(i, p):
    lam[i] = E.padd(lam[i], p)


# K^2 E4 G
addlam(3, E.pmul(E.pmul(K, K), G))
# - K^2 [E5E6 - K'V01 E6 - J V20 E5 + J' V00 E4]
addlam(4, E.pneg(E.pmul(E.pmul(K, K), E6)))              # -K^2 E5*E6 (put on E5)
addlam(5, E.pmul(E.pmul(K, K), E.pmul(Kp, V01)))          # +K^2 K'V01 E6
addlam(4, E.pmul(E.pmul(K, K), E.pmul(J, V20)))           # +K^2 J V20 E5
addlam(3, E.pneg(E.pmul(E.pmul(K, K), E.pmul(Jp, V00))))  # -K^2 J'V00 E4
# + J K' * (E1E4 - E2E3 - L2Rb E1 + L2Ra E2 + L1Rb E3 - L1Ra E4)
JK = E.pmul(J, Kp)
addlam(0, E.pmul(JK, E.psub(E4, E.pmul(L2, Rb))))
addlam(1, E.pmul(JK, E.psub(E.pmul(L2, Ra), E3)))
addlam(2, E.pmul(JK, E.pmul(L1, Rb)))
addlam(3, E.pneg(E.pmul(JK, E.pmul(L1, Ra))))

chk = {}
acc = {}
for i in range(6):
    acc = E.padd(acc, E.pmul(lam[i], Hs[i]))
out["explicit_cofactor_identity_verified"] = (acc == E.pmul(mult_A6, G))
out["cofactor_sizes"] = {f"lambda{i+1}": len(lam[i]) for i in range(6)}
out["all_six_cofactors_nonzero"] = all(lam[i] for i in range(6))

# ------------------------------------------------------- mutation controls
mc = {}
# M1: wrong sign in identity (1)
bad1 = E.padd(
    E.padd(E.padd(E.pmul(E1, E4), E.pmul(E2, E3)),
           E.psub(E.pmul(E.pmul(L2, Ra), E2), E.pmul(E.pmul(L2, Rb), E1))),
    E.psub(E.pmul(E.pmul(L1, Rb), E3), E.pmul(E.pmul(L1, Ra), E4)))
mc["sign_mutation_of_identity1_fails"] = (id1_lhs != bad1)
# M2: drop one cofactor term from the assembled identity
mc["dropping_JK_term_fails"] = (
    E.psub(E.pmul(E.pmul(K, K), E.pmul(E4, G)),
           E.pmul(E.pmul(K, K), brack)) != lhsB)
# M3: swap one certificate word for a neighbour -> normal form must change
alt = (1, 0, 0, 0, 0, 2, 0, 1)
mc["alt_word_10000201_fibre"] = len(E.fibre(T, alt))
mc["alt_word_H_differs_from_w1"] = (E.Hpoly(T, V, alt) != E1)
# M4: a smaller multiplier K^2 V21 must NOT be produced by this chain
mc["K2V21_chain_identity_holds"] = (
    E.pmul(E.pmul(E.pmul(K, K), V21), G) == rhsB)   # expect False
out["mutation_controls"] = mc

json.dump(out, open("results_A2_certificate.json", "w"), indent=1)
print(json.dumps(out, indent=1))

# --------------------------------------------------- A6's REDUCED certificate
# Every cofactor above is divisible by K, so the identity divides through:
#   K^2 V21 G = K J' V21 E1 - K J' V20 E2 + J' L1 Rb E3
#               + (K L0 R0 - J' L1 Ra) E4 - K L2 R0 E5 + K K' V01 E6
red = {}
red_cof = [E.pmul(E.pmul(K, Jp), V21),
           E.pneg(E.pmul(E.pmul(K, Jp), V20)),
           E.pmul(E.pmul(Jp, L1), Rb),
           E.psub(E.pmul(K, E.pmul(L0, R0)), E.pmul(E.pmul(Jp, L1), Ra)),
           E.pneg(E.pmul(K, E.pmul(L2, R0))),
           E.pmul(E.pmul(K, Kp), V01)]
acc2 = {}
for i in range(6):
    acc2 = E.padd(acc2, E.pmul(red_cof[i], Hs[i]))
mult_red = E.pmul(E.pmul(K, K), V21)
res = {"A6_reduced_multiplier": "A07[1][0]^2*A23[0][0]^2*A56[2][0]^2*A14[2][1]",
       "A6_reduced_identity_verified": (acc2 == E.pmul(mult_red, G)),
       "reduced_cofactor_sizes": [len(x) for x in red_cof],
       # control: the same cofactors against a mutated E1 must fail
       "control_mutated_E1_breaks_reduced": (
           E.padd(E.pmul(red_cof[0], E.padd(Hs[0], {((0,)): 1})),
                  E.padd(*[{}]) if False else
                  {m: c for m, c in
                   E.padd(*[{}]).items()} if False else
                  {}) != {}),
       }
acc3 = E.pmul(red_cof[0], E.padd(Hs[0], {(0,): 1}))
for i in range(1, 6):
    acc3 = E.padd(acc3, E.pmul(red_cof[i], Hs[i]))
res["control_mutated_E1_breaks_reduced"] = (acc3 != E.pmul(mult_red, G))
print(json.dumps(res, indent=1))
json.dump(res, open("results_A2b_reduced.json", "w"), indent=1)
