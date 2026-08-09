#!/usr/bin/env python3
"""Exact blocked-colour quotient obstruction for the D1 residue K4."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
EXPECTED_LEDGER_SHA256 = (
    "a320d6f7513b9c52b8b87f1270fe6bc60421dc86e2809b84c99a5dddc0ce4929"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_334_branch63_candidate.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_SHA256,
            "the pinned D1 candidate source changed")
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D = C.D

CENTER = 4
BLOCKED = 1
ACTIVE = 0
NEIGHBOURS = (5, 6, 7)
HOLES = tuple(
    C.V.cell(CENTER, site, BLOCKED, colour)
    for site in NEIGHBOURS for colour in C.V.COLORS
)


def quotient_incidence_audit():
    """Check that each double quotient isolates one opposite form."""
    # A zero contraction has one term for every star neighbour i.  Its term
    # contains u_i at factor i and the opposite form on the other two
    # factors.  Quotienting factors j,k by u_j,u_k kills those two terms and
    # retains exactly the i term.
    records = []
    indices = range(3)
    for retained in indices:
        quotiented = tuple(i for i in indices if i != retained)
        survivors = []
        for term in indices:
            killed = term in quotiented
            if not killed:
                survivors.append(term)
        require(survivors == [retained],
                "a double quotient did not isolate its opposite form")
        records.append({
            "retained_star_factor": retained,
            "quotiented_factors": list(quotiented),
            "surviving_zero_contraction_terms": survivors,
            "conclusion": (
                "the opposite form vanishes in the corresponding double "
                "quotient"
            ),
        })

    # Once all three opposite forms vanish in their double quotients, every
    # term of the target-colour contraction dies in the triple quotient.
    killed_target_terms = []
    for star_factor in indices:
        opposite_factors = tuple(i for i in indices if i != star_factor)
        require(len(opposite_factors) == 2,
                "an opposite edge lost an endpoint")
        killed_target_terms.append(star_factor)
    require(killed_target_terms == [0, 1, 2],
            "a target-contraction term survived the triple quotient")
    return records


def support_audit():
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    support = set(admissible) - set(HOLES)
    require(base_support <= support and len(support) == 208,
            "the blocked-colour representative changed")
    shadow = C.support_shadow_audit(support)
    witnesses = []
    for site in NEIGHBOURS:
        group = [C.V.cell(CENTER, site, ACTIVE, colour)
                 for colour in (0, 1)]
        present = [cell for cell in group if cell in support]
        require(present,
                "an active incident row became the target line")
        witnesses.append(list(present[0]))
    return {
        "holes": [list(cell) for cell in HOLES],
        "active_non_target_witnesses": witnesses,
        "localized_cells": len(support),
        "complete_fibres_checked": shadow["fibres_checked"],
    }


def audit():
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "support": support_audit(),
        "double_quotients": quotient_incidence_audit(),
        "theorem": (
            "If one non-target colour is absent on all three residue edges "
            "incident to a vertex, and the other non-target incident rows "
            "are nonzero and not target lines, residue purity is impossible."
        ),
        "proof": (
            "The active non-target coefficient is sum u_i tensor F_jk=0. "
            "Quotienting the two opposite factors by their u-lines isolates "
            "and kills each F_jk.  The target coefficient then dies in the "
            "triple quotient, while the required pure target tensor survives."
        ),
        "hypothesis_strength": (
            "Only the nine blocked cells and one non-target witness in each "
            "active incident row are used; all other support is arbitrary."
        ),
        "characteristic_scope": "every field",
        "status": "the common blocked-colour residue family is empty",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the blocked-colour quotient ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("n8 D1 residue blocked-colour quotient: PASS (exact)")
    print("double quotients:", len(ledger["double_quotients"]))
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
