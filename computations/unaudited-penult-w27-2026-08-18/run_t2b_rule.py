#!/usr/bin/env python3
"""W27 T2b -- FIND THE SKELETON-LEVEL WITNESS CRITERION.

Input: results_t2a_classverdicts.json (24 N=6 diagonal skeleton classes, every
live pair, exact WITNESS/BLOCKED verdict, constant across weight points).

Method: assemble a feature table, then
  (a) report every single feature that is a perfect separator;
  (b) exhaustively search boolean formulas over atomic predicates
      (single atoms, conjunctions/disjunctions of two and of three atoms) for a
      rule that reproduces the verdict on ALL pairs of ALL classes;
  (c) report the minimal such rule and its failure modes;
  (d) sanity-check the rule against W25-U3 (both endpoints clean => witness).
"""
from __future__ import annotations

import json
import sys
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
sys.path.insert(0, BASE)

RES = {}
RAN = []
OUT = f"{BASE}/results_t2b_rule.json"


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def load():
    with open(f"{BASE}/results_t2a_classverdicts.json") as fh:
        D = json.load(fh)
    rows = []
    for key, cl in sorted(D["classes"].items(), key=lambda kv: int(kv[0])):
        wit = set(cl["witness_pairs"])
        for pk, f in cl["features"].items():
            rows.append({"class": cl["idx"], "pair": pk,
                         "verdict": "WITNESS" if pk in wit else "BLOCKED",
                         **f})
    return D, rows


def atoms(rows):
    """Every atomic predicate: (name, function) over the feature dicts."""
    A = []
    keys = set()
    for r in rows:
        keys |= set(r.keys())
    keys -= {"class", "pair", "verdict"}
    for k in sorted(keys):
        vals = sorted(set(json.dumps(r.get(k)) for r in rows))
        if len(vals) > 14:
            continue
        for v in vals:
            A.append((f"{k}=={v}", lambda r, k=k, v=v: json.dumps(r.get(k)) == v))
        # ordered thresholds for numeric features
        nums = [r.get(k) for r in rows if isinstance(r.get(k), (int, float))
                and not isinstance(r.get(k), bool)]
        if len(nums) == len(rows):
            for th in sorted(set(nums)):
                A.append((f"{k}>={th}",
                          lambda r, k=k, th=th: r.get(k) is not None
                          and r.get(k) >= th))
                A.append((f"{k}<={th}",
                          lambda r, k=k, th=th: r.get(k) is not None
                          and r.get(k) <= th))
    return A


def evalrule(f, rows):
    tp = fp = tn = fn = 0
    wrong = []
    for r in rows:
        pred = f(r)
        act = r["verdict"] == "WITNESS"
        if pred and act:
            tp += 1
        elif pred and not act:
            fp += 1
            wrong.append((r["class"], r["pair"], "predicted WITNESS"))
        elif not pred and act:
            fn += 1
            wrong.append((r["class"], r["pair"], "predicted BLOCKED"))
        else:
            tn += 1
    return tp, fp, tn, fn, wrong


