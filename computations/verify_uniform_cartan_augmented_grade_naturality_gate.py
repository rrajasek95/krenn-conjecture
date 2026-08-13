#!/usr/bin/env python3
"""Audit augmented-grade naturality of the uniformly placed Cartan prism.

The ambient source prism and its nonzero critical placement are uniform.
The augmented terminal packet is only covariant.  Multiplication by a tail
commutes with the endpoint/Weyl mixed difference exactly when that tail is
invariant on the four-corner orbit.  A common tail never repairs the two
site-degree blocks of the Kähler ridge.  This checker isolates those exact
obstructions and records that the Schur-unit branch does not consume them.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
    "computations/verify_uniform_cartan_critical_component_placement_gate.py":
        "68c56c1a9144dd92fa803962697de60b78b58a125191450f1af1abcd1befe2a1",
    "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py":
        "24ec9e3c1d1f9b689fa5a47faf9900c16724dc215fee0a41a0b653f410427fb3",
    "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py":
        "aea73ce5ff6ce183245d209393ed60192066d38eab7d4d203caa0c82cc5b16d6",
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
    "computations/verify_oo_zero_holonomy_schur_interference_reduction.py":
        "1e96bf98e997e55d2b050de6c56e7f597cd507737aefa6386296c44adab03631",
}
EXPECTED_LEDGER_SHA256 = (
    "12be7e0141f24ae8cb2db689db118d8d42363a1d58705daca45ce17e0500d7de"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def identity(size):
    return tuple(tuple(Q(int(row == column)) for column in range(size))
                 for row in range(size))


def mat_mul(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(sum(Q(a) * Q(b) for a, b in
                           zip(row, column, strict=True))
                       for column in columns) for row in left)


def mat_sub(left, right):
    return tuple(tuple(Q(a) - Q(b) for a, b in
                       zip(left_row, right_row, strict=True))
                 for left_row, right_row in zip(left, right, strict=True))


def diagonal(values):
    return tuple(tuple(Q(values[row]) if row == column else Q(0)
                       for column in range(len(values)))
                 for row in range(len(values)))


def mat_vec(matrix, vector):
    return tuple(sum(Q(entry) * Q(value) for entry, value in
                     zip(row, vector, strict=True)) for row in matrix)


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    if not matrix:
        return 0
    height, width = len(matrix), len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, height)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def audit_tail_residue_naturality():
    # Orbit order: 1,w,s,sw.  Both involutions act by their regular
    # permutations.  D=(1-s)(w-1) is the endpoint/Weyl mixed difference.
    one = identity(4)
    weyl = (
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 1, 0),
    )
    endpoint = (
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (1, 0, 0, 0),
        (0, 1, 0, 0),
    )
    mixed = mat_mul(mat_sub(one, endpoint), mat_sub(weyl, one))
    alpha = mat_vec(mixed, (1, 0, 0, 0))
    require(alpha == (Q(-1), Q(1), Q(1), Q(-1)),
            "the abstract Cartan residue changed")

    # For a tail with four orbit values t_i, the commutator has entry
    # D_ij*(t_j-t_i).  Since every entry of D is nonzero, it vanishes iff all
    # four values agree.  The linear constraint matrix has rank three.
    constraints = []
    for row in range(4):
        for column in range(4):
            if not mixed[row][column]:
                continue
            equation = [Q(0)] * 4
            equation[column] += mixed[row][column]
            equation[row] -= mixed[row][column]
            constraints.append(equation)
    require(rank(constraints) == 3,
            "tail-invariance constraint rank changed")
    require(all(sum(equation) == 0 for equation in constraints),
            "constant tails stopped commuting with the mixed difference")

    noninvariant_tail = (Q(1), Q(2), Q(3), Q(5))
    multiplier = diagonal(noninvariant_tail)
    commutator = mat_sub(mat_mul(mixed, multiplier),
                         mat_mul(multiplier, mixed))
    require(any(any(row) for row in commutator),
            "a generic tail unexpectedly commuted with the Cartan boundary")

    endpoint_reversal = mat_vec(endpoint, alpha)
    require(endpoint_reversal == tuple(-value for value in alpha),
            "endpoint orientation stopped reversing alpha")
    return {
        "corner_order": ["1", "w", "s", "sw"],
        "mixed_operator": "D=(1-s)(w-1)",
        "D_on_seed": [int(value) for value in alpha],
        "tail_commutator": "[D,M_T]_(i,j)=D_(i,j)*(T_j-T_i)",
        "tail_invariance_constraint_rank": 3,
        "exact_factorization_criterion": "T=wT=sT=swT",
        "generic_tail_commutes": False,
        "positive_transport": (
            "if T is invariant under both the chosen Weyl and endpoint "
            "transposition, D(T xi)=T D(xi), so residue transports as T*alpha"
        ),
        "orientation_rule": (
            "alpha is covariant, not invariant: reversing the endpoint "
            "orientation sends alpha to -alpha"
        ),
    }


def add_degree(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def permute_degree(degree, permutation):
    answer = [0] * len(degree)
    for old, value in enumerate(degree):
        answer[permutation[old]] = value
    return tuple(answer)


def audit_ridge_grade_naturality(ridge):
    ridge_ledger = ridge.audit()
    gate = ridge_ledger["physical_grading_gate"]
    require(not gate["common_tail_makes_homogeneous"]
            and not gate["terminal_law_preserved_as_polynomial_identity"],
            "the canonical Kähler grading gate changed")

    # Abstract the site supports of the two halves of -dOmega.
    degree_pq = (0, 0, 0, 0, 0, 0, 1, 1)
    degree_xv = (1, 1, 0, 0, 0, 0, 0, 0)
    tail = (2, 1, 3, 0, 1, 2, 4, 1)
    require(add_degree(degree_pq, tail)
            != add_degree(degree_xv, tail),
            "a common tail repaired distinct site degrees")
    permutation = (2, 3, 0, 1, 4, 5, 6, 7)
    require(permute_degree(degree_pq, permutation)
            != permute_degree(degree_xv, permutation),
            "site relabeling collapsed the ridge degree mismatch")

    # gamma=-da+dt+db-du.  Exchanging the pq and xv blocks sends gamma to
    # -gamma in fixed coordinates, so fixed eta/sigma functionals change
    # sign.  Transporting the functionals too restores the pairing.
    gamma = (Q(-1), Q(1), Q(1), Q(-1))
    block_exchange = (gamma[2], gamma[3], gamma[0], gamma[1])
    require(block_exchange == tuple(-value for value in gamma),
            "the fixed-label ridge covariance guard changed")
    eta_fixed = gamma[1]
    sigma_fixed = gamma[0]
    require((block_exchange[1], block_exchange[0])
            == (-eta_fixed, -sigma_fixed),
            "fixed terminal functionals stopped detecting relabeling")

    return {
        "ridge": "gamma_v=-dOmega_v=-da+dt+db-du",
        "degree_pq_block": list(degree_pq),
        "degree_xv_block": list(degree_xv),
        "arbitrary_common_tail_repairs_degree": False,
        "site_relabeling_repairs_degree": False,
        "tail_scaled_contractions": {
            "eta": "i_eta(T gamma)=T*(1+delta_(vz)u_z/t)",
            "sigma": "i_sigma(T gamma)=-T*q_pq^22",
        },
        "product_differential": "-d(T Omega)=T gamma-Omega*dT",
        "fixed_numeric_terminal_law": (
            "requires a normalized Kähler-constant tail (dT=0 and T=1 "
            "in the terminal quotient), or a labelled shifted lift"
        ),
        "choice_dependence": (
            "site/colour relabeling preserves gamma and its contractions "
            "only covariantly, when Omega, eta, and sigma are transported together"
        ),
        "ordinary_lcm_completion": gate["minimal_lcm_completion"],
        "ordinary_lcm_terminal_law_correct": False,
        "first_grade_obstruction": (
            "the pq and xv halves occupy distinct site degrees; adding the "
            "same matching tail preserves their difference"
        ),
    }


def audit_branch_consumption(schur, placement, odd, commutation):
    cycle = schur.audit_cycle(4)
    require(cycle["every_coordinate_test_nonzero"],
            "the Schur connector interface changed")
    placement_ledger, placement_digest = placement.audit()
    require(placement_digest == placement.EXPECTED_LEDGER_SHA256,
            "the Cartan placement ledger changed")
    odd_ledger, odd_digest = odd.audit()
    require(odd_digest == odd.EXPECTED_LEDGER_SHA256,
            "the endpoint-odd augmentation ledger changed")
    commute_ledger = commutation.audit()
    require(commute_ledger["complete_hasse_tower_can_tensor_with_ridge_jet"],
            "the canonical Hasse/ridge commutation changed")

    return {
        "Schur_unit_branch_inputs": [
            "complete physical source prism G",
            "target-zero ambient boundary",
            "nonzero exact fine-label projection g=pi_M G",
            "rank(M)=n-1 and nonzero anchor amplitude h^T c",
            "nonzero Cartan charge ell^T g",
        ],
        "Schur_unit_uses_ordinary_residue": False,
        "Schur_unit_uses_eta_sigma_ridge": False,
        "consequence": (
            "346d76a plus 6824c9e already make the nonzero-charge Schur "
            "branch uniform; augmented grade typing is not a prerequisite "
            "for that unit"
        ),
        "terminal_branches_need": [
            "ordinary residue identification in the chosen four-corner grade",
            "a labelled shifted lift of -dOmega_v",
            "eta/sigma functionals transported with the chosen labels",
            "the complete Hasse/ridge tensor mapped to the physical augmented cone",
        ],
        "canonical_h3_status": {
            "residue": odd_ledger["mixed_boundary_alpha"],
            "endpoint_even_readouts": odd_ledger[
                "endpoint_even_augmentations_killed"],
            "Hasse_ridge_polynomial_commutator": 0,
            "physical_labelled_shift_outside_canonical_grade": "OPEN",
        },
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ridge = load(
        "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py",
        "uniform_augmented_ridge",
    )
    schur = load(
        "computations/verify_oo_zero_holonomy_schur_interference_reduction.py",
        "uniform_augmented_schur",
    )
    placement = load(
        "computations/verify_uniform_cartan_critical_component_placement_gate.py",
        "uniform_augmented_placement",
    )
    odd = load(
        "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py",
        "uniform_augmented_odd",
    )
    commutation = load(
        "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py",
        "uniform_augmented_commutation",
    )
    ledger = {
        "theorem": "uniform Cartan augmented-grade naturality gate",
        "ordinary_residue": audit_tail_residue_naturality(),
        "ridge_eta_sigma": audit_ridge_grade_naturality(ridge),
        "branch_consumption": audit_branch_consumption(
            schur, placement, odd, commutation),
        "verdict": (
            "augmented values are natural under invariant normalized tails "
            "and simultaneous transport of all labels/readouts, but not under "
            "arbitrary matching-tail multiplication or independent choices"
        ),
        "sharp_frontier": (
            "the uniform Schur-unit branch is closed without terminal typing.  "
            "For the generator/separator and residual branches, construct a "
            "labelled shifted Kähler lift in each new component grade; an "
            "ordinary common-tail product cannot do so"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniform augmented-grade ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("uniform Cartan augmented grade: COVARIANT, NOT ARBITRARY-NATURAL")
    print("Schur-unit branch needs residue/eta/sigma: NO")
    print("tail residue criterion: T=wT=sT=swT")
    print("first terminal obstruction: pq/xv site-degree mismatch")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
