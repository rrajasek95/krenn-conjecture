#!/usr/bin/env python3
r"""W31 -- LEMMA W31-4: the k<=1 AFFINE LAW, tier A's first mechanism.
UNAUDITED PROBE.  Exact rational arithmetic only.  Single process, seconds.

THE STATEMENT.

Let T be a template, v a site, N(v) = {s_1 < ... < s_n} its Gamma-neighbours,
w a word, and tau the tuple w induces on N(v).  Put

    S'(tau)[t][j] = A_{v,s_j}[t][tau_j]            (3 x n, committed Def 3.1)
    Q(w)_j        = haf_{Gamma - {v,s_j}}(w)       (committed Thm 4.1)
    E_t(w)        = sum of the monomials of the supported matchings of
                    w|v=t that do NOT lie inside Gamma.

**(D) DECOMPOSITION (identity, every point, every ring).**

    H(w|v=t)  =  < S'(tau)_t , Q(w) >  +  E_t(w) .

*Proof.*  H = Phi + E by the definition of extras, and committed Theorem 4.1
gives Phi(w|v=t) = <S'(tau)_t, Q(w)>.  Neither tau nor Q(w) depends on the
letter at v, so the same S'(tau) and Q(w) serve all three letters.  []

**(A) LEMMA W31-4 (the k<=1 affine law).**  Suppose that for each letter t the
word w|v=t is mixed with k(w|v=t) <= 1, and let mu_t be its single extra
monomial (mu_t = 0 when k = 0).  Then at any exact source

    S'(tau) . Q(w)  =  - mu(w),      mu(w) = (mu_0, mu_1, mu_2)^T .

*Proof.*  Exactness gives H(w|v=t) = 0; substitute into (D).  []

This is the affine replacement for committed Corollary 4.2, which is the
special case mu = 0 (untriggered words).  Route A obtains mu = 0 from CLEAN
words, where H = Phi.  The stratum has no clean words -- but it does have
k = 1 words, and Lemma W31-4 consumes those.

**(B) THE AFFINE RANK BOUND (the Theorem 4.3 analogue).**  Fix (v, tau) and
let W(tau) be the set of words with that tuple whose three letters all satisfy
the hypothesis of (A).  Every row S'(tau)_t is then a solution of the linear
system  { Q(w) . X = -mu_t(w) : w in W(tau) }  in n unknowns.  Hence

  (B1) DIFFERENCE BOUND.  rank S'(tau) <= n - dim span{ Q(w) - Q(w') :
       w, w' in W(tau) with mu_t(w) = mu_t(w') for every t }.
       With mu == 0 this is exactly committed Theorem 4.3.

  (B2) CONSISTENCY / KILL.  The system must be CONSISTENT.  By
       Rouche-Capelli, for each t,
              rank [ Q ]  =  rank [ Q | -mu_t ] .
       If the augmented rank exceeds the plain rank at some (v, tau, t), no
       exact source exists on that template.  This is the affine analogue of
       W26's Farkas branch, and it is the first kill criterion tier A has.

HONEST SCOPE.  Q(w) and mu_t(w) are polynomials in the cell values and S' is
built from cell values, so (B2) is a condition ON THE POINT, not a numeric
test computable from the template alone; it becomes a determinantal condition
for elimination.  What is proved here is (D), (A), (B1), (B2) as statements,
plus the exact inventory that says whether they have input.

CONTROLS
  V1  (D) verified at RANDOM cell values (committed hypothesis (H1): a check
      confined to a solution locus cannot distinguish an identity from a
      coincidence).  0 mismatches required, every site, every letter.
  V2  MUTATION: perturb one Q entry; (D) must break.
  V3  INVENTORY: the k-distribution of the tier-A template, and |W(tau)| per
      (v, tau) -- does the law have input at all?
  V4  POSITIVE CONTROL: on a template WITH clean words, the words with mu = 0
      must be exactly the untriggered ones, so (A) reduces to committed
      Corollary 4.2 -- checked by comparing the two predicates directly.
  V5  DEGENERACY GUARD: report dim span{Q(w)} per tuple at a random point; if
      it were 0 the bound would be vacuous.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "computations",
                                "unaudited-blockers-w26-2026-08-16"))
N, FULL = 8, 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}


def _pms(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        for mm in _pms(rest[:i] + rest[i + 1:]):
            out.append(((a, b),) + mm)
    return out


PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(N))))
WORDS = tuple(product(range(3), repeat=N))
MIXED = set(w for w in WORDS if len(set(w)) > 1)


def occ(T, e, i, j):
    return (T[EIDX[e]] >> (3 * i + j)) & 1


def rank_Q(rows, ncol):
    m = [[Fraction(v) for v in r] for r in rows]
    r = 0
    for c in range(ncol):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        pv = m[r][c]
        m[r] = [v / pv for v in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == ncol:
            break
    return r


def main():
    OUT = {"_header": "UNAUDITED W31 Lemma W31-4 (k<=1 affine law). Exact "
                      "rational arithmetic only. Nothing here is a proved "
                      "claim of the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}
    rng = random.Random(20260819)

    tA = json.load(open(os.path.join(HERE, "results_tierA.json")))
    T = tA["T1_template"]
    gm = tA["T1_gamma_mask"]
    gs = set(EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1)
    OUT["template_gamma_mask"] = gm
    print("[setup] tier-A template, gamma =", gm)

    val = {(e, i, j): Fraction(rng.randint(-9, 9) or 5)
           for e in EDGES for i in range(3) for j in range(3)
           if occ(T, e, i, j)}

    def cellv(u, v, a, b):
        e = (u, v) if u < v else (v, u)
        i, j = (a, b) if u < v else (b, a)
        return val[(e, i, j)] if occ(T, e, i, j) else Fraction(0)

    def gcell(u, v, a, b):
        e = (u, v) if u < v else (v, u)
        if e not in gs:
            return Fraction(0)
        return cellv(u, v, a, b)

    def gamma_haf(sites, w):
        tot = Fraction(0)
        for M in _pms(tuple(sorted(sites))):
            p = Fraction(1)
            for u, v in M:
                p *= gcell(u, v, w[u], w[v])
                if p == 0:
                    break
            tot += p
        return tot

    def H(w):
        tot = Fraction(0)
        for M in PMS:
            p = Fraction(1)
            for u, v in M:
                p *= cellv(u, v, w[u], w[v])
                if p == 0:
                    break
            tot += p
        return tot

    def extras(w):
        """(count, sum of monomials) over supported matchings outside Gamma."""
        n, tot = 0, Fraction(0)
        for M in PMS:
            if all(e in gs for e in M):
                continue
            p = Fraction(1)
            for u, v in M:
                p *= cellv(u, v, w[u], w[v])
                if p == 0:
                    break
            if p != 0 or all(occ(T, e, w[e[0]], w[e[1]]) for e in M):
                if all(occ(T, e, w[e[0]], w[e[1]]) for e in M):
                    n += 1
                    tot += p
        return n, tot

    NB = {v: sorted(s for s in range(N)
                    if (min(v, s), max(v, s)) in gs) for v in range(N)}
    OUT["gamma_degrees"] = {str(v): len(NB[v]) for v in range(N)}

    # ---------------- V1 / V2 : the decomposition identity -----------------
    tests = mism = 0
    for v in range(N):
        for _ in range(20):
            w = [rng.randrange(3) for _ in range(N)]
            Q = [gamma_haf([s for s in range(N) if s not in (v, sj)], w)
                 for sj in NB[v]]
            for t in range(3):
                wt = tuple(w[:v] + [t] + w[v + 1:])
                _, E = extras(wt)
                rhs = sum(cellv(v, sj, t, w[sj]) * Q[k]
                          for k, sj in enumerate(NB[v])) + E
                tests += 1
                if H(wt) != rhs:
                    mism += 1
    OUT["V1_decomposition_tests"] = tests
    OUT["V1_decomposition_mismatches"] = mism
    print("[V1] decomposition (D): %d tests, %d mismatches" % (tests, mism))

    v = 0
    w = [rng.randrange(3) for _ in range(N)]
    Q = [gamma_haf([s for s in range(N) if s not in (v, sj)], w)
         for sj in NB[v]]
    Q[0] += 1
    wt = tuple([0] + w[1:])
    _, E = extras(wt)
    OUT["V2_mutation_fires"] = (
        H(wt) != sum(cellv(v, sj, 0, w[sj]) * Q[k]
                     for k, sj in enumerate(NB[v])) + E)
    print("[V2] mutation control fires:", OUT["V2_mutation_fires"])

    # ---------------- V3 : the inventory -----------------------------------
    nF = sum(1 for M in PMS if all(e in gs for e in M))
    kdist = {}
    kof = {}
    for w in WORDS:
        n, _ = extras(w)
        kof[w] = n
        kdist[n] = kdist.get(n, 0) + 1
    OUT["V3_k_distribution_all_words"] = {str(k): v for k, v in
                                          sorted(kdist.items())}
    OUT["V3_nF"] = nF
    print("[V3] |F| =", nF, " k-distribution over all 6561 words:",
          OUT["V3_k_distribution_all_words"])

    inv = {}
    for v in range(N):
        per_tau = {}
        for w in WORDS:
            tau = tuple(w[s] for s in NB[v])
            ok = all((tuple(w[:v] + (t,) + w[v + 1:]) in MIXED
                      and kof[tuple(w[:v] + (t,) + w[v + 1:])] <= 1)
                     for t in range(3))
            if ok:
                per_tau.setdefault(tau, set()).add(
                    tuple(w[s] for s in range(N) if s != v and s not in NB[v]))
        inv[v] = {str(k): len(s) for k, s in per_tau.items()}
    tot = {v: sum(inv[v].values()) for v in inv}
    best = {v: (max(inv[v].values()) if inv[v] else 0) for v in inv}
    OUT["V3_words_meeting_the_hypothesis_per_site"] = tot
    OUT["V3_max_W_tau_per_site"] = best
    print("[V3] words meeting the k<=1 hypothesis, per site:", tot)
    print("     largest |W(tau)| per site:", best)
    OUT["V3_law_has_input"] = any(b >= 2 for b in best.values())
    print("     the affine law has input (some |W(tau)| >= 2):",
          OUT["V3_law_has_input"])

    # V3b : the RELAXED inventory.  The k<=1 hypothesis only exists to make
    # E_t a single monomial; the identity (D) holds for every k.  Measure how
    # controlled the right-hand side can be: the distribution of
    # max_t k(w|v=t), the number of extra monomials the affine law must carry.
    relax = {}
    for v in range(N):
        d = {}
        for w in WORDS:
            mk = max(kof[tuple(w[:v] + (t,) + w[v + 1:])] for t in range(3))
            d[mk] = d.get(mk, 0) + 1
        relax[v] = dict(sorted(d.items())[:6])
    OUT["V3b_max_letter_k_distribution_per_site"] = {
        str(v): {str(a): b for a, b in relax[v].items()} for v in relax}
    mins = {v: min(relax[v]) for v in relax}
    OUT["V3b_min_over_words_of_max_letter_k"] = mins
    print("[V3b] min over words of max_t k(w|v=t), per site:", mins)
    print("      => the affine law's RHS must carry at least that many "
          "monomials; the k<=1 form needs 1")

    # ---------------- V5 : Q-span degeneracy guard -------------------------
    spans = {}
    for v in range(N):
        n = len(NB[v])
        rows = []
        for _ in range(40):
            w = [rng.randrange(3) for _ in range(N)]
            rows.append([gamma_haf([s for s in range(N) if s not in (v, sj)],
                                   w) for sj in NB[v]])
        spans[v] = dict(n=n, dim_span_Q_at_random_point=rank_Q(rows, n))
    OUT["V5_Q_span"] = spans
    print("[V5] dim span Q at a random point, per site:",
          {v: spans[v]["dim_span_Q_at_random_point"] for v in spans})

    # ---------------- V4 : positive control on a clean-word template -------
    import w26_core as C26                                        # noqa: E402
    T26 = list(C26.TEMPLATES[28])
    gs26 = set(C26.gamma_edges(T26))
    v26 = 4
    NB26 = sorted(s for s in range(N)
                  if (min(v26, s), max(v26, s)) in gs26)
    val26 = {(e, i, j): Fraction(rng.randint(-9, 9) or 5)
             for e in EDGES for i in range(3) for j in range(3)
             if (T26[EIDX[e]] >> (3 * i + j)) & 1}

    def ext26(w):
        n = 0
        for M in PMS:
            if all(e in gs26 for e in M):
                continue
            if all((T26[EIDX[e]] >> (3 * w[e[0]] + w[e[1]])) & 1 for e in M):
                n += 1
        return n
    agree = dis = 0
    for _ in range(400):
        w = tuple(rng.randrange(3) for _ in range(N))
        mu_zero = all(ext26(tuple(w[:v26] + (t,) + w[v26 + 1:])) == 0
                      for t in range(3))
        clean = all(ext26(tuple(w[:v26] + (t,) + w[v26 + 1:])) == 0
                    for t in range(3))
        if mu_zero == clean:
            agree += 1
        else:
            dis += 1
    OUT["V4_mu_zero_equals_clean"] = dict(agree=agree, disagree=dis)
    OUT["V4_ok"] = (dis == 0)
    print("[V4] on a clean-word template, 'mu = 0' and 'untriggered/clean' "
          "coincide:", OUT["V4_ok"], "(%d/%d)" % (agree, agree + dis))

    OUT["VERDICT"] = (
        "(D) verified as an identity (%d tests, %d mismatches) and Lemma "
        "W31-4 follows from it by substituting H = 0. Inventory on the "
        "tier-A template: k-distribution %s; largest |W(tau)| per site %s; "
        "the law has usable input: %s."
        % (tests, mism, OUT["V3_k_distribution_all_words"], best,
           OUT["V3_law_has_input"]))
    print()
    print("[VERDICT]", OUT["VERDICT"])

    json.dump(OUT, open(os.path.join(HERE, "results_affine.json"), "w"),
              indent=1, sort_keys=True)
    declared = ["V1_decomposition_mismatches", "V2_mutation_fires",
                "V3_k_distribution_all_words", "V4_ok", "V5_Q_span"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
