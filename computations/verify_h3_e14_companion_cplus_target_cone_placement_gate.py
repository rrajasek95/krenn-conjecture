#!/usr/bin/env python3
"""Attempt the generic even Cartan/C+ cone at the E14 companion coordinate.

The h2/h3 C+ package closes its abstract target/Eq triangle.  This checker
grants the strongest possible literal placement of its principal face on the
single dual-visible E14 companion and asks the stronger membership question:
does that one coordinate land the complete twelve-tail E14 target modulo the
269 old complete unary/G11 columns?

It does not.  The old 22-support dual is killed, but a new 42-support dual
annihilates the old columns and the companion unit and still detects the E14
target.  Independently, the reduced-Eq correction cancels the formal Eq face
exactly; its nearest checked physical dressing leaves the known lower/private
and word-resolved residue pair.  Thus the first failure is principal E14
landing, not the sign of the reduced-Eq cone.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py":
        "754038f33ae07329e0fc6a8825df9f1695664a40df91afbb77e52dedb1e1aae1",
    "notes/h3-e14-cplus-keq-companion-assembly-gate.md":
        "8548c1db8ec362fce0876c0f67d77efc96f141ebd4c82b6564069e3a089eff3a",
    "computations/verify_h3_e14_companion_target_normal_specialization_gate.py":
        "310b2f0b6263d0cb41d82050159ee0ae3a68ea4c1c829025dfe0edd9777890f9",
    "notes/h3-e14-companion-target-normal-specialization-gate.md":
        "1e3212ec37de0cbae51cac83f6e109c8dbecbf00c3473c0a9b9fca8bb087cc2d",
    "computations/verify_h3_relative_occurrence_e14_endpoint_word_change_spair_gate.py":
        "5dbdd2d7f005b47317896282f4d4118ccc8433e4979a5aa68eb3367a812989cb",
    "notes/h3-relative-occurrence-e14-endpoint-word-change-spair-gate.md":
        "282c668019009e4363d307b943052ef3d0def2c5749fed1b6ad1d694f30d3678",
    "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py":
        "09ba792f229bb3a1e930b2c59b0de2356b08a7434c648aad9573d8382c652a52",
    "notes/h2-lower-even-cartan-jstar-target-cone-gate.md":
        "2f80cf6fa8d87a9acc4f3441bba5753b9b3c7de5c19e6c709d75969b7eb9d381",
    "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py":
        "9bd2c9f482dc3277d07bd96a4e2189034e766f97e7800d3864179a75e03cef17",
    "notes/h3-cplus-root-even-koszul-physical-dressing-gate.md":
        "c21d7e3e140d2d86d040f9928c787011a7b49e9c58493f812086065c05715e9b",
    "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py":
        "e8014fdfd2263a8eb6bffff11e31c339b5b7965989a61324f8d118a91f791f46",
    "notes/h3-cplus-conditional-physical-dressing-assembly.md":
        "b3afd746e6c275ca23e0b3ee5f26dfbc763301ed7371be4377612709904c19c0",
}
EXPECTED_LEDGER_SHA256 = (
    "8ac9ba66d12df11541b785f0abf1578054aec292dc6dd523c28bad8fbad03e52"
)

ENDPOINT = ("p1_0_1", "s1_1_1")
COMPANION = (ENDPOINT, ("u05_01", "v1301", "v2411"))
CORE = (ENDPOINT, ("u05_01", "v2411", "v3410"))
MATE = (ENDPOINT, ("u05_01", "v2301", "v2411"))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def sparse_pair(dual, vector):
    return sum((coefficient * dual.get(coordinate, Q(0))
                for coordinate, coefficient in vector.items()), Q(0))


def rational_dual(first, pivots, target):
    residual = first.exact_reduce(target, pivots)
    require(residual, "target unexpectedly entered the image")
    free = min(residual)
    dual = {free: Q(1)}
    for leading in sorted(pivots, reverse=True):
        value = sum((coefficient * dual.get(coordinate, Q(0))
                     for coordinate, coefficient in pivots[leading].items()
                     if coordinate != leading), Q(0))
        if value:
            dual[leading] = -value
    return residual, dual


def primitive_pairing(dual, value):
    denominator = math.lcm(*(entry.denominator for entry in dual.values()))
    content = math.gcd(*(
        abs(int(entry * denominator)) for entry in dual.values()
    ))
    return Q(value) * denominator / content


def display_coordinate(coordinate):
    return [list(coordinate[0]), list(coordinate[1])]


def e14_companion_placement_audit():
    special = load(
        "computations/verify_h3_e14_companion_target_normal_specialization_gate.py",
        "e14_cplus_special",
    )
    first, first_ledger, endpoint, target, columns = special.reconstruct()
    require(endpoint == ENDPOINT and len(target) == 12 and len(columns) == 269,
            "canonical E14 packet changed")

    base_pivots = {}
    for column in columns.values():
        first.add_exact_column(column, base_pivots)
    old_residual, old_dual = rational_dual(first, base_pivots, target)
    require(len(base_pivots) == 269 and len(old_dual) == 22
            and sparse_pair(old_dual, target) == -1
            and old_dual.get(COMPANION) == 1,
            "old E14 first-hit obstruction changed")

    # Strongest one-coordinate placement grant: the C+ principal boundary
    # is a literal unit on the dual-visible companion, with all proper rows
    # kept in separate augmented summands below.
    augmented_pivots = {coordinate: dict(column)
                        for coordinate, column in base_pivots.items()}
    require(first.add_exact_column({COMPANION: Q(1)}, augmented_pivots),
            "companion unit unexpectedly belonged to the old image")
    new_residual, new_dual = rational_dual(
        first, augmented_pivots, target)
    require(len(augmented_pivots) == 270
            and len(new_dual) == 42
            and sparse_pair(new_dual, target) == -1
            and new_dual.get(COMPANION, 0) == 0
            and all(sparse_pair(new_dual, column) == 0
                    for column in columns.values()),
            "post-companion E14 dual changed")
    require(new_residual == old_residual
            and old_residual == {
                (ENDPOINT, ("u35_11", "v2411")): Q(1),
                (ENDPOINT, ("u35_11", "v0400", "v2411")): Q(-1),
            }, ("the target residual changed after companion placement",
                old_residual, new_residual))

    contributions = {
        coordinate: coefficient * new_dual.get(coordinate, Q(0))
        for coordinate, coefficient in target.items()
        if coefficient * new_dual.get(coordinate, Q(0))
    }
    require(contributions == {CORE: Q(-1, 4), MATE: Q(-3, 4)}
            and new_dual.get(CORE) == Q(-1, 4)
            and new_dual.get(MATE) == Q(1, 4),
            ("post-companion target pairing did not migrate to core/mate",
             contributions))
    require(primitive_pairing(new_dual, sparse_pair(new_dual, target)) == -60,
            "post-companion primitive target pairing changed")

    # Stronger than testing the selected singleton: modulo the old image the
    # twelve canonical target-tail coordinate classes are independent.  It
    # suffices to omit each one in turn.  If any smaller subset spanned the
    # target, some eleven-element superset would also span it.
    omission_records = []
    for omitted in target:
        pivots = {coordinate: dict(column)
                  for coordinate, column in base_pivots.items()}
        for coordinate in target:
            if coordinate != omitted:
                first.add_exact_column({coordinate: Q(1)}, pivots)
        residual = first.exact_reduce(target, pivots)
        require(len(pivots) == 280 and residual,
                ("eleven target-tail units unexpectedly landed target",
                 omitted, residual))
        omission_records.append({
            "omitted": display_coordinate(omitted),
            "omitted_target_coefficient": str(target[omitted]),
            "rank_old_plus_other_eleven": len(pivots),
            "residual_support": len(residual),
        })
    all_pivots = {coordinate: dict(column)
                  for coordinate, column in base_pivots.items()}
    for coordinate in target:
        first.add_exact_column({coordinate: Q(1)}, all_pivots)
    require(len(all_pivots) == 281
            and not first.exact_reduce(target, all_pivots),
            "all twelve target units stopped spanning the target")

    return {
        "first_ledger": first_ledger["canonical_first_reduction"],
        "old_rank_then_target": [269, 270],
        "old_dual_support_and_pairing": [22, "-1"],
        "granted_principal_placement": display_coordinate(COMPANION),
        "old_dual_on_granted_coordinate": "1",
        "rank_after_grant_then_target": [270, 271],
        "target_residual_unchanged": True,
        "target_residual": [
            [display_coordinate(coordinate), str(coefficient)]
            for coordinate, coefficient in sorted(new_residual.items())
        ],
        "new_dual_support": len(new_dual),
        "new_dual_on_companion": "0",
        "new_dual_on_target": "-1",
        "new_primitive_integral_pairing": "-60",
        "new_nonzero_target_contributions": [
            [display_coordinate(coordinate), str(coefficient)]
            for coordinate, coefficient in sorted(contributions.items())
        ],
        "strict_target_tail_subset_can_land_target": False,
        "target_tail_quotient_rank": 12,
        "eleven_tail_omission_checks": omission_records,
        "consequence": (
            "a C+ face placed only at the dual-visible companion kills the "
            "old 22-support seed but not the E14 target class; the obstruction "
            "rotates to a 42-support seed whose target value is carried by "
            "the decorated core and the u05*v23*v24 mate"
        ),
    }, new_dual


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "vector widths differ")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)


def cplus_target_eq_and_physical_face_audit():
    positive = load(
        "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py",
        "e14_cplus_positive_assembly",
    )
    positive_ledger, positive_digest = positive.audit()
    require(positive_digest == positive.EXPECTED_LEDGER_SHA256
            and positive_ledger["canonical_E14_S_pair"]["exact_identity"]
            == "B_E14=U[000101]*v24_11+R_E14"
            and positive_ledger["conditional_physical_assembly"]
            ["first_row_after_occurrence_placement"]
            == "word-resolved labelled ordinary residue -E",
            "positive E14 Cplus/K_Eq assembly changed")

    even = load(
        "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py",
        "e14_cplus_even",
    )
    even_ledger, even_digest = even.audit()
    require(even_digest == even.EXPECTED_LEDGER_SHA256,
            "h2 even Cartan cone changed")
    principal = even_ledger["first_principal_parts_residual"]
    require(principal["canonical_two_row_projection"]["required_correction"]
            == "+2D*(H0-u)*Eq",
            "reduced-Eq correction sign changed")

    dressing = load(
        "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py",
        "e14_cplus_dressing",
    )
    dressing.pin_inputs()
    physical = dressing.audit()
    require(physical["required_Eq"]
            == "2 D_root (H0-u)e_Eq tensor v"
            and physical["nearest_checked_physical_lift"]["lower_private"]
            == "+E"
            and physical["nearest_checked_physical_lift"]
            ["word_resolved_labelled_ores"] == "-E (nonzero)",
            "root-even physical dressing changed")

    assembly = load(
        "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py",
        "e14_cplus_assembly",
    )
    assembly_ledger, assembly_digest = assembly.audit()
    require(assembly_digest == assembly.EXPECTED_LEDGER_SHA256
            and assembly_ledger["core_assembly"]["assembled_core"]
            ["mixed_target_debt"] == 0,
            "conditional C+ assembly changed")

    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    v = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    e = tuple(2 * root * label for root in d_root for label in v)
    require(len(e) == 24 and sum(value != 0 for value in e) == 8,
            "root-even E packet changed")

    # Row order: principal companion quotient, lower/private, reduced Eq,
    # mixed target normal, word-resolved ordinary residue.
    width = 1 + 4 * len(e)
    lower = slice(1, 1 + len(e))
    eq = slice(lower.stop, lower.stop + len(e))
    target = slice(eq.stop, eq.stop + len(e))
    ores = slice(target.stop, target.stop + len(e))

    def vector(*, principal=0, lower_values=(), eq_values=(),
               target_values=(), ores_values=()):
        answer = [Q(0)] * width
        answer[0] = Q(principal)
        for section, values in ((lower, lower_values), (eq, eq_values),
                                (target, target_values), (ores, ores_values)):
            if values:
                require(len(values) == len(e), "section width")
                answer[section] = values
        return tuple(answer)

    lower_endpoint = vector(target_values=e)
    cplus = vector(principal=1, eq_values=scale(-1, e),
                   target_values=scale(-1, e))
    clean_k_eq = vector(eq_values=e)
    formal_total = add(lower_endpoint, cplus, clean_k_eq)
    require(formal_total == vector(principal=1),
            "formal C+/K_Eq target-Eq triangle stopped closing")

    nearest_physical = vector(lower_values=e, eq_values=e,
                              ores_values=scale(-1, e))
    nearest_total = add(lower_endpoint, cplus, nearest_physical)
    expected_nearest = vector(principal=1, lower_values=e,
                              ores_values=scale(-1, e))
    require(nearest_total == expected_nearest,
            "nearest physical Eq lift residual changed")
    hidden_lower = vector(lower_values=scale(-1, e))
    root_d_even = vector(ores_values=e)
    require(add(nearest_total, hidden_lower, root_d_even)
            == vector(principal=1),
            "conditional hidden/d_even correction stopped closing")

    return {
        "coefficient_packet": {
            "E": "2 D_root tensor v",
            "D_root": [str(value) for value in d_root],
            "v": [str(value) for value in v],
            "nonzero_word_labels": 8,
        },
        "formal_target_Eq_triangle": {
            "lower_endpoint": ["principal 0", "Eq 0", "target +E"],
            "Cplus_Jstar": ["principal companion", "Eq -E", "target -E"],
            "clean_KEq": ["principal 0", "Eq +E", "target 0"],
            "sum": "principal companion only",
            "Eq_face_cancels": True,
            "target_face_cancels": True,
        },
        "nearest_checked_physical_KEq": {
            "boundary": "lower/private +E, Eq +E, ores -E",
            "after_Cplus_and_endpoint": "principal companion + lower E - ores E",
            "Eq_face_cancels": True,
            "first_nonzero_proper_faces": [
                "lower/private +E", "word-resolved labelled ores -E",
            ],
            "nonzero_labels_each": 8,
            "primitive_old_block_detectors": [
                "lower-Eq", "-Eq+W+target-ores",
            ],
        },
        "conditional_full_core_repair": {
            "P2_hidden": "lower/private -E",
            "root_decorated_d_even": "word-resolved ores +E",
            "sum_after_repairs": "principal companion only",
            "constructed_unconditionally": False,
        },
        "interpretation": (
            "the +2D(H0-u)Eq correction has the correct sign and cancels the "
            "formal Eq face.  Its nearest physical lift is not clean, and "
            "even granting the two conditional hidden repairs leaves only "
            "the singleton E14 companion principal face, which the 42-support "
            "post-companion dual kills"
        ),
        "positive_private_return_contrast": {
            "identity": "B_E14=U[000101]*v24_11+R_E14",
            "R_E14": (
                "(p1_0_1*s1_1_1)u35_11*v24_11*(1-v04_00)"
            ),
            "why_not_contradicted": (
                "R_E14 is the full two-term old quotient residual, not the "
                "dual-visible companion unit.  Placing K_Eq on R_E14 and "
                "adding the old unary column produces the entire twelve-tail "
                "target; the singleton experiment proves only that a direct "
                "companion section is insufficient"
            ),
        },
    }


def audit():
    pin_dependencies()
    e14, _new_dual = e14_companion_placement_audit()
    cone = cplus_target_eq_and_physical_face_audit()
    ledger = {
        "theorem": "E14 companion placement of the even Cartan Cplus cone",
        "pins": PINS,
        "E14_principal_placement": e14,
        "Cplus_target_Eq_proper_faces": cone,
        "first_nonzero_residual": {
            "before_granting_hidden_physical_repairs": (
                "the principal E14 target remains independent, detected by "
                "the new 42-support dual; the nearest physical K_Eq lift also "
                "has lower/private +E and word-resolved ores -E"
            ),
            "after_granting_hidden_physical_repairs": (
                "the same principal E14 target remains independent; all "
                "abstract target/Eq/lower/ores faces may cancel without "
                "turning a singleton companion into the twelve-tail target"
            ),
            "next_exact_positive_input": (
                "a source-valid comparison whose E14 principal projection is "
                "the complete twelve-tail unary S-pair remainder modulo the "
                "269 old rows, not a coordinate section at the companion"
            ),
        },
        "verdict": (
            "The generic J*/C+ cone has the correct target and reduced-Eq "
            "signs, but literal placement at only the canonical unary-times-q "
            "companion does not land the E14 target.  It kills the old "
            "22-support seed and exposes a new 42-support seed pairing -1 "
            "with the target through the decorated core and u05*v23*v24 mate. "
            "The physical Eq dressing additionally carries the known hidden "
            "lower/residue pair.  Therefore the cone must be promoted as the "
            "whole twelve-tail unary S-pair comparison, not as one companion."
        ),
        "scope": (
            "Exact canonical chart-(1,1) E14 first-hit module and generic "
            "alpha*beta!=0 C+ coefficient packet.  The all-twelve necessity "
            "is for principal projections supported on the canonical target "
            "tails.  It does not exclude a new comparison with additional "
            "off-target E14 coordinates, nor construct beta=0 or the physical "
            "P2/KEq/d_even hypotheses."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("E14/Cplus placement ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    principal = ledger["E14_principal_placement"]
    print("C+ at E14 companion: OLD 22-DUAL KILLED, TARGET STILL OUTSIDE")
    print("rank old+companion -> +target: 270 -> 271")
    print("new target dual: support 42, pairing -1, primitive -60")
    print("new target support: decorated core + u05*v23*v24 mate")
    print("strict subset of 12 canonical target tails suffices:",
          principal["strict_target_tail_subset_can_land_target"])
    print("+2D(H0-u)Eq: FORMALLY CANCELS")
    print("nearest physical lift: lower/private +E, ores -E (8 labels)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
