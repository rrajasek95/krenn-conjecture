#!/usr/bin/env python3
"""Z-optional four-star O4 six-site obstruction in characteristic not two."""

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


PINNED_SIX_SITE_SHA256 = (
    "85c5959e6fbf13939ec41884d95fb625701920241198989500ebf8f5f209ef19"
)
SOURCE = os.path.join(HERE,
                      "verify_n8_d1_residue_orbit4_six_site_closure.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_SIX_SITE_SHA256,
            "the pinned O4 six-site checker changed")
S = importlib.import_module("verify_n8_d1_residue_orbit4_six_site_closure")
C, D, V, O = S.C, S.D, S.V, S.O

EXPECTED_LEDGER_SHA256 = (
    "fef45ef653c790a79c1517d38cb3298a0e5ed52c336663ba7955bde26100c275"
)


def polynomial_trace(polynomial):
    return [[list(monomial), str(coefficient)]
            for monomial, coefficient in sorted(polynomial.items())]


def matrix_equal(left, right):
    return all(a == b for row0, row1 in zip(left, right)
               for a, b in zip(row0, row1))


def reduced_tensor_audit():
    c, e, b, d, alpha, target, A, B, D56, blocks = S.family_data()
    injectivity = S.phi_injectivity_audit(A, B, D56, alpha, c, e, b, d)
    raw_reduction = S.six_site_reduction_audit(
        c, e, alpha, target, A, B, D56, blocks
    )
    P4 = tuple(S.var("p4%d" % index) for index in range(3))
    P5 = tuple(S.var("p5%d" % index) for index in range(3))
    P6 = tuple(S.var("p6%d" % index) for index in range(3))
    tau, w = S.var("tau"), S.var("w")
    phi = S.phi_tensor(P4, P5, P6, A, B, D56)
    psi = S.psi_tensor(P4, P5, P6, c, e, target)
    reduced = S.tensor3_add(
        S.outer3(target, target, S.vector_scale(w, target)),
        S.tensor3_scale(tau, phi),
        S.tensor3_scale(D.p_const(-2), psi),
    )

    # tau != 0: one non-target site-6 slice writes A as a sum of two
    # decomposables.  No occurrence of w is present in this slice.
    slice0 = tuple(tuple(reduced[i][j][0] for j in range(3))
                   for i in range(3))
    expected_slice0 = S.matrix_add(
        S.matrix_scale(D.p_mul(tau, P6[0]), A),
        S.matrix_scale(D.p_neg(D.p_add(
            D.p_mul(tau, alpha[0]),
            D.p_mul(D.p_const(2), P6[0]))), S.outer(P4, e)),
        S.matrix_scale(D.p_sub(
            D.p_mul(tau, alpha[0]),
            D.p_mul(D.p_const(2), P6[0])), S.outer(c, P5)),
    )
    require(matrix_equal(slice0, expected_slice0),
            "the w-free tau-nonzero slice changed")
    require(all("w" not in monomial for entry in slice0 for monomial in entry),
            "the direct boundary edge entered the non-target slice")

    # tau = 0: the same slice is -2*p60*(P4 tensor e+c tensor P5).
    tau_zero_slice = tuple(tuple(
        D.p_sub(entry, D.p_mul(tau, D.p_const(0)))
        for entry in row) for row in slice0)
    # Substitute tau=0 by rebuilding the expected polynomial directly; the
    # actual substitution just drops monomials containing tau.
    def set_tau_zero(poly):
        return {monomial: coefficient for monomial, coefficient in poly.items()
                if "tau" not in monomial}

    tau_zero_slice = tuple(tuple(set_tau_zero(entry) for entry in row)
                           for row in slice0)
    expected_tau_zero = S.matrix_scale(
        D.p_mul(D.p_const(-2), P6[0]),
        S.matrix_add(S.outer(P4, e), S.outer(c, P5)),
    )
    require(matrix_equal(tau_zero_slice, expected_tau_zero),
            "the tau-zero non-target slice changed")

    # The rank-one relation gives P4=kappa*c, P5=-kappa*e.  Check that the
    # target slice retains arbitrary w and becomes w*E22+2*kappa^2*c*e.
    kappa = S.var("kappa")
    specialized_psi = S.psi_tensor(
        S.vector_scale(kappa, c),
        S.vector_scale(D.p_neg(kappa), e),
        P6, c, e, target,
    )
    target_slice = S.matrix_add(
        S.outer(target, S.vector_scale(w, target)),
        S.matrix_scale(D.p_const(-2),
                       tuple(tuple(specialized_psi[i][j][2]
                                   for j in range(3)) for i in range(3))),
    )
    expected_target_slice = S.matrix_add(
        S.outer(target, S.vector_scale(w, target)),
        S.matrix_scale(
            D.p_mul(D.p_const(2), D.p_mul(kappa, kappa)),
            S.outer(c, e)),
    )
    require(matrix_equal(target_slice, expected_target_slice),
            "the w-optional tau-zero target slice changed")

    return {
        "tripod_minor": injectivity["determinant"],
        "raw_matching_reduction_sha256": raw_reduction[
            "reduced_tensor_sha256"
        ],
        "reduced_equation": "w*E222+tau*Phi(P)-2*Psi(P)=0",
        "w_assumption": "none: w may vanish",
        "tau_nonzero": (
            "p60,tau nonzero express A as L*(P4 tensor e)+M*(c tensor P5); "
            "E22=A+b tensor e+c tensor d contradicts c0,e0 nonzero"
        ),
        "tau_zero": (
            "in characteristic not 2, p60 gives P4 tensor e+c tensor P5=0; "
            "p40 makes kappa nonzero, and the target slice "
            "w*E22+2*kappa^2*c tensor e=0 is impossible modulo <c>"
        ),
        "slice0_sha256": D.content_hash(
            [[polynomial_trace(entry) for entry in row] for row in slice0]
        ),
        "target_slice_sha256": D.content_hash(
            [[polynomial_trace(entry) for entry in row]
             for row in target_slice]
        ),
    }


