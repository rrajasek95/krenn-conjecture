#!/usr/bin/env python3
"""Exact closure22 lift on all three triangle blocks and the cap block."""

from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import audit_symbolic_triangle_cap_blocks_lift as base


RESULTS = HERE / "results_symbolic_full_triangle_cap_blocks_lift.json"
EDGES = ((0, 1), (0, 2), (1, 2), (6, 7))
PREFIXES = ("u", "v", "w", "x")
base.PARAMETERS = tuple(
    f"{prefix}{a}{b}" for prefix in PREFIXES
    for a in range(3) for b in range(3)
)
base.MARKED = {
    (edge[0], edge[1], a, b): 9 * edge_index + 3 * a + b
    for edge_index, edge in enumerate(EDGES)
    for a in range(3) for b in range(3)
}


def run_audit():
    result = base.run_audit()
    result.update({
        "status": (
            "PASS closure22 generic polynomial full-triangle-cap lift"
            if result["terminal_orders_zero"] else
            "NONTERMINAL closure22 full-triangle-cap lift"
        ),
        "marked_edges": [f"{u}{v}" for u, v in EDGES],
        "parameter_count": len(base.PARAMETERS),
        "scope": (
            "Exact over 36 independent polynomial parameters for the complete "
            "A01, A02, A12 and A67 blocks. The other 24 edge blocks remain at "
            "the physical-edge diagonal."
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
        raise RuntimeError("stored full-triangle-cap result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
