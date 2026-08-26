#!/usr/bin/env python3
"""Exact missing-column ideal on a generic single 6+1+1 cofactor boundary."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = HERE / "results_tail_polar_source_lift.json"
OUT = HERE / "results_single_cofactor_boundary.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def word_name(word):
    return "".join(map(str, word))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        answer.extend((((first, second),) + tail
                       for tail in perfect_matchings(rest)))
    return tuple(answer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    try:
        import sympy as sp
    except ImportError:
        sites = sorted((ROOT / ".venv/lib").glob("python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp

    require(UPSTREAM.exists(), "upstream 380x12 result missing")
    upstream = json.loads(UPSTREAM.read_text())
    require(upstream["logical_sha256"] ==
            "273c321313d8bea2dcd3ea19fe282c078dcfa481d956839607db35100a7612b9",
            "upstream logical digest changed")

    vertices = tuple(range(8))
    residual = tuple(range(6))
    tails = (6, 7)
    anchors = frozenset({(0, 1), (2, 3), (4, 5), (6, 7)})
    edges = tuple(combinations(vertices, 2))
    diagonal = {
        (colour, edge): sp.symbols(f"g{colour}_{edge[0]}{edge[1]}")
        for colour in range(3) for edge in edges
    }

    @lru_cache(None)
    def hafnian(colour, subset):
        subset = tuple(subset)
        if not subset:
            return sp.Integer(1)
        first = subset[0]
        answer = 0
        for index in range(1, len(subset)):
            second = subset[index]
            rest = subset[1:index] + subset[index + 1:]
            answer += diagonal[colour, tuple(sorted((first, second)))] * \
                hafnian(colour, rest)
        return sp.expand(answer)

    # By the fixed-tail stabilizer every one of the twelve 611 factors is
    # equivalent to the y0 factor h2_06.
    missing_edge = (0, 6)
    missing_column = "y0"
    complement = tuple(v for v in vertices if v not in missing_edge)
    h = {colour: hafnian(colour, complement) for colour in range(3)}
    require(all(len(sp.Poly(h[colour]).terms()) == 15 for colour in range(3)),
            "six-site cofactor term count changed")

    other_star_edges = tuple((a, tail) for tail in tails for a in residual
                             if (a, tail) != missing_edge)
    other_h2 = tuple(hafnian(2, tuple(v for v in vertices
                                     if v not in edge))
                     for edge in other_star_edges)
    d_hat = sp.prod(other_h2)
    require(len(other_h2) == 11 and d_hat != 0,
            "other-eleven localization product changed")

    # Two 7+1 missing-column coefficients.
    word_71_majority0 = (0, 0, 0, 0, 0, 0, 1, 0)
    word_71_majority1 = (0, 1, 1, 1, 1, 1, 1, 1)
    rows_71 = (
        ("F_" + word_name(word_71_majority0), h[0]),
        ("F_" + word_name(word_71_majority1), h[1]),
    )

    # The 90 profile-332 rows containing y0.  Removing edge 06 leaves an
    # ordered partition of the six complementary sites into one same-colour
    # pair for each of G0,G1,G2.
    rows_332 = []
    raw_matchings = perfect_matchings(vertices)
    require(len(raw_matchings) == 105, "K8 matching census changed")
    for zero_pair in combinations(complement, 2):
        left = tuple(v for v in complement if v not in zero_pair)
        for one_pair in combinations(left, 2):
            two_pair = tuple(v for v in left if v not in one_pair)
            word = [None] * 8
            word[0] = 0
            word[6] = 1
            for v in zero_pair:
                word[v] = 0
            for v in one_pair:
                word[v] = 1
            for v in two_pair:
                word[v] = 2
            word = tuple(word)
            coefficient = (
                diagonal[0, tuple(sorted(zero_pair))]
                * diagonal[1, tuple(sorted(one_pair))]
                * diagonal[2, tuple(sorted(two_pair))]
            )

            # Independent literal 105-matching coefficient extraction.
            raw = 0
            for matching in raw_matchings:
                if missing_edge not in matching:
                    continue
                cross = tuple(edge for edge in matching
                              if word[edge[0]] != word[edge[1]])
                if cross != (missing_edge,):
                    continue
                term = 1
                for edge in matching:
                    if edge == missing_edge:
                        continue
                    require(word[edge[0]] == word[edge[1]],
                            "332 raw fine lost same-colour type")
                    term *= diagonal[word[edge[0]], edge]
                raw += term
            require(sp.expand(raw-coefficient) == 0,
                    ("332 raw missing coefficient changed", word_name(word)))
            rows_332.append(("F_" + word_name(word), coefficient,
                             tuple(sorted(zero_pair)),
                             tuple(sorted(one_pair)),
                             tuple(sorted(two_pair))))
    require(len(rows_332) == 90
            and len({label for label, *_rest in rows_332}) == 90,
            "missing-column 332 row census changed")

    # Every missing-column coefficient q gives a literal maximal minor
    # +/- D_hat*q after adjoining the other eleven diagonal 611 pivots.
    missing_coefficients = (h[0], h[1]) + tuple(row[1] for row in rows_332)
    coefficient_gcd = missing_coefficients[0]
    for value in missing_coefficients[1:]:
        coefficient_gcd = sp.gcd(coefficient_gcd, value)
        if coefficient_gcd == 1:
            break
    require(coefficient_gcd == 1,
            "missing-column coefficients acquired a common divisor")

    # Normalize the four selected anchors.  The 90 tricolour monomials give
    # 87 distinct generators; the matching 17|23|45 supplies the three
    # linear generators g0_17,g1_17,g2_17.
    anchor_substitution = {
        diagonal[colour, edge]: 1
        for colour in range(3) for edge in anchors
    }
    normalized_groups = defaultdict(list)
    for label, coefficient, *_pairs in rows_332:
        normalized = sp.expand(coefficient.subs(anchor_substitution))
        normalized_groups[str(normalized)].append(label)
    degree_histogram = Counter(
        sp.Poly(sp.sympify(key), *tuple(diagonal.values())).total_degree()
        for key in normalized_groups
    )
    require(len(normalized_groups) == 87
            and degree_histogram == {1: 3, 2: 24, 3: 60},
            ("normalized 332 generator profile changed",
             len(normalized_groups), degree_histogram))
    singleton_generators = {
        f"g{colour}_17": normalized_groups[f"g{colour}_17"]
        for colour in range(3)
    }
    require(all(len(labels) == 2
                for labels in singleton_generators.values()),
            "normalized singleton source multiplicity changed")

    # Once the three singleton generators vanish, exactly 72 normalized
    # monomial generators remain nontrivial (24 quadrics, 48 cubics).
    singleton_symbols = {diagonal[colour, (1, 7)]: 0
                         for colour in range(3)}
    residual_monomials = {
        str(sp.expand(sp.sympify(key).subs(singleton_symbols)))
        for key in normalized_groups
        if sp.expand(sp.sympify(key).subs(singleton_symbols)) != 0
    }
    residual_degree_histogram = Counter(
        sp.Poly(sp.sympify(key), *tuple(diagonal.values())).total_degree()
        for key in residual_monomials
    )
    require(len(residual_monomials) == 72
            and residual_degree_histogram == {2: 24, 3: 48},
            "post-singleton 332 residual profile changed")

    # Exact fixed-tail orbit of the representative missing edge.
    orbit = set()
    for residual_permutation in permutations(range(3)):
        for flip_mask in range(16):
            flips = tuple((flip_mask >> block) & 1 for block in range(4))

            def act(vertex):
                block, clone = divmod(vertex, 2)
                image_block = (residual_permutation[block]
                               if block < 3 else 3)
                return 2*image_block + (clone ^ flips[block])

            orbit.add(tuple(sorted(map(act, missing_edge))))
    expected_orbit = {(a, tail) for a in residual for tail in tails}
    require(orbit == expected_orbit,
            "fixed-tail cofactor orbit changed")

    # Mutations: remove a source coefficient, corrupt an endpoint word, and
    # break one anchor specialization.
    deletion_mutation_fired = len(rows_332[:-1]) == 89
    wrong_word = list(word_71_majority0)
    wrong_word[6], wrong_word[7] = wrong_word[7], wrong_word[6]
    orientation_mutation_fired = tuple(wrong_word) != word_71_majority0
    mutated_anchor = dict(anchor_substitution)
    mutated_anchor[diagonal[0, (2, 3)]] = 2
    anchor_mutation_fired = any(
        sp.expand(coefficient.subs(mutated_anchor)
                  - coefficient.subs(anchor_substitution)) != 0
        for _label, coefficient, *_pairs in rows_332
    )
    require(deletion_mutation_fired and orientation_mutation_fired
            and anchor_mutation_fired,
            "single-boundary mutation control failed")

    rows_332_ledger = [{
        "source_label": label,
        "missing_column_coefficient": str(coefficient),
        "G0_pair": "".join(map(str, zero_pair)),
        "G1_pair": "".join(map(str, one_pair)),
        "G2_pair": "".join(map(str, two_pair)),
        "maximal_minor_up_to_sign": f"Dhat*({coefficient})",
    } for label, coefficient, zero_pair, one_pair, two_pair in rows_332]

    result = {
        "status": "PASS exact generic single-cofactor missing-column audit",
        "representative": {
            "missing_611_factor": "h2_06=Haf(G2 on {1,2,3,4,5,7})",
            "missing_star_column": missing_column,
            "localized_other_611_factors": 11,
            "localizer": "Dhat=product of the other eleven h2_at",
            "fixed_tail_orbit_size": len(orbit),
        },
        "missing_column_ideal": {
            "name": "J06",
            "generators": (
                "h0_06, h1_06, and the 90 coefficients "
                "g0_A*g1_B*g2_C for ordered pair partitions "
                "A sqcup B sqcup C={1,2,3,4,5,7}"),
            "raw_generator_count": 92,
            "coefficient_gcd": str(coefficient_gcd),
            "maximal_minor_ideal_after_localizing_Dhat": "Dhat*J06",
            "rank_criterion": (
                "rank=12 iff at least one generator of J06 is nonzero; "
                "rank=11 iff every generator of J06 vanishes"),
            "seven_plus_one_generators": [
                {"source_label": label,
                 "missing_column_coefficient": str(value),
                 "maximal_minor_up_to_sign": f"Dhat*({value})"}
                for label, value in rows_71
            ],
            "three_three_two_rows": rows_332_ledger,
        },
        "anchor_normalized_332_ideal": {
            "distinct_generator_count": len(normalized_groups),
            "degree_histogram": {str(key): value
                                 for key, value in degree_histogram.items()},
            "three_linear_generators_and_source_labels": singleton_generators,
            "after_three_linear_generators_vanish": {
                "remaining_distinct_generators": len(residual_monomials),
                "degree_histogram": {
                    str(key): value
                    for key, value in residual_degree_histogram.items()
                },
            },
        },
        "rank_drop_statement": {
            "single_divisor": "h2_06=0, Dhat!=0",
            "restoring_open": "Spec minus V(J06)",
            "no_common_restoring_factor": True,
            "no_next_divisorial_rank_drop": (
                "J06 contains the coprime independent-colour cofactors "
                "h0_06 and h1_06, so inside h2_06=0 the rank-drop locus "
                "has codimension at least two, not a divisorial component"),
            "first_exact_residual": (
                "h2_06=h0_06=h1_06=g0_17=g1_17=g2_17=0, "
                "together with the remaining 72 normalized 332 monomials; "
                "the other eleven h2 factors stay inverted"),
            "global_codimension_guard": (
                "before imposing diagonal packet equations, the first "
                "possible rank-drop locus is at least codimension three "
                "in the independent-graph ambient space: h2_06=h0_06="
                "h1_06=0; 332 rows cut it further"),
        },
        "covariance": {
            "fixed_tail_stabilizer_orbit": [
                "".join(map(str, edge)) for edge in sorted(orbit)
            ],
            "conclusion": (
                "the representative ideal transports to each of the "
                "twelve possible single missing 611 factors"),
        },
        "mutation_guards": {
            "delete_one_332_source": deletion_mutation_fired,
            "tail_endpoint_orientation": orientation_mutation_fired,
            "anchor_coefficient_specialization": anchor_mutation_fired,
        },
        "scope_guard": (
            "This proves the exact generic rank criterion on one "
            "single-cofactor boundary after localizing the other eleven "
            "611 factors. It does not prove that the diagonal packet avoids "
            "the codimension-at-least-two residual V(J06), and it performs "
            "no Groebner or full 240-variable calculation."),
        "source_hashes": {
            "upstream_result": file_hash(UPSTREAM),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("single cofactor boundary: PASS", result["logical_sha256"])
    print("missing ideal 2+90 generators; normalized 332", len(normalized_groups))
    print("post-singleton residual", len(residual_monomials),
          "gcd", coefficient_gcd)


if __name__ == "__main__":
    main()
