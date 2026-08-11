#!/usr/bin/env python3
"""Exact affine/Hall boundary for multisite endpoint-star concentration.

For fixed q and opposite star rows, replacing one endpoint row is an affine
joint-kernel problem.  A selected diagonal matching gives a nonzero term at
an ordered hole pair, but does not imply that the affine response fibre
meets the corresponding target-coordinate line.  Minimum support instead
makes the occupied response columns independent and produces a unique
full-support circuit modulo the target.

Before that affine line-hitting problem, four distinct ordered holes exist
iff the two families of diagonal-response hole pairs contain disjoint
physical edges.  If two nonempty edge families are cross-intersecting, the
first has matching number at most two: matching number one is contained in
a star or triangle, while matching number two confines the other family to
the K2,2 rectangle between two disjoint edges.  This is the exact Hall
normal form, not a support-cardinality search.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AFFINE_PATH = "computations/verify_n8_one_bad_affine_coordinate_concentration_guard.py"
HESSIAN_PATH = "computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py"
PINS = {
    AFFINE_PATH:
        "cbc615239037fc5f9664fb1846043a1aa523f716c19d8a03cba4e239c07eb4ab",
    "notes/n8-one-bad-affine-coordinate-concentration-guard.md":
        "275613605e5b36b6fb7776848de4cac5a770ef9c442a4be2d3dcef2f92a860a4",
    HESSIAN_PATH:
        "1594dcac16bb77bb929c18edda224e215ea99697bfd36edabc4230a0d341b5c8",
    "notes/uniform-one-bad-axis-hessian-carrier-circuit-boundary.md":
        "d784f8d25461ffcdafcc3fb9a39ccc776f770fb63359f722bead4fe7c965e73e",
    "computations/verify_n8_lemma_e_unary_top_channel_synchronization.py":
        "822c9ff2b0839f3c91fe317218b5ddf4861bd737f912a9b85e9b51e324db243e",
    "notes/n8-lemma-e-unary-top-channel-synchronization.md":
        "2c00687a7ce18aa4c7152de1bb6dd2300e00de007ad04ce4c6200077f67572bf",
    "computations/verify_uniform_anchor_edge_offdiagonal_alternating_exit_dichotomy.py":
        "2de838ff96118a7c54df23c8df02202090a52a3b0ca83f62c400a7a8241f37b8",
    "notes/uniform-anchor-edge-offdiagonal-alternating-exit-dichotomy.md":
        "9b4d2dabf493845de4570008835d544cdb0a9591c5272758e5390f19e70bdc02",
    "computations/verify_uniform_cubic_anchor_union_incidence_dichotomy.py":
        "89b7383c8d604f1bc9c99cd61501be589895054fd754c374c89393fca635b501",
    "notes/uniform-cubic-anchor-union-incidence-dichotomy.md":
        "227f2ec779d270b952fee2c1f6f948c9c2da4ea7a25de06c14549859d09f72d8",
}
EXPECTED_LEDGER_SHA256 = "2168b112db11f4e652d1bc70e6569b0319f455ddf61fffc8cad8cbd073810613"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value
                             for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def in_span(columns, target):
    if not columns:
        return not any(target)
    rows = len(target)
    matrix = [[columns[column][row] for column in range(len(columns))]
              for row in range(rows)]
    return rank(matrix) == rank([
        row_values + [target[row]]
        for row, row_values in enumerate(matrix)
    ])


def affine_block_candidates(columns, target, site_blocks):
    """Sites whose coordinate block contains an exact target preimage."""
    return tuple(site for site, indices in site_blocks.items()
                 if in_span([columns[index] for index in indices], target))


def audit_exact_affine_replacement():
    # A bilinear two-output response B.  Left changes k_i are chosen in the
    # joint kernel against both fixed right rows; right changes l_j are then
    # chosen in the joint kernel against the changed left rows.  Bilinearity
    # makes the sequential replacement exact, not infinitesimal.
    # The third coordinate is an honest common radical on both sides, so
    # the example exercises nonzero finite translations rather than only
    # the tautological zero displacement.
    tensor = (
        ((Q(1), Q(0)), (Q(0), Q(1)), (Q(0), Q(0))),
        ((Q(0), Q(1)), (Q(1), Q(0)), (Q(0), Q(0))),
        ((Q(0), Q(0)), (Q(0), Q(0)), (Q(0), Q(0))),
    )

    def bilinear(left, right):
        return tuple(sum(left[i] * right[j] * tensor[i][j][output]
                         for i in range(3) for j in range(3))
                     for output in range(2))

    p = ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)))
    s = ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)))
    k = ((Q(0), Q(0), Q(1)), (Q(0), Q(0), Q(-2)))
    p_new = tuple(tuple(p_i[index] + k_i[index] for index in range(3))
                  for p_i, k_i in zip(p, k, strict=True))
    require(all(bilinear(k_i, s_j) == (0, 0)
                for k_i in k for s_j in s),
            "the left joint-kernel criterion changed")
    require(all(bilinear(p_new[i], s[j]) == bilinear(p[i], s[j])
                for i in range(2) for j in range(2)),
            "the exact left replacement failed")
    ell = ((Q(0), Q(0), Q(3)), (Q(0), Q(0), Q(-1)))
    s_new = tuple(tuple(s_j[index] + ell_j[index] for index in range(3))
                  for s_j, ell_j in zip(s, ell, strict=True))
    require(all(bilinear(p_i, ell_j) == (0, 0)
                for p_i in p_new for ell_j in ell),
            "the right joint-kernel criterion changed")
    require(all(bilinear(p_new[i], s_new[j]) == bilinear(p[i], s[j])
                for i in range(2) for j in range(2)),
            "the sequential concentration criterion stopped being exact")
    return {
        "left_condition": "B(k_i,s_1)=B(k_i,s_2)=0",
        "right_condition": "B(p'_1,ell_j)=B(p'_2,ell_j)=0",
        "conclusion": "B(p'_i,s'_j)=B(p_i,s_j) for all i,j",
        "order": "left affine replacement, then recompute right fibres",
    }


def edges(vertices=range(6)):
    return tuple(itertools.combinations(vertices, 2))


def matching_number_two_or_less(family):
    return not any(set(first).isdisjoint(second)
                   and set(first).isdisjoint(third)
                   and set(second).isdisjoint(third)
                   for first, second, third
                   in itertools.combinations(family, 3))


def contained_in_star_or_triangle(family):
    vertices = set(itertools.chain.from_iterable(family))
    for centre in vertices:
        if all(centre in pair for pair in family):
            return "star"
    for triangle in itertools.combinations(vertices, 3):
        if all(set(pair) <= set(triangle) for pair in family):
            return "triangle"
    return None


def audit_cross_intersecting_hall_theorem():
    all_edges = edges()
    category = Counter()
    audited = 0
    # It suffices to enumerate the first family.  Its maximal possible mate
    # family consists of all edges meeting every member; every actual second
    # family is a subset of this maximal transversal family.
    for mask in range(1, 1 << len(all_edges)):
        first = tuple(all_edges[index] for index in range(len(all_edges))
                      if mask & (1 << index))
        second_max = tuple(pair for pair in all_edges
                           if all(set(pair) & set(member)
                                  for member in first))
        if not second_max:
            continue
        audited += 1
        require(matching_number_two_or_less(first),
                "a nonempty cross-intersector met three disjoint edges")
        has_disjoint_pair = next((pair for pair in itertools.combinations(
            first, 2) if set(pair[0]).isdisjoint(pair[1])), None)
        if has_disjoint_pair is None:
            shape = contained_in_star_or_triangle(first)
            require(shape in ("star", "triangle"),
                    "a pairwise-intersecting edge family left star/triangle")
            category[shape] += 1
            continue
        left, right = has_disjoint_pair
        rectangle = {
            tuple(sorted((u, v))) for u in left for v in right
        }
        require(set(second_max) <= rectangle,
                "the cross-intersector escaped the four-site K2,2")
        category["four_site_rectangle"] += 1
    require(audited == 5141,
            f"the cross-intersecting maximal-family count changed: {audited}")
    require(category == Counter({
        "star": 171, "triangle": 20, "four_site_rectangle": 4950,
    }), f"the Hall normal-form histogram changed: {category}")

    # For two already selected diagonal terms, four distinct physical ports
    # are exactly the assertion that their two hole edges are disjoint.
    pair_histogram = Counter(
        "four_distinct_ports" if set(first).isdisjoint(second)
        else "Hall_collision"
        for first in all_edges for second in all_edges
    )
    require(pair_histogram == Counter({
        "Hall_collision": 135, "four_distinct_ports": 90,
    }), "the selected-hole Hall count changed")
    return {
        "nonempty_first_families_with_nonempty_cross_intersector": audited,
        "maximal_cross_intersection_types": dict(category),
        "selected_ordered_hole_pair_count": dict(pair_histogram),
        "uniform_theorem": (
            "no disjoint selected hole pair implies star/triangle or a "
            "four-site K2,2 cross-intersection normal form"
        ),
    }


def audit_physical_affine_line_hitting(affine):
    q = affine.q_data()
    ledger = affine.affine_fibre_audit(q)
    require(ledger["response"] == "X1"
            and ledger["multisite_p"] == ["e1@0", "e1@1"],
            "the physical multisite response guard changed")
    require(not ledger["literal_target_columns"],
            "the physical affine guard acquired a coordinate candidate")

    # Rebuild its nine independent nonzero columns abstractly.  The target
    # is in their total span, but no individual target-axis site line spans
    # it.  This is exactly the distinction between a selected response term
    # and an affine coordinate point.
    x, y = (Q(1), Q(0)), (Q(0), Q(1))
    occupied = ((Q(1), Q(1)), (Q(0), Q(-1)))
    target = x
    require(in_span(occupied, target)
            and not any(in_span((column,), target) for column in occupied),
            "the two-column affine line-hitting guard changed")
    candidates = affine_block_candidates(
        occupied, target, {0: (0,), 1: (1,)})
    require(candidates == (),
            "a minimum two-site circuit acquired a target-line candidate")
    return {
        "physical_q_cells": len(q),
        "response": "(e1@0+e1@1)*(e1@5)*q^[2]=X1",
        "occupied_columns": ["X1+Y", "-Y"],
        "occupied_column_rank": 2,
        "affine_target_coordinate_candidates": list(candidates),
        "missing_full_packet_rows": [
            "q^[3]=X0", "the X2 diagonal row", "both crossed companions",
        ],
    }


def audit_minimum_support_circuit(hessian):
    audits = hessian.audit_linear_circuit_normal_form()
    require(len(audits) == 7
            and all(record["column_rank"] == record["occupied_sites"]
                    and record["target_quotient_rank"]
                    == record["occupied_sites"] - 1
                    for record in audits),
            "the minimum-support quotient-circuit theorem changed")
    return audits


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    affine = load(AFFINE_PATH, "multisite_affine_guard")
    hessian = load(HESSIAN_PATH, "multisite_hessian_boundary")
    ledger = {
        "exact_sequential_joint_kernel_concentration":
            audit_exact_affine_replacement(),
        "selected_hole_hall_normal_form":
            audit_cross_intersecting_hall_theorem(),
        "minimum_support_response_circuits":
            audit_minimum_support_circuit(hessian),
        "physical_affine_line_hitting_guard":
            audit_physical_affine_line_hitting(affine),
        "sharp_concentration_criterion": (
            "choose disjoint diagonal-response hole pairs; the left affine "
            "fibres must meet target-coordinate lines at the chosen p "
            "sites, then the recomputed right affine fibres must meet "
            "target-coordinate lines at distinct s sites.  Joint-kernel "
            "differences preserve all four responses exactly; anchor safety "
            "additionally requires every deleted coordinate to be "
            "unprotected or carried by an anchor-preserving switch"
        ),
        "exact_obstruction": (
            "either the two selected-hole families are cross-intersecting "
            "(star/triangle/K2,2 Hall type), or a required affine fibre "
            "misses every target-coordinate line and minimum support leaves "
            "a full-support quotient circuit.  A selected matching term "
            "proves neither line-hitting nor anchor safety"
        ),
        "free_active_alternative": (
            "if a circuit carrier supplies a nonzero active product at a "
            "free selected-anchor companion, the pinned c78fc9b theorem "
            "lands in the distinct-head four-good branch; the unresolved "
            "circuits have all active products trapped in the selected "
            "anchor web"
        ),
        "scope": (
            "exact linear/Hall reduction and physical common-q response "
            "guard, not a full one-bad counterexample: the guard omits the "
            "unary top and second-colour companion packet.  The missing "
            "proof is the full-packet theorem forcing line-hitting or a "
            "free active carrier"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"multisite affine/Hall ledger changed: {digest}")
    print("uniform multisite endpoint affine/Hall boundary: PASS")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
