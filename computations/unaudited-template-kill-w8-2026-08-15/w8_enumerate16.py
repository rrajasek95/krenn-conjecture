#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- enumerate the admissible zero-singleton templates
at support <= 16 up to S_8 x S_3, and decide every one of them.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

Only 2 of the 31 constant-witness orbits admit any zero-singleton template at
support <= 16, so the space is small enough to enumerate exactly (models are
blocked one at a time; the run is complete when the solver returns UNSAT).
"""
import json, sys, time
from collections import Counter
import numpy as np
import w8_core as C
import w8_cert as K
from w8_sat import Encoding, near_constant_words
from w8_symmetry import canonical_fast
from w8_triples import orbits


def main():
    geo = C.geometry(8)
    reps = sorted(orbits(geo))
    canonical = geo.matchings.index(tuple((2 * k, 2 * k + 1) for k in range(4)))
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 600.0
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    found, verdicts, classes = [], Counter(), {}
    complete = True
    only = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
    for number, (a, b) in enumerate(reps):
        if only is not None and number not in only:
            continue
        enc = Encoding(geo, m, "cadical153")
        for colour, matching in enumerate((canonical, a, b)):
            for u, v in geo.matchings[matching]:
                enc.solver.add_clause([enc.cell_lit(geo.index[(u, v)],
                                                    colour, colour)])
        for w in near_constant_words(geo, 2):
            enc.word_constraint(w)
        start = time.time()
        count = 0
        while True:
            if time.time() - start > budget:
                complete = False
                print(f"  orbit {number}: TIMEOUT after {count}", flush=True)
                break
            if enc.solver.solve() is False:
                break
            template = enc.decode(enc.solver.get_model())
            compat = C.compat_matrix(geo, template)
            sizes = compat.sum(axis=0, dtype=np.int64)
            bad = np.nonzero((sizes == 1) & geo.mixed)[0]
            if len(bad):
                for w in sorted(int(x) for x in bad)[:32]:
                    enc.word_constraint(w)
                continue
            cert = K.certify(geo, template, compat=compat)
            ok, _ = K.verify(geo, template, cert)
            verdicts[cert["verdict"] if ok else "UNVERIFIED"] += 1
            key = canonical_fast(geo, template)
            classes.setdefault(key, {"count": 0, "verdict": cert["verdict"],
                                     "template": list(template),
                                     "audit": C.audit(geo, template, compat)})
            classes[key]["count"] += 1
            found.append(list(template))
            count += 1
            enc.block(template)
        if count:
            print(f"  orbit {number}: {count} zero-singleton templates",
                  flush=True)
        enc.solver.delete()
    print(f"\ntotal zero-singleton templates at support <= {m}: {len(found)}")
    print(f"distinct up to S_8 x S_3: {len(classes)}")
    print("verdicts:", dict(verdicts))
    print("complete enumeration:", complete)
    for key, value in classes.items():
        a = value["audit"]
        print(f"   class: m={a['m']} Sigma={a['sigma']} beta={a['beta']} "
              f"thin={a['thin']} fat={a['fat']} copies={value['count']} "
              f"-> {value['verdict']}")
    json.dump({"m": m, "total": len(found), "orbits": len(classes),
               "verdicts": dict(verdicts), "complete": complete,
               "classes": [{"count": v["count"], "verdict": v["verdict"],
                            "audit": v["audit"], "template": v["template"]}
                           for v in classes.values()]},
              open(f"results_enumerate_m{m}.json", "w"), indent=1, default=str)
    print(f"wrote results_enumerate_m{m}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
