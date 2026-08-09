#!/usr/bin/env python3
"""Exact six-site closure of the four-omission O4 coefficient frontier."""

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


PINNED_O4_SHA256 = (
    "ccf37cd1d35584c9d064200e2614dcacacf6c99ec3a0af327a92ca25ac1eb652"
)
SOURCE = os.path.join(HERE,
                      "verify_n8_d1_residue_orbit4_family_and_lift.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest() == PINNED_O4_SHA256,
            "the pinned O4 family/lift checker changed")
O = importlib.import_module("verify_n8_d1_residue_orbit4_family_and_lift")
C, D, V = O.C, O.D, O.V

EXPECTED_FRONTIER_GENERATOR_SHA256 = (
    "8a56323184fa379ff15fcea0a30267bcc7466be069a07c52946ff39f5cb08b9f"
)
EXPECTED_LEDGER_SHA256 = (
    "3b2d56fa5fdb1852e3967c321558cdce1bc777c408455ab4e624140bd0954f31"
)
BOUNDARY_OMISSIONS = frozenset({
    (0, 2, 2, 0), (0, 2, 2, 1),
    (1, 3, 2, 0), (1, 3, 2, 1),
})


def var(name):
    return D.p_var(name)


def product(*polynomials):
    out = D.p_const(1)
    for polynomial in polynomials:
        out = D.p_mul(out, polynomial)
    return out


def vector_scale(scalar, vector):
    return tuple(D.p_mul(scalar, entry) for entry in vector)


def vector_add(left, right):
    return tuple(D.p_add(a, b) for a, b in zip(left, right))


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


def matrix_add(*matrices):
    zero = D.p_const(0)
    out = tuple(tuple(zero for _ in range(3)) for _ in range(3))
    for matrix in matrices:
        out = tuple(tuple(D.p_add(a, b) for a, b in zip(row0, row1))
                    for row0, row1 in zip(out, matrix))
    return out


def matrix_scale(scalar, matrix):
    return tuple(tuple(D.p_mul(scalar, entry) for entry in row)
                 for row in matrix)


def tensor3_zero():
    return tuple(tuple(tuple(D.p_const(0) for _ in range(3))
                       for _ in range(3)) for _ in range(3))


def tensor3_add(*tensors):
    out = tensor3_zero()
    for tensor in tensors:
        out = tuple(tuple(tuple(D.p_add(a, b)
                                  for a, b in zip(line0, line1))
                          for line0, line1 in zip(plane0, plane1))
                    for plane0, plane1 in zip(out, tensor))
    return out


def tensor3_scale(scalar, tensor):
    return tuple(tuple(tuple(D.p_mul(scalar, entry) for entry in line)
                       for line in plane) for plane in tensor)


def outer3(first, second, third):
    return tuple(tuple(tuple(product(first[i], second[j], third[k])
                             for k in range(3))
                       for j in range(3)) for i in range(3))


def tensor3_equal(left, right):
    return all(a == b
               for plane0, plane1 in zip(left, right)
               for row0, row1 in zip(plane0, plane1)
               for a, b in zip(row0, row1))


def determinant(matrix):
    """Sparse exact determinant by nonzero-column backtracking."""
    size = len(matrix)
    total = D.p_const(0)

    def visit(row, columns, term, parity):
        nonlocal total
        if row == size:
            total = D.p_add(total, D.p_neg(term) if parity else term)
            return
        for column, entry in enumerate(matrix[row]):
            if not entry or column in columns:
                continue
            inversions = sum(previous > column for previous in columns)
            visit(row + 1, columns + (column,), D.p_mul(term, entry),
                  parity ^ (inversions % 2))

    visit(0, tuple(), D.p_const(1), False)
    return total


def family_data():
    c = tuple(var("c%d" % index) for index in range(3))
    e = tuple(var("e%d" % index) for index in range(3))
    b = tuple(var("b%d" % index) for index in range(3))
    d = tuple(var("d%d" % index) for index in range(3))
    alpha = (var("alpha0"), var("alpha1"))
    zero, one = D.p_const(0), D.p_const(1)
    target = (zero, zero, one)
    target_matrix = outer(target, target)
    A = matrix_add(target_matrix,
                   matrix_scale(D.p_const(-1), outer(b, e)),
                   matrix_scale(D.p_const(-1), outer(c, d)))
    B = tuple(tuple(D.p_mul(alpha[column], c[row])
                    if column < 2 else b[row]
                    for column in range(3)) for row in range(3))
    C47 = outer(c, target)
    D56 = tuple(tuple(D.p_neg(D.p_mul(alpha[column], e[row]))
                      if column < 2 else d[row]
                      for column in range(3)) for row in range(3))
    E57 = outer(e, target)
    F67 = outer(target, target)
    blocks = {(4, 5): A, (4, 6): B, (4, 7): C47,
              (5, 6): D56, (5, 7): E57, (6, 7): F67}
    return c, e, b, d, alpha, target, A, B, D56, blocks


