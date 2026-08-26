#!/usr/bin/env python3
"""Sparse affine test for a literal F_0-contraction lift of the 44-dual."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
AUDIT13 = HERE.parent / "unaudited-codex-carrier-minor-pure-amplitude-degree13-x5-2026-08-23" / "audit_pure_amplitude_carrier_minor_separator.py"
OUT = HERE / "results_exact_separator_prolongation_shell_p32003.json"
P = 32003
FILL_CAP = 12_000_000
NEXT_SHELL_CAP = 10_000


def load_audit13():
    spec = importlib.util.spec_from_file_location("audit13", AUDIT13)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


A = load_audit13()
C = A.C
D9 = A.D9


def source_separator():
    record = json.loads(A.OUT.read_text())
    return {
        A.parse_monomial(entry["monomial"]): entry["coefficient"]
        for entry in record["exact_separator"]["entries"]
    }


def build_system():
    separator = source_separator()
    pure = tuple(D9.amplitude((0,) * 8))
    generators = tuple(tuple(D9.amplitude(word)) for word in C.WORDS)
    shell = {
        tuple(sorted(monomial + matching))
        for monomial in separator for matching in pure
    }

    contraction_labels = set()
    x5_labels = set()
    for column in shell:
        for matching in pure:
            quotient = C.divides(column, matching)
            if quotient is not None:
                contraction_labels.add(quotient)
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = C.divides(column, term)
                if quotient is not None:
                    x5_labels.add((word_index, quotient))

    equations = []
    equation_kinds = Counter()
    for quotient in sorted(contraction_labels):
        row = Counter()
        for matching in pure:
            column = tuple(sorted(quotient + matching))
            if column in shell:
                row[column] += 1
        equations.append(("contraction", quotient, row, separator.get(quotient, 0)))
        equation_kinds["contraction"] += 1
    for word_index, quotient in sorted(x5_labels):
        row = Counter()
        for term in generators[word_index]:
            column = tuple(sorted(quotient + term))
            if column in shell:
                row[column] += 1
        label = (D9.word_text(C.WORDS[word_index]), quotient)
        equations.append(("X5", label, row, 0))
        equation_kinds[f"X5_{label[0]}"] += 1
    return separator, pure, generators, shell, equations, equation_kinds


def remap_variables(shell, equations):
    frequencies = Counter()
    for _, _, row, _ in equations:
        frequencies.update(row)
    ordered = sorted(shell, key=lambda monomial: (frequencies[monomial], monomial))
    variable = {monomial: index for index, monomial in enumerate(ordered)}
    remapped = [
        (kind, label,
         {variable[monomial]: coefficient % P
          for monomial, coefficient in row.items() if coefficient % P},
         rhs % P)
        for kind, label, row, rhs in equations
    ]
    return ordered, remapped, frequencies


def reduce_affine(row, rhs, basis):
    row = dict(row)
    while row:
        pivot = min(row)
        coefficient = row[pivot]
        stored = basis.get(pivot)
        if stored is None:
            break
        stored_row, stored_rhs = stored
        for column, value in stored_row.items():
            updated = (row.get(column, 0) - coefficient * value) % P
            if updated:
                row[column] = updated
            else:
                row.pop(column, None)
        rhs = (rhs - coefficient * stored_rhs) % P
    return row, rhs


def solve_affine(equations):
    basis = {}
    dependent = 0
    contradiction = None
    fill_cap_hit = False
    for equation_index, (kind, label, raw, raw_rhs) in enumerate(equations):
        row, rhs = reduce_affine(raw, raw_rhs, basis)
        if not row:
            if rhs:
                contradiction = {
                    "equation_index": equation_index,
                    "kind": kind,
                    "label": (
                        D9.monomial_text(label) if kind == "contraction"
                        else [label[0], D9.monomial_text(label[1])]
                    ),
                    "residual_rhs": rhs,
                }
                break
            dependent += 1
            continue
        pivot = min(row)
        inverse = pow(row[pivot], P - 2, P)
        basis[pivot] = (
            {column: coefficient * inverse % P
             for column, coefficient in row.items()},
            rhs * inverse % P,
        )
        if sum(len(stored[0]) for stored in basis.values()) > FILL_CAP:
            fill_cap_hit = True
            break
        if equation_index and equation_index % 1000 == 0:
            print("insert", equation_index, len(basis),
                  sum(len(stored[0]) for stored in basis.values()), flush=True)
    return basis, dependent, contradiction, fill_cap_hit


def particular_solution(basis, variable_count):
    solution = [0] * variable_count
    for pivot in sorted(basis, reverse=True):
        row, rhs = basis[pivot]
        value = rhs - sum(
            coefficient * solution[column]
            for column, coefficient in row.items() if column != pivot
        )
        solution[pivot] = value % P
    return solution


def exact_contradiction_certificate(equations, variables, terminal_index):
    """Exact-Q replay through the modular contradiction row, with provenance."""
    variable = {monomial: index for index, monomial in enumerate(variables)}
    basis = {}
    contradiction = None
    for equation_index, (kind, label, raw, raw_rhs) in enumerate(equations):
        if equation_index > terminal_index:
            break
        assert kind == "contraction"
        row = {
            variable[monomial]: Fraction(coefficient)
            for monomial, coefficient in raw.items() if coefficient
        }
        rhs = Fraction(raw_rhs)
        provenance = {equation_index: Fraction(1)}
        while row:
            pivot = min(row)
            coefficient = row[pivot]
            stored = basis.get(pivot)
            if stored is None:
                break
            stored_row, stored_rhs, stored_provenance = stored
            for column, value in stored_row.items():
                updated = row.get(column, Fraction(0)) - coefficient * value
                if updated:
                    row[column] = updated
                else:
                    row.pop(column, None)
            rhs -= coefficient * stored_rhs
            for source, value in stored_provenance.items():
                updated = provenance.get(source, Fraction(0)) - coefficient * value
                if updated:
                    provenance[source] = updated
                else:
                    provenance.pop(source, None)
        if not row:
            if rhs:
                contradiction = (equation_index, rhs, provenance)
                break
            continue
        pivot = min(row)
        scale = row[pivot]
        basis[pivot] = (
            {column: value / scale for column, value in row.items()},
            rhs / scale,
            {source: value / scale for source, value in provenance.items()},
        )
    assert contradiction is not None
    equation_index, rhs, provenance = contradiction

    # Independent literal replay of the linear combination.
    combined = Counter()
    combined_rhs = Fraction(0)
    for source, coefficient in provenance.items():
        _, _, row, source_rhs = equations[source]
        for monomial, value in row.items():
            combined[monomial] += coefficient * value
            if not combined[monomial]:
                del combined[monomial]
        combined_rhs += coefficient * source_rhs
    assert not combined and combined_rhs == rhs != 0
    entries = [
        {
            "equation_index": source,
            "quotient": D9.monomial_text(equations[source][1]),
            "coefficient": (
                str(value.numerator) if value.denominator == 1
                else f"{value.numerator}/{value.denominator}"
            ),
        }
        for source, value in sorted(provenance.items())
    ]
    return {
        "terminal_equation_index": equation_index,
        "terminal_quotient": D9.monomial_text(equations[equation_index][1]),
        "certificate_support": len(provenance),
        "combined_lhs_nonzero_terms": len(combined),
        "combined_rhs": (
            str(rhs.numerator) if rhs.denominator == 1
            else f"{rhs.numerator}/{rhs.denominator}"
        ),
        "coefficient_numerator_minimum": min(
            value.numerator for value in provenance.values()
        ),
        "coefficient_numerator_maximum": max(
            value.numerator for value in provenance.values()
        ),
        "coefficient_denominator_maximum": max(
            value.denominator for value in provenance.values()
        ),
        "entries": entries,
        "sha256": sha256(json.dumps(
            entries, sort_keys=True, separators=(",", ":")
        ).encode()).hexdigest(),
    }


def main():
    started = time.time()
    separator, pure, generators, shell, equations, kinds = build_system()
    print("system", len(shell), len(equations), dict(kinds),
          "secs", time.time() - started, flush=True)
    variables, remapped, frequencies = remap_variables(shell, equations)
    basis, dependent, contradiction, fill_cap_hit = solve_affine(remapped)
    if contradiction is not None:
        status = "INCONSISTENT_MOD_P"
        solution = None
    elif fill_cap_hit:
        status = "FILL_CAP"
        solution = None
    else:
        status = "CONSISTENT_MOD_P"
        solution = particular_solution(basis, len(variables))
        # Replay every affine equation independently.
        assert all(
            sum(coefficient * solution[column]
                for column, coefficient in row.items()) % P == rhs
            for _, _, row, rhs in remapped
        )
    exact_contradiction = (
        exact_contradiction_certificate(
            equations, variables, contradiction["equation_index"]
        ) if contradiction is not None else None
    )
    if exact_contradiction is not None:
        certificate_sources = {
            entry["equation_index"]
            for entry in exact_contradiction["entries"]
        }
        repair_outside = set()
        repair_inside = set()
        for source in certificate_sources:
            quotient = equations[source][1]
            for matching in pure:
                column = tuple(sorted(quotient + matching))
                if column in shell:
                    repair_inside.add(column)
                else:
                    repair_outside.add(column)
        next_shell = {
            "cap": NEXT_SHELL_CAP,
            "certificate_inside_variables": len(repair_inside),
            "certificate_outside_repair_variables": len(repair_outside),
            "shell_plus_all_certificate_repairs": len(shell | repair_outside),
            "exceeds_cap": len(shell | repair_outside) > NEXT_SHELL_CAP,
        }
    else:
        next_shell = None
    payload = {
        "status": status,
        "prime": P,
        "source_separator_support": len(separator),
        "pure_matching_terms": len(pure),
        "prolongation_shell_variables": len(shell),
        "equations": len(equations),
        "equation_kinds": dict(kinds),
        "variable_frequency": {
            "minimum": min(frequencies.values()),
            "maximum": max(frequencies.values()),
            "histogram": {
                str(key): value for key, value in sorted(Counter(frequencies.values()).items())
            },
        },
        "rank_before_terminal": len(basis),
        "dependent_rows_before_terminal": dependent,
        "basis_fill": sum(len(stored[0]) for stored in basis.values()),
        "fill_cap": FILL_CAP,
        "contradiction": contradiction,
        "exact_Q_contradiction": exact_contradiction,
        "next_shell_from_certificate": next_shell,
        "solution_nonzero_variables": (
            sum(value != 0 for value in solution) if solution is not None else None
        ),
        "scope": (
            "Affine degree-17 inverse-system lift on the literal shell "
            "supp(lambda)*supp(F_00000000). Contraction by F_00000000 is "
            "required to equal the exact degree-13 lambda on every quotient "
            "touched by the shell, and every mixed-X5 translate touching the "
            "shell is imposed. Inconsistency at one prime is discovery only "
            "until an exact-Q contradiction is replayed."
        ),
    }
    payload["logical_sha256"] = sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(status, "rank", len(basis), "fill", payload["basis_fill"],
          "contradiction", contradiction, "logical", payload["logical_sha256"],
          "secs", time.time() - started, flush=True)


if __name__ == "__main__":
    main()
