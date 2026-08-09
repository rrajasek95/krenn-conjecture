#!/usr/bin/env python3
"""Inventory the first source-typed candidate for the OO cap defect.

The curved OO overlap leaves the target-free cap defect ``-kappa*Y*w``.
This checker compares that defect with the already committed adjacent-power,
mixed-word-reset, and fourth-Hasse constructions.  It verifies that the
fourth Hasse/Spencer cone has exactly the required opposite boundary and the
strict pq-direct/pr-two-star provenance, but only in the prolonged complex.
Its diagonal image in the old physical two-row complex retains the independent
``(H0-u)*eq`` boundary, and the fourth selector sends the source equation
``Hm`` to one.  Thus no already constructed *physical* source syzygy is the
missing relative generator.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_h3_full_hasse_cone_d4_descent_obstruction as hasse  # noqa: E402
import verify_h3_mixed_word_reset_cross_quotient_chain_lift_no_go as reset  # noqa: E402
import verify_offdiagonal_same_power_target_residue_lock as adjacent  # noqa: E402


Q = Fraction
EXPECTED_DIGEST = "1ea40b149d701b272cea40f57e6271e6d92767d737f7cf39847b4f4d4b0a3534"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# Sparse polynomials in (kappa, B=H0-u, Y, Hm).  This tiny independent ring
# keeps the cokernel/separator check exact without a computer-algebra package.
N_VARIABLES = 4
KAPPA, B_PURE, CAP_Y, H_MIXED = range(N_VARIABLES)


def constant(value=1):
    value = Q(value)
    return {(0,) * N_VARIABLES: value} if value else {}


def variable(index):
    exponent = [0] * N_VARIABLES
    exponent[index] = 1
    return {tuple(exponent): Q(1)}


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(scalar, polynomial):
    scalar = Q(scalar)
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_monomial[index] + right_monomial[index]
                for index in range(N_VARIABLES)
            )
            answer[monomial] = answer.get(monomial, Q(0)) + (
                left_coefficient * right_coefficient
            )
            if not answer[monomial]:
                del answer[monomial]
    return answer


def dot(left, right):
    return add(*(multiply(a, b) for a, b in zip(left, right, strict=True)))


def in_principal_variable_ideal(polynomial, index):
    return all(monomial[index] for monomial in polynomial)


def matrix_rank(rows):
    matrix = [[Q(value) for value in row] for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(
                    matrix[row], matrix[rank], strict=True
                )
            ]
        rank += 1
    return rank


def audit_old_physical_inventory():
    # This is the exact physical adjacent-power Euler/Bianchi ledger.  Both
    # displayed brackets vanish separately; it constructs no Bockstein.
    adjacent.check_adjacent_power_overlap_ledger()

    reset_records = {
        name: reset.audit_packet(name, packet)
        for name, packet in reset.PACKETS.items()
    }
    require(reset_records["direct_free"]["descent"]["12112"],
            "the direct-free reset quotient descent changed")
    require(reset_records["direct_free"]["descent"]["12212"],
            "the second direct-free reset quotient descent changed")
    require(reset_records["tilted"]["descent"]["02012"],
            "the tilted reset quotient descent changed")
    require(not reset_records["tilted"]["descent"]["22012"],
            "the tilted reset counterguard disappeared")

    return {
        "adjacent_power_euler_bianchi": {
            "physical_source_identity": True,
            "ordinary_boundary": 0,
            "constructs_relative_generator": False,
        },
        "mixed_word_resets": {
            "descended_quotient_tags": ["12112", "12212", "02012"],
            "failed_tag": "22012",
            "physical_source_secondary_cell": False,
            "reason": "reset transports an EqSystem failure; it is zero on a true source",
        },
    }


def audit_formal_positive_candidate():
    records = hasse.formal_hasse_cone_audit()
    charts = hasse.chart_and_endpoint_audit()
    denominator = hasse.denominator_face_audit()
    require(len(records) == 15 and len(charts) == 5 and len(denominator) == 15,
            "the fourth-Hasse face census changed")
    require(all(record["formal_cap_boundary"] == "Y*w"
                and record["curvature_boundary"] == "kappa*Y*w"
                and record["formal_target_after_minus_T"] == 0
                and record["formal_cap_ordinary_residue"] == 0
                and record["diagonal_chain_defect"] == "(H0-u)*e"
                and record["selector_Hm"] == 1
                and not record["selector_descends_to_source_quotient"]
                for record in records),
            "the formal positive chain or its physical obstruction changed")
    require(all(record["top_sector_transfer"]
                == ["pq_direct", "pr_two_star"] for record in charts),
            "the strict pq/pr provenance changed")
    require(all(record["top_support"]
                == [record["deleted"], hasse.MIXED5[record["deleted"]]]
                for record in denominator),
            "the denominator top support stopped being Kronecker")

    return {
        "candidate": "kappa*n_I=kappa*(s_I-T)",
        "complex": "fourth Hasse/Spencer prolonged target cone",
        "boundary": "+kappa*Y*w",
        "target": 0,
        "ordinary_residue": 0,
        "strict_chart_sectors": ["pq_direct", "pr_two_star"],
        "face_records": len(records),
        "denominator_records": len(denominator),
        "physical_source_syzygy": False,
        "diagonal_projection_defect": "kappa*(H0-u)*eq",
        "source_ideal_defect": "fourth selector sends Hm to 1",
        "missing_physical_type": "source-valid fourth Spencer generator with all proper faces",
    }


def audit_smallest_physical_cokernel():
    kappa = variable(KAPPA)
    pure = variable(B_PURE)
    cap_y = variable(CAP_Y)
    mixed = variable(H_MIXED)

    # Boundary coordinates are (Eq,w).  The diagonal projection of the
    # formal candidate is kappa*(r0-T), whereas the required new physical
    # generator has no Eq boundary.
    projected = (multiply(kappa, pure), multiply(kappa, cap_y))
    desired = ({}, multiply(kappa, cap_y))
    separator = (cap_y, scale(-1, pure))
    require(not dot(separator, projected),
            "the cokernel covector stopped killing the physical projection")
    obstruction = dot(separator, desired)
    expected = scale(-1, multiply(multiply(kappa, pure), cap_y))
    require(obstruction == expected and obstruction,
            "the desired cap boundary lost its exact cokernel class")

    # An old-row repair would need b*Hm=-kappa*(H0-u).  The right side is
    # not in (Hm): setting every mixed source cell to zero kills Hm but not
    # H0-u.  This monomial-ideal test is the algebraic version of that guard.
    rhs = scale(-1, multiply(kappa, pure))
    require(not in_principal_variable_ideal(rhs, H_MIXED)
            and in_principal_variable_ideal(multiply(mixed, rhs), H_MIXED),
            "the Hm-principal-ideal separation guard changed")

    # At the exact unit specialization kappa=B=Y=1 the physical boundary
    # line and the desired boundary have ranks one and two respectively.
    projected_unit = [Q(1), Q(1)]
    desired_unit = [Q(0), Q(1)]
    require(matrix_rank([projected_unit]) == 1
            and matrix_rank([projected_unit, desired_unit]) == 2,
            "the smallest generic cokernel rank changed")

    return {
        "boundary_coordinates": ["Eq", "w"],
        "old_physical_projection": ["kappa*(H0-u)", "kappa*Y"],
        "required_boundary": ["0", "kappa*Y"],
        "integral_cokernel_covector": ["Y", "-(H0-u)"],
        "required_pairing": "-kappa*(H0-u)*Y",
        "generic_old_rank": 1,
        "generic_augmented_rank": 2,
        "old_two_row_repair": "impossible because H0-u is not in (Hm)",
    }


def word_partition(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def audit_word_orbit_scope():
    formal_word = tuple(hasse.MIXED8)
    formal_partition = word_partition(formal_word)
    records = []
    for a in range(3):
        for ell in range(3):
            word = (a, 0, 1, ell, 2, 2, 2, 2)
            records.append({
                "a": a,
                "ell": ell,
                "word": "".join(map(str, word)),
                "S8xS3_word_partition": list(word_partition(word)),
                "same_unlabelled_word_orbit_as_formal_candidate": (
                    word_partition(word) == formal_partition
                ),
            })
    matched = [[record["a"], record["ell"]] for record in records
               if record["same_unlabelled_word_orbit_as_formal_candidate"]]
    require(formal_partition == (4, 3, 1) and matched == [[0, 0], [1, 1]],
            "the formal-candidate/OO word-orbit intersection changed")
    require(Counter(tuple(record["S8xS3_word_partition"])
                    for record in records)
            == Counter({(4, 3, 1): 2, (4, 2, 2): 2,
                        (5, 2, 1): 4, (6, 1, 1): 1}),
            "the nine OO word orbit census changed")
    return {
        "formal_word": "".join(map(str, formal_word)),
        "formal_partition": list(formal_partition),
        "OO_normalizations": records,
        "same_unlabelled_orbit_pairs": matched,
        "scope_guard": (
            "word-orbit equality alone is not a labelled chart/source map"
        ),
    }


def main():
    ledger = {
        "old_physical_inventory": audit_old_physical_inventory(),
        "formal_positive_candidate": audit_formal_positive_candidate(),
        "smallest_physical_cokernel": audit_smallest_physical_cokernel(),
        "word_orbit_scope": audit_word_orbit_scope(),
        "verdict": {
            "formal_map_found": True,
            "physical_adjacent_power_generator_found": False,
            "next_missing_datum": (
                "source-valid fourth Spencer/Hasse lift cancelling the Eq defect"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"inventory digest changed: {digest}")
    print("OO adjacent-power relative-generator inventory: PASS")
    print("formal fourth-Hasse chain: d(kappa*n_I)=+kappa*Y*w, target/ores=0")
    print("strict provenance: pq-direct/pr-two-star; all 15 faces retained")
    print("physical descent fails: kappa*(H0-u)*eq and selector(Hm)=1")
    print("old physical boundary rank 1 -> 2 after adjoining the required class")
    print("formal word orbit meets OO normalizations only at (a,ell)=(0,0),(1,1)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
