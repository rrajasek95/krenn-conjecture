"""UNAUDITED (W11).  For every SAT support, regenerate witnesses on a known
SAT support-graph class, save them, and re-verify each one with the THIRD
independent checker in verify_witness.py (subset-DP matching count, matrix
form of (SC), brute-force matchings).
"""

import json
import os
import sys

import krenn_core as K
import per_graph as PG
import verify_witness as V

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "witnesses")


def collect(m, mask, n=3, **kw):
    os.makedirs(OUT, exist_ok=True)
    r = PG.decide_graph(mask, max_solutions=n, **kw)
    rows = []
    for k, (T, a) in enumerate(r["witnesses"]):
        path = os.path.join(OUT, "m%d_%s_%d.json" % (m, mask, k))
        json.dump(K.template_to_json(T), open(path, "w"), indent=1)
        ind = V.report(path, verbose=False)
        rows.append(dict(
            m=m, mask=mask, index=k, path=os.path.relpath(path, HERE),
            encoder_audit={kk: vv for kk, vv in a.items()
                           if kk != "singleton_examples"},
            independent=ind,
            agree=(ind["support"] == a["support"] and
                   ind["sigma"] == a["sigma"] and
                   ind["n_singletons"] == a["n_singletons"] == 0 and
                   not ind["sc_failures"] and not a["sc_failures"] and
                   ind["ADMISSIBLE_ZERO_SINGLETON"])))
    return dict(m=m, mask=mask, verdict=r["verdict"], npm=r["npm"],
                n_witnesses=len(rows), rows=rows)


if __name__ == "__main__":
    print("verify_witness selfcheck:", V.selfcheck(), flush=True)
    targets = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    allrows = []
    for m, spec in sorted(targets.items(), key=lambda kv: int(kv[0])):
        mask = spec["mask"] if isinstance(spec, dict) else spec
        kw = spec.get("kw", {}) if isinstance(spec, dict) else {}
        res = collect(int(m), mask, **kw)
        allrows.append(res)
        for row in res["rows"]:
            print("  m=%-3d mask=%-11d Sigma=%-4d singletons=%d  "
                  "(SC) ok=%s  independent_agrees=%s"
                  % (row["m"], row["mask"], row["independent"]["sigma"],
                     row["independent"]["n_singletons"],
                     not row["independent"]["sc_failures"], row["agree"]),
                  flush=True)
    json.dump(allrows, open(os.path.join(OUT, "summary.json"), "w"),
              indent=1, default=str)
    ok = all(r["agree"] for res in allrows for r in res["rows"])
    print("ALL WITNESSES INDEPENDENTLY CONFIRMED:", ok)
