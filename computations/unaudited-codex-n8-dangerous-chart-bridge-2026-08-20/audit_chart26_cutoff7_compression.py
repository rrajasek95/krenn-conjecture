#!/usr/bin/env python3
"""Structural census of the exact chart-26 cutoff-7 core certificate.

This does not attempt another elimination.  It measures the affine freedom
seen by the modular rank computations, the bipartite connected components,
and obvious exact column collisions that can support cheap nullspace swaps.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUST = HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
INTERFACE = RUST / "results_chart26_cutoff7_direct.jsonl"
CERTIFICATE = RUST / "results_chart26_cutoff7_exact_core_certificate.json"
MODULAR = RUST / "results_chart26_cutoff7_solution_p1009.json"
OUT = HERE / "results_chart26_cutoff7_compression.json"


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, value):
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left, right):
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return

        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]


def histogram(values):
    return dict(sorted(Counter(values).items()))


def main():
    certificate_data = json.loads(CERTIFICATE.read_text())
    certificate = {
        int(index): Fraction(numerator, denominator)
        for index, numerator, denominator in certificate_data["coefficients"]
    }
    modular = json.loads(MODULAR.read_text())

    with INTERFACE.open() as handle:
        header = json.loads(next(handle))
        row_count = header["row_count"]
        column_count = header["column_count"]
        target_rows = {int(index) for index, _num, _den in header["target"]}
        uf = UnionFind(row_count + column_count)
        columns = []
        entry_to_columns = defaultdict(list)
        for line in handle:
            record = json.loads(line)
            index = int(record["index"])
            entries = tuple((int(row), int(value))
                            for row, value in record["entries"])
            columns.append((record["word"], tuple(record["multiplier_cell_ids"]),
                            entries))
            entry_to_columns[entries].append(index)
            column_vertex = row_count + index
            for row, _value in entries:
                uf.union(row, column_vertex)

    components = defaultdict(lambda: {
        "rows": 0,
        "columns": 0,
        "target_rows": 0,
        "certificate_columns": 0,
    })
    for row in range(row_count):
        component = components[uf.find(row)]
        component["rows"] += 1
        component["target_rows"] += row in target_rows
    for index in range(column_count):
        component = components[uf.find(row_count + index)]
        component["columns"] += 1
        component["certificate_columns"] += index in certificate

    component_rows = sorted(
        components.values(),
        key=lambda item: (-item["target_rows"], -item["rows"], -item["columns"]),
    )
    exact_collision_classes = [indices for indices in entry_to_columns.values()
                               if len(indices) > 1]
    collision_certificate_usage = []
    immediately_removable = 0
    for indices in exact_collision_classes:
        used = [index for index in indices if index in certificate]
        if len(used) > 1:
            immediately_removable += len(used) - 1
        if used:
            collision_certificate_usage.append({
                "class_size": len(indices),
                "certificate_used": len(used),
                "indices": indices,
                "coefficients": [
                    [index, certificate[index].numerator,
                     certificate[index].denominator]
                    for index in used
                ],
            })

    word_all = histogram(word for word, _multiplier, _entries in columns)
    word_certificate = histogram(columns[index][0] for index in certificate)
    support_all = histogram(sum(value for _row, value in entries)
                            for _word, _multiplier, entries in columns)
    support_certificate = histogram(
        sum(value for _row, value in columns[index][2]) for index in certificate
    )
    numerator_bits = histogram(abs(value.numerator).bit_length()
                               for value in certificate.values())
    denominator_bits = histogram(value.denominator.bit_length()
                                 for value in certificate.values())

    rank = int(modular["rank"])
    output = {
        "status": "exact structural census; rank/nullity conditional on common modular rank",
        "interface_sha256": sha256(INTERFACE.read_bytes()).hexdigest(),
        "certificate_sha256": sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "core": {
            "rows": row_count,
            "columns": column_count,
            "rank_mod_1009": rank,
            "affine_nullity_mod_1009": column_count - rank,
            "exact_rank_bounds": [rank, row_count],
            "exact_affine_nullity_bounds": [column_count - row_count,
                                            column_count - rank],
            "certificate_support": len(certificate),
        },
        "components": {
            "count": len(component_rows),
            "with_target": sum(item["target_rows"] > 0 for item in component_rows),
            "rows": component_rows,
        },
        "exact_column_collisions": {
            "classes": len(exact_collision_classes),
            "columns_in_classes": sum(map(len, exact_collision_classes)),
            "classes_touching_certificate": len(collision_certificate_usage),
            "immediately_removable_certificate_terms": immediately_removable,
            "usage": collision_certificate_usage,
        },
        "histograms": {
            "word_all": word_all,
            "word_certificate": word_certificate,
            "column_mass_all": support_all,
            "column_mass_certificate": support_certificate,
            "coefficient_numerator_bits": numerator_bits,
            "coefficient_denominator_bits": denominator_bits,
        },
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
