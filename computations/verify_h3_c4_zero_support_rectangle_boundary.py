#!/usr/bin/env python3
"""Exact ternary zero-support theorem for the diagonal-return C4.

Let four edge functions on the cycle 01-14-45-05 define

    A(x)=f01(x0,x1) f45(x4,x5),
    B(x)=f05(x0,x5) f14(x1,x4).

If the nonzero supports of A and B agree, the four edge supports are
rectangles S_u x S_v for one nonempty subset S_v at every vertex.  Hence
the common word support is the single Cartesian product of those subsets;
zeros cannot split it into several Hamming components.

The exhaustive ternary audit considers all 511^2 possible nonempty
supports for f01,f45 and finds exactly the 7^4 rectangle cases which also
factor across the other matching.  It then specializes to the target-
coloop base colours (0,0,2,2).
"""

from __future__ import annotations

from collections import Counter, deque
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_zero_face_affine_accessibility_reduction.py":
        "3d346d9d55fc2736de58252d1b9a03d0191faa1cb38fa0fcc62cb4d4863d279f",
    "notes/h3-axis-target-coloop-zero-face-affine-accessibility-reduction.md":
        "0cc8ee2ab2126170677a5b77803e2e3544520b1d9fd74765155d887dd5856aa8",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "e716cd11480815da0fa4c8565c442ec1087feece4ffe1480c2d63f3aa9571381"
)

COLOURS = tuple(range(3))
ALL_PAIRS = tuple(itertools.product(COLOURS, repeat=2))
ALL_WORDS = tuple(itertools.product(COLOURS, repeat=4))
BASE = (0, 0, 2, 2)  # vertex order 0,1,4,5


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def relation(mask):
    return frozenset(pair for index, pair in enumerate(ALL_PAIRS)
                     if mask & (1 << index))


def rectangle(left, right):
    return frozenset(itertools.product(left, right))


def word_support(r01, r45):
    return frozenset(
        (x0, x1, x4, x5)
        for x0, x1 in r01 for x4, x5 in r45
    )


def crossed_projections(words):
    return (
        frozenset((x0, x5) for x0, _x1, _x4, x5 in words),
        frozenset((x1, x4) for _x0, x1, x4, _x5 in words),
    )


def hamming_components(words):
    words = set(words)
    components = []
    while words:
        seed = words.pop()
        component = {seed}
        queue = deque((seed,))
        while queue:
            word = queue.popleft()
            for site in range(4):
                for colour in COLOURS:
                    changed = word[:site] + (colour,) + word[site + 1:]
                    if changed in words:
                        words.remove(changed)
                        component.add(changed)
                        queue.append(changed)
        components.append(frozenset(component))
    return tuple(components)


def exhaustive_relation_audit():
    valid = 0
    size_profiles = Counter()
    common_word_sizes = Counter()
    for mask01 in range(1, 1 << len(ALL_PAIRS)):
        r01 = relation(mask01)
        for mask45 in range(1, 1 << len(ALL_PAIRS)):
            r45 = relation(mask45)
            words = word_support(r01, r45)
            r05, r14 = crossed_projections(words)
            if len(words) != len(r05) * len(r14):
                continue
            if words != frozenset(
                    (x0, x1, x4, x5)
                    for x0, x5 in r05 for x1, x4 in r14):
                continue

            s0 = frozenset(x0 for x0, _x1 in r01)
            s1 = frozenset(x1 for _x0, x1 in r01)
            s4 = frozenset(x4 for x4, _x5 in r45)
            s5 = frozenset(x5 for _x4, x5 in r45)
            require(r01 == rectangle(s0, s1)
                    and r45 == rectangle(s4, s5)
                    and r05 == rectangle(s0, s5)
                    and r14 == rectangle(s1, s4),
                    "a two-bipartition support escaped vertex rectangles")
            require(len(hamming_components(words)) == 1,
                    "a nonempty rectangle support became disconnected")
            valid += 1
            size_profiles[(len(s0), len(s1), len(s4), len(s5))] += 1
            common_word_sizes[len(words)] += 1

    require(valid == 7 ** 4,
            f"the ternary rectangle count changed: {valid}")
    require(len(size_profiles) == 3 ** 4
            and sum(size_profiles.values()) == valid,
            "the rectangle size-profile census changed")
    return {
        "relation_pairs_tested": ((1 << 9) - 1) ** 2,
        "two_bipartition_factorizations": valid,
        "expected_nonempty_vertex_subset_choices": 7 ** 4,
        "size_profiles": len(size_profiles),
        "common_word_size_histogram": dict(sorted(common_word_sizes.items())),
        "all_common_supports_hamming_connected": True,
    }


