#!/usr/bin/env python3
"""Close the 24-cell Segre leading face by universal odd-star circuits.

The checker builds a necessary Boolean support shadow for every coefficient
of q^[3]=X0 and the four one-bad responses.  It then reconstructs universal
two-term response rows and adds the ordinary odd-triangle circuit clauses.
A generated deletion-free DRUP proof is replayed by reverse unit propagation.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path

from pysat.solvers import Solver


ROOT = Path(__file__).resolve().parents[1]
ANCHOR = ROOT / "computations/verify_n8_one_bad_segre_cube_anchor_initial_cover.py"
ANCHOR_SHA256 = "a0a2f5600029f6c79ce931171b53fff772f2fef7e0c0bb4b971ba56c0fd44ef0"
EXPECTED_FORMULA_SHA256 = (
    "779e7df5f8060a570c7671cf03f391c50c73439d465d67e0ca71d0a12e842d07"
)
EXPECTED_PROOF_SHA256 = (
    "ea3237a755bceca5adb0b28208607508be120653369a1ab6e16f324f07cd1a9e"
)
EXPECTED_LEDGER_SHA256 = (
    "bdc82c6acf94a372b2890e30b0212a31ea1415367899c296ec5da07f63712365"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_anchor():
    actual = sha256(ANCHOR.read_bytes()).hexdigest()
    require(actual == ANCHOR_SHA256,
            f"anchor dependency changed: {actual}")
    spec = spec_from_file_location("anchor", ANCHOR)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    anchor = load_anchor()
    four = anchor.load_dependency()
    one = four.load_dependency()
    first = one.load_dependency()
    diagonal = first.load_dependency()
    pure = diagonal.load_dependency()
    source = pure.load_dependency()
    support_h, _weights_h = pure.build_top_null_H(source)
    fixed = set(support_h) | {
        anchor.parse_cell(label) for label in anchor.LARGE_ZERO_CLASS
    }

    variables = {}
    next_variable = 1
    for edge in anchor.EDGES:
        for colour in range(3):
            variables[("q", edge, colour)] = next_variable
            next_variable += 1
    for star in ("p1", "p2", "s1", "s2"):
        for site in range(6):
            variables[(star, site)] = next_variable
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

    def q_literal(cell):
        if cell in fixed:
            return 0
        edge, colours = cell
        if colours[0] != colours[1]:
            return None
        return variables[("q", edge, colours[0])]

    def zero_or_at_least_two(monomials):
        constant_count = monomials.count(0)
        monomials = [monomial for monomial in monomials if monomial]
        if constant_count >= 2:
            return
        if constant_count == 1:
            clauses.append(monomials)
            return
        for index, monomial in enumerate(monomials):
            clauses.append(
                [-monomial] + monomials[:index] + monomials[index + 1:]
            )

    top_fibres = 0
    response_fibres = {}

    # Complete top shadow.
    for word in itertools.product(range(3), repeat=6):
        monomials = []
        for matching in anchor.MATCHINGS:
            required = []
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
        if word == (0,) * 6:
            clauses.append(
                [monomial for monomial in monomials if monomial]
                if 0 not in monomials else [1, -1]
            )
        else:
            zero_or_at_least_two(monomials)
        if monomials:
            top_fibres += 1

    # Complete four-response shadow.
    response_data = (
        ("p1", "s1", (1,) * 6),
        ("p1", "s2", None),
        ("p2", "s1", None),
        ("p2", "s2", (2,) * 6),
    )
    for p_star, s_star, target in response_data:
        fibre_count = 0
        p_colour = int(p_star[1])
        s_colour = int(s_star[1])
        for word in itertools.product(range(3), repeat=6):
            monomials = []
            for p_site in range(6):
                if word[p_site] != p_colour:
                    continue
                for s_site in range(6):
                    if s_site == p_site or word[s_site] != s_colour:
                        continue
                    residual = tuple(site for site in range(6)
                                     if site not in (p_site, s_site))
                    for matching in anchor.perfect_matchings(residual):
                        required = [variables[(p_star, p_site)],
                                    variables[(s_star, s_site)]]
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
                clauses.append(
                    [monomial for monomial in monomials if monomial]
                    if 0 not in monomials else [1, -1]
                )
            else:
                zero_or_at_least_two(monomials)
            if monomials:
                fibre_count += 1
        response_fibres[p_star + s_star] = fibre_count

    base_clause_count = len(clauses)
    require(base_clause_count == 40635,
            f"the pre-circuit support shadow changed: {base_clause_count}")
    with Solver(name="cadical195", bootstrap_with=clauses) as base_solver:
        require(base_solver.solve(),
                "the support shadow closed before the algebraic circuits")

    # Universal binomial rows are detected with every allowed diagonal cell
    # formally present.  Their two terms have a common q monomial and the
    # two swapped star factors.
    binomial_witnesses = {}
    for p_star, s_star in (("p1", "s1"), ("p2", "s2")):
        colour = int(p_star[1])
        per_edge = {edge: [] for edge in itertools.combinations(range(6), 2)}
        for word in itertools.product(range(3), repeat=6):
            terms = []
            for p_site in range(6):
                if word[p_site] != colour:
                    continue
                for s_site in range(6):
                    if s_site == p_site or word[s_site] != colour:
                        continue
                    residual = tuple(site for site in range(6)
                                     if site not in (p_site, s_site))
                    for matching in anchor.perfect_matchings(residual):
                        required = []
                        q_factor = []
                        for edge in matching:
                            cell = (edge, (word[edge[0]], word[edge[1]]))
                            literal = q_literal(cell)
                            if literal is None:
                                break
                            q_factor.append(cell)
                            if literal:
                                required.append(literal)
                        else:
                            terms.append((p_site, s_site,
                                          tuple(sorted(set(required))),
                                          tuple(sorted(q_factor))))
            if len(terms) != 2:
                continue
            left, right = terms
            if (left[0], left[1]) != (right[1], right[0]):
                continue
            # Equality of optional support literals is insufficient here:
            # mandatory H/24-face cells still carry independent nonzero
            # coefficients.  The two terms must use the literal same two
            # q-cells, which also pins their fixed H signs.
            if left[2] != right[2] or left[3] != right[3]:
                continue
            edge = tuple(sorted((left[0], left[1])))
            per_edge[edge].append(left[2])
        require(all(per_edge[edge] for edge in per_edge),
                f"the universal {p_star}/{s_star} graph changed")
        binomial_witnesses[(p_star, s_star)] = per_edge

        odd_clause_count = 0
        for triangle in itertools.combinations(range(6), 3):
            edge_list = tuple(itertools.combinations(triangle, 2))
            star_literals = [variables[(p_star, site)] for site in triangle]
            star_literals += [variables[(s_star, site)] for site in triangle]
            for witnesses in itertools.product(*(per_edge[edge]
                                                  for edge in edge_list)):
                antecedent = set(star_literals)
                for witness in witnesses:
                    antecedent.update(witness)
                clauses.append([-literal for literal in sorted(antecedent)])
                odd_clause_count += 1
        require(odd_clause_count == 13756,
                f"the {p_star}/{s_star} odd-clause count changed")

    variable_count = next_variable - 1
    require(variable_count == 6399,
            f"the support-shadow variable count changed: {variable_count}")
    require(len(clauses) == 68147,
            f"the support-shadow clause count changed: {len(clauses)}")
    formula_payload = json.dumps(
        {"variables": variable_count, "clauses": clauses},
        separators=(",", ":"),
    )
    formula_digest = sha256(formula_payload.encode()).hexdigest()
    if EXPECTED_FORMULA_SHA256 != "TO_BE_FILLED":
        require(formula_digest == EXPECTED_FORMULA_SHA256,
                f"the support-shadow formula changed: {formula_digest}")

    with Solver(name="glucose42", bootstrap_with=clauses,
                with_proof=True) as solver:
        verdict = solver.solve()
        require(not verdict,
                "the support shadow acquired a circuit-free model")
        proof = solver.get_proof() or []
    additions = tuple(line for line in proof if not line.startswith("d "))
    parsed_proof = []
    for index, line in enumerate(additions):
        numbers = tuple(map(int, line.split()))
        require(numbers and numbers[-1] == 0 and 0 not in numbers[:-1],
                f"malformed proof addition {index}")
        parsed_proof.append(numbers[:-1])
    require(parsed_proof and parsed_proof[-1] == (),
            "the deletion-free proof does not end in empty")
    proof_payload = "\n".join(additions) + "\n"
    proof_digest = sha256(proof_payload.encode()).hexdigest()
    if EXPECTED_PROOF_SHA256 != "TO_BE_FILLED":
        require(proof_digest == EXPECTED_PROOF_SHA256,
                f"the deletion-free proof changed: {proof_digest}")

    # Independent RUP replay: retain every learned clause and refute its
    # negation by unit propagation in a fresh solver instance.
    with Solver(name="cadical195", bootstrap_with=clauses) as verifier:
        for index, clause in enumerate(parsed_proof):
            consistent, _propagated = verifier.propagate(
                assumptions=[-literal for literal in clause]
            )
            require(not consistent,
                    f"proof addition {index} is not RUP")
            verifier.add_clause(list(clause))

    witness_histogram = {
        p_star + s_star: {
            f"{left}{right}": len(witnesses)
            for (left, right), witnesses in sorted(per_edge.items())
        }
        for (p_star, s_star), per_edge in binomial_witnesses.items()
    }
    ledger = {
        "dependency": {"path": str(ANCHOR.relative_to(ROOT)),
                       "sha256": ANCHOR_SHA256},
        "mandatory_mixed_cells": sorted(anchor.LARGE_ZERO_CLASS),
        "optional_q_diagonal_cells": 45,
        "optional_star_coordinates": 24,
        "top_nonempty_fibres": top_fibres,
        "response_nonempty_fibres": response_fibres,
        "pre_circuit_clauses": base_clause_count,
        "pre_circuit_shadow_sat": True,
        "universal_binomial_witnesses": witness_histogram,
        "odd_triangle_clauses_per_diagonal_response": 13756,
        "cnf_variables": variable_count,
        "cnf_clauses": len(clauses),
        "formula_sha256": formula_digest,
        "proof_additions": len(parsed_proof),
        "proof_sha256": proof_digest,
        "certificate": (
            "every zero source coefficient has zero or at least two live "
            "monomials; target coefficients are nonempty; every activated "
            "universal star triangle is excluded by an ordinary 2P source "
            "identity; deletion-free RUP closes the resulting support CNF"
        ),
        "conclusion": (
            "the mandatory 24-cell off-01 Segre leading face admits no "
            "complex common-q one-bad packet"
        ),
    }
    ledger_payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    ledger_digest = sha256(ledger_payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(ledger_digest == EXPECTED_LEDGER_SHA256,
                f"the response-shadow ledger changed: {ledger_digest}")

    print("N=8 Segre 24-cell response shadow: PASS")
    print(f"CNF: {variable_count} variables; {len(clauses)} clauses")
    print(f"proof: {len(parsed_proof)} deletion-free RUP additions")
    print(f"formula sha256: {formula_digest}")
    print(f"proof sha256: {proof_digest}")
    print(f"ledger sha256: {ledger_digest}")


if __name__ == "__main__":
    main()
