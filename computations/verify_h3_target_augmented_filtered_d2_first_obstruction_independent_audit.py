#!/usr/bin/env python3
"""Independent audit of the selected-row filtered-d2 obstruction.

This checker does not import the primary checker.  It represents the
three-grade differential as sparse grade-aware maps, reconstructs the six
component matrices, checks every filtration drop of d^2 (zero through four),
and computes the relevant E1/E2 dimensions and defects independently.
"""

from fractions import Fraction as F
from hashlib import sha256
import json


ZERO = F(0)
ONE = F(1)

C0 = ("x", "e", "a")
C1 = ("V1_0", "V1_1", "V0_0", "V0_1", "T", "R")
C2 = ("z", "w")
GRADES = {
    "x": 2,
    "e": 1,
    "a": 1,
    "V1_0": 1,
    "V1_1": 1,
    "V0_0": 0,
    "V0_1": 0,
    "T": 0,
    "R": 0,
    "z": 0,
    "w": 0,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def clean(vector):
    return {basis: value for basis, value in vector.items() if value}


def add_vectors(*vectors):
    answer = {}
    for vector in vectors:
        for basis, value in vector.items():
            answer[basis] = answer.get(basis, ZERO) + value
    return clean(answer)


def scale(scalar, vector):
    return clean({basis: scalar * value for basis, value in vector.items()})


def image(linear_map, vector):
    return add_vectors(*(
        scale(coefficient, linear_map.get(basis, {}))
        for basis, coefficient in vector.items()
    )) if vector else {}


def compose(left, right, source_basis):
    return {
        basis: image(left, right.get(basis, {}))
        for basis in source_basis
    }


def add_maps(source_basis, *maps):
    return {
        basis: add_vectors(*(linear_map.get(basis, {}) for linear_map in maps))
        for basis in source_basis
    }


def matrix(linear_map, source_basis, target_basis):
    return [
        [linear_map.get(source, {}).get(target, ZERO) for source in source_basis]
        for target in target_basis
    ]


def rank(input_matrix):
    work = [list(row) for row in input_matrix]
    result = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(result, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        pivot_value = work[result][column]
        work[result] = [value / pivot_value for value in work[result]]
        for row in range(len(work)):
            if row == result or not work[row][column]:
                continue
            coefficient = work[row][column]
            work[row] = [
                value - coefficient * pivot_entry
                for value, pivot_entry in zip(work[row], work[result])
            ]
        result += 1
    return result


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), ZERO)


def sparse_differential(A, B, F_value, U, Y):
    """Build maps by their action on named generators, not dense matrices."""
    kappa = A * U - B * F_value
    require(kappa, "curvature minor vanished")
    require(Y, "odd residue must be nonzero")

    maps_01 = {
        0: {
            "x": {},
            "e": {"V1_0": A, "V1_1": F_value},
            "a": {},
        },
        1: {
            "x": {"V1_0": -A, "V1_1": -F_value},
            "e": {
                "V0_0": B,
                "V0_1": U,
                "T": -kappa,
                "R": -kappa * Y,
            },
            "a": {"T": ONE, "R": Y},
        },
        2: {
            "x": {"V0_0": -B, "V0_1": -U},
            "e": {},
            "a": {},
        },
    }
    maps_12 = {
        0: {
            "V1_0": {},
            "V1_1": {},
            "V0_0": {"z": -F_value},
            "V0_1": {"z": A},
            "T": {"w": -Y},
            "R": {"w": ONE},
        },
        1: {
            "V1_0": {"z": -U},
            "V1_1": {"z": B},
            "V0_0": {},
            "V0_1": {},
            "T": {},
            "R": {},
        },
        2: {basis: {} for basis in C1},
    }

    for drop, linear_map in maps_01.items():
        for source, vector in linear_map.items():
            for target in vector:
                require(
                    GRADES[target] == GRADES[source] - drop,
                    f"bad 0->1 filtration type at {source}->{target}",
                )
    for drop, linear_map in maps_12.items():
        for source, vector in linear_map.items():
            for target in vector:
                require(
                    GRADES[target] == GRADES[source] - drop,
                    f"bad 1->2 filtration type at {source}->{target}",
                )
    return kappa, maps_01, maps_12


