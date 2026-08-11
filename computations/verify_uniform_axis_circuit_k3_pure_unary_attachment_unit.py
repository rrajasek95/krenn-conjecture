#!/usr/bin/env python3
"""Exact source unit against pure-zero unary attachment of the k=3 guard.

Keep the coordinate-11 slice of the c536b88 common quadratic, but replace
its coordinate-00 slice by arbitrary coefficients z_uv on all 28 physical
edges.  This checker constructs the literal eight-site equations

    q^[4] = X0,
    (e1@0+e1@1+e1@2)(e1@7) q^[3] = X1,

and verifies an integral 22-row source identity equal to 1.  Hence no pure
unary attachment can preserve even the aggregate diagonal response.  The
certificate uses neither localization nor a fixed value of z34 or z04.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_axis_circuit_k3_common_q_transfer_guard.py":
        "fe8dc76d8f42dd7ae35ea19934ee12da2c114bfd7d9a7590d33cf821bd0b8065",
    "notes/uniform-axis-circuit-k3-common-q-transfer-guard.md":
        "62f879a04a2d0830a3a870d8ff578b91f62eafe8d9a0248291b9c9d89a6bd7be",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "f37fc9f482f0876ef60701a3b6ef9438244f23f999fd7d360b0f59899a3e529e"
)


Monomial = tuple[str, ...]
Polynomial = Counter[Monomial]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(poly):
    return Counter({monomial: coefficient
                    for monomial, coefficient in poly.items()
                    if coefficient})


def constant(value):
    return Counter({(): value}) if value else Counter()


def variable(name):
    return Counter({(name,): 1})


def add(left, right, scalar=1):
    output = Counter(left)
    for monomial, coefficient in right.items():
        output[monomial] += scalar * coefficient
    return clean(output)


def multiply(left, right):
    output = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            output[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient)
    return clean(output)


def scale(poly, scalar):
    return clean(Counter({monomial: scalar * coefficient
                          for monomial, coefficient in poly.items()}))


@lru_cache(maxsize=None)
def perfect_matchings(sites):
    if not sites:
        return ((),)
    first = sites[0]
    output = []
    for index in range(1, len(sites)):
        second = sites[index]
        remainder = sites[1:index] + sites[index + 1:]
        for matching in perfect_matchings(remainder):
            output.append(((first, second),) + matching)
    return tuple(output)


SITES = tuple(range(8))
EDGES = tuple((left, right) for left in SITES for right in SITES
              if left < right)
EDGE_NAME = {edge: f"z{edge[0]}{edge[1]}" for edge in EDGES}

# The fixed coordinate-11 slice of c536b88.  All other 11 cells vanish.
ONE_SLICE = {
    (1, 2): 1,
    (0, 2): -1,
    (5, 6): 1,
    (2, 5): 1,
    (3, 6): 1,
    (1, 3): -1,
    (1, 4): 1,
}


def q_data():
    q = {}
    for edge in EDGES:
        q[(edge[0], edge[1], 0, 0)] = variable(EDGE_NAME[edge])
    for edge, coefficient in ONE_SLICE.items():
        q[(edge[0], edge[1], 1, 1)] = constant(coefficient)
    return q


def edge_cells(q, edge):
    return tuple((left_colour, right_colour, coefficient)
                 for (left, right, left_colour, right_colour), coefficient
                 in q.items() if (left, right) == edge)


def hafnian(q, sites):
    sites = tuple(sites)
    output = {}
    for matching in perfect_matchings(sites):
        choices = [edge_cells(q, edge) for edge in matching]
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            assignment = {}
            coefficient = constant(1)
            for (left, right), (left_colour, right_colour, value) in zip(
                    matching, selected, strict=True):
                assignment[left] = left_colour
                assignment[right] = right_colour
                coefficient = multiply(coefficient, value)
            word = tuple(assignment[site] for site in sites)
            output[word] = add(output.get(word, Counter()), coefficient)
    return {word: clean(coefficient) for word, coefficient in output.items()
            if clean(coefficient)}


def build_source_generators():
    q = q_data()
    generators = {}

    top = hafnian(q, SITES)
    top_words = set(top) | {(0,) * 8}
    for word in sorted(top_words):
        generator = Counter(top.get(word, Counter()))
        if word == (0,) * 8:
            generator = add(generator, constant(1), -1)
        if generator:
            generators[("top", word)] = generator

    response = {}
    for occupied_site in (0, 1, 2):
        remainder = tuple(site for site in SITES
                          if site not in (occupied_site, 7))
        for word, coefficient in hafnian(q, remainder).items():
            assignment = dict(zip(remainder, word, strict=True))
            assignment[occupied_site] = 1
            assignment[7] = 1
            full_word = tuple(assignment[site] for site in SITES)
            response[full_word] = add(
                response.get(full_word, Counter()), coefficient)

    target = (1,) * 8
    response_words = set(response) | {target}
    for word in sorted(response_words):
        generator = Counter(response.get(word, Counter()))
        if word == target:
            generator = add(generator, constant(1), -1)
        if generator:
            generators[("response", word)] = generator

    return generators


def parse_polynomial(text):
    text = text.replace("-", "+-")
    output = Counter()
    for raw_term in text.split("+"):
        term = raw_term.strip()
        if not term:
            continue
        factors = term.split("*")
        coefficient = 1
        variables = []
        for factor in factors:
            if factor.lstrip("-").isdigit():
                coefficient *= int(factor)
            elif factor.startswith("-"):
                coefficient *= -1
                variables.append(factor[1:])
            else:
                variables.append(factor)
        output[tuple(sorted(variables))] += coefficient
    return clean(output)


# Exact liftstd trace, rewritten by literal source labels rather than row
# indices.  Every entry is a polynomial over Z in the pure-zero cells.
CERTIFICATE = {
    ("top", (0, 0, 0, 0, 0, 0, 0, 0)): "-1",
    ("top", (1, 1, 1, 1, 0, 0, 0, 0)): "z02*z13",
    ("top", (0, 1, 0, 1, 0, 1, 1, 0)): "-z16*z35+z13*z56",
    ("top", (1, 0, 1, 0, 0, 1, 1, 0)): "-z02*z56",
    ("top", (1, 1, 1, 1, 0, 1, 1, 0)):
        "z06*z15*z23+z05*z16*z23+z06*z13*z25+z03*z16*z25+"
        "z05*z13*z26+z03*z15*z26+z06*z12*z35+z01*z26*z35+"
        "z05*z12*z36+z02*z15*z36+z01*z25*z36+z03*z12*z56+"
        "z01*z23*z56",
    ("top", (1, 1, 1, 0, 1, 0, 0, 0)): "-z04*z12",
    ("top", (1, 1, 1, 1, 1, 0, 1, 0)):
        "-z06*z14*z23-z04*z16*z23-z06*z13*z24-z03*z16*z24-"
        "z04*z13*z26-z03*z14*z26-z06*z12*z34-z02*z16*z34-"
        "z01*z26*z34-z02*z14*z36-z01*z24*z36-z03*z12*z46-"
        "z01*z23*z46",
    ("top", (1, 1, 1, 0, 1, 1, 1, 0)):
        "-z06*z15*z24-z05*z16*z24-z06*z14*z25-z04*z16*z25-"
        "z05*z14*z26-z04*z15*z26-z06*z12*z45-z02*z16*z45-"
        "z01*z26*z45-z01*z24*z56",
    ("top", (0, 1, 1, 1, 1, 1, 1, 0)):
        "z15*z26*z34+z13*z26*z45+z12*z34*z56",
    ("response", (0, 1, 1, 1, 1, 0, 1, 1)):
        "z17*z26*z34+z16*z27*z34+z12*z34*z67",
    ("response", (1, 1, 0, 0, 1, 1, 1, 1)):
        "z07*z16*z45+z06*z17*z45+z07*z14*z56+z05*z14*z67+"
        "z01*z45*z67",
    ("response", (0, 1, 0, 0, 0, 1, 1, 1)): "z15*z67",
    ("response", (0, 1, 1, 1, 0, 0, 0, 1)): "-z13*z27",
    ("response", (1, 1, 1, 1, 0, 1, 0, 1)):
        "-z07*z15*z23-z05*z17*z23-z07*z13*z25-z03*z17*z25-"
        "z07*z12*z35-z02*z17*z35-z01*z27*z35-z05*z12*z37-"
        "z02*z15*z37-z01*z25*z37",
    ("response", (1, 1, 0, 1, 0, 1, 1, 1)):
        "-z06*z17*z35-2*z07*z13*z56-z03*z17*z56-"
        "z05*z13*z67-z01*z35*z67",
    ("response", (1, 0, 1, 1, 0, 1, 1, 1)):
        "z07*z26*z35+z06*z27*z35+z02*z35*z67",
    ("response", (1, 1, 1, 0, 1, 1, 0, 1)):
        "z07*z15*z24+z05*z17*z24+z07*z14*z25+z05*z14*z27+"
        "z07*z12*z45+z02*z17*z45+z01*z27*z45",
    ("response", (0, 1, 1, 0, 1, 1, 1, 1)):
        "z17*z26*z45+z16*z27*z45+z12*z45*z67",
    ("response", (1, 1, 0, 0, 1, 0, 0, 1)): "z04*z17",
    ("response", (0, 1, 1, 0, 0, 1, 0, 1)): "z15*z27",
    ("response", (0, 0, 1, 0, 0, 1, 1, 1)): "z27*z56",
    ("response", (1, 1, 0, 1, 1, 0, 1, 1)):
        "z07*z16*z34+z06*z17*z34+z04*z13*z67+z03*z14*z67+"
        "z01*z34*z67",
}


def audit_certificate(generators):
    require(set(CERTIFICATE) <= set(generators),
            "a certified literal source row disappeared")
    total = Counter()
    multiplier_terms = Counter()
    for label, multiplier_text in CERTIFICATE.items():
        multiplier = parse_polynomial(multiplier_text)
        multiplier_terms[len(multiplier)] += 1
        total = add(total, multiply(multiplier, generators[label]))
    require(total == constant(1),
            f"the 22-row source lift no longer expands to one: {total}")
    return {
        "certificate_rows": len(CERTIFICATE),
        "multiplier_term_histogram": dict(sorted(multiplier_terms.items())),
        "expanded_terms": len(total),
        "expanded_value": 1,
        "uses_localization": False,
        "uses_z34_normalization": False,
        "uses_z04_normalization": False,
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    generators = build_source_generators()
    family_counts = Counter(label[0] for label in generators)
    term_histograms = {}
    for family in ("top", "response"):
        histogram = Counter(len(polynomial) for label, polynomial
                            in generators.items() if label[0] == family)
        term_histograms[family] = dict(sorted(histogram.items()))
    require(family_counts == Counter({"top": 24, "response": 23}),
            f"the literal source-row census changed: {family_counts}")

    certificate = audit_certificate(generators)
    ledger = {
        "variables": len(EDGES),
        "pure_zero_slice": "arbitrary z_uv on all 28 physical edges",
        "fixed_one_slice_cells": len(ONE_SLICE),
        "source_rows": dict(sorted(family_counts.items())),
        "source_term_histograms": term_histograms,
        "certificate": certificate,
        "consequence": (
            "no pure-zero unary attachment preserves the aggregate k3 "
            "diagonal response"
        ),
        "remaining_attachment_types": [
            "off-diagonal decoration on a selected anchor edge",
            "deformation of the coordinate-11/22 slices",
            "nonanchor off-diagonal cells already route by 336492c",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"pure unary attachment ledger changed: {digest}")
    print("uniform k3 pure-unary attachment source unit: PASS")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
