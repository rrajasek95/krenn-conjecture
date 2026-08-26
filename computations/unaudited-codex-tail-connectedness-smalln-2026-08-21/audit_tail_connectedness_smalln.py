#!/usr/bin/env python3
"""Exact small-n and algebraic audit of the tail-connectedness proposal."""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_tail_connectedness_smalln.json"
PINS = {
    "computations/unaudited-codex-tail-filtered-lift-obstruction-2026-08-21/REPORT.md":
        "4466c51de6710e3ecacfdca4b8fc4e6203e26c5f09cd4cebc1879b17fbe37610",
    "computations/unaudited-codex-tail-idempotent-remote-2026-08-21/REPORT.md":
        "1fdcc98daf930a655584b129c393e000b71aae8bd63ccec04049ccfacfdf0b59",
    "computations/unaudited-promotion-diag-2026-08-20/proof_eight-site-diagonal-obstruction.md":
        "61371c3c11ac1c5924ce26e79a8e729ab4845ac5b2d58c4bbbb8380331c7e004",
    "computations/unaudited-lean-l1-2026-08-20/work/algal/README.md":
        "9268043f8c4e556b78818f795d2666baf4820119f30c49111cc099ffe842fba5",
    "computations/unaudited-lean-l1-2026-08-20/work/algal/src/ivc/witnesses.py":
        "a36f6540ca49af94e3fd69d64286727e7b6e5e9d5bbc430108c9729d5d897c7b",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


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


def amplitude(word, weights, matchings):
    value = Fraction(0)
    for matching in matchings:
        term = Fraction(1)
        for u, v in matching:
            term *= weights.get((u, v, word[u], word[v]), 0)
        value += term
    return value


def rational_rank(matrix):
    rows = [[Fraction(entry) for entry in row] for row in matrix]
    if not rows:
        return 0
    row_count, column_count = len(rows), len(rows[0])
    pivot = 0
    for column in range(column_count):
        found = next((r for r in range(pivot, row_count)
                      if rows[r][column]), None)
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        scale = rows[pivot][column]
        rows[pivot] = [entry / scale for entry in rows[pivot]]
        for r in range(row_count):
            if r == pivot or not rows[r][column]:
                continue
            scale = rows[r][column]
            rows[r] = [left - scale * right
                       for left, right in zip(rows[r], rows[pivot])]
        pivot += 1
        if pivot == row_count:
            break
    return pivot


def n4_audit():
    sites = range(4)
    edges = tuple(combinations(sites, 2))
    matchings = tuple(perfect_matchings(sites))
    variables = tuple((edge, a, b) for edge in edges
                      for a in range(3) for b in range(3))
    variable_index = {variable: index
                      for index, variable in enumerate(variables)}
    one_factors = matchings
    weights = {}
    for colour, matching in enumerate(one_factors):
        for u, v in matching:
            weights[(u, v, colour, colour)] = Fraction(1)

    values = {}
    jacobian = []
    for word in product(range(3), repeat=4):
        values["".join(map(str, word))] = amplitude(word, weights, matchings)
        row = [Fraction(0)] * len(variables)
        for matching in matchings:
            for edge_position, (u, v) in enumerate(matching):
                cell = ((u, v), word[u], word[v])
                other_u, other_v = matching[1 - edge_position]
                row[variable_index[cell]] += weights.get(
                    (other_u, other_v, word[other_u], word[other_v]), 0)
        jacobian.append(row)

    require(sum(value != 0 for value in values.values()) == 3,
            "n4 witness output support changed")
    require(all(values[str(c) * 4] == 1 for c in range(3)),
            "n4 pure normalization changed")
    cross = [index for index, (_edge, a, b) in enumerate(variables) if a != b]
    diagonal = [index for index, (_edge, a, b) in enumerate(variables) if a == b]
    cross_matrix = [[row[index] for index in cross] for row in jacobian]
    diagonal_matrix = [[row[index] for index in diagonal] for row in jacobian]
    cross_row_counts = [sum(bool(row[index]) for index in cross)
                        for row in jacobian]
    ranks = {
        "total": rational_rank(jacobian),
        "cross": rational_rank(cross_matrix),
        "diagonal": rational_rank(diagonal_matrix),
    }
    require(ranks == {"total": 51, "cross": 36, "diagonal": 15}, ranks)
    require(cross_row_counts.count(1) == 36
            and cross_row_counts.count(0) == 45,
            "n4 cross Jacobian stopped being a monomial matrix")
    return {
        "variables": len(variables),
        "equations": len(values),
        "matching_count": len(matchings),
        "nonzero_outputs": {key: str(value) for key, value in values.items()
                            if value},
        "jacobian_ranks": ranks,
        "tangent_dimension": len(variables) - ranks["total"],
        "cross_columns": len(cross),
        "cross_monomial_rows": cross_row_counts.count(1),
        "component": (
            "The six support cells with three complementary-edge products "
            "equal to one form a closed (G_m)^3. Full cross normal rank 36 "
            "and total tangent dimension 3 make it a smooth component."
        ),
    }


def n6_border_audit():
    sites = range(6)
    matchings = tuple(perfect_matchings(sites))
    x = Fraction(2)
    small, large = x ** -2, x
    weights = {
        (0, 3, 0, 0): small, (1, 4, 0, 0): large,
        (2, 5, 0, 0): large,
        (0, 2, 1, 1): large, (1, 5, 1, 1): small,
        (3, 4, 1, 1): large,
        (0, 5, 2, 2): large, (1, 3, 2, 2): large,
        (2, 4, 2, 2): small,
    }
    nonzero = {}
    for word in product(range(3), repeat=6):
        value = amplitude(word, weights, matchings)
        if value:
            nonzero["".join(map(str, word))] = value
    require(nonzero == {
        "000000": Fraction(1), "111111": Fraction(1),
        "222222": Fraction(1), "012021": Fraction(1, 64),
    }, nonzero)
    return {
        "matching_count": len(matchings),
        "test_parameter": str(x),
        "nonzero_outputs": {key: str(value) for key, value in nonzero.items()},
        "symbolic_mixed_residue": "F_012021=x^(-6)",
        "meaning": (
            "The exact diagonal Laurent family approaches GHZ only at "
            "x=infinity. The frozen unrestricted n=6 theorem says the "
            "normalized full fibre itself is empty."
        ),
    }


def logical_sha(payload):
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    for relative, expected in PINS.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, (relative, observed, expected))

    payload = {
        "status": "PASS exact tail-connectedness small-n no-go audit",
        "n4": n4_audit(),
        "n6": n6_border_audit(),
        "n8_algebra": {
            "ring": "A8=Q[source cells]/(all mixed F_w, F_c^pure-1)",
            "full_tail_ideal": "J8=(A_uv[a,b]:a!=b)",
            "diagonal_quotient": (
                "A8/J8 is the normalized block-diagonal n=8,d=3 fibre ring"
            ),
            "audited_input": (
                "The frozen N8-DIAGONAL theorem says this fibre is empty over "
                "every field; over Q, A8/J8=0 by Nullstellensatz/base change."
            ),
            "consequence": (
                "J8=A8. Therefore J8=J8^2 already, and on any hypothetical "
                "nonzero full fibre its idempotent is e=1: the entire fibre "
                "is remote. Connectedness cannot force e=0."
            ),
        },
        "grading_audit": {
            "full_site_multigrading": (
                "All amplitudes are multihomogeneous before normalization, "
                "but F_(c^n)=1 destroys every positive source grading."
            ),
            "normalization_preserving_torus": (
                "The residual torus grading survives, but each pure perfect-"
                "matching monomial has character zero and equals part of 1; "
                "hence the degree-zero ring is not the ground field."
            ),
            "idempotents": (
                "A connected torus fixes the finite set of components, so an "
                "idempotent has weight zero. This does not make it scalar."
            ),
        },
        "rees_audit": {
            "affine_countercontrol": (
                "Q[s,t]/(t-s*t^2)=Q[s] x Q[s,s^-1] is flat and has a remote "
                "generic branch t=1/s missing the special fibre."
            ),
            "source_control": (
                "The n=6 Erhard family has pure outputs one and mixed residue "
                "x^-6, so GHZ is reached only at infinity despite the exact "
                "affine fibre being empty."
            ),
            "missing_hypothesis": (
                "A proper flat compactification with no loss of the three "
                "nonzero pure anchors would prevent generic-only escape. The "
                "normalized source fibre is affine/nonproper, and known "
                "Laurent arcs show precisely this escape at infinity."
            ),
        },
        "terminal_verdict": (
            "Connectedness is not a route to killing the n=8 remote factor. "
            "The full zero-tail fibre is empty, so the full tail ideal is the "
            "unit ideal and e=1. At n=4 the zero-tail torus is already a "
            "smooth component; at n=6 the fibre is empty. A small-n induction "
            "would need the unavailable and false-in-scope hypothesis of a "
            "nonempty zero-tail fibre plus proper no-escape deformation."
        ),
        "input_hashes": PINS,
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("tail connectedness small-n audit: PASS")
    print("n4 Jacobian ranks total/cross/diagonal: 51/36/15")
    print("n6 border residue: F_012021=x^-6")
    print("n8 full-tail consequence: A8/J8=0, hence J8=A8 and e=1")
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
