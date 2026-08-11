#!/usr/bin/env python3
"""Target-augmented private-site identity and active-minor dichotomy.

For a pure-a target word and the mixed word obtained by changing only site v
from a to b, the private-site identity has an inhomogeneous term.  If the
mixed row contains a nonzero reference cell A_vu[b,a], exactness gives

    sum_s Delta_us C_s = -A_vu[b,a].

Consequently some determinant/cofactor product is nonzero.  Thus every
off-diagonal endpoint or direct cell enters the active determinant branch;
cofactor-invisible rank minors can survive only when they compare differently
coloured neighbour ports and hence are not minors of one fixed word pair.

The checker verifies the polynomial identity through N=10, audits all six
ternary off-diagonal cell types, and checks that the exact counterguard from
fb8d482 escapes precisely through the untyped diagonal-port case.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_hafnian_private_site_matching_bijection_lemma.py":
        "310167f3f51cdbf7619497662b29b267f2d34de4c7e67c00110dba55d4c77efc",
    "computations/verify_n8_one_bad_endpoint_minor_c4_counterguard.py":
        "09deff150677bfa67f0109cb3f961d840bfc4856a759f3f8d18a99d24038b5a6",
}
EXPECTED_LEDGER_SHA256 = (
    "279a7b150da2571461ae438256bd70b7f12b8a11f183de074401cef69151dae4"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def target_augmented_identity(private, vertex_count):
    vertices = tuple(range(vertex_count))
    changed_site = vertex_count - 1
    reference = 0
    pure = private.symbolic_tail(vertices, changed_site, 0)
    mixed = private.symbolic_tail(vertices, changed_site, 1)
    one = Counter({(): Fraction(1)})
    g_pure = private.add((pure, 1), (one, -1))
    g_mixed = mixed
    p_reference = private.variable(private.incident_name(0, reference))
    q_reference = private.variable(private.incident_name(1, reference))
    left = private.add(
        (private.multiply(p_reference, g_mixed), 1),
        (private.multiply(q_reference, g_pure), -1),
    )
    right = q_reference
    active_terms = 0
    for neighbour in vertices:
        if neighbour in (changed_site, reference):
            continue
        determinant = private.add(
            (private.multiply(
                p_reference,
                private.variable(private.incident_name(1, neighbour))), 1),
            (private.multiply(
                q_reference,
                private.variable(private.incident_name(0, neighbour))), -1),
        )
        product = private.multiply(
            determinant,
            private.common_cofactor(vertices, changed_site, neighbour),
        )
        right = private.add((right, 1), (product, 1))
        active_terms += len(product)
    require(left == right,
            f"the target-augmented identity failed at N={vertex_count}")

    # The equality is source-provenant: after setting both source generators
    # to zero, the determinant/cofactor sum is exactly -q_reference.  Hence
    # localizing q_reference excludes the branch in which all those products
    # vanish.  This conclusion is the displayed identity, not a support-SAT
    # implication or an evaluation at a generic point.
    return {
        "vertices": vertex_count,
        "perfect_matchings_per_row": len(pure),
        "alternate_neighbours": max(vertex_count - 2, 0),
        "expanded_determinant_cofactor_monomials": active_terms,
        "source_identity": (
            "p_u*G_mixed-q_u*G_pure="
            "q_u+sum_s (p_u*q_s-q_u*p_s)*C_s"
        ),
        "exact_source_consequence": "sum_s Delta_us*C_s=-q_u",
    }


def ternary_typing_audit():
    colours = tuple(range(3))
    typed = []
    for pure_colour in colours:
        for mixed_colour in colours:
            if pure_colour == mixed_colour:
                continue
            typed.append({
                "pure_word": str(pure_colour) + "..." + str(pure_colour),
                "mixed_site_colour": mixed_colour,
                "reference_cell_type": [mixed_colour, pure_colour],
                "pure_incident_type": [pure_colour, pure_colour],
                "mixed_incident_type": [mixed_colour, pure_colour],
            })
    require(len(typed) == 6, "the ternary off-diagonal type count changed")
    require({tuple(record["reference_cell_type"]) for record in typed}
            == {(row, column) for row in colours for column in colours
                if row != column},
            "the target-augmented word pairs missed an off-diagonal type")

    # A determinant between A_vu[a,a] and A_vs[b,b] uses neighbour colours
    # a and b at two different sites.  No pair of full words differing only
    # at v can select both ports: the remaining word is common, and therefore
    # fixes one colour at each neighbour.  Such a cross-colour rank minor is
    # outside the private-site identity rather than a vanishing instance of
    # it.
    diagonal_cross_types = [
        [[left, left], [right, right]]
        for left in colours for right in range(left + 1, 3)
    ]
    require(len(diagonal_cross_types) == 3,
            "the diagonal cross-colour minor type count changed")
    return {
        "off_diagonal_reference_types": typed,
        "off_diagonal_types_covered": 6,
        "diagonal_cross_colour_minor_types": diagonal_cross_types,
        "typing_boundary": (
            "a single word pair fixes the neighbour colour at every port; "
            "minors comparing (a,a) with (b,b) for a!=b are not Delta_us "
            "in one target-augmented identity"
        ),
    }


def counterguard_scope_audit(guard):
    old = guard.load_guard()
    _q_cells, stars, blocks = guard.source_packet(old)
    endpoint_cells = {
        "P": [], "Q": [],
    }
    for endpoint, label in ((guard.P_ENDPOINT, "P"),
                            (guard.Q_ENDPOINT, "Q")):
        for other in guard.SITES:
            if other == endpoint:
                continue
            for row in guard.COLOURS:
                for column in guard.COLOURS:
                    value = blocks.get(
                        old.source_cell(endpoint, other, row, column), 0
                    )
                    if value:
                        endpoint_cells[label].append(
                            [other, row, column, str(value)]
                        )
    require(endpoint_cells == {
        "P": [[0, 1, 1, "1"], [2, 2, 2, "1"], [5, 1, 1, "1"]],
        "Q": [[1, 1, 1, "1"], [3, 2, 2, "1"]],
    }, f"the fb8 endpoint support changed: {endpoint_cells}")
    require(all(row == column
                for cells in endpoint_cells.values()
                for _site, row, column, _value in cells),
            "the fb8 guard acquired an off-diagonal endpoint cell")

    old_result = old.exact_response_guard()
    require(old_result["response_rows"] == {
        "11": "X1", "12": "0", "21": "0", "22": "X2"
    }, "the four-response guard changed")
    require(old_result["q_cubed"] == "0",
            "the guard acquired the missing unary target")
    return {
        "endpoint_cells": endpoint_cells,
        "all_endpoint_cells_diagonal": True,
        "rank_two_minors_from_fb8": 3,
        "typed_off_diagonal_reference_cells": 0,
        "why_fb8_is_not_a_counterexample": (
            "its nonzero rank minors compare differently coloured diagonal "
            "ports, and it still fails q^[3]=X0"
        ),
    }


def main():
    private = load(
        "computations/verify_hafnian_private_site_matching_bijection_lemma.py",
        "private_site_active_minor_dependency",
    )
    guard = load(
        "computations/verify_n8_one_bad_endpoint_minor_c4_counterguard.py",
        "endpoint_minor_guard_dependency",
    )
    identities = [target_augmented_identity(private, size)
                  for size in (2, 4, 6, 8, 10)]
    typing = ternary_typing_audit()
    old_scope = counterguard_scope_audit(guard)

    ledger = {
        "dependencies": PINS,
        "target_augmented_identity_checks": identities,
        "ternary_endpoint_typing": typing,
        "fb8_scope_audit": old_scope,
        "theorem": (
            "in any exact ternary GHZ source at any even order, every "
            "nonzero off-diagonal incident cell A_vu[b,a], b!=a, forces "
            "sum_s Delta_us*C_s=-A_vu[b,a], so at least one literal "
            "determinant/cofactor product is nonzero"
        ),
        "source_valid_dichotomy": (
            "off-diagonal endpoint/direct support enters the active "
            "determinant-cofactor branch; otherwise every endpoint row is "
            "axis-purified, with row a supported only in neighbour colour a"
        ),
        "remaining_gate": (
            "the identity does not turn an active determinant into a "
            "doubly-good curved OO pair.  In the axis-purified branch it also "
            "does not concentrate a multisite diagonal star to one site; "
            "that is the remaining minimum-support/common-q carrier-exchange "
            "problem"
        ),
        "scope": (
            "ordinary source polynomial identity over every commutative "
            "ring; the nonvanishing conclusion is over a field or after "
            "localizing the named off-diagonal source cell"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"target-augmented active-minor ledger changed: {digest}")

    print("uniform target-augmented private-site active-minor lemma: PASS")
    print("symbolic source identities checked at N=2,4,6,8,10")
    print("ternary off-diagonal endpoint/direct cell types covered: 6/6")
    print("fb8 rank-two escape: diagonal cross-colour minors only")
    print("remaining gate: axis-purified multisite concentration / OO upgrade")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
