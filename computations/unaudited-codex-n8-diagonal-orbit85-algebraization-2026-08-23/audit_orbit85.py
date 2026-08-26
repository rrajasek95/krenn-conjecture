#!/usr/bin/env python3
"""Bounded algebraization audit of the shortest N8-DIAGONAL DRAT proof.

The script rebuilds orbit 85 from the certified encoder, counts the exact
clause-polynomial and source-faithful selector/Rabinowitsch interfaces, asks
drat-trim to reject all non-RUP additions, emits a core LRAT in a temporary
directory, and reconstructs its ordered RUP resolution chains.  It performs
no polynomial solve.
"""

from __future__ import annotations

import collections
import importlib.util
import json
import math
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "computations/certificates/n8_diagonal/orbits"
DRAT_TRIM = (ROOT / "computations/unaudited-hygiene-h1-2026-08-15/tools/"
             "drat-trim/drat-trim")
ORBIT = 85


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def load_certified_encoder():
    path = ROOT / "computations/verify_eight_site_diagonal_obstruction.py"
    spec = importlib.util.spec_from_file_location("n8diag_certified", path)
    require(spec is not None and spec.loader is not None, "cannot load encoder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = None
    clauses = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("c"):
            continue
        if line.startswith("p cnf "):
            _, _, raw_variables, raw_clauses = line.split()
            variables = int(raw_variables)
            expected = int(raw_clauses)
            continue
        words = [int(word) for word in line.split()]
        require(words[-1] == 0, "unterminated DIMACS clause")
        clauses.append(tuple(words[:-1]))
    require(variables is not None, "missing DIMACS header")
    require(len(clauses) == expected, "DIMACS clause count mismatch")
    return variables, clauses


def parse_lrat(path: Path):
    additions = []
    deletions = 0
    for line in path.read_text(encoding="ascii").splitlines():
        words = line.split()
        if not words:
            continue
        clause_id = int(words[0])
        if words[1] == "d":
            require(words[-1] == "0", "unterminated LRAT deletion")
            deletions += 1
            continue
        first_zero = words.index("0", 1)
        require(words[-1] == "0", "unterminated LRAT hints")
        literals = tuple(map(int, words[1:first_zero]))
        hints = tuple(map(int, words[first_zero + 1:-1]))
        require(all(hint > 0 for hint in hints),
                "RAT/negative LRAT hint found in claimed RUP core")
        additions.append((clause_id, literals, hints))
    return additions, deletions


def extract_resolution_profile(
        input_clauses: list[tuple[int, ...]], additions):
    """Replay ordered RUP and reverse it to ordinary resolution chains."""
    database = {index + 1: clause for index, clause in enumerate(input_clauses)}
    resolution_steps = 0
    skipped_propagations = 0
    weakenings = 0
    max_intermediate_width = 0

    for added_id, target, hints in additions:
        assignment: dict[int, bool] = {}
        reasons: list[tuple[int, int]] = []
        conflict = None

        # Assume the negation of the candidate clause.
        for literal in target:
            variable = abs(literal)
            value = literal < 0
            require(variable not in assignment or assignment[variable] == value,
                    f"tautological LRAT target {added_id}")
            assignment[variable] = value

        for hint in hints:
            require(hint in database, f"unknown LRAT hint {hint}")
            clause = database[hint]
            unassigned = []
            satisfied = False
            for literal in clause:
                variable = abs(literal)
                if variable not in assignment:
                    unassigned.append(literal)
                elif assignment[variable] == (literal > 0):
                    satisfied = True
                    break
            require(not satisfied,
                    f"LRAT hint {hint} is satisfied while deriving {added_id}")
            if not unassigned:
                conflict = clause
                break
            require(len(unassigned) == 1,
                    f"LRAT hint {hint} is not unit while deriving {added_id}")
            unit = unassigned[0]
            assignment[abs(unit)] = unit > 0
            reasons.append((unit, hint))
        require(conflict is not None, f"no RUP conflict for lemma {added_id}")

        # Reverse unit propagation.  Each used reason resolves away one unit.
        current = set(conflict)
        require(not any(-literal in current for literal in current),
                "tautological conflict clause")
        for unit, reason_id in reversed(reasons):
            if -unit not in current:
                skipped_propagations += 1
                continue
            reason = set(database[reason_id])
            require(unit in reason, "unit is absent from its reason")
            current.remove(-unit)
            reason.remove(unit)
            current.update(reason)
            require(not any(-literal in current for literal in current),
                    f"tautological reconstructed resolvent for {added_id}")
            resolution_steps += 1
            max_intermediate_width = max(max_intermediate_width, len(current))

        target_set = set(target)
        require(current.issubset(target_set),
                f"RUP chain does not derive a subclause of lemma {added_id}")
        if current != target_set:
            weakenings += 1
        database[added_id] = target

    require(additions[-1][1] == (), "LRAT core does not finish with empty clause")
    return {
        "resolution_steps": resolution_steps,
        "skipped_unit_propagations": skipped_propagations,
        "weakening_steps": weakenings,
        "max_intermediate_clause_width": max_intermediate_width,
        # For the standard clause-polynomial resolution identity, a resolvent
        # of width w is obtained from products of degree at most w+1.
        "pc_degree_upper_bound": max_intermediate_width + 1,
    }


def main() -> None:
    module = load_certified_encoder()
    reps = module.orbit_reps(8)
    case, orbit_size = reps[ORBIT]
    encoder = module.Enc(8, case, k=4).build()
    cnf_path = CERT / f"n8k4_{ORBIT}.cnf"
    drat_path = CERT / f"n8k4_{ORBIT}.drat"
    require(encoder.dimacs().encode("ascii") == cnf_path.read_bytes(),
            "certified encoder does not rebuild orbit-85 CNF byte-for-byte")

    # Confirm that orbit 85 is smallest by both nonempty lines and bytes.
    proof_sizes = []
    for path in CERT.glob("n8k4_*.drat"):
        nonempty = sum(bool(line.strip()) for line in path.open("rb"))
        proof_sizes.append((nonempty, path.stat().st_size,
                            int(path.stem.rsplit("_", 1)[1])))
    require(min(proof_sizes) == (1076, 11291, ORBIT),
            f"orbit 85 is no longer the smallest proof: {min(proof_sizes)}")

    variables, clauses = parse_cnf(cnf_path)
    require(variables == encoder.nv == 5592, "Boolean variable count changed")
    require(clauses == encoder.cls, "parsed and rebuilt clauses differ")

    widths = collections.Counter(map(len, clauses))
    positive_counts = collections.Counter(
        sum(literal > 0 for literal in clause) for clause in clauses)
    family_counts = collections.Counter(tag[0] for tag in encoder.tags)
    p_size_counts = collections.Counter(
        key[2].bit_count() for key in encoder.vmap if key[0] == "p")
    p_atoms = sum(p_size_counts.values())
    g_atoms = sum(key[0] == "g" for key in encoder.vmap)
    require((p_atoms, g_atoms) == (384, 5208), "p/g atom census changed")

    # A clause C maps to prod_{positive x in C}(1-x) *
    # prod_{negative -x in C}x.  Its expanded support has exactly 2^#positive
    # monomials because the variables within a clause are distinct.
    clause_monomial_occurrences = sum(
        2 ** sum(literal > 0 for literal in clause) for clause in clauses)

    # There are 84 diagonal source weights.  Each p_h gets one inverse u_h and
    # two link equations: (1-p)h=0 and p(h*u-1)=0.  A size-s hafnian contains
    # (s-1)!! matching monomials (with the empty hafnian containing one).
    hafnian_terms = {0: 1, 2: 1, 4: 3, 6: 15, 8: 105}
    total_hafnian_terms = sum(
        count * hafnian_terms[size] for size, count in p_size_counts.items())
    link_monomial_occurrences = 3 * total_hafnian_terms + p_atoms
    require(total_hafnian_terms == 2292, "hafnian support census changed")
    require(link_monomial_occurrences == 7260, "link support census changed")

    require(DRAT_TRIM.is_file(), f"missing frozen drat-trim: {DRAT_TRIM}")
    with tempfile.TemporaryDirectory(prefix="n8diag85-") as temporary:
        lrat_path = Path(temporary) / "core.lrat"
        proc = subprocess.run(
            [str(DRAT_TRIM), str(cnf_path), str(drat_path), "-U", "-L",
             str(lrat_path)],
            text=True, capture_output=True, timeout=30, check=False)
        transcript = proc.stdout + proc.stderr
        require(proc.returncode == 0 and "s VERIFIED" in transcript,
                f"RUP-only replay failed:\n{transcript}")
        require("0 RAT lemmas in core" in transcript,
                f"RAT lemma entered core:\n{transcript}")
        additions, deletions = parse_lrat(lrat_path)

    require(len(additions) == 41 and deletions == 40,
            f"unexpected LRAT core shape: {len(additions)} additions, "
            f"{deletions} deletions")
    require(sum(len(hints) for _, _, hints in additions) == 1731,
            "LRAT hint count changed")
    resolution = extract_resolution_profile(clauses, additions)
    require(resolution == {
        "resolution_steps": 1652,
        "skipped_unit_propagations": 38,
        "weakening_steps": 5,
        "max_intermediate_clause_width": 45,
        "pc_degree_upper_bound": 46,
    }, f"resolution profile changed: {resolution}")

    boolean_axiom_monomials = 2 * variables
    result = {
        "verdict": "BOOLEAN_PC_CONVERSION_FEASIBLE_SOURCE_LIFT_NOT_OBTAINED",
        "orbit": ORBIT,
        "case": case,
        "case_orbit_size": orbit_size,
        "shortest_drat": {"nonempty_lines": 1076, "bytes": 11291},
        "cnf": {
            "boolean_variables": variables,
            "p_atoms": p_atoms,
            "g_atoms": g_atoms,
            "clauses": len(clauses),
            "clause_width_histogram": dict(sorted(widths.items())),
            "positive_literal_histogram": dict(sorted(positive_counts.items())),
            "family_counts": dict(sorted(family_counts.items())),
            "max_clause_polynomial_degree": max(widths),
            "expanded_clause_monomial_occurrences": clause_monomial_occurrences,
        },
        "source_faithful_extended_ring": {
            "diagonal_source_variables": 84,
            "boolean_selector_variables": variables,
            "hafnian_inverse_variables": p_atoms,
            "total_variables": 84 + variables + p_atoms,
            "clause_equations": len(clauses),
            "boolean_axioms": variables,
            "selector_hafnian_link_equations": 2 * p_atoms,
            "total_equations": len(clauses) + variables + 2 * p_atoms,
            "p_atom_subset_size_histogram": dict(sorted(p_size_counts.items())),
            "hafnian_monomial_occurrences": total_hafnian_terms,
            "link_monomial_occurrences": link_monomial_occurrences,
            "boolean_axiom_monomial_occurrences": boolean_axiom_monomials,
            "total_expanded_monomial_occurrences": (
                clause_monomial_occurrences + boolean_axiom_monomials
                + link_monomial_occurrences),
            "max_input_degree": max(max(widths), 6),
        },
        "rup_core": {
            "lrat_additions": len(additions),
            "lrat_deletions": deletions,
            "lrat_hints": sum(len(hints) for _, _, hints in additions),
            **resolution,
            "all_core_lemmas_rup": True,
        },
        "static_source_nullstellensatz": False,
        "remaining_barrier": (
            "compile each support clause from literal amplitude/hafnian rows, "
            "then eliminate selectors and inverses; DRAT supplies neither"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
