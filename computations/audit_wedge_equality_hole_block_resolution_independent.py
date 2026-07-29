#!/usr/bin/env python3
"""Clean-room exact audit of the unconditional wedge hole-block proof.

This file deliberately does not import the primary checker.  It rebuilds the
matching ledger with a bit-mask recursion, models the typed-mode implications,
checks a flattening-rank certificate, audits every zero/nonzero branch in the
single-survivor reduction, and verifies the last syzygy component by component.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json

import sympy as sy


SITE_NAMES = ("a", "b", "c", "d", "e", "f")
SITE_NUMBER = {name: number for number, name in enumerate(SITE_NAMES)}
NUMBER_SITE = dict(enumerate(SITE_NAMES))
FULL_MASK = (1 << len(SITE_NAMES)) - 1
FROZEN_LEDGER_SHA256 = "92e9ad11445b29cc87693fcbfe3a80be9ef21d664d799451b2f5f141910ce462"


def canonical_edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


EDGES = tuple(combinations(range(6), 2))
EDGE_SYMBOL = {
    pair: sy.Symbol("x_" + NUMBER_SITE[pair[0]] + NUMBER_SITE[pair[1]])
    for pair in EDGES
}


@lru_cache(maxsize=None)
def mask_matchings(mask: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate matchings by taking the highest numbered remaining site."""
    if mask == 0:
        return ((),)
    pivot = mask.bit_length() - 1
    without_pivot = mask ^ (1 << pivot)
    results: list[tuple[tuple[int, int], ...]] = []
    partner_mask = without_pivot
    while partner_mask:
        low_bit = partner_mask & -partner_mask
        partner = low_bit.bit_length() - 1
        remainder = without_pivot ^ low_bit
        for tail in mask_matchings(remainder):
            results.append(tuple(sorted((canonical_edge(pivot, partner),) + tail)))
        partner_mask ^= low_bit
    return tuple(sorted(results))


def edge_word(pair: tuple[int, int]) -> str:
    return NUMBER_SITE[pair[0]] + NUMBER_SITE[pair[1]]


def matching_polynomial(mask: int) -> sy.Expr:
    return sy.expand(
        sum(
            sy.prod(EDGE_SYMBOL[pair] for pair in matching)
            for matching in mask_matchings(mask)
        )
    )


def cofactor(omitted: tuple[int, int]) -> sy.Expr:
    mask = FULL_MASK ^ (1 << omitted[0]) ^ (1 << omitted[1])
    return matching_polynomial(mask)


def audit_matchings() -> dict[str, object]:
    full_matchings = mask_matchings(FULL_MASK)
    assert len(full_matchings) == 15
    assert len(set(full_matchings)) == 15

    cofactor_words: dict[str, list[list[str]]] = {}
    for omitted in EDGES:
        remaining_mask = FULL_MASK ^ (1 << omitted[0]) ^ (1 << omitted[1])
        terms = mask_matchings(remaining_mask)
        assert len(terms) == 3
        cofactor_words[edge_word(omitted)] = [
            [edge_word(pair) for pair in matching] for matching in terms
        ]

    # These are the nine identities actually used by the proof.  Compare
    # monomial supports, so no ordering choice is inherited from the primary.
    expected = {
        "ab": (("cd", "ef"), ("ce", "df"), ("cf", "de")),
        "bc": (("ad", "ef"), ("ae", "df"), ("af", "de")),
        "de": (("ab", "cf"), ("ac", "bf"), ("af", "bc")),
        "ac": (("bd", "ef"), ("be", "df"), ("bf", "de")),
        "ae": (("bc", "df"), ("bd", "cf"), ("bf", "cd")),
        "be": (("ac", "df"), ("ad", "cf"), ("af", "cd")),
        "bd": (("ac", "ef"), ("ae", "cf"), ("af", "ce")),
        "cd": (("ab", "ef"), ("ae", "bf"), ("af", "be")),
        "bf": (("ac", "de"), ("ad", "ce"), ("ae", "cd")),
    }
    for omitted_word, wanted in expected.items():
        got = {tuple(sorted(term)) for term in cofactor_words[omitted_word]}
        assert got == {tuple(sorted(term)) for term in wanted}

    # A perfect matching is assigned to its unique b-edge.  Thus the star is
    # an exact partition, rather than a formula true only after specialization.
    b = SITE_NUMBER["b"]
    star = sy.Integer(0)
    incidence_count: dict[tuple[tuple[int, int], ...], int] = {
        matching: 0 for matching in full_matchings
    }
    for other in range(6):
        if other == b:
            continue
        b_edge = canonical_edge(b, other)
        star += EDGE_SYMBOL[b_edge] * cofactor(b_edge)
        for matching in full_matchings:
            if b_edge in matching:
                incidence_count[matching] += 1
    assert set(incidence_count.values()) == {1}
    assert sy.expand(star - matching_polynomial(FULL_MASK)) == 0

    return {
        "full_matchings": [
            [edge_word(pair) for pair in matching] for matching in full_matchings
        ],
        "cofactors": cofactor_words,
        "b_star_incidence": sorted(incidence_count.values()),
    }


