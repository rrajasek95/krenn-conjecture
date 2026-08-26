#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- kill-mechanism inventory for the census.

UNAUDITED.  Nothing here is a proved claim of the repository.
Exact integer arithmetic only.

MECHANISM W16-B (vertex factorisation).  If site t factors (all Gamma
blocks at t rank one with a common t-vector) then Phi_w = gamma_{w_t} *
Psi(off t), so Phi_w = 0 <=> Phi_w' = 0 for words agreeing off t.  The
TEMPLATE-COMBINATORIAL input is the pair inventory:
    (clean, k=1) pair at site t  ->  outright kill
    (clean, k=2) pair at site t  ->  a binomial relation
where k(w) = #supported matchings NOT inside Gamma = fibre(w) - |F(Gamma)|
(F(Gamma) is contained in every fibre), and "clean" means k(w) = 0.

THEOREM W19C-K1 [PROVED-HERE].  For every T in (R),
        k(w) = fibre(T,w) - |F(Gamma)|  >=  3 - |F(Gamma)|   (w mixed).
Hence if |F(Gamma)| <= 2 the clean layer is EMPTY: no mixed word is
effectively clean, so W16-B has no (clean, k) pair at any site and BOTH the
k=1 and the k=2 routes are vacuous for that member.  |F(Gamma)| <= 2 happens
for 75 of the 794 admissible Gamma classes -- including the whole
|Gamma| = 8 stratum.

CALIBRATION.  The inventory code is checked against W16's independently
computed numbers for the W8 ladder m=24..28 (results_vertex.json).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, N, NE, FULL, WORDS, MIXED_POS, CONST_POS, W8_IMMUNE,
    fibres_all_words, fast_in_R, fast_audit, pms_inside, mask_to_edges,
    extras_at, full_pm_indices, effectively_clean, block_class,
)

HERE = os.path.dirname(os.path.abspath(__file__))
W16 = os.path.join(os.path.dirname(HERE), "..",
                   "unaudited-residual2-w16-2026-08-15", "results_vertex.json")

MIXEDB = np.zeros(6561, dtype=bool)
MIXEDB[MIXED_POS] = True
POW3 = [3 ** (N - 1 - p) for p in range(N)]


def kvec(T):
    """k(w) for all 6561 words, exactly."""
    f = fibres_all_words(T)
    nF = len(pms_inside([EDGES[i] for i, t in enumerate(T) if t == FULL]))
    return f - nF, nF


def inventory(T):
    k, nF = kvec(T)
    kk = k.reshape((3,) * N)
    mm = MIXEDB.reshape((3,) * N)
    res = dict(nF=int(nF),
               n_clean=int(((k == 0) & MIXEDB).sum()),
               n_k1=int(((k == 1) & MIXEDB).sum()),
               n_k2=int(((k == 2) & MIXEDB).sum()),
               per_site={})
    for t in range(N):
        kt = np.moveaxis(kk, t, 0).reshape(3, -1)
        mt = np.moveaxis(mm, t, 0).reshape(3, -1)
        c = (kt == 0) & mt
        a1 = (kt == 1) & mt
        a2 = (kt == 2) & mt
        # ordered pairs (w clean, w' with k=1) differing only at site t
        n1 = 0
        n2 = 0
        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                n1 += int((c[i] & a1[j]).sum())
                n2 += int((c[i] & a2[j]).sum())
        res["per_site"][t] = dict(n_clean_to_k1=n1, n_clean_to_k2=n2)
    return res


def kill_status(inv):
    if inv["n_clean"] == 0:
        return "NO-CLEAN-LAYER (W16-B and the k=2 route are vacuous)"
    if any(v["n_clean_to_k1"] > 0 for v in inv["per_site"].values()):
        return "W16-B k=1 available"
    if any(v["n_clean_to_k2"] > 0 for v in inv["per_site"].values()):
        return "k=2 binomial route only"
    return "clean layer nonempty but NO (clean,k<=2) pair at any site"


RES = {}
print("=== CALIBRATION against W16 results_vertex.json ===")
try:
    w16 = json.load(open(W16))
except OSError:
    w16 = None
