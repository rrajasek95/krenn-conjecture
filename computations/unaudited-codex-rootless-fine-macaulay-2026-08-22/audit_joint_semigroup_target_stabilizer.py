#!/usr/bin/env python3
"""Audit target symmetry before any 37-coordinate isotypic compression."""

from itertools import permutations, product
from pathlib import Path
from collections import defaultdict
import argparse
import hashlib
import json
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_colour_holonomy_quotients import semigroup_key
from audit_physical_graph_quotient import SLICES, T_EDGES, holonomy


RESULTS = HERE / "results_joint_semigroup_target_stabilizer.json"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def parity(perm):
    return -1 if sum(
        perm[i] > perm[j]
        for i in range(len(perm)) for j in range(i + 1, len(perm))
    ) % 2 else 1


def transform_word(word, site_perm, colour_perm):
    out = [None] * 8
    for site, colour in enumerate(word):
        out[site_perm[site]] = colour_perm[colour]
    return tuple(out)


def canonical_cell(u, v, a, b):
    return (u, v, a, b) if u < v else (v, u, b, a)


def transform_term(term, site_perm, colour_perm):
    return tuple(sorted(
        canonical_cell(
            site_perm[u], site_perm[v], colour_perm[a], colour_perm[b]
        )
        for u, v, a, b in term
    ))


def source_datum_stabilizer():
    edges = tuple(T_EDGES)
    slices = tuple(tuple(word) for word in SLICES)
    out = []
    for site_perm in permutations(range(8)):
        if set(site_perm[:3]) != {0, 1, 2}:
            continue
        edge_perm = []
        for u, v in edges:
            image = tuple(sorted((site_perm[u], site_perm[v])))
            if image not in edges:
                break
            edge_perm.append(edges.index(image))
        else:
            for colour_perm in permutations(range(3)):
                row_perm = []
                for word in slices:
                    image = transform_word(word, site_perm, colour_perm)
                    if image not in slices:
                        break
                    row_perm.append(slices.index(image))
                else:
                    sign = parity(row_perm) * parity(edge_perm)
                    reversals = tuple(
                        site_perm[u] > site_perm[v]
                        for u in range(8) for v in range(u + 1, 8)
                    )
                    out.append({
                        "site_permutation": site_perm,
                        "colour_permutation": colour_perm,
                        "slice_permutation": tuple(row_perm),
                        "selected_edge_permutation": tuple(edge_perm),
                        "sign": sign,
                        "uniform_edge_orientation_reversal": (
                            len(set(reversals)) == 1
                        ),
                        "reversals": reversals,
                    })
    return out


def transform_poly(poly, element):
    out = defaultdict(int)
    for term, coefficient in poly.items():
        image = transform_term(
            term, element["site_permutation"], element["colour_permutation"]
        )
        out[image] += coefficient
        if not out[image]:
            del out[image]
    return dict(out)


def descent_counterexample(element):
    edges = tuple((u, v) for u in range(8) for v in range(u + 1, 8))
    false_edge = next(
        edge for edge, reversed_ in zip(edges, element["reversals"])
        if not reversed_
    )
    true_edge = next(
        edge for edge, reversed_ in zip(edges, element["reversals"])
        if reversed_
    )
    terms = []
    for first_pair, second_pair in (((0, 1), (1, 0)), ((1, 0), (0, 1))):
        terms.append(tuple(sorted((
            canonical_cell(*false_edge, *first_pair),
            canonical_cell(*true_edge, *second_pair),
        ))))
    before = [semigroup_key(term) for term in terms]
    after_terms = [transform_term(
        term, element["site_permutation"], element["colour_permutation"]
    ) for term in terms]
    after = [semigroup_key(term) for term in after_terms]
    require(before[0] == before[1], "counterexample inputs have different keys")
    require(after[0] != after[1], "counterexample outputs have the same key")
    return {
        "same_input_key": before[0],
        "first_literal_term": terms[0],
        "second_literal_term": terms[1],
        "first_transformed_key": after[0],
        "second_transformed_key": after[1],
        "one_nonreversed_edge": false_edge,
        "one_reversed_edge": true_edge,
    }


def word_sets():
    closure22 = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    words = set(closure22)
    for word in product(range(3), repeat=8):
        counts = sorted(word.count(colour) for colour in set(word))
        if counts in ([1, 7], [2, 6]):
            words.add("".join(map(str, word)))
    return closure22, words


