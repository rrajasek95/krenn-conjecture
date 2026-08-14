#!/usr/bin/env python3
"""Audit selected db01 against the active pure-colour coloop chart.

In the coefficient/Kahler shadow, q*H=1 gives

    db01 = p0*s1*dH = -p0*s1*H/q*dq01.

This checker retains the physical top and removed-edge labels.  The
physical product which could change the pure-coloop operation into the
selected endpoint operation has top p0*s1*q01*H.  It is a double-collision
P4+2K2 top, not the squarefree response top.  Its tail faces are P4+K2 and
its dq01 faces are 4K2.  Neither family occurs in the complete first-PP
fan exits, whose cofactors are only 3K2 and P3+K2.

The final rank guard is deliberately generous: it grants a termwise monic
reinsertion graph for all 180 tail flags in all thirty ordered endpoint
fibres, as well as both complete source and target rows.  The centered
selected-six dual still survives.  Localization rescales columns but does
not create the missing absolute selected-fibre or double-collision descent
column.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_three_cap_mixed_koszul_colon_gate.py":
        "6d1d90407fe095025525c94957b1d23b59ebf364ea21aebd5561aa9bfe47df55",
    "notes/h3-active-coloop-three-cap-mixed-koszul-colon-gate.md":
        "33b43045ec877e49febe0e856dfec504d666f517639dd564f7ac9de3614a42b1",
    "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py":
        "c0c6c075388a2eb2d5dad6d133166a3f211dd268183d3e2a5433d922e2ea8ceb",
    "notes/h3-hyperbolic-root-collision-tate-cobar-totalization-gate.md":
        "673722b62a59f10b00aa20796236146df052a4d45eda0764053737bca401e95a",
    "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py":
        "620b3e54e8e6ee09a0b616d0259c8d109b0359645b20d35db5fb876c8e7e0311",
    "notes/h3-selected-db01-normalized-gl3-bar-companion-gate.md":
        "46aa4e74c52160cfaa74089727defb1a0d6c4d0051130374ec12dcc887de09de",
    "computations/verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py":
        "9b9c05a6789d2ade9359934f279eeb429591b2e85651ebaba8485195050417eb",
    "notes/h3-gate-ii-uniform-response-relative-carrier-landing-gate.md":
        "e1d0b1185cd72ff4d0d915abb1db25835f2848f65f1509458aee9f2325699084",
}
EXPECTED_LEDGER_SHA256 = "39ddf6b23e9ffd12e0f4084d3c23f9684bd635263ed88e19291fea1fe27576a3"

P, S, ZERO, ONE, TWO, THREE, FOUR, FIVE = range(8)
NAMES = ("P", "S", "0", "1", "2", "3", "4", "5")
Edge = tuple[int, int]
Monomial = tuple[Edge, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def edge(left: int, right: int) -> Edge:
    require(left != right, "loop edge")
    return (left, right) if left < right else (right, left)


def label_edge(value: Edge) -> str:
    left, right = (NAMES[value[0]], NAMES[value[1]])
    if (left, right) == ("P", "S"):
        return "D"
    if left == "P":
        return "p" + right
    if left == "S":
        return "s" + right
    return "q" + left + right


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


P0 = edge(P, ZERO)
S1 = edge(S, ONE)
Q01 = edge(ZERO, ONE)
TAILS = tuple(perfect_matchings((TWO, THREE, FOUR, FIVE)))


def site_profile(monomial: Monomial) -> tuple[int, ...]:
    profile = [0] * 8
    for left, right in monomial:
        profile[left] += 1
        profile[right] += 1
    return tuple(profile)


def component_type(monomial: Monomial) -> str:
    adjacency = {site: set() for site in range(8)}
    for left, right in monomial:
        adjacency[left].add(right)
        adjacency[right].add(left)
    components = []
    unseen = {site for site in range(8) if adjacency[site]}
    while unseen:
        seed = min(unseen)
        stack = [seed]
        vertices = set()
        while stack:
            current = stack.pop()
            if current in vertices:
                continue
            vertices.add(current)
            stack.extend(adjacency[current] - vertices)
        unseen -= vertices
        edge_count = sum(len(adjacency[site]) for site in vertices) // 2
        degrees = sorted((len(adjacency[site]) for site in vertices),
                         reverse=True)
        require(edge_count == len(vertices) - 1 and max(degrees) <= 2,
                ("non-path component", monomial, vertices, degrees))
        components.append((len(vertices), min(vertices)))
    counts = Counter(size for size, _seed in components)
    labels = []
    for size in sorted(counts, reverse=True):
        name = "K2" if size == 2 else f"P{size}"
        multiplicity = counts[size]
        labels.append((str(multiplicity) if multiplicity > 1 else "") + name)
    return "+".join(labels)


def coefficient_kahler_shadow_audit() -> dict[str, object]:
    # Basis order (dq,dH).  At q=2,H=1/2,p0*s1=3, the conormal relation is
    # H*dq+q*dH=0.  The displayed difference is an exact multiple of it.
    q, h, ps = Q(2), Q(1, 2), Q(3)
    relation = (h, q)
    db = (Q(0), ps)
    reduced = (-ps * h / q, Q(0))
    multiplier = ps / q
    difference = tuple(left - right for left, right in
                       zip(db, reduced, strict=True))
    require(q * h == 1
            and difference == tuple(multiplier * value for value in relation),
            ("localized Kahler identity changed", relation, db, reduced))
    return {
        "active_relation": "q01*H2345=1",
        "conormal_relation": "H2345*dq01+q01*dH2345=0",
        "selected_face": "db01=p0*s1*dH2345",
        "localized_identity": "db01=-p0*s1*H2345/q01*dq01=-p0*s1*H2345^2*dq01",
        "sample_q_H_ps": [str(q), str(h), str(ps)],
        "identity_holds_in_unlabelled_Omega1": True,
        "physical_source_column_constructed_by_identity": False,
    }


def literal_face_inventory_audit() -> dict[str, object]:
    require(len(TAILS) == 3, "K4 tail count")
    selected_tops = tuple(tuple(sorted((P0, S1) + tail)) for tail in TAILS)
    selected_flags = tuple(
        (top, removed, tuple(item for item in top if item != removed))
        for top, tail in zip(selected_tops, TAILS, strict=True)
        for removed in tail
    )
    require(len(selected_flags) == len(set(selected_flags)) == 6
            and {site_profile(top) for top in selected_tops} == {(1,) * 8}
            and {component_type(cofactor)
                 for _top, _removed, cofactor in selected_flags} == {"3K2"},
            "selected db01 labels changed")

    coloop_tops = tuple(tuple(sorted((Q01,) + tail)) for tail in TAILS)
    coloop_tail_flags = tuple(
        (top, removed, tuple(item for item in top if item != removed))
        for top, tail in zip(coloop_tops, TAILS, strict=True)
        for removed in tail
    )
    coloop_dq_flags = tuple(
        (top, Q01, tuple(item for item in top if item != Q01))
        for top in coloop_tops
    )
    require(len(coloop_tail_flags) == 6 and len(coloop_dq_flags) == 3,
            "coloop PP census changed")

    double_tops = tuple(tuple(sorted((P0, S1, Q01) + tail))
                        for tail in TAILS)
    require({component_type(top) for top in double_tops} == {"P4+2K2"}
            and {site_profile(top) for top in double_tops}
                == {(1, 1, 2, 2, 1, 1, 1, 1)},
            "double-collision top changed")

    face_families: dict[str, list[tuple[Monomial, Edge, Monomial]]] = {
        "endpoint_dp_ds": [], "tail_q_db01": [], "dq01_companion": [],
    }
    for top, tail in zip(double_tops, TAILS, strict=True):
        for removed in top:
            cofactor = tuple(item for item in top if item != removed)
            if removed in (P0, S1):
                face_families["endpoint_dp_ds"].append((top, removed, cofactor))
            elif removed == Q01:
                face_families["dq01_companion"].append((top, removed, cofactor))
            else:
                require(removed in tail, ("unclassified edge", removed))
                face_families["tail_q_db01"].append((top, removed, cofactor))
    counts = {key: len(value) for key, value in face_families.items()}
    types = {key: sorted(set(component_type(record[2]) for record in value))
             for key, value in face_families.items()}
    require(counts == {"endpoint_dp_ds": 6, "tail_q_db01": 6,
                       "dq01_companion": 3}
            and types == {"endpoint_dp_ds": ["P3+2K2"],
                          "tail_q_db01": ["P4+K2"],
                          "dq01_companion": ["4K2"]},
            (counts, types))

    return {
        "selected_response": {
            "word_head": "11:110000",
            "top": "p0*s1*H2345, squarefree 4K2",
            "term_count": len(selected_flags),
            "PP_cofactor_type": "3K2",
            "removed_edges": ["dq23", "dq45", "dq24", "dq35",
                              "dq25", "dq34"],
        },
        "pure_coloop_PP": {
            "top": "q01*H2345, squarefree 3K2 on residual six sites",
            "tail_flags": len(coloop_tail_flags),
            "dq01_flags": len(coloop_dq_flags),
        },
        "physical_endpoint_insertion": {
            "top": "p0*s1*q01*H2345",
            "top_type": "P4+2K2",
            "repeated_sites": [0, 1],
            "face_counts": counts,
            "face_types": types,
            "exact_existing_selected_exit": (
                "the ds1 face p0*q01*H2345 is the reverse-root collision top"
            ),
            "strong_grant_used_below": "all six dp0/ds1 faces may exit",
        },
    }


def existing_fan_exit_audit() -> dict[str, object]:
    hyperbolic = load(
        "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py",
        "selected_db01_active_coloop_hyperbolic",
    )
    ledger, digest = hyperbolic.audit()
    require(digest == hyperbolic.EXPECTED_LEDGER_SHA256,
            "the hyperbolic collision ledger changed")
    pp = ledger["complete_and_selected_PP_boundaries"]
    require(pp["complete_type_counts"] == {"3K2": 360, "P3+K2": 360}
            and pp["selected_type_counts"] == {"3K2": 24,
                                                "P3+K2": 24},
            "the complete collision fan types changed")
    new_types = {"P4+K2", "4K2"}
    old_types = set(pp["complete_type_counts"])
    require(new_types.isdisjoint(old_types),
            "a new double-collision face entered the old PP fan")
    return {
        "existing_complete_collision_PP_flags": pp["complete_labelled_PP_flags"],
        "existing_PP_cofactor_types": sorted(old_types),
        "new_unrouted_cofactor_types": sorted(new_types),
        "topology_intersection": [],
        "even_after_granting_all_endpoint_dp_ds_exits": (
            "six q01*db01 P4+K2 faces and three p0*s1*H*dq01 4K2 faces remain"
        ),
        "first_missing_operation": (
            "a localized PS insertion/descent over the q01 coloop, with "
            "P4+2K2 top and its P4+K2/4K2 PP faces"
        ),
    }


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        pivot_value = rows[answer][column]
        rows[answer] = [value / pivot_value for value in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [left - multiple * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def maximal_termwise_counterguard_audit() -> dict[str, object]:
    # Thirty ordered endpoint fibres, three K4 tails and two tail deletions.
    # There are 180 response flags and a deliberately granted target/carrier
    # copy of each one.  All 180 monic graphs are supplied.  Only the two
    # complete rows are absolute.
    endpoint_fibres, flags_per_fibre = 30, 6
    block = endpoint_fibres * flags_per_fibre
    width = 2 * block

    def unit(position: int) -> tuple[Q, ...]:
        return tuple(Q(index == position) for index in range(width))

    response_complete = tuple(Q(index < block) for index in range(width))
    target_complete = tuple(Q(index >= block) for index in range(width))
    graphs = tuple(
        tuple(target - source for target, source in zip(
            unit(block + index), unit(index), strict=True
        ))
        for index in range(block)
    )
    old = graphs + (response_complete, target_complete)
    selected = tuple(Q(index < flags_per_fibre) for index in range(width))
    centered_weights = tuple(
        Q(29 if (index % block) < flags_per_fibre else -1)
        for index in range(width)
    )
    old_rank = rank(old)
    new_rank = rank(old + (selected,))
    require(old_rank == block + 1 and new_rank == block + 2
            and all(dot(centered_weights, column) == 0 for column in old)
            and dot(centered_weights, selected) == Q(174),
            ("maximal termwise counterguard changed", old_rank, new_rank))

    # A common localization unit only rescales columns.  It cannot change
    # their span or the operation-block decomposition.
    rescaled = tuple(tuple(Q(2) * value for value in column)
                     for column in old)
    require(rank(rescaled) == old_rank
            and rank(rescaled + (selected,)) == new_rank,
            "unit localization changed the selected rank")
    return {
        "ordered_endpoint_fibres": endpoint_fibres,
        "tail_PP_flags_per_fibre": flags_per_fibre,
        "response_flags": block,
        "granted_target_carrier_flags": block,
        "granted_monic_termwise_reinsertion_graphs": block,
        "absolute_rows": ["complete response PP", "complete target PP"],
        "rank_before_after_selected_db01": [old_rank, new_rank],
        "primitive_centered_dual": {
            "weight_on_selected_six_in_both_blocks": 29,
            "weight_on_each_other_flag_in_both_blocks": -1,
            "on_every_graph_and_complete_row": 0,
            "on_selected_db01": 174,
        },
        "common_unit_rescaling_changes_rank": False,
        "interpretation": (
            "termwise reinsertion identifies relative flags, but with only "
            "complete absolute rows it retains the endpoint-centered class"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 selected db01 active-coloop localized reinsertion gate",
        "pins": PINS,
        "localized_coefficient_shadow": coefficient_kahler_shadow_audit(),
        "literal_PP_and_reinsertion_faces": literal_face_inventory_audit(),
        "existing_fan_exit_comparison": existing_fan_exit_audit(),
        "maximal_termwise_full_label_counterguard":
            maximal_termwise_counterguard_audit(),
        "verdict": (
            "On q01*H2345=1 the unlabelled Kahler identity expresses db01 "
            "as -p0*s1*H2345^2*dq01.  It is not a source-valid expression "
            "in the fixed physical presentation.  Treating the Laurent "
            "factors as scalars leaves the pure-coloop operation idempotent; "
            "treating them as physical insertions produces the double-"
            "collision top p0*s1*q01*H2345.  After granting every endpoint "
            "dp/ds fan exit, its six P4+K2 q01*db01 faces and three 4K2 "
            "dq01 companions have no existing collision-PP landing.  Even "
            "a maximal termwise relative reinsertion grant plus both complete "
            "rows leaves the centered selected-six dual."
        ),
        "shortest_positive_datum": (
            "one source-labelled localized PS-over-q01 restriction/insertion "
            "column whose absolute endpoint is the selected six-term db01 "
            "packet and whose P4+K2/4K2 double-collision companions land in "
            "physical fan rows without killing the classical fibre"
        ),
        "scope": (
            "exact h=3 fixed-window theorem before every cap/K_Eq row; it "
            "proves nonimplication from the active coloop, complete response/"
            "target rows, the committed collision fan, and arbitrary monic "
            "termwise relative reinsertion graphs.  It does not rule out a "
            "new double-collision descent cell"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return ledger, sha256(payload.encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("shadow", "fan", "counterguard"),
                        default="counterguard")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("selected db01 active-coloop ledger changed", digest))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
        return
    print(f"h3 selected db01 active-coloop gate ({arguments.mode}): PASS")
    print("unlabelled localized Kahler identity: EXACT")
    print("source-valid selected db01 combination: NOT CONSTRUCTED")
    print("first product top: P4+2K2; live PP faces: 6 P4+K2 + 3 4K2")
    print("maximal termwise graph rank: 181 -> 182 after db01")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
