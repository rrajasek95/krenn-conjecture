#!/usr/bin/env python3
"""Exact audit of the simultaneous-diagonal flattening palette gate.

Complementary rank-r factorizations of Delta_r have an independent GL_r
gauge at every (unoriented) cut.  A source-valid columnwise fusion square is
much more rigid: if the Khatri--Rao columns of two invertible shore factors
land in the diagonal palette space, both factors are aligned monomial
matrices.

The companion note proves the uniform characteristic-zero statement.  This
checker:

* constructs dense, nonmonomial inverse factorizations for all seven cuts of
  Delta_(4,3) simultaneously;
* verifies that every complementary product is exactly the target
  flattening;
* computes the nonzero cross-palette fusion defect on every disjoint pair of
  proper shores; and
* exhausts GL_2(F_3)^2 and GL_3(F_2)^2, confirming that zero fusion defect
  leaves exactly the aligned monomial pairs.

Only exact Fraction / finite-field arithmetic is used.  Bare asserts are
deliberately avoided so ``python -O`` checks the same statements.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "computations/verify_global_cut_wick_invariant_boundary.py":
        "7aa7289cce09e86be8958263932e56a57c8cd7b565bb17ebfde6fdf9805925bd",
    "computations/verify_global_wick_top_invariant_counterguard.py":
        "192c03668e56262315e685f49c29fafeed071faf2a292dfdc94544fd7a5f4183",
    "computations/verify_target_flattening_essential_star_pair_bound.py":
        "56598490ae2868b35c1e73da7d543c61b4c071effc9798e83705cb255a298ad0",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def canonical(value):
    if isinstance(value, Fraction):
        return "F" + str(value)
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return [
            [canonical(key), canonical(value[key])]
            for key in sorted(value, key=repr)
        ]
    if isinstance(value, (tuple, list)):
        return [canonical(entry) for entry in value]
    raise RuntimeError("unsupported canonical value: %r" % (type(value),))


def content_hash(value):
    payload = json.dumps(canonical(value), sort_keys=True,
                         separators=(",", ":"))
    return sha256(payload.encode("ascii")).hexdigest()


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(len(matrix)))
                 for column in range(len(matrix[0])))


def multiply(left, right):
    require(not left or len(left[0]) == len(right),
            ("matrix product shape", len(left[0]) if left else 0, len(right)))
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(len(right)))
              for j in range(len(right[0])))
        for i in range(len(left))
    )


def identity(size):
    return tuple(tuple(Fraction(int(i == j)) for j in range(size))
                 for i in range(size))


def inverse(matrix):
    size = len(matrix)
    work = [
        [Fraction(entry) for entry in matrix[row]]
        + [Fraction(int(row == column)) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        require(pivot is not None, ("singular matrix", matrix))
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [entry / scale for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column])
            ]
    return tuple(tuple(row[size:]) for row in work)


def rank_fraction(matrix):
    work = [[Fraction(entry) for entry in row] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def diagonal_embedding(shore_size, palette=3):
    words = tuple(product(range(palette), repeat=shore_size))
    return tuple(
        tuple(Fraction(int(word == (colour,) * shore_size))
              for colour in range(palette))
        for word in words
    )


def cut_mask(shore):
    return sum(1 << site for site in shore)


def complement(shore, sites):
    shore = frozenset(shore)
    return tuple(site for site in sites if site not in shore)


def varying_dense_gauge(index):
    """A diagonal rescaling of a dense matrix with dense inverse."""
    base = (
        (Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(2), Fraction(4)),
        (Fraction(1), Fraction(3), Fraction(9)),
    )
    left = tuple(Fraction(index + row + 1) for row in range(3))
    right = tuple(Fraction(index + column + 4) for column in range(3))
    answer = tuple(
        tuple(left[row] * base[row][column] * right[column]
              for column in range(3))
        for row in range(3)
    )
    require(all(entry for row in answer for entry in row),
            "the dense gauge acquired a zero")
    inv = inverse(answer)
    require(all(entry for row in inv for entry in row),
            "the dense inverse acquired a zero")
    return answer


def all_cut_counterguard():
    sites = tuple(range(4))
    subsets = tuple(
        tuple(chosen)
        for size in range(1, len(sites))
        for chosen in combinations(sites, size)
    )
    gauges = {}
    unoriented = []
    for shore in subsets:
        if shore in gauges:
            continue
        other = complement(shore, sites)
        owner, mate = sorted((shore, other), key=cut_mask)
        gauge = varying_dense_gauge(len(unoriented) + 1)
        gauges[owner] = gauge
        gauges[mate] = inverse(transpose(gauge))
        unoriented.append((owner, mate))

    require(len(unoriented) == 7 and len(gauges) == 14,
            ("four-site cut count", len(unoriented), len(gauges)))
    factors = {
        shore: multiply(diagonal_embedding(len(shore)), gauges[shore])
        for shore in subsets
    }

    cut_ledger = []
    for shore in subsets:
        other = complement(shore, sites)
        actual = multiply(factors[shore], transpose(factors[other]))
        target = multiply(diagonal_embedding(len(shore)),
                          transpose(diagonal_embedding(len(other))))
        require(actual == target, ("inverse cut factorization", shore))
        require(all(entry for row in gauges[shore] for entry in row),
                ("cut gauge is not dense", shore))
        cut_ledger.append((shore, other, len(actual), len(actual[0])))

    # The cross-palette projection of the columnwise product.  A right-hand
    # transition by an invertible matrix cannot kill it: rank(Omega C)=rank
    # Omega.  Thus this is the exact fusion/associator obstruction.
    fusion_ledger = []
    for left in subsets:
        left_set = set(left)
        for right in subsets:
            if cut_mask(left) >= cut_mask(right) or left_set & set(right):
                continue
            union = tuple(sorted(left_set | set(right)))
            if len(union) == len(sites):
                continue
            cross = tuple(
                tuple(gauges[left][a][column] * gauges[right][b][column]
                      for column in range(3))
                for a in range(3) for b in range(3) if a != b
            )
            defect_rank = rank_fraction(cross)
            require(defect_rank > 0,
                    ("dense gauges accidentally fused", left, right))
            fusion_ledger.append((left, right, defect_rank))
    require(fusion_ledger, "no proper disjoint fusion pairs were audited")
    return {
        "unoriented_cut_count": len(unoriented),
        "oriented_cut_count": len(cut_ledger),
        "cut_shapes": sorted(set((row[2], row[3]) for row in cut_ledger)),
        "proper_disjoint_fusions": len(fusion_ledger),
        "fusion_defect_rank_histogram": {
            rank: sum(row[2] == rank for row in fusion_ledger)
            for rank in sorted(set(row[2] for row in fusion_ledger))
        },
        "first_dense_gauge": gauges[unoriented[0][0]],
        "first_dense_inverse_transpose": gauges[unoriented[0][1]],
    }


def rank_mod(matrix, prime):
    work = [[entry % prime for entry in row] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column] % prime), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inv = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [entry * inv % prime
                           for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column] % prime:
                continue
            multiple = work[row][column] % prime
            work[row] = [
                (entry - multiple * pivot_entry) % prime
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def monomial_permutation(matrix, prime):
    size = len(matrix)
    positions = []
    for column in range(size):
        support = tuple(row for row in range(size)
                        if matrix[row][column] % prime)
        if len(support) != 1:
            return None
        positions.append(support[0])
    if len(set(positions)) != size:
        return None
    return tuple(positions)


def fusion_zero(left, right, prime):
    size = len(left)
    return all(
        left[a][column] * right[b][column] % prime == 0
        for a in range(size) for b in range(size) if a != b
        for column in range(size)
    )


def finite_field_fusion_audit(size, prime, expected):
    matrices = []
    for entries in product(range(prime), repeat=size * size):
        matrix = tuple(tuple(entries[size * row + column]
                             for column in range(size))
                       for row in range(size))
        if rank_mod(matrix, prime) == size:
            matrices.append(matrix)

    hits = []
    for left in matrices:
        for right in matrices:
            if not fusion_zero(left, right, prime):
                continue
            left_permutation = monomial_permutation(left, prime)
            right_permutation = monomial_permutation(right, prime)
            require(left_permutation is not None,
                    ("fusion-zero left factor is nonmonomial", size, prime, left))
            require(right_permutation == left_permutation,
                    ("fusion-zero permutations are not aligned", size, prime,
                     left_permutation, right_permutation))
            hits.append((left, right))
    require(len(hits) == expected,
            ("finite fusion count", size, prime, len(hits), expected))
    return {
        "size": size,
        "prime": prime,
        "GL_size": len(matrices),
        "aligned_monomial_pairs": len(hits),
    }


def audit_pins():
    result = []
    for relative, expected in PINNED.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected,
                ("pinned dependency changed", relative, observed, expected))
        result.append((relative, observed))
    return tuple(result)


def main():
    ledger = {
        "pins": audit_pins(),
        "all_cut_counterguard": all_cut_counterguard(),
        "finite_fusion_audits": (
            finite_field_fusion_audit(2, 3, 32),
            finite_field_fusion_audit(3, 2, 6),
        ),
    }
    digest = content_hash(ledger)
    expected = "1a52ac63c0309d975df18c546b607436f14d37cbf25ed8bd9275cd32002a5735"
    require(digest == expected,
            ("unexpected ledger digest", digest, expected))
    print("simultaneous diagonal flattening palette fusion gate: PASS")
    print("all 7 four-site cuts admit dense independent inverse gauges")
    print("one source-valid fusion square forces aligned monomial axes")
    print("finite audits: GL2(F3)=48, GL3(F2)=168")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
