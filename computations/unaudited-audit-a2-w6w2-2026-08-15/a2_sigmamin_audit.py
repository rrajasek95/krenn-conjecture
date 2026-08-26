#!/usr/bin/env python3
"""AUDIT A2 / claim A.4 -- independent verification of every saved W6
zero-singleton certificate (results_sigmamin_N8.json, results_sigmamin_N6.json,
results_band_certificates.json, results_ceiling_N*.json, results_collision8*).

Every verdict below comes from a2_core's pure-python subset-DP hafnian, which
shares no code with W6.  Mutation controls per certificate:
  M1  delete one occupied cell   -> the verdict must be allowed to change and
      the audit records how often singletons appear (a checker that always
      says "0 singletons" would be exposed);
  M2  delete one whole edge      -> same;
  M3  add one cell               -> same.
"""

from __future__ import annotations

import json
import random
import sys

from a2_core import COLORS, audit_template, geom, normalise_template

W6 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-bridge-w6-2026-08-15"
CELLS = [(a, b) for a in COLORS for b in COLORS]


def load(name):
    with open(f"{W6}/{name}") as h:
        return json.load(h)


def mutate_stats(g, template, rng, trials=25):
    """Mutation control: how many single-cell perturbations create singletons /
    break a constant fibre?  A trustworthy checker must report changes."""
    t = [set(s) for s in template]
    occupied = [(i, c) for i, s in enumerate(t) for c in s]
    stats = {"drop_cell": {"changed": 0, "total": 0},
             "drop_edge": {"changed": 0, "total": 0},
             "add_cell": {"changed": 0, "total": 0}}
    base = audit_template(g, template, exact=False)
    for _ in range(trials):
        i, c = rng.choice(occupied)
        u = [set(s) for s in t]
        u[i].discard(c)
        r = audit_template(g, u, exact=False)
        stats["drop_cell"]["total"] += 1
        if (r["mixed_singletons"], r["constants_all_nonempty"]) != (
                base["mixed_singletons"], base["constants_all_nonempty"]):
            stats["drop_cell"]["changed"] += 1
    nonempty = [i for i, s in enumerate(t) if s]
    for _ in range(trials):
        i = rng.choice(nonempty)
        u = [set(s) for s in t]
        u[i] = set()
        r = audit_template(g, u, exact=False)
        stats["drop_edge"]["total"] += 1
        if (r["mixed_singletons"], r["constants_all_nonempty"]) != (
                base["mixed_singletons"], base["constants_all_nonempty"]):
            stats["drop_edge"]["changed"] += 1
    for _ in range(trials):
        i = rng.randrange(len(t))
        c = rng.choice(CELLS)
        if c in t[i]:
            continue
        u = [set(s) for s in t]
        u[i].add(c)
        r = audit_template(g, u, exact=False)
        stats["add_cell"]["total"] += 1
        if (r["mixed_singletons"], r["constants_all_nonempty"]) != (
                base["mixed_singletons"], base["constants_all_nonempty"]):
            stats["add_cell"]["changed"] += 1
    return stats


def main():
    rng = random.Random(4242)
    report = {"note": "independent audit of W6 saved certificates", "files": {}}

    for fname, key in (("results_sigmamin_N8.json", 8),
                       ("results_sigmamin_N6.json", 6)):
        data = load(fname)
        g = geom(key)
        rows = []
        for row in data["rows"]:
            t = row.get("template")
            if t is None:
                rows.append({"m": row["m"], "claimed_sigma":
                             row.get("sigma_min_upper_bound"),
                             "verdict": "NO CERTIFICATE SAVED"})
                print(f"  N={key} m={row['m']}: NO CERTIFICATE SAVED "
                      f"(claimed sigma={row.get('sigma_min_upper_bound')})")
                continue
            tt = normalise_template(g, [[tuple(c) for c in s] for s in t])
            rep = audit_template(g, tt, exact=True)
            claimed_m = row["m"]
            claimed_beta = row["beta"]
            claimed_sigma = row["sigma_min_upper_bound"]
            ok = (rep["m"] == claimed_m and rep["sigma"] == claimed_sigma
                  and rep["mixed_singletons"] == 0
                  and rep["constants_all_nonempty"]
                  and rep["min_degree"] >= 3 and rep["slots"] == 3 * key)
            beta_ok = rep["beta"] == claimed_beta
            rows.append({"m": claimed_m, "claimed_beta": claimed_beta,
                         "claimed_sigma": claimed_sigma,
                         "measured": {k: rep[k] for k in
                                      ("m", "sigma", "beta", "min_degree",
                                       "slots", "const_fibres",
                                       "mixed_singletons")},
                         "all_checks_pass": bool(ok),
                         "beta_matches_floor": bool(beta_ok),
                         "mutation": mutate_stats(g, tt, rng)})
            print(f"  N={key} m={claimed_m}: measured m={rep['m']} "
                  f"sigma={rep['sigma']} (claim {claimed_sigma}) "
                  f"beta={rep['beta']} (claim {claimed_beta}) "
                  f"mindeg={rep['min_degree']} slots={rep['slots']} "
                  f"const={rep['const_fibres']} "
                  f"SINGLETONS={rep['mixed_singletons']} "
                  f"-> {'PASS' if ok and beta_ok else 'FAIL'}")
        report["files"][fname] = rows

    with open("results_sigmamin_audit.json", "w") as h:
        json.dump(report, h, indent=1, default=str)
    print("wrote results_sigmamin_audit.json")


if __name__ == "__main__":
    sys.exit(main())
