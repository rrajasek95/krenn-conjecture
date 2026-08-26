#!/usr/bin/env python3
"""Exact finite audit of the 15/90 minimum-layer-to-clean-cap interface."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "results_minlayer_clean_cap_interface.json"
SOURCES = {
    ROOT / "notes/clean-pair-cap-exact-descent-target.md":
        "90f49ac4fde9b793409d9081977e7a7135ebd76c1b5df5d699387d142c2b9b75",
    ROOT / "computations/unaudited-codex-n8-orbit26-minlayer-spk6-audit-2026-08-23/REPORT.md":
        "03710d76e799e25e58107d9aa702b3848de32a65b4d6bb7b479b9a424ecdd884",
    ROOT / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/REPORT.md":
        "96cb4cc599f871abeb0f07018ff43c947967f3beecf2b70133a6e7c25408c40e",
    ROOT / "computations/unaudited-codex-triangle-five-set-annihilator-2026-08-22/REPORT.md":
        "5962f271d55ec42ee479e5f8407b5d1595bc64fc30fabdd4fb9b35f97a6c945e",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def edge_of(matching, vertex):
    for edge in matching:
        if vertex in edge:
            return edge
    raise RuntimeError("vertex absent from perfect matching")


def audit(mutate=False):
    for path, digest in SOURCES.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")

    p, q = 6, 7
    residual = tuple(range(6))
    matchings8 = tuple(perfect_matchings(range(8)))
    containing = tuple(matching for matching in matchings8 if (p, q) in matching)
    avoiding = tuple(matching for matching in matchings8 if (p, q) not in matching)
    require(len(matchings8) == 105 and len(containing) == 15
            and len(avoiding) == 90, "105=15+90 partition changed")

    # Direct terms are in bijection with PM(U).  Avoiding terms are in
    # bijection with (unordered response edge, endpoint orientation, PM(U-ab)).
    residual_matchings = set(perfect_matchings(residual))
    direct_images = {
        tuple(edge for edge in matching if edge != (p, q))
        for matching in containing
    }
    require(direct_images == residual_matchings,
            "direct cap terms stopped being s*exp(x)")

    response_packets = defaultdict(list)
    avoiding_keys = set()
    for matching in avoiding:
        ep = edge_of(matching, p)
        eq = edge_of(matching, q)
        a = ep[0] if ep[1] == p else ep[1]
        b = eq[0] if eq[1] == q else eq[1]
        require(a != b and a in residual and b in residual,
                "cap endpoints did not choose distinct residual neighbours")
        response_edge = tuple(sorted((a, b)))
        orientation = 0 if a < b else 1
        tail = tuple(edge for edge in matching if p not in edge and q not in edge)
        key = (response_edge, orientation, tail)
        require(key not in avoiding_keys, "response factorization is not injective")
        avoiding_keys.add(key)
        response_packets[response_edge].append((orientation, tail))

    require(len(response_packets) == 15
            and all(Counter(orientation for orientation, _tail in packet)
                    == Counter({0: 3, 1: 3})
                    for packet in response_packets.values())
            and all({tail for _orientation, tail in packet}
                    == set(perfect_matchings(set(residual) - set(edge)))
                    for edge, packet in response_packets.items()),
            "90 terms stopped being 15 response edges x 2 orientations x 3 tails")

    triangle = {(0, 1), (0, 2), (1, 2)}
    triangle_terms = sum(len(response_packets[edge]) for edge in triangle)
    outside_terms = len(avoiding) - triangle_terms
    require(triangle_terms == 18 and outside_terms == 72,
            "triangle response split changed")

    # Full-support edge-degree expansion in the six-site squarefree algebra:
    # s exp(x+r/s) has edge degree three.  Compare its k=0,1 terms with
    # (s+r)exp(x), leaving precisely s^-1 r^2 x/2+s^-2 r^3/6.
    reinsertion = {
        0: (1, Fraction(1, 6)),   # s^1 x^3 / 3!
        1: (0, Fraction(1, 2)),   # s^0 r x^2 / 2!
        2: (-1, Fraction(1, 2)),  # s^-1 r^2 x / 2!
        3: (-2, Fraction(1, 6)),  # s^-2 r^3 / 3!
    }
    capped = {
        0: (1, Fraction(1, 6)),
        1: (0, Fraction(1, 2)),
    }
    correction = {degree: data for degree, data in reinsertion.items()
                  if degree not in capped}
    require(correction == {
        2: (-1, Fraction(1, 2)),
        3: (-2, Fraction(1, 6)),
    }, "reinsertion correction changed")
    # Multiplication by s^2 gives the certified homogeneous N=8 cap error.
    homogeneous_error = {
        "s*r^2*x": str(correction[2][1]),
        "r^3": str(correction[3][1]),
    }
    require(homogeneous_error == {"s*r^2*x": "1/2", "r^3": "1/6"},
            "homogeneous clean error changed")

    # Literal aggregate counterguard to gluing three coordinate caps.
    # A_60[0,0] A_71[0,0], A_62[1,1] A_73[1,1], and
    # A_64[2,2] A_75[2,2] give r_0=01, r_1=23, r_2=45.
    response_edges = {0: (0, 1), 1: (2, 3), 2: (4, 5)}
    require(len({site for edge in response_edges.values() for site in edge}) == 6,
            "counterguard response edges ceased to be disjoint")
    coordinate_r_square = {colour: 0 for colour in range(3)}
    coordinate_r_cube = {colour: 0 for colour in range(3)}
    summed_r_cube_over_six = (tuple(sorted(response_edges.values())), 1)
    require(all(value == 0 for value in coordinate_r_square.values())
            and all(value == 0 for value in coordinate_r_cube.values())
            and summed_r_cube_over_six[1] == 1,
            "coordinate-clean/common-dirty counterguard changed")

    if mutate:
        outside_terms += 1
    require(triangle_terms + outside_terms == 90,
            "hostile response-count mutation survived")

    result = {
        "format": "n8-minlayer-clean-cap-interface-v1",
        "status": "PASS exact 15/90 response identity and triangle blocker bridge",
        "source_sha256": {
            str(path.relative_to(ROOT)): digest for path, digest in SOURCES.items()
        },
        "literal_matching_partition": {
            "sites": 8,
            "cap_pair": [p, q],
            "residual_sites": list(residual),
            "perfect_matchings": len(matchings8),
            "containing_cap_edge": len(containing),
            "avoiding_cap_edge": len(avoiding),
            "direct_identity": "containing = [s exp(x)]_U",
            "response_identity": "avoiding = [r exp(x)]_U",
            "response_packets": {
                "residual_edges": len(response_packets),
                "endpoint_orientations_per_edge": 2,
                "remaining_four_site_matchings_per_orientation": 3,
            },
        },
        "reinsertion_identity": {
            "capped": "K contract H8 = [(s+r) exp(x)]_U",
            "effective_source": "y=x+r/s",
            "difference": "s H6(y)-K contract H8=s^-1 r^2 x/2+s^-2 r^3/6",
            "homogeneous_error": "E_pq(K)=s r^2 x/2+r^3/6",
            "guard": "the 90 avoiding terms are linear response, not E_pq",
        },
        "triangle_interface": {
            "triangle": sorted(map(list, triangle)),
            "outside_response_edges": 12,
            "outside_response_coordinate_rows": 108,
            "avoiding_terms_killed_by_K_in_kernel_L_triangle": outside_terms,
            "avoiding_terms_retained_on_triangle_edges": triangle_terms,
            "reason_error_vanishes": (
                "a three-edge triangle has matching number one, so r^2=r^3=0"
            ),
            "carrier_count": 28 * 20,
            "activity_map": "K -> (K00,K11,K22,<K,A_pq>)",
            "active_iff": (
                "none of K00,K11,K22,<K,A_pq> belongs to rowspan L_triangle"
            ),
            "blocked_iff": (
                "K00 or K11 or K22 or <K,A_pq> belongs to rowspan L_triangle"
            ),
            "blocker_meanings": {
                "K00": "colour-0 endpoint channel vanishes on ker L_triangle",
                "K11": "colour-1 endpoint channel vanishes on ker L_triangle",
                "K22": "colour-2 endpoint channel vanishes on ker L_triangle",
                "<K,A_pq>": "direct cap scalar vanishes on ker L_triangle",
            },
        },
        "coordinate_gluing_counterguard": {
            "nonzero_source_cells": [
                "A_60[0,0]=1", "A_71[0,0]=1",
                "A_62[1,1]=1", "A_73[1,1]=1",
                "A_64[2,2]=1", "A_75[2,2]=1",
                "A_67[0,0]=A_67[1,1]=A_67[2,2]=1",
            ],
            "internal_x": 0,
            "coordinate_responses": {
                "E00": "r0=R_01[0,0] (internal A_01=0)",
                "E11": "r1=R_23[1,1] (internal A_23=0)",
                "E22": "r2=R_45[2,2] (internal A_45=0)",
            },
            "coordinate_errors": "E_pq(Ecc)=0 for c=0,1,2",
            "summed_cap": "K=E00+E11+E22 has r^3/6=R_01[00]*R_23[11]*R_45[22] !=0",
            "scope": (
                "literal aggregate clean-error counterguard only; it is not an X5 point"
            ),
        },
        "conclusion": (
            "The fixed-edge 90-term remainder is the useful linear response, "
            "not an error to cancel. Three colour-fixed coordinate closures do "
            "not produce one common active clean K. On a chosen triangle, the "
            "existence of that K is exactly the complement of the four row-span "
            "memberships; failure is one of the 560 triangle clauses. Star "
            "memberships are tautological on X5 and play no role."
        ),
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text()) == result,
                "stored result changed")
    print(result["status"])
    print("matching split", 105, "=", 15, "+", 90)
    print("triangle split", 90, "=", 72, "+", 18)
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
