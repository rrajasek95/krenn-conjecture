#!/usr/bin/env python3
"""Classify the first PP faces of the augmented-vertex shear collision.

At h=3 the projected shear face C_(a,b) is quartic.  Every one of its
monomials has graph type P3 + 2 K2.  Its labelled first edge-removal faces
split evenly into

    3 K2       (remove one of the two edges through the doubled vertex),
    P3 + K2    (remove one of the two disjoint tail edges).

For P<-0 the latter six faces are the literal SQQ cubics

    s0*q01*q45, s0*q01*q23,
    s0*q01*q35, s0*q01*q24,
    s0*q01*q34, s0*q01*q25.

Thus the collision has a genuine associated-graded P2/AugP2 face, but the
quartic collision is not itself the committed repeated P3+K2 cell.  Nor
does the cofactor topology identify its response word/fine grade with the
canonical cap word, or supply the independent shifted Kahler face.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_chart_unipotent_shear_collision_gate.py":
        "6f05b788400279a8dd19c09acbb1e883eb74c8a9c21f9d00e2bc6a048543922e",
    "notes/uniform-chart-unipotent-shear-collision-gate.md":
        "7fe9e709dd414c101fb1178dc2dee5f5b1d98db0192a525c48cde1e5cfba5a63",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "notes/h2-p2-0112-one-endpoint-hasse-placement-gate.md":
        "5b17afb39c796d79021e0c16fb9e9d0e65c33acc9c7d1b8b6185747bd1450ab5",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
    "computations/verify_h3_centered_pointed_face_existing_conormal_cap_terminal_gate.py":
        "dabaf6c5132f835c6d681d1ecb30611eae8b0920b2c97272e487bcb9c9f068c9",
    "notes/h3-centered-pointed-face-existing-conormal-cap-terminal-gate.md":
        "9f41f22cc232beefca120c770c5815faa2aff0b80c738069cfd18a5c3557fa17",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
    "notes/h3-rootless-zero-anchor-collision-edge-source-obstruction.md":
        "6f5ad0adb20bcfb3c736125f40fedd78f8ec225f28cd43606038c849f32152a7",
}
EXPECTED_LEDGER_SHA256 = (
    "d09ff0f804f569295e4f70d2f1000a4ea8ea9e681ae4e4bff143a0f272df2315"
)

Edge = tuple[int, int]
Monomial = tuple[Edge, ...]


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


def positive_degree_profile(monomial: Monomial) -> tuple[int, ...]:
    degrees: Counter[int] = Counter()
    for left, right in monomial:
        degrees[left] += 1
        degrees[right] += 1
    return tuple(sorted(degrees.values(), reverse=True))


def topology(monomial: Monomial) -> str:
    profile = positive_degree_profile(monomial)
    lookup = {
        (2, 1, 1, 1, 1, 1, 1): "P3+2K2",
        (2, 1, 1, 1, 1): "P3+K2",
        (1, 1, 1, 1, 1, 1): "3K2",
    }
    require(profile in lookup, ("unexpected graph profile", profile, monomial))
    return lookup[profile]


def rank(matrix: tuple[tuple[Q, ...], ...]) -> int:
    work = [list(row) for row in matrix]
    if not work:
        return 0
    rows, columns = len(work), len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * base
                         for entry, base in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def label_edge(value: Edge) -> str:
    names = ("P", "S", "0", "1", "2", "3", "4", "5")
    left, right = (names[value[0]], names[value[1]])
    if left == "P":
        return "p" + right
    if left == "S":
        return "s" + right
    return "q" + left + right


def monomial_label(monomial: Monomial) -> str:
    return "*".join(label_edge(value) for value in monomial)


def collision_face_audit() -> dict[str, object]:
    shear = load(
        "computations/verify_uniform_chart_unipotent_shear_collision_gate.py",
        "shear_collision_for_p3k2",
    )
    shear_ledger, shear_digest = shear.audit()
    require(shear_digest == shear.EXPECTED_LEDGER_SHA256,
            "the pinned shear ledger changed")

    matchings = tuple(shear.perfect_matchings(tuple(range(8))))
    collision = shear.shear_polynomial(matchings, 0, 2)  # P <- physical 0
    require(len(collision) == 45 and set(collision.values()) == {2},
            (len(collision), Counter(collision.values())))
    require({topology(monomial) for monomial in collision} == {"P3+2K2"},
            "a collision top stopped being P3+2K2")

    flagged = []
    for monomial, coefficient in collision.items():
        for removed in monomial:
            remainder = tuple(value for value in monomial if value != removed)
            flagged.append((monomial, removed, remainder, coefficient,
                            topology(remainder)))
    type_count = Counter(item[4] for item in flagged)
    require(len(flagged) == 180
            and type_count == Counter({"3K2": 90, "P3+K2": 90}),
            (len(flagged), type_count))
    require(all(item[3] == 2 for item in flagged),
            "the divided-power collision coefficient changed")
    require(len({item[2] for item in flagged if item[4] == "3K2"}) == 90
            and len({item[2] for item in flagged if item[4] == "P3+K2"}) == 90,
            "two labelled first faces unexpectedly collided")

    # Selected block 2*s0*q01*H2345.
    s0, q01 = shear.edge(1, 2), shear.edge(2, 3)
    tails = tuple(shear.perfect_matchings((4, 5, 6, 7)))
    selected = tuple(tuple(sorted((s0, q01) + tail)) for tail in tails)
    require(all(collision[value] == 2 and topology(value) == "P3+2K2"
                for value in selected), "selected collision block changed")

    selected_p3k2 = []
    selected_3k2 = []
    for monomial in selected:
        for removed in monomial:
            remainder = tuple(value for value in monomial if value != removed)
            record = {
                "top": monomial_label(monomial),
                "removed": label_edge(removed),
                "remainder": monomial_label(remainder),
                "coefficient": 2,
            }
            if topology(remainder) == "P3+K2":
                selected_p3k2.append(record)
                require(removed not in (s0, q01),
                        "a path removal was mislabeled P3+K2")
            else:
                selected_3k2.append(record)
                require(removed in (s0, q01),
                        "a tail removal was mislabeled 3K2")

    expected_p3k2 = {
        "s0*q01*q45", "s0*q01*q23",
        "s0*q01*q35", "s0*q01*q24",
        "s0*q01*q34", "s0*q01*q25",
    }
    require({item["remainder"] for item in selected_p3k2} == expected_p3k2
            and len(selected_3k2) == 6,
            selected_p3k2)
    return {
        "pinned_shear_ledger": shear_digest,
        "collision_top_support": len(collision),
        "collision_top_coefficient": 2,
        "collision_top_topology": "P3+2K2",
        "first_PP_flag_count": len(flagged),
        "first_PP_topology_counts": dict(sorted(type_count.items())),
        "unique_3K2_faces": 90,
        "unique_P3K2_faces": 90,
        "selected_block": "2*s0*q01*H2345",
        "selected_tail_cofactor_P3K2_faces": selected_p3k2,
        "selected_path_cofactor_3K2_faces": selected_3k2,
        "associated_graded_species": (
            "the six tail-removal cubics are literal SQQ P2 species with "
            "one repeated physical site; topology agrees with P3+K2"
        ),
    }


def grade_and_augmented_scope_audit() -> dict[str, object]:
    # These are distinct homogeneous summands in the pinned physical
    # interfaces.  Same site topology is not an identification of summands.
    grades = {
        "collision_top": {
            "source_block": "selected response chart",
            "head_word": "11:110000",
            "operation": "SQQQ",
            "polynomial_degree": 4,
            "site_topology": "P3+2K2",
            "homological_face": "response collision / PP top",
        },
        "collision_tail_cofactor": {
            "source_block": "first PP of selected response collision",
            "head_word": "11:110000",
            "operation": "SQQ with one labelled removed-tail differential",
            "polynomial_degree": 3,
            "site_topology": "P3+K2",
            "homological_face": "response PP1",
        },
        "canonical_augp2_cap": {
            "source_block": "physical augmented P2/cap",
            "head_word": "01211222",
            "operation": "t*q_(v,N)",
            "site_topology": "P3+K2",
            "homological_face": "primitive cap p=(-Q,-ores)",
        },
        "canonical_shifted_ridge": {
            "source_block": "relative Kahler face of AugP2",
            "head_word": "01211222",
            "operation": "gamma_v=-dOmega_v",
            "site_topology": "shifted P3+K2",
            "homological_face": "Kahler degree one; eta/sigma contractions",
        },
    }
    require(grades["collision_top"]["site_topology"] !=
            grades["canonical_augp2_cap"]["site_topology"],
            "quartic collision was accidentally identified with the cap")
    require(grades["collision_tail_cofactor"]["site_topology"] ==
            grades["canonical_augp2_cap"]["site_topology"],
            "the associated-graded topology bridge disappeared")
    require(grades["collision_tail_cofactor"]["head_word"] !=
            grades["canonical_augp2_cap"]["head_word"],
            "the unconstructed cross-word comparison was silently imposed")

    # Primitive grade/readout projections: response word, cap word and
    # shifted-Kahler face are independent direct-sum coordinates.
    response_cofactor = (Q(1), Q(0), Q(0))
    cap = (Q(0), Q(1), Q(0))
    ridge = (Q(0), Q(0), Q(1))
    require(rank((response_cofactor, cap, ridge)) == 3,
            "word/Kahler grade separators lost rank")

    # Even after a physical P3+K2 response edge is reached, the pinned
    # bounded source has a first reduced-Eq obstruction.  Rows are
    # (pure Eq, ainc, W, target, ores).
    r0 = (Q(1), Q(-1), Q(0), Q(1), Q(0))
    target_cap = (Q(0), Q(0), Q(-1), Q(1), Q(0))
    residue_split = (Q(0), Q(0), Q(1), Q(0), Q(1))
    desired_reduced_eq = (Q(-1), Q(0), Q(0), Q(0), Q(0))
    separator = (Q(1), Q(1), Q(0), Q(0), Q(0))
    dot = lambda left, right: sum(a * b for a, b in zip(left, right))
    require(all(dot(separator, value) == 0
                for value in (r0, target_cap, residue_split))
            and dot(separator, desired_reduced_eq) == -1,
            "the pure-Eq+ainc P3+K2 separator changed")
    require(rank((r0, target_cap, residue_split)) == 3
            and rank((r0, target_cap, residue_split,
                      desired_reduced_eq)) == 4,
            "the bounded P3+K2 rank jump changed")
    return {
        "homogeneous_grade_table": grades,
        "grade_separator_rank": 3,
        "exact_mismatch": (
            "C_(P,0) is one polynomial/PP level above P3+K2.  Its six "
            "selected tail cofactors have the correct P2 site topology, "
            "but remain in response head/word 11:110000 rather than the "
            "canonical 01211222 cap summand.  The shifted ridge is a third, "
            "independent Kahler summand"
        ),
        "existing_physical_P3K2_edge_guard": {
            "rows": ["pure Eq", "ainc", "W", "target", "ores"],
            "admitted_rank": 3,
            "rank_with_reduced_Eq_face": 4,
            "primitive_separator": "pure Eq + ainc",
            "meaning": (
                "even after a source map lands the P3+K2 response edge, "
                "the committed literal cell still needs its reduced pure-Eq "
                "descent correction; site topology alone is not a filler"
            ),
        },
        "ridge_scope": (
            "C_ab has no Omega, physical-q, anchor, ridge or eta/sigma "
            "pullback because the augmented-vertex shear already fails on "
            "the response equation.  gamma_v must be supplied as the "
            "independent relative-Kahler face of an enriched comparison"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform shear collision to P3+K2/AugP2 grade gate",
        "pins": PINS,
        "collision_first_faces": collision_face_audit(),
        "physical_grade_scope": grade_and_augmented_scope_audit(),
        "verdict": (
            "The shear collision is not an existing repeated P3+K2 or "
            "shifted-ridge cell.  At h=3 its top is P3+2K2.  Exactly half "
            "of its 180 labelled first PP faces (90 globally, six in the "
            "selected H2345 block) are P3+K2 SQQ/P2 cofactors.  This is an "
            "associated-graded bridge only: response word/fine placement, "
            "the reduced-Eq correction, and the shifted Kahler face remain "
            "independent physical data."
        ),
        "shortest_positive_theorem": (
            "construct one source-labelled Hasse/Spencer collision top whose "
            "boundary contains all six selected P3+K2 tail cofactors and six "
            "3K2 path cofactors, then give an augmented cross-word P2 map "
            "from the former to 01211222/t*q_(v,N), including the known "
            "reduced-Eq correction and the independent gamma=-dOmega face"
        ),
        "scope": (
            "exact complete h3 C_(P,0) collision packet and its labelled "
            "first PP faces, with physical word/fine/readout scope pinned to "
            "the canonical AugP2 and repeated-site obstruction interfaces. "
            "This does not construct the cross-word map or an all-resolution "
            "no-go."
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
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    counts = ledger["collision_first_faces"]["first_PP_topology_counts"]
    print("h3 collision top: P3+2K2 (45 monomials, coefficient 2)")
    print("first PP flags: " + repr(counts))
    print("selected P3+K2 tail cofactors: 6 literal SQQ/P2 faces")
    print("physical identification: NO (word/reduced-Eq/Kahler faces remain)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
