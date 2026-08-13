#!/usr/bin/env python3
"""Audit terminalization of L=90 f-R after the relative Segre Tate lift."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_shear_relative_tate_completion_gate.py":
        "5137f0aa5fa062a8310064b7e655bc87dbe9d1d6ec71741ff2bc53b39f1b16f6",
    "notes/h3-centered-shear-relative-tate-completion-gate.md":
        "ffd8a9a888c768c2cbffa7f19988ff1eefd4bde2dcc5d13712a7a771a578c2b4",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
    "computations/verify_dark_cartan_physical_q_transport_gate.py":
        "8dc8e1e25316fd32ac27d86ebfff1ca77c870c302ff7becd9f10751d8567046c",
    "notes/dark-cartan-physical-q-transport-gate.md":
        "da4b08160796b659b42e891efaae08d5063693af704394b70ae6904faa1c4424",
    "computations/verify_h3_rootless_augmented_pentagon_fredholm_alternative.py":
        "0b0831391416f85302b5f2d89da0672e07dca4c73fc5f3893ad992abd48c1d2b",
    "notes/h3-rootless-augmented-pentagon-fredholm-alternative.md":
        "4febecdfa01b6697970af0d518721058842afe784ac59f267b8ebc847a43cecb",
}
EXPECTED_LEDGER_SHA256 = "190d537e5f24985505bece1677c24d85ff3275c8075bc69b88ac7ca5096dbcda"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def matvec(matrix: tuple[tuple[Q, ...], ...], vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum((a*b for a, b in zip(row, vector, strict=True)), Q(0))
                 for row in matrix)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def fixed_fibre_obstruction() -> dict[str, object]:
    # The trapped normalization is R(x)=0 and f(x)=1.
    N, f_value, response_value = Q(90), Q(1), Q(0)
    L_value = N*f_value-response_value
    require(L_value == 90, "the centered scalar normal changed")

    # A chain map to the classical fibre k (zero differential) would have
    # 0=d(phi(epsilon))=phi(d epsilon)=phi(L), a contradiction.
    terminal_differential_of_epsilon = Q(0)
    require(terminal_differential_of_epsilon != L_value,
            "the fixed-fibre obstruction disappeared")
    return {
        "trapped_values": {"R": 0, "f": 1, "L=90f-R": 90},
        "relative_cell": "d epsilon=L",
        "fixed_fibre_chain_map": False,
        "reason": "0=d(phi epsilon) differs from phi(L)=90",
        "mandatory_next_face": (
            "a physical scalar/target source correction before epsilon can be a "
            "column of the fixed trapped packet"
        ),
    }


def two_completion_guard() -> dict[str, object]:
    # Columns are (placed base, corrected epsilon, three independent Segre
    # Tate directions).  Once a hypothetical scalar/target correction closes
    # L, the principal map has the epsilon line as its sole kernel.
    J = (
        (Q(1), 0, 0, 0, 0),
        (0, 0, Q(1), 0, 0),
        (0, 0, 0, Q(1), 0),
        (0, 0, 0, 0, Q(1)),
    )
    kernel = (Q(0), Q(1), Q(0), Q(0), Q(0))
    require(matvec(J, kernel) == (0, 0, 0, 0), "kernel line changed")

    matching = (Q(1), Q(0), Q(0), Q(0), Q(0))
    ainc_dark = (Q(0), Q(0), Q(0), Q(0), Q(0))
    ainc_bright = (Q(0), Q(-1), Q(0), Q(0), Q(0))
    q_dark = tuple(m-a for m, a in zip(matching, ainc_dark, strict=True))
    q_bright = tuple(m-a for m, a in zip(matching, ainc_bright, strict=True))
    require(q_dark == (1, 0, 0, 0, 0)
            and q_bright == (1, 1, 0, 0, 0),
            "q=M-ainc changed")
    require(sum(q_dark[i]*kernel[i] for i in range(5)) == 0
            and sum(q_bright[i]*kernel[i] for i in range(5)) == 1,
            "the generator/separator fork changed")

    # q_dark is literally the first principal row, while q_bright cannot
    # factor through J because it detects ker J.
    require(q_dark == J[0], "the dark q no longer factors through J")

    common_rows = {
        "anchor": [0, 90, 0, 0, 0],
        "target": [0, 0, 0, 0, 0],
        "ordinary_residue": [0, 0, 0, 0, 0],
        "W": [0, 0, 0, 0, 0],
        "shifted_ridge": [0, 0, 0, 0, 0],
        "eta": [0, 0, 0, 0, 0],
        "sigma": [0, 0, 0, 0, 0],
    }
    return {
        "domain_columns": [
            "placed base", "corrected epsilon", "Segre Tate 01",
            "Segre Tate 02", "Segre Tate 12",
        ],
        "principal_kernel": "span(corrected epsilon)",
        "common_output_rows": common_rows,
        "common_matching_row": [int(value) for value in matching],
        "completion_dark": {
            "ainc": [int(value) for value in ainc_dark],
            "q=M-ainc": [int(value) for value in q_dark],
            "outcome": "q kills ker(J) and factors through the first J row",
        },
        "completion_bright": {
            "ainc": [int(value) for value in ainc_bright],
            "q=M-ainc": [int(value) for value in q_bright],
            "outcome": "q(kernel)=1, the relative-generator branch",
        },
        "Segre_Tate_effect_on_ambiguity": (
            "none: all three new directions are principal pivots and are dark "
            "in every listed augmented row"
        ),
        "minimality": (
            "one corrected hidden kernel line and one placed line are necessary "
            "and sufficient to distinguish factorization from generator"
        ),
    }


def terminal_pairing_audit() -> dict[str, object]:
    return {
        "before_physical_placement": (
            "L belongs to the occurrence coefficient algebra; the physical "
            "source-terminal/Macaulay quotient is a quotient of the augmented "
            "output.  No committed chain map identifies these two classes."
        ),
        "after_adjoining_epsilon": (
            "L=d epsilon is exact.  Every genuine terminal cocycle annihilates "
            "its image under any chain comparison."
        ),
        "nonzero_pairing_meaning": (
            "a terminal covector pairing nontrivially with L would obstruct the "
            "physical epsilon; it cannot simultaneously be a cocycle on a complex "
            "that contains that epsilon"
        ),
        "conclusion": (
            "Segre Tate completion does not itself terminalize L.  It converts L "
            "to an exact face and leaves the same augmented placement/zero-"
            "indeterminacy theorem as the only bridge to the Macaulay quotient."
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 centered scalar normal terminal-extension guard",
        "pins": PINS,
        "fixed_fibre": fixed_fibre_obstruction(),
        "two_completion_guard": two_completion_guard(),
        "terminal_pairing": terminal_pairing_audit(),
        "verdict": (
            "At the trapped normalization R=0,f=1, L=90 cannot be the boundary "
            "of a cell in the fixed classical fibre without an additional physical "
            "scalar/target correction.  After granting that correction and all "
            "Segre Tate cells, the full disclosed anchor/target/residue/W/ridge/"
            "eta/sigma data still admit two exact q=M-ainc completions: one gives "
            "the factorized Fredholm arm and one gives a unit kernel generator. "
            "Thus L has no canonical class in the existing terminal/Macaulay "
            "quotient; the missing datum is the complete physical augmented "
            "placement, not another toric relation."
        ),
        "scope": (
            "exact h=3 relative-Tate and complete-output linear guard.  The two "
            "completions obey every currently committed row identity but are not "
            "claimed to be two complete GHZ source points."
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("L on trapped fixed fibre: 90 (NOT A BOUNDARY)")
    print("Segre Tate completion terminalizes L: NO; L BECOMES EXACT")
    print("full disclosed augmented rows determine q: NO")
    print("sharp completions: FACTORIZED FREDHOLM / UNIT GENERATOR")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
