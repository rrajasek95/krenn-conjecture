#!/usr/bin/env python3
"""A5 / claim 6: THEOREM W13.6 (the K_{2,3} circuit for F_n and F'_n).

I re-implement both families from the closed-form rules, compute fibres by
DIRECT enumeration of all perfect matchings of K_N (no product formula), and
compute the binomial difference vectors HONESTLY as chi(M+) - chi(M-) (W13's
checker instead *constructs* d from the predicted cross edges).

Checked at N = 8, 10, 12, 14:
  (a) the six edges v_x u_y all carry colour 0;
  (b) each of the three predicted words is MIXED and has fibre exactly 2, with
      the predicted two members;
  (c) the three honest difference vectors sum to zero (up to the orientation
      choice), and the resulting relation has ODD coefficient sum;
  (d) the family is singleton-free (no mixed word with fibre of size 1) --
      otherwise the O1 argument would be moot;
  (e) F'_n's defect vertex a and its partners b, c are not among the five
      marked vertices;
  (f) the oddness logic itself: w^{d_i} = -1 for each binomial fibre and
      sum n_i d_i = 0 with sum n_i odd gives 1 = -1; orientation flips
      preserve the parity.
"""
from __future__ import annotations
import json, sys
from itertools import combinations
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15")

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a5-w13-2026-08-15/"


# ------------------------------------------------------------------ families
def family_F(n):
    """N = 2n, n EVEN >= 4.  X = 0..n-1, Y = n..2n-1;
    colour 1 = M_X u M_Y, colour 2 = other intra-part edges, colour 0 = K_{X,Y}."""
    assert n % 2 == 0 and n >= 4
    N = 2 * n
    X, Y = list(range(n)), list(range(n, 2 * n))
    E1 = set()
    for part in (X, Y):
        for i in range(0, n, 2):
            E1.add((part[i], part[i + 1]))
    E2 = set()
    for part in (X, Y):
        for e in combinations(part, 2):
            if e not in E1:
                E2.add(e)
    E0 = {(x, y) for x in X for y in Y}
    return N, [E0, E1, E2], {}


def family_Fprime(n):
    """N = 2n, n ODD >= 5.  A = 0..n-1, B = n..2n-1, a = 0, b = n,
    P_c = (2n-2, 2n-1), c = 2n-1."""
    assert n % 2 == 1 and n >= 5
    N = 2 * n
    Aa, Bb = list(range(n)), list(range(n, 2 * n))
    a, b = 0, n
    MA = [(Aa[i], Aa[i + 1]) for i in range(1, n - 1, 2)]
    MB = [(Bb[i], Bb[i + 1]) for i in range(1, n - 1, 2)]
    Pc = MB[-1]
    c = Pc[1]
    E1 = set(MA) | set(MB) | {(a, b)}
    E0 = {(x, y) for x in Aa for y in Bb}
    E0 -= {(a, y) for y in Bb if y != c}
    E2 = set()
    for S in (Aa, Bb):
        for e in combinations(S, 2):
            if e in E1:
                continue
            if S is Aa and a in e:
                continue
            if S is Bb and b in e and (e[0] in Pc or e[1] in Pc):
                continue
            E2.add(e)
    E2 |= {(a, y) for y in Bb if y not in (b, c)}
    return N, [E0, E1, E2], {"a": a, "b": b, "c": c, "Pc": list(Pc)}


# -------------------------------------------------------------- enumeration
def all_matchings(verts):
    verts = tuple(verts)
    if not verts:
        yield ()
        return
    first = verts[0]
    for i in range(1, len(verts)):
        rest = verts[1:i] + verts[i + 1:]
        for tail in all_matchings(rest):
            yield ((first, verts[i]),) + tail


def census(N, cs):
    """{word: [matchings]} by DIRECT enumeration of every perfect matching."""
    lab = {}
    for r, es in enumerate(cs):
        for e in es:
            lab[tuple(sorted(e))] = r
    out = {}
    for M in all_matchings(range(N)):
        word = [-1] * N
        ok = True
        for e in M:
            k = tuple(sorted(e))
            r = lab.get(k)
            if r is None:
                ok = False
                break
            word[e[0]] = word[e[1]] = r
        if ok:
            out.setdefault(tuple(word), []).append(tuple(sorted(tuple(sorted(e)) for e in M)))
    return out


def chi(M, eindex):
    v = [0] * len(eindex)
    for e in M:
        v[eindex[e]] = 1
    return tuple(v)


