#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- LEMMA W18-C: the whole-template ratio kill.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

The value system of a template T: variables = the occupied cells (all nonzero),
one vanishing equation per MIXED word with a nonempty fibre, one
required-nonzero equation per constant word.  Lemma W18-C is exactly the
monomial-ratio engine of w18_ratio applied to that system; a contradiction
means T carries no exact source.

This is the last cheap fallback under Lemma W18-A (combinatorial) and Lemma
W18-D (cut-local); it has no small reason set, so a kill here is turned into a
plain blocking clause for the template's orbit.
"""

from __future__ import annotations

import w18_core as C
import w18_ratio as RA


def varindex(T):
    idx = {}
    for e, mask in enumerate(T):
        for (i, j) in C.cells(mask):
            idx[(e, i, j)] = len(idx)
    return idx


def monomials_from_fibre(idx, w, fib):
    out = []
    for nm in fib:
        vec = [0] * len(idx)
        for e in C.PM_EIDX[nm]:
            u, v = C.EDGES[e]
            vec[idx[(e, w[u], w[v])]] += 1
        out.append(tuple(vec))
    return sorted(out)


def build(T, fibres=None):
    idx = varindex(T)
    if fibres is None:
        fibres = C.all_fibres(T)
    zeros, nonzeros = {}, {}
    for w, fib in fibres.items():
        monos = monomials_from_fibre(idx, w, fib)
        (nonzeros if len(set(w)) == 1 else zeros)[w] = monos
    return len(idx), zeros, nonzeros


def find_kill_C(T, fibres=None):
    for c in range(C.Q):
        if not C.fibre(T, (c,) * C.N):
            return {"lemma": "W18-C", "rule": "C4", "word": [c] * C.N}
    n, zeros, nonzeros = build(T, fibres)
    cert = RA.run(n, zeros, nonzeros)
    if cert is None:
        return None
    cert = RA.compress(cert)
    out = {"lemma": "W18-C", "nvars": n, "ratio": _keys_to_str(cert)}
    return out


def _keys_to_str(cert):
    out = dict(cert)
    if "key" in out:
        out["key"] = "".join(map(str, out["key"]))
    out["generators"] = [dict(g, key="".join(map(str, g["key"])))
                         for g in out["generators"]]
    return out


def _keys_from_str(cert):
    out = dict(cert)
    if "key" in out:
        out["key"] = tuple(int(c) for c in out["key"])
    out["generators"] = [dict(g, key=tuple(int(c) for c in g["key"]))
                         for g in out["generators"]]
    return out


def verify_C(T, cert):
    if cert.get("rule") == "C4":
        w = tuple(cert["word"])
        return (len(set(w)) == 1 and not C.fibre(T, w),
                "a constant word has an empty fibre")
    idx = varindex(T)
    if len(idx) != cert["nvars"]:
        return False, "variable count mismatch"
    ratio = _keys_from_str(cert["ratio"])
    keys = set(g["key"] for g in ratio["generators"])
    if "key" in ratio:
        keys.add(ratio["key"])
    zeros, nonzeros = {}, {}
    for w in keys:
        if len(w) != C.N:
            return False, "cited key is not a word"
        fib = C.fibre(T, w)
        monos = monomials_from_fibre(idx, w, fib)
        (nonzeros if len(set(w)) == 1 else zeros)[w] = monos
    return RA.verify(len(idx), zeros, nonzeros, ratio)
