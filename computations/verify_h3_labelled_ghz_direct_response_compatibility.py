#!/usr/bin/env python3
"""Recover a,K after labelled GHZ normalization and test the selected line.

In the branch q^[3] independent of X_0,X_1,X_2, dual functionals recover
the three labelled quotient slices and the q^[3] coefficient matrix.  Exact
rank-one factors normalize the slices to E_cc; the same basis changes recover
the direct matrix a and response cross matrix K from J.  The remaining
diagonal torus is eliminated by a short invariant polynomial criterion.
"""

from __future__ import annotations

import argparse
import importlib
import os
import sys
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product


HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINS = {
    "verify_h3_labelled_ghz_slice_normalization.py":
        "6ee645ab0a1dd7c4130b668d7f98c45d27aad4f88aff226e3061bf0dcf767a9e",
    "../notes/2026-08-15-h3-labelled-ghz-slice-normalization.md":
        "e32f229c12a8fc7b842944e6a26dca7d728f461bf4c01b071b64a838e97b37d2",
    "verify_h3_fullnine_latent_involution_physical_audit.py":
        "d24685acabaf0fd90904e780af1199bdbd34f048830a910abc31634d3b7796d7",
}
EXPECTED_LEDGER_SHA256 = "ac71e30a953ad6b2890f3e2c50507a03df28a930e8ca9481c13d8d15af83809a"


def pin_sources():
    answer = {}
    for relative, expected in sorted(PINS.items()):
        path = os.path.normpath(os.path.join(HERE, relative))
        with open(path, "rb") as handle:
            actual = sha256(handle.read()).hexdigest()
        require(actual == expected,
                "pinned source changed: %s (%s)" % (relative, actual))
        answer[relative] = actual
    return answer


PINNED = pin_sources()
G = importlib.import_module("verify_h3_labelled_ghz_slice_normalization")
A = G.A
COLORS = (0, 1, 2)


def matrix_scale(scalar, matrix):
    return [[scalar * entry for entry in row] for row in matrix]


def matrix_sub(left, right):
    return [[left[row][column] - right[row][column]
             for column in range(len(left[0]))]
            for row in range(len(left))]


def outer(left, right):
    return [[left_entry * right_entry for right_entry in right]
            for left_entry in left]


def columns(matrix):
    return tuple(tuple(matrix[row][column] for row in range(len(matrix)))
                 for column in range(len(matrix[0])))


def matrix_from_columns(items):
    return [list(row) for row in zip(*items, strict=True)]


def vector_pair(functional, vector):
    return sum((left * right for left, right in
                zip(functional, vector, strict=True)), Q(0))


def dual_functionals(targets, q3):
    """Return lambda_0,lambda_1,lambda_2,eta dual to X_0,X_1,X_2,q3."""
    vectors = tuple(targets) + (tuple(q3),)
    require(len({len(vector) for vector in vectors}) == 1,
            "top vectors have inconsistent lengths")
    require(len(A.independent_vectors(vectors)) == 4,
            "q^[3] is not independent of the labelled target space")
    pivot_rows = []
    for coordinate in range(len(q3)):
        candidate = [tuple(vector[index] for vector in vectors)
                     for index in pivot_rows + [coordinate]]
        if A.D.C.rank(candidate) > len(pivot_rows):
            pivot_rows.append(coordinate)
        if len(pivot_rows) == 4:
            break
    require(len(pivot_rows) == 4, "failed to find a four-coordinate chart")
    pivot = [[vector[row] for vector in vectors] for row in pivot_rows]
    pivot_inverse = A.inverse(pivot)
    functionals = []
    for label in range(4):
        functional = [Q(0)] * len(q3)
        for coefficient, row in zip(pivot_inverse[label], pivot_rows,
                                    strict=True):
            functional[row] = coefficient
        expected = tuple(Q(1) if index == label else Q(0)
                         for index in range(4))
        require(tuple(vector_pair(functional, vector) for vector in vectors)
                == expected, "dual target chart is not exact")
        functionals.append(tuple(functional))
    return tuple(functionals), tuple(pivot_rows)


def factor_rank_one(matrix):
    """Canonical exact factor B=left*right^T, using its first nonzero entry."""
    pivot = next(((row, column)
                  for row, column in product(COLORS, repeat=2)
                  if matrix[row][column]), None)
    require(pivot is not None, "a labelled quotient slice is zero")
    row, column = pivot
    value = matrix[row][column]
    left = tuple(matrix[index][column] for index in COLORS)
    right = tuple(matrix[row][index] / value for index in COLORS)
    require(outer(left, right) == matrix,
            "a labelled quotient slice has rank greater than one")
    return left, right, pivot


