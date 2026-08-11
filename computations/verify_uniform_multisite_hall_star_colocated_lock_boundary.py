#!/usr/bin/env python3
"""Reduce the co-located Hall-star debt to a two-neighbour source trap.

After the common-side Hall-star reduction, one off-anchor physical block
P-u may carry both ordered off-diagonal cells x_12 and x_21.  The selected
pure matchings make P-u good at both endpoints.  Applying the exact
target-augmented private-site identity to each cell gives

    x_ij + sum_s Delta^ij_us C^ij_s = 0.

At the shared endpoint P, the three selected pure matchings have only two
distinct anchor neighbours: the unary endpoint S and the common Hall centre
c.  Any active companion outside {S,c} is another off-anchor good pair and
forms the certified distinct-head wedge with P-u.  The exact residual has
both private-site sums supported on {S,c}.

This checker also replays the pinned rational four-response packet with
direct block E_01+E_10.  It proves that the off-diagonal two-cycle and the
response rows alone do not close the trap; that packet fails the unary top.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARD_PATH = "computations/verify_n8_one_bad_fixed_star_flattening_counterguard.py"
PINS = {
    "computations/verify_uniform_multisite_hall_star_source_reduction.py":
        "65ccab6e5830efd9f0dfa084c0d98391e89bad083fa7a41743b2fec7dde15bd5",
    "notes/uniform-multisite-hall-star-source-reduction.md":
        "a0efe068a25423f16d0e24f8d943fd09c4c6911d1dbcdd231d45e66ae37868e0",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    GUARD_PATH:
        "406e80e05c94e8d97aad036e4062b9c560a83e19fc100795bd2d5ccc18f1bd9e",
    "notes/n8-one-bad-fixed-star-flattening-counterguard.md":
        "c29bce71e97405c1df8c323f65cec40667c85c4aa47560ae9f7f4e7ee3864cf1",
}
EXPECTED_LEDGER_SHA256 = "dbece81cbbb7f24ef1360311a3da92db4269b1d2f0936cf2902abadcc6aeb04c"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def audit_private_site_trap():
    # These are the two literal source identities after collecting active
    # products by the companion neighbour of P.  The two named trapped
    # neighbours are S and c; f0,f1 are arbitrary free neighbours.
    names = ("S", "c", "f0", "f1")
    values = {
        "x12": Q(2), "A12_S": Q(-1), "A12_c": Q(-1),
        "x21": Q(3), "A21_S": Q(-3), "A21_c": Q(0),
    }

    def row(direction):
        return values.get(f"x{direction}", Q(0)) + sum(
            values.get(f"A{direction}_{site}", Q(0)) for site in names
        )

    require(row("12") == row("21") == 0,
            "the exact two-neighbour private-site guard changed")
    require(values["x12"] and values["x21"],
            "a reciprocal direct cell vanished")
    require(all(values.get(f"A{direction}_{site}", Q(0)) == 0
                for direction in ("12", "21") for site in ("f0", "f1")),
            "the trapped guard acquired a free companion")
    require(all(any(values.get(f"A{direction}_{site}", Q(0))
                    for site in ("S", "c"))
                for direction in ("12", "21")),
            "a private identity lost every trapped active product")

    # Uniform set-theoretic dichotomy: a nonzero active set either meets the
    # free complement, or it is contained in the two selected neighbours.
    universe = frozenset(("S", "c", "f0", "f1"))
    trapped = frozenset(("S", "c"))
    examples = (
        frozenset(("S",)), frozenset(("c",)),
        frozenset(("S", "c")), frozenset(("f0",)),
        frozenset(("c", "f1")),
    )
    for active in examples:
        require(bool(active - trapped) != bool(active <= trapped),
                "free-or-trapped support dichotomy changed")
        require(active <= universe, "the representative active set escaped")
    return {
        "private_rows": [
            "x12+sum_s Delta12_us*C12_s=0",
            "x21+sum_s Delta21_us*C21_s=0",
        ],
        "selected_anchor_neighbours_at_P": ["S", "c"],
        "free_conclusion": (
            "an active product at s outside {S,c} makes P-u and P-s two "
            "off-anchor good pairs with a nonzero transition minor"
        ),
        "sharp_guard": {
            "x12": "2", "active12": {"S": "-1", "c": "-1"},
            "x21": "3", "active21": {"S": "-3", "c": "0"},
            "free_products": 0,
        },
    }


def audit_uniform_good_pair_rank():
    # At either endpoint of an off-anchor pair, selected matching Q_colour
    # contributes the coordinate label (neighbour_colour, colour).  Check
    # every equality pattern among physical neighbours: colours still make
    # the three labels distinct and hence independent.
    patterns = 0
    for neighbours in itertools.product(range(3), repeat=3):
        labels = tuple((neighbours[colour], colour) for colour in range(3))
        require(len(set(labels)) == 3,
                "a three-colour off-anchor endpoint lost rank")
        patterns += 1
    require(patterns == 27, "the neighbour-equality audit changed")
    return {
        "neighbour_equality_patterns": patterns,
        "rank_at_each_endpoint": 3,
        "co_located_pair_count": 1,
        "warning": (
            "one rank-(3,3) pair is not the two-pair OO overlap; a second "
            "free active companion or a clean-cap identity is still needed"
        ),
    }


def audit_physical_response_guard():
    def cell(left, right, left_colour, right_colour):
        if left > right:
            left, right = right, left
            left_colour, right_colour = right_colour, left_colour
        return (left, right, left_colour, right_colour)

    def perfect_matchings(vertices):
        vertices = tuple(vertices)
        if not vertices:
            yield ()
            return
        first = vertices[0]
        for index, second in enumerate(vertices[1:], 1):
            remainder = vertices[1:index] + vertices[index + 1:]
            for tail in perfect_matchings(remainder):
                yield ((first, second),) + tail

    def hafnian_tensor(q, vertices):
        vertices = tuple(vertices)
        answer = {}
        for word in itertools.product(range(3), repeat=len(vertices)):
            colouring = dict(zip(vertices, word, strict=True))
            coefficient = 0
            for matching in perfect_matchings(vertices):
                term = 1
                for left, right in matching:
                    term *= q.get(cell(left, right, colouring[left],
                                       colouring[right]), 0)
                coefficient += term
            if coefficient:
                answer[word] = coefficient
        return answer

    q = {
        cell(0, 1, 0, 1): 1, cell(0, 1, 1, 0): 1,
        cell(0, 2, 0, 0): 1, cell(0, 3, 1, 1): 1,
        cell(0, 4, 0, 0): 1, cell(0, 5, 1, 1): 1,
        cell(1, 3, 1, 1): 1, cell(1, 4, 0, 0): 1,
        cell(3, 4, 1, 0): -1,
    }
    require(hafnian_tensor(q, (0, 1, 2, 4)) == {(0, 0, 0, 0): 1}
            and hafnian_tensor(q, (0, 1, 3, 5)) == {(1, 1, 1, 1): 1},
            "the two physical pure response rows changed")
    require(hafnian_tensor(q, (0, 1, 2, 5)) == {}
            and hafnian_tensor(q, (0, 1, 3, 4)) == {},
            "a physical crossed response guard changed")
    top = hafnian_tensor(q, tuple(range(6)))
    direct = [[q.get(cell(0, 1, row, column), 0)
               for column in range(3)] for row in range(3)]
    require(direct == [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
            "the physical reciprocal two-cycle changed")
    require(not top,
            "the response guard acquired the unary top")
    return {
        "literal_cells": len(q),
        "complete_response_rows": ["X0", "X1", "0", "0"],
        "direct_binary_block": "E01+E10",
        "direct_rank": 2,
        "unary_top": "0 (required source target is the missing fifth row)",
        "consequence": (
            "the reciprocal block and four response equations alone do not "
            "force line-hitting, a determinant unit, or a clean cap"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "private_site_free_or_trapped": audit_private_site_trap(),
        "off_anchor_rank": audit_uniform_good_pair_rank(),
        "physical_response_only_guard": audit_physical_response_guard(),
        "theorem": (
            "the co-located Hall-star lock is one off-anchor rank-(3,3) "
            "pair.  Each reciprocal cell has a nonempty private-site active "
            "set.  If either set leaves the two selected neighbours {S,c}, "
            "the pinned four-good wedge applies"
        ),
        "exact_residual": (
            "both ordered private-site transition sums are supported on the "
            "same two selected anchor neighbours S and c; the genuine unary "
            "top and remaining full coefficients must straighten this "
            "two-neighbour bidirectional lock"
        ),
        "scope": (
            "source-labelled reduction plus a genuine four-response guard, "
            "not a full one-bad source: the guard has top zero and therefore "
            "does not refute a theorem using q^[h]=X0"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"co-located Hall-star lock ledger changed: {digest}")
    print("uniform co-located Hall-star lock boundary: PASS")
    print("one off-anchor good pair; two exact private-site active sums")
    print("free companion -> four-good; residual -> {S,c} two-neighbour trap")
    print("physical response-only reciprocal block guard retained")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
