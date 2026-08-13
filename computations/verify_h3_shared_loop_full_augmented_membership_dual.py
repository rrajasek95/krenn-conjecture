#!/usr/bin/env python3
"""Solve the full augmented membership problem for the shared-loop repairs.

The fixed and paired Gate-I repairs ask for, respectively, one complete
90-term pure boundary B_i or one half-sum of two disjoint such boundaries,
with Eq, W, target, ainc, ordinary residue, and eta/sigma all zero.

This checker first rebuilds the canonical faces-(3,5) component: 288
columns/rank 288, six pure 90-term boundaries, and one private feature for
each pure column.  It then forms a deliberately enlarged augmented source
inventory.  Besides the actual r0/T/rho columns, it grants the recorded
Cartan/M_v augmented signatures, all fifteen complete collision differences,
and all six
labelwise pure-residue sections.  The latter sections are not constructed;
granting them makes the negative result stronger.

On the decisive quotient, the physical covector

    nu = sum_i private_Bi + ainc

kills every granted column, including the eta/sigma-bearing Cartan/M_v
columns, but evaluates to one on every normalized fixed or paired repair.
With the lower-row orientation of the first-flat theorem, nu=-Lambda.
Thus no committed product-rule, Spencer, or third-Bianchi inventory supplies
either repair.  After granting the labelwise residue sections, the smallest
missing correction has (literal, Eq, ainc)=(0,-u,+1).
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
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py":
        "96280ef01c70b4f3381e6d85d2c9fb64b1620850305a4346601fccbd7d63dc44",
    "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py":
        "cc551585391a990060f78b49486c05af6c3b4a301058c855a422ae9d54fe5be5",
    "computations/verify_h3_beta_zero_d0_unary_third_bianchi_membership_gate.py":
        "2b1bead205d5c766ffff6a0ab9a4d39a5d5ba8308bc0e96d70c1bc7974e00677",
}
EXPECTED_LEDGER_SHA256 = (
    "da3a04511fb4695bf6921c47be2b20d017823a8fc01a3057c9daa462424ccd5f"
)

N = 6
LOWER = slice(0, N)
EQ = slice(N, 2 * N)
W = slice(2 * N, 3 * N)
TARGET = slice(3 * N, 4 * N)
ORES = slice(4 * N, 5 * N)
AINC = 5 * N
TERMINAL = slice(AINC + 1, AINC + 8)
BARE_Q = slice(TERMINAL.stop, TERMINAL.stop + N)
SCALAR_ORES = BARE_Q.stop
ROWS = SCALAR_ORES + 1
TERMINAL_PACKET = (Q(1), Q(1), Q(1), Q(1), Q(1), Q(1), Q(-1))


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


def unit(index: int) -> tuple[Q, ...]:
    return tuple(Q(int(position == index)) for position in range(N))


def vector(*, lower=(), eq=(), w=(), target=(), ores=(), ainc=0,
           terminal=(), bare_q=(), scalar_ores=0) -> tuple[Q, ...]:
    answer = [Q(0)] * ROWS
    for section, values in ((LOWER, lower), (EQ, eq), (W, w),
                            (TARGET, target), (ORES, ores),
                            (TERMINAL, terminal), (BARE_Q, bare_q)):
        for index, value in enumerate(values):
            answer[section.start + index] = Q(value)
    answer[AINC] = Q(ainc)
    answer[SCALAR_ORES] = Q(scalar_ores)
    return tuple(answer)


def add(*columns):
    return tuple(sum((Q(column[row]) for column in columns), Q(0))
                 for row in range(ROWS))


def scale(value, column):
    return tuple(Q(value) * Q(entry) for entry in column)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns):
    if not columns:
        return 0
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(ROWS)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, ROWS)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(ROWS):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [left - multiple * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def sparse_add(boundaries, coefficients):
    answer = defaultdict(Q)
    for coefficient, boundary in zip(coefficients, boundaries, strict=True):
        for feature in boundary:
            answer[feature] += Q(coefficient)
    return {feature: value for feature, value in answer.items() if value}


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "shared_full_complete")
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "shared_full_base")
    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "shared_full_literal")
    anchor = load(
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py",
        "shared_full_anchor")
    hasse = load(
        "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py",
        "shared_full_hasse")

    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, degree)
    pure = tuple((index, multiplier, boundary)
                 for index, (word, multiplier, boundary)
                 in enumerate(component["columns"])
                 if word == complete.PURE_WORD)
    require((left, right) == (3, 5)
            and len(component["columns"]) == component["rank"] == 288
            and len(pure) == N,
            "the canonical complete component changed")

    owners = defaultdict(list)
    for column_index, (_word, _multiplier, boundary) in enumerate(
            component["columns"]):
        for feature in boundary:
            owners[feature].append(column_index)
    private = []
    private_counts = []
    for column_index, _multiplier, boundary in pure:
        choices = sorted(feature for feature in boundary
                         if owners[feature] == [column_index])
        require(choices, ("a pure column lost private features", column_index))
        private.append(choices[0])
        private_counts.append(len(choices))
    boundaries = tuple(boundary for _index, _multiplier, boundary in pure)
    require(all(len(boundary) == 90 for boundary in boundaries)
            and len({feature for boundary in boundaries for feature in boundary})
                == 540,
            "the six literal 90-term boundaries changed")

    # The augmented envelope.  Collision and pure-residue columns are
    # deliberately granted labelwise although that source typing is open.
    # Likewise all Cartan/M_v signatures are granted as abstract columns:
    # the external repair-1 audit challenges their termwise private/terminal
    # realization, so they are safe overgrants for this negative theorem.
    r0 = []
    target_caps = []
    split_residues = []
    pure_residues = []
    for index in range(N):
        e = unit(index)
        r0.append(vector(lower=e, eq=e, target=e, ainc=-1))
        target_caps.append(vector(w=tuple(-value for value in e), target=e))
        split_residues.append(vector(w=e, ores=e))
        pure_residues.append(vector(ores=e))

    collisions = []
    bare_q_differences = []
    for i, j in combinations(range(N), 2):
        difference = tuple(a - b for a, b in zip(unit(i), unit(j), strict=True))
        collisions.append(vector(lower=difference))
        bare_q_differences.append(vector(bare_q=difference))

    mv_columns = []
    cartan_columns = []
    alpha_vectors = []
    for selected in combinations(range(N), 4):
        alpha = [Q(0)] * N
        for coefficient, index in zip(literal.ALPHA, selected, strict=True):
            alpha[index] += coefficient
        require(sum(alpha) == 0, "an alpha placement gained augmentation")
        alpha = tuple(alpha)
        alpha_vectors.append(alpha)
        # Recorded M_v signature: literal alpha, Eq alpha, zero
        # residue/protected, terminal.  It is an overgrant here, not a claim
        # that the termwise Cartan/private comparison is settled.
        mv_columns.append(vector(lower=alpha, eq=alpha,
                                 terminal=TERMINAL_PACKET))
        # Recorded Cartan K signature, again granted as an abstract column.
        cartan_columns.append(vector(ores=alpha,
                                     terminal=TERMINAL_PACKET))

    scalar_residue = vector(scalar_ores=1)
    known_columns = (
        r0 + target_caps + split_residues + pure_residues + collisions
        + bare_q_differences + mv_columns + cartan_columns + [scalar_residue]
    )

    nu = vector(lower=(Q(1),) * N, ainc=1)
    require(all(dot(nu, column) == 0 for column in known_columns),
            "the physical six-term covector sees a granted inventory column")

    # Literal alpha packets are 360 terms, including the selected physical
    # placement B0+B2-B3-B5.
    alpha_supports = []
    for alpha in alpha_vectors:
        aggregate = sparse_add(boundaries, alpha)
        require(len(aggregate) == 360,
                ("an M_v literal aggregate changed", alpha, len(aggregate)))
        alpha_supports.append(len(aggregate))

    candidates = {
        "fixed_B1": unit(1),
        "fixed_B4": unit(4),
        "paired_B0_B5": tuple(Q(int(index in (0, 5)), 2)
                               for index in range(N)),
        "paired_B2_B3": tuple(Q(int(index in (2, 3)), 2)
                               for index in range(N)),
    }
    base_rank = rank(known_columns)
    candidate_records = {}
    for name, u in candidates.items():
        desired = vector(lower=u)
        literal_target = sparse_add(boundaries, u)
        require(sum(u) == 1 and dot(nu, desired) == 1
                and rank(known_columns + [desired]) == base_rank + 1,
                ("a shared repair entered the augmented envelope", name))

        R = add(*(scale(value, column)
                  for value, column in zip(u, r0, strict=True)))
        T = add(*(scale(value, column)
                  for value, column in zip(u, target_caps, strict=True)))
        rho = add(*(scale(value, column)
                    for value, column in zip(u, split_residues, strict=True)))
        d_ores = add(*(scale(value, column)
                       for value, column in zip(u, pure_residues, strict=True)))
        near_hit = add(R, scale(-1, T), scale(-1, rho), d_ores)
        expected_near_hit = vector(lower=u, eq=u, ainc=-1)
        require(near_hit == expected_near_hit and dot(nu, near_hit) == 0,
                ("the strongest target/residue near-hit changed", name))
        missing = add(desired, scale(-1, near_hit))
        require(missing == vector(eq=tuple(-value for value in u), ainc=1)
                and dot(nu, missing) == 1,
                ("the minimal augmented correction changed", name))

        candidate_records[name] = {
            "u": [str(value) for value in u],
            "literal_boundary_features": len(literal_target),
            "literal_coefficients": sorted({str(value)
                                             for value in literal_target.values()}),
            "desired_Eq_W_target_ainc_ores_terminal": [0, 0, 0, 0, 0, 0],
            "nu_on_desired": 1,
            "rank_before_after_adjoining": [base_rank, base_rank + 1],
            "strongest_near_hit": "R_u-T_u-rho_u+d_ores,u",
            "near_hit_literal_Eq_ainc": ["B_u", "u", -1],
            "minimal_missing_after_grants": {
                "literal": 0,
                "Eq": [str(-value) for value in u],
                "ainc": 1,
                "W_target_ores_terminal": [0, 0, 0, 0],
            },
        }

    anchor_ledger = anchor.audit()
    require(anchor_ledger["physical_covector"]
            == "Lambda=sum_6 selected matching rows - ainc"
            and anchor_ledger["pairings"]["complete_288_repeated_columns"]
                == [0]
            and anchor_ledger["pairings"]
                ["complete_8580_first_flat_operator_columns"] == 0
            and anchor_ledger["pairings"]["known_relative_alpha_cell"] == 0,
            "the physical first-flat separator changed")

    hasse_ledger, hasse_digest = hasse.audit()
    require(hasse_digest == hasse.EXPECTED_LEDGER_SHA256
            and hasse_ledger["formal_totalization"]["source_valid"] is False
            and hasse_ledger["formal_totalization"]
                ["tail_signature_ainc_W_target_ores"] == [-1, 0, 0, 0]
            and hasse_ledger["third_Bianchi_carrier"]["common_marked_word"]
                == "222000",
            "the product-rule/third-Bianchi source obstruction changed")

    ledger = {
        "theorem": "full augmented fixed/paired shared-loop membership dual",
        "pins": PINS,
        "canonical_complete_component": {
            "faces": [left, right],
            "fine_degree": list(degree),
            "columns_rank": [len(component["columns"]), component["rank"]],
            "literal_boundary_features": len(owners),
            "literal_boundary_incidences": sum(
                len(boundary) for _word, _multiplier, boundary
                in component["columns"]),
            "pure_boundaries": N,
            "features_per_pure_boundary": 90,
            "disjoint_pure_union": 540,
            "private_features_per_pure_min_max": [
                min(private_counts), max(private_counts)],
            "selected_private_features": [repr(feature) for feature in private],
        },
        "augmented_rows": {
            "row_order": (
                "private_B0..B5, Eq_B0..B5, W_B0..B5, target_B0..B5, "
                "ores_B0..B5, ainc, eta1..eta5 constants, eta1_U1, "
                "sigma_qpq22, bare_Q_B0..B5, scalar_ores"
            ),
            "rows": ROWS,
            "eta_sigma_packet": [str(value) for value in TERMINAL_PACKET],
        },
        "strong_augmented_envelope": {
            "columns": len(known_columns),
            "rank": base_rank,
            "families": {
                "r0_T_rho": [len(r0), len(target_caps), len(split_residues)],
                "granted_labelwise_pure_ores": len(pure_residues),
                "granted_complete_collision_differences": len(collisions),
                "physical_bare_Q_endpoint_differences": len(bare_q_differences),
                "all_recorded_Mv_alpha_signatures": len(mv_columns),
                "all_recorded_Cartan_alpha_signatures": len(cartan_columns),
                "aggregate_scalar_ores": 1,
            },
            "literal_Mv_supports": sorted(set(alpha_supports)),
            "strengthening": (
                "the six labelwise pure-ores sections and all fifteen "
                "complete collision differences are granted even though the "
                "committed source presentation does not construct them"
            ),
        },
        "repair_membership": candidate_records,
        "primitive_physical_dual": {
            "reduced_formula": "nu=sum_i private_Bi+ainc",
            "first_flat_identification": "nu=-Lambda after orienting lower=-literal matching boundary",
            "kills_full_granted_augmented_envelope": True,
            "kills_complete_288_and_order6_8580_blocks": True,
            "kills_granted_eta_sigma_bearing_Mv_and_Cartan_signatures": True,
            "fixed_and_paired_values": 1,
        },
        "inventory_search": {
            "product_rule": (
                "constructs exactly the fixed/pair occurrence directions, "
                "but not a physical source column"
            ),
            "third_Bianchi": (
                "marked word 222000; rho adds a complementary word; the "
                "formal tail has ainc=-1 plus endpoint/Omega defects"
            ),
            "Spencer_order6": (
                "the pinned physical first-flat block is killed by nu; its "
                "known endpoint-odd alpha image has augmentation and ainc zero"
            ),
            "actual_image_found": False,
        },
        "sharp_frontier": (
            "neither fixed nor paired repair is in the complete augmented "
            "committed inventory, even after the displayed overgrants.  "
            "After granting labelled residue cancellation, one new relative "
            "column must carry Eq=-u and physical ainc=+1 with every other "
            "listed row zero.  Equivalently, any larger source extension "
            "must break the primitive physical dual nu; nonzero pairing is "
            "the relative-generator branch, while zero pairing leaves nu as "
            "the bounded Fredholm separator"
        ),
        "scope": (
            "exact canonical h=3 faces-(3,5), normalized Y=1 component and "
            "the named physical/product-rule/Spencer/third-Bianchi inventories. "
            "The dual is bounded against these inventories, not an annihilator "
            "of arbitrary future higher relative cells"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("full augmented shared-loop ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("h3 shared-loop full augmented membership: NO IMAGE IN KNOWN INVENTORY")
    print("literal targets: fixed=90 features; paired=180 features")
    print("physical dual: nu=sum private_Bi+ainc; target value=1")
    print("minimal correction after strong grants: Eq=-u, ainc=+1")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
