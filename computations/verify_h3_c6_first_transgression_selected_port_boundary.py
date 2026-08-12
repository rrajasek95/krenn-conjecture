#!/usr/bin/env python3
"""Factor the canonical C6 transgression and audit selected-port visibility.

For the canonical M,N,K of 820c626, one mixed face recombines exactly with
the desired target face.  The other two mixed products contain q03:01.  On
the surviving quotient the obstruction is K_t(M_z+N_z), but the four fixed
one-bad response ports are all blind to z=012111.  The unary z row therefore
introduces thirteen competitors rather than isolating K.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_punctured_face_even_cycle_transgression_boundary.py":
        "d249556172ed778ea265ebe5c8193db31156984bd500fc0397958b16505a939e",
    "notes/h3-punctured-face-even-cycle-transgression-boundary.md":
        "c671636f6cf1edadd6ef9686a31fd056e5749a98db3f16645ee85051d9de491d",
    "computations/verify_h3_four_base_disconnected_unary_bridge.py":
        "d947a03540fedf42d6c5b3eaa37838d7f087659251d3a26fdcd1b8dd64ef092d",
    "notes/h3-four-base-disconnected-unary-bridge.md":
        "65fa33d6a61af853effc66f7edbe5b670d8f600f0c28770bd416fa25cff0ccd8",
}
EXPECTED_LEDGER_SHA256 = "cbcfb53638fd3170967224331fc06c200e8cb36b8d2e1da3702dcd330971ec10"

SITES = tuple(range(6))
M = ((0, 1), (2, 3), (4, 5))
N = ((0, 5), (1, 2), (3, 4))
K = ((0, 3), (1, 2), (4, 5))
T = (1, 1, 1, 1, 1, 1)
X = (0, 1, 1, 1, 1, 1)
Y = (1, 1, 2, 1, 1, 1)
Z = (0, 1, 2, 1, 1, 1)

BASES = (
    M,
    ((0, 1), (2, 4), (3, 5)),
    ((0, 2), (1, 5), (3, 4)),
    N,
)
BASE_UNION = set().union(*(set(base) for base in BASES))

SELECTED_RESPONSE_PORTS = {
    "G11": {"hole": (0, 1), "colours": (1, 1)},
    "G12": {"hole": (0, 4), "colours": (1, 2)},
    "G21": {"hole": (1, 3), "colours": (1, 2)},
    "G22": {"hole": (3, 4), "colours": (2, 2)},
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    if not vertices:
        return [()]
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return answer


MATCHINGS = tuple(perfect_matchings(SITES))


def q_name(edge, word):
    return f"q{edge[0]}{edge[1]}_{word[edge[0]]}{word[edge[1]]}"


def matching_monomial(matching, word):
    return tuple(sorted(q_name(edge, word) for edge in matching))


def multiply(left, right):
    return tuple(sorted(left + right))


def audit_factorization():
    mt = matching_monomial(M, T)
    mx = matching_monomial(M, X)
    my = matching_monomial(M, Y)
    mz = matching_monomial(M, Z)
    nt = matching_monomial(N, T)
    nx = matching_monomial(N, X)
    ny = matching_monomial(N, Y)
    nz = matching_monomial(N, Z)
    kt = matching_monomial(K, T)
    kx = matching_monomial(K, X)
    ky = matching_monomial(K, Y)
    kz = matching_monomial(K, Z)

    # The fourth face is not independent: it is the crosswise
    # recombination of the desired face.
    require(multiply(nx, ky) == multiply(nz, kt),
            "the N/K face recombination changed")

    terms = (
        {"sign": 1, "name": "M_z*K_t", "monomial": multiply(mz, kt)},
        {"sign": -1, "name": "M_y*K_x", "monomial": multiply(my, kx)},
        {"sign": 1, "name": "N_x*K_y", "monomial": multiply(nx, ky)},
        {"sign": -1, "name": "N_t*K_z", "monomial": multiply(nt, kz)},
    )
    require(len({item["monomial"] for item in terms}) == 4,
            "the canonical transgression lost a distinct face")

    q03_01 = "q03_01"
    routed = [item for item in terms
              if item["name"] in ("M_y*K_x", "N_t*K_z")]
    require(all(q03_01 in item["monomial"] for item in routed),
            "a routed mixed face lost q03:01")
    require(q03_01 not in terms[0]["monomial"]
            and q03_01 not in terms[2]["monomial"],
            "q03:01 entered the two recombined faces")

    return {
        "terms": terms,
        "exact_recombination": "N_x*K_y=N_z*K_t",
        "factorization": (
            "D_K=K_t*(M_z+N_z)-M_y*K_x-N_t*K_z"
        ),
        "first_mixed_route": (
            "M_y*K_x and N_t*K_z both contain the same offdiagonal "
            "shortening-chord cell q03:01"
        ),
        "surviving_class": "K_t*(M_z+N_z)",
        "unused_evaluations": {
            "M_t": mt, "M_x": mx, "N_y": ny,
        },
    }


def audit_response_visibility():
    visibility = {}
    for word_name, word in (("t", T), ("x", X), ("y", Y), ("z", Z)):
        records = []
        for row, data in SELECTED_RESPONSE_PORTS.items():
            hole = data["hole"]
            actual = (word[hole[0]], word[hole[1]])
            records.append({
                "row": row,
                "hole": hole,
                "selected_endpoint_colours": data["colours"],
                "word_endpoint_colours": actual,
                "visible": actual == data["colours"],
            })
        visibility[word_name] = records

    require([item["row"] for item in visibility["t"] if item["visible"]]
            == ["G11"], "the pure-face response visibility changed")
    require(not any(item["visible"] for item in visibility["x"]),
            "the x face acquired a selected-port response row")
    require([item["row"] for item in visibility["y"] if item["visible"]]
            == ["G11"], "the y-face response visibility changed")
    require(not any(item["visible"] for item in visibility["z"]),
            "the residual z face acquired a selected-port response row")

    required = {
        item["row"]: item["word_endpoint_colours"]
        for item in visibility["z"]
    }
    require(required == {
        "G11": (0, 1), "G12": (0, 1),
        "G21": (1, 1), "G22": (1, 1),
    }, "the z-face endpoint word-change packet changed")
    return {
        "face_visibility": visibility,
        "z_selected_port_rows": 0,
        "z_required_endpoint_colours": required,
        "first_missing_endpoint_components": (
            "p1@0:0 (for the G11 hole 01) or p2@3:1 "
            "(for the G21 hole 13), with their already selected companions"
        ),
    }


def audit_unary_z_competitors():
    competitors = tuple(matching for matching in MATCHINGS
                        if matching not in (M, N))
    require(len(competitors) == 13,
            "the unary z complement stopped having thirteen bases")
    records = []
    route_counts = Counter()
    for matching in competitors:
        cells = []
        for edge in matching:
            decoration = (Z[edge[0]], Z[edge[1]])
            external_offdiagonal = (
                edge not in BASE_UNION and decoration[0] != decoration[1]
            )
            cells.append({
                "edge": edge,
                "decoration": decoration,
                "outside_old_base_union": edge not in BASE_UNION,
                "offdiagonal": decoration[0] != decoration[1],
                "external_offdiagonal": external_offdiagonal,
            })
        route = ("external_offdiagonal"
                 if any(cell["external_offdiagonal"] for cell in cells)
                 else "anchor_contained")
        route_counts[route] += 1
        records.append({"matching": matching, "cells": cells, "route": route})

    require(route_counts == Counter({"external_offdiagonal": 7,
                                     "anchor_contained": 6}),
            f"the unary-z route split changed: {route_counts}")
    anchor_contained = tuple(record["matching"] for record in records
                             if record["route"] == "anchor_contained")
    require(anchor_contained == (
        ((0, 1), (2, 4), (3, 5)),
        ((0, 2), (1, 3), (4, 5)),
        ((0, 2), (1, 4), (3, 5)),
        ((0, 2), (1, 5), (3, 4)),
        ((0, 5), (1, 3), (2, 4)),
        ((0, 5), (1, 4), (2, 3)),
    ), "the six anchor-contained z competitors changed")
    return {
        "unary_identity": (
            "H_z=M_z+N_z+sum_(Q!=M,N)Q_z=0; hence the surviving "
            "transgression is -K_t*sum_(Q!=M,N)Q_z modulo H_z"
        ),
        "competitor_count": len(competitors),
        "route_counts": dict(sorted(route_counts.items())),
        "anchor_contained_competitors": anchor_contained,
        "records": records,
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    ledger = {
        "canonical_bases": {"M": M, "N": N, "K": K},
        "face_words": {"t": T, "x": X, "y": Y, "z": Z},
        "transgression": audit_factorization(),
        "selected_port_visibility": audit_response_visibility(),
        "unary_z_boundary": audit_unary_z_competitors(),
        "theorem": (
            "two mixed faces of the canonical C6 transgression share the "
            "offdiagonal shortening-chord cell q03:01; the other mixed "
            "face recombines with the target face, leaving K_t(M_z+N_z). "
            "The complete unary z row attaches this to thirteen bases, "
            "while all four selected response ports are blind to z"
        ),
        "scope": (
            "exact fixed-port first-transgression boundary in the c44d784 "
            "minimum packet.  It is not a full-source counterexample: a "
            "word-changed endpoint component or another complete-column "
            "route can supply the missing z response coefficient"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"C6 first-transgression ledger changed: {digest}")
    print("h3 canonical C6 first-transgression selected-port boundary: PASS")
    print("factorization: Kt*(Mz+Nz) minus two q03:01 faces")
    print("z face: 0 selected response rows; unary competitors 7 routed / 6 anchor")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
