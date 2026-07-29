#!/usr/bin/env python3
"""Empirically search for a well-founded measure behind the filtered DFS.

This is a diagnostic, not part of the membership certificate.  It replays a
prefix of one checkpoint layer, records the selected leading rewrites, and
tests several invariant/canonical row orders on every dependency edge.
"""

from __future__ import annotations

import argparse
import itertools
import pickle
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

sys.setrecursionlimit(200_000)
sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

import lift_power2_offdiag2 as L


def cross_counts(row):
    counts = Counter()
    for i in row[0]:
        _, _, a, b = L.OFF_VARS[i]
        counts[tuple(sorted((a, b)))] += 1
    return tuple(counts[(a, b)] for a, b in ((0, 1), (0, 2), (1, 2)))


def matching_number(edges):
    best = 0
    edge_set = set(edges)
    for pm in L.PM:
        best = max(best, sum(e in edge_set for e in pm))
    return best


@lru_cache(None)
def signatures(row):
    off, gs = row
    decoded = tuple(L.decode(z) for z in gs)
    diag_counts = tuple(sum(x) for x in decoded)
    diag_supports = tuple(sum(x > 0 for x in xs) for xs in decoded)
    diag_match = tuple(
        matching_number(L.EDGES[i] for i, x in enumerate(xs) if x)
        for xs in decoded
    )
    rainbow2 = 0
    rainbow2_weighted = 0
    for a in range(3):
        for b in range(a + 1, 3):
            for i, x in enumerate(decoded[a]):
                if not x:
                    continue
                e = set(L.EDGES[i])
                for j, y in enumerate(decoded[b]):
                    if y and e.isdisjoint(L.EDGES[j]):
                        rainbow2 += 1
                        rainbow2_weighted += x * y
    vertex_color_degrees = []
    for v in range(6):
        vertex_color_degrees.append(
            tuple(
                sum(decoded[a][L.EDGE_INDEX[tuple(sorted((u, v)))]] for u in range(6) if u != v)
                for a in range(3)
            )
        )
    e = cross_counts(row)
    # All signatures are invariant under global color permutation except the
    # final two canonical-coordinate orders.
    base = {
        "cross_sorted": tuple(sorted(e)),
        "cross_sorted_rev": tuple(sorted(e, reverse=True)),
        "diag_sorted": tuple(sorted(diag_counts)),
        "diag_sorted_rev": tuple(sorted(diag_counts, reverse=True)),
        "diag_support_sorted": tuple(sorted(diag_supports)),
        "diag_match_sorted": tuple(sorted(diag_match)),
        "rainbow2": rainbow2,
        "rainbow2_weighted": rainbow2_weighted,
        "vertex_color_degrees": tuple(sorted(vertex_color_degrees)),
        "off_lex": off,
        "row_lex": row,
    }
    base.update(
        {
            "rainbow2_then_row": (rainbow2, row),
            "neg_rainbow2_then_row": (-rainbow2, row),
            "support_then_row": (tuple(sorted(diag_supports)), row),
            "neg_support_then_row": (tuple(-x for x in sorted(diag_supports)), row),
            "match_then_row": (tuple(sorted(diag_match)), row),
            "neg_match_then_row": (tuple(-x for x in sorted(diag_match)), row),
            "neg_support_then_reverse_row": (
                tuple(-x for x in sorted(diag_supports)),
                tuple(-x for x in off),
                tuple(-x for x in gs),
            ),
            "support_then_reverse_row": (
                tuple(sorted(diag_supports)),
                tuple(-x for x in off),
                tuple(-x for x in gs),
            ),
            "neg_support_neg_rainbow2_row": (
                tuple(-x for x in sorted(diag_supports)),
                -rainbow2,
                row,
            ),
            "neg_support_neg_rainbow2_reverse_row": (
                tuple(-x for x in sorted(diag_supports)),
                -rainbow2,
                tuple(-x for x in off),
                tuple(-x for x in gs),
            ),
            "neg_support_rainbow2_reverse_row": (
                tuple(-x for x in sorted(diag_supports)),
                rainbow2,
                tuple(-x for x in off),
                tuple(-x for x in gs),
            ),
            "neg_support_rainbow2_row": (
                tuple(-x for x in sorted(diag_supports)),
                rainbow2,
                row,
            ),
            "neg_rainbow2_neg_support_row": (
                -rainbow2,
                tuple(-x for x in sorted(diag_supports)),
                row,
            ),
            "rainbow2_neg_support_row": (
                rainbow2,
                tuple(-x for x in sorted(diag_supports)),
                row,
            ),
        }
    )
    return base


