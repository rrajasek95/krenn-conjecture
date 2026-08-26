#!/usr/bin/env python3
"""A7 -- TARGET 4(b): THEOREM W20-R's corollary as a STANDALONE statement,
probed adversarially per ledger item 12 (exhaustive structured sweeps).

ABSTRACTED STATEMENT.  Let t have Gamma-neighbours s = 1..deg and blocks
A_s (3 x 3, all entries nonzero), A_s[c][d] = the cell with colour c at t and
colour d at s.  For a neighbour pattern p in {0,1,2}^deg put
        V_c(p) = ( A_s[c][p_s] )_{s=1..deg}.
Call p REGULAR when V_0(p), V_1(p), V_2(p) are pairwise proportional (this is
what "rank Cf(p) = deg - 1" delivers).  Build the graph on regular patterns
joining p, p' differing in exactly ONE coordinate.  W20-R's corollary:

    regular set CONNECTED and COVERING (meets every (s,d))  =>  site t
    factors, i.e. A_s[c][d] = lam_c * A_s[0][d] for all s,d.

MY PROOF.  Regularity at p gives lam_c(p) with A_s[c][p_s] = lam_c(p)
A_s[0][p_s] for every s.  If p, p' are regular and differ only in coordinate
s0, then for EVERY s != s0 we have p_s = p'_s and A_s[0][p_s] != 0, so
lam_c(p) = lam_c(p').  THIS STEP NEEDS deg >= 2 (otherwise there is no shared
coordinate).  Hence lam_c is constant on each connected component; connected
=> one constant lam_c; covering => the relation holds at every (s,d).  QED.

TESTS BELOW (all exhaustive over structured strata, all-entries-nonzero):
  R1  the conclusion holds whenever connected AND covering AND deg >= 2;
  R2  deg = 1 is a genuine counterexample (the hidden hypothesis);
  R3  dropping CONNECTEDNESS breaks it (explicit witness);
  R4  dropping COVERING breaks it (explicit witness);
  R5  dropping "all entries nonzero" breaks it (explicit witness).
"""
from __future__ import annotations
import os, sys, json, itertools
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))


def prop(a, b):
    return all(a[i] * b[j] - a[j] * b[i] == 0
               for i in range(len(a)) for j in range(i + 1, len(a)))


