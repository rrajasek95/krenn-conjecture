#!/usr/bin/env python3
"""W9 Task B7c -- MECHANISM (2) decided with W3's OWN exactly-certified
balance/degeneration alternative (w3_balance.find_balance / find_degeneration).

W3 Theorem A.1: for a cell support S exactly one of
  (D) an admissible pure-preserving weight w with S_0(w) a PROPER subset of S
      -- then the restriction is again an exact source at SMALLER support; or
  (P) a strictly positive balanced weighting y (Kempf-Ness balance).
W3 Corollary A.2: a MINIMUM-CELL-SUPPORT counterexample is balanced, i.e. is
in case (P).  So any template in case (D) either is not minimum-cell-support
or degenerates -- in both cases it is not the minimal counterexample's
template.

QUESTION FOR H4: does (D)/(P) constrain the CELL COUNT?  Run it on
  * the committed near-exact source's template (which EXISTS),
  * W6's Sigma_min certificate templates,
  * W9's honest (beta-free) Sigma_min certificate templates.
"""
from __future__ import annotations
import importlib, json, os, sys
from fractions import Fraction as F
from itertools import combinations
import w9_core as w9
import w9_template as wt

W3DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "unaudited-git-moment-w3-2026-08-15")
sys.path.insert(0, W3DIR)
import w3_core as w3c              # noqa: E402
import w3_balance as w3b           # noqa: E402

N = 8
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: k for k, e in enumerate(EDGES)}


def to_S(template):
    """W9 template -> W3 cell-index set."""
    ci = w3c.cell_index(N)
    return sorted(ci[(EIDX[e], i, j)] for e in template for (i, j) in template[e])


def classify(label, template):
    S = to_S(template)
    bal = w3b.find_balance(N, S)
    if bal is not None:
        ok = w3b.verify_balance(N, S, bal["y"], bal["mu"])
        return {"label": label, "Sigma": len(S), "case": "P (balanced)",
                "verified": bool(ok), "mu": [str(x) for x in bal["mu"]]}
    deg = w3b.find_degeneration(N, S)
    if deg is not None:
        ok = w3b.verify_degeneration(N, S, deg)
        return {"label": label, "Sigma": len(S), "case": "D (degenerates)",
                "verified": bool(ok), "S0_size": len(deg.get("S0", []))}
    return {"label": label, "Sigma": len(S), "case": "undecided", "verified": False}


if __name__ == "__main__":
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")

    def build(params):
        blocks = mod.build_stage_a(params)
        return {(u, v): [[F(x) for x in row] for row in mod.C.oriented(blocks, u, v)]
                for u, v in combinations(range(8), 2)}
    BEST = ((F(-7), F(-9)), (F(7), F(8)), F(5,3), F(-7,4), F(-1,5), F(-8,5),
            (F(-7,4), F(-4), F(7,5)), (F(-3,2), F(-5,4), F(-9)),
            (F(1,5), F(8,3), F(-1,5)), (F(-9,2), F(1), F(3,4)), F(6), F(-9))

    print("=" * 86)
    print("B7c  W3's exact balance/degeneration alternative on the H4 templates")
    print("=" * 86)
    cands = [("STAGE_A_GENERIC (exists!)", wt.template_of(build(BEST)))]
    blob = json.load(open(os.path.join("..", "unaudited-bridge-w6-2026-08-15",
                                       "results_sigmamin_N8.json")))
    for rec in blob["rows"]:
        if rec["template"] is None or rec["m"] < 19 or rec["m"] > 27:
            continue
        cands.append((f"W6_sigmamin_m{rec['m']}",
                      {EDGES[n]: frozenset(tuple(c) for c in s)
                       for n, s in enumerate(rec["template"])}))
    try:
        mine = json.load(open("results_b0_sigmamin_honest.json"))
        for rec in mine["rows"]:
            if rec.get("template"):
                cands.append((f"W9_sigmamin_m{rec['m']}",
                              {EDGES[n]: frozenset(tuple(c) for c in s)
                               for n, s in enumerate(rec["template"])}))
    except (FileNotFoundError, KeyError):
        pass

    out = []
    print(f"{'template':28s} {'Sigma':>6}  case")
    for lbl, T in cands:
        r = classify(lbl, T)
        out.append(r)
        print(f"{lbl:28s} {r['Sigma']:6d}  {r['case']}"
              f"{'  [verified]' if r['verified'] else ''}", flush=True)
    with open("results_b7c_w3balance.json", "w") as fh:
        json.dump({"rows": out}, fh, indent=1, default=str)
    print("\nwrote results_b7c_w3balance.json")
