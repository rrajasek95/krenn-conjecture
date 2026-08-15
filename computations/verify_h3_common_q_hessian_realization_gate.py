#!/usr/bin/env python3
"""Common-q Hessian realization after labelled GHZ quotient normalization.

For a literal six-site quadratic q and physical endpoint stars p_i,s_j, put

    H_(xy,bar w) = [q^[2]]_(bar w on U-{x,y}).

The same H coordinate is shared by all nine extensions of bar w at x,y, and

    C_(ij,w) = sum_(x<y)
        (p_i(x,w_x)s_j(y,w_y)+p_i(y,w_y)s_j(x,w_x)) H_(xy,bar w).

Equivalently H is the first derivative of [q^[3]]_w with respect to the
decorated q_xy cell.  The H coordinates themselves obey the three-term
four-site hafnian equations and the disjoint-edge mixed-partial/Schreyer
symmetries.  These equations are independent of the latent involution and
the labelled GHZ slice-rank conditions.

The literal 77-cell guard passes every common-q identity.  If its two missing
pure target slices are repaired only formally by adding X_0 to C_00 and X_1
to C_11, the resulting tensor passes exact labelled GHZ normalization and
all nine coarse target equations, but fails exactly two Hessian realization
coordinates.  The first is the one-scalar identity

    [C_00]_(0^6) = 23 H_(01,0^4) = 23*0 = 0,

whereas the formal repair demands the left side be one.
"""

from __future__ import annotations

import importlib
import os
import sys
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINS = {
    "verify_h3_labelled_ghz_slice_normalization.py":
        "6ee645ab0a1dd7c4130b668d7f98c45d27aad4f88aff226e3061bf0dcf767a9e",
    "../notes/2026-08-15-h3-labelled-ghz-slice-normalization.md":
        "e32f229c12a8fc7b842944e6a26dca7d728f461bf4c01b071b64a838e97b37d2",
}
EXPECTED_LEDGER_SHA256 = (
    "32e0e3257c226402e10868d184094b4dcc5e52d879dc2f41e502199d7781435c"
)


def pin_sources():
    result = {}
    for relative, expected in sorted(PINS.items()):
        path = os.path.normpath(os.path.join(HERE, relative))
        with open(path, "rb") as handle:
            result[relative] = sha256(handle.read()).hexdigest()
        require(result[relative] == expected,
                "pinned source changed: %s (%s)" %
                (relative, result[relative]))
    return result


PINNED = pin_sources()
N = importlib.import_module("verify_h3_labelled_ghz_slice_normalization")
A = N.A

SITES = tuple(range(6))
PAIRS = tuple(combinations(SITES, 2))


def deleted_sites(edge):
    return tuple(site for site in SITES if site not in edge)


def deleted_word(word, edge):
    return tuple(word[site] for site in deleted_sites(edge))


def hessian_key(edge, word):
    return edge + deleted_word(word, edge)


def four_site_hafnian(packet, edge, letters):
    rest = deleted_sites(edge)
    assignment = dict(zip(rest, letters))
    return packet.haf(
        lambda x, y: packet.qe(x, y, assignment[x], assignment[y]), rest)


def build_hessian(packet):
    hessian = {}
    for edge in PAIRS:
        for letters in product(A.COLORS, repeat=4):
            hessian[edge + letters] = four_site_hafnian(packet, edge, letters)
    require(len(hessian) == 15 * 3 ** 4,
            "the deleted-word Hessian does not have 1215 coordinates")
    return hessian


def response_edge(left, right, word, edge):
    x, y = edge
    return (left[3 * x + word[x]] * right[3 * y + word[y]]
            + left[3 * y + word[y]] * right[3 * x + word[x]])


def reconstruct_coordinate(left, right, word, hessian):
    return sum((response_edge(left, right, word, edge)
                * hessian[hessian_key(edge, word)] for edge in PAIRS), Q(0))


def q_cube_derivative(packet, word, edge):
    """Literal derivative of the matching sum with respect to q_edge(word)."""
    total = Q(0)
    for matching in A.L.M6:
        if edge not in matching:
            continue
        term = Q(1)
        for other in matching:
            if other == edge:
                continue
            term *= packet.qe(other[0], other[1],
                              word[other[0]], word[other[1]])
        total += term
    return total


def mixed_hessian_derivative(packet, word, first, second):
    """d H_first / d q_second; zero unless the two edges are disjoint."""
    if set(first) & set(second):
        return Q(0)
    remaining = tuple(site for site in SITES
                      if site not in first and site not in second)
    require(len(remaining) == 2, "two disjoint edges did not leave one edge")
    return packet.qe(remaining[0], remaining[1],
                     word[remaining[0]], word[remaining[1]])


