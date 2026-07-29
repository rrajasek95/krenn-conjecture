#!/usr/bin/env python3
"""Attempt the first off-diagonal lift of the diagonal P^2 certificate.

Filter by the number of bichromatic source variables.  Degree one is empty
in the target multigrading.  This script constructs only the connected
components of the degree-two leading Macaulay map that meet the remainder of
a concrete diagonal certificate, avoiding the 312,975,000 raw degree-two
monomials.
"""

from __future__ import annotations

import itertools
from collections import Counter, deque
from functools import lru_cache
from pathlib import Path

from test_diagonal_power2 import (
    COLOR_PERMS,
    EDGES,
    EDGE_INDEX,
    PM,
    VERTEX_PERMS,
    add_matching,
    build_matrix,
    decode,
    encode,
    modular_membership,
    transform_coloring,
    transform_graph,
)


PRIME = 1009
COLOR_TYPES = (
    (0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, 1, 1),
    (0, 0, 0, 0, 1, 2),
    (0, 0, 0, 1, 1, 1),
    (0, 0, 0, 1, 1, 2),
    (0, 0, 1, 1, 2, 2),
)
TYPE_SET = set(COLOR_TYPES)


# Off-diagonal variables retain endpoint order u<v.
OFF_VARS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a in range(3)
    for b in range(3)
    if a != b
)
OFF_INDEX = {x: i for i, x in enumerate(OFF_VARS)}


def moved_var(x, vp, cp):
    u, v, a, b = x
    uu, vv, aa, bb = vp[u], vp[v], cp[a], cp[b]
    if uu > vv:
        uu, vv, aa, bb = vv, uu, bb, aa
    return uu, vv, aa, bb


ACTIONS = []
for vi, vp in enumerate(VERTEX_PERMS):
    for cp in COLOR_PERMS:
        om = tuple(OFF_INDEX[moved_var(x, vp, cp)] for x in OFF_VARS)
        ACTIONS.append((vi, vp, cp, om))
assert len(ACTIONS) == 4320


def transform_off(off, action_index):
    om = ACTIONS[action_index][3]
    return tuple(sorted(om[i] for i in off))


@lru_cache(None)
def off_canonicalizers(off):
    best = None
    choices = []
    for gi in range(len(ACTIONS)):
        z = transform_off(off, gi)
        if best is None or z < best:
            best, choices = z, [gi]
        elif z == best:
            choices.append(gi)
    return best, tuple(choices)


def transform_diag_triple(gs, gi):
    vi, _, cp, _ = ACTIONS[gi]
    out = [None] * 3
    for a in range(3):
        out[cp[a]] = transform_graph(gs[a], vi)
    return tuple(out)


@lru_cache(None)
def canonical_row(off, gs):
    off0, choices = off_canonicalizers(off)
    return off0, min(transform_diag_triple(gs, gi) for gi in choices)


@lru_cache(None)
def coloring_canonicalizers(c):
    choices = []
    for gi, (_, vp, cp, _) in enumerate(ACTIONS):
        cc = transform_coloring(c, vp, cp)
        if cc in TYPE_SET:
            choices.append((cc, gi))
    assert choices and len({cc for cc, _ in choices}) == 1
    return tuple(choices)


@lru_cache(None)
def canonical_column(c, off, gs):
    choices = coloring_canonicalizers(c)
    cc = choices[0][0]
    best = None
    for _, gi in choices:
        z = (transform_off(off, gi), transform_diag_triple(gs, gi))
        if best is None or z < best:
            best = z
    return cc, best[0], best[1]


def min_cross_degree(c):
    odd = sum(c.count(a) % 2 for a in range(3))
    assert odd in (0, 2)
    return odd // 2


def term_variables(c, pm):
    return tuple((u, v, c[u], c[v]) for u, v in pm)


def add_term(off, gs, term):
    off = list(off)
    xs = [list(decode(z)) for z in gs]
    for u, v, a, b in term:
        if a == b:
            xs[a][EDGE_INDEX[u, v]] += 1
            assert xs[a][EDGE_INDEX[u, v]] <= 2
        else:
            off.append(OFF_INDEX[u, v, a, b])
    return tuple(sorted(off)), tuple(encode(x) for x in xs)


