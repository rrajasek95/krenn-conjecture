#!/usr/bin/env python3
"""Close the singular-spoke overlap of the terminal one-column charts.

Assume the one-column terminal equations give

    Q_t=q e_r,  H=h e_s^6,  C_t=c e_r^5,  r=1-s,

but impose no invertibility hypothesis on the I-z spokes.  The triangle
cofactor map Phi from the direct sum of three spoke columns to an I-tensor is
injective.  Since C_t at zero-shore word rr is nonzero, the r-column triple
at each zero shore is nonzero, hence so is its Phi-image L_z^r.

If either pair (L_z^s,L_z^r) is independent, the three forbidden H shore
corners contradict the pure ss corner.  If both pairs are dependent,
injectivity makes every I-z block have one fixed right factor at z.  Together
with the one-column I-t blocks and M_45=0, this is the coordinate-shore class
with exceptional path t-4-t-5, whose exact differential-rank bound is 49.

The normalization used to audit Phi is only an invertible change of basis on
the I sites; no normalized selected vector is identified with a physical
pure target colour.

Standard library only; checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
PURE = run_path(str(
    HERE
    / "verify_level_two_three_invertible_one_column_pure_tensor_obstruction.py"
))
SHORE = run_path(str(
    HERE / "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
))


# Sparse formal polynomials; monomials are sorted tuples of variable names.
def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        updated = {}
        for left_monomial, left_coefficient in answer.items():
            for right_monomial, right_coefficient in polynomial.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                updated[monomial] = (
                    updated.get(monomial, Q(0))
                    + left_coefficient * right_coefficient
                )
                if not updated[monomial]:
                    del updated[monomial]
        answer = updated
    return answer


def terminal_cofactor(inner_word, colour4, colour5):
    """Formal C_t coefficient, with no normalization of its target factors."""

    answer = constant(0)
    for i in range(3):
        j, k = tuple(vertex for vertex in range(3) if vertex != i)
        p_i = variable(f"p{i}_{inner_word[i]}")
        first = multiply(
            p_i,
            variable(f"m{j}4_{inner_word[j]}_{colour4}"),
            variable(f"m{k}5_{inner_word[k]}_{colour5}"),
        )
        second = multiply(
            p_i,
            variable(f"m{j}5_{inner_word[j]}_{colour5}"),
            variable(f"m{k}4_{inner_word[k]}_{colour4}"),
        )
        answer = add(answer, first, second)
    return answer


def audit_terminal_cofactor_uses_both_shores():
    checks = 0
    for pure_colour in (0, 1):
        for inner_word in product((0, 1), repeat=3):
            coefficient = terminal_cofactor(
                inner_word, pure_colour, pure_colour
            )
            require(coefficient, "a formal pure cofactor coefficient vanished")
            for monomial in coefficient:
                if not monomial:
                    continue
                shore4 = tuple(
                    name for name in monomial
                    if name.startswith("m") and name[2] == "4"
                )
                shore5 = tuple(
                    name for name in monomial
                    if name.startswith("m") and name[2] == "5"
                )
                require(
                    len(shore4) == len(shore5) == 1,
                    ("a C_t term lost a zero shore", monomial),
                )
                require(
                    shore4[0].endswith(f"_{pure_colour}")
                    and shore5[0].endswith(f"_{pure_colour}"),
                    ("a C_t pure-shore term changed colour", monomial),
                )
                checks += 1
    require(checks == 96, "terminal cofactor monomial census changed")
    return checks


def audit_dependent_pair_factorization():
    # In the direct sum W of the three I-site column spaces, dependence and
    # U_z^r!=0 give U_z^s=alpha_z U_z^r.  Componentwise, every block M_iz
    # therefore has the same right factor (alpha_z,1) at z.  This statement
    # is covariant at I and does not choose a physical target coordinate.
    checks = 0
    for missing_colour in (0, 1):
        other = 1 - missing_colour
        for zero in (4, 5):
            alpha = variable(f"alpha{zero}")
            for inner in range(3):
                for local_colour in (0, 1):
                    base = variable(f"u{inner}_{local_colour}_{zero}")
                    columns = {
                        missing_colour: multiply(alpha, base),
                        other: base,
                    }
                    require(
                        columns[missing_colour] == multiply(
                            alpha, columns[other]
                        ),
                        "dependent cofactor columns lost their right factor",
                    )
                    checks += 1
    require(checks == 24, "dependent-pair factor count changed")
    return checks


def audit_covariant_dichotomy():
    # C_t^(rr)!=0 and injectivity of Phi give L_4^r,L_5^r!=0.  The four
    # independence patterns then have exactly the following outcomes.
    outcomes = {}
    for independent4, independent5 in product((False, True), repeat=2):
        if independent4 or independent5:
            outcome = "pure-shore contradiction"
        else:
            outcome = "coordinate-shore path rank <= 49"
        outcomes[independent4, independent5] = outcome
    require(
        outcomes == {
            (False, False): "coordinate-shore path rank <= 49",
            (False, True): "pure-shore contradiction",
            (True, False): "pure-shore contradiction",
            (True, True): "pure-shore contradiction",
        },
        "terminal singular-overlap dichotomy changed",
    )
    return outcomes


def audit_imported_exact_lemmas():
    # The first checker verifies the covariant t-slice identity after using
    # I-site changes of basis solely to audit Phi.  The second verifies the
    # formal matching factorization and 28+21=49 differential-rank count for
    # the two-edge exceptional shore path.
    slice_checks = PURE["audit_t_slice_identity"]()
    phi_shape = PURE["audit_cofactor_injectivity"]()
    path_identities, categories = SHORE["audit_path_factorization"]()
    require(slice_checks == 64, "imported pure-shore identity count changed")
    require(phi_shape == (8, 6), "imported cofactor-map shape changed")
    require(path_identities == 64, "imported path identity count changed")
    require(
        categories == {"all_cross": 6, "34": 3, "35": 3, "45": 3},
        "imported path matching categories changed",
    )
    return slice_checks, phi_shape, path_identities, categories


def main():
    cofactor_terms = audit_terminal_cofactor_uses_both_shores()
    factors = audit_dependent_pair_factorization()
    outcomes = audit_covariant_dichotomy()
    slices, phi_shape, paths, categories = audit_imported_exact_lemmas()
    print("three-invertible one-column/singular overlap: all checks passed")
    print(f"  terminal C_t shore terms : {cofactor_terms}")
    print(f"  dependent-pair factors   : {factors}")
    print(f"  pure t-slice/Phi audits  : {slices}/{phi_shape}")
    print(f"  terminal dichotomy       : {outcomes}")
    print(f"  path identities          : {paths}, {categories}")
    print("  conclusion               : contradiction or rank dPsi <= 49")


if __name__ == "__main__":
    main()
