#!/usr/bin/env python3
"""Post-KS classification of the same-head rank/support boundary.

The residual-q KS attachment closes endpoint holonomy but has no physical
target or anchor readout.  This checker separates the next two linear events.

* A dependence among complete columns of occupied cells in one p_i or s_j
  row gives an exact support-reducing source update.  This extends the pinned
  two-column proportional move to an arbitrary same-row span.
* If those complete columns are independent, support descent is unavailable.
  A deleted-star profile (2,2,3,3) is restored exactly when the available
  physical columns are visible in both one-dimensional deficient cokernels.

The pinned target-coloop/same-head modules realize the independent and
double-dark branch even after adjoining the signless and KS endpoint
orientations.  Thus the KS hypothesis alone forces neither event.  The first
missing rank input is a source-labelled common-q exchange with nonzero
projection to both deficient star quotients; Hall landing is downstream.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_ks_constructive_landing_boundary.py":
        "bc11c8fe61ec8c21a1850326de037a328ab7f7404bcf3902655f6541e496bc9f",
    "computations/verify_uniform_axis_circuit_third_component_rank_guard.py":
        "d9e852bad1b94c1918523fa834029abff04f4c288bde2f97c790def1bef2644f",
    "computations/verify_uniform_axis_circuit_target_coloop_full_five_boundary.py":
        "4e84ec46bac4b9b97a69dbfa61899877c5b09f3960bf666af1ddf1ade01c54d6",
    "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py":
        "6f27d3585fdc4708026ab6fef6134295dd874f83bb43fd1f480b7314362c56f3",
}
EXPECTED_LEDGER_SHA256 = "6fec2ed27b57816687e7084ef6fa01c042bfc8dbef9c1d50ecdbf7438b09b154"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged columns")
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def matvec(columns, coefficients):
    require(len(columns) == len(coefficients), "coefficient width changed")
    return add(*(scale(value, column)
                 for value, column in zip(coefficients, columns, strict=True)))


def mutual_anchors(edges):
    degrees = {}
    for left, right in edges:
        degrees[left] = degrees.get(left, 0) + 1
        degrees[right] = degrees.get(right, 0) + 1
    return frozenset(edge for edge in edges
                     if degrees[edge[0]] == degrees[edge[1]] == 1)


def audit_complete_same_row_span_descent(proportional):
    """Any occupied same-row complete-column dependence lowers support."""
    pair_move = proportional.audit_exact_proportional_move()
    require(pair_move["finite_update"]
            == "x_out'=0, x_comp'=x_comp+lambda*x_out",
            "the pinned two-column support move changed")

    # A genuine three-column dependence, not reducible to a proportional
    # occupied pair.  The update is the general formula x'=x-(x_e/k_e)k.
    c0 = (Q(1), Q(0), Q(1), Q(0))
    c1 = (Q(0), Q(1), Q(0), Q(1))
    c2 = add(c0, c1)
    columns = (c0, c1, c2)
    kernel_relation = (Q(-1), Q(-1), Q(1))
    require(rank(columns) == 2
            and matvec(columns, kernel_relation) == (Q(0),) * 4,
            "the three-column same-row relation changed")
    old_coefficients = (Q(2), Q(3), Q(5))
    carrier = 2
    factor = old_coefficients[carrier] / kernel_relation[carrier]
    new_coefficients = tuple(
        old - factor * relation for old, relation in
        zip(old_coefficients, kernel_relation, strict=True)
    )
    require(new_coefficients[carrier] == 0
            and matvec(columns, old_coefficients)
                == matvec(columns, new_coefficients)
            and sum(value != 0 for value in new_coefficients)
                < sum(value != 0 for value in old_coefficients),
            "the multi-column support update changed")

    # All changed cells share the row head H, so none is a mutual coordinate
    # anchor.  Exhaust arbitrary ambient graphs and every nonempty subset of
    # the three same-row cells which might cancel under the update.
    head = "H"
    tails = ("T0", "T1", "T2")
    same_row_edges = tuple(tuple(sorted((head, tail))) for tail in tails)
    vertices = (head, *tails, "A", "B")
    optional = tuple(
        tuple(sorted(edge)) for edge in combinations(vertices, 2)
        if tuple(sorted(edge)) not in same_row_edges
    )
    graph_audits = 0
    for mask in range(1 << len(optional)):
        old_edges = set(same_row_edges)
        old_edges.update(optional[index] for index in range(len(optional))
                         if mask & (1 << index))
        old_anchors = mutual_anchors(old_edges)
        require(not any(edge in old_anchors for edge in same_row_edges),
                "a same-row occupied cell became a mutual anchor")
        for deletion_mask in range(1, 1 << len(same_row_edges)):
            new_edges = set(old_edges)
            for index, edge in enumerate(same_row_edges):
                if deletion_mask & (1 << index):
                    new_edges.remove(edge)
            require(old_anchors <= mutual_anchors(new_edges)
                    and len(new_edges) < len(old_edges),
                    "a same-row span update damaged the lexicographic invariant")
            graph_audits += 1

    # The converse is exact linear algebra: a kernel vector touching e is
    # equivalent to C_e lying in the span of the other occupied columns.
    independent = tuple(
        tuple(Q(int(row == column)) for row in range(3))
        for column in range(3)
    )
    require(rank(independent) == 3,
            "the independent same-row boundary changed")
    return {
        "general_relation": "sum_i k_i L(z_i)=0 with k_e!=0",
        "finite_update": "x'=x-(x_e/k_e)k, hence x'_e=0",
        "three_column_example": {
            "rank": rank(columns),
            "kernel_relation": [str(value) for value in kernel_relation],
            "old_coefficients": [str(value) for value in old_coefficients],
            "new_coefficients": [str(value) for value in new_coefficients],
        },
        "anchor_safe_graph_audits": graph_audits,
        "exact_criterion": (
            "carrier e is support-deletable inside its occupied same row iff "
            "L(z_e) lies in the span of the other occupied complete columns"
        ),
        "minimum_support_consequence": (
            "every occupied same-row family of complete response columns is "
            "linearly independent"
        ),
        "independent_boundary_rank": rank(independent),
    }


def audit_deleted_star_quotient_classification():
    """Rank restoration is visibility in two one-dimensional cokernels."""
    e0 = (Q(1), Q(0), Q(0))
    e1 = (Q(0), Q(1), Q(0))
    e2 = (Q(0), Q(0), Q(1))
    deficient_u = (e0, e1)
    deficient_v = (e0, e1)
    good = (e0, e1, e2)
    lambda_u = e2
    lambda_v = e2

    def pairing(left, right):
        return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))

    def profile(candidates):
        u_columns = deficient_u + tuple(item[0] for item in candidates)
        v_columns = deficient_v + tuple(item[1] for item in candidates)
        return (rank(u_columns), rank(v_columns), rank(good), rank(good))

    same_head = ((add(e0, e1), e0),)
    u_only = ((e2, e0),)
    v_only = ((e0, e2),)
    double_transverse = ((e2, e2),)
    split_transverse = ((e2, e0), (e0, e2))
    require(profile(()) == (2, 2, 3, 3)
            and profile(same_head) == (2, 2, 3, 3)
            and profile(u_only) == (3, 2, 3, 3)
            and profile(v_only) == (2, 3, 3, 3)
            and profile(double_transverse) == (3, 3, 3, 3)
            and profile(split_transverse) == (3, 3, 3, 3),
            "the deficient-star quotient classification changed")
    require(pairing(lambda_u, same_head[0][0]) == 0
            and pairing(lambda_v, same_head[0][1]) == 0
            and pairing(lambda_u, double_transverse[0][0]) == 1
            and pairing(lambda_v, double_transverse[0][1]) == 1,
            "the deficient-star dual readouts changed")
    return {
        "baseline_profile": [2, 2, 3, 3],
        "deficient_cokernel_dimensions": [1, 1],
        "same_head_profile": list(profile(same_head)),
        "one_sided_profiles": [list(profile(u_only)), list(profile(v_only))],
        "double_transverse_profile": list(profile(double_transverse)),
        "split_transverse_profile": list(profile(split_transverse)),
        "exact_criterion": (
            "a set Z restores (3,3,3,3) iff its projections have nonzero "
            "image in each of the two deficient one-dimensional quotients"
        ),
        "single_arm_criterion": "lambda_u(z_u)*lambda_v(z_v)!=0",
    }


def audit_post_ks_combined_counterguard(landing, local_rank, coloop):
    local = local_rank.audit_order(3)
    full_five = coloop.audit_full_five_boundary()
    require(local["deleted_star_profile"] == [2, 2, 3, 3]
            and local["outer_head_span_rank"] == 1
            and full_five["column_ranks"] == [3, 3]
            and full_five["joint_kernel_dimensions"] == [0, 0]
            and full_five["pure_target_port_supports"]["X2"] == [0],
            "the pinned same-head/target-coloop packet changed")

    # Replay the exact KS correction type consumed by 2593831.  It is
    # residue-only before composition; modulo the old bar it gives D.  In
    # either description its displayed geometric/protected boundary entries
    # remain zero.  The hypothesis does not specify a physical deleted-star
    # column; the product counterguard below takes the compatible zero lift.
    require(landing.FEATURES == (
        "E_plus", "E_minus", "Omega", "q_comp",
        "ores_pure_plus", "ores_pure_minus",
        "ores_mixed_plus", "ores_mixed_minus", "W", "target", "ainc",
    ), "the KS feature order changed")
    ks_correction = landing.vector(
        ores_pure_plus=-1, ores_pure_minus=1,
        ores_mixed_plus=1, ores_mixed_minus=-1,
    )
    require(all(ks_correction[landing.FEATURES.index(row)] == 0 for row in (
        "E_plus", "E_minus", "Omega", "q_comp", "W", "target", "ainc",
    )), "the KS correction acquired a protected boundary readout")

    # Use the second three-column target-coloop circuit and adjoin the old
    # signless endpoint row S and the KS endpoint determinant D in a direct
    # endpoint block.  Give these boundary columns zero projection to the
    # physical deleted-star block.  This is compatible with every readout in
    # the KS hypothesis and is the smallest simultaneous structural module;
    # it is not claimed to reconstruct the unknown physical lift.
    physical = tuple(tuple(Q(value) for value in column)
                     for column in full_five["p2_complete_columns"])
    embedded = tuple((Q(0), Q(0), *column) for column in physical)
    zero_tail = (Q(0),) * len(physical[0])
    signless = (Q(1), Q(1), *zero_tail)
    determinant = (Q(1), Q(-1), *zero_tail)
    post_ks = embedded + (signless, determinant)
    target_coordinate = 2 + full_five["feature_basis"].index("22:X2")
    require(rank(embedded) == 3
            and rank((signless,)) == 1
            and rank((signless, determinant)) == 2
            and rank(post_ks) == 5
            and tuple(index for index, column in enumerate(post_ks)
                      if column[target_coordinate]) == (0,),
            "the combined post-KS coloop counterguard changed")
    return {
        "physical_complete_column_rank": rank(embedded),
        "physical_complete_column_kernel_dimension": 0,
        "endpoint_orientation_rank_before_after": [1, 2],
        "combined_column_rank_and_count": [rank(post_ks), len(post_ks)],
        "pure_target_support_after_KS": [0],
        "deleted_star_profile_after_KS": local["deleted_star_profile"],
        "outer_head_span_after_KS": local["outer_head_span_rank"],
        "compatible_KS_deleted_star_quotient": [0, 0],
        "verdict": (
            "endpoint holonomy is split, but the occupied physical columns "
            "remain injective, the pure target remains a port coloop, and "
            "both deficient star quotients remain dark"
        ),
        "scope": (
            "smallest exact product of the pinned structural modules; not a "
            "physical common-q GHZ source"
        ),
    }


def main():
    pin_dependencies()
    landing = load(
        "computations/verify_h3_residual_q_ks_constructive_landing_boundary.py",
        "post_ks_landing",
    )
    local_rank = load(
        "computations/verify_uniform_axis_circuit_third_component_rank_guard.py",
        "post_ks_local_rank",
    )
    coloop = load(
        "computations/verify_uniform_axis_circuit_target_coloop_full_five_boundary.py",
        "post_ks_coloop",
    )
    proportional = load(
        "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py",
        "post_ks_proportional",
    )

    ledger = {
        "pins": PINS,
        "complete_same_row_support_descent":
            audit_complete_same_row_span_descent(proportional),
        "deleted_star_quotient_classification":
            audit_deleted_star_quotient_classification(),
        "post_KS_target_coloop_counterguard":
            audit_post_ks_combined_counterguard(landing, local_rank, coloop),
        "rank_restoration_or_support_descent_interface": (
            "for an occupied same-row carrier e, a complete-column relation "
            "touching e gives an exact anchor-safe support descent.  If the "
            "same-row complete columns are independent, rank restoration is "
            "equivalent to nonzero physical source image in both deficient "
            "deleted-star quotient lines.  The exact KS boundary asserts "
            "neither a relation nor such a physical quotient image"
        ),
        "first_missing_source_theorem": (
            "in the independent target-coloop branch, a literal common-q "
            "four-hole exchange must either create a complete same-row "
            "dependence touching the carrier or produce occupied physical "
            "columns visible in both deficient deleted-star quotients"
        ),
        "separation_of_scopes": {
            "termination": (
                "only the complete-column dependence branch lowers physical "
                "support; the KS typed-component decrease is a separate "
                "filtration move"
            ),
            "Hall": (
                "Hall/lock routing begins only after a nonzero transverse or "
                "offanchor physical carrier exists and is not used here"
            ),
        },
        "scope": (
            "exact same-row support theorem, exact rank-quotient criterion, "
            "and smallest post-KS structural counterguard.  No assertion "
            "that the counterguard is a physical GHZ source"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"post-KS rank/support ledger changed: {digest}")
    print("h3 post-KS same-head rank/support boundary: COUNTERGUARD")
    print("same-row complete dependence -> exact anchor-safe support descent")
    print("independent branch: rank restoration iff both star quotients are visible")
    print("post-KS target-coloop: kernel 0, quotient visibility 0/0, profile 2233")
    print("Hall and KS typed termination are separate")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
