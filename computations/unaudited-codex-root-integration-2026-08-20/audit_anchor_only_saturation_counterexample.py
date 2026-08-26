#!/usr/bin/env python3
"""Audit the universal counterexample to anchor-only chart saturation.

For every triple of pure perfect matchings choose a physical edge outside
their union.  Put z=-6 on that edge and z=1 elsewhere, and set every
endpoint-colour cell on uv equal to z_uv.  Every coloured Hafnian is then
the same scalar 90+15*(-6)=0, while all twelve selected anchor cells are 1.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_anchor_only_saturation_counterexample.json"
VERTICES = tuple(range(8))
EDGES = tuple(combinations(VERTICES, 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted(((u, v),) + tail)))
    return tuple(answer)


def main():
    matchings = perfect_matchings(VERTICES)
    assert len(matchings) == 105 and len(set(matchings)) == 105
    contain_counts = {
        edge: sum(edge in matching for matching in matchings) for edge in EDGES
    }
    assert set(contain_counts.values()) == {15}
    avoid_counts = {edge: 105 - count for edge, count in contain_counts.items()}
    assert set(avoid_counts.values()) == {90}

    maximum_union = 0
    triples_checked = 0
    chosen_edge_histogram = {edge: 0 for edge in EDGES}
    edge_set = set(EDGES)
    for first in matchings:
        for second in matchings:
            for third in matchings:
                union = set(first) | set(second) | set(third)
                maximum_union = max(maximum_union, len(union))
                outside = min(edge_set - union)
                chosen_edge_histogram[outside] += 1
                triples_checked += 1
    assert triples_checked == 105**3
    assert maximum_union <= 12 < len(EDGES)

    exceptional_weight = -6
    hafnian = 90 + 15 * exceptional_weight
    assert hafnian == 0
    result = {
        "status": "UNAUDITED exact universal anchor-only saturation counterexample",
        "vertices": len(VERTICES),
        "physical_edges": len(EDGES),
        "perfect_matchings": len(matchings),
        "pure_matching_triples_checked": triples_checked,
        "maximum_selected_edge_union": maximum_union,
        "perfect_matchings_containing_exceptional_edge": 15,
        "perfect_matchings_avoiding_exceptional_edge": 90,
        "exceptional_edge_weight": exceptional_weight,
        "common_coloured_hafnian": hafnian,
        "construction": (
            "For each chart choose an edge e outside the three selected pure "
            "matchings. Set x_uv[a,b]=z_uv for all endpoint colours, with "
            "z_e=-6 and every other z=1. Every coloured Hafnian equals "
            "90+15*(-6)=0, while all selected anchor cells equal 1."
        ),
        "conclusion": (
            "For every pure-matching chart A, its anchor product a_A is not "
            "in sqrt(I_mix). A valid localized certificate must retain a "
            "pure target factor, for example a_A^r*(H0*H1*H2)^m."
        ),
        "chosen_edge_histogram": {
            f"{u}{v}": count for (u, v), count in chosen_edge_histogram.items()
            if count
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("anchor-only saturation counterexample audit: PASS")
    print("triples / max union:", triples_checked, maximum_union)
    print("common hafnian:", hafnian)
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
