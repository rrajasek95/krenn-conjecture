#!/usr/bin/env python3
"""Separate the order-six source weight from the five non-Euler polars.

The endpoint-recoloured order-six source class has one common total
site-colour shift ``gamma``.  The five marked non-Euler faces have the
diagonal GHZ-stabilizer characters ``chi_v``.  This audit proves that gamma
is independent of their five-dimensional span, so the two constructions
cannot be identified equivariantly without an additional comparison.

The required differences beta_v=chi_v-gamma are nevertheless completely
structured: each is a product of seven local colour-root directions, one at
every site except v.  Their input colours are mixed, hence the all-output
endpoint and every source-derivation corner of the seven-cube are target
zero.  The normalized covariance prism therefore gives the unique
weight-correct target-zero bridge.  It does not prove that its all-source
endpoint is the order-six physical correction; that is the remaining
chain-level comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "6ab3f36073cd08c1ccad97ebd6f8ed3c5f39736be82b6063436c161f176cfeb0",
    "computations/verify_h3_ghz_stabilizer_face_weight_gate.py":
        "4e2ad694f8cf62319b9f60eec7ee7ef002435b8795022ed803a1c886097df526",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
}
EXPECTED_LEDGER_SHA256 = "6fb940267987ecbcdbf4a80c4be70bc2b300feb5fe1b728c233f475ea27b3a18"

SITES = tuple(range(8))
COLOURS = tuple(range(3))
ODD_WORD = (1, 2, 1, 1, 2)  # sites 1,...,5

# Exact common source-module shift from the endpoint-recoloured order-six
# audit, displayed site by site.  It is the character
# (0<-1)_x + (2<-1)_p + (2<-1)_q.
GAMMA = (
    1, -1, 0,
    0, 0, 0,
    0, 0, 0,
    0, 0, 0,
    0, 0, 0,
    0, 0, 0,
    0, -1, 1,
    0, -1, 1,
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def rank(rows: list[list[Q]]) -> int:
    work = [list(map(Q, row)) for row in rows]
    pivot_row = 0
    for column in range(24):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def add(*vectors: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(entries) for entries in zip(*vectors, strict=True))


def scale(value: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(value * entry for entry in vector)


def root(site: int, new: int, old: int) -> tuple[int, ...]:
    vector = [0] * 24
    vector[3 * site + new] = 1
    vector[3 * site + old] = -1
    return tuple(vector)


def polar_character(deleted: int) -> tuple[int, ...]:
    """Bare h_v Y_0 connection character on F_v."""
    vectors = []
    for site in range(1, 6):
        if site == deleted:
            continue
        vectors.append(root(site, 0, ODD_WORD[site - 1]))
    return add(*vectors)


def stabilizer_annihilator(sl: bool) -> list[list[Q]]:
    rows: list[list[Q]] = []
    # The three GHZ colour-product equations.
    for colour in COLOURS:
        row = [Q(0)] * 24
        for site in SITES:
            row[3 * site + colour] = Q(1)
        rows.append(row)
    if sl:
        # Local trace-zero only changes the annihilator, not the ranks below.
        for site in SITES:
            row = [Q(0)] * 24
            for colour in COLOURS:
                row[3 * site + colour] = Q(1)
            rows.append(row)
    return rows


def cube_rank(dimension: int) -> tuple[int, int, int]:
    vertices = 1 << dimension
    columns: list[list[Q]] = []
    for vertex in range(vertices):
        for direction in range(dimension):
            if vertex & (1 << direction):
                continue
            column = [Q(0)] * vertices
            column[vertex] = Q(-1)
            column[vertex | (1 << direction)] = Q(1)
            columns.append(column)
    rows = [[columns[column][row] for column in range(len(columns))]
            for row in range(vertices)]
    # rank() above assumes width 24, so use a local rectangular elimination.
    work = [row[:] for row in rows]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, vertices)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(vertices):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return vertices, len(columns), answer


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    chis = tuple(polar_character(deleted) for deleted in range(1, 6))
    rank_records = {}
    for label, sl in (("GL", False), ("SL", True)):
        constraints = stabilizer_annihilator(sl)
        base_rank = rank(constraints)
        chi_rank = rank(constraints + [list(vector) for vector in chis])
        enlarged = rank(constraints + [list(vector) for vector in chis]
                        + [list(GAMMA)])
        require(chi_rank - base_rank == 5
                and enlarged - base_rank == 6,
                ("stabilizer character ranks changed", label))
        require(all(rank(constraints + [list(chis[index]), list(GAMMA)])
                    - base_rank == 2 for index in range(5)),
                ("one polar collided with gamma", label))
        rank_records[label] = {
            "constraint_rank": base_rank,
            "five_polar_rank": chi_rank - base_rank,
            "five_polars_plus_order6_rank": enlarged - base_rank,
        }

    bridge_records = []
    for deleted, chi in enumerate(chis, 1):
        beta = add(chi, scale(-1, GAMMA))
        roots = [root(0, 1, 0)]
        input_colours = [0]
        for site in range(1, 6):
            if site == deleted:
                continue
            old = ODD_WORD[site - 1]
            roots.append(root(site, 0, old))
            input_colours.append(old)
        roots.extend((root(6, 1, 2), root(7, 1, 2)))
        input_colours.extend((2, 2))
        require(len(roots) == 7 and add(*roots) == beta,
                ("seven-root bridge changed", deleted))
        # A product of local output matrix units acts on a GHZ pure summand
        # only if every old/input colour is the same.  Here they are mixed.
        require(len(set(input_colours)) >= 2,
                ("bridge acquired a diagonal target input", deleted))
        bridge_records.append({
            "face": deleted,
            "beta_by_site": [list(beta[3 * site:3 * site + 3])
                             for site in SITES],
            "acted_sites": [site for site in SITES if site != deleted],
            "input_colours": input_colours,
            "all_output_target_terms": 0,
            "every_corner_target_terms": 0,
        })

    vertices, edges, incidence_rank = cube_rank(7)
    require((vertices, edges, incidence_rank) == (128, 448, 127),
            "seven-cube incidence changed")

    ledger = {
        "theorem": "order-six to non-Euler polar stabilizer bridge",
        "order6_character_gamma_by_site": [
            list(GAMMA[3 * site:3 * site + 3]) for site in SITES
        ],
        "polar_characters": [
            [list(chi[3 * site:3 * site + 3]) for site in SITES]
            for chi in chis
        ],
        "character_ranks": rank_records,
        "direct_equivariant_identification": False,
        "bridge": {
            "type": "seven-site local-GL3 covariance prism",
            "records": bridge_records,
            "cube_vertices_edges_rank": [vertices, edges, incidence_rank],
            "h0_dimension": vertices - incidence_rank,
            "target_zero_reason": (
                "the seven old/input colours contain at least two colours; "
                "all-output lowering kills GHZ, and every other cube corner "
                "contains a source derivation"
            ),
        },
        "proved_reduction": (
            "the physical comparison cannot identify the order-six and "
            "non-Euler classes in one stabilizer weight; it must compose "
            "the order-six class with the five explicit target-zero "
            "seven-site covariance prisms"
        ),
        "remaining_chain_gate": (
            "identify the all-source endpoint of each covariance prism with "
            "the corresponding face of the canonical order-six totalization, "
            "or evaluate their difference as a physical relative class"
        ),
        "scope": (
            "exact character and covariance-cube theorem; no claim that the "
            "all-source endpoint is already the physical correction or that "
            "the normalized H0 class vanishes"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("order6/polar bridge ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 order-six/non-Euler stabilizer covariance bridge: PASS")
    print("polar weights: rank 5; with order-six weight: rank 6")
    print("minimal weight bridge: five target-zero seven-site covariance prisms")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
