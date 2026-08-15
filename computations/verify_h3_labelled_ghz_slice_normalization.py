#!/usr/bin/env python3
"""Exact labelled GHZ slice criterion beyond coarse latent containment.

Let B:P x S -> X be the image of C(P,S) in
W/<q^[3]>=span(X_0,X_1,X_2), with the target labels fixed.  In bases of P,S
write B_c for the 3x3 coefficient matrix of X_c.  There are bases in which

    B(p_i,s_j) = delta_ij X_i

if and only if

  (i) every 2x2 minor of every B_c vanishes;
 (ii) the 3x9 horizontal concatenation [B_0 B_1 B_2] has rank 3; and
(iii) the 9x3 vertical stack [B_0;B_1;B_2] has rank 3.

The rank-three opens force the three slices to be nonzero rank one and make
their left and right factor lines bases.  Inverse-transpose basis changes
then normalize all three diagonal coefficients to exactly one.

The physical 77-cell rootless guard from the preceding audit has quotient
slices (0,0,E_22), so it fails at the first rank condition.  This proves the
new equations retain precisely normalization data discarded by the coarse
involution system.
"""

from __future__ import annotations

import importlib
import os
import sys
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINS = {
    "verify_h3_fullnine_latent_involution_physical_audit.py":
        "d24685acabaf0fd90904e780af1199bdbd34f048830a910abc31634d3b7796d7",
    "../notes/2026-08-15-h3-fullnine-latent-involution-physical-audit.md":
        "106bd89a905f844fe897aadef749e4ab4f403dba35abb83aa2fb94e565c9c8ca",
}
EXPECTED_LEDGER_SHA256 = (
    "8dca337e2e7aa9b24dd5bad0413b8294f7b2d432e8e923562683a4ed8aaaab1f"
)


def pin_sources():
    result = {}
    for relative, expected in sorted(PINS.items()):
        path = os.path.normpath(os.path.join(HERE, relative))
        with open(path, "rb") as handle:
            result[relative] = sha256(handle.read()).hexdigest()
        require(result[relative] == expected,
                "pinned source changed: %s (%s)" %
                (relative, result[relative]))
    return result


PINNED = pin_sources()
A = importlib.import_module("verify_h3_fullnine_latent_involution_physical_audit")


def outer(left, right):
    return [[x * y for y in right] for x in left]


def matrix_rank(matrix):
    return A.D.C.rank([tuple(row) for row in matrix])


def minor2(matrix, rows, columns):
    i, j = rows
    k, ell = columns
    return matrix[i][k] * matrix[j][ell] - matrix[i][ell] * matrix[j][k]


def slice_minor_ledger(slices):
    entries = []
    for colour, matrix in enumerate(slices):
        for rows in combinations(range(3), 2):
            for columns in combinations(range(3), 2):
                entries.append((colour, rows, columns,
                                minor2(matrix, rows, columns)))
    require(len(entries) == 27, "the 3x9 slice-minor census changed")
    return tuple(entries)


def horizontal(slices):
    return [sum((list(matrix[row]) for matrix in slices), [])
            for row in range(3)]


def vertical(slices):
    return [list(row) for matrix in slices for row in matrix]


def criterion(slices):
    minor_ledger = slice_minor_ledger(slices)
    slice_ranks = tuple(matrix_rank(matrix) for matrix in slices)
    left_rank = matrix_rank(horizontal(slices))
    right_rank = matrix_rank(vertical(slices))
    passes = (all(not entry[3] for entry in minor_ledger)
              and left_rank == 3 and right_rank == 3)
    return {
        "slice_ranks": slice_ranks,
        "all_2x2_minors_zero": all(not entry[3] for entry in minor_ledger),
        "minor_equation_count": len(minor_ledger),
        "horizontal_rank": left_rank,
        "vertical_rank": right_rank,
        "passes": passes,
    }


def transform_slice(matrix, left_change, right_change):
    return A.matmul(A.transpose(left_change),
                    A.matmul(matrix, right_change))


def canonical_slices():
    answer = []
    for colour in range(3):
        matrix = A.zero_matrix(3, 3)
        matrix[colour][colour] = Q(1)
        answer.append(matrix)
    return tuple(answer)