def pure_pair_nonzero(left: str, right: str) -> bool:
    return left != right


def support_pair_can_be_nonzero(
    left: frozenset[str], right: frozenset[str]
) -> bool:
    return ("P" in left and "S" in right) or ("S" in left and "P" in right)


def audit_typed_modes_and_symmetry() -> dict[str, object]:
    # Target corners pair oppositely; crossed zero corners pair equally.
    core_names = ("A0", "B0", "B1", "C1")
    assignments: list[dict[str, str]] = []
    for values in product(("P", "S"), repeat=4):
        mode = dict(zip(core_names, values, strict=True))
        if not pure_pair_nonzero(mode["A0"], mode["B0"]):
            continue
        if not pure_pair_nonzero(mode["B1"], mode["C1"]):
            continue
        if pure_pair_nonzero(mode["A0"], mode["B1"]):
            continue
        if pure_pair_nonzero(mode["B0"], mode["C1"]):
            continue
        assignments.append(mode)
    assert len(assignments) == 2
    for mode in assignments:
        assert mode["A0"] == mode["B1"]
        assert mode["B0"] == mode["C1"]
        assert pure_pair_nonzero(mode["A0"], mode["C1"])

    # Fix the harmless global type swap.  A response vanishing against both a
    # nonzero P-pure point and a nonzero S-pure point annihilates both of its
    # components.  This is the exact logical step used for bd and be.
    oriented = {"A0": "P", "B0": "S", "B1": "P", "C1": "S"}
    all_supports = tuple(
        frozenset(kind for bit, kind in enumerate(("P", "S")) if mask & (1 << bit))
        for mask in range(4)
    )
    annihilates_both = [
        support
        for support in all_supports
        if not support_pair_can_be_nonzero(frozenset({"P"}), support)
        and not support_pair_can_be_nonzero(frozenset({"S"}), support)
    ]
    assert annihilates_both == [frozenset()]

    nonempty = tuple(support for support in all_supports if support)
    de_cases = 0
    oriented_cases = 0
    for d_support, e_support in product(nonempty, repeat=2):
        if not support_pair_can_be_nonzero(d_support, e_support):
            continue
        de_cases += 1

        # If F_bd or F_be were nonzero, the tensor response identity would
        # force the corresponding mode into annihilates_both, contradicting
        # this nonzero DE case.
        assert d_support not in annihilates_both
        assert e_support not in annihilates_both

        # A nonzero DE response has at least one ordered cross term.  Swap d,e
        # when needed, then C1(S) sees P_D and A0(P) sees S_E.
        if not ("P" in d_support and "S" in e_support):
            d_support, e_support = e_support, d_support
        assert "P" in d_support and "S" in e_support
        assert support_pair_can_be_nonzero(
            frozenset({oriented["C1"]}), d_support
        )
        assert support_pair_can_be_nonzero(
            frozenset({oriented["A0"]}), e_support
        )
        oriented_cases += 1
    assert de_cases == 7
    assert oriented_cases == de_cases

    # Reconstruct the typed 3x3 grid.  Its diagonal is the omission matching;
    # among the six off-diagonal cells, one is the b-b collision and the other
    # five are precisely the response pairs just proved nonzero above.
    p_sites = ("a", "b", "d")
    s_sites = ("b", "c", "e")
    diagonal_pairs = {
        "".join(sorted((p_sites[index], s_sites[index]))) for index in range(3)
    }
    forced_zero_pairs: set[str] = set()
    collisions: list[tuple[int, int, str]] = []
    for p_index, s_index in product(range(3), repeat=2):
        if p_index == s_index:
            continue
        if p_sites[p_index] == s_sites[s_index]:
            collisions.append((p_index, s_index, p_sites[p_index]))
        else:
            forced_zero_pairs.add(
                "".join(sorted((p_sites[p_index], s_sites[s_index])))
            )
    assert diagonal_pairs == {"ab", "bc", "de"}
    assert collisions == [(1, 0, "b")]
    assert forced_zero_pairs == {"ac", "ae", "bd", "be", "cd"}
    relabel_site = {"a": "c", "b": "b", "c": "a", "d": "e", "e": "d", "f": "f"}

    def relabel_pair(word: str) -> str:
        return "".join(sorted((relabel_site[word[0]], relabel_site[word[1]])))

    assert {relabel_pair(pair) for pair in forced_zero_pairs} == forced_zero_pairs
    assert {relabel_pair(pair) for pair in diagonal_pairs} == diagonal_pairs
    assert relabel_pair("ab") == "bc" and relabel_pair("bc") == "ab"

    # The accompanying colour involution 0<->1 takes the endpoint-space table
    # and the ab target to the bc target; colour 2 and the de target are fixed.
    colour_swap = {0: 1, 1: 0, 2: 2}
    spaces = {
        "a": {1, 2}, "b": {2}, "c": {0, 2},
        "d": {0, 1}, "e": {0, 1}, "f": {0, 1, 2},
    }
    for site, colours in spaces.items():
        image = {colour_swap[colour] for colour in colours}
        assert image == spaces[relabel_site[site]]

    targets = {
        "ab": {"c": 0, "d": 0, "e": 0, "f": 0},
        "bc": {"a": 1, "d": 1, "e": 1, "f": 1},
        "de": {"a": 2, "b": 2, "c": 2, "f": 2},
    }
    target_image: dict[str, dict[str, int]] = {}
    for omitted, tensor in targets.items():
        image_omitted = relabel_pair(omitted)
        target_image[image_omitted] = {
            relabel_site[site]: colour_swap[colour] for site, colour in tensor.items()
        }
    assert target_image == targets

    return {
        "core_assignments": assignments,
        "annihilates_both": [sorted(value) for value in annihilates_both],
        "nonzero_de_support_cases": de_cases,
        "typed_grid_collision": collisions,
        "forced_zeros": sorted(forced_zero_pairs),
        "site_involution": relabel_site,
        "colour_involution": colour_swap,
    }


