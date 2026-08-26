#!/usr/bin/env python3
"""T2c: how the residual shape list depends on the number of composed
transfer steps.

The endgame's uniformity clause needs the construction to survive iteration
in h.  Here the same all-role insertion transfer is composed `steps` times
and the resulting Gram row is decomposed fibrewise in the residual
perfect-matching scheme.  The output is the padded shape list as a function
of (base order h, number of steps).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_stress import marked_occurrence  # noqa: E402
from t2_transfer_residuals import analyse_row  # noqa: E402
from transfer import n_step_row  # noqa: E402


def main():
    out = {}
    plan = [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2)]
    if len(sys.argv) > 1:
        plan = [tuple(int(v) for v in arg.split(",")) for arg in sys.argv[1:]]
    for h, steps in plan:
        order = h + steps
        sites = tuple(range(2 * order))
        marked = marked_occurrence(order - 1)
        row, columns = n_step_row(h, steps, marked, sites)
        print(f"base h={h}, steps={steps} -> order {order}, "
              f"columns={columns}, diagonal={row[marked]}")
        record = analyse_row(f"k^({steps})_f", row, order, marked, sites,
                             types_only=True, verbose=False)
        families = record["padded_families"]
        levels = sorted({len(f) and sum(f) // 2 or 0 for f in families})
        print(f"    padded families mu: {families}   levels present: "
              f"{sorted({sum(f)//2 for f in families})}")
        out[f"h{h}_steps{steps}"] = {
            "h": h, "steps": steps, "order": order,
            "columns": columns, "diagonal": row[marked],
            "padded_families": families,
            "levels_present": sorted({sum(f) // 2 for f in families}),
            "matching_flat": record["matching_flat"],
        }
    path = Path(__file__).resolve().parent / "t2c_step_level.json"
    path.write_text(json.dumps(out, indent=1, sort_keys=True))
    print("wrote", path)


if __name__ == "__main__":
    main()
