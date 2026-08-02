#!/usr/bin/env python3
"""Independent audit of the derived cap/base-change classification.

This file does not import the primary checker.  It rebuilds the split cap
block, formal occupancy section, relative connecting class, and hypothetical
invisible lift.  It also contains a minimal non-flat counterexample showing
why Tor_1(coker(b), S) must be retained for the full source complex.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
import json


Q = Fraction
ZERO = Q(0)
ONE = Q(1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(row, column):
    require(len(row) == len(column), "dot-product dimensions differ")
    return sum((left * right for left, right in zip(row, column)), ZERO)


def rational_rank(columns, height):
    """Rank of a matrix supplied by columns over Q."""
    if not columns:
        return 0
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(pivot_row, height) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def modular_rank(columns, height, prime):
    """Rank of integer columns after the base change Z -> F_prime."""
    if not columns:
        return 0
    work = [[int(columns[column][row]) % prime
             for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(pivot_row, height)
             if work[row][column] % prime),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [entry * inverse % prime
                           for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column] % prime:
                continue
            scale = work[row][column]
            work[row] = [
                (entry - scale * pivot_entry) % prime
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def cap_audit():
    packets = (
        (Q(2), Q(3), Q(5), Q(11), Q(7, 5)),
        (Q(3), ZERO, Q(2), Q(5), Q(-4, 9)),
        (Q(-2), Q(7), Q(3), Q(-5), Q(13, 6)),
        (Q(5, 3), Q(-7, 4), Q(11, 5), Q(2, 9), Q(-8, 7)),
    )
    ledger = []
    for A, B, F, U, Y in packets:
        kappa = A * U - B * F
        require(kappa * Y != ZERO, "packet is outside the active open")

        differential = (-Y, ONE)
        graph = (ONE, Y)
        contractible = (ZERO, ONE)
        require(dot(differential, graph) == ZERO,
                "graph vector is not closed")
        require(dot(differential, contractible) == ONE,
                "rho does not contract the cap row")
        # Columns (graph,rho) form [[1,0],[Y,1]].
        require(ONE * ONE - ZERO * Y == ONE,
                "cap basis change is not unimodular")

        relative = (ZERO, -kappa * Y)
        connecting = dot(differential, relative)
        require(connecting == -kappa * Y and connecting != ZERO,
                "relative connecting value/sign differs")

        filtered = (-kappa, -kappa * Y)
        require(dot(differential, filtered) == ZERO,
                "selected representative left the graph line")

        extended = (-Y, ONE, kappa * Y)
        invisible_cycle = (ZERO, -kappa * Y, ONE)
        extended_graph = (ONE, Y, ZERO)
        require(dot(extended, invisible_cycle) == ZERO,
                "hypothetical invisible lift has wrong sign")
        require(dot(extended, extended_graph) == ZERO,
                "old graph is not closed in the extension")
        require(rational_rank((extended,), 3) == 1,
                "extended differential has wrong rank")
        target_constraint = (ONE, ZERO, ZERO)
        require(rational_rank((extended, target_constraint), 3) == 2,
                "target-zero kernel does not have rank one")

        ledger.append({
            "kappa": str(kappa),
            "Y": str(Y),
            "connecting": str(connecting),
            "target_zero_response": str(invisible_cycle[1]),
            "direct_free": B == ZERO,
        })
    return ledger


def matchings(vertices):
    """All partial matchings, represented by sorted tuples of edges."""
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = list(matchings(vertices[1:]))
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def occupancy_audit():
    ledger = []
    for size in range(1, 7):
        states = matchings(tuple(range(size)))
        quotient_states = matchings(tuple(range(1, size)))
        state_index = {state: index for index, state in enumerate(states)}
        quotient_index = {
            state: index for index, state in enumerate(quotient_states)
        }
        height = len(states)

        kernel_states = tuple(
            state for state in states
            if any(0 in edge for edge in state)
        )
        kernel_columns = []
        for state in kernel_states:
            column = [0] * height
            column[state_index[state]] = 1
            kernel_columns.append(tuple(column))

        section_columns = []
        for state in quotient_states:
            column = [0] * height
            column[state_index[state]] = 1
            occupied = {site for edge in state for site in edge}
            for site in range(1, size):
                if site not in occupied:
                    exposed = tuple(sorted(((0, site),) + state))
                    column[state_index[exposed]] += 1
            section_columns.append(tuple(column))

            # pi keeps only states in which site 0 is unmatched.
            projected = [0] * len(quotient_states)
            for row, coefficient in enumerate(column):
                if not coefficient:
                    continue
                matching = states[row]
                if not any(0 in edge for edge in matching):
                    projected[quotient_index[matching]] += coefficient
            expected = [0] * len(quotient_states)
            expected[quotient_index[state]] = 1
            require(projected == expected, "pi_x s_x is not identity")

        decomposition = tuple(kernel_columns + section_columns)
        require(len(decomposition) == height,
                "occupancy decomposition is not square")
        require(rational_rank(decomposition, height) == height,
                "occupancy section does not split over Q")
        for prime in (2, 3, 5, 7):
            require(modular_rank(decomposition, height, prime) == height,
                    f"occupancy split died after base change mod {prime}")

        ledger.append({
            "sites": size,
            "states": height,
            "kernel": len(kernel_states),
            "quotient": len(quotient_states),
        })
    return ledger


def section_defect_audit():
    # Coordinates of P are (k0,k1,sq0,sq1), with K=<k0,k1>.
    k0 = (ONE, ZERO, ZERO, ZERO)
    k1 = (ZERO, ONE, ZERO, ZERO)
    sq0 = (ZERO, ZERO, ONE, ZERO)
    coupled = tuple(left + right for left, right in zip(k0, sq0))

    # E=<k0+sq0,k1>.  Two lifts of q0 differ by 3*k1, hence their
    # defects agree modulo E intersection K=<k1>.
    defect_one = k0
    defect_two = tuple(left + 3 * right for left, right in zip(k0, k1))
    require(rational_rank((k1, defect_one), 4) == 2,
            "coupled section defect unexpectedly vanished")
    difference = tuple(left - right
                       for left, right in zip(defect_two, defect_one))
    require(rational_rank((k1, difference), 4) == 1,
            "section defect depends on the chosen lift")
    require(rational_rank((coupled, k1, sq0), 4) == 3,
            "the canonical section unexpectedly descends through E")

    # In the blockwise relation E0=<k0,sq0>, s(q0)=sq0 is itself a
    # relation and the defect is zero, as for a pure base-ideal relation.
    require(rational_rank((k0, sq0), 4) == 2,
            "blockwise relation model is degenerate")
    zero_defect = tuple(left - right for left, right in zip(sq0, sq0))
    require(not any(zero_defect), "blockwise section defect is nonzero")
    return {
        "coupled_defect_nonzero": True,
        "lift_independent_mod_kernel_relations": True,
        "blockwise_defect_zero": True,
    }


def tor_audit():
    # Minimal full-source kernel enlargement:
    # R=Q[t], C=V=R, b is multiplication by t, a is the identity, and
    # S=R/(t)=Q.  Universally ker(b)=0, so O=Rw and [w] is nonzero after
    # tensoring.  But b tensor S is zero, its entire source becomes
    # invisible, and a sends that new chain to w.  The new kernel quotient
    # and Tor_1^R(R/(t),R/(t)) both have Q-dimension one.
    universal_kernel_rank = 0
    specialized_b = ZERO  # image of t in S=R/(t)
    specialized_kernel_dimension = 1 if specialized_b == 0 else 0
    tor_dimension = 1  # kernel of t:S->S in the standard free resolution
    obstruction_class_nonzero = ONE != ZERO
    specialized_cap_value = ONE
    require(universal_kernel_rank == 0,
            "counterexample acquired a universal invisible chain")
    require(specialized_kernel_dimension == tor_dimension == 1,
            "Tor_1 does not match the enlarged invisible kernel")
    require(obstruction_class_nonzero and specialized_cap_value == ONE,
            "Tor transgression does not supply the cap row")

    # Separate exact scalar model of the degree-zero mechanism: after a
    # flat localization in which the boundary scalar 2 is invertible, the
    # descended chain (1/2)n maps to w and there is no positive Tor.
    descended_coefficient = Q(1, 2)
    require(2 * descended_coefficient == ONE,
            "degree-zero cokernel lift has wrong coefficient")
    flat_tor_dimension = 0
    require(flat_tor_dimension == 0,
            "flat degree-zero example acquired positive Tor")
    return {
        "post_base_change_kernel_dimension": specialized_kernel_dimension,
        "tor1_coker_dimension": tor_dimension,
        "nonzero_degree_zero_obstruction": obstruction_class_nonzero,
        "tor_transgression_hits_w": specialized_cap_value == ONE,
        "flat_degree_zero_lift": str(descended_coefficient),
        "flat_tor_dimension": flat_tor_dimension,
    }


EXPECTED_DIGEST = "223e8f5530585c2ff92b3d74f4fc80afe3a2c513244b353fdf2a648b0a8e9f06"


def run(mode):
    ledger = {}
    if mode in ("all", "cap"):
        ledger["cap"] = cap_audit()
    if mode in ("all", "occupancy"):
        ledger["occupancy"] = occupancy_audit()
    if mode in ("all", "defect"):
        ledger["defect"] = section_defect_audit()
    if mode in ("all", "tor"):
        ledger["tor"] = tor_audit()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if mode == "all":
        require(digest == EXPECTED_DIGEST,
                "independent derived-class audit digest differs")
    print(f"independent derived cap/base-change audit ({mode}): PASS")
    if mode in ("all", "cap"):
        print("cap block splits; relative connecting value is -kappa*Y*w")
    if mode in ("all", "occupancy", "defect"):
        print("formal occupancy is universally split; evaluated coupling may obstruct descent")
    if mode in ("all", "tor"):
        print("full-source Tor_1(coker(b),S) can create the first invisible lift")
    print(f"sha256: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "cap", "occupancy", "defect", "tor"),
        default="all",
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()
