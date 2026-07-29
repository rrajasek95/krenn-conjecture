#!/usr/bin/env python3
"""Build/audit the compact integral H-orbit degree-nine Macaulay matrix.

The GF(2) cache records only odd row incidences.  This companion reconstructs
the actual incidence multiplicities (0,...,15), together with row and column
orbit sizes.  It checks reduction modulo two column-by-column against the
cache used by the saved membership certificate.
"""

from __future__ import annotations

import importlib.util
import itertools
import pickle
from array import array
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_builder():
    path = HERE / "test_degree9_source_ideal_char2.py"
    spec = importlib.util.spec_from_file_location("char2_degree9", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main():
    builder = load_builder()
    with (HERE / "degree9_source_ideal_char2_h27.pkl").open("rb") as stream:
        parity_matrix = pickle.load(stream)
    expected_columns = parity_matrix["columns"]
    expected_row_codes = parity_matrix["row_codes"]
    row_lookup = {code: index for index, code in enumerate(expected_row_codes)}

    actions = builder.group_actions()

    def canonical_row(code):
        return min(
            builder.transform_code(code, edge_map) for _, _, edge_map in actions
        )

    all_colorings = set(itertools.product(range(builder.Q), repeat=builder.N))
    color_reps = []
    while all_colorings:
        coloring = min(all_colorings)
        orbit = {
            builder.transform_coloring(coloring, vertex_perm, color_perm)
            for vertex_perm, color_perm, _ in actions
        }
        all_colorings.difference_update(orbit)
        if len(set(coloring)) > 1:
            color_reps.append(coloring)

    offsets = array("Q", [0])
    row_indices = array("I")
    coefficients = bytearray()
    column_sizes = bytearray()
    column_reps = []
    column_index = 0

    for rep_number, coloring in enumerate(color_reps, 1):
        stabilizer = tuple(
            edge_map
            for vertex_perm, color_perm, edge_map in actions
            if builder.transform_coloring(coloring, vertex_perm, color_perm) == coloring
        )
        coloring_orbit_size = 27 // len(stabilizer)
        unseen = set(builder.complement_matchings(coloring))
        complement_reps = []
        complement_orbit_sizes = []
        while unseen:
            code = next(iter(unseen))
            orbit = {builder.transform_code(code, edge_map) for edge_map in stabilizer}
            unseen.difference_update(orbit)
            complement_reps.append(min(orbit))
            complement_orbit_sizes.append(len(orbit))

        f_terms = tuple(
            builder.f_matching_code(coloring, matching)
            for matching in builder.VERTEX_PMS
        )
        for complement, complement_orbit_size in zip(
            complement_reps, complement_orbit_sizes
        ):
            counts = Counter(canonical_row(complement | term) for term in f_terms)
            entries = [
                (row_lookup[code], counts[code]) for code in sorted(counts)
            ]
            parity_rows = tuple(row for row, count in entries if count & 1)
            assert set(parity_rows) == set(expected_columns[column_index]), column_index
            for row, count in entries:
                row_indices.append(row)
                coefficients.append(count)
            offsets.append(len(row_indices))
            column_sizes.append(coloring_orbit_size * complement_orbit_size)
            column_reps.append((coloring, complement))
            column_index += 1
        print(
            f"color orbit {rep_number}/{len(color_reps)}: columns={column_index}",
            flush=True,
        )

    assert column_index == len(expected_columns) == 162_672
    row_sizes = bytearray()
    for code in expected_row_codes:
        row_sizes.append(
            len({builder.transform_code(code, edge_map) for _, _, edge_map in actions})
        )
    assert all(size in (1, 3, 9, 27) for size in row_sizes)
    assert all(size in (1, 3, 9, 27) for size in column_sizes)
    assert sum(column_sizes) == 726 * 6_040
    assert sum(
        size
        for code, size in zip(expected_row_codes, row_sizes)
        if builder.is_target_monomial(code)
    ) == 15**3

    data = {
        "version": 1,
        "shape": (len(expected_row_codes), len(expected_columns)),
        "offsets": offsets,
        "row_indices": row_indices,
        "coefficients": bytes(coefficients),
        "row_sizes": bytes(row_sizes),
        "column_sizes": bytes(column_sizes),
        "column_reps": tuple(column_reps),
    }
    output = HERE / "degree9_source_ideal_h27_integer.pkl"
    with output.open("wb") as stream:
        pickle.dump(data, stream, protocol=pickle.HIGHEST_PROTOCOL)
    print(
        f"wrote {output}: shape={data['shape']} integer nnz={len(row_indices)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
