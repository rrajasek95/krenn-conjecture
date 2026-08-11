#!/usr/bin/env python3
"""Exact first-four-hole obstruction for the chart-25 relative cell.

The balanced chart-25 columns have endpoint fine degree 111|111.  For a
selected off-diagonal endpoint order (a,b), exactly four endpoint half-edge
labels must change to reach 3e_a|3e_b.  This checker constructs the complete
literal four-cube for every one of the 56 mixed and 32 pure first-neighbour
source columns, including every Hamming face.

The fully changed bridge is source-labelled and target-free, but it has no
pure-anchor incidence and retains a large off-fibre boundary.  More
generally, on every literal cube vertex (and hence on every Hamming/four-hole
/Bianchi finite difference) the integral character

                    pure-anchor incidence + total target

vanishes.  The Component-III lower face has values (-1,0), so it is outside
the complete first-order image.  Ordinary residue and w are retained as
separate zero readouts throughout.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_LEDGER_SHA256 = "5163f98d2734d1b6c386b898bcdc994494dd03525ba7f0b67ca25bc69bc24fc5"
PINS = {
    "computations/verify_h3_rootless_component_iii_complete_typed_inventory.py":
        "3e2b5912f58646169547b418bb4975a27635dcd8d548a010eb4c2e265412f465",
    "computations/verify_n8_chart25_pure_anchor_relative_bridge_frontier.py":
        "5fd3ed5f649393841acfac17dec1be01d4edc77166674b836c913b24ab770e3f",
    "computations/verify_n8_chart25_relative_cell_component_iii_grade_gate.py":
        "616f63b349c5aeb70c02dfeaa380fb7b8595545f4cc5090ac9d12021402ba131",
    "computations/verify_n8_chart25_relative_4d_obstruction.py":
        "afb3ff04ec4c2c487b577d8d332f993e4fcf469244da8c77f5c51ff04b3753c5",
    "computations/verify_fourhole_allword_row_identity_grade_ladder.py":
        "74f97ca3f3735e75e460fee6b61fc7ddba357da49a5f67905061d1b9f24969b0",
    "computations/verify_overlapping_pair_cap_bianchi_connection.py":
        "4f7baaf35b5e77658ff6fbfa7dc669cc516f5eb89b4cf7582cfe518f7600ec55",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def subtract_multiset(row: bytes, term: bytes) -> bytes:
    remainder = Counter(row)
    remainder.subtract(Counter(term))
    require(all(value >= 0 for value in remainder.values()),
            "term does not divide source row")
    return bytes(sorted(remainder.elements()))


def fine_degree(column, base):
    word, multiplier = column
    degree = [[0, 0, 0] for _ in range(8)]
    for site, colour in enumerate(word):
        degree[site][colour] += 1
    for coordinate in multiplier:
        left, right, left_colour, right_colour = base.COORDINATES[coordinate]
        degree[left][left_colour] += 1
        degree[right][right_colour] += 1
    return tuple(tuple(row) for row in degree)


def endpoint_modifications(column, selected, base):
    """The four individual half-label changes to selected endpoint degree."""

    word, multiplier = column
    modifications = []
    multiplier = tuple(multiplier)
    for endpoint, target in enumerate(selected):
        if word[endpoint] != target:
            modifications.append(("word", endpoint))
        for occurrence, coordinate in enumerate(multiplier):
            left, right, left_colour, right_colour = base.COORDINATES[coordinate]
            if left == endpoint and left_colour != target:
                modifications.append(("multiplier", occurrence, endpoint))
            if right == endpoint and right_colour != target:
                modifications.append(("multiplier", occurrence, endpoint))
    require(len(modifications) == 4, (column, selected, modifications))
    require(Counter(item[-1] for item in modifications) == {0: 2, 1: 2},
            "the first grade-changing operation stopped being 2+2")
    return tuple(modifications)


def apply_modifications(column, selected, modifications, chosen, base):
    word, raw_multiplier = column
    word = list(word)
    multiplier = list(raw_multiplier)
    for index in chosen:
        operation = modifications[index]
        if operation[0] == "word":
            endpoint = operation[1]
            word[endpoint] = selected[endpoint]
            continue
        _kind, occurrence, endpoint = operation
        left, right, left_colour, right_colour = base.COORDINATES[
            multiplier[occurrence]
        ]
        if left == endpoint:
            left_colour = selected[endpoint]
        elif right == endpoint:
            right_colour = selected[endpoint]
        else:
            raise RuntimeError("multiplier occurrence lost its endpoint")
        multiplier[occurrence] = base.COORDINATE_ID[
            (left, right, left_colour, right_colour)
        ]
    return tuple(word), bytes(sorted(multiplier))


def column_readout(column):
    """(anchor incidence, labelled targets, ordinary residue, w)."""

    word, multiplier = column
    if len(set(word)) == 1:
        return Q(1), Counter({multiplier: Q(-1)}), Q(0), Q(0)
    return Q(0), Counter(), Q(0), Q(0)


def add_scaled_readout(total, coefficient, readout) -> None:
    anchor, targets, ores, w = readout
    total["anchor"] += coefficient * anchor
    total["ores"] += coefficient * ores
    total["w"] += coefficient * w
    for label, value in targets.items():
        total["targets"][label] += coefficient * value
        if not total["targets"][label]:
            del total["targets"][label]


def operation_readout(operation, literal_readouts):
    total = {
        "anchor": Q(0), "targets": Counter(),
        "ores": Q(0), "w": Q(0),
    }
    for column, coefficient in operation.items():
        add_scaled_readout(total, coefficient, literal_readouts[column])
    return total


def face_operation(vertices, fixed_mask, directions):
    operation = Counter()
    directions = tuple(directions)
    for moving_mask in range(1 << len(directions)):
        mask = fixed_mask
        parity = 0
        for local_index, direction in enumerate(directions):
            if moving_mask & (1 << local_index):
                mask |= 1 << direction
                parity += 1
        operation[vertices[mask]] += -1 if parity % 2 else 1
    return Counter({column: coefficient for column, coefficient
                    in operation.items() if coefficient})


def encoded_operation(operation):
    return tuple(sorted(
        ((column[0], column[1].hex(), coefficient)
         for column, coefficient in operation.items()),
        key=repr,
    ))


def signed_boundary(columns, base):
    boundary = Counter()
    for coefficient, column in columns:
        for row in base.column_rows(column):
            boundary[row] += coefficient
    return Counter({row: coefficient for row, coefficient in boundary.items()
                    if coefficient})


def audit():
    pin_dependencies()
    bridge = load(
        "chart25_fourhole_bridge",
        "verify_n8_chart25_pure_anchor_relative_bridge_frontier.py",
    )
    fourhole = load(
        "chart25_fourhole_rows",
        "verify_fourhole_allword_row_identity_grade_ladder.py",
    )
    relative = load(
        "chart25_fourhole_relative",
        "verify_n8_chart25_relative_4d_obstruction.py",
    )
    base = relative.BASE
    dual = relative.DUAL
    expanded, _ = dual.expanded_functional()
    local_rows = relative.frozen_rows()
    leaves = local_rows[:4]
    centre = local_rows[4]

    # These are the two non-cubical members of the requested operation
    # inventory.  The all-word four-hole rows are response-affine/grade zero,
    # so they cannot change 111|111 into 3e_a|3e_b.  The ten committed
    # cap/Bianchi expressions are literal zero identities and therefore add
    # no new chain readout.  Re-run both facts from their source checkers.
    fourhole.audit_allword_identity_and_weights()
    fourhole.audit_grade_ladder()
    require(bridge.BIANCHI.audit() == 10,
            "committed cap/Bianchi identity census moved")

    mixed_columns = tuple(sorted(
        dual.actual_incident_source_columns(expanded)[2], key=repr
    ))
    require(len(mixed_columns) == 56, "mixed first-neighbour census moved")

    pure_columns = set()
    for row in expanded:
        row_counter = Counter(row)
        for colour in range(3):
            word = (colour,) * 8
            for term in base.word_terms(word):
                term_counter = Counter(term)
                if all(row_counter[key] >= value
                       for key, value in term_counter.items()):
                    pure_columns.add((word, subtract_multiset(row, term)))
    pure_columns = tuple(sorted(pure_columns, key=repr))
    require(len(pure_columns) == 32, "pure first-neighbour census moved")
    raw_columns = mixed_columns + pure_columns
    balanced_degree = ((1, 1, 1),) * 8
    require(all(fine_degree(column, base) == balanced_degree
                for column in raw_columns),
            "a first-neighbour source column left the balanced degree")

    literal_columns = set()
    literal_readouts = {}
    operation_sets = {rank: set() for rank in range(1, 5)}
    target_active_vertex_histogram = Counter()
    cube_records = []

    for selected in ((2, 1), (1, 2)):
        terminal_endpoint_degree = (
            tuple(3 if colour == selected[0] else 0 for colour in range(3)),
            tuple(3 if colour == selected[1] else 0 for colour in range(3)),
        )
        for source_index, column in enumerate(raw_columns):
            modifications = endpoint_modifications(column, selected, base)
            vertices = {}
            selected_masks = []
            target_active = 0
            for mask in range(16):
                chosen = tuple(index for index in range(4)
                               if mask & (1 << index))
                vertex = apply_modifications(
                    column, selected, modifications, chosen, base
                )
                vertices[mask] = vertex
                literal_columns.add(vertex)
                literal_readouts[vertex] = column_readout(vertex)
                endpoint_degree = fine_degree(vertex, base)[:2]
                if endpoint_degree == terminal_endpoint_degree:
                    selected_masks.append(mask)
                if len(set(vertex[0])) == 1:
                    target_active += 1
            require(selected_masks == [15],
                    "a lower Hamming face reached the repeated endpoint grade")
            target_active_vertex_histogram[target_active] += 1

            # Every cubical finite-difference face at ranks one through four.
            # Rank one is literal Hamming transport, rank two contains the
            # square/Bianchi comparisons, and rank four is the first complete
            # four-hole operation.
            for rank in range(1, 5):
                for directions in itertools.combinations(range(4), rank):
                    complement = tuple(index for index in range(4)
                                       if index not in directions)
                    for fixed_bits in range(1 << len(complement)):
                        fixed_mask = sum(
                            (1 << direction)
                            for local, direction in enumerate(complement)
                            if fixed_bits & (1 << local)
                        )
                        operation = face_operation(
                            vertices, fixed_mask, directions
                        )
                        operation_sets[rank].add(encoded_operation(operation))
                        readout = operation_readout(operation, literal_readouts)
                        character = readout["anchor"] + sum(
                            readout["targets"].values(), Q(0)
                        )
                        require(character == 0,
                                "a literal cubical operation broke the character")
                        require(readout["ores"] == readout["w"] == 0,
                                "a literal operation acquired ores or w")

            cube_records.append({
                "selected": list(selected),
                "source_index": source_index,
                "modification_types": [item[0] for item in modifications],
                "target_active_vertices": target_active,
            })

    require(len(cube_records) == 176, "literal four-cube census moved")
    # For a pure word, only multiplier-only vertices retain a target.  Mixed
    # inputs can sometimes enter/leave another pure word, so freeze the exact
    # complete histogram rather than assuming a formula for them.
    require(sum(target_active_vertex_histogram.values()) == 176,
            "target-active histogram lost cubes")

    # The primitive integral dual on chain/readout coordinates.  It kills
    # every literal source column and therefore every face operation.
    for column in literal_columns:
        anchor, targets, ores, w = literal_readouts[column]
        require(anchor + sum(targets.values(), Q(0)) == 0,
                "primitive source character failed on a literal column")
        require(ores == w == 0, "literal source column acquired ores/w")
    desired = {
        "anchor": Q(-1), "targets": Counter(),
        "ores": Q(0), "w": Q(0),
    }
    desired_pairing = desired["anchor"] + sum(
        desired["targets"].values(), Q(0)
    )
    require(desired_pairing == -1,
            "Component-III lower face escaped the primitive dual")

    # Apply the full four-Hamming change to all 144 physical bridge choices.
    # This is the most generous literal grade transport: both the mixed and
    # pure-anchor columns are moved into one selected endpoint grade.
    pure_zero_matching = bytes(sorted(
        base.COORDINATE_ID[(left, right, 0, 0)]
        for left, right in ((0, 1), (2, 4), (3, 5), (6, 7))
    ))
    anchor_columns = []
    groups = []
    for leaf in leaves:
        multiplier = subtract_multiset(leaf, pure_zero_matching)
        anchor_columns.append(((0,) * 8, multiplier))
        choices = tuple(column for column in mixed_columns
                        if leaf in base.column_rows(column)
                        and centre in base.column_rows(column))
        groups.append(tuple(sorted(choices, key=repr)))
    require(tuple(map(len, groups)) == (3, 4, 4, 3),
            "physical bridge choice multiplicities moved")

    transported_support_histograms = {}
    transported_l1_histograms = {}
    transported_minimum_records = {}
    for selected in ((2, 1), (1, 2)):
        support_histogram = Counter()
        l1_histogram = Counter()
        minima = []
        for choices in itertools.product(*groups):
            terms = []
            for mixed, anchor in zip(choices, anchor_columns, strict=True):
                for coefficient, column in ((1, mixed), (-1, anchor)):
                    modifications = endpoint_modifications(
                        column, selected, base
                    )
                    transported = apply_modifications(
                        column, selected, modifications, range(4), base
                    )
                    require(fine_degree(transported, base)[:2] == (
                        tuple(3 if colour == selected[0] else 0
                              for colour in range(3)),
                        tuple(3 if colour == selected[1] else 0
                              for colour in range(3)),
                    ), "transported bridge missed its selected endpoint grade")
                    require(len(set(transported[0])) > 1,
                            "selected off-diagonal endpoint word became pure")
                    terms.append((coefficient, transported))
            boundary = signed_boundary(terms, base)
            require(not any(row in boundary for row in local_rows),
                    "transported bridge retained a balanced chart25 row")
            support_histogram[len(boundary)] += 1
            l1_histogram[sum(map(abs, boundary.values()))] += 1
            minima.append((len(boundary), tuple(
                "".join(map(str, column[0])) for column in choices
            )))
        require(support_histogram == {
            775: 2, 797: 24, 801: 16, 811: 56, 817: 4,
            819: 10, 821: 6, 823: 16, 825: 10,
        }, "transported off-fibre support histogram moved")
        require(l1_histogram == {832: 144},
                "transported off-fibre L1 histogram moved")
        minimum = tuple(words for size, words in minima if size == 775)
        require(len(minimum) == 2,
                "transported minimum bridge multiplicity moved")
        key = "".join(map(str, selected))
        transported_support_histograms[key] = sorted(
            [size, count] for size, count in support_histogram.items()
        )
        transported_l1_histograms[key] = sorted(
            [size, count] for size, count in l1_histogram.items()
        )
        transported_minimum_records[key] = [list(words) for words in minimum]

    operation_counts = {
        str(rank): len(operations) for rank, operations in operation_sets.items()
    }
    ledger = {
        "pins": PINS,
        "scope": (
            "complete first-four-Hamming cubes on the 56 mixed plus 32 pure "
            "chart25 first-neighbour columns, for both selected orders"
        ),
        "balanced_columns": {
            "mixed": len(mixed_columns),
            "pure_anchor": len(pure_columns),
            "total": len(raw_columns),
            "four_cubes": len(cube_records),
            "distinct_literal_vertices": len(literal_columns),
            "target_active_vertex_histogram": sorted(
                [count, cubes] for count, cubes
                in target_active_vertex_histogram.items()
            ),
        },
        "first_possible_grade_change": {
            "endpoint_changes": 4,
            "per_endpoint": [2, 2],
            "selected_orders": [[2, 1], [1, 2]],
            "selected_vertex_mask": 15,
            "proper_face_reaches_selected_grade": False,
        },
        "literal_operation_inventory": {
            "rank1_Hamming_differences": operation_counts["1"],
            "rank2_cubical_square_differences": operation_counts["2"],
            "rank3_faces": operation_counts["3"],
            "rank4_fourhole_differences": operation_counts["4"],
            "pure_anchor_columns_included": len(pure_columns),
            "allword_fourhole_rows": "729 words x 9 label pairs; grade zero",
            "committed_cap_Bianchi_identities": 10,
            "ordinary_residue": 0,
            "normalized_w": 0,
        },
        "transported_bridge": {
            "choices_per_selected_order": 144,
            "target": 0,
            "pure_anchor_incidence": 0,
            "balanced_chart25_rows": 0,
            "off_fibre_support_histograms": transported_support_histograms,
            "off_fibre_l1_histograms": transported_l1_histograms,
            "minimum_support": 775,
            "minimum_records": transported_minimum_records,
        },
        "primitive_dual": {
            "formula": "pure_anchor_incidence + sum(labelled_targets)",
            "on_every_literal_vertex_and_operation": 0,
            "on_required_C_rel_lower_face": str(desired_pairing),
            "primitive": True,
        },
        "verdict": (
            "the unique first-order four-Hamming transport reaches one "
            "repeated selected endpoint grade only after turning every pure "
            "anchor into a mixed target-zero column; it therefore loses the "
            "required -1 anchor incidence and retains at least 775 off-fibre "
            "rows. Hamming, four-hole, pure-anchor and Bianchi combinations "
            "cannot repair this because the primitive dual annihilates their "
            "complete literal image"
        ),
        "minimal_new_generator": (
            "a genuinely source-labelled grade-changing relative cell with "
            "pure-anchor incidence -1 and target=ores=w=0; it is not a finite "
            "difference of the first-four-Hamming literal columns"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"first-four-hole ledger changed: {digest}")
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    inventory = ledger["literal_operation_inventory"]
    print("chart25 first four-hole grade-change obstruction: PASS")
    print("balanced first-neighbour columns: 56 mixed + 32 pure")
    print("literal four-cubes: 176; selected vertex only at mask 15")
    print("operation counts:", inventory)
    print("transported bridge: target=anchor=0; minimum tail=775")
    print("primitive dual on required C_rel lower face: -1")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
