#!/usr/bin/env python3
"""Alternating path/cycle response boundary of a dark Hall unary coloop."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_hall_triangle_bridge_dark_coloured_escape.py":
        "6b8392e7329b60f949779a3d9259a7bd7f91428de80a59245f2c12860b11da77",
    "notes/uniform-hall-triangle-bridge-dark-coloured-escape.md":
        "7f510657210143b910e85e87dbedc7098e7b97f5a8278145cb4ba692542694b5",
    "computations/verify_uniform_decorated_anchor_mixed_word_exchange.py":
        "150bf15eb8ac475f866c062afcd7e3002477d02338acdb082c14f9136a3e58b7",
    "notes/uniform-decorated-anchor-mixed-word-exchange.md":
        "0cdc391bebb44150c7941bdbeec853029929f20d46ee813eb2a09bb76c27a5de",
    "computations/verify_uniform_triple_shared_anchor_unary_escape.py":
        "3f754bd020c63a7b03079746b26293e52af6c64d7edd1b7049b70f75ebe45283",
    "notes/uniform-triple-shared-anchor-unary-escape.md":
        "bc5840079555fed469dbc8fcb34ba50b84a8e7dfd35423cfe75b9902e831376e",
}
EXPECTED_LEDGER_SHA256 = "13f4c57cd3f07095db65cde5233bfda870c8be3c6c3ae7da6b5b8d242b366ab9"


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


def alternating_path(first, second, start, finish):
    # Retain the two matching copies of a shared physical edge as distinct
    # tokens; a shared edge is therefore an alternating two-cycle, not a
    # collapsed degree-one component.
    adjacency = {site: [] for matching in (first, second)
                 for pair in matching for site in pair}
    tokens = []
    for colour, matching in enumerate((first, second)):
        for pair in matching:
            token = len(tokens)
            tokens.append((pair, colour))
            left, right = pair
            adjacency[left].append((token, right))
            adjacency[right].append((token, left))
    path = [start]
    used = set()
    current = start
    while current != finish:
        choices = [(token, other) for token, other in adjacency[current]
                   if token not in used]
        require(len(choices) == 1,
                f"the alternating path branched at {current}: {choices}")
        token, other = choices[0]
        used.add(token)
        path.append(other)
        current = other
    return tuple(path), frozenset(used), tuple(tokens)


def union_supports_matching(first, second, vertices):
    support = set(first) | set(second)
    return any(set(matching) <= support
               for matching in perfect_matchings(vertices))


def audit_path_cycle_dichotomy():
    audits = []
    for size in (6, 8):
        b, c, a = 0, 1, 2
        vertices = tuple(range(size))
        unary_matchings = tuple(
            matching for matching in perfect_matchings(vertices)
            if edge(a, b) not in matching
        )
        colour2_matchings = tuple(perfect_matchings(vertices[2:]))
        cycle_case = path_odd = path_even = 0
        for unary in unary_matchings:
            escape = edge(a, partner(unary, a))
            for colour2 in colour2_matchings:
                path, _used, _tokens = alternating_path(
                    unary, colour2, b, c)
                if a not in path:
                    cycle_case += 1
                    # The component containing a is an alternating cycle.
                    # Taking unary edges on that component and colour-two
                    # edges elsewhere is a PM on U-{b,c} containing escape.
                    adjacency = {site: set() for site in vertices}
                    for matching in (unary, colour2):
                        for left, right in matching:
                            adjacency[left].add(right)
                            adjacency[right].add(left)
                    component = set()
                    stack = [a]
                    while stack:
                        site = stack.pop()
                        if site in component:
                            continue
                        component.add(site)
                        stack.extend(adjacency[site] - component)
                    switched = {
                        pair for pair in unary
                        if pair[0] in component
                    } | {
                        pair for pair in colour2
                        if pair[0] not in component and pair[1] not in component
                    }
                    require(escape in switched
                            and len({site for pair in switched for site in pair})
                            == size - 2,
                            "the cycle-switched diagonal matching changed")
                else:
                    position = path.index(a)
                    cross_exists = union_supports_matching(
                        unary, colour2,
                        tuple(site for site in vertices
                              if site not in (a, b)))
                    require(cross_exists == (position % 2 == 1),
                            "the alternating-path crossed parity changed")
                    if position % 2:
                        path_odd += 1
                    else:
                        path_even += 1
        require(cycle_case and path_odd and path_even,
                f"an alternating branch disappeared at size {size}")
        audits.append({
            "residual_sites": size,
            "unary_colour2_pairs": len(unary_matchings)
                                      * len(colour2_matchings),
            "escape_on_cycle": cycle_case,
            "escape_on_path_odd_from_b": path_odd,
            "escape_on_path_even_from_b": path_even,
        })
    return audits


def cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return left, right, left_colour, right_colour


def q_terms(q, vertices, word):
    terms = []
    for matching in perfect_matchings(vertices):
        labels = tuple(cell(left, right, word[left], word[right])
                       for left, right in matching)
        coefficient = 1
        for label in labels:
            coefficient *= q.get(label, 0)
        if coefficient:
            terms.append((coefficient, matching, labels))
    return tuple(terms)


def response_census(q, first_star, second_star):
    first_site, first_colour = first_star
    second_site, second_colour = second_star
    if first_site == second_site:
        return {}
    vertices = tuple(site for site in range(6)
                     if site not in (first_site, second_site))
    output = {}
    for word in itertools.product(range(3), repeat=6):
        if word[first_site] != first_colour \
                or word[second_site] != second_colour:
            continue
        terms = q_terms(q, vertices, word)
        value = sum(term[0] for term in terms)
        if value:
            output[word] = (value, terms)
    return output


def audit_paired_third_colour_web():
    # Dual-blind Hamilton paths:
    # M0=03|14|25, M1=24|35, M2=15|34.
    # The first trapped mates cancel one mixed 11 and one mixed 22 word.
    m0 = (edge(0, 3), edge(1, 4), edge(2, 5))
    m1 = (edge(2, 4), edge(3, 5))
    m2 = (edge(1, 5), edge(3, 4))
    q = {
        cell(0, 3, 0, 0): 1,
        cell(1, 4, 0, 0): 1,
        cell(2, 5, 0, 0): 1,
        cell(2, 4, 1, 1): 1,
        cell(3, 5, 1, 1): 1,
        cell(1, 5, 2, 2): 1,
        cell(3, 4, 2, 2): 1,
        # Trapped mates; each is a third-colour decoration of its selected
        # pure-one or pure-two physical anchor edge.
        cell(2, 4, 0, 2): 1,
        cell(3, 5, 2, 0): -1,
        cell(1, 5, 0, 1): 1,
        cell(3, 4, 1, 0): -1,
    }
    top = {}
    for word in itertools.product(range(3), repeat=6):
        terms = q_terms(q, tuple(range(6)), word)
        value = sum(term[0] for term in terms)
        if value:
            top[word] = (value, terms)
    responses = {
        "11": response_census(q, (0, 1), (1, 1)),
        "12": response_census(q, (0, 1), (0, 2)),
        "21": response_census(q, (2, 2), (1, 1)),
        "22": response_census(q, (2, 2), (0, 2)),
    }
    require(tuple(("".join(map(str, word)), value)
                  for word, (value, _terms) in top.items()) == (
        ("000000", 1), ("000021", 1), ("001011", 1),
        ("020022", 1), ("021012", 1)),
        "the paired-web unary census changed")
    expected_response_debts = {
        "11": (("110100", -1), ("110121", 1), ("111210", -1)),
        "12": (),
        "21": (),
        "22": (("202200", -1), ("202221", 1), ("222102", -1)),
    }
    actual_debts = {}
    for label, census in responses.items():
        pure = (int(label[0]),) * 6 if label[0] == label[1] else None
        actual_debts[label] = tuple(
            ("".join(map(str, word)), value)
            for word, (value, _terms) in census.items() if word != pure
        )
    require(actual_debts == expected_response_debts,
            f"the paired-web response singleton rows changed: {actual_debts}")

    anchors = {pair: 0 for pair in m0}
    anchors.update({pair: 1 for pair in m1})
    anchors.update({pair: 2 for pair in m2})
    decorated_activity = Counter()
    for label in ("11", "22"):
        pure = (int(label[0]),) * 6
        for word, (_value, terms) in responses[label].items():
            if word == pure:
                continue
            require(len(terms) == 1,
                    "a complete paired-web response debt stopped singleton")
            wrong = []
            for q_label in terms[0][2]:
                pair = q_label[:2]
                anchor_colour = anchors[pair]
                endpoint_labels = q_label[2:]
                if endpoint_labels != (anchor_colour, anchor_colour):
                    wrong.append((pair, endpoint_labels, anchor_colour))
            require(len(wrong) == 1,
                    f"a response singleton lost its unique decoration: {wrong}")
            pair, endpoint_labels, anchor_colour = wrong[0]
            require(anchor_colour not in endpoint_labels,
                    "a paired-web decoration stopped being third-colour")
            decorated_activity[(pair, endpoint_labels, anchor_colour)] += 1
    require(len(decorated_activity) == 4,
            "the six rows stopped covering four active decorations")
    return {
        "physical_matchings": {"M0": m0, "M1": m1, "M2": m2},
        "cancelled_first_debts": ["11:110220", "22:202101"],
        "mixed_unary_singletons": [
            ["".join(map(str, word)), value]
            for word, (value, _terms) in top.items() if word != (0,) * 6
        ],
        "response_singletons": {
            label: [list(item) for item in debts]
            for label, debts in actual_debts.items() if debts
        },
        "active_third_colour_decorations": [
            {"edge": list(pair), "labels": list(labels),
             "anchor_colour": colour, "singleton_rows": multiplicity}
            for (pair, labels, colour), multiplicity
            in sorted(decorated_activity.items())
        ],
        "complete_row_consequence": (
            "for each non-pure decoration on a selected pure-k edge, the "
            "full mixed word partitions as q_e*C_e^k+R_e.  Cofactor dark "
            "reselects pure Qk; cofactor non-dark forces an avoiding mixed "
            "matching or a unit.  An off-anchor endpoint escape is free"
        ),
        "sharp_residual": (
            "all avoiding endpoint escapes remain on the anchor union and "
            "carry the two colours different from k, so neither restores "
            "the lost k-column.  A companion row must supply a k-labelled "
            "endpoint or a lock-kernel deletion"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "alternating_path_cycle_audit": audit_path_cycle_dichotomy(),
        "paired_third_colour_web": audit_paired_third_colour_web(),
        "theorem": (
            "for unary M0 and the selected colour-two near-matching M2, "
            "their union is one b-c alternating path plus cycles.  An "
            "escape edge on a cycle gives a mixed diagonal-22 pivot.  On "
            "the path it gives a crossed-21 pivot exactly when a has odd "
            "distance from b.  The even path is the exact first blind case"
        ),
        "complete_mate_reduction": (
            "the minimal dual-blind paired C4 mates do not close: they "
            "create four unary and six diagonal response singleton rows.  "
            "Those six rows make four third-colour anchor decorations "
            "source-active.  Complete mixed-word exchange forces a pure "
            "anchor reselection, an avoiding mixed matching, or a unit; "
            "only anchor-contained wrong-colour escapes remain"
        ),
        "scope": (
            "uniform alternating-component theorem plus one exact critical "
            "web, not a support-layer census and not a full one-bad guard"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall alternating-path ledger changed: {digest}")
    print("uniform Hall bridge-dark alternating-path boundary: PASS")
    print("cycle -> mixed diagonal pivot; odd path -> crossed pivot")
    print("even path -> first blind branch; dual-blind K6 -> paired web")
    print("six response singleton rows -> four active decorations")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