def audit_positive_normalization():
    # Columns are the labelled left/right factors.  Both changes are dense
    # and non-monomial, so normalization is not being tested in its answer
    # basis.
    left_factors = [
        [Q(1), Q(2), Q(0)],
        [Q(0), Q(1), Q(1)],
        [Q(1), Q(0), Q(1)],
    ]
    right_factors = [
        [Q(2), Q(1), Q(0)],
        [Q(1), Q(0), Q(1)],
        [Q(0), Q(1), Q(1)],
    ]
    require(A.determinant(left_factors) != 0
            and A.determinant(right_factors) != 0,
            "the positive factor bases are singular")
    slices = tuple(outer([left_factors[row][colour] for row in range(3)],
                         [right_factors[row][colour] for row in range(3)])
                   for colour in range(3))
    verdict = criterion(slices)
    require(verdict["passes"] and verdict["slice_ranks"] == (1, 1, 1),
            "the nontrivial positive tensor failed the rank criterion")

    # G^T L=I and R^T H=I, hence G=L^{-T}, H=R^{-T}.
    left_change = A.inverse(A.transpose(left_factors))
    right_change = A.inverse(A.transpose(right_factors))
    normalized = tuple(transform_slice(matrix, left_change, right_change)
                       for matrix in slices)
    require(normalized == canonical_slices(),
            "inverse-transpose changes did not give exact coefficient one")

    # A genuine GL(3) target shear is not an allowed relabelling: one of its
    # new coordinate slices has rank two.  A target permutation, in contrast,
    # only permutes the labelled rank-one slices.
    target_shear = (A.matrix_add(normalized[0], normalized[1]),
                    normalized[1], normalized[2])
    require(tuple(matrix_rank(matrix) for matrix in target_shear) == (2, 1, 1),
            "the target-GL shear did not expose rank-two mixing")
    permutation = (normalized[1], normalized[2], normalized[0])
    require(criterion(permutation)["passes"],
            "simultaneous target relabelling broke the criterion")
    return {
        "unnormalized_criterion": verdict,
        "left_factor_determinant": A.determinant(left_factors),
        "right_factor_determinant": A.determinant(right_factors),
        "normalized_slices": tuple(tuple(tuple(row) for row in matrix)
                                   for matrix in normalized),
        "target_shear_slice_ranks": tuple(matrix_rank(matrix)
                                           for matrix in target_shear),
        "target_permutation_passes": criterion(permutation)["passes"],
    }


def functional_for_pure_target(q3, colour):
    """A chart representative lambda_c with lambda_c(q3)=0, lambda_c(Xd)=δcd."""
    mixed_index = next(index for index, word in enumerate(A.WORDS)
                       if len(set(word)) > 1 and q3[index])
    pure_index = A.WORDS.index((colour,) * 6)
    functional = [Q(0)] * len(A.WORDS)
    functional[pure_index] = Q(1)
    functional[mixed_index] = -q3[pure_index] / q3[mixed_index]
    return tuple(functional), mixed_index


def audit_physical_guard():
    blocks = A.D.build_stage_a(A.D.STAGE_A_BASE)
    packet = A.as_chart_packet(blocks)
    p_vectors = tuple(A.star_vector(packet, "P", colour)
                      for colour in A.COLORS)
    s_vectors = tuple(A.star_vector(packet, "S", colour)
                      for colour in A.COLORS)
    q3 = A.q_cube(packet)
    targets = tuple(A.target_vector(colour) for colour in A.COLORS)
    require(len(A.independent_vectors((q3,) + targets)) == 4,
            "the guard lies in the q^[3]/pure-target degeneracy")

    c_cross = [[A.pair_q2(packet, p_vectors[i], s_vectors[j])
                for j in A.COLORS] for i in A.COLORS]
    slices = []
    chart_words = []
    for colour in A.COLORS:
        functional, mixed_index = functional_for_pure_target(q3, colour)
        require(A.pairing(functional, q3) == 0,
                "the quotient target functional does not kill q^[3]")
        require(tuple(A.pairing(functional, target) for target in targets)
                == tuple(Q(1) if d == colour else Q(0) for d in A.COLORS),
                "the quotient target functional lost its fixed label")
        slices.append([[A.pairing(functional, c_cross[i][j])
                        for j in A.COLORS] for i in A.COLORS])
        chart_words.append(A.WORDS[mixed_index])
    slices = tuple(slices)
    expected = list(canonical_slices())
    expected[0] = A.zero_matrix(3, 3)
    expected[1] = A.zero_matrix(3, 3)
    require(slices == tuple(expected),
            "the physical guard quotient slices changed: %s" % (slices,))
    verdict = criterion(slices)
    require(verdict == {
        "slice_ranks": (0, 0, 1),
        "all_2x2_minors_zero": True,
        "minor_equation_count": 27,
        "horizontal_rank": 1,
        "vertical_rank": 1,
        "passes": False,
    }, "the physical guard no longer sharply fails the labelled criterion")
    return {
        "scope": "literal 77-cell N=8 guard at endpoints (2,3)",
        "rank_q3_X0_X1_X2": 4,
        "quotient_chart_words": tuple(chart_words),
        "slices": tuple(tuple(tuple(row) for row in matrix)
                        for matrix in slices),
        "criterion": verdict,
        "failure": (
            "X0 and X1 slices are zero; the horizontal and vertical factor "
            "spans both have rank one"
        ),
    }


