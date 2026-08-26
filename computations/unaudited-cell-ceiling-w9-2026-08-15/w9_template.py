#!/usr/bin/env python3
"""W9 -- exact template (support-level) fibre counting, pure Python integers.

A TEMPLATE is the cell pattern of a source: template[e] = set of (a,b) cells
of the block on edge e.  The FIBRE of a word w is the number of perfect
matchings all of whose edges carry the cell (w_u, w_v).

W6's Sigma_min feasibility conditions (structural_ok + evaluate), restated:
 (T1) exactly m nonempty blocks
 (T2) exactly beta of them single cells        <-- W6 fixed beta = floor
 (T4) each of the 3 constant words has fibre >= 1  ("no missing pure")
 (T5) every vertex meets >= 3 nonempty blocks
 (T6) every (vertex, colour) slot carries a cell
 (S)  NO mixed word has fibre exactly 1        ("singleton-free")
"""
from __future__ import annotations
from itertools import combinations, product
from functools import lru_cache

COLORS = (0, 1, 2)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple) -> tuple:
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for i in range(1, len(vertices)):
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, vertices[i]),) + tail)
    return tuple(out)


def template_of(source, size=8):
    """{edge: frozenset of cells} from a numeric source."""
    return {(u, v): frozenset((i, j) for i in COLORS for j in COLORS
                              if source[(u, v)][i][j])
            for u, v in combinations(range(size), 2)}


def fibres(template, size=8):
    """{word: #supported matchings} for all 3^size words. Exact integers."""
    ms = perfect_matchings(tuple(range(size)))
    out = {}
    for word in product(COLORS, repeat=size):
        n = 0
        for matching in ms:
            ok = True
            for u, v in matching:
                if (word[u], word[v]) not in template[(u, v)]:
                    ok = False
                    break
            if ok:
                n += 1
        out[word] = n
    return out


def audit(template, size=8):
    """All W6 Sigma_min feasibility conditions + the census, exactly."""
    f = fibres(template, size)
    live = [e for e in template if template[e]]
    m = len(live)
    Sigma = sum(len(template[e]) for e in live)
    beta = sum(1 for e in live if len(template[e]) == 1)
    deg = [0] * size
    slots = set()
    for (u, v) in live:
        deg[u] += 1
        deg[v] += 1
        for a, b in template[(u, v)]:
            slots.add((u, a))
            slots.add((v, b))
    const = [(c,) * size for c in COLORS]
    missing = [c for c in COLORS if f[const[c]] == 0]
    singletons = [w for w, n in f.items() if n == 1 and len(set(w)) > 1]
    return {
        "m": m, "Sigma": Sigma, "beta": beta,
        "min_degree": min(deg), "degrees": deg,
        "slots_covered": len(slots), "slots_needed": 3 * size,
        "T4_missing_pures": missing,
        "T4_pure_fibres": [f[const[c]] for c in COLORS],
        "T5_min_degree_ok": min(deg) >= 3,
        "T6_slots_ok": len(slots) == 3 * size,
        "S_mixed_singletons": len(singletons),
        "S_singleton_free": len(singletons) == 0,
        "singleton_words": sorted("".join(map(str, w)) for w in singletons)[:20],
        "mixed_fibre_histogram": _hist(f, size),
    }


def _hist(f, size):
    h = {}
    for w, n in f.items():
        if len(set(w)) > 1:
            h[n] = h.get(n, 0) + 1
    return dict(sorted(h.items()))
