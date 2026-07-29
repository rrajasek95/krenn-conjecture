#!/usr/bin/env python3
"""Finite-field reconnaissance for singular corank-two relation blocks.

This is a search aid, not a proof.  It samples endpoint star matrices and
tests the intrinsic rank-three live-line conditions described in
``notes/corank-two-local-block-classification.md``.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np


ORDERED = tuple((c, d) for c in range(3) for d in range(3) if c != d)


def inv_mod(a: int, prime: int) -> int:
    return pow(int(a) % prime, -1, prime)


def rank_mod(matrix: np.ndarray, prime: int) -> int:
    a = np.array(matrix, dtype=np.int64, copy=True) % prime
    row = 0
    for col in range(a.shape[1]):
        pivots = np.flatnonzero(a[row:, col])
        if not len(pivots):
            continue
        pivot = row + int(pivots[0])
        a[[row, pivot]] = a[[pivot, row]]
        a[row] = a[row] * inv_mod(a[row, col], prime) % prime
        for other in range(a.shape[0]):
            if other != row and a[other, col]:
                a[other] = (a[other] - a[other, col] * a[row]) % prime
        row += 1
        if row == a.shape[0]:
            break
    return row


def det3(matrix: np.ndarray, prime: int) -> int:
    a = matrix % prime
    return int(
        a[0, 0] * (a[1, 1] * a[2, 2] - a[1, 2] * a[2, 1])
        - a[0, 1] * (a[1, 0] * a[2, 2] - a[1, 2] * a[2, 0])
        + a[0, 2] * (a[1, 0] * a[2, 1] - a[1, 1] * a[2, 0])
    ) % prime


def block_columns(P: np.ndarray, S: np.ndarray, Q: np.ndarray,
                  T: np.ndarray, prime: int) -> np.ndarray:
    columns = []
    for c, d in ORDERED:
        value = np.outer(P[:, c], T[:, d]) + np.outer(S[:, d], Q[:, c])
        columns.append(value.reshape(9) % prime)
    return np.stack(columns, axis=1)


def basis_columns(matrix: np.ndarray, prime: int) -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for column in matrix.T:
        if rank_mod(np.stack(basis + [column], axis=1), prime) > len(basis):
            basis.append(column)
    return basis


def projective_coefficients(prime: int, dimension: int):
    for vector in itertools.product(range(prime), repeat=dimension):
        if not any(vector):
            continue
        first = next(entry for entry in vector if entry)
        if first == 1:
            yield vector


def common_right_kernel(A: np.ndarray, B: np.ndarray, prime: int) -> bool:
    return rank_mod(np.vstack((A, B)), prime) < 3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=3)
    parser.add_argument("--trials", type=int, default=1_000_000)
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument(
        "--all-singular", action="store_true",
        help="also require both secondary endpoint matrices to be singular",
    )
    parser.add_argument(
        "--one-primary-singular", action="store_true",
        help="require P singular but allow Q to be invertible",
    )
    parser.add_argument("--image-rank", type=int, choices=(2, 3), default=3)
    args = parser.parse_args()
    p = args.prime
    rng = np.random.default_rng(args.seed)
    rank_three = 0
    live_nets = 0

    for trial in range(1, args.trials + 1):
        P, S, Q, T = [rng.integers(p, size=(3, 3), dtype=np.int64)
                      for _ in range(4)]
        # Target the genuinely singular stratum, with no desired conclusion
        # already visible at either endpoint.
        if rank_mod(P, p) == 3:
            continue
        if not args.one_primary_singular and rank_mod(Q, p) == 3:
            continue
        if args.all_singular and (rank_mod(S, p) == 3 or rank_mod(T, p) == 3):
            continue
        if common_right_kernel(P, S, p) or common_right_kernel(Q, T, p):
            continue
        L = block_columns(P, S, Q, T, p)
        if rank_mod(L, p) != args.image_rank:
            continue
        rank_three += 1

        row_indices = [[k for k, (c, d) in enumerate(ORDERED) if c == fixed]
                       for fixed in range(3)]
        col_indices = [[k for k, (c, d) in enumerate(ORDERED) if d == fixed]
                       for fixed in range(3)]
        planes = row_indices + col_indices
        required_plane_rank = 2 if args.image_rank == 3 else 1
        if any(rank_mod(L[:, indices], p) != required_plane_rank
               for indices in planes):
            continue

        basis = basis_columns(L, p)
        assert len(basis) == args.image_rank
        valid_h = []
        for coeffs in projective_coefficients(p, args.image_rank):
            h = sum((coefficient * vector for coefficient, vector
                     in zip(coeffs, basis)), np.zeros(9, dtype=np.int64)) % p
            if det3(h.reshape(3, 3), p) == 0:
                continue
            if any(rank_mod(np.column_stack((L[:, indices], h)), p)
                   == required_plane_rank for indices in planes):
                continue
            valid_h.append(h)
        if not valid_h:
            continue
        live_nets += 1
        print(f"FOUND trial={trial} prime={p} valid_h={len(valid_h)}")
        for name, matrix in (("P", P), ("S", S), ("Q", Q), ("T", T)):
            print(name, "rank", rank_mod(matrix, p))
            print(matrix)
        print("L rank", rank_mod(L, p))
        print("row/column image ranks",
              [rank_mod(L[:, indices], p) for indices in planes])
        print("H")
        print(valid_h[0].reshape(3, 3))
        return

    print({"trials": args.trials, "rank_three": rank_three,
           "live_nets": live_nets, "found": False})


if __name__ == "__main__":
    main()
