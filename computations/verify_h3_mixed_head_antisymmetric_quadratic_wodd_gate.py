#!/usr/bin/env python3
"""Audit the mixed-head antisymmetric quadratic-selector candidate for W_odd.

The coefficient proposal is exact.  On the two ordered mixed-head response
objects, the diagonal selector sends

    R_01(w) - R_10(tau w)

to the direct-sum vector (e_f,-e_{tau f}).  Both mixed heads have zero GHZ
target, so the earlier scalar target defect disappears.

It still does not give a fixed-object occurrence boundary.  Canonical
endpoint/head transport sends the second selected coordinate back to e_f,
so the difference descends to zero.  Forgetting the object/head/word tags
without transport gives e_f-e_{tau f}, but this is the noncanonical fold
already isolated by the endpoint-role groupoid gate: it lowers fixed-source
H0 and is a chain map only after the desired odd comparison is supplied.

The checker also enumerates the two quadratic feature supports and all eight
literal first product-rule flags.  The flags cancel only after canonical
two-object transport; none cancels in the retained word/head/fine/operation
direct sum.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_direct_free_feature_selector_index_gate.py":
        "46102bc139de2754e5d1b6775a2731ae26d70f250f533b34f3bbc4f69241df08",
    "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py":
        "2b720f2a81d047454e224ec6af7ad62680c6ffeae33b6d7275cf995789bc8b8c",
    "computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py":
        "ac7f88b21976cae557ed6b4cacaeca19d5799ef7a30ac53df6dc0f0ab08b0f93",
    "computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py":
        "24c5504111da4f284d9d01a535de544a44ea1bae75430d98761e093cc6ca8482",
    "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py":
        "c0a34736979eb8a5d059dce30224b3d22f3930e9afaf07916dbbf51b3539c15d",
}
EXPECTED_LEDGER_SHA256 = (
    "148738356fd104ad32ead0ca2d93f4658beac57943acb670225d246d4018fdff"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def unit(width: int, index: int) -> tuple[Q, ...]:
    return tuple(Q(position == index) for position in range(width))


def rank(columns: tuple[tuple[Q, ...], ...] | list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    columns = tuple(tuple(map(Q, column)) for column in columns)
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[columns[column][row] for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def swap_endpoints(matching, euler):
    permutation = {euler.P: euler.S, euler.S: euler.P}
    return tuple(sorted(
        euler.edge(permutation.get(left, left),
                   permutation.get(right, right))
        for left, right in matching
    ))


def direct_sum_selector_audit(euler, selector) -> tuple[dict[str, object], dict[str, object]]:
    selector_ledger, selector_digest = selector.audit()
    require(selector_digest == selector.EXPECTED_DIGEST
            and selector_ledger["pointed_feature_identity"]
                == "Q_(0,1)*X_23=Q_(0,1)*X_45=e_f",
            "the direct-free quadratic selector changed")

    occurrences = tuple(euler.OCCURRENCES)
    size = len(occurrences)
    require(size == 90, size)
    index = {matching: position for position, matching in enumerate(occurrences)}
    tau = tuple(index[swap_endpoints(matching, euler)]
                for matching in occurrences)
    require(all(tau[tau[position]] == position and tau[position] != position
                for position in range(size)),
            "endpoint transpose stopped acting freely")

    f = euler.MARKED_INDEX
    tf = tau[f]
    mate = occurrences[tf]
    mate_name = "|".join(
        "".join(euler.NAMES[vertex] for vertex in edge)
        for edge in mate
    )
    require(mate_name == "P1|S0|23|45", mate_name)

    P0 = euler.edge(euler.P, euler.ZERO)
    S1 = euler.edge(euler.S, euler.ONE)
    P1 = euler.edge(euler.P, euler.ONE)
    S0 = euler.edge(euler.S, euler.ZERO)
    q23 = euler.edge(euler.TWO, euler.THREE)

    def indicator(predicate) -> tuple[Q, ...]:
        return tuple(Q(bool(predicate(matching))) for matching in occurrences)

    q01 = indicator(lambda matching: P0 in matching and S1 in matching)
    q10 = indicator(lambda matching: P1 in matching and S0 in matching)
    x23 = indicator(lambda matching: q23 in matching)
    selected_plus = tuple(a * b for a, b in zip(q01, x23, strict=True))
    selected_minus = tuple(a * b for a, b in zip(q10, x23, strict=True))
    e_f = unit(size, f)
    e_tf = unit(size, tf)
    require(selected_plus == e_f and selected_minus == e_tf
            and tuple(map(int, (sum(q01), sum(q10), sum(x23),
                                sum(selected_plus), sum(selected_minus))))
                == (3, 3, 12, 1, 1),
            "the paired quadratic selectors stopped being pointed")

    complete = (Q(1),) * size
    antisymmetric_complete = complete + scale(-1, complete)
    selected_pair = selected_plus + scale(-1, selected_minus)
    diagonal_selector = q01 + q10
    diagonal_x23 = x23 + x23
    selected_from_complete = tuple(
        response * q * x for response, q, x in
        zip(antisymmetric_complete, diagonal_selector, diagonal_x23,
            strict=True)
    )
    require(selected_from_complete == selected_pair,
            "the antisymmetric selected shadow changed")

    zero_mixed_target = (Q(0),) * (2 * size)
    require(dot(zero_mixed_target, antisymmetric_complete) == 0
            and dot(zero_mixed_target, selected_pair) == 0,
            "a mixed-head target scalar appeared")

    data = {
        "occurrences_per_head": size,
        "plus_object": {
            "word": "w", "head": "01",
            "operation": "Q_(0,1) X_23",
            "fine": "P0|S1|23|45",
        },
        "transpose_object": {
            "word": "tau(w)", "head": "10",
            "operation": "Q_(1,0) X_23",
            "fine": mate_name,
        },
        "antisymmetric_equation": "R_01(w)-R_10(tau w)",
        "selected_shadow_in_direct_sum": "(e_f,-e_tau_f)",
        "support_counts_per_object": {
            "complete": 90, "Q_ordered_endpoint": 3,
            "X_23": 12, "Q_X23_top": 1,
        },
        "support_counts_two_object": {
            "complete": 180, "Q_ordered_endpoint": 6,
            "X_23": 24, "Q_X23_top": 2,
        },
        "unselected_support_per_object": {
            "Q_minus_top": 2, "X23_minus_top": 11,
        },
        "mixed_GHZ_target_R01": 0,
        "mixed_GHZ_target_R10": 0,
        "selected_odd_target": 0,
        "scalar_target_obstruction_removed": True,
    }
    vectors = {
        "tau": tau,
        "marked_index": f,
        "selected_pair": selected_pair,
        "raw_odd": add(e_f, scale(-1, e_tf)),
    }
    return data, vectors


def two_object_descent_audit(vectors: dict[str, object]) -> dict[str, object]:
    tau = tuple(vectors["tau"])
    marked_index = int(vectors["marked_index"])
    selected_pair = tuple(vectors["selected_pair"])
    raw_odd = tuple(vectors["raw_odd"])
    size = len(tau)

    bars = []
    for index in range(size):
        bars.append(add(
            scale(-1, unit(2 * size, index)),
            unit(2 * size, size + tau[index]),
        ))
    require(rank(bars) == size
            and selected_pair == scale(-1, bars[marked_index]),
            "the selected pair stopped being one relative groupoid bar")

    def canonical_fold(vector: tuple[Q, ...]) -> tuple[Q, ...]:
        answer = [Q(0)] * size
        for index in range(size):
            answer[index] += vector[index]
            answer[tau[index]] += vector[size + index]
        return tuple(answer)

    def raw_fold(vector: tuple[Q, ...]) -> tuple[Q, ...]:
        return tuple(vector[index] + vector[size + index]
                     for index in range(size))

    canonical_images = tuple(canonical_fold(bar) for bar in bars)
    raw_images = tuple(raw_fold(bar) for bar in bars)
    require(all(not any(image) for image in canonical_images)
            and canonical_fold(selected_pair) == (Q(0),) * size
            and raw_fold(selected_pair) == raw_odd
            and rank(raw_images) == size // 2,
            "the canonical/raw fold comparison changed")

    groupoid_h0 = 2 * size - rank(bars)
    raw_fixed_h0 = size - rank((raw_odd,))
    graph_boundary = raw_odd + (Q(-1),)
    graph_h0 = size + 1 - rank((graph_boundary,))
    require((groupoid_h0, raw_fixed_h0, graph_h0) == (90, 89, 90),
            (groupoid_h0, raw_fixed_h0, graph_h0))

    return {
        "honest_location": "two-object word/head groupoid",
        "C0_dimension": 2 * size,
        "bar_rank": rank(bars),
        "groupoid_H0": groupoid_h0,
        "selected_pair_is_one_bar_boundary": True,
        "canonical_transport": (
            "(tau(w),10,Q_(1,0),tau f) -> "
            "(w,01,Q_(0,1),f)"
        ),
        "canonical_fixed_source_image": 0,
        "raw_nontransported_fold": "e_f-e_tau_f",
        "raw_odd_fold_rank_over_all_occurrences": rank(raw_images),
        "fixed_source_H0_before_after_raw_selected_relation": [90, raw_fixed_h0],
        "minimal_H0_preserving_relative_repair":
            "d b=(e_f-e_tau_f)-u^-",
        "minimal_relative_repair_H0": graph_h0,
        "first_failure": (
            "the fold needed for W_odd forgets the head/word/operation "
            "object without applying its endpoint-label transport"
        ),
    }


def product_rule_face_audit() -> dict[str, object]:
    # We list ordinary product-rule flags.  Koszul signs can be restored by
    # orienting each object's four directions; the direct-sum noncancellation
    # and the canonical tau pairing are independent of that convention.
    plus = [
        "+ dP0*S1*q23*q45",
        "+ P0*dS1*q23*q45",
        "+ P0*S1*dq23*q45",
        "+ P0*S1*q23*dq45",
    ]
    minus = [
        "- dP1*S0*q23*q45",
        "- P1*dS0*q23*q45",
        "- P1*S0*dq23*q45",
        "- P1*S0*q23*dq45",
    ]
    canonical_pairs = [
        [plus[0], minus[1]],
        [plus[1], minus[0]],
        [plus[2], minus[2]],
        [plus[3], minus[3]],
    ]
    require(len(set(plus + minus)) == 8
            and all(len(pair) == 2 for pair in canonical_pairs),
            "the first product-rule flag inventory changed")
    return {
        "literal_first_flags": plus + minus,
        "literal_flag_count": 8,
        "retained_direct_sum_cancellations": 0,
        "canonical_tau_pairs": canonical_pairs,
        "canonical_transport_after_pairing": "four zero pairs",
        "lower_q23_raw_face": (
            "P0|S1|45 - P1|S0|45, with heads 01 and 10 retained"
        ),
        "lower_q45_raw_face": (
            "P0|S1|23 - P1|S0|23, with heads 01 and 10 retained"
        ),
        "endpoint_raw_faces": [
            "dP0*S1 - dP1*S0", "P0*dS1 - P1*dS0",
        ],
        "word_head_operation_guard": (
            "before transport the plus flags lie at (w,01,Q_(0,1)) and "
            "the minus flags at (tau w,10,Q_(1,0)); equality of their "
            "scalar targets does not identify these idempotents"
        ),
        "relative_face_repair_needed": (
            "one transported odd carrier u^- for every retained Boolean "
            "face; the two marked q faces are the order-two W_odd copies"
        ),
    }


def dependency_scope_audit(quadratic, groupoid, order2) -> dict[str, object]:
    quadratic_ledger, quadratic_digest = quadratic.audit()
    groupoid_ledger, groupoid_digest = groupoid.audit()
    order2_ledger, order2_digest = order2.audit()
    require(quadratic_digest == quadratic.EXPECTED_LEDGER_SHA256
            and groupoid_digest == groupoid.EXPECTED_LEDGER_SHA256
            and order2_digest == order2.EXPECTED_LEDGER_SHA256,
            "a dependency ledger changed")
    prior_scalar = groupoid_ledger["pointed_basepoint_and_target"]
    orientation = order2_ledger["parity_decomposition"]
    require(prior_scalar["condition_forced_by_complete_response"] is False
            and orientation["primitive_orientation"]
                == "o_f=e_f-e_tau_f"
            and quadratic_ledger["quadratic_coefficient_top_and_physical_faces"][
                "coefficient_identity"]
                == "Q_(0,1)*X_23=Q_(0,1)*X_45=e_f",
            "the prior odd-selector interface changed")
    return {
        "improvement_over_single_head_selector": (
            "the ordered mixed-head difference has target zero termwise; "
            "there is no f_tau(x)-f(x) scalar target debt"
        ),
        "unchanged_gate": (
            "the endpoint/head transpose remains a flat two-object "
            "transport, not a fixed-object boundary"
        ),
        "required_fixed_source_class":
            orientation["primitive_orientation"],
        "physical_terminal_claimed": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    euler = load(
        "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py",
        "mixed_head_wodd_euler",
    )
    selector = load(
        "computations/verify_h3_direct_free_feature_selector_index_gate.py",
        "mixed_head_wodd_selector",
    )
    quadratic = load(
        "computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py",
        "mixed_head_wodd_quadratic",
    )
    groupoid = load(
        "computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py",
        "mixed_head_wodd_groupoid",
    )
    order2 = load(
        "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py",
        "mixed_head_wodd_order2",
    )

    selected, vectors = direct_sum_selector_audit(euler, selector)
    ledger = {
        "theorem": "h3 mixed-head antisymmetric quadratic W_odd gate",
        "pins": PINS,
        "selected_two_object_shadow": selected,
        "descent_and_H0": two_object_descent_audit(vectors),
        "unselected_and_product_rule_faces": product_rule_face_audit(),
        "comparison_with_prior_gates": dependency_scope_audit(
            quadratic, groupoid, order2
        ),
        "verdict": (
            "The quadratic selector on R_01(w)-R_10(tau w) is an exact "
            "source-valid relative two-object bar and its mixed target is "
            "zero.  It is not a literal fixed-source W_odd column.  "
            "Canonical head/word transport sends its selected shadow to "
            "zero; the raw fold giving e_f-e_tau_f forgets the retained "
            "object grades and lowers fixed-source H0 from 90 to 89.  All "
            "eight first product-rule flags remain distinct before the "
            "same transport.  Thus the scalar target obstruction is "
            "removed, but one H0-preserving endpoint-odd graph carrier "
            "with its four transported face families is still the first "
            "missing physical datum."
        ),
        "scope": (
            "exact rational direct-free h=3 occurrence and two-object "
            "word/head audit.  It tests the coefficient selector, target, "
            "H0 and first product-rule faces; it does not claim a full "
            "augmented q/anchor/residue terminal."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("mixed-head antisymmetric selector: EXACT TWO-OBJECT BAR")
    print("mixed target: ZERO; SCALAR DEFECT REMOVED")
    print("canonical fixed-source descent: ZERO")
    print("raw W_odd fold: LOWERS H0 90 -> 89")
    print("first product-rule flags: 8 DISTINCT BEFORE TRANSPORT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
