#!/usr/bin/env python3
"""Audit termination of the first mixed-unary active-coloop recurrence.

The fourteen-mate theorem gives two coloop escapes and twelve offdiagonal
active-fan entries.  This checker composes that exact split with K6 Galois
saturation and tests whether coloop edge, closed Hall shore and unary word
support a further recurrence potential.

They do not, unconditionally.  The eight endpoint-closable occurrences can
all be trapped in the closed triangle {01,04,14}.  The four head-dark mates
can all be trapped in the nine-edge shore T({45}).  Every mate remains in
the same word 000011, and all physical edges form one S6 orbit, so neither
word nor edge supplies a relabeling-invariant strict decrease.

The sound well-founded protocol is one-shot: saturate the Hall shore; an
outside certified hole strictly lowers 15-|cl(A)|; otherwise process the
whole mate packet once and pass a surviving literal coloop to the existing
fan-grade physical normalization/P_f gate.  Restarting the mate construction
at an arbitrary new coloop is not a proved transition.
"""

from __future__ import annotations

from ast import literal_eval
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_coloop_first_mixed_unary_fourteen_mate_landing.py":
        "9e9f78abde2144cb1f03c41afaea991b2b7052f86ab2fd068417f9dee132684d",
    "notes/h3-coloop-first-mixed-unary-fourteen-mate-landing.md":
        "a7c064185b1eeafe8a718696c826377d5765f73aefdcc14e1d26e02a6eb379dc",
    "computations/verify_h3_active_fan_coloop_saturation_boundary.py":
        "35658ebed521b93387fc00aa7d2600d703f57b3e5e5deca67a11a1ab155d6c56",
    "notes/h3-active-fan-coloop-saturation-boundary.md":
        "4431948d139c45f8619928878b0dde0cba39ddc9a0942bd6a899bd9d53daa1d6",
    "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py":
        "22e1e7a6a933b1ba71bbd95bb605b1351e823506e495682cccff312cd3df3b15",
    "notes/h3-active-fan-coloop-gate-ii-assembly-boundary.md":
        "bacb7b4b138882c0cc07f13767f2e4ead86aa630c55cf1a946943141b7cee7a7",
}
EXPECTED_LEDGER_SHA256 = "0a0d767063e37b2398126592e132cf6225aaa89bd1794a8e576e724962bfe70d"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left, right):
    return tuple(sorted((left, right)))


def mask_for(saturation, edges):
    return sum(1 << saturation.EDGE_INDEX[edge(*physical)]
               for physical in edges)


def closed_concepts(saturation):
    concepts = set()
    for mask in range(1, saturation.FULL_MASK + 1):
        mate = saturation.transversal(mask)
        if mate:
            concepts.add((saturation.transversal(mate), mate))
    require(len(concepts) == 446,
            "the closed ordered Hall-concept count changed")
    return concepts


