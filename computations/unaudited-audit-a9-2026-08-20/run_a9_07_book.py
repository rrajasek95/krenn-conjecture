#!/usr/bin/env python3
"""A9-07: row bookkeeping, the X_4 = EXACT identification, and the
CANCELLATION question (links 3 and 5).

  B1  every mixed word of K_8 with all-even profile <-> exactly one A2 clause
      at k=4, and k=4 drops NOTHING (so the k=4 system IS the exact system).
  B2  the FREE rows are genuine mixed words too (off-count <= 4).
  B3  structural: no clause forces a hafnian to be NONZERO from support --
      every positive p-literal sits in a clause that also has a negative
      p-literal or is one of the four licensed units (A0/A1/Cnz/Ch).
  B4  operational: models with heavy cancellation exist (a 4-set hafnian
      vanishing while all six of its edges are nonzero) -- so the abstraction
      really does allow cancellation.
"""
from __future__ import annotations

import json
import sys
import time
from itertools import product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import a9_enc as E                                                   # noqa: E402

RES = {}
OUT = f"{BASE}/results_a9_07_book.json"
T0 = time.time()


def b1_words(n=8):
    """All 3^n words; the A2 clause set must be exactly the mixed all-even
    ordered partitions, and at k=4 none of them is dropped."""
    V = tuple(range(n))
    const, odd_part, mixed_even = 0, 0, 0
    parts_needed = set()
    offs = {}
    for w in product(range(3), repeat=n):
        parts = tuple(tuple(v for v in V if w[v] == c) for c in range(3))
        sizes = [len(p) for p in parts]
        if max(sizes) == n:
            const += 1
            continue
        if any(s % 2 for s in sizes):
            odd_part += 1
            continue
        mixed_even += 1
        off = n - max(sizes)
        offs[off] = offs.get(off, 0) + 1
        parts_needed.add(tuple(E.mask_of(p) for p in parts))
    e4 = E.Enc(n, ((), (), ()), k=4).build()
    einf = E.Enc(n, ((), (), ()), k=None).build()
    got4 = {t[1] for t, in zip(e4.tags) if t[0] == "A2"}
    gotinf = {t[1] for t, in zip(einf.tags) if t[0] == "A2"}
    return {"n_words": 3 ** n, "constant": const, "odd_part": odd_part,
            "mixed_even": mixed_even, "offcount_histogram": offs,
            "A2_rows_k4": len(got4), "A2_rows_kNone": len(gotinf),
            "A2_k4_equals_kNone": got4 == gotinf,
            "A2_k4_equals_words": got4 == parts_needed,
            "PASS": got4 == gotinf == parts_needed}


def b2_free_rows(n=8, k=4):
    """Every FREE row is the word (c on {z,y}, d on S_1, e on S_2): mixed,
    all-even, off-count <= 4 -- so it IS an exact-source condition."""
    e = E.Enc(n, ((3, 4, 5, 6),) * 3, k=k).build()
    bad = []
    nfree = 0
    for tag in e.tags:
        if tag[0] != "FR":
            continue
        _, c, y, s1, s2 = tag
        nfree += 1
        sizes = [2, E.popcount(s1), E.popcount(s2)]
        if sum(sizes) != n or any(s % 2 for s in sizes) or max(sizes) == n:
            bad.append(tag)
        if n - max(sizes) > k:
            bad.append(tag)
    return {"free_rows": nfree, "malformed": len(bad), "PASS": not bad}


def b3_polarity(n=8):
    e = E.Enc(n, ((3, 4), (5,), ()), k=4).build()
    licensed = {"A0", "A1", "Cnz", "Ch"}
    bad = []
    counts = {}
    for tag, cl in zip(e.tags, e.cls):
        pos = [l for l in cl if l > 0]
        neg = [l for l in cl if l < 0]
        counts[tag[0]] = counts.get(tag[0], 0) + 1
        if not pos:
            continue
        if tag[0] in licensed and len(cl) == 1:
            continue
        if neg:
            continue                       # an implication FROM a nonzero
        bad.append((str(tag), [str(e.vname[abs(l)]) for l in cl]))
    return {"clause_counts": counts, "unconditional_positive_clauses": bad,
            "PASS": not bad}


def b4_cancellation(n=8):
    """Ask for a model where a 4-set hafnian VANISHES although its six edges
    are all nonzero -- the vanishing pattern of a cancelling point."""
    from pysat.solvers import Solver
    out = {}
    for k, Rs in ((3, ((3, 4, 5, 6),) * 3), (3, ((), (), ()))):
        e = E.Enc(n, Rs, k=k).build()
        S = (0, 1, 2, 3)
        m = E.mask_of(S)
        extra = [[-e.p(0, m)]]
        for i in range(4):
            for j in range(i + 1, 4):
                extra.append([e.p(0, (1 << S[i]) | (1 << S[j]))])
        with Solver(name="cadical195",
                    bootstrap_with=[list(c) for c in e.cls] + extra) as So:
            out[f"k{k}_R{Rs[0]}"] = So.solve()
    out["PASS"] = any(out.values())
    return out


def main():
    RES["B1_word_bookkeeping"] = b1_words()
    print("B1", RES["B1_word_bookkeeping"], flush=True)
    RES["B2_free_rows"] = b2_free_rows()
    print("B2", RES["B2_free_rows"], flush=True)
    RES["B3_polarity"] = b3_polarity()
    print("B3", RES["B3_polarity"], flush=True)
    RES["B4_cancellation"] = b4_cancellation()
    print("B4", RES["B4_cancellation"], flush=True)
    RES["seconds"] = round(time.time() - T0, 1)
    RES["PASS"] = all(v["PASS"] for v in RES.values() if isinstance(v, dict))
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("PASS", RES["PASS"])


if __name__ == "__main__":
    main()
