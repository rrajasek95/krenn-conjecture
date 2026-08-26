#!/usr/bin/env python3
"""AUDIT A4 / CHECK 05 -- CLAIM 3 (PROPOSITION W12-C, the structural boundary).

CLAIM: for a graph Gamma on [N] (N even), an even bipartition (L,R) whose
Gamma-crossing edges pairwise intersect EXISTS  <=>  Gamma is NOT a spanning
2-connected subgraph of K_N.

The probe checked 4000 random graphs (edge count uniform on 0..19, so dense
graphs were never sampled).  Here the equivalence is instead settled
EXHAUSTIVELY by an extremal argument, because both sides are monotone:

  D = {Gamma : a feasible cut exists}   is a DOWN-set (removing edges keeps it)
  U = {Gamma : spanning 2-connected}    is an UP-set

so D = U^c follows from two finite checks:
  (a) U n D = 0:  no MAXIMAL element of D is 2-connected.  The maximal
      elements of D are, for each even cut (L,R) and each vertex x,
      E(L) u E(R) u {crossing edges incident to x}.
  (b) U^c c D:  every MAXIMAL element of U^c lies in D.  A maximal
      non-spanning-2-connected graph is connected with a cut vertex x and is
      therefore K_{A u {x}} u K_{B u {x}} for a partition A|B of [N]\\{x}.

Plus: exhaustive over ALL 2^15 graphs on 6 vertices, and a stratified random
sample at N=8 covering every edge count 0..28 (the probe's sample did not).
Plus: the Gamma predicate recomputed on the probe's own 135 targets from the
ORIGINAL template sources and compared to the recorded cut outcomes.
"""
from __future__ import annotations

import glob
import json
import os
import random
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")
W11 = os.path.join(ROOT, "computations", "unaudited-sat-pair-w11-2026-08-15")
W12 = os.path.join(ROOT, "computations", "unaudited-thickfibre-w12-2026-08-15")
import a4_engine as E  # noqa: E402

out = {}


# --------------------------------------------------- graph predicates (mine)
def connected_on(vertices, edges):
    vs = set(vertices)
    if not vs:
        return True
    adj = {v: set() for v in vs}
    for (a, b) in edges:
        if a in vs and b in vs:
            adj[a].add(b)
            adj[b].add(a)
    start = next(iter(vs))
    seen = {start}
    stack = [start]
    while stack:                                  # DFS, not union-find
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen == vs


def spanning_2connected(G, n):
    """Spans [n], connected, and no single vertex removal disconnects it."""
    cov = {v for e in G for v in e}
    if cov != set(range(n)):
        return False
    if not connected_on(range(n), G):
        return False
    for x in range(n):
        rest = [v for v in range(n) if v != x]
        sub = [e for e in G if x not in e]
        if not connected_on(rest, sub):
            return False
    return True


def even_cuts(n):
    seen, res = set(), []
    for k in range(2, n - 1, 2):
        for L in combinations(range(n), k):
            Ls = frozenset(L)
            key = frozenset((Ls, frozenset(range(n)) - Ls))
            if key not in seen:
                seen.add(key)
                res.append((Ls, frozenset(range(n)) - Ls))
    return res


def pairwise_intersecting(edges):
    return all(len({a, b, c, d}) < 4
               for (a, b), (c, d) in combinations(edges, 2))


def feasible_cut(G, n, cuts=None):
    for (L, R) in (cuts or even_cuts(n)):
        cross = [e for e in G if (e[0] in L) != (e[1] in L)]
        if pairwise_intersecting(cross):
            return True, sorted(L)
    return False, None


