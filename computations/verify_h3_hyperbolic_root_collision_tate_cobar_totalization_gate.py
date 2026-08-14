#!/usr/bin/env python3
"""Audit physical Tate/cobar totalization of the two hyperbolic root squares.

The coefficient identity of a29eb69 uses the four selected collision faces

    -D*s1*H, -D*s0*H, p0*q01*H, p1*q01*H.

This checker restores the complete K8 response, the physical six-site unary
row, and every labelled first principal-parts face.  The result is a sharp
three-stage boundary.

* In a complete response row, each displayed three-term collision cancels
  against its adjacent chart.  The root extended only on the six named
  operation coordinates instead leaves a signed 24-term subset of the
  45-term missing/doubled collision sector.  Its centered dual kills the
  complete symmetric collision row and detects the subset.
* On the complete unary row the forward roots give -s1*H and -s0*H, while
  the reverse roots give zero.  The opposite-root orders therefore differ
  by q01*H in each square.  This is a selected three-of-fifteen unary block,
  not the complete unary row.
* Each selected collision top has twelve labelled PP flags: six 3K2
  path-edge cofactors and six P3+K2 tail cofactors.  Across four roots all
  48 labelled flags are distinct.  The forward tail cofactors have DSQ
  operation type, outside the committed DQ/PS/QQ/PQ/SQ lower packets.  The
  reverse PQQ cofactors have only an associated-graded P2 topology and still
  lack the physical word/fine comparison.

Presentation-safe relative graphs retain carriers and preserve H0 at the
response and unary stages, but they carry the displayed duals.  No physical
root pair or accepted terminal is constructed here.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py":
        "f52c7a8b447a63ee34b3b41e7bbab713409366e7a5a1a16087032a205da2fa9f",
    "computations/verify_uniform_chart_unipotent_shear_collision_gate.py":
        "6f05b788400279a8dd19c09acbb1e883eb74c8a9c21f9d00e2bc6a048543922e",
    "computations/verify_uniform_shear_collision_p3k2_augp2_grade_gate.py":
        "a68dd835badb415454ed43186a68c82ee5f699eb118b0575014babf728a7c2bf",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
}
EXPECTED_LEDGER_SHA256 = (
    "369c13561001f6dc4f1f18e1c1dd8543549cec346ebd7fb2f047c1f3ef85d7d4"
)


Edge = tuple[int, int]
Monomial = tuple[Edge, ...]
Polynomial = Counter[Monomial]

NAMES = ("P", "S", "0", "1", "2", "3", "4", "5")
P, S, ZERO, ONE, TWO, THREE, FOUR, FIVE = range(8)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def edge(left: int, right: int) -> Edge:
    return tuple(sorted((left, right)))


def label_edge(value: Edge) -> str:
    left, right = (NAMES[value[0]], NAMES[value[1]])
    if (left, right) == ("P", "S"):
        return "D"
    if left == "P":
        return "p" + right
    if left == "S":
        return "s" + right
    return "q" + left + right


def label_monomial(value: Monomial) -> str:
    return "*".join(label_edge(item) for item in value)


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


def add(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def scale(coefficient: int | Q, polynomial: Polynomial) -> Polynomial:
    answer = Counter({monomial: Q(coefficient) * value
                      for monomial, value in polynomial.items()})
    return Counter({monomial: value for monomial, value in answer.items()
                    if value})


def derivation(polynomial: Polynomial,
               replacements: tuple[tuple[Edge, Q, Edge], ...]) -> Polynomial:
    """Apply a linear edge derivation, retaining polynomial multiplicity."""
    answer: Polynomial = Counter()
    for monomial, coefficient in polynomial.items():
        for position, source in enumerate(monomial):
            for varied, factor, target in replacements:
                if source != varied:
                    continue
                out = list(monomial)
                out[position] = target
                answer[tuple(sorted(out))] += coefficient * factor
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or rows[row][column] == 0:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def vertex_degree(monomial: Monomial) -> tuple[int, ...]:
    degree = [0] * 8
    for left, right in monomial:
        degree[left] += 1
        degree[right] += 1
    return tuple(degree)


def topology(monomial: Monomial) -> str:
    positive = tuple(sorted((value for value in vertex_degree(monomial)
                             if value), reverse=True))
    lookup = {
        (2, 1, 1, 1, 1, 1, 1): "P3+2K2",
        (2, 1, 1, 1, 1): "P3+K2",
        (1, 1, 1, 1, 1, 1): "3K2",
    }
    require(positive in lookup, ("unexpected topology", positive, monomial))
    return lookup[positive]


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


D = edge(P, S)
P0 = edge(P, ZERO)
P1 = edge(P, ONE)
Q01 = edge(ZERO, ONE)
S1 = edge(S, ONE)
S0 = edge(S, ZERO)
TAILS = tuple(perfect_matchings((TWO, THREE, FOUR, FIVE)))
H = Counter({tail: Q(1) for tail in TAILS})
RESPONSE = Counter({matching: Q(1)
                    for matching in perfect_matchings(tuple(range(8)))})
UNARY = Counter({matching: Q(1)
                 for matching in perfect_matchings(
                     (ZERO, ONE, TWO, THREE, FOUR, FIVE))})


ROOTS = (
    {
        "name": "E01",
        "pair": "0<->1",
        "order": "forward",
        "replacements": ((P0, Q(1), D), (Q01, Q(-1), S1)),
        "opposite": "E10",
        "sector": (ZERO, S),
        "selected_head": (D, S1),
        "selected_sign": Q(-1),
        "selected_label": "-D*s1*H",
        "tail_operation": "DSQ",
    },
    {
        "name": "E02",
        "pair": "0<->2",
        "order": "forward",
        "replacements": ((P1, Q(1), D), (Q01, Q(-1), S0)),
        "opposite": "E20",
        "sector": (ONE, S),
        "selected_head": (D, S0),
        "selected_sign": Q(-1),
        "selected_label": "-D*s0*H",
        "tail_operation": "DSQ",
    },
    {
        "name": "E10",
        "pair": "0<->1",
        "order": "reverse",
        "replacements": ((D, Q(1), P0), (S1, Q(-1), Q01)),
        "opposite": "E01",
        "sector": (S, ZERO),
        "selected_head": (P0, Q01),
        "selected_sign": Q(1),
        "selected_label": "+p0*q01*H",
        "tail_operation": "PQQ",
    },
    {
        "name": "E20",
        "pair": "0<->2",
        "order": "reverse",
        "replacements": ((D, Q(1), P1), (S0, Q(-1), Q01)),
        "opposite": "E02",
        "sector": (S, ONE),
        "selected_head": (P1, Q01),
        "selected_sign": Q(1),
        "selected_label": "+p1*q01*H",
        "tail_operation": "PQQ",
    },
)
ROOT_LOOKUP = {record["name"]: record for record in ROOTS}


def selected_polynomial(record: dict[str, object]) -> Polynomial:
    head = tuple(record["selected_head"])
    return Counter({tuple(sorted(head + tail)): Q(record["selected_sign"])
                    for tail in TAILS})


def complete_collision_sector(missing: int, doubled: int) -> Polynomial:
    """The 45-term symmetric collision row C_(missing,doubled)."""
    available = tuple(vertex for vertex in range(8)
                      if vertex not in (missing, doubled))
    answer: Polynomial = Counter()
    for left, right in combinations(available, 2):
        rest = tuple(vertex for vertex in available
                     if vertex not in (left, right))
        for matching in perfect_matchings(rest):
            monomial = tuple(sorted((edge(doubled, left),
                                     edge(doubled, right)) + matching))
            answer[monomial] += 2
    require(len(answer) == 45 and set(answer.values()) == {2},
            (missing, doubled, len(answer), set(answer.values())))
    return answer


def complete_response_root_audit() -> dict[str, object]:
    records = []
    for root in ROOTS:
        derivative = derivation(RESPONSE, root["replacements"])
        selected = selected_polynomial(root)
        sector = complete_collision_sector(*root["sector"])
        require(len(derivative) == 24
                and Counter(derivative.values()) == Counter({Q(1): 12,
                                                               Q(-1): 12}),
                (root["name"], len(derivative), Counter(derivative.values())))
        require(set(derivative).issubset(sector)
                and set(selected).issubset(sector)
                and set(derivative).isdisjoint(selected),
                ("complete response collision placement changed", root["name"]))

        # On the 45 sector coordinates the complete collision is constant 2,
        # while the partial-root residual has twelve +1, twelve -1 and 21
        # zeros.  residual/24 is a primitive rational separator.
        order = tuple(sorted(sector))
        complete_vector = tuple(Q(sector[value]) for value in order)
        residual_vector = tuple(Q(derivative[value]) for value in order)
        dual = tuple(value / 24 for value in residual_vector)
        require(dot(dual, complete_vector) == 0
                and dot(dual, residual_vector) == 1
                and rank((complete_vector, residual_vector)) == 2,
                ("the signed collision separator changed", root["name"]))

        # A monic relative graph t-residual preserves the old sector H0 and
        # forces the separator to take value one on t.
        complete_extended = complete_vector + (Q(0),)
        graph = tuple(-value for value in residual_vector) + (Q(1),)
        old_h0 = 45 - rank((complete_vector,))
        relative_h0 = 46 - rank((complete_extended, graph))
        extended_dual = dual + (Q(1),)
        require((old_h0, relative_h0) == (44, 44)
                and dot(extended_dual, complete_extended) == 0
                and dot(extended_dual, graph) == 0,
                ("the response relative graph changed", root["name"]))
        records.append({
            "root": root["name"],
            "sector_missing_doubled": [NAMES[value]
                                        for value in root["sector"]],
            "selected_internal_face": root["selected_label"],
            "selected_internal_terms": len(selected),
            "selected_coefficient_in_complete_derivative": 0,
            "complete_root_residual_terms": len(derivative),
            "residual_coefficients": {"+1": 12, "-1": 12},
            "symmetric_collision_terms": len(sector),
            "dual_on_symmetric_collision_residual": ["0", "1"],
            "H0_old_relative": [old_h0, relative_h0],
        })
    return {
        "complete_response_terms": len(RESPONSE),
        "records": records,
        "consequence": (
            "the desired three-term collision is an occurrence-relative A-"
            "chart face and cancels in the complete response row.  The "
            "six-coordinate root is not a complete response symmetry: it "
            "leaves a different centered 24-term collision splitter which "
            "the symmetric 45-term collision row cannot absorb"
        ),
    }


def unary_and_commutator_audit() -> dict[str, object]:
    expected_forward = {
        "E01": Counter({tuple(sorted((S1,) + tail)): Q(-1)
                         for tail in TAILS}),
        "E02": Counter({tuple(sorted((S0,) + tail)): Q(-1)
                         for tail in TAILS}),
    }
    q_block = Counter({tuple(sorted((Q01,) + tail)): Q(1)
                       for tail in TAILS})
    records = []
    for root in ROOTS:
        first = derivation(UNARY, root["replacements"])
        if root["order"] == "forward":
            require(first == expected_forward[root["name"]],
                    ("the forward unary collision changed", root["name"], first))
            opposite = ROOT_LOOKUP[root["opposite"]]
            returned = derivation(first, opposite["replacements"])
            reverse_first = derivation(UNARY, opposite["replacements"])
            reverse_return = derivation(reverse_first, root["replacements"])
            require(returned == q_block and not reverse_first
                    and not reverse_return,
                    ("the unary root-order defect changed", root["name"],
                     returned, reverse_first, reverse_return))
            records.append({
                "pair": root["pair"],
                "forward_first_face": "-s1*H" if root["name"] == "E01"
                                      else "-s0*H",
                "forward_first_terms": len(first),
                "reverse_first_face": 0,
                "forward_then_reverse": "q01*H",
                "reverse_then_forward": 0,
                "commutator_Cartan_face": "q01*H",
            })

    # Exact complete-unary occurrence separator.  q01*H has three of the
    # fifteen matching coordinates.  Values 1/3 on the selected block and
    # -1/12 on its complement kill the complete unary row and read one on
    # q01*H.
    order = tuple(sorted(UNARY))
    unary_vector = tuple(Q(1) for _value in order)
    q_vector = tuple(Q(q_block[value]) for value in order)
    dual = tuple(Q(1, 3) if q_block[value] else Q(-1, 12)
                 for value in order)
    require(dot(dual, unary_vector) == 0
            and dot(dual, q_vector) == 1
            and rank((unary_vector, q_vector)) == 2,
            "the selected unary block separator changed")

    unary_extended = unary_vector + (Q(0),)
    graph = tuple(-value for value in q_vector) + (Q(1),)
    extended_dual = dual + (Q(1),)
    old_h0 = 15 - rank((unary_vector,))
    relative_h0 = 16 - rank((unary_extended, graph))
    require((old_h0, relative_h0) == (14, 14)
            and dot(extended_dual, unary_extended) == 0
            and dot(extended_dual, graph) == 0,
            "the unary relative Tate graph changed")
    return {
        "physical_unary_terms": len(UNARY),
        "root_pair_records": records,
        "shared_selected_Cartan_face": "q01*H2345 (3 of 15 unary matchings)",
        "sum_of_two_square_commutators": "2*q01*H2345",
        "primitive_unary_dual": {
            "on_selected_three": "1/3",
            "on_other_twelve": "-1/12",
            "on_complete_unary": 0,
            "on_q01_H": 1,
        },
        "H0_old_relative": [old_h0, relative_h0],
        "first_missing_unary_cell": (
            "an occurrence-local Cartan/restriction cell landing q01*H, "
            "or a retained t_q with a separate physical absolute preimage"
        ),
    }


def collision_pp_boundary_audit() -> dict[str, object]:
    complete_flags = []
    selected_flags = []
    sector_records = []
    known_lower_pairs = {"DQ", "PS", "QQ", "PQ", "SQ"}
    for root in ROOTS:
        sector = complete_collision_sector(*root["sector"])
        selected = selected_polynomial(root)
        sector_counts: Counter[str] = Counter()
        for monomial, coefficient in sector.items():
            for position, removed in enumerate(monomial):
                remainder = monomial[:position] + monomial[position + 1:]
                kind = topology(remainder)
                sector_counts[kind] += 1
                complete_flags.append((root["name"], removed, remainder,
                                       coefficient, kind))
        require(sector_counts == Counter({"3K2": 90, "P3+K2": 90}),
                (root["name"], sector_counts))

        selected_counts: Counter[str] = Counter()
        selected_rows = []
        for monomial, coefficient in selected.items():
            for position, removed in enumerate(monomial):
                remainder = monomial[:position] + monomial[position + 1:]
                kind = topology(remainder)
                selected_counts[kind] += 1
                flag = (root["name"], removed, remainder, coefficient, kind)
                selected_flags.append(flag)
                selected_rows.append({
                    "removed_label": "d" + label_edge(removed),
                    "remainder": label_monomial(remainder),
                    "topology": kind,
                    "coefficient": str(coefficient),
                })
        require(selected_counts == Counter({"3K2": 6, "P3+K2": 6}),
                (root["name"], selected_counts))
        sector_records.append({
            "root": root["name"],
            "selected_top": root["selected_label"],
            "complete_top_terms": len(sector),
            "complete_PP_flags": dict(sorted(sector_counts.items())),
            "selected_PP_flags": dict(sorted(selected_counts.items())),
            "tail_cofactor_operation": root["tail_operation"],
            "tail_pair_in_committed_lower_list": (
                root["tail_operation"] != "DSQ"
            ),
            "selected_faces": selected_rows,
        })

    require(len(complete_flags) == 720
            and len({(name, removed, remainder)
                     for name, removed, remainder, _coefficient, _kind
                     in complete_flags}) == 720,
            "complete collision PP flags lost literal independence")
    require(len(selected_flags) == 48
            and len({(name, removed, remainder)
                     for name, removed, remainder, _coefficient, _kind
                     in selected_flags}) == 48,
            "selected collision PP flags lost literal independence")
    complete_types = Counter(flag[4] for flag in complete_flags)
    selected_types = Counter(flag[4] for flag in selected_flags)
    require(complete_types == Counter({"3K2": 360, "P3+K2": 360})
            and selected_types == Counter({"3K2": 24, "P3+K2": 24}),
            (complete_types, selected_types))

    # Group the complete 3K2 faces.  For sector (a,b), deleting the b-k edge
    # gives the complete fifteen-matching row on V\{a,k}; there are six k.
    # Deleting an edge disjoint from b gives fifteen six-term P3+K2 rows.
    family_records = []
    for root in ROOTS:
        missing, doubled = root["sector"]
        unary_groups: Counter[int] = Counter()
        repeated_groups: Counter[Edge] = Counter()
        for name, removed, _remainder, _coefficient, kind in complete_flags:
            if name != root["name"]:
                continue
            if kind == "3K2":
                require(doubled in removed,
                        ("3K2 face did not delete doubled vertex edge", name))
                other = removed[1] if removed[0] == doubled else removed[0]
                unary_groups[other] += 1
            else:
                require(doubled not in removed,
                        ("P3K2 face deleted doubled vertex edge", name))
                repeated_groups[removed] += 1
        require(len(unary_groups) == 6
                and set(unary_groups.values()) == {15}
                and len(repeated_groups) == 15
                and set(repeated_groups.values()) == {6},
                (root["name"], unary_groups, repeated_groups))
        physical_unary = (missing == S and P in unary_groups)
        family_records.append({
            "root": root["name"],
            "six_unary_cofactor_rows": {
                NAMES[key]: value for key, value in unary_groups.items()
            },
            "fifteen_repeated_PP_rows_each_six_terms": len(repeated_groups),
            "contains_physical_six_site_unary_row": physical_unary,
            "physical_unary_removed_edge": (
                "dp0" if root["name"] == "E10" else
                "dp1" if root["name"] == "E20" else None
            ),
        })

    # The forward DSQ tail cofactors have varied operation pair DS, which is
    # absent from the committed DQ,PS,QQ,PQ,SQ second-Hasse list.  The reverse
    # PQQ cofactors have the P2 associated-graded profile but retain response
    # word 11:110000 rather than the canonical AugP2 word 01211222.
    require("DS" not in known_lower_pairs and "PQ" in known_lower_pairs,
            "the committed lower operation list changed")
    return {
        "complete_labelled_PP_flags": len(complete_flags),
        "complete_type_counts": dict(sorted(complete_types.items())),
        "selected_labelled_PP_flags": len(selected_flags),
        "selected_type_counts": dict(sorted(selected_types.items())),
        "all_flags_distinct_with_root_and_removed_edge_labels": True,
        "sector_records": sector_records,
        "complete_family_decomposition": family_records,
        "first_forward_typed_failure": (
            "DSQ/P3+K2 tail cofactor: varied pair DS is not a committed "
            "C4/C2+/P2 lower idempotent"
        ),
        "reverse_P2_scope": (
            "PQQ has the associated-graded P2 topology, but lies in response "
            "word 11:110000; the canonical cap word is 01211222 and the "
            "word/fine mapping cylinder, reduced-Eq face and shifted ridge "
            "remain unconstructed"
        ),
    }


def totalization_boundary_audit() -> dict[str, object]:
    # Minimal presentation-safe shadows for four collision classes and one
    # shared unary Cartan class.  Each graph t-c raises coordinates and rank
    # together.  Absolute carrier columns would kill the detected H0 class;
    # none is supplied by the pinned collision/P2 inventories.
    collision_old_dimension = 4
    collision_old_boundaries: tuple[tuple[Q, ...], ...] = ()
    collision_graphs = tuple(
        tuple(Q(-1) if index == root else Q(1) if index == 4 + root else Q(0)
              for index in range(8))
        for root in range(4)
    )
    require(8 - rank(collision_graphs) == collision_old_dimension,
            "the four relative collision graphs changed H0")

    # Two root squares have a common q01*H Cartan face.  Their coefficients
    # add, not cancel.  In the two-dimensional shadow (q,t), dG=t-q has H0=1.
    unary_graph = (Q(-1), Q(1))
    require(2 - rank((unary_graph,)) == 1,
            "the unary Cartan relative graph changed H0")
    return {
        "formal_collision_graphs": [
            "dt_E01=t_E01-C_(0,S)",
            "dt_E02=t_E02-C_(1,S)",
            "dt_E10=t_E10-C_(S,0)",
            "dt_E20=t_E20-C_(S,1)",
        ],
        "collision_H0_old_relative": [collision_old_dimension,
                                         8 - rank(collision_graphs)],
        "shared_unary_graph": "dG_q=t_q-q01*H2345",
        "unary_Cartan_coefficients_from_two_squares": [1, 1],
        "unary_H0_old_relative": [1, 1],
        "absolute_carrier_preimages_in_existing_inventory": False,
        "reason": (
            "the complete symmetric collision row misses the signed response "
            "splitter; the complete unary row misses q01*H; and the lower "
            "P2 cells begin only after an unconstructed operation/word map"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 hyperbolic-root collision Tate/cobar totalization gate",
        "pins": PINS,
        "complete_response_boundaries": complete_response_root_audit(),
        "unary_and_root_order_boundaries": unary_and_commutator_audit(),
        "complete_and_selected_PP_boundaries": collision_pp_boundary_audit(),
        "presentation_safe_totalization": totalization_boundary_audit(),
        "verdict": (
            "The two hyperbolic coefficient returns do not yet define a "
            "physical relative Tate/cobar pair.  The desired three-term "
            "collisions cancel inside the complete response row, while the "
            "six-coordinate root leaves an independent centered 24-term "
            "collision splitter in each 45-term sector.  On the complete "
            "unary row the two root orders differ by q01*H in each square. "
            "The full selected PP boundary has 48 distinct labelled faces; "
            "its forward DSQ tail faces have no committed lower idempotent, "
            "and its reverse PQQ faces still lack the response-to-cap word/"
            "fine map.  Relative carrier graphs preserve H0 but carry all "
            "three obstruction classes rather than filling them."
        ),
        "first_missing_typed_face": (
            "already at complete-response naturality: one source-labelled "
            "signed 24-term collision splitter (for each root), or an "
            "extension of the root to the omitted cross edges which cancels "
            "it.  After that grant, the first new square face is the shared "
            "selected-unary Cartan block q01*H2345; after both grants, the "
            "forward DSQ/P3+K2 PP face is the first lower typing failure"
        ),
        "nonclaims": [
            "the formal six-coordinate root is not called a complete source vector field",
            "the symmetric collision polynomial is not called its signed splitter",
            "an undecorated P3+K2 topology match is not called a P2 landing",
            "the relative Tate carriers are not called absolute fillers",
        ],
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("complete response root: FOUR SIGNED 24-TERM COLLISION SPLITTERS")
    print("unary root-order defect: q01*H IN EACH SQUARE")
    print("selected collision PP flags: 48 DISTINCT (24 3K2, 24 P3+K2)")
    print("forward lower face: DSQ BLOCK ABSENT; reverse PQQ: WORD MAP ABSENT")
    print("relative Tate graphs: H0 PRESERVED / OBSTRUCTIONS RETAINED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
