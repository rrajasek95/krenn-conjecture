#!/usr/bin/env python3
"""Construct an exact full degree-12 separator and evaluate fixed C10.

The separator is built filtration-first.  Delta at y10 is a degree-10
separator.  At D=11 and D=12, every new t-free-multiplier column crossing
the lifted separator is corrected by a top-y private-row functional.  All
positive-t multiplier columns are inherited from the preceding degree.

The fixed C10 pairing is evaluated coefficient-first from its exact factored
straight-line circuit; this is equivalent to streaming all 142,520,100
emitted contributions, but retains only the separator's y10 support.
"""

from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D12_PATH = (
    ROOT / "computations/unaudited-codex-n8-y10-degree12-seeds-2026-08-23"
    / "audit_degree12_restricted.py"
)
FACTORED_PATH = (
    ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
    / "audit_factored_y10_transfer.py"
)
ARTIFACT = (
    ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
)
AGGREGATE = ARTIFACT / "results_full_y10_aggregate.json"
RESULTS = HERE / "results_degree12_full_dual_fixed_c10.json"
TIME_CAP_SECONDS = 300.0
RSS_CAP_BYTES = 12 * 1024 ** 3
EXPECTED_LOGICAL_SHA256 = (
    "cde136aef242841bc78bc9b7da8e56323ab0b273bb637a30253902e9b2729aed"
)
EXPECTED_RESIDUAL_SHA256 = {
    "R6": "234edf92012e289fab8b5e98dfb73148985755ca2eafa200b0f71c1886ace456",
    "R7": "08165ec117f204048c8e1f1c676da54c0e18eb0815899c0facf6a887b5e6a840",
    "R8": "88baac36e9e2ef8b1797c725c5b8fe4dab2309d44d5fe744fc310266428381ef",
    "R9": "40cb703326dd0499013d2b190a1f32cd296d8433397d44ca7c57a56c7233c75c",
    "R10": "256d2385ef781aa8af76221620d3128cb49dc14e7418ee967ca0775ad1972ec8",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D12 = load(D12_PATH, "n8_full_dual_d12_authority")
FACTORED = load(FACTORED_PATH, "n8_full_dual_factored_source")


def add_fraction(vector, key, value):
    value = vector.get(key, Fraction(0)) + value
    if value:
        vector[key] = value
    else:
        vector.pop(key, None)


def column_value(functional, code, multiplier, originals):
    value = Fraction(0)
    for term, coefficient in originals[code].items():
        row = bytes(sorted(term + multiplier))
        value += functional.get(row, 0) * coefficient
    return value


def incident_primitive(functional, total_degree, term_sources, base):
    multiplier_degree = total_degree - 4
    columns = set()
    for row in functional:
        term_degree = len(row) - multiplier_degree
        if not 0 <= term_degree <= 4:
            continue
        for term in base.divisors(row, term_degree):
            multiplier = base.quotient(row, term)
            require(len(multiplier) == multiplier_degree,
                    "primitive inverse incidence changed multiplier degree")
            for code in term_sources.get(term, ()):
                columns.add((code, multiplier))
    return columns


def incident_all(functional, total_degree, term_sources, base):
    """Every total-degree-D original column touching functional support."""
    multiplier_total_degree = total_degree - 4
    columns = set()
    for row in functional:
        minimum_term_degree = max(0, len(row) - multiplier_total_degree)
        for term_degree in range(minimum_term_degree, min(4, len(row)) + 1):
            for term in base.divisors(row, term_degree):
                multiplier = base.quotient(row, term)
                if len(multiplier) > multiplier_total_degree:
                    continue
                for code in term_sources.get(term, ()):
                    columns.add((code, multiplier))
    return columns


def weighted_singleton_peel(column_to_rows, row_to_columns):
    active = set(column_to_rows)
    queue = deque(sorted(
        row for row, owners in row_to_columns.items() if len(owners) == 1
    ))
    pivots = []
    while queue:
        row = queue.popleft()
        owners = set(row_to_columns[row]) & active
        if len(owners) != 1:
            continue
        column = next(iter(owners))
        active.remove(column)
        pivots.append((column, row))
        for touched in column_to_rows[column]:
            if len(set(row_to_columns[touched]) & active) == 1:
                queue.append(touched)
    return pivots, active


def extend_separator(functional, total_degree, originals, term_sources,
                     top_sources, base, check_cap):
    incident = incident_primitive(
        functional, total_degree, term_sources, base
    )
    values = {
        column: column_value(functional, *column, originals)
        for column in incident
    }
    crossing = {column for column, value in values.items() if value}

    rows = set()
    for code, multiplier in crossing:
        for term, coefficient in originals[code].items():
            if len(term) == 4:
                require(coefficient != 0, "a top crossing coefficient vanished")
                rows.add(bytes(sorted(term + multiplier)))

    row_to_columns = defaultdict(dict)
    column_to_rows = defaultdict(set)
    for row_index, row in enumerate(sorted(rows), 1):
        for term in base.divisors(row, 4):
            owners = top_sources.get(term, ())
            if not owners:
                continue
            multiplier = base.quotient(row, term)
            require(len(multiplier) == total_degree - 4,
                    "top owner multiplier degree changed")
            for code, coefficient in owners:
                column = (code, multiplier)
                require(column not in row_to_columns[row],
                        "one column acquired duplicate top ownership")
                row_to_columns[row][column] = Fraction(coefficient)
                column_to_rows[column].add(row)
        if row_index % 128 == 0:
            check_cap(f"D{total_degree}_owner_rows_{row_index}")
    require(crossing <= set(column_to_rows),
            "a crossing column disappeared from its top rows")

    pivots, residual = weighted_singleton_peel(
        column_to_rows, row_to_columns
    )
    residual_crossing = residual & crossing
    if residual_crossing:
        return None, {
            "status": f"D{total_degree}_CROSSING_CORE",
            "incident_primitive_columns": len(incident),
            "crossing_columns": len(crossing),
            "top_rows": len(rows),
            "owner_columns": len(column_to_rows),
            "singleton_pivots": len(pivots),
            "residual_columns": len(residual),
            "residual_crossing_columns": [
                [code, multiplier.hex()]
                for code, multiplier in sorted(residual_crossing)
            ],
        }

    desired = {
        column: -column_value(functional, *column, originals)
        for column in column_to_rows
    }
    achieved = defaultdict(Fraction)
    correction = {}
    for column, row in reversed(pivots):
        pivot = row_to_columns[row][column]
        value = (desired[column] - achieved[column]) / pivot
        if value:
            require(row not in correction, "a pivot row was reused")
            correction[row] = value
            for owner, coefficient in row_to_columns[row].items():
                achieved[owner] += value * coefficient
    require(all(achieved[column] == desired[column]
                for column in column_to_rows),
            "reverse triangular solve did not realize the desired crossings")

    extended = dict(functional)
    for row, value in correction.items():
        require(len(row) == total_degree,
                "a top correction row has the wrong y degree")
        add_fraction(extended, row, value)
    replay_incident = incident_primitive(
        extended, total_degree, term_sources, base
    )
    replay_values = {
        column: column_value(extended, *column, originals)
        for column in replay_incident
    }
    require(not {column: value for column, value in replay_values.items() if value},
            "the extended separator misses a primitive incident column")
    return extended, {
        "status": f"D{total_degree}_EXACT_EXTENSION",
        "input_functional_support": len(functional),
        "incident_primitive_columns": len(incident),
        "crossing_columns": len(crossing),
        "top_rows": len(rows),
        "owner_columns": len(column_to_rows),
        "singleton_pivots": len(pivots),
        "residual_columns": len(residual),
        "residual_crossing_columns": 0,
        "correction_support": len(correction),
        "output_functional_support": len(extended),
        "exhaustive_replay_incident_columns": len(replay_incident),
        "exhaustive_replay_nonzero_columns": 0,
    }


def quotient(row, divisor):
    answer = list(row)
    for value in divisor:
        if value not in answer:
            return None
        answer.remove(value)
    return bytes(answer)


def residual_queries(path, expected_degree, query_weights):
    """Stream a residual packet and pair it with a sparse query functional."""
    value = 0
    count = 0
    expected = None
    with path.open(encoding="ascii") as source:
        for line_number, line in enumerate(source):
            fields = line.split()
            if line_number == 0:
                require(fields[1:4] == ["SCALE", "4", "COUNT"],
                        "residual header changed")
                expected = int(fields[4])
                continue
            require(len(fields) == 3 and fields[0] == "ROW",
                    "malformed residual row")
            row = bytes.fromhex(fields[1])
            require(len(row) == expected_degree, "residual y degree changed")
            coefficient = int(fields[2])
            value += query_weights.get(row, 0) * coefficient
            count += 1
    require(count == expected, "residual row count changed")
    return value, count


def evaluate_fixed_c10(target):
    _constant_code, constant, _linear_code, quadratic = FACTORED.parse_provider()
    s3, s4 = FACTORED.build_kernels(constant, quadratic)

    def convolution_queries(kernel, sign):
        queries = defaultdict(int)
        for term, coefficient in kernel.items():
            row = quotient(target, term)
            if row is not None:
                queries[row] += sign * coefficient
        return dict(queries)

    q10 = {target: 1}
    q8 = convolution_queries(constant[2], -1)
    q7 = convolution_queries(s3, 1)
    q6 = convolution_queries(s4, 1)
    parts = {}
    counts = {}
    for degree, query in ((10, q10), (8, q8), (7, q7), (6, q6)):
        value, count = residual_queries(
            ARTIFACT / f"direct_fh_original_y{degree}_residual.txt",
            degree, query,
        )
        parts[f"R{degree}"] = value
        counts[f"R{degree}"] = count

    # L(R9): source implementation takes the first cell x of each sorted R9
    # row, removes it, and emits -coefficient*(quotient*q2_x).
    l_value = 0
    r9_count = 0
    r9_path = ARTIFACT / "direct_fh_original_y9_residual.txt"
    with r9_path.open(encoding="ascii") as source:
        expected = None
        for line_number, line in enumerate(source):
            fields = line.split()
            if line_number == 0:
                require(fields[1:4] == ["SCALE", "4", "COUNT"],
                        "R9 header changed")
                expected = int(fields[4])
                continue
            require(len(fields) == 3 and fields[0] == "ROW", "malformed R9 row")
            row = bytes.fromhex(fields[1])
            require(len(row) == 9, "R9 y degree changed")
            coefficient = int(fields[2])
            cell, rest = row[0], row[1:]
            for term, term_coefficient in quadratic[cell].items():
                if bytes(sorted(rest + term)) == target:
                    l_value -= coefficient * term_coefficient
            r9_count += 1
    require(r9_count == expected, "R9 row count changed")
    parts["L(R9)"] = l_value
    counts["R9"] = r9_count
    residual_sha256 = {
        f"R{degree}": sha256((
            ARTIFACT / f"direct_fh_original_y{degree}_residual.txt"
        ).read_bytes()).hexdigest()
        for degree in (6, 7, 8, 9, 10)
    }
    require(residual_sha256 == EXPECTED_RESIDUAL_SHA256,
            "a fixed C10 residual input packet changed")
    return {
        "formula_parts": parts,
        "pairing": sum(parts.values()),
        "streamed_residual_row_counts": counts,
        "residual_packet_sha256": residual_sha256,
        "equivalent_emitted_contributions": 142_520_100,
        "method": (
            "coefficient-first exact streaming of the factored circuit; only "
            "kernel terms dividing the functional's sole y10 support row are "
            "retained, algebraically equivalent to scanning every emission"
        ),
    }


def fraction_record(value):
    return [value.numerator, value.denominator]


def audit():
    started = time.monotonic()
    d12 = D12.audit()
    require(d12["status"] == "EXACT_MONOMIAL_NONMEMBERSHIP_AT_TOTAL_D12"
            and d12["logical_sha256"]
            == "8030714e1f1edaa844664c893bb28f6574e32cca7d3e88a3e1379cfc25d541bd",
            "the frozen degree-twelve monomial authority changed")
    d10_helpers = D12.D11_HELPERS.D10_HELPERS

    def check_cap(label):
        elapsed = time.monotonic() - started
        rss = d10_helpers.peak_rss_bytes()
        if elapsed > TIME_CAP_SECONDS or rss > RSS_CAP_BYTES:
            raise d10_helpers.BoundedStop({
                "label": label, "elapsed_seconds": elapsed,
                "peak_rss_bytes": rss,
            })

    base = d10_helpers.load(d10_helpers.D8_BASE_PATH, "n8_full_dual_base")
    source = base.load_source()
    originals, _leads = source.FIRST.original_basis()
    term_sources = base.make_term_sources(originals)
    top_sources = defaultdict(list)
    for code, polynomial in originals.items():
        for term, coefficient in polynomial.items():
            if len(term) == 4:
                top_sources[term].append((code, coefficient))
    target = base.TARGET

    functional = {target: Fraction(1)}
    # At total degree ten, no original column contains the t-free target row.
    require(not incident_primitive(functional, 10, term_sources, base),
            "the base delta functional acquired a degree-ten incident column")
    stages = []
    for total_degree in (11, 12):
        functional, stage = extend_separator(
            functional, total_degree, originals, term_sources,
            top_sources, base, check_cap,
        )
        stages.append(stage)
        if functional is None:
            return {
                "status": "BOUNDED_EXACT_CROSSING_CORE_UNRESOLVED",
                "terminal_stage": stage,
                "scope": "no full-C10 membership or saturation inference",
            }
        all_incident = incident_all(
            functional, total_degree, term_sources, base
        )
        all_values = {
            column: column_value(functional, *column, originals)
            for column in all_incident
        }
        require(not {column: value for column, value in all_values.items() if value},
                f"the D{total_degree} functional misses a full incident column")
        stage["exhaustive_all_incident_columns"] = len(all_incident)
        stage["exhaustive_all_nonzero_columns"] = 0
        check_cap(f"extended_D{total_degree}")

    require(functional.get(target) == 1,
            "the full separator lost unit target pairing")
    y_degree_histogram = Counter(map(len, functional))
    require(set(y_degree_histogram) <= {10, 11, 12},
            "the separator escaped the filtration construction")
    evaluation = evaluate_fixed_c10(target)
    require(evaluation["pairing"] != 0,
            "the full separator cancels on the fixed C10 residual")
    aggregate = json.loads(AGGREGATE.read_text())
    require(aggregate["logical_sha256"]
            == "3dd16ca8793cb5b435700fb90773dd1c4dae5a4b9166034feaef944740ffa75d",
            "the independently aggregated full C10 result changed")
    require(aggregate["PM4_incidence"]["lex_dead_row"] == target.hex()
            and aggregate["PM4_incidence"]["lex_dead_coefficient"]
            == evaluation["pairing"],
            "coefficient-first pairing disagrees with full aggregation")
    require((len(functional), dict(sorted(y_degree_histogram.items())))
            == (20, {10: 1, 11: 3, 12: 16}),
            "the full separator support profile changed")
    require(stages[0]["exhaustive_all_incident_columns"] == 3
            and stages[1]["exhaustive_all_incident_columns"] == 22,
            "the exhaustive full-column replay census changed")
    require(evaluation["formula_parts"]
            == {"R10": 0, "R8": 0, "R7": 0, "R6": -4, "L(R9)": 0},
            "the fixed C10 factor pairing decomposition changed")
    check_cap("fixed_C10_evaluation")

    functional_rows = [
        [row.hex(), *fraction_record(value)]
        for row, value in sorted(functional.items())
    ]
    payload = {
        "format": "n8-degree12-full-ideal-dual-fixed-c10-v1",
        "status": "EXACT_FIXED_C10_NONMEMBERSHIP",
        "scope": (
            "exact full homogeneous total-degree-12 normalized mixed ideal "
            "and the fixed deterministic C10 residual; no alternative "
            "right-inverse invariance, t-saturation, degree13, or global claim"
        ),
        "target": target.hex(),
        "target_pairing": fraction_record(functional[target]),
        "construction_stages": stages,
        "functional_support": len(functional),
        "functional_y_degree_histogram": dict(sorted(y_degree_histogram.items())),
        "functional_rows": functional_rows,
        "full_degree12_column_replay": (
            "every original degree-12 column incident to the 20-row functional "
            "support is enumerated and pairs to zero; all nonincident columns "
            "pair to zero tautologically"
        ),
        "fixed_c10_evaluation": evaluation,
        "independent_full_aggregate_crosscheck": {
            "logical_sha256": aggregate["logical_sha256"],
            "target_coefficient": aggregate["PM4_incidence"][
                "lex_dead_coefficient"
            ],
        },
        "d12_monomial_authority_logical_sha256": d12["logical_sha256"],
        "factored_c10_authority_logical_sha256": (
            "e15fb02c5ba4b4b0dadefb0f536953c785d7d07b658b7195a976fc5c145bcd93"
        ),
        "time_cap_seconds": TIME_CAP_SECONDS,
        "rss_cap_bytes": RSS_CAP_BYTES,
        "elapsed_seconds_nonlogical": time.monotonic() - started,
        "peak_rss_bytes_nonlogical": d10_helpers.peak_rss_bytes(),
    }
    logical = {
        key: value for key, value in payload.items()
        if not key.endswith("_nonlogical")
    }
    encoded = json.dumps(logical, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode()).hexdigest()
    require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
            "the full degree-twelve dual ledger changed: "
            + payload["logical_sha256"])
    return payload


if __name__ == "__main__":
    try:
        result = audit()
        RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result, indent=2, sort_keys=True))
    except D12.D11_HELPERS.D10_HELPERS.BoundedStop as stopped:
        print(json.dumps({
            "status": "BOUNDED_UNRESOLVED",
            "detail": stopped.args[0],
            "scope": "no full-C10 membership, saturation, or degree13 inference",
        }, indent=2, sort_keys=True))
