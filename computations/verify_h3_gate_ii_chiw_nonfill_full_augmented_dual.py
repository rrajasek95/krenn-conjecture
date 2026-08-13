#!/usr/bin/env python3
"""Compute the full known-row dual on the Gate-II chi_w nonfill arm.

The missing root-only cylinder has mixed-target signature

    delta = (1,1,-1,-1),      Y = (0,-delta).

The cap/Cartan extension formula for a local dual with values mu_j on the
four literal B_j corners is

    target=-mu, W=-mu, ores=mu,
    ridge=-alpha.mu, q=ainc=Eq=0,

where alpha=(-1,1,1,-1).  For mu=delta, alpha.delta=0.  Hence the primitive
integer dual has no q, anchor, ridge, eta, or sigma coefficient.  It
annihilates every known r0/T/rho/K column and detects both the local delta-B
face and the target-only companion Y with value four.

This is not yet an accepted physical terminal.  It has only been extended
through the known cap/Cartan submap.  Promotion requires its pullback to
vanish on every additional literal source column in the identical
word/fine/repeated/Hasse/common-tail grade (or to be correctable without
changing the detected value).  Equivalently, one must place the C4 output
in an exhaustive source-labelled augmented map.  Then exact duality gives
the already accepted filler-or-terminal fork.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_physical_orbit_invariant_pointed_cylinder.py":
        "8e218076d03456a04fdd6efb2720c6d38d89230574c0c8f1cd0bf99e37eaee23",
    "notes/h3-gate-ii-physical-orbit-invariant-pointed-cylinder.md":
        "7c661eb393793ed6b17a7bb85fe1d9a759588beab6c044da291c471cb56d1b28",
    "computations/verify_h3_gate_ii_chiw_chart_complete_h2_face.py":
        "a80e5ec2a1aaa90814b412d13b1c7981f345bb41ca5a5450d5361ae2bc9f5773",
    "notes/h3-gate-ii-chiw-chart-complete-h2-face.md":
        "95fcde72841aa4b859ffa0711fb30149cd9d3406ad44dcba228445f0023c5505",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
    "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py":
        "ecb8725715747c3270fb069545309283d1890fbac6e66dfb6ed2f53b609e0030",
    "notes/h3-generic-symmetric-c4-placement-terminal-gate.md":
        "dcf0ef4adf500b4bee46ca301b12241e95ed1343a509a4fe4110d5dd3a906e92",
    "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py":
        "aea73ce5ff6ce183245d209393ed60192066d38eab7d4d203caa0c82cc5b16d6",
    "notes/h3-residual-q-terminal-ridge-kahler-identification.md":
        "ddccd38496103c2a597d3f6f589adf65f3ed7a5ab4da1bc8e36168618d480fd6",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "notes/h3-first-flat-physical-anchor-six-term-separator.md":
        "73d389a492b26c40ab27b0ed788c43c04a1e58a1abae94800916667aa6150b7f",
}
EXPECTED_LEDGER_SHA256 = (
    "124b6abd4248fadcba37ce7b0627e7675f014cc946ad4f6b8f1f7ef230b2324b"
)

ALPHA = tuple(map(Q, (-1, 1, 1, -1)))
DELTA = tuple(map(Q, (1, 1, -1, -1)))
LABELS = (
    *(f"B{j}" for j in range(4)),
    *(f"Eq{j}" for j in range(4)),
    "M", "ainc", "q", "P_f",
    *(f"target{j}" for j in range(4)),
    *(f"W{j}" for j in range(4)),
    *(f"ores{j}" for j in range(4)),
    "ridge", "eta_constant", "eta_u_over_t", "sigma_q22",
    "W_global", "common_tail_escape",
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
    require(not unknown, ("unknown labels", sorted(unknown)))
    return tuple(Q(entries.get(label, 0)) for label in LABELS)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(value) for value in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient: int | Q,
          value: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in value)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def cap_cartan_columns(extra_values=(Q(0), Q(0), Q(0), Q(0))):
    """Known columns, with arbitrary pointed-anchor values on r0 corners."""
    require(len(extra_values) == 4, "four P_f values required")
    columns = []
    for corner in range(4):
        # M=ainc=-1 makes the physical q=M-ainc row zero, as in the
        # canonical cap packet.  P_f is deliberately arbitrary: the dual
        # has zero P_f coefficient, so the cap cancellation does not use it.
        columns.extend((
            (f"r0_{corner}", vector(**{
                f"B{corner}": 1, f"Eq{corner}": 1,
                f"target{corner}": 1,
                "M": -1, "ainc": -1, "q": 0,
                "P_f": extra_values[corner],
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
        # The ridge terminal contractions are present on K.  Their exact
        # values do not enter because the chi_w dual has zero ridge and
        # eta/sigma coefficients.
        "eta_constant": 1, "eta_u_over_t": 1, "sigma_q22": -1,
    })))
    return tuple(columns)


def primitive_augmented_dual() -> tuple[Q, ...]:
    alpha_delta = dot(ALPHA, DELTA)
    require(alpha_delta == 0, "alpha stopped being orthogonal to delta")
    return vector(**{
        **{f"B{corner}": DELTA[corner] for corner in range(4)},
        **{f"target{corner}": -DELTA[corner] for corner in range(4)},
        **{f"W{corner}": -DELTA[corner] for corner in range(4)},
        **{f"ores{corner}": DELTA[corner] for corner in range(4)},
        "ridge": -alpha_delta,
    })


def audit_full_known_augmented_extension() -> dict[str, object]:
    dual = primitive_augmented_dual()
    nonzero_integers = [abs(int(value)) for value in dual if value]
    require(nonzero_integers and gcd(*nonzero_integers) == 1,
            "the augmented dual stopped being primitive")

    # Stress arbitrary pointed-anchor data on the four cap corners.  Because
    # the dual's P_f coefficient is zero, all packets give the same answer.
    tested = 0
    for p_f_values in product((-1, 0, 1), repeat=4):
        columns = cap_cartan_columns(tuple(map(Q, p_f_values)))
        require(all(dot(dual, value) == 0 for _name, value in columns),
                ("the full dual failed on a known column", p_f_values))
        tested += 1
    require(tested == 81, "the pointed-anchor stress census changed")

    columns = cap_cartan_columns()
    values = tuple(value for _name, value in columns)
    b_delta = vector(**{
        **{f"B{corner}": DELTA[corner] for corner in range(4)}
    })
    y_target = vector(**{
        **{f"target{corner}": -DELTA[corner] for corner in range(4)}
    })
    require(dot(dual, b_delta) == dot(dual, y_target) == Q(4),
            "the primitive dual stopped detecting the two nonfill shadows")
    require(rank(values + (b_delta,)) == rank(values) + 1
            and rank(values + (y_target,)) == rank(values) + 1,
            "a detected nonfill shadow entered the known cap image")

    coefficients = {
        label: str(dual[index])
        for index, label in enumerate(LABELS) if dual[index]
    }
    require(all(dual[LABELS.index(label)] == 0 for label in (
        "M", "ainc", "q", "P_f", "ridge", "eta_constant",
        "eta_u_over_t", "sigma_q22", "W_global", "common_tail_escape",
    )), "a protected zero coefficient changed")
    return {
        "corner_vectors": {
            "alpha": list(map(int, ALPHA)),
            "delta": list(map(int, DELTA)),
            "alpha_dot_delta": str(dot(ALPHA, DELTA)),
        },
        "primitive_integer_dual_nonzero_coefficients": coefficients,
        "compact_signature": {
            "B": list(map(int, DELTA)),
            "target": list(map(int, scale(-1, DELTA))),
            "W": list(map(int, scale(-1, DELTA))),
            "ordinary_residue": list(map(int, DELTA)),
            "Eq": [0, 0, 0, 0],
            "M": 0, "ainc": 0, "q=M-ainc": 0, "P_f": 0,
            "ridge": 0,
            "eta_constant_eta_u_over_t_sigma_q22": [0, 0, 0],
            "global_W": 0, "common_tail_escape": 0,
        },
        "known_columns_annihilated": [name for name, _value in columns],
        "pointed_anchor_assignments_stressed": tested,
        "value_on_local_delta_B": "4",
        "value_on_target_companion_Y": "4",
        "normalized_rational_detector": "tilde_psi_delta/4",
        "explanation": (
            "target/W/ores cancel each r0/T/rho corner, while "
            "alpha.delta=0 cancels K without a ridge coefficient.  Hence "
            "the induced eta/sigma coefficients vanish as well"
        ),
    }


def audit_q_anchor_and_terminal_separation() -> dict[str, object]:
    dual = primitive_augmented_dual()
    # q=M-ainc is checked literally on a sample family of source columns.
    # The new dual ignores all three rows.  This proves compatibility, not
    # that q or the pointed anchor detects the missing class.
    samples = 0
    for matching, anchor, pointed in product((-1, 0, 1), repeat=3):
        column = vector(M=matching, ainc=anchor,
                        q=matching - anchor, P_f=pointed)
        require(column[LABELS.index("q")]
                == column[LABELS.index("M")]
                   - column[LABELS.index("ainc")]
                and dot(dual, column) == 0,
                "q/anchor compatibility changed")
        samples += 1
    require(samples == 27, "the q/anchor sample count changed")

    # The accepted first-flat separator has zero target/W/ores and a nonzero
    # anchor component.  Our new dual has the opposite qualitative support,
    # so it cannot simply be renamed as that terminal.
    new_support = {label for label, value in zip(LABELS, dual, strict=True)
                   if value}
    accepted_support = {"selected_matching_sum", "ainc"}
    require(new_support.isdisjoint(accepted_support),
            "the chi_w dual became the old first-flat separator")
    return {
        "q_equals_M_minus_ainc_samples": samples,
        "dual_coefficients_on_M_ainc_q_Pf": [0, 0, 0, 0],
        "q_or_anchor_generator_detected": False,
        "accepted_first_flat_separator_support":
            sorted(accepted_support),
        "new_dual_support_kind": [
            "local C4", "mixed target", "W corners", "labelled residue",
        ],
        "same_as_existing_first_flat_separator": False,
        "consequence": (
            "the q and P_f rows do not obstruct extension, but they also do "
            "not promote the coefficient covector to an accepted generator "
            "or separator"
        ),
    }


def audit_same_grade_extension_gate() -> dict[str, object]:
    dual = primitive_augmented_dual()
    known_columns = tuple(value for _name, value in cap_cartan_columns())
    candidate = vector(**{
        **{f"B{corner}": DELTA[corner] for corner in range(4)}
    })

    # A first extra same-grade column can either preserve the dual or break
    # it.  These exact representatives demonstrate why known-row
    # annihilation is not full-source terminality.
    dark_extra = add(known_columns[0], known_columns[1])
    bright_extra = vector(B0=1)
    require(dot(dual, dark_extra) == 0
            and dot(dual, bright_extra) == 1,
            "the extra-column extension guard changed")

    # Once an exhaustive same-grade map is supplied, ordinary image/cokernel
    # duality has no third branch.  The bright example may either fill the
    # candidate after further columns or force a mutated full dual; the
    # particular known-row dual is not guaranteed to survive unchanged.
    return {
        "candidate_output": "i(B_delta) in the literal C4 AugP2 grade",
        "known_cap_cartan_pullback": 0,
        "sample_dark_extra_pullback": str(dot(dual, dark_extra)),
        "sample_bright_extra_pullback": str(dot(dual, bright_extra)),
        "specific_primitive_dual_is_full_terminal_iff":
            "tilde_psi_delta * J_extra = 0",
        "allowing_augmented_correction": (
            "there exists a full covector Psi extending the local delta "
            "value, with Psi*J_full=0 and Psi(i(B_delta))=1"
        ),
        "missing_extension": (
            "the literal source-labelled map from the original "
            "Hasse[2](D,Q01) fan word/fine/direction-pair/common-tail block "
            "into an exhaustive AugP2/repeated physical codomain, including "
            "all response/block-projector and downstream word-0102 columns"
        ),
        "after_extension": {
            "candidate_in_image": "protected-zero filler/generator",
            "candidate_outside_image": "full augmented physical terminal",
            "third_branch": False,
        },
        "why_absence_from_current_inventory_is_insufficient": (
            "not finding a named source cell proves neither nonmembership "
            "in the span of all same-grade physical columns nor annihilation "
            "of their pullbacks by the displayed dual"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II chi_w nonfill full augmented dual gate",
        "pins": PINS,
        "full_known_augmented_dual": audit_full_known_augmented_extension(),
        "physical_q_anchor_terminal_separation":
            audit_q_anchor_and_terminal_separation(),
        "same_grade_full_source_extension": audit_same_grade_extension_gate(),
        "verdict": (
            "On the nonfill arm the primitive covariant dual is explicit: "
            "B=delta, target=W=-delta, ores=delta, and every Eq, M, ainc, "
            "q, P_f, ridge, eta/sigma, global-W and tail-escape coefficient "
            "is zero.  Since alpha.delta=0, it annihilates the entire known "
            "r0/T/rho/K packet and detects the missing local or target face "
            "with value four.  It is not yet an accepted physical terminal: "
            "the remaining requirement is extension across every additional "
            "source column in the identical literal Hasse/word/fine/repeated "
            "and common-tail grade.  Once that exhaustive placement is "
            "provided, the committed filler-or-terminal fork has no third arm"
        ),
        "scope": (
            "exact primitive dual and augmented sign audit for the known "
            "canonical cap/Cartan packet, with symbolic pointed-anchor and "
            "literal q=M-ainc stress.  It does not prove nonmembership in an "
            "unconstructed exhaustive source map or promote a bare local "
            "coefficient covector to a physical terminal"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Gate-II nonfill dual ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("Gate II nonfill primitive dual: EXPLICIT")
    print("B/target/W/ores = delta/-delta/-delta/delta")
    print("q, P_f, ridge, eta/sigma: ZERO")
    print("known r0/T/rho/K packet: ANNIHILATED")
    print("accepted physical terminal: NEEDS FULL SAME-GRADE EXTENSION")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
