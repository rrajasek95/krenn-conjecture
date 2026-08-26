#!/usr/bin/env python3
"""Export the exact chart-1 isolated-support Laurent feasibility gate."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIME = 1073741827
BASE = ((0, 1), (2, 3), (4, 5), (6, 7))
BASE_SET = frozenset(BASE)
GRAPHS = (
    frozenset({(0,1),(0,3),(0,5),(0,6),(0,7),(1,3),(1,5),(2,3),
               (2,4),(2,5),(2,6),(2,7),(4,5),(4,6),(5,6),(6,7)}),
    frozenset({(0,1),(0,2),(0,3),(1,4),(1,5),(1,6),(1,7),(2,3),
               (2,4),(3,4),(3,6),(3,7),(4,5),(5,6),(5,7),(6,7)}),
    frozenset({(0,1),(0,2),(0,4),(0,5),(1,2),(1,6),(1,7),(2,3),
               (2,4),(2,6),(3,4),(3,6),(4,5),(5,6),(5,7),(6,7)}),
)
INPUT = HERE / f"isolated_support_full_live_p{PRIME}.msolve"
RESULT = HERE / "results_isolated_support_export.json"


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
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(range(8)))


def name(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    return f"x{u}{v}_{a}{b}"


def is_live(u, v, a, b):
    return a != b or (u, v) in GRAPHS[a]


def normalized_term(word, matching):
    factors = []
    for u, v in matching:
        a, b = word[u], word[v]
        if not is_live(u, v, a, b):
            return None
        if not ((u, v) in BASE_SET and a == b):
            factors.append(name(u, v, a, b))
    return tuple(sorted(factors))


def polynomial(word, pure):
    terms = Counter()
    for matching in MATCHINGS:
        term = normalized_term(word, matching)
        if term is not None:
            terms[term] += 1
    if pure:
        terms[()] -= 1
    return Counter({term: coefficient for term, coefficient in terms.items()
                    if coefficient})


def render(poly):
    pieces = []
    for term, coefficient in sorted(poly.items()):
        monomial = "*".join(term) or "1"
        if coefficient == 1:
            piece = monomial
        elif coefficient == -1:
            piece = "-" + monomial
        else:
            piece = f"{coefficient}*{monomial}"
        pieces.append(piece)
    return "+".join(pieces).replace("+-", "-")


def main():
    require(len(MATCHINGS) == 105, len(MATCHINGS))
    require(all(BASE_SET <= graph and len(graph) == 16 for graph in GRAPHS),
            "diagonal graph shape")
    replacements = []
    for left, right in combinations(BASE, 2):
        a, b = left; c, d = right
        replacements.extend((((a, c), (b, d)), ((a, d), (b, c))))
    require(len(replacements) == 12, len(replacements))
    require(all(not set(replacement) <= graph for graph in GRAPHS
                for replacement in replacements), "base has a live C4 exit")
    require((0, 2) not in GRAPHS[0]
            and (0, 2) in GRAPHS[1] and (0, 2) in GRAPHS[2],
            "marked boundary guard")

    support = [(u, v, a, b) for u, v in combinations(range(8), 2)
               for a, b in product(range(3), repeat=2)
               if is_live(u, v, a, b)]
    normalized = {(u, v, c, c) for u, v in BASE for c in range(3)}
    variables = [name(*cell) for cell in support if cell not in normalized]
    require((len(support), len(variables), len(set(variables))) == (216, 204, 204),
            (len(support), len(variables), len(set(variables))))

    rows = []
    mixed_histogram = Counter()
    profile_min = {}
    total_terms = 0
    pure_terms = []
    for word in product(range(3), repeat=8):
        pure = len(set(word)) == 1
        poly = polynomial(word, pure)
        require(poly, ("zero source row", word))
        count = len(poly)
        total_terms += count
        rows.append(render(poly))
        if pure:
            pure_terms.append(count)
        else:
            mixed_histogram[count] += 1
            profile = tuple(sorted((word.count(c) for c in range(3)), reverse=True))
            profile_min[profile] = min(profile_min.get(profile, 10**9), count)
    require(len(rows) == 6561 and sum(mixed_histogram.values()) == 6558,
            (len(rows), sum(mixed_histogram.values())))
    require(min(mixed_histogram) == 12, min(mixed_histogram))
    require(pure_terms == [9, 12, 11], pure_terms)

    rows.append("*".join(variables))
    with INPUT.open("w") as handle:
        handle.write(",".join(variables) + "\n")
        handle.write(str(PRIME) + "\n")
        for index, row in enumerate(rows):
            handle.write(row)
            handle.write(",\n" if index + 1 < len(rows) else "\n")

    result = {
        "format": "n8-chart1-isolated-support-f4sat-export-v1",
        "status": "EXACT_EXPORT_NO_ALGEBRAIC_VERDICT",
        "prime": PRIME,
        "support_cells": len(support),
        "normalized_anchor_cells": len(normalized),
        "source_variables": len(variables),
        "source_rows": 6561,
        "f4sat_rows_including_live_product": len(rows),
        "source_monomial_terms": total_terms,
        "pure_residual_term_counts": pure_terms,
        "mixed_distinct_term_histogram": {str(k): v for k, v in sorted(mixed_histogram.items())},
        "mixed_profile_minimum_terms": {"-".join(map(str, k)): v
                                        for k, v in sorted(profile_min.items())},
        "minimum_mixed_terms": min(mixed_histogram),
        "maximum_mixed_terms": max(mixed_histogram),
        "marked_boundary": "A_02[0,0]=0; A_02[1,1],A_02[2,2] live",
        "base_live_c4_exits": 0,
        "pure_fibre_counts_before_target_subtraction": [10, 13, 12],
        "round6_control": {
            "colour1_dual_matching_02_14_36_57_live":
                set(((0,2),(1,4),(3,6),(5,7))) <= GRAPHS[1],
            "colour1_second_matching_02_16_34_57_live":
                set(((0,2),(1,6),(3,4),(5,7))) <= GRAPHS[1],
            "colour2_second_matching_02_16_34_57_live":
                set(((0,2),(1,6),(3,4),(5,7))) <= GRAPHS[2],
        },
        "input": INPUT.name,
        "input_bytes": INPUT.stat().st_size,
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "scope": (
            "Literal full 6561-row restriction with all 204 non-anchor live "
            "cells saturated. Modular F4SAT is discovery only; this export "
            "itself gives no characteristic-zero feasibility verdict."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
