#!/usr/bin/env python3
"""Exact sign referee for the frozen leading-K14 K2-tail response."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import ast
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23"
          / "filtered_k24_reducer.py")
K16_RESULT = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
              / "results_orbit0_k16_literal_residual.json")
COVER = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
         / "results_k16_anchor_cover.json")
DAFSA_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
                / "build_k16_weighted_dafsa.py")
OUT = HERE / "results_filtered_k16_sign_referee.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load("filtered_k16_sign_design", DESIGN)
F = D.F


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def divides_signature(left, right):
    return all(a >= b for a, b in zip(left, right, strict=True))


def main(write_results=False):
    # Pin the formal telescope orientation.
    lhs, rhs = F.formal_telescoping()
    require(lhs == rhs, "formal telescope changed")
    telescope = (
        "t0*t1*t2 + E0*E1*E2 = H0*t1*t2 - E0*H1*t2 + E0*E1*H2"
    )
    # Hence a=t0t1t2 is congruent to -E0E1E2, and if R=T-S then
    # the current residual aR has leading coefficient -r.

    cover_raw = json.loads(COVER.read_text())
    cover = frozenset(ast.literal_eval(row) for row in
                      cover_raw["single_pivot_cover"]["minimum_cover_orbit_representatives"])
    require(len(cover) == 25, len(cover))

    words = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    anchors = tuple(F.BASE.term_ids(word, F.M0) for word in words)
    errors2 = tuple(Counter({term: 1 for term in F.BASE.word_terms(word)
                             if term != anchor and F.row_k_degree(term) == 2})
                    for word, anchor in zip(words, anchors, strict=True))
    packet = F.polynomial_product(F.polynomial_product(errors2[0], errors2[1]),
                                  errors2[2])
    require(len(packet) == 1728, len(packet))

    anchor_cells = D.CTX.anchor_cells
    pivots = D.CTX.pivots

    def signature(row):
        counts = Counter(row)
        return tuple(counts[cell] for cell in anchor_cells)

    def valid_pivots(sig):
        answer = []
        for pivot in pivots(sig):
            base = tuple(a - b for a, b in
                         zip(sig, D.CTX.vectors[pivot], strict=True))
            survivors = set()
            for tail in D.CTX.tails[pivot][2]:
                counts = Counter(tail)
                child = tuple(a + counts[cell] for a, cell in
                              zip(base, anchor_cells, strict=True))
                if not pivots(child):
                    survivors.add(D.CTX.canonical_signature(child))
            if survivors <= cover:
                answer.append(pivot)
        require(answer, sig)
        return tuple(answer)

    # Pick the lexicographically first literal factored K14 row.
    best = None
    for r8, orbit_size, coefficient in D.r8_h_records():
        for packet_row, packet_coefficient in packet.items():
            target = bytes(sorted(r8 + packet_row))
            candidate = (target, r8, orbit_size, coefficient, packet_row,
                         packet_coefficient)
            if best is None or target < best[0]:
                best = candidate
    target, r8, orbit_size, r8_coefficient, packet_row, packet_coefficient = best
    available = valid_pivots(signature(target))
    pivot = available[0]
    base = Counter(target)
    base.subtract(D.CTX.anchors[pivot])
    require(all(value >= 0 for value in base.values()), "pivot does not divide")
    multiplier = bytes(sorted(base.elements()))
    first_tail = min(D.CTX.tails[pivot][2])
    child = bytes(sorted(multiplier + first_tail))

    r = r8_coefficient * packet_coefficient
    current_head = -r
    source_coefficient = current_head / len(available)
    # Residual convention is P - sum(source_coefficient * H).
    replay_head = current_head - len(available) * source_coefficient
    correct_tail_per_pivot = -source_coefficient
    frozen_collector_tail_per_pivot = -r / len(available)
    require(replay_head == 0, replay_head)
    require(correct_tail_per_pivot == r / len(available), correct_tail_per_pivot)
    require(frozen_collector_tail_per_pivot == -correct_tail_per_pivot,
            (frozen_collector_tail_per_pivot, correct_tail_per_pivot))

    # The sign mismatch is uniform term-by-term, hence survives collection and
    # discarding the pivotable K16 rows.  Pin a literal frozen sentinel.
    dafsa = load("filtered_k16_sign_dafsa", DAFSA_SOURCE)
    first_frozen = next(dafsa.literal_records(K16_RESULT))
    require(first_frozen == (
        bytes.fromhex("09090d0d1821484c4c5160627d96c3cacacee0e3f3f7f7fb"), -384, 1
    ), first_frozen)

    result = {
        "status": "EXACT_SIGN_RETRACTION_FROZEN_RESPONSE_IS_NEGATIVE_OF_POST_REDUCTION",
        "telescope": telescope,
        "orientation": {
            "R_definition": "R=T-S, as in the exact cutoff-nine replay",
            "pre_reduction": "a*R is congruent to -R*E0*E1*E2",
            "residual_convention": "P - source_combination",
            "correct_K2_response": "+R8prime*E0_2*E1_2*E2_2 pivot tails",
            "frozen_collector_response": "the negative of that response",
            "safe_reinterpretation": (
                "the frozen artifact is the K2 tail of the source correction / "
                "source-minus-target orientation, not the post-reduction residual"
            ),
        },
        "lex_literal_replay": {
            "K14_row": target.hex(),
            "R8prime_row": r8.hex(),
            "R8prime_H_orbit_size": orbit_size,
            "R8prime_labelled_coefficient": [r8_coefficient.numerator,
                                               r8_coefficient.denominator],
            "packet_row": packet_row.hex(),
            "valid_pivots": len(available),
            "chosen_pivot_index": pivot,
            "chosen_pivot_word": "".join(map(str, D.CTX.words[pivot])),
            "multiplier": multiplier.hex(),
            "first_K2_tail": first_tail.hex(),
            "first_K16_child": child.hex(),
            "current_head_coefficient": [current_head.numerator,
                                           current_head.denominator],
            "source_coefficient_per_pivot": [source_coefficient.numerator,
                                               source_coefficient.denominator],
            "head_after_subtraction": [replay_head.numerator, replay_head.denominator],
            "correct_tail_contribution_per_pivot": [correct_tail_per_pivot.numerator,
                                                      correct_tail_per_pivot.denominator],
            "collector_tail_contribution_per_pivot": [
                frozen_collector_tail_per_pivot.numerator,
                frozen_collector_tail_per_pivot.denominator],
        },
        "frozen_sentinel": {
            "row": first_frozen[0].hex(),
            "stored_orbit_mass": [first_frozen[1], first_frozen[2]],
            "correct_post_reduction_orbit_mass": [-first_frozen[1], first_frozen[2]],
        },
        "combined_K16_guard": (
            "The actual full K16 residual must combine the direct -R8prime*E-product "
            "K16 slice with MINUS the stored frozen response.  Adding it is unsound."
        ),
        "pinned": {
            str(DESIGN.relative_to(ROOT)): sha256(DESIGN.read_bytes()).hexdigest(),
            str(K16_RESULT.relative_to(ROOT)): sha256(K16_RESULT.read_bytes()).hexdigest(),
            str(COVER.relative_to(ROOT)): sha256(COVER.read_bytes()).hexdigest(),
        },
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"],
                      "lex_literal_replay": result["lex_literal_replay"],
                      "logical_sha256": logical}, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
