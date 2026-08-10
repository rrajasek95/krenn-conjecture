#!/usr/bin/env python3
"""Exact signed-cycle Fitting lemma at the curved OO global boundary.

For a cyclic two-class source module with rows

    f_i = u_i X_i + v_i X_(i+1),

the coefficient determinant is prod(u_i)+(-1)^(ell-1)prod(v_i).  If the
matching exponents close, both products are the same active monomial K.
Thus an odd plus-hafnian cycle has Fitting class 2K, while an even cycle has
zero Fitting class.  The dense curved packet from b942209 contains both a
nonzero three-cycle and a parallel two-row/even component.  Curvature,
goodness, activity, and alignment therefore do not determine cycle parity;
they only coexist with whichever global source circuit is present.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY_PATH = (
    "computations/verify_oo_curved_global_private_transport_boundary.py"
)
BOUNDARY_NOTE = "notes/oo-curved-global-private-transport-boundary.md"
SEGRE_PATH = "computations/verify_recombination_cube_segre_cancellation.py"
SEGRE_NOTE = "notes/recombination-cube-segre-cancellation.md"
PINS = {
    BOUNDARY_PATH:
        "9a4c6bd04ea8d0466efee9f5188c1ffa922ac82ec0187b3fc4213b355091c2c5",
    BOUNDARY_NOTE:
        "1256fcfd1df1316b6fb3af824bfdde202f8ccf05325c9337fe74780514853bd2",
    SEGRE_PATH:
        "b2e3bcfa8b4a7832b2db128f53cc524cb12c8aa87f0490e680f238757af81023",
    SEGRE_NOTE:
        "b758a8121a9bfc5e78ffe61d40a64b101d97ecf0e0fcd7138b75ec08995deb89",
}
EXPECTED_DIGEST = "cdb83f8b4d9faa1c7d75547d46416b115947336b234f9e6fab5161072b3cea5a"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"pinned dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


boundary = None
segre = None


def monomial_product(*monomials):
    return tuple(sorted(cell for monomial in monomials for cell in monomial))


def polynomial_add(*scaled):
    answer = defaultdict(Fraction)
    for scalar, polynomial in scaled:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += Fraction(scalar) * coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def polynomial_multiply(left, right):
    answer = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[monomial_product(left_monomial, right_monomial)] += (
                left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def determinant(matrix):
    """Leibniz determinant over sparse monomial polynomials."""
    size = len(matrix)
    require(size and all(len(row) == size for row in matrix),
            "Fitting matrix is not square")
    answer = {}

    def visit(row, used, inversions, product):
        nonlocal answer
        if row == size:
            sign = -1 if inversions % 2 else 1
            answer = polynomial_add((1, answer), (sign, product))
            return
        for column in range(size):
            if column in used or not matrix[row][column]:
                continue
            added_inversions = sum(previous > column for previous in used)
            visit(
                row + 1,
                used + (column,),
                inversions + added_inversions,
                polynomial_multiply(product, matrix[row][column]),
            )

    visit(0, (), 0, {(): Fraction(1)})
    return answer


def cyclic_matrix(u, v):
    require(len(u) == len(v) >= 2, "cyclic coefficient lengths")
    size = len(u)
    matrix = [[{} for _ in range(size)] for _ in range(size)]
    for row in range(size):
        matrix[row][row] = {u[row]: Fraction(1)}
        next_column = (row + 1) % size
        entry = {v[row]: Fraction(1)}
        matrix[row][next_column] = polynomial_add(
            (1, matrix[row][next_column]), (1, entry)
        )
    return matrix


def abstract_cycle_parity_audit():
    records = []
    for size in range(2, 10):
        # Use formal distinct one-letter coefficients, then impose exponent
        # balance only after the determinant signs have been audited.
        u = tuple((f"u{index}",) for index in range(size))
        v = tuple((f"v{index}",) for index in range(size))
        det = determinant(cyclic_matrix(u, v))
        up = monomial_product(*u)
        vp = monomial_product(*v)
        expected = {up: Fraction(1), vp: Fraction((-1) ** (size - 1))}
        require(det == expected,
                f"cyclic determinant sign changed in size {size}: {det}")
        balanced_coefficient = 1 + (-1) ** (size - 1)
        require(balanced_coefficient == (2 if size % 2 else 0),
                "cycle parity coefficient changed")
        records.append({
            "length": size,
            "determinant": "prod(u)+(-1)^(ell-1)*prod(v)",
            "balanced_Fitting_coefficient": balanced_coefficient,
            "saturated_unit": bool(balanced_coefficient),
        })
    return records


def actual_triangle_audit(blocks):
    terms = [boundary.fibre_terms(blocks, word)
             for word in boundary.TRIANGLE_WORDS]
    require(all(len(row) == 2 for row in terms),
            "actual odd triangle stopped being binomial")
    (A, B), (C, D), (E, Fm) = terms

    # Rows are written on three Laurent classes so that the two determinant
    # permutations are A*D*E and B*C*F.
    matrix = [
        [{A: Fraction(1)}, {B: Fraction(1)}, {}],
        [{}, {D: Fraction(1)}, {C: Fraction(1)}],
        [{Fm: Fraction(1)}, {}, {E: Fraction(1)}],
    ]
    det = determinant(matrix)
    Kleft = monomial_product(A, D, E)
    Kright = monomial_product(B, C, Fm)
    require(Kleft == Kright and det == {Kleft: Fraction(2)},
            "actual triangle Fitting class stopped being 2K")
    require(all(
        word[boundary.base.P] != word[boundary.base.Q]
        and word[boundary.base.P] != word[boundary.base.R]
        for word in boundary.TRIANGLE_WORDS
    ), "odd triangle left the doubly off-diagonal source sector")
    return {
        "source_words": ["".join(map(str, word))
                         for word in boundary.TRIANGLE_WORDS],
        "endpoint_sector": "offdiagonal in both pq and pr charts",
        "Fitting_matrix_size": 3,
        "Fitting_determinant": "2*K",
        "active_K_degree": len(Kleft),
        "coefficient_independent_under_nonzero_cell_rescaling": True,
    }


def even_parallel_counterguard(blocks):
    first_word = tuple(map(int, "20120121"))
    second_word = tuple(map(int, "21120121"))
    first = boundary.fibre_terms(blocks, first_word)
    second = boundary.fibre_terms(blocks, second_word)
    require(len(first) == len(second) == 2,
            "parallel even component stopped being binomial")
    A, B = first
    C, D = second

    # The two rows have different active common factors but the same two
    # core matching classes.  Algebraically A/B=C/D, so their 2x2 Fitting
    # determinant vanishes identically.
    require(monomial_product(A, D) == monomial_product(B, C),
            "parallel binomial ratios stopped agreeing")
    matrix = [
        [{A: Fraction(1)}, {B: Fraction(1)}],
        [{C: Fraction(1)}, {D: Fraction(1)}],
    ]
    det = determinant(matrix)
    require(not det, "even/parallel Fitting counterguard became nonzero")

    # It lives in exactly the same numeric packet as the odd triangle, so
    # all curved OO local invariants are literally identical rather than
    # merely isomorphic.
    local = boundary.local_structure_audit(blocks)
    require(local["curvature"] == "-1"
            and local["good_star_ranks"] == [3, 3, 3, 3]
            and local["arm_cofactors_support_active"] == [True, True],
            "even counterguard lost the local OO packet")
    return {
        "source_words": ["20120121", "21120121"],
        "ratio_identity": "A/B=C/D",
        "Fitting_matrix_size": 2,
        "Fitting_determinant": "0",
        "same_local_packet_as_odd_triangle": True,
        "curvature": local["curvature"],
        "good_star_ranks": local["good_star_ranks"],
        "both_arms_active": local["arm_cofactors_support_active"],
    }


def segre_fitting_comparison():
    """Compare the exact mate-sum Segre theorem with the OO Fitting gate."""
    abstract = segre.abstract_segre_lemma()
    require(abstract["all_forced_alternate_entries_nonzero"]
            and abstract["flattening_minors_checked"] == 112,
            "pinned dense-Segre cancellation theorem changed")

    # Exact mixed-row cancellation makes every recombination-mate
    # flattening rank one.  Thus it supplies zero, rather than the nonzero
    # minor that would be needed to deduce a critical Fitting unit directly
    # from a local RR ledger.  A nonzero class can only come from signed
    # cycle holonomy between several such rows, as in the odd triangle.
    return {
        "exact_mate_sum_condition": "dense Segre tensor",
        "flattening_minors_checked": abstract["flattening_minors_checked"],
        "all_flattening_minors": "0",
        "relation_to_RR": (
            "RR curvature/goodness/activity do not turn a Segre minor "
            "nonzero; the same local packet has the explicit zero 2x2 "
            "Fitting rectangle"
        ),
        "needed_extra_datum": (
            "a source-labelled odd or nontrivial-character cycle among "
            "mate-sum classes, not a local flattening minor"
        ),
    }


def main():
    global boundary, segre
    boundary = load_pinned("oo_global_private_boundary", BOUNDARY_PATH)
    segre = load_pinned("recombination_segre", SEGRE_PATH)
    require(sha256((ROOT / BOUNDARY_NOTE).read_bytes()).hexdigest()
            == PINS[BOUNDARY_NOTE], "global-boundary note changed")
    require(sha256((ROOT / SEGRE_NOTE).read_bytes()).hexdigest()
            == PINS[SEGRE_NOTE], "recombination-Segre note changed")
    blocks = boundary.build_packet()
    parity = abstract_cycle_parity_audit()
    triangle = actual_triangle_audit(blocks)
    even = even_parallel_counterguard(blocks)
    segre_comparison = segre_fitting_comparison()
    ledger = {
        "pins": PINS,
        "uniform_signed_cycle_lemma": parity,
        "smallest_nonzero_balanced_plus_SCC": triangle,
        "sharp_even_counterguard": even,
        "dense_Segre_mate_sum_comparison": segre_comparison,
        "verdict": (
            "an odd balanced plus-hafnian SCC automatically has nonzero "
            "Fitting class 2K, but curvedness, goodness, activity, and "
            "alignment do not force SCC parity: the same physical packet "
            "contains a zero-Fitting even/parallel component"
        ),
        "remaining_uniform_lemma": (
            "after all private/unit pivots, every reachable critical SCC "
            "contains an odd cycle or a coefficient character with nonzero "
            "cycle determinant; local OO data alone do not imply this"
        ),
        "scope": (
            "uniform cycle determinant theorem plus exact same-packet "
            "structural counterguard; not arbitrary-packet saturation"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    require(EXPECTED_DIGEST != "TO_BE_FILLED", "pin EXPECTED_DIGEST")
    require(digest == EXPECTED_DIGEST, ("ledger digest changed", digest))
    print("curved OO signed-cycle Fitting lemma: PASS")
    print("balanced odd SCC: det=2K; balanced even SCC: det=0")
    print("actual 3-word offdiagonal triangle: nonzero Fitting class")
    print("same curved packet has a parallel 2-word zero-Fitting component")
    print("exact recombination mate sums: Segre, so every flattening minor is zero")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
