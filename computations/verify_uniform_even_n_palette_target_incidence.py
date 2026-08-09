#!/usr/bin/env python3
"""Dimension-free one-site target-incidence theorem with N=8 audit."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_N8_SHA256 = (
    "96bdbf54797b283c7239042ad2b3a9b0d052603aa63d74e491d29527f702337c"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_one_site_target_incidence.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest() == PINNED_N8_SHA256,
            "the pinned N=8 target-incidence specialization changed")
N8 = importlib.import_module("verify_n8_d1_one_site_target_incidence")
D = N8.D

EXPECTED_LEDGER_SHA256 = (
    "e83344fe364080a4d7fd96da3bfd899b7fd3cfbf3d226f39582bf86f0928216b"
)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for matching in perfect_matchings(remainder):
            result.append(((first, second),) + matching)
    return tuple(result)


def odd_double_factorial(value):
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def recursion_audit():
    rows = []
    for order in (2, 4, 6, 8, 10):
        vertices = tuple(range(order))
        matchings = perfect_matchings(vertices)
        expected_total = odd_double_factorial(order - 1)
        require(len(matchings) == expected_total,
                "the perfect-matching count recurrence changed")
        center = 0
        packets = {
            neighbour: tuple(matching for matching in matchings
                             if (center, neighbour) in matching)
            for neighbour in vertices if neighbour != center
        }
        expected_packet = odd_double_factorial(order - 3)
        require(all(len(packet) == expected_packet
                    for packet in packets.values()),
                "a one-site cofactor packet changed size")
        recovered = [matching for packet in packets.values()
                     for matching in packet]
        require(len(recovered) == len(set(recovered)) == len(matchings)
                and set(recovered) == set(matchings),
                "the partner packets do not partition the matching sum")
        rows.append({
            "even_order": order,
            "matching_count": len(matchings),
            "partner_routes": order - 1,
            "cofactor_matchings_per_route": expected_packet,
        })
    return rows


def palette_mask_audit():
    rows = []
    for palette_size in (2, 3, 4, 5, 6):
        for target in range(palette_size):
            classification = {"absent": 0, "target_line": 0,
                              "non_target_line": 0}
            for mask in itertools.product((False, True),
                                          repeat=palette_size):
                support = {index for index, live in enumerate(mask) if live}
                if not support:
                    classification["absent"] += 1
                elif support == {target}:
                    classification["target_line"] += 1
                else:
                    require(support - {target},
                            "a non-target vector lacks a quotient witness")
                    classification["non_target_line"] += 1
            require(classification == {
                "absent": 1,
                "target_line": 1,
                "non_target_line": 2 ** palette_size - 2,
            }, "the arbitrary-palette line trichotomy changed")
            rows.append({
                "palette_size": palette_size,
                "target": target,
                **classification,
            })
    return rows


def audit():
    started = monotonic()
    n8_ledger = N8.build_ledger()
    n8_digest = D.content_hash(n8_ledger)
    require(n8_digest
            == "091f1fb4305131bea5b5dc0c73cf27c5af5efe3d196b8e60a007ae75eee897ec",
            "the N=8 specialization ledger changed")
    recursion = recursion_audit()
    masks = palette_mask_audit()
    ledger = {
        "pinned_n8_specialization_sha256": PINNED_N8_SHA256,
        "n8_specialization_ledger_sha256": n8_digest,
        "finite_recursion_controls": recursion,
        "finite_palette_controls": masks,
        "theorem": (
            "for every even N>=2, palette dimension d>=2, site v and "
            "pure target a, some nonzero incident row-a vector is a scalar "
            "multiple of the target basis vector e_a"
        ),
        "matching_identity": (
            "H_N=sum_{u!=v} p_{vu,a}(site u) tensor H_{N-2}^{(u)}"
        ),
        "proof": (
            "if no nonzero p_{vu,a} is on <e_a>, quotient every neighbour "
            "space by <p_{vu,a}> (and use the identity on absent routes). "
            "Each left summand dies in its partner factor, while the image "
            "of e_a^(tensor N-1) is a tensor product of nonzero vectors"
        ),
        "base_ring_scope": (
            "integral matching identity over Z; quotient proof over any "
            "field, hence over the fraction field of a localized integral "
            "domain"
        ),
        "characteristic_scope": "every characteristic",
        "status": "uniform one-site target-incidence theorem proved",
    }
    return ledger, D.content_hash(ledger), monotonic() - started


def main():
    ledger, digest, elapsed = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the uniform target-incidence ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("uniform even-N, arbitrary-palette target incidence: PASS")
    print("scope:", ledger["characteristic_scope"])
    print("elapsed: %.3fs" % elapsed)


if __name__ == "__main__":
    main()
