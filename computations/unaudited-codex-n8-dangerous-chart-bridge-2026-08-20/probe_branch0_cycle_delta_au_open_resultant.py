#!/usr/bin/env python3
"""Diagnostic quotient-ring resultant for the Delta/Au-open packet.

This is a modular discovery probe only.  It asks Singular for the resultant
of the two source-derived consistency minors in b1 after imposing Q in the
quadratic b0 quotient.  Any discovered divisor still requires exact-Q and
full-packet replay.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_branch0_cycle_delta_au_open_generic.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def singular(poly):
    return str(poly.expand()).replace("**", "^")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--factor-norm", action="store_true")
    parser.add_argument("--raw-type", action="store_true")
    parser.add_argument("--ordinary-nested", action="store_true")
    parser.add_argument("--pair", choices=("LR", "LT", "RT"), default="LR")
    parser.add_argument("--export-nonlive", type=Path)
    args = parser.parse_args()
    audit = load("n8_cycle_delta_au_resultant_audit", AUDIT_PATH)
    source = audit.SOURCE
    rows = {label: source.expression(poly)
            for label, poly, _ in source.SOURCE.data()[0]}
    derived = audit.derive(rows)
    q, left, right = (derived[key] for key in ("q", "left", "right"))
    if args.pair != "LR":
        b0, b1, _, d1, _, d4 = source.PARAMETERS
        x = audit.sp.Symbol("x")
        normalized = audit.INTERFACE.derive(rows)[6]
        live_row_factors = (b1**2*d1**2*x, 1, 1,
                            d4**2*x, b1*x, d1*d4)
        matrix = [[audit.sp.cancel(entry/live_row_factors[row])
                   for entry in entries]
                  for row, entries in enumerate(normalized)]
        third = audit.minor_core(
            matrix, (1, 2, 3, 4), d4, derived["d4_value"], q,
            b0, b1, x, d1)
        if args.pair == "LT":
            right = third
        else:
            left, right = right, third
    norm_commands = (
        "poly r0=subst(rho,b0,0);poly r1=(rho-r0)/b0;"
        "number n0=leadcoef(r0);number n1=leadcoef(r1);"
        f"number norm=({singular(derived['a'])}*x^2)*n0^2"
        f"+({singular(derived['c'])})*n1^2;"
        'print("NBEGIN");print(numerator(norm));print("NEND");'
        'print("DBEGIN");print(denominator(norm));print("DEND");quit;'
    )
    if args.raw_type:
        terminal = ('def raw=resultant(left,right,b1);'
                    'print("TYPE");print(typeof(raw));print(size(raw));quit;')
    elif args.factor_norm:
        terminal = ("poly raw=cleardenom(resultant(left,right,b1));"
                    "poly rho=reduce(raw,G);" + norm_commands)
    elif args.summary:
        terminal = ("poly raw=cleardenom(resultant(left,right,b1));"
                    "poly rho=reduce(raw,G);"
                    'print("BEGIN");print(size(rho));print(leadexp(rho));'
                    'print("END");quit;')
    else:
        terminal = ("poly raw=cleardenom(resultant(left,right,b1));"
                    "poly rho=reduce(raw,G);"
                    'print("BEGIN");print(size(rho));print(rho);'
                    'print("END");quit;')
    if args.ordinary_nested:
        command = (
            f"ring R={args.characteristic},(b0,b1,d1,x),dp;"
            f"poly q={singular(q)};poly left={singular(left)};"
            f"poly right={singular(right)};"
            "poly rho=resultant(left,right,b1);"
            "poly N=resultant(q,rho,b0);"
            'print("ORDINARY");print(size(rho));print(size(N));'
            'print(deg(N));quit;'
        )
    else:
        command = (
            f"ring R=({args.characteristic},d1,x),(b0,b1),dp;"
            f"ideal J={singular(q)};"
            "ideal G=std(J);"
            f"poly left={singular(left)};poly right={singular(right)};"
            + terminal
        )
    try:
        completed = subprocess.run(
            ["Singular", "-q", "--no-warn"], input=command, text=True,
            capture_output=True, timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return
    print("returncode", completed.returncode)
    if not args.factor_norm:
        print(completed.stdout)
    else:
        begin = completed.stdout.index("NBEGIN\n") + len("NBEGIN\n")
        end = completed.stdout.index("\nNEND", begin)
        norm = completed.stdout[begin:end].strip()
        denominator_begin = (completed.stdout.index("DBEGIN\n", end)
                             + len("DBEGIN\n"))
        denominator_end = completed.stdout.index("\nDEND", denominator_begin)
        denominator = completed.stdout[denominator_begin:denominator_end].strip()
        print("norm bytes", len(norm))
        print("norm sha256", sha256(norm.encode("ascii")).hexdigest())
        print("denominator bytes", len(denominator))
        print("denominator sha256",
              sha256(denominator.encode("ascii")).hexdigest())
        factor_command = (
            f"ring P={args.characteristic},(d1,x),dp;"
            f"poly N={norm};poly D={denominator};"
            "list L=factorize(N);print(\"NUMERATOR\");"
            "for(int i=1;i<=size(L[1]);i++)"
            "{print(string(i)+\",\"+string(size(L[1][i]))+\",\""
            "+string(deg(L[1][i]))+\",\"+string(L[2][i]));"
            "if(deg(L[1][i])<=20){print(L[1][i]);};"
            + ('if(deg(L[1][i])>20){print("FBEGIN");'
               'print(L[1][i]);print("FEND");};'
               if args.export_nonlive else '')
            + "};"
            "L=factorize(D);print(\"DENOMINATOR\");"
            "for(int i=1;i<=size(L[1]);i++)"
            "{print(string(i)+\",\"+string(size(L[1][i]))+\",\""
            "+string(deg(L[1][i]))+\",\"+string(L[2][i]));"
            "if(deg(L[1][i])<=20){print(L[1][i]);};};quit;"
        )
        try:
            factored = subprocess.run(
                ["Singular", "-q", "--no-warn"], input=factor_command,
                text=True, capture_output=True, timeout=args.timeout,
                check=False)
        except subprocess.TimeoutExpired:
            print("FACTOR_TIMEOUT")
            return
        print("factor returncode", factored.returncode)
        if args.export_nonlive:
            factor_begin = (factored.stdout.index("FBEGIN\n")
                            + len("FBEGIN\n"))
            factor_end = factored.stdout.index("\nFEND", factor_begin)
            nonlive = factored.stdout[factor_begin:factor_end].strip()
            args.export_nonlive.write_text(nonlive + "\n")
            print("nonlive bytes", len(nonlive))
            print("nonlive sha256",
                  sha256(nonlive.encode("ascii")).hexdigest())
            printable = (factored.stdout[:factor_begin-len("FBEGIN\n")]
                         + factored.stdout[factor_end+len("\nFEND"):])
            print(printable)
        else:
            print(factored.stdout)
        if factored.stderr:
            print("FACTOR_STDERR")
            print(factored.stderr)
    if completed.stderr:
        print("STDERR")
        print(completed.stderr)


if __name__ == "__main__":
    main()
