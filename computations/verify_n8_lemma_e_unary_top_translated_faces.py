#!/usr/bin/env python3
"""Exact translated-fibre guards for the Lemma-E unary-top packet.

The first support audit froze 39/46-cell odd-circuit faces.  There are much
smaller deletion-irredundant faces: 24 cells for A_02=E_11 and 25 cells for
A_02=E_21.  Their mixed binomial character systems are consistent, but one
mixed zero fibre is a Laurent translate of a nonzero pure fibre.  Hence both
coefficient tori are empty by a single denominator-cleared identity.

These are exact face exclusions, not an exhaustive support theorem.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import verify_n8_lemma_e_shared_unary_top_support_packets as base


EXPECTED_DIGEST = "dd56ca264935bce13d09f2ce6fe8740aaa2cdc57202fd0e8e246ceacaa007661"


PACKETS = {
    1: frozenset({
        (0, 1, 0, 0), (0, 2, 1, 1), (0, 7, 2, 2),
        (1, 6, 2, 2), (1, 7, 1, 1), (2, 5, 2, 2),
        (2, 7, 0, 0), (3, 4, 2, 2), (3, 5, 0, 0),
        (3, 5, 0, 1), (3, 5, 1, 0), (3, 5, 1, 1),
        (3, 6, 0, 0), (3, 6, 0, 1), (3, 6, 1, 0),
        (3, 6, 1, 1), (4, 5, 0, 0), (4, 5, 0, 1),
        (4, 5, 1, 0), (4, 5, 1, 1), (4, 6, 0, 0),
        (4, 6, 0, 1), (4, 6, 1, 0), (4, 6, 1, 1),
    }),
    2: frozenset({
        (0, 1, 0, 0), (0, 2, 2, 1), (0, 7, 1, 1),
        (0, 7, 2, 2), (1, 6, 1, 1), (1, 6, 2, 2),
        (2, 4, 1, 1), (2, 4, 1, 2), (2, 4, 2, 1),
        (2, 4, 2, 2), (2, 5, 1, 1), (2, 5, 1, 2),
        (2, 5, 2, 1), (2, 5, 2, 2), (2, 7, 0, 0),
        (3, 4, 1, 1), (3, 4, 1, 2), (3, 4, 2, 1),
        (3, 4, 2, 2), (3, 5, 1, 1), (3, 5, 1, 2),
        (3, 5, 2, 1), (3, 5, 2, 2), (3, 6, 0, 0),
        (4, 5, 0, 0),
    }),
}


ZERO_WORDS = {
    1: (1, 1, 1, 0, 0, 0, 0, 1),
    2: (1, 2, 1, 1, 1, 1, 2, 1),
}


PURE_COLORS = {1: 0, 2: 1}


TRANSLATIONS = {
    # target_multiplier * pure_fibre = zero_multiplier * zero_fibre
    1: {
        "target_multiplier": ((0, 2, 1, 1), (1, 7, 1, 1)),
        "zero_multiplier": ((0, 1, 0, 0), (2, 7, 0, 0)),
    },
    2: {
        "target_multiplier": ((1, 6, 2, 2),),
        "zero_multiplier": ((1, 6, 1, 1),),
    },
}


NEGATIVE_PHASE_CELLS = {
    1: frozenset({
        (4, 6, 0, 0), (4, 6, 0, 1),
        (4, 6, 1, 0), (4, 6, 1, 1),
    }),
    2: frozenset({
        (3, 5, 1, 1), (3, 5, 1, 2),
        (3, 5, 2, 1), (3, 5, 2, 2),
    }),
}


EXPECTED_HISTOGRAMS = {
    1: {
        "full:target:1": 1,
        "full:target:2": 2,
        "full:zero:0": 6528,
        "full:zero:2": 30,
        "residual:target:2": 1,
        "residual:zero:0": 713,
        "residual:zero:2": 15,
    },
    2: {
        "full:target:1": 1,
        "full:target:2": 2,
        "full:zero:0": 6496,
        "full:zero:2": 62,
        "residual:target:1": 1,
        "residual:zero:0": 728,
    },
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def multiply(left, right):
    return tuple(sorted(left + right))


def scale_fibre(fibre, monomial):
    answer = Counter()
    for term in fibre:
        answer[multiply(term, monomial)] += 1
    return answer


def phase_audit(head, support):
    cells = tuple(sorted(support))
    cell_index = {cell: index for index, cell in enumerate(cells)}
    rows = []
    unique = set()

    for residual_word in product(base.COLORS, repeat=6):
        word = (0, 0) + residual_word
        target = len(set(residual_word)) == 1 and residual_word[0] == 0
        terms = base.monomials(word, base.MATCHINGS6, support)
        if target or not terms:
            continue
        require(len(terms) == 2, "a residual zero fibre stopped being binomial")
        row = [0] * len(cells)
        for cell in terms[0]:
            row[cell_index[cell]] += 1
        for cell in terms[1]:
            row[cell_index[cell]] -= 1
        row = tuple(row)
        rows.append(row)
    for word in product(base.COLORS, repeat=8):
        target = len(set(word)) == 1
        terms = base.monomials(word, base.MATCHINGS8, support)
        if target or not terms:
            continue
        require(len(terms) == 2, "a full zero fibre stopped being binomial")
        row = [0] * len(cells)
        for cell in terms[0]:
            row[cell_index[cell]] += 1
        for cell in terms[1]:
            row[cell_index[cell]] -= 1
        row = tuple(row)
        rows.append(row)

    for row in rows:
        first = next(value for value in row if value)
        unique.add(row if first > 0 else tuple(-value for value in row))
    # A concrete sign assignment is stronger and more portable than relying
    # on a solver/HNF package: the four displayed cells have weight -1 and
    # every other support cell has weight +1.  Each zero binomial then has
    # opposite term signs.
    negative = NEGATIVE_PHASE_CELLS[head]
    require(negative <= support, "a negative phase cell left the support")
    for row in rows:
        phase = sum(row[cell_index[cell]] for cell in negative)
        require(phase & 1, "the explicit +/-1 phase stopped cancelling a row")

    basis = {}
    for row in rows:
        mask = sum(
            1 << index for index, value in enumerate(row) if value & 1
        )
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = mask
                break
            mask ^= basis[pivot]
    require(len(unique) == 16 and len(basis) == 9,
            "the mixed character ledger changed")
    return len(rows), len(unique), len(basis)


def audit_packet(head):
    support = PACKETS[head]
    fixed = base.fixed_cells(head)
    require(fixed <= support, f"head {head}: fixed matrix units disappeared")
    require(len(support) == (24 if head == 1 else 25),
            f"head {head}: support size changed")
    require({cell for cell in support if cell[:2] == (base.P, base.R)}
            == {(base.P, base.R, head, 1)},
            f"head {head}: shared block is no longer E_head,1")
    require(not any(cell[0] == base.P and cell[2] == 0
                    for cell in support if cell[:2] != (base.P, base.Q)),
            f"head {head}: the Lemma-E p_0 row is no longer zero")

    require(not base.support_shadow_violations(support),
            f"head {head}: support shadow became infeasible")
    histogram = base.serial_histogram(base.support_histogram(support))
    require(histogram == EXPECTED_HISTOGRAMS[head],
            f"head {head}: support histogram changed")

    deletion_witnesses = {}
    for cell in sorted(support - fixed):
        violations = base.support_shadow_violations(support - {cell})
        require(violations,
                f"head {head}: cell became deletion-redundant: {cell}")
        kind, word, count, target = violations[0]
        deletion_witnesses[str(cell)] = (
            kind, "".join(map(str, word)), count, target
        )

    pure_word = (PURE_COLORS[head],) * 8
    pure_fibre = base.monomials(pure_word, base.MATCHINGS8, support)
    zero_word = ZERO_WORDS[head]
    zero_fibre = base.monomials(zero_word, base.MATCHINGS8, support)
    require(len(pure_fibre) == len(zero_fibre) == 2,
            f"head {head}: translated fibres stopped being binomial")
    translation = TRANSLATIONS[head]
    target_multiplier = tuple(sorted(translation["target_multiplier"]))
    zero_multiplier = tuple(sorted(translation["zero_multiplier"]))
    require(set(target_multiplier) <= support,
            f"head {head}: target multiplier is not a support unit")
    require(set(zero_multiplier) <= support,
            f"head {head}: zero multiplier is not a support unit")
    require(scale_fibre(pure_fibre, target_multiplier)
            == scale_fibre(zero_fibre, zero_multiplier),
            f"head {head}: translated-fibre polynomial identity changed")

    phase_rows, unique_rows, exponent_rank = phase_audit(head, support)
    return {
        "head": head,
        "cells": len(support),
        "histogram": histogram,
        "deletion_witnesses": deletion_witnesses,
        "mixed_phase": {
            "binomial_rows": phase_rows,
            "unique_up_to_sign": unique_rows,
            "gf2_exponent_rank": exponent_rank,
            "negative_phase_cells": [
                list(cell) for cell in sorted(NEGATIVE_PHASE_CELLS[head])
            ],
            "consistent": True,
        },
        "translated_identity": {
            "pure_word": "".join(map(str, pure_word)),
            "zero_word": "".join(map(str, zero_word)),
            "pure_terms": [[list(cell) for cell in term]
                           for term in pure_fibre],
            "zero_terms": [[list(cell) for cell in term]
                           for term in zero_fibre],
            "identity": "target_multiplier*P=zero_multiplier*Z",
            "target_multiplier": [list(cell) for cell in target_multiplier],
            "zero_multiplier": [list(cell) for cell in zero_multiplier],
            "consequence": "P=1 and Z=0 force a support-torus unit to vanish",
        },
    }


def main():
    packets = [audit_packet(head) for head in (1, 2)]
    ledger = {
        "packets": packets,
        "verdict": {
            "support_shadow": "SAT on 24/25-cell deletion-irredundant faces",
            "mixed_binomial_phase": "consistent on both faces",
            "coefficient_tori": "empty by one translated pure/zero fibre",
            "global_packet": "open outside the two frozen faces",
        },
        "scope": (
            "literal normalized Lemma-E unary-top packet; exact sparse-face "
            "exclusions, not an exhaustive support theorem or rational point"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"translated-face ledger changed: {digest}")
    print("N=8 Lemma-E unary-top translated faces: PASS")
    print("support shadows: 24/25 cells; deletion-irredundant")
    print("mixed binomial phases: consistent (45/62 rows, 16 unique)")
    print("coefficient tori: EMPTY by one translated pure/zero fibre")
    print("global normalized packet: OPEN outside the frozen faces")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