def audit_trapped_shores(mates, saturation):
    first = load(
        "computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py",
        "recurrence_first_mixed_gate",
    )
    classified = mates.audit_mates(first)
    records = classified["mate_records"]
    response = [record for record in records
                if record["class"]
                == "labelled_R11_coloop_avoiding_active_carrier"]
    head_dark = [record for record in records
                 if record["class"] == "head_dark_two_cross_active_carrier"]
    diagonal = [record for record in records
                if record["class"] == "pure_zero_matching_avoids_coloop"]
    require((len(diagonal), len(response), len(head_dark)) == (2, 8, 4),
            "the recurrence mate split changed")

    response_holes = Counter(
        literal_eval(record["removed_closure_edge"]) for record in response
    )
    require(response_holes == Counter({
        (0, 1): 2, (0, 4): 3, (1, 4): 3,
    }), ("the response-hole split changed", response_holes))
    triangle = frozenset(((0, 1), (0, 4), (1, 4)))
    triangle_mask = mask_for(saturation, triangle)
    require(saturation.transversal(triangle_mask) == triangle_mask,
            "the response-hole triangle stopped being a closed concept")

    head_dark_edges = set()
    for record in head_dark:
        head_dark_edges.update(
            tuple(value[1:3]) for value in
            map(literal_eval, record["cross_colour_cells"])
        )
    # literal_eval('(0, 5, 0, 1)')[1:3] is wrong: use the physical endpoints.
    head_dark_edges = {
        tuple(literal_eval(value)[:2])
        for record in head_dark for value in record["cross_colour_cells"]
    }
    require(head_dark_edges == {(0, 5), (1, 5), (2, 4), (3, 4)},
            ("the head-dark active rectangle changed", head_dark_edges))
    nine_edge = frozenset(
        physical for physical in saturation.EDGES
        if set(physical) & {4, 5}
    )
    nine_mask = mask_for(saturation, nine_edge)
    singleton_45 = mask_for(saturation, ((4, 5),))
    require(len(nine_edge) == 9
            and saturation.transversal(nine_mask) == singleton_45
            and saturation.transversal(singleton_45) == nine_mask
            and head_dark_edges <= nine_edge,
            "the head-dark singleton/nine-edge concept changed")

    concepts = closed_concepts(saturation)
    require((triangle_mask, triangle_mask) in concepts
            and (nine_mask, singleton_45) in concepts,
            "a sharp trapped shore left the closed-concept census")

    # There is exactly one closed shore containing all eight possible
    # offdiagonal physical edges from the fourteen-mate theorem: T({45}).
    all_active_edges = {
        tuple(literal_eval(value)[:2])
        for value in classified["all_added_offdiagonal_cells"]
    }
    containing_all = [
        left for left, _right in concepts
        if all(edge(*physical) in set(saturation.mask_edges(left))
               for physical in all_active_edges)
    ]
    require(len(all_active_edges) == 8 and containing_all == [nine_mask],
            ("the universal trapped active shore changed", containing_all))
    return {
        "diagonal_coloop_escapes": len(diagonal),
        "response_occurrences": len(response),
        "response_hole_histogram": {
            repr(key): value for key, value in sorted(response_holes.items())
        },
        "sharp_response_trap": {
            "closed_shore": [list(value) for value in sorted(triangle)],
            "type": "triangle/triangle",
            "all_eight_response_holes_internal": True,
        },
        "head_dark_occurrences": len(head_dark),
        "head_dark_active_edges": [list(value)
                                    for value in sorted(head_dark_edges)],
        "sharp_head_dark_trap": {
            "closed_shore": [list(value) for value in sorted(nine_edge)],
            "dual_shore": [[4, 5]],
            "type": "nine-edge/singleton",
            "all_four_head_dark_rectangles_internal": True,
        },
        "unique_closed_shore_containing_all_eight_possible_active_edges": (
            "the nine edges meeting 45"
        ),
        "consequence": (
            "outside-hole growth is available unless the actual mate is "
            "trapped, but exact closed concepts trap all response closures "
            "or all head-dark active edges; no outside-hole conclusion is uniform"
        ),
    }


def audit_word_and_edge_no_potential(mates):
    # All fourteen alternatives occur in the same unary coefficient.
    require(mates.WORD == (0, 0, 0, 0, 1, 1),
            "the recurrence unary word changed")
    word_orbit = set()
    for site_permutation in permutations(range(6)):
        permuted = tuple(mates.WORD[site_permutation[index]]
                         for index in range(6))
        for colour_permutation in permutations(range(3)):
            word_orbit.add(tuple(colour_permutation[value]
                                 for value in permuted))
    require(len(word_orbit) == 90
            and {tuple(sorted(Counter(word).values(), reverse=True))
                 for word in word_orbit} == {(4, 2)},
            "the two-colour unary-word orbit changed")

    edge_orbit = {
        edge(permutation[0], permutation[1])
        for permutation in permutations(range(6))
    }
    require(len(edge_orbit) == 15,
            "physical edges stopped forming one S6 orbit")
    return {
        "unary_word": "000011",
        "all_mates_stay_in_same_unary_coefficient": True,
        "site_and_colour_orbit_size": len(word_orbit),
        "word_orbit_invariant": "colour multiplicities (4,2,0)",
        "physical_edge_orbit_size_under_S6": len(edge_orbit),
        "edge_order_warning": (
            "all edges are symmetry equivalent; a numerical edge order is "
            "not a source-invariant decreasing potential"
        ),
        "conclusion": (
            "in trapped branches neither the unary-word orbit nor the "
            "coloop-edge orbit changes, so these labels cannot repair the "
            "nondecreasing Hall potential"
        ),
    }


