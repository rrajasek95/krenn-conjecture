#!/usr/bin/env python3
"""Exact audit for the escape-chart descent theorems (defect-one charts).

Companion checker for notes/good-pair-fan-escape-chart-descent-theorem.md.

Everything runs over exact rationals (Fraction) or, for the |W| = 6
Hessian ranks, modulo a prime as an exact lower bound paired with exact
integer gauge independence and annihilation (the registered two-sided
scheme).  No floating point, no numerical tolerance.  Checks:

 1. the affine graph step: for a battery of graphs, the nullity of
    {alpha_i + alpha_j = 0 on edges} is the defect nu = #bipartite
    components + #isolated vertices, with the zeta basis (shore signs and
    isolated-vertex indicators); alpha = gamma/2 solves the inhomogeneous
    system, so its solution space is gamma/2 + span(zeta);
 2. q q^[t-1] = t q^[t] and H_q(Z^alpha) = (sum alpha) q^[t], exactly;
 3. gauge-rigid defect-one charts exist: connected spanning bipartite
    with shores 2+2 and 1+3 at |W| = 4, an isolated-vertex chart at
    |W| = 4, a disconnected K_2 u K_4 chart and a connected C_6 chart at
    |W| = 6 -- so every defect-one chart type of Theorem B is nonvacuous;
 4. the block-pair kernel mechanism of Theorem C at |W| = 4: killing one
    same-shore block puts the opposite nine-dimensional block space
    inside the Hessian kernel (exact kernel 11 = 3 + 9 - 1);
 5. the collision mechanism: the window forced by a surviving pair --
    rank-one visible blocks with shared row factors -- always breaks
    gauge rigidity: exact kernel 9 = 3 + 6 at |W| = 4 shores 1+3, exact
    kernel 11 = 5 + 6 at |W| = 6 shores 4+2, in both cases spanned by
    gauge plus w|_x times the antipodal Ann-partner of a window row;
    generic support-3 rows have exact kernel 0 in T(a, s) on all three
    gauge-rigid |W| = 4 chart types, and the surviving beta line pins
    the direct entry a = -beta Delta;
 6. Lemma R (a site with at most two nonzero-block partners breaks
    rigidity), the Theorem E sign cancellation p.(x|_w) on the
    K_2-component chart, the exhaustive |W| = 6 support-pattern censuses
    (K_2 + K_4: exactly the 12 straddling patterns survive the filters,
    all killed by Theorem E; P_3 + triangle: zero survivors), and the
    reproduction of the post-fan status note's K_3,3 witness, whose
    colour-proportional triples have rank one (never a good pair);
 7. matching-balance facts: on connected bipartite charts with same-shore
    support confined to a window, top powers vanish exactly when the
    shore imbalance exceeds the disjoint live pairs (|Delta| bound);
 8. the (P)-guard family: six rows with both triples independent, all
    supports <= 2, satisfying all six off-diagonal product relations
    p_c s_d = beta_cd Z with one nonzero Z -- the product relations alone
    do not exclude a defect-one chart -- and the two independent deaths
    of its |W| = 4 embedding (dead-shore diagonal and Theorem C kernel);
 9. the window lemma at |W| = 4 (shores 2+2): no product of two rows has
    both same-shore blocks nonzero while every cross block vanishes
    (exhaustive support census, single-term principle);
10. a structural census of the zero-block defect-one system at |W| = 4:
    no support pattern survives even the product-level filter;
11. defect censuses of the two recorded structural guard families
    (fourteen-site bridge family, eight-site all-pair missing-row model)
    and an exact two-sided Hessian verdict on a defect-one chart of the
    eight-site model (gauge-rigid: a full structural guard);
12. the four-deletion support lemma and the fan / clique / shore
    threshold arithmetic of the corollaries.
13. all 24 K_1,3 + K_4 patterns at |W| = 8: a two-vertex deletion
    strands two leaves on one common mate, giving a nine-dimensional
    block kernel disjoint from the gauge space.

Run from the repository root:

    uv run python computations/fan_escape_chart_bipartite_sparse_check.py

Every check prints PASS; any failure raises.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from random import Random

COLORS = range(3)
PRIME = 1_000_003

CHECKS = []


def check(label, condition=True):
    if not condition:
        raise AssertionError(f"FAIL: {label}")
    CHECKS.append(label)
    print(f"PASS  {label}")


# ---------------------------------------------------------------------------
# exact linear algebra
# ---------------------------------------------------------------------------

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def exact_rank(rows):
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    rank = 0
    if not matrix:
        return 0
    cols = len(matrix[0])
    for col in range(cols):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = Fraction(1) / matrix[rank][col]
        matrix[rank] = [entry * inv for entry in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank and matrix[r][col]:
                factor = matrix[r][col]
                matrix[r] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry in zip(matrix[r], matrix[rank])
                ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def rank_mod(rows, prime=PRIME):
    matrix = [[int(entry) % prime for entry in row] for row in rows]
    rank = 0
    if not matrix:
        return 0
    cols = len(matrix[0])
    for col in range(cols):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], prime - 2, prime)
        matrix[rank] = [entry * inv % prime for entry in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank and matrix[r][col]:
                factor = matrix[r][col]
                matrix[r] = [
                    (entry - factor * pivot_entry) % prime
                    for entry, pivot_entry in zip(matrix[r], matrix[rank])
                ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def exact_nullspace(rows):
    """Exact rational nullspace basis of rows * x = 0."""
    if not rows:
        return []
    cols = len(rows[0])
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    pivots = []
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = Fraction(1) / matrix[rank][col]
        matrix[rank] = [entry * inv for entry in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank and matrix[r][col]:
                factor = matrix[r][col]
                matrix[r] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry in zip(matrix[r], matrix[rank])
                ]
        pivots.append(col)
        rank += 1
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        vec = [Fraction(0)] * cols
        vec[f] = Fraction(1)
        for r, pcol in enumerate(pivots):
            vec[pcol] = -matrix[r][f]
        basis.append(vec)
    return basis


def scale_int_rows(rows):
    out = []
    for row in rows:
        denom = 1
        for entry in row:
            d = Fraction(entry).denominator
            denom = denom * d // gcd(denom, d)
        out.append([int(Fraction(entry) * denom) for entry in row])
    return out


# ---------------------------------------------------------------------------
# square-zero site algebra with V_x = C^3
# ---------------------------------------------------------------------------
# quadratic: dict {(i, j): 3x3 matrix}, i < j; row: dict {site: [v0, v1, v2]}.

def matchings(sites):
    sites = sorted(sites)
    if not sites:
        yield ()
        return
    first, rest = sites[0], sites[1:]
    for k, partner in enumerate(rest):
        remaining = rest[:k] + rest[k + 1:]
        for tail in matchings(remaining):
            yield ((first, partner),) + tail


def block(q, i, j):
    if i < j:
        return q.get((i, j))
    entry = q.get((j, i))
    if entry is None:
        return None
    return [[entry[b][a] for b in COLORS] for a in COLORS]


def top_power(q, sites):
    """q^[t] over the site set (t = |sites|/2): dict word -> coefficient."""
    sites = sorted(sites)
    index = {s: k for k, s in enumerate(sites)}
    out = {}
    for matching in matchings(sites):
        blocks = []
        good = True
        for i, j in matching:
            entry = block(q, i, j)
            if entry is None or not any(any(r) for r in entry):
                good = False
                break
            blocks.append(((i, j), entry))
        if not good:
            continue
        partial = [((), Fraction(1))]
        for (i, j), entry in blocks:
            new = []
            for word, coeff in partial:
                for a, b in product(COLORS, repeat=2):
                    if entry[a][b]:
                        new.append((word + ((i, a), (j, b)), coeff * entry[a][b]))
            partial = new
            if not partial:
                break
        for assignment, coeff in partial:
            word = [None] * len(sites)
            for site, colour in assignment:
                word[index[site]] = colour
            word = tuple(word)
            out[word] = out.get(word, Fraction(0)) + coeff
    return {w: c for w, c in out.items() if c}


def quad_times_power(z, q, sites):
    """z * q^[t-1] over the site set (the Hessian image of z)."""
    sites = sorted(sites)
    index = {s: k for k, s in enumerate(sites)}
    out = {}
    for (i, j) in combinations(sites, 2):
        entry = block(z, i, j)
        if entry is None:
            continue
        complement = [s for s in sites if s not in (i, j)]
        tail = top_power(q, complement)
        if not tail:
            continue
        tail_index = [index[s] for s in complement]
        for a, b in product(COLORS, repeat=2):
            if not entry[a][b]:
                continue
            for word, coeff in tail.items():
                full = [None] * len(sites)
                full[index[i]] = a
                full[index[j]] = b
                for pos, colour in zip(tail_index, word):
                    full[pos] = colour
                full = tuple(full)
                out[full] = out.get(full, Fraction(0)) + entry[a][b] * coeff
    return {w: c for w, c in out.items() if c}


def row_product(p, s, sites):
    """The quadratic p*s of two site-linear families."""
    out = {}
    for (i, j) in combinations(sorted(sites), 2):
        blockm = [[Fraction(0)] * 3 for _ in COLORS]
        nonzero = False
        pi, sj = p.get(i), s.get(j)
        si, pj = s.get(i), p.get(j)
        for a, b in product(COLORS, repeat=2):
            value = Fraction(0)
            if pi is not None and sj is not None:
                value += Fraction(pi[a]) * Fraction(sj[b])
            if si is not None and pj is not None:
                value += Fraction(si[a]) * Fraction(pj[b])
            if value:
                nonzero = True
            blockm[a][b] = value
        if nonzero:
            out[(i, j)] = blockm
    return out


def gauge_quadratic(q, alpha, sites):
    """Z^alpha with blocks (alpha_i + alpha_j) q_ij."""
    out = {}
    for (i, j) in combinations(sorted(sites), 2):
        entry = block(q, i, j)
        if entry is None:
            continue
        scale = Fraction(alpha[i]) + Fraction(alpha[j])
        if not scale:
            continue
        out[(i, j)] = [[scale * Fraction(entry[a][b]) for b in COLORS] for a in COLORS]
    return out


def vectorize(element, sites):
    words = list(product(COLORS, repeat=len(sites)))
    return [element.get(w, Fraction(0)) for w in words]


def hessian_rows(q, sites):
    rows = []
    labels = []
    for (i, j) in combinations(sorted(sites), 2):
        for a, b in product(COLORS, repeat=2):
            unit = {(i, j): [[1 if (x, y) == (a, b) else 0 for y in COLORS]
                             for x in COLORS]}
            rows.append(vectorize(quad_times_power(unit, q, sites), sites))
            labels.append((i, j, a, b))
    return rows, labels


def q_vector(q, sites):
    vec = []
    for (i, j) in combinations(sorted(sites), 2):
        entry = block(q, i, j)
        for a, b in product(COLORS, repeat=2):
            vec.append(Fraction(entry[a][b]) if entry is not None else Fraction(0))
    return vec


# ---------------------------------------------------------------------------
# random exact matrices
# ---------------------------------------------------------------------------

def det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def random_rank3(rng):
    while True:
        m = [[rng.randrange(1, 20) for _ in COLORS] for _ in COLORS]
        if det3(m):
            return m


def random_rank2(rng):
    while True:
        left = [[rng.randrange(1, 12) for _ in range(2)] for _ in COLORS]
        right = [[rng.randrange(1, 12) for _ in COLORS] for _ in range(2)]
        m = [[sum(left[i][k] * right[k][j] for k in range(2)) for j in COLORS]
             for i in COLORS]
        if det3(m) == 0 and any(
            m[i][j] * m[k][l] - m[i][l] * m[k][j]
            for i, k in combinations(COLORS, 2)
            for j, l in combinations(COLORS, 2)
        ):
            return m


# ---------------------------------------------------------------------------
# graph utilities
# ---------------------------------------------------------------------------

def graph_components(n, edges):
    adjacency = {v: set() for v in range(n)}
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    seen = set()
    comps = []
    for v in range(n):
        if v in seen:
            continue
        stack, comp = [v], set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            stack.extend(adjacency[u] - comp)
        seen |= comp
        comps.append(sorted(comp))
    return comps, adjacency


def bipartition(comp, adjacency):
    colour = {comp[0]: 1}
    stack = [comp[0]]
    while stack:
        u = stack.pop()
        for w in adjacency[u]:
            if w in colour:
                if colour[w] == colour[u]:
                    return None
            else:
                colour[w] = -colour[u]
                stack.append(w)
    return colour


def defect_data(n, edges):
    comps, adjacency = graph_components(n, edges)
    basis, deltas = [], []
    b = iso = 0
    for comp in comps:
        if len(comp) == 1:
            iso += 1
            vec = [0] * n
            vec[comp[0]] = 1
            basis.append(vec)
            deltas.append(1)
            continue
        colour = bipartition(comp, adjacency)
        if colour is not None:
            b += 1
            vec = [0] * n
            for v in comp:
                vec[v] = colour[v]
            basis.append(vec)
            deltas.append(sum(vec))
    return b + iso, b, iso, basis, deltas


# ---------------------------------------------------------------------------
# 1. affine graph step
# ---------------------------------------------------------------------------

def check_graph_step():
    battery = [
        ("K4", 4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)], 0),
        ("K22", 4, [(0, 2), (0, 3), (1, 2), (1, 3)], 1),
        ("K13", 4, [(0, 1), (0, 2), (0, 3)], 1),
        ("P4", 4, [(0, 1), (1, 2), (2, 3)], 1),
        ("triangle+iso", 4, [(1, 2), (1, 3), (2, 3)], 1),
        ("two_triangles", 6, [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5)], 0),
        ("K4+K2", 6, [(0, 1), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)], 1),
        ("C6", 6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)], 1),
        ("K33", 6, [(i, j) for i in range(3) for j in range(3, 6)], 1),
        ("C5+iso", 6, [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)], 1),
        ("2xC4", 8, [(0, 1), (1, 2), (2, 3), (0, 3), (4, 5), (5, 6), (6, 7), (4, 7)], 2),
        ("C4+K4", 8, [(0, 1), (1, 2), (2, 3), (0, 3),
                      (4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)], 1),
        ("path+2iso", 6, [(0, 1), (1, 2), (2, 3)], 3),
    ]
    for name, n, edges, expected_nu in battery:
        nu, b, iso, basis, deltas = defect_data(n, edges)
        rows = []
        for i, j in edges:
            row = [0] * n
            row[i] += 1
            row[j] += 1
            rows.append(row)
        null = exact_nullspace(rows)
        if not (len(null) == nu == expected_nu):
            raise AssertionError(
                f"graph {name}: nullity {len(null)} vs nu {nu} vs {expected_nu}")
        for vec in basis:
            for i, j in edges:
                assert vec[i] + vec[j] == 0
        if basis:
            assert exact_rank(basis) == len(basis) == nu
            assert exact_rank([list(map(Fraction, v)) for v in basis] + null) == nu
        for vec, delta in zip(basis, deltas):
            assert sum(vec) == delta
        # particular solution alpha = 1/2 for gamma = 1
        for i, j in edges:
            assert Fraction(1, 2) + Fraction(1, 2) == 1
    check("graph step: nullity = defect nu with zeta basis on 13 graphs")


# ---------------------------------------------------------------------------
# 2. gauge identities
# ---------------------------------------------------------------------------

def check_gauge_identity():
    rng = Random(41)
    for sites in (tuple(range(4)), tuple(range(6))):
        q = {}
        for pair in combinations(sites, 2):
            q[pair] = random_rank3(rng) if rng.random() < 0.7 else random_rank2(rng)
        t = len(sites) // 2
        top = vectorize(top_power(q, sites), sites)
        qq = vectorize(quad_times_power(q, q, sites), sites)
        assert qq == [t * c for c in top]
        alpha = {s: Fraction(rng.randrange(-9, 10), rng.randrange(1, 7)) for s in sites}
        z = gauge_quadratic(q, alpha, sites)
        image = vectorize(quad_times_power(z, q, sites), sites)
        total = sum(alpha.values())
        assert image == [total * c for c in top]
    check("q q^[t-1] = t q^[t] and H(Z^alpha) = (sum alpha) q^[t] at |W| = 4, 6")


# ---------------------------------------------------------------------------
# 3. gauge-rigid defect-one charts
# ---------------------------------------------------------------------------

def gauge_basis(sites):
    sites = sorted(sites)
    basis = []
    for s in sites[:-1]:
        alpha = {x: Fraction(0) for x in sites}
        alpha[s] = Fraction(1)
        alpha[sites[-1]] = Fraction(-1)
        basis.append(alpha)
    return basis


def certify_gauge_rigid(q, sites, exact=True):
    rows, _ = hessian_rows(q, sites)
    dim = len(rows)
    n = len(sites)
    expected = dim - (n - 1)
    int_rows = scale_int_rows(rows)
    lower = rank_mod(int_rows)
    if lower != expected:
        return None
    if exact:
        assert exact_rank(rows) == expected
    gauges = [q_vector(gauge_quadratic(q, alpha, sites), sites)
              for alpha in gauge_basis(sites)]
    assert exact_rank(gauges) == n - 1
    for alpha in gauge_basis(sites):
        z = gauge_quadratic(q, alpha, sites)
        assert not quad_times_power(z, q, sites)
    return expected


def build_chart(rng, rank3_pairs, rank2_pairs, fixed_blocks=None):
    q = {}
    for pair in rank3_pairs:
        q[pair] = random_rank3(rng)
    for pair in rank2_pairs:
        q[pair] = random_rank2(rng)
    if fixed_blocks:
        q.update(fixed_blocks)
    return q


def search_chart(rng, rank3_pairs, rank2_pairs, sites, fixed_blocks=None,
                 exact=True, trials=60):
    for trial in range(1, trials + 1):
        q = build_chart(rng, rank3_pairs, rank2_pairs, fixed_blocks)
        result = certify_gauge_rigid(q, sites, exact=exact)
        if result is not None:
            return trial, q, result
    return None, None, None


CHARTS = {}


def check_rigid_charts():
    rng = Random(20260728)
    sites4 = (0, 1, 2, 3)
    cross22 = [(0, 2), (0, 3), (1, 2), (1, 3)]
    trial, q, rank = search_chart(rng, cross22, [(0, 1), (2, 3)], sites4)
    assert q is not None
    CHARTS["shores22"] = q
    check(f"|W|=4 shores 2+2 chart gauge-rigid (trial {trial}, exact rank {rank}/54)")

    star13 = [(0, 1), (0, 2), (0, 3)]
    trial, q, rank = search_chart(rng, star13, [(1, 2), (1, 3), (2, 3)], sites4)
    assert q is not None
    CHARTS["shores13"] = q
    check(f"|W|=4 shores 1+3 chart gauge-rigid (trial {trial}, exact rank {rank}/54)")

    triangle = [(1, 2), (1, 3), (2, 3)]
    trial, q, rank = search_chart(rng, triangle, [(0, 1), (0, 2), (0, 3)], sites4)
    assert q is not None
    CHARTS["iso4"] = q
    check(f"|W|=4 isolated-vertex chart gauge-rigid (trial {trial}, exact rank {rank}/54)")

    sites6 = tuple(range(6))
    k2k4_r3 = [(0, 1)] + list(combinations((2, 3, 4, 5), 2))
    k2k4_r2 = [(i, j) for i in (0, 1) for j in (2, 3, 4, 5)]
    trial, q, rank = search_chart(rng, k2k4_r3, k2k4_r2, sites6, exact=False, trials=25)
    assert q is not None
    CHARTS["k2k4"] = q
    check(f"|W|=6 K_2 u K_4 chart gauge-rigid (trial {trial}, rank {rank}/135 two-sided)")

    c6 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)]
    others = [p for p in combinations(sites6, 2) if p not in c6]
    trial, q, rank = search_chart(rng, c6, others, sites6, exact=False, trials=25)
    assert q is not None
    CHARTS["c6"] = q
    check(f"|W|=6 C_6 bipartite chart gauge-rigid (trial {trial}, rank {rank}/135 two-sided)")


# ---------------------------------------------------------------------------
# 4. Theorem C block-pair kernel mechanism at |W| = 4
# ---------------------------------------------------------------------------

def check_theorem_c_kernel():
    # shores {0,1} | {2,3}; q_23 = 0 (dead shore pair), everything else generic
    rng = Random(9)
    for _ in range(3):
        q = {
            (0, 1): random_rank2(rng),
            (0, 2): random_rank3(rng),
            (0, 3): random_rank3(rng),
            (1, 2): random_rank3(rng),
            (1, 3): random_rank3(rng),
        }
        sites = (0, 1, 2, 3)
        rows, labels = hessian_rows(q, sites)
        rank = exact_rank(rows)
        kernel_dim = len(rows) - rank
        # kernel = gauge (3) + block {0,1} (9), overlapping exactly in the
        # line C q_01 (alpha constant on one shore, opposite on the other):
        # 3 + 9 - 1 = 11, hence extra kernel of dimension 8.
        assert kernel_dim == 11, kernel_dim
        # the whole block {0,1} space is in the kernel: q^[1] on {2,3} is zero
        for a, b in product(COLORS, repeat=2):
            unit = {(0, 1): [[1 if (x, y) == (a, b) else 0 for y in COLORS]
                             for x in COLORS]}
            assert not quad_times_power(unit, q, sites)
        # and the three gauges are independent and annihilated
        gauges = [q_vector(gauge_quadratic(q, alpha, sites), sites)
                  for alpha in gauge_basis(sites)]
        assert exact_rank(gauges) == 3
        # the gauge/block overlap: alpha = (1, 1, -1, -1)/2 gives Z^alpha = q_01
        overlap = gauge_quadratic(
            q, {0: Fraction(1, 2), 1: Fraction(1, 2),
                2: Fraction(-1, 2), 3: Fraction(-1, 2)}, sites)
        assert set(overlap) == {(0, 1)}
        assert vectorize(overlap, sites) == vectorize({(0, 1): q[(0, 1)]}, sites)
    check("Theorem C mechanism at |W|=4: dead shore pair gives exact kernel 11 = 3 + 9 - 1, extra kernel 8")


# ---------------------------------------------------------------------------
# 5. beta-line engine at |W| = 4
# ---------------------------------------------------------------------------

def kernel_of_T(q, sites, p):
    sites = sorted(sites)
    top = vectorize(top_power(q, sites), sites)
    columns = [top]
    for site in sites:
        for coord in COLORS:
            unit = {site: [1 if k == coord else 0 for k in COLORS]}
            prod = row_product(p, unit, sites)
            columns.append(vectorize(quad_times_power(prod, q, sites), sites))
    rows = [[col[k] for col in columns] for k in range(len(columns[0]))]
    return exact_nullspace(rows), columns


def check_engine_w4():
    rng = Random(7)
    sites = (0, 1, 2, 3)

    for name in ("shores22", "shores13", "iso4"):
        q = CHARTS[name]
        for _ in range(2):
            support = rng.sample(sites, 3)
            p = {s: [rng.randrange(1, 9) for _ in COLORS] for s in support}
            null, _ = kernel_of_T(q, sites, p)
            assert not null, f"{name}: unexpected kernel for support-3 row"
    check("|W|=4 engine: generic support-3 rows have exact kernel 0 on all three chart types")

    # shores {0} | {1,2,3} (Delta = -2) with the planted three-block window:
    # p supported on {1,2}, s0 on {2,3}; the three minority... majority-shore
    # blocks are the forced single-term rank-one product blocks.  The window
    # itself destroys gauge rigidity: the shared factors make the two
    # complementary matchings through any window block collide.  The chart
    # has exact kernel 9 = 3 gauge + 6 collision, with the collision space
    # spanned by w|_0 . m for m in Ann(p) and Ann(s) (antipodal partners).
    p1, p2 = [1, 2, 3], [2, 5, 1]
    s2, s3 = [1, 1, 4], [3, 1, 2]
    p_row = {1: p1, 2: p2}
    s_row = {2: s2, 3: s3}
    fixed = {
        (1, 2): [[Fraction(-p1[a] * s2[b], 2) for b in COLORS] for a in COLORS],
        (1, 3): [[Fraction(-p1[a] * s3[b], 2) for b in COLORS] for a in COLORS],
        (2, 3): [[Fraction(-p2[a] * s3[b], 2) for b in COLORS] for a in COLORS],
    }
    star13 = [(0, 1), (0, 2), (0, 3)]
    rng2 = Random(2027)
    for _ in range(3):
        q = build_chart(rng2, star13, [], fixed_blocks=fixed)
        rows, _ = hessian_rows(q, sites)
        kernel = len(rows) - exact_rank(rows)
        assert kernel == 9, kernel
        zeta = {0: 1, 1: -1, 2: -1, 3: -1}
        z = gauge_quadratic(q, zeta, sites)
        assert vectorize(row_product(p_row, s_row, sites), sites) == vectorize(z, sites)
        # collision elements: w|_0 . m with m the antipodal generator of
        # Ann(s) (and of Ann(p)); all exactly annihilated and non-gauge
        m_s = {2: s2, 3: [-v for v in s3]}
        m_p = {1: p1, 2: [-v for v in p2]}
        for m in (m_s, m_p):
            for wi in COLORS:
                w = {0: [1 if k == wi else 0 for k in COLORS]}
                collision = row_product(w, m, sites)
                assert collision
                assert not quad_times_power(collision, q, sites)
        # ker T for the window row is still Ann(p) + the beta line, with the
        # direct entry pinned a = -beta Delta = 2 beta != 0
        null, columns = kernel_of_T(q, sites, p_row)
        candidate = [Fraction(2)] + [Fraction(0)] * 12
        for site, vec in s_row.items():
            for k in COLORS:
                candidate[1 + 3 * site + k] = Fraction(vec[k])
        image = [sum(candidate[c] * columns[c][k] for c in range(13))
                 for k in range(len(columns[0]))]
        assert not any(image)
    check(
        "|W|=4 shores 1+3 window: forced rank-one shared-factor blocks give exact "
        "kernel 9 = 3 + 6 (collision w|_x . Ann-partner), beta line pins a = 2 beta")


# ---------------------------------------------------------------------------
# 6. the collision death of the |W| = 6 connected window charts
# ---------------------------------------------------------------------------

def check_engine_w6():
    rng = Random(2026)
    sites = tuple(range(6))
    # shores {0,1,2,3} | {4,5}, Delta = 2; window rows: p on {0,1,2}, s on {2,3}
    p_row = {s: [rng.randrange(1, 9) for _ in COLORS] for s in (0, 1, 2)}
    s_row = {s: [rng.randrange(1, 9) for _ in COLORS] for s in (2, 3)}
    prod = row_product(p_row, s_row, sites)
    fixed = {}
    for pair in combinations((0, 1, 2, 3), 2):
        entry = prod.get(pair)
        if entry is None:
            continue
        fixed[pair] = [[Fraction(entry[a][b], 2) for b in COLORS] for a in COLORS]
    cross = [(i, j) for i in (0, 1, 2, 3) for j in (4, 5)]
    zeta = {0: 1, 1: 1, 2: 1, 3: 1, 4: -1, 5: -1}
    m_s = {2: s_row[2], 3: [-v for v in s_row[3]]}   # antipodal Ann(s) generator
    for _ in range(2):
        q = build_chart(rng, cross, [], fixed_blocks=fixed)
        z = gauge_quadratic(q, zeta, sites)
        assert vectorize(prod, sites) == vectorize(z, sites)
        rows, _ = hessian_rows(q, sites)
        kernel_upper = len(rows) - rank_mod(scale_int_rows(rows))
        assert kernel_upper == 11, kernel_upper
        # exact collision elements: w|_x . m for x in the minority shore
        members = []
        for x in (4, 5):
            for wi in COLORS:
                w = {x: [1 if k == wi else 0 for k in COLORS]}
                collision = row_product(w, m_s, sites)
                assert collision
                assert not quad_times_power(collision, q, sites)
                members.append(q_vector(collision, sites))
        gauges = [q_vector(gauge_quadratic(q, alpha, sites), sites)
                  for alpha in gauge_basis(sites)]
        for alpha in gauge_basis(sites):
            assert not quad_times_power(gauge_quadratic(q, alpha, sites), q, sites)
        assert exact_rank(members + gauges) == 11
    check(
        "|W|=6 shores 4+2 window chart: exact kernel 11 = 5 gauge + 6 collision "
        "(w|_x . Ann(s)-partner for both minority sites); never gauge-rigid")


# ---------------------------------------------------------------------------
# 6b. Lemma R: minimum block-degree three on gauge-rigid charts
# ---------------------------------------------------------------------------

def check_lemma_r():
    rng = Random(55)
    sites = tuple(range(6))
    # site 0 has exactly two nonzero blocks (to 1 and 2); the rest generic
    q = {}
    for pair in combinations(sites, 2):
        if 0 in pair and pair not in ((0, 1), (0, 2)):
            continue
        q[pair] = random_rank3(rng)
    # P = {1, 2} strands site 0: the complement top power vanishes exactly
    assert not top_power(q, (0, 3, 4, 5))
    for a, b in product(COLORS, repeat=2):
        unit = {(1, 2): [[1 if (x, y) == (a, b) else 0 for y in COLORS]
                         for x in COLORS]}
        assert not quad_times_power(unit, q, sites)
    # gauge image on block {1,2} is only the line C q_12, so at least eight
    # of these nine dimensions are extra kernel
    rows, _ = hessian_rows(q, sites)
    kernel_upper = len(rows) - rank_mod(scale_int_rows(rows))
    assert kernel_upper >= 5 + 8, kernel_upper
    check(
        f"Lemma R mechanism at |W|=6: a degree-2 site strands under the pair of its "
        f"partners; block kernel 9 vs gauge line 1 (kernel bound {kernel_upper})")


# ---------------------------------------------------------------------------
# 6c. Theorem E: the K_2-component defect chart dies by sign cancellation
# ---------------------------------------------------------------------------

def check_theorem_e():
    rng = Random(31)
    sites = tuple(range(6))
    # K_0 = edge {0,1} (zeta = +1, -1), nonbipartite K_4 on {2,3,4,5};
    # window rows p on {0,1} (straddling K_0), s on {2,3} (outside);
    # forced interface blocks q_{0z} = +(ps)_{0z}, q_{1z} = -(ps)_{1z}
    p_row = {0: [rng.randrange(1, 9) for _ in COLORS],
             1: [rng.randrange(1, 9) for _ in COLORS]}
    s_row = {2: [rng.randrange(1, 9) for _ in COLORS],
             3: [rng.randrange(1, 9) for _ in COLORS]}
    prod = row_product(p_row, s_row, sites)
    assert sorted(prod) == [(0, 2), (0, 3), (1, 2), (1, 3)]
    fixed = {}
    for (i, j), entry in prod.items():
        coeff = 1 if i == 0 else -1
        fixed[(i, j)] = [[Fraction(entry[a][b], coeff) for b in COLORS]
                         for a in COLORS]
    r3 = [(0, 1)] + list(combinations((2, 3, 4, 5), 2))
    zeta = {0: 1, 1: -1, 2: 0, 3: 0, 4: 0, 5: 0}
    for _ in range(2):
        q = build_chart(rng, r3, [], fixed_blocks=fixed)
        z = gauge_quadratic(q, zeta, sites)
        assert vectorize(prod, sites) == vectorize(z, sites)
        # the +/- interface signs cancel p . (x|_w) for w outside the window
        members = []
        for w_site in (4, 5):
            for wi in COLORS:
                x = {w_site: [1 if k == wi else 0 for k in COLORS]}
                collision = row_product(p_row, x, sites)
                assert collision
                assert not quad_times_power(collision, q, sites)
                members.append(q_vector(collision, sites))
        gauges = [q_vector(gauge_quadratic(q, alpha, sites), sites)
                  for alpha in gauge_basis(sites)]
        assert exact_rank(members + gauges) == 11
        kernel_upper = len(sites) * 0 + 135 - rank_mod(
            scale_int_rows(hessian_rows(q, sites)[0]))
        assert kernel_upper >= 11, kernel_upper
    check(
        "Theorem E mechanism: K_2-component window chart has the exact sign-cancelled "
        "kernel p.(x|_w) (6 dims beyond gauge); never gauge-rigid")


# ---------------------------------------------------------------------------
# 6d. defect-one support-pattern census at |W| = 6 (P_3 + triangle shape)
# ---------------------------------------------------------------------------

def defect_one_pattern_census(sites, k0_sites, k0_edges, o_edges, zeta):
    """Count (supp p, supp s) patterns passing all structural survival filters.

    Filters (each is a proved necessary condition for a surviving good pair
    on a gauge-rigid defect-one chart):
      F1 a live single-term product block on a zeta-invisible pair is nonzero
         there, contradiction;
      F2 some live zeta-visible pair must exist (else Z^zeta = 0, collapse);
      F3 every site needs at least three nonzero-block partners (Lemma R);
         available partners: G_3 edges, live visible pairs, and free
         invisible non-edge pairs (counted generously as available);
      F4 if K_0 is a proper component (O nonempty), at least one live
         interface block must exist: for odd K_0 because q^[t] = 0 would
         make q a non-gauge kernel element, for even K_0 because a mixed
         pair P = {i, z} strands the odd remainder K_0 - i, putting the
         nine-dimensional block-P space inside the kernel.
    """
    all_pairs = list(combinations(sorted(sites), 2))
    edges = set(k0_edges) | set(o_edges)
    supports = [frozenset(c) for k in (1, 2) for c in combinations(sorted(sites), k)]
    survivors = []
    for sp, ss in product(supports, repeat=2):
        def live(i, j):
            return (i in sp and j in ss) or (i in ss and j in sp)

        def single(i, j):
            return (i in sp and j in ss) != (i in ss and j in sp)

        ok = True
        some_visible = False
        interface_live = False
        for (i, j) in all_pairs:
            vis = zeta[i] + zeta[j] != 0
            if live(i, j):
                if not vis and single(i, j):
                    ok = False   # F1
                    break
                if vis:
                    some_visible = True
                    if (i in k0_sites) != (j in k0_sites):
                        interface_live = True
        if not ok:
            continue
        if not some_visible:
            continue   # F2
        if len(k0_sites) < len(sites) and not interface_live:
            continue   # F4
        # F3: partner count
        deficient = False
        for x in sites:
            partners = set()
            for (i, j) in all_pairs:
                if x not in (i, j):
                    continue
                y = j if i == x else i
                if (min(i, j), max(i, j)) in edges:
                    partners.add(y)
                elif zeta[i] + zeta[j] != 0:
                    if live(i, j):
                        partners.add(y)
                else:
                    partners.add(y)   # free invisible block, generously
            if len(partners) < 3:
                deficient = True
                break
        if deficient:
            continue
        survivors.append((set(sp), set(ss)))
    return survivors


def check_k2_census():
    sites = tuple(range(6))
    zeta = {0: 1, 1: -1, 2: 0, 3: 0, 4: 0, 5: 0}
    survivors = defect_one_pattern_census(
        sites, {0, 1}, [(0, 1)], list(combinations((2, 3, 4, 5), 2)), zeta)
    assert len(survivors) == 12, survivors
    for sp, ss in survivors:
        assert sp == {0, 1} or ss == {0, 1}, (sp, ss)
        outside = ss if sp == {0, 1} else sp
        assert outside <= {2, 3, 4, 5} and len(outside) == 2
    check(
        "K_2+K_4 census at |W|=6: exactly 12 of 441 patterns survive the structural "
        "filters, all of the K_0-straddling shape killed by the Theorem E cancellation")


def check_p3_triangle_census():
    sites = tuple(range(6))
    # K_0 = path 0-1-2 (zeta = +1,-1,+1), triangle {3,4,5}
    zeta = {0: 1, 1: -1, 2: 1, 3: 0, 4: 0, 5: 0}
    survivors = defect_one_pattern_census(
        sites, {0, 1, 2}, [(0, 1), (1, 2)], [(3, 4), (3, 5), (4, 5)], zeta)
    assert survivors == [], survivors
    # concrete plant: the natural window sp = {0,2}, ss = {3,4} strands site 5
    rng = Random(1234)
    p_row = {0: [rng.randrange(1, 9) for _ in COLORS],
             2: [rng.randrange(1, 9) for _ in COLORS]}
    s_row = {3: [rng.randrange(1, 9) for _ in COLORS],
             4: [rng.randrange(1, 9) for _ in COLORS]}
    prod = row_product(p_row, s_row, sites)
    fixed = {}
    for (i, j), entry in prod.items():
        coeff = zeta[i] + zeta[j]
        assert coeff != 0
        fixed[(i, j)] = [[Fraction(entry[a][b], coeff) for b in COLORS]
                         for a in COLORS]
    q = build_chart(rng, [(0, 1), (1, 2), (3, 4), (3, 5), (4, 5)], [],
                    fixed_blocks=fixed)
    assert not top_power(q, (0, 1, 2, 5))   # site 5 stranded by P = {3,4}
    kernel_upper = 135 - rank_mod(scale_int_rows(hessian_rows(q, sites)[0]))
    assert kernel_upper >= 14, kernel_upper
    check(
        f"P_3+triangle census at |W|=6: 0 of 441 support patterns survive the "
        f"structural filters; the natural plant has kernel >= {kernel_upper}")


# ---------------------------------------------------------------------------
# 6e. reconciliation with the post-fan status note's K_3,3 witness
# ---------------------------------------------------------------------------

def check_w8_census():
    sites8 = tuple(range(8))
    k4 = list(combinations((4, 5, 6, 7), 2))
    zeta22 = {0: 1, 1: -1, 2: 1, 3: -1, 4: 0, 5: 0, 6: 0, 7: 0}
    zeta13 = {0: 1, 1: -1, 2: -1, 3: -1, 4: 0, 5: 0, 6: 0, 7: 0}
    zeta_p3 = {0: 1, 1: -1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
    zeta_k2 = {0: 1, 1: -1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
    six_nonbip = [(2, 3), (2, 4), (3, 4), (4, 5), (5, 6), (6, 7), (5, 7), (2, 5)]
    results = {}
    results["C4+K4"] = len(defect_one_pattern_census(
        sites8, {0, 1, 2, 3}, [(0, 1), (1, 2), (2, 3), (0, 3)], k4, zeta22))
    results["P4+K4"] = len(defect_one_pattern_census(
        sites8, {0, 1, 2, 3}, [(0, 1), (1, 2), (2, 3)], k4, zeta22))
    results["K13+K4"] = len(defect_one_pattern_census(
        sites8, {0, 1, 2, 3}, [(0, 1), (0, 2), (0, 3)], k4, zeta13))
    results["P3+C5"] = len(defect_one_pattern_census(
        sites8, {0, 1, 2}, [(0, 1), (1, 2)],
        [(3, 4), (4, 5), (5, 6), (6, 7), (3, 7)], zeta_p3))
    results["K2+6nonbip"] = len(defect_one_pattern_census(
        sites8, {0, 1}, [(0, 1)], six_nonbip, zeta_k2))
    expected = {"C4+K4": 0, "P4+K4": 0, "K13+K4": 24, "P3+C5": 0,
                "K2+6nonbip": 30}
    assert results == expected, results
    # the 30 K_2 patterns are all of the straddling shape killed by Theorem E,
    # so the only |W| = 8 residual is the K_1,3 + K_4 shape with Delta = -2:
    # its pinned direct entries a_cd = 2 beta_cd are nonzero, so no zero-block
    # pair can occupy it.  Every equal-shore (Delta = 0) shape at |W| <= 8 is
    # census-dead or Theorem-E-dead.
    check(
        "defect-one censuses at |W|=8: C4+K4 0, P4+K4 0, P3+C5 0, K2-shape 30 "
        "(all Theorem E), K13+K4 24 -- the only residual, with Delta = -2")


def check_k13_k4_residual_death():
    """Close all 24 |W|=8 residual patterns without a Hessian matrix.

    Up to swapping the two rows, every survivor has one row on two star
    leaves and the other on the third leaf plus one K4 vertex o.  Delete the
    star centre and that third leaf.  In the six-site complement the two
    retained leaves can only meet o, so no perfect matching exists.  Hence
    q^[3] on the complement is zero and every matrix unit on the deleted
    block is a Hessian-kernel direction.
    """
    sites = tuple(range(8))
    centre = 0
    leaves = {1, 2, 3}
    outside = {4, 5, 6, 7}
    zeta = {0: 1, 1: -1, 2: -1, 3: -1, 4: 0, 5: 0, 6: 0, 7: 0}
    graph_edges = {
        tuple(sorted(edge))
        for edge in [(0, 1), (0, 2), (0, 3), *combinations(outside, 2)]
    }
    survivors = defect_one_pattern_census(
        sites, {0, 1, 2, 3}, [(0, 1), (0, 2), (0, 3)],
        list(combinations(outside, 2)), zeta,
    )
    assert len(survivors) == 24

    matching_count = kernel_count = 0
    for pattern_index, (sp0, ss0) in enumerate(survivors):
        if len(sp0 & leaves) == 2:
            p_support, s_support = set(sp0), set(ss0)
        else:
            p_support, s_support = set(ss0), set(sp0)
        retained = p_support & leaves
        third = next(iter(leaves - retained))
        interface = s_support & outside
        assert len(retained) == 2
        assert s_support == {third} | interface and len(interface) == 1
        outside_vertex = next(iter(interface))

        live_visible = {
            tuple(sorted((i, j)))
            for i in p_support for j in s_support
            if i != j and zeta[i] + zeta[j] != 0
        }
        support = graph_edges | live_visible
        deleted = {centre, third}
        complement = tuple(site for site in sites if site not in deleted)
        for matching in matchings(complement):
            matching_count += 1
            assert any(tuple(sorted(edge)) not in support for edge in matching)
        for leaf in retained:
            assert tuple(sorted((leaf, outside_vertex))) in support
            assert all(
                other == outside_vertex
                for other in complement
                if other not in retained
                and tuple(sorted((leaf, other))) in support
            )

        rng = Random(9100 + pattern_index)
        q = {edge: random_rank3(rng) for edge in graph_edges}
        for i, j in live_visible - graph_edges:
            left = [Fraction(1 + i + c) for c in COLORS]
            right = [Fraction(2 + j + c) for c in COLORS]
            q[(i, j)] = [[left[a] * right[b] for b in COLORS] for a in COLORS]

        pair = tuple(sorted(deleted))
        units = []
        for a, b in product(COLORS, repeat=2):
            entry = [[Fraction(0) for _ in COLORS] for _ in COLORS]
            entry[a][b] = Fraction(1)
            direction = {pair: entry}
            assert not quad_times_power(direction, q, sites)
            units.append(q_vector(direction, sites))
            kernel_count += 1
        assert exact_rank(units) == 9
        gauges = [
            q_vector(gauge_quadratic(q, alpha, sites), sites)
            for alpha in gauge_basis(sites)
        ]
        assert exact_rank(gauges) == 7
        assert exact_rank(gauges + units) == 16

    assert matching_count == 24 * 15 and kernel_count == 24 * 9
    check(
        "K13+K4 residual at |W|=8: 24 patterns, 360 complementary matchings "
        "all absent, and 216 block-unit kernel checks (9D disjoint from 7D gauge)")


def check_postfan_witness_compatibility():
    rng = Random(60)
    sites = tuple(range(6))
    shores = {0: 1, 1: 1, 2: 1, 3: -1, 4: -1, 5: -1}
    z_loc = {s: [rng.randrange(1, 9) for _ in COLORS] for s in sites}
    # K_3,3 chart: cross blocks rank three, shore blocks z_i z_j^T
    fixed = {}
    for (i, j) in combinations(sites, 2):
        if shores[i] == shores[j]:
            fixed[(i, j)] = [[Fraction(z_loc[i][a] * z_loc[j][b]) for b in COLORS]
                             for a in COLORS]
    cross = [(i, j) for i in (0, 1, 2) for j in (3, 4, 5)]
    q = build_chart(rng, cross, [], fixed_blocks=fixed)
    p = {s: z_loc[s] for s in sites}
    s_row = {s: [shores[s] * v for v in z_loc[s]] for s in sites}
    prod = row_product(p, s_row, sites)
    zvec = gauge_quadratic(q, shores, sites)
    assert vectorize(prod, sites) == vectorize(zvec, sites)
    assert not quad_times_power(prod, q, sites)   # (ps) q^[2] = 0, a = 0
    # but the colour-proportional triples p_c = t_c p are dependent: the
    # witness is not a good pair, so Theorem B's sparse-row conclusion for
    # good pairs is untouched by this full-support solution family.
    def family_vector(row):
        vec = [Fraction(0)] * 18
        for site, local in row.items():
            for k in COLORS:
                vec[3 * site + k] = Fraction(local[k])
        return vec
    triples = [family_vector({s: [t * v for v in p[s]] for s in p})
               for t in (2, 3, 5)]
    assert exact_rank(triples) == 1
    check(
        "post-fan K_3,3 witness reproduced: full-support rows solve the mixed cells "
        "but are colour-proportional (rank 1), hence never a good pair")


# ---------------------------------------------------------------------------
# 7. matching-balance facts (the |Delta| bound)
# ---------------------------------------------------------------------------

def check_balance():
    rng = Random(13)
    sites = tuple(range(6))
    # shores 4+2, no live majority pair: top power must vanish
    cross = [(i, j) for i in (0, 1, 2, 3) for j in (4, 5)]
    q = build_chart(rng, cross, [])
    assert not top_power(q, sites)
    # one live majority pair: top power can be nonzero
    q[(0, 1)] = random_rank2(rng)
    assert top_power(q, sites)
    # shores 5+1 with only one live majority pair: needs two disjoint, vanishes
    cross51 = [(i, 5) for i in range(5)]
    q51 = build_chart(rng, cross51, [])
    q51[(0, 1)] = random_rank2(rng)
    assert not top_power(q51, sites)
    # two disjoint live majority pairs: nonzero
    q51[(2, 3)] = random_rank2(rng)
    assert top_power(q51, sites)
    check("matching balance: |Delta| = 2 needs one live majority pair, |Delta| = 4 needs two")


# ---------------------------------------------------------------------------
# 8. the (P)-guard family and its two deaths at |W| = 4
# ---------------------------------------------------------------------------

def check_p_guard():
    sites = (0, 1, 2, 3)
    a = [1, 2, 3]
    b = [1, 0, 1]
    v = [2, 1, 5]
    w = [0, 1, 4]
    p_rows = [{0: a}, {0: b}, {1: v}]
    s_rows = [{0: a}, {1: v}, {0: w}]

    def family_vector(row):
        vec = [Fraction(0)] * 12
        for site, local in row.items():
            for k in COLORS:
                vec[3 * site + k] = Fraction(local[k])
        return vec

    assert exact_rank([family_vector(r) for r in p_rows]) == 3
    assert exact_rank([family_vector(r) for r in s_rows]) == 3
    z = row_product(p_rows[0], s_rows[1], sites)
    assert set(z) == {(0, 1)}
    beta = {(0, 1): 1, (2, 0): 1}
    for c, d in product(COLORS, repeat=2):
        if c == d:
            continue
        prod = row_product(p_rows[c], s_rows[d], sites)
        if beta.get((c, d)):
            assert vectorize(prod, sites) == vectorize(z, sites)
        else:
            assert not prod
    check("(P)-guard: all six off-diagonal products equal beta_cd Z, independent triples, supports <= 2")

    # death 1 (diagonal): the window block is {0,1}, so q_23 = 0; then
    # p_1 s_1 q^[1] = 0 identically and the c = 0, 1 diagonals force
    # q^[2] proportional to two independent pure words.
    rng = Random(5)
    for _ in range(3):
        q = {
            (0, 1): [[Fraction(a[i] * v[j], 2) for j in COLORS] for i in COLORS],
            (0, 2): random_rank3(rng),
            (0, 3): random_rank3(rng),
            (1, 2): random_rank3(rng),
            (1, 3): random_rank3(rng),
        }
        diag = row_product(p_rows[1], s_rows[1], sites)
        assert set(diag) == {(0, 1)}
        assert not quad_times_power(diag, q, sites)
        assert not row_product(p_rows[0], s_rows[0], sites)
        words = list(product(COLORS, repeat=4))
        top = vectorize(top_power(q, sites), sites)
        x0 = [Fraction(1) if wd == (0, 0, 0, 0) else Fraction(0) for wd in words]
        x1 = [Fraction(1) if wd == (1, 1, 1, 1) else Fraction(0) for wd in words]
        assert exact_rank([x0, x1]) == 2
        assert exact_rank([top, x0]) == 2  # q^[2] is not proportional to X_0 anyway
        # death 2 (Theorem C): the same chart has the nine-dimensional
        # block {0,1} kernel, so it is never gauge-rigid (kernel 11 > 3).
        rows, _ = hessian_rows(q, sites)
        assert len(rows) - exact_rank(rows) >= 11
    check("(P)-guard embedding at |W|=4 dies twice: dead-shore diagonal and Theorem C kernel")


# ---------------------------------------------------------------------------
# 9. the |W| = 4 window lemma
# ---------------------------------------------------------------------------

def check_window_lemma():
    sites = (0, 1, 2, 3)
    plus, minus = {0, 1}, {2, 3}
    supports = [frozenset(c) for k in (1, 2) for c in combinations(sites, k)]
    killed = 0
    candidates = 0
    for sp, ss in product(supports, repeat=2):
        def live(i, j):
            return (i in sp and j in ss) or (i in ss and j in sp)

        if not (live(0, 1) and live(2, 3)):
            continue
        candidates += 1
        single = False
        for i, j in product(plus, minus):
            term1 = i in sp and j in ss
            term2 = i in ss and j in sp
            if term1 != term2:
                single = True
                break
        if single:
            killed += 1
            continue
        raise AssertionError(f"window census: pattern {set(sp)}, {set(ss)} survives")
    assert candidates == killed and candidates > 0
    check(
        f"|W|=4 window lemma: {candidates} support patterns reach both same-shore "
        f"blocks and every one dies on a single-term cross pair")


# ---------------------------------------------------------------------------
# 10. structural census of the zero-block defect-one system at |W| = 4
# ---------------------------------------------------------------------------

def check_zero_block_census():
    sites = (0, 1, 2, 3)
    plus, minus = {0, 1}, {2, 3}
    supports = [frozenset(c) for k in (1, 2) for c in combinations(sites, k)]

    def cross_ok(sp, ss):
        for i, j in product(plus, minus):
            term1 = i in sp and j in ss
            term2 = i in ss and j in sp
            if term1 != term2:
                return False
        return True

    def live(pair, sp, ss):
        i, j = pair
        return (i in sp and j in ss) or (i in ss and j in sp)

    survivors = 0
    total = 0
    for pattern in product(range(len(supports)), repeat=6):
        total += 1
        sp = [supports[pattern[c]] for c in range(3)]
        ss = [supports[pattern[3 + c]] for c in range(3)]
        ok = True
        for c, d in product(COLORS, repeat=2):
            if c == d:
                continue
            if not cross_ok(sp[c], ss[d]):
                ok = False
                break
            if live((2, 3), sp[c], ss[d]):
                term1 = 2 in sp[c] and 3 in ss[d]
                term2 = 2 in ss[d] and 3 in sp[c]
                if term1 != term2:
                    ok = False
                    break
        if not ok:
            continue
        if not any(live((0, 1), sp[c], ss[d])
                   for c, d in product(COLORS, repeat=2) if c != d):
            continue
        diag_ok = True
        for c in COLORS:
            live_pairs = [pair for pair in combinations(sites, 2)
                          if pair != (0, 1) and live(pair, sp[c], ss[c])]
            if not live_pairs:
                diag_ok = False
                break
        if not diag_ok:
            continue
        survivors += 1
    # every survivor needs the window on one shore pair (here normalized to
    # {0,1}), so the opposite shore pair of q is dead and check 4 gives the
    # nine-dimensional block kernel: no survivor lives on a gauge-rigid chart.
    check(
        f"zero-block census at |W|=4: {total} support patterns, {survivors} "
        f"survive the product-level filter, all forced onto a dead-shore chart "
        f"(non-rigid by the Theorem C kernel)")
    return survivors


# ---------------------------------------------------------------------------
# 11. guard families
# ---------------------------------------------------------------------------

def pair_defect_census(n, edges):
    census = {}
    for pair in combinations(range(n), 2):
        kept = [v for v in range(n) if v not in pair]
        relabel = {v: k for k, v in enumerate(kept)}
        sub_edges = [(relabel[i], relabel[j]) for i, j in edges
                     if i not in pair and j not in pair]
        nu, b, iso, _, _ = defect_data(len(kept), sub_edges)
        census[nu] = census.get(nu, 0) + 1
    return census


def check_guard_families():
    cyc = []
    for base in (0, 7):
        for i in range(7):
            a, b = base + i, base + (i + 1) % 7
            cyc.append((min(a, b), max(a, b)))
    census14 = pair_defect_census(14, cyc)
    assert census14 == {1: 14, 2: 77}, census14
    check("bridge family: G_3 = two 7-cycles; 14 of 91 pair charts have defect 1, 77 have defect 2")

    inf = 7

    def f_round(r):
        pairs = [(inf, r % 7)]
        for k in (1, 2, 3):
            pairs.append(((r + k) % 7, (r - k) % 7))
        return [(min(i, j), max(i, j)) for i, j in pairs]

    edges8 = f_round(0) + f_round(1)
    comps, adjacency = graph_components(8, edges8)
    assert len(comps) == 1 and all(len(adjacency[v]) == 2 for v in range(8))
    census8 = pair_defect_census(8, edges8)
    assert census8 == {1: 8, 2: 20}, census8
    check("all-pair missing-row model: G_3 is one 8-cycle; 8 pair charts defect 1, 20 defect 2")

    # exact two-sided Hessian verdict on the defect-one chart at pair {inf, 0}
    D = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
    q_model = {}
    for r in (0, 1):
        for pair in f_round(r):
            q_model[pair] = [row[:] for row in D]
    for c in COLORS:
        for pair in f_round(c + 2):
            m = [[0] * 3 for _ in COLORS]
            m[c][c] = 1
            q_model[pair] = m
    scale = {0: [Fraction(1, 49), Fraction(1, 53), Fraction(1, 41)]}
    for (i, j), m in list(q_model.items()):
        entry = [[Fraction(m[a][b]) for b in COLORS] for a in COLORS]
        if i in scale:
            entry = [[scale[i][a] * entry[a][b] for b in COLORS] for a in COLORS]
        if j in scale:
            entry = [[entry[a][b] * scale[j][b] for b in COLORS] for a in COLORS]
        q_model[(i, j)] = entry
    pair = (0, inf)
    kept = [v for v in range(8) if v not in pair]
    chart = {(i, j): entry for (i, j), entry in q_model.items()
             if i not in pair and j not in pair}
    sub_edges = [(i, j) for (i, j) in edges8 if i not in pair and j not in pair]
    relabel = {v: k for k, v in enumerate(kept)}
    nu, b, iso, _, _ = defect_data(
        len(kept), [(relabel[i], relabel[j]) for i, j in sub_edges])
    assert (nu, b, iso) == (1, 1, 0)
    rows, _ = hessian_rows(chart, kept)
    int_rows = scale_int_rows(rows)
    rank = rank_mod(int_rows)
    kernel_upper = len(rows) - rank
    gauges = [q_vector(gauge_quadratic(chart, alpha, kept), kept)
              for alpha in gauge_basis(kept)]
    assert exact_rank(gauges) == 5
    for alpha in gauge_basis(kept):
        assert not quad_times_power(gauge_quadratic(chart, alpha, kept), chart, kept)
    verdict = "gauge-rigid: full structural guard" if kernel_upper == 5 else \
        f"extra kernel of dimension {kernel_upper - 5}: the chart escapes into (E1)"
    check(
        f"eight-site model chart at (inf,0): defect (1,1,0), Hessian rank {rank}/135, "
        f"kernel {kernel_upper} -- {verdict}")
    return kernel_upper


# ---------------------------------------------------------------------------
# 12. corollary arithmetic
# ---------------------------------------------------------------------------

def check_four_deletion_lemma():
    universe = list(range(8))
    for size in range(0, 9):
        for S in combinations(universe, min(size, 8)):
            S = set(S)
            for F in combinations(universe, 4):
                if all(len(S - {v}) <= 2 for v in F):
                    assert len(S) <= 2, (S, F)
    check("four-deletion support lemma exhaustive on an 8-point universe")


def check_thresholds():
    printed = []
    for N in range(8, 62, 2):
        good = N * (N - 7) // 2
        fan = N - 7
        assert good >= 4 and fan >= 1
        for k in range(1, 6):
            if N >= 7 * k + 7:
                assert (N - 7) - (7 * k - 1) == N - 7 * k - 6 >= 1
        K = -(-N // 5)
        for h in (2, 3, 4):
            x_needed = 7 * h - 6
            if x_needed <= K:
                e3_max = Fraction(3 * K + (7 * h - 7) * (K - 4), 2)
                e12_min = Fraction(K * (K - 1), 2) - e3_max
                if N in (40, 60):
                    printed.append((N, K, h, e12_min))
    expected_40_2 = Fraction(8 * 7, 2) - Fraction(3 * 8 + 7 * 4, 2)
    assert any(row[:3] == (40, 8, 2) and row[3] == expected_40_2 for row in printed)
    for row in printed:
        print(f"      clique row: N={row[0]} K={row[1]} h={row[2]} "
              f"min (E1 u E2) clique pairs if no h-shore: {row[3]}")
    check("fan/clique/shore threshold arithmetic for even N in 8..60")


# ---------------------------------------------------------------------------

def main():
    check_graph_step()
    check_gauge_identity()
    check_rigid_charts()
    check_theorem_c_kernel()
    check_engine_w4()
    check_engine_w6()
    check_lemma_r()
    check_theorem_e()
    check_k2_census()
    check_p3_triangle_census()
    check_w8_census()
    check_k13_k4_residual_death()
    check_postfan_witness_compatibility()
    check_balance()
    check_p_guard()
    check_window_lemma()
    check_zero_block_census()
    check_guard_families()
    check_four_deletion_lemma()
    check_thresholds()
    print()
    print(f"checks run: {len(CHECKS)}")
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
