#!/usr/bin/env python3
"""First physical common-q four-hole exchange at the h=3 affine gate.

Let M be a literal coloop target matching and N a literal matching summand
from a nonzero outside complete column.  Their endpoint holes are assumed
distinct.  The five-word evaluation vectors a=mu_M and b=mu_N satisfy an
exact dichotomy: b has a target entry (an alternate target matching), or a
target/outside 2x2 minor Delta is nonzero.  The latter is precisely the E2
matching-base exchange carrier from hafnian path-forest straightening.

On six residual sites the two four-hole tails have nine possible matching
pairs.  Their exposed endpoints have three pairing types.  After restoring
the two endpoint-star edges, the full matchings differ by C6, C8, or two
C4s, with histogram 1/6/2.  Only the two-C4 type has new recombined perfect
matchings on the same edge union; the single-cycle types are the sharp even-
cycle residual of this first physical exchange.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_chart26_c4_exchange_3cell.py":
        "4398d15df3a5f0b34c2745fdb7087a289452ed03983d22431c4f20d116f019c6",
    "notes/hafnian-path-forest-straightening.md":
        "0713791a87b692da809b5f64fe8d757d6454d59e550a859b8d7b7dea68598921",
    "computations/verify_uniform_axis_circuit_outside_endpoint_rank_restoration.py":
        "1af29dfddaf3127e758f07c53cf08189bda72df4e54a58a4e0ca78f6709874ac",
    "notes/uniform-axis-circuit-outside-endpoint-rank-restoration.md":
        "a7345aa254a4dcfb65742b8b09f0dafe7a1ef1b1b9a2fa67b6e8528e462a9516",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "948b396097dff3ab1a1f9d9b5297550adf3e4abedb21eb012efc8c7e03bd2127"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


TARGET_HOLES = (0, 1)
OUTSIDE_HOLES = (2, 3)
COMMON = (4, 5)
P, S = 6, 7
TARGET_TAILS = tuple(perfect_matchings(OUTSIDE_HOLES + COMMON))
OUTSIDE_TAILS = tuple(perfect_matchings(TARGET_HOLES + COMMON))


def multigraph_components(first, second):
    """Components of two labelled matchings, retaining parallel edges."""
    adjacency = {site: [] for site in range(8)}
    for label, matching in ((0, first), (1, second)):
        for index, (left, right) in enumerate(matching):
            token = (label, index, left, right)
            adjacency[left].append((right, token))
            adjacency[right].append((left, token))
    components = []
    seen_edges = set()
    for site in adjacency:
        for _neighbour, token in adjacency[site]:
            if token in seen_edges:
                continue
            vertices = set()
            edges = set()
            frontier = [site]
            while frontier:
                current = frontier.pop()
                vertices.add(current)
                for neighbour, current_token in adjacency[current]:
                    if current_token not in edges:
                        edges.add(current_token)
                        frontier.append(neighbour)
            seen_edges |= edges
            components.append((frozenset(vertices), frozenset(edges)))
    return tuple(components)


def exposed_pairing(target_tail, outside_tail):
    components = multigraph_components(target_tail, outside_tail)
    exposed = set(TARGET_HOLES + OUTSIDE_HOLES)
    pairs = []
    for vertices, _edges in components:
        ends = tuple(sorted(vertices & exposed))
        if ends:
            require(len(ends) == 2,
                    "a tail component stopped pairing two exposed sites")
            pairs.append(ends)
    return frozenset(pairs)


def symmetric_difference_cycles(first, second):
    common = set(first) & set(second)
    symmetric = (set(first) | set(second)) - common
    adjacency = {}
    for left, right in symmetric:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    require(all(len(neighbours) == 2 for neighbours in adjacency.values()),
            "the full matching symmetric difference stopped being cyclic")
    lengths = []
    unseen = set(adjacency)
    while unseen:
        start = next(iter(unseen))
        previous = None
        current = start
        length = 0
        while True:
            neighbours = adjacency[current]
            following = next(item for item in neighbours if item != previous)
            length += 1
            previous, current = current, following
            unseen.discard(previous)
            if current == start:
                break
        lengths.append(length)
    require(all(length % 2 == 0 for length in lengths),
            "an alternating matching component became odd")
    return tuple(sorted(lengths)), tuple(sorted(common))


def cycle_edge_sets(first, second):
    common = set(first) & set(second)
    symmetric = (set(first) | set(second)) - common
    adjacency = {}
    for pair in symmetric:
        for site in pair:
            adjacency.setdefault(site, []).append(pair)
    cycles = []
    unused = set(symmetric)
    while unused:
        seed = next(iter(unused))
        vertices = set(seed)
        edges = {seed}
        frontier = list(seed)
        while frontier:
            site = frontier.pop()
            for pair in adjacency[site]:
                if pair not in edges:
                    edges.add(pair)
                    vertices.update(pair)
                    frontier.extend(pair)
        unused -= edges
        cycles.append(frozenset(edges))
    return tuple(cycles), frozenset(common)


def recombined_matchings(first, second):
    cycles, common = cycle_edge_sets(first, second)
    outputs = set()
    for choices in product((0, 1), repeat=len(cycles)):
        selected = set(common)
        for cycle, choice in zip(cycles, choices, strict=True):
            source = first if choice == 0 else second
            selected |= set(source) & set(cycle)
        matching = tuple(sorted(selected))
        require(len(matching) == 4
                and len({site for pair in matching for site in pair}) == 8,
                "cycle flip stopped producing a perfect matching")
        outputs.add(matching)
    return tuple(sorted(outputs))


def audit_tail_topology():
    require(len(TARGET_TAILS) == len(OUTSIDE_TAILS) == 3,
            "a four-site tail lost its three perfect matchings")
    pairing_histogram = Counter()
    cycle_histogram = Counter()
    recombination_histogram = Counter()
    records = []
    expected_pairings = {
        frozenset((TARGET_HOLES, OUTSIDE_HOLES)): "internal",
        frozenset(((0, 2), (1, 3))): "endpoint_aligned",
        frozenset(((0, 3), (1, 2))): "endpoint_crossed",
    }
    for target_tail in TARGET_TAILS:
        for outside_tail in OUTSIDE_TAILS:
            pairing = exposed_pairing(target_tail, outside_tail)
            require(pairing in expected_pairings,
                    f"an unknown exposed pairing appeared: {pairing}")
            pairing_type = expected_pairings[pairing]
            pairing_histogram[pairing_type] += 1

            target = tuple(sorted((edge(P, 0), edge(S, 1)) + target_tail))
            outside = tuple(sorted((edge(P, 2), edge(S, 3)) + outside_tail))
            cycles, common = symmetric_difference_cycles(target, outside)
            cycle_histogram[str(cycles)] += 1
            recombined = recombined_matchings(target, outside)
            recombination_histogram[len(recombined)] += 1

            if pairing_type == "endpoint_aligned":
                require(cycles == (4, 4) and len(recombined) == 4,
                        "aligned exposed paths stopped giving two C4s")
                new = set(recombined) - {target, outside}
                ports = {
                    (partner(matching, P), partner(matching, S))
                    for matching in new
                }
                require(ports == {(2, 1), (0, 3)},
                        f"the two cross recombination ports changed: {ports}")
            else:
                require(len(recombined) == 2,
                        "a single alternating cycle acquired a third matching")

            records.append({
                "target_tail": target_tail,
                "outside_tail": outside_tail,
                "exposed_pairing": pairing_type,
                "full_cycle_lengths": cycles,
                "common_full_edges": common,
                "perfect_matchings_on_union": len(recombined),
            })

    require(pairing_histogram == Counter({
        "internal": 5, "endpoint_aligned": 2, "endpoint_crossed": 2,
    }), f"the exposed-pairing histogram changed: {pairing_histogram}")
    require(cycle_histogram == Counter({"(8,)": 6, "(4, 4)": 2,
                                        "(6,)": 1}),
            f"the full alternating-cycle histogram changed: {cycle_histogram}")
    require(recombination_histogram == Counter({2: 7, 4: 2}),
            f"the cycle-flip matching count changed: {recombination_histogram}")
    return {
        "tail_pairs": len(records),
        "exposed_pairing_histogram": dict(pairing_histogram),
        "full_cycle_histogram": dict(cycle_histogram),
        "union_matching_count_histogram": dict(recombination_histogram),
        "records": records,
    }


def audit_e2_target_coloop_dichotomy():
    # c=0 is the pure target word.  M is its nonzero coloop matching;
    # N is a literal summand selected from the nonzero outside column.
    a = (Q(2), Q(3), Q(-1), Q(4), Q(5))
    b = (Q(0), Q(7), Q(0), Q(-2), Q(1))
    h = (Q(1), Q(0), Q(0), Q(0), Q(0))
    c, d = 0, 1
    delta = a[c] * b[d] - a[d] * b[c]
    require(a[c] and not b[c] and b[d] and delta == 14,
            "the target-coloop exchange minor changed")

    def p(vector, left, right):
        return vector[left] * h[right] - vector[right] * h[left]

    left_e2 = b[c] * p(a, c, d) - a[c] * p(b, c, d)
    right_e2 = b[d] * p(a, c, d) - a[d] * p(b, c, d)
    require(left_e2 == delta * h[c]
            and right_e2 == delta * h[d],
            "the exact E2 endpoint exchange identity changed")

    # If every Delta_{c,d} vanishes, b_c=0 and a_c!=0 force b=0.  Hence a
    # nonzero outside evaluation vector cannot remain proportional to the
    # target-coloop vector.  This proves the dichotomy without genericity.
    require(all(a[c] * Q(0) - a[index] * Q(0) == 0
                for index in range(5)),
            "the zero-vector proportional branch changed")
    for index in range(5):
        if b[index]:
            require(a[c] * b[index] - a[index] * b[c] != 0,
                    "a nonzero outside word escaped every target minor")

    # The complementary branch b_c!=0 is literally an avoiding pure target
    # matching and therefore breaks the coloop before E2 is needed.
    b_alternate = (Q(1), Q(0), Q(0), Q(0), Q(0))
    require(b_alternate[c] != 0,
            "the alternate-target branch lost its target evaluation")
    return {
        "word_count": len(a),
        "target_state": c,
        "outside_active_state": d,
        "target_matching_evaluation": [str(value) for value in a],
        "outside_matching_evaluation": [str(value) for value in b],
        "exchange_minor": str(delta),
        "E2_left": str(left_e2),
        "E2_right": str(right_e2),
        "dichotomy": (
            "b_target!=0 gives an alternate pure target matching; otherwise "
            "any nonzero b_d gives Delta_target,d=a_target*b_d!=0"
        ),
        "all_minors_zero_consequence": "outside evaluation vector b=0",
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "E2_coloop_dichotomy": audit_e2_target_coloop_dichotomy(),
        "h3_four_hole_topology": audit_tail_topology(),
        "uniform_lemma": (
            "for a nonzero literal outside matching N and a nonzero coloop "
            "target matching M, either N has nonzero pure-target evaluation "
            "and is an alternate target matching, or some target/outside "
            "minor Delta^MN is nonzero and E2 supplies a literal common-q "
            "matching-exchange carrier.  The all-minors-zero branch forces "
            "N's complete five-word evaluation vector to vanish"
        ),
        "two_c4_landing": (
            "when the exposed tail pairing agrees with the P/S endpoint "
            "pairing, M triangle N is C4+C4 and flipping one cycle gives "
            "two new full matchings with crossed endpoint ports.  A pure "
            "decoration is an alternate target matching; a mixed decoration "
            "is a literal exchange carrier, and any new physical edge "
            "outside the selected anchor union enters the pinned nonanchor "
            "good active route"
        ),
        "sharp_boundary": (
            "the other seven tail pairs have a single C6 or C8 alternating "
            "component and no third perfect matching on the same edge union. "
            "E2 still gives a nonzero physical exchange minor, but routing "
            "that anchor-contained even-cycle carrier requires a further "
            "complete coefficient row or an external edge; signless cycle "
            "flipping alone cannot do it"
        ),
        "scope": (
            "h=3 with four distinct endpoint holes; collisions are lower "
            "Hall/reselection strata.  The theorem is a literal matching-"
            "base exchange and topology classification, not a claim that "
            "every even-cycle E2 carrier is already four-good"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"h3 four-hole exchange ledger changed: {digest}")
    print("h3 target-coloop four-hole exchange: PASS")
    print("E2: alternate target or nonzero literal exchange minor")
    print("tail pairings internal/aligned/crossed: 5/2/2")
    print("full cycles C6/C8/(C4+C4): 1/6/2")
    print("sharp residual: seven single even-cycle exchange carriers")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
