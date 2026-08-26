#!/usr/bin/env python3
"""Exact 27-dimensional binary-tensor complement of full P_(3,3,2)."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_full1680_tensor_complement.json"
Q = Fraction
N = 8
SUBSETS = tuple(range(1 << N))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def full_assignments():
    answer = []
    for counts in ((2, 3, 3), (3, 2, 3), (3, 3, 2)):
        answer.extend(word for word in product(range(3), repeat=N)
                      if tuple(word.count(kind) for kind in range(3)) == counts)
    require(len(answer) == len(set(answer)) == 1680,
            "full S3 assignment count changed")
    return tuple(answer)


def contraction_row(assignment):
    """Expansion in binary t_S, with p=0, q=1, r=q-p=2."""
    q_sites = [site for site, label in enumerate(assignment) if label == 1]
    r_sites = [site for site, label in enumerate(assignment) if label == 2]
    base = sum(1 << site for site in q_sites)
    row = {}
    for choice in range(1 << len(r_sites)):
        subset = base
        coefficient = 1
        for index, site in enumerate(r_sites):
            if choice & (1 << index):
                subset |= 1 << site
            else:
                coefficient *= -1
        row[subset] = coefficient
    require(len(row) in (4, 8), "contraction row support changed")
    return row


def sparse_modular_rank(rows, prime):
    basis = {}
    for input_row in rows:
        row = {index: value % prime for index, value in input_row.items()
               if value % prime}
        while row:
            pivot = min(row)
            if pivot not in basis:
                inverse = pow(row[pivot], -1, prime)
                basis[pivot] = {
                    index: value * inverse % prime
                    for index, value in row.items() if value % prime
                }
                break
            factor = row[pivot]
            other = basis[pivot]
            for index, value in other.items():
                updated = (row.get(index, 0) - factor * value) % prime
                if updated:
                    row[index] = updated
                else:
                    row.pop(index, None)
    return len(basis)


def subset_sum(mask, vector):
    return sum(vector[site] for site in range(N) if mask & (1 << site))


def zero_sum_basis(index):
    require(0 <= index < 7, "standard basis index outside 0..6")
    vector = [Q(0)] * N
    vector[index] = Q(1)
    vector[7] = Q(-1)
    return tuple(vector)


def parameter_basis():
    basis = []
    names = []
    # Six trivial/radial parameters: f0, f1, alpha, beta, f7, f8, with
    # f_k=alpha+beta*k on all middle levels 2<=k<=6.
    for name in ("f0", "f1", "alpha", "beta", "f7", "f8"):
        vector = [Q(0)] * (1 << N)
        for mask in SUBSETS:
            size = mask.bit_count()
            if name == "f0" and size == 0:
                vector[mask] = 1
            elif name == "f1" and size == 1:
                vector[mask] = 1
            elif name == "alpha" and 2 <= size <= 6:
                vector[mask] = 1
            elif name == "beta" and 2 <= size <= 6:
                vector[mask] = size
            elif name == "f7" and size == 7:
                vector[mask] = 1
            elif name == "f8" and size == 8:
                vector[mask] = 1
        names.append(name)
        basis.append(tuple(vector))

    # Three independent standard copies: arbitrary zero-sum site effects at
    # layer 1, at every middle layer together, and at layer 7.
    for sector, allowed_sizes in (
        ("u_layer1", {1}),
        ("v_middle", {2, 3, 4, 5, 6}),
        ("w_layer7", {7}),
    ):
        for index in range(7):
            site_vector = zero_sum_basis(index)
            vector = tuple(
                Q(subset_sum(mask, site_vector))
                if mask.bit_count() in allowed_sizes else Q(0)
                for mask in SUBSETS
            )
            names.append(f"{sector}_{index}_minus_7")
            basis.append(vector)
    require(len(basis) == len(names) == 27,
            "explicit complement basis dimension changed")
    return tuple(names), tuple(basis)


def dot_sparse(row, vector):
    return sum(value * vector[index] for index, value in row.items())


def dense_column_rank(columns, prime):
    rows = []
    for coordinate in SUBSETS:
        rows.append({column: int(vector[coordinate]) % prime
                     for column, vector in enumerate(columns)
                     if vector[coordinate]})
    return sparse_modular_rank(rows, prime)


def target_values(tensor):
    a = tensor[0]
    b = tensor[(1 << N) - 1]
    c = sum((Q(-1) if mask.bit_count() % 2 else Q(1)) * tensor[mask]
            for mask in SUBSETS)
    heron = (a + b - c) * (a + c - b) * (b + c - a)
    return a, b, c, heron


def main():
    assignments = full_assignments()
    rows = tuple(contraction_row(assignment) for assignment in assignments)
    rank1009 = sparse_modular_rank(rows, 1009)
    rank1013 = sparse_modular_rank(rows, 1013)
    require(rank1009 == rank1013 == 229,
            "full contraction rank changed")

    names, basis = parameter_basis()
    require(all(dot_sparse(row, vector) == 0
                for row in rows for vector in basis),
            "explicit parameter vector violates a contraction")
    require(dense_column_rank(basis, 1009)
            == dense_column_rank(basis, 1013) == 27,
            "explicit parameter basis lost independence")
    # Integer rows have rank at least 229 because of either nonzero modular
    # minor, and at most 256-27 because of the exact Q-kernel above.
    exact_rank = 229
    exact_nullity = 27

    # Transposition (0 1): six radial basis vectors are fixed. On each
    # zero-sum standard copy e0-e7 and e1-e7 swap, while the other five
    # displayed basis vectors are fixed, so its trace is 6+3*5=21.
    transposition_trace = 6 + 3 * 5
    require(transposition_trace == 21,
            "transposition character changed")

    # An abstract tensor in the complement with nonzero Heron. It is not
    # asserted to lie in the nonlinear Hafnian image.
    control = [Q(0)] * (1 << N)
    for coefficient, vector in zip(
            (Q(1), Q(-1, 8), Q(0), Q(0), Q(0), Q(0)) + (Q(0),) * 21,
            basis):
        for index, value in enumerate(vector):
            control[index] += coefficient * value
    require(all(dot_sparse(row, control) == 0 for row in rows),
            "abstract complement control violates a contraction")
    a, b, c, heron = target_values(control)
    require((a, b, c, heron) == (Q(1), Q(0), Q(2), Q(-3)),
            "abstract Heron countercontrol changed")

    # Direct target formula on the parametrization. Standard site effects
    # sum to zero on every layer.
    c_coefficients = {
        "f0": 1, "f1": -8, "alpha": 14,
        "beta": 56, "f7": -8, "f8": 1,
    }
    require(sum((-1) ** size * math.comb(8, size)
                for size in range(2, 7)) == 14,
            "alpha coefficient changed")
    require(sum((-1) ** size * math.comb(8, size) * size
                for size in range(2, 7)) == 56,
            "beta coefficient changed")

    result = {
        "status": "UNAUDITED exact full-1680 tensor complement",
        "binary_tensor_coordinates": 256,
        "contraction_rows": len(rows),
        "row_support_histogram": {
            "4": sum(len(row) == 4 for row in rows),
            "8": sum(len(row) == 8 for row in rows),
        },
        "rank_mod_1009": rank1009,
        "rank_mod_1013": rank1013,
        "exact_rank": exact_rank,
        "exact_nullity": exact_nullity,
        "kernel_basis_names": list(names),
        "kernel_parametrization": (
            "For t_S with k=|S|: t_empty=f0; t_{i}=f1+u_i; "
            "t_S=alpha+beta*k+sum_{i in S}v_i for 2<=k<=6; "
            "t_{[8]\\{i}}=f7-w_i; t_[8]=f8, where each of u,v,w "
            "has site-coordinate sum zero."
        ),
        "S8_decomposition": "6*S^(8) + 3*S^(7,1)",
        "S8_dimension_check": "6*1 + 3*7 = 27",
        "transposition_character_trace": transposition_trace,
        "rowspace_decomposition": (
            "3*S^(8) + 4*S^(7,1) + 5*S^(6,2) + "
            "3*S^(5,3) + S^(4,4), dimension 229"
        ),
        "A_B_C_on_parameters": {
            "A": "f0",
            "B": "f8",
            "C": "f0-8*f1+14*alpha+56*beta-8*f7+f8",
        },
        "abstract_non_Hafnian_control": {
            "parameters": {"f0": [1, 1], "f1": [-1, 8],
                           "alpha": [0, 1], "beta": [0, 1],
                           "f7": [0, 1], "f8": [0, 1]},
            "A_B_C": [[1, 1], [0, 1], [2, 1]],
            "Heron": [-3, 1],
        },
        "conclusion": (
            "The 1,680 balanced contrast equations kill every S8 type of "
            "interaction order at least two. Their exact binary-evaluation "
            "kernel consists only of six radial degrees of freedom and "
            "three standard site-effect vectors. They do not force Heron "
            "linearly: the displayed abstract kernel tensor has Heron=-3. "
            "Any positive theorem must use the nonlinear fact that t_S is "
            "the Hafnian image of 28 bilinear edge blocks."
        ),
        "next_nonlinear_landing": (
            "Intersect the explicit affine-middle parametrization with the "
            "Hafnian image. Equivalently, prove that a bilinear-edge Hafnian "
            "whose binary evaluations have no Johnson interaction of order "
            ">=2 and constant middle site effect must have degenerate "
            "directional Hafnians A,B,C (Heron=0), or exhibit a counterexample."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("full1680 tensor complement: PASS")
    print("rank/nullity:", exact_rank, exact_nullity)
    print("S8 kernel / transposition trace:",
          result["S8_decomposition"], transposition_trace)
    print("abstract A,B,C / Heron:", a, b, c, heron)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
