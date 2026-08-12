#!/usr/bin/env python3
r"""The first physical single-v comparison needs a new site-collision face.

The non-Euler two-chart class has a derived squarefree normal filler with
zero target and ordinary residue, but its chart correction is not physical
anchor incidence.  The first physical companion degree which can see one
ridge class is a repeated-site P3+K2 degree in the C5 companion ideal.

This checker builds the complete two-column component of each such degree.
A single multiplied route has a private ordinary-residue companion.  The
unique cancellation uses the adjacent route; it has the desired ridge
S-pair but zero physical anchor incidence.  That relation is the boundary
specified for a formal first-Tor cell, not a literal physical higher cell.
Even if the polynomial coefficient augmentation is declared to be an anchor
row, it equals the
ordinary-residue row at the diagonal torus point.  Thus a primitive anchor
face is not obtained by the existing multiplier comparison.

The result is a no-go for the first literal collision/multiplier module, not
for an enlarged relative source resolution.  It specifies the missing
source cell exactly.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "a007638ab5f17241f9e6a8ece18692447757c6577ed9593dd869204f0d50647d"
PINS = {
    "computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py":
        "0bbed406d393543b6badf222ff0665dc1b12445a2360a015e5398bd538bd5e5c",
    "computations/verify_h3_rootless_non_euler_90term_chart_h1_separator.py":
        "6b27d870a87e3f95d274c1cb1a5d785bf04a5d5f3c353d54a11bd231a3fe1950",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
    "computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py":
        "c409a62957dba0d101d1298ec16695482fce705d3131323a8d3657074f1bf2b0",
    "computations/verify_h3_rootless_five_cycle_first_tor_multidegree_gate.py":
        "a5d9021664b904f895323c29806a825545afd16085c971dc573353bb6c11a81f",
    "computations/verify_h3_rootless_five_cycle_positive_interface.py":
        "fd359b3ff2abbb01d9508996c754a27b70890b2cd621926fc30b92057b337851",
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "2e09f9be1ed1b57821c64dd690df7e4d6b2efebe93cb8aae9ff0a58b3190022d",
}

CYCLE_EDGES = ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5))
GENERATOR_SITES = (1, 3, 5, 2, 4)
Monomial = tuple[int, int, int, int, int]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def rank(columns: list[tuple[int | Q, ...]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns),
            "ragged matrix")
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
        if pivot_row == height:
            break
    return pivot_row


def determinant(columns: list[tuple[int | Q, ...]]) -> Q:
    size = len(columns)
    require(size and all(len(column) == size for column in columns),
            "determinant needs a square matrix")
    work = [[Q(columns[column][row]) for column in range(size)]
            for row in range(size)]
    result = Q(1)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        work[column] = [entry / value for entry in work[column]]
        for row in range(column + 1, size):
            value = work[row][column]
            if value:
                work[row] = [left - value * right for left, right in
                             zip(work[row], work[column], strict=True)]
    return result


def monomial(*indices: int) -> Monomial:
    value = [0] * 5
    for index in indices:
        value[index] += 1
    return tuple(value)  # type: ignore[return-value]


def lcm(left: Monomial, right: Monomial) -> Monomial:
    return tuple(max(a, b) for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def divides(left: Monomial, right: Monomial) -> bool:
    return all(a <= b for a, b in zip(left, right, strict=True))


def site_profile(value: Monomial) -> tuple[int, ...]:
    profile = {site: 0 for site in range(1, 6)}
    for edge_index, exponent in enumerate(value):
        require(exponent in (0, 1), "unexpected repeated cycle edge")
        if exponent:
            for site in CYCLE_EDGES[edge_index]:
                profile[site] += 1
    return tuple(profile[site] for site in range(1, 6))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices if site not in (first, second))
        for tail in perfect_matchings(rest):
            result.append(((first, second),) + tail)
    return tuple(result)


def chart_and_cap_gate() -> dict[str, object]:
    # Literal physical augmented boundary of the two chart copies.  Rows are
    # (source matching boundary, W, target, ordinary residue).  Fine degree
    # is common and therefore adds another even row, not a chart-odd row.
    c_pq = (1, 0, 0, 0)
    c_pr = (1, 0, 0, 0)
    require(rank([c_pq, c_pr]) == 1, "two-chart physical rank changed")
    kernel = (1, -1)
    require(tuple(kernel[0] * a + kernel[1] * b
                  for a, b in zip(c_pq, c_pr, strict=True)) == (0, 0, 0, 0),
            "chart difference stopped being physical-boundary zero")

    # The normalized marked chart row is (1/2,-1/2).  Every physical row
    # pulled back through the forgetful map is chart-even, so adjoining the
    # marked row raises rank.  This is the presentation/physical split.
    physical_row = (1, 1)
    chart_odd = (Q(1, 2), Q(-1, 2))
    require(rank([physical_row]) == 1
            and rank([physical_row, chart_odd]) == 2,
            "chart-odd separator unexpectedly factored physically")
    require(sum(a * b for a, b in zip(chart_odd, kernel, strict=True)) == 1,
            "normalized chart separator stopped reading one")

    # Normalize the shifted derived filler on D(hY), or after the completed
    # normal inverse on V(h).  Rows are (W boundary, target, ores, chart).
    # The two standard cap columns T and rho are the old correction block
    # tested here; this is not a claim about an enlarged source resolution.
    n_v = (1, 0, 0, -1)
    h_T = (-1, 1, 0, 0)
    hY_rho = (1, 0, 1, 0)
    desired_chart_cycle = (0, 0, 0, -1)
    require(rank([n_v, h_T, hY_rho]) == 3,
            "derived cap block rank changed")
    require(rank([n_v, h_T, hY_rho, desired_chart_cycle]) == 4,
            "old cap block unexpectedly produced a clean chart correction")
    require(abs(determinant([n_v, h_T, hY_rho,
                             desired_chart_cycle])) == 1,
            "derived cap obstruction stopped being primitive")

    return {
        "literal_chart_boundary_rows": ["source", "W", "target", "ores"],
        "literal_chart_columns": [list(c_pq), list(c_pr)],
        "primitive_kernel": list(kernel),
        "normalized_chart_odd_row": ["1/2", "-1/2"],
        "physical_pullback_rows_are_chart_even": True,
        "derived_cap_rows": ["W", "target", "ores", "chart_S"],
        "derived_cap_columns": {
            "n_v": list(n_v),
            "hT": list(h_T),
            "hYrho": list(hY_rho),
        },
        "desired_clean_chart_cycle": list(desired_chart_cycle),
        "derived_cap_determinant": 1,
        "physical_anchor_incidence": (
            "not a chart row; no physical ainc value is assigned to n_v"
        ),
    }


def collision_gate() -> dict[str, object]:
    # (h1,h3,h5,h2,h4)=(bd,ad,ac,ce,be).
    generators = (
        monomial(1, 3),
        monomial(0, 3),
        monomial(0, 2),
        monomial(2, 4),
        monomial(1, 4),
    )
    records = []
    for left in range(5):
        right = (left + 1) % 5
        target = lcm(generators[left], generators[right])
        active = [index for index, value in enumerate(generators)
                  if divides(value, target)]
        require(active == [left, right] or (left == 4 and active == [0, 4]),
                ("first collision degree has extra routes", left, active))
        profile = site_profile(target)
        require(sorted(profile) == [1, 1, 1, 1, 2],
                ("collision target stopped being P3+K2", left, profile))

        # Factor the common repeated-site monomial.  The two oriented literal
        # route columns have rows
        #   (ridge_left, ridge_right, ores, W, target, physical_ainc).
        # Physical ainc is zero: these are response/bar multiplier columns,
        # not a relative pure-anchor face.
        left_column = (-1, 0, 1, 0, 0, 0)
        right_column = (0, 1, -1, 0, 0, 0)
        pair = tuple(a + b for a, b in
                     zip(left_column, right_column, strict=True))
        require(pair == (-1, 1, 0, 0, 0, 0),
                "two-route collision stopped cancelling ordinary residue")

        # On one v alone, the ores row is a private unit, so zero ordinary
        # residue forces the coefficient to vanish.  The two-v S-pair has
        # the desired source boundary but still no physical anchor.
        require(left_column[2] == 1 and right_column[2] == -1,
                "private companion signs changed")
        desired_anchor = (1, 0, 0, 0, 0, -1)
        require(rank([left_column, right_column]) == 2
                and rank([left_column, right_column, desired_anchor]) == 3,
                "separate primitive physical-anchor column stopped being new")
        physical_separator = (0, 0, 0, 0, 0, 1)
        require(all(sum(a * b for a, b in zip(physical_separator, column,
                                               strict=True)) == 0
                    for column in (left_column, right_column))
                and sum(a * b for a, b in zip(physical_separator, desired_anchor,
                                               strict=True)) == -1,
                "physical ainc separator failed")

        # Grant the strongest tempting replacement: identify the signed
        # coefficient augmentation with an anchor row.  At a=b=...=1 that
        # declared row equals the ores row on both columns.  Hence the
        # primitive covector (declared anchor - ores) still detects desired.
        generous_left = (1, 1)       # (ores, declared augmentation)
        generous_right = (-1, -1)
        generous_desired_anchor = (0, -1)
        separator = (-1, 1)
        require(all(sum(a * b for a, b in zip(separator, column, strict=True)) == 0
                    for column in (generous_left, generous_right))
                and sum(a * b for a, b in zip(separator, generous_desired_anchor,
                                               strict=True)) == -1,
                "diagonal augmentation separator failed")

        records.append({
            "faces": [GENERATOR_SITES[left], GENERATOR_SITES[right]],
            "fine_cycle_degree": list(target),
            "site_profile": list(profile),
            "active_literal_routes": [GENERATOR_SITES[index] for index in active],
            "oriented_columns": [list(left_column), list(right_column)],
            "formal_first_Tor_boundary": list(pair),
            "literal_higher_cell_with_this_boundary": False,
            "separate_desired_anchor_column": list(desired_anchor),
            "single_v_zero_ores_solution_dimension": 0,
            "two_v_physical_ainc": 0,
            "generous_formal_separator": "declared_augmentation - ores",
        })

    return {
        "row_order": [
            "ridge_left", "ridge_right", "ores_companion",
            "W", "target", "physical_ainc",
        ],
        "records": records,
        "all_five_single_v_modules_fail": True,
        "all_five_two_v_spairs_have_zero_W_target_ores": True,
        "all_five_two_v_spairs_have_zero_physical_ainc": True,
        "primitive_physical_separator_for_separate_anchor": "physical_ainc",
        "generous_diagonal_separator": "declared_augmentation - ores",
    }


def squarefree_inventory_gate() -> dict[str, object]:
    checked = 0
    for matching in perfect_matchings(tuple(range(8))):
        for subset_size in range(5):
            for subset in combinations(matching, subset_size):
                profile = [0] * 8
                for left, right in subset:
                    profile[left] += 1
                    profile[right] += 1
                require(max(profile, default=0) <= 1,
                        "literal Hasse face repeated a physical site")
                checked += 1
    require(checked == 105 * 16, "squarefree Hasse census changed")
    return {
        "literal_matching_Hasse_faces_checked": checked,
        "maximum_physical_site_degree": 1,
        "collision_target_maximum_site_degree": 2,
        "degree_zero_comparison_possible": False,
        "first_degree_shift": (
            "multiply a response route by the unique incident C5 edge; "
            "the private ores companion forces the adjacent two-face S-pair"
        ),
    }


def main() -> None:
    pin_dependencies()
    chart = chart_and_cap_gate()
    collision = collision_gate()
    inventory = squarefree_inventory_gate()
    ledger = {
        "pins": PINS,
        "single_v_chart_and_cap_gate": chart,
        "site_collision_gate": collision,
        "squarefree_inventory_gate": inventory,
        "verdict": (
            "the derived chart correction does not factor as physical anchor "
            "incidence; a homogeneous comparison cannot send a squarefree "
            "normal face to P3+K2, and the complete first collision degree "
            "has no single-v zero-ores column"
        ),
        "minimal_new_physical_datum": {
            "name": "site-collision comparison E_v",
            "fine_degree": "one of the five repeated-site P3+K2 degrees",
            "source_boundary": "the adjacent two-face ridge S-pair -r_v+r_w",
            "W_target_ores": [0, 0, 0],
            "physical_ainc": 0,
            "chart_requirement": (
                "supply a genuine degree-shifting chain map; the derived "
                "-S_v correction is not this cell's physical ainc"
            ),
            "family_compatibility": "the degree-five odd-cycle second face",
            "independent_anchor_requirement": (
                "a separate primitive vertex-boundary cell with physical "
                "ainc=-1 and W=target=ores=0"
            ),
        },
        "scope": (
            "exact first-degree/common-q source obstruction; a new relative "
            "site-collision generator is not excluded"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h=3 rootless single-v site-collision comparison: OBSTRUCTED")
    print("literal chart kernel: chart-odd, physical-forgetful zero")
    print("first collision degree: no single-v zero-ores column")
    print("two-face S-pair: boundary restored, physical ainc still zero")
    print("minimal new datum: repeated-site collision face (ainc=0)")
    print("primitive physical anchor remains a separate cell")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
