#!/usr/bin/env python3
"""Audit physical matching/naturality of the hyperbolic root returns.

The four first collision faces are

    D*s1, p0*q01, D*s0, p1*q01

times a perfect-matching tail on the fixed residual window.  Each is a
two-edge star on the operation ports P,S,0,1: one port is missing and one
is doubled.  A tail-preserving squarefree one-arm repair is forced to
replace one of the two star arms.  There are exactly two repairs.  They are
A/B for the first root pair and A/C for the second, where

    A=D*q01=PS|01, B=p0*s1=P0|S1, C=p1*s0=P1|S0.

This checker proves the resolution uniformly over tail sizes through six
vertices and checks restriction/reinsertion naturality.  At h=3 it audits
all twelve collision occurrences (four sectors times three tails), their
48 first-PP flags, and the exact oriented/signless return.

The positive matching routing does not itself make a physical source cell.
Collision monomials have a missing/doubled vertex degree and are disjoint
from all 105 perfect-matching monomials on the eight augmented vertices.
Thus the smallest guard is one collision star plus its two physical repairs:
the repairs exist, but the collision coordinate remains detected.  A full
root-return construction needs four tail-natural collision Tate families
and their complete PP/AugP2/augmented faces.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py":
        "f52c7a8b447a63ee34b3b41e7bbab713409366e7a5a1a16087032a205da2fa9f",
    "notes/h3-balanced-c4-hyperbolic-root-return-gate.md":
        "c4fcd6505401b413bb45aa5fcdc2e3e04f7e38d555250c3cfbee7c643fe1cbcc",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "notes/h3-fixed-window-centered-k22-physical-routing-gate.md":
        "73147addd04f69ea5a6a21e408dbd7030cd449f0cebbe46bb35caa2c32d6c189",
    "computations/verify_uniform_shear_collision_p3k2_augp2_grade_gate.py":
        "a68dd835badb415454ed43186a68c82ee5f699eb118b0575014babf728a7c2bf",
    "notes/uniform-shear-collision-p3k2-augp2-grade-gate.md":
        "d2968439dbc821510cf254c06a580b5205da53668ffd666fb54f6f9f9d7c204d",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "notes/h3-shear-collision-augp2-packaging-map-gate.md":
        "9d5918605dd94d08d18c099966e5956fa0f1c62855b97fd81bf9ada54f2f45ad",
}
EXPECTED_LEDGER_SHA256 = (
    "354f38f45d4ac0de09b8f2fe1fe2efb0d54a40ac2ddadf5ad85694636e924e52"
)


PORTS = ("P", "S", "0", "1")
ORDER = {label: index for index, label in enumerate(
    PORTS + tuple(str(value) for value in range(2, 12))
)}
Edge = tuple[str, str]
Monomial = tuple[Edge, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: str, right: str) -> Edge:
    require(left != right, ("loop", left))
    return ((left, right) if ORDER[left] < ORDER[right]
            else (right, left))


def monomial(*edges: Edge) -> Monomial:
    return tuple(sorted(edges, key=lambda value: (ORDER[value[0]],
                                                   ORDER[value[1]])))


def perfect_matchings(vertices: tuple[str, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield monomial(edge(first, second), *tail)


def degree(value: Monomial, vertices: tuple[str, ...]) -> tuple[int, ...]:
    count = Counter(site for item in value for site in item)
    return tuple(count[site] for site in vertices)


def is_perfect(value: Monomial, vertices: tuple[str, ...]) -> bool:
    return degree(value, vertices) == (1,) * len(vertices)


def collision_signature(value: Monomial, vertices: tuple[str, ...]):
    degrees = degree(value, vertices)
    missing = tuple(vertices[index] for index, item in enumerate(degrees)
                    if item == 0)
    doubled = tuple(vertices[index] for index, item in enumerate(degrees)
                    if item == 2)
    require(len(missing) == len(doubled) == 1
            and sorted(degrees) == [0] + [1] * (len(vertices) - 2) + [2],
            ("not a one-missing/one-doubled collision", value, degrees))
    return missing[0], doubled[0], degrees


def repair_collision(value: Monomial, vertices: tuple[str, ...]):
    missing, doubled, _degrees = collision_signature(value, vertices)
    incident = tuple(item for item in value if doubled in item)
    require(len(incident) == 2, ("doubled incidence", doubled, incident))
    repairs = []
    for old in incident:
        other = old[1] if old[0] == doubled else old[0]
        remaining = list(value)
        remaining.remove(old)
        repaired = monomial(*remaining, edge(missing, other))
        require(is_perfect(repaired, vertices),
                ("one-arm repair is not squarefree", value, repaired))
        repairs.append(repaired)
    require(len(set(repairs)) == 2, "collision repairs coalesced")
    return tuple(sorted(repairs, key=repr))


LOCAL = {
    "A=D*q01": monomial(edge("P", "S"), edge("0", "1")),
    "B=p0*s1": monomial(edge("P", "0"), edge("S", "1")),
    "C=p1*s0": monomial(edge("P", "1"), edge("S", "0")),
}
COLLISIONS = (
    {
        "name": "forward_01=-D*s1",
        "local": monomial(edge("P", "S"), edge("S", "1")),
        "endpoints": ("A=D*q01", "B=p0*s1"),
        "missing": "0", "doubled": "S", "root_pair": "0<->1",
    },
    {
        "name": "reverse_01=p0*q01",
        "local": monomial(edge("P", "0"), edge("0", "1")),
        "endpoints": ("A=D*q01", "B=p0*s1"),
        "missing": "S", "doubled": "0", "root_pair": "0<->1",
    },
    {
        "name": "forward_02=-D*s0",
        "local": monomial(edge("P", "S"), edge("S", "0")),
        "endpoints": ("A=D*q01", "C=p1*s0"),
        "missing": "1", "doubled": "S", "root_pair": "0<->2",
    },
    {
        "name": "reverse_02=p1*q01",
        "local": monomial(edge("P", "1"), edge("0", "1")),
        "endpoints": ("A=D*q01", "C=p1*s0"),
        "missing": "S", "doubled": "1", "root_pair": "0<->2",
    },
)

PARENT_CONTRIBUTIONS = {
    # (squarefree parent, coefficient of its first root face).  The two
    # parent contributions collect to zero in the complete response.
    "forward_01=-D*s1": (("A=D*q01", Q(-1)), ("B=p0*s1", Q(1))),
    "reverse_01=p0*q01": (("A=D*q01", Q(1)), ("B=p0*s1", Q(-1))),
    "forward_02=-D*s0": (("A=D*q01", Q(-1)), ("C=p1*s0", Q(1))),
    "reverse_02=p1*q01": (("A=D*q01", Q(1)), ("C=p1*s0", Q(-1))),
}


def odd_double_factorial(value: int) -> int:
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def combine(local: Monomial, tail: Monomial) -> Monomial:
    return monomial(*local, *tail)


def symmetric_difference_cycle(left: Monomial, right: Monomial):
    difference = set(left).symmetric_difference(right)
    incidence = Counter(site for item in difference for site in item)
    return difference, incidence


def audit_tail_order(tail_vertices: int):
    require(tail_vertices % 2 == 0 and 0 <= tail_vertices <= 6,
            tail_vertices)
    tail_sites = tuple(str(value) for value in range(2, 2 + tail_vertices))
    tails = tuple(perfect_matchings(tail_sites))
    require(len(tails) == odd_double_factorial(tail_vertices - 1),
            (tail_vertices, len(tails)))
    vertices = PORTS + tail_sites
    records = []
    sectors = set()
    outside_tail_edges = 0
    for collision in COLLISIONS:
        for tail in tails:
            value = combine(collision["local"], tail)
            missing, doubled, degrees = collision_signature(value, vertices)
            require((missing, doubled)
                    == (collision["missing"], collision["doubled"]),
                    (collision["name"], missing, doubled))
            sectors.add(degrees)
            repairs = repair_collision(value, vertices)
            expected = tuple(sorted((
                combine(LOCAL[name], tail)
                for name in collision["endpoints"]
            ), key=repr))
            require(repairs == expected,
                    ("fixed-tail repairs changed", collision["name"], tail,
                     repairs, expected))
            for repaired in repairs:
                added = set(repaired) - set(value)
                outside_tail_edges += sum(
                    1 for item in added if any(site in tail_sites for site in item)
                )
            difference, incidence = symmetric_difference_cycle(*repairs)
            require(len(difference) == 4
                    and set(incidence) == set(PORTS)
                    and set(incidence.values()) == {2},
                    ("repair endpoints lost the operation C4", repairs,
                     difference, incidence))

            # Removing a common tail edge before resolving commutes with
            # resolving and then removing it.  This is the literal
            # restriction law; reinsertion is the reverse equality.
            for tail_edge in tail:
                restricted_collision = monomial(*(
                    item for item in value if item != tail_edge
                ))
                restricted_vertices = tuple(
                    site for site in vertices if site not in tail_edge
                )
                restricted_repairs = repair_collision(
                    restricted_collision, restricted_vertices
                )
                expected_restriction = tuple(sorted((
                    monomial(*(item for item in repaired
                               if item != tail_edge))
                    for repaired in repairs
                ), key=repr))
                require(restricted_repairs == expected_restriction,
                        ("restriction stopped commuting with repair",
                         collision["name"], tail_edge))
            records.append((collision["name"], tail, repairs))
    require(outside_tail_edges == 0,
            "a collision repair entered the residual tail fan")
    # Four collision types have distinct operation-port degree sectors.
    require(len(sectors) == len(COLLISIONS),
            ("collision fine sectors coalesced", tail_vertices, sectors))
    return {
        "tail_vertices": tail_vertices,
        "tail_matchings": len(tails),
        "collision_occurrences": len(records),
        "repairs_per_collision": 2,
        "repair_C4_ports": list(PORTS),
        "outside_tail_edges_introduced": outside_tail_edges,
        "restriction_reinsertion_natural": True,
        "distinct_collision_degree_sectors": len(sectors),
    }


def audit_h3_fixed_window():
    tail_sites = ("2", "3", "4", "5")
    tails = tuple(perfect_matchings(tail_sites))
    require(tuple(map(repr, tails)) == tuple(map(repr, (
        monomial(edge("2", "3"), edge("4", "5")),
        monomial(edge("2", "4"), edge("3", "5")),
        monomial(edge("2", "5"), edge("3", "4")),
    ))), ("h3 tail order changed", tails))
    vertices = PORTS + tail_sites
    collision_values = []
    pp_flags = []
    pp_types = Counter()
    pp_monomials = {"3K2": set(), "P3+K2": set()}
    collected_3k2 = Counter()
    examples = []
    for collision in COLLISIONS:
        for tail in tails:
            value = combine(collision["local"], tail)
            collision_values.append(value)
            _missing, doubled, _degrees = collision_signature(value, vertices)
            repairs = repair_collision(value, vertices)
            examples.append({
                "collision": collision["name"],
                "tail": ["".join(item) for item in tail],
                "repairs": [["".join(item) for item in repair]
                            for repair in repairs],
            })
            for removed in value:
                face = monomial(*(item for item in value if item != removed))
                face_type = "3K2" if doubled in removed else "P3+K2"
                # Removing an arm through the doubled vertex leaves three
                # disjoint edges.  Removing one tail edge retains the P3.
                degrees = degree(face, vertices)
                if face_type == "3K2":
                    require(max(degrees) == 1,
                            ("3K2 face still collided", collision, face))
                else:
                    require(max(degrees) == 2,
                            ("P3+K2 face lost its collision", collision, face))
                pp_flags.append((value, removed, face))
                pp_types[face_type] += 1
                pp_monomials[face_type].add(face)
                if face_type == "3K2":
                    collected_3k2[face] += PARENT_CONTRIBUTIONS[
                        collision["name"]
                    ][0][1]
    require(len(collision_values) == 12
            and len(set(collision_values)) == 12
            and len(pp_flags) == 48
            and pp_types == Counter({"3K2": 24, "P3+K2": 24})
            and {key: len(value) for key, value in pp_monomials.items()}
            == {"3K2": 18, "P3+K2": 24}
            and Counter(collected_3k2.values())
            == Counter({Q(-1): 6, Q(1): 6, Q(-2): 3, Q(2): 3}),
            ("h3 collision/PP census changed", len(collision_values),
             len(pp_flags), pp_types,
             {key: len(value) for key, value in pp_monomials.items()}))
    return {
        "fixed_window": [2, 3, 4, 5],
        "tail_matchings": [["".join(item) for item in tail]
                           for tail in tails],
        "collision_families": [collision["name"]
                               for collision in COLLISIONS],
        "collision_occurrences": len(collision_values),
        "all_collision_occurrences_distinct": True,
        "first_PP_flags": len(pp_flags),
        "first_PP_split": dict(pp_types),
        "distinct_PP_monomials": {
            key: len(value) for key, value in pp_monomials.items()
        },
        "shared_3K2_monomials": 6,
        "shared_3K2_multiplicity": 2,
        "selected_path_signed_3K2_coefficient_histogram": {
            "-2": 3, "-1": 6, "1": 6, "2": 3,
        },
        "sample_repairs": examples[:4],
        "full_boundary_warning": (
            "each collision family has six tail-removal P3+K2 faces and "
            "six star-arm-removal 3K2 flags; six pairs of the latter collect "
            "to the same unlabelled monomial with equal, not cancelling, "
            "selected-path signs"
        ),
    }


def matrix_rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def audit_parent_collection_guard():
    records = []
    for collision in COLLISIONS:
        parents = PARENT_CONTRIBUTIONS[collision["name"]]
        require(tuple(name for name, _coefficient in parents)
                == collision["endpoints"],
                ("collision parents stopped matching its repairs",
                 collision["name"], parents, collision["endpoints"]))
        split = tuple(coefficient for _name, coefficient in parents)
        require(sum(split, Q(0)) == 0 and split[0] == -split[1]
                and split[0] != 0,
                ("complete response stopped cancelling a collision", parents))
        records.append({
            "collision": collision["name"],
            "two_squarefree_parents": [name for name, _value in parents],
            "root_face_coefficients": [str(value) for _name, value in parents],
            "collected_collision_coefficient": "0",
            "required_occurrence_class": "parent anti-diagonal",
        })

    # Collection Q^2 -> Q is block diagonal over the four collision sectors.
    # It has rank four and a four-dimensional occurrence kernel, spanned by
    # the four root anti-diagonals.  Tensoring with the three h3 tails gives
    # rank 12 and kernel dimension 12.
    collection_columns = []
    for block in range(len(COLLISIONS)):
        left = [Q(0)] * len(COLLISIONS)
        right = [Q(0)] * len(COLLISIONS)
        left[block] = right[block] = Q(1)
        collection_columns.extend((tuple(left), tuple(right)))
    require(matrix_rank(tuple(collection_columns)) == len(COLLISIONS),
            "four-sector parent collection rank changed")
    for block, collision in enumerate(COLLISIONS):
        split = tuple(value for _name, value in
                      PARENT_CONTRIBUTIONS[collision["name"]])
        collected = tuple(
            split[0] * collection_columns[2 * block][row]
            + split[1] * collection_columns[2 * block + 1][row]
            for row in range(len(COLLISIONS))
        )
        require(collected == (Q(0),) * len(COLLISIONS),
                "a root parent anti-diagonal survived collection")
    return {
        "parent_tables": records,
        "one_sector_collection": "Q{parent A}+Q{parent B/C} -> Q{collision}",
        "one_sector_kernel": "Q*(parent_left-parent_right)",
        "four_sector_collection_rank_kernel": [4, 4],
        "h3_three_tail_collection_rank_kernel": [12, 12],
        "exact_naturality_gap": (
            "the complete response contains both parents and its first root "
            "faces cancel after collision collection.  The hyperbolic return "
            "requires the anti-diagonal parent occurrence class.  A physical "
            "construction must retain that class in an occurrence-labelled "
            "relative collision splitter; an unlabelled coefficient row "
            "cannot recover it"
        ),
    }


def audit_return_signs():
    response = (Q(1), Q(1), Q(1))
    oriented_ab = (Q(1), Q(-1), Q(0))
    oriented_ac = (Q(1), Q(0), Q(-1))
    balanced = (Q(2), Q(-1), Q(-1))
    require(tuple(a + b for a, b in zip(
        oriented_ab, oriented_ac, strict=True
    )) == balanced, "opposite-root returns stopped summing to L")
    shore_gauge = (Q(1), Q(-1), Q(-1))
    signless_ab = tuple(a * b for a, b in zip(
        shore_gauge, oriented_ab, strict=True
    ))
    signless_ac = tuple(a * b for a, b in zip(
        shore_gauge, oriented_ac, strict=True
    ))
    require(signless_ab == (Q(1), Q(1), Q(0))
            and signless_ac == (Q(1), Q(0), Q(1)),
            "the root-return/signless-mate gauge changed")
    require(matrix_rank((response, signless_ab)) == 2
            and matrix_rank((response, signless_ab, balanced)) == 3
            and matrix_rank((response, signless_ac)) == 2
            and matrix_rank((response, signless_ac, balanced)) == 3
            and matrix_rank((response, signless_ab, signless_ac)) == 3,
            "the two-switch necessity/sufficiency ranks changed")
    exact = tuple(-4 * response[index]
                  + 3 * signless_ab[index] + 3 * signless_ac[index]
                  for index in range(3))
    require(exact == balanced, "the signless physical projection changed")
    gauged_balanced = tuple(shore_gauge[index] * balanced[index]
                            for index in range(3))
    require(gauged_balanced == (Q(2), Q(1), Q(1))
            and sum(gauged_balanced, Q(0)) == 4,
            "the returned charge stopped being noncentered after gauge")
    return {
        "oriented_returns": ["A-B", "A-C"],
        "return_sum": "2A-B-C",
        "shore_sign_gauge": [1, -1, -1],
        "signless_mate_families": ["A+B", "A+C"],
        "one_family_plus_response_projects_L": False,
        "both_families_plus_response_project_L": True,
        "exact_signless_projection":
            "L=-4*(A+B+C)+3*(A+B)+3*(A+C)",
        "gauged_L": [str(value) for value in gauged_balanced],
        "gauged_augmentation": "4",
    }


def audit_squarefree_source_guard():
    vertices = PORTS + ("2", "3", "4", "5")
    physical = tuple(perfect_matchings(vertices))
    tails = tuple(perfect_matchings(("2", "3", "4", "5")))
    collisions = tuple(combine(spec["local"], tail)
                       for spec in COLLISIONS for tail in tails)
    require(len(physical) == 105 and len(set(physical)) == 105
            and len(collisions) == 12 and len(set(collisions)) == 12,
            "the squarefree/collision source census changed")
    require(set(physical).isdisjoint(collisions)
            and all(is_perfect(value, vertices) for value in physical)
            and all(not is_perfect(value, vertices) for value in collisions),
            "a collision entered the physical matching module")

    # All monomials have distinct exponent coordinates, so rank is support
    # cardinality.  Adding the two physical repairs of a collision changes
    # nothing: they were already among the 105 matching occurrences.  Adding
    # the collision itself raises rank by one and is detected by its private
    # missing/doubled-degree coordinate.
    smallest = combine(
        next(spec["local"] for spec in COLLISIONS
             if spec["name"] == "forward_01=-D*s1"),
        monomial(edge("2", "3"), edge("4", "5")),
    )
    repairs = repair_collision(smallest, vertices)
    require(all(repair in physical for repair in repairs)
            and smallest not in physical,
            "the smallest collision guard changed")
    return {
        "augmented_vertices": list(vertices),
        "physical_perfect_matching_monomials": len(physical),
        "h3_selected_collision_monomials": len(collisions),
        "physical_plus_all_collision_rank": len(physical) + len(collisions),
        "collision_quotient_dimension": len(collisions),
        "smallest_guard": {
            "collision": ["".join(item) for item in smallest],
            "vertex_degree": list(degree(smallest, vertices)),
            "two_physical_repairs": [["".join(item) for item in value]
                                     for value in repairs],
            "collision_detector": (
                "coefficient of the missing-0/doubled-S monomial; zero on "
                "all 105 perfect matchings and one on this collision"
            ),
        },
        "logical_boundary": (
            "matching completion determines the endpoints of a collision "
            "Tate cell; it cannot construct the collision cell inside the "
            "squarefree perfect-matching source module"
        ),
    }


def audit():
    pin_dependencies()
    uniform = [audit_tail_order(tail_vertices)
               for tail_vertices in (0, 2, 4, 6)]
    ledger = {
        "theorem": "hyperbolic collision fixed-window matching routing gate",
        "pins": PINS,
        "uniform_fixed_tail_resolution": uniform,
        "h3_fixed_window": audit_h3_fixed_window(),
        "complete_response_parent_collection":
            audit_parent_collection_guard(),
        "root_return_to_required_switches": audit_return_signs(),
        "smallest_exact_source_guard": audit_squarefree_source_guard(),
        "positive_routing_theorem": (
            "For any perfect-matching tail T disjoint from P,S,0,1, each "
            "of the four hyperbolic collision stars has exactly two "
            "tail-preserving squarefree one-arm repairs.  They are A*T and "
            "B*T for root 0<->1, and A*T and C*T for root 0<->2.  The repair "
            "C4 is always the fixed operation port set P,S,0,1, introduces "
            "no residual-tail edge, and commutes with every common-tail "
            "restriction and reinsertion.  With the shore sign gauge, the "
            "two oriented returns are exactly the required A+B and A+C "
            "families and their sum carries nonzero augmentation"
        ),
        "physical_failure": (
            "The collision stars themselves are not perfect matchings: "
            "each has one missing and one doubled augmented vertex.  Their "
            "four fine sectors are disjoint from the squarefree source and "
            "from one another.  Moreover each collision has two squarefree "
            "parents whose root contributions cancel in the complete "
            "response; the desired return is their parent anti-diagonal.  "
            "At h=3 the order-natural packet therefore needs four new "
            "occurrence-labelled collision splitters over three tails "
            "(twelve anti-diagonal coordinates), including all 24 P3+K2 "
            "and all 24 sibling 3K2 first-PP flags"
        ),
        "first_missing_full_source_object": (
            "a four-family, tail-natural occurrence-split collision PP "
            "mapping cylinder for "
            "D*s1, p0*q01, D*s0, p1*q01 in response word 11:110000, whose "
            "squarefree return faces are the two switches, whose complete "
            "first boundary retains both P3+K2 and 3K2 halves, and whose "
            "word-changing AugP2 comparison carries reduced Eq, q, anchor, "
            "W, ordinary residue and shifted ridge"
        ),
        "verdict": (
            "Positive at the exact matching-placement level, negative as "
            "an unconditional physical source construction.  No outside "
            "residual fan or port wandering is forced: the unique repairs "
            "land exactly A/B and A/C on the common operation C4.  But the "
            "missing/doubled collision top is outside the squarefree source "
            "module.  If its four natural Tate families are constructed, "
            "the returned noncentered charge fills the 0d3f6d4 gate; if "
            "they are absent from the exhaustive full map, any one of the "
            "twelve primitive parent-anti-diagonal collision duals is a "
            "terminal guard"
        ),
        "scope": (
            "exact augmented-port matching algebra and first labelled PP "
            "boundary at canonical h=3, with a uniform tail theorem through "
            "six residual vertices.  The checker does not construct the "
            "cross-word AugP2/ridge mapping cylinder"
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
    print("four collision stars: UNIQUE FIXED-TAIL A/B AND A/C REPAIRS")
    print("restriction/reinsertion: NATURAL; outside residual edges: ZERO")
    print("oriented returns gauge to required A+B and A+C families")
    print("h3 collision tops: 12-DIMENSIONAL OUTSIDE SQUAREFREE SOURCE")
    print("needed: FOUR COLLISION TATE FAMILIES WITH FULL PP/AugP2 FACES")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
