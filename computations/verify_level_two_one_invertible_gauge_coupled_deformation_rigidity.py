#!/usr/bin/env python3
"""Exact deformation rigidity of the minimal gauge-coupled 1I+5Z packet.

Enlarge the canonical rank-38 construction by allowing arbitrary 2x2
blocks on the five zero-sum edges, independent scalar E01 blocks on the
four mixed cross edges, and all endpoint coefficients on the same minimal
supports.  Require the pure slices exactly and require both mixed tangents
to remain multiples of the canonical vertex gauge.

The exact 40-by-34 Jacobian has rank 25.  Its nine-dimensional kernel has
seven residual directions, exactly the tangent space of the diagonal-torus
residual orbit, plus two endpoint-only rescalings.  Direct equations then
classify every solution on the nonzero local chart, so every integrated
member still has rank 38.  Standard library only; live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
BASE = run_path(str(
    HERE / "verify_level_two_one_invertible_minimal_gauge_coupled_l0_family.py"
))
CORE = BASE["CORE"]
COLOURS = (0, 1)
ZERO_SUM_EDGES = ((0, 1), (0, 2), (1, 3), (2, 3), (4, 5))
CROSS_EDGES = ((0, 4), (0, 5), (1, 4), (1, 5))
SIGNS = {0: 1, 1: -1}

RESIDUAL_NAMES = tuple(
    f"m{r}{u}{a}{b}"
    for r, u in ZERO_SUM_EDGES
    for a, b in product(COLOURS, repeat=2)
) + tuple(f"m{r}{u}" for r, u in CROSS_EDGES)
ENDPOINT_NAMES = (
    "a0", "a1", "b0", "b1", "c4", "c5", "d4", "d5",
    "lambda", "mu",
)
VARIABLE_NAMES = RESIDUAL_NAMES + ENDPOINT_NAMES
VARIABLE_INDEX = {name: index for index, name in enumerate(VARIABLE_NAMES)}
N_VARIABLES = len(VARIABLE_NAMES)


class Jet:
    """A rational value and its first derivative in all ansatz variables."""

    __slots__ = ("value", "gradient")

    def __init__(self, value, gradient=None):
        self.value = Q(value)
        self.gradient = (
            tuple(Q(0) for _ in range(N_VARIABLES))
            if gradient is None else tuple(Q(entry) for entry in gradient)
        )

    def __add__(self, other):
        other = as_jet(other)
        return Jet(
            self.value + other.value,
            tuple(left + right
                  for left, right in zip(self.gradient, other.gradient)),
        )

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.value, tuple(-entry for entry in self.gradient))

    def __sub__(self, other):
        return self + (-as_jet(other))

    def __rsub__(self, other):
        return as_jet(other) - self

    def __mul__(self, other):
        other = as_jet(other)
        return Jet(
            self.value * other.value,
            tuple(
                self.value * right + left * other.value
                for left, right in zip(self.gradient, other.gradient)
            ),
        )

    __rmul__ = __mul__


def as_jet(value):
    return value if isinstance(value, Jet) else Jet(value)


def variable(name, value):
    gradient = [Q(0)] * N_VARIABLES
    gradient[VARIABLE_INDEX[name]] = Q(1)
    return Jet(value, gradient)


def canonical_point():
    point = {name: Q(0) for name in VARIABLE_NAMES}
    for edge in ((0, 2), (1, 3)):
        point[f"m{edge[0]}{edge[1]}11"] = Q(1)
    for edge in ((2, 3), (4, 5)):
        point[f"m{edge[0]}{edge[1]}00"] = Q(1)
    for edge in CROSS_EDGES:
        point[f"m{edge[0]}{edge[1]}"] = Q(1)
    point.update({
        "a0": Q(1), "a1": Q(-1),
        "b0": Q(-1, 2), "b1": Q(1, 2),
        "c4": Q(1, 2), "c5": Q(1, 2),
        "d4": Q(1), "d5": Q(1),
        "lambda": Q(1), "mu": Q(-1, 4),
    })
    return point


def block_entry(values, edge, a, b):
    return values[f"m{edge[0]}{edge[1]}{a}{b}"]


def ansatz_equations(values):
    a = {i: values[f"a{i}"] for i in (0, 1)}
    b = {i: values[f"b{i}"] for i in (0, 1)}
    c = {j: values[f"c{j}"] for j in (4, 5)}
    d = {j: values[f"d{j}"] for j in (4, 5)}
    n00 = a[0] * b[1] + b[0] * a[1]
    n11 = c[4] * d[5] + d[4] * c[5]

    equations = []
    for word in product(COLOURS, repeat=4):
        # Complement 2345: only the matching 23|45 survives the support.
        h = (
            block_entry(values, (2, 3), word[0], word[1])
            * block_entry(values, (4, 5), word[2], word[3])
        )
        equations.append(n00 * h - int(word == (0, 0, 0, 0)))

    for word in product(COLOURS, repeat=4):
        # Complement 0123: the matchings 01|23 and 02|13 survive.
        h = (
            block_entry(values, (0, 1), word[0], word[1])
            * block_entry(values, (2, 3), word[2], word[3])
            + block_entry(values, (0, 2), word[0], word[2])
            * block_entry(values, (1, 3), word[1], word[3])
        )
        equations.append(n11 * h - int(word == (1, 1, 1, 1)))

    for i in (0, 1):
        for j in (4, 5):
            cross = values[f"m{i}{j}"]
            equations.append(
                a[i] * d[j]
                - values["lambda"] * SIGNS[i] * cross
            )
    for i in (0, 1):
        for j in (4, 5):
            cross = values[f"m{i}{j}"]
            equations.append(
                b[i] * c[j]
                - values["mu"] * SIGNS[i] * cross
            )
    require(len(equations) == 40, "the enlarged ansatz equation count changed")
    return tuple(equations)


def residual_tangent_constraints():
    rows = []

    def coordinate(name):
        row = [Q(0)] * N_VARIABLES
        row[VARIABLE_INDEX[name]] = Q(1)
        return row

    for edge, live in (
        ((0, 1), None),
        ((0, 2), (1, 1)),
        ((1, 3), (1, 1)),
        ((2, 3), (0, 0)),
        ((4, 5), (0, 0)),
    ):
        for a, b in product(COLOURS, repeat=2):
            if live is not None and (a, b) == live:
                continue
            rows.append(coordinate(f"m{edge[0]}{edge[1]}{a}{b}"))

    # Tangent equation to det((m_ij))=0 at the all-one cross matrix.
    rectangle = [Q(0)] * N_VARIABLES
    for edge, coefficient in (
        ((0, 4), 1), ((0, 5), -1),
        ((1, 4), -1), ((1, 5), 1),
    ):
        rectangle[VARIABLE_INDEX[f"m{edge[0]}{edge[1]}"]] = Q(coefficient)
    rows.append(rectangle)
    require(len(rows) == 17, "the residual tangent constraint count changed")
    require(CORE["rational_rank"](rows) == 17,
            "the residual tangent constraints are dependent")
    return rows


def audit_exact_jacobian():
    point = canonical_point()
    jets = {name: variable(name, point[name]) for name in VARIABLE_NAMES}
    equations = ansatz_equations(jets)
    require(all(equation.value == 0 for equation in equations),
            "the canonical point left the enlarged ansatz")
    jacobian = [list(equation.gradient) for equation in equations]
    rank = CORE["rational_rank"](jacobian)
    require((len(jacobian), len(jacobian[0]), rank) == (40, 34, 25),
            ("the enlarged ansatz Jacobian changed", rank))
    nullity = N_VARIABLES - rank
    require(nullity == 9, ("the ansatz tangent nullity changed", nullity))

    endpoint_columns = tuple(range(len(RESIDUAL_NAMES), N_VARIABLES))
    endpoint_matrix = [
        [row[column] for column in endpoint_columns] for row in jacobian
    ]
    endpoint_rank = CORE["rational_rank"](endpoint_matrix)
    endpoint_only_nullity = len(endpoint_columns) - endpoint_rank
    require((endpoint_rank, endpoint_only_nullity) == (8, 2),
            ("the endpoint-only tangent count changed", endpoint_rank))
    residual_projection = nullity - endpoint_only_nullity
    require(residual_projection == 7,
            ("the residual tangent projection changed", residual_projection))

    constraints = residual_tangent_constraints()
    augmented_rank = CORE["rational_rank"](jacobian + constraints)
    require(augmented_rank == rank,
            ("a claimed residual rigidity row is not a Jacobian consequence",
             augmented_rank, rank))
    return jacobian, rank, nullity, residual_projection, endpoint_only_nullity


def integrated_member():
    p, q = 2, 3
    beta, gamma = 5, 7
    left = {0: 11, 1: 13}
    right = {4: 17, 5: 19}

    packet = {cell: 0 for cell in CORE["CELLS"]}
    packet[0, 2, 1, 1] = beta
    packet[1, 3, 1, 1] = gamma
    packet[2, 3, 0, 0] = p
    packet[4, 5, 0, 0] = q
    for i in (0, 1):
        for j in (4, 5):
            packet[i, j, 0, 1] = left[i] * right[j]

    kappa = Q(-1, 2 * left[0] * left[1] * p * q)
    eta = Q(1, 2 * right[4] * right[5] * beta * gamma)
    u_star = {
        (s, r, a): Q(0)
        for s in COLOURS for r in BASE["SITES"] for a in COLOURS
    }
    v_star = dict(u_star)
    u_star[0, 0, 0] = left[0]
    u_star[0, 1, 0] = -left[1]
    v_star[0, 0, 0] = kappa * left[0]
    v_star[0, 1, 0] = -kappa * left[1]
    u_star[1, 4, 1] = eta * right[4]
    u_star[1, 5, 1] = eta * right[5]
    v_star[1, 4, 1] = right[4]
    v_star[1, 5, 1] = right[5]
    return packet, u_star, v_star, (p, q, beta, gamma, left, right)


def audit_integrated_family_member():
    packet, u_star, v_star, parameters = integrated_member()
    tangents = {
        (s, t): BASE["factored_tangent"](u_star, v_star, s, t)
        for s, t in product(COLOURS, repeat=2)
    }
    outputs = {
        key: CORE["apply_differential"](packet, tangent)
        for key, tangent in tangents.items()
    }
    require(outputs == {
        (0, 0): [int(word == (0,) * 6) for word in CORE["WORDS"]],
        (0, 1): [0] * 64,
        (1, 0): [0] * 64,
        (1, 1): [int(word == (1,) * 6) for word in CORE["WORDS"]],
    }, "the integrated enlarged-family member lost the four L0 slices")

    p, q, beta, gamma, left, right = parameters
    diagonal = {
        0: (left[0], beta),
        1: (left[1], gamma),
        2: (p, 1),
        3: (1, 1),
        4: (q, right[4]),
        5: (1, right[5]),
    }
    require(BASE["transform_packet"](BASE["M"], diagonal) == packet,
            "the classified residual member is not in the diagonal orbit")

    derivative = CORE["differential_matrix"](packet)
    mixed = [
        row for row, word in zip(derivative, CORE["WORDS"])
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": BASE["ranks_over_fields"](derivative),
        "D_mixed": BASE["ranks_over_fields"](mixed),
    }
    require(ranks == {
        "D": (38, 38, 38, 38),
        "D_mixed": (36, 36, 36, 36),
    }, ("the integrated family rank changed", ranks))
    require(BASE["audit_literal_eight_site_slices"](
        packet, u_star, v_star
    ) == 256, "the literal eight-site audit changed")
    endpoint_ranks, generic, preserving = BASE["audit_selected_block_and_r2"](
        packet
    )
    return ranks, endpoint_ranks, generic, preserving


def audit_classification_implications():
    # The hand classification uses only these nonzero pivot facts on its
    # local chart.  Pin them on the integrated member and verify the exact
    # rank-one cross rectangle forced by either mixed gauge equation.
    packet, u_star, v_star, _parameters = integrated_member()
    cross = {
        (i, j): packet[i, j, 0, 1]
        for i in (0, 1) for j in (4, 5)
    }
    require(all(cross.values()), "a classified cross weight vanished")
    require(
        cross[0, 4] * cross[1, 5]
        == cross[0, 5] * cross[1, 4],
        "the classified cross matrix is not rank one",
    )
    n00 = (
        u_star[0, 0, 0] * v_star[0, 1, 0]
        + v_star[0, 0, 0] * u_star[0, 1, 0]
    )
    n11 = (
        u_star[1, 4, 1] * v_star[1, 5, 1]
        + v_star[1, 4, 1] * u_star[1, 5, 1]
    )
    require(n00 and n11, "a pure tangent coefficient vanished")
    require(n00 * packet[2, 3, 0, 0] * packet[4, 5, 0, 0] == 1,
            "the classified pure-zero scalar identity failed")
    require(n11 * packet[0, 2, 1, 1] * packet[1, 3, 1, 1] == 1,
            "the classified pure-one scalar identity failed")
    return len(cross)


def main():
    _jacobian, rank, nullity, residual, endpoint = audit_exact_jacobian()
    ranks, endpoint_ranks, generic, preserving = audit_integrated_family_member()
    cross = audit_classification_implications()
    print("one-invertible gauge-coupled deformation rigidity: all checks passed")
    print(f"  enlarged ansatz Jacobian    : 40x34, rank {rank}, nullity {nullity}")
    print(f"  residual tangent projection : {residual} dimensions")
    print(f"  endpoint-only tangents      : {endpoint} dimensions")
    print(f"  classified cross weights    : {cross}/4, rank-one rectangle")
    print(f"  integrated differential     : {ranks}")
    print(f"  endpoint ranks              : {endpoint_ranks}")
    print(f"  generic/R2 preserving roots : {generic}/60, {len(preserving)}/5")
    print("  conclusion                  : enlarged sparse family stays rank 38")


if __name__ == "__main__":
    main()
