#!/usr/bin/env python3
"""Private-row lazy CEGAR for the chart-26 degree-nine dual.

The frozen round-14 packet has full top rank for the strongest possible
combinatorial reason: every selected source column owns a degree-nine row
that occurs in no other selected column.  This driver uses those rows as an
explicit diagonal solve.  It therefore avoids rebuilding the 2.9-million-row
relative matrix at every CEGAR round.

Discovery is modular.  A zero-crossing terminal is accepted only after the
same private rows are replayed over Q and every literal incident column is
checked exactly.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_degree8_dual_extension.py"
RUST_DRIVER_PATH = HERE / "audit_degree8_lazy_dual_cegar_rust.py"
D8_PATH = HERE / "results_degree8_rust_cegar.json"
CHECKPOINT_PATH = HERE / "results_degree9_rust_cegar_checkpoint.json"
OUT_PATH = HERE / "results_degree9_private_row_cegar.json"
STATE_PATH = HERE / "results_degree9_private_row_cegar_checkpoint.json"
EXPECTED_D8_DUAL = "561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d"
EXPECTED_CHECKPOINT = "9100c0624464d0a82c0e11bde9a2782d555d1f1d7b7f7368b603a343928034a5"
PRIME = 1_073_741_827
WALL_SECONDS = 540
ROUND_CAP = 100
SELECTED_CAP = 250_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def residue(value):
    if isinstance(value, Fraction):
        return value.numerator * pow(value.denominator, PRIME - 2, PRIME) % PRIME
    return value % PRIME


def signed(value):
    return value if value <= PRIME // 2 else value - PRIME


def column_record(column):
    return [column[0], column[1].hex()]


def main():
    started = monotonic()
    require(sha256(CHECKPOINT_PATH.read_bytes()).hexdigest() == EXPECTED_CHECKPOINT,
            "frozen round-14 checkpoint changed")
    audit = load(AUDIT_PATH, "degree9_private_audit")
    rust = load(RUST_DRIVER_PATH, "degree9_private_rust")
    source = audit.load_d7()
    d8 = json.loads(D8_PATH.read_text())
    require(d8["status"] == "EXTENDED_DUAL_EXACT_Q"
            and d8["exact_extended_dual_sha256"] == EXPECTED_D8_DUAL,
            "pinned lambda8 changed")
    lambda8_exact = {
        bytes.fromhex(encoded): Fraction(numerator, denominator)
        for encoded, numerator, denominator in d8["exact_extended_dual"]
    }
    require(len(lambda8_exact) == 561 and lambda8_exact.get(b"") == 1,
            "lambda8 support/target changed")
    lambda8 = {row: residue(value) for row, value in lambda8_exact.items()}

    frozen = json.loads(CHECKPOINT_PATH.read_text())
    selected = {
        (word, bytes.fromhex(multiplier))
        for word, multiplier in frozen["selected_columns"]
    }
    require(frozen["completed_round"] == 14 and len(selected) == 53_995,
            "frozen selected packet changed")

    @lru_cache(maxsize=None)
    def entries(column):
        return tuple(sorted(audit.invariant_entries(source, column).items()))

    def pairing(column, functional):
        return sum(coefficient * functional.get(row, 0)
                   for row, coefficient in entries(column)) % PRIME

    rounds = []
    terminal = None
    terminal_functional = None
    terminal_private = None
    terminal_missing = None
    for round_index in range(ROUND_CAP):
        if monotonic() - started >= WALL_SECONDS:
            terminal = "WALL_CAP_UNRESOLVED"
            break
        require(len(selected) <= SELECTED_CAP, "selected-column cap exceeded")
        columns = tuple(sorted(selected))

        # Saturate owner counts at two: only uniqueness matters.
        owner_count = {}
        top_nnz = 0
        for index, column in enumerate(columns, 1):
            for row, _coefficient in entries(column):
                if len(row) == 9:
                    owner_count[row] = min(2, owner_count.get(row, 0) + 1)
                    top_nnz += 1
            if index % 10_000 == 0:
                print("owner pass", round_index, index, "/", len(columns),
                      "rows", len(owner_count), "elapsed", f"{monotonic()-started:.1f}",
                      flush=True)

        private_rows = {row for row, count in owner_count.items() if count == 1}
        private_candidates = {}
        missing = []
        boundary_nonzero = 0
        for column in columns:
            boundary = pairing(column, lambda8)
            if boundary:
                boundary_nonzero += 1
            private = next(((row, coefficient) for row, coefficient in entries(column)
                            if len(row) == 9 and row in private_rows), None)
            if private is None:
                missing.append(column)
                continue
            candidates_for_column = tuple(
                (row, coefficient) for row, coefficient in entries(column)
                if len(row) == 9 and row in private_rows
            )
            require(candidates_for_column, "private candidate disappeared")
            private_candidates[column] = candidates_for_column

        # Solve only the exceptional non-private columns.  Their solution may
        # touch rows of ordinary columns; the globally private row of each
        # ordinary column then compensates that contribution without changing
        # any other equation.
        functional = dict(lambda8)
        missing_extension = {}
        missing_rank = 0
        if missing:
            missing = tuple(sorted(missing))
            missing_index = {column: index for index, column in enumerate(missing)}
            row_vectors = {}
            target = {}
            for column in missing:
                cindex = missing_index[column]
                boundary = pairing(column, lambda8)
                if boundary:
                    target[cindex] = (-boundary) % PRIME
                for row, coefficient in entries(column):
                    if len(row) == 9:
                        row_vectors.setdefault(row, {})[cindex] = coefficient % PRIME
            missing_rank, remainder, missing_extension = rust.run_modsolve(
                missing, tuple(sorted(row_vectors)), row_vectors, target
            )
            if remainder:
                terminal = "MODULAR_EXCEPTIONAL_BLOCK_INCONSISTENCY"
                rounds.append({
                    "round": round_index,
                    "selected_columns": len(columns),
                    "top_rows": len(owner_count),
                    "top_nnz": top_nnz,
                    "private_rows": len(private_rows),
                    "columns_without_private_row": len(missing),
                    "exceptional_block_rank": missing_rank,
                    "exceptional_block_remainder_terms": remainder,
                    "first_missing_columns": [column_record(column) for column in missing[:32]],
                    "elapsed_seconds": monotonic() - started,
                })
                break
            functional.update(missing_extension)

        # Choose active private pivots by direct crossing minimization.  A
        # private row has a fixed weight (boundary divided by its diagonal),
        # so every option has an explicit sparse effect on incident columns.
        # Coordinate descent minimizes the *actual* nonzero outside pairings,
        # including cancellations between chosen rows, rather than merely the
        # union of their supports.
        base_candidates = {
            column for column in source.bounded_incident_columns(
                functional, maximum_output_degree=9
            ) if len(column[1]) == 5
        }
        base_pairings = {
            column: pairing(column, functional) for column in base_candidates
        }
        base_pairings = {column: value for column, value in base_pairings.items() if value}
        options = {}
        for column in columns:
            if column not in private_candidates:
                continue
            boundary = pairing(column, functional)
            if not boundary:
                continue
            ranked_private = []
            for row, coefficient in private_candidates[column]:
                incident = tuple(
                    candidate for candidate in source.top_incident_columns(row)
                    if len(candidate[1]) == 5
                )
                ranked_private.append((
                    sum(candidate not in selected for candidate in incident),
                    len(incident), row, coefficient, incident,
                ))
            # Computing invariant effects for every private row materializes
            # too many Python row objects.  The four cheapest choices retain
            # a deterministic local-search neighbourhood while bounding RSS.
            ranked_private.sort()
            local_options = []
            for _outside, _incidence_count, row, coefficient, incident in ranked_private[:4]:
                value = (-boundary * pow(coefficient % PRIME, PRIME - 2, PRIME)) % PRIME
                effects = {}
                for candidate in incident:
                    entry = dict(entries(candidate)).get(row, 0) % PRIME
                    require(entry, "top incidence omitted its displayed row")
                    effects[candidate] = entry * value % PRIME
                local_options.append((row, coefficient, value, effects))
            options[column] = tuple(local_options)

        # Low-external-incidence initialization.
        choice = {}
        for column, local_options in options.items():
            choice[column] = min(
                local_options,
                key=lambda item: (sum(candidate not in selected for candidate in item[3]),
                                  len(item[3]), item[0]),
            )

        pairings = dict(base_pairings)
        for _column, (_row, _coefficient, _value, effects) in choice.items():
            for candidate, effect in effects.items():
                value = (pairings.get(candidate, 0) + effect) % PRIME
                if value:
                    pairings[candidate] = value
                else:
                    pairings.pop(candidate, None)

        local_search_sweeps = 0
        local_search_changes = 0
        for sweep in range(6):
            changes = 0
            for column in sorted(options):
                old = choice[column]
                old_effects = old[3]
                best = old
                affected_old = set(old_effects)
                def local_score(candidate_option):
                    new_effects = candidate_option[3]
                    affected = affected_old | set(new_effects)
                    violations = 0
                    for candidate in affected:
                        value = (pairings.get(candidate, 0)
                                 - old_effects.get(candidate, 0)
                                 + new_effects.get(candidate, 0)) % PRIME
                        violations += candidate not in selected and value != 0
                    return (violations, candidate_option is not old,
                            len(new_effects), candidate_option[0])
                best = min(options[column], key=local_score)
                if best is old:
                    continue
                old_score = local_score(old)[0]
                best_score = local_score(best)[0]
                if best_score >= old_score:
                    continue
                for candidate in affected_old | set(best[3]):
                    value = (pairings.get(candidate, 0)
                             - old_effects.get(candidate, 0)
                             + best[3].get(candidate, 0)) % PRIME
                    if value:
                        pairings[candidate] = value
                    else:
                        pairings.pop(candidate, None)
                choice[column] = best
                changes += 1
            local_search_sweeps = sweep + 1
            local_search_changes += changes
            if changes == 0:
                break

        chosen = {}
        candidate_union = set(base_candidates)
        for column, (row, coefficient, value, effects) in choice.items():
            require(row not in chosen and coefficient % PRIME,
                    "private row reused or has zero pivot")
            chosen[row] = (column, coefficient, value)
            if value:
                functional[row] = value
                candidate_union.update(effects)

        require(all(pairing(column, functional) == 0 for column in columns),
                "private-row extension fails a selected column")
        candidates = {
            column for column in source.bounded_incident_columns(
                functional, maximum_output_degree=9
            ) if len(column[1]) == 5
        }
        require(candidates == candidate_union,
                "greedy incident union disagrees with literal provider")
        violations = {
            column: pairing(column, functional)
            for column in candidates
            if pairing(column, functional)
        }
        require(violations == {column: value for column, value in pairings.items() if value},
                "local-search pairing ledger disagrees with literal provider")
        require(not (set(violations) & selected),
                "private-row extension fails an already selected column")
        new_violating_columns = set(violations) - selected
        new_columns = set(new_violating_columns)
        record = {
            "round": round_index,
            "selected_columns": len(columns),
            "top_rows": len(owner_count),
            "top_nnz": top_nnz,
            "private_rows": len(private_rows),
            "columns_without_private_row": len(missing),
            "exceptional_block_rank": missing_rank,
            "exceptional_block_extension_support": len(missing_extension),
            "private_pivot_rule": "six-sweep deterministic coordinate descent minimizing actual nonzero outside pairings",
            "local_search_sweeps": local_search_sweeps,
            "local_search_changes": local_search_changes,
            "boundary_nonzero_columns": boundary_nonzero,
            "extension_support": sum(value != 0 for _column, _coefficient, value in chosen.values()),
            "incident_degree9_columns": len(candidates),
            "new_violating_columns": len(new_violating_columns),
            "new_forced_incident_columns": len(new_columns),
            "violation_residue_histogram": [
                [signed(value), count]
                for value, count in sorted(Counter(violations.values()).items())
            ],
            "elapsed_seconds": monotonic() - started,
        }
        rounds.append(record)
        print("private round", round_index, "selected", len(columns),
              "rows", len(owner_count), "candidates", len(candidates),
              "violating", len(new_violating_columns), "forced", len(new_columns),
              "elapsed", f"{monotonic()-started:.1f}",
              flush=True)
        if not new_columns:
            terminal = "MODULAR_PRIVATE_ROW_DUAL"
            terminal_functional = functional
            terminal_private = chosen
            terminal_missing = missing
            break
        selected.update(new_columns)
        state = {
            "format": "n8-chart26-degree9-private-row-cegar-checkpoint-v1",
            "prime": PRIME,
            "completed_round": round_index,
            "selected_columns": [column_record(column) for column in sorted(selected)],
            "rounds": rounds,
        }
        STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")

    result = {
        "format": "n8-chart26-degree9-private-row-cegar-v1",
        "status": terminal,
        "prime": PRIME,
        "lambda8_sha256": EXPECTED_D8_DUAL,
        "frozen_round14_checkpoint_sha256": EXPECTED_CHECKPOINT,
        "initial_selected_columns": 53_995,
        "terminal_selected_columns": len(selected),
        "round_cap": ROUND_CAP,
        "wall_cap_seconds": WALL_SECONDS,
        "rounds": rounds,
        "elapsed_seconds": monotonic() - started,
        "scope_guard": "modular discovery alone proves no characteristic-zero statement",
    }

    if terminal == "MODULAR_PRIVATE_ROW_DUAL":
        # The private solve is diagonal over Q, so exact replay needs no
        # elimination and is independent of the discovery prime.
        exact_functional = dict(lambda8_exact)
        exact_missing_support = 0
        if terminal_missing:
            missing = tuple(sorted(terminal_missing))
            missing_index = {column: index for index, column in enumerate(missing)}
            exact_rows = {}
            exact_target = {}
            for column in missing:
                cindex = missing_index[column]
                boundary = sum(Fraction(coefficient) * lambda8_exact.get(row, 0)
                               for row, coefficient in entries(column))
                if boundary:
                    exact_target[cindex] = -boundary
                for row, coefficient in entries(column):
                    if len(row) == 9:
                        exact_rows.setdefault(row, {})[cindex] = coefficient
            ordered_rows = tuple(sorted(exact_rows))
            exact_rank, exact_extension, exact_remainder, _separator = (
                audit.exact_relative_solve(
                    ordered_rows, [exact_rows[row] for row in ordered_rows],
                    exact_target, monotonic(),
                )
            )
            require(not exact_remainder and exact_rank == len(missing),
                    "exceptional block failed exact replay")
            exact_functional.update(exact_extension)
            exact_missing_support = len(exact_extension)
        exact_private = []
        for row, (column, coefficient, _modular_value) in sorted(terminal_private.items()):
            boundary = sum(Fraction(entry_coefficient) * exact_functional.get(entry_row, 0)
                           for entry_row, entry_coefficient in entries(column))
            value = -boundary / coefficient
            if value:
                exact_functional[row] = value
            exact_private.append([
                row.hex(), column[0], column[1].hex(), coefficient,
                value.numerator, value.denominator,
            ])
        require(all(sum(Fraction(coefficient) * exact_functional.get(row, 0)
                            for row, coefficient in entries(column)) == 0
                    for column in selected),
                "exact private-row extension fails a selected column")
        exact_candidates = {
            column for column in source.bounded_incident_columns(
                exact_functional, maximum_output_degree=9
            ) if len(column[1]) == 5
        }
        exact_violations = {
            column: sum(Fraction(coefficient) * exact_functional.get(row, 0)
                        for row, coefficient in entries(column))
            for column in exact_candidates
        }
        exact_violations = {column: value for column, value in exact_violations.items() if value}
        require(not exact_violations,
                "exact private-row terminal misses a literal incident column")
        dual_record = [
            [row.hex(), value.numerator, value.denominator]
            for row, value in sorted(exact_functional.items())
        ]
        private_digest = sha256(json.dumps(
            exact_private, separators=(",", ":")
        ).encode()).hexdigest()
        dual_digest = sha256(json.dumps(
            dual_record, separators=(",", ":")
        ).encode()).hexdigest()
        result.update({
            "status": "EXTENDED_PRIVATE_ROW_DUAL_EXACT_Q",
            "exact_extended_dual_support": len(exact_functional),
            "exact_extension_support": len(exact_functional) - len(lambda8_exact),
            "exact_exceptional_block_support": exact_missing_support,
            "exact_incident_columns": len(exact_candidates),
            "exact_private_pivot_ledger_sha256": private_digest,
            "exact_extended_dual_sha256": dual_digest,
            "exact_extended_dual": dual_record,
            "conclusion": "t^9 is not in the degree-nine homogeneous mixed ideal over Q",
            "scope_guard": "chart26 degree-nine homogeneous cap only; no degree>=10 or unrestricted saturation inference",
        })

    OUT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("degree9 private terminal", result["status"],
          "selected", len(selected), "elapsed", f"{monotonic()-started:.1f}")


if __name__ == "__main__":
    main()
