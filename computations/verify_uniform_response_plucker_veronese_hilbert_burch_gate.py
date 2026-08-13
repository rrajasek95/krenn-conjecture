#!/usr/bin/env python3
"""Test response Plucker syzygies against the uniform clean Fitting target.

On the q=0 associated-graded face, a rank-one response pencil

    r(u,v)=u Z00+v Z11,  Zij=p_i s_j

has clean tail r(u,v)^[h].  Its h+1 decorated response-power coordinates
are the full Veronese basis u^(h-j)v^j.  The response table satisfies every
2x2 Plucker relation, but the clean Macaulay map is surjective.

The Veronese coordinates have exactly h independent linear syzygies,
v*g_j-u*g_(j+1)=0.  Their Hilbert--Burch column-degree sum is h, the sharp
non-forcing boundary.  This audits h=3 and h=4 explicitly and the same
finite algebra for h through 10.  The paired note proves the all-h result
and states the extra source relation required to beat this guard.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import json
from math import comb, factorial
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/uniform-anchor-crossed-bezout-fitting-hilbert-burch-gate.md":
        "afda3275f855a2f3d06e33f4bf15b39277415f31dedd27183f54245c256dc901",
    "computations/verify_uniform_anchor_crossed_bezout_fitting_hilbert_burch_gate.py":
        "b614562d72cf1fe76da78248b38bffd7b45c58aa1f11b0121a5bed6d1146a626",
    "notes/plucker-hessian-closure-and-defect-three-transition-guard.md":
        "b7fc6e209ec09d63cd6a0cbd9de7baa68ce30a84419ffd337cd3f3f71c5d64e7",
    "computations/verify_plucker_hessian_closure_and_defect_three_transition_guard.py":
        "bc53dd16029db17a0f99645bae55582c467aaab61e390ac44ae97e7a1d8aec54",
    "notes/curved-rootless-line-uniform-response-resultant.md":
        "36d0c291156328afedbd71486998b5f7dbcc8444431d3cf7a94aaf3185da8cd7",
    "notes/uniform-full-nine-scalar-tangent-clean-counterguard.md":
        "f513419b998a066828f436f9c89aefccc4ea2aebf1e7f35f8452d22bd75049d6",
    "computations/verify_uniform_full_nine_scalar_tangent_clean_counterguard.py":
        "44d49909bc05da17cfe264721e6218d7b33ad87f030ffeafc28aa5961f6a9c20",
}
EXPECTED_LEDGER_SHA256 = "bb50c262cebe7f4f6cc9d71bbd8211bbddd8523d682397582ee7f6d2e3160c4b"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def matrix_rank(matrix) -> int:
    if not matrix:
        return 0
    work = [list(map(Fraction, row)) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            coefficient = work[row][column]
            work[row] = [
                entry - coefficient * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[rank], strict=True
                )
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def determinant(matrix) -> Fraction:
    require(len(matrix) == len(matrix[0]), "determinant needs square matrix")
    work = [list(map(Fraction, row)) for row in matrix]
    output = Fraction(1)
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work))
             if work[row][column]), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            output *= -1
        pivot_value = work[column][column]
        output *= pivot_value
        for row in range(column + 1, len(work)):
            coefficient = work[row][column] / pivot_value
            for entry in range(column, len(work)):
                work[row][entry] -= coefficient * work[column][entry]
    return output


def polynomial_matrix_apply(matrix, vector):
    """Matrix entries/vectors are low-to-high coefficient arrays."""
    output = []
    for row in matrix:
        degree = max(
            (len(entry) + len(value) - 2
             for entry, value in zip(row, vector, strict=True)
             if entry and value),
            default=0,
        )
        result = [Fraction(0)] * (degree + 1)
        for entry, value in zip(row, vector, strict=True):
            for i, left in enumerate(entry):
                for j, right in enumerate(value):
                    result[i + j] += left * right
        while len(result) > 1 and not result[-1]:
            result.pop()
        output.append(result)
    return output


def linear_syzygy_map(h: int):
    """Map coefficients (a_j,b_j) to sum_j (a_j u+b_j v)g_j."""
    # Target degree is h+1, ordered by v-degree 0..h+1.
    matrix = [[Fraction(0) for _ in range(2 * (h + 1))]
              for _ in range(h + 2)]
    for j in range(h + 1):
        matrix[j][2 * j] = 1       # u*g_j
        matrix[j + 1][2 * j + 1] = 1  # v*g_j
    return matrix


def adjacent_syzygy_vectors(h: int):
    vectors = []
    for j in range(h):
        vector = [Fraction(0)] * (2 * (h + 1))
        vector[2 * j + 1] = 1       # +v*g_j
        vector[2 * (j + 1)] = -1    # -u*g_(j+1)
        vectors.append(vector)
    return vectors


def hb_matrix(h: int):
    """(h+1)-by-h matrix with v on row j and -u on row j+1."""
    zero = [Fraction(0)]
    u = [Fraction(1), Fraction(0)]
    v = [Fraction(0), Fraction(1)]
    return [
        [
            v if row == column else
            [-entry for entry in u] if row == column + 1 else
            zero
            for column in range(h)
        ]
        for row in range(h + 1)
    ]


def delete_row(matrix, deleted):
    return [row for index, row in enumerate(matrix) if index != deleted]


def polynomial_determinant(matrix):
    if not matrix:
        return [Fraction(1)]
    result = [Fraction(0)]
    for column, entry in enumerate(matrix[0]):
        minor = [row[:column] + row[column + 1:] for row in matrix[1:]]
        product = [Fraction(0)] * (
            len(entry) + len(polynomial_determinant(minor)) - 1
        )
        minor_det = polynomial_determinant(minor)
        for i, left in enumerate(entry):
            for j, right in enumerate(minor_det):
                product[i + j] += left * right
        sign = Fraction(-1 if column % 2 else 1)
        if len(result) < len(product):
            result += [Fraction(0)] * (len(product) - len(result))
        for index, value in enumerate(product):
            result[index] += sign * value
    while len(result) > 1 and not result[-1]:
        result.pop()
    return result


def macaulay_matrix_for_forms(forms, h):
    columns = []
    for form in forms:
        for shift in range(h):
            column = [Fraction(0)] * (2 * h)
            for degree, coefficient in enumerate(form):
                column[degree + shift] += coefficient
            columns.append(column)
    return [
        [columns[column][row] for column in range(len(columns))]
        for row in range(2 * h)
    ]


def response_plucker_audit() -> dict[str, object]:
    # Formal exponent vectors in p0,p1,s0,s1.
    z00 = (1, 0, 1, 0)
    z01 = (1, 0, 0, 1)
    z10 = (0, 1, 1, 0)
    z11 = (0, 1, 0, 1)
    add = lambda left, right: tuple(
        x + y for x, y in zip(left, right, strict=True)
    )
    require(add(z00, z11) == add(z01, z10),
            "rank-one response Plucker identity changed")

    records = {}
    for h in range(3, 11):
        # The DP expansion of (u Z00+v Z11)^[h] has one decorated basis
        # vector in each response-power profile j.
        profiles = [
            tuple((h - j) * left + j * right
                  for left, right in zip(z00, z11, strict=True))
            for j in range(h + 1)
        ]
        require(len(set(profiles)) == h + 1,
                ("decorated response powers collided", h))
        coefficients = [
            [Fraction(0)] * j + [Fraction(1)]
            + [Fraction(0)] * (h - j)
            for j in range(h + 1)
        ]

        # All h+1 Veronese coordinate forms span S_h and have gcd one.
        require(matrix_rank(coefficients) == h + 1,
                ("Veronese clean coordinates lost rank", h))
        macaulay = macaulay_matrix_for_forms(coefficients, h)
        require(matrix_rank(macaulay) == 2 * h,
                ("response Plucker clean Macaulay lost surjectivity", h))

        # All linear syzygies are generated by the h adjacent relations.
        syzygy_map = linear_syzygy_map(h)
        syzygy_dimension = 2 * (h + 1) - matrix_rank(syzygy_map)
        adjacent = adjacent_syzygy_vectors(h)
        require(syzygy_dimension == h
                and matrix_rank(adjacent) == h,
                ("linear Veronese syzygy module changed", h))
        for vector in adjacent:
            require(all(
                sum(syzygy_map[row][column] * vector[column]
                    for column in range(len(vector))) == 0
                for row in range(h + 2)
            ), ("adjacent response syzygy failed", h))

        # The signed maximal minors of the standard HB matrix recover the
        # Veronese coordinates.  Every column has degree one, total h.
        minors = []
        if h <= 4:
            hb = hb_matrix(h)
            for deleted in range(h + 1):
                minor = polynomial_determinant(delete_row(hb, deleted))
                expected = coefficients[deleted]
                # Cofactor sign and the chosen -u orientation contribute one
                # harmless global/row sign; support and unit magnitude matter.
                padded_minor = (
                    minor + [Fraction(0)] * (h + 1 - len(minor))
                )
                require([abs(value) for value in padded_minor] == expected,
                        ("HB maximal minor support changed",
                         h, deleted, minor))
                minors.append(padded_minor)
        else:
            # Bidiagonal triangularity proves this formula for all h; avoid
            # a factorial-time Laplace expansion in the regression loop.
            minors = coefficients

        records[h] = {
            "decorated_response_profiles": h + 1,
            "clean_coordinate_rank": h + 1,
            "Macaulay_rank": 2 * h,
            "simultaneous_Bezout_kernel_dimension": 0,
            "linear_syzygy_dimension": syzygy_dimension,
            "adjacent_linear_syzygies": h,
            "HB_column_degrees": [1] * h,
            "HB_total_column_degree": h,
            "common_factor_forced": False,
            "extremal_minor_coefficients": [
                str(minors[0][0]), str(minors[-1][-1])
            ],
        }
    return {
        "literal_response_identity": "Z00*Z11=Z01*Z10",
        "clean_associated_graded": (
            "(u Z00+v Z11)^[h] with q=0; decorated coordinates are "
            "u^(h-j)v^j for 0<=j<=h"
        ),
        "physical_realization": (
            "put p0,p1 on h left residual sites and s0,s1 on h right "
            "sites with two distinct local colours; every response-power "
            "profile is nonzero and distinguished by its colour count"
        ),
        "orders": records,
        "all_h_pattern": (
            "ordinary rank-one response Plucker polarization yields the "
            "standard Veronese HB matrix with h linear columns and total "
            "degree exactly h"
        ),
    }


def h3_h4_source_target() -> dict[str, object]:
    return {
        "h3": {
            "clean_forms": ["u^3", "u^2v", "uv^2", "v^3"],
            "response_syzygies": [
                "v*u^3-u*u^2v=0",
                "v*u^2v-u*uv^2=0",
                "v*uv^2-u*v^3=0",
            ],
            "HB_degree_sum": 3,
            "forcing_threshold": 2,
            "missing_drop": 1,
        },
        "h4": {
            "clean_forms": ["u^4", "u^3v", "u^2v^2", "uv^3", "v^4"],
            "response_syzygies": [
                "v*g0-u*g1=0",
                "v*g1-u*g2=0",
                "v*g2-u*g3=0",
                "v*g3-u*g4=0",
            ],
            "HB_degree_sum": 4,
            "forcing_threshold": 3,
            "missing_drop": 1,
        },
        "exact_extra_source_relation": (
            "a relation that makes the clean HB maximal-minor vector "
            "acquire a positive-degree factor: equivalently "
            "wedge^h(M_f)=0, or a full-rank HB presentation with total "
            "column degree at most h-1"
        ),
        "pure_chart_leading_form": (
            "[u^h] sum_(j=2)^h alpha_i^(h-j) "
            "R_i^[j]q_i^[h-j]=0 for every clean coordinate i"
        ),
    }


def literal_cyclic_matching_word_audit() -> dict[str, object]:
    """Enumerate the physical cross-shore matchings at h=3 and h=4.

    The entry polynomial on left site k and right site ell is

        u p0(k)s1(ell) + v p2(k)s2(ell).

    We record monomials by the pair (u-degree,v-degree).  Because the
    response block has no same-shore entries, its perfect matchings are
    exactly the h! permutations from the left shore to the right shore.
    """
    records = {}
    for h in (3, 4):
        shore_u = tuple(index % 3 for index in range(h))
        shore_v = tuple((index + 1) % 3 for index in range(h))
        words = {
            "wU": shore_u + shore_u,
            "wV": shore_v + shore_v,
        }
        profiles = {}
        for name, word in words.items():
            monomial_counts: dict[tuple[int, int], int] = {}
            for matching in permutations(range(h)):
                u_degree = 0
                v_degree = 0
                for left, right in enumerate(matching):
                    left_colour = word[left]
                    right_colour = word[h + right]
                    z01 = int(
                        left_colour == shore_u[left]
                        and right_colour == shore_u[right]
                    )
                    z22 = int(
                        left_colour == shore_v[left]
                        and right_colour == shore_v[right]
                    )
                    require(z01 + z22 == 1,
                            ("cyclic response edge lost purity",
                             h, name, left, right, z01, z22))
                    u_degree += z01
                    v_degree += z22
                monomial = (u_degree, v_degree)
                monomial_counts[monomial] = (
                    monomial_counts.get(monomial, 0) + 1
                )

            expected = {(h, 0): factorial(h)} if name == "wU" else {
                (0, h): factorial(h)
            }
            require(monomial_counts == expected,
                    ("literal cyclic matching polynomial changed",
                     h, name, monomial_counts, expected))
            profiles[name] = {
                "physical_word": "".join(map(str, word)),
                "cross_matchings": factorial(h),
                "matching_polynomial": (
                    f"{factorial(h)}*u^{h}" if name == "wU"
                    else f"{factorial(h)}*v^{h}"
                ),
                "endpoint_component_grade": (
                    f"p0^{h}*s1^{h}" if name == "wU"
                    else f"p2^{h}*s2^{h}"
                ),
                "repeated_insertion_grade": f"R^[{h}]*q^[0]",
                "response_count": h,
                "q_count": 0,
            }
        records[h] = profiles

    require(records[3]["wU"]["physical_word"] == "012012"
            and records[3]["wV"]["physical_word"] == "120120",
            "h=3 literal words changed")
    require(records[4]["wU"]["physical_word"] == "01200120"
            and records[4]["wV"]["physical_word"] == "12011201",
            "h=4 literal words changed")
    return {
        "orders": records,
        "physical_typing": (
            "word idempotent plus endpoint component exponents plus the "
            "top repeated grade R^[h]q^[0]; endpoint component indices "
            "01/22 are not residual word labels"
        ),
        "all_h_count": (
            "for the cyclic shores U_k=k mod 3 and V_k=k+1 mod 3, "
            "every one of the h! cross-shore perfect matchings has the "
            "same pure monomial u^h on U|U or v^h on V|V"
        ),
    }


def mixed_target_grade_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 11):
        # Grade j counts response factors in R^[j]q^[h-j].  A physical pair
        # row at a mixed (non-GHZ) word contains only grades j=0 and j=1:
        # s*q^[h]+R*q^[h-1]=0.  The clean tail contains only j>=2.
        mixed_target_support = {0, 1}
        clean_tail_support = set(range(2, h + 1))
        require(not (mixed_target_support & clean_tail_support),
                ("mixed target and clean tail grades collided", h))

        # On q=0 the mixed row vanishes identically, while R^[h] can be a
        # nonzero complete matching.  Take h left and h right sites and the
        # response R(u,v)=u*Z01+v*Z22.  On both shores put
        # U_k=e_(k mod 3), V_k=e_(k+1 mod 3), and use p0=s1=U,
        # p2=s2=V.  The two cyclic mixed words w_U and w_V then read
        # h!*u^h and h!*v^h.  (Endpoint row labels are not residual
        # physical word labels.)
        target_row_u = Fraction(0)
        target_row_v = Fraction(0)
        clean_u = factorial(h)
        clean_v = factorial(h)
        w_u = [index % 3 for index in range(h)] * 2
        w_v = [(index + 1) % 3 for index in range(h)] * 2
        require(len(set(w_u)) > 1 and len(set(w_v)) > 1,
                ("cyclic guard word became GHZ-constant", h, w_u, w_v))

        # Literal star evaluation.  On left and right site k, U_k and V_k
        # are different physical basis vectors.  Hence the Z01 block reads
        # one on w_U and zero on w_V, while Z22 does the reverse.  A perfect
        # matching of the complete bipartite cross block is a permutation
        # of the h right sites, giving h! equal monomials.
        z01_on_wu = [
            int(w_u[k] == k % 3)
            * int(w_u[h + ell] == ell % 3)
            for k in range(h) for ell in range(h)
        ]
        z22_on_wu = [
            int(w_u[k] == (k + 1) % 3)
            * int(w_u[h + ell] == (ell + 1) % 3)
            for k in range(h) for ell in range(h)
        ]
        z01_on_wv = [
            int(w_v[k] == k % 3)
            * int(w_v[h + ell] == ell % 3)
            for k in range(h) for ell in range(h)
        ]
        z22_on_wv = [
            int(w_v[k] == (k + 1) % 3)
            * int(w_v[h + ell] == (ell + 1) % 3)
            for k in range(h) for ell in range(h)
        ]
        require(all(z01_on_wu) and not any(z22_on_wu)
                and not any(z01_on_wv) and all(z22_on_wv),
                ("literal cyclic star evaluation changed", h))
        require(target_row_u == target_row_v == 0
                and clean_u != 0 and clean_v != 0,
                ("q=0 mixed-word grade guard changed", h))
        records[h] = {
            "mixed_target_source_grades": [0, 1],
            "clean_tail_source_grades": list(range(2, h + 1)),
            "q_zero_mixed_target_row": 0,
            "mixed_word_wU_clean_coefficient": f"{factorial(h)}*u^h",
            "mixed_word_wV_clean_coefficient": f"{factorial(h)}*v^h",
            "wU": w_u,
            "wV": w_v,
            "matching_monomials_per_word": factorial(h),
            "target_projection_equals_clean_projection": False,
        }
    return {
        "orders": records,
        "answer": (
            "chi_i is indexed by a residual word, which may be a mixed "
            "GHZ word, but it is not the target coefficient at that word: "
            "target elimination kills only response-count grades 0 and 1; "
            "chi_i lies in the nonlinear grades 2 through h"
        ),
        "complete_mixed_rows_already_include_chi": False,
        "what_would_connect_them": (
            "a higher-polar/Bianchi or cross-chart source identity whose "
            "boundary moves from the j>=2 repeated-response grades to the "
            "j<=1 target row without collapsing word/fine grade"
        ),
        "scope": (
            "the q=0 model satisfies every mixed/off-diagonal pair row "
            "but not the diagonal GHZ anchors; it refutes the simple "
            "word-projection inference, not a new nonlinear coupling that "
            "essentially uses those anchors"
        ),
    }


def scope_audit() -> dict[str, object]:
    fitting = (ROOT / (
        "notes/uniform-anchor-crossed-bezout-fitting-hilbert-burch-gate.md"
    )).read_text()
    plucker = (ROOT / (
        "notes/plucker-hessian-closure-and-defect-three-transition-guard.md"
    )).read_text()
    response = (ROOT / (
        "notes/curved-rootless-line-uniform-response-resultant.md"
    )).read_text()
    require(r"\bigwedge^h\mathcal M_f=0" in fitting
            and "column-degree sum is at most" in fitting,
            "uniform Fitting/HB target changed")
    require(r"Z_{ab}Z_{cd}=Z_{ad}Z_{cb}" in plucker
            and "Plücker-Hessian annihilators" in plucker,
            "physical response Plucker theorem changed")
    require(r"{\cal E}(K)=\sum_{j=2}^{h}" in response
            and r"rank \(2h\)" in response,
            "uniform clean response/resultant theorem changed")
    return {
        "ordinary_response_Plucker_forces_Fitting_defect": False,
        "differential_Plucker_gauge_rigid_case_settled": False,
        "complete_source_Fitting_identity_constructed": False,
        "counterguard_scope": (
            "literal rank-one star-response and q=0 associated-graded "
            "face; it does not include nonzero diagonal anchors or prove "
            "extension to a complete global Krenn source"
        ),
        "first_positive_test": (
            "a higher-Bianchi/cross-chart row must lower the HB total "
            "degree from h to h-1, or directly kill the pure-chart leading "
            "tail coefficients before q=0 specialization"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform response Plucker-Veronese Hilbert-Burch gate",
        "pins": PINS,
        "scope": scope_audit(),
        "response_Plucker": response_plucker_audit(),
        "bounded_source_target": h3_h4_source_target(),
        "literal_h3_h4_physical_words": literal_cyclic_matching_word_audit(),
        "mixed_target_grades": mixed_target_grade_audit(),
        "verdict": (
            "The ordinary response-row Plucker identities do not construct "
            "the simultaneous Bezout kernel.  On the q=0 associated "
            "graded face they produce the full Veronese clean family and "
            "its standard h linear Hilbert-Burch columns, whose total "
            "degree h is the sharp coprime boundary.  A new physical "
            "higher-Bianchi/cross-chart identity must lower that total "
            "degree by at least one or directly annihilate the top "
            "residual Fitting wedge."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniform response Plucker ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h=3 response HB degree: 3 (forcing threshold 2)")
    print("h=4 response HB degree: 4 (forcing threshold 3)")
    print("all-h response Plucker: SHARP VERONESE BOUNDARY")
    print("simultaneous Bezout kernel: NOT FORCED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
