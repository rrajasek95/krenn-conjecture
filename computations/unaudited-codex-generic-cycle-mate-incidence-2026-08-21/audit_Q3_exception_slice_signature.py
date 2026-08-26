#!/usr/bin/env python3
"""Two-prime incidence signatures on a generic slice of the Q3 exception."""

from __future__ import annotations

import ast
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

from flint import nmod_poly


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_left_slices_export_mate.py"
OUT = HERE / "results_Q3_exception_slice_signature.json"
PRIMES = (1073741827, 1073741789)
GENERIC_COMPACT_COFACTORS = frozenset((1, 2, 6, 10, 14, 18, 21, 22))
GENERIC_COMPACT_LEFT_Q = frozenset((15, 3, 10, 9))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("generic_cycle_Q3_signature_audit", AUDIT_PATH)


def parse_rur(prime):
    path = HERE / f"results_left_Q3_Hlive_slice_p{prime}.param.out"
    encoded = path.read_text().strip()
    if not encoded.endswith(":"):
        raise RuntimeError("Q3 slice RUR delimiter changed")
    envelope = ast.literal_eval(encoded[:-1])
    payload = envelope[1]
    if payload[0] != prime or payload[1:4] != [7, 4,
            ["b0", "b1", "b3", "d1", "d3", "d4", "z"]]:
        raise RuntimeError("Q3 slice RUR header changed")
    if payload[4] != [0, 0, 0, 0, 0, 0, 1]:
        raise RuntimeError("Q3 slice separating variable changed")
    data = payload[5][1]
    eliminant = nmod_poly(data[0][1], prime)
    if data[1] != [0, [1]] or eliminant.degree() != 4:
        raise RuntimeError("Q3 slice eliminant changed")
    unit, factors = eliminant.factor()
    if int(unit) != 1 or any(exponent != 1 for _, exponent in factors):
        raise RuntimeError("Q3 slice eliminant is not monic squarefree")
    numerators = [nmod_poly(record[0][1], prime) for record in data[2]]
    if len(numerators) != 6:
        raise RuntimeError("Q3 slice coordinate count changed")
    return path, eliminant, tuple(factor for factor, _ in factors), numerators


def specialize(poly, zero_cells):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient and not any(index in zero_cells for index in monomial)}


def main():
    parameters, entry_expressions = AUDIT.raw_left_expressions()
    raw_h = AUDIT.CORE.pure_hafnian()
    raw_cofactors = tuple(AUDIT.PROBE.derivative(raw_h, index)
                          for index in range(24))
    raw_q = tuple(AUDIT.CORE.q_orientation(tuple(
        (index >> (3-site)) & 1 for site in range(4))) for index in range(16))
    records = []
    for prime in PRIMES:
        path, eliminant, factors, numerators = parse_rur(prime)
        for factor_index, modulus in enumerate(factors):
            values = tuple((-numerator) % modulus for numerator in numerators)
            entries = tuple(AUDIT.evaluate_rational(
                expression, parameters, values, modulus, prime)
                for expression in entry_expressions)
            cofactors = tuple(AUDIT.evaluate_raw(poly, entries, modulus, prime)
                              for poly in raw_cofactors)
            q_values = tuple(AUDIT.evaluate_raw(poly, entries, modulus, prime)
                             for poly in raw_q)
            h_value = AUDIT.evaluate_raw(raw_h, entries, modulus, prime)
            entry_support = frozenset(index for index, value in enumerate(entries)
                                      if len(value))
            cofactor_support = frozenset(index for index, value in enumerate(cofactors)
                                         if len(value))
            q_support = frozenset(index for index, value in enumerate(q_values)
                                  if len(value))
            structural_mate_q_zeros = frozenset(
                index for index, poly in enumerate(raw_q)
                if not specialize(poly, cofactor_support))
            directional_mate_q_zeros = frozenset(15-index for index in q_support)
            all_mate_q_zeros = structural_mate_q_zeros | directional_mate_q_zeros
            uncovered_pairs = tuple((index, 15-index) for index in range(8)
                                    if not ({index, 15-index} & all_mate_q_zeros))
            records.append({
                "prime": prime,
                "factor_index": factor_index,
                "factor_degree": modulus.degree(),
                "entry_support": sorted(entry_support),
                "cofactor_support": sorted(cofactor_support),
                "left_Q_support": sorted(q_support),
                "left_H_nonzero": bool(len(h_value)),
                "generic_compact_unit_applies": (
                    GENERIC_COMPACT_COFACTORS <= cofactor_support and
                    GENERIC_COMPACT_LEFT_Q <= q_support),
                "structural_mate_Q_zeros": sorted(structural_mate_q_zeros),
                "directional_mate_Q_zeros": sorted(directional_mate_q_zeros),
                "uncovered_complementary_Q_pairs": [list(pair)
                                                       for pair in uncovered_pairs],
                "polarized_Qcover_unit_applies": not uncovered_pairs,
            })
    # The signature may split into conjugate factors, but it must agree as a
    # set between the two large primes.
    def signature(record):
        return (tuple(record["entry_support"]), tuple(record["cofactor_support"]),
                tuple(record["left_Q_support"]),
                tuple(tuple(pair) for pair in
                      record["uncovered_complementary_Q_pairs"]))
    signatures = {prime: sorted(signature(record) for record in records
                                if record["prime"] == prime)
                  for prime in PRIMES}
    if signatures[PRIMES[0]] != signatures[PRIMES[1]]:
        raise RuntimeError("Q3 two-prime signatures disagree")
    result = {
        "status": "UNAUDITED two-prime Q3-exception slice signature PASS",
        "records": records,
        "signature_count": len(signatures[PRIMES[0]]),
        "conclusion": (
            "The Q3=0 H-live exception has the displayed literal incidence "
            "signature. The generic 11-row compact certificate applies only "
            "when its eight cofactor and four Q localizers remain nonzero; "
            "the uncovered-pair field decides whether a reselected polarized "
            "identity already closes the mate."
        ),
        "scope_guard": (
            "This is a source-replayed two-prime generic slice signature, not "
            "a characteristic-zero component classification or mate theorem."
        ),
        "source_hashes": {
            "audit": sha256(AUDIT_PATH.read_bytes()).hexdigest(),
            "rurs": {str(prime): sha256(
                (HERE / f"results_left_Q3_Hlive_slice_p{prime}.param.out").read_bytes()
            ).hexdigest() for prime in PRIMES},
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Q3 exception slice signature PASS")
    for record in records:
        print(record["prime"], record["factor_degree"],
              len(record["cofactor_support"]), len(record["left_Q_support"]),
              record["generic_compact_unit_applies"],
              record["uncovered_complementary_Q_pairs"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