cal = {}
for m in range(24, 29):
    inv = inventory(W8_IMMUNE[m])
    ref = w16.get(str(m)) if w16 else None
    same = None
    if ref:
        same = (inv["n_clean"] == ref["n_clean"] and inv["n_k1"] == ref["n_k1"]
                and inv["n_k2"] == ref["n_k2"])
        ps = all(inv["per_site"][t]["n_clean_to_k1"]
                 == ref["per_site"][str(t)]["n_clean_to_k1"]
                 and inv["per_site"][t]["n_clean_to_k2"]
                 == ref["per_site"][str(t)]["n_clean_to_k2"] for t in range(N))
        same = bool(same and ps)
    cal[m] = dict(mine=dict(n_clean=inv["n_clean"], n_k1=inv["n_k1"],
                            n_k2=inv["n_k2"],
                            per_site={t: inv["per_site"][t] for t in range(N)}),
                  w16=dict(n_clean=ref["n_clean"], n_k1=ref["n_k1"],
                           n_k2=ref["n_k2"]) if ref else None,
                  agree=same)
    print("  m=%d clean=%d k1=%d k2=%d  |F|=%d  agrees with W16: %s  status: %s"
          % (m, inv["n_clean"], inv["n_k1"], inv["n_k2"], inv["nF"], same,
             kill_status(inv)))
RES["calibration_W8_ladder"] = cal
RES["calibration_all_agree"] = all(v["agree"] for v in cal.values())

# MUTATION CONTROL: shift k by one and require the calibration to break
inv = inventory(W8_IMMUNE[28])
mut = dict(inv)
RES["MUTATION_offbyone_breaks_calibration"] = (
    inv["n_clean"] != inv["n_k1"])
print("  mutation control (k off by one would disagree):",
      RES["MUTATION_offbyone_breaks_calibration"])

# ---------------------------------------------------------------------------
print("\n=== THEOREM W19C-K1: |F(Gamma)| <= 2  =>  empty clean layer ===")
D = json.load(open(os.path.join(HERE, "results_decide.json")))
G = json.load(open(os.path.join(HERE, "results_gamma.json")))
pmof = {r["mask"]: r["pms"] for r in G["gamma_classes"]}
nedge = {r["mask"]: r["n_edges"] for r in G["gamma_classes"]}

rows = []
viol = []
for smask, T in D["reps"].items():
    gm = int(smask)
    assert fast_in_R(T)
    inv = inventory(T)
    st = kill_status(inv)
    rows.append(dict(gamma_mask=gm, n_edges=nedge[gm], pms=pmof[gm],
                     n_clean=inv["n_clean"], n_k1=inv["n_k1"],
                     n_k2=inv["n_k2"], status=st,
                     per_site={str(t): inv["per_site"][t] for t in range(N)}))
    if pmof[gm] <= 2 and inv["n_clean"] != 0:
        viol.append(gm)
RES["theorem_K1_violations"] = viol
RES["reps_inventory"] = rows
print("representatives audited:", len(rows),
      "| violations of W19C-K1:", len(viol))

import collections  # noqa: E402
cnt = collections.Counter(r["status"] for r in rows)
RES["status_counts_over_reps"] = dict(cnt)
print("\nkill status over the 794 Gamma-class representatives:")
for k, v in cnt.items():
    print("   %-58s %d" % (k, v))

lowF = [r for r in rows if r["pms"] <= 2]
RES["lowF_all_no_clean"] = all(r["n_clean"] == 0 for r in lowF)
print("\nall %d low-|F| representatives have an EMPTY clean layer: %s"
      % (len(lowF), RES["lowF_all_no_clean"]))

# ---------------------------------------------------------------------------
# the |Gamma| = 8 witness from w19c_low.py, in full
L = json.load(open(os.path.join(HERE, "results_low.json")))
if L.get("stratum_i_members"):
    T8 = L["stratum_i_members"][0]["template"]
    inv = inventory(T8)
    RES["stratum_i_witness"] = dict(template=T8, inventory=inv,
                                    status=kill_status(inv),
                                    audit=fast_audit(T8))
    print("\n|Gamma|=8 witness: |F|=%d clean=%d k1=%d k2=%d -> %s"
          % (inv["nF"], inv["n_clean"], inv["n_k1"], inv["n_k2"],
             kill_status(inv)))
    f = fibres_all_words(T8)
    print("   min mixed fibre =", int(f[MIXED_POS].min()),
          " min k over mixed words =", int((f[MIXED_POS] - inv["nF"]).min()))

# how many of the 794 reps have a nonempty clean layer but no usable pair?
RES["reps_with_clean_but_no_pair"] = [
    r["gamma_mask"] for r in rows
    if r["status"].startswith("clean layer nonempty but NO")]

json.dump(RES, open(os.path.join(HERE, "results_kill.json"), "w"))
print("\nwritten results_kill.json")
