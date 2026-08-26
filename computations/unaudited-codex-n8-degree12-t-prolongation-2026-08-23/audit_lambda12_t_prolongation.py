#!/usr/bin/env python3
"""Exact first t-prolongation boundary of the frozen 20-row lambda12."""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL_DIR = ROOT / "computations/unaudited-codex-n8-degree12-full-dual-2026-08-23"
FULL_SCRIPT = FULL_DIR / "audit_degree12_full_dual.py"
FULL_RESULT = FULL_DIR / "results_degree12_full_dual_fixed_c10.json"
TRANSFER_REPORT = (
    ROOT / "computations/unaudited-codex-n8-degree8-transfer-audit-2026-08-23"
    / "REPORT.md"
)
TRANSFER_RESULT = TRANSFER_REPORT.parent / "results_lambda7_lambda8_transfer.json"
REFEREE_REPORT = (
    ROOT / "computations/unaudited-codex-n8-degree13-full-dual-referee-2026-08-23"
    / "REPORT.md"
)
REFEREE_RESULT = REFEREE_REPORT.parent / "results_degree13_full_dual_referee.json"
RESULT = HERE / "results_lambda12_t_prolongation.json"
EXPECTED = {
    FULL_SCRIPT: "3e0e3e7c07201d99ffffdccc95ae65a969ced4f96c425f7b9011ab99777a8fb5",
    FULL_RESULT: "2353a0c3f001fabfc1bb30e199a286c096d3b5b573b55af58b26910a8d2c5137",
    TRANSFER_REPORT: "2077227deca6f8f871310a1cc5a1d56535671ccc05a119e8b0e7fe072f12c6e9",
    TRANSFER_RESULT: "d9f82b3210cae2994b292569653b3e55d945eebdc3e481dc9cd6f81a9b83a7e4",
    REFEREE_REPORT: "06759de26fa82a22d3138787a6ea526adaf41168398bdc9fdb44b2b72387c02d",
    REFEREE_RESULT: "3160c65f21b2cc5d2ec4b4197706ddcb1be7c0f9152c9fdf8312d79054be6b25",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FULL = load(FULL_SCRIPT, "n8_lambda12_t_prolongation_authority")


def fraction(pair):
    return Fraction(pair[0], pair[1])


def sparse_rank(equations, variable_index, prime, include_rhs):
    """Rank of the equation matrix, with source columns as matrix rows."""
    pivots = {}
    selected = []
    rhs_index = len(variable_index)
    for label, coefficients, rhs in equations:
        vector = {
            variable_index[row]: int(value) % prime
            for row, value in coefficients.items() if int(value) % prime
        }
        if include_rhs and rhs:
            vector[rhs_index] = int(rhs) % prime
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                inverse = pow(vector[pivot], prime - 2, prime)
                vector = {key: value * inverse % prime
                          for key, value in vector.items()}
                pivots[pivot] = vector
                selected.append(label)
                break
            factor = vector[pivot]
            for key, value in pivots[pivot].items():
                new_value = (vector.get(key, 0) - factor * value) % prime
                if new_value:
                    vector[key] = new_value
                else:
                    vector.pop(key, None)
    return len(pivots), selected


def residual_core_census(functional, originals, top_sources, base, crossing):
    """Rebuild the exact top-owner graph and census the post-peel core."""
    rows = set()
    for code, multiplier in crossing:
        for term, coefficient in originals[code].items():
            if len(term) == 4:
                require(coefficient != 0, "top crossing coefficient vanished")
                rows.add(bytes(sorted(term + multiplier)))
    row_to_columns = defaultdict(dict)
    column_to_rows = defaultdict(set)
    for row in sorted(rows):
        for term in base.divisors(row, 4):
            for code, coefficient in top_sources.get(term, ()):
                column = (code, base.quotient(row, term))
                row_to_columns[row][column] = Fraction(coefficient)
                column_to_rows[column].add(row)
    pivots, active = FULL.weighted_singleton_peel(column_to_rows, row_to_columns)
    parent = {column: column for column in active}

    def find(column):
        while parent[column] != column:
            parent[column] = parent[parent[column]]
            column = parent[column]
        return column

    def union(left, right):
        left, right = find(left), find(right)
        if left != right:
            parent[right] = left

    active_row_owners = {}
    for row, owners in row_to_columns.items():
        live = sorted(set(owners) & active)
        if live:
            active_row_owners[row] = live
            for column in live[1:]:
                union(live[0], column)
    components = defaultdict(set)
    for column in active:
        components[find(column)].add(column)
    component_rows = defaultdict(set)
    for row, owners in active_row_owners.items():
        component_rows[find(owners[0])].add(row)
    records = []
    for root, columns in components.items():
        hits = columns & set(crossing)
        rows_here = sorted(component_rows[root])
        record = {
            "columns": len(columns),
            "rows": len(rows_here),
            "crossing_columns": len(hits),
            "crossing_ledger": [
                [code, multiplier.hex()] for code, multiplier in sorted(hits)
            ],
        }
        if hits:
            row_index = {row: index for index, row in enumerate(rows_here)}
            equations = []
            for column in sorted(columns):
                coefficients = {
                    row: row_to_columns[row][column]
                    for row in column_to_rows[column]
                    if row in row_index
                }
                rhs = -FULL.column_value(functional, *column, originals)
                equations.append((
                    [column[0], column[1].hex()], coefficients, rhs
                ))
            ranks = {}
            for prime in (32003, 32009):
                rank_a, _selected_a = sparse_rank(
                    equations, row_index, prime, False
                )
                rank_aug, selected_aug = sparse_rank(
                    equations, row_index, prime, True
                )
                ranks[str(prime)] = {
                    "rank_owner": rank_a,
                    "rank_augmented": rank_aug,
                    "owner_variables": len(rows_here),
                    "full_column_rank_obstruction": (
                        rank_aug == len(rows_here) + 1
                    ),
                    "selected_augmented_equations": (
                        selected_aug if rank_aug == len(rows_here) + 1 else []
                    ),
                }
            record["modular_rank_certificate"] = ranks
        records.append(record)
    records.sort(key=lambda record: (
        -record["crossing_columns"], -record["columns"], -record["rows"]
    ))
    return {
        "pivots": len(pivots),
        "active_columns": len(active),
        "active_rows": len(active_row_owners),
        "components": len(records),
        "crossing_components": sum(bool(r["crossing_columns"]) for r in records),
        "component_census": records,
    }


def audit(mutate=False):
    started = time.monotonic()
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    frozen = json.loads(FULL_RESULT.read_text())
    referee = json.loads(REFEREE_RESULT.read_text())
    require(referee["status"] == "D12_FH_UPGRADE_FALSE_D13_CROSSING_CORE"
            and referee["logical_sha256"]
            == "0942f658d68bf670f17af93e6201414a55d25611c84a88a623021f411be2eee8",
            "degree12/Fh scope referee changed")
    require(referee["d12_referee"]["normalized_Fh_pairing"] == [0, 1]
            and referee["d12_referee"]["fixed_c10_pairing"] == -4,
            "Fh versus fixed-C10 correction changed")
    require(frozen["status"] == "EXACT_FIXED_C10_NONMEMBERSHIP"
            and frozen["logical_sha256"]
            == "cde136aef242841bc78bc9b7da8e56323ab0b273bb637a30253902e9b2729aed",
            "lambda12 authority changed")
    functional = {
        bytes.fromhex(row): Fraction(numerator, denominator)
        for row, numerator, denominator in frozen["functional_rows"]
    }
    if mutate:
        row = min(functional)
        functional[row] += 1
    require(len(functional) == 20
            and Counter(map(len, functional)) == {10: 1, 11: 3, 12: 16},
            "lambda12 support/profile changed")

    helpers = FULL.D12.D11_HELPERS.D10_HELPERS
    base = helpers.load(helpers.D8_BASE_PATH, "n8_lambda12_t_base")
    source = base.load_source()
    originals, _leads = source.FIRST.original_basis()
    term_sources = base.make_term_sources(originals)
    top_sources = defaultdict(list)
    for code, polynomial in originals.items():
        for term, coefficient in polynomial.items():
            if len(term) == 4:
                top_sources[term].append((code, coefficient))

    primitive = FULL.incident_primitive(functional, 13, term_sources, base)
    primitive_values = {
        column: FULL.column_value(functional, *column, originals)
        for column in primitive
    }
    crossing = {column: value for column, value in primitive_values.items()
                if value}

    def check_cap(label):
        require(time.monotonic() - started < 120, f"time cap at {label}")
        require(helpers.peak_rss_bytes() < 4 * 1024 ** 3,
                f"rss cap at {label}")

    extended, stage = FULL.extend_separator(
        functional, 13, originals, term_sources, top_sources, base, check_cap,
    )
    if extended is None:
        core = residual_core_census(
            functional, originals, top_sources, base, crossing
        )
        result = {
            "format": "n8-lambda12-first-t-prolongation-v1",
            "status": "D13_TOP_SINGLETON_REPAIR_CORE_UNRESOLVED",
            "lambda12": {
                "logical_sha256": frozen["logical_sha256"],
                "support": len(functional),
                "y_degree_histogram": dict(sorted(Counter(map(len, functional)).items())),
                "C10_pairing": frozen["fixed_c10_evaluation"]["pairing"],
                "normalized_Fh_pairing": referee["d12_referee"]["normalized_Fh_pairing"],
                "omitted_y11_y12_tail_pairing": 4,
            },
            "naive_t_prolongation_boundary": {
                "new_t_free_multiplier_degree": 9,
                "incident_primitive_columns": len(primitive),
                "crossing_columns": len(crossing),
                "crossing_pairing_histogram": {
                    f"{n}/{d}": count
                    for (n, d), count in sorted(Counter(
                        (value.numerator, value.denominator)
                        for value in crossing.values()
                    ).items())
                },
                "crossing_column_ledger": [
                    [code, multiplier.hex(), value.numerator, value.denominator]
                    for (code, multiplier), value in sorted(crossing.items())
                ],
            },
            "top_repair": {"stage": stage, "residual_core": core},
            "relative_bockstein": {
                "rhs": (
                    "pairings of the naive t-shift with the 122 new t-free "
                    "nonic-multiplier columns"
                ),
                "correction_map": (
                    "transpose of the y13 top-row/owner-column incidence"
                ),
                "criterion": (
                    "lambda12 extends with fixed rho_t restriction iff this "
                    "RHS belongs to the full transpose image"
                ),
                "audited_page": (
                    "7894 first owner rows and 7309 owner columns; private "
                    "triangular repair kills 85 crossings and leaves 27 in "
                    "nine connected components"
                ),
                "smallest_component": (
                    "71 columns, 68 rows, one crossing; modular ranks of "
                    "owner/augmented matrices are 52/53 at both 32003 and "
                    "32009. This is a first-page obstruction only because "
                    "unexposed y13 rows may attach to it."
                ),
            },
            "transfer_and_all_k_guard": {
                "existing_lambda7_lambda8_audit": (
                    "applicable only as a methodological no-go: it refutes "
                    "scalar, profile-only, row-induced, and flat-Hankel "
                    "recurrences and exhibits nonunique invisible top rows"
                ),
                "why_no_all_k_invariant": (
                    "the lambda12 first page is not even privately closed, "
                    "and no finite source-labelled contraction module or "
                    "right inverse for all top-owner pages is known"
                ),
            },
            "target_scope_correction": (
                "lambda12(Fh)=0 exactly, while lambda12(C10)=-4; the omitted "
                "y11/y12 actual residual contributes +4. Therefore this is "
                "only a fixed-C10/truncated-tail prolongation audit and is "
                "not an Fh t-saturation obstruction."
            ),
            "scope": (
                "exact normalized orbit26 first D13 owner page for the fixed "
                "20-row functional; no D13 extension/nonextension theorem, "
                "Fh nonmembership, t-saturation, all-k, or global claim"
            ),
        }
        logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
        result["logical_sha256"] = sha256(logical.encode()).hexdigest()
        return result
    require(stage["status"] == "D13_EXACT_EXTENSION",
            "unexpected t-prolongation terminal status")
    all_incident = FULL.incident_all(extended, 13, term_sources, base)
    all_values = {
        column: FULL.column_value(extended, *column, originals)
        for column in all_incident
    }
    require(not {column: value for column, value in all_values.items() if value},
            "lambda13 misses a full incident degree13 column")

    old_rows = set(functional)
    correction = {row: value for row, value in extended.items()
                  if row not in old_rows}
    require(all(len(row) == 13 for row in correction),
            "the repair is not entirely in the t-free top layer")
    require(all(extended[row] == value for row, value in functional.items()),
            "rho_t(lambda13) is not lambda12")
    target = bytes.fromhex(frozen["target"])
    require(extended[target] == 1, "the prolonged target pairing moved")
    require(frozen["fixed_c10_evaluation"]["pairing"] == -4,
            "the frozen C10 pairing moved")

    crossing_histogram = Counter(
        (value.numerator, value.denominator) for value in crossing.values()
    )
    correction_histogram = Counter(
        (value.numerator, value.denominator) for value in correction.values()
    )
    stage["exhaustive_all_incident_columns"] = len(all_incident)
    stage["exhaustive_all_nonzero_columns"] = 0
    result = {
        "format": "n8-lambda12-first-t-prolongation-v1",
        "status": "EXACT_LAMBDA13_EXTENSION_FIRST_T_SATURATION_STEP_SURVIVES",
        "lambda12": {
            "logical_sha256": frozen["logical_sha256"],
            "support": len(functional),
            "y_degree_histogram": dict(sorted(Counter(map(len, functional)).items())),
            "C10_pairing": frozen["fixed_c10_evaluation"]["pairing"],
        },
        "naive_t_prolongation_boundary": {
            "new_t_free_multiplier_degree": 9,
            "incident_primitive_columns": len(primitive),
            "crossing_columns": len(crossing),
            "crossing_pairing_histogram": {
                f"{n}/{d}": count
                for (n, d), count in sorted(crossing_histogram.items())
            },
            "crossing_column_ledger": [
                [code, multiplier.hex(), value.numerator, value.denominator]
                for (code, multiplier), value in sorted(crossing.items())
            ],
        },
        "top_repair": {
            "stage": stage,
            "support": len(correction),
            "coefficient_histogram": {
                f"{n}/{d}": count
                for (n, d), count in sorted(correction_histogram.items())
            },
            "rows": [
                [row.hex(), value.numerator, value.denominator]
                for row, value in sorted(correction.items())
            ],
        },
        "lambda13": {
            "support": len(extended),
            "y_degree_histogram": dict(sorted(Counter(map(len, extended)).items())),
            "rho_t_identity": "restriction to rows with positive implicit t exponent equals lambda12",
            "all_incident_degree13_columns": len(all_incident),
            "all_nonzero_pairings": 0,
            "target": target.hex() + "*t^3",
            "target_pairing": 1,
            "t_times_fixed_C10_pairing": -4,
        },
        "relative_bockstein": {
            "complex": (
                "new t-free degree13 columns -> their t-free y13 owner rows; "
                "the naive shifted lambda12 supplies the crossing RHS"
            ),
            "criterion": (
                "the RHS must lie in the transpose image of the top-owner "
                "incidence map"
            ),
            "result": (
                "the weighted singleton ledger supplies an exact right inverse; "
                "the first obstruction vanishes"
            ),
        },
        "all_k_guard": {
            "verdict": "NO_ALL_K_RECURRENCE_FROM_ONE_MORE_LIFT",
            "reason": (
                "lambda13 adds genuinely new t-free top rows. Iteration requires "
                "recomputing the next owner incidence or proving a stable finite "
                "source-labelled right inverse; neither is contained in this packet."
            ),
            "previous_transfer_audit": (
                "lambda7->lambda8 already refutes scalar/profile-only/flat-Hankel "
                "rules and exhibits nonunique invisible top directions; those "
                "counterguards apply to the method, not as a proof that lambda13 "
                "cannot lift further."
            ),
        },
        "scope": (
            "exact normalized orbit26 homogeneous degree13 and t*C10 only; "
            "this proves the first t-saturation step but no t^2 step, all-k "
            "saturation, or global unlocalized theorem"
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text()) == result,
                "stored result changed")
    print(result["status"])
    print("logical", result["logical_sha256"])
    print("boundary", result["naive_t_prolongation_boundary"])
    print("repair support", result["top_repair"].get("support", "unresolved"))


if __name__ == "__main__":
    main()
