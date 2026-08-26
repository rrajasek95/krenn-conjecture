#!/usr/bin/env python3
"""Fast evaluator for E_w over ALL words, certified against a5_core's raw
definitional route (cap_error_raw) by exact agreement on samples.

E_w = sum_{k=2}^{h} s^{h-k} iota_k(z_{w,k}),
z_{w,k} = sum_{|J|=h-k} weight(J) * sum_{S subset free, |S|=k} (prod_S p) (x) (prod_T q).
"""
from __future__ import annotations
import sys
from itertools import combinations, permutations, product
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")
import a5_core as A
import numpy as np


def multisets(k):
    return tuple(tuple(sorted(m)) for m in combinations_with_repl(k))


def combinations_with_repl(k):
    from itertools import combinations_with_replacement
    return list(combinations_with_replacement(A.C3, k))


def iota_vec(k, mu, nu):
    """iota_k(e_mu (x) f_nu) = Perm_k([K_{mu_a nu_b}]) as a degree-k vector."""
    acc = {}
    for sigma in permutations(range(k)):
        e = [0] * 9
        for t in range(k):
            e[3 * mu[t] + nu[sigma[t]]] += 1
        key = tuple(e)
        acc[key] = acc.get(key, 0) + 1
    return A.poly_vec(acc, k)


def block_matrices(h, svec):
    """For each k: (list of (mu,nu), int64 matrix rows = s^{h-k} iota_k(mu,nu))."""
    sp = A.var_poly(svec)
    out = {}
    for k in range(2, h + 1):
        ms = combinations_with_repl(k)
        pairs = [(mu, nu) for mu in ms for nu in ms]
        spk = A.ppow(sp, h - k)
        rows = []
        for mu, nu in pairs:
            f = A.vec_poly(iota_vec(k, mu, nu), k)
            if h - k:
                f = A.pmul(f, spk)
            rows.append(A.poly_vec(f, h))
        out[k] = (pairs, np.array(rows, dtype=object))
    return out


def z_tables(source, h, word):
    """{k: dict[(mu,nu) -> int]} for one word."""
    p, q, U = A.sites(h)
    slot = {u: n for n, u in enumerate(U)}
    Pv = {a: [A.blk(source, p, a, i, word[slot[a]]) for i in A.C3] for a in U}
    Qv = {a: [A.blk(source, q, a, j, word[slot[a]]) for j in A.C3] for a in U}

    def subset_prods(vecs):
        prods = {frozenset(): {(): 1}}
        for size in range(1, len(U) + 1):
            for S in combinations(U, size):
                key = frozenset(S)
                a = S[-1]
                base = prods[frozenset(S[:-1])]
                new = {}
                for m, c in base.items():
                    for i in A.C3:
                        if vecs[a][i]:
                            mm = tuple(sorted(m + (i,)))
                            new[mm] = new.get(mm, 0) + c * vecs[a][i]
                prods[key] = {m: c for m, c in new.items() if c}
        return prods

    pp, qq = subset_prods(Pv), subset_prods(Qv)
    # Z_F for each even subset F: sum over half-subsets S of F
    out = {}
    for k in range(2, h + 1):
        acc = {}
        for J in A.partial_matchings(U, h - k):
            wt = 1
            for a, b in J:
                wt *= source[(a, b)][word[slot[a]]][word[slot[b]]]
                if wt == 0:
                    break
            if wt == 0:
                continue
            used = set()
            for a, b in J:
                used.update((a, b))
            free = tuple(u for u in U if u not in used)
            for S in combinations(free, k):
                T = tuple(u for u in free if u not in S)
                fp = pp[frozenset(S)]
                if not fp:
                    continue
                fq = qq[frozenset(T)]
                if not fq:
                    continue
                for mu, cp in fp.items():
                    for nu, cq in fq.items():
                        key = (mu, nu)
                        acc[key] = acc.get(key, 0) + wt * cp * cq
        out[k] = {kk: c for kk, c in acc.items() if c}
    return out


def error_vec_fast(source, h, word, bmats):
    dim = len(A.deg_monoms(h))
    vec = [0] * dim
    z = z_tables(source, h, word)
    for k in range(2, h + 1):
        pairs, mat = bmats[k]
        index = {pr: i for i, pr in enumerate(pairs)}
        for key, c in z[k].items():
            row = mat[index[key]]
            for t in range(dim):
                if row[t]:
                    vec[t] += c * int(row[t])
    return vec


def all_error_vectors(source, h, bmats=None):
    """Matrix (3^{2h} x dim) of E_w over all words, exact python ints."""
    if bmats is None:
        bmats = block_matrices(h, A.s_vector(source))
    words = A.all_words(h)
    dim = len(A.deg_monoms(h))
    zmats, index = {}, {}
    for k in range(2, h + 1):
        pairs, _ = bmats[k]
        index[k] = {pr: i for i, pr in enumerate(pairs)}
        zmats[k] = np.zeros((len(words), len(pairs)), dtype=object)
    for wi, w in enumerate(words):
        z = z_tables(source, h, w)
        for k in range(2, h + 1):
            row = zmats[k][wi]
            idx = index[k]
            for key, c in z[k].items():
                row[idx[key]] += c
    total = np.zeros((len(words), dim), dtype=np.int64)
    for k in range(2, h + 1):
        Z = zmats[k]
        B = bmats[k][1]
        mz = max((abs(int(x)) for x in Z.ravel()), default=0)
        mb = max((abs(int(x)) for x in B.ravel()), default=0)
        bound = mz * mb * Z.shape[1] * (h - 1)
        assert bound < 2 ** 62, ("int64 overflow risk", bound)
        total += Z.astype(np.int64).dot(B.astype(np.int64))
    return words, total
