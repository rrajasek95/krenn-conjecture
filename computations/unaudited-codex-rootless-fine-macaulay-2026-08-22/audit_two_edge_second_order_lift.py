#!/usr/bin/env python3
"""Bounded mixed-two-edge normal-jet lift of the colour certificate.

For selected distinct labelled edges e,f, expand both edge blocks as
``y + epsilon*z_e`` and ``y + epsilon*z_f``.  Exact first-order lifts are
constructed independently, then all 81 coefficients z_e,ab*z_f,cd are
reduced modulo the colour-only X5 ideal, including the literal matching
cross-term of every source row.

Passing is a constructive second-order lift on the selected edge pair.
Failure would remain choice-dependent until first-order syzygies are added.
"""

from collections import defaultdict
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

from audit_colour_only_hamming_certificate import (
    EXPECTED_ACTIVE,
    VARIABLES,
    build_generators,
    polynomial,
    run_certificate,
)
from audit_first_edge_deviation_lift import (
    EDGES,
    derivative,
    exponent,
    literal_target,
    literal_word,
)
from audit_same_edge_second_order_lift import DIRECTIONS, direction_name


RESULTS = HERE / "results_two_edge_second_order_lift.json"
DEFAULT_PAIRS = (
    ((0, 1), (0, 2)),  # adjacent inside the response triangle
    ((0, 1), (2, 3)),  # disjoint; both occur in the fixed pure cone
    ((0, 1), (6, 7)),  # triangle edge versus cap pair
    ((0, 3), (1, 4)),  # disjoint triangle-to-outside edges
    ((0, 3), (3, 4)),  # adjacent cross/internal-outside edges
    ((3, 4), (5, 6)),  # disjoint outside/cap-incidence edges
)


def mixed_derivative(poly, left_edge, left_colour, right_edge, right_colour):
    out = defaultdict(int)
    for term, coefficient in poly.items():
        left_count = sum(
            1 for u, v, a, b in term
            if (u, v) == left_edge and (a, b) == left_colour
        )
        right_count = sum(
            1 for u, v, a, b in term
            if (u, v) == right_edge and (a, b) == right_colour
        )
        multiplicity = left_count * right_count
        if not multiplicity:
            continue
        key = exponent(term)
        key[3 * left_colour[0] + left_colour[1]] -= 1
        key[3 * right_colour[0] + right_colour[1]] -= 1
        out[tuple(key)] += coefficient * multiplicity
    return {key: value for key, value in out.items() if value}


def edge_name(edge):
    return f"{edge[0]}{edge[1]}"


