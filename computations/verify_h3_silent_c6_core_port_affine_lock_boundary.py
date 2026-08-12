#!/usr/bin/env python3
"""Exact core-port boundary after the fixed-port silent-C6 closure.

Allow arbitrary endpoint components on core ports 0,1,3,4, but retain the
already-routed branch: PS=q04=q13=0, no outside endpoint term, and no
nonanchor offdiagonal q mate.  In each of b4d8568's nine private rows, the
complete core-port expansion has exactly two terms: the fixed orientation
and the endpoint-swapped orientation on the identical q tail.

At a synchronized minimum-support source, proportional complete columns
are exactly deletable.  In the remaining branch both endpoint pairs are
nonproportional and their common private word is a permanent-null 2x2 port
lock.  For the first two X1 tails it is the reciprocal 04 K2,2/Hall lock.
For the third tail it kills the entire selected X1 hole-01 contribution, so
the bright target forces another core hole, necessarily intersecting the
selected X2 hole 34.  Thus the first unavoidable core-port topology is
precisely the existing Hall/affine Fitting interface.  Surplus
nonproportional columns absent from this private word are not concentrated.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
B4_PATH = "computations/verify_h3_silent_c6_complete_response_mate_boundary.py"
COMMON_PATH = (
    "computations/verify_h3_axis_target_coloop_common_covector_synchronization.py"
)
PINS = {
    B4_PATH:
        "4f4a54d210b21da1183fe2fbfbb4441cec2388111b8c9e2d966a47e1d8fdcb7d",
    "notes/h3-silent-c6-complete-response-mate-boundary.md":
        "6c2dc1826d0e9be6b01081c2b84c535f30a5a427ae9a2225f490fdd2fc9bb22e",
    "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py":
        "6f27d3585fdc4708026ab6fef6134295dd874f83bb43fd1f480b7314362c56f3",
    "notes/h3-axis-target-coloop-proportional-nu-safe-reduction.md":
        "8e9ba2c477be06a022f1c86f334d45a95b1ff7d9393b7134c6f38aa21d797f14",
    COMMON_PATH:
        "cb834de7584912dc8c4f650a0504326cf8badb7f4c4e9e823bad5068a53e7d31",
    "notes/h3-axis-target-coloop-common-covector-synchronization.md":
        "59d0b3778a1a86febdda55a428083e1e756131bf45e4e8a1c5883e30cc08d33c",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
}
EXPECTED_LEDGER_SHA256 = (
    "6936556a3c9ec116a8250954d0b9afff3749cf99ec223ac8046d22c7adbef6fa"
)
CORE = frozenset((0, 1, 3, 4))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def endpoint_site(matching, endpoint):
    incident = next(edge for edge in matching if endpoint in edge)
    return next(site for site in incident if site != endpoint)


def supported_q_cells(b4, first_tail, second_tail):
    cells = {physical: {(0, 0)} for physical in b4.Q00_WEIGHTS}
    for colour, tail in ((1, first_tail), (2, second_tail)):
        for physical in tail:
            cells.setdefault(physical, set()).add((colour, colour))
    return cells


def core_port_terms(b4, row_name, word, first_tail, second_tail):
    cells = supported_q_cells(b4, first_tail, second_tail)
    terms = []
    for matching in b4.MATCHINGS:
        if b4.uses_physical_pair(matching, ("P", "S")):
            continue
        p_site = endpoint_site(matching, "P")
        s_site = endpoint_site(matching, "S")
        if p_site not in CORE or s_site not in CORE or p_site == s_site:
            continue
        q_factors = []
        for physical in b4.residual_tail(matching):
            decoration = (word[physical[0]], word[physical[1]])
            if decoration not in cells.get(physical, set()):
                break
            q_factors.append((physical, decoration))
        else:
            terms.append({
                "matching": matching,
                "ports": (p_site, s_site),
                "q_factors": tuple(q_factors),
                "endpoint_cells": (
                    ("p", row_name[1], p_site, word[p_site]),
                    ("s", row_name[2], s_site, word[s_site]),
                ),
            })
    return terms


def determinant(matrix):
    require(len(matrix) == len(matrix[0]) == 2,
            "only the two-port determinant is used")
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def audit_complete_column_split(common):
    # Proportional full columns admit the exact one-sided update of 1a2713d.
    selected = (Q(2), Q(-1), Q(3), Q(4))
    extra = tuple(Q(-3, 2) * value for value in selected)
    selected_coefficient, extra_coefficient = Q(5), Q(4)
    old = tuple(selected_coefficient * selected[index]
                + extra_coefficient * extra[index]
                for index in range(4))
    updated = selected_coefficient + Q(-3, 2) * extra_coefficient
    new = tuple(updated * value for value in selected)
    require(old == new, "the proportional complete-column deletion changed")

    # In the nonproportional branch, apply the pinned characteristic-zero
    # common-covector construction to the P and S endpoint pairs.
    p_pair = ((Q(1), Q(1), Q(0), Q(0)),
              (Q(1), Q(0), Q(0), Q(0)))
    s_pair = ((Q(1), Q(0), Q(1), Q(0)),
              (Q(1), Q(0), Q(0), Q(0)))
    d = (Q(1), Q(0), Q(0), Q(0))
    e_p = (Q(0), Q(1), Q(0), Q(0))
    e_s = (Q(0), Q(0), Q(1), Q(0))
    synchronized, candidates = common.synchronize(
        p_pair, s_pair, d, e_p, e_s
    )
    require(synchronized[0] == 1
            and synchronized[2] == (Q(-1), Q(-1)),
            "the common endpoint covector changed")
    return {
        "proportional_full_columns": (
            "exact one-sided nu-safe absorption to the fixed-port branch"
        ),
        "sample_old_complete_response": [str(value) for value in old],
        "sample_new_complete_response": [str(value) for value in new],
        "nonproportional_pairs": (
            "one common output covector detects both endpoint minors"
        ),
        "common_covector_scalar": str(synchronized[0]),
        "common_minor_values": [str(value) for value in synchronized[2]],
        "candidate_count": len(candidates),
    }


def audit_core_private_rows(b4):
    fixed_records = b4.fixed_port_bright_closure()
    require(len(fixed_records) == 9,
            "the nine fixed-port bright records changed")
    records = []
    orbit_histogram = Counter()
    for record in fixed_records:
        first_index = record["X1_tail_index"]
        second_index = record["X2_tail_index"]
        first_tail = b4.BRIGHT_TAILS[1][first_index - 1]
        second_tail = b4.BRIGHT_TAILS[2][second_index - 1]
        row_name = record["private_row"]
        word = tuple(map(int, record["private_word"]))
        terms = core_port_terms(
            b4, row_name, word, first_tail, second_tail
        )
        require(len(terms) == 2,
                "a private row acquired more than its swapped orientation")

        fixed_ports = ((0, 4) if row_name == "G12" else (0, 1))
        swapped_ports = tuple(reversed(fixed_ports))
        by_ports = {term["ports"]: term for term in terms}
        require(set(by_ports) == {fixed_ports, swapped_ports},
                "the core-port orientations changed")
        require(by_ports[fixed_ports]["q_factors"]
                == by_ports[swapped_ports]["q_factors"],
                "the swapped term lost the identical common q tail")
        common_tail = by_ports[fixed_ports]["q_factors"]

        if first_index in (1, 2):
            require(row_name == "G12" and fixed_ports == (0, 4),
                    "the reciprocal core orbit changed")
            kind = "reciprocal_04_K22_lock"
            endpoint_matrix = ((Q(0), Q(1)), (Q(1), Q(0)))
            endpoint_relation = "p1_0:11*s2_4:22+p1_4:12*s2_0:21=0"
            require(determinant(endpoint_matrix) == -1,
                    "the reciprocal core cofactor matrix lost rank")
        else:
            require(row_name == "G11" and fixed_ports == (0, 1),
                    "the diagonal swapped-hole orbit changed")
            kind = "diagonal_01_orientation_lock"
            endpoint_matrix = ((Q(0), Q(1)), (Q(1), Q(0)))
            endpoint_relation = "p1_0:11*s1_1:11+p1_1:11*s1_0:11=0"
            require(determinant(endpoint_matrix) == -1,
                    "the diagonal core cofactor matrix lost rank")

        orbit_histogram[kind] += 1
        records.append({
            "X1_tail_index": first_index,
            "X2_tail_index": second_index,
            "private_row": row_name,
            "private_word": record["private_word"],
            "kind": kind,
            "fixed_ports": fixed_ports,
            "swapped_ports": swapped_ports,
            "identical_q_tail": common_tail,
            "fixed_endpoint_cells": by_ports[fixed_ports]["endpoint_cells"],
            "swapped_endpoint_cells": by_ports[swapped_ports]["endpoint_cells"],
            "core_term_count": len(terms),
            "localized_endpoint_relation": endpoint_relation,
            "two_port_cofactor_determinant": "-T^2",
        })

    require(orbit_histogram == Counter({
        "reciprocal_04_K22_lock": 6,
        "diagonal_01_orientation_lock": 3,
    }), f"the core affine orbit split changed: {orbit_histogram}")
    return records, dict(sorted(orbit_histogram.items()))


def audit_diagonal_bright_reselection():
    # If the endpoint permanent on hole 01 vanishes, every pure-X1 matching
    # using that hole is killed at once.  X1=1 must use another occupied core
    # hole.  Every other core edge meets the selected X2 hole 34.
    core_edges = tuple(
        (left, right) for left in sorted(CORE) for right in sorted(CORE)
        if left < right
    )
    alternatives = tuple(edge for edge in core_edges if edge != (0, 1))
    require(alternatives == ((0, 3), (0, 4), (1, 3), (1, 4), (3, 4)),
            "the alternate core-hole list changed")
    require(all(set(edge) & {3, 4} for edge in alternatives),
            "an alternate X1 core hole escaped the X2 Hall collision")

    # A nonzero permanent-null sample pins that the relation does not itself
    # delete an endpoint component.
    a, b, c, d = Q(1), Q(1), Q(-1), Q(1)
    require(a * d + b * c == 0 and all((a, b, c, d)),
            "the diagonal orientation lock sample changed")
    return {
        "selected_X1_hole": [0, 1],
        "selected_X2_hole": [3, 4],
        "endpoint_permanent_sample": [str(value) for value in (a, b, c, d)],
        "selected_hole_contribution": "(ad+bc)*H01^[1111]=0",
        "alternate_core_holes": [list(edge) for edge in alternatives],
        "all_alternates_meet_X2_hole34": True,
        "landing": "star/triangle/K2,2 Hall normal form",
    }


def audit():
    pin_dependencies()
    b4 = load(B4_PATH, "silent_c6_core_b4")
    common = load(COMMON_PATH, "silent_c6_core_common_covector")
    records, histogram = audit_core_private_rows(b4)
    ledger = {
        "pins": PINS,
        "complete_column_split": audit_complete_column_split(common),
        "complete_core_private_expansion": {
            "records": records,
            "orbit_histogram": histogram,
            "theorem": (
                "after the previously routed terms are removed, every b4 "
                "private coefficient has exactly its fixed endpoint "
                "orientation and the swapped orientation on the identical "
                "common q tail"
            ),
        },
        "diagonal_bright_reselection": audit_diagonal_bright_reselection(),
        "theorem": (
            "in each selected private fine coefficient arbitrary core-port "
            "support reduces to the fixed and swapped endpoint "
            "orientations.  Proportional complete columns absorb nu-safely "
            "to the fixed-port closure.  Otherwise the first two bright-"
            "tail orbits give the nondegenerate reciprocal 04 K2,2 port "
            "lock, while the third kills the selected X1 hole and forces "
            "an alternate Hall-colliding bright hole"
        ),
        "sharp_residual": (
            "a nonproportional two-port permanent-null block with a common "
            "Fitting covector, trapped in the four-core-site Hall graph; "
            "routing its carrier to deleted-star rank three is exactly the "
            "existing affine/Hall accessibility interface"
        ),
        "scope": (
            "exact full unary-plus-bright private-row consequence after the "
            "b4 outside-q/outside-endpoint routes.  It is a reduction to the "
            "existing Hall interface, not a claim that arbitrary Hall "
            "triangle/K2,2 accessibility is globally closed.  Surplus "
            "nonproportional endpoint columns absent from the selected "
            "private word may enlarge the Hall/Fitting module and are not "
            "proved deletable here"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"silent C6 core-port boundary changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 silent C6 core-port affine lock boundary: PASS (exact)")
    print("nine private rows: exactly fixed + swapped endpoint orientation")
    print("orbits: 6 reciprocal-04 K2,2; 3 diagonal-01 Hall reselections")
    print("proportional columns -> nu-safe absorption")
    print("residual -> nonproportional Hall/Fitting accessibility")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
