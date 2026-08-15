#!/usr/bin/env python3
"""Finite h=3 Beck--Chevalley audit for the full marked collision species.

The response trigger and cap collision descriptions are compared before
forgetting the missing-site/fine mark.  With that mark the first P3+K2
square is a literal bijection.  The full derived cap fibre is the product
of the replacement 5-simplex with the two-tail 1-simplex, hence a free
resolution of the same 90-parent module as the response simplex.

This does not silently identify the derived cap totalization with physical
r0.  The final audit separates the derived SDR from the protected Eq and
pointed-augmentation descent required by PAComp.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py":
        "3ca82479bd2d1c2847dff55f3c05c87f24406ec1c2f3a5fbb9cdf619a6f7047a",
    "computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py":
        "26259bb67476a30c4237c20f8e393ec919e934f95bab0d0c6845adc9295c3132",
    "computations/verify_h3_endpoint_even_literal_operator_algebra_r0_action_gate.py":
        "42a30f9cd823a67a0733dfb6961ed224e228caa3236140c2e0803db686839ef7",
    "computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py":
        "9e60fb8410288a192b8be3b59938e5e7ba4ea42b455fee67b94ca6ef37777fde",
    "computations/verify_h3_selected_lower_excess_orbit_pointed_comparison_gate.py":
        "057ca135e410ccf597a90a034e08868b3c901223981ca68662d6ad72414e4759",
    "computations/verify_h3_normalized_eq_base_change_tor_gate.py":
        "b7c409db8cff0141a153816d0d14525464c4fcadb0607b97da06181435059d50",
}
EXPECTED_LEDGER_SHA256 = (
    "519a980ee5f935db8d924324a9321b42848a83ffc0aa00eb1e3da476e345e1ee"
)
SITES = frozenset(range(8))
DIRECT_FREE_EDGE = (3, 6)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def perfect_matchings(vertices: frozenset[int]):
    if not vertices:
        yield frozenset()
        return
    first = min(vertices)
    for second in sorted(vertices - {first}):
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(vertices - {first, second}):
            yield tail | {edge}


def site_profile(edges: frozenset[tuple[int, int]]) -> tuple[int, ...]:
    degree = Counter(site for edge in edges for site in edge)
    return tuple(sorted(degree.values(), reverse=True))


def collision_species_audit() -> dict[str, object]:
    parents = tuple(matching for matching in perfect_matchings(SITES)
                    if DIRECT_FREE_EDGE not in matching)
    require(len(parents) == len(set(parents)) == 90, len(parents))

    branches = []
    branch_seen = {}
    marked_faces = []
    unmarked_fibres = defaultdict(list)
    marked_face_seen = {}
    deletion_types = Counter()
    for parent_index, parent in enumerate(parents):
        source_edge = next(edge for edge in parent if 0 in edge)
        missing = source_edge[1] if source_edge[0] == 0 else source_edge[0]
        for doubled in range(1, 8):
            if doubled == missing:
                continue
            inserted = (0, doubled)
            branch = (parent - {source_edge}) | {inserted}
            branch_record = (parent_index, missing, doubled, branch)
            require(branch not in branch_seen,
                    ("collision branch lost parent recovery", branch,
                     branch_seen.get(branch), branch_record))
            branch_seen[branch] = branch_record
            branches.append(branch_record)

            for removed in sorted(branch):
                cofactor = branch - {removed}
                profile = site_profile(cofactor)
                if profile == (2, 1, 1, 1, 1):
                    kind = "P3+K2"
                elif profile == (1, 1, 1, 1, 1, 1):
                    kind = "3K2"
                else:
                    raise RuntimeError(("unexpected cofactor", profile))
                deletion_types[kind] += 1
                if kind != "P3+K2":
                    continue
                # The cap fine mark is the original missing site.  Given the
                # unmarked P3+K2 cofactor and this mark, the two other absent
                # sites recover the removed remote K2, hence the parent.
                cap_mark = (cofactor, missing)
                flag = (parent_index, missing, doubled, branch, removed)
                require(cap_mark not in marked_face_seen,
                        ("marked cap face ambiguous", cap_mark,
                         marked_face_seen.get(cap_mark), flag))
                marked_face_seen[cap_mark] = flag
                marked_faces.append(flag)
                unmarked_fibres[cofactor].append(flag)

    require(len(branches) == len(branch_seen) == 540
            and deletion_types == {"P3+K2": 1080, "3K2": 1080}
            and len(marked_faces) == len(marked_face_seen) == 1080,
            (len(branches), len(branch_seen), deletion_types,
             len(marked_faces), len(marked_face_seen)))
    fibre_histogram = Counter(len(fibre)
                              for fibre in unmarked_fibres.values())
    require(len(unmarked_fibres) == 380
            and fibre_histogram == {2: 60, 3: 320},
            (len(unmarked_fibres), fibre_histogram))

    # Explicit recovery verifies that the marked DQ->PS correspondence is a
    # bijection, not only an equality of cardinalities.
    for (cofactor, missing), flag in marked_face_seen.items():
        parent_index, saved_missing, doubled, branch, removed = flag
        absent = SITES - frozenset(site for edge in cofactor for site in edge)
        require(saved_missing == missing and missing in absent
                and len(absent) == 3, (cofactor, missing, absent))
        removed_vertices = tuple(sorted(absent - {missing}))
        require(removed == removed_vertices,
                ("remote edge recovery failed", removed, removed_vertices))
        recovered_branch = cofactor | {removed}
        source_edge = (0, missing)
        recovered_parent = (recovered_branch - {(0, doubled)}) | {source_edge}
        require(recovered_branch == branch
                and recovered_parent == parents[parent_index],
                (flag, recovered_branch, recovered_parent))

    return {
        "direct_free_parents": len(parents),
        "replacement_branches": len(branches),
        "branches_per_parent": 6,
        "branch_monomials_distinct": len(branch_seen),
        "first_deletion_flags": dict(sorted(deletion_types.items())),
        "marked_P3K2_flags": len(marked_faces),
        "marked_cap_fine_objects": len(marked_face_seen),
        "marked_DQ_to_PS_map_is_bijection": True,
        "unmarked_P3K2_cofactors": len(unmarked_fibres),
        "unmarked_forgetting_fibre_histogram": {
            str(size): count for size, count in sorted(fibre_histogram.items())
        },
        "unmarked_square_is_homotopy_Cartesian": False,
        "marked_square_is_strictly_Cartesian": True,
        "mark_needed_for_cartesianness": (
            "the original missing site, equivalently the retained cap fine/"
            "reinsertion label t*q_(v,N)"
        ),
        "excess_before_marking": (
            "each unmarked P3+K2 face has two or three parent/branch lifts"
        ),
    }


def simplex_basis(vertices: int, degree: int):
    return tuple(combinations(range(vertices), degree + 1))


def simplex_boundary(vertices: int, degree: int):
    if degree == 0:
        return ()
    lower = simplex_basis(vertices, degree - 1)
    lower_index = {face: index for index, face in enumerate(lower)}
    columns = []
    for face in simplex_basis(vertices, degree):
        column = {}
        for position in range(len(face)):
            lower_face = face[:position] + face[position + 1:]
            column[lower_index[lower_face]] = Q(-1 if position % 2 else 1)
        columns.append(column)
    return tuple(columns)


def sparse_rank(columns) -> int:
    basis = {}
    for original in columns:
        vector = {row: Q(value) for row, value in original.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                coefficient = vector[pivot]
                basis[pivot] = {row: value / coefficient
                                for row, value in vector.items()}
                break
            coefficient = vector[pivot]
            for row, value in basis[pivot].items():
                result = vector.get(row, Q(0)) - coefficient * value
                if result:
                    vector[row] = result
                else:
                    vector.pop(row, None)
    return len(basis)


def product_simplex_complex(left_vertices: int, right_vertices: int):
    left_max = left_vertices - 1
    right_max = right_vertices - 1
    bases = []
    for total_degree in range(left_max + right_max + 1):
        basis = []
        for left_degree in range(left_max + 1):
            right_degree = total_degree - left_degree
            if not 0 <= right_degree <= right_max:
                continue
            for left_face in simplex_basis(left_vertices, left_degree):
                for right_face in simplex_basis(right_vertices, right_degree):
                    basis.append((left_degree, left_face,
                                  right_degree, right_face))
        bases.append(tuple(basis))

    boundaries = []
    for total_degree in range(1, len(bases)):
        lower_index = {cell: index for index, cell in
                       enumerate(bases[total_degree - 1])}
        columns = []
        for left_degree, left_face, right_degree, right_face in bases[total_degree]:
            column = Counter()
            if left_degree:
                for position in range(len(left_face)):
                    lower_face = left_face[:position] + left_face[position + 1:]
                    cell = (left_degree - 1, lower_face,
                            right_degree, right_face)
                    column[lower_index[cell]] += Q(-1 if position % 2 else 1)
            if right_degree:
                tensor_sign = -1 if left_degree % 2 else 1
                for position in range(len(right_face)):
                    lower_face = right_face[:position] + right_face[position + 1:]
                    cell = (left_degree, left_face,
                            right_degree - 1, lower_face)
                    face_sign = -1 if position % 2 else 1
                    column[lower_index[cell]] += Q(tensor_sign * face_sign)
            columns.append({row: value for row, value in column.items() if value})
        boundaries.append(tuple(columns))

    # Verify d^2 directly.
    for degree in range(2, len(bases)):
        lower = boundaries[degree - 2]
        upper = boundaries[degree - 1]
        for column in upper:
            composite = Counter()
            for middle, coefficient in column.items():
                for row, value in lower[middle].items():
                    composite[row] += coefficient * value
            require(not {row: value for row, value in composite.items() if value},
                    ("product simplex d2", degree, composite))
    return tuple(bases), tuple(boundaries)


def derived_resolution_audit() -> dict[str, object]:
    response_dimensions = tuple(len(simplex_basis(6, degree))
                                for degree in range(6))
    response_ranks = tuple(sparse_rank(simplex_boundary(6, degree))
                           for degree in range(1, 6))
    require(response_dimensions == (6, 15, 20, 15, 6, 1)
            and response_ranks == (5, 10, 10, 5, 1),
            (response_dimensions, response_ranks))

    cap_bases, cap_boundaries = product_simplex_complex(6, 2)
    cap_dimensions = tuple(map(len, cap_bases))
    cap_ranks = tuple(sparse_rank(boundary) for boundary in cap_boundaries)
    require(cap_dimensions == (12, 36, 55, 50, 27, 8, 1)
            and cap_ranks == (11, 25, 30, 20, 7, 1),
            (cap_dimensions, cap_ranks))

    # Exactness including the augmentations follows from the displayed rank
    # identities.  The projection id x epsilon_Delta1 and Reynolds section
    # id x (u+v)/2 form an SDR; verify the one-simplex contraction explicitly.
    d_edge = (Q(-1), Q(1))
    section = (Q(1, 2), Q(1, 2))
    h_u, h_v = Q(-1, 2), Q(1, 2)
    require(tuple(d_edge[index] * h_u + section[index]
                  for index in range(2)) == (Q(1), Q(0))
            and tuple(d_edge[index] * h_v + section[index]
                      for index in range(2)) == (Q(0), Q(1)),
            "Delta1 SDR changed")

    return {
        "common_base": "V_parent=Q{90 direct-free perfect matchings}",
        "response_fibre": "augmented Delta^5",
        "response_chain_dimensions": list(response_dimensions),
        "response_boundary_ranks": list(response_ranks),
        "response_is_free_resolution": True,
        "derived_marked_cap_fibre": "augmented Delta^5 x Delta^1",
        "derived_cap_chain_dimensions": list(cap_dimensions),
        "derived_cap_boundary_ranks": list(cap_ranks),
        "derived_cap_is_free_resolution": True,
        "one_root_response_map_ranks_augmentation_then_d":
            [90] + [90 * rank for rank in response_ranks],
        "one_root_derived_cap_map_ranks_augmentation_then_d":
            [90] + [90 * rank for rank in cap_ranks],
        "two_root_base_dimension": 180,
        "canonical_projection": "id_Delta5 tensor epsilon_Delta1",
        "endpoint_even_section": "id_Delta5 tensor (u+v)/2",
        "Delta1_contraction": {"h(u)": "-e/2", "h(v)": "e/2"},
        "projection_after_section_is_identity": True,
        "comparison_cone_acyclic": True,
        "claim_i_projective_resolutions_same_base": True,
    }


def physical_descent_and_derived_N_audit() -> dict[str, object]:
    # The first protected descent compares the response and cap Eq copies of
    # H-u.  Coefficient forgetting ties them; the physical augmented target
    # retains both.  This is independent of the acyclic derived comparison.
    d_n = (Q(1), Q(0))
    d_r0 = (Q(0), Q(1))
    omega_eq = (Q(1), Q(-1))
    require(sparse_rank((dict(enumerate(d_n)),
                         dict(enumerate(d_r0)))) == 2
            and sum(x * y for x, y in zip(omega_eq, d_n, strict=True)) == 1
            and sum(x * y for x, y in zip(omega_eq, d_r0, strict=True)) == -1,
            "derived/underived Eq descent changed")

    # If a mixed comparison k and the existing Eq cone theta are both in the
    # same augmented category, d k = r0-N-theta has square zero precisely
    # when d theta=d r0-d N.  This verifies the proposed global cancellation
    # algebra, but not the existence/typing of k or the augmentation on N.
    difference = tuple(right - left for left, right in
                       zip(d_n, d_r0, strict=True))
    theta_boundary = difference
    second_boundary = tuple(right - left - theta for left, right, theta in
                            zip(d_n, d_r0, theta_boundary, strict=True))
    require(second_boundary == (Q(0), Q(0)), second_boundary)
    return {
        "derived_N_boundary": [1, 0],
        "underived_physical_r0_boundary": [0, 1],
        "protected_boundary_rank": 2,
        "primitive_descent_dual": [1, -1],
        "descent_excess": "(H0-u)e_Eq relative to the response copy",
        "Eq_cone_global_cancellation_formula": "d k=r0-N-theta",
        "Eq_cone_boundary": [-1, 1],
        "second_boundary_zero": True,
        "normalization_t_equals_zero_guard": {
            "evident_top_map_is_chain_map": True,
            "comparison_cone_H0_H1_H2": [1, 0, 0],
            "H0_generator": "e_Eq",
            "relative_dK_equals_tE_after_base_change_H0_H1": [1, 1],
            "absolute_dK_equals_E_H0_H1": [0, 0],
            "current_relative_K_Eq_suffices": False,
        },
        "claim_ii_underived_physical_retraction_constructed": False,
        "derived_N_can_replace_r0_unconditionally_in_current_PAComp": False,
        "why_not_yet": (
            "PAComp is a pointed augmented statement, not invariant under an "
            "unaugmented quasi-isomorphism; the species SDR does not itself "
            "define the response/cap operation, marked/global anchor, q, "
            "target, residue, W, ridge, eta or sigma readouts"
        ),
        "minimal_derived_N_consumption_hypothesis": (
            "all PAComp/descent maps factor through the augmented marked "
            "collision totalization N, and the full enriched target contains "
            "an absolute decorated Eq contraction dK=E (not only dK=tE); "
            "no conclusion may require an underived r0 representative"
        ),
        "consequence_under_hypothesis": (
            "the acyclic species comparison cone plus the absolute Eq "
            "contraction make derived N sufficient; the relative tE cone "
            "alone leaves H0=eEq and a new H1 Tor cycle"
        ),
        "first_unproved_augmented_datum": (
            "a pointed physical linearization of the marked collision "
            "correspondence carrying operation, anchor/q and protected rows"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": (
            "the full fine-marked shared-collision species gives a strict "
            "Beck-Chevalley bijection and a derived cap resolution of the "
            "same 90-parent module, but physical r0/PAComp descent still "
            "requires an augmented pointed linearization"
        ),
        "finite_collision_groupoid": collision_species_audit(),
        "derived_resolutions": derived_resolution_audit(),
        "physical_descent_and_derived_N":
            physical_descent_and_derived_N_audit(),
        "verdict": {
            "claim_i": "PROVED for the full marked derived totalization N",
            "claim_ii": "OPEN for underived physical r0",
            "derived_N_bypass": (
                "not achieved by normalization or the current relative "
                "K_Eq; valid only after an augmented-derived PAComp "
                "invariance theorem and an absolute decorated Eq contraction"
            ),
        },
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("mode", arguments.mode)
        print("ledger_sha256", digest)
        print("derived_claim", ledger["verdict"]["claim_i"])
        print("physical_claim", ledger["verdict"]["claim_ii"])


if __name__ == "__main__":
    main()
