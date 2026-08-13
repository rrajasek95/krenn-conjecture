#!/usr/bin/env python3
"""Audit common-core cancellation for the generic symmetric h=3 C4 face.

The E2/E3/E4 square gives undivided, source-labelled C4 transport.  On the
three local matching occurrences its E2 boundaries give the two standard
differences, while the complete response face gives their symmetric sum.
All three carry the common occurrence core g.

If the *entire physically typed common core* is a unit, multiplication by
its inverse cancels g without a denominator.  The sum and the two E2
differences then isolate every local matching occurrence over characteristic
zero; E3/E4 provide path coherence.  The active-coloop equation q_e*C_e=1
proves this only when g is literally q_e.  It does not cancel an additional
H2 direction/reinsertion or one-sided endpoint-pivot factor.

The selected pure-trapped hypotheses do not prove that literal identification.
They also include 14 DQ grades whose Q edge is not e and 30 PS grades whose
common occurrence head is p_u*s_v.  Modulo the augmentation-zero plane, the
exact first source gate is

    R*u --g--> R*u.

Its primitive colon is ((g*u):g)/(g*u) = (R/(g))*u, and after base change to
g=0 its H1 is the same one-dimensional Tor line.  The average local dual
detects it and 4373ae6 supplies the target/W/ores/ridge augmented extension
after a same-grade physical placement.  Thus the C4 square gives an exact
unit-or-colon theorem, but current typing does not retire U_C4 merely from the
active-coloop normalization.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py":
        "ecb8725715747c3270fb069545309283d1890fbac6e66dfb6ed2f53b609e0030",
    "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py":
        "026eb42fac96e2c21e6466f51322a18d45d975bcf5f48e0dc33f9cfa740d8d41",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "notes/h3-active-fan-coloop-complete-row-pivot.md":
        "2a68b7a9da9c61c67c4f63e666a6cbb1023344722943b9042f2ff15b2863e92e",
    "computations/verify_local_c4_relative_coherence_curvature_square.py":
        "9753c669db38b29e55706d4d8865c3beb46dcb0835298a90061babcda6483744",
    "notes/local-c4-coherence-curvature-relative-square.md":
        "5ed2232758948b993826d69158f6cdb57a06c077ad3a37af7db3a5005d9b9b43",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "computations/verify_c4_excess_tor_terminal_readout_boundary.py":
        "03d10fb2a59334f0b8321f9a877792768ee15622b49a9b57c136188b26ae0968",
}
EXPECTED_LEDGER_SHA256 = (
    "1459d3ba5d21d11802a5f05e0e730d86fd67a06c8e22484b5c062ae111c05aea"
)

S = (Q(1), Q(1), Q(1))
D01 = (Q(1), Q(-1), Q(0))
D12 = (Q(0), Q(1), Q(-1))
EPSILON = (Q(1, 3), Q(1, 3), Q(1, 3))
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def local_c4_linear_audit() -> dict[str, object]:
    # E2 supplies the two path differences and the response/H2 row supplies
    # the symmetric aggregate.  Their inverse formulas isolate each literal
    # matching occurrence.  E3/E4 are coherence relations among the E2 paths;
    # their boundaries remain in the augmentation-zero plane.
    e0 = scale(Q(1, 3), add(S, scale(2, D01), D12))
    e1 = scale(Q(1, 3), add(S, scale(-1, D01), D12))
    e2 = scale(Q(1, 3), add(S, scale(-1, D01), scale(-2, D12)))
    require((e0, e1, e2) == (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    ), (e0, e1, e2))
    require(rank((D01, D12)) == 2
            and rank((D01, D12, S)) == 3
            and dot(EPSILON, S) == 1
            and dot(EPSILON, D01) == dot(EPSILON, D12) == 0,
            "the local C4 standard/trivial split changed")
    return {
        "local_occurrences": ["23|45", "24|35", "25|34"],
        "E2_standard_boundaries": [
            [str(value) for value in D01],
            [str(value) for value in D12],
        ],
        "complete_response_symmetric_face": [str(value) for value in S],
        "inverse_formulas": {
            "m0": "(s+2*d01+d12)/3",
            "m1": "(s-d01+d12)/3",
            "m2": "(s-d01-2*d12)/3",
        },
        "E3_E4_role": (
            "Bianchi/path coherence for the E2 transports; no new invariant "
            "augmentation-one boundary is created"
        ),
        "curvature_split": {
            "Delta_nonzero": (
                "the undivided E2 boundary exposes the literal curved "
                "common-q carrier and leaves the generic-flat branch"
            ),
            "Delta_zero": (
                "the two E2 transports are flat; common-core saturation is "
                "then the first remaining source gate"
            ),
        },
        "primitive_average_dual": [str(value) for value in EPSILON],
    }


def core_orbit_audit() -> dict[str, object]:
    sites = range(6)
    q_edges = tuple(combinations(sites, 2))
    active_coloop = (0, 1)
    aligned = tuple(edge for edge in q_edges if edge == active_coloop)
    unaligned = tuple(edge for edge in q_edges if edge != active_coloop)
    ps_pairs = tuple((p_site, s_site) for p_site in sites for s_site in sites
                     if p_site != s_site)
    require(len(q_edges) == 15 and len(aligned) == 1 and len(unaligned) == 14
            and len(ps_pairs) == 30,
            (q_edges, aligned, unaligned, ps_pairs))

    # Literal local guards.  In the unaligned DQ packet the active coloop is
    # q01=1 but the common edge q02 may vanish, while the residual K4 tail on
    # 1,3,4,5 is fully symmetric and nonzero.  In the PS packet the endpoint
    # core p0*s1 may vanish while the residual K4 tail is again nonzero.
    dq_values = {
        "q01_active_coloop": Q(1), "q02_common_core": Q(0),
        "q13": Q(1), "q45": Q(1),
        "q14": Q(1), "q35": Q(1),
        "q15": Q(1), "q34": Q(1),
    }
    dq_tail = (dq_values["q13"] * dq_values["q45"]
               + dq_values["q14"] * dq_values["q35"]
               + dq_values["q15"] * dq_values["q34"])
    ps_values = {
        "q01_active_coloop": Q(1), "p0": Q(0), "s1": Q(0),
        "q23": Q(1), "q45": Q(1),
        "q24": Q(1), "q35": Q(1),
        "q25": Q(1), "q34": Q(1),
    }
    ps_tail = (ps_values["q23"] * ps_values["q45"]
               + ps_values["q24"] * ps_values["q35"]
               + ps_values["q25"] * ps_values["q34"])
    require(dq_values["q02_common_core"] == 0 and dq_tail == 3
            and ps_values["p0"] * ps_values["s1"] == 0 and ps_tail == 3,
            (dq_values, dq_tail, ps_values, ps_tail))

    return {
        "active_coloop_edge": list(active_coloop),
        "DQ_grades": {
            "total": len(q_edges),
            "coloop_aligned": len(aligned),
            "not_forced_unit": len(unaligned),
            "visible_common_matching_factor": "q_uv",
            "full_physical_core": (
                "q_uv times any retained H2 direction/reinsertion and "
                "one-sided pivot factors"
            ),
        },
        "PS_grades": {
            "total": len(ps_pairs),
            "coloop_aligned": 0,
            "not_forced_unit": len(ps_pairs),
            "visible_common_occurrence_factor": "p_u*s_v",
            "full_physical_core": (
                "p_u*s_v times any retained H2 reinsertion/pivot factors"
            ),
        },
        "literal_nonunit_guards": {
            "unaligned_DQ": {
                "active_coloop_q01": "1",
                "common_core_q02": "0",
                "symmetric_tail_on_1345": str(dq_tail),
            },
            "PS": {
                "active_coloop_q01": "1",
                "common_core_p0s1": "0",
                "symmetric_tail_on_2345": str(ps_tail),
            },
        },
        "scope": (
            "exact local H2-grade evaluations, not standalone complete GHZ "
            "sources; they prove that the selected pure-trapped and active-"
            "coloop hypotheses alone do not imply that every C4 core is a "
            "unit.  Even in the aligned DQ label, q_e*C_e=1 cancels only the "
            "q_e factor unless the remaining grade/pivot core is proved trivial"
        ),
    }


def conditional_unit_construction_audit() -> dict[str, object]:
    # If the full core g has an inverse c_g in the physically typed source
    # quotient, the construction is exact.  The numerical values merely
    # audit the algebra.  The source theorem still has to identify c_g with
    # an actual same-grade physical cofactor; q_e*C_e=1 is sufficient only
    # after proving g=q_e (not q_e times a retained pivot).
    g = Q(2)
    c_g = Q(1, 2)
    require(g * c_g == 1, "the common-core inverse changed")
    undivided = tuple(scale(g, vector) for vector in (S, D01, D12))
    primitive = tuple(scale(c_g, vector) for vector in undivided)
    require(primitive == (S, D01, D12),
            ("coloop cancellation stopped being exact", primitive))
    isolated = (
        scale(Q(1, 3), add(primitive[0], scale(2, primitive[1]), primitive[2])),
        scale(Q(1, 3), add(primitive[0], scale(-1, primitive[1]), primitive[2])),
        scale(Q(1, 3), add(primitive[0], scale(-1, primitive[1]),
                          scale(-2, primitive[2]))),
    )
    require(isolated == (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    ), isolated)
    return {
        "hypothesis": "the entire physically typed common core g is a unit",
        "unit_relation": "g*c_g=1 in the same word/fine/direction-pair grade",
        "cancellation": "c_g*(g*s,g*d01,g*d12)=(s,d01,d12)",
        "constructed_local_columns": ["m0", "m1", "m2"],
        "denominator_or_localization_symbol_added": False,
        "source_saturation_under_the_unit_hypothesis": "PROVED",
        "coherence": "E3/E4 make the E2 path choices compatible",
        "active_coloop_specialization": {
            "known": "q_e*C_e=1",
            "sufficient_if": "g is literally q_e in the full physical grade",
            "not_currently_proved": (
                "that no H2 direction/reinsertion or endpoint-pivot factor "
                "remains in g"
            ),
        },
        "unconditional_construction_status": "OPEN",
    }


def colon_tor_audit() -> dict[str, object]:
    # Let R=k[g], M=R^3 on the three occurrence tags.  The undivided response
    # and E2 columns are g*s,g*d01,g*d12.  Since (s,d01,d12) is a basis, their
    # image is exactly gM.  Thus (gM:g)/gM=M/gM has raw rank three.  After
    # quotienting the standard plane (the strongest same-grade difference
    # grant), it is the single invariant line R/(g)*u.
    require(rank((S, D01, D12)) == 3,
            "undivided local columns stopped generating gM")

    # The Koszul differential multiplication by g becomes zero on the fibre
    # g=0.  Record it as a 1x1 matrix on the invariant quotient.
    generic_differential = (("g",),)
    fibre_differential = ((Q(0),),)
    fibre_h1_dimension = 1 - rank(((Q(0),),))
    require(generic_differential == (("g",),)
            and fibre_differential == ((Q(0),),)
            and fibre_h1_dimension == 1,
            "the invariant Koszul/Tor line changed")

    # The average dual selects the invariant class and kills both E2 paths.
    require(dot(EPSILON, S) == 1
            and dot(EPSILON, D01) == dot(EPSILON, D12) == 0,
            "the colon detector changed")
    return {
        "branch": "the surviving Delta=0 symmetric/flat C4 packet",
        "raw_local_module": "M=R^3, R=k[g] in the selected word/fine grade",
        "undivided_image": "g*M generated by g*s,g*d01,g*d12",
        "raw_colon": "(g*M:g)/(g*M)=M/g*M, rank 3 over k on g=0",
        "invariant_quotient": {
            "module": "R*u, u=s/3 after the standard E2 plane",
            "differential": "multiplication by g",
            "colon": "((g*u):g)/(g*u)=(R/(g))*u",
            "Tor1_on_g_zero": "(R/(g))*u",
            "dimension": fibre_h1_dimension,
        },
        "primitive_dual": [str(value) for value in EPSILON],
        "primitive_dual_value": "1 on s, 0 on every E2/E3/E4 standard boundary",
        "first_missing_source_column": (
            "a degree-one relative/excess generator tau_C4 with "
            "d(tau_C4)=g*u, or an independent full-source column killing "
            "the class of u in (im d:g)/im d"
        ),
        "finite_membership_test": (
            "u belongs to the saturated physical boundary module iff its "
            "class vanishes in (im d:g)/im d in the literal augmented grade"
        ),
        "E3_E4_non_effect": (
            "they are syzygies/coherences among E2 paths and project to zero "
            "on the invariant quotient; d^2=0 does not kill this H1"
        ),
    }


def augmented_promotion_audit() -> dict[str, object]:
    # Replay the 4373ae6 formula symbolically on three representative cap
    # packets.  The four cap-corner coordinates are distinct from the three
    # C4 occurrences and from the six pure tail columns.
    samples = {}
    for name, mu in {
        "zero": (Q(0), Q(0), Q(0), Q(0)),
        "one_cap_corner": (Q(1), Q(0), Q(0), Q(0)),
        "Cartan_alpha": ALPHA,
    }.items():
        alpha_mu = dot(ALPHA, mu)
        samples[name] = {
            "mu": [str(value) for value in mu],
            "target": [str(-value) for value in mu],
            "W": [str(-value) for value in mu],
            "ores": [str(value) for value in mu],
            "ridge": str(-alpha_mu),
            "q_ainc_Eq": 0,
        }
    require(samples["one_cap_corner"]["ridge"] == "1",
            "the 4373ae6 cap-corner sign changed")
    return {
        "local_detector": "epsilon=(1,1,1)/3 on the C4 occurrence tags",
        "4373ae6_extension": (
            "for induced cap values mu_j: target_j=W_j=-mu_j, "
            "ores_j=mu_j, ridge=-alpha.mu, q=ainc=Eq=0"
        ),
        "verified_samples": samples,
        "post_placement_fork": [
            "colon class in exhaustive physical image -> protected relative filler/generator",
            "colon class outside image -> augmented terminal extending epsilon",
        ],
        "third_branch": False,
        "scope_guard": (
            "the formula promotes the colon dual only after the actual "
            "source-labelled cap placement; the local quotient guard is not "
            "itself called a physical terminal"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 generic symmetric C4 core saturation / Tor gate",
        "pins": PINS,
        "local_C4_square": local_c4_linear_audit(),
        "common_core_orbits": core_orbit_audit(),
        "conditional_unit_construction": conditional_unit_construction_audit(),
        "nonunit_core_colon": colon_tor_audit(),
        "augmented_terminal_promotion": augmented_promotion_audit(),
        "verdict": (
            "The E2/E3/E4 square proves a sharp unit-or-colon theorem.  If "
            "the entire physically typed common core g is a unit, the "
            "symmetric row plus two E2 paths isolate all three occurrences. "
            "The active-coloop relation only proves q_e is a unit; current "
            "typing does not prove that g has no extra H2 reinsertion/pivot "
            "factor.  Fourteen unaligned DQ grades and thirty PS grades also "
            "have no forced unit core.  The first exact source gate is the "
            "invariant colon/Tor line (R/(g))*u.  The primitive average dual "
            "detects it, and after same-grade placement 4373ae6 gives the "
            "exhaustive filler-or-augmented-terminal alternative."
        ),
        "frontier": {
            "retired": "no full physical grade unconditionally",
            "conditional_positive": (
                "U_C4 is explicit once g*c_g=1 is proved in the same grade"
            ),
            "remaining": (
                "prove the complete aligned core equals the coloop unit, or "
                "construct one tail-covariant excess/relative generator for "
                "the invariant colon line and apply the 4373ae6 fork"
            ),
        },
        "nonclaims": [
            "E3/E4 coherence is not called primitive saturation",
            "the active coloop q_e is not identified with every varied q_uv or endpoint head p_u*s_v",
            "the local nonunit evaluation is not called a complete GHZ source",
            "the coefficient colon dual is not called physical before augmented placement",
        ],
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
    print("full common core unit: EXPLICIT C4 CONSTRUCTION")
    print("active coloop alone -> full core unit: NOT PROVED")
    print("first obstruction: ONE INVARIANT COLON/TOR LINE")
    print("after physical placement: FILLER OR 4373ae6 TERMINAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
