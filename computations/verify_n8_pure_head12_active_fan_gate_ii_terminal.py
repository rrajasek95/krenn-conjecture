#!/usr/bin/env python3
"""Route the forced pure head-12 face to the existing active-fan frontier.

The nonlinear SCC chase ends at

    G12 = P1*R*c*e,  word/head 111111:12,

where R=s_2(site 3, physical colour 1).  Restoring endpoint names P=6 and
S=7 identifies R literally with A_{S,3}[2,1].  Thus G12 is the mixed row
obtained from the normalized pure G11 target by changing only endpoint S
from colour 1 to colour 2; P1*c*e is the common hafnian cofactor after
deleting S and 3.

Consequently any complete exact-source closure of G12 is covered by the
target-augmented private-site identity.  Since R is nonzero on the active
chart, it forces a source-provenant active fan.  The pinned h=3 landing then
gives either an existing four-good exit or a literal pure-colour coloop;
finite Hall saturation identifies the latter with the already isolated
Gate-II fan-grade Phi/q packet.  No further G12-specific mate recursion or
new terminal theorem is required.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_pure21_head02_pure_anchor_exit_gate.py":
        "675af0792856e238c81dbd76bb05b6268c1c68b6272acf4e837faba1d3029eb6",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "computations/verify_h3_active_coloop_extra_mate_deletion_or_gate_ii.py":
        "337e739a7392e207c37e9aa5fe0f0900d90c967bb764c981f3f71b2922f7036d",
}
EXPECTED_LEDGER_SHA256 = (
    "49c7a03b6ee9ae876989f2bdf76125634664e4fbf1aa961c9f3c93f5241bbf99"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    path = ROOT / relative
    specification = spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def symbolic_private_site_typing(head) -> dict[str, object]:
    head.install_symbolic_head02(include_r=True)
    algebra = head.B
    pure_word = head.PURE_ONE

    pure = algebra.residual(1, 1, pure_word)
    mixed = algebra.residual(1, 2, pure_word)
    common_cofactor = algebra.product_polynomials((
        algebra.variable("P1"), algebra.variable("c"), algebra.variable("e"),
    ))
    expected_pure = algebra.subtract(
        algebra.multiply(algebra.variable("S1"), common_cofactor),
        algebra.constant(1),
    )
    expected_mixed = algebra.multiply(algebra.variable("R"), common_cofactor)
    require(pure == expected_pure, ("pure G11 row changed", pure))
    require(mixed == expected_mixed, ("mixed G12 row changed", mixed))

    # In the eight-site response presentation the endpoints are P=6,S=7.
    # FIRST[(1,5,1)] is edge 65 with endpoint head/inner colour [1,1].
    # SECOND[(2,3,1)] is edge 73 with [2,1], while SECOND[(1,3,1)]
    # is its pure diagonal mate.  The remaining q edges are 02 and 14.
    require((1, 5, 1) in algebra.FIRST
            and (1, 3, 1) in algebra.SECOND
            and head.R_KEY == (2, 3, 1)
            and (0, 2, 1, 1) in algebra.Q_EDGE
            and (1, 4, 1, 1) in algebra.Q_EDGE,
            "the literal 65|73|02|14 cells changed")
    require(pure_word == (1,) * 6 and head.G12 == (pure_word, 1, 2),
            (pure_word, head.G12))

    # This is the local algebraic shadow of the target-augmented identity:
    # S1*G12 - R*G11 = R.  It records exactly why a complete exact closure
    # with R nonzero must acquire other private-site determinant/cofactor
    # summands; the current sparse packet itself is not claimed exact.
    local_left = algebra.subtract(
        algebra.multiply(algebra.variable("S1"), mixed),
        algebra.multiply(algebra.variable("R"), pure),
    )
    require(local_left == algebra.variable("R"),
            ("local target augmentation lost its unit", local_left))
    head.M.reset_tables()

    return {
        "full_vertex_count": 8,
        "internal_word": "111111",
        "pure_response_head": "11",
        "mixed_response_head": "12",
        "changed_private_site": "S=7",
        "reference_neighbour": 3,
        "pure_colour_a": 1,
        "changed_head_b": 2,
        "diagonal_reference_cell": "S1=A_73[1,1]",
        "offdiagonal_reference_cell": "R=A_73[2,1]",
        "common_cofactor": "P1*c*e",
        "cofactor_matching": "65|02|14",
        "full_fine_matching": "65|73|02|14",
        "operation": "PS",
        "pure_generator": "G11=S1*P1*c*e-1",
        "mixed_generator": "G12=R*P1*c*e",
        "local_augmented_identity": "S1*G12-R*G11=R",
        "typing_verdict": (
            "literal N=8 private-site word pair with (b,a)=(2,1); "
            "not off-grade, diagonal, or a cross-colour untyped minor"
        ),
    }


def normalized_chart_audit(head) -> dict[str, object]:
    head.install_normalized_head02(include_r=True)
    algebra = head.B
    pure_value = head.M.P.evaluate(algebra.residual(1, 1, head.PURE_ONE))
    mixed_value = head.M.P.evaluate(algebra.residual(1, 2, head.PURE_ONE))
    r_value = head.M.P.evaluate(algebra.SECOND[head.R_KEY])
    require((pure_value, mixed_value, r_value) == (0, -1, -1),
            (pure_value, mixed_value, r_value))
    pure_value, mixed_value, r_value = map(
        int, (pure_value, mixed_value, r_value)
    )
    head.M.reset_tables()
    return {
        "G11": pure_value,
        "G12": mixed_value,
        "R": r_value,
        "active_localization": "R is a complex unit",
        "meaning": (
            "the inherited pure target is normalized, while the forced "
            "offdiagonal endpoint cell makes the mixed row nonzero"
        ),
    }


def dependency_route(active, fan, coloop) -> dict[str, object]:
    private_core = active.load(
        "computations/verify_hafnian_private_site_matching_bijection_lemma.py",
        "pure_head12_private_core",
    )
    n8_identity = active.target_augmented_identity(private_core, 8)
    require(n8_identity["exact_source_consequence"]
            == "sum_s Delta_us*C_s=-q_u",
            n8_identity)

    fan_split = fan.audit_ternary_rank_alternative()
    require(fan_split["four_good_assignments"] == 1
            and fan_split["literal_coloop_assignments"] == 26,
            fan_split)

    coloop_ledger, coloop_digest = coloop.audit()
    require(coloop_digest == coloop.EXPECTED_LEDGER_SHA256,
            (coloop_digest, coloop.EXPECTED_LEDGER_SHA256))
    terminal = coloop_ledger["active_terminal_map"]
    require(terminal["four_good"] == "existing transverse landing"
            and terminal["gate_ii_open_datum"]
                == "single missing fan-grade physical Phi/q packet"
            and terminal["after_gate_ii_phi"]
                == "all branches exhaustive; no new termination input",
            terminal)

    return {
        "private_site_identity": n8_identity["source_identity"],
        "exact_source_consequence": n8_identity["exact_source_consequence"],
        "application": (
            "any complete exact-source closure of G12 retaining R!=0 "
            "contains a nonzero determinant/cofactor active-fan summand"
        ),
        "active_fan_split": {
            "neither fan edge a pure coloop": "four-good existing landing",
            "some fan edge a pure-colour coloop":
                "finite Hall saturation to Gate-II Phi/q",
        },
        "gate_ii_open_datum": terminal["gate_ii_open_datum"],
        "after_gate_ii_phi": terminal["after_gate_ii_phi"],
        "new_G12_specific_mate_theorem_needed": False,
        "terminal_scope": (
            "the first nonlinear SCC branch is reduced to existing exits; "
            "this checker does not construct the still-open Gate-II Phi"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    head = load(
        "computations/verify_n8_pure21_head02_pure_anchor_exit_gate.py",
        "pure_head12_source",
    )
    active = load(
        "computations/verify_uniform_target_augmented_private_site_active_minor.py",
        "pure_head12_active_minor",
    )
    fan = load(
        "computations/verify_h3_active_fan_coloop_or_four_good.py",
        "pure_head12_fan_split",
    )
    coloop = load(
        "computations/verify_h3_active_coloop_extra_mate_deletion_or_gate_ii.py",
        "pure_head12_coloop_terminal",
    )

    ledger = {
        "theorem": "n8 forced pure head12 active-fan/Gate-II terminal routing",
        "pins": PINS,
        "literal_private_site_typing": symbolic_private_site_typing(head),
        "normalized_chart": normalized_chart_audit(head),
        "pinned_dependency_route": dependency_route(active, fan, coloop),
        "shortest_branch_map": [
            "exact nonlinear SCC -> private F01",
            "unique J mate -> F02",
            "unique R=A_73[2,1] mate -> pure G12",
            "complete exact G12 closure -> target-augmented private-site active fan",
            "fan non-coloop -> four-good existing landing",
            "fan coloop -> finite Hall saturation -> existing Gate-II Phi/q frontier",
        ],
        "verdict": (
            "G12 is already terminal relative to the pinned proof interface. "
            "It is a literal offdiagonal endpoint cell on the pure-one "
            "target word, so completing its response row enters the existing "
            "active-fan theorem.  Four-good is closed and the only other "
            "outcome is the pre-existing Gate-II Phi/q packet.  Recursing "
            "through G12 mates would duplicate that established reduction."
        ),
        "scope": (
            "canonical h=3 characteristic-zero maximum-anchor/minimum-support "
            "complete five-tensor source, on the active R chart.  No all-h "
            "claim and no construction of Gate II's Phi."
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
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("n=8 pure head12 private-site typing: LITERAL")
    print("complete exact closure: ACTIVE FAN")
    print("fan split: FOUR-GOOD CLOSED / COLOOP TO GATE-II PHI/Q")
    print("new G12 mate recursion: NOT NEEDED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
