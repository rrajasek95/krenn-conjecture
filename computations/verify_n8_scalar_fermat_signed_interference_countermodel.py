#!/usr/bin/env python3
"""Exact scalar-Fermat countermodel produced by signed matching interference.

The general eight-site matching tensor may be diagonally scalarized by using
the same variables x_0,x_1,x_2 at every output site.  Exact tensor equality
would imply

    haf(B(x)) = x_0^8 + x_1^8 + x_2^8,

where every edge B_uv is a ternary quadratic.  This checker constructs an
exact integral solution of that scalar identity which is *not* an exact
tensor source: two different mixed output words have coefficients +1 and -1
and disappear only after the site labels are forgotten.

Companion note:
  notes/n8-scalar-fermat-signed-interference-countermodel.md
"""

from __future__ import annotations

import json
from functools import lru_cache
from hashlib import sha256


EXPECTED_LEDGER_SHA256 = (
    "a1ab0292e17c8000ec081afd2599180dc723dad66b1c0cee4378b1f92a376f3f"
)
N = 8
ZERO = (0, 0, 0)


def require(condition, detail):
    """Assertion that survives ``python -O``."""
    if not condition:
        raise RuntimeError(detail)


def add(left, right):
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, 0) + coefficient
        if answer[exponent] == 0:
            del answer[exponent]
    return answer


def multiply(left, right):
    answer = {}
    for alpha, a_coefficient in left.items():
        for beta, b_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(alpha, beta))
            answer[exponent] = answer.get(exponent, 0) + a_coefficient * b_coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items()
            if coefficient}


def monomial(colour, coefficient=1):
    exponent = [0, 0, 0]
    exponent[colour] = 2
    return {tuple(exponent): coefficient}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


# Three pure matchings on the seven-site cofactor packet.  The negative
# 0-edge makes the two extra 0/1/2 matchings cancel.
EDGE_DATA = {
    (0, 1): (0, -1),
    (0, 2): (1, +1),
    (0, 3): (2, +1),
    (1, 4): (1, +1),
    (1, 5): (2, +1),
    (2, 3): (0, -1),
    (2, 7): (2, +1),
    (3, 6): (1, +1),
    (4, 5): (0, +1),
    (4, 6): (2, +1),
    (5, 7): (1, +1),
    (6, 7): (0, +1),
}
EDGE_POLYNOMIALS = {
    edge: monomial(colour, coefficient)
    for edge, (colour, coefficient) in EDGE_DATA.items()
}


@lru_cache(maxsize=None)
def hafnian(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return {ZERO: 1}
    first = vertices[0]
    answer = {}
    for index in range(1, len(vertices)):
        partner = vertices[index]
        edge = tuple(sorted((first, partner)))
        if edge not in EDGE_POLYNOMIALS:
            continue
        rest = vertices[1:index] + vertices[index + 1:]
        answer = add(answer, multiply(EDGE_POLYNOMIALS[edge], hafnian(rest)))
    return answer


def matching_record(matching):
    coefficient = 1
    exponent = [0, 0, 0]
    word = [None] * N
    for raw_edge in matching:
        edge = tuple(sorted(raw_edge))
        if edge not in EDGE_DATA:
            return None
        colour, scalar = EDGE_DATA[edge]
        coefficient *= scalar
        exponent[colour] += 2
        for site in edge:
            word[site] = colour
    return {
        "matching": "|".join(f"{u}{v}" for u, v in sorted(matching)),
        "coefficient": coefficient,
        "exponent": tuple(exponent),
        "word": "".join(str(colour) for colour in word),
    }


def canonical(value):
    if isinstance(value, dict):
        return {str(key): canonical(item)
                for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    full = hafnian(tuple(range(N)))
    target = {(8, 0, 0): 1, (0, 8, 0): 1, (0, 0, 8): 1}
    require(full == target, ("scalar Fermat identity failed", full))

    cofactors = {
        partner: hafnian(tuple(site for site in range(1, N) if site != partner))
        for partner in (1, 2, 3)
    }
    expected_cofactors = {
        1: {(6, 0, 0): -1},
        2: {(0, 6, 0): +1},
        3: {(0, 0, 6): +1},
    }
    require(cofactors == expected_cofactors,
            ("three cofactor identities changed", cofactors))

    records = []
    for matching in perfect_matchings(range(N)):
        record = matching_record(matching)
        if record is not None:
            records.append(record)
    records.sort(key=lambda record: record["matching"])
    require(len(records) == 5, ("supported matching count changed", records))

    pure = [record for record in records if len(set(record["word"])) == 1]
    mixed = [record for record in records if len(set(record["word"])) > 1]
    require(len(pure) == 3 and all(record["coefficient"] == 1 for record in pure),
            ("pure matching packet changed", pure))
    require(
        [(record["exponent"], record["coefficient"]) for record in mixed]
        == [((4, 2, 2), +1), ((4, 2, 2), -1)],
        ("signed mixed cancellation changed", mixed),
    )
    require(mixed[0]["word"] != mixed[1]["word"],
            ("the cancelling tensor words unexpectedly coincide", mixed))
    tensor_coefficients = {record["word"]: record["coefficient"] for record in records}
    require(tensor_coefficients[mixed[0]["word"]] == +1
            and tensor_coefficients[mixed[1]["word"]] == -1,
            ("mixed tensor coefficients disappeared before scalarization", tensor_coefficients))

    # Expansion at site 0 is an independent reconstruction of the identity.
    reconstructed = {}
    for partner in (1, 2, 3):
        reconstructed = add(
            reconstructed,
            multiply(EDGE_POLYNOMIALS[(0, partner)], cofactors[partner]),
        )
    require(reconstructed == target,
            ("site-zero cofactor reconstruction failed", reconstructed))

    ledger = canonical({
        "edge_data": EDGE_DATA,
        "cofactors": cofactors,
        "full_scalar_hafnian": full,
        "supported_matchings": records,
        "mixed_tensor_words": [record["word"] for record in mixed],
        "mixed_scalar_exponent": mixed[0]["exponent"],
        "mixed_signed_sum": sum(record["coefficient"] for record in mixed),
    })
    digest = sha256(json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                ("scalar-Fermat interference ledger changed", digest))

    print("n=8 scalar Fermat signed-interference countermodel: PASS")
    print("  supported physical matchings : 5")
    print("  pure target matchings        : 3")
    print("  mixed tensor words           :", ", ".join(record["word"] for record in mixed))
    print("  mixed scalar coefficients    : +1, -1")
    print("  scalar hafnian               : x0^8 + x1^8 + x2^8")


if __name__ == "__main__":
    main()
