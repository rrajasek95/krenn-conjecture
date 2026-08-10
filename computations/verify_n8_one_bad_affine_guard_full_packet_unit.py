#!/usr/bin/env python3
"""Impose the missing one-bad rows on the frozen affine-fibre guard.

The five-cell q from ``verify_n8_one_bad_affine_coordinate_concentration_guard``
has no cell incident with residual site 5.  Hence q^[3] is identically zero
on its entire coefficient/support fibre.  Adding arbitrary multisite p2,s2
and reconstructing the second diagonal response plus both cross-zero rows
does not change this fact: the unary-top residual contains the constant
generator -1.

This checker builds the complete symbolic 36-star-variable response packet
anyway.  The ordinary source certificate is the single physical coefficient

    -g_top[000000] = 1.

Thus this local q-fibre is empty before Hall or concentration enters.  To use
the cancellation circuit inside a full one-bad packet, q itself must deform
outside the frozen five-cell fibre; such a deformation changes q^[2] and its
affine response map and is a different relative problem.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_affine_coordinate_concentration_guard.py":
        "cbc615239037fc5f9664fb1846043a1aa523f716c19d8a03cba4e239c07eb4ab",
    "computations/verify_n8_multisite_full_anchor_cap_quotient.py":
        "7f720829f6dd6bad4236d4226c299a0f03c5d94acecba8c4bace1435166327af",
}
EXPECTED_LEDGER_SHA256 = (
    "6bcfbd5dd391dabed8061702bd8143f0fa31554677bca07701d121699037c8d1"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GUARD_PATH = (
    "computations/verify_n8_one_bad_affine_coordinate_concentration_guard.py"
)
CAP_PATH = "computations/verify_n8_multisite_full_anchor_cap_quotient.py"
guard = load_pinned("one_bad_affine_guard", GUARD_PATH)
# This pin records the full five-row cap quotient and prevents the present
# fibre kill from being misread as a replacement for its unrestricted gate.
require(sha256((ROOT / CAP_PATH).read_bytes()).hexdigest() == PINS[CAP_PATH],
        "the unrestricted full-anchor cap quotient changed")


ZERO_MONOMIAL = ()
P2_OFFSET = 0
S2_OFFSET = 18
VARIABLES = tuple(
    [f"p2_{site}_{colour}"
     for site in guard.SITES for colour in guard.COLOURS]
    + [f"s2_{site}_{colour}"
       for site in guard.SITES for colour in guard.COLOURS]
)


def variable_entry(site, colour, offset):
    index = offset + 3 * site + colour
    return site, colour, {(index,): Fraction(1)}


def fixed_entry(site, colour, coefficient=1):
    return site, colour, {ZERO_MONOMIAL: Fraction(coefficient)}


def multiply_polynomials(left, right, scalar=1):
    result = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] += (
                Fraction(scalar) * left_coefficient * right_coefficient
            )
    return {monomial: coefficient
            for monomial, coefficient in result.items() if coefficient}


def add_polynomial_term(target, polynomial, scalar=1):
    for monomial, coefficient in polynomial.items():
        target[monomial] += Fraction(scalar) * coefficient


def symbolic_response(q, left, right):
    output = defaultdict(lambda: defaultdict(Fraction))
    for u, i, left_coefficient in left:
        for v, j, right_coefficient in right:
            if u == v:
                continue
            complement = tuple(site for site in guard.SITES
                               if site not in (u, v))
            cofactor = guard.hafnian_tensor(q, complement)
            coefficient_product = multiply_polynomials(
                left_coefficient, right_coefficient
            )
            for cofactor_word, coefficient in cofactor.items():
                word = [None] * 6
                word[u], word[v] = i, j
                for site, colour in zip(
                        complement, cofactor_word, strict=True):
                    word[site] = colour
                add_polynomial_term(
                    output[tuple(word)], coefficient_product, coefficient
                )
    return {
        word: {monomial: coefficient
               for monomial, coefficient in polynomial.items() if coefficient}
        for word, polynomial in output.items()
        if any(polynomial.values())
    }


def subtract_target(rows, target_word):
    result = {word: dict(polynomial) for word, polynomial in rows.items()}
    target = defaultdict(Fraction, result.get(target_word, {}))
    target[ZERO_MONOMIAL] -= 1
    result[target_word] = {
        monomial: coefficient for monomial, coefficient in target.items()
        if coefficient
    }
    return {word: polynomial for word, polynomial in result.items()
            if polynomial}


def polynomial_stream(rows):
    return [
        [list(word), [
            [[VARIABLES[index] for index in monomial], str(coefficient)]
            for monomial, coefficient in sorted(polynomial.items())
        ]]
        for word, polynomial in sorted(rows.items())
    ]


def full_packet(q):
    p1 = (fixed_entry(0, 1), fixed_entry(1, 1))
    s1 = (fixed_entry(5, 1),)
    p2 = tuple(variable_entry(site, colour, P2_OFFSET)
               for site in guard.SITES for colour in guard.COLOURS)
    s2 = tuple(variable_entry(site, colour, S2_OFFSET)
               for site in guard.SITES for colour in guard.COLOURS)

    row11 = subtract_target(symbolic_response(q, p1, s1), (1,) * 6)
    row12 = symbolic_response(q, p1, s2)
    row21 = symbolic_response(q, p2, s1)
    row22 = subtract_target(symbolic_response(q, p2, s2), (2,) * 6)
    require(not row11, "the already exact first diagonal response changed")

    top = guard.hafnian_tensor(q, guard.SITES)
    require(top == Counter(), "the frozen q-fibre acquired a top matching")
    top_residual = {(0,) * 6: {ZERO_MONOMIAL: Fraction(-1)}}

    # A constant nonzero generator alone certifies the unit ideal.  Keep the
    # sign/source row explicit rather than relying on a solver verdict.
    top_generator = top_residual[(0,) * 6]
    certificate = {
        monomial: -coefficient
        for monomial, coefficient in top_generator.items()
    }
    require(certificate == {ZERO_MONOMIAL: Fraction(1)},
            "the one-row ordinary source certificate changed")

    streams = {
        "top": polynomial_stream(top_residual),
        "11": polynomial_stream(row11),
        "12": polynomial_stream(row12),
        "21": polynomial_stream(row21),
        "22": polynomial_stream(row22),
    }
    stream_hashes = {
        name: sha256(json.dumps(stream, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
        for name, stream in streams.items()
    }
    term_histograms = {
        name: dict(sorted(Counter(len(polynomial)
                                 for _word, polynomial in rows.items()).items()))
        for name, rows in {
            "top": top_residual, "11": row11, "12": row12,
            "21": row21, "22": row22,
        }.items()
    }
    return {
        "symbolic_star_variables": len(VARIABLES),
        "conceptual_top_rows": 3 ** 6,
        "conceptual_rows_per_response": 3 ** 6,
        "response_labels": ["11=X1", "12=0", "21=0", "22=X2"],
        "nonzero_generator_counts": {
            "top": len(top_residual), "11": len(row11),
            "12": len(row12), "21": len(row21), "22": len(row22),
        },
        "term_count_histograms": term_histograms,
        "generator_stream_sha256": stream_hashes,
        "unit_source_row": "q^[3][000000]-1=-1",
        "ordinary_certificate": "-(q^[3][000000]-1)=1",
        "certificate_rows": 1,
    }


def main():
    q = guard.q_data()
    require(len(q) == 5 and all(site != 5 for key in q
                                for site in key[:2]),
            "the frozen q support stopped omitting site 5")
    packet = full_packet(q)
    ledger = {
        "pins": PINS,
        "frozen_q_cells": [
            f"{u}{v}:{i}{j}={coefficient}"
            for (u, v, i, j), coefficient in sorted(q.items())
        ],
        "full_symbolic_packet": packet,
        "verdict": (
            "the exact full one-bad ideal on the frozen c11e7b7 q-fibre is "
            "the unit ideal: q has no site-5 cell, so q^[3]=0 identically "
            "and the pure unary-top row is the constant generator -1"
        ),
        "concentration_consequence": (
            "none of the added binary rows enforces Hall or coordinate "
            "concentration on this fibre; the unary top deletes the fibre "
            "before those questions arise"
        ),
        "remaining_relative_problem": (
            "a full-packet use of the c11e7b7 circuit must deform q outside "
            "the five-cell/site-5-free fibre while preserving all five "
            "one-bad tensors; that deformation changes q^[2] and its joint "
            "response kernels"
        ),
        "scope": (
            "fixed q/support-and-coefficient fibre from c11e7b7 with arbitrary "
            "multisite p2,s2; not the unrestricted 135-variable q ideal"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"affine-guard full-packet ledger changed: {digest}")

    counts = packet["nonzero_generator_counts"]
    print("N=8 affine-guard full one-bad fibre: PASS")
    print(f"symbolic p2/s2 variables: {packet['symbolic_star_variables']}")
    print(f"nonzero generators top/11/12/21/22: "
          f"{counts['top']}/{counts['11']}/{counts['12']}/"
          f"{counts['21']}/{counts['22']}")
    print("unit certificate: -(q^[3][000000]-1)=1")
    print("Hall/concentration reached: no; unary top kills fibre first")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
