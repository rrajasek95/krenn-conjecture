#!/usr/bin/env python3
"""Exact checks for the post-fan status of the induced-zero four-cut /
growing-shore identity (Priority 3 of the current audit).

Three independent exact checks, all over Z or Q (mod-p is used once, only
as an exact *lower* bound for a rational rank):

CHECK 1 (the surviving half).  The shore expansion -- equation (2)/(11) of
  notes/good-pair-fan-induced-zero-four-cut-reduction.md -- is CHART-FREE.
  At N=8, for shores of size h=2,3,4 with scattered labels (so both block
  storage orientations occur), and with a deliberately mixed internal
  chart (a zero block and a rank-one block planted inside D), the h-slot
  extraction of the full matching power a^[4] equals
      (prod_j p^{(j)}_{c_j}) q^{[m-h]}
  for all 3^h colour tuples.  No Hessian, gauge, or graph hypothesis is
  used anywhere in this check.  The matching-support count (12) of the
  four-cut note, (N-h)_h (N-2h-1)!!, is also verified.

CHECK 2 (the dead half).  The shore CONSTRUCTION needed the sparse-row
  bound, whose derivation lives on the regular NONBIPARTITE chart.  On a
  regular BIPARTITE chart it is not merely unproven but false as an
  inference: at the N=8 pair-chart size |W|=6 we construct an exact
  integer chart with
    - rank-three blocks exactly on K_{3,3} (connected, spanning,
      bipartite, balanced), rank-one blocks z_i z_j^T inside the shores,
    - gauge-rigid Hessian (two-sided certificate: exact integer
      annihilation + independence of the five vertex gauges, and mod-p
      rank 130 of the 135x729 Hessian as an exact lower bound),
  on which the FULL-SUPPORT rows p = z, s = z^sigma satisfy the mixed
  pair-contraction kernel equation
      a_cd q^{[3]} + p_c s_d q^{[2]} = 0   with a_cd = 0,
  because p s equals the bipartition gauge element Z^sigma.  By
  bilinearity p_c = t_c z, s_d = u_d z^sigma satisfies all six mixed
  cells at once.  Hence no support bound follows on the bipartite chart.

CHECK 3 (where the mechanism lives, exactly).  The graph step of the
  sparse-row theorem and of Theorem A of
  notes/good-pair-fan-six-port-simultaneous-exclusion.md is the affine
  system {alpha_i + alpha_j = gamma on E, sum alpha = 0}.  Its exact
  rational solution dimensions on seven 6-vertex graphs localize the
  failure to {some component bipartite (isolated vertices included)}:
    K_6 -> 0, C_5+pendant -> 0, two disjoint triangles -> 0 (the audit's
    sufficiency remark), K_{3,3} -> 1 with gamma == 0 forced (balanced:
    the a_cd = 0 half survives), K_{2,4} -> 1 with gamma free
    (unbalanced: even a_cd escapes), C_6 -> 1, triangle+edge+isolated
    -> 2.

Run from the repository root:

    uv run python computations/zero_shore_post_fan_status_check.py

Prints PASS lines and ALL CHECKS PASS; exits nonzero on any failure.
"""

import itertools
import random
import sys
from fractions import Fraction

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, ok))
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line, flush=True)
    if not ok:
        print("ABORT: check failed", flush=True)
        sys.exit(1)


# ----------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------

def perfect_matchings(sites):
    """All perfect matchings of the list `sites` as tuples of (i,j), i<j."""
    sites = sorted(sites)
    if not sites:
        return [()]
    first, rest = sites[0], sites[1:]
    out = []
    for k, partner in enumerate(rest):
        sub = rest[:k] + rest[k + 1:]
        for m in perfect_matchings(sub):
            out.append(((first, partner),) + m)
    return out


def k_matchings(sites, k):
    """All k-matchings (k disjoint edges) of the list `sites`."""
    out = []
    for subset in itertools.combinations(sorted(sites), 2 * k):
        out.extend(perfect_matchings(list(subset)))
    return out


def mat_rank_int(M):
    """Exact rank of an integer/Fraction matrix via rational elimination."""
    A = [[Fraction(x) for x in row] for row in M]
    rows = len(A)
    cols = len(A[0]) if rows else 0
    rank = 0
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        pivval = A[r][c]
        for i in range(r + 1, rows):
            if A[i][c] != 0:
                f = A[i][c] / pivval
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
        rank += 1
        if r == rows:
            break
    return rank


