#!/usr/bin/env python3
"""Source reduction and sharp guard for the Hall-triangle three-term lock.

The non-dark residual is

    B_ab + A_Rc + A_Pc = 0,       B_ab != 0.

At least one anchored correction is nonzero.  Every literal matching term
of A_Rc (respectively A_Pc) contains exactly one internal 10 (respectively
20) cell and a pure-zero tail.  This makes the cell source-active.  An
off-anchor physical pair enters the pinned rank-three active-minor route;
only decorated selected-anchor edges remain.

The checker also constructs a literal common-q six-site packet satisfying
the complete unary tensor, both diagonal target coefficients, the silent
12 row, and the displayed three-term 21 coefficient.  It proves that these
rows alone have no signed-holonomy unit; the other response grades are
load-bearing.
"""

from __future__ import annotations

from collections import Counter
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
    "computations/verify_uniform_anchor_edge_offdiagonal_alternating_exit_dichotomy.py":
        "2de838ff96118a7c54df23c8df02202090a52a3b0ca83f62c400a7a8241f37b8",
    "notes/uniform-anchor-edge-offdiagonal-alternating-exit-dichotomy.md":
        "9b4d2dabf493845de4570008835d544cdb0a9591c5272758e5390f19e70bdc02",
}
EXPECTED_LEDGER_SHA256 = "5fb50e5271c3425353760f8b78b25857354b1a04c7ae0c163cc51ea54e6c8819"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return left, right, left_colour, right_colour


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def q_terms(q, vertices, word):
    position = {site: index for index, site in enumerate(vertices)}
    terms = []
    for matching in perfect_matchings(vertices):
        coefficient = 1
        labels = []
        for left, right in matching:
            label = cell(
                left, right, word[position[left]], word[position[right]])
            coefficient *= q.get(label, 0)
            labels.append(label)
        if coefficient:
            terms.append((coefficient, tuple(labels)))
    return tuple(terms)


def response_terms(q, p_row, s_row, word):
    answer = []
    for (p_site, p_colour), p_value in p_row.items():
        if word[p_site] != p_colour:
            continue
        for (s_site, s_colour), s_value in s_row.items():
            if p_site == s_site or word[s_site] != s_colour:
                continue
            vertices = tuple(site for site in range(len(word))
                             if site not in (p_site, s_site))
            tail_word = tuple(word[site] for site in vertices)
            for q_value, labels in q_terms(q, vertices, tail_word):
                answer.append((p_value * s_value * q_value,
                               (p_site, p_colour), (s_site, s_colour),
                               labels))
    return tuple(answer)


def response_census(q, p_row, s_row):
    nonzero = []
    for word in itertools.product(range(3), repeat=6):
        terms = response_terms(q, p_row, s_row, word)
        value = sum(term[0] for term in terms)
        if value:
            nonzero.append(("".join(map(str, word)), value))
    return tuple(nonzero)


