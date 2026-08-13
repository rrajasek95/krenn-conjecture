#!/usr/bin/env python3
"""Audit square flatness and first triangle holonomy of endpoint adjacency."""

from __future__ import annotations

from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
WORD = (1, 1, 0, 0, 0, 0)
MARKED = (0, 1, ((2, 3), (4, 5)))
TARGET_BASIS = tuple(product(range(3), repeat=6))
PINS = {
    "computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py":
        "80c9e21304bb679292671c1f344a154d4ae102c1219c4c7e1f3aad9c948be7ac",
    "notes/h3-endpoint-projector-post-bminus4-target-rank-gate.md":
        "62cba9a83f0fba0e74f1274d4dea8968d31bdd45b96cf80b2e862e0107018fab",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py":
        "403819751753802f4bb01b07cca2540fc6abf0479b9be5569ee74f414ea667ad",
    "notes/uniform-physical-bar-occurrence-splitter-cokernel.md":
        "5aecb6fecbb3dffc720efaeb412d366a4c4c7b4475f61535280cc0df4c2b3007",
}
EXPECTED_LEDGER_SHA256 = (
    "f54d250fe9caafe9db445cc6e252341d786e3bddee3e500428b50da460041725"
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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def neighbours(occurrence):
    p_site, s_site, matching = occurrence
    answer = []
    for selected in range(6):
        if selected in (p_site, s_site):
            continue
        mate = next(other for pair in matching if selected in pair
                    for other in pair if other != selected)
        remainder = tuple(pair for pair in matching if selected not in pair)
        answer.append((
            (selected, s_site,
             tuple(sorted(remainder + (edge(p_site, mate),)))),
            (p_site, selected),
        ))
        answer.append((
            (p_site, selected,
             tuple(sorted(remainder + (edge(s_site, mate),)))),
            (s_site, selected),
        ))
    require(len(answer) == len(set(answer)) == 8,
            ("endpoint neighbours changed", occurrence))
    return tuple(answer)


def act_edge(word: tuple[int, ...], move: tuple[int, int]):
    left, right = move
    left_colour, right_colour = WORD[left], WORD[right]
    value = list(word)
    if left_colour != right_colour:
        for site in (left, right):
            if value[site] == left_colour:
                value[site] = right_colour
            elif value[site] == right_colour:
                value[site] = left_colour
    value[left], value[right] = value[right], value[left]
    return tuple(value)


def act_path(word: tuple[int, ...], path):
    return reduce(act_edge, path, word)


def operator_signature(path):
    return tuple(act_path(word, path) for word in TARGET_BASIS)


def target_signature(path):
    return tuple(sorted(act_path((colour,) * 6, path) for colour in range(3)))


def paths(length: int):
    values = ((MARKED, ()),)
    for _ in range(length):
        values = tuple((target, path + (move,))
                       for source, path in values
                       for target, move in neighbours(source))
    return values


def two_step_square_audit() -> dict[str, object]:
    values = paths(2)
    by_target = {}
    for target, path in values:
        by_target.setdefault(target, []).append(path)
    multiplicities = {}
    for packet in by_target.values():
        multiplicities[len(packet)] = multiplicities.get(len(packet), 0) + 1
    operator_counts = {
        target: len({operator_signature(path) for path in packet})
        for target, packet in by_target.items()
    }
    target_counts = {
        target: len({target_signature(path) for path in packet})
        for target, packet in by_target.items()
    }
    require(len(values) == 64 and len(by_target) == 45
            and multiplicities == {8: 1, 2: 12, 1: 32}
            and set(operator_counts.values()) == {1}
            and set(target_counts.values()) == {1},
            ("the two-step endpoint path census changed", multiplicities))

    # First literal diamond: move the p endpoint 0->2 and the s endpoint
    # 1->3.  The moves are disjoint, so the full site/Weyl maps commute, not
    # merely their images of Delta.
    first = ((0, 2), (1, 3))
    second = ((1, 3), (0, 2))
    destination = (2, 3, ((0, 1), (4, 5)))
    require(any(target == destination and path == first for target, path in values)
            and any(target == destination and path == second
                    for target, path in values)
            and operator_signature(first) == operator_signature(second),
            "the first endpoint square stopped commuting")
    return {
        "length_two_paths": len(values),
        "destinations": len(by_target),
        "destination_path_multiplicities": {
            str(key): value for key, value in sorted(multiplicities.items())
        },
        "commuting_two_path_diamonds": 12,
        "backtrack_paths_at_marked_vertex": 8,
        "full_operator_classes_per_destination": 1,
        "target_Delta_classes_per_destination": 1,
        "first_square": {
            "destination": repr(destination),
            "path_one": [list(move) for move in first],
            "path_two": [list(move) for move in second],
            "full_site_Weyl_commutator": 0,
            "target_curvature_after_common_cone": 0,
        },
        "verdict": (
            "every two-step diamond and backtrack is flat as a full target "
            "operator; the independent B-2 PP packet is a product-rule "
            "face, not square curvature"
        ),
    }


def swap_sites(word, left: int, right: int):
    value = list(word)
    value[left], value[right] = value[right], value[left]
    return tuple(value)


def three_step_holonomy_audit() -> dict[str, object]:
    values = paths(3)
    by_target = {}
    for target, path in values:
        by_target.setdefault(target, []).append(path)
    path_multiplicities = {}
    operator_class_counts = {}
    target_class_counts = {}
    for packet in by_target.values():
        path_multiplicities[len(packet)] = (
            path_multiplicities.get(len(packet), 0) + 1
        )
        count = len({operator_signature(path) for path in packet})
        operator_class_counts[count] = operator_class_counts.get(count, 0) + 1
        count = len({target_signature(path) for path in packet})
        target_class_counts[count] = target_class_counts.get(count, 0) + 1
    require(len(values) == 512 and len(by_target) == 88
            and path_multiplicities == {8: 4, 4: 36, 6: 24, 3: 16, 18: 8}
            and operator_class_counts == {2: 27, 1: 45, 3: 16}
            and target_class_counts == {1: 88},
            ("the three-step holonomy census changed", path_multiplicities,
             operator_class_counts, target_class_counts))

    triangle_23 = ((0, 2), (2, 3), (3, 0))
    triangle_45 = ((0, 4), (4, 5), (5, 0))
    require(any(target == MARKED and path == triangle_23
                for target, path in values)
            and any(target == MARKED and path == triangle_45
                    for target, path in values),
            "the two marked endpoint triangles disappeared")
    require(all(act_path(word, triangle_23) == swap_sites(word, 2, 3)
                and act_path(word, triangle_45) == swap_sites(word, 4, 5)
                for word in TARGET_BASIS),
            "the first endpoint triangle holonomies changed")

    delta_words = tuple((colour,) * 6 for colour in range(3))
    require(all(act_path(word, triangle_23) == word
                and act_path(word, triangle_45) == word
                for word in delta_words),
            "a residual edge flip stopped fixing Delta")
    witness_23 = (0, 0, 1, 0, 0, 0)
    witness_45 = (0, 0, 0, 0, 0, 1)
    require(act_path(witness_23, triangle_23)
                == (0, 0, 0, 1, 0, 0)
            and act_path(witness_45, triangle_45)
                == (0, 0, 0, 0, 1, 0),
            "the primitive mixed-word holonomy witnesses changed")
    return {
        "length_three_paths": len(values),
        "destinations": len(by_target),
        "destination_path_multiplicities": {
            str(key): value for key, value in sorted(path_multiplicities.items())
        },
        "operator_class_count_histogram": {
            str(key): value for key, value in sorted(operator_class_counts.items())
        },
        "destinations_with_nontrivial_operator_holonomy": 43,
        "target_Delta_class_count_histogram": {"1": 88},
        "marked_triangle_23": {
            "path": [list(move) for move in triangle_23],
            "returns_to_marked_occurrence": True,
            "composite_operator": "site transposition (2 3)",
            "on_GHZ_Delta": "identity",
            "mixed_word_witness": "X_001000 -> X_000100",
            "primitive_holonomy_face": "X_000100-X_001000",
        },
        "marked_triangle_45": {
            "path": [list(move) for move in triangle_45],
            "returns_to_marked_occurrence": True,
            "composite_operator": "site transposition (4 5)",
            "on_GHZ_Delta": "identity",
            "mixed_word_witness": "X_000001 -> X_000010",
            "primitive_holonomy_face": "X_000010-X_000001",
        },
        "classification": (
            "target-normal curvature is zero, but the quotient occurrence "
            "graph has nontrivial residual-edge-flip isotropy holonomy"
        ),
    }


def source_provenance_and_frontier_audit() -> dict[str, object]:
    sequential = load(
        "computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py",
        "endpoint_holonomy_sequential",
    )
    ledger, digest = sequential.audit()
    require(digest == sequential.EXPECTED_LEDGER_SHA256,
            "the sequential endpoint ledger changed")
    target = ledger["sequential_target"]
    private = ledger["sequential_private_and_protected"]
    require(target["sequential_target_ranks"] == [1, 1, 1]
            and private["stage_input_sequential_ranks"] == [1, 2, 3],
            "the target/private rank split changed")
    return {
        "common_target_line": True,
        "target_ratios": target["target_ratios_to_Bminus4"],
        "private_stage_ranks": private["stage_input_sequential_ranks"],
        "two_step_private_rank_is_curvature": False,
        "three_step_first_new_datum": (
            "residual-edge stabilizer bar/2-simplex based at the pointed "
            "occurrence section"
        ),
        "formal_action_groupoid_nerve": (
            "flat after retaining isotropy arrows (2 3) and (4 5); the "
            "triangle composites are those arrows, not the identity"
        ),
        "trivial_occurrence_local_system": False,
        "physical_site_permutation_status": (
            "the residual edge flips are target-safe physical site "
            "permutations, but a bar based at a selected occurrence requires "
            "the same occurrence-local source section that is currently open"
        ),
        "complete_row_bar_suffices": False,
        "reason": (
            "a complete response row is invariant under the residual flip; "
            "its bar has trivial occurrence-centered projection"
        ),
        "shortest_extension": (
            "require the B-4/AugP2 section to be equivariant over the full "
            "endpoint action groupoid, including residual-edge isotropy bars "
            "and their triangle 2-simplices.  Then reuse one C2+ target cone; "
            "B-2, B+2, and matching PP packets remain typed proper faces."
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 endpoint correspondence square/triangle holonomy gate",
        "pins": PINS,
        "two_step_square": two_step_square_audit(),
        "three_step_holonomy": three_step_holonomy_audit(),
        "source_provenance_and_frontier": source_provenance_and_frontier_audit(),
        "verdict": (
            "The endpoint correspondence is exactly flat through every "
            "two-step diamond as a full site/Weyl operator, so rank-two "
            "private PP data are not square curvature.  At three steps the "
            "quotient occurrence graph develops target-dark stabilizer "
            "holonomy: the first marked triangles compose to residual-edge "
            "flips (2 3) and (4 5), not identity.  Hence B has a flat action-"
            "groupoid nerve only when those isotropy arrows and 2-simplices "
            "are retained.  Their physical target is harmless, but their "
            "occurrence-local source bars are not supplied by complete rows."
        ),
        "scope": (
            "exact h=3 path census and full 3^6 target-operator audit through "
            "length three; no occurrence-local physical isotropy bar or "
            "higher endpoint totalization is constructed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256, ("ledger", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("all two-step endpoint diamonds: FULL-OPERATOR FLAT")
    print("three-step target Delta holonomy: ZERO")
    print("three-step full-operator holonomy destinations:",
          ledger["three_step_holonomy"][
              "destinations_with_nontrivial_operator_holonomy"])
    print("first triangle holonomies: residual flips (2 3), (4 5)")
    print("flat endpoint nerve: YES WITH ISOTROPY; NO AS TRIVIAL LOCAL SYSTEM")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
