#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- J.1c: pattern co-occurrence and the h=3 analogue of
W4's criterion (C).

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

Three parts.

(A) CO-OCCURRENCE.  P1 and P2 recorded which SINGLE patterns fire; J.1c is a
    statement about the SET.  We tabulate the sets on
      * P2's 69 all-blocked shadow sources (h = 2, N = 6, 1,034 live pairs);
      * P2's generic / stratified / anchored runs (h = 2);
      * the committed near-exact eight-site source (h = 3, 28 pairs).
    W4 proved (Cauchy/Pieri) that pattern laws exist only in degrees 2 and 3,
    so degree 3 is the whole law-governed range and nothing above it is
    measured.

(B) THE h=3 ANALOGUE OF (C) IN R_cell.  In R_cell write the single cell of
    A_px as (i_x, j_x) with weight alpha_x (row = colour at p) and of A_qx as
    (k_x, l_x) with weight beta_x.  Then

        R_ab(c_a, c_b) = [c_a=j_a][c_b=l_b] alpha_a beta_b K_{i_a k_b}
                       + [c_a=l_a][c_b=j_b] alpha_b beta_a K_{i_b k_a},

    so in  6E_w = [3 s r^2 x + r^3]_full  the r^3 part is indexed by an
    ORIENTED perfect matching of U: a 3+3 split U = X (p-side) u Y (q-side)
    together with a bijection sigma.  All oriented matchings with p-side X hit
    the SAME word w(X) (w_x = j_x on X, w_y = l_y on Y) and contribute

        per_3( [ alpha_x beta_y K_{i_x k_y} ]_{x in X, y in Y} ),          (P3)

    a 3x3 PERMANENT -- exactly the shape P1's ``three_star`` family predicts.
    The s r^2 x part contributes s * gamma_ab * per_2 on the complementary
    2+2 split.  Hence the exact h=3 analogues of W4's 2+2 criterion:

    (C3-kappa)  kappa_c^3 is proportional to the r^3 part of E_{w(X)} iff some
                3+3 split has i_x = c for every x in X and k_y = c for every
                y in Y (and the weight product is nonzero);
    (C3-s)      s^3 likewise with c replaced by (i_0 on the p-side, j_0 on the
                q-side), (i_0, j_0) the cell of A_pq.

    Both are SUPPORT conditions on the cell pattern -- the same shape as (C).
    They are sufficient-modulo-collision: if the word w(X) also receives other
    contributions the component is a sum, and membership can still hold in the
    SPAN.  Measured below against exact degree-3 membership.

(C) TRACKING W4's NECESSARY CONDITION (N) (e_c in the column spans P and Q)
    as exactness is imposed -- see w6_task1_mechanism.py for (STAR).

