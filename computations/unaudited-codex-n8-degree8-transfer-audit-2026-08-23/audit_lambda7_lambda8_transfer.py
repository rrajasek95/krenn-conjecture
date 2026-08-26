#!/usr/bin/env python3
"""Exact transfer audit for the compatible chart-26 pair lambda7 -> lambda8.

This checker does not construct or solve any degree-nine system.  It verifies
the literal multiplication-by-t restriction, expands the invariant weights
to the full monomial space, classifies the 512 new top orbits, computes the
first homogeneous catalecticant ranks by exact sparse elimination, and
freezes two obstructions to a naive all-k recurrence.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
COMPUTATIONS = HERE.parent
D8_DIR = COMPUTATIONS / "unaudited-codex-n8-normalized-dfs-degree7-2026-08-23"
AUDIT_PATH = D8_DIR / "audit_degree8_dual_extension.py"
CORE_PATH = D8_DIR / "results_degree8_initial_core.json"
CERTIFICATE_PATH = D8_DIR / "results_degree8_rust_cegar.json"
RESULTS_PATH = HERE / "results_lambda7_lambda8_transfer.json"
EXPECTED = {
    AUDIT_PATH: "9df003b78c558a6ec2167651bcb06b98a9a86760c064dbae825e11085da40282",
    CORE_PATH: "0111fbb5c61c415d559d3927fcee1d4a451d546514ce9ffeef3f78502daa49b5",
    CERTIFICATE_PATH: "5d39aa3d8d6ae83a8b2b357e148232fb1046e069c79bed5ff8e5ff970b6d8485",
}
EXPECTED_DUAL8_SHA256 = (
    "561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    require(sha256(path.read_bytes()).hexdigest() == EXPECTED[path],
            f"source drift: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def parse_functional(record):
    return {
        bytes.fromhex(encoded): Fraction(numerator, denominator)
        for encoded, numerator, denominator in record
    }


def fraction_record(value):
    return [value.numerator, value.denominator]


def fraction_histogram(values):
    return [fraction_record(value) + [count]
            for value, count in sorted(Counter(values).items())]


def partition(values):
    return tuple(sorted(Counter(values).values(), reverse=True))


def partition_histogram(counter):
    return [[list(key), value] for key, value in sorted(counter.items())]


def expand_invariant(source, functional):
    full = {}
    for row, value in functional.items():
        orbit = source.normalized_row_orbit(row)
        require(row == min(orbit), "functional row is not canonical")
        actual_value = value / len(orbit)
        for actual in orbit:
            require(actual not in full, "distinct invariant rows share an orbit")
            full[actual] = actual_value
    return full


def contract_t(functional, degree):
    return {row: value for row, value in functional.items()
            if len(row) <= degree - 1}


def contract_coordinate(functional, coordinate, top_degree=None):
    answer = {}
    for row, value in functional.items():
        if top_degree is not None and len(row) != top_degree:
            continue
        if coordinate not in row:
            continue
        quotient = list(row)
        quotient.remove(coordinate)
        quotient = bytes(quotient)
        require(quotient not in answer,
                "a monomial contraction acquired a duplicate quotient")
        answer[quotient] = value
    return answer


def exact_sparse_rank_minor(rows):
    """Return rank and an exact pivot minor for labelled sparse rows."""
    basis = {}
    pivots = []
    pivot_labels = []
    determinant = Fraction(1)
    for label, raw in rows:
        row = {column: Fraction(value) for column, value in raw.items() if value}
        while row:
            pivot = min(row)
            coefficient = row[pivot]
            if pivot not in basis:
                determinant *= coefficient
                pivots.append(pivot)
                pivot_labels.append(label)
                basis[pivot] = {
                    column: value / coefficient
                    for column, value in row.items()
                }
                break
            for column, value in basis[pivot].items():
                updated = row.get(column, Fraction(0)) - coefficient * value
                if updated:
                    row[column] = updated
                else:
                    row.pop(column, None)
    pivot_record = [[label, pivot.hex()]
                    for label, pivot in zip(pivot_labels, pivots)]
    pivot_digest = sha256(json.dumps(
        pivot_record, separators=(",", ":")
    ).encode()).hexdigest()
    return {
        "rank": len(basis),
        "minor_determinant": fraction_record(determinant),
        "pivot_record_sha256": pivot_digest,
        "pivot_record": pivot_record,
    }


def combined_profile(source, row):
    coordinates = [source.D5.COORDINATES[value] for value in row]
    colours = Counter(
        colour for coordinate in coordinates for colour in coordinate[2:]
    )
    colour_profile = (
        colours[0], *sorted((colours[1], colours[2]), reverse=True)
    )
    return (
        len(source.normalized_row_orbit(row)),
        partition(row),
        partition(coordinate[:2] for coordinate in coordinates),
        partition(site for coordinate in coordinates for site in coordinate[:2]),
        colour_profile,
    )


def profile_record(profile):
    orbit, variables, edges, sites, colours = profile
    return {
        "row_orbit_size": orbit,
        "variable_multiplicity_partition": list(variables),
        "edge_multiplicity_partition": list(edges),
        "site_degree_partition": list(sites),
        "colour_endpoint_profile_0_then_sorted_12": list(colours),
    }


def audit(mutate=False):
    audit_module = load(AUDIT_PATH, "degree8_transfer_source")
    source = audit_module.load_d7()
    core = json.loads(CORE_PATH.read_text())
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    require(certificate["status"] == "EXTENDED_DUAL_EXACT_Q",
            "degree-eight certificate is not exact-terminal")
    record8 = certificate["exact_extended_dual"]
    digest8 = sha256(json.dumps(
        record8, separators=(",", ":")
    ).encode()).hexdigest()
    require(digest8 == certificate["exact_extended_dual_sha256"]
            == EXPECTED_DUAL8_SHA256, "degree-eight dual digest changed")

    lambda7 = parse_functional(core["degree7_dual"])
    lambda8 = parse_functional(record8)
    if mutate:
        lambda8[bytes.fromhex("0408757eaeccf5f6")] += 1
    lower8 = {row: value for row, value in lambda8.items() if len(row) <= 7}
    require(lower8 == lambda7, "rho_t(lambda8) is not lambda7")
    require(lambda8.get(b"") == lambda7.get(b"") == 1,
            "target pairing changed")

    top8 = {row: value for row, value in lambda8.items() if len(row) == 8}
    require(len(lambda7) == 49 and len(top8) == 512,
            "lower/top invariant support changed")
    full7 = expand_invariant(source, lambda7)
    full8 = expand_invariant(source, lambda8)
    actual_top8 = {row: value for row, value in full8.items() if len(row) == 8}
    require((len(full7), len(full8), len(actual_top8)) == (191, 2229, 2038),
            "full-space support census changed")
    require(contract_t(full8, 8) == full7,
            "full-space rho_t restriction changed")

    orbit_sizes = Counter(len(source.normalized_row_orbit(row)) for row in top8)
    require(orbit_sizes == Counter({4: 507, 2: 5}),
            "top row-orbit census changed")
    variable_partitions = Counter(partition(row) for row in top8)
    edge_partitions = Counter(partition(
        source.D5.COORDINATES[value][:2] for value in row
    ) for row in top8)
    site_partitions = Counter(partition(
        site for value in row for site in source.D5.COORDINATES[value][:2]
    ) for row in top8)
    colour_profiles = Counter()
    profile_classes = defaultdict(list)
    for row, value in top8.items():
        coordinates = [source.D5.COORDINATES[item] for item in row]
        colours = Counter(
            colour for coordinate in coordinates for colour in coordinate[2:]
        )
        colour_profile = (
            colours[0], *sorted((colours[1], colours[2]), reverse=True)
        )
        colour_profiles[colour_profile] += 1
        profile_classes[combined_profile(source, row)].append((row, value))
    ambiguous = {
        profile: rows for profile, rows in profile_classes.items()
        if len({value for _row, value in rows}) > 1
    }
    require((len(profile_classes), len(ambiguous),
             sum(map(len, ambiguous.values()))) == (94, 53, 462),
            "combined profile ambiguity census changed")
    collision_profile = (
        2,
        (1, 1, 1, 1, 1, 1, 1, 1),
        (2, 2, 1, 1, 1, 1),
        (2, 2, 2, 2, 2, 2, 2, 2),
        (8, 4, 4),
    )
    collision = sorted(ambiguous[collision_profile])
    require(collision == [
        (bytes.fromhex("0408757eaeccf5f6"), Fraction(1)),
        (bytes.fromhex("0507757eaeccf5f6"), Fraction(-3, 4)),
    ], "profile collision changed")

    # Every one-coordinate top deletion is private: it is distinct globally
    # and misses the entire old full-space support.
    deletions = set()
    deletion_count = 0
    for row in actual_top8:
        row_deletions = {
            row[:index] + row[index + 1:] for index in range(len(row))
        }
        deletion_count += len(row_deletions)
        deletions.update(row_deletions)
    require(deletion_count == len(deletions) == 16092,
            "top deletion uniqueness changed")
    require(not (deletions & set(full7)),
            "a new top deletion entered the old support")

    nonsupport_coordinates = sorted(
        set(range(len(source.D5.COORDINATES))) - set(source.D5.SUPPORT_IDS)
    )
    require(len(nonsupport_coordinates) == 240,
            "normalized coordinate census changed")

    hankel = {}
    active_by_level = {}
    for degree, functional in ((7, full7), (8, full8)):
        coordinate_channels = [
            (coordinate, contract_coordinate(functional, coordinate))
            for coordinate in nonsupport_coordinates
        ]
        active = [(coordinate, row) for coordinate, row in coordinate_channels
                  if row]
        rows = [("t", contract_t(functional, degree))] + [
            (f"x{coordinate}", row) for coordinate, row in active
        ]
        exact = exact_sparse_rank_minor(rows)
        expected = {
            7: (140, 141, Fraction(-1, 2 ** 152)),
            8: (220, 221, Fraction(-1, 2 ** 236)),
        }[degree]
        require((len(active), exact["rank"],
                 Fraction(*exact["minor_determinant"])) == expected,
                f"degree-{degree} first Hankel data changed")
        active_by_level[degree] = {coordinate for coordinate, _row in active}
        hankel[str(degree)] = {
            "nonzero_coordinate_contractions": len(active),
            "zero_coordinate_contractions": 240 - len(active),
            "t_contraction_support": len(contract_t(functional, degree)),
            "first_homogeneous_catalecticant_rows": len(rows),
            **exact,
        }

    top_channels = [
        (f"x{coordinate}", channel)
        for coordinate in nonsupport_coordinates
        if (channel := contract_coordinate(
            full8, coordinate, top_degree=8
        ))
    ]
    top_rank = exact_sparse_rank_minor(top_channels)
    require(len(top_channels) == top_rank["rank"] == 220
            and Fraction(*top_rank["minor_determinant"])
            == Fraction(-1, 2 ** 236),
            "new top contraction channels lost independence")

    # Coordinate orbit decomposition under the order-four chart stabilizer.
    coordinate_orbits = []
    seen = set()
    for coordinate in nonsupport_coordinates:
        if coordinate in seen:
            continue
        orbit = tuple(sorted(set(
            transform[coordinate]
            for transform in source.D5.VARIABLE_TRANSFORMS
        )))
        seen.update(orbit)
        require(set(orbit).issubset(nonsupport_coordinates),
                "coordinate orbit left the normalized variables")
        active_flags = {item in active_by_level[8] for item in orbit}
        require(len(active_flags) == 1, "activity is not stabilizer invariant")
        coordinate_orbits.append((orbit, active_flags.pop()))
    active_orbit_sizes = Counter(
        len(orbit) for orbit, active in coordinate_orbits if active
    )
    zero_orbit_sizes = Counter(
        len(orbit) for orbit, active in coordinate_orbits if not active
    )
    require(active_orbit_sizes == Counter({4: 49, 2: 12})
            and zero_orbit_sizes == Counter({4: 5}),
            "active coordinate-orbit census changed")

    # A literal kernel direction shows that the lift is not canonical.  The
    # row x_19^8 contains no four-edge mixed-generator term, so its orbit is
    # invisible to every bounded degree-eight source column and lies in
    # ker(rho_t).  Its four coordinate labels are absent from the displayed
    # top support, so this free change also raises the first Hankel rank.
    invisible_row = bytes([19]) * 8
    require(invisible_row == source.canonical_normalized_row(invisible_row)
            and invisible_row not in lambda8,
            "invisible counterguard row changed")
    invisible_orbit = source.normalized_row_orbit(invisible_row)
    require(len(invisible_orbit) == 4
            and all(not source.top_incident_columns(row)
                    for row in invisible_orbit)
            and not source.bounded_incident_columns(
                {invisible_row: Fraction(1)}, maximum_output_degree=8
            ), "invisible kernel direction acquired a source incidence")
    alternative8 = dict(lambda8)
    alternative8[invisible_row] = Fraction(1)
    full_alternative8 = expand_invariant(source, alternative8)
    alternative_rows = [
        ("t", contract_t(full_alternative8, 8))
    ] + [
        (f"x{coordinate}", channel)
        for coordinate in nonsupport_coordinates
        if (channel := contract_coordinate(full_alternative8, coordinate))
    ]
    alternative_hankel = exact_sparse_rank_minor(alternative_rows)
    require(len(alternative_rows) == alternative_hankel["rank"] == 225
            and Fraction(*alternative_hankel["minor_determinant"])
            == Fraction(-1, 2 ** 244),
            "invisible alternative Hankel counterguard changed")

    result = {
        "format": "n8-chart26-lambda7-lambda8-transfer-audit-v1",
        "status": "PASS exact transfer obstruction",
        "source_sha256": {
            str(path.relative_to(COMPUTATIONS.parent)): digest
            for path, digest in EXPECTED.items()
        },
        "degree7_dual_sha256": core["degree7_dual_sha256"],
        "degree8_dual_sha256": digest8,
        "multiplication_by_t": {
            "rho_t_lambda8_equals_lambda7": True,
            "invariant_lower_support": len(lambda7),
            "full_lower_support": len(full7),
            "target_pairing_both_levels": [1, 1],
        },
        "new_top_layer": {
            "invariant_row_orbits": len(top8),
            "actual_rows": len(actual_top8),
            "row_orbit_size_histogram": dict(sorted(orbit_sizes.items())),
            "coefficient_histogram": fraction_histogram(top8.values()),
            "variable_multiplicity_partitions":
                partition_histogram(variable_partitions),
            "edge_multiplicity_partitions":
                partition_histogram(edge_partitions),
            "site_degree_partitions": partition_histogram(site_partitions),
            "colour_endpoint_profiles": partition_histogram(colour_profiles),
            "combined_natural_profiles": len(profile_classes),
            "coefficient_ambiguous_profiles": len(ambiguous),
            "rows_in_coefficient_ambiguous_profiles":
                sum(map(len, ambiguous.values())),
            "explicit_profile_collision": {
                "profile": profile_record(collision_profile),
                "rows": [[row.hex(), *fraction_record(value)]
                         for row, value in collision],
            },
        },
        "parent_deletion_obstruction": {
            "actual_top_rows": len(actual_top8),
            "one_coordinate_deletions_within_rows": deletion_count,
            "distinct_one_coordinate_deletions": len(deletions),
            "deletions_meeting_lambda7_support": 0,
            "conclusion": (
                "no rowwise coordinate-multiplication rule from the support "
                "of lambda7 can produce any displayed top weight"
            ),
        },
        "first_homogeneous_catalecticants": hankel,
        "new_top_coordinate_channels": {
            "nonzero_channels": len(top_channels),
            **top_rank,
            "active_coordinate_orbit_size_histogram":
                dict(sorted(active_orbit_sizes.items())),
            "zero_coordinate_orbit_size_histogram":
                dict(sorted(zero_orbit_sizes.items())),
            "active_coordinates": [
                [coordinate, *source.D5.COORDINATES[coordinate]]
                for coordinate in sorted(active_by_level[8])
            ],
            "zero_coordinates": [
                [coordinate, *source.D5.COORDINATES[coordinate]]
                for coordinate in nonsupport_coordinates
                if coordinate not in active_by_level[8]
            ],
        },
        "nonuniqueness_counterguard": {
            "invisible_canonical_row_hex": invisible_row.hex(),
            "row_orbit_size": len(invisible_orbit),
            "bounded_incident_columns": 0,
            "rho_t_of_direction_is_zero": True,
            "displayed_first_catalecticant_rank": 221,
            "rank_after_adding_direction_with_weight_one":
                alternative_hankel["rank"],
            "alternative_minor_determinant":
                alternative_hankel["minor_determinant"],
            "alternative_pivot_record_sha256":
                alternative_hankel["pivot_record_sha256"],
            "conclusion": (
                "lambda8+c*delta is another compatible exact separator for "
                "every rational c; the displayed lift and its Hankel rank "
                "are not canonical"
            ),
        },
        "verdict": (
            "The exact pair gives one genuine lift rho_t(lambda8)=lambda7, "
            "but no scalar, rank-stable, profile-only, or rowwise induced "
            "recurrence. The first catalecticant rank grows 141 to 221 and "
            "the new layer contributes 220 independent source-labelled "
            "coordinate channels."
        ),
        "smallest_missing_statement": (
            "An all-k theorem still needs either an exact lift of lambda8 to "
            "D9, or a finite-dimensional source-labelled inverse-system "
            "module stable under all coordinate contractions together with "
            "a t-contraction right inverse preserving every mixed-generator "
            "annihilation relation and the target pairing."
        ),
        "scope_guard": (
            "No degree-nine incidence or solve is performed. Two compatible "
            "levels and the displayed counterguards do not rule out a larger "
            "finitely generated transfer module with new states."
        ),
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-lambda8", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate_lambda8)
    if args.check_results:
        canonical = json.loads(json.dumps(result, sort_keys=True))
        require(RESULTS_PATH.exists()
                and json.loads(RESULTS_PATH.read_text()) == canonical,
                "stored transfer result changed")
    if args.write_results:
        RESULTS_PATH.write_text(json.dumps(
            result, indent=2, sort_keys=True
        ) + "\n")
    print(result["status"])
    print(
        "restriction/top/actual=",
        result["multiplication_by_t"]["rho_t_lambda8_equals_lambda7"],
        result["new_top_layer"]["invariant_row_orbits"],
        result["new_top_layer"]["actual_rows"],
    )
    print(
        "first Hankel ranks=",
        result["first_homogeneous_catalecticants"]["7"]["rank"],
        result["first_homogeneous_catalecticants"]["8"]["rank"],
    )
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
