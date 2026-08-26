#!/usr/bin/env python3
"""W10 task E -- WHICH FILTER SURVIVES.

Task B/C proved: (T4)+(T5)+(T6)+(S) -- W9's admissibility -- plus the whole
mixed system does NOT bound the cell count (witnesses reach Sigma = 9m, the
absolute maximum).  So a cell ceiling can only come from a template condition
STRICTLY STRONGER than (T4/T5/T6/S).  This script identifies exactly which one
the campaign already has, and checks it against the witnesses.

The candidate is W8's FIE filter (`w8_core.fie_ok`), the TEMPLATE shadow of
W6's input (S1) (the slice-cover forced incident-edge theorem):

  (FIE) for every vertex p and every colour r some incident block is THIN at
        the far endpoint with far colour r (all its cells in column r at j).

(FIE) is a genuine consequence of full EXACTNESS at value level, NOT of
mixed-exactness, and the witnesses show it is not implied by (T4/T5/T6/S).
Also run here: W3's balance/degeneration alternative (case (P) vs (D)) on the
witness templates, since W3 Corollary A.2 makes case (P) a WLOG for the
minimal counterexample.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE,
          os.path.join(REPO, "computations", "unaudited-bridge-w6-2026-08-15"),
          os.path.join(REPO, "computations", "unaudited-cell-ceiling-w9-2026-08-15"),
          os.path.join(REPO, "computations", "unaudited-template-kill-w8-2026-08-15"),
          os.path.join(REPO, "computations", "unaudited-git-moment-w3-2026-08-15")):
    if p not in sys.path:
        sys.path.insert(0, p)

import w10_core as w10                                            # noqa: E402
from w10_core import COLORS, require                              # noqa: E402
import w8_core as w8                                              # noqa: E402
import w3_core as w3c                                             # noqa: E402
import w3_balance as w3b                                          # noqa: E402

OUT = {}
log = []


def say(s="", flush=True):
    print(s, flush=flush)
    log.append(s)


def to_w8(template, size):
    geo = w8.geometry(size)
    masks = []
    for e in geo.edges:
        mask = 0
        for (i, j) in template[e]:
            mask |= 1 << (3 * i + j)
        masks.append(mask)
    return geo, masks


# ---------------------------------------------------------- E1 the witnesses
say("=" * 94)
say("E1  W8's template filters on the W10 witnesses (N=8 band) -- which fail?")
say("=" * 94)
res = json.load(open(os.path.join(HERE, "results_c_n8.json")))
rows = []
say(f"{'m':>3} {'Sigma':>6} {'beta':>5} {'T4/T5/T6/S':>11} {'W8 fie':>7} "
    f"{'W8 constants':>13} {'W8 mixedSing':>13} {'budgetFloor':>12}")
for rec in res["C1_sweep"]:
    m = rec["m"]
    G = set(tuple(e) for e in rec["graph"])
    tpl = {e: (frozenset((i, j) for i in COLORS for j in COLORS)
               if e in G else frozenset())
           for e in w10.edges(8)}
    geo, masks = to_w8(tpl, 8)
    a8 = w8.audit(geo, masks)
    row = {"m": m, "Sigma": a8["sigma"], "beta": a8["beta"],
           "w9_admissible": rec["ADMISSIBLE"],
           "w8_fie": bool(a8["fie"]), "w8_constants": bool(a8["constants"]),
           "w8_mixed_singletons": a8["mixed_singletons"],
           "w8_budget_floor_ok": bool(a8["budget_floor_ok"]),
           "budget_floor_required": max(0, 24 - m)}
    rows.append(row)
    say(f"{m:>3} {a8['sigma']:>6} {a8['beta']:>5} "
        f"{str(rec['ADMISSIBLE']):>11} {str(bool(a8['fie'])):>7} "
        f"{str(bool(a8['constants'])):>13} {a8['mixed_singletons']:>13} "
        f"{str(bool(a8['budget_floor_ok'])):>12}")
OUT["E1_witness_filters"] = rows
say()
say("  Read-off: the witnesses pass (T4)=constants, (S)=no mixed singleton,")
say("  (T5), (T6) -- and FAIL exactly (FIE) and the budget floor beta >= 3N-m.")
say("  Those two are the SAME ingredient: the budget floor is derived FROM (S1),")
say("  whose template shadow is (FIE).")

# ---------------------------------------------------------- E2 W6 certificates
say()
say("=" * 94)
say("E2  the same filters on W6's Sigma_min band certificates (the objects H4")
say("    is about) -- they DO satisfy (FIE)")
say("=" * 94)
blob = json.load(open(os.path.join(REPO, "computations",
                                   "unaudited-bridge-w6-2026-08-15",
                                   "results_sigmamin_N8.json")))
EDGES8 = w10.edges(8)
w6rows = []
say(f"{'m':>3} {'Sigma':>6} {'beta':>5} {'fie':>6} {'constants':>10} "
    f"{'mixedSing':>10} {'budgetFloor':>12}")
for rec in blob["rows"]:
    if rec.get("template") is None or not (19 <= rec["m"] <= 27):
        continue
    tpl = {EDGES8[n]: frozenset(tuple(c) for c in s)
           for n, s in enumerate(rec["template"])}
    geo, masks = to_w8(tpl, 8)
    a8 = w8.audit(geo, masks)
    aud = w10.audit(tpl, 8)
    w6rows.append({"m": rec["m"], "Sigma": a8["sigma"], "beta": a8["beta"],
                   "fie": bool(a8["fie"]), "constants": bool(a8["constants"]),
                   "mixed_singletons": a8["mixed_singletons"],
                   "budget_floor_ok": bool(a8["budget_floor_ok"]),
                   "w10_admissible": aud["ADMISSIBLE"]})
    say(f"{rec['m']:>3} {a8['sigma']:>6} {a8['beta']:>5} "
        f"{str(bool(a8['fie'])):>6} {str(bool(a8['constants'])):>10} "
        f"{a8['mixed_singletons']:>10} {str(bool(a8['budget_floor_ok'])):>12}")
OUT["E2_w6_certificates"] = w6rows
nfie = sum(1 for r in w6rows if r["fie"])
say(f"  {nfie}/{len(w6rows)} of W6's band certificates satisfy (FIE); "
    f"{sum(1 for r in w6rows if r['w10_admissible'])}/{len(w6rows)} satisfy "
    f"(T4/T5/T6/S).")

# ------------------------------------------------- E3 FIE is not implied
say()
say("=" * 94)
say("E3  (FIE) is NOT implied by (T4)+(T5)+(T6)+(S) -- the separation, proved")
say("=" * 94)
sep = [r for r in rows if r["w9_admissible"] and not r["w8_fie"]]
say(f"  {len(sep)} of {len(rows)} witness templates are (T4/T5/T6/S)-admissible")
say(f"  and violate (FIE).  Supports: {[r['m'] for r in sep]}")
require(len(sep) == len(rows), "separation not clean")
OUT["E3_separation"] = {"admissible_and_not_fie": [r["m"] for r in sep]}
say("  Consequently a cell ceiling C(m) < 9m is NOT derivable from the mixed")
say("  equations plus (T4/T5/T6/S).  Any such ceiling must consume (FIE) --")
say("  equivalently (S1) at value level, i.e. the PURE equations.")

# ------------------------------------------------- E4 W3 balance case (P)/(D)
say()
say("=" * 94)
say("E4  W3's balance/degeneration alternative on the witness templates")
say("=" * 94)


def to_S(template, size):
    ci = w3c.cell_index(size)
    eidx = {e: k for k, e in enumerate(w10.edges(size))}
    return sorted(ci[(eidx[e], i, j)] for e in template for (i, j) in template[e])


w3rows = []
for rec in res["C1_sweep"]:
    m = rec["m"]
    if not (19 <= m <= 27):
        continue
    G = set(tuple(e) for e in rec["graph"])
    tpl = {e: (frozenset((i, j) for i in COLORS for j in COLORS)
               if e in G else frozenset())
           for e in w10.edges(8)}
    S = to_S(tpl, 8)
    bal = w3b.find_balance(8, S)
    if bal is not None:
        ok = bool(w3b.verify_balance(8, S, bal["y"], bal["mu"]))
        case, verified = "P (balanced)", ok
    else:
        deg = w3b.find_degeneration(8, S)
        if deg is not None:
            case = "D (degenerates)"
            verified = bool(w3b.verify_degeneration(8, S, deg))
        else:
            case, verified = "undecided", False
    w3rows.append({"m": m, "Sigma": len(S), "case": case, "verified": verified})
    say(f"  m={m:2d} Sigma={len(S):3d}  {case}"
        f"{'  [verified]' if verified else ''}")
OUT["E4_w3_case"] = w3rows
nP = sum(1 for r in w3rows if r["case"].startswith("P"))
say(f"  case (P): {nP}/{len(w3rows)}  -- W3 Corollary A.2 makes case (P) the")
say("  WLOG stratum for a minimal counterexample, so case-(P) witnesses are the")
say("  ones that survive that filter too.")

with open(os.path.join(HERE, "results_e_filters.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_e_filters.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say()
say("E DONE")
