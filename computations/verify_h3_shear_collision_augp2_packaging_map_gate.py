#!/usr/bin/env python3
"""Audit a literal map from shear-collision cofactors to AugP2.

The six selected P3+K2 cofactors have the right undecorated SQQ/P2 graph,
but are response-word monomials in 11:110000.  Decorating the same six
under the AugP2 word 01211222 changes every fine degree.  The cap word is
also outside the existing 110000->111111 D4 response cube.  Hence the
committed objects supply no literal degree-preserving map.

After adjoining a word-changing arrow, the collision cofactors can supply
only the hidden lower/P2 coordinate.  They do not fill the primitive mixed
mapping-square incidence, the reduced-Eq/cap faces, or the independent
shifted-Kahler gamma face.  The current AugP2 result is therefore a
conditional multi-face schema, not an already constructed source object
that absorbs C_(a,b).
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
    "computations/verify_uniform_shear_collision_p3k2_augp2_grade_gate.py":
        "a68dd835badb415454ed43186a68c82ee5f699eb118b0575014babf728a7c2bf",
    "notes/uniform-shear-collision-p3k2-augp2-grade-gate.md":
        "d2968439dbc821510cf254c06a580b5205da53668ffd666fb54f6f9f9d7c204d",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
    "notes/h3-e14-pointed-orbit-keq-mapping-cylinder-gate.md":
        "f5008f5b7e892b5ce5270faacee4ec9f2bffc2630b8dd15a55cb8f5c6800cb21",
    "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py":
        "42bf68eeb963d568d1c8d9156d4176bec31a114b6fe804744833364fe3633475",
    "notes/h3-e14-cap-graph-two-parameter-flat-transport-gate.md":
        "61c093eed30cd2fff1be086e6069d344e76a583ee31f93528a31aebe76c5c5d6",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
}
EXPECTED_LEDGER_SHA256 = (
    "9095b2120fd787af031e4f830bfe3a42a838bb253e91290381e9823c700b4fec"
)

Edge = tuple[int, int]


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


NAMES = ("P", "S", "0", "1", "2", "3", "4", "5")
EDGE_SITES = {
    "s0": (1, 2),
    "q01": (2, 3),
    "q23": (4, 5),
    "q24": (4, 6),
    "q25": (4, 7),
    "q34": (5, 6),
    "q35": (5, 7),
    "q45": (6, 7),
}


def decorated_factor(label: str, word: tuple[int, ...]) -> str:
    left, right = EDGE_SITES[label]
    return f"{label}^{word[left]}{word[right]}"


def fine_degree(labels: tuple[str, ...], word: tuple[int, ...]) -> tuple[int, ...]:
    answer = Counter()
    for label in labels:
        for site in EDGE_SITES[label]:
            answer[(site, word[site])] += 1
    return tuple(answer[(site, colour)]
                 for site in range(8) for colour in range(3))


def word_and_fine_grade_audit() -> dict[str, object]:
    # 11:110000 means endpoint head 11 followed by residual word 110000.
    response_word = tuple(map(int, "11110000"))
    cap_word = tuple(map(int, "01211222"))
    require(len(response_word) == len(cap_word) == 8,
            "the canonical words stopped having eight sites")
    differing_sites = tuple(index for index, values in enumerate(
        zip(response_word, cap_word)) if values[0] != values[1])
    require(differing_sites == (0, 2, 4, 5, 6, 7), differing_sites)

    selected_faces = (
        ("s0", "q01", "q45"),
        ("s0", "q01", "q23"),
        ("s0", "q01", "q35"),
        ("s0", "q01", "q24"),
        ("s0", "q01", "q34"),
        ("s0", "q01", "q25"),
    )
    rows = []
    for labels in selected_faces:
        response_decorated = tuple(decorated_factor(label, response_word)
                                   for label in labels)
        cap_decorated = tuple(decorated_factor(label, cap_word)
                              for label in labels)
        response_fine = fine_degree(labels, response_word)
        cap_fine = fine_degree(labels, cap_word)
        require(response_decorated != cap_decorated
                and response_fine != cap_fine,
                (labels, response_decorated, cap_decorated))
        rows.append({
            "undecorated": "*".join(labels),
            "response_11_110000": "*".join(response_decorated),
            "cap_01211222": "*".join(cap_decorated),
            "fine_degrees_equal": False,
        })

    # Existing response D4 root cube changes only the last four residual
    # zeroes to zero/one, retaining the full prefix 11:11.
    d4_words = set()
    for mask in range(16):
        word = list(response_word)
        for offset, site in enumerate((4, 5, 6, 7)):
            word[site] = (mask >> offset) & 1
        d4_words.add(tuple(word))
    require(len(d4_words) == 16 and cap_word not in d4_words,
            "the cap word unexpectedly entered the response D4 cube")
    return {
        "response_word_full": "11110000",
        "response_word_display": "11:110000",
        "canonical_cap_word": "01211222",
        "word_hamming_distance": len(differing_sites),
        "differing_augmented_sites": [NAMES[site] for site in differing_sites],
        "selected_P3K2_decorations": rows,
        "all_six_fine_degrees_change": True,
        "response_D4_cube": "11:11 epsilon_2 epsilon_3 epsilon_4 epsilon_5",
        "D4_cube_vertex_count": len(d4_words),
        "cap_word_in_existing_D4_cube": False,
        "literal_grade_preserving_map": False,
        "first_required_arrow": (
            "a new word-changing, occurrence-local Cartan/Spencer/PP map; "
            "neither identity/relabeling nor the existing D4 cube supplies it"
        ),
    }


def augmented_packaging_audit() -> dict[str, object]:
    collision = load(
        "computations/verify_uniform_shear_collision_p3k2_augp2_grade_gate.py",
        "collision_packaging_input",
    )
    collision_ledger, collision_digest = collision.audit()
    require(collision_digest == collision.EXPECTED_LEDGER_SHA256,
            "the collision/cofactor ledger changed")
    first = collision_ledger["collision_first_faces"]
    require(first["first_PP_topology_counts"] == {"3K2": 90, "P3+K2": 90}
            and len(first["selected_tail_cofactor_P3K2_faces"]) == 6
            and len(first["selected_path_cofactor_3K2_faces"]) == 6,
            "the collision first-face packet changed")

    augp2_note = (ROOT / "notes/h3-augmented-p2-section-shortest-conditional-gate.md").read_text()
    mapping_note = (ROOT / "notes/h3-e14-pointed-orbit-keq-mapping-cylinder-gate.md").read_text()
    flat_note = (ROOT / "notes/h3-e14-cap-graph-two-parameter-flat-transport-gate.md").read_text()
    q_note = (ROOT / "notes/h3-universal-response-ks-augmented-readout-extension-gate.md").read_text()
    require("one theorem schema" in augp2_note
            and "not one bare source\ncolumn" in augp2_note
            and "H_1\\cong\\mathbb Z" in mapping_note
            and "mapping-cylinder/Tate face is both" in mapping_note
            and "physical_shifted_connection_face_constructed" not in flat_note
            and "place both its shifted" in flat_note
            and "Word/fine/repeated-grade\nlanding" in q_note,
            "a pinned packaging scope statement changed")

    # Quotient rows: hidden lower/P2, central Eq, mixed square incidence,
    # shifted Kahler.  The cofactor fills only the first coordinate.  Old
    # clean K_Eq fills only the second.  The mapping 2-cell and gamma are
    # independently required third and fourth directions.
    collision_p2 = tuple(map(Q, (1, 0, 0, 0)))
    clean_keq = tuple(map(Q, (0, 1, 0, 0)))
    mixed_incidence = tuple(map(Q, (0, 0, 1, 0)))
    shifted_ridge = tuple(map(Q, (0, 0, 0, 1)))
    require(rank((collision_p2, clean_keq)) == 2
            and rank((collision_p2, clean_keq, mixed_incidence)) == 3
            and rank((collision_p2, clean_keq, mixed_incidence,
                      shifted_ridge)) == 4,
            "the four packaging faces stopped being independent")
    mixed_dual = tuple(map(Q, (0, 0, 1, 0)))
    ridge_dual = tuple(map(Q, (0, 0, 0, 1)))
    dot = lambda left, right: sum(a * b for a, b in zip(left, right))
    require(dot(mixed_dual, collision_p2) == dot(mixed_dual, clean_keq) == 0
            and dot(mixed_dual, mixed_incidence) == 1
            and dot(ridge_dual, collision_p2) == dot(ridge_dual, clean_keq) == 0
            and dot(ridge_dual, shifted_ridge) == 1,
            "the mixed/ridge primitive separators changed")

    return {
        "pinned_collision_ledger": collision_digest,
        "existing_AugP2_status": {
            "conditional_multi_face_theorem_schema": True,
            "constructed_literal_source_object": False,
            "one_bare_homogeneous_column": False,
        },
        "selected_collision_contribution": {
            "supplies_at_associated_graded_level": (
                "six hidden lower/P2 SQQ cofactors"
            ),
            "also_carries": "six sibling 3K2 first faces",
            "does_not_supply": [
                "word-changing 11:110000 -> 01211222 comparison",
                "mixed mapping-square incidence",
                "physical reduced-Eq/cap label descent",
                "shifted pq/xv Kahler gamma and its connection face",
            ],
        },
        "packaging_quotient_rows": [
            "hidden lower/P2", "central Eq", "mixed incidence", "shifted ridge"
        ],
        "collision_P3K2_column": [1, 0, 0, 0],
        "old_clean_K_Eq_column": [0, 1, 0, 0],
        "rank_before_mixed_cell": 2,
        "rank_after_mixed_cell": 3,
        "rank_after_labelled_ridge": 4,
        "first_post_word_obstruction": (
            "the primitive H1 of the pointed P_f/K_Eq/word-transport square; "
            "one mixed mapping-cylinder/Tate 2-cell is necessary"
        ),
        "first_ridge_obstruction": (
            "place both shifted pq/xv halves of gamma=-dOmega and the "
            "connection face -d(q_xv^01) in the same labelled P3+K2 module"
        ),
        "formal_flatness_scope": (
            "after a physical bottom AugP2 section is granted, cap and ridge "
            "transport has zero mixed curvature; flatness does not construct "
            "the bottom word/fine section"
        ),
        "physical_q_scope": (
            "q is undefined on the collision/response relative generator "
            "before the complete augmented word map, so the q-defect "
            "generator/Fredholm alternative cannot be invoked early"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 shear-collision to AugP2 literal packaging map gate",
        "pins": PINS,
        "literal_word_and_fine_map": word_and_fine_grade_audit(),
        "augmented_packaging": augmented_packaging_audit(),
        "verdict": (
            "No existing AugP2 source object packages the shear-collision "
            "P3+K2 faces with the shifted ridge.  The undecorated graph "
            "matches, but all six decorated fine degrees lie in response "
            "word 11:110000 rather than cap word 01211222, which is outside "
            "the existing D4 cube.  After one grants a new word-changing "
            "map, the collision fills only the hidden lower/P2 row; the "
            "primitive mixed mapping-square 2-cell and labelled shifted "
            "Kahler face remain independent."
        ),
        "shortest_positive_construction": (
            "extend the collision top to a pointed relative PP mapping "
            "cylinder whose word-changing diagonal lands the six SQQ "
            "cofactors in the canonical AugP2 occurrence packet, retains "
            "the six 3K2 sibling faces, carries the reduced-Eq/cap label "
            "descent, and adjoins gamma=-dOmega with its -d(q_xv^01) "
            "connection.  Existing flatness then supplies coherence and "
            "eta/sigma, while physical q closes by the protected defect fork."
        ),
        "scope": (
            "exact canonical h3 selected collision packet, full literal "
            "eight-site words and fine degrees, and the committed AugP2/E14 "
            "mapping-cylinder and ridge interfaces.  This is the first "
            "grade/mixed-incidence obstruction, not an all-resolution no-go."
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
    words = ledger["literal_word_and_fine_map"]
    package = ledger["augmented_packaging"]
    print("literal word map: NO; Hamming distance=" +
          str(words["word_hamming_distance"]))
    print("cap word in existing response D4 cube: NO")
    print("collision packaging rank before mixed cell: " +
          str(package["rank_before_mixed_cell"]))
    print("first post-word obstruction: primitive mapping-square H1")
    print("shifted ridge: independent labelled Kahler face")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
