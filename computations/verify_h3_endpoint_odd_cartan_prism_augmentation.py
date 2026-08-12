#!/usr/bin/env python3
"""Verify the endpoint-odd Cartan-prism reduction.

Let ``s`` interchange the two endpoint orientations and let ``w`` be the
simultaneous tail-colour Weyl action.  If ``H_w`` is the Cartan homotopy

    w - 1 = d H_w + H_w d,

then ``K=(1-s)H_w`` satisfies

    d K + K d = (1-s)(w-1).

The right side is exactly the four-corner residual with coefficients
(-1,+1,+1,-1).  More importantly, every endpoint-even augmentation kills
``K`` before any tail calculation.  The pinned physical cap quotient says
that D, W, target, and anchor are endpoint-even in this packet.  Thus those
readouts are formal consequences of endpoint oddness; source-labelled
descent, ordinary residue, and the eta/sigma ridge packet remain open.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_sl2_weyl_cartan_prism.py":
        "1024864418fea8f7f4ca6c77015972febd236f2a9822112daf20e1cf979bddaa",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_residual_q_reduced_eq_cap_factorization.py":
        "b6cea93a8a009fce3e97eac0b6321c1175686aa47bb374e82bed7f7e0f604cb4",
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
}
EXPECTED_LEDGER_SHA256 = (
    "2fb16b1648b2a69e892a45387bf86430200312d8ecfe1ae8d922a5c403a63c6b"
)

# Four-corner order used throughout the residual-q audits.
CORNERS = ("E+T0", "E-T0", "E+T1", "E-T1")
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def mat_vec(matrix, vector):
    return tuple(sum(Q(entry) * value for entry, value in zip(row, vector,
                                                               strict=True))
                 for row in matrix)


def mat_mul(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(sum(Q(a) * Q(b) for a, b in zip(row, column,
                                                       strict=True))
                       for column in columns)
                 for row in left)


def mat_sub(left, right):
    return tuple(tuple(Q(a) - Q(b) for a, b in zip(row_l, row_r,
                                                   strict=True))
                 for row_l, row_r in zip(left, right, strict=True))


def identity(size):
    return tuple(tuple(Q(int(i == j)) for j in range(size))
                 for i in range(size))


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    # Replay the exact source and cap ledgers rather than relying only on
    # their prose statements.
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "endpoint_odd_commutator",
    )
    commutator_ledger, commutator_digest = commutator.audit()
    require(commutator_digest == commutator.EXPECTED_LEDGER_SHA256,
            "covariance-curvature ledger changed")
    cap = load(
        "computations/verify_h3_residual_q_reduced_eq_cap_factorization.py",
        "endpoint_odd_cap",
    )
    cap_ledger, cap_digest = cap.audit()
    require(cap_digest == cap.EXPECTED_LEDGER_SHA256,
            "reduced-Eq/cap ledger changed")
    ridge = load(
        "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py",
        "endpoint_odd_ridge",
    )
    ridge_audit = ridge.audit()

    require(tuple(map(Q, commutator_ledger["alpha"])) == ALPHA,
            "source commutator alpha changed")
    protected = cap_ledger["four_corner"][
        "strict_aggregate_readouts"
    ]
    require(protected["pure_Eq"] == 0 and protected["ainc"] == 0
            and protected["W"] == 0 and protected["target"] == 0,
            "protected cap readouts stopped vanishing")
    require(tuple(map(Q, protected["residue_corners"])) == ALPHA,
            "labelled residue stopped retaining alpha")

    # Vector order is E+T0,E-T0,E+T1,E-T1.  Endpoint swap and tail swap
    # commute.  Applying (1-s)(w-1) to E+T0 gives the desired alpha.
    endpoint_swap = (
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 1, 0),
    )
    tail_swap = (
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (1, 0, 0, 0),
        (0, 1, 0, 0),
    )
    one = identity(4)
    endpoint_odd = mat_sub(one, endpoint_swap)
    tail_difference = mat_sub(tail_swap, one)
    require(mat_mul(endpoint_swap, tail_swap)
            == mat_mul(tail_swap, endpoint_swap),
            "endpoint and tail involutions stopped commuting")
    mixed_boundary = mat_mul(endpoint_odd, tail_difference)
    seed = (Q(1), Q(0), Q(0), Q(0))
    require(mat_vec(mixed_boundary, seed) == ALPHA,
            ("mixed prism boundary changed", mat_vec(mixed_boundary, seed)))

    # Every endpoint-even functional is a linear combination of the two
    # tailwise sums.  It kills the full image of 1-s, hence it kills K for
    # arbitrary Cartan homotopy values, not only the selected seed.
    even_rows = (
        (1, 1, 0, 0),
        (0, 0, 1, 1),
    )
    even_after_odd = mat_mul(even_rows, endpoint_odd)
    require(even_after_odd == ((0, 0, 0, 0), (0, 0, 0, 0)),
            "endpoint-even augmentation no longer kills endpoint oddness")

    # Alpha is a pure mixed difference: both endpoint marginals and both
    # tail marginals vanish.  This explains simultaneous protection of all
    # corner-independent and one-factor readouts.
    endpoint_marginals = (ALPHA[0] + ALPHA[1], ALPHA[2] + ALPHA[3])
    tail_marginals = (ALPHA[0] + ALPHA[2], ALPHA[1] + ALPHA[3])
    require(endpoint_marginals == (0, 0) and tail_marginals == (0, 0),
            "alpha stopped being a mixed second difference")

    # The operator proof is formal: since s commutes with d,H,w,
    # d(1-s)H+(1-s)Hd=(1-s)(dH+Hd)=(1-s)(w-1).  The pinned Weyl checker
    # proves dH+Hd=w-1 on the universal Cartan complex, and the ridge audit
    # proves strict commutation with the terminal Kähler factor.
    ledger = {
        "theorem": "endpoint-odd Cartan prism protects physical augmentations",
        "corner_order": list(CORNERS),
        "mixed_boundary_alpha": [int(value) for value in ALPHA],
        "operator": "K=(1-s_endpoint) H_w",
        "chain_identity": "dK+Kd=(1-s_endpoint)(w_tail-1)",
        "endpoint_tail_involutions_commute": True,
        "endpoint_marginals": [int(value) for value in endpoint_marginals],
        "tail_marginals": [int(value) for value in tail_marginals],
        "endpoint_even_augmentations_killed": [
            "D", "W", "target", "anchor incidence", "pure Eq aggregate"
        ],
        "labelled_residue_retained": [int(value) for value in ALPHA],
        "source_symbol": {
            "top": 0,
            "codimension_one": 0,
            "codimension_two": "(E_minus-E_plus)(T_zero-T_one)=-delta",
        },
        "ridge_commutation": ridge_audit["formal_interchange_identity"],
        "remaining_obligations": [
            "descend H_w/root contractions to the complete physical labelled source complex",
            "identify the ordinary-residue face with the pinned complete order-six tower",
            "tensor with -dOmega_v for eta/sigma and prove terminal zero-indeterminacy",
        ],
        "scope": (
            "protected-readout theorem after endpoint oddization; it does not "
            "construct the physical source-labelled Cartan contraction or the "
            "relative mapping-cone cell"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("endpoint-odd Cartan ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 endpoint-odd Cartan prism augmentation: PASS")
    print("mixed boundary: (-1,+1,+1,-1) = -delta")
    print("protected endpoint-even readouts: D/W/target/anchor/Eq = 0")
    print("physical source-labelled Cartan descent: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