def remove_term(off, gs, term):
    off = list(off)
    xs = [list(decode(z)) for z in gs]
    for u, v, a, b in term:
        if a == b:
            k = EDGE_INDEX[u, v]
            assert xs[a][k] > 0
            xs[a][k] -= 1
        else:
            k = OFF_INDEX[u, v, a, b]
            off.remove(k)
    return tuple(sorted(off)), tuple(encode(x) for x in xs)


def variables_by_underlying_pair(row):
    off, gs = row
    ans = {e: [] for e in EDGES}
    for a, z in enumerate(gs):
        for k, mult in enumerate(decode(z)):
            if mult:
                u, v = EDGES[k]
                ans[u, v].append((u, v, a, a))
    for k in set(off):
        u, v, a, b = OFF_VARS[k]
        ans[u, v].append((u, v, a, b))
    return ans


@lru_cache(None)
def incident_leading_columns(row):
    by_pair = variables_by_underlying_pair(row)
    out = set()
    for pm in PM:
        choices = [by_pair[e] for e in pm]
        if any(not z for z in choices):
            continue
        for term in itertools.product(*choices):
            c = [None] * 6
            for u, v, a, b in term:
                c[u], c[v] = a, b
            c = tuple(c)
            if len(set(c)) == 1:
                continue
            cross = sum(a != b for _, _, a, b in term)
            if cross != min_cross_degree(c):
                continue
            qoff, qgs = remove_term(*row, term)
            out.add(canonical_column(c, qoff, qgs))
    return tuple(out)


@lru_cache(None)
def leading_outputs(col):
    c, off, gs = col
    r0 = min_cross_degree(c)
    out = []
    for pm in PM:
        term = term_variables(c, pm)
        if sum(a != b for _, _, a, b in term) != r0:
            continue
        out.append(canonical_row(*add_term(off, gs, term)))
    return tuple(out)


def diagonal_remainder():
    d = build_matrix(Path("/tmp/diagonal_power2_v2.pkl"))
    ok, solution, pivot_columns = modular_membership(d, PRIME, True)
    assert ok
    rhs2 = Counter()
    rhs3 = Counter()
    for j, z in solution.items():
        c, gs = d["column_reps"][j]
        for pm in PM:
            term = term_variables(c, pm)
            cross = sum(a != b for _, _, a, b in term)
            if not cross:
                continue
            row = canonical_row(*add_term((), gs, term))
            (rhs2 if cross == 2 else rhs3)[row] = (
                (rhs2 if cross == 2 else rhs3)[row] + z
            ) % PRIME
    rhs2 = Counter({r: z for r, z in rhs2.items() if z})
    rhs3 = Counter({r: z for r, z in rhs3.items() if z})
    print(f"diagonal lift remainder: k2 orbits={len(rhs2)}, k3 orbits={len(rhs3)}")
    return rhs2, rhs3, d, pivot_columns


def component_closure(starts):
    rows = set(starts)
    cols = set()
    queue = deque(starts)
    while queue:
        row = queue.popleft()
        for col in incident_leading_columns(row):
            if col in cols:
                continue
            cols.add(col)
            for rr in leading_outputs(col):
                if rr not in rows:
                    rows.add(rr)
                    queue.append(rr)
        if len(rows) % 1000 == 0:
            print(f"closure rows={len(rows)}, cols={len(cols)}, queue={len(queue)}")
    print(f"closed component union: rows={len(rows)}, cols={len(cols)}")
    return rows, cols


@lru_cache(None)
def monomial_killed(row):
    # A one-term leading column is exactly a 2+2+2 coloring whose unique
    # degree-minimal matching consists of three diagonal edges, one of each
    # color.  Test the 15 vertex matchings and six color assignments directly;
    # this is far cheaper than enumerating every incident column.
    _, gs = row
    exps = tuple(decode(z) for z in gs)
    for pm in PM:
        edge_ids = tuple(EDGE_INDEX[e] for e in pm)
        for colors in itertools.permutations(range(3)):
            if all(exps[a][k] for a, k in zip(colors, edge_ids)):
                return True
    return False


