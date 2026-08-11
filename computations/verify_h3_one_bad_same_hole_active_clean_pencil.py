#!/usr/bin/env python3
"""Exact active-clean upgrade of the literal h=3 same-hole cap.

The cap K=E_tt from 9b2d709 is clean but inactive.  The same selected
p-r block also has the canonical generically active line

    L(mu) = E_cc + mu I.

This checker computes the full h=3 homogeneous cap error of K+zL in the
six-site square-zero algebra.  It vanishes identically, while mu=z=1 is
active.  Thus the literal same-hole quadratic packet has an active clean
point; the earlier inactive landing alone was not the conclusion.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_same_hole_intrinsic_cap.py":
        "8a6e55f37a2989f2020a2d9e18a3f4e6ac88e7b1e1d599ce74b188b495132755",
    "notes/clean-pair-cap-exact-descent-target.md":
        "90f49ac4fde9b793409d9081977e7a7135ebd76c1b5df5d699387d142c2b9b75",
    "notes/unconditional-curvature-line-selection.md":
        "a64dc29a6e88df96b47c0f5d64107d4cd4316cf8b3e1c230033dd988f7363e48",
    "computations/verify_h3_one_bad_companion_quadratic_mate_partition.py":
        "b8047fd1e610052fc47fcc0a5e11dd99d582f3ae638ad18825af46d036bc52cb",
}
EXPECTED_LEDGER_SHA256 = (
    "c8a84df94e1be3e4fe80526cdbd63c3d00cc04140a67f019f77aba4bd91860fc"
)

P, Q, R = 5, 6, 7
W = (0, 1, 2, 3, 4, Q)
A, C, T = range(3)

# Polynomial variables are (z, mu, gamma), where gamma is the arbitrary
# product of the two same-hole P_c/R_c coefficients.
ZERO_MONOMIAL = (0, 0, 0)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def clean(poly):
    return Counter({monomial: coefficient
                    for monomial, coefficient in poly.items() if coefficient})


def poly_add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def poly_scale(poly, scalar):
    return clean(Counter({monomial: scalar * coefficient
                          for monomial, coefficient in poly.items()}))


def poly_mul(left, right):
    answer = Counter()
    for lm, lc in left.items():
        for rm, rc in right.items():
            answer[tuple(a + b for a, b in zip(lm, rm, strict=True))] += lc * rc
    return clean(answer)


ONE = Counter({ZERO_MONOMIAL: Fraction(1)})
Z = Counter({(1, 0, 0): Fraction(1)})
MU = Counter({(0, 1, 0): Fraction(1)})
GAMMA = Counter({(0, 0, 1): Fraction(1)})


def matching_tensor(polynomial_cells, vertices):
    """Full matching tensor with polynomial-valued decorated cells."""
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    output = Counter()
    for matching in base.perfect_matchings(vertices):
        choices = []
        for u, v in matching:
            choices.append([(key, poly) for key, poly in polynomial_cells.items()
                            if key[:2] == (u, v)])
        if any(not choice for choice in choices):
            continue
        for selected in itertools.product(*choices):
            word = {}
            coefficient = ONE
            for (u, v), (key, poly) in zip(matching, selected, strict=True):
                word[u], word[v] = key[2], key[3]
                coefficient = poly_mul(coefficient, poly)
            for monomial, value in coefficient.items():
                output[(tuple(word[site] for site in vertices), monomial)] += value
    return clean(output)


def mixed_r2_q_tensor(response, q, vertices):
    """Compute r^[2] q in the six-site square-zero algebra."""
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    output = Counter()
    for matching in base.perfect_matchings(vertices):
        for q_index in range(3):
            choices = []
            for index, (u, v) in enumerate(matching):
                cells = q if index == q_index else response
                choices.append([(key, poly) for key, poly in cells.items()
                                if key[:2] == (u, v)])
            if any(not choice for choice in choices):
                continue
            for selected in itertools.product(*choices):
                word = {}
                coefficient = ONE
                for (u, v), (key, poly) in zip(
                        matching, selected, strict=True):
                    word[u], word[v] = key[2], key[3]
                    coefficient = poly_mul(coefficient, poly)
                for monomial, value in coefficient.items():
                    output[(tuple(word[site] for site in vertices), monomial)] += value
    return clean(output)


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    cell = base.cell

    source = clean(closure.build_eight_site_source(base, Fraction(0)))

    # Exact selected p-r normal form.  The direct anchor is E_cc.  Endpoint
    # multiplication gives three diagonal response edges.  The q-site
    # collision in P_a*R_a is automatically zero; the surviving a edge is 26.
    direct = [[source.get(cell(P, R, i, k), Fraction(0))
               for k in range(3)] for i in range(3)]
    require(direct == [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            f"the p-r direct block changed: {direct}")

    edge_a = cell(2, Q, A, A)
    edge_c = cell(1, 2, C, C)
    edge_t = cell(1, 4, T, T)
    require(len({edge_a[:2], edge_c[:2], edge_t[:2]}) == 3,
            "the three response edges collided")
    require(set(edge_a[:2]).isdisjoint(edge_t[:2]),
            "the a/t response edges stopped being disjoint")
    require(not set(edge_c[:2]).isdisjoint(edge_a[:2])
            and not set(edge_c[:2]).isdisjoint(edge_t[:2]),
            "the same-hole c edge stopped meeting both other edges")

    # L(mu)=E_cc+mu I.  Its response is
    # mu*A + (1+mu)*gamma*C + mu*T.  K=E_tt has response T.
    # Hence K+zL has the following complete ternary response.
    z_mu = poly_mul(Z, MU)
    response = {
        edge_a: z_mu,
        edge_c: poly_mul(Z, poly_mul(poly_add(ONE, MU), GAMMA)),
        edge_t: poly_add(ONE, z_mu),
    }
    response = {key: clean(value) for key, value in response.items()}

    # The residual internal quadratic x is extracted literally.  Polynomial
    # coefficients are constants.  Crucially, it has no cell on the only
    # complement edge 03 left by the disjoint a/t response pair.
    q = {
        key: Counter({ZERO_MONOMIAL: value})
        for key, value in source.items()
        if key[0] in W and key[1] in W and value
    }
    require(not any(key[:2] == (0, 3) for key in q),
            "the complement edge 03 acquired an internal cell")

    # This absence is not merely a sparse-support observation.  At the
    # first filtered tangent layer, build all 167 literal columns of the
    # four surrounding response tensors.  Every decorated q03 direction is
    # forced to zero.  Six have a unique ca-row coefficient.  The remaining
    # three can be paired only with Ra@3:b, whose extra Ra-row coefficient
    # is itself unique, so that attempted repair is also zero.
    mate = importlib.import_module(
        "verify_h3_one_bad_companion_quadratic_mate_partition")
    q0 = {key: value for key, value in source.items()
          if key[0] in range(5) and key[1] in range(5) and value}
    q0 = Counter(q0)
    stars0 = {
        "Qc": ((0, C, Fraction(1)),),
        "Ra": ((2, A, Fraction(1)),),
        "Pt": ((1, T, Fraction(1)),),
        "Qt": ((0, T, Fraction(1)),),
        "Rt": ((4, T, Fraction(1)),),
    }
    tangent_base = mate.flatten(mate.four_rows(base, q0, stars0))

    def tangent_column(moved_q, moved_stars,
                       d_ca=Fraction(1), d_tt=Fraction(0)):
        result = mate.flatten(mate.four_rows(
            base, moved_q, moved_stars, d_ca, d_tt))
        result.subtract(tangent_base)
        return mate.clean(result)

    tangent_columns = {}
    for u, v in itertools.combinations(range(5), 2):
        for a in range(3):
            for b in range(3):
                moved = Counter(q0)
                moved[cell(u, v, a, b)] += 1
                tangent_columns[f"q{u}{v}:{a}{b}"] = tangent_column(
                    moved, stars0)
    for family in stars0:
        for hole in range(5):
            for colour in range(3):
                moved = dict(stars0)
                moved[family] = stars0[family] + (
                    (hole, colour, Fraction(1)),)
                tangent_columns[f"{family}@{hole}:{colour}"] = tangent_column(
                    q0, moved)
    tangent_columns["Dca"] = tangent_column(q0, stars0, 2, 0)
    tangent_columns["Dtt"] = tangent_column(q0, stars0, 1, 1)
    require(len(tangent_columns) == 167,
            "the filtered four-row tangent width changed")

    q03_incidence = {}
    for a in range(3):
        for b in range(3):
            name = f"q03:{a}{b}"
            coordinate = (2, (a, T, C, b, C))
            require(tangent_columns[name] == Counter({coordinate: 1}),
                    f"the q03 tangent defect changed: {name}")
            hits = tuple(sorted(column_name for column_name, column
                                in tangent_columns.items()
                                if column.get(coordinate)))
            expected = ((name,) if a != C
                        else (f"Ra@3:{b}", name))
            require(hits == tuple(sorted(expected)),
                    f"the q03 incidence changed: {name}: {hits}")
            if a == C:
                repair_tail = (1, (A, A, C, b, C))
                repair_name = f"Ra@3:{b}"
                repair_hits = tuple(sorted(
                    column_name for column_name, column
                    in tangent_columns.items() if column.get(repair_tail)))
                require(repair_hits == (repair_name,),
                        f"the Ra repair tail acquired a mate: {repair_hits}")
            q03_incidence[name] = hits

    r3 = matching_tensor(response, W)
    r2q = mixed_r2_q_tensor(response, q, W)
    scalar = poly_mul(Z, poly_add(ONE, MU))  # z(1+mu)
    error = Counter(r3)
    for (word, monomial), coefficient in r2q.items():
        product = poly_mul(Counter({monomial: coefficient}), scalar)
        for product_monomial, product_coefficient in product.items():
            error[(word, product_monomial)] += product_coefficient
    error = clean(error)
    require(not r3, f"the cap pencil acquired r^[3]: {r3}")
    require(not r2q, f"the cap pencil acquired r^[2]q: {r2q}")
    require(not error, f"the homogeneous cap error is nonzero: {error}")

    # The vanishing is structural: r^[2] has only A*T, whose unused sites
    # are 0,3.  Record its exact polynomial coefficient before multiplication
    # by q, to ensure the result is not a vacuous r^[2]=0 assertion.
    r2_coefficient = poly_mul(response[edge_a], response[edge_t])
    expected_r2 = poly_add(z_mu, poly_mul(z_mu, z_mu))
    require(r2_coefficient == expected_r2 and r2_coefficient,
            f"the nonzero r^[2] coefficient changed: {r2_coefficient}")

    # Exact stability boundary.  Adding any one decorated q03 cell produces
    # a distinct nonzero A*T*q03 coefficient.  Thus the all-order condition
    # for this same pencil is literally q|_{03}=0; the tangent audit proves
    # it only at the first filtered layer, not automatically at all orders.
    q03_error_words = {}
    for a in range(3):
        for b in range(3):
            q03 = {cell(0, 3, a, b): ONE}
            tail = mixed_r2_q_tensor(response, q03, W)
            expected_word = (a, T, A, b, T, A)
            require(set(word for word, _ in tail) == {expected_word}
                    and len(tail) == 2,
                    f"the q03 stability tail changed: {(a, b)}: {tail}")
            q03_error_words[f"{a}{b}"] = "".join(map(str, expected_word))
    require(len(set(q03_error_words.values())) == 9,
            "two decorated q03 tails acquired the same output word")

    # Activity ledger for K+zL:
    # s=z(1+mu), kappas=(z*mu, z*(1+mu), 1+z*mu).
    kappas = (z_mu, poly_mul(Z, poly_add(ONE, MU)), poly_add(ONE, z_mu))
    activity = scalar
    for kappa in kappas:
        activity = poly_mul(activity, kappa)
    require(activity, "the cap pencil is identically inactive")

    # The explicit point mu=z=1 is active and clean.
    def evaluate(poly, z_value=1, mu_value=1, gamma_value=1):
        return sum(coefficient * z_value ** monomial[0]
                   * mu_value ** monomial[1] * gamma_value ** monomial[2]
                   for monomial, coefficient in poly.items())

    scalar_at_one = evaluate(scalar)
    kappas_at_one = tuple(evaluate(kappa) for kappa in kappas)
    require(scalar_at_one == 2 and kappas_at_one == (1, 2, 2),
            f"the explicit active point changed: {scalar_at_one}, {kappas_at_one}")
    require(evaluate(activity) == 8,
            "the explicit cap stopped being active")

    cap_at_one = [[Fraction(int(i == T and k == T)
                            + int(i == C and k == C)
                            + int(i == k))
                   for k in range(3)] for i in range(3)]
    require(cap_at_one == [[1, 0, 0], [0, 2, 0], [0, 0, 2]],
            f"the explicit cap matrix changed: {cap_at_one}")

    ledger = {
        "dependencies": PINS,
        "selected_pair": (P, R),
        "inactive_cap": "K=E_tt",
        "canonical_active_line": "L(mu)=E_cc+mu*I",
        "pencil": "K+zL",
        "response_edges": {
            "A": str(edge_a), "C": str(edge_c), "T": str(edge_t),
            "intersection": "C meets A and T; A and T are disjoint",
        },
        "response_coefficients": {
            "A": "z*mu",
            "C": "z*(1+mu)*gamma",
            "T": "1+z*mu",
        },
        "error": {
            "formula_h3": "s*r^[2]*q+r^[3]",
            "r3_terms": len(r3),
            "r2q_terms": len(r2q),
            "reason": (
                "only A*T survives r^[2], and its complementary physical "
                "edge 03 is absent from q"
            ),
            "verdict": "identically zero in z,mu,gamma",
        },
        "edge03_scope": {
            "first_filtered_tangent_columns": len(tangent_columns),
            "q03_incidence": q03_incidence,
            "forced_zero_at_first_filtered_layer": True,
            "all_order_stability_condition": "q restricted to physical edge 03 is zero",
            "one_cell_error_words": q03_error_words,
            "not_proved": (
                "nonlinear higher-order tails cannot regenerate q03 in the "
                "completed arbitrary-support branch"
            ),
        },
        "activity": {
            "s": "z*(1+mu)",
            "kappas": ("z*mu", "z*(1+mu)", "1+z*mu"),
            "explicit_mu_z": (1, 1),
            "explicit_cap": [[str(value) for value in row]
                             for row in cap_at_one],
            "explicit_s": str(scalar_at_one),
            "explicit_kappas": tuple(str(value) for value in kappas_at_one),
            "activity_product": str(evaluate(activity)),
        },
        "verdict": (
            "the inactive K=E_tt landing upgrades along the canonical "
            "physical line to the explicit active clean cap diag(1,2,2)"
        ),
        "scope": (
            "exact literal same-hole quadratic normal form, with arbitrary "
            "same-hole product gamma.  The complete four-row tangent module "
            "forces edge 03 to stay absent at the first filtered layer.  "
            "All-order cleanliness holds exactly while q|_03=0, but no claim "
            "is made that nonlinear higher-order tails preserve that condition"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the active-clean pencil ledger changed: {digest}")

    print("h=3 one-bad same-hole active-clean pencil: PASS")
    print("pencil: E_tt + z(E_cc + mu I)")
    print("cap error: identically zero in z,mu,gamma")
    print("nonzero r^[2] uses edges 26 and 14; complement edge 03 is absent")
    print("mu=z=1: cap=diag(1,2,2), s=2, kappa=(1,2,2)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
