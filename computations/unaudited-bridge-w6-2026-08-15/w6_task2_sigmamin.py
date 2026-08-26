#!/usr/bin/env python3
"""UNAUDITED PROBE (W6) -- J.1d in its USABLE form: the cell price of killing
every mixed singleton.

Pinned HEAD: 31cefe2b247450d1168abc07f6dc73318c068e44

w6_task2_focus / results_band_certificates showed that the J.1d floor
beta >= 3N - m is, by itself, compatible with zero mixed singletons at every
N = 8 support m >= 15 -- but only via templates whose non-single blocks are
CELL-RICH.  The counting lemma therefore has to be stated in cells:

    Sigma_min(N, m) := min { total cells Sigma(T) : T a support-m template
                             with beta = max(0, 3N - m) single cells,
                             the three constant fibres nonempty, every
                             (vertex,colour) slot covered, min degree >= 3,
                             and NO mixed singleton }.

    J.1d (usable):  an exact N-site source of support m with
                    Sigma(A) < Sigma_min(N, m)  has a mixed singleton, hence
                    a nonzero monomial mixed coefficient -- contradiction.

The residual hypothesis for route I is then exactly a CELL CEILING on the
band.  This module measures Sigma_min by annealing

        cost = 500*(missing constants) + 50*(mixed singletons) + Sigma,

recording the smallest Sigma seen at zero singletons.  It is an UPPER bound
on Sigma_min (a search finds templates, so the true minimum can only be
lower) -- which is the conservative direction for the lemma: the real cell
ceiling needed is at most what we report.

Run: python3 w6_task2_sigmamin.py [--size 8] [--budget SECONDS]
"""

from __future__ import annotations

import json
import math
import random
import sys
import time

from w6_task2_collision8 import geometry
import w6_task2_ceiling as CEIL

CELLS = CEIL.CELLS


def sigma(template):
    return sum(len(s) for s in template)


def cost(geo, template, m, beta):
    if not CEIL.structural_ok(geo, template, m, beta):
        return None, None
    missing, singletons = CEIL.evaluate(geo, template)
    value = 500 * missing + 50 * singletons + sigma(template)
    return value, {"missing": missing, "singletons": singletons,
                   "sigma": sigma(template)}


def anneal(geo, rng, m, beta, seconds):
    start = time.time()
    best_zero = None
    while time.time() - start < seconds:
        template = CEIL.full_warm(geo, rng, m, beta)
        if template is None:
            template, _v, _r = CEIL.seed(geo, rng, m, beta)
            if template is None:
                return None
        current, record = cost(geo, template, m, beta)
        if current is None:
            continue
        if record["singletons"] == 0 and record["missing"] == 0:
            if best_zero is None or record["sigma"] < best_zero[0]:
                best_zero = (record["sigma"], [sorted(s) for s in template])
        temperature = 25.0
        while time.time() - start < seconds:
            temperature = max(temperature * 0.99965, 0.3)
            candidate = CEIL.move(geo, rng, template, m, beta)
            if candidate is None:
                continue
            value, rec = cost(geo, candidate, m, beta)
            if value is None:
                continue
            if value <= current or rng.random() < math.exp(
                    -(value - current) / temperature):
                template, current, record = candidate, value, rec
            if rec["singletons"] == 0 and rec["missing"] == 0:
                if best_zero is None or rec["sigma"] < best_zero[0]:
                    best_zero = (rec["sigma"], [sorted(s) for s in candidate])
    return best_zero


def main():
    args = sys.argv[1:]
    size = int(args[args.index("--size") + 1]) if "--size" in args else 8
    budget = float(args[args.index("--budget") + 1]) if "--budget" in args else 45.0
    geo = geometry(size)
    rng = random.Random(20260815)
    edges = size * (size - 1) // 2
    supports = (list(range(3 * size // 2, edges + 1)) if size == 6
                else [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
    print(f"UNAUDITED PROBE (W6) -- Sigma_min at N={size}, HEAD 31cefe2",
          flush=True)
    print("   m  beta=floor  Sigma_min(upper bound)  cells/block avg  "
          "Sigma if all blocks were single cells")
    rows = []
    for m in supports:
        beta = max(0, 3 * size - m)
        best = anneal(geo, rng, m, beta, budget)
        row = {"m": m, "beta": beta,
               "sigma_min_upper_bound": None if best is None else best[0],
               "template": None if best is None else best[1]}
        rows.append(row)
        value = row["sigma_min_upper_bound"]
        print(f"  {m:2d}     {beta:3d}          "
              f"{'--' if value is None else value:>8}              "
              f"{'--' if value is None else round(value / m, 2):>6}"
              f"                {m}", flush=True)
    with open(f"results_sigmamin_N{size}.json", "w") as handle:
        json.dump({"N": size, "budget": budget, "rows": rows}, handle,
                  indent=1, default=str)
    print(f"wrote results_sigmamin_N{size}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
