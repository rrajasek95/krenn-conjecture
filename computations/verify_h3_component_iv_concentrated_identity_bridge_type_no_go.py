#!/usr/bin/env python3
"""Type obstruction to using the concentrated unit as Component-IV n_c.

The universal concentrated identity is an ordinary scalar coefficient-ring
identity of q-edge degree seven.  Any ordinary q-cell polarization lowers
that degree but preserves cap degree zero and denominator-relative degree
zero.  Duplicating it on the two charts is chart-neutral; antisymmetrizing
the copies produces a chart kernel, but still has cap/denominator degree
zero.  The Component-IV bridge has initial h_v of q-degree two and must be
chart-odd, cap-degree one, and denominator-relative.

Thus five q polarizations can match the scalar q-degree, but no number of
such polarizations can match the relative source type.  Declaring the
chart-odd kernel to be physical Yw is exactly the primitive missing column
detected by lambda(E,W,T,O)=E+W+T-O.
"""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import verify_h3_component_iv_physical_definability_gate as GATE
import verify_uniform_diagonal_aggregate_offdiagonal_universal_fine_span as UNIT


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIGEST = "3f63f74ba8a775c97f91f54486fb2782ea40ac9afe529d2c460adecc6ddc794c"
PINS = {
    "computations/verify_uniform_diagonal_aggregate_offdiagonal_universal_fine_span.py":
        "a4407c5e7d69057a243d61d102a66230ab34e8504f1bed53f2f55ab31dd5e197",
    "notes/uniform-diagonal-aggregate-offdiagonal-universal-fine-span.md":
        "379e3d13cbf7df2fdeea2f8fd4d370ba3c4ad6e8288fbaf0ef55ba3ce62d5913",
    "computations/verify_h3_component_iv_first_new_source_row_no_go.py":
        "42d168c0f5ee3f18ca5e9e1e2990efcdf1ab8a581fb8ed47ce354b036a5afe5b",
    "notes/h3-component-iv-first-new-source-row-no-go.md":
        "a307c5a515be7320463c08d0428d9fbe1727e199a2a4636af699de74d11255b1",
    "computations/verify_h3_component_iv_cyclotomic_rees_lift_physical_separator.py":
        "12f7edba228a034523c61f10fc7633c7c736516dd3890ab3a89fce376eaa49bb",
    "notes/h3-component-iv-cyclotomic-rees-lift-physical-separator.md":
        "6e5f7b0daa37c19fbdba024f76cf5456e97931caa2c602211a5b02ac65b853e4",
    "computations/verify_h3_component_iv_physical_definability_gate.py":
        "d2753b9e885464243a471387f168531484edafa8aa4bb34d160308a128237c00",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def row_edge_degree(label):
    return 3 if label.startswith("top:") else 2


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}: {actual}")

    base = UNIT.load_base()
    tokens = {
        0: (0, 2), 1: (0, 2), 2: (0, 1), 3: (0, 1),
        4: (0, 1, 2), 5: (0, 1, 2),
    }
    target_tokens = tuple((site, colour)
                          for site, colours in tokens.items()
                          for colour in colours)
    require(len(target_tokens) == 14,
            "concentrated target fine degree stopped having fourteen tokens")
    target_site_multiplicity = Counter(site for site, _colour in target_tokens)
    require(tuple(target_site_multiplicity[site] for site in base.SITES)
            == (2, 2, 2, 2, 3, 3),
            "concentrated target site multiplicity changed")
    require(len(target_tokens) % 2 == 0,
            "concentrated target stopped having an integral edge degree")
    target_q_degree = len(target_tokens) // 2
    require(target_q_degree == 7, "concentrated target q-degree changed")

    labels = UNIT.build_complete_labels(tokens, base.SITES)
    require(len(labels) == 143, "complete concentrated row count changed")
    column_count = 0
    source_type_histogram = Counter()
    multiplier_degree_histogram = Counter()
    for label in labels:
        vertices, word = UNIT.row_word(label, base.SITES)
        consumed = {(site, colour)
                    for site, colour in zip(vertices, word, strict=True)}
        complement = tuple(token for token in target_tokens
                           if token not in consumed)
        multipliers = UNIT.token_matchings(complement)
        generator_degree = row_edge_degree(label)
        require(all(len(multiplier) + generator_degree == target_q_degree
                    for multiplier in multipliers),
                f"fine-degree column for {label} left q-degree seven")
        column_count += len(multipliers)
        source_type_histogram[label.split(":", 1)[0]] += len(multipliers)
        multiplier_degree_histogram.update(map(len, multipliers))
    require(column_count == 5230,
            "complete concentrated fine-degree column count changed")

    # Feature order: (q-edge degree, cap degree, denominator-relative mark,
    # chart parity).  Ordinary q-cell Hasse polarizations only lower the
    # first coordinate.  Antisymmetrizing two identical chart copies can
    # change parity, but creates no cap or denominator-relative cell.
    neutral_types = []
    odd_kernel_types = []
    for order in range(target_q_degree + 1):
        neutral_types.append((target_q_degree - order, 0, 0, 0))
        odd_kernel_types.append((target_q_degree - order, 0, 0, 1))
    desired_type = (2, 1, 1, 1)
    scalar_match_orders = [order for order, feature in enumerate(neutral_types)
                           if feature[0] == desired_type[0]]
    require(scalar_match_orders == [5],
            "minimum scalar q-degree match stopped being order five")
    require(desired_type not in neutral_types,
            "an ordinary concentrated polarization acquired the relative type")
    require(desired_type not in odd_kernel_types,
            "a chart-odd concentrated kernel acquired cap/denominator type")

    # The all-colour extension can enlarge the allowed internal q cells and
    # source column count, but if its columns remain ordinary top/cofactor
    # coefficient rows then the three discrete type coordinates above are
    # unchanged.  A new denominator/cap-relative row would not be an
    # extension of this identity; it would be precisely the missing datum.
    physical = GATE.source_relative_gate()["downstairs"]
    separator = tuple(map(int, physical["separator"]))
    desired_column = tuple(map(int, physical["desired_chain"]))
    separator_value = sum(a * b for a, b in
                          zip(separator, desired_column, strict=True))
    require(separator == (1, 1, 1, -1)
            and desired_column == (0, 1, 0, 0)
            and separator_value == 1,
            "primitive physical bridge separator changed")
    require(physical["physical_rank"] == 3
            and physical["rank_after_chain"] == 4
            and abs(int(physical["determinant_after_chain"])) == 1,
            "physical bridge gap stopped being primitive")

    required_faces = [
        {"deleted_site": 1, "face_word": "2112"},
        {"deleted_site": 2, "face_word": "1112"},
        {"deleted_site": 3, "face_word": "1212"},
        {"deleted_site": 4, "face_word": "1212"},
        {"deleted_site": 5, "face_word": "1211"},
    ]

    ledger = {
        "scope": "typed bridge from the universal concentrated source identity to Component IV",
        "concentrated_identity": {
            "fine_tokens": {str(site): list(colours)
                            for site, colours in tokens.items()},
            "site_multiplicity": [target_site_multiplicity[site]
                                  for site in base.SITES],
            "target_q_edge_degree": target_q_degree,
            "source_rows": len(labels),
            "fine_degree_columns": column_count,
            "source_type_histogram": dict(sorted(source_type_histogram.items())),
            "multiplier_degree_histogram": dict(
                sorted(multiplier_degree_histogram.items())
            ),
            "cap_degree": 0,
            "denominator_relative_mark": 0,
            "chart_parity": "neutral/unlabelled",
            "physical_target_and_ores_maps": "not defined on this scalar identity",
        },
        "ordinary_q_polarization_types": [list(feature)
                                          for feature in neutral_types],
        "chart_antisymmetrized_kernel_types": [list(feature)
                                               for feature in odd_kernel_types],
        "desired_component_iv_type": list(desired_type),
        "first_matching_q_degree_order": scalar_match_orders[0],
        "type_membership": False,
        "reason": (
            "ordinary q polarizations preserve cap-degree 0 and denominator mark 0; "
            "chart antisymmetrization changes only parity and remains a comparison kernel"
        ),
        "all_colour_scope_guard": (
            "enlarging internal q colours does not alter this no-go while every new column "
            "is still an ordinary top/cofactor coefficient row"
        ),
        "physical_separator": list(separator),
        "attempted_chart_odd_to_Yw_column": list(desired_column),
        "separator_value": separator_value,
        "physical_rank_change": [physical["physical_rank"],
                                 physical["rank_after_chain"]],
        "primitive_gap": True,
        "minimal_extra_source_row": {
            "type": "five face-labelled denominator-relative cap-degree-one rows tau_v",
            "initial_boundary": "h_v*Y_0+delta(eta_v)+higher/full-nine rows",
            "target": 0,
            "ordinary_residue": 0,
            "faces": required_faces,
        },
        "verdict": (
            "polarizing the universal concentrated identity cannot promote the all-order "
            "chart comparison to physical Yw; the primitive n_c row remains genuinely new"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 Component-IV concentrated-identity bridge type audit: PASS")
    print("concentrated identity: q-degree 7, cap/denominator degrees 0/0")
    print("q-degree 2 first occurs after five polarizations, still type-incompatible")
    print("chart antisymmetrization: comparison kernel, not physical Yw")
    print("primitive physical separator value: 1")
    print("minimal new row: five denominator-relative cap-degree-one tau_v")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
