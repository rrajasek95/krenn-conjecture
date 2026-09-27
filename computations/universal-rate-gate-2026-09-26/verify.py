#!/usr/bin/env python3
"""Exact feasibility gate: a nonnegative rate bound and a failed complex shortcut.

Standard library, Python 3.10+. This checks the finite certificate portions,
not the accompanying all-order algebraic/analytic written arguments.
"""
import argparse
import copy
import hashlib
import itertools as it
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def require(value, message):
    if not value:
        raise ValueError(message)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    for j in range(1, len(vertices)):
        for matching in matchings(vertices[1:j] + vertices[j + 1:]):
            yield ((vertices[0], vertices[j]),) + matching


def setup():
    vertices = tuple(range(6))
    edges = list(it.combinations(vertices, 2))
    ms = list(matchings(vertices))
    subsets = {tuple(sorted(m)) for m in it.combinations(edges, 3)
               if sorted(v for e in m for v in e) == list(vertices)}
    require(set(ms) == subsets and len(ms) == 15, "independent matching enumerations")
    return vertices, edges, ms, {m: i for i, m in enumerate(ms)}


def ideal_relations(vertices, lookup):
    """Every monomial multiple in the target's site-and-color multidegree.

    A target monomial uses every (site,color) exactly once. A mixed coefficient
    occupies one color at each site. Its multiplier must match the remaining
    sites separately in each color. Odd-sized color sets give zero generators.
    """
    for word in it.product(range(3), repeat=6):
        if len(set(word)) == 1:
            continue
        groups = [tuple(v for v in vertices if word[v] == c) for c in range(3)]
        if any(len(group) % 2 for group in groups):
            continue
        complements = [tuple(v for v in vertices if word[v] != c) for c in range(3)]
        generator_terms = list(it.product(*(list(matchings(g)) for g in groups)))
        for multiplier in it.product(*(list(matchings(g)) for g in complements)):
            yield tuple(tuple(lookup[tuple(sorted(generator_terms_part[c] + multiplier[c]))]
                              for c in range(3))
                        for generator_terms_part in generator_terms)


def check_dual(data, vertices, lookup):
    require(data["matching_order"] == [list(map(list, m)) for m in matchings(vertices)],
            "dual matching convention changed")
    dual = {tuple(entry["triple"]): Q(entry["value"]) for entry in data["functional"]}
    require(len(dual) == len(data["functional"]), "duplicate dual entry")
    require(all(len(row) == 3 and all(0 <= i < 15 for i in row) for row in dual),
            "invalid dual row")
    sizes = Counter()
    for relation in ideal_relations(vertices, lookup):
        require(sum((dual.get(row, Q(0)) for row in relation), Q(0)) == 0,
                "functional does not annihilate every ideal generator multiple")
        sizes[len(relation)] += 1
    target_value = sum(dual.values(), Q(0))
    require(target_value != 0, "functional must detect the target")
    require(target_value == Q(data["target_value"]), "wrong claimed target evaluation")
    return {"support_size": len(dual), "target_evaluation": str(target_value),
            "one_term_multiples": sizes[1], "three_term_multiples": sizes[3],
            "total_multiples": sum(sizes.values())}


def check_positive_cover(vertices, edges, ms):
    edge_id = {edge: i for i, edge in enumerate(edges)}
    sets = list(map(set, ms))
    word_totals = defaultdict(Q)
    quotient_coefficients = defaultdict(Q)
    quotient_owner = {}
    selection_histogram = Counter()
    all_triples = list(it.product(range(15), repeat=3))
    for row in all_triples:
        cells = {(c, edge) for c, mi in enumerate(row) for edge in ms[mi]}
        require(len(cells) == 9, "target monomial must have nine distinct variables")
        candidates = {}
        for matching in ms:
            palettes = [[c for c in range(3) if edge in sets[row[c]]] for edge in matching]
            for colors in it.product(*palettes):
                if len(set(colors)) < 2:
                    continue
                word = [None] * 6
                for edge, color in zip(matching, colors):
                    for v in edge:
                        word[v] = color
                word = tuple(word)
                used = set(zip(colors, matching))
                quotient = tuple(sorted(c * 15 + edge_id[e] for c, e in cells - used))
                require(len(quotient) == 6 and len(set(quotient)) == 6,
                        "quotient must have six distinct variables")
                require(word not in candidates, "one word must determine its matching in this union")
                candidates[word] = quotient
        chosen = [word for word in candidates if len(set(word)) == 3] or list(candidates)
        require(bool(chosen), "a triple of pure matchings had no mixed matching")
        selection_histogram[len(set(chosen[0])), len(chosen)] += 1
        weight = Q(1, len(chosen))
        for word in chosen:
            quotient = candidates[word]
            if quotient in quotient_owner:
                require(quotient_owner[quotient] == word, "quotient must determine missing colors")
            quotient_owner[quotient] = word
            word_totals[word] += weight
            quotient_coefficients[quotient] += weight

    totals = Counter((len(set(word)), value) for word, value in word_totals.items())
    require(totals == Counter({(2, Q(17)): 90, (3, Q(41, 2)): 90}), "word multiplicities")
    weighted_max = max(word_totals[quotient_owner[q]] * alpha
                       for q, alpha in quotient_coefficients.items())
    require(weighted_max == Q(41, 2), "wrong coefficient in norm estimate")
    # The expansion of (sum a_i^2)^6 contains every squarefree six-variable
    # monomial with coefficient 6!=720. All its other terms are nonnegative.
    B_squared = weighted_max / 720
    require(B_squared == Q(41, 1440), "wrong nonnegative rate constant")
    require(sum(word_totals.values(), Q(0)) == 3375, "cover must count every target term once")

    # Scope guard: two diagonal contributions to aabbbb can cancel.
    # a_01=1; b_23=b_45=b_24=1; b_35=-1; all other cells zero.
    weights = {(0, (0, 1)): Q(1), (1, (2, 3)): Q(1), (1, (4, 5)): Q(1),
               (1, (2, 4)): Q(1), (1, (3, 5)): Q(-1)}
    terms = []
    for remainder in matchings((2, 3, 4, 5)):
        value = weights[0, (0, 1)]
        for edge in remainder:
            value *= weights.get((1, edge), Q(0))
        terms.append(value)
    require(sum(terms) == 0 and Q(1) in terms and Q(-1) in terms,
            "negative-weight cancellation guard")
    return {"pure_matching_triples": len(all_triples), "mixed_words": len(word_totals),
            "quotient_monomials": len(quotient_coefficients),
            "word_totals": {"two_colors": "17", "three_colors": "41/2"},
            "maximum_weighted_quotient": str(weighted_max), "B_squared": str(B_squared),
            "selection_histogram": {f"{kind}_colors_{count}_choices": value
                                    for (kind, count), value in sorted(selection_histogram.items())},
            "negative_weight_guard": "PASS"}


