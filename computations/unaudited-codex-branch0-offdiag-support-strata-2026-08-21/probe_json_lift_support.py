#!/usr/bin/env python3
"""Discovery helper: print nonzero generator support of lift(I,<1>)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("interface", type=Path)
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--drop-label", action="append", default=[])
    args = parser.parse_args()
    data = json.loads(args.interface.read_text())
    kept = [(generator, label)
            for generator, label in zip(data["generators"], data["labels"])
            if label not in set(args.drop_label)]
    generators = [row[0] for row in kept]
    labels = [row[1] for row in kept]
    names = [name for name in data["variables"]
             if any(re.search(rf"\b{re.escape(name)}\b", generator)
                    for generator in generators)]
    command = (
        f"ring R={args.characteristic},({','.join(names)}),dp;"
        f"ideal I={','.join(generators)};matrix L=lift(I,ideal(1));"
        'print("BEGIN");for(int i=1;i<=nrows(L);i++)'
        '{if(L[i,1]!=0){print(i);}};print("END");quit;'
    )
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c", command], text=True,
            capture_output=True, timeout=args.timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return
    print("returncode", completed.returncode)
    lines = completed.stdout.splitlines()
    if "BEGIN" in lines and "END" in lines:
        body = lines[lines.index("BEGIN") + 1:lines.index("END")]
        indices = [int(value) - 1 for value in body]
        print("indices", indices)
        print("labels", [labels[index] for index in indices])
    print(completed.stdout[-4000:])
    print(completed.stderr[-1000:])


if __name__ == "__main__":
    main()
