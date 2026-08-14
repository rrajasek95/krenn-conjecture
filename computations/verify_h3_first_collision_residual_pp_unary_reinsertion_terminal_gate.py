#!/usr/bin/env python3
"""Propagate the first signed 24-term collision residual through first PP.

Work in the E01 missing-0/doubled-S collision sector.  The complete root
residual R has twelve +1 and twelve -1 entries among the 45 collision
monomials, and lambda_R=R/24 kills the symmetric collision row and reads one
on R.

The reinsertion-natural normalized first-PP pullback is dR/96.  It has 180
flag coordinates and reads one on dR.  Its collected unary/repeated values
form a K_(2,4) cut.  Resolving every *distinct* root/PP direction into the
literal C2+, C4 and P2 packets leaves a smaller class: 24 same-cell flags,
the two-hole unary reinsertion anti-diagonal

    J_E01=(U_dD-K_(D,q01))-(U_ds1-K_(p0,s1)).

The unique root-branch/tail-equivariant normalized detector of this class is
+1/24 on the twelve p0->D,dD flags, -1/24 on the twelve
q01->-s1,ds1 flags, and zero elsewhere.  It kills the complete collision,
all repeated rows, and all distinct-direction C2+/C4/P2 packets.  It does
not kill the two formal unary cofactor rows separately.  In this forward
sector neither row is the physical unary row on sites 0,...,5, so an
absolute one-hole unary reinsertion/word bridge is still missing.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py":
        "c0c6c075388a2eb2d5dad6d133166a3f211dd268183d3e2a5433d922e2ea8ceb",
    "notes/h3-hyperbolic-root-collision-tate-cobar-totalization-gate.md":
        "673722b62a59f10b00aa20796236146df052a4d45eda0764053737bca401e95a",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "notes/h2-p2-0112-one-endpoint-hasse-placement-gate.md":
        "5b17afb39c796d79021e0c16fb9e9d0e65c33acc9c7d1b8b6185747bd1450ab5",
}
EXPECTED_LEDGER_SHA256 = (
    "4f8ee89c0f13ab86eff1998d11ec3608f107d0c54d3a3ecace58db934d6b1f1e"
)


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


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def vector(order, support, coefficient=Q(1)):
    support = set(support)
    return tuple(Q(coefficient) if label in support else Q(0)
                 for label in order)


def rank(columns) -> int:
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


def direction_shape(total, pair) -> str:
    """Literal lower packet type, retaining the source direction pair."""
    labels = tuple(sorted(total.label_edge(edge) for edge in pair))
    kinds = tuple(sorted(label[0] for label in labels))
    if kinds == ("D", "q") or kinds == ("p", "s"):
        return "C4"
    if kinds == ("q", "q"):
        return "C2+"
    if kinds in (("p", "q"), ("q", "s")):
        return "P2"
    raise RuntimeError(("unexpected root/PP pair", labels, kinds))


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    total = load(
        "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py",
        "first_collision_totalization",
    )
    lower = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "first_collision_lower_packets",
    )
    p2 = load(
        "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py",
        "first_collision_p2_placement",
    )
    lower_ledger, lower_digest = lower.audit()
    p2_ledger, p2_digest = p2.audit()
    require(lower_digest == lower.EXPECTED_LEDGER_SHA256
            and p2_digest == p2.EXPECTED_LEDGER_SHA256,
            "a pinned lower-packet ledger changed")

    root = next(record for record in total.ROOTS
                if record["name"] == "E01")
    missing, doubled = root["sector"]
    require((missing, doubled) == (total.ZERO, total.S), root["sector"])
    sector = total.complete_collision_sector(missing, doubled)
    residual = total.derivation(total.RESPONSE, root["replacements"])
    order45 = tuple(sorted(sector))
    complete45 = tuple(Q(sector[monomial]) for monomial in order45)
    residual45 = tuple(Q(residual[monomial]) for monomial in order45)
    lambda_r = scale(Q(1, 24), residual45)
    require(len(sector) == 45 and len(residual) == 24
            and Counter(residual.values()) == Counter({Q(1): 12, Q(-1): 12})
            and dot(lambda_r, complete45) == 0
            and dot(lambda_r, residual45) == 1,
            "the E01 top separator changed")

    # Literal first PP flags.  The removed edge is part of the label, so the
    # 45 four-edge collision monomials give 180 independent coordinates.
    flags = tuple((monomial, removed)
                  for monomial in order45 for removed in monomial)
    d_complete = tuple(Q(sector[monomial])
                       for monomial, _removed in flags)
    d_residual = tuple(Q(residual[monomial])
                       for monomial, _removed in flags)
    raw_pp_dual = scale(Q(1, 96), d_residual)
    require(len(flags) == 180
            and Counter(raw_pp_dual) == Counter({Q(1, 96): 48,
                                                  Q(-1, 96): 48,
                                                  Q(0): 84})
            and dot(raw_pp_dual, d_complete) == 0
            and dot(raw_pp_dual, d_residual) == 1,
            "the normalized 180-flag descendant changed")

    # The 180 flags collect into six 15-term unary rows (remove an edge at
    # doubled S) and fifteen six-term repeated rows (remove a disjoint edge).
    unary_support: dict[int, set[object]] = defaultdict(set)
    repeated_support: dict[object, set[object]] = defaultdict(set)
    for flag in flags:
        _monomial, removed = flag
        if doubled in removed:
            other = removed[1] if removed[0] == doubled else removed[0]
            unary_support[other].add(flag)
        else:
            repeated_support[removed].add(flag)
    require(len(unary_support) == 6
            and {len(support) for support in unary_support.values()} == {15}
            and len(repeated_support) == 15
            and {len(support) for support in repeated_support.values()} == {6},
            "the unary/repeated flag collection changed")
    raw_unary = {
        total.NAMES[key]: dot(raw_pp_dual, vector(flags, support))
        for key, support in unary_support.items()
    }
    raw_repeated = {
        total.label_edge(key): dot(raw_pp_dual, vector(flags, support))
        for key, support in repeated_support.items()
    }
    expected_unary = {"P": Q(1, 8), "1": Q(-1, 8),
                      "2": Q(0), "3": Q(0), "4": Q(0), "5": Q(0)}
    expected_repeated = {total.label_edge(edge): Q(0)
                         for edge in repeated_support}
    for site in (total.TWO, total.THREE, total.FOUR, total.FIVE):
        expected_repeated[total.label_edge(total.edge(total.P, site))] = Q(-1, 32)
        expected_repeated[total.label_edge(total.edge(total.ONE, site))] = Q(1, 32)
    require(raw_unary == expected_unary
            and raw_repeated == expected_repeated,
            ("the forced K2,4 lower charge changed", raw_unary, raw_repeated))

    # Recover the original response occurrence and the source direction that
    # produced each root-output flag.  Distinct directions are precisely the
    # literal lower C4/C2+/P2 packets.  Removing the varied edge after the
    # root is the exceptional same-cell PP/reinsertion face.
    packet_support: dict[frozenset[object], set[object]] = defaultdict(set)
    reinsertion_support: dict[object, set[object]] = defaultdict(set)
    tagged_records = []
    for source in total.RESPONSE:
        for varied, factor, target in root["replacements"]:
            if varied not in source:
                continue
            output = list(source)
            output[output.index(varied)] = target
            output = tuple(sorted(output))
            require(output in sector, (source, varied, target, output))
            for removed in output:
                flag = (output, removed)
                if removed == target:
                    reinsertion_support[varied].add(flag)
                    tag = "PP/reinsertion-same-cell"
                else:
                    pair = frozenset((varied, removed))
                    packet_support[pair].add(flag)
                    tag = direction_shape(total, pair)
                tagged_records.append((source, varied, factor, target,
                                       removed, flag, tag))
    require({len(support) for support in packet_support.values()} == {3}
            and len(packet_support) == 30
            and {len(support) for support in reinsertion_support.values()} == {15}
            and len(reinsertion_support) == 2,
            "the source-tagged packet decomposition changed")

    packet_values = {
        tuple(sorted(total.label_edge(edge) for edge in pair)):
            dot(raw_pp_dual, vector(flags, support))
        for pair, support in packet_support.items()
    }
    packet_shapes = Counter(direction_shape(total, pair)
                            for pair in packet_support)
    nonzero_by_shape = Counter()
    value_histogram_by_shape: dict[str, Counter[Q]] = defaultdict(Counter)
    for pair, support in packet_support.items():
        shape = direction_shape(total, pair)
        value = dot(raw_pp_dual, vector(flags, support))
        value_histogram_by_shape[shape][value] += 1
        nonzero_by_shape[shape] += bool(value)
    require(packet_shapes == Counter({"P2": 18, "C4": 6, "C2+": 6})
            and nonzero_by_shape == Counter({"P2": 18, "C4": 4, "C2+": 6})
            and value_histogram_by_shape["C4"]
                == Counter({Q(1, 32): 4, Q(0): 2})
            and value_histogram_by_shape["C2+"]
                == Counter({Q(-1, 48): 6})
            and value_histogram_by_shape["P2"]
                == Counter({Q(-1, 32): 8, Q(1, 48): 6,
                            Q(1, 32): 4}),
            (packet_shapes, nonzero_by_shape, value_histogram_by_shape))

    packet_columns = tuple(vector(flags, support)
                           for support in packet_support.values())
    repeated_columns = tuple(vector(flags, support)
                             for support in repeated_support.values())
    # The exact residual modulo all distinct-direction packets is the two
    # reinsertion complements.  The selected three flags in each formal
    # unary row are the D,q01 and p0,s1 packet faces respectively.
    live_reinsertion = {
        varied: {flag for flag in support if residual[flag[0]]}
        for varied, support in reinsertion_support.items()
    }
    require({len(support) for support in live_reinsertion.values()} == {12},
            "the two selected three-term cancellations changed")
    rein_p0 = vector(flags, live_reinsertion[total.P0])
    rein_q01 = vector(flags, live_reinsertion[total.Q01])
    reinsertion_class = add(rein_p0, scale(-1, rein_q01))
    packet_signed = []
    for pair, support in packet_support.items():
        # The two packets K_(D,q01) and K_(p0,s1) are exactly the selected
        # three-term cancellation blocks.  Their residual value is zero and
        # they are excluded together with the matching reinsertion copy.
        if not dot(raw_pp_dual, vector(flags, support)):
            continue
        varied = next(edge for edge in pair
                      if edge in (total.P0, total.Q01))
        coefficient = Q(1) if varied == total.P0 else Q(-1)
        packet_signed.append(scale(coefficient, vector(flags, support)))
    require(d_residual == add(reinsertion_class, *packet_signed)
            and in_span(packet_columns,
                        add(d_residual, scale(-1, reinsertion_class)))
            and not in_span(packet_columns, d_residual)
            and not in_span(packet_columns, reinsertion_class),
            "the residual stopped reducing to the unary reinsertion class")

    # After requiring every distinct-direction packet to be killed, symmetry
    # and normalization force the reinsertion-only detector.  It is +1/24 on
    # the p0->D complement, -1/24 on the q01->-s1 complement.
    terminal_dual = add(scale(Q(1, 24), rein_p0),
                        scale(Q(-1, 24), rein_q01))
    require(dot(terminal_dual, d_residual) == 1
            and dot(terminal_dual, d_complete) == 0
            and all(dot(terminal_dual, column) == 0
                    for column in packet_columns + repeated_columns)
            and Counter(terminal_dual) == Counter({Q(1, 24): 12,
                                                   Q(-1, 24): 12,
                                                   Q(0): 156}),
            "the reinsertion terminal detector changed")
    terminal_unary = {
        total.NAMES[key]: dot(terminal_dual, vector(flags, support))
        for key, support in unary_support.items()
    }
    require(terminal_unary == {"P": Q(1, 2), "1": Q(-1, 2),
                               "2": Q(0), "3": Q(0),
                               "4": Q(0), "5": Q(0)},
            terminal_unary)

    # A same-cell packet is not one of the distinct scalar-direction second
    # faces classified as C2+/C4/P2.  Moreover, in the forward missing-0
    # sector the two unary cofactors live on augmented vertex sets and are
    # not the physical unary row on sites 0,...,5.  This is the placement
    # reason the formal group rows cannot simply be adjoined as old columns.
    unary_vertices = {}
    for key, support in unary_support.items():
        sample, removed = next(iter(support))
        remainder = tuple(edge for edge in sample if edge != removed)
        vertices = sorted({vertex for edge in remainder for vertex in edge})
        unary_vertices[total.NAMES[key]] = [total.NAMES[v] for v in vertices]
    require(unary_vertices["P"] == ["S", "1", "2", "3", "4", "5"]
            and unary_vertices["1"] == ["P", "S", "2", "3", "4", "5"]
            and unary_vertices["P"] != ["0", "1", "2", "3", "4", "5"]
            and unary_vertices["1"] != ["0", "1", "2", "3", "4", "5"],
            unary_vertices)

    # Pin the downstream fact rather than silently identifying these response
    # flags with the canonical cap P2 section.
    require(p2_ledger["physical_cut"]["top_word"] == "01211222"
            and p2_ledger["first_absent_column"].startswith(
                "one occurrence-local endpoint-even")
            and lower_ledger["physical_route_classification"]
                ["PQ_or_SQ_response"]["unconditional_terminal"] is False,
            "the downstream P2 placement status changed")

    ledger = {
        "theorem": "h3 first collision residual PP/unary reinsertion terminal gate",
        "pins": PINS,
        "sector": {
            "root": "E01[p0->D, q01->-s1]",
            "response_word": "11:110000",
            "fine_sector": "missing 0 / doubled S",
            "collision_topology": "P3+2K2",
            "coordinates": 45,
            "symmetric_collision_coefficients": "2 on all 45",
            "residual": "12(+1)+12(-1)+21(0)",
            "lambda_R": "R/24",
            "lambda_R_on_complete_and_R": ["0", "1"],
        },
        "first_PP": {
            "flags": len(flags),
            "raw_normalized_dual": "dR/96",
            "raw_value_histogram": {
                "+1/96": 48, "-1/96": 48, "0": 84,
            },
            "raw_on_d_complete_and_dR": ["0", "1"],
            "groups": {"unary_15_term": 6, "repeated_6_term": 15},
            "forced_raw_unary_values": {
                key: str(value) for key, value in raw_unary.items()
            },
            "forced_raw_repeated_nonzero_values": {
                key: str(value) for key, value in raw_repeated.items() if value
            },
            "K2_4_identity": (
                "32*g=sum_(x=2..5)(U_P-U_1-V_p_x+V_q1x)"
            ),
        },
        "source_direction_packets": {
            "root_and_removed_edge_labels_retained": True,
            "distinct_packets": len(packet_support),
            "packet_type_counts": dict(sorted(packet_shapes.items())),
            "nonzero_packet_counts": dict(sorted(nonzero_by_shape.items())),
            "value_histograms": {
                shape: {str(value): count for value, count in sorted(hist.items())}
                for shape, hist in sorted(value_histogram_by_shape.items())
            },
            "all_packet_values": {
                "+".join(pair): str(value)
                for pair, value in sorted(packet_values.items())
            },
            "same_cell_flags_are_not_distinct_Hasse_pairs": True,
        },
        "smaller_obstruction": {
            "name": "J_E01, two-hole unary reinsertion anti-diagonal",
            "formula": (
                "(U_dD-K_(D,q01))-(U_ds1-K_(p0,s1))"
            ),
            "support": "12 p0->D,dD flags minus 12 q01->-s1,ds1 flags",
            "identity_mod_lower_packets": "dR == J_E01 mod C2+/C4/P2",
            "normalized_detector": (
                "+1/24 on first twelve, -1/24 on second twelve"
            ),
            "detector_values": {
                "dR": "1", "d_complete_collision": "0",
                "all_repeated_groups": "0",
                "all_distinct_C2plus_C4_P2_packets": "0",
                "U_dD": "1/2", "U_ds1": "-1/2",
            },
            "unary_vertex_sets": unary_vertices,
            "physical_six_site_unary_available": False,
        },
        "existing_column_verdict": {
            "complete_collision_P3plus2K2": "killed by both duals",
            "C2plus_C4_P2": (
                "remove all distinct-direction PP faces but leave J_E01"
            ),
            "canonical_AugP2_word": "01211222",
            "word_identified_with_response_sector": False,
            "first_missing_column": (
                "an E01/root-labelled one-hole unary PP/reinsertion section "
                "joining the two augmented six-vertex cofactors, natural on "
                "the D,q01 and p0,s1 selected faces; downstream P2 transport "
                "must retain the response-to-01211222 word/fine comparison"
            ),
        },
        "terminal_criterion": (
            "If the complete same-word/fine/root-labelled source map has no "
            "absolute column with nonzero J_E01 value (equivalently no "
            "one-hole unary reinsertion landing), the reinsertion-only dual "
            "is the first-collision terminal.  Any such face-natural landing "
            "fills this lane; coefficient-level C2+/C4/P2 shadows alone do not."
        ),
        "scope": (
            "one exact E01 45-term sector and all 180 labelled first-PP "
            "flags; the other three sectors follow by the recorded root/site "
            "relabellings.  Terminality remains conditional on exhaustivity "
            "of the fully augmented same-grade physical map."
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
    print("E01 collision residual: 45 TOP / 24 SIGNED / lambda=R/24")
    print("first PP: 180 FLAGS / raw normalized dual dR/96")
    print("distinct lower packets: C2+ 6 / C4 6 / P2 18")
    print("residual modulo those packets: J_E01, 24 SAME-CELL FLAGS")
    print("existing physical unary landing: ABSENT IN FORWARD SECTOR")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
