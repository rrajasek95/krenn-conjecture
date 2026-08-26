#!/usr/bin/env python3
"""One-shot exact membership for scalar deformations of the colour certificate.

The recursive scalar-path checker chooses a representative for every successive
multiplier.  Such a choice is not canonical: a syzygy invisible at the current
order can control a later obstruction.  This checker avoids that gauge choice.
It substitutes the complete path into the 22-row perturbation closure and tests
the resulting ideal directly in Q[y00,...,y22,t].

This is still a one-parameter slice, not a proof for all 252 normal variables.
"""

from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_colour_only_hamming_certificate import VARIABLES, build_generators
from audit_first_edge_deviation_lift import literal_target, literal_word
from audit_scalar_path_complete_lift import ALL_PATHS, DEFAULT_PATHS, path_expansion


RESULTS = HERE / "results_scalar_path_direct_total_lift.json"


def expanded_polynomial(expansion):
    terms = []
    for degree in sorted(expansion):
        for exponents, coefficient in sorted(expansion[degree].items()):
            if not coefficient:
                continue
            factors = []
            if degree:
                factors.append("t" if degree == 1 else f"t^{degree}")
            for variable, exponent in zip(VARIABLES, exponents):
                if exponent == 1:
                    factors.append(variable)
                elif exponent:
                    factors.append(f"{variable}^{exponent}")
            monomial = "*".join(factors) or "1"
            terms.append(f"({coefficient})*{monomial}")
    return "+".join(terms) or "0"


def run_path(path, prime=0, lift_profile=False, timeout=120, modular_q=False):
    all_generators = build_generators()
    generator_map = {
        "".join(map(str, word)): (word, poly) for word, poly in all_generators
    }
    closure_words = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    generators = [generator_map[word] for word in closure_words]
    rows = [literal_word(word) for word, _ in generators]
    target = literal_target()

    row_expansions = [path_expansion(row, path) for row in rows]
    target_expansion = path_expansion(target, path)
    source = [
        f"ring r={prime},({','.join(VARIABLES)},t),dp;",
        "option(redSB);",
        "ideal I=" + ",".join(expanded_polynomial(row) for row in row_expansions) + ";",
    ]
    if modular_q:
        if prime:
            raise ValueError("modular_q requires characteristic zero")
        source.extend([
            'LIB "modstd.lib";',
            "proc finalTestSequential(string command, alias list args, def result)",
            "{",
            "  attrib(result,\"isSB\",1);",
            "  for(int j=ncols(args[1]);j>0;j--){if(reduce(args[1][j],result,1)!=0){return(0);}}",
            "  def Gcheck=std(result);",
            "  for(j=ncols(Gcheck);j>0;j--){if(reduce(Gcheck[j],result,1)!=0){return(0);}}",
            "  return(1);",
            "}",
            "ideal G=modular(\"std\",list(I),Modstd::primeTest_std,"
            "Modstd::deleteUnluckyPrimes_std,Modstd::pTest_std,finalTestSequential);",
            "attrib(G,\"isSB\",1);",
        ])
    else:
        source.append("ideal G=std(I);")
    source.extend([
        "poly T=" + expanded_polynomial(target_expansion) + ";",
        "poly R=reduce(T,G);",
        'print("BEGIN_RESULT");',
        'print("GBSIZE="+string(size(G)));',
        'print("REMAINDER_ZERO="+string(R==0));',
        'print("TARGET_DEG="+string(deg(T)));',
    ])
    if lift_profile:
        source.extend([
            "matrix M[size(I)][1];",
            "if(R==0){M=lift(I,ideal(T));}",
            "int mt=0; int md=-1;",
            "for(int k=1;k<=size(I);k++){mt=mt+size(M[k,1]);if(deg(M[k,1])>md){md=deg(M[k,1]);}}",
            'print("LIFT_TERMS="+string(mt));',
            'print("LIFT_MAX_DEG="+string(md));',
            "if(matrix(I)*M-matrix(ideal(T))!=0){print(\"LIFT_VERIFY=0\");}else{print(\"LIFT_VERIFY=1\");}",
        ])
    source.extend(['print("END_RESULT");', "quit;"])
    with tempfile.TemporaryDirectory(prefix="krenn-direct-total-") as directory:
        script = Path(directory) / "direct_total.sing"
        script.write_text("\n".join(source))
        singular_command = ["Singular", "-q"]
        if modular_q:
            singular_command.append("--cpus=1")
        singular_command.append(str(script))
        completed = subprocess.run(
            singular_command,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
            stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0 or "   ?" in completed.stdout:
        raise RuntimeError(completed.stderr + completed.stdout[-8000:])
    body = completed.stdout.split("BEGIN_RESULT\n", 1)[1].split("\nEND_RESULT", 1)[0]
    fields = dict(line.split("=", 1) for line in body.splitlines())
    result = {
        "gb_size": int(fields["GBSIZE"]),
        "remainder_zero": bool(int(fields["REMAINDER_ZERO"])),
        "target_degree": int(fields["TARGET_DEG"]),
        "source_rows": len(rows),
        "max_source_t_order": max(max(row, default=0) for row in row_expansions),
        "max_target_t_order": max(target_expansion),
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
    }
    if lift_profile:
        result.update({
            "lift_terms": int(fields["LIFT_TERMS"]),
            "lift_max_degree": int(fields["LIFT_MAX_DEG"]),
            "lift_verified": bool(int(fields["LIFT_VERIFY"])),
        })
    return result


def run_audit(paths, prime=0, lift_profile=False, timeout=120, modular_q=False):
    path_results = {
        name: run_path(path, prime, lift_profile, timeout, modular_q)
        for name, path in paths.items()
    }
    return {
        "status": (
            "PASS target belongs to every selected total deformed 22-row ideal"
            if all(result["remainder_zero"] for result in path_results.values())
            else "NONMEMBER on at least one selected total deformation"
        ),
        "paths": {
            name: [list(cell) + [scalar] for cell, scalar in path]
            for name, path in paths.items()
        },
        "path_results": path_results,
        "characteristic": prime,
        "groebner_algorithm": "modStd" if modular_q else "std",
        "scope": (
            "Exact one-shot ideal membership after scalar specialization. This "
            "does not prove membership over the full 252-variable normal base."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", choices=tuple(ALL_PATHS))
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--prime", type=int, default=0)
    parser.add_argument("--lift-profile", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--modular-q", action="store_true")
    args = parser.parse_args()
    paths = {args.path: ALL_PATHS[args.path]} if args.path else DEFAULT_PATHS
    result = run_audit(
        paths, args.prime, args.lift_profile, args.timeout, args.modular_q
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        if (args.path or args.prime or args.lift_profile or args.timeout != 120
                or args.modular_q):
            raise RuntimeError("refusing to store a specialized run")
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored direct-total result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