def phi_tensor(P4, P5, P6, A, B, D56):
    return tensor3_add(
        tuple(tuple(tuple(D.p_mul(P4[i], D56[j][k])
                          for k in range(3))
                    for j in range(3)) for i in range(3)),
        tuple(tuple(tuple(D.p_mul(B[i][k], P5[j])
                          for k in range(3))
                    for j in range(3)) for i in range(3)),
        tuple(tuple(tuple(D.p_mul(A[i][j], P6[k])
                          for k in range(3))
                    for j in range(3)) for i in range(3)),
    )


def psi_tensor(P4, P5, P6, c, e, target):
    return tensor3_add(outer3(P4, P5, target),
                       outer3(P4, e, P6),
                       outer3(c, P5, P6))


def phi_injectivity_audit(A, B, D56, alpha, c, e, b, d):
    # Columns are P4_0..2,P5_0..2,P6_0..2; rows are (i,j,k).
    matrix = []
    for i, j, k in itertools.product(range(3), repeat=3):
        row = [D.p_const(0) for _ in range(9)]
        row[i] = D56[j][k]
        row[3 + j] = B[i][k]
        row[6 + k] = A[i][j]
        matrix.append(tuple(row))
    pivot_rows = (0, 1, 2, 3, 6, 9, 18, 24, 26)
    minor = determinant(tuple(matrix[index] for index in pivot_rows))
    a00_unit = D.p_add(D.p_mul(b[0], e[0]),
                       D.p_mul(c[0], d[0]))
    expected = product(alpha[0], alpha[0], alpha[0], alpha[0], alpha[0],
                       c[0], c[0], e[0], e[0], a00_unit, a00_unit)
    require(minor == expected,
            "the O4 tripod injectivity minor changed")
    require(A[0][0] == D.p_neg(a00_unit),
            "the injectivity factor stopped being -A45_00")
    return {
        "pivot_rows": list(pivot_rows),
        "determinant": "alpha0^5*c0^2*e0^2*A45_00^2",
        "determinant_sha256": D.content_hash([
            [list(monomial), str(coefficient)]
            for monomial, coefficient in sorted(minor.items())
        ]),
        "localized_source_cells": [
            "x46_00=alpha0*c0", "x47_02=c0",
            "x57_02=e0", "x45_00=A45_00",
        ],
    }


def six_site_reduction_audit(c, e, alpha, target, A, B, D56, blocks):
    rho, tau, w = var("rho"), var("tau"), var("w")
    P = {site: tuple(var("p%d%d" % (site, index))
                     for index in range(3)) for site in V.RESIDUE}
    Q = {site: vector_scale(D.p_neg(rho), P[site])
         for site in (4, 5, 6)}
    Q[7] = vector_add(vector_scale(rho, P[7]),
                      vector_scale(D.p_mul(rho, tau), target))
    z = D.p_mul(rho, w)

    # Reconstruct the six-site matching tensor for fixed boundary colors
    # (site0,site2)=(0,0), directly from the twelve boundary-residue
    # matchings and the boundary-edge/residue term.
    raw = {}
    for colours in itertools.product(range(3), repeat=4):
        word = dict(zip(V.RESIDUE, colours))
        value = product(z, *(target[colours[position]]
                             for position in range(4)))
        for first in V.RESIDUE:
            for second in V.RESIDUE:
                if first == second:
                    continue
                rest = tuple(site for site in V.RESIDUE
                             if site not in (first, second))
                u, v = sorted(rest)
                term = product(P[first][word[first]],
                               Q[second][word[second]],
                               blocks[(u, v)][word[u]][word[v]])
                value = D.p_add(value, term)
        raw[colours] = value

    phi = phi_tensor(P[4], P[5], P[6], A, B, D56)
    psi = psi_tensor(P[4], P[5], P[6], c, e, target)
    reduced = tensor3_add(
        outer3(target, target, vector_scale(w, target)),
        tensor3_scale(tau, phi),
        tensor3_scale(D.p_const(-2), psi),
    )
    for i, j, k, ell in itertools.product(range(3), repeat=4):
        expected = (D.p_mul(rho, reduced[i][j][k])
                    if ell == 2 else D.p_const(0))
        require(raw[(i, j, k, ell)] == expected,
                "the proportional O4 six-site reduction changed")

    # The color-0 slice at site6 is the short equation used when tau != 0.
    P4, P5, P6 = P[4], P[5], P[6]
    slice0 = tuple(tuple(reduced[i][j][0] for j in range(3))
                   for i in range(3))
    expected_slice0 = matrix_add(
        matrix_scale(D.p_mul(tau, P6[0]), A),
        matrix_scale(D.p_neg(D.p_add(D.p_mul(tau, alpha[0]),
                                             D.p_mul(D.p_const(2), P6[0]))),
                     outer(P4, e)),
        matrix_scale(D.p_sub(D.p_mul(tau, alpha[0]),
                             D.p_mul(D.p_const(2), P6[0])),
                     outer(c, P5)),
    )
    require(slice0 == expected_slice0,
            "the decisive site6 color-0 slice changed")

    # In the tau=0, char!=2 branch the slice forces P4*e+c*P5=0.
    # Substitute P4=kappa*c, P5=-kappa*e and check the target slice.
    kappa = var("kappa")
    specialized_psi = psi_tensor(vector_scale(kappa, c),
                                 vector_scale(D.p_neg(kappa), e),
                                 P6, c, e, target)
    specialized = tensor3_add(
        outer3(target, target, vector_scale(w, target)),
        tensor3_scale(D.p_const(-2), specialized_psi),
    )
    expected_specialized = tensor3_add(
        outer3(target, target, vector_scale(w, target)),
        tensor3_scale(D.p_const(2),
                      outer3(vector_scale(D.p_mul(kappa, kappa), c),
                             e, target)),
    )
    require(tensor3_equal(specialized, expected_specialized),
            "the tau=0 target-slice reduction changed")

    return {
        "boundary_colors": [0, 0],
        "independent_branch": (
            "Delta(P7_non-target,Q7_non-target) != 0 gives Phi(P)=Phi(Q)=0; "
            "the localized minor makes Phi injective"
        ),
        "dependent_substitution": {
            "Q4,Q5,Q6": "-rho*(P4,P5,P6)",
            "Q7": "rho*P7+rho*tau*e2",
            "x02_00": "rho*w",
        },
        "reduced_equation": "w*E222+tau*Phi(P)-2*Psi(P)=0",
        "reduced_tensor_sha256": D.content_hash(
            [
                [
                    [
                        [[list(monomial), str(coefficient)]
                         for monomial, coefficient in sorted(entry.items())]
                        for entry in row
                    ]
                    for row in plane
                ]
                for plane in reduced
            ]
        ),
        "tau_nonzero_slice": (
            "tau*p60*A=(tau*alpha0+2*p60)*P4 tensor e"
            "+(2*p60-tau*alpha0)*c tensor P5"
        ),
        "tau_nonzero_quotient": (
            "substitution in E22=A+b tensor e+c tensor d expresses E22 "
            "as u tensor e+c tensor v; modulo <c>, nonzero [e2] tensor e2 "
            "equals [u] tensor e, forcing e parallel e2, contrary to e0!=0"
        ),
        "tau_zero_branch": (
            "in characteristic 2 the equation is w*E222=0; otherwise the "
            "color-0 slice gives P4 tensor e+c tensor P5=0, and the target "
            "slice becomes w*E22+2*kappa^2*c tensor e=0, impossible modulo <c>"
        ),
    }


