#!/usr/bin/env python3
"""H1 / BLOCKER 1 addendum -- two scope facts the A3 report and the
promotion draft do not state.

UNAUDITED.  Hygiene agent H1, 2026-08-15.  Exact integer arithmetic.

A  THE N = 4 EXCEPTION to the even-cycle-free corollary.
   A3's report states "every diagonal monomial source with even-cycle-free
   colour graphs dies" with no order hypothesis.  The proof runs through
   Theorem A3.4, which is FALSE at N = 4, so the corollary needs N >= 6.
   This enumerates every diagonal template on K_4 with three live constant
   fibres and even-cycle-free colour graphs and reports how many have NO
   mixed singleton fibre.  A nonzero count is a genuine counterexample to
   the corollary as stated, and pins the hypothesis.

B  THE J.1d BUDGET AT m = 3N/2 AND AT m = 3N/2 + 1.
   W6's budget (w6_task2_counting.py, inequalities (4),(6),(7)) reads
        beta   >= 3N - m + |H|                                        (4)
        t1 + 2 t2 + 3 t3 = 3N/2,  beta <= m - t2 - t3                 (6)
        t2 + t3 <= 2m - 3N - |H|                                      (7)
   At m = 3N/2 the right-hand side of (7) is -|H|, forcing
   t2 = t3 = |H| = 0: every block a single DIAGONAL cell on a properly
   3-edge-coloured cubic graph.  This enumerates the integer solutions of
   (4)/(6)/(7) at m = 3N/2 and at m = 3N/2 + 1 to show WHETHER the same
   forcing holds one step above the floor.
"""

from __future__ import annotations

import json
import os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))

import h1_b1_fourth_matching as B1                              # noqa: E402


# ------------------------------------------------------- A: the N=4 case

def n4_exception():
    n = 4
    alledges = list(combinations(range(n), 2))
    full = (1 << n) - 1
    tested = 0
    no_mixed_singleton = []
    with_mixed_singleton = 0
    # every assignment of the 6 edges of K_4 to {G_0,G_1,G_2,absent}
    for code in range(4 ** len(alledges)):
        t = code
        cols = [set(), set(), set()]
        for e in alledges:
            r = t % 4
            t //= 4
            if r < 3:
                cols[r].add(e)
        nbrs = [B1.nbr_bits(n, cols[r]) for r in range(3)]
        # three live constant fibres
        if any(B1.pm_count_mask(nbrs[r], full, {}) == 0 for r in range(3)):
            continue
        # even-cycle-free colour graphs
        if any(B1.has_even_cycle(n, sorted(cols[r])) for r in range(3)):
            continue
        tested += 1
        found = False
        for w in _words(n):
            if len(set(w)) == 1:
                continue
            if B1.fibre_size_dp(n, cols, w, nbrs) == 1:
                found = True
                break
        if found:
            with_mixed_singleton += 1
        else:
            no_mixed_singleton.append([sorted(map(list, c)) for c in cols])
    return dict(N=4, templates_tested=tested,
                with_mixed_singleton=with_mixed_singleton,
                without_mixed_singleton=len(no_mixed_singleton),
                corollary_holds_at_N4=(len(no_mixed_singleton) == 0),
                counterexample_sample=no_mixed_singleton[:3])


def _words(n):
    for k in range(3 ** n):
        t, w = k, []
        for _ in range(n):
            w.append(t % 3)
            t //= 3
        yield tuple(w)


# --------------------------------------------------- B: the J.1d budget

def budget_solutions(N, m):
    """Integer solutions of W6's (4)/(6)/(7) at support m.

    Reports whether the single-diagonal-cell regime is FORCED, i.e. whether
    t2 = t3 = |H| = 0 and every block is a basis edge in every solution."""
    sols = []
    for H in range(0, m + 1):
        R = m - H
        for t3 in range(0, 3 * N // 2 // 3 + 1):
            for t2 in range(0, 3 * N // 2 // 2 + 1):
                t1 = 3 * N // 2 - 2 * t2 - 3 * t3
                if t1 < 0:
                    continue
                if t2 + t3 > 2 * m - 3 * N - H:          # (7)
                    continue
                lo = 3 * N - m + H                       # (4)
                hi = m - t2 - t3                         # (6)
                for beta in range(max(lo, 0), hi + 1):
                    if beta > R:
                        continue
                    sols.append(dict(H=H, t1=t1, t2=t2, t3=t3, beta=beta,
                                     nonbasis_R_blocks=R - beta))
    forced = all(s["H"] == 0 and s["t2"] == 0 and s["t3"] == 0
                 and s["nonbasis_R_blocks"] == 0 for s in sols)
    return dict(N=N, m=m, solutions=len(sols),
                single_diagonal_cell_regime_forced=forced,
                max_nonbasis_R_blocks=max([s["nonbasis_R_blocks"]
                                           for s in sols], default=None),
                max_H=max([s["H"] for s in sols], default=None),
                max_t2_plus_t3=max([s["t2"] + s["t3"] for s in sols],
                                   default=None),
                sample=sols[:6])


def main():
    out = {"agent": "H1", "blocker": "1-addendum",
           "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")
                               ).read().split()[0]}

    print("== A: the N = 4 exception to the even-cycle-free corollary ==")
    a = n4_exception()
    out["A_N4_exception"] = a
    print(f"   templates with 3 live pures + even-cycle-free colours: "
          f"{a['templates_tested']}")
    print(f"   WITH a mixed singleton: {a['with_mixed_singleton']}")
    print(f"   WITHOUT (counterexamples to the corollary as stated): "
          f"{a['without_mixed_singleton']}")
    print(f"   corollary holds at N=4: {a['corollary_holds_at_N4']}")

    print("== B: the J.1d budget at the floor and one above ==")
    out["B_budget"] = {}
    for N in (6, 8, 10, 12):
        for m in (3 * N // 2, 3 * N // 2 + 1):
            r = budget_solutions(N, m)
            out["B_budget"][f"N={N},m={m}"] = r
            print(f"   N={N:2d} m={m:2d} ({'floor' if m == 3*N//2 else 'floor+1'}): "
                  f"solutions={r['solutions']:4d} "
                  f"single-diagonal-cell FORCED={r['single_diagonal_cell_regime_forced']} "
                  f"max non-basis R blocks={r['max_nonbasis_R_blocks']} "
                  f"max|H|={r['max_H']} max(t2+t3)={r['max_t2_plus_t3']}")

    with open(os.path.join(HERE, "results_b1_addendum.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("\nwrote results_b1_addendum.json")


if __name__ == "__main__":
    main()
