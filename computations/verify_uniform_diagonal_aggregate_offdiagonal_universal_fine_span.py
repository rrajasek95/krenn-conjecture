#!/usr/bin/env python3
"""Verify the universal fine-degree source unit in the full 01/10 sector."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
BASE_RELATIVE = (
    "computations/verify_n8_lemma_e_unary_top_diagonal_aggregate_identity.py"
)
BASE_PATH = ROOT / BASE_RELATIVE
PRIME = 1_000_003
PINS = {
    BASE_RELATIVE:
        "d805a2d78ddf83239b2edca0598b8a88f90517296b375613030eb24defb1b2c2",
    "notes/n8-lemma-e-unary-top-diagonal-aggregate-identity.md":
        "d959fd085e6585d46000ace7a173d898e0a5f0306f03f2f476ad1890a0e24aa0",
    "computations/verify_uniform_diagonal_aggregate_offdiagonal_quadratic_defect.py":
        "cdf5a71f6f5dcef524c22c9790f0a29bf902ddf8e58bccb7b5233655f0359f07",
    "notes/uniform-diagonal-aggregate-offdiagonal-quadratic-defect.md":
        "9aa57c618f3ae8bca6b335fb050c881039e70449f6798240a50ba28429e667fb",
    "computations/verify_uniform_diagonal_aggregate_offdiagonal_cubic_defect.py":
        "9bea51acfdf30c679bcb1ceb1c5de693df18234359d5bfbac61175da3fccf987",
    "notes/uniform-diagonal-aggregate-offdiagonal-cubic-defect.md":
        "af29dafb11463813f9be0a37c22337659b9fdb5d6c6b40548cfea566eda92d04",
}
EXPECTED_LEDGER_SHA256 = (
    "283e21edf14b5e7a3c0ce42a70621f2cd28f92a310e4fa770cfa5dab051bf7bd"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def load_base():
    spec = spec_from_file_location("diagonal_aggregate", BASE_PATH)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def variable(first, second):
    (site1, colour1), (site2, colour2) = sorted((first, second))
    if site1 == site2:
        return None
    if colour1 == colour2 or (colour1, colour2) in ((0, 1), (1, 0)):
        return ((site1, site2), (colour1, colour2))
    return None


@lru_cache(None)
def token_matchings(tokens):
    tokens = tuple(sorted(tokens))
    if not tokens:
        return ((),)
    first = tokens[0]
    answer = []
    for index, second in enumerate(tokens[1:], start=1):
        cell = variable(first, second)
        if cell is None:
            continue
        remainder = tokens[1:index] + tokens[index + 1:]
        for tail in token_matchings(remainder):
            answer.append(tuple(sorted((cell,) + tail)))
    return tuple(answer)


def row_word(label, sites):
    kind, *parts = label.split(":")
    if kind == "top":
        return sites, tuple(map(int, parts[0]))
    holes = tuple(map(int, parts[0]))
    vertices = tuple(site for site in sites if site not in holes)
    return vertices, tuple(map(int, parts[1]))


def row_terms(label, sites):
    vertices, word = row_word(label, sites)
    tokens = tuple((site, colour) for site, colour in zip(vertices, word))
    return Counter(token_matchings(tokens))


def build_complete_labels(tokens, sites):
    labels = []
    for word in itertools.product(*(tokens[site] for site in sites)):
        if len(set(word)) == 1:
            continue
        label = "top:" + "".join(map(str, word))
        if row_terms(label, sites):
            labels.append(label)
    packets = (
        ((0, 1), (1, 1, 1, 1)),
        ((2, 3), (2, 2, 2, 2)),
        ((0, 3), None),
        ((1, 2), None),
    )
    for holes, target in packets:
        vertices = tuple(site for site in sites if site not in holes)
        for word in itertools.product(*(tokens[site] for site in vertices)):
            if target is not None and word == target:
                continue
            label = ("cofactor:" + "".join(map(str, holes)) + ":"
                     + "".join(map(str, word)))
            if row_terms(label, sites):
                labels.append(label)
    return tuple(labels)


def multiply(left, right):
    answer = Counter()
    for first, a in left.items():
        for second, b in right.items():
            answer[tuple(sorted(first + second))] += a * b
    return answer


def sparse_reduce(vector, pivots, prime):
    vector = {row: value % prime for row, value in vector.items()
              if value % prime}
    while vector:
        pivot = min(vector)
        if pivot not in pivots:
            inverse = pow(vector[pivot], -1, prime)
            return {row: value * inverse % prime
                    for row, value in vector.items()}
        factor = vector[pivot]
        basis = pivots[pivot]
        for row, value in basis.items():
            updated = (vector.get(row, 0) - factor * value) % prime
            if updated:
                vector[row] = updated
            else:
                vector.pop(row, None)
    return {}


def main():
    pin_dependencies()
    base = load_base()
    tokens = {
        0: (0, 2), 1: (0, 2), 2: (0, 1), 3: (0, 1),
        4: (0, 1, 2), 5: (0, 1, 2),
    }
    target_tokens = tuple((site, colour) for site, colours in tokens.items()
                          for colour in colours)
    diagonal_labels = set(base.build_generators()[1])
    labels = build_complete_labels(tokens, base.SITES)
    columns = []
    column_metadata = []
    multiplier_histogram = Counter()
    for label in labels:
        vertices, word = row_word(label, base.SITES)
        consumed = {(site, colour) for site, colour in zip(vertices, word)}
        complement = tuple(token for token in target_tokens
                           if token not in consumed)
        multipliers = token_matchings(complement)
        generator = row_terms(label, base.SITES)
        for multiplier in multipliers:
            offdegree = sum(colours[0] != colours[1]
                            for _, colours in multiplier)
            multiplier_histogram[offdegree] += 1
            columns.append(multiply(Counter({multiplier: 1}), generator))
            column_metadata.append((label, multiplier, offdegree))

    pure1 = Counter(
        {tuple((((u, v), (1, 1)) for u, v in matching)): 1
         for matching in base.perfect_matchings((2, 3, 4, 5))}
    )
    pure2 = Counter(
        {tuple((((u, v), (2, 2)) for u, v in matching)): 1
         for matching in base.perfect_matchings((0, 1, 4, 5))}
    )
    pure0 = Counter(
        {tuple((((u, v), (0, 0)) for u, v in matching)): 1
         for matching in base.perfect_matchings(base.SITES)}
    )
    target = multiply(multiply(pure1, pure2), pure0)
    monomials = sorted(set(target).union(
        *(set(column) for column in columns)
    ))
    row_index = {monomial: index for index, monomial in enumerate(monomials)}
    pivots = {}
    for column in columns:
        vector = {row_index[monomial]: coefficient
                  for monomial, coefficient in column.items()}
        reduced = sparse_reduce(vector, pivots, PRIME)
        if reduced:
            pivot = min(reduced)
            pivots[pivot] = reduced
    target_vector = {row_index[monomial]: coefficient
                     for monomial, coefficient in target.items()}
    target_remainder = sparse_reduce(target_vector, pivots, PRIME)
    require(not target_remainder,
            "the complete fine-degree target left the modular source span")
    exact_singular = None
    if not target_remainder:
        dense_columns = []
        for column in columns:
            entries = ["0"] * len(monomials)
            for monomial, coefficient in column.items():
                entries[row_index[monomial]] = str(coefficient)
            dense_columns.append("[" + ",".join(entries) + "]")
        target_entries = ["0"] * len(monomials)
        for monomial, coefficient in target.items():
            target_entries[row_index[monomial]] = str(coefficient)
        code = "ring r=0,(t),dp; option(redSB);\n"
        code += "module M=" + ",".join(dense_columns) + ";\n"
        code += "vector T=[" + ",".join(target_entries) + "];\n"
        code += "module G=std(M); vector R=reduce(T,G);\n"
        code += "matrix L=lift(M,module(T)); vector C=0; int i; int nz=0;\n"
        code += (
            "for(i=1;i<=size(M);i++){C=C+M[i]*L[i,1];"
            "if(L[i,1]!=0){nz=nz+1;}}\n"
        )
        code += 'if(C-T!=0){print("SOURCE_LIFT_FAILED");exit(1);}\n'
        code += 'print("EXACT_REMAINDER");print(R);\n'
        code += 'print("EXACT_NONZERO");print(nz);\n'
        code += 'print("BEGIN_EXACT_LIFT");L;print("END_EXACT_LIFT");\n'
        result = subprocess.run(
            ("/usr/local/bin/Singular", "-q"), input=code, text=True,
            capture_output=True, check=False, timeout=60,
        )
        require(result.returncode == 0,
                f"exact Singular failed: {result.stderr or result.stdout}")
        require("SOURCE_LIFT_FAILED" not in result.stdout,
                "the exact fine-degree source lift failed")
        lines = result.stdout.splitlines()
        lift = result.stdout.split("BEGIN_EXACT_LIFT\n", 1)[1].split(
            "\nEND_EXACT_LIFT", 1
        )[0]
        nonzero_lift = []
        exact_sum = Counter()
        for line in lift.splitlines():
            if not line.startswith("L[") or line.endswith("=0"):
                continue
            index = int(line.split("[", 1)[1].split(",", 1)[0]) - 1
            coefficient = Fraction(line.split("=", 1)[1])
            nonzero_lift.append((index, coefficient))
            for monomial, value in columns[index].items():
                exact_sum[monomial] += coefficient * value
        exact_sum += Counter()
        require(exact_sum == target,
                "the Python replay of the exact lift failed")
        exact_singular = (
            lines[lines.index("EXACT_REMAINDER") + 1],
            int(lines[lines.index("EXACT_NONZERO") + 1]),
            lift,
            nonzero_lift,
        )
    require(exact_singular is not None and exact_singular[0] == "[0]",
            "the exact fine-degree remainder changed")
    selected_offdegrees = Counter(
        column_metadata[index][2] for index, _ in exact_singular[3]
    )
    selected_label_types = Counter(
        column_metadata[index][0].split(":", 1)[0]
        for index, _ in exact_singular[3]
    )
    selected_decorated_only = sum(
        column_metadata[index][0] not in diagonal_labels
        for index, _ in exact_singular[3]
    )
    coefficient_histogram = Counter(
        str(coefficient) for _, coefficient in exact_singular[3]
    )
    source_packet_histogram = Counter(
        label.split(":", 2)[0] + (
            ":" + label.split(":", 2)[1]
            if label.startswith("cofactor:") else ""
        ) for label in labels
    )
    monomial_offdegrees = Counter(
        sum(colours[0] != colours[1] for _, colours in monomial)
        for monomial in monomials
    )
    ledger = {
        "source_rows": len(labels),
        "diagonal_active_rows": len(diagonal_labels),
        "decorated_only_rows": len(set(labels) - diagonal_labels),
        "source_packet_histogram": dict(sorted(source_packet_histogram.items())),
        "fine_degree_source_columns": len(columns),
        "fine_degree_monomial_rows": len(monomials),
        "monomial_offdegree_histogram": dict(sorted(monomial_offdegrees.items())),
        "multiplier_offdegree_histogram": dict(sorted(multiplier_histogram.items())),
        "target_terms": len(target),
        "modular_prime": PRIME,
        "modular_rank": len(pivots),
        "modular_cokernel_dimension": len(monomials) - len(pivots),
        "modular_target_remainder": 0,
        "exact_remainder": exact_singular[0],
        "exact_nonzero_columns": exact_singular[1],
        "exact_lift_sha256": sha256(exact_singular[2].encode()).hexdigest(),
        "exact_coefficient_histogram": dict(sorted(coefficient_histogram.items())),
        "selected_multiplier_offdegree_histogram": dict(
            sorted(selected_offdegrees.items())
        ),
        "selected_source_type_histogram": dict(sorted(selected_label_types.items())),
        "selected_columns_from_decorated_only_rows": selected_decorated_only,
        "python_exact_replay": True,
        "verdict": (
            "the complete fine-token source span contains the normalized "
            "target over Z; one 165-column identity is valid for arbitrary "
            "simultaneous diagonal and ordered 01/10 internal support"
        ),
        "scope": (
            "concentrated response spokes and the full fine-compatible "
            "top/F01/F23/F03/F12 row inventory in the diagonal+01/10 "
            "sector; no 02/20, 12/21, or multisite-star conclusion"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(payload)
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