def recover_normalized_packet(c_cross, targets, q3, j_form):
    """Recover normalized slices, a, and K in the independent-q3 branch."""
    functionals, pivot_rows = dual_functionals(targets, q3)
    lambdas = functionals[:3]
    eta = functionals[3]
    slices = tuple([[vector_pair(lambdas[colour], c_cross[i][j])
                     for j in COLORS] for i in COLORS]
                   for colour in COLORS)
    verdict = G.criterion(slices)
    require(verdict["passes"], ("labelled GHZ criterion failed", verdict))
    factors = tuple(factor_rank_one(matrix) for matrix in slices)
    left_factor_matrix = matrix_from_columns(tuple(item[0] for item in factors))
    right_factor_matrix = matrix_from_columns(tuple(item[1] for item in factors))
    require(A.determinant(left_factor_matrix)
            and A.determinant(right_factor_matrix),
            "the recovered factor lines do not form bases")
    p_change = A.inverse(A.transpose(left_factor_matrix))
    s_change = A.inverse(A.transpose(right_factor_matrix))
    normalized_slices = tuple(G.transform_slice(
        matrix, p_change, s_change) for matrix in slices)
    require(normalized_slices == G.canonical_slices(),
            "recovered bases do not normalize the labelled slices")

    q3_coefficients = [[vector_pair(eta, c_cross[i][j])
                        for j in COLORS] for i in COLORS]
    normalized_q3 = G.transform_slice(
        q3_coefficients, p_change, s_change)
    direct = matrix_scale(Q(-1), normalized_q3)
    require(len(j_form) == 6 and all(len(row) == 6 for row in j_form),
            "J must be a 6 by 6 latent response form")
    require(j_form == A.transpose(j_form), "J is not symmetric")
    require(all(not j_form[i][j] and not j_form[i + 3][j + 3]
                for i, j in product(COLORS, repeat=2)),
            "the involution eigenspaces are not J-isotropic")
    j_cross = [[j_form[i][j + 3] for j in COLORS] for i in COLORS]
    require([[j_form[j + 3][i] for j in COLORS] for i in COLORS]
            == j_cross, "the two response cross blocks disagree")
    response = G.transform_slice(j_cross, p_change, s_change)
    return {
        "quotient_chart_rows": pivot_rows,
        "criterion": verdict,
        "slice_factor_pivots": tuple(item[2] for item in factors),
        "p_change": p_change,
        "s_change": s_change,
        "normalized_slices": normalized_slices,
        "q3_coefficient": normalized_q3,
        "direct_a": direct,
        "response_K": response,
    }


def residual_conjugate(matrix, diagonal):
    return [[diagonal[i] * matrix[i][j] / diagonal[j]
             for j in COLORS] for i in COLORS]


def required_channel(direct, selected):
    left, right = selected
    trace = sum((direct[index][index] for index in COLORS), Q(0))
    alpha = direct[left][right]
    answer = A.zero_matrix(3, 3)
    for index in COLORS:
        answer[index][index] = -alpha
    answer[left][right] += trace
    return answer


