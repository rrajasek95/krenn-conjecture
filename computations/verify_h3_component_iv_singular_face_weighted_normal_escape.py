#!/usr/bin/env python3
"""Weighted-normal escape for the singular Component-IV face-zero strata.

The five h_v are literal marked Schur polars of complete endpoint-word-change
rows.  At the singular support points classified in 9376a3f, this checker
constructs exact q-arcs whose first nonzero Hasse coefficients complete the
five face directions.  The cyclotomic isolated-K4 covector is hit in order
two.  Intersecting supports require order at most three.

This proves a source-row coefficient statement, not the existence of the
normal-indexed source-chain companions or a physical cap comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import verify_h3_component_iv_nondense_face_zero_strata as ND


PINS = {
    "computations/verify_h3_component_iv_nondense_face_zero_strata.py":
        "dc626a20e81628ceb5a0ca318226a1cf0f702be1b7144f09dc8e7640788fdba7",
    "notes/h3-component-iv-nondense-face-zero-strata.md":
        "d1286c98005734dab854799435adead51ec719e6e7778c510ffa42f1c13da638",
    "computations/verify_h3_component_iv_cyclotomic_word_change_relation.py":
        "335c82b382dcb3b8d69cd57a4fa54185a0db96368b5413b218b7c0f8bf303dae",
    "notes/h3-component-iv-cyclotomic-word-change-relation.md":
        "ffae52a1adeb4eef3f94f550778b04bdcfdc2bd02fb65292c174fa3c54920975",
    "computations/verify_h3_component_iv_cyclotomic_schur_face_composition.py":
        "66086a7a67e5ca05864394933d37e36b6b92b990b91169eef19b275e7c02181d",
    "notes/h3-component-iv-cyclotomic-schur-face-composition.md":
        "23f8e58768a416299fda86c04bae06528472dd18ebf7930625e98898011a212c",
    "computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py":
        "c409a62957dba0d101d1298ec16695482fce705d3131323a8d3657074f1bf2b0",
    "notes/h3-cyclotomic-regularized-shifted-filler-normal-face.md":
        "33d23d5f30afd8edc8b4e6f5599d027620587b600c87476a1adabf967820ea63",
}
EXPECTED_LEDGER_SHA256 = "29a01bfdb19f1dac157ab20ad0e876d8602d37020bc4e69f9fdd95fd1aa0ef1d"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def zero_like(example):
    return ND.QZ() if isinstance(example, ND.QZ) else Q(0)


def face_series(base, directions):
    """Exact coefficients of h(base + sum tau^k direction[k])."""
    sample = next(iter(base.values()), None)
    if sample is None:
        sample = next((value for direction in directions.values()
                       for value in direction.values()), Q(0))
    zero = zero_like(sample)
    edge_series = {}
    for edge in ND.EDGES:
        polynomial = {}
        if edge in base:
            polynomial[0] = base[edge]
        for power, direction in directions.items():
            if edge in direction:
                polynomial[power] = polynomial.get(power, zero) + direction[edge]
        edge_series[edge] = polynomial

    output = {}
    for face_index, face in enumerate(ND.FACES):
        for matching in ND.face_matchings(face):
            left, right = matching
            for left_power, left_value in edge_series[left].items():
                for right_power, right_value in edge_series[right].items():
                    power = left_power + right_power
                    if power not in output:
                        output[power] = [zero for _ in ND.FACES]
                    output[power][face_index] = (
                        output[power][face_index] + left_value * right_value
                    )
    return {power: vector for power, vector in output.items()
            if any(vector)}


def rank_columns(columns):
    if not columns:
        return 0
    return ND.matrix_rank([list(row) for row in zip(*columns, strict=True)])


def independent_jacobian_columns(base, zero=Q(0)):
    jacobian = ND.face_jacobian(base, zero)
    columns = []
    labels = []
    for edge_index, edge in enumerate(ND.EDGES):
        column = [jacobian[row][edge_index] for row in range(len(ND.FACES))]
        if rank_columns(columns + [column]) > len(columns):
            columns.append(column)
            labels.append(edge)
    return columns, labels


def vector_text(vector):
    return [entry.text() if isinstance(entry, ND.QZ) else str(entry)
            for entry in vector]


def direction_text(directions):
    return {
        str(power): {f"{edge[0]}{edge[1]}":
                     (value.text() if isinstance(value, ND.QZ) else str(value))
                     for edge, value in sorted(direction.items())}
        for power, direction in sorted(directions.items())
    }


def cyclotomic_k4_escape():
    zeta = ND.QZ(0, 1)
    base = {
        (0, 1): ND.QZ(1), (0, 2): ND.QZ(1), (0, 3): ND.QZ(1),
        (1, 2): ND.QZ(1), (1, 3): zeta, (2, 3): zeta * zeta,
    }
    # A tangent combining a support rescaling and an isolated-vertex spoke.
    tangent = {
        (0, 1): ND.QZ(1, 1), (0, 2): ND.QZ(1),
        (0, 4): ND.QZ(1), (1, 4): zeta * zeta,
        (2, 4): zeta, (3, 4): ND.QZ(1),
    }
    series = face_series(base, {1: tangent})
    require(0 not in series and 1 not in series,
            "cyclotomic K4 escape stopped being tangent to V(h)")
    second = series[2]
    expected = [ND.QZ(), ND.QZ(-2, -1), ND.QZ(1, 1), ND.QZ(1), ND.QZ()]
    require(second == expected, "cyclotomic K4 second face coefficient changed")
    covector = [ND.QZ(), ND.QZ(1), zeta, zeta * zeta, ND.QZ(1)]
    pairing = sum((left * right for left, right in zip(covector, second, strict=True)),
                  ND.QZ())
    require(pairing == ND.QZ(-4, -2) and pairing,
            "second normal coefficient stopped hitting the primitive covector")

    first_columns, first_labels = independent_jacobian_columns(base, ND.QZ())
    require(len(first_columns) == 4, "cyclotomic K4 first normal rank changed")
    require(rank_columns(first_columns + [second]) == 5,
            "cyclotomic K4 weighted normal system is not full")
    return {
        "first_normal_rank": 4,
        "first_normal_edges": first_labels,
        "primitive_covector": vector_text(covector),
        "tangent": direction_text({1: tangent}),
        "second_face_coefficient": vector_text(second),
        "covector_pairing": pairing.text(),
        "weighted_normal_degrees": [1, 1, 1, 1, 2],
        "source_row": (
            "second Hasse coefficient of the literal covariance plus five marked "
            "Schur face rows"
        ),
    }


def rational_arc(direction1, direction2=None):
    directions = {1: {edge: Q(value) for edge, value in direction1.items()}}
    if direction2:
        directions[2] = {edge: Q(value) for edge, value in direction2.items()}
    return directions


def intersecting_weighted_escape():
    bases = {
        "zero": {},
        "edge": {(0, 1): Q(1)},
        "two_star": {(0, 1): Q(1), (0, 2): Q(1)},
        "three_star": {(0, 1): Q(1), (0, 2): Q(1), (0, 3): Q(1)},
        "triangle": {(0, 1): Q(1), (0, 2): Q(1), (1, 2): Q(1)},
        "four_star": {(0, 1): Q(1), (0, 2): Q(1),
                      (0, 3): Q(1), (0, 4): Q(1)},
    }
    arcs = {
        "zero": [
            rational_arc({(0, 1): 1, (2, 3): 1}),
            rational_arc({(0, 1): 1, (2, 4): 1}),
            rational_arc({(0, 1): 1, (3, 4): 1}),
            rational_arc({(0, 2): 1, (3, 4): 1}),
            rational_arc({(1, 2): 1, (3, 4): 1}),
        ],
        "edge": [
            rational_arc({(0, 2): 1}, {(3, 4): 1}),
            rational_arc({(1, 2): 1}, {(3, 4): 1}),
        ],
        "two_star": [
            rational_arc({(0, 3): -1, (1, 4): -1, (2, 4): 1}),
            rational_arc({(1, 3): -1, (1, 4): -1,
                          (2, 3): 1, (2, 4): 1}),
        ],
        "three_star": [
            rational_arc({(1, 2): 1}, {(3, 4): 1}),
        ],
        "triangle": [
            rational_arc({(0, 3): 1, (1, 3): -1,
                          (1, 4): 1, (2, 4): -1}),
            rational_arc({(0, 3): 1, (1, 3): -1,
                          (0, 4): 1, (2, 4): -1}),
        ],
        "four_star": [
            rational_arc({(1, 2): 1, (1, 4): -1,
                          (2, 3): -1, (3, 4): 1}),
        ],
    }
    expected_first_ranks = {
        "zero": 0, "edge": 3, "two_star": 3,
        "three_star": 4, "triangle": 3, "four_star": 4,
    }
    expected_degrees = {
        "zero": [2, 2, 2, 2, 2],
        "edge": [1, 1, 1, 3, 3],
        "two_star": [1, 1, 1, 2, 2],
        "three_star": [1, 1, 1, 1, 3],
        "triangle": [1, 1, 1, 2, 2],
        "four_star": [1, 1, 1, 1, 2],
    }
    records = {}
    for name, base in bases.items():
        require(ND.face_values(base) == [Q(0)] * 5, f"{name} left V(h)")
        columns, labels = independent_jacobian_columns(base)
        require(len(columns) == expected_first_ranks[name],
                f"{name} first normal rank changed")
        arc_records = []
        degrees = [1] * len(columns)
        for directions in arcs[name]:
            series = face_series(base, directions)
            new_power = None
            new_vector = None
            for power in sorted(series):
                vector = series[power]
                if rank_columns(columns + [vector]) > len(columns):
                    new_power, new_vector = power, vector
                    break
                require(rank_columns(columns + [vector]) == len(columns),
                        f"{name}: a lower coefficient left the accumulated span")
            require(new_vector is not None,
                    f"{name}: an arc supplied no new weighted normal direction")
            columns.append(new_vector)
            degrees.append(new_power)
            arc_records.append({
                "directions": direction_text(directions),
                "all_face_coefficients": {
                    str(power): vector_text(vector)
                    for power, vector in sorted(series.items())
                },
                "first_new_power": new_power,
                "first_new_vector": vector_text(new_vector),
            })
        require(len(columns) == rank_columns(columns) == 5,
                f"{name}: weighted normal columns are not a basis")
        require(degrees == expected_degrees[name],
                f"{name}: weighted degree profile changed: {degrees}")
        records[name] = {
            "first_normal_rank": expected_first_ranks[name],
            "first_normal_edges": labels,
            "weighted_normal_degrees": degrees,
            "higher_arcs": arc_records,
        }
    return records


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    ledger = {
        "scope": "singular exact-support strata of q_m in V(h) at h=3",
        "literal_source_provenance": (
            "7ee2f87/5462b2a: each h_v is the marked polar of a complete "
            "endpoint-word-change Schur row; q-Hasse coefficients retain that provenance"
        ),
        "cyclotomic_isolated_K4": cyclotomic_k4_escape(),
        "intersecting_strata": intersecting_weighted_escape(),
        "theorem": (
            "every singular support orbit from 9376a3f has a full five-direction "
            "weighted normal system using literal face coefficients of order at most three"
        ),
        "target_and_old_ores": (
            "zero coefficientwise: the complete face words stay mixed and the two chart "
            "sectors retain opposite equal copies"
        ),
        "minimal_new_source_faces": {
            "cyclotomic_K4_and_order2_intersecting": (
                "the complete second-normal Hasse/principal-parts companion"
            ),
            "edge_and_three_star": (
                "the complete third-normal companion for the displayed triangular arcs"
            ),
        },
        "physical_promotion": (
            "not proved: weighted face coefficients are source-provenant rows, but their "
            "normal-indexed chain companions and the derived-Yw to physical-W map remain"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"singular weighted-normal ledger changed: {digest}")
    print("h3 Component-IV singular weighted-normal escape: PASS")
    print("cyclotomic isolated K4: order-2 row pairs -4-2*zeta with primitive covector")
    print("all intersecting strata: full weighted normal systems, maximum order 3")
    print("normal-indexed chain companions / physical cap comparison: OPEN")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
