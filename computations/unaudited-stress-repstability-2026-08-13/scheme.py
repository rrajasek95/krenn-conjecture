#!/usr/bin/env python3
"""Exact isotypic decomposition in the perfect-matching association scheme.

The permutation module C[PM(K_2h)] of S_{2h} is multiplicity free with
summands S^{2lam}, lam |- h, so the scheme's common eigenspaces ARE the
isotypic summands.  This module

  * builds the scheme relations by union-cycle type,
  * computes the exact P-matrix (joint eigenvalues) from intersection
    numbers,
  * labels every eigenspace by its partition lam, using the exact level
    invariant  level(j) = min{k : E_j(1_{k-partial matching}) != 0} = h-lam_1
    together with the multiplicity f^{2lam},
  * decomposes an arbitrary exact vector into its isotypic components by
    sequential Lagrange projectors in a separating set of cheap relation
    operators (single-cycle relations lam = (k,1,...,1)).

Everything is exact.  Floats appear only to *propose* eigenvalue candidates;
every accepted value is verified over Q.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations

from lib_stress import (
    MatchingSpace, coset_type, hook_dimension, minimal_polynomial_on_vector,
    partitions, perfect_matchings, poly_eval,
)


def single_cycle_neighbors(matching, k, index):
    """Neighbours N with coset type (k,1,...,1): re-pair k edges into one
    2k-cycle."""
    answer = []
    for chosen in combinations(range(len(matching)), k):
        block = [matching[i] for i in chosen]
        rest = tuple(v for i, v in enumerate(matching) if i not in chosen)
        vertices = tuple(sorted(v for e in block for v in e))
        for candidate in perfect_matchings(vertices):
            if coset_type(tuple(sorted(block)), candidate) == (k,):
                answer.append(index[tuple(sorted(rest + candidate))])
    return tuple(answer)


class Scheme:
    def __init__(self, h: int, extra_relations=(3,), full=True):
        self.h = h
        self.full = full
        self.space = MatchingSpace(h)
        self.points = self.space.points
        self.index = self.space.index
        self.classes = sorted(partitions(h), reverse=True)
        self.class_index = {c: i for i, c in enumerate(self.classes)}
        base = self.points[0]
        self.valency = {c: 0 for c in self.classes}
        for m in self.points:
            self.valency[coset_type(base, m)] += 1
        self._intersection()
        self._eigenvalues()
        self.operators = {}
        self._register_operator(2, self.space.adjacency)
        for k in (extra_relations if full else ()):
            if k <= h:
                adjacency = tuple(
                    single_cycle_neighbors(m, k, self.index) for m in self.points
                )
                assert all(len(row) == len(adjacency[0]) for row in adjacency)
                self._register_operator(k, adjacency)
        self._label()

    # ------------------------------------------------------------ internals
    def _register_operator(self, k, adjacency):
        cls = tuple(sorted([k] + [1] * (self.h - k), reverse=True))
        assert len(adjacency[0]) == self.valency[cls], (
            "relation valency mismatch", k, len(adjacency[0]), self.valency[cls])
        self.operators[k] = (cls, adjacency)

    def apply(self, k, vector):
        _cls, adjacency = self.operators[k]
        return tuple(sum(vector[j] for j in row) for row in adjacency)

    def _intersection(self):
        base = self.points[0]
        representative = {}
        for m in self.points:
            t = coset_type(base, m)
            representative.setdefault(t, m)
        n = len(self.classes)
        B = [[[0] * n for _ in range(n)] for _ in range(n)]
        for k_class in self.classes:
            y = representative[k_class]
            k_idx = self.class_index[k_class]
            for z in self.points:
                i_idx = self.class_index[coset_type(base, z)]
                j_idx = self.class_index[coset_type(z, y)]
                B[i_idx][k_idx][j_idx] += 1
        self.B = B

    def _eigenvalues(self):
        import numpy as np
        n = len(self.classes)
        weights = [1, 3, 7, 13, 23, 37, 53, 71, 97, 113, 131, 157, 173, 197,
                   211, 233, 257, 281, 307, 331, 353]
        C = [[sum(weights[i] * self.B[i][k][j] for i in range(n))
              for j in range(n)] for k in range(n)]
        proposals = sorted({round(float(v.real))
                            for v in np.linalg.eigvals(np.array(C, dtype=float))})
        rows = []
        for cand in proposals:
            M = [[Q(C[k][j]) - (Q(cand) if k == j else Q(0)) for j in range(n)]
                 for k in range(n)]
            vec = _nullspace_vector(M, n)
            if vec is None:
                continue
            pivot = next(i for i, v in enumerate(vec) if v)
            eigen = []
            ok = True
            for i in range(n):
                image = [sum(Q(self.B[i][k][j]) * vec[j] for j in range(n))
                         for k in range(n)]
                theta = image[pivot] / vec[pivot]
                if image != [theta * v for v in vec]:
                    ok = False
                    break
                eigen.append(theta)
            if ok:
                rows.append(tuple(eigen))
        rows = sorted(set(rows), reverse=True)
        assert len(rows) == n, ("eigenvalue rows != classes", len(rows), n)
        self.P = rows
        mult = []
        for row in rows:
            total = sum(row[i] ** 2 / Q(self.valency[self.classes[i]])
                        for i in range(n))
            m = Q(len(self.points)) / total
            assert m.denominator == 1
            mult.append(int(m))
        assert sum(mult) == len(self.points)
        self.multiplicity = mult

    def eigenvalue(self, eigenspace: int, k: int) -> Q:
        cls, _ = self.operators[k]
        return self.P[eigenspace][self.class_index[cls]]

    def separating_keys(self):
        keys = [tuple(self.eigenvalue(j, k) for k in sorted(self.operators))
                for j in range(len(self.P))]
        assert len(set(keys)) == len(keys), (
            "registered relations do not separate the eigenspaces", keys)
        return keys

    def _label_light(self):
        """Label only those eigenspaces whose multiplicity f^{2lam} is unique.

        No V_k filtration, no extra relation operators: used for the largest
        orders, where only the low-level shapes are needed and their
        dimensions are unambiguous.
        """
        dims = {}
        for lam in partitions(self.h):
            dims.setdefault(hook_dimension(tuple(2 * p for p in lam)), []).append(lam)
        assignment = {}
        for j in range(len(self.P)):
            fits = dims.get(self.multiplicity[j], [])
            if len(fits) == 1:
                assignment[j] = fits[0]
        self.shape = assignment
        self.by_shape = {lam: j for j, lam in assignment.items()}
        self.level = {j: self.h - lam[0] for j, lam in assignment.items()}

    def _label(self):
        if not self.full:
            self._label_light()
            return
        keys = self.separating_keys()
        self.keys = keys
        # exact level = h - lam_1 via the V_k filtration
        levels = {}
        for k in range(0, self.h + 1):
            partial = [(2 * i, 2 * i + 1) for i in range(k)]
            vector = self.space.partial_matching_indicator(partial)
            content = self.decompose(vector)
            for j in content:
                levels.setdefault(j, k)
            if len(levels) == len(self.P):
                break
        assert len(levels) == len(self.P), ("levels incomplete", levels)
        self.level = levels
        # match (level, multiplicity) to (h-lam_1, f^{2lam})
        available = list(partitions(self.h))
        assignment = {}
        for j in range(len(self.P)):
            fits = [lam for lam in available
                    if self.h - lam[0] == levels[j]
                    and hook_dimension(tuple(2 * p for p in lam))
                    == self.multiplicity[j]]
            assert len(fits) == 1, ("ambiguous shape label", j, fits,
                                    levels[j], self.multiplicity[j])
            assignment[j] = fits[0]
            available.remove(fits[0])
        assert not available
        self.shape = assignment
        self.by_shape = {lam: j for j, lam in assignment.items()}

    # ------------------------------------------------------------ decompose
    def decompose(self, vector, tolerate_zero=True):
        """Exact isotypic decomposition.  Returns {eigenspace index: component}."""
        vector = tuple(Q(v) for v in vector)
        if not any(vector):
            return {}
        pieces = [(vector, list(range(len(self.P))))]
        for k in sorted(self.operators):
            nxt = []
            for piece, candidates in pieces:
                if len(candidates) == 1:
                    nxt.append((piece, candidates))
                    continue
                op = lambda v, k=k: self.apply(k, v)
                coeffs = minimal_polynomial_on_vector(op, piece)
                values = sorted({self.eigenvalue(j, k) for j in candidates})
                roots = [t for t in values if poly_eval(coeffs, t) == 0]
                assert len(roots) == len(coeffs) - 1, (
                    "minimal polynomial has roots outside the scheme spectrum",
                    k, coeffs, values)
                for theta in roots:
                    component = piece
                    scale = Q(1)
                    for other in roots:
                        if other == theta:
                            continue
                        image = op(component)
                        component = tuple(a - other * b for a, b
                                          in zip(image, component, strict=True))
                        scale *= (theta - other)
                    component = tuple(v / scale for v in component)
                    if any(component):
                        nxt.append((component,
                                    [j for j in candidates
                                     if self.eigenvalue(j, k) == theta]))
            pieces = nxt
        result = {}
        for piece, candidates in pieces:
            assert len(candidates) == 1, ("unseparated piece", candidates)
            j = candidates[0]
            assert j not in result
            result[j] = piece
        total = [Q(0)] * len(vector)
        for piece in result.values():
            total = [a + b for a, b in zip(total, piece, strict=True)]
        assert tuple(total) == vector, "isotypic components do not sum to the vector"
        return result

    def shape_content(self, vector):
        """Sorted list of partitions 2lam whose isotypic component is nonzero."""
        content = self.decompose(vector)
        return sorted(tuple(2 * p for p in self.shape[j]) for j in content)


def _nullspace_vector(M, n):
    rows = [list(r) for r in M]
    pivot_row = {}
    order = []
    used = set()
    for c in range(n):
        r = next((i for i in range(len(rows)) if i not in used and rows[i][c]), None)
        if r is None:
            continue
        used.add(r)
        pivot_row[c] = r
        order.append(c)
        pv = rows[r][c]
        rows[r] = [v / pv for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r], strict=True)]
    free = [c for c in range(n) if c not in pivot_row]
    if not free:
        return None
    f0 = free[0]
    vec = [Q(0)] * n
    vec[f0] = Q(1)
    for c in order:
        vec[c] = -rows[pivot_row[c]][f0]
    return vec
