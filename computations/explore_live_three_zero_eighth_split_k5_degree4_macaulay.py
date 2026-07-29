#!/usr/bin/env python3
"""Explore a bounded degree-4 affine certificate for the k=5 d=9 K5 system.

This is deliberately an exploratory, one-parameter calculation.  It works
over GF(32003)(a), with anchors (a,2,3,4), singleton 30, and candidates
(5,6,7,8,9).  It asks whether 1 is in the linear span of

    {m Q_j : deg(m) <= 2, 1 <= j <= 5} union {F_01}.

There are 76 products with one edge, or 80 with the connected odd-cycle
edge set, and 70 monomials of degree at most four.  Several column-order
charts are used only to expose different denominator minors; their gcd is a
diagnostic for structural localization, not a uniform proof.
"""

from __future__ import annotations

import argparse
import itertools
import random
import re
import subprocess
from dataclasses import dataclass

import sympy as sp


PRIME = 32003
CANDIDATES = (5, 6, 7, 8, 9)
VARIABLES = ("k0", "k1", "k2", "k3")
CHARTS = (1701, 2903, 4517, 6361)


def inverse(value: int) -> int:
    return pow(value % PRIME, -1, PRIME)


def centered(value: int) -> str:
    value %= PRIME
    return str(value if value <= PRIME // 2 else value - PRIME)


def numeric_phi(anchor: int, candidate: int) -> int:
    return (5 * anchor + candidate) * inverse(anchor * anchor - candidate * candidate) % PRIME


def monomial(exponents: tuple[int, int, int, int]) -> str:
    factors: list[str] = []
    for variable, exponent in zip(VARIABLES, exponents, strict=True):
        if exponent == 1:
            factors.append(variable)
        elif exponent > 1:
            factors.append(f"{variable}^{exponent}")
    return "*".join(factors) or "1"


def exponent_tuples(max_degree: int) -> list[tuple[int, int, int, int]]:
    return [
        exponents
        for exponents in itertools.product(range(max_degree + 1), repeat=4)
        if sum(exponents) <= max_degree
    ]


def row_entries(anchor: str | int, x: int, y: int, variable: str) -> list[str]:
    if anchor == "a":
        xi = "(a-30)"
        phi_x = f"((5a+{x})/(a^2-{x * x}))"
        phi_y = f"((5a+{y})/(a^2-{y * y}))"
    else:
        xi = centered(anchor - 30)
        phi_x = centered(numeric_phi(anchor, x))
        phi_y = centered(numeric_phi(anchor, y))
    jet = f"({variable}-({phi_x})-({phi_y}))"
    return [
        f"(1+2*({xi})*({jet}))",
        f"(({xi})*(2+2*({xi})*({jet})))",
        f"(({xi})^2*(3+2*({xi})*({jet})))",
        f"(({xi})^3*(4+2*({xi})*({jet})))",
    ]


def singular_program(chart: int, edge_products: tuple[str, ...]) -> str:
    lines = [
        'LIB "linalg.lib";',
        "ring R=(32003,a),(k0,k1,k2,k3),dp;",
        "option(redSB);",
    ]
    for i, x in enumerate(CANDIDATES):
        for j in range(i + 1, 5):
            entries: list[str] = []
            for anchor, variable in zip(("a", 2, 3, 4), VARIABLES, strict=True):
                entries.extend(row_entries(anchor, x, CANDIDATES[j], variable))
            lines.extend(
                [
                    f"matrix D{i}{j}[4][4]=" + ",".join(entries) + ";",
                    f"poly f{i}{j}=det(D{i}{j});",
                ]
            )
    q_definitions = (
        "f01+f23-f02-f13",
        "f01+f23-f03-f12",
        "f01+f24-f02-f14",
        "f01+f24-f04-f12",
        "f01+f34-f03-f14",
    )
    for index, definition in enumerate(q_definitions, 1):
        lines.append(f"poly q{index}={definition};")

    basis = sorted(exponent_tuples(4), key=lambda item: (sum(item), item))
    multipliers = sorted(exponent_tuples(2), key=lambda item: (sum(item), item))
    products = [
        f"({monomial(exponents)})*q{q_index}"
        for q_index in range(1, 6)
        for exponents in multipliers
    ] + list(edge_products)
    random.Random(chart).shuffle(products)
    lines.append("list PP;")
    for column, product in enumerate(products, 1):
        lines.append(f"PP[{column}]={product};")
    product_count = len(products)

    lines.extend(["intvec POS;", "POS[625]=0;"])
    for index, exponents in enumerate(basis, 1):
        code = exponents[0] + 5 * exponents[1] + 25 * exponents[2] + 125 * exponents[3]
        lines.append(f"POS[{code + 1}]={index};")
    constant_row = basis.index((0, 0, 0, 0)) + 1

    lines.extend(
        [
            f"matrix MM[70][{product_count}];",
            "int jj; int code; int row; intvec ee; poly gg;",
            f"for(jj=1;jj<={product_count};jj++)",
            "{",
            "  gg=PP[jj];",
            "  while(gg!=0)",
            "  {",
            "    ee=leadexp(gg);",
            "    code=ee[1]+5*ee[2]+25*ee[3]+125*ee[4];",
            "    row=POS[code+1];",
            "    MM[row,jj]=leadcoef(gg);",
            "    gg=gg-lead(gg);",
            "  }",
            "}",
            "matrix bb[70][1];",
            f"bb[{constant_row},1]=1;",
            # linalg.lib's linsolve has a one-index assignment bug for an
            # underdetermined matrix.  This local version fixes that typo.
            "proc boundedSolve(matrix A,matrix b)",
            "{",
            "  int n=nrows(A); int m=ncols(A);",
            "  matrix Ab[n][m+1]; matrix X[m][1];",
            "  int i,j,k,piv,allzero; poly c;",
            "  for(i=1;i<=n;i++)",
            "  {",
            "    for(j=1;j<=m;j++){Ab[i,j]=A[i,j];}",
            "    Ab[i,m+1]=b[i,1];",
            "  }",
            "  list Z=gaussred(Ab); Ab=Z[3]; int rr=Z[4];",
            "  for(i=1;i<=n;i++)",
            "  {",
            "    allzero=1;",
            "    for(j=1;j<=m;j++){if(Ab[i,j]!=0){allzero=0;break;}}",
            '    if((allzero==1)&&(Ab[i,m+1]!=0)){"NOSOLUTION";return(X);}',
            "  }",
            "  k=m;",
            "  for(i=rr;i>=1;i--)",
            "  {",
            "    piv=1; while((piv<=m)&&(Ab[i,piv]==0)){piv++;}",
            "    if(piv>m){continue;}",
            "    for(;k>piv;k--){X[k,1]=0;}",
            "    c=Ab[i,m+1];",
            "    for(j=m;j>k;j--){c=c-X[j,1]*Ab[i,j];}",
            "    X[k,1]=c/Ab[i,k]; k--; if(k==0){break;}",
            "  }",
            "  return(X);",
            "}",
            "int started=timer; matrix sol=boundedSolve(MM,bb);",
            '"SOLVETIME",timer-started;',
            "poly certificate=0;",
            f"for(jj=1;jj<={product_count};jj++){{certificate=certificate+sol[jj,1]*PP[jj];}}",
            '"CERTIFICATE",certificate;',
            "vector vv=["
            + ",".join(f"sol[{j},1]" for j in range(1, product_count + 1))
            + "];",
            "vector ww=cleardenom(vv);",
            "poly scalar=0;",
            f"for(jj=1;jj<={product_count};jj++){{scalar=scalar+ww[jj]*PP[jj];}}",
            "number scalar_number=leadcoef(scalar);",
            "number scalar_numerator=numerator(scalar_number);",
            '"NUM_BEGIN";',
            "scalar_numerator;",
            '"NUM_END";',
            "exit;",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_singular_polynomial(raw: str) -> sp.Poly:
    match = re.search(r"NUM_BEGIN\s*(.*?)\s*NUM_END", raw, flags=re.DOTALL)
    if not match:
        raise RuntimeError(f"Singular did not return a numerator:\n{raw[-4000:]}")
    expression = "".join(match.group(1).split())
    expression = re.sub(r"a(\d+)", r"a**\1", expression)
    expression = re.sub(r"(?<=\d)a", "*a", expression)
    a = sp.Symbol("a")
    return sp.Poly(sp.sympify(expression, locals={"a": a}), a, modulus=PRIME)


@dataclass
class ChartResult:
    chart: int
    numerator: sp.Poly
    transcript: str


def run_chart(chart: int, timeout: int, edge_products: tuple[str, ...]) -> ChartResult:
    process = subprocess.run(
        ["Singular", "-q"],
        input=singular_program(chart, edge_products),
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    transcript = process.stdout + process.stderr
    if process.returncode != 0 or "CERTIFICATE 1" not in transcript:
        raise RuntimeError(f"chart {chart} failed:\n{transcript[-6000:]}")
    return ChartResult(chart, parse_singular_polynomial(transcript), transcript)


def structural_multiplicity(poly: sp.Poly, root: int) -> int:
    a = poly.gens[0]
    divisor = sp.Poly(a - root, a, modulus=PRIME)
    multiplicity = 0
    while poly.rem(divisor).is_zero:
        poly = poly.exquo(divisor)
        multiplicity += 1
    return multiplicity


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--charts", type=int, default=4, choices=range(1, 5))
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--edges",
        choices=("one", "odd-cycle"),
        default="one",
        help="use F01 only, or five edges of a connected graph with a triangle",
    )
    args = parser.parse_args()

    edge_products = ("f01",) if args.edges == "one" else ("f01", "f02", "f12", "f03", "f04")

    results: list[ChartResult] = []
    for chart in CHARTS[: args.charts]:
        result = run_chart(chart, args.timeout, edge_products)
        results.append(result)
        timing = re.search(r"SOLVETIME\s+(\d+)", result.transcript)
        print(
            f"chart seed {chart}: degree {result.numerator.degree()}, "
            f"Singular timer {timing.group(1) if timing else '?'}"
        )

    gcd = results[0].numerator
    for result in results[1:]:
        gcd = sp.gcd(gcd, result.numerator)
    gcd = gcd.monic()
    print(f"gcd degree: {gcd.degree()}")
    multiplicities = {root: structural_multiplicity(gcd, root) for root in (2, 3, 4, 30)}
    print("structural multiplicities:", multiplicities)
    residual = gcd
    a = gcd.gens[0]
    for root, multiplicity in multiplicities.items():
        residual = residual.exquo(sp.Poly((a - root) ** multiplicity, a, modulus=PRIME))
    print(f"degree after stripping the four visible structural roots: {residual.degree()}")
    print("EXPLORATORY ONLY: this one-parameter calculation is not a uniform closure")


if __name__ == "__main__":
    main()