def audit_scalar_zero_compatibility():
    """Freeze the exact post-normalization equations and their scaling debt."""
    direct = [
        [Q(1), Q(2), Q(0)],
        [Q(3), Q(4), Q(5)],
        [Q(0), Q(6), Q(7)],
    ]
    selected = (0, 1)
    alpha = direct[selected[0]][selected[1]]
    tau = sum(direct[index][index] for index in range(3))
    channel = [[-alpha if i == j else Q(0) for j in range(3)]
               for i in range(3)]
    channel[selected[0]][selected[1]] += tau
    require(channel == [[Q(-2), Q(12), Q(0)],
                        [Q(0), Q(-2), Q(0)],
                        [Q(0), Q(0), Q(-2)]],
            "the synthetic scalar-zero channel changed")
    require(sum(channel[i][j] * direct[i][j]
                for i, j in product(range(3), repeat=2)) == 0,
            "the synthetic K is not scalar-zero")
    require(A.determinant(channel) == Q(-8),
            "the off-diagonal scalar-zero channel is singular")

    # Residual normalized-slice changes are p_i -> d_i p_i,
    # s_i -> e_i s_i with d_i e_i=1.  In the bilinear-form convention of
    # 0902, both a and the cross block K acquire the factor d_i e_j.  The
    # physical selected-line equation must be imposed after this choice; it
    # is not automatic from normalization.
    d = (Q(2), Q(3), Q(5))
    e = tuple(Q(1) / value for value in d)
    require(all(d[i] * e[i] == 1 for i in range(3)),
            "the residual scaling does not preserve normalized slices")
    scaled_direct = [[d[i] * e[j] * direct[i][j] for j in range(3)]
                     for i in range(3)]
    scaled_channel = [[d[i] * e[j] * channel[i][j] for j in range(3)]
                      for i in range(3)]
    scaled_alpha = scaled_direct[selected[0]][selected[1]]
    scaled_tau = sum(scaled_direct[i][i] for i in range(3))
    scaled_required = [[-scaled_alpha if i == j else Q(0) for j in range(3)]
                       for i in range(3)]
    scaled_required[selected[0]][selected[1]] += scaled_tau
    require(scaled_channel != scaled_required,
            "a generic residual scaling accidentally preserved the selected line")
    return {
        "selected_labels": selected,
        "direct_matrix": tuple(tuple(row) for row in direct),
        "tau": tau,
        "alpha": alpha,
        "channel_K": tuple(tuple(row) for row in channel),
        "det_K": A.determinant(channel),
        "residual_scaling": {"d": d, "e": e},
        "generic_scaling_preserves_selected_line": False,
        "polynomial_equations": (
            "d_i*e_i=1 for i=0,1,2",
            "d_i*e_j*K_ij = tau*delta_(i,a)delta_(j,b) "
            "- d_a*e_b*a_ab*delta_ij for all i,j",
        ),
    }


def build_ledger():
    positive = audit_positive_normalization()
    guard = audit_physical_guard()
    scalar = audit_scalar_zero_compatibility()
    return {
        "theorem": (
            "with fixed labelled target basis, GHZ diagonalizability under "
            "P/S basis changes is equivalent to slice rank<=1 plus rank-three "
            "horizontal and vertical factor spans"
        ),
        "pins": PINNED,
        "polynomial_system": {
            "closed_equations": "27 two-by-two slice minors",
            "left_open": "rank([B0 B1 B2])=3: 84 maximal minors",
            "right_open": "rank([B0;B1;B2])=3: 84 maximal minors",
            "open_encoding": (
                "split into nonzero-minor charts, or adjoin y_m,z_n with "
                "sum_m y_m Delta_m=1 and sum_n z_n Nabla_n=1"
            ),
            "direct_exact_encoding": (
                "equivalently adjoin G,H and inverses with "
                "G^T B_c H=E_cc for c=0,1,2"
            ),
            "target_quotient_chart": (
                "require X intersect span(q^[3])=0: either q^[3]=0, or "
                "rank(q^[3],X0,X1,X2)=4; then choose lambda_c with "
                "lambda_c(q^[3])=0, lambda_c(X_d)=delta_cd"
            ),
        },
        "allowed_symmetry": {
            "fixed_labels": (
                "independent P/S basis changes; after normalization only "
                "p_c->d_c p_c, s_c->d_c^-1 s_c remains"
            ),
            "permutation": (
                "only one simultaneous permutation of P labels, S labels, "
                "and the physical target colours"
            ),
            "forbidden": (
                "an arbitrary GL3 change of target basis; it can mix two "
                "rank-one slices into rank two"
            ),
        },
        "positive_model": positive,
        "physical_guard": guard,
        "next_scalar_zero_compatibility": scalar,
        "remaining_scope": (
            "in the nonzero q^[3] branch, after quotient normalization the "
            "q^[3] coefficients determine a and must match the literal direct "
            "block; then K from J must satisfy the selected scalar-zero "
            "equations on some allowed residual diagonal-scaling chart.  The "
            "q^[3]=0 and nonzero-pure q^[3] degeneracies are separate."
        ),
    }


def main():
    ledger = build_ledger()
    digest = A.D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "ledger digest changed: got %s" % digest)
    print("PASS: exact labelled GHZ quotient-slice criterion")
    print("equations: 27 slice minors; open ranks: 3 and 3")
    print("positive dense factor model normalizes exactly to coefficient one")
    print("77-cell guard slices: ranks (0,0,1), factor-span ranks (1,1): FAIL")
    print("arbitrary target GL3 mixing is forbidden; simultaneous S3 is allowed")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