def replay(starts, limit):
    assigned = {}
    used_columns = set()
    visiting = set()
    calls = 0

    def prove(row):
        nonlocal calls
        calls += 1
        if L.monomial_killed(row) or row in assigned:
            return True
        if row in visiting:
            return False
        visiting.add(row)
        options = []
        for col in L.incident_leading_columns(row):
            if col in used_columns:
                continue
            deps = {
                rr
                for rr in L.leading_outputs(col)
                if rr != row and not L.monomial_killed(rr)
            }
            options.append((len(deps), col, tuple(sorted(deps))))
        options.sort(key=lambda z: (z[0], z[1]))
        for _, col, deps in options:
            if col in used_columns:
                continue
            if all(prove(rr) for rr in deps):
                if col in used_columns:
                    continue
                assigned[row] = (col, deps)
                used_columns.add(col)
                visiting.remove(row)
                return True
        visiting.remove(row)
        return False

    survivors = [r for r in starts if not L.monomial_killed(r)]
    for i, row in enumerate(survivors[:limit], 1):
        if not prove(row):
            raise RuntimeError(f"failed at survivor start {i}")
        if i % 100 == 0:
            print(f"starts={i}, assigned={len(assigned)}, calls={calls}", flush=True)
    return assigned, calls


def describe_row(row):
    off, gs = row
    off_vars = tuple(L.OFF_VARS[i] for i in off)
    diag = []
    for a, z in enumerate(gs):
        for i, mult in enumerate(L.decode(z)):
            if mult:
                diag.append((a, L.EDGES[i], mult))
    return {"off": off_vars, "diag": tuple(diag)}


def exponent_vector(row):
    out = np.zeros(len(L.OFF_VARS) + 3 * len(L.EDGES), dtype=float)
    for i in row[0]:
        out[i] += 1
    for a, z in enumerate(row[1]):
        out[len(L.OFF_VARS) + a * len(L.EDGES) : len(L.OFF_VARS) + (a + 1) * len(L.EDGES)] = L.decode(z)
    return out


def fit_additive_weight(assigned):
    constraints = []
    for row, (_, deps) in assigned.items():
        vr = exponent_vector(row)
        constraints.extend(vr - exponent_vector(dep) for dep in deps)
    if not constraints:
        print("additive_weight: vacuous")
        return
    diffs = np.vstack(constraints)
    result = linprog(
        np.zeros(diffs.shape[1]),
        A_ub=-diffs,
        b_ub=-np.ones(diffs.shape[0]),
        bounds=[(None, None)] * diffs.shape[1],
        method="highs",
    )
    print(
        f"additive_weight: success={result.success}, constraints={len(diffs)}, "
        f"status={result.message}"
    )
    if result.success:
        w = result.x
        margins = diffs @ w
        nz = [(i, round(x, 6)) for i, x in enumerate(w) if abs(x) > 1e-8]
        print(f"additive_weight: min_margin={margins.min():.6g}, nonzero={nz}")


def compare(a, b):
    return -1 if a < b else 1 if a > b else 0


