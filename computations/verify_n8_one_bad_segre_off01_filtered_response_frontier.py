#!/usr/bin/env python3
"""Audit the filtered-response frontier of the off-01 Segre cocharacter.

The affine q-limit is the optional 24-cell face closed by 4a213d8, but the
two diagonal response targets have word weight three.  After compatible
endpoint shifts, every term in a fixed response word has the same total
grade.  Thus all positive-grade q cells remain as possible
contaminants of the face's literal two-term response rows.

This checker builds one global source-support formula.  It includes all top
and four response fibres, and weakens each ordinary odd-triangle clause by
the exact physical contaminating monomials in its three rows.  It then finds
and verifies the minimum number of positive-grade q cells required by
any support-shadow survivor.  This is an associated-graded frontier, not a
coefficient point or a cardinality census of source supports.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.solvers import Solver


ROOT = Path(__file__).resolve().parents[1]
ANCHOR = ROOT / "computations/verify_n8_one_bad_segre_cube_anchor_initial_cover.py"
ANCHOR_SHA256 = "a0a2f5600029f6c79ce931171b53fff772f2fef7e0c0bb4b971ba56c0fd44ef0"
COCHARACTER = (
    (0, 0, 0),
    (0, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 0, 1),
)
EXPECTED_FORMULA_SHA256 = (
    "c8eba8e4cfb2303f965f6094fec67417113db6e4558760d9a437853730d619f6"
)
EXPECTED_BOUND_FORMULA_SHA256 = (
    "1688d15a9fc8597c96b3c41726b7396cc0ae8c6bdf7b15927f89cc52dca740a2"
)
EXPECTED_BOUND_PROOF_SHA256 = (
    "f8a416b6dd65b335f55d66a54c86a7ae7eb18cf18bbb791728e04246acf0569a"
)
EXPECTED_LEDGER_SHA256 = (
    "0428b66afaa140021ab8db49d8ace6dd7b872940e6857fdba96243e804894b2c"
)
EXPECTED_SKIP_LEDGER_SHA256 = (
    "9a9921431b7f8c0066f35fd3c22b897eed71c3d33b1cbacccdfcc216e79faed1"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_anchor():
    actual = sha256(ANCHOR.read_bytes()).hexdigest()
    require(actual == ANCHOR_SHA256, f"anchor dependency changed: {actual}")
    spec = spec_from_file_location("anchor", ANCHOR)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(skip_rup=False):
    anchor = load_anchor()
    four = anchor.load_dependency()
    one = four.load_dependency()
    first = one.load_dependency()
    diagonal = first.load_dependency()
    pure = diagonal.load_dependency()
    source = pure.load_dependency()
    support_h, _weights_h = pure.build_top_null_H(source)

    face_labels = tuple(sorted(anchor.LARGE_ZERO_CLASS))
    face_by_cell = {anchor.parse_cell(label): label for label in face_labels}
    grade_zero_diagonal_cells = tuple(sorted(
        (edge, (colour, colour))
        for edge in anchor.EDGES for colour in anchor.COLOURS
        if (edge, (colour, colour)) not in support_h
        and anchor.weight((edge, (colour, colour)), COCHARACTER) == 0
    ))
    grade_zero_diagonal_labels = tuple(
        anchor.cell_label(cell) for cell in grade_zero_diagonal_cells
    )
    grade_zero_diagonal_by_cell = dict(zip(
        grade_zero_diagonal_cells, grade_zero_diagonal_labels, strict=True
    ))
    high_cells = tuple(sorted(
        (edge, colours)
        for edge in anchor.EDGES
        for colours in itertools.product(anchor.COLOURS, repeat=2)
        if (edge, colours) not in support_h
        and (edge, colours) not in face_by_cell
        and anchor.weight((edge, colours), COCHARACTER) > 0
    ))
    require(len(grade_zero_diagonal_cells) == 21,
            "the grade-zero diagonal universe changed")
    require(len(high_cells) == 76, "the positive-grade q universe changed")
    high_labels = tuple(anchor.cell_label(cell) for cell in high_cells)
    high_by_cell = dict(zip(high_cells, high_labels, strict=True))
    high_grade_histogram = Counter(anchor.weight(cell, COCHARACTER)
                                   for cell in high_cells)
    require(high_grade_histogram == Counter({1: 62, 2: 14}),
            f"the positive q grades changed: {high_grade_histogram}")

    variables = {}
    next_variable = 1
    for label in grade_zero_diagonal_labels:
        variables[("diag", label)] = next_variable
        next_variable += 1
    for label in face_labels:
        variables[("face", label)] = next_variable
        next_variable += 1
    for label in high_labels:
        variables[("high", label)] = next_variable
        next_variable += 1
    for star in ("p1", "p2", "s1", "s2"):
        for site in anchor.SITES:
            variables[("star", star, site)] = next_variable
            next_variable += 1

    clauses = []
    conjunction_cache = {}

    def conjunction(required):
        nonlocal next_variable
        required = tuple(sorted(set(required)))
        if not required:
            return 0
        if required in conjunction_cache:
            return conjunction_cache[required]
        if len(required) == 1:
            return required[0]
        result = next_variable
        next_variable += 1
        conjunction_cache[required] = result
        for literal in required:
            clauses.append([-result, literal])
        clauses.append([result] + [-literal for literal in required])
        return result

    def q_literal(cell, include_positive_mixed=True):
        if cell in support_h:
            return 0
        if cell in face_by_cell:
            return variables[("face", face_by_cell[cell])]
        if cell in high_by_cell:
            if cell[1][0] == cell[1][1] or include_positive_mixed:
                return variables[("high", high_by_cell[cell])]
            return None
        if cell in grade_zero_diagonal_by_cell:
            return variables[("diag", grade_zero_diagonal_by_cell[cell])]
        return None

    def zero_or_at_least_two(monomials):
        constant_count = monomials.count(0)
        live = [monomial for monomial in monomials if monomial]
        if constant_count >= 2:
            return
        if constant_count == 1:
            clauses.append(live)
            return
        for index, monomial in enumerate(live):
            clauses.append([-monomial] + live[:index] + live[index + 1:])

    # Complete source-support shadow with all q grades present.
    for word in itertools.product(anchor.COLOURS, repeat=6):
        monomials = []
        for matching in anchor.MATCHINGS:
            required = []
            for edge in matching:
                literal = q_literal((edge, (word[edge[0]], word[edge[1]])))
                if literal is None:
                    break
                if literal:
                    required.append(literal)
            else:
                monomials.append(conjunction(required))
        if word == (0,) * 6:
            clauses.append([m for m in monomials if m]
                           if 0 not in monomials else [1, -1])
        else:
            zero_or_at_least_two(monomials)

    response_data = (
        ("p1", "s1", (1,) * 6),
        ("p1", "s2", None),
        ("p2", "s1", None),
        ("p2", "s2", (2,) * 6),
    )
    for p_star, s_star, target in response_data:
        p_colour, s_colour = int(p_star[1]), int(s_star[1])
        for word in itertools.product(anchor.COLOURS, repeat=6):
            monomials = []
            for p_site in anchor.SITES:
                if word[p_site] != p_colour:
                    continue
                for s_site in anchor.SITES:
                    if s_site == p_site or word[s_site] != s_colour:
                        continue
                    residual = tuple(site for site in anchor.SITES
                                     if site not in (p_site, s_site))
                    for matching in anchor.perfect_matchings(residual):
                        required = [variables[("star", p_star, p_site)],
                                    variables[("star", s_star, s_site)]]
                        for edge in matching:
                            literal = q_literal(
                                (edge, (word[edge[0]], word[edge[1]]))
                            )
                            if literal is None:
                                break
                            if literal:
                                required.append(literal)
                        else:
                            monomials.append(conjunction(required))
            if target is not None and word == target:
                clauses.append([m for m in monomials if m]
                               if 0 not in monomials else [1, -1])
            else:
                zero_or_at_least_two(monomials)

    pre_circuit_clause_count = len(clauses)

    # Reconstruct every literal two-term row in the grade-zero face universe.
    # In the full filtered universe its additional physical terms are the
    # exact contaminants which weaken the odd-triangle clause.
    row_witnesses = {}
    for p_star, s_star in (("p1", "s1"), ("p2", "s2")):
        colour = int(p_star[1])
        per_edge = {edge: [] for edge in itertools.combinations(anchor.SITES, 2)}
        for word in itertools.product(anchor.COLOURS, repeat=6):
            base_terms = []
            full_terms = []
            for p_site in anchor.SITES:
                if word[p_site] != colour:
                    continue
                for s_site in anchor.SITES:
                    if s_site == p_site or word[s_site] != colour:
                        continue
                    residual = tuple(site for site in anchor.SITES
                                     if site not in (p_site, s_site))
                    for matching in anchor.perfect_matchings(residual):
                        q_cells = tuple(sorted(
                            (edge, (word[edge[0]], word[edge[1]]))
                            for edge in matching
                        ))
                        full_required = [variables[("star", p_star, p_site)],
                                         variables[("star", s_star, s_site)]]
                        base_required = []
                        base_allowed = True
                        for cell in q_cells:
                            full_literal = q_literal(cell)
                            require(full_literal is not None,
                                    "the full q universe lost a physical cell")
                            if full_literal:
                                full_required.append(full_literal)
                            base_literal = q_literal(
                                cell, include_positive_mixed=False
                            )
                            if base_literal is None:
                                base_allowed = False
                            elif base_literal:
                                base_required.append(base_literal)
                        full_terms.append((p_site, s_site, q_cells,
                                           conjunction(full_required)))
                        if base_allowed:
                            base_terms.append((p_site, s_site, q_cells,
                                               tuple(sorted(set(base_required)))))
            if len(base_terms) != 2:
                continue
            left, right = base_terms
            if ((left[0], left[1]) != (right[1], right[0])
                    or left[2] != right[2] or left[3] != right[3]):
                continue
            pair = tuple(sorted((left[0], left[1])))
            selected = {(left[0], left[1], left[2]),
                        (right[0], right[1], right[2])}
            contaminants = tuple(sorted(
                term_var for p_site, s_site, q_cells, term_var in full_terms
                if (p_site, s_site, q_cells) not in selected
            ))
            require(contaminants,
                    "a face binomial unexpectedly stayed universal")
            per_edge[pair].append({
                "q_required": left[3],
                "contaminants": contaminants,
                "word": word,
            })
        require(all(per_edge.values()),
                f"the filtered {p_star}/{s_star} witness graph changed")
        row_witnesses[(p_star, s_star)] = per_edge

    conditional_odd_clauses = 0
    for (p_star, s_star), per_edge in row_witnesses.items():
        for triangle in itertools.combinations(anchor.SITES, 3):
            edges = tuple(itertools.combinations(triangle, 2))
            star_antecedent = {
                variables[("star", star, site)]
                for star in (p_star, s_star) for site in triangle
            }
            for witnesses in itertools.product(*(per_edge[edge]
                                                  for edge in edges)):
                antecedent = set(star_antecedent)
                contaminants = set()
                for witness in witnesses:
                    antecedent.update(witness["q_required"])
                    contaminants.update(witness["contaminants"])
                clauses.append([-literal for literal in sorted(antecedent)]
                               + sorted(contaminants))
                conditional_odd_clauses += 1

    variable_count = next_variable - 1
    high_variables = [variables[("high", label)] for label in high_labels]

    # One weighted MaxSAT problem finds the global minimum number of live
    # positive-grade q cells.  A separate cardinality-bounded SAT query then
    # certifies the strict lower bound.
    weighted = WCNF()
    for clause in clauses:
        weighted.append(clause)
    for variable in high_variables:
        weighted.append([-variable], weight=1)
    with RC2(weighted, solver="cadical195") as optimizer:
        model = optimizer.compute()
        minimum_high = optimizer.cost
    require(model is not None, "the filtered support formula is UNSAT")
    positive_model = frozenset(literal for literal in model if literal > 0)
    live_high = tuple(label for label in high_labels
                      if variables[("high", label)] in positive_model)
    require(len(live_high) == minimum_high,
            "the MaxSAT model cost does not match its live high cells")
    print("minimum positive-grade q cells (MaxSAT):", minimum_high,
          ",".join(live_high), flush=True)
    with Solver(name="cadical195", bootstrap_with=clauses) as verifier:
        require(verifier.solve(assumptions=[literal if literal in positive_model
                                           else -literal
                                           for literal in range(1, variable_count + 1)]),
                "the frozen filtered support assignment is not a model")

    # The actual decorated weighted site stabilizer of H is trivial.  Hence
    # the exact minimum-support census below is already its orbit census.
    def transform_cell(cell, permutation):
        (left, right), (left_colour, right_colour) = cell
        image_left, image_right = permutation[left], permutation[right]
        if image_left < image_right:
            return ((image_left, image_right), (left_colour, right_colour))
        return ((image_right, image_left), (right_colour, left_colour))

    weighted_stabilizer = []
    for permutation in itertools.permutations(anchor.SITES):
        transformed = {transform_cell(cell, permutation) for cell in support_h}
        if transformed != set(support_h):
            continue
        if all(_weights_h[transform_cell(cell, permutation)] == coefficient
               for cell, coefficient in _weights_h.items()):
            weighted_stabilizer.append(permutation)
    require(weighted_stabilizer == [anchor.SITES],
            f"the weighted H stabilizer changed: {weighted_stabilizer}")

    minimum_bound = CardEnc.atmost(
        lits=high_variables, bound=minimum_high, top_id=variable_count,
        encoding=EncType.totalizer,
    )
    feasible_supports = []
    support_models = []
    with Solver(name="cadical195",
                bootstrap_with=clauses + minimum_bound.clauses) as census:
        while census.solve():
            support_positive = frozenset(
                literal for literal in census.get_model() if literal > 0
            )
            live_variables = tuple(variable for variable in high_variables
                                   if variable in support_positive)
            require(len(live_variables) == minimum_high,
                    "a minimum-census model has the wrong support size")
            live_support = tuple(high_labels[high_variables.index(variable)]
                                 for variable in live_variables)
            feasible_supports.append(live_support)
            support_models.append({
                "high": live_support,
                "face": tuple(label for label in face_labels
                              if variables[("face", label)]
                              in support_positive),
                "diagonal": tuple(label for label
                                  in grade_zero_diagonal_labels
                                  if variables[("diag", label)]
                                  in support_positive),
                "stars": tuple(
                    f"{star}:{site}"
                    for star in ("p1", "p2", "s1", "s2")
                    for site in anchor.SITES
                    if variables[("star", star, site)] in support_positive
                ),
            })
            census.add_clause([-variable for variable in live_variables])
            if len(feasible_supports) % 100 == 0:
                print("minimum-support census:", len(feasible_supports),
                      flush=True)
    require(feasible_supports,
            "the minimum filtered support census became empty")
    ordered = sorted(zip(feasible_supports, support_models, strict=True))
    feasible_supports = [support for support, _model in ordered]
    support_models = [model for _support, model in ordered]
    support_payload = json.dumps(feasible_supports, separators=(",", ":"))
    support_digest = sha256(support_payload.encode()).hexdigest()
    support_model_payload = json.dumps(support_models, separators=(",", ":"))
    support_model_digest = sha256(support_model_payload.encode()).hexdigest()

    lower_bound = CardEnc.atmost(
        lits=high_variables,
        bound=minimum_high - 1,
        top_id=variable_count,
        encoding=EncType.totalizer,
    )
    bounded_clauses = clauses + lower_bound.clauses
    bound_payload = json.dumps(
        {"variables": lower_bound.nv, "clauses": bounded_clauses},
        separators=(",", ":"),
    )
    bound_digest = sha256(bound_payload.encode()).hexdigest()
    with Solver(name="glucose42", bootstrap_with=bounded_clauses,
                with_proof=True) as solver:
        require(not solver.solve(),
                "a filtered survivor exists below the claimed minimum")
        proof = solver.get_proof() or []
    additions = tuple(line for line in proof if not line.startswith("d "))
    parsed_proof = []
    for index, line in enumerate(additions):
        numbers = tuple(map(int, line.split()))
        require(numbers and numbers[-1] == 0 and 0 not in numbers[:-1],
                f"malformed lower-bound proof addition {index}")
        parsed_proof.append(numbers[:-1])
    require(parsed_proof and parsed_proof[-1] == (),
            "the lower-bound proof does not end in empty")
    proof_payload = "\n".join(additions) + "\n"
    proof_digest = sha256(proof_payload.encode()).hexdigest()
    print("lower-bound proof generated:", len(parsed_proof),
          "additions;", proof_digest, flush=True)
    print("minimum-support orbits (trivial weighted H stabilizer):",
          len(feasible_supports), support_digest, flush=True)
    print("minimum-support list:", support_payload, flush=True)
    print("minimum-support models:", support_model_payload, flush=True)
    if not skip_rup:
        with Solver(name="cadical195", bootstrap_with=bounded_clauses) as verifier:
            for index, clause in enumerate(parsed_proof):
                consistent, _propagated = verifier.propagate(
                    assumptions=[-literal for literal in clause]
                )
                require(not consistent,
                        f"lower-bound proof addition {index} is not RUP")
                verifier.add_clause(list(clause))
                if (index + 1) % 10000 == 0:
                    print("independent RUP replay:", index + 1, "/",
                          len(parsed_proof), flush=True)

    face_live = tuple(label for label in face_labels
                      if variables[("face", label)] in positive_model)
    diagonal_live = tuple(label for label in grade_zero_diagonal_labels
                          if variables[("diag", label)] in positive_model)
    star_live = tuple(
        f"{star}:{site}" for star in ("p1", "p2", "s1", "s2")
        for site in anchor.SITES
        if variables[("star", star, site)] in positive_model
    )

    formula_payload = json.dumps(
        {"variables": variable_count, "clauses": clauses},
        separators=(",", ":"),
    )
    formula_digest = sha256(formula_payload.encode()).hexdigest()
    if EXPECTED_FORMULA_SHA256 != "TO_BE_FILLED":
        require(formula_digest == EXPECTED_FORMULA_SHA256,
                f"the filtered formula changed: {formula_digest}")
    if EXPECTED_BOUND_FORMULA_SHA256 != "TO_BE_FILLED":
        require(bound_digest == EXPECTED_BOUND_FORMULA_SHA256,
                f"the strict lower-bound formula changed: {bound_digest}")
    if EXPECTED_BOUND_PROOF_SHA256 != "TO_BE_FILLED":
        require(proof_digest == EXPECTED_BOUND_PROOF_SHA256,
                f"the strict lower-bound proof changed: {proof_digest}")
    ledger = {
        "dependency": {"path": str(ANCHOR.relative_to(ROOT)),
                       "sha256": ANCHOR_SHA256},
        "cocharacter": COCHARACTER,
        "q_grade_histogram": {"0_fixed_H": len(support_h),
                              "0_optional_face": len(face_labels),
                              "0_optional_diagonal": len(
                                  grade_zero_diagonal_labels),
                              "positive_q": dict(high_grade_histogram)},
        "pure_word_weights": [sum(COCHARACTER[site][colour]
                                  for site in anchor.SITES)
                              for colour in anchor.COLOURS],
        "compatible_diagonal_star_shifts": "a_i+b_i=-3 for i=1,2",
        "pre_circuit_clauses": pre_circuit_clause_count,
        "conditional_odd_clauses": conditional_odd_clauses,
        "cnf_variables": variable_count,
        "cnf_clauses": len(clauses),
        "formula_sha256": formula_digest,
        "minimum_positive_grade_q_cells": minimum_high,
        "weighted_H_site_stabilizer_order": len(weighted_stabilizer),
        "minimum_support_orbits": feasible_supports,
        "minimum_support_orbits_sha256": support_digest,
        "minimum_support_models": support_models,
        "minimum_support_models_sha256": support_model_digest,
        "minimum_strict_lower_bound": {
            "variables": lower_bound.nv,
            "clauses": len(bounded_clauses),
            "formula_sha256": bound_digest,
            "proof_additions": len(parsed_proof),
            "proof_sha256": proof_digest,
            "independent_RUP_replay": not skip_rup,
        },
        "survivor": {"positive_grade_q": live_high,
                     "grade_zero_face": face_live,
                     "diagonal": diagonal_live,
                     "stars": star_live},
        "scope": (
            "exact source-support frontier for the filtered response system; "
            "SAT is not a coefficient point; the strict lower-bound UNSAT "
            "has a deletion-free independently replayed RUP certificate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    expected_ledger = (EXPECTED_SKIP_LEDGER_SHA256 if skip_rup
                       else EXPECTED_LEDGER_SHA256)
    if expected_ledger != "TO_BE_FILLED":
        require(digest == expected_ledger,
                f"the filtered-response ledger changed: {digest}")
    print("N=8 off-01 filtered-response frontier: PASS")
    print("q positive grades:", dict(high_grade_histogram))
    print("CNF:", variable_count, "variables;", len(clauses), "clauses")
    print("conditional odd clauses:", conditional_odd_clauses)
    print("minimum-support orbits:", len(feasible_supports))
    print("minimum-support orbit sha256:", support_digest)
    print("minimum-support model sha256:", support_model_digest)
    print("minimum positive-grade q cells:", minimum_high)
    print("live high cells:", ",".join(live_high))
    print("live face cells:", ",".join(face_live))
    print("live diagonal cells:", ",".join(diagonal_live))
    print("live stars:", ",".join(star_live))
    print("formula sha256:", formula_digest)
    print("bound formula sha256:", bound_digest)
    print("bound proof:", len(parsed_proof), "RUP additions")
    print("bound proof sha256:", proof_digest)
    print("ledger sha256:", digest)
    return support_models


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-rup", action="store_true",
                        help="exploratory only: skip the slow independent replay")
    arguments = parser.parse_args()
    main(skip_rup=arguments.skip_rup)
