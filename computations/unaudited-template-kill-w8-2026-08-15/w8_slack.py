#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- W9's overdetermination slack, applied to W8's
admissible templates and (above all) to W8's SURVIVORS.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

W9 (computations/unaudited-cell-ceiling-w9-2026-08-15/REPORT.md, task B5):
gauge multiplies H(c^N) by prod_u d_{u,c} and preserves the mixed zeros, so a
nonempty exact locus with template T carries a component of dimension at least
r(T) - 3, where r(T) is the rank of the cell/slot incidence matrix (the
Sigma x 24 matrix with a 1 in slot (u,i) and slot (v,j) for the cell (uv,i,j)).
At a smooth point the Jacobian rank therefore obeys J <= Sigma - r + 3, and

        slack(T) = Sigma - r(T) + 3 - J(T)

is negative exactly when the template is value-level overdetermined.  W9
measures +19 on the object that exists and -11...-14 on band templates.

THIS IS A DIAGNOSTIC, NOT A VERDICT.  J(T) is the rank of the Jacobian of the
exactness map at a random point of the template torus, computed exactly modulo
a prime (a lower bound on the generic rank over Q, so `slack` is an UPPER
bound on the true slack -- the conservative direction for reading a negative
slack as "overdetermined").  Several random points are used and the largest
rank is kept.

Run: python3 w8_slack.py
"""

from __future__ import annotations

import glob
import json
import sys

import numpy as np

import w8_core as C

PRIME = 65521


def cell_list(template):
    out = []
    for e, mask in enumerate(template):
        for k in range(9):
            if (mask >> k) & 1:
                out.append((e, k // 3, k % 3))
    return out


def incidence_rank(geo, template):
    cells = cell_list(template)
    matrix = np.zeros((len(cells), 24), dtype=np.int64)
    for row, (e, i, j) in enumerate(cells):
        u, v = geo.edges[e]
        matrix[row, 3 * u + i] += 1
        matrix[row, 3 * v + j] += 1
    return rank_mod(matrix), len(cells)


def rank_mod(matrix, prime=PRIME):
    a = np.mod(matrix.astype(np.int64), prime)
    rows, cols = a.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for r in range(rank, rows):
            if a[r, col] % prime:
                pivot = r
                break
        if pivot is None:
            continue
        a[[rank, pivot]] = a[[pivot, rank]]
        inverse = pow(int(a[rank, col]), prime - 2, prime)
        a[rank] = (a[rank] * inverse) % prime
        column = a[rank + 1:, col].copy()
        nz = np.nonzero(column)[0]
        if len(nz):
            a[rank + 1 + nz] = (a[rank + 1 + nz]
                                - np.outer(column[nz], a[rank])) % prime
        rank += 1
        if rank == rows:
            break
    return rank


def jacobian_rank(geo, template, trials=3, seed=20260815):
    cells = cell_list(template)
    index = {(e, i, j): n for n, (e, i, j) in enumerate(cells)}
    compat = C.compat_matrix(geo, template)
    table = C.fibre_table(geo, template, compat)
    rng = np.random.default_rng(seed)
    best = 0
    for _ in range(trials):
        values = rng.integers(1, PRIME, size=len(cells), dtype=np.int64)
        rows = []
        for w, members in table.items():
            word = geo.words[w]
            row = np.zeros(len(cells), dtype=np.int64)
            for mnum in members:
                positions = []
                for e in geo.matching_edges[mnum]:
                    u, v = geo.edges[e]
                    positions.append(index[(e, word[u], word[v])])
                for p in positions:
                    product = 1
                    for q in positions:
                        if q != p:
                            product = product * int(values[q]) % PRIME
                    row[p] = (row[p] + product) % PRIME
            rows.append(row)
        best = max(best, rank_mod(np.array(rows, dtype=np.int64)))
    return best, len(table)


def slack(geo, template, trials=3):
    r, sigma = incidence_rank(geo, template)
    j, equations = jacobian_rank(geo, template, trials)
    return {"sigma": sigma, "r": r, "J": j, "budget": sigma - r + 3,
            "slack": sigma - r + 3 - j, "live_words": equations}


def collect():
    """(label, template) pairs from every W8 result file."""
    out = []
    for name in sorted(glob.glob("results_*.json")):
        try:
            data = json.load(open(name))
        except Exception:
            continue
        if name == "results_immunity.json":
            for row in data["results"]:
                out.append((f"immune-construction m={row['m']}",
                            tuple(row["template"])))
        elif "rows" in data and isinstance(data["rows"], list):
            for row in data["rows"]:
                for t in (row.get("survivors") or []):
                    out.append((f"{name}:orbit{row.get('orbit')}", tuple(t)))
                if "template" in row and isinstance(row["template"], list):
                    out.append((f"{name}", tuple(row["template"])))
        for t in (data.get("found") or []):
            out.append((name, tuple(t)))
        for t in (data.get("survivors") or []):
            out.append((f"{name}:SURVIVOR", tuple(t)))
    seen, unique = set(), []
    for label, t in out:
        if len(t) == 28 and t not in seen:
            seen.add(t)
            unique.append((label, t))
    return unique


def main():
    geo = C.geometry(8)
    rows = []
    for label, template in collect():
        audit = C.audit(geo, template)
        if not audit["fie"] or audit["mixed_singletons"]:
            continue
        cert = C.analyse(geo, template)
        data = slack(geo, template)
        data.update({"label": label, "m": audit["m"], "beta": audit["beta"],
                     "thin": audit["thin"], "fat": audit["fat"],
                     "verdict": cert["verdict"]})
        rows.append(data)
        print(f"  {label[:46]:<46} m={data['m']:2d} Sigma={data['sigma']:3d} "
              f"r={data['r']:2d} J={data['J']:3d} budget={data['budget']:3d} "
              f"slack={data['slack']:4d}  {data['verdict']}", flush=True)
    rows.sort(key=lambda r: r["slack"])
    json.dump({"rows": rows, "prime": PRIME}, open("results_slack.json", "w"),
              indent=1)
    positive = [r for r in rows if r["slack"] >= 0]
    print(f"\ntemplates measured: {len(rows)}; nonnegative slack "
          f"(escalation signal): {len(positive)}")
    print("wrote results_slack.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
