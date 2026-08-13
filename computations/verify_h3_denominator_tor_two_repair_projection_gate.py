#!/usr/bin/env python3
"""Exact two-output quotient of the five-face denominator transgression.

The full five-face Tor map is stronger than Gate I needs.  For any chosen
surjection pi:F=Q^5 -> P=Q^2, put U=ker(pi).  Modulo the ten unselected
denominator columns and b_sel(U), the two section columns define

    beta:P -> coker[b_oth, b_sel|U].

Then pi(im Tor) = ker(beta).  Thus the desired rank-two image is equivalent
to two column memberships, and failure over a field has an exact left-
covector certificate.  This checker verifies the algebra exhaustively in
small quotient models and audits the two known rational denominator packets.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_denominator_tor_transgression_fitting_gate.py":
        "33cd6ac3de85f83ee16189601930938d73f35f2fef5db20253380801bdd78459",
    "computations/verify_h3_single_koszul_cell_face_star_no_go.py":
        "5b94a8b213213ce64dd8536baf638e619a4773a2dfc4a2318e1820742f8f8165",
    "computations/verify_h3_shared_repair_residue_scope_and_fan_q_independence.py":
        "f78869532f809e1fffabe914521a1e7361815bbe187dbb72140d693975e0c2e7",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py":
        "673b30ac4b68c8a3af42e9c0803b3d5a39796b366b3ac15b5fd8b31b02d8df5d",
    "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py":
        "96280ef01c70b4f3381e6d85d2c9fb64b1620850305a4346601fccbd7d63dc44",
}
EXPECTED_LEDGER_SHA256 = (
    "4a2abb7eedf6864d349f897059ac318248050242b701ca030e90109f5f3bf354"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def unit(index: int, width: int = 5):
    return tuple(Q(int(position == index)) for position in range(width))


def matrix_columns(matrix, indices):
    return tuple(tuple(row[index] for row in matrix) for index in indices)


def linear_column(matrix, selected, coefficient):
    return tuple(sum((Q(coefficient[position]) * row[selected[position]]
                      for position in range(5)), Q(0))
                 for row in matrix)


def column_rank(tor, columns):
    if not columns:
        return 0
    return tor.matrix_rank(tuple(zip(*columns, strict=True)))


def membership(tor, base, candidate):
    return column_rank(tor, base) == column_rank(tor, base + (candidate,))


PROJECTIONS = {
    # Two relabelled-chart seed representatives.  This is an abstract
    # two-seed quotient; no committed map places it in B0,...,B5.
    "seed_faces_1_2": {
        "section": (unit(0), unit(1)),
        "kernel": (unit(2), unit(3), unit(4)),
        "map": lambda row: (row[0], row[1]),
    },
    # The only presently evaluated denominator-tail placement in the
    # canonical faces-(3,5) component: face 3 -> B4 and face 5 -> B1.
    "evaluated_tail_faces_3_5": {
        "section": (unit(2), unit(4)),
        "kernel": (unit(0), unit(1), unit(3)),
        "map": lambda row: (row[2], row[4]),
    },
    # Stabilizer-invariant orbit sums for 12112, A={1,3,4}, B={2,5}.
    "word_orbit_sums_A_B": {
        "section": (unit(0), unit(1)),
        "kernel": (
            add(unit(2), scale(-1, unit(0))),
            add(unit(3), scale(-1, unit(0))),
            add(unit(4), scale(-1, unit(1))),
        ),
        "map": lambda row: (
            row[0] + row[2] + row[3], row[1] + row[4]
        ),
    },
}


def projection_audit(tor, matrix, transgression_rows):
    selected = tor.label_indices(tor.SELECTED)
    other = tuple(index for index in range(15) if index not in selected)
    other_columns = matrix_columns(matrix, other)
    records = {}
    for name, data in PROJECTIONS.items():
        kernel_columns = tuple(
            linear_column(matrix, selected, vector)
            for vector in data["kernel"]
        )
        section_columns = tuple(
            linear_column(matrix, selected, vector)
            for vector in data["section"]
        )
        base = other_columns + kernel_columns
        memberships = tuple(
            membership(tor, base, column) for column in section_columns
        )
        projected_rows = tuple(data["map"](row)
                               for row in transgression_rows)
        projected_rank = tor.matrix_rank(projected_rows)
        require((memberships == (True, True)) == (projected_rank == 2),
                ("two-membership theorem failed", name, memberships,
                 projected_rank))
        records[name] = {
            "projected_rank": projected_rank,
            "two_section_memberships": list(memberships),
            "base_rank": column_rank(tor, base),
            "projected_rows": [list(map(str, row))
                               for row in projected_rows if any(row)],
        }
    return records


def packet_audit(tor, name):
    expected = tor.PACKET_EXPECTATIONS[name]
    matrix = tor.denominator_matrix(tor.sparse_value(expected["rows"]))
    kernel = tor.nullspace(matrix)
    selected = tor.label_indices(tor.SELECTED)
    transgression_rows = tuple(
        tuple(vector[index] for index in selected) for vector in kernel
    )
    total_rank = tor.matrix_rank(transgression_rows)
    require(total_rank == expected["transgression_rank"],
            (name, "total transgression rank changed"))
    return {
        "total_five_face_rank": total_rank,
        "projections": projection_audit(tor, matrix, transgression_rows),
    }


def universal_audit(tor):
    matrix = tor.denominator_matrix(tor.generic_value)
    # The universal denominator map is injective, so its Tor image is zero.
    records = projection_audit(tor, matrix, ())
    require(all(record["projected_rank"] == 0
                and record["two_section_memberships"] == [False, False]
                for record in records.values()),
            "the universal injective presentation acquired a two-output lift")
    return records


def quotient_covector_audit(tor):
    """Exhaust every binary beta:P^2 -> Q^h for 0<=h<=3.

    In the full-source theorem beta is the two-column map after quotienting
    the output by J(ker r).  Its kernel is precisely r(ker J).  A nonzero
    row is the descended output covector witnessing failure.
    """
    total = 0
    zero_maps = 0
    failures_with_covector = 0
    rank_histogram = {0: 0, 1: 0, 2: 0}
    for height in range(4):
        for entries in product((Q(0), Q(1)), repeat=2 * height):
            matrix = tuple(tuple(entries[2 * row:2 * row + 2])
                           for row in range(height))
            rank = tor.matrix_rank(matrix)
            rank_histogram[rank] += 1
            total += 1
            kernel_dimension = 2 - rank
            onto = kernel_dimension == 2
            is_zero = not any(entries)
            require(onto == is_zero,
                    ("beta zero/surjectivity equivalence failed", matrix))
            if is_zero:
                zero_maps += 1
                continue
            covector = next(row for row in matrix if any(row))
            for vector in tor.nullspace(matrix):
                require(sum((left * right for left, right
                             in zip(covector, vector, strict=True)), Q(0)) == 0,
                        ("quotient covector missed projected kernel", matrix))
            failures_with_covector += 1
    require((total, zero_maps, failures_with_covector) == (85, 4, 81),
            "the exhaustive two-output quotient census changed")
    return {
        "binary_quotient_maps_checked": total,
        "zero_maps_rank_two_image": zero_maps,
        "nonzero_maps_with_covector": failures_with_covector,
        "rank_histogram": rank_histogram,
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    tor = load(
        "computations/verify_h3_denominator_tor_transgression_fitting_gate.py",
        "two_repair_tor",
    )
    ledger = {
        "theorem": "two-output denominator Tor membership/covector gate",
        "pins": PINS,
        "full_source_criterion": {
            "setup": "r:X->P rank 2, K=ker(r), section s:P->X",
            "quotient": "C=coker(J|K), beta=[J*s]:P->C",
            "identity": "r(ker J)=ker beta",
            "rank_two_iff": [
                "J*s(d_fixed) belongs to J(K)",
                "J*s(d_pair) belongs to J(K)",
            ],
            "field_failure_alternative": (
                "lambda*J|K=0 and nonzero c=lambda*J*s in P*; "
                "then c annihilates r(ker J)"
            ),
        },
        "abstract_covector_census": quotient_covector_audit(tor),
        "universal_injective_denominator": universal_audit(tor),
        "direct_free": packet_audit(tor, "direct_free"),
        "tilted": packet_audit(tor, "tilted"),
        "scope": {
            "full_S5_surjectivity_required": False,
            "abstract_seed_projection_closes_both_packets": True,
            "evaluated_faces_3_5_projection_closes_direct_free": True,
            "evaluated_faces_3_5_projection_closes_tilted": False,
            "physical_fixed_pair_placement_constructed": False,
            "Hall_or_active_rows_force_two_memberships": False,
            "reason": (
                "the committed active-fan theorem types downstream target/"
                "exchange carriers but proves no equality of either chosen "
                "selected denominator column modulo the full zero-readout "
                "source image"
            ),
        },
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("two-output denominator Tor ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 denominator Tor two-repair projection gate: PASS")
    print("weak criterion: two full-source quotient memberships")
    print("direct-free total/projection(3,5): 4/2")
    print("tilted total/projection(3,5): 3/1")
    print("abstract seed projection: rank 2 on both packets")
    print("Hall/active rows do not type the two B-label sections")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