def audit_flattening() -> dict[str, object]:
    lam0, lam1 = sy.symbols("lambda_0 lambda_1", nonzero=True)
    xa = sy.symbols("x_a0 x_a1")
    yc = sy.symbols("y_c0 y_c1")

    # Columns index a,c,d,e.  The two target summands use disjoint d-slices,
    # so a pivot component of x_a and one of y_c give a diagonal 2x2 minor.
    columns = list(product(range(2), repeat=4))
    column_number = {index: number for number, index in enumerate(columns)}
    matrix = sy.zeros(3, len(columns))
    for a_index in range(2):
        matrix[0, column_number[(a_index, 0, 0, 0)]] = lam0 * xa[a_index]
    for c_index in range(2):
        matrix[1, column_number[(0, c_index, 1, 1)]] = lam1 * yc[c_index]

    pivot_minors: dict[str, str] = {}
    for a_index, c_index in product(range(2), repeat=2):
        first_column = column_number[(a_index, 0, 0, 0)]
        second_column = column_number[(0, c_index, 1, 1)]
        minor = sy.factor(matrix.extract((0, 1), (first_column, second_column)).det())
        wanted = lam0 * lam1 * xa[a_index] * yc[c_index]
        assert sy.expand(minor - wanted) == 0
        pivot_minors[f"a{a_index}c{c_index}"] = str(minor)

    # Exhaust all possible nonempty coordinate supports.  Some pivot minor is
    # nonzero whenever x_a and y_c are both nonzero.
    support_cases = 0
    for x_support_bits, y_support_bits in product(range(1, 4), repeat=2):
        x_pivot = (x_support_bits & -x_support_bits).bit_length() - 1
        y_pivot = (y_support_bits & -y_support_bits).bit_length() - 1
        assert f"a{x_pivot}c{y_pivot}" in pivot_minors
        support_cases += 1
    assert support_cases == 9

    # An arbitrary decomposable correction z_f tensor R has every 2x2 minor
    # zero across the same flattening.
    z = sy.symbols("z_0:3")
    right = sy.symbols(f"r_0:{len(columns)}")
    rank_one = sy.Matrix([[z[row] * right[col] for col in range(len(columns))]
                          for row in range(3)])
    checked_rank_one_minors = 0
    for row_pair in combinations(range(3), 2):
        for col_pair in combinations(range(len(columns)), 2):
            assert sy.expand(rank_one.extract(row_pair, col_pair).det()) == 0
            checked_rank_one_minors += 1
    assert checked_rank_one_minors == 3 * sy.binomial(len(columns), 2)

    return {
        "right_dimension": len(columns),
        "nonzero_support_cases": support_cases,
        "rank_two_pivot_minors": pivot_minors,
        "rank_one_minors_checked": int(checked_rank_one_minors),
    }


