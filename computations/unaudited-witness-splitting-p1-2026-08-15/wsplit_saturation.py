#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1: the dichotomy criterion, decided with Singular.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

Criterion (see wsplit_dichotomy.py for the statement and its proof):

    a clean-cap witness exists at (p,q)
      <=>  g = s*kappa_0*kappa_1*kappa_2  is NOT in sqrt(I),  I = (E_w : w)
      <=>  J = I : g^infty  is proper AND dim J >= 1
           (J proper but dim J = 0 would mean V(J) = {0}: the saturation is
           supported at the irrelevant point, so no projective witness).

Both tests are done in characteristic zero by Singular (same tool and same
sat()/std() idiom as the committed computations/cap_selection_*.sing).
Every reported witness is re-verified independently in exact rational
arithmetic by the square-zero evaluator of wsplit_core.

Run: python3 wsplit_saturation.py [--pairs p,q ...]
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import wsplit_core as core
import wsplit_sources as sources
from wsplit_core import CUBIC_MONOMIALS, NCAP, dense_rows, error_matrix, require
from wsplit_dichotomy import linear_forms, split_pattern
from wsplit_structural import independent_rows

VARS = [f"K{k // 3}{k % 3}" for k in range(NCAP)]


def poly_terms(row) -> list:
    """Integer-cleared terms of a row of C, as Singular monomial strings."""
    terms = []
    denom = 1
    for value in row:
        if isinstance(value, Fraction):
            denom = denom * value.denominator // _gcd(denom, value.denominator)
    for index, value in enumerate(row):
        if not value:
            continue
        coef = int(value * denom)
        mono = "*".join(VARS[k] for k in CUBIC_MONOMIALS[index])
        terms.append(f"{'+' if coef > 0 else '-'}{abs(coef)}*{mono}")
    return terms or ["0"]


def poly_statements(name: str, row, chunk: int = 12) -> str:
    """Emit ``poly name = ...;`` in short lines (Singular has a line limit)."""
    terms = poly_terms(row)
    head = "".join(terms[:chunk]).lstrip("+")
    lines = [f"poly {name} = {head};"]
    for start in range(chunk, len(terms), chunk):
        lines.append(f"{name} = {name} {''.join(terms[start:start + chunk])};")
    return "\n".join(lines)


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def linear_string(form) -> str:
    terms = []
    denom = 1
    for value in form:
        if isinstance(value, Fraction):
            denom = denom * value.denominator // _gcd(denom, value.denominator)
    for k in range(NCAP):
        value = form[k]
        if not value:
            continue
        coef = int(value * denom)
        terms.append(f"{'+' if coef > 0 else '-'}{abs(coef)}*{VARS[k]}")
    return "".join(terms).lstrip("+") if terms else "0"


SINGULAR_TEMPLATE = """
LIB "elim.lib";
option(redSB);
ring r = 0, ({vars}), dp;
{gens}
ideal I = {gennames};
poly h = ({s})*({k0})*({k1})*({k2});
ideal J = sat(I, ideal(h))[1];
ideal Jstd = std(J);
int isunit = (reduce(1, Jstd) == 0);
int dsat = dim(Jstd);
ideal Istd = std(I);
int dide = dim(Istd);
"SAT_UNIT:", isunit;
"SAT_DIM:", dsat;
"IDEAL_DIM:", dide;
exit;
"""


def run_singular(script: str, timeout: int = 600) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script)
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
        return proc.stdout + proc.stderr
    finally:
        Path(path).unlink(missing_ok=True)


