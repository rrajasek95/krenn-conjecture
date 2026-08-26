#!/usr/bin/env python3
"""Independent exact audit of the rep2 tensor/core43 result."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
SUPPORT = FIXED | ADDED | VARIABLE
RANK_ONE_EDGES = frozenset(((5, 6), (5, 7)))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


SUPPORTED = tuple(m for m in matchings(tuple(range(8))) if set(m) <= SUPPORT)
assert len(SUPPORTED) == 13


def parse_z3_model(path):
    text = path.read_text()
    assert text.splitlines()[0] == "sat"
    return {
        match.group(1): int(match.group(2), 16)
        for match in re.finditer(
            r"\(define-fun (\w+) \(\) \(_ BitVec 8\)\s+#x([0-9a-f]+)\)", text
        )
    }


def amplitude(word, values, modulus=None):
    def value(name):
        answer = values.get(name, 0)
        return answer % modulus if modulus else answer

    def entry(edge, i, j):
        if edge in FIXED:
            return int(i == j)
        if edge == (5, 7):
            answer = value(f"u{i}") * value(f"v{j}")
        elif edge == (5, 6):
            a26v = sum(value(f"a26_{j}{k}") * value(f"v{k}") for k in range(3))
            answer = -value(f"u{i}") * a26v
        else:
            answer = value(f"a{edge[0]}{edge[1]}_{i}{j}")
        return answer % modulus if modulus else answer

    answer = sum(
        math.prod(entry(edge, word[edge[0]], word[edge[1]]) for edge in matching)
        for matching in SUPPORTED
    )
    return answer % modulus if modulus else answer


def rational_point():
    # Literal characteristic-zero solution of the exact 43 amplitude equations.
    # Every omitted source/factor coordinate is zero.
    return {
        "a04_01": Fraction(1),
        "a06_10": Fraction(-1, 2),
        "a12_01": Fraction(1),
        "a14_00": Fraction(1),
        "a14_10": Fraction(1),
        "a17_00": Fraction(-2),
        "a17_10": Fraction(-1),
        "a23_01": Fraction(-1),
        "a26_01": Fraction(-1),
        "a26_12": Fraction(1),
        "a35_01": Fraction(-1),
        "a35_10": Fraction(1),
        "a67_01": Fraction(-1),
        "a67_11": Fraction(1),
        "u0": Fraction(1),
        "v0": Fraction(1),
        "v2": Fraction(1),
    }


def flattening_census():
    records = []
    for mask in range(1, 1 << 8):
        side = frozenset(i for i in range(8) if mask & (1 << i))
        if 0 not in side or len(side) == 8:
            continue
        terms = []
        for index, matching in enumerate(SUPPORTED):
            crossing = tuple(
                edge for edge in matching if (edge[0] in side) != (edge[1] in side)
            )
            binary_rank = math.prod(1 if edge in RANK_ONE_EDGES else 2 for edge in crossing)
            ternary_rank = math.prod(1 if edge in RANK_ONE_EDGES else 3 for edge in crossing)
            terms.append({
                "matching_index": index,
                "crossing_edges": [f"{a}{b}" for a, b in crossing],
                "binary_rank_bound": binary_rank,
                "ternary_rank_bound": ternary_rank,
            })
        records.append({
            "side": "".join(map(str, sorted(side))),
            "binary_sum_bound": sum(term["binary_rank_bound"] for term in terms),
            "ternary_sum_bound": sum(term["ternary_rank_bound"] for term in terms),
            "terms": terms,
        })
    assert len(records) == 127
    records.sort(key=lambda item: (item["ternary_sum_bound"], item["binary_sum_bound"], item["side"]))
    return records


def main():
    core = json.loads((HERE / "results_f2_core43.json").read_text())
    words = [tuple(map(int, raw)) for raw in core["amplitude_words"]]
    assert len(words) == 43 and len(set(words)) == 43

    # Independently replay the literal odd-prime model on the 43 equations.
    f3 = parse_z3_model(HERE / "rep2_core43_f3.stdout")
    assert len(f3) == 103 and all(0 <= value < 3 for value in f3.values())
    f3_residuals = {
        "".join(map(str, word)): (amplitude(word, f3, 3) - int(word == (0,) * 8)) % 3
        for word in words
    }
    assert not any(f3_residuals.values())

    # Independently replay the much stronger explicit Q point.
    qpoint = rational_point()
    q_residuals = {
        "".join(map(str, word)): amplitude(word, qpoint) - int(word == (0,) * 8)
        for word in words
    }
    assert not any(q_residuals.values())
    other_pair01 = []
    for word in itertools.product((0, 1), repeat=8):
        if word in words:
            continue
        residual = amplitude(word, qpoint) - int(len(set(word)) == 1)
        if residual:
            other_pair01.append({
                "word": "".join(map(str, word)),
                "residual": str(residual),
            })
    assert other_pair01  # The point refutes only the core identity, not full pair01.

    flattenings = flattening_census()
    best = flattenings[0]
    assert best["side"] == "0123467"
    singleton5_groups = {}
    for item in best["terms"]:
        assert len(item["crossing_edges"]) == 1
        edge = item["crossing_edges"][0]
        singleton5_groups.setdefault(edge, []).append(item["matching_index"])
    assert singleton5_groups == {
        "35": [5, 7, 9, 11],
        "45": [0, 3, 4, 12],
        "56": [2, 8],
        "57": [1, 6, 10],
    }
    assert best["binary_sum_bound"] == 21 and best["ternary_sum_bound"] == 29
    # Target ranks are only 2 and 3, so naive subadditive flattening rank cannot close.
    assert all(item["binary_sum_bound"] >= 2 for item in flattenings)
    assert all(item["ternary_sum_bound"] >= 3 for item in flattenings)

    result = {
        "schema": "KRENN_X5_REP2_TENSOR_CORE43_AUDIT_V1",
        "status": "PASS_F2_ONLY_OBSTRUCTION_AND_EXACT_Q_COUNTERMODEL_TO_CORE_LIFT",
        "support": {
            "fixed": ["03", "16", "27", "45"],
            "variable": ["04", "12", "35", "67"],
            "added": ["06", "14", "17", "23", "26", "56", "57"],
            "supported_matchings": [
                [f"{a}{b}" for a, b in matching] for matching in SUPPORTED
            ],
        },
        "f2_core": {
            "size": len(words),
            "deletion_minimal": all(
                item["status"] == "sat" for item in core["deletion_checks"]
            ),
            "proof_input_sha256": sha256(HERE / core["proof_input"]),
            "proof_output_sha256": sha256(HERE / core["proof_output"]),
            "scope": core["scope"],
        },
        "odd_prime_lift_test": {
            "field": 3,
            "literal_model_sha256": sha256(HERE / "rep2_core43_f3.stdout"),
            "all_43_residuals_zero": True,
        },
        "rational_lift_test": {
            "point": {name: str(value) for name, value in sorted(qpoint.items())},
            "omitted_coordinates": "zero",
            "all_43_residuals_zero": True,
            "non_boolean_coordinates": {
                name: str(value) for name, value in sorted(qpoint.items())
                if value not in (0, 1)
            },
            "other_pair01_violation_count": len(other_pair01),
            "other_pair01_first_16": other_pair01[:16],
            "conclusion": "the F2 contradiction uses characteristic-two/Boolean field identities and does not lift to Q",
        },
        "flattening_census": {
            "canonical_bipartitions": len(flattenings),
            "best_side": best["side"],
            "best_binary_sum_rank_bound": best["binary_sum_bound"],
            "best_ternary_sum_rank_bound": best["ternary_sum_bound"],
            "singleton5_source_groups": singleton5_groups,
            "shared_rank1_site5_subspace": "the five A56/A57 terms have site-5 factor in span(u)",
            "naive_rank_obstruction": False,
            "reason": "minimum termwise sum bounds 21/29 exceed GHZ flattening ranks 2/3",
        },
        "scope": {
            "proved": "exact characteristic-two obstruction for the 43 amplitudes; exact F3 and Q countermodels to lifting that core identity",
            "not_proved": "full pair01 satisfiability over Q, rep2 rank1 closure, or either-carrier activity",
            "next": "a rational contraction must use equations outside the 43-core or a different source-labelled carrier identity",
        },
    }
    path = HERE / "results_tensor_core_audit.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)
    print(json.dumps({
        "status": result["status"],
        "core": len(words),
        "q_residuals": sum(value != 0 for value in q_residuals.values()),
        "other_pair01_violations": len(other_pair01),
        "best_flattening": best["side"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
