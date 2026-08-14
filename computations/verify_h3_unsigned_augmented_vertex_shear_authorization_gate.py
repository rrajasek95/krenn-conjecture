#!/usr/bin/env python3
"""Audit full unsigned augmented-vertex shears and their ordered return.

Let X be the projected augmented-vertex shear 0->S and Y its opposite
S->0 on the complete K8 hafnian response R.  They act on every incident
off-diagonal edge and kill the edge 0S because its image would be a loop.
Exactly:

    X R = C_(0,S),
    Y X R = X Y R = 2*(R-s0*d_(s0)R).

C_(0,S) is the symmetric 45-term missing-0/doubled-S collision row, with
coefficient two.  Its complete 180 first-PP flags are Kähler-natural:
varying a retained factor and varying the removed-edge label reconstruct
d(XR)=X(dR) occurrence by occurrence.  The second return lies in the old
complete-response plus coordinate-Euler span.

Neither fact authorizes the first collision face as an absolute physical
boundary.  P,S are operation/head roles rather than GHZ sites; the full
physical coefficient inventory is squarefree and has zero projection to
this collision degree.  The shear supplies a KS/tangent curvature.  An
H0-preserving graph is relative, d kappa=C-t; declaring d kappa=C is the
missing non-diagonal Spencer generator itself.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_chart_unipotent_shear_collision_gate.py":
        "6f05b788400279a8dd19c09acbb1e883eb74c8a9c21f9d00e2bc6a048543922e",
    "notes/uniform-chart-unipotent-shear-collision-gate.md":
        "7fe9e709dd414c101fb1178dc2dee5f5b1d98db0192a525c48cde1e5cfba5a63",
    "computations/verify_h3_fullword_collision_sector_parent_inventory_gate.py":
        "beb11bfb1fbe9aee732cc7975b108270af9c2e70c6ff9155a45cf420e3eb6187",
    "notes/h3-fullword-collision-sector-parent-inventory-gate.md":
        "04968b23ff618ad4262f6a40ebc5190bc4dd449930bc58c7fcb6beeee1795169",
    "computations/verify_h3_h2_fixed_chart_l01_reset_augmented_gate.py":
        "6acd2eec727e1030c58d14da6a2c8b26f884bb0ed5ada02b904c5e4c54d6ca6f",
    "notes/h3-h2-fixed-chart-l01-reset-augmented-gate.md":
        "110e850f43b4520a5a47e53d74f190ae7012547ff87d27da1e27ba4c5568f701",
}
EXPECTED_LEDGER_SHA256 = (
    "00fec8c96544113af5878c91245ffcb0aa746e62df9cb055f8f604a71003e5c9"
)


NAMES = ("P", "S", "0", "1", "2", "3", "4", "5")
P, S, ZERO, ONE, TWO, THREE, FOUR, FIVE = range(8)
VERTICES = tuple(range(8))
Edge = tuple[int, int]
Monomial = tuple[Edge, ...]
Polynomial = Counter[Monomial]
PPFlag = tuple[Monomial, Edge]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def label_edge(value: Edge) -> str:
    left, right = (NAMES[value[0]], NAMES[value[1]])
    if (left, right) == ("P", "S"):
        return "D"
    if left == "P":
        return "p" + right
    if left == "S":
        return "s" + right
    return "q" + left + right


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def moved_edge(value: Edge, source: int, replacement: int) -> Edge | None:
    if source not in value:
        return None
    other = value[1] if value[0] == source else value[0]
    if other == replacement:
        return None
    return edge(replacement, other)


def derivation(polynomial: Polynomial, source: int,
               replacement: int) -> Polynomial:
    answer: Polynomial = Counter()
    for monomial, coefficient in polynomial.items():
        for position, value in enumerate(monomial):
            moved = moved_edge(value, source, replacement)
            if moved is None:
                continue
            output = list(monomial)
            output[position] = moved
            answer[tuple(sorted(output))] += coefficient
    return +answer


def pp(polynomial: Polynomial) -> Counter[PPFlag]:
    answer: Counter[PPFlag] = Counter()
    for monomial, coefficient in polynomial.items():
        for removed in monomial:
            answer[(monomial, removed)] += coefficient
    return +answer


def flag_derivation(flags: Counter[PPFlag], source: int,
                    replacement: int) -> Counter[PPFlag]:
    """Kähler lift: act on retained factors and on the d-edge label."""
    answer: Counter[PPFlag] = Counter()
    for (monomial, removed), coefficient in flags.items():
        for position, value in enumerate(monomial):
            moved = moved_edge(value, source, replacement)
            if moved is None:
                continue
            output = list(monomial)
            output[position] = moved
            output = tuple(sorted(output))
            output_removed = moved if value == removed else removed
            answer[(output, output_removed)] += coefficient
    return +answer


def vertex_degree(monomial: Monomial) -> tuple[int, ...]:
    degree = [0] * len(VERTICES)
    for left, right in monomial:
        degree[left] += 1
        degree[right] += 1
    return tuple(degree)


def rank(rows) -> int:
    rows = [list(map(Q, row)) for row in rows]
    if not rows:
        return 0
    answer = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    shear_pin = load(
        "computations/verify_uniform_chart_unipotent_shear_collision_gate.py",
        "unsigned_shear_scope_pin",
    )
    shear_ledger, shear_digest = shear_pin.audit()
    require(shear_digest == shear_pin.EXPECTED_LEDGER_SHA256
            and shear_ledger["physical_scope"]["GHZ_target_scope"].startswith(
                "P and S are operation/direction roles"),
            "the augmented-vertex authorization gate changed")

    matchings = tuple(perfect_matchings(VERTICES))
    response = Counter({matching: Q(1) for matching in matchings})
    require(len(matchings) == 105
            and {vertex_degree(matching) for matching in matchings}
                == {(1,) * 8},
            "the complete K8 response changed")

    # X is 0->S and Y is S->0.  Their first faces are the two opposite
    # collision multidegrees.
    x_response = derivation(response, ZERO, S)
    y_response = derivation(response, S, ZERO)
    require(len(x_response) == len(y_response) == 45
            and set(x_response.values()) == set(y_response.values()) == {Q(2)}
            and {vertex_degree(value) for value in x_response}
                == {(1, 2, 0, 1, 1, 1, 1, 1)}
            and {vertex_degree(value) for value in y_response}
                == {(1, 0, 2, 1, 1, 1, 1, 1)},
            "the two unsigned first collision faces changed")

    # The complete first PP boundary is exactly natural only when the shear
    # also acts on the removed-edge (Kähler d-edge) label.
    x_pp_direct = pp(x_response)
    x_pp_lifted = flag_derivation(pp(response), ZERO, S)
    y_pp_direct = pp(y_response)
    y_pp_lifted = flag_derivation(pp(response), S, ZERO)
    require(x_pp_direct == x_pp_lifted
            and y_pp_direct == y_pp_lifted
            and len(x_pp_direct) == len(y_pp_direct) == 180
            and set(x_pp_direct.values()) == {Q(2)},
            "[PP,unsigned shear] stopped vanishing")

    unary_groups: Counter[int] = Counter()
    repeated_groups: Counter[Edge] = Counter()
    for (monomial, removed), coefficient in x_pp_direct.items():
        require(coefficient == 2, (monomial, removed, coefficient))
        if S in removed:
            other = removed[1] if removed[0] == S else removed[0]
            unary_groups[other] += 1
        else:
            repeated_groups[removed] += 1
    require(len(unary_groups) == 6 and set(unary_groups.values()) == {15}
            and len(repeated_groups) == 15
            and set(repeated_groups.values()) == {6},
            (unary_groups, repeated_groups))

    # Opposite orders agree.  The selected edge s0=0S cannot move because it
    # would create a loop.  Every other response matching returns twice:
    # once by undoing the moved edge and once by moving the old opposite arm.
    yx = derivation(x_response, S, ZERO)
    xy = derivation(y_response, ZERO, S)
    s0 = edge(S, ZERO)
    edge_euler = Counter({matching: Q(1) for matching in matchings
                          if s0 in matching})
    expected_second = Counter({matching: Q(2) for matching in matchings
                               if s0 not in matching})
    require(yx == xy == expected_second
            and len(edge_euler) == 15 and len(expected_second) == 90,
            "the ordered unsigned return changed")
    return_order = tuple(sorted(response))
    response_vector = tuple(Q(1) for _matching in return_order)
    euler_vector = tuple(Q(edge_euler[matching]) for matching in return_order)
    second_vector = tuple(Q(expected_second[matching])
                          for matching in return_order)
    expected_vector = tuple(2 * (one - euler)
                            for one, euler in
                            zip(response_vector, euler_vector, strict=True))
    require(second_vector == expected_vector
            and rank((response_vector, euler_vector)) == 2
            and rank((response_vector, euler_vector, second_vector)) == 2,
            "2*(R-s0*d_s0 R) left the response/Euler span")

    # Literal selected-chart return.  Tensoring by H2345 is passive.
    D = edge(P, S)
    q01 = edge(ZERO, ONE)
    p0 = edge(P, ZERO)
    s1 = edge(S, ONE)
    a = Counter({tuple(sorted((D, q01))): Q(1)})
    b = Counter({tuple(sorted((p0, s1))): Q(1)})
    a_plus_b = a + b
    require(derivation(derivation(a, ZERO, S), S, ZERO) == a_plus_b
            and derivation(derivation(a, S, ZERO), ZERO, S) == a_plus_b,
            "the unsigned A+B ordered return changed")

    # Absolute d kappa=C drops the collision coordinate from H0.  The graph
    # d kappa=C-t raises coordinates and rank together, preserving it.  This
    # is the minimal linear authorization distinction.
    absolute = ((Q(1),),)
    relative = ((Q(1), Q(-1)),)
    require(1 - rank(absolute) == 0
            and 2 - rank(relative) == 1,
            "the absolute/relative collision graph H0 fork changed")

    ledger = {
        "theorem": "h3 unsigned augmented-vertex shear authorization gate",
        "pins": PINS,
        "unsigned_pair": {
            "vertices_are_roles": ["0", "S"],
            "forward": "X: 0->S on every incident off-diagonal edge",
            "reverse": "Y: S->0 on every incident off-diagonal edge",
            "loop_projection": "X(s0)=Y(s0)=0",
        },
        "complete_response_first_faces": {
            "X_R": "C_(0,S), missing 0 / doubled S",
            "Y_R": "C_(S,0), missing S / doubled 0",
            "terms_each": 45,
            "coefficient": 2,
            "physical_squarefree_projection": 0,
            "authorization": "KS/tangent curvature, not absolute boundary",
        },
        "first_PP": {
            "identity": "d(XR)=X(dR), including X(d-edge)",
            "flags": len(x_pp_direct),
            "coefficients": "2 on all 180",
            "unary_groups": {
                NAMES[key]: value for key, value in unary_groups.items()
            },
            "repeated_groups": {
                label_edge(key): value for key, value in repeated_groups.items()
            },
            "algebraically_closed": True,
            "physical_absolute_cell_constructed": False,
        },
        "ordered_second_response": {
            "identity": "YX(R)=XY(R)=2*(R-s0*d_s0 R)",
            "complete_response_terms": len(response),
            "s0_Euler_terms": len(edge_euler),
            "returned_terms": len(expected_second),
            "rank_R_Euler": 2,
            "rank_after_return": 2,
            "coefficient_closure": "2R-2E_s0(R), in old R+coordinate-Euler span",
            "selected_chart": "YX(A)=XY(A)=A+B",
        },
        "authorization": {
            "P_S_are_physical_GHZ_sites": False,
            "global_even_product_repairs_target_scope": False,
            "reason": (
                "there is no induced GHZ action for an augmented operation-"
                "role shear; the physical 3^8 coefficient inventory remains "
                "squarefree and projects zero to C_(0,S)"
            ),
            "absolute_model": "d kappa=C; H0 1->0; unauthorized",
            "presentation_safe_model": "d kappa=C-t; H0 1->1; relative",
            "retained_carrier_absolute_landing": False,
        },
        "verdict": (
            "The unsigned construction removes the signed 24-term residual "
            "and has perfect first-PP and second-order coefficient algebra.  "
            "It does not supply a physical source boundary.  C_(0,S) is the "
            "nonzero curvature of a shear mixing operation/head roles, not "
            "a relation generated by the squarefree GHZ source.  The old "
            "R+Euler rows close the ordered second return but do not make the "
            "first collision carrier absolute."
        ),
        "sharp_extra_hypothesis": (
            "one source-labelled non-diagonal Spencer/Tate generator with "
            "absolute boundary C_(0,S), complete 180-flag PP naturality, and "
            "all target/Eq/q/anchor/W/ordinary-residue/ridge faces.  Without "
            "it only d kappa=C-t is presentation-safe."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("unsigned first face: SYMMETRIC 45-TERM COLLISION C_(0,S)")
    print("first PP: 180 FLAGS, [PP,X]=0 INCLUDING d-EDGE ACTION")
    print("ordered return: 2*(R-s0*d_s0 R), OLD R+EULER SPAN")
    print("source authorization: RELATIVE KS CURVATURE, NOT ABSOLUTE")
    print("global even GHZ argument: TYPE ERROR (P,S ARE HEAD ROLES)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
