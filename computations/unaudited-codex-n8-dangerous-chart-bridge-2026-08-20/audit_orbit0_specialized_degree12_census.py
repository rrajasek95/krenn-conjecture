#!/usr/bin/env python3
"""Exact input census for the orbit-0 anchors=1 degree-12 Macaulay test."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPORT_PATH = HERE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("specialized_orbit0", EXPORT_PATH)
ORBIT0 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ORBIT0)
BASE = ORBIT0.BASE
OUT = HERE / "results_orbit0_specialized_degree12_census.json"


def specialized(term: bytes) -> bytes:
    return bytes(cell for cell in term if cell not in ORBIT0.ANCHORS)


def main() -> None:
    generator_global_support = set()
    generator_degree_occurrences = Counter()
    generator_word_histograms = Counter()
    constant_words = []
    within_word_collisions = 0
    for word in product(BASE.COLORS, repeat=BASE.N):
        if len(set(word)) == 1:
            continue
        terms = [specialized(term) for term in BASE.word_terms(word)]
        counts = Counter(terms)
        within_word_collisions += len(terms) - len(counts)
        histogram = tuple(sorted(Counter(map(len, counts)).items()))
        generator_word_histograms[histogram] += 1
        generator_global_support.update(counts)
        generator_degree_occurrences.update(map(len, terms))
        if b"" in counts:
            constant_words.append("".join(map(str, word)))
    if within_word_collisions or len(constant_words) != 78:
        raise RuntimeError("specialized generator term census changed")

    pure_terms = [[specialized(term) for term in BASE.word_terms((colour,) * 8)]
                  for colour in BASE.COLORS]
    target = set()
    for left in pure_terms[0]:
        for middle in pure_terms[1]:
            prefix = left + middle
            for right in pure_terms[2]:
                target.add(bytes(sorted(prefix + right)))
    if len(target) != 105 ** 3:
        raise RuntimeError("specialized pure target acquired a collision")

    unseen = set(target)
    orbit_degree_histogram = Counter()
    orbit_size_histogram = Counter()
    while unseen:
        row = unseen.pop()
        orbit = {bytes(sorted(transform[cell] for cell in row))
                 for transform in ORBIT0.TRANSFORMS}
        if not orbit <= target:
            raise RuntimeError("specialized target is not invariant")
        unseen.difference_update(orbit)
        orbit_degree_histogram[len(row)] += 1
        orbit_size_histogram[len(orbit)] += 1

    result = {
        "status": "UNAUDITED exact orbit0 anchors=1 input census",
        "exporter_sha256": sha256(EXPORT_PATH.read_bytes()).hexdigest(),
        "stabilizer_order": len(ORBIT0.TRANSFORMS),
        "specialized_variables": len(BASE.CELLS) - len(ORBIT0.ANCHORS),
        "mixed_generators": 3 ** 8 - 3,
        "terms_per_generator_before_specialization": 105,
        "generator_term_occurrences": sum(generator_degree_occurrences.values()),
        "generator_global_distinct_monomials": len(generator_global_support),
        "generator_within_word_collisions": within_word_collisions,
        "generator_term_degree_occurrence_histogram": {
            str(k): v for k, v in sorted(generator_degree_occurrences.items())
        },
        "generator_word_degree_histograms": {
            str(histogram): count for histogram, count
            in sorted(generator_word_histograms.items())
        },
        "constant_term_generators": len(constant_words),
        "constant_term_words_sample": constant_words[:6],
        "target_labelled_support": len(target),
        "target_coefficients_all_one": True,
        "target_degree_support_histogram": {
            str(k): v for k, v in sorted(Counter(map(len, target)).items())
        },
        "target_quotient_orbits": sum(orbit_degree_histogram.values()),
        "target_orbit_degree_histogram": {
            str(k): v for k, v in sorted(orbit_degree_histogram.items())
        },
        "target_orbit_size_histogram": {
            str(k): v for k, v in sorted(orbit_size_histogram.items())
        },
        "bounded_macaulay_columns": (
            "Homogenize H_w to degree 4 with t and T to degree 12. Columns "
            "are H_w^h*U with U homogeneous of degree 8. After t=1, a basis "
            "column is H_w*u for a nonanchor monomial u of degree at most 8; "
            "the omitted t exponent is 8-degree(u)."
        ),
        "closure_rule": (
            "From a row r, enumerate specialized H_w terms g dividing r; "
            "the incident column is H_w*(r/g). Closing this bipartite "
            "component is exact for the bounded degree<=12 Macaulay matrix."
        ),
        "homogenization_guard": (
            "A specialized row of nonanchor degree d represents its unique "
            "degree-12 homogenization t^(12-d)*row. One must not allow "
            "multipliers of nonanchor degree above 8 and discard their high "
            "outputs; that naive truncation would falsely make a generator "
            "with constant term look like a unit."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 specialized degree12 census: PASS")
    print("target labelled/orbits:", len(target),
          sum(orbit_degree_histogram.values()))
    print("generator occurrences/distinct:",
          sum(generator_degree_occurrences.values()), len(generator_global_support))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
