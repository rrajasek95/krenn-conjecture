#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- aggregate every band result into the verdict table.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

Reads results_band_m*_{nosingleton,closure}.json and orbits/results_m*_*.json
and prints the per-support verdict table with the kill-mechanism distribution.
"""

from __future__ import annotations

import glob
import json
import re
import sys
from collections import Counter, defaultdict


def load():
    table = defaultdict(lambda: defaultdict(dict))     # m -> mode -> orbit
    for name in glob.glob("results_band_m*_*.json"):
        match = re.match(r"results_band_m(\d+)_(\w+?)(_control)?\.json$", name)
        if not match:
            continue
        m, mode, control = int(match.group(1)), match.group(2), match.group(3)
        if control:
            continue
        data = json.load(open(name))
        for row in data["rows"]:
            table[m][mode][row["orbit"]] = row
    for name in glob.glob("orbits/results_m*_*_o*.json"):
        match = re.match(r"orbits/results_m(\d+)_(\w+)_o(\d+)\.json$", name)
        if not match:
            continue
        m, mode = int(match.group(1)), match.group(2)
        data = json.load(open(name))
        for row in data["rows"]:
            table[m][mode][row["orbit"]] = row
    return table


def main():
    table = load()
    print(f"{'m':>3} {'mode':<12} {'orbits':>7} {'UNSAT':>6} {'SAT':>5} "
          f"{'SURV':>5} {'TIMEOUT':>8}   kill mechanism distribution")
    summary = {}
    for m in sorted(table):
        for mode in ("nosingleton", "closure"):
            rows = table[m].get(mode)
            if not rows:
                continue
            tally = Counter(r["status"] for r in rows.values())
            mech = Counter()
            for r in rows.values():
                for k, v in r["verdicts"].items():
                    mech[k] += v
            print(f"{m:>3} {mode:<12} {len(rows):>7} {tally.get('UNSAT', 0):>6} "
                  f"{tally.get('SAT', 0):>5} {tally.get('SURVIVOR', 0):>5} "
                  f"{tally.get('timeout', 0):>8}   {dict(mech)}")
            summary[f"m{m}_{mode}"] = {
                "orbits_decided": len(rows), "tally": dict(tally),
                "mechanisms": dict(mech),
                "complete": len(rows) == 31 and tally.get("UNSAT", 0) == 31}
    json.dump(summary, open("results_summary.json", "w"), indent=1)
    print("\nwrote results_summary.json")
    for key, value in sorted(summary.items()):
        if value["complete"]:
            print(f"  CLOSED: {key} (31/31 orbits UNSAT)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
