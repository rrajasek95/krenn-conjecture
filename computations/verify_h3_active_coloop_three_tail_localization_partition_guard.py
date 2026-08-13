#!/usr/bin/env python3
"""Audit localization/partition attempts for arbitrary active-coloop entry.

Write the normalized residual cofactor as

    alpha*C=1,   C=t1+t2+t3.

The principal opens D(t_i) cover the coloop chart and
lambda_i=alpha*t_i form a polynomial partition of unity.  But the special
processor lives on the sparse axis stratum (at most one t_i nonzero), not on
D(t_i).  Localizing at one tail leaves the other two free.

The exact obstruction is the rank-two relative tail cotangent

    dt1+dt2+dt3=0.

At the symmetric normalized point t_i=1/3, all three opens meet.  Aggregate
rows have rank one, normalized local selectors disagree on overlaps modulo
that row, and partition recombination returns only the aggregate.  A
logarithmic coordinate projector has scalar face alpha*t_i, so it is not
source-valid.  Thus alpha*C=1 plus closed-shore support does not extend the
sparse processor; two tail-asymmetric physical rows, or an equivalent
pointed cofactor-tail comparison, are the first missing datum.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_literal_packet_termination_scope.py":
        "ad369a692aa2a7bde3b30a0a4cba5e401b6e61afc62dd752a4f51781a9e6485e",
    "notes/h3-active-coloop-literal-packet-termination-scope.md":
        "1201ea94d8faafefefeaff81a47987e41a817c4775fc98057294ed80fdfe51c5",
    "computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py":
        "f0905b3e33a45b51f03dd6716c3f6b29ae21c39fecf50a4ffc32960499a608c7",
    "notes/h3-coloop-alpha-localized-pointed-pf-ga-fitting-gate.md":
        "5d637d94ec2bab2f968dcb31b45b805fecd66da13fb1c927a490a6e20927fe4f",
    "computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py":
        "f35618988f591a28fd2a6574977c058aa2bec83a2cacfeb9e7567873e0b61d1c",
    "notes/h3-coloop-two-occurrence-complete-response-first-mixed-unary-gate.md":
        "94ffe3523f27aebb1064f2778b9a2a6fe99835ad98fc59b6a28dd57b6d9e9fa6",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "notes/h3-active-fan-coloop-complete-row-pivot.md":
        "2a68b7a9da9c61c67c4f63e666a6cbb1023344722943b9042f2ff15b2863e92e",
}
EXPECTED_LEDGER_SHA256 = (
    "853b7793089f4c4cfd22a234c062a8bd9594d9e38579b45b5dd809365820f535"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b
                in zip(left, right, strict=True)), Q(0))


def rank(rows) -> int:
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot = 0
    for column in range(len(work[0])):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        value = work[pivot][column]
        work[pivot] = [entry / value for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right
                         in zip(work[row], work[pivot], strict=True)]
        pivot += 1
    return pivot


def support_strata_audit() -> dict[str, object]:
    # Every nonempty support pattern occurs on alpha*(sum t_i)=1 over Q.
    witnesses = {}
    for size in (1, 2, 3):
        for support in itertools.combinations(range(3), size):
            tails = [Q(0)] * 3
            for index in support:
                tails[index] = Q(1, size)
            alpha = Q(1)
            require(alpha * sum(tails, Q(0)) == 1,
                    (support, tails))
            witnesses[repr(support)] = [str(value) for value in tails]
    require(len(witnesses) == 7, witnesses)

    symmetric = (Q(1, 3),) * 3
    alpha = Q(1)
    lambdas = tuple(alpha * value for value in symmetric)
    require(sum(lambdas, Q(0)) == 1
            and all(value and value * value != value for value in lambdas)
            and all(lambdas[left] * lambdas[right]
                    for left in range(3) for right in range(left + 1, 3)),
            lambdas)
    return {
        "normalized_support_strata": len(witnesses),
        "witnesses_t1_t2_t3": witnesses,
        "special_sparse_processor_strata": ["(t1!=0,0,0)",
                                              "(0,t2!=0,0)",
                                              "(0,0,t3!=0)"],
        "sparse_axis_equations": "t1*t2=t1*t3=t2*t3=0",
        "principal_open_cover": "D(t1) union D(t2) union D(t3)=D(C)",
        "cover_does_not_sparse": (
            "the symmetric point lies in all three D(t_i) and in none of "
            "the three sparse-axis strata"
        ),
        "partition_weights_at_symmetric_point": [str(value)
                                                   for value in lambdas],
        "weights_are_orthogonal_idempotents": False,
        "geometric_consequence": (
            "localization selects a nonzero tail but never sets the other "
            "two tails to zero; the special support theorem cannot simply "
            "be invoked on this open cover"
        ),
    }


def literal_three_tail_point(first) -> dict[str, object]:
    q_label = first.q_label
    values = {
        q_label(0, 1, 0, 0): Q(1),
        q_label(2, 3, 0, 0): Q(1, 3),
        q_label(4, 5, 0, 0): Q(1),
        q_label(2, 4, 0, 0): Q(1, 3),
        q_label(3, 5, 0, 0): Q(1),
        q_label(2, 5, 0, 0): Q(1, 3),
        q_label(3, 4, 0, 0): Q(1),
    }
    tails = tuple(
        first.product_values(values[first.q_label(left, right, 0, 0)]
                             for left, right in matching)
        for matching in first.perfect_matchings((2, 3, 4, 5))
    )
    alpha = values[q_label(0, 1, 0, 0)]
    require(tails == (Q(1, 3), Q(1, 3), Q(1, 3))
            and alpha * sum(tails, Q(0)) == 1,
            (tails, alpha))
    pure_matchings = tuple(
        matching for matching in first.MATCHINGS6
        if first.product_values(values.get(q_label(left, right, 0, 0), Q(0))
                                for left, right in matching)
    )
    require(len(pure_matchings) == 3
            and all((0, 1) in matching for matching in pure_matchings),
            pure_matchings)
    return {
        "alpha": str(alpha),
        "cofactor_tail_values": [str(value) for value in tails],
        "cofactor": str(sum(tails, Q(0))),
        "pure_target_value": str(alpha * sum(tails, Q(0))),
        "nonzero_pure_matchings": [repr(value) for value in pure_matchings],
        "literal_coloop": "01 occurs in every nonzero pure matching",
        "all_three_tail_principal_opens_active": True,
        "scope": (
            "literal normalized cofactor/support point, not a complete GHZ source"
        ),
    }


def cotangent_and_partition_audit() -> dict[str, object]:
    tails = (Q(1, 3), Q(1, 3), Q(1, 3))
    alpha = Q(1)
    aggregate = (Q(1), Q(1), Q(1))
    selected = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    )
    differences = (
        (Q(1), Q(-1), Q(0)),
        (Q(1), Q(0), Q(-1)),
    )
    require(rank((aggregate,)) == 1
            and rank((aggregate,) + selected) == 3
            and rank(differences) == 2
            and all(dot(aggregate, value) == 0 for value in differences),
            "the aggregate/tail cotangent split changed")

    # On D(t_i), normalize the ith selector by 1/t_i.  All three charts
    # contain the symmetric point.  Their pairwise differences are nonzero
    # modulo the aggregate row and span the two-dimensional quotient.
    local_selectors = tuple(tuple(entry / tails[index] for entry in vector)
                            for index, vector in enumerate(selected))
    overlap_differences = tuple(
        tuple(left - right for left, right
              in zip(local_selectors[index], local_selectors[0], strict=True))
        for index in (1, 2)
    )
    require(rank((aggregate,) + overlap_differences) == 3
            and rank(overlap_differences) == 2,
            overlap_differences)

    lambdas = tuple(alpha * value for value in tails)
    recombined = tuple(
        sum(lambdas[index] * local_selectors[index][column]
            for index in range(3))
        for column in range(3)
    )
    require(recombined == aggregate,
            ("partition recombination changed", recombined))

    # The coordinate logarithmic operator E_i=t_i*d/dt_i has a nonzero
    # scalar face on F=alpha*(sum t)-1.  Source-preserving combinations r_i
    # must satisfy sum r_i*t_i=0.  A selected coordinate vector does not.
    scalar_faces = tuple(alpha * value for value in tails)
    require(scalar_faces == lambdas and sum(scalar_faces, Q(0)) == 1,
            scalar_faces)
    require(all(dot(vector, tails) != 0 for vector in selected)
            and all(dot(vector, tails) == 0 for vector in differences),
            "the logarithmic source-validity test changed")

    # A primitive dual to the aggregate detects every attempted selected
    # row.  These two duals are also the tangent redistribution directions
    # with dC=0.
    require(dot(differences[0], selected[0]) == 1
            and dot(differences[1], selected[0]) == 1,
            "the selected-tail dual changed")
    return {
        "base_ring": (
            "B=Q[alpha,C,C^-1]/(alpha*C-1), "
            "R=B[t1,t2,t3]/(t1+t2+t3-C)"
        ),
        "relative_presentation": "R=B[t1,t2], t3=C-t1-t2",
        "relative_cotangent": (
            "Omega_(R/B)=R*dt1 plus R*dt2, with dt3=-dt1-dt2"
        ),
        "relative_cotangent_rank": rank(differences),
        "aggregate_row": [str(value) for value in aggregate],
        "aggregate_row_rank": rank((aggregate,)),
        "local_normalized_selectors": [
            [str(value) for value in vector] for vector in local_selectors
        ],
        "Cech_overlap_difference_rank_mod_aggregate": 2,
        "partition_weights": [str(value) for value in lambdas],
        "partition_recombination": [str(value) for value in recombined],
        "recombination_verdict": "returns the aggregate row, not a sparse selector",
        "log_coordinate_projector_faces": [str(value)
                                             for value in scalar_faces],
        "sum_of_projector_faces": str(sum(scalar_faces, Q(0))),
        "source_preserving_condition": "sum_i r_i*t_i=0",
        "source_preserving_tail_syzygies": [
            "(t2,-t1,0)", "(t3,0,-t1)", "(0,t3,-t2)"
        ],
        "coordinate_selector_source_valid": False,
        "first_proper_face": "lambda_i=alpha*t_i (or alpha after dividing by t_i)",
    }


def closed_shore_scope() -> dict[str, object]:
    # Closed-shore/Hall data depend on support.  On the full three-tail
    # torus, the two redistribution tangent directions retain all support.
    tails = (Q(1, 3), Q(1, 3), Q(1, 3))
    epsilon = Q(1, 12)
    deformations = (
        (tails[0] + epsilon, tails[1] - epsilon, tails[2]),
        (tails[0] + epsilon, tails[1], tails[2] - epsilon),
    )
    require(all(sum(value, Q(0)) == 1 and all(value)
                for value in deformations), deformations)
    return {
        "full_tail_torus": "D(t1*t2*t3)",
        "redistribution_directions": ["(1,-1,0)", "(1,0,-1)"],
        "cofactor_fixed": True,
        "support_fixed": True,
        "closed_shore_support_data_fixed": True,
        "consequence": (
            "a Hall/closed-shore predicate depending only on occupied tails "
            "cannot kill the rank-two redistribution module or make one "
            "tail private"
        ),
    }


def dependency_scope(literal_scope, localized_gate) -> dict[str, object]:
    literal = literal_scope.audit()
    require(literal["relabel_scaling_boundary"]
            ["arbitrary_coloop_guard_cofactor_support"] == 3,
            "the three-tail entry guard changed")
    localized = localized_gate.audit()
    require(localized["U_bright_local_chart"]["P_f_on_infinitesimal_generator"] == 1
            and localized["V_bright_local_chart"]["P_f_on_infinitesimal_generator"] == 1,
            "the localized pointed obstruction changed")
    return {
        "special_processor": (
            "proved only after the cofactor support is one and the selected "
            "mixed response rows are private"
        ),
        "arbitrary_entry_from_relabel_scaling": False,
        "alpha_localization_kills_pointed_module": False,
        "new_sharp_rank": (
            "three cofactor tails leave rank two rather than the rank-one "
            "two-occurrence redistribution in the pinned local model"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    first = load(
        "computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py",
        "coloop_three_tail_literal",
    )
    literal_scope = load(
        "computations/verify_h3_active_coloop_literal_packet_termination_scope.py",
        "coloop_three_tail_scope",
    )
    localized = load(
        "computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py",
        "coloop_three_tail_localized",
    )
    ledger = {
        "theorem": "h3 active-coloop three-tail localization/partition guard",
        "pins": PINS,
        "support_geometry": support_strata_audit(),
        "literal_symmetric_three_tail_point": literal_three_tail_point(first),
        "cotangent_and_partition": cotangent_and_partition_audit(),
        "closed_shore_scope": closed_shore_scope(),
        "pinned_processor_scope": dependency_scope(literal_scope, localized),
        "smallest_positive_extension": {
            "name": "pointed cofactor-tail comparison",
            "required_boundary": (
                "two independent tail-asymmetric rows killing "
                "Omega_(R/B), or relative graph coordinates u_i with "
                "d epsilon_i=dt_i-du_i and compatible overlap homotopies"
            ),
            "weaker_branch_sufficient": (
                "one physical tail-asymmetric row plus a source/Hall argument "
                "forcing deletion of one of the remaining two occupied tails"
            ),
            "then": (
                "a genuine support-one/private packet can enter the completed "
                "special processor of 93cf9ae"
            ),
        },
        "answer": (
            "The localization/partition route does not extend the special "
            "processor from alpha*(t1+t2+t3)=1.  D(t_i) covers the coloop "
            "chart but not by sparse strata; normalized local selectors have "
            "a rank-two overlap obstruction, and partition recombination is "
            "only the aggregate row.  The first source-validity defect is "
            "alpha*t_i.  Closed-shore support is constant along the two "
            "cofactor-redistribution directions, so privacy needs new "
            "tail-asymmetric physical rows or support deletion."
        ),
        "scope": (
            "exact cofactor-target quotient, literal normalized three-tail "
            "support point, and pinned sparse processor interface.  The "
            "counterguard is not a complete GHZ source and does not exclude "
            "asymmetric rows from the full physical source map."
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("D(t1),D(t2),D(t3): COVER, BUT NOT SPARSE")
    print("partition alpha*t_i: SUM 1, NOT ORTHOGONAL IDEMPOTENTS")
    print("relative tail cotangent / overlap obstruction: RANK 2")
    print("partitioned local selectors recombine to aggregate only")
    print("first proper face: alpha*t_i; private extraction OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
