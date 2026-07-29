#!/usr/bin/env python3
"""Exact bookkeeping audit for the three-hole/Hessian quotient injection."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import random


def audit(size: int, seed: int) -> None:
    assert size % 2 == 0 and size >= 4
    rng = random.Random(seed)
    s = size // 2
    dim_bar = 2

    # Scalar stand-ins for arbitrary nonzero q_ik blocks.  Every asserted
    # identity is coefficientwise in the barred slot and in q_ik.
    q = {
        edge: Fraction(rng.randrange(1, 17), rng.randrange(1, 11))
        for edge in combinations(range(size), 2)
    }
    w = [
        tuple(Fraction(rng.randrange(-9, 10), rng.randrange(1, 8))
              for _ in range(dim_bar))
        for _ in range(size)
    ]
    u = tuple(sum((w[i][a] for i in range(size)), Fraction(0))
              for a in range(dim_bar))

    # Test against several quotient covectors phi.
    phis = [(Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
            (Fraction(2), Fraction(-3))]
    for phi in phis:
        alpha = [sum(phi[a] * w[i][a] for a in range(dim_bar))
                 for i in range(size)]
        total = sum(alpha, Fraction(0))
        beta = [-value + total / (2 * s) for value in alpha]
        assert sum(beta, Fraction(0)) == 0
        for i, k in combinations(range(size), 2):
            contracted_t = -(alpha[i] + alpha[k]) * q[i, k]
            hessian_kernel_block = contracted_t + total * q[i, k] / s
            gauge_block = (beta[i] + beta[k]) * q[i, k]
            assert hessian_kernel_block == gauge_block

    # Reverse reconstruction.  Start from vector-valued zero-sum beta_i
    # and u, construct T via (17), then recover the Psi expansion gauges.
    b = [
        [Fraction(rng.randrange(-8, 9), rng.randrange(1, 7))
         for _ in range(dim_bar)]
        for _ in range(size - 1)
    ]
    b.append([-sum((b[i][a] for i in range(size - 1)), Fraction(0))
              for a in range(dim_bar)])
    assert all(sum((b[i][a] for i in range(size)), Fraction(0)) == 0
               for a in range(dim_bar))
    u2 = tuple(Fraction(rng.randrange(-8, 9), rng.randrange(1, 7))
               for _ in range(dim_bar))
    w2 = [tuple(-b[i][a] + u2[a] / (2 * s)
                for a in range(dim_bar)) for i in range(size)]
    assert all(sum((w2[i][a] for i in range(size)), Fraction(0)) == u2[a]
               for a in range(dim_bar))
    for i, k in combinations(range(size), 2):
        tensor_from_b = tuple(
            (b[i][a] + b[k][a] - u2[a] / s) * q[i, k]
            for a in range(dim_bar)
        )
        tensor_from_w = tuple(
            -(w2[i][a] + w2[k][a]) * q[i, k]
            for a in range(dim_bar)
        )
        assert tensor_from_b == tensor_from_w

    # Euler normalization H_q(q)=s C follows from factorials:
    # q*q^(s-1)/(s-1)! = s*q^s/s!.
    lhs_factor = Fraction(1, 1)
    rhs_factor = Fraction(s, 1)
    # Relative to C=q^s/s!, lhs has factor s!/((s-1)!)=s.
    for value in range(2, s + 1):
        lhs_factor *= value
    for value in range(2, s):
        rhs_factor *= value
    assert lhs_factor == rhs_factor


def main() -> None:
    for size in (4, 6, 8):
        audit(size, 1000 + size)
    print("PASS three-hole contraction, gauge descent, and reconstruction")


if __name__ == "__main__":
    main()
