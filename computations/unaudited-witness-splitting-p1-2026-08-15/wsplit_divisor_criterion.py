#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1: the single-hyperplane criterion (test T2).

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

CORRECTION NOTE.  An earlier draft of this module used "l divides every
component E_w" as a sufficient condition for case (b).  That is FALSE and
points the wrong way: l | E gives V(l) contained in V(I), not V(I)
contained in V(l).  (Counterexample produced by this probe: the two-star
source with colours (0,1) has E = s*(k_0 k_1 + K_01 K_10), so s divides E,
yet an active clean cap exists -- verified in wsplit_dichotomy.py.)  The
correct cheap test is radical membership of a single linear form:

  LEMMA (T2).  If l^N lies in I = (E_w : w) for some N >= 1 and some
  l in {s, kappa_0, kappa_1, kappa_2}, then V(I) is contained in V(l),
  hence in V(g) = V(s k_0 k_1 k_2), so NO active clean cap exists at (p,q).

  Proof: l^N in I gives V(I) contained in V(l^N) = V(l); V(l) is one of the
  four components of V(g).  (Nullstellensatz is not even needed for this
  direction.)

T2 is checkable by exact linear algebra: I is generated in K-degree 3, so
l^N in I is a rational linear-solvability question inside the degree-N
piece Sym^N (dimensions 165, 495, 1287 for N = 3,4,5).

Hierarchy of criteria for case (b) at a pair:
  T1  rank C = 1 and the single generator splits into three of the four
      forms  -- the plan's 20 patterns; complete on the rank-1 stratum;
  T2  this module -- covers ideals whose zero set sits in ONE of the four
      hyperplanes; disjoint from T1 in general;
  T3  g in sqrt(I) -- complete, decided by saturation (wsplit_saturation.py).

Run: python3 wsplit_divisor_criterion.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from itertools import combinations, combinations_with_replacement

import wsplit_core as core
import wsplit_sources as sources
from wsplit_core import (CUBIC_MONOMIALS, NCAP, dense_rows, error_matrix,
                         require)
from wsplit_dichotomy import linear_forms

MAX_POWER = 5


def monomials(degree: int) -> tuple:
    return tuple(combinations_with_replacement(range(NCAP), degree))


MONOMIALS = {d: monomials(d) for d in range(1, MAX_POWER + 1)}
INDEX = {d: {m: n for n, m in enumerate(MONOMIALS[d])}
         for d in MONOMIALS}


def power_of_linear(form, power: int) -> dict:
    """l^power as {monomial -> coefficient}."""
    result = {(): Fraction(1)}
    for _ in range(power):
        nxt: dict = {}
        for mono, coef in result.items():
            for k in range(NCAP):
                if not form[k]:
                    continue
                key = tuple(sorted(mono + (k,)))
                nxt[key] = nxt.get(key, 0) + coef * form[k]
        result = {m: c for m, c in nxt.items() if c}
    return result


def degree_piece(rows, degree: int) -> list:
    """A spanning set of I_degree as dense vectors (degree >= 3)."""
    require(degree >= 3, degree)
    multipliers = monomials(degree - 3) if degree > 3 else ((),)
    basis = MONOMIALS[degree]
    index = INDEX[degree]
    out = []
    for row in rows:
        for mult in multipliers:
            vec = [Fraction(0)] * len(basis)
            for cidx, coef in enumerate(row):
                if coef:
                    key = tuple(sorted(CUBIC_MONOMIALS[cidx] + mult))
                    vec[index[key]] += coef
            out.append(vec)
    return out


def in_span(vectors, target) -> bool:
    """Exact test: is ``target`` in the Q-span of ``vectors``?"""
    basis = []
    pivots = []
    for vec in vectors:
        cur = list(vec)
        for pcol, brow in zip(pivots, basis):
            if cur[pcol]:
                factor = cur[pcol] / brow[pcol]
                cur = [a - factor * b for a, b in zip(cur, brow)]
        pcol = next((c for c in range(len(cur)) if cur[c]), None)
        if pcol is None:
            continue
        basis.append(cur)
        pivots.append(pcol)
    cur = list(target)
    for pcol, brow in zip(pivots, basis):
        if cur[pcol]:
            factor = cur[pcol] / brow[pcol]
            cur = [a - factor * b for a, b in zip(cur, brow)]
    return not any(cur)


def linear_radical_members(source, max_power: int = MAX_POWER) -> dict:
    """For each of the four forms, the least N with l^N in I (or None)."""
    matrix = error_matrix(source)
    rows = [r for r in dense_rows(matrix) if any(r)]
    if rows:
        # a Q-basis of I_3 generates I; using it keeps the graded pieces small
        from wsplit_structural import independent_rows
        rows, _rank = independent_rows(rows)
    forms = linear_forms(source)
    out = {}
    if not rows:
        return {name: (0 if all(v == 0 for v in form) else None)
                for name, form in forms.items()}
    pieces = {}
    for name, form in forms.items():
        if all(v == 0 for v in form):
            out[name] = 0            # the zero form is trivially in I
            continue
        found = None
        for power in range(3, max_power + 1):
            if power not in pieces:
                pieces[power] = degree_piece(rows, power)
            target_poly = power_of_linear(form, power)
            index = INDEX[power]
            target = [Fraction(0)] * len(MONOMIALS[power])
            for mono, coef in target_poly.items():
                target[index[mono]] = coef
            if in_span(pieces[power], target):
                found = power
                break
        out[name] = found
    return out


def main() -> int:
    physical = sources.load_stage_a()
    verdicts = {}
    try:
        with open("saturation_verdicts.json") as handle:
            for rec in json.load(handle)["stage_a"]:
                verdicts[tuple(rec["pair"])] = rec
    except FileNotFoundError:
        pass

    print("== T2: least N with l^N in I, near-exact eight-site source ==")
    records = []
    for p, q in combinations(range(8), 2):
        src = sources.rechart(physical, p, q)
        powers = linear_radical_members(src)
        witness = verdicts.get((p, q), {}).get("witness_exists")
        hits = {name: n for name, n in powers.items() if n is not None}
        rec = {"pair": [p, q], "least_power": powers,
               "T2_applies": bool(hits), "witness_exists": witness}
        records.append(rec)
        print(f"  ({p},{q}) T2 hits: {hits or '-'}   witness={witness}")
        if hits and witness:
            raise AssertionError(f"T2 contradicts a verified witness at "
                                 f"({p},{q}): {hits}")

    negative = [r for r in records if r["witness_exists"] is False]
    explained = [r for r in negative if r["T2_applies"]]
    print(f"  case (b) pairs explained by T2: {len(explained)}/{len(negative)}")

    # controls
    control = linear_radical_members(sources.two_star(0, 1))
    print(f"  control two_star(0,1) [has a verified witness]: {control}")
    require(all(value is None or name == "s" and value is None
                for name, value in control.items()),
            ("T2 must not fire on a source with a witness", control))
    control00 = linear_radical_members(sources.two_star(0, 0))
    print(f"  control two_star(0,0) [pattern s*k0*k0, no witness]: {control00}")

    with open("linear_radical_criterion.json", "w") as handle:
        json.dump({"stage_a": records,
                   "control_two_star_0_1": control,
                   "control_two_star_0_0": control00},
                  handle, indent=1, sort_keys=True, default=str)
    print("wrote linear_radical_criterion.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
