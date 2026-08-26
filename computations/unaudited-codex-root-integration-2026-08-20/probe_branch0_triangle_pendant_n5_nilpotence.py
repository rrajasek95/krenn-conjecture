#!/usr/bin/env python3
"""Find the modular nilpotence exponent of the TP Cramer a5 numerator.

Discovery only until the resulting power membership is reconstructed and
replayed over Q.  The nine equations and N5 are derived from the exact
source-faithful minor-split helper rather than serialized modular data.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
MINOR = HERE / "probe_branch0_triangle_pendant_minor_split.py"


def load(path: Path):
    spec = importlib.util.spec_from_file_location("root_tp_minor", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


M = load(MINOR)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--bound", type=int, default=64)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--lift", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    _, split, compatibility, generic_live, _ = M.derive()
    n5 = generic_live[-1]
    variables = ",".join(map(str, M.PARAMETERS))
    rows = ",".join(M.singular(value) for _, value in compatibility)
    target = M.singular(n5)
    if args.lift:
        command = (
            f"ring R={args.characteristic},({variables}),dp;"
            f"ideal I={rows};poly N={target};ideal J=N^3;matrix U;"
            'matrix T=lift(I,J,U,"slimgb");print("BEGIN");'
            'print(nrows(T));print(ncols(T));'
            'for(int i=1;i<=nrows(T);i++){print(i);print(deg(T[i,1]));'
            'print(size(T[i,1]));};print("END");quit;')
    else:
        command = (
            f"ring R={args.characteristic},({variables}),dp;"
            f"ideal I={rows};ideal G=slimgb(I);poly N={target};"
            'print("BEGIN");print(size(G));print(dim(G));'
            f"int answer=0;for(int e=1;e<={args.bound};e++)"
            "{poly q=reduce(N^e,G);if(q==0){answer=e;break;}};"
            'print(answer);print("END");quit;')
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT after {time.monotonic()-started:.3f}s")
        return
    print("elapsed_seconds:", time.monotonic()-started)
    print("compatibility_rows:", [label for label, _ in compatibility])
    print("split_terms:", len(M.sp.Poly(split, *M.PARAMETERS).terms()))
    print("n5_terms:", len(M.sp.Poly(n5, *M.PARAMETERS).terms()))
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
