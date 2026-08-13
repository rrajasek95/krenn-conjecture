#!/usr/bin/env python3
"""Promote an o2 output dual through the known cap/Cartan packet.

Let psi be a local output covector detecting the second Hasse obstruction
o2=[F_[2](xi)] in coker(A).  On the four literal cap corners write
mu_j=psi(B_j).  The old r0,T,rho columns and the physical Cartan K have
signatures

    r0_j = B_j + Eq_j + target_j - ainc,
    T_j  = -W_j + target_j,
    rho_j= W_j + ores_j,
    K    = sum_j alpha_j ores_j + ridge,

where alpha=(-1,1,1,-1), physical q is zero, and ``ridge`` denotes one
primitive nonzero coordinate of the known eta/sigma ridge.  Then psi has
the explicit augmented extension

    target_j=-mu_j, W_j=-mu_j, ores_j=mu_j,
    ridge=-sum_j alpha_j mu_j,

with q=ainc=Eq=0.  It annihilates every r0,T,rho,K column.  In particular,
the first literal stress column M_v=-O_alpha+K is not an obstruction.

For an exhaustive same-grade physical map J, ordinary exact duality then
gives the desired no-third-branch statement: either the pure local column
i(o2) is in im(J), yielding a protected-zero physical relative filler, or
an augmented covector annihilates J and detects i(o2).  The remaining input
is the source-labelled word/fine/repeated-grade placement of o2 in that J.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_occurrence_kernel_integrability_terminal_gate.py":
        "40a3a5875951b2d48aeda4ca58ea25029bb12d7195988c057f7c3590ec10039c",
    "notes/h3-occurrence-kernel-integrability-terminal-gate.md":
        "62210dd5971832b3b7b2227f56fe15dd54adc2492c834a4498a0d455d4ce94c6",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "notes/h3-literal-mv-cap-cartan-composition.md":
        "1f1a3596bcbbabe8756ce3097a21bfba38ccdf9474352ec73e17d55f524d9cc1",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "notes/h3-first-flat-physical-anchor-six-term-separator.md":
        "73d389a492b26c40ab27b0ed788c43c04a1e58a1abae94800916667aa6150b7f",
    "computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py":
        "a51b8f091a25624d17443c70ac70b60eb257c8b11dafb0b9ad3f17962dc07390",
    "notes/h3-trapped-hessian-to-six-term-endpoint-polarization-gate.md":
        "45d4d6604a58da20bec8aa87cb9522b658e2454a939533075d6e8d607ed895b8",
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
    "notes/h3-six-term-exhaustive-relative-extension-alternative.md":
        "98d95662d6adcf4684d6e15e60193369564e1d45ed0db19f822ce2a2add79977",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
    "computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py":
        "f35618988f591a28fd2a6574977c058aa2bec83a2cacfeb9e7567873e0b61d1c",
    "notes/h3-coloop-two-occurrence-complete-response-first-mixed-unary-gate.md":
        "94ffe3523f27aebb1064f2778b9a2a6fe99835ad98fc59b6a28dd57b6d9e9fa6",
}
EXPECTED_LEDGER_SHA256 = "1b7c2bcd9d381196c33fd10ee0f0cb26870b6c9a2e03549cb30616b40669c16e"

ALPHA = (Q(-1), Q(1), Q(1), Q(-1))
LABELS = (
    *(f"B{j}" for j in range(4)),
    *(f"Eq{j}" for j in range(4)),
    "q", "ainc",
    *(f"target{j}" for j in range(4)),
    *(f"W{j}" for j in range(4)),
    *(f"ores{j}" for j in range(4)),
    "ridge",
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def vector(**entries: int | Q) -> tuple[Q, ...]:
    unknown = set(entries) - set(LABELS)
    require(not unknown, ("unknown rows", sorted(unknown)))
    return tuple(Q(entries.get(label, 0)) for label in LABELS)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(value) for value in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, value: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in value)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(rows: tuple[tuple[Q, ...], ...]) -> int:
    if not rows:
        return 0
    work = [list(map(Q, row)) for row in rows]
    width = len(work[0])
    require(all(len(row) == width for row in work), "rank width")
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def nullspace(rows: tuple[tuple[Q, ...], ...], width: int
              ) -> tuple[tuple[Q, ...], ...]:
    if not rows:
        return tuple(tuple(Q(i == j) for i in range(width))
                     for j in range(width))
    work = [list(map(Q, row)) for row in rows]
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
    free = tuple(column for column in range(width) if column not in pivots)
    basis = []
    for column in free:
        value = [Q(0)] * width
        value[column] = Q(1)
        for row, pivot in enumerate(pivots):
            value[pivot] = -work[row][column]
        basis.append(tuple(value))
    return tuple(basis)


def cap_cartan_columns() -> tuple[tuple[str, tuple[Q, ...]], ...]:
    columns = []
    for corner in range(4):
        columns.extend((
            (f"r0_{corner}", vector(**{
                f"B{corner}": 1, f"Eq{corner}": 1,
                f"target{corner}": 1, "ainc": -1,
            })),
            (f"T_{corner}", vector(**{
                f"W{corner}": -1, f"target{corner}": 1,
            })),
            (f"rho_{corner}", vector(**{
                f"W{corner}": 1, f"ores{corner}": 1,
            })),
        ))
    columns.append(("K", vector(**{
        **{f"ores{corner}": ALPHA[corner] for corner in range(4)},
        "ridge": 1,
    })))
    return tuple(columns)


def row_matrix(columns: tuple[tuple[str, tuple[Q, ...]], ...],
               labels: tuple[str, ...]) -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(value[LABELS.index(label)]
                       for _name, value in columns) for label in labels)


def cap_cartan_intersection_audit() -> dict[str, object]:
    columns = cap_cartan_columns()
    values = tuple(value for _name, value in columns)
    coefficients = tuple(
        coefficient
        for alpha in ALPHA
        for coefficient in (alpha, -alpha, -alpha)
    ) + (Q(1),)
    mv = add(*(scale(coefficient, value) for coefficient, value in
               zip(coefficients, values, strict=True)))
    expected_mv = vector(**{
        **{f"B{corner}": ALPHA[corner] for corner in range(4)},
        **{f"Eq{corner}": ALPHA[corner] for corner in range(4)},
        "ridge": 1,
    })
    require(mv == expected_mv, "the literal M_v signature changed")

    first_rows = (
        "q", "ainc",
        *(f"target{j}" for j in range(4)),
        *(f"W{j}" for j in range(4)),
        *(f"ores{j}" for j in range(4)),
    )
    first_matrix = row_matrix(columns, first_rows)
    first_kernel = nullspace(first_matrix, len(columns))
    require(rank(first_matrix) == 12 and len(first_kernel) == 1
            and first_kernel[0] in (coefficients, scale(-1, coefficients)),
            ("the first augmented-row kernel changed", first_kernel))
    with_eq = first_matrix + row_matrix(
        columns, tuple(f"Eq{j}" for j in range(4))
    )
    with_ridge = first_matrix + row_matrix(columns, ("ridge",))
    require(rank(with_eq) == rank(with_ridge) == len(columns),
            "Eq/ridge stopped killing the M_v residual line")
    return {
        "column_order": [name for name, _value in columns],
        "first_rows": list(first_rows),
        "rank_on_first_rows": rank(first_matrix),
        "source_columns": len(columns),
        "first_rows_kernel_dimension": len(first_kernel),
        "unique_kernel_coefficients": [str(value) for value in coefficients],
        "unique_residual": {
            "name": "M_v=-O_alpha+K",
            "local_B": [int(value) for value in ALPHA],
            "Eq": [int(value) for value in ALPHA],
            "ridge": 1,
            "q_ainc_target_W_ores": 0,
        },
        "rank_after_Eq": rank(with_eq),
        "rank_after_ridge": rank(with_ridge),
        "pure_local_intersection_after_full_known_rows": 0,
    }


def explicit_dual_extension_audit() -> dict[str, object]:
    columns = cap_cartan_columns()
    values = tuple(value for _name, value in columns)
    samples = 0
    stress_failures = 0
    for raw_mu in product((-1, 0, 1), repeat=4):
        mu = tuple(map(Q, raw_mu))
        alpha_mu = dot(ALPHA, mu)
        local = vector(**{f"B{j}": mu[j] for j in range(4)})
        extension = vector(**{
            **{f"B{j}": mu[j] for j in range(4)},
            **{f"target{j}": -mu[j] for j in range(4)},
            **{f"W{j}": -mu[j] for j in range(4)},
            **{f"ores{j}": mu[j] for j in range(4)},
            "ridge": -alpha_mu,
        })
        require(all(dot(extension, value) == 0 for value in values),
                ("the explicit cap/Cartan extension failed", mu))
        mv = vector(**{
            **{f"B{j}": ALPHA[j] for j in range(4)},
            **{f"Eq{j}": ALPHA[j] for j in range(4)},
            "ridge": 1,
        })
        require(dot(local, mv) == alpha_mu
                and dot(extension, mv) == 0,
                ("the M_v stress pairing changed", mu))
        stress_failures += int(bool(alpha_mu))
        samples += 1
    require(samples == 81 and stress_failures == 62,
            ("the extension mutation census changed", samples,
             stress_failures))
    return {
        "local_values": "mu_j=psi(B_j)",
        "extension_formula": {
            "q": 0, "ainc": 0, "Eq_j": 0,
            "target_j": "-mu_j", "W_j": "-mu_j",
            "ores_j": "mu_j", "ridge": "-sum alpha_j mu_j",
        },
        "ternary_mu_packets": samples,
        "uncorrected_packets_detecting_M_v": stress_failures,
        "corrected_packets_detecting_any_known_column": 0,
        "conclusion": (
            "q/ainc require no correction; target/W/ores cancel r0/T/rho, "
            "and the physical ridge cancels the remaining Cartan pairing"
        ),
    }


def literal_lower_face_scope_audit() -> dict[str, object]:
    # Representatives from the complete 378-pair / 630-incidence census.
    # Keep literal factor names: this freezes the fact that the residual is
    # an actual lower source packet, while also exposing that none of these
    # coefficient polynomials carries an AugP2/cap readout by itself.
    c2plus = ("d*q45", "p4*s5", "p5*s4")
    c4 = ("q23*q45", "q24*q35", "q25*q34")
    p2 = ("s3*q45", "s4*q35", "s5*q34")
    require(len(set(c2plus)) == len(set(c4)) == len(set(p2)) == 3,
            "a canonical lower face changed")

    # The exact pure trapped guard q23=q45=d=s3=1 and all other displayed
    # entries zero makes every representative nonzero.
    values = {
        "d": Q(1), "q23": Q(1), "q24": Q(0), "q25": Q(0),
        "q34": Q(0), "q35": Q(0), "q45": Q(1),
        "p4": Q(0), "p5": Q(0), "s3": Q(1), "s4": Q(0),
        "s5": Q(0),
    }
    evaluated = {
        "C2plus": values["d"] * values["q45"],
        "C4": (values["q23"] * values["q45"]
               + values["q24"] * values["q35"]
               + values["q25"] * values["q34"]),
        "P2": (values["s3"] * values["q45"]
               + values["s4"] * values["q35"]
               + values["s5"] * values["q34"]),
    }
    require(set(evaluated.values()) == {Q(1)}, evaluated)
    return {
        "complete_H2_face_classes": [
            "QQ one-edge", "C2plus", "C4", "P2",
        ],
        "canonical_representatives": {
            "C2plus": list(c2plus), "C4": list(c4), "P2": list(p2),
        },
        "pure_trapped_values": {key: str(value)
                                 for key, value in evaluated.items()},
        "raw_lower_face_has_AugP2_rows": False,
        "first_global_source_row_beyond_selected_packet": "H0[000011]",
        "its_literal_effect": (
            "forces one of fourteen alternate matching mates; it does not "
            "choose a terminal extension or a unique occurrence section"
        ),
        "minimal_missing_typed_object": (
            "one totalized source-labelled landing of the selected C2+/C4/P2 "
            "face from its original response word/fine/direction-pair grade "
            "into the cap/Cartan relative grade, with protected q, ainc and "
            "target zero and the shifted ridge carried explicitly"
        ),
        "after_that_landing": (
            "the displayed cap/Cartan extension consumes every local dual; "
            "the exhaustive map gives protected filler or terminal"
        ),
    }


def solve(rows: tuple[tuple[Q, ...], ...], rhs: tuple[Q, ...]
          ) -> tuple[Q, ...] | None:
    variables = len(rows[0]) if rows else 0
    work = [list(map(Q, row)) + [Q(value)]
            for row, value in zip(rows, rhs, strict=True)]
    pivots = []
    pivot_row = 0
    for column in range(variables):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
    if any(not any(row[:variables]) and row[variables] for row in work):
        return None
    answer = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        answer[pivot] = work[row][variables]
    return tuple(answer)


def exhaustive_generator_or_terminal_guard() -> dict[str, object]:
    # Exhaust all small binary complete maps J and nonzero local targets b.
    # Columns of J already include whatever old/source/relative presentation
    # is declared complete.  Either i(b) is a column combination, or solve
    # J^T Psi=0, Psi(i(b))=1.  This is the exact post-placement alternative.
    cases = generators = terminals = 0
    for local_dimension in (1, 2, 3):
        for external_dimension in (0, 1, 2):
            height = local_dimension + external_dimension
            for width in (0, 1, 2):
                for matrix_mask in range(1 << (height * width)):
                    columns = tuple(tuple(Q(
                        (matrix_mask >> (column * height + row)) & 1
                    ) for row in range(height)) for column in range(width))
                    for target_mask in range(1, 1 << local_dimension):
                        target = tuple(Q((target_mask >> row) & 1)
                                       for row in range(local_dimension))
                        embedded = target + (Q(0),) * external_dimension
                        # Solve J*c=embedded.
                        column_rows = tuple(tuple(
                            columns[column][row] for column in range(width)
                        ) for row in range(height))
                        filler = solve(column_rows, embedded)
                        if filler is not None:
                            require(tuple(sum(
                                filler[column] * columns[column][row]
                                for column in range(width)
                            ) for row in range(height)) == embedded,
                                    "generator reconstruction failed")
                            generators += 1
                        else:
                            equations = tuple(tuple(
                                columns[column][row] for row in range(height)
                            ) for column in range(width)) + (embedded,)
                            rhs = (Q(0),) * width + (Q(1),)
                            terminal = solve(equations, rhs)
                            require(terminal is not None
                                    and all(dot(terminal, column) == 0
                                            for column in columns)
                                    and dot(terminal, embedded) == 1,
                                    "terminal reconstruction failed")
                            terminals += 1
                        cases += 1
    require(cases == generators + terminals and generators and terminals,
            ("dichotomy census changed", cases, generators, terminals))
    return {
        "small_binary_packets": cases,
        "pure_local_filler_cases": generators,
        "augmented_terminal_cases": terminals,
        "exact_alternative": (
            "i(o2) in im(J): protected-zero physical filler; otherwise "
            "there is Psi with Psi*J=0 and Psi(i(o2))=1"
        ),
        "third_branch": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 o2 augmented cap/Cartan extension and exact fork",
        "pins": PINS,
        "known_packet_intersection": cap_cartan_intersection_audit(),
        "explicit_local_dual_extension": explicit_dual_extension_audit(),
        "literal_H2_lower_face_scope": literal_lower_face_scope_audit(),
        "post_placement_dichotomy": exhaustive_generator_or_terminal_guard(),
        "source_level_consequence": (
            "For o2 nonzero modulo the 171-column source Jacobian, the known "
            "r0/T/rho/K packet creates no augmented terminal obstruction. "
            "After o2 is placed in an exhaustive same-grade physical map, "
            "it is either the boundary of a protected-zero relative filler "
            "or is detected by an actual augmented terminal.  Hence the "
            "only unresolved source arm after this fork is o2=0, where the "
            "formal source arc must be prolonged to higher order."
        ),
        "first_literal_stress_column": (
            "M_v=-O_alpha+K; the uncorrected local dual pairs by alpha.mu, "
            "but the displayed target/W/ores/ridge correction makes the "
            "pairing zero on every constituent column"
        ),
        "first_missing_physical_datum": (
            "for the classified nonzero H2 face, a source-labelled map "
            "placing its literal C2+/C4/P2 response word/fine/direction-pair "
            "grade in the same exhaustive AugP2/repeated physical codomain. "
            "The first omitted unary H0[000011] forces a mate but does not "
            "supply this landing.  Endpoint polarization gives the symbol, "
            "but not the response-to-relative map."
        ),
        "scope": (
            "exact canonical normalized cap/Cartan signatures and exact "
            "finite-dimensional duality.  It does not construct the missing "
            "word-grade landing or evaluate o2 at every trapped source."
        ),
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
    print("known q/ainc/target/W/ores rows: ONE RESIDUAL M_v LINE")
    print("Eq or physical ridge kills the residual local intersection")
    print("every local o2 dual extends over r0/T/rho/K explicitly")
    print("after grade placement: PHYSICAL FILLER OR AUGMENTED TERMINAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
