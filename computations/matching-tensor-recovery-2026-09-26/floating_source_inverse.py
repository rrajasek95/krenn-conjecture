"""Numerical covariance/scale proposal from a tensor and proposed mean lines.

This is a proposal, not a certificate. Source-parameter comparison belongs
in a separate driver. Exact finite-error acceptance is developed separately.
"""

import itertools
from functools import lru_cache

import numpy as np
from blind_mean_search import contract
from scipy.linalg import lstsq, solve, svd


def propose_mean_lines(tensor):
    n = tensor.ndim
    tail = n - 1
    size = 3**tail
    steps = np.asarray(list(itertools.product([1, 2], repeat=tail)))
    signs = (-1.0) ** np.sum(steps == 2, axis=1)
    powers = 3 ** np.arange(tail - 1, -1, -1)
    matrices = []
    for colour in range(3):
        matrix = np.zeros((size, size))
        flat = tensor[colour].reshape(-1)
        for index, word in enumerate(itertools.product(range(3), repeat=tail)):
            word = np.asarray(word)
            matrix[index, ((word + steps) % 3) @ powers] = (
                signs * flat[((word - steps) % 3) @ powers]
            )
        matrices.append(matrix)
    a = solve(matrices[0], matrices[1], assume_a="sym")
    b = solve(matrices[0], matrices[2], assume_a="sym")
    c = a @ b - b @ a
    _, _, vh = svd(np.concatenate([c, c @ a]), full_matrices=False)
    v = vh[-1]
    lines = [np.array([1, v @ a @ v, v @ b @ v])]
    for i in range(tail):
        matrix = np.moveaxis(v.reshape((3,) * tail), i, 0).reshape(3, -1)
        u, _, _ = svd(matrix, full_matrices=False)
        lines.append(u[:, 0])
    return lines


class Exterior:
    def __init__(self, tensor, n):
        self.n = n
        self.tensor = np.asarray(tensor).reshape(-1)
        self.powers = 3 ** np.arange(n - 1, -1, -1)
        self.bits = np.array(list(itertools.product([0, 1], repeat=n)))
        self.sign = (-1.0) ** (n - self.bits.sum(axis=1))
        self.cache = {}

    def column(self, index):
        if index not in self.cache:
            b = index // self.powers % 3
            a = (b + 1 + self.bits) % 3
            c = 3 - a - b
            self.cache[index] = (
                a @ self.powers,
                self.sign * self.tensor[c @ self.powers],
            )
        return self.cache[index]

    def apply(self, polys):
        out = np.zeros((3**self.n, len(polys)))
        for j, poly in enumerate(polys):
            for index, value in poly.items():
                rows, vals = self.column(index)
                out[rows, j] += value * vals
        return out


def setup(n):
    keys = [
        (i, j, a, b)
        for i, j in itertools.combinations(range(n), 2)
        for a, b in itertools.product(range(3), repeat=2)
    ]
    index = {key: q for q, key in enumerate(keys)}
    powers = 3 ** np.arange(n - 1, -1, -1)
    codes = [int(a * powers[i] + b * powers[j]) for i, j, a, b in keys]
    masks = [(1 << i) | (1 << j) for i, j, a, b in keys]
    flows = []
    for i in range(n):
        others = [j for j in range(n) if j != i]
        for a in [1, 2]:
            for j in others[1:]:
                d = {}
                for k, val in [(j, 1), (others[0], -1)]:
                    key = (i, k, a, 0) if i < k else (k, i, 0, a)
                    d[index[key]] = val
                flows.append(d)
    pure = [index[i, j, 0, 0] for i, j in itertools.combinations(range(n), 2)]
    zeros = [{j: 1, pure[0]: -1} for j in pure[1:]]

    def product(x, y):
        out = {}
        for q, v in x.items():
            for r, w in y.items():
                if not masks[q] & masks[r]:
                    code = codes[q] + codes[r]
                    out[code] = out.get(code, 0) + v * w
        return out

    return keys, codes, flows, zeros, product


def add(vec, basis, coeff):
    result = dict(vec)
    for d, c in zip(basis, coeff):
        for k, v in d.items():
            result[k] = result.get(k, 0) + c * v
    return result


