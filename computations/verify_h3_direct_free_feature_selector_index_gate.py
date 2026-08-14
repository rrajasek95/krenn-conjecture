#!/usr/bin/env python3
"""Identify the canonical h=3 direct-free packet with Gram parameter h=2.

The 90 response matchings on P,S,0,...,5 avoiding PS are in bijection with
ordered endpoints (p,s) on six sites plus a perfect matching of the other
four sites.  This is ``occurrences(2)`` in the uniform Gram checker, not
``occurrences(3)``.  Consequently the pointed feature selector in this
literal packet is Q_(0,1) X_23 (equally Q_(0,1) X_45), of feature degree 2.

The equality is coefficientwise.  It does not collapse the label-faithful
four-edge Euler/PP cube, because Q_(0,1) itself packages the P0 and S1
faces, and the implication X_23=X_45 holds only after endpoint selection.
"""

from __future__ import annotations

import importlib.util
import json
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAM_PATH = ROOT / "computations/verify_uniform_actual_gram_rank_pointed_selector_no_go.py"
EULER_PATH = ROOT / "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py"
PINNED = {
    "computations/verify_uniform_actual_gram_feature_algebra_pointed_monomial.py":
        "4ec0c01122033af3ef5dc3da41a431162d6cad9e3036c0526cd93bff081a405b",
    "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py":
        "2b720f2a81d047454e224ec6af7ad62680c6ffeae33b6d7275cf995789bc8b8c",
    "notes/uniform-actual-gram-feature-algebra-pointed-monomial.md":
        "735df10d941f639f02c9e8155746c7c178d21c858935336db3edfe0600b5f75e",
    "notes/h3-pointed-occurrence-edge-euler-boolean-cube-gate.md":
        "ecb448d30f18e65b6fad4ac51d0a8bd433dfa865d7104d4840b764f061a3d699",
}
EXPECTED_DIGEST = "4343d93bf1c4b4fbfecad2173ee06548fd7d29737366de15fbb5d555165536f5"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def direct_to_gram(matching, euler):
    partner_p = next(
        right if left == euler.P else left
        for left, right in matching if euler.P in (left, right)
    )
    partner_s = next(
        right if left == euler.S else left
        for left, right in matching if euler.S in (left, right)
    )
    require(partner_p >= euler.ZERO and partner_s >= euler.ZERO,
            ("direct edge entered direct-free packet", matching))
    residual = frozenset(
        (left - euler.ZERO, right - euler.ZERO)
        for left, right in matching
        if euler.P not in (left, right) and euler.S not in (left, right)
    )
    return partner_p - euler.ZERO, partner_s - euler.ZERO, residual


def audit():
    for relative, expected in PINNED.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, (relative, observed, expected))

    gram = load("gram_rank_for_index_gate", GRAM_PATH)
    euler = load("euler_cube_for_index_gate", EULER_PATH)

    direct = tuple(euler.OCCURRENCES)
    abstract_h2 = tuple(gram.occurrences(2))
    abstract_h3 = tuple(gram.occurrences(3))
    image = tuple(direct_to_gram(matching, euler) for matching in direct)

    require(len(direct) == len(abstract_h2) == 90,
            (len(direct), len(abstract_h2)))
    require(len(abstract_h3) == 840, len(abstract_h3))
    require(len(set(image)) == 90 and set(image) == set(abstract_h2),
            "direct-free/Gram h=2 bijection failed")

    marked = direct_to_gram(euler.MARKED, euler)
    require(marked == (0, 1, frozenset({(2, 3), (4, 5)})), marked)

    direct_index = {matching: index for index, matching in enumerate(direct)}
    marked_index = direct_index[euler.MARKED]
    q01 = []
    x23 = []
    x45 = []
    full_euler = []
    qx23 = []
    qx45 = []
    for matching in direct:
        p, s, residual = direct_to_gram(matching, euler)
        q = int((p, s) == (0, 1))
        left = int((2, 3) in residual)
        right = int((4, 5) in residual)
        q01.append(q)
        x23.append(left)
        x45.append(right)
        qx23.append(q * left)
        qx45.append(q * right)
        full_euler.append(int(all(edge in matching for edge in euler.MARKED)))

    delta = [int(index == marked_index) for index in range(len(direct))]
    require(qx23 == qx45 == full_euler == delta,
            "quadratic selector stopped being pointed")
    require(q01 != delta and x23 != x45,
            "proper feature faces collapsed globally")
    require(sum(q01) == 3 and sum(x23) == sum(x45) == 12,
            (sum(q01), sum(x23), sum(x45)))

    # The four labelled Euler directions remain four different source
    # faces even though their top product has a shorter coefficient formula.
    single_supports = {
        euler.NAMES[left] + euler.NAMES[right]:
            sum(int((left, right) in matching) for matching in direct)
        for left, right in euler.MARKED
    }
    require(single_supports == {"P0": 15, "S1": 15, "23": 12, "45": 12},
            single_supports)

    ledger = {
        "pins": PINNED,
        "canonical_direct_free_occurrences": len(direct),
        "uniform_gram_parameter": 2,
        "uniform_h2_occurrences": len(abstract_h2),
        "uniform_h3_occurrences": len(abstract_h3),
        "bijection": (
            "remove P-p and S-s; retain ordered partners (p,s) and the "
            "matching on the other four sites"
        ),
        "marked": "P0|S1|23|45 <-> (0,1,{23,45})",
        "pointed_feature_identity": "Q_(0,1)*X_23=Q_(0,1)*X_45=e_f",
        "feature_degree": 2,
        "support_counts": {
            "Q_01": sum(q01), "X_23": sum(x23), "X_45": sum(x45),
            "pointed": sum(delta),
        },
        "labelled_single_face_supports": single_supports,
        "physical_scope": (
            "the quadratic identity is coefficientwise; Q_(0,1) packages "
            "two endpoint faces and the tail implication is fibre-local, "
            "so the label-faithful PP/Euler cube and its relative carrier "
            "remain"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, (digest, EXPECTED_DIGEST))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("canonical h=3 direct-free feature indexing: PASS")
    print("90 occurrences = uniform Gram parameter h=2 (not h=3)")
    print("pointed coefficient selector: Q_(0,1)*X_23 (degree 2)")
    print("physical labelled Euler/PP cube: STILL RELATIVE")
    print("ledger sha256", digest)


if __name__ == "__main__":
    main()
