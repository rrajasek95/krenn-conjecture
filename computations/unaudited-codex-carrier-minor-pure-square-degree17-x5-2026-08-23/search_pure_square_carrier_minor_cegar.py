#!/usr/bin/env python3
"""Support-driven degree-17 CEGAR for F_0^2 times canonical Delta."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
COMMON_PATH = HERE.parent / "unaudited-codex-carrier-minor-coned-degree13-x5-2026-08-23" / "search_coned_carrier_minor_cegar.py"
OUT = HERE / "results_pure_square_carrier_minor_cegar_p32003.json"
ROUND_CAP = 512
SUPPORT_CAP = 5_000
FILL_CAP = 12_000_000


def load_common():
    spec = importlib.util.spec_from_file_location("coned_common", COMMON_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


C = load_common()
D9 = C.D9
P = C.P


class TargetOracle:
    def __init__(self):
        self.delta = D9.target_minor()
        pure = D9.amplitude((0,) * 8)
        self.pure_square = D9.poly_mul(pure, pure)
        assert len(self.delta) == 6900 and len(self.pure_square) == 5250
        self.calls = 0
        self.nonzero_calls = 0

    @lru_cache(maxsize=None)
    def coefficient(self, monomial):
        self.calls += 1
        value = 0
        # Iterate over the smaller square factor; a quotient, when present,
        # must be a literal degree-9 Delta monomial.
        for factor, coefficient in self.pure_square.items():
            quotient = C.divides(monomial, factor)
            if quotient is not None:
                value += coefficient * self.delta.get(quotient, 0)
        if value:
            self.nonzero_calls += 1
        return value

    def seed_candidates(self, count=64):
        candidates = []
        seen = set()
        delta_terms = sorted(self.delta)[:16]
        square_terms = sorted(self.pure_square)[:16]
        for left in delta_terms:
            for right in square_terms:
                monomial = tuple(sorted(left + right))
                if monomial in seen:
                    continue
                seen.add(monomial)
                coefficient = self.coefficient(monomial)
                if coefficient:
                    candidates.append((monomial, coefficient))
                    if len(candidates) == count:
                        return tuple(candidates)
        assert candidates
        return tuple(candidates)


class Columns:
    def __init__(self, reserved):
        self.to_id = {}
        self.from_id = {}
        self.next_outside = 0
        for index, monomial in enumerate(reserved):
            column = C.TARGET_BASE + index
            self.to_id[monomial] = column
            self.from_id[column] = monomial

    def identify(self, monomial):
        column = self.to_id.get(monomial)
        if column is None:
            assert self.next_outside < C.TARGET_BASE
            column = self.next_outside
            self.next_outside += 1
            self.to_id[monomial] = column
            self.from_id[column] = monomial
        return column


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


def choose_separator(basis, seed_columns, columns, oracle):
    for free in seed_columns:
        if free in basis:
            continue
        dual = functional_from_free(basis, free)
        pairing = sum(
            coefficient * oracle.coefficient(columns.from_id[column])
            for column, coefficient in dual.items()
        ) % P
        if pairing:
            return dual, pairing, free
    return {}, 0, None


def rational_reconstruction(residue):
    candidates = []
    from fractions import Fraction
    from math import gcd
    for denominator in range(1, 33):
        inverse = pow(denominator, P - 2, P)
        for numerator in range(-64, 65):
            if gcd(abs(numerator), denominator) == 1 \
                    and numerator * inverse % P == residue % P:
                candidates.append(Fraction(numerator, denominator))
    if not candidates:
        return None
    candidates.sort(key=lambda value: (
        abs(value.numerator) + value.denominator,
        value.denominator, abs(value.numerator), value.numerator,
    ))
    return candidates[0]


def exact_replay(dual, generators, columns, oracle):
    reconstructed = {
        columns.from_id[column]: rational_reconstruction(coefficient)
        for column, coefficient in dual.items()
    }
    if any(value is None for value in reconstructed.values()):
        return {"reconstruction_succeeded": False}
    from functools import reduce
    from math import gcd, lcm
    denominator = reduce(lcm, (value.denominator for value in reconstructed.values()), 1)
    integer = {
        monomial: int(value * denominator)
        for monomial, value in reconstructed.items()
    }
    common = reduce(gcd, (abs(value) for value in integer.values()))
    integer = {monomial: value // common for monomial, value in integer.items()}
    labels = set()
    occurrences = 0
    for monomial in integer:
        for word_index, generator in enumerate(generators):
            for term in generator:
                quotient = C.divides(monomial, term)
                if quotient is not None:
                    labels.add((word_index, quotient))
                    occurrences += 1
    by_word = Counter()
    nonzero = []
    for label in sorted(labels):
        by_word[D9.word_text(C.WORDS[label[0]])] += 1
        pairing = sum(
            integer.get(monomial, 0)
            for monomial in C.row_monomials(label, generators)
        )
        if pairing:
            nonzero.append((label, pairing))
    target_pairing = sum(
        coefficient * oracle.coefficient(monomial)
        for monomial, coefficient in integer.items()
    )
    entries = [
        {"monomial": D9.monomial_text(monomial), "coefficient": coefficient}
        for monomial, coefficient in sorted(integer.items())
    ]
    return {
        "reconstruction_succeeded": True,
        "rational_denominators": sorted({
            value.denominator for value in reconstructed.values()
        }),
        "clearing_denominator": denominator,
        "primitive_gcd_removed": common,
        "support": len(integer),
        "coefficient_minimum": min(integer.values()),
        "coefficient_maximum": max(integer.values()),
        "coefficient_set": sorted(set(integer.values())),
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
        "is_exact_integer_separator": not nonzero and target_pairing != 0,
        "entries": entries,
        "sha256": sha256(json.dumps(
            entries, sort_keys=True, separators=(",", ":")
        ).encode()).hexdigest(),
    }


def main():
    started = time.time()
    oracle = TargetOracle()
    seeds = oracle.seed_candidates()
    columns = Columns(monomial for monomial, _ in seeds)
    seed_columns = tuple(columns.to_id[monomial] for monomial, _ in seeds)
    generators = tuple(tuple(D9.amplitude(word)) for word in C.WORDS)
    basis = {}
    seen = set()
    rounds = []
    terminal = "ROUND_CAP"
    dual = {}
    print("factors/seeds", len(oracle.delta), len(oracle.pure_square), len(seeds),
          "oracle", oracle.calls, flush=True)

    for round_index in range(ROUND_CAP):
        dual, pairing, free = choose_separator(
            basis, seed_columns, columns, oracle
        )
        if not dual:
            terminal = "NO_SEPARATOR_ON_SEED_QUOTIENT"
            break
        if len(dual) > SUPPORT_CAP or sum(map(len, basis.values())) > FILL_CAP:
            terminal = "SIZE_CAP"
            break
        live, quotient_candidates = C.crossing_labels(dual, generators, columns)
        new_live = tuple(label for label in live if label not in seen)
        rank_before = len(basis)
        for label in new_live:
            seen.add(label)
            C.insert(C.encoded_row(label, generators, columns), basis)
        record = {
            "round": round_index + 1,
            "rank_before": rank_before,
            "dual_support": len(dual),
            "seed_index": free - C.TARGET_BASE,
            "quotient_candidates": quotient_candidates,
            "crossing_rows": len(live),
            "new_crossing_rows": len(new_live),
            "rank_after": len(basis),
            "columns_after": len(columns.to_id),
            "basis_fill_after": sum(map(len, basis.values())),
            "target_pairing": pairing,
            "target_oracle_cache": oracle.coefficient.cache_info().currsize,
        }
        rounds.append(record)
        print("ROUND", json.dumps(record, sort_keys=True), flush=True)
        if not new_live:
            assert not live
            terminal = "SEPARATOR_MOD_P"
            break

    exact = exact_replay(dual, generators, columns, oracle) \
        if terminal == "SEPARATOR_MOD_P" else None
    payload = {
        "status": terminal,
        "prime": P,
        "target": {
            "formula": "F_00000000^2 * canonical Delta",
            "degree": 17,
            "delta_terms": len(oracle.delta),
            "pure_square_terms": len(oracle.pure_square),
            "not_materialized": True,
        },
        "candidate_mixed_words": [D9.word_text(word) for word in C.WORDS],
        "seed_target_columns": len(seeds),
        "round_cap": ROUND_CAP,
        "support_cap": SUPPORT_CAP,
        "fill_cap": FILL_CAP,
        "rounds": rounds,
        "final_rank": len(basis),
        "final_columns": len(columns.to_id),
        "final_basis_fill": sum(map(len, basis.values())),
        "final_dual_support": len(dual),
        "target_oracle": {
            "cache_size": oracle.coefficient.cache_info().currsize,
            "calls": oracle.calls,
            "nonzero_calls": oracle.nonzero_calls,
        },
        "exact_replay": exact,
        "scope": (
            "Support-driven complete crossing scans in the fixed fine grade. "
            "A modular separator stall is global for the degree-17 translate "
            "universe; characteristic-zero nonmembership requires successful "
            "exact replay. A size/no-separator terminal is only bounded evidence."
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(terminal, "rank", len(basis), "columns", len(columns.to_id),
          "dual", len(dual), "exact", exact and exact.get("is_exact_integer_separator"),
          "oracle", oracle.calls, "secs", time.time() - started, flush=True)


if __name__ == "__main__":
    main()