def explicit_hessian_derivative(packet, word, first, second):
    """Differentiate the literal three-term four-site hafnian H_first."""
    rest = deleted_sites(first)
    if not set(second).issubset(rest):
        return Q(0)
    total = Q(0)
    for matching in A.L.perfect_matchings(rest):
        if second not in matching:
            continue
        term = Q(1)
        for edge in matching:
            if edge != second:
                term *= packet.qe(edge[0], edge[1],
                                  word[edge[0]], word[edge[1]])
        total += term
    return total


def audit_common_q(packet, p_vectors, s_vectors):
    hessian = build_hessian(packet)
    derivative_checks = 0
    extension_reuses = 0
    for word in A.WORDS:
        for edge in PAIRS:
            value = hessian[hessian_key(edge, word)]
            require(value == q_cube_derivative(packet, word, edge),
                    "H is not the first q^[3] derivative")
            derivative_checks += 1
    require(derivative_checks == 15 * 3 ** 6,
            "the q^[3] derivative census changed")

    # Each deleted coordinate is reused across the nine choices at its two
    # missing sites.  This is the cross-word compatibility absent from an
    # arbitrary collection of 729 matrices.
    for edge in PAIRS:
        rest = deleted_sites(edge)
        for letters in product(A.COLORS, repeat=4):
            seen = set()
            for endpoint_letters in product(A.COLORS, repeat=2):
                word = [None] * 6
                for site, colour in zip(rest, letters):
                    word[site] = colour
                for site, colour in zip(edge, endpoint_letters):
                    word[site] = colour
                seen.add(hessian[hessian_key(edge, tuple(word))])
                extension_reuses += 1
            require(len(seen) == 1,
                    "a deleted Hessian coordinate depends on reinserted letters")
    require(extension_reuses == 15 * 3 ** 4 * 3 ** 2,
            "the nine-extension reuse census changed")

    schreyer_checks = 0
    for word in A.WORDS:
        for first in PAIRS:
            for second in PAIRS:
                if set(first) & set(second):
                    continue
                left = mixed_hessian_derivative(packet, word, first, second)
                right = mixed_hessian_derivative(packet, word, second, first)
                explicit = explicit_hessian_derivative(
                    packet, word, first, second)
                require(left == explicit == right,
                        "disjoint-edge Hessian mixed partials disagree")
                schreyer_checks += 1
    require(schreyer_checks == 3 ** 6 * 90,
            "the ordered disjoint-edge Schreyer census changed")

    actual = [[None for _ in A.COLORS] for _ in A.COLORS]
    reconstruction_checks = 0
    for i, j in product(A.COLORS, repeat=2):
        vector = []
        for word in A.WORDS:
            value = reconstruct_coordinate(p_vectors[i], s_vectors[j],
                                           word, hessian)
            vector.append(value)
            reconstruction_checks += 1
        actual[i][j] = tuple(vector)
        require(actual[i][j] == A.pair_q2(packet, p_vectors[i], s_vectors[j]),
                "Hessian reconstruction disagrees with literal p_i s_j q^[2]")
    require(reconstruction_checks == 9 * 3 ** 6,
            "the nine-row Hessian reconstruction census changed")
    return hessian, actual, {
        "hessian_coordinates": len(hessian),
        "q_cube_first_derivative_checks": derivative_checks,
        "nine_extension_reuses": extension_reuses,
        "ordered_schreyer_checks": schreyer_checks,
        "nine_row_reconstruction_checks": reconstruction_checks,
    }


