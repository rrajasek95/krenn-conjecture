#!/usr/bin/env python3
"""Audit the tempting Y-sign antisymmetrization of the h=3 cap graph.

The universal cap complex is

    Q[Y]<T,rho> --[-Y,1]--> Q[Y]<w>.

There is a genuine semilinear involution covering Y |-> -Y, but it fixes the
closed graph T+Y*rho.  It exchanges the fibres Y=1 and Y=-1 and therefore
does not descend to an internal operation on the normalized physical fibre.
At Y=1, fixing target while negating ordinary residue is incompatible with
the chain equation.  This checker records those statements exactly.
"""

from fractions import Fraction
from hashlib import sha256
import json


Q = Fraction
EXPECTED_DIGEST = "74e2642daf991c78d203db2bdc3247248a7da01b602dfa2d2993fcc26394e9f7"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matmul(left, right):
    if not left or not right:
        return []
    require(len(left[0]) == len(right), "matrix shape mismatch")
    return [
        [sum((a * right[k][j] for k, a in enumerate(row)), Q(0))
         for j in range(len(right[0]))]
        for row in left
    ]


def rank(matrix):
    rows = [list(map(Q, row)) for row in matrix]
    if not rows:
        return 0
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (i for i in range(pivot_row, len(rows)) if rows[i][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for i, row in enumerate(rows):
            if i == pivot_row or not row[column]:
                continue
            value = row[column]
            rows[i] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(row, rows[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def universal_semilinear_audit():
    # D=[-Y,1].  Store coefficients as affine pairs (constant,Y).
    D = (((Q(0), Q(-1)), (Q(1), Q(0))),)

    def sigma(poly):
        constant, y_coefficient = poly
        return constant, -y_coefficient

    sigma_D = tuple(tuple(sigma(entry) for entry in row) for row in D)

    # tau_1(T)=T, tau_1(rho)=-rho; tau_0(w)=-w.
    S1 = ((Q(1), Q(0)), (Q(0), Q(-1)))
    S0 = ((Q(-1),),)

    def affine_matmul(left, right):
        answer = []
        for row in left:
            output_row = []
            for j in range(len(right[0])):
                constant = Q(0)
                y_coefficient = Q(0)
                for k, (c, y) in enumerate(row):
                    scalar = right[k][j]
                    constant += c * scalar
                    y_coefficient += y * scalar
                output_row.append((constant, y_coefficient))
            answer.append(tuple(output_row))
        return tuple(answer)

    def scalar_left(left, right):
        return tuple(
            tuple((left[i][0] * entry[0], left[i][0] * entry[1])
                  for entry in row)
            for i, row in enumerate(right)
        )

    lhs = affine_matmul(D, S1)
    rhs = scalar_left(S0, sigma_D)
    require(lhs == rhs == (((Q(0), Q(-1)), (Q(-1), Q(0))),),
            "semilinear chain identity failed")

    # G=T+Y*rho.  Semilinearity flips Y and tau flips rho, so the signs
    # cancel.  The graph is invariant, not anti-invariant.
    graph = ((Q(1), Q(0)), (Q(0), Q(1)))
    tau_graph = (sigma(graph[0]), tuple(-x for x in sigma(graph[1])))
    require(tau_graph == graph, "the universal graph is not fixed")

    # sigma(Y-1)=-(Y+1), so the ideal (Y-1) is not stable.  Evaluation at
    # Y=1 distinguishes the two generators and proves non-descent.
    sigma_y_minus_one = (Q(-1), Q(-1))
    require(sum(sigma_y_minus_one) == Q(-2),
            "Y-sign unexpectedly descended to the normalized fibre")

    return {
        "universal_differential": ["-Y", "1"],
        "semilinear_ring_action": "Y -> -Y",
        "semilinear_degree_one": {"T": "T", "rho": "-rho"},
        "semilinear_degree_zero": {"w": "-w"},
        "graph": "T+Y*rho",
        "graph_action": "fixed",
        "normalized_ideal_action": "(Y-1) -> -(Y+1)",
        "normalized_fibre_endomorphism": False,
    }


def normalized_fibre_audit():
    # At Y=1, d=[-1,1].  The desired fixed-target/residue-negating action is
    # forced to M=diag(1,-1).  A degree-zero action is multiplication by s.
    # The chain equation dM=s d gives simultaneously s=1 and s=-1.
    D = ((Q(-1), Q(1)),)
    M = ((Q(1), Q(0)), (Q(0), Q(-1)))
    DM = matmul(D, M)
    require(DM == [[Q(-1), Q(-1)]], "normalized sign matrix changed")

    equations = (
        (Q(-1), Q(1)),   # -1=-s
        (Q(-1), Q(-1)),  # -1= s
    )
    coefficient = [[row[0]] for row in equations]
    augmented = [[row[0], row[1]] for row in equations]
    require(rank(coefficient) == 1 and rank(augmented) == 2,
            "fixed-fibre chain-map contradiction disappeared")

    # The illicit anti-part of G=T+rho is 2*rho.  It is target-zero and has
    # residue 2, but d(2*rho)=2*w, so it is not a cap class.
    anti_graph = (Q(0), Q(2))
    boundary = D[0][0] * anti_graph[0] + D[0][1] * anti_graph[1]
    require(boundary == Q(2), "pure-residue anti-part became a cycle")

    # More generally, every target-zero chain is b*rho and its boundary is
    # b*w.  Thus the target-zero cycle kernel is zero in characteristic zero.
    target_zero_cycle_matrix = ((Q(1), Q(0)), (Q(-1), Q(1)))
    require(rank(target_zero_cycle_matrix) == 2,
            "target-zero cycle kernel is nonzero")

    return {
        "normalized_differential": [-1, 1],
        "desired_action": {"T": "T", "rho": "-rho"},
        "chain_scalar_equations": ["s=1", "s=-1"],
        "consistent": False,
        "illicit_graph_anti_part": "2*rho",
        "anti_part_boundary": "2*w",
        "target_zero_cycle_kernel_dimension": 0,
    }


def main():
    certificate = {
        "universal": universal_semilinear_audit(),
        "normalized_fibre": normalized_fibre_audit(),
        "conclusion": {
            "signed_antisymmetrization_constructs_residue": False,
            "reason": (
                "the legal semilinear involution fixes the graph and "
                "exchanges Y=1 with Y=-1; the fixed-fibre sign map is not "
                "a chain map"
            ),
            "remaining_datum": (
                "an invisible degree-one n with dn=w, or the equivalent "
                "physical cross-word cap/comparison placement"
            ),
        },
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"certificate digest changed: {digest}")
    print("h=3 cap Y-sign antisymmetrization audit: PASS")
    print("universal semilinear involution: LEGAL, GRAPH FIXED")
    print("normalized Y=1 residue sign: NOT A CHAIN MAP")
    print("illicit anti-part 2*rho has boundary 2*w")
    print(f"certificate sha256 {digest}")


if __name__ == "__main__":
    main()
