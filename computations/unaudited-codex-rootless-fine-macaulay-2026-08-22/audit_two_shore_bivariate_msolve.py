#!/usr/bin/env python3
"""Compiled F4 normal-form gate for the dense two-shore bivariate plane."""

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
from audit_two_shore_bivariate_total_lift import expansion, polynomial


RESULTS = HERE / "results_two_shore_bivariate_msolve.json"


def run_audit(prime=1009, timeout=300, mutate_target=False):
    generator_map = {
        "".join(map(str, word)): word for word, _ in build_generators()
    }
    closure_words = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    rows = [polynomial(expansion(literal_word(generator_map[word])), prime)
            for word in closure_words]
    target = polynomial(expansion(literal_target()), prime)
    rows = [row.replace("(", "").replace(")", "") for row in rows]
    target = target.replace("(", "").replace(")", "")
    if mutate_target:
        target += "+1"
    with tempfile.TemporaryDirectory(prefix="krenn-two-shore-msolve-") as directory:
        directory = Path(directory)
        input_path = directory / "input.ms"
        output_path = directory / "output.ms"
        input_path.write_text(
            ",".join(VARIABLES + ("s", "t")) + "\n" +
            str(prime) + "\n" +
            ",\n".join(rows + [target]) + "\n"
        )
        input_bytes = input_path.stat().st_size
        completed = subprocess.run(
            ["msolve", "-f", str(input_path), "-o", str(output_path),
             "-n", "1", "-t", "1", "-v", "1", "--random-seed", "0"],
            text=True, capture_output=True, timeout=timeout, check=False,
            stdin=subprocess.DEVNULL,
        )
        output = output_path.read_text() if output_path.exists() else ""
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr + completed.stdout[-8000:])
    # Normal-form mode prints the normal form in the output packet.  Keep the
    # raw digest and a conservative textual zero classifier; hostile nonzero
    # controls are checked separately before this is promoted to a theorem.
    compact = "".join(output.split())
    zero_markers = ("[0]", "0", "[0,]", "[0]:")
    zero = compact in zero_markers or compact.endswith("[0]")
    stable_stat_labels = (
        "size of basis", "#terms in basis", "#pairs reduced",
        "#redundant elements", "#rows reduced", "#zero reductions",
        "max. matrix data",
    )
    stable_stats = {}
    for line in completed.stderr.splitlines():
        stripped = line.strip()
        for label in stable_stat_labels:
            if stripped.startswith(label):
                stable_stats[label] = stripped[len(label):].strip()
    return {
        "status": (
            "PASS hostile mutation has nonzero normal form"
            if mutate_target and not zero else
            "PASS msolve reports zero bivariate normal form"
            if not mutate_target and zero else
            "UNEXPECTED msolve normal-form verdict"
        ),
        "characteristic": prime,
        "source_rows": len(rows),
        "input_bytes": input_bytes,
        "target_terms_after_collection": len(expansion(literal_target())),
        "msolve_returncode": completed.returncode,
        "msolve_stable_statistics": stable_stats,
        "output": output,
        "output_sha256": hashlib.sha256(output.encode()).hexdigest(),
        "normal_form_zero": zero,
        "mutate_target_by_constant": mutate_target,
        "scope": (
            "Exact F4 normal-form computation over the pinned prime on one "
            "dense two-parameter plane. Output parsing is deliberately guarded."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-target", action="store_true")
    args = parser.parse_args()
    result = run_audit(args.prime, args.timeout, args.mutate_target)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        if args.prime != 1009 or args.timeout != 300 or args.mutate_target:
            raise RuntimeError("stored msolve result is pinned to default gate")
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored msolve result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
