#!/usr/bin/env python3
"""STEP 4: the attainable-D2 space S vs the physically-realisable space W.

S = D2( ker(source, D1) )  inside the grade-forgotten pair space
W = shadow_2( committed physical inventory )

Both are computed in the SAME row coordinates (pairs of cells).  We then
compute dim(S), dim(W), dim(S+W), dim(S \\cap W) and locate -delta.
Arithmetic mod two independent primes (control).
"""
from collections import Counter, defaultdict
from itertools import combinations, product
import json
import sys

import common as C

PRIMES = [1_000_003, 999_983]


def reduce_mod(vector, basis, p, order):
    vector = {r: v % p for r, v in vector.items() if v % p}
    while vector:
        piv = min(vector, key=order)
        if piv not in basis:
            return vector, piv
        c = vector[piv]
        for r, v in basis[piv].items():
            x = (vector.get(r, 0) - c * v) % p
            if x:
                vector[r] = x
            else:
                vector.pop(r, None)
    return {}, None


def insert(vector, basis, p, order):
    red, piv = reduce_mod(vector, basis, p, order)
    if not red:
        return False, None
    inv = pow(red[piv], p - 2, p)
    basis[piv] = {r: v * inv % p for r, v in red.items()}
    return True, piv


def run(p):
    m = C.modules()
    cols, shifts = C.build_operator_columns(m, verbose=False)
    base, cm = m["base"], m["commutator"]

    # order: all constraint rows (kind 0,1) strictly before shadow rows (2)
    def order(row):
        return (row[0] >= 2, repr(row))

    by_shift = defaultdict(list)
    for (mdata, col), sh in zip(cols, shifts):
        by_shift[repr(sh)].append(col)

    constraint_rank = 0
    shadow_vectors = []
    for key in sorted(by_shift):
        basis = {}
        for col in by_shift[key]:
            added, piv = insert(dict(col), basis, p, order)
            if added and piv[0] == 2:
                assert all(r[0] == 2 for r in basis[piv]), \
                    "kernel-shadow pivot retained a constraint row"
                shadow_vectors.append(basis[piv])
        constraint_rank += sum(1 for piv in basis if piv[0] < 2)
    S = {}
    for v in shadow_vectors:
        insert(dict(v), S, p, order)

    # W: physical inventories
    def inv_words(words):
        mons, seen = [], set()
        for w in words:
            for mon in C.physical_row(base, w):
                if mon not in seen:
                    seen.add(mon)
                    mons.append(mon)
        return mons

    PURE, MIXED = cm.PURE_WORD, cm.MIXED_WORD
    TAIL_WORDS = [tuple(1 if i not in (2, 5) else (a if i == 2 else b)
                        for i in range(8))
                  for a in (1, 2) for b in (1, 2)]
    ALL_ROWS = None

    result = {"prime": p,
              "operator_columns": len(cols),
              "constraint_rank_source_plus_D1": constraint_rank,
              "attainable_D2_dim_S": len(S)}

    target = {(2, pair): int(v) % p
              for pair, v in cm.expected_second_shadow().items()}
    red, _ = reduce_mod(dict(target), S, p, order)
    result["minus_delta_in_S"] = not red

    for name, words in (("two active rows", [PURE, MIXED]),
                        ("tail orbit (4 words)", TAIL_WORDS)):
        mons = inv_words(words)
        Wcols = [{(2, pr): 1 for pr in C.shadow2_of_monomial(mon)}
                 for mon in mons]
        W = {}
        for c in Wcols:
            insert(dict(c), W, p, order)
        SW = dict(S)
        for c in Wcols:
            insert(dict(c), SW, p, order)
        red, _ = reduce_mod(dict(target), W, p, order)
        entry = {
            "monomials": len(mons),
            "dim_W": len(W),
            "dim_S_plus_W": len(SW),
            "dim_S_cap_W": len(S) + len(W) - len(SW),
            "minus_delta_in_W": not red,
        }
        result[name] = entry
    return result


out = []
for p in PRIMES:
    r = run(p)
    print(json.dumps(r, indent=1, sort_keys=True), flush=True)
    out.append(r)
json.dump(out, open("step4_attainable.json", "w"), indent=1, sort_keys=True)