# ------------------------------------------------- (a) maximal elements of D
def check_exhaustive(n):
    cuts = even_cuts(n)
    res = {"n": n, "maxD_tested": 0, "maxD_2connected": [],
           "maxUc_tested": 0, "maxUc_not_feasible": []}
    for (L, R) in cuts:
        internal = [e for e in combinations(range(n), 2)
                    if (e[0] in L) == (e[1] in L)]
        crossing = [e for e in combinations(range(n), 2)
                    if (e[0] in L) != (e[1] in L)]
        for x in range(n):
            G = internal + [e for e in crossing if x in e]
            res["maxD_tested"] += 1
            assert feasible_cut(G, n, cuts)[0], "maximal-D element not in D"
            if spanning_2connected(G, n):
                res["maxD_2connected"].append([sorted(L), x])
    # (b) maximal elements of U^c
    others = list(range(n))
    for x in range(n):
        rest = [v for v in others if v != x]
        for mask in range(1, 1 << (n - 1)):
            A = [rest[k] for k in range(n - 1) if (mask >> k) & 1]
            B = [v for v in rest if v not in A]
            if not A or not B:
                continue
            if A[0] != rest[0]:            # unordered partition
                continue
            SA, SB = set(A) | {x}, set(B) | {x}
            G = [e for e in combinations(range(n), 2)
                 if set(e) <= SA or set(e) <= SB]
            res["maxUc_tested"] += 1
            assert not spanning_2connected(G, n), "maximal-U^c element is 2conn"
            ok, _ = feasible_cut(G, n, cuts)
            if not ok:
                res["maxUc_not_feasible"].append([x, sorted(A), sorted(B)])
    res["equivalence_proved"] = (not res["maxD_2connected"]
                                 and not res["maxUc_not_feasible"])
    return res


for n in (4, 6, 8, 10):
    r = check_exhaustive(n)
    out[f"extremal_N{n}"] = r
    print(f"EXTREMAL N={n}: maximal-D elements tested {r['maxD_tested']} "
          f"(2-connected among them: {len(r['maxD_2connected'])}); "
          f"maximal-U^c tested {r['maxUc_tested']} (without a feasible cut: "
          f"{len(r['maxUc_not_feasible'])})  ==> EQUIVALENCE PROVED: "
          f"{r['equivalence_proved']}")


# ---------------------------------------- exhaustive over ALL graphs, N=4, 6
def exhaustive_all(n):
    ALL = list(combinations(range(n), 2))
    cuts = even_cuts(n)
    bad = []
    tot = 0
    for bits in range(1 << len(ALL)):
        G = [ALL[k] for k in range(len(ALL)) if (bits >> k) & 1]
        tot += 1
        a = spanning_2connected(G, n)
        b = feasible_cut(G, n, cuts)[0]
        if a == b:
            bad.append(sorted(map(list, G)))
    return {"graphs": tot, "violations": len(bad), "examples": bad[:3]}


for n in (4, 6):
    r = exhaustive_all(n)
    out[f"exhaustive_all_N{n}"] = r
    print(f"EXHAUSTIVE all {r['graphs']} graphs on {n} vertices: "
          f"violations = {r['violations']}")


# --------------------------- stratified random sample at N=8 (all densities)
ALL8 = list(combinations(range(8), 2))
CUTS8 = even_cuts(8)
rng = random.Random(31337)
bad, per_density = [], {}
for k in range(0, 29):
    n2c = 0
    for _ in range(1200):
        G = rng.sample(ALL8, k)
        a = spanning_2connected(G, 8)
        b = feasible_cut(G, 8, CUTS8)[0]
        n2c += a
        if a == b:
            bad.append([k, sorted(map(list, G))])
    per_density[k] = n2c
out["random_N8_stratified"] = {"per_density_2connected": per_density,
                               "violations": len(bad),
                               "examples": bad[:3], "samples": 29 * 1200}
print(f"RANDOM N=8 stratified over edge counts 0..28 ({29*1200} graphs): "
      f"violations = {len(bad)}; 2-connected seen at densities "
      f"{[k for k,v in per_density.items() if v]}")

# MUTATION CONTROL on the checker: a deliberately wrong predicate must fail.
wrong = 0
for _ in range(400):
    k = rng.randrange(0, 29)
    G = rng.sample(ALL8, k)
    a = connected_on(range(8), G) and {v for e in G for v in e} == set(range(8))
    b = feasible_cut(G, 8, CUTS8)[0]
    if a == b:
        wrong += 1
