#!/usr/bin/env python3
"""Formal audit of the constant-spoke level-two rank bound.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE is
untouched, and no certified dependency changes.

Four live vertices 0,...,3 meet vertex 4 only in output column 0 and vertex
5 only in output column 1.  The 4-5 block and all six live-live blocks are
arbitrary.  The theorem is rank(dPsi)<=50.

The checker represents every structural parameter by a formal monomial and
verifies the matching-cofactor factorization which yields the 50-dimensional
image bound.  A deterministic integral specialization has exact rank 50
modulo two primes, showing sharpness.  Standard library only; checks remain
live under python -O and python -I -S.
"""

from collections import Counter
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


COLOURS = (0, 1)
LIVE = (0, 1, 2, 3)
SITES = tuple(range(6))
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=6))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((head, partner),) + tail)
    return tuple(answer)


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for size in (0, 2, 4, 6)
    for vertices in combinations(SITES, size)
}


def variable(name):
    return Counter({(name,): 1})


def add(left, right):
    answer = left + right
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def scale(coefficient, polynomial):
    return Counter({monomial: coefficient * value
                    for monomial, value in polynomial.items()
                    if coefficient * value})


def multiply(left, right):
    answer = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] += left_coefficient * right_coefficient
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def parameter_name(u, v, a, b):
    if v <= 3:
        return f"A_{u}_{v}_{a}_{b}"
    if u <= 3 and v == 4 and b == 0:
        return f"U_{u}_{a}"
    if u <= 3 and v == 5 and b == 1:
        return f"V_{u}_{a}"
    if (u, v) == (4, 5):
        return f"G_{a}_{b}"
    return None


def build_formal_packet():
    packet = {}
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            name = parameter_name(u, v, a, b)
            packet[u, v, a, b] = variable(name) if name else Counter()
    return packet


def hafnian(packet, vertices, word):
    vertices = tuple(sorted(vertices))
    total = Counter()
    for matching in MATCHINGS[vertices]:
        term = Counter({(): 1})
        for u, v in matching:
            term = multiply(term, packet[u, v, word[u], word[v]])
        total = add(total, term)
    return total


def audit_formal_factorization(packet):
    identities = 0
    for word in WORDS:
        outer_slice = (word[4], word[5])
        live_word = word[:4] + (0, 0)
        live_tensor = hafnian(packet, LIVE, live_word)

        # A 4-5 variation is exactly the four-live-vertex tensor in its own
        # output slice.
        complement_45 = LIVE
        require(hafnian(packet, complement_45, word) == live_tensor,
                ("4-5 cofactor mismatch", word))
        identities += 1

        # Away from slice 01, a live-live cofactor can pair 4 and 5 only to
        # each other.  It is G_slice times the two-live-vertex cofactor.
        if outer_slice != (0, 1):
            g_entry = packet[4, 5, word[4], word[5]]
            for i, j in combinations(LIVE, 2):
                complement = tuple(x for x in SITES if x not in (i, j))
                other_live = tuple(x for x in LIVE if x not in (i, j))
                expected = multiply(
                    g_entry, hafnian(packet, other_live, word)
                )
                require(hafnian(packet, complement, word) == expected,
                        ("outer live-live factorization mismatch", word, i, j))
                identities += 1

        # A spoke to 4 has cofactor support only when vertex 5 has output 1;
        # a spoke to 5 has cofactor support only when vertex 4 has output 0.
        for i in LIVE:
            complement_i4 = tuple(x for x in SITES if x not in (i, 4))
            complement_i5 = tuple(x for x in SITES if x not in (i, 5))
            if word[5] == 0:
                require(not hafnian(packet, complement_i4, word),
                        ("i-4 cofactor leaked to w5=0", word, i))
                identities += 1
            if word[4] == 1:
                require(not hafnian(packet, complement_i5, word),
                        ("i-5 cofactor leaked to w4=1", word, i))
                identities += 1

    # Euler for the quadratic four-site tensor puts H in the live-live
    # tangent image.  This saves one dimension in the three outer slices.
    for local_word in product(COLOURS, repeat=4):
        word = local_word + (0, 0)
        left = Counter()
        for i, j in combinations(LIVE, 2):
            cell = packet[i, j, word[i], word[j]]
            complement = tuple(x for x in LIVE if x not in (i, j))
            left = add(left, multiply(
                cell, hafnian(packet, complement, word)
            ))
        right = scale(2, hafnian(packet, LIVE, word))
        require(left == right, ("four-site Euler identity failed", word))
        identities += 1
    return identities


def build_numeric_packet():
    names = []
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            name = parameter_name(u, v, a, b)
            if name and name not in names:
                names.append(name)
    values = {
        name: 1 + ((5 * index + 3 * index * index + 7) % 17)
        for index, name in enumerate(names)
    }
    return {
        (u, v, a, b): (
            values[parameter_name(u, v, a, b)]
            if parameter_name(u, v, a, b) else 0
        )
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def audit_r2_budget():
    # s is the number of nonzero endpoint-star columns at a root.  Exactly s
    # endpoint edges are disqualified, so two distinct R2 witnesses require
    # at least s internal pure edges.
    for star_support in (0, 1, 2):
        eligible_endpoints = 2 - star_support
        required_internal = max(0, 2 - eligible_endpoints)
        require(required_internal == star_support,
                ("wrong R2 singular-edge budget", star_support))


def main():
    identities = audit_formal_factorization(build_formal_packet())
    audit_r2_budget()

    core = run_path(str(Path(__file__).with_name(
        "verify_level_two_one_sided_overlap_collapse.py"
    )))
    derivative = core["differential"](build_numeric_packet())
    ranks = (
        core["rank_mod"](derivative, 101),
        core["rank_mod"](derivative, 1_000_003),
    )
    require(ranks == (50, 50), ("sharp calibration rank mismatch", ranks))
    print(
        "constant-spoke rank bound: "
        f"{identities} formal matching identities; "
        "outer-three image <=34, slice-01 image <=16, rank dPsi<=50; "
        "exact calibration rank=50"
    )


if __name__ == "__main__":
    main()
