#!/usr/bin/env python3
"""Exact counterguard for the current source-constrained HPL packet.

This checker combines two *necessary* blocks of the proposed anchored
two-chart contraction, without identifying their generators:

1. the literal chart-25 five-row fibre and all physical mixed-source
   columns incident to its frozen source-annihilating functional; and
2. the target/ordinary-residue augmented cap block used by the h=3
   Reynolds attaching comparison.

The first block has the integral separator ``D-sum(A_i)``.  Hence the
missing HPL correction ``4D`` is not a boundary of the existing labelled
mixed-source family.  The second block has zero common augmentation kernel,
so it contains no invisible chain with nonzero cap-row boundary.  These are
pre-d2 obstructions.  A larger relative source complex may add either
missing type; this checker is not a no-go for such an extension.
"""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_DIGEST = "909cd81e09160255b99807063b392dda85189226eead2cc0ba56da4a5f4c9d96"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LITERAL = load(
    "source_constrained_literal_hpl",
    "verify_n8_literal_hafnian_hpl_no_go.py",
)
CAP = load(
    "source_constrained_reynolds_cap",
    "verify_h3_reynolds_attach_coupled_obstruction.py",
)


def rank(matrix):
    work = [list(map(F, row)) for row in matrix]
    if not work:
        return 0
    answer = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(answer, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [
                left - value * right
                for left, right in zip(work[row], work[answer], strict=True)
            ]
        answer += 1
    return answer


def dot(left, right):
    require(len(left) == len(right), "dot-product dimensions disagree")
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def source_fibre_audit(literal_ledger):
    """Audit the universal five-row incidence forced by the literal fibre."""
    fibre = literal_ledger["canonical_five_row_fibre"]
    require(fibre["source_column_multiplicities"] == [3, 4, 4, 3],
            "literal source multiplicities moved")
    require(fibre["weights"] == [[-1, 4]] * 4 + [[1, 4]],
            "literal partial character moved")

    # Rows are A1,A2,A3,A4,D.  One representative of every physical
    # leaf-centre incidence type has boundary A_i+D.  Multiplicities do not
    # change the image.  The vector ell is four times the actual frozen
    # partial character and annihilates every such labelled column.
    boundary = [
        [F(1) if row == column or row == 4 else F(0)
         for column in range(4)]
        for row in range(5)
    ]
    ell = [F(-1), F(-1), F(-1), F(-1), F(1)]
    require(rank(boundary) == 4, "five-row source rank moved")
    require(all(dot(ell, [boundary[row][column] for row in range(5)]) == 0
                for column in range(4)),
            "source separator stopped annihilating a physical incidence")

    naive = [F(-1), F(-1), F(-1), F(0), F(1)]
    missing = [F(0), F(0), F(0), F(0), F(4)]
    forced = [left + right for left, right in zip(naive, [0, 0, 0, 4, 0])]
    require(dot(ell, naive) == 4, "naive HPL packet defect moved")
    require(dot(ell, missing) == 4, "missing 4D defect moved")
    require(dot(ell, forced) == 0, "forced hidden A4 row left source image")
    require(literal_ledger["literal_one_pair_HPL"]["forced_second_transfer"]
            == "-3D", "literal second transfer moved")
    require(literal_ledger["literal_one_pair_HPL"]["desired_second_transfer"]
            == "+D", "desired second transfer moved")

    # Any algebraic-Morse cancellation is a change of bases followed by a
    # Schur complement, so it cannot remove a nonzero cokernel functional.
    # The rank computation makes that invariant explicit for this minimal
    # physical fibre: four unit pivots leave exactly one critical row.
    coker_dimension = 5 - rank(boundary)
    require(coker_dimension == 1, "five-row critical dimension moved")

    return {
        "physical_row_labels": ["A1", "A2", "A3", "A4", "D"],
        "physical_incidence_multiplicities": [3, 4, 4, 3],
        "boundary_rank": rank(boundary),
        "critical_row_dimension": coker_dimension,
        "integral_separator": [int(value) for value in ell],
        "naive_packet_separator": int(dot(ell, naive)),
        "missing_4D_separator": int(dot(ell, missing)),
        "forced_hidden_A4_coefficient": 4,
        "literal_second_transfer": "-3D",
        "desired_second_transfer": "+D",
    }


def cap_relative_audit(cap_ledger):
    """Audit the relative kernel before any curvature d2 is formed."""
    require(cap_ledger["common_augmentation_kernel"] == 0,
            "old cap common augmentation kernel moved")
    require(cap_ledger["five_block_obstruction_rank"] == 5,
            "five-face attaching obstruction rank moved")

    # Basis T,rho.  The two augmentations are the identity.  Therefore the
    # invisible submodule is zero over every coefficient ring.  We also use
    # rational Y samples to replay the boundary equation d(T,rho)=-YT+rho.
    augmentation = [[F(1), F(0)], [F(0), F(1)]]
    require(rank(augmentation) == 2, "target/ores map lost rank")
    records = []
    for y, gamma in ((F(1), F(1)), (F(2), F(-3)), (F(-5, 2), F(7, 3))):
        equations = [
            [F(-1) * y, F(1)],  # selected cap-row boundary
            augmentation[0],     # physical target
            augmentation[1],     # ordinary residue
        ]
        augmented = [
            equations[0] + [gamma],
            equations[1] + [F(0)],
            equations[2] + [F(0)],
        ]
        require(rank(equations) == 2 and rank(augmented) == 3,
                "an invisible cap-row lift appeared")
        records.append({
            "Y": str(y),
            "gamma": str(gamma),
            "coefficient_rank": 2,
            "augmented_rank": 3,
        })

    return {
        "cap_degree_one_labels": ["T", "rho"],
        "boundary": {"T": "-Y*w", "rho": "w"},
        "physical_target": {"T": 1, "rho": 0},
        "ordinary_residue": {"T": 0, "rho": 1},
        "relative_invisible_kernel_dimension": 0,
        "five_face_obstruction_rank": 5,
        "rational_rank_replays": records,
    }


def main():
    literal_ledger, literal_digest = LITERAL.audit()
    require(
        literal_digest
        == "501f74cb2441c4ce451fc4db2cc8a1d6c13f7a8bc9eec98a14d115d4a406034e",
        "literal source-labelled HPL dependency moved",
    )
    denominator_records, formal_source = CAP.denominator_reynolds_differential()
    cap_ledger = CAP.derived_cap_and_attach_audit()
    missing = CAP.diagnostic_minimal_extension()
    cap_certificate = {
        "denominator_reynolds": denominator_records,
        "formal_source_symbol_complex": formal_source,
        "smallest_derived_cap_complex": cap_ledger,
        "missing_generator": missing,
        "conclusion": {
            "A_attach_in_smallest_complex": "obstructed",
            "obstruction_class": "[gamma*w] in G0/d(ker(tgt,ores))",
            "obstruction_rank_five_blocks": 5,
            "sequential_construction": "impossible without a new cap-degree-one chain",
            "bare_cap_if_and_only_if": "invisible attach exists iff gamma=0",
            "first_candidate_total_PP_order": 4,
            "higher_physical_sector": "not tested",
        },
    }
    cap_digest = sha256(json.dumps(
        cap_certificate, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    require(cap_digest == CAP.EXPECTED_DIGEST,
            "Reynolds/cap dependency moved")

    source = source_fibre_audit(literal_ledger)
    cap = cap_relative_audit(cap_ledger)
    ledger = {
        "dependencies": {
            "literal_hpl_digest": literal_digest,
            "reynolds_cap_digest": cap_digest,
            "single_edge_terminal_commit": "a67ec1d",
        },
        "source_provenance_counterguard": source,
        "zero_indeterminacy_counterguard": cap,
        "conclusion": {
            "old_source_ADMT_HPL_contraction": "obstructed before curvature d2",
            "source_failure": "required 4D lower face has nonzero partial character",
            "relative_failure": "ker(target,ordinary_residue)=0, so w survives",
            "single_edge_terminal_test": (
                "not reached: there is no invisible cap chain whose physical-edge "
                "support could be tested"
            ),
            "minimal_extensions": [
                "a source-labelled relative cell with projected boundary 4D",
                "an invisible cap chain n with d(n)=gamma*w",
            ],
            "scope": (
                "necessary blocks of the current labelled source/cap inventory; "
                "a larger relative complex may add the two missing cell types"
            ),
        },
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FROZEN":
        require(digest == EXPECTED_DIGEST, ("ledger changed", digest, ledger))
    print("source-constrained anchored HPL counterguard: PASS")
    print("literal source obstruction: critical character detects 4D")
    print("relative augmentation obstruction: invisible cap kernel is zero")
    print("single-edge terminal criterion: unreachable in the current complex")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
