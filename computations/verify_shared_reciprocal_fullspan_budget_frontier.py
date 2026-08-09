#!/usr/bin/env python3
"""Audit the shared-reciprocal full-span rank-budget frontier.

The committed response-filtration theorem gives a six-site lower bound
``sum(dim W_u) >= 12``.  Its equality case is already closed by the
coordinate-plane, path/triangle, and wedge certificates pinned below.
This checker independently reconstructs the finite equality census and the
first strict-excess layer, budget 13.

A bit in a site mask means that the corresponding target axis is omitted
from ``W_u``.  At budget 13 there are exactly two possibilities:

* target-incidence sum 13: all spaces are coordinate target spans and the
  three colour-cover sizes are (5,4,4);
* target-incidence sum 12: all cover sizes are four and exactly one rank-one
  target span acquires one transverse direction.  The marked site must omit
  two axes; adding a direction to a rank-two target span would fill the
  three-dimensional target space and hence contain the allegedly omitted
  third axis.

Modulo six-site and three-colour relabeling these give nine normal forms.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLORS = range(3)
SITES = range(6)
COLOR_PERMUTATIONS = tuple(permutations(COLORS))
PINS = {
    "computations/verify_coordinate_plane_mixed_packet_obstruction.py":
        "a84e600cb8d9eed4371653e52401c37946163a9c4c9879f178b34e3c4c99e660",
    "computations/verify_full_rank_site_response_invisibility_countermodel.py":
        "793e53da8295bb64454b4d481ba90947cf9ebd0d9664cc9edfde55a2c00a8839",
    "computations/verify_rank_budget_path_triangle_exposed_grid_obstruction.py":
        "23f38b6b65ac9ddfb9cca0d8ae74a1c62e053ffb7f1f45cd7d55421a945fa0fe",
    "computations/verify_wedge_equality_hole_block_resolution.py":
        "851a209b9a4b903636611fb010f9d7f781fd84ed877c2e948fec343b00355f10",
    "computations/verify_shared_reciprocal_lowrank_pure_support_closure.py":
        "efb5a88b3571698ef89cd0129e1923940aed5623403e8f23d65db883fcce6c8e",
}
EXPECTED_LEDGER_SHA256 = (
    "0be34806754fdb6f63a777f9cc57da25984a40489c8156166dcdb2228394a54c"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency drift: {relative}")


def permute_mask(mask, permutation):
    out = 0
    for old, new in enumerate(permutation):
        if mask & (1 << old):
            out |= 1 << new
    return out


def canonical_unmarked(masks):
    """Quotient a six-site mask tuple by S_6 x S_3."""

    return min(
        tuple(sorted(permute_mask(mask, permutation) for mask in masks))
        for permutation in COLOR_PERMUTATIONS
    )


def canonical_marked(records):
    """Quotient mask/transverse-mark records by S_6 x S_3."""

    return min(
        tuple(sorted(
            (permute_mask(mask, permutation), marked)
            for mask, marked in records
        ))
        for permutation in COLOR_PERMUTATIONS
    )


def omission_counts(masks):
    return tuple(
        sum(bool(mask & (1 << color)) for mask in masks)
        for color in COLORS
    )


def target_ranks(masks):
    return tuple(3 - mask.bit_count() for mask in masks)


def rank_profile(dimensions):
    return tuple(dimensions.count(rank) for rank in (3, 2, 1))


def equality_census():
    """Reconstruct the three distinct-pair budget-twelve geometries."""

    labelled = []
    for masks in product(range(7), repeat=6):
        if omission_counts(masks) != (2, 2, 2):
            continue
        pairs = tuple(
            frozenset(site for site, mask in enumerate(masks)
                      if mask & (1 << color))
            for color in COLORS
        )
        # The double-quotient tensor-rank argument makes the three omission
        # pairs distinct.  The coordinate-plane theorem removes the no-rank3
        # case, so retain exactly the frontier handed to path/triangle/wedge.
        if len(set(pairs)) != 3 or 0 not in masks:
            continue
        labelled.append(masks)

    orbits = tuple(sorted({canonical_unmarked(row) for row in labelled}))
    expected = (
        (0, 0, 0, 3, 5, 6),       # triangle, profile (3,0,3)
        (0, 0, 1, 2, 5, 6),       # path, profile (2,2,2)
        (0, 1, 1, 2, 4, 6),       # wedge+disjoint, profile (1,4,1)
    )
    require(len(labelled) == 2280,
            f"labelled equality census changed: {len(labelled)}")
    require(orbits == expected, f"equality orbit census changed: {orbits}")
    profiles = Counter(rank_profile(target_ranks(row)) for row in orbits)
    require(profiles == {(3, 0, 3): 1, (2, 2, 2): 1, (1, 4, 1): 1},
            f"equality profiles changed: {profiles}")
    return labelled, orbits, profiles


def budget_thirteen_census():
    """Enumerate the first strict-excess normal forms exactly."""

    labelled = []
    for masks in product(range(7), repeat=6):
        omissions = omission_counts(masks)
        ranks = target_ranks(masks)
        incidence_sum = sum(ranks)

        # No transverse direction: total omission count five.  Four-cover
        # says every colour is omitted at most twice, hence (2,2,1).
        if incidence_sum == 13 and sorted(omissions) == [1, 2, 2]:
            labelled.append(tuple((mask, False) for mask in masks))

        # One transverse direction over equality target incidence.  It can
        # occur only at a rank-one target span (two omitted target axes).
        if incidence_sum == 12 and omissions == (2, 2, 2):
            for site, mask in enumerate(masks):
                if mask.bit_count() != 2:
                    continue
                labelled.append(tuple(
                    (other, index == site)
                    for index, other in enumerate(masks)
                ))

    orbits = tuple(sorted({canonical_marked(row) for row in labelled}))
    expected = (
        ((0, False), (0, False), (0, False), (1, False), (3, False), (6, False)),
        ((0, False), (0, False), (0, False), (1, False), (6, False), (6, False)),
        ((0, False), (0, False), (0, False), (3, False), (5, False), (6, True)),
        ((0, False), (0, False), (1, False), (1, False), (2, False), (6, False)),
        ((0, False), (0, False), (1, False), (1, False), (6, False), (6, True)),
        ((0, False), (0, False), (1, False), (2, False), (3, False), (4, False)),
        ((0, False), (0, False), (1, False), (2, False), (5, False), (6, True)),
        ((0, False), (1, False), (1, False), (2, False), (2, False), (4, False)),
        ((0, False), (1, False), (1, False), (2, False), (4, False), (6, True)),
    )
    require(len(labelled) == 7740,
            f"labelled budget-thirteen census changed: {len(labelled)}")
    require(orbits == expected,
            f"budget-thirteen orbit census changed: {orbits}")

    histogram = Counter()
    for orbit in orbits:
        dimensions = tuple(
            3 - mask.bit_count() + int(marked)
            for mask, marked in orbit
        )
        cover = tuple(sorted(
            (6 - value for value in omission_counts(
                tuple(mask for mask, _marked in orbit)
            )), reverse=True
        ))
        histogram[(any(marked for _mask, marked in orbit),
                   rank_profile(dimensions), cover)] += 1

    expected_histogram = {
        (False, (1, 5, 0), (5, 4, 4)): 1,
        (False, (2, 3, 1), (5, 4, 4)): 2,
        (False, (3, 1, 2), (5, 4, 4)): 2,
        (True, (1, 5, 0), (4, 4, 4)): 1,
        (True, (2, 3, 1), (4, 4, 4)): 2,
        (True, (3, 1, 2), (4, 4, 4)): 1,
    }
    require(histogram == expected_histogram,
            f"budget-thirteen orbit histogram changed: {histogram}")

    labelled_histogram = Counter()
    for row in labelled:
        dimensions = tuple(
            3 - mask.bit_count() + int(marked)
            for mask, marked in row
        )
        labelled_histogram[(
            "transverse" if any(marked for _mask, marked in row)
            else "coordinate",
            rank_profile(dimensions),
        )] += 1
    expected_labelled_histogram = {
        ("coordinate", (1, 5, 0)): 540,
        ("coordinate", (2, 3, 1)): 2160,
        ("coordinate", (3, 1, 2)): 900,
        ("transverse", (1, 5, 0)): 1080,
        ("transverse", (2, 3, 1)): 2700,
        ("transverse", (3, 1, 2)): 360,
    }
    require(labelled_histogram == expected_labelled_histogram,
            f"labelled strict-excess histogram changed: {labelled_histogram}")
    return labelled, orbits, histogram, labelled_histogram


def serial_counter(counter):
    return sorted((repr(key), value) for key, value in counter.items())


def main():
    pin_dependencies()
    equality_labelled, equality_orbits, equality_profiles = equality_census()
    strict_labelled, strict_orbits, strict_histogram, labelled_histogram = (
        budget_thirteen_census()
    )
    ledger = {
        "dependency_hashes": PINS,
        "equality_labelled": len(equality_labelled),
        "equality_orbits": equality_orbits,
        "equality_profiles": serial_counter(equality_profiles),
        "equality_status": "closed_by_pinned_exact_theorem_chain",
        "strict_excess_budget": 13,
        "strict_excess_labelled": len(strict_labelled),
        "strict_excess_orbits": strict_orbits,
        "strict_excess_orbit_histogram": serial_counter(strict_histogram),
        "strict_excess_labelled_histogram": serial_counter(labelled_histogram),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            f"ledger drift: {digest}")
    print("shared reciprocal full-span budget frontier: PASS")
    print(f"  equality: {len(equality_labelled)} labelled / "
          f"{len(equality_orbits)} orbits, all closed")
    print(f"  budget 13: {len(strict_labelled)} labelled / "
          f"{len(strict_orbits)} orbits")
    print("  split: 5 coordinate (cover 5,4,4) + "
          "4 one-transverse (cover 4,4,4)")
    print(f"  ledger_sha256={digest}")


if __name__ == "__main__":
    main()
