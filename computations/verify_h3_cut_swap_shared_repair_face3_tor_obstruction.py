#!/usr/bin/env python3
"""Reduce the Gate-I shared repair to one face-3 Tor class and obstruct it.

For the canonical faces-(3,5) repeated component, choose the rho-fixed C4
repair B4 and the rho-paired repairs B0,B5.  Literal decorated matching
census identifies their sum with the complete face-3 endpoint packet

    q_34:11 * (q_(3,12|45) + q_(3,14|25) + q_(3,15|24)).

Thus the tempting endpoint/PP/bar construction of both labelled residue
sections factors through the selected face-3 denominator transgression e3.
On the exact clean C5 slice, however, reset-word projection sends every
denominator kernel projection y to sum_v h_v y_v=0, with all h_v=1.
The primitive covector epsilon=(1,1,1,1,1) therefore kills the physical
Tor image but evaluates to one on e3.  Endpoint/PP matching differences and
the physical Cartan residue have zero augmentation and cannot change this.

This obstructs this complete standard source route; it is not a no-go for
an additional higher relative cell, nor a physical terminal annihilator.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py":
        "bd20b6320172f846d7c4aa38ec6ebba0c0cfea4c056b8758df19d31b5ab20231",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py":
        "b1d1a62d229d9ebb3d20abbc7359503af08506fec882f629ee95a886c58490a8",
    "computations/verify_h3_denominator_tor_transgression_fitting_gate.py":
        "33cd6ac3de85f83ee16189601930938d73f35f2fef5db20253380801bdd78459",
    "computations/verify_h3_rootless_endpoint_word_change_attachment_or_dual.py":
        "a98a37e07b7847c4484de9505b1f833fc269b02126091d3ee92463bc65ad60d4",
    "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py":
        "96280ef01c70b4f3381e6d85d2c9fb64b1620850305a4346601fccbd7d63dc44",
}
EXPECTED_LEDGER_SHA256 = "ef2c8f58a5fd0fe33082fd79460477fbdacabb9c7d1ef1628a0487c7eccc0253"

RHO_TARGET = (5, 1, 3, 2, 4, 0)
CYCLE = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))


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


def graph(multiplier):
    return tuple(sorted((left, right) for left, right, _lc, _rc in multiplier))


def unit(index: int, size: int) -> tuple[Q, ...]:
    return tuple(Q(int(position == index)) for position in range(size))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    repair = load(
        "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py",
        "face3_tor_repair",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "face3_tor_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "face3_tor_base",
    )
    tor = load(
        "computations/verify_h3_denominator_tor_transgression_fitting_gate.py",
        "face3_tor_denominator",
    )
    endpoint = load(
        "computations/verify_h3_rootless_endpoint_word_change_attachment_or_dual.py",
        "face3_tor_endpoint",
    )

    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    require((left, right) == (3, 5), "the canonical face pair moved")
    degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    require(len(component["columns"]) == 288 and len(pure) == 6,
            "the canonical repeated component changed")
    graphs = tuple(graph(multiplier) for multiplier, _boundary in pure)
    require(len(set(graphs)) == 6, "the pure multiplier graphs collided")

    # Every pure P3+K2 multiplier has two endpoint decompositions: the tail
    # must join the deleted face to the repeated site.  The decoration left
    # after deleting that edge is exactly the matching q_(v,N); no colour
    # labels are forgotten.
    decompositions = []
    per_B = {}
    for index, (multiplier, _boundary) in enumerate(pure):
        site_degrees = {site: 0 for site in range(1, 6)}
        for left_site, right_site, _left_colour, _right_colour in multiplier:
            site_degrees[left_site] += 1
            site_degrees[right_site] += 1
        repeated = tuple(site for site, value in site_degrees.items() if value == 2)
        leaves = tuple(site for site, value in site_degrees.items() if value == 1)
        require(repeated == (4,) and len(leaves) == 4,
                ("a canonical pure multiplier lost P3+K2 type", index))
        records = []
        for face in leaves:
            tail = next(cell for cell in multiplier if face in cell[:2])
            matching = tuple(cell for cell in multiplier if cell != tail)
            covered = sorted(site for cell in matching for site in cell[:2])
            if covered != [site for site in range(1, 6) if site != face]:
                continue
            record = {
                "B": index,
                "face": face,
                "tail_multiplier": list(tail),
                "matching": [list(cell) for cell in matching],
            }
            records.append(record)
            decompositions.append(record)
        per_B[index] = records
        require(len(records) == 2,
                ("a P3+K2 multiplier lost its two endpoint decompositions", index))
    require(len(decompositions) == 12,
            "the six pure columns stopped having 12 endpoint decompositions")

    t3 = (3, 4, 1, 1)
    t5 = (4, 5, 1, 2)
    face3 = tuple(record["B"] for record in decompositions
                  if record["face"] == 3
                  and tuple(record["tail_multiplier"]) == t3)
    face5 = tuple(record["B"] for record in decompositions
                  if record["face"] == 5
                  and tuple(record["tail_multiplier"]) == t5)
    require(face3 == (0, 4, 5) and face5 == (0, 1, 2),
            ("canonical endpoint packets changed", face3, face5))

    # Pin one literal C4 assignment from f59bbc6.  On the first support
    # collapse, matching choices 10,7,2 send shared matching labels 3,4,5
    # to B0,B4,B5 respectively.  This is rho-equivariant.
    repair_ledger, repair_digest = repair.audit()
    require(repair_digest == repair.EXPECTED_LEDGER_SHA256,
            "the shared-loop repair ledger changed")
    first_record = repair_ledger["C4_repair_census"]["records"][0]
    alternatives = first_record["C4_alternatives_per_shared_label"]
    chosen = {
        3: next(target for matching, target in alternatives["3"]
                if matching == 10),
        4: next(target for matching, target in alternatives["4"]
                if matching == 7),
        5: next(target for matching, target in alternatives["5"]
                if matching == 2),
    }
    require(chosen == {3: 0, 4: 4, 5: 5}
            and RHO_TARGET[chosen[3]] == chosen[5]
            and RHO_TARGET[chosen[4]] == chosen[4],
            ("the face-3 repair assignment changed", chosen))

    fixed = unit(4, 6)
    pair = tuple(Q(int(index in (0, 5)), 2) for index in range(6))
    face3_vector = tuple(fixed[index] + 2 * pair[index]
                         for index in range(6))
    expected_face3 = tuple(Q(int(index in face3)) for index in range(6))
    require(face3_vector == expected_face3,
            "fixed plus paired repair stopped being the face-3 packet")

    # In the endpoint/denominator interface, a simultaneous source-valid
    # lift of these three occurrence sections supplies the selected face-3
    # projection e3.  On R=0 the exact reset equation forces every physical
    # denominator-kernel projection into ker(epsilon).
    endpoint_gate = endpoint.aggregate_tor_gate()
    clean = endpoint_gate["exact_R_zero_slice"]
    require(clean["h_v"] == [1, 1, 1, 1, 1]
            and clean["positive_aggregate_branch"] is False
            and clean["only_possible_branch"] == "aggregate separator",
            "the clean C5 denominator reset obstruction changed")
    epsilon = (Q(1),) * 5
    e3 = unit(2, 5)  # face order here is the literal sites 1,2,3,4,5.
    require(dot(epsilon, e3) == 1,
            "the face-3 class stopped being primitive")

    # The frozen rational denominator packets do contain e3, which is useful
    # evidence but cannot negate the clean-slice theorem: neither packet is
    # a point of the full source scheme.  Record this counterguard explicitly.
    frozen = {}
    for name in ("direct_free", "tilted"):
        packet = tor.packet_audit(name)
        require(packet["individual_classes_hit"]
                == [True, False, True, False, False],
                ("a frozen Tor packet changed", name))
        frozen[name] = {
            "transgression_rank": packet["transgression_rank"],
            "face3_hit": packet["individual_classes_hit"][2],
            "is_full_source_point": False,
        }

    cartan_residue = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
    require(sum(cartan_residue) == 0,
            "the physical Cartan residue acquired augmentation")
    matching_differences = tuple(
        tuple(unit(i, 3)[j] - unit(k, 3)[j] for j in range(3))
        for i in range(3) for k in range(i + 1, 3)
    )
    require(all(sum(value) == 0 for value in matching_differences),
            "a same-face matching difference acquired aggregate")

    ledger = {
        "theorem": "Gate-I shared repair reduces to an obstructed face-3 Tor class",
        "pins": PINS,
        "canonical_component": {
            "faces": [left, right],
            "fine_degree": list(degree),
            "columns": len(component["columns"]),
            "pure_columns": len(pure),
            "pure_graphs": [[list(edge) for edge in value] for value in graphs],
            "endpoint_decompositions": decompositions,
            "face3_packet": list(face3),
            "face5_packet": list(face5),
        },
        "rho_equivariant_shared_assignment": {
            "shared_matching_to_B": {str(key): value for key, value in chosen.items()},
            "fixed_direction": "B4",
            "paired_direction": "(B0+B5)/2",
            "combined_three_label_image": "B0+B4+B5",
            "literal_endpoint_identification": (
                "q_34:11*(q_(3,12|45)+q_(3,14|25)+q_(3,15|24))"
            ),
        },
        "denominator_Tor_route": {
            "required_selected_projection": "e_3",
            "clean_reset_equation": "sum_v h_v*y_v=0",
            "clean_h": clean["h_v"],
            "primitive_dual": "epsilon=(1,1,1,1,1)",
            "epsilon_on_required_e3": 1,
            "matching_PP_Bianchi_differences_have_epsilon": 0,
            "physical_Cartan_residue_has_augmentation": 0,
            "verdict": (
                "no clean-slice denominator-kernel construction of both "
                "labelled sections through the face-3 packet"
            ),
        },
        "frozen_specialization_counterguard": frozen,
        "sharp_remaining_statement": (
            "construct a higher relative occurrence-splitting cell outside "
            "the standard denominator-kernel/endpoint-PP route whose three "
            "outputs are B0,B4,B5 with protected rows zero, or extend "
            "epsilon across that enlarged physical source as a terminal "
            "separator"
        ),
        "Gate_I_assembly_now": False,
        "scope": (
            "exact canonical decorated matching census and exact clean-C5 "
            "denominator-Tor obstruction.  The primitive epsilon is a source-"
            "route obstruction; its promotion to the full physical Fredholm "
            "annihilator still requires the committed Omega/ridge and terminal "
            "extension guards"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("face-3 Tor obstruction ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 Gate-I shared repair: FACE-3 TOR OBSTRUCTION")
    print("rho assignment: labels 3,4,5 -> B0,B4,B5")
    print("combined packet: q_34 * h_3")
    print("required Tor projection: e3; clean epsilon(e3)=1")
    print("standard denominator/PP/bar construction: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