Run: python3 w6_task1_bridge.py [--templates N]
"""

from __future__ import annotations

import json
import random
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations

P1 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p1-2026-08-15")
P2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p2-2026-08-15")
# P2 is read only as JSON (its wsplit_core would shadow P1's), so only P1 is
# put on the import path.
if P1 not in sys.path:
    sys.path.insert(0, P1)

import wsplit_core as pcore                                     # noqa: E402
from wsplit_core import COLORS, P, Q, U, kidx                   # noqa: E402
from wsplit_h3_structure import (blocking_certificate,          # noqa: E402
                                 degree3_obstructions)


# --------------------------------------------------------------------- part A


def kind_of(pattern):
    left, right = pattern.split("*")
    if left == "s" and right == "s":
        return "s2"
    if left == "s" or right == "s":
        return "s*kappa"
    if left == right:
        return "kappa2"
    return "kappa*kappa'"


def h2_tables():
    out = {}
    for name, key in (("results_c.json", "shadows"),
                      ("results_a.json", "generic"),
                      ("results_b.json", "strata"),
                      ("results_b2.json", "anchored-coordinate")):
        try:
            with open(f"{P2}/{name}") as handle:
                blob = json.load(handle)
        except (OSError, json.JSONDecodeError):
            continue
        rows = blob.get("results", blob)
        if isinstance(rows, dict):
            rows = rows.get("results", [])
        if key == "shadows":
            rows = [r for r in rows if r.get("all_live_blocked")]
        histogram = Counter()
        sets = Counter()
        blocked_live = 0
        for row in rows:
            for record in row.get("pairs", []):
                if record.get("status") == "dead":
                    continue
                if record.get("witness"):
                    continue
                blocked_live += 1
                patterns = tuple(sorted(record.get("patterns") or []))
                sets[patterns] += 1
                histogram[sum(1 for p in patterns
                              if kind_of(p) == "s*kappa")] += 1
        out[key] = {
            "blocked_live_pairs": blocked_live,
            "s_kappa_count_histogram": dict(sorted(histogram.items())),
            "at_least_two_s_kappa": sum(v for k, v in histogram.items()
                                        if k >= 2),
            "top_sets": {str(k): v for k, v in sets.most_common(10)},
        }
    return out


def h3_stage_a_table():
    with open(f"{P1}/h3_structure.json") as handle:
        blob = json.load(handle)
    rows = blob["stage_a"]
    sets = Counter()
    histogram = Counter()
    detail = []
    for record in rows:
        hits = tuple(sorted(k for k, v in record["all_degree3"].items() if v))
        mixed = sum(1 for name in hits
                    if name.startswith("s") and "kappa" in name)
        sets[hits] += 1
        if record["dead_edge"]:
            continue
        histogram[mixed] += 1
        detail.append({"pair": record["pair"], "blocked": record["blocked"],
                       "degree": record["degree"], "hits": list(hits),
                       "mixed_s_kappa": mixed,
                       "slice_dirty": record["monochrome_slice_nonzero"]})
    return {"pattern_sets": {str(k): v for k, v in sets.most_common()},
            "live_mixed_count_histogram": dict(sorted(histogram.items())),
            "pairs": detail}


# --------------------------------------------------------------------- part B


def rcell_source(rng, allow_absent=0.0):
    """An eight-site R_cell source: at most one cell per aggregate block."""
    src = pcore.zero_source()
    cells = {}
    for u, v in combinations(pcore.B, 2):
        if rng.random() < allow_absent:
            cells[(u, v)] = None
            continue
        i, j = rng.randrange(3), rng.randrange(3)
        weight = rng.choice([1, 2, -1, 3, -2])
        src[(u, v)][i][j] = weight
        cells[(u, v)] = (i, j, weight)
    return src, cells


def c3_criterion(cells, colour=None, use_s=False):
    """(C3-kappa) / (C3-s): is there a 3+3 split with the required colours?"""
    if use_s:
        cell = cells[(P, Q)]
        if cell is None:
            return False, []
        want_p, want_q = cell[0], cell[1]
    else:
        want_p = want_q = colour
    good = []
    for X in combinations(U, 3):
        Y = tuple(x for x in U if x not in X)
        ok = True
        for x in X:
            entry = cells[pcore.edge_key(P, x)]
            if entry is None or entry[0] != want_p:
                ok = False
                break
        if ok:
            for y in Y:
                entry = cells[pcore.edge_key(Q, y)]
                if entry is None or entry[0] != want_q:
                    ok = False
                    break
        if ok:
            good.append((X, Y))
    return bool(good), good


def part_b(rng, templates=60):
    stats = {"templates": 0,
             "kappa": {"criterion_and_member": 0, "criterion_not_member": 0,
                       "member_not_criterion": 0, "neither": 0},
             "s3": {"criterion_and_member": 0, "criterion_not_member": 0,
                    "member_not_criterion": 0, "neither": 0},
             "pattern_sets": Counter(),
             "mixed_count_histogram": Counter()}
    examples = []
    for _ in range(templates):
        src, cells = rcell_source(rng, allow_absent=rng.choice([0.0, 0.2, 0.35]))
        cert = blocking_certificate(src, max_degree=3)
        hits = cert.get("all_degree3", {})
        if not hits:
            continue
        stats["templates"] += 1
        names = tuple(sorted(k for k, v in hits.items() if v))
        stats["pattern_sets"][names] += 1
        stats["mixed_count_histogram"][
            sum(1 for n in names if n.startswith("s") and "kappa" in n)] += 1
        for colour in COLORS:
            criterion, _ = c3_criterion(cells, colour=colour)
            member = hits.get(f"kappa_{colour}^3", False)
            key = ("criterion_and_member" if criterion and member else
                   "criterion_not_member" if criterion and not member else
                   "member_not_criterion" if member else "neither")
            stats["kappa"][key] += 1
            if key == "criterion_not_member" and len(examples) < 6:
                examples.append({"kind": "kappa", "colour": colour,
                                 "cells": {str(k): v for k, v in cells.items()}})
        criterion, _ = c3_criterion(cells, use_s=True)
        member = hits.get("s^3", False)
        key = ("criterion_and_member" if criterion and member else
               "criterion_not_member" if criterion and not member else
               "member_not_criterion" if member else "neither")
        stats["s3"][key] += 1
    stats["pattern_sets"] = {str(k): v for k, v
                             in stats["pattern_sets"].most_common(12)}
    stats["mixed_count_histogram"] = dict(sorted(
        stats["mixed_count_histogram"].items()))
    return stats, examples


# --------------------------------------------------------------------- part C


def column_spans(source, p, q):
    """W4's (N): the column spans P = sum_x col(A_px), Q = sum_x col(A_qx)."""
    def span(vertex):
        vectors = []
        for x in range(8):
            if x in (p, q):
                continue
            table = pcore.block
            column = [table(source, vertex, x, i, c)
                      for c in COLORS for i in COLORS]
            for c in COLORS:
                vectors.append([table(source, vertex, x, i, c) for i in COLORS])
        return vectors
    return span(p), span(q)


