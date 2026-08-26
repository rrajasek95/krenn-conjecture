#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- cross-implementation control: W8's (FIE) checker
against audit A2's independent slice-cover checker.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

A2 (computations/unaudited-audit-a2-w6w2-2026-08-15/a2_slicecover.py) and W8
(w8_core.fie_demands) implement the same committed condition
(notes/slice-cover.md sec. 2 eq. (6)) from independent code.  Agreement on
every template W8 handles is the control.
"""
import glob, json, sys
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-audit-a2-w6w2-2026-08-15")
import w8_core as C
from a2_core import geom
from a2_slicecover import slice_cover_report


def to_cells(template):
    return [[(k // 3, k % 3) for k in range(9) if (mask >> k) & 1]
            for mask in template]


def main():
    geo = C.geometry(8)
    g = geom(8)
    templates = []
    for name in sorted(glob.glob("results_*.json")):
        try:
            data = json.load(open(name))
        except Exception:
            continue
        stack = [data]
        while stack:
            item = stack.pop()
            if isinstance(item, dict):
                for key, value in item.items():
                    if key == "template" and isinstance(value, list) \
                            and len(value) == 28 and all(isinstance(x, int)
                                                         for x in value):
                        templates.append((name, tuple(value)))
                    else:
                        stack.append(value)
            elif isinstance(item, list):
                if len(item) == 28 and all(isinstance(x, int) for x in item):
                    templates.append((name, tuple(item)))
                else:
                    stack.extend(item)
    seen, unique = set(), []
    for name, t in templates:
        if t not in seen:
            seen.add(t)
            unique.append((name, t))
    agree = disagree = 0
    rows = []
    for name, t in unique:
        mine = C.fie_ok(geo, t)
        theirs = slice_cover_report(g, to_cells(t))
        same = bool(mine) == bool(theirs["SC_ok"])
        agree += same
        disagree += not same
        rows.append({"file": name, "w8_fie": mine, "a2_sc": theirs["SC_ok"],
                     "a2_missing": theirs["n_missing"], "agree": same,
                     "a2_sharp_count_ok": theirs["sharp_count_ok"]})
    print(f"templates cross-checked: {len(unique)}; agree {agree}; "
          f"disagree {disagree}")
    admissible = sum(1 for r in rows if r["a2_sc"])
    print(f"  (SC)-admissible: {admissible}; inadmissible: "
          f"{len(rows) - admissible}")
    json.dump({"checked": len(unique), "agree": agree, "disagree": disagree,
               "rows": rows[:40]}, open("results_sc_crosscheck.json", "w"),
              indent=1)
    print("wrote results_sc_crosscheck.json")
    return 0 if disagree == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
