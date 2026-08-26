#!/usr/bin/env python3
"""Exhaust the full 252-direction quadratic normal layer in closure22."""

from collections import defaultdict
from itertools import combinations_with_replacement
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
    EXPECTED_ACTIVE, VARIABLES, build_generators, polynomial, run_certificate,
)
from audit_first_edge_deviation_lift import EDGES, literal_target, literal_word


RESULTS = HERE / "results_closure22_full_quadratic.json"
DIRECTIONS = tuple((edge, (a, b)) for edge in EDGES for a in range(3) for b in range(3))


def direction_name(direction):
    edge, colour = direction
    return f"{edge[0]}{edge[1]}_{colour[0]}{colour[1]}"


def add_poly(table, key, monomial, coefficient):
    row = table[key]
    row[monomial] += coefficient
    if row[monomial] == 0:
        del row[monomial]


def jets(poly):
    first = defaultdict(lambda: defaultdict(int))
    second = defaultdict(lambda: defaultdict(int))
    for term, coefficient in poly.items():
        exponent = [0] * 9
        occurrences = []
        for u, v, a, b in term:
            exponent[3 * a + b] += 1
            occurrences.append(((u, v), (a, b)))
        for index, direction in enumerate(occurrences):
            key = list(exponent)
            key[3 * direction[1][0] + direction[1][1]] -= 1
            add_poly(first, direction, tuple(key), coefficient)
            for other in occurrences[index + 1:]:
                pair = tuple(sorted((direction, other)))
                key2 = list(key)
                key2[3 * other[1][0] + other[1][1]] -= 1
                add_poly(second, pair, tuple(key2), coefficient)
    return (
        {key: dict(value) for key, value in first.items()},
        {key: dict(value) for key, value in second.items()},
    )


def run_audit():
    certificate = run_certificate()
    all_generators = build_generators()
    generator_map = {
        "".join(map(str, word)): (word, poly)
        for word, poly in all_generators
    }
    closure_words = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    generators = [generator_map[word] for word in closure_words]
    projected = [poly for _, poly in generators]
    literal_rows = [literal_word(word) for word, _ in generators]
    target_first, target_second = jets(literal_target())
    row_jets = [jets(row) for row in literal_rows]
    active_indices = {
        word: closure_words.index(word) for word in EXPECTED_ACTIVE
    }

    source = [
        f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);",
        "ideal I=" + ",".join(polynomial(poly) for poly in projected) + ";",
        "ideal G=std(I);", "int k;int checked=0;int nonzero=0;",
    ]
    for direction in DIRECTIONS:
        name = direction_name(direction)
        source.append(
            f"ideal D{name}=" + ",".join(
                polynomial(first.get(direction, {}), True)
                for first, _ in row_jets
            ) + ";"
        )
        pieces = [polynomial(target_first.get(direction, {}), True)]
        for word in sorted(EXPECTED_ACTIVE):
            row = row_jets[active_indices[word]][0].get(direction, {})
            if row:
                pieces.append(
                    "-(" + certificate["active_multipliers"][word] + ")*(" +
                    polynomial(row, True) + ")"
                )
        source.append(f"poly O{name}=" + "".join(pieces) + ";")
        source.append(f"matrix M{name}=lift(I,ideal(O{name}));")
        source.append(
            f"if(matrix(I)*M{name}-matrix(ideal(O{name}))!=0)"
            "{print(\"FIRST_LIFT_FAILED\");exit(1);}"
        )

    source.append('print("BEGIN_FAILURES");')
    for left_index, left in enumerate(DIRECTIONS):
        lname = direction_name(left)
        for right in DIRECTIONS[left_index:]:
            rname = direction_name(right)
            pair = tuple(sorted((left, right)))
            source.append(
                "poly O2=" + polynomial(target_second.get(pair, {}), True) + ";"
            )
            for word in sorted(EXPECTED_ACTIVE):
                row = row_jets[active_indices[word]][1].get(pair, {})
                if row:
                    source.append(
                        f"O2=O2-({certificate['active_multipliers'][word]})*"
                        f"({polynomial(row, True)});"
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
                f'if(R2!=0){{nonzero++;print("FAIL={lname},{rname}");}}'
            )
    source.extend([
        'print("END_FAILURES");',
        'print("CHECKED="+string(checked));',
        'print("NONZERO="+string(nonzero));',
        "quit;",
    ])
    with tempfile.TemporaryDirectory(prefix="krenn-closure22-quadratic-") as directory:
        script = Path(directory) / "closure22_quadratic.sing"
        script.write_text("\n".join(source))
        source_bytes = script.stat().st_size
        completed = subprocess.run(
            ["Singular", "-q", str(script)], text=True, capture_output=True,
            timeout=120, check=False, stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0 or "FIRST_LIFT_FAILED" in completed.stdout:
        raise RuntimeError(completed.stderr + completed.stdout[-8000:])
    failures = sorted(
        line.split("=", 1)[1] for line in completed.stdout.splitlines()
        if line.startswith("FAIL=")
    )
    checked = int(completed.stdout.split("CHECKED=", 1)[1].splitlines()[0])
    nonzero = int(completed.stdout.split("NONZERO=", 1)[1].splitlines()[0])
    assert nonzero == len(failures)
    return {
        "status": (
            "PASS closure22 contains the full quadratic normal layer"
            if nonzero == 0 else
            "NONZERO full quadratic obstruction outside closure22"
        ),
        "source_rows": len(generators),
        "normal_directions": len(DIRECTIONS),
        "quadratic_directions_checked": checked,
        "expected_quadratic_directions": len(DIRECTIONS) * (len(DIRECTIONS) + 1) // 2,
        "nonzero_remainders": nonzero,
        "failure_labels": failures,
        "failure_ledger_sha256": hashlib.sha256(
            json.dumps(failures, separators=(",", ":")).encode()
        ).hexdigest(),
        "singular_source_bytes": source_bytes,
        "scope": (
            "This exhausts all unordered degree-two monomials in the 252 "
            "literal edge-cell normal directions for the deterministic "
            "closure22 first lifts. It does not test cubic or higher normal order."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored closure22 full-quadratic result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
