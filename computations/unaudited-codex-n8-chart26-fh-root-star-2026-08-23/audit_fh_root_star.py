#!/usr/bin/env python3
"""Exact normalized degree-12 F^h root star and first killing cell."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_PATH = (ROOT / "computations" /
    "unaudited-codex-n8-normalized-dfs-degree7-2026-08-23" /
    "audit_degree8_dual_extension.py")
RESULT_PATH = HERE / "results_fh_root_star.json"
EXPECTED_SOURCE = "9df003b78c558a6ec2167651bcb06b98a9a86760c064dbae825e11085da40282"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_source():
    require(sha256(SOURCE_PATH.read_bytes()).hexdigest() == EXPECTED_SOURCE,
            "normalized source provider drifted")
    spec = importlib.util.spec_from_file_location("fh_root_source", SOURCE_PATH)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, str(SOURCE_PATH))
    spec.loader.exec_module(module)
    return module, module.load_d7()


def quotient_if_divides(target, factor):
    answer = bytearray()
    i = j = 0
    while i < len(target) and j < len(factor):
        if target[i] < factor[j]:
            answer.append(target[i])
            i += 1
        elif target[i] == factor[j]:
            i += 1
            j += 1
        else:
            return None
    if j != len(factor):
        return None
    answer.extend(target[i:])
    return bytes(answer)


def audit(mutate=False):
    source_api, source = load_source()
    pure_terms = tuple(tuple(sorted(
        source.normalized_generator(source.D5.word_code((colour,) * 8)).items(),
        key=lambda item: (len(item[0]), item[0])
    )) for colour in range(3))

    @lru_cache(None)
    def coefficient_fh(row, colours=(0, 1, 2)):
        if not colours:
            return int(not row)
        total = 0
        for term, coefficient in pure_terms[colours[0]]:
            if len(term) > len(row):
                break
            quotient = quotient_if_divides(row, term)
            if quotient is not None:
                total += coefficient * coefficient_fh(quotient, colours[1:])
        return total

    root = b""  # t^12 in the implicit homogenized-row encoding.
    root_columns = sorted(source.bounded_incident_columns(
        {root: Fraction(1)}, maximum_output_degree=12
    ))
    require(len(root_columns) == 1, "root column-orbit count changed")
    root_column = root_columns[0]
    root_entries = source_api.invariant_entries(source, root_column)
    require(len(root_entries) == 56
            and Counter(map(len, root_entries)) == Counter({0: 1, 2: 7, 3: 18, 4: 30})
            and root_entries[root] == 2,
            "root star changed")
    target_hits = {
        row: coefficient_fh(row) for row in root_entries if coefficient_fh(row)
    }
    require(target_hits == {b"": 1, bytes.fromhex("75c6"): 1},
            "F^h support intersection with root star changed")

    repair_row = bytes.fromhex("0576cc")
    require(root_entries[repair_row] == 1 and coefficient_fh(repair_row) == 0,
            "lex-first target-free repair row changed")
    witness = {root: Fraction(1), repair_row: Fraction(-2)}
    require(source_api.pairing(root_entries, witness) == 0,
            "two-row root witness stopped annihilating root column")
    target_pairing = sum(value * coefficient_fh(row)
                         for row, value in witness.items())
    require(target_pairing == 1, "two-row witness lost F^h pairing")

    incident = sorted(source.bounded_incident_columns(
        witness, maximum_output_degree=12
    ))
    violations = []
    for column in incident:
        entries = source_api.invariant_entries(source, column)
        value = source_api.pairing(entries, witness)
        if value:
            violations.append((column, value, entries))
    require(len(incident) == 10 and len(violations) == 9,
            "first witness boundary census changed")
    first_column, first_value, first_entries = violations[0]
    require(first_column == (5, bytes.fromhex("07"))
            and first_value == -2
            and first_entries.get(repair_row) == 1
            and root not in first_entries,
            "lex-first killing cell changed")

    if mutate:
        first_value += 1
    require(first_value == -2, "hostile killing-cell mutation survived")

    def coordinate_record(row):
        return [list(source.D5.COORDINATES[item]) for item in row]

    result = {
        "format": "n8-chart26-normalized-fh-root-star-v1",
        "status": "PASS local Fh dual; killed by explicit next incident cell",
        "source_sha256": {
            str(SOURCE_PATH.relative_to(ROOT)): EXPECTED_SOURCE,
        },
        "homogeneous_degree": 12,
        "implicit_root": {"row_hex": "", "meaning": "t^12", "Fh_coefficient": 1},
        "root_star": {
            "invariant_column_orbits": 1,
            "actual_column_orbit_size": len(source.normalized_column_orbit(root_column)),
            "word_code": root_column[0],
            "word": "".join(map(str, source.D5.decode_word(root_column[0]))),
            "multiplier_hex": root_column[1].hex(),
            "rows": len(root_entries),
            "row_degree_histogram": dict(sorted(Counter(map(len, root_entries)).items())),
            "root_coefficient": root_entries[root],
            "Fh_support_hits": [
                {"row_hex": row.hex(), "coordinates": coordinate_record(row),
                 "Fh_coefficient": coefficient}
                for row, coefficient in sorted(target_hits.items())
            ],
        },
        "smallest_local_target_dual": {
            "support": [
                {"row_hex": row.hex(), "coordinates": coordinate_record(row),
                 "weight": [value.numerator, value.denominator]}
                for row, value in sorted(witness.items())
            ],
            "root_column_pairing": [0, 1],
            "Fh_pairing": [1, 1],
        },
        "first_incident_boundary": {
            "incident_column_orbits": len(incident),
            "violating_column_orbits": len(violations),
            "lex_first_killing_cell": {
                "word_code": first_column[0],
                "word": "".join(map(str, source.D5.decode_word(first_column[0]))),
                "multiplier_hex": first_column[1].hex(),
                "multiplier_coordinates": coordinate_record(first_column[1]),
                "actual_column_orbit": [
                    {"word": "".join(map(str, source.D5.decode_word(code))),
                     "multiplier_hex": multiplier.hex()}
                    for code, multiplier in source.normalized_column_orbit(first_column)
                ],
                "witness_pairing": [first_value.numerator, first_value.denominator],
                "overlap_row_hex": repair_row.hex(),
                "overlap_coefficient": first_entries[repair_row],
            },
        },
        "verdict": (
            "The first normalized degree-12 root star has a two-row exact "
            "functional pairing 1 with the actual F^h target, but it is not "
            "closed: the literal word 00000012 with multiplier x_01^(2,1) "
            "pairs -2.  This is the first required repair cell."
        ),
        "scope_guard": (
            "Only the root star and the complete incident scan of this selected "
            "two-row functional are audited.  The 9 violating orbit columns "
            "are not closed, so this is neither F^h membership nor "
            "nonmembership in the full homogeneous mixed ideal."
        ),
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return json.loads(json.dumps(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.check_results:
        require(RESULT_PATH.exists()
                and json.loads(RESULT_PATH.read_text()) == result,
                "stored result changed")
    if args.write_results:
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("root rows/incident/violating=", result["root_star"]["rows"],
          result["first_incident_boundary"]["incident_column_orbits"],
          result["first_incident_boundary"]["violating_column_orbits"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
