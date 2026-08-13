#!/usr/bin/env python3
"""Audit the first toric conormal of the universal response KS shear.

The four occurrence coordinates in one endpoint/matching rectangle are

    x=u_(01;24|35), y=u_(10;23|45),
    z=u_(01;23|45), w=u_(10;24|35).

Physical factorization gives ``xy-zw=0``.  The constant occurrence shear
``(1,1,1,1)`` is detected by the conormal with value

    (p1*s0-p0*s1)*(q23*q45-q24*q35).

This checker distinguishes that proper face from the scalar KS face 90*f
and freezes the exact active-fan/coloop scope.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py":
        "39713f3683dd3d2376e5a911987ee3670ec291cf850072d6b4932e7a93745fc7",
    "notes/h3-universal-response-deformation-e14-orbit-ks-gate.md":
        "d9032c365e8fd8fb5baf320dcc5adac8832c023119fb7d4df69d02cce3d5878f",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
    "computations/verify_h3_common_tail_pair_cut_determinant_split.py":
        "e0987e07dbb95a58a8d5e9c8c10b8302701e9fac9a258745520faa9e509022b7",
    "notes/h3-common-tail-pair-cut-determinant-split.md":
        "44422dc4966c4cf7885e8c4c9f3dff469201cb13fd366fdbd6d6c2e7b49f5e5d",
    "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py":
        "c0a34736979eb8a5d059dce30224b3d22f3930e9afaf07916dbbf51b3539c15d",
    "notes/h3-order2-promoted-occurrence-orientation-gate.md":
        "5a4f015c519421d4df2cff2c267f4cee00b6f8e35435ad97323f453831305edb",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "notes/h3-centered-occurrence-same-grade-physical-gate.md":
        "b183f3b5dab83fa79d17c3f539b9f146e3be176a96bfe52b267529148b64134a",
    "computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py":
        "a51b8f091a25624d17443c70ac70b60eb257c8b11dafb0b9ad3f17962dc07390",
    "notes/h3-trapped-hessian-to-six-term-endpoint-polarization-gate.md":
        "45d4d6604a58da20bec8aa87cb9522b658e2454a939533075d6e8d607ed895b8",
}
EXPECTED_LEDGER_SHA256 = (
    "82e6fd5666464fa1c49e6d518a54e414248112465f558158ab996070a43bd336"
)
SITES = tuple(range(6))
N = 90


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def toric_conormal_audit() -> dict[str, object]:
    samples = 0
    bright = 0
    for e01 in map(Q, range(-2, 3)):
        for e10 in map(Q, range(-2, 3)):
            for q_a in map(Q, range(-2, 3)):
                for q_b in map(Q, range(-2, 3)):
                    # Order (x,y,z,w) matches the displayed toric minor.
                    x = e01 * q_b
                    y = e10 * q_a
                    z = e01 * q_a
                    w = e10 * q_b
                    gradient = (y, x, -w, -z)
                    tangent_columns = (
                        (q_b, Q(0), q_a, Q(0)),
                        (Q(0), q_a, Q(0), q_b),
                        (Q(0), e10, e01, Q(0)),
                        (e01, Q(0), Q(0), e10),
                    )
                    require(x * y - z * w == 0
                            and all(dot(gradient, column) == 0
                                    for column in tangent_columns),
                            ("physical Segre tangent changed",
                             e01, e10, q_a, q_b))
                    shear_value = dot(gradient, (1, 1, 1, 1))
                    factored = (e10 - e01) * (q_a - q_b)
                    require(shear_value == factored,
                            ("constant shear factorization changed",
                             shear_value, factored))
                    samples += 1
                    bright += bool(shear_value)
    require(samples == 625 and bright == 400,
            ("small-grid conormal census changed", samples, bright))
    return {
        "occurrence_order": [
            "u_(01;24|35)", "u_(10;23|45)",
            "u_(01;23|45)", "u_(10;24|35)",
        ],
        "toric_minor": "x*y-z*w=0",
        "physical_composite_coordinates": [
            "e01=p0*s1", "e10=p1*s0",
            "qA=q23*q45", "qB=q24*q35",
        ],
        "conormal_kills_all_factor_tangents": True,
        "constant_shear": [1, 1, 1, 1],
        "constant_shear_value": "(p1*s0-p0*s1)*(q23*q45-q24*q35)",
        "same_response_head_and_word": "11:110000",
        "same_fine_multidegree": True,
        "grid_samples": samples,
        "grid_nonzero_shear_values": bright,
    }


def scalar_independence_audit() -> dict[str, object]:
    # Normalize the marked occurrence f=e01*qA to one.  The scalar KS face
    # stays 90 while the toric conormal can vanish or be nonzero.
    records = []
    for e10, q_b in ((Q(1), Q(0)), (Q(0), Q(0)), (Q(3), Q(0))):
        e01 = q_a = Q(1)
        scalar = N * e01 * q_a
        toric = (e10 - e01) * (q_a - q_b)
        records.append({
            "e01": str(e01), "e10": str(e10),
            "qA": str(q_a), "qB": str(q_b),
            "90f": str(scalar), "toric_conormal": str(toric),
        })
    require([record["90f"] for record in records] == ["90"] * 3
            and [record["toric_conormal"] for record in records]
                == ["0", "-1", "2"],
            ("scalar/toric independence guard changed", records))
    return {
        "normalized_marked_occurrence": "f=(p0*s1)(q23*q45)=1",
        "records": records,
        "toric_conormal_equals_scalar_90f": False,
        "logical_relation": "independent proper faces of a physical lift",
    }


def support_completion_audit() -> dict[str, object]:
    matchings = tuple(perfect_matchings(SITES))
    require(len(matchings) == 15, "K6 matching count changed")
    e = (2, 3)
    f = (2, 4)

    def rank_at(edge, families) -> int:
        return sum(any(edge not in matching for matching in family)
                   for family in families)

    edges = tuple(combinations(SITES, 2))
    dense_values = {edge: Q(1) for edge in edges}
    dense_values[(3, 5)] = Q(2)
    sparse_values = {edge: Q(0) for edge in edges}
    sparse_values.update({
        (2, 3): Q(1), (4, 5): Q(1),
        (2, 4): Q(1), (3, 5): Q(2),
        (0, 5): Q(1), (1, 4): Q(1),
    })

    def support(values):
        return tuple(matching for matching in matchings
                     if all(values[edge] for edge in matching))

    dense_support = support(dense_values)
    sparse_support = support(sparse_values)
    coloop_matching = ((0, 5), (1, 4), (2, 3))
    require(dense_support == matchings
            and sparse_support == (coloop_matching,),
            ("literal pure-support completions changed",
             dense_support, sparse_support))
    all_support = (dense_support,) * 3
    coloop_support = (sparse_support, dense_support, dense_support)
    require(rank_at(e, all_support) == rank_at(f, all_support) == 3
            and rank_at(e, coloop_support) == 2
            and rank_at(f, coloop_support) == 3,
            "pure-support completion fork changed")

    # Both completions may be paired with the same nonzero local toric data.
    # The displayed q cells all have decoration 00, so the off-diagonal
    # reference hypothesis of the private-site fan theorem is absent.
    e01, e10, q_a, q_b = map(Q, (1, 0, 1, 2))
    toric = (e10 - e01) * (q_a - q_b)
    require(toric == 1, "nonzero toric guard changed")
    return {
        "common_local_toric_data": {
            "e01": 1, "e10": 0, "qA": 1, "qB": 2,
            "toric_conormal": 1,
            "tail_decorations": "q23:00,q45:00,q24:00,q35:00",
        },
        "completion_without_pure_coloop": {
            "colour_zero_cells": (
                "all fifteen edges nonzero, with q35=2 and the rest 1"
            ),
            "pure_supports": "all fifteen K6 matchings in every colour",
            "deleted_star_ranks_if_an_active_fan_were_supplied": [3, 3],
        },
        "completion_with_pure_coloop": {
            "colour_zero_nonzero_cells": [
                "23", "45", "24", "35", "05", "14",
            ],
            "colour_zero_support": "{05|14|23}",
            "colour_zero_coloop": "23",
            "deleted_star_ranks_on_23_24": [2, 3],
        },
        "offdiagonal_private_site_reference_supplied": False,
        "toric_brightness_selects_four_good_or_coloop_branch": False,
        "scope": (
            "exact pure-support/readout completions, not asserted complete "
            "GHZ sources; they prove the branch is not chosen by the toric "
            "factor alone"
        ),
    }


def landing_scope_audit() -> dict[str, object]:
    return {
        "endpoint_factor": "p1*s0-p0*s1",
        "endpoint_factor_existing_interface": (
            "endpoint-odd orientation/KS line; not by itself a physical "
            "deleted-star head"
        ),
        "tail_factor": "q23*q45-q24*q35",
        "tail_factor_existing_interface": (
            "evaluated residual C4/common-tail Fitting carrier"
        ),
        "new_positive_information": (
            "the shear failure is block-local, same-word and decomposable, "
            "so it supplies the shape requested by the curvature shortcut"
        ),
        "missing_active_landing_data": [
            "a nonzero offdiagonal physical reference cell",
            "complete pure-support deleted-star ranks or a literal coloop",
            "cofactor/common-q and protected augmented source placement",
        ],
        "actual_first_order_source_tangent": (
            "nonzero conormal value excludes the constant shear"
        ),
        "relative_KS_or_PP_cell": (
            "the conormal becomes a compulsory proper face, not an "
            "automatic terminal"
        ),
        "terminal_promotion_requires": (
            "extend the conormal across the complete word/fine/repeated, "
            "target, ainc/q, W, ridge and eta/sigma comparison"
        ),
        "shortest_alternative": (
            "cancel every endpoint/matching toric conormal in one protected "
            "KS/PP totalization, or promote the first surviving fully "
            "augmented conormal to the accepted physical terminal"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 universal-response toric-minor terminal gate",
        "pins": PINS,
        "toric_conormal": toric_conormal_audit(),
        "scalar_independence": scalar_independence_audit(),
        "pure_support_completion_fork": support_completion_audit(),
        "landing_scope": landing_scope_audit(),
        "verdict": (
            "The first endpoint/matching Segre minor is a genuine physical "
            "conormal.  It kills every factor tangent and reads the constant "
            "four-occurrence shear by the exact product "
            "(p1*s0-p0*s1)(q23*q45-q24*q35).  This is independent of the "
            "scalar KS face 90f.  A nonzero value supplies the missing "
            "same-word decomposable curvature shape, but does not choose "
            "four-good versus coloop and supplies no offdiagonal private-site "
            "reference.  It blocks an honest tangent lift; in a higher "
            "KS/PP comparison it is a required proper face whose augmented "
            "cancellation or terminal extension remains open."
        ),
        "scope": (
            "canonical h=3 four-occurrence rectangle in response head/word "
            "11:110000.  The conormal and support completions are exact.  "
            "No complete GHZ source counterexample, active-fan landing, or "
            "fully typed Fredholm terminal is claimed."
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
    print("toric conormal: PHYSICAL AND DECOMPOSABLE")
    print("constant shear tangent: NO WHEN PRODUCT NONZERO")
    print("toric face equals scalar 90f: NO")
    print("four-good/coloop branch selected: NO")
    print("higher KS/PP landing: PROPER FACE OR AUGMENTED TERMINAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
