#!/usr/bin/env python3
"""Two-prime generic-slice signatures for Q3, Q11, and Q7 exceptions."""

from __future__ import annotations

import ast
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

from flint import nmod_poly


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit_Q3_exception_slice_signature.py"
OUT = HERE / "results_sparse_exception_slice_signatures.json"
PRIMES = (1073741827, 1073741789)
EXCEPTIONS = (1, 2, 3, 11, 7)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE = load("generic_cycle_sparse_signature_base", BASE_PATH)
AUDIT = BASE.AUDIT


def parse_rur(index, prime):
    path = HERE / f"results_left_Q{index}_Hlive_slice_p{prime}.param.out"
    encoded = path.read_text().strip()
    if not encoded.endswith(":"):
        raise RuntimeError(f"Q{index} slice delimiter changed")
    payload = ast.literal_eval(encoded[:-1])[1]
    expected_variables = ["b0", "b1", "b3", "d1", "d3", "d4", "z"]
    if (payload[0] != prime or payload[1] != 7 or
            payload[3] != expected_variables or payload[2] <= 0):
        raise RuntimeError(f"Q{index} slice header changed")
    if payload[4] != [0, 0, 0, 0, 0, 0, 1]:
        raise RuntimeError(f"Q{index} separating variable changed")
    data = payload[5][1]
    eliminant = nmod_poly(data[0][1], prime)
    if data[1] != [0, [1]] or eliminant.degree() != payload[2]:
        raise RuntimeError(f"Q{index} eliminant changed")
    unit, factors = eliminant.factor()
    if int(unit) != 1 or any(exponent != 1 for _, exponent in factors):
        raise RuntimeError(f"Q{index} eliminant not monic squarefree")
    numerators = [nmod_poly(record[0][1], prime) for record in data[2]]
    return path, tuple(factor for factor, _ in factors), numerators


def support_signature(index, prime, modulus, numerators, entries_expr,
                      parameters, raw_h, raw_cofactors, raw_q):
    values = tuple((-numerator) % modulus for numerator in numerators)
    entries = tuple(AUDIT.evaluate_rational(expression, parameters, values,
                                            modulus, prime)
                    for expression in entries_expr)
    cofactors = tuple(AUDIT.evaluate_raw(poly, entries, modulus, prime)
                      for poly in raw_cofactors)
    q_values = tuple(AUDIT.evaluate_raw(poly, entries, modulus, prime)
                     for poly in raw_q)
    h_value = AUDIT.evaluate_raw(raw_h, entries, modulus, prime)
    entry_support = frozenset(i for i, value in enumerate(entries) if len(value))
    cofactor_support = frozenset(i for i, value in enumerate(cofactors) if len(value))
    q_support = frozenset(i for i, value in enumerate(q_values) if len(value))
    structural = frozenset(i for i, poly in enumerate(raw_q)
                           if not BASE.specialize(poly, cofactor_support))
    directional = frozenset(15-i for i in q_support)
    uncovered = tuple((i, 15-i) for i in range(8)
                      if not ({i, 15-i} & (structural | directional)))
    return {
        "exception_Q": index,
        "prime": prime,
        "factor_degree": modulus.degree(),
        "entry_support": sorted(entry_support),
        "cofactor_support": sorted(cofactor_support),
        "left_Q_support": sorted(q_support),
        "left_H_nonzero": bool(len(h_value)),
        "structural_mate_Q_zeros": sorted(structural),
        "directional_mate_Q_zeros": sorted(directional),
        "uncovered_complementary_Q_pairs": [list(pair) for pair in uncovered],
    }


def main():
    parameters, entries_expr = AUDIT.raw_left_expressions()
    raw_h = AUDIT.CORE.pure_hafnian()
    raw_cofactors = tuple(AUDIT.PROBE.derivative(raw_h, i) for i in range(24))
    raw_q = tuple(AUDIT.CORE.q_orientation(tuple(
        (i >> (3-site)) & 1 for site in range(4))) for i in range(16))
    records = []
    rur_hashes = {}
    for index in EXCEPTIONS:
        for prime in PRIMES:
            path, factors, numerators = parse_rur(index, prime)
            rur_hashes[f"Q{index}_p{prime}"] = sha256(path.read_bytes()).hexdigest()
            for factor_index, modulus in enumerate(factors):
                record = support_signature(index, prime, modulus, numerators,
                                           entries_expr, parameters, raw_h,
                                           raw_cofactors, raw_q)
                record["factor_index"] = factor_index
                records.append(record)
    def key(record):
        return (tuple(record["entry_support"]),
                tuple(record["cofactor_support"]),
                tuple(record["left_Q_support"]),
                tuple(tuple(pair) for pair in
                      record["uncovered_complementary_Q_pairs"]))
    signature_counts = {}
    agreement = {}
    for index in EXCEPTIONS:
        by_prime = {prime: sorted(key(record) for record in records
                                  if record["exception_Q"] == index and
                                  record["prime"] == prime)
                    for prime in PRIMES}
        agreement[str(index)] = (set(by_prime[PRIMES[0]]) ==
                                 set(by_prime[PRIMES[1]]))
        signature_counts[str(index)] = len(set(
            by_prime[PRIMES[0]] + by_prime[PRIMES[1]]))
    result = {
        "status": "UNAUDITED sparse-exception signature export PASS",
        "records": records,
        "signature_counts": signature_counts,
        "two_prime_signature_agreement": agreement,
        "scope": (
            "Source-replayed generic-slice entry/cofactor/Q incidence for the "
            "five H-live exceptional divisors. Exact B4 transport must "
            "compare the full joint signatures, not only the named Q index."
        ),
        "source_hashes": {
            "base": sha256(BASE_PATH.read_bytes()).hexdigest(),
            "rurs": rur_hashes,
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("sparse exception slice signatures PASS")
    for index in EXCEPTIONS:
        subset = [record for record in records
                  if record["exception_Q"] == index and
                  record["prime"] == PRIMES[0]]
        print("Q", index, [(record["factor_degree"],
                             len(record["entry_support"]),
                             len(record["cofactor_support"]),
                             len(record["left_Q_support"]),
                             record["uncovered_complementary_Q_pairs"])
                            for record in subset])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
