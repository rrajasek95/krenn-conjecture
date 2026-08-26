#!/usr/bin/env python3
"""Drop identically zero equation coordinates from a SpaSM export.

Only columns of the transposed SpaSM matrix are removed.  Every coordinate
appearing in either the source matrix or RHS is retained, and the sorted map is
serialized and hashed.  A solution therefore replays unchanged against the
original JSONL source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sms_entries(path: Path):
    with path.open("r", encoding="ascii") as handle:
        fields = handle.readline().split()
        if len(fields) != 3 or fields[2] != "M":
            raise ValueError(f"bad SMS header in {path}")
        rows, columns = map(int, fields[:2])
        terminated = False
        for line_number, line in enumerate(handle, 2):
            values = tuple(map(int, line.split()))
            if len(values) != 3:
                raise ValueError(f"bad SMS line {line_number} in {path}")
            if values == (0, 0, 0):
                terminated = True
                if handle.readline():
                    raise ValueError(f"trailing data in {path}")
                break
            yield rows, columns, values
        if not terminated:
            raise ValueError(f"missing SMS terminator in {path}")


def temporary_text(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return tempfile.NamedTemporaryFile(
        mode="w", encoding="ascii", newline="\n", dir=path.parent,
        prefix=path.name + ".", suffix=".tmp", delete=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output_prefix", type=Path)
    args = parser.parse_args()
    source = json.loads(args.manifest.read_text())
    if source.get("format") != "krenn-macaulay-spasm-export-v1":
        raise SystemExit("unsupported export manifest")
    matrix_in, rhs_in = Path(source["matrix"]), Path(source["rhs"])
    if sha256_file(matrix_in) != source["matrix_sha256"]:
        raise SystemExit("matrix hash mismatch")
    if sha256_file(rhs_in) != source["rhs_sha256"]:
        raise SystemExit("RHS hash mismatch")
    spasm_rows, spasm_columns = map(int, source["spasm_shape"])

    active = bytearray(spasm_columns)
    matrix_nnz = 0
    for rows, columns, (_, column, _) in sms_entries(matrix_in):
        if (rows, columns) != (spasm_rows, spasm_columns):
            raise ValueError("matrix dimensions disagree with manifest")
        active[column - 1] = 1
        matrix_nnz += 1
    rhs_nnz = 0
    for rows, columns, (_, column, _) in sms_entries(rhs_in):
        if (rows, columns) != (1, spasm_columns):
            raise ValueError("RHS dimensions disagree with manifest")
        active[column - 1] = 1
        rhs_nnz += 1
    retained = [index for index, keep in enumerate(active) if keep]
    remap = [-1] * spasm_columns
    for new, old in enumerate(retained):
        remap[old] = new

    matrix_out = args.output_prefix.with_suffix(".matrix.sms")
    rhs_out = args.output_prefix.with_suffix(".rhs.sms")
    map_out = args.output_prefix.with_suffix(".equation_rows.txt")
    manifest_out = args.output_prefix.with_suffix(".manifest.json")
    matrix_tmp, rhs_tmp, map_tmp = (temporary_text(matrix_out),
                                    temporary_text(rhs_out),
                                    temporary_text(map_out))
    try:
        matrix_tmp.write(f"{spasm_rows} {len(retained)} M\n")
        for _, _, (row, column, coefficient) in sms_entries(matrix_in):
            matrix_tmp.write(f"{row} {remap[column - 1] + 1} {coefficient}\n")
        matrix_tmp.write("0 0 0\n")
        rhs_tmp.write(f"1 {len(retained)} M\n")
        for _, _, (row, column, coefficient) in sms_entries(rhs_in):
            rhs_tmp.write(f"{row} {remap[column - 1] + 1} {coefficient}\n")
        rhs_tmp.write("0 0 0\n")
        for old in retained:
            map_tmp.write(f"{old}\n")
        for temporary in (matrix_tmp, rhs_tmp, map_tmp):
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary.close()
        for temporary, output in ((matrix_tmp, matrix_out), (rhs_tmp, rhs_out),
                                  (map_tmp, map_out)):
            os.replace(temporary.name, output)
    finally:
        for temporary in (matrix_tmp, rhs_tmp, map_tmp):
            if not temporary.closed:
                temporary.close()
            if os.path.exists(temporary.name):
                os.unlink(temporary.name)

    result = dict(source)
    result.update({
        "matrix": str(matrix_out.resolve()),
        "matrix_sha256": sha256_file(matrix_out),
        "rhs": str(rhs_out.resolve()),
        "rhs_sha256": sha256_file(rhs_out),
        "spasm_shape": [spasm_rows, len(retained)],
        "matrix_nnz": matrix_nnz,
        "target_nnz": rhs_nnz,
        "equation_row_map": str(map_out.resolve()),
        "equation_row_map_sha256": sha256_file(map_out),
        "zero_equations_dropped": spasm_columns - len(retained),
        "parent_export_manifest": str(args.manifest.resolve()),
        "parent_export_manifest_sha256": sha256_file(args.manifest),
        "compression": "dropped exactly the equation coordinates absent from both matrix and RHS",
    })
    manifest_tmp = temporary_text(manifest_out)
    try:
        json.dump(result, manifest_tmp, indent=2, sort_keys=True)
        manifest_tmp.write("\n")
        manifest_tmp.flush()
        os.fsync(manifest_tmp.fileno())
        manifest_tmp.close()
        os.replace(manifest_tmp.name, manifest_out)
    finally:
        if not manifest_tmp.closed:
            manifest_tmp.close()
        if os.path.exists(manifest_tmp.name):
            os.unlink(manifest_tmp.name)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
