#!/usr/bin/env python3
"""Exact natural-order factorized B20=(K20,K22,K23,K24) Gram provider."""
from collections import Counter
from functools import lru_cache
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL_PROVIDER = ROOT / "computations/unaudited-codex-orbit0-k24-relative-column-interface-gate-2026-08-24/k24_relative_column_provider.py"
FULL_PROVIDER_SHA = "bc69f705fea1aad120a622055d25687b22e12ac6141bd47166274d16f47fb3cd"
DEGREES = (20, 22, 23, 24)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_full_provider():
    need(sha(FULL_PROVIDER) == FULL_PROVIDER_SHA, "full-provider hash")
    spec = importlib.util.spec_from_file_location("factorized_B20_full_provider", FULL_PROVIDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


F = load_full_provider()
P = F.P


@lru_cache(None)
def fast_natural_canonical_and_orbit_size(column):
    word, multiplier = column
    word_images = [(action, P.move_word(word, action)) for action in P.H]
    minimum_word = min(image for _action, image in word_images)
    fibre_actions = [action for action, image in word_images if image == minimum_word]
    fibre_multipliers = {
        bytes(sorted(P.F.EXPORT.TRANSFORMS[action][cell] for cell in multiplier))
        for action in fibre_actions
    }
    word_orbit_size = len({image for _action, image in word_images})
    representative = (minimum_word, min(fibre_multipliers))
    orbit_size = word_orbit_size * len(fibre_multipliers)
    return representative, orbit_size, word_orbit_size, len(fibre_actions), len(fibre_multipliers)


@lru_cache(None)
def natural_orbit(column):
    return tuple(sorted({P.move_column(column, action) for action in P.H}))


@lru_cache(None)
def literal_block_counters(column):
    counters = {degree: Counter() for degree in DEGREES}
    rows = P.D24.degree24_column_rows(column)
    need(len(rows) == 105, "matching-term census")
    for row in rows:
        degree = P.D24.row_k_degree(row)
        need(degree in DEGREES, f"B20 column escaped local blocks: K{degree}")
        counters[degree][row] += 1
    return tuple((degree, counters[degree]) for degree in DEGREES)


def block_counter(column, degree):
    return dict(literal_block_counters(column))[degree]


def literal_dot(left, right, degree):
    a = block_counter(left, degree)
    b = block_counter(right, degree)
    return sum(value * b.get(row, 0) for row, value in a.items())


def orbit_block_gram(left, right):
    """Exact Gram of unnormalised H-orbit-sum columns, no row canonicalization.

    By H-invariance, sum over the left orbit is |Orb(left)| times the
    pairing of one left representative with the entire right orbit.
    """
    left_rep, left_size, *_ = fast_natural_canonical_and_orbit_size(left)
    right_rep, right_size, *_ = fast_natural_canonical_and_orbit_size(right)
    right_orbit = natural_orbit(right_rep)
    need(len(right_orbit) == right_size, "right orbit-size theorem")
    answer = {}
    for degree in DEGREES:
        answer[degree] = left_size * sum(literal_dot(left_rep, moved, degree) for moved in right_orbit)
    # Symmetry is a load-bearing cross-check of the orbit formula.
    left_orbit = natural_orbit(left_rep)
    need(len(left_orbit) == left_size, "left orbit-size theorem")
    for degree in DEGREES:
        reverse = right_size * sum(literal_dot(right_rep, moved, degree) for moved in left_orbit)
        need(answer[degree] == reverse, f"block Gram asymmetry K{degree}")
    return answer


def term_table_descriptor(word):
    terms = tuple(P.D24.BASE.word_terms(word))
    need(len(terms) == 105, "word term table")
    rows = [{"matching_term": term.hex(), "K_degree": P.D24.row_k_degree(term)} for term in terms]
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    histogram = Counter(item["K_degree"] for item in rows)
    return rows, hashlib.sha256(payload).hexdigest(), dict(sorted(histogram.items()))


def column_descriptor(column):
    representative, orbit_size, word_orbit_size, fibre_actions, fibre_multipliers = fast_natural_canonical_and_orbit_size(column)
    brute = natural_orbit(column)
    need(representative == brute[0] and orbit_size == len(brute), "fast natural canonical theorem")
    terms, term_hash, term_histogram = term_table_descriptor(representative[0])
    multiplier_K = P.D24.row_k_degree(representative[1])
    need(multiplier_K == 20, "B20 requires anchor-free K20 multiplier")
    output_histogram = {str(multiplier_K + key): value for key, value in term_histogram.items()}
    need(set(map(int, output_histogram)) == set(DEGREES), "B20 output degrees")
    return {
        "natural_column_key": P.column_key(representative),
        "column_orbit_size": orbit_size,
        "column_stabilizer_size": len(P.H) // orbit_size,
        "natural_word": "".join(map(str, representative[0])),
        "word_orbit_size": word_orbit_size,
        "minimum_word_fibre_actions": fibre_actions,
        "minimum_word_fibre_multiplier_images": fibre_multipliers,
        "multiplier_K_degree": multiplier_K,
        "shared_word_term_table_sha256": term_hash,
        "shared_word_term_count": len(terms),
        "output_degree_histogram": output_histogram,
        "sparse_B_record_semantics": "row outputs are reconstructed as sorted(multiplier + shared_word_matching_term); no row is stored in the column record",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--column-key", required=True)
    parser.add_argument("--exhaustive-vector", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    vector_path = args.exhaustive_vector if args.exhaustive_vector.is_absolute() else ROOT / args.exhaustive_vector
    output = args.output if args.output.is_absolute() else ROOT / args.output
    column = P.parse_column_key(args.column_key)
    begun = perf_counter()
    descriptor = column_descriptor(column)
    gram = orbit_block_gram(column, column)
    elapsed = perf_counter() - begun
    exhaustive = Counter()
    lines = vector_path.read_text().splitlines()
    need(len(lines) == 106, "exhaustive bounded vector shape")
    for line in lines[1:]:
        fields = line.split("\t")
        degree, orbit_size, mass = int(fields[0]), int(fields[2]), int(fields[3])
        need(mass % orbit_size == 0, "exhaustive orbit division")
        exhaustive[degree] += mass * mass // orbit_size
    need(dict(gram) == dict(exhaustive), "factorized/exhaustive block Gram equivalence")
    lower_gram = sum(gram[degree] for degree in (20, 22, 23))
    top_gram = gram[24]
    need(lower_gram > 0 and top_gram > 0, "nonzero bounded blocks")
    result = {
        "status": "PASS_BOUNDED_FACTORIZED_K24_B20_EQUIVALENCE",
        "degree": 24,
        "format": "orbit0-factorized-B20-column-orbit-v1",
        "canonical_order_id": "natural_word_tuple_then_multiplier_bytes_v1",
        "H_order": len(P.H),
        "column": descriptor,
        "factorized_block_gram": {str(key): str(value) for key, value in sorted(gram.items())},
        "exhaustive_orbit_mass_block_gram": {str(key): str(value) for key, value in sorted(exhaustive.items())},
        "lower_gram_K20_K22_K23": str(lower_gram),
        "top_gram_K24": str(top_gram),
        "factorized_equals_exhaustive": True,
        "factorized_elapsed_seconds": elapsed,
        "exhaustive_control_vector_sha256": sha(vector_path),
        "full_provider_sha256": FULL_PROVIDER_SHA,
        "row_orbit_canonicalization_performed": False,
        "scope_guard": "B20 anchor-free top-touching columns only. ker(L20) gives a sufficient positive global certificate; negative/global completeness additionally requires the certified lower-transfer domain below K20.",
        "production_launched": False,
    }
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
