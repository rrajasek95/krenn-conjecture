#!/usr/bin/env python3
"""Lazy modular CEGAR for M times one canonical carrier minor in mixed X5.

This is a bounded discovery program.  A terminal modular separator is not a
characteristic-zero certificate until it is lifted and replayed exactly.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
DEG9 = HERE.parent / "unaudited-codex-carrier-minor-degree9-x5-2026-08-23" / "audit_carrier_minor_degree9_x5.py"
P = 32003
TARGET_BASE = 1_000_000_000
WORDS = (
    (0, 0, 0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 0, 1, 1),
    (0, 0, 0, 0, 0, 0, 2, 0),
    (0, 0, 0, 0, 0, 0, 2, 1),
)


def load_degree9():
    spec = importlib.util.spec_from_file_location("degree9_carrier", DEG9)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D9 = load_degree9()


def divides(big, small):
    """Return the sorted multiset quotient big/small, or None."""
    counts = Counter(big)
    for atom in small:
        if not counts[atom]:
            return None
        counts[atom] -= 1
    return tuple(sorted(counts.elements()))


def coned_target():
    cone = (
        D9.cell(0, 1, 0, 0), D9.cell(2, 3, 0, 0),
        D9.cell(4, 5, 0, 0), D9.cell(6, 7, 0, 0),
    )
    target = Counter()
    for monomial, coefficient in D9.target_minor().items():
        target[tuple(sorted(monomial + cone))] += coefficient
    assert len(target) == 6900 and set(map(len, target)) == {13}
    return target, tuple(sorted(cone))


def target_touching_labels(target, generators):
    labels = set()
    touching_by_word = Counter()
    for monomial in target:
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = divides(monomial, term)
                if quotient is not None:
                    labels.add((word_index, quotient))
    for word_index, _ in labels:
        touching_by_word[D9.word_text(WORDS[word_index])] += 1
    return tuple(sorted(labels)), touching_by_word


class Columns:
    def __init__(self, target):
        self.target = set(target)
        self.to_id = {}
        self.from_id = {}
        for index, monomial in enumerate(sorted(target)):
            column = TARGET_BASE + index
            self.to_id[monomial] = column
            self.from_id[column] = monomial
        self.next_outside = 0

    def preload_outside(self, frequencies):
        for monomial, _ in sorted(frequencies.items(), key=lambda item: (item[1], item[0])):
            if monomial not in self.to_id:
                self.add_outside(monomial)

    def add_outside(self, monomial):
        assert self.next_outside < TARGET_BASE
        column = self.next_outside
        self.next_outside += 1
        self.to_id[monomial] = column
        self.from_id[column] = monomial
        return column

    def identify(self, monomial):
        column = self.to_id.get(monomial)
        if column is None:
            column = self.add_outside(monomial)
        return column


def row_monomials(label, generators):
    word_index, quotient = label
    return tuple(tuple(sorted(term + quotient)) for term in generators[word_index])


def encoded_row(label, generators, columns):
    row = {}
    for monomial in row_monomials(label, generators):
        column = columns.identify(monomial)
        row[column] = (row.get(column, 0) + 1) % P
    return {column: coefficient for column, coefficient in row.items() if coefficient}


def reduce_row(raw, basis):
    row = dict(raw)
    while row:
        pivot = min(row)
        coefficient = row[pivot]
        stored = basis.get(pivot)
        if stored is None:
            break
        for column, value in stored.items():
            updated = (row.get(column, 0) - coefficient * value) % P
            if updated:
                row[column] = updated
            else:
                row.pop(column, None)
    return row


def insert(raw, basis):
    row = reduce_row(raw, basis)
    if not row:
        return False
    pivot = min(row)
    inverse = pow(row[pivot], P - 2, P)
    basis[pivot] = {
        column: coefficient * inverse % P
        for column, coefficient in row.items()
    }
    return True


def separating_dual(basis, remainder):
    free = min(remainder)
    dual = {free: 1}
    for pivot in sorted(basis, reverse=True):
        value = sum(
            coefficient * dual.get(column, 0)
            for column, coefficient in basis[pivot].items()
            if column != pivot
        ) % P
        if value:
            dual[pivot] = -value % P
    pairing = sum(coefficient * dual.get(column, 0)
                  for column, coefficient in remainder.items()) % P
    assert pairing
    return dual, pairing


def crossing_labels(dual, generators, columns):
    """Enumerate every translate with nonzero pairing against dual."""
    pairings = [defaultdict(int) for _ in generators]
    quotient_candidates = 0
    for column, dual_coefficient in dual.items():
        monomial = columns.from_id[column]
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = divides(monomial, term)
                if quotient is not None:
                    pairings[word_index][quotient] = (
                        pairings[word_index][quotient] + dual_coefficient
                    ) % P
                    quotient_candidates += 1
    live = []
    for word_index, word_pairings in enumerate(pairings):
        live.extend(
            (word_index, quotient)
            for quotient, coefficient in word_pairings.items()
            if coefficient
        )
    return tuple(sorted(live)), quotient_candidates


def target_digest(target):
    record = [
        [D9.monomial_text(monomial), coefficient]
        for monomial, coefficient in sorted(target.items())
    ]
    return sha256(json.dumps(record, separators=(",", ":")).encode()).hexdigest()


def exact_separator_replay(dual, target, generators, columns):
    """Try the centered modular dual as a literal integer functional."""
    centered = {
        columns.from_id[column]: (
            coefficient if coefficient <= P // 2 else coefficient - P
        )
        for column, coefficient in dual.items()
    }
    candidate_labels = set()
    for monomial in centered:
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = divides(monomial, term)
                if quotient is not None:
                    candidate_labels.add((word_index, quotient))
    nonzero_pairings = []
    for label in sorted(candidate_labels):
        pairing = sum(centered.get(monomial, 0)
                      for monomial in row_monomials(label, generators))
        if pairing:
            nonzero_pairings.append((label, pairing))
    target_pairing = sum(coefficient * centered.get(monomial, 0)
                         for monomial, coefficient in target.items())
    entries = [
        {
            "monomial": D9.monomial_text(monomial),
            "coefficient": coefficient,
        }
        for monomial, coefficient in sorted(centered.items())
    ]
    digest = sha256(json.dumps(
        entries, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return {
        "centered_support": len(centered),
        "minimum_coefficient": min(centered.values()),
        "maximum_coefficient": max(centered.values()),
        "translate_candidates_touching_support": len(candidate_labels),
        "nonzero_integer_row_pairings": len(nonzero_pairings),
        "first_nonzero_pairings": [
            {
                "word": D9.word_text(WORDS[label[0]]),
                "multiplier": D9.monomial_text(label[1]),
                "pairing": pairing,
            }
            for label, pairing in nonzero_pairings[:10]
        ],
        "integer_target_pairing": target_pairing,
        "sha256": digest,
        "entries": entries,
        "is_exact_integer_separator": (
            not nonzero_pairings and target_pairing != 0
        ),
    }


def main():
    start = time.time()
    target, cone = coned_target()
    generators = tuple(tuple(D9.amplitude(word)) for word in WORDS)
    labels, touching_by_word = target_touching_labels(target, generators)
    print("target/touching", len(target), len(labels), dict(touching_by_word), flush=True)

    # Assign low indices to rare outside columns, keeping every target column
    # last.  This substantially limits fill without changing row space.
    frequencies = Counter()
    for index, label in enumerate(labels):
        for monomial in row_monomials(label, generators):
            if monomial not in target:
                frequencies[monomial] += 1
        if index and index % 1000 == 0:
            print("preload", index, len(frequencies), time.time() - start,
                  file=sys.stderr, flush=True)
    columns = Columns(target)
    columns.preload_outside(frequencies)
    print("initial outside columns", columns.next_outside, flush=True)

    basis = {}
    seen = set(labels)
    independent = 0
    for index, label in enumerate(labels):
        independent += insert(encoded_row(label, generators, columns), basis)
        if index and index % 500 == 0:
            fill = sum(map(len, basis.values()))
            print("insert", index, len(basis), fill, time.time() - start,
                  file=sys.stderr, flush=True)
    target_row = {columns.to_id[monomial]: coefficient % P
                  for monomial, coefficient in target.items()}
    print("initial rank/fill", len(basis), sum(map(len, basis.values())),
          "columns", len(columns.to_id), "secs", time.time() - start, flush=True)

    rounds = []
    for round_index in range(16):
        remainder = reduce_row(target_row, basis)
        if not remainder:
            terminal = "MEMBER_MOD_P"
            dual = {}
            break
        dual, pairing = separating_dual(basis, remainder)
        live, quotient_candidates = crossing_labels(dual, generators, columns)
        new_live = tuple(label for label in live if label not in seen)
        rank_before = len(basis)
        for label in new_live:
            seen.add(label)
            insert(encoded_row(label, generators, columns), basis)
        round_record = {
            "round": round_index + 1,
            "rank_before": rank_before,
            "dual_support": len(dual),
            "target_remainder": len(remainder),
            "quotient_candidates": quotient_candidates,
            "crossing_rows": len(live),
            "new_crossing_rows": len(new_live),
            "rank_after": len(basis),
            "columns_after": len(columns.to_id),
            "basis_fill_after": sum(map(len, basis.values())),
            "target_pairing": pairing,
        }
        rounds.append(round_record)
        print("ROUND", json.dumps(round_record, sort_keys=True), flush=True)
        if not new_live:
            assert not live
            terminal = "SEPARATOR_MOD_P"
            break
    else:
        terminal = "ROUND_CAP"
        remainder = reduce_row(target_row, basis)
        dual, pairing = separating_dual(basis, remainder)

    exact_replay = exact_separator_replay(
        dual, target, generators, columns
    ) if terminal == "SEPARATOR_MOD_P" else None
    payload = {
        "status": terminal,
        "prime": P,
        "target_degree": 13,
        "target_terms": len(target),
        "target_sha256": target_digest(target),
        "pure_cone": D9.monomial_text(cone),
        "candidate_words": [D9.word_text(word) for word in WORDS],
        "target_touching_rows": len(labels),
        "target_touching_by_word": dict(touching_by_word),
        "initial_outside_columns": len(frequencies),
        "initial_rank": independent,
        "rounds": rounds,
        "final_rank": len(basis),
        "final_columns": len(columns.to_id),
        "final_basis_fill": sum(map(len, basis.values())),
        "final_remainder_terms": len(reduce_row(target_row, basis)),
        "final_dual_support": len(dual),
        "centered_integer_replay": exact_replay,
        "scope": (
            "Discovery over F_32003 in the complete fine-graded degree-13 "
            "mixed-X5 translate universe. MEMBER needs exact-Q coefficient "
            "replay; SEPARATOR needs an exact-Q dual replay against all rows."
        ),
    }
    (HERE / "results_coned_carrier_minor_cegar_p32003.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(terminal, "rank", len(basis), "columns", len(columns.to_id),
          "remainder", payload["final_remainder_terms"],
          "dual", len(dual), "secs", time.time() - start, flush=True)


if __name__ == "__main__":
    main()
