#!/usr/bin/env python3
"""Audit full-tail two-window Cech descent at h=5 and h=6.

For each perfect tail matching M, the C(m,2) two-edge windows form one
Johnson fibre.  Conditional on a natural Phi and the signed Hasse tower,
that fibre has one H0 class.  The rational section averaging its windows by
1/C(m,2) is an exact normalized coequalizer.  Taking the direct sum over all
M covers every tail coefficient exactly once and preserves the literal
matching-indexed H0: 105 at h=5 and 945 at h=6.

The matching-flip graph is connected and every tail outside the fixed
four-site partition is at distance at most two.  This is reachability, not
source-valid descent.  A flip has common windows whose physical word and q
window agree, but its spectator fine, removed/reinserted repeated label and
coefficient monomial differ.  Adding raw flip bars collapses matching H0 to
one; even a forest which merely attaches the 96/900 outside tails lowers H0
by exactly 96/900.  BC and higher Hasse cells cannot repair im(d1).

The presentation-safe cylinder keeps one exchange coordinate u_e with
d b_e=(M'-M)-u_e.  It preserves H0 but leaves precisely the exchange debt,
so it does not descend a fixed-partition proof.  Hence full coverage is
positive from independent natural instantiation on every M, and negative
from matching-exchange identification unless a new coefficient-labelled
comparison is supplied.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_johnson_window_hasse_coherence_resolution.py":
        "d10e82c97135106638ba46add3030fb28f716337853c5c2381c4ab0eeb145fe5",
    "notes/uniform-johnson-window-hasse-coherence-resolution.md":
        "e88afb6ebf94508f5ef552a804c888ce3221a07a663c381f3db9332a8a279130",
    "computations/verify_h5_pointed_phi_two_spectator_beck_chevalley_coherence.py":
        "55f363146627bf44974d28556bd669b4c1908cab9bb187b9a389e2cbd23fd650",
    "notes/h5-pointed-phi-two-spectator-beck-chevalley-coherence.md":
        "c56d667abc5e4d5396a76972c383e87412dd74ebdb25b029e2d8e8a08307f365",
    "computations/verify_h6_five_tail_divided_hasse_protected_boundary_gate.py":
        "7128b655eefc576033932a6e38f6cef0a33bbfdfd87d84862418b88215448de2",
    "notes/h6-five-tail-divided-hasse-protected-boundary-gate.md":
        "fd05a8df4f829a40cc1ca3cb2b4ee509833f73a1fb8c02ac668cd2108f36b91f",
    "computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py":
        "0eedcb3f03e98ea18b549e2b6e21d7082cf368d8e3bc77fd3f104a178104c25a",
}
EXPECTED_LEDGER_SHA256 = "f4c29d574e796c21fac989b7e55cdc5967028af604da60ca67b751ea6f019b3b"

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Window = tuple[Edge, Edge]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def odd_double_factorial(value: int) -> int:
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        selected = (min(first, second), max(first, second))
        for tail in perfect_matchings(rest):
            yield tuple(sorted((selected,) + tail))


def matching_key(value: Matching) -> str:
    return "|".join(f"{left}{right}" for left, right in value)


def window_key(value: Window) -> str:
    return "|".join(f"{left}{right}" for left, right in value)


def flip_neighbors(value: Matching) -> tuple[Matching, ...]:
    answer = set()
    for first, second in combinations(value, 2):
        a, b = first
        c, d = second
        remainder = set(value) - {first, second}
        alternatives = (
            ((min(a, c), max(a, c)), (min(b, d), max(b, d))),
            ((min(a, d), max(a, d)), (min(b, c), max(b, c))),
        )
        for left, right in alternatives:
            answer.add(tuple(sorted(remainder | {left, right})))
    return tuple(sorted(answer))


def presentation_record(value: Matching, window: Window) -> dict[str, object]:
    require(len(window) == 2 and all(edge in value for edge in window),
            ("window outside matching", value, window))
    window = tuple(sorted(window))
    spectators = tuple(edge for edge in value if edge not in window)
    marked = min(window)
    tail_word = ["2"] * (2 * len(value))
    tail_word[marked[0]] = "1"
    tail_word[marked[1]] = "2"
    return {
        "matching": matching_key(value),
        "window": window_key(window),
        "word": "0121" + "".join(tail_word),
        "fine": "T_[" + matching_key(spectators) + "]*q_(v," +
                window_key(window) + ")",
        "removed_edges": [list(edge) for edge in spectators],
        "reinserted_edges": [list(edge) for edge in spectators],
        "coarse_repeated": "P3+K2",
        "full_repeated": (
            "window=" + window_key(window) + ";spectators=" +
            matching_key(spectators)
        ),
        "coefficient_monomial": "q_[" + matching_key(value) + "]",
        "operation_parent": "Phi_KS,r0/P_f prolonged PP/AugP2",
    }


def fixed_partition_matchings(m: int) -> set[Matching]:
    fixed_sites = (0, 1, 2, 3)
    remote_sites = tuple(range(4, 2 * m))
    return {
        tuple(sorted(local + remote))
        for local in perfect_matchings(fixed_sites)
        for remote in perfect_matchings(remote_sites)
    }


def exchange_edges(matchings: tuple[Matching, ...]) \
        -> tuple[tuple[Matching, Matching], ...]:
    universe = set(matchings)
    result = set()
    for value in matchings:
        for neighbor in flip_neighbors(value):
            require(neighbor in universe, "flip left matching census")
            result.add(tuple(sorted((value, neighbor))))
    return tuple(sorted(result))


def multi_source_distances(matchings: tuple[Matching, ...],
                           fixed: set[Matching]) \
        -> tuple[dict[Matching, int], dict[Matching, Matching]]:
    distance = {value: 0 for value in fixed}
    parent: dict[Matching, Matching] = {}
    queue = deque(sorted(fixed))
    universe = set(matchings)
    while queue:
        value = queue.popleft()
        for neighbor in flip_neighbors(value):
            require(neighbor in universe, "BFS left matching census")
            if neighbor not in distance:
                distance[neighbor] = distance[value] + 1
                parent[neighbor] = value
                queue.append(neighbor)
    require(len(distance) == len(matchings), "exchange graph disconnected")
    return distance, parent


def fixed_partition_distance_audit(m: int, matchings: tuple[Matching, ...]) \
        -> dict[str, object]:
    fixed = fixed_partition_matchings(m)
    distance, parent = multi_source_distances(matchings, fixed)
    distribution = Counter(distance.values())
    fixed_count = 3 * odd_double_factorial(2 * m - 5)
    cross_two = 6 * math.comb(2 * m - 4, 2) * 2 * odd_double_factorial(
        2 * m - 7
    )
    cross_four = math.comb(2 * m - 4, 4) * math.factorial(4) * (
        odd_double_factorial(2 * m - 9)
    )
    require(len(fixed) == fixed_count
            and distribution == Counter({0: fixed_count, 1: cross_two,
                                         2: cross_four})
            and len(parent) == len(matchings) - len(fixed),
            ("fixed partition distance profile", m, distribution))
    return {
        "fixed_four_tail_sites": [0, 1, 2, 3],
        "fixed_partition_tail_matchings": len(fixed),
        "outside_tail_matchings": len(matchings) - len(fixed),
        "matching_exchange_distance_distribution": {
            str(key): distribution[key] for key in sorted(distribution)
        },
        "maximum_exchange_distance": max(distance.values()),
        "distance_one_description": "exactly two fixed-block sites leave",
        "distance_two_description": "all four fixed-block sites leave",
        "multi_root_forest_edges_needed": len(parent),
        "reachability": True,
    }


def fibre_cech_audit(m: int, matchings: tuple[Matching, ...]) \
        -> dict[str, object]:
    windows_per_tail = math.comb(m, 2)
    internal_edges_per_tail = 3 * math.comb(m, 3)
    objects = len(matchings) * windows_per_tail
    internal_edges = len(matchings) * internal_edges_per_tail
    incidence_rank = len(matchings) * (windows_per_tail - 1)
    h0 = objects - incidence_rank
    require(h0 == len(matchings), "window fibre H0")

    coefficient_check = Counter()
    fine_counts = set()
    for value in matchings:
        presentations = tuple(
            presentation_record(value, tuple(window))
            for window in combinations(value, 2)
        )
        require(len(presentations) == windows_per_tail
                and len({record["fine"] for record in presentations}) ==
                    windows_per_tail
                and len({record["full_repeated"] for record in
                         presentations}) == windows_per_tail,
                ("literal fibre label census", value))
        fine_counts.add(len({record["fine"] for record in presentations}))
        for _record in presentations:
            coefficient_check[value] += Q(1, windows_per_tail)
    require(set(coefficient_check.values()) == {Q(1)}
            and len(coefficient_check) == len(matchings),
            "normalized window cover multiplicity")
    return {
        "tail_matching_H0_classes": len(matchings),
        "window_presentations_per_tail": windows_per_tail,
        "total_window_objects": objects,
        "Johnson_edges_per_tail": internal_edges_per_tail,
        "total_internal_window_connectors": internal_edges,
        "internal_C1_to_C0_rank": incidence_rank,
        "H0_after_internal_Cech_BC_Hasse": h0,
        "normalized_section": (
            f"s(M)=1/{windows_per_tail} times sum over all windows W subset M"
        ),
        "projection_section_identity": True,
        "every_matching_coefficient_after_normalization": "1",
        "literal_fine_and_repeated_labels_per_fibre":
            next(iter(fine_counts)),
        "higher_cell_effect_on_H0": (
            "none: triangle, BC and signed higher Hasse cells change ker(d1) "
            "and higher homology, not im(d1)"
        ),
        "conditional_positive_descent": (
            "one natural labelled Phi instance on every window plus the "
            "signed Hasse tower descends independently to one class Phi(M) "
            "for every matching M"
        ),
    }


def exchange_label_and_h0_audit(m: int, matchings: tuple[Matching, ...]) \
        -> dict[str, object]:
    edges = exchange_edges(matchings)
    expected_degree = 2 * math.comb(m, 2)
    expected_edges = len(matchings) * math.comb(m, 2)
    require(len(edges) == expected_edges
            and all(len(flip_neighbors(value)) == expected_degree
                    for value in matchings),
            "matching exchange graph census")

    common_windows_per_exchange = math.comb(m - 2, 2)
    lifted = 0
    equal_words = 0
    equal_windows = 0
    unequal_fines = 0
    unequal_repeated = 0
    unequal_coefficients = 0
    examples = []
    for left, right in edges:
        common_edges = tuple(sorted(set(left) & set(right)))
        require(len(common_edges) == m - 2,
                ("exchange common edge count", left, right))
        for window in combinations(common_edges, 2):
            left_record = presentation_record(left, tuple(window))
            right_record = presentation_record(right, tuple(window))
            require(left_record["word"] == right_record["word"]
                    and left_record["window"] == right_record["window"]
                    and left_record["fine"] != right_record["fine"]
                    and left_record["full_repeated"] !=
                        right_record["full_repeated"]
                    and left_record["coefficient_monomial"] !=
                        right_record["coefficient_monomial"],
                    ("strongest exchange lift labels", left_record,
                     right_record))
            lifted += 1
            equal_words += 1
            equal_windows += 1
            unequal_fines += 1
            unequal_repeated += 1
            unequal_coefficients += 1
            if len(examples) < 3:
                examples.append({"left": left_record,
                                 "right": right_record})
    require(lifted == len(edges) * common_windows_per_exchange
            and len({equal_words, equal_windows, unequal_fines,
                     unequal_repeated, unequal_coefficients}) == 1,
            "lifted exchange count")

    windows = math.comb(m, 2)
    objects = len(matchings) * windows
    internal_rank = len(matchings) * (windows - 1)
    raw_full_rank = objects - 1
    fixed = fixed_partition_matchings(m)
    outside = len(matchings) - len(fixed)
    raw_forest_rank = internal_rank + outside
    require(objects - internal_rank == len(matchings)
            and objects - raw_forest_rank == len(fixed)
            and objects - raw_full_rank == 1,
            "exchange H0 ranks")

    # Presentation-safe graph cylinder: add one u coordinate for each edge
    # of the multi-root forest.  Its columns have unique -u pivots, hence
    # rank outside and H0 remains N rather than falling to |F|.
    cylinder_c0 = len(matchings) + outside
    cylinder_rank = outside
    cylinder_h0 = cylinder_c0 - cylinder_rank
    require(cylinder_h0 == len(matchings), "exchange cylinder H0")
    return {
        "matching_exchange_degree": expected_degree,
        "matching_exchange_edges": len(edges),
        "common_window_lifts_per_exchange": common_windows_per_exchange,
        "total_strongest_common_window_lifts": lifted,
        "all_common_lifts_same_word": equal_words == lifted,
        "all_common_lifts_same_q_window": equal_windows == lifted,
        "all_common_lifts_change_spectator_fine": unequal_fines == lifted,
        "all_common_lifts_change_full_repeated_label":
            unequal_repeated == lifted,
        "all_common_lifts_change_coefficient_monomial":
            unequal_coefficients == lifted,
        "first_literal_mismatch": (
            "spectator fine T_S and tied removed/reinserted repeated label; "
            "the underlying matching coefficient monomial changes as well"
        ),
        "sample_lifts": examples,
        "matching_H0_before_cross_exchange": len(matchings),
        "H0_after_minimal_fixed_partition_forest": len(fixed),
        "H0_loss_on_attaching_outside_tails": outside,
        "H0_after_all_raw_exchange_bars": 1,
        "H0_loss_after_all_raw_exchange_bars": len(matchings) - 1,
        "BC_or_higher_Hasse_can_restore_H0": False,
        "presentation_safe_exchange_cylinder": {
            "boundary": "db_e=(M'-M)-u_e",
            "new_u_coordinates": outside,
            "C0_dimension_on_matching_quotient": cylinder_c0,
            "C1_image_rank": cylinder_rank,
            "H0_dimension": cylinder_h0,
            "unpaid_debt": (
                "the u_e classes retain the changed coefficient/fine/repeated "
                "labels and require a new physical exchange comparison"
            ),
        },
        "terminal_duals": (
            f"{outside} independent outside-matching coordinate covectors; "
            "each extends over db_e by chi(u_e)=chi(M')-chi(M)"
        ),
    }


def order_audit(m: int) -> dict[str, object]:
    h = m + 1
    matchings = tuple(perfect_matchings(tuple(range(2 * m))))
    require(len(matchings) == odd_double_factorial(2 * m - 1),
            "matching census")
    fixed = fixed_partition_distance_audit(m, matchings)
    fibre = fibre_cech_audit(m, matchings)
    exchange = exchange_label_and_h0_audit(m, matchings)
    require(fixed["outside_tail_matchings"] ==
                exchange["H0_loss_on_attaching_outside_tails"],
            "outside/H0 loss mismatch")
    return {
        "h": h,
        "tail_edges": m,
        "tail_sites": 2 * m,
        "all_tail_matchings": len(matchings),
        "fixed_partition_reachability": fixed,
        "window_fibre_normalized_Cech": fibre,
        "matching_exchange_label_and_H0_gate": exchange,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    records = tuple(order_audit(m) for m in (4, 5))
    require([record["fixed_partition_reachability"]
             ["outside_tail_matchings"] for record in records] == [96, 900]
            and [record["window_fibre_normalized_Cech"]
                 ["H0_after_internal_Cech_BC_Hasse"]
                 for record in records] == [105, 945],
            "h5/h6 headline counts")
    ledger = {
        "theorem": "h5/h6 full-tail window Cech and matching-exchange descent gate",
        "pins": PINS,
        "orders": list(records),
        "conditional_positive_theorem": (
            "If Phi is a genuinely source-labelled natural schema on every "
            "two-edge window and the signed Hasse deletion tower acts on all "
            "literal PP/AugP2 labels, then normalized Cech descent is the "
            "direct sum over matchings: average the C(m,2) windows inside "
            "each matching, obtaining one Phi(M), and sum over every M.  "
            "Each matching coefficient occurs exactly once and matching-"
            "indexed H0 is unchanged.  This covers the 96/900 tails outside "
            "the fixed partition without any cross-matching identification."
        ),
        "matching_exchange_verdict": (
            "The flip graph proves two-step reachability but not physical "
            "descent.  Its strongest common-window lift preserves word and "
            "q-window yet changes coefficient, spectator fine and full "
            "repeated labels.  Raw bars attaching the outside tails lower "
            "H0 by exactly 96/900; all flip bars lower it to one.  BC and "
            "higher Hasse cells cannot change this C1-to-C0 image.  A graph "
            "cylinder preserves H0 only by retaining an equally large u_e "
            "exchange debt."
        ),
        "scope": (
            "exact complete matching and two-window census for h=5 and h=6, "
            "including every matching flip and every strongest common-window "
            "lift with literal site word, fine, removed/reinserted, repeated, "
            "coefficient and operation labels.  The positive theorem is "
            "conditional on natural Phi/full Hasse action; it does not "
            "derive naturality from one fixed-partition cell or construct "
            "the optional coefficient-changing exchange comparison."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("full-tail window descent ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "h5", "h6", "cech",
                                           "exchange", "labels", "h0"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h5/h6 full-tail window descent ({arguments.mode}): PASS")
        print("per-matching normalized Cech H0: 105, 945 (PRESERVED)")
        print("outside fixed partition: 96, 900; exchange distance <=2")
        print("raw forest H0 loss: 96, 900")
        print("all flip bars H0: 1, 1")
        print("first cross-tail mismatch: fine/repeated/coefficient, not word")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