def base_specialization_audit():
    containing_base = 0
    offanchor_exit = 0
    residual = Counter()
    examples = {}
    for subsets in itertools.product(
            tuple(frozenset(colour for colour in COLOURS
                            if mask & (1 << colour))
                  for mask in range(1, 1 << 3)),
            repeat=4):
        s0, s1, s4, s5 = subsets
        if not all(base_colour in support
                   for base_colour, support in zip(BASE, subsets)):
            continue
        containing_base += 1
        r45 = rectangle(s4, s5)

        # In the canonical target-coloop packet the physical edge 45 is
        # outside K union L union M.  Any enlargement of either endpoint
        # colour set creates an off-diagonal decorated cell on that edge.
        has_offdiagonal_45 = any(left != right for left, right in r45)
        if has_offdiagonal_45:
            offanchor_exit += 1
            continue

        require(s4 == s5 == frozenset((2,)),
                "a non-exiting 45 rectangle acquired another colour")
        active_free_vertices = int(len(s0) > 1) + int(len(s1) > 1)
        kind = {
            0: "singleton_diagonal_C4",
            1: "one_decorated_vertex_star_on_C4",
            2: "two_adjacent_decorated_vertex_stars_on_C4",
        }[active_free_vertices]
        residual[kind] += 1
        examples.setdefault(kind, [sorted(item) for item in subsets])

    require(containing_base == 4 ** 4,
            "the base-containing vertex-subset count changed")
    require(offanchor_exit == 240,
            "the off-anchor edge-45 exit count changed")
    require(residual == Counter({
        "singleton_diagonal_C4": 1,
        "one_decorated_vertex_star_on_C4": 6,
        "two_adjacent_decorated_vertex_stars_on_C4": 9,
    }), f"the no-offanchor rectangle split changed: {residual}")
    return {
        "base_containing_rectangles": containing_base,
        "offanchor_45_offdiagonal_exit": offanchor_exit,
        "no_offanchor_residual": dict(sorted(residual.items())),
        "residual_physical_graph": "01-14-45-05 is C4=K2,2",
        "examples": examples,
    }


def coefficient_guards():
    # A=-B on the smallest nonempty support.  These are the actual four
    # decorated cells of the target-coloop diagonal return.
    cells = {
        "x01_00": 1,
        "x45_22": -1,
        "x05_02": 1,
        "x14_02": 1,
    }
    A = cells["x01_00"] * cells["x45_22"]
    B = cells["x05_02"] * cells["x14_02"]
    require(A == -B != 0,
            "the singleton diagonal-return coefficient guard changed")

    # Vertex-gauge examples exist on every rectangle support, including all
    # zero patterns.  Use nonzero vertex weights and edge scalars whose
    # products differ by -1.
    examples_checked = 0
    for subsets in itertools.product(
            tuple(frozenset(colour for colour in COLOURS
                            if mask & (1 << colour))
                  for mask in range(1, 1 << 3)),
            repeat=4):
        vertex_values = [
            {colour: (site + 2) * (colour + 1)
             for colour in support}
            for site, support in enumerate(subsets)
        ]

        def value(edge, left, right):
            scalars = {"01": 1, "45": -1, "05": 1, "14": 1}
            u, v = {"01": (0, 1), "45": (2, 3),
                    "05": (0, 3), "14": (1, 2)}[edge]
            if left not in subsets[u] or right not in subsets[v]:
                return 0
            return scalars[edge] * vertex_values[u][left] * vertex_values[v][right]

        for x0, x1, x4, x5 in ALL_WORDS:
            left = value("01", x0, x1) * value("45", x4, x5)
            right = value("05", x0, x5) * value("14", x1, x4)
            require(left == -right,
                    "a rectangle vertex-gauge example lost A=-B")
        examples_checked += 1

    require(examples_checked == 7 ** 4,
            "the coefficient rectangle-example count changed")
    return {
        "vertex_gauge_rectangle_examples": examples_checked,
        "singleton_guard": cells,
        "singleton_A": A,
        "singleton_B": B,
        "consequence": (
            "support equality and coefficient flatness alone permit the "
            "fully concentrated diagonal C4; they do not create an "
            "endpoint-hole Hall family or a joint-kernel source move"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "ternary_relation_audit": exhaustive_relation_audit(),
        "target_coloop_base_specialization": base_specialization_audit(),
        "coefficient_guards": coefficient_guards(),
        "support_theorem": (
            "if the two nonzero matching supports agree, all four edge "
            "supports are vertex rectangles and their common word support "
            "is one Hamming-connected Cartesian product; a support mismatch "
            "is the first curvature word"
        ),
        "full_coefficient_equality": (
            "if A=lambda B holds coefficientwise as complete tensors, "
            "support equality is automatic and the rectangle theorem plus "
            "the multiplicative identity gives the usual vertex-gauge "
            "Segre factorization even in the presence of zeros"
        ),
        "physical_boundary": (
            "240 of 256 base-containing rectangle patterns expose an "
            "off-diagonal cell on the off-anchor edge 45. The remaining "
            "16 are supported on the anchor-contained physical C4=K2,2, "
            "but support algebra alone does not identify this residual-q "
            "cycle with the endpoint-hole Hall hypotheses"
        ),
        "minimal_extra_input": (
            "a source-labelled response-hole lift which turns the residual "
            "q-edge C4 into cross-intersecting endpoint hole families, or "
            "an Euler/cofactor identity producing a complete-column kernel"
        ),
        "scope": (
            "the support theorem classifies equality of nonzero supports "
            "and additional-term boundaries; full coefficientwise equality "
            "has no extra zero obstruction and is Segre-flat. Neither result "
            "is a full five-tensor source or a strict-Hall landing"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the frozen C4 zero-support ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("h3 C4 zero-support rectangle boundary: PASS")


if __name__ == "__main__":
    main()
