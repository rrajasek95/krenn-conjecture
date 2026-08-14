#!/usr/bin/env python3
"""Smallest source-labelled wandering guard for primitive-C4 completion.

At order six, build three normalized constant-colour coefficients and one
primitive diagonal C4 repair.  The repaired top word and both mandatory
one-edge boundary words each have exactly two live matching occurrences and
cancel.  Their unique mate flips retain respectively the tails 01, 23, 45,
so the C4 windows are 2345, 0145, 0123.  Their intersection is empty: total
first-boundary mating does not place the component in a common endpoint-star
four-port space.

The packet is not a ternary GHZ source; six further mixed singleton debts
are displayed.  It is a counterguard to automatic physical placement from
normalization, primitive boundary identities, and unique same-character
mates alone.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_signed_matching_holonomy_boundary_counterguard.py":
        "12bb763f3ca2f2dde30f6a8f932fd6d8b9fa3c970e1e3aab2f46592bcde93547",
    "notes/uniform-signed-matching-holonomy-boundary-counterguard.md":
        "afa8c41df024b2c6b9b7b7088346880059ca54cdb060216bd9009ca5066aae37",
    "computations/verify_uniform_boundary_complete_flat_even_component_theorem.py":
        "08db6dd78869d5d236d43fe8ae91e1e944d2b60d16a7f5f7a684f766a4187530",
    "notes/uniform-boundary-complete-flat-even-component-theorem.md":
        "b223d7d65852fcd086bff58673c6a3fb6811003b74bf742dc34ba96c0049fc31",
    "computations/verify_uniform_one_bad_square_zero_clean_cap.py":
        "a943fffdc3ce86aa5506e6774ec3a6a8ff10c70491225417152a1298e2754883",
    "notes/uniform-one-bad-square-zero-clean-cap.md":
        "2af5f90040152079c094e03b0b1bb794761a07d2418182586ab06848ee820c2e",
}
EXPECTED_DIGEST = "885b7de1169942f2ec316e06ebcc2291bd85048a02aed8d02c6c492a31647b7e"

ZERO = (0, 0)
ONE = (1, 0)
I = (0, 1)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def gadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def gmul(left, right):
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gsum(values):
    answer = ZERO
    for value in values:
        answer = gadd(answer, value)
    return answer


def gneg(value):
    return -value[0], -value[1]


def gtext(value):
    names = {
        ZERO: "0", ONE: "1", (-1, 0): "-1", I: "i", (0, -1): "-i"
    }
    return names.get(value, f"({value[0]}+{value[1]}i)")


def edge(left, right):
    return min(left, right), max(left, right)


def cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return left, right, left_colour, right_colour


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


def add_cell(cells, label, value):
    require(label not in cells, f"duplicate decorated cell: {label}")
    cells[label] = value


def build_packet():
    cells = {}
    anchors = {
        0: ((0, 1), (2, 3), (4, 5)),
        1: ((0, 2), (1, 4), (3, 5)),
        2: ((0, 3), (1, 5), (2, 4)),
    }
    # The selected colour-zero anchor occurrence has weight -1; its two
    # boundary mates contribute +1 each, so the complete pure coefficient is
    # normalized to +1.  The other two pure anchors retain unit weights.
    zero_weights = {(0, 1): ONE, (2, 3): (-1, 0), (4, 5): ONE}
    for pair in anchors[0]:
        add_cell(cells, cell(*pair, 0, 0), zero_weights[pair])
    for colour in (1, 2):
        for pair in anchors[colour]:
            add_cell(cells, cell(*pair, colour, colour), ONE)

    # Original diagonal repair: product i*i=-1 on matching M0 at 002121.
    add_cell(cells, cell(2, 3, 2, 1), I)
    add_cell(cells, cell(4, 5, 2, 1), I)

    # Unique mate of L=002100.  It retains edge 23 and flips the C4 0145.
    add_cell(cells, cell(0, 4, 0, 0), (-1, 0))
    add_cell(cells, cell(1, 5, 0, 0), ONE)

    # Unique mate of R=000021.  It retains edge 45 and flips the C4 0123.
    add_cell(cells, cell(0, 2, 0, 0), (-1, 0))
    add_cell(cells, cell(1, 3, 0, 0), (-1, 0))
    return cells, anchors


def matching_term(cells, matching, word):
    value = ONE
    labels = []
    for left, right in matching:
        label = cell(left, right, word[left], word[right])
        factor = cells.get(label, ZERO)
        if factor == ZERO:
            return ZERO, ()
        value = gmul(value, factor)
        labels.append(label)
    return value, tuple(labels)


def live_fibres(cells):
    matchings = tuple(perfect_matchings(range(6)))
    answer = {}
    for word in itertools.product(range(3), repeat=6):
        terms = []
        for matching in matchings:
            value, labels = matching_term(cells, matching, word)
            if value != ZERO:
                terms.append((matching, value, labels))
        if terms:
            answer[word] = tuple(terms)
    return answer


def c4_data(left, right):
    common = set(left) & set(right)
    symmetric = set(left) ^ set(right)
    require(len(common) == 1 and len(symmetric) == 4,
            f"the alleged primitive pair is not tail+C4: {left}, {right}")
    tail = next(iter(common))
    window = tuple(sorted(set().union(*symmetric)))
    require(len(window) == 4,
            f"the symmetric difference lost its four-site window: {window}")
    return tail, window


def audit_exact_packet():
    cells, anchors = build_packet()
    fibres = live_fibres(cells)
    compact = {
        "".join(map(str, word)): tuple(term[1] for term in terms)
        for word, terms in fibres.items()
    }
    expected = {
        "000000": ((-1, 0), ONE, ONE),
        "000021": ((0, -1), I),
        "002100": (I, (0, -1)),
        "002121": ((-1, 0), ONE),
        "010111": ((-1, 0),),
        "020002": (ONE,),
        "022102": ((0, -1),),
        "101000": ((-1, 0),),
        "101021": ((0, -1),),
        "111111": (ONE,),
        "202220": (ONE,),
        "222222": (ONE,),
    }
    require(compact == expected,
            f"the wandering source packet changed: {compact}")
    require(all(gsum(compact[word]) == ONE
                for word in ("000000", "111111", "222222")),
            "a constant-colour coefficient lost normalization")
    cancelled = ("002121", "002100", "000021")
    require(all(len(compact[word]) == 2 and gsum(compact[word]) == ZERO
                for word in cancelled),
            "a mandatory primitive/boundary fibre stopped cancelling uniquely")

    # The selected M0 occurrence is the first term in each cancellation
    # fibre.  Extract its unique mate and the physical flip window.
    records = []
    expected_tails = ((0, 1), (2, 3), (4, 5))
    expected_windows = ((2, 3, 4, 5), (0, 1, 4, 5), (0, 1, 2, 3))
    for word_text, expected_tail, expected_window in zip(
            cancelled, expected_tails, expected_windows, strict=True):
        word = tuple(map(int, word_text))
        terms = fibres[word]
        selected = next(term for term in terms if term[0] == anchors[0])
        mate = next(term for term in terms if term[0] != anchors[0])
        require(mate[1] == gneg(selected[1]),
                f"the mate character changed on {word_text}")
        tail, window = c4_data(selected[0], mate[0])
        require(tail == expected_tail and window == expected_window,
                f"the source-label wandering changed on {word_text}")
        records.append({
            "word": word_text,
            "selected_matching": [list(pair) for pair in selected[0]],
            "selected_weight": gtext(selected[1]),
            "unique_mate_matching": [list(pair) for pair in mate[0]],
            "mate_weight": gtext(mate[1]),
            "retained_tail": list(tail),
            "C4_window": list(window),
        })

    windows = tuple(set(record["C4_window"]) for record in records)
    common_sites = set.intersection(*windows)
    require(not common_sites,
            f"the wandering windows acquired a common endpoint: {common_sites}")
    require({tuple(record["retained_tail"]) for record in records}
            == {tuple(pair) for pair in anchors[0]},
            "the mates stopped rotating through all three anchor tails")

    # The exact primitive boundary identity at the selected occurrence.
    base = compact["000000"][0]
    diagonal = compact["002121"][0]
    forced = compact["002121"][1]
    left = compact["002100"][0]
    right = compact["000021"][0]
    require(gmul(left, right) == gmul(base, diagonal)
            == gneg(gmul(base, forced)) == ONE,
            "LR=BD=-BF changed in the wandering packet")

    singleton_debts = {
        word: gtext(values[0]) for word, values in compact.items()
        if len(set(map(int, word))) > 1 and len(values) == 1
    }
    require(singleton_debts == {
        "010111": "-1", "020002": "1", "022102": "-i",
        "101000": "-1", "101021": "-i", "202220": "1",
    }, f"the wandering debt ledger changed: {singleton_debts}")
    return {
        "decorated_cells": len(cells),
        "nonzero_word_fibres": len(fibres),
        "constant_colour_coefficients": {
            word: gtext(gsum(compact[word]))
            for word in ("000000", "111111", "222222")
        },
        "primitive_and_boundary_rows": records,
        "retained_tail_cycle": ["01", "23", "45"],
        "C4_windows": [record["C4_window"] for record in records],
        "common_window_sites": sorted(common_sites),
        "common_ordered_endpoint_pair": False,
        "boundary_identity": "L*R=B*D=-B*F=1",
        "mixed_singleton_debts": singleton_debts,
        "is_complete_ternary_source": False,
    }


def audit_minimal_order_and_compatibility():
    # A perfect-matching coefficient exists only in even order.  On four
    # sites every primitive C4 uses the complete vertex set, so every family
    # of C4 windows has a common endpoint pair.  Six is the first order at
    # which the total intersection can have fewer than two sites.
    k4 = tuple(perfect_matchings(range(4)))
    require(len(k4) == 3,
            "the K4 matching count changed")
    k4_windows = []
    for left, right in itertools.combinations(k4, 2):
        _tail = set(left) & set(right)
        symmetric = set(left) ^ set(right)
        require(not _tail and len(symmetric) == 4,
                "two K4 matchings stopped differing on the whole C4")
        k4_windows.append(set().union(*symmetric))
    require(set.intersection(*k4_windows) == set(range(4)),
            "K4 unexpectedly admitted physical window wandering")

    # A sufficient placement hypothesis is deliberately literal.  If one
    # ordered endpoint pair p,s belongs to every C4 window, all mate rows
    # retain one common residual tail, and every varying cell is incident to
    # p or s, the component lies in the product of the p- and s-star port
    # spaces.  One-site support of each of p1,p2,s1,s2 then gives the pinned
    # square-zero cap landing.
    return {
        "orders_below_six": [2, 4],
        "K4_primitive_windows": [sorted(window) for window in k4_windows],
        "K4_common_window_sites": [0, 1, 2, 3],
        "first_possible_wandering_order": 6,
        "sufficient_extra_compatibility": {
            "fixed_ordered_endpoint_pair": "the same p,s lie in every C4 window",
            "cartesian_port_labels": (
                "path-independent labels p1,p2 on the p-star and s1,s2 on "
                "the s-star; every varying occurrence is one p_i*s_j product"
            ),
            "cofactor_transport": (
                "after deleting the chosen ports, all tails are coefficients "
                "of one fixed residual q-family and coincide whenever the "
                "same residual complement recurs"
            ),
            "one_site_ports": "each of p1,p2,s1,s2 is supported at at most one residual site",
            "response_typing": (
                "the retained complete rows are q^[h]=X0 and "
                "p_i*s_j*q^[h-1]=delta_ij*X_i"
            ),
        },
        "consequence": (
            "fixed endpoints plus Cartesian labels and cofactor transport "
            "give a common physical bistar port space; one-site support "
            "makes its four port squares zero, and response typing lets the "
            "pinned normalized one-bad cap land actively and cleanly"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "exact_wandering_packet": audit_exact_packet(),
        "minimality_and_repair_hypothesis": audit_minimal_order_and_compatibility(),
        "verdict": (
            "unique same-character mates for the primitive top and both "
            "mandatory L/R boundary fibres do not force common same-star "
            "placement.  Their retained matching tail can rotate, moving "
            "the physical C4 window through disjoint endpoint pairs"
        ),
        "scope": (
            "exact Gaussian-integer decorated K6 coefficient packet with "
            "three normalized pure coefficients; not a ternary GHZ source, "
            "because six explicit mixed singleton debts remain"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"primitive-C4 wandering ledger changed: {digest}")
    print("uniform primitive-C4 source-label wandering counterguard: PASS")
    print("three normalized constant-colour coefficients: 1,1,1")
    print("unique cancelling rows: top D/F and both mandatory L/R fibres")
    print("retained tails: 01 -> 23 -> 45")
    print("C4 windows: 2345, 0145, 0123; common sites: none")
    print("remaining mixed singleton debts: 6")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