def mat_rank_modp(M, p):
    """Rank of an integer matrix modulo the prime p (lower bound for Q-rank)."""
    A = [[x % p for x in row] for row in M]
    rows = len(A)
    cols = len(A[0]) if rows else 0
    rank = 0
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i][c]:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(a * inv) % p for a in A[r]]
        rowr = A[r]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                Ai = A[i]
                A[i] = [(a - f * b) % p for a, b in zip(Ai, rowr)]
        r += 1
        rank += 1
        if r == rows:
            break
    return rank


def mat3_rank(B):
    return mat_rank_int(B)


def det3(B):
    return (B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1])
            - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0])
            + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0]))


# ----------------------------------------------------------------------
# CHECK 1: chart-free shore expansion at N=8, h = 2,3,4
# ----------------------------------------------------------------------

def run_check1():
    N, m = 8, 4
    rng = random.Random(20260728)
    all_sites = list(range(N))
    matchings = perfect_matchings(all_sites)
    assert len(matchings) == 105

    for h in (2, 3, 4):
        shore = [1, 4, 6, 3][:h]           # scattered: both orientations occur
        D = [x for x in all_sites if x not in shore]

        # random asymmetric integer blocks, stored under (i<j): row = colour
        # at i, column = colour at j
        A = {}
        for i in range(N):
            for j in range(i + 1, N):
                A[(i, j)] = [[rng.randint(-9, 9) for _ in range(3)]
                             for _ in range(3)]
        # induced-zero shore
        for i in shore:
            for j in shore:
                if i < j:
                    A[(i, j)] = [[0] * 3 for _ in range(3)]
        # mixed internal chart inside D: one zero block, one rank-one block
        d0, d1, d2, d3 = D[0], D[1], D[2], D[3]
        key = (min(d0, d1), max(d0, d1))
        A[key] = [[0] * 3 for _ in range(3)]
        u = [rng.randint(1, 5) for _ in range(3)]
        v = [rng.randint(1, 5) for _ in range(3)]
        key = (min(d2, d3), max(d2, d3))
        A[key] = [[u[a] * v[b] for b in range(3)] for a in range(3)]

        # full matching power a^[m]: tensor over {0,1,2}^N
        T = {}
        n_support = 0
        for M in matchings:
            if any(i in shore and j in shore for (i, j) in M):
                continue  # literally zero on the shore blocks
            n_support += 1
            for combo in itertools.product(range(3), repeat=len(M)):
                # combo[k] will be split into two colours below
                pass
            # accumulate: iterate over 9 colour choices per edge
            for colour_choices in itertools.product(
                    itertools.product(range(3), repeat=2), repeat=len(M)):
                coeff = 1
                key = [0] * N
                for (edge, (ci, cj)) in zip(M, colour_choices):
                    i, j = edge
                    coeff *= A[(i, j)][ci][cj]
                    if coeff == 0:
                        break
                    key[i] = ci
                    key[j] = cj
                if coeff == 0:
                    continue
                k = tuple(key)
                T[k] = T.get(k, 0) + coeff

        # count formula (12): (N-h)_h (N-2h-1)!!
        falling = 1
        for t in range(h):
            falling *= (N - h - t)
        dfac = 1
        x = N - 2 * h - 1
        while x > 1:
            dfac *= x
            x -= 2
        check(f"h={h}: contributing matching supports = (N-h)_h (N-2h-1)!!",
              n_support == falling * dfac,
              f"{n_support} == {falling * dfac}")

        # endpoint-oriented rows p^{(j)}_c : linear forms on D
        def row(named, colour):
            comp = {}
            for x in D:
                if named < x:
                    vec = A[(named, x)][colour]          # row of the block
                else:
                    vec = [A[(x, named)][a][colour] for a in range(3)]  # column
                comp[x] = vec
            return comp

        # D-site square-zero algebra: dict {sorted ((site,colour),...): coeff}
        def alg_mul(e1, e2):
            out = {}
            for k1, c1 in e1.items():
                s1 = {sc[0] for sc in k1}
                for k2, c2 in e2.items():
                    if any(sc[0] in s1 for sc in k2):
                        continue
                    k = tuple(sorted(k1 + k2))
                    out[k] = out.get(k, 0) + c1 * c2
            return {k: v for k, v in out.items() if v != 0}

        def lin_elem(comp):
            return {((x, c),): comp[x][c]
                    for x in comp for c in range(3) if comp[x][c] != 0}

        # q^{[m-h]} on D: sum over (m-h)-matchings of D
        qpow = {}
        for Mk in k_matchings(D, m - h):
            for colour_choices in itertools.product(
                    itertools.product(range(3), repeat=2), repeat=len(Mk)):
                coeff = 1
                kk = []
                for (edge, (ci, cj)) in zip(Mk, colour_choices):
                    i, j = edge
                    coeff *= A[(i, j)][ci][cj]
                    if coeff == 0:
                        break
                    kk.append((i, ci))
                    kk.append((j, cj))
                if coeff == 0:
                    continue
                k = tuple(sorted(kk))
                qpow[k] = qpow.get(k, 0) + coeff
        if m - h == 0:
            qpow = {(): 1}

        ok_all = True
        for cs in itertools.product(range(3), repeat=h):
            rhs = {(): 1}
            for jidx, j in enumerate(shore):
                rhs = alg_mul(rhs, lin_elem(row(j, cs[jidx])))
            rhs = alg_mul(rhs, qpow)
            # compare with slot extraction of T
            for dcols in itertools.product(range(3), repeat=len(D)):
                key = [0] * N
                for jidx, j in enumerate(shore):
                    key[j] = cs[jidx]
                for xidx, x in enumerate(D):
                    key[x] = dcols[xidx]
                lhs_val = T.get(tuple(key), 0)
                rkey = tuple(sorted((x, dcols[xidx])
                             for xidx, x in enumerate(D)))
                rhs_val = rhs.get(rkey, 0)
                if lhs_val != rhs_val:
                    ok_all = False
                    break
            if not ok_all:
                break
        check(f"h={h}: shore expansion (2)/(11) chart-free, all 3^{h} slots",
              ok_all,
              f"shore={shore}, mixed internal chart, no Hessian input")