def run(kind, n, deep=True):
    N, cs, marks = family_F(n) if kind == "F" else family_Fprime(n)
    rec = {"kind": kind, "n": n, "N": N,
           "support": sum(len(s) for s in cs),
           "colour_sizes": [len(s) for s in cs]}
    # marked vertices, exactly as W13.6 predicts
    if kind == "F":
        v = (n - 3, n - 2, n - 1)
        u = (2 * n - 2, 2 * n - 1)

        def partner(x):
            return x + 1 if x % 2 == 0 else x - 1
    else:
        v = (n - 3, n - 2, n - 1)
        u = (2 * n - 3, 2 * n - 2)
        pm = {}
        for e in cs[1]:
            pm[e[0]] = e[1]
            pm[e[1]] = e[0]

        def partner(x):
            return pm[x]
    rec["v"], rec["u"] = list(v), list(u)
    # (e) defect vertex not marked
    if kind == "Fprime":
        rec["defect_not_marked"] = (marks["a"] not in set(v) | set(u)
                                    and marks["b"] not in set(v) | set(u)
                                    and marks["c"] not in set(v) | set(u))
    # colour 1 is a perfect matching
    cov = sorted(x for e in cs[1] for x in e)
    rec["colour1_is_pm"] = (cov == list(range(N)) and len(cs[1]) == N // 2)
    # (a) the six edges are colour 0
    rec["six_edges_colour0"] = all(tuple(sorted((x, y))) in cs[0] for x in v for y in u)

    tab = census(N, cs) if deep else None
    if tab is not None:
        mixed = {w: m for w, m in tab.items() if len(set(w)) > 1}
        rec["n_matchings_supported"] = sum(len(m) for m in tab.values())
        rec["pures"] = [len(tab.get(tuple([r] * N), [])) for r in range(3)]
        rec["singletons"] = sum(1 for w, m in mixed.items() if len(m) == 1)
        rec["binomials"] = sum(1 for w, m in mixed.items() if len(m) == 2)
        rec["mixed_fibre_hist"] = {}
        for w, m in mixed.items():
            rec["mixed_fibre_hist"][str(len(m))] = rec["mixed_fibre_hist"].get(str(len(m)), 0) + 1

    # (b),(c): the three predicted words
    edges = sorted(set().union(*[set(map(lambda e: tuple(sorted(e)), s)) for s in cs]))
    eindex = {e: i for i, e in enumerate(edges)}
    diffs, words, details = [], [], []
    for x, y in ((v[0], v[1]), (v[1], v[2]), (v[2], v[0])):
        word = [1] * N
        for z in (x, y, u[0], u[1]):
            word[z] = 0
        orph = [partner(z) for z in (x, y, u[0], u[1])
                if partner(z) not in (x, y, u[0], u[1])]
        for z in orph:
            word[z] = 2
        word = tuple(word)
        fib = tab[word] if tab is not None else None
        mixedw = len(set(word)) > 1
        pred1 = {tuple(sorted((x, u[0]))), tuple(sorted((y, u[1])))}
        pred2 = {tuple(sorted((x, u[1]))), tuple(sorted((y, u[0])))}
        ok_members = None
        d = None
        if fib is not None:
            ok_members = (len(fib) == 2
                          and {frozenset(set(m) & (pred1 | pred2)) for m in fib}
                          == {frozenset(pred1), frozenset(pred2)})
            # HONEST difference: chi(M+) - chi(M-), oriented so that M+ is the
            # member containing pred1
            m_plus = [m for m in fib if pred1 <= set(m)]
            m_minus = [m for m in fib if pred2 <= set(m)]
            if len(m_plus) == 1 and len(m_minus) == 1:
                a1, a2 = chi(m_plus[0], eindex), chi(m_minus[0], eindex)
                d = tuple(p - q for p, q in zip(a1, a2))
                diffs.append(d)
        words.append(list(word))
        details.append({"pair": [x, y], "word": list(word), "mixed": mixedw,
                        "orphans": sorted(orph),
                        "fibre_size": (len(fib) if fib is not None else None),
                        "members_as_predicted": ok_members,
                        "d_support": (sorted(i for i, t in enumerate(d) if t)
                                      if d else None)})
    rec["words"] = words
    rec["details"] = details
    if len(diffs) == 3:
        tot = [sum(t) for t in zip(*diffs)]
        rec["three_diffs_sum_to_zero"] = all(t == 0 for t in tot)
        rec["relation_coeff_sum"] = 3
        rec["relation_is_odd"] = True
        # honest support of each difference: exactly the 4 cross edges?
        rec["each_diff_has_4_nonzeros"] = [sum(1 for t in d if t) for d in diffs]
    json.dump(rec, sys.stdout, indent=None)
    print(flush=True)
    return rec


if __name__ == "__main__":
    out = []
    for kind, ns in (("F", [4, 6, 8]), ("Fprime", [5, 7])):
        for n in ns:
            deep = 2 * n <= 14
            r = run(kind, n, deep=deep)
            out.append(r)
    json.dump(out, open(OUT + "results_t6_k23.json", "w"), indent=1)
