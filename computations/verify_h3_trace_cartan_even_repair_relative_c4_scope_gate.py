#!/usr/bin/env python3
"""Audit whether the odd relative-C4 primitive also closes tau_plus.

The coarse protected signature required by the even repair is the same
U=(occurrence=1, ainc=W=target=ores=0) isolated in the rootless primitive-
anchor lane.  At that coarse level, any protected-zero augmentation-one C4
primitive can be translated by the augmentation-zero M_v/collision span to
the desired tail r=(B1+B4)/2.

This does not yet construct the physical repair.  For every one of the 16
maximal tau_plus site collapses, all single-C4 replacements of either omitted
label land only in {B0,B3} or {B2,B5}; none lands in the deficient fixed
columns B1,B4.  The omitted labels also have repeated grades 01/04 or 12/24,
whereas the tau_minus shared-loop cells have repeated grade 02.  Therefore
the same family closes both gates only under a tail-covariant, same-grade
translation hypothesis.

The anchor-kernel dichotomy cannot supply that hypothesis: its five coarse
rows forget the six-column tail.  Nonzero anchor indeterminacy is already a
relative-generator proof exit, but zero indeterminacy gives no U; even a
coarse physical U has a five-dimensional affine fibre of possible tails.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py":
        "f0801bfcd5362f2fc8d9a81bf85a84b2d380fd37cbbe7db2252b352b785d5474",
    "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py":
        "bd20b6320172f846d7c4aa38ec6ebba0c0cfea4c056b8758df19d31b5ab20231",
    "computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py":
        "7abab46d3ae648dd309c2fec3266e70dec5b95c5fd150fea2c8c6035840e9bd3",
    "computations/verify_h3_component_iv_collision_family_normal_jet_interface.py":
        "a777687ed775c73b10129c0bee32b59f12fa3b579de39e6c4154e5ed94634651",
}
EXPECTED_LEDGER_SHA256 = (
    "a1612c0085b4b88081781a9b86f200a90c4cf730fc5d960198fb8629dad32e63"
)


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


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    pivot_row = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def unit(index, size=6):
    return tuple(Q(int(position == index)) for position in range(size))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    tau = load(
        "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py",
        "even_repair_tau",
    )
    shared = load(
        "computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py",
        "even_repair_shared",
    )
    abcde = load(
        "computations/verify_h3_rootless_abcde_target_normalization_generator_dichotomy.py",
        "even_repair_abcde",
    )
    normal = load(
        "computations/verify_h3_component_iv_collision_family_normal_jet_interface.py",
        "even_repair_normal",
    )
    support = tau.load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "even_repair_support",
    )
    lower = support.load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "even_repair_lower",
    )
    tangent = support.load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "even_repair_tangent",
    )
    complete = support.load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "even_repair_complete",
    )
    base = support.load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "even_repair_base",
    )

    # Reconstruct U15 and the six target columns.
    key = lambda label: (label[1], label[2])
    cut_012 = frozenset(map(key, lower.lower_labels(tangent, (0, 1, 2))))
    cut_024 = frozenset(map(key, lower.lower_labels(tangent, (0, 2, 4))))
    labels = tuple(sorted(cut_012 | cut_024))
    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, target_degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    graph_index = {support.graph(multiplier): index
                   for index, (multiplier, _boundary) in enumerate(pure)}
    require(len(labels) == 15 and len(graph_index) == 6,
            "the U15/six-column interface changed")

    # Find the same sixteen maximal maps as the tau_plus theorem, then audit
    # every single-C4 matching replacement of each omitted label.
    maximal = []
    for values in product(support.TARGET_ODD, repeat=6):
        phi = dict(enumerate(values))
        if any(phi[support.RHO[site]] != support.TARGET_S[phi[site]]
               for site in range(6)):
            continue
        images = tuple(support.collapse_graph(tangent, label, phi)
                       for label in labels)
        valid = tuple(index for index, image in enumerate(images)
                      if image in graph_index)
        if len(valid) == 13:
            maximal.append((values, valid))
    require(len(maximal) == 16, "the maximal tau_plus family changed")

    c4_records = []
    all_c4_targets = set()
    omitted_labels = set()
    for values, valid in maximal:
        phi = dict(enumerate(values))
        invalid = tuple(sorted(set(range(15)) - set(valid)))
        target_sets = []
        for label_index in invalid:
            label = labels[label_index]
            omitted_labels.add(label)
            matching = tangent.MATCHINGS[label[0]]
            candidates = []
            for candidate_index, candidate in enumerate(tangent.MATCHINGS):
                if len(set(matching) & set(candidate)) != 1:
                    continue
                image = support.collapse_graph(
                    tangent, (candidate_index, candidate[0]), phi
                )
                if image in graph_index:
                    candidates.append((candidate_index, graph_index[image]))
            require(len(candidates) == 4,
                    ("the omitted-label C4 census changed", values, label,
                     candidates))
            targets = tuple(sorted(set(target for _candidate, target
                                       in candidates)))
            require(targets in ((0, 3), (2, 5)),
                    ("a local C4 acquired a fixed-column target", targets))
            require(not set(targets) & {1, 4},
                    "a local C4 directly supplied B1 or B4")
            all_c4_targets.update(targets)
            target_sets.append(targets)
        require(set(target_sets) == {(0, 3), (2, 5)},
                "the omitted rho-pair stopped seeing complementary C4 orbits")
        c4_records.append({
            "phi": list(values),
            "omitted": [
                [labels[index][0], list(labels[index][1])]
                for index in invalid
            ],
            "single_C4_target_sets": [list(targets)
                                      for targets in target_sets],
        })
    require(all_c4_targets == {0, 2, 3, 5},
            "the complete omitted-label C4 target inventory changed")
    require({edge for _matching, edge in omitted_labels}
            == {(0, 1), (0, 4), (1, 2), (2, 4)},
            "the tau_plus omitted repeated grades changed")
    require(all(edge != (0, 2) for _matching, edge in omitted_labels),
            "a tau_plus omitted label entered the tau_minus shared grade")

    # Coarse target algebra: the desired repair has augmentation one.  The
    # exact M_v/collision family spans ker(augmentation), so any unit C4
    # primitive could be translated to r -- but only in the same source
    # word/fine/repeated grade.
    desired_tail = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    augmentation = (Q(1),) * 6
    zero_aug = [
        tuple(left - right for left, right in
              zip(unit(i), unit(j), strict=True))
        for i, j in combinations(range(6), 2)
    ]
    require(sum(desired_tail) == 1 and rank(zero_aug) == 5,
            "the augmentation-one/zero decomposition changed")
    translations = {}
    for index in all_c4_targets:
        correction = tuple(left - right for left, right in
                           zip(desired_tail, unit(index), strict=True))
        require(sum(correction) == 0
                and rank(zero_aug + [correction]) == 5,
                "a C4 unit could not be translated to the desired tail")
        translations[str(index)] = [str(value) for value in correction]
    require(shared.rank([tuple(vector) for vector in zero_aug]) == 5,
            "the shared-repair augmentation-zero theorem changed")

    # The abcde alternative sees only five coarse readouts.  Both r and e0
    # lift the same coarse U, so it cannot select the deficient B1/B4 tail.
    x = tuple(Q(value) for value in (1, -1, 0, 0, 0))
    coarse_u = tuple(Q(value) for value in (1, 0, 0, 0, 0))
    u_from_r = (sum(desired_tail), Q(0), Q(0), Q(0), Q(0))
    u_from_e0 = (sum(unit(0)), Q(0), Q(0), Q(0), Q(0))
    require(x == tuple(map(Q, abcde.generator_dichotomy()["clean_lower_lift_x"]))
            and u_from_r == u_from_e0 == coarse_u,
            "the coarse U fibre changed")
    tail_kernel = [
        tuple(left - right for left, right in zip(unit(i), unit(0), strict=True))
        for i in range(1, 6)
    ]
    require(rank(tail_kernel) == 5
            and all(sum(vector) == 0 for vector in tail_kernel),
            "the coarse U tail fibre stopped having dimension five")

    edges, anchor, aggregate = normal.c5_incidence_audit()
    require(normal.rank(edges) == 4
            and normal.rank(edges + [anchor]) == 5
            and aggregate == (1, 1, 1, 1, 1),
            "the conditional primitive-anchor interface changed")

    ledger = {
        "theorem": "even trace repair versus primitive relative C4 scope",
        "pins": PINS,
        "tau_plus_local_C4_census": {
            "maximal_site_collapses": len(maximal),
            "records": c4_records,
            "all_direct_C4_targets": sorted(all_c4_targets),
            "direct_targets_B1_or_B4": False,
            "tau_plus_omitted_repeated_grades": [
                list(edge) for edge in sorted(
                    {edge for _matching, edge in omitted_labels}
                )
            ],
            "tau_minus_shared_repeated_grade": [0, 2],
            "same_source_grade": False,
        },
        "coarse_positive_interface": {
            "desired_tail": [str(value) for value in desired_tail],
            "desired_augmentation": str(sum(desired_tail)),
            "augmentation_zero_span_rank": rank(zero_aug),
            "translations_from_each_direct_C4_unit": translations,
            "conditional_sufficiency": (
                "one protected-zero augmentation-one C4 primitive in the "
                "actual omitted label grade, plus a same-grade exact "
                "augmentation-zero correction, yields (B1+B4)/2"
            ),
        },
        "anchor_indeterminacy_audit": {
            "clean_lift_x": [str(value) for value in x],
            "coarse_U": [str(value) for value in coarse_u],
            "desired_tail_and_e0_have_same_coarse_U": True,
            "coarse_U_tail_fibre_dimension": rank(tail_kernel),
            "nonzero_anchor_indeterminacy": (
                "already gives the physical relative-generator proof exit; "
                "it does not construct iota or select the B1/B4 tail"
            ),
            "zero_anchor_indeterminacy": (
                "does not construct U and hence cannot repair tau_plus"
            ),
            "conditional_physical_A": (
                "constructs coarse U=A/5 but still leaves the six-column "
                "tail in a five-dimensional affine fibre"
            ),
        },
        "normal_jet_primitive_anchor_family": {
            "C5_edge_rank": normal.rank(edges),
            "rank_with_one_vertex_anchor": normal.rank(edges + [anchor]),
            "status": (
                "the functorial primitive family would provide the right "
                "augmentation type at each jet order, but it remains a "
                "conditional source family and carries no B_i tail map"
            ),
        },
        "sharp_frontier": (
            "the tau_minus and tau_plus missing cells share the coarse "
            "protected-zero augmentation-one type.  They are one uniform "
            "family only if that primitive is covariant under the required "
            "word/fine/repeated-edge transport and admits same-grade "
            "augmentation-zero translation.  Current anchor/Fredholm and "
            "normal-jet alternatives do not prove those tail laws"
        ),
        "nonclaims": [
            "a target-module translation is not promoted to a source-valid chain",
            "the tau_minus repeated-02 cell is not identified with the tau_plus 01/04 or 12/24 cell",
            "a relative-generator exit is not called a construction of iota",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("even repair relative-C4 ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 even repair / relative-C4 scope gate: PASS")
    print("local C4 targets: B0,B2,B3,B5; direct B1/B4 targets: none")
    print("coarse protected-zero augmentation-one type: shared")
    print("same-grade augmentation-zero translation: sufficient if physical")
    print("anchor indeterminacy: generator exit or no U; tail not selected")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
