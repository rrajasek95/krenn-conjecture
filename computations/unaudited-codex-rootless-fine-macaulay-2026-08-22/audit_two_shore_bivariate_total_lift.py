#!/usr/bin/env python3
"""One-shot closure22 membership on a dense two-shore bivariate plane."""

from collections import defaultdict
from itertools import combinations
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
from audit_first_edge_deviation_lift import EDGES, literal_target, literal_word


RESULTS = HERE / "results_two_shore_bivariate_total_lift.json"
LEFT = (0, 1, 2, 6, 7)
RIGHT = (3, 4, 5)
INTERNAL = set(combinations(LEFT, 2)) | set(combinations(RIGHT, 2))


def weights():
    out = {}
    for edge_index, edge in enumerate(EDGES):
        variable = 0 if edge in INTERNAL else 1
        modulus = 5 if variable == 0 else 7
        for a in range(3):
            for b in range(3):
                out[(edge[0], edge[1], a, b)] = (
                    variable, 1 + ((9 * edge_index + 3 * a + b) % modulus)
                )
    return out


def expansion(poly):
    selected = weights()
    out = defaultdict(int)
    for term, coefficient in poly.items():
        ybase = [0] * 9
        for _, _, a, b in term:
            ybase[3 * a + b] += 1
        states = {(0, 0, tuple(ybase)): coefficient}
        for cell in term:
            variable, scalar = selected[cell]
            updated = defaultdict(int)
            for (sdegree, tdegree, ykey), value in states.items():
                updated[(sdegree, tdegree, ykey)] += value
                shifted = list(ykey)
                shifted[3 * cell[2] + cell[3]] -= 1
                key = (
                    sdegree + (variable == 0),
                    tdegree + (variable == 1),
                    tuple(shifted),
                )
                updated[key] += scalar * value
            states = {key: value for key, value in updated.items() if value}
        for key, value in states.items():
            out[key] += value
    return {key: value for key, value in out.items() if value}


def polynomial(poly, modulus=None):
    pieces = []
    for (sdegree, tdegree, ykey), coefficient in sorted(poly.items()):
        if modulus:
            coefficient %= modulus
        if coefficient == 0:
            continue
        factors = []
        for variable, degree in (("s", sdegree), ("t", tdegree)):
            if degree == 1:
                factors.append(variable)
            elif degree:
                factors.append(f"{variable}^{degree}")
        for variable, degree in zip(VARIABLES, ykey):
            if degree == 1:
                factors.append(variable)
            elif degree:
                factors.append(f"{variable}^{degree}")
        pieces.append(f"({coefficient})*" + ("*".join(factors) or "1"))
    return "+".join(pieces) or "0"


def run_audit(prime, algorithm="std", timeout=300, coefficient_plane=False):
    all_generators = build_generators()
    generator_map = {
        "".join(map(str, word)): word for word, _ in all_generators
    }
    closure_words = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    rows = [expansion(literal_word(generator_map[word])) for word in closure_words]
    target = expansion(literal_target())
    ring_declaration = (
        f"ring r=({prime},s,t),({','.join(VARIABLES)}),dp;"
        if coefficient_plane else
        f"ring r={prime},({','.join(VARIABLES)},s,t),dp;"
    )
    source = [
        ring_declaration,
        "option(redSB);",
        "ideal I=" + ",".join(polynomial(row) for row in rows) + ";",
        f"ideal G={algorithm}(I);",
        "poly T=" + polynomial(target) + ";",
        "poly R=reduce(T,G);",
        'print("GBSIZE="+string(size(G)));',
        'print("ZERO="+string(R==0));',
    ]
    if coefficient_plane:
        source.extend([
            "matrix M[size(I)][1];if(R==0){M=lift(I,ideal(T));}",
            "int dc=0;poly tmp;number cf;",
            'print("BEGIN_DENOMINATORS");',
            "for(int k=1;k<=size(I);k++){tmp=M[k,1];while(tmp!=0){cf=leadcoef(tmp);"
            "if(denominator(cf)!=1){dc++;print(string(denominator(cf)));}"
            "tmp=tmp-lead(tmp);}}",
            'print("END_DENOMINATORS");',
            'print("DENOMINATOR_COUNT="+string(dc));',
            "if(matrix(I)*M-matrix(ideal(T))!=0){print(\"LIFT_VERIFY=0\");}"
            "else{print(\"LIFT_VERIFY=1\");}",
        ])
    source.append("quit;")
    with tempfile.TemporaryDirectory(prefix="krenn-two-shore-plane-") as directory:
        script = Path(directory) / "two_shore.sing"
        script.write_text("\n".join(source))
        completed = subprocess.run(
            ["Singular", "-q", str(script)], text=True, capture_output=True,
            timeout=timeout, check=False, stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0 or "   ?" in completed.stdout:
        raise RuntimeError(completed.stderr + completed.stdout[-8000:])
    result = {
        "status": (
            "PASS bivariate two-shore target membership"
            if "ZERO=1" in completed.stdout else
            "NONMEMBER bivariate two-shore target"
        ),
        "characteristic": prime,
        "groebner_algorithm": algorithm,
        "coefficient_plane": coefficient_plane,
        "source_rows": len(rows),
        "groebner_basis_size": int(
            completed.stdout.split("GBSIZE=", 1)[1].splitlines()[0]
        ),
        "remainder_zero": "ZERO=1" in completed.stdout,
        "target_terms_after_collection": len(target),
        "source_terms_after_collection": sum(map(len, rows)),
        "max_bidegree": [
            max(key[0] for key in target), max(key[1] for key in target)
        ],
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "scope": (
            "Exact finite-field membership on one deterministic dense plane: "
            "s moves all 13 within-shore blocks and t moves all 15 cross-shore "
            "blocks. This is not the full 252-parameter theorem."
        ),
    }
    if coefficient_plane:
        block = completed.stdout.split("BEGIN_DENOMINATORS\n", 1)[1].split(
            "\nEND_DENOMINATORS", 1
        )[0]
        denominators = sorted(set(line for line in block.splitlines() if line))
        dependent = [
            value for value in denominators
            if any(character.isalpha() for character in value)
        ]
        result.update({
            "lift_verified": "LIFT_VERIFY=1" in completed.stdout,
            "denominator_occurrences": int(
                completed.stdout.split("DENOMINATOR_COUNT=", 1)[1].splitlines()[0]
            ),
            "unique_denominators": denominators,
            "parameter_dependent_denominators": dependent,
        })
        if result["remainder_zero"] and result["lift_verified"] and not dependent:
            result["status"] = "PASS exact polynomial bivariate two-shore lift"
            result["scope"] = (
                "Exact characteristic-zero identity on the deterministic dense "
                "two-parameter plane. The coefficient-field lift has no "
                "parameter-dependent denominator. This remains a plane, not "
                "the full 252-parameter theorem."
            )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--algorithm", choices=("std", "slimgb"), default="std")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--coefficient-plane", action="store_true")
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit(
        args.prime, args.algorithm, args.timeout, args.coefficient_plane
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        if (args.prime != 1009 or args.algorithm != "std" or args.timeout != 300
                or args.coefficient_plane):
            raise RuntimeError("stored result is pinned to the default gate")
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored bivariate result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
