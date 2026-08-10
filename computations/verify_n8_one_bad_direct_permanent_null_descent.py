#!/usr/bin/env python3
"""Exact permanent-null descent for the two fixed-star one-bad packets.

Relabel the unary top colour as 0 and the two response colours as 1,2.
For either fixed star orientation, let p_i and s_j be the literal one-site
coordinate ports.  With

    K = ((1, 1), (-1, 1)),
    R_K = sum K_ij p_i s_j,

the first insertion is X_1+X_2 by the full 2x2 response packet.  The four
ports are distinct, so R_K is a literal K2,2.  Its only two-edge matching
coefficient is perm(K)=1-1=0, hence R_K^[2]=0 source-coefficientwise;
R_K^[3]=0 because it is supported on only four sites.  Therefore

    (q+R_K)^[3] = q^[3] + R_K q^[2] = X_0+X_1+X_2.

This produces a forbidden six-site ternary source and closes both fixed-star
one-bad orientations using the pinned arbitrary-complex N=6 theorem.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIX_SITE_THEOREM = "proofs/six-site-arbitrary-complex-obstruction.md"
SIX_SITE_THEOREM_SHA256 = (
    "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713"
)
EXPECTED_LEDGER_SHA256 = (
    "ee43c4d86ffa7969b78c4d2eaa27eca79c3c407dd217045df0aac5eebd38ee89"
)

SITES = tuple(range(6))
TOP = 0
RESPONSE_COLOURS = (1, 2)
K = ((Fraction(1), Fraction(1)),
     (Fraction(-1), Fraction(1)))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return (left, right), (left_colour, right_colour)


def matching_tensor(vertices, edges):
    vertices = tuple(sorted(vertices))
    tensor = Counter()
    for word in itertools.product(range(3), repeat=len(vertices)):
        colouring = dict(zip(vertices, word))
        coefficient = Fraction(0)
        for matching in perfect_matchings(vertices):
            term = Fraction(1)
            for left, right in matching:
                term *= edges.get(cell(
                    left, right, colouring[left], colouring[right]
                ), Fraction(0))
            coefficient += term
        if coefficient:
            tensor[word] = coefficient
    return tensor


def insert_fixed(tensor, fixed):
    result = Counter()
    remaining = tuple(site for site in SITES if site not in fixed)
    for word, coefficient in tensor.items():
        colouring = dict(fixed)
        colouring.update(dict(zip(remaining, word)))
        result[tuple(colouring[site] for site in SITES)] += coefficient
    return result


def star_data(orbit):
    # Rows/columns are ordered by response colours 1,2.  Orbit 1 reverses
    # only the two colour-2 endpoints.
    if orbit == 0:
        p_sites = (3, 2)
        s_sites = (5, 4)
        cross_complements = ((0, 1, 2, 5), (0, 1, 3, 4))
    else:
        p_sites = (3, 4)
        s_sites = (5, 2)
        cross_complements = ((0, 1, 4, 5), (0, 1, 2, 3))
    return p_sites, s_sites, cross_complements


def build_insertion(orbit):
    p_sites, s_sites, cross_complements = star_data(orbit)
    require(len(set(p_sites + s_sites)) == 4
            and not (set(p_sites) & set(s_sites)),
            f"orbit {orbit} lost four distinct binary ports")
    edges = {}
    provenance = []
    for row, row_colour in enumerate(RESPONSE_COLOURS):
        for column, column_colour in enumerate(RESPONSE_COLOURS):
            source_cell = cell(
                p_sites[row], s_sites[column],
                row_colour, column_colour,
            )
            require(source_cell not in edges,
                    f"orbit {orbit} collapsed two insertion sources")
            edges[source_cell] = K[row][column]
            provenance.append({
                "row_colour": row_colour,
                "column_colour": column_colour,
                "p_site": p_sites[row],
                "s_site": s_sites[column],
                "cell": [list(source_cell[0]), list(source_cell[1])],
                "coefficient": str(K[row][column]),
            })
    return edges, provenance, p_sites, s_sites, cross_complements


def response_first_insertion(p_sites, s_sites):
    # This reconstructs R_K q^[2] from the exact fixed-star premises
    # p_i s_j q^[2] = delta_ij X_i.  It is independent of unknown q cells.
    result = Counter()
    response_rows = []
    for row, row_colour in enumerate(RESPONSE_COLOURS):
        for column, column_colour in enumerate(RESPONSE_COLOURS):
            fixed = {
                p_sites[row]: row_colour,
                s_sites[column]: column_colour,
            }
            if row == column:
                complement = tuple(site for site in SITES if site not in fixed)
                cofactor = {(row_colour,) * len(complement): Fraction(1)}
            else:
                cofactor = {}
            lifted = insert_fixed(cofactor, fixed)
            for word, coefficient in lifted.items():
                result[word] += K[row][column] * coefficient
            response_rows.append({
                "row_colour": row_colour,
                "column_colour": column_colour,
                "port_sites": [p_sites[row], s_sites[column]],
                "cofactor": (f"X{row_colour}" if row == column else "0"),
                "K_coefficient": str(K[row][column]),
            })
    require(result == Counter({
        (1,) * 6: Fraction(1),
        (2,) * 6: Fraction(1),
    }), "the permanent-null first insertion changed")
    return result, response_rows


def audit_orbit(orbit):
    edges, provenance, p_sites, s_sites, cross_complements = build_insertion(
        orbit
    )
    ports = tuple(sorted(set(p_sites + s_sites)))
    second = matching_tensor(ports, edges)
    permanent = K[0][0] * K[1][1] + K[0][1] * K[1][0]
    require(permanent == 0 and second == Counter(),
            f"orbit {orbit} lost permanent-null R^[2]")

    third = matching_tensor(SITES, edges)
    require(third == Counter(),
            f"orbit {orbit} acquired an R^[3] matching")
    first, response_rows = response_first_insertion(p_sites, s_sites)

    top = Counter({(TOP,) * 6: Fraction(1)})
    completed = top + first
    require(completed == Counter({
        (0,) * 6: Fraction(1),
        (1,) * 6: Fraction(1),
        (2,) * 6: Fraction(1),
    }), f"orbit {orbit} failed clean six-site completion")
    return {
        "p_sites_by_colour_1_2": list(p_sites),
        "s_sites_by_colour_1_2": list(s_sites),
        "four_distinct_ports": True,
        "cross_cofactor_sets": [list(vertices)
                                  for vertices in cross_complements],
        "K": [[str(value) for value in row] for row in K],
        "det_K": str(K[0][0] * K[1][1] - K[0][1] * K[1][0]),
        "perm_K": str(permanent),
        "literal_insertion_sources": provenance,
        "full_response_rows": response_rows,
        "R_K_q_squared": ["X1", "X2"],
        "R_K_squared": "zero tensor on the four ports",
        "R_K_squared_q": "zero for arbitrary q",
        "R_K_cubed": "site-zero on six sites",
        "completed_top": ["X0", "X1", "X2"],
    }


def main():
    actual = sha256((ROOT / SIX_SITE_THEOREM).read_bytes()).hexdigest()
    require(actual == SIX_SITE_THEOREM_SHA256,
            "the pinned arbitrary-complex six-site theorem changed")
    require(K[0][0] and K[1][1],
            "the canonical permanent-null cap lost a diagonal response")
    orbits = [audit_orbit(orbit) for orbit in (0, 1)]
    ledger = {
        "six_site_theorem": {
            "path": SIX_SITE_THEOREM,
            "sha256": SIX_SITE_THEOREM_SHA256,
            "statement": "H6(A) != Delta_(6,3) for arbitrary complex blocks",
        },
        "colour_relabelling": {
            "unary_top": 0,
            "binary_response_rows": [1, 2],
        },
        "fixed_star_orbits": orbits,
        "exact_identity": (
            "(q+R_K)^[3]=q^[3]+R_K q^[2]+R_K^[2]q+R_K^[3]="
            "X0+X1+X2"
        ),
        "verdict": (
            "the canonical permanent-null direct binary cap is clean in "
            "both fixed-star orientations; either hypothetical one-bad "
            "packet would descend to the forbidden six-site ternary target"
        ),
        "scope": (
            "literal fixed one-site coordinate ports and the complete 2x2 "
            "response tensor; this does not extend to arbitrary multi-site "
            "star forms, where repeated-row higher insertions can survive"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"one-bad permanent-null descent ledger changed: {digest}")

    print("N=8 one-bad direct permanent-null descent: PASS")
    print("fixed-star orbits: 2; four distinct literal ports in each")
    print("K diagonal/determinant/permanent: (1,1) / 2 / 0")
    print("higher defects R^[2]q / R^[3]: zero / zero")
    print("clean residual top: X0+X1+X2 (forbidden by N=6 theorem)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
