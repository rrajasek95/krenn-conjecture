#!/usr/bin/env python3
"""Independent exact replay of the exception-1114 symbolic reduction seal."""

from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-exception1114-rank1-refinement-design-2026-08-26"


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


result_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "results_symbolic_reduction.json"
result = json.loads(result_path.read_text())
require(result["status"] == "PASS_EXACT_SYMBOLIC_REDUCTION_ZERO_SOLVES")
require(result["scope"]["singular_runs"] == result["scope"]["sat_runs"] == result["scope"]["cnf_reads"] == 0)
require(result["scope"]["records_closed"] == 0 and result["scope"]["conjecture_claim"] is False)
require(result["exact_generator_reduction"]["original_generators"] == 6553)
require(result["exact_generator_reduction"]["exact_Q_rank"] == 6533)
require(result["exact_generator_reduction"]["signed_relation_count"] == 20)
require(result["exact_generator_reduction"]["relation_sizes"] == {"2": 16, "4": 4})
require(result["source_site_symmetry"]["residual_color_S2_orbits"] == 1094)
require(result["source_site_symmetry"]["formal_guard_stabilizer_order"] == 1)
require(result["determinantal_rank_strata"]["rank_profiles"] == 27)
require(result["determinantal_rank_strata"]["raw_minor_charts"] == 1331)
require(result["elimination_exhaustion"]["localized_unit_coefficient_scan"]["hits"] == [])

for pin in result["pins"].values():
    path = Path(pin["path"])
    require(path.is_file() and sha(path) == pin["sha256"], ("pin", path))

spec = importlib.util.spec_from_file_location("sealed_refinement", PARENT / "build_refinement.py")
require(spec is not None and spec.loader is not None)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
equations = b.all_equations()
relations = result["exact_generator_reduction"]["relations"]
removed = []
for relation in relations:
    coefficients = {int(index): Fraction(coefficient) for index, coefficient in relation["coefficients"].items()}
    require(b.add(*(b.scale(equations[index], coefficient) for index, coefficient in coefficients.items())) == b.ZERO)
    require(relation["removed_equation"] == max(coefficients))
    removed.append(relation["removed_equation"])
require(removed == result["exact_generator_reduction"]["removed_original_equation_indices"])
require(len(set(removed)) == 20)
kept = [equation for index, equation in enumerate(equations) if index not in set(removed)]
require(len(kept) == 6533)

source_path = HERE / result["verdict"]["held_source_path"]
require(source_path.is_file() and sha(source_path) == result["verdict"]["held_source_sha256"])
expected_source = b.build_program(kept).replace(
    "HELD DIAGNOSTIC ONLY: rep1114 rank1 z1/full-torus canonical chart",
    "HELD DIAGNOSTIC ONLY: exact 20-relation dedup of rep1114 rank1 z1/full-torus chart",
)
require(source_path.read_text() == expected_source)
require(source_path.read_text().count(",\n") == 6532)

analysis_spec = importlib.util.spec_from_file_location("symbolic_analysis", HERE / "analyze_symbolic.py")
require(analysis_spec is not None and analysis_spec.loader is not None)
analysis = importlib.util.module_from_spec(analysis_spec)
analysis_spec.loader.exec_module(analysis)
minor = result["jacobian"]
prime = minor["prime"]
values = analysis.random_values(prime, 1)
rows = analysis.jacobian(kept, values, prime)
selected = minor["selected_deduplicated_row_indices"]
require(len(selected) == 58 and len(set(selected)) == 58)
require(analysis.determinant_mod([rows[index] for index in selected], prime) == minor["determinant_mod_prime"] != 0)

held_path = HERE / result["verdict"]["held_plan_path"]
require(held_path.is_file() and sha(held_path) == result["verdict"]["held_plan_sha256"])
held = json.loads(held_path.read_text())
require(held["status"] == "HELD_Q_ZERO_SOLVE_NO_CLEARANCE")
require(held["source"]["variables"] == 58 and held["source"]["generators"] == 6533)
require(held["source"]["sha256"] == sha(source_path))

print("PASS exact symbolic reduction replay: 58 variables / 6533 generators / full Jacobian / zero solve")
