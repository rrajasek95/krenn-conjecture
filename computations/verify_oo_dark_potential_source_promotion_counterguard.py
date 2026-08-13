#!/usr/bin/env python3
"""Exact source-promotion boundary for a dark Cartan potential.

Let M be a minimal zero-holonomy critical block, let ell span its left
kernel, and suppose a typed Cartan connector g is dark: ell^T g=0.  Then
g=M y.  This equality is only in the critical-component projection.

For complete lifted columns C and connector G define

                         R = G-C y.

The component projection of R is zero.  If that projection is saturated by
all current component labels, nonzero R is a literal typed exit.  If R=0
and the kernel vector (-y,1) is realized by occupied scalar cells in one
p_i or s_j row, the complete same-row theorem of 0a965e7 deletes support
anchor-safely.

Neither conclusion follows from M y=g alone.  A parallel two-class critical
block admits an exact dark potential with R=0 whose involved occupied cells
have different row heads and are mutual anchors.  It has no same-row kernel
and no external residual.  A second guard shows why an unsaturated
projection can misclassify a forgotten internal coordinate as an exit.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_oo_zero_holonomy_schur_interference_reduction.py":
        "1e96bf98e997e55d2b050de6c56e7f597cd507737aefa6386296c44adab03631",
    "computations/verify_matching_interference_head_invariance_cartan_gate.py":
        "17b84de9c22247d617b9919fb5cf18593300226619945c7e6b5f5cef029ab787",
    "computations/verify_h3_post_ks_same_head_rank_support_counterguard.py":
        "21ebd9d48fed3bc91af820bc84b37bd5133971e519d60fb1d0727de4a4acec3e",
    "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py":
        "6f27d3585fdc4708026ab6fef6134295dd874f83bb43fd1f480b7314362c56f3",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
}
EXPECTED_LEDGER_SHA256 = "19a2e8b6979c3197cbf1419e54f0b0430817b1e7f02d438b5e82f1979223b0c3"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def columns(matrix):
    return tuple(tuple(Q(matrix[row][column]) for row in range(len(matrix)))
                 for column in range(len(matrix[0])))


def linear_combination(source_columns, coefficients):
    require(len(source_columns) == len(coefficients), "coefficient width changed")
    return add(*(scale(value, column) for value, column in
                 zip(coefficients, source_columns, strict=True)))


def rank(source_columns):
    if not source_columns:
        return 0
    height = len(source_columns[0])
    require(all(len(column) == height for column in source_columns),
            "ragged columns")
    work = [[Q(source_columns[column][row])
             for column in range(len(source_columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(source_columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def mutual_anchors(edges):
    degrees = {}
    for left, right in edges:
        degrees[left] = degrees.get(left, 0) + 1
        degrees[right] = degrees.get(right, 0) + 1
    return frozenset(edge for edge in edges
                     if degrees[edge[0]] == degrees[edge[1]] == 1)


def complete_lift_residual(matrix, potential, internal_lifts, connector_lift):
    """Return g and R=G-Cy, checking the projected potential equation."""
    size = len(matrix)
    require(len(potential) == len(internal_lifts) == size,
            "critical lift width changed")
    require(all(len(column) == len(connector_lift)
                for column in internal_lifts), "complete lift height changed")
    g = matvec(matrix, potential)
    require(tuple(column[:size] for column in internal_lifts)
            == columns(matrix), "internal lifts changed their M projection")
    require(tuple(connector_lift[:size]) == g,
            "connector lift changed its g projection")
    residual = add(connector_lift,
                   scale(-1, linear_combination(internal_lifts, potential)))
    require(residual[:size] == (Q(0),) * size,
            "the lifted potential left a critical-component boundary")
    return g, residual


def audit_dark_potential_interface(schur, source_descent, same_row):
    matrix, _right, left = schur.compatible_cycle(4)
    potential = (Q(1), Q(-2), Q(3), Q(1, 2))
    g = matvec(matrix, potential)
    require(dot(left, g) == 0 and schur.solve_image(matrix, g) is not None,
            "the dark Cartan potential stopped being component-exact")

    cartan = source_descent.audit()
    require(cartan["physical_packet"]["protected_D_W_target_anchor_Eq"] == 0
            and cartan["target_defect"]["endpoint_odd_target"] == 0,
            "the physical Cartan protected readouts changed")
    support = same_row.audit_complete_same_row_span_descent(
        load(
            "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py",
            "dark_potential_proportional",
        )
    )
    require(support["minimum_support_consequence"].endswith(
                "linearly independent")
            and support["anchor_safe_graph_audits"] > 0,
            "the complete same-row kernel theorem changed")

    size = len(matrix)
    critical_columns = columns(matrix)

    # Exact same-row branch: the complete lifts have no outside coordinates.
    internal_exact = tuple(column + (Q(0), Q(0))
                           for column in critical_columns)
    connector_exact = g + (Q(0), Q(0))
    _, exact_residual = complete_lift_residual(
        matrix, potential, internal_exact, connector_exact)
    kernel = tuple(-value for value in potential) + (Q(1),)
    require(not any(exact_residual)
            and not any(linear_combination(
                internal_exact + (connector_exact,), kernel)),
            "the exact complete potential stopped being a kernel vector")

    # Exit branch: a literal outside coordinate survives in the connector.
    connector_exit = g + (Q(1), Q(0))
    _, exit_residual = complete_lift_residual(
        matrix, potential, internal_exact, connector_exit)
    require(exit_residual == (Q(0),) * size + (Q(1), Q(0)),
            "the typed exit residual changed")
    return {
        "critical_size": size,
        "critical_rank": schur.rank(matrix),
        "left_pairing": str(dot(left, g)),
        "component_potential": [str(value) for value in potential],
        "complete_promotion_identity": "R=G-Cy and pi_component(R)=0",
        "exact_same_row_model": {
            "residual": [str(value) for value in exact_residual],
            "complete_kernel": [str(value) for value in kernel],
            "consequence_under_occupied_same_row_typing":
                "anchor-safe support deletion by 0a965e7",
        },
        "saturated_exit_model": {
            "residual": [str(value) for value in exit_residual],
            "literal_outside_coordinate": "exchange:E0",
            "consequence_under_component_saturation":
                "typed exchange leaving/enlarging the component",
        },
        "physical_Cartan_packet": {
            "source_provenant_in_canonical_grade": True,
            "protected_D_W_target_anchor_Eq": 0,
            "uniform_componentwise_complete_lift": False,
        },
    }


def audit_smallest_type_split_counterguard():
    # Parallel signless two-cycle.  Both right and left charges have full
    # support, rank is one, and g is a non-coordinate dark aggregate.
    matrix = ((Q(1), Q(-1)), (Q(1), Q(-1)))
    right = (Q(1), Q(1))
    left = (Q(1), Q(-1))
    potential = (Q(1), Q(0))
    g = matvec(matrix, potential)
    require(rank(columns(matrix)) == 1
            and matvec(matrix, right) == (Q(0), Q(0))
            and matvec(tuple(zip(*matrix, strict=True)), left)
                == (Q(0), Q(0))
            and dot(left, g) == 0,
            "the two-class dark critical block changed")

    internal = columns(matrix)
    connector = g
    _, residual = complete_lift_residual(matrix, potential, internal, connector)
    all_columns = internal + (connector,)
    type_labels = ("p0", "s0", "Cartan-chain")
    require(not any(residual) and rank(all_columns) == 1,
            "the type-split potential stopped being complete-exact")

    # No row type contains two columns, hence no same-row kernel exists.
    type_groups = {
        label: tuple(index for index, value in enumerate(type_labels)
                     if value == label)
        for label in type_labels
    }
    require(all(len(indices) == 1 for indices in type_groups.values()),
            "the type-split guard acquired a same-row pair")

    # If the two scalar cells are disjoint they are both mutual anchors.
    # The Cartan-chain column is not an occupied scalar cell at all.
    scalar_edges = (("P0", "T0"), ("S0", "T1"))
    anchors = mutual_anchors(scalar_edges)
    require(anchors == frozenset(scalar_edges),
            "the type-split scalar cells stopped being mutual anchors")
    return {
        "size": 2,
        "matrix": [[str(value) for value in row] for row in matrix],
        "rank": rank(columns(matrix)),
        "right_charge": [str(value) for value in right],
        "left_charge": [str(value) for value in left],
        "connector_g": [str(value) for value in g],
        "left_pairing": str(dot(left, g)),
        "potential_y": [str(value) for value in potential],
        "complete_residual": [str(value) for value in residual],
        "column_type_labels": list(type_labels),
        "same_row_kernel_available": False,
        "occupied_scalar_cells_are_mutual_anchors": True,
        "connector_is_occupied_scalar_cell": False,
        "literal_outside_contaminant": False,
        "verdict": (
            "My=g and even complete exactness do not imply the 0a965e7 "
            "deletion when the potential is type-split and the connector is "
            "a relative chain rather than an occupied same-row scalar cell"
        ),
    }


def audit_unsaturated_projection_counterguard():
    # The visible critical row forgets a second row labelled as part of the
    # same component.  A residual in that row is not an escaping exchange.
    matrix = ((Q(1), Q(-1)), (Q(1), Q(-1)))
    potential = (Q(1), Q(0))
    g = matvec(matrix, potential)
    internal = tuple(column + (Q(0),) for column in columns(matrix))
    connector = g + (Q(1),)
    _, residual = complete_lift_residual(matrix, potential, internal, connector)
    require(residual == (Q(0), Q(0), Q(1)),
            "the forgotten internal residual changed")
    return {
        "residual": [str(value) for value in residual],
        "extra_coordinate_label": "current_component:forgotten_fine_row",
        "projection_component_saturated": False,
        "typed_exit_valid": False,
        "verdict": (
            "pi(R)=0 does not mean R leaves the component unless pi retains "
            "every current component fine label"
        ),
    }


def main():
    pin_dependencies()
    schur = load(
        "computations/verify_oo_zero_holonomy_schur_interference_reduction.py",
        "dark_potential_schur",
    )
    source_descent = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "dark_potential_source_descent",
    )
    same_row = load(
        "computations/verify_h3_post_ks_same_head_rank_support_counterguard.py",
        "dark_potential_same_row",
    )

    ledger = {
        "pins": PINS,
        "dark_potential_complete_lift_interface":
            audit_dark_potential_interface(schur, source_descent, same_row),
        "smallest_type_split_counterguard":
            audit_smallest_type_split_counterguard(),
        "unsaturated_component_projection_counterguard":
            audit_unsaturated_projection_counterguard(),
        "conditional_dark_potential_theorem": (
            "let C,G be complete source lifts with component projections M,g "
            "and My=g.  Then R=G-Cy has zero component projection.  If the "
            "projection is fine-label saturated, R!=0 is a literal typed "
            "exchange outside the component.  If R=0 and (-y,1) is realized "
            "by occupied scalar cells in one p_i or s_j row with connector "
            "coefficient nonzero, 0a965e7 gives an anchor-safe support deletion"
        ),
        "necessary_source_typing": [
            "complete lifted columns retain every source equation/readout",
            "the component projection retains every current fine label",
            "nonzero complementary coordinates are literal adjacency/exchange labels",
            "the zero-residual kernel is realized by already occupied scalar cells",
            "all kernel cells used for 0a965e7 lie in one fixed p_i or s_j row",
            "the connector is an occupied scalar cell, not only a relative chain generator",
        ],
        "remaining_uniform_theorem": (
            "prove that the componentwise physical Cartan lift satisfies the "
            "saturated complete-lift interface and that every zero-residual "
            "potential is same-row/anchor-safe, or supplies another explicitly "
            "well-founded physical kernel move"
        ),
        "scope": (
            "exact linear promotion theorem and two smallest typing guards.  "
            "The canonical h3 Cartan cell is source-provenant, but its uniform "
            "attachment to every critical block with these typing properties "
            "is not proved here"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"dark-potential source-promotion ledger changed: {digest}")
    print("OO dark potential source promotion: CONDITIONAL / COUNTERGUARD")
    print("R=G-Cy has zero critical-component projection")
    print("saturated R!=0 -> typed exit; occupied same-row R=0 -> support deletion")
    print("My=g alone: insufficient by the two-class type-split guard")
    print("uniform componentwise Cartan typing: OPEN")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
