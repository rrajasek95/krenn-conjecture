#!/usr/bin/env python3
"""Exact orbit-23 T0 gauge slice and bounded X5 tangent-core exporter."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ORBIT_RESULT = (ROOT / "computations/unaudited-codex-x4-quotient-eliminator-2026-08-20"
                / "results.json")
ORBIT_RESULT_SHA256 = "7b61e3c5cc2422087ea6d6d2a4e393fdebfd5df88c4e6eb5805f894ab01f8162"
EXPORTER = (ROOT / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22"
            / "export_canonical_triangle_branch_msolve.py")
EXPORTER_SHA256 = "3abf2f6b61df486679132bf234b6235df12f36e6609b34a1a37886802882959e"
OUT = HERE / "results_orbit23_t0_gauge_x5.json"
CORE = HERE / "orbit23_t0_core_p32003.ms"
EXPECTED_LOGICAL_SHA256 = "3992167f07c0a25e708959edb03d0038eb6ca430905d4b0587492e498de55cf0"
P = 32003
SEED = 2026082317
ORBIT = 23


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pinned(path, expected):
    raw = path.read_bytes()
    actual = sha256(raw).hexdigest()
    require(actual == expected, (str(path), actual, expected))
    return raw, actual


def load_exporter():
    spec = importlib.util.spec_from_file_location("x5_exporter", EXPORTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rational_rank_and_pivots(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_columns = []
    pivot_row = 0
    for column in range(len(work[0])):
        selected = next((row for row in range(pivot_row, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [left - scale * right
                         for left, right in zip(work[row], work[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row, pivot_columns


def determinant(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    answer = Fraction(1)
    for column in range(len(work)):
        selected = next((row for row in range(column, len(work))
                         if work[row][column]), None)
        if selected is None:
            return Fraction(0)
        if selected != column:
            work[column], work[selected] = work[selected], work[column]
            answer = -answer
        pivot = work[column][column]
        answer *= pivot
        for row in range(column + 1, len(work)):
            scale = work[row][column] / pivot
            for entry in range(column, len(work)):
                work[row][entry] -= scale * work[column][entry]
    return answer


def t0_weight(edge, colour):
    i, j = edge
    return [
        int(active_colour == colour)
        * (int(i == site) + int(j == site) - int(i == 7) - int(j == 7))
        for active_colour in range(3)
        for site in range(7)
    ]


def add(row, variable, value):
    value %= P
    if not value:
        return
    value = (row.get(variable, 0) + value) % P
    if value:
        row[variable] = value
    elif variable in row:
        del row[variable]


class Slice:
    def __init__(self, source, matchings):
        self.source = source
        self.matchings = matchings
        self.anchors = [
            source.xvar(u, v, colour, colour)
            for colour, matching in enumerate(matchings)
            for u, v in matching
        ]
        self.fixed = tuple(
            source.xvar(u, v, colour, colour)
            for colour, matching in enumerate(matchings)
            for u, v in matching[:3]
        )
        self.products = tuple(
            source.xvar(*matching[3], colour, colour)
            for colour, matching in enumerate(matchings)
        )
        require(len(self.anchors) == len(set(self.anchors)) == 12,
                self.anchors)
        require(len(self.fixed) == 9 and len(self.products) == 3,
                (self.fixed, self.products))
        self.source_variables = [name for name in source.source_variables()
                                 if name not in self.fixed]
        self.variables = self.source_variables + ["uinv"]
        self.variable_index = {name: index for index, name in enumerate(self.variables)}
        require(len(self.source_variables) == 243 and len(self.variables) == 244,
                len(self.variables))

    def value(self, values, name):
        return 1 if name in self.fixed else values[name]

    def amplitude_and_gradient(self, values, word):
        answer = 0
        gradient = {}
        for matching in self.source.PM8:
            names = [self.source.xvar(u, v, word[u], word[v]) for u, v in matching]
            entries = [self.value(values, name) for name in names]
            term = 1
            for entry in entries:
                term = term * entry % P
            answer = (answer + term) % P
            for index, name in enumerate(names):
                if name in self.fixed:
                    continue
                derivative = 1
                for other, entry in enumerate(entries):
                    if other != index:
                        derivative = derivative * entry % P
                add(gradient, self.variable_index[name], derivative)
        return answer, gradient

    def normalize_pure(self, values, colour):
        pivot = self.products[colour]
        values[pivot] = 0
        without, gradient = self.amplitude_and_gradient(values, (colour,) * 8)
        cofactor = gradient[self.variable_index[pivot]]
        require(cofactor, (colour, "zero anchor cofactor"))
        values[pivot] = (1 - without) * pow(cofactor, P - 2, P) % P
        require(values[pivot], (colour, "anchor product specialized to zero"))
        check, _ = self.amplitude_and_gradient(values, (colour,) * 8)
        require(check == 1, (colour, check))

    def normalized_point(self):
        rng = random.Random(SEED)
        values = {name: rng.randrange(1, P) for name in self.source_variables}
        for colour in range(3):
            self.normalize_pure(values, colour)
        anchor_product = 1
        for name in self.products:
            anchor_product = anchor_product * values[name] % P
        values["uinv"] = pow(anchor_product, P - 2, P)
        return values

    def base_equations(self, values):
        rows = []
        for colour in range(3):
            value, gradient = self.amplitude_and_gradient(values, (colour,) * 8)
            rows.append((f"pure_{colour}", (value - 1) % P, gradient))
        product_value = 1
        for name in self.products:
            product_value = product_value * values[name] % P
        value = (values["uinv"] * product_value - 1) % P
        gradient = {self.variable_index["uinv"]: product_value}
        for omitted, name in enumerate(self.products):
            derivative = values["uinv"]
            for index, other in enumerate(self.products):
                if index != omitted:
                    derivative = derivative * values[other] % P
            gradient[self.variable_index[name]] = derivative
        rows.append(("anchor_product_localizer", value, gradient))
        require(not any(value for _, value, _ in rows), rows)
        return rows

    @staticmethod
    def word_data(word):
        counts = sorted((word.count(colour) for colour in range(3)), reverse=True)
        return {
            "word": "".join(map(str, word)),
            "off_count": 8 - counts[0],
            "profile": "".join(str(count) for count in counts if count),
        }

    def tangent_core(self, values):
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

        for label, value, gradient in self.base_equations(values):
            require(insert(label, value, gradient, {"kind": "base"})
                    != "contradiction", label)
        profile_residuals = Counter()
        mixed_seen = 0
        words = [word for word in product(range(3), repeat=8)
                 if len(set(word)) > 1]
        words.sort(key=lambda word: (self.word_data(word)["off_count"], word))
        for word in words:
            mixed_seen += 1
            metadata = self.word_data(word)
            value, gradient = self.amplitude_and_gradient(values, word)
            if value:
                profile_residuals[metadata["profile"]] += 1
            outcome = insert(f"X5_{metadata['word']}", value, gradient,
                             {"kind": "mixed", **metadata})
            if outcome == "contradiction":
                return {
                    "rank_before_contradiction": len(basis),
                    "mixed_rows_seen_including_contradiction": mixed_seen,
                    "selected_rows": selected,
                    "contradiction_row": {"label": f"X5_{metadata['word']}",
                                          **metadata},
                    "residual_profile_histogram": dict(sorted(profile_residuals.items())),
                }
        raise RuntimeError("full mixed system was tangent-consistent")

    def polynomial(self, word, pure=False):
        polynomial = Counter()
        for matching in self.source.PM8:
            names = tuple(sorted(
                self.source.xvar(u, v, word[u], word[v])
                for u, v in matching
                if self.source.xvar(u, v, word[u], word[v]) not in self.fixed
            ))
            polynomial[names] += 1
        if pure:
            polynomial[()] -= 1
        return {monomial: coefficient for monomial, coefficient in polynomial.items()
                if coefficient}

    @staticmethod
    def render(polynomial):
        terms = []
        for monomial, coefficient in sorted(polynomial.items()):
            body = "*".join(monomial) if monomial else "1"
            if coefficient == 1:
                terms.append(body)
            elif coefficient == -1:
                terms.append(f"-{body}")
            else:
                terms.append(f"{coefficient}*{body}")
        return "+".join(terms).replace("+-", "-") or "0"

    def export_core(self, core):
        mixed_words = [tuple(map(int, row["word"])) for row in core["selected_rows"]
                       if row["kind"] == "mixed"]
        mixed_words.append(tuple(map(int, core["contradiction_row"]["word"])))
        require(len(mixed_words) == len(set(mixed_words)), len(mixed_words))
        rows = [self.render(self.polynomial(word)) for word in mixed_words]
        rows.extend(self.render(self.polynomial((colour,) * 8, pure=True))
                    for colour in range(3))
        rows.append("uinv*" + "*".join(self.products) + "-1")
        require(len(rows) == len(mixed_words) + 4, len(rows))
        with CORE.open("w") as handle:
            handle.write(",".join(self.variables) + f"\n{P}\n")
            for index, row in enumerate(rows):
                handle.write(row)
                handle.write(",\n" if index + 1 < len(rows) else "\n")
        return {
            "variables": len(self.variables),
            "equations": len(rows),
            "mixed_equations": len(mixed_words),
            "input_sha256": sha256(CORE.read_bytes()).hexdigest(),
            "input_bytes": CORE.stat().st_size,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    orbit_raw, orbit_hash = pinned(ORBIT_RESULT, ORBIT_RESULT_SHA256)
    _, exporter_hash = pinned(EXPORTER, EXPORTER_SHA256)
    orbit_data = json.loads(orbit_raw)
    orbit_weight_ranks = []
    for orbit_record in orbit_data["pure_matching_orbits"]["records"]:
        orbit_matchings = tuple(tuple(tuple(edge) for edge in matching)
                                for matching in orbit_record["representative"])
        weights = [t0_weight(edge, colour)
                   for colour, matching in enumerate(orbit_matchings)
                   for edge in matching]
        orbit_weight_ranks.append(rational_rank_and_pivots(weights)[0])
    require(orbit_weight_ranks == [9] * 31, orbit_weight_ranks)
    record = orbit_data["pure_matching_orbits"]["records"][ORBIT]
    require(record["orbit"] == ORBIT and record["selected_physical_pairs"] == 12,
            record)
    matchings = tuple(tuple(tuple(edge) for edge in matching)
                      for matching in record["representative"])
    source = load_exporter()
    slice_data = Slice(source, matchings)

    anchor_weights = [t0_weight(edge, colour)
                      for colour, matching in enumerate(matchings)
                      for edge in matching]
    full_rank, full_pivots = rational_rank_and_pivots(anchor_weights)
    fixed_weights = [t0_weight(edge, colour)
                     for colour, matching in enumerate(matchings)
                     for edge in matching[:3]]
    fixed_rank, fixed_pivots = rational_rank_and_pivots(fixed_weights)
    minor = determinant([[row[column] for column in fixed_pivots]
                         for row in fixed_weights])
    require((full_rank, fixed_rank, minor) == (9, 9, -1),
            (full_rank, fixed_rank, minor))
    # Each colour's four anchor weights sum to its pure character, zero on T0.
    for colour in range(3):
        require(all(sum(anchor_weights[4 * colour + edge][column]
                        for edge in range(4)) == 0 for column in range(21)),
                colour)

    values = slice_data.normalized_point()
    core = slice_data.tangent_core(values)
    export = slice_data.export_core(core)
    result = {
        "status": "PASS exact orbit23 unimodular T0 slice and tangent core",
        "pins": {"31_orbit_result_sha256": orbit_hash,
                 "literal_X5_exporter_sha256": exporter_hash},
        "scope": {
            "matching_triple_orbit": ORBIT,
            "representative": record["representative"],
            "orbit_size": record["orbit_size"],
            "selected_physical_pairs": record["selected_physical_pairs"],
            "all_31_anchor_weight_rank_histogram": {"9": 31},
            "maximal_anchor_weight_rank": max(orbit_weight_ranks),
            "guard": "one certified orbit only; no statement about the other 30 orbits",
        },
        "T0_gauge": {
            "T0_dimension": 21,
            "anchor_variables": slice_data.anchors,
            "anchor_weight_rank": full_rank,
            "fixed_to_one": list(slice_data.fixed),
            "fixed_weight_rank": fixed_rank,
            "unimodular_minor_columns": [
                {"colour": column // 7, "site_difference_to_7": column % 7}
                for column in fixed_pivots
            ],
            "unimodular_minor_determinant": int(minor),
            "invariant_anchor_products_on_slice": list(slice_data.products),
            "remaining_T0_stabilizer_dimension": 21 - fixed_rank,
            "source_variables_before_after": [252, 243],
            "localized_variables_including_inverse": 244,
            "exact_statement": (
                "The determinant -1 character minor makes the nine anchor "
                "normalizations an integral T0 gauge, without extracting roots. "
                "The fourth anchor in each colour equals the invariant product "
                "of that colour's four original anchors."
            ),
        },
        "normalized_specialization": {
            "prime": P,
            "seed": SEED,
            "pure_and_localizer_equations_satisfied": 4,
            "source_value_sha256": sha256(json.dumps(
                [values[name] for name in slice_data.source_variables],
                separators=(",", ":")
            ).encode()).hexdigest(),
            "anchor_product_values": {name: values[name]
                                      for name in slice_data.products},
        },
        "tangent_core": core,
        "nonlinear_core_export": export,
        "verdict": (
            "The certified anchor chart supports only a rank-nine T0 gauge: "
            "the exact source count falls from 252 to 243 (244 with one chart "
            "inverse), while a 12-dimensional T0 stabilizer remains.  The "
            "incremental literal X5 core is exported for one bounded F4 test."
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
        require(export["input_sha256"] == sha256(CORE.read_bytes()).hexdigest(),
                "stored core changed")
    print(result["status"])
    print("anchor rank", full_rank, "fixed rank", fixed_rank, "minor", minor)
    print("variables", export["variables"], "equations", export["equations"])
    print("tangent rank", core["rank_before_contradiction"],
          "at", core["contradiction_row"]["label"])
    print("logical sha256", digest)


if __name__ == "__main__":
    main()
