#!/usr/bin/env python3
r"""REPAIR PROBE (item 3): is the D2 CORNER value -delta canonical?

UNAUDITED.  Pinned to krenn-conjecture HEAD 7d57c552a3ef57d3a95c3bc933af547ad55e087d.

Background.  verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py records
``"D2_value": "-delta=(-1,+1,+1,-1)"`` together with the hardcoded boolean
``"canonical_on_D1_homology": True``.  The external audit showed that on
ker(source, D1) the *whole* pair shadow has 488 dimensions of freedom
(rank(source+D1) = 840 vs rank(source+D1+shadow) = 1328), so "-delta" is
attainability, not equality.

The claim consumed downstream is narrower: it is the value of the shadow on
the FOUR CORNER CLASSES, not the whole shadow vector.  Write

    B_j  (j = 1..4) = indicator of the 2x2 block E_j x T_j
                      (E_+/E_- endpoint sectors, T_0/T_1 tail sectors),
    W  = span(B_1, B_2, B_3, B_4)  inside shadow-row space,
    expected_second_shadow = sum_j alpha_j B_j  with alpha = -delta.

A shadow vector has a corner value at all only if it lies in W, and then the
corner value is the unique alpha with s = sum_j alpha_j B_j.  With

    F = shadow(ker(source, D1))        (the 488-dimensional freedom)

the attainable shadows are exactly F (a linear space that contains -delta,
because the committed exact solve produces a y with source = D1 = 0 and
shadow = -delta).  So F cap W always contains the line through -delta and the
sharp question is its DIMENSION:

    dim(F cap W) = 1  and spanned by -delta
        => every attainable pure-corner shadow is a scalar multiple of -delta:
           the corner CLASS is canonical, and only its scale is a convention
           (fixed elsewhere by the augmented-HPL normalization D = 1);
    dim(F cap W) > 1
        => there are dim - 1 genuinely free corner directions and the value
           -delta is only attainable, as the external audit suspected.

Method (exact rank identities, two independent primes):

    dim F        = rank[A;S] - rank[A]
    dim(F cap W) = 4 - ( rank[M | v_1..v_4] - rank[M] )

where M is the stacked matrix (rows = source, D1 and shadow rows; columns =
operator columns) and v_j is the extra COLUMN equal to B_j on the shadow rows
and 0 on every source/D1 row.  Indeed c lies in the kernel of
c |-> [ (0, sum c_j B_j) ] in coker(M) exactly when some y has Ay = 0 and
Sy = sum c_j B_j, i.e. exactly when c is a legal change of the corner value.
Note this already imposes that the shadow is a *pure* corner class (zero on
every pair outside the four blocks, constant inside each block), so no
further "read it as an alpha" normalization can help.

Two variants of A are run:
  * "D1"          - source rows + first endpoint-Spencer rows (the committed
                    ker(source, D1) of the HPL ledger);
  * "D1+D2faces"  - additionally the second endpoint-Spencer face rows, i.e.
                    the rows the affine feasibility module itself builds under
                    its committed --second-row-elim switch.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path
import sys


REPO = Path(__file__).resolve().parents[2]
SNAP = Path("/private/tmp/claude-501/-Users-rishi/"
            "f8396279-dd28-41de-876d-5c03a4d8d65a/scratchpad/repair23/snap")
PINNED_HEAD = "7d57c552a3ef57d3a95c3bc933af547ad55e087d"

PINS = {
    "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py":
        "ef9bd416986f7dc8c07ffa3b396d1c1f92237c8e1a0539ecbb0ddbeaadb1c18e",
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
    "computations/verify_h3_residual_q_order5_generator_repair.py":
        "f4b338f557729313fa70da78caec17de861738275b89e7dc9dc97d7e2ae83267",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
}

PRIMES = ((1 << 61) - 1, 2147483647)
MISSING = frozenset(((0, 7, 1, 1), (2, 4, 1, 1)))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(
        name, SNAP / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


# ------------------------------------------------------------- linear algebra

def reduce_pivots(vectors, prime):
    pivots = {}
    for vector in vectors:
        work = {key: value % prime for key, value in vector.items()
                if value % prime}
        while work:
            head = min(work)
            if head not in pivots:
                inverse = pow(work[head], prime - 2, prime)
                pivots[head] = {key: value * inverse % prime
                                for key, value in work.items()}
                break
            row = pivots[head]
            factor = work[head]
            for key, value in row.items():
                new = (work.get(key, 0) - factor * value) % prime
                if new:
                    work[key] = new
                else:
                    work.pop(key, None)
    return pivots


def rank_of(vectors, prime):
    return len(reduce_pivots(vectors, prime))


def corner_freedom(column_pivots, blocks, prime):
    """Which c satisfy  sum_j c_j B_j  in  colspace(M) ?

    The echelon table is SEEDED with the column space of M (combination zero),
    then the four B_j are inserted one at a time with combination tracking.
    A vector that reduces to zero yields a relation sum_j c_j B_j in colspace,
    i.e. an element of F cap W; a vector that acquires a new pivot is
    independent modulo the column space.
    """
    count = len(blocks)
    pivots = {head: (vector, tuple([0] * count))
              for head, vector in column_pivots.items()}
    kernel = []
    independent = 0
    for position, block in enumerate(blocks):
        work = {key: value % prime for key, value in block.items()
                if value % prime}
        combination = [1 if index == position else 0 for index in range(count)]
        placed = False
        while work:
            head = min(work)
            if head not in pivots:
                inverse = pow(work[head], prime - 2, prime)
                work = {key: value * inverse % prime
                        for key, value in work.items()}
                combination = [value * inverse % prime
                               for value in combination]
                pivots[head] = (work, tuple(combination))
                placed = True
                independent += 1
                break
            row, row_combination = pivots[head]
            factor = work[head]
            for key, value in row.items():
                new = (work.get(key, 0) - factor * value) % prime
                if new:
                    work[key] = new
                else:
                    work.pop(key, None)
            combination = [(left - factor * right) % prime for left, right
                           in zip(combination, row_combination)]
        if not placed:
            kernel.append(tuple(combination))
    return independent, kernel


def in_column_space(column_pivots, vector, prime):
    """Full echelon membership test against a seeded pivot table."""
    pivots = dict(column_pivots)
    work = {key: value % prime for key, value in vector.items()
            if value % prime}
    while work:
        head = min(work)
        if head not in pivots:
            return False
        row = pivots[head]
        factor = work[head]
        for key, value in row.items():
            new = (work.get(key, 0) - factor * value) % prime
            if new:
                work[key] = new
            else:
                work.pop(key, None)
    return True


def signed(value, prime):
    return value - prime if value > prime // 2 else value


def modular(value, prime):
    numerator, denominator = ((value.numerator, value.denominator)
                              if hasattr(value, "numerator")
                              else (int(value), 1))
    return (numerator % prime) * pow(denominator % prime, prime - 2,
                                     prime) % prime


# ------------------------------------------------------------ the 8580 block

def build_block(second_spencer):
    sys.argv = [sys.argv[0]]
    affine = load(
        "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py",
        "d2c_affine")
    order6 = load(
        "computations/verify_h3_residual_q_order6_missing_face_probe.py",
        "d2c_order6")
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "d2c_repair")
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "d2c_commutator")
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "d2c_base")

    system = repair.build_system(base, commutator)
    sixth = order6.build_exact_sixth_derivatives(system)
    fourth = affine.exact_derivatives_of_order(system, 4)
    fifth = affine.exact_derivatives_of_order(system, 5)
    seventh = affine.exact_derivatives_of_order(system, 7)
    shadow_kind = 3 if second_spencer else 2

    metadata = set()
    for _product_index, directions in sixth:
        if not MISSING.issubset(directions):
            continue
        for coefficient in order6.eligible_coefficients(
                repair, commutator, directions):
            metadata.add((coefficient, directions))

    columns = []
    for coefficient, directions in sorted(metadata, key=repr):
        column = Counter()
        for product_index in range(3):
            for remainder, value in sixth.get(
                    (product_index, directions), {}).items():
                column[(0, product_index,
                        tuple(sorted(remainder + coefficient)))] += value
        for (composed_coefficient, composed_directions), weight in (
                affine.endpoint_composition_antisymmetric(
                    (coefficient, directions)).items()):
            for selected, multiplicity in Counter(composed_directions).items():
                remaining = list(composed_directions)
                remaining.remove(selected)
                remaining = tuple(remaining)
                table = {5: fifth, 6: sixth, 7: seventh}[len(remaining)]
                for product_index in range(3):
                    for remainder, value in table.get(
                            (product_index, remaining), {}).items():
                        column[(1, product_index, selected, tuple(sorted(
                            remainder + composed_coefficient)))] += (
                                weight * multiplicity * value)
            if second_spencer:
                removed_faces = Counter()
                for positions in combinations(
                        range(len(composed_directions)), 2):
                    removed = tuple(sorted(composed_directions[position]
                                           for position in positions))
                    remaining = tuple(
                        composed_directions[position]
                        for position in range(len(composed_directions))
                        if position not in positions)
                    removed_faces[(removed, remaining)] += 1
                for (removed, remaining), multiplicity in (
                        removed_faces.items()):
                    table = {4: fourth, 5: fifth, 6: sixth}[len(remaining)]
                    for product_index in range(3):
                        for remainder, value in table.get(
                                (product_index, remaining), {}).items():
                            column[(2, product_index, removed, tuple(sorted(
                                remainder + composed_coefficient)))] += (
                                    weight * multiplicity * value)
        for left, right in combinations(range(6), 2):
            column[(shadow_kind, tuple(sorted(
                (directions[left], directions[right]))))] += 1
        columns.append({row: value for row, value in column.items() if value})
    return columns, commutator, shadow_kind


def corner_blocks(commutator, shadow_kind):
    blocks = []
    for endpoint, tail in ((commutator.E_PLUS, commutator.T_ZERO),
                           (commutator.E_MINUS, commutator.T_ZERO),
                           (commutator.E_PLUS, commutator.T_ONE),
                           (commutator.E_MINUS, commutator.T_ONE)):
        block = {}
        for endpoint_cell in endpoint:
            for tail_cell in tail:
                block[(shadow_kind,
                       tuple(sorted((endpoint_cell, tail_cell))))] = 1
        blocks.append(block)
    supports = [frozenset(block) for block in blocks]
    require(len(set().union(*supports)) == sum(len(item) for item in supports),
            "the four corner blocks stopped having disjoint supports")
    delta_class = defaultdict(Q)
    for coefficient, block in zip(commutator.ALPHA, blocks, strict=True):
        for row, value in block.items():
            delta_class[row] += coefficient * value
    reference = {(shadow_kind, pair): value for pair, value
                 in commutator.expected_second_shadow().items()}
    require({row: value for row, value in delta_class.items() if value}
            == reference, "sum_j alpha_j B_j is not expected_second_shadow")
    return blocks, reference


# ----------------------------------------------------------------- the probe

def analyse(columns, blocks, reference, shadow_kind, prime, label):
    rows = defaultdict(dict)
    for index, column in enumerate(columns):
        for row, value in column.items():
            rows[row][index] = modular(value, prime)
    a_rows = [dict(value) for row, value in rows.items()
              if row[0] != shadow_kind]
    s_rows = [dict(value) for row, value in rows.items()
              if row[0] == shadow_kind]
    rank_a = rank_of(a_rows, prime)
    rank_as = rank_of(a_rows + s_rows, prime)

    column_vectors = [{row: modular(value, prime)
                       for row, value in column.items()} for column in columns]
    pivots = reduce_pivots(column_vectors, prime)
    independent, kernel = corner_freedom(pivots, blocks, prime)
    delta_vector = {row: modular(value, prime)
                    for row, value in reference.items()}
    delta_attainable = in_column_space(pivots, delta_vector, prime)

    return {
        "variant": label,
        "prime": prime,
        "columns": len(columns),
        "constraint_rows_A": len(a_rows),
        "shadow_rows_S": len(s_rows),
        "rank_A": rank_a,
        "rank_A_plus_S": rank_as,
        "dim_shadow_freedom_F": rank_as - rank_a,
        "rank_M_column_space": len(pivots),
        "corner_blocks_independent_mod_image_M": independent,
        "dim_F_cap_W": 4 - independent,
        "attainable_corner_directions": [
            [signed(value, prime) for value in vector] for vector in kernel],
        "free_corner_directions_beyond_scale": 4 - independent - 1,
        "corner_class_canonical_up_to_scale": (4 - independent) == 1,
        "positive_control_minus_delta_attainable": delta_attainable,
    }


def main():
    pin_report = {}
    for relative, expected in PINS.items():
        actual = sha256((REPO / relative).read_bytes()).hexdigest()
        pin_report[relative] = actual
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
        require(sha256((SNAP / relative).read_bytes()).hexdigest() == expected,
                ("snapshot drift", relative))

    variants = (("D1", False),) if "--d1-only" in sys.argv else (
        ("D1", False), ("D1+D2faces", True))
    analyses = []
    for label, second in variants:
        columns, commutator, shadow_kind = build_block(second)
        blocks, reference = corner_blocks(commutator, shadow_kind)
        print(f"[{label}] columns:", len(columns), flush=True)
        for prime in PRIMES:
            record = analyse(columns, blocks, reference, shadow_kind, prime,
                             label)
            analyses.append(record)
            print(json.dumps({key: value for key, value in record.items()
                              if key != "attainable_corner_directions"},
                             sort_keys=True), flush=True)
            print("  attainable corner directions:",
                  record["attainable_corner_directions"], flush=True)
        if label == "D1":
            delta_reference = sorted((repr(row), str(value))
                                     for row, value in reference.items())

    primary = [record for record in analyses if record["variant"] == "D1"]
    require(len({record["dim_F_cap_W"] for record in primary}) == 1,
            "the two primes disagree on dim(F cap W)")
    require(all(record["positive_control_minus_delta_attainable"]
                for record in primary),
            "positive control failed: -delta is not attainable on ker(source,D1)")
    alpha = (-1, 1, 1, -1)
    for record in primary:
        for direction in record["attainable_corner_directions"]:
            require(all(direction[i] * alpha[j] == direction[j] * alpha[i]
                        for i in range(4) for j in range(4)),
                    ("an attainable corner direction is not proportional to "
                     "-delta", direction))

    ledger = {
        "probe": "repair item 3: canonicity of the D2 corner value",
        "variants_run": [label for label, _second in variants],
        "status": "UNAUDITED REPAIR PROBE",
        "pinned_head": PINNED_HEAD,
        "pins": pin_report,
        "delta_class": delta_reference,
        "analyses": analyses,
        "verdict": ("CANONICAL-UP-TO-SCALE"
                    if primary[0]["corner_class_canonical_up_to_scale"]
                    else "FREE"),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    print("verdict:", ledger["verdict"])
    print("ledger_sha256=" + digest)
    Path(__file__).with_name("ledger_d2_corner_canonicity.json").write_text(
        json.dumps(ledger, sort_keys=True, indent=1) + "\n")


if __name__ == "__main__":
    main()
