#!/usr/bin/env python3
"""Audit the response/unary and Cartan landing of the E01 one-hole class.

The first signed collision residual reduces, after its distinct-direction
lower packets, to two twelve-term reinsertion complements.  Complete each
complement by its three cancelled terms.  Their source parents are the two
fifteen-term cofactors

    A_s : p0 removed, on {S,1,2,3,4,5},
    B_s : q01 removed, on {P,S,2,3,4,5}.

The four response heads have rank-one projection A_s+B_s.  The physical
unary row on {0,1,2,3,4,5} has zero projection.  This checker grants the
strongest presentation-safe Cartan transport, one termwise relative graph
from each source cofactor to its root image.  Nevertheless the normalized
anti-diagonal extends across all thirty graphs and still detects the target
class.  Thus universal Cartan/de Rham contraction supplies only a relative
carrier here; it does not manufacture the missing absolute cofactor split.

Adjoining either the target one-hole anti-diagonal or the source cofactor
split raises rank by exactly one and fills the residual modulo the two
three-term lower packets.  This is the sharp physical landing criterion.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_first_collision_residual_pp_unary_reinsertion_terminal_gate.py":
        "74ee5a56f2d11f910a1121f7ebe48d051913a939c786cb9bd5ed6a6250a1eda7",
    "notes/h3-first-collision-residual-pp-unary-reinsertion-terminal-gate.md":
        "62984587b90c5f628acadc25fe5ecb067f7ffffce88a5961581dd42adcd2482e",
    "computations/verify_h3_xi01_occurrence_spencer_universal_graph_gate.py":
        "19e8fa46cc275f6c18a22b73a8ba31c24d21476c5bce6bc3fe4b34b9a6497e19",
    "computations/verify_h3_universal_spencer_euler_contraction.py":
        "4e4e4810dc49ab366555288ab7c696047cd3ce79ab7dc4b159b38047def8942b",
    "computations/verify_h3_complete_hasse_cartan_naturality_square_gate.py":
        "3ea6a79bc6918cc4569bd12ad0b1634679c28037b687b6ae7c0e610e81998279",
    "computations/verify_h3_unsigned_augmented_vertex_shear_authorization_gate.py":
        "a7e4fdc36cb59e1b96fa917b0498057e35ff649e1aabb644d7157952f824d0da",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
}
EXPECTED_LEDGER_SHA256 = (
    "6aa03c5eba430a577b54fe4448169e83b53753f6f8bdeb726ea0a9d800b63e93"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(columns)
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
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def in_span(columns, value) -> bool:
    columns = tuple(columns)
    return rank(columns) == rank(columns + (tuple(value),))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge,) + tail))


def unit(order, label, coefficient=Q(1)):
    return tuple(Q(coefficient) if value == label else Q(0)
                 for value in order)


def characteristic(order, support, coefficient=Q(1)):
    support = set(support)
    return tuple(Q(coefficient) if value in support else Q(0)
                 for value in order)


def replace_edge(matching, source, target):
    output = list(matching)
    require(output.count(source) == 1, (matching, source))
    output[output.index(source)] = target
    return tuple(sorted(output))


def pp(polynomial):
    answer = Counter()
    for monomial, coefficient in polynomial.items():
        for removed in monomial:
            answer[(monomial, removed)] += coefficient
    return Counter({label: value for label, value in answer.items() if value})


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    terminal = load(
        "computations/verify_h3_first_collision_residual_pp_unary_reinsertion_terminal_gate.py",
        "one_hole_terminal_pin",
    )
    terminal_ledger, terminal_digest = terminal.audit()
    require(terminal_digest == terminal.EXPECTED_LEDGER_SHA256
            and terminal_ledger["smaller_obstruction"]["support"]
                == "12 p0->D,dD flags minus 12 q01->-s1,ds1 flags",
            "the first-collision terminal changed")

    total = load(
        "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py",
        "one_hole_totalization",
    )
    root = next(record for record in total.ROOTS
                if record["name"] == "E01")
    replacements = {
        varied: (factor, target)
        for varied, factor, target in root["replacements"]
    }
    require(replacements == {
        total.P0: (Q(1), total.D),
        total.Q01: (Q(-1), total.S1),
    }, ("E01 replacements changed", replacements))
    residual = total.derivation(total.RESPONSE, root["replacements"])

    # The two source first-PP fibres.  Removing p0 or q01 leaves a perfect
    # matching on the displayed augmented six-vertex set.  Root transport is
    # a literal termwise bijection to the two target unary cofactors.
    branch_data = {}
    for name, source in (("A", total.P0), ("B", total.Q01)):
        factor, target = replacements[source]
        source_by_remainder = {}
        target_by_remainder = {}
        live_remainders = set()
        for matching in total.RESPONSE:
            if source not in matching:
                continue
            remainder = tuple(edge for edge in matching if edge != source)
            output = replace_edge(matching, source, target)
            require(tuple(edge for edge in output if edge != target) == remainder,
                    ("root transport changed the cofactor remainder", name,
                     matching, output))
            source_by_remainder[remainder] = matching
            target_by_remainder[remainder] = output
            if residual[output]:
                require(residual[output] == factor,
                        ("root residual sign changed", name, output))
                live_remainders.add(remainder)
        require(len(source_by_remainder) == len(target_by_remainder) == 15
                and len(live_remainders) == 12,
                ("one-hole fibre changed", name, len(source_by_remainder),
                 len(target_by_remainder), len(live_remainders)))
        branch_data[name] = {
            "source": source,
            "target": target,
            "factor": factor,
            "source_by_remainder": source_by_remainder,
            "target_by_remainder": target_by_remainder,
            "remainders": tuple(sorted(source_by_remainder)),
            "live": frozenset(live_remainders),
            "cancelled": frozenset(set(source_by_remainder)-live_remainders),
        }
    require({len(data["cancelled"]) for data in branch_data.values()} == {3},
            "the two three-term companion packets changed")

    a_vertices = sorted({vertex for remainder in branch_data["A"]["remainders"]
                         for edge in remainder for vertex in edge})
    b_vertices = sorted({vertex for remainder in branch_data["B"]["remainders"]
                         for edge in remainder for vertex in edge})
    require(a_vertices == [total.S, total.ONE, total.TWO, total.THREE,
                           total.FOUR, total.FIVE]
            and b_vertices == [total.P, total.S, total.TWO, total.THREE,
                               total.FOUR, total.FIVE],
            ("augmented cofactor vertices changed", a_vertices, b_vertices))

    # A literal 60-coordinate comparison: two source cofactors and their two
    # rooted target copies.  Root/reinsertion labels are part of each label.
    order = tuple(
        (side, name, remainder)
        for side in ("source", "target")
        for name in ("A", "B")
        for remainder in branch_data[name]["remainders"]
    )
    require(len(order) == len(set(order)) == 60, "comparison width changed")
    full = {}
    live = {}
    cancelled = {}
    for side in ("source", "target"):
        for name in ("A", "B"):
            full[side, name] = characteristic(
                order, ((side, name, remainder)
                        for remainder in branch_data[name]["remainders"])
            )
            live[side, name] = characteristic(
                order, ((side, name, remainder)
                        for remainder in branch_data[name]["live"])
            )
            cancelled[side, name] = characteristic(
                order, ((side, name, remainder)
                        for remainder in branch_data[name]["cancelled"])
            )
            require(full[side, name] == add(live[side, name],
                                            cancelled[side, name]),
                    ("cofactor completion changed", side, name))

    # Restrict the selected complete response first-PP row to these source
    # fibres.  It is A_s+B_s.  Four response heads and all their differences
    # still have rank one after projection to the selected head.
    response_projection = [Q(0)] * len(order)
    for matching in total.RESPONSE:
        for removed in matching:
            if removed not in replacements:
                continue
            name = "A" if removed == total.P0 else "B"
            remainder = tuple(edge for edge in matching if edge != removed)
            response_projection[order.index(("source", name, remainder))] += 1
    response_projection = tuple(response_projection)
    response_expected = add(full["source", "A"], full["source", "B"])
    require(response_projection == response_expected,
            "the complete response PP projection changed")
    zero = (Q(0),) * len(order)
    head_rows = (response_projection, zero, zero, zero)
    head_differences = tuple(add(head_rows[index], scale(-1, head_rows[0]))
                             for index in range(1, 4))
    require(rank(head_rows + head_differences) == 1,
            "response-head differences split the two source cofactors")

    # The actual physical unary row has vertices 0,...,5.  Its fifteen
    # matching monomials are disjoint from both augmented cofactor supports,
    # before the still stricter root/reinsertion tags are imposed.
    physical_unary = set(perfect_matchings((total.ZERO, total.ONE, total.TWO,
                                            total.THREE, total.FOUR,
                                            total.FIVE)))
    augmented_remainders = (set(branch_data["A"]["remainders"])
                            | set(branch_data["B"]["remainders"]))
    require(len(physical_unary) == 15
            and not (physical_unary & augmented_remainders),
            "the physical unary row entered an augmented cofactor")
    physical_unary_projections = (zero,) * 4

    # Grant all termwise presentation-safe Cartan graphs.  With the root
    # coefficient retained they are f*(target-source), hence their sum is
    # the target signed cofactor split minus its source counterpart.
    graphs = []
    for name in ("A", "B"):
        factor = branch_data[name]["factor"]
        for remainder in branch_data[name]["remainders"]:
            graphs.append(add(
                unit(order, ("target", name, remainder), factor),
                unit(order, ("source", name, remainder), -factor),
            ))
    graphs = tuple(graphs)
    require(len(graphs) == rank(graphs) == 30,
            "the termwise relative Cartan graphs changed")

    source_split = add(full["source", "A"],
                       scale(-1, full["source", "B"]))
    target_landing = add(full["target", "A"],
                        scale(-1, full["target", "B"]))
    require(add(*graphs) == add(target_landing, scale(-1, source_split)),
            "the signed Cartan graph sum changed")

    packet_a = cancelled["target", "A"]
    packet_b = cancelled["target", "B"]
    target_class = add(live["target", "A"],
                       scale(-1, live["target", "B"]))
    target_complete_collision = scale(
        2, add(full["target", "A"], full["target", "B"]))
    require(target_class == add(target_landing, scale(-1, packet_a), packet_b),
            "the completed one-hole landing identity changed")

    old_columns = (head_rows + head_differences
                   + physical_unary_projections
                   + (packet_a, packet_b, target_complete_collision)
                   + graphs)
    old_rank = rank(old_columns)

    # Extend the old reinsertion detector equally across each relative graph.
    # It kills the complete response aggregate, every response-head image,
    # both companion packets, the complete collision, every physical unary
    # projection and all thirty Cartan graphs, but reads one on J_E01.
    terminal_dual = [Q(0)] * len(order)
    for side in ("source", "target"):
        for name, sign in (("A", Q(1)), ("B", Q(-1))):
            for remainder in branch_data[name]["live"]:
                terminal_dual[order.index((side, name, remainder))] = sign / 24
    terminal_dual = tuple(terminal_dual)
    require(all(dot(terminal_dual, column) == 0 for column in old_columns)
            and dot(terminal_dual, target_class) == 1
            and not in_span(old_columns, target_class),
            "the response/Cartan one-hole detector stopped extending")

    # Either an absolute target landing or the missing absolute source split
    # (followed by the already-granted graphs) is exactly one rank raiser and
    # fills the class.  The identities are checked term by term.
    target_repaired = old_columns + (target_landing,)
    source_repaired = old_columns + (source_split,)
    require(rank(target_repaired) == rank(source_repaired) == old_rank + 1
            and in_span(target_repaired, target_class)
            and in_span(source_repaired, target_class)
            and add(add(*graphs), source_split,
                    scale(-1, packet_a), packet_b) == target_class,
            "the sharp one-hole repair changed")

    # Exact universal Cartan identities.  Contracting the complete response
    # one-form with E01 is precisely the signed top residual.  Lie derivative
    # commutes with first PP only when it transports the removed d-edge label.
    contracted = Counter()
    lie_pp = Counter()
    for matching, coefficient in total.RESPONSE.items():
        for removed in matching:
            if removed in replacements:
                factor, target = replacements[removed]
                contracted[replace_edge(matching, removed, target)] += (
                    coefficient * factor
                )
        for varied, (factor, target) in replacements.items():
            if varied not in matching:
                continue
            output = replace_edge(matching, varied, target)
            for removed in matching:
                output_removed = target if removed == varied else removed
                lie_pp[(output, output_removed)] += coefficient * factor
    contracted = Counter({label: value for label, value in contracted.items()
                          if value})
    lie_pp = Counter({label: value for label, value in lie_pp.items() if value})
    require(contracted == residual
            and lie_pp == pp(residual),
            "the universal Cartan/Kahler identities changed")

    local_cartan = {
        "i_X(dp0)": "D",
        "d_i_X(dp0)": "dD=L_X(dp0)",
        "i_X(dq01)": "-s1",
        "d_i_X(dq01)": "-ds1=L_X(dq01)",
    }
    # On a one-variable positive Spencer generator, Euler contraction gives
    # H(dx)=x and H(d x)=x, hence dH(dx)+Hd(dx)=dx and Hd(x)=x.  The pinned
    # universal checker proves the same in every degree <=6 and exterior
    # degree <=5; this local equality records the precise symbols used here.
    euler_local = {
        "H(dx)": "x",
        "dH(dx)+Hd(dx)": "dx",
        "Hd(x)": "x",
    }

    ledger = {
        "theorem": "E01 one-hole response/Cartan/de Rham landing gate",
        "pins": PINS,
        "two_complete_cofactors": {
            "A": {
                "source_removed": "p0",
                "target_removed": "dD",
                "vertices": [total.NAMES[value] for value in a_vertices],
                "terms": 15,
                "live_after_lower_packets": 12,
                "cancelled_companion": 3,
            },
            "B": {
                "source_removed": "q01",
                "target_removed": "ds1",
                "vertices": [total.NAMES[value] for value in b_vertices],
                "terms": 15,
                "live_after_lower_packets": 12,
                "cancelled_companion": 3,
            },
            "target_class": "J_E01=A_t^live-B_t^live",
            "completion_identity": "J_E01=(A_t-B_t)-K_A+K_B",
        },
        "full_response_head_and_unary_inventory": {
            "selected_PP_projection": "A_s+B_s",
            "four_heads_and_head_differences_rank": 1,
            "individual_source_cofactor_split_available": False,
            "physical_unary_vertices": ["0", "1", "2", "3", "4", "5"],
            "physical_unary_terms": len(physical_unary),
            "intersection_with_A_or_B_remainders": 0,
            "root_reinsertion_label_preserved": False,
        },
        "cartan_derham": {
            "exact_top_identity": "i_X(dR_complete)=X(R_complete)=R_E01",
            "exact_PP_identity": "L_X(dR_complete)=d(XR_complete)",
            "local_one_form_identities": local_cartan,
            "euler_local_identity": euler_local,
            "universal_positive_degree_contraction_pinned": True,
            "relative_graphs_granted": len(graphs),
            "relative_graph_rank": rank(graphs),
            "graph_sum": "(A_t-B_t)-(A_s-B_s)",
            "physical_comparison_functor_for_i_X_constructed": False,
            "classification": (
                "Cartan and Euler identities are exact in the universal "
                "polynomial de Rham/PP algebra.  With the word/fine/root/"
                "reinsertion labels retained, their presentation-safe "
                "realization is the relative graph, not an absolute column."
            ),
        },
        "exact_rank_gate": {
            "ambient_coordinates": len(order),
            "old_column_rank_after_all_relative_graphs": old_rank,
            "old_H0_dimension": len(order) - old_rank,
            "J_in_old_span": False,
            "normalized_extended_dual": (
                "+1/24 on the 12 live A source and target coordinates; "
                "-1/24 on the 12 live B source and target coordinates"
            ),
            "dual_on_old_columns": "0",
            "dual_on_J": "1",
            "rank_after_absolute_target_landing": rank(target_repaired),
            "rank_after_absolute_source_split": rank(source_repaired),
            "J_filled_after_either_repair": True,
        },
        "verdict": (
            "The full response-head/unary inventory does not supply the two "
            "one-hole cofactors: it sees only A_s+B_s, while the physical "
            "unary row is disjoint.  Even all termwise Cartan graphs leave "
            "J_E01 nonzero.  The universal de Rham contraction closes this "
            "lane iff it descends as an absolute physical comparison that "
            "supplies A_s-B_s (equivalently A_t-B_t); asserting that descent "
            "without the comparison is exactly the missing generator."
        ),
        "terminal_criterion": (
            "If no same-word/fine/root/reinsertion physical column has "
            "nonzero pairing with the extended anti-diagonal, J_E01 is the "
            "first one-hole augmented terminal.  A descended absolute Cartan "
            "contraction or one source-valid cofactor-split row is necessary "
            "and sufficient for this reduced lane."
        ),
        "scope": (
            "exact E01 one-hole quotient after the committed C2+/C4/P2 "
            "companions, all four response-head projections, the physical "
            "six-site unary row, and every termwise relative Cartan graph. "
            "Global terminality still requires extending the dual across "
            "the remaining augmented readout grades."
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
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    gate = ledger["exact_rank_gate"]
    print("E01 unary cofactors: 15+15 TERMS / LIVE 12+12")
    print("response-head/unary projection: RANK 1 / PHYSICAL UNARY DISJOINT")
    print("relative Cartan graphs: 30 / J_E01 SURVIVES")
    print("old rank/H0:", gate["old_column_rank_after_all_relative_graphs"],
          gate["old_H0_dimension"])
    print("absolute cofactor split: ONE RANK RAISER / J_E01 FILLED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
