#!/usr/bin/env python3
"""Minimal resolutions of the 9-row certificate and its 19-row closure."""

from pathlib import Path
import argparse
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_colour_only_hamming_certificate import (
    EXPECTED_ACTIVE, VARIABLES, build_generators, polynomial,
)


RESULTS = HERE / "results_perturbation_closure_resolution.json"


def parse_betti(text):
    return [
        [int(value) for value in line.rstrip(",").split(",")]
        for line in text.strip().splitlines()
        if line.strip()
    ]


def column_totals(table):
    return [sum(row[column] for row in table) for column in range(len(table[0]))]


def run_audit():
    closure = json.loads((HERE / "results_first_edge_lift_support.json").read_text())[
        "union_words"
    ]
    closure22 = json.loads((HERE / "results_second_order_lift_support.json").read_text())[
        "combined_closure_words"
    ]
    generator_map = {
        "".join(map(str, word)): poly for word, poly in build_generators()
    }
    packets = {
        "active9": sorted(EXPECTED_ACTIVE),
        "closure19": closure,
        "closure22": closure22,
    }
    source = [f"ring r=0,({','.join(VARIABLES)}),dp;", "option(redSB);"]
    for name, words in packets.items():
        source.append(
            f"ideal I{name}=" + ",".join(
                polynomial(generator_map[word]) for word in words
            ) + ";"
        )
        source.append(f"ideal G{name}=std(I{name});")
        source.append(f'resolution R{name}=mres(I{name},0);')
        source.append(f'print("BEGIN_{name}");')
        source.append(f'print("GB="+string(size(G{name})));')
        source.append(f'print("LENGTH="+string(size(R{name})));')
        source.append('print("BETTI");')
        source.append(f'betti(R{name});')
        source.append(f'print("END_{name}");')
    source.append("quit;")
    with tempfile.TemporaryDirectory(prefix="krenn-closure-resolution-") as directory:
        script = Path(directory) / "resolution.sing"
        script.write_text("\n".join(source))
        completed = subprocess.run(
            ["Singular", "-q", str(script)], text=True, capture_output=True,
            timeout=120, check=False, stdin=subprocess.DEVNULL,
        )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr + completed.stdout[-6000:])
    result = {}
    for name, words in packets.items():
        block = completed.stdout.split(f"BEGIN_{name}\n", 1)[1].split(
            f"\nEND_{name}", 1
        )[0]
        table = parse_betti(block.split("BETTI\n", 1)[1])
        result[name] = {
            "source_rows": len(words),
            "groebner_basis_size": int(block.split("GB=", 1)[1].splitlines()[0]),
            "resolution_length": int(block.split("LENGTH=", 1)[1].splitlines()[0]),
            "betti_table": table,
            "betti_column_totals": column_totals(table),
        }
    return {
        "status": "PASS exact minimal perturbation-closure resolutions",
        "packets": result,
        "scope": (
            "The 19-row packet is the deterministic first-normal lift closure; "
            "the 22-row packet adds the three rows forced by its exceptional "
            "quadratic remainders. Neither packet is claimed minimal or closed "
            "at every normal order."
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
        raise RuntimeError("stored closure-resolution result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