def selected_line_test(direct, response, selected, require_full_rank=True):
    """Eliminate the residual diagonal torus for one fixed labelled line."""
    left, right = selected
    trace = sum((direct[index][index] for index in COLORS), Q(0))
    alpha = direct[left][right]
    det_response = A.determinant(response)
    if left == right:
        required = required_channel(direct, selected)
        passes = response == required and (not require_full_rank or det_response)
        return {
            "selected": selected,
            "diagonal_line": True,
            "trace": trace,
            "alpha": alpha,
            "det_K": det_response,
            "passes": bool(passes),
            "reason": "the residual torus fixes E_aa and a_aa",
        }

    kappa = response[0][0]
    forbidden = tuple((i, j, response[i][j])
                      for i, j in product(COLORS, repeat=2)
                      if i != j and (i, j) != selected)
    diagonal_differences = tuple(response[index][index] - kappa
                                 for index in COLORS[1:])
    invariant = alpha * trace + kappa * response[left][right]
    closed_passes = (all(not value for _, _, value in forbidden)
                     and all(not value for value in diagonal_differences)
                     and not invariant)
    open_passes = (alpha != 0 and kappa != 0
                   and (not require_full_rank or det_response != 0))
    passes = closed_passes and open_passes
    witness = None
    if passes:
        ratio = -kappa / alpha
        diagonal = [Q(1)] * 3
        diagonal[left] = ratio
        diagonal[right] = Q(1)
        transformed_direct = residual_conjugate(direct, diagonal)
        transformed_response = residual_conjugate(response, diagonal)
        require(transformed_response == required_channel(
            transformed_direct, selected),
            "the invariant criterion did not construct its torus witness")
        witness = {
            "d_a_over_d_b": ratio,
            "diagonal": tuple(diagonal),
            "transformed_direct": transformed_direct,
            "transformed_response": transformed_response,
        }
    return {
        "selected": selected,
        "diagonal_line": False,
        "trace": trace,
        "alpha": alpha,
        "kappa": kappa,
        "K_ab": response[left][right],
        "det_K": det_response,
        "forbidden_offdiagonal": forbidden,
        "diagonal_differences": diagonal_differences,
        "invariant_alpha_tau_plus_kappa_Kab": invariant,
        "closed_passes": closed_passes,
        "open_alpha_kappa_det": open_passes,
        "passes": bool(passes),
        "torus_witness": witness,
    }


def build_c_cross(slices, q3_coefficient, targets, q3):
    answer = [[None for _ in COLORS] for _ in COLORS]
    for i, j in product(COLORS, repeat=2):
        answer[i][j] = tuple(
            sum((slices[colour][i][j] * targets[colour][coordinate]
                 for colour in COLORS), Q(0))
            + q3_coefficient[i][j] * q3[coordinate]
            for coordinate in range(len(q3)))
    return answer


