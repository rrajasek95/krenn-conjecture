#!/usr/bin/env python3
"""Test the seven carrier residuals as physical occurrence redistributions.

Rebuild the exact seven-dimensional residual inside the two active complete
90-term rows.  Each vector has zero codimension-two shadow and zero value on
all committed parity, corner, row and single-cell readouts.

On the active coefficient torus, a physical support-preserving scalar
variation changes a matching occurrence by the sum of the logarithmic
variations of its four decorated cells.  Thus physical first-order
occurrence redistributions form the column space of the 180-by-40 monomial/
cell incidence matrix I.  The committed single-cell-zero condition says
exactly I^T r=0 for every residual r.  Since the rational Euclidean pairing
is positive definite, im(I) intersects ker(I^T) only in zero.  All seven
nonzero residuals are therefore toric normal/circuit directions, not
physical first-order redistributions.

The proposed minimum-support/Hasse exit stops before the second Hasse face.
If occurrences are freed as independent coordinates the residuals integrate
linearly, but that leaves the physical scalar-factor torus.  Their normalized
self-pairings give literal local covectors, not accepted augmented terminals.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_site_repeating_two_root_augp2_naturality_residual_gate.py":
        "9bde6f6e09ba6e3ca5145f68fad17565c3398270b7f9ac8a6ba236c1c8c2bdea",
    "computations/verify_h3_occurrence_kernel_integrability_terminal_gate.py":
        "40a3a5875951b2d48aeda4ca58ea25029bb12d7195988c057f7c3590ec10039c",
    "computations/verify_h3_pf_dark_kernel_support_lowering_hasse_coloop_gate.py":
        "5feb07c35c4e5ce304a305f0146441de7af5a9dc2d5466a794d315d99b626e48",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_unaudited_repair1_order6_scope_audit.py":
        "0d5be2b2d5c90d5aff04545e7a0712701ef5364266a3ac53f41d7b81da8f530a",
}
EXPECTED_LEDGER_SHA256 = "315ebeeee3552294fb5cec1c744bdbf1eb3c144456149a4a2071487b2cd2e94c"

PURE_WORD = (1,) * 8
MIXED_WORD = (1, 1, 2, 1, 1, 2, 1, 1)
ENDPOINT_SWAP = {0: 1, 1: 0}
TAIL_SITES = (2, 5)


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


def sparse_rank(columns) -> int:
    basis = {}
    for source in columns:
        value = {row: Q(coefficient) for row, coefficient in source.items()
                 if coefficient}
        while value:
            pivot = min(value, key=repr)
            if pivot not in basis:
                inverse = Q(1) / value[pivot]
                basis[pivot] = {
                    row: coefficient * inverse
                    for row, coefficient in value.items()
                }
                break
            coefficient = value[pivot]
            for row, entry in basis[pivot].items():
                result = value.get(row, Q(0)) - coefficient * entry
                if result:
                    value[row] = result
                else:
                    value.pop(row, None)
    return len(basis)


def sparse_nullspace(columns):
    """Return exact relations among sparse columns."""
    columns = tuple(columns)
    basis = {}
    relations = []
    for index, source in enumerate(columns):
        value = {row: Q(coefficient) for row, coefficient in source.items()
                 if coefficient}
        expression = {index: Q(1)}
        while value:
            pivot = min(value, key=repr)
            if pivot not in basis:
                inverse = Q(1) / value[pivot]
                value = {row: coefficient * inverse
                         for row, coefficient in value.items()}
                expression = {column: coefficient * inverse
                              for column, coefficient in expression.items()}
                basis[pivot] = (value, expression)
                break
            pivot_value, pivot_expression = basis[pivot]
            coefficient = value[pivot]
            for row, entry in pivot_value.items():
                result = value.get(row, Q(0)) - coefficient * entry
                if result:
                    value[row] = result
                else:
                    value.pop(row, None)
            for column, entry in pivot_expression.items():
                result = expression.get(column, Q(0)) - coefficient * entry
                if result:
                    expression[column] = result
                else:
                    expression.pop(column, None)
        else:
            relations.append(expression)

    require(len(relations) == len(columns) - len(basis),
            "sparse nullity changed")
    for relation in relations:
        check = Counter()
        for column, coefficient in relation.items():
            for row, entry in columns[column].items():
                check[row] += coefficient * entry
        check = Counter({row: coefficient for row, coefficient in check.items()
                         if coefficient})
        require(not check, ("invalid sparse relation", relation, check))
    return tuple(relations), len(basis)


def permute_cell(cell):
    left, right, left_colour, right_colour = cell
    left = ENDPOINT_SWAP.get(left, left)
    right = ENDPOINT_SWAP.get(right, right)
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def endpoint_swap(monomial):
    return tuple(sorted(permute_cell(cell) for cell in monomial)), 1


def signed_tail_weyl(monomial):
    cells = list(monomial)
    sign = 1
    for site in TAIL_SITES:
        positions = [index for index, cell in enumerate(cells)
                     if site in cell[:2]]
        require(len(positions) == 1,
                ("matching incidence changed", site, monomial))
        position = positions[0]
        left, right, left_colour, right_colour = cells[position]
        if left == site:
            if left_colour == 1:
                left_colour, sign = 2, -sign
            elif left_colour == 2:
                left_colour = 1
        else:
            require(right == site, (site, cells[position]))
            if right_colour == 1:
                right_colour, sign = 2, -sign
            elif right_colour == 2:
                right_colour = 1
        cells[position] = (left, right, left_colour, right_colour)
    return tuple(sorted(cells)), sign


def act_on_chain(chain, action):
    answer = Counter()
    for monomial, coefficient in chain.items():
        image, sign = action(monomial)
        answer[image] += sign * coefficient
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def shadow_two(chain):
    answer = Counter()
    for monomial, coefficient in chain.items():
        for pair in combinations(monomial, 2):
            answer[tuple(sorted(pair))] += coefficient
    return Counter({pair: coefficient
                    for pair, coefficient in answer.items()
                    if coefficient})


def reconstruct_residual7(base, commutator):
    monomials = []
    seen = set()
    for word in (PURE_WORD, MIXED_WORD):
        for monomial in base.full_row(word):
            if monomial in seen:
                continue
            seen.add(monomial)
            monomials.append(monomial)
    require(len(monomials) == 180, "two-word occurrence count changed")
    index = {monomial: position
             for position, monomial in enumerate(monomials)}

    shadow_columns = []
    for monomial in monomials:
        shadow_columns.append({
            tuple(sorted(pair)): Q(1)
            for pair in combinations(monomial, 2)
        })
    kernel21, shadow_rank = sparse_nullspace(shadow_columns)
    require(shadow_rank == 159 and len(kernel21) == 21,
            ("two-word pair-shadow rank changed", shadow_rank, len(kernel21)))

    families = []
    seen_orbits = set()
    for monomial in monomials:
        image, _sign = endpoint_swap(monomial)
        key = tuple(sorted((monomial, image)))
        if key in seen_orbits:
            continue
        seen_orbits.add(key)
        family = Counter({index[monomial]: Q(1)})
        family[index[image]] += Q(1)
        families.append({position: coefficient
                         for position, coefficient in family.items()
                         if coefficient})
    seen_orbits = set()
    for monomial in monomials:
        image, sign = signed_tail_weyl(monomial)
        key = tuple(sorted((monomial, image)))
        if key in seen_orbits:
            continue
        seen_orbits.add(key)
        family = Counter({index[monomial]: Q(1)})
        family[index[image]] += Q(sign)
        families.append({position: coefficient
                         for position, coefficient in family.items()
                         if coefficient})
    for corner in commutator.CORNERS:
        families.append({index[corner]: Q(1)})
    pure = set(base.full_row(PURE_WORD))
    mixed = set(base.full_row(MIXED_WORD))
    families.append({index[monomial]: Q(1) for monomial in pure})
    families.append({index[monomial]: Q(1) for monomial in mixed})
    buckets = {}
    for monomial in monomials:
        for cell in monomial:
            buckets.setdefault(cell, {})[index[monomial]] = Q(1)
    families.extend(buckets.values())
    require(len(buckets) == 40, ("decorated cell count changed", len(buckets)))

    constraint_columns = []
    for relation in kernel21:
        column = {}
        for family_index, family in enumerate(families):
            value = sum((coefficient * relation.get(position, Q(0))
                         for position, coefficient in family.items()), Q(0))
            if value:
                column[family_index] = value
        constraint_columns.append(column)
    residual_combinations, constraint_rank = sparse_nullspace(
        constraint_columns)
    require(constraint_rank == 14 and len(residual_combinations) == 7,
            ("committed readout rank changed", constraint_rank,
             len(residual_combinations)))

    residuals = []
    for combination in residual_combinations:
        chain_coordinates = Counter()
        for kernel_index, coefficient in combination.items():
            for position, value in kernel21[kernel_index].items():
                chain_coordinates[position] += coefficient * value
        chain = Counter({monomials[position]: value
                         for position, value in chain_coordinates.items()
                         if value})
        require(chain, "zero residual basis vector")
        residuals.append(chain)
    require(sparse_rank(tuple({index[monomial]: coefficient
                               for monomial, coefficient in chain.items()}
                              for chain in residuals)) == 7,
            "residual chains stopped being independent")
    return tuple(monomials), tuple(residuals), tuple(buckets)


def exact_residual_basis_audit(base, commutator):
    monomials, residuals, cells = reconstruct_residual7(base, commutator)
    pure = set(base.full_row(PURE_WORD))
    mixed = set(base.full_row(MIXED_WORD))
    support_profile = []
    norm_profile = []
    records = []
    for basis_index, chain in enumerate(residuals):
        cell_values = {
            cell: sum((coefficient for monomial, coefficient in chain.items()
                       if cell in monomial), Q(0))
            for cell in cells
        }
        norm = sum((coefficient * coefficient
                    for coefficient in chain.values()), Q(0))
        require(not shadow_two(chain)
                and not any(cell_values.values())
                and sum((chain.get(monomial, Q(0))
                         for monomial in pure), Q(0)) == 0
                and sum((chain.get(monomial, Q(0))
                         for monomial in mixed), Q(0)) == 0
                and act_on_chain(chain, endpoint_swap)
                    == Counter({monomial: -coefficient
                                for monomial, coefficient in chain.items()})
                and act_on_chain(chain, signed_tail_weyl)
                    == Counter({monomial: -coefficient
                                for monomial, coefficient in chain.items()})
                and all(chain.get(corner, Q(0)) == 0
                        for corner in commutator.CORNERS)
                and norm > 0,
                ("residual property changed", basis_index))
        support_profile.append(len(chain))
        norm_profile.append(norm)
        records.append({
            "basis": basis_index,
            "support": len(chain),
            "pure_terms": sum(monomial in pure for monomial in chain),
            "mixed_terms": sum(monomial in mixed for monomial in chain),
            "coefficient_denominators": sorted({
                coefficient.denominator for coefficient in chain.values()
            }),
            "squared_norm": str(norm),
            "pair_shadow": 0,
            "single_cell_incidence": 0,
            "row_augmentation": [0, 0],
            "corner_values": [0, 0, 0, 0],
            "endpoint_swap_character": -1,
            "signed_Weyl_character": -1,
        })
    require(sorted(support_profile) == [12, 12, 36, 36, 48, 56, 60]
            and set(coefficient.denominator for chain in residuals
                    for coefficient in chain.values()) == {1},
            (support_profile, records))
    return monomials, residuals, cells, {
        "two_complete_words": ["11111111", "11211211"],
        "occurrence_coordinates": len(monomials),
        "decorated_cell_coordinates": len(cells),
        "pair_shadow_rank_kernel": [159, 21],
        "committed_readout_rank_residual": [14, 7],
        "support_profile_sorted": sorted(support_profile),
        "squared_norms": [str(value) for value in norm_profile],
        "basis_records": records,
    }


def toric_first_order_gate(monomials, residuals, cells):
    occurrence_index = {monomial: index
                        for index, monomial in enumerate(monomials)}
    incidence_columns = tuple({
        occurrence_index[monomial]: Q(1)
        for monomial in monomials if cell in monomial
    } for cell in cells)
    incidence_rank = sparse_rank(incidence_columns)
    residual_columns = tuple({
        occurrence_index[monomial]: coefficient
        for monomial, coefficient in residual.items()
    } for residual in residuals)
    combined_rank = sparse_rank(incidence_columns + residual_columns)
    require(combined_rank == incidence_rank + len(residuals),
            ("residual met the toric tangent", incidence_rank, combined_rank))

    dual_records = []
    for basis_index, residual in enumerate(residuals):
        norm = sum((coefficient * coefficient
                    for coefficient in residual.values()), Q(0))
        pairings = []
        for column in incidence_columns:
            pairing = sum((residuals[basis_index].get(
                monomials[position], Q(0)) * coefficient
                for position, coefficient in column.items()), Q(0))
            pairings.append(pairing)
        require(not any(pairings), ("I^T r stopped vanishing", basis_index))
        normalized_value = sum((coefficient * coefficient / norm
                                for coefficient in residual.values()), Q(0))
        require(normalized_value == 1,
                ("normalized circuit dual changed", basis_index))
        dual_records.append({
            "basis": basis_index,
            "functional": f"psi_{basis_index}=r_{basis_index}/<r_{basis_index},r_{basis_index}>",
            "on_every_log_scalar_tangent": 0,
            "on_own_occurrence_direction": 1,
        })
    return {
        "active_torus_base_occurrence_weights": "all 180 coefficient occurrences have weight one",
        "log_scalar_tangent_formula": "delta(m)=sum_(cell in m) z_cell",
        "incidence_matrix_shape": [len(monomials), len(cells)],
        "incidence_rank": incidence_rank,
        "residual_rank": len(residuals),
        "rank_incidence_plus_residual7": combined_rank,
        "orthogonality_identity": "I^T*r_j=0 for j=0,...,6",
        "cut_cycle_intersection": "im(I) intersect ker(I^T)=0 over Q",
        "physical_first_order_occurrence_redistributions_among_residual7": 0,
        "normalized_local_duals": dual_records,
    }


def free_occurrence_vs_physical_support_audit():
    return {
        "free_occurrence_presentation": {
            "integration": "c_m(t)=1+t*r_m",
            "linear_complete_row_single_cell_pair_equations_preserved": True,
            "can_kill_one_occurrence_coefficient": True,
            "physical_scalar_factorization_preserved": False,
            "H0_changed": True,
        },
        "physical_scalar_presentation": {
            "first_order_lift_exists": False,
            "minimum_occupied_scalar_support_applies": False,
            "second_Hasse_class_reached": False,
            "reason": (
                "the residual is a normal/circuit direction to the active "
                "matching-monomial torus, not a tangent direction"
            ),
        },
        "exact_first_obstruction": (
            "the source-labelled Euler/incidence equation I*z=r_j; the "
            "normalized r_j self-dual annihilates I and reads one on r_j"
        ),
    }


def terminal_scope_audit(integrability, support_lowering):
    integrability_ledger, integrability_digest = integrability.audit()
    require(integrability_digest == integrability.EXPECTED_LEDGER_SHA256,
            integrability_digest)
    support_ledger, support_digest = support_lowering.audit()
    require(support_digest == support_lowering.EXPECTED_LEDGER_SHA256,
            support_digest)
    terminal = integrability_ledger["terminal_extension"]
    line = support_ledger["matching_affine_line"]
    require(not terminal["same_local_A_and_psi_decide_terminal_promotion"]
            and "occupied non-anchor support" in line["minimum_support_clause"],
            (terminal, line))
    return {
        "local_source_labelled_covectors_constructed": 7,
        "literal_support": "the two 90-term words with matching/fine labels",
        "accepted_augmented_terminals_constructed": 0,
        "why_not_terminal": terminal["exact_extension_criterion"],
        "why_not_support_lowering": (
            "the exact affine deletion lemma requires a physical scalar "
            "kernel direction confined to occupied non-anchor cells; the "
            "residual7 has no scalar first-order lift on the active torus"
        ),
        "next_if_a_non_toric_source_operation_is_proposed": (
            "compute its literal first boundary into the 180 occurrence rows; "
            "if it equals r_j, then compute F_[2] and use the committed "
            "lift-or-augmented-terminal alternative"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "residual7_toric_base",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "residual7_toric_commutator",
    )
    integrability = load(
        "computations/verify_h3_occurrence_kernel_integrability_terminal_gate.py",
        "residual7_toric_integrability",
    )
    support_lowering = load(
        "computations/verify_h3_pf_dark_kernel_support_lowering_hasse_coloop_gate.py",
        "residual7_toric_support",
    )

    monomials, residuals, cells, basis_ledger = exact_residual_basis_audit(
        base, commutator)
    ledger = {
        "theorem": "h3 residual7 occurrence-toric integrability gate",
        "pins": PINS,
        "exact_residual_basis": basis_ledger,
        "physical_first_order_toric_gate":
            toric_first_order_gate(monomials, residuals, cells),
        "free_occurrence_vs_physical_support":
            free_occurrence_vs_physical_support_audit(),
        "terminal_scope": terminal_scope_audit(integrability, support_lowering),
        "verdict": (
            "None of the seven carrier residuals is a physical first-order "
            "occurrence redistribution on the active scalar-factor torus.  "
            "The exact committed single-cell equations give I^T r_j=0, while "
            "every support-preserving scalar tangent lies in im(I); positive "
            "definiteness over Q makes the intersection zero.  Thus the "
            "minimum-support/Hasse exit stops at the first Euler-incidence "
            "lift I z=r_j, before a second Hasse class exists.  Freely "
            "integrating r_j in independent occurrence coordinates changes "
            "the physical presentation/H0.  The normalized self-pairings "
            "supply seven literal local covectors, but accepted terminal "
            "promotion still needs extension through the exhaustive augmented map"
        ),
        "scope": (
            "exact rational reconstruction of the canonical seven residual "
            "basis and the active coefficient-torus logarithmic tangent.  It "
            "does not exclude a non-toric relative source operation whose "
            "first boundary is one residual, nor does it analyze boundary "
            "strata where some decorated scalar factors vanish"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("residual7 toric ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "basis", "toric", "terminal"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 residual7 occurrence-toric gate ({arguments.mode}): PASS")
        print("exact residual basis: DIMENSION 7")
        print("physical scalar occurrence tangents among residuals: ZERO")
        print("first obstruction: EULER/INCIDENCE, BEFORE SECOND HASSE")
        print("normalized local source covectors: SEVEN")
        print("accepted augmented terminal: NOT YET")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