def minor_orbit_audit():
    c, e, _b, _d, alpha, _target, A, B, D56, _blocks = S.family_data()
    matrix = []
    for i, j, k in itertools.product(range(3), repeat=3):
        row = [D.p_const(0) for _ in range(9)]
        row[i] = D56[j][k]
        row[3 + j] = B[i][k]
        row[6 + k] = A[i][j]
        matrix.append(tuple(row))
    minor_families = {
        "non_target_corner": (
            ((0, 0, 0), (0, 0, 1), (0, 0, 2),
             (0, 1, 0), (0, 2, 0), (1, 0, 0),
             (2, 0, 0), (2, 2, 0), (2, 2, 2)),
            lambda i, j: (i, j),
        ),
        "target_column": (
            ((0, 0, 0), (0, 1, 0), (0, 2, 0),
             (0, 2, 1), (0, 2, 2), (1, 0, 0),
             (2, 0, 0), (2, 2, 0), (2, 2, 2)),
            lambda i, _j: (i, 2),
        ),
        "target_row": (
            ((0, 0, 0), (0, 1, 0), (0, 2, 0),
             (1, 0, 0), (2, 0, 0), (2, 0, 1),
             (2, 0, 2), (2, 2, 0), (2, 2, 2)),
            lambda _i, j: (2, j),
        ),
    }
    rows = []
    for family, (base_rows, A_indices) in minor_families.items():
        for i, j, k in itertools.product((0, 1), repeat=3):
            def swap_zero(value, image):
                if value == 0:
                    return image
                if value == image:
                    return 0
                return value

            pivot_rows = tuple(
                swap_zero(x, i) * 9
                + swap_zero(y, j) * 3
                + swap_zero(z, k)
                for x, y, z in base_rows
            )
            ai, aj = A_indices(i, j)
            minor = S.determinant(
                tuple(matrix[index] for index in pivot_rows)
            )
            expected = S.product(
                alpha[k], alpha[k], alpha[k], alpha[k], alpha[k],
                c[i], c[i], e[j], e[j], A[ai][aj], A[ai][aj],
            )
            sign = -1 if (i + j + k) % 2 else 1
            require(minor == (D.p_neg(expected) if sign < 0 else expected),
                    "a transported O4 tripod minor changed")
            rows.append({
                "family": family,
                "indices": [i, j, k],
                "A_indices": [ai, aj],
                "pivot_rows": list(pivot_rows),
                "sign": sign,
                "factorization": (
                    "alpha%d^5*c%d^2*e%d^2*A45_%d%d^2"
                    % (k, i, j, ai, aj)
                ),
                "sha256": D.content_hash(polynomial_trace(minor)),
            })
    require(len(rows) == 24, "the transported minor census changed")
    return rows


