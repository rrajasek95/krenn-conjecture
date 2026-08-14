#!/usr/bin/env python3
"""Exact mixed-fibre repair exhaustion for the edge-37 coordinate strata.

The two unresolved local strata in the edge-37 audit differ only in the rank
of the sole nonanchor block M_13 (rank three, or rank two with the exceptional
left kernel).  This checker deliberately gives M_13 *all nine cells*.  It
then exhausts every globally anchor-complete coordinate colouring compatible
with the selected edge-37 normalization and the three pure rows.

Each colouring retains six unique mixed fibres whose matchings avoid edge 13.
Their coefficients are Laurent units in the nonzero anchor scalars, so no
choice, rank, or repair of M_13 can cancel them.  Moreover every alternative
matching for a selected detector asks for an incompatible cell either on an
edge incident to cubic vertex 6 or 7, or on the protected response anchor
03.  Such a repair either destroys the forced anchor placement or makes its
near vector noncoordinate, one of the active-zero strata proved previously.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "654a90328fa9d3d3b5e742f71eddc6e9b708149cab8be2977eef1af7a90343a6"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EDGE37 = load_local(
    "n8_support15_edge37_anchor_rank_strata",
    "verify_n8_support15_edge37_anchor_rank_strata.py",
)
N = EDGE37.N
COLORS = tuple(EDGE37.COLORS)
EDGES = tuple(EDGE37.FULL_EDGES)
NONANCHOR = EDGE37.NONANCHOR_EDGE
CUBIC_VERTICES = frozenset((6, 7))
# Edge 03 is the anchored response block M0=w tensor e_0 in the selected
# edge-37 chart.  Altering its near row makes w noncoordinate, which is the
# other rank-one active-zero route from the preceding audit.
PROTECTED_RESPONSE_EDGE = (0, 3)
MATCHINGS = tuple(
    matching for matching in EDGE37.perfect_matchings(tuple(range(N)))
    if all(tuple(sorted(edge)) in EDGES for edge in matching)
)

# This fixes the selected one-anchor edge-37 chart, including the three
# distinct anchors at cubic vertex 7 and the anchored response block 03.
FIXED_COLOURS = {
    (2, 7): 0,
    (5, 7): 1,
    (3, 7): 2,
    (0, 3): 0,
    (3, 5): 1,
}


def edge_word_cell(edge, word):
    u, v = edge
    return word[u], word[v]


def matching_word(matching, colouring, nonanchor_diagonal=None):
    """Return the unique word selected by a coordinate matching.

    When edge 13 occurs, ``nonanchor_diagonal`` supplies its chosen diagonal
    colour.  This is used only for the pure-row compatibility census.
    """
    word = [None] * N
    for edge in matching:
        edge = tuple(sorted(edge))
        if edge == NONANCHOR:
            require(nonanchor_diagonal is not None,
                    ("nonanchor colour missing", matching))
            colour = nonanchor_diagonal
        else:
            colour = colouring[edge]
        for vertex in edge:
            if word[vertex] is not None and word[vertex] != colour:
                return None
            word[vertex] = colour
    require(all(value is not None for value in word),
            ("matching did not cover every vertex", matching))
    return tuple(word)


def matching_supported(matching, word, colouring, wildcard_nonanchor):
    for edge in matching:
        edge = tuple(sorted(edge))
        if edge == NONANCHOR and wildcard_nonanchor:
            continue
        if edge == NONANCHOR:
            require(False, "non-wildcard nonanchor support is undefined")
        colour = colouring[edge]
        if edge_word_cell(edge, word) != (colour, colour):
            return False
    return True


def anchor_complete(colouring):
    for vertex in range(N):
        incident = {
            colour for edge, colour in colouring.items() if vertex in edge
        }
        if incident != set(COLORS):
            return False
    return True


def pure_supported(colouring, colour):
    word = (colour,) * N
    return any(
        matching_supported(matching, word, colouring, True)
        for matching in MATCHINGS
    )


def enumerate_colourings():
    free_edges = tuple(
        edge for edge in EDGES
        if edge != NONANCHOR and edge not in FIXED_COLOURS
    )
    colourings = []
    for values in product(COLORS, repeat=len(free_edges)):
        colouring = dict(FIXED_COLOURS)
        colouring.update(zip(free_edges, values))
        if not anchor_complete(colouring):
            continue
        if not all(pure_supported(colouring, colour) for colour in COLORS):
            continue
        colourings.append(colouring)
    require(len(colourings) == 6,
            ("coordinate-colouring census changed", len(colourings)))
    return tuple(colourings)


def mixed_detector_ledger(colouring):
    """Find unique fibres even after M_13 is replaced by a full matrix."""
    detectors = []
    for word in product(COLORS, repeat=N):
        if len(set(word)) == 1:
            continue
        supported = tuple(
            matching for matching in MATCHINGS
            if matching_supported(matching, word, colouring, True)
        )
        if len(supported) != 1 or NONANCHOR in supported[0]:
            continue
        matching = supported[0]
        monomial = tuple(sorted(
            "t" + "".join(map(str, edge)) for edge in matching
        ))
        detectors.append({
            "word": "".join(map(str, word)),
            "matching": matching,
            "laurent_unit": monomial,
        })
    require(len(detectors) == 6,
            ("wildcard-nonanchor detector count changed", detectors))
    return tuple(detectors)


def incompatible_routing_cells(matching, word, colouring):
    bad = []
    for edge in matching:
        edge = tuple(sorted(edge))
        if edge == NONANCHOR:
            continue
        colour = colouring[edge]
        cell = edge_word_cell(edge, word)
        protected = CUBIC_VERTICES.intersection(edge)
        if cell != (colour, colour) and (protected or edge == PROTECTED_RESPONSE_EDGE):
            if protected:
                near = next(vertex for vertex in edge if vertex in CUBIC_VERTICES)
                far = next(vertex for vertex in edge if vertex != near)
                near_kind = "cubic"
            else:
                near, far = 3, 0
                near_kind = "anchored response"
            if word[far] != colour:
                route = "destroys fixed far colour/anchor placement"
            else:
                require(word[near] != colour,
                        ("purported protected repair did not change a cell",
                         matching, word, edge))
                route = (f"noncoordinate {near_kind} near vector: "
                         "active rank-one zero")
            bad.append((edge, cell, colour, route))
    return tuple(bad)


def audit_repairs(colouring, detector):
    word = tuple(map(int, detector["word"]))
    selected = detector["matching"]
    require(NONANCHOR not in selected,
            ("detector unexpectedly uses nonanchor", detector))

    repairs = []
    for matching in MATCHINGS:
        if matching == selected:
            continue
        routing_bad = incompatible_routing_cells(matching, word, colouring)
        require(routing_bad,
                ("alternate matching escaped protected-anchor routing",
                 detector, matching))
        repairs.append({
            "matching": matching,
            "protected_incompatible_cells": routing_bad,
        })
    require(len(repairs) == len(MATCHINGS) - 1,
            ("alternate matching count changed", len(repairs)))
    return tuple(repairs)


def colouring_record(colouring):
    detectors = mixed_detector_ledger(colouring)
    selected = detectors[0]
    repairs = audit_repairs(colouring, selected)
    return {
        "colouring": tuple(sorted(colouring.items())),
        "detectors": detectors,
        "selected_detector": selected,
        "all_alternate_repairs_route_at_protected_anchor": True,
        "alternate_matching_count": len(repairs),
        "alternate_repairs": repairs,
    }


def canonical(value):
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    require(len(MATCHINGS) == 10,
            ("support perfect-matching count changed", len(MATCHINGS)))
    records = tuple(colouring_record(colouring)
                    for colouring in enumerate_colourings())
    require(records[0]["selected_detector"] == {
        "word": "00000101",
        "matching": ((0, 3), (1, 6), (2, 4), (5, 7)),
        "laurent_unit": ("t03", "t16", "t24", "t57"),
    }, ("first requested detector changed", records[0]))

    first_word_distribution = tuple(
        record["selected_detector"]["word"] for record in records
    )
    require(first_word_distribution == (
        "00000101", "00101101", "00202101",
        "00010100", "00202101", "00202101",
    ), ("selected detector distribution changed", first_word_distribution))

    ledger = canonical({
        "support_matchings": MATCHINGS,
        "fixed_edge37_colours": FIXED_COLOURS,
        "coordinate_colourings": records,
        "exceptional_nonanchor_ranks_excluded": (
            "rank3",
            "rank2_left_kernel_equals_direct_coordinate",
        ),
        "uniform_identity":
            "H_00000101=t03*t16*t24*t57=0; anchors invertible => 1=0",
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("coordinate repair ledger changed", digest))

    print("N=8 support-15 coordinate repair exhaustion: PASS")
    print("  normalized pure-compatible coordinate colourings: 6")
    print("  robust mixed detectors per colouring: 6")
    print("  nonanchor M13 support allowed: all 9 cells")
    print("  first detector: 00000101 = t03*t16*t24*t57")
    print("  alternate repairs: forced through a protected local anchor edge")
    print("  exceptional ranks excluded uniformly: rank3 and rank2-direct-kernel")


if __name__ == "__main__":
    main()
