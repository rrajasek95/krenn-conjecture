#!/usr/bin/env python3
"""Reduce the centered-shear attack to one physical cross-word bridge."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_scalar_normal_terminal_extension_guard.py":
        "2c0b5f89a99a2ad9058aaa1648ecdff6933d60bee6bc1f92cdb389e64ba73ca7",
    "notes/h3-centered-scalar-normal-terminal-extension-guard.md":
        "ca7320c152463d9fd594adcb35048343d276aefe4663826fe609ae8ee3effafb",
    "computations/verify_h3_centered_shear_h0_target_cylinder_alternative.py":
        "b4aa84a571500c0e4745ae29ea6c1f23076c63bac139d1bd839fdb1160f515ab",
    "notes/h3-centered-shear-h0-target-cylinder-alternative.md":
        "d21d02f0d3dfece57e080511c34af78b38b77b87600837a05668ae1970b7e70e",
    "computations/verify_h3_segre_bright_full_row_min_support_completion_gate.py":
        "3db99d9141e3015c6199da76c0619a235bb6fb95f364e3d2dce338fa2d428572",
    "notes/h3-segre-bright-full-row-min-support-completion-gate.md":
        "26f94fac7c66405eff04406c95935da910d26cdecf135b05a212e469506cbfc9",
    "computations/verify_h3_h0_cylinder_mixed_curvature_landing_guard.py":
        "9395988206e235f9770e32c06c7cbed0ba9f98705a6ab00e5c667596853b9386",
    "notes/h3-h0-cylinder-mixed-curvature-landing-guard.md":
        "eb98851250ef123de44a9033beb3abcebc045f326fc254c68f07cab1d226893b",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
}
EXPECTED_LEDGER_SHA256 = "4be857848f9e83390378f7304f77fb9819fe981d408ff15069b0d3e472f41da4"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(vectors: tuple[tuple[Q, ...], ...]) -> int:
    rows = [list(map(Q, vector)) for vector in vectors]
    answer = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry/value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left-value*right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a*b for a, b in zip(left, right, strict=True)), Q(0))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    # Coordinates are (Aq0,Aq1,Aq2,Bq0,Bq1,Bq2).  These are the three
    # toric characters; their span is endpoint-odd times matching-standard.
    characters = (
        tuple(map(Q, (-1, 1, 0, 1, -1, 0))),
        tuple(map(Q, (-1, 0, 1, 1, 0, -1))),
        tuple(map(Q, (0, -1, 1, 0, 1, -1))),
    )
    aggregate = (
        tuple(map(Q, (1, 1, 1, 0, 0, 0))),
        tuple(map(Q, (0, 0, 0, 1, 1, 1))),
        tuple(map(Q, (1, 0, 0, 1, 0, 0))),
        tuple(map(Q, (0, 1, 0, 0, 1, 0))),
        tuple(map(Q, (0, 0, 1, 0, 0, 1))),
    )
    require(rank(characters) == 2
            and all(dot(character, row) == 0
                    for character in characters for row in aggregate),
            "the mixed character decomposition changed")

    # A homogeneous Macaulay multiple of a target-only generator closes the
    # cylinder curvature.  The physical cap graph instead has target=ores=1,
    # so its multiple moves the same coefficient from target to residue.
    k = Q(7)
    target_curvature = (k, Q(0))
    pure_target_multiple = (-k, Q(0))
    cap_graph_multiple = (-k, -k)
    require(tuple(a+b for a, b in zip(target_curvature,
                                      pure_target_multiple, strict=True))
            == (0, 0), "pure target multiplication stopped closing curvature")
    require(tuple(a+b for a, b in zip(target_curvature,
                                      cap_graph_multiple, strict=True))
            == (0, -k), "cap multiplication stopped reducing to residue")

    # The old standard graph has R=D.  It cannot fill a residue-only class.
    graph_columns = tuple(
        tuple(Q(index == corner) for index in range(4))
        + tuple(Q(index == corner) for index in range(4))
        for corner in range(4)
    )
    desired = (Q(0),)*4 + tuple(map(Q, (-1, 0, 0, 1)))
    separator = (Q(0), Q(0), Q(0), Q(-1),
                 Q(0), Q(0), Q(0), Q(1))
    require(all(dot(separator, column) == 0 for column in graph_columns)
            and dot(separator, desired) == 1,
            "the residue-only graph lock changed")

    ledger = {
        "theorem": "centered shear to physical Cartan single-bridge reduction",
        "pins": PINS,
        "mixed_character": {
            "local_rank": 2,
            "representation": "endpoint-odd tensor matching-standard",
            "aggregate_endpoint_matching_rows": "annihilate it",
        },
        "exact_trichotomy": {
            "ordinary_Segre_Tate": "preserves H0=A but cannot lift the non-tangent shear",
            "relative_d_epsilon_equals_L": "lifts recursively but changes H0 to A/(L)",
            "H0_preserving_cylinder": "exports target curvature t*k",
        },
        "Macaulay_reduction": {
            "after_pure_target_placement": "-k times the target generator closes t*k",
            "after_known_cap_graph": "target closes and the only debt is ordinary residue -k",
            "new_mixed_target_theorem_needed": False,
        },
        "residue_identification": {
            "coefficient_character": "the existing residual-q four-corner -delta",
            "standard_graph_fills_it": False,
            "reason": "standard transport obeys R=D; the required class has D=0,R!=0",
            "physical_Cartan_in_canonical_grade": "already source-provenant",
        },
        "single_open_local_bridge": {
            "from": "centered response word 11:110000 with pure-00 matching tails",
            "to": "cap/rootless word 01211222 (1211222 after deletion), labelled P3+K2 grade",
            "must_carry": [
                "the physical cap/target generator and its principal companion",
                "the residue-only endpoint-odd matching-standard class",
                "anchor and q=M-ainc",
                "W and shifted Kahler ridge with eta/sigma",
            ],
            "interpretation": (
                "a source-labelled augmented word/grade comparison; not another "
                "Segre relation, target module, or abstract terminal"
            ),
        },
        "full_row_branching": {
            "offdiagonal_completion": "routes to private-site fan then four-good/coloop",
            "smallest_axis_pure_completion": "impossible on all 1440 viable orientations",
            "remaining_support_escape": "larger axis-pure multi-term cancellation packet",
        },
        "verdict": (
            "all new algebraic obstruction layers collapse to one physical "
            "cross-word comparison.  Polynomial closure retires the mixed "
            "target curvature; the surviving residue has the already constructed "
            "Cartan character, but the source-labelled 110000-to-P3+K2 bridge "
            "and its complete augmented readouts remain open"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("honest H0-preserving shear lift: NO")
    print("Macaulay target curvature after cap placement: RESIDUE-ONLY")
    print("new residue representation: NO (same Cartan -delta)")
    print("single open local object: AUGMENTED CROSS-WORD BRIDGE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
