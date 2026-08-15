#!/usr/bin/env python3
"""Show that setting H0-u=0 does not supply the missing Eq comparison.

The local response complex is N -> Y.  The physical cap top is

    B -> Y + t E,                 t = H0-u.

After base change t=0 the evident map N->B becomes a chain map, but it is
not a quasi-isomorphism: the cap retains the unhit Eq row E.  Its mapping
cone has one-dimensional H0.  A relative cell with boundary tE becomes a
cycle after the same base change and therefore cannot remove this class.
Only an absolute/source-labelled E-preimage makes the cone acyclic.

This is the elementary Tor obstruction behind the protected 126/127
calculation.  It rules out using normalization alone to bypass the missing
response-to-cap operation cell.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json


EXPECTED_LEDGER_SHA256 = (
    "1667bcf3593571e5b37e525bf802333a70e677546517169295eeea1d1c637bbd"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right
                         for left, right in zip(rows[row], rows[answer],
                                                strict=True)]
        answer += 1
    return answer


def homology_dimensions(dimensions: tuple[int, ...],
                        differentials: tuple[tuple[tuple[Q, ...], ...], ...]
                        ) -> tuple[int, ...]:
    """Return H_i dims for C_top -> ... -> C_0.

    ``dimensions`` is ordered C0,C1,... and ``differentials[i-1]`` stores
    columns of d_i:C_i->C_(i-1).
    """
    require(len(differentials) + 1 == len(dimensions),
            (dimensions, len(differentials)))
    ranks = tuple(rank(differential) for differential in differentials)
    for index, differential in enumerate(differentials, start=1):
        require(len(differential) == dimensions[index],
                (index, len(differential), dimensions[index]))
        require(all(len(column) == dimensions[index - 1]
                    for column in differential),
                (index, dimensions[index - 1]))
    answer = []
    for degree, dimension in enumerate(dimensions):
        outgoing = ranks[degree - 1] if degree else 0
        incoming = ranks[degree] if degree < len(ranks) else 0
        answer.append(dimension - outgoing - incoming)
    require(all(value >= 0 for value in answer), answer)
    return tuple(answer)


def normalized_comparison() -> dict[str, object]:
    # X: N -> Y is acyclic.
    d_response = (((Q(1),),),)
    response_h = homology_dimensions((1, 1), d_response)
    require(response_h == (0, 0), response_h)

    # At t=0, C: B -> (Y,E), B |-> Y.  E survives in H0.
    d_cap = (((Q(1), Q(0)),),)
    cap_h = homology_dimensions((2, 1), d_cap)
    require(cap_h == (1, 0), cap_h)

    # Cone(f) for f(N)=B, f(Y)=Y at t=0:
    # C2=X1 -> C1=C1_cap + X0 -> C0=C0_cap.
    # d2(N)=(-B,Y), d1(B,Y)=(Y,Y), all E components zero.
    d1 = ((Q(1), Q(0)), (Q(1), Q(0)))
    d2 = ((Q(-1), Q(1)),)
    require(tuple(sum(d1[column][row] * d2[0][column]
                      for column in range(2)) for row in range(2))
            == (Q(0), Q(0)), "cone d^2")
    cone_h = homology_dimensions((2, 2, 1), (d1, d2))
    require(cone_h == (1, 0, 0), cone_h)

    return {
        "normalization": "t=H0-u=0",
        "response_homology_H0_H1": list(response_h),
        "cap_homology_H0_H1": list(cap_h),
        "evident_map_is_chain_map_after_base_change": True,
        "mapping_cone_homology_H0_H1_H2": list(cone_h),
        "surviving_class": "E=e_Eq",
        "map_is_quasi_isomorphism": False,
    }


def relative_versus_absolute_filler() -> dict[str, object]:
    # A relative K with dK=tE has zero boundary after t=0.  The cap complex
    # has B,K -> Y,E with columns (1,0),(0,0), hence H0=E and H1=K.
    d_relative = (((Q(1), Q(0)), (Q(0), Q(0))),)
    relative_h = homology_dimensions((2, 2), d_relative)
    require(relative_h == (1, 1), relative_h)

    # A genuine absolute/source-labelled filler K_abs -> E produces the
    # identity differential and removes both classes.
    d_absolute = (((Q(1), Q(0)), (Q(0), Q(1))),)
    absolute_h = homology_dimensions((2, 2), d_absolute)
    require(absolute_h == (0, 0), absolute_h)
    return {
        "relative_boundary_before_base_change": "dK_rel=t*E",
        "relative_boundary_after_base_change": 0,
        "relative_cap_homology_H0_H1": list(relative_h),
        "absolute_boundary": "dK_abs=E",
        "absolute_cap_homology_H0_H1": list(absolute_h),
        "normalization_substitutes_for_absolute_filler": False,
    }


def audit() -> tuple[dict[str, object], str]:
    ledger = {
        "theorem": "normalized Eq base change leaves a Tor comparison class",
        "normalized_comparison": normalized_comparison(),
        "relative_versus_absolute_filler": relative_versus_absolute_filler(),
        "interpretation": (
            "Setting H0-u=0 makes the coefficient-level top projection a "
            "chain map but not a quasi-isomorphism.  The unhit reduced-Eq "
            "row survives in H0 of its cone.  A relative t*Eq cell becomes "
            "a new H1 cycle after base change; only an absolute decorated "
            "Eq preimage, equivalently the missing response-to-cap "
            "comparison orbit, removes the obstruction."
        ),
        "scope": (
            "the exact two-term local model of the pinned rank-one Eq "
            "commutator; this is a no-go for normalization/base-change "
            "alone, not a no-go for an unmodeled physical bright primitive"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        print("h3 normalized Eq base-change Tor gate: PASS")
        print("cone homology:", ledger["normalized_comparison"][
            "mapping_cone_homology_H0_H1_H2"])
        print("relative filler homology:", ledger[
            "relative_versus_absolute_filler"][
                "relative_cap_homology_H0_H1"])
        print("absolute filler homology:", ledger[
            "relative_versus_absolute_filler"][
                "absolute_cap_homology_H0_H1"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
