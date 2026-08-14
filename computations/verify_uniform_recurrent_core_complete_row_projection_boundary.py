#!/usr/bin/env python3
"""Complete-row projection criterion and smallest recurrent-core guard.

After localizing the nonzero tail monomials, write a finite common-core row
component as

    F_v = C + sum_e A[e,v] Z_e.

A source-valid row combination projects C exactly when there is a companion
syzygy lambda in ker(A) whose coordinate sum is nonzero.  For a connected
pair-complete flat component, ker(A) is the transported alternating charge,
so the criterion is simply sum(lambda) != 0.

The criterion is sharp.  The smallest simple face-complete guard is the
unweighted K2,2.  Its transported charge is (1,1,-1,-1), hence centered.
The four complete rows vanish at C=1 and every companion Z_e=-1/2.  Thus C
is not in their span (or in the tail-saturated row ideal), the ideal is not
the unit ideal, every companion occurs twice, and the signed holonomy is
even.  Fixed-bistar placement alone therefore cannot prove projection.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_primitive_c4_recursive_boundary_counterguard.py":
        "65d453c7bcddca3c31b3124ce9ecd606a4ce10382302c3b062f08949c91f6cf9",
    "notes/uniform-primitive-c4-recursive-boundary-counterguard.md":
        "40b530f742361d7da0d6c27680c8b7f6fe475e9cd4900926c512a273504cb197",
    "computations/verify_uniform_boundary_complete_flat_even_component_theorem.py":
        "08db6dd78869d5d236d43fe8ae91e1e944d2b60d16a7f5f7a684f766a4187530",
    "notes/uniform-boundary-complete-flat-even-component-theorem.md":
        "b223d7d65852fcd086bff58673c6a3fb6811003b74bf742dc34ba96c0049fc31",
}
EXPECTED_LEDGER_SHA256 = (
    "2a5e470e6d101a3e845f81c259f504e023b1f149a65dadd58c28c17a4e096325"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def rref(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    if not matrix:
        return matrix, ()
    width = len(matrix[0])
    require(all(len(row) == width for row in matrix), "ragged matrix")
    pivot_row = 0
    pivots = []
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value
                             for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def transpose(matrix):
    if not matrix:
        return []
    return [list(column) for column in zip(*matrix, strict=True)]


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    width = len(matrix[0]) if matrix else 0
    free = [column for column in range(width) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(tuple(vector))
    return tuple(basis)


def matvec(matrix, vector):
    return tuple(sum((Q(left) * Q(right) for left, right in
                      zip(row, vector, strict=True)), Q(0))
                 for row in matrix)


def same_line(left, right):
    require(len(left) == len(right), "line width")
    pivot = next((index for index, value in enumerate(right) if value), None)
    if pivot is None or not left[pivot]:
        return False
    scalar = Q(left[pivot]) / Q(right[pivot])
    return all(Q(a) == scalar * Q(b)
               for a, b in zip(left, right, strict=True))


def in_column_span(matrix, target):
    # matrix is given by rows.
    require(len(matrix) == len(target), "target height")
    return rank([row + [target[index]]
                 for index, row in enumerate(matrix)]) == rank(matrix)


def connected(vertices, edges):
    reached = {vertices[0]}
    while True:
        old = len(reached)
        for left, right in edges:
            if left in reached:
                reached.add(right)
            if right in reached:
                reached.add(left)
        if len(reached) == old:
            return len(reached) == len(vertices)


def bipartition(vertices, edges):
    adjacency = {vertex: [] for vertex in vertices}
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    colours = {vertices[0]: 0}
    frontier = [vertices[0]]
    while frontier:
        vertex = frontier.pop()
        for neighbour in adjacency[vertex]:
            expected = 1 - colours[vertex]
            if neighbour in colours:
                if colours[neighbour] != expected:
                    return None
            else:
                colours[neighbour] = expected
                frontier.append(neighbour)
    return tuple(tuple(vertex for vertex in vertices
                       if colours[vertex] == side) for side in (0, 1))


def unsigned_incidence(vertices, edges):
    return [[Q(int(vertex in edge)) for vertex in vertices]
            for edge in edges]


def complete_rows(incidence):
    # Columns are complete rows F_v in basis (C,Z_e).  Return a row matrix.
    vertices = len(incidence[0]) if incidence else 0
    return [[Q(1)] * vertices] + [list(row) for row in incidence]


def audit_uniform_incidence_theorem():
    counts = {}
    smallest_face_complete = []
    for order in range(2, 7):
        vertices = tuple(range(order))
        all_edges = tuple(itertools.combinations(vertices, 2))
        categories = Counter()
        for mask in range(1, 1 << len(all_edges)):
            edges = tuple(all_edges[index] for index in range(len(all_edges))
                          if mask & (1 << index))
            if not connected(vertices, edges):
                continue
            shores = bipartition(vertices, edges)
            incidence = unsigned_incidence(vertices, edges)
            incidence_rank = rank(incidence)
            if shores is None:
                categories["nonbipartite"] += 1
                require(incidence_rank == order,
                        "a connected nonbipartite incidence lost full rank")
                continue

            categories["bipartite"] += 1
            require(incidence_rank == order - 1,
                    "a connected bipartite incidence lost corank one")
            charge = tuple(Q(1 if vertex in shores[0] else -1)
                           for vertex in vertices)
            kernel = nullspace(incidence)
            require(len(kernel) == 1
                    and matvec(incidence, charge) == (Q(0),) * len(edges),
                    "the alternating incidence charge changed")
            total = sum(charge, Q(0))
            balanced = len(shores[0]) == len(shores[1])
            categories["balanced" if balanced else "unbalanced"] += 1

            rows = complete_rows(incidence)
            core = [Q(1)] + [Q(0)] * len(edges)
            projects = in_column_span(rows, core)
            require(projects == bool(total),
                    "the complete-row projection criterion changed")
            # F_v(C=1,Z=z)=0 is solvable exactly in the centered branch.
            evaluation_exists = in_column_span(
                transpose(incidence), [Q(-1)] * order)
            require(evaluation_exists == (not bool(total)),
                    "the centered affine counter-evaluation criterion changed")

            degrees = Counter(site for edge in edges for site in edge)
            if min(degrees.values()) >= 2:
                categories["bipartite_min_degree_two"] += 1
                if balanced:
                    categories["balanced_min_degree_two"] += 1
                    smallest_face_complete.append((order, edges))
        counts[order] = dict(categories)

    expected = {
        2: {"bipartite": 1, "balanced": 1},
        3: {"bipartite": 3, "unbalanced": 3, "nonbipartite": 1},
        4: {
            "bipartite": 19, "balanced": 15, "unbalanced": 4,
            "nonbipartite": 19, "bipartite_min_degree_two": 3,
            "balanced_min_degree_two": 3,
        },
        5: {
            "bipartite": 195, "unbalanced": 195,
            "nonbipartite": 533, "bipartite_min_degree_two": 10,
        },
        6: {
            "bipartite": 3031, "balanced": 2050, "unbalanced": 981,
            "nonbipartite": 23673, "bipartite_min_degree_two": 355,
            "balanced_min_degree_two": 340,
        },
    }
    require(counts == expected,
            f"the connected graph projection census changed: {counts}")
    minimum_order = min(order for order, _edges in smallest_face_complete)
    minimum = [edges for order, edges in smallest_face_complete
               if order == minimum_order]
    require(minimum_order == 4 and len(minimum) == 3
            and all(len(edges) == 4 for edges in minimum),
            "the smallest simple face-complete guard changed")
    return {
        "labelled_connected_graph_census_through_six_vertices": counts,
        "uniform_projection_criterion": (
            "for connected pair-complete flat rows, let lambda span the "
            "transported companion-incidence kernel; C projects iff "
            "sum_v lambda_v is nonzero"
        ),
        "unweighted_bipartite_specialization": (
            "C projects iff the two shores have unequal cardinality"
        ),
        "smallest_simple_min_degree_two_centered_order": minimum_order,
        "labelled_minimizers": len(minimum),
        "one_isomorphism_type": "C4=K2,2",
    }


def audit_weighted_flat_criterion():
    # Shores U={0,1}, W={2,3}; edge order 02,03,12,13.
    edges = ((0, 2), (0, 3), (1, 2), (1, 3))
    unweighted = unsigned_incidence(tuple(range(4)), edges)
    centered = (Q(1), Q(1), Q(-1), Q(-1))
    centered_kernel = nullspace(unweighted)
    require(len(centered_kernel) == 1
            and same_line(centered_kernel[0], centered)
            and sum(centered, Q(0)) == 0,
            "the centered weighted charge changed")

    # The same topology can project when its flat transport is uncentered.
    # Desired charge (1,2,-1,-1); rows are edge coefficients at vertices.
    weighted = (
        (Q(1), Q(0), Q(1), Q(0)),
        (Q(1), Q(0), Q(0), Q(1)),
        (Q(0), Q(1), Q(2), Q(0)),
        (Q(0), Q(1), Q(0), Q(2)),
    )
    charge = (Q(1), Q(2), Q(-1), Q(-1))
    weighted_kernel = nullspace(weighted)
    require(len(weighted_kernel) == 1
            and same_line(weighted_kernel[0], charge)
            and sum(charge, Q(0)) == 1,
            "the uncentered flat transport changed")
    rows = complete_rows(weighted)
    core = [Q(1)] + [Q(0)] * 4
    require(in_column_span(rows, core),
            "the uncentered weighted C4 stopped projecting")
    projected = matvec(rows, charge)
    require(projected == tuple(core),
            f"the explicit weighted projector changed: {projected}")
    return {
        "same_physical_topology": "K2,2",
        "centered_charge": [str(value) for value in centered],
        "centered_total": "0",
        "uncentered_charge": [str(value) for value in charge],
        "uncentered_total": "1",
        "exact_projector": "F0+2F1-F2-F3=C",
        "consequence": (
            "topology and flatness do not decide projection; the transported "
            "charge must be tested against the common-core coefficient row"
        ),
    }


def audit_smallest_complete_row_guard():
    # Vertex order A0,A1,B0,B1 and companion order z00,z01,z10,z11.
    incidence = (
        (Q(1), Q(0), Q(1), Q(0)),  # z00 at A0,B0
        (Q(1), Q(0), Q(0), Q(1)),  # z01 at A0,B1
        (Q(0), Q(1), Q(1), Q(0)),  # z10 at A1,B0
        (Q(0), Q(1), Q(0), Q(1)),  # z11 at A1,B1
    )
    rows = complete_rows(incidence)
    core = [Q(1), Q(0), Q(0), Q(0), Q(0)]
    charge = (Q(1), Q(1), Q(-1), Q(-1))
    guard_kernel = nullspace(incidence)
    require(rank(incidence) == 3 and len(guard_kernel) == 1
            and same_line(guard_kernel[0], charge),
            "the K2,2 companion incidence changed")
    require(rank(rows) == 3
            and not in_column_span(rows, core)
            and rank([row + [core[index]]
                      for index, row in enumerate(rows)]) == 4,
            "the K2,2 common core became projectable")
    require(matvec(rows, charge) == (Q(0),) * 5,
            "the centered complete-row relation changed")

    # Explicit rational point of the saturated complete-row ideal.
    evaluation = (Q(1), Q(-1, 2), Q(-1, 2), Q(-1, 2), Q(-1, 2))
    row_values = tuple(sum((row[index] * evaluation[index]
                            for index in range(5)), Q(0))
                       for row in transpose(rows))
    require(row_values == (Q(0),) * 4 and evaluation[0] == 1,
            "the exact nonprojection point changed")

    # Every tail-saturated S-pair is a difference F_v-F_w.  Their span has
    # rank two; the common affine companion class survives it.
    columns = transpose(rows)
    spairs = [[left - right for left, right in
               zip(columns[index], columns[0], strict=True)]
              for index in range(1, 4)]
    require(rank(spairs) == 2,
            "the K2,2 S-pair quotient changed")
    detector = evaluation
    require(all(sum((detector[index] * column[index]
                     for index in range(5)), Q(0)) == 0
                for column in columns)
            and detector[0] == 1,
            "the normalized dual nonprojection detector changed")

    companion_degrees = tuple(sum(row) for row in incidence)
    vertex_degrees = tuple(sum(incidence[edge][vertex]
                               for edge in range(4))
                           for vertex in range(4))
    require(companion_degrees == (2, 2, 2, 2)
            and vertex_degrees == (2, 2, 2, 2),
            "the guard acquired a singleton or incomplete boundary")
    return {
        "complete_rows": [
            "F_A0=C+z00+z01",
            "F_A1=C+z10+z11",
            "F_B0=C+z00+z10",
            "F_B1=C+z01+z11",
        ],
        "tail_saturation": (
            "for unsaturated rows tau_v*F_v, colon by the product of all "
            "tau_v gives these four normalized rows; C still does not lie "
            "in their span"
        ),
        "centered_relation": "F_A0+F_A1-F_B0-F_B1=0",
        "companion_incidence_rank": rank(incidence),
        "complete_row_rank": rank(rows),
        "rank_after_adjoining_C": 4,
        "S_pair_difference_rank": rank(spairs),
        "exact_zero_point": {
            "C": "1",
            "z00=z01=z10=z11": "-1/2",
            "all_complete_rows": "0",
        },
        "dual_detector": [str(value) for value in detector],
        "each_companion_occurs_in_rows": [int(value)
                                             for value in companion_degrees],
        "companions_per_row": [int(value) for value in vertex_degrees],
        "odd_holonomy": False,
        "unit_ideal": False,
        "common_core_projects": False,
        "physical_typing": (
            "all four companion coordinates may be declared internal to the "
            "same fixed bistar; the abstract complete-row algebra supplies "
            "no outside-fan or anchor-deletion label"
        ),
    }


def audit_projection_ideal_statement():
    # General finite-dimensional model.  A maps row coefficients to the
    # companion quotient, while t reads the common-core coefficient.
    examples = (
        {
            "name": "two-row parallel companion minimum",
            "A": ((Q(1), Q(1)),),
            "t": (Q(1), Q(1)),
            "kernel": ((Q(-1), Q(1)),),
            "projection_ideal": "0",
        },
        {
            "name": "three-row unbalanced path",
            "A": ((Q(1), Q(1), Q(0)),
                  (Q(0), Q(1), Q(1))),
            "t": (Q(1), Q(1), Q(1)),
            "kernel": ((Q(1), Q(-1), Q(1)),),
            "projection_ideal": "Q",
        },
    )
    records = []
    for example in examples:
        kernel = nullspace(example["A"])
        require(len(kernel) == len(example["kernel"])
                and all(same_line(left, right) for left, right in
                        zip(kernel, example["kernel"], strict=True)),
                f"the projection kernel changed: {example['name']}")
        values = tuple(sum((example["t"][index] * vector[index]
                            for index in range(len(example["t"]))), Q(0))
                       for vector in kernel)
        ideal = "Q" if any(values) else "0"
        require(ideal == example["projection_ideal"],
                f"the projection ideal changed: {example['name']}")
        records.append({
            "name": example["name"],
            "kernel_dimension": len(kernel),
            "tail_values_on_kernel": [str(value) for value in values],
            "projection_ideal_over_Q": ideal,
        })
    return {
        "general_ring_formula": (
            "P=t(ker A); the common core projects source-validly exactly "
            "when 1 belongs to the projection ideal P"
        ),
        "localized_field_formula": (
            "after tail localization, projection is equivalent to one "
            "companion syzygy having nonzero total core coefficient"
        ),
        "examples": records,
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "projection_ideal": audit_projection_ideal_statement(),
        "uniform_pair_complete_theorem": audit_uniform_incidence_theorem(),
        "weighted_flat_boundary": audit_weighted_flat_criterion(),
        "smallest_face_complete_counterguard":
            audit_smallest_complete_row_guard(),
        "verdict": (
            "the unconditional complete-row recurrent-core projection "
            "theorem is false, even after tail saturation and with a "
            "fixed path-independent bistar, paired companion completion, "
            "no singleton, and even flat holonomy"
        ),
        "proved_restricted_theorem": (
            "for a finite connected pair-complete flat companion component, "
            "transport its unique alternating charge lambda.  If its total "
            "common-core coefficient is nonzero, the lambda-weighted sum "
            "of the complete source rows projects the core exactly"
        ),
        "sharp_missing_hypothesis": (
            "exclude centered balanced companion components, or prove from "
            "physical source labels that their first centered component "
            "has an off-anchor active fan, a private/deletable coordinate, "
            "odd multiplicative holonomy, or a higher boundary which makes "
            "the transported charge noncentered"
        ),
        "scope": (
            "uniform linear complete-row/S-pair theorem and exact rational "
            "counterguard; the K2,2 module is not claimed to be a full "
            "ternary decorated hafnian source"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"complete-row projection ledger changed: {digest}")
    print("recurrent-core complete-row projection: SHARP BOUNDARY")
    print("projection ideal: t(ker companion map)")
    print("pair-complete flat component: project iff transported charge is uncentered")
    print("smallest face-complete guard: centered K2,2, C=1, z_e=-1/2")
    print("guard is tail-saturated, singleton-free, and even-holonomy")
    print("needed: physical exclusion or landing of centered balanced components")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