# ----------------------------------------------------------------------
# CHECK 2: full-support witness on a gauge-rigid bipartite chart, |W| = 6
# ----------------------------------------------------------------------

def top3(mark2form, q0, W):
    """Exact top-degree product (2-form) * q0^{[2]} on 6 sites.

    mark2form and q0: dict (i,j)->3x3 int matrix (i<j).
    Returns dict colour-tuple -> int (3^6 entries implicit)."""
    out = {}
    for M in perfect_matchings(W):
        for markpos in range(3):
            blocks = []
            okay = True
            for t, e in enumerate(M):
                src = mark2form if t == markpos else q0
                if e not in src:
                    okay = False
                    break
                blocks.append((e, src[e]))
            if not okay:
                continue
            for colour_choices in itertools.product(
                    itertools.product(range(3), repeat=2), repeat=3):
                coeff = 1
                key = [0] * 6
                for ((edge, B), (ci, cj)) in zip(blocks, colour_choices):
                    i, j = edge
                    coeff *= B[ci][cj]
                    if coeff == 0:
                        break
                    key[i] = ci
                    key[j] = cj
                if coeff == 0:
                    continue
                k = tuple(key)
                out[k] = out.get(k, 0) + coeff
    return {k: v for k, v in out.items() if v != 0}


def top_q3(q0, W):
    """q0^{[3]}: sum over perfect matchings, colour-decorated."""
    out = {}
    for M in perfect_matchings(W):
        if any(e not in q0 for e in M):
            continue
        for colour_choices in itertools.product(
                itertools.product(range(3), repeat=2), repeat=3):
            coeff = 1
            key = [0] * 6
            for (edge, (ci, cj)) in zip(M, colour_choices):
                i, j = edge
                coeff *= q0[edge][ci][cj]
                if coeff == 0:
                    break
                key[i] = ci
                key[j] = cj
            if coeff == 0:
                continue
            k = tuple(key)
            out[k] = out.get(k, 0) + coeff
    return {k: v for k, v in out.items() if v != 0}


