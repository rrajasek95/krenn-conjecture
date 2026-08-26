#!/usr/bin/env python3
"""Bounded lazy CEGAR for F_(0^8) times the canonical carrier minor."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
COMMON_PATH = HERE.parent / "unaudited-codex-carrier-minor-coned-degree13-x5-2026-08-23" / "search_coned_carrier_minor_cegar.py"
OUT = HERE / "results_pure_amplitude_carrier_minor_cegar_p32003.json"


def load_common():
    spec = importlib.util.spec_from_file_location("coned_common", COMMON_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


C = load_common()
D9 = C.D9
P = C.P


def target_polynomial():
    target = D9.poly_mul(D9.target_minor(), D9.amplitude((0,) * 8))
    assert len(target) == 664_776 and set(map(len, target)) == {13}
    return target


def target_digest(target):
    digest = sha256()
    for monomial, coefficient in sorted(target.items()):
        digest.update(D9.monomial_text(monomial).encode())
        digest.update(b":")
        digest.update(str(coefficient).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def functional_from_free(basis, free):
    dual = {free: 1}
    for pivot in sorted(basis, reverse=True):
        value = sum(
            coefficient * dual.get(column, 0)
            for column, coefficient in basis[pivot].items()
            if column != pivot
        ) % P
        if value:
            dual[pivot] = -value % P
    return dual


def choose_separator(basis, target_row):
    # In this run every discovered basis pivot is outside the target support.
    # Retain a guarded fallback for source drift.
    for free in sorted(target_row):
        if free in basis:
            continue
        dual = functional_from_free(basis, free)
        pairing = sum(coefficient * dual.get(column, 0)
                      for column, coefficient in target_row.items()) % P
        if pairing:
            return dual, pairing, free
    remainder = C.reduce_row(target_row, basis)
    if not remainder:
        return {}, 0, None
    dual, pairing = C.separating_dual(basis, remainder)
    return dual, pairing, min(remainder)


def exact_replay(dual, target, generators, columns):
    centered = {
        columns.from_id[column]: (
            coefficient if coefficient <= P // 2 else coefficient - P
        )
        for column, coefficient in dual.items()
    }
    labels = set()
    occurrences = 0
    for monomial in centered:
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = C.divides(monomial, term)
                if quotient is not None:
                    labels.add((word_index, quotient))
                    occurrences += 1
    nonzero = []
    by_word = Counter()
    for label in sorted(labels):
        by_word[D9.word_text(C.WORDS[label[0]])] += 1
        pairing = sum(
            centered.get(monomial, 0)
            for monomial in C.row_monomials(label, generators)
        )
        if pairing:
            nonzero.append((label, pairing))
    target_pairing = sum(coefficient * centered.get(monomial, 0)
                         for monomial, coefficient in target.items())
    entries = [
        {
            "monomial": D9.monomial_text(monomial),
            "coefficient": coefficient,
        }
        for monomial, coefficient in sorted(centered.items())
    ]
    return {
        "support": len(centered),
        "coefficient_minimum": min(centered.values()),
        "coefficient_maximum": max(centered.values()),
        "quotient_occurrences": occurrences,
        "distinct_translates_touching_support": len(labels),
        "translates_by_word": dict(by_word),
        "nonzero_integer_row_pairings": len(nonzero),
        "first_nonzero_pairings": [
            {
                "word": D9.word_text(C.WORDS[label[0]]),
                "multiplier": D9.monomial_text(label[1]),
                "pairing": pairing,
            }
            for label, pairing in nonzero[:10]
        ],
        "target_pairing": target_pairing,
        "entries": entries,
        "sha256": sha256(json.dumps(
            entries, sort_keys=True, separators=(",", ":")
        ).encode()).hexdigest(),
        "is_exact_integer_separator": not nonzero and target_pairing != 0,
    }


def main():
    start = time.time()
    target = target_polynomial()
    coefficient_histogram = Counter(target.values())
    print("target", len(target), dict(sorted(coefficient_histogram.items())),
          "secs", time.time() - start, flush=True)
    generators = tuple(tuple(D9.amplitude(word)) for word in C.WORDS)
    columns = C.Columns(target)
    target_row = {
        columns.to_id[monomial]: coefficient % P
        for monomial, coefficient in target.items()
    }
    basis = {}
    seen = set()
    rounds = []
    terminal = "ROUND_CAP"
    dual = {}

    for round_index in range(256):
        dual, pairing, free = choose_separator(basis, target_row)
        if not dual:
            terminal = "MEMBER_MOD_P"
            break
        live, quotient_candidates = C.crossing_labels(
            dual, generators, columns
        )
        new_live = tuple(label for label in live if label not in seen)
        rank_before = len(basis)
        for label in new_live:
            seen.add(label)
            C.insert(C.encoded_row(label, generators, columns), basis)
        record = {
            "round": round_index + 1,
            "rank_before": rank_before,
            "dual_support": len(dual),
            "free_is_target_column": free >= C.TARGET_BASE,
            "quotient_candidates": quotient_candidates,
            "crossing_rows": len(live),
            "new_crossing_rows": len(new_live),
            "rank_after": len(basis),
            "columns_after": len(columns.to_id),
            "basis_fill_after": sum(map(len, basis.values())),
            "target_pairing": pairing,
        }
        rounds.append(record)
        print("ROUND", json.dumps(record, sort_keys=True), flush=True)
        if not new_live:
            assert not live
            terminal = "SEPARATOR_MOD_P"
            break

    exact = exact_replay(dual, target, generators, columns) \
        if terminal == "SEPARATOR_MOD_P" else None
    payload = {
        "status": terminal,
        "prime": P,
        "target": {
            "formula": "F_00000000 * canonical Delta",
            "degree": 13,
            "terms": len(target),
            "coefficient_histogram": {
                str(key): value for key, value in sorted(coefficient_histogram.items())
            },
            "sha256": target_digest(target),
        },
        "candidate_mixed_words": [D9.word_text(word) for word in C.WORDS],
        "initial_rank": 0,
        "rounds": rounds,
        "final_rank": len(basis),
        "final_columns": len(columns.to_id),
        "final_basis_fill": sum(map(len, basis.values())),
        "final_dual_support": len(dual),
        "centered_integer_replay": exact,
        "scope": (
            "Complete fine-graded degree-13 homogeneous mixed-X5 translate "
            "universe. The empty-seed lazy theorem makes a zero-crossing "
            "terminal scan exhaustive. Exact-Z replay is mandatory for a "
            "characteristic-zero nonmembership claim."
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(terminal, "rank", len(basis), "columns", len(columns.to_id),
          "dual", len(dual), "exact", exact and exact["is_exact_integer_separator"],
          "secs", time.time() - start, flush=True)


if __name__ == "__main__":
    main()
