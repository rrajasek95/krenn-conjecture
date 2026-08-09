#!/usr/bin/env python3
"""Exact O4 target-line alignment obstruction in characteristic zero."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_FOUR_STAR_SHA256 = (
    "cffd8ac0c5d54fddd365e4a610f2bed00881683a61733669e2bb41af972ecad1"
)
SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_four_star_lemma.py"
)
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_FOUR_STAR_SHA256,
            "the pinned O4 four-star checker changed")
F = importlib.import_module("verify_n8_d1_residue_orbit4_four_star_lemma")
S, C, D, V, O = F.S, F.C, F.D, F.V, F.O

EXPECTED_LEDGER_SHA256 = (
    "1b869666b0b59178b6d3fd5b9122c5df6de25a349fae08dc44ccf7b57180ec19"
)


def var(name):
    return D.p_var(name)


def add(*values):
    result = D.p_const(0)
    for value in values:
        result = D.p_add(result, value)
    return result


def mul(*values):
    result = D.p_const(1)
    for value in values:
        result = D.p_mul(result, value)
    return result


def scale(integer, polynomial):
    return D.p_mul(D.p_const(integer), polynomial)


def trace(polynomial):
    return [[list(monomial), str(coefficient)]
            for monomial, coefficient in sorted(polynomial.items())]


def aligned_family():
    c = tuple(var("c%d" % index) for index in range(3))
    eta = var("eta")
    target = (D.p_const(0), D.p_const(0), D.p_const(1))
    e = (D.p_const(0), D.p_const(0), eta)
    b = tuple(var("b%d" % index) for index in range(3))
    d = tuple(var("d%d" % index) for index in range(3))
    alpha = (var("alpha0"), var("alpha1"))
    A = S.matrix_add(
        S.outer(target, target),
        S.matrix_scale(D.p_const(-1), S.outer(b, e)),
        S.matrix_scale(D.p_const(-1), S.outer(c, d)),
    )
    B = tuple(tuple(D.p_mul(alpha[column], c[row])
                    if column < 2 else b[row]
                    for column in range(3)) for row in range(3))
    D56 = tuple(tuple(D.p_neg(D.p_mul(alpha[column], e[row]))
                      if column < 2 else d[row]
                      for column in range(3)) for row in range(3))
    return c, eta, e, b, d, alpha, target, A, B, D56


def injectivity_audit():
    c, _eta, _e, _b, d, alpha, _target, A, B, D56 = aligned_family()
    matrix = []
    for i, j, k in itertools.product(range(3), repeat=3):
        row = [D.p_const(0) for _ in range(9)]
        row[i] = D56[j][k]
        row[3 + j] = B[i][k]
        row[6 + k] = A[i][j]
        matrix.append(tuple(row))
    base_rows = (
        (0, 0, 0), (0, 0, 1), (0, 0, 2),
        (0, 1, 0), (0, 2, 0), (1, 0, 2),
        (2, 0, 2), (2, 2, 0), (2, 2, 2),
    )
    rows = []
    for i, j, k in itertools.product((0, 1), repeat=3):
        def swap_zero(value, image):
            if value == 0:
                return image
            if value == image:
                return 0
            return value

        pivot_rows = tuple(
            9 * swap_zero(x, i)
            + 3 * swap_zero(y, j)
            + swap_zero(z, k)
            for x, y, z in base_rows
        )
        determinant = S.determinant(
            tuple(matrix[position] for position in pivot_rows)
        )
        expected = mul(
            alpha[k], alpha[k], alpha[k],
            c[i], c[i], c[i], c[i],
            d[j], d[j], d[j], d[j],
        )
        sign = -1 if (i + j + k) % 2 else 1
        require(determinant
                == (D.p_neg(expected) if sign < 0 else expected),
                "an aligned-tripod injectivity minor changed")
        rows.append({
            "indices": [i, j, k],
            "pivot_rows": list(pivot_rows),
            "sign": sign,
            "factorization": "alpha%d^3*c%d^4*d%d^4" % (k, i, j),
            "sha256": D.content_hash(trace(determinant)),
        })
    require(len(rows) == 8, "the aligned minor orbit changed")
    return rows


def reduced_tensor_audit():
    c, eta, e, _b, _d, _alpha, target, A, B, D56 = aligned_family()
    P4 = tuple(var("p4%d" % index) for index in range(3))
    P5 = tuple(var("p5%d" % index) for index in range(3))
    P6 = tuple(var("p6%d" % index) for index in range(3))
    tau = var("tau")
    reduced = S.tensor3_add(
        S.tensor3_scale(tau, S.phi_tensor(P4, P5, P6, A, B, D56)),
        S.tensor3_scale(
            D.p_const(-2), S.psi_tensor(P4, P5, P6, c, e, target)
        ),
    )
    expected_tau_zero = scale(-2, mul(c[0], P5[0], P6[0]))
    actual_tau_zero = {
        monomial: coefficient
        for monomial, coefficient in reduced[0][0][0].items()
        if "tau" not in monomial
    }
    require(actual_tau_zero == expected_tau_zero,
            "the aligned tau-zero monomial changed")
    return {
        "reduced_equation": "tau*Phi(P)-2*Psi(P)=0",
        "direct_edge": "zero; no w term",
        "tau_zero_witness": trace(actual_tau_zero),
        "alignment": "e=eta*e2",
    }


def scalar_elimination_audit():
    kappa, mu = var("kappa"), var("mu")
    L, N, Z = var("L"), var("N"), var("Z")
    (cvec, eta, _e, bvec, dvec, alpha, target,
     A, B, D56) = aligned_family()
    c, b, d = cvec[0], bvec[0], dvec[2]
    q = mul(kappa, mu)
    one = D.p_const(1)

    def cleared_generic(N_value):
        plus = add(one, q)
        minus = add(one, D.p_neg(q))
        X = tuple(add(
            mul(kappa, add(target[index],
                           D.p_neg(mul(eta, bvec[index])))),
            mul(L, cvec[index]),
        ) for index in range(3))
        Y = tuple(add(mul(kappa, dvec[index]),
                      mul(N_value, target[index]))
                  for index in range(3))
        alpha_vector = (alpha[0], alpha[1], D.p_const(0))
        Zvec = tuple(add(mul(kappa, alpha_vector[index]),
                         mul(Z, target[index]))
                     for index in range(3))
        out = []
        for i in range(3):
            plane = []
            for j in range(3):
                row = []
                for k in range(3):
                    row.append(add(
                        mul(minus, X[i], D56[j][k]),
                        mul(eta, plus, B[i][k], Y[j]),
                        mul(eta, plus, minus, A[i][j], Zvec[k]),
                        D.p_neg(mul(mu, X[i], Y[j], target[k])),
                        D.p_neg(mul(mu, eta, minus, X[i],
                                    target[j], Zvec[k])),
                        D.p_neg(mul(mu, eta, plus, cvec[i],
                                    Y[j], Zvec[k])),
                    ))
                plane.append(tuple(row))
            out.append(tuple(plane))
        return tuple(out)

    general_tensor = cleared_generic(N)
    expected_L_minus_N = mul(
        alpha[0], c, eta, add(L, D.p_neg(N)),
        add(q, D.p_const(-1)), add(q, one),
    )
    require(general_tensor[0][2][0] == expected_L_minus_N,
            "the L=N aligned coefficient changed")

    # Generic q != +/-1 branch.  These are one non-target coefficient E
    # and its target companion T after zbar=kappa*alphabar and L=N.
    E = add(
        mul(c, add(
            mul(L, add(one, scale(-2, q))),
            D.p_neg(mul(Z, eta, add(one, q))),
        )),
        scale(3, mul(b, eta, kappa, kappa, mu)),
    )
    T = add(
        D.p_neg(mul(L, L, c, mu)),
        mul(L, Z, c, eta, kappa, mu, mu),
        D.p_neg(mul(L, Z, c, eta, mu)),
        scale(-2, mul(L, c, d, kappa, mu)),
        mul(L, c, d),
        D.p_neg(mul(L, Z, c, eta, kappa, mu, mu)),
        D.p_neg(mul(L, Z, c, eta, mu)),
        scale(2, mul(L, b, eta, kappa, mu)),
        mul(L, b, eta),
        mul(Z, b, eta, eta, kappa, mu),
        D.p_neg(mul(Z, b, eta, eta)),
        D.p_neg(mul(Z, c, d, eta, kappa, mu)),
        D.p_neg(mul(Z, c, d, eta)),
        scale(3, mul(b, d, eta, kappa, kappa, mu)),
    )
    specialized_tensor = cleared_generic(L)
    require(specialized_tensor[0][0][2] == mul(dvec[0], E)
            and specialized_tensor[0][2][2] == T,
            "the generic aligned scalar coefficients left the tensor")
    cofactor = add(
        scale(2, mul(L, kappa, mu)), L,
        mul(Z, eta, kappa, mu), D.p_neg(mul(Z, eta)),
        scale(3, mul(d, kappa, kappa, mu)),
    )
    generic_identity = add(
        scale(3, mul(kappa, kappa, mu, T)),
        D.p_neg(mul(cofactor, E)),
        D.p_neg(mul(
            c, mul(add(L, D.p_neg(mul(Z, eta))),
                   add(L, D.p_neg(mul(Z, eta)))),
            add(q, D.p_const(-1)), add(q, one),
        )),
    )
    require(not generic_identity,
            "the generic target-alignment elimination identity changed")

    # Exceptional q=-1 branch after its first coefficient gives s=-r.
    r, x = var("r"), var("x")
    U = add(mul(Z, eta), mul(kappa, r))
    Eminus = add(scale(3, mul(eta, x)), D.p_neg(mul(c, U)))
    numerator = add(
        D.p_neg(mul(Z, c, d, eta, kappa)),
        mul(Z, c, eta, kappa, r),
        scale(2, mul(Z, eta, eta, x)),
        D.p_neg(mul(c, d, kappa, kappa, r)),
        mul(c, kappa, kappa, r, r),
        scale(3, mul(d, eta, kappa, x)),
        D.p_neg(mul(eta, kappa, r, x)),
    )

    # Reconstruct 2*eta*kappa times the q=-1 tensor after the preceding
    # coefficient has imposed eta*b=e2-r*c and y=kappa*(d-r*e2)/2.
    Bnumerator = tuple(add(target[index],
                           D.p_neg(mul(r, cvec[index])))
                       for index in range(3))
    Ynumerator = tuple(mul(
        kappa, add(dvec[index], D.p_neg(mul(r, target[index])))
    ) for index in range(3))
    alpha_vector = (alpha[0], alpha[1], D.p_const(0))
    Zvec = tuple(add(mul(kappa, alpha_vector[index]),
                     mul(Z, target[index]))
                 for index in range(3))
    Xvec = (x, var("x1"), var("x2"))
    exceptional = []
    for i in range(3):
        plane = []
        for j in range(3):
            row = []
            for k in range(3):
                row.append(add(
                    scale(-2, mul(eta, eta, kappa, Xvec[i],
                                  target[j], alpha_vector[k])),
                    scale(2, mul(eta, kappa, Xvec[i], dvec[j],
                                 target[k])),
                    mul(eta, kappa, cvec[i], Ynumerator[j],
                        alpha_vector[k]),
                    mul(kappa, Bnumerator[i], Ynumerator[j], target[k]),
                    scale(2, mul(eta, kappa, target[i], target[j],
                                 Zvec[k])),
                    scale(-2, mul(eta, kappa, Bnumerator[i], target[j],
                                  Zvec[k])),
                    scale(-2, mul(eta, kappa, cvec[i], dvec[j], Zvec[k])),
                    mul(eta, Xvec[i], Ynumerator[j], target[k]),
                    scale(2, mul(eta, eta, Xvec[i], target[j], Zvec[k])),
                    mul(eta, cvec[i], Ynumerator[j], Zvec[k]),
                ))
            plane.append(tuple(row))
        exceptional.append(tuple(plane))
    exceptional = tuple(exceptional)
    require(exceptional[0][0][2] == mul(kappa, dvec[0], Eminus)
            and exceptional[0][2][2] == numerator,
            "the q=-1 scalar coefficients left the tensor")
    exceptional_cofactor = add(
        scale(2, mul(Z, eta)), scale(3, mul(d, kappa)),
        D.p_neg(mul(kappa, r)),
    )
    exceptional_identity = add(
        scale(3, numerator),
        D.p_neg(mul(exceptional_cofactor, Eminus)),
        scale(-2, mul(c, U, U)),
    )
    require(not exceptional_identity,
            "the q=-1 target-alignment identity changed")
    return {
        "generic_identity": (
            "3*kappa^2*mu*T-Q*E="
            "c*(L-Z*eta)^2*(kappa*mu-1)*(kappa*mu+1)"
        ),
        "generic_conclusion": (
            "away from kappa*mu=+/-1, L=Z*eta and E=0 force "
            "the localized non-target coordinate of P4 to vanish"
        ),
        "q_plus_one": (
            "(1-kappa*mu)P5=kappa*d+N*e2 forces a localized "
            "non-target coordinate of d to vanish"
        ),
        "q_minus_one_identity": (
            "3*Tminus-Qminus*Eminus=2*c*(Z*eta+kappa*r)^2"
        ),
        "q_minus_one_conclusion": (
            "the square identity and Eminus=0 force the localized "
            "non-target coordinate of P4 to vanish"
        ),
    }


def clause_audit():
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    allowed = (set(admissible) - set(O.RESIDUE_HOLES)
               - set(S.BOUNDARY_OMISSIONS))
    clauses = []
    for alignment in ("e_target", "c_target"):
        alignment_holes = (
            (V.cell(5, 7, 0, 2), V.cell(5, 7, 1, 2))
            if alignment == "e_target"
            else (V.cell(4, 7, 0, 2), V.cell(4, 7, 1, 2))
        )
        for u, v in ((0, 2), (1, 3)):
            for left_colour in (0, 1):
                for right_colour in V.COLORS:
                    direct = V.cell(u, v, left_colour, right_colour)
                    for i, j, k, ell in itertools.product((0, 1), repeat=4):
                        if alignment == "e_target":
                            residue = (
                                V.cell(4, 6, i, k),
                                V.cell(4, 7, i, 2),
                                V.cell(5, 6, j, 2),
                            )
                            star = (
                                V.cell(u, 4, left_colour, i),
                                V.cell(u, 5, left_colour, j),
                                V.cell(u, 6, left_colour, k),
                            )
                        else:
                            residue = (
                                V.cell(5, 6, i, k),
                                V.cell(5, 7, i, 2),
                                V.cell(4, 6, j, 2),
                            )
                            star = (
                                V.cell(u, 5, left_colour, i),
                                V.cell(u, 4, left_colour, j),
                                V.cell(u, 6, left_colour, k),
                            )
                        ratio = (
                            V.cell(u, 7, left_colour, ell),
                            V.cell(v, 7, right_colour, ell),
                        )
                        witnesses = residue + star + ratio
                        require(len(set(witnesses)) == 8
                                and set(witnesses) <= allowed
                                and direct in allowed,
                                "an aligned support clause changed")
                        clauses.append({
                            "alignment": alignment,
                            "domain": [u, v] + list(V.RESIDUE),
                            "boundary_colours": [left_colour, right_colour],
                            "indices": [i, j, k, ell],
                            "alignment_holes": [list(cell)
                                                for cell in alignment_holes],
                            "direct_edge_hole": list(direct),
                            "localized_witnesses": [list(cell)
                                                    for cell in witnesses],
                            "cnf_clause": (
                                [list(cell) for cell in alignment_holes]
                                + [list(direct)]
                                + [["not"] + list(cell)
                                   for cell in witnesses]
                            ),
                        })
    require(len(clauses) == 384,
            "the target-alignment clause census changed")
    return clauses


def build_ledger():
    return {
        "pinned_four_star_sha256": PINNED_FOUR_STAR_SHA256,
        "aligned_tripod_minors": injectivity_audit(),
        "reduced_tensor": reduced_tensor_audit(),
        "scalar_elimination": scalar_elimination_audit(),
        "transported_support_clauses": clause_audit(),
        "clause_count": 384,
        "clause_shape": (
            "two positive alignment escapes, one positive direct-edge "
            "escape, and eight negative localized witnesses"
        ),
        "symmetry": "both e-target and c-target alignments; W1 and W2",
        "characteristic_scope": "every field of characteristic not 2 or 3",
        "status": (
            "the target-aligned O4 six-site chart is empty whenever the "
            "named direct cell is absent and the eight witnesses are units"
        ),
    }


def main():
    started = monotonic()
    ledger = build_ledger()
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the O4 target-alignment ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("O4 target-alignment lemma: PASS (char != 2,3)")
    print("transported support clauses: 384")
    print("elapsed: %.3fs" % (monotonic() - started))


if __name__ == "__main__":
    main()
