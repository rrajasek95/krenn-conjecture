#!/usr/bin/env python3
"""Audit the chart gauge normalization and its exact radical formulation."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit_dangerous_charts.py"
SPEC = importlib.util.spec_from_file_location("gauge_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
ORBIT_DATA = (HERE.parent /
              "unaudited-codex-x4-quotient-eliminator-2026-08-20" /
              "results.json")
OUT = HERE / "results_anchor_gauge_specialization.json"
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def audit_hafnian_covariance() -> int:
    checked = 0
    for code in range(3 ** BASE.N):
        digits = []
        value = code
        for _ in range(BASE.N):
            digits.append(value % 3)
            value //= 3
        word = tuple(reversed(digits))
        for term in BASE.word_terms(word):
            ports = [None] * BASE.N
            for cell_id in term:
                u, v, a, b = BASE.CELLS[cell_id]
                require(ports[u] is None and ports[v] is None,
                        "matching term repeats a site")
                ports[u], ports[v] = a, b
            require(tuple(ports) == word,
                    "H_w term has the wrong diagonal-gauge character")
            checked += 1
    require(checked == 3 ** 8 * 105, "full covariance census changed")
    return checked


def audit_forward_anchor_normalization():
    # Twelve arbitrary nonzero values, deliberately all different.
    values = {}
    next_value = 2
    lambdas = {(site, colour): Fraction(1)
               for site in range(BASE.N) for colour in BASE.COLORS}
    for colour in BASE.COLORS:
        for u, v in M0:
            value = Fraction(next_value)
            next_value += 1
            values[(u, v, colour)] = value
            lambdas[(u, colour)] = 1
            lambdas[(v, colour)] = 1 / value
    normalized = {
        key: value * lambdas[(key[0], key[2])] * lambdas[(key[1], key[2])]
        for key, value in values.items()
    }
    require(set(normalized.values()) == {1},
            "the twelve selected cells did not normalize independently")
    characters = {
        colour: product(lambdas[(site, colour)] for site in range(BASE.N))
        for colour in BASE.COLORS
    }
    require(all(value for value in characters.values()),
            "a pure H character vanished")
    return values, lambdas, characters


def product(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def audit_backward_pure_normalization():
    pure_values = (Fraction(17), Fraction(19), Fraction(23))
    lambdas = {(site, colour): Fraction(1)
               for site in range(BASE.N) for colour in BASE.COLORS}
    for colour, value in enumerate(pure_values):
        lambdas[(0, colour)] = 1 / value
    characters = tuple(product(lambdas[(site, colour)]
                               for site in range(BASE.N))
                       for colour in BASE.COLORS)
    require(tuple(characters[c] * pure_values[c] for c in BASE.COLORS)
            == (1, 1, 1), "pure H values did not normalize to one")
    return pure_values, characters


def main() -> None:
    checked = audit_hafnian_covariance()
    values, _lambdas, forward_characters = audit_forward_anchor_normalization()
    pure_values, backward_characters = audit_backward_pure_normalization()
    orbit_data = json.loads(ORBIT_DATA.read_text())
    orbit_count = orbit_data["pure_matching_orbits"]["count"]
    labelled_triples = orbit_data["pure_matching_orbits"]["labelled_triples"]
    require(orbit_count == 31 and labelled_triples == 105 ** 3,
            "pure matching orbit cover changed")
    anchor_count = 3 * len(M0)
    require(len(BASE.CELLS) == 252 and anchor_count == 12,
            "cell/anchor census changed")

    result = {
        "status": "UNAUDITED exact diagonal-gauge specialization audit",
        "base_sha256": sha256(BASE_PATH.read_bytes()).hexdigest(),
        "orbit_data_sha256": sha256(ORBIT_DATA.read_bytes()).hexdigest(),
        "hafnian_terms_checked": checked,
        "gauge_action": (
            "x_{uv}^{ab} maps to lambda_{u,a} lambda_{v,b} x_{uv}^{ab}"
        ),
        "hafnian_character": "H_w maps to (product_v lambda_{v,w_v}) H_w",
        "forward_normalization": {
            "selected_anchor_values": [str(value)
                                       for _key, value in sorted(values.items())],
            "normalized_values_all_one": True,
            "pure_characters": [str(forward_characters[c])
                                for c in BASE.COLORS],
            "reason": (
                "For each colour the selected matching has four disjoint "
                "edges, so the four equations lambda_u lambda_v x_uv=1 "
                "are independent and have nonzero solutions."
            ),
        },
        "backward_normalization": {
            "sample_nonzero_pure_values": [str(value) for value in pure_values],
            "characters": [str(value) for value in backward_characters],
            "normalized_pure_values_all_one": True,
        },
        "ambient_cells": 252,
        "specialized_anchor_cells": anchor_count,
        "specialized_ring_variables": 252 - anchor_count,
        "pure_matching_triples": labelled_triples,
        "pure_matching_triple_orbits": orbit_count,
        "chart_equivalence": (
            "An exact source exists on chart A iff, after setting its twelve "
            "selected anchor variables to 1, there is a common zero of all "
            "mixed H_w at which T=H_0 H_1 H_2 is nonzero."
        ),
        "algebraic_equivalence_over_C": (
            "For J_A generated by the specialized mixed H_w in the "
            "240-variable ring, chart A is excluded iff V(J_A) cap D(T) is "
            "empty iff J_A localized at T is the unit ideal iff T belongs "
            "to radical(J_A) iff T^m belongs to J_A for some m>=1."
        ),
        "global_cover": (
            "The 31 representative charts cover all 105^3 choices of one "
            "nonzero pure perfect-matching term in each H_c. Excluding all "
            "31 specialized charts therefore excludes every exact source."
        ),
        "macaulay_scope_guard": (
            "Homogenize every specialized H_w to degree 4 with t and T to "
            "degree 12. A degree-12 homogeneous exponent-one identity is a "
            "valid positive certificate and dehomogenizes to T in J_A. "
            "Failure of that bounded search is not nonmembership unless "
            "every higher-degree cancellation is included or an exact "
            "global dual is supplied."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("anchor gauge specialization: PASS")
    print("hafnian terms checked:", checked)
    print("charts / specialized variables:", orbit_count, 252 - anchor_count)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
