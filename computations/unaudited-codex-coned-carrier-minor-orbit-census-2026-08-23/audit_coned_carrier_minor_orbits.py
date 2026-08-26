#!/usr/bin/env python3
"""Exact S8 x S3 orbit census for pure-coned carrier maximal minors."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_coned_carrier_minor_orbits.json"
SITES = tuple(range(8))
COLOURS = tuple(range(3))
TRIANGLE = (0, 1, 2)
OUTSIDE = (3, 4, 5)
CAP = (6, 7)
BASE_MATCHING = ((0, 1), (2, 3), (4, 5), (6, 7))
BASE_ROWS = ((0, 1), (1, 1), (2, 1))


def edge(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS = tuple(perfect_matchings(SITES))
ROW_LABELS = tuple(pair for pair in product(COLOURS, repeat=2) if pair != (0, 0))
ROW_SETS = tuple(combinations(ROW_LABELS, 3))
assert len(MATCHINGS) == 105 and len(ROW_SETS) == 56


def canonical_matching(matching):
    return tuple(sorted(edge(u, v) for u, v in matching))


def carrier_stabilizer():
    # Stabilize triangle/outside/cap blocks and residual colour zero.  The
    # cap may swap, and colours 1,2 may swap.
    answer = []
    for triangle_perm in permutations(TRIANGLE):
        for outside_perm in permutations(OUTSIDE):
            for cap_swap, colour_swap in product(range(2), repeat=2):
                site = list(SITES)
                site[:3] = triangle_perm
                site[3:6] = outside_perm
                if cap_swap:
                    site[6], site[7] = 7, 6
                colour = (0, 2, 1) if colour_swap else (0, 1, 2)
                answer.append((tuple(site), colour, bool(cap_swap)))
    assert len(answer) == 144
    return tuple(answer)


H = carrier_stabilizer()


def act_matching(matching, element):
    site, _, _ = element
    return canonical_matching((site[u], site[v]) for u, v in matching)


def act_rows(rows, element):
    _, colour, cap_reversed = element
    answer = []
    for a, b in rows:
        a, b = colour[a], colour[b]
        if cap_reversed:
            a, b = b, a
        answer.append((a, b))
    return tuple(sorted(answer))


def orbit_partition(items, action):
    items = set(items)
    seen = set()
    orbits = []
    for item in sorted(items):
        if item in seen:
            continue
        orbit = {action(item, element) for element in H}
        assert orbit <= items
        seen.update(orbit)
        orbits.append(orbit)
    assert seen == items
    return orbits


def block_signature(matching):
    block = {site: "T" for site in TRIANGLE}
    block.update({site: "O" for site in OUTSIDE})
    block.update({site: "P" for site in CAP})
    counts = Counter("".join(sorted((block[u], block[v]))) for u, v in matching)
    return dict(sorted(counts.items()))


def pair_orbits():
    universe = {(matching, rows) for matching in MATCHINGS for rows in ROW_SETS}
    seen = set()
    orbits = []
    for item in sorted(universe):
        if item in seen:
            continue
        orbit = {
            (act_matching(item[0], element), act_rows(item[1], element))
            for element in H
        }
        assert orbit <= universe
        seen.update(orbit)
        orbits.append(orbit)
    assert seen == universe and len(orbits) == 124
    return orbits


def act_full_descriptor(descriptor, site, colour):
    cap, triangle, residual_colour, matching, rows = descriptor
    cap_image = (site[cap[0]], site[cap[1]])
    cap_reversed = cap_image[0] > cap_image[1]
    cap_image = tuple(sorted(cap_image))
    triangle_image = tuple(sorted(site[value] for value in triangle))
    matching_image = canonical_matching((site[u], site[v]) for u, v in matching)
    rows_image = []
    for a, b in rows:
        a, b = colour[a], colour[b]
        if cap_reversed:
            a, b = b, a
        rows_image.append((a, b))
    return (
        cap_image, triangle_image, colour[residual_colour], matching_image,
        tuple(sorted(rows_image)),
    )


def full_base_orbit():
    base = (CAP, TRIANGLE, 0, BASE_MATCHING, BASE_ROWS)
    orbit = set()
    for site in permutations(SITES):
        for colour in permutations(COLOURS):
            orbit.add(act_full_descriptor(base, site, colour))
    assert len(orbit) == 60480
    canonical_intersection = {
        item for item in orbit
        if item[0] == CAP and item[1] == TRIANGLE and item[2] == 0
    }
    assert len(canonical_intersection) == 36
    return orbit, canonical_intersection


def independent_cone_colour_orbits(cone_colours):
    universe = {
        (cone_colour, matching, rows)
        for cone_colour in cone_colours for matching in MATCHINGS for rows in ROW_SETS
    }
    seen = set()
    count = 0
    sizes = Counter()
    for item in sorted(universe):
        if item in seen:
            continue
        orbit = set()
        for element in H:
            site, colour, _ = element
            orbit.add((
                colour[item[0]],
                act_matching(item[1], element),
                act_rows(item[2], element),
            ))
        orbit &= universe
        seen.update(orbit)
        count += 1
        sizes[len(orbit)] += 1
    assert seen == universe
    return count, dict(sorted(sizes.items()))


def audit():
    matching_orbits = orbit_partition(MATCHINGS, act_matching)
    row_orbits = orbit_partition(ROW_SETS, act_rows)
    joint_orbits = pair_orbits()
    assert len(matching_orbits) == 6
    assert len(row_orbits) == 17
    size_census = Counter(len(orbit) for orbit in joint_orbits)
    assert size_census == {36: 51, 72: 50, 24: 11, 12: 6, 18: 6}

    base_pair = (BASE_MATCHING, BASE_ROWS)
    base_orbit = next(orbit for orbit in joint_orbits if base_pair in orbit)
    base_matchings = {item[0] for item in base_orbit}
    base_rows = {item[1] for item in base_orbit}
    assert len(base_orbit) == 36
    assert len(base_matchings) == 9 and len(base_rows) == 4
    assert len(base_orbit) == len(base_matchings) * len(base_rows)

    full_orbit, canonical_intersection = full_base_orbit()
    full_family_size = 560 * 3 * 105 * 56
    assert full_family_size == 9_878_400
    assert sum(count * size * 1680 for size, count in size_census.items()) == full_family_size

    different_colour_count, different_colour_sizes = independent_cone_colour_orbits((1, 2))
    all_colour_count, all_colour_sizes = independent_cone_colour_orbits((0, 1, 2))
    assert different_colour_count == 236 and all_colour_count == 360

    result = {
        "status": "PASS coned carrier-minor orbit census: 124 same-colour target orbits",
        "canonical_target": {
            "pure_cone_colour": 0,
            "pure_matching": [list(pair) for pair in BASE_MATCHING],
            "cap_pair": list(CAP),
            "triangle": list(TRIANGLE),
            "carrier_colour": 0,
            "minor_rows": ["01", "11", "21"],
            "minor_columns": ["01", "02", "12"],
        },
        "fixed_carrier_stabilizer": {
            "order": len(H),
            "structure": "S3(triangle) x S3(outside) x S2(cap) x S2(nonresidual colours)",
        },
        "matching_chart_orbits": {
            "count": len(matching_orbits),
            "sizes": dict(sorted(Counter(len(orbit) for orbit in matching_orbits).items())),
            "records": [
                {
                    "representative": [list(pair) for pair in min(orbit)],
                    "size": len(orbit),
                    "block_incidence": block_signature(min(orbit)),
                }
                for orbit in matching_orbits
            ],
        },
        "minor_rowset_orbits": {
            "count": len(row_orbits),
            "sizes": dict(sorted(Counter(len(orbit) for orbit in row_orbits).items())),
            "records": [
                {
                    "representative": ["".join(map(str, pair)) for pair in min(orbit)],
                    "size": len(orbit),
                }
                for orbit in row_orbits
            ],
        },
        "joint_same_colour_targets": {
            "targets_per_fixed_carrier_colour": len(MATCHINGS) * len(ROW_SETS),
            "orbit_count": len(joint_orbits),
            "relative_orbit_size_census": dict(sorted(size_census.items())),
            "full_family_carrier_count": 560,
            "full_family_colour_count": 3,
            "full_family_target_count": full_family_size,
            "full_orbit_sizes": {
                str(relative_size * 1680): count
                for relative_size, count in sorted(size_census.items())
            },
        },
        "canonical_certificate_transport": {
            "full_S8xS3_orbit_size": len(full_orbit),
            "full_target_stabilizer_order": 241920 // len(full_orbit),
            "targets_on_each_fixed_carrier_colour": len(canonical_intersection),
            "matching_charts_reached": len(base_matchings),
            "minor_rowsets_reached": len(base_rows),
            "matching_minor_pairs_reached": len(base_orbit),
            "reached_matching_incidence": block_signature(BASE_MATCHING),
            "reached_minor_rowsets": [
                ["".join(map(str, pair)) for pair in rows]
                for rows in sorted(base_rows)
            ],
        },
        "independent_cone_colour_guard": {
            "same_as_carrier_colour_orbits": len(joint_orbits),
            "different_from_carrier_colour_orbits": different_colour_count,
            "all_cone_colours_orbits": all_colour_count,
            "different_colour_orbit_sizes": different_colour_sizes,
            "all_colour_orbit_sizes": all_colour_sizes,
        },
        "proof_spine_consequence": (
            "A certificate for the canonical M*Delta transports to only 9 of "
            "105 pure matching charts and 4 of 56 maximal minors on any fixed "
            "C_c (36 pairs), not to their full Cartesian family.  To sum over "
            "the pure matching cover and force all maximal minors, the natural "
            "same-colour strategy needs one certificate for each of 124 joint "
            "orbits.  Six matching types and 17 rowset types alone are not "
            "enough because the shared cap swap splits their product into 124, "
            "rather than 102, joint classes."
        ),
        "scope": (
            "Finite descriptor orbit census up to determinant sign. Cone colour "
            "is tied to carrier residual colour in the main 124-orbit count. "
            "If cone colour is independent, equality versus inequality is an "
            "additional invariant and 360 target orbits are required."
        ),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(canonical.encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check_results:
        if not OUT.exists() or OUT.read_text() != rendered:
            print("frozen result mismatch", file=sys.stderr)
            return 1
        print(result["status"], result["logical_sha256"])
        return 0
    OUT.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
