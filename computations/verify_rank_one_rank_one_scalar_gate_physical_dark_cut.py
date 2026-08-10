#!/usr/bin/env python3
"""Exact incidence audit: every maximal scalar shore has a physical dark cut.

The mathematical proof combines the rank-one scalar-shore cap with the
two-site blocked-target theorem.  This checker pins those source theorems,
exhausts the full-support annihilator choice over F_5, and verifies the
three-site blocker contradiction without making a support ansatz for q.
"""

from hashlib import sha256
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEPENDENCIES = {
    "verify_target_blocked_site_polar_descent.py":
        "bdfbf7a816ad992e3e81b02d0ab6afb1b7ca3d3129e4429985450525f4275eb4",
    "verify_curvature_bearing_cap_to_k6_dark_cut.py":
        "a2c03159a5e10227d805b87a71525a53c43c883b9d9b174a495496d9a37038b9",
    "verify_rank_one_rank_one_scalar_gate_diagonal_cycle.py":
        "a7efd73c93ad435b4026237d83f68b095a3e88cf3f75f3c397e5c8c486ea42f7",
}
EXPECTED_LEDGER_DIGEST = "7e97c3eaf90f94a056f8473bebaf5a9d05f167a1aabeee04de37f2f0df9cdb06"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dependency_guard():
    for name, expected in DEPENDENCIES.items():
        actual = sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, ("dependency changed", name, actual))


def dot(left, right, prime):
    return sum(a * b for a, b in zip(left, right)) % prime


def projective_vectors(prime):
    answer = []
    for vector in product(range(prime), repeat=3):
        if not any(vector):
            continue
        first = next(value for value in vector if value)
        inverse = pow(first, -1, prime)
        normalized = tuple(value * inverse % prime for value in vector)
        if normalized not in answer:
            answer.append(normalized)
    return tuple(answer)


def annihilator_audit(prime=5):
    """Every non-coordinate lambda has a full-support kernel vector."""
    vectors = projective_vectors(prime)
    noncoordinate = tuple(vector for vector in vectors
                          if sum(value != 0 for value in vector) >= 2)
    witnesses = []
    for vector in noncoordinate:
        kernel = tuple(candidate for candidate in vectors
                       if all(candidate) and dot(vector, candidate, prime) == 0)
        require(kernel, ("a non-coordinate label lost full-support kernel", vector))
        witness = kernel[0]
        require(all(witness), "diagonal activity witness lost a coordinate")
        witnesses.append((vector, witness))
    return len(vectors), len(noncoordinate), tuple(witnesses)


def blocker_audit():
    """No-cut blocker inequalities are impossible on only three sites."""
    sites = range(3)
    colours = range(3)
    admissible = 0
    for mask in range(1 << 9):
        blocked = {
            colour: {site for site in sites
                     if mask & (1 << (3 * colour + site))}
            for colour in colours
        }
        # The blocked-target theorem says no dark cut forces at least three
        # blockers for every active target.  All three targets are active.
        if any(len(blocked[colour]) < 3 for colour in colours):
            continue
        # Each local cap-factor span has dimension at most two and therefore
        # cannot contain the three independent target axes.
        local_counts = tuple(sum(site in blocked[colour] for colour in colours)
                             for site in sites)
        if all(count <= 2 for count in local_counts):
            admissible += 1
    require(admissible == 0, "a three-site no-dark-cut blocker survived")
    return 1 << 9, admissible


def audit():
    dependency_guard()
    annihilators = annihilator_audit()
    blockers = blocker_audit()
    ledger = (annihilators, blockers)
    digest = sha256(repr(ledger).encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST is not None:
        require(digest == EXPECTED_LEDGER_DIGEST,
                ("scalar dark-cut ledger changed", digest))
    return annihilators[:2], blockers, digest


def main():
    annihilators, blockers, digest = audit()
    print("rank-(1,1) scalar-shore physical dark cut: passed")
    print(f"  F5 projective/noncoordinate labels : {annihilators[0]}/{annihilators[1]}")
    print(f"  blocker incidence masks            : {blockers[0]}")
    print(f"  no-cut survivors                    : {blockers[1]}")
    print(f"  aggregate ledger digest             : {digest}")
    print("  conclusion                          : every scalar gate exports a dark cut")


if __name__ == "__main__":
    main()
