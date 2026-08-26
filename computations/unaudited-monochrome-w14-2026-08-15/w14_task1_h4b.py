#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- Task 1(b) at h = 4, fraction-free.

Same test as w14_task1_h4.py but with integral (fraction-free) elimination, and
with the F3 shape -- the one that is clean at EVERY h (one site with no
colour-c attachment to either p or q).  F2 (kill the colour-c p-row at 4 sites)
is clean only when 2h - 4 <= h - 1, i.e. h <= 3, so at h = 4 it is expected to
report an unclean slice; it is kept as a control.
"""
from __future__ import annotations
import json, random, sys, time
HERE = __file__.rsplit("/", 1)[0]
sys.path.insert(0, HERE)
from w14_core import (COLORS, delta, det3, G_level, graded_error, mono_name,
                      no_zero_row_or_col, rank3, sigma_basis, sites)
from w14_task1_transfer import build
from w14_ffree import IntSpan

def graded_row(z, h):
    row = []
    for k in range(2, h + 1):
        idx = {key: n for n, key in enumerate(sigma_basis(k))}
        vec = [0] * len(idx)
        for key, c in z[k].items():
            vec[idx[key]] += c
        row.extend(vec)
    return row

def target_row(h, a, c):
    row = []
    for k in range(2, h + 1):
        idx = {key: n for n, key in enumerate(sigma_basis(k))}
        vec = [0] * len(idx)
        if k == h - a:
            vec[idx[((c,) * k, (c,) * k)]] = 1
        row.extend(vec)
    return row

def run(h, kind, c, zero_diag, rng, nwords):
    src = build(kind, h, rng, c, zero_diag)
    A = src[(0, 1)]
    words = [tuple(rng.randrange(3) for _ in range(2 * h)) for _ in range(nwords)]
    words += [(cc,) * (2 * h) for cc in COLORS]
    sp = IntSpan(sum(len(sigma_basis(k)) for k in range(2, h + 1)))
    t0 = time.time()
    for w in words:
        sp.add(graded_row(graded_error(src, h, w), h))
    dc, sc = delta(c), A[c][c]
    Gs = {j: [G_level(src, h, w, dc, dc, j) for w in words] for j in range(h - 1)}
    clean = all(sum(sc ** j * Gs[j][n] for j in range(h - 1)) == 0
                for n in range(len(words)))
    rec = {"h": h, "kind": kind, "colour": c, "A_cc": sc, "det_A": det3(A),
           "rank_A": rank3(A), "no_zero_row_col": no_zero_row_or_col(A),
           "words": len(words), "span_dim": sp.dim(), "slice_clean": clean,
           "G_nonzero": {j: any(x != 0 for x in Gs[j]) for j in range(h - 1)},
           "seconds": round(time.time() - t0, 1)}
    for a in range(0, h - 1):
        rec[mono_name(a, tuple((h - a) if t == c else 0 for t in COLORS))] = \
            sp.contains(target_row(h, a, c))
    return rec

def main():
    rng = random.Random(24680)
    out = []
    print("== W14 Task 1(b), h = 4, fraction-free exact membership ==")
    for kind, zd in (("F1", True), ("F3", True), ("F2", True), ("F3", False)):
        for c in ((0, 2) if kind == "F3" else (0,)):
            rec = run(4, kind, c, zd, rng, 480)
            out.append(rec)
            mono = {k: v for k, v in rec.items()
                    if isinstance(v, bool) and (k.startswith("k") or
                                                (k.startswith("s") and "k" in k))}
            print(f"  [{kind}] colour {c}, A_cc = {rec['A_cc']}, det {rec['det_A']}: "
                  f"clean {rec['slice_clean']}, G nonzero {rec['G_nonzero']}, "
                  f"span {rec['span_dim']}/361 [{rec['seconds']}s]")
            print(f"        {mono}")
    json.dump(out, open(HERE + "/results_task1_h4.json", "w"), indent=1, default=str)
    print("wrote results_task1_h4.json")

if __name__ == "__main__":
    main()
