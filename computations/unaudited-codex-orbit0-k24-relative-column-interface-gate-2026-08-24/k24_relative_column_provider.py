#!/usr/bin/env python3
"""Exact natural-order full filtered vector for one multiplier-aware column orbit."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TOP_PROVIDER = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23/k24_factorized_gram_provider.py"
TOP_PROVIDER_SHA = "29075c59bdc72237c9e88cd8df360dfcb5184968c4824556032b437f8fb8112d"
VECTOR_HEADER = "K_degree\tcanonical_row_hex\trow_orbit_size\torbit_total_unit_multiplicity\tper_labelled_unit_multiplicity\tweighted_orbit_mass_numerator\tweighted_orbit_mass_denominator"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_provider():
    need(sha(TOP_PROVIDER) == TOP_PROVIDER_SHA, "top-provider hash")
    spec = importlib.util.spec_from_file_location("relative_k24_top_provider", TOP_PROVIDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P = load_provider()


@lru_cache(None)
def natural_column_orbit(column):
    return tuple(sorted({P.move_column(column, action) for action in P.H}))


@lru_cache(None)
def natural_canonical_column(column):
    return natural_column_orbit(column)[0]


def full_filtered_orbit_vector(column):
    """Return exact unit orbit-mass coordinates in K20, K22, K23, K24."""
    representative = natural_canonical_column(column)
    masses = Counter()
    literal_outputs = 0
    for moved in natural_column_orbit(representative):
        rows = P.D24.degree24_column_rows(moved)
        need(len(rows) == 105, "physical-perfect-matching term census")
        literal_outputs += len(rows)
        for row in rows:
            degree = P.D24.row_k_degree(row)
            need(degree in (20, 22, 23, 24), f"unexpected K degree {degree}")
            masses[(degree, P.canonical_row(row))] += 1
    vector = []
    for (degree, row), mass in sorted(masses.items()):
        orbit_size = len(P.row_orbit(row))
        need(mass % orbit_size == 0, "row-orbit divisibility")
        vector.append((degree, row, orbit_size, mass, mass // orbit_size))
    need(sum(item[3] for item in vector) == literal_outputs, "full vector mass")
    return representative, tuple(vector), literal_outputs


def write_vector(path, vector, coefficient):
    lines = [VECTOR_HEADER]
    for degree, row, orbit_size, mass, per_labelled in vector:
        weighted = coefficient * mass
        lines.append("\t".join((
            str(degree), row.hex(), str(orbit_size), str(mass), str(per_labelled),
            str(weighted.numerator), str(weighted.denominator),
        )))
    temporary = Path(str(path) + ".tmp")
    temporary.write_text("\n".join(lines) + "\n")
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--column-key", required=True)
    parser.add_argument("--coefficient-numerator", type=int, required=True)
    parser.add_argument("--coefficient-denominator", type=int, default=1)
    parser.add_argument("--vector-output", type=Path, required=True)
    parser.add_argument("--result-output", type=Path, required=True)
    args = parser.parse_args()
    need(args.coefficient_denominator > 0, "positive coefficient denominator")
    vector_output = args.vector_output if args.vector_output.is_absolute() else ROOT / args.vector_output
    result_output = args.result_output if args.result_output.is_absolute() else ROOT / args.result_output
    column = P.parse_column_key(args.column_key)
    need(len(column[0]) == 8 and len(set(column[0])) > 1 and len(column[1]) == 20, "literal degree-24 column")
    representative, vector, literal_outputs = full_filtered_orbit_vector(column)
    coefficient = Fraction(args.coefficient_numerator, args.coefficient_denominator)
    write_vector(vector_output, vector, coefficient)
    degree_coordinates = Counter()
    degree_unit_masses = Counter()
    degree_weighted_masses = Counter()
    for degree, _row, _size, mass, _per in vector:
        degree_coordinates[degree] += 1
        degree_unit_masses[degree] += mass
        degree_weighted_masses[degree] += coefficient * mass
    top_actual = tuple(item for item in vector if item[0] == 24)
    top_expected = tuple((24, row, size, mass, mass // size)
                         for row, mass, size in P.orbit_column_vector(column))
    need(top_actual == top_expected, "top vector differs from pinned factorized provider")
    natural = P.column_key(representative)
    repr_first = P.column_key(P.column_orbit(column)[0])
    result = {
        "status": "PASS_BOUNDED_K24_RELATIVE_COLUMN_FULL_VECTOR_CONTROL",
        "format": "orbit0-k24-relative-column-prefix-control-v1",
        "degree": 24,
        "canonical_order_id": "natural_word_tuple_then_multiplier_bytes_v1",
        "H_order": len(P.H),
        "input_column_key": args.column_key,
        "natural_canonical_column_key": natural,
        "provider_repr_first_column_key": repr_first,
        "natural_equals_provider_repr_first": natural == repr_first,
        "column_orbit_size": len(natural_column_orbit(column)),
        "coefficient": [coefficient.numerator, coefficient.denominator],
        "full_literal_outputs": literal_outputs,
        "degree_coordinate_counts": {str(key): value for key, value in sorted(degree_coordinates.items())},
        "degree_unit_orbit_masses": {str(key): value for key, value in sorted(degree_unit_masses.items())},
        "degree_weighted_orbit_masses": {str(key): [value.numerator, value.denominator] for key, value in sorted(degree_weighted_masses.items())},
        "lower_projection_nonzero": any(degree < 24 and mass for degree, _row, _size, mass, _per in vector),
        "top_projection_exactly_matches_factorized_provider": True,
        "raw_top_only_constructive_certificate_accepted": False,
        "vector_path": str(vector_output.relative_to(ROOT)),
        "vector_sha256": sha(vector_output),
        "provider_sha256": TOP_PROVIDER_SHA,
        "scope": "one literal column-orbit bounded control; no relative kernel, R24, production, membership, or charge claim",
    }
    temporary = Path(str(result_output) + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, result_output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
