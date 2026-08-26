#!/usr/bin/env python3
"""Audit literal cross-word components after target-preserving chart gauge."""

from __future__ import annotations

from collections import Counter, defaultdict
import importlib.util
import itertools
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPORTER_PATH = HERE / "export_normalized_chart_full_fibre.py"
SPEC = importlib.util.spec_from_file_location("chart_exporter", EXPORTER_PATH)
EXPORTER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(EXPORTER)


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.weight = [1] * size

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, first: int, second: int) -> None:
        first, second = self.find(first), self.find(second)
        if first == second:
            return
        if self.weight[first] < self.weight[second]:
            first, second = second, first
        self.parent[second] = first
        self.weight[first] += self.weight[second]


def audit(chart: int):
    support = EXPORTER.chart_support(chart)
    normalized = frozenset(variable for part in support for variable in part[:3])
    words = tuple(itertools.product(EXPORTER.COLOURS, repeat=8))
    union = UnionFind(len(words))
    monomial_owner = {}
    row_terms = []
    for row, word in enumerate(words):
        terms = set()
        for matching in EXPORTER.PM8:
            monomial = tuple(sorted(
                variable
                for u, v in matching
                if (variable := EXPORTER.xvar(u, v, word[u], word[v]))
                not in normalized
            ))
            terms.add(monomial)
            owner = monomial_owner.setdefault(monomial, row)
            union.union(row, owner)
        row_terms.append(len(terms))

    components = defaultdict(list)
    for row in range(len(words)):
        components[union.find(row)].append(row)
    component_monomials = Counter()
    for monomial, owner in monomial_owner.items():
        component_monomials[union.find(owner)] += 1
    records = sorted(
        (len(rows), component_monomials[root], min(words[row] for row in rows))
        for root, rows in components.items()
    )
    return {
        "chart": chart,
        "rows": len(words),
        "monomials": len(monomial_owner),
        "components": len(records),
        "row_term_histogram": dict(sorted(Counter(row_terms).items())),
        "component_row_histogram": dict(sorted(Counter(r[0] for r in records).items())),
        "component_monomial_histogram": dict(sorted(Counter(r[1] for r in records).items())),
        "largest": records[-10:],
    }


def main() -> None:
    for chart in (25, 26):
        result = audit(chart)
        print("chart", chart)
        for key, value in result.items():
            if key != "chart":
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()
