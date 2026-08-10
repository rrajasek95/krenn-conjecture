#!/usr/bin/env python3
"""Find the smallest optional-support survivor on the Segre 24-cell face.

This is the all-subsets complement to the mandatory-face theorem 710e2f5.
The 24 mixed cells are Boolean optional variables, while H is fixed and the
45 diagonal q cells and 24 star coordinates are optional.  We impose the
complete top/four-response support shadow and the same source-labelled odd
star triangles as 710e2f5, then minimize the number of live face cells after
excluding the already-audited two-cell layer.
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
EXPECTED_LEDGER_SHA256 = (
    "539937103167ea8a95f72454e88602abc30a317b4aa11a21fe3dd4fd8fb746be"
)
EXPECTED_FORMULA_SHA256 = (
    "49f9879f7e5cc117c63ce886b3cefa5586e38601dd7599eae15f2ca7e777d24c"
)
EXPECTED_PROOF_SHA256 = (
    "3563bda3b92b4183f1402b7e12580cd5f466a59e43ce8bfe1ea9072c1059a794"
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


def main():
    anchor = load_anchor()
    four = anchor.load_dependency()
    one = four.load_dependency()
    first = one.load_dependency()
    diagonal = first.load_dependency()
    pure = diagonal.load_dependency()
    source = pure.load_dependency()
    support_h, _weights_h = pure.build_top_null_H(source)
    fixed = set(support_h)
    face = tuple(sorted(anchor.LARGE_ZERO_CLASS))
    face_cells = {anchor.parse_cell(label): label for label in face}

    variables = {}
    next_variable = 1
    for edge in anchor.EDGES:
        for colour in range(3):
            variables[("qdiag", edge, colour)] = next_variable
            next_variable += 1
    for label in face:
        variables[("qface", label)] = next_variable
        next_variable += 1
    for star in ("p1", "p2", "s1", "s2"):
        for site in range(6):
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

    def q_literal(cell):
        if cell in fixed:
            return 0
        if cell in face_cells:
            return variables[("qface", face_cells[cell])]
        edge, colours = cell
        if colours[0] == colours[1]:
            return variables[("qdiag", edge, colours[0])]
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

    # Complete top shadow.
    top_fibres = 0
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
            clauses.append([m for m in monomials if m]
                           if 0 not in monomials else [1, -1])
        else:
            zero_or_at_least_two(monomials)
        top_fibres += bool(monomials)

    # Complete response shadow.
    response_data = (
        ("p1", "s1", (1,) * 6),
        ("p1", "s2", None),
        ("p2", "s1", None),
        ("p2", "s2", (2,) * 6),
    )
    response_fibres = {}
    for p_star, s_star, target in response_data:
        count = 0
        p_colour, s_colour = int(p_star[1]), int(s_star[1])
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
            count += bool(monomials)
        response_fibres[p_star + s_star] = count

    pre_circuit_clauses = len(clauses)
    with Solver(name="cadical195", bootstrap_with=clauses) as base_solver:
        require(base_solver.solve(),
                "the optional support shadow closed before odd triangles")

    # Conditional versions of the same exact odd triangles as 710e2f5.
    witness_histogram = {}
    odd_clause_count = 0
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
                        required, q_factor = [], []
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
            if ((left[0], left[1]) != (right[1], right[0]) or
                    left[2] != right[2] or left[3] != right[3]):
                continue
            per_edge[tuple(sorted((left[0], left[1])))].append(left[2])
        require(all(per_edge.values()),
                f"the optional-face {p_star}/{s_star} graph changed")
        witness_histogram[p_star + s_star] = {
            f"{edge[0]}{edge[1]}": len(witnesses)
            for edge, witnesses in sorted(per_edge.items())
        }
        for triangle in itertools.combinations(range(6), 3):
            edge_list = tuple(itertools.combinations(triangle, 2))
            star_literals = [variables[("star", p_star, site)]
                             for site in triangle]
            star_literals += [variables[("star", s_star, site)]
                              for site in triangle]
            for witnesses in itertools.product(
                    *(per_edge[edge] for edge in edge_list)):
                antecedent = set(star_literals)
                for witness in witnesses:
                    antecedent.update(witness)
                clauses.append([-literal for literal in sorted(antecedent)])
                odd_clause_count += 1

    variable_count = next_variable - 1
    formula_payload = json.dumps(
        {"variables": variable_count, "clauses": clauses},
        separators=(",", ":"),
    )
    formula_digest = sha256(formula_payload.encode()).hexdigest()
    require(formula_digest == EXPECTED_FORMULA_SHA256,
            f"the optional-face formula changed: {formula_digest}")

    with Solver(name="glucose42", bootstrap_with=clauses,
                with_proof=True) as solver:
        verdict = solver.solve()
        require(not verdict,
                "the unrestricted optional shadow acquired a circuit-free model")
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
    require(proof_digest == EXPECTED_PROOF_SHA256,
            f"the deletion-free proof changed: {proof_digest}")

    # Independent deletion-free RUP replay in a fresh solver instance.
    with Solver(name="cadical195", bootstrap_with=clauses) as verifier:
        for index, clause in enumerate(parsed_proof):
            consistent, _propagated = verifier.propagate(
                assumptions=[-literal for literal in clause]
            )
            require(not consistent, f"proof addition {index} is not RUP")
            verifier.add_clause(list(clause))

    ledger = {
        "dependency": {"path": str(ANCHOR.relative_to(ROOT)),
                       "sha256": ANCHOR_SHA256},
        "optional_face_cells": list(face),
        "incidence_classes": {"A": sorted(anchor.NEGATIVE_CLASS),
                              "B": sorted(anchor.POSITIVE_CLASS)},
        "optional_diagonal_q_cells": 45,
        "optional_star_coordinates": 24,
        "top_nonempty_fibres": top_fibres,
        "response_nonempty_fibres": response_fibres,
        "pre_circuit_clauses": pre_circuit_clauses,
        "pre_circuit_shadow_sat": True,
        "odd_triangle_clauses": odd_clause_count,
        "binomial_witnesses": witness_histogram,
        "cnf_variables": variable_count,
        "cnf_clauses": len(clauses),
        "formula_sha256": formula_digest,
        "proof_additions": len(parsed_proof),
        "proof_sha256": proof_digest,
        "verdict": (
            "the conditional odd-triangle support shadow is UNSAT for every "
            "optional subset of the 24-cell face; no A/B incidence assumption "
            "is needed"
        ),
        "scope": (
            "the fixed Segre H chart with arbitrary support on the 24 face, "
            "all 45 diagonal q cells, and all 24 star coordinates"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"optional-face ledger changed: {digest}")
    print("N=8 Segre optional 24-face shadow: PASS")
    print("all optional supports: UNSAT (no A/B assumption)")
    print("CNF:", variable_count, "variables;", len(clauses), "clauses")
    print("proof:", len(parsed_proof), "deletion-free RUP additions")
    print("formula sha256:", formula_digest)
    print("proof sha256:", proof_digest)
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
