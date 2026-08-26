#!/usr/bin/env python3
"""Exact-Z source resultant divisibility for the D0 eliminant candidate."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
import sys
import time

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))

from flint import fmpz_mpoly_ctx
import sympy as sp


HERE = Path(__file__).resolve().parent
SOURCE = (HERE.parent / "unaudited-codex-root-integration-2026-08-20" /
          "probe_branch0_cycle_d0_c0_pivot.py")
FACTORS = HERE / "results_d0_eliminant_factor_reconstruction.json"
OUTPUT = HERE / "results_d0_exact_resultant_factor.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def poly_digest(poly):
    rows = [[*(int(value) for value in monomial), int(coefficient)]
            for monomial, coefficient in sorted(poly.to_dict().items())]
    return digest(rows)


def profile(poly):
    return {"terms": len(poly.to_dict()),
            "total_degree": int(poly.total_degree()),
            "multidegree_b0_d1_d4": [int(value) for value in poly.degrees()],
            "coefficient_ledger_sha256": poly_digest(poly)}


def load(path):
    spec = importlib.util.spec_from_file_location("d0_resultant_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main():
    module = load(SOURCE)
    variables, residual, _ = module.P.derive()
    b0, d1, d4, a0, a5 = variables
    equations = [value for _, value in residual]
    matrix, rhs = sp.linear_eq_to_matrix(equations, [a0, a5])
    augmented = matrix.row_join(rhs)
    pivot = sp.primitive(sp.Poly(
        sp.expand(matrix[[1, 4], :].det()), b0, d1, d4))[1]
    compatibilities = [sp.primitive(sp.Poly(
        sp.expand(augmented[[1, 4, row], :].det()), b0, d1, d4))[1]
        for row in (0, 2, 3, 5)]

    context = fmpz_mpoly_ctx.get(
        ["b0", "d1", "d4"], ordering="degrevlex")

    def convert(poly):
        return context.from_dict({tuple(int(value) for value in monomial):
                                  int(coefficient)
                                  for monomial, coefficient in poly.terms()})

    pivot_value = convert(pivot)
    stripped = []
    gcds = []
    for value in compatibilities:
        source = convert(value)
        common = source.gcd(pivot_value)
        gcds.append(common)
        stripped.append(source // common)
    # The third compatibility has one additional exact d4^2 monomial factor.
    _, _, d4_value = context.gens()
    require(stripped[2] % (d4_value**2) == 0,
            "expected d4^2 source factor disappeared")
    stripped[2] //= d4_value**2

    started = time.monotonic()
    resultant = stripped[1].resultant(stripped[2], 0)
    elapsed = time.monotonic() - started

    factor_data = json.loads(FACTORS.read_text())
    product = {}
    denominators = []
    for row in factor_data["product_coefficients"]:
        coefficient = Fraction(*row["coefficient"])
        denominators.append(coefficient.denominator)
        product[(0, row["d1_degree"], row["d4_degree"])] = coefficient
    scale = lcm(*denominators)
    integral = {monomial: int(scale * coefficient)
                for monomial, coefficient in product.items()}
    content = gcd(*(abs(value) for value in integral.values()))
    integral = {monomial: value // content
                for monomial, value in integral.items()}
    candidate = context.from_dict(integral)
    quotient, remainder = divmod(resultant, candidate)
    require(remainder.is_zero(),
            "reconstructed exact eliminant does not divide source resultant")
    mutation_remainder = divmod(resultant, candidate + 1)[1]
    require(not mutation_remainder.is_zero(),
            "candidate +1 mutation did not fire")

    result = {
        "status": "UNAUDITED exact-Z source resultant theorem",
        "source_path": str(SOURCE),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "factor_source_logical_sha256": factor_data["logical_sha256"],
        "pivot": profile(pivot_value),
        "compatibility_pivot_gcds": [profile(value) for value in gcds],
        "stripped_compatibilities": [profile(value) for value in stripped],
        "resultant_pair": [1, 2],
        "resultant": profile(resultant),
        "resultant_elapsed_seconds_informational": elapsed,
        "candidate_primitive_integral_scale_before_content": scale,
        "candidate_content_before_primitive_normalization": content,
        "candidate": profile(candidate),
        "quotient": profile(quotient),
        "remainder_terms": len(remainder.to_dict()),
        "theorem": (
            "The primitive 450-term product of the two reconstructed "
            "degree-21 factors divides exactly over Z the b0-resultant of "
            "the two pivot-stripped literal Cramer compatibilities 1 and 2."
        ),
        "scope_guard": (
            "Resultant divisibility proves that the candidate is an exact "
            "characteristic-zero resultant factor. It does not prove that "
            "every common source zero lies on this factor rather than on "
            "the 14,350-term quotient, and it is not an exact saturated "
            "Groebner-basis reconstruction."
        ),
        "mutation_control": "candidate + 1 has nonzero resultant remainder",
    }
    # Runtime is not logical content.
    logical = dict(result)
    logical.pop("resultant_elapsed_seconds_informational")
    result["logical_sha256"] = digest(logical)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 exact resultant factor: PASS")
    print("resultant/quotient terms:", len(resultant.to_dict()),
          len(quotient.to_dict()))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
