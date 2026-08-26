#!/usr/bin/env python3
"""Localized closure22 lift with the complete 5-by-3 cross shore marked."""

from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import audit_symbolic_triangle_cap_blocks_lift as base


RESULTS = HERE / "results_symbolic_cross_shore_lift.json"
LEFT = (0, 1, 2, 6, 7)
RIGHT = (3, 4, 5)
EDGES = tuple(sorted((min(u, v), max(u, v)) for u in LEFT for v in RIGHT))
base.PARAMETERS = tuple(
    f"u{edge_index}_{a}{b}" for edge_index in range(len(EDGES))
    for a in range(3) for b in range(3)
)
base.MARKED = {
    (edge[0], edge[1], a, b): 9 * edge_index + 3 * a + b
    for edge_index, edge in enumerate(EDGES)
    for a in range(3) for b in range(3)
}
base.TIMEOUT = 600
base.COEFFICIENT_PARAMETERS = True


def run_audit():
    result = base.run_audit()
    result.update({
        "status": (
            "PASS closure22 generic polynomial cross-shore lift"
            if (result["terminal_orders_zero"]
                and result["parameter_dependent_denominator_count"] == 0) else
            "PASS localized rational-function cross-shore lift"
            if result["terminal_orders_zero"] else
            "NONTERMINAL closure22 cross-shore lift"
        ),
        "marked_edges": [f"{u}{v}" for u, v in EDGES],
        "parameter_count": len(base.PARAMETERS),
        "scope": (
            "Exact over the rational-function field in 135 parameters for the "
            "complete 5-by-3 cross shore. Denominators are recorded and "
            "classified; all 13 within-shore blocks remain at the physical-edge "
            "diagonal."
        ),
    })
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored cross-shore result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
