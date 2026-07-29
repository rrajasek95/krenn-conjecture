#!/usr/bin/env python3
r"""Search the full five-vertex K4 vertex-expansion gadget.

Let C={0,...,4} be the replacement of one K4 vertex and let the three
outside terminals be 5,6,7.  The terminal r is 5+r.  We allow every
internal edge of C and every edge from C to a terminal, but keep the three
old K4 edges between terminals out of the variables.  The desired local
identities are

  K_r = e_r^{\otimes C} tensor e_r       (r=0,1,2),
  T_3 = 0,

where K_r is the sum of matchings with the unique crossing edge ending at
terminal r and T_3 is the sum of matchings using all three boundary
terminals.  With old edge E_rr between the other two terminals these two
identities give GHZ_3 on eight vertices exactly.

This is only a numerical discovery tool.  It uses an explicit adjoint of
the tensor-network evaluation, so a trial costs roughly one forward and
one reverse pass rather than hundreds of finite differences.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


Q = 3
C = tuple(range(5))
TERMINALS = tuple(range(5, 8))
INTERNAL_EDGES = tuple(itertools.combinations(C, 2))
BOUNDARY_EDGES = tuple((c, u) for c in C for u in TERMINALS)
EDGES = INTERNAL_EDGES + BOUNDARY_EDGES
EDGE_INDEX = {edge: i for i, edge in enumerate(EDGES)}


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


def one_cross_terms(r: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    u = 5 + r
    answer = []
    for c in C:
        for matching in perfect_matchings(tuple(v for v in C if v != c)):
            answer.append(tuple(matching) + ((c, u),))
    return tuple(answer)


def three_cross_terms() -> tuple[tuple[tuple[int, int], ...], ...]:
    answer = []
    for chosen in itertools.permutations(C, 3):
        remaining = tuple(v for v in C if v not in chosen)
        internal = (min(remaining), max(remaining))
        boundary = tuple((chosen[r], 5 + r) for r in range(3))
        answer.append((internal,) + boundary)
    return tuple(answer)


ONE_TERMS = tuple(one_cross_terms(r) for r in range(3))
THREE_TERMS = three_cross_terms()
HIGH_WEIGHT = 1.0


def edge_axes(edge: tuple[int, int], vertices: tuple[int, ...]) -> tuple[int, int]:
    return vertices.index(edge[0]), vertices.index(edge[1])


def term_tensor(
    matrices: np.ndarray,
    term: tuple[tuple[int, int], ...],
    vertices: tuple[int, ...],
) -> np.ndarray:
    """Outer product of disjoint edge matrices in natural vertex order."""
    letters = "abcdefgh"
    inputs = []
    operands = []
    for edge in term:
        a, b = edge_axes(edge, vertices)
        inputs.append(letters[a] + letters[b])
        operands.append(matrices[EDGE_INDEX[edge]])
    equation = ",".join(inputs) + "->" + letters[: len(vertices)]
    return np.einsum(equation, *operands, optimize=True)


def term_adjoint(
    residual: np.ndarray,
    matrices: np.ndarray,
    term: tuple[tuple[int, int], ...],
    vertices: tuple[int, ...],
    gradient: np.ndarray,
) -> None:
    """Accumulate J(term)^H residual into the edge-matrix gradient."""
    letters = "abcdefgh"
    full = letters[: len(vertices)]
    for differentiated in term:
        operands = [residual]
        inputs = [full]
        for edge in term:
            if edge == differentiated:
                continue
            a, b = edge_axes(edge, vertices)
            inputs.append(letters[a] + letters[b])
            operands.append(np.conjugate(matrices[EDGE_INDEX[edge]]))
        a, b = edge_axes(differentiated, vertices)
        equation = ",".join(inputs) + "->" + letters[a] + letters[b]
        gradient[EDGE_INDEX[differentiated]] += np.einsum(
            equation, *operands, optimize=True
        )


ONE_VERTICES = tuple(C) + (5,)  # terminal label is replaced per r below
ALL_VERTICES = tuple(C) + TERMINALS


def target_one(r: int) -> np.ndarray:
    result = np.zeros((Q,) * 6, dtype=np.complex128)
    result[(r,) * 6] = 1
    return result


TARGETS = tuple(target_one(r) for r in range(3))


def unpack(x: np.ndarray) -> np.ndarray:
    count = len(EDGES) * Q * Q
    return (x[:count] + 1j * x[count:]).reshape(len(EDGES), Q, Q)


def objective_and_gradient(x: np.ndarray) -> tuple[float, np.ndarray]:
    matrices = unpack(x)
    residuals: list[tuple[np.ndarray, tuple[tuple[tuple[int, int], ...], ...], tuple[int, ...]]] = []

    for r in range(3):
        vertices = tuple(C) + (5 + r,)
        value = np.zeros((Q,) * 6, dtype=np.complex128)
        for term in ONE_TERMS[r]:
            value += term_tensor(matrices, term, vertices)
        residuals.append((value - TARGETS[r], ONE_TERMS[r], vertices))

    high = np.zeros((Q,) * 8, dtype=np.complex128)
    for term in THREE_TERMS:
        high += term_tensor(matrices, term, ALL_VERTICES)
    residuals.append((np.sqrt(HIGH_WEIGHT) * high, THREE_TERMS, ALL_VERTICES))

    value = float(sum(np.vdot(residual, residual).real for residual, _, _ in residuals))
    complex_gradient = np.zeros_like(matrices)
    for residual, terms, vertices in residuals:
        # The high-sector residual was multiplied by sqrt(HIGH_WEIGHT), so
        # its Jacobian must receive the same factor in the adjoint pass.
        if terms is THREE_TERMS:
            residual = np.sqrt(HIGH_WEIGHT) * residual
        for term in terms:
            term_adjoint(residual, matrices, term, vertices, complex_gradient)

    # For holomorphic residuals and f=||residual||^2, if g=J^H r then
    # grad_(Re z) f=2 Re g and grad_(Im z) f=2 Im g.
    flat = complex_gradient.ravel()
    gradient = 2 * np.r_[flat.real, flat.imag]
    return value, gradient


def sector_errors(matrices: np.ndarray) -> tuple[float, float, float, float]:
    errors = []
    for r in range(3):
        vertices = tuple(C) + (5 + r,)
        value = np.zeros((Q,) * 6, dtype=np.complex128)
        for term in ONE_TERMS[r]:
            value += term_tensor(matrices, term, vertices)
        errors.append(float(np.vdot(value - TARGETS[r], value - TARGETS[r]).real))
    high = np.zeros((Q,) * 8, dtype=np.complex128)
    for term in THREE_TERMS:
        high += term_tensor(matrices, term, ALL_VERTICES)
    errors.append(float(np.vdot(high, high).real))
    return tuple(errors)  # type: ignore[return-value]


def audit_gradient(rng: np.random.Generator) -> None:
    count = len(EDGES) * Q * Q
    x = rng.normal(scale=0.2, size=2 * count)
    value, gradient = objective_and_gradient(x)
    direction = rng.normal(size=x.size)
    direction /= np.linalg.norm(direction)
    eps = 1e-6
    plus = objective_and_gradient(x + eps * direction)[0]
    minus = objective_and_gradient(x - eps * direction)[0]
    finite = (plus - minus) / (2 * eps)
    exact = float(gradient @ direction)
    rel = abs(finite - exact) / max(1, abs(finite), abs(exact))
    print(
        f"gradient audit value={value:.9g} adjoint={exact:.9g} "
        f"finite={finite:.9g} rel={rel:.3g}",
        flush=True,
    )
    if rel > 2e-6:
        raise AssertionError("adjoint gradient check failed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--maxiter", type=int, default=4000)
    parser.add_argument("--scale", type=float, default=0.35)
    parser.add_argument("--audit-gradient", action="store_true")
    parser.add_argument("--save-best", type=str)
    parser.add_argument("--initial", type=str)
    parser.add_argument("--high-weight", type=float, default=1.0)
    args = parser.parse_args()

    global HIGH_WEIGHT
    HIGH_WEIGHT = args.high_weight
    rng = np.random.default_rng(args.seed)
    if args.audit_gradient:
        audit_gradient(rng)

    count = len(EDGES) * Q * Q
    best: tuple[float, np.ndarray, np.ndarray] | None = None
    for start in range(args.starts):
        if args.initial:
            initial = np.load(args.initial)["matrices"]
            z = np.asarray(initial, dtype=np.complex128).ravel()
            x0 = np.r_[z.real, z.imag]
            if start:
                x0 += rng.normal(scale=args.scale, size=x0.size)
        else:
            x0 = rng.normal(scale=args.scale, size=2 * count)
        fit = minimize(
            objective_and_gradient,
            x0,
            method="L-BFGS-B",
            jac=True,
            options={"maxiter": args.maxiter, "ftol": 1e-15, "gtol": 1e-10, "maxls": 40},
        )
        value, gradient = objective_and_gradient(fit.x)
        matrices = unpack(fit.x)
        sectors = sector_errors(matrices)
        print(
            f"start={start} objective={value:.12g} rms={np.sqrt(value / 8748):.6g} "
            f"norm={np.linalg.norm(fit.x):.6g} grad={np.linalg.norm(gradient):.3g} "
            f"sectors={','.join(f'{v:.6g}' for v in sectors)} "
            f"nit={fit.nit} success={fit.success}",
            flush=True,
        )
        if best is None or value < best[0]:
            best = (value, fit.x.copy(), gradient.copy())
        if value < 1e-16 and np.linalg.norm(fit.x) < 1e5:
            np.savez(
                f"candidate_full_vertex_expansion_seed{args.seed + start}.npz",
                edges=np.asarray(EDGES),
                matrices=matrices,
                objective=value,
                gradient=gradient,
            )
    if args.save_best and best is not None:
        value, x, gradient = best
        np.savez(
            args.save_best,
            edges=np.asarray(EDGES),
            matrices=unpack(x),
            objective=value,
            gradient=gradient,
            sectors=np.asarray(sector_errors(unpack(x))),
        )


if __name__ == "__main__":
    main()
