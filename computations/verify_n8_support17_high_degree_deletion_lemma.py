#!/usr/bin/env python3
"""Verify the support-17 high-degree deletion lemma on eight vertices.

For a simple graph on eight vertices with 17 edges and minimum degree at
least three, put H={v:deg(v)>=4}.  The degree excess above three is ten.
If H were independent, all degrees at H would be carried by the cubic
vertices L, giving 3|H|+10 <= 3(8-|H|).  This forces |H|<=2, whereas ten
units of excess and maximum degree seven force |H|>=3.  Hence H contains an
edge.  Deleting that edge leaves a 16-edge graph of minimum degree at least
three.

The finite audit enumerates every possible ordered degree sequence; the
proof itself is the displayed capacity argument and does not rely on graph
enumeration.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
import json


N = 8
EDGES = 17
MIN_DEGREE = 3
MAX_DEGREE = N - 1
EXPECTED_LEDGER_SHA256 = (
    "d79dd734c485958f88567d8dc683f03408d09b47c695ff87e9dc7b1a99e61631"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def audit() -> tuple[dict[str, object], str]:
    degree_sequences = tuple(
        degrees for degrees in product(
            range(MIN_DEGREE, MAX_DEGREE + 1), repeat=N
        )
        if sum(degrees) == 2 * EDGES
    )
    require(degree_sequences, "degree-sequence census is empty")

    hist: dict[int, int] = {}
    for degrees in degree_sequences:
        high = tuple(degree for degree in degrees if degree >= 4)
        low = tuple(degree for degree in degrees if degree == 3)
        excess = sum(degree - 3 for degree in degrees)
        require(excess == 2 * EDGES - 3 * N == 10,
                (degrees, excess))
        require(len(high) >= 3,
                ("ten excess units need at least three high vertices",
                 degrees, high))
        high_degree_sum = sum(high)
        low_capacity = sum(low)
        require(high_degree_sum == 3 * len(high) + 10,
                (degrees, high_degree_sum))
        require(high_degree_sum > low_capacity,
                ("an independent high set would fit into cubic capacity",
                 degrees, high_degree_sum, low_capacity))
        hist[len(high)] = hist.get(len(high), 0) + 1

    ledger = {
        "theorem": "N=8 support-17 high-degree deletion lemma",
        "ordered_degree_sequences": len(degree_sequences),
        "high_vertex_count_histogram": hist,
        "degree_excess": 10,
        "independent_high_set_capacity":
            "3|H|+10 <= 3(8-|H|) would force |H|<=2",
        "excess_lower_bound":
            "max(deg-3)=4 forces |H|>=ceil(10/4)=3",
        "conclusion": (
            "every simple 17-edge graph on eight vertices with minimum "
            "degree at least three has an edge joining two vertices of "
            "degree at least four; deleting it leaves support 16 and "
            "minimum degree at least three"
        ),
        "scope": (
            "graph-theoretic reduction only; persistence of a support-16 "
            "clean-cap or singleton exit after reinserting the edge is a "
            "separate source-labelled theorem"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("N=8 support-17 high-degree deletion lemma: PASS")
    print("ordered degree sequences:", ledger["ordered_degree_sequences"])
    print("high-vertex histogram:", ledger["high_vertex_count_histogram"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
