#!/usr/bin/env python3
"""Lift the colour certificate through second order on one edge at a time.

The first-order correction is chosen by Singular's exact ``lift`` against
the 5,210-generator colour ideal.  For each labelled edge, this checker then
tests all 45 quadratic products of its nine cell-normal directions.  A zero
remainder proves existence for this recursive choice.  A nonzero remainder
would not by itself prove an obstruction, because first-order syzygy freedom
would still have to be included.
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


RESULTS = HERE / "results_same_edge_second_order_lift.json"
DIRECTIONS = tuple((a, b) for a in range(3) for b in range(3))


def second_derivative(poly, edge, left, right):
    """Coefficient of z_left*z_right (or z_left^2) at one marked edge."""
    out = defaultdict(int)
    for term, coefficient in poly.items():
        left_count = sum(
            1 for u, v, a, b in term
            if (u, v) == edge and (a, b) == left
        )
        right_count = sum(
            1 for u, v, a, b in term
            if (u, v) == edge and (a, b) == right
        )
        if left == right:
            multiplicity = left_count * (left_count - 1) // 2
        else:
            multiplicity = left_count * right_count
        if not multiplicity:
            continue
        key = exponent(term)
        key[3 * left[0] + left[1]] -= 1
        key[3 * right[0] + right[1]] -= 1
        out[tuple(key)] += coefficient * multiplicity
    return {key: value for key, value in out.items() if value}


def direction_name(direction):
    return f"{direction[0]}{direction[1]}"


def run_edge(edge, generators, multipliers, target, literal_active):
    words = [word for word, _ in generators]
    projected = [poly for _, poly in generators]
    literal_rows = [literal_word(word) for word in words]
    source = [f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);"]
    source.append("ideal I=" + ",".join(polynomial(poly) for poly in projected) + ";")
    source.append("ideal G=std(I);")
    source.append("int k;int nonzero=0;int checked=0;")

    for direction in DIRECTIONS:
        name = direction_name(direction)
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
    for left_index, left in enumerate(DIRECTIONS):
        for right in DIRECTIONS[left_index:]:
            lname = direction_name(left)
            rname = direction_name(right)
            target_second = second_derivative(target, edge, left, right)
            source.append(
                "poly O2=" + polynomial(target_second, signed_coefficients=True) + ";"
            )
            source.append(
                f"for(k=1;k<=size(I);k++){{O2=O2-D{rname}[k]*M{lname}[k,1];}}"
            )
            if left != right:
                source.append(
                    f"for(k=1;k<=size(I);k++){{O2=O2-D{lname}[k]*M{rname}[k,1];}}"
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
    with tempfile.TemporaryDirectory(prefix="krenn-edge-jet2-") as directory:
        script = Path(directory) / "edge_jet2.sing"
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


def run_audit(edge_limit=None):
    certificate = run_certificate()
    multipliers = certificate["active_multipliers"]
    generators = build_generators()
    target = literal_target()
    literal_active = {
        word: literal_word(tuple(map(int, word))) for word in EXPECTED_ACTIVE
    }
    edges = EDGES if edge_limit is None else EDGES[:edge_limit]
    edge_results = {}
    for edge in edges:
        label = f"{edge[0]}{edge[1]}"
        edge_results[label] = run_edge(
            edge, generators, multipliers, target, literal_active
        )
    nonzero = sum(result["nonzero"] for result in edge_results.values())
    return {
        "status": (
            "PASS selected recursive lift through every same-edge quadratic jet"
            if nonzero == 0 and len(edges) == len(EDGES) else
            "BOUNDED/FAIL same-edge quadratic jet audit"
        ),
        "edges_checked": len(edges),
        "quadratic_directions_checked": sum(
            result["checked"] for result in edge_results.values()
        ),
        "nonzero_remainders": nonzero,
        "edge_results": edge_results,
        "scope": (
            "Passing proves existence for the exact first-order lifts selected "
            "by Singular, one marked edge at a time. It does not include mixed "
            "two-edge jets. A failure would require a syzygy-freedom audit."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--edge-limit", type=int)
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit(args.edge_limit)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        if args.edge_limit is not None:
            raise RuntimeError("refusing to store a bounded edge-limit run")
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored same-edge second-order result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
