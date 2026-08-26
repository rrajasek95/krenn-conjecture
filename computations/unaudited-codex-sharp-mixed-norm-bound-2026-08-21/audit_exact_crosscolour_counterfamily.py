#!/usr/bin/env python3
"""Exact algebraic balanced clean-cap family with P_mixed < 2 near Laurent."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from math import comb
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from probe_laurent_second_variation import LAYERS, PM8


OUT = HERE / "results_exact_crosscolour_counterfamily.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(poly, exponent, coefficient):
    poly[exponent] = poly.get(exponent, Fraction(0)) + coefficient
    if not poly[exponent]:
        del poly[exponent]


def multiply(left, right):
    answer = defaultdict(Fraction)
    for (r1, t1), c1 in left.items():
        for (r2, t2), c2 in right.items():
            add(answer, (r1 + r2, t1 + t2), c1 * c2)
    return dict(answer)


def add_poly(left, right):
    answer = dict(left)
    for exponent, coefficient in right.items():
        add(answer, exponent, coefficient)
    return answer


def square(poly):
    return multiply(poly, poly)


def source():
    # A coefficient is a Laurent monomial coefficient * r^a * t^b.
    answer = {}
    for colour, edges in LAYERS.items():
        for e in edges:
            if colour == 1:
                value = {(0, 0): Fraction(1)}
            elif (colour, e) in ((0, (2, 5)), (2, (0, 7))):
                value = {(-3, 0): Fraction(1)}
            else:
                value = {(1, 0): Fraction(1)}
            answer[(*e, colour, colour)] = value
    answer[(0, 2, 2, 0)] = {(0, 1): Fraction(1)}
    answer[(5, 7, 0, 2)] = {(0, 1): Fraction(-1)}
    return answer


def cell(src, u, v, a, b):
    if u < v:
        return src.get((u, v, a, b), {})
    return src.get((v, u, b, a), {})


def identity_response_support(src, p, q):
    residual = tuple(site for site in range(8) if site not in (p, q))
    support = []
    for a_index in range(len(residual)):
        for b_index in range(a_index + 1, len(residual)):
            a, b = residual[a_index], residual[b_index]
            for alpha in range(3):
                for beta in range(3):
                    value = {}
                    for colour in range(3):
                        value = add_poly(value, multiply(
                            cell(src, p, a, colour, alpha),
                            cell(src, q, b, colour, beta),
                        ))
                        value = add_poly(value, multiply(
                            cell(src, p, b, colour, beta),
                            cell(src, q, a, colour, alpha),
                        ))
                    if value:
                        support.append(((a, b), (alpha, beta), value))
    return support


def amplitudes(src):
    by_edge = defaultdict(list)
    for (u, v, a, b), value in src.items():
        by_edge[u, v].append((a, b, value))
    answer = defaultdict(lambda: defaultdict(Fraction))
    for matching in PM8:
        choices = [by_edge[edge] for edge in matching]
        if not all(choices):
            continue
        for selected in product(*choices):
            word = [None] * 8
            value = {(0, 0): Fraction(1)}
            for (u, v), (a, b, monomial) in zip(matching, selected):
                word[u], word[v] = a, b
                value = multiply(value, monomial)
            for exponent, coefficient in value.items():
                add(answer[tuple(word)], exponent, coefficient)
    return {word: dict(value) for word, value in answer.items()}


def substitute_t_squared(poly):
    # t^2 = r^2-r^-6, which is exactly the moment/pure constraint.
    answer = defaultdict(Fraction)
    for (r_exponent, t_exponent), coefficient in poly.items():
        require(t_exponent % 2 == 0, (r_exponent, t_exponent, coefficient))
        power = t_exponent // 2
        for negative_count in range(power + 1):
            # Choose negative r^-6 factors and positive r^2 factors.
            exponent = r_exponent + 2 * (power - negative_count) - 6 * negative_count
            value = coefficient * comb(power, negative_count) * (-1) ** negative_count
            add(answer, exponent, value)
    return dict(answer)


def format_laurent(poly):
    terms = []
    for exponent, coefficient in sorted(poly.items(), reverse=True):
        terms.append(f"({coefficient})*r^{exponent}")
    return " + ".join(terms) if terms else "0"


def evaluate(poly, value):
    return sum(float(coefficient) * value ** exponent
               for exponent, coefficient in poly.items())


def evaluate_exact(poly, value):
    return sum(coefficient * value ** exponent
               for exponent, coefficient in poly.items())


def derivative_polynomial(value):
    return (3 * value**8 + 2 * value**7 + value**6 + 3 * value**4
            + 2 * value**3 + 3 * value**2 - 20)


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-cap", action="store_true")
    args = parser.parse_args()
    src = source()
    amps = amplitudes(src)
    require(amps[(0,) * 8] == {(0, 0): Fraction(1)}, amps[(0,) * 8])
    require(amps[(1,) * 8] == {(0, 0): Fraction(1)}, amps[(1,) * 8])
    require(amps[(2,) * 8] == {(0, 0): Fraction(1)}, amps[(2,) * 8])
    mixed = {word: value for word, value in amps.items() if len(set(word)) > 1}
    p_rt = defaultdict(Fraction)
    for value in mixed.values():
        for exponent, coefficient in square(value).items():
            add(p_rt, exponent, coefficient)
    require(all(t_power % 2 == 0 for _, t_power in p_rt), p_rt)
    p_r = substitute_t_squared(p_rt)
    p_minus_two = dict(p_r)
    add(p_minus_two, 0, Fraction(-2))

    # Exact port balance: colours 0 and 2 have squared energy r^2 at every
    # port, because the special anchor has r^-6 and leakage t^2=r^2-r^-6.
    # Colour 1 has unit energy.  Pure products are r^3*r^-3=1.
    block_occupancies = Counter((u, v) for u, v, _, _ in src)
    require(max(block_occupancies.values()) == 2, block_occupancies)
    require(all(value <= 2 for value in block_occupancies.values()), block_occupancies)

    cap_source = dict(src)
    if args.mutate_cap:
        cap_source.pop((6, 7, 0, 0))
    identity_caps = []
    for p, q in sorted(block_occupancies):
        scalar = add_poly(add_poly(cell(cap_source, p, q, 0, 0),
                                   cell(cap_source, p, q, 1, 1)),
                          cell(cap_source, p, q, 2, 2))
        if not scalar:
            continue
        support = identity_response_support(cap_source, p, q)
        centres = [site for site in range(8) if site not in (p, q)
                   and support and all(site in item[0] for item in support)]
        identity_caps.append({
            "pair": (p, q),
            "response_cells": len(support),
            "response_edges": len({item[0] for item in support}),
            "star_centres": tuple(centres),
        })
    witness_pairs = {record["pair"] for record in identity_caps
                     if record["star_centres"]}
    require((6, 7) in witness_pairs, "pair67 active clean-cap witness deleted")

    x_left, x_right = Fraction(1073, 1000), Fraction(537, 500)
    require(derivative_polynomial(x_left) < 0 < derivative_polynomial(x_right),
            (x_left, x_right))
    x_witness = Fraction(101, 100)
    p_witness = evaluate_exact(p_r, x_witness)
    require(p_witness < 2, p_witness)

    output_rows = {
        "".join(map(str, word)): {
            f"r^{r_power}*t^{t_power}": str(coefficient)
            for (r_power, t_power), coefficient in sorted(value.items())
        }
        for word, value in sorted(amps.items())
    }
    payload = {
        "status": "PASS exact balanced clean-cap counterfamily to universal P>=2",
        "parameterization": {
            "x": "r^2 > 1",
            "t_squared": "x-x^-3",
            "special_anchor_magnitude": "r^-3",
            "ordinary_anchor_magnitude": "r",
            "leakage_cells": ["A_02[2,0]=t", "A_57[0,2]=-t"],
            "balance": "port energy x in colours 0,2 and 1 in colour 1",
            "pure": "r^3*r^-3=1 in colours 0,2; colour 1 is unit",
        },
        "P_of_x": "x^3+x^2+x-3*x^-1-x^-2-x^-3+4*x^-5",
        "P_minus_2_numerator": (
            "x^8+x^7+x^6-2*x^5-3*x^4-x^3-x^2+4"
        ),
        "exact_less_than_2_witness": {
            "x": str(x_witness), "P": str(p_witness), "P_less_than_2": True,
        },
        "global_minimum": {
            "critical_polynomial": (
                "D(x)=3*x^8+2*x^7+x^6+3*x^4+2*x^3+3*x^2-20"
            ),
            "uniqueness": "D'(x)>0 for x>0",
            "root_bracket": [str(x_left), str(x_right)],
            "approx_x": 1.0732667367,
            "approx_P": 1.798070075935623,
            "P_never_zero": (
                "For x>1, t^2=x-x^-3>0 and mixed amplitude 11111012=-t."
            ),
        },
        "outputs": output_rows,
        "output_counts": {"nonzero": len(amps), "pure": 3, "mixed": len(mixed)},
        "active_identity_response_star_caps": [
            {**record, "pair": list(record["pair"]),
             "star_centres": list(record["star_centres"])}
            for record in identity_caps if record["star_centres"]
        ],
        "cap_scope": (
            "Each listed K=I cap has nonzero trace scalar and kappa=(1,1,1); "
            "star response support gives r^2=0, hence an active clean cap. "
            "The family refutes the unrestricted bound, not a no-cap bound."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print("source cells", len(src), "max cells per physical block", max(block_occupancies.values()))
    print("nonzero output words/mixed", len(amps), len(mixed))
    print("P(r,t)=", format_laurent(p_rt))
    print("P(r)=", format_laurent(p_r))
    print("P(r)-2=", format_laurent(p_minus_two))
    print("nearby exact checks", {str(x): evaluate(p_r, x) for x in (1.001, 1.01, 1.05, 1.1, 1.2, 2.0)})
    print("amplitudes")
    for word, value in sorted(amps.items()):
        print("".join(map(str, word)), format_laurent(value))
    print("active identity-cap star screen")
    for record in identity_caps:
        print(record)
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