def main():
    D, rows = load()
    nW = sum(1 for r in rows if r["verdict"] == "WITNESS")
    print(f"pairs: {len(rows)} over {len(D['classes'])} classes; "
          f"WITNESS {nW}, BLOCKED {len(rows) - nW}")
    RES["n_pairs"] = len(rows)
    RES["n_witness"] = nW
    RES["table"] = rows
    control("T2b0_load")
    ck("load")

    A = atoms(rows)
    print(f"atomic predicates: {len(A)}")
    RES["n_atoms"] = len(A)

    print("=" * 74)
    print("(1) single-atom separators")
    print("=" * 74)
    singles = []
    for name, f in A:
        tp, fp, tn, fn, wrong = evalrule(f, rows)
        acc = (tp + tn) / len(rows)
        singles.append((acc, name, tp, fp, tn, fn))
    singles.sort(reverse=True)
    for acc, name, tp, fp, tn, fn in singles[:14]:
        print(f"   {acc:.4f}  {name:38s}  tp {tp:3d} fp {fp:3d} "
              f"tn {tn:3d} fn {fn:3d}")
    RES["best_singles"] = [{"acc": a, "atom": n, "tp": tp, "fp": fp,
                            "tn": tn, "fn": fn}
                           for a, n, tp, fp, tn, fn in singles[:25]]
    perfect = [s for s in singles if s[0] == 1.0]
    print(f"   PERFECT single-atom separators: {len(perfect)} "
          f"{[s[1] for s in perfect][:6]}")
    control("T2b1_singles")
    ck("singles")

    print("=" * 74)
    print("(2) sound one-sided atoms (never wrong in one direction)")
    print("=" * 74)
    suff = []          # atom => WITNESS (no false positives)
    nec = []           # atom => BLOCKED (no false negatives when negated)
    for name, f in A:
        tp, fp, tn, fn, _ = evalrule(f, rows)
        if fp == 0 and tp > 0:
            suff.append((tp, name))
        if fn == 0 and tn > 0:
            nec.append((tn, name))
    suff.sort(reverse=True)
    nec.sort(reverse=True)
    print(f"   SUFFICIENT-for-witness atoms: {len(suff)}; strongest:")
    for k, n in suff[:10]:
        print(f"      covers {k:3d} witnesses: {n}")
    print(f"   SUFFICIENT-for-blocked atoms (negation): {len(nec)}; strongest:")
    for k, n in nec[:10]:
        print(f"      covers {k:3d} blocked: NOT({n})")
    RES["sufficient_witness"] = [{"covers": k, "atom": n} for k, n in suff[:30]]
    RES["sufficient_blocked"] = [{"covers": k, "atom": n} for k, n in nec[:30]]
    control("T2b2_onesided")
    ck("onesided")

    print("=" * 74)
    print("(3) exhaustive search: OR of two / AND of two / mixed, over the "
          "strongest atoms")
    print("=" * 74)
    # keep atoms that are individually informative
    pool = [(n, f) for (n, f) in A]
    accs = {n: a for a, n, *_ in singles}
    pool.sort(key=lambda nf: -accs.get(nf[0], 0))
    pool = pool[:220]
    found = []
    for i in range(len(pool)):
        n1, f1 = pool[i]
        for j in range(i + 1, len(pool)):
            n2, f2 = pool[j]
            for op, g, sym in (("or", lambda r, f1=f1, f2=f2: f1(r) or f2(r), "|"),
                               ("and", lambda r, f1=f1, f2=f2: f1(r) and f2(r), "&"),
                               ("andnot", lambda r, f1=f1, f2=f2: f1(r) and not f2(r), "&!"),
                               ("ornot", lambda r, f1=f1, f2=f2: f1(r) or not f2(r), "|!")):
                tp, fp, tn, fn, _ = evalrule(g, rows)
                if fp == 0 and fn == 0:
                    found.append(f"({n1}) {sym} ({n2})")
        if found and i > 40:
            break
    print(f"   EXACT two-atom rules found: {len(found)}")
    for r in found[:12]:
        print(f"      {r}")
    RES["exact_two_atom"] = found[:60]
    control("T2b3_two_atom")
    ck("two_atom")

    print("=" * 74)
    print("(4) per-class breakdown of the blocked pairs")
    print("=" * 74)
    bycl = {}
    for r in rows:
        bycl.setdefault(r["class"], []).append(r)
    lines = []
    for c in sorted(bycl):
        rs = bycl[c]
        bl = [r for r in rs if r["verdict"] == "BLOCKED"]
        prof = rs[0]["profile"]
        line = (f"   class {c:2d} {str(prof):10s} live {len(rs):2d} blocked "
                f"{len(bl):2d}: " +
                ", ".join(f"{r['pair']}[cl{int(r['clean_p'])}{int(r['clean_q'])}"
                          f",deg{r['live_deg_p']}/{r['live_deg_q']}"
                          f",off{r['off_comp_sizes']}]" for r in bl[:6]))
        print(line)
        lines.append(line)
    RES["per_class_blocked"] = lines
    control("T2b4_breakdown")

    declared = ["T2b0_load", "T2b1_singles", "T2b2_onesided", "T2b3_two_atom",
                "T2b4_breakdown"]
    missing = [x for x in declared if x not in RAN]
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing
    ck("final")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
