#!/usr/bin/env python3
"""Collect one provenance-safe orbit-zero K16 residual exactly.

The reduction is canonical relative to the frozen 25-signature cover: at a
literal K14 row, average over *all* literal mixed singleton pivots whose
irreducible K16 signature tails lie in that cover.  This choice is equivariant
under the order-384 factor stabilizer.  Coefficients are collected before any
signature projection; only then are reducible K16 rows discarded modulo the
K0 initial mixed ideal.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
import ast
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K14_DIR = ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
K14_PATH = K14_DIR / "audit_orbit0_k14_interface.py"
COVER_PATH = K14_DIR / "results_k16_anchor_cover.json"
OUT = HERE / "results_orbit0_k16_literal_residual.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


K14 = load("k14_literal_collection", K14_PATH)
F = K14.FROZEN


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def build():
    cover_raw = json.loads(COVER_PATH.read_text())
    cover = frozenset(
        ast.literal_eval(row) for row in
        cover_raw["single_pivot_cover"]["minimum_cover_orbit_representatives"]
    )
    require(len(cover) == 25, len(cover))

    three_words = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    three_anchors = tuple(F.BASE.term_ids(word, F.M0) for word in three_words)
    errors = tuple(Counter({
        term: 1 for term in F.BASE.word_terms(word)
        if term != anchor and F.row_k_degree(term) == 2
    }) for word, anchor in zip(three_words, three_anchors, strict=True))
    packet = F.polynomial_product(F.polynomial_product(errors[0], errors[1]), errors[2])
    require(len(packet) == sum(packet.values()) == 1728, len(packet))

    factor_set = frozenset(three_anchors)
    stabilizer = tuple(
        action for action in range(len(F.EXPORT.STABILIZER))
        if frozenset(F.move_row(term, action) for term in three_anchors) == factor_set
    )
    require(len(stabilizer) == 384, len(stabilizer))

    anchor_cells = tuple(sorted(F.A))
    anchor_position = {cell: index for index, cell in enumerate(anchor_cells)}
    mixed_anchors = []
    mixed_vectors = []
    mixed_tails = []
    mixed_labels = []
    for colours in product(range(3), repeat=4):
        if len(set(colours)) == 1:
            continue
        word = F.word_from_pair_colours(colours)
        anchor = F.BASE.term_ids(word, F.M0)
        terms = F.BASE.word_terms(word)
        tails = tuple(term for term in terms if F.row_k_degree(term) == 2)
        require(len(tails) == 12, (colours, len(tails)))
        mixed_labels.append(colours)
        mixed_anchors.append(anchor)
        mixed_vectors.append(tuple(Counter(anchor)[cell] for cell in anchor_cells))
        mixed_tails.append(tails)
    require(len(mixed_anchors) == 78, len(mixed_anchors))
    anchor_to_pivot = {row: index for index, row in enumerate(mixed_anchors)}
    require(len(anchor_to_pivot) == 78, len(anchor_to_pivot))

    signature_permutations = {}
    pivot_permutations = {}
    for action in stabilizer:
        transform = F.EXPORT.TRANSFORMS[action]
        signature_permutations[action] = tuple(
            anchor_position[transform[cell]] for cell in anchor_cells
        )
        pivot_permutations[action] = tuple(
            anchor_to_pivot[F.move_row(anchor, action)] for anchor in mixed_anchors
        )
    require(all(len(set(row)) == 12 for row in signature_permutations.values()),
            "anchor action is not a permutation")
    require(all(len(set(row)) == 78 for row in pivot_permutations.values()),
            "pivot action is not a permutation")

    # Canonicalizing millions of literal rows used to dominate this audit:
    # ``F.move_row`` performs the cell substitution in a Python generator.
    # The action is a byte permutation, so do that substitution in C via
    # ``bytes.translate`` and retain only the unavoidable length-24 sort.
    translation_tables = {}
    for action in stabilizer:
        transform = tuple(F.EXPORT.TRANSFORMS[action]) + tuple(range(252, 256))
        require(len(transform) == 256 and len(set(transform)) == 256,
                (action, "cell action is not a byte permutation"))
        translation_tables[action] = bytes(transform)

    def move_row_fast(row, action):
        return bytes(sorted(row.translate(translation_tables[action])))

    def orbit_under_fast(row):
        return frozenset(move_row_fast(row, action) for action in stabilizer)

    # The K2 tail packet must transport with the literal source row, not only
    # with its anchor signature.
    tail_transport_checks = 0
    for action in stabilizer:
        for pivot, tails in enumerate(mixed_tails):
            moved = pivot_permutations[action][pivot]
            require(
                {F.move_row(tail, action) for tail in tails} == set(mixed_tails[moved]),
                (action, pivot, moved, "tail provenance mismatch"),
            )
            tail_transport_checks += len(tails)

    def move_signature(signature, action):
        moved = [0] * 12
        for old, new in enumerate(signature_permutations[action]):
            moved[new] = signature[old]
        return tuple(moved)

    signature_data = {}

    def canonical_signature(signature):
        if signature not in signature_data:
            images = [(move_signature(signature, action), action)
                      for action in stabilizer]
            canonical = min(row for row, _action in images)
            actions = tuple(action for row, action in images if row == canonical)
            signature_data[signature] = (canonical, actions)
        return signature_data[signature][0]

    pivot_cache = {}

    def pivots(signature):
        if signature not in pivot_cache:
            pivot_cache[signature] = tuple(
                index for index, vector in enumerate(mixed_vectors)
                if all(left >= right
                       for left, right in zip(signature, vector, strict=True))
            )
        return pivot_cache[signature]

    valid_cache = {}

    def valid_pivots(signature):
        if signature not in valid_cache:
            valid = []
            for pivot in pivots(signature):
                base = tuple(left - right for left, right
                             in zip(signature, mixed_vectors[pivot], strict=True))
                survivor_orbits = set()
                for tail in mixed_tails[pivot]:
                    counts = Counter(tail)
                    new = tuple(left + counts[cell] for left, cell
                                in zip(base, anchor_cells, strict=True))
                    if not pivots(new):
                        survivor_orbits.add(canonical_signature(new))
                if survivor_orbits <= cover:
                    valid.append(pivot)
            require(valid, (signature, canonical_signature(signature), "no cover pivot"))
            valid_cache[signature] = tuple(valid)
        return valid_cache[signature]

    def canonical_literal(row):
        row_counter = Counter(row)
        signature = tuple(row_counter[cell] for cell in anchor_cells)
        canonical, actions = signature_data.get(signature, (None, None))
        if canonical is None:
            canonical = canonical_signature(signature)
            actions = signature_data[signature][1]
        moved_rows = tuple(move_row_fast(row, action) for action in actions)
        return canonical, min(moved_rows)

    # Split the frozen full-stabilizer R8' rows into exact H-orbits while
    # retaining the actual per-labelled-row coefficient.  Quotient input
    # coefficients are full-orbit masses.
    raw = json.loads(F.R8P.read_text())
    h_records = []
    actual_r8_coefficients = Counter()
    for row_hex, numerator, denominator in raw["residual"]:
        representative = bytes.fromhex(row_hex)
        full_orbit = set(F.EXPORT.row_orbit(representative))
        actual_coefficient = Fraction(numerator, denominator) / len(full_orbit)
        actual_r8_coefficients[actual_coefficient] += len(full_orbit)
        unseen = set(full_orbit)
        while unseen:
            seed = min(unseen)
            orbit = orbit_under_fast(seed)
            require(orbit <= unseen, "H orbit crossed frozen full orbit")
            h_records.append((seed, len(orbit), actual_coefficient))
            unseen.difference_update(orbit)
    require(len(h_records) == 485, len(h_records))
    require(sum(size for _row, size, _coefficient in h_records) == 148176,
            sum(size for _row, size, _coefficient in h_records))

    residual = defaultdict(Fraction)
    factored_pairs = 0
    literal_pivot_uses = 0
    irreducible_tail_occurrences = 0
    reducible_tail_occurrences = 0
    valid_pivot_histogram = Counter()
    input_signature_histogram = Counter()
    for r8, orbit_size, coefficient in h_records:
        for packet_row, packet_coefficient in packet.items():
            target = bytes(sorted(r8 + packet_row))
            target_counter = Counter(target)
            signature = tuple(target_counter[cell] for cell in anchor_cells)
            available = valid_pivots(signature)
            valid_pivot_histogram[len(available)] += 1
            input_signature_histogram[canonical_signature(signature)] += 1
            factored_pairs += 1
            # This is the total mass represented by the fixed-r8 slice.
            pair_mass = coefficient * orbit_size * packet_coefficient
            pivot_weight = -pair_mass / len(available)
            for pivot in available:
                literal_pivot_uses += 1
                base = Counter(target)
                base.subtract(mixed_anchors[pivot])
                require(all(value >= 0 for value in base.values()),
                        (target.hex(), pivot, "nondividing chosen pivot"))
                quotient = bytes(sorted(
                    cell for cell, value in base.items() for _ in range(value)
                ))
                for tail in mixed_tails[pivot]:
                    row = bytes(sorted(quotient + tail))
                    row_counter = Counter(row)
                    row_signature = tuple(row_counter[cell] for cell in anchor_cells)
                    if pivots(row_signature):
                        reducible_tail_occurrences += 1
                        continue
                    irreducible_tail_occurrences += 1
                    _signature_rep, row_rep = canonical_literal(row)
                    residual[row_rep] += pivot_weight

    require(factored_pairs == 485 * 1728 == 838080, factored_pairs)
    residual = {row: value for row, value in residual.items() if value}

    output_signature_orbits = Counter()
    coefficient_histogram = Counter()
    orbit_size_histogram = Counter()
    labelled_support = 0
    for row, mass in residual.items():
        row_counter = Counter(row)
        signature = tuple(row_counter[cell] for cell in anchor_cells)
        canonical = canonical_signature(signature)
        require(signature == canonical, (signature, canonical, "noncanonical output"))
        output_signature_orbits[canonical] += 1
        orbit = orbit_under_fast(row)
        orbit_size_histogram[len(orbit)] += 1
        labelled_support += len(orbit)
        coefficient_histogram[mass / len(orbit)] += len(orbit)

    # Exact equivariance of the reduction rule on every literal signature
    # encountered in the collection.
    equivariance_checks = 0
    for signature in tuple(valid_cache):
        valid = set(valid_pivots(signature))
        for action in stabilizer:
            moved_signature = move_signature(signature, action)
            moved_valid = {pivot_permutations[action][pivot] for pivot in valid}
            require(moved_valid == set(valid_pivots(moved_signature)),
                    (signature, action, "valid-pivot rule is not equivariant"))
            equivariance_checks += 1

    result = {
        "status": "PASS exact literal-provenance orbit-zero K16 collection",
        "theorem": {
            "input": "the frozen H-invariant leading K14 polynomial -R8prime*E0_2*E1_2*E2_2",
            "reduction": (
                "at each literal K14 row, average over every literal mixed "
                "K0 singleton pivot whose irreducible K16 signature tails "
                "lie in the frozen exact 25-orbit cover"
            ),
            "output": (
                "the fully coefficient-collected irreducible K16 residual "
                "modulo the K0 initial mixed ideal, stored by literal H-orbits"
            ),
            "scope": (
                "This is one canonical H-equivariant reduction on orbit zero. "
                "It is not pivot-independent, does not use hidden initial "
                "forms from lower filtration, and makes no claim for the "
                "other 30 pure-matching charts."
            ),
        },
        "source_provenance": {
            "factor_stabilizer_order": len(stabilizer),
            "literal_mixed_singleton_rows": len(mixed_anchors),
            "literal_K2_tails_per_row": sorted(set(map(len, mixed_tails))),
            "tail_transport_checks": tail_transport_checks,
            "valid_pivot_equivariance_checks": equivariance_checks,
            "valid_pivot_count_histogram_per_factored_pair": {
                str(key): value for key, value in sorted(valid_pivot_histogram.items())
            },
        },
        "input": {
            "R8prime_H_orbits": len(h_records),
            "R8prime_labelled_rows": sum(size for _row, size, _coefficient in h_records),
            "R8prime_actual_coefficient_histogram": {
                str(key): value for key, value in sorted(actual_r8_coefficients.items())
            },
            "leading_packet_rows": len(packet),
            "factored_H_slice_pairs": factored_pairs,
            "K14_signature_orbits_seen": len(input_signature_histogram),
        },
        "collection": {
            "literal_pivot_uses": literal_pivot_uses,
            "reducible_K16_tail_occurrences": reducible_tail_occurrences,
            "irreducible_K16_tail_occurrences_before_collection": (
                irreducible_tail_occurrences
            ),
            "nonzero_literal_H_orbits_after_collection": len(residual),
            "nonzero_anchor_signature_orbits_after_collection": len(
                output_signature_orbits
            ),
            "literal_orbits_per_anchor_signature": {
                str(key): value for key, value in sorted(output_signature_orbits.items())
            },
            "labelled_support_after_collection": labelled_support,
            "literal_H_orbit_size_histogram": {
                str(key): value for key, value in sorted(orbit_size_histogram.items())
            },
            "labelled_row_coefficient_histogram": {
                str(key): value for key, value in sorted(coefficient_histogram.items())
            },
            "zero_residual": not residual,
        },
        "literal_orbits": [
            [row.hex(), value.numerator, value.denominator]
            for row, value in sorted(residual.items())
        ],
        "pinned": {
            str(K14_PATH.relative_to(ROOT)): sha256(K14_PATH.read_bytes()).hexdigest(),
            str(COVER_PATH.relative_to(ROOT)): sha256(COVER_PATH.read_bytes()).hexdigest(),
            str(F.R8P.relative_to(ROOT)): sha256(F.R8P.read_bytes()).hexdigest(),
        },
    }
    return result


def main(write_results=False):
    result = build()
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": logical,
        "source_provenance": result["source_provenance"],
        "input": result["input"],
        "collection": {
            key: value for key, value in result["collection"].items()
            if key not in {"literal_orbits_per_anchor_signature",
                           "labelled_row_coefficient_histogram"}
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
