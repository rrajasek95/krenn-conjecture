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
EXPECTED_DIGEST = "db42c1d31507b7fa217171c81267c1c823643b5f17ec5ea2e6a5a94294601793"


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


def build(full=False, contract_site=5):
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

    visible_dark = tuple(site for site in (x, y, z)
                         if site != contract_site)
    selected_star = []
    for site in range(6):
        if site == contract_site:
            continue
        for colour in range(3):
            if site < contract_site:
                selected_star.append((site, contract_site, colour, 0))
            else:
                selected_star.append((contract_site, site, 0, colour))
    selected = (tuple((u, v, a, b)
                      for u, v in combinations(range(6), 2)
                      for a in range(3) for b in range(3)) if full else
                tuple(selected_star) + tuple(
                    (visible_dark[0], visible_dark[1], first, second)
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
    output_sites = tuple(site for site in range(6)
                         if site != contract_site)
    for i in range(3):
        for j in range(3):
            for output in product(range(3), repeat=5):
                word_list = [0] * 6
                for site, colour in zip(output_sites, output):
                    word_list[site] = colour
                word = tuple(word_list)
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
    label_00 = (0, 0, (0, 0, 0, 0, 0))
    configurations = {
        3: {
            "counts": (24, 370, 547),
            "labels": (label_00,
                       (2, 1, (0, 0, 0, 0, 2)),
                       (2, 2, (0, 0, 0, 1, 2))),
            "coefficients": (-2, -2),
            "multiplier": "x4500",
            "constant": 2,
            "rows": ("-1+x2300*x4500+x3400", "-x3400", "2*x2300"),
            "full_counts": (135, 1239, 15958),
            "carrier_split": (12, 0, 6),
        },
        4: {
            "counts": (24, 410, 619),
            "labels": (label_00,
                       (2, 1, (0, 0, 0, 0, 2)),
                       (2, 2, (0, 0, 0, 2, 2))),
            "coefficients": (-1, -1),
            "multiplier": "x3500",
            "constant": 1,
            "rows": ("-1+x2400*x3500+x3400", "-x3400", "x2400"),
            "full_counts": (135, 1359, 17173),
            "carrier_split": (12, 0, 3),
        },
        5: {
            "counts": (24, 360, 508),
            "labels": (label_00, None,
                       (2, 2, (0, 0, 0, 2, 1))),
            "coefficients": (-1, 0),
            "multiplier": "x3400",
            "constant": 1,
            "rows": ("-1+x2500*x3400", None, "x2500"),
            "full_counts": (135, 1359, 17173),
            "carrier_split": (12, 0, 3),
        },
    }

    records = []
    for contract_site, config in configurations.items():
        names, labels, rows = build(contract_site=contract_site)
        require((len(names), len(rows), sum(map(len, rows))) ==
                config["counts"],
                ("a natural joint fibre changed", contract_site))
        chosen = []
        for label in config["labels"]:
            chosen.append(None if label is None else rows[labels.index(label)])
        chosen_text = tuple(None if row is None else expression(row, names)
                            for row in chosen)
        require(chosen_text == config["rows"],
                ("a natural labelled row changed", contract_site, chosen_text))
        unit = scale(config["coefficients"][0], chosen[0])
        if chosen[1] is not None:
            unit = add(unit, scale(config["coefficients"][1], chosen[1]))
        multiplier = names.index(config["multiplier"])
        unit = add(unit, multiply({(multiplier,): 1}, chosen[2]))
        require(unit == {(): config["constant"]},
                ("a natural ordinary unit failed", contract_site, unit))

        full_names, full_labels, full_rows = build(
            full=True, contract_site=contract_site
        )
        require((len(full_names), len(full_rows), sum(map(len, full_rows))) ==
                config["full_counts"],
                ("an unrestricted joint source changed", contract_site))
        full_chosen = [None if label is None else
                       full_rows[full_labels.index(label)]
                       for label in config["labels"]]
        # The middle row is used to obtain the natural-fibre unit, but is
        # itself zero in a full source.  Add it back before recording the
        # unrestricted escape, leaving the reduced two-row carrier.
        carrier = scale(config["coefficients"][0], full_chosen[0])
        full_multiplier = full_names.index(config["multiplier"])
        carrier = add(
            carrier,
            multiply({(full_multiplier,): 1}, full_chosen[2]),
        )
        require(carrier.get(()) == config["constant"],
                ("the unrestricted constant changed", contract_site))

        pure_cubic = []
        pure_quadratic = []
        mixed_cubic = []
        for monomial, coefficient in carrier.items():
            if not monomial:
                continue
            decorated = tuple(full_names[index] for index in monomial)
            if all(name.endswith("00") for name in decorated):
                target = pure_cubic if len(monomial) == 3 else pure_quadratic
            else:
                target = mixed_cubic
            target.append((decorated, coefficient))
        split = (len(pure_cubic), len(pure_quadratic), len(mixed_cubic))
        require(split == config["carrier_split"],
                ("an unrestricted carrier split changed", contract_site, split))
        selected_edge = config["multiplier"]
        require(all(selected_edge not in monomial
                    for monomial, _ in pure_cubic),
                ("a pure cubic retained the selected edge", contract_site))
        records.append((contract_site, chosen_text,
                        expression(carrier, full_names),
                        tuple(sorted(pure_cubic)),
                        tuple(sorted(pure_quadratic)),
                        tuple(sorted(mixed_cubic))))

    ledger = tuple(records)
    digest = sha256(repr(ledger).encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                ("the joint carrier ledger changed", digest))
    print("N=8 scalar fixed-dark-plane joint labelled carrier: passed")
    print("  natural fibres                     : 3 / 3 ordinary units")
    print("  natural constants                  : 2 / 1 / 1")
    print("  unrestricted pure cubics           : 12 / 12 / 12")
    print("  unrestricted pure quadratics       : 0 / 0 / 0")
    print("  unrestricted mixed cubics          : 6 / 3 / 3")
    print(f"  ledger sha256                      : {digest}")


if __name__ == "__main__":
    main()
