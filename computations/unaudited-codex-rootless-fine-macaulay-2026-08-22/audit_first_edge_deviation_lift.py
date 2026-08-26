#!/usr/bin/env python3
"""Test the first normal jet of the exact colour-marginal certificate.

For one labelled physical edge at a time, replace its nine cells by
``y_ab + epsilon*z_ab`` and identify every other physical edge cell with
``y_ab``.  Modulo epsilon^2 the known colour-only identity has a lift iff
the coefficient of every z_ab is in the colour-only mixed X5 ideal.

This is a first-order conormal test only.  It does not assert a lift through
higher edge-colour correlation order or to the full decorated source ring.
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
    signed,
)
from audit_physical_graph_quotient import PM8, holonomy


RESULTS = HERE / "results_first_edge_deviation_lift.json"
EDGES = tuple((u, v) for u in range(8) for v in range(u + 1, 8))


def word_term(word, matching):
    return tuple((u, v, word[u], word[v]) for u, v in matching)


def exponent(term):
    out = [0] * 9
    for _, _, a, b in term:
        out[3 * a + b] += 1
    return out


def derivative(poly, edge, colour_pair):
    """Coefficient of the marked-edge first variation at the diagonal."""
    out = defaultdict(int)
    for term, coefficient in poly.items():
        multiplicity = sum(
            1 for u, v, a, b in term
            if (u, v) == edge and (a, b) == colour_pair
        )
        if not multiplicity:
            continue
        key = exponent(term)
        index = 3 * colour_pair[0] + colour_pair[1]
        key[index] -= 1
        out[tuple(key)] += coefficient * multiplicity
    return {key: value for key, value in out.items() if value}


def literal_target():
    cone = word_term((0,) * 8, PM8[0])
    out = defaultdict(int)
    for term, coefficient in holonomy().items():
        out[tuple(sorted(term + cone))] += signed(coefficient)
    return {term: coefficient for term, coefficient in out.items() if coefficient}


def literal_word(word):
    out = defaultdict(int)
    for matching in PM8:
        out[word_term(word, matching)] += 1
    return dict(out)


def run_audit():
    certificate = run_certificate()
    multipliers = certificate["active_multipliers"]
    generators = build_generators()
    generator_by_word = {
        "".join(map(str, word)): poly for word, poly in generators
    }
    literal_generators = {
        word: literal_word(tuple(map(int, word))) for word in EXPECTED_ACTIVE
    }
    target = literal_target()

    source = [f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);"]
    source.append(
        "ideal I=" + ",".join(polynomial(poly) for _, poly in generators) + ";"
    )
    source.append("ideal G=std(I);")
    source.append('print("GBSIZE="+string(size(G)));')
    source.append("int nonzero=0;int checked=0;")
    source.append('print("BEGIN_FAILURES");')

    labels = []
    derivative_term_counts = {}
    for edge in EDGES:
        edge_label = f"{edge[0]}{edge[1]}"
        for a in range(3):
            for b in range(3):
                label = f"{edge_label}:{a}{b}"
                labels.append(label)
                target_derivative = derivative(target, edge, (a, b))
                pieces = [polynomial(target_derivative, signed_coefficients=True)]
                count = len(target_derivative)
                for word in sorted(EXPECTED_ACTIVE):
                    row_derivative = derivative(
                        literal_generators[word], edge, (a, b)
                    )
                    if row_derivative:
                        pieces.append(
                            "-(" + multipliers[word] + ")*(" +
                            polynomial(row_derivative, signed_coefficients=True) + ")"
                        )
                        count += len(row_derivative)
                derivative_term_counts[label] = count
                source.append("poly O=" + "".join(pieces) + ";")
                source.append("poly R=reduce(O,G);checked++;")
                source.append(
                    'if(R!=0){nonzero++;print("LABEL=' + label + '");print(string(R));}'
                )
    source.extend([
        'print("END_FAILURES");',
        'print("CHECKED="+string(checked));',
        'print("NONZERO="+string(nonzero));',
        "quit;",
    ])

    with tempfile.TemporaryDirectory(prefix="krenn-edge-jet-") as directory:
        script = Path(directory) / "edge_jet.sing"
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
    checked = int(stdout.split("CHECKED=", 1)[1].splitlines()[0])
    nonzero = int(stdout.split("NONZERO=", 1)[1].splitlines()[0])
    failures = stdout.split("BEGIN_FAILURES\n", 1)[1].split("\nEND_FAILURES", 1)[0]
    return {
        "status": (
            "PASS all first edge-deviation obstructions reduce to zero"
            if nonzero == 0 else
            "NONZERO first edge-deviation obstruction"
        ),
        "groebner_basis_size": int(stdout.split("GBSIZE=", 1)[1].splitlines()[0]),
        "marked_edges": len(EDGES),
        "marked_cell_directions": checked,
        "nonzero_remainders": nonzero,
        "failure_sha256": hashlib.sha256(
            (failures if nonzero else "").encode()
        ).hexdigest(),
        "maximum_raw_derivative_terms": max(derivative_term_counts.values()),
        "derivative_term_count_sha256": hashlib.sha256(
            json.dumps(derivative_term_counts, sort_keys=True).encode()
        ).hexdigest(),
        "scope": (
            "This proves only first-order lifting through each one-edge normal "
            "direction after diagonal physical-edge identification. Higher "
            "edge-correlation jets and simultaneous decorated lifting remain open."
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
        raise RuntimeError("stored first-edge-deviation result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
