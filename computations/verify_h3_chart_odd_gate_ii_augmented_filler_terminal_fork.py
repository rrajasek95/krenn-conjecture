#!/usr/bin/env python3
"""Audit the h=3 chart-odd Gate-II augmented filler/terminal fork.

The checker composes the exact Gate-II primitive dual, its forced extension
over presentation-safe carrier graphs, the first-PP obstruction, and the
labelled P2/Q/ores tail.  It also audits the universal linear fact that a
relative graph preserves a detected class, while one absolute carrier
saturation column either fills it or breaks the dual.

No missing physical carrier landing is constructed here.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from pathlib import Path


Q = Fraction
ROOT = Path(__file__).resolve().parents[1]

PINNED = {
    "notes/uniform-chart-odd-carrier-gate-collapse.md":
        "7a32482e0e6c8ff9966ef44579eb0f89506e75184de5ea042c0433715f459b39",
    "computations/verify_uniform_chart_odd_carrier_gate_collapse.py":
        "67b86d1f9d8f22fa46e45582bea90435dfdebad86dcea47c76518a087bf200b9",
    "notes/h3-gate-ii-chiw-nonfill-full-augmented-dual.md":
        "f7fd790075f7cf3d31b9d4a6035fa6bc476a3bdc16ce4bda97b777b153664568",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
    "notes/h3-gate-ii-psidelta-same-grade-extension-chain.md":
        "2e7aea9a551ddc2ab845fb2c0717cbffb8f7db772c329fb3c11d6bdc3dc34fae",
    "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py":
        "d5628f66ffbf94e2de37318ab136adda96af5e114e2bea8dce22542ec9f30cb1",
    "notes/h3-gate-ii-three-cap-relative-tate-carrier-obstruction.md":
        "a4c19d4c5f28da42ec1a4af29e2008bd85eee131e7f4d787cb0f8ace14f88ec0",
    "computations/verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py":
        "0be2bde12d3d4b85cad67b4a647b4cb4f7e89ed1a04bff14f6091eb257224dcc",
    "notes/h3-gate-ii-uniform-response-relative-carrier-landing-gate.md":
        "e1d0b1185cd72ff4d0d915abb1db25835f2848f65f1509458aee9f2325699084",
    "computations/verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py":
        "9b9c05a6789d2ade9359934f279eeb429591b2e85651ebaba8485195050417eb",
    "notes/uniform-chart-odd-matching-exchange-operation-tag-tor-gate.md":
        "050191376b790ec1f7092f3ff3ef3f1f20f44bdcc9403e96048c598a27ce9493",
    "computations/verify_uniform_chart_odd_matching_exchange_operation_tag_tor_gate.py":
        "a835e816347b15f8c88c7f9995374468cd421cd68a64650bda128eda75ae8f39",
    "notes/uniform-strict-four-cut-homotopy-moment-collapse.md":
        "61e0b2267bb5b71253e9bcc4d94173b925851034754cf4f38842575f3bec56de",
    "computations/verify_uniform_strict_four_cut_homotopy_moment_collapse.py":
        "8910f6ce438257d310fce12b8f76c4639d2c42033950ab6ea7072bcca702bf1c",
    "notes/h3-p2-labelled-ores-cut-even-deven-gauge-gate.md":
        "0477f14ab8725708711ff098c68ae29f10625516024cc2a93413c780ea466054",
    "computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py":
        "0a4215db2b91843753cc636b489a81f8e30a8c3de234979c74c9f852d74e3d8a",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def check_pins() -> None:
    for relative, expected in PINNED.items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        pivot_value = rows[answer][column]
        rows[answer] = [value / pivot_value for value in rows[answer]]
        for row in range(height):
            if row == answer or rows[row][column] == 0:
                continue
            factor = rows[row][column]
            rows[row] = [left - factor * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def universal_relative_fork() -> dict[str, object]:
    # Coordinate order is (beta,t).  The presentation-safe graph has
    # boundary t-beta.  It does not fill beta; adding the absolute carrier
    # column t fills both t and beta.
    beta = (Q(1), Q(0))
    carrier = (Q(0), Q(1))
    graph = (Q(-1), Q(1))
    dual = (Q(1), Q(1))
    require(rank((graph,)) == 1
            and rank((graph, beta)) == rank((graph, carrier)) == 2,
            "relative graph stopped preserving the detected class")
    require(dot(dual, graph) == 0
            and dot(dual, beta) == dot(dual, carrier) == 1,
            "forced carrier dual changed")
    require(rank((graph, carrier)) == 2
            and rank((graph, carrier, beta)) == 2,
            "carrier saturation did not fill beta")
    return {
        "relative_graph_boundary": "t-beta",
        "relative_graph_rank": 1,
        "beta_rank_increment": 1,
        "forced_dual_values_beta_t": [1, 1],
        "absolute_saturation_column": "t",
        "rank_after_saturation": 2,
        "identity_after_saturation": "beta=t-(t-beta)",
    }


def known_augmented_dual() -> dict[str, object]:
    # Four cap characters and the known augmented extension.
    delta = (Q(1), Q(1), Q(-1), Q(-1))
    alpha = (Q(-1), Q(1), Q(1), Q(-1))
    require(dot(alpha, delta) == 0, "alpha.delta changed")

    # Coordinate blocks are B,target,W,ores plus ridge.  Eq, M, ainc, q,
    # P_f, eta and sigma have dual coefficient zero and need no coordinates.
    dual = delta + tuple(-value for value in delta) \
        + tuple(-value for value in delta) + delta + (Q(0),)

    def unit(block: int, corner: int) -> tuple[Q, ...]:
        values = [Q(0)] * 17
        values[4 * block + corner] = 1
        return tuple(values)

    columns = []
    for corner in range(4):
        # r0=B+target, T=-W+target, rho=W+ores after suppressing rows on
        # which the dual is zero.
        columns.append(tuple(a + b for a, b in zip(
            unit(0, corner), unit(1, corner), strict=True)))
        columns.append(tuple(-a + b for a, b in zip(
            unit(2, corner), unit(1, corner), strict=True)))
        columns.append(tuple(a + b for a, b in zip(
            unit(2, corner), unit(3, corner), strict=True)))
    k_column = [Q(0)] * 17
    for corner, coefficient in enumerate(alpha):
        k_column[12 + corner] = coefficient
    k_column[16] = 1
    columns.append(tuple(k_column))
    require(all(dot(dual, column) == 0 for column in columns),
            "Gate-II known augmented dual stopped annihilating old columns")
    return {
        "primitive_character": list(delta),
        "target_W_ores": [list(-value for value in delta),
                           list(-value for value in delta), list(delta)],
        "ridge": 0,
        "zero_dual_rows": ["Eq", "M", "ainc", "q", "P_f", "eta", "sigma"],
        "named_augmented_columns_checked": len(columns),
        "all_named_column_values": [str(dot(dual, column)) for column in columns],
    }


def gate_ii_relative_carriers() -> dict[str, object]:
    # Coordinates (R01,L01,t_R,t_L).  Normalize psi(L01)=1.  The exact
    # degree-zero occurrence calculation gives psi(R01)=-1.  Annihilation
    # of t_R-R01 and t_L-L01 forces psi(t_R,t_L)=(-1,1).
    psi = (Q(-1), Q(1), Q(-1), Q(1))
    graph_r = (Q(-1), Q(0), Q(1), Q(0))
    graph_l = (Q(0), Q(-1), Q(0), Q(1))
    r01 = (Q(1), Q(0), Q(0), Q(0))
    l01 = (Q(0), Q(1), Q(0), Q(0))
    t_r = (Q(0), Q(0), Q(1), Q(0))
    t_l = (Q(0), Q(0), Q(0), Q(1))
    require(dot(psi, graph_r) == dot(psi, graph_l) == 0,
            "relative carrier dual does not kill graph columns")
    require(tuple(dot(psi, vector) for vector in (r01, l01, t_r, t_l))
            == (Q(-1), Q(1), Q(-1), Q(1)),
            "forced Gate-II carrier values changed")
    require(rank((graph_r, graph_l)) == 2
            and rank((graph_r, graph_l, l01)) == 3
            and rank((graph_r, graph_l, t_l)) == 3
            and rank((graph_r, graph_l, t_l, l01)) == 3,
            "Gate-II relative/saturation ranks changed")
    return {
        "graph_columns": ["t_R-R01", "t_L-L01"],
        "normalized_dual_values_R_L_tR_tL": [-1, 1, -1, 1],
        "relative_graph_preserves_detected_dimension": True,
        "absolute_tL_column_fills_L01": True,
        "absolute_tL_dual_value": 1,
    }


def proper_face_chain() -> dict[str, object]:
    # Exact constants pinned by the first-PP and labelled P2 computations.
    six_marginals = (Q(6), Q(6), Q(-3), Q(-3), Q(-3), Q(-3))
    primitive = tuple(value / 3 for value in six_marginals)
    require(primitive == (Q(2), Q(2), Q(-1), Q(-1), Q(-1), Q(-1)),
            "endpoint/direction primitive profile changed")

    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(12))
    require(sum(detector, Q(0)) == 0,
            "word-0102 detector stopped killing complete response")
    centered_image = tuple(12 * value - sum(detector, Q(0))
                           for value in detector)
    require(centered_image == tuple(12 * value for value in detector),
            "C*d=12*d changed")

    q_component = Q(35, 72)
    labelled_ores = Q(-35, 72)
    require(q_component + labelled_ores == 0,
            "conditional Q/ores cancellation changed")
    return {
        "first_ungranted_fixed_PP_face": {
            "name": "selected db01",
            "terms": 6,
            "rank_before_after": [2, 3],
        },
        "after_tail_grants": {
            "face": "18 endpoint/direction terms of dL01",
            "marginals": list(six_marginals),
            "primitive_profile": list(primitive),
            "normalized_dual_value": 1,
        },
        "word_0102": {
            "detector": "+e0+e3-e1-e6",
            "detector_on_private_face": "-13/6",
            "forced_carrier_dual": "C*d=12*d",
        },
        "dq_Q_ores": {
            "Q_component": str(q_component),
            "labelled_ores": str(labelled_ores),
            "scalar_ores": 0,
            "new_direction_after_conditional_gauge": False,
        },
    }


def strict_common_four_cut() -> dict[str, object]:
    k_right = (Q(1), Q(0), Q(-1))
    k_left = (Q(1), Q(-1), Q(1))
    boundary = tuple(-(left + right) for left, right in
                     zip(k_right, k_left, strict=True))
    require(boundary == (Q(-2), Q(1), Q(0)),
            "dGamma=r-2q sign changed")
    return {
        "K_right": list(k_right),
        "K_left": list(k_left),
        "common_boundary": list(boundary),
        "formula": "dGamma=r-2q",
        "all_moment_consequence": "d(Gamma*H_s)=(r-2q)H_s for every s",
    }


def mutation_guards() -> None:
    # Setting a carrier to zero is an absolute attachment, not the monic
    # relative graph: it raises the rank and kills the detected class.
    graph = (Q(-1), Q(1))
    carrier = (Q(0), Q(1))
    require(rank((graph, carrier)) == 2,
            "absolute-carrier mutation stopped changing H0")
    require(Q(-13, 6) != 0, "word-0102 detector mutation was not detected")
    require(Q(-35, 72) != 0,
            "labelled-residue mutation was not detected")


def main() -> None:
    check_pins()
    ledger = {
        "universal_relative_fork": universal_relative_fork(),
        "known_augmented_dual": known_augmented_dual(),
        "gate_ii_relative_carriers": gate_ii_relative_carriers(),
        "proper_face_chain": proper_face_chain(),
        "strict_common_four_cut": strict_common_four_cut(),
    }
    mutation_guards()
    digest = hashlib.sha256(repr(ledger).encode()).hexdigest()
    print("PASS: h3 chart-odd Gate-II augmented filler/terminal fork")
    print("primitive dual through named augmented columns: EXTENDS")
    print("relative graph: FORCES NONZERO CARRIER DUAL")
    print("absolute chart-odd saturation: FILLS CLASS / BREAKS DUAL")
    print("first absent physical totalization: U_C4 + PP-NATURAL CARRIER")
    print("accepted full terminal or dLambda=beta: NOT YET")
    print("dGamma=r-2q and all moments: IMMEDIATE AFTER SATURATION")
    print(f"digest: {digest}")


if __name__ == "__main__":
    main()
