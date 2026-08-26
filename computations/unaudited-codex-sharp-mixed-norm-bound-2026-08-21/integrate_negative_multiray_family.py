#!/usr/bin/env python3
"""Formal exact integration of the six-cell negative Laurent tangent.

The three diagonal-colour layers are rescaled by analytic algebraic functions
so every port energy is constant within a colour and every pure hafnian stays
one.  Rational power series certify existence by the implicit-function
theorem and give every output through the requested order.  A separate
support audit proves that all 168 response stars and 560 response triangles
contain a literal monomial row isolating a diagonal K coordinate.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE / "results_negative_multiray_integrated_family.json"
sys.path.insert(0, str(HERE))
from probe_laurent_second_variation import BASE, LAYERS, PM8  # noqa: E402


ORDER = 10
A = Fraction(1, 2)
D = Fraction(1)
E = Fraction(1, 10)
LEAK = {
    (2, 5, 1, 2): A,
    (4, 6, 1, 2): A,
    (0, 2, 2, 0): D,
    (5, 7, 0, 2): -D,
    (0, 4, 2, 0): -E,
    (3, 7, 0, 2): E,
}

# Squared leakage energy on each diagonal anchor edge, as a multiple of s^2.
ENERGY = {
    0: {(0, 1): 0, (2, 5): D * D, (3, 4): E * E, (6, 7): 0},
    1: {(0, 3): 0, (1, 6): 0, (2, 4): A * A, (5, 7): 0},
    2: {(0, 7): D * D + E * E, (1, 4): 0,
        (2, 3): 0, (5, 6): A * A},
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sadd(left, right):
    n = max(len(left), len(right))
    return tuple((left[i] if i < len(left) else 0)
                 + (right[i] if i < len(right) else 0) for i in range(n))


def smul(left, right, order=ORDER):
    answer = [Fraction(0)] * (order + 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            if i + j <= order:
                answer[i + j] += x * y
    return tuple(answer)


def spow(value, exponent, order=ORDER):
    answer = (Fraction(1),) + (Fraction(0),) * order
    for _ in range(exponent):
        answer = smul(answer, value, order)
    return answer


def rho_series(edge_energies, order=ORDER // 2):
    """Solve product_e (rho-k_e*u)=1 near rho=1 in Q[[u]]."""
    rho = [Fraction(1)] + [Fraction(0)] * order

    def equation(series):
        value = (Fraction(1),) + (Fraction(0),) * order
        for k in edge_energies:
            factor = list(series)
            factor[1] -= k
            value = smul(value, tuple(factor), order)
        value = list(value)
        value[0] -= 1
        return value

    for degree in range(1, order + 1):
        rho[degree] = 0
        residual = equation(rho)[degree]
        # At u=0, derivative in rho of the four-factor product is four.
        rho[degree] = -residual / 4
        require(equation(rho)[degree] == 0, (degree, rho, equation(rho)))
    return tuple(rho)


def sqrt_series(target, order=ORDER // 2):
    answer = [Fraction(1)] + [Fraction(0)] * order
    for degree in range(1, order + 1):
        known = sum(answer[i] * answer[degree - i]
                    for i in range(1, degree))
        answer[degree] = (target[degree] - known) / 2
    require(smul(tuple(answer), tuple(answer), order) == tuple(target),
            (target, answer))
    return tuple(answer)


def u_to_s(series, order=ORDER):
    answer = [Fraction(0)] * (order + 1)
    for degree, value in enumerate(series):
        if 2 * degree <= order:
            answer[2 * degree] = value
    return tuple(answer)


def source_series():
    source = {}
    rho = {}
    for colour, layer in LAYERS.items():
        ks = [ENERGY[colour][edge] for edge in layer]
        rho[colour] = rho_series(ks)
        for edge, k in zip(layer, ks):
            target = list(rho[colour])
            target[1] -= k
            source[edge + (colour, colour)] = u_to_s(sqrt_series(target))
    for cell, coefficient in LEAK.items():
        value = [Fraction(0)] * (ORDER + 1)
        value[1] = coefficient
        source[cell] = tuple(value)
    return rho, source


def get_edge_cells(source):
    answer = defaultdict(list)
    for (u, v, a, b), value in source.items():
        answer[u, v].append((a, b, value))
    return answer


def outputs(source):
    edge_cells = get_edge_cells(source)
    answer = defaultdict(lambda: (Fraction(0),) * (ORDER + 1))
    for matching in PM8:
        choices = [edge_cells[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [None] * 8
            amplitude = (Fraction(1),) + (Fraction(0),) * ORDER
            for (u, v), (a, b, value) in zip(matching, picked):
                word[u], word[v] = a, b
                amplitude = smul(amplitude, value)
            key = tuple(word)
            answer[key] = sadd(answer[key], amplitude)
    return {word: value for word, value in answer.items() if any(value)}


def leading(series):
    for degree, value in enumerate(series):
        if value:
            return degree, value
    return None


def moment_and_pure_checks(rho, source, output):
    # The support is Gram-orthogonal at each port: no two cells sharing a
    # physical edge and remote colour have different local colours.
    for site in range(8):
        for colour in range(3):
            energy = (Fraction(0),) * (ORDER + 1)
            for (u, v, a, b), value in source.items():
                if (u == site and a == colour) or (v == site and b == colour):
                    energy = sadd(energy, smul(value, value))
            require(energy == u_to_s(rho[colour]),
                    (site, colour, energy, rho[colour]))
    for colour in range(3):
        word = (colour,) * 8
        expected = (Fraction(1),) + (Fraction(0),) * ORDER
        require(output[word] == expected, (colour, output[word]))


def mixed_norm(output):
    answer = (Fraction(0),) * (ORDER + 1)
    for word, amplitude in output.items():
        if len(set(word)) > 1:
            answer = sadd(answer, smul(amplitude, amplitude))
    return answer


def occupied(support, u, v, a, b):
    return (u, v, a, b) in support if u < v else (v, u, b, a) in support


def literal_diagonal_witness(support, p, q, allowed_edges):
    residual = tuple(site for site in range(8) if site not in (p, q))
    for a, b in combinations(residual, 2):
        if (a, b) in allowed_edges:
            continue
        for alpha in range(3):
            for beta in range(3):
                terms = []
                for i in range(3):
                    for j in range(3):
                        if (occupied(support, p, a, i, alpha)
                                and occupied(support, q, b, j, beta)):
                            terms.append((3 * i + j, "direct"))
                        if (occupied(support, p, b, i, beta)
                                and occupied(support, q, a, j, alpha)):
                            terms.append((3 * i + j, "cross"))
                if len(terms) == 1 and terms[0][0] in (0, 4, 8):
                    return (a, b, alpha, beta, terms[0])
    return None


def carrier_witnesses(source):
    support = set(source)
    stars = []
    triangles = []
    for p, q in combinations(range(8), 2):
        residual = tuple(site for site in range(8) if site not in (p, q))
        for centre in residual:
            allowed = {edge for edge in combinations(residual, 2)
                       if centre in edge}
            witness = literal_diagonal_witness(support, p, q, allowed)
            require(witness is not None, ("star", p, q, centre))
            stars.append((p, q, centre, witness))
        for triangle in combinations(residual, 3):
            allowed = set(combinations(triangle, 2))
            witness = literal_diagonal_witness(support, p, q, allowed)
            require(witness is not None, ("triangle", p, q, triangle))
            triangles.append((p, q, triangle, witness))
    return stars, triangles


def render(series):
    return {degree: str(value) for degree, value in enumerate(series) if value}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-delete-leak", action="store_true")
    parser.add_argument("--mutate-delete-carrier-cell", action="store_true")
    args = parser.parse_args()
    rho, source = source_series()
    if args.mutate_delete_leak:
        del source[(3, 7, 0, 2)]
    output = outputs(source)
    moment_and_pure_checks(rho, source, output)
    p = mixed_norm(output)
    require(p[0] == 2, p)
    require(p[2] == Fraction(-51, 200), p)
    carrier_source = dict(source)
    if args.mutate_delete_carrier_cell:
        for cell in LEAK:
            del carrier_source[cell]
    stars, triangles = carrier_witnesses(carrier_source)
    print("rho(u)", {c: render(value) for c, value in rho.items()})
    print("nonzero outputs", len(output), "mixed", sum(len(set(w)) > 1 for w in output))
    print("P_mixed(s)", render(p))
    print("leading output ledger")
    for word, value in sorted(output.items(), key=lambda item: (leading(item[1]), item[0])):
        print("OUTPUT", "".join(map(str, word)), "lead", leading(value), "series", render(value))
    print("literal carrier blockers", len(stars), len(triangles),
          "total", len(stars) + len(triangles))
    require(len(stars) == 168 and len(triangles) == 560,
            (len(stars), len(triangles)))
    payload = {
        "scope": {
            "base": "unit diagonal Laurent equality support",
            "leakage_coefficients": {
                str(cell): str(value) for cell, value in sorted(LEAK.items())
            },
            "series_order": ORDER,
            "carrier_scope": "all 168 response stars and 560 response triangles; arbitrary 3x3 K",
        },
        "algebraic_integration": {
            "rho_equations": {
                "0": "rho0^2*(rho0-s^2)*(rho0-s^2/100)=1",
                "1": "rho1^3*(rho1-s^2/4)=1",
                "2": "rho2^2*(rho2-101*s^2/100)*(rho2-s^2/4)=1",
            },
            "rho_u_series": {str(c): render(value) for c, value in rho.items()},
            "moment": "each site-colour port energy equals rho_c; all off-diagonal port Gram entries vanish structurally",
            "pure": "H_0=H_1=H_2=1 exactly on the analytic branches rho_c(0)=1",
        },
        "outputs": {
            "nonzero_count": len(output),
            "mixed_count": sum(len(set(word)) > 1 for word in output),
            "ledger": {
                "".join(map(str, word)): {
                    "leading": [leading(value)[0], str(leading(value)[1])],
                    "series": render(value),
                }
                for word, value in sorted(output.items())
            },
        },
        "mixed_norm_series": render(p),
        "carrier_blockers": {
            "stars": len(stars),
            "triangles": len(triangles),
            "witnesses": {
                "stars": repr(stars),
                "triangles": repr(triangles),
            },
            "proof": "each carrier has a forbidden response row consisting of one nonzero source monomial times one diagonal K_cc coordinate",
        },
        "theorem": "There is an exact balanced pure-normalized analytic no-response-carrier family with P_mixed=2-51*s^2/200+O(s^4)<2 for all sufficiently small nonzero real s.",
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["logical_sha256"] = sha256(raw).hexdigest()
    print("logical sha256", payload["logical_sha256"])
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print("wrote", OUT)


if __name__ == "__main__":
    main()