def check_conversion():
    values = {}
    for m in (3, 4, 5):
        s = Q(3 * m, 4)
        require(Q(m) / s - 1 / (1 - s / (3 * m)) == 0, "Gaussian prefactor stationary point")
        value = s ** m * (1 - s / (3 * m)) ** (3 * m)
        require(value == Q(81 * m, 256) ** m, "Gaussian prefactor value")
        values[str(2 * m)] = str(value)
    require(Q(values["6"]) == Q(243, 256) ** 3, "six-site conversion")
    require(Q(values["6"]) ** 2 * Q(123, 160) < Q(3, 4) ** 2,
            "rounded-up physical rate constant 3/4")
    return values


def check_prism_tangent(ms):
    model = json.loads((ROOT / "computations/useful-consequences-2026-09-26/prism.json").read_text())
    word = tuple("bcabca")
    edges = {tuple(e["ends"]): e for e in model["edges"]}
    constant_edges = [e for e in model["edges"] if e["omega_power"] == 0]
    require(len(constant_edges) == 6, "prism base must have six constant edges")
    for e in constant_edges:
        require(not all(word[v] == e["color"] for v in e["ends"]),
                "a constant edge is compatible with the protected mixed word")
    expansion = defaultdict(Counter)
    for matching in ms:
        if not all(pair in edges for pair in matching):
            continue
        colors = [None] * 6
        degree = 0
        for pair in matching:
            edge = edges[pair]
            for v in pair:
                colors[v] = edge["color"]
            degree += edge["omega_power"]
        expansion[tuple(colors)][degree] += 1
    expected = {tuple(c * 6): Counter({1: 1}) for c in "abc"}
    expected[word] = Counter({3: 1})
    require(dict(expansion) == expected, "prism tangent and protected coefficient")
    return {"constant_edges_incompatible_with_word": 6, "protected_word": "bcabca",
            "protected_cubic_coefficient": 1,
            "scope": "Fixed A0 and A1; arbitrary analytic terms starting at order two."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a new JSON receipt; refuses overwrite")
    args = parser.parse_args()
    vertices, edges, ms, lookup = setup()
    data = json.loads((HERE / "dual.json").read_text())
    report = {"status": "PASS", "evidence_status": "NEW RESEARCH; NOT INDEPENDENTLY AUDITED",
              "complex_cubic_product_identity": check_dual(data, vertices, lookup),
              "nonnegative_bound": check_positive_cover(vertices, edges, ms),
              "gaussian_conversion_factors": check_conversion(),
              "prism_tangent": check_prism_tangent(ms)}
    bad = copy.deepcopy(data)
    bad["functional"][0]["value"] *= -1
    try:
        check_dual(bad, vertices, lookup)
    except ValueError:
        report["dual_mutation"] = "REJECTED"
    else:
        raise ValueError("corrupt dual accepted")
    report["dual_sha256"] = hashlib.sha256((HERE / "dual.json").read_bytes()).hexdigest()
    report["six_site_proof_sha256"] = hashlib.sha256(
        (ROOT / "proofs/six-site-arbitrary-complex-obstruction.md").read_bytes()).hexdigest()
    report["generic_six_site_exponent_denominator_cap"] = str(3 ** 135 - 1)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x") as handle:
            handle.write(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