out["mutation_control_wrong_predicate_violations"] = wrong
print(f"MUTATION CONTROL: replacing '2-connected' by 'connected+spanning' "
      f"gives {wrong}/400 violations (must be > 0)")


# ------------------------- CLAIM 3, part 3: the predicate on the 135 targets
def gamma_of(T):
    """Graph of FULL nine-cell blocks."""
    full = []
    for k, (u, v) in enumerate(T.edges):
        if len(T.cells_of(k)) == 9:
            full.append((u, v))
    return full


def load_targets():
    tg = []
    with open(os.path.join(W8, "results_close_m20.json")) as fh:
        tg.append(("survivor_m20", E.Template.from_masks(
            json.load(fh)["survivors"][0])))
    with open(os.path.join(W8, "results_immunity.json")) as fh:
        for e in json.load(fh)["results"]:
            tg.append((f"immunity_m{e['m']}", E.Template.from_masks(e["template"])))
    for path in sorted(glob.glob(os.path.join(W11, "witnesses", "*.json"))):
        if os.path.basename(path) == "summary.json":
            continue
        with open(path) as fh:
            d = json.load(fh)
        base = E.Template(8, ())
        occ = set()
        for e, cells in zip(d["edges"], d["blocks"]):
            k = base.eidx[tuple(sorted(e))]
            for (i, j) in cells:
                occ.add((k, i, j))
        tg.append((os.path.basename(path)[:-5], E.Template(8, occ)))
    with open(os.path.join(W8, "results_enumerate_m17.json")) as fh:
        for k, c in enumerate(json.load(fh)["classes"]):
            tg.append((f"m17_class{k}", E.Template.from_masks(c["template"])))
    return tg


TARGETS = load_targets()
print(f"\nGAMMA PREDICATE over {len(TARGETS)} targets (recomputed from the "
      f"original template sources):")
rows = []
for name, T in TARGETS:
    G = gamma_of(T)
    ok, L = feasible_cut(G, 8, CUTS8)
    rows.append({"name": name, "gamma_size": len(G),
                 "spanning_2connected": spanning_2connected(G, 8),
                 "feasible_cut": ok, "witness_L": L})
out["targets_gamma"] = rows
no_cut = [r["name"] for r in rows if not r["feasible_cut"]]
two_conn = [r["name"] for r in rows if r["spanning_2connected"]]
print(f"  targets with NO feasible cut : {no_cut}")
print(f"  targets with Gamma 2-connected: {two_conn}")
out["no_feasible_cut"] = no_cut
out["gamma_2connected"] = two_conn
out["predicate_agrees_with_equivalence"] = (sorted(no_cut) == sorted(two_conn))

# compare with the probe's recorded outcomes
with open(os.path.join(W12, "results_t3_cut_core.json")) as fh:
    core = {r["name"]: r["verdict"] for r in json.load(fh)}
with open(os.path.join(W12, "results_t3_cut_w11.json")) as fh:
    w11 = {r["name"]: r["verdict"] for r in json.load(fh)}
recorded = dict(core)
recorded.update(w11)
mism = []
for r in rows:
    v = recorded.get(r["name"])
    if v is None:
        continue
    if (v == "killed") != r["feasible_cut"]:
        mism.append([r["name"], v, r["feasible_cut"]])
out["recorded_outcome_vs_predicate_mismatches"] = mism
out["recorded_outcomes_compared"] = sum(
    1 for r in rows if r["name"] in recorded)
print(f"  compared against {out['recorded_outcomes_compared']} recorded cut "
      f"verdicts: mismatches = {len(mism)}  {mism}")
missing = [r["name"] for r in rows
           if r["name"] not in recorded and not r["name"].startswith("m17_")]
print(f"  targets with NO recorded cut verdict in the probe's JSONs: {missing}")
out["targets_without_recorded_cut_verdict"] = missing

with open(os.path.join(HERE, "results_chk05.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote results_chk05.json")
