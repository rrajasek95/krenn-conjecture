#!/usr/bin/env python3
"""Independent generator: filter edge subsets, without the checker's recursion."""
from itertools import combinations
import json
from pathlib import Path


def generate():
    edges = tuple(combinations(range(8), 2))
    matchings = [p for p in combinations(edges, 4)
                 if len({v for e in p for v in e}) == 8]
    red = tuple((p, p + 1) for p in range(0, 8, 2))
    candidates = [p for p in matchings if set(p).isdisjoint(red)]
    cases = []
    for blue in candidates:
        for green in candidates:
            if not set(blue).isdisjoint(green):
                continue
            union = set(red + blue + green)
            witness = next((p for p in matchings if p not in (red, blue, green)
                            and set(p) <= union), None)
            if witness is None:
                raise ValueError("Counterexample to proposed matching lemma")
            cases.append({"blue": blue, "green": green, "witness": witness})
    return {"n": 8, "red": red, "cases": cases}


if __name__ == "__main__":
    target = Path(__file__).with_name("matching8.json")
    encoded = json.dumps(generate(), separators=(",", ":")) + "\n"
    with target.open("x", encoding="utf-8") as stream:
        stream.write(encoded)
    print("Wrote", target.name)
