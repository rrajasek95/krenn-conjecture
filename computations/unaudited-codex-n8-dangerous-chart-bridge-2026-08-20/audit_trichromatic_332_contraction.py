#!/usr/bin/env python3
"""Exact (3,3,2) sitewise contrast contraction in the mixed Hafnian ideal."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit_dangerous_charts.py"
SPEC = importlib.util.spec_from_file_location("tri332_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
OUT = HERE / "results_trichromatic_332_contraction.json"

VECTORS = {
    "01": (1, -1, 0),
    "02": (1, 0, -1),
    "12": (0, 1, -1),
}
ASSIGNMENT = ("01", "01", "01", "02", "02", "02", "12", "12")


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def word_coefficient(word: tuple[int, ...]) -> int:
    answer = 1
    for site, colour in enumerate(word):
        answer *= VECTORS[ASSIGNMENT[site]][colour]
    return answer


def weighted_mixed_hafnians() -> tuple[Counter, Counter]:
    polynomial = Counter()
    word_histogram = Counter()
    for word in product(BASE.COLORS, repeat=BASE.N):
        coefficient = word_coefficient(word)
        if not coefficient:
            continue
        require(len(set(word)) > 1,
                "(3,3,2) tensor unexpectedly retained a pure word")
        word_histogram[coefficient] += 1
        for term in BASE.word_terms(word):
            polynomial[term] += coefficient
    return Counter({row: value for row, value in polynomial.items() if value}), word_histogram


def polarized_hafnian() -> Counter:
    answer = Counter()
    for matching in BASE.PM8:
        partial = Counter({b"": 1})
        for u, v in matching:
            left = VECTORS[ASSIGNMENT[u]]
            right = VECTORS[ASSIGNMENT[v]]
            edge = []
            for a in BASE.COLORS:
                for b in BASE.COLORS:
                    coefficient = left[a] * right[b]
                    if coefficient:
                        edge.append((BASE.CELL_ID[(u, v, a, b)], coefficient))
            require(len(edge) == 4, "polarized bilinear edge support changed")
            updated = Counter()
            for row, coefficient in partial.items():
                for cell, edge_coefficient in edge:
                    updated[bytes(sorted(row + bytes((cell,))))] += (
                        coefficient * edge_coefficient
                    )
            partial = updated
        answer.update(partial)
    return Counter({row: value for row, value in answer.items() if value})


def determinant3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def main() -> None:
    require(Counter(ASSIGNMENT) == {"01": 3, "02": 3, "12": 2},
            "site-vector assignment is no longer (3,3,2)")
    pure_coefficients = tuple(word_coefficient((colour,) * BASE.N)
                              for colour in BASE.COLORS)
    require(pure_coefficients == (0, 0, 0),
            "trichromatic contraction does not kill all pure words")
    weighted, word_histogram = weighted_mixed_hafnians()
    polarized = polarized_hafnian()
    require(weighted == polarized,
            "literal mixed-H combination differs from polarized Hafnian")
    require(word_histogram == {-1: 128, 1: 128},
            "(3,3,2) mixed word coefficient census changed")
    require(len(weighted) == 105 * 4 ** 4 == 26_880,
            "polarized Hafnian support changed")

    # All-same contractions have pure coefficient rows (1,1,0), (1,0,1),
    # (0,1,1).  Their determinant is -2, so they coordinatize the complete
    # three-dimensional pure quotient: no linear identity involving only
    # A,B,C can follow from this contraction calculus.
    evaluation_matrix = ((1, 1, 0), (1, 0, 1), (0, 1, 1))
    evaluation_determinant = determinant3(evaluation_matrix)
    require(evaluation_determinant == -2,
            "binary evaluation matrix lost rank")

    mutated = weighted.copy()
    mutated[min(mutated)] += 1
    require(mutated != polarized, "mutation control failed")

    result = {
        "status": "UNAUDITED exact trichromatic (3,3,2) contraction",
        "base_sha256": sha256(BASE_PATH.read_bytes()).hexdigest(),
        "site_vector_assignment": list(ASSIGNMENT),
        "site_vector_histogram": dict(Counter(ASSIGNMENT)),
        "site_assignment_orbit_size": math.factorial(8) // (
            math.factorial(3) * math.factorial(3) * math.factorial(2)
        ),
        "pure_word_coefficients": list(pure_coefficients),
        "mixed_source_words": sum(word_histogram.values()),
        "mixed_source_word_coefficient_histogram": {
            str(k): v for k, v in sorted(word_histogram.items())
        },
        "literal_monomial_support": len(weighted),
        "literal_monomial_coefficient_histogram": {
            str(k): v for k, v in sorted(Counter(weighted.values()).items())
        },
        "bilinear_contrast": (
            "D^{r,s}_{uv}=sum_{a,b} r_a s_b x_{uv}^{ab}"
        ),
        "identity": (
            "P_sigma=sum_M product_{uv in M} D^{sigma_u,sigma_v}_{uv} "
            "=sum_{w mixed}(product_i sigma_i(w_i))*H_w, hence P_sigma "
            "belongs to I_mix for every site assignment using all three "
            "difference-vector types; the displayed audit uses counts3,3,2."
        ),
        "all_same_evaluation_matrix": [list(row) for row in evaluation_matrix],
        "all_same_evaluation_determinant": evaluation_determinant,
        "linear_scope_guard": (
            "The all-same evaluations A,B,C have full rank on the three pure "
            "Hafnians. Therefore the linear contraction identities alone "
            "place no relation on the triple (A,B,C); the (3,3,2) identity "
            "introduces a genuinely mixed polarization P_sigma=0. Forcing "
            "the Heron cubic requires a nonlinear syzygy/product relation "
            "among these mixed polarizations, not another linear contraction."
        ),
        "coefficient_mutation_fires": True,
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("trichromatic (3,3,2) contraction: PASS")
    print("mixed words / monomials:", sum(word_histogram.values()), len(weighted))
    print("all-same determinant:", evaluation_determinant)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
