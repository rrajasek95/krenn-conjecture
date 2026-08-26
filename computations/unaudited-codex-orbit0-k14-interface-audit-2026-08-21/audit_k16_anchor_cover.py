#!/usr/bin/env python3
"""Finite equivariant cover/affine-incidence audit for the orbit-zero K16 tail."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K14_PATH = HERE / "audit_orbit0_k14_interface.py"
SPEC = importlib.util.spec_from_file_location("k14", K14_PATH)
K14 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(K14)
F = K14.FROZEN
OUT = HERE / "results_k16_anchor_cover.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def exact_consistent(rows, variable_count):
    """Solve sparse rational equations; each row is (coefficients, rhs)."""
    pivots = {}
    for coefficients, rhs in rows:
        row = [Fraction(value) for value in coefficients] + [Fraction(rhs)]
        while True:
            pivot = next((i for i in range(variable_count) if row[i]), None)
            if pivot is None:
                if row[-1]:
                    return False
                break
            if pivot not in pivots:
                scale = row[pivot]
                row = [value / scale for value in row]
                pivots[pivot] = row
                break
            scale = row[pivot]
            old = pivots[pivot]
            row = [left - scale * right for left, right in zip(row, old, strict=True)]
    return True


def build():
    raw = json.loads(F.R8P.read_text())
    residual = tuple(bytes.fromhex(row) for row, _n, _d in raw["residual"])
    three_words = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    anchor_terms = tuple(F.BASE.term_ids(word, F.M0) for word in three_words)
    errors = tuple(Counter({
        term: 1 for term in F.BASE.word_terms(word)
        if term != anchor and F.row_k_degree(term) == 2
    }) for word, anchor in zip(three_words, anchor_terms, strict=True))
    leading_packet = F.polynomial_product(F.polynomial_product(errors[0], errors[1]), errors[2])
    factor_set = frozenset(anchor_terms)
    stabilizer = tuple(action for action in range(len(F.EXPORT.STABILIZER))
                       if frozenset(F.move_row(term, action) for term in anchor_terms)
                       == factor_set)
    require(len(stabilizer) == 384, len(stabilizer))
    h_representatives = []
    for representative in residual:
        unseen = set(F.EXPORT.row_orbit(representative))
        while unseen:
            seed = min(unseen)
            orbit = F.orbit_under(seed, stabilizer)
            h_representatives.append(seed)
            unseen.difference_update(orbit)
    require(len(h_representatives) == 485, len(h_representatives))

    cells = tuple(sorted(F.A))
    position = {cell: index for index, cell in enumerate(cells)}
    vectors = []
    tails = []
    labels = []
    for colours in product(range(3), repeat=4):
        if len(set(colours)) == 1:
            continue
        word = F.word_from_pair_colours(colours)
        anchor = F.BASE.term_ids(word, F.M0)
        vectors.append(tuple(Counter(anchor)[cell] for cell in cells))
        tails.append(tuple(term for term in F.BASE.word_terms(word)
                           if F.row_k_degree(term) == 2))
        labels.append(colours)
    require(len(vectors) == len(tails) == len(labels) == 78, "mixed rows")
    pivot_cache = {}

    def pivots(signature):
        if signature not in pivot_cache:
            pivot_cache[signature] = tuple(i for i, vector in enumerate(vectors)
                                           if all(a >= b for a, b in zip(signature, vector, strict=True)))
        return pivot_cache[signature]

    permutations = []
    for action in stabilizer:
        transform = F.EXPORT.TRANSFORMS[action]
        permutations.append(tuple(position[transform[cell]] for cell in cells))

    def canonical(signature):
        images = []
        for permutation in permutations:
            moved = [0] * 12
            for old, new in enumerate(permutation):
                moved[new] = signature[old]
            images.append(tuple(moved))
        return min(images)

    k14 = Counter()
    for r8 in h_representatives:
        for packet in leading_packet:
            target = bytes(sorted(r8 + packet))
            counts = Counter(target)
            signature = tuple(counts[cell] for cell in cells)
            k14[signature] += 1
    require(sum(k14.values()) == 838080 and len(k14) == 216,
            (sum(k14.values()), len(k14)))
    representatives = sorted({canonical(signature) for signature in k14})
    require(len(representatives) == 33, len(representatives))

    candidate_data = {}
    cover_groups = []
    all_tail_orbits = set()
    zero_affine = []
    affine_obstructed = []
    affine_instances = {}
    forced_single_pivot_orbits = set()
    for signature in representatives:
        columns = []
        candidate_orbit_sets = []
        coordinate_universe = set()
        for pivot in pivots(signature):
            base = tuple(a - b for a, b in zip(signature, vectors[pivot], strict=True))
            survivor_counter = Counter()
            for tail in tails[pivot]:
                tail_count = Counter(tail)
                tail_vector = tuple(tail_count[cell] for cell in cells)
                new = tuple(a + b for a, b in zip(base, tail_vector, strict=True))
                if not pivots(new):
                    survivor_counter[new] += 1
            columns.append(survivor_counter)
            orbit_set = frozenset(canonical(row) for row in survivor_counter)
            candidate_orbit_sets.append(orbit_set)
            all_tail_orbits.update(orbit_set)
            coordinate_universe.update(survivor_counter)
        require(columns, signature)
        rows = [(tuple(1 for _ in columns), 1)]
        for coordinate in sorted(coordinate_universe):
            rows.append((tuple(column[coordinate] for column in columns), 0))
        if exact_consistent(rows, len(columns)):
            zero_affine.append(signature)
        else:
            affine_obstructed.append(signature)
            affine_instances[signature] = (tuple(columns),
                                           tuple(sorted(coordinate_universe)))
        forced = set.intersection(*(set(row) for row in candidate_orbit_sets))
        forced_single_pivot_orbits.update(forced)
        deduplicated = sorted({tuple(sorted(row)) for row in candidate_orbit_sets})
        minimal_candidates = []
        for row in map(frozenset, deduplicated):
            if not any(other < row for other in map(frozenset, deduplicated)):
                minimal_candidates.append(row)
        cover_groups.append(tuple(sorted(set(minimal_candidates),
                                         key=lambda row: (len(row), tuple(row)))))
        candidate_data[str(signature)] = {
            "available_literal_pivots": len(columns),
            "distinct_single_pivot_orbit_sets": len(deduplicated),
            "minimum_single_pivot_orbit_count": min(map(len, deduplicated)),
            "forced_orbits_across_single_pivots": [str(row) for row in sorted(forced)],
            "candidate_orbit_sets": [[str(item) for item in row] for row in deduplicated],
            "zero_in_exact_signature_affine_hull": signature in zero_affine,
        }

    # Exact minimum-union cover for the single-pivot model. A group is
    # satisfied when the chosen global orbit set contains all survivor orbits
    # of at least one literal pivot. Removing a strict superset candidate is
    # safe. The recursion selects an unsatisfied group and branches over every
    # remaining minimal candidate, so termination proves the lower bound as
    # well as producing an upper-bound witness.
    nontrivial_groups = tuple(group for group in cover_groups
                              if not any(len(row) == 0 for row in group))
    orbit_list = tuple(sorted(all_tail_orbits))
    orbit_index = {row: index for index, row in enumerate(orbit_list)}
    z3_path = shutil.which("z3")
    require(z3_path is not None, "z3 CLI unavailable")

    def cover_smt(bound, values=False):
        lines = ["(set-logic QF_LIA)"]
        lines.extend(f"(declare-fun y{i} () Bool)"
                     for i in range(len(orbit_list)))
        for group in nontrivial_groups:
            choices = []
            for candidate in group:
                atoms = " ".join(f"y{orbit_index[row]}" for row in candidate)
                choices.append(f"(and {atoms})")
            lines.append(f"(assert (or {' '.join(choices)}))")
        weight = " ".join(f"(ite y{i} 1 0)"
                          for i in range(len(orbit_list)))
        lines.append(f"(assert (<= (+ {weight}) {bound}))")
        lines.append("(check-sat)")
        if values:
            lines.append("(get-value (" + " ".join(
                f"y{i}" for i in range(len(orbit_list))) + "))")
        return "\n".join(lines) + "\n"

    optimum = None
    unsat_bounds = []
    for bound in range(len(orbit_list) + 1):
        run = subprocess.run([z3_path, "-in"], input=cover_smt(bound),
                             text=True, capture_output=True, check=True)
        answer = run.stdout.strip().splitlines()[0]
        require(answer in {"sat", "unsat"}, (answer, run.stderr))
        if answer == "sat":
            optimum = bound
            break
        unsat_bounds.append(bound)
    require(optimum is not None, "cover unexpectedly infeasible")
    model_run = subprocess.run([z3_path, "-in"],
                               input=cover_smt(optimum, values=True),
                               text=True, capture_output=True, check=True)
    require(model_run.stdout.startswith("sat\n"), model_run.stdout)
    tokens = model_run.stdout.replace("(", " ").replace(")", " ").split()
    assignments = {tokens[i]: tokens[i + 1] for i in range(1, len(tokens) - 1, 2)
                   if tokens[i].startswith("y")}
    best_cover = {orbit_list[i] for i in range(len(orbit_list))
                  if assignments.get(f"y{i}") == "true"}
    require(len(best_cover) == optimum, (len(best_cover), optimum, assignments))
    require(all(any(candidate <= best_cover for candidate in group)
                for group in nontrivial_groups), "cover witness invalid")

    # Multi-pivot relaxation. Allow arbitrary rational coefficients on all
    # available literal pivots, with their coefficients summing to one. For a
    # proposed global orbit support S, every exact anchor-signature coordinate
    # outside S must cancel. If this is inconsistent, a deletion-minimal set
    # C of zeroed orbit blocks is a valid hitting clause: every feasible S must
    # contain at least one orbit of C. Alternate exact rational core extraction
    # with minimum-cardinality hitting-set solves until every instance passes.
    def instance_consistent(instance, allowed_orbits=None, zero_orbits=None):
        columns, coordinates = instance
        require((allowed_orbits is None) != (zero_orbits is None), "mode")
        rows = [(tuple(1 for _ in columns), 1)]
        for coordinate in coordinates:
            orbit = canonical(coordinate)
            constrained = (orbit not in allowed_orbits
                           if allowed_orbits is not None else orbit in zero_orbits)
            if constrained:
                rows.append((tuple(column[coordinate] for column in columns), 0))
        return exact_consistent(rows, len(columns))

    def hitting_smt(clauses, bound, values=False):
        lines = ["(set-logic QF_LIA)"]
        lines.extend(f"(declare-fun y{i} () Bool)"
                     for i in range(len(orbit_list)))
        for clause in clauses:
            atoms = " ".join(f"y{orbit_index[row]}" for row in clause)
            lines.append(f"(assert (or {atoms}))")
        weight = " ".join(f"(ite y{i} 1 0)"
                          for i in range(len(orbit_list)))
        lines.append(f"(assert (<= (+ {weight}) {bound}))")
        lines.append("(check-sat)")
        if values:
            lines.append("(get-value (" + " ".join(
                f"y{i}" for i in range(len(orbit_list))) + "))")
        return "\n".join(lines) + "\n"

    def solve_hitting(clauses):
        unsat = []
        for bound in range(len(orbit_list) + 1):
            run = subprocess.run([z3_path, "-in"],
                                 input=hitting_smt(clauses, bound), text=True,
                                 capture_output=True, check=True)
            answer = run.stdout.strip().splitlines()[0]
            require(answer in {"sat", "unsat"}, (answer, run.stderr))
            if answer == "unsat":
                unsat.append(bound)
                continue
            model = subprocess.run([z3_path, "-in"],
                                   input=hitting_smt(clauses, bound, values=True),
                                   text=True, capture_output=True, check=True)
            tokens = model.stdout.replace("(", " ").replace(")", " ").split()
            assignments = {tokens[i]: tokens[i + 1]
                           for i in range(1, len(tokens) - 1, 2)
                           if tokens[i].startswith("y")}
            selected = {orbit_list[i] for i in range(len(orbit_list))
                        if assignments.get(f"y{i}") == "true"}
            require(len(selected) == bound, (len(selected), bound))
            return selected, unsat
        raise RuntimeError("hitting set infeasible")

    clauses = set()
    clause_witness = {}
    lazy_iterations = 0
    while True:
        affine_cover, affine_unsat_bounds = solve_hitting(tuple(sorted(clauses,
                                                   key=lambda row: (len(row), tuple(row)))))
        failures = []
        for signature, instance in affine_instances.items():
            if instance_consistent(instance, allowed_orbits=affine_cover):
                continue
            excluded = set(orbit_list) - affine_cover
            core = set(excluded)
            require(not instance_consistent(instance, zero_orbits=core),
                    "failed instance unexpectedly consistent")
            for orbit in sorted(tuple(core)):
                trial = core - {orbit}
                if not instance_consistent(instance, zero_orbits=trial):
                    core = trial
            require(core and not instance_consistent(instance, zero_orbits=core),
                    (signature, core))
            require(all(instance_consistent(instance, zero_orbits=core - {orbit})
                        for orbit in core), (signature, "nonminimal core"))
            failures.append((signature, frozenset(core)))
        if not failures:
            break
        previous = len(clauses)
        for signature, core in failures:
            clauses.add(core)
            clause_witness.setdefault(core, signature)
        require(len(clauses) > previous, "lazy hitting loop made no progress")
        lazy_iterations += 1
        require(lazy_iterations <= 500, lazy_iterations)

    result = {
        "status": "PASS finite equivariant K16 anchor cover audit",
        "source": {
            "K14_signatures": len(k14),
            "K14_factor_stabilizer_orbits": len(representatives),
            "mixed_singleton_rows": len(vectors),
            "exact_K2_tails_per_row": sorted(set(map(len, tails))),
        },
        "affine_signature_test": {
            "K14_orbits_with_complete_signature_level_K16_cancellation": len(zero_affine),
            "K14_orbits_with_signature_level_affine_obstruction": len(affine_obstructed),
            "obstructed_representatives": [str(row) for row in affine_obstructed],
            "exact_minimum_global_tail_orbit_support_in_signature_relaxation": len(
                affine_cover),
            "minimum_affine_cover_orbit_representatives": [str(row) for row in sorted(
                affine_cover)],
            "deletion_minimal_inconsistency_clauses": len(clauses),
            "inconsistency_clause_witnesses": [
                {
                    "K14_signature": str(clause_witness[clause]),
                    "zeroed_tail_orbit_core": [str(row) for row in sorted(clause)],
                }
                for clause in sorted(clauses, key=lambda row: (len(row), tuple(row)))
            ],
            "lazy_hitting_iterations": lazy_iterations,
            "proved_unsat_cardinality_bounds": affine_unsat_bounds,
            "guard": (
                "Exact rational affine incidence on full anchor signatures. "
                "Feasibility is necessary for cancellation after forgetting "
                "nonanchor labels, hence infeasibility and the resulting "
                "minimum support are valid lower bounds; feasibility alone "
                "does not prove literal monomial cancellation."
            ),
        },
        "single_pivot_cover": {
            "candidate_tail_orbits": len(all_tail_orbits),
            "globally_forced_tail_orbits_across_every_single_pivot": len(
                forced_single_pivot_orbits),
            "forced_orbit_representatives": [str(row) for row in sorted(
                forced_single_pivot_orbits)],
            "exact_minimum_global_orbit_union": len(best_cover),
            "minimum_cover_orbit_representatives": [str(row) for row in sorted(
                best_cover)],
            "nontrivial_K14_orbit_groups": len(nontrivial_groups),
            "proved_unsat_cardinality_bounds": unsat_bounds,
            "solver": subprocess.run([z3_path, "-version"], text=True,
                                     capture_output=True, check=True).stdout.strip(),
            "candidate_data": candidate_data,
            "guard": (
                "This finite cover instance keeps all literal pivots and all "
                "twelve exact K2 terms before projecting to anchor-signature "
                "orbits. The finite exhaustive minimum-union calculation is "
                "exact for choosing one literal pivot per K14 signature orbit; "
                "it does not model multi-pivot coefficient cancellation."
            ),
        },
        "pinned": {
            str(K14_PATH.relative_to(ROOT)): sha256(K14_PATH.read_bytes()).hexdigest(),
            str(F.R8P.relative_to(ROOT)): sha256(F.R8P.read_bytes()).hexdigest(),
        },
    }
    return result


def main(write_results=False):
    result = build()
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": logical,
        "source": result["source"],
        "affine_signature_test": {
            key: value for key, value in result["affine_signature_test"].items()
            if key not in {"obstructed_representatives",
                           "inconsistency_clause_witnesses",
                           "minimum_affine_cover_orbit_representatives"}
        },
        "single_pivot_cover": {
            key: value for key, value in result["single_pivot_cover"].items()
            if key not in {"candidate_data", "forced_orbit_representatives"}
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
