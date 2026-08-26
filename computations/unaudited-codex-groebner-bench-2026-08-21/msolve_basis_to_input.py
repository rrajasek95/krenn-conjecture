#!/usr/bin/env python3
"""Convert an msolve ``-g 2`` text basis into a new msolve input file.

This supports the staged workaround required by msolve 0.10.1 when native
F4SAT (``-S``) and block elimination (``-e``) cannot be combined safely.
The converter does not alter coefficients or reorder variables.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("basis")
    parser.add_argument("output")
    args = parser.parse_args()

    source = Path(args.basis).read_text()
    characteristic_match = re.search(
        r"^#field characteristic:\s*(\d+)\s*$", source, re.MULTILINE)
    variables_match = re.search(
        r"^#variable order:\s*(.*?)\s*$", source, re.MULTILINE)
    if characteristic_match is None or variables_match is None:
        raise SystemExit("missing characteristic or variable-order metadata")

    start = source.find("[")
    end = source.rfind("]")
    if start < 0 or end < start:
        raise SystemExit("missing bracketed basis")
    body = source[start + 1:end].strip()
    if body in {"", "-1"}:
        body = "1"

    variables = [value.strip() for value in
                 variables_match.group(1).split(",")]
    if any(not value for value in variables):
        raise SystemExit("invalid variable list")
    output = (",".join(variables) + "\n" +
              characteristic_match.group(1) + "\n" + body + "\n")
    Path(args.output).write_text(output)
    print(f"converted {args.basis} -> {args.output}")


if __name__ == "__main__":
    main()
