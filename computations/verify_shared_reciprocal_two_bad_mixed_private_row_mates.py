#!/usr/bin/env python3
"""Classify the minimal simultaneous mates of the two private X_c rows.

The rank-13 second-kernel packet has two private K2 words, CCAT and TACC.
Each has exactly two alternate physical matchings, hence four simultaneous
mate types.  After imposing the two cancellation products, every type has
a 14x14 cofactor-map minor equal to +/-16/p^2.  Thus the second kernel is
killed uniformly; only the old tilted kernel remains and X_t is still
absent from the complete kernel-product span.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path

import sympy as sp

import verify_shared_reciprocal_two_bad_mixed_bright_completion as chart
import verify_shared_reciprocal_two_bad_mixed_second_kernel_gate as gate


ROOT = Path(__file__).resolve().parents[1]
PINNED_SECOND_KERNEL_SHA256 = (
    "6936c030433b3ded42fc07dd830b0fbcb92e84373e87d5eafac90da062d9c3e3"
)
EXPECTED_DIGEST = "1eb4972f703b3567d62621f82c87a10b87f7200837306fa43e52fa0802b771fe"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_mixed_second_kernel_gate.py"
    )
    require(sha256(path.read_bytes()).hexdigest()
            == PINNED_SECOND_KERNEL_SHA256,
            "the second-kernel dependency changed")


CC_ROUTES = {
    "03/14": (((0, 3), chart.C, chart.A),
              ((1, 4), chart.C, chart.T)),
    "04/13": (((0, 4), chart.C, chart.T),
              ((1, 3), chart.C, chart.A)),
}
TC_ROUTES = {
    "03/14": (((0, 3), chart.T, chart.C),
              ((1, 4), chart.A, chart.C)),
    "04/13": (((0, 4), chart.T, chart.C),
              ((1, 3), chart.A, chart.C)),
}


def compatible_cells(word):
    vertices = tuple(sorted(word))
    answer = []
    for matching in chart.perfect_matchings(vertices):
        answer.append(tuple(
            (tuple(sorted(edge)), word[edge[0]], word[edge[1]])
            for edge in matching
        ))
    return tuple(answer)


def audit_route_classification():
    cc_word = {0: chart.C, 1: chart.C, 3: chart.A, 4: chart.T}
    tc_word = {0: chart.T, 1: chart.A, 3: chart.C, 4: chart.C}
    cc_selected = (((0, 1), chart.C, chart.C),
                   ((3, 4), chart.A, chart.T))
    tc_selected = (((0, 1), chart.T, chart.A),
                   ((3, 4), chart.C, chart.C))
    cc_terms = compatible_cells(cc_word)
    tc_terms = compatible_cells(tc_word)
    require(cc_terms[0] == cc_selected and tc_terms[0] == tc_selected,
            "the selected private matching changed")
    require(set(cc_terms[1:]) == set(CC_ROUTES.values()),
            "the CCAT mate routes changed")
    require(set(tc_terms[1:]) == set(TC_ROUTES.values()),
            "the TACC mate routes changed")
    types = tuple(itertools.product(CC_ROUTES, TC_ROUTES))
    require(len(types) == 4, "the simultaneous mate-type count changed")
    return {
        "CCAT_alternates": {
            name: [[list(edge), left, right] for edge, left, right in cells]
            for name, cells in CC_ROUTES.items()
        },
        "TACC_alternates": {
            name: [[list(edge), left, right] for edge, left, right in cells]
            for name, cells in TC_ROUTES.items()
        },
        "simultaneous_types": [list(kind) for kind in types],
    }


def base_packet():
    return gate.parameter_cells(
        z=1, y=-1, b=1, w=1, v=-1, r=1, s=-2
    )


def add_mates(cc_kind, tc_kind, x, p):
    cells = base_packet()
    cc_values = (x, 2 / x)
    tc_values = (p, -1 / p)
    for key, value in zip(CC_ROUTES[cc_kind], cc_values):
        cells[key] = value
    for key, value in zip(TC_ROUTES[tc_kind], tc_values):
        cells[key] = value
    return cells


def sparse_tensor(vector):
    return {
        chart.WORDS[index]: sp.factor(value)
        for index, value in enumerate(vector) if value != 0
    }


def audit_type(cc_kind, tc_kind):
    x, p = sp.symbols("x p", nonzero=True)
    cells = add_mates(cc_kind, tc_kind, x, p)
    phi, _cofactors = chart.phi_matrix(cells)

    u = sp.zeros(len(chart.LABELS), 1)
    u[chart.LABELS.index((0, chart.T))] = 1
    u[chart.LABELS.index((1, chart.A))] = -1
    v = sp.zeros(len(chart.LABELS), 1)
    v[chart.LABELS.index((3, chart.A))] = 1
    v[chart.LABELS.index((4, chart.T))] = -1
    require(phi * u == sp.zeros(len(chart.WORDS), 1),
            "a minimal mate broke the old tilted kernel")
    v_residual = sparse_tensor(phi * v)
    require(len(v_residual) == 4,
            f"the second-kernel residual count changed: {v_residual}")
    require(all(value != 0 for value in v_residual.values()),
            "a localized mate residual vanished")

    # U supplies one relation, so rank(Phi)<=14.  Delete its duplicate
    # column and find a 14-row pivot chart at x=p=1, then evaluate the same
    # minor symbolically over Q(x,p).
    selected_columns = [
        index for index, label in enumerate(chart.LABELS)
        if label != (1, chart.A)
    ]
    matrix = phi[:, selected_columns]
    numeric = matrix.subs({x: 1, p: 1})
    pivot_rows = tuple(numeric.T.rref()[1])
    require(len(pivot_rows) == 14,
            "a simultaneous mate failed to restore rank 14")
    minor = matrix.extract(pivot_rows, tuple(range(14)))
    determinant = sp.factor(minor.det())
    sign = 1 if cc_kind == "04/13" else -1
    require(determinant == sign * 16 / p ** 2,
            f"the repair-invariant minor changed: {determinant}")

    target_index = chart.WORDS.index((chart.T,) * 5)
    require(all(phi[target_index, column] == 0
                for column in range(phi.cols)),
            "a minimal mate put X_t into im(Phi)")
    target_products = []
    for p_index in range(len(chart.LABELS)):
        controller = sp.zeros(len(chart.LABELS), 1)
        controller[p_index] = 1
        product = chart.kernel_product(
            cells, chart.vector_as_rows(controller), chart.vector_as_rows(u),
            chart.vector_as_rows(u))
        target_products.append(sp.factor(product[target_index]))
    require(target_products == [0] * len(chart.LABELS),
            "the surviving one-kernel products acquired X_t")

    numeric_audit = chart.full_audit({
        key: sp.factor(value.subs({x: 1, p: 1}))
        if hasattr(value, "subs") else value
        for key, value in cells.items()
    })
    expected_summary = (14, 1, 16, 0, (False, False, False), False)
    require(numeric_audit["summary"] == expected_summary,
            f"the numerical mate replay changed: {numeric_audit['summary']}")
    return {
        "type": [cc_kind, tc_kind],
        "second_kernel_residual": {
            str(word): str(value) for word, value in v_residual.items()
        },
        "pivot_rows": [list(chart.WORDS[row]) for row in pivot_rows],
        "minor": str(determinant),
        "unit_summary": list(expected_summary[:4]),
    }


def main():
    pin_dependency()
    routes = audit_route_classification()
    records = [
        audit_type(cc_kind, tc_kind)
        for cc_kind, tc_kind in itertools.product(CC_ROUTES, TC_ROUTES)
    ]
    ledger = {
        "pinned_second_kernel_sha256": PINNED_SECOND_KERNEL_SHA256,
        "route_classification": routes,
        "type_records": records,
        "repair_invariant": (
            "after localizing the two mate products, every simultaneous "
            "minimal repair has rank(Phi)=14 and ker(Phi)=<U>"
        ),
        "verdict": (
            "all four minimal mate types kill the second kernel and still "
            "exclude X_t from the complete surviving kernel-product span"
        ),
        "scope": (
            "minimal two-cell mate for each of the two private rows in the "
            "canonical rank-13 packet, over characteristic zero"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"private-row mate ledger changed: {digest}")

    print("shared reciprocal two-bad private-row mates: PASS")
    print("simultaneous mate types: 4")
    print("all localized minors: +/-16/p^2")
    print("all types: rank 14, one kernel, X_t absent")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
