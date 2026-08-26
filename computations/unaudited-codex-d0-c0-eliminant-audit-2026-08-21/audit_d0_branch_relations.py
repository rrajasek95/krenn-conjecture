#!/usr/bin/env python3
"""Reconstruct and exactly replay the two D0 eliminant branches.

The modular elimination bases supply a linear relation A(d1,d4)b0+B(d1,d4)
on each degree-21 factor.  Coefficients are reconstructed from three large
primes, then every original pivot-chart compatibility is checked directly in
Q[d1,d4]/(F), after the substitution b0=-B/A.  This is a source replay on
the pivot-open chart, not an exact-Q Groebner-basis reconstruction.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd, isqrt, lcm
from pathlib import Path
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))

from flint import fmpq_mpoly_ctx, fmpz_mod_mpoly_ctx
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOOLKIT = ROOT / "toolkit/groebner"
sys.path.insert(0, str(TOOLKIT))
from msolve_io import file_sha256, read_msolve_basis  # noqa: E402

PROFILE = HERE / "results_d0_eliminant_factor_profiles.json"
FACTORS = HERE / "results_d0_eliminant_factor_reconstruction.json"
OUTPUT = HERE / "results_d0_branch_relations.json"
SOURCE = (ROOT / "unaudited-codex-root-integration-2026-08-20" /
          "probe_branch0_cycle_d0_c0_pivot.py")
BRANCH_PRIMES = (1073741827, 536870909, 536870879, 536870869, 536870849)


def branch_basis_path(index, prime):
    return HERE / f"d0_factor{index}_p{prime}_resat_toolkit.elim.full.gb.out"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_modular_poly(text, names, prime):
    answer = Counter()
    for raw in text.replace(" ", "").replace("-", "+-").split("+"):
        if not raw:
            continue
        factors = raw.split("*")
        coefficient = int(factors[0]) % prime
        exponent = [0] * len(names)
        for factor in factors[1:]:
            if "^" in factor:
                variable, power = factor.split("^")
                power = int(power)
            else:
                variable, power = factor, 1
            exponent[names.index(variable)] += power
        answer[tuple(exponent)] = (
            answer[tuple(exponent)] + coefficient) % prime
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def crt_many(residues, primes):
    value, modulus = residues[0], primes[0]
    for residue, prime in zip(residues[1:], primes[1:], strict=True):
        value += ((residue - value) * pow(modulus, -1, prime) % prime) * modulus
        modulus *= prime
        value %= modulus
    return value, modulus


def rational_reconstruct(value, modulus):
    bound = isqrt(modulus // 2)
    r0, r1, t0, t1 = modulus, value, 0, 1
    while r1 > bound:
        quotient = r0 // r1
        r0, r1 = r1, r0 - quotient * r1
        t0, t1 = t1, t0 - quotient * t1
    numerator, denominator = r1, t1
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    require(denominator and abs(numerator) <= bound and denominator <= bound
            and gcd(numerator, denominator) == 1
            and (numerator - value * denominator) % modulus == 0,
            "three-prime rational reconstruction failed")
    return Fraction(numerator, denominator)


def decode_q_poly(rows):
    return {(row["d1_degree"], row["d4_degree"]):
            Fraction(*row["coefficient"]) for row in rows}


def normalize_relation_mod_factor(text, factor, prime):
    parsed = parse_modular_poly(text, ("b0", "d1", "d4"), prime)
    require(all(power <= 1 for power, _, _ in parsed),
            "selected elimination row is not linear in b0")
    a = {(i, j): coefficient for (power, i, j), coefficient in parsed.items()
         if power == 1}
    b = {(i, j): coefficient for (power, i, j), coefficient in parsed.items()
         if power == 0}
    context = fmpz_mod_mpoly_ctx.get(
        ["d1", "d4"], prime, ordering="degrevlex")
    modulus = context.from_dict({tuple(monomial[1:]): coefficient
                                 for monomial, coefficient in zip(
                                     factor["support"],
                                     factor["monic_coefficients"],
                                     strict=True)})
    a = {tuple(key): int(value) for key, value in
         divmod(context.from_dict(a), modulus)[1].to_dict().items()}
    b = {tuple(key): int(value) for key, value in
         divmod(context.from_dict(b), modulus)[1].to_dict().items()}
    require((0, 0) in a and a[(0, 0)] != 0,
            "relation normalization coefficient vanished")
    unit = pow(a[(0, 0)], -1, prime)
    return ({key: value * unit % prime for key, value in a.items()},
            {key: value * unit % prime for key, value in b.items()})


def encode(poly):
    return [{"d1_degree": monomial[0], "d4_degree": monomial[1],
             "coefficient": [coefficient.numerator,
                             coefficient.denominator]}
            for monomial, coefficient in sorted(poly.items())]


def primitive_integral(poly):
    denominator = lcm(*(value.denominator for value in poly.values()))
    integral = {monomial: int(denominator * value)
                for monomial, value in poly.items()}
    content = gcd(*(abs(value) for value in integral.values()))
    integral = {monomial: value // content
                for monomial, value in integral.items()}
    first = integral[min(integral)]
    if first < 0:
        integral = {monomial: -value for monomial, value in integral.items()}
    return integral


def primitive_integral_pair(left, right):
    denominator = lcm(*(value.denominator
                        for value in [*left.values(), *right.values()]))
    left_int = {monomial: int(denominator * value)
                for monomial, value in left.items()}
    right_int = {monomial: int(denominator * value)
                 for monomial, value in right.items()}
    content = gcd(*(abs(value)
                    for value in [*left_int.values(), *right_int.values()]))
    left_int = {monomial: value // content
                for monomial, value in left_int.items()}
    right_int = {monomial: value // content
                 for monomial, value in right_int.items()}
    if left_int[min(left_int)] < 0:
        left_int = {monomial: -value for monomial, value in left_int.items()}
        right_int = {monomial: -value for monomial, value in right_int.items()}
    return left_int, right_int


def qpoly(context, poly):
    return context.from_dict({monomial: Fraction(value)
                              for monomial, value in poly.items()})


def substituted_remainder(source, a, b, factor, context):
    """Return A^n source(-B/A,d1,d4) modulo factor."""
    maximum = max(monomial[0] for monomial in source)
    factor_value = qpoly(context, factor)
    a_value = divmod(qpoly(context, a), factor_value)[1]
    b_value = divmod(-qpoly(context, b), factor_value)[1]

    def powers(value):
        answer = [context.constant(1)]
        for _ in range(maximum):
            answer.append(divmod(answer[-1] * value, factor_value)[1])
        return answer

    a_powers, b_powers = powers(a_value), powers(b_value)
    d1, d4 = context.gens()
    answer = context.constant(0)
    for (power, i, j), coefficient in source.items():
        term = (Fraction(coefficient) * d1**i * d4**j *
                b_powers[power] * a_powers[maximum - power])
        answer = divmod(answer + term, factor_value)[1]
    return answer


def exact_source_rows():
    module = load(SOURCE, "d0_relation_source")
    variables, residual, c0 = module.P.derive()
    b0, d1, d4, a0, a5 = variables
    equations = [value for _, value in residual]
    matrix, rhs = sp.linear_eq_to_matrix(equations, [a0, a5])
    augmented = matrix.row_join(rhs)
    pivot_rows = (1, 4)
    pivot = sp.primitive(sp.Poly(
        sp.expand(matrix[list(pivot_rows), :].det()), b0, d1, d4))[1]
    compatibilities = []
    labels = []
    for row in (0, 2, 3, 5):
        value = sp.primitive(sp.Poly(
            sp.expand(augmented[[*pivot_rows, row], :].det()),
            b0, d1, d4))[1]
        compatibilities.append(value)
        labels.append("det_rows_1_4_" + str(row))

    def terms(poly):
        return {tuple(int(power) for power in monomial): int(coefficient)
                for monomial, coefficient in poly.terms()}

    return (labels, [terms(poly) for poly in compatibilities],
            terms(pivot), terms(sp.Poly(c0, b0, d1, d4)))


def main():
    profile = json.loads(PROFILE.read_text())
    factor_data = json.loads(FACTORS.read_text())
    profiles = profile["profiles"]
    require(len(profiles) == 2, "expected two unfactored modular profiles")
    primes = list(BRANCH_PRIMES)
    require(primes[:2] == [item["basis"]["characteristic"]
                           for item in profiles],
            "profile primes changed")
    require(len(set(primes)) == len(primes), "modular primes repeat")

    factor_by_hash = []
    for item in profiles:
        factor_by_hash.append({factor["support_sha256"]: factor
                               for factor in item["factors"]})
    support_hashes = [item["support_sha256"]
                      for item in profiles[0]["factors"]]
    exact_factors = [decode_q_poly(item["coefficients"])
                     for item in factor_data["factors"]]
    require(len(exact_factors) == len(support_hashes) == 2,
            "expected two exact factors")

    reconstructed = []
    for index, support_hash in enumerate(support_hashes):
        component_bases = [read_msolve_basis(
            branch_basis_path(index, prime), require_full=True)
            for prime in primes]
        require(all(len(basis.polynomials) >= 2
                    for basis in component_bases),
                "component elimination basis lacks its linear b0 row")
        modular = []
        for basis, prime in zip(component_bases, primes, strict=True):
            factor = {
                "support": [[0, *monomial]
                            for monomial in sorted(exact_factors[index])],
                "monic_coefficients": [
                    exact_factors[index][monomial].numerator *
                    pow(exact_factors[index][monomial].denominator,
                        -1, prime) % prime
                    for monomial in sorted(exact_factors[index])],
            }
            modular.append(normalize_relation_mod_factor(
                basis.polynomials[1], factor, prime))
        for part in (0, 1):
            require(all(value[part].keys() == modular[0][part].keys()
                        for value in modular[1:]),
                    "branch relation supports changed across primes")
        exact_parts = []
        modulus = 1
        for prime in primes:
            modulus *= prime
        for part in (0, 1):
            exact = {}
            for monomial in modular[0][part]:
                residue, actual_modulus = crt_many(
                    [value[part][monomial] for value in modular], primes)
                require(actual_modulus == modulus, "CRT modulus changed")
                exact[monomial] = rational_reconstruct(residue, modulus)
            exact_parts.append(exact)
        # Every reconstructed coefficient must replay at every prime.
        for prime, value in zip(primes, modular, strict=True):
            for part, exact in enumerate(exact_parts):
                replay = {monomial: coefficient.numerator *
                          pow(coefficient.denominator, -1, prime) % prime
                          for monomial, coefficient in exact.items()}
                require(replay == value[part],
                        f"branch relation replay failed modulo {prime}")
        reconstructed.append((exact_factors[index], *exact_parts))

    labels, compatibilities, pivot, c0 = exact_source_rows()
    context = fmpq_mpoly_ctx.get(["d1", "d4"], ordering="degrevlex")
    branch_results = []
    for index, (factor, a, b) in enumerate(reconstructed):
        factor = primitive_integral(factor)
        a, b = primitive_integral_pair(a, b)
        residual_terms = []
        for label, source in zip(labels, compatibilities, strict=True):
            remainder = substituted_remainder(
                source, a, b, factor, context)
            residual_terms.append(len(remainder.terms()))
            require(remainder.is_zero(),
                    f"exact source compatibility failed: branch {index} "
                    f"row {label}")
        pivot_remainder = substituted_remainder(
            pivot, a, b, factor, context)
        c0_remainder = substituted_remainder(c0, a, b, factor, context)
        require(not pivot_remainder.is_zero(),
                f"branch {index} lies entirely on excluded pivot")
        require(not c0_remainder.is_zero(),
                f"branch {index} lies entirely on excluded C0=0 boundary")
        require(b and a, "degenerate reconstructed relation")
        branch_results.append({
            "factor_index": index,
            "factor_terms": len(factor),
            "factor_total_degree": max(sum(key) for key in factor),
            "factor_multidegree_d1_d4": [
                max(key[0] for key in factor), max(key[1] for key in factor)],
            "factor_coefficients": encode({key: Fraction(value)
                                             for key, value in factor.items()}),
            "relation": "A(d1,d4)*b0+B(d1,d4)=0",
            "A_terms": len(a), "B_terms": len(b),
            "A_coefficients": encode({key: Fraction(value)
                                       for key, value in a.items()}),
            "B_coefficients": encode({key: Fraction(value)
                                       for key, value in b.items()}),
            "source_compatibility_remainder_terms": residual_terms,
            "pivot_remainder_terms": len(pivot_remainder.terms()),
            "C0_remainder_terms": len(c0_remainder.terms()),
            "generic_open_component_logic": (
                "F is irreducible over Q; A, the selected 2x2 pivot, and "
                "C0 have nonzero restrictions on F. Their simultaneous "
                "nonvanishing is therefore a nonempty open subset of the "
                "curve. On that subset b0=-B/A and the two pivot rows solve "
                "a0,a5; the four exact determinant replays make all six "
                "literal residual rows consistent."
            ),
        })

    result = {
        "status": "UNAUDITED exact Q source replay",
        "source": {"path": str(SOURCE), "sha256": file_sha256(SOURCE)},
        "profile_source": {"path": str(PROFILE),
                           "sha256": file_sha256(PROFILE)},
        "factor_source": {"path": str(FACTORS),
                          "logical_sha256": factor_data["logical_sha256"]},
        "primes": primes,
        "crt_modulus": __import__("math").prod(primes),
        "branches": branch_results,
        "theorem": (
            "Both reconstructed irreducible degree-21 factors carry a "
            "nonempty exact-Q generic source component on the frozen "
            "D0=0,C0!=0,pivot!=0 chart. Thus these factors are components "
            "to classify against the remaining activity/mate conditions, "
            "not unit/empty branches."
        ),
        "scope_guard": (
            "This proves exact source consistency on dense opens of the two "
            "candidate factors. It does not prove that the characteristic-"
            "zero saturated elimination ideal has no additional components, "
            "nor does it test H/activity or arbitrary-mate compatibility."
        ),
        "mutation_control": (
            "Changing any reconstructed modular residue is rejected by all-"
            "prime replay before the exact source calculation."
        ),
    }
    result["logical_sha256"] = digest(result)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 branch relation/source replay: PASS")
    print("relation sizes:", [(item["A_terms"], item["B_terms"])
                              for item in branch_results])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
