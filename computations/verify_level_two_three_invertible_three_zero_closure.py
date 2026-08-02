#!/usr/bin/env python3
"""Formal audit of the 3I+3Z generic-kernel support closure."""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
formal_core = run_path(str(HERE / (
    "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
)))
rank_core = run_path(str(HERE / (
    "verify_level_two_one_sided_overlap_collapse.py"
)))

Counter = formal_core["Counter"]
variable = formal_core["variable"]
poly_add = formal_core["polynomial_add"]
poly_mul = formal_core["polynomial_multiply"]
formal_tensor = formal_core["formal_matching_tensor"]
MATCHINGS = formal_core["MATCHINGS"]

COLOURS = (0, 1)
SITES = tuple(range(6))
INNER = (0, 1, 2)
ZERO = (3, 4, 5)
EDGES = tuple(combinations(SITES, 2))

ENVELOPES = {
    "bipartite": (
        set(combinations(INNER, 2))
        | {(i, z) for i in INNER for z in ZERO}
    ),
    "leaf_path": (
        set(combinations(INNER, 2))
        | {(i, z) for i in INNER for z in (4, 5)}
        | {(3, 4), (3, 5)}
    ),
    "zero_triangle": (
        set(combinations(INNER, 2))
        | {(0, z) for z in ZERO}
        | set(combinations(ZERO, 2))
    ),
    "centre_star": (
        set(combinations(INNER, 2))
        | {(i, 3) for i in INNER}
        | {(3, 4), (3, 5)}
    ),
}


def build_formal_packet(kind):
    support = ENVELOPES[kind]
    return {
        (u, v, a, b): (
            variable(f"M_{u}_{v}_{a}_{b}")
            if (u, v) in support else Counter()
        )
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def term(packet, matching, word):
    answer = Counter({(): 1})
    for u, v in matching:
        answer = poly_mul(answer, packet[u, v, word[u], word[v]])
    return answer


def audit_factorizations():
    counts = {}
    for kind in ENVELOPES:
        packet = build_formal_packet(kind)
        live_matchings = tuple(
            matching for matching in MATCHINGS[SITES]
            if all((u, v) in ENVELOPES[kind] for u, v in matching)
        )
        counts[kind] = len(live_matchings)

        if kind == "bipartite":
            require(all(
                all((u in INNER) != (v in INNER) for u, v in matching)
                for matching in live_matchings
            ), "bipartite envelope has a noncross matching")
        elif kind == "leaf_path":
            require(all(
                sum(edge in ((3, 4), (3, 5)) for edge in matching) == 1
                for matching in live_matchings
            ), "leaf-path factor split failed")
        elif kind == "zero_triangle":
            require(all((1, 2) in matching for matching in live_matchings),
                    "zero-triangle fixed edge failed")
        else:
            require(not live_matchings,
                    "centre-star envelope unexpectedly has a matching")

        for word in product(COLOURS, repeat=6):
            expected = poly_add(*(
                term(packet, matching, word)
                for matching in live_matchings
            ))
            require(formal_tensor(packet, word) == expected,
                    (kind, "formal matching split failed", word))

    require(counts == {
        "bipartite": 6,
        "leaf_path": 6,
        "zero_triangle": 3,
        "centre_star": 0,
    }, ("matching counts changed", counts))
    require((32 + 12, 38 + 16, 19 + 24, 0 + 28)
            == (44, 54, 43, 28), "dimension bounds changed")
    return counts


def audit_zero_sum_classification():
    observed = set()
    for values in product(range(-3, 4), repeat=6):
        if any(values[i] + values[j] == 0
               for i, j in combinations(INNER, 2)):
            continue
        z_edges = {
            edge for edge in combinations(ZERO, 2)
            if values[edge[0]] + values[edge[1]] == 0
        }
        if len(z_edges) == 3:
            require(all(values[z] == 0 for z in ZERO),
                    ("nonzero zero-sum triangle", values))
            require(sum(values[i] == 0 for i in INNER) <= 1,
                    ("two zero invertible multipliers", values))
            observed.add("zero_triangle")
        elif len(z_edges) == 2:
            degrees = {
                z: sum(z in edge for edge in z_edges)
                for z in ZERO
            }
            centre = next(z for z in ZERO if degrees[z] == 2)
            leaves = set(ZERO) - {centre}
            inner_to_centre = {
                i for i in INNER if values[i] + values[centre] == 0
            }
            inner_to_leaves = {
                i for i in INNER
                if any(values[i] + values[z] == 0 for z in leaves)
            }
            require(not (inner_to_centre and inner_to_leaves),
                    ("path cross classes mixed", values))
            observed.add(
                "centre_star" if inner_to_centre else "leaf_path"
            )
        elif len(z_edges) == 1:
            u, v = next(iter(z_edges))
            if values[u]:
                require(not (
                    any(values[i] + values[u] == 0 for i in INNER)
                    and any(values[i] + values[v] == 0 for i in INNER)
                ), ("opposite nonzero Z endpoints both met INNER", values))
            else:
                require(sum(values[i] == 0 for i in INNER) <= 1,
                        ("two zero invertible multipliers", values))
            observed.add("leaf_path")
        else:
            observed.add("bipartite")
    require(observed == set(ENVELOPES),
            ("support envelope classification incomplete", observed))
    return observed


def build_numeric_packet(kind):
    support = ENVELOPES[kind]
    return {
        (u, v, a, b): (
            1 + (17 * edge_index + 7 * a + 11 * b
                 + 3 * edge_index * edge_index) % 29
            if (u, v) in support else 0
        )
        for edge_index, (u, v) in enumerate(EDGES)
        for a, b in product(COLOURS, repeat=2)
    }


def main():
    counts = audit_factorizations()
    observed = audit_zero_sum_classification()
    ranks = []
    for kind in ENVELOPES:
        derivative = rank_core["differential"](build_numeric_packet(kind))
        ranks.append(tuple(
            rank_core["rank_mod"](derivative, prime)
            for prime in (101, 1_000_003)
        ))
    require(ranks == [(44, 44), (48, 48), (42, 42), (27, 27)],
            ("calibration ranks changed", ranks))
    print(
        "3I+3Z closure: "
        f"matching counts {counts}, envelopes {sorted(observed)}; "
        "rank bounds 44/54/43/28, calibrations 44/48/42/27"
    )


if __name__ == "__main__":
    main()