def run_check2():
    W = list(range(6))
    P, Qsh = [0, 1, 2], [3, 4, 5]
    sigma = {0: 1, 1: 1, 2: 1, 3: -1, 4: -1, 5: -1}
    prime = 1000003

    found = None
    for seed in range(1, 26):
        rng = random.Random(700 + seed)
        z = {i: [rng.randint(1, 7) for _ in range(3)] for i in W}
        q0 = {}
        ok = True
        for i in range(6):
            for j in range(i + 1, 6):
                same = (i in P) == (j in P)
                if same:
                    q0[(i, j)] = [[z[i][a] * z[j][b] for b in range(3)]
                                  for a in range(3)]
                else:
                    B = [[rng.randint(-9, 9) for _ in range(3)]
                         for _ in range(3)]
                    if det3(B) == 0:
                        ok = False
                    q0[(i, j)] = B
        if not ok:
            continue
        # Hessian 135 x 729 and mod-p rank
        basis = []
        Hrows = []
        idx_of = {c: n for n, c in enumerate(
            itertools.product(range(3), repeat=6))}
        for i in range(6):
            for j in range(i + 1, 6):
                for a in range(3):
                    for b in range(3):
                        Z = {(i, j): [[1 if (r == a and c == b) else 0
                                       for c in range(3)] for r in range(3)]}
                        vec = [0] * 729
                        for k, v in top3(Z, q0, W).items():
                            vec[idx_of[k]] = v
                        basis.append(((i, j), (a, b)))
                        Hrows.append(vec)
        rank_p = mat_rank_modp(Hrows, prime)
        if rank_p == 130:
            found = (seed, z, q0, Hrows, basis, idx_of)
            break
    check("bipartite chart: gauge-rigid seed found (mod-p rank 130/135)",
          found is not None,
          f"seed={found[0] if found else None}, prime={prime}")
    seed, z, q0, Hrows, basis, idx_of = found

    # G_3 is exactly K_{3,3}
    g3_ok = True
    for i in range(6):
        for j in range(i + 1, 6):
            same = (i in P) == (j in P)
            r = mat3_rank(q0[(i, j)])
            if same and r != 1:
                g3_ok = False
            if (not same) and r != 3:
                g3_ok = False
    check("bipartite chart: G_3(q0) == K_{3,3} (cross rank 3, shore rank 1)",
          g3_ok)

    # five vertex gauges: exact integer annihilation + exact independence
    gauge_rows = []
    ann_ok = True
    for k in range(5):
        alpha = {i: 0 for i in W}
        alpha[k] = 1
        alpha[5] = -1
        Zg = {}
        for (i, j), B in q0.items():
            f = alpha[i] + alpha[j]
            Zg[(i, j)] = [[f * B[a][b] for b in range(3)] for a in range(3)]
        if any(v != 0 for v in top3(Zg, q0, W).values()):
            ann_ok = False
        vec = [0] * 135
        for n, ((i, j), (a, b)) in enumerate(basis):
            vec[n] = (alpha[i] + alpha[j]) * q0[(i, j)][a][b]
        gauge_rows.append(vec)
    check("bipartite chart: five vertex gauges exactly annihilated over Z",
          ann_ok)
    check("bipartite chart: gauge vectors independent (exact rank 5)",
          mat_rank_int(gauge_rows) == 5)
    # two-sided conclusion: mod-p rank 130 <= Q-rank, gauge gives kernel >= 5,
    # 135 - 130 = 5, hence kernel over Q is exactly the gauge space.
    check("bipartite chart: kernel over Q is exactly the vertex-gauge space",
          True, "rank_Q >= 130 (mod-p) and dim gauge = 5 = 135 - 130")

    check("bipartite chart: q0^{[3]} != 0",
          any(v != 0 for v in top_q3(q0, W).values()))

    # the full-support witness: p = z (support 6), s = z^sigma (support 6)
    p_vec = {i: z[i] for i in W}
    s_vec = {i: [sigma[i] * c for c in z[i]] for i in W}
    check("witness rows: |supp(p)| = |supp(s)| = 6 (full, not <= 2)",
          all(any(c != 0 for c in p_vec[i]) for i in W)
          and all(any(c != 0 for c in s_vec[i]) for i in W))

    # blockwise p*s == Z^sigma (the bipartition gauge element)
    ps = {}
    for i in range(6):
        for j in range(i + 1, 6):
            ps[(i, j)] = [[p_vec[i][a] * s_vec[j][b] + s_vec[i][a] * p_vec[j][b]
                           for b in range(3)] for a in range(3)]
    zsigma_ok = True
    for (i, j), B in ps.items():
        f = sigma[i] + sigma[j]
        Bs = [[f * q0[(i, j)][a][b] for b in range(3)] for a in range(3)]
        if B != Bs:
            zsigma_ok = False
    check("witness: p s == Z^sigma blockwise (bipartition gauge element)",
          zsigma_ok)

    # the mixed kernel equation with a_cd = 0: (p s) q0^{[2]} == 0 exactly
    check("witness: a q^{[3]} + (p s) q^{[2]} = 0 with a = 0, full support",
          all(v == 0 for v in top3(ps, q0, W).values()),
          "all 729 top coefficients vanish exactly over Z")
    # bilinearity: p_c = t_c z, s_d = u_d z^sigma satisfies all six mixed
    # cells (c != d) at once, with every row of full support 6.
    check("witness: all six mixed cells satisfied by p_c = t_c z, "
          "s_d = u_d z^sigma (bilinearity)", True,
          "p_c s_d q^{[2]} = t_c u_d (p s) q^{[2]} = 0")


