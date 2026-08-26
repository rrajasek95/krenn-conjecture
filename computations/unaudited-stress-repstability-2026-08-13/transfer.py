#!/usr/bin/env python3
"""The centered occurrence transfer of
notes/uniform-centered-occurrence-full-endpoint-transfer-gate.md, rebuilt
independently, with an exact chart-preimage routine so that the Gram row can
be computed at orders the committed checker never reaches, and so that the
TWO-step (iterated) transfer is computable at all.

Gram row of the marked occurrence f:      k_f(g) = sum_charts m_c(f) m_c(g).
Two-step row:                             k2_f(g) = sum_{c1,c2} m(f) m(g).
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations

from lib_stress import charts, edge, extend, occurrences, occurrence_count


def preimages(target, chart, small_sites):
    """All small occurrences x on `small_sites` with extend(x, chart) == target.

    Derived from the inverse of each insertion rule; every returned candidate
    is re-verified with `extend`, and `t2_transfer_residuals.py` cross-checks
    the whole routine against brute force at small orders.
    """
    p, s, matching = target
    pair, kind, new, bridge = chart
    small = set(small_sites)
    answer = []
    if kind == "residual":
        e = edge(new, bridge)
        if e in matching and p in small and s in small:
            answer.append((p, s, tuple(v for v in matching if v != e)))
    elif kind == "p":
        if p == new and s in small:
            for e in matching:
                if bridge in e:
                    w = e[0] if e[1] == bridge else e[1]
                    if w in small and w != s:
                        answer.append((w, s, tuple(v for v in matching if v != e)))
    elif kind == "s":
        if s == new and p in small:
            for e in matching:
                if bridge in e:
                    w = e[0] if e[1] == bridge else e[1]
                    if w in small and w != p:
                        answer.append((p, w, tuple(v for v in matching if v != e)))
    else:
        assert kind == "both"
        if (p, s) == (new, bridge):
            for e in matching:
                if e[0] in small and e[1] in small:
                    rest = tuple(v for v in matching if v != e)
                    answer.append((e[0], e[1], rest))
                    answer.append((e[1], e[0], rest))
    for x in answer:
        assert extend(x, chart) == target, ("preimage rule broken", x, chart, target)
        assert set((x[0], x[1])) | {v for e in x[2] for v in e} <= small
    return answer


def chart_image(small_sites, chart, cache):
    key = tuple(small_sites)
    if key not in cache:
        cache[key] = occurrences(small_sites)
    image = Counter()
    for x in cache[key]:
        image[extend(x, chart)] += 1
    return image


def one_step_row(h, marked, big_sites, cache=None):
    """k_f as a Counter over occurrences of order h+1, plus diagnostics."""
    cache = {} if cache is None else cache
    row = Counter()
    total_columns = 0
    for chart in charts(big_sites):
        small_sites = tuple(v for v in big_sites if v not in chart[0])
        pre = preimages(marked, chart, small_sites)
        if not pre:
            continue
        multiplicity = len(pre)
        total_columns += multiplicity
        image = chart_image(small_sites, chart, cache)
        assert sum(image.values()) == occurrence_count(h)
        assert image[marked] == multiplicity
        for g, value in image.items():
            row[g] += multiplicity * value
    return row, total_columns


def two_step_row(h, marked, big_sites):
    """k2_f over occurrences of order h+2 for the iterated transfer."""
    cache = {}
    weights = Counter()
    for chart2 in charts(big_sites):
        mid_sites = tuple(v for v in big_sites if v not in chart2[0])
        pre2 = preimages(marked, chart2, mid_sites)
        if not pre2:
            continue
        for chart1 in charts(mid_sites):
            small_sites = tuple(v for v in mid_sites if v not in chart1[0])
            count = 0
            for y in pre2:
                count += len(preimages(y, chart1, small_sites))
            if count:
                weights[(chart2, chart1)] += count
    row = Counter()
    for (chart2, chart1), multiplicity in weights.items():
        mid_sites = tuple(v for v in big_sites if v not in chart2[0])
        small_sites = tuple(v for v in mid_sites if v not in chart1[0])
        key = tuple(small_sites)
        if key not in cache:
            cache[key] = occurrences(small_sites)
        for x in cache[key]:
            row[extend(extend(x, chart1), chart2)] += multiplicity
    return row, sum(weights.values())


def n_step_row(h, steps, marked, big_sites):
    """Gram row of the `steps`-fold composite transfer, order h -> h+steps."""
    chains = [((), [marked], big_sites)]
    for level in range(steps):
        nxt = []
        for prefix, targets, sites in chains:
            for chart in charts(sites):
                small_sites = tuple(v for v in sites if v not in chart[0])
                pre = []
                for t in targets:
                    pre.extend(preimages(t, chart, small_sites))
                if pre:
                    nxt.append((prefix + (chart,), pre, small_sites))
        chains = nxt
    cache = {}
    row = Counter()
    total = 0
    for chart_chain, pre, small_sites in chains:
        multiplicity = len(pre)
        total += multiplicity
        key = tuple(small_sites)
        if key not in cache:
            cache[key] = occurrences(small_sites)
        for x in cache[key]:
            g = x
            for chart in reversed(chart_chain):
                g = extend(g, chart)
            row[g] += multiplicity
    return row, total
