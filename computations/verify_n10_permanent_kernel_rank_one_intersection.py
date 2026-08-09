#!/usr/bin/env python3
"""Exact rank-one/permanent intersection with the N=10 nine-dimensional kernel.

The all-cut kernel from verify_n10_permanent_grade_four_cut_kernel.py has one
four-grade generator for each ordered pair of new-end colours (beta, delta).
For fixed beta, delta, cross weights give endpoint-colour vectors

    u_i = (X_{i,beta}, Y_{i,delta})

and the visible permanent is B(u_i,u_j), where
B((x,y),(x',y')) = x*y' + x'*y.

If a kernel coefficient k_beta,delta were nonzero, three of its required
nonzero entries and four required zero entries would force three nonzero
vectors onto the same B-orthogonal line.  One required entry makes that line
non-isotropic; another required zero makes it isotropic.  This contradiction
is independent of the coefficient values.  Hence the permanent image meets
the exact nine-dimensional all-cut kernel only at the origin.

This closes exact invisible quadratic-grade cancellation on the anchored
forced-pair model.  It does not prove that ordinary four-cylinder membership
separates grades modulo lower-degree or column-span cancellations.
"""

from __future__ import annotations

import importlib.util
from collections import Counter
from fractions import Fraction
from pathlib import Path


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_permanent_kernel():
    path = Path(__file__).with_name(
        "verify_n10_permanent_grade_four_cut_kernel.py"
    )
    spec = importlib.util.spec_from_file_location("permanent_kernel", path)
    require(spec is not None and spec.loader is not None, "cannot load permanent kernel")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def circuit(beta, delta):
    return (
        (((2, 8, 2, beta), (7, 9, 2, delta)), Q(1)),
        (((3, 8, 1, beta), (6, 9, 1, delta)), Q(-1)),
        (((5, 8, 1, beta), (7, 9, 1, delta)), Q(1)),
        (((5, 8, 2, beta), (6, 9, 2, delta)), Q(-1)),
    )


def endpoint_node(coordinate):
    return coordinate[0], coordinate[2]


def permanent_node_pair(pair):
    return endpoint_node(pair[0]), endpoint_node(pair[1])


def canonical_node_pair(left, right):
    return tuple(sorted((left, right)))


def audit_projective_orthogonality_no_go(circuit_records):
    """Return the finite incidence certificate for one nonzero channel.

    Write A=(a,b), B=(c,d), C=(e,f), D=(g,h).  The circuit has nonzero
    coordinates A,B,C,D and zero coordinates at every other visible pair.
    Since old(a)=2, old(c)=3, old(d)=6, old(e)=5, the zero pairs ac, ad,
    ae, ce are all valid permanent coordinates.

    B(a,c)=B(a,d)=B(a,e)=0 puts c,d,e on the one-dimensional orthogonal
    complement of nonzero a.  B(c,d) != 0 says that line is non-isotropic;
    B(c,e)=0 says the same line is isotropic, a contradiction.
    """
    pairs = [permanent_node_pair(pair) for pair, _coefficient in circuit_records]
    (a, b), (c, d), (e, f), (g, h) = pairs
    require(
        len({a, b, c, d, e, f, g, h}) == 8,
        "circuit endpoint-colour nodes are not distinct",
    )
    nonzero_pairs = {canonical_node_pair(*pair) for pair in pairs}
    zero_witnesses = (
        canonical_node_pair(a, c),
        canonical_node_pair(a, d),
        canonical_node_pair(a, e),
        canonical_node_pair(c, e),
    )
    for left, right in zero_witnesses:
        require(left[0] != right[0], "orthogonality witness repeats an old vertex")
        require(
            (left, right) not in nonzero_pairs,
            "orthogonality witness is a supported kernel coordinate",
        )
    require(
        canonical_node_pair(c, d) in nonzero_pairs,
        "non-isotropic-line witness is absent",
    )
    require(
        canonical_node_pair(e, f) in nonzero_pairs,
        "the third circuit edge does not force e nonzero",
    )
    return {
        "orthogonal_to_a": (c, d, e),
        "nonisotropic_pair": canonical_node_pair(c, d),
        "contradictory_zero": canonical_node_pair(c, e),
    }


