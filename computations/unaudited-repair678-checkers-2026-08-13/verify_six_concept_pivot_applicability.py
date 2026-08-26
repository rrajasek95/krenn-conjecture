#!/usr/bin/env python3
"""UNAUDITED REPAIR CANDIDATE (repair item 8): six-concept pivot applicability.

Replaces ``audit_six_closed_concepts`` and the free-symbol half of
``audit_complete_row_pivot`` inside
``computations/verify_h3_active_fan_coloop_complete_row_pivot.py``.

What the committed checker does:

  * ``audit_complete_row_pivot`` manipulates five FREE symbols
    (alpha, d_i, C_i, U_i, V_i) in a polynomial ring and checks that
    ``alpha*(d_i C_i + U_i - 1) - d_i*(alpha C_i + V_i)`` expands to
    ``alpha U_i - d_i V_i - alpha``.  True, but it is ring arithmetic: no
    matching, no cell, no coloop and no normalization is involved, so it
    cannot detect that "= alpha" needs BOTH normalizations
    (pure target row = 1, two-site mixed row = 0).
  * ``audit_six_closed_concepts`` checks Galois-closure and closure growth on
    K6 and then *emits the string* ``"the same alpha*U_i-d_i*V_i=alpha
    pivot"`` for each of the six representatives.  The two functions never
    touch each other's data, so zero of six concepts is verified (external
    audit 2026-08-13, HIGH defect 10).

THIS CHECKER instead builds, for each concept and each endpoint hole, an
HONEST complete-row model (the model shape is the one the external audit used
in ``scratchpad/indep/c3_indep.py``, extended so that the coloop and the
normalizations are CONSTRUCTED rather than posited):

  * exact rational decorated cells ``A[edge][a][b]`` on all eight sites,
    three colours; every row is a genuine sum over all 105 physical
    matchings; the direct PS cell is zero (direct-free presentation);
  * ``e = (0,1)`` is made a LITERAL coloop of the pure-c target support by
    zeroing every pure-c cell on an edge meeting {0,1} other than e -- and
    the checker then verifies that every nonzero pure-c monomial does contain
    e, so coloopness is a computed property, not a label;
  * ``alpha = A_e^{cc}`` is solved so that ``alpha * C_c = 1``, i.e. the
    coloop target row is normalized;
  * the endpoint hole of the i-channel rows is pinned to a prescribed
    residual edge h by zeroing the i-channel P-arm and S-arm cells off h,
    which leaves the pure-c row untouched;
  * the pure-i target row is SOLVED to 1 and the two-site mixed row is SOLVED
    to 0, on cells that occur in exactly one of the two rows.

Then, for every (channel, hole) model, the checker computes the four
aggregates from the matchings themselves and verifies

    d_i C_i + U_i = 1,      alpha C_i + V_i = 0,
    alpha U_i - d_i V_i = alpha,     alpha != 0,

hence ``U_i`` or ``V_i`` is nonzero and a LITERAL omit-e matching term is
forced; it exhibits one, checks its endpoint hole is exactly h, and checks
the claimed TYPING is retained term by term: the paired pure/mixed omit-e
terms use the same physical matching, the same P and S partners and
orientation, the same endpoint output heads, and identical decorations away
from the two changed coloop endpoints -- exactly two changed cells, both
incident with e.

Finally the six concepts are identified honestly: all 448 Galois-closed edge
sets of K6 are enumerated, decomposed into 11 S6-orbits, the two degenerate
ones (empty and complete) are removed to leave 446 in 9 orbits, and the 9
orbits are paired by the blocker duality F <-> T(F) into exactly SIX concept
types.  The six committed representatives are verified to realize the six
types, one each.  For each type and each of the 15 possible holes the pivot
model above is exercised: a hole on the shore types the concept, a hole off
the shore strictly enlarges the Galois closure, and in BOTH cases the very
same pivot identity applies.

Frozen ledger hashes: the 30 model certificates (exact alpha, d_i, C_i, U_i,
V_i, and forced witnesses), the per-concept hole tables, and the computed
orbit/duality classification of the closed concepts.

POSITIVE CONTROLS (run in the same process, must FAIL):
  1. fabricated coloop -- keep the pure-c cells on edges meeting {0,1}, so e
     is not a coloop; the computed coloop property and alpha*C_c = 1 fail;
  2. fabricated closed concept -- the non-closed family {01, 02, 03}
     presented as a saturated concept.
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
RESIDUAL = tuple(range(6))
P, S = 6, 7
ALL_SITES = tuple(range(8))
COLOUR_C = 0
CHANNELS = (1, 2)
E = (0, 1)
DIRECT = (P, S)
EDGES = tuple(combinations(RESIDUAL, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}

PINS = {
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "1d9800d9b1d84260741fff843a036a0d426128b4cda1acb042267c986fb493ac",
    "computations/verify_h3_active_fan_coloop_saturation_boundary.py":
        "cf22023a325bc0bc1588e990b515e5c79ab6436a37e9aa96c8f1eb592baef248",
}
EXPECTED_LEDGER_SHA256 = (
    "a07fd3ffac971fb9b330d59b81a3a5822382d47b88a61deba9a4cf88d9c013f7"
)


class ControlDidNotFail(RuntimeError):
    pass


class ModelNotGeneric(RuntimeError):
    """Raised when a pseudo-random cell assignment is too degenerate to carry
    the normalizations; the caller retries with a fresh seed.  It never masks
    a failure of the mathematical claims, which use `require`."""


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def should_fail(label, thunk):
    try:
        thunk()
    except RuntimeError as failure:
        return {"control": label, "fired": True, "reason": str(failure)[:200]}
    raise ControlDidNotFail(("positive control did not fail", label))


# ------------------------------------------------------- Galois concepts ----

def transversal_mask(mask):
    answer = 0
    for index, candidate in enumerate(EDGES):
        if all(set(candidate) & set(member)
               for position, member in enumerate(EDGES)
               if mask >> position & 1):
            answer |= 1 << index
    return answer


def build_closed_concepts():
    neighbourhood = []
    for edge in EDGES:
        mask = 0
        for index, other in enumerate(EDGES):
            if set(edge) & set(other):
                mask |= 1 << index
        neighbourhood.append(mask)
    full = (1 << len(EDGES)) - 1
    table = [0] * (1 << len(EDGES))
    table[0] = full
    for mask in range(1, 1 << len(EDGES)):
        low = mask & -mask
        table[mask] = table[mask ^ low] & neighbourhood[low.bit_length() - 1]
    # Sanity: the fast transversal table agrees with the direct definition.
    for mask in (0, 1, 5, 1 << 14, (1 << 15) - 1, 0b101010101010101):
        require(table[mask] == transversal_mask(mask),
                ("transversal table disagreed with the definition", mask))
    closed = sorted({table[mask] for mask in range(1 << len(EDGES))})
    require(all(table[table[mask]] == mask for mask in closed),
            "a claimed closed set is not a fixed point of T o T")
    return tuple(closed), table


def mask_of(family):
    mask = 0
    for edge in family:
        mask |= 1 << EDGE_INDEX[tuple(sorted(edge))]
    return mask


def family_of(mask):
    return tuple(EDGES[index] for index in range(len(EDGES))
                 if mask >> index & 1)


def relabel_mask(mask, permutation):
    answer = 0
    for index, edge in enumerate(EDGES):
        if mask >> index & 1:
            left, right = permutation[edge[0]], permutation[edge[1]]
            answer |= 1 << EDGE_INDEX[(min(left, right), max(left, right))]
    return answer


def classify_concepts():
    closed, table = build_closed_concepts()
    require(len(closed) == 448,
            ("Galois-closed concept count changed", len(closed)))
    group = tuple(permutations(RESIDUAL))
    remaining = set(closed)
    orbits = []
    while remaining:
        seed = min(remaining)
        orbit = {relabel_mask(seed, permutation) for permutation in group}
        require(orbit <= remaining, "closed-set orbits are not a partition")
        orbits.append({"representative": seed, "size": len(orbit),
                       "members": orbit})
        remaining -= orbit
    require(len(orbits) == 11,
            ("S6 orbit count on closed concepts changed", len(orbits)))
    degenerate = [orbit for orbit in orbits
                  if orbit["size"] == 1 and orbit["representative"]
                  in (0, (1 << len(EDGES)) - 1)]
    require(len(degenerate) == 2, "the two degenerate concepts changed")
    proper = [orbit for orbit in orbits if orbit not in degenerate]
    require(len(proper) == 9 and sum(orbit["size"] for orbit in proper) == 446,
            ("non-degenerate closed concept census changed",
             len(proper), sum(orbit["size"] for orbit in proper)))

    # Pair the 9 orbits by blocker duality F <-> T(F): three self-dual orbits
    # and three dual pairs give exactly SIX concept types.
    orbit_of = {}
    for index, orbit in enumerate(proper):
        for member in orbit["members"]:
            orbit_of[member] = index
    types = []
    seen = set()
    for index, orbit in enumerate(proper):
        if index in seen:
            continue
        dual = orbit_of[table[orbit["representative"]]]
        seen.add(index)
        seen.add(dual)
        types.append({
            "orbits": sorted({index, dual}),
            "self_dual": dual == index,
            "sides": sorted([
                [len(family_of(orbit["representative"])),
                 orbit["size"]],
                [len(family_of(proper[dual]["representative"])),
                 proper[dual]["size"]],
            ]),
        })
    require(len(types) == 6,
            ("closed concept types changed", len(types)))
    return closed, table, proper, orbit_of, types


# ----------------------------------------------- honest complete-row model --

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
COFACTOR_MATCHINGS = perfect_matchings(
    tuple(site for site in ALL_SITES if site not in E))
RETAIN = tuple(matching for matching in ALL_MATCHINGS if E in matching)
OMIT = tuple(matching for matching in ALL_MATCHINGS if E not in matching)


class Cells:
    def __init__(self, seed):
        self.state = seed & 0x7FFFFFFF
        self.values = {}
        for left, right in combinations(ALL_SITES, 2):
            for a in range(3):
                for b in range(3):
                    self.values[(left, right, a, b)] = Q(self._next())

    def _next(self):
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
            if not answer:
                return Q(0)
        return answer

    def row(self, matchings, word):
        return sum((self.monomial(matching, word) for matching in matchings),
                   Q(0))

    def split_on(self, matchings, word, left, right, a, b):
        """Exact coefficient/remainder split of a row in one cell."""
        head, tail = (left, right) if left < right else (right, left)
        colours = (a, b) if left < right else (b, a)
        coefficient = Q(0)
        remainder = Q(0)
        for matching in matchings:
            if ((head, tail) in matching
                    and (word[head], word[tail]) == colours):
                product = Q(1)
                for edge_left, edge_right in matching:
                    if (edge_left, edge_right) == (head, tail):
                        continue
                    product *= self.get(edge_left, edge_right,
                                        word[edge_left], word[edge_right])
                coefficient += product
            else:
                remainder += self.monomial(matching, word)
        return coefficient, remainder


def words(channel):
    pure_c = (COLOUR_C,) * 8
    pure_i = (channel,) * 8
    mixed = (COLOUR_C, COLOUR_C) + (channel,) * 6
    return pure_c, pure_i, mixed


def hole_of(matching):
    partner = {}
    for left, right in matching:
        partner[left] = right
        partner[right] = left
    return partner[P], partner[S]


def build_model(channel, hole, seed, honest_coloop=True):
    """Construct an honest complete-row model with e=(0,1) a literal coloop of
    the pure-c target and the i-channel endpoint hole pinned to `hole`."""
    cells = Cells(seed)
    pure_c, pure_i, mixed = words(channel)
    hole_p, hole_s = hole

    # direct-free presentation
    for a in range(3):
        for b in range(3):
            cells.set(P, S, a, b, Q(0))

    # e is a coloop of the pure-c target support
    if honest_coloop:
        for left, right in combinations(ALL_SITES, 2):
            if (left, right) == E:
                continue
            if left in E or right in E:
                cells.set(left, right, COLOUR_C, COLOUR_C, Q(0))

    # pin the i-channel endpoint hole (leaves the pure-c row untouched)
    for site in RESIDUAL:
        if site != hole_p:
            cells.set(site, P, channel, channel, Q(0))
            cells.set(site, P, COLOUR_C, channel, Q(0))
        if site != hole_s:
            cells.set(site, S, channel, channel, Q(0))
            cells.set(site, S, COLOUR_C, channel, Q(0))

    # normalize the coloop target row: alpha * C_c = 1
    cofactor_c = cells.row(COFACTOR_MATCHINGS, pure_c)
    if cofactor_c == 0:
        raise ModelNotGeneric("the pure-c cofactor vanished")
    alpha = Q(1) / cofactor_c
    cells.set(E[0], E[1], COLOUR_C, COLOUR_C, alpha)

    # Normalize the pure-i target row to 1.  Any pure-i diagonal cell may be
    # used: the mixed row is normalized afterwards on a cell that occurs in
    # the mixed row only, so the two solves do not interfere.
    chosen_pure = None
    for left, right in combinations(ALL_SITES, 2):
        coefficient, remainder = cells.split_on(
            ALL_MATCHINGS, pure_i, left, right, channel, channel)
        if coefficient:
            chosen_pure = (left, right)
            cells.set(left, right, channel, channel,
                      (Q(1) - remainder) / coefficient)
            break
    if chosen_pure is None:
        raise ModelNotGeneric("no free pure-i cell normalizes the target row")

    # normalize the two-site mixed row to 0, on a cell absent from pure-i
    chosen_mixed = None
    for left, right in combinations(ALL_SITES, 2):
        if (left in E) == (right in E):
            continue
        coefficient, remainder = cells.split_on(
            ALL_MATCHINGS, mixed, left, right,
            mixed[left], mixed[right])
        if coefficient:
            chosen_mixed = (left, right)
            cells.set(left, right, mixed[left], mixed[right],
                      -remainder / coefficient)
            break
    if chosen_mixed is None:
        raise ModelNotGeneric(
            "no free mixed cell normalizes the two-site mixed row")
    return cells, chosen_pure, chosen_mixed


def pivot_certificate(channel, hole, seed, honest_coloop=True):
    attempt = 0
    while True:
        try:
            cells, chosen_pure, chosen_mixed = build_model(
                channel, hole, seed + 7919 * attempt,
                honest_coloop=honest_coloop)
            break
        except ModelNotGeneric:
            attempt += 1
            require(attempt < 40,
                    ("no generic complete-row model exists for this hole",
                     channel, hole))
    used_seed = seed + 7919 * attempt
    pure_c, pure_i, mixed = words(channel)

    # (a) coloopness is COMPUTED, not labelled
    coloop_support = [matching for matching in ALL_MATCHINGS
                      if cells.monomial(matching, pure_c)]
    require(coloop_support, "the pure-c target support became empty")
    require(all(E in matching for matching in coloop_support),
            ("e is not a coloop of the pure-c target support",
             len(coloop_support)))
    alpha = cells.get(E[0], E[1], COLOUR_C, COLOUR_C)
    cofactor_c = cells.row(COFACTOR_MATCHINGS, pure_c)
    require(alpha * cofactor_c == 1,
            ("the coloop target factorization alpha*C_c=1 failed",
             alpha * cofactor_c))
    require(alpha != 0, "alpha vanished")

    # (b) the two complete-row splits, computed from the matchings
    diagonal = cells.get(E[0], E[1], channel, channel)
    cofactor_i = cells.row(COFACTOR_MATCHINGS, pure_i)
    pure_omit = cells.row(OMIT, pure_i)
    mixed_omit = cells.row(OMIT, mixed)
    require(cells.row(RETAIN, pure_i) == diagonal * cofactor_i,
            "the pure-i retain part did not factor through the cofactor")
    require(cells.row(RETAIN, mixed) == alpha * cofactor_i,
            "the mixed retain part did not factor through the same cofactor")
    require(diagonal * cofactor_i + pure_omit == 1,
            ("the pure target split d_i*C_i+U_i=1 failed",
             diagonal * cofactor_i + pure_omit))
    require(alpha * cofactor_i + mixed_omit == 0,
            ("the mixed split alpha*C_i+V_i=0 failed",
             alpha * cofactor_i + mixed_omit))

    # (c) the elimination, DERIVED here rather than asserted symbolically
    require(alpha * pure_omit - diagonal * mixed_omit == alpha,
            ("the complete-row pivot alpha*U_i-d_i*V_i=alpha failed",
             alpha * pure_omit - diagonal * mixed_omit, alpha))
    require(pure_omit != 0 or mixed_omit != 0,
            "the pivot failed to force a nonzero omit-e aggregate")

    # (d) the forced literal omit-e term, and its endpoint hole
    witnesses = [matching for matching in OMIT
                 if cells.monomial(matching, pure_i)
                 or cells.monomial(matching, mixed)]
    require(witnesses, "no literal omit-e term was forced")
    holes = {hole_of(matching) for matching in witnesses}
    require(holes == {hole},
            ("the forced omit-e terms left the pinned endpoint hole",
             sorted(map(repr, holes)), hole))

    # (e) the CLAIMED TYPING, checked term by term on the forced carriers
    changed_profile = Counter()
    for matching in witnesses:
        pure_cells = {edge: (pure_i[edge[0]], pure_i[edge[1]])
                      for edge in matching}
        mixed_cells = {edge: (mixed[edge[0]], mixed[edge[1]])
                       for edge in matching}
        changed = tuple(edge for edge in matching
                        if pure_cells[edge] != mixed_cells[edge])
        require(len(changed) == 2
                and all(set(edge) & set(E) for edge in changed),
                ("a paired omit-e term lost its two changed incident cells",
                 matching, changed))
        require(all(pure_cells[edge] == mixed_cells[edge]
                    for edge in matching if edge not in changed),
                "the paired omit-e terms lost their common remote tail")
        require(pure_i[P] == mixed[P] == channel
                and pure_i[S] == mixed[S] == channel,
                "the paired term changed an endpoint output head")
        require(hole_of(matching) == hole,
                "a forced carrier changed its ordered endpoint ports")
        changed_profile[len(changed)] += 1

    return {
        "channel": channel,
        "hole": list(hole),
        "alpha": str(alpha),
        "d_i": str(diagonal),
        "C_c": str(cofactor_c),
        "C_i": str(cofactor_i),
        "U_i": str(pure_omit),
        "V_i": str(mixed_omit),
        "alpha_U_minus_d_V": str(alpha * pure_omit - diagonal * mixed_omit),
        "coloop_support_size": len(coloop_support),
        "forced_omit_e_witnesses": len(witnesses),
        "first_witness": [list(edge) for edge in witnesses[0]],
        "changed_cells_per_paired_term": dict(sorted(changed_profile.items())),
        "normalizing_pure_cell": list(chosen_pure),
        "normalizing_mixed_cell": list(chosen_mixed),
        "model_seed": used_seed,
    }


# ------------------------------------------------------------------- audit --

def committed_representatives():
    triangle = ((0, 1), (0, 2), (1, 2))
    matching = ((0, 3), (1, 2))
    path_left = ((0, 1), (0, 3), (1, 2))
    adjacent = ((0, 1), (0, 2))
    singleton = ((0, 1),)
    star = tuple((0, site) for site in range(1, 6))
    return (
        ("triangle", triangle, (3, 3)),
        ("two_disjoint_edges", matching, (2, 4)),
        ("path_on_four_vertices", path_left, (3, 3)),
        ("adjacent_pair", adjacent, (2, 6)),
        ("singleton", singleton, (1, 9)),
        ("star", star, (5, 5)),
    )


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    closed, table, proper, orbit_of, types = classify_concepts()

    # The six committed representatives realize the six concept types, once
    # each -- verified, not assumed.
    representatives = committed_representatives()
    require(len(representatives) == 6, "the representative list changed")
    realized = {}
    concept_records = []
    for name, family, sizes in representatives:
        mask = mask_of(family)
        dual = table[mask]
        require(table[dual] == mask and table[table[mask]] == mask,
                ("a committed representative is not Galois-closed", name))
        require((len(family_of(mask)), len(family_of(dual))) == sizes,
                ("a committed representative changed sides", name))
        require(mask in orbit_of,
                ("a committed representative left the proper concepts", name))
        index = orbit_of[mask]
        type_index = next(position for position, record in enumerate(types)
                          if index in record["orbits"])
        require(type_index not in realized,
                ("two committed representatives share a concept type", name,
                 realized.get(type_index)))
        realized[type_index] = name
        concept_records.append({
            "name": name,
            "left": [list(edge) for edge in family_of(mask)],
            "right": [list(edge) for edge in family_of(dual)],
            "sides": list(sizes),
            "orbit_index": index,
            "orbit_size": proper[index]["size"],
            "concept_type": type_index,
            "self_dual": types[type_index]["self_dual"],
        })
    require(len(realized) == 6,
            "the six committed representatives do not realize six types")

    # ---- one model per (channel, hole); reused by every concept ----------
    models = {}
    for channel in CHANNELS:
        for hole_p in RESIDUAL:
            for hole_s in RESIDUAL:
                if hole_p == hole_s:
                    continue
                seed = (20260813 + 101 * channel + 17 * hole_p + hole_s)
                models[(channel, (hole_p, hole_s))] = pivot_certificate(
                    channel, (hole_p, hole_s), seed)
    require(len(models) == len(CHANNELS) * 30,
            ("model census changed", len(models)))
    for certificate in models.values():
        require(certificate["alpha_U_minus_d_V"] == certificate["alpha"],
                ("a model lost the pivot identity", certificate["hole"]))

    # ---- per concept: every hole is typed or grows the closure -----------
    for record in concept_records:
        mask = mask_of([tuple(edge) for edge in record["left"]])
        dual = table[mask]
        sides = []
        for side_mask in (mask, dual):
            inside = 0
            outside = 0
            typed_by_model = 0
            grew = 0
            for edge in EDGES:
                position = 1 << EDGE_INDEX[edge]
                on_shore = bool(side_mask & position)
                enlarged = table[table[side_mask | position]]
                if on_shore:
                    inside += 1
                    require(enlarged == side_mask,
                            "an on-shore hole changed the closure")
                else:
                    outside += 1
                    require(len(family_of(enlarged))
                            > len(family_of(side_mask)),
                            "a new typed hole failed to enlarge a closed shore")
                    grew += 1
                for channel in CHANNELS:
                    for orientation in (edge, (edge[1], edge[0])):
                        certificate = models[(channel, orientation)]
                        # the SAME pivot identity applies at this hole
                        require(certificate["alpha_U_minus_d_V"]
                                == certificate["alpha"],
                                "the pivot identity failed at a concept hole")
                        require(certificate["forced_omit_e_witnesses"] >= 1,
                                "the pivot forced no carrier at this hole")
                        require(tuple(certificate["hole"]) == orientation,
                                "a model drifted off its pinned hole")
                        if on_shore:
                            typed_by_model += 1
            sides.append({
                "shore_size": len(family_of(side_mask)),
                "holes_on_shore": inside,
                "holes_off_shore": outside,
                "strict_growth_checks": grew,
                "pivot_models_typing_the_shore": typed_by_model,
            })
        record["sides"] = sides
        record["source_identity"] = "alpha*U_i - d_i*V_i = alpha (computed)"

    model_stream = sha256()
    for key in sorted(models, key=repr):
        certificate = models[key]
        model_stream.update(json.dumps(certificate, sort_keys=True,
                                       separators=(",", ":")).encode())

    return {
        "theorem": ("the complete-row coloop pivot applies, with its typing "
                    "retained, at every hole of each of the six saturated "
                    "closed K6 concepts"),
        "closed_concepts_total": len(closed),
        "closed_concepts_non_degenerate": 446,
        "s6_orbits_total": 11,
        "s6_orbits_non_degenerate": 9,
        "concept_types_after_blocker_duality": len(types),
        "concept_type_table": types,
        "committed_representatives_realize_all_types": True,
        "concepts": concept_records,
        "pivot_models": len(models),
        "pivot_model_certificates": {repr(key): models[key]
                                     for key in sorted(models, key=repr)},
        "pivot_model_stream_sha256": model_stream.hexdigest(),
        "identity": (
            "on an honest complete-row model with e a computed coloop, the "
            "pure target row solved to 1 and the two-site mixed row solved "
            "to 0, the elimination alpha*U_i - d_i*V_i = alpha is a derived "
            "identity, alpha is nonzero because alpha*C_c = 1, and therefore "
            "a literal omit-e matching term is forced with the pinned "
            "endpoint hole and the claimed common-tail typing"
        ),
        "reading": (
            "the two normalizations are what turn the free-symbol elimination "
            "into '= alpha'.  Both are constructed here, so the identity is "
            "verified rather than posited, and it is verified at all 30 "
            "oriented holes in both target channels, which covers every hole "
            "of every one of the six concept types"
        ),
        "scope": (
            "an honest complete-row model of the coloop pivot and the exact "
            "Galois classification of the K6 concepts.  It does not prove "
            "that the physical rows realize this model, does not choose which "
            "hole is nonzero, and does not produce the simultaneous "
            "four-response affine coordinate point"
        ),
    }


def controls():
    fired = []

    def fabricated_coloop():
        # Fabricated geometry: e is declared a coloop but the pure-c cells on
        # edges meeting {0,1} are left in place, so it is not one.
        pivot_certificate(1, (2, 3), 4242, honest_coloop=False)

    def fabricated_closed_concept():
        family = ((0, 1), (0, 2), (0, 3))
        _closed, table = build_closed_concepts()
        mask = mask_of(family)
        require(table[table[mask]] == mask,
                ("the fabricated family {01,02,03} is not Galois-closed",
                 [list(edge) for edge in family_of(table[table[mask]])]))

    fired.append(should_fail("fabricated coloop (pure-c cells on edges "
                             "meeting the coloop retained)", fabricated_coloop))
    fired.append(should_fail("fabricated closed concept {01,02,03}",
                             fabricated_closed_concept))
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
                ("six-concept pivot ledger changed", digest))
    print("repair678 six-concept pivot applicability: PASS")
    print("closed K6 concepts:", ledger["closed_concepts_total"],
          "| non-degenerate:", ledger["closed_concepts_non_degenerate"],
          "| S6 orbits:", ledger["s6_orbits_non_degenerate"],
          "| concept types:",
          ledger["concept_types_after_blocker_duality"])
    print("honest pivot models built and verified:", ledger["pivot_models"])
    print("model stream sha256:", ledger["pivot_model_stream_sha256"])
    for record in control_records:
        print("positive control fired:", record["control"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