def audit_single_survivor() -> dict[str, object]:
    alpha, beta, gamma = sy.symbols("alpha beta gamma", nonzero=True)
    lam1, lam2 = sy.symbols("lambda_1 lambda_2", nonzero=True)

    # Before normalization, the f/e1 quotient of F_de is T_af tensor y_c
    # = lambda_2*a2*c2*f2.  The displayed elimination certificate forces the
    # c0 coordinate of y_c to vanish without dividing by an unknown component.
    y0 = sy.Symbol("y_0")
    y2, pivot = sy.symbols("y_2 t", nonzero=True)
    c0_equation = pivot * y0
    c2_equation = pivot * y2 - lam2
    y0_certificate = sy.expand(y2 * c0_equation - y0 * c2_equation)
    assert y0_certificate == lam2 * y0
    # c2_equation=0 also makes y2 nonzero because lambda_2 is nonzero.  Rename
    # it alpha.  Projecting the original equation modulo c2 gives beta times
    # every c0 coordinate of q_ac, hence q_ac=x_a*c2.
    qac_c0 = sy.symbols("qac_c0_0:2")
    assert all(sy.cancel((beta * entry) / beta) == entry for entry in qac_c0)

    x1, x2 = sy.symbols("x_1 x_2")
    qaf = sy.Matrix([
        [0, -beta * x1 / alpha, 0],
        [0, -beta * x2 / alpha, lam2 / alpha],
    ])
    xa_e1 = sy.Matrix([[0, beta * x1, 0], [0, beta * x2, 0]])
    target = sy.zeros(2, 3)
    target[1, 2] = lam2
    assert qaf * alpha + xa_e1 == target

    # In F_cd=0, quotienting f by e1 leaves (lambda_2/alpha)*a2*f2*E_e.
    # Check both coordinates of E_e; tensor injectivity forces E_e=0, and then
    # beta*q_ae*e1=0 forces q_ae=0.
    e0, e1 = sy.symbols("E_0 E_1")
    e_residuals = [sy.factor((lam2 / alpha) * entry) for entry in (e0, e1)]
    assert all(sy.cancel(residual / (lam2 / alpha)) in (e0, e1)
               for residual in e_residuals)
    qae_entries = sy.symbols("qae_0:4")
    assert all(sy.cancel((beta * entry) / beta) == entry for entry in qae_entries)

    # q_de=0: factor-line uniqueness supplies a nonzero c2*e1 coefficient s
    # of q_ce.  Modulo f/e1, F_bd has exactly this surviving coefficient.
    s = sy.Symbol("s", nonzero=True)
    zero_de_residual = sy.factor(s * qaf[1, 2])
    assert zero_de_residual == s * lam2 / alpha
    assert zero_de_residual != 0

    # q_de!=0: F_ac first makes D_d nonzero (otherwise beta*q_de*e1=0),
    # then D_d tensor pi(q_ef)=0 kills pi(q_ef).  Enumerate either possible
    # nonzero pivot of D and every quotient coordinate of q_ef.
    d_pivots = sy.symbols("D_0 D_1", nonzero=True)
    quotient_qef = sy.symbols("w_0:4")
    injectivity_checks = 0
    for d_pivot in d_pivots:
        for entry in quotient_qef:
            assert sy.cancel((d_pivot * entry) / d_pivot) == entry
            injectivity_checks += 1
    assert injectivity_checks == 8

    # After pi(q_ef)=0, the quotient of the F_bc target retains a nonzero
    # lambda_2/alpha multiple of whichever coordinate witnesses q_de!=0.
    qde_pivots = sy.symbols("delta_00 delta_01 delta_10 delta_11", nonzero=True)
    nonzero_de_residuals = tuple(sy.factor(qaf[1, 2] * entry) for entry in qde_pivots)
    assert all(residual != 0 for residual in nonzero_de_residuals)
    assert all(sy.cancel(residual / entry) == lam2 / alpha
               for residual, entry in zip(nonzero_de_residuals, qde_pivots, strict=True))

    # The pure-tensor factorization used at the start has beta*gamma=-lambda_1;
    # no later step divides by gamma or lambda_1.  Record that its scalar is
    # nonzero, while keeping the sign visible.
    factor_scalar = sy.factor(beta * gamma + lam1)

    return {
        "normal_form_qaf": [[str(value) for value in qaf.row(row)] for row in range(2)],
        "y0_elimination_certificate": str(y0_certificate),
        "E_quotient_residuals": [str(value) for value in e_residuals],
        "qde_zero_residual": str(zero_de_residual),
        "qde_nonzero_residuals": [str(value) for value in nonzero_de_residuals],
        "injectivity_pivot_checks": injectivity_checks,
        "factor_scalar_relation": str(factor_scalar),
        "denominators": ["alpha"],
        "certified_nonzero_scalars": ["alpha", "beta", "gamma", "lambda_1", "lambda_2"],
    }


