#!/usr/bin/env python3
"""Bigraded recursive lift on the deterministic dense two-shore plane."""

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
    EXPECTED_ACTIVE, VARIABLES, build_generators, polynomial, run_certificate,
)
from audit_first_edge_deviation_lift import literal_target, literal_word
from audit_two_shore_bivariate_total_lift import expansion


RESULTS = HERE / "results_two_shore_bigraded_recursive_lift.json"


def grouped(poly):
    out = defaultdict(dict)
    for (sdegree, tdegree, ykey), coefficient in expansion(poly).items():
        out[(sdegree, tdegree)][ykey] = coefficient
    return dict(out)


def pair_name(pair):
    return f"{pair[0]}_{pair[1]}"


def run_audit():
    certificate = run_certificate()
    all_generators = build_generators()
    generator_map = {
        "".join(map(str, word)): (word, projected)
        for word, projected in all_generators
    }
    closure_words = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    generators = [generator_map[word] for word in closure_words]
    projected = [item[1] for item in generators]
    row_expansions = [grouped(literal_word(item[0])) for item in generators]
    target_expansion = grouped(literal_target())
    row_bidegrees = sorted(set(
        pair for item in row_expansions for pair in item if pair != (0, 0)
    ))
    max_row_total = max(sum(pair) for pair in row_bidegrees)
    terminal_total = 9 + max_row_total

    source = [
        f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);",
        "ideal I=" + ",".join(polynomial(item) for item in projected) + ";",
        "ideal G=std(I);", "int k;",
    ]
    for pair in row_bidegrees:
        source.append(
            f"ideal D{pair_name(pair)}=" + ",".join(
                polynomial(item.get(pair, {}), signed_coefficients=True)
                for item in row_expansions
            ) + ";"
        )
    source.append("matrix M0_0[size(I)][1];")
    word_to_index = {word: index + 1 for index, word in enumerate(closure_words)}
    for word in sorted(EXPECTED_ACTIVE):
        source.append(
            f"M0_0[{word_to_index[word]},1]={certificate['active_multipliers'][word]};"
        )
    source.append('print("BEGIN_FAILURES");')
    pairs = []
    for total in range(1, terminal_total + 1):
        for sdegree in range(total + 1):
            pair = (sdegree, total - sdegree)
            pairs.append(pair)
            name = pair_name(pair)
            source.append(
                f"poly O{name}=" + polynomial(
                    target_expansion.get(pair, {}), signed_coefficients=True
                ) + ";"
            )
            for row_pair in row_bidegrees:
                if row_pair[0] > pair[0] or row_pair[1] > pair[1]:
                    continue
                previous = (pair[0] - row_pair[0], pair[1] - row_pair[1])
                source.append(
                    f"for(k=1;k<=size(I);k++){{O{name}=O{name}"
                    f"-D{pair_name(row_pair)}[k]*M{pair_name(previous)}[k,1];}}"
                )
            source.append(f"poly R{name}=reduce(O{name},G);")
            source.append(f"matrix M{name}[size(I)][1];")
            if total <= 9:
                source.append(
                    f"if(R{name}!=0){{print(\"FAIL={name}:REMAINDER\");}}"
                    f"else{{if(O{name}!=0){{M{name}=lift(I,ideal(O{name}));}}}}"
                )
            else:
                source.append(
                    f"if(O{name}!=0){{print(\"FAIL={name}:POST_DEGREE9\");}}"
                )
    source.extend(['print("END_FAILURES");', "quit;"])
    with tempfile.TemporaryDirectory(prefix="krenn-two-shore-bigraded-") as directory:
        script = Path(directory) / "two_shore_bigraded.sing"
        script.write_text("\n".join(source))
        source_bytes = script.stat().st_size
        completed = subprocess.run(
            ["Singular", "-q", str(script)], text=True, capture_output=True,
            timeout=300, check=False, stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0 or "   ?" in completed.stdout:
        raise RuntimeError(completed.stderr + completed.stdout[-8000:])
    block = completed.stdout.split("BEGIN_FAILURES\n", 1)[1].split(
        "\nEND_FAILURES", 1
    )[0]
    failures = [line.split("=", 1)[1] for line in block.splitlines()
                if line.startswith("FAIL=")]
    return {
        "status": (
            "PASS exact bigraded two-shore recursive lift"
            if not failures else
            "NONTERMINAL chosen-gauge bigraded recursion"
        ),
        "source_rows": len(generators),
        "row_bidegrees": [list(pair) for pair in row_bidegrees],
        "target_bidegrees": [list(pair) for pair in sorted(target_expansion)],
        "terminal_total_degree": terminal_total,
        "bidegrees_checked": len(pairs),
        "failures": failures,
        "failure_sha256": hashlib.sha256(
            json.dumps(failures, separators=(",", ":")).encode()
        ).hexdigest(),
        "singular_source_bytes": source_bytes,
        "scope": (
            "Exact characteristic-zero recursion on one deterministic dense "
            "two-parameter plane. A failure is gauge-dependent and is not "
            "nonmembership; a pass is a verified finite polynomial identity."
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
        raise RuntimeError("stored bigraded recursive result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
