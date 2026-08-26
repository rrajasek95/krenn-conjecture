#!/usr/bin/env python3
"""Two-prime gcd probe for the D0 resultant quotient and one independent pair.

This is discovery until an exact Z/Q gcd or Bezout/subresultant certificate is
replayed.  It derives and strips the literal Cramer rows exactly before any
finite-field conversion.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = (ROOT / "unaudited-codex-root-integration-2026-08-20" /
          "probe_branch0_cycle_d0_c0_pivot.py")
FACTORS = (ROOT / "unaudited-codex-d0-c0-eliminant-audit-2026-08-21" /
           "results_d0_eliminant_factor_reconstruction.json")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def ledger(poly):
    return digest([[*map(int, monomial), int(coefficient)]
                   for monomial, coefficient in sorted(poly.to_dict().items())])


def profile(poly):
    return {"terms": len(poly.to_dict()),
            "total_degree": int(poly.total_degree()),
            "multidegree_b0_d1_d4": list(map(int, poly.degrees())),
            "ledger_sha256": ledger(poly)}


def exact_record(poly):
    value = profile(poly)
    value["coefficient_ledger"] = [
        {"monomial_b0_d1_d4": list(map(int, monomial)),
         "coefficient": int(coefficient)}
        for monomial, coefficient in sorted(poly.to_dict().items())]
    return value


def main():
    from flint import fmpz_mpoly_ctx, nmod_mpoly_ctx

    module = load("d0_exhaustiveness_source", SOURCE)
    sp = module.sp
    variables, residual, _ = module.P.derive()
    b0, d1, d4, a0, a5 = variables
    equations = [value for _, value in residual]
    matrix, rhs = sp.linear_eq_to_matrix(equations, [a0, a5])
    augmented = matrix.row_join(rhs)
    pivot = sp.primitive(sp.Poly(matrix[[1, 4], :].det(),
                                 b0, d1, d4))[1]
    compatibilities = [sp.primitive(sp.Poly(
        augmented[[1, 4, row], :].det(), b0, d1, d4))[1]
        for row in (0, 2, 3, 5)]

    zctx = fmpz_mpoly_ctx.get(["b0", "d1", "d4"], ordering="degrevlex")
    def zconvert(poly):
        return zctx.from_dict({tuple(map(int, monomial)): int(coefficient)
                               for monomial, coefficient in poly.terms()})
    zpivot = zconvert(pivot)
    zstripped = []
    zgcds = []
    for compatibility in compatibilities:
        value = zconvert(compatibility)
        common = value.gcd(zpivot)
        zgcds.append(common)
        zstripped.append(value // common)
    d4z = zctx.gens()[2]
    if zstripped[2] % d4z**2 != 0:
        raise RuntimeError("compatibility 2 d4^2 content changed")
    zstripped[2] //= d4z**2
    shared_13 = zstripped[1].gcd(zstripped[3])
    if shared_13.total_degree() <= 0:
        raise RuntimeError("expected pair (1,3) shared factor disappeared")
    alternative_pairs = ((0,1), (0,2), (0,3), (2,3))
    exact_shared = []
    for pair in ((1,3),) + alternative_pairs:
        common = zstripped[pair[0]].gcd(zstripped[pair[1]])
        exact_shared.append({
            "pair": list(pair),
            "profile": profile(common),
            "positive_b0_degree": int(common.degrees()[0]) > 0,
            "pivot_gcd_profile": profile(common.gcd(zpivot)),
        })
    factor_a = zstripped[0].gcd(zstripped[1])
    factor_b = zstripped[0].gcd(zstripped[2])
    if zstripped[1].gcd(zstripped[3]) != factor_a:
        raise RuntimeError("pairwise factor A pattern changed")
    if zstripped[2].gcd(zstripped[3]) != factor_b:
        raise RuntimeError("pairwise factor B pattern changed")
    if zstripped[0].gcd(zstripped[3]) != factor_a*factor_b:
        raise RuntimeError("pair (0,3) is not exactly A*B")
    if factor_a.gcd(factor_b).total_degree() != 0:
        raise RuntimeError("pairwise factors A,B are no longer coprime")
    reduced_rows = [
        zstripped[0] // (factor_a*factor_b),
        zstripped[1] // factor_a,
        zstripped[2] // factor_b,
        zstripped[3] // (factor_a*factor_b),
    ]
    if any(zstripped[index] != reduced_rows[index] * divisor
           for index, divisor in enumerate(
               (factor_a*factor_b, factor_a, factor_b,
                factor_a*factor_b))):
        raise RuntimeError("exact A/B row decomposition failed")
    exact_all_common = zstripped[0]
    for poly in zstripped[1:]:
        exact_all_common = exact_all_common.gcd(poly)
    if exact_all_common.degrees()[0] != 0:
        raise RuntimeError("unexpected all-four positive-b0 common factor")

    factor_data = json.loads(FACTORS.read_text())
    coefficients = {}
    denominators = []
    for row in factor_data["product_coefficients"]:
        value = Fraction(*row["coefficient"])
        denominators.append(value.denominator)
        coefficients[(0,row["d1_degree"],row["d4_degree"])] = value
    scale = lcm(*denominators)
    integral = {m: int(scale*c) for m,c in coefficients.items()}
    content = gcd(*(abs(c) for c in integral.values()))
    zcandidate = zctx.from_dict({m:c//content for m,c in integral.items()})

    primes = (1073741827, 536870909)
    runs = []
    selected_pair = None
    for prime_index, prime in enumerate(primes):
        ctx = nmod_mpoly_ctx.get(["b0", "d1", "d4"], prime,
                                 ordering="degrevlex")
        def reduce(poly):
            return ctx.from_dict({m:int(c)%prime
                                  for m,c in poly.to_dict().items()})
        stripped = [reduce(poly) for poly in zstripped]
        all_common = stripped[0]
        for poly in stripped[1:]:
            all_common = all_common.gcd(poly)
        candidate = reduce(zcandidate)
        started = time.monotonic()
        r12 = stripped[1].resultant(stripped[2], 0)
        t12 = time.monotonic() - started
        quotient, remainder = divmod(r12, candidate)
        if not remainder.is_zero():
            raise RuntimeError(f"E does not divide R12 mod {prime}")
        zero_13 = stripped[1].resultant(stripped[3], 0)
        if not zero_13.is_zero():
            raise RuntimeError(f"pair (1,3) zero diagnostic failed mod {prime}")
        screened = []
        if prime_index == 0:
            for pair in alternative_pairs:
                started = time.monotonic()
                trial = stripped[pair[0]].resultant(stripped[pair[1]], 0)
                elapsed = time.monotonic() - started
                screened.append({"pair": list(pair), "zero": trial.is_zero(),
                                 "elapsed_seconds_informational": elapsed})
                if not trial.is_zero():
                    selected_pair = pair
                    alternative = trial
                    talternative = elapsed
                    break
        elif selected_pair is not None:
            started = time.monotonic()
            alternative = stripped[selected_pair[0]].resultant(
                stripped[selected_pair[1]], 0)
            talternative = time.monotonic() - started
            if alternative.is_zero():
                raise RuntimeError(f"selected pair becomes zero mod {prime}")
        started = time.monotonic()
        common = (quotient.gcd(alternative)
                  if selected_pair is not None else quotient)
        tgcd = time.monotonic() - started
        factor_constant, factors = common.factor()
        factor_rows = [{"multiplicity": int(multiplicity),
                        "profile": profile(factor)}
                       for factor, multiplicity in factors]
        runs.append({
            "prime": prime,
            "R12": profile(r12),
            "all_four_gcd_over_fraction_field_guard": {
                "profile": profile(all_common),
                "b0_degree": int(all_common.degrees()[0]),
                "interpretation": (
                    "A positive b0-degree fraction-field gcd would clear to "
                    "a positive b0-degree multivariate common divisor."
                ),
            },
            "E": profile(candidate),
            "Q": profile(quotient),
            "R13_zero_diagnostic": True,
            "screened_pairs": screened,
            "selected_pair": list(selected_pair) if selected_pair else None,
            "alternative_resultant": (profile(alternative)
                                      if selected_pair else None),
            "gcd_Q_alternative": (profile(common)
                                  if selected_pair else None),
            "gcd_Q_R13_zero_resultant": profile(quotient),
            "gcd_factor_constant": int(factor_constant),
            "gcd_factors": factor_rows,
            "elapsed_seconds_informational": {"R12": t12,
                                               "alternative": (talternative
                                                               if selected_pair else None),
                                               "gcd": tgcd},
        })
        print("prime", prime, "pair", selected_pair,
              "Q/gcd terms", len(quotient.to_dict()),
              len(common.to_dict()), "factors", factor_rows, flush=True)
    result = {
        "status": "UNAUDITED two-prime D0 alternative resultant gcd probe",
        "source_path": str(SOURCE),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "factor_source_sha256": sha256(FACTORS.read_bytes()).hexdigest(),
        "resultant_pairs": {"frozen": [1,2],
                            "zero_diagnostic": [1,3],
                            "selected_alternative": (list(selected_pair)
                                                     if selected_pair else None)},
        "exact_pair13_shared_factor": profile(shared_13),
        "exact_pairwise_shared_factors": exact_shared,
        "exact_pairwise_factorization": {
            "A": exact_record(factor_a),
            "B": exact_record(factor_b),
            "gcd_A_B": profile(factor_a.gcd(factor_b)),
            "gcd_all_four": profile(exact_all_common),
            "row_divisibility": {
                "compatibility_0": ["A", "B"],
                "compatibility_1": ["A"],
                "compatibility_2": ["B"],
                "compatibility_3": ["A", "B"],
            },
            "reduced_rows_U0_U1_U2_U3": [exact_record(row)
                                          for row in reduced_rows],
            "pivot_open_residual_case_split": [
                "A=0 and U2=0 (because A=B=0 is pivot-empty)",
                "B=0 and U1=0 (because A=B=0 is pivot-empty)",
                "A,B nonzero and U0=U1=U2=U3=0",
            ],
            "pivot_gcd_A": profile(factor_a.gcd(zpivot)),
            "pivot_gcd_B": profile(factor_b.gcd(zpivot)),
        },
        "pivot": profile(zpivot),
        "compatibility_pivot_gcds": [profile(poly) for poly in zgcds],
        "stripped_compatibilities": [profile(poly) for poly in zstripped],
        "candidate": profile(zcandidate),
        "runs": runs,
        "scope": (
            "All alternative raw pairs have zero b0-resultant after the frozen "
            "stripping. No independent-pair gcd conclusion over Q is available."
        ),
    }
    logical = json.loads(json.dumps(result))
    for run in logical["runs"]:
        run.pop("elapsed_seconds_informational")
        for screened in run["screened_pairs"]:
            screened.pop("elapsed_seconds_informational")
    result["logical_sha256"] = digest(logical)
    out = HERE / "results_d0_alternative_resultant_gcd.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("logical sha256", result["logical_sha256"])


if __name__ == "__main__":
    main()
