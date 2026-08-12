#!/usr/bin/env python3
"""Audit the local E2/E3 transport-square boundary at the affine gate.

The zero-face relation compares the two four-hole matching monomials

    A(w) = x01(w0,w1) x45(w4,w5),
    B(w) = x05(w0,w5) x14(w1,w4).

At d=(0,0,2,2), A(d)+B(d)=0 after the routed 04|15 term is removed.
Changing one residual colour produces an exact matching-base 2x2 minor.
Its factorization is a common-tail same-star Pluecker carrier.  The checker
also freezes a literal edge-monomial counterexample showing that vanishing
on d and every Hamming-one neighbour does not imply global proportionality:
the first obstruction can occur on a Hamming-two face.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json


EXPECTED_LEDGER_SHA256 = (
    "9417e879bd19e1cd282e670f0d77c747a0014c02ecddf6df52a656aab86efa87"
)
COLOURS = (0, 1, 2)
BASE = (0, 0, 2, 2)  # sites 0,1,4,5


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def changed(word, position, colour):
    result = list(word)
    result[position] = colour
    return tuple(result)


def evaluation(word, edges):
    w0, w1, w4, w5 = word
    return edges["01"][w0][w1] * edges["45"][w4][w5]


def alternate_evaluation(word, edges):
    w0, w1, w4, w5 = word
    return edges["05"][w0][w5] * edges["14"][w1][w4]


def determinant(left, right, first, second):
    return left(first) * right(second) - left(second) * right(first)


def constant_matrix(value):
    return tuple(tuple(Q(value) for _ in COLOURS) for _ in COLOURS)


def audit_factorizations():
    # Generic numerical entries make every displayed symbolic factorization
    # check exact over Q without introducing a CAS dependency.
    x01 = tuple(tuple(Q(2 + 3 * a + 5 * b) for b in COLOURS)
                 for a in COLOURS)
    x45 = tuple(tuple(Q(7 + 2 * a + b) for b in COLOURS)
                 for a in COLOURS)
    x05 = tuple(tuple(Q(11 + 4 * a + 3 * b) for b in COLOURS)
                 for a in COLOURS)
    x14 = tuple(tuple(Q(13 + 5 * a + 2 * b) for b in COLOURS)
                 for a in COLOURS)
    edges = {"01": x01, "45": x45, "05": x05, "14": x14}
    A = lambda word: evaluation(word, edges)
    B = lambda word: alternate_evaluation(word, edges)

    formulae = []
    for position, site in enumerate((0, 1, 4, 5)):
        for colour in COLOURS:
            if colour == BASE[position]:
                continue
            neighbour = changed(BASE, position, colour)
            delta = determinant(B, A, BASE, neighbour)
            if site == 0:
                expected = (
                    x14[0][2] * x45[2][2]
                    * (x05[0][2] * x01[colour][0]
                       - x05[colour][2] * x01[0][0])
                )
            elif site == 1:
                expected = (
                    x05[0][2] * x45[2][2]
                    * (x14[0][2] * x01[0][colour]
                       - x14[colour][2] * x01[0][0])
                )
            elif site == 4:
                expected = (
                    x05[0][2] * x01[0][0]
                    * (x14[0][2] * x45[colour][2]
                       - x14[0][colour] * x45[2][2])
                )
            else:
                expected = (
                    x14[0][2] * x01[0][0]
                    * (x05[0][2] * x45[2][colour]
                       - x05[0][colour] * x45[2][2])
                )
            require(delta == expected,
                    f"the site-{site} E2 factorization changed")
            formulae.append({
                "site": site,
                "new_colour": colour,
                "delta": str(delta),
                "factorization_verified": True,
            })
    return formulae


def audit_first_square_counterexample():
    # B is the constant matching monomial 1.  A is -1 everywhere except at
    # the (w0,w1)=(1,1) corner, where its 01 edge vanishes.  Thus A+B is
    # zero at BASE and all its Hamming-one neighbours, while the first
    # Hamming-two face is nonzero.  All values come from literal products of
    # four physical edge matrices.
    minus_one_except_11 = tuple(tuple(
        Q(0) if (a, b) == (1, 1) else Q(-1)
        for b in COLOURS) for a in COLOURS)
    edges = {
        "01": minus_one_except_11,
        "45": constant_matrix(1),
        "05": constant_matrix(1),
        "14": constant_matrix(1),
    }
    A = lambda word: evaluation(word, edges)
    B = lambda word: alternate_evaluation(word, edges)
    defect = lambda word: A(word) + B(word)

    neighbours = []
    for position, site in enumerate((0, 1, 4, 5)):
        for colour in COLOURS:
            if colour == BASE[position]:
                continue
            word = changed(BASE, position, colour)
            require(defect(word) == 0,
                    "the counterexample stopped being first-square flat")
            require(determinant(B, A, BASE, word) == 0,
                    "a Hamming-one E2 curvature became nonzero")
            neighbours.append({"site": site, "colour": colour, "word": word})

    obstruction = (1, 1, 2, 2)
    require(defect(BASE) == 0 and defect(obstruction) == 1,
            "the Hamming-two obstruction changed")

    # The E3 determinant on BASE, any Hamming-one neighbour, and a second
    # Hamming-one neighbour vanishes because the A and B evaluation vectors
    # agree up to sign on that first star.  This records that adjoining the
    # first Bianchi face alone does not see the Hamming-two defect.
    e3_vanishing = 0
    for left_index in range(len(neighbours)):
        for right_index in range(left_index + 1, len(neighbours)):
            u = neighbours[left_index]["word"]
            v = neighbours[right_index]["word"]
            # det [[B],[A],[1]] on the three states.
            determinant3 = (
                B(BASE) * (A(u) - A(v))
                - B(u) * (A(BASE) - A(v))
                + B(v) * (A(BASE) - A(u))
            )
            require(determinant3 == 0,
                    "the first-star E3 face stopped being flat")
            e3_vanishing += 1

    return {
        "base": BASE,
        "hamming_one_states": len(neighbours),
        "flat_E3_faces": e3_vanishing,
        "first_nonzero_face": obstruction,
        "base_defect": str(defect(BASE)),
        "hamming_two_defect": str(defect(obstruction)),
        "literal_edge_assignment": (
            "x05=x14=x45=1; x01(a,b)=-1 except x01(1,1)=0"
        ),
    }


def main():
    ledger = {
        "local_E2_factorizations": audit_factorizations(),
        "first_square_counterexample": audit_first_square_counterexample(),
        "proved_positive": (
            "nonzero Hamming-one matching-base curvature factors as a "
            "localized common-tail same-star Pluecker carrier"
        ),
        "refuted_implication": (
            "flatness at the base and every Hamming-one neighbour, even "
            "with all first-star E3 faces, does not imply global matching-"
            "base proportionality or complete-column dependence"
        ),
        "replacement_target": (
            "Hamming-cube descent: the first nonflat face gives a literal "
            "carrier; if every face is flat, source-saturation must lift "
            "global matching-evaluation dependence to a one-star joint-"
            "kernel deletion"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"local transport-square ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("h3 local E2/E3 transport-square boundary: PASS")


if __name__ == "__main__":
    main()
