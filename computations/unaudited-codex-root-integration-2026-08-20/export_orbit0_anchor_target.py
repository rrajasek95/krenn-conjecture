#!/usr/bin/env python3
"""Export orbit0 anchor or anchor-times-pure targets for sound cutoff closure.

The anchor target is a=product_{c,uv in M0} x_uv[c,c].  The valid localized
target is a*T with T=H0*H1*H2.  At a cutoff above the total degree, the closed
component decides literal membership in I_mix.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations, product
import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = (HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
             / "audit_dangerous_charts.py")
SPEC = importlib.util.spec_from_file_location("orbit0_anchor_target_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))


def site_stabilizer():
    actions = []
    for block_image in permutations(range(4)):
        for flips in product(range(2), repeat=4):
            action = [None] * 8
            for source, destination in enumerate(block_image):
                action[2 * source] = 2 * destination + flips[source]
                action[2 * source + 1] = 2 * destination + 1 - flips[source]
            actions.append(tuple(action))
    answer = tuple(sorted(actions))
    assert len(answer) == len(set(answer)) == 384
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=13)
    parser.add_argument("--target", choices=("anchor", "anchor-times-pure"),
                        default="anchor")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or HERE / (
        f"orbit0_{args.target.replace('-', '_')}_cutoff{args.cutoff}.txt"
    )

    anchors = frozenset(
        BASE.CELL_ID[(u, v, colour, colour)]
        for colour in BASE.COLORS for u, v in M0
    )
    anchor_row = bytes(sorted(anchors))
    sites = site_stabilizer()
    colours = tuple(permutations(BASE.COLORS))
    actions = tuple((site, colour) for site in sites for colour in colours)
    assert len(anchors) == 12 and len(actions) == 2304

    lines = [
        "KRENN_ANCHOR_K_SEED_V1",
        f"CUTOFF {args.cutoff}",
        "ANCHORS " + anchor_row.hex(),
        "EXPECTED 0 0 0 0 0",
    ]
    for site, colour in actions:
        lines.append("ACTION " + "".join(map(str, site)) + " "
                     + "".join(map(str, colour)))
    targets = Counter()
    if args.target == "anchor":
        targets[anchor_row] = 1
    else:
        pure_by_colour = []
        for colour in BASE.COLORS:
            by_degree = defaultdict(list)
            for row in BASE.word_terms((colour,) * BASE.N):
                by_degree[BASE.row_degree(row, anchors)].append(row)
            pure_by_colour.append(by_degree)
        for degree in range(args.cutoff):
            for degrees in product(range(degree + 1), repeat=3):
                if sum(degrees) != degree:
                    continue
                groups = tuple(pure_by_colour[colour].get(degrees[colour], ())
                               for colour in BASE.COLORS)
                for terms in product(*groups):
                    row = bytes(sorted(anchor_row + b"".join(terms)))
                    targets[row] += 1
    for row, coefficient in sorted(targets.items()):
        lines.append(f"ROW {row.hex()} {coefficient} 1")
    payload = "\n".join(lines) + "\n"
    output.write_text(payload)
    print("chart: orbit0 (three identical pure matchings)")
    print("cutoff / target:", args.cutoff, args.target)
    print("anchors:", anchor_row.hex())
    print("stabilizer order:", len(actions))
    print("raw target rows/mass:", len(targets), sum(targets.values()))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())


if __name__ == "__main__":
    main()