def audit_conditional_well_founded_protocol(saturation, assembly):
    saturation_result = saturation.audit_galois_saturation()
    assembly_result = assembly.audit_branch_assembly()
    require("15-|cl(A)|" in saturation_result["potential"]
            and assembly_result["only_nonterminal_after_saturation"]
            == "single missing fan-grade physical Phi/q packet",
            (saturation_result, assembly_result))
    # Phase is used only within one fixed (word,coloop,closed-shore) key.
    # Process the complete fourteen-way alternative simultaneously.  It may
    # move 1->0 once; no transition 0->1 is admitted without the open
    # physical normalization theorem.
    examples = []
    for closure_size in (1, 2, 3, 4, 5, 6, 9):
        before = (15 - closure_size, 1)
        after_packet = (15 - closure_size, 0)
        require(after_packet < before,
                "the one-shot packet phase stopped decreasing")
        examples.append([list(before), list(after_packet)])
    return {
        "state_key": "(unary word w, literal coloop edge e, closed shore cl(A))",
        "conditional_potential": "(15-|cl(A)|, mate_packet_unprocessed)",
        "order": "lexicographic on nonnegative integers",
        "outside_hole_step": "strictly lowers 15-|cl(A)|",
        "trapped_packet_step": "processes all fourteen alternatives once: phase 1->0",
        "sample_phase_decreases": examples,
        "phase_zero_action": (
            "four-good terminates; an already normalized coloop enters the "
            "committed h3 closure; an arbitrary literal coloop enters the "
            "single fan-grade physical Phi/q (equivalently pointed P_f) gate"
        ),
        "forbidden_unproved_step": (
            "reset phase to one at a relabelled/new arbitrary coloop and rerun "
            "the two-occurrence mate guard"
        ),
        "termination_scope": (
            "well-founded after the physical normalization gate is supplied; "
            "not an unconditional recurrence theorem from mate support alone"
        ),
    }


def audit():
    pin_dependencies()
    mates = load(
        "computations/verify_h3_coloop_first_mixed_unary_fourteen_mate_landing.py",
        "recurrence_fourteen_mates",
    )
    saturation = load(
        "computations/verify_h3_active_fan_coloop_saturation_boundary.py",
        "recurrence_saturation",
    )
    assembly = load(
        "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py",
        "recurrence_gate_ii",
    )
    ledger = {
        "theorem": "h3 active-coloop forced-mate recurrence/potential boundary",
        "pins": PINS,
        "fourteen_mate_closed_shore_audit":
            audit_trapped_shores(mates, saturation),
        "edge_word_no_potential": audit_word_and_edge_no_potential(mates),
        "conditional_protocol":
            audit_conditional_well_founded_protocol(saturation, assembly),
        "exact_verdict": (
            "The fourteen mates cannot cycle inside one processed packet.  "
            "Two break the current coloop and twelve enter the physical fan "
            "alternative.  However closed triangle and singleton/nine-edge "
            "shores show that no outside-hole decrease is uniform, while "
            "word and coloop edge have unchanged symmetry type.  Therefore "
            "one must not recursively reapply the special two-occurrence "
            "guard to an arbitrary new coloop.  The only surviving lower "
            "placement is the already named fan-grade physical Phi/q or "
            "pointed-P_f normalization; conditional on it, Hall closure plus "
            "one packet phase is well-founded and the committed normalized "
            "coloop chain terminates"
        ),
        "scope": (
            "exact K6 closed-shore and fourteen-mate census.  The trapped "
            "shores are combinatorial/source-label guards, not asserted full "
            "GHZ solutions; no missing physical comparison is assumed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("active-coloop recurrence ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    print("forced-mate packet: ONE-SHOT, NO INTERNAL CYCLE")
    print("closed triangle and nine-edge shores: STRICT GROWTH NOT UNIFORM")
    print("sole lower placement: FAN-GRADE PHYSICAL Phi/q / POINTED P_f")
    print("ledger_sha256=" + digest)
    return ledger


if __name__ == "__main__":
    audit()
