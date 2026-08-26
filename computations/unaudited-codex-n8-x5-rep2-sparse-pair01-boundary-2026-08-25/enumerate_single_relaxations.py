#!/usr/bin/env python3
"""Generate and exact-normalize every one-coordinate sparse relaxation."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def normalized_input(text, extra, base):
    answer = re.sub(rf"\b{re.escape(extra)}\b", "extra", text)
    lines = answer.splitlines()
    expected_ring = f"ring r=0,({','.join(sorted(set(base) | {'extra'}))}),dp;"
    for index, line in enumerate(lines):
        if line.startswith("ring r=0,"):
            lines[index] = expected_ring
            break
    else:
        raise AssertionError("ring line absent")
    return "\n".join(lines) + "\n"


def support_automorphisms(generator):
    # Preserve the three edge classes and the rank-one substitution skeleton
    # (57,56,26 individually); this is the exact source-labelled symmetry.
    def image(permutation, edge):
        return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))

    core = generator.load_core()
    fixed = set(core.FIXED)
    variable = set(core.VARIABLE)
    added = set(generator.REP2_ADDED)
    answers = []
    for permutation in itertools.permutations(range(8)):
        if {image(permutation, edge) for edge in fixed} != fixed:
            continue
        if {image(permutation, edge) for edge in added} != added:
            continue
        if {image(permutation, edge) for edge in variable} != variable:
            continue
        if any(image(permutation, edge) != edge for edge in ((5, 7), (5, 6), (2, 6))):
            continue
        answers.append(permutation)
    return answers


def main():
    generator = load("generate_sparse_pair01.py")
    module = generator.load_core()
    all_variables = set(module.SOURCE.values()) | set(module.U) | set(module.V)
    zero_variables = sorted(all_variables - generator.BASE_LIVE)
    assert len(all_variables) == 87 and len(zero_variables) == 70
    automorphisms = support_automorphisms(generator)
    assert automorphisms == [tuple(range(8))]
    # The residual pair01 color symmetry is 0<->1, but it does not stabilize
    # this 17-coordinate chart.  Thus the exact chart stabilizer is trivial.
    color_swap_live = set()
    for name in generator.BASE_LIVE:
        if name[0] in "uv":
            color_swap_live.add(name[0] + str({0: 1, 1: 0, 2: 2}[int(name[1])]))
        else:
            i, j = map(int, name[4:6])
            swap = {0: 1, 1: 0, 2: 2}
            color_swap_live.add(name[:4] + str(swap[i]) + str(swap[j]))
    assert color_swap_live != set(generator.BASE_LIVE)

    records = []
    normalized_groups = {}
    for extra in zero_variables:
        safe = extra.replace("_", "")
        label = f"plus_{safe}"
        generated = generator.build(generator.BASE_LIVE | {extra}, label)
        text = (HERE / generated["path"]).read_text()
        normalized = normalized_input(text, extra, generator.BASE_LIVE)
        digest = sha256_text(normalized)
        record = {
            "extra": extra,
            "label": label,
            "input": generated["path"],
            "input_sha256": generated["sha256"],
            "normalized_sha256": digest,
            "emitted_equation_count": generated["emitted_equation_count"],
        }
        records.append(record)
        normalized_groups.setdefault(digest, []).append(extra)
    result = {
        "schema": "KRENN_X5_REP2_SPARSE_SINGLE_RELAXATION_LEDGER_V1",
        "status": "PASS_ALL_SINGLE_COORDINATES_GENERATED",
        "all_amplitude_variables": len(all_variables),
        "base_live_variables": len(generator.BASE_LIVE),
        "zero_coordinate_count": len(zero_variables),
        "source_labelled_site_automorphisms": [list(item) for item in automorphisms],
        "pair01_color_swap_stabilizes_base_chart": False,
        "exact_chart_symmetry_orbits": len(zero_variables),
        "normalized_polynomial_groups": [
            {"normalized_sha256": digest, "members": members, "representative": members[0]}
            for digest, members in sorted(normalized_groups.items())
        ],
        "normalized_group_count": len(normalized_groups),
        "records": records,
        "scope": "one new amplitude coordinate; guard, adjoint, incidence, and rank assertions excluded",
    }
    output = HERE / "single_relaxation_ledger.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "coordinates": len(zero_variables),
        "chart_orbits": len(zero_variables),
        "normalized_groups": len(normalized_groups),
        "largest_group": max(map(len, normalized_groups.values())),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