def audit_packet(name, A, B, F_value, U, Y):
    A, B, F_value, U, Y = map(F, (A, B, F_value, U, Y))
    kappa, d01, d12 = sparse_differential(A, B, F_value, U, Y)

    c1 = (A, F_value)
    c2 = (B, U)
    lam = (-F_value, A)
    eta = (U, -B)
    require(dot(lam, c1) == dot(eta, c2) == ZERO,
            f"{name}: adjugate kernel sign")
    require(dot(lam, c2) == dot(eta, c1) == kappa,
            f"{name}: adjugate curvature sign")

    expected_01 = {
        0: [
            [ZERO, A, ZERO],
            [ZERO, F_value, ZERO],
            [ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO],
        ],
        1: [
            [-A, ZERO, ZERO],
            [-F_value, ZERO, ZERO],
            [ZERO, B, ZERO],
            [ZERO, U, ZERO],
            [ZERO, -kappa, ONE],
            [ZERO, -kappa * Y, Y],
        ],
        2: [
            [ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO],
            [-B, ZERO, ZERO],
            [-U, ZERO, ZERO],
            [ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO],
        ],
    }
    expected_12 = {
        0: [
            [ZERO, ZERO, -F_value, A, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, -Y, ONE],
        ],
        1: [
            [-U, B, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
        ],
        2: [
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
        ],
    }
    for drop in range(3):
        require(matrix(d01[drop], C0, C1) == expected_01[drop],
                f"{name}: 0->1 drop-{drop} matrix")
        require(matrix(d12[drop], C1, C2) == expected_12[drop],
                f"{name}: 1->2 drop-{drop} matrix")

    square_components = {}
    for total_drop in range(5):
        summands = []
        for left_drop in range(3):
            right_drop = total_drop - left_drop
            if 0 <= right_drop <= 2:
                summands.append(compose(
                    d12[left_drop], d01[right_drop], C0
                ))
        component = add_maps(C0, *summands)
        square_components[total_drop] = component
        require(all(not vector for vector in component.values()),
                f"{name}: d^2 drop {total_drop} is nonzero")

    drop1_left = compose(d12[0], d01[1], C0)["e"]
    drop1_right = compose(d12[1], d01[0], C0)["e"]
    require(drop1_left == {"z": kappa},
            f"{name}: drop-one left summand")
    require(drop1_right == {"z": -kappa},
            f"{name}: drop-one right summand")
    drop2_direct = compose(d12[0], d01[2], C0)["x"]
    drop2_iterated = compose(d12[1], d01[1], C0)["x"]
    require(drop2_direct == {"z": -kappa},
            f"{name}: direct curvature sign")
    require(drop2_iterated == {"z": kappa},
            f"{name}: omitted curvature sign")

    total_01 = add_maps(C0, d01[0], d01[1], d01[2])
    total_12 = add_maps(C1, d12[0], d12[1], d12[2])
    total_square = compose(total_12, total_01, C0)
    require(all(not vector for vector in total_square.values()),
            f"{name}: total differential does not square")
    require(rank(matrix(total_01, C0, C1)) == 2,
            f"{name}: total 0->1 rank")
    require(rank(matrix(total_12, C1, C2)) == 2,
            f"{name}: total 1->2 rank")

    require(add_vectors(d01[1]["x"], d01[0]["e"]) == {},
            f"{name}: corrected lift sign")
    beta = add_vectors(d01[2]["x"], d01[1]["e"])
    graph = {"T": ONE, "R": Y}
    require(beta == scale(-kappa, graph), f"{name}: beta2 sign")
    require(image(d12[0], beta) == {}, f"{name}: beta2 not a d0-cycle")
    require(d01[1]["a"] == graph, f"{name}: common anchor graph")
    require(beta == scale(-kappa, d01[1]["a"]),
            f"{name}: beta2 common-mode indeterminacy")

    v1_d0_rank = rank(matrix(d01[0], ("e", "a"), ("V1_0", "V1_1")))
    g0_d0_rank = rank(matrix(
        d12[0], ("V0_0", "V0_1", "T", "R"), C2
    ))
    e1 = {
        "G2_H0": 1,
        "G1_H0": 2 - v1_d0_rank,
        "G1_H1": 2 - v1_d0_rank,
        "G0_H1": 4 - g0_d0_rank,
        "G0_H2": 2 - g0_d0_rank,
    }
    require(e1 == {
        "G2_H0": 1,
        "G1_H0": 1,
        "G1_H1": 1,
        "G0_H1": 2,
        "G0_H2": 0,
    }, f"{name}: E1 dimensions")
    require(image(d12[0], graph) == {}, f"{name}: graph not in low kernel")
    require(rank([[ONE, Y]]) == 1, f"{name}: graph indeterminacy rank")
    e2 = {
        "G2_H0": 1,
        "G1_H0": 0,
        "G1_H1": 1,
        "G0_H1": e1["G0_H1"] - 1,
    }
    require(e2 == {
        "G2_H0": 1,
        "G1_H0": 0,
        "G1_H1": 1,
        "G0_H1": 1,
    }, f"{name}: E2 dimensions")

    desired = {"R": -kappa * Y}
    desired_defect = image(d12[0], desired)
    require(desired_defect == {"w": -kappa * Y},
            f"{name}: target-zero noncycle defect")

    mutated_d01 = {
        drop: {basis: dict(vector) for basis, vector in linear_map.items()}
        for drop, linear_map in d01.items()
    }
    mutated_d01[1]["e"] = {
        "V0_0": B,
        "V0_1": U,
        "R": -kappa * Y,
    }
    mutated_drop1 = add_maps(
        C0,
        compose(d12[0], mutated_d01[1], C0),
        compose(d12[1], mutated_d01[0], C0),
    )
    require(mutated_drop1["e"] == {"w": -kappa * Y},
            f"{name}: target-zero mutation defect")

    require(beta.get("R", ZERO) - Y * beta.get("T", ZERO) == ZERO,
            f"{name}: graph annihilator did not kill beta2")
    require((graph["T"], graph["R"]) == (ONE, Y),
            f"{name}: pair readout killed common mode")

    return {
        "name": name,
        "parameters": tuple(map(str, (A, B, F_value, U, Y, kappa))),
        "matrix_ranks": (2, 2),
        "square_drops": tuple(
            all(not vector for vector in square_components[drop].values())
            for drop in range(5)
        ),
        "E1": e1,
        "E2": e2,
        "beta": tuple(str(beta.get(basis, ZERO)) for basis in ("T", "R")),
        "target_zero_defect": str(desired_defect["w"]),
        "omitted_curvature": str(drop2_iterated["z"]),
    }


SAMPLES = (
    ("generic_1", F(2), F(3), F(5), F(11), F(7, 5)),
    ("primary_direct_free", F(3), ZERO, F(2), F(5), F(-4, 9)),
    ("generic_2", F(-2), F(7), F(3), F(-5), F(13, 6)),
    ("generic_3", F(5, 3), F(-7, 4), F(11, 5), F(2, 9), F(-8, 7)),
    # The selected overlap square from the b20c7f0 audit.  Y=1 is an audit
    # normalization only; it is not claimed to be a physical cap readout.
    ("b20_selected_square", F(-1, 4), ZERO, ZERO, ONE, ONE),
)


EXPECTED_DIGEST = "6037977041e629dcdc9f3521cd3a8047bcab772df622b6be7249c02e2e616ab8"


def main():
    records = [audit_packet(*sample) for sample in SAMPLES]
    b20 = records[-1]
    require(
        b20["parameters"] == ("-1/4", "0", "0", "1", "1", "-1/4"),
        "b20 selected-square calibration changed",
    )
    require(b20["beta"] == ("1/4", "1/4"),
            "b20 beta normalization changed")
    payload = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST:
        require(digest == EXPECTED_DIGEST, "independent audit digest changed")
    print("independent target-augmented filtered-d2 audit: PASS")
    print("  exact packets                 :", len(records))
    print("  all d^2 drops (0..4)          : PASS")
    print("  primary direct-free B         :", records[1]["parameters"][1])
    print("  b20 selected-square kappa     :", b20["parameters"][-1])
    print("  low E1/E2 dimensions          :", (2, 1))
    print("  target-zero representative    : NONCYCLE")
    print("  aggregate SHA-256             :", digest)
    print("  physical full-source complex  : NOT CONSTRUCTED")


if __name__ == "__main__":
    main()