def audit_literal_common_q_guard():
    # Residual c=0,a=1,b=2,d=3,e=4,f=5.  The pure-zero bridge cofactor
    # H0_ab is q04*q35.  The two anchored corrections use q14:10*q35
    # and q24:20*q35, so all three lock terms have one literal common tail.
    q = {
        cell(0, 4, 0, 0): 1,
        cell(1, 2, 0, 0): 1,
        cell(3, 5, 0, 0): 1,
        cell(2, 3, 1, 1): 1,
        cell(4, 5, 1, 1): 1,
        cell(1, 3, 2, 2): 1,
        cell(4, 5, 2, 2): 1,
        cell(1, 4, 1, 0): 1,
        cell(2, 4, 2, 0): 1,
    }
    p1 = {(0, 1): 1}
    s1 = {(1, 1): 1, (0, 0): 1}
    p2 = {(2, 2): 1, (0, 0): -2}
    s2 = {(0, 2): 1}

    top = []
    for word in itertools.product(range(3), repeat=6):
        terms = q_terms(q, tuple(range(6)), word)
        value = sum(term[0] for term in terms)
        if value:
            top.append(("".join(map(str, word)), value, len(terms)))
    require(top == [("000000", 1, 1)],
            f"the lock guard stopped satisfying the unary tensor: {top}")

    census = {
        "11": response_census(q, p1, s1),
        "22": response_census(q, p2, s2),
        "12": response_census(q, p1, s2),
        "21": response_census(q, p2, s1),
    }
    require(census == {
        "11": (("111111", 1), ("111122", 1), ("112000", 1)),
        "22": (("212000", 1), ("222211", 1), ("222222", 1)),
        "12": (),
        "21": (("011111", -2), ("011122", -2),
               ("022211", 1), ("022222", 1)),
    }, f"the literal response guard changed: {census}")

    lock_word = (0, 1, 2, 0, 0, 0)
    lock_terms = response_terms(q, p2, s1, lock_word)
    require(tuple(term[0] for term in lock_terms) == (1, 1, -2),
            f"the three-term lock coefficients changed: {lock_terms}")
    require(sum(term[0] for term in lock_terms) == 0,
            "the physical three-term row stopped vanishing")
    common_tail = cell(3, 5, 0, 0)
    require(all(common_tail in term[3] for term in lock_terms),
            "the three lock terms lost their literal common tail")

    require(response_terms(q, p1, s1, (1,) * 6)[0][0] == 1
            and response_terms(q, p2, s2, (2,) * 6)[0][0] == 1,
            "a diagonal target normalization changed")
    return {
        "unary_nonzero_outputs": top,
        "diagonal_target_values": {"11": 1, "22": 1},
        "silent_12_nonzero_outputs": len(census["12"]),
        "lock_word": "012000",
        "lock_term_coefficients": [term[0] for term in lock_terms],
        "lock_common_tail": "q35_00",
        "remaining_response_debts": {
            key: [[word, value] for word, value in values]
            for key, values in census.items() if key != "12"
            for values in (tuple(item for item in values
                                 if not (key == "11" and item[0] == "111111")
                                 and not (key == "22" and item[0] == "222222")),)
        },
        "character_guard": (
            "the complete unary rows, two target normalizations, silent "
            "12 row, and three-term 21 lock have this rational point; "
            "there is no unit or signed-holonomy contradiction in that "
            "row packet"
        ),
    }


def audit_literal_correction_shape():
    # In A_Rc, holes are b,c and the retained word has exactly a:1.
    # Every matching must pair a with one zero-coloured site d, hence has
    # exactly one q_ad:10 cell.  The dual A_Pc statement is identical.
    vertices = (1, 3, 4, 5)
    word = (1, 0, 0, 0)
    shapes = []
    for matching in perfect_matchings(vertices):
        labels = tuple(cell(left, right, word[vertices.index(left)],
                            word[vertices.index(right)])
                       for left, right in matching)
        mixed = tuple(label for label in labels
                      if label[2:] != (0, 0))
        require(len(mixed) == 1 and mixed[0][2:] in ((1, 0), (0, 1)),
                f"an A_Rc term lost its unique 10 cell: {labels}")
        shapes.append({
            "matching": [list(pair) for pair in matching],
            "unique_mixed_cell": list(mixed[0]),
        })
    require(len(shapes) == 3,
            "the four-site correction matching count changed")
    return {
        "A_Rc_term_shapes": shapes,
        "A_Pc_dual": "replace a:1 by b:2; unique cell is q_be:20",
        "domain_selection": (
            "B!=0 and B+A_Rc+A_Pc=0 make at least one correction "
            "nonzero; a nonzero aggregate has a nonzero literal term"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "literal_correction_shape": audit_literal_correction_shape(),
        "common_q_sharp_guard": audit_literal_common_q_guard(),
        "theorem": (
            "a nonzero Hall-triangle lock selects an active internal 10 or "
            "20 cell.  Off the selected pure-anchor union it enters the "
            "pinned rank-three active-minor route; otherwise it is exactly "
            "a decorated-anchor-edge residual"
        ),
        "anchor_edge_refinement": (
            "with an avoiding pure matching, the pinned alternating-exit "
            "theorem lands unless every active product is trapped on at "
            "most two other-colour anchor neighbours; without such a "
            "matching, rank repair is the named missing input"
        ),
        "signed_holonomy_verdict": (
            "negative for unary + two diagonal target normalizations + "
            "silent 12 + the one three-term 21 row: an exact rational "
            "common-q realization satisfies all of them"
        ),
        "scope": (
            "uniform source-labelled reduction, not closure of the "
            "decorated-anchor residual and not a full one-bad point; the "
            "guard lists its nonzero omitted response coefficients"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall triangle lock ledger changed: {digest}")
    print("uniform Hall-triangle three-term anchor lock reduction: PASS")
    print("B!=0 -> an active literal 10/20 internal correction cell")
    print("off-anchor -> pinned rank-three active-minor route")
    print("signed-holonomy shortcut: refuted by exact common-q row packet")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