# ----------------------------------------------------------------------
# CHECK 3: the affine graph step, exact solution dimensions
# ----------------------------------------------------------------------

def affine_gauge_solutions(nverts, edges):
    """Exact nullspace basis of {alpha_i+alpha_j = gamma on E, sum alpha = 0}
    in variables (alpha_0..alpha_{n-1}, gamma).  Returns (dim, basis)."""
    rows = []
    for (i, j) in edges:
        r = [Fraction(0)] * (nverts + 1)
        r[i] = Fraction(1)
        r[j] = Fraction(1)
        r[nverts] = Fraction(-1)
        rows.append(r)
    r = [Fraction(1)] * nverts + [Fraction(0)]
    rows.append(r)
    ncols = nverts + 1
    # row echelon
    A = [row[:] for row in rows]
    pivots = []
    rr = 0
    for c in range(ncols):
        piv = None
        for i in range(rr, len(A)):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[rr], A[piv] = A[piv], A[rr]
        pv = A[rr][c]
        A[rr] = [x / pv for x in A[rr]]
        for i in range(len(A)):
            if i != rr and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[rr])]
        pivots.append(c)
        rr += 1
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        vec = [Fraction(0)] * ncols
        vec[fc] = Fraction(1)
        for prow, pcol in zip(range(len(pivots)), pivots):
            vec[pcol] = -A[prow][fc]
        basis.append(vec)
    return len(free), basis


def run_check3():
    n = 6
    K6 = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    K33 = [(i, j) for i in [0, 1, 2] for j in [3, 4, 5]]
    K24 = [(i, j) for i in [0, 1] for j in [2, 3, 4, 5]]
    C6 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)]
    two_triangles = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
    c5_pendant = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4), (0, 5)]
    tri_edge_iso = [(0, 1), (1, 2), (0, 2), (3, 4)]

    cases = [
        ("K_6 (connected spanning nonbipartite)", K6, 0, None),
        ("C_5 + pendant (connected spanning nonbipartite)", c5_pendant, 0,
         None),
        ("two disjoint triangles (spanning, every component odd)",
         two_triangles, 0, None),
        ("K_{3,3} (connected spanning bipartite, balanced)", K33, 1,
         "gamma0"),
        ("K_{2,4} (connected spanning bipartite, unbalanced)", K24, 1,
         "gammafree"),
        ("C_6 (connected spanning bipartite, balanced)", C6, 1, "gamma0"),
        ("triangle + edge + isolated vertex (nonspanning)", tri_edge_iso, 2,
         None),
    ]
    for name, edges, want_dim, gamma_flag in cases:
        dim, basis = affine_gauge_solutions(n, edges)
        check(f"graph step on {name}: solution dim = {want_dim}",
              dim == want_dim)
        if gamma_flag == "gamma0":
            check(f"graph step on {name}: gamma = 0 on every solution "
                  "(balanced: a_cd = 0 survives)",
                  all(b[n] == 0 for b in basis))
        elif gamma_flag == "gammafree":
            check(f"graph step on {name}: some solution has gamma != 0 "
                  "(unbalanced: even a_cd escapes)",
                  any(b[n] != 0 for b in basis))


def main():
    print("== CHECK 1: chart-free shore expansion at N=8 (h=2,3,4) ==")
    run_check1()
    print("== CHECK 2: full-support witness on a gauge-rigid bipartite "
          "chart (|W|=6) ==")
    run_check2()
    print("== CHECK 3: the affine graph step, exact dimensions ==")
    run_check3()
    print(f"checks run: {len(CHECKS)}")
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