def run_pair(edge_left, edge_right, generators, multipliers, target, literal_active):
    words = [word for word, _ in generators]
    projected = [poly for _, poly in generators]
    literal_rows = [literal_word(word) for word in words]
    source = [f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);"]
    source.append("ideal I=" + ",".join(polynomial(poly) for poly in projected) + ";")
    source.append("ideal G=std(I);")
    source.append("int k;int nonzero=0;int checked=0;")

    for prefix, edge in (("L", edge_left), ("R", edge_right)):
        for direction in DIRECTIONS:
            name = prefix + direction_name(direction)
            entries = [
                polynomial(derivative(row, edge, direction), signed_coefficients=True)
                for row in literal_rows
            ]
            source.append(f"ideal D{name}=" + ",".join(entries) + ";")
            pieces = [
                polynomial(derivative(target, edge, direction), signed_coefficients=True)
            ]
            for word in sorted(EXPECTED_ACTIVE):
                row_derivative = derivative(literal_active[word], edge, direction)
                if row_derivative:
                    pieces.append(
                        "-(" + multipliers[word] + ")*(" +
                        polynomial(row_derivative, signed_coefficients=True) + ")"
                    )
            source.append(f"poly O{name}=" + "".join(pieces) + ";")
            source.append(f"matrix M{name}=lift(I,ideal(O{name}));")
            source.append(
                f"if(matrix(I)*M{name}-matrix(ideal(O{name}))!=0)"
                "{print(\"FIRST_LIFT_FAILED\");exit(1);}"
            )

    source.append('print("BEGIN_FAILURES");')
    for left in DIRECTIONS:
        for right in DIRECTIONS:
            lname = direction_name(left)
            rname = direction_name(right)
            target_mixed = mixed_derivative(
                target, edge_left, left, edge_right, right
            )
            row_mixed = [
                mixed_derivative(row, edge_left, left, edge_right, right)
                for row in literal_rows
            ]
            source.append(
                "ideal X=" + ",".join(
                    polynomial(poly, signed_coefficients=True) for poly in row_mixed
                ) + ";"
            )
            source.append(
                "poly O2=" + polynomial(target_mixed, signed_coefficients=True) + ";"
            )
            for word in sorted(EXPECTED_ACTIVE):
                index = next(
                    i for i, candidate in enumerate(words)
                    if "".join(map(str, candidate)) == word
                )
                if row_mixed[index]:
                    source.append(
                        f"O2=O2-({multipliers[word]})*X[{index + 1}];"
                    )
            source.append(
                f"for(k=1;k<=size(I);k++){{O2=O2-DR{rname}[k]*ML{lname}[k,1]"
                f"-DL{lname}[k]*MR{rname}[k,1];}}"
            )
            source.append("poly R2=reduce(O2,G);checked++;")
            source.append(
                f'if(R2!=0){{nonzero++;print("{lname},{rname}");print(string(R2));}}'
            )
    source.extend([
        'print("END_FAILURES");',
        'print("CHECKED="+string(checked));',
        'print("NONZERO="+string(nonzero));',
        "quit;",
    ])
    with tempfile.TemporaryDirectory(prefix="krenn-edge-pair-jet2-") as directory:
        script = Path(directory) / "edge_pair_jet2.sing"
        script.write_text("\n".join(source))
        completed = subprocess.run(
            ["Singular", "-q", str(script)],
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
            stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr + completed.stdout[-4000:])
    stdout = completed.stdout
    if "FIRST_LIFT_FAILED" in stdout:
        raise RuntimeError("invalid first-order source lift")
    checked = int(stdout.split("CHECKED=", 1)[1].splitlines()[0])
    nonzero = int(stdout.split("NONZERO=", 1)[1].splitlines()[0])
    failures = stdout.split("BEGIN_FAILURES\n", 1)[1].split("\nEND_FAILURES", 1)[0]
    failure_labels = [
        line for line in failures.splitlines()
        if len(line) == 5 and line[2] == ","
        and all(character in "012" for character in line[:2] + line[3:])
    ]
    return {
        "checked": checked,
        "nonzero": nonzero,
        "failure_labels": failure_labels,
        "failure_sha256": hashlib.sha256(
            (failures if nonzero else "").encode()
        ).hexdigest(),
    }


def parse_pair(text):
    left, right = text.split(",")
    pair = ((int(left[0]), int(left[1])), (int(right[0]), int(right[1])))
    if pair[0] not in EDGES or pair[1] not in EDGES or pair[0] == pair[1]:
        raise argparse.ArgumentTypeError("expected two distinct canonical edges, e.g. 01,23")
    return pair


def run_audit(pairs):
    certificate = run_certificate()
    multipliers = certificate["active_multipliers"]
    generators = build_generators()
    target = literal_target()
    literal_active = {
        word: literal_word(tuple(map(int, word))) for word in EXPECTED_ACTIVE
    }
    pair_results = {}
    for left, right in pairs:
        label = edge_name(left) + "," + edge_name(right)
        pair_results[label] = run_pair(
            left, right, generators, multipliers, target, literal_active
        )
    nonzero = sum(result["nonzero"] for result in pair_results.values())
    return {
        "status": (
            "PASS selected mixed-two-edge quadratic jets"
            if nonzero == 0 else
            "NONZERO selected mixed-two-edge quadratic jet"
        ),
        "edge_pairs_checked": len(pairs),
        "mixed_directions_checked": sum(
            result["checked"] for result in pair_results.values()
        ),
        "nonzero_remainders": nonzero,
        "pair_results": pair_results,
        "scope": (
            "This is an exact bounded audit of the listed edge pairs and the "
            "specific first-order lifts returned by Singular, not an all-pair "
            "or all-order formal lifting theorem."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", action="append", type=parse_pair)
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    pairs = tuple(args.pair) if args.pair else DEFAULT_PAIRS
    result = run_audit(pairs)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        if args.pair:
            raise RuntimeError("refusing to store a custom pair run")
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored mixed-two-edge result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
