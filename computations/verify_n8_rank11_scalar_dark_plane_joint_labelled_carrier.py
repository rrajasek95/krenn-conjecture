#!/usr/bin/env python3
"""Exact labelled carrier for the fixed-dark-plane joint-site guard.

The natural 24-coordinate completion fibre is killed by two literal joint
rows.  With all 135 q-cells restored, the same combination leaves exactly
twelve pure-zero matching carriers and three mixed carriers.  This is the
smallest source-labelled escape ledger beyond the cap-plane quotient.
"""

from __future__ import annotations

import importlib.util
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "computations/verify_n8_rank11_scalar_dark_plane_one_site_guard.py"
EXPECTED_DIGEST = "11731e55eac7c0d1b2431e3d9bc5e0d0681b1be0740099cf975bf96a10b07ff7"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_guard():
    spec = importlib.util.spec_from_file_location("dark_guard", GUARD)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def add(*polynomials):
    out = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] = out.get(monomial, 0) + coefficient
            if not out[monomial]:
                del out[monomial]
    return out


def scale(coefficient, polynomial):
    return {monomial: coefficient * value
            for monomial, value in polynomial.items() if coefficient * value}


def multiply(left, right):
    out = {}
    for first, a in left.items():
        for second, b in right.items():
            monomial = tuple(sorted(first + second))
            out[monomial] = out.get(monomial, 0) + a * b
    return {monomial: coefficient for monomial, coefficient in out.items()
            if coefficient}


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        out.extend(((first, second),) + matching
                   for matching in matchings(rest))
    return out


def build(full=False):
    guard = load_guard()
    x, y, z = 3, 4, 5
    l0 = guard.linear(((0, 0, 1), (1, 2, 1), (2, 1, 1)))
    l1 = guard.linear(((1, 2, 1), (2, 0, 1)))
    m0 = guard.linear(((1, 1, 1), (1, 2, 1), (2, 0, 1)))
    m1 = guard.atom(1, 0)
    t = guard.linear(((1, 0, 1), (1, 1, -1),
                      (1, 2, -1), (2, 0, 1)))
    base_q = guard.add(guard.multiply(l0, m1),
                       guard.multiply(guard.atom(y, 0), guard.atom(x, 0)),
                       guard.multiply(guard.atom(z, 0), t))

    selected = (tuple((u, v, a, b)
                      for u, v in combinations(range(6), 2)
                      for a in range(3) for b in range(3)) if full else
                tuple((site, z, colour, 0)
                      for site in range(5) for colour in range(3)) + tuple(
                    (x, y, first, second)
                    for first in range(3) for second in range(3)
                ))
    variable_index = {cell: index for index, cell in enumerate(selected)}
    names = tuple(f"x{u}{v}{a}{b}" for u, v, a, b in selected)

    def word_cell(u, v, a, b):
        word = [-1] * 6
        word[u], word[v] = a, b
        return tuple(word)

    def q_cell(u, v, a, b):
        if u > v:
            u, v, a, b = v, u, b, a
        cell = (u, v, a, b)
        if cell in variable_index:
            return {(variable_index[cell],): 1}
        coefficient = int(base_q.get(word_cell(u, v, a, b), 0))
        return {(): coefficient} if coefficient else {}

    matching_cache = {
        vertices: matchings(vertices)
        for size in (4, 6) for vertices in combinations(range(6), size)
    }

    def q_power(word, vertices):
        terms = []
        for matching in matching_cache[tuple(vertices)]:
            term = {(): 1}
            for u, v in matching:
                term = multiply(term, q_cell(u, v, word[u], word[v]))
            terms.append(term)
        return add(*terms)

    lam = (1, 1, -1)
    mu = (1, -1, -1)
    dark_u = {(3, 1): 1, (4, 1): 1, (5, 2): 1}
    dark_v = {(3, 2): 1, (4, 1): 1, (5, 2): 1}
    p_base = (
        {(0, 0): 1, (1, 2): 1, (2, 1): 1},
        {(1, 2): 1, (2, 0): 1},
        {},
    )
    s_base = (
        {},
        {(1, 1): 1, (1, 2): 1, (2, 0): 1},
        {(1, 0): 1},
    )
    p, s = [], []
    for index in range(3):
        left = dict(p_base[index])
        for key, coefficient in dark_u.items():
            left[key] = left.get(key, 0) + lam[index] * coefficient
        p.append({key: coefficient for key, coefficient in left.items()
                  if coefficient})
        right = dict(s_base[index])
        for key, coefficient in dark_v.items():
            right[key] = right.get(key, 0) + mu[index] * coefficient
        s.append({key: coefficient for key, coefficient in right.items()
                  if coefficient})

    direct = ((1, -1, -1), (0, 0, 0), (0, 0, 0))
    labels, rows = [], []
    for i in range(3):
        for j in range(3):
            for output in product(range(3), repeat=5):
                word = output + (0,)
                polynomial = (scale(direct[i][j], q_power(word, range(6)))
                              if direct[i][j] else {})
                for (left_site, left_colour), left_value in p[i].items():
                    if word[left_site] != left_colour:
                        continue
                    for (right_site, right_colour), right_value in s[j].items():
                        if (left_site == right_site or
                                word[right_site] != right_colour):
                            continue
                        residual = tuple(site for site in range(6)
                                         if site not in (left_site, right_site))
                        polynomial = add(
                            polynomial,
                            scale(left_value * right_value,
                                  q_power(word, residual)),
                        )
                if i == j == 0 and all(colour == 0 for colour in word):
                    polynomial = add(polynomial, {(): -1})
                if polynomial:
                    labels.append((i, j, output))
                    rows.append(polynomial)
    return names, labels, rows


