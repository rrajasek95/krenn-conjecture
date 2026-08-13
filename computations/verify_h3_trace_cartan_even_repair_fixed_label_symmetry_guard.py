#!/usr/bin/env python3
"""Show that canonical covariance cannot duplicate one fixed repair section.

In the canonical faces-(3,5) grade, the complete physical site/colour
stabilizer acts on (B0,...,B5) through the order-two permutation
(B0 B5)(B2 B3), fixing B1 and B4 separately.  Thus covariance from a
constructed B1 (respectively B4) section never produces B4 (respectively
B1).  The two C4 realizations also have different source-orbit forms: B4 is
represented by a rho-fixed matching, while B1 is a rho-average of a two-cycle.

Consequently a uniform theorem quantified over *every* fixed target choice
would close the even labelled-residue input, but an existential ``one fixed
section'' theorem or covariance from one seed does not.  The direct-free
denominator packet passes both evaluated face memberships only conditionally;
the tilted packet passes B4 and fails B1, so it supplies a sharp control.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py":
        "bd20b6320172f846d7c4aa38ec6ebba0c0cfea4c056b8758df19d31b5ab20231",
    "computations/verify_h3_denominator_tor_two_repair_projection_gate.py":
        "b2baa9f90310002a9eb0001d8e757f8f7518295a3a8dbe7869ea29a5db880c3d",
    "computations/verify_h3_trace_cartan_even_repair_anchor_residue_fibre_gate.py":
        "3012b12ed19c1453e9d14a95beee3542d4385e70c53a553661a5d3cd1bcdb1a9",
}
EXPECTED_LEDGER_SHA256 = (
    "a831df876b698e2602bd7ff4171005130ab990ec5626016789fa4ed19fa4e856"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def unit(index, width=6):
    return tuple(Q(int(index == position)) for position in range(width))


def apply_action(action, vector):
    answer = [Q(0)] * len(vector)
    for source, target in enumerate(action):
        answer[target] += Q(vector[source])
    return tuple(answer)


def orbit(action, seed):
    found = {seed}
    current = action[seed]
    while current not in found:
        found.add(current)
        current = action[current]
    return tuple(sorted(found))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    support = load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "fixed_label_symmetry_support",
    )
    repair = load(
        "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py",
        "fixed_label_symmetry_repair",
    )
    two = load(
        "computations/verify_h3_denominator_tor_two_repair_projection_gate.py",
        "fixed_label_symmetry_two_membership",
    )
    even = load(
        "computations/verify_h3_trace_cartan_even_repair_anchor_residue_fibre_gate.py",
        "fixed_label_symmetry_even",
    )

    support_ledger, support_digest = support.audit()
    require(support_digest == support.EXPECTED_LEDGER_SHA256,
            "the physical stabilizer theorem changed")
    component = support_ledger["canonical_component"]
    require(component["physical_grade_automorphisms"] == 4
            and component["induced_pure_action"]
                == "(0 5)(2 3), with 1 and 4 fixed",
            "the physical pure-label stabilizer changed")

    # Endpoint permutations act trivially on pure multiplier labels, so the
    # image of the full four-element physical stabilizer is this C2 action.
    action = (5, 1, 3, 2, 4, 0)
    identity = tuple(range(6))
    require(tuple(action[action[index]] for index in range(6)) == identity,
            "the nontrivial pure-label action stopped being an involution")
    orbits = tuple(sorted({orbit(action, index) for index in range(6)},
                          key=lambda value: value[0]))
    require(orbits == ((0, 5), (1,), (2, 3), (4,)),
            ("the physical label orbits changed", orbits))

    b1 = unit(1)
    b4 = unit(4)
    v = tuple((left + right) / 2 for left, right
              in zip(b1, b4, strict=True))
    require(apply_action(action, b1) == b1
            and apply_action(action, b4) == b4
            and apply_action(action, v) == v,
            "a fixed target direction changed parity")
    require({apply_action(group_element, b1)
             for group_element in (identity, action)} == {b1}
            and {apply_action(group_element, b4)
                 for group_element in (identity, action)} == {b4},
            "canonical covariance unexpectedly exchanged B1 and B4")

    # One fixed unit plus the scalar diagonal and physical Cartan line still
    # does not contain the even direction.  Both independent fixed units do.
    diagonal = (Q(1),) * 6
    cartan = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
    base_rank = rank((diagonal, cartan))
    require(base_rank == 2
            and rank((diagonal, cartan, b1)) == 3
            and rank((diagonal, cartan, b1, v)) == 4
            and rank((diagonal, cartan, b4)) == 3
            and rank((diagonal, cartan, b4, v)) == 4
            and rank((diagonal, cartan, b1, b4))
                == rank((diagonal, cartan, b1, b4, v)) == 4,
            "the one-versus-two fixed-section span guard changed")

    # Replay the literal source-orbit distinction of the two fixed outputs.
    repair_ledger, repair_digest = repair.audit()
    require(repair_digest == repair.EXPECTED_LEDGER_SHA256,
            "the C4 repair census changed")
    records = repair_ledger["C4_repair_census"]["records"]
    require(len(records) == 4
            and all(record["fixed_orbit_choices"] == [
                "rho-fixed matching 7 or 14 -> B4",
                "rho-average (matching 1 + matching 9)/2 -> B1",
            ] for record in records),
            "the B1/B4 source-orbit realizations changed")
    require(repair_ledger["protected_base_guard"]
            ["can_cancel_r0_target_and_ainc"] is False,
            "the old C4 candidates became protected source boundaries")

    # The only positive two-face calculation is still conditional.  It is a
    # useful control: direct-free sees both B4/B1 routes, while tilted sees
    # face3->B4 only and misses face5->B1.
    two_ledger, two_digest = two.audit()
    require(two_digest == two.EXPECTED_LEDGER_SHA256,
            "the two-membership theorem changed")
    direct = two_ledger["direct_free"]["projections"][
        "evaluated_tail_faces_3_5"]
    tilted = two_ledger["tilted"]["projections"][
        "evaluated_tail_faces_3_5"]
    require(direct["projected_rank"] == 2
            and direct["two_section_memberships"] == [True, True]
            and tilted["projected_rank"] == 1
            and tilted["two_section_memberships"] == [True, False],
            "the evaluated face3/face5 membership control changed")

    # Content pinning above freezes the expensive complete-row audit.  The
    # theorem's frozen digest/name guard the precise conclusion used here.
    even_source = (ROOT / "computations/verify_h3_trace_cartan_even_repair_anchor_residue_fibre_gate.py").read_text()
    require(even.EXPECTED_LEDGER_SHA256
            == "7c869d6660a62bcdb6e2874d848b82fb6f0c2b5fc1540435dbd3583d9d4b9fc5"
            and '"coarse_name": "d_even"' in even_source,
            "the even labelled-residue gate changed")

    ledger = {
        "theorem": "fixed-label symmetry guard for the tau_plus even repair",
        "pins": PINS,
        "canonical_physical_stabilizer": {
            "full_site_colour_automorphisms": 4,
            "pure_label_image_order": 2,
            "nontrivial_action": "(B0 B5)(B2 B3)",
            "label_orbits": [["B" + str(index) for index in group]
                              for group in orbits],
            "B1_to_B4_by_physical_grade_symmetry": False,
            "multi_step_symmetry_escape": False,
            "reason": (
                "any composition of physical site/colour symmetries which "
                "returns to this fine grade lies in the exhaustively computed "
                "stabilizer and therefore fixes B1 and B4 separately"
            ),
        },
        "source_orbit_typing": {
            "B4": "rho-fixed matching 7 or 14",
            "B1": "rho-average of matching 1 and matching 9",
            "same_constructor_by_rho_covariance": False,
            "old_frame_C4_typing_is_a_relative_boundary": False,
        },
        "uniform_theorem_logic": {
            "one_existential_fixed_section_suffices_for_even_repair": False,
            "one_fixed_seed_plus_canonical_covariance_suffices": False,
            "one_fixed_unit_plus_diagonal_and_Cartan_suffices": False,
            "theorem_for_every_allowed_fixed_C4_target_suffices": True,
            "direct_construction_of_d_even_suffices": True,
            "minimal_remaining_choice": (
                "construct the second independent fixed section, or directly "
                "construct the equal rho-even sum d_even=(d_B1+d_B4)/2"
            ),
        },
        "denominator_control": {
            "route_order": ["face3->B4", "face5->B1"],
            "direct_free_memberships": [True, True],
            "tilted_memberships": [True, False],
            "physical_labelled_sections_constructed": False,
            "consequence": (
                "the direct-free packet is evidence for a two-fixed-section "
                "theorem after placement, not such a theorem; the tilted "
                "packet proves that one visible fixed route does not force "
                "the other"
            ),
        },
        "verdict": (
            "no committed physical symmetry or Gate-I theorem duplicates one "
            "fixed labelled-residue section into both B1 and B4.  Uniformity "
            "must be componentwise in the target choice, not merely natural "
            "under the canonical involution"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("fixed-label symmetry ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 tau_plus fixed-label symmetry: SHARP GUARD")
    print("canonical action: (B0 B5)(B2 B3), B1 and B4 fixed separately")
    print("one fixed section plus covariance: DOES NOT give the other")
    print("uniform theorem over every fixed target: WOULD close d_even")
    print("direct-free face3/5 memberships: 2; tilted: only B4")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
