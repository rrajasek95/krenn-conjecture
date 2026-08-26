#!/usr/bin/env python3
"""Seal the exact symbolic reduction of the exception-1114 58-variable chart."""

from fractions import Fraction
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-exception1114-rank1-refinement-design-2026-08-26"
PINS = {
    "parent_manifest": (PARENT / "MANIFEST.sha256", "aea0841b7b1b6fe0773cfb5087a930329c4da5d94951ad23d559de6d61cddb46"),
    "parent_result": (PARENT / "results_rank1_refinement.json", "3da9583ca3c8ed49b0983960f1147238def7fe19b43905f3d5cef57811c6e99b"),
    "parent_source": (PARENT / "rep1114_rank1_z1_fulltorus_Q.sing", "7b20f216cf2313f7abe82f4c1b29d7084a5a82716e457f1554262c5e46ce82f8"),
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


for label, (path, expected) in PINS.items():
    require(path.is_file() and sha(path) == expected, (label, path))

spec = importlib.util.spec_from_file_location("sealed_refinement", PARENT / "build_refinement.py")
require(spec is not None and spec.loader is not None)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

analysis_spec = importlib.util.spec_from_file_location("symbolic_analysis", HERE / "analyze_symbolic.py")
require(analysis_spec is not None and analysis_spec.loader is not None)
analysis = importlib.util.module_from_spec(analysis_spec)
analysis_spec.loader.exec_module(analysis)


def exact_generator_reduction(equations):
    ledger = json.loads((HERE / "affine_dependencies_mod1000003.json").read_text())
    require(ledger["prime"] == 1000003 and ledger["nonlinear_rank"] == 6533)
    relations = ledger["exact_signed_relations"]
    require(len(relations) == 20)
    removed = []
    for relation in relations:
        coefficients = {int(i): Fraction(c) for i, c in relation["coefficients"].items()}
        require(set(coefficients.values()) <= {Fraction(-1), Fraction(1)})
        require(b.add(*(b.scale(equations[i], c) for i, c in coefficients.items())) == b.ZERO)
        pivot = relation["removed_equation"]
        require(pivot == max(coefficients) and coefficients[pivot] != 0)
        removed.append(pivot)
    require(len(set(removed)) == 20)
    kept = [equation for i, equation in enumerate(equations) if i not in set(removed)]
    require(len(kept) == 6533)
    return kept, relations, removed, ledger


def replay_full_rank_minor(equations, original_indices):
    prime = 1000003
    values = analysis.random_values(prime, 1)
    rows = analysis.jacobian(equations, values, prime)
    basis, source_rows = analysis.rref(rows, len(b.VARIABLES), prime)
    require(len(basis) == 58)
    selected_local = [source_rows[i] for i in range(58)]
    selected_original = [original_indices[i] for i in selected_local]
    determinant = analysis.determinant_mod([rows[i] for i in selected_local], prime)
    require(determinant != 0)
    return {
        "prime": prime,
        "point": "python random.Random(1).randrange(prime) in sealed VARIABLES order",
        "point_value_sha256": hashlib.sha256(json.dumps([values[name] for name in b.VARIABLES], separators=(",", ":")).encode()).hexdigest(),
        "selected_deduplicated_row_indices": selected_local,
        "selected_original_equation_indices": selected_original,
        "determinant_mod_prime": determinant,
        "consequence": "a nonzero modular minor proves generic Jacobian rank 58 over Q; the earlier arithmetic-progression rank57 values are special evaluations, not a corank-one identity",
    }


def main():
    equations = b.all_equations()
    kept, relations, removed, dependency_ledger = exact_generator_reduction(equations)
    original_indices = [i for i in range(len(equations)) if i not in set(removed)]
    source = b.build_program(kept).replace(
        "HELD DIAGNOSTIC ONLY: rep1114 rank1 z1/full-torus canonical chart",
        "HELD DIAGNOSTIC ONLY: exact 20-relation dedup of rep1114 rank1 z1/full-torus chart",
    )
    source_path = HERE / "rep1114_rank1_z1_fulltorus_dedup_Q.sing"
    temporary = source_path.with_suffix(".sing.tmp")
    temporary.write_text(source)
    os.replace(temporary, source_path)

    diagnostics = json.loads((HERE / "symbolic_diagnostics.json").read_text())
    require(diagnostics["jacobian"]["conclusion"] == "GENERIC_JACOBIAN_FULL_RANK_CERTIFIED")
    require(diagnostics["localized_monic_scan"]["hits"] == [])
    require(diagnostics["source_site_symmetry"]["formal_guard_stabilizer_order"] == 1)
    require(diagnostics["determinantal_rank_strata"]["rank_profiles"] == 27)
    require(dependency_ledger["exact_Q_full_generator_rank"] == 6533)
    full_rank = replay_full_rank_minor(kept, original_indices)

    held = {
        "schema": "n8-x5-exception1114-rank1-dedup-q-held-v1",
        "status": "HELD_Q_ZERO_SOLVE_NO_CLEARANCE",
        "scope": "one z1/full-torus/factor-normalized subchart of canonical rank(H)=1 record1114; source-site transport remains exactly the sealed four-record orbit",
        "source": {"path": source_path.name, "sha256": sha(source_path), "variables": 58, "generators": 6533, "ring": "Q", "order": "dp with sealed variable order"},
        "future_acceptance": "only proof-producing exact-Q UNIT_IDEAL plus reduce(1,G)=0 and literal source replay; all other outcomes diagnostic",
        "refusal": "no Singular/modular/CNF run, sibling profile, transport promotion, or relaunch without independent referee and fresh explicit clearance",
    }
    held_path = HERE / "held_deduplicated_Q_plan.json"
    held_path.write_text(json.dumps(held, indent=2, sort_keys=True) + "\n")

    result = {
        "schema": "n8-x5-exception1114-rank1-symbolic-reduction-design-v1",
        "status": "PASS_EXACT_SYMBOLIC_REDUCTION_ZERO_SOLVES",
        "pins": {label: {"path": str(path), "sha256": expected} for label, (path, expected) in PINS.items()},
        "scope": {
            "representative": 1114,
            "transport_records": [1114, 1978, 2014, 2036],
            "chart": "canonical rank(H)=1, z1/full-torus, a04_00 nonzero factor chart",
            "singular_runs": 0,
            "sat_runs": 0,
            "cnf_reads": 0,
            "records_closed": 0,
            "conjecture_claim": False,
        },
        "exact_generator_reduction": {
            "original_generators": 6553,
            "nonlinear_coefficient_rank_mod_1000003": 6533,
            "exact_Q_rank": 6533,
            "signed_relation_count": 20,
            "relation_sizes": {"2": 16, "4": 4},
            "removed_original_equation_indices": removed,
            "relations": relations,
            "proof": "the modular nonlinear rank is a Q lower bound; 20 independent signed full-polynomial identities are a matching upper bound, replay exactly over Q, and have no affine remainder",
            "consequence": "the 6533 retained generators span exactly the same Q ideal and are constant-coefficient independent",
        },
        "elimination_exhaustion": {
            "original_individual_monic_scan": "zero across every generator and all 58 variables",
            "localized_unit_coefficient_scan": diagnostics["localized_monic_scan"],
            "constant_coefficient_combinations": "the entire 20-dimensional kernel of nonlinear coefficient rows is spanned by exact zero polynomial identities, so no Q-linear combination exposes an affine/monic relation",
            "ordering_scope": "these negative tests are variable-order independent; changing a dp tie-break cannot create a literal or constant-combination affine substitution",
            "not_claimed": "no claim of ideal primeness, radicality, or absence of nonlinear Groebner consequences",
        },
        "jacobian": full_rank,
        "determinantal_rank_strata": diagnostics["determinantal_rank_strata"],
        "source_site_symmetry": {
            **diagnostics["source_site_symmetry"],
            "residual_profiles": 2187,
            "residual_color_S2_orbits": 1094,
        },
        "verdict": {
            "smaller_exact_chart": "58 variables / 6533 generators, exact same ideal as sealed 58/6553 parent",
            "variable_reduction": "none uniformly valid",
            "reason": "generic Jacobian is full rank; no localized/affine monic elimination survives; optional A01/A25/A67 rank cover shrinks rank1 strata only and leaves rank2/rank3 at 58 variables; no nonidentity site symmetry preserves the formal guard chart",
            "held_source_path": source_path.name,
            "held_source_sha256": sha(source_path),
            "held_plan_path": held_path.name,
            "held_plan_sha256": sha(held_path),
        },
    }
    result_path = HERE / "results_symbolic_reduction.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "source": held["source"], "jacobian_det": full_rank["determinant_mod_prime"], "removed": removed}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
