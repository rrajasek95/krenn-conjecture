#!/usr/bin/env python3
"""Solve the strongest linear ``A_Gamma`` landing problem on residual seven.

The physical two-word carrier has 180 literal perfect-matching monomials.
Its pair-shadow fibre has dimension 21; the committed parity, Weyl, corner,
aggregate and single-cell readouts leave a seven-dimensional kernel.  This
checker rebuilds that kernel over Q from the current constructors.

The 159 site-repeating order-six rows are pair coordinates, so they vanish on
this shadow-zero kernel and add no equation.  In contrast, insertion of one
fixed private multiplier into the literal full-nine boundary is split monic:
deleting that multiplier recovers the original monomial.  Its 180-coordinate
readout therefore has rank seven on the residual.

For both AB and AC root labels, the most general normalized linear chain-map
ansatz has four scalar coefficients and two copies of the residual seven.
Chain-map, root-naturality and monic equations have rank 11 of 18.  Adding the
termwise/private landing on one root representative raises the rank to 18;
the second root equations are then consequences of naturality.  The unique
formal solution is

    epsilon_AB, epsilon_AC -> r0,
    c_AB, c_AC             -> -E,
    residual_AB=residual_AC=0.

Thus the linear problem has a unique B=Eq-tied solution.  It is not yet a
physical construction: the current source operation algebra has no nonzero
e_C A e_R arrow.  The nearest literal H_w*r0 relation is cap-internal and
target/anchor locked, so it cannot realize the formal termwise landing.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py":
        "9bde6f6e09ba6e3ca5145f68fad17565c3398270b7f9ac8a6ba236c1c8c2bdea",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "computations/verify_h3_rootless_c5_first_higher_anchor_spair.py":
        "3f9c39e8505da148d85a2d5125cefc502321f3652af2d9c0d12cd65aa41d469c",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
}
EXPECTED_LEDGER_SHA256 = (
    "0cc7b94a5d54da346ef3650213016fad5c080caf1a58cbc882f497f1a54c1cf5"
)

ROOT_LABELS = ("AB", "AC")
TAIL_SITES = (2, 5)
PRIVATE_MATCHING = ((1, 2), (3, 4))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def sparse_rank(vectors) -> int:
    """Exact rank of sparse vectors keyed by comparable coordinates."""
    basis = {}
    for source in vectors:
        vector = {key: Q(value) for key, value in source.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                inverse = Q(1) / vector[pivot]
                basis[pivot] = {
                    key: value * inverse for key, value in vector.items()
                }
                break
            coefficient = vector[pivot]
            for key, value in basis[pivot].items():
                residue = vector.get(key, Q(0)) - coefficient * value
                if residue:
                    vector[key] = residue
                else:
                    vector.pop(key, None)
    return len(basis)


def sparse_nullspace(rows, width: int):
    """Exact nullspace of sparse row equations in ``width`` variables."""
    basis = {}
    for source in rows:
        row = {int(key): Q(value) for key, value in source.items() if value}
        while row:
            common = sorted(set(row) & set(basis))
            if not common:
                break
            pivot = common[0]
            coefficient = row[pivot]
            for key, value in basis[pivot].items():
                residue = row.get(key, Q(0)) - coefficient * value
                if residue:
                    row[key] = residue
                else:
                    row.pop(key, None)
        if row:
            pivot = min(row)
            inverse = Q(1) / row[pivot]
            basis[pivot] = {
                key: value * inverse for key, value in row.items()
            }

    pivots = set(basis)
    free = tuple(index for index in range(width) if index not in pivots)
    kernel = []
    for free_index in free:
        vector = {free_index: Q(1)}
        for pivot in sorted(pivots, reverse=True):
            row = basis[pivot]
            value = -sum((coefficient * vector.get(index, Q(0))
                          for index, coefficient in row.items()
                          if index != pivot), Q(0))
            if value:
                vector[pivot] = value
        kernel.append(vector)
    return len(basis), tuple(kernel)


def permute_cell(cell, swap):
    left, right, left_colour, right_colour = cell
    left = swap.get(left, left)
    right = swap.get(right, right)
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def endpoint_swap(monomial):
    return tuple(sorted(permute_cell(cell, {0: 1, 1: 0})
                        for cell in monomial))


def tail_weyl(monomial):
    cells = list(monomial)
    sign = 1
    for site in TAIL_SITES:
        positions = [position for position, cell in enumerate(cells)
                     if site in cell[:2]]
        require(len(positions) == 1,
                ("matching incidence changed", site, monomial))
        position = positions[0]
        left, right, left_colour, right_colour = cells[position]
        if left == site:
            if left_colour == 1:
                left_colour = 2
                sign = -sign
            elif left_colour == 2:
                left_colour = 1
        else:
            require(right == site, (site, cells[position]))
            if right_colour == 1:
                right_colour = 2
                sign = -sign
            elif right_colour == 2:
                right_colour = 1
        cells[position] = (left, right, left_colour, right_colour)
    return tuple(sorted(cells)), sign


def literal_residual_audit(base, commutator):
    pure = tuple(base.full_row(commutator.PURE_WORD))
    mixed = tuple(base.full_row(commutator.MIXED_WORD))
    monomials = pure + mixed
    require(len(pure) == len(mixed) == 90
            and len(set(monomials)) == 180,
            "two-word physical inventory changed")
    index = {monomial: position for position, monomial in enumerate(monomials)}

    pair_rows = defaultdict(dict)
    for position, monomial in enumerate(monomials):
        cells = tuple(monomial)
        for left in range(len(cells)):
            for right in range(left + 1, len(cells)):
                pair_rows[tuple(sorted((cells[left], cells[right])))][position] = Q(1)

    all_rows = list(pair_rows.values())

    # Endpoint oddness.
    seen = set()
    for monomial in monomials:
        image = endpoint_swap(monomial)
        require(image in index, ("endpoint image left inventory", monomial))
        orbit = tuple(sorted((monomial, image)))
        if orbit in seen:
            continue
        seen.add(orbit)
        row = Counter({index[monomial]: Q(1), index[image]: Q(1)})
        all_rows.append({key: value for key, value in row.items() if value})

    # Tail Weyl oddness.
    seen = set()
    for monomial in monomials:
        image, sign = tail_weyl(monomial)
        require(image in index, ("Weyl image left inventory", monomial))
        orbit = tuple(sorted((monomial, image)))
        if orbit in seen:
            continue
        seen.add(orbit)
        row = Counter({index[monomial]: Q(1)})
        row[index[image]] += Q(sign)
        all_rows.append({key: value for key, value in row.items() if value})

    # Four protected corner residues.
    for corner in commutator.CORNERS:
        all_rows.append({index[corner]: Q(1)})

    # Complete word-row and fine-degree augmentations.
    all_rows.append({index[monomial]: Q(1) for monomial in pure})
    all_rows.append({index[monomial]: Q(1) for monomial in mixed})
    fine_rows = defaultdict(dict)
    for position, monomial in enumerate(monomials):
        fine_rows[base.fine_degree_of_edge_monomial(monomial)][position] = Q(1)
    all_rows.extend(fine_rows.values())

    # Codimension-three/single-cell incidence readouts.
    cell_rows = defaultdict(dict)
    for position, monomial in enumerate(monomials):
        for cell in monomial:
            cell_rows[cell][position] = Q(1)
    all_rows.extend(cell_rows.values())

    shadow_rank, shadow_kernel = sparse_nullspace(pair_rows.values(), 180)
    full_rank, residual = sparse_nullspace(all_rows, 180)
    require(shadow_rank == 159 and len(shadow_kernel) == 21,
            ("raw shadow fibre changed", shadow_rank, len(shadow_kernel)))
    require(full_rank == 173 and len(residual) == 7,
            ("literal residual changed", full_rank, len(residual)))

    # Every residual vector has zero pair shadow, including every possible
    # site-repeating subset.  The current 159-row enrichment therefore has
    # rank zero on this residual even though it is essential on the universal
    # order-six operator module.
    require(all(not any(
        sum((coefficient * vector.get(position, Q(0))
             for position, coefficient in row.items()), Q(0))
        for row in pair_rows.values()) for vector in residual),
        "residual acquired pair shadow")

    colouring = {site: 0 for site in (1, 2, 3, 4)}
    private_multiplier = base.matching_monomial(PRIVATE_MATCHING, colouring)

    def insertion(monomial):
        return tuple(sorted(private_multiplier + monomial))

    def restriction(feature):
        terms = Counter(feature)
        for cell in private_multiplier:
            require(terms[cell] > 0, ("private multiplier missing", feature))
            terms[cell] -= 1
            if not terms[cell]:
                del terms[cell]
        return tuple(sorted(cell for cell, multiplicity in terms.items()
                            for _ in range(multiplicity)))

    features = tuple(insertion(monomial) for monomial in monomials)
    require(len(set(features)) == 180
            and all(restriction(feature) == monomial
                    for feature, monomial in zip(features, monomials, strict=True)),
            "private insertion/restriction stopped being split monic")
    termwise_rank = sparse_rank(residual)
    require(termwise_rank == 7,
            ("termwise identity rank on residual changed", termwise_rank))

    # Aggregating the 180 terms back to H_pure and H_mixed is already among
    # the committed rows, hence has rank zero on the residual.
    aggregate_values = []
    for vector in residual:
        aggregate_values.append((
            sum((vector.get(index[monomial], Q(0)) for monomial in pure), Q(0)),
            sum((vector.get(index[monomial], Q(0)) for monomial in mixed), Q(0)),
        ))
    require(set(aggregate_values) == {(Q(0), Q(0))},
            "aggregate H_w unexpectedly detects the residual")

    return {
        "monomials": monomials,
        "residual": residual,
        "inventory_summary": {
            "literal_full_nine_monomials": 180,
            "pair_shadow_rank": shadow_rank,
            "raw_pair_shadow_fibre": len(shadow_kernel),
            "all_committed_readout_rank": full_rank - shadow_rank,
            "residual_dimension": len(residual),
        },
        "site_repeating_summary": {
            "universal_new_coordinates": 159,
            "universal_projection_rank_two_primes": 153,
            "rank_on_literal_shadow_zero_residual": 0,
            "reason": "every residual vector has zero complete pair shadow",
        },
        "private_summary": {
            "termwise_coordinates": len(features),
            "distinct_private_features": len(set(features)),
            "private_multiplier": repr(private_multiplier),
            "restriction_after_insertion_is_identity": True,
            "rank_on_residual": termwise_rank,
            "aggregate_Hw_rank_on_residual": 0,
        },
    }


def dense_rank(rows, width: int) -> int:
    sparse = ({index: Q(value) for index, value in enumerate(row) if value}
              for row in rows)
    return sparse_rank(sparse)


def linear_landing_audit(literal):
    residual = literal["residual"]
    monomials = literal["monomials"]
    residual_dimension = len(residual)
    width = 4 + 2 * residual_dimension
    require(width == 18, width)

    A_AB, B_AB, A_AC, B_AC = range(4)
    X_AB = tuple(range(4, 4 + residual_dimension))
    X_AC = tuple(range(4 + residual_dimension, width))

    def row(**entries):
        vector = [Q(0)] * width
        for key, value in entries.items():
            vector[int(key)] += Q(value)
        return tuple(vector)

    chain = (
        row(**{str(A_AB): 1, str(B_AB): 1}),
        row(**{str(A_AC): 1, str(B_AC): 1}),
    )
    scalar_naturality = (
        row(**{str(A_AB): 1, str(A_AC): -1}),
        row(**{str(B_AB): 1, str(B_AC): -1}),
    )
    residual_covariance = tuple(
        row(**{str(left): 1, str(right): -1})
        for left, right in zip(X_AB, X_AC, strict=True)
    )
    monic_ab = (row(**{str(A_AB): 1}),)
    monic_both = (row(**{str(A_AB): 1}), row(**{str(A_AC): 1}))

    termwise_ab = []
    termwise_ac = []
    for monomial_index in range(len(monomials)):
        ab = [Q(0)] * width
        ac = [Q(0)] * width
        for residual_index, vector in enumerate(residual):
            value = vector.get(monomial_index, Q(0))
            ab[X_AB[residual_index]] = value
            ac[X_AC[residual_index]] = value
        if any(ab):
            termwise_ab.append(tuple(ab))
        if any(ac):
            termwise_ac.append(tuple(ac))
    require(dense_rank(termwise_ab, width) == 7
            and dense_rank(termwise_ac, width) == 7,
            "literal termwise constraint rank changed")

    natural_base = chain + scalar_naturality + residual_covariance + monic_ab
    rank_natural_base = dense_rank(natural_base, width)
    rank_natural_ab = dense_rank(natural_base + tuple(termwise_ab), width)
    rank_natural_both = dense_rank(
        natural_base + tuple(termwise_ab) + tuple(termwise_ac), width)
    require((rank_natural_base, rank_natural_ab, rank_natural_both)
            == (11, 18, 18),
            ("natural landing ranks changed", rank_natural_base,
             rank_natural_ab, rank_natural_both))

    separate_base = chain + monic_both
    rank_separate_base = dense_rank(separate_base, width)
    rank_separate_ab = dense_rank(separate_base + tuple(termwise_ab), width)
    rank_separate_both = dense_rank(
        separate_base + tuple(termwise_ab) + tuple(termwise_ac), width)
    require((rank_separate_base, rank_separate_ab, rank_separate_both)
            == (4, 11, 18),
            ("separate-root landing ranks changed", rank_separate_base,
             rank_separate_ab, rank_separate_both))

    solution = (Q(1), Q(-1), Q(1), Q(-1)) + (Q(0),) * 14
    # The only inhomogeneous equation is A_AB=1 (or both monic equations in
    # the separate-root presentation).  Verify the displayed solution and
    # the homogeneous equations directly.
    for equation in chain + scalar_naturality + residual_covariance:
        require(sum((left * right for left, right in
                     zip(equation, solution, strict=True)), Q(0)) == 0,
                ("formal solution broke a homogeneous equation", equation))
    require(solution[A_AB] == solution[A_AC] == 1
            and solution[B_AB] == solution[B_AC] == -1,
            "normalized scalar solution changed")

    return {
        "variables": {
            "total": width,
            "scalar_chain_map": ["a_AB", "b_AB", "a_AC", "b_AC"],
            "literal_residual": ["x_AB[1..7]", "x_AC[1..7]"],
        },
        "equations": {
            "chain_map": "a_root+b_root=0",
            "root_scalar_naturality": "a_AB=a_AC and b_AB=b_AC",
            "root_residual_naturality": "x_AB=x_AC",
            "normalization": "a_AB=1",
            "site_repeating_159": "zero on residual; no rank increase",
            "private_landing": (
                "I_private(K_root)-a_root*I_private(K_phys)=0 termwise; "
                "equivalently the seven residual coefficients vanish"
            ),
        },
        "natural_system_rank_before_termwise": rank_natural_base,
        "natural_system_freedom_before_termwise": width - rank_natural_base,
        "rank_after_one_root_termwise_landing": rank_natural_ab,
        "freedom_after_one_root_with_full_naturality": width - rank_natural_ab,
        "rank_after_both_root_termwise_landings": rank_natural_both,
        "freedom_after_both": width - rank_natural_both,
        "without_root_covariance": {
            "normalized_chain_rank": rank_separate_base,
            "rank_after_AB_only": rank_separate_ab,
            "remaining_AC_freedom": width - rank_separate_ab,
            "rank_after_AB_and_AC": rank_separate_both,
        },
        "unique_formal_solution": {
            "Phi_1(epsilon_AB)": "r0_AB",
            "Phi_0(c_AB)": "-E_AB",
            "Phi_1(epsilon_AC)": "r0_AC",
            "Phi_0(c_AC)": "-E_AC",
            "residual_AB": [0] * 7,
            "residual_AC": [0] * 7,
            "B_Eq_signature_each_root": [1, 1],
            "Psi_each_root": 0,
        },
        "unique_tied_solution_exists_in_linear_enriched_category": True,
    }


def dependency_and_physical_obstruction_audit(
        two_root, response, spair, base):
    two_root_ledger, two_root_digest = two_root.audit()
    require(two_root_digest == two_root.EXPECTED_LEDGER_SHA256,
            ("two-root ledger changed", two_root_digest))
    paired = two_root_ledger["paired_root_residual_and_covariance"]
    require(paired["joint_residual_without_root_covariance"] == 14
            and paired["joint_residual_after_maximal_covariance"] == 7,
            paired)

    response_ledger, response_digest = response.audit()
    require(response_digest == response.EXPECTED_LEDGER_SHA256,
            ("response/cap ledger changed", response_digest))
    hom = response_ledger["literal_idempotent_Hom"]
    require(hom["Hom_degree0_response_to_cap_in_current_grammar"] == 0,
            hom)

    spair.pin_dependencies()
    spair_ledger = spair.audit(base)
    spair_digest = sha256(json.dumps(
        spair_ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    require(spair_digest == spair.EXPECTED_LEDGER_SHA256, spair_digest)
    kernel = spair_ledger["kernel_generator"]
    require(kernel["formula"] == "H_w*r0-(H_0-u)*r_w"
            and kernel["typed_readout_ainc_w_tgt_ores"]
                == ["-H_w", 0, "H_w", 0],
            kernel)

    return {
        "linear_system_status": "unique normalized tied solution",
        "current_physical_realization_status": "not constructed",
        "first_typed_obstruction": {
            "equation": "e_C * A_Gamma * e_R = A_Gamma",
            "current_operation_algebra_value": "e_C A e_R=0",
            "formal_solution_requires": "nonzero coefficient a_AB=a_AC=1",
            "meaning": (
                "termwise rows are readout coordinates; restriction and "
                "insertion do not create the missing response-to-cap matrix unit"
            ),
        },
        "first_multiplicative_candidate": {
            "formula": kernel["formula"],
            "typed_ainc_word_target_ores":
                kernel["typed_readout_ainc_w_tgt_ores"],
            "operation_corner": "cap -> cap",
            "target_anchor_lock": "target H_w and anchor -H_w vanish together",
            "why_it_fails": (
                "it is off-grade and diagonal; using its termwise factors as "
                "A_Gamma would change the operation idempotent by declaration"
            ),
        },
        "precise_remaining_physical_axiom": (
            "a source-derived mixed divided-Hasse module action whose private "
            "insertion/restriction square is the split-monic 180-term identity "
            "and whose operation component is a natural nonzero e_C A e_R map"
        ),
        "not_an_additional_linear_ambiguity": True,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "landing_base",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "landing_commutator",
    )
    two_root = load(
        "computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py",
        "landing_two_root",
    )
    response = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "landing_response_cap",
    )
    spair = load(
        "computations/verify_h3_rootless_c5_first_higher_anchor_spair.py",
        "landing_hw_spair",
    )

    literal = literal_residual_audit(base, commutator)
    linear = linear_landing_audit(literal)
    physical = dependency_and_physical_obstruction_audit(
        two_root, response, spair, base)
    ledger = {
        "theorem": "h3 termwise private-full-nine AugP2 linear landing gate",
        "pins": PINS,
        "literal_two_word_residual": literal["inventory_summary"],
        "site_repeating_compatibility": literal["site_repeating_summary"],
        "private_insertion_restriction": literal["private_summary"],
        "most_general_two_root_linear_augmentation": linear,
        "physical_obstruction_after_linear_solution": physical,
        "verdict": (
            "The literal residual-seven reconstruction is exact over Q.  All "
            "159 site-repeating pair rows vanish on it, while the split-monic "
            "180-coordinate private full-nine insertion has rank seven.  The "
            "18-variable two-root chain-map/naturality system has rank 11 before "
            "that termwise landing and rank 18 after it, so there is a unique "
            "normalized formal solution and it is B=Eq tied.  No scalar, sign, "
            "or residual ambiguity remains.  What remains is physical rather "
            "than linear: current source operations have e_C A e_R=0, and the "
            "literal H_w*r0 S-pair is cap-internal and target/anchor locked"
        ),
        "scope": (
            "exact rational canonical h=3 two-word/two-root landing problem; "
            "the 159/153 universal support dimension retains its stated "
            "two-prime scope.  The checker proves uniqueness conditional on a "
            "termwise source-derived operation, not existence of that operation"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("termwise landing ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "residual", "linear", "physical"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 termwise/private AugP2 landing ({arguments.mode}): PASS")
        print("literal residual: 21 - 14 = 7 over Q")
        print("159 site-repeating rows on residual: RANK 0")
        print("180 private termwise rows on residual: RANK 7")
        print("two-root affine ranks: 11 -> 18; UNIQUE TIED SOLUTION")
        print("physical obstruction: e_C A e_R=0; H_w*r0 is cap-internal")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
