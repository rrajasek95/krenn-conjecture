#!/usr/bin/env python3
"""Exact tensor identity compressing the three pure Hafnians modulo I_mix."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit_dangerous_charts.py"
SPEC = importlib.util.spec_from_file_location("contrast_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
OUT = HERE / "results_binary_contrast_hafnian_identity.json"

VECTORS = {
    "01": (1, -1, 0),
    "02": (1, 0, -1),
    "12": (0, 1, -1),
}
K_SIGNS = {
    0: {"01": 1, "02": 1, "12": -1},
    1: {"01": 1, "02": -1, "12": 1},
    2: {"01": -1, "02": 1, "12": 1},
}


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def tensor_coefficient(vector: tuple[int, int, int], word: tuple[int, ...]) -> int:
    answer = 1
    for colour in word:
        answer *= vector[colour]
    return answer


def k_coefficient(pure_colour: int, word: tuple[int, ...]) -> Fraction:
    return Fraction(sum(sign * tensor_coefficient(VECTORS[name], word)
                        for name, sign in K_SIGNS[pure_colour].items()), 2)


def weighted_hafnians(pure_colour: int) -> Counter:
    answer = Counter()
    for word in product(BASE.COLORS, repeat=BASE.N):
        coefficient = k_coefficient(pure_colour, word)
        if not coefficient:
            continue
        for term in BASE.word_terms(word):
            answer[term] += coefficient
    return Counter({row: value for row, value in answer.items() if value})


def contrast_hafnian(name: str) -> Counter:
    vector = VECTORS[name]
    answer = Counter()
    for matching in BASE.PM8:
        partial = Counter({b"": 1})
        for u, v in matching:
            edge = []
            for a in BASE.COLORS:
                for b in BASE.COLORS:
                    coefficient = vector[a] * vector[b]
                    if coefficient:
                        edge.append((BASE.CELL_ID[(u, v, a, b)], coefficient))
            require(len(edge) == 4, "binary contrast edge support changed")
            updated = Counter()
            for row, coefficient in partial.items():
                for cell, edge_coefficient in edge:
                    updated[bytes(sorted(row + bytes((cell,))))] += (
                        coefficient * edge_coefficient
                    )
            partial = updated
        answer.update(partial)
    return Counter({row: value for row, value in answer.items() if value})


def add_scaled(target: Counter, source: Counter, coefficient: Fraction) -> None:
    for row, value in source.items():
        target[row] += coefficient * value
        if not target[row]:
            del target[row]


def main() -> None:
    pure_words = [tuple([colour] * BASE.N) for colour in BASE.COLORS]
    pure_values = {
        colour: tuple(k_coefficient(colour, word) for word in pure_words)
        for colour in BASE.COLORS
    }
    require(pure_values == {0: (1, 0, 0), 1: (0, 1, 0), 2: (0, 0, 1)},
            "K_c does not isolate its pure word")

    # Each rank-one tensor factor has coordinate sum zero.  Hence every
    # proper marginal of K_c vanishes; record this explicitly for all subsets
    # of one through seven retained sites via the scalar missing-site factor.
    require(all(sum(vector) == 0 for vector in VECTORS.values()),
            "contrast vector no longer has zero sum")

    contrasts = {name: contrast_hafnian(name) for name in VECTORS}
    checks = []
    weighted = {}
    for colour in BASE.COLORS:
        left = weighted_hafnians(colour)
        right = Counter()
        for name, sign in K_SIGNS[colour].items():
            add_scaled(right, contrasts[name], Fraction(sign, 2))
        require(left == right,
                f"binary contrast identity failed for pure colour {colour}")
        weighted[colour] = left
        mixed_coefficients = Counter(
            k_coefficient(colour, word)
            for word in product(BASE.COLORS, repeat=BASE.N)
            if len(set(word)) > 1 and k_coefficient(colour, word)
        )
        checks.append({
            "pure_colour": colour,
            "weighted_polynomial_support": len(left),
            "coefficient_histogram": {
                str(k): v for k, v in sorted(Counter(left.values()).items())
            },
            "nonzero_mixed_word_coefficient_histogram": {
                str(k): v for k, v in sorted(mixed_coefficients.items())
            },
            "exact_monomial_equality": True,
        })

    # Mutation control: changing one contrast coefficient breaks equality.
    mutated = weighted[0].copy()
    first = min(mutated)
    mutated[first] += 1
    require(mutated, "mutation setup became vacuous")
    expected0 = Counter()
    for name, sign in K_SIGNS[0].items():
        add_scaled(expected0, contrasts[name], Fraction(sign, 2))
    require(mutated != expected0, "coefficient mutation did not fire")

    result = {
        "status": "UNAUDITED exact binary-contrast Hafnian identity",
        "base_sha256": sha256(BASE_PATH.read_bytes()).hexdigest(),
        "contrast_definition": (
            "D^{pq}_{uv}=x^{pp}_{uv}-x^{pq}_{uv}-x^{qp}_{uv}+x^{qq}_{uv}"
        ),
        "contrast_hafnian_support": {
            name: len(polynomial) for name, polynomial in contrasts.items()
        },
        "tensor_definition": (
            "K0=((e0-e1)^tensor8+(e0-e2)^tensor8-(e1-e2)^tensor8)/2; "
            "K1 and K2 are obtained cyclically."
        ),
        "pure_word_coefficients": {
            str(colour): [str(value) for value in values]
            for colour, values in pure_values.items()
        },
        "proper_marginals_of_Kc": "zero for every retained-site set of size <8",
        "checks": checks,
        "exact_identities": [
            "H0 + sum_{w mixed} K0(w) H_w = (A+B-C)/2",
            "H1 + sum_{w mixed} K1(w) H_w = (A+C-B)/2",
            "H2 + sum_{w mixed} K2(w) H_w = (B+C-A)/2",
        ],
        "quotient_consequence": (
            "With A=Haf(D01), B=Haf(D02), C=Haf(D12), "
            "8*T=(A+B-C)(A+C-B)(B+C-A) modulo I_mix."
        ),
        "normalized_source_consequence": (
            "At an exact source H0=H1=H2=1 and all mixed H_w=0, the three "
            "linear identities force A=B=C=2."
        ),
        "conormal_consequence": (
            "At every colour-blind point x_{uv}^{ab}=z_{uv}, all D^{pq}=0. "
            "Modulo the mixed equations each pure H_c is represented by a "
            "quartic in the transverse colour contrasts, so its derivatives "
            "of orders 1,2,3 lie in the corresponding mixed derivative span; "
            "in particular the pure gradients add no Jacobian rank."
        ),
        "coefficient_mutation_fires": True,
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("binary contrast Hafnian identity: PASS")
    print("contrast supports:", {name: len(p) for name, p in contrasts.items()})
    print("weighted supports:", [len(weighted[c]) for c in BASE.COLORS])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
