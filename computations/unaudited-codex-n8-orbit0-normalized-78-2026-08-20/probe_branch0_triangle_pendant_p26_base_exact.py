#!/usr/bin/env python3
"""Exact-Q probes for the minimal TP P26=0 base localization.

The input consists of the twelve exact closed Cramer rows and one expanded
Rabinowitsch row for

    F0=b0*b1*b3*d4*d5*(b1*d4+b0*d5).

`gb` proves exact emptiness if Singular returns the unit basis.  `lift` asks
for a source multiplier matrix; its output is independently replayed before
being accepted as a certificate.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_branch0_triangle_pendant_p26_boundary_msolve.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


E = load(EXPORTER, "n8_tp_p26_exporter_exact")
D = E.D
C = E.C


CORE_LABELS = (7, 8, 9, 10, 12, 15, 19, 101)


def exact_input(core: bool = False):
    data = D.cramer_branch_system(7, 12)
    rows = [(str(label), E.encode(poly)) for label, poly in data["closed_rows"]]
    if core:
        rows = [(label, poly) for label, poly in rows
                if int(label) in CORE_LABELS]
    base = data["closed_live_factors"][0]
    rab = E.encode_z_times_minus_one(base)
    return rows + [("RAB_F0", rab)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("gb", "lift", "modgb-homog"),
                        default="gb")
    parser.add_argument("--algorithm", choices=("slimgb", "std"),
                        default="slimgb")
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--core", action="store_true",
                        help="use the two-prime eight-row modular core")
    parser.add_argument("--max-exponent", type=int, default=64)
    args = parser.parse_args()
    labelled = exact_input(args.core)
    generators = [poly for _, poly in labelled]
    names = (("z", *E.VARIABLES, "t") if args.mode == "modgb-homog"
             else ("z", *E.VARIABLES))
    command = f"ring R={args.characteristic},({','.join(names)}),dp;"
    command += f"ideal I={','.join(generators)};"
    if args.mode == "gb":
        command += (f"ideal G={args.algorithm}(I);"
                    'print("BEGIN");print(size(G));print(dim(G));'
                    'print(string(reduce(1,G)));print("END");quit;')
    elif args.mode == "lift":
        # lift(I,1) is source-traceable.  Singular defines L by I*L=1;
        # print every coefficient for an independent exact replay.
        command += (
            "ideal T=1;matrix L=lift(I,T);poly check=1;"
            "int terms=0;int maxd=0;int dd;"
            "for(int i=1;i<=nrows(L);i++){"
            "check=check-I[i]*L[i,1];terms=terms+size(L[i,1]);"
            "dd=deg(I[i])+deg(L[i,1]);if(dd>maxd){maxd=dd;}"
            'print("COEFF");print(i);print(string(L[i,1]));}'
            'print("BEGIN");print(string(check));print(nrows(L));'
            'print(terms);print(maxd);print("END");quit;')
    else:
        if args.characteristic != 0:
            raise SystemExit("modgb-homog is an exact-Q probe")
        command += (
            'LIB "modstd.lib";ideal J=homog(I,t);'
            f'ideal G=modGB("{args.algorithm}",J,1);'
            'int first=0;poly q=1;'
            f'for(int e=1;e<={args.max_exponent};e++){{q=q*t;'
            'if(first==0 && reduce(q,G)==0){first=e;}}'
            'print("BEGIN");print(size(G));print(first);'
            'print(size(reduce(J,G)));print("END");quit;')
    started = time.monotonic()
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   cwd=HERE, text=True, capture_output=True,
                                   check=False, timeout=args.timeout)
        status = "completed" if completed.returncode == 0 else "process_error"
        stdout, stderr = completed.stdout, completed.stderr
        returncode = completed.returncode
        if status == "completed" and "BEGIN" not in stdout:
            status = "invalid_transcript"
    except subprocess.TimeoutExpired as error:
        status = "timeout"
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        returncode = None
    elapsed = time.monotonic() - started
    result = {
        "status": status,
        "proof_scope": "exact Q" if args.characteristic == 0 else "modular discovery",
        "mode": args.mode,
        "algorithm": args.algorithm,
        "row_selection": "eight_row_core" if args.core else "all_rows",
        "characteristic": args.characteristic,
        "max_exponent": args.max_exponent,
        "elapsed_seconds": elapsed,
        "returncode": returncode,
        "labels": [label for label, _ in labelled],
        "row_sha256": [sha256(poly.encode()).hexdigest() for _, poly in labelled],
        "stdout": stdout,
        "stderr": stderr,
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    output = args.output or HERE / (
        f"results_branch0_triangle_pendant_p26_base_exact_"
        f"{'core_' if args.core else ''}{args.mode}_"
        f"c{args.characteristic}.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(status, round(elapsed, 3), "seconds")
    print(stdout[-5000:])
    print(stderr[-1000:])
    print("result sha256", result["result_sha256"])


if __name__ == "__main__":
    main()
