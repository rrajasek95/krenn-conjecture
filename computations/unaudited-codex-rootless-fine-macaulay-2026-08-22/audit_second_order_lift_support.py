#!/usr/bin/env python3
"""Extract new colour rows needed by the four closure19 quadratic failures."""

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
from audit_first_edge_deviation_lift import derivative, literal_target, literal_word
from audit_same_edge_second_order_lift import second_derivative
from audit_same_edge_second_order_lift import run_edge
from audit_two_edge_second_order_lift import mixed_derivative, run_pair


RESULTS = HERE / "results_second_order_lift_support.json"
SAME_EDGES = ((0, 1), (0, 4), (1, 3))
MIXED_PAIR = ((0, 1), (6, 7))
DIRECTION = (2, 2)


def first_obstruction(edge, certificate, literal_active, target):
    pieces = [polynomial(derivative(target, edge, DIRECTION), True)]
    for word in sorted(EXPECTED_ACTIVE):
        row = derivative(literal_active[word], edge, DIRECTION)
        if row:
            pieces.append(
                "-(" + certificate["active_multipliers"][word] + ")*(" +
                polynomial(row, True) + ")"
            )
    return "".join(pieces)


def run_audit():
    certificate = run_certificate()
    full = build_generators()
    full_words = [word for word, _ in full]
    full_projected = [poly for _, poly in full]
    full_literal = [literal_word(word) for word in full_words]
    word_map = {"".join(map(str, word)): (word, poly) for word, poly in full}
    closure_words = json.loads(
        (HERE / "results_first_edge_lift_support.json").read_text()
    )["union_words"]
    closure = [word_map[word] for word in closure_words]
    closure_literal = [literal_word(word) for word, _ in closure]
    target = literal_target()
    literal_active = {
        word: literal_word(tuple(map(int, word))) for word in EXPECTED_ACTIVE
    }
    source = [
        f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);",
        "ideal IF=" + ",".join(polynomial(poly) for poly in full_projected) + ";",
        "ideal IC=" + ",".join(polynomial(poly) for _, poly in closure) + ";",
        "int k;", 'print("BEGIN_USES");',
    ]

    for edge in SAME_EDGES:
        label = f"same{edge[0]}{edge[1]}"
        drows = [derivative(row, edge, DIRECTION) for row in closure_literal]
        source.append("ideal D=" + ",".join(polynomial(row, True) for row in drows) + ";")
        source.append("poly O1=" + first_obstruction(edge, certificate, literal_active, target) + ";")
        source.append("matrix M=lift(IC,ideal(O1));")
        source.append("if(matrix(IC)*M-matrix(ideal(O1))!=0){print(\"FIRST_FAIL\");exit(1);}")
        source.append(
            "poly O2=" + polynomial(
                second_derivative(target, edge, DIRECTION, DIRECTION), True
            ) + ";"
        )
        source.append("for(k=1;k<=size(IC);k++){O2=O2-D[k]*M[k,1];}")
        source.append("matrix N=lift(IF,ideal(O2));")
        source.append("if(matrix(IF)*N-matrix(ideal(O2))!=0){print(\"SECOND_FAIL\");exit(1);}")
        source.append(
            f'for(k=1;k<=nrows(N);k++){{if(N[k,1]!=0)'
            f'{{print("USE={label}:"+string(k));}}}}'
        )

    left, right = MIXED_PAIR
    for prefix, edge in (("L", left), ("R", right)):
        drows = [derivative(row, edge, DIRECTION) for row in closure_literal]
        source.append(
            f"ideal D{prefix}=" + ",".join(polynomial(row, True) for row in drows) + ";"
        )
        source.append(
            f"poly O{prefix}=" + first_obstruction(
                edge, certificate, literal_active, target
            ) + ";"
        )
        source.append(f"matrix M{prefix}=lift(IC,ideal(O{prefix}));")
        source.append(
            f"if(matrix(IC)*M{prefix}-matrix(ideal(O{prefix}))!=0)"
            "{print(\"FIRST_FAIL\");exit(1);}"
        )
    mixed_rows = [
        mixed_derivative(row, left, DIRECTION, right, DIRECTION)
        for row in closure_literal
    ]
    source.append("ideal X=" + ",".join(polynomial(row, True) for row in mixed_rows) + ";")
    source.append(
        "poly O2=" + polynomial(
            mixed_derivative(target, left, DIRECTION, right, DIRECTION), True
        ) + ";"
    )
    for word in sorted(EXPECTED_ACTIVE):
        index = closure_words.index(word)
        if mixed_rows[index]:
            source.append(
                f"O2=O2-({certificate['active_multipliers'][word]})*X[{index + 1}];"
            )
    source.append(
        "for(k=1;k<=size(IC);k++){O2=O2-DR[k]*ML[k,1]-DL[k]*MR[k,1];}"
    )
    source.append("matrix N=lift(IF,ideal(O2));")
    source.append("if(matrix(IF)*N-matrix(ideal(O2))!=0){print(\"SECOND_FAIL\");exit(1);}")
    source.append(
        'for(k=1;k<=nrows(N);k++){if(N[k,1]!=0)'
        '{print("USE=mixed0167:"+string(k));}}'
    )
    source.extend(['print("END_USES");', "quit;"])

    with tempfile.TemporaryDirectory(prefix="krenn-second-lift-support-") as directory:
        script = Path(directory) / "second_lift_support.sing"
        script.write_text("\n".join(source))
        completed = subprocess.run(
            ["Singular", "-q", str(script)], text=True, capture_output=True,
            timeout=120, check=False, stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0 or "_FAIL" in completed.stdout:
        raise RuntimeError(completed.stderr + completed.stdout[-6000:])
    uses = []
    for line in completed.stdout.splitlines():
        if line.startswith("USE="):
            label, index = line.split("=", 1)[1].split(":")
            uses.append((label, int(index)))
    union_indices = sorted({index for _, index in uses})
    union_words = sorted("".join(map(str, full_words[index - 1])) for index in union_indices)
    added = sorted(set(union_words) - set(closure_words))
    combined = sorted(set(closure_words) | set(added))
    combined_generators = [word_map[word] for word in combined]
    retest = {
        f"same{edge[0]}{edge[1]}": run_edge(
            edge, combined_generators, certificate["active_multipliers"],
            target, literal_active,
        )
        for edge in SAME_EDGES
    }
    retest["mixed0167"] = run_pair(
        MIXED_PAIR[0], MIXED_PAIR[1], combined_generators,
        certificate["active_multipliers"], target, literal_active,
    )
    if any(item["nonzero"] for item in retest.values()):
        raise RuntimeError("combined second-order closure did not absorb all failures")
    return {
        "status": "PASS exact second-normal source-row closure extracted",
        "failure_directions": [
            "same01:22^2", "same04:22^2", "same13:22^2", "mixed01,67:22*22",
        ],
        "source_row_occurrences": len(uses),
        "source_rows_in_union": len(union_words),
        "additional_rows_beyond_closure19": len(added),
        "additional_words": added,
        "combined_closure_words": combined,
        "combined_closure_rows": len(combined),
        "failure_retest": retest,
        "use_ledger_sha256": hashlib.sha256(
            json.dumps(uses, separators=(",", ":")).encode()
        ).hexdigest(),
        "scope": (
            "Rows are selected by deterministic exact lifts of the four "
            "closure19 failures. This is sufficient, not minimal, and has "
            "not yet been reclosed at third order."
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
        raise RuntimeError("stored second-lift support result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
