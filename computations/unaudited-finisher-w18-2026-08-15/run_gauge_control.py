#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- soundness control for the gauge fixing in W18-B.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

`w18_deep.decide_half` now normalises |sites| cells to 1 before the Groebner
computation (`gauge_columns`).  That is only legitimate because a half-system
is invariant under  A_uv -> l_u l_v A_uv , so this control tries hard to break
it:

  GC1  EXPLICIT POINTS.  Build half-systems that PROVABLY have a solution (the
       zero words are read off an actual random point, so the point itself is a
       witness) and require the gauge-fixed decider to answer "feasible".  A
       single "infeasible" here would be a manufactured kill.

  GC2  GAUGE ORBIT.  Apply a random gauge  l  to the point and check every
       half-system equation still vanishes and every pinned word stays
       non-zero -- i.e. the invariance the fixing relies on really holds for
       the systems this lane builds.

  GC3  SLICE REACHABILITY.  For the chosen columns, solve  l_u l_v x_c = 1
       exactly over Q(i)-free rationals by linear algebra in the exponents,
       and confirm the incidence rows have full rank (the criterion used).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C          # noqa: E402
import w18_deep as D          # noqa: E402
import w18_fast as F          # noqa: E402
import w18_half as H          # noqa: E402
import run_epc as E           # noqa: E402


def systems(rng, want, sizes=(4, 6)):
    """Yield (T, vals, sites, sys_) for half-systems with an explicit point."""
    got = 0
    while got < want:
        T = E.random_template(rng, rng.randint(16, 22))
        vals = E.random_point(rng, T)
        cut = rng.choice([c for c in F.CUTS if len(c.L) == 4])
        sites = rng.choice([cut.L, cut.R])
        if len(sites) not in sizes:
            continue
        vidx = H.side_varindex(sites)
        zero_words, pinned = [], []
        for sub in product(range(3), repeat=len(sites)):
            if not H.side_monomials(T, sites, vidx, sub):
                continue
            if E.side_value(T, vals, sites, sub) == 0:
                zero_words.append(sub)
            else:
                pinned.append(sub)
        if not zero_words or not pinned:
            continue
        sys_ = D.half_system(T, sites, zero_words, pinned)
        if not sys_["eqs"] or all(len(p) == 1 for _, p in sys_["eqs"]):
            continue
        got += 1
        yield T, vals, sites, sys_


def gc1(trials=14, seed=11, timeout=120):
    rng = random.Random(seed)
    rows, bad = [], []
    for T, vals, sites, sys_ in systems(rng, trials):
        v = D.decide_half(sys_, timeout=timeout, want_lift=False, gauge=True)
        rows.append({"sites": list(sites), "nvar": sys_["nvar"],
                     "neqs": len(sys_["eqs"]), "verdict": v["verdict"],
                     "gauge_cols": v.get("gauge_cols")})
        if v["verdict"] == "infeasible":
            bad.append({"template": [int(x) for x in T], "sites": list(sites)})
    return {"systems": len(rows), "verdicts":
            {k: sum(1 for r in rows if r["verdict"] == k)
             for k in {r["verdict"] for r in rows}},
            "false_kills": bad, "passes": not bad}


def gc2(trials=25, seed=12):
    rng = random.Random(seed)
    bad = 0
    checked = 0
    for T, vals, sites, sys_ in systems(rng, trials):
        lam = {s: Fraction(rng.randint(1, 9), rng.randint(1, 9))
               for s in range(C.N)}
        moved = {}
        for (e, i, j), val in vals.items():
            u, v = C.EDGES[e]
            moved[(e, i, j)] = val * lam[u] * lam[v]
        scale = Fraction(1)
        for s in sorted(sites):
            scale *= lam[s]
        for y, _ in sys_["eqs"]:
            checked += 1
            if E.side_value(T, moved, sites, y) != 0:
                bad += 1
        for y, _ in sys_["nonvanishing"]:
            checked += 1
            a = E.side_value(T, vals, sites, y)
            b = E.side_value(T, moved, sites, y)
            if b != a * scale or b == 0:
                bad += 1
    return {"checked": checked, "violations": bad, "passes": bad == 0}


def gc3(trials=25, seed=13):
    rng = random.Random(seed)
    bad = []
    n = 0
    for T, vals, sites, sys_ in systems(rng, trials):
        cols = D.gauge_columns(sys_["varkeys"], sys_["sites"])
        n += 1
        # The criterion is INDEPENDENCE of the chosen incidence rows, not that
        # there are |sites| of them: a side whose internal edges miss a vertex
        # simply has a smaller gauge to fix, and fixing fewer cells is always
        # sound.  So the control checks rank == len(cols).
        # rank of the chosen incidence rows over Q
        pos = {s: k for k, s in enumerate(sorted(sites))}
        rows = []
        for k in cols:
            e, i, j = sys_["varkeys"][k]
            u, v = C.EDGES[e]
            r = [Fraction(0)] * len(sites)
            r[pos[u]] += 1
            r[pos[v]] += 1
            rows.append(r)
        rank = 0
        piv = []
        for r in rows:
            r = list(r)
            for (p, b) in piv:
                if r[p]:
                    f = r[p] / b[p]
                    r = [a - f * c for a, c in zip(r, b)]
            nz = next((t for t, val in enumerate(r) if val), None)
            if nz is not None:
                piv.append((nz, r))
                rank += 1
        if rank != len(cols):
            bad.append({"sites": list(sites), "cols": len(cols),
                        "rank": rank, "why": "chosen rows are dependent"})
    return {"systems": n, "rank_failures": bad, "passes": not bad}


if __name__ == "__main__":
    out = {"GC1_explicit_points": gc1(),
           "GC2_gauge_orbit": gc2(),
           "GC3_slice_rank": gc3()}
    for k, v in out.items():
        print(k, json.dumps(v)[:500], flush=True)
    out["ALL_PASS"] = all(v["passes"] for v in out.values())
    print("ALL_PASS", out["ALL_PASS"])
    json.dump(out, open(os.path.join(HERE, "results_gauge_control.json"), "w"),
              indent=1)
    print("wrote results_gauge_control.json")
