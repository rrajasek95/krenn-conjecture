#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1 task B: the 20 splitting systems, machine-usable.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

A splitting pattern is a multiset {l_1,l_2,l_3} from {s, kappa_0, kappa_1,
kappa_2}; there are C(6,3) = 20.  Because the cap error is tensor valued,
"E = c * l_1 l_2 l_3" means: there is a tensor T in (x)_{u in U} V_u with

        E_w(K) = T_w * (l_1 l_2 l_3)(K)     for every boundary word w,

i.e. the 729 x 165 coefficient matrix C of E satisfies

        C = T . v^T,      v = coefficient vector of l_1 l_2 l_3,

so the system on the SOURCE variables is exactly

   (P1) rank [ C ; v ] = 1     <=>   all 2x2 minors of the 730 x 165 matrix
                                     obtained by appending v to C vanish;
   (P2) C != 0                 (otherwise the pair is in plan case (c)).

kappa_c is the coordinate form K_cc, so v depends on the source only
through the nine entries a_ij = A_pq[i][j] of the pair block (s = sum a_ij
K_ij).  Writing n_s for the multiplicity of s in the pattern:

  n_s = 0 (10 patterns):  v is the single monomial K_{c1c1}K_{c2c2}K_{c3c3},
                          support 1, so 164 of the 165 columns of C must
                          vanish identically -- 729*164 equations of
                          bidegree (6 in A, 0 in a);
  n_s = 1 (6 patterns):   support 9,  v[m] = a_k;
  n_s = 2 (3 patterns):   support 45, v[m] = mult * a_{k1} a_{k2};
  n_s = 3 (1 pattern):    support 165, v[m] = mult * a_{k1}a_{k2}a_{k3}.

In every case a row of C carries exactly 164 independent conditions, so the
pattern system is 729*164 = 119,556 polynomial relations in the 252
endpoint-ordered source coordinates, plus the open condition C != 0.

Measured collapse: none of the 120,285 entries C[w][m] vanishes identically
in the source (checked on random exact sources); the entire "site-algebra
collapse" shows up as a RANK drop -- rank C = 136 < 165 for generic sources
(and 0..6 on the committed near-exact eight-site source).

The JSON written by this module (``splitting_systems.json``) is the
machine-usable form for P2/P4: for each pattern it carries v as an exact
polynomial in the pair-block entries, the support/hard-zero split, the
relation schema, and a pinned reference instance of C.

Run: python3 wsplit_patterns.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from itertools import combinations_with_replacement

import wsplit_core as core
from wsplit_core import (CUBIC_MONOMIALS, MONOMIAL_INDEX, NCAP, WORDS,
                         dense_rows, error_matrix, kidx, require)
from wsplit_dichotomy import PATTERNS


def a_index(i: int, j: int) -> int:
    """Index of the pair-block entry a_ij = A_pq[i][j] (same as kidx)."""
    return kidx(i, j)


def pattern_vector(pattern) -> dict:
    """v as {cubic monomial -> {a-monomial -> integer coefficient}}.

    a-monomials are sorted tuples of pair-block indices; the empty tuple is
    the constant 1.
    """
    kappas = [name for name in pattern if name.startswith("kappa")]
    n_s = sum(1 for name in pattern if name == "s")
    fixed = tuple(sorted(kidx(int(name[-1]), int(name[-1])) for name in kappas))
    out: dict = {}
    for combo in combinations_with_replacement(range(NCAP), n_s):
        mono = tuple(sorted(fixed + combo))
        # multinomial coefficient of the monomial in s^{n_s}
        counts: dict = {}
        for k in combo:
            counts[k] = counts.get(k, 0) + 1
        coefficient = 1
        remaining = n_s
        for value in counts.values():
            from math import comb
            coefficient *= comb(remaining, value)
            remaining -= value
        entry = out.setdefault(mono, {})
        key = tuple(sorted(combo))
        entry[key] = entry.get(key, 0) + coefficient
    return out


