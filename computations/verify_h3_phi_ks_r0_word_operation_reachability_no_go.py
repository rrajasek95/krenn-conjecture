#!/usr/bin/env python3
"""Compute shortest existing word/operation routes to Phi_KS,r0.

The actual root, restriction/reinsertion, occurrence-projector, fixed-window
and cap constructors are source-valid inside their literal operation
summands.  This checker builds their finite reachability shadow and then
grants the strongest possible word help: every one-site ternary root on the
response object.  The response word reaches the cap word in six roots, but
the fine/repeated/operation/window tags remain those of the response object.
The typed target is therefore unreachable.

The first new edge after this shortest word route is the degree-zero matrix
unit Phi_KS,r0 from the root-transported response occurrence to cap r0.  In
the fixed window its first local representative is a DQ-to-PS chart switch
such as A_[a|b] -> B, with all four K2,2 mates supplied by the one schema.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gamma_star_executable_gen_phys_registry.py":
        "173ebdedcfdadd9891704223ea93731509c18a4d120aa34d6c7bc8a4f3aebddb",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py":
        "39713f3683dd3d2376e5a911987ee3670ec291cf850072d6b4932e7a93745fc7",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "computations/verify_h3_centered_projector_e14_word_arrow_gate.py":
        "e1b8b17c75292f55439652ac9e5dcb1a24a3e4079c2d378e9fa63544e5491b46",
    "computations/verify_h3_tau_plus_connected_sl3_label_orbit_obstruction.py":
        "7048ab1ea5912f1be38014f193970e093c1f5d1259cc56e1e5566b1552358b52",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
}
EXPECTED_LEDGER_SHA256 = "c7f94180bc4c5be5fbf719c5836a115459f52d918a9ff73b88897f5e18325b5b"

RESPONSE_WORD = tuple(map(int, "11110000"))
CAP_WORD = tuple(map(int, "01211222"))
RESPONSE_SECTOR = "response KS / endpoint-matching orbit"
CAP_SECTOR = "AugP2 cap / K_Eq r0"


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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def word_text(word: tuple[int, ...]) -> str:
    return "".join(map(str, word))


def hamming(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    require(len(left) == len(right), "Hamming width")
    return sum(a != b for a, b in zip(left, right, strict=True))


@dataclass(frozen=True)
class State:
    word: tuple[int, ...]
    sector: str


def one_root_neighbours(word: tuple[int, ...]):
    for site, old in enumerate(word):
        for new in range(3):
            if new == old:
                continue
            changed = list(word)
            changed[site] = new
            yield tuple(changed)


def bfs_distance(start: State, target: State, allow_phi: bool) \
        -> tuple[int | None, int]:
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, distance = queue.popleft()
        if state == target:
            return distance, len(seen)
        neighbours = []
        if state.sector == RESPONSE_SECTOR:
            neighbours.extend(State(word, RESPONSE_SECTOR)
                              for word in one_root_neighbours(state.word))
            if allow_phi and state.word == CAP_WORD:
                neighbours.append(State(CAP_WORD, CAP_SECTOR))
        # All implemented cap r0/normalizer/Macaulay operations are internal.
        # They add no different-word or response-sector neighbour.
        for neighbour in neighbours:
            if neighbour in seen:
                continue
            seen.add(neighbour)
            queue.append((neighbour, distance + 1))
    return None, len(seen)


def exact_existing_word_closure(response, packaging, cartan) \
        -> dict[str, object]:
    word_ledger = packaging.word_and_fine_grade_audit()
    d4_ledger = response.d4_orbit_relative_family_audit()
    cartan_ledger = cartan.audit()
    roots = cartan_ledger["literal_root_covariance"]
    require(word_ledger["D4_cube_vertex_count"] == 16
            and not word_ledger["cap_word_in_existing_D4_cube"]
            and d4_ledger["occurrence_parameter_D4_edges"] == 32
            and roots["tail_sites"] == [2, 5]
            and roots["ordered_root_directions"] == [[1, 2], [2, 1]],
            (word_ledger, d4_ledger, roots))

    # Generously combine all sixteen D4 words, the two audited 1<->2 tail
    # roots, and the physical endpoint swap 0<->1.  This union can only make
    # reachability easier than following a single chain with target faces.
    closure = {
        tuple(map(int, "1111" + "".join(map(str, bits))))
        for bits in ((a, b, c, d) for a in (0, 1) for b in (0, 1)
                     for c in (0, 1) for d in (0, 1))
    }
    changed = True
    while changed:
        changed = False
        additions = set()
        for word in closure:
            for site in (2, 5):
                if word[site] not in (1, 2):
                    continue
                value = list(word)
                value[site] = 3 - value[site]
                additions.add(tuple(value))
            swapped = list(word)
            swapped[0], swapped[1] = swapped[1], swapped[0]
            additions.add(tuple(swapped))
        old_size = len(closure)
        closure.update(additions)
        changed = len(closure) != old_size
    require(len(closure) == 48 and CAP_WORD not in closure,
            (len(closure), CAP_WORD in closure))
    frozen_coordinates = {
        site: sorted({word[site] for word in closure}) for site in range(8)
    }
    require(frozen_coordinates[0] == frozen_coordinates[1] == [1]
            and frozen_coordinates[3] == [1]
            and frozen_coordinates[6] == frozen_coordinates[7] == [0, 1],
            frozen_coordinates)
    return {
        "response_D4_vertices": 16,
        "response_D4_edges": d4_ledger["occurrence_parameter_D4_edges"],
        "audited_tail_root_sites": roots["tail_sites"],
        "closure_after_D4_tail_roots_endpoint_swap": len(closure),
        "coordinate_colour_sets": {
            str(site): values for site, values in frozen_coordinates.items()
        },
        "cap_word": word_text(CAP_WORD),
        "cap_word_in_exact_existing_closure": False,
        "first_word_separators": [
            "site P remains 1 but cap P is 0",
            "sites 6 and 7 remain binary but cap colours are 2",
        ],
        "scope": (
            "union closure grants every audited D4/tail-root/swap move and "
            "therefore is an upper bound on an actual compatible chain"
        ),
    }


def generous_root_reachability(connected) -> dict[str, object]:
    scope = connected.audit_cartan_scope()
    require("root-word target" in scope["connected_group_positive"]
            and "matching/repeated-edge source grade" in
                scope["what_it_does_not_change"],
            scope)
    differing = tuple(index for index, pair in enumerate(
                      zip(RESPONSE_WORD, CAP_WORD, strict=True))
                      if pair[0] != pair[1])
    path = [RESPONSE_WORD]
    current = list(RESPONSE_WORD)
    for site in differing:
        current[site] = CAP_WORD[site]
        path.append(tuple(current))
    require(differing == (0, 2, 4, 5, 6, 7)
            and len(path) == 7
            and path[-1] == CAP_WORD
            and all(hamming(left, right) == 1 for left, right in
                    zip(path, path[1:])),
            (differing, path))

    start = State(RESPONSE_WORD, RESPONSE_SECTOR)
    target = State(CAP_WORD, CAP_SECTOR)
    no_phi_distance, no_phi_seen = bfs_distance(start, target, False)
    with_phi_distance, with_phi_seen = bfs_distance(start, target, True)
    require(no_phi_distance is None and no_phi_seen == 3 ** 8
            and with_phi_distance == 7
            and with_phi_seen <= 3 ** 8 + 1,
            (no_phi_distance, no_phi_seen, with_phi_distance, with_phi_seen))
    return {
        "grant": "every one-site ternary root on the response object",
        "word_hamming_distance": hamming(RESPONSE_WORD, CAP_WORD),
        "changed_sites": list(differing),
        "one_shortest_word_path": [word_text(word) for word in path],
        "word_only_cap_landing_after_roots": True,
        "root_preserves": scope["what_it_does_not_change"],
        "typed_response_states_reached": no_phi_seen,
        "typed_cap_r0_reached_without_new_edge": False,
        "distance_after_one_new_same-word_operation_edge": with_phi_distance,
        "interpretation": (
            "six roots can repair the word in the strongest granted root "
            "graph, but the landed object is still response-labelled"
        ),
    }


def restriction_projector_and_bar_audit(restriction, projector) \
        -> dict[str, object]:
    restrict = restriction.component_audit(3)
    coefficient = projector.centered_selected_arrow_audit()
    bar = projector.decorated_core_and_bar_audit()
    require(restrict["global_reconstruction"] == "sum_e I_e D_e = 2 id"
            and len(restrict["marked_residual_cuts"]) == 2
            and not coefficient["selected_arrow_in_centered_image"]
            and coefficient["missing_coefficient_line"] ==
                "aggregate sum_i d_i"
            and bar["normalized_bar_constructs_01211222_to_00000000"]
            and not bar["selected_promoted_occurrence_arrow_constructed"],
            (restrict, coefficient, bar))
    return {
        "restriction_insertion": {
            "identity": restrict["global_reconstruction"],
            "marked_lower_centered_cuts":
                len(restrict["marked_residual_cuts"]),
            "operation_effect": (
                "restriction and insertion act in the occurrence/PP object; "
                "they do not create a cap-r0 matrix unit"
            ),
        },
        "occurrence_projector": {
            "centered_rank": coefficient["centered_arrow_rank"],
            "selected_arrow_in_centered_image": False,
            "missing_line": coefficient["missing_coefficient_line"],
        },
        "normalized_covariance_bar": {
            "word_shadow": "01211222 -> 00000000",
            "source_defined": True,
            "selected_occurrence_arrow_constructed": False,
            "reason": bar["reason"],
        },
        "conclusion": (
            "restriction/reinsertion and centered projection can resolve "
            "coefficient occurrence shadows; neither changes the source "
            "operation parent to cap r0"
        ),
    }


def fixed_window_operation_gate(fixed_window) -> dict[str, object]:
    columns, _detector, candidate_h, candidate_r, packet = (
        fixed_window.audit_cartesian_physical_packet()
    )
    switch = fixed_window.audit_operation_switch_boundary(
        columns, candidate_h, candidate_r)
    require(packet["internal_boundary_columns"] == 100
            and packet["internal_rank"] == 46
            and switch["operation_profile_changing_edges"] == 4
            and switch["rank_base_one_switch_candidate"] == [46, 47, 48]
            and switch["rank_base_two_switches_candidate"] == [46, 48, 48],
            (packet, switch))
    return {
        "internal_words": list(fixed_window.WORDS),
        "internal_word_edges": [list(edge) for edge in fixed_window.WORD_EDGES],
        "internal_columns": packet["internal_boundary_columns"],
        "internal_rank": packet["internal_rank"],
        "formal_cross_profile_edges": switch["formal_K2,2_edges"],
        "cross_profile_edges_present_in_internal_constructor": 0,
        "first_new_local_edge": "A_[a|b] -> B (or its endpoint/root mate)",
        "required_face_complete_families":
            switch["projected_missing_row_families"],
        "rank_effect_one_switch_then_candidate":
            switch["rank_base_one_switch_candidate"],
        "rank_effect_two_switches_then_candidate":
            switch["rank_base_two_switches_candidate"],
    }


def terminal_edge_audit(registry, comparison) -> dict[str, object]:
    response_grade = registry.RESPONSE_KS
    target_grade = registry.GAMMA
    landed_response_grade = registry.Grade(
        word="01211222",
        fine="root-transported centered response occurrence / selected PP",
        repeated=response_grade.repeated,
        operation=response_grade.operation,
        window=response_grade.window,
    )
    mismatches = [field for field in
                  ("fine", "repeated", "operation", "window")
                  if getattr(landed_response_grade, field)
                  != getattr(target_grade, field)]
    require(landed_response_grade.word == target_grade.word
            and mismatches == ["fine", "repeated", "operation", "window"],
            (landed_response_grade, target_grade, mismatches))

    comparison_ledger, comparison_digest = comparison.audit()
    require(comparison_digest == comparison.EXPECTED_LEDGER_SHA256,
            "comparison ledger changed")
    hom = comparison_ledger["literal_idempotent_Hom"]
    schema = comparison_ledger["minimal_positive_schema"]
    require(hom["Hom_degree0_response_to_cap_in_current_grammar"] == 0
            and schema["one_new_schema"] ==
                "Phi_KS,r0, natural in the marked one-root object",
            (hom, schema))
    return {
        "source_after_shortest_word_landing": {
            "word": landed_response_grade.word,
            "fine": landed_response_grade.fine,
            "repeated": landed_response_grade.repeated,
            "operation": landed_response_grade.operation,
            "window": landed_response_grade.window,
        },
        "target_cap_r0": {
            "word": target_grade.word,
            "fine": target_grade.fine,
            "repeated": target_grade.repeated,
            "operation": target_grade.operation,
            "window": target_grade.window,
        },
        "same_word": True,
        "remaining_tag_mismatches": mismatches,
        "existing_degree_zero_Hom_dimension": 0,
        "first_new_edge": (
            "Phi_KS,r0: root-transported response occurrence at word "
            "01211222 -> cap r0 at word 01211222"
        ),
        "fixed_window_representative": "A_[a|b] -> B",
        "schema_mates": [
            "A_[a|b]->B", "A_[a|b]->C",
            "A_[b|a]->B", "A_[b|a]->C",
        ],
        "proper_faces": schema["cap_proper_faces"],
        "conditional_kappa_charges_after_edge": [
            entry["lambda_after_schema"]
            for entry in schema["all_eight_instantiation"]
        ],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    registry = load(
        "computations/verify_h3_gamma_star_executable_gen_phys_registry.py",
        "phi_reach_registry",
    )
    cartan = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "phi_reach_cartan",
    )
    response = load(
        "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py",
        "phi_reach_response",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "phi_reach_packaging",
    )
    fixed_window = load(
        "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py",
        "phi_reach_fixed_window",
    )
    restriction = load(
        "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py",
        "phi_reach_restriction",
    )
    projector = load(
        "computations/verify_h3_centered_projector_e14_word_arrow_gate.py",
        "phi_reach_projector",
    )
    connected = load(
        "computations/verify_h3_tau_plus_connected_sl3_label_orbit_obstruction.py",
        "phi_reach_connected",
    )
    comparison = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "phi_reach_comparison",
    )

    ledger = {
        "theorem": "h3 Phi_KS,r0 word-operation reachability no-go",
        "pins": PINS,
        "exact_existing_word_closure": exact_existing_word_closure(
            response, packaging, cartan),
        "maximally_generous_root_closure":
            generous_root_reachability(connected),
        "restriction_projector_bar_routes":
            restriction_projector_and_bar_audit(restriction, projector),
        "fixed_window_operation_gate":
            fixed_window_operation_gate(fixed_window),
        "first_new_edge": terminal_edge_audit(registry, comparison),
        "verdict": (
            "No composition of the implemented restriction/reinsertion, "
            "occurrence projector, root/Weyl, fixed-window PP/Hasse and cap "
            "r0 operations constructs Phi_KS,r0.  The exact D4 plus audited "
            "tail-root closure has 48 words and does not contain the cap "
            "word.  More strongly, granting every one-site ternary root "
            "reaches the cap word in six steps but visits all 3^8 words only "
            "inside the response operation sector.  At the cap word the "
            "fine, repeated, operation and window tags still mismatch.  "
            "Restriction/insertion and centered projectors remain internal, "
            "and the normalized cap-to-zero covariance bar has no selected "
            "occurrence arrow.  The first required new edge is the same-word "
            "operation switch Phi_KS,r0; locally it begins with one DQ-to-PS "
            "K2,2 edge and its four naturality mates."
        ),
        "scope": (
            "exact h=3 reachability for the named implemented operation APIs, "
            "plus a maximally generous all-site root grant; not a global "
            "nonexistence theorem for an unregistered physical constructor"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "words", "operations"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("Phi word-operation reachability ledger changed", digest))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 Phi_KS,r0 reachability ({arguments.mode}): PASS")
        print("exact D4/tail-root word closure: 48; cap word absent")
        print("all-site root grant: word distance 6; typed target unreachable")
        print("first new edge: Phi_KS,r0 (local A_[a|b] -> B plus mates)")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
