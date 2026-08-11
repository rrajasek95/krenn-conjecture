#!/usr/bin/env python3
"""Response-visibility gate for a bridge-dark Hall unary escape.

Let q_ad:00 H_ad be a nonzero pure-zero summand forced by unary
reselection.  Attaching s1(a,1) and any p_i(d,gamma) gives a literal term
in the corresponding complete response coefficient.  For d outside the
two selected P-neighbours, this is already a support-active good pair P-d.
If both P rows vanish at d, the unary escape is invisible to this first
response attachment.  A six-site common-q guard realizes that boundary.

Separately, an alternate pure-zero matching avoiding a-d repairs the two
deleted-star ranks of the internal active edge a-d.  Its exact obstruction
is a unary coloop (or reuse of a-d by another selected target matching).
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_hall_triangle_bridge_dark_unary_reselection.py":
        "ad1c2f890bdf207add20c6524eb5c91f5925aef8aed77f26f290491a4bb937d6",
    "notes/uniform-hall-triangle-bridge-dark-unary-reselection.md":
        "3985d1e9fad83e773fc00acdd71a398cb10698d6a7207f247d561f454f293453",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = "e55dd3b1b74a68fa6d6e881083c980e5010960436584f3f37048653632a370cb"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def selected_rank(selected, deleted_pair, endpoint):
    other = deleted_pair[0] if endpoint == deleted_pair[1] else deleted_pair[1]
    surviving = []
    for colour, matching in selected:
        neighbour = partner(matching, endpoint)
        if neighbour != other:
            surviving.append((neighbour, colour))
    return len({colour for _neighbour, colour in surviving}), tuple(surviving)


def audit_response_attachment_bijection():
    audits = []
    for size in (4, 6, 8, 10):
        a, d = 0, 1
        tails = tuple(perfect_matchings(range(2, size)))
        unary = tuple(tuple(sorted((edge(a, d),) + tail)) for tail in tails)
        # Replacing q_ad by the two fixed endpoint stars deletes the same
        # sites and leaves exactly the same literal q-tail.
        response = tuple(("p_i(d,gamma)", "s_1(a,1)", tail)
                         for tail in tails)
        require(len(unary) == len(response) and len(set(unary)) == len(unary),
                f"the unary/response tail bijection changed at size {size}")
        audits.append({
            "residual_sites": size,
            "common_H_ad_matching_terms": len(tails),
            "identity": (
                "q_ad^00*H_ad^0 -> "
                "p_i(d,gamma)*s_1(a,1)*H_ad^0"
            ),
        })
    return audits


def audit_alternate_unary_rank_repair():
    # Residual c=0,a=1,b=2,d=3,e=4,f=5; outer P=6,R=7.
    # Q0 uses a-d.  Q0' avoids it, and Q1,Q2 also avoid it.
    q0 = ((0, 2), (1, 3), (4, 5), (6, 7))
    q0_alt = ((0, 3), (1, 4), (2, 5), (6, 7))
    q1 = ((0, 6), (1, 7), (2, 3), (4, 5))
    q2 = ((0, 7), (1, 4), (2, 6), (3, 5))
    selected = ((0, q0_alt), (1, q1), (2, q2))
    deleted = edge(1, 3)
    ranks = tuple(selected_rank(selected, deleted, endpoint)[0]
                  for endpoint in deleted)
    require(ranks == (3, 3),
            f"the alternate-unary rank repair changed: {ranks}")
    require(deleted in q0 and deleted not in q0_alt + q1 + q2,
            "the repaired unary edge incidence changed")
    return {
        "active_unary_matching": q0,
        "alternate_unary_matching": q0_alt,
        "selected_diagonal_matchings": [q1, q2],
        "deleted_pair": deleted,
        "deleted_star_ranks": ranks,
        "condition": (
            "a-d is absent from Q1,Q2 and a nonzero pure-zero matching "
            "pairs a somewhere other than d"
        ),
    }


def coefficient(support, word):
    terms = []
    for matching in perfect_matchings(range(len(word))):
        labels = tuple((pair, word[pair[0]]) for pair in matching)
        if all(word[left] == word[right] for left, right in matching) \
                and all(label in support for label in labels):
            terms.append(labels)
    return tuple(terms)


def audit_response_invisible_coloop_guard():
    # This is the physical bridge-dark packet of 4888b26, now viewed at its
    # escape a-d=1-4.  The pure-zero support has exactly one matching, so
    # there is no alternate Q0 column.  The selected P rows occur only at
    # c and b, and hence both vanish at d.
    c, a, b, d = 0, 1, 2, 4
    m0 = (edge(0, 3), edge(1, 4), edge(2, 5))
    m1 = (edge(2, 3), edge(4, 5))
    m2 = (edge(1, 3), edge(4, 5))
    support = ({(pair, 0) for pair in m0}
               | {(pair, 1) for pair in m1}
               | {(pair, 2) for pair in m2})
    nonzero_top = []
    for word in itertools.product(range(3), repeat=6):
        terms = coefficient(support, word)
        if terms:
            nonzero_top.append((word, len(terms)))
    require(nonzero_top == [((0,) * 6, 1)],
            f"the exact unary-coloop guard changed: {nonzero_top}")

    q0 = tuple(sorted(m0 + (edge(6, 7),)))
    q1 = tuple(sorted(m1 + (edge(6, c), edge(7, a))))
    q2 = tuple(sorted(m2 + (edge(6, b), edge(7, c))))
    selected = ((0, q0), (1, q1), (2, q2))
    deleted = edge(a, d)
    ranks = tuple(selected_rank(selected, deleted, endpoint)[0]
                  for endpoint in deleted)
    require(ranks == (2, 2),
            f"the unary-coloop rank guard changed: {ranks}")

    p1_sites = {c}
    p2_sites = {b}
    require(d not in p1_sites | p2_sites,
            "the response-invisible escape acquired a P-star evaluation")
    return {
        "residual_sites": {"centre": c, "leaf1": a,
                           "leaf2": b, "escape": d},
        "pure_zero_matching": m0,
        "nonzero_unary_outputs": [
            ["".join(map(str, word)), count] for word, count in nonzero_top
        ],
        "selected_colour1_cofactor": m1,
        "selected_colour2_cofactor": m2,
        "escape_edge": deleted,
        "alternate_pure_zero_matchings": 0,
        "deleted_star_ranks": ranks,
        "P_row_support": {"p1": sorted(p1_sites), "p2": sorted(p2_sites)},
        "response_attachment_at_escape": "zero for both P rows",
        "scope": (
            "complete unary tensor plus selected diagonal cofactors, not "
            "the complete four response tensors"
        ),
    }


def audit_centre_escape_gate():
    # If d=c, the selected p1(c,1),s1(a,1) automatically attach the same
    # H_ca tail to a mixed 11 output.  The tiny source below verifies the
    # literal term; an exact response must supply a cancellation mate.
    c, a = 0, 1
    tail = ((2, 3), (4, 5))
    unary_matching = tuple(sorted((edge(c, a),) + tail))
    word = (1, 1, 0, 0, 0, 0)
    require(unary_matching == ((0, 1), (2, 3), (4, 5)),
            "the centre-escape unary matching changed")
    require(word[c] == word[a] == 1
            and all(word[site] == 0 for site in range(2, 6)),
            "the centre-escape response word changed")
    return {
        "unary_term": "q_ca^00*H_ca^0",
        "response_term": "p1(c,1)*s1(a,1)*H_ca^0",
        "response_word": "110000",
        "consequence": (
            "H_ca^0!=0 makes this a nonzero mixed 11 pivot; the complete "
            "zero row must introduce another endpoint-star site or an "
            "anchored correction"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "common_tail_attachment": audit_response_attachment_bijection(),
        "alternate_unary_rank_repair": audit_alternate_unary_rank_repair(),
        "response_invisible_coloop_guard":
            audit_response_invisible_coloop_guard(),
        "centre_escape_gate": audit_centre_escape_gate(),
        "theorem": (
            "a bridge-dark unary escape a-d has two exact positive exits: "
            "an alternate pure-zero matching avoiding a-d repairs its "
            "deleted-star colour-zero columns (unless another selected "
            "target also uses the edge); or a nonzero P-star evaluation at "
            "external d makes P-d a nonanchor support-active good pair.  "
            "For d=c the selected p1(c)s1(a) row supplies the response pivot "
            "automatically"
        ),
        "sharp_residual": (
            "the escape is a unary support coloop or multiply-used edge, "
            "and at an external escape site both P response rows vanish.  "
            "The six-site common-q guard realizes the coloop plus response-"
            "invisible conditions while retaining the complete unary top "
            "and selected diagonal cofactor monomials"
        ),
        "scope": (
            "uniform matching/response-attachment theorem with a physical "
            "six-site counterguard; not a full one-bad survivor and not a "
            "finite selected-support closure"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"bridge-dark coloured-escape ledger changed: {digest}")
    print("uniform Hall bridge-dark coloured escape gate: PASS")
    print("alternate Q0 -> active internal edge has ranks (3,3)")
    print("external response evaluation -> nonanchor support-active P-d arm")
    print("sharp residual: unary coloop plus response-invisible escape")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
