#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1: extract and independently verify clean-cap witnesses.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a (dependencies unchanged
at a9dbf954, see REPORT.md)

wsplit_saturation.py decides (a) vs (b) with a Groebner saturation.  A
verdict of (a) deserves a CERTIFICATE, not a verdict: this module produces
an explicit exact rational cap K and checks, with the independent
square-zero evaluator of wsplit_core (which never sees the cubic
coefficient matrix), that

        E_{p,q}(K) = 0  as a tensor      and     s k_0 k_1 k_2 (K) != 0.

Method (exact, no Groebner): restrict the ideal to a random rational line
K(t) = K0 + t K1.  Every generator becomes a univariate cubic in t; the GCD
of those univariate polynomials is the restriction of the common part of
the ideal.  Rational roots of the GCD are exact points of V(I); each is
then screened for activity and verified.

Run: python3 wsplit_witness_extraction.py
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations

import wsplit_core as core
import wsplit_sources as sources
from wsplit_core import CUBIC_MONOMIALS, NCAP, dense_rows, error_matrix, require
from wsplit_dichotomy import linear_forms, verify_witness
from wsplit_structural import independent_rows


def restrict_to_line(cubic_row, k0, k1) -> list:
    """Coefficients [t^0, t^1, t^2, t^3] of the row along K0 + t K1."""
    out = [Fraction(0)] * 4
    for index, coef in enumerate(cubic_row):
        if not coef:
            continue
        mono = CUBIC_MONOMIALS[index]
        # product over the three factors of (k0[k] + t k1[k])
        poly = [Fraction(1)]
        for k in mono:
            new = [Fraction(0)] * (len(poly) + 1)
            for degree, value in enumerate(poly):
                new[degree] += value * k0[k]
                new[degree + 1] += value * k1[k]
            poly = new
        for degree, value in enumerate(poly):
            out[degree] += coef * value
    return out


def poly_gcd(a: list, b: list) -> list:
    """Monic GCD of univariate rational polynomials given low-to-high."""
    def trim(p):
        while p and p[-1] == 0:
            p = p[:-1]
        return p

    a, b = trim(list(a)), trim(list(b))
    while b:
        # a mod b
        a = list(a)
        while len(a) >= len(b) and a:
            factor = a[-1] / b[-1]
            shift = len(a) - len(b)
            for i, value in enumerate(b):
                a[shift + i] -= factor * value
            a = trim(a)
        a, b = b, a
    if a:
        lead = a[-1]
        a = [value / lead for value in a]
    return a


def rational_roots(poly: list) -> list:
    """All rational roots of a univariate rational polynomial."""
    poly = list(poly)
    while poly and poly[-1] == 0:
        poly.pop()
    if len(poly) < 2:
        return []
    denominator = 1
    for value in poly:
        denominator = denominator * value.denominator // _gcd(
            denominator, value.denominator)
    ints = [int(value * denominator) for value in poly]
    common = 0
    for value in ints:
        common = _gcd(common, abs(value))
    if common:
        ints = [value // common for value in ints]
    constant = ints[0]
    lead = ints[-1]
    roots = []
    if constant == 0:
        roots.append(Fraction(0))
        ints = ints[1:]
        if len(ints) < 2:
            return roots
        constant, lead = ints[0], ints[-1]
    for p in divisors(abs(constant)):
        for q in divisors(abs(lead)):
            for sign in (1, -1):
                candidate = Fraction(sign * p, q)
                value = sum(c * candidate ** n for n, c in enumerate(ints))
                if value == 0 and candidate not in roots:
                    roots.append(candidate)
    return roots


def divisors(n: int) -> list:
    if n == 0:
        return [1]
    out = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            if d != n // d:
                out.append(n // d)
        d += 1
    return sorted(out)


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def find_witness(source, tries: int = 400, seed: int = 20260815) -> dict:
    rng = random.Random(seed)
    matrix = error_matrix(source)
    rows = [r for r in dense_rows(matrix) if any(r)]
    if not rows:
        cap = tuple(1 if k in (0, 4, 8) else 0 for k in range(NCAP))
        return {"method": "E == 0 identically", **verify_witness(source, cap)}
    chosen, _rank = independent_rows(rows)
    for attempt in range(tries):
        k0 = [rng.randint(-6, 6) for _ in range(NCAP)]
        k1 = [rng.randint(-6, 6) for _ in range(NCAP)]
        restricted = [restrict_to_line(row, k0, k1) for row in chosen]
        gcd = restricted[0]
        for other in restricted[1:]:
            gcd = poly_gcd(gcd, other)
            if len(gcd) <= 1:
                break
        if len(gcd) <= 1:
            continue
        for root in rational_roots(gcd):
            cap = tuple(Fraction(a) + root * b for a, b in zip(k0, k1))
            checked = verify_witness(source, cap)
            if checked["is_witness"]:
                checked["method"] = (f"random line attempt {attempt}, "
                                     f"gcd degree {len(gcd) - 1}, t = {root}")
                checked["line"] = {"K0": k0, "K1": k1}
                return checked
    return {"is_witness": False,
            "method": f"no rational witness on {tries} random lines"}


def main() -> int:
    physical = sources.load_stage_a()
    out = {}
    for p, q in ((0, 2), (1, 3)):
        src = sources.rechart(physical, p, q)
        forms = linear_forms(src)
        record = find_witness(src)
        record["pair"] = [p, q]
        if record.get("is_witness"):
            cap = record["cap"]
            # belt and braces: recompute the four activity scalars and the
            # full 729-component error from scratch
            err = core.direct_error_tensor(src, cap)
            require(all(value == 0 for value in err.values()),
                    "witness failed the independent error recomputation")
            for name, form in forms.items():
                require(core.eval_form(form, cap) != 0,
                        f"witness failed activity at {name}")
        print(f"  STAGE_A pair ({p},{q}): witness = {record.get('is_witness')} "
              f"[{record.get('method')}]")
        if record.get("is_witness"):
            print(f"      K = {[str(v) for v in record['cap']]}")
            print(f"      s,k0,k1,k2 = {record['values']}")
        out[f"{p},{q}"] = record

    # control: a pair the saturation declares witness-free must yield nothing
    control = find_witness(sources.rechart(physical, 0, 4), tries=120)
    print(f"  control STAGE_A pair (0,4) [saturation says no witness]: "
          f"{control.get('is_witness')}")
    require(control.get("is_witness") is False, control)
    out["control_0,4"] = control

    with open("witness_certificates.json", "w") as handle:
        json.dump(out, handle, indent=1, sort_keys=True, default=str)
    print("wrote witness_certificates.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