def add_vectors(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def audit_formal_ghz_repair(packet, p_vectors, s_vectors, hessian, actual):
    q3 = A.q_cube(packet)
    targets = tuple(A.target_vector(colour) for colour in A.COLORS)
    formal = [[actual[i][j] for j in A.COLORS] for i in A.COLORS]
    formal[0][0] = add_vectors(formal[0][0], targets[0])
    formal[1][1] = add_vectors(formal[1][1], targets[1])

    # The repaired object has all nine exact coarse equations with the same
    # direct block and q^[3].
    for i, j in product(A.COLORS, repeat=2):
        lhs = add_vectors(formal[i][j],
                          tuple(packet.de(i, j) * value for value in q3))
        want = targets[i] if i == j else (Q(0),) * len(A.WORDS)
        require(lhs == want,
                "the formal repair does not satisfy an exact full-nine row")

    # It also passes the exact labelled quotient-slice criterion of 81bbb0f.
    slices = []
    for colour in A.COLORS:
        functional, _ = N.functional_for_pure_target(q3, colour)
        slices.append([[A.pairing(functional, formal[i][j])
                        for j in A.COLORS] for i in A.COLORS])
    slices = tuple(slices)
    require(slices == N.canonical_slices(),
            "the formal repair is not exactly labelled GHZ in the quotient")
    quotient_verdict = N.criterion(slices)
    require(quotient_verdict["passes"],
            "the formal repair failed the quotient rank criterion")

    residuals = []
    for i, j in product(A.COLORS, repeat=2):
        for word_index, word in enumerate(A.WORDS):
            reconstructed = reconstruct_coordinate(
                p_vectors[i], s_vectors[j], word, hessian)
            difference = formal[i][j][word_index] - reconstructed
            if difference:
                residuals.append((i, j, word, difference))
    expected = [(0, 0, (0,) * 6, Q(1)),
                (1, 1, (1,) * 6, Q(1))]
    require(residuals == expected,
            "the formal repair's common-q residual ledger changed: %s"
            % (residuals,))

    first_word = (0,) * 6
    first_terms = []
    for edge in PAIRS:
        response = response_edge(p_vectors[0], s_vectors[0], first_word, edge)
        cofactor = hessian[hessian_key(edge, first_word)]
        if response or cofactor:
            first_terms.append((edge, response, cofactor, response * cofactor))
    require(first_terms == [((0, 1), Q(23), Q(0), Q(0))],
            "the first scalar Hessian obstruction changed")
    first_index = A.WORDS.index(first_word)
    require(formal[0][0][first_index] == 1
            and actual[0][0][first_index] == 0,
            "the normalized formal/physical first coordinate is not 1 vs 0")
    return {
        "formal_full_nine_rows": 9 * 3 ** 6,
        "quotient_slices": tuple(tuple(tuple(row) for row in matrix)
                                 for matrix in slices),
        "quotient_criterion": quotient_verdict,
        "common_q_residuals": tuple(residuals),
        "first_failing_identity": {
            "row": (0, 0),
            "word": first_word,
            "formal_left_side": formal[0][0][first_index],
            "source_terms": tuple(first_terms),
            "physical_right_side": actual[0][0][first_index],
            "equation": "1 = 23*H_(01,0^4) = 23*0",
        },
    }


def build_ledger():
    blocks = A.D.build_stage_a(A.D.STAGE_A_BASE)
    packet = A.as_chart_packet(blocks)
    p_vectors = tuple(A.star_vector(packet, "P", colour)
                      for colour in A.COLORS)
    s_vectors = tuple(A.star_vector(packet, "S", colour)
                      for colour in A.COLORS)
    hessian, actual, common = audit_common_q(packet, p_vectors, s_vectors)
    repaired = audit_formal_ghz_repair(
        packet, p_vectors, s_vectors, hessian, actual)
    return {
        "theorem": (
            "a source-labelled common-q lift factors every word slice through "
            "the shared deleted-word Hessian H=q^[2]; this is independent of "
            "the involution and labelled GHZ quotient-rank equations"
        ),
        "pins": PINNED,
        "finite_appendage": {
            "q_cube_equations": "729 equations Q_w=haf_w(q)",
            "hessian_equations": (
                "1215 three-term equations H_(xy,barw)=haf_barw(q)"
            ),
            "response_equations": (
                "6561 equations C_ij,w=sum_(xy) "
                "(p_i,x s_j,y+p_i,y s_j,x) H_(xy,barw)"
            ),
            "cross_word_feature": (
                "each H_(xy,barw) is reused by all nine reinsertion letters"
            ),
            "schreyer_feature": (
                "disjoint decorated-edge mixed derivatives of H agree"
            ),
        },
        "literal_guard_common_q": common,
        "formal_exact_ghz_no_lift_guard": repaired,
        "scope": (
            "the no-lift verdict fixes the literal q and physical p_i,s_j; "
            "it does not exclude an unrelated refactorization with new stars "
            "or a different quadratic having the same cubic power"
        ),
    }


def main():
    ledger = build_ledger()
    digest = A.D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "ledger digest changed: got %s" % digest)
    print("PASS: source-labelled common-q Hessian realization gate")
    print("literal guard: 1215 H coordinates, 6561 response equations pass")
    print("formal exact GHZ repair: quotient criterion passes, common-q fails")
    print("smallest failure: [C_00]_(0^6)=1 but 23*H_(01,0^4)=0")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
