#!/usr/bin/env python3
"""UNAUDITED REPAIR CANDIDATE (repair item 7): the 270-packet hybrid identity.

Replaces the content-free half of
``computations/verify_h3_order6_double_coloop_hybrid_interference_closure.py``.
That checker verifies, per packet, the mate partition

    selected_seed 1 | retains_e 14 | mixed_direct_PS 15 | new_offdiagonal 75

which is a statement about *matching counts only*: for ANY edge e incident
with S in ANY packet, 15 of the 105 physical matchings contain e, 15 contain
the direct PS pair (disjointly, since both meet S), and 105-15-15 = 75 remain.
It holds for every edge in every packet and never looks at a single colour or
coefficient (external audit 2026-08-13, CRITICAL defect 5).  It also records
the residual as one orbit; it is two.

WHAT THIS CHECKER VERIFIES INSTEAD.

(1) CENSUS AND ORBIT STRUCTURE, stated correctly.  The 270 residual ordered
    packets split into exactly TWO orbits of the internal relabelling group
    S6, of sizes 90 (matching1 = matching2, identical two-edge tails) and 180
    (tails one C4 apart).  A single orbit of size 270 is impossible by
    Lagrange, since 270 does not divide |S6| = 720; the checker states and
    verifies that arithmetic obstruction, computes the orbit decomposition by
    union-find over the generators (0 1) and (0 1 2 3 4 5), and verifies that
    the shape invariant is constant on each orbit.  The count remains 270
    under the extra bright-colour swap because that swap preserves both
    orbits.

(2) THE ACTUAL CELL-LEVEL COEFFICIENT CLAIM.  The hybrid word w has colour 2
    at S and at the common S-neighbour n, and colour 1 everywhere else.  For
    every one of the 270 packets and every one of the 105 physical matchings
    the checker computes the LITERAL decorated cell multiset that w assigns,
    and verifies:

      * the seed term (matching1) uses exactly the pure-2 diagonal cell on
        the common S-arm e = (n, S) together with the three pure-1 diagonal
        cells of matching1 -- every factor is an anchor cell of one of the
        two selected pure matchings;
      * each of the 14 remaining retain-e mates uses that same pure-2
        diagonal cell on e and pure-1 diagonal cells on a matching of the
        six sites off e, so seed + retain-e = A_e^{22} * (pure-1 cofactor);
      * each of the 15 direct-PS mates uses the MIXED off-diagonal cell
        ((P,S), 1, 2) -- the forbidden direct cell -- and the checker records
        its colours, not merely its count;
      * each of the 75 avoiding mates exposes exactly one S-arm cell
        ((m,S), 1, 2) with m outside {n, P}: an off-diagonal cell on an edge
        that is in none of the three pure anchors.

(3) THE ALGEBRAIC IDENTITY, on an honest complete-row model.  Exact rational
    cell values A[edge][a][b] over three colours; rows are genuine sums over
    all 105 matchings.  The escape hypotheses are imposed as cell values
    (forbidden direct mixed cell = 0; no new off-diagonal S-arm cell), the
    normalizations are SOLVED for (not assumed), and then the checker derives

        R_hybrid = A_e^{22} * C_1,     A_e^{22} != 0,
        R_hybrid = 0  ==>  C_1 = 0,
        R_pure1 = A_e^{11} * C_1 + (omit-e terms) = 1  ==>  omit-e terms = 1,

    so a nonzero pure-1 matching term omitting the common S-arm is FORCED and
    is exhibited explicitly.  That is the actual content of "if there is no
    avoiding mate, the pure-1 target row forces a pure matching omitting e".

Frozen ledger hashes: the two orbit representatives with their literal cell
profiles, the aggregate cell-colour profile table over all 270 packets, a
rolling digest of the full 270 x 105 cell-type stream, and the exact
algebraic certificates (cofactor values, forced omit-e witnesses).

POSITIVE CONTROLS (run in the same process, must FAIL):
  1. fabricated hybrid geometry -- put the second bright colour at S and at
     the common P-neighbour p instead of the common S-neighbour n.  The seed
     term then uses an off-diagonal cell on e and is not a substitution into
     the anchors at all;
  2. fabricated residual geometry -- define the residual by the shared
     S-neighbour alone (dropping the shared P-neighbour), which is not the
     double-coloop condition; the 270 = 90 + 180 two-orbit census fails.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
P, S = 6, 7
INTERNAL = tuple(range(6))
ALL_SITES = tuple(range(8))
COLOURS = (0, 1, 2)
PURE_ONE, PURE_TWO = 1, 2

PINS = {
    "computations/verify_h3_order6_double_coloop_hybrid_interference_closure.py":
        "fcbddfc7bb31389c9e8110fb6347e7393ae581878b6a6dbbe68a6602a68ce740",
    "computations/verify_h3_order6_primitive_selected_matching_activity.py":
        "aa0c3ec3f3a96f7fe9e8bb98117f4aec21501c0b77dda2ff5245eef19e9a34f2",
}
EXPECTED_LEDGER_SHA256 = (
    "505624ba62ee7a720beb89f3cc319078aaee83595519d42aedd76a31ffccb9d7"
)


class ControlDidNotFail(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def should_fail(label, thunk):
    try:
        thunk()
    except RuntimeError as failure:
        return {"control": label, "fired": True, "reason": str(failure)[:200]}
    raise ControlDidNotFail(("positive control did not fail", label))


# ---------------------------------------------------------------- geometry --

def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(tuple(sorted((tuple(sorted((first, second))),)
                                       + tail)))
    return tuple(answer)


ALL_MATCHINGS = perfect_matchings(ALL_SITES)
DIRECT = tuple(sorted((P, S)))
BRIGHT = tuple(matching for matching in ALL_MATCHINGS
               if DIRECT not in matching)


def neighbour(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError(("site absent from matching", site, matching))


def residual_packets(require_shared_p_neighbour=True):
    packets = []
    for matching1 in BRIGHT:
        n1, p1 = neighbour(matching1, S), neighbour(matching1, P)
        for matching2 in BRIGHT:
            n2, p2 = neighbour(matching2, S), neighbour(matching2, P)
            if n1 != n2:
                continue
            if require_shared_p_neighbour and p1 != p2:
                continue
            packets.append((matching1, matching2, n1, p1))
    return tuple(packets)


def packet_shape(matching1, matching2, neighbour_s, neighbour_p):
    common = {tuple(sorted((S, neighbour_s))), tuple(sorted((P, neighbour_p)))}
    tail1 = set(matching1) - common
    tail2 = set(matching2) - common
    require(len(tail1) == len(tail2) == 2,
            "double-coloop tail inventory changed")
    if tail1 == tail2:
        return "same_two_edge_tail"
    require(len(tail1 ^ tail2) == 4,
            "unequal double-coloop tails stopped being one C4")
    return "one_C4_tail_switch"


# ------------------------------------------------------------ cell algebra --

def decorated_cells(matching, word):
    """The literal decorated cells a colour word assigns to a matching."""
    return tuple(sorted((left, right, word[left], word[right])
                        for left, right in matching))


def hybrid_word(hot_sites):
    word = [PURE_ONE] * 8
    for site in hot_sites:
        word[site] = PURE_TWO
    return tuple(word)


def classify_packet(matching1, matching2, neighbour_s, neighbour_p,
                    hot_sites=None):
    """Full literal cell-type classification of all 105 mates."""
    edge_e = tuple(sorted((S, neighbour_s)))
    require(edge_e in matching1 and edge_e in matching2,
            "hybrid edge stopped being common to both bright anchors")
    hot = (S, neighbour_s) if hot_sites is None else hot_sites
    word = hybrid_word(hot)
    anchor_cells = set(decorated_cells(matching1, (PURE_ONE,) * 8))
    anchor_cells |= set(decorated_cells(matching2, (PURE_ONE,) * 8))
    anchor_cells |= set(decorated_cells(matching1, (PURE_TWO,) * 8))
    anchor_cells |= set(decorated_cells(matching2, (PURE_TWO,) * 8))
    anchor_edges = ({tuple(sorted(edge)) for edge in matching1}
                    | {tuple(sorted(edge)) for edge in matching2} | {DIRECT})

    classes = Counter()
    profile = Counter()
    stream = []
    for mate in ALL_MATCHINGS:
        cells = decorated_cells(mate, word)
        offdiagonal = tuple(cell for cell in cells if cell[2] != cell[3])
        if mate == matching1:
            label = "selected_seed"
            require(not offdiagonal,
                    ("the hybrid seed acquired an off-diagonal cell", cells))
            require((edge_e[0], edge_e[1], PURE_TWO, PURE_TWO) in cells,
                    ("the seed lost the pure-2 diagonal cell on the common "
                     "S arm", cells))
            require(sum(1 for cell in cells
                        if cell[2] == cell[3] == PURE_ONE) == 3,
                    ("the seed lost its three pure-1 diagonal cells", cells))
            require(all(cell in anchor_cells for cell in cells),
                    ("a seed factor is not a selected anchor cell", cells))
        elif edge_e in mate:
            label = "retains_e_pure1_reselection"
            require(not offdiagonal,
                    ("a retain-e mate acquired an off-diagonal cell", cells))
            require((edge_e[0], edge_e[1], PURE_TWO, PURE_TWO) in cells
                    and sum(1 for cell in cells
                            if cell[2] == cell[3] == PURE_ONE) == 3,
                    ("a retain-e mate is not A_e^22 times a pure-1 cofactor",
                     cells))
        elif DIRECT in mate:
            label = "mixed_direct_PS_forbidden"
            direct_cell = next(cell for cell in cells
                               if cell[:2] == DIRECT)
            require(direct_cell == (P, S, PURE_ONE, PURE_TWO),
                    ("the forbidden direct cell changed colours",
                     direct_cell))
        else:
            label = "new_offdiagonal_S_arm"
            arm_cells = tuple(cell for cell in cells if S in cell[:2])
            require(len(arm_cells) == 1, ("a mate lost its unique S arm",
                                          cells))
            arm_cell = arm_cells[0]
            require(arm_cell[2] != arm_cell[3],
                    ("the avoiding S arm stopped being off-diagonal",
                     arm_cell))
            require(arm_cell[:2] not in anchor_edges,
                    ("the avoiding S arm is inside the pure anchors",
                     arm_cell))
            require(arm_cell == (min(arm_cell[0], arm_cell[1]),
                                 S, PURE_ONE, PURE_TWO),
                    ("the avoiding S arm colours changed", arm_cell))
        classes[label] += 1
        signature = tuple(sorted((cell[2], cell[3]) for cell in cells))
        profile[(label, signature)] += 1
        stream.append((label, signature))
    require(dict(classes) == {
        "selected_seed": 1,
        "retains_e_pure1_reselection": 14,
        "mixed_direct_PS_forbidden": 15,
        "new_offdiagonal_S_arm": 75,
    }, ("hybrid mate partition changed", dict(classes)))
    return classes, profile, tuple(stream), edge_e, word


# --------------------------------------------------- honest complete rows --

def cell_key(left, right):
    return (left, right) if left < right else (right, left)


class Cells:
    """Exact rational decorated cell values on the complete eight-site graph."""

    def __init__(self, seed):
        self.state = seed & 0xFFFFFFFF
        self.values = {}
        for left, right in combinations(ALL_SITES, 2):
            for a in COLOURS:
                for b in COLOURS:
                    self.values[(left, right, a, b)] = Q(self._next())

    def _next(self):
        # Deterministic stdlib-free LCG so the certificate is reproducible.
        # Values avoid zero so that generic-position reasoning is honest.
        self.state = (1103515245 * self.state + 12345) & 0x7FFFFFFF
        value = (self.state % 18) - 9
        return value + 1 if value >= 0 else value

    def get(self, left, right, a, b):
        if left < right:
            return self.values[(left, right, a, b)]
        return self.values[(right, left, b, a)]

    def set(self, left, right, a, b, value):
        if left < right:
            self.values[(left, right, a, b)] = value
        else:
            self.values[(right, left, b, a)] = value

    def monomial(self, matching, word):
        answer = Q(1)
        for left, right in matching:
            answer *= self.get(left, right, word[left], word[right])
        return answer

    def row(self, matchings, word):
        return sum((self.monomial(matching, word) for matching in matchings),
                   Q(0))


def linear_in_cell(cells, matchings, word, left, right, a, b):
    """Split a row exactly as coefficient * A[cell] + remainder.

    No division is used, so the split is valid even when the current value of
    the cell happens to vanish.
    """
    if left < right:
        target = (left, right, a, b)
    else:
        target = (right, left, b, a)
    head, tail = target[0], target[1]
    coefficient = Q(0)
    remainder = Q(0)
    for matching in matchings:
        if ((head, tail) in matching
                and (word[head], word[tail]) == (target[2], target[3])):
            product = Q(1)
            for edge_left, edge_right in matching:
                if (edge_left, edge_right) == (head, tail):
                    continue
                product *= cells.get(edge_left, edge_right,
                                     word[edge_left], word[edge_right])
            coefficient += product
        else:
            remainder += cells.monomial(matching, word)
    return coefficient, remainder


def algebraic_certificate(matching1, matching2, neighbour_s, neighbour_p,
                          seed):
    """Build an honest complete-row model for one residual packet and derive
    the interference identity exactly."""
    cells = Cells(seed)
    edge_e = tuple(sorted((S, neighbour_s)))
    word = hybrid_word((S, neighbour_s))
    pure_one = (PURE_ONE,) * 8
    off_e_sites = tuple(site for site in ALL_SITES if site not in edge_e)
    cofactor_matchings = perfect_matchings(off_e_sites)
    require(len(cofactor_matchings) == 15, "cofactor inventory changed")

    # ESCAPE HYPOTHESES, imposed as literal cell values.
    #  * the forbidden mixed direct cell vanishes
    cells.set(P, S, PURE_ONE, PURE_TWO, Q(0))
    cells.set(P, S, PURE_TWO, PURE_ONE, Q(0))
    #  * there is no new off-diagonal S arm outside the pure anchors
    for site in ALL_SITES:
        if site in (S, neighbour_s, P):
            continue
        cells.set(site, S, PURE_ONE, PURE_TWO, Q(0))
        cells.set(site, S, PURE_TWO, PURE_ONE, Q(0))

    # The selected pure-2 anchor cell on the common S arm is nonzero.
    alpha = cells.get(edge_e[0], edge_e[1], PURE_TWO, PURE_TWO)
    if alpha == 0:
        alpha = Q(7)
        cells.set(edge_e[0], edge_e[1], PURE_TWO, PURE_TWO, alpha)

    # Normalization 1 (SOLVED, not assumed): force the pure-1 cofactor C_1 on
    # the six sites off e to vanish, by solving for one free pure-1 diagonal
    # cell inside that cofactor.
    free_edge = None
    for candidate in combinations(off_e_sites, 2):
        if candidate == DIRECT:
            continue
        coefficient, remainder = linear_in_cell(
            cells, cofactor_matchings, pure_one,
            candidate[0], candidate[1], PURE_ONE, PURE_ONE)
        if coefficient:
            free_edge = candidate
            break
    require(free_edge is not None,
            "the pure-1 cofactor is independent of every free cell")
    cells.set(free_edge[0], free_edge[1], PURE_ONE, PURE_ONE,
              -remainder / coefficient)
    cofactor = cells.row(cofactor_matchings, pure_one)
    require(cofactor == 0, ("pure-1 cofactor normalization failed", cofactor))

    # Normalization 2 (SOLVED): the pure-1 target row equals 1.  Solve on an
    # S-incident pure-1 diagonal cell, which is invisible to C_1 (no cofactor
    # matching touches S) and to the hybrid row (which uses the (1,2) cell
    # there, already set to zero).
    normalizing_site = None
    for candidate in INTERNAL:
        if candidate == neighbour_s:
            continue
        coefficient, remainder = linear_in_cell(
            cells, ALL_MATCHINGS, pure_one, candidate, S,
            PURE_ONE, PURE_ONE)
        if coefficient:
            normalizing_site = candidate
            break
    require(normalizing_site is not None,
            "the pure-1 target row is independent of every normalizing cell")
    cells.set(normalizing_site, S, PURE_ONE, PURE_ONE,
              (Q(1) - remainder) / coefficient)
    pure_row = cells.row(ALL_MATCHINGS, pure_one)
    require(pure_row == 1, ("pure-1 target normalization failed", pure_row))
    require(cells.row(cofactor_matchings, pure_one) == 0,
            "the second normalization disturbed the pure-1 cofactor")

    # ---- the derivation, verified term by term --------------------------
    seed_term = cells.monomial(matching1, word)
    retain = sum((cells.monomial(mate, word) for mate in ALL_MATCHINGS
                  if edge_e in mate), Q(0))
    direct_part = sum((cells.monomial(mate, word) for mate in ALL_MATCHINGS
                       if edge_e not in mate and DIRECT in mate), Q(0))
    avoiding = sum((cells.monomial(mate, word) for mate in ALL_MATCHINGS
                    if edge_e not in mate and DIRECT not in mate), Q(0))
    hybrid_row = cells.row(ALL_MATCHINGS, word)
    require(hybrid_row == retain + direct_part + avoiding,
            "the hybrid row partition is not exact")
    require(direct_part == 0,
            ("the forbidden direct class did not vanish", direct_part))
    require(avoiding == 0,
            ("the avoiding class did not vanish under the escape hypothesis",
             avoiding))
    require(retain == alpha * cofactor,
            ("retain-e class is not A_e^22 times the pure-1 cofactor",
             retain, alpha * cofactor))
    require(hybrid_row == alpha * cofactor == 0,
            ("the hybrid mixed row did not vanish", hybrid_row))
    require(alpha != 0, "the selected pure-2 anchor cell vanished")

    # C_1 = 0 with alpha != 0 forces the omit-e part of the pure-1 row to
    # carry the whole normalization, hence a literal omit-e matching term.
    diagonal = cells.get(edge_e[0], edge_e[1], PURE_ONE, PURE_ONE)
    retain_pure = sum((cells.monomial(mate, pure_one)
                       for mate in ALL_MATCHINGS if edge_e in mate), Q(0))
    omit_pure = sum((cells.monomial(mate, pure_one)
                     for mate in ALL_MATCHINGS if edge_e not in mate), Q(0))
    require(retain_pure == diagonal * cofactor == 0,
            ("the retain-e part of the pure-1 row is nonzero", retain_pure))
    require(omit_pure == 1,
            ("the forced omit-e aggregate changed", omit_pure))
    witnesses = [mate for mate in ALL_MATCHINGS
                 if edge_e not in mate and cells.monomial(mate, pure_one)]
    require(witnesses, "no literal omit-e pure-1 matching term was forced")

    return {
        "packet_edge_e": list(edge_e),
        "hybrid_word": list(word),
        "alpha_pure2_anchor_cell": str(alpha),
        "pure1_cofactor_C1": str(cofactor),
        "pure1_target_row": str(pure_row),
        "hybrid_mixed_row": str(hybrid_row),
        "seed_term": str(seed_term),
        "retain_class": str(retain),
        "direct_PS_class": str(direct_part),
        "avoiding_class": str(avoiding),
        "retain_equals_alpha_times_C1": True,
        "forced_omit_e_aggregate": str(omit_pure),
        "forced_omit_e_witness_count": len(witnesses),
        "forced_omit_e_first_witness": [list(edge) for edge in witnesses[0]],
        "forced_omit_e_first_witness_value":
            str(cells.monomial(witnesses[0], pure_one)),
    }


# ------------------------------------------------------------------ orbits --

def relabel_matching(matching, permutation):
    mapping = dict(zip(INTERNAL, permutation))
    mapping[P] = P
    mapping[S] = S
    return tuple(sorted(tuple(sorted((mapping[left], mapping[right])))
                        for left, right in matching))


def orbit_membership(packets, generators, colour_swap):
    """Union-find orbit membership of the residual packets under the given
    generators of the internal relabelling group (optionally together with
    the bright-colour swap that exchanges matching1 and matching2)."""
    index = {(matching1, matching2): position
             for position, (matching1, matching2, _n, _p)
             in enumerate(packets)}
    parent = list(range(len(packets)))

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(left, right):
        left, right = find(left), find(right)
        if left != right:
            parent[left] = right

    for position, (matching1, matching2, _n, _p) in enumerate(packets):
        images = [(relabel_matching(matching1, permutation),
                   relabel_matching(matching2, permutation))
                  for permutation in generators]
        if colour_swap:
            images.append((matching2, matching1))
        for key in images:
            require(key in index, ("the residual set is not stable", key))
            union(position, index[key])
    return [find(position) for position in range(len(packets))], index


def audit():
    for relative, expected in PINS.items():
        path = ROOT / relative
        require(path.exists(), ("pinned dependency missing", relative))
        actual = sha256(path.read_bytes()).hexdigest()
        if expected != "TO_BE_PINNED":
            require(actual == expected,
                    ("pinned dependency changed", relative, actual))

    require(len(ALL_MATCHINGS) == 105 and len(BRIGHT) == 90,
            "the physical matching inventory changed")

    packets = residual_packets()
    require(len(packets) == 270, ("residual packet census changed",
                                  len(packets)))
    shapes = Counter(packet_shape(*packet) for packet in packets)
    require(dict(shapes) == {"same_two_edge_tail": 90,
                             "one_C4_tail_switch": 180},
            ("double-coloop residual shapes changed", dict(shapes)))

    # The wording correction, as an arithmetic obstruction.
    require(720 % 270 != 0,
            "270 unexpectedly divides |S6|; the Lagrange obstruction changed")
    generators = ((1, 0, 2, 3, 4, 5), (1, 2, 3, 4, 5, 0))
    membership, _index = orbit_membership(packets, generators,
                                          colour_swap=False)
    orbits = Counter(membership)
    require(len(orbits) == 2,
            ("the residual is not two S6 orbits", len(orbits)))
    orbit_sizes = sorted(orbits.values())
    require(orbit_sizes == [90, 180],
            ("residual orbit sizes changed", orbit_sizes))
    # The extra bright-colour swap preserves both orbits, so the count is the
    # same for the full S6 x S2 action.
    swapped_membership, _index = orbit_membership(packets, generators,
                                                  colour_swap=True)
    require(len(Counter(swapped_membership)) == 2
            and sorted(Counter(swapped_membership).values()) == [90, 180],
            "the bright-colour swap merged the two residual orbits")

    by_orbit = {}
    for position, (matching1, matching2, neighbour_s, neighbour_p) in enumerate(
            packets):
        root = membership[position]
        shape = packet_shape(matching1, matching2, neighbour_s, neighbour_p)
        record = by_orbit.setdefault(root, {"size": 0, "shape": shape,
                                            "representative": position})
        require(record["shape"] == shape,
                ("the tail shape is not an S6-orbit invariant", position))
        record["size"] += 1
    require(sorted((record["size"], record["shape"])
                   for record in by_orbit.values())
            == [(90, "same_two_edge_tail"), (180, "one_C4_tail_switch")],
            "the two-orbit shape/size correspondence changed")

    # ---- literal cell classification of every packet --------------------
    aggregate = Counter()
    totals = Counter()
    cell_stream = sha256()
    for position, (matching1, matching2, neighbour_s, neighbour_p) in enumerate(
            packets):
        classes, profile, stream, edge_e, word = classify_packet(
            matching1, matching2, neighbour_s, neighbour_p)
        totals.update(classes)
        aggregate.update(profile)
        cell_stream.update(f"{position}|{edge_e}|{word}\n".encode())
        for label, signature in stream:
            cell_stream.update(f"{label}|{signature}\n".encode())
    require(dict(totals) == {
        "selected_seed": 270,
        "retains_e_pure1_reselection": 3780,
        "mixed_direct_PS_forbidden": 4050,
        "new_offdiagonal_S_arm": 20250,
    }, ("aggregate hybrid routing changed", dict(totals)))

    # ---- exact algebraic certificate on each orbit representative -------
    certificates = []
    for root, record in sorted(by_orbit.items(),
                               key=lambda item: item[1]["shape"]):
        position = record["representative"]
        matching1, matching2, neighbour_s, neighbour_p = packets[position]
        certificate = algebraic_certificate(
            matching1, matching2, neighbour_s, neighbour_p,
            seed=20260813 + position)
        certificate["orbit_shape"] = record["shape"]
        certificate["orbit_size"] = record["size"]
        certificate["representative_packet"] = [
            [list(edge) for edge in matching1],
            [list(edge) for edge in matching2],
        ]
        certificates.append(certificate)
    require(len(certificates) == 2,
            "the algebraic certificate lost an orbit")

    # ...and, so that the certificate is not merely representative, on every
    # one of the 270 packets with an independent model seed.
    forced_witnesses = Counter()
    certificate_stream = sha256()
    for position, (matching1, matching2, neighbour_s, neighbour_p) in enumerate(
            packets):
        certificate = algebraic_certificate(
            matching1, matching2, neighbour_s, neighbour_p,
            seed=771 + 13 * position)
        require(certificate["hybrid_mixed_row"] == "0"
                and certificate["pure1_cofactor_C1"] == "0"
                and certificate["forced_omit_e_aggregate"] == "1",
                ("the interference identity failed on a packet", position))
        forced_witnesses[certificate["forced_omit_e_witness_count"]] += 1
        certificate_stream.update(
            f"{position}|{certificate['alpha_pure2_anchor_cell']}|"
            f"{certificate['seed_term']}|{certificate['retain_class']}|"
            f"{certificate['forced_omit_e_first_witness']}|"
            f"{certificate['forced_omit_e_first_witness_value']}\n".encode())

    return {
        "theorem": ("double-coloop hybrid interference: literal cell "
                    "coefficients and the forced omit-e reselection"),
        "physical_matchings": len(ALL_MATCHINGS),
        "bright_matchings": len(BRIGHT),
        "residual_packets": len(packets),
        "residual_shapes": dict(sorted(shapes.items())),
        "residual_orbit_count_under_S6": len(orbits),
        "residual_orbit_sizes": orbit_sizes,
        "single_orbit_impossible_by_lagrange": {
            "group_order": 720, "claimed_orbit": 270,
            "divides": 720 % 270 == 0,
        },
        "orbit_shape_correspondence": sorted(
            (record["size"], record["shape"]) for record in by_orbit.values()
        ),
        "aggregate_mate_routes": dict(sorted(totals.items())),
        "cell_colour_profile": sorted(
            (f"{label}|{list(signature)}", count)
            for (label, signature), count in aggregate.items()
        ),
        "full_cell_type_stream_sha256": cell_stream.hexdigest(),
        "orbit_representative_certificates": certificates,
        "all_270_certificate_stream_sha256": certificate_stream.hexdigest(),
        "forced_omit_e_witness_histogram": dict(sorted(
            forced_witnesses.items())),
        "identity": (
            "with the forbidden direct mixed cell and every new off-diagonal "
            "S-arm cell set to zero, the hybrid mixed row is exactly "
            "alpha * C_1 with alpha the selected pure-2 anchor cell on the "
            "common S arm.  Vanishing of that row forces C_1 = 0, and the "
            "pure-1 target normalization then forces a nonzero pure-1 "
            "matching term omitting the common S arm"
        ),
        "wording_correction": (
            "the 270 residual packets are TWO S6 orbits, of sizes 90 "
            "(matching1 = matching2) and 180 (tails one C4 apart).  A single "
            "orbit of size 270 is impossible: 270 does not divide 720"
        ),
        "scope": (
            "the literal cell-level content of the hybrid substitution and "
            "its exact consequence on an honest complete-row model.  It does "
            "not prove that the physical rows satisfy the escape hypotheses, "
            "and it does not close the reselected selected-arm branch"
        ),
    }


def controls():
    fired = []

    def fabricated_hybrid_colouring():
        # Fabricated geometry: heat S and the common P-neighbour instead of
        # the common S-neighbour.  The common S arm is then off-diagonal and
        # the seed is not a substitution into the two pure anchors.
        packets = residual_packets()
        for matching1, matching2, neighbour_s, neighbour_p in packets[:1]:
            classify_packet(matching1, matching2, neighbour_s, neighbour_p,
                            hot_sites=(S, neighbour_p))

    def fabricated_residual_condition():
        # Fabricated geometry: shared S-neighbour only.  This is not the
        # double-coloop condition and does not give 270 = 90 + 180.
        packets = residual_packets(require_shared_p_neighbour=False)
        require(len(packets) == 270,
                ("fabricated residual condition changed the census",
                 len(packets)))
        shapes = Counter(packet_shape(*packet) for packet in packets)
        require(dict(shapes) == {"same_two_edge_tail": 90,
                                 "one_C4_tail_switch": 180},
                ("fabricated residual condition changed the shapes",
                 dict(shapes)))

    fired.append(should_fail("fabricated hybrid colouring (colour 2 at the "
                             "P-neighbour)", fabricated_hybrid_colouring))
    fired.append(should_fail("fabricated residual condition (shared S "
                             "neighbour only)", fabricated_residual_condition))
    return fired


def main():
    control_records = controls()
    ledger = audit()
    ledger["positive_controls"] = [
        {"control": record["control"], "fired": record["fired"]}
        for record in control_records
    ]
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("double-coloop interference coefficient ledger changed",
                 digest))
    print("repair678 double-coloop interference coefficients: PASS")
    print("residual packets:", ledger["residual_packets"],
          "= TWO S6 orbits of sizes", ledger["residual_orbit_sizes"])
    print("cell-type stream sha256:", ledger["full_cell_type_stream_sha256"])
    print("270-packet certificate stream sha256:",
          ledger["all_270_certificate_stream_sha256"])
    for record in control_records:
        print("positive control fired:", record["control"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
