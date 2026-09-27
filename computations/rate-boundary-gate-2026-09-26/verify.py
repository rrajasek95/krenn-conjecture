#!/usr/bin/env python3
"""Exact finite checks for two non-prism boundary exclusions.

Python 3.10+, standard library. Checks integer coefficient maps, Gram
identities, rational norm constants, and corruption controls. The written
continuity and all-source norm arguments still need independent audit.
"""
import argparse
import hashlib
import itertools as it
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
VERTICES = tuple(range(6))
WORDS = tuple(it.product(range(3), repeat=6))
WORD_ID = {word: i for i, word in enumerate(WORDS)}


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


MATCHINGS = tuple(matchings(VERTICES))


def core_response(source, root):
    """T_Q: 15 inserted one-site entries -> 243 five-site coefficients."""
    core = tuple(v for v in VERTICES if v != root)
    words = tuple(it.product(range(3), repeat=5))
    columns = tuple(it.product(core, range(3)))
    result = [[0] * 15 for _ in words]
    for row, word in enumerate(words):
        colors = dict(zip(core, word))
        for column, (p, color) in enumerate(columns):
            if colors[p] != color:
                continue
            for matching in matchings(tuple(v for v in core if v != p)):
                value = 1
                for a, b in matching:
                    value *= source.get((a, b, colors[a], colors[b]), 0)
                result[row][column] += value
    pure = [[int(word == (c,) * 5) for c in range(3)] for word in words]
    return result, pure


def transpose(matrix):
    return list(map(list, zip(*matrix)))


def matmul(a, b):
    columns = transpose(b)
    return [[sum(x * y for x, y in zip(row, column)) for column in columns] for row in a]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def shift(matrix, scalar):
    return [[value - (scalar if i == j else 0) for j, value in enumerate(row)]
            for i, row in enumerate(matrix)]


def rank(matrix):
    pivots = {}
    for row in matrix:
        vector = {i: Q(value) for i, value in enumerate(row) if value}
        while vector:
            p = min(vector)
            if p not in pivots:
                coefficient = vector[p]
                pivots[p] = {i: value / coefficient for i, value in vector.items()}
                break
            coefficient = vector[p]
            for i, value in pivots[p].items():
                updated = vector.get(i, 0) - coefficient * value
                if updated:
                    vector[i] = updated
                elif i in vector:
                    del vector[i]
    return len(pivots)


def check_core_formula(source, root):
    """Compare the five-site formula against all six-site matching coefficients."""
    response, _ = core_response(source, root)
    core = tuple(v for v in VERTICES if v != root)
    core_word_id = {w: i for i, w in enumerate(it.product(range(3), repeat=5))}
    columns = {p: i for i, p in enumerate(it.product(core, range(3)))}
    for word in WORDS:
        direct = Counter()
        for matching in MATCHINGS:
            incident = next(edge for edge in matching if root in edge)
            p = incident[0] if incident[1] == root else incident[1]
            value = 1
            for a, b in matching:
                if (a, b) != incident:
                    value *= source.get((a, b, word[a], word[b]), 0)
            direct[p, word[p]] += value
        row = response[core_word_id[tuple(word[v] for v in core)]]
        require(all(direct[p] == row[i] for p, i in columns.items()),
                "one-site response disagrees with matching expansion")


