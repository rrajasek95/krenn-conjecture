#!/usr/bin/env python3
"""Decompose the P2 0102 private face and audit q23 reinsertion.

The first P2 placement gate isolates an endpoint-even occurrence vector
r_0102 modulo the complete response line.  This checker decomposes it under
endpoint adjacency B (eigenvalues 4,0,-2).  The 4-part is exactly the
constant response row; the surviving private part lies in the 0 and -2
even centered summands.  Its endpoint-odd projection is zero, so it does
not enter the already typed active-clean orientation fork.  Coefficientwise
it is another B-4 debt with an explicit preimage.

Finally the principal-parts product rule for reinsertion q23:21 is audited:

    d(q23*a)=q23*d(a)+dq23*a.

The dq23 face is a distinct nonzero occurrence-private block.  Thus a
physical lift of the displayed B-4 preimage must totalize both its lower
boundary and its labelled reinsertion conormal.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "notes/h2-p2-0112-one-endpoint-hasse-placement-gate.md":
        "5b17afb39c796d79021e0c16fb9e9d0e65c33acc9c7d1b8b6185747bd1450ab5",
    "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py":
        "47ea1f915429dc7937ef2e81037c0494136d9ae379d76e0584bb22cef8e0d390",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
}
EXPECTED_LEDGER_SHA256 = (
    "4aed2e5ba33a3ac820c1f7b62c1a75a57565f16f9fd721cfb5f4592a76f1e28f"
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


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * value for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    first = load(
        "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py",
        "p2_private_first",
    )
    first_ledger, first_digest = first.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256,
            "the initial P2 placement ledger changed")
    r = tuple(map(Q, first_ledger["one_endpoint_Hasse_faces"]
                  ["representative_occurrence_vector"]))

    parity = load(
        "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py",
        "p2_private_parity",
    )
    occurrence, values, lookup, swap, b_matrix, s_matrix = parity.endpoint_data()
    size = len(values)
    identity = parity.identity(size)
    require(size == 12 and parity.matvec(s_matrix, r) == r,
            "the 0102 face stopped being endpoint-even")

    # Spectral projectors for B on the endpoint-even occurrence module.
    # The B eigenvalues are 4,0,-2.
    b_plus_two = parity.matrix_add(
        b_matrix, parity.matrix_scale(2, identity)
    )
    b_minus_four = parity.matrix_add(
        b_matrix, parity.matrix_scale(-4, identity)
    )
    p4 = scale(Q(1, 24), parity.matvec(
        parity.matmul(b_matrix, b_plus_two), r
    ))
    p0 = scale(Q(-1, 8), parity.matvec(
        parity.matmul(b_minus_four, b_plus_two), r
    ))
    pminus2 = scale(Q(1, 12), parity.matvec(
        parity.matmul(b_minus_four, b_matrix), r
    ))
    require(add(p4, p0, pminus2) == r,
            "the B spectral decomposition stopped reconstructing r0102")
    require(parity.matvec(b_matrix, p4) == scale(4, p4)
            and parity.matvec(b_matrix, p0) == (Q(0),) * size
            and parity.matvec(b_matrix, pminus2) == scale(-2, pminus2),
            "the endpoint adjacency eigenvalues changed")
    require(all(parity.matvec(s_matrix, vector) == vector
                for vector in (p4, p0, pminus2)),
            "a spectral piece acquired endpoint-odd parity")

    one = (Q(1),) * size
    require(p4 == scale(Q(-1, 18), one),
            "the B=4 piece stopped being the complete response line")
    private = add(p0, pminus2)
    require(add(p4, private) == r
            and sum(private, Q(0)) == 0
            and private != (Q(0),) * size,
            "the augmentation-zero private piece changed")
    odd_projection = scale(Q(1, 2), add(
        private, scale(-1, parity.matvec(s_matrix, private))
    ))
    require(odd_projection == (Q(0),) * size,
            "the private face entered the endpoint-odd line")

    # B-4 is invertible on the 0 and -2 summands.
    private_preimage = add(scale(Q(-1, 4), p0),
                           scale(Q(-1, 6), pminus2))
    require(parity.matvec(b_minus_four, private_preimage) == private,
            "the second even B-4 preimage changed")
    integral_private_preimage = scale(432, private_preimage)
    require(all(value.denominator == 1 for value in integral_private_preimage),
            "the denominator-432 integral preimage changed")

    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(size))
    require(dot(detector, p4) == 0
            and dot(detector, private) == Q(-13, 6)
            and dot(detector, private_preimage) == Q(35, 72),
            "the representative even private detector changed")

    # Recover the original exact B-4 preimage z from the first gate's input.
    marked = (0, 1, (occurrence.edge(2, 3),))
    c_plus = tuple(Q(6 if value in (marked, swap(marked)) else 0) - 1
                   for value in values)
    z = scale(Q(-1, 24), parity.matvec(
        parity.matrix_add(b_matrix, parity.matrix_scale(6, identity)),
        c_plus,
    ))
    require(parity.matvec(b_minus_four, z) == c_plus
            and sum(z, Q(0)) == 0
            and parity.matvec(s_matrix, z) == z
            and dot(detector, z) == Q(-5, 2),
            "the raw reinsertion coefficient changed")

    # The two summands in d(q*a) are stored in independent q and dq blocks.
    # This is the literal first-PP/Hasse coproduct for a linear q factor.
    zero = (Q(0),) * size
    raw_q_part = c_plus + zero
    raw_dq_part = zero + z
    raw_total = add(raw_q_part, raw_dq_part)
    require(raw_total[:size] == c_plus
            and raw_total[size:] == z
            and raw_dq_part != (Q(0),) * (2 * size),
            "the q23 product-rule face changed")

    # If the coefficientwise second B-4 preimage is promoted to the missing
    # one-endpoint cell, reinsertion forces its own dq companion as well.
    repair_q_part = private + zero
    repair_dq_part = zero + private_preimage
    repair_total = add(repair_q_part, repair_dq_part)
    require(repair_total[:size] == private
            and repair_total[size:] == private_preimage
            and dot(detector, repair_total[size:]) == Q(35, 72),
            "the repaired reinsertion pair changed")

    ledger = {
        "theorem": "h2 P2 0102 private parity and q23 reinsertion gate",
        "pins": PINS,
        "representative": {
            "word": "0102",
            "vector": [str(value) for value in r],
            "endpoint_parity": "even",
            "augmentation": str(sum(r, Q(0))),
        },
        "endpoint_adjacency_decomposition": {
            "eigenvalues": [4, 0, -2],
            "B4_complete_part": [str(value) for value in p4],
            "B0_private_part": [str(value) for value in p0],
            "Bminus2_private_part": [str(value) for value in pminus2],
            "private_part": [str(value) for value in private],
            "private_augmentation": 0,
            "private_endpoint_odd_projection": 0,
            "active_clean_orientation_fork_applies": False,
            "reason": "the typed active-clean carrier is endpoint-odd",
        },
        "second_even_Bminus4_debt": {
            "identity": "(B-4I)z_private=r_private",
            "preimage": [str(value) for value in private_preimage],
            "integral_denominator": 432,
            "integral_preimage": [int(value)
                                  for value in integral_private_preimage],
            "physical_lift_constructed": False,
        },
        "representative_detector": {
            "support": "+e0+e3-e1-e6",
            "on_complete_part": "0",
            "on_private_part": "-13/6",
            "on_private_preimage": "35/72",
            "physical_terminal": False,
        },
        "q23_reinsertion": {
            "product_rule": "d(q23*a)=q23*d(a)+dq23*a",
            "raw_lower_coefficient": "c_plus",
            "raw_dq23_coefficient": [str(value) for value in z],
            "raw_dq23_augmentation": 0,
            "raw_dq23_private_detector": "-5/2",
            "repair_lower_coefficient": "r_private",
            "forced_repair_dq23_coefficient": [str(value)
                                                for value in private_preimage],
            "forced_repair_dq23_private_detector": "35/72",
            "ordinary_residue_aggregate": 0,
            "occurrence_labelled_conormal_nonzero": True,
        },
        "sharp_interface": (
            "the missing 0102 endpoint-even PP section must realize the "
            "second B-4 preimage and, after q23:21 reinsertion, carry its "
            "independent dq23:21 occurrence-labelled conormal; neither "
            "piece enters the existing endpoint-odd active-clean fork"
        ),
        "scope": (
            "coefficient and first-PP associated graded of the literal "
            "0112/q23 cut.  The B-4 identity does not itself construct its "
            "physical lift, and the displayed detector is not promoted to "
            "a full augmented terminal."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h2 P2 private/reinsertion ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("0102 private face: ENDPOINT-EVEN")
    print("B spectrum: constant 4-line plus private 0,-2 lines")
    print("active-clean endpoint-odd fork: DOES NOT APPLY")
    print("private face: SECOND COEFFICIENT B-4 DEBT")
    print("q23 reinsertion: NONZERO OCCURRENCE-LABELLED dq23 FACE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
