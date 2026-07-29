#!/usr/bin/env python3
r"""Search the necessary five-party column system for a K4 expansion.

Contract boundary terminal u_r of B^(r) against e_r^*.  Any full
copy-then-cancel gadget yields internal matrices X_ab and local vectors
b[c,r] satisfying

  sum_c b[c,r] tensor H_(C\c)(X) = e_r^tensor5,
  Q_X(b[:,0],b[:,1],b[:,2]) = 0.

The second tensor is the contraction of T3 at terminal colors (0,1,2).
This script searches that smaller necessary system with an exact analytic
adjoint.  Numerical output is not a proof.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


QDIM = 3
C = tuple(range(5))
IEDGES = tuple(itertools.combinations(C, 2))
IINDEX = {edge: i for i, edge in enumerate(IEDGES)}
HIGH_WEIGHT = 1.0


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for pos in range(1, len(vertices)):
        b = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for tail in perfect_matchings(rest):
            yield ((min(a, b), max(a, b)),) + tail


# A factor is (kind, first, second), where X uses an edge and b uses (c,r).
ONE_TERMS = tuple(
    tuple(
        (("b", c, r),) + tuple(("X", a, b) for a, b in matching)
        for c in C
        for matching in perfect_matchings(tuple(v for v in C if v != c))
    )
    for r in range(3)
)
THREE_TERMS = tuple(
    (("b", chosen[0], 0), ("b", chosen[1], 1), ("b", chosen[2], 2),
     ("X", *tuple(v for v in C if v not in chosen)))
    for chosen in itertools.permutations(C, 3)
)


def unpack(z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    complex_count = 10 * 9 + 5 * 3 * 3
    w = z[:complex_count] + 1j * z[complex_count:]
    x = w[:90].reshape(10, 3, 3)
    b = w[90:].reshape(5, 3, 3)
    return x, b


def factor_array(factor, x, b):
    kind, a, d = factor
    if kind == "X":
        return x[IINDEX[min(a, d), max(a, d)]]
    return b[a, d]


def factor_axes(factor):
    kind, a, d = factor
    if kind == "X":
        return (a, d)
    return (a,)


def term_tensor(term, x, b):
    letters = "abcde"
    inputs = []
    operands = []
    for factor in term:
        inputs.append("".join(letters[a] for a in factor_axes(factor)))
        operands.append(factor_array(factor, x, b))
    return np.einsum(",".join(inputs) + "->abcde", *operands, optimize=True)


def term_adjoint(residual, term, x, b, gx, gb):
    letters = "abcde"
    for differentiated in term:
        inputs = ["abcde"]
        operands = [residual]
        skipped = False
        for factor in term:
            if factor == differentiated and not skipped:
                skipped = True
                continue
            inputs.append("".join(letters[a] for a in factor_axes(factor)))
            operands.append(np.conjugate(factor_array(factor, x, b)))
        output = "".join(letters[a] for a in factor_axes(differentiated))
        value = np.einsum(",".join(inputs) + "->" + output, *operands, optimize=True)
        kind, a, d = differentiated
        if kind == "X":
            gx[IINDEX[min(a, d), max(a, d)]] += value
        else:
            gb[a, d] += value


TARGETS = []
for r in range(3):
    target = np.zeros((3,) * 5, dtype=np.complex128)
    target[(r,) * 5] = 1
    TARGETS.append(target)


def residuals(x, b):
    answer = []
    for r in range(3):
        value = np.zeros((3,) * 5, dtype=np.complex128)
        for term in ONE_TERMS[r]:
            value += term_tensor(term, x, b)
        answer.append(value - TARGETS[r])
    value = np.zeros((3,) * 5, dtype=np.complex128)
    for term in THREE_TERMS:
        value += term_tensor(term, x, b)
    answer.append(value)
    return answer


def objective_gradient(z):
    x, b = unpack(z)
    rs = residuals(x, b)
    weights = (1.0, 1.0, 1.0, HIGH_WEIGHT)
    value = float(sum(w * np.vdot(r, r).real for w, r in zip(weights, rs)))
    gx = np.zeros_like(x)
    gb = np.zeros_like(b)
    for terms, r, weight in zip(ONE_TERMS + (THREE_TERMS,), rs, weights):
        for term in terms:
            term_adjoint(weight * r, term, x, b, gx, gb)
    g = np.r_[gx.ravel(), gb.ravel()]
    return value, 2 * np.r_[g.real, g.imag]


def sector_errors(x, b):
    return tuple(float(np.vdot(r, r).real) for r in residuals(x, b))


def gradient_audit(rng):
    z = rng.normal(scale=0.2, size=270)
    value, gradient = objective_gradient(z)
    direction = rng.normal(size=z.size)
    direction /= np.linalg.norm(direction)
    eps = 1e-6
    finite = (
        objective_gradient(z + eps * direction)[0]
        - objective_gradient(z - eps * direction)[0]
    ) / (2 * eps)
    adjoint = float(gradient @ direction)
    relative = abs(finite - adjoint) / max(1, abs(finite), abs(adjoint))
    print(
        f"gradient audit value={value:.9g} adjoint={adjoint:.9g} "
        f"finite={finite:.9g} rel={relative:.3g}"
    )
    assert relative < 2e-6


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--maxiter", type=int, default=5000)
    parser.add_argument("--scale", type=float, default=0.35)
    parser.add_argument("--high-weight", type=float, default=1.0)
    parser.add_argument("--audit-gradient", action="store_true")
    parser.add_argument("--save-best", type=str)
    args = parser.parse_args()
    global HIGH_WEIGHT
    HIGH_WEIGHT = args.high_weight
    rng = np.random.default_rng(args.seed)
    if args.audit_gradient:
        gradient_audit(rng)

    best = None
    for start in range(args.starts):
        z0 = rng.normal(scale=args.scale, size=270)
        fit = minimize(
            objective_gradient,
            z0,
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": args.maxiter, "ftol": 1e-15, "gtol": 1e-10, "maxls": 50},
        )
        value, gradient = objective_gradient(fit.x)
        x, b = unpack(fit.x)
        sectors = sector_errors(x, b)
        print(
            f"start={start} objective={value:.12g} norm={np.linalg.norm(fit.x):.6g} "
            f"grad={np.linalg.norm(gradient):.3g} sectors="
            f"{','.join(f'{v:.6g}' for v in sectors)} nit={fit.nit} "
            f"success={fit.success}",
            flush=True,
        )
        if best is None or value < best[0]:
            best = (value, fit.x.copy(), gradient.copy())
    if args.save_best and best is not None:
        value, z, gradient = best
        x, b = unpack(z)
        np.savez(
            args.save_best,
            internal=x,
            boundary_vectors=b,
            objective=value,
            gradient=gradient,
            sectors=np.asarray(sector_errors(x, b)),
        )


if __name__ == "__main__":
    main()