@lru_cache(None)
def monomial_column(row):
    """Return a one-term 2+2+2 leading column for a cone row, or None."""
    _, gs = row
    exps = tuple(decode(z) for z in gs)
    for pm in PM:
        edge_ids = tuple(EDGE_INDEX[e] for e in pm)
        for colors in itertools.permutations(range(3)):
            if not all(exps[a][k] for a, k in zip(colors, edge_ids)):
                continue
            c = [None] * 6
            term = []
            for (u, v), a in zip(pm, colors):
                c[u] = c[v] = a
                term.append((u, v, a, a))
            qoff, qgs = remove_term(*row, tuple(term))
            col = canonical_column(tuple(c), qoff, qgs)
            assert len(leading_outputs(col)) == 1
            return col
    return None


def quotient_component_closure(starts):
    """Close only after quotienting rows hit by one-term 2+2+2 columns."""
    starts = tuple(r for r in starts if not monomial_killed(r))
    rows = set(starts)
    cols = set()
    queue = deque(starts)
    while queue:
        row = queue.popleft()
        for col in incident_leading_columns(row):
            outputs = leading_outputs(col)
            if len(outputs) == 1 or col in cols:
                continue
            cols.add(col)
            for rr in outputs:
                if monomial_killed(rr):
                    continue
                if rr not in rows:
                    rows.add(rr)
                    queue.append(rr)
        if len(rows) and len(rows) % 500 == 0:
            print(
                f"quotient closure rows={len(rows)}, cols={len(cols)}, queue={len(queue)}",
                flush=True,
            )
    print(f"quotient component: rows={len(rows)}, cols={len(cols)}", flush=True)
    return rows, cols


def solve_component(rhs, rows, cols):
    row_list = tuple(sorted(rows))
    row_index = {r: i for i, r in enumerate(row_list)}
    pivots = {}
    for k, col in enumerate(cols):
        v = Counter(row_index[r] for r in leading_outputs(col) if r in row_index)
        v = {i: z % PRIME for i, z in v.items() if z % PRIME}
        while v:
            i = min(v)
            a = v[i]
            if i not in pivots:
                inv = pow(a, PRIME - 2, PRIME)
                pivots[i] = {j: z * inv % PRIME for j, z in v.items() if z % PRIME}
                break
            p = pivots[i]
            for j, z in p.items():
                w = (v.get(j, 0) - a * z) % PRIME
                if w:
                    v[j] = w
                elif j in v:
                    del v[j]
        if (k + 1) % 1000 == 0:
            print(f"eliminate cols={k+1}, rank={len(pivots)}")
    v = {row_index[r]: (-z) % PRIME for r, z in rhs.items() if z % PRIME}
    while v:
        i = min(v)
        a = v[i]
        if i not in pivots:
            break
        for j, z in pivots[i].items():
            w = (v.get(j, 0) - a * z) % PRIME
            if w:
                v[j] = w
            elif j in v:
                del v[j]
    print(f"k2 remainder in leading span={not v}, rank={len(pivots)}, residual={len(v)}")
    return not v


def peel_component(rows, cols):
    """Look for a unitriangular certificate by singleton-column peeling."""
    live_rows = set(rows)
    supports = {}
    row_cols = {r: set() for r in rows}
    queue = deque()
    for col in cols:
        supp = Counter(r for r in leading_outputs(col) if r in live_rows)
        supp = {r: a for r, a in supp.items() if a}
        supports[col] = supp
        for r in supp:
            row_cols[r].add(col)
        if len(supp) == 1:
            queue.append(col)
    pivots = []
    while queue:
        col = queue.popleft()
        supp = supports[col]
        if len(supp) != 1:
            continue
        row, coeff = next(iter(supp.items()))
        if row not in live_rows:
            continue
        pivots.append((row, col, coeff))
        live_rows.remove(row)
        for other in tuple(row_cols[row]):
            ss = supports[other]
            ss.pop(row, None)
            if len(ss) == 1:
                queue.append(other)
        if len(pivots) % 500 == 0:
            print(f"peeled={len(pivots)}, remaining={len(live_rows)}", flush=True)
    print(
        f"singleton peel rank certificate={len(pivots)}/{len(rows)}, "
        f"remaining={len(live_rows)}",
        flush=True,
    )
    return pivots, live_rows


if __name__ == "__main__":
    rhs2, rhs3, _, _ = diagonal_remainder()
    rhs2q = Counter({r: z for r, z in rhs2.items() if not monomial_killed(r)})
    print(f"k2 rhs after monomial quotient={len(rhs2q)}", flush=True)
    rows, cols = quotient_component_closure(rhs2q)
    peel_component(rows, cols)
    solve_component(rhs2q, rows, cols)
