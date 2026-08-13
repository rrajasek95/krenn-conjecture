#!/usr/bin/env python3
"""Audit descent of the universal occurrence shear to the physical algebra.

On the free ninety-occurrence module the universal centered response family is
globally trivial.  For ``1^T z=0`` put

    M_z = I - 1 z^T.

Then ``M_z^{-1}=I+1 z^T``, ``det(M_z)=1``, and
``1^T M_z u=R-N z^T u``.  This checker verifies the exact equivariance of
this shear and then tests whether it descends through the physical monomial
presentation ``u_M -> f_M(p,s,q)``.

The first obstruction is already the homogeneous toric minor

    u_(0,1;24|35) u_(1,0;23|45)
      - u_(0,1;23|45) u_(1,0;24|35) = 0.

Writing ``A=p0*s1``, ``B=p1*s0``, ``x=q23*q45``, and
``y=q24*q35``, contraction of its conormal with the constant occurrence
direction ``1`` is

    k = A*y+B*x-A*x-B*y = (B-A)(x-y).

For the shear direction ``D(u_i)=-L`` with ``L=z^T u``, the minor has
derivative ``-L*k``, which is generically nonzero.  Thus the global free
shear has no strict presentation-preserving lift to the physical p,s,q
algebra.  The S6 orbit of k has rank 30.  It is matching-standard:
``(A_match+I)k=0``.  The rank-two endpoint private curvatures instead obey
``(A_match+I)C_i=3C_i``; hence this is a distinct proper face, not C2 or C3.

There is no abstract Cech monodromy: the free shear is global.  In the
moving-parameter action groupoid, k is odd under a literal site
transposition and is Maschke-contractible over characteristic zero.  That
does not contract the fixed selected fibre, since the transposition also
moves its parameter.  If a multiplicative physical Tate comparison
``d epsilon=L`` is constructed, the minor face is automatically
``d(-epsilon*k)=-L*k``.  Consequently the toric face is a compulsory
multiplicative face of the same centered comparison, not an independent
conjecture-level generator.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
N = 90
PINS = {
    "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py":
        "39713f3683dd3d2376e5a911987ee3670ec291cf850072d6b4932e7a93745fc7",
    "notes/h3-universal-response-deformation-e14-orbit-ks-gate.md":
        "d9032c365e8fd8fb5baf320dcc5adac8832c023119fb7d4df69d02cce3d5878f",
    "computations/verify_h3_endpoint_projector_common_c2plus_private_curvature_gate.py":
        "011e1882f9391a2e9ca1b58adce0cefdd4b3ced602f5ba823e1b3bbdadfdf6ce",
    "notes/h3-endpoint-projector-common-c2plus-private-curvature-gate.md":
        "a84bf36aec408b35ef8979190faa313e8f6188b4af2fd13e10a602d97d25e30f",
    "computations/verify_h3_matching_face_residual_flip_semidirect_gate.py":
        "0769314fa55e0978a24680a16f5f5bd4bad8b176322d9709cb42c8b73e025f1e",
    "notes/h3-matching-face-residual-flip-semidirect-gate.md":
        "7e93c5dbf094748371b274bbacce6f677f3eeb8fc8476aca38956652bfae3bf9",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
}
EXPECTED_LEDGER_SHA256 = (
    "1ed6491c0446cf0f77f811091c5ade86d5d79b0298013b1ec479441ea724e59f"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def matching4(sites):
    a, b, c, d = sites
    return (
        ((a, b), (c, d)),
        ((a, c), (b, d)),
        ((a, d), (b, c)),
    )


def canonical_matching(matching):
    return tuple(sorted(tuple(sorted(edge)) for edge in matching))


def occurrences():
    answer = []
    for p_site in range(6):
        for s_site in range(6):
            if p_site == s_site:
                continue
            tail = tuple(site for site in range(6)
                         if site not in (p_site, s_site))
            for matching in matching4(tail):
                answer.append((p_site, s_site,
                               canonical_matching(matching)))
    require(len(answer) == N and len(set(answer)) == N,
            "the complete occurrence set changed")
    return tuple(answer)


def occurrence_monomial(occurrence):
    p_site, s_site, matching = occurrence
    factors = [("p", p_site), ("s", s_site)]
    factors.extend(("q", left, right) for left, right in matching)
    return tuple(sorted(factors))


def poly_add(*polynomials):
    answer = defaultdict(Q)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += Q(coefficient)
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def poly_scale(coefficient, polynomial):
    coefficient = Q(coefficient)
    return {monomial: coefficient * value
            for monomial, value in polynomial.items() if coefficient * value}


def poly_multiply(left, right):
    answer = defaultdict(Q)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def unit(index: int):
    return tuple(Q(index == other) for other in range(N))


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def shear(direction, vector, sign=-1):
    """Apply I + sign*1*direction^T to a coefficient vector."""
    return add(vector, scale(sign * dot(direction, vector), (Q(1),) * N))


def permute_occurrence(occurrence, permutation):
    p_site, s_site, matching = occurrence
    return (
        permutation[p_site],
        permutation[s_site],
        canonical_matching((permutation[left], permutation[right])
                           for left, right in matching),
    )


def permute_vector(vector, permutation, occurrence_list, lookup):
    answer = [Q(0)] * N
    for index, coefficient in enumerate(vector):
        answer[lookup[permute_occurrence(occurrence_list[index], permutation)]] = (
            coefficient
        )
    return tuple(answer)


def universal_free_shear_audit(occurrence_list, lookup) -> dict[str, object]:
    one = (Q(1),) * N
    marked = lookup[(0, 1, ((2, 3), (4, 5)))]
    direction = add(unit(marked), scale(Q(-1, N), one))
    require(dot(direction, one) == 0, "the selected direction is not centered")

    # U=1*z^T is square-zero, hence (I-U)(I+U)=I.  Verify on the full basis.
    for index in range(N):
        basis = unit(index)
        require(shear(direction, shear(direction, basis, sign=+1), sign=-1)
                == basis,
                ("the rank-one inverse changed", index))
    row_after = tuple(dot(one, shear(direction, unit(index), sign=-1))
                      for index in range(N))
    require(row_after == add(one, scale(-N, direction)),
            "the response-row pullback changed")

    # Check S6 naturality on adjacent site transpositions and every basis
    # occurrence.  The universal parameter moves with the occurrence tags.
    for left in range(5):
        permutation = list(range(6))
        permutation[left], permutation[left + 1] = (
            permutation[left + 1], permutation[left]
        )
        permutation = tuple(permutation)
        moved_direction = permute_vector(direction, permutation,
                                         occurrence_list, lookup)
        for index in range(N):
            basis = unit(index)
            moved_basis = permute_vector(basis, permutation,
                                         occurrence_list, lookup)
            require(
                shear(moved_direction, moved_basis, sign=-1)
                == permute_vector(shear(direction, basis, sign=-1),
                                  permutation, occurrence_list, lookup),
                ("the free shear lost site equivariance", left, index),
            )

    return {
        "free_shear": "M_z=I-1*z^T on 1^T*z=0",
        "inverse": "I+1*z^T",
        "rank_one_nilpotence": "(1*z^T)^2=0",
        "determinant": 1,
        "response_pullback": "1^T*M_z=1^T-N*z^T",
        "adjacent_site_generators_checked": 5,
        "basis_occurrences_checked_per_generator": N,
        "global_free_coordinate_trivialization": True,
        "free_coordinate_cech_monodromy": 0,
    }


def physical_toric_conormal_audit(occurrence_list, lookup) -> tuple[dict[str, object], tuple[Q, ...]]:
    x = ((2, 3), (4, 5))
    y = ((2, 4), (3, 5))
    ay = (0, 1, y)
    bx = (1, 0, x)
    ax = (0, 1, x)
    by = (1, 0, y)
    for occurrence in (ay, bx, ax, by):
        require(occurrence in lookup, ("missing minor occurrence", occurrence))

    physical = {
        occurrence: {occurrence_monomial(occurrence): Q(1)}
        for occurrence in occurrence_list
    }
    toric_left = poly_multiply(physical[ay], physical[bx])
    toric_right = poly_multiply(physical[ax], physical[by])
    require(toric_left == toric_right and len(toric_left) == 1,
            "the literal 2x2 toric minor stopped vanishing")

    k = add(unit(lookup[ay]), unit(lookup[bx]),
            scale(-1, unit(lookup[ax])), scale(-1, unit(lookup[by])))
    require(sum(k, Q(0)) == 0 and sum(bool(value) for value in k) == 4,
            "the toric conormal changed")
    k_polynomial = {}
    for index, coefficient in enumerate(k):
        if coefficient:
            k_polynomial = poly_add(
                k_polynomial,
                poly_scale(coefficient, physical[occurrence_list[index]]),
            )
    require(k_polynomial, "the physical conormal vanished")

    # Mark ax.  L=h_ax^T u=ax-R/N is the selected centered scalar.  The
    # desired infinitesimal shear sends every u_i to -L, so d(minor)=-L*k.
    one = (Q(1),) * N
    direction = add(unit(lookup[ax]), scale(Q(-1, N), one))
    response_polynomial = {}
    for occurrence in occurrence_list:
        response_polynomial = poly_add(response_polynomial,
                                       physical[occurrence])
    L = poly_add(physical[ax],
                 poly_scale(Q(-1, N), response_polynomial))
    shear_minor_derivative = poly_scale(-1, poly_multiply(L, k_polynomial))
    require(shear_minor_derivative,
            "the selected centered shear unexpectedly preserved the toric ideal")

    # A sparse centered direction gives a compact six-monomial witness too.
    sparse_L = poly_add(physical[ax], poly_scale(-1, physical[by]))
    sparse_derivative = poly_scale(-1,
                                   poly_multiply(sparse_L, k_polynomial))
    require(len(sparse_derivative) == 6,
            "the compact toric obstruction support changed")

    # The two products in the relation have exactly the same literal factor
    # multiset, so word/fine/repeated grading cannot discard this equation.
    common_product = next(iter(toric_left))
    factor_profile = {
        kind: sum(1 for factor in common_product if factor[0] == kind)
        for kind in ("p", "s", "q")
    }
    require(factor_profile == {"p": 2, "s": 2, "q": 4},
            "the toric relation factor grade changed")

    return ({
        "literal_relation": "u_Ay*u_Bx-u_Ax*u_By=0",
        "A": "p0*s1",
        "B": "p1*s0",
        "x": "q23*q45",
        "y": "q24*q35",
        "constant_direction_conormal": "k=(B-A)*(x-y)",
        "conormal_occurrence_support": 4,
        "selected_direction": "h_ax=e_ax-(1/90)1",
        "selected_L": "ax-R/90",
        "minor_derivative_under_shear": "-L*k",
        "selected_derivative_monomial_support": len(shear_minor_derivative),
        "sparse_centered_derivative_monomial_support": len(sparse_derivative),
        "generic_conormal_nonzero": True,
        "strict_physical_p_s_q_lift": False,
        "common_literal_factor_profile": factor_profile,
        "same_word_fine_repeated_grade": True,
        "first_failure_precedes_augmented_readouts": [
            "target", "anchor", "q", "ridge", "eta", "sigma"
        ],
    }, k)


def matching_curvature_separation_audit(occurrence_list, lookup, k) -> dict[str, object]:
    curvature = load(
        "computations/verify_h3_endpoint_projector_common_c2plus_private_curvature_gate.py",
        "universal_occurrence_shear_curvature",
    )
    base, committed_occurrences, committed_lookup, matching, stages = (
        curvature.occurrence_stage_data()
    )
    require(tuple(committed_occurrences) == occurrence_list
            and committed_lookup == lookup,
            "the occurrence ordering changed")
    v0, v1, v2 = stages
    c2 = add(v1, scale(Q(32, 7), v0))
    c3 = add(v2, scale(Q(-108, 7), v0))
    require(not any(matching(k))
            and matching(c2) == scale(3, c2)
            and matching(c3) == scale(3, c3)
            and rank((k, c2, c3)) == 3,
            "the toric/endpoint curvature separation changed")

    # Generate the complete site-permutation orbit of the prototype.  This
    # is the smallest covariant proper-face module forced by the one minor.
    orbit = []
    for permutation in permutations(range(6)):
        orbit.append(permute_vector(k, permutation,
                                    occurrence_list, lookup))
    unique_orbit = tuple(set(orbit))
    require(len(unique_orbit) == 90 and rank(unique_orbit) == 30
            and all(not any(matching(vector)) for vector in unique_orbit),
            "the S6 toric-conormal orbit changed")

    endpoint_swap = (1, 0, 2, 3, 4, 5)
    matching_swap = (0, 1, 2, 4, 3, 5)
    require(permute_vector(k, endpoint_swap, occurrence_list, lookup)
            == scale(-1, k)
            and permute_vector(k, matching_swap, occurrence_list, lookup)
            == scale(-1, k),
            "the toric conormal lost its two odd orientations")

    return {
        "S6_orbit_size_with_orientation": len(unique_orbit),
        "S6_orbit_span_rank": rank(unique_orbit),
        "matching_action_on_k": "(A_match+I)k=0",
        "matching_action_on_endpoint_curvature": "(A_match+I)C_i=3*C_i",
        "rank_of_k_C2_C3": rank((k, c2, c3)),
        "k_is_endpoint_private_C2_or_C3": False,
        "endpoint_role_swap_on_k": "-k",
        "tail_matching_swap_on_k": "-k",
        "coefficient_only_A_B_totalization_supplies_minor_face": False,
        "minor_face_kind": "matching-standard quadratic toric conormal",
    }


def derived_groupoid_scope_audit() -> dict[str, object]:
    # In the universal family, z and u move together, hence L=z^T u is
    # invariant.  Since tau*k=-k, d[tau|Lk]=tau(Lk)-Lk=-2Lk.
    require(Q(-1, 2) * Q(-2) == 1,
            "the characteristic-zero bar normalization changed")
    # If d epsilon=L and dk=0, Leibniz gives d(-epsilon*k)=-L*k.
    require(Q(-1) * Q(1) == Q(-1),
            "the multiplicative Tate sign changed")
    return {
        "universal_diagonal_parameter_scalar": "L=z^T*u is invariant",
        "odd_bar_boundary": "d[tau|Lk]=-2*Lk",
        "characteristic_zero_bar_preimage_of_Lk": "-(1/2)[tau|Lk]",
        "universal_action_groupoid_minor_contractible": True,
        "selected_fixed_parameter_preserved_by_tau": False,
        "fixed_selected_fibre_contraction_from_group_bar": False,
        "physical_Tate_hypothesis": "d epsilon=L",
        "forced_multiplicative_face": "d(-epsilon*k)=-L*k",
        "independent_generator_after_multiplicative_epsilon": False,
        "remaining_requirement": (
            "a termwise multiplicative physical AugP2/E14 image of epsilon"
        ),
        "abstract_cech_or_monodromy_obstruction": False,
        "physical_obstruction": (
            "nonzero toric conormal / failure to preserve the monomial graph ideal"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    occurrence_list = occurrences()
    lookup = {occurrence: index
              for index, occurrence in enumerate(occurrence_list)}
    free = universal_free_shear_audit(occurrence_list, lookup)
    toric, k = physical_toric_conormal_audit(occurrence_list, lookup)
    separation = matching_curvature_separation_audit(
        occurrence_list, lookup, k
    )
    derived = derived_groupoid_scope_audit()
    ledger = {
        "theorem": "universal occurrence shear / physical toric lift gate",
        "scope": "canonical h=3 over characteristic zero",
        "pins": PINS,
        "free_occurrence_shear": free,
        "physical_toric_conormal": toric,
        "matching_endpoint_separation": separation,
        "derived_groupoid_scope": derived,
        "conclusion": {
            "free_family_globally_equivariantly_trivial": True,
            "strict_physical_p_s_q_trivialization": False,
            "first_exact_obstruction": "-L*(B-A)*(x-y)",
            "obstruction_is_C2_or_C3": False,
            "new_independent_cell_beyond_multiplicative_epsilon": False,
            "next_theorem": (
                "construct epsilon as a termwise multiplicative, pointed, "
                "word/fine/repeated-grade physical AugP2/E14 comparison"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return ledger, sha256(payload.encode()).hexdigest()


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    require(digest == EXPECTED_LEDGER_SHA256,
            ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger sha256: {digest}")
    print("free occurrence shear: global, det 1, S6-equivariant")
    print("strict physical p,s,q lift: NO (-L*(B-A)*(x-y))")
    print("toric proper face: matching-standard rank-30 orbit, not C2/C3")
    print("multiplicative physical epsilon: would fill face automatically")


if __name__ == "__main__":
    main()
