#!/usr/bin/env python3
"""Bounded finite-field tangent/core screen for four canonical triangle branches."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPORTER = (ROOT / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22"
            / "export_canonical_triangle_branch_msolve.py")
EXPORTER_SHA256 = "3abf2f6b61df486679132bf234b6235df12f36e6609b34a1a37886802882959e"
MANIFEST = EXPORTER.with_name("canonical_triangle_incidence_manifest.json")
MANIFEST_SHA256 = "0b556f2f217e1a1f158edb66e64d74fa8f5f7b649be182c797c10711f378b529"
OUT = HERE / "results_canonical_triangle_ff_screen.json"
EXPECTED_LOGICAL_SHA256 = "16b55f4de26583520f74a85207fd5d39ce3cb75cfb0c9fef7f30c5b1d50ac811"
P = 32003
SEEDS = (2026082301, 2026082302, 2026082303)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pinned(path, expected):
    raw = path.read_bytes()
    actual = sha256(raw).hexdigest()
    require(actual == expected, (str(path), actual, expected))
    return raw, actual


def load_exporter():
    spec = importlib.util.spec_from_file_location("triangle_exporter", EXPORTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add(row, variable, value):
    value %= P
    if not value:
        return
    value = (row.get(variable, 0) + value) % P
    if value:
        row[variable] = value
    elif variable in row:
        del row[variable]


def product_except(values, omitted):
    result = 1
    for index, value in enumerate(values):
        if index != omitted:
            result = result * value % P
    return result


class Screen:
    def __init__(self, source):
        self.source = source
        self.xvars = source.source_variables()
        self.lvars = source.witness_variables()
        self.variables = self.xvars + self.lvars + ["sy0"]
        self.variable_index = {name: index for index, name in enumerate(self.variables)}
        require(len(self.xvars) == 252 and len(self.lvars) == 108
                and len(self.variables) == 361, len(self.variables))

    def amplitude_and_gradient(self, values, word):
        answer = 0
        gradient = {}
        for matching in self.source.PM8:
            names = [self.source.xvar(u, v, word[u], word[v]) for u, v in matching]
            entries = [values[name] for name in names]
            term = 1
            for entry in entries:
                term = term * entry % P
            answer = (answer + term) % P
            for index, name in enumerate(names):
                add(gradient, self.variable_index[name], product_except(entries, index))
        return answer, gradient

    def normalize_pure(self, values, colour):
        pivot = self.source.xvar(0, 1, colour, colour)
        values[pivot] = 0
        word = (colour,) * 8
        without, _ = self.amplitude_and_gradient(values, word)
        cofactor = 0
        for matching in self.source.PM8:
            if (0, 1) not in matching:
                continue
            term = 1
            for u, v in matching:
                if (u, v) != (0, 1):
                    term = term * values[self.source.xvar(u, v, colour, colour)] % P
            cofactor = (cofactor + term) % P
        require(cofactor, (colour, "zero normalization cofactor"))
        values[pivot] = (1 - without) * pow(cofactor, P - 2, P) % P
        check, _ = self.amplitude_and_gradient(values, word)
        require(check == 1, (colour, check))

    def response_row(self, values, a, b, ca, cb):
        result = []
        for i, j in product(range(3), repeat=2):
            first, second = self.source.response_coefficient(a, b, ca, cb, i, j)
            f0, f1 = first.split("*")
            s0, s1 = second.split("*")
            result.append((values[f0] * values[f1]
                           + values[s0] * values[s1]) % P)
        return result

    @staticmethod
    def solve_full_row_rank(matrix, rhs):
        # Solve the 9 x 108 system matrix * lambda = rhs with free variables 0.
        augmented = [list(row) + [value % P] for row, value in zip(matrix, rhs)]
        pivot_columns = []
        pivot_row = 0
        for column in range(len(matrix[0])):
            selected = next((r for r in range(pivot_row, len(augmented))
                             if augmented[r][column] % P), None)
            if selected is None:
                continue
            augmented[pivot_row], augmented[selected] = augmented[selected], augmented[pivot_row]
            inverse = pow(augmented[pivot_row][column] % P, P - 2, P)
            augmented[pivot_row] = [value * inverse % P
                                    for value in augmented[pivot_row]]
            for row in range(len(augmented)):
                if row == pivot_row:
                    continue
                scale = augmented[row][column] % P
                if scale:
                    augmented[row] = [
                        (left - scale * right) % P
                        for left, right in zip(augmented[row], augmented[pivot_row])
                    ]
            pivot_columns.append(column)
            pivot_row += 1
            if pivot_row == len(augmented):
                break
        require(pivot_row == 9, ("response rank", pivot_row))
        solution = [0] * len(matrix[0])
        for row, column in enumerate(pivot_columns):
            solution[column] = augmented[row][-1]
        require(all(sum(a * b for a, b in zip(row, solution)) % P == value % P
                    for row, value in zip(matrix, rhs)), "witness solve failed")
        return solution, pivot_columns

    @staticmethod
    def determinant(matrix):
        work = [list(row) for row in matrix]
        answer = 1
        for column in range(len(work)):
            selected = next((row for row in range(column, len(work))
                             if work[row][column] % P), None)
            if selected is None:
                return 0
            if selected != column:
                work[column], work[selected] = work[selected], work[column]
                answer = -answer
            pivot = work[column][column] % P
            answer = answer * pivot % P
            inverse = pow(pivot, P - 2, P)
            for row in range(column + 1, len(work)):
                scale = work[row][column] * inverse % P
                for entry in range(column, len(work)):
                    work[row][entry] = (work[row][entry]
                                        - scale * work[column][entry]) % P
        return answer % P

    def construct_base_point(self, branch, seed):
        rng = random.Random(seed)
        values = {name: rng.randrange(1, P) for name in self.xvars}
        values[self.source.xvar(0, 6, 0, 1)] = 1
        for colour in range(3):
            self.normalize_pure(values, colour)
        response_rows = [
            self.response_row(values, a, b, ca, cb)
            for a, b in self.source.OUTSIDE
            for ca, cb in product(range(3), repeat=2)
        ]
        matrix = [list(column) for column in zip(*response_rows)]
        if branch == "triangle_endpoint_colour":
            rhs = [int((i, j) == (0, 0)) for i, j in product(range(3), repeat=2)]
        elif branch == "cap_endpoint_colour":
            rhs = [int((i, j) == (1, 1)) for i, j in product(range(3), repeat=2)]
        elif branch == "third_colour":
            rhs = [int((i, j) == (2, 2)) for i, j in product(range(3), repeat=2)]
        else:
            require(branch == "direct", branch)
            rhs = [values[self.source.xvar(6, 7, i, j)]
                   for i, j in product(range(3), repeat=2)]
        witnesses, pivot_columns = self.solve_full_row_rank(matrix, rhs)
        values.update(zip(self.lvars, witnesses))
        values["sy0"] = 1
        first_edge_minor = self.determinant([row[:9] for row in matrix])
        require(first_edge_minor, first_edge_minor)
        return values, response_rows, pivot_columns, first_edge_minor

    def membership_equation(self, values, branch, i, j):
        if branch == "triangle_endpoint_colour":
            value = int((i, j) == (0, 0))
            gradient = {}
        elif branch == "cap_endpoint_colour":
            value = int((i, j) == (1, 1))
            gradient = {}
        elif branch == "third_colour":
            value = int((i, j) == (2, 2))
            gradient = {}
        else:
            name = self.source.xvar(6, 7, i, j)
            value = values[name]
            gradient = {self.variable_index[name]: 1}
        row_number = 0
        for a, b in self.source.OUTSIDE:
            for ca, cb in product(range(3), repeat=2):
                lname = self.source.lvar(a, b, ca, cb)
                lam = values[lname]
                first, second = self.source.response_coefficient(a, b, ca, cb, i, j)
                pairs = (first.split("*"), second.split("*"))
                coefficient = 0
                for left, right in pairs:
                    coefficient = (coefficient + values[left] * values[right]) % P
                    add(gradient, self.variable_index[left], -lam * values[right])
                    add(gradient, self.variable_index[right], -lam * values[left])
                value = (value - lam * coefficient) % P
                add(gradient, self.variable_index[lname], -coefficient)
                row_number += 1
        require(row_number == 108, row_number)
        return value, gradient

    def base_equations(self, values, branch):
        equations = []
        for colour in range(3):
            value, gradient = self.amplitude_and_gradient(values, (colour,) * 8)
            equations.append((f"pure_{colour}", (value - 1) % P, gradient))
        for i, j in product(range(3), repeat=2):
            value, gradient = self.membership_equation(values, branch, i, j)
            equations.append((f"membership_K{i}{j}", value, gradient))
        live = self.source.xvar(0, 6, 0, 1)
        value = (values["sy0"] * values[live] - 1) % P
        gradient = {
            self.variable_index[live]: values["sy0"],
            self.variable_index["sy0"]: values[live],
        }
        equations.append(("live_A06_01", value, gradient))
        require(len(equations) == 13 and not any(value for _, value, _ in equations),
                [(label, value) for label, value, _ in equations if value])
        return equations

    @staticmethod
    def word_data(word):
        counts = sorted((word.count(c) for c in range(3)), reverse=True)
        return {
            "word": "".join(map(str, word)),
            "off_count": 8 - counts[0],
            "profile": "".join(str(value) for value in counts if value),
        }

    def mixed_equations(self, values):
        words = [word for word in product(range(3), repeat=8)
                 if len(set(word)) > 1]
        words.sort(key=lambda word: (self.word_data(word)["off_count"], word))
        for word in words:
            data = self.word_data(word)
            value, gradient = self.amplitude_and_gradient(values, word)
            yield (f"X5_{data['word']}", value, gradient, data)

    def tangent_core(self, values, branch):
        basis = {}
        selected = []

        def insert(label, value, gradient, metadata):
            row = {column: coefficient % P for column, coefficient in gradient.items()
                   if coefficient % P}
            rhs = (-value) % P
            while row:
                pivot = min(row)
                if pivot not in basis:
                    inverse = pow(row[pivot], P - 2, P)
                    row = {column: coefficient * inverse % P
                           for column, coefficient in row.items()}
                    rhs = rhs * inverse % P
                    basis[pivot] = (row, rhs, label)
                    selected.append({"label": label, **metadata})
                    return "independent"
                brow, brhs, _ = basis[pivot]
                scale = row[pivot]
                for column, coefficient in brow.items():
                    next_value = (row.get(column, 0) - scale * coefficient) % P
                    if next_value:
                        row[column] = next_value
                    elif column in row:
                        del row[column]
                rhs = (rhs - scale * brhs) % P
            return "contradiction" if rhs else "dependent"

        for label, value, gradient in self.base_equations(values, branch):
            outcome = insert(label, value, gradient, {"kind": "base"})
            require(outcome != "contradiction", (branch, label))
        rows_seen = 0
        nonzero_residuals = 0
        residual_histogram = Counter()
        for label, value, gradient, metadata in self.mixed_equations(values):
            rows_seen += 1
            if value:
                nonzero_residuals += 1
                residual_histogram[metadata["profile"]] += 1
            outcome = insert(label, value, gradient, {"kind": "mixed", **metadata})
            if outcome == "contradiction":
                return {
                    "status": "tangent-inconsistent at deterministic normalized branch point",
                    "coefficient_rank_before_contradiction": len(basis),
                    "rows_seen_including_contradiction": 13 + rows_seen,
                    "mixed_rows_seen_including_contradiction": rows_seen,
                    "nonzero_mixed_residuals_seen": nonzero_residuals,
                    "residual_profile_histogram": dict(sorted(residual_histogram.items())),
                    "contradiction_row": {"label": label, **metadata},
                    "selected_independent_row_count": len(selected),
                    "selected_row_labels": selected,
                }
        raise RuntimeError((branch, "all mixed rows were tangent-consistent"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    _, exporter_hash = pinned(EXPORTER, EXPORTER_SHA256)
    manifest_raw, manifest_hash = pinned(MANIFEST, MANIFEST_SHA256)
    manifest = json.loads(manifest_raw)
    source = load_exporter()
    screen = Screen(source)
    records = []
    for seed in SEEDS:
        for branch in source.BRANCHES:
            values, response_rows, pivot_columns, first_edge_minor = screen.construct_base_point(branch, seed)
            record = screen.tangent_core(values, branch)
            record.update({
                "seed": seed,
                "branch": branch,
                "prime": P,
                "base_equations_satisfied": 13,
                "outside_response_rank": len(pivot_columns),
                "outside_response_pivot_rows": pivot_columns,
                "response_edge_03_9x9_minor_mod_p": first_edge_minor,
                "source_value_sha256": sha256(json.dumps(
                    [values[name] for name in screen.xvars], separators=(",", ":")
                ).encode()).hexdigest(),
                "witness_value_sha256": sha256(json.dumps(
                    [values[name] for name in screen.lvars], separators=(",", ":")
                ).encode()).hexdigest(),
            })
            records.append(record)
    require(len(records) == 12, len(records))
    require(all(record["outside_response_rank"] == 9 for record in records), records)
    result = {
        "status": "PASS bounded finite-field normalized-point tangent screen",
        "pins": {"exporter_sha256": exporter_hash,
                 "canonical_manifest_sha256": manifest_hash},
        "prime": P,
        "seeds": list(SEEDS),
        "branch_count": len(source.BRANCHES),
        "variables_per_branch": len(screen.variables),
        "equations_per_branch": len(manifest["full_X5_rows"]) + 13,
        "construction": (
            "Dense deterministic source values; impose A_06[0,1]=1; solve "
            "each pure Hafnian linearly through A_01[c,c]; solve the 9x108 "
            "membership system at response rank 9; then increment literal "
            "X5 rows by off-count and test J*delta=-F over F_32003."
        ),
        "records": records,
        "verdict": (
            "All four branches have exact finite-field points on their "
            "13-equation pure/live/membership base, and every sampled L_triangle "
            "has rank 9, so membership is generically vacuous.  Each sampled "
            "base point is excluded already by a finite literal X5 tangent "
            "core.  This is a local/random-specialization screen, not global "
            "branch UNSAT."
        ),
        "scope_guard": (
            "A tangent contradiction at a nonsolution says no first-order "
            "Newton correction passes through that specialized base point. "
            "It neither proves the nonlinear branch ideal is the unit ideal "
            "nor excludes other components."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = sha256(logical.encode()).hexdigest()
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LOGICAL_SHA256, (digest, EXPECTED_LOGICAL_SHA256))
    result["logical_sha256"] = digest
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered)
    if args.check_results:
        require(OUT.read_text() == rendered, "stored result changed")
    print(result["status"])
    for record in records:
        print(record["seed"], record["branch"],
              "rank", record["coefficient_rank_before_contradiction"],
              "mixed", record["mixed_rows_seen_including_contradiction"],
              "at", record["contradiction_row"]["label"])
    print("logical sha256", digest)


if __name__ == "__main__":
    main()
