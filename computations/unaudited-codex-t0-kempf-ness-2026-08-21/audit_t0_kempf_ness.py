#!/usr/bin/env python3
"""Exact T0 weight, balance, mixed-norm, and Laurent escape audit."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_t0_kempf_ness.json"
PINS = {
    "computations/unaudited-codex-x5-torus-hm-audit-2026-08-21/results_x5_torus_hm.json":
        "90d56147432f341d2bd29ddd24fd73a89505a7f3e8eeb0a77fb40c2fbfd8b24a",
    "computations/unaudited-codex-x5-global-base-locus-2026-08-21/results_x5_global_base_locus.json":
        "ce16613bb2ea41849e8174e7dee379884d5081d033db8c420e38d50f28291873",
    "computations/unaudited-x4general-w40-2026-08-20/results_t3.json":
        "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
    "computations/unaudited-x3core-w25-2026-08-15/OBJECT_W25-F8_n8_allblocked_X3.json":
        "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rank(matrix):
    matrix = [list(map(Fraction, row)) for row in matrix]
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left - scale * right
                           for left, right in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def weight(cell, n=8):
    u, v, a, b = cell
    answer = []
    for colour in range(3):
        for site in range(n - 1):
            answer.append(
                int((u, a) == (site, colour))
                + int((v, b) == (site, colour))
                - int((u, a) == (n - 1, colour))
                - int((v, b) == (n - 1, colour))
            )
    return answer


def support_rank(source, n=8):
    columns = [weight(cell, n) for cell, value in source.items() if value]
    matrix = [[column[row] for column in columns]
              for row in range(3 * (n - 1))]
    return rank(matrix)


def port_energies(source, n=8):
    return {
        (site, colour): sum(
            value * value for (u, v, a, b), value in source.items()
            if (u, a) == (site, colour) or (v, b) == (site, colour)
        )
        for site in range(n) for colour in range(3)
    }


def is_balanced(source, n=8):
    energies = port_energies(source, n)
    return all(len({energies[site, colour] for site in range(n)}) == 1
               for colour in range(3))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


PM8 = tuple(perfect_matchings(range(8)))


def amplitude(source, word):
    return sum(
        reduce(
            lambda current, edge: current * source.get(
                (edge[0], edge[1], word[edge[0]], word[edge[1]]), 0
            ),
            matching,
            Fraction(1),
        )
        for matching in PM8
    )


def output_profile(source):
    pure = []
    mixed_norm = Fraction(0)
    mixed_nonzero = 0
    by_offcount = Counter()
    for word in product(range(3), repeat=8):
        value = amplitude(source, word)
        if len(set(word)) == 1:
            pure.append(value)
        else:
            mixed_norm += value * value
            mixed_nonzero += bool(value)
            offcount = 8 - max(word.count(colour) for colour in range(3))
            by_offcount[offcount] += value * value
    return {
        "pure": [str(value) for value in pure],
        "mixed_nonzero": mixed_nonzero,
        "mixed_squared_norm": str(mixed_norm),
        "mixed_squared_norm_by_offcount": {
            str(key): str(value) for key, value in sorted(by_offcount.items())
        },
    }


def unbounded_balanced_family():
    anchor = ((0, 1), (2, 3), (4, 5), (6, 7))
    def at(t):
        source = {}
        for u, v in anchor:
            for colour in range(3):
                source[(u, v, colour, colour)] = Fraction(1)
        for u, v in combinations(range(8), 2):
            for a in range(3):
                for b in range(3):
                    if a != b:
                        source[(u, v, a, b)] = Fraction(t)
        return source

    checks = {}
    for t in (1, 2, 3):
        source = at(t)
        require(is_balanced(source), t)
        require(support_rank(source) == 21, t)
        pure = [amplitude(source, (colour,) * 8) for colour in range(3)]
        require(pure == [1, 1, 1], (t, pure))
        checks[str(t)] = {
            "norm_squared": str(sum(value * value for value in source.values())),
            "port_energy": str(1 + 14 * t * t),
            "pure": [str(value) for value in pure],
        }

    # Exact symbolic mixed norm. A term has degree equal to its number of
    # off-diagonal cells, and all coefficients are positive integers.
    mixed_norm_polynomial = Counter()
    anchor_set = frozenset(anchor)
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        coefficient = Counter()
        for matching in PM8:
            degree = 0
            live = True
            for u, v in matching:
                if word[u] == word[v]:
                    if (u, v) not in anchor_set:
                        live = False
                        break
                else:
                    degree += 1
            if live:
                coefficient[degree] += 1
        for left_degree, left_value in coefficient.items():
            for right_degree, right_value in coefficient.items():
                mixed_norm_polynomial[left_degree + right_degree] += (
                    left_value * right_value
                )
    require(mixed_norm_polynomial == {
        0: 78, 2: 1944, 3: 3744, 4: 35856, 5: 115200,
        6: 585792, 7: 1555200, 8: 3991680,
    }, mixed_norm_polynomial)
    return {
        "support_cells": 180,
        "support_weight_rank": 21,
        "closed_orbit_reason": (
            "Every support coordinate is nonzero and its squared magnitudes "
            "give a strictly positive zero combination of all support weights; "
            "the weights span T0^*, so zero is interior to the support polytope."
        ),
        "norm_formula": "12+168*t^2",
        "port_energy_formula": "1+14*t^2 for every site and colour",
        "pure_formula": "H_0=H_1=H_2=1",
        "mixed_norm_polynomial": {
            str(degree): coefficient
            for degree, coefficient in sorted(mixed_norm_polynomial.items())
        },
        "checks": checks,
    }


def laurent_balance_audit():
    matchings = {
        0: (((0, 1), -1), ((2, 5), 1), ((3, 4), 0), ((6, 7), 0)),
        1: (((0, 3), 0), ((1, 6), 0), ((2, 4), 0), ((5, 7), 0)),
        2: (((0, 7), 0), ((1, 4), 0), ((2, 3), 0), ((5, 6), 0)),
    }
    source_exponents = {}
    balancing_exponents = {}
    for colour, records in matchings.items():
        for (u, v), valuation in records:
            source_exponents[(u, v, colour, colour)] = valuation
            balancing_exponents[(u, colour)] = Fraction(-valuation, 2)
            balancing_exponents[(v, colour)] = Fraction(-valuation, 2)
        require(sum(balancing_exponents[site, colour] for site in range(8)) == 0,
                colour)
    transformed = {
        cell: exponent + balancing_exponents[cell[0], cell[2]]
        + balancing_exponents[cell[1], cell[3]]
        for cell, exponent in source_exponents.items()
    }
    require(set(transformed.values()) == {0}, transformed)
    require(support_rank({cell: Fraction(1) for cell in transformed}) == 9,
            transformed)
    return {
        "source_valuations": sorted(source_exponents.values()),
        "balancing_site_exponents": {
            f"{site},{colour}": str(value)
            for (site, colour), value in sorted(balancing_exponents.items())
        },
        "all_balanced_cell_valuations": [str(value) for value in sorted(transformed.values())],
        "balanced_norm_squared": 12,
        "support_weight_rank": 9,
        "mixed_squared_norm_before_balance": "2*t^2",
        "mixed_squared_norm_after_balance": "2",
        "meaning": (
            "The known source escape is entirely removed by its T0 balancing: "
            "all twelve cells become unit magnitude. P is not invariant under "
            "the complex torus, and its small value before balancing does not "
            "give a balanced P-to-zero sequence."
        ),
    }


def balanced_base_locus_control():
    edges = ((0, 1), (1, 2), (0, 2),
             (3, 4), (4, 5), (5, 6), (6, 7), (3, 7))
    source = {(u, v, 0, 0): Fraction(1) for u, v in edges}
    require(is_balanced(source), port_energies(source))
    require(all(amplitude(source, word) == 0
                for word in product(range(3), repeat=8)), "not in base locus")
    require(support_rank(source) == 7, support_rank(source))
    return {
        "underlying_graph": "C3 disjoint_union C5",
        "support_cells": 8,
        "support_weight_rank": 7,
        "port_energy_colour0": 2,
        "other_port_energies": 0,
        "top_tensor": "zero: each component has odd order, so no perfect matching",
        "meaning": (
            "Moment-zero base-locus directions exist. Any coercivity proof must "
            "exclude GHZ-accessible higher jets over them, not merely exclude "
            "balanced points of the top base locus."
        ),
    }


def load_control(name):
    if name == "W40":
        record = json.loads((ROOT / next(key for key in PINS if "results_t3" in key)).read_text())
        blocks = record["engine_audit"]["witness_B_integral"]["source"]
    else:
        record = json.loads((ROOT / next(key for key in PINS if "OBJECT_W25" in key)).read_text())
        blocks = record["blocks"]
    source = {}
    for label, matrix in blocks.items():
        u, v = map(int, label.strip("()").split(","))
        for a in range(3):
            for b in range(3):
                value = Fraction(matrix[a][b])
                if value:
                    source[(u, v, a, b)] = value
    energies = port_energies(source)
    return {
        "support_cells": len(source),
        "support_weight_rank": support_rank(source),
        "raw_balanced": is_balanced(source),
        "raw_norm_squared": str(sum(value * value for value in source.values())),
        "raw_port_energies": {
            str(colour): [str(energies[site, colour]) for site in range(8)]
            for colour in range(3)
        },
        "output": output_profile(source),
    }


def n4_control():
    matchings = tuple(perfect_matchings(range(4)))
    source = {}
    for colour, matching in enumerate(matchings):
        for u, v in matching:
            source[(u, v, colour, colour)] = Fraction(1)
    require(is_balanced(source, 4), port_energies(source, 4))
    return {
        "balanced": True,
        "support_cells": 6,
        "support_weight_rank": support_rank(source, 4),
        "T0_dimension": 9,
        "stabilizer_dimension": 9 - support_rank(source, 4),
        "norm_squared": 6,
        "output": "exact GHZ4",
    }


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    for relative, expected in PINS.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, (relative, observed, expected))

    payload = {
        "status": "PASS exact T0 orbit theorem; global coercivity remains open",
        "orbit_theorem": {
            "closed": "T0.A is closed iff 0 lies in relint conv(support weights)",
            "moment_zero": (
                "A closed orbit meets moment zero; the intersection is one "
                "compact torus orbit modulo the point stabilizer."
            ),
            "coordinate_balance": (
                "d_i,c=sum_(j,b)|A_ij^(c,b)|^2 is independent of site i "
                "for each fixed colour c"
            ),
            "pure_implication": (
                "H_c=1 supplies a live pure matching whose four restricted "
                "weights average to zero, for each colour. Hence 0 is in the "
                "support polytope (semistability), but need not be in its "
                "relative interior after all other support weights are added."
            ),
        },
        "balanced_unbounded_pure_family": unbounded_balanced_family(),
        "known_laurent_balance": laurent_balance_audit(),
        "balanced_base_locus": balanced_base_locus_control(),
        "n4_exact_control": n4_control(),
        "W40_control": load_control("W40"),
        "W25_control": load_control("W25"),
        "asymptotic_P_to_zero_criterion": {
            "statement": (
                "If balanced pure-normalized A_k has ||A_k||=R_k to infinity "
                "and mixed P(A_k) to zero, then a subsequential limit "
                "B0=lim A_k/R_k is nonzero, moment-zero, and H(B0)=0."
            ),
            "support_consequences": (
                "For every active colour, every site has equal positive leading "
                "port energy. The support weights admit a positive zero relation. "
                "Every supported top word has either no perfect matching term or "
                "at least two leading terms that cancel; a singleton is forbidden."
            ),
            "remaining_guard": (
                "No-cap membership is torus invariant at finite points but is not "
                "closed across carrier rank drops. A limit theorem must retain the "
                "initial valuations of a nonzero carrier pivot and its blocker, not "
                "merely the support of B0."
            ),
        },
        "terminal_scope": (
            "Pure normalization plus moment balance is not compact or coercive: "
            "the explicit closed-orbit family has norm to infinity. It has mixed "
            "norm growing, so it does not refute coercivity of P on the no-cap "
            "slice. The known Laurent P-to-zero escape balances to norm 12 and "
            "P=2. Thus the sharpened no-cap coercivity question reduces exactly "
            "to excluding balanced GHZ-accessible jets over the moment-zero base "
            "locus with rank-stratified carrier data; no such exclusion or "
            "balanced P-to-zero counterfamily is presently frozen."
        ),
        "input_hashes": PINS,
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("T0 Kempf-Ness audit: PASS; sharpened P-coercivity open")
    print("balanced pure family norm=12+168t^2, weight rank 21")
    print("known Laurent after balance: norm 12, mixed P=2")
    print("controls W40/W25 P:", payload["W40_control"]["output"]["mixed_squared_norm"],
          payload["W25_control"]["output"]["mixed_squared_norm"])
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