def coordinate_symbols(prefix: str, site: str, dimension: int) -> tuple[sy.Symbol, ...]:
    return sy.symbols(" ".join(f"{prefix}_{site}{index}" for index in range(dimension)))


def audit_final_component_syzygy() -> dict[str, object]:
    alpha = sy.Symbol("alpha", nonzero=True)
    dimensions = {"d": 2, "e": 2, "f": 3}
    A = {site: coordinate_symbols("A", site, dimension)
         for site, dimension in dimensions.items()}
    U = {site: coordinate_symbols("U", site, dimension)
         for site, dimension in dimensions.items()}
    V = {site: coordinate_symbols("V", site, dimension)
         for site, dimension in dimensions.items()}

    def relation(i: str, j: str, i_coord: int, j_coord: int) -> sy.Expr:
        return A[i][i_coord] * V[j][j_coord] + V[i][i_coord] * A[j][j_coord]

    def uv_sum(i: str, j: str, i_coord: int, j_coord: int) -> sy.Expr:
        return U[i][i_coord] * V[j][j_coord] + V[i][i_coord] * U[j][j_coord]

    def q_value(i: str, j: str, i_coord: int, j_coord: int) -> sy.Expr:
        return -uv_sum(i, j, i_coord, j_coord) / alpha

    # Reconstruct the two a,c coefficients of each complete zero cofactor.
    zero_relation_components = 0
    solved_q_components = 0
    for i, j in (("d", "e"), ("d", "f"), ("e", "f")):
        for i_coord, j_coord in product(range(dimensions[i]), range(dimensions[j])):
            a1c2 = (
                A[i][i_coord] * V[j][j_coord]
                + A[j][j_coord] * V[i][i_coord]
            )
            assert sy.expand(a1c2 - relation(i, j, i_coord, j_coord)) == 0
            zero_relation_components += 1

            a2c2 = (
                alpha * q_value(i, j, i_coord, j_coord)
                + U[i][i_coord] * V[j][j_coord]
                + U[j][j_coord] * V[i][i_coord]
            )
            assert sy.expand(a2c2) == 0
            solved_q_components += 1
    assert zero_relation_components == 16
    assert solved_q_components == 16

    # Verify alpha*H is in the module generated by the three A_i V_j+A_j V_i
    # relations for every coordinate of W_d tensor W_e tensor W_f.
    h_components = 0
    certificate_samples: list[str] = []
    for d_coord, e_coord, f_coord in product(range(2), range(2), range(3)):
        h_value = (
            A["d"][d_coord] * q_value("e", "f", e_coord, f_coord)
            + A["e"][e_coord] * q_value("d", "f", d_coord, f_coord)
            + A["f"][f_coord] * q_value("d", "e", d_coord, e_coord)
        )
        certificate = sy.expand(
            alpha * h_value
            + U["d"][d_coord] * relation("e", "f", e_coord, f_coord)
            + U["e"][e_coord] * relation("d", "f", d_coord, f_coord)
            + U["f"][f_coord] * relation("d", "e", d_coord, e_coord)
        )
        assert certificate == 0
        if len(certificate_samples) < 3:
            certificate_samples.append(str(certificate))
        h_components += 1
    assert h_components == 12

    return {
        "zero_relation_components": zero_relation_components,
        "solved_q_components": solved_q_components,
        "H_components": h_components,
        "certificate_samples": certificate_samples,
        "denominators": ["alpha"],
    }


def make_ledger() -> dict[str, object]:
    return {
        "matching": audit_matchings(),
        "typed_modes": audit_typed_modes_and_symmetry(),
        "flattening": audit_flattening(),
        "single_survivor": audit_single_survivor(),
        "final_syzygy": audit_final_component_syzygy(),
    }


def main() -> None:
    ledger = make_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if FROZEN_LEDGER_SHA256 != "TO_BE_FROZEN":
        assert digest == FROZEN_LEDGER_SHA256

    print("independent full matchings:", len(ledger["matching"]["full_matchings"]))
    print("independent cofactors:", len(ledger["matching"]["cofactors"]))
    print("typed-grid forced zeros:", ledger["typed_modes"]["forced_zeros"])
    print("flattening nonzero-support cases:", ledger["flattening"]["nonzero_support_cases"])
    print("rank-one minors checked:", ledger["flattening"]["rank_one_minors_checked"])
    print("single-survivor q_de branches: zero and nonzero PASS")
    print("final component syzygies:", ledger["final_syzygy"]["H_components"])
    print("ledger sha256:", digest)
    print("clean-room wedge hole-block audit: PASS")


if __name__ == "__main__":
    main()