def check_cycle():
    source = {(0, 1, 0, 0): 1, (1, 2, 1, 1): 1, (2, 3, 2, 2): 1,
              (3, 4, 0, 0): 1, (0, 4, 1, 1): 1}
    response, pure = core_response(source, 5)
    gram = matmul(transpose(response), response)
    require(gram == identity(15), "five-cycle response columns are orthonormal")
    projected = matmul(response, matmul(transpose(response), pure))
    pure_overlaps = [sum(row[c] ** 2 for row in projected) for c in range(3)]
    require(pure_overlaps == [1, 1, 0], "five-cycle accessible pure coordinates")
    augmented = [a + b for a, b in zip(response, pure)]
    require(rank(augmented) == 16, "five-cycle augmented response rank")
    check_core_formula(source, 5)
    eta = Q(1, 200)
    require(15 + Q(27, 4) * Q(1, 20) < 16, "cofactor perturbation constant")
    ceiling = 1 - (1 - 16 * eta) ** 2 / 3
    require(ceiling == Q(1346, 1875) and ceiling < Q(3, 4), "five-cycle fidelity gap")
    return {"response_rank": 15, "augmented_rank": 16,
            "squared_pure_projection_norms": pure_overlaps,
            "exact_fixed_core_fidelity_ceiling": "2/3", "core_radius": str(eta),
            "nearby_core_fidelity_ceiling": str(ceiling),
            "star_entries": "all 45 arbitrary complex entries; no smallness restriction"}


def build_two_four_map():
    """Full matching derivative at eight crossing I_3 blocks."""
    cells = [(p, q, i, j) for p, q in it.combinations(range(2, 6), 2)
             for i, j in it.product(range(3), repeat=2)]
    matrix = [[0] * 54 for _ in WORDS]
    for column, (p, q, i, j) in enumerate(cells):
        for matching in MATCHINGS:
            if (p, q) not in matching:
                continue
            rest = [edge for edge in matching if edge != (p, q)]
            if not all(a < 2 <= b for a, b in rest):
                continue
            for colors in it.product(range(3), repeat=2):
                word = [None] * 6
                word[p], word[q] = i, j
                for (a, b), color in zip(rest, colors):
                    word[a] = word[b] = color
                matrix[WORD_ID[tuple(word)]][column] += 1
    # A separate cut-based construction checks the same map.
    by_cut = [[0] * 54 for _ in WORDS]
    for column, (p, q, i, j) in enumerate(cells):
        r, s = [v for v in range(2, 6) if v not in (p, q)]
        for a, b in it.product(range(3), repeat=2):
            for first, second in ((r, s), (s, r)):
                word = [a, b, None, None, None, None]
                word[p], word[q], word[first], word[second] = i, j, a, b
                by_cut[WORD_ID[tuple(word)]][column] += 1
    require(matrix == by_cut, "two-versus-four response constructions disagree")
    return cells, matrix


def check_gram(gram):
    require(gram == transpose(gram) and len(gram) == 54, "symmetric Gram matrix")
    roots = (8, 12, 20, 40, 60)
    annihilator = identity(54)
    for root in roots:
        annihilator = matmul(annihilator, shift(gram, root))
    require(all(value == 0 for row in annihilator for value in row), "Gram annihilating polynomial")
    multiplicities = (9, 12, 18, 9, 6)
    power = identity(54)
    for degree in range(5):
        require(sum(power[i][i] for i in range(54))
                == sum(count * value ** degree for value, count in zip(roots, multiplicities)),
                "Gram spectral multiplicities")
        power = matmul(power, gram)
    return {str(value): count for value, count in zip(roots, multiplicities)}