def search_orders(assigned):
    """Search short lexicographic combinations of natural graph features."""
    feature_names = (
        "diag_support_sorted",
        "rainbow2",
        "rainbow2_weighted",
        "diag_match_sorted",
        "vertex_color_degrees",
        "off_lex",
    )
    rows_and_options = []
    for row in assigned:
        options = []
        for col in L.incident_leading_columns(row):
            deps = tuple(
                rr
                for rr in set(L.leading_outputs(col))
                if rr != row and not L.monomial_killed(rr)
            )
            options.append(deps)
        if not any(not deps for deps in options):
            rows_and_options.append((row, options))
    print(f"measure_search: non-direct rows={len(rows_and_options)}")

    best = []
    for length in range(0, 4):
        for names in itertools.permutations(feature_names, length):
            for signs in itertools.product((-1, 1), repeat=length + 1):
                spec = tuple(zip(names + ("row_lex",), signs))
                failures = 0
                for row, options in rows_and_options:
                    sr = signatures(row)
                    succeeds = False
                    for deps in options:
                        option_ok = True
                        for dep in deps:
                            sd = signatures(dep)
                            direction = 0
                            for name, sign in spec:
                                direction = sign * compare(sd[name], sr[name])
                                if direction:
                                    break
                            if direction >= 0:
                                option_ok = False
                                break
                        if option_ok:
                            succeeds = True
                            break
                    if not succeeds:
                        failures += 1
                        if len(best) >= 20 and failures > best[-1][0]:
                            break
                best.append((failures, spec))
                best.sort(key=lambda z: (z[0], z[1]))
                del best[20:]
    print("measure_search best:")
    for failures, spec in best:
        print(f"  failures={failures}, order={spec}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--after", type=int, default=3)
    parser.add_argument("--degree", type=int, default=4)
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--search-orders", action="store_true")
    args = parser.parse_args()
    path = Path(f"/tmp/krenn_p2_filter_after{args.after}.pkl")
    with path.open("rb") as fh:
        saved = pickle.load(fh)
    starts = saved["supports"][args.degree]
    print(f"checkpoint={path}, starts={len(starts)}", flush=True)
    assigned, calls = replay(starts, args.limit)

    comparisons = {name: Counter() for name in signatures(next(iter(assigned)))}
    monotone_options = {name: Counter() for name in comparisons}
    type_counts = Counter()
    dep_counts = Counter()
    heights = {}
    edges = 0
    for row, (col, deps) in assigned.items():
        # Dict insertion order is the recursive postorder: every dependency
        # has already been assigned (or is a cone of height zero).
        heights[row] = 1 + max((heights.get(dep, 0) for dep in deps), default=0)
        type_counts[tuple(sorted(Counter(col[0]).values(), reverse=True))] += 1
        dep_counts[len(deps)] += 1
        sr = signatures(row)
        option_deps = []
        for candidate in L.incident_leading_columns(row):
            ds = {
                rr
                for rr in L.leading_outputs(candidate)
                if rr != row and not L.monomial_killed(rr)
            }
            option_deps.append(ds)
        for name in monotone_options:
            has_down = any(all(signatures(dep)[name] < sr[name] for dep in ds) for ds in option_deps)
            has_up = any(all(signatures(dep)[name] > sr[name] for dep in ds) for ds in option_deps)
            monotone_options[name]["down" if has_down else "no_down"] += 1
            monotone_options[name]["up" if has_up else "no_up"] += 1
        inspect_name = "neg_support_then_row"
        if args.inspect and not any(
            all(signatures(dep)[inspect_name] < sr[inspect_name] for dep in ds)
            for ds in option_deps
        ):
            print(f"NO_DOWN {inspect_name}: row={describe_row(row)}")
            print(f"  signature={sr[inspect_name]}")
            for candidate, ds in zip(L.incident_leading_columns(row), option_deps):
                vals = [signatures(dep)[inspect_name] for dep in ds]
                print(
                    "  option",
                    tuple(sorted(Counter(candidate[0]).values(), reverse=True)),
                    "deps=", len(ds),
                    "values=", vals,
                )
                if len(ds) == 1:
                    dep = next(iter(ds))
                    sdep = signatures(dep)
                    print(
                        "    singleton comparisons=",
                        {
                            name: (-1 if sdep[name] < sr[name] else 1 if sdep[name] > sr[name] else 0)
                            for name in sr
                        },
                    )
        for dep in deps:
            edges += 1
            sd = signatures(dep)
            for name in comparisons:
                comparisons[name]["lt" if sd[name] < sr[name] else "gt" if sd[name] > sr[name] else "eq"] += 1
    print(f"assigned={len(assigned)}, dependency_edges={edges}, calls={calls}")
    print(f"generator_types={dict(type_counts)}")
    print(f"dependency_counts={dict(dep_counts)}")
    print(
        f"attractor_heights=max {max(heights.values(), default=0)}, "
        f"distribution={dict(Counter(heights.values()))}"
    )
    fit_additive_weight(assigned)
    if args.search_orders:
        search_orders(assigned)
    for name, counts in comparisons.items():
        print(f"{name}: {dict(counts)}")
        print(f"{name}_options: {dict(monotone_options[name])}")


if __name__ == "__main__":
    main()
