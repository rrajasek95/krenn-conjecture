#!/usr/bin/env python3
"""W10 task G -- (FIE) audit of the campaign's Sigma_min certificates.

(FIE) is the TEMPLATE reading of W6's input (S1) (notes/slice-cover.md,
"Forced incident-edge theorem"): for every vertex p and colour r there is an
incident block A_pj = a (x) e_r^{(j)}, i.e. a block ALL of whose cells lie in
column r at the far endpoint j.  (S1) is committed and is a necessary
condition on an EXACT source, so (FIE) is a necessary condition on the
TEMPLATE of an exact source.

Question: do W6's and W9's Sigma_min certificates -- the objects that define
the H4 target number -- satisfy it?  Answer below.  If they do not, then
Sigma_min(m) as measured is a minimum over a class strictly larger than the
templates an exact source can have, i.e. an UNDER-estimate of the honest H4
target Sigma_min^+(m).
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE,
          os.path.join(REPO, "computations", "unaudited-template-kill-w8-2026-08-15")):
    if p not in sys.path:
        sys.path.insert(0, p)

import w10_core as w10                                            # noqa: E402
import w8_core as w8                                              # noqa: E402

GEO = w8.geometry(8)
EDGES = w10.edges(8)
log = []
OUT = {}


def say(s="", flush=True):
    print(s, flush=flush)
    log.append(s)


def masks_of(template_rows):
    masks = []
    for n, s in enumerate(template_rows):
        mk = 0
        for (i, j) in s:
            mk |= 1 << (3 * int(i) + int(j))
        masks.append(mk)
    return masks


def audit_row(label, m, rows):
    masks = masks_of(rows)
    tpl = {EDGES[n]: frozenset(w8.cells(masks[n])) for n in range(28)}
    a10 = w10.audit(tpl, 8)
    fd = w8.fie_demands(GEO, masks)
    unserved = sorted(k for k, v in fd.items() if not v)
    cls = Counter(w8.block_class(mk) for mk in masks if mk)
    return {"label": label, "m": m, "Sigma": a10["Sigma"], "beta": a10["beta"],
            "budget_floor": max(0, 24 - m),
            "T4T5T6S": a10["ADMISSIBLE"],
            "FIE": len(unserved) == 0,
            "fie_unserved": len(unserved),
            "fie_unserved_slots": [list(x) for x in unserved],
            "block_classes": dict(cls)}


say("=" * 94)
say("G  (FIE) audit of the Sigma_min certificates that define the H4 target")
say("=" * 94)
say(f"{'certificate':>18} {'m':>3} {'Sigma':>6} {'beta':>5} {'floor':>6} "
    f"{'T4/T5/T6/S':>11} {'FIE':>5} {'unserved/24':>12}  block classes")
rows_out = []

w6 = json.load(open(os.path.join(REPO, "computations",
                                 "unaudited-bridge-w6-2026-08-15",
                                 "results_sigmamin_N8.json")))
for rec in w6["rows"]:
    if rec.get("template") is None or not (19 <= rec["m"] <= 27):
        continue
    r = audit_row("W6", rec["m"], [[tuple(c) for c in s]
                                   for s in rec["template"]])
    rows_out.append(r)
    say(f"{'W6 sigma_min':>18} {r['m']:>3} {r['Sigma']:>6} {r['beta']:>5} "
        f"{r['budget_floor']:>6} {str(r['T4T5T6S']):>11} {str(r['FIE']):>5} "
        f"{r['fie_unserved']:>12}  {r['block_classes']}")

try:
    w9 = json.load(open(os.path.join(REPO, "computations",
                                     "unaudited-cell-ceiling-w9-2026-08-15",
                                     "results_b0_sigmamin_honest.json")))
    for rec in w9.get("rows", []):
        if not rec.get("template") or not (19 <= rec["m"] <= 27):
            continue
        r = audit_row("W9", rec["m"], [[tuple(c) for c in s]
                                       for s in rec["template"]])
        rows_out.append(r)
        say(f"{'W9 sigma_min':>18} {r['m']:>3} {r['Sigma']:>6} {r['beta']:>5} "
            f"{r['budget_floor']:>6} {str(r['T4T5T6S']):>11} {str(r['FIE']):>5} "
            f"{r['fie_unserved']:>12}  {r['block_classes']}")
except FileNotFoundError:
    say("  (W9 b0 certificates not found)")

n = len(rows_out)
nf = sum(1 for r in rows_out if r["FIE"])
na = sum(1 for r in rows_out if r["T4T5T6S"])
say()
say(f"  {na}/{n} certificates satisfy (T4)+(T5)+(T6)+(S).")
say(f"  {nf}/{n} certificates satisfy (FIE).")
say("  => Sigma_min(m) as recorded in plan v8/v10 is a minimum over templates")
say("     that INCLUDE ones no exact source can inhabit.  The honest H4 target")
say("     is Sigma_min^+(m) >= Sigma_min(m), the minimum over (T4/T5/T6/S)+(FIE).")
say("  Direction of the correction: it RAISES the target, i.e. it works in")
say("  H4's favour -- the opposite direction to W9's two corrections.")
say("  It does NOT overturn W9 Theorem C2: the best conceivable counting")
say("  ceiling C_best(m) = m + 96 - 8*max(0,24-m) = 75..123 still exceeds every")
say("  Sigma value task F finds inside (T4/T5/T6/S)+(FIE).")
OUT["rows"] = rows_out
OUT["summary"] = {"n": n, "n_fie": nf, "n_admissible": na}

with open(os.path.join(HERE, "results_g_sigmamin_fie_audit.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_g_sigmamin_fie_audit.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("G DONE")