def pattern_record(pattern) -> dict:
    v = pattern_vector(pattern)
    support = sorted(v)
    n_s = sum(1 for name in pattern if name == "s")
    hard_zero = [m for m in CUBIC_MONOMIALS if m not in v]
    return {
        "pattern": list(pattern),
        "s_multiplicity": n_s,
        "kappa_colours": [int(name[-1]) for name in pattern
                          if name.startswith("kappa")],
        "v_support_size": len(support),
        "hard_zero_monomial_count": len(hard_zero),
        "equations_per_word": 164,
        "total_equations": 729 * 164,
        "v": {
            "".join(f"K{m // 3}{m % 3}" for m in mono): {
                ("1" if not amono else
                 "*".join(f"a{k // 3}{k % 3}" for k in amono)): coefficient
                for amono, coefficient in terms.items()
            }
            for mono, terms in sorted(v.items())
        },
        "hard_zero_monomials": [
            "".join(f"K{k // 3}{k % 3}" for k in mono) for mono in hard_zero
        ],
        "relations": {
            "hard_zeros":
                "C[w][m] = 0 for every word w and every m in "
                "hard_zero_monomials (degree 6 in the source entries)",
            "proportionality":
                "C[w][m] * v[m'] - C[w][m'] * v[m] = 0 for every word w and "
                "all m, m' in the support of v (degree 6+n_s)",
            "cross_word_rank_one":
                "C[w][m] * C[w'][m'] - C[w][m'] * C[w'][m] = 0 "
                "(implied by the two above when v != 0)",
            "nondegeneracy": "C != 0, else the pair is in case (c)",
        },
    }


def reference_instance() -> dict:
    """A pinned integer source with a hash of its exact C matrix."""
    src = core.zero_source()
    value = 1
    for key in sorted(src):
        for i in range(3):
            for j in range(3):
                src[key][i][j] = ((value * 7919) % 11) - 5
                value += 1
    matrix = error_matrix(src)
    rows = dense_rows(matrix)
    digest = hashlib.sha256(
        json.dumps(rows, separators=(",", ":")).encode()).hexdigest()
    nonzero = [r for r in rows if any(r)]
    sample = {
        "word_000000": {
            "".join(f"K{m // 3}{m % 3}" for m in mono): str(coef)
            for mono, coef in sorted(matrix[WORDS[0]].items())
        },
        "word_012012": {
            "".join(f"K{m // 3}{m % 3}" for m in mono): str(coef)
            for mono, coef in sorted(matrix[(0, 1, 2, 0, 1, 2)].items())
        },
    }
    return {
        "source": {f"A_{u}_{v}": src[(u, v)] for u, v in sorted(src)},
        "C_sha256": digest,
        "nonzero_words": len(nonzero),
        "sample_rows": sample,
    }


def main() -> int:
    records = [pattern_record(pattern) for pattern in PATTERNS]
    by_class: dict = {}
    for rec in records:
        by_class.setdefault(rec["s_multiplicity"], []).append(rec)
    print("== P1 task B: the 20 splitting systems ==")
    for n_s in sorted(by_class):
        rec = by_class[n_s][0]
        print(f"  s-multiplicity {n_s}: {len(by_class[n_s]):2d} patterns, "
              f"|supp v| = {rec['v_support_size']:3d}, "
              f"hard-zero columns = {rec['hard_zero_monomial_count']:3d}, "
              f"equations/word = {rec['equations_per_word']}")
    require(sum(len(v) for v in by_class.values()) == 20, by_class)

    ref = reference_instance()
    payload = {
        "unaudited_probe": True,
        "pinned_head": "86a9479bef38169bbfd8d9100c6d81ce4c66209a",
        "conventions": {
            "sites": {"P": 0, "Q": 1, "U": list(core.U)},
            "cap_coordinates": "K_ij, i = P-colour, j = Q-colour, k = 3i+j",
            "pair_block_entries": "a_ij = A_pq[i][j] (so s = sum a_ij K_ij)",
            "C": "729 x 165 matrix, rows = boundary words on U in "
                 "itertools.product((0,1,2), repeat=6) order, columns = "
                 "itertools.combinations_with_replacement(range(9), 3) order",
            "E": "6E = [3 s r^2 x + r^3] full-U-support component",
        },
        "patterns": records,
        "reference_instance": ref,
    }
    with open("splitting_systems.json", "w") as handle:
        json.dump(payload, handle, indent=1, sort_keys=True, default=str)
    print(f"  reference instance C sha256 = {ref['C_sha256'][:32]}...")
    print("wrote splitting_systems.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
