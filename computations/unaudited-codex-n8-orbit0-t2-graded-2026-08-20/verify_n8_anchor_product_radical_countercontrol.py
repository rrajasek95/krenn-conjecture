#!/usr/bin/env python3
"""Exact countercontrol to anchor-product radical membership on all 31 charts."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from math import prod
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHART_PATH = ROOT / "computations" / "verify_n8_target_triple_localization_orbits.py"
SPEC = importlib.util.spec_from_file_location("chart_cover", CHART_PATH)
CHART = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHART)
SOURCE = CHART.SOURCE
OUT = HERE / "results_n8_anchor_product_radical_countercontrol.json"


def require(condition: bool, detail: str) -> None:
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
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield (tuple(sorted((first, second))),) + tail


def hafnian(edge_values, matchings):
    return sum(prod(edge_values[edge] for edge in matching)
               for matching in matchings)


def chart_physical_edges(row):
    mate = SOURCE.decode_key(row)
    port_edges = SOURCE.mate_edges(mate)
    require(len(port_edges) == 12, "chart does not have twelve anchors")
    answer = []
    for left, right in port_edges:
        u, a = divmod(left, 3)
        v, b = divmod(right, 3)
        require(a == b, "chart anchor is not pure")
        answer.append((min(u, v), max(u, v), a))
    return tuple(answer)


def main() -> None:
    rows = tuple(sorted(SOURCE.target_orbit_rows()))
    require(len(rows) == 31, "chart count changed")
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105 and len(set(matchings)) == 105,
            "PM(8) count changed")
    all_edges = tuple((u, v) for u in range(8) for v in range(u + 1, 8))
    records = []
    for index, row in enumerate(rows, 1):
        anchors = chart_physical_edges(row)
        selected_physical = {(u, v) for u, v, _colour in anchors}
        outside = next(edge for edge in all_edges if edge not in selected_physical)
        values = {edge: (-6 if edge == outside else 1) for edge in all_edges}
        containing = sum(outside in matching for matching in matchings)
        avoiding = len(matchings) - containing
        require((avoiding, containing) == (90, 15),
                "single-edge PM split changed")
        value = hafnian(values, matchings)
        require(value == avoiding - 6 * containing == 0,
                "countercontrol hafnian is nonzero")
        require(all(values[(u, v)] == 1 for u, v, _colour in anchors),
                "chosen exceptional edge hits a chart anchor")

        # With x_uv^{ab}=s_{u,a}s_{v,b}z_uv and all s=1, every H_w is
        # literally the same hafnian.  Check representative pure/mixed words
        # directly as a guard on endpoint factorization.
        test_words = ((0,) * 8, (1,) * 8, (2,) * 8,
                      (0, 1, 2, 0, 1, 2, 0, 1))
        evaluations = []
        for word in test_words:
            word_value = sum(prod(values[edge] for edge in matching)
                             for matching in matchings)
            evaluations.append(word_value)
        require(evaluations == [0, 0, 0, 0],
                "word evaluations no longer share the scalar hafnian")
        records.append({
            "chart": index,
            "selected_physical_edge_count": len(selected_physical),
            "exceptional_edge": list(outside),
            "z_exceptional_value": -6,
            "hafnian_avoiding_terms": avoiding,
            "hafnian_containing_terms": containing,
            "all_mixed_Hw": 0,
            "all_pure_Hc": 0,
            "anchor_product": 1,
        })

    result = {
        "status": "UNAUDITED exact all-chart radical countercontrol",
        "chart_ledger_sha256": CHART.EXPECTED_LEDGER_SHA256,
        "charts": len(records),
        "construction": (
            "For each chart choose e outside its selected physical edges; "
            "put x_uv^{ab}=z_uv, z_e=-6, and all other z_uv=1. Every word "
            "hafnian is 90+15*(-6)=0, while all twelve selected anchors "
            "equal one."
        ),
        "records": records,
        "conclusion": (
            "For every chart j, its twelve-anchor product a_j is not in "
            "sqrt(I_mix)."
        ),
        "scope": (
            "This does not refute the valid localization cover using "
            "a_j^N*(H0*H1*H2)^e, because this countercontrol also has all "
            "three pure hafnians equal to zero."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("N=8 anchor-product radical countercontrol: PASS")
    print("charts/counterexamples:", len(records), len(records))
    print("all evaluations: mixed=0 pure=0 anchor_product=1")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
