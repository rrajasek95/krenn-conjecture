#!/usr/bin/env python3
"""Exact selected 7+1 minors for all 2/3 missing-cofactor orbits."""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "results_tail_polar_source_lift.json"
SCREEN = HERE / "results_multi_cofactor_generic_rank_screen.json"
OUT = HERE / "results_multi_cofactor_exact_minors.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    try:
        import sympy as sp
    except ImportError:
        sites = sorted((ROOT / ".venv/lib").glob("python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp

    source = json.loads(SOURCE.read_text())
    screen = json.loads(SCREEN.read_text())
    require(source["logical_sha256"] ==
            "273c321313d8bea2dcd3ea19fe282c078dcfa481d956839607db35100a7612b9",
            "source-lift digest changed")
    require(screen["logical_sha256"] ==
            "03a01ad9f8793dac8bd6c06242831ced622e10a72bf5e7735e3f1c2f60c3a844",
            "multi-cofactor screen digest changed")

    vertices = tuple(range(8))
    edges = tuple(combinations(vertices, 2))
    columns = tuple((site, tail) for tail in (6, 7)
                    for site in range(6))
    column_names = tuple(f"{'y' if tail == 6 else 'z'}{site}"
                         for site, tail in columns)
    diagonal = {(colour, edge): sp.symbols(
        f"g{colour}_{edge[0]}{edge[1]}")
        for colour in range(3) for edge in edges}
    all_symbols = tuple(diagonal.values())

    @lru_cache(None)
    def hafnian(colour, subset):
        subset = tuple(subset)
        if not subset:
            return sp.Integer(1)
        first = subset[0]
        answer = 0
        for index in range(1, len(subset)):
            second = subset[index]
            rest = subset[1:index] + subset[index+1:]
            answer += diagonal[colour, tuple(sorted((first, second)))] * \
                hafnian(colour, rest)
        return sp.expand(answer)

    def coefficient(word, site, tail):
        if word[site] != 0 or word[tail] != 1:
            return sp.Integer(0)
        counts = Counter(word)
        counts[0] -= 1
        counts[1] -= 1
        if any(counts[colour] % 2 for colour in range(3)):
            return sp.Integer(0)
        remaining = tuple(vertex for vertex in vertices
                          if vertex not in (site, tail))
        answer = sp.Integer(1)
        for colour in range(3):
            subset = tuple(vertex for vertex in remaining
                           if word[vertex] == colour)
            answer *= hafnian(colour, subset)
        return sp.expand(answer)

    rows_71 = []
    for word in product(range(3), repeat=8):
        if profile(word) != (7, 1):
            continue
        values = tuple(coefficient(word, *column) for column in columns)
        if any(values):
            rows_71.append({
                "word": word,
                "source_label": "F_" + "".join(map(str, word)),
                "values": values,
            })
    require(len(rows_71) == 8, "7+1 row census changed")

    # Match every compact row against the frozen raw-source ledger.
    frozen = {row["source_label"]: row for row in source["row_ledger"]
              if row["profile"] == "7+1"}
    require(set(frozen) == {row["source_label"] for row in rows_71},
            "frozen 7+1 label set changed")
    for row in rows_71:
        expected = {column_names[index]: str(value)
                    for index, value in enumerate(row["values"]) if value}
        require(frozen[row["source_label"]]["nonzero_columns"] == expected,
                ("raw-source coefficient mismatch", row["source_label"]))

    exact_orbits = {"2": [], "3": []}
    row_by_label = {row["source_label"]: row for row in rows_71}
    exceptional_labels = {
        site: "F_" + "".join(
            "0" if vertex == site else "1" for vertex in vertices)
        for site in range(6)
    }

    def permutation_sign(permutation):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(len(permutation))
                         for j in range(i+1, len(permutation)))
        return -1 if inversions % 2 else 1

    for size in (2, 3):
        for orbit in screen["subset_orbits"][str(size)]:
            missing = tuple(orbit["representative_indices"])
            residual_sites = [columns[index][0] for index in missing]
            repeated = [site for site, count in Counter(residual_sites).items()
                        if count > 1]
            if repeated:
                require(len(repeated) == 1 and residual_sites.count(
                    repeated[0]) == 2,
                    ("unexpected repeated residual pattern", missing))
                selected_labels = ["F_00000001"] + [
                    exceptional_labels[site]
                    for site in sorted(set(residual_sites))
                ]
            else:
                selected_labels = [exceptional_labels[site]
                                   for site in residual_sites]
            require(len(selected_labels) == size,
                    ("selected 7+1 row count changed", missing,
                     selected_labels))
            selected_rows = [row_by_label[label] for label in selected_labels]
            matrix = sp.Matrix([
                [row["values"][column] for column in missing]
                for row in selected_rows
            ])

            # The chosen support is permutation-triangular.  Build the raw
            # determinant as its unique nonzero Leibniz term.  This avoids
            # asking a general factorizer to rediscover an evident product
            # of six-site Hafnians.
            leibniz_terms = []
            for permutation in permutations(range(size)):
                entries = [matrix[row, permutation[row]]
                           for row in range(size)]
                if all(entries):
                    leibniz_terms.append((permutation_sign(permutation),
                                          entries))
            require(len(leibniz_terms) == 1,
                    ("selected matrix ceased to be permutation-triangular",
                     missing, selected_labels))
            coefficient, raw_factors = leibniz_terms[0]
            determinant = coefficient * sp.prod(raw_factors)
            require(sp.expand(matrix.det()-determinant) == 0,
                    ("literal selected determinant mismatch", missing))

            factor_counter = Counter(raw_factors)
            factor_profiles = []
            for factor, multiplicity in sorted(
                    factor_counter.items(), key=lambda item: str(item[0])):
                polynomial = sp.Poly(factor, all_symbols)
                require(sp.factor(factor) == factor,
                        ("six-site Hafnian unexpectedly factored", factor))
                factor_profiles.append({
                    "factor": str(factor),
                    "multiplicity": multiplicity,
                    "total_degree": polynomial.total_degree(),
                    "term_count": len(polynomial.terms()),
                    "colours_used": sorted({int(str(symbol)[1])
                                            for symbol in factor.free_symbols}),
                })
            expanded = sp.Poly(sp.expand(determinant), all_symbols)
            remaining_pivots = [
                f"h2_{site}{tail}"
                for index, (site, tail) in enumerate(columns)
                if index not in missing
            ]
            exact_orbits[str(size)].append({
                "representative_columns": orbit["representative_columns"],
                "orbit_size": orbit["orbit_size"],
                "selected_source_labels": selected_labels,
                "selected_matrix": [[str(value) for value in row]
                                    for row in matrix.tolist()],
                "missing_minor_determinant": str(determinant),
                "integer_content": str(coefficient),
                "determinant_total_degree": expanded.total_degree(),
                "determinant_expanded_term_count": len(expanded.terms()),
                "irreducible_factor_profiles": factor_profiles,
                "localized_remaining_611_pivots": remaining_pivots,
                "full_12x12_minor": (
                    "(" + str(determinant) + ")*"
                    + "*".join(remaining_pivots)),
                "exact_generic_open": (
                    "selected missing minor nonzero, selected h2 factors "
                    "zero, and all listed remaining 611 pivots nonzero"),
                "next_closed_divisor": "V(" + str(determinant) + ")",
            })

    # All selected determinants are independent of G2.  Thus their nonzero
    # opens meet every nonempty G2 cofactor component; no reduction modulo
    # the selected h2 equations is being smuggled into the claim.
    require(all(not any(str(symbol).startswith("g2_")
                        for symbol in sp.sympify(
                            row["missing_minor_determinant"]).free_symbols)
                for size in ("2", "3") for row in exact_orbits[size]),
            "a selected missing minor unexpectedly depends on G2")

    # Mutation: replacing the first selected nonzero entry by zero changes
    # the first exact determinant.
    first = exact_orbits["2"][0]
    mutated = [list(map(sp.sympify, row))
               for row in first["selected_matrix"]]
    old_det = sp.factor(sp.Matrix(mutated).det())
    nonzero_position = next((i, j)
                            for i in range(2) for j in range(2)
                            if mutated[i][j] != 0)
    mutated[nonzero_position[0]][nonzero_position[1]] = 0
    mutation_fired = sp.expand(sp.Matrix(mutated).det()-old_det) != 0
    require(mutation_fired, "selected-minor mutation did not fire")

    result = {
        "status": "PASS exact selected multi-cofactor generic-open minors",
        "selected_row_family": "literal 7+1 source rows",
        "orbit_counts": {"2": len(exact_orbits["2"]),
                         "3": len(exact_orbits["3"])},
        "exact_orbits": exact_orbits,
        "rank_deficient_representatives": [],
        "theorem": (
            "For every fixed-tail orbit of two or three selected h2 pivot "
            "zeros, the displayed raw-source 7+1 minor is a nonzero "
            "polynomial independent of G2. After inverting the remaining "
            "611 pivots and this minor, the full 380x12 source map has rank "
            "12. Its complement is the explicitly displayed next divisor."),
        "scope_guard": (
            "These are exact generic-open theorems, not closures of the "
            "displayed next divisors and not a computation of a full "
            "Fitting ideal."),
        "mutation_guards": {
            "zero_selected_entry_changes_minor": mutation_fired,
        },
        "source_hashes": {
            "source_lift_result": file_hash(SOURCE),
            "generic_screen_result": file_hash(SCREEN),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("multi-cofactor exact minors: PASS", result["logical_sha256"])
    for size in ("2", "3"):
        for row in exact_orbits[size]:
            print(size, row["representative_columns"],
                  row["selected_source_labels"],
                  "terms/factors", row["determinant_expanded_term_count"],
                  len(row["irreducible_factor_profiles"]))


if __name__ == "__main__":
    main()