def clause_audit():
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    allowed = (set(admissible) - set(O.RESIDUE_HOLES)
               - set(S.BOUNDARY_OMISSIONS))
    clauses = []
    minors = minor_orbit_audit()
    for u, v in ((0, 2), (1, 3)):
        for left_colour in (0, 1):
            for right_colour in V.COLORS:
                for minor in minors:
                    i, j, k = minor["indices"]
                    ai, aj = minor["A_indices"]
                    for ell in (0, 1):
                        residue_witnesses = (
                            V.cell(4, 6, i, k),
                            V.cell(4, 7, i, 2),
                            V.cell(5, 7, j, 2),
                            V.cell(4, 5, ai, aj),
                        )
                        boundary = (
                            V.cell(u, 7, left_colour, ell),
                            V.cell(v, 7, right_colour, ell),
                            V.cell(u, 6, left_colour, k),
                            V.cell(u, 4, left_colour, i),
                        )
                        antecedent = residue_witnesses + boundary
                        require(len(set(antecedent)) == 8
                                and set(antecedent) <= allowed,
                                "a four-star support antecedent changed")
                        clauses.append({
                            "domain": [u, v] + list(V.RESIDUE),
                            "boundary_colours": [left_colour, right_colour],
                            "minor_family": minor["family"],
                            "minor_indices": [i, j, k],
                            "A_indices": [ai, aj],
                            "site7_ratio_coordinate": ell,
                            "residue_witnesses": [
                                list(cell) for cell in residue_witnesses
                            ],
                            "boundary_star_witnesses": [
                                list(cell) for cell in boundary
                            ],
                            "support_clause": [
                                list(cell) for cell in antecedent
                            ],
                        })
    require(len(clauses) == 576,
            "the four-star transported clause census changed")
    return clauses


def build_ledger():
    clauses = clause_audit()
    return {
        "pinned_six_site_sha256": PINNED_SIX_SITE_SHA256,
        "algebra": reduced_tensor_audit(),
        "tripod_minor_orbit": minor_orbit_audit(),
        "transported_support_clauses": clauses,
        "antecedent_size": 8,
        "boundary_star_units": ["p7_ell", "q7_ell", "p6_k", "p4_i"],
        "direct_edge_localized": False,
        "base_ring_scope": (
            "polynomial over Z through the tensor reduction; the final "
            "tau=0 contradiction uses 2 invertible"
        ),
        "characteristic_scope": "every field of characteristic not 2",
        "conclusion": (
            "no O4 support may contain all eight witnesses of any transported "
            "four-star antecedent, whether or not the direct boundary edge lives"
        ),
    }


def main():
    started = monotonic()
    ledger = build_ledger()
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256: %s" % digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the O4 four-star lemma ledger changed")
        print("ledger sha256 (frozen): %s" % digest)
    print("O4 z-optional four-star lemma: PASS (char != 2)")
    print("transported support clauses: 576 of size 8")
    print("elapsed: %.3fs" % (monotonic() - started))


if __name__ == "__main__":
    main()