def audit():
    datum_stabilizer = source_datum_stabilizer()
    require(len(datum_stabilizer) == 12, len(datum_stabilizer))
    require(all(item["sign"] == 1 for item in datum_stabilizer), "nontrivial sign")
    require(all(item["colour_permutation"] == (0, 1, 2)
                for item in datum_stabilizer), "unexpected colour action")
    require(all(item["site_permutation"][:3] == (0, 1, 2)
                for item in datum_stabilizer), "triangle not fixed pointwise")
    require(all(set(item["site_permutation"][3:5]) == {3, 4}
                and set(item["site_permutation"][5:]) == {5, 6, 7}
                for item in datum_stabilizer), "not S2 x S3 on tail")

    unconed = holonomy()
    cone = ((0, 1, 0, 0), (2, 3, 0, 0), (4, 5, 0, 0), (6, 7, 0, 0))
    target = defaultdict(int)
    for term, coefficient in unconed.items():
        image = tuple(sorted(cone + term))
        target[image] += coefficient
        if not target[image]:
            del target[image]
    target = dict(target)
    stabilizer = [
        element for element in datum_stabilizer
        if transform_poly(target, element) == {
            term: element["sign"] * coefficient
            for term, coefficient in target.items()
        }
    ]
    require(len(stabilizer) == 2, len(stabilizer))
    equivariant = []
    descending = []
    counterexamples = []
    for index, element in enumerate(stabilizer):
        expected = {
            term: element["sign"] * coefficient
            for term, coefficient in target.items()
        }
        require(transform_poly(target, element) == expected,
                f"target equivariance failed at {index}")
        equivariant.append(index)
        if element["uniform_edge_orientation_reversal"]:
            descending.append(index)
        else:
            counterexamples.append({
                "stabilizer_index": index,
                **descent_counterexample(element),
            })
    require(descending == [0], descending)
    require(len(counterexamples) == 1, len(counterexamples))

    closure22, module_words = word_sets()
    missing = set()
    nonclosed_seeds = {}
    for label in sorted(module_words):
        orbit = set()
        for element in stabilizer:
            image = transform_word(
                tuple(map(int, label)), element["site_permutation"],
                element["colour_permutation"]
            )
            orbit.add("".join(map(str, image)))
        absent = sorted(orbit - module_words)
        if absent:
            nonclosed_seeds[label] = absent
            missing.update(absent)
    require(len(module_words) == 221, len(module_words))
    require(sorted(missing) == ["21111101"],
            sorted(missing))

    result = {
        "status": "NO-GO nontrivial target stabilizer does not act on 37-coordinate quotient",
        "literal_unconed_holonomy_terms": len(unconed),
        "literal_coned_target_terms": len(target),
        "unconed_source_datum_stabilizer_order": len(datum_stabilizer),
        "unconed_source_datum_stabilizer_structure": "S2({3,4}) x S3({5,6,7})",
        "literal_target_stabilizer_order": len(stabilizer),
        "literal_target_stabilizer_structure": "S2({6,7})",
        "target_character": "trivial",
        "exact_target_equivariance_checks": len(equivariant),
        "quotient_descending_elements": len(descending),
        "quotient_descending_indices": descending,
        "nonidentity_descent_counterexamples": len(counterexamples),
        "counterexamples": counterexamples,
        "profile71_profile62_module_words": len(module_words),
        "module_is_literal_H_stable": not missing,
        "missing_words_for_literal_H_closure": sorted(missing),
        "nonclosed_seed_orbits": nonclosed_seeds,
        "closure22_words": closure22,
        "compression_factor_available_on_joint_quotient": 1,
        "conclusion": (
            "The coned literal holonomy target has stabilizer S2({6,7}) and "
            "trivial character, but its nonidentity element reverses some physical "
            "edge orientations and preserves others. Two literal monomials "
            "can therefore have the same physical-edge plus global ordered-"
            "colour-pair key and different transformed keys. There is no "
            "nontrivial action on the 37-coordinate semigroup columns, so "
            "signed orbit-sum/isotypic compression of the abstract exchange "
            "matrix is not defined."
        ),
        "scope": (
            "Exact exhaustive S8 x S3 audit of automorphisms of the three "
            "slice words and selected triangle edges, followed by the frozen "
            "pure-cone multiplication and literal target replay. No rank solve was run."
        ),
    }
    result["logical_sha256"] = hashlib.sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored stabilizer audit changed")
    print(json.dumps({
        key: value for key, value in result.items()
        if key not in ("counterexamples", "closure22_words", "nonclosed_seed_orbits")
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
