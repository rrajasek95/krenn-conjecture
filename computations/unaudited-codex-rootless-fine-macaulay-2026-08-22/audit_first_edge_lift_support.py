#!/usr/bin/env python3
"""Extract the source-row closure used by all first edge-deviation lifts.

The nine active colour-certificate rows are not closed under physical-edge
perturbation.  This checker uses Singular's deterministic exact lift against
all 5,210 projected mixed rows for each of the 252 first normal directions
and records the union of source rows actually used.  The result is a
candidate finite HPL/Schreyer subcomplex, not a minimal-support theorem:
different valid lifts can use different generators.
"""

from pathlib import Path
from collections import Counter
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
from audit_first_edge_deviation_lift import (
    EDGES, derivative, literal_target, literal_word,
)


RESULTS = HERE / "results_first_edge_lift_support.json"


def run_audit():
    certificate = run_certificate()
    generators = build_generators()
    words = [word for word, _ in generators]
    projected = [poly for _, poly in generators]
    literal_active = {
        word: literal_word(tuple(map(int, word))) for word in EXPECTED_ACTIVE
    }
    target = literal_target()
    source = [
        f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);",
        "ideal I=" + ",".join(polynomial(poly) for poly in projected) + ";",
        "int k;", 'print("BEGIN_USES");',
    ]
    for edge in EDGES:
        for a in range(3):
            for b in range(3):
                direction = (a, b)
                label = f"{edge[0]}{edge[1]}:{a}{b}"
                pieces = [
                    polynomial(derivative(target, edge, direction), signed_coefficients=True)
                ]
                for word in sorted(EXPECTED_ACTIVE):
                    row_derivative = derivative(literal_active[word], edge, direction)
                    if row_derivative:
                        pieces.append(
                            "-(" + certificate["active_multipliers"][word] + ")*(" +
                            polynomial(row_derivative, signed_coefficients=True) + ")"
                        )
                source.append("poly O=" + "".join(pieces) + ";")
                source.append("matrix M=lift(I,ideal(O));")
                source.append(
                    "if(matrix(I)*M-matrix(ideal(O))!=0)"
                    "{print(\"LIFT_FAILED\");exit(1);}"
                )
                source.append(
                    f'for(k=1;k<=nrows(M);k++){{if(M[k,1]!=0)'
                    f'{{print("USE={label}:"+string(k));}}}}'
                )
    source.extend(['print("END_USES");', "quit;"])
    with tempfile.TemporaryDirectory(prefix="krenn-first-lift-support-") as directory:
        script = Path(directory) / "first_lift_support.sing"
        script.write_text("\n".join(source))
        completed = subprocess.run(
            ["Singular", "-q", str(script)], text=True, capture_output=True,
            timeout=120, check=False, stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0 or "LIFT_FAILED" in completed.stdout:
        raise RuntimeError(completed.stderr + completed.stdout[-6000:])
    uses = []
    for line in completed.stdout.splitlines():
        if not line.startswith("USE="):
            continue
        payload = line.split("=", 1)[1]
        edge, colour, index = payload.split(":")
        uses.append((edge + ":" + colour, int(index)))
    by_direction = Counter(label for label, _ in uses)
    union = sorted({index for _, index in uses})
    union_words = sorted("".join(map(str, words[index - 1])) for index in union)
    added_words = sorted(set(union_words) - EXPECTED_ACTIVE)
    histogram = Counter(by_direction.values())
    return {
        "status": "PASS exact first-normal source-row closure extracted",
        "directions": len(EDGES) * 9,
        "directions_with_nonzero_correction": len(by_direction),
        "source_row_occurrences": len(uses),
        "source_rows_in_union": len(union),
        "original_active_rows_in_union": len(set(union_words) & EXPECTED_ACTIVE),
        "additional_rows_in_union": len(added_words),
        "maximum_rows_per_direction": max(by_direction.values(), default=0),
        "rows_per_direction_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "union_words": union_words,
        "additional_words": added_words,
        "use_ledger_sha256": hashlib.sha256(
            json.dumps(uses, separators=(",", ":")).encode()
        ).hexdigest(),
        "scope": (
            "This is the union selected by one deterministic exact Singular "
            "lift. It proves sufficiency for first normal corrections but not "
            "minimality or closure at higher perturbation order."
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
        raise RuntimeError("stored first-lift support result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
