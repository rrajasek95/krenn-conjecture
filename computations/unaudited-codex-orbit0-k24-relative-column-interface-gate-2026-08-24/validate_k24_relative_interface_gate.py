#!/usr/bin/env python3
"""Fail-closed schema and bounded-control validator for A24_rel."""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCHEMA = HERE / "k24_relative_column_certificate.schema.json"
CONTROL = HERE / "results_k24_relative_column_prefix_control.json"
VECTOR = HERE / "prefix_control_full_vector.tsv"
WITNESSES = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/prefix1/literal_witnesses.tsv"
SUFFICIENCY = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-logical-sufficiency-referee-2026-08-24/results_k24_factorized_logical_sufficiency_referee.json"
PROVIDER = HERE / "k24_relative_column_provider.py"
PINS = {
    ROOT / "computations/unaudited-codex-orbit0-k24-availability-schedule-2026-08-24/k24_expected_scalar_groups.json": "9ee7c5b6c31b70a7e06f8a4909c8b9aa77a87444cb12992c9971b5259bb8a986",
    WITNESSES: "477b9ae9249b72d2e1c9ba4c71fd5b63605866ce533c6c79eb199b8103dd001c",
    SUFFICIENCY: "eef90f74da0a478214035fcbd6f5b1932ebc246ef2bd047781a4286523ab3e6f",
    ROOT / "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23/k24_factorized_gram_provider.py": "29075c59bdc72237c9e88cd8df360dfcb5184968c4824556032b437f8fb8112d",
    ROOT / "computations/unaudited-codex-orbit0-k16-lower-kernel-hpl-2026-08-23/audit_k16_lower_kernel_component.py": "a2a7ed51a76e274b39973484cf47375e4a6e148c760fdb3db811161bdeb0e132",
    ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/audit_orbit0_t2_pivot_setup.py": "71111eabf3822bc08678f19de0b1faf3fb61af12dd5e36acf04313de56bf7e8b",
}
HEADER = "K_degree\tcanonical_row_hex\trow_orbit_size\torbit_total_unit_multiplicity\tper_labelled_unit_multiplicity\tweighted_orbit_mass_numerator\tweighted_orbit_mass_denominator"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_vector(path):
    lines = path.read_text().splitlines()
    need(lines and lines[0] == HEADER, "vector header")
    rows = []
    previous = None
    for line in lines[1:]:
        fields = line.split("\t")
        need(len(fields) == 7, "vector field count")
        degree = int(fields[0])
        row = bytes.fromhex(fields[1])
        orbit_size, mass, per = map(int, fields[2:5])
        weighted = Fraction(int(fields[5]), int(fields[6]))
        key = (degree, row)
        need(previous is None or previous < key, "vector strict sorting")
        previous = key
        need(degree in (20, 22, 23, 24) and len(row) == 24, "vector row grade")
        need(orbit_size > 0 and mass > 0 and mass % orbit_size == 0 and per == mass // orbit_size, "vector orbit division")
        need(weighted == -128 * mass, "bounded coefficient application")
        rows.append((degree, row, orbit_size, mass, per))
    return rows


def validate(control):
    need(control["status"] == "PASS_BOUNDED_K24_RELATIVE_COLUMN_FULL_VECTOR_CONTROL", "control status")
    need(control["canonical_order_id"] == "natural_word_tuple_then_multiplier_bytes_v1" and control["H_order"] == 384, "natural H convention")
    need(control["input_column_key"] == control["natural_canonical_column_key"], "natural canonical key")
    need(control["natural_equals_provider_repr_first"] is False and control["provider_repr_first_column_key"] != control["natural_canonical_column_key"], "repr hostile control")
    need(control["coefficient"] == [-128, 1] and control["column_orbit_size"] == 384, "coefficient/orbit")
    need(control["full_literal_outputs"] == 40_320, "full output census")
    need(control["degree_coordinate_counts"] == {"20": 1, "22": 12, "23": 32, "24": 60}, "degree coordinate census")
    need(control["degree_unit_orbit_masses"] == {"20": 384, "22": 4608, "23": 12288, "24": 23040}, "degree unit masses")
    need(control["degree_weighted_orbit_masses"] == {"20": [-49152, 1], "22": [-589824, 1], "23": [-1572864, 1], "24": [-2949120, 1]}, "degree weighted masses")
    need(control["lower_projection_nonzero"] is True, "load-bearing lower support")
    need(control["top_projection_exactly_matches_factorized_provider"] is True, "top compatibility")
    need(control["raw_top_only_constructive_certificate_accepted"] is False, "raw-top rejection")
    need(sha(VECTOR) == control["vector_sha256"], "vector content hash")
    rows = parse_vector(VECTOR)
    counts = Counter(degree for degree, *_rest in rows)
    masses = Counter()
    for degree, _row, _size, mass, _per in rows:
        masses[degree] += mass
    need({str(key): value for key, value in sorted(counts.items())} == control["degree_coordinate_counts"], "coordinate recount")
    need({str(key): value for key, value in sorted(masses.items())} == control["degree_unit_orbit_masses"], "mass recount")
    witness_lines = WITNESSES.read_text().splitlines()
    need(len(witness_lines) == 258, "witness census")
    fields = witness_lines[1].split("\t")
    need(fields[14] == control["input_column_key"] and [int(fields[17]), int(fields[18])] == control["coefficient"], "source witness pin")
    return rows


def validate_schema():
    schema = json.loads(SCHEMA.read_text())
    need(schema["$id"] == "orbit0-k24-relative-column-certificate-v1" and schema["additionalProperties"] is False, "schema identity/closed shape")
    theorem = schema["x-exact-theorem"]
    need(theorem["relative_operator"] == "A24_rel=T|ker(L)", "schema theorem")
    need("Lx=0" in theorem["explicit_certificate"] and "Tx=R24" in theorem["explicit_certificate"], "explicit certificate equations")
    need("rank equality" in theorem["gram_certificate"] and "exact norm" in theorem["gram_certificate"], "relative Gram condition")
    need("must be rejected" in theorem["raw_top_guard"], "raw top guard")
    retention = schema["x-retention-contract"]
    need(len(retention) == 8 and any("K20 cancellation ledger" in item for item in retention), "K20 retention")
    need(any("lower-only correction" in item for item in retention), "correction retention")
    need(any("never publish" in item for item in retention), "capped closure rejection")
    source_required = schema["$defs"]["source_pins"]["required"]
    need("expected_35_contract_sha256" in source_required, "35-ID contract pin")
    coverage_required = schema["$defs"]["coverage"]["required"]
    need("covered_ids" in coverage_required and "covered_ids_sha256" in coverage_required, "literal 35-ID set retention")


def full_replay(expected_rows):
    spec = importlib.util.spec_from_file_location("relative_prefix_full_replay", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    column = module.P.parse_column_key(json.loads(CONTROL.read_text())["input_column_key"])
    representative, rows, literal_outputs = module.full_filtered_orbit_vector(column)
    need(module.P.column_key(representative) == json.loads(CONTROL.read_text())["natural_canonical_column_key"], "full replay representative")
    need(list(rows) == expected_rows and literal_outputs == 40_320, "full replay vector")


def hostile_self_test(control):
    mutations = []
    bad = copy.deepcopy(control); bad["raw_top_only_constructive_certificate_accepted"] = True; mutations.append(bad)
    bad = copy.deepcopy(control); bad["lower_projection_nonzero"] = False; mutations.append(bad)
    bad = copy.deepcopy(control); bad["natural_canonical_column_key"] = bad["provider_repr_first_column_key"]; mutations.append(bad)
    bad = copy.deepcopy(control); bad["vector_sha256"] = "0" * 64; mutations.append(bad)
    rejected = 0
    for bad in mutations:
        try:
            validate(bad)
        except ValueError:
            rejected += 1
        else:
            need(False, "hostile mutation accepted")
    need(rejected == 4, "hostile rejection count")
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-prefix-replay", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "results_k24_relative_interface_gate_audit.json")
    args = parser.parse_args()
    for path, digest in PINS.items():
        need(path.is_file() and sha(path) == digest, f"source pin {path}")
    validate_schema()
    control = json.loads(CONTROL.read_text())
    rows = validate(control)
    rejected = hostile_self_test(control)
    if args.full_prefix_replay:
        full_replay(rows)
    audit = {
        "status": "PASS_K24_RELATIVE_COLUMN_INTERFACE_BOUNDED_GATE",
        "relative_operator": "A24_rel=T|ker(L)",
        "schema_sha256": sha(SCHEMA),
        "provider_sha256": sha(PROVIDER),
        "control_sha256": sha(CONTROL),
        "vector_sha256": sha(VECTOR),
        "source_pins_rehashed": len(PINS),
        "vector_coordinates_replayed": len(rows),
        "full_prefix_provider_replay": args.full_prefix_replay,
        "hostile_mutations_rejected": rejected,
        "raw_top_only_rejected_for_nonzero_lower_projection": True,
        "natural_repr_mismatch_guarded": True,
        "production_launched": False,
        "scope": "schema/theorem and one-column bounded control only; no relative kernel, R24, membership, charge, or heavy production",
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(audit, sort_keys=True))


if __name__ == "__main__":
    main()
