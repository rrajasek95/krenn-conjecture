#!/usr/bin/env python3
"""Reduce the 1I+5R generic-kernel/R2 potential frontier.

Let X_0 be invertible and X_i=h_i b_i^T be nonzero rank one for i=1,...,5.
On the rank-one sites, the zero-sum graph E has edge ij when nu_i+nu_j=0.
Every E-edge must also satisfy b_i^T J b_j=0 and is the only kind of edge
whose base block can be arbitrary.

An isolated E-vertex is a fixed root and gives rank(dPsi)<=42.  With no
isolates, the scalar graph has exactly five signatures:

    K5, K1,4, K2,3, K3 disjoint union K2, K1,2 disjoint union K2.

The K5 pair-pencil is one common isotropic line, fixing all five blocks at
root 0 and again giving rank <=42.  The two disconnected signatures are a
constant-cross triangle shore (rank <=51) and a coordinate-shore path
(rank <=49).  Thus only connected K1,4 and K2,3 remain.  Their two
pair-pencil shores are distinct nonisotropic lines; otherwise root 0 is
fixed.  In physical selected coordinates their slopes are antipodal.
Consequently all rank-one selected columns are nonzero and literal R2 must
use two internal pure-column witnesses at every root.  At root 0 this
forces distinct h_i on the two physical coordinate axes.

Research evidence only.  Standard library exact arithmetic; checks remain
live under python -O and python -I -S.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SHORE = run_path(str(
    HERE / "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
))
FIXED_ROOT = run_path(str(
    HERE
    / "verify_level_two_two_invertible_asymmetric_one_active_cofactor_kernel_normal_form.py"
))

RANK_ONE = tuple(range(1, 6))
PAIRS = tuple(combinations(RANK_ONE, 2))
J = ((Q(0), Q(1)), (Q(1), Q(0)))


def pairing(left, right):
    return left[0] * right[1] + left[1] * right[0]


def outer(left, right):
    return tuple(
        tuple(left[row] * right[column] for column in range(2))
        for row in range(2)
    )


def matrix_multiply(left, right):
    return tuple(
        tuple(sum(left[row][middle] * right[middle][column]
                  for middle in range(2))
              for column in range(2))
        for row in range(2)
    )


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(2))
                 for column in range(2))


def graph_signature(values):
    edges = frozenset(
        (left, right) for left, right in PAIRS
        if values[left - 1] + values[right - 1] == 0
    )
    degrees = tuple(sorted(
        sum(vertex in edge for edge in edges) for vertex in RANK_ONE
    ))
    if not degrees or degrees[0] == 0:
        return "isolated", edges, degrees
    signatures = {
        (10, (4, 4, 4, 4, 4)): "K5",
        (4, (1, 1, 1, 1, 4)): "K14",
        (6, (2, 2, 2, 3, 3)): "K23",
        (4, (1, 1, 2, 2, 2)): "K3+K2",
        (3, (1, 1, 1, 1, 2)): "K12+K2",
    }
    signature = signatures.get((len(edges), degrees))
    require(signature is not None,
            ("unexpected no-isolate zero-sum graph", values, edges, degrees))
    return signature, edges, degrees


def audit_zero_sum_graph_classification():
    # Two nonzero signed magnitudes and zero realize every abstract scalar
    # zero/opposition component on five labelled vertices.
    counts = Counter()
    representatives = {}
    for values in product((-2, -1, 0, 1, 2), repeat=5):
        signature, edges, degrees = graph_signature(values)
        counts[signature] += 1
        representatives.setdefault(signature, (values, edges, degrees))
    expected = {
        "isolated", "K5", "K14", "K23", "K3+K2", "K12+K2",
    }
    require(set(counts) == expected,
            ("zero-sum graph signatures changed", counts))

    require(representatives["K5"][0] == (0, 0, 0, 0, 0),
            "the complete zero-sum graph stopped being all-zero")
    return counts, representatives


def audit_rank_one_pair_pencil():
    # X_i=h_i b_i^T gives
    # X_i J X_j^T=(b_i^T J b_j) h_i h_j^T.
    vectors = (
        (Q(1), Q(0)), (Q(0), Q(1)),
        (Q(1), Q(1)), (Q(1), Q(-1)), (Q(2), Q(3)),
    )
    checks = 0
    for h_i, b_i, h_j, b_j in product(vectors, repeat=4):
        x_i = outer(h_i, b_i)
        x_j = outer(h_j, b_j)
        actual = matrix_multiply(matrix_multiply(x_i, J), transpose(x_j))
        expected = tuple(
            tuple(pairing(b_i, b_j) * h_i[row] * h_j[column]
                  for column in range(2))
            for row in range(2)
        )
        require(actual == expected,
                ("rank-one pair-pencil identity changed", h_i, b_i, h_j, b_j))
        checks += 1
    require(checks == len(vectors) ** 4,
            "pair-pencil identity census changed")

    # At the invertible root, X_0 J b_i is nonzero for every b_i!=0, so
    # nu_0+nu_i can never vanish.
    x0 = ((Q(2), Q(3)), (Q(5), Q(7)))
    det_x0 = x0[0][0] * x0[1][1] - x0[0][1] * x0[1][0]
    require(det_x0 != 0, "invertible-root witness became singular")
    root_images = {}
    for b in vectors:
        image = tuple(
            sum(x0[row][middle] * J[middle][column] * b[column]
                for middle in range(2) for column in range(2))
            for row in range(2)
        )
        require(any(image), ("X0 J b vanished", b))
        root_images[b] = image
    return checks, root_images


def audit_fixed_root_bound():
    # The fixed-root theorem is support-only.  If a rank-one potential
    # vertex i is isolated, every nonzero-multiplier block ij is either zero
    # or h_i h_j^T, and M_i0 also has factor h_i.  If all five b_i share one
    # isotropic line, the five M_0i instead share X_0 J b at root 0.
    calibration = FIXED_ROOT["audit_product_slice_and_fixed_root_bound"]()
    require(calibration[4:] == (42, 42),
            ("fixed-root bound/calibration changed", calibration))
    cases = {
        "isolated rank-one potential": "fixed root at that rank-one site",
        "common isotropic pencil": "fixed root at site 0",
    }
    return cases, calibration[4], calibration[5]


def audit_complete_orthogonal_pencil():
    # In dimension two, three nonzero pairwise J-orthogonal vectors share
    # one isotropic line.  Audit this directly on a finite exact projective
    # grid, including both coordinate isotropic lines.
    vectors = tuple(
        (Q(x), Q(y))
        for x, y in product(range(-2, 3), repeat=2)
        if (x, y) != (0, 0)
    )

    def proportional(left, right):
        return left[0] * right[1] - left[1] * right[0] == 0

    triples = 0
    for first, second, third in product(vectors, repeat=3):
        if not (
            pairing(first, second) == 0
            and pairing(first, third) == 0
            and pairing(second, third) == 0
        ):
            continue
        require(pairing(first, first) == 0,
                ("complete orthogonal pencil was not isotropic",
                 first, second, third))
        require(proportional(first, second)
                and proportional(first, third),
                ("complete orthogonal pencil split lines",
                 first, second, third))
        triples += 1
    require(triples > 0, "no complete orthogonal pencil was audited")

    # Symbolically, if b=(x,y), its J-orthogonal line is (x,-y);
    # the self-pairing on that line is -2xy.
    formula_checks = []
    for x, y in product(range(-3, 4), repeat=2):
        if (x, y) == (0, 0):
            continue
        b = (Q(x), Q(y))
        orthogonal = (Q(x), Q(-y))
        require(pairing(b, orthogonal) == 0,
                ("displayed orthogonal vector changed", b, orthogonal))
        formula_checks.append(
            pairing(orthogonal, orthogonal) == -2 * Q(x) * Q(y)
        )
    require(all(formula_checks), "orthogonal-line self-pairing changed")
    return triples, len(formula_checks)


def audit_disconnected_coordinate_shores():
    # K12+K2: take the three-vertex K12 component as shore.  Its two free
    # edges form the exceptional path; all cross blocks from the other
    # component and root 0 have fixed shore factors.
    path_identities, path_categories = SHORE["audit_path_factorization"]()
    require(path_identities == 64 and path_categories == {
        "all_cross": 6, "34": 3, "35": 3, "45": 3,
    }, "three-site path-shore theorem changed")

    # K3+K2: take the zero-potential K3 as shore.  Pair-pencil orthogonality
    # makes its b-lines one common isotropic line, and every inner site's
    # three cross spokes are constant.  The triangle theorem gives 51.
    constant_identities = SHORE["audit_constant_cross_factorization"]()
    require(constant_identities == 64,
            "constant-cross triangle identities changed")
    bounds = {"K12+K2": 49, "K3+K2": 51}
    return path_identities, constant_identities, bounds


def audit_remaining_connected_normal_forms():
    # Representatives of the only remaining paired lines.  Their mutual
    # J-pairing vanishes, while both self-pairings are nonzero.  Thus each
    # rank-one endpoint has both selected columns live.
    b_a = (Q(1), Q(1))
    b_b = (Q(1), Q(-1))
    require(pairing(b_a, b_b) == 0,
            "remaining paired-pencil shores stopped being orthogonal")
    require(pairing(b_a, b_a) != 0 and pairing(b_b, b_b) != 0,
            "remaining paired-pencil line became isotropic")
    require(all(b_a) and all(b_b),
            "remaining rank-one site lost a selected column")
    require(b_b == (b_a[0], -b_a[1]),
            "paired-pencil slopes stopped being antipodal")

    normal_forms = {
        "K14": {
            "potential shores": (1, 4),
            "free blocks": 4,
            "within-shore blocks": "fixed nonzero rank one",
            "0-spokes": "constant on each pencil shore",
        },
        "K23": {
            "potential shores": (2, 3),
            "free blocks": 6,
            "within-shore blocks": "fixed nonzero rank one",
            "0-spokes": "constant on each pencil shore",
        },
    }

    # X0 invertible and both columns of every rank-one X_i nonzero make the
    # R2 preservation alternative fail at all six roots.  The residual R2
    # condition is therefore exactly two distinct internal pure-column
    # witnesses, one for each physical binary output, at every root.
    r2 = {
        0: (
            "some h_i is physical e_0",
            "some distinct h_j is physical e_1",
        ),
    }
    r2.update({
        root: ("internal pure-column 0", "internal pure-column 1")
        for root in range(1, 6)
    })
    require(all(left != right for left, right in r2.values()),
            "remaining R2 witness labels collided")

    # At root 0, every internal block is a nonzero-g outer product g h_i^T.
    # Such a block is supported in physical output column c exactly when
    # h_i is on the corresponding physical coordinate axis.  Audit the
    # equivalence without changing basis.
    g = (Q(2), Q(3))
    h_zero = (Q(5), Q(0))
    h_one = (Q(0), Q(7))
    h_mixed = (Q(11), Q(13))

    def pure_output_column(block, column):
        other = 1 - column
        return (all(block[row][other] == 0 for row in range(2))
                and any(block[row][column] != 0 for row in range(2)))

    require(pure_output_column(outer(g, h_zero), 0)
            and not pure_output_column(outer(g, h_zero), 1),
            "physical h=e0 stopped giving exactly pure output column 0")
    require(pure_output_column(outer(g, h_one), 1)
            and not pure_output_column(outer(g, h_one), 0),
            "physical h=e1 stopped giving exactly pure output column 1")
    require(not any(pure_output_column(outer(g, h_mixed), column)
                    for column in range(2)),
            "mixed physical h unexpectedly became a pure output column")
    return normal_forms, r2


def audit_frontier_map():
    frontier = {
        "has isolated vertex": "rank <= 42",
        "K5": "rank <= 42",
        "K3+K2": "rank <= 51",
        "K12+K2": "rank <= 49",
        "K14": "open connected residual",
        "K23": "open connected residual",
    }
    require(sum("open" in value for value in frontier.values()) == 2,
            ("1I+5R frontier count changed", frontier))
    return frontier


def main():
    graphs = audit_zero_sum_graph_classification()
    pencil = audit_rank_one_pair_pencil()
    fixed = audit_fixed_root_bound()
    complete = audit_complete_orthogonal_pencil()
    shores = audit_disconnected_coordinate_shores()
    residual = audit_remaining_connected_normal_forms()
    frontier = audit_frontier_map()

    print("1I+5R potential/support reduction: passed")
    print(f"  zero-sum graph signatures     : {graphs[0]}")
    print(f"  pair-pencil identities/images : {pencil[0]}/{len(pencil[1])}")
    print(f"  fixed-root cases/bound        : {fixed}")
    print(f"  complete orthogonal pencils   : {complete}")
    print(f"  disconnected shore bounds     : {shores}")
    print(f"  connected covariant residues  : {residual[0]}")
    print(f"  literal R2 residual roots     : {len(residual[1])}/6")
    print(f"  frontier                      : {frontier}")


if __name__ == "__main__":
    main()
