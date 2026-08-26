#!/usr/bin/env python3
"""Exact fixed-base residual hypergraph and minimal four-coordinate supports."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
import os
import re
import statistics
import tempfile
import time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TRIPLE = ROOT / "computations/unaudited-codex-n8-x5-rep2-sparse-pair01-triple-boundary-2026-08-25"
DOUBLE = ROOT / "computations/unaudited-codex-n8-x5-rep2-sparse-pair01-boundary-2026-08-25"
TENSOR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-tensor-flattening-2026-08-25"
PINS = {
    TRIPLE / "MANIFEST.sha256": "fb5f9d9bb179bccff0daad0e2bb6dc551280eed388a7db93dedf07683a6cff7e",
    TRIPLE / "results_triple_groups.json": "766676f3dfae8d0bb7eaf5d77918a0511193bfb6f44cc030dddcd40913592a54",
    DOUBLE / "generate_sparse_pair01.py": "635049c3df63a3a078c1b03a0e99c20867e97acf3ce8c405d0641715242b42b9",
    TENSOR / "results_tensor_core_audit.json": "b164264e31b6b3c9341409db79df81cabb3b843db7aae7cf6615715656a16a00",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def poly_add(first, second):
    result = defaultdict(Fraction)
    for monomial, coefficient in itertools.chain(first.items(), second.items()):
        result[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def poly_mul(first, second):
    result = defaultdict(Fraction)
    for left, left_coefficient in first.items():
        for right, right_coefficient in second.items():
            result[tuple(sorted(left + right))] += left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def constant(value):
    return {} if not value else {(): Fraction(value)}


def variable(name):
    return {(name,): Fraction(1)}


def entry_poly(module, edge, i, j):
    if edge in module.FIXED:
        return constant(i == j)
    if edge == (5, 7):
        return poly_mul(variable(f"u{i}"), variable(f"v{j}"))
    if edge == (5, 6):
        result = {}
        for k in range(3):
            term = poly_mul(variable(f"u{i}"), variable(f"a26_{j}{k}"))
            term = poly_mul(term, variable(f"v{k}"))
            term = {monomial: -coefficient for monomial, coefficient in term.items()}
            result = poly_add(result, term)
        return result
    return variable(f"a{edge[0]}{edge[1]}_{i}{j}")


def amplitude_poly(module, word):
    result = {}
    for matching in module.SUPPORTED:
        term = constant(1)
        for edge in matching:
            term = poly_mul(term, entry_poly(module, edge, word[edge[0]], word[edge[1]]))
            if not term:
                break
        result = poly_add(result, term)
    return result


def substitute_base(polynomial, point):
    result = defaultdict(Fraction)
    for monomial, coefficient in polynomial.items():
        remaining = []
        value = coefficient
        for name in monomial:
            if name in point:
                value *= point[name]
            else:
                remaining.append(name)
        result[tuple(sorted(remaining))] += value
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def minimal_sets(sets):
    ordered = sorted(set(map(frozenset, sets)), key=lambda item: (len(item), tuple(sorted(item))))
    answer = []
    for item in ordered:
        if not any(prior <= item for prior in answer):
            answer.append(item)
    return answer


def is_hit(support, families):
    return all(any(activation <= support for activation in family) for family in families)


def normalize(text, extras, base):
    pattern = re.compile(r"\b(?:" + "|".join(map(re.escape, extras)) + r")\b")
    answers = []
    for ordering in itertools.permutations(extras):
        mapping = {name: f"extra{index}" for index, name in enumerate(ordering)}
        value = pattern.sub(lambda match: mapping[match.group(0)], text)
        lines = value.splitlines()
        ring = f"ring r=0,({','.join(sorted(set(base) | set(mapping.values())))}),dp;"
        positions = [index for index, line in enumerate(lines) if line.startswith("ring r=0,")]
        assert len(positions) == 1
        lines[positions[0]] = ring
        answers.append("\n".join(lines) + "\n")
    return min(answers)


def atomic_write(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def main():
    assert __debug__
    for path, digest in PINS.items():
        assert sha256(path) == digest, path
    generator = load(DOUBLE / "generate_sparse_pair01.py")
    module = generator.load_core()
    tensor = json.loads((TENSOR / "results_tensor_core_audit.json").read_text())
    point = {
        name: Fraction(value)
        for name, value in tensor["rational_lift_test"]["point"].items()
    }
    violations = tensor["rational_lift_test"]["other_pair01_first_16"]
    assert len(violations) == tensor["rational_lift_test"]["other_pair01_violation_count"] == 13
    amplitude_variables = set(module.SOURCE.values()) | set(module.U) | set(module.V)
    zero = sorted(amplitude_variables - set(point))
    assert set(point) == set(generator.BASE_LIVE) and len(zero) == 70

    equation_records = []
    families = []
    for violation in violations:
        word = tuple(map(int, violation["word"]))
        polynomial = substitute_base(amplitude_poly(module, word), point)
        constant_term = polynomial.get((), Fraction(0))
        assert constant_term == Fraction(violation["residual"])
        nonconstant = {
            monomial: coefficient for monomial, coefficient in polynomial.items() if monomial
        }
        activation_sets = minimal_sets(set(monomial) for monomial in nonconstant)
        assert activation_sets
        assert all(activation <= set(zero) for activation in activation_sets)
        families.append(activation_sets)
        equation_records.append({
            "word": violation["word"],
            "constant_residual": str(constant_term),
            "nonconstant_monomial_count": len(nonconstant),
            "minimal_activation_sets": [sorted(item) for item in activation_sets],
            "minimal_activation_size_histogram": {
                str(size): sum(len(item) == size for item in activation_sets)
                for size in sorted({len(item) for item in activation_sets})
            },
            "expanded_polynomial": [
                {"coefficient": str(coefficient), "monomial": list(monomial)}
                for monomial, coefficient in sorted(polynomial.items())
            ],
        })

    # Exact exhaustive support-hitting census through size four.
    hit_by_size = {}
    for size in range(5):
        hit_by_size[size] = [
            frozenset(candidate)
            for candidate in itertools.combinations(zero, size)
            if is_hit(frozenset(candidate), families)
        ]
    minimal_four = [
        support for support in hit_by_size[4]
        if not any(prior < support for size in range(4) for prior in hit_by_size[size])
    ]
    # Exact transversal-by-union closure: choose one activation monomial for
    # each residual, union the coordinate supports, and delete supersets after
    # every stage.  The survivors are precisely the inclusion-minimal fixed-
    # base hitting supports.
    closure = [frozenset()]
    closure_counts = []
    for family in families:
        closure = minimal_sets(left | right for left in closure for right in family)
        closure_counts.append(len(closure))
    minimum_hitting_size = min(map(len, closure))
    minimum_hitting_supports = [
        support for support in closure if len(support) == minimum_hitting_size
    ]
    assert minimum_hitting_size > 4 and not minimal_four

    # Normalize only the inclusion-minimal size-four necessary supports.
    groups = {}
    support_records = []
    normalization_started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="rep2_quad_hitting_") as temporary_directory:
        original_here = generator.HERE
        generator.HERE = Path(temporary_directory)
        try:
            for index, support in enumerate(minimal_four):
                extras = tuple(sorted(support))
                generated = generator.build(generator.BASE_LIVE | support, f"hit4_{index}")
                raw = (generator.HERE / generated["path"]).read_text()
                canonical = normalize(raw, extras, generator.BASE_LIVE)
                digest = hashlib.sha256(canonical.encode()).hexdigest()
                support_records.append({"support": list(extras), "normalized_sha256": digest})
                if digest not in groups:
                    group_index = len(groups)
                    path = HERE / f"group_{group_index:05d}_{digest[:16]}.sing"
                    atomic_write(path, canonical)
                    groups[digest] = {
                        "normalized_sha256": digest,
                        "representative": list(extras),
                        "canonical_input": path.name,
                        "canonical_input_sha256": sha256(path),
                        "canonical_input_bytes": path.stat().st_size,
                        "members": [],
                    }
                groups[digest]["members"].append(list(extras))
        finally:
            generator.HERE = original_here
    normalization_wall = time.monotonic() - normalization_started
    group_list = sorted(groups.values(), key=lambda item: item["normalized_sha256"])

    triple_run = json.loads((TRIPLE / "results_triple_groups.json").read_text())
    timings = [item["wall_seconds"] for item in triple_run["attempts"]]
    mean = statistics.mean(timings)
    maximum = max(timings)
    projected_mean = mean * len(group_list)
    projected_conservative = min(maximum * len(group_list), mean * 2 * len(group_list))
    result = {
        "schema": "KRENN_X5_REP2_FIXED_BASE_RESIDUAL_HITTING_DESIGN_V1",
        "status": "PASS_DESIGN_ONLY_NO_Q_IDEALS_RUN",
        "pins": {str(path): digest for path, digest in PINS.items()},
        "base_point": {name: str(value) for name, value in sorted(point.items())},
        "zero_coordinate_count": len(zero),
        "violated_equation_count": len(equation_records),
        "equations": equation_records,
        "necessary_condition": (
            "with the 17 base coordinates fixed at the sealed rational values, every nonzero residual "
            "must have at least one nonconstant monomial whose entire zero-coordinate support is admitted"
        ),
        "logical_scope": {
            "necessary_for": "literal fixed-base coefficient repair",
            "not_necessary_for": "arbitrary points of the base17+S chart where the 17 base coordinates may move",
            "not_a_global_quadruple_filter": True,
        },
        "hitting_support_counts": {str(size): len(items) for size, items in hit_by_size.items()},
        "minimal_size4_hitting_support_count": len(minimal_four),
        "minimal_size4_supports": [sorted(item) for item in minimal_four],
        "inclusion_minimal_hitting_support_count": len(closure),
        "hitting_closure_counts_by_equation": closure_counts,
        "minimum_fixed_base_hitting_size": minimum_hitting_size,
        "minimum_fixed_base_hitting_support_count": len(minimum_hitting_supports),
        "minimum_fixed_base_hitting_supports": [
            sorted(item) for item in minimum_hitting_supports
        ],
        "normalized_group_count": len(group_list),
        "groups": group_list,
        "support_records": support_records,
        "normalization_wall_seconds": normalization_wall,
        "canonical_input_total_bytes": sum(item["canonical_input_bytes"] for item in group_list),
        "projection_from_triple_run": {
            "per_group_mean_seconds": mean,
            "per_group_max_seconds": maximum,
            "projected_mean_seconds": projected_mean,
            "projected_conservative_seconds": projected_conservative,
        },
        "launch_gate": {
            "no_q_ideals_run": True,
            "requires_explicit_authorization": True,
            "warning": "even an exhaustive UNIT result covers only fixed-base repair candidates, not all C(70,4) charts",
        },
    }
    output = HERE / "hitting_support_ledger.json"
    atomic_write(output, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "hit_counts": result["hitting_support_counts"],
        "minimal4": len(minimal_four),
        "fixed_base_minimum": minimum_hitting_size,
        "fixed_base_minimum_count": len(minimum_hitting_supports),
        "groups": len(group_list),
        "input_bytes": result["canonical_input_total_bytes"],
        "projected_mean": projected_mean,
        "projected_conservative": projected_conservative,
        "scope": result["logical_scope"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
