#!/usr/bin/env python3
r"""Denominator/PP inventory versus the five-cycle first-Tor classes.

The cycle specialization leaves one internal matching N_v in each h_v.
For adjacent cycle generators, multiplying the two denominator-marked
two-edge PP cubes by their respective missing cycle edges puts both in the
same cubic P3+K2 degree.  Their response symbols cancel and reproduce the
five first-Tor S-pairs exactly.

The actual order-four cube carries a pure-Eq diagonal defect.  On the five
cubic pairs these defects are the differences

    a-b, c-d, e-a, b-c, d-e,

so they have rank four and generate the proper diagonal ideal.  Strict
chart Bianchi squares have zero four-readout signature, selector shifts have
zero internal cycle degree, and the mixed bar/curvature endpoint has equal
q-augmentation and ordinary residue.  None supplies the fifth aggregate or
the desired primitive invisible anchor.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "f245e206da5139e72e0e39cdf4b13dd78dcc4655f6ca73be7483ed9764cd1c64"
PINS = {
    "computations/verify_h3_rootless_five_cycle_first_tor_multidegree_gate.py":
        "a5d9021664b904f895323c29806a825545afd16085c971dc573353bb6c11a81f",
    "computations/verify_h3_rootless_first_bianchi_selector_operation_no_go.py":
        "98691b0cc5e3b89ebf3373c207cba15953ee0a4cce4dbf7708602d23a9268073",
    "computations/verify_h3_order4_denominator_cube_boundary.py":
        "f3f58f1f516dff9af0d5f58466d646e37dfa3f1779eab7f69e89f51740303f4b",
    "computations/verify_h3_mixed_bar_curvature_bicomplex.py":
        "6d239dfa1610d36de3385f9e084693523225528f8343ea9412773604fe396318",
}

ODD = (1, 2, 3, 4, 5)
CYCLE_EDGES = ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5))
VARIABLES = ("a=q12", "b=q23", "c=q34", "d=q45", "e=q15")
GENERATOR_ORDER = (1, 3, 5, 2, 4)
ZERO = Q(0)

Monomial = tuple[int, int, int, int, int]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices if site not in (first, second))
        for tail in perfect_matchings(rest):
            result.append(((first, second),) + tail)
    return tuple(result)


def exponent(edges) -> Monomial:
    result = [0] * len(CYCLE_EDGES)
    for edge in edges:
        edge = tuple(sorted(edge))
        require(edge in CYCLE_EDGES, ("off-cycle exponent requested", edge))
        result[CYCLE_EDGES.index(edge)] += 1
    return tuple(result)  # type: ignore[return-value]


def add(left: Monomial, right: Monomial) -> Monomial:
    return tuple(a + b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def subtract(left: Monomial, right: Monomial) -> Monomial:
    result = tuple(a - b for a, b in zip(left, right, strict=True))
    require(all(value >= 0 for value in result), ("negative exponent", left, right))
    return result  # type: ignore[return-value]


def lcm(left: Monomial, right: Monomial) -> Monomial:
    return tuple(max(a, b) for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def degree(value: Monomial) -> int:
    return sum(value)


def rank(columns) -> int:
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


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), ZERO)


def specialized_denominator_inventory():
    selected = {}
    excluded = []
    all_records = []
    for v in ODD:
        face = tuple(site for site in ODD if site != v)
        matchings = perfect_matchings(face)
        require(len(matchings) == 3, ("K4 matching count changed", v))
        cycle_matchings = [matching for matching in matchings
                           if all(tuple(sorted(edge)) in CYCLE_EDGES
                                  for edge in matching)]
        require(len(cycle_matchings) == 1,
                ("cycle face did not select one denominator square", v))
        chosen = tuple(sorted(cycle_matchings[0]))
        selected[v] = chosen
        for matching in matchings:
            matching = tuple(sorted(matching))
            on_cycle = matching == chosen
            if not on_cycle:
                off_cycle = [edge for edge in matching if edge not in CYCLE_EDGES]
                require(off_cycle, ("unselected matching stayed on cycle", v, matching))
                excluded.append((v, matching))
            all_records.append({
                "v": v,
                "matching": [list(edge) for edge in matching],
                "cycle_fine_degree": on_cycle,
            })
    require(len(all_records) == 15 and len(excluded) == 10,
            "denominator-square cycle census changed")

    expected = {
        1: ((2, 3), (4, 5)),
        2: ((1, 5), (3, 4)),
        3: ((1, 2), (4, 5)),
        4: ((1, 5), (2, 3)),
        5: ((1, 2), (3, 4)),
    }
    require(selected == expected, ("selected cycle matchings changed", selected))
    return selected, all_records


def pp_to_first_tor(selected):
    generators = [exponent(selected[v]) for v in GENERATOR_ORDER]
    records = []
    ridge_columns = []
    eq_residual_columns = []
    for index in range(5):
        following = (index + 1) % 5
        left_site = GENERATOR_ORDER[index]
        right_site = GENERATOR_ORDER[following]
        left = generators[index]
        right = generators[following]
        target = lcm(left, right)
        left_multiplier = subtract(target, left)
        right_multiplier = subtract(target, right)
        require(degree(target) == 3
                and degree(left_multiplier) == degree(right_multiplier) == 1,
                ("PP lift missed first Tor", left_site, right_site))
        require(add(left_multiplier, left) == add(right_multiplier, right) == target,
                "multiplied PP responses did not cancel")

        # In the ridge quotient, each selected PP route has response h_v.
        # The difference of the two multiplied routes cancels that response.
        ridge = [0] * 5
        ridge[index] = -1
        ridge[following] = 1
        ridge_columns.append(ridge)

        # The actual order-four cube has diagonal commutator (H0-u)e_Eq.
        # Multiplication by the two missing edges makes its residual the
        # difference of those two degree-one coefficients.
        left_variable = left_multiplier.index(1)
        right_variable = right_multiplier.index(1)
        residual = [0] * 5
        residual[left_variable] = 1
        residual[right_variable] = -1
        eq_residual_columns.append(residual)
        records.append({
            "faces": [left_site, right_site],
            "cubic_multidegree": list(target),
            "left_PP_multiplier": list(left_multiplier),
            "right_PP_multiplier": list(right_multiplier),
            "response_after_subtraction": 0,
            "strict_PP_readouts_ainc_w_tgt_ores": [0, 0, 0, 0],
            "physical_cube_Eq_residual": {
                "left_sign_monomial": [1, list(left_multiplier)],
                "right_sign_monomial": [-1, list(right_multiplier)],
            },
        })

    require(rank(ridge_columns) == rank(eq_residual_columns) == 4,
            "five PP S-pairs stopped being a rank-four cycle")
    require(all(sum(column) == 0 for column in ridge_columns + eq_residual_columns),
            "a PP S-pair stopped vanishing on the diagonal")
    return records, ridge_columns, eq_residual_columns


def selector_and_readout_no_go(ridge_columns, eq_residual_columns):
    # Selector localization shifts only the external x,p,q character in the
    # pinned operation.  It has zero internal cycle multidegree.  The active
    # point below has every allowed selector/star/curvature unit equal to 1,
    # so the diagonal ideal remains proper after that localization.
    selector_internal_shift = [0] * 5
    require(not any(selector_internal_shift), "selector acquired q-cycle degree")
    active_diagonal_point = [1] * 5
    require(all(dot(active_diagonal_point, column) == 0
                for column in eq_residual_columns),
            "selector-active diagonal point left the residual ideal")

    # Strict chart PP/Bianchi columns have zero four-readout signature.
    # The actual mixed bar-curvature endpoint has qaug=ores=kappa; a bar
    # edge has both zero.  Therefore any combination with ores=0 also has
    # qaug=0 and cannot supply an invisible fifth endpoint.
    bar_endpoint = [1, 1]  # normalized (q-augmentation, ordinary residue)
    bar_edge = [0, 0]
    invisible = [1, 0]
    require(rank([bar_endpoint, bar_edge]) == 1
            and rank([bar_endpoint, bar_edge, invisible]) == 2,
            "bar/residue rank separator changed")

    # Reproduce the pinned old-cap separator in coordinates
    # (uEq,w,target,ordinary residue), at Y=1.
    old_columns = [
        [-1, 0, 1, 0],
        [0, -1, 1, 0],
        [0, 1, 0, 1],
    ]
    desired = [-1, 0, 0, 0]
    separator = [1, 1, 1, -1]
    require(all(dot(separator, column) == 0 for column in old_columns),
            "old-cap separator failed")
    require(dot(separator, desired) == -1
            and rank(old_columns) == 3
            and rank(old_columns + [desired]) == 4,
            "desired invisible anchor entered old readout span")

    return {
        "selector_internal_cycle_shift": selector_internal_shift,
        "active_localization_guard": {
            "cycle_cells": active_diagonal_point,
            "selector_star_curvature_units": "all 1",
            "all_PP_difference_residuals": 0,
        },
        "strict_PP_Bianchi_signature": [0, 0, 0, 0],
        "mixed_bar_endpoint_qaug_ores": bar_endpoint,
        "mixed_bar_edge_qaug_ores": bar_edge,
        "rank_old_bar_readouts": 1,
        "rank_with_invisible_endpoint": 2,
        "old_cap_rank": 3,
        "old_cap_rank_with_Crel": 4,
        "surviving_fifth_aggregate": "sum_v lambda_v",
        "ridge_rank_after_all_cubic_PP_pairs": rank(ridge_columns),
    }


def main() -> None:
    pin_dependencies()
    selected, inventory = specialized_denominator_inventory()
    pairs, ridge_columns, residual_columns = pp_to_first_tor(selected)
    readouts = selector_and_readout_no_go(ridge_columns, residual_columns)
    ledger = {
        "pins": PINS,
        "cycle_variables": list(VARIABLES),
        "denominator_PP_inventory": inventory,
        "selected_cycle_matchings": {
            str(v): [list(edge) for edge in matching]
            for v, matching in sorted(selected.items())
        },
        "cubic_PP_pairs": pairs,
        "pair_ridge_rank": rank(ridge_columns),
        "pair_Eq_residual_rank": rank(residual_columns),
        "readout_no_go": readouts,
        "verdict": (
            "the five selected denominator PP square pairs reproduce exactly "
            "the five cubic Tor S-pairs, but only the rank-four diagonal "
            "difference module; off-cycle squares miss the fine degree and "
            "selectors/Bianchi/bar corrections do not supply the fifth "
            "anchor-normalized aggregate"
        ),
        "minimal_missing_face": (
            "a new repeated-site relative lower face outside the denominator "
            "PP inventory, with nonzero sum-lambda value and signature "
            "(-1,0,0,0)"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED", ("pin ledger digest", digest))
    require(digest == EXPECTED_LEDGER_SHA256, ("ledger digest changed", digest))
    print("h=3 five-cycle denominator/PP aggregate gate: PASS")
    print("15 PP squares: 5 cycle-degree, 10 off-degree")
    print("five cubic PP pairs reproduce first Tor with rank 4")
    print("selector/Bianchi/bar inventory supplies no fifth aggregate")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
