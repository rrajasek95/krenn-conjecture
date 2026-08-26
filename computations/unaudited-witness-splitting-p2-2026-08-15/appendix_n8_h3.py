#!/usr/bin/env python3
"""UNAUDITED PROBE (P2 appendix) -- does the h=2 structure survive to h=3?

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

At six sites (h=2) every component of the cap error E_pq is a quadratic form
in the cap K lying in W_2 = Sym^2(V_p^*) (x) Sym^2(V_q^*) (the annihilator of
the nine 2x2 minors of K), and kappa_c^2 lies in W_2, so a generic source is
split-blocked at every pair.  This script tests the same two statements at the
first inductive boundary N=8, h=3, where (descent note, eq. 17)

    6 E_pq(K) = 3 s r^2 x + r^3
              = 6 * sum_{M in PM(U)} [ R_e1 R_e2 R_e3
                        + s (R_e1 R_e2 A_e3 + R_e1 R_e3 A_e2
                             + R_e2 R_e3 A_e1) ] / 6

componentwise on the 3^6 = 729 boundary words of U, |U| = 6.

Tested:
 (i)  is every component in W_3 = Sym^3(V_p^*) (x) Sym^3(V_q^*) (dim 100 of
      the 165 cubics)?
 (ii) which of the 20 degree-3 L-monomials lie in the ideal?
 (iii) does a witness exist (Rabinowitsch, Singular)?

Usage: python3 appendix_n8_h3.py [--sources 3]
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
import json
import random
import time

from wsplit_core import (KAPPA_VARS, NVAR, VARS, lin_is_zero, lin_zero,
                         parse_singular, perfect_matchings, poly_string_lin,
                         run_singular)

SITES8 = tuple(range(8))
PAIRS8 = tuple(combinations(SITES8, 2))


def random_blocks(rng, lo=-3, hi=3):
    return {pair: [[Fraction(rng.randint(lo, hi)) for _ in range(3)]
                   for _ in range(3)] for pair in PAIRS8}


def oriented(blocks, u, v):
    if u < v:
        return blocks[(u, v)]
    matrix = blocks[(v, u)]
    return [[matrix[j][i] for j in range(3)] for i in range(3)]


def cubic_mul(quad, form):
    """(dict on sorted pairs) * (linear form) -> dict on sorted triples."""
    out = {}
    for key, value in quad.items():
        for index in range(NVAR):
            if form[index] == 0:
                continue
            triple = tuple(sorted(key + (index,)))
            out[triple] = out.get(triple, Fraction(0)) + value * form[index]
    return {key: value for key, value in out.items() if value != 0}


def lin_mul_pair(a, b):
    out = {}
    for i in range(NVAR):
        if a[i] == 0:
            continue
        for j in range(NVAR):
            if b[j] == 0:
                continue
            key = (i, j) if i <= j else (j, i)
            out[key] = out.get(key, Fraction(0)) + a[i] * b[j]
    return {key: value for key, value in out.items() if value != 0}


def multinomial(triple):
    counts = Counter(triple)
    factor = 1
    remaining = 3
    for value in counts.values():
        from math import comb
        factor *= comb(remaining, value)
        remaining -= value
    return factor


def in_sym_cube(cubic):
    """Is the cubic in Sym^3(row) (x) Sym^3(col)?

    Equivalent to invariance of the symmetric coefficient array under
    permuting the three column (q-slot) indices among the three factors.
    """
    array = {key: Fraction(value, multinomial(key))
             for key, value in cubic.items()}

    def value(triple):
        key = tuple(sorted(triple))
        return array.get(key, Fraction(0))

    for key in list(array):
        rows = [divmod(index, 3)[0] for index in key]
        cols = [divmod(index, 3)[1] for index in key]
        base = value(key)
        for permuted in ((0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
            other = tuple(3 * rows[n] + cols[permuted[n]] for n in range(3))
            if value(other) != base:
                return False
    return True


def error_cubics(blocks, p, q):
    U = tuple(site for site in SITES8 if site not in (p, q))
    block = oriented(blocks, p, q)
    s_form = [block[i][j] for i in range(3) for j in range(3)]
    R = {}
    for a, b in combinations(U, 2):
        Apa, Aqb = oriented(blocks, p, a), oriented(blocks, q, b)
        Apb, Aqa = oriented(blocks, p, b), oriented(blocks, q, a)
        table = []
        for alpha in range(3):
            row = []
            for beta in range(3):
                form = lin_zero()
                for i in range(3):
                    for j in range(3):
                        value = (Apa[i][alpha] * Aqb[j][beta]
                                 + Apb[i][beta] * Aqa[j][alpha])
                        if value:
                            form[3 * i + j] += value
                row.append(form)
            table.append(row)
        R[(a, b)] = table
    position = {site: index for index, site in enumerate(U)}
    matchings = perfect_matchings(U)
    out = []
    for encoded in range(3 ** 6):
        word = []
        value = encoded
        for _ in range(6):
            word.append(value % 3)
            value //= 3
        word = tuple(word)
        cubic = {}
        for matching in matchings:
            edges = [tuple(sorted(edge)) for edge in matching]
            forms = [R[edge][word[position[edge[0]]]][word[position[edge[1]]]]
                     for edge in edges]
            entries = [oriented(blocks, *edge)[word[position[edge[0]]]][
                word[position[edge[1]]]] for edge in edges]
            if not any(lin_is_zero(form) for form in forms):
                term = cubic_mul(lin_mul_pair(forms[0], forms[1]), forms[2])
                for key, value in term.items():
                    cubic[key] = cubic.get(key, Fraction(0)) + value
            for drop in range(3):
                keep = [index for index in range(3) if index != drop]
                if entries[drop] == 0:
                    continue
                if lin_is_zero(forms[keep[0]]) or lin_is_zero(forms[keep[1]]):
                    continue
                quad = lin_mul_pair(forms[keep[0]], forms[keep[1]])
                term = cubic_mul(quad, s_form)
                for key, value in term.items():
                    cubic[key] = cubic.get(key, Fraction(0)) + value * entries[drop]
        cubic = {key: value for key, value in cubic.items() if value != 0}
        if cubic:
            out.append(cubic)
    return s_form, out


def poly_string_cubic(cubic):
    parts = []
    for (i, j, k), value in sorted(cubic.items()):
        parts.append(f"({value.numerator}/{value.denominator})"
                     f"*{VARS[i]}*{VARS[j]}*{VARS[k]}")
    return "+".join(parts) if parts else "0"


def singular_report(s_form, cubics, p=0, q=1, timeout=1800):
    gens = ",".join(poly_string_cubic(cubic) for cubic in cubics)
    forms = [poly_string_lin(s_form)] + [VARS[v] for v in KAPPA_VARS]
    fprod = "*".join(f"({form})" for form in forms)
    V = ",".join(VARS)
    lines = [f"ring R=0,({V}),dp;", f"ideal I={gens};", "ideal G=std(I);",
             f'"DIM {p} {q} "+string(dim(G));']
    for degree in (3, 4):
        for combo in combinations_with_replacement(range(4), degree):
            mono = "*".join(f"({forms[index]})" for index in combo)
            name = "".join("s" if c == 0 else str(c - 1) for c in combo)
            lines.append(f'"MEM {p} {q} {degree} {name} "'
                         f"+string(reduce({mono},G)==0);")
    lines += [f"ring RT=0,({V},t),dp;", "ideal I=imap(R,I);",
              f"ideal J=I,t*{fprod}-1;",
              f'"WIT {p} {q} "+string(dim(std(J)));']
    return parse_singular(run_singular("\n".join(lines), timeout=timeout))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=int, default=2)
    parser.add_argument("--out", default="results_n8.json")
    args = parser.parse_args()
    results = []
    for index in range(args.sources):
        rng = random.Random(90000 + index)
        blocks = random_blocks(rng)
        start = time.time()
        s_form, cubics = error_cubics(blocks, 0, 1)
        build = time.time() - start
        outside = sum(1 for cubic in cubics if not in_sym_cube(cubic))
        start = time.time()
        try:
            table = singular_report(s_form, cubics)
            entry = table[(0, 1)]
            decided = True
        except Exception as error:  # timeout or Singular failure
            entry = {"dim": None, "witness": None, "mem": {}}
            decided = False
            print("singular failed:", type(error).__name__)
        record = {
            "seed": 90000 + index,
            "components": len(cubics),
            "components_outside_Sym3": outside,
            "cone_dim": entry["dim"],
            "witness": entry["witness"],
            "decided": decided,
            "blocking_monomials": sorted(f"{degree}:{name}" for
                                         (degree, name), value
                                         in entry["mem"].items() if value),
            "build_seconds": round(build, 1),
            "singular_seconds": round(time.time() - start, 1),
        }
        results.append(record)
        print(json.dumps(record), flush=True)
    with open(args.out, "w") as handle:
        json.dump(results, handle, indent=1)


if __name__ == "__main__":
    main()
