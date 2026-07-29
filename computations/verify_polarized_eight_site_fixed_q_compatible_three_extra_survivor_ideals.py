#!/usr/bin/env python3
"""Resumable exact ideals for compatible three-extra projective survivors.

This is a follow-up to
``verify_polarized_eight_site_fixed_q_three_extra_frontier.py``.  It rebuilds
the 87,027 triples of invisible cells for which the fixed displayed z keeps
the polarized target identically, applies the sound projective closure, drops
the sole one-physical-pair survivor (covered by the separate arbitrary
one-block theorem), and computes saturated full coordinate ideals for the
remaining 742 multi-pair survivors.

Successful Singular results are cached as small JSON records, so an
interrupted batch can be resumed without trusting incomplete jobs.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess
import time

import verify_polarized_eight_site_fixed_q_three_extra_frontier as frontier


EXPECTED_COMPATIBLE_TRIPLES = 87_027
EXPECTED_PROJECTIVE_SURVIVORS = Counter({1: 1, 2: 229, 3: 513})
EXPECTED_MULTI_PAIR_SURVIVORS = 742
EXPECTED_PROJECTIVE_SURVIVOR_SHA256 = (
    "b481e4abddc0e98e8cbde9486d7d384a821430b15964dde6e9b279367988a57a"
)
EXPECTED_FULL_RESULT_SHA256 = (
    "7ea7959152651bf9564d5d21222afdc93c6158ea116d13e85341d63c3ddeed77"
)


def compatible_triples():
    invisible = tuple(
        cell for cell in frontier.ALL_CELLS
        if cell not in frontier.BASE_Q and not frontier.single_debt(cell)
    )
    assert len(invisible) == 99
    compatible_pairs = frozenset(
        (left, right) for left, right in combinations(invisible, 2)
        if not frontier.cross_debt(left, right)
    )
    assert len(compatible_pairs) == 3_960
    triples = []
    for triple in combinations(invisible, 3):
        if not all(pair in compatible_pairs for pair in combinations(triple, 2)):
            continue
        assert not frontier.triple_debt(*triple)
        triples.append(triple)
    assert len(triples) == EXPECTED_COMPATIBLE_TRIPLES
    return tuple(triples)


def multi_pair_projective_survivors(triples):
    survivor_counts = Counter()
    multi_pair = []
    digest = hashlib.sha256()
    for triple in triples:
        physical_pair_count = len({cell[:2] for cell in triple})
        closed, branches, kinds, reason = frontier.projective_closure(triple)
        if not closed:
            survivor_counts[physical_pair_count] += 1
            record = (triple, physical_pair_count, reason, branches)
            digest.update(repr(record).encode())
            digest.update(b"\n")
            if physical_pair_count >= 2:
                multi_pair.append(triple)
    assert survivor_counts == EXPECTED_PROJECTIVE_SURVIVORS
    assert len(multi_pair) == EXPECTED_MULTI_PAIR_SURVIVORS
    assert digest.hexdigest() == EXPECTED_PROJECTIVE_SURVIVOR_SHA256
    return tuple(multi_pair), survivor_counts, digest.hexdigest()


def full_program(triple):
    forms, q_four = frontier.tagged_forms(triple)
    equations = []
    for word in sorted(set(forms) | set(q_four) | set(frontier.DELTA_WORDS)):
        terms = []
        for (edge, tag), coefficient in sorted(forms.get(word, {}).items()):
            frontier.append_term(
                terms,
                4 * coefficient,
                (frontier.TAG_MONOMIAL[tag], frontier.beta_expression(edge)),
            )
        for tag, coefficient in sorted(q_four.get(word, {}).items()):
            frontier.append_term(
                terms, 4 * coefficient, ("a", frontier.TAG_MONOMIAL[tag])
            )
        if word in frontier.DELTA_WORDS:
            terms.append("-1")
        if terms:
            equations.append("+".join(terms))
    equations.append("h*t*u*v-1")
    variables = frontier.ring_variables()
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "option(redSB);\nideal G=std(I);\n"
        'print("BASIS_SIZE");\nprint(size(G));\n'
        'print("BASIS_FIRST");\nprint(G[1]);\n'
    )
    return program, len(equations), len(variables)


def cache_path(cache_dir, index, triple):
    token = hashlib.sha256(repr(triple).encode()).hexdigest()[:16]
    return cache_dir / f"{index:04d}-{token}.json"


def validated_cached_result(path, index, triple, program_sha256):
    if not path.exists():
        return None
    try:
        result = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    expected = {
        "index": index,
        "triple": [list(cell) for cell in triple],
        "program_sha256": program_sha256,
        "basis_size": "1",
        "basis_first": "1",
    }
    if any(result.get(key) != value for key, value in expected.items()):
        return None
    return result


def run_job(executable, cache_dir, index, triple, timeout):
    program, equation_count, variable_count = full_program(triple)
    program_sha256 = hashlib.sha256(program.encode()).hexdigest()
    path = cache_path(cache_dir, index, triple)
    cached = validated_cached_result(path, index, triple, program_sha256)
    if cached is not None:
        cached["cached"] = True
        return cached

    start = time.monotonic()
    process = subprocess.run(
        [executable, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    elapsed = time.monotonic() - start
    if process.stderr.strip():
        raise AssertionError(process.stderr)
    lines = tuple(line.strip() for line in process.stdout.splitlines() if line.strip())
    basis_size = lines[lines.index("BASIS_SIZE") + 1]
    basis_first = lines[lines.index("BASIS_FIRST") + 1]
    assert basis_size == basis_first == "1", process.stdout
    result = {
        "index": index,
        "triple": [list(cell) for cell in triple],
        "program_sha256": program_sha256,
        "equations": equation_count,
        "variables": variable_count,
        "basis_size": basis_size,
        "basis_first": basis_first,
        "seconds": elapsed,
        "cached": False,
    }
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(result, sort_keys=True) + "\n")
    temporary.replace(path)
    return result


def result_digest(results):
    digest = hashlib.sha256()
    for result in sorted(results, key=lambda item: item["index"]):
        stable = (
            result["index"],
            tuple(tuple(cell) for cell in result["triple"]),
            result["program_sha256"],
            result["equations"],
            result["variables"],
            result["basis_size"],
            result["basis_first"],
        )
        digest.update(repr(stable).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("/tmp/krenn-compatible-three-extra-ideals"),
    )
    parser.add_argument(
        "--limit", type=int,
        help="run only the first N ideals (diagnostic; not a complete proof)",
    )
    parser.add_argument(
        "--print-survivors", action="store_true",
        help="print the exact ordered 742-triple ideal frontier",
    )
    args = parser.parse_args()
    assert args.workers >= 1 and args.timeout >= 1

    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required")
    args.cache_dir.mkdir(parents=True, exist_ok=True)

    start = time.monotonic()
    triples = compatible_triples()
    survivors, survivor_counts, survivor_sha256 = multi_pair_projective_survivors(triples)
    print("compatible triples:", len(triples), flush=True)
    print("projective survivor counts:", dict(sorted(survivor_counts.items())), flush=True)
    print("multi-pair ideal frontier:", len(survivors), flush=True)
    print("projective-survivor sha256:", survivor_sha256, flush=True)
    if args.print_survivors:
        for index, triple in enumerate(survivors):
            print("survivor", index, triple, flush=True)

    selected = tuple(enumerate(survivors))
    if args.limit is not None:
        assert args.limit >= 0
        selected = selected[:args.limit]

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                run_job, executable, args.cache_dir, index, triple, args.timeout
            ): (index, triple)
            for index, triple in selected
        }
        for completed, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            print(
                "completed", completed, "/", len(selected),
                "index", result["index"],
                "equations", result["equations"],
                "seconds", f"{result['seconds']:.3f}",
                "cached", result["cached"],
                flush=True,
            )

    assert len(results) == len(selected)
    assert all(
        result["variables"] == 53
        and result["basis_size"] == result["basis_first"] == "1"
        for result in results
    )
    print("unit ideals:", len(results), "/", len(selected))
    digest = result_digest(results)
    print("result sha256:", digest)
    print("wall seconds:", f"{time.monotonic() - start:.3f}")
    if args.limit is not None:
        print("DIAGNOSTIC PREFIX ONLY: no complete 742-ideal claim")
    else:
        assert digest == EXPECTED_FULL_RESULT_SHA256
        print("all 742 compatible multi-pair survivors excluded: PASS")


if __name__ == "__main__":
    main()
