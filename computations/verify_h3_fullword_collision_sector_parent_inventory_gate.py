#!/usr/bin/env python3
"""Exhaust the physical 3^8 rows in one parent-labelled collision sector.

The chosen operation sector is the E01 sector on augmented vertices

    (P,S,0,1,2,3,4,5),       missing 0 / doubled S,

in response word 11:110000.  A physical coefficient monomial is a perfect
matching and therefore has squarefree operation degree.  A collision
monomial has operation degree (1,2,0,1,1,1,1,1).  The two spaces are
disjoint before any linear algebra.

The exhaustive word sweep below nevertheless materializes every decorated
coefficient monomial in all 3^8 complete 105-term rows (and counts the
direct-free 90-term subinventory).  It then resolves the 45 collision
monomials into their 90 operation-parent occurrences.  The incomplete root

    Xi_01 = a_PS d/da_P0 - a_S1 d/da_01

has 30 signed parent occurrences.  Collection cancels two occurrences over
each of three monomials, leaving the known 24-term residual.  The physical
inventory projects to zero, the parent-even collision row has rank one, and
the residual raises the rank to two.  Exact normalized duals are Xi/30 in
the parent lift and R/24 after collection.

Thus the first possible rank-raising family is not another output word.  It
is an occurrence-labelled first Spencer/root family realizing Xi_01(H_w),
with all 120 labelled first-PP faces (60 3K2 and 60 P3+K2) and their
restriction/reinsertion data.  This checker identifies that missing family;
it does not assert that such a source cell exists.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py":
        "c0c6c075388a2eb2d5dad6d133166a3f211dd268183d3e2a5433d922e2ea8ceb",
    "computations/verify_h3_collision_parent_split_relative_bar_terminal_gate.py":
        "918e89d2298b2def33fd77ad0edac7c3b1f61c52d6000a0b6cc31b6ea58a45ae",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
EXPECTED_LEDGER_SHA256 = (
    "bfafda8698a3e58346212a8287729574ddaccdd9ce668d299479c28ba2f6b385"
)


NAMES = ("P", "S", "0", "1", "2", "3", "4", "5")
P, S, ZERO, ONE, TWO, THREE, FOUR, FIVE = range(8)
VERTICES = tuple(range(8))
COLOURS = (0, 1, 2)
FIXED_WORD = (1, 1, 1, 1, 0, 0, 0, 0)
FIXED_WORD_LABEL = "11:110000"
DIRECT_FREE_PAIR = frozenset((6, 3))


Edge = tuple[int, int]
Matching = tuple[Edge, ...]
DecoratedEdge = tuple[int, int, int, int]
DecoratedMonomial = tuple[DecoratedEdge, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def decorated_edge(left: int, right: int,
                   left_colour: int, right_colour: int) -> DecoratedEdge:
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS = tuple(perfect_matchings(VERTICES))
DIRECT_FREE_MATCHINGS = tuple(
    matching for matching in MATCHINGS
    if all(frozenset(item) != DIRECT_FREE_PAIR for item in matching)
)


def decorate_matching(matching: Matching,
                      word: tuple[int, ...]) -> DecoratedMonomial:
    return tuple(sorted(decorated_edge(left, right, word[left], word[right])
                        for left, right in matching))


def operation_degree(matching: Matching) -> tuple[int, ...]:
    answer = [0] * 8
    for left, right in matching:
        answer[left] += 1
        answer[right] += 1
    return tuple(answer)


def decorated_operation_degree(monomial: DecoratedMonomial) -> tuple[int, ...]:
    return operation_degree(tuple((item[0], item[1]) for item in monomial))


def fine_degree(monomial: DecoratedMonomial) -> tuple[int, ...]:
    answer = [0] * 24
    for left, right, left_colour, right_colour in monomial:
        answer[3 * left + left_colour] += 1
        answer[3 * right + right_colour] += 1
    return tuple(answer)


def collision_skeletons() -> tuple[Matching, ...]:
    available = tuple(vertex for vertex in VERTICES
                      if vertex not in (ZERO, S))
    answer = []
    for left, right in combinations(available, 2):
        rest = tuple(vertex for vertex in available
                     if vertex not in (left, right))
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted(
                (edge(S, left), edge(S, right)) + tail
            )))
    require(len(answer) == len(set(answer)) == 45,
            "collision sector stopped having 45 skeletons")
    expected_degree = (1, 2, 0, 1, 1, 1, 1, 1)
    require({operation_degree(value) for value in answer} == {expected_degree},
            "collision operation degree changed")
    return tuple(sorted(answer))


COLLISIONS = collision_skeletons()


def repair_occurrence(collision: Matching, target_edge: Edge,
                      word: tuple[int, ...]):
    """Reverse one doubled-S edge to 0, decorate its parent, then push it."""
    require(S in target_edge and target_edge in collision,
            ("not a doubled-S occurrence", collision, target_edge))
    neighbour = target_edge[0] if target_edge[1] == S else target_edge[1]
    source_edge = edge(ZERO, neighbour)
    parent = tuple(sorted(tuple(item for item in collision
                                if item != target_edge) + (source_edge,)))
    require(operation_degree(parent) == (1,) * 8,
            ("repair is not a perfect matching", collision, target_edge))

    cells = []
    for item in parent:
        if item != source_edge:
            left, right = item
            cells.append(decorated_edge(left, right, word[left], word[right]))
            continue
        # The colour attached to the missing 0 occurrence travels to the
        # newly created S occurrence.  This is the operation-parent label
        # which ordinary collection forgets.
        cells.append(decorated_edge(
            S, neighbour, word[ZERO], word[neighbour]
        ))
    target_monomial = tuple(sorted(cells))
    require(decorated_operation_degree(target_monomial)
            == (1, 2, 0, 1, 1, 1, 1, 1),
            "transport left the collision sector")
    return parent, source_edge, target_edge, target_monomial


def all_occurrences():
    answer = []
    for collision in COLLISIONS:
        incident = tuple(item for item in collision if S in item)
        require(len(incident) == 2, "collision lost its two repairs")
        for target_edge in incident:
            answer.append(repair_occurrence(collision, target_edge, FIXED_WORD))
    require(len(answer) == len(set(answer)) == 90,
            "parent-labelled sector stopped having 90 occurrences")
    return tuple(sorted(answer))


OCCURRENCES = all_occurrences()


def root_weight(source_edge: Edge) -> Q:
    if source_edge == edge(P, ZERO):
        return Q(1)
    if source_edge == edge(ZERO, ONE):
        return Q(-1)
    return Q(0)


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def topology_after_removal(monomial: DecoratedMonomial,
                           removed_index: int) -> str:
    remainder = monomial[:removed_index] + monomial[removed_index + 1:]
    positive = tuple(sorted((value for value in
                             decorated_operation_degree(remainder) if value),
                            reverse=True))
    lookup = {
        (1, 1, 1, 1, 1, 1): "3K2",
        (2, 1, 1, 1, 1): "P3+K2",
    }
    require(positive in lookup, ("unknown PP topology", positive, monomial))
    return lookup[positive]


def exhaustive_physical_inventory(collision_fine: tuple[int, ...]):
    content = sha256()
    words = 0
    complete_terms = 0
    direct_free_terms = 0
    same_word_complete_terms = 0
    same_word_direct_free_terms = 0
    same_word_fine_repeated_hits = 0
    projected_nonzero_rows = 0
    pure_target_rows = 0
    mixed_zero_target_rows = 0
    direct_free_set = set(DIRECT_FREE_MATCHINGS)
    squarefree_degree = (1,) * 8

    for word in product(COLOURS, repeat=8):
        words += 1
        target = int(len(set(word)) == 1)
        pure_target_rows += target
        mixed_zero_target_rows += 1 - target
        row_hits = 0
        row_terms = []
        for matching in MATCHINGS:
            monomial = decorate_matching(matching, word)
            row_terms.append(monomial)
            complete_terms += 1
            require(operation_degree(matching) == squarefree_degree,
                    "a physical matching stopped being squarefree")
            if matching in direct_free_set:
                direct_free_terms += 1
            if word == FIXED_WORD:
                same_word_complete_terms += 1
                if matching in direct_free_set:
                    same_word_direct_free_terms += 1
                if (fine_degree(monomial) == collision_fine
                        and operation_degree(matching)
                        == (1, 2, 0, 1, 1, 1, 1, 1)):
                    row_hits += 1
                    same_word_fine_repeated_hits += 1
        require(len(row_terms) == len(set(row_terms)) == 105,
                ("physical row term collision", word))
        if row_hits:
            projected_nonzero_rows += 1
        content.update(bytes(word))
        for monomial in row_terms:
            content.update(repr(monomial).encode("ascii"))
        content.update(b"|")

    require(words == 3 ** 8 == 6561, "word census changed")
    require(complete_terms == 6561 * 105 == 688905,
            "complete coefficient census changed")
    require(direct_free_terms == 6561 * 90 == 590490,
            "direct-free coefficient census changed")
    require((same_word_complete_terms, same_word_direct_free_terms)
            == (105, 90), "fixed-word census changed")
    require(not same_word_fine_repeated_hits and not projected_nonzero_rows,
            "a squarefree physical row entered the collision sector")
    require((pure_target_rows, mixed_zero_target_rows) == (3, 6558),
            "pure/mixed target census changed")
    require(not len(set(FIXED_WORD)) == 1,
            "the fixed collision word became a pure target word")
    return {
        "words": words,
        "complete_105_terms": complete_terms,
        "direct_free_90_terms": direct_free_terms,
        "fixed_word_complete_direct_free_terms": [
            same_word_complete_terms, same_word_direct_free_terms
        ],
        "fixed_word_fine_repeated_hits": same_word_fine_repeated_hits,
        "projected_nonzero_rows": projected_nonzero_rows,
        "pure_target_rows": pure_target_rows,
        "mixed_zero_target_rows": mixed_zero_target_rows,
        "fixed_word_target": 0,
        "inventory_content_sha256": content.hexdigest(),
    }


def parent_and_collection_audit():
    collision_monomials = tuple(sorted({item[3] for item in OCCURRENCES}))
    require(len(collision_monomials) == 45,
            "repeated grade stopped collecting 90 parents to 45 terms")
    collision_fines = {fine_degree(value) for value in collision_monomials}
    require(len(collision_fines) == 1,
            "fixed repeated collision packet split into several fine grades")
    collision_fine = next(iter(collision_fines))

    parent_even = tuple(Q(1) for _item in OCCURRENCES)
    parent_root = tuple(root_weight(item[1]) for item in OCCURRENCES)
    root_counts = Counter(parent_root)
    require(root_counts == Counter({Q(0): 60, Q(1): 15, Q(-1): 15}),
            ("parent root support changed", root_counts))
    parent_dual = tuple(value / 30 for value in parent_root)
    require(dot(parent_dual, parent_even) == 0
            and dot(parent_dual, parent_root) == 1,
            "parent-labelled normalized dual changed")

    index = {monomial: position
             for position, monomial in enumerate(collision_monomials)}
    collected_even = [Q(0)] * 45
    collected_root = [Q(0)] * 45
    fibers = Counter()
    cancelled_parent_pairs = []
    for occurrence, coefficient in zip(OCCURRENCES, parent_root, strict=True):
        monomial = occurrence[3]
        position = index[monomial]
        collected_even[position] += 1
        collected_root[position] += coefficient
        fibers[monomial] += 1
    require(set(fibers.values()) == {2}
            and set(collected_even) == {Q(2)},
            "parent collection stopped being two-to-one")
    collected_counts = Counter(collected_root)
    require(collected_counts == Counter({Q(0): 21,
                                         Q(1): 12, Q(-1): 12}),
            ("collected 24-term residual changed", collected_counts))
    for monomial, coefficient in zip(collision_monomials, collected_root,
                                     strict=True):
        if coefficient:
            continue
        weights = [root_weight(item[1]) for item in OCCURRENCES
                   if item[3] == monomial]
        if sorted(weights) == [Q(-1), Q(1)]:
            cancelled_parent_pairs.append(monomial)
    require(len(cancelled_parent_pairs) == 3,
            "the three double-parent cancellations changed")

    collected_even = tuple(collected_even)
    collected_root = tuple(collected_root)
    collected_dual = tuple(value / 24 for value in collected_root)
    require(dot(collected_dual, collected_even) == 0
            and dot(collected_dual, collected_root) == 1,
            "collected normalized dual changed")

    # Cross-check the undecorated collected vector against the independently
    # pinned complete-response root audit.
    total = load(
        "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py",
        "fullword_collision_totalization_base",
    )
    expected = total.derivation(total.RESPONSE,
                                total.ROOT_LOOKUP["E01"]["replacements"])
    observed = Counter()
    for monomial, coefficient in zip(collision_monomials, collected_root,
                                     strict=True):
        if not coefficient:
            continue
        skeleton = tuple((cell[0], cell[1]) for cell in monomial)
        observed[skeleton] += coefficient
    require(observed == expected,
            "decorated parent collection disagrees with complete root audit")

    # The parent-labelled first-PP packet of the missing root family.  The
    # occurrence id is retained, so no two flags are silently collected.
    parent_pp = []
    collected_pp = []
    for occurrence_index, (occurrence, coefficient) in enumerate(
            zip(OCCURRENCES, parent_root, strict=True)):
        if not coefficient:
            continue
        monomial = occurrence[3]
        for removed_index, removed in enumerate(monomial):
            parent_pp.append((occurrence_index, removed, coefficient,
                              topology_after_removal(monomial, removed_index)))
    for monomial, coefficient in zip(collision_monomials, collected_root,
                                     strict=True):
        if not coefficient:
            continue
        for removed_index, removed in enumerate(monomial):
            collected_pp.append((monomial, removed, coefficient,
                                 topology_after_removal(monomial,
                                                        removed_index)))
    require(len(parent_pp) == len(set(parent_pp)) == 120,
            "parent-labelled PP packet changed")
    require(Counter(value[3] for value in parent_pp)
            == Counter({"3K2": 60, "P3+K2": 60}),
            "parent-labelled PP topology count changed")
    require(len(collected_pp) == len(set(collected_pp)) == 96,
            "collected residual PP packet changed")
    require(Counter(value[3] for value in collected_pp)
            == Counter({"3K2": 48, "P3+K2": 48}),
            "collected PP topology count changed")

    inventory = exhaustive_physical_inventory(collision_fine)
    # All 6561 projected physical columns are zero.  Adding the parent-even
    # collision column gives rank one; the normalized dual proves that the
    # signed root column raises it to two, both before and after collection.
    require(any(parent_even) and any(parent_root)
            and parent_root != parent_even
            and dot(parent_dual, parent_even) == 0
            and dot(parent_dual, parent_root) == 1,
            "parent rank certificate failed")
    require(any(collected_even) and any(collected_root)
            and dot(collected_dual, collected_even) == 0
            and dot(collected_dual, collected_root) == 1,
            "collected rank certificate failed")

    return {
        "sector": {
            "word": FIXED_WORD_LABEL,
            "word_tuple": list(FIXED_WORD),
            "missing_doubled": ["0", "S"],
            "operation_degree": [1, 2, 0, 1, 1, 1, 1, 1],
            "fine_degree": list(collision_fine),
            "collected_coordinates": len(collision_monomials),
            "operation_parent_occurrences": len(OCCURRENCES),
            "collection_fiber_size": 2,
        },
        "physical_inventory": inventory,
        "parent_lift": {
            "symmetric_collision_vector": "one on all 90 parent occurrences",
            "root_support": {"+1": 15, "-1": 15, "0": 60},
            "physical_plus_symmetric_rank": 1,
            "rank_after_root_residual": 2,
            "normalized_dual": "Xi_01/30",
            "dual_on_physical_symmetric_root": [0, 0, 1],
        },
        "collection": {
            "symmetric_collision_coefficients": "2 on all 45 terms",
            "root_support": {"+1": 12, "-1": 12, "0": 21},
            "cancelled_double_parent_monomials": 3,
            "physical_plus_symmetric_rank": 1,
            "rank_after_root_residual": 2,
            "normalized_dual": "R_01/24",
            "dual_on_physical_symmetric_root": [0, 0, 1],
        },
        "first_PP": {
            "parent_labelled_flags": len(parent_pp),
            "parent_labelled_topologies": {"3K2": 60, "P3+K2": 60},
            "collected_nonzero_flags": len(collected_pp),
            "collected_topologies": {"3K2": 48, "P3+K2": 48},
            "required_labels": [
                "response word", "operation parent", "root trigger",
                "removed edge", "fine degree", "reinsertion edge"
            ],
        },
    }


def audit():
    pin_dependencies()
    require(len(MATCHINGS) == 105 and len(DIRECT_FREE_MATCHINGS) == 90,
            "physical matching inventories changed")
    data = parent_and_collection_audit()
    ledger = {
        "theorem": "full-word parent-labelled collision-sector terminal gate",
        "pins": PINS,
        **data,
        "verdict": (
            "No.  The complete 3^8 physical coefficient inventory has zero "
            "projection to the fixed missing-0/doubled-S operation degree, "
            "in both the 105-term and direct-free 90-term presentations.  "
            "The only present collision column is parent-even and has rank "
            "one.  The signed root packet is parent-odd, raises rank to two, "
            "and is detected by Xi_01/30 before collection and R_01/24 after "
            "collection.  Pure-target normalization and all mixed-word zero "
            "equations remain in squarefree operation degree and are killed."
        ),
        "first_extra_row_family": (
            "an occurrence-labelled first Spencer/root family realizing "
            "Xi_01(H_w), where Xi_01=a_PS d/da_P0-a_S1 d/da_01, for every "
            "word.  At 11:110000 its top has 30 signed parent occurrences "
            "and collected boundary R_01.  Source validity additionally "
            "requires all 120 parent-labelled first-PP restriction faces, "
            "their reinsertion squares, and the downstream word/fine, target, "
            "ordinary-residue, anchor, q, W, and shifted-ridge augmentations."
        ),
        "scope": (
            "exact finite h=3 coefficient-support and rational-rank theorem "
            "for one 45-term collision sector, exhaustive over all 3^8 "
            "physical words and both complete-105 and direct-free-90 matching "
            "inventories.  It proves that no existing output equation supplies "
            "the residual; it does not construct the missing Spencer/root cell "
            "or certify its augmented physical descent."
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
    ledger, digest = audit()
    print("full 3^8 physical collision-sector inventory: ZERO PROJECTION")
    print("complete/direct-free terms:",
          ledger["physical_inventory"]["complete_105_terms"],
          ledger["physical_inventory"]["direct_free_90_terms"])
    print("parent lift rank: 1 -> 2; dual Xi_01/30")
    print("collected rank: 1 -> 2; dual R_01/24")
    print("first extra family: occurrence-labelled Spencer/root plus 120 PP faces")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
