#!/usr/bin/env python3
"""Exact support lower bound for the h=3 axis-purified cancellation branch.

Work with the five one-bad tensors

    q^[3] = X0,
    p_i s_j q^[2] = delta_ij Xi,  i,j in {1,2}.

All q cells are colour-diagonal and each endpoint row i is supported only in
colour i.  A nonzero target coefficient supplies one matching monomial in
each of X0, X1, X2.  Choosing those monomials gives an eleven-coordinate
target skeleton.  Up to the 48-element stabilizer of a fixed X0 matching,
there are 185 skeletons.

In an exact source every off-target coefficient is zero.  Since all occupied
coordinates are nonzero, no off-target matching fibre may contain exactly
one monomial.  This necessary ``no singleton fibre`` condition is enough to
exclude every axis-purified support through sixteen decorated coordinates.

The first circuit-repair layer occurs after four added coordinates: 98
placements repair every singleton already present on their skeleton, but
each creates new singleton unary/response locks.  One further coordinate
does not close them.  Thus a hypothetical axis-purified exact source has at
least seventeen decorated coordinates.  The checker does not claim that a
support of size seventeen exists or that maximum-support circuits can all
be lowered.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_segre_bright_full_row_min_support_completion_gate.py":
        "3db99d9141e3015c6199da76c0619a235bb6fb95f364e3d2dce338fa2d428572",
    "notes/h3-segre-bright-full-row-min-support-completion-gate.md":
        "26f94fac7c66405eff04406c95935da910d26cdecf135b05a212e469506cbfc9",
    "computations/verify_uniform_diagonal_alternating_cycle_switch_boundary.py":
        "f99c185403bf2e86b7352c555cd02d85bfed0df668b8a87b44a725c3db7edc71",
    "notes/uniform-diagonal-alternating-cycle-switch-boundary.md":
        "1e5b1a530d782ff03805b293ccfc3e6d76db6f046c8d8ffd4224ed3f9725f9e8",
    "computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py":
        "1594dcac16bb77bb929c18edda224e215ea99697bfd36edabc4230a0d341b5c8",
    "notes/uniform-one-bad-axis-hessian-carrier-circuit-boundary.md":
        "d784f8d25461ffcdafcc3fb9a39ccc776f770fb63359f722bead4fe7c965e73e",
}
EXPECTED_LEDGER_SHA256 = "144a19ff9a970d26add55bcd3b3a953e742695a772e64be23649d82ba112f4d0"

SITES = tuple(range(6))
EDGES = tuple((left, right) for left in SITES for right in SITES
              if left < right)
F0 = frozenset(((0, 1), (2, 3), (4, 5)))

# Coordinates are q(c,edge), p(i,site), and s(i,site).  The colour on an
# endpoint coordinate equals its row label in the axis-purified branch.
ALL_COORDINATES = frozenset(
    [("q", colour, edge) for colour in range(3) for edge in EDGES]
    + [(shore, label, site) for shore in ("p", "s")
       for label in (1, 2) for site in SITES]
)

Coordinate = tuple[object, ...]
Support = frozenset[Coordinate]
Fibre = tuple[object, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def coordinate_key(coordinate: Coordinate) -> str:
    if coordinate[0] == "q":
        _kind, colour, physical = coordinate
        left, right = physical
        return f"q{left}{right}:{colour}{colour}"
    shore, label, site = coordinate
    return f"{shore}{label}@{site}:{label}"


def support_key(support: Support) -> tuple[str, ...]:
    return tuple(sorted(map(coordinate_key, support)))


def fibre_label(fibre: Fibre) -> str:
    if fibre[0] == "q3":
        return "q3@" + "".join(map(str, fibre[1]))
    _kind, left, right, word = fibre
    return f"G{left}{right}@" + "".join(map(str, word))


def is_target_fibre(fibre: Fibre) -> bool:
    if fibre[0] == "q3":
        return fibre[1] == (0,) * 6
    _kind, left, right, word = fibre
    return left == right and word == (left,) * 6


def all_matching_terms() -> dict[Fibre, tuple[Support, ...]]:
    """Build every axis-purified matching monomial, grouped by output."""
    by_fibre: defaultdict[Fibre, list[Support]] = defaultdict(list)

    # 15 physical matchings times 3^3 diagonal decorations.
    for matching in perfect_matchings(SITES):
        for colours in product(range(3), repeat=3):
            word: list[int | None] = [None] * 6
            support = []
            for physical, colour in zip(matching, colours, strict=True):
                word[physical[0]] = word[physical[1]] = colour
                support.append(("q", colour, physical))
            by_fibre[("q3", tuple(word))].append(frozenset(support))

    # For each response row: 30 ordered endpoint holes, 3 residual
    # matchings, and 3^2 diagonal q decorations.
    for left_label, right_label in product((1, 2), repeat=2):
        for left_site in SITES:
            for right_site in SITES:
                if left_site == right_site:
                    continue
                residual = tuple(site for site in SITES
                                 if site not in (left_site, right_site))
                for matching in perfect_matchings(residual):
                    for colours in product(range(3), repeat=2):
                        word: list[int | None] = [None] * 6
                        word[left_site] = left_label
                        word[right_site] = right_label
                        support: list[Coordinate] = [
                            ("p", left_label, left_site),
                            ("s", right_label, right_site),
                        ]
                        for physical, colour in zip(
                                matching, colours, strict=True):
                            word[physical[0]] = word[physical[1]] = colour
                            support.append(("q", colour, physical))
                        by_fibre[("G", left_label, right_label,
                                  tuple(word))].append(frozenset(support))

    answer = {fibre: tuple(terms) for fibre, terms in by_fibre.items()}
    require(sum(map(len, answer.values())) == 3645,
            "the global matching-monomial count changed")
    require(len(answer) == 849, "the output-fibre count changed")
    return answer


def target_skeletons() -> tuple[Support, ...]:
    """Enumerate the 8,100 skeletons containing one term per target."""
    skeletons = set()
    matchings = perfect_matchings(SITES)
    for matching1 in matchings:
        for endpoint_edge1 in matching1:
            tail1 = set(matching1) - {endpoint_edge1}
            for p1, s1 in (endpoint_edge1, endpoint_edge1[::-1]):
                for matching2 in matchings:
                    for endpoint_edge2 in matching2:
                        tail2 = set(matching2) - {endpoint_edge2}
                        for p2, s2 in (endpoint_edge2,
                                       endpoint_edge2[::-1]):
                            skeletons.add(frozenset(
                                {("q", 0, physical) for physical in F0}
                                | {("q", 1, physical) for physical in tail1}
                                | {("q", 2, physical) for physical in tail2}
                                | {("p", 1, p1), ("s", 1, s1),
                                   ("p", 2, p2), ("s", 2, s2)}
                            ))
    answer = tuple(sorted(skeletons, key=support_key))
    require(len(answer) == 8100, "the target-skeleton count changed")
    require(all(len(skeleton) == 11 for skeleton in answer),
            "a target skeleton lost the sharp support size")
    return answer


def f0_stabilizer() -> tuple[tuple[int, ...], ...]:
    answer = []
    for permutation in permutations(SITES):
        image = frozenset(edge(permutation[left], permutation[right])
                          for left, right in F0)
        if image == F0:
            answer.append(permutation)
    require(len(answer) == 48, "the F0 stabilizer order changed")
    return tuple(answer)


def transport_coordinate(
    coordinate: Coordinate, permutation: tuple[int, ...]
) -> Coordinate:
    if coordinate[0] == "q":
        _kind, colour, physical = coordinate
        return ("q", colour,
                edge(permutation[physical[0]], permutation[physical[1]]))
    shore, label, site = coordinate
    return (shore, label, permutation[site])


def skeleton_orbit_representatives(
    skeletons: tuple[Support, ...]
) -> tuple[Support, ...]:
    group = f0_stabilizer()
    unseen = set(skeletons)
    representatives = []
    while unseen:
        skeleton = min(unseen, key=support_key)
        orbit = {
            frozenset(transport_coordinate(coordinate, permutation)
                      for coordinate in skeleton)
            for permutation in group
        }
        require(orbit <= set(skeletons),
                "an F0 transport left the skeleton set")
        unseen -= orbit
        representatives.append(min(orbit, key=support_key))
    answer = tuple(sorted(representatives, key=support_key))
    require(len(answer) == 185,
            "the target-skeleton orbit count changed")
    return answer


def fibre_count(terms: tuple[Support, ...], support: Support) -> int:
    return sum(term <= support for term in terms)


def bad_fibres(
    terms_by_fibre: dict[Fibre, tuple[Support, ...]], support: Support
) -> tuple[Fibre, ...]:
    bad = []
    for fibre, terms in terms_by_fibre.items():
        count = fibre_count(terms, support)
        if (is_target_fibre(fibre) and count == 0) \
                or (not is_target_fibre(fibre) and count == 1):
            bad.append(fibre)
    return tuple(sorted(bad, key=fibre_label))


def minimal_options(options: list[Support]) -> tuple[Support, ...]:
    answer = []
    for option in sorted(set(options),
                         key=lambda item: (len(item), support_key(item))):
        if not any(old <= option for old in answer):
            answer.append(option)
    return tuple(answer)


def singleton_repair_constraints(
    terms_by_fibre: dict[Fibre, tuple[Support, ...]],
    skeleton: Support,
    budget: int,
) -> tuple[tuple[Support, ...], ...]:
    constraints = []
    for fibre, terms in terms_by_fibre.items():
        if is_target_fibre(fibre) or fibre_count(terms, skeleton) != 1:
            continue
        options = [term - skeleton for term in terms
                   if term - skeleton and len(term - skeleton) <= budget]
        constraints.append(minimal_options(options))
    require(constraints, "a skeleton unexpectedly has no singleton lock")
    return tuple(constraints)


def solve_repair_constraints(
    constraints: tuple[tuple[Support, ...], ...], budget: int
) -> tuple[Support, ...]:
    """Return minimal unions which repair every old singleton fibre."""
    visited: set[Support] = set()
    solutions: set[Support] = set()

    def visit(chosen: Support) -> None:
        if chosen in visited:
            return
        visited.add(chosen)
        unsatisfied = [constraint for constraint in constraints
                       if not any(option <= chosen for option in constraint)]
        if not unsatisfied:
            solutions.add(chosen)
            return

        scored = []
        for constraint in unsatisfied:
            feasible = [option for option in constraint
                        if len(chosen | option) <= budget]
            if not feasible:
                return
            scored.append((len(feasible),
                           sum(len(chosen | option) for option in feasible),
                           feasible))
        feasible = min(scored, key=lambda item: (item[0], item[1]))[2]
        for option in feasible:
            visit(chosen | option)

    visit(frozenset())
    return tuple(sorted(solutions,
                        key=lambda item: (len(item), support_key(item))))


def row_family(fibre: Fibre) -> str:
    return "q3" if fibre[0] == "q3" else f"G{fibre[1]}{fibre[2]}"


def cancellation_support_audit() -> dict[str, object]:
    terms_by_fibre = all_matching_terms()
    skeletons = target_skeletons()
    representatives = skeleton_orbit_representatives(skeletons)

    survivor_orbits = {}
    solution_counts = {}
    solutions_by_representative: dict[int, tuple[Support, ...]] = {}
    for budget in range(6):
        survivors = 0
        solutions = 0
        for index, skeleton in enumerate(representatives):
            constraints = singleton_repair_constraints(
                terms_by_fibre, skeleton, budget)
            repairs = solve_repair_constraints(constraints, budget)
            if repairs:
                survivors += 1
                solutions += len(repairs)
                if budget == 5:
                    solutions_by_representative[index] = repairs
        survivor_orbits[str(budget)] = survivors
        solution_counts[str(budget)] = solutions

    require(survivor_orbits == {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 21, "5": 21,
    }, ("the skeleton-repair survivor census changed", survivor_orbits))
    require(solution_counts == {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 98, "5": 98,
    }, ("the skeleton-repair solution census changed", solution_counts))
    require(all(len(repair) == 4
                for repairs in solutions_by_representative.values()
                for repair in repairs),
            "a five-coordinate repair ceased to contain a four-cell core")

    # Size 15: every possible old-singleton repair is one of the 98 cores.
    size15 = []
    for index, repairs in solutions_by_representative.items():
        skeleton = representatives[index]
        for repair in repairs:
            size15.append((index, skeleton | repair))
    require(len(size15) == 98,
            "the size-15 candidate placement count changed")

    bad15_histogram = Counter()
    bad15_families = Counter()
    for _index, support in size15:
        bad = bad_fibres(terms_by_fibre, support)
        require(bad, "a size-15 support became cancellation-compatible")
        bad15_histogram[len(bad)] += 1
        bad15_families.update(map(row_family, bad))

    # Size 16: a solution must contain one of the same four-cell repair
    # cores plus one arbitrary new coordinate.  Deduplicate within each
    # skeleton orbit before checking all full fibres.
    size16 = set()
    for index, repairs in solutions_by_representative.items():
        skeleton = representatives[index]
        for repair in repairs:
            for extra in ALL_COORDINATES - skeleton - repair:
                size16.add((index, skeleton | repair | {extra}))
    require(len(size16) == 5292,
            "the size-16 candidate placement count changed")

    bad16_histogram = Counter()
    bad16_families = Counter()
    best16: tuple[int, int, Support, tuple[Fibre, ...]] | None = None
    for index, support in size16:
        bad = bad_fibres(terms_by_fibre, support)
        require(bad, "a size-16 support became cancellation-compatible")
        bad16_histogram[len(bad)] += 1
        bad16_families.update(map(row_family, bad))
        record = (len(bad), index, support, bad)
        if best16 is None or (record[0], record[1], support_key(record[2])) \
                < (best16[0], best16[1], support_key(best16[2])):
            best16 = record
    require(best16 is not None and best16[0] == 5,
            "the closest size-16 guard changed")

    return {
        "axis_coordinate_universe": len(ALL_COORDINATES),
        "matching_monomials": sum(map(len, terms_by_fibre.values())),
        "output_fibres": len(terms_by_fibre),
        "target_skeletons_with_F0_fixed": len(skeletons),
        "F0_stabilizer_order": len(f0_stabilizer()),
        "target_skeleton_orbits": len(representatives),
        "added_coordinate_budget": list(range(6)),
        "old_singleton_repair_survivor_orbits": survivor_orbits,
        "minimal_repair_core_counts": solution_counts,
        "size15": {
            "candidate_placements_after_old_lock_repair": len(size15),
            "cancellation_compatible": 0,
            "new_singleton_count_histogram": dict(sorted(bad15_histogram.items())),
            "new_singletons_by_row_family": dict(sorted(bad15_families.items())),
        },
        "size16": {
            "candidate_placements_after_old_lock_repair": len(size16),
            "cancellation_compatible": 0,
            "new_singleton_count_histogram": dict(sorted(bad16_histogram.items())),
            "new_singletons_by_row_family": dict(sorted(bad16_families.items())),
            "closest_guard": {
                "remaining_singletons": best16[0],
                "skeleton_orbit": best16[1],
                "support": list(support_key(best16[2])),
                "singleton_fibres": list(map(fibre_label, best16[3])),
            },
        },
        "exact_support_lower_bound": 17,
        "proof": (
            "every nonzero target coefficient contains a target monomial, "
            "hence one of the enumerated skeletons after site relabelling; "
            "an exact zero coefficient cannot have a singleton monomial "
            "fibre over a field.  No skeleton plus at most five coordinates "
            "passes this necessary condition."
        ),
    }


def extremal_and_circuit_scope() -> dict[str, object]:
    return {
        "direct_block": (
            "q^[3]=X0 makes every direct coefficient in G11,G12,G21,G22 "
            "visible at residual word 000000; axis endpoint responses cannot "
            "occupy that word, so the four direct coefficients are zero"
        ),
        "toric_switch": (
            "two monomials in one zero fibre differ by alternating matching "
            "cycles and admit a fibrewise binomial resize, but the other four "
            "tensors are its exact cycle lock"
        ),
        "finite_cascade": (
            "the first 98 four-coordinate repair cores cancel every lock on "
            "their chosen target skeleton, yet create new singleton unary or "
            "response fibres; a fifth coordinate still leaves at least five"
        ),
        "maximum_anchor_minimum_support": (
            "the lower bound holds for every axis-purified exact source and "
            "does not use extremality.  At a lexicographic minimizer it means "
            "the occupied >16 support must carry genuine coupled circuits. "
            "No support-lowering switch is inferred until its complete five-"
            "row lock is shown to vanish or land in an existing carrier."
        ),
        "remaining_theorem": (
            "for supports of size at least 17, prove that the coupled "
            "matching-fibre circuit hypergraph has an anchor-safe toric "
            "direction, or that one nonzero cycle lock supplies a unit, "
            "literal coloop, or active common-q carrier"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 axis-purified cancellation support lower bound",
        "pins": PINS,
        "finite_support_audit": cancellation_support_audit(),
        "extremal_and_circuit_scope": extremal_and_circuit_scope(),
        "verdict": (
            "the larger axis-purified branch has no full-source-compatible "
            "support through 16 decorated coordinates.  The first 98 "
            "matching-circuit repair cores do not close: they merely move "
            "the obstruction to new singleton full-row locks.  Thus any "
            "hypothetical exact axis source has support at least 17; the "
            "remaining issue is a coupled-circuit support-lowering or "
            "unit/coloop/active-carrier theorem, not a one-cycle switch."
        ),
        "scope": (
            "canonical h=3 axis-purified five-tensor one-bad equations over "
            "a field.  This is a necessary support-fibre census, not a "
            "construction at support 17 or an emptiness proof for the full "
            "ternary source locus."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    finite = ledger["finite_support_audit"]
    print("axis-pure target skeletons: 8100 / symmetry orbits: 185")
    print("repair cores at +4 coordinates: 98")
    print("support 15 compatible: 0 / support 16 compatible: 0")
    print("exact axis-pure support lower bound: >=17")
    print("first circuit layer: NEW SINGLETON FULL-ROW LOCKS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
