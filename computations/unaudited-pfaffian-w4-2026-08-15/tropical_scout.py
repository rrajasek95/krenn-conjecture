#!/usr/bin/env python3
"""UNAUDITED PROBE (W4 / Route T.1 scouting) -- Newton-polytope / initial-form
structure of the six-site mixed system.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Setting.  135 cell variables x[(u,v), i, j] (15 edges of K_6 times 9 colour
pairs).  For a colour word chi in {0,1,2}^6,

    Phi_chi = sum over the 15 perfect matchings M of K_6 of
              prod_{(u,v) in M} x[(u,v), chi_u, chi_v],

a sum of 15 DISTINCT squarefree cubic monomials, all with coefficient 1.  So
Newton(Phi_chi) is the convex hull of 15 distinct 0/1 vectors of weight 3, all
of which are vertices; the face structure that matters for T.1 is: for a weight
vector w, the w-minimal face of Newton(Phi_chi) is a vertex (equivalently
in_w(Phi_chi) is a MONOMIAL) exactly when the minimum of the 15 matching
weights is attained once.

Mixed words (chi non-constant, 726 of them) give the equations Phi_chi = 0;
the three pure words give Phi_c = 1.

What is measured.
  1. The exact GAUGE LINEALITY.  Rescaling the colour basis at each site,
     x[(u,v),i,j] -> t_u(i) + t_v(j), changes every matching weight of a given
     word by the SAME amount, so the whole 18-dimensional gauge space L is
     contained in the no-singleton locus.  Full-cone coverage is therefore
     impossible on the nose; the sharp question is whether the no-singleton
     locus is EXACTLY L (up to the pure-equation mechanism).
  2. Random samples (exact rationals, and integer weights with many ties).
  3. The natural symmetry cones: fixed spaces of elements of S_6 x S_3 acting
     on the cells, one representative per conjugacy class, plus some standard
     subgroups.  These are the candidate higher-dimensional no-singleton cones.
  4. A subgradient search for no-singleton points transverse to L.
  5. The pure-equation mechanism (Laurent saturation): if the pure word c has
     min_M W(M) > 0 then in_w(Phi_c - 1) = -1, a unit, so the initial ideal is
     everything; if min < 0 and attained once, in_w is a monomial.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
import json
import random

SITES = tuple(range(6))
EDGES = tuple(combinations(SITES, 2))
EDGE_INDEX = {e: n for n, e in enumerate(EDGES)}
NCELL = len(EDGES) * 9


def cell(edge, i, j):
    return EDGE_INDEX[edge] * 9 + 3 * i + j


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, vertices[index]),) + tail)
    return tuple(out)


MATCHINGS = perfect_matchings(SITES)
WORDS = tuple(product(range(3), repeat=6))
MIXED = tuple(chi for chi in WORDS if len(set(chi)) > 1)
PURE = tuple(chi for chi in WORDS if len(set(chi)) == 1)

# supports: for each (word, matching) the triple of cell indices
SUPPORT = {}
for chi in WORDS:
    rows = []
    for matching in MATCHINGS:
        rows.append(tuple(cell((u, v), chi[u], chi[v]) for u, v in matching))
    SUPPORT[chi] = tuple(rows)


def matching_weights(w, chi):
    return [w[a] + w[b] + w[c] for a, b, c in SUPPORT[chi]]


def has_singleton(w, words=MIXED):
    """Does some word in `words` have a unique w-minimal matching?"""
    for chi in words:
        values = matching_weights(w, chi)
        best = min(values)
        if values.count(best) == 1:
            return True, chi
    return False, None


def singleton_count(w, words=MIXED):
    total = 0
    for chi in words:
        values = matching_weights(w, chi)
        if values.count(min(values)) == 1:
            total += 1
    return total


def slack(w, words=MIXED):
    """sum over words of (second smallest - smallest); zero iff no singleton."""
    total = Fraction(0) if isinstance(w[0], Fraction) else 0.0
    for chi in words:
        values = sorted(matching_weights(w, chi))
        total += values[1] - values[0]
    return total


# ------------------------------------------------------------- lineality

def gauge_basis():
    """t_u(i) -> w[(u,v),i,j] = t_u(i) + t_v(j); 18 generators."""
    basis = []
    for u in SITES:
        for i in range(3):
            vector = [Fraction(0)] * NCELL
            for edge in EDGES:
                for a in range(3):
                    for b in range(3):
                        if edge[0] == u and a == i:
                            vector[cell(edge, a, b)] += 1
                        if edge[1] == u and b == i:
                            vector[cell(edge, a, b)] += 1
            basis.append(vector)
    return basis


def row_reduce(rows):
    basis, pivots = [], []
    for vector in rows:
        row = list(vector)
        for pivot, brow in zip(pivots, basis):
            if row[pivot]:
                factor = row[pivot] / brow[pivot]
                row = [a - factor * b for a, b in zip(row, brow)]
        pivot = next((n for n, value in enumerate(row) if value), None)
        if pivot is None:
            continue
        basis.append(row)
        pivots.append(pivot)
    return list(zip(pivots, basis))


def nullspace(equations, nvars):
    rows = [list(map(Fraction, eq)) for eq in equations]
    pivots, r = [], 0
    for column in range(nvars):
        pivot = None
        for index in range(r, len(rows)):
            if rows[index][column]:
                pivot = index
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        head = rows[r]
        for index in range(len(rows)):
            if index != r and rows[index][column]:
                factor = rows[index][column] / head[column]
                rows[index] = [a - factor * b for a, b in zip(rows[index], head)]
        pivots.append(column)
        r += 1
    free = [c for c in range(nvars) if c not in pivots]
    basis = []
    for f in free:
        vector = [Fraction(0)] * nvars
        vector[f] = Fraction(1)
        for index, column in enumerate(pivots):
            vector[column] = -rows[index][f] / rows[index][column]
        basis.append(vector)
    return basis


def all_tied_space():
    """{w : every word has all 15 matching weights equal}, exactly."""
    equations = []
    for chi in WORDS:
        rows = SUPPORT[chi]
        first = rows[0]
        for other in rows[1:]:
            equation = [0] * NCELL
            for index in first:
                equation[index] += 1
            for index in other:
                equation[index] -= 1
            equations.append(equation)
    return nullspace(equations, NCELL)


# ------------------------------------------------------- symmetry cones

def act(sigma, tau):
    """Permutation of the 135 cells induced by (sigma on sites, tau on colours)."""
    image = [0] * NCELL
    for edge in EDGES:
        u, v = edge
        for i in range(3):
            for j in range(3):
                su, sv = sigma[u], sigma[v]
                if su < sv:
                    target = cell((su, sv), tau[i], tau[j])
                else:
                    target = cell((sv, su), tau[j], tau[i])
                image[cell(edge, i, j)] = target
    return image


def fixed_space(perms):
    """Basis of the subspace of R^135 fixed by all given cell permutations."""
    equations = []
    for image in perms:
        for index in range(NCELL):
            equation = [0] * NCELL
            equation[image[index]] += 1
            equation[index] -= 1
            equations.append(equation)
    return nullspace(equations, NCELL)


def random_point(basis, rng, lo=-20, hi=20):
    coefficients = [Fraction(rng.randint(lo, hi)) for _ in basis]
    vector = [Fraction(0)] * NCELL
    for coefficient, row in zip(coefficients, basis):
        if coefficient:
            for index in range(NCELL):
                if row[index]:
                    vector[index] += coefficient * row[index]
    return vector


CYCLE_TYPES_6 = ((1, 1, 1, 1, 1, 1), (2, 1, 1, 1, 1), (2, 2, 1, 1), (2, 2, 2),
                 (3, 1, 1, 1), (3, 2, 1), (3, 3), (4, 1, 1), (4, 2), (5, 1), (6,))
CYCLE_TYPES_3 = ((1, 1, 1), (2, 1), (3,))


def permutation_of_type(cycle_type, n):
    perm = list(range(n))
    start = 0
    for length in cycle_type:
        block = list(range(start, start + length))
        for index, value in enumerate(block):
            perm[value] = block[(index + 1) % length]
        start += length
    return perm


# --------------------------------------------------------------- samplers

def random_generic(rng):
    return [Fraction(rng.randint(-10 ** 6, 10 ** 6), rng.randint(1, 997))
            for _ in range(NCELL)]


def random_integer(rng, span):
    return [Fraction(rng.randint(-span, span)) for _ in range(NCELL)]


def structured(rng, kind):
    w = [Fraction(0)] * NCELL
    if kind == "edge-only":
        values = {edge: Fraction(rng.randint(-9, 9)) for edge in EDGES}
        for edge in EDGES:
            for i in range(3):
                for j in range(3):
                    w[cell(edge, i, j)] = values[edge]
    elif kind == "colour-only":
        values = {(i, j): Fraction(rng.randint(-9, 9))
                  for i in range(3) for j in range(3)}
        for edge in EDGES:
            for i in range(3):
                for j in range(3):
                    w[cell(edge, i, j)] = values[(i, j)]
    elif kind == "colour-only-symmetric":
        values = {}
        for i in range(3):
            for j in range(3):
                key = (min(i, j), max(i, j))
                values.setdefault(key, Fraction(rng.randint(-9, 9)))
        for edge in EDGES:
            for i in range(3):
                for j in range(3):
                    w[cell(edge, i, j)] = values[(min(i, j), max(i, j))]
    elif kind == "diagonal-indicator":
        a, b = Fraction(0), Fraction(1)
        for edge in EDGES:
            for i in range(3):
                for j in range(3):
                    w[cell(edge, i, j)] = a if i == j else b
    elif kind == "edge+colour":
        e = {edge: Fraction(rng.randint(-9, 9)) for edge in EDGES}
        c = {(i, j): Fraction(rng.randint(-9, 9))
             for i in range(3) for j in range(3)}
        for edge in EDGES:
            for i in range(3):
                for j in range(3):
                    w[cell(edge, i, j)] = e[edge] + c[(i, j)]
    else:
        raise ValueError(kind)
    return w


# ------------------------------------------------------- descent search

def project_out(vector, basis_reduced):
    row = list(vector)
    for pivot, brow in basis_reduced:
        if row[pivot]:
            factor = row[pivot] / brow[pivot]
            row = [a - factor * b for a, b in zip(row, brow)]
    return row


def subgradient_search(rng, gauge_reduced, restarts=6, steps=400):
    """Minimise the piecewise-linear slack transverse to the gauge lineality."""
    best = None
    for _ in range(restarts):
        w = [rng.uniform(-1, 1) for _ in range(NCELL)]
        w = [float(x) for x in project_out([Fraction(x).limit_denominator(10 ** 6)
                                            for x in w], gauge_reduced)]
        norm = sum(x * x for x in w) ** 0.5
        w = [x / norm for x in w]
        step = 0.25
        for iteration in range(steps):
            grad = [0.0] * NCELL
            value = 0.0
            for chi in MIXED:
                values = matching_weights(w, chi)
                order = sorted(range(15), key=lambda n: values[n])
                first, second = order[0], order[1]
                value += values[second] - values[first]
                for index in SUPPORT[chi][second]:
                    grad[index] += 1.0
                for index in SUPPORT[chi][first]:
                    grad[index] -= 1.0
            gnorm = sum(g * g for g in grad) ** 0.5
            if gnorm == 0:
                break
            w = [x - step * g / gnorm for x, g in zip(w, grad)]
            w = [float(x) for x in project_out(
                [Fraction(x).limit_denominator(10 ** 9) for x in w],
                gauge_reduced)]
            norm = sum(x * x for x in w) ** 0.5
            if norm == 0:
                break
            w = [x / norm for x in w]
            step *= 0.995
        final = slack(w)
        if best is None or final < best[0]:
            best = (final, singleton_count(w))
    return best


# ------------------------------------------------------------------- main

def main():
    print("UNAUDITED PROBE (W4, Route T.1 scouting) -- K_6 initial-form structure")
    print("pinned HEAD 26ba69f7e643694c6a58464af6e9e1de9ec92f01")
    print("cells %d, mixed words %d, pure words %d, matchings %d"
          % (NCELL, len(MIXED), len(PURE), len(MATCHINGS)))
    print()

    rng = random.Random(2026)
    report = {}

    gauge = gauge_basis()
    gauge_reduced = row_reduce(gauge)
    print("1. gauge lineality dim :", len(gauge_reduced))
    tied = all_tied_space()
    print("   {w : every word has all 15 matchings tied} dim :", len(tied))
    zero_point = random_point(gauge, rng)
    ok, _ = has_singleton(zero_point)
    print("   a random gauge point has a mixed singleton :", ok,
          "(slack %s)" % slack(zero_point))
    report["gauge_dim"] = len(gauge_reduced)
    report["all_tied_dim"] = len(tied)

    print()
    print("2. random samples (exact rationals / integers)")
    families = [("uniform rationals", lambda r: random_generic(r), 200),
                ("integers |w|<=1", lambda r: random_integer(r, 1), 200),
                ("integers |w|<=2", lambda r: random_integer(r, 2), 200),
                ("integers |w|<=5", lambda r: random_integer(r, 5), 200),
                ("0/1 weights", lambda r: random_integer(r, 0) if False
                 else [Fraction(r.randint(0, 1)) for _ in range(NCELL)], 200)]
    report["random"] = {}
    for name, sampler, trials in families:
        hits = 0
        counts = []
        for _ in range(trials):
            w = sampler(rng)
            ok, _ = has_singleton(w)
            hits += ok
            counts.append(singleton_count(w))
        report["random"][name] = {"trials": trials, "with_singleton": hits,
                                  "mean_singleton_words":
                                  sum(counts) / len(counts),
                                  "min_singleton_words": min(counts)}
        print("   %-20s %3d/%3d have a singleton; mixed words with a singleton:"
              " mean %.1f, min %d"
              % (name, hits, trials, sum(counts) / len(counts), min(counts)))

    print()
    print("3. structured / symmetric weight families")
    report["structured"] = {}
    for kind in ("edge-only", "colour-only", "colour-only-symmetric",
                 "diagonal-indicator", "edge+colour"):
        hits, trials = 0, 60 if kind != "diagonal-indicator" else 1
        counts = []
        for _ in range(trials):
            w = structured(rng, kind)
            ok, _ = has_singleton(w)
            hits += ok
            counts.append(singleton_count(w))
        report["structured"][kind] = {"trials": trials, "with_singleton": hits,
                                      "mean_singleton_words":
                                      sum(counts) / len(counts)}
        print("   %-24s %2d/%2d have a singleton (mean %.1f mixed words)"
              % (kind, hits, trials, sum(counts) / len(counts)))

    print()
    print("4. natural symmetry cones: fixed spaces of (sigma,tau) in S_6 x S_3")
    report["symmetry"] = []
    for type6 in CYCLE_TYPES_6:
        for type3 in CYCLE_TYPES_3:
            sigma = permutation_of_type(type6, 6)
            tau = permutation_of_type(type3, 3)
            if sigma == list(range(6)) and tau == list(range(3)):
                continue
            basis = fixed_space([act(sigma, tau)])
            hits, trials = 0, 25
            worst = None
            for _ in range(trials):
                w = random_point(basis, rng)
                ok, _ = has_singleton(w)
                hits += ok
                count = singleton_count(w)
                worst = count if worst is None else min(worst, count)
            entry = {"sigma": type6, "tau": type3, "dim": len(basis),
                     "with_singleton": hits, "trials": trials,
                     "min_singleton_words": worst}
            report["symmetry"].append(entry)
            flag = "" if hits == trials else "   <<< NO-SINGLETON CONE"
            print("   sigma%-18s tau%-10s dim %3d  singleton %2d/%2d%s"
                  % (str(type6), str(type3), len(basis), hits, trials, flag))

    print()
    print("5. subgradient search for no-singleton points transverse to gauge")
    best = subgradient_search(rng, gauge_reduced)
    print("   best slack found on the unit sphere mod gauge: %.6f"
          " (mixed words with a singleton there: %d of %d)"
          % (best[0], best[1], len(MIXED)))
    report["search"] = {"best_slack": best[0], "singleton_words": best[1]}

    print()
    print("6. the pure-equation (Laurent saturation) mechanism")
    counts = {"unit": 0, "monomial": 0, "neither": 0}
    for _ in range(200):
        w = random_generic(rng)
        fired = "neither"
        for chi in PURE:
            values = matching_weights(w, chi)
            best_value = min(values)
            if best_value > 0:
                fired = "unit"
                break
            if best_value < 0 and values.count(best_value) == 1:
                fired = "monomial"
        counts[fired] += 1
    print("   of 200 random w: in_w(Phi_c - 1) is a unit for %d, a monomial for"
          " %d, neither for %d" % (counts["unit"], counts["monomial"],
                                   counts["neither"]))
    report["pure"] = counts
    # on the gauge lineality itself
    gauge_counts = {"unit": 0, "monomial": 0, "neither": 0}
    for _ in range(200):
        w = random_point(gauge, rng)
        fired = "neither"
        for chi in PURE:
            values = matching_weights(w, chi)
            best_value = min(values)
            if best_value > 0:
                fired = "unit"
                break
            if best_value < 0 and values.count(best_value) == 1:
                fired = "monomial"
        gauge_counts[fired] += 1
    print("   on the 18-dim gauge lineality: unit %d, monomial %d, neither %d"
          % (gauge_counts["unit"], gauge_counts["monomial"],
             gauge_counts["neither"]))
    report["pure_on_gauge"] = gauge_counts

    with open("results_tropical.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print()
    print("wrote results_tropical.json")


if __name__ == "__main__":
    main()