def main() -> None:
    permanent_kernel = load_permanent_kernel()
    provenance = permanent_kernel.load_provenance_cancellation()
    graded_guard = provenance.load_graded_guard()
    multitrace = graded_guard.load_multitrace()
    frontier = multitrace.load_frontier()
    one_cross = frontier.load_one_cross_edge()
    forced_pair = one_cross.load_forced_pair_contraction()
    certificate = forced_pair.load_positive_moduli_certificate()
    two_cell = certificate.load_two_cell_audit()
    one_cell = two_cell.load_one_cell_elimination()
    unit_gate = one_cell.load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)
    lifted_base = forced_pair.lift_cells(module, base)

    support = tuple(
        (left, right, colour_l, colour_r)
        for (left, right), entries in lifted_base.items()
        for colour_l, colour_r, weight in entries
        if weight
    )
    target_characters = tuple(
        {3 * vertex + colour: Q(1) for vertex in provenance.B10}
        for colour in range(3)
    )
    constraint_basis = module.rational_basis(
        [provenance.coordinate_character(coordinate) for coordinate in support]
        + list(target_characters)
    )
    representatives = permanent_kernel.permanent_representatives(
        provenance, frontier
    )
    groups = permanent_kernel.character_groups(
        provenance, two_cell, constraint_basis, representatives
    )
    grades = permanent_kernel.full_grades(
        provenance, module, base, representatives
    )

    dependent_groups = []
    for character, records in groups.items():
        if len(module.rational_basis([grades[pair] for pair in records])) < len(records):
            dependent_groups.append((character, records))
    dependent_pairs = {
        pair for _character, records in dependent_groups for pair in records
    }
    cofactors = permanent_kernel.cofactor_grades(
        provenance,
        frontier,
        forced_pair,
        one_cell,
        module,
        lifted_base,
        dependent_pairs,
    )

    def signature(pair):
        return permanent_kernel.combined_signature(
            grades[pair],
            {z: cofactors[(pair, z)] for z in module.S},
            tuple(module.S),
        )

    kernel_dimension = 0
    combined_patterns = Counter()
    for _character, records in dependent_groups:
        rank = len(module.rational_basis([signature(pair) for pair in records]))
        kernel_dimension += len(records) - rank
        combined_patterns[(len(records), rank)] += 1
    require(
        kernel_dimension == 9
        and combined_patterns == Counter({(22, 21): 6, (66, 63): 1}),
        "all-cut permanent kernel changed",
    )

    circuits = tuple(circuit(beta, delta) for beta in range(3) for delta in range(3))
    circuit_pairs = {pair for records in circuits for pair, _coefficient in records}
    require(len(circuit_pairs) == 36, "the nine circuits do not have disjoint support")
    incidence_certificates = {}
    for beta in range(3):
        for delta in range(3):
            records = circuit(beta, delta)
            require(
                all(pair in dependent_pairs for pair, _coefficient in records),
                f"circuit left the exact kernel domain at {(beta, delta)}",
            )
            require(
                not one_cell.sparse_linear_combination(
                    *((coefficient, signature(pair)) for pair, coefficient in records)
                ),
                f"channel circuit failed at {(beta, delta)}",
            )
            incidence_certificates[(beta, delta)] = audit_projective_orthogonality_no_go(
                records
            )

    # Nine independent kernel vectors in a nine-dimensional kernel form a
    # basis.  Because their supports are disjoint by (beta,delta), every
    # nonzero kernel point has a nonzero coefficient in at least one channel,
    # where the projective orthogonality certificate applies.
    require(
        len(circuits) == kernel_dimension,
        "channel circuits do not account for the full kernel dimension",
    )

    # The smallest circuit itself is therefore unrealizable, and the same
    # argument eliminates every denser linear combination of the nine
    # channel circuits.  Anchor conditions can only shrink the parameter
    # space, so the no-go holds before and after imposing them.

    # A nonzero cross source can still map to the *zero* permanent point.
    # Re-audit the smallest permanent-zero four-cell block from the previous
    # note to record that the preimage of the origin is nontrivial.
    zero_block = (
        (provenance.PAIR_A[0], Q(1)),
        (provenance.PAIR_A[1], Q(1)),
        (provenance.PAIR_B[0], Q(1)),
        (provenance.PAIR_B[1], Q(-1)),
    )
    zero_cells = provenance.add_weighted_coordinates(
        module, lifted_base, zero_block
    )
    require(
        module.matching_tensor(provenance.B10, zero_cells)
        == module.matching_tensor(provenance.B10, lifted_base),
        "permanent-zero survivor changed the forced-lift tensor",
    )

    # Forced-pair stability: the nine circuit identities persist at N=12,
    # and the incidence contradiction only uses their unchanged old endpoint
    # nodes.  Verify the full identities exactly after the lift.
    for beta in range(3):
        for delta in range(3):
            terms = []
            for pair, coefficient in circuit(beta, delta):
                shifted = (
                    (pair[0][0], 10, pair[0][2], pair[0][3]),
                    (pair[1][0], 11, pair[1][2], pair[1][3]),
                )
                terms.append(
                    (
                        coefficient,
                        provenance.ordered_pair_grade(
                            module,
                            lifted_base,
                            shifted,
                            provenance.B10,
                            (10, 11),
                        ),
                    )
                )
            require(
                not one_cell.sparse_linear_combination(*terms),
                f"N=12 channel circuit failed at {(beta, delta)}",
            )

    print("N=10 permanent-image/all-cut-kernel intersection: exact PASS")
    print(f"all-cut kernel dimension: {kernel_dimension}")
    print("kernel basis: one four-grade circuit for each of 9 new-colour pairs")
    print("rank-one/permanent intersection with kernel: origin only")
    print("minimal four-grade circuit: not realizable in isolation")
    print("anchor/forced-lift constraints: no new nonzero intersection")
    print("origin preimage: nontrivial permanent-zero four-cell blocks survive")
    print("forced-pair full-grade stability: exact at N=12")
    print("verdict: nonlinear invisible quadratic-grade cancellation eliminated")
    print("scope: lower-degree and cylinder-span cancellations remain open")


if __name__ == "__main__":
    main()
