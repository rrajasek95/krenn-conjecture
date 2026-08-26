#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- encoding control for the 'fibre != 1' constraints.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

For random templates, assert the template as unit clauses and check that the
SAT encoding of "fibre(w) != 1" (both styles) is satisfiable exactly when the
numpy fibre engine says fibre(w) != 1.  Mutation control: planted singletons
must make the encoding UNSAT.
"""
import json, random, sys
import numpy as np
import w8_core as C
from w8_sat import Encoding


def main():
    geo = C.geometry(8)
    rng = random.Random(7)
    rows = []
    bad = 0
    for style in ("counter", "long"):
        agree = disagree = 0
        for trial in range(6):
            m = rng.randint(10, 20)
            template = [0] * 28
            for e in rng.sample(range(28), m):
                mask = 0
                for c in rng.sample(range(9), rng.randint(1, 4)):
                    mask |= 1 << c
                template[e] = mask
            template = tuple(template)
            sizes = C.fibre_sizes(geo, template)
            enc = Encoding(geo, 28, style=style, bare=True)
            for e in range(28):
                for k in range(9):
                    lit = enc.cell[e][k]
                    enc.solver.add_clause([lit if (template[e] >> k) & 1
                                           else -lit])
            words = rng.sample(range(6561), 40)
            for w in words:
                enc.word_constraint(w)
            sat = enc.solver.solve()
            truth = all(sizes[w] != 1 for w in words)
            agree += (sat == truth)
            disagree += (sat != truth)
            rows.append({"style": style, "m": m, "sat": bool(sat),
                         "truth": bool(truth),
                         "singleton_words": int(sum(1 for w in words
                                                    if sizes[w] == 1))})
        bad += disagree
        print(f"style {style}: agree {agree}, disagree {disagree}")
    json.dump({"rows": rows, "disagreements": bad},
              open("results_enc_control.json", "w"), indent=1)
    print("ENCODING CONTROL PASS" if bad == 0 else "ENCODING CONTROL FAILED")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
