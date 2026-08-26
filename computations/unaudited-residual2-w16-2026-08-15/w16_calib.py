#!/usr/bin/env python3
"""W16 T5 -- calibration: independent engine vs W8's stored audit."""
from __future__ import annotations
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (EDGES, FULL, W8_IMMUNE, audit, gamma_edges,
                      spanning_2conn, pms_of_graph, singles, word_clean,
                      full_pm_indices, extras_at, MIXED, CONSTS, support)

ROOT = "/Users/rishi/workplace/krenn-conjecture"
W8 = os.path.join(ROOT, "computations/unaudited-template-kill-w8-2026-08-15")

def main():
    j = json.load(open(os.path.join(W8, "results_immunity.json")))
    out = {"template_match": {}, "audit_match": {}, "structure": {}}
    # locate templates in the JSON
    def find_templates(o, acc):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("template", "T", "mask", "masks") and isinstance(v, list) \
                   and len(v) == 28 and all(isinstance(x, int) for x in v):
                    acc.append((k, v, o))
                else:
                    find_templates(v, acc)
        elif isinstance(o, list):
            if len(o) == 28 and all(isinstance(x, int) for x in o):
                acc.append((None, o, None))
            else:
                for v in o:
                    find_templates(v, acc)
    acc = []
    find_templates(j, acc)
    found = {}
    for k, v, parent in acc:
        m = sum(1 for x in v if x)
        found.setdefault(m, []).append(v)
    for m, T in sorted(W8_IMMUNE.items()):
        cands = found.get(m, [])
        out["template_match"][m] = any(list(c) == list(T) for c in cands)
    # audit each
    for m, T in sorted(W8_IMMUNE.items()):
        a = audit(T)
        ge = gamma_edges(T)
        out["audit_match"][m] = dict(m=a["m"], sigma=a["sigma"],
                                     min_mixed=a["min_mixed"],
                                     consts=a["consts"],
                                     hist=dict(sorted(a["hist"].items())))
        fullm = full_pm_indices(T)
        nclean = sum(1 for w in MIXED if word_clean(T, w))
        neff = sum(1 for w in MIXED if not extras_at(T, w, fullm))
        effc = [c for c in CONSTS if not extras_at(T, c, fullm)]
        k1 = sum(1 for w in MIXED if len(extras_at(T, w, fullm)) == 1)
        k2 = sum(1 for w in MIXED if len(extras_at(T, w, fullm)) == 2)
        exparity = sorted(set(len(extras_at(T, w, fullm)) for w in MIXED))
        out["structure"][m] = dict(
            gamma=[list(e) for e in ge], n_gamma=len(ge),
            gamma_pms=len(pms_of_graph(ge)),
            gamma_span2conn=spanning_2conn(ge),
            n_singles=len(singles(T)),
            singles={"%d%d" % EDGES[e]: T[e].bit_length() - 1
                     for e in singles(T)},
            other_blocks={"%d%d" % EDGES[i]: t for i, t in enumerate(T)
                          if t and t != FULL and bin(t).count("1") != 1},
            n_word_clean_mixed=nclean, n_effectively_clean_mixed=neff,
            n_effclean_consts=len(effc), k1_words=k1, k2_words=k2,
            extras_multiset=exparity)
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "results_calib.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
