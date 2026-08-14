#!/usr/bin/env python3
"""Exact nonlinear completion of the first pure-21 cost-three octagon.

Adjoin simultaneously the twelve source cells in the endpoint-fixed
octagon from the cost-three incidence audit.  Enumerate all +/-1 cell
assignments realizing its eight signed path coefficients, expand every
cross-product, and replay all 6561 rows.  The old eleven-row dual is not
nonlinearly stable.  A symbolic replay exhibits its first typed defect and
proves that the selected polynomial is not even in the radical of the old
mixed-row/anchor ideal after localizing at all twelve new source cells.
Every signed realization nevertheless descends to the cost-two colour-two
cofactor/22-anchor obstruction and none cancels the selected row.
"""

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from math import prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


PARENT_PATH = Path(__file__).with_name(
    "verify_n8_pure21_cost3_multicompanion_circuit_gate.py"
)
SPEC = spec_from_file_location("octagon_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
M = module_from_spec(SPEC)
SPEC.loader.exec_module(M)
B = M.B


NAMES = (
    "z0", "z1", "z3", "z4",
    "q01", "q03", "q05", "q14", "q15", "q34", "q35", "q45",
)

# The first signed octagon, in the order recorded in the cost-three note.
CIRCUIT_TERMS = (
    (("z0", "q14", "q35"), 1, (0, ((1, 4), (3, 5)))),
    (("z0", "q15", "q34"), -1, (0, ((1, 5), (3, 4)))),
    (("z1", "q03", "q45"), -1, (1, ((0, 3), (4, 5)))),
    (("z1", "q05", "q34"), 1, (1, ((0, 5), (3, 4)))),
    (("z3", "q01", "q45"), 1, (3, ((0, 1), (4, 5)))),
    (("z3", "q05", "q14"), -1, (3, ((0, 5), (1, 4)))),
    (("z4", "q01", "q35"), -1, (4, ((0, 1), (3, 5)))),
    (("z4", "q03", "q15"), 1, (4, ((0, 3), (1, 5)))),
)

CROSS_PATHS = {
    (0, ((1, 3), (4, 5))),
    (1, ((0, 4), (3, 5))),
    (3, ((0, 4), (1, 5))),
    (4, ((0, 5), (1, 3))),
}
LOWER_PATHS = {
    (5, ((0, 1), (3, 4))),
    (5, ((0, 3), (1, 4))),
}
BASE_PATH = (5, ((0, 4), (1, 3)))


def sign_solutions():
    answer = []
    for signs in product((1, -1), repeat=len(NAMES)):
        values = dict(zip(NAMES, signs))
        if all(
            prod(values[name] for name in names) == wanted
            for names, wanted, _ in CIRCUIT_TERMS
        ):
            answer.append(values)
    require(len(answer) == 32, ("octagon sign fibre changed", len(answer)))
    return tuple(answer)


SOLUTIONS = sign_solutions()


def adjoin(values):
    M.reset_tables()
    for site in (0, 1, 3, 4):
        B.SECOND[(1, site, 2)] = B.constant(values[f"z{site}"])
    for left, right in ((0, 1), (0, 3), (0, 5), (1, 4),
                        (1, 5), (3, 4), (3, 5), (4, 5)):
        B.Q_EDGE[(left, right, 2, 2)] = B.constant(values[f"q{left}{right}"])


def adjoin_symbolic():
    M.reset_tables()
    variables = {name: B.variable(name) for name in NAMES}
    for site in (0, 1, 3, 4):
        B.SECOND[(1, site, 2)] = variables[f"z{site}"]
    for left, right in ((0, 1), (0, 3), (0, 5), (1, 4),
                        (1, 5), (3, 4), (3, 5), (4, 5)):
        B.Q_EDGE[(left, right, 2, 2)] = variables[f"q{left}{right}"]
    return variables


def scale(polynomial_value, scalar):
    return B.clean({monomial: scalar * value
                    for monomial, value in polynomial_value.items()})


def evaluate_at(polynomial_value, values):
    answer = Q(0)
    for monomial, coefficient in polynomial_value.items():
        answer += coefficient * prod(values[name] for name in monomial)
    return answer


def polynomial(terms):
    return {tuple(sorted(names)): Q(coefficient)
            for names, coefficient in terms}


def normalize_old(polynomial_value):
    """Specialize the inherited source cells, retaining the twelve new ones."""
    old = M.P.NORMALIZATION
    answer = {}
    for monomial, coefficient in polynomial_value.items():
        kept = []
        value = coefficient
        for name in monomial:
            if name in old:
                value *= old[name]
            else:
                kept.append(name)
        key = tuple(kept)
        answer[key] = answer.get(key, Q(0)) + value
    return B.clean(answer)


def pure_path_terms():
    terms = {}
    for s_site in (0, 1, 3, 4, 5):
        second = B.SECOND.get((1, s_site, 2), {})
        if not second:
            continue
        rest = tuple(site for site in B.SITES if site not in (2, s_site))
        for matching in B.matchings(rest):
            edges = tuple(sorted(tuple(sorted(edge)) for edge in matching))
            term = B.multiply(B.FIRST[(2, 2, 2)], second)
            for left, right in edges:
                term = B.multiply(term, B.q_edge(left, right, 2, 2))
            value = M.evaluate(term)
            if value:
                terms[(s_site, edges)] = value
    return terms


def invariants(values):
    cross = (
        values["z0"] * values["q45"]
        + values["z1"] * values["q35"]
        + values["z3"] * values["q15"]
        + values["z4"] * values["q05"]
    )
    lower = (
        values["q01"] * values["q34"]
        + values["q03"] * values["q14"]
    )
    return Q(cross), Q(lower)


def audit_path_expansion():
    distribution = Counter()
    for values in SOLUTIONS:
        adjoin(values)
        terms = pure_path_terms()
        require(len(terms) == 15, ("pure nonlinear path count moved", values, terms))
        circuit_sum = sum(
            (terms[path] for _, _, path in CIRCUIT_TERMS), Q(0)
        )
        cross_sum = sum((terms[path] for path in CROSS_PATHS), Q(0))
        lower_sum = sum((terms[path] for path in LOWER_PATHS), Q(0))
        base_value = terms[BASE_PATH]
        cross, lower = invariants(values)
        require(circuit_sum == 0, ("octagon became selected-bright", values, terms))
        require(cross_sum == cross, ("cross-path sum changed", values, terms))
        require(lower_sum == -lower, ("lower-cost sum changed", values, terms))
        require(base_value == -1, ("old pure-21 term moved", values, base_value))
        require(sum(terms.values(), Q(0)) == -1 + cross - lower,
                ("nonlinear selected expansion changed", values, terms))
        distribution[(int(cross), int(lower), int(cross - lower))] += 1
    expected = Counter({(0, 2, -2): 16, (4, -2, 6): 8, (-4, -2, -2): 8})
    require(distribution == expected, ("nonlinear invariant distribution moved", distribution))
    M.reset_tables()
    return distribution


def audit_full_rows_and_dual():
    M.reset_tables()
    base = M.row_ledger()
    selected = M.SELECTED
    anchor = ((2,) * 6, 2, 2)
    outcomes = Counter()
    for values in SOLUTIONS:
        adjoin(values)
        candidate = M.row_ledger()
        difference = {
            row: candidate.get(row, Q(0)) - base.get(row, Q(0))
            for row in set(candidate) | set(base)
        }
        difference = {row: value for row, value in difference.items() if value}
        cross, lower = invariants(values)
        selected_value = difference.get(selected, Q(0))
        anchor_value = difference.get(anchor, Q(0))
        psi = sum(
            (weight * difference.get(row, Q(0)) for row, weight in M.DUAL.items()),
            Q(0),
        )
        require(selected_value == cross - lower,
                ("full selected row disagrees with path expansion", values, difference))
        require(anchor_value == lower,
                ("cost-two 22-anchor descent moved", values, difference))
        require(selected_value != 1,
                ("a sign-octagon unexpectedly repaired pure 21", values, difference))
        require(len(difference) == 32,
                ("nonlinear full-row support count moved", values, len(difference)))
        outcomes[(int(selected_value), int(psi), int(selected_value - psi))] += 1
    expected = Counter({
        (-2, 0, -2): 12,
        (-2, 2, -4): 6,
        (-2, -2, 0): 6,
        (6, 0, 6): 4,
        (6, 2, 4): 2,
        (6, -2, 8): 2,
    })
    require(outcomes == expected, ("nonlinear dual distribution moved", outcomes))
    require(sum(count for (selected_value, psi, _), count in outcomes.items()
                if selected_value != psi) == 26,
            "the eleven-row dual mismatch count changed")
    M.reset_tables()
    return outcomes


def audit_symbolic_dual_extension():
    selected = M.SELECTED
    anchor = ((2,) * 6, 2, 2)
    rows = set(M.DUAL) | {selected, anchor}
    M.reset_tables()
    base = {
        row: B.residual(row[1], row[2], row[0])
        for row in rows
    }
    adjoin_symbolic()
    difference = {
        row: B.subtract(B.residual(row[1], row[2], row[0]), base[row])
        for row in rows
    }
    psi = {}
    for row, weight in M.DUAL.items():
        psi = B.add(psi, scale(difference[row], weight))
    defect = B.subtract(difference[selected], psi)

    selected_expected = polynomial((
        (("P2", "Y", "q01", "q34"), 1),
        (("P2", "Y", "q03", "q14"), 1),
        (("P2", "f", "q15", "z3"), 1),
        (("P2", "f", "q35", "z1"), 1),
        (("P2", "g", "q05", "z4"), 1),
        (("P2", "g", "q45", "z0"), 1),
        (("P2", "q01", "q35", "z4"), 1),
        (("P2", "q01", "q45", "z3"), 1),
        (("P2", "q03", "q15", "z4"), 1),
        (("P2", "q03", "q45", "z1"), 1),
        (("P2", "q05", "q14", "z3"), 1),
        (("P2", "q05", "q34", "z1"), 1),
        (("P2", "q14", "q35", "z0"), 1),
        (("P2", "q15", "q34", "z0"), 1),
    ))
    psi_expected = polynomial((
        (("D", "c", "g", "q45"), 1),
        (("D", "c", "q14", "q35"), 1),
        (("D", "c", "q15", "q34"), 1),
        (("P1", "c", "g", "z4"), 1),
        (("P1", "c", "q14", "z3"), 1),
        (("P1", "c", "q34", "z1"), 1),
    ))
    anchor_expected = polynomial((
        (("P2", "S2", "q01", "q34"), 1),
        (("P2", "S2", "q03", "q14"), 1),
    ))
    require(difference[selected] == selected_expected,
            ("symbolic selected polynomial changed", difference[selected]))
    require(psi == psi_expected, ("symbolic dual polynomial changed", psi))
    require(difference[anchor] == anchor_expected,
            ("symbolic anchor polynomial changed", difference[anchor]))
    require(len(defect) == 20, ("symbolic dual defect size changed", defect))
    first_monomial = ("D", "c", "g", "q45")
    require(sorted(defect.items())[0] == (first_monomial, Q(-1)),
            ("first symbolic defect moved", sorted(defect.items())[0]))

    active_dual_rows = {row for row in M.DUAL if difference[row]}
    expected_active = {
        ((1, 2, 1, 2, 2, 1), 1, 1),
        ((1, 2, 1, 2, 2, 2), 0, 1),
    }
    require(active_dual_rows == expected_active,
            ("active symbolic dual rows changed", active_dual_rows))

    # This all-nonzero point proves non-membership after saturating by the
    # product of all twelve new cells.  The two active old mixed rows and the
    # 22 anchor vanish, while the selected change is nonzero.
    witness = dict(M.P.NORMALIZATION)
    witness.update({
        "z0": Q(1), "z1": Q(1), "z3": Q(1), "z4": Q(-2),
        "q01": Q(1), "q03": Q(-1), "q05": Q(1), "q14": Q(1),
        "q15": Q(1), "q34": Q(1), "q35": Q(1), "q45": Q(-2),
    })
    require(all(witness[name] for name in NAMES), "torus witness left the localization")
    require(all(evaluate_at(difference[row], witness) == 0 for row in M.DUAL),
            "torus witness did not kill every old dual row")
    require(evaluate_at(difference[anchor], witness) == 0,
            "torus witness did not kill the old anchor")
    require(evaluate_at(difference[selected], witness) == 2,
            "torus witness no longer separates the selected polynomial")

    M.reset_tables()
    return {
        "selected_terms": len(selected_expected),
        "psi_terms": len(psi_expected),
        "defect_terms": len(defect),
        "first_defect": "-D*c*g*q45",
        "first_defect_row": "121222:01",
        "first_defect_operation": "DQ",
        "first_defect_fine": "67|02|13|45",
        "localized_ideal_witness_selected": 2,
    }


def audit_polynomial_descent():
    variables = {name: B.variable(name) for name in NAMES}
    q = lambda edge: variables[f"q{edge}"]
    r1 = B.add(B.multiply(q("03"), q("45")), B.multiply(q("05"), q("34")))
    r2 = B.add(B.multiply(q("01"), q("45")), B.multiply(q("05"), q("14")))
    e1 = B.multiply(variables["z1"], r1)
    e2 = B.multiply(variables["z3"], r2)
    j = B.add(B.multiply(q("01"), q("34")), B.multiply(q("03"), q("14")))

    # Direct polynomial saturation certificate:
    # 2*z1*z3*q05*q01*q34
    # = z1*z3*q05*J + z3*q01*E1 - z1*q03*E2.
    left = B.product_polynomials((
        B.constant(2), variables["z1"], variables["z3"],
        q("05"), q("01"), q("34"),
    ))
    right = B.add(
        B.multiply(
            B.product_polynomials((variables["z1"], variables["z3"], q("05"))),
            j,
        ),
        B.subtract(
            B.multiply(B.multiply(variables["z3"], q("01")), e1),
            B.multiply(B.multiply(variables["z1"], q("03")), e2),
        ),
    )
    require(left == right, ("lower-cost saturation certificate changed", left, right))

    # E1 and E2 are consequences of an exact factorization of the signed
    # octagon vector (the two displayed path monomials have opposite common
    # value).  They are not, however, standalone full residual rows once all
    # cross products are present.  This distinction separates the general
    # octagon-factorization theorem from a theorem on the whole source torus.
    M.reset_tables()
    all_rows = tuple(
        (word, row, column)
        for word in product(B.COLORS, repeat=6)
        for row in B.COLORS
        for column in B.COLORS
    )
    base = {
        key: B.residual(key[1], key[2], key[0])
        for key in all_rows
    }
    adjoin_symbolic()
    full_differences = tuple(
        normalize_old(B.subtract(B.residual(key[1], key[2], key[0]), base[key]))
        for key in all_rows
    )
    require(not any(candidate in (e1, B.negate(e1), e2, B.negate(e2))
                    for candidate in full_differences),
            "a circuit pair relation unexpectedly became a standalone full row")
    M.reset_tables()

    # The +/-1 circuit quotient is finite and radical.  Its selected change
    # D=C-J has values only -2 and 6, so D-1 is a unit with inverse (D-3)/15.
    values_seen = set()
    for values in SOLUTIONS:
        cross, lower = invariants(values)
        selected_change = cross - lower
        values_seen.add(selected_change)
        require((selected_change + 2) * (selected_change - 6) == 0,
                ("Boolean annihilator failed", values, selected_change))
        inverse = (selected_change - 3) / 15
        require(inverse * (selected_change - 1) == 1,
                ("Boolean unit inverse failed", values, selected_change))
    require(values_seen == {Q(-2), Q(6)}, ("selected value set moved", values_seen))
    return {
        "laurent_octagon_factorizations_excluded": True,
        "circuit_pair_relations_are_standalone_full_rows": False,
        "finite_sign_selected_unit": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "signs", "paths", "rows", "symbolic", "certificate"),
        default="all",
    )
    args = parser.parse_args()

    path_distribution = row_outcomes = symbolic = certificate = None
    if args.mode in ("all", "signs", "paths"):
        path_distribution = audit_path_expansion()
    if args.mode in ("all", "rows"):
        row_outcomes = audit_full_rows_and_dual()
    if args.mode in ("all", "symbolic"):
        symbolic = audit_symbolic_dual_extension()
    if args.mode in ("all", "certificate"):
        certificate = audit_polynomial_descent()

    report = {
        "mode": args.mode,
        "new_s1_cells": 4,
        "new_q2_cells": 8,
        "simultaneous_new_cells": 12,
        "signed_octagon_solutions": len(SOLUTIONS),
        "active_pure21_paths": 15,
        "path_partition": {"base": 1, "octagon": 8, "cross": 4, "lower_cost": 2},
        "selected_delta_values": [-2, 6],
        "selected_final_values": [-3, 5],
        "path_distributions": None if path_distribution is None else {
            str(key): value for key, value in sorted(path_distribution.items())
        },
        "row_outcome_types": None if row_outcomes is None else len(row_outcomes),
        "old_dual_failures": None if row_outcomes is None else 26,
        "symbolic_dual": symbolic,
        "lower_cost_anchor_delta_values": [-2, 2],
        "saturation_certificate": certificate,
        "scope": (
            "arbitrary nonzero exact signed-octagon factorizations by Laurent descent; "
            "+/-1 only for the selected-row unit census"
        ),
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 pure-21 octagon nonlinear completion gate: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
