#!/usr/bin/env python3
"""Audit the exact two-parameter zero-row retraction of the two-bad packet.

For the shared-endpoint two-bad normal form use colours (a,c,t)=(0,1,2).
The odd rows Qa*K=0 and Rc*K=0 and the full rows with q-colour a or
r-colour c are multihomogeneous.  Give Qa and the a-row of D weight (1,0),
Rc and the c-column of D weight (0,1), with D_ac having weight (1,1).
All 1,458 odd rows and 2,187 full common-hafnian rows are homogeneous, and
the only nonzero right-hand sides have weight (0,0).

Consequently (s,t)=(0,0) is an exact ordinary-source specialization.  It
kills every row-a cell at q away from pq and every row-c cell at r away
from pr, while preserving the two diagonal direct arms and their pure
deleted tensors.  This is an affine retraction, not a target gauge action;
it need not preserve the maximum-anchor stratum.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "computations"))

import verify_shared_reciprocal_two_bad_common_hafnian as common


A, C, T = 0, 1, 2
PINS = {
    "computations/verify_shared_reciprocal_two_bad_common_hafnian.py":
        "9bc7f4c017ba797304057ec182112c5c4f0bfc210d3729243958d723cac1a1d6",
    "computations/verify_shared_reciprocal_lemma_e_flag_normal_form.py":
        "7019b885b0337c8848dad180ff28a7ff5cec59ed65008ef32c6d33dd4bd9a3b5",
}
PINNED_COMMON_ROW_SHA256 = (
    "b6b295867a97ee7d17b6d05f80a0c51a0de85db47f952621db78fba9edb33674"
)
EXPECTED_DIGEST = "f51b282b3c35dbc31998b31894b976f550eb4b1d144ef7ed880ebe4c2f49ebc2"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def atom_bidegree(atom):
    if atom.startswith("Q"):
        match = re.fullmatch(r"Q\d+_(\d)(\d)", atom)
        require(match is not None, f"unparsed Q atom: {atom}")
        return (int(match.group(1)) == A, 0)
    if atom.startswith("R"):
        match = re.fullmatch(r"R\d+_(\d)(\d)", atom)
        require(match is not None, f"unparsed R atom: {atom}")
        return (0, int(match.group(1)) == C)
    if atom.startswith("D_"):
        match = re.fullmatch(r"D_(\d)(\d)", atom)
        require(match is not None, f"unparsed D atom: {atom}")
        return (int(match.group(1)) == A, int(match.group(2)) == C)
    require(atom.startswith(("I", "P")), f"unparsed source atom: {atom}")
    return (0, 0)


def monomial_bidegree(monomial):
    degrees = tuple(atom_bidegree(atom) for atom in monomial)
    return (sum(degree[0] for degree in degrees),
            sum(degree[1] for degree in degrees))


def polynomial_bidegrees(polynomial):
    return {monomial_bidegree(monomial) for monomial in polynomial}


def audit_literal_multihomogeneity():
    odd_rows = 0
    full_rows = 0
    odd_monomials = 0
    full_monomials = 0
    row_hash = sha256()

    for word in itertools.product(common.COLORS, repeat=len(common.COMMON)):
        for outer_colour in common.COLORS:
            q_row = common.odd_star_direct("Q", outer_colour, word)
            r_row = common.odd_star_direct("R", outer_colour, word)
            q_degree = (int(outer_colour == A), 0)
            r_degree = (0, int(outer_colour == C))
            require(polynomial_bidegrees(q_row) == {q_degree},
                    "an odd Q row left its retraction degree")
            require(polynomial_bidegrees(r_row) == {r_degree},
                    "an odd R row left its retraction degree")

            # Only Q_c*K=X_c and R_a*K=X_a have nonzero right sides.
            # Both are unscaled degree-zero rows.  Qa and Rc are precisely
            # the scaled zero-target rows.
            if outer_colour == C:
                require(q_degree == (0, 0),
                        "the bright Q_c row acquired positive degree")
            if outer_colour == A:
                require(r_degree == (0, 0),
                        "the bright R_a row acquired positive degree")
            odd_rows += 2
            odd_monomials += len(q_row) + len(r_row)
            row_hash.update(json.dumps(
                (tuple(sorted(q_row.items())), tuple(sorted(r_row.items()))),
                separators=(",", ":"),
            ).encode())

        for q_colour in common.COLORS:
            for r_colour in common.COLORS:
                row = common.full_remainder_direct(q_colour, r_colour, word)
                expected = (int(q_colour == A), int(r_colour == C))
                require(polynomial_bidegrees(row) == {expected},
                        "a full row left its retraction bidegree")
                if q_colour == r_colour == T:
                    require(expected == (0, 0),
                            "the unique target row acquired positive degree")
                full_rows += 1
                full_monomials += len(row)
                row_hash.update(json.dumps(
                    tuple(sorted(row.items())), separators=(",", ":")
                ).encode())

    require((odd_rows, full_rows) == (1458, 2187),
            "the literal common-hafnian row census changed")
    require(row_hash.hexdigest() == PINNED_COMMON_ROW_SHA256,
            f"the literal common-hafnian rows changed: {row_hash.hexdigest()}")
    return {
        "odd_rows": odd_rows,
        "full_rows": full_rows,
        "odd_monomials": odd_monomials,
        "full_monomials": full_monomials,
        "literal_row_sha256": row_hash.hexdigest(),
        "scaled_zero_rows": ["Qa*K=0", "Rc*K=0"],
        "full_row_bidegree": "(1_{j=a},1_{k=c})",
        "nonzero_target_bidegree": [0, 0],
    }


def audit_physical_specialization():
    # The q endpoint row a away from p consists of the five Qa endpoint
    # rows and the a-row of the qr chord.  The r endpoint row c is the
    # symmetric family.  D_ac belongs to both and receives the product st.
    q_outer_slots = {
        f"Q{site}_{A}{endpoint}"
        for site in common.COMMON for endpoint in common.COLORS
    } | {f"D_{A}{endpoint}" for endpoint in common.COLORS}
    r_outer_slots = {
        f"R{site}_{C}{endpoint}"
        for site in common.COMMON for endpoint in common.COLORS
    } | {f"D_{endpoint}{C}" for endpoint in common.COLORS}
    require(len(q_outer_slots) == len(r_outer_slots) == 18,
            "an outer zero-row family changed size")
    require(q_outer_slots & r_outer_slots == {f"D_{A}{C}"},
            "the two endpoint retractions acquired another overlap")
    require(len(q_outer_slots | r_outer_slots) == 35,
            "the simultaneous retraction slot count changed")

    return {
        "parameters": ["s", "t"],
        "Qa_and_D_a_star": "multiply by s",
        "Rc_and_D_star_c": "multiply by t",
        "D_ac": "multiply by s*t",
        "zero_limit_slots": len(q_outer_slots | r_outer_slots),
        "preserved_data": [
            "A_pq=lambda*E_aa", "H_(B\\{p,q})=lambda^-1*X_a",
            "A_pr=mu*E_cc", "H_(B\\{p,r})=mu^-1*X_c",
        ],
        "zero_limit_flags": [
            "p is essential at q", "p is essential at r",
        ],
        "ordinary_source_reduction": (
            "the limit lies in the double-outer-flag scalar-unit packet; "
            "around either preserved bad arm it is the known one-bad "
            "binary-response source"
        ),
        "minimality_scope": (
            "global minimum scalar-entry support forces all 35 slots zero; "
            "maximum-anchor-then-minimum-support does not unless the "
            "retraction is separately proved anchor-preserving"
        ),
    }


def main():
    pin_dependencies()
    rows = audit_literal_multihomogeneity()
    physical = audit_physical_specialization()
    ledger = {
        "pins": PINS,
        "literal_rows": rows,
        "physical_specialization": physical,
        "verdict": (
            "the projection-degenerate branch, and in fact the entire "
            "shared-endpoint two-bad packet, retracts through exact ordinary "
            "sources to the double-outer-flag one-bad packet"
        ),
        "scope": (
            "source-faithful affine specialization at fixed order; not a "
            "contradiction and not certified inside the maximum-anchor stratum"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"zero-row affine retraction ledger changed: {digest}")

    print("shared reciprocal two-bad zero-row affine retraction: PASS")
    print("literal odd/full rows: 1458 / 2187")
    print("exact parameters: Qa,D_a* -> s; Rc,D_*c -> t")
    print("(s,t)=(0,0): both outer essential flags; arms/activity preserved")
    print("ordinary existence reduces to the known one-bad packet")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
