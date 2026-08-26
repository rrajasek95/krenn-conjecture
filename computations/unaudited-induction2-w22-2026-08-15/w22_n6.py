#!/usr/bin/env python3
"""W22 -- N = 6 (h = 2) test bed: exact mixed-exact sources by PURE STRATUM,
plus the exact blocking decision for general caps and for rank-one caps.

PURE STRATUM P_k = mixed-exact sources with exactly k nonzero pure
coefficients.  At N = 6, P_3 is EMPTY (six-site theorem + W10-G).  This file
builds exact representatives of P_0, P_1, P_2 and the machinery to decide
blocking at every pair.

All arithmetic exact.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-induction2-w22-2026-08-15")
import w22_core as W                                        # noqa: E402


# ------------------------------------------------------------------ builders

def zero_source(n):
    return {(a, b): [[0] * 3 for _ in range(3)] for a, b in combinations(range(n), 2)}


def constant_block_source(t, n):
    """A_uv = t_uv * J (all-ones).  H_w = haf(t) for EVERY word (W10)."""
    src = zero_source(n)
    for e in src:
        src[e] = [[t[e]] * 3 for _ in range(3)]
    return src


def diag_gauge(src, g, n):
    """A_uv(i,j) -> g_u[i] g_v[j] A_uv(i,j): the pure-rescaling gauge.
    Mixed-exactness is preserved; pure c is multiplied by prod_u g_u[c]."""
    out = {}
    for (a, b), m in src.items():
        out[(a, b)] = [[g[a][i] * g[b][j] * m[i][j] for j in range(3)]
                       for i in range(3)]
    return out


def diagonal_colour_source(tables, n):
    """A_uv = diag(tables[0][uv], tables[1][uv], tables[2][uv]).
    H_w = prod_c haf(tables[c] | w^{-1}(c))."""
    src = zero_source(n)
    for a, b in combinations(range(n), 2):
        for c in range(3):
            src[(a, b)][c][c] = tables[c].get((a, b), 0)
    return src


def indicator(edges, n, val=1):
    return {W.ekey(*e): val for e in edges}


def delta_n2_cycle(n, cycle=None):
    """Delta_{N,2} (2 colours) by the alternating-Hamiltonian-cycle
    construction: colour 0 on the even edges of the cycle, colour 1 on the odd
    ones.  Returns (M0, M1) as edge sets."""
    if cycle is None:
        cycle = list(range(n))
    edges = [(cycle[i], cycle[(i + 1) % n]) for i in range(n)]
    M0 = [edges[i] for i in range(0, n, 2)]
    M1 = [edges[i] for i in range(1, n, 2)]
    return M0, M1


def source_P2(n=6, cycle=None):
    """Delta_{N,2} padded to three colours: pures (1, 1, 0)."""
    M0, M1 = delta_n2_cycle(n, cycle)
    return diagonal_colour_source([indicator(M0, n), indicator(M1, n), {}], n)


def source_P1(n=6, cycle=None):
    """Pures (1, 0, 0): colour 0 on a perfect matching; colour 1 on the
    complementary matching with ONE edge deleted (so haf = 0 but the cross
    conditions still hold); colour 2 absent."""
    M0, M1 = delta_n2_cycle(n, cycle)
    return diagonal_colour_source(
        [indicator(M0, n), indicator(M1[:-1], n), {}], n)


def source_P0_constant(t, n=6):
    return constant_block_source(t, n)


# ------------------------------------------------------------- pure stratum

def pure_profile(src, n):
    pu = W.pures(src, n)
    return tuple(1 if pu[c] != 0 else 0 for c in range(3)), pu


def is_mixed_exact(src, n):
    return len(W.mixed_defects(src, n)) == 0


# ------------------------------------------------------- symbolic cap error

def sym_cap_quadrics(src, p, q, sites):
    """h = 2 only.  Returns (list of sympy polys E_w(K), s(K), kappas) in the
    nine cap variables k00..k22."""
    import sympy
    sites = tuple(sorted(sites))
    assert len(sites) == 4
    K = [[sympy.Symbol(f"k{i}{j}") for j in range(3)] for i in range(3)]
    apq = W.oriented(src, p, q)
    s = sympy.expand(sum(K[i][j] * apq[i][j] for i in range(3) for j in range(3)))
    R = {}
    for a, b in combinations(sites, 2):
        apa, aqa = W.oriented(src, p, a), W.oriented(src, q, a)
        apb, aqb = W.oriented(src, p, b), W.oriented(src, q, b)
        mat = [[sympy.expand(sum(K[i][j] * (apa[i][ca] * aqb[j][cb]
                                            + aqa[j][ca] * apb[i][cb])
                                 for i in range(3) for j in range(3)))
                for cb in range(3)] for ca in range(3)]
        R[(a, b)] = mat
    slot = {a: i for i, a in enumerate(sites)}
    eqs = []
    for word in product(range(3), repeat=4):
        tot = sympy.Integer(0)
        for M in W.perfect_matchings(sites):
            (a1, b1), (a2, b2) = M
            tot += (R[W.ekey(a1, b1)][word[slot[min(a1, b1)]]][word[slot[max(a1, b1)]]]
                    * R[W.ekey(a2, b2)][word[slot[min(a2, b2)]]][word[slot[max(a2, b2)]]])
        tot = sympy.expand(tot)
        if tot != 0:
            eqs.append(tot)
    return eqs, s, [K[c][c] for c in range(3)]


def sing_poly(expr):
    import sympy
    return str(sympy.expand(expr)).replace("**", "^").replace(" ", "")


KVARS = tuple(f"k{i}{j}" for i in range(3) for j in range(3))


def decide_pair_general(src, p, q, sites, tag, timeout=900):
    """EXACT decision: does an ADMISSIBLE general cap with E_pq(K) = 0 exist?
    Rabinowitsch on s * kappa_0 * kappa_1 * kappa_2.  Returns
    'WITNESS' / 'BLOCKED'."""
    eqs, s, kap = sym_cap_quadrics(src, p, q, sites)
    gens = [sing_poly(e) for e in eqs]
    nz = "(" + sing_poly(s) + ")*(" + ")*(".join(sing_poly(k) for k in kap) + ")"
    lines = [f'ring RR=0,({",".join(KVARS)},zzt),dp;',
             "ideal zzI=" + (",".join(gens) if gens else "0") + ";",
             f"ideal zzJ=zzI,zzt*({nz})-1;",
             f'"DEC {tag} "+string(dim(std(zzJ)));']
    script = "\n".join(lines)
    W.no_shadow_guard(script, set(KVARS) | {"zzt"})
    out = W.run_singular(script, timeout=timeout)
    line = [ln for ln in out.splitlines() if ln.startswith(f"DEC {tag} ")]
    assert line, out
    d = int(line[0].split()[-1])
    return ("BLOCKED" if d == -1 else "WITNESS"), d


def decide_pair_rank1(src, p, q, sites, tag, timeout=900):
    """EXACT decision for RANK-ONE caps K = u (x) v."""
    import sympy
    u = sympy.symbols("zu0 zu1 zu2")
    v = sympy.symbols("zv0 zv1 zv2")
    Kuv = [[u[i] * v[j] for j in range(3)] for i in range(3)]
    sites = tuple(sorted(sites))
    apq = W.oriented(src, p, q)
    s = sympy.expand(sum(Kuv[i][j] * apq[i][j] for i in range(3) for j in range(3)))
    alpha, beta = {}, {}
    for a in sites:
        apa, aqa = W.oriented(src, p, a), W.oriented(src, q, a)
        alpha[a] = [sympy.expand(sum(u[i] * apa[i][c] for i in range(3)))
                    for c in range(3)]
        beta[a] = [sympy.expand(sum(v[j] * aqa[j][c] for j in range(3)))
                   for c in range(3)]
    slot = {a: i for i, a in enumerate(sites)}

    def Rent(a, b, ca, cb):
        return alpha[a][ca] * beta[b][cb] + beta[a][ca] * alpha[b][cb]

    eqs = []
    for word in product(range(3), repeat=4):
        tot = sympy.Integer(0)
        for M in W.perfect_matchings(sites):
            (a1, b1), (a2, b2) = M
            tot += (Rent(a1, b1, word[slot[a1]], word[slot[b1]])
                    * Rent(a2, b2, word[slot[a2]], word[slot[b2]]))
        tot = sympy.expand(tot)
        if tot != 0:
            eqs.append(tot)
    gens = [sing_poly(e) for e in eqs]
    uv = tuple(str(x) for x in u + v)
    nz = "(" + sing_poly(s) + ")*zu0*zu1*zu2*zv0*zv1*zv2"
    lines = [f'ring RR=0,({",".join(uv)},zzt),dp;',
             "ideal zzI=" + (",".join(gens) if gens else "0") + ";",
             f"ideal zzJ=zzI,zzt*({nz})-1;",
             f'"DEC {tag} "+string(dim(std(zzJ)));']
    script = "\n".join(lines)
    W.no_shadow_guard(script, set(uv) | {"zzt"})
    out = W.run_singular(script, timeout=timeout)
    line = [ln for ln in out.splitlines() if ln.startswith(f"DEC {tag} ")]
    assert line, out
    d = int(line[0].split()[-1])
    return ("BLOCKED" if d == -1 else "WITNESS"), d


def live(src, p, q):
    """An admissible cap EXISTS (before any cleanliness demand) iff A_pq != 0:
    kappa_c = K_cc are free, and s = <K, A_pq> can be made nonzero."""
    return any(x != 0 for row in W.oriented(src, p, q) for x in row)


def live_diagonal(src, p, q):
    """The stronger liveness used for diagonal caps: some A_pq(c,c) != 0."""
    m = W.oriented(src, p, q)
    return any(m[c][c] != 0 for c in range(3))
