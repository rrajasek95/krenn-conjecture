#!/usr/bin/env python3
"""AUDIT A6-B10: characteristic-independence corroboration.

If 1 lies in the Rabinowitsch ideal over Q, then clearing denominators gives
N*1 = sum f_i g_i over Z, so 1 lies in the ideal mod p for every p not
dividing N.  Hence a mod-p verdict of "dim != -1" (1 NOT in the ideal) for two
different primes is strong corroboration of the same verdict over Q, and the
converse direction (dim == -1 mod p while != -1 over Q) can only happen by bad
reduction.  Run on the 10 featured pairs and on the one witness pair for which
no low-height rational rank-one point was found.
"""
from __future__ import annotations

import json
import sys

HERE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a6-w15w14-2026-08-15")
P2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p2-2026-08-15")
sys.path.insert(0, HERE)
import b10_core as B  # noqa: E402

PAIRS = [(1002, (2, 5)), (1005, (0, 5)), (1005, (4, 5)), (1008, (0, 3)),
         (1008, (1, 2)), (1000, (0, 1)), (1001, (2, 3)), (1003, (1, 4)),
         (1006, (0, 5)), (1007, (3, 4)), (1005, (0, 4))]
PRIMES = [32003, 7919]


def main():
    p2 = json.load(open(P2 + "/results_a.json"))
    modes = {r["seed"]: r["mode"] for r in p2["results"]}
    rows = []
    for seed, pq in PAIRS:
        pd = B.Pair(B.gen_source(seed, modes[seed]), pq[0], pq[1])
        tag = f"{seed}_{pq[0]}{pq[1]}"
        rec = {"seed": seed, "pair": list(pq)}
        for ch in [0] + PRIMES:
            g, _, _, _ = B.decide(pd, tag, "gen", char=ch)
            r, _, _, _ = B.decide(pd, tag, "rk1", char=ch)
            rec[f"char{ch}"] = [g, r]
        rec["consistent"] = (rec["char0"] == rec[f"char{PRIMES[0]}"]
                             == rec[f"char{PRIMES[1]}"])
        rows.append(rec)
        print(f"{seed} {pq}: Q={rec['char0']} "
              f"p={PRIMES[0]}:{rec[f'char{PRIMES[0]}']} "
              f"p={PRIMES[1]}:{rec[f'char{PRIMES[1]}']} "
              f"consistent={rec['consistent']}")
    print("\nall consistent:", all(r["consistent"] for r in rows))
    json.dump({"all_consistent": all(r["consistent"] for r in rows),
               "rows": rows}, open(HERE + "/b10_modp.json", "w"), indent=1)


if __name__ == "__main__":
    main()
