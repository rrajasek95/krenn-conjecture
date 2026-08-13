#!/usr/bin/env python3
"""Unify the odd Gate-I and even trace repairs by one loop resolution.

The only labels missed by the canonical cut-collapse contain the repeated
edge 02, which becomes the forbidden loop 44.  If the two remaining edges
are ab and cd, there are two canonical loop-free C4 resolutions:

    ab | 4c | 4d,       cd | 4a | 4b.

In the canonical faces-(3,5) component these are exactly

    fixed shared label: B4 or B1,
    paired shared orbit: (B0,B5) or (B3,B2).

Thus an oriented physical loop-resolution family supplies the fixed and
paired Gate-I sections, while its even average supplies
(B1+B4)/2, the missing d_even direction.  This checker proves the exact
label/combinatorial reduction.  It does not construct the physical relative
source cell carrying either resolution.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py":
        "ba2c32a41b1d070d2af24546819e838697aba0273e85586a796ee25a27f5a950",
    "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py":
        "ea45c09a8347c312ea9721475d54a4b4f9aad21d8d51cb9d4d297aeaa99ba429",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py":
        "f0801bfcd5362f2fc8d9a81bf85a84b2d380fd37cbbe7db2252b352b785d5474",
}
EXPECTED_LEDGER_SHA256 = "33813e438b4d3d51df6867f6f0df59ee018550f9bd741f69d41cc2b0bea58e1c"


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


def resolution_graphs(loop_site, first, second):
    """Resolve loop ll with disjoint edges ab,cd in its two face directions."""
    (a, b), (c, d) = first, second
    left = tuple(sorted((first,
                         tuple(sorted((loop_site, c))),
                         tuple(sorted((loop_site, d))))))
    right = tuple(sorted((second,
                          tuple(sorted((loop_site, a))),
                          tuple(sorted((loop_site, b))))))
    return left, right


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    support = load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "oriented_loop_support",
    )
    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "oriented_loop_tangent",
    )
    lower = load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "oriented_loop_lower",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "oriented_loop_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "oriented_loop_base",
    )
    trace = load(
        "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py",
        "oriented_loop_trace",
    )

    key = lambda label: (label[1], label[2])
    cut_012 = frozenset(map(key, lower.lower_labels(tangent, (0, 1, 2))))
    cut_024 = frozenset(map(key, lower.lower_labels(tangent, (0, 2, 4))))
    shared = tuple(sorted(cut_012 & cut_024))
    require(shared == ((3, (0, 2)), (4, (0, 2)), (5, (0, 2))),
            ("the shared repeated-02 packet changed", shared))

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
    require((left, right) == (3, 5) and len(pure) == len(graph_index) == 6,
            "the canonical six-target component changed")

    # A canonical successful odd collapse.  It identifies source 0,2 at
    # target site 4 and intertwines rho with the physical target involution.
    values = (4, 2, 4, 1, 5, 3)
    require(values[0] == values[2] == 4,
            "the canonical collision stopped mapping 02 to loop 44")
    records = []
    for label in shared:
        matching_index, repeated_edge = label
        other = []
        for edge in tangent.MATCHINGS[matching_index]:
            image = tuple(sorted((values[edge[0]], values[edge[1]])))
            if edge != repeated_edge:
                other.append(image)
        require(len(other) == 2,
                ("a shared matching lost its two complementary edges", label))
        first, second = resolution_graphs(4, other[0], other[1])
        require(first in graph_index and second in graph_index,
                ("a canonical loop resolution left the pure target packet",
                 label, first, second))
        records.append((label, graph_index[first], graph_index[second]))

    require(records == [
        ((3, (0, 2)), 0, 3),
        ((4, (0, 2)), 4, 1),
        ((5, (0, 2)), 2, 5),
    ], ("the oriented loop-resolution table changed", records))

    # The middle label is rho-fixed; the outer two form one rho-pair.
    require(support.rho_label(tangent, shared[1]) == shared[1]
            and support.rho_label(tangent, shared[0]) == shared[2],
            "the fixed/pair shared-orbit decomposition changed")
    target_action = (5, 1, 3, 2, 4, 0)
    require(target_action[4] == 4 and target_action[1] == 1
            and target_action[0] == 5 and target_action[3] == 2,
            "the physical target involution changed")

    # Two oriented choices give exactly the two Gate-I alternatives.
    choice_a = {shared[1]: 4, shared[0]: 0, shared[2]: 5}
    choice_b = {shared[1]: 1, shared[0]: 3, shared[2]: 2}
    require(target_action[choice_a[shared[0]]] == choice_a[shared[2]]
            and target_action[choice_b[shared[0]]] == choice_b[shared[2]],
            "an oriented paired repair stopped being equivariant")
    fixed_a = tuple(Q(int(index == 4)) for index in range(6))
    fixed_b = tuple(Q(int(index == 1)) for index in range(6))
    pair_a = tuple(Q(int(index in (0, 5)), 2) for index in range(6))
    pair_b = tuple(Q(int(index in (2, 3)), 2) for index in range(6))

    # Even symmetrization of the fixed loop is precisely d_even.  The sum
    # over the paired orbit is its diagonal complement.
    d_even = tuple((a + b) / 2 for a, b in zip(fixed_a, fixed_b, strict=True))
    pair_even = tuple(Q(int(index in (0, 2, 3, 5)), 4)
                      for index in range(6))
    diagonal = tuple(Q(1, 6) for _index in range(6))
    require(d_even == (0, Q(1, 2), 0, 0, Q(1, 2), 0)
            and pair_even == (Q(1, 4), 0, Q(1, 4), Q(1, 4), 0, Q(1, 4))
            and tuple((d_even[index] + 2 * pair_even[index]) / 3
                      for index in range(6)) == diagonal,
            "the even loop-resolution decomposition changed")

    trace_ledger, trace_digest = trace.audit()
    require(trace_digest == trace.EXPECTED_LEDGER_SHA256
            and trace_ledger["smallest_relative_repair"]
                ["per_omitted_label_image"] == "(B1+B4)/2",
            "the tau-plus even repair target changed")

    # Hasse's product rule explains why this is the first possible local
    # source shape: for two multi-affine occurrence factors f=x+ta and
    # g=y+tb, the second divided coefficient is ab.  This verifies the
    # coefficient, not the physical comparison/terminal typing.
    x, y, a, b = Q(2), Q(3), Q(5), Q(7)
    product_coefficients = (x * y, x * b + y * a, a * b)
    require(product_coefficients == (6, 29, 35),
            "the divided Hasse cross term changed")

    ledger = {
        "theorem": "oriented shared-loop resolution unifies odd/even repairs",
        "pins": PINS,
        "shared_packet": {
            "labels": [[matching, list(edge)] for matching, edge in shared],
            "forced_loop": "02 -> 44",
            "rho_orbits": "one fixed label 4 and one pair 3<->5",
        },
        "oriented_resolution_table": [
            {"label": [label[0], list(label[1])],
             "first_B": first, "second_B": second}
            for label, first, second in records
        ],
        "Gate_I_choices": {
            "choice_A": "fixed B4 and paired (B0+B5)/2",
            "choice_B": "fixed B1 and paired (B2+B3)/2",
            "consequence": (
                "one source-valid oriented loop-resolution family supplies "
                "both d_fixed and d_pair"
            ),
        },
        "generic_even_choice": {
            "fixed_symmetrization": [str(value) for value in d_even],
            "equals": "(B1+B4)/2=d_even",
            "paired_symmetrization": [str(value) for value in pair_even],
            "consequence": (
                "the same oriented family, averaged over its two local "
                "resolutions, supplies the tau-plus labelled residue section"
            ),
        },
        "Hasse_cross_term": {
            "identity": "[t^2](x+t*a)(y+t*b)=a*b",
            "interpretation": (
                "the loop resolution has the shape of the first divided "
                "Hasse cross term for the two collapsed occurrence factors"
            ),
        },
        "sharp_remaining_statement": (
            "construct one physical oriented diagonal/loop-resolution "
            "relative cell with the displayed images, the canonical word/"
            "fine/repeated labels, and zero protected lower/W/target/ainc "
            "apart from its labelled ordinary-residue boundary"
        ),
        "nonclaims": [
            "the combinatorial resolution is not yet a physical source chain",
            "the Hasse coefficient alone does not define the comparison to the augmented correction complex",
            "the beta-zero selected-colour order-three cell is not constructed",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("oriented loop-resolution ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 oriented shared-loop resolution: EXACT UNIFICATION")
    print("fixed label: B4 or B1")
    print("paired orbit: (B0,B5) or (B3,B2)")
    print("even average: (B1+B4)/2")
    print("physical relative loop-resolution cell: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
