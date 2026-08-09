#!/usr/bin/env python3
"""Exact overlap audit for two reciprocal pairs sharing one endpoint.

The full-pair four-cover theorem is applied to deletions pq and pr.  The
checker proves the general common-site overlap and enumerates the complete
rank-at-most-two omission normal forms, including the distinguished-site
diagonal routing clauses supplied by the two reciprocal coordinate blocks.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLORS = (0, 1, 2)
COMMON = tuple(range(5))
EXCEPTIONAL = 5
PINS = {
    "computations/verify_n8_rge4_reciprocal_classification.py":
        "55e3c94cbce928b39bb2f41885266549dd5d897ba5493dded520ee13595624e0",
}
FOUR_COVER_DEPENDENCY_COMMIT = "6a9f784"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency drift: {relative}")


def general_fourcover_overlap():
    """Each colour has a common residual site in both pair covers."""

    residual = COMMON + (EXCEPTIONAL,)
    covers = tuple(
        frozenset(chosen)
        for size in range(4, 7)
        for chosen in combinations(residual, size)
    )
    require(len(covers) == 22, "six-site four-cover census changed")
    minimum_common_part = min(len(cover & set(COMMON)) for cover in covers)
    minimum_simultaneous = min(
        len((left & set(COMMON)) & (right & set(COMMON)))
        for left in covers for right in covers
    )
    require(minimum_common_part == 3,
            "a four-cover retained fewer than three common sites")
    require(minimum_simultaneous == 1,
            "two pair covers lost their forced common site")
    return len(covers), minimum_common_part, minimum_simultaneous


def balanced_omission_maps():
    """Every low-rank six-site chart omits each colour exactly twice."""

    return tuple(sorted(set(permutations((0, 0, 1, 1, 2, 2)))))


def state_from_maps(left, right):
    matrix = [[0] * 3 for _ in COLORS]
    for site in COMMON:
        matrix[left[site]][right[site]] += 1
    return (left[EXCEPTIONAL], right[EXCEPTIONAL],
            tuple(value for row in matrix for value in row))


def transform_state(state, color_permutation, exchange):
    left_exception, right_exception, flat = state
    matrix = [flat[3 * row:3 * row + 3] for row in COLORS]
    relabelled = [[0] * 3 for _ in COLORS]
    for left in COLORS:
        for right in COLORS:
            relabelled[color_permutation[left]][color_permutation[right]] = (
                matrix[left][right]
            )
    transformed = (
        color_permutation[left_exception],
        color_permutation[right_exception],
        tuple(value for row in relabelled for value in row),
    )
    if not exchange:
        return transformed
    return (
        transformed[1], transformed[0],
        tuple(relabelled[right][left]
              for left in COLORS for right in COLORS),
    )


def canonical_state(state):
    return min(
        transform_state(state, color_permutation, exchange)
        for color_permutation in permutations(COLORS)
        for exchange in (False, True)
    )


def mismatch_count(state):
    _left_exception, _right_exception, flat = state
    return sum(flat[3 * left + right]
               for left in COLORS for right in COLORS if left != right)


def low_rank_normal_forms():
    maps = balanced_omission_maps()
    require(len(maps) == 90, "balanced omission-map count changed")
    states = {state_from_maps(left, right) for left in maps for right in maps}
    require(len(states) == 99, "labelled contingency-state count changed")
    canonical = tuple(sorted({canonical_state(state) for state in states}))
    require(len(canonical) == 16, "shared-pair omission orbit count changed")
    histogram = Counter(mismatch_count(state) for state in canonical)
    require(histogram == {0: 1, 1: 1, 2: 3, 3: 3, 4: 5, 5: 3},
            f"omission mismatch orbit histogram changed: {histogram}")

    # If the exceptional omitted colours differ, the common five-site
    # multisets have different profiles (1,2,2), so some common site must be
    # a mismatch.  There is exactly one orbit with no mismatch: both
    # exceptional sites omit the same colour and the five common planes
    # agree site by site.
    for left in maps:
        for right in maps:
            state = state_from_maps(left, right)
            if left[EXCEPTIONAL] != right[EXCEPTIONAL]:
                require(mismatch_count(state) >= 1,
                        "different exceptional omissions aligned everywhere")
    zero_orbits = tuple(state for state in canonical if mismatch_count(state) == 0)
    require(len(zero_orbits) == 1,
            "aligned omission normal form stopped being unique")
    return maps, states, canonical, histogram


def common_core_plane_intersections():
    """A disagreement of omission colours purifies the common core."""

    planes = {omitted: set(COLORS) - {omitted} for omitted in COLORS}
    table = {}
    for left in COLORS:
        for right in COLORS:
            intersection = planes[left] & planes[right]
            table[(left, right)] = tuple(sorted(intersection))
            if left == right:
                require(intersection == planes[left],
                        "equal omission planes changed")
            else:
                third = (set(COLORS) - {left, right}).pop()
                require(intersection == {third},
                        "mismatched omission planes lost coordinate-line core")
    return table


def reciprocal_diagonal_routing():
    """Audit the distinguished omission support alternatives.

    In the pr-deletion chart, if q omits colour j internally, the two star
    factors must cover q in pure colour j.  Therefore A_pq[j,j] or
    A_rq[j,j] is nonzero.  A reciprocal coordinate block A_pq=lambda E_ba
    has such a diagonal cell exactly when a=b=j.  The pq-deletion chart gives
    the symmetric clause at r.
    """

    direct_types = (None, 0, 1, 2)  # None means reciprocal off diagonal.
    clauses = []
    for omitted_r in COLORS:
        for omitted_q in COLORS:
            for diagonal_pq in direct_types:
                for diagonal_pr in direct_types:
                    required_chord = set()
                    if diagonal_pq != omitted_q:
                        required_chord.add(omitted_q)
                    if diagonal_pr != omitted_r:
                        required_chord.add(omitted_r)
                    # The exact support clause is
                    # (pq diagonal j OR qr[j,j]) AND
                    # (pr diagonal i OR qr[i,i]).
                    for chord_diagonals_code in range(8):
                        chord_diagonals = {
                            color for color in COLORS
                            if chord_diagonals_code & (1 << color)
                        }
                        survives = required_chord <= chord_diagonals
                        direct_formula = (
                            (diagonal_pq == omitted_q
                             or omitted_q in chord_diagonals)
                            and
                            (diagonal_pr == omitted_r
                             or omitted_r in chord_diagonals)
                        )
                        require(survives == direct_formula,
                                "distinguished diagonal routing changed")
                    clauses.append((omitted_r, omitted_q,
                                    diagonal_pr, diagonal_pq,
                                    tuple(sorted(required_chord))))
    require(len(clauses) == 144,
            "reciprocal diagonal-routing clause count changed")
    return clauses


def main():
    pin_dependencies()
    cover_data = general_fourcover_overlap()
    maps, states, canonical, histogram = low_rank_normal_forms()
    intersections = common_core_plane_intersections()
    clauses = reciprocal_diagonal_routing()
    ledger = {
        "four_cover_dependency_commit": FOUR_COVER_DEPENDENCY_COMMIT,
        "four_covers": cover_data[0],
        "minimum_common_sites_per_cover": cover_data[1],
        "minimum_simultaneous_common_sites_per_color": cover_data[2],
        "balanced_omission_maps": len(maps),
        "labelled_contingency_states": len(states),
        "omission_orbits": len(canonical),
        "mismatch_orbit_histogram": dict(sorted(histogram.items())),
        "plane_intersections": {
            f"{left}{right}": list(value)
            for (left, right), value in sorted(intersections.items())
        },
        "diagonal_routing_clauses": len(clauses),
        "canonical_states": [list(state[:2]) + [list(state[2])]
                             for state in canonical],
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    expected = "b99959a6a30f9faf012baad082d990f4bc7895107405f86f6a05b23a0af10c01"
    require(digest == expected, f"shared-pair overlap ledger changed: {digest}")
    print("shared reciprocal four-cover overlap: PASS")
    print("general common-site minimum per color:", cover_data[2])
    print("low-rank omission normal forms: 99 labelled / 16 orbits")
    print("mismatch orbit histogram:", dict(sorted(histogram.items())))
    print("distinguished diagonal-routing clauses:", len(clauses))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
