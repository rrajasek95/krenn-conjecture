#!/usr/bin/env python3
"""Exact obstruction to contracting a minimum k>=3 axis circuit to k=2.

At a minimum-support representative the occupied complete response columns
C_i are independent and T=sum lambda_i C_i with every lambda_i nonzero.
Therefore the coefficient vector lambda is unique.  For every pair u,v and
every omitted w, the dual coordinate ell_w annihilates C_u,C_v but evaluates
T to lambda_w.  No coefficient-only deletion/source specialization with the
cofactor columns fixed can retain T on two columns.

The checker audits the quotient circuit, every pair separator, and the exact
rank/cokernel dimensions through k=10.  The proof is the displayed basis
argument for arbitrary k, not a finite-support inference.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py":
        "1594dcac16bb77bb929c18edda224e215ea99697bfd36edabc4230a0d341b5c8",
    "notes/uniform-one-bad-axis-hessian-carrier-circuit-boundary.md":
        "d784f8d25461ffcdafcc3fb9a39ccc776f770fb63359f722bead4fe7c965e73e",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_uniform_one_bad_five_axis_mate_clean_closure.py":
        "bc78078b3b8b16545cdab9fe083e6071d596d7c5338a119a4d7805a168971142",
    "notes/uniform-one-bad-five-axis-mate-clean-closure.md":
        "3f62426bca8f8a27e7a46013af743bb859231451fc17e118e60673a07c409df0",
}
EXPECTED_LEDGER_SHA256 = (
    "a3ad54e1ddc2a88c092e73757816942b5bf28de524f3d516f0d25cda2839cb06"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def rank(columns):
    if not columns:
        return 0
    rows = len(columns[0])
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(rows)]
    output = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(output, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[output], matrix[pivot] = matrix[pivot], matrix[output]
        value = matrix[output][column]
        matrix[output] = [entry / value for entry in matrix[output]]
        for row in range(rows):
            if row == output or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right
                           in zip(matrix[row], matrix[output], strict=True)]
        output += 1
    return output


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def audit_order(k):
    columns = tuple(
        tuple(Q(int(row == column)) for row in range(k))
        for column in range(k)
    )
    coefficients = tuple(Q(1) for _ in range(k))
    target = tuple(sum(coefficients[column] * columns[column][row]
                       for column in range(k)) for row in range(k))
    require(target == coefficients and rank(columns) == k,
            f"the minimum column presentation changed at k={k}")

    # Quotient V/<T>: subtract the last coordinate times T, then retain the
    # first k-1 coordinates.  Its kernel on the k columns is exactly <(1,...,1)>.
    quotient_columns = tuple(
        tuple(columns[column][row] - columns[column][-1] * target[row]
              for row in range(k - 1))
        for column in range(k)
    )
    require(rank(quotient_columns) == k - 1,
            f"the target quotient rank changed at k={k}")
    quotient_sum = tuple(sum(column[row] for column in quotient_columns)
                         for row in range(k - 1))
    require(quotient_sum == (Q(0),) * (k - 1),
            f"the full-support quotient circuit changed at k={k}")
    for omitted in range(k):
        require(rank(tuple(column for index, column
                           in enumerate(quotient_columns)
                           if index != omitted)) == k - 1,
                f"the quotient circuit stopped being unique at k={k}")

    pair_records = []
    for u, v in combinations(range(k), 2):
        # A nonzero self-square pair means lambda_u*lambda_v != 0.  It does
        # not put T in span(C_u,C_v): the augmented rank is exactly three.
        require(coefficients[u] * coefficients[v] == 1,
                "the representative self-square pair vanished")
        augmented_rank = rank((columns[u], columns[v], target))
        require(augmented_rank == 3,
                f"a k>=3 pair unexpectedly spans T: {(k, u, v)}")

        omitted = next(index for index in range(k) if index not in (u, v))
        separator = columns[omitted]
        require(dot(separator, columns[u]) == 0
                and dot(separator, columns[v]) == 0
                and dot(separator, target) == 1,
                f"the primitive pair separator changed: {(k, u, v)}")

        quotient_target = tuple(target[index] for index in range(k)
                                if index not in (u, v))
        require(quotient_target == (Q(1),) * (k - 2),
                f"the pair-contraction target residue changed: {(k, u, v)}")
        pair_records.append({
            "pair": [u, v],
            "self_square_coefficient": "1",
            "rank_Cu_Cv_T": augmented_rank,
            "primitive_separator": omitted,
            "separator_on_target": "1",
            "pair_quotient_target": ["1"] * (k - 2),
        })

    return {
        "k": k,
        "column_rank": rank(columns),
        "target_quotient_rank": rank(quotient_columns),
        "unique_full_support_circuit": [1] * k,
        "pairs_checked": len(pair_records),
        "pair_contraction_cokernel_dimension": k - 2,
        "pair_records": pair_records,
    }


def main():
    pin_dependencies()
    audits = tuple(audit_order(k) for k in range(3, 11))
    require(sum(record["pairs_checked"] for record in audits) == 164,
            "the representative pair audit count changed")

    ledger = {
        "dependencies": PINS,
        "representative_exact_audits": audits,
        "linear_theorem": (
            "if independent occupied columns C_i satisfy "
            "T=sum_i lambda_i C_i with every lambda_i nonzero, then lambda "
            "is the unique coefficient vector; for every proper subset S, "
            "T is not in span{C_i:i in S}.  In particular every two-column "
            "contraction at k>=3 has a primitive dual separator"
        ),
        "self_square_scope": (
            "choosing a nonzero self-square pair only selects u,v with "
            "lambda_u lambda_v nonzero; it does not change the pair-span "
            "obstruction or the k-2 dimensional target residue"
        ),
        "source_row_boundary": {
            "hessian_role": (
                "the genuine cofactor recurrence constructs each fixed "
                "column C_i but, at the same source point, supplies no "
                "deformation delta C_i"
            ),
            "unary_private_site_role": (
                "the target-augmented identity forces a nonzero literal "
                "Delta*K product from an off-diagonal cell; it does not "
                "alter the unique response coefficients lambda_i"
            ),
            "first_required_operation": (
                "a simultaneous source-valid deformation of the common q "
                "or opposite stars whose column corrections transfer the "
                "k-2 omitted target residues into the retained pair while "
                "preserving all response rows and localized units"
            ),
        },
        "verdict": (
            "there is no induction from a minimum k>=3 axis circuit to the "
            "proved k=2 module by deleting/scaling star components with the "
            "complete response columns fixed; the first possible escape "
            "must change those columns through a new source-labelled row"
        ),
        "scope": (
            "coordinate-free linear/source-typing obstruction, not a "
            "physical counterexample and not a k=3 support census"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"axis-circuit contraction ledger changed: {digest}")

    print("uniform axis-circuit k-to-2 contraction obstruction: PASS")
    print("orders k=3..10; pair separators checked: 164")
    print("minimum response coefficients are unique and full-support")
    print("every two-column contraction retains k-2 nonzero target residues")
    print("missing operation: source-valid deformation of the columns C_i")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
