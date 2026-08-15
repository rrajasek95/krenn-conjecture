#!/usr/bin/env python3
"""Interface the all-singleton N=8 chart to the diagonal recurrence theorem.

An all-singleton decorated support assigns at most one diagonal colour to
each live physical edge.  It is therefore a specialization of the arbitrary
diagonal three-matrix model already excluded at N=8 by the characteristic-
free hafnian recurrence obstruction.

This checker independently verifies the coefficient factorization for all
3^8 words, pins and runs the existing N=8 recurrence checker, and records why
the fixed target cell, pure-occurrence, and no-mixed-singleton clauses only
restrict the already excluded diagonal model.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "proofs/diagonal-hafnian-recurrence-obstruction.md":
        "5a1ccbcbe852c5b240f1b2d94013ef2ab1af896350020795e80a51a67db7fb97",
    "computations/verify_diagonal_recurrence_obstruction.py":
        "4421f3145c52dc64a4108687735064aaad93b5332f06135e59ce5c54311a25a1",
}
EXPECTED_LEDGER_SHA256 = (
    "ddbe0ea62e8ce0b9d67fc50a2d8ef1c7bdfa9f812e97e10686ed03fc177bdbfe"
)

N = 8
COLOURS = (0, 1, 2)
VERTICES = tuple(range(N))
TARGET_EDGE = (0, 1)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))


def global_diagonal_monomials(word):
    """Coefficient monomials from global perfect matchings."""
    answer = Counter()
    for matching in MATCHINGS:
        cells = []
        for left, right in matching:
            if word[left] != word[right]:
                break
            cells.append((left, right, word[left]))
        else:
            answer[tuple(sorted(cells))] += 1
    return answer


def partition_hafnian_monomials(word):
    """Monomials in product_c haf(A_c[S_c])."""
    colour_sites = tuple(
        tuple(vertex for vertex in VERTICES if word[vertex] == colour)
        for colour in COLOURS
    )
    if any(len(sites) % 2 for sites in colour_sites):
        return Counter()
    factors = tuple(tuple(perfect_matchings(sites)) for sites in colour_sites)
    answer = Counter()
    for chosen in product(*factors):
        cells = []
        for colour, matching in enumerate(chosen):
            cells.extend((left, right, colour) for left, right in matching)
        answer[tuple(sorted(cells))] += 1
    return answer


def factorization_audit():
    parity_histogram = Counter()
    term_count_histogram = Counter()
    even_words = 0
    proper_even_partitions = 0
    for word in product(COLOURS, repeat=N):
        global_terms = global_diagonal_monomials(word)
        factored_terms = partition_hafnian_monomials(word)
        require(global_terms == factored_terms,
                ("diagonal coefficient did not factor", word,
                 global_terms, factored_terms))
        parity = tuple(word.count(colour) % 2 for colour in COLOURS)
        parity_histogram[parity] += 1
        term_count_histogram[len(global_terms)] += 1
        if parity == (0, 0, 0):
            even_words += 1
            if len(set(word)) > 1:
                proper_even_partitions += 1
        require(all(value == 1 for value in global_terms.values()),
                ("diagonal matching monomial gained multiplicity", word))
    require(len(MATCHINGS) == 105, len(MATCHINGS))
    require(even_words == 1641 and proper_even_partitions == 1638,
            (even_words, proper_even_partitions))
    return {
        "words_audited": 3 ** N,
        "global_perfect_matchings": len(MATCHINGS),
        "even_partition_words": even_words,
        "proper_even_partition_words": proper_even_partitions,
        "parity_histogram": sorted(parity_histogram.items()),
        "term_count_histogram": sorted(term_count_histogram.items()),
        "literal_identity": (
            "coefficient(word)=product_c haf(A_c[word^{-1}(c)])"
        ),
    }


def run_recurrence_dependency():
    python = ROOT / ".venv/bin/python"
    checker = ROOT / "computations/verify_diagonal_recurrence_obstruction.py"
    require(python.exists(), ("audited PySAT environment missing", python))
    completed = subprocess.run(
        (str(python), str(checker), "--n", "8"),
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    require(completed.returncode == 0,
            ("recurrence dependency failed", completed.returncode,
             completed.stdout, completed.stderr))
    branch_lines = tuple(
        line for line in completed.stdout.splitlines()
        if line.startswith("n=8 branch=")
    )
    require(len(branch_lines) == 9
            and all(line.endswith("sat=False") for line in branch_lines),
            branch_lines)
    summary = next(
        (line for line in completed.stdout.splitlines()
         if line.startswith("VERIFIED n=8:")),
        "",
    )
    require("vars=2988 clauses=23844 branches=9" in summary, summary)
    return {
        "symmetry_branches": 9,
        "all_unsat": True,
        "variables": 2988,
        "base_clauses": 23844,
        "summary_without_timing": summary.split(" seconds=")[0],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    factorization = factorization_audit()
    recurrence = run_recurrence_dependency()
    ledger = {
        "mode_independent": True,
        "dependencies": PINS,
        "factorization": factorization,
        "recurrence_obstruction": recurrence,
        "singleton_chart_embedding": {
            "support_datum": (
                "each live edge uv has one colour sigma(uv) and nonzero "
                "weight x_uv"
            ),
            "diagonal_matrices": (
                "A_c[uv]=x_uv if sigma(uv)=c, otherwise zero"
            ),
            "target_specialization": (
                "sigma(01)=0 is a restriction inside the arbitrary diagonal "
                "model and is not used by the recurrence obstruction"
            ),
            "pure_exact_equations": "haf(A_c[V])=1, hence nonzero",
            "mixed_exact_equations": (
                "every proper even partition product is zero"
            ),
            "occurrence_no_singleton": (
                "necessary for a live singleton-weight support but redundant "
                "once the exact mixed coefficient equations are imposed"
            ),
        },
        "theorem": (
            "there is no exact N=8 all-singleton diagonal source over any "
            "field; indeed there is no exact arbitrary diagonal source"
        ),
        "scope": (
            "this closes the coefficient branch, not the standalone relaxed "
            "occurrence CNF; that Boolean shadow may have SAT supports with "
            "no field-valued exact lift"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))

    print("N=8 all-singleton diagonal recurrence interface: PASS")
    print("mode", arguments.mode)
    print("words / proper even partitions",
          factorization["words_audited"],
          factorization["proper_even_partition_words"])
    print("recurrence branches / vars / clauses",
          recurrence["symmetry_branches"], recurrence["variables"],
          recurrence["base_clauses"])
    print("consequence: singleton target-colour-0 chart has no exact lift")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