def check_two_four():
    cells, matrix = build_two_four_map()
    gram = matmul(transpose(matrix), matrix)
    spectrum = check_gram(gram)
    target = [int(len(set(word)) == 1) for word in WORDS]
    correlation = [sum(column[i] * target[i] for i in range(729)) for column in transpose(matrix)]
    require(correlation == [2 if i == j else 0 for p, q, i, j in cells], "target correlation")
    require([sum(a * b for a, b in zip(row, correlation)) for row in gram]
            == [60 * a for a in correlation], "exact normal equations")
    projection_squared = Q(sum(a * a for a in correlation), 60)
    require(projection_squared == Q(6, 5), "target projection squared norm")
    fidelity = projection_squared / 3
    require(fidelity == Q(2, 5), "linear response fidelity ceiling")
    source = {(p, q, color, color): 1 for p in range(2)
              for q in range(2, 6) for color in range(3)}
    root_ranks = []
    for root in VERTICES:
        response, pure = core_response(source, root)
        pair = [rank(response), rank([a + b for a, b in zip(response, pure)])]
        require(pair == ([0, 3] if root < 2 else [9, 12]), "one-site ranks of two-four base")
        root_ranks.append(pair)
    crossing_histogram = Counter(sum(a < 2 <= b for a, b in m) for m in MATCHINGS)
    require(crossing_histogram == Counter({2: 12, 0: 3}), "two-four matching decomposition")
    eta = Q(1, 1000)
    require(Q(49, 10) ** 2 > 24 and Q(5, 2) ** 2 > 6, "radical upper bounds")
    require(49 + 5 * eta < 50, "crossing-map perturbation constant")
    require(Q(8, 3) ** 2 < 8, "smallest singular value lower bound")
    relative_error = Q(3, 8) * (50 * eta + 2 * eta ** 2)
    require(relative_error < Q(1, 50), "relative nonlinear error")
    require(Q(2, 3) ** 2 > Q(2, 5), "projection amplitude rounding")
    ceiling = ((Q(2, 3) + Q(1, 50)) / (1 - Q(1, 50))) ** 2
    require(ceiling == Q(103, 147) ** 2 and ceiling < Q(1, 2), "neighborhood fidelity ceiling")
    corrupted = [row[:] for row in gram]
    corrupted[0][0] += 1
    try:
        check_gram(corrupted)
    except ValueError:
        mutation = "REJECTED"
    else:
        raise ValueError("corrupt Gram matrix accepted")
    return {"response_shape": [729, 54], "response_rank": 54, "Gram_spectrum": spectrum,
            "target_projection_squared": str(projection_squared),
            "linear_response_fidelity_ceiling": str(fidelity),
            "neighborhood_radius": str(eta), "relative_error_upper": str(relative_error),
            "neighborhood_fidelity_ceiling": str(ceiling),
            "one_site_response_and_augmented_ranks": root_ranks,
            "Gram_mutation": mutation}


def check_prism_guard():
    base = {(0, 1, 0, 0): 1, (0, 2, 2, 2): 1, (1, 2, 1, 1): 1,
            (3, 4, 0, 0): 1, (3, 5, 2, 2): 1, (4, 5, 1, 1): 1}
    vertical = {(0, 3, 1, 1), (1, 4, 2, 2), (2, 5, 0, 0)}
    ranks = []
    for root in VERTICES:
        response, pure = core_response(base, root)
        pair = [rank(response), rank([a + b for a, b in zip(response, pure)])]
        require(pair == [9, 11], "known GHZ-approaching prism limit must pass the rank filter")
        ranks.append(pair)
    output = {}
    for word in WORDS:
        polynomial = Counter()
        for matching in MATCHINGS:
            power = 0
            for p, q in matching:
                x = (p, q, word[p], word[q])
                if x in vertical:
                    power += 1
                elif x not in base:
                    break
            else:
                polynomial[power] += 1
        if polynomial:
            output[word] = polynomial
    expected = {(c,) * 6: Counter({1: 1}) for c in range(3)}
    expected[(1, 2, 0) * 2] = Counter({3: 1})
    require(output == expected, "prism guard must retain its exact GHZ border family")
    return {"one_site_response_and_augmented_ranks": ranks,
            "exact_output": "t * Delta + t^3 * bcabca", "rank_filter": "PASSES, as required"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a receipt; refuses overwrite")
    args = parser.parse_args()
    result = {"status": "PASS", "evidence_status": "NEW RESEARCH; NOT INDEPENDENTLY AUDITED",
              "five_cycle": check_cycle(), "two_versus_four": check_two_four(),
              "prism_scope_guard": check_prism_guard()}
    paths = [HERE / "verify.py", ROOT / "notes/rate-boundary-exclusions-2026-09-26.md",
             ROOT / "proofs/six-site-arbitrary-complex-obstruction.md"]
    result["sha256"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in paths}
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x") as handle:
            handle.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