def expression(polynomial, names):
    terms = []
    for monomial, coefficient in sorted(polynomial.items()):
        value = "*".join(names[index] for index in monomial) or "1"
        if coefficient == 1:
            terms.append(value)
        elif coefficient == -1:
            terms.append("-" + value)
        else:
            terms.append(f"{coefficient}*{value}")
    return "+".join(terms).replace("+-", "-")


def main():
    names, labels, rows = build()
    require((len(names), len(rows), sum(map(len, rows))) == (24, 360, 508),
            "the natural joint fibre changed")
    label_00 = (0, 0, (0, 0, 0, 0, 0))
    label_22 = (2, 2, (0, 0, 0, 2, 1))
    row_00 = rows[labels.index(label_00)]
    row_22 = rows[labels.index(label_22)]
    a = names.index("x2500")
    b = names.index("x3400")
    require(expression(row_00, names) == "-1+x2500*x3400",
            "the diagonal anchor row changed")
    require(expression(row_22, names) == "x2500",
            "the labelled mixed row changed")
    unit = add(multiply({(b,): 1}, row_22), scale(-1, row_00))
    require(unit == {(): 1}, "the two-row ordinary unit failed")

    full_names, full_labels, full_rows = build(full=True)
    require((len(full_names), len(full_rows), sum(map(len, full_rows))) ==
            (135, 1359, 17173), "the unrestricted joint source changed")
    full_00 = full_rows[full_labels.index(label_00)]
    full_22 = full_rows[full_labels.index(label_22)]
    full_b = full_names.index("x3400")
    carrier = add(multiply({(full_b,): 1}, full_22), scale(-1, full_00))
    carrier_text = expression(carrier, full_names)
    require(len(carrier) == 16 and carrier.get(()) == 1,
            "the unrestricted carrier count changed")

    pure_carriers = []
    mixed_carriers = []
    for monomial, coefficient in carrier.items():
        if not monomial:
            continue
        require(coefficient == -1 and len(monomial) == 3,
                "the carrier stopped being a negative cubic")
        decorated = tuple(full_names[index] for index in monomial)
        if all(name.endswith("00") for name in decorated):
            pure_carriers.append(decorated)
        else:
            mixed_carriers.append(decorated)
    require((len(pure_carriers), len(mixed_carriers)) == (12, 3),
            "the pure/mixed carrier split changed")
    require(all("x3400" not in carrier for carrier in pure_carriers),
            "a pure carrier still uses the selected 34 anchor")
    require(all("x3400" in carrier for carrier in mixed_carriers),
            "a mixed carrier lost the selected 34 anchor")

    ledger = (
        expression(row_00, names), expression(row_22, names),
        carrier_text, tuple(sorted(pure_carriers)),
        tuple(sorted(mixed_carriers)),
    )
    digest = sha256(repr(ledger).encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                ("the joint carrier ledger changed", digest))
    print("N=8 scalar fixed-dark-plane joint labelled carrier: passed")
    print(f"  natural fibre variables/rows/terms : {len(names)} / "
          f"{len(rows)} / {sum(map(len, rows))}")
    print("  natural fibre ordinary unit        : x3400*g22-g00 = 1")
    print(f"  unrestricted variables/rows/terms  : {len(full_names)} / "
          f"{len(full_rows)} / {sum(map(len, full_rows))}")
    print(f"  unrestricted carrier split         : "
          f"{len(pure_carriers)} pure + {len(mixed_carriers)} mixed")
    print(f"  ledger sha256                      : {digest}")


if __name__ == "__main__":
    main()
