#!/usr/bin/env python3
"""Exact fixed-tail orbit/containment coverage of the four frozen 332 rescues."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results_tail_polar_source_lift.json"
FROZEN = HERE / "results_611_71_sdr_and_332_rescue.json"
OUT = HERE / "results_332_rescue_orbit_cover.json"
VERTICES = tuple(range(8))
COLUMNS = tuple((site, tail) for tail in (6, 7) for site in range(6))
COLUMN_NAMES = tuple(f"{'y' if tail == 6 else 'z'}{site}"
                     for site, tail in COLUMNS)
SEED_ROWS = ("F_01001212", "F_00101212", "F_01100212")
EXPECTED_DIGEST = "6d55fe4a761cc60665268e1ebfa61215390b6994134749b7fa6fe5610f2b4ad2"


def require(value, detail):
    if not value:
        raise RuntimeError(detail)


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def vertex_actions():
    actions = []
    for block_permutation in permutations(range(3)):
        for flips in product((0, 1), repeat=4):
            mapping = {}
            for vertex in VERTICES:
                block, clone = divmod(vertex, 2)
                image_block = (block_permutation[block]
                               if block < 3 else 3)
                mapping[vertex] = 2*image_block + (clone ^ flips[block])
            actions.append(mapping)
    require(len(actions) == 96 and
            len({tuple(action.items()) for action in actions}) == 96,
            "fixed-tail vertex action changed")
    return actions


def transform_label(label, action):
    old = label.removeprefix("F_")
    new = [None]*8
    for vertex, colour in enumerate(old):
        new[action[vertex]] = colour
    return "F_"+"".join(new)


def transform_column(column, action):
    tail = 6 if column[0] == "y" else 7
    site = int(column[1:])
    image = tuple(sorted((action[site], action[tail])))
    require(image[0] < 6 and image[1] in (6, 7),
            "fixed-tail action ceased to preserve columns")
    return ("y" if image[1] == 6 else "z")+str(image[0])


def transform_coefficient(value, action):
    factors = []
    for factor in value.split("*"):
        match = re.fullmatch(r"g([012])_(\d)(\d)", factor)
        require(match is not None, ("non-monomial 332 coefficient", value))
        left, right = sorted((action[int(match.group(2))],
                              action[int(match.group(3))]))
        factors.append(f"g{match.group(1)}_{left}{right}")
    return "*".join(factors)


def doubled_sites(columns):
    names = set(columns)
    return tuple(site for site in range(6)
                 if f"y{site}" in names and f"z{site}" in names)


def block_shape(sites):
    counts = Counter(site//2 for site in sites)
    return tuple(sorted((counts.get(block, 0) for block in range(3)),
                        reverse=True))


def single_pivot_factors(columns, doubles):
    answer = []
    for column in columns:
        site = int(column[1:])
        if site not in doubles:
            answer.append(f"h1_{site}{6 if column[0] == 'y' else 7}")
    return sorted(answer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    frozen = json.loads(FROZEN.read_text())
    require(frozen["logical_sha256"] == EXPECTED_DIGEST,
            "frozen Hall/rescue digest changed")
    rows = {row["source_label"]: row for row in source["row_ledger"]}
    actions = vertex_actions()

    # Literal covariance of the two seed-row orbits, not only support
    # covariance.  The first two displayed rescue minors use rows in the
    # same orbit; the Hall representatives together generate two orbits.
    row_orbits = {}
    for seed in SEED_ROWS:
        orbit = set()
        seed_row = rows[seed]
        for action in actions:
            label = transform_label(seed, action)
            orbit.add(label)
            actual = rows[label]
            expected = {
                transform_column(column, action):
                    transform_coefficient(coefficient, action)
                for column, coefficient in seed_row["nonzero_columns"].items()
            }
            require(actual["profile"] == "3+3+2" and
                    actual["nonzero_columns"] == expected,
                    ("literal 332 row transport changed", seed, label))
        row_orbits[seed] = sorted(orbit)
    require([len(row_orbits[seed]) for seed in SEED_ROWS] == [48, 48, 48],
            "seed row orbit sizes changed")
    require(row_orbits[SEED_ROWS[0]] == row_orbits[SEED_ROWS[1]] and
            not set(row_orbits[SEED_ROWS[0]]) & set(row_orbits[SEED_ROWS[2]]),
            "seed row orbit intersection changed")

    records = []
    status_counts = Counter()
    uncovered = []
    theta_by_shape = {
        (2, 2, 0): "Theta_220",
        (2, 1, 1): "Theta_211",
        (2, 2, 1): "Theta_221",
        (2, 2, 2): "Theta_222",
    }
    for record in frozen["orbit_ledger"]:
        status = record["status"]
        if status == "full_SDR":
            continue
        columns = record["representative_columns"]
        doubles = doubled_sites(columns)
        shape = block_shape(doubles)
        if len(doubles) == 2:
            rescue_type = ("two-double adjacent" if shape == (2, 0, 0)
                           else "two-double separated")
            coverage = "covered_exact_rescue_open"
            new_factor = ("M_adj" if shape == (2, 0, 0) else "M_sep")
        elif len(doubles) == 3:
            rescue_type = ("Hall adjacent triple" if shape == (2, 1, 0)
                           else "Hall separated triple")
            coverage = "covered_exact_rescue_open"
            new_factor = ("Delta_sep" if shape == (2, 1, 0)
                          else "Delta_sep")
        else:
            rescue_type = "needs multiple independent transported 332 rows"
            coverage = "uncovered_by_four_frozen_minors"
            new_factor = theta_by_shape[shape]
        item = {
            "representative_mask": record["representative_mask"],
            "representative_columns": columns,
            "fixed_tail_orbit_size": record["orbit_size"],
            "single_sites": record["single_sites"],
            "double_sites": record["double_sites"],
            "double_block_shape": list(shape),
            "original_status": status,
            "coverage": coverage,
            "rescue_route": rescue_type,
            "minimal_new_factor": new_factor,
            "singleton_extension_factors": single_pivot_factors(columns, doubles),
        }
        records.append(item)
        status_counts[(status, coverage)] += 1
        if coverage.startswith("uncovered"):
            uncovered.append(item)

    require(status_counts == {
        ("Delta_divisor", "covered_exact_rescue_open"): 33,
        ("Hall_defect", "covered_exact_rescue_open"): 16,
        ("Hall_defect", "uncovered_by_four_frozen_minors"): 11,
    }, "rescue coverage census changed")
    uncovered_shapes = Counter(tuple(row["double_block_shape"])
                               for row in uncovered)
    require(uncovered_shapes == {
        (2, 2, 0): 4, (2, 1, 1): 4, (2, 2, 1): 2, (2, 2, 2): 1,
    }, "uncovered Hall shape census changed")

    # The first uncovered containment layer consists of the two four-double
    # site types.  Every later D contains one of these as a site subset.
    minimal_sets = ((0, 1, 2, 3), (0, 1, 2, 4))
    for row in uncovered:
        sites = doubled_sites(row["representative_columns"])
        require(any(block_shape(subset) in ((2, 2, 0), (2, 1, 1))
                    for subset in combinations(sites, 4)),
                ("uncovered pattern lacks four-site core", sites))
    antichain = [
        {"double_sites": list(sites), "double_block_shape": list(block_shape(sites)),
         "minimal_new_factor": theta_by_shape[block_shape(sites)]}
        for sites in minimal_sets
    ]

    result = {
        "status": "PASS exact four-rescue orbit/containment coverage ledger",
        "frozen_tail_group_order": len(actions),
        "literal_seed_row_orbits": {
            seed: {"orbit_size": len(row_orbits[seed]),
                   "orbit_sha256": logical_hash(row_orbits[seed])}
            for seed in SEED_ROWS
        },
        "distinct_seed_row_orbit_count": 2,
        "coverage_summary": {
            "Delta_orbits_total": 33,
            "Delta_orbits_covered_on_rescue_opens": 33,
            "Hall_orbits_total": 27,
            "Hall_orbits_covered_on_rescue_opens": 16,
            "Hall_orbits_uncovered": 11,
        },
        "coverage_table": records,
        "uncovered_shape_census": [
            {"double_block_shape": list(shape), "orbit_count": count,
             "minimal_new_factor": theta_by_shape[shape]}
            for shape, count in sorted(uncovered_shapes.items())
        ],
        "minimal_uncovered_containment_antichain": antichain,
        "interpretation": (
            "The four frozen minors, literal fixed-tail transports, and "
            "singleton E-site pivots cover every two-double orbit and every "
            "three-double Hall orbit on their displayed factor opens. They "
            "cannot alone prove a d>=4 pattern full: its 611+71 defect is "
            "d-2>=2, so a single transported 332 row raises rank by at most "
            "one. The next exact objects are the two-rescue determinants "
            "Theta_220 and Theta_211; larger shapes recurse from them."
        ),
        "scope_guard": (
            "Coverage means a literal nonzero maximal minor on the named "
            "principal open. Vanishing of M/Delta/Theta is not declared "
            "empty here and must route through the divisor ledger."
        ),
        "source_hashes": {
            "source": sha256(SOURCE.read_bytes()).hexdigest(),
            "frozen": sha256(FROZEN.read_bytes()).hexdigest(),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("332 rescue orbit cover: PASS", result["logical_sha256"])
    print("covered Delta/Hall; uncovered Hall", 33, 16, 11)
    print("antichain", [row["minimal_new_factor"] for row in antichain])


if __name__ == "__main__":
    main()