def frontier_audit():
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    support = set(admissible) - set(O.RESIDUE_HOLES) - set(BOUNDARY_OMISSIONS)
    require(len(admissible) == 217 and len(support) == 193,
            "the O4 four-omission support changed")
    shadow = C.support_shadow_audit(support)
    records = C.coefficient_generators(support)
    require(len(records) == 4969
            and D.content_hash(records) == EXPECTED_FRONTIER_GENERATOR_SHA256,
            "the O4 four-omission coefficient input changed")
    required = {
        V.cell(boundary, residue, 0, colour)
        for boundary in (0, 2) for residue in V.RESIDUE
        for colour in V.COLORS
    } | {V.cell(0, 2, 0, 0)}
    require(required <= support and len(required) == 25,
            "a localized cell used by the O4 six-site proof disappeared")
    return {
        "localized_cells": len(support),
        "boundary_omissions": [list(cell) for cell in sorted(BOUNDARY_OMISSIONS)],
        "complete_fibres_checked": shadow["fibres_checked"],
        "coefficient_generators": len(records),
        "generator_sha256": D.content_hash(records),
        "six_site_localized_cells_used": len(required),
    }


def build_ledger():
    c, e, b, d, alpha, target, A, B, D56, blocks = family_data()
    return {
        "pinned_o4_sha256": PINNED_O4_SHA256,
        "frontier": frontier_audit(),
        "tripod_injectivity": phi_injectivity_audit(
            A, B, D56, alpha, c, e, b, d
        ),
        "six_site_reduction": six_site_reduction_audit(
            c, e, alpha, target, A, B, D56, blocks
        ),
        "base_ring_scope": (
            "polynomial over Z until the explicit field branch split; only "
            "the named localized cells are divided by"
        ),
        "characteristic_scope": "all fields, including characteristic 2",
        "conclusion": (
            "the 193-cell O4 four-boundary-omission localized coefficient "
            "frontier is empty using residue purity and W1 six-site exactness"
        ),
        "downset_warning": (
            "the proof localizes 25 W1 cells; O4 sub-supports omitting one of "
            "those cells require a transported or degenerate branch argument"
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
                "the O4 six-site closure ledger changed")
        print("ledger sha256 (frozen): %s" % digest)
    print("O4 four-omission frontier: EMPTY (exact, all characteristics)")
    print("localized cells / generators: 193 / 4969")
    print("tripod minor: alpha0^5*c0^2*e0^2*A45_00^2")
    print("elapsed: %.3fs" % (monotonic() - started))


if __name__ == "__main__":
    main()
