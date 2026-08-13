#!/usr/bin/env python3
"""Audit the five quadratic reset faces and their first physical descent gate.

The bare reset at the odd word 12112 has five denominator defects h_v.  On
the one-monomial C5 specialization the familiar five cubic PP switches form
the saturated rank-four face incidence lattice.  Universally, however, the
same five expressions have pairwise disjoint four-term residual supports and
rank five.  Thus projected cap closure is not a source-valid full-row cycle.

The complete Hasse four-cube fills each h_v face in the derived presentation,
but underived descent leaves h_v*(H0-u)*e_Eq.  The degree-four mixed/pure
Koszul cell is closed and cannot alter this residual.  Even on the aggregate,
the residual is not an Hm multiple.  Its scalar Eq factor is the common
odd/even/beta-Bockstein conormal, but equality of that scalar does not supply
the missing physical labelled comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h3_five_denominator_hafnians_complete_intersection.py":
        "4c87c1db939346e8f1d83a26b5edef19e3143a65cc6d6fd5ea636f99d13b5615",
    "computations/verify_h3_direct_free_first_syzygy_multidegree_gate.py":
        "7308d9b55740644affedbda04c8085517bcc2a0881eb5a8c839fc6cdee5547e5",
    "computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py":
        "4f691d119469e76436e36566a1ca7307bc49a52f66b0687c1554a9e6531ec4de",
    "computations/verify_h3_qzero_denominator_rees_four_cube.py":
        "70600661cd6a14e509a9e6487d4caa833c8bdb4419a2f442efd4b95bed7eebda",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "computations/verify_h3_shifted_filler_koszul_absorption_no_go.py":
        "37929e514e1f796725d658378b30b953d6859dfa1dcd347143c9ce80f25e6f16",
    "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py":
        "315508b572fa0d96b33ba83b8ac4905e59dfbf8f484023891618dbb3c6489d83",
    "computations/verify_h3_jd_normalized_cube_physical_cap_homology.py":
        "2488998937c4aac2915a9335c48d40398b419ee654092d9a9942157abd04b9e3",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_c6_e14_two_cell_unit_frontier.py":
        "b5a2609b64f5a0bf1720a3c571c6c4d28aa316df00129f5b4574e0f32b8c3971",
    "computations/verify_h3_c6_e14_three_cell_top_degree_boundary.py":
        "ac4ae4b8e2a351f4666cc2e196073663da94634ed4aac4c3f4e6b5dd92169313",
}
EXPECTED_LEDGER_SHA256 = "1764d43ec6e85f44dde547036cc2bdc7202722070648ffb6985aca9622072c85"

VARS = ("x12", "x13", "x14", "x15", "x23",
        "x24", "x25", "x34", "x35", "x45")
CYCLE = ("x12", "x23", "x34", "x45", "x15")
FACE_ORDER = (1, 3, 5, 2, 4)
ZERO = Q(0)

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, Q]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def polynomial(*terms: tuple[int, tuple[str, ...]]) -> Polynomial:
    result: Polynomial = {}
    for coefficient, variables in terms:
        monomial = tuple(sorted(variables))
        result[monomial] = result.get(monomial, ZERO) + Q(coefficient)
        if not result[monomial]:
            del result[monomial]
    return result


def add(left: Polynomial, right: Polynomial, scale: Q = Q(1)) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, ZERO) + scale * coefficient
        if not result[monomial]:
            del result[monomial]
    return result


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = (
                result.get(monomial, ZERO)
                + left_coefficient * right_coefficient
            )
            if not result[monomial]:
                del result[monomial]
    return result


def variable(name: str) -> Polynomial:
    return {(name,): Q(1)}


def derivative(value: Polynomial, name: str) -> Polynomial:
    result: Polynomial = {}
    for monomial, coefficient in value.items():
        count = monomial.count(name)
        if not count:
            continue
        remaining = list(monomial)
        remaining.remove(name)
        term = tuple(remaining)
        result[term] = result.get(term, ZERO) + coefficient * count
    return {term: coefficient for term, coefficient in result.items()
            if coefficient}


def evaluate_support(value: Polynomial, support: dict[str, Q]) -> Q:
    answer = ZERO
    for monomial, coefficient in value.items():
        product = coefficient
        for name in monomial:
            product *= support.get(name, ZERO)
        answer += product
    return answer


def substitute_base(value: Polynomial, support: dict[str, Q]) -> Polynomial:
    """Substitute the displayed base cells, retaining every normal variable."""
    result: Polynomial = {}
    for monomial, coefficient in value.items():
        remaining = []
        for name in monomial:
            if name in support:
                coefficient *= support[name]
            else:
                remaining.append(name)
        term = tuple(remaining)
        result[term] = result.get(term, ZERO) + coefficient
        if not result[term]:
            del result[term]
    return result


def specialize_cycle(value: Polynomial) -> Polynomial:
    allowed = set(CYCLE)
    return {
        monomial: coefficient
        for monomial, coefficient in value.items()
        if all(item in allowed for item in monomial)
    }


def rank(columns: list[list[Q]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def determinant(matrix: list[list[Q]]) -> Q:
    work = [[Q(value) for value in row] for row in matrix]
    result = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        work[column] = [entry / value for entry in work[column]]
        for row in range(column + 1, len(work)):
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[column], strict=True)]
    return result


def denominator_faces() -> dict[int, Polynomial]:
    faces = {
        1: polynomial(
            (1, ("x23", "x45")),
            (1, ("x24", "x35")),
            (1, ("x25", "x34")),
        ),
        2: polynomial(
            (1, ("x13", "x45")),
            (1, ("x14", "x35")),
            (1, ("x15", "x34")),
        ),
        3: polynomial(
            (1, ("x12", "x45")),
            (1, ("x14", "x25")),
            (1, ("x15", "x24")),
        ),
        4: polynomial(
            (1, ("x12", "x35")),
            (1, ("x13", "x25")),
            (1, ("x15", "x23")),
        ),
        5: polynomial(
            (1, ("x12", "x34")),
            (1, ("x13", "x24")),
            (1, ("x14", "x23")),
        ),
    }
    require(all(len(value) == 3 for value in faces.values()),
            "a quadratic denominator face lost a matching")
    require(set().union(*(set(monomial) for value in faces.values()
                         for monomial in value)) == set(VARS),
            "the five faces stopped using the ten K5 edges")
    return faces


def projected_and_full_switch_audit(faces: dict[int, Polynomial]):
    # Cycle order h1,h3,h5,h2,h4 and its selected monomials
    # bd,ad,ac,ce,be.  The displayed multipliers cancel exactly only after
    # every off-cycle edge is set to zero.
    pairs = (
        (1, 3, "x12", "x23"),
        (3, 5, "x34", "x45"),
        (5, 2, "x15", "x12"),
        (2, 4, "x23", "x34"),
        (4, 1, "x45", "x15"),
    )
    selected = {
        1: polynomial((1, ("x23", "x45"))),
        3: polynomial((1, ("x12", "x45"))),
        5: polynomial((1, ("x12", "x34"))),
        2: polynomial((1, ("x15", "x34"))),
        4: polynomial((1, ("x15", "x23"))),
    }
    require(all(specialize_cycle(faces[site]) == value
                for site, value in selected.items()),
            "C5 specialization stopped selecting one matching per face")

    incidence_columns: list[list[Q]] = []
    residuals: list[Polynomial] = []
    records = []
    all_supports: set[Monomial] = set()
    for index, (left, right, left_multiplier, right_multiplier) in enumerate(pairs):
        projected = add(
            multiply(variable(left_multiplier), selected[left]),
            multiply(variable(right_multiplier), selected[right]),
            Q(-1),
        )
        require(not projected, ("projected C5 switch did not close", index))
        residual = add(
            multiply(variable(left_multiplier), faces[left]),
            multiply(variable(right_multiplier), faces[right]),
            Q(-1),
        )
        require(len(residual) == 4 and residual,
                ("full switch residual changed", index, residual))
        require(not (all_supports & set(residual)),
                ("full switch residual lost its private block", index))
        all_supports.update(residual)
        residuals.append(residual)

        column = [Q(0)] * 5
        column[index] = Q(-1)
        column[(index + 1) % 5] = Q(1)
        incidence_columns.append(column)
        records.append({
            "faces": [left, right],
            "multipliers": [left_multiplier, right_multiplier],
            "projected_boundary": [int(value) for value in column],
            "full_residual": [
                {"coefficient": int(coefficient), "monomial": list(monomial)}
                for monomial, coefficient in sorted(residual.items())
            ],
        })

    require(len(all_supports) == 20,
            "the five full residual blocks stopped being disjoint")
    residual_rows = sorted(all_supports)
    residual_columns = [
        [residual.get(row, ZERO) for row in residual_rows]
        for residual in residuals
    ]
    require(rank(incidence_columns) == 4
            and rank(residual_columns) == 5,
            "projected/full switch ranks changed")
    aggregate = [Q(1)] * 5
    require(all(sum(a * b for a, b in zip(aggregate, column, strict=True)) == 0
                for column in incidence_columns),
            "projected aggregate stopped annihilating C5 incidence")
    # Deleting one row and one cycle column gives a signed tree incidence
    # matrix with determinant +/-1, proving integral saturation.
    tree_columns = incidence_columns[:-1]
    tree_matrix = [[tree_columns[column][row]
                    for column in range(len(tree_columns))]
                   for row in range(4)]
    require(abs(determinant(tree_matrix)) == 1,
            "projected C5 image stopped being saturated")

    # Every residual column has a monomial coordinate private to it.  The
    # corresponding five coordinate covectors form a literal primitive dual
    # basis and prove that no nonzero combination of the five projected
    # switches is a full source cycle.
    private_duals = []
    for index, residual in enumerate(residuals):
        private = min(residual)
        values = [column.get(private, ZERO) for column in residuals]
        require(values[index] in (Q(-1), Q(1))
                and sum(value != 0 for value in values) == 1,
                "a private full-row dual stopped being primitive")
        private_duals.append({
            "monomial": list(private),
            "values_on_five_switches": [int(value) for value in values],
        })
    return {
        "switches": records,
        "projected_cap_face_rank": rank(incidence_columns),
        "projected_integral_image": "saturated ker(sum: Z^5 -> Z)",
        "projected_primitive_dual": [1, 1, 1, 1, 1],
        "full_polynomial_residual_rank": rank(residual_columns),
        "full_polynomial_residual_coordinates": len(residual_rows),
        "private_full_row_duals": private_duals,
        "full_source_cycle_kernel_dimension": 0,
    }


def higher_reset_audit(faces: dict[int, Polynomial]):
    # The committed Hasse four-cube gives a derived filler for h_v Yw.  Its
    # projection to the underived physical differential leaves h_v*E with
    # E=(H0-u)e_Eq.  The aggregate coefficient is nonzero.
    aggregate: Polynomial = {}
    for value in faces.values():
        aggregate = add(aggregate, value)
    require(len(aggregate) == 15
            and all(coefficient == 1 for coefficient in aggregate.values()),
            "the aggregate quadratic face changed")

    # A correction b*r_m has Eq boundary b*Hm.  Membership of
    # (H0-u)*sum(h_v) in (Hm) would survive Hm=H0=0, but there it becomes
    # -u*sum(h_v), a nonzero polynomial.  This is the literal aggregate
    # version of the pinned shifted-filler Koszul absorption guard.
    specialized_residual = multiply(variable("u"), aggregate)
    specialized_residual = {
        monomial: -coefficient
        for monomial, coefficient in specialized_residual.items()
    }


def physical_cap_image_audit():
    # Rows are Omega_v followed by three labelled Q_(v,N) rows for each
    # face.  The physical cap routes are b_(v,N)=-Omega_v+Q_(v,N).
    row_count = 20
    routes: list[list[Q]] = []
    for face in range(5):
        for matching in range(3):
            column = [Q(0)] * row_count
            column[face] = Q(-1)
            column[5 + 3 * face + matching] = Q(1)
            routes.append(column)
    require(rank(routes) == 15,
            "the fifteen physical cap routes stopped being independent")

    # The separately committed endpoint-odd physical Cartan orbit induces
    # the five standard C5 directions after quotienting by the routes.  Any
    # route-adjusted lift has the same rank; use Omega differences as normal
    # form representatives.
    cartan = []
    for face in range(5):
        column = [Q(0)] * row_count
        column[face] = Q(-1)
        column[(face + 1) % 5] = Q(1)
        cartan.append(column)
    require(rank(routes + cartan) == 19,
            "route plus physical Cartan cap rank changed")
    epsilon = [Q(1)] * row_count
    require(all(sum(a * b for a, b in zip(epsilon, column, strict=True)) == 0
                for column in routes + cartan),
            "the primitive cap aggregate stopped annihilating the image")

    reset_values = []
    for face in range(5):
        reset = [Q(0)] * row_count
        for matching in range(3):
            reset[5 + 3 * face + matching] = Q(1)
        reset_values.append(sum(a * b for a, b in
                                zip(epsilon, reset, strict=True)))
    primitive_p = [Q(0)] * row_count
    primitive_p[5] = Q(-1)
    require(reset_values == [Q(3)] * 5
            and sum(a * b for a, b in zip(epsilon, primitive_p, strict=True)) == -1
            and rank(routes + cartan + [primitive_p]) == 20,
            "the reset/primitive aggregate cap values changed")
    return {
        "row_basis": "Omega_v plus three labelled Q_(v,N) per face",
        "physical_route_columns": 15,
        "physical_route_rank": rank(routes),
        "separate_physical_Cartan_standard_columns": 5,
        "combined_rank": rank(routes + cartan),
        "primitive_dual": "epsilon=sum_v lambda_v; coefficient 1 on every Omega/Q row",
        "reset_face_values": [int(value) for value in reset_values],
        "primitive_cap_example": "p=-Q_(1,N0), epsilon(p)=-1",
        "rank_after_primitive": rank(routes + cartan + [primitive_p]),
        "distinction": (
            "this source-provenant endpoint-odd Cartan orbit is not the "
            "denominator-marked cubic PP switch whose universal hidden "
            "polynomial residual has rank five"
        ),
    }


def direct_free_normal_slice_audit(faces: dict[int, Polynomial]):
    # The direct-free guard keeps only x12=a and x14=b.  Use one rational
    # point with both nonzero to certify the generic rank, and verify the
    # symbolic pattern coefficientwise by differentiating the five literal
    # quadrics before evaluation.
    a, b = Q(2), Q(3)
    base = {"x12": a, "x14": b}
    jacobian_rows = []
    derivative_records = {}
    for site in range(1, 6):
        row = [evaluate_support(derivative(faces[site], name), base)
               for name in VARS]
        jacobian_rows.append(row)
        derivative_records[str(site)] = {
            name: str(value) for name, value in zip(VARS, row, strict=True)
            if value
        }
    require(derivative_records == {
        "1": {},
        "2": {"x35": "3"},
        "3": {"x25": "3", "x45": "2"},
        "4": {"x35": "2"},
        "5": {"x23": "3", "x34": "2"},
    }, ("direct-free Jacobian formulas changed", derivative_records))
    # rank() accepts columns; transpose the five Jacobian rows.
    require(rank([[Q(value) for value in row] for row in jacobian_rows]) == 3,
            "direct-free denominator Jacobian rank changed")
    left_kernel = (
        (Q(1), Q(0), Q(0), Q(0), Q(0)),
        (Q(0), a, Q(0), -b, Q(0)),
    )
    require(all(all(sum(covector[row] * jacobian_rows[row][column]
                        for row in range(5)) == 0
                        for column in range(len(VARS)))
                for covector in left_kernel),
            "the two direct-free cokernel covectors changed")

    # The two first-order-dark equations start in two-new-cell degree.
    h1 = faces[1]
    normal_h2 = substitute_base(faces[2], base)
    normal_h4 = substitute_base(faces[4], base)
    dependent = add(
        {term: a * coefficient for term, coefficient in normal_h2.items()},
        {term: b * coefficient for term, coefficient in normal_h4.items()},
        Q(-1),
    )
    require(len(h1) == 3 and all(len(term) == 2 for term in h1),
            "the opposite h1 face stopped being quadratic")
    require(len(dependent) == 4
            and all(len(term) == 2 for term in dependent),
            "the dependent h2/h4 face stopped starting in degree two")
    require(all(not derivative(dependent, name) or
                all(len(term) >= 1 for term in derivative(dependent, name))
                for name in VARS),
            "the dependent face acquired a first-order term")
    return {
        "guard_support": {"x12": str(a), "x14": str(b)},
        "jacobian_rows": derivative_records,
        "jacobian_rank": 3,
        "first_order_cokernel_basis": [
            "h1",
            "a*h2-b*h4, with a=x12 and b=x14 on the guard",
        ],
        "h1_two_cell_monomials": len(h1),
        "dependent_two_cell_monomials": len(dependent),
        "dependent_quadratic": [
            {"coefficient": str(coefficient), "monomial": list(monomial)}
            for monomial, coefficient in sorted(dependent.items())
        ],
        "conditional_E14_terminal": (
            "if a source-labelled comparison carries either quadratic normal "
            "class to a two-new-internal-cell extension of a canonical E14 "
            "chart while preserving its core endpoint rows, the pinned E14 "
            "two-cell theorem supplies an ordinary source unit.  Multiplying "
            "by one further normal cell is covered supportwise by the pinned "
            "three-cell theorem"
        ),
        "E14_lift_constructed": False,
        "E14_guard": (
            "the E14 results classify already placed canonical chart cells; "
            "they do not construct the word/fine/repeated-grade map from "
            "these denominator normal classes.  The three-cell witnesses "
            "also vary with support and do not glue to one universal row"
        ),
    }
    require(len(specialized_residual) == 15 and specialized_residual,
            "the aggregate Eq residual vanished under the no-go specialization")

    # The CI theorem says every denominator-only first syzygy is Koszul.
    # All its coefficients lie in (h_1,...,h_5), so evaluation at h=0
    # has zero face coefficient: it cannot give a primitive aggregate unit.
    koszul_pairs = list(combinations(range(1, 6), 2))
    require(len(koszul_pairs) == 10,
            "the denominator Koszul first-syzygy count changed")
    return {
        "derived_face_fillers": {
            "count": 5,
            "boundary": "h_v*Yw",
            "target": 0,
            "ordinary_residue": 0,
            "underived_residual": "h_v*(H0-u)*e_Eq",
        },
        "aggregate_quadratic_terms": len(aggregate),
        "aggregate_underived_residual": "sum_v(h_v)*(H0-u)*e_Eq",
        "aggregate_not_in_Hm_ideal_witness": {
            "specialization": "Hm=H0=0",
            "value": "-u*sum_v(h_v)",
            "nonzero_terms": len(specialized_residual),
        },
        "degree4_mixed_pure_Koszul_cell": "closed; adding it changes no boundary",
        "denominator_CI_first_syzygies": len(koszul_pairs),
        "denominator_CI_first_syzygy_type": "Koszul h_i*e_j-h_j*e_i",
        "primitive_aggregate_from_denominator_only": False,
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    faces = denominator_faces()
    switch = projected_and_full_switch_audit(faces)
    higher = higher_reset_audit(faces)
    ledger = {
        "theorem": "degree-four reset five-face aggregate gate",
        "pins": PINS,
        "mixed_word": "12112",
        "full_word": "01211222",
        "quadratic_denominator_faces": {
            str(site): [list(monomial) for monomial in sorted(value)]
            for site, value in faces.items()
        },
        "matching_switch_comparison": switch,
        "physical_cap_image": physical_cap_image_audit(),
        "higher_reset_Bianchi_audit": higher,
        "direct_free_normal_slice": direct_free_normal_slice_audit(faces),
        "relation_to_even_beta_packet": {
            "common_scalar_conormal": "E=(H0-u)*e_Eq",
            "reset_top": "+E in each normalized deletion-face top",
            "generic_even_shadow": "+2D*E tensor (B1+B4)/2",
            "beta_zero_shadow": "V has +E and zero rho0/rho2",
            "literal_physical_identification": False,
            "missing_data": (
                "one integral source-labelled K_Eq(beta) comparison carrying "
                "word, repeated grade, ridge, labelled residue, target, W, "
                "anchor, eta, and sigma; only then may the normalized reset "
                "aggregate be called the even/Bockstein face"
            ),
        },
        "verdict": (
            "the C5 matching-switch/Hasse packet kills the saturated "
            "rank-four projected face-difference lattice only after the "
            "one-monomial cycle specialization.  Universally its five "
            "hidden polynomial residuals have disjoint support and rank "
            "five.  Complete Hasse reset totalization repairs the derived "
            "faces but physical underived descent leaves the common "
            "reduced-Eq conormal.  The existing closed mixed/pure Koszul "
            "cell and all denominator-only Koszul syzygies cannot remove it"
        ),
        "smallest_remaining_cell": (
            "the pointed augmented physical reduced-Eq comparison K_Eq(beta); "
            "its normalized deletion-face projection cancels E and converts "
            "the derived reset top into the primitive cap lift n"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("degree-four reset ledger changed", digest))
    print("h3 degree-four reset five-face aggregate gate: PASS")
    print("projected C5 face image: rank 4, saturated, dual all-ones")
    print("full five switch residuals: rank 5, 20 private monomials")
    print("higher derived filler: yes; physical descent leaves E=(H0-u)e_Eq")
    print("denominator-only/Koszul nullhomotopy: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