def analyse(A):
    """A: list of deg blocks, each 3x3.  Returns the regular set, whether it
    is connected and covering, and whether the site factors."""
    deg = len(A)
    reg = []
    for p in itertools.product(range(3), repeat=deg):
        V = [[A[s][c][p[s]] for s in range(deg)] for c in range(3)]
        if all(prop(V[a], V[b]) for a in range(3) for b in range(a + 1, 3)):
            reg.append(p)
    idx = {p: i for i, p in enumerate(reg)}
    par = list(range(len(reg)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for p in reg:
        for k in range(deg):
            for d in range(3):
                q = p[:k] + (d,) + p[k + 1:]
                if q in idx and q != p:
                    ra, rb = find(idx[p]), find(idx[q])
                    if ra != rb:
                        par[ra] = rb
    ncomp = len({find(i) for i in range(len(reg))}) if reg else 0
    covered = {(k, d) for p in reg for k, d in enumerate(p)}
    covering = covered == {(k, d) for k in range(deg) for d in range(3)}
    # does the site factor?
    big = [[A[s][c][d] for s in range(deg) for d in range(3)]
           for c in range(3)]
    fac = all(prop(big[a], big[b]) for a in range(3) for b in range(a + 1, 3))
    return dict(n_regular=len(reg), n_components=ncomp,
                connected=(ncomp == 1 and bool(reg)), covering=covering,
                factors=fac)


def blocks_from_columns(cols):
    """a block from its three columns (columns are indexed by the neighbour
    colour d, entries by the colour c at t)."""
    return [[cols[d][c] for d in range(3)] for c in range(3)]


def col_reps(vals):
    """COLUMN SCALING IS A SYMMETRY of the whole statement: scaling column d
    of block s multiplies coordinate s of ALL THREE V_c(p) with p_s = d by the
    same factor, so both 'regular' and 'factors' are invariant.  Hence we may
    normalise every column to first entry 1 -- an exact reduction, not a
    sample."""
    return [(1, a, b) for a in vals for b in vals]


def sweep_cols(deg, vals):
    """EXHAUSTIVE over all deg blocks, columns normalised to first entry 1
    with the remaining entries in vals."""
    reps = col_reps(vals)
    mats = [blocks_from_columns(c) for c in itertools.product(reps, repeat=3)]
    n = 0
    viol = []
    tally = {}
    for combo in itertools.product(mats, repeat=deg):
        n += 1
        r = analyse(list(combo))
        key = (r["connected"], r["covering"], r["factors"])
        tally[str(key)] = tally.get(str(key), 0) + 1
        if r["connected"] and r["covering"] and not r["factors"]:
            if len(viol) < 5:
                viol.append(dict(blocks=[[[str(x) for x in row] for row in M]
                                         for M in combo], **r))
    return n, tally, viol


def sweep(deg, vals):
    """EXHAUSTIVE over all deg blocks with entries in vals."""
    mats = [[list(f[0:3]), list(f[3:6]), list(f[6:9])]
            for f in itertools.product(vals, repeat=9)]
    n = 0
    viol = []
    tally = {}
    for combo in itertools.product(mats, repeat=deg):
        n += 1
        r = analyse(list(combo))
        key = (r["connected"], r["covering"], r["factors"])
        tally[str(key)] = tally.get(str(key), 0) + 1
        if r["connected"] and r["covering"] and not r["factors"]:
            if len(viol) < 5:
                viol.append(dict(blocks=[[[str(x) for x in row] for row in M]
                                         for M in combo], **r))
    return n, tally, viol


def main():
    res = {}
    # R1: exhaustive at deg = 2 over full {1,2} and {-1,1} entry sweeps ...
    for deg, vals in ((2, (1, 2)), (2, (-1, 1))):
        n, tally, viol = sweep(deg, vals)
        k = "R1_deg%d_vals%s" % (deg, "".join(map(str, vals)))
        res[k] = dict(n=n, tally=tally, violations=viol)
        print("%s: %d instances, tally %s, violations %d"
              % (k, n, tally, len(viol)), flush=True)
    # ... and exhaustive in the COLUMN-NORMALISED reduction at deg = 2 and 3
    for deg, vals in ((2, (1, 2, 3)), (3, (1, 2))):
        n, tally, viol = sweep_cols(deg, vals)
        k = "R1_colnorm_deg%d_vals%s" % (deg, "".join(map(str, vals)))
        res[k] = dict(n=n, tally=tally, violations=viol)
        print("%s: %d instances, tally %s, violations %d"
              % (k, n, tally, len(viol)), flush=True)
    # R2: deg = 1 must break the corollary
    n, tally, viol = sweep(1, (1, 2))
    res["R2_deg1"] = dict(n=n, tally=tally, n_violations=len(viol),
                          witness=viol[0] if viol else None)
    print("R2 deg=1: %d instances, connected+covering-but-not-factoring: %d"
          % (n, len(viol)), flush=True)
    # R3 / R4: search deg=2 for regular sets that are covering-but-disconnected
    # or connected-but-not-covering, with no factoring
    r3 = r4 = None
    reps = col_reps((1, 2, 3))
    mats = [blocks_from_columns(c) for c in itertools.product(reps, repeat=3)]
    import random
    rng = random.Random(5)
    for _ in range(60000):
        A = [rng.choice(mats), rng.choice(mats)]
        r = analyse(A)
        if r["factors"]:
            continue
        if r["covering"] and not r["connected"] and r3 is None:
            r3 = dict(blocks=[[[str(x) for x in row] for row in M] for M in A],
                      **r)
        if r["connected"] and not r["covering"] and r4 is None:
            r4 = dict(blocks=[[[str(x) for x in row] for row in M] for M in A],
                      **r)
        if r3 and r4:
            break
    res["R3_covering_not_connected_witness"] = r3
    res["R4_connected_not_covering_witness"] = r4
    print("R3 (covering, disconnected, not factoring) witness found:", r3 is not None)
    print("R4 (connected, not covering, not factoring) witness found:", r4 is not None)
    # R5: allow a zero entry -> the chaining step can fail
    r5 = None
    reps0 = [(1, a, b) for a in (0, 1, 2) for b in (0, 1, 2)] + \
            [(0, a, b) for a in (0, 1) for b in (0, 1)]
    mats0 = [blocks_from_columns(c) for c in itertools.product(reps0, repeat=3)]
    for A in itertools.product(mats0, repeat=2):
        if all(x for M in A for row in M for x in row):
            continue
        r = analyse(list(A))
        if r["connected"] and r["covering"] and not r["factors"]:
            r5 = dict(blocks=[[[str(x) for x in row] for row in M] for M in A],
                      **r)
            break
    res["R5_zero_entry_witness"] = r5
    print("R5 (zero entry breaks the corollary) witness found:", r5 is not None)
    json.dump(res, open(os.path.join(HERE, "results_w20r.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