def contains_axis(vectors, colour):
    """Is e_colour in the span of ``vectors``?  Exact elimination."""
    rows = [[Fraction(x) for x in vector] for vector in vectors if any(vector)]
    target = [Fraction(1 if i == colour else 0) for i in COLORS]
    basis, pivots = [], []
    for row in rows + [target]:
        current = list(row)
        for pivot, base in zip(pivots, basis):
            if current[pivot]:
                factor = current[pivot] / base[pivot]
                current = [a - factor * b for a, b in zip(current, base)]
        pivot = next((n for n, value in enumerate(current) if value), None)
        if pivot is None:
            if row is target:
                return True
            continue
        if row is target:
            return False
        basis.append(current)
        pivots.append(pivot)
    return False


def part_c():
    """(N) on the committed near-exact source, whose mixed system is EXACT."""
    import wsplit_sources as sources
    physical = sources.load_stage_a()
    out = []
    for p, q in combinations(range(8), 2):
        src = sources.rechart(physical, p, q)
        pv, qv = column_spans(src, P, Q)
        record = {"pair": [p, q],
                  "e_c_in_P": [contains_axis(pv, c) for c in COLORS],
                  "e_c_in_Q": [contains_axis(qv, c) for c in COLORS]}
        out.append(record)
    return out


def main():
    args = sys.argv[1:]
    templates = int(args[args.index("--templates") + 1]
                    ) if "--templates" in args else 60
    print("UNAUDITED PROBE (W6) -- J.1c bridge, HEAD 31cefe2", flush=True)
    rng = random.Random(20260815)
    report = {}

    print("== (A) pattern-set co-occurrence ==", flush=True)
    report["h2"] = h2_tables()
    for key, value in report["h2"].items():
        print(f"  h=2 {key}: {value['blocked_live_pairs']} blocked live pairs; "
              f"#s*kappa histogram {value['s_kappa_count_histogram']}; "
              f">=2 s*kappa: {value['at_least_two_s_kappa']}")
    report["h3_stage_a"] = h3_stage_a_table()
    print(f"  h=3 near-exact source: mixed(s*kappa) count histogram "
          f"{report['h3_stage_a']['live_mixed_count_histogram']}")
    for key, value in report["h3_stage_a"]["pattern_sets"].items():
        print(f"    {value:2d} x {key}")

    print("== (B) the h=3 analogue of (C) in R_cell ==", flush=True)
    stats, examples = part_b(rng, templates)
    report["h3_rcell"] = stats
    report["h3_rcell_examples"] = examples
    print(f"  templates {stats['templates']}")
    print(f"  kappa_c^3: {json.dumps(stats['kappa'])}")
    print(f"  s^3      : {json.dumps(stats['s3'])}")
    print(f"  mixed-pattern count histogram {stats['mixed_count_histogram']}")
    for key, value in list(stats["pattern_sets"].items())[:8]:
        print(f"    {value:3d} x {key}")

    print("== (C) W4's (N) on the near-exact source (mixed system exact) ==",
          flush=True)
    report["condition_N"] = part_c()
    both = sum(1 for r in report["condition_N"]
               if all(r["e_c_in_P"]) and all(r["e_c_in_Q"]))
    print(f"  pairs where every e_c lies in BOTH column spans: {both}/28")
    for record in report["condition_N"][:8]:
        print(f"    pair {record['pair']}: e_c in P {record['e_c_in_P']}, "
              f"e_c in Q {record['e_c_in_Q']}")

    with open("results_bridge.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print("wrote results_bridge.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
