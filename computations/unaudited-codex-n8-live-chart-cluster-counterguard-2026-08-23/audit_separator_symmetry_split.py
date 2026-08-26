#!/usr/bin/env python3
"""Replay the sound symmetry reduction and scoped terminal timeout ledger."""

from hashlib import sha256
from itertools import permutations
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ATLAS_PATH = (ROOT / "computations/unaudited-codex-n8-chart-c4-transition-2026-08-23"
              / "audit_chart_c4_transition.py")
FIXED = HERE / "separating_support_cap36_symbreak_progress.json"
SPLIT = HERE / "separating_support_cap36_orbit_split.json"
RESULT = HERE / "results_separator_symmetry_split_audit.json"
EXPECTED = {
    ATLAS_PATH: "9fed1ac370435a1cb1b0ca60fd5bf4591f1d659fd4c191ab929d8231b2697722",
    FIXED: "fa105590a8c11597bd6daa9d63d314cd783599fd90f049a56e3c4eb656376e17",
    SPLIT: "bf84b185ef3113835ee6e5990ddecf59b7fa3cf85503e49e2be1ee3eb9c18b86",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def site_transform(triple, sigma):
    return tuple(tuple(sorted(tuple(sorted((sigma[u], sigma[v])))
                              for u, v in matching))
                 for matching in triple)


def labelled_orbit(triple):
    answer = set()
    for sigma in permutations(range(8)):
        changed = site_transform(triple, sigma)
        for colour_permutation in permutations(range(3)):
            answer.add(tuple(changed[colour_permutation[c]] for c in range(3)))
    return answer


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                ("source drift", path))
    atlas = load(ATLAS_PATH, "separator_split_replay_atlas")
    rows = tuple(sorted(atlas.CHART.SOURCE.target_orbit_rows()))
    representatives = {index: atlas.chart_triple(rows[index - 1])
                       for index in range(1, 32)}
    forbidden = (11, 24, 25)
    sizes = {index: len(labelled_orbit(representatives[index]))
             for index in forbidden}
    union = set().union(*(labelled_orbit(representatives[index])
                          for index in forbidden))
    allowed = tuple(index for index in range(1, 32)
                    if index not in forbidden)
    if mutate:
        allowed = allowed[:-1]
    require(sizes == {11: 7560, 24: 1260, 25: 30240}, sizes)
    require(len(union) == 39060, len(union))
    require(len(allowed) == 28, len(allowed))

    fixed = json.loads(FIXED.read_text())
    split = json.loads(SPLIT.read_text())
    require(fixed == {
        "cap": 36,
        "elapsed_seconds": 104.11795016698306,
        "fixed_colour0_matching": [[0, 1], [2, 3], [4, 5], [6, 7]],
        "forbidden_labelled_triples": 39060,
        "format": "n8-live-chart-separator-symbreak-progress-v1",
        "phase": "SOLVING",
        "round": 420,
        "selected_cells": 16,
        "singleton_gadgets": 6834,
        "singletons_in_last_model": 10,
    }, "fixed matching checkpoint changed")
    require(split["status"] == "TIMEOUT_UNRESOLVED_28_ORBIT_SPLIT"
            and split["active_cases"] == list(allowed)
            and split["solver_calls"] == 104
            and split["singleton_gadgets"] == 6830
            and split["forbidden_labelled_triples"] == 39060
            and all(status != "UNSAT"
                    for status in split["case_status"].values()),
            "split terminal scope changed")
    timed = sorted(int(index) for index, count in split["case_timeouts"].items()
                   if count)
    require(len(timed) == 24, timed)

    result = {
        "format": "n8-live-chart-separator-symmetry-audit-v1",
        "status": "UNRESOLVED_NO_SAT_NO_UNSAT",
        "sound_symmetry_lemma": (
            "Every admissible support has a live pure matching in each colour. "
            "The resulting ordered pure triple belongs to one of 31 S8xS3 "
            "atlas orbits. Since live triples of types 11,24,25 are forbidden, "
            "the remaining 28 representative seeds are exhaustive WLOG."
        ),
        "forbidden_orbit_sizes": {str(key): value for key, value in sizes.items()},
        "forbidden_labelled_triples": len(union),
        "allowed_seed_orbits": list(allowed),
        "fixed_matching_phase": {
            "round": fixed["round"],
            "elapsed_seconds": fixed["elapsed_seconds"],
            "singleton_gadgets": fixed["singleton_gadgets"],
        },
        "orbit_split_phase": {
            "elapsed_seconds": split["elapsed_seconds"],
            "solver_calls": split["solver_calls"],
            "singleton_gadgets": split["singleton_gadgets"],
            "active_cases": split["active_cases"],
            "call_timeout_cases": timed,
            "case_calls": split["case_calls"],
            "case_timeouts": split["case_timeouts"],
        },
        "scope": (
            "The bounded aggregate found neither a singleton-free support nor "
            "an UNSAT case. It proves no global hitting-number bound. Every "
            "singleton gadget added is a sound exact implication, but incomplete "
            "clause learning plus timeout has no feasibility consequence."
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(json.loads(RESULT.read_text()) == result, "stored result drift")
    print(result["status"])
    print(result["logical_sha256"])


if __name__ == "__main__":
    main()
