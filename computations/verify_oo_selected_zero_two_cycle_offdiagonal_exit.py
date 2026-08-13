#!/usr/bin/env python3
"""Eliminate the diagonal 2+2 switch from a selected OO two-cycle.

The equal-partition reduction leaves 90 diagonal four-site spectator
decorations.  Tensor each with every four-site alternating core word and
ordered pair of distinct core matchings.  Two distinct core matchings are
both diagonal exactly when the core word is monochromatic.  Otherwise the
core relation contains a nonzero off-diagonal cell and enters the pinned
bidirectional fan / physical Cartan endpoint-holonomy theorem.

Hence a literal zero-Fitting two-cycle containing the selected off-diagonal
OO matching class has no diagonal 2+2 survivor.  Entirely diagonal switches
exist, but their core word is monochromatic and they cannot be the selected
off-diagonal class.  Higher SCC entry remains outside this theorem.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLOURS = tuple(range(3))
PINS = {
    "computations/verify_oo_zero_holonomy_equal_partition_reduction.py":
        "a24235514c568c3743b4fc3a6f7dab760c4f0cf87b5bc04f5804943b5accc56a",
    "notes/oo-zero-holonomy-equal-partition-reduction.md":
        "2316b6731f8e26fa721f66d1c0517431f31315f71f8467df2936a4d06478375f",
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
    "notes/uniform-bidirectional-private-site-fan-rank-boundary.md":
        "7d0f04d22fe11d1ba797a29507fd43915dc98e9d89bdc4085f1c8561deaa1402",
    "computations/verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py":
        "4453dad26b5d13767fc206e9a8dc98af5428ac6d00cfc9444ac6b4253c834f7c",
    "notes/h3-physical-cartan-closes-residual-q-ks-hypothesis.md":
        "7f144e607e2fbfa4031ed8b282d7ae6f1da59ce0e7e696b5ae2b8840bcc12236",
}
EXPECTED_LEDGER_SHA256 = (
    "792bee9611258262b25343eb97b08b4a06feb049f4801f2610c199436c684b33"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices
                     if site not in (first, second))
        for tail in perfect_matchings(rest):
            output.append((tuple(sorted((first, second))),) + tail)
    return tuple(output)


def diagonal(word, matching):
    return all(word[left] == word[right] for left, right in matching)


def diagonal_spectator_cases():
    words = tuple(product(COLOURS, repeat=4))
    matchings = perfect_matchings(range(4))
    cases = []
    subtype = Counter()
    for left in words:
        for right in words:
            if left == right or Counter(left) != Counter(right):
                continue
            for G in matchings:
                for H in matchings:
                    if not (diagonal(left, G) and diagonal(right, H)):
                        continue
                    kind = ("same_skeleton_colour_swap" if G == H
                            else "physical_C4_switch")
                    subtype[kind] += 1
                    cases.append((left, right, G, H, kind))
    require(len(cases) == 90 and subtype == {
        "same_skeleton_colour_swap": 18,
        "physical_C4_switch": 72,
    }, ("diagonal spectator inventory changed", len(cases), subtype))
    return tuple(cases), subtype


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    spectators, spectator_types = diagonal_spectator_cases()
    core_matchings = perfect_matchings(range(4))
    core_rows = tuple((word, U, V)
                      for word in product(COLOURS, repeat=4)
                      for U in core_matchings for V in core_matchings
                      if U != V)
    require(len(core_rows) == 3 ** 4 * 6,
            "four-site core row inventory changed")

    core_types = Counter()
    examples = {}
    for word, U, V in core_rows:
        if diagonal(word, U) and diagonal(word, V):
            branch = "entire_core_diagonal"
            require(len(set(word)) == 1,
                    "two distinct diagonal core matchings became non-monochrome")
        else:
            branch = "core_contains_offdiagonal_cell"
        core_types[branch] += 1
        examples.setdefault(branch, {
            "word": list(word),
            "U": [list(edge) for edge in U],
            "V": [list(edge) for edge in V],
        })
    require(core_types == {
        "entire_core_diagonal": 18,
        "core_contains_offdiagonal_cell": 468,
    }, ("core diagonal/offdiagonal split changed", core_types))

    combined = Counter()
    for _left, _right, _G, _H, spectator_kind in spectators:
        for word, U, V in core_rows:
            core_kind = ("entirely_diagonal_unselected_component"
                         if diagonal(word, U) and diagonal(word, V)
                         else "offdiagonal_core_fan_route")
            combined[(spectator_kind, core_kind)] += 1
    require(sum(combined.values()) == 90 * 486,
            "combined selected-two-cycle census changed")
    require(sum(value for (spectator_kind, core_kind), value in combined.items()
                if core_kind == "offdiagonal_core_fan_route") == 42120,
            "offdiagonal core route count changed")
    require(sum(value for (spectator_kind, core_kind), value in combined.items()
                if core_kind == "entirely_diagonal_unselected_component") == 1620,
            "entirely diagonal count changed")

    return {
        "theorem": "selected zero-Fitting two-cycle has no diagonal 2+2 survivor",
        "diagonal_spectator_cases": {
            "total": len(spectators),
            "subtypes": dict(sorted(spectator_types.items())),
        },
        "ordered_four_site_core_rows": len(core_rows),
        "core_split": dict(sorted(core_types.items())),
        "combined_split": [
            {"spectator_type": spectator_kind,
             "core_type": core_kind,
             "count": value}
            for (spectator_kind, core_kind), value in sorted(combined.items())
        ],
        "combined_totals": {
            "offdiagonal_core_fan_route": 42120,
            "entirely_diagonal_unselected_component": 1620,
        },
        "selected_active_consequence": (
            "the selected OO matching class contains a fixed nonzero off-"
            "diagonal direct cell.  In the all-diagonal spectator branch it "
            "must therefore lie in U or V, selecting one of the 42120 fan "
            "routes.  The 1620 remaining rectangles have monochromatic core "
            "word and only diagonal core cells, so they cannot be that "
            "selected class"
        ),
        "fan_landing": (
            "the pinned private-site theorem gives an off-anchor distinct-"
            "head four-good fan or the anchor-contained five-lock; physical "
            "Cartan descent now closes the latter endpoint-holonomy/terminal "
            "alternative in the canonical h=3 packet"
        ),
        "scope": (
            "literal selected zero-Fitting two-row block only.  A general "
            "higher-row SCC can contain diagonal two-cycles away from its "
            "selected vertex, and proving a source-valid path from the "
            "selected vertex to every surviving charge remains the global "
            "source-exhaustivity theorem"
        ),
        "examples": examples,
    }


def main():
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("OO selected zero two-cycle offdiagonal exit: PASS")
    print("diagonal spectator x offdiagonal core:", 42120)
    print("entirely diagonal, hence not selected OO class:", 1620)
    print("remaining global gate: higher-SCC source exhaustivity")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
