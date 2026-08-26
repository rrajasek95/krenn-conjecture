#!/usr/bin/env python3
"""Referee the D12 C10/Fh implication and expose the first D13 boundary."""

from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL_PATH = ROOT / "computations/unaudited-codex-n8-degree12-full-dual-2026-08-23/audit_degree12_full_dual.py"
FULL_RESULT = FULL_PATH.with_name("results_degree12_full_dual_fixed_c10.json")
WITNESS = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_c10_constant_provider_kernel.json"
EXPORT_PATH = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/export_full_direct_residual_through10.py"
RESULT = HERE / "results_degree13_full_dual_referee.json"
TIME_CAP = 300.0


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


FULL = load(FULL_PATH, "d13_referee_full")
EXPORT = load(EXPORT_PATH, "d13_referee_export")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    started = time.monotonic()
    authority = json.loads(FULL_RESULT.read_text())
    require(authority["logical_sha256"] == "cde136aef242841bc78bc9b7da8e56323ab0b273bb637a30253902e9b2729aed",
            "D12 functional authority changed")
    functional = {bytes.fromhex(row): Fraction(numerator, denominator)
                  for row, numerator, denominator in authority["functional_rows"]}
    require(Counter(map(len, functional)) == {10: 1, 11: 3, 12: 16},
            "D12 functional profile changed")

    helpers = FULL.D12.D11_HELPERS.D10_HELPERS
    base = helpers.load(helpers.D8_BASE_PATH, "d13_referee_base")
    source = base.load_source()
    originals, _ = source.FIRST.original_basis()
    term_sources = base.make_term_sources(originals)
    top_sources = defaultdict(list)
    for code, polynomial in originals.items():
        for term, coefficient in polynomial.items():
            if len(term) == 4:
                top_sources[term].append((code, coefficient))

    # Independent D12 ideal replay and the explicit 90-column guard.
    incident12 = FULL.incident_all(functional, 12, term_sources, base)
    bad12 = {column: FULL.column_value(functional, *column, originals)
             for column in incident12}
    require(not {column: value for column, value in bad12.items() if value},
            "functional misses a D12 ideal column")
    witness = json.loads(WITNESS.read_text())["lex_smallest_minimal_column_witness"]
    witness_by_degree = defaultdict(Fraction)
    individual_pairings = []
    for record in witness["source_columns"]:
        code = int(record["code"])
        multiplier = bytes.fromhex(record["multiplier_y"])
        scalar = int(record["coefficient"])
        pairing = Fraction()
        for term, coefficient in originals[code].items():
            row = bytes(sorted(multiplier + term))
            contribution = functional.get(row, 0) * scalar * coefficient
            witness_by_degree[len(row)] += contribution
            pairing += contribution
        individual_pairings.append(pairing)
    require(len(individual_pairings) == 90 and all(value == 0 for value in individual_pairings),
            "90-column witness escaped the ideal dual")
    require(witness_by_degree[10] == 1 and witness_by_degree[11] == -1
            and sum(witness_by_degree.values(), Fraction()) == 0,
            "90-column filtration cancellation changed")

    # Direct Fh pairing: this is the decisive congruence referee.
    cache = {}
    def generator(code):
        if code not in cache:
            cache[code] = EXPORT.normalized_generator(code)
        return cache[code]
    pure = [generator(EXPORT.D5.word_code((colour,) * 8)) for colour in range(3)]
    target = EXPORT.truncated_product(pure, 12)
    target_hits = {row: target[row] for row in functional if target.get(row)}
    target_pairing = sum((functional[row] * coefficient
                          for row, coefficient in target_hits.items()), Fraction())
    require(len(target) == 1_157_625 and not target_hits and target_pairing == 0,
            "direct Fh pairing changed")
    require(authority["fixed_c10_evaluation"]["pairing"] == -4,
            "fixed C10 pairing changed")

    # D13 initial boundary. Positive-t columns are inherited; primitive nonic
    # multipliers are the only new columns.
    primitive = FULL.incident_primitive(functional, 13, term_sources, base)
    primitive_values = {column: FULL.column_value(functional, *column, originals)
                        for column in primitive}
    crossing = {column for column, value in primitive_values.items() if value}
    all_incident13 = FULL.incident_all(functional, 13, term_sources, base)
    all_values13 = {column: FULL.column_value(functional, *column, originals)
                    for column in all_incident13}
    all_crossing13 = {column for column, value in all_values13.items() if value}
    require(all_crossing13 == crossing,
            "a positive-t D13 column crossed the inherited functional")

    top_rows = set()
    for code, multiplier in crossing:
        for term, coefficient in originals[code].items():
            if len(term) == 4:
                require(coefficient != 0, "zero top coefficient")
                top_rows.add(bytes(sorted(term + multiplier)))
    row_to_columns = defaultdict(dict)
    column_to_rows = defaultdict(set)
    for row in sorted(top_rows):
        for term in base.divisors(row, 4):
            multiplier = base.quotient(row, term)
            require(len(multiplier) == 9, "D13 owner multiplier changed")
            for code, coefficient in top_sources.get(term, ()):
                column = (code, multiplier)
                row_to_columns[row][column] = Fraction(coefficient)
                column_to_rows[column].add(row)
        require(time.monotonic() - started < TIME_CAP, "D13 cap")
    require(crossing <= set(column_to_rows), "crossing lost top owner")
    pivots, residual = FULL.weighted_singleton_peel(column_to_rows, row_to_columns)
    residual_crossing = residual & crossing
    require(residual_crossing, "D13 unexpectedly private-repaired completely")

    # Exact connected component of the lex-first surviving crossing.
    seed = min(residual_crossing)
    component_columns = {seed}
    component_rows = set()
    queue = deque([seed])
    while queue:
        column = queue.popleft()
        for row in column_to_rows[column]:
            if row in component_rows:
                continue
            component_rows.add(row)
            for owner in row_to_columns[row]:
                if owner in residual and owner not in component_columns:
                    component_columns.add(owner)
                    queue.append(owner)
    component_crossing = component_columns & crossing

    def column_record(column):
        code, multiplier = column
        value = primitive_values.get(column, Fraction())
        return {
            "code": code,
            "word": list(source.D5.decode_word(code)),
            "multiplier_y9": multiplier.hex(),
            "lambda_pairing": [value.numerator, value.denominator],
        }

    payload = {
        "format": "n8-degree13-full-dual-scope-referee-v1",
        "status": "D12_FH_UPGRADE_FALSE_D13_CROSSING_CORE",
        "d12_referee": {
            "complete_incident_ideal_columns": len(incident12),
            "nonzero_ideal_column_pairings": 0,
            "witness_source_columns": 90,
            "witness_individual_nonzero_pairings": 0,
            "witness_pairing_by_y_degree": {
                str(degree): [value.numerator, value.denominator]
                for degree, value in sorted(witness_by_degree.items()) if value
            },
            "witness_total_pairing": [0, 1],
            "fixed_c10_pairing": -4,
            "normalized_Fh_terms": len(target),
            "functional_support_rows_occurring_in_Fh": len(target_hits),
            "normalized_Fh_pairing": [0, 1],
            "logical_implication": (
                "The functional is invariant under every homogeneous D12 source-image/right-inverse change, "
                "but C10 alone is not congruent to Fh modulo the ideal: their pairings are -4 and 0. "
                "The omitted y11/y12 part of the actual post-correction residual must pair by +4."
            ),
        },
        "d13_initial_boundary": {
            "all_incident_columns": len(all_incident13),
            "primitive_nonic_incident_columns": len(primitive),
            "crossing_columns": len(crossing),
            "positive_t_crossing_columns": len(all_crossing13 - primitive),
            "top_rows": len(top_rows),
            "owner_columns": len(column_to_rows),
            "singleton_pivots": len(pivots),
            "crossings_private_repaired": len(crossing - residual),
            "residual_columns": len(residual),
            "residual_crossing_columns": len(residual_crossing),
            "residual_crossings": [column_record(column)
                                   for column in sorted(residual_crossing)],
            "first_core": {
                "seed": column_record(seed),
                "columns": len(component_columns),
                "rows": len(component_rows),
                "crossing_columns": len(component_crossing),
                "crossings": [column_record(column)
                              for column in sorted(component_crossing)],
            },
            "verdict": (
                "The inherited t*lambda12 boundary is not removable by the audited private-top-row "
                "triangular repair: 27 crossings survive in a genuine owner core. This does not prove "
                "that no D13 extension exists; a coupled solve on the core would be required."
            ),
        },
        "scope": (
            "Exact normalized orbit26 chart. The D12 conclusion refutes only the Fh scope inflation; "
            "the fixed-C10 and monomial dual remain valid. D13 is an initial owner/peel boundary only; "
            "no D13 nonmembership, t-saturation, D14, or global inference."
        ),
        "source_sha256": {
            str(FULL_RESULT.relative_to(ROOT)): sha256(FULL_RESULT.read_bytes()).hexdigest(),
            str(WITNESS.relative_to(ROOT)): sha256(WITNESS.read_bytes()).hexdigest(),
            str(EXPORT_PATH.relative_to(ROOT)): sha256(EXPORT_PATH.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
