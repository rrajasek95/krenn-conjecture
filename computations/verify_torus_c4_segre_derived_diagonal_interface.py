#!/usr/bin/env python3
"""Exact rank audit for the torus C4 Segre/derived-diagonal interface.

The ordinary flat locus is the intersection of the two balanced-flattening
rank-one tori.  This checker verifies that their character lattices generate
the full four-factor Segre lattice, records the clean-intersection excess,
and pins the source-relative C4 square to which the Tor criterion applies.
It does not claim to construct the missing physical source contraction.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_local_c4_relative_coherence_curvature_square.py":
        "9753c669db38b29e55706d4d8865c3beb46dcb0835298a90061babcda6483744",
    "notes/local-c4-coherence-curvature-relative-square.md":
        "5ed2232758948b993826d69158f6cdb57a06c077ad3a37af7db3a5005d9b9b43",
    "notes/hafnian-path-forest-straightening.md":
        "0713791a87b692da809b5f64fe8d757d6454d59e550a859b8d7b7dea68598921",
    "notes/augmented-hpl-terminal-bockstein-lemma.md":
        "de1d34da41ed3f845003adec41cb2907b8dc4917ed9c75f6b375ea1aea021f89",
}
EXPECTED_LEDGER_SHA256 = (
    "24061d46bf525cc0b2f3e0126cfba67d920d4fb0f38c6f645108b9f2d24b80a8"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def incidence(n, partitions):
    words = tuple(product(range(n), repeat=4))
    rows = []
    for positions in partitions:
        for value in product(range(n), repeat=len(positions)):
            rows.append(tuple(
                int(tuple(word[position] for position in positions) == value)
                for word in words
            ))
    return rows


def rank(matrix, modulus=None):
    if modulus is None:
        work = [[Q(entry) for entry in row] for row in matrix]
    else:
        work = [[entry % modulus for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        if modulus is None:
            work[pivot_row] = [entry / pivot_value
                               for entry in work[pivot_row]]
        else:
            inverse = pow(pivot_value, -1, modulus)
            work[pivot_row] = [entry * inverse % modulus
                               for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            if modulus is None:
                work[row] = [entry - multiplier * pivot_entry
                             for entry, pivot_entry
                             in zip(work[row], work[pivot_row], strict=True)]
            else:
                work[row] = [
                    (entry - multiplier * pivot_entry) % modulus
                    for entry, pivot_entry
                    in zip(work[row], work[pivot_row], strict=True)
                ]
        pivot_row += 1
    return pivot_row


def audit_lattices(n):
    ambient = n ** 4
    first = incidence(n, ((0, 1), (2, 3)))
    crossed = incidence(n, ((0, 3), (1, 2)))
    full = incidence(n, ((0,), (1,), (2,), (3,)))
    field_records = {}
    for label, modulus in (("Q", None), ("F2", 2), ("F3", 3),
                           ("F5", 5), ("F7", 7)):
        rank_first = rank(first, modulus)
        rank_crossed = rank(crossed, modulus)
        rank_full = rank(full, modulus)
        rank_stacked = rank(first + crossed, modulus)
        row_intersection = rank_first + rank_crossed - rank_stacked
        require(rank_first == 2 * n * n - 1,
                f"{label}: first balanced torus rank changed")
        require(rank_crossed == rank_first,
                f"{label}: crossed balanced torus rank changed")
        require(rank_full == 4 * n - 3,
                f"{label}: full Segre torus rank changed")
        require(row_intersection == rank_full,
                f"{label}: the two pair-additive row spaces stopped "
                "intersecting in the site-additive space")
        field_records[label] = {
            "balanced_parameter_rank": rank_first,
            "full_segre_parameter_rank": rank_full,
            "pair_row_intersection_rank": row_intersection,
        }

    balanced_codimension = ambient - (2 * n * n - 1)
    full_codimension = ambient - (4 * n - 3)
    excess = 2 * balanced_codimension - full_codimension
    require(excess == n ** 4 - 4 * n * n + 4 * n - 1,
            "the clean-intersection excess formula changed")
    return {
        "colours": n,
        "ambient_torus_dimension": ambient,
        "balanced_segre_dimension": 2 * n * n - 1,
        "full_segre_dimension": 4 * n - 3,
        "balanced_codimension": balanced_codimension,
        "full_segre_codimension": full_codimension,
        "derived_excess_rank": excess,
        "Tor1_excess_rank": excess,
        "Tor2_excess_rank": comb(excess, 2),
        "field_rank_checks": field_records,
    }


def outer(left, right, scalar=Q(1)):
    return tuple(tuple(scalar * x * y for y in right) for x in left)


def audit_flat_gauge():
    site = {
        0: (Q(2), Q(3), Q(5)),
        1: (Q(7), Q(11), Q(13)),
        4: (Q(17), Q(19), Q(23)),
        5: (Q(29), Q(31), Q(37)),
    }
    edge = {
        "01": outer(site[0], site[1], Q(2)),
        "45": outer(site[4], site[5], Q(3)),
        "05": outer(site[0], site[5], Q(-1)),
        "14": outer(site[1], site[4], Q(6)),
    }

    checked = 0
    for i, j, k, ell in product(range(3), repeat=4):
        first = edge["01"][i][j] * edge["45"][k][ell]
        crossed = edge["05"][i][ell] * edge["14"][j][k]
        require(first + crossed == 0,
                "the fully decomposable C4 flat equality changed")
        checked += 1

    minors = 0
    for name, matrix in edge.items():
        for i, ip, j, jp in product(range(3), repeat=4):
            require(matrix[i][j] * matrix[ip][jp]
                    == matrix[i][jp] * matrix[ip][j],
                    f"{name}: a site-factor Segre minor became nonzero")
            minors += 1
    return {
        "flat_tensor_entries": checked,
        "edge_rank_one_minors": minors,
        "edge_scalars": {"01": 2, "45": 3, "05": -1, "14": 6},
        "holonomy": "lambda01*lambda45+lambda05*lambda14=0",
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")

    ledger = {
        "ternary_C4_torus": audit_lattices(3),
        "binary_sanity": audit_lattices(2),
        "literal_flat_gauge": audit_flat_gauge(),
        "ordinary_intersection": (
            "on the coefficient torus, the two crossing balanced-rank-one "
            "loci meet scheme-theoretically in the four-factor Segre torus"
        ),
        "scope": (
            "coefficient-torus lattice and derived-intersection theorem; "
            "the stronger zero-tolerant set-theoretic intersection is "
            "separate and is not used here"
        ),
        "wrong_Tor_target": (
            "the Segre-pair derived intersection has unavoidable excess "
            "Tor (rank 56 in degree one for three colours)"
        ),
        "minimal_physical_descent": (
            "identify the depolarized total complex with the literal source "
            "complex and make the terminal readout annihilate its C4-grade "
            "H1; under a polarized resolution this H1 is Tor_1(M~,S)"
        ),
        "stronger_than_needed": (
            "Tor_1(M~,S)=0 in the C4 multidegree is sufficient; vanishing "
            "of all higher Tor or of Segre-pair Tor is not required"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"torus C4 Segre/Tor ledger changed: {digest}")
    print("torus C4 Segre/derived-diagonal interface: PASS")
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
