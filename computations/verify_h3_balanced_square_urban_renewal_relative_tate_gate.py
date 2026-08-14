#!/usr/bin/env python3
"""Audit urban renewal on the h=3 balanced chart square.

The four chart vertices are the two ordered copies of the direct DQ chart
and the two endpoint PS charts.  The formal mate columns form a signless
K2,2 and miss z=(1,1,-1,-1).  This checker tests the strongest ordinary
four-terminal square move on that packet.

For a square with cyclic weights a,b,c,d, urban renewal has denominator

    Delta=a*c+b*d

and renewed weights (c,d,a,b)/Delta.  The checker verifies the complete
sixteen-state boundary signature identity over the universal rational
function field and the involution formula.  On D(Delta) this is a
birational degree-zero coordinate change.  It replaces edge-incidence
columns by edge-incidence columns and therefore cannot create a column of
nonzero balanced/gauged vertex augmentation.

The minimal H0-preserving relative Tate column is also audited:

    dG=t-Delta*z.

It has nonzero z-component on D(Delta), but the primitive dual extends with
value Delta on t.  It is a formal retained carrier, not an absolute filler
and not a consequence of urban renewal.  On Delta=0 it reduces to dG=t and
leaves z untouched.  The four edge-graph equations have no lift at a
nonzero Delta=0 square and acquire an excess A^4 fibre over the all-zero
square.  The full normalized signature move has no finite Delta=0 point at
all, because it also requires Delta*Delta'=1.  No physical cross-grade
label map is manufactured here.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_balanced_chart_square_master_obstruction.py":
        "306980dc569795fa3ec2c8e6fdbdf2b67fa5d85cd75ebebe62be7db15b1e1a59",
    "computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py":
        "10c2ca7ca9168d41f25f428b628710c0eaf8bc2aa910e23100da161869fdc72e",
    "computations/verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py":
        "48bb5568b6d3360dd592011ed09aca364cfdbd24770d2e2419c1f99464825878",
    "computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py":
        "d77f4fd853673c434d4a0bb4027bf9ba046f1bb7ea4d752028a609e832255f44",
}
EXPECTED_LEDGER_SHA256 = (
    "d6eb23ef7b715c02eb933f98f957250c4b2bfdf205bb7bd8362cfa1545ace000"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((vector[index] for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * value for value in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or rows[row][column] == 0:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


class Poly:
    """A tiny exact Q[a,b,c,d] implementation."""

    def __init__(self, terms: dict[tuple[int, int, int, int], Q] | None = None):
        self.terms = {monomial: Q(coefficient)
                      for monomial, coefficient in (terms or {}).items()
                      if coefficient}

    @classmethod
    def constant(cls, value: int | Q) -> "Poly":
        return cls({(0, 0, 0, 0): Q(value)}) if value else cls()

    @classmethod
    def variable(cls, index: int) -> "Poly":
        exponent = [0, 0, 0, 0]
        exponent[index] = 1
        return cls({tuple(exponent): Q(1)})

    def __add__(self, other: "Poly") -> "Poly":
        terms = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            terms[monomial] = terms.get(monomial, Q(0)) + coefficient
        return Poly(terms)

    def __neg__(self) -> "Poly":
        return Poly({monomial: -coefficient
                     for monomial, coefficient in self.terms.items()})

    def __sub__(self, other: "Poly") -> "Poly":
        return self + (-other)

    def __mul__(self, other: "Poly") -> "Poly":
        terms: dict[tuple[int, int, int, int], Q] = {}
        for left, left_coefficient in self.terms.items():
            for right, right_coefficient in other.terms.items():
                monomial = tuple(a + b for a, b in
                                 zip(left, right, strict=True))
                terms[monomial] = (terms.get(monomial, Q(0))
                                   + left_coefficient * right_coefficient)
        return Poly(terms)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Poly) and self.terms == other.terms

    def __bool__(self) -> bool:
        return bool(self.terms)


class Rat:
    """Unreduced exact rational functions, compared by cross multiplication."""

    def __init__(self, numerator: Poly, denominator: Poly | None = None):
        self.numerator = numerator
        self.denominator = denominator or Poly.constant(1)
        require(bool(self.denominator), "zero rational denominator")

    @classmethod
    def zero(cls) -> "Rat":
        return cls(Poly())

    @classmethod
    def one(cls) -> "Rat":
        return cls(Poly.constant(1))

    def __add__(self, other: "Rat") -> "Rat":
        return Rat(self.numerator * other.denominator
                   + other.numerator * self.denominator,
                   self.denominator * other.denominator)

    def __mul__(self, other: "Rat") -> "Rat":
        return Rat(self.numerator * other.numerator,
                   self.denominator * other.denominator)

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Rat)
                and self.numerator * other.denominator
                == other.numerator * self.denominator)


def square_signature(weights: tuple[Rat, Rat, Rat, Rat],
                     removed: frozenset[int]) -> Rat:
    """Perfect-matching signature after the listed terminals are removed."""
    remaining = frozenset(range(4)) - removed
    if not remaining:
        return Rat.one()
    if len(remaining) == 4:
        a, b, c, d = weights
        return a * c + b * d
    if len(remaining) != 2:
        return Rat.zero()
    edge_for_pair = {
        frozenset((0, 1)): 0,
        frozenset((1, 2)): 1,
        frozenset((2, 3)): 2,
        frozenset((0, 3)): 3,
    }
    return weights[edge_for_pair[remaining]] \
        if remaining in edge_for_pair else Rat.zero()


def urban_renewal_signature_audit() -> dict[str, object]:
    variables = tuple(Poly.variable(index) for index in range(4))
    a, b, c, d = variables
    delta = a * c + b * d
    old = tuple(Rat(value) for value in variables)
    renewed = (Rat(c, delta), Rat(d, delta),
               Rat(a, delta), Rat(b, delta))
    delta_rat = Rat(delta)

    states = tuple(frozenset(subset)
                   for size in range(5)
                   for subset in combinations(range(4), size))
    for removed in states:
        complement = frozenset(range(4)) - removed
        left = square_signature(old, removed)
        right = delta_rat * square_signature(renewed, complement)
        require(left == right,
                ("urban-renewal boundary signature changed", removed))

    renewed_delta = renewed[0] * renewed[2] + renewed[1] * renewed[3]
    require(renewed_delta == Rat(Poly.constant(1), delta),
            "renewed denominator stopped being Delta^{-1}")
    twice = (
        Rat(renewed[2].numerator * renewed_delta.denominator,
            renewed[2].denominator * renewed_delta.numerator),
        Rat(renewed[3].numerator * renewed_delta.denominator,
            renewed[3].denominator * renewed_delta.numerator),
        Rat(renewed[0].numerator * renewed_delta.denominator,
            renewed[0].denominator * renewed_delta.numerator),
        Rat(renewed[1].numerator * renewed_delta.denominator,
            renewed[1].denominator * renewed_delta.numerator),
    )
    require(all(left == right for left, right in zip(twice, old, strict=True)),
            "urban renewal stopped being an involution")
    return {
        "cyclic_old_weights": ["a", "b", "c", "d"],
        "denominator": "Delta=a*c+b*d",
        "renewed_weights": ["c/Delta", "d/Delta", "a/Delta", "b/Delta"],
        "boundary_rule": "Sig_old(R)=Delta*Sig_new(V\\R)",
        "boundary_states_checked": len(states),
        "renewed_denominator": "1/Delta",
        "involution": True,
        "domain": "the principal open D(Delta)",
    }


def labelled_balanced_square_audit() -> dict[str, object]:
    # Vertex order: two ordered DQ copies and the two endpoint PS charts.
    # All four carry the same fixed tail H_2345 but retain distinct operation
    # idempotents.  The formal mate columns are the four K2,2 edges.
    z = (Q(1), Q(1), Q(-1), Q(-1))
    edges = (
        (Q(1), Q(0), Q(1), Q(0)),  # A_[D|Q] + B_[P0|S1]
        (Q(1), Q(0), Q(0), Q(1)),  # A_[D|Q] + C_[P1|S0]
        (Q(0), Q(1), Q(1), Q(0)),  # A_[Q|D] + B_[P0|S1]
        (Q(0), Q(1), Q(0), Q(1)),  # A_[Q|D] + C_[P1|S0]
    )
    require(rank(edges) == 3
            and all(dot(z, edge) == 0 for edge in edges)
            and rank(edges + (z,)) == 4,
            "the labelled balanced square changed")
    gauge = z
    oriented = tuple(tuple(gauge[index] * value
                           for index, value in enumerate(edge))
                     for edge in edges)
    augmentation = (Q(1),) * 4
    require(all(dot(augmentation, edge) == 0 for edge in oriented)
            and tuple(gauge[index] * z[index] for index in range(4))
            == augmentation,
            "the shore-sign incidence gauge changed")

    # Renewal permutes edge weights by opposite edge and rescales them.  Its
    # terminal boundary supports are still these four incidence columns.
    opposite_permutation = (3, 2, 1, 0)
    renewed_supports = tuple(edges[index] for index in opposite_permutation)
    require(rank(renewed_supports) == 3
            and all(dot(z, edge) == 0 for edge in renewed_supports),
            "urban renewal acquired balanced augmentation")
    return {
        "fixed_window": [2, 3, 4, 5],
        "fixed_tail": "H=q23*q45+q24*q35+q25*q34",
        "vertices": [
            {
                "name": "A_[D|Q]",
                "coefficient": "D*q01*H",
                "grade": "Hasse[2](D,Q01), ordered D|Q",
            },
            {
                "name": "A_[Q|D]",
                "coefficient": "D*q01*H",
                "grade": "Hasse[2](D,Q01), ordered Q|D",
            },
            {
                "name": "B",
                "coefficient": "p0*s1*H",
                "grade": "Hasse[2](P0,S1)",
            },
            {
                "name": "C",
                "coefficient": "p1*s0*H",
                "grade": "Hasse[2](P1,S0)",
            },
        ],
        "balanced_face": "Z=A_[D|Q]+A_[Q|D]-B-C",
        "Gate_II_projection": "Z -> 2*A-B-C=L01",
        "formal_mate_rank": 3,
        "balanced_dual": ["1/4", "1/4", "-1/4", "-1/4"],
        "shore_gauge": [1, 1, -1, -1],
        "gauged_face": [1, 1, 1, 1],
        "urban_renewal_support_image": (
            "ordinary terminal incidence = kernel of gauged augmentation"
        ),
        "urban_renewal_nonzero_augmentation_column": False,
        "physical_input_scope": (
            "the four mate edges already require DQ-to-PS chart switches; "
            "the pinned joint-cobar audit constructs only their formal K2,2 "
            "shadow, not physical cross-grade edge cells"
        ),
    }


def localized_graph_and_zero_fibre_audit() -> dict[str, object]:
    # At a point of D(Delta), the four graph relations
    # Delta*(a',b',c',d')-(c,d,a,b) are monic after division by Delta.
    # Their coefficient shadow has rank four in eight coordinates, hence the
    # graph has the same four degree-zero parameters as the old square.
    delta = Q(2)
    graph_columns = (
        (Q(0), Q(0), Q(-1), Q(0), delta, Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(-1), Q(0), delta, Q(0), Q(0)),
        (Q(-1), Q(0), Q(0), Q(0), Q(0), Q(0), delta, Q(0)),
        (Q(0), Q(-1), Q(0), Q(0), Q(0), Q(0), Q(0), delta),
    )
    require(rank(graph_columns) == 4 and 8 - rank(graph_columns) == 4,
            "the localized renewal graph changed H0")

    def denominator(values: tuple[Q, Q, Q, Q]) -> Q:
        a, b, c, d = values
        return a * c + b * d

    nonzero_zero_delta = (Q(1), Q(1), Q(1), Q(-1))
    require(denominator(nonzero_zero_delta) == 0
            and any(nonzero_zero_delta),
            "the nonzero Delta=0 test point changed")
    # On Delta=0 the graph equations read 0*(new)=(c,d,a,b).  Hence a
    # finite lift exists iff every old edge is zero.  At the origin every
    # renewed coordinate is free.
    rhs = (nonzero_zero_delta[2], nonzero_zero_delta[3],
           nonzero_zero_delta[0], nonzero_zero_delta[1])
    require(any(rhs), "the no-lift right side vanished")
    origin = (Q(0),) * 4
    arbitrary_new_points = (
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(1), Q(2), Q(3), Q(4)),
        (Q(-5), Q(7), Q(11), Q(-13)),
    )
    require(denominator(origin) == 0
            and all(tuple(Q(0) * value for value in point) == origin
                    for point in arbitrary_new_points),
            "the all-zero renewal fibre stopped being free")

    # These four equations are only the closure of the edge-weight graph.
    # The normalized empty/full boundary state of a genuine renewal also
    # imposes Delta*Delta'=1, which has no finite solution on Delta=0.
    for finite_renewed_delta in (Q(-7), Q(0), Q(1), Q(5, 2)):
        require(Q(0) * finite_renewed_delta != Q(1),
                "a finite full-signature Delta=0 renewal appeared")
    return {
        "localized_graph_relations": [
            "Delta*a'-c", "Delta*b'-d",
            "Delta*c'-a", "Delta*d'-b",
        ],
        "localized_old_new_coordinates": 8,
        "localized_graph_rank": 4,
        "localized_H0_dimension": 4,
        "edge_graph_closure_at_zero": {
            "Delta=0_and_some_old_edge_nonzero": (
                "no edge-graph point; at least one equation is 0=nonzero"
            ),
            "all_old_edges_zero": (
                "every renewed edge is free; the edge-graph closure has an "
                "A^4 non-flat fibre over the old origin"
            ),
        },
        "full_signature_at_Delta_zero": (
            "no finite point, even at the origin: the empty/full boundary "
            "state also requires Delta*Delta'=1"
        ),
        "nonzero_Delta0_example": ["1", "1", "1", "-1"],
        "finite_regular_extension_across_Delta0": False,
    }


def relative_tate_cone_audit() -> dict[str, object]:
    # Coordinates are the four square vertices and one retained carrier t.
    # Old mate edges have t-coordinate zero.  The relative graph is
    # g=t-Delta*z.  It raises both the ambient dimension and boundary rank by
    # one, so the unique H0 class remains.  Its dual is forced to take value
    # Delta on t.
    z = (Q(1), Q(1), Q(-1), Q(-1))
    edges = (
        (Q(1), Q(0), Q(1), Q(0), Q(0)),
        (Q(1), Q(0), Q(0), Q(1), Q(0)),
        (Q(0), Q(1), Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0), Q(1), Q(0)),
    )
    psi_vertex = scale(Q(1, 4), z)
    records = []
    for delta in (Q(-3), Q(0), Q(2)):
        graph = tuple(-delta * value for value in z) + (Q(1),)
        dual = psi_vertex + (delta,)
        old_h0 = 4 - rank(tuple(edge[:4] for edge in edges))
        relative_h0 = 5 - rank(edges + (graph,))
        require((old_h0, relative_h0) == (1, 1)
                and all(dot(dual, edge) == 0 for edge in edges)
                and dot(dual, graph) == 0
                and dot(psi_vertex, z) == 1,
                ("the relative Tate carrier changed", delta))

        absolute_t = (Q(0), Q(0), Q(0), Q(0), Q(1))
        rank_with_t = rank(edges + (graph, absolute_t))
        require(rank_with_t == (5 if delta else 4),
                ("the localized absolute saturation rank changed", delta))
        records.append({
            "Delta": str(delta),
            "H0_old_relative": [old_h0, relative_h0],
            "forced_dual_on_t": str(delta),
            "rank_after_absolute_t": rank_with_t,
            "z_filled_after_t": bool(delta),
        })
    return {
        "relative_column": "dG=t-Delta*Z",
        "gauged_z_augmentation": "-4*Delta",
        "presentation_safe_for_all_Delta": True,
        "forced_dual": "psi(Z)=1, psi(t)=Delta",
        "records": records,
        "open_branch": (
            "on D(Delta), a separate physical dE=t gives "
            "Z=Delta^{-1}(t-dG) and closes the square"
        ),
        "zero_branch": (
            "at Delta=0, dG=t; the carrier is killed but Z survives unchanged"
        ),
        "global_colon_class": "(R/(Delta))*Z after absolute t-saturation",
        "urban_renewal_sources_this_column": False,
        "reason": (
            "urban renewal has only edge-incidence output; writing t-Delta*Z "
            "adjoins exactly the missing cross-grade relative datum"
        ),
    }


def first_augmented_faces_audit() -> dict[str, object]:
    # The PP/reinsertion derivation of Delta=a*c+b*d is forced.  Record its
    # four independent terms and the relative-column product rule.  No
    # cancellation can be claimed before the cross-grade maps for t and Z
    # are physically typed.
    derivative_coordinates = (
        (Q(1), Q(0), Q(0), Q(0)),
        (Q(0), Q(1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(0), Q(1)),
    )
    require(rank(derivative_coordinates) == 4,
            "the urban denominator derivative collapsed")
    return {
        "denominator_product_rule": (
            "dDelta=(da)*c+a*(dc)+(db)*d+b*(dd)"
        ),
        "relative_square_product_rule": (
            "d_PP(dG)=d_PP(t)-(dDelta)*Z-Delta*d_PP(Z)"
        ),
        "independent_denominator_faces": 4,
        "fixed_tail_component": (
            "d_PP(Z) contains the already isolated DQ/PS direction and "
            "residual-tail faces on H_2345"
        ),
        "renewed_weight_derivative": (
            "d(c/Delta)=((dc)*Delta-c*dDelta)/Delta^2, and cyclic mates"
        ),
        "consequence": (
            "even on D(Delta), PP naturality requires the same missing "
            "cross-grade restriction/insertion maps and introduces "
            "Delta^{-2}; the coefficient mutation supplies no augmented face"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 balanced-square urban-renewal / relative-Tate gate",
        "pins": PINS,
        "universal_urban_renewal": urban_renewal_signature_audit(),
        "full_source_labels": labelled_balanced_square_audit(),
        "localized_graph_and_zero_fibre": localized_graph_and_zero_fibre_audit(),
        "relative_Tate_cone": relative_tate_cone_audit(),
        "first_augmented_faces": first_augmented_faces_audit(),
        "verdict": (
            "Ordinary four-terminal urban renewal is an exact birational "
            "boundary-signature equivalence on D(Delta), but it only changes "
            "coefficients of the same K2,2 incidence columns and has zero "
            "balanced augmentation.  It cannot create the missing cross-"
            "grade cone.  The formal relative Tate column dG=t-Delta*Z is "
            "H0-preserving and has nonzero Z component on D(Delta), but the "
            "balanced dual extends to t and a separate physical dE=t is "
            "still required.  At Delta=0 the relative column reduces to t "
            "and Z survives.  The edge-graph closure has no point away from "
            "the all-zero square and an excess A4 fibre at the origin, while "
            "the full signature move has no finite Delta=0 point at all."
        ),
        "shortest_positive_datum": (
            "a physically labelled cross-grade carrier t with an absolute "
            "source preimage on D(Delta), together with a separate Delta=0 "
            "terminal/filler theorem; the urban-renewal coefficient identity "
            "does not supply either datum"
        ),
        "nonclaims": [
            "the four formal DQ-to-PS mate edges are not called physical cells",
            "a birational coefficient change is not called a chain boundary",
            "the retained Tate carrier is not called an absolute filler",
            "the Delta=0 non-flat fibre is not called a GHZ source counterexample",
        ],
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("urban renewal on D(Delta): EXACT BIRATIONAL SIGNATURE MOVE")
    print("balanced-square augmentation created: NO")
    print("relative Tate dG=t-Delta*Z: H0-PRESERVING / OBSTRUCTION RETAINED")
    print("Delta=0: NO FULL-SIGNATURE LIFT; EDGE-GRAPH A4 EXCESS AT ORIGIN")
    print("physical DQ/PS cross-grade cone: STILL REQUIRED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
