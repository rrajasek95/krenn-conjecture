#!/usr/bin/env python3
"""Exact finite replay for the written local complex stability proof.

No floating-point evidence, optimizer, third-party library, or assertion is
needed. This verifies the finite lemmas, not an independent mathematical audit.
"""
import argparse
import copy
import hashlib
import itertools as it
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
EDGES = tuple(it.combinations(range(6), 2))
EDGE_ID = {edge: i for i, edge in enumerate(EDGES)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    for j in range(1, len(vertices)):
        for rest in matchings(vertices[1:j] + vertices[j + 1:]):
            yield ((vertices[0], vertices[j]),) + rest


MATCHINGS = tuple(matchings(tuple(range(6))))


@lru_cache(None)
def graphs(degrees):
    """Pair one stub at a time, deduplicating repeated edges.

    Independent of the generator's whole-vertex neighbor-allocation method.
    Returns edge indices, permitting repeated indices in a multigraph.
    """
    if not any(degrees):
        return ((),)
    p = next(i for i, value in enumerate(degrees) if value)
    out = set()
    for q in range(p + 1, 6):
        if degrees[q]:
            updated = list(degrees)
            updated[p] -= 1
            updated[q] -= 1
            edge = EDGE_ID[p, q]
            for rest in graphs(tuple(updated)):
                out.add(tuple(sorted((edge,) + rest)))
    return tuple(sorted(out))


def colored_products(degrees):
    for parts in it.product(*(graphs(d) for d in degrees)):
        yield tuple(c * 15 + edge for c, part in enumerate(parts) for edge in part)


def mixed_columns():
    for pattern in it.product(range(4), repeat=3):
        if sum(pattern) != 3:
            continue
        for word in it.product(range(3), repeat=6):
            if len(set(word)) == 1:
                continue
            degrees = [tuple(pattern[c] - int(word[i] == c) for i in range(6))
                       for c in range(3)]
            if any(min(d) < 0 or sum(d) % 2 for d in degrees):
                continue
            generator = [tuple(sorted(15 * word[p] + EDGE_ID[p, q] for p, q in matching))
                         for matching in MATCHINGS
                         if all(word[p] == word[q] for p, q in matching)]
            for multiplier in colored_products(degrees):
                yield Counter(tuple(sorted(multiplier + term)) for term in generator)


def balance_columns():
    pure = [tuple(EDGE_ID[edge] for edge in matching) for matching in MATCHINGS]
    for pattern in it.product(range(3), repeat=3):
        if sum(pattern) != 2:
            continue
        for multiplier in colored_products([(k,) * 6 for k in pattern]):
            for color in (1, 2):
                column = Counter()
                for matching in pure:
                    column[tuple(sorted(multiplier + matching))] += 1
                    shifted = tuple(15 * color + edge for edge in matching)
                    column[tuple(sorted(multiplier + shifted))] -= 1
                yield column


def check_dual(certificate):
    require(certificate["format"] == "diagonal-edge-cell-ids-v1", "certificate format")
    require(certificate["edge_order"] == list(map(list, EDGES)), "edge ordering")
    require(certificate["target"] == "tau_a * tau_b * tau_c", "target convention")
    functional = {}
    for monomial, value in certificate["functional"]:
        m = tuple(monomial)
        require(len(m) == 9 and m == tuple(sorted(m))
                and all(type(i) is int and 0 <= i < 45 for i in m), "monomial encoding")
        require(m not in functional and type(value) is int and value != 0, "functional entry")
        degrees = [[0] * 6 for _ in range(3)]
        for cell in m:
            color, edge = divmod(cell, 15)
            for vertex in EDGES[edge]:
                degrees[color][vertex] += 1
        require(all(len(set(d)) == 1 for d in degrees)
                and sum(d[0] for d in degrees) == 3, "uniform degree-nine sector")
        functional[m] = value
    counts = {}
    for name, columns in (("mixed", mixed_columns()), ("balanced", balance_columns())):
        count = 0
        for column in columns:
            require(sum(a * functional.get(m, 0) for m, a in column.items()) == 0,
                    f"functional does not annihilate every {name} column")
            count += 1
        counts[name] = count
    require(counts == {"mixed": 16290, "balanced": 2130}, "complete column counts")
    target_value = sum(functional.get(m, 0)
                       for m in colored_products([(1,) * 6] * 3))
    require(target_value == certificate["target_evaluation"] == 64, "nonzero target evaluation")
    regular_counts = [len(graphs((k,) * 6)) for k in (1, 2, 3)]
    require(regular_counts == [15, 130, 760], "regular multigraph counts")
    sector_size = 3 * 760 + 6 * 130 * 15 + 15 ** 3
    require(sector_size == 17355, "sector basis count")
    require(len(functional) == 1296, "functional support size")
    return {"coefficient_field": "integers", "support_size": len(functional),
            "sector_basis_size": sector_size, "column_counts": counts,
            "total_columns": sum(counts.values()), "target_evaluation": target_value}


def cell(p, q, i, j):
    return (p, q, i, j) if p < q else (q, p, j, i)


BASE = {(0, 1): (0, 0), (0, 2): (2, 2), (1, 2): (1, 1),
        (3, 4): (0, 0), (3, 5): (2, 2), (4, 5): (1, 1)}
VERTICAL = {(0, 3): (1, 1), (1, 4): (2, 2), (2, 5): (0, 0)}


def output_word(cells):
    word = [None] * 6
    for p, q, i, j in cells:
        require(word[p] is None and word[q] is None, "overlapping matching cells")
        word[p], word[q] = i, j
    require(None not in word, "incomplete matching")
    return tuple(word)


def check_decomposition():
    counts = Counter(sum(p < 3 <= q for p, q in matching) for matching in MATCHINGS)
    require(counts == Counter({1: 9, 3: 6}), "one-or-three crossing decomposition")
    coefficient_count = 0
    for word in it.product(range(3), repeat=6):
        full = Counter(tuple(sorted(cell(p, q, word[p], word[q]) for p, q in matching))
                       for matching in MATCHINGS)
        split = Counter()
        for p in range(3):
            left = tuple(v for v in range(3) if v != p)
            for q in range(3, 6):
                right = tuple(v for v in range(3, 6) if v != q)
                matching = (left, (p, q), right)
                split[tuple(sorted(cell(i, j, word[i], word[j]) for i, j in matching))] += 1
        for permutation in it.permutations(range(3, 6)):
            matching = tuple(zip(range(3), permutation))
            split[tuple(sorted(cell(i, j, word[i], word[j]) for i, j in matching))] += 1
        require(full == split, "H = U B V^T + K(B) coefficient identity")
        coefficient_count += 1
    selected = []
    for p in range(3):
        pair = tuple(v for v in range(3) if v != p)
        for color in range(3):
            word = [None] * 3
            word[p] = color
            word[pair[0]], word[pair[1]] = BASE[pair]
            selected.append(tuple(word))
    require(len(set(selected)) == 9, "U0 selected block is the identity")
    require(all((c, c, c) in selected for c in range(3)), "pure-word projection")
    require((1, 2, 0) not in selected, "protected row lies outside selected block")
    return {"matching_counts": dict(counts), "coefficient_identities": coefficient_count,
            "selected_local_words": ["".join("abc"[c] for c in w) for w in selected]}


def check_tangent():
    cells = [edge + colors for edge in EDGES for colors in it.product(range(3), repeat=2)]
    derivative = defaultdict(list)
    for x in cells:
        for matching in MATCHINGS:
            if x[:2] not in matching:
                continue
            rest = [edge for edge in matching if edge != x[:2]]
            if all(edge in BASE for edge in rest):
                derivative[output_word([x] + [edge + BASE[edge] for edge in rest])].append(x)
    crossing = {x for x in cells if x[0] < 3 <= x[1]}
    require(len(derivative) == 81 and all(len(v) == 1 for v in derivative.values()),
            "derivative has 81 independent crossing columns")
    require({v[0] for v in derivative.values()} == crossing, "derivative kernel is internal")
    require({derivative[(c,) * 6][0] for c in range(3)}
            == {edge + colors for edge, colors in VERTICAL.items()}, "forced crossing tangent")
    second_order = defaultdict(Counter)
    for x in cells:
        if x[:2] not in BASE:
            continue
        for edge, base_colors in BASE.items():
            for cross, cross_colors in VERTICAL.items():
                if len(set(x[:2] + edge + cross)) == 6:
                    word = output_word([x, edge + base_colors, cross + cross_colors])
                    if word not in derivative:
                        second_order[word][x] += 1
    require(len(second_order) == 48
            and all(len(row) == 1 and next(iter(row.values())) == 1
                    for row in second_order.values()), "48 separate second-order equations")
    constrained = {x for row in second_order.values() for x in row}
    remaining = {x for x in cells if x[:2] in BASE} - constrained
    require(len(constrained) == 48 and remaining == {edge + colors for edge, colors in BASE.items()},
            "only the six original internal cells survive")
    word = (1, 2, 0) * 2
    require(all((word[p], word[q]) != colors for (p, q), colors in BASE.items()),
            "protected word cannot use a base edge at any perturbation order")
    protected = sum(all(edge in VERTICAL and (word[edge[0]], word[edge[1]]) == VERTICAL[edge]
                        for edge in matching) for matching in MATCHINGS)
    require(protected == 1, "protected cubic coefficient")
    return {"crossing_rank": 81, "internal_kernel_dimension": 54,
            "second_order_constraints": 48, "remaining_internal_dimension": 6,
            "protected_word": "bcabca", "protected_cubic_coefficient": protected}


def check_constants():
    eta = Q(1, 1000)
    l_max = 2 * eta
    inverse = 1 / (1 - 2 * eta)
    deviation = 2 * eta / (1 - 2 * eta)
    require(inverse < Q(101, 100) and deviation < Q(1, 400), "inverse estimates")
    require(Q(101, 100) ** 2 < Q(11, 10), "inverse product")
    require((1 + 2 * eta) ** 2 + 2 * eta ** 2 < 2, "target amplitude bound")
    b_factor = Q(11, 10) * (Q(7, 4) + l_max ** 2 / 2) / (1 - Q(11, 5) * eta ** 2)
    require(b_factor < 2, "b < 2 |lambda| under the contradiction assumption")
    d_factor = Q(7, 4) * Q(1, 400) * Q(201, 100) + Q(11, 10) * Q(33, 2) * l_max ** 2
    require(d_factor < Q(1, 100), "crossing-matrix approximation")
    require(Q(401, 400) * Q(33, 2) < 17, "pure-column graph bounds")
    linear_factor = 289 * l_max ** 2 + Q(33, 320000)
    require(linear_factor < Q(1, 500), "possible linear cancellation")
    cubic_factor = 1 - 4 * 2 ** 2 * Q(1, 100)
    require(cubic_factor == Q(21, 25), "protected cubic lower bound")
    require(cubic_factor - Q(1, 500) > Q(1, 2), "strict contradiction margin")
    require(Q(7, 4) ** 2 > 3 and 4 ** 2 > 12, "radical roundings")
    return {"radius": str(eta), "error_lower_bound_coefficient": "1/2",
            "b_over_lambda_upper": str(b_factor), "crossing_error_over_lambda_upper": str(d_factor),
            "linear_cancellation_over_lambda_cubed_upper": str(linear_factor),
            "protected_cubic_lower": str(cubic_factor),
            "final_lower_before_contradiction": str(cubic_factor - Q(1, 500))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a receipt, refusing to overwrite")
    args = parser.parse_args()
    certificate = json.loads((HERE / "balanced-dual.json").read_text())
    result = {"status": "PASS", "evidence_status": "NEW RESEARCH; NOT INDEPENDENTLY AUDITED",
              "matching_decomposition": check_decomposition(), "tangent": check_tangent(),
              "local_norm_constants": check_constants(), "balanced_cubic_nonmembership": check_dual(certificate)}
    corrupt = copy.deepcopy(certificate)
    corrupt["functional"][0][1] += 1
    try:
        check_dual(corrupt)
    except ValueError:
        result["dual_mutation"] = "REJECTED"
    else:
        raise ValueError("corrupt certificate accepted")
    paths = [HERE / "verify.py", HERE / "build_dual.py", HERE / "balanced-dual.json",
             ROOT / "notes/complex-rate-bound-2026-09-26.md",
             ROOT / "notes/universal-rate-bound-feasibility-2026-09-26.md"]
    result["sha256"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in paths}
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x") as handle:
            handle.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
