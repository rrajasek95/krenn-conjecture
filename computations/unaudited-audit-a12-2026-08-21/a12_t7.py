#!/usr/bin/env python3
"""A12 -- the (R25) count reconciliation, pinned to code.  UNAUDITED.

R0_defs    -- A11's definition (a11_t10.R25: |T_f| = 1, hafL != 0, two
              different firing letters at one tuple) and W36's (grouping the
              same choices by L-part and subtracting the dead set Z) are
              re-implemented here and compared choice by choice
R1_corpora -- the same predicate evaluated on THREE corpora: A11's actual
              on-disk corpus (points_m25_wide + the s1073 escape object),
              W36's 42-object corpus, and the union
R2_ondisk  -- what A11's stored artifact actually records
"""
from __future__ import annotations
import json, os, sys, time
from collections import defaultdict
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W30 = os.path.join(ROOT, "unaudited-exclusion-w30-2026-08-19")
A11 = os.path.join(ROOT, "unaudited-audit-a11-2026-08-20")
sys.path.insert(0, HERE)
import a12_lib as A
from a12_t0 import Manifest
from a12_t2 import corpus25, slots

DECL = ["R0_defs", "R1_corpora", "R2_ondisk"]


def r25_a11(tm, bl, K, idx):
    by = defaultdict(set)
    for (w, fire) in idx:
        if len(fire) != 1:
            continue
        if K.iszero(tm.hafL(bl, tuple(w[:4]), K)):
            continue
        by[(w[5], w[7])].add(sorted(fire)[0])
    return sorted(str(k) for k, s in by.items() if len(s) >= 2)


def r25_w36(tm, bl, K, idx):
    by = defaultdict(lambda: defaultdict(set))
    Xv = set()
    for (w, fire) in idx:
        if len(fire) == 1:
            by[(w[5], w[7])][sorted(fire)[0]].add(tuple(w[:4]))
            Xv.add(tuple(w[:4]))
    Z = {x for x in Xv if K.iszero(tm.hafL(bl, x, K))}
    return sorted(str(k) for k, d in by.items()
                  if len([f for f, s in d.items() if s - Z]) >= 2)


def main():
    t0 = time.time()
    man = Manifest(DECL)
    tm = A.T(25)
    idx, by, big = slots(tm)
    cp = corpus25()
    a11_tags = set()
    for (tag, fld, ptj) in cp:
        if tag.startswith("wide25_") or "s1073" in tag:
            a11_tags.add(tag)
    rows = []
    ndiff = 0
    for (tag, fld, ptj) in cp:
        K = A.K_of(fld)
        bl = A.load_point(ptj, K)
        if set(bl) != set(tm.gamma) or not (tm.is_clean(bl, K)
                                            and tm.all_nonzero(bl, K)):
            continue
        a = r25_a11(tm, bl, K, idx)
        w = r25_w36(tm, bl, K, idx)
        ndiff += (a != w)
        rows.append(dict(tag=tag, field=fld, in_A11_corpus=(tag in a11_tags),
                         a11_tuples=a, w36_tuples=w, agree=(a == w),
                         R25=bool(a)))
    man.record("R0_defs", dict(
        n=len(rows), n_definition_disagreements=ndiff, ok=(ndiff == 0),
        note="A11's and W36's (R25) are the SAME predicate: hafL depends "
             "only on the L-part, so 'both choices live' and 'the L-part is "
             "outside Z' are the same condition"))
    a11c = [r for r in rows if r["in_A11_corpus"]]
    man.record("R1_corpora", dict(
        A11_corpus=dict(n=len(a11c),
                        n_R25_fail=sum(1 for r in a11c if not r["R25"]),
                        failing=[r["tag"] for r in a11c if not r["R25"]]),
        W36_corpus=dict(n=len(rows),
                        n_R25_fail=sum(1 for r in rows if not r["R25"]),
                        failing=[r["tag"] for r in rows if not r["R25"]]),
        per_point=rows, ok=True))
    rec = {}
    p = os.path.join(A11, "results_t10.json")
    if os.path.exists(p):
        d = json.load(open(p))
        tab = d.get("W3_supersession", {}).get("table", [])
        rec = dict(file="results_t10.json", n_rows=len(tab),
                   n_R25_false=sum(1 for r in tab if not r.get("R25")),
                   seeds=[r.get("seed") for r in tab if not r.get("R25")],
                   only_ab=d.get("W3_supersession", {}).get(
                       "points_where_only_W30_M25_applies"))
    grep = {}
    for f in ("REPORT.md",):
        q = os.path.join(A11, f)
        if os.path.exists(q):
            grep[f] = [ln.strip() for ln in open(q)
                       if "4 of 32" in ln or "4/32" in ln or "32" in ln]
    man.record("R2_ondisk", dict(
        a11_results_t10=rec, a11_report_lines=grep,
        ok=(rec.get("n_rows") is not None),
        note="A11's REPORT.md says (R25) fails at 4 of 32 corpus points; the "
             "only (R25) computation A11 has on disk is results_t10.json, "
             "which evaluates 11 points and records ONE failure"))
    print(json.dumps(dict(defs_disagree=ndiff,
                          a11_corpus=(len(a11c),
                                      sum(1 for r in a11c if not r["R25"])),
                          w36_corpus=(len(rows),
                                      sum(1 for r in rows if not r["R25"])),
                          a11_ondisk=rec), indent=1)[:900], flush=True)
    man.finish(os.path.join(HERE, "results_t7.json"),
               extra={"elapsed_s": round(time.time() - t0, 1)})
    print("T7 DONE", flush=True)


if __name__ == "__main__":
    main()