def audit_positive_model():
    targets = (
        (Q(1), Q(0), Q(0), Q(0)),
        (Q(0), Q(1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(0)),
    )
    q3 = (Q(1), Q(2), Q(3), Q(5))
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
    slices = tuple(outer(left, right) for left, right in
                   zip(columns(left_factors), columns(right_factors),
                       strict=True))
    direct_normalized = [
        [Q(1), Q(2), Q(0)],
        [Q(3), Q(4), Q(5)],
        [Q(0), Q(6), Q(7)],
    ]
    selected = (0, 1)
    response_normalized = required_channel(direct_normalized, selected)
    require(A.determinant(response_normalized) == Q(-8),
            "the designed positive response is not full rank")
    q3_coefficient_normalized = matrix_scale(Q(-1), direct_normalized)
    # Old-coordinate forms are L*(normalized form)*R^T.
    q3_coefficient = A.matmul(left_factors, A.matmul(
        q3_coefficient_normalized, A.transpose(right_factors)))
    j_cross = A.matmul(left_factors, A.matmul(
        response_normalized, A.transpose(right_factors)))
    j_form = A.block_cross(j_cross)
    c_cross = build_c_cross(slices, q3_coefficient, targets, q3)
    recovered = recover_normalized_packet(c_cross, targets, q3, j_form)
    verdict = selected_line_test(
        recovered["direct_a"], recovered["response_K"], selected)
    require(verdict["passes"], verdict)

    perturbed_response = [row[:] for row in recovered["response_K"]]
    perturbed_response[selected[0]][selected[1]] += Q(1)
    negative = selected_line_test(
        recovered["direct_a"], perturbed_response, selected)
    require(not negative["passes"]
            and negative["invariant_alpha_tau_plus_kappa_Kab"] != 0,
            negative)
    return {
        "q3": q3,
        "rank_q3_X": len(A.independent_vectors(targets + (q3,))),
        "selected": selected,
        "recovered": recovered,
        "compatibility": verdict,
        "one_entry_perturbation": negative,
    }


def audit_diagonal_selected_model():
    direct = [
        [Q(1), Q(7), Q(0)],
        [Q(0), Q(2), Q(5)],
        [Q(3), Q(0), Q(3)],
    ]
    selected = (1, 1)
    response = required_channel(direct, selected)
    verdict = selected_line_test(direct, response, selected)
    require(verdict["passes"] and verdict["diagonal_line"], verdict)
    perturbed = [row[:] for row in response]
    perturbed[0][0] += Q(1)
    negative = selected_line_test(direct, perturbed, selected)
    require(not negative["passes"], negative)
    return {
        "selected": selected,
        "direct": direct,
        "response": response,
        "positive": verdict,
        "one_diagonal_perturbation_passes": negative["passes"],
    }


def audit_q3_degeneracies():
    targets = tuple(A.target_vector(colour) for colour in COLORS)
    zero = tuple(Q(0) for _ in A.WORDS)
    in_target = targets[0]
    require(len(A.independent_vectors(targets + (zero,))) == 3,
            "zero q3 branch rank changed")
    require(len(A.independent_vectors(targets + (in_target,))) == 3,
            "q3-in-X branch rank changed")
    return {
        "q3_zero": {
            "quotient": "the labelled GHZ slices remain defined in X",
            "failure": (
                "eta(q3)=1 does not exist, so C does not determine a; "
                "the literal direct block must be supplied separately"
            ),
        },
        "q3_nonzero_in_X": {
            "example": "q3=X0",
            "failure": (
                "X maps to a two-dimensional quotient; three fixed labelled "
                "slices and the q3 coefficient are not separately recoverable"
            ),
        },
    }


def audit_77_cell_guard():
    guard = G.audit_physical_guard()
    require(not guard["criterion"]["passes"]
            and guard["criterion"]["slice_ranks"] == (0, 0, 1), guard)
    direct = [list(row) for row in
              A.audit_physical_packet()["direct_block"]]
    selected = (0, 1)
    raw_response = required_channel(direct, selected)
    raw_test = selected_line_test(direct, raw_response, selected)
    require(raw_test["passes"], raw_test)
    return {
        "scope": guard["scope"],
        "quotient_criterion": guard["criterion"],
        "recovery_reached": False,
        "reason": "two labelled quotient slices are zero",
        "literal_direct_and_defined_scalar_zero_K_pass_orbit_test":
            raw_test["passes"],
        "interpretation": (
            "direct/K compatibility is a later independent layer and does "
            "not repair failure of labelled GHZ normalization"
        ),
    }


def build_ledger():
    positive = audit_positive_model()
    diagonal = audit_diagonal_selected_model()
    guard = audit_77_cell_guard()
    degeneracies = audit_q3_degeneracies()
    return {
        "theorem": (
            "in the q3-independent labelled-GHZ branch, normalized P/S "
            "bases recover a=-coeff_q3(C) and K=J(P,S); the fixed selected "
            "scalar-zero line is decided exactly modulo the residual torus"
        ),
        "pins": PINNED,
        "recovery": {
            "target_dual": (
                "lambda_c(X_d)=delta_cd, lambda_c(q3)=0; "
                "eta(X_d)=0, eta(q3)=1"
            ),
            "rank_one_factorization": "B_c=ell_c*r_c^T with labelled c",
            "basis_changes": "G=L^-T, H=R^-T",
            "outputs": "a=-G^T D_q3 H; K=G^T J_PS H",
            "residual_torus": "a,K -> D(a,K)D^-1; target labels fixed",
        },
        "offdiagonal_selected_polynomial_test": {
            "closed": (
                "K_ij=0 off diagonal except (a,b)",
                "K_00=K_11=K_22=kappa",
                "a_ab*tr(a)+kappa*K_ab=0",
            ),
            "open_full_rank": "a_ab*kappa*det(K) != 0",
            "witness": "d_a/d_b=-kappa/a_ab",
            "augmented_polynomial_form": (
                "d_i e_i=1 and d_i e_j K_ij = tr(a) delta_ia delta_jb "
                "- d_a e_b a_ab delta_ij"
            ),
        },
        "diagonal_selected_test": (
            "the residual torus fixes E_aa and a_aa, so require literally "
            "K=tr(a)E_aa-a_aa I"
        ),
        "positive_model": positive,
        "diagonal_selected_model": diagonal,
        "physical_77_cell_guard": guard,
        "q3_degeneracies": degeneracies,
        "scope": (
            "no target GL3 is used.  A simultaneous colour permutation is "
            "only a relabelling; selected (a,b) stays fixed in the test."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    digest = A.D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "ledger digest changed: got %s" % digest)
    if arguments.dump_ledger:
        import pprint
        pprint.pp(ledger, sort_dicts=True)
    print("PASS: labelled GHZ direct/response compatibility")
    print("mode", arguments.mode)
    print("recovery: normalized P/S, direct a, response K")
    print("offdiagonal orbit test: alpha*tau+kappa*K_ab=0 plus shape/open")
    print("77-cell guard: rejected before recovery; designed model: PASS")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
