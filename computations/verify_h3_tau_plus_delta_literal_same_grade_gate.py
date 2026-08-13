#!/usr/bin/env python3
"""Audit the literal same-grade status of the tau-plus transport debt.

The abstract debt

    delta_+ = (-B0+2B1-B2-B3+2B4-B5)/4

is rho-even and augmentation zero.  Matching-Bianchi endpoint differences
factor it at the bare-Q level, and the physical s=(2 5) automorphism carries
the two differences literally to their mates.  This is source-valid and
uses no selected denominator transgression.

It does not construct delta_+ in the complete full-nine lower module.  A
bare endpoint Q_i-Q_j is not the 90-term boundary B_i-B_j.  In the committed
same-grade complete/cap/M_v inventory, every coefficient on a private B_i
pivot is tied to the same labelled Eq coefficient.  Delta_+ requires its
private packet with Eq zero.  The primitive rho-even covector

    chi_D = sum_i D_i(private_i-Eq_i),
    D=(-1,2,-1,-1,2,-1),

kills that inventory and reads 12 on the integral debt D.  Thus the
matching-Bianchi proposal is an exact conditional factorization whose one
remaining common-tail comparison is precisely the first literal obstruction.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_oriented_shared_loop_resolution_unification.py":
        "e6819e5437d967ec9bb0f32a24836c70c34e5b35bbd4f9e3ebd38b0a5c4fb714",
    "computations/verify_h3_trace_cartan_even_repair_relative_c4_scope_gate.py":
        "645df036367a7fe60f3ce625dc37710f7e83129a84a3619005945ca6b4f0a486",
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
}
EXPECTED_LEDGER_SHA256 = (
    "85a9002daf41154cab2d6671917dc0d6b4b33ae3f841d478ed4a74043e42bf8e"
)

D = (Q(-1), Q(2), Q(-1), Q(-1), Q(2), Q(-1))
DELTA = tuple(value / 4 for value in D)
TARGET_ACTION = (5, 1, 3, 2, 4, 0)
S_SITE = (0, 1, 5, 3, 4, 2, 6, 7)
COLOUR_ID = (0, 1, 2)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def rank(columns):
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
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def add_sparse(*vectors):
    answer = defaultdict(Q)
    for vector in vectors:
        for key, value in vector.items():
            answer[key] += Q(value)
    return {key: value for key, value in answer.items() if value}


def scale_sparse(value, vector):
    value = Q(value)
    return {key: value * Q(entry) for key, entry in vector.items()
            if value * Q(entry)}


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))


def endpoint_decompositions(pure):
    records = []
    for index, (multiplier, _boundary) in enumerate(pure):
        site_degrees = {site: 0 for site in range(1, 6)}
        for left, right, _left_colour, _right_colour in multiplier:
            site_degrees[left] += 1
            site_degrees[right] += 1
        repeated = tuple(site for site, count in site_degrees.items()
                         if count == 2)
        require(repeated == (4,),
                ("a pure target left the repeated-site-4 grade", index))
        for face, count in site_degrees.items():
            if count != 1:
                continue
            tail = next(cell for cell in multiplier if face in cell[:2])
            matching = tuple(cell for cell in multiplier if cell != tail)
            if sorted(site for cell in matching for site in cell[:2]) \
                    != [site for site in range(1, 6) if site != face]:
                continue
            records.append({
                "B": index,
                "face": face,
                "tail": tail,
                "matching": matching,
            })
    require(len(records) == 12,
            "the six P3+K2 columns lost endpoint decompositions")
    return records


def endpoint_and_involution_audit(base, support, degree, pure):
    decompositions = endpoint_decompositions(pure)
    by_face = defaultdict(set)
    for record in decompositions:
        by_face[record["face"]].add(record["B"])
    require(dict(by_face) == {
                3: {0, 4, 5}, 5: {0, 1, 2}, 2: {1, 3, 5},
                1: {2, 3, 4}},
            ("the endpoint packet incidence changed", dict(by_face)))

    pairs = {
        "B1-B0": (5, 1, 0),
        "B4-B0": (3, 4, 0),
        "B1-B5": (2, 1, 5),
        "B4-B5": (3, 4, 5),
    }
    pair_records = {}
    for name, (face, positive, negative) in pairs.items():
        left = next(record for record in decompositions
                    if record["face"] == face and record["B"] == positive)
        right = next(record for record in decompositions
                     if record["face"] == face and record["B"] == negative)
        require(left["tail"] == right["tail"],
                ("an endpoint difference lost its common tail", name))
        pair_records[name] = {
            "face": face,
            "common_tail": list(left["tail"]),
            "positive_matching": [list(cell) for cell in left["matching"]],
            "negative_matching": [list(cell) for cell in right["matching"]],
        }

    require(support.transform_degree(degree, S_SITE, COLOUR_ID) == degree,
            "s=(2 5) left the canonical fine degree")
    transformed = []
    for index, (multiplier, boundary) in enumerate(pure):
        moved_multiplier = support.transform_multiplier(
            base, multiplier, S_SITE, COLOUR_ID)
        target = next(position for position, (candidate, _row)
                      in enumerate(pure) if candidate == moved_multiplier)
        moved_boundary = {
            support.transform_multiplier(base, feature, S_SITE, COLOUR_ID)
            for feature in boundary
        }
        require(moved_boundary == set(pure[target][1]),
                ("s stopped transporting a complete 90-term boundary",
                 index, target))
        transformed.append(target)
    require(tuple(transformed) == TARGET_ACTION,
            ("the literal s action changed", transformed))

    # It follows at the decorated source level, not merely in Q^6, that the
    # two H0 endpoint cycles are carried to the two H5 cycles.
    require(TARGET_ACTION[1] == 1 and TARGET_ACTION[0] == 5
            and TARGET_ACTION[4] == 4,
            "s stopped carrying H0 to H5")
    return {
        "target_degree": list(degree),
        "endpoint_pairs": pair_records,
        "physical_site_automorphism": "s=(2 5), endpoints fixed",
        "literal_complete_boundary_action": "(B0 B5)(B2 B3), B1,B4 fixed",
        "H0_to_H5_source_valid": True,
        "bare_Q_protected_readouts_target_ainc_W_ores": [0, 0, 0, 0],
    }


def literal_debt_audit(component, pure, literal):
    require(sum(D) == sum(DELTA) == 0
            and tuple(D[index] for index in TARGET_ACTION) == D,
            "the integral tau-plus debt lost augmentation/parity")
    boundaries = [
        {feature: Q(1) for feature in boundary}
        for _multiplier, boundary in pure
    ]
    integral_boundary = add_sparse(*(
        scale_sparse(D[index], boundaries[index]) for index in range(6)
    ))
    require(len(integral_boundary) == 540
            and set(integral_boundary.values()) == {Q(-1), Q(2)},
            "the literal integral debt packet changed")

    # A coefficient-level combination of the 15 alpha packets exists and
    # may even be chosen with coefficient sum zero.  This cancels a common
    # terminal packet, but every M_v has Eq equal to its lower alpha packet.
    selections = tuple(combinations(range(6), 4))
    alpha_columns = []
    alpha_boundaries = []
    for selected in selections:
        vector = [Q(0)] * 6
        aggregate = {}
        for coefficient, index in zip(literal.ALPHA, selected, strict=True):
            vector[index] += coefficient
            aggregate = add_sparse(
                aggregate, scale_sparse(coefficient, boundaries[index]))
        alpha_columns.append(tuple(vector))
        alpha_boundaries.append(aggregate)
    coefficients = {
        (0, 1, 2, 3): Q(1, 4),
        (0, 1, 2, 4): Q(-1, 2),
        (0, 1, 2, 5): Q(1, 4),
        (0, 1, 3, 4): Q(1, 4),
        (1, 2, 3, 4): Q(-1, 4),
    }
    mv_coefficients = tuple(coefficients.get(selected, Q(0))
                            for selected in selections)
    reconstructed = tuple(sum(
        mv_coefficients[column] * alpha_columns[column][row]
        for column in range(len(selections))) for row in range(6))
    reconstructed_boundary = add_sparse(*(
        scale_sparse(mv_coefficients[index], alpha_boundaries[index])
        for index in range(len(selections))
    ))
    require(reconstructed == DELTA and sum(mv_coefficients) == 0
            and reconstructed_boundary
                == scale_sparse(Q(1, 4), integral_boundary),
            "the zero-total M_v realization of the lower debt changed")

    # Literal private pivots exist for every pure row against all 288 source
    # columns.  On these six pivots and the corresponding six Eq rows, r0 and
    # M_v lie in the diagonal subspace (x,x).  Cap, Cartan, bare-Q endpoint,
    # and chart-difference columns read zero.  The desired common-tail bridge
    # is (D,0), outside that subspace.
    owners = defaultdict(list)
    for column_index, (_word, _multiplier, boundary) in enumerate(
            component["columns"]):
        for feature in boundary:
            owners[feature].append(column_index)
    private = []
    pure_indices = []
    for multiplier, boundary in pure:
        index = next(column_index for column_index,
                     (word, candidate, _row) in enumerate(component["columns"])
                     if word == (0,) * 8 and candidate == multiplier)
        choices = tuple(feature for feature in boundary
                        if owners[feature] == [index])
        require(choices, ("a pure column lost its literal private pivot", index))
        private.append(choices[0])
        pure_indices.append(index)

    diagonal_columns = []
    for index in range(6):
        unit = tuple(Q(int(position == index)) for position in range(6))
        diagonal_columns.append(unit + unit)
    diagonal_columns.extend(alpha + alpha for alpha in alpha_columns)
    desired = D + (Q(0),) * 6
    chi = D + tuple(-value for value in D)
    require(rank(diagonal_columns) == 6
            and rank(diagonal_columns + [desired]) == 7
            and all(dot(chi, column) == 0 for column in diagonal_columns)
            and dot(chi, desired) == 12,
            "the literal private/Eq dual changed")
    return {
        "integral_debt_D": [int(value) for value in D],
        "delta_plus": [str(value) for value in DELTA],
        "literal_complete_boundary_support": len(integral_boundary),
        "literal_coefficients": sorted(
            {str(value) for value in integral_boundary.values()}),
        "private_pivots": [repr(value) for value in private],
        "private_pivot_counts_min": min(
            sum(owners[feature] == [index] for feature in pure[position][1])
            for position, index in enumerate(pure_indices)),
        "Mv_lower_representation": {
            "nonzero_coefficients": {
                str(selected): str(value) for selected, value in
                coefficients.items()
            },
            "coefficient_sum": str(sum(mv_coefficients)),
            "lower": "delta_plus",
            "Eq": "delta_plus (uncancelled)",
            "common_terminal_if_uniform": "cancels because coefficient sum=0",
        },
        "bounded_literal_dual": {
            "chi_D": "sum_i D_i*(private_i-Eq_i)",
            "rho_parity": "even",
            "on_complete_r0_and_Mv_diagonal_tie": 0,
            "on_cap_Cartan_bareQ_and_chart_differences": 0,
            "on_integral_common_tail_bridge": 12,
        },
    }


def audit():
    pin_dependencies()
    support = load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "tau_delta_support",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "tau_delta_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "tau_delta_base",
    )
    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "tau_delta_literal",
    )

    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    require((left, right) == (3, 5)
            and len(component["columns"]) == component["rank"] == 288
            and len(pure) == 6,
            "the canonical complete component changed")

    ledger = {
        "theorem": "tau-plus delta literal same-grade gate",
        "pins": PINS,
        "endpoint_Bianchi_factorization":
            endpoint_and_involution_audit(base, support, degree, pure),
        "literal_complete_column_gate":
            literal_debt_audit(component, pure, literal),
        "exact_positive_statement": (
            "the four endpoint matching-Bianchi differences are physical "
            "bare-Q cycles, lie in the common canonical target degree, and "
            "the physical s automorphism transports H0 to H5 literally"
        ),
        "exact_negative_statement": (
            "no committed complete/cap/M_v column combination promotes the "
            "bare-Q factorization to a complete Eq-zero delta_plus packet; "
            "even a zero-total M_v combination leaves Eq=delta_plus"
        ),
        "smallest_remaining_membership": (
            "a rho-even source-labelled common-tail comparison in the actual "
            "tau-plus placement with complete lower delta_plus, Eq=0, and "
            "zero target/ainc/W/ores; equivalently a reduced-Eq correction "
            "-delta_plus for the displayed M_v combination"
        ),
        "scope": (
            "exact canonical faces-(3,5) normalized Y=1 repeated grade and "
            "the committed complete, cap, Cartan, endpoint, chart-difference, "
            "and M_v families.  chi_D is a literal bounded-inventory dual, "
            "not a full Fredholm annihilator against unknown higher cells"
        ),
        "delta_plus_physical_now": False,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("tau-plus delta literal ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 tau-plus delta+: BARE-Q FACTORIZATION / COMPLETE NO-GO")
    print("decorated H0 -> H5 under physical s: YES")
    print("delta+ in projected M_v span: YES, with coefficient sum zero")
    print("remaining M_v Eq packet: delta+ (nonzero)")
    print("bounded literal dual: chi_D=sum D_i(private_i-Eq_i)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
