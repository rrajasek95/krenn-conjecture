#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- TASK 4 calibration: reproduce W8's fibre data.

Independent pure-Python fibre engine (w12_core) vs W8's numpy engine's
PUBLISHED numbers (results_close_m20.json, results_immunity.json).
Also runs the mutation control: perturbing one cell must change the
histogram (otherwise the checker is not discriminating).
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import w12_core as C  # noqa: E402

W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")


def load_survivor():
    with open(os.path.join(W8, "results_close_m20.json")) as fh:
        data = json.load(fh)
    return tuple(data["survivors"][0])


def load_immunity():
    with open(os.path.join(W8, "results_immunity.json")) as fh:
        data = json.load(fh)
    return [(entry["m"], tuple(entry["template"]), entry["audit"])
            for entry in data["results"]]


def main():
    geo = C.geometry()
    out = {"pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read().strip()}

    # ---- target 1: the m=20 CEGAR survivor -----------------------------
    surv = load_survivor()
    a = C.audit(geo, surv)
    out["survivor"] = {"template": list(surv), "audit": a}
    expected_hist = {2: 90, 3: 42, 8: 8, 10: 12, 12: 6, 15: 1}
    out["survivor"]["w8_expected_histogram"] = expected_hist
    out["survivor"]["histogram_match"] = (a["fibre_histogram"] == expected_hist)
    out["survivor"]["expected_m_sigma_beta"] = [20, 58, 9]
    out["survivor"]["ms_match"] = ([a["m"], a["sigma"], a["beta"]] == [20, 58, 9])
    print("SURVIVOR audit:", json.dumps(a, sort_keys=True))
    print("  histogram matches W8:", out["survivor"]["histogram_match"])
    print("  m/sigma/beta match  :", out["survivor"]["ms_match"])

    # ---- target 2: the immunity family --------------------------------
    imm = load_immunity()
    rows = []
    for m, tmpl, w8audit in imm:
        mine = C.audit(geo, tmpl)
        same = all(mine[k] == w8audit[k] for k in
                   ("m", "sigma", "beta", "thin", "fat", "fie", "constants",
                    "mixed_singletons"))
        hist_same = (mine["fibre_histogram"]
                     == {int(k): v for k, v in w8audit["fibre_histogram"].items()})
        rows.append({"m": m, "audit": mine, "scalar_match": same,
                     "histogram_match": hist_same,
                     "template": list(tmpl)})
        print(f"IMMUNITY m={m}: sigma={mine['sigma']} beta={mine['beta']} "
              f"fat={mine['fat']} min_mixed={mine['min_mixed_fibre']} "
              f"live={mine['mixed_words_live']} scalars={same} hist={hist_same}")
    out["immunity"] = rows

    # ---- mutation control ---------------------------------------------
    # Removing one occupied cell of the survivor must change the histogram
    # for at least the vast majority of cells (checker is discriminating).
    changed = 0
    tested = 0
    base = C.fibre_histogram(geo, surv)
    for e, mask in enumerate(surv):
        for (i, j) in C.cells(mask):
            mutant = list(surv)
            mutant[e] = mask & ~C.bit(i, j)
            tested += 1
            if C.fibre_histogram(geo, mutant) != base:
                changed += 1
    out["mutation_control_survivor"] = {"tested": tested, "changed": changed}
    print(f"MUTATION CONTROL (survivor, delete one cell): "
          f"{changed}/{tested} change the histogram")

    # adding a cell to the immunity object must also change it
    m20 = imm[0][1]
    base20 = C.fibre_histogram(geo, m20)
    add_changed = 0
    add_tested = 0
    for e in range(len(geo.edges)):
        if m20[e] == C.FULL9:
            continue
        for c in range(9):
            if (m20[e] >> c) & 1:
                continue
            mutant = list(m20)
            mutant[e] = m20[e] | (1 << c)
            add_tested += 1
            if C.fibre_histogram(geo, mutant) != base20:
                add_changed += 1
    out["mutation_control_immunity_add"] = {"tested": add_tested,
                                            "changed": add_changed}
    print(f"MUTATION CONTROL (immunity m=20, add one cell): "
          f"{add_changed}/{add_tested} change the histogram")

    with open(os.path.join(HERE, "results_t4_calibration.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote results_t4_calibration.json")


if __name__ == "__main__":
    main()
