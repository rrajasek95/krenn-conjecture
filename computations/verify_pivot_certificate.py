#!/usr/bin/env python3
"""Verify the persisted triangular blocks in the filtered P^2 lift."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import pickle
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

import lift_power2_offdiag2 as L


def verify(path):
    with gzip.open(path, "rb") as fh:
        payload = fh.read()
    digest = hashlib.sha256(payload).hexdigest()
    certificate = pickle.loads(payload)
    degree = certificate["degree"]
    cone_pivots = certificate["cone_pivots"]
    noncone_pivots = certificate["noncone_pivots"]

    checkpoint = Path(f"/tmp/krenn_p2_filter_after{degree - 1}.pkl")
    with checkpoint.open("rb") as fh:
        starts = pickle.load(fh)["supports"][degree]

    cone_rows = {row for row, _, _ in cone_pivots}
    noncone_rows = {row for row, _, _ in noncone_pivots}
    assert len(cone_rows) == len(cone_pivots)
    assert len(noncone_rows) == len(noncone_pivots)
    assert cone_rows.isdisjoint(noncone_rows)
    assert starts <= cone_rows | noncone_rows

    used_columns = set()
    for row, col, coeff in cone_pivots:
        assert len(row[0]) == degree
        assert L.monomial_killed(row)
        output = Counter(L.leading_outputs(col))
        assert output == Counter({row: coeff})
        assert col not in used_columns
        used_columns.add(col)

    seen = set()
    heights = {}
    generator_types = Counter()
    dependency_counts = Counter()
    for row, col, coeff in noncone_pivots:
        assert len(row[0]) == degree
        assert not L.monomial_killed(row)
        output = Counter(L.leading_outputs(col))
        assert output[row] == coeff > 0
        assert col not in used_columns
        used_columns.add(col)
        deps = []
        for other in output:
            if other == row:
                continue
            if L.monomial_killed(other):
                assert other in cone_rows
            else:
                assert other in seen
                deps.append(other)
        heights[row] = 1 + max((heights[other] for other in deps), default=0)
        generator_types[tuple(sorted(Counter(col[0]).values(), reverse=True))] += 1
        dependency_counts[len(deps)] += 1
        seen.add(row)

    print(
        f"verified {path}: degree={degree}, cone={len(cone_pivots)}, "
        f"noncone={len(noncone_pivots)}, max_height={max(heights.values(), default=0)}, "
        f"sha256={digest}"
    )
    print(f"  generator_types={dict(generator_types)}")
    print(f"  dependency_counts={dict(dependency_counts)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = args.paths or sorted(
        Path(__file__).with_name("certificates").glob("p2_degree*_triangular.pkl.gz")
    )
    for path in paths:
        verify(path)


if __name__ == "__main__":
    main()
