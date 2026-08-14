#!/usr/bin/env python3
"""Audit the active-fan Cartan prism on the literal omit-coloop packet.

Put the pure-colour coloop at 01 and the response endpoint edge at 67.
For every matching which omits both edges, the complete-row pivot has the
weighted pure/mixed terms alpha*U and d*V.  The signed Weyl action at 0,1
sends alpha*U to d*V term by term, while the physical endpoint
transposition 6<->7 exchanges the two orientations.  Consequently

    (1-s)(w-1)(alpha U_+) = -D,

where D=alpha(U_+-U_-)-d(V_+-V_-), with no coefficient, matching, word,
fine, or remote-tail remainder.

This does not yet produce the complete protected Phi.  The ordinary
four-corner residue transports, but the two halves of the Kähler ridge have
different site degrees.  A common tail preserves that difference; for a
nonconstant tail, -d(T Omega)=T(-dOmega)-Omega*dT also has a literal extra
face.  Those are operation/readout faces in the same Hall shore, not
support holes already forced to a typed exit.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
    "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py":
        "d71b2ae71cdfc910e374b498a70edbb5e897867cf624dec49203c34e74647925",
    "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py":
        "6f791c41e743a94279ccf9e4924af11a42c278baa7737a5eed108bf85136f499",
}
EXPECTED_LEDGER_SHA256 = (
    "5061ab738d5bdacf416f8a3453e7cc6557fc3c91e4d3397abd74b144a6cc5a25"
)

ROOT_SITES = (0, 1)
ENDPOINT_SITES = (6, 7)
COLOOP_EDGE = ROOT_SITES
ENDPOINT_EDGE = ENDPOINT_SITES
ACTION_SITES = frozenset(ROOT_SITES + ENDPOINT_SITES)
PURE_COLOUR = 1
COLOOP_COLOUR = 0


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def decorated(matching, word):
    return tuple((left, right, word[left], word[right])
                 for left, right in matching)


def augmented_term(weight_colour: int, matching, word):
    """The coefficient cell on 01 followed by the omit-01 matching term."""
    weight = (0, 1, weight_colour, weight_colour)
    return tuple(sorted((weight,) + decorated(matching, word)))


def signed_weyl_colour(colour: int) -> tuple[int, int]:
    # 0 -> -1, 1 -> 0.  Colour 2 is a spectator in this packet.
    if colour == 0:
        return 1, -1
    if colour == 1:
        return 0, 1
    return colour, 1


def signed_weyl_term(term):
    answer = []
    sign = 1
    for left, right, left_colour, right_colour in term:
        if left in ROOT_SITES:
            left_colour, local_sign = signed_weyl_colour(left_colour)
            sign *= local_sign
        if right in ROOT_SITES:
            right_colour, local_sign = signed_weyl_colour(right_colour)
            sign *= local_sign
        answer.append((left, right, left_colour, right_colour))
    return tuple(sorted(answer)), sign


def swap_endpoint_site(site: int) -> int:
    if site == ENDPOINT_SITES[0]:
        return ENDPOINT_SITES[1]
    if site == ENDPOINT_SITES[1]:
        return ENDPOINT_SITES[0]
    return site


def endpoint_swap_term(term):
    answer = []
    for left, right, left_colour, right_colour in term:
        new_left = swap_endpoint_site(left)
        new_right = swap_endpoint_site(right)
        if new_left < new_right:
            answer.append((new_left, new_right, left_colour, right_colour))
        else:
            answer.append((new_right, new_left, right_colour, left_colour))
    return tuple(sorted(answer))


def add_counter(*pieces):
    answer = Counter()
    for coefficient, term in pieces:
        answer[term] += coefficient
    return Counter({term: value for term, value in answer.items() if value})


def site_degree(term):
    degree = [0] * 8
    for left, right, _a, _b in term:
        degree[left] += 1
        degree[right] += 1
    return tuple(degree)


def audit_termwise_boundary() -> dict[str, object]:
    all_matchings = tuple(perfect_matchings(tuple(range(8))))
    sector = tuple(matching for matching in all_matchings
                   if COLOOP_EDGE not in matching
                   and ENDPOINT_EDGE not in matching)
    require(len(all_matchings) == 105 and len(sector) == 78,
            (len(all_matchings), len(sector)))

    pure_word = (PURE_COLOUR,) * 8
    mixed_word = (COLOOP_COLOUR, COLOOP_COLOUR) + (PURE_COLOUR,) * 6
    visited = set()
    orbit_records = []
    tail_histogram = Counter()
    matching_term_checks = 0

    for matching in sector:
        u_plus = augmented_term(COLOOP_COLOUR, matching, pure_word)
        v_plus = augmented_term(PURE_COLOUR, matching, mixed_word)
        transported, weyl_sign = signed_weyl_term(u_plus)
        require(weyl_sign == 1 and transported == v_plus,
                ("w(alpha U) != d V", matching, weyl_sign))
        matching_term_checks += 1

        swapped = tuple(cell[:2] for cell in endpoint_swap_term(
            decorated(matching, pure_word)))
        swapped = tuple(sorted(swapped))
        require(swapped in sector and swapped != matching,
                ("endpoint orbit left the sector", matching, swapped))
        if matching in visited:
            continue
        visited.update((matching, swapped))

        u_minus = endpoint_swap_term(u_plus)
        v_minus = endpoint_swap_term(v_plus)

        # Boundary convention: (1-s)(w-1) on alpha*U_plus.
        boundary = add_counter(
            (1, v_plus), (-1, u_plus), (-1, v_minus), (1, u_minus))
        desired_negative = add_counter(
            (-1, u_plus), (1, u_minus), (1, v_plus), (-1, v_minus))
        require(boundary == desired_negative and len(boundary) == 4,
                ("the literal boundary is not -D", matching, boundary))

        tail = tuple(pair for pair in matching
                     if set(pair).isdisjoint(ACTION_SITES))
        swapped_tail = tuple(pair for pair in swapped
                             if set(pair).isdisjoint(ACTION_SITES))
        require(tail == swapped_tail,
                ("endpoint swap changed the remote tail", matching, tail,
                 swapped_tail))
        tail_histogram[len(tail)] += 1

        expected_degree = (2, 2, 1, 1, 1, 1, 1, 1)
        require(all(site_degree(term) == expected_degree for term in
                    (u_plus, u_minus, v_plus, v_minus)),
                ("the four corners left the repeated grade", matching))
        orbit_records.append({
            "representative": [list(pair) for pair in matching],
            "remote_tail": [list(pair) for pair in tail],
            "boundary_terms": 4,
        })

    require(len(visited) == 78 and len(orbit_records) == 39
            and tail_histogram == Counter({0: 12, 1: 24, 2: 3}),
            (len(visited), len(orbit_records), tail_histogram))
    return {
        "complete_matchings": len(all_matchings),
        "omit_coloop_and_endpoint_edge_terms": len(sector),
        "endpoint_orbits": len(orbit_records),
        "weighted_Weyl_term_checks": matching_term_checks,
        "orbit_remote_tail_edge_histogram": dict(sorted(
            tail_histogram.items())),
        "four_corner_repeated_site_degree": [2, 2, 1, 1, 1, 1, 1, 1],
        "literal_identity": (
            "(1-s_67)(w_01-1)(alpha*U_+)="
            "d(V_+-V_-)-alpha(U_+-U_-)=-D"
        ),
        "matching_word_fine_remote_tail_remainder": 0,
    }


def monomial_differential_faces(tail):
    # Formal exterior derivative of the squarefree remote-tail monomial.
    # Differential labels retain the differentiated edge, hence the faces
    # are distinct and cannot cancel.
    return Counter({(differentiated,
                     tuple(pair for pair in tail
                           if pair != differentiated)): 1
                    for differentiated in tail})


def add_degree(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def audit_protected_readout_gate() -> dict[str, object]:
    sector = tuple(matching for matching in
                   perfect_matchings(tuple(range(8)))
                   if COLOOP_EDGE not in matching
                   and ENDPOINT_EDGE not in matching)
    representatives = []
    visited = set()
    for matching in sector:
        if matching in visited:
            continue
        swapped = tuple(sorted(edge(swap_endpoint_site(left),
                                    swap_endpoint_site(right))
                               for left, right in matching))
        visited.update((matching, swapped))
        representatives.append(matching)

    nonconstant = 0
    kahler_extra_faces = 0
    for matching in representatives:
        tail = tuple(pair for pair in matching
                     if set(pair).isdisjoint(ACTION_SITES))
        differential = monomial_differential_faces(tail)
        require(len(differential) == len(tail)
                and all(value == 1 for value in differential.values()),
                ("the literal dT faces changed", tail, differential))
        if tail:
            nonconstant += 1
            kahler_extra_faces += len(differential)
    require(nonconstant == 27 and kahler_extra_faces == 30,
            (nonconstant, kahler_extra_faces))

    # The two halves of -dOmega occupy the endpoint and root pairs.  A
    # common tail adds the same multidegree and cannot identify them.
    endpoint_degree = (0, 0, 0, 0, 0, 0, 1, 1)
    root_degree = (1, 1, 0, 0, 0, 0, 0, 0)
    degree_checks = 0
    for matching in representatives:
        tail_degree = [0] * 8
        for left, right in matching:
            if {left, right}.isdisjoint(ACTION_SITES):
                tail_degree[left] += 1
                tail_degree[right] += 1
        require(add_degree(endpoint_degree, tail_degree)
                != add_degree(root_degree, tail_degree),
                ("a common tail repaired the ridge grade", matching))
        degree_checks += 1
    require(degree_checks == 39,
            "the ridge-degree orbit census changed")

    # Ordinary residue is endpoint/root covariant, but fixed terminal
    # contractions are multiplied by T.  For a nonconstant monomial T this
    # is not the normalized scalar 1 in the polynomial source ring.
    return {
        "ordinary_four_corner_residue": "T*(-1,+1,+1,-1)",
        "endpoint_even_D_W_target_anchor_Eq_readouts": 0,
        "endpoint_orbits_with_nonconstant_remote_tail": nonconstant,
        "literal_extra_Omega_dT_faces": kahler_extra_faces,
        "ridge_degree_checks": degree_checks,
        "ridge_degree_endpoint_half": list(endpoint_degree),
        "ridge_degree_root_half": list(root_degree),
        "common_tail_repairs_ridge_degree": False,
        "product_rule": "-d(T*Omega)=T*(-dOmega)-Omega*dT",
        "fixed_eta_sigma_normalization": (
            "scaled by T unless T=1 in the terminal quotient"
        ),
        "first_mismatch": (
            "not word/fine/matching: the labelled Kähler ridge/readout; "
            "its two halves have different site degree, and nonconstant "
            "tails add the same-shore Omega*dT operation faces"
        ),
        "typed_exit_status": (
            "not forced: these are operation/Kähler faces in the selected "
            "packet, not outside-Hall-shore matching holes"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": (
            "h3 active-fan omit-coloop Cartan termwise restriction and "
            "protected-readout gate"
        ),
        "pins": PINS,
        "termwise_boundary": audit_termwise_boundary(),
        "protected_readout": audit_protected_readout_gate(),
        "verdict": (
            "The physical Cartan prism gives the desired odd weighted U/V "
            "boundary exactly, term by term, on all 78 literal omit-coloop "
            "response occurrences.  Thus there is no matching, word, fine, "
            "orientation, coefficient, or ordinary-residue mismatch.  This "
            "does not by itself give the protected Phi: the common-tail "
            "extension does not supply the labelled shifted Kähler ridge, "
            "and its extra operation faces are not forced outside the shore."
        ),
        "shortest_positive_addition": (
            "a source-labelled shifted lift keeping the endpoint and root "
            "halves of -dOmega separate and transporting eta/sigma with the "
            "Cartan labels; after that lift the existing q quotient theorem "
            "can classify disagreement as correction or typed witness"
        ),
        "scope": (
            "exact h=3 01-coloop/67-response direct-free packet and all 78 "
            "matching occurrences; not an all-h lift and not a full GHZ "
            "source counterexample"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("omit-coloop Cartan weighted U/V boundary: EXACT TERM BY TERM")
    print("matching/word/fine/orientation/ordinary residue mismatch: NONE")
    print("protected Phi: OPEN AT LABELLED KAHLER RIDGE/READOUT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
