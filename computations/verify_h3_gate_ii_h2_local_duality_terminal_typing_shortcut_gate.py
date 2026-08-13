#!/usr/bin/env python3
"""Audit the proposed original-Hasse[2] Fredholm shortcut for Gate II.

Finite duality may certainly be applied to an exhaustive boundary map in
the original Hasse[2](D,Q01) output object.  If the selected class is not in
the image, it gives a covector on that Hasse output.  This checker records
why that covector is not, merely by zero extension, an accepted physical
terminal on the cap--Cartan correction object.

The first obstruction is already the old cap column

    r0_j = B_j + Eq_j + target_j - ainc.

A local value mu_j on B_j pairs nontrivially with r0_j unless the target
coefficient is extended by -mu_j.  Continuing through T_j, rho_j and K
forces W=-mu, ores=mu and ridge=-alpha.mu.  For the Gate-II character
delta=(1,1,-1,-1), alpha.delta=0, so ridge, q and eta/sigma are zero.  Thus
ridge is not the obstruction in this special character: the missing datum
is the typed identification of the original Hasse output with the four
literal cap corners and extension across every same-grade source column.

That identification is not definitional.  The Hasse survivor is a
three-occurrence C4 tail in Hasse[2](D,Q01), in the parent fan
word/fine/repeated object.  The cap corners are four complete 90-term
boundaries in the normalized relative P3+K2/faces-(3,5) object.  The
committed theorems deliberately introduce a map i:Y_loc->Y_aug; none
identifies these two differently tagged summands by identity.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_chiw_chart_complete_h2_face.py":
        "a80e5ec2a1aaa90814b412d13b1c7981f345bb41ca5a5450d5361ae2bc9f5773",
    "notes/h3-gate-ii-chiw-chart-complete-h2-face.md":
        "95fcde72841aa4b859ffa0711fb30149cd9d3406ad44dcba228445f0023c5505",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
    "notes/h3-gate-ii-chiw-nonfill-full-augmented-dual.md":
        "f7fd790075f7cf3d31b9d4a6035fa6bc476a3bdc16ce4bda97b777b153664568",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "notes/h3-literal-mv-cap-cartan-composition.md":
        "1f1a3596bcbbabe8756ce3097a21bfba38ccdf9474352ec73e17d55f524d9cc1",
    "computations/verify_h3_gate_ii_complete_rows_pointed_scalar_boundary.py":
        "077960db0b93888eb323cce89b81dced2d98d3086fc397180d4d446818b1cbe8",
    "notes/h3-gate-ii-complete-rows-pointed-scalar-boundary.md":
        "42a9adbf5e417b0ecae151f8b504c3f75524b3f8b909d69bf8a63b51a8329d6e",
}
EXPECTED_LEDGER_SHA256 = (
    "fce6af9f531f0b75d02ba321026b73951efb48f54ec155f22262f440397793cb"
)

ALPHA = tuple(map(Q, (-1, 1, 1, -1)))
DELTA = tuple(map(Q, (1, 1, -1, -1)))
LABELS = (
    *(f"B{j}" for j in range(4)),
    *(f"Eq{j}" for j in range(4)),
    "ainc", "q",
    *(f"target{j}" for j in range(4)),
    *(f"W{j}" for j in range(4)),
    *(f"ores{j}" for j in range(4)),
    "ridge", "eta", "sigma",
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
    require(not (set(entries) - set(LABELS)),
            ("unknown rows", sorted(set(entries) - set(LABELS))))
    return tuple(Q(entries.get(label, 0)) for label in LABELS)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def cap_columns() -> tuple[tuple[str, tuple[Q, ...]], ...]:
    columns = []
    for j in range(4):
        columns.extend((
            (f"r0_{j}", vector(**{
                f"B{j}": 1, f"Eq{j}": 1, f"target{j}": 1,
                "ainc": -1,
            })),
            (f"T_{j}", vector(**{
                f"W{j}": -1, f"target{j}": 1,
            })),
            (f"rho_{j}", vector(**{
                f"W{j}": 1, f"ores{j}": 1,
            })),
        ))
    columns.append(("K", vector(**{
        **{f"ores{j}": ALPHA[j] for j in range(4)},
        "ridge": 1, "eta": 1, "sigma": -1,
    })))
    return tuple(columns)


def local_duality_and_zero_extension_audit() -> dict[str, object]:
    columns = cap_columns()
    samples = 0
    zero_extensions_that_annihilate_cap = 0
    corrected_extensions_that_fail = 0
    for raw_mu in product((-1, 0, 1), repeat=4):
        mu = tuple(map(Q, raw_mu))
        local = vector(**{f"B{j}": mu[j] for j in range(4)})
        alpha_mu = sum((ALPHA[j] * mu[j] for j in range(4)), Q(0))
        corrected = vector(**{
            **{f"B{j}": mu[j] for j in range(4)},
            **{f"target{j}": -mu[j] for j in range(4)},
            **{f"W{j}": -mu[j] for j in range(4)},
            **{f"ores{j}": mu[j] for j in range(4)},
            "ridge": -alpha_mu,
        })
        zero_extensions_that_annihilate_cap += int(all(
            dot(local, column) == 0 for _name, column in columns
        ))
        corrected_extensions_that_fail += int(any(
            dot(corrected, column) != 0 for _name, column in columns
        ))
        samples += 1
    require(samples == 81
            and zero_extensions_that_annihilate_cap == 1
            and corrected_extensions_that_fail == 0,
            (samples, zero_extensions_that_annihilate_cap,
             corrected_extensions_that_fail))

    delta_alpha = sum((a * d for a, d in
                       zip(ALPHA, DELTA, strict=True)), Q(0))
    require(delta_alpha == 0, "Gate-II character acquired a ridge value")
    zero_delta = vector(**{f"B{j}": DELTA[j] for j in range(4)})
    require(tuple(dot(zero_delta, column) for name, column in columns
                  if name.startswith("r0_")) == DELTA,
            "the first r0 obstruction changed")
    return {
        "local_linear_alternative": (
            "for exhaustive J_H2, either o2 is in im J_H2 or a local "
            "covector psi_H2 annihilates J_H2 and detects o2"
        ),
        "ternary_local_covectors_tested": samples,
        "zero_extensions_annihilating_all_known_cap_columns":
            zero_extensions_that_annihilate_cap,
        "first_failure": "psi_zero(r0_j)=mu_j",
        "forced_known_packet_extension": {
            "target_j": "-mu_j", "W_j": "-mu_j",
            "ores_j": "mu_j", "ridge": "-alpha.mu",
            "q": 0, "ainc": 0, "Eq_j": 0,
        },
        "Gate_II_delta": list(map(int, DELTA)),
        "alpha_dot_delta": str(delta_alpha),
        "delta_ridge_q_eta_sigma": [0, 0, 0, 0],
        "consequence": (
            "ridge is a required row of the terminal codomain but its "
            "coefficient is zero on this character; cap/full-map extension, "
            "not a nonzero ridge value, is the obstruction"
        ),
    }


def typed_inclusion_audit() -> dict[str, object]:
    local_type = {
        "source_head": "11:110000 parent fan response block",
        "order_and_directions": "Hasse[2](D,Q01)",
        "residual_sites": "2345",
        "local_face": ["q23*q45", "q24*q35", "q25*q34"],
        "occurrence_coordinates": 3,
        "operation_profile": "DQ (or transported PS), retained",
        "augmented_rows_before_comparison": "not canonically defined",
    }
    cap_type = {
        "source_word": "1211222 after deleting the distinguished endpoint",
        "order_and_directions": "relative r0/T/rho + Cartan/HPL",
        "relative_grade": "canonical labelled repeated P3+K2, faces-(3,5)",
        "corner_coordinates": 4,
        "literal_features_per_B_corner": 90,
        "literal_features_in_alpha_aggregate": 360,
        "augmented_rows": "Eq,target,ainc,W,ores,ridge,eta,sigma,q",
    }
    require(local_type["order_and_directions"]
            != cap_type["order_and_directions"]
            and local_type["occurrence_coordinates"]
            != cap_type["corner_coordinates"]
            and local_type["operation_profile"]
            not in cap_type["relative_grade"],
            "the two physical types accidentally became identical")
    return {
        "original_H2_output": local_type,
        "cap_Cartan_output": cap_type,
        "same_word_fine_repeated_idempotent": False,
        "B_notation_guard": (
            "the three H2345 matching occurrences are not the four "
            "B_j^cap complete 90-term boundaries"
        ),
        "definitional_inclusion_exists": False,
        "required_new_data": (
            "a source-labelled comparison i from the parent fan Hasse[2] "
            "object to the cap/repeated object, or directly a covector on "
            "the complete augmented map whose restriction is psi_H2"
        ),
        "why_r0_does_not_define_i": (
            "r0_j defines a column after a cap corner has been selected; it "
            "does not identify a DQ-tagged three-matching Hasse tail with "
            "one of four repeated-grade complete boundaries"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II original-H2 duality terminal-typing shortcut gate",
        "pins": PINS,
        "local_duality_vs_physical_terminal":
            local_duality_and_zero_extension_audit(),
        "typed_inclusion": typed_inclusion_audit(),
        "verdict": (
            "Running exact duality in the exhaustive original Hasse[2] "
            "grade is legitimate and can produce a local obstruction "
            "covector without first constructing a primal filler.  It does "
            "not by itself produce an accepted physical terminal.  The "
            "terminal must annihilate the complete augmented source map; "
            "zero extension fails already on r0.  The 4373ae6 correction "
            "solves the known cap rows once local corner values are typed, "
            "but the required Hasse-to-cap identification is not "
            "definitional because the word/fine/direction/repeated objects "
            "and occurrence arities differ."
        ),
        "frontier": (
            "placement-before-duality is avoidable only as an order of "
            "operations: compute psi_H2 locally first.  Physical terminal "
            "promotion still requires the dual comparison/extension.  On "
            "delta no separate ridge/eta/sigma construction is needed."
        ),
        "scope": (
            "exact canonical h=3 local Hasse and normalized cap/Cartan "
            "packets.  This does not construct the comparison or prove "
            "annihilation of unenumerated full same-grade source columns."
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
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("original Hasse[2] duality: VALID LOCAL ALTERNATIVE")
    print("local covector as accepted terminal: NO")
    print("zero extension first fails: r0_j")
    print("delta ridge/q/eta/sigma coefficients: ZERO")
    print("Hasse-to-cap inclusion: NOT DEFINITIONAL; TYPES DIFFER")
    print("remaining datum: typed dual extension or comparison i")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
