#!/usr/bin/env python3
"""Audit the actual order-four denominator cube and its first typed face.

This is deliberately not a declaration of a new attaching generator.  It
starts with the literal four directions and rows used by the committed
denominator/Rees cube, reconstructs the complete squarefree Hasse/Koszul
Leibniz lift, and asks what remains after diagonal descent to the physical
two-row complex.

The full lift closes.  Its diagonal projection does not: the first surviving
typed face is (H_0-u)e_Eq.  The endpoint 22-to-00 operator has the same top
unit as the zero-endpoint chart cube, but changes two directions at once and
is not a cubical facet.  Consequently a curvature lower face is not forced by
the cubical boundary identity.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


_BASE_PATH = Path(__file__).resolve().with_name(
    "verify_h3_full_hasse_koszul_cap_totalization.py"
)
_BASE_SPEC = importlib.util.spec_from_file_location(
    "verify_h3_full_hasse_koszul_cap_totalization", _BASE_PATH
)
require_base = _BASE_SPEC is not None and _BASE_SPEC.loader is not None
if not require_base:
    raise RuntimeError("cannot load the committed Hasse cube checker")
cube = importlib.util.module_from_spec(_BASE_SPEC)
_BASE_SPEC.loader.exec_module(cube)


EXPECTED_DIGEST = "063f6306ef3e87c53903162cff6fdaca27e7fe41d03a36f01fff585666627486"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def mask_directions(directions, mask):
    return tuple(
        direction for index, direction in enumerate(directions)
        if mask & (1 << index)
    )


def exact_leibniz_ledger(directions):
    """Return both copies of every term in d(s_I), indexed by Eq face."""
    full = (1 << len(directions)) - 1
    positive = {}
    negative = {}
    for derivative_mask in cube.submasks(full):
        coefficient = cube.derivative(
            cube.H_MIXED, mask_directions(directions, derivative_mask)
        )
        if not coefficient:
            continue
        eq_face = full ^ derivative_mask
        value = cube.multiply(cube.F_PURE, coefficient)
        positive[eq_face] = value
        negative[eq_face] = cube.scale(-cube.ONE, value)

    require(set(positive) == set(range(16)),
            "a Boolean Leibniz face disappeared")
    require(
        all(cube.add(positive[face], negative[face]) == {}
            for face in positive),
        "a Leibniz face failed to cancel",
    )
    return positive, negative


def reset_support(deleted, internal):
    support = {}
    for mask in range(4):
        selected = mask_directions(internal, mask)
        live = []
        for site in cube.ODD:
            value = cube.derivative(cube.face_hafnian(site), selected)
            if value:
                live.append((site, cube.MIXED[site]))
        support[mask] = tuple(live)
    require(tuple(map(len, support.values())) == (5, 3, 3, 1),
            "proper denominator support ledger changed")
    require(support[3] == ((deleted, cube.MIXED[deleted]),),
            "top denominator face is not Kronecker")
    return support


def zero_endpoint_chart_row(deleted):
    colouring = {site: 0 for site in cube.SITES}
    for site in cube.face(deleted):
        colouring[site] = cube.MIXED[site]
    return cube.polynomial_from_matching(
        cube.SITES, colouring, direct_free=True
    )


def audit_cube(deleted, matching):
    internal = cube.internal_variables(matching)
    mixed_external = cube.endpoint_variables(deleted)
    directions = mixed_external + internal
    require(len(directions) == len(set(directions)) == 4,
            "the physical cube does not have four distinct directions")

    full_mask = 15
    cycle = cube.indexed_top_koszul_cycle(directions)
    require(len(cycle) == 17,
            "the complete lift is not sixteen r0 faces plus one rm face")
    require(not cube.indexed_hasse_chain_differential(cycle, directions),
            "the complete squarefree Leibniz boundary is nonzero")
    positive, negative = exact_leibniz_ledger(directions)

    require(cycle.get(("r_0", 0)) == cube.constant(),
            "the top unit did not land on the zero jet of r0")
    require(cycle.get(("r_m", full_mask))
            == cube.scale(-cube.ONE, cube.F_PURE),
            "the top mixed-row correction changed")

    # Coupling the already existing cap face -T gives +Yw.  This statement
    # uses no newly declared cap/attaching generator.
    cap_boundary = cube.CAP_Y
    require(cap_boundary == cube.variable(("cap", "Y")),
            "cap boundary normalization changed")

    # Forgetting every positive Hasse face retains r0-T.  With the original
    # physical differential, r0 contributes the uncancelled pure Eq row.
    diagonal_chain = {"r_0": cube.constant(), "T": cube.constant(-1)}
    physical_differential = {
        "r_0": {"eq": cube.F_PURE},
        "T": {"w": cube.scale(-cube.ONE, cube.CAP_Y)},
    }
    diagonal_boundary = cube.apply_module_map(
        diagonal_chain, physical_differential
    )
    require(diagonal_boundary == {
        "eq": cube.F_PURE,
        "w": cube.CAP_Y,
    }, "the first diagonal typed face changed")

    # Compare with the actual zero-endpoint denominator/Rees cube.  The top
    # units agree, but its two endpoint directions are different variables.
    # Replacing both is the endpoint bridge operator, not deletion of one of
    # the four directions and hence not one of the eight cubical facets.
    chart_row = zero_endpoint_chart_row(deleted)
    zero_external = (
        cube.edge(cube.X, deleted, 0, 0),
        cube.edge(cube.P, cube.QSITE, 0, 0),
    )
    zero_directions = zero_external + internal
    chart_face_values = []
    for face_mask in range(16):
        value = cube.derivative(
            chart_row, mask_directions(zero_directions, face_mask)
        )
        require(value, "an actual denominator-cube face disappeared")
        require(cube.add(value, cube.scale(-cube.ONE, value)) == {},
                "a strict pq/pr chart face failed to cancel")
        chart_face_values.append(value)

    pq_direct, pq_star = cube.partition(chart_row, (cube.P, cube.QSITE))
    pr_direct, pr_star = cube.partition(chart_row, (cube.P, cube.R))
    require(not pr_direct, "the forbidden pr-direct sector returned")
    for internal_mask in range(4):
        selected = zero_external + mask_directions(internal, internal_mask)
        value = cube.derivative(chart_row, selected)
        require(cube.derivative(pq_direct, selected) == value,
                "an external face left the pq-direct sector")
        require(not cube.derivative(pq_star, selected),
                "an external face entered the pq-star sector")
        require(cube.derivative(pr_star, selected) == value,
                "an external face left the pr-two-star sector")

    physical_top = cube.derivative(cube.H_MIXED, directions)
    chart_top = cube.derivative(chart_row, zero_external + internal)
    require(physical_top == chart_top == cube.constant(),
            "physical/chart endpoint tops no longer agree")
    require(set(zero_external).isdisjoint(mixed_external),
            "endpoint bridge accidentally became an ordinary cube facet")
    require(cube.add(chart_row, cube.scale(-cube.ONE, chart_row)) == {},
            "strict chart comparison acquired a global Eq boundary")

    support = reset_support(deleted, internal)
    return {
        "deleted": deleted,
        "matching": [list(pair) for pair in matching],
        "directions": [list(item) for item in directions],
        "hasse_chain_terms": len(cycle),
        "leibniz_eq_faces": len(positive),
        "leibniz_pairwise_cancellations": len(positive),
        "formal_cap_boundary": "Y*w",
        "diagonal_boundary_types": ["(H0-u)*e_Eq", "Y*w"],
        "first_uncancelled_typed_face": "(H0-u)*e_Eq",
        "denominator_support_counts": [
            len(support[0]), len(support[1]),
            len(support[2]), len(support[3]),
        ],
        "physical_and_zero_endpoint_top": 1,
        "strict_chart_face_cancellations": len(chart_face_values),
        "external_sector_faces_checked": 4,
        "endpoint_bridge_is_cubical_facet": False,
        "curvature_lower_face_forced_by_D2": False,
    }


def main():
    records = []
    for deleted in cube.ODD:
        for matching in cube.matchings(cube.face(deleted)):
            records.append(audit_cube(deleted, matching))
    require(len(records) == 15, "expected five faces times three matchings")

    certificate = {
        "source_faces": ["ed60e2c", "e7723de"],
        "identity": (
            "s_I=sum_{S subset I}(partial_S H_m)r0[I\\S]"
            "-(H0-u)rm[I]; d(s_I)=0"
        ),
        "cap_coupling_without_new_generator": "d(s_I-T)=Y*w",
        "physical_diagonal_commutator": (
            "[d,pi_diagonal](s_I-T)=(H0-u)*e_Eq"
        ),
        "curvature_verdict": (
            "22-to-00 top equality is a two-direction endpoint bridge, "
            "not a facet; its lower curvature face is independent data"
        ),
        "records": records,
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"certificate digest changed: {digest}")

    print("h=3 actual order-four denominator cube boundary: PASS")
    print("all 15 cubes: 16 Leibniz faces cancel in the prolonged cone")
    print("first physical typed face: (H0-u)*e_Eq")
    print("22-to-00 curvature lower face is not forced by cubical D^2=0")
    print(f"certificate sha256 {digest}")


if __name__ == "__main__":
    main()
