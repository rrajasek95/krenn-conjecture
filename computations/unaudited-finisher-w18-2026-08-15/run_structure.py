#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- the structural facts that frame the m <= 19 band.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

LEMMA W18-E.  For an (SC)-admissible template T at N = 8 with support m,
    |Gamma(T)| <= m - 12,
where Gamma(T) is the graph of FULL nine-cell blocks.  Consequently, at
m <= 19 we get |Gamma| <= 7 < 8, and since every spanning 2-connected
subgraph of K_8 has at least 8 edges, Gamma(T) is NEVER spanning 2-connected:
W12's residual family (R) is EMPTY at every support <= 19, and W12-C's
feasible-cut criterion always applies.

Proof of the bound.  (SC) gives, for each of the 8 vertices p and each of the
3 colours r, an incident edge whose block is nonzero and supported in the
single far-end colour r.  Two different colours at the same endpoint need two
different edges (a nonzero block is supported in at most one far colour from a
given end), so the 24 (vertex, colour) slots are served by SERVER edges, each
of which serves at most 2 slots (one per endpoint).  Hence there are at least
12 server edges.  A server edge is thin at one end, so it has at most 3 cells
and is not full: Gamma is disjoint from the server set, giving the bound.

This script checks the three ingredients by brute force:
  E1  a block that is thin at one end has at most 3 cells (all 512 masks);
  E2  a nonzero block is thin in at most one far colour per endpoint;
  E3  every spanning 2-connected subgraph of K_8 has >= 8 edges;
and then verifies |Gamma| <= m - 12 on every admissible template this lane
has on file (W11's witnesses, W8's m=18 orbit witnesses, and every template
stored in a W18-D / W18-C certificate).
"""
from __future__ import annotations

import glob
import gzip
import json
import os
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C          # noqa: E402


def e1_thin_blocks():
    bad = []
    for mask in range(1, 512):
        for side in (False, True):
            if C.far_colour(mask, side) is not None:
                if bin(mask).count("1") > 3:
                    bad.append((mask, side))
    return {"masks_checked": 511, "violations": bad, "passes": not bad}


def e2_unique_far_colour():
    bad = []
    for mask in range(1, 512):
        for side in (False, True):
            hits = 0
            for r in range(3):
                cells = C.cells(mask)
                if all((j if side else i) == r for (i, j) in cells):
                    hits += 1
            if hits > 1:
                bad.append((mask, side, hits))
    return {"masks_checked": 511, "violations": bad, "passes": not bad}


def _components(vertices, edges):
    parent = {v: v for v in vertices}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for (u, v) in edges:
        ra, rb = find(u), find(v)
        if ra != rb:
            parent[ra] = rb
    return len({find(v) for v in vertices})


def spanning_2connected(edges):
    vs = set()
    for e in edges:
        vs.update(e)
    if vs != set(range(8)):
        return False
    if _components(range(8), edges) > 1:
        return False
    for x in range(8):
        rest = [v for v in range(8) if v != x]
        sub = [e for e in edges if x not in e]
        if _components(rest, sub) > 1:
            return False
    return True


def e3_min_edges_spanning_2connected():
    allE = list(combinations(range(8), 2))
    for k in range(0, 8):
        for sub in combinations(allE, k):
            if spanning_2connected(list(sub)):
                return {"found_with": k, "passes": False}
    example = [(i, (i + 1) % 8) for i in range(8)]
    return {"min_edges": 8, "no_spanning_2connected_below": 8,
            "example_at_8": example, "passes": spanning_2connected(example)}


def server_count(T):
    """Number of edges that serve at least one (vertex, colour) slot."""
    srv = set()
    for p in range(C.N):
        for r in range(3):
            for e in C.INCIDENT[p]:
                u, v = C.EDGES[e]
                if C.far_colour(T[e], p_is_first=(u == p)) == r:
                    srv.add(e)
                    break
    return len(srv)


def gamma_edges(T):
    return [e for e, mask in enumerate(T) if mask == C.FULL9]


def check_templates():
    rows = []
    # W11 witnesses
    wdir = os.path.join(HERE, "..", "unaudited-sat-pair-w11-2026-08-15",
                        "witnesses")
    for name in sorted(os.listdir(wdir)):
        if not name.endswith(".json") or name == "summary.json":
            continue
        obj = json.load(open(os.path.join(wdir, name)))
        T = []
        for blk in obj["blocks"]:
            mk = 0
            for (i, j) in blk:
                mk |= 1 << (3 * i + j)
            T.append(mk)
        rows.append(("w11:" + name, tuple(T)))
    # W8's m=18 orbit witnesses
    p = os.path.join(HERE, "..", "unaudited-template-kill-w8-2026-08-15",
                     "results_band_m18_nosingleton.json")
    if os.path.exists(p):
        d = json.load(open(p))
        for r in d["rows"]:
            for T in r.get("survivors", []):
                rows.append(("w8:o%d" % r["orbit"], tuple(int(x) for x in T)))
    # every template stored in this lane's D/C certificates
    for path in glob.glob(os.path.join(HERE, "certificates", "*_kills",
                                       "*.json.gz")):
        with gzip.open(path, "rt") as fh:
            obj = json.load(fh)
        for kind in ("D", "C", "B"):
            for cert in obj["certificates"].get(kind, []):
                if "template" in cert:
                    rows.append((os.path.basename(path) + ":" + kind,
                                 tuple(cert["template"])))
    bad = []
    stats = []
    for name, T in rows:
        m = C.support(T)
        s = server_count(T)
        g = len(gamma_edges(T))
        stats.append({"name": name, "m": m, "sigma": C.sigma(T),
                      "servers": s, "gamma": g})
        if s < 12 or g > m - 12:
            bad.append(stats[-1])
    return {"templates_checked": len(rows), "violations": bad[:10],
            "n_violations": len(bad),
            "max_gamma_at_m_le_19": max([x["gamma"] for x in stats
                                         if x["m"] <= 19] or [0]),
            "min_servers": min([x["servers"] for x in stats] or [0]),
            "sigma_range": [min([x["sigma"] for x in stats] or [0]),
                            max([x["sigma"] for x in stats] or [0])]}


if __name__ == "__main__":
    out = {"E1_thin_blocks_have_at_most_3_cells": e1_thin_blocks(),
           "E2_one_far_colour_per_end": e2_unique_far_colour(),
           "E3_spanning_2connected_needs_8_edges":
               e3_min_edges_spanning_2connected(),
           "templates": check_templates()}
    print(json.dumps(out, indent=1)[:3000])
    json.dump(out, open(os.path.join(HERE, "results_structure.json"), "w"),
              indent=1)
    print("wrote results_structure.json")
