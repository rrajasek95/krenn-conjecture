#!/usr/bin/env python3
"""Replay the isolated C4-boundary support guard and bounded coefficient gate."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPORT_SCRIPT = HERE / "export_isolated_support_f4sat.py"
EXPORT_RESULT = HERE / "results_isolated_support_export.json"
RUNNER = HERE / "run_isolated_support_f4sat.py"
RUN_RESULT = HERE / "results_isolated_support_f4sat_manifest.json"
D12 = (ROOT / "computations/unaudited-codex-n8-chart1-boundary-a0200-2026-08-23"
       / "checkpoint_d12_lazy_cegar.json")
ATLAS = (ROOT / "computations/unaudited-codex-n8-chart-c4-boundary-atlas-2026-08-23"
         / "results_c4_boundary_atlas.json")
RESULT = HERE / "results_recursive_boundary_counterguard.json"
EXPECTED = {
    EXPORT_SCRIPT: "f4b1c50959380f296118d11a8ca4e3a54929035605acc441bc36d140d968d664",
    EXPORT_RESULT: "a1adc569f4d45cb724054ea7aecc44b045289477c11f4ffe8b01e38e22adfa31",
    RUNNER: "d4ed27f0950cabb7d83d1016f8d03d18fc30679c3edab6e9a4b7d030f76855ca",
    RUN_RESULT: "0c982223bcd0c2b7d13be2837923826afe25be46c8cad65ad171b2024a798ee9",
    D12: "1ddd96e2cad9cf132336db0b68d208292554b96d4acb2df1879dd6f0e7db366f",
    ATLAS: "14706238c6bb4707707400aa2f80980ca86247c9f2c0e669d0918613cbebc370",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                ("source drift", path))
    E = load(EXPORT_SCRIPT, "recursive_boundary_export_replay")
    exported = json.loads(EXPORT_RESULT.read_text())
    run = json.loads(RUN_RESULT.read_text())
    d12 = json.loads(D12.read_text())
    atlas = json.loads(ATLAS.read_text())

    replacements = []
    for left, right in combinations(E.BASE, 2):
        a, b = left; c, d = right
        replacements.extend((((a, c), (b, d)), ((a, d), (b, c))))
    exits = [sum(set(replacement) <= graph for replacement in replacements)
             for graph in E.GRAPHS]
    if mutate:
        exits[0] += 1
    require(exits == [0, 0, 0], exits)
    require((0, 2) not in E.GRAPHS[0]
            and (0, 2) in E.GRAPHS[1]
            and (0, 2) in E.GRAPHS[2], "marked boundary")

    mixed = Counter()
    profile_min = {}
    pure_before = []
    for word in product(range(3), repeat=8):
        pure = len(set(word)) == 1
        poly = E.polynomial(word, pure)
        if pure:
            pure_before.append(len(poly) + 1)
        else:
            mixed[len(poly)] += 1
            profile = tuple(sorted((word.count(c) for c in range(3)), reverse=True))
            profile_min[profile] = min(profile_min.get(profile, 999), len(poly))
    require(sum(mixed.values()) == 6558 and min(mixed) == 12,
            (sum(mixed.values()), min(mixed)))
    require(pure_before == [10, 13, 12], pure_before)
    require({"-".join(map(str, key)): value for key, value in profile_min.items()}
            == exported["mixed_profile_minimum_terms"], "profile drift")
    require(exported["source_variables"] == 204
            and exported["source_rows"] == 6561
            and exported["source_monomial_terms"] == 372669
            and exported["base_live_c4_exits"] == 0,
            "export interface drift")

    require(d12["last_dual"] == [["0d55b8ee", 1, 1]]
            and d12["ledger"][-1]["new_violating_column_orbits"] == 42,
            "round-six packet drift")
    require(all(exported["round6_control"].values()),
            "round-six live controls drift")
    first = atlas["first_uncovered_representative"]
    require(first["source_chart"] == 1 and first["destination_chart"] == 2
            and first["zero_cells"] == [[0, 6]], first)
    require(run["status"] == "TIMEOUT"
            and run["returncode"] == -15
            and run["elapsed_seconds"] < 301
            and run["files"]["isolated_support_full_live_p1073741827.gb.out"]["bytes"] == 0,
            "bounded gate terminal drift")

    result = {
        "format": "n8-recursive-c4-boundary-counterguard-v1",
        "status": "SUPPORT_RECURSION_FALSE_COEFFICIENT_FEASIBILITY_UNRESOLVED",
        "counterguard": {
            "support_cells": 216,
            "normalized_anchor_cells": 12,
            "nonanchor_live_variables": 204,
            "marked_boundary": "A_02[0,0]=0 with A_02[1,1],A_02[2,2] live",
            "cross_colour_cells": "all 168 live",
            "diagonal_cells_per_colour": [16, 16, 16],
            "base_live_c4_exits_per_colour": exits,
            "pure_fibre_counts": pure_before,
            "minimum_mixed_fibre": min(mixed),
            "profile_minimum_terms": exported["mixed_profile_minimum_terms"],
            "round6_dual_row_live": True,
            "round6_incident_killers": 42,
        },
        "formal_no_go": (
            "The normalized base triple is isolated in the live C4 exchange "
            "graph, although the support is cross-colour dense and triggers "
            "neither block-diagonal nor matching-hole antecedents. Every literal "
            "mixed row has at least twelve live normalized monomials. Therefore "
            "no support/singleton implication, including the 42-killer packet, "
            "forces an alternate flip or a known closure. Since C4 transitions "
            "are reversible, no statistic can be strictly decreasing on every "
            "live transition; this isolated vertex also defeats an existence-of-"
            "lower-neighbour rule at the support level."
        ),
        "coefficient_gate": {
            "prime": 1073741827,
            "variables": 204,
            "source_rows": 6561,
            "source_terms": 372669,
            "live_saturator": "product of all 204 nonanchor live variables",
            "status": run["status"],
            "elapsed_seconds": run["elapsed_seconds"],
            "sampled_peak_rss_kib": 5849240,
            "basis_bytes": 0,
        },
        "scope": (
            "This is a literal source-support and row-incidence counterguard, "
            "not an X5 solution. The full coefficient-coupled Laurent gate timed "
            "out and gives neither feasibility nor infeasibility, over the prime "
            "or in characteristic zero. Hence a genuinely coefficient-sensitive "
            "boundary identity remains possible but is not supplied by recursive "
            "C4 support descent."
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
