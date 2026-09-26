#!/usr/bin/env python3
"""Independent package-auditor controls, with no imports from the proof package."""
from collections import Counter
from itertools import permutations
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def permutation_matchings(n):
    # Every perfect matching has a permutation listing its paired endpoints.
    return sorted({tuple(sorted(tuple(sorted(p[i:i + 2])) for i in range(0, n, 2)))
                   for p in permutations(range(n))})


def freeze(raw):
    return tuple(sorted(tuple(e) for e in raw))


def matching_check(root):
    data = json.loads((root / "matching8.json").read_text())
    pm = permutation_matchings(8)
    require(len(pm) == 105, "Permutation enumeration did not give 105 matchings")
    red = ((0, 1), (2, 3), (4, 5), (6, 7))
    candidates = [p for p in pm if set(p).isdisjoint(red)]
    indexed = {(freeze(c["blue"]), freeze(c["green"])): freeze(c["witness"])
               for c in data["cases"]}
    require(len(indexed) == len(data["cases"]), "Repeated certificate case")
    require(freeze(data["red"]) == red and data["n"] == 8, "Wrong normalization")
    expected = set()
    histogram = Counter()
    checks = 0
    for blue in candidates:
        for green in candidates:
            if not set(blue).isdisjoint(green):
                continue
            expected.add((blue, green))
            colors = {e: h for h, p in enumerate((red, blue, green)) for e in p}
            supported = [p for p in pm if all(e in colors for e in p)]
            extra = [p for p in supported if p not in (red, blue, green)]
            require(extra, "Counterexample to extra-matching lemma")
            histogram[len(supported)] += 1
            require(indexed.get((blue, green)) in extra, "Invalid supplied witness")
            # Check every extra matching, not just the supplied witness.
            for witness in extra:
                word = [None] * 8
                for u, v in witness:
                    word[u] = word[v] = colors[u, v]
                require(len(set(word)) > 1, "Unexpected pure extra matching")
                compatible = [p for p in pm if all(
                    e in colors and colors[e] == word[e[0]] == word[e[1]] for e in p)]
                require(compatible == [witness], "Mixed word is not unique")
                checks += 1
    require(set(indexed) == expected and len(expected) == 1884, "Coverage mismatch")
    small = permutation_matchings(4)
    require(len(small) == 3, "Four-site exception lost")
    return {"matchings": len(pm), "red_disjoint_matchings": len(candidates),
            "ordered_pairs": len(expected), "all_extra_witnesses_checked": checks,
            "union_matching_count_histogram": dict(sorted(histogram.items()))}


def add(*polynomials):
    out = Counter()
    for p in polynomials:
        for key, value in p.items():
            out[key] += value
    return {key: value for key, value in out.items() if value}


def mul(a, b):
    out = Counter()
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            out[i + k, j + l] += x * y
    return {key: value for key, value in out.items() if value}


def scale(p, c):
    return {key: c * value for key, value in p.items() if c * value}


def reflection_check():
    # Coefficientwise identities over Z[s,t], not numerical evaluations.
    s, t = {(1, 0): 1}, {(0, 1): 1}
    s2, t2, st = mul(s, s), mul(t, t), mul(s, t)
    d = add(s2, t2)
    n = [[add(s2, scale(t2, -1)), scale(st, 2)],
         [scale(st, 2), add(t2, scale(s2, -1))]]
    count = 0
    for i in range(2):
        for j in range(2):
            require(add(*(mul(n[k][i], n[k][j]) for k in range(2))) ==
                    (mul(d, d) if i == j else {}), "N^T N != D^2 I")
            count += 1
    require(add(mul(n[0][0], n[1][1]), scale(mul(n[0][1], n[1][0]), -1)) ==
            scale(mul(d, d), -1), "det N != -D^2")
    for j, variable in enumerate((s, t)):
        require(add(mul(s, n[0][j]), mul(t, n[1][j])) == mul(d, variable),
                "Reflection does not fix auxiliary combination")
    return {"coefficientwise_polynomial_equalities": count + 3}


def main():
    root = Path(__file__).resolve().parents[1] / "stronger-results-2026-09-26"
    print(json.dumps({"status": "PASS", "scope": "Independent matching proof replay and reflection controls",
                      "manifest_sha256": hashlib.sha256((root / "manifest.json").read_bytes()).hexdigest(),
                      "matching": matching_check(root), "reflection": reflection_check()}, indent=2))


if __name__ == "__main__":
    main()
