#!/usr/bin/env python3
r"""Numerically search for a five-vertex color-preserving expansion gadget.

The boundary terminals are 0,1,2 and the internal vertices are 3,4.  Only
the six terminal--internal matrices are allowed.  Deleting terminal r must
leave the four-party tensor e_r^{\otimes 4}.  If such a finite solution
exists, replacing a vertex by this gadget transports any q=3 realization
to one four vertices larger; numerical output is only a discovery aid.

The system is now known to be exactly impossible: after attaching the three
coordinate interface edges and merging their outside endpoints its support
is K_(3,3), whose contraction would make a 3x3 vector permanent equal GHZ_3.
See notes/vertex-expansion-gadget-obstruction.md.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


Q = 3
TERMINALS = (0, 1, 2)
INTERNAL = (3, 4)
EDGES = tuple((u, v) for u in TERMINALS for v in INTERNAL)
EDGE_INDEX = {edge: i for i, edge in enumerate(EDGES)}
COLORINGS = tuple(itertools.product(range(Q), repeat=4))


def unpack(z: np.ndarray) -> np.ndarray:
    return z.reshape(len(EDGES), Q, Q)


def boundary_tensor(matrices: np.ndarray, deleted: int) -> np.ndarray:
    vertices = tuple(v for v in range(5) if v != deleted)
    answer = np.zeros((Q,) * 4, dtype=matrices.dtype)
    a, b = (v for v in TERMINALS if v != deleted)
    # The remaining graph is K_{2,2}, with its two perfect matchings.
    for coloring in COLORINGS:
        c = dict(zip(vertices, coloring, strict=True))
        value = (
            matrices[EDGE_INDEX[(a, 3)], c[a], c[3]]
            * matrices[EDGE_INDEX[(b, 4)], c[b], c[4]]
            + matrices[EDGE_INDEX[(a, 4)], c[a], c[4]]
            * matrices[EDGE_INDEX[(b, 3)], c[b], c[3]]
        )
        answer[coloring] = value
    return answer


def target(deleted: int) -> np.ndarray:
    result = np.zeros((Q,) * 4)
    result[(deleted,) * 4] = 1.0
    return result


def complex_residual(x: np.ndarray) -> np.ndarray:
    count = len(EDGES) * Q * Q
    z = x[:count] + 1j * x[count:]
    matrices = unpack(z)
    residual = np.concatenate(
        [(boundary_tensor(matrices, r) - target(r)).ravel() for r in TERMINALS]
    )
    return np.r_[residual.real, residual.imag]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=12)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-nfev", type=int, default=10000)
    parser.add_argument("--scale", type=float, default=0.5)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    count = len(EDGES) * Q * Q
    for start in range(args.starts):
        x0 = rng.normal(scale=args.scale, size=2 * count)
        fit = least_squares(
            complex_residual,
            x0,
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
            tr_solver="lsmr",
        )
        raw = complex_residual(fit.x)
        print(
            f"start={start} cost={fit.cost:.12g} max={np.max(np.abs(raw)):.6g} "
            f"norm={np.linalg.norm(fit.x):.6g} opt={fit.optimality:.3g} "
            f"nfev={fit.nfev}",
            flush=True,
        )
        if np.max(np.abs(raw)) < 1e-8 and np.linalg.norm(fit.x) < 1e4:
            z = fit.x[:count] + 1j * fit.x[count:]
            np.savez(
                f"candidate_vertex_expansion_seed{args.seed + start}.npz",
                edges=np.asarray(EDGES),
                matrices=unpack(z),
                residual=raw,
            )


if __name__ == "__main__":
    main()
