#!/usr/bin/env python3
"""Prioritize triple relaxations that activate a three-missing-coordinate monomial."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
import os
import re
import subprocess
import time
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def factor_monomials(module, edge, i, j):
    if edge in module.FIXED:
        return [()] if i == j else []
    if edge == (5, 7):
        return [(f"u{i}", f"v{j}")]
    if edge == (5, 6):
        return [(f"u{i}", f"a26_{j}{k}", f"v{k}") for k in range(3)]
    return [(f"a{edge[0]}{edge[1]}_{i}{j}",)]


def candidate_triples(generator):
    module = generator.load_core()
    counts = Counter()
    words = list(itertools.product((0, 1), repeat=8)) + [(2,) * 8]
    for word in words:
        for matching in module.SUPPORTED:
            factors = [factor_monomials(module, edge, word[edge[0]], word[edge[1]]) for edge in matching]
            if any(not factor for factor in factors):
                continue
            for choice in itertools.product(*factors):
                monomial = tuple(itertools.chain.from_iterable(choice))
                missing = tuple(sorted(set(monomial) - set(generator.BASE_LIVE)))
                if len(missing) == 3:
                    counts[missing] += 1
    assert len(counts) == 388
    return counts


def normalize(text, extras, base):
    candidates = []
    for ordering in itertools.permutations(extras):
        names = {name: f"extra{index}" for index, name in enumerate(ordering)}
        pattern = re.compile(r"\b(?:" + "|".join(map(re.escape, names)) + r")\b")
        answer = pattern.sub(lambda match: names[match.group(0)], text)
        lines = answer.splitlines()
        expected = f"ring r=0,({','.join(sorted(set(base) | set(names.values())))}),dp;"
        for index, line in enumerate(lines):
            if line.startswith("ring r=0,"):
                lines[index] = expected
                break
        candidates.append("\n".join(lines) + "\n")
    return min(candidates)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    generator = load("generate_sparse_pair01.py")
    triples = candidate_triples(generator)
    groups = {}
    retained = set()
    for index, (triple, occurrence) in enumerate(sorted(triples.items(), key=lambda item: (-item[1], item[0]))):
        label = f"mtriple_{index:03d}"
        generated = generator.build(generator.BASE_LIVE | set(triple), label)
        path = HERE / generated["path"]
        normalized = normalize(path.read_text(), triple, generator.BASE_LIVE)
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        if digest not in groups:
            groups[digest] = {
                "normalized_sha256": digest,
                "representative": list(triple),
                "input": path.name,
                "input_sha256": generated["sha256"],
                "max_monomial_occurrence": occurrence,
                "members": [],
            }
            retained.add(path)
        groups[digest]["members"].append(list(triple))
        groups[digest]["max_monomial_occurrence"] = max(groups[digest]["max_monomial_occurrence"], occurrence)
        if path not in retained:
            path.unlink()
    ordered = sorted(groups.values(), key=lambda item: (-item["max_monomial_occurrence"], item["normalized_sha256"]))
    attempts = []
    winner = None
    started_global = time.monotonic()
    for group in ordered:
        if time.monotonic() - started_global > 120:
            break
        path = HERE / group["input"]
        started = time.monotonic()
        process = subprocess.run(
            ["gtimeout", "5", "Singular", str(path)], capture_output=True,
            text=True, timeout=7,
        )
        stdout = process.stdout + process.stderr
        wall = time.monotonic() - started
        if process.returncode == 0 and "STATUS=NONUNIT" in stdout:
            status = "NONUNIT"
        elif process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout:
            status = "UNIT_IDEAL"
        else:
            status = "FAIL_CLOSED_RESOURCE_OR_PROCESS"
        output = HERE / f"stdout_mtriple_{len(attempts):03d}.txt"
        temporary = output.with_suffix(".txt.tmp")
        temporary.write_text(stdout)
        os.replace(temporary, output)
        record = {
            **group,
            "stdout": output.name,
            "stdout_sha256": sha256(output),
            "returncode": process.returncode,
            "wall_seconds": wall,
            "status": status,
            "groebner_size": int(re.search(r"GROEBNER_SIZE=(\d+)", stdout).group(1))
                if re.search(r"GROEBNER_SIZE=(\d+)", stdout) else None,
        }
        attempts.append(record)
        if status == "NONUNIT":
            winner = record
            break
    result = {
        "schema": "KRENN_X5_REP2_SPARSE_MONOMIAL_TRIPLE_SEARCH_V1",
        "status": "PASS_FOUND_TERMINAL_NONUNIT_TRIPLE" if winner else "FAIL_CLOSED_NO_NONUNIT_IN_MONOMIAL_TRIPLES",
        "candidate_triple_count": len(triples),
        "normalized_group_count": len(groups),
        "attempt_count": len(attempts),
        "attempts": attempts,
        "winner": winner,
        "minimum_extra_coordinate_count_with_nonunit": 3 if winner else None,
        "scope": "all triples co-occurring in at least one newly activated amplitude monomial",
    }
    path = HERE / "results_monomial_triples.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)
    print(json.dumps({
        "status": result["status"],
        "candidate_triples": len(triples),
        "groups": len(groups),
        "attempts": len(attempts),
        "winner": winner["representative"] if winner else None,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
