#!/usr/bin/env python3
"""Exact active-exit dichotomy for a decorated selected-anchor edge.

Let Q0,Q1,Q2 be selected pure target matchings, let e=vu belong to Q0,
and let a second nonzero pure-0 matching Q0' avoid e.  Q0' is the
alternating repair needed to make the deleted stars of e rank three.

The target-augmented source identity for a nonzero off-diagonal cell q_u on
e supplies an active product Delta_us*C_s.  If vs avoids Q1 union Q2, then
Q0,Q1,Q2 make the active companion pair vs rank three, while Q0',Q1,Q2
make e rank three.  Delta_us != 0 supplies distinct centre heads.  The only
incidence escapes are a multiply used e, or concentration of every active
product on the at most two Q1/Q2 anchor neighbours of v.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_crossed_lock_common_provenance_boundary.py":
        "862a615b9da32743964380917f178774c6725dd6390cec9ce259f021d58f3033",
    "notes/uniform-crossed-lock-common-provenance-boundary.md":
        "d7b7b6befea91d15c672fe928162aa4c54988b40a83ab2ad32f2dfdd217f5dd7",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
    "computations/verify_uniform_five_lock_diagonal_mate_obstruction.py":
        "c5cbea951b2bab4cfb83971fc68386c538166ec020bdfafc62fd03d75244481a",
    "notes/uniform-five-lock-diagonal-mate-obstruction.md":
        "39cdab0b012aaa5e1387ef396391adfc7dc97eb42853963f93abb070988c42ce",
    "computations/verify_uniform_diagonal_aggregate_offdiagonal_quadratic_defect.py":
        "cdf5a71f6f5dcef524c22c9790f0a29bf902ddf8e58bccb7b5233655f0359f07",
    "notes/uniform-diagonal-aggregate-offdiagonal-quadratic-defect.md":
        "9aa57c618f3ae8bca6b335fb050c881039e70449f6798240a50ba28429e667fb",
}
EXPECTED_LEDGER_SHA256 = (
    "78c6744f5b1f91ff3344ab77eb91191be55144335c05dbf074c0eda9290693f4"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(left, right),) + tail))


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError(f"site {site} is absent from {matching}")


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


def endpoint_columns(selected, site, deleted_pair):
    columns = []
    for colour, matching in enumerate(selected):
        neighbour = partner(matching, site)
        if edge(site, neighbour) != deleted_pair:
            columns.append((neighbour, colour))
    rows = sorted(columns)
    matrix = [[Q(int(row == column)) for column in columns] for row in rows]
    return tuple(columns), rank(matrix)


def pair_ranks(selected, deleted_pair):
    return tuple(endpoint_columns(selected, site, deleted_pair)[1]
                 for site in deleted_pair)


def alternating_component(first, second, seed_edge):
    adjacency = {}
    symmetric = set(first) ^ set(second)
    require(seed_edge in symmetric,
            "the repaired edge left the alternating symmetric difference")
    for left, right in symmetric:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    seen = set(seed_edge)
    frontier = list(seed_edge)
    while frontier:
        site = frontier.pop()
        for neighbour in adjacency.get(site, ()):
            if neighbour not in seen:
                seen.add(neighbour)
                frontier.append(neighbour)
    component_edges = {pair for pair in symmetric if set(pair) <= seen}
    require(all(len(adjacency[site]) == 2 for site in seen),
            "the repair component stopped being an alternating cycle")
    return component_edges


def active_landing(q0, q0_prime, q1, q2, decorated, centre,
                   active_site, q_u, delta, cofactor):
    """Apply the selected-anchor rank proof to one source-active product."""
    require(centre in decorated and active_site not in decorated,
            "the active companion did not leave the decorated pair")
    require(decorated in q0 and decorated not in q0_prime,
            "Q0' does not repair the decorated Q0 edge")
    alternating_component(q0, q0_prime, decorated)
    active_product = delta * cofactor
    require(q_u and delta and cofactor and q_u + active_product == 0,
            "the one-term target-augmented identity is not exact")
    if decorated in q1 or decorated in q2:
        return {"landing": False, "obstruction": "multiply_used_anchor"}

    companion = edge(centre, active_site)
    if companion in q1 or companion in q2:
        return {"landing": False,
                "obstruction": "active_product_trapped_on_anchor"}

    direct_ranks = pair_ranks((q0_prime, q1, q2), decorated)
    companion_ranks = pair_ranks((q0, q1, q2), companion)
    require(direct_ranks == (3, 3) and companion_ranks == (3, 3),
            "the free active companion lost a selected-anchor column")
    return {
        "landing": True,
        "decorated_pair": decorated,
        "active_companion_pair": companion,
        "shared_centre": centre,
        "four_deleted_star_ranks": direct_ranks + companion_ranks,
        "transition_minor": str(delta),
        "cofactor": str(cofactor),
        "transition_minor_times_cofactor": str(active_product),
        "distinct_heads": True,
        "source_operation": "matching reselection only",
    }


def audit_canonical_active_landing():
    q0 = ((0, 1), (2, 3), (4, 5), (6, 7))
    q0_prime = ((0, 2), (1, 3), (4, 5), (6, 7))
    q1 = ((0, 3), (1, 2), (4, 6), (5, 7))
    q2 = ((0, 5), (1, 4), (2, 6), (3, 7))
    landing = active_landing(
        q0, q0_prime, q1, q2, (0, 1), 0, 4,
        Q(1), Q(-1), Q(1))
    require(landing["landing"]
            and landing["four_deleted_star_ranks"] == (3, 3, 3, 3),
            "the canonical active-exit landing failed")

    # The actual alternating exit 02 has a nonzero pure cofactor, but that
    # fact alone says nothing about its transition minor.  The landing may
    # use any source-active site, here the free site 4.
    exit_pair = edge(0, partner(q0_prime, 0))
    require(exit_pair == (0, 2) and exit_pair not in q0,
            "the canonical alternating repair exit changed")
    return {
        "landing": landing,
        "alternating_repair_exit": exit_pair,
        "guard": (
            "the repair exit need not itself have nonzero transition minor; "
            "the target-augmented identity selects the active companion"
        ),
    }


def audit_sharp_source_labelled_guards():
    q0 = ((0, 1), (2, 3), (4, 5), (6, 7))
    q0_prime = ((0, 2), (1, 3), (4, 5), (6, 7))
    decorated = (0, 1)
    free = ((0, 4), (1, 5), (2, 6), (3, 7))

    shared = active_landing(
        q0, q0_prime, q0, free, decorated, 0, 3,
        Q(1), Q(-1), Q(1))
    require(shared == {"landing": False,
                       "obstruction": "multiply_used_anchor"},
            "the multiply anchored direct-pair guard changed")
    shared_ranks = pair_ranks((q0_prime, q0, free), decorated)
    require(shared_ranks == (2, 2),
            "the multiply anchored selected-rank guarantee changed")

    traps_active = ((0, 3), (1, 2), (4, 6), (5, 7))
    trapped = active_landing(
        q0, q0_prime, traps_active, free,
        decorated, 0, 3, Q(1), Q(-1), Q(1))
    require(trapped == {"landing": False,
                        "obstruction": "active_product_trapped_on_anchor"},
            "the trapped active-product guard changed")
    trapped_ranks = pair_ranks((q0, traps_active, free), (0, 3))
    require(trapped_ranks == (2, 2),
            "the trapped active pair selected-rank guarantee changed")

    # A known nonzero repair cofactor at 02 can have zero determinant while
    # the complete target-augmented identity is carried on trapped 03:
    # p_u=q_u=p_2=q_2=1 gives Delta_u2=0; p_3=0,q_3=-1 gives
    # Delta_u3*C_3=-1=-q_u.  Thus incidence plus one alternating repair does
    # not force the repair exit itself to be active.
    p_u, q_u = Q(1), Q(1)
    p_exit, q_exit, c_exit = Q(1), Q(1), Q(1)
    p_trap, q_trap, c_trap = Q(0), Q(-1), Q(1)
    delta_exit = p_u * q_exit - q_u * p_exit
    delta_trap = p_u * q_trap - q_u * p_trap
    require(delta_exit == 0 and c_exit,
            "the inactive alternating-exit cofactor guard changed")
    require(q_u + delta_exit * c_exit + delta_trap * c_trap == 0,
            "the trapped one-term source identity stopped cancelling")
    return {
        "multiply_used_anchor": {
            "result": shared,
            "selected_anchor_rank_guarantee": shared_ranks,
        },
        "active_product_trapped_on_anchor": {
            "result": trapped,
            "selected_anchor_rank_guarantee": trapped_ranks,
        },
        "repair_exit_need_not_be_active": {
            "Delta_exit": str(delta_exit),
            "C_exit": str(c_exit),
            "Delta_trapped_times_C": str(delta_trap * c_trap),
            "q_u_plus_sum_DeltaC": "0",
            "scope": "exact target-augmented scalar packet",
        },
    }


def audit_complete_n8_incidence_census():
    sites = tuple(range(8))
    matchings = tuple(perfect_matchings(sites))
    require(len(matchings) == 105, "the K8 matching count changed")
    q0 = ((0, 1), (2, 3), (4, 5), (6, 7))
    decorated = (0, 1)
    centre, other = decorated
    repairs = tuple(matching for matching in matchings
                    if decorated not in matching)
    require(len(repairs) == 90,
            "the alternating repair-matching count changed")

    configurations = Counter()
    designated_exit = Counter()
    for q0_prime in repairs:
        repair_exit = edge(centre, partner(q0_prime, centre))
        for q1, q2 in itertools.product(matchings, repeat=2):
            if decorated in q1 or decorated in q2:
                configurations["multiply_used_anchor"] += 1
                designated_exit["multiply_used_anchor"] += 1
                continue
            blocked = {
                partner(q1, centre), partner(q2, centre)
            }
            require(other not in blocked,
                    "a supposedly unique decorated edge stayed blocked")
            free_sites = set(sites) - {centre, other} - blocked
            require(len(free_sites) in (4, 5),
                    "the two other matchings blocked too many active sites")
            configurations[f"unique_edge_free_active_sites_{len(free_sites)}"] += 1
            designated_exit[
                "repair_exit_free"
                if partner(q0_prime, centre) in free_sites
                else "repair_exit_trapped"
            ] += 1

    expected_configurations = Counter({
        "multiply_used_anchor": 263250,
        "unique_edge_free_active_sites_4": 607500,
        "unique_edge_free_active_sites_5": 121500,
    })
    expected_exit = Counter({
        "multiply_used_anchor": 263250,
        "repair_exit_free": 506250,
        "repair_exit_trapped": 222750,
    })
    require(configurations == expected_configurations,
            f"the active-site incidence census changed: {configurations}")
    require(designated_exit == expected_exit,
            f"the repair-exit census changed: {designated_exit}")
    return {
        "normalization": "Q0 fixed, decorated edge 01 and centre 0 fixed",
        "repair_matchings_Q0_prime": len(repairs),
        "other_selected_matching_pairs": len(matchings) ** 2,
        "total_configurations": len(repairs) * len(matchings) ** 2,
        "active_site_capacity": dict(configurations),
        "alternating_repair_exit": dict(designated_exit),
        "uniform_measure": (
            "after excluding a multiply used decorated edge, Q1 and Q2 "
            "trap at most two active sites; at least N-4 sites are free"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "canonical_active_landing": audit_canonical_active_landing(),
        "sharp_source_labelled_guards": audit_sharp_source_labelled_guards(),
        "complete_n8_incidence_census": audit_complete_n8_incidence_census(),
        "uniform_theorem": (
            "a uniquely anchored decorated edge with a nonzero pure-colour "
            "alternating repair has rank-three deleted stars; any nonzero "
            "target-augmented determinant/cofactor product on a companion "
            "edge outside the other two selected matchings supplies the "
            "distinct-head active arm and the other two rank-three stars"
        ),
        "exact_residual": (
            "the decorated pair is used by another selected colour, or "
            "every nonzero determinant/cofactor product is concentrated "
            "on the at most two other-colour anchor neighbours of the "
            "decorated endpoint"
        ),
        "concentrated_01_10_coefficient_landing": (
            "the pinned quadratic aggregate theorem gives an ordinary "
            "source unit for every chart with at most two ordered 01/10 "
            "internal cells, including all eight nonzero quotient defects; "
            "its first coefficient residual is a three-cell decorated "
            "physical perfect matching entirely on selected anchor edges"
        ),
        "scope": (
            "the alternating repair cofactor need not itself have a "
            "nonzero transition minor; the complete source identity only "
            "guarantees some active product"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"anchor-edge active-exit ledger changed: {digest}")
    print("uniform anchor-edge active-exit dichotomy: PASS")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
