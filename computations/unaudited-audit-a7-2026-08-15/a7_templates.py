#!/usr/bin/env python3
"""A7 -- independent audit of the W8 immunity templates and their fibre data.

Checks:
  (T1) transcription of W8_IMMUNE equals W8's stored results_immunity.json;
  (T2) my engine reproduces W8's stored fibre histograms exactly (m=20..28);
  (T3) Gamma / F(Gamma) / effectively-clean / word-clean counts at 24..28;
  (T4) mutation control: flipping one template bit must break (T2).
"""
from __future__ import annotations
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import (W8_IMMUNE, MIXED, CONSTS, fibre, F_gamma, k_of,
                     gamma_edges, word_clean, single_cells, template_stats,
                     EDGES, FULL)

HERE = os.path.dirname(os.path.abspath(__file__))
W8 = os.path.join(os.path.dirname(HERE),
                  "unaudited-template-kill-w8-2026-08-15",
                  "results_immunity.json")


def hist_of(T):
    h = {}
    for w in MIXED:
        s = len(fibre(T, w))
        h[s] = h.get(s, 0) + 1
    return h


def main():
    out = {}
    stored = json.load(open(W8))["results"]
    by_m = {r["m"]: r for r in stored}
    # (T1)
    t1 = {m: (list(W8_IMMUNE[m]) == list(by_m[m]["template"])) for m in W8_IMMUNE}
    out["T1_transcription_matches_W8"] = t1
    print("T1 transcription:", all(t1.values()))
    # (T2)
    t2 = {}
    for m in sorted(W8_IMMUNE):
        T = W8_IMMUNE[m]
        mine = hist_of(T)
        theirs = {int(k): v for k, v in by_m[m]["audit"]["fibre_histogram"].items()}
        t2[m] = dict(match=(mine == theirs), sigma_mine=sum(bin(t).count("1") for t in T),
                     sigma_theirs=by_m[m]["audit"]["sigma"],
                     m_mine=sum(1 for t in T if t), m_theirs=by_m[m]["audit"]["m"],
                     min_mixed_mine=min(mine), min_mixed_theirs=by_m[m]["min_mixed_fibre"],
                     consts_mine=[len(fibre(T, w)) for w in CONSTS])
        print("T2 m=%d: hist match=%s sigma %d/%d consts=%s"
              % (m, t2[m]["match"], t2[m]["sigma_mine"], t2[m]["sigma_theirs"],
                 t2[m]["consts_mine"]))
    out["T2_fibre_histograms"] = t2
    # (T3)
    t3 = {}
    for m in range(24, 29):
        T = W8_IMMUNE[m]
        st = template_stats(T)
        st["gamma"] = [list(e) for e in st["gamma"]]
        st["gamma_degrees"] = {u: sum(1 for e in gamma_edges(T) if u in e)
                               for u in range(8)}
        st["single_cells"] = {str(EDGES[e]): v for e, v in single_cells(T).items()}
        t3[m] = st
        print("T3 m=%d: |Gamma|=%d |F|=%d effclean=%d wordclean=%d minfibre=%d degs=%s"
              % (m, st["n_gamma"], st["nF"], st["n_eff_clean"], st["n_word_clean"],
                 st["min_mixed_fibre"], st["gamma_degrees"]))
    out["T3_gamma_and_clean"] = t3
    # (T4) mutation control
    T = list(W8_IMMUNE[26])
    T[0] ^= 1
    mut_ok = (hist_of(T) != {int(k): v for k, v in
                             by_m[26]["audit"]["fibre_histogram"].items()})
    out["T4_mutation_breaks_T2"] = mut_ok
    print("T4 mutation control fires:", mut_ok)
    json.dump(out, open(os.path.join(HERE, "results_templates.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