def decide(source, label: str = "", timeout: int = 600) -> dict:
    matrix = error_matrix(source)
    rows = [r for r in dense_rows(matrix) if any(r)]
    forms = linear_forms(source)
    record = {"label": label,
              "s_identically_zero": all(v == 0 for v in forms["s"])}
    if not rows:
        record.update({"case": "(c) E == 0 identically",
                       "witness_exists": not record["s_identically_zero"],
                       "generators": 0})
        return record
    chosen, rank = independent_rows(rows)
    record["rank_C"] = rank
    record["generators"] = len(chosen)
    if rank == 1:
        record["patterns"] = [
            p["pattern"] for p in split_pattern(
                {CUBIC_MONOMIALS[c]: v for c, v in enumerate(chosen[0]) if v},
                forms)]
    if record["s_identically_zero"]:
        record.update({"case": "dead edge (s == 0): g == 0, no witness",
                       "witness_exists": False})
        return record
    script = SINGULAR_TEMPLATE.format(
        vars=",".join(VARS),
        gens="\n".join(poly_statements(f"g{n}", row)
                       for n, row in enumerate(chosen)),
        gennames=",".join(f"g{n}" for n in range(len(chosen))),
        s=linear_string(forms["s"]),
        k0=linear_string(forms["kappa_0"]),
        k1=linear_string(forms["kappa_1"]),
        k2=linear_string(forms["kappa_2"]),
    )
    try:
        out = run_singular(script, timeout=timeout)
    except subprocess.TimeoutExpired:
        record.update({"case": "singular timeout", "witness_exists": None})
        return record
    values = {}
    for line in out.splitlines():
        for key in ("SAT_UNIT", "SAT_DIM", "IDEAL_DIM"):
            if line.startswith(key + ":"):
                values[key] = int(line.split(":", 1)[1].strip())
    if "SAT_UNIT" not in values:
        record.update({"case": "singular failed", "raw": out[:400],
                       "witness_exists": None})
        return record
    unit = bool(values["SAT_UNIT"])
    dim_sat = values["SAT_DIM"]
    record.update({
        "saturation_is_unit": unit,
        "saturation_krull_dim": dim_sat,
        "ideal_krull_dim": values["IDEAL_DIM"],
        "witness_exists": (not unit) and dim_sat >= 1,
    })
    record["case"] = ("(a) active clean cap exists"
                      if record["witness_exists"] else
                      "(b) no active clean cap: g in sqrt(I)")
    return record


def main() -> int:
    physical = sources.load_stage_a()
    records = []
    for p, q in combinations(range(8), 2):
        src = sources.rechart(physical, p, q)
        rec = decide(src, label=f"STAGE_A pair ({p},{q})")
        rec["pair"] = [p, q]
        records.append(rec)
        print(f"  ({p},{q}) rank={rec.get('rank_C', 0):2d} "
              f"s==0:{str(rec['s_identically_zero']):5s} "
              f"satUnit={rec.get('saturation_is_unit')} "
              f"dimSat={rec.get('saturation_krull_dim')} "
              f"witness={rec['witness_exists']}  {rec['case']}")
    live = [r for r in records if not r["s_identically_zero"]]
    wins = [r for r in live if r["witness_exists"]]
    print(f"STAGE_A: {len(live)}/28 live pairs, witness at {len(wins)}")

    # controls: the demo families of wsplit_dichotomy must be reproduced
    controls = []
    for c1, c2 in ((0, 0), (0, 1)):
        rec = decide(sources.two_star(c1, c2), label=f"two_star({c1},{c2})")
        controls.append(rec)
        print(f"  control two_star({c1},{c2}): witness={rec['witness_exists']}"
              f" patterns={rec.get('patterns')}")
    require(controls[0]["witness_exists"] is False, controls[0])
    require(controls[1]["witness_exists"] is True, controls[1])
    rec = decide(sources.single_star(), label="single_star (E == 0)")
    controls.append(rec)
    require(rec["witness_exists"] is True, rec)
    print(f"  control single_star: witness={rec['witness_exists']} "
          f"({rec['case']})")

    with open("saturation_verdicts.json", "w") as handle:
        json.dump({"stage_a": records, "controls": controls}, handle,
                  indent=1, sort_keys=True, default=str)
    print("wrote saturation_verdicts.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
