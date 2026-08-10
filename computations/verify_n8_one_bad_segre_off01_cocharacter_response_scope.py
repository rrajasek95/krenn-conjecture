#!/usr/bin/env python3
"""Audit the off-01 Segre cocharacter and its response-scaling scope.

The 24-cell quotient class from the anchor-initial checker is an honest
exposed face for the residual quadratic/top equation.  This file verifies
the exact common exposing cocharacter for all twelve off-01 pure anchors.

It also records the load-bearing limitation: every strict exposing
cocharacter kills all two-edge colour-1 and colour-2 cofactors in its affine
limit.  Consequently that limit does not retain either diagonal response
anchor of the common-q one-bad packet.  Restoring those anchors by endpoint
weights introduces negative valuations and does not restrict the response
rows to the 24-cell affine face.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANCHOR = ROOT / "computations/verify_n8_one_bad_segre_cube_anchor_initial_cover.py"
ANCHOR_SHA256 = "a0a2f5600029f6c79ce931171b53fff772f2fef7e0c0bb4b971ba56c0fd44ef0"
EXPECTED_LEDGER_SHA256 = (
    "9f7b5ba5233b4cf5e73c215fcf483633af4a31a1453732310fc4f1bcb39fa349"
)

FREE_COORDINATES = (
    (1, 1), (1, 2), (2, 1), (3, 2), (4, 1), (5, 2),
)
COMMON_COCHARACTER = (
    (0, 0, 0),
    (0, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 0, 1),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_anchor():
    actual = sha256(ANCHOR.read_bytes()).hexdigest()
    require(actual == ANCHOR_SHA256, f"anchor dependency changed: {actual}")
    spec = spec_from_file_location("anchor", ANCHOR)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    anchor = load_anchor()
    four = anchor.load_dependency()
    one = four.load_dependency()
    first = one.load_dependency()
    diagonal = first.load_dependency()
    pure = diagonal.load_dependency()
    source = pure.load_dependency()
    support_h, _weights_h = pure.build_top_null_H(source)

    face = frozenset(anchor.parse_cell(label)
                     for label in anchor.LARGE_ZERO_CLASS)
    outside = frozenset(
        (edge, colours)
        for edge in anchor.EDGES
        for colours in itertools.product(anchor.COLOURS, repeat=2)
        if colours[0] != colours[1]
        and (edge, colours) not in support_h
    )
    remaining = outside - face
    free_index_tuple = tuple(anchor.COORDINATE_INDEX[coordinate]
                             for coordinate in FREE_COORDINATES)
    free_indices = frozenset(free_index_tuple)

    # The face equalities have rank twelve and literally avoid the six free
    # coordinates.  Their common annihilator is therefore exactly the span
    # of those six coordinate vectors, for every off-01 anchor matching.
    off_01_matchings = []
    for matching in anchor.MATCHINGS:
        if (0, 1) in matching:
            continue
        rows = ([anchor.incidence(cell) for cell in sorted(support_h)]
                + [anchor.incidence((edge, (0, 0))) for edge in matching]
                + [anchor.incidence(cell) for cell in sorted(face)])
        require(anchor.matrix_rank(rows) == 12,
                f"off-01 equality rank changed: {matching}")
        require(all(all(not row[index] for index in free_indices)
                    for row in rows),
                f"an equality uses a purported free coordinate: {matching}")
        off_01_matchings.append(
            "|".join(f"{left}{right}" for left, right in matching)
        )
    require(len(off_01_matchings) == 12,
            "the off-01 matching count changed")

    # Each free coordinate occurs by itself in at least one remaining mixed
    # cell.  Strict positivity of all 52 remaining cells therefore forces
    # all six free parameters to be strictly positive.
    positivity_witnesses = {}
    for free_position, coordinate in enumerate(FREE_COORDINATES):
        unit = tuple(1 if position == free_position else 0
                     for position in range(len(FREE_COORDINATES)))
        witnesses = sorted(anchor.cell_label(cell) for cell in remaining
                           if tuple(anchor.incidence(cell)[index]
                                    for index in free_index_tuple) == unit)
        require(witnesses,
                f"no strict-positivity witness for {coordinate}")
        positivity_witnesses[f"{coordinate[0]}:{coordinate[1]}"] = witnesses[0]

    require(all(anchor.weight(cell, COMMON_COCHARACTER) == 0
                for cell in support_h), "the common cocharacter moved H")
    require(all(anchor.weight(cell, COMMON_COCHARACTER) == 0
                for cell in face), "the common cocharacter moved the face")
    remaining_histogram = Counter(
        anchor.weight(cell, COMMON_COCHARACTER) for cell in remaining
    )
    require(remaining_histogram == Counter({1: 44, 2: 8}),
            f"remaining mixed weights changed: {remaining_histogram}")
    for matching in anchor.MATCHINGS:
        if (0, 1) not in matching:
            require(all(anchor.weight((edge, (0, 0)), COMMON_COCHARACTER) == 0
                        for edge in matching),
                    f"an off-01 pure anchor moved: {matching}")

    diagonal_zero_edges = {}
    for colour in anchor.COLOURS:
        zero_edges = tuple(edge for edge in anchor.EDGES
                           if anchor.weight((edge, (colour, colour)),
                                            COMMON_COCHARACTER) == 0)
        diagonal_zero_edges[str(colour)] = [
            f"{left}{right}" for left, right in zero_edges
        ]
        if colour in (1, 2):
            require(not any(set(left).isdisjoint(right)
                            for left, right in itertools.combinations(
                                zero_edges, 2)),
                    f"colour {colour} acquired a zero-weight two-matching")
    require(diagonal_zero_edges["1"] == ["03", "05", "35"],
            "the zero-weight 11 graph changed")
    require(diagonal_zero_edges["2"] == ["02", "04", "24"],
            "the zero-weight 22 graph changed")

    target_weights = tuple(
        sum(COMMON_COCHARACTER[site][colour] for site in anchor.SITES)
        for colour in anchor.COLOURS
    )
    require(target_weights == (0, 3, 3),
            f"the pure target weights changed: {target_weights}")

    # A diagonal response monomial deletes two star sites and matches the
    # other four sites by two q-edges.  At least one of the three positive
    # colour-c sites remains, so its q cofactor has positive weight.  This
    # proves the statement for every strict separator, not only the integral
    # point above: the six free parameters are all positive.
    positive_sites = {
        colour: frozenset(site for site in anchor.SITES
                          if (site, colour) in FREE_COORDINATES)
        for colour in (1, 2)
    }
    for colour, sites in positive_sites.items():
        require(len(sites) == 3, f"colour {colour} positive sites changed")
        for p_site, s_site in itertools.permutations(anchor.SITES, 2):
            residual = frozenset(anchor.SITES) - {p_site, s_site}
            require(residual & sites,
                    f"a colour-{colour} response cofactor lost all positive sites")

    ledger = {
        "dependency": {
            "path": str(ANCHOR.relative_to(ROOT)),
            "sha256": ANCHOR_SHA256,
        },
        "off_01_anchor_matchings": off_01_matchings,
        "face_equalities_rank": 12,
        "annihilator_coordinates": [f"u{site}{colour}"
                                     for site, colour in FREE_COORDINATES],
        "strict_positivity_witnesses": positivity_witnesses,
        "common_integral_cocharacter": COMMON_COCHARACTER,
        "remaining_mixed_weight_histogram": dict(remaining_histogram),
        "zero_diagonal_edges": diagonal_zero_edges,
        "pure_target_weights": target_weights,
        "response_obstruction": (
            "every strict separator leaves three zero-weight vertices in "
            "each of colours 1 and 2, hence no zero-weight two-edge q "
            "cofactor; the affine limit loses both diagonal responses"
        ),
        "scope": (
            "the cocharacter exposes the 24-cell face for q and q^[3]=X0; "
            "it does not produce a full one-bad point on that face. "
            "Endpoint shifts which restore X1/X2 require negative source "
            "valuations and retain the higher-weight q terms in each "
            "homogeneous response row."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"off-01 response-scope ledger changed: {digest}")

    print("N=8 off-01 Segre cocharacter response-scope audit: PASS")
    print("12 anchors; equality rank 12; strict cone has six positive axes")
    print("remaining mixed weights: 44 at 1, 8 at 2")
    print("zero 11 graph: 03,05,35; zero 22 graph: 02,04,24")
    print("affine limit loses both diagonal response anchors")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
