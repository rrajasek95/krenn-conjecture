#!/usr/bin/env python3
"""Bézout certificate for the cheapest omitted literal source row.

The full literal census shows that every frozen modular RUR component is
rejected.  This script selects the cheapest omitted row by
``(term count, total degree, serialized length, label)`` and evaluates it
directly in each complete degree-268 RUR quotient.  An explicit inverse
modulo the eliminant gives a compact targeted certificate that the row is
nonzero on every one of the 16 squarefree factors.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_all_minor_components_literal_rows.py"
OUT = HERE / "results_cheapest_omitted_row_unit.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("k4_literal_all_factor_referee", AUDIT_PATH)
nmod_poly = AUDIT.nmod_poly


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def coefficients(poly, length=None):
    size = len(poly) if length is None else length
    return [int(poly[index]) if index < len(poly) else 0
            for index in range(size)]


def support(poly):
    return sum(int(poly[index]) != 0 for index in range(len(poly)))


def poly_digest(poly, length=None):
    return sha256(json.dumps(coefficients(poly, length),
                             separators=(",", ":")).encode("ascii")).hexdigest()


def exact_source_payload(poly):
    return [{"exponents": list(exponents),
             "numerator": Fraction(value).numerator,
             "denominator": Fraction(value).denominator}
            for exponents, value in sorted(poly.items())]


def logical_digest(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def main():
    candidates = []
    sources = {}
    for label, poly, encoded in AUDIT.DIRECT_ROWS:
        if (label.startswith("cofactor_") and label.endswith("_3")
                and label != "cofactor_0_3"):
            profile = {
                "label": label,
                "term_count": len(poly),
                "total_degree": max(map(sum, poly)),
                "serialized_length": len(encoded),
            }
            candidates.append(profile)
            sources[label] = (poly, encoded)
    candidates.sort(key=lambda item: (item["term_count"],
                                      item["total_degree"],
                                      item["serialized_length"],
                                      item["label"]))
    require(candidates[0]["label"] == "cofactor_1_3"
            and candidates[0]["term_count"] == 17
            and candidates[0]["total_degree"] == 6,
            "cheapest omitted-row selection changed")
    chosen = candidates[0]["label"]
    source, source_encoded = sources[chosen]

    prime_certificates = []
    mutation_fired = False
    for prime, rur_path in AUDIT.RURS:
        eliminant, numerators, factors = AUDIT.parse_rur(prime, rur_path)
        values = AUDIT.decode_component(prime, eliminant, numerators)
        residue = AUDIT.evaluate_counter(source, values, eliminant, prime)
        gcd, inverse, bezout_eliminant = residue.xgcd(eliminant)
        require(gcd == nmod_poly([1], prime),
                "omitted row is not a unit in the full squarefree quotient")
        require((residue*inverse) % eliminant == nmod_poly([1], prime),
                "full-quotient inverse replay failed")
        require(residue*inverse + eliminant*bezout_eliminant == gcd,
                "literal extended-gcd identity failed")

        factor_certificates = []
        for index, factor in enumerate(factors):
            factor_residue = residue % factor
            factor_gcd, factor_inverse, _ = factor_residue.xgcd(factor)
            require(factor_gcd == nmod_poly([1], prime)
                    and (factor_residue*factor_inverse) % factor
                    == nmod_poly([1], prime),
                    "factorwise inverse replay failed")
            factor_certificates.append({
                "factor_index": index,
                "factor_degree": factor.degree(),
                "factor_sha256": AUDIT.COMP.poly_digest(factor),
                "residue_degree": factor_residue.degree(),
                "residue_support": support(factor_residue),
                "residue_sha256": poly_digest(factor_residue,
                                               factor.degree()),
                "gcd_coefficients": coefficients(factor_gcd),
                "inverse_degree": factor_inverse.degree(),
                "inverse_support": support(factor_inverse),
                "inverse_sha256": poly_digest(factor_inverse,
                                               factor.degree()),
            })

        mutated = Counter(source)
        key = sorted(mutated)[0]
        mutated[key] = -mutated[key]
        mutated_residue = AUDIT.evaluate_counter(mutated, values,
                                                 eliminant, prime)
        fired = mutated_residue != residue
        require(fired, "source coefficient mutation did not alter residue")
        mutation_fired = mutation_fired or fired
        prime_certificates.append({
            "prime": prime,
            "rur_sha256": sha256(rur_path.read_bytes()).hexdigest(),
            "eliminant_degree": eliminant.degree(),
            "eliminant_coefficients": coefficients(eliminant, 269),
            "eliminant_sha256": AUDIT.COMP.poly_digest(eliminant),
            "residue_degree": residue.degree(),
            "residue_support": support(residue),
            "residue_coefficients": coefficients(residue, 268),
            "residue_sha256": poly_digest(residue, 268),
            "gcd_coefficients": coefficients(gcd),
            "inverse_degree": inverse.degree(),
            "inverse_support": support(inverse),
            "inverse_coefficients": coefficients(inverse, 268),
            "inverse_sha256": poly_digest(inverse, 268),
            "bezout_eliminant_degree": bezout_eliminant.degree(),
            "bezout_eliminant_support": support(bezout_eliminant),
            "bezout_eliminant_sha256": poly_digest(bezout_eliminant, 268),
            "factor_certificates": factor_certificates,
            "must_fire_mutated_residue_sha256": poly_digest(
                mutated_residue, 268),
        })

    require(mutation_fired, "global source mutation guard did not fire")
    result = {
        "status": "UNAUDITED targeted modular RUR unit certificate PASS",
        "candidate_cost_profiles": candidates,
        "selection_rule": (
            "lexicographic minimum of term_count, total_degree, "
            "serialized_length, label"),
        "selected_source_label": chosen,
        "source_variable_order": list(AUDIT.PCOORD.NAMES),
        "exact_source_polynomial": exact_source_payload(source),
        "exact_source_singular": source_encoded,
        "exact_source_sha256": logical_digest(exact_source_payload(source)),
        "prime_certificates": prime_certificates,
        "must_fire": {
            "mutation": "negate lex-first exact source coefficient",
            "changed_residue_at_both_primes": True,
        },
        "scope": (
            "For each displayed prime, the literal cofactor_1_3 row is a "
            "unit in the complete squarefree degree-268 RUR quotient; its "
            "explicit inverse proves it rejects every one of the 16 "
            "frozen factors. This is modular only and does not certify the "
            "positive-dimensional characteristic-zero all-minor scheme."),
    }
    result["result_sha256"] = logical_digest(result)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("cheapest omitted-row full-RUR unit: PASS")
    print("selected:", chosen, candidates[0])
    for certificate in prime_certificates:
        print(certificate["prime"],
              "residue", certificate["residue_degree"],
              certificate["residue_support"],
              "inverse", certificate["inverse_degree"],
              certificate["inverse_support"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
