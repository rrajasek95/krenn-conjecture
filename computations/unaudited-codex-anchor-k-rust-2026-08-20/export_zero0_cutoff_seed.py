#!/usr/bin/env python3
"""Export raw H0H1H2 target rows for the maximally symmetric zero0 chart."""

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
SPEC = importlib.util.spec_from_file_location("anchor_k_raw", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
MATCHING = ((0, 1), (2, 3), (4, 5), (6, 7))


def site_stabilizer():
    answer = []
    for block_image in permutations(range(4)):
        for flips in product(range(2), repeat=4):
            action = [None] * 8
            for source, destination in enumerate(block_image):
                action[2 * source] = 2 * destination + flips[source]
                action[2 * source + 1] = 2 * destination + 1 - flips[source]
            answer.append(tuple(action))
    assert len(answer) == len(set(answer)) == 384
    return tuple(sorted(answer))


def target_below(cutoff, anchors):
    pure_groups = []
    for colour in BASE.COLORS:
        by_degree = defaultdict(list)
        word = (colour,) * BASE.N
        for row in BASE.word_terms(word):
            degree = BASE.row_degree(row, anchors)
            by_degree[degree].append(row)
        pure_groups.append(by_degree)
    total = Counter()
    actual_by_degree = {}
    for degree in range(cutoff):
        part = Counter()
        for degrees in product(range(degree + 1), repeat=3):
            if sum(degrees) != degree:
                continue
            for terms in product(*(pure_groups[c].get(degrees[c], ()) for c in BASE.COLORS)):
                part[bytes(sorted(b"".join(terms)))] += 1
        actual_by_degree[degree] = len(part)
        total.update(part)
    return total, actual_by_degree


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or HERE / f"zero0_cutoff{args.cutoff}_raw_seed.txt"
    anchor_cells = tuple(
        (u, v, colour, colour)
        for colour in BASE.COLORS for u, v in MATCHING
    )
    anchors = frozenset(BASE.CELL_ID[cell] for cell in anchor_cells)
    assert len(anchors) == 12
    sites = site_stabilizer()
    colours = tuple(permutations(BASE.COLORS))
    actions = tuple((site, colour) for site in sites for colour in colours)
    assert len(actions) == 2304
    target, actual_by_degree = target_below(args.cutoff, anchors)
    lines = [
        "KRENN_ANCHOR_K_SEED_V1",
        f"CUTOFF {args.cutoff}",
        "ANCHORS " + bytes(sorted(anchors)).hex(),
        "EXPECTED 0 0 0 0 0",
    ]
    for site, colour in actions:
        lines.append("ACTION " + "".join(map(str, site)) + " " + "".join(map(str, colour)))
    for row, coefficient in sorted(target.items()):
        lines.append(f"ROW {row.hex()} {coefficient} 1")
    payload = "\n".join(lines) + "\n"
    output.write_text(payload)
    print("chart: zero0 (three identical matchings)")
    print("anchors:", bytes(sorted(anchors)).hex())
    print("stabilizer order:", len(actions))
    print("actual target rows by degree:", actual_by_degree)
    print("raw target rows/mass:", len(target), sum(target.values()))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())


if __name__ == "__main__":
    main()