def layers(n, edges):
    @lru_cache(None)
    def go(sites):
        if not sites:
            return np.array([1.0])
        i, *rest = sites
        result = np.zeros((len(sites) // 2 + 1,) + (3,) * len(sites))
        old = go(tuple(rest))
        result[: len(old), 0] = old
        for pos, j in enumerate(rest, 1):
            old = go(tuple(k for k in rest if k != j))
            pair = edges[i, j].reshape((1, 3, 3) + (1,) * (len(rest) - 1))
            term = np.moveaxis(pair * old[:, None, None], 2, pos + 1)
            result[1 : len(old) + 1] += term
        return result

    return go(tuple(range(n))).reshape((n // 2 + 1, -1)).T[:, ::-1]


def recover(tensor, mean_lines):
    n = tensor.ndim
    bases = []
    for row in mean_lines:
        row = np.asarray(row, dtype=float)
        pivot = int(np.argmax(abs(row)))
        x = np.asarray(row) / row[pivot]
        basis = np.column_stack([x] + [np.eye(3)[:, a] for a in range(3) if a != pivot])
        bases.append(basis)
    t = contract(tensor, [np.linalg.inv(b) for b in bases]).reshape(-1)
    action = Exterior(t, n)
    keys, codes, flows, zeros, product = setup(n)
    f2 = sorted(set(codes))
    exterior = action.apply([{code: 1} for code in f2])
    _, s, vh = svd(exterior[:, 1:], full_matrices=False)
    outside = [
        j
        for j, code in enumerate(f2)
        if np.count_nonzero(code // (3 ** np.arange(n - 1, -1, -1)) % 3) == 2
    ]
    vector = np.r_[0, vh[-1]]
    pivot = max(outside, key=lambda j: abs(vector[j]))
    vector /= vector[pivot]
    cols = [j for j in range(len(f2)) if j not in [0, pivot]]
    nuisance = exterior[:, cols]
    rest = lstsq(nuisance, -exterior[:, pivot])[0]
    vector = np.zeros(len(f2))
    vector[pivot] = 1
    vector[cols] = rest
    section = {}
    for q, code in enumerate(codes):
        section.setdefault(code, q)
    q0 = {section[code]: val for code, val in zip(f2, vector) if val}
    j1 = np.column_stack([action.apply([product(q0, d) for d in flows]), nuisance])
    rhs = action.apply([{k: v / 2 for k, v in product(q0, q0).items()}])[:, 0]
    coeff1, _, _, s1 = lstsq(j1, -rhs)
    q1 = add(q0, flows, coeff1[: len(flows)])
    j2 = action.apply([product(q1, d) for d in zeros])
    rhs2 = action.apply([{k: v / 2 for k, v in product(q1, q1).items()}])[:, 0]
    coeff2, _, _, s2 = lstsq(j2, -rhs2)
    q = add(q1, zeros, coeff2)
    edges = {ij: np.zeros((3, 3)) for ij in itertools.combinations(range(n), 2)}
    for k, (i, j, a, b) in enumerate(keys):
        edges[i, j][a, b] = q.get(k, 0)
    frame = layers(n, edges)
    co, _, _, sf = lstsq(frame, t)
    z, c3, c5, c7 = co[:4]
    ss = c3 / (3 * z)
    beta2 = 1.5 * (15 * z * ss**2 - c5) / z**5
    beta3 = 9 / 16 * (c7 - 105 * z * ss**3 + 14 * beta2 * z**5 * ss) / z**7
    beta = beta3 / beta2
    k = ss - beta * z * z / 3
    m = n // 2
    tau = z**n * beta**m
    mu = [b[:, 0] * (tau if i == n - 1 else 1) for i, b in enumerate(bases)]
    out = {}
    for (i, j), edge in edges.items():
        shifted = edge.copy()
        shifted[0, 0] += k
        scale = beta ** (m - 1) * z ** (n - 2) if j == n - 1 else 1 / (beta * z * z)
        out[i, j] = bases[i] @ (scale * shifted) @ bases[j].T
    return (
        mu,
        out,
        {
            "sigma_f2": s[-2],
            "sigma_j1": s1[-1],
            "sigma_j2": s2[-1],
            "sigma_frame": sf[-1],
            "z": z,
            "beta": beta,
            "tau": tau,
            "res1": np.linalg.norm(j1 @ coeff1 + rhs),
            "res2": np.linalg.norm(j2 @ coeff2 + rhs2),
            "resframe": np.linalg.norm(frame @ co - t),
            "F2_pivot": int(pivot),
        },
    )
