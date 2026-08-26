#!/usr/bin/env python3
"""Fast exact b0-resultant builder for the reduced Cof(1,3) interface.

The strict integer msolve rows are parsed without SymPy into FLINT
``fmpz_mpoly`` objects over Z[b1,d1,x].  With

    Q = A*b0^2 + C,      G = g1*b0 + g0,

the exact norm ``A*g0^2 + C*g1^2`` is a necessary b0-free condition for
Q=G=0.  No coefficient or pivot is divided.  Only integer content and the
chart-live monomial b1^a*d1^b*x^c are removed from the exported primitive.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import json
from math import gcd
from pathlib import Path
import re
import sys


_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
from flint import fmpz_mpoly_ctx


HERE = Path(__file__).resolve().parent
VOLTA = HERE.parent / "unaudited-codex-k4-cycle-char0-rur-referee-2026-08-21"
INPUTS = (
    VOLTA / "cofactor13_all_minors_p1073741827.msolve",
    VOLTA / "cofactor13_all_minors_p1073741789.msolve",
)
POLY_OUT = HERE / "cofactor13_qg_resultant_primitive.txt"
LARGE_OUT = HERE / "cofactor13_qg_resultant_large_factor.txt"
RESULT = HERE / "results_cofactor13_qg_resultant_flint.json"
CTX = fmpz_mpoly_ctx.get(("b1", "d1", "x"))
VARIABLES = {"b0": 0, "b1": 1, "d1": 2, "x": 3}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def read_rows(path):
    lines = path.read_text().splitlines()
    require(lines[0] == "b0,b1,d1,x", "input variable order changed")
    prime = int(lines[1])
    rows = tuple(value.strip() for value in
                 "\n".join(lines[2:]).split(",") if value.strip())
    require(len(rows) == 18, "extended input row count changed")
    return prime, rows


def parse_b0_coefficients(text):
    """Return {b0 exponent: polynomial in b1,d1,x}."""
    accum = defaultdict(lambda: defaultdict(int))
    compact = re.sub(r"\s+", "", text)
    require(not any(token in compact for token in ("(", ")", "**")),
            "row escaped strict expanded syntax")
    for encoded in re.findall(r"[+-]?[^+-]+", compact):
        sign = -1 if encoded.startswith("-") else 1
        if encoded[:1] in "+-":
            encoded = encoded[1:]
        coefficient = sign
        exponent = [0, 0, 0, 0]
        saw_symbol = False
        for factor in encoded.split("*"):
            if re.fullmatch(r"\d+", factor):
                require(not saw_symbol,
                        "integer coefficient followed a symbolic factor")
                coefficient *= int(factor)
                continue
            match = re.fullmatch(
                r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?", factor)
            require(match is not None and match.group(1) in VARIABLES,
                    f"unsupported strict factor {factor!r}")
            saw_symbol = True
            exponent[VARIABLES[match.group(1)]] += int(match.group(2) or 1)
        accum[exponent[0]][tuple(exponent[1:])] += coefficient
    return {power: CTX.from_dict({monomial: coefficient
                                  for monomial, coefficient in values.items()
                                  if coefficient})
            for power, values in accum.items()}


def normalized(poly):
    values = poly.to_dict()
    require(values, "zero resultant")
    coefficient_content = 0
    for coefficient in values.values():
        coefficient_content = gcd(coefficient_content, abs(int(coefficient)))
    monomial_content = tuple(int(min(exponent[index] for exponent in values))
                             for index in range(3))
    primitive_dict = {
        tuple(exponent[index]-monomial_content[index]
              for index in range(3)): int(coefficient)//coefficient_content
        for exponent, coefficient in values.items()
    }
    # Deterministic sign: leading lexicographic coefficient positive.
    lead = primitive_dict[max(primitive_dict)]
    sign = 1 if lead > 0 else -1
    primitive = CTX.from_dict({exponent: sign*coefficient
                               for exponent, coefficient
                               in primitive_dict.items()})
    return primitive, int(coefficient_content*sign), monomial_content


def poly_sha(poly):
    logical = [[[int(value) for value in exponent], int(coefficient)]
               for exponent, coefficient in sorted(poly.to_dict().items())]
    return sha256(json.dumps(logical, separators=(",", ":")).encode()).hexdigest()


def profile(poly):
    return {"terms": len(poly), "total_degree": int(poly.total_degree()),
            "degrees_b1_d1_x": [int(value) for value in poly.degrees()],
            "sha256": poly_sha(poly)}


def main():
    ledgers = [read_rows(path) for path in INPUTS]
    require(ledgers[0][0] == 1073741827
            and ledgers[1][0] == 1073741789
            and ledgers[0][1] == ledgers[1][1],
            "two-prime exact integer ledgers diverged")
    rows = ledgers[0][1]
    q = parse_b0_coefficients(rows[0])
    g = parse_b0_coefficients(rows[16])
    require(set(q) == {0, 2} and set(g) == {0, 1},
            "Q/G b0 degree pattern changed")
    a, c = q[2], q[0]
    g1, g0 = g[1], g[0]
    resultant = a*g0*g0 + c*g1*g1
    primitive, scalar_content, monomial_content = normalized(resultant)
    # Literal reconstruction, including the removed factors.
    b1, d1, x = CTX.gens()
    monomial = (b1**monomial_content[0]
                * d1**monomial_content[1]
                * x**monomial_content[2])
    require(resultant == scalar_content*monomial*primitive,
            "normalized resultant failed exact reconstruction")

    unit, factors = primitive.factor()
    require(int(unit) in (-1, 1), "primitive factor unit changed")
    factor_records = [{"multiplicity": int(multiplicity), **profile(factor)}
                      for factor, multiplicity in factors]
    large_factor, large_multiplicity = max(
        factors, key=lambda value: len(value[0]))
    require(int(large_multiplicity) == 1 and len(large_factor) == 3152,
            "large resultant factor profile changed")
    encoded = str(primitive).replace("**", "^")
    POLY_OUT.write_text(encoded + "\n")
    LARGE_OUT.write_text(str(large_factor).replace("**", "^") + "\n")

    # Hostile exact input mutation changes the norm before normalization.
    mutated_g0_dict = g0.to_dict()
    key = min(mutated_g0_dict)
    mutated_g0_dict[key] = -mutated_g0_dict[key]
    mutated_g0 = CTX.from_dict(mutated_g0_dict)
    require(a*mutated_g0*mutated_g0 + c*g1*g1 != resultant,
            "G coefficient mutation did not fire")
    result = {
        "status": "UNAUDITED exact FLINT b0-resultant export PASS",
        "source_rows": ["Q", "cofactor_1_3_cramer_homogenized"],
        "identity": "Res_b0(A*b0^2+C,g1*b0+g0)=A*g0^2+C*g1^2",
        "Q_coefficient_profiles": {"A": profile(a), "C": profile(c)},
        "G_coefficient_profiles": {"g1": profile(g1), "g0": profile(g0)},
        "raw_resultant_profile": profile(resultant),
        "removed_integer_content_signed": scalar_content,
        "removed_chart_live_monomial_b1_d1_x": list(monomial_content),
        "primitive_profile": profile(primitive),
        "factor_count": len(factor_records),
        "factor_profiles": factor_records,
        "primitive_path": POLY_OUT.name,
        "primitive_file_sha256": sha256(POLY_OUT.read_bytes()).hexdigest(),
        "large_factor_path": LARGE_OUT.name,
        "large_factor_profile": profile(large_factor),
        "large_factor_file_sha256": sha256(
            LARGE_OUT.read_bytes()).hexdigest(),
        "input_sha256": [{"prime": prime, "sha256": sha256(
            path.read_bytes()).hexdigest()}
            for (prime, _), path in zip(ledgers, INPUTS, strict=True)],
        "must_fire": "negating the lex-first g0 coefficient changes R_QG",
        "scope": (
            "The primitive is a necessary three-variable condition for "
            "Q=G=0 after removing only integer content and chart-live "
            "monomial powers. It is not by itself a unit or emptiness "
            "certificate."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Cof(1,3) Q/G FLINT resultant: PASS")
    print("primitive:", result["primitive_profile"])
    print("factors:", factor_records)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
