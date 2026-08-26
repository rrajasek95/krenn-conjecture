#!/usr/bin/env python3
"""Audit named m=25..28 endpoint-cell supports against honest source filters.

The templates are restated verbatim from the W8/W15 residual family, but no
code from that family is imported.  They are support-level controls only.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
COLORS = (0, 1, 2)
EDGES = tuple(itertools.combinations(range(8), 2))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(matchings(range(8)))
require(len(MATCHINGS) == 105, "matching census")
EIDX = {edge: i for i, edge in enumerate(EDGES)}


TEMPLATES = {
    25: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511),
    26: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 0, 511, 511, 0, 511),
    27: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 0, 511),
    28: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511, 8, 511,
         128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 511, 511),
}


# Positive integer Stiemke weights in occupied-cell order: edge index first,
# then cell index 3*i+j.  These are frozen witnesses, not solver output at
# replay time.  Sparse overrides keep the certificates reviewable.
def weights(length, overrides):
    answer = [1] * length
    for index, value in overrides.items():
        answer[index] = value
    return tuple(answer)


BALANCE = {
    25: {"mu": (21, 14, 13), "weights": weights(129, {
        8: 2, 18: 7, 21: 3, 57: 9, 69: 5, 70: 6, 90: 2, 96: 6,
        99: 5, 111: 3, 114: 4, 117: 5, 120: 7, 123: 7, 127: 6, 128: 2,
    })},
    26: {"mu": (15, 14, 15), "weights": weights(138, {
        8: 4, 12: 3, 48: 3, 81: 2, 87: 3, 92: 2, 95: 3, 105: 3,
        110: 4, 111: 4, 114: 4, 119: 4, 121: 4, 123: 4, 136: 6,
    })},
    27: {"mu": (15, 14, 22), "weights": weights(147, {
        8: 11, 21: 3, 48: 2, 49: 2, 81: 4, 85: 4, 87: 7, 91: 4,
        95: 2, 101: 5, 110: 5, 125: 3, 126: 7, 129: 3, 145: 6, 146: 5,
    })},
    28: {"mu": (15, 14, 15), "weights": weights(156, {
        8: 4, 12: 3, 48: 3, 81: 2, 85: 3, 92: 2, 95: 3, 107: 3,
        126: 2, 127: 3, 153: 3,
    })},
}


def occupied(mask, i, j):
    return bool(mask & (1 << (3 * i + j)))


def fibre_matching(template, word):
    total = 0
    for matching in MATCHINGS:
        if all(occupied(template[EIDX[u, v]], word[u], word[v]) for u, v in matching):
            total += 1
    return total


def fibre_dp(template, word):
    memo = {0: 1}

    def rec(subset):
        if subset in memo:
            return memo[subset]
        ub = subset & -subset
        u = ub.bit_length() - 1
        rest = subset ^ ub
        total = 0
        r = rest
        while r:
            vb = r & -r
            v = vb.bit_length() - 1
            r ^= vb
            edge = (u, v) if u < v else (v, u)
            i, j = (word[u], word[v]) if u < v else (word[v], word[u])
            if occupied(template[EIDX[edge]], i, j):
                total += rec(rest ^ vb)
        memo[subset] = total
        return total

    return rec((1 << 8) - 1)


def occupied_cells(template):
    return tuple((e, cell) for e, mask in enumerate(template)
                 for cell in range(9) if mask & (1 << cell))


def balance_loads(template, certificate):
    cells = occupied_cells(template)
    weights = certificate["weights"]
    require(len(cells) == len(weights), "balance support mismatch")
    require(all(weight > 0 for weight in weights), "nonpositive balance weight")
    loads = {(v, c): 0 for v in range(8) for c in COLORS}
    for (edge_index, cell), weight in zip(cells, weights):
        u, v = EDGES[edge_index]
        i, j = divmod(cell, 3)
        loads[u, i] += weight
        loads[v, j] += weight
    mu = tuple(loads[0, c] for c in COLORS)
    require(mu == certificate["mu"], (mu, certificate["mu"]))
    require(all(loads[v, c] == mu[c] for v in range(8) for c in COLORS), "unbalanced port loads")
    return loads


def transpose_template(template):
    answer = []
    for mask in template:
        moved = 0
        for i in COLORS:
            for j in COLORS:
                if occupied(mask, i, j):
                    moved |= 1 << (3 * j + i)
        answer.append(moved)
    return tuple(answer)


def audit_one(m, template):
    require(len(template) == 28, "template edge count")
    cells = occupied_cells(template)
    require(sum(bool(mask) for mask in template) == m, "live edge count")
    expected_sigma = {25: 129, 26: 138, 27: 147, 28: 156}[m]
    require(len(cells) == expected_sigma, "occupied cell count")
    loads = balance_loads(template, BALANCE[m])

    all_hist = Counter()
    central_hist = Counter()
    pure = []
    ledger = []
    for word in itertools.product(COLORS, repeat=8):
        first = fibre_matching(template, word)
        second = fibre_dp(template, word)
        require(first == second, (m, word, first, second))
        if len(set(word)) == 1:
            pure.append(first)
        else:
            all_hist[first] += 1
        counts = sorted(Counter(word).values())
        if counts == [2, 3, 3]:
            central_hist[first] += 1
        ledger.append((word, first))
    require(all(value > 0 for value in pure), "pure matching liveness")
    require(all_hist.get(1, 0) == 0, "mixed singleton survived")
    require(central_hist.get(1, 0) == 0 and sum(central_hist.values()) == 1680,
            "NO-SINGLETON-332 failed")
    expected_min = {25: 8, 26: 11, 27: 12, 28: 16}[m]
    require(min(central_hist) == expected_min, "central minimum moved")

    transposed = transpose_template(template)
    transposed_ledger = tuple(fibre_matching(transposed, w)
                              for w in itertools.product(COLORS, repeat=8))
    require(tuple(value for _, value in ledger) != transposed_ledger,
            "endpoint transpose mutation did not fire")
    bad = dict(BALANCE[m])
    bad_weights = list(bad["weights"])
    bad_weights[0] += 1
    bad["weights"] = tuple(bad_weights)
    try:
        balance_loads(template, bad)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("balance-weight mutation survived")

    return {
        "m_live_edge_blocks": m,
        "sigma_occupied_endpoint_cells": len(cells),
        "positive_balance_mu": list(BALANCE[m]["mu"]),
        "pure_matching_counts": pure,
        "minimum_mixed_matching_count": min(k for k in all_hist if k),
        "minimum_332_matching_count": min(central_hist),
        "central_matching_histogram": dict(sorted(central_hist.items())),
        "mixed_singletons": all_hist.get(1, 0),
        "central_singletons": central_hist.get(1, 0),
        "fibre_ledger_sha256": hashlib.sha256(
            json.dumps(ledger, separators=(",", ":")).encode()).hexdigest(),
        "balance_loads_sha256": hashlib.sha256(
            json.dumps(sorted(((list(k), v) for k, v in loads.items())),
                       separators=(",", ":")).encode()).hexdigest(),
    }


def diagonal_shell_guard():
    # If every cell is diagonal, every supported matching pairs equal word
    # colours, so each colour class has even cardinality.  Exhaustively verify
    # the parity statement on the full diagonal support.
    diagonal = tuple(sum(1 << (3 * c + c) for c in COLORS) for _ in EDGES)
    central_live = sum(fibre_matching(diagonal, word) > 0
                       for word in itertools.product(COLORS, repeat=8)
                       if sorted(Counter(word).values()) == [2, 3, 3])
    require(central_live == 0, "diagonal support unexpectedly sees the 332 shell")
    return {
        "full_diagonal_332_live_words": central_live,
        "reason": "each diagonal matching edge pairs equal colours, forcing even colour-class sizes",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    rows = [audit_one(m, TEMPLATES[m]) for m in range(25, 29)]
    result = {
        "schema": "codex.n8_support_survivors.v1",
        "status": "UNAUDITED exact support-level controls",
        "survivors": rows,
        "diagonal_family_scope_guard": diagonal_shell_guard(),
        "conclusion": (
            "BAL + PURE-LIVE + NO-MIXED-SINGLETON (hence NO-SINGLETON-332) leaves all four named "
            "full endpoint-cell supports m=25..28 alive; coefficient equations and carrier conditions remain essential."
        ),
        "scope": (
            "These are support survivors, not X4 points and not exact sources. m counts live edge blocks, while "
            "sigma counts occupied endpoint-colour cells; neither is the globally minimized sigma a priori."
        ),
    }
    digest = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    output = {"result": result, "result_sha256": digest}
    if args.write_results:
        (HERE / "results_support_survivors.json").write_text(
            json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"PASS": True, "survivors": [
        {"m": row["m_live_edge_blocks"], "sigma": row["sigma_occupied_endpoint_cells"],
         "mu": row["positive_balance_mu"], "min332": row["minimum_332_matching_count"]}
        for row in rows], "result_sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()
