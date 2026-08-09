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
    "44c46b173b15be66006817d7ca0aea4d4aa036be31e80369e34588e625e17eb9"
)
RESIDUE_WITNESSES = (
    (4, 6, 0, 0),  # alpha0*c0
    (4, 7, 0, 2),  # c0
    (5, 7, 0, 2),  # e0
    (4, 5, 0, 0),  # A00
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


def clause_audit():
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    allowed = (set(admissible) - set(O.RESIDUE_HOLES)
               - set(S.BOUNDARY_OMISSIONS))
    clauses = []
    for u, v in ((0, 2), (1, 3)):
        for left_colour in (0, 1):
            for right_colour in V.COLORS:
                boundary = (
                    V.cell(u, 7, left_colour, 0),  # p70
                    V.cell(v, 7, right_colour, 0),  # q70
                    V.cell(u, 6, left_colour, 0),  # p60
                    V.cell(u, 4, left_colour, 0),  # p40
                )
                antecedent = tuple(RESIDUE_WITNESSES) + boundary
                require(len(set(antecedent)) == 8 and set(antecedent) <= allowed,
                        "a four-star support antecedent changed")
                clauses.append({
                    "domain": [u, v] + list(V.RESIDUE),
                    "boundary_colours": [left_colour, right_colour],
                    "residue_witnesses": [list(cell)
                                           for cell in RESIDUE_WITNESSES],
                    "boundary_star_witnesses": [list(cell)
                                                 for cell in boundary],
                    "support_clause": [list(cell) for cell in antecedent],
                })
    require(len(clauses) == 12,
            "the four-star transported clause census changed")
    return clauses


def build_ledger():
    clauses = clause_audit()
    return {
        "pinned_six_site_sha256": PINNED_SIX_SITE_SHA256,
        "algebra": reduced_tensor_audit(),
        "residue_minor_witnesses": [list(cell)
                                    for cell in RESIDUE_WITNESSES],
        "transported_support_clauses": clauses,
        "antecedent_size": 8,
        "boundary_star_units": ["p70", "q70", "p60", "p40"],
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
    print("transported support clauses: 12 of size 8")
    print("elapsed: %.3fs" % (monotonic() - started))


if __name__ == "__main__":
    main()
