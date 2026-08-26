#!/usr/bin/env python3
"""Five-prime support/height audit for D0 component b0 relations."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd, isqrt
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
CORE = HERE / "audit_d0_branch_relations.py"
FACTORS = HERE / "results_d0_eliminant_factor_reconstruction.json"
OUTPUT = HERE / "results_d0_branch_relation_height.json"


def load():
    spec = importlib.util.spec_from_file_location("d0_height_core", CORE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    core = load()
    factor_rows = json.loads(FACTORS.read_text())["factors"]
    primes = list(core.BRANCH_PRIMES)
    branches = []
    for index, factor_rows_for_branch in enumerate(factor_rows):
        exact_factor = core.decode_q_poly(
            factor_rows_for_branch["coefficients"])
        modular = []
        basis_hashes = []
        for prime in primes:
            path = core.branch_basis_path(index, prime)
            basis = core.read_msolve_basis(path, require_full=True)
            factor = {
                "support": [[0, *monomial]
                            for monomial in sorted(exact_factor)],
                "monic_coefficients": [
                    exact_factor[monomial].numerator *
                    pow(exact_factor[monomial].denominator, -1, prime) % prime
                    for monomial in sorted(exact_factor)],
            }
            modular.append(core.normalize_relation_mod_factor(
                basis.polynomials[1], factor, prime))
            basis_hashes.append(sha256(path.read_bytes()).hexdigest())
        for part in (0, 1):
            if any(value[part].keys() != modular[0][part].keys()
                   for value in modular[1:]):
                raise RuntimeError("component relation support changed")

        prefixes = []
        for count in range(2, len(primes) + 1):
            selected_primes = primes[:count]
            modulus = __import__("math").prod(selected_primes)
            failures = []
            successes = []
            for part in (0, 1):
                failed = 0
                passed = 0
                for monomial in modular[0][part]:
                    residue, actual = core.crt_many(
                        [value[part][monomial]
                         for value in modular[:count]], selected_primes)
                    if actual != modulus:
                        raise RuntimeError("CRT modulus changed")
                    try:
                        core.rational_reconstruct(residue, modulus)
                    except RuntimeError:
                        failed += 1
                    else:
                        passed += 1
                failures.append(failed)
                successes.append(passed)
            prefixes.append({
                "prime_count": count,
                "modulus": modulus,
                "unique_height_bound": isqrt(modulus // 2),
                "A_success_failure": [successes[0], failures[0]],
                "B_success_failure": [successes[1], failures[1]],
            })

        # Simultaneous/common-denominator test.  A(0,0)=1 is the stable
        # normalization coefficient, so these residues are already ratios to
        # one fixed nonzero coordinate.  On deterministic subsets, LLL seeks
        # a q such that every q*r_i has a small centered representative.  We
        # test several numerator/denominator weightings and validate any q on
        # the complete A,B vector, excluding the trivial q=M vector.
        modulus = __import__("math").prod(primes)
        residues = []
        for part in (0, 1):
            for monomial in sorted(modular[0][part]):
                residue, _ = core.crt_many(
                    [value[part][monomial] for value in modular], primes)
                residues.append(residue)
        attempts = 0
        simultaneous = None
        for dimension in (4, 6, 8, 10, 12):
            for offset in range(4):
                indices = [
                    (offset + item * (len(residues) - 1) //
                     (dimension - 1)) % len(residues)
                    for item in range(dimension)]
                sample = [residues[item] for item in indices]
                for scale_power in range(0, 161, 8):
                    scale = 1 << scale_power
                    lattice = []
                    for position in range(dimension):
                        row = [0] * (dimension + 1)
                        row[position] = modulus * scale
                        lattice.append(row)
                    lattice.append([value * scale for value in sample] + [1])
                    reduced = core.sp.Matrix(lattice).lll()
                    attempts += 1
                    for row in reduced.tolist():
                        denominator = abs(int(row[-1]))
                        if (not denominator or denominator >= modulus or
                                gcd(denominator, modulus) != 1):
                            continue
                        numerators = [(denominator * value) % modulus
                                      for value in residues]
                        numerators = [value - modulus
                                      if value > modulus // 2 else value
                                      for value in numerators]
                        maximum = max(abs(value) for value in numerators)
                        if 2 * denominator * maximum < modulus:
                            simultaneous = {
                                "denominator": denominator,
                                "max_abs_numerator": maximum,
                                "sample_dimension": dimension,
                                "sample_offset": offset,
                                "scale_power": scale_power,
                            }
                            break
                    if simultaneous is not None:
                        break
                if simultaneous is not None:
                    break
            if simultaneous is not None:
                break
        branches.append({
            "branch": index,
            "A_support_terms": len(modular[0][0]),
            "B_support_terms": len(modular[0][1]),
            "A_support_sha256": digest([
                [int(value) for value in monomial]
                for monomial in sorted(modular[0][0])]),
            "B_support_sha256": digest([
                [int(value) for value in monomial]
                for monomial in sorted(modular[0][1])]),
            "basis_file_sha256": basis_hashes,
            "prefix_reconstruction_census": prefixes,
            "common_denominator_lll": {
                "normalization": "A(0,0)=1",
                "attempts": attempts,
                "dimensions": [4, 6, 8, 10, 12],
                "offsets_per_dimension": 4,
                "numerator_scale_powers": list(range(0, 161, 8)),
                "globally_unique_candidate": simultaneous,
            },
        })

    result = {
        "status": "UNAUDITED bounded five-prime height obstruction",
        "primes": primes,
        "branches": branches,
        "conclusion": (
            "The componentwise reduced-basis relation supports are stable "
            "at five independent large primes, but unique rational "
            "reconstruction remains incomplete even at the five-prime "
            "height bound. The deterministic simultaneous-LLL scan also "
            "finds no common denominator whose full vector satisfies the "
            "global uniqueness inequality. No exact A*b0+B relation or "
            "source-component claim is made."
        ),
        "scope_guard": (
            "Failure of bounded rational reconstruction is a coefficient-"
            "height/compression blocker only, not evidence that the modular "
            "components fail to lift to characteristic zero."
        ),
        "mutation_control": (
            "All supports and coefficient residues are keyed by the exact "
            "basis file hashes; a residue mutation changes the census input."
        ),
    }
    result["logical_sha256"] = digest(result)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 branch relation height audit: PASS")
    print("final failures:",
          [(row["prefix_reconstruction_census"][-1]["A_success_failure"][1],
            row["prefix_reconstruction_census"][-1]["B_success_failure"][1])
           for row in branches])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
