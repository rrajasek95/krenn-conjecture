#!/usr/bin/env python3
"""Replay all frozen artifacts for the W3 x W3 ten-source lower bound."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
COMPUTATIONS = HERE.parent
sys.path.insert(0, str(COMPUTATIONS))

from verify_drup_certificate import verify as verify_drup  # noqa: E402
from search_w3w3_support import build_formula, dimacs_bytes  # noqa: E402
from w3w3_support_core import (  # noqa: E402
    MATCHINGS,
    OCCURRENCES,
    PYTHEUS_TEN_SOURCE_SOLUTION,
    SOURCES,
    TARGET_WORDS,
    WORDS,
    audit_occurrence_support,
    audit_target_cover,
)


RESULT9 = HERE / "results_target_cover9_certified.json"
RESULT10 = HERE / "results_support10.json"
CNF9 = HERE / "w3w3_target_cover9.cnf"
PROOF9 = HERE / "w3w3_target_cover9.drup"


def require(condition: bool, detail) -> None:
    if not condition:
        raise RuntimeError(detail)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_inventory() -> None:
    require(len(SOURCES) == 60, len(SOURCES))
    require(len(MATCHINGS) == 15, len(MATCHINGS))
    require(len(WORDS) == 64, len(WORDS))
    require(len(TARGET_WORDS) == 9, len(TARGET_WORDS))
    for word in WORDS:
        require(len(OCCURRENCES[word]) == len(MATCHINGS), word)
        for matching, occurrence in zip(
            MATCHINGS, OCCURRENCES[word], strict=True
        ):
            require(len(occurrence) == 3, occurrence)
            reconstructed = [None] * 6
            for (u, v), source in zip(matching, occurrence, strict=True):
                require(source[:2] == (u, v), (matching, occurrence))
                reconstructed[u], reconstructed[v] = source[2:]
            require(tuple(reconstructed) == word, (word, reconstructed))


def audit_frozen_formula(payload9) -> None:
    formula, _pool, _sources, _occurrences = build_formula(
        9, forbid_singletons=False
    )
    raw = dimacs_bytes(formula)
    require(raw == CNF9.read_bytes(), "frozen CNF differs from rebuilt CNF")
    require(hashlib.sha256(raw).hexdigest() == payload9["cnf_sha256"], payload9)
    require(sha256(PROOF9) == payload9["proof_sha256"], payload9)


def audit_solver_boundary() -> None:
    formula9, _pool9, _sources9, _occurrences9 = build_formula(
        9, forbid_singletons=False
    )
    formula10, _pool10, source_variables10, _occurrences10 = build_formula(
        10, forbid_singletons=False
    )
    with Solver(name="cadical195", bootstrap_with=formula9.clauses) as solver:
        require(not solver.solve(), "independent CaDiCaL run found <=9 cover")
    with Solver(name="cadical195", bootstrap_with=formula10.clauses) as solver:
        require(solver.solve(), "independent CaDiCaL run missed 10 cover")
        positive = {literal for literal in solver.get_model() if literal > 0}
    support = tuple(
        source
        for source, variable in source_variables10.items()
        if variable in positive
    )
    audit_target_cover(support, 10)


def main() -> None:
    payload9 = json.loads(RESULT9.read_text(encoding="utf-8"))
    payload10 = json.loads(RESULT10.read_text(encoding="utf-8"))
    require(payload9["status"] == "unsat", payload9)
    require(payload9["schema"] == "w3w3-target-cover-v1", payload9)
    require(payload9["maximum_sources"] == 9, payload9)
    require(payload10["status"] == "sat", payload10)
    require(payload10["maximum_sources"] == 10, payload10)

    audit_inventory()
    audit_frozen_formula(payload9)
    baseline = audit_occurrence_support(PYTHEUS_TEN_SOURCE_SOLUTION, 10)
    require(baseline["forbidden_nonzero_words"] == [], baseline)
    require(set(baseline["target_multiplicities"].values()) == {1}, baseline)
    audit_occurrence_support(payload10["audited_model"]["support"], 10)
    audit_solver_boundary()
    verify_drup(CNF9, PROOF9, solver_name="cadical195")
    print("PASS W3 x W3: no <=9-source target cover; exact 10-source support exists")


if __name__ == "__main__":
    main()
