#!/usr/bin/env python3
"""Factor one elimination polynomial at one or more primes.

This is a discovery/referee tool, not an exact-Q lifting theorem.  It selects
the unique basis element independent of named eliminated variables, factors
it with python-flint, normalizes every factor to monic form, and records
supports, multidegrees, multiplicities, and coefficient vectors.  CRT is
declared eligible only when those structural profiles agree at every prime.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

import sympy as sp
from flint import nmod_mpoly_ctx

from msolve_io import file_sha256, read_msolve_basis


TOOLKIT_VERSION = "1"


def atomic_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def parse_poly(text: str, names: tuple[str, ...], prime: int) -> sp.Poly:
    symbols = sp.symbols(" ".join(names))
    if len(names) == 1:
        symbols = (symbols,)
    locals_map = dict(zip(names, symbols, strict=True))
    expression = sp.sympify(text.replace("^", "**"), locals=locals_map,
                            evaluate=True)
    return sp.Poly(expression, *symbols, modulus=prime)


def to_flint(poly: sp.Poly, names: tuple[str, ...], prime: int):
    context = nmod_mpoly_ctx.get(list(names), prime)
    terms = {tuple(int(value) for value in monomial): int(coefficient) % prime
             for monomial, coefficient in poly.terms()}
    return context.from_dict(terms)


def normalized_factor(value, multiplicity: int, prime: int) -> dict:
    leading = int(value.leading_coefficient()) % prime
    if leading == 0:
        raise ValueError("factor has zero leading coefficient")
    monic = value * pow(leading, -1, prime)
    terms = sorted((tuple(int(item) for item in monomial),
                    int(coefficient) % prime)
                   for monomial, coefficient in monic.to_dict().items())
    support = [list(monomial) for monomial, _ in terms]
    coefficients = [coefficient for _, coefficient in terms]
    multidegree = [max(monomial[index] for monomial, _ in terms)
                   for index in range(len(terms[0][0]))]
    return {
        "multiplicity": int(multiplicity),
        "terms": len(terms),
        "total_degree": int(monic.total_degree()),
        "multidegree": multidegree,
        "support": support,
        "support_sha256": digest(support),
        "monic_coefficients": coefficients,
        "monic_coefficients_sha256": digest(coefficients),
        "polynomial": str(monic),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--basis", action="append", type=Path, required=True)
    parser.add_argument("--exclude-variable", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", action="append", type=Path, default=[])
    parser.add_argument("--scope", required=True)
    args = parser.parse_args()

    profiles = []
    for path in args.basis:
        basis = read_msolve_basis(path, require_full=True)
        unknown = set(args.exclude_variable) - set(basis.variables)
        if unknown:
            raise SystemExit(f"excluded variables absent from basis: {unknown}")
        parsed = [(text, parse_poly(text, basis.variables,
                                    basis.characteristic))
                  for text in basis.polynomials]
        candidates = []
        for text, poly in parsed:
            if poly.total_degree() == 0:
                continue
            if all(poly.degree(variable) <= 0
                   for variable in args.exclude_variable):
                candidates.append((text, poly))
        if len(candidates) != 1:
            raise SystemExit(
                f"expected one nonconstant elimination polynomial in {path}, "
                f"found {len(candidates)}")
        text, poly = candidates[0]
        flint_poly = to_flint(poly, basis.variables, basis.characteristic)
        constant, raw_factors = flint_poly.factor()
        reconstructed = flint_poly.context().constant(constant)
        for factor, multiplicity in raw_factors:
            reconstructed *= factor ** multiplicity
        if reconstructed != flint_poly:
            raise AssertionError("FLINT factor reconstruction failed")
        factors = [normalized_factor(factor, multiplicity,
                                     basis.characteristic)
                   for factor, multiplicity in raw_factors]
        factors.sort(key=lambda item: (
            item["multidegree"], item["support_sha256"],
            item["multiplicity"]))
        profile = [(item["multiplicity"], item["multidegree"],
                    item["support_sha256"]) for item in factors]
        profiles.append({
            "basis": basis.manifest(),
            "selected_polynomial_sha256": sha256(
                text.replace(" ", "").encode()).hexdigest(),
            "selected_terms": len(poly.terms()),
            "selected_total_degree": int(poly.total_degree()),
            "excluded_variables": args.exclude_variable,
            "factor_constant": int(constant),
            "factors": factors,
            "structural_profile": profile,
            "structural_profile_sha256": digest(profile),
        })

    agree = all(item["structural_profile"] ==
                profiles[0]["structural_profile"] for item in profiles[1:])
    result = {
        "toolkit_version": TOOLKIT_VERSION,
        "proof_status": "modular_factor_discovery_only",
        "scope": args.scope,
        "sources": [{"path": str(path), "sha256": file_sha256(path)}
                    for path in args.source],
        "profiles": profiles,
        "profiles_agree_for_coefficient_crt": agree,
        "crt_performed": False,
        "exact_q_replay_required": True,
    }
    result["logical_sha256"] = digest(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    atomic_json(args.output, result)
    print(f"factor profiles: PASS ({result['logical_sha256']})")


if __name__ == "__main__":
    main()
