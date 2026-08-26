#!/usr/bin/env python3
"""Exact polarized superpair identity behind the 78+breaker strategy."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_pairconstant_transversal_polarization_identity.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRIANGLES = ((0, 1, 3), (0, 2, 4), (1, 2, 5), (3, 4, 5))
ONE = Counter({(): 1})


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return Counter({key: value for key, value in answer.items() if value})


def scale(polynomial, scalar):
    return Counter({key: scalar * value for key, value in polynomial.items()
                    if scalar * value})


def multiply(*polynomials):
    answer = Counter(ONE)
    for polynomial in polynomials:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                updated[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = Counter({key: value for key, value in updated.items() if value})
    return answer


def variable(edge, left, right):
    return Counter({(4 * edge + 2 * left + right,): 1})


def permanent(edge):
    return add(multiply(variable(edge, 0, 0), variable(edge, 1, 1)),
               multiply(variable(edge, 0, 1), variable(edge, 1, 0)))


def triangle(first, second, third):
    return add(*(multiply(variable(first, ri, rj),
                          variable(second, 1 - ri, rk),
                          variable(third, 1 - rj, 1 - rk))
                 for ri, rj, rk in product(range(2), repeat=3)))


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(((first, second),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))


def matching_polynomial(matching):
    factors = []
    for left_site, right_site in matching:
        left_pair, left_clone = divmod(left_site, 2)
        right_pair, right_clone = divmod(right_site, 2)
        if left_pair == right_pair:
            factors.append(ONE)  # normalized same-colour anchor
        else:
            factors.append(variable(EDGE_INDEX[left_pair, right_pair],
                                    left_clone, right_clone))
    return multiply(*factors)


def transversal(index):
    sites = tuple((index >> (3 - site)) & 1 for site in range(4))
    return add(
        multiply(variable(0, sites[0], sites[1]),
                 variable(5, sites[2], sites[3])),
        multiply(variable(1, sites[0], sites[2]),
                 variable(4, sites[1], sites[3])),
        multiply(variable(2, sites[0], sites[3]),
                 variable(3, sites[1], sites[2])),
    )


def digest(polynomial):
    payload = json.dumps([[list(key), value]
                          for key, value in sorted(polynomial.items())],
                         separators=(",", ":"))
    return sha256(payload.encode("ascii")).hexdigest()


def main() -> None:
    require(len(PM8) == 105, "PM8 census changed")
    permanents = tuple(permanent(edge) for edge in range(6))
    triangles = tuple(triangle(*triple) for triple in TRIANGLES)
    pure_h = add(*(matching_polynomial(matching) for matching in PM8))
    no_anchor = add(*(matching_polynomial(matching) for matching in PM8
                      if all(left // 2 != right // 2
                             for left, right in matching)))
    require(sum(1 for matching in PM8
                if all(left // 2 != right // 2
                       for left, right in matching)) == 60,
            "no-anchor matching census changed")
    q = tuple(transversal(index) for index in range(16))
    self_pair_sum = add(*(multiply(q[index], q[15 - index])
                          for index in range(16)))
    double_pair = add(
        multiply(permanents[0], permanents[5]),
        multiply(permanents[1], permanents[4]),
        multiply(permanents[2], permanents[3]),
    )
    require(self_pair_sum == add(scale(no_anchor, 2),
                                 scale(double_pair, 2)),
            "universal transversal/no-anchor identity failed")
    require(pure_h == add(ONE, *permanents, *triangles, no_anchor),
            "pure Hafnian superpair decomposition failed")

    # Pair-constant equations are e_i=per_i+1 and t_j=tau_j-2.
    e = tuple(add(polynomial, ONE) for polynomial in permanents)
    t = tuple(add(polynomial, scale(ONE, -2)) for polynomial in triangles)
    packet = add(
        self_pair_sum,
        scale(add(multiply(e[0], e[5]), multiply(e[1], e[4]),
                  multiply(e[2], e[3])), -2),
        scale(add(*e), 4),
        scale(add(*t), 2),
    )
    require(packet == scale(pure_h, 2),
            "polarized pairconstant packet did not equal 2H")
    hostile = add(
        self_pair_sum,
        scale(add(multiply(e[0], e[5]), multiply(e[1], e[4]),
                  multiply(e[2], e[3])), -2),
        scale(add(*e), 3),
        scale(add(*t), 2),
    )
    require(hostile != scale(pure_h, 2),
            "coefficient-4 mutation did not fire")

    result = {
        "status": "UNAUDITED exact polarized pairconstant/transversal identity",
        "variables": 24,
        "edge_blocks": 6,
        "normalized_internal_anchors": 4,
        "pairconstant_equations": {
            "e_i": "per(M_i)+1, i=0,...,5",
            "t_j": "triangle_j-2, j=0,...,3",
        },
        "transversal_definition": (
            "Q(s) is the four-site Hafnian on clone selection "
            "s in {0,1}^4; complement index is 15-s."
        ),
        "universal_identity": (
            "sum_s Q(s)Q(sbar)=2D+2(per01 per23+per02 per13+per03 per12), "
            "where D is the 60-term no-anchor part of H."
        ),
        "polarized_packet": (
            "2H = sum_s Q(s)Q(sbar) "
            "-2(e01 e23+e02 e13+e03 e12)+4 sum_i e_i+2 sum_j t_j."
        ),
        "mod_pairconstant_conclusion": "sum_s Q(s)Q(sbar)=2H",
        "term_counts": {
            "pure_H": len(pure_h),
            "no_anchor_D": len(no_anchor),
            "each_Q": sorted(Counter(len(row) for row in q).items()),
            "self_pair_sum": len(self_pair_sum),
        },
        "digests": {
            "pure_H": digest(pure_h),
            "no_anchor_D": digest(no_anchor),
            "self_pair_sum": digest(self_pair_sum),
            "packet_rhs": digest(packet),
        },
        "three_colour_use": (
            "The smallest 48-word breaker orbit supplies cross-colour rows "
            "Q_c(s)Q_d(sbar)=0. Hence any complement pair with nonzero "
            "Q_c(s)Q_c(sbar) is unavailable to the other two colours. The "
            "identity proves only that each live H_c has at least one such "
            "pair; the separate Hensel obstruction shows that a universal "
            "lower bound of three is false in characteristic zero."
        ),
        "scope": (
            "The identity is exact on the same-colour diagonal superpair "
            "locus. Cross-colour cells require additional polarization terms."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("pairconstant/transversal polarization identity: PASS")
    print("H / D / self supports:", len(pure_h), len(no_anchor),
          len(self_pair_sum))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
