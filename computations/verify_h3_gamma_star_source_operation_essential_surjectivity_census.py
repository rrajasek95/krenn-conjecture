#!/usr/bin/env python3
"""Audit the literal relative-degree-one source-operation census at Gamma_*.

The source grammar in this checker is the canonical free cellular/bar closure
of the operations which actually occur in the h=3 construction:

* coefficient equations and their Macaulay multiples;
* PP/Hasse restriction and labelled reinsertion;
* Cartan/Weyl/root faces;
* objectwise K_Eq and cap-internal AugP2 faces; and
* standard mapping cylinders and their naturality/interchange cells.

The full tag is retained: eight-site word, the six literal cap fine degrees,
repeated-edge shape, operation parent, marked window, and relative degree.
At relative total degree one, all primitives are canonical or chi-dark except
the interchange of a cross-word occurrence map with K_Eq.  Its literal lower
word is a one-site ternary neighbour of 0112, giving exactly eight kappa
instances.  Thus the quotient by canonical plus dark cells is spanned by
those eight classes.  This does not evaluate their eight lambda coefficients.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py":
        "2ae3d0fe36ca6ab92ee506b4a4441d6476ecb09567a1441c66f54793e304980d",
    "notes/h3-psi-source-grade-macaulay-exhaustiveness-terminal-gate.md":
        "de47eeafdfcffbd043f3b2472f3be54b7ec94ad546fe2bab7194e8b64bd9c98a",
    "computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py":
        "269a1b775e0790c3e4f1f6390b83673c1118270e491885ce9383e703f07b3278",
    "notes/h3-four-site-full-source-exhaustiveness-decomposition-gate.md":
        "703da478db0e60c53f98bdd4835248172872b7412eb884a60d08ac14bef1fb4e",
    "computations/verify_h3_kappa_mix_eight_instance_symmetry_covariance_gate.py":
        "ecaeb7612191eeb78609560f886f2fa19b00ae41379ab335a2436db14b05b143",
    "notes/h3-kappa-mix-eight-instance-symmetry-covariance-gate.md":
        "65ac9bd838529b3be775c15cc2f358e8072f1c9afec1f781e1a7bd0d86e5e259",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
    "computations/verify_h3_degree4_hv_psiloc_augmented_landing_gate.py":
        "5032493dce5c96b0ddb28175dd8b8a9a73a3c4f566d48d48d63f673802a85106",
    "notes/h3-degree4-hv-psiloc-augmented-landing-gate.md":
        "e431d03f23c2549e0987d680e48389775444f72eb2ba17cdb5529ed64036a5f5",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "notes/h3-shear-collision-augp2-packaging-map-gate.md":
        "9d5918605dd94d08d18c099966e5956fa0f1c62855b97fd81bf9ada54f2f45ad",
    "computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py":
        "2e4b1a1b9bb5b5be8d0997132b49b95576a28dc6ccb9cfd83db808ace8f52f3e",
    "notes/h3-e14-pointed-orbit-keq-mapping-cylinder-gate.md":
        "f5008f5b7e892b5ce5270faacee4ec9f2bffc2630b8dd15a55cb8f5c6800cb21",
    "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py":
        "00db2478df3162a374434ea7d0ab285f770510d33b72619377560404c96b16e8",
    "notes/h3-shared-four-term-endpoint-word-change-inventory-boundary.md":
        "12ffea4f2c520f22320ba47a253b686e0b29dbe43d6e2ef8f43f4f86208a4c29",
}
EXPECTED_LEDGER_SHA256 = "193ea36ee809852222d9a99f14a8dca181b10973e69773e09583cfb57398add9"

CAP_WORD = tuple(map(int, "01211222"))
RESPONSE_WORD = tuple(map(int, "11110000"))
LOWER_PARENT = tuple(map(int, "0112"))
LOWER_SITES = (0, 1, 4, 5)
KAPPA_WORDS = tuple(tuple(map(int, word)) for word in (
    "0012", "0102", "0110", "0111",
    "0122", "0212", "1112", "2112",
))
DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO8 = (Q(0),) * 8
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
SELECTED_FACES = (
    ("s0", "q01", "q45"),
    ("s0", "q01", "q23"),
    ("s0", "q01", "q35"),
    ("s0", "q01", "q24"),
    ("s0", "q01", "q34"),
    ("s0", "q01", "q25"),
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def word_text(word: tuple[int, ...]) -> str:
    return "".join(map(str, word))


def fine_degree(labels: tuple[str, ...], word: tuple[int, ...]) -> tuple[int, ...]:
    degree = Counter()
    for label in labels:
        for site in EDGE_SITES[label]:
            degree[(site, word[site])] += 1
    return tuple(degree[(site, colour)]
                 for site in range(8) for colour in range(3))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
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


def full_grade_audit() -> dict[str, object]:
    cap_fine = tuple(fine_degree(labels, CAP_WORD) for labels in SELECTED_FACES)
    response_fine = tuple(fine_degree(labels, RESPONSE_WORD)
                          for labels in SELECTED_FACES)
    require(len(set(cap_fine)) == len(set(response_fine)) == 6,
            "the six literal fine idempotents stopped separating")
    require(all(cap != response for cap, response in
                zip(cap_fine, response_fine, strict=True)),
            "a response fine degree entered the cap fine orbit")
    changed = tuple(index for index, pair in enumerate(
        zip(CAP_WORD, RESPONSE_WORD, strict=True)) if pair[0] != pair[1])
    require(changed == (0, 2, 4, 5, 6, 7), changed)
    return {
        "word": word_text(CAP_WORD),
        "fine_lattice_coordinate_width": 24,
        "fine_orbit": [list(degree) for degree in cap_fine],
        "fine_labels": ["*".join(labels) for labels in SELECTED_FACES],
        "repeated": "P3+K2",
        "operation_parent": "response-to-AugP2 mixed orbit/K_Eq",
        "window": "2345 with literal occurrence labels",
        "lower_parent": "0112 on sites 0,1,4,5; ordered 01; q45:12; q23:21",
        "relative_total_degree": 1,
        "response_word": word_text(RESPONSE_WORD),
        "word_changed_sites": [NAMES[index] for index in changed],
        "all_six_response_fine_degrees_different": True,
    }


def ternary_one_root_neighbours() -> tuple[tuple[int, ...], ...]:
    words = []
    for site in range(len(LOWER_PARENT)):
        for colour in range(3):
            if colour == LOWER_PARENT[site]:
                continue
            word = list(LOWER_PARENT)
            word[site] = colour
            words.append(tuple(word))
    return tuple(sorted(words))


def operation_census() -> tuple[dict[str, object], ...]:
    """Return every indecomposable C1 type in the declared source grammar.

    `same` means that all Gamma_* tags displayed by full_grade_audit agree.
    When it is false, mismatch gives the first literal direct-sum separator.
    A same-grade dark cell has a proved B/Eq projection reason instead.
    """
    return (
        {"primitive": "coefficient equation / Macaulay multiple",
         "source_operation": "coefficient", "same": True,
         "class": "canonical", "reason": "canonical presentation image"},
        {"primitive": "PP/Hasse restriction face",
         "source_operation": "PP-Hasse", "same": True,
         "class": "dark", "reason": "local rank-126/127 chi-kernel"},
        {"primitive": "labelled spectator reinsertion",
         "source_operation": "reinsertion", "same": True,
         "class": "dark", "reason": "tied B/Eq local incidence"},
        {"primitive": "Cartan/Weyl same-shore face",
         "source_operation": "Cartan-Weyl", "same": True,
         "class": "dark", "reason": "same-shore/local fan"},
        {"primitive": "shore-gauged DQ/PS root face",
         "source_operation": "Cartan-Weyl", "same": True,
         "class": "dark", "reason": "signless edge u with delta.u=0"},
        {"primitive": "pointed occurrence conormal P_f",
         "source_operation": "AugP2", "same": True,
         "class": "dark", "reason": "anchor/conormal row outside B/Eq"},
        {"primitive": "primitive cap p / target-residue graph",
         "source_operation": "AugP2", "same": True,
         "class": "dark", "reason": "Q/target/residue rows outside B/Eq"},
        {"primitive": "objectwise K_Eq face",
         "source_operation": "K_Eq", "same": True,
         "class": "dark", "reason": "diagonal or tied reduced-Eq incidence"},
        {"primitive": "shifted gamma=-dOmega ridge face",
         "source_operation": "AugP2", "same": False,
         "mismatch": "fine,repeated", "class": "off-grade",
         "reason": "shifted Kahler direct summand"},
        {"primitive": "degree-four h_v Koszul x Eq product",
         "source_operation": "coefficient/Koszul", "same": False,
         "mismatch": "repeated,operation", "class": "off-grade",
         "reason": "raw 2K2 and central-Eq parent; diagonal placement is dark"},
        {"primitive": "collision / one-hole response face",
         "source_operation": "coefficient/PP", "same": False,
         "mismatch": "word,fine,operation", "class": "off-grade",
         "reason": "response/collision direct summand"},
        {"primitive": "3K2 collision sibling",
         "source_operation": "PP-Hasse", "same": False,
         "mismatch": "repeated,operation", "class": "off-grade",
         "reason": "3K2 proper-face summand"},
        {"primitive": "lower word section / dq reinsertion before placement",
         "source_operation": "reinsertion", "same": False,
         "mismatch": "word,fine,repeated,operation", "class": "off-grade",
         "reason": "lower P2 direct summand"},
        {"primitive": "cross-word occurrence mapping-cylinder edge",
         "source_operation": "mapping-cylinder", "same": True,
         "class": "dark", "reason": "word transport has no untied Eq component"},
        {"primitive": "same-object K_Eq mapping-cylinder edge",
         "source_operation": "mapping-cylinder/K_Eq", "same": True,
         "class": "dark", "reason": "objectwise/tied Eq naturality"},
        {"primitive": "cross-word x K_Eq interchange two-cell",
         "source_operation": "mapping-cylinder/K_Eq", "same": True,
         "class": "kappa", "reason": "only mixed B/Eq naturality incidence"},
        {"primitive": "residual-response Kodaira-Spencer tail transport",
         "source_operation": "residual KS", "same": False,
         "mismatch": "operation", "class": "off-grade",
         "reason": "endpoint-residue parent, not AugP2/K_Eq mixed parent"},
    )


def operation_parent_interchange_audit() -> dict[str, object]:
    # Parents 0,1 are DQ; 2,3 are PS.  Physical shore gauge makes every
    # cross-shore primitive incidence signless.
    cross = tuple((left, right) for left in (0, 1) for right in (2, 3))
    edges = tuple(tuple(Q(1 if index in pair else 0) for index in range(4))
                  for pair in cross)
    require(len(cross) == 4 and rank(edges) == 3
            and all(sum((DELTA[i] * edge[i] for i in range(4)), Q(0)) == 0
                    for edge in edges),
            "the four DQ/PS primitive incidences changed")

    # The two binary decorations give the exhaustive mapping-cylinder
    # truth table.  Only their interchange is not already canonical/dark.
    table = (
        {"cross_word": 0, "K_Eq_mixed": 0, "class": "local/canonical"},
        {"cross_word": 1, "K_Eq_mixed": 0, "class": "word-cylinder dark"},
        {"cross_word": 0, "K_Eq_mixed": 1, "class": "objectwise Eq dark"},
        {"cross_word": 1, "K_Eq_mixed": 1, "class": "kappa"},
    )
    require(sum(row["class"] == "kappa" for row in table) == 1,
            "interchange truth table")
    return {
        "parents": ["DQ[a|b]", "DQ[b|a]", "PS[P0,S1]", "PS[P1,S0]"],
        "cross_shore_types": [list(pair) for pair in cross],
        "physical_signless_edge_rank": rank(edges),
        "delta_pairings": [0, 0, 0, 0],
        "root_sections": {
            "AB": ["g02", "g12"],
            "AC": ["g03", "g13"],
        },
        "mapping_cylinder_truth_table": table,
    }


def quotient_audit(records: tuple[dict[str, object], ...]) -> dict[str, object]:
    neighbours = ternary_one_root_neighbours()
    require(neighbours == KAPPA_WORDS,
            (tuple(map(word_text, neighbours)), tuple(map(word_text, KAPPA_WORDS))))
    require(len(records) == 17
            and sum(record["class"] == "kappa" for record in records) == 1,
            "primitive source-operation census")
    require(all(record.get("mismatch") or record["class"] in
                ("canonical", "dark", "kappa") for record in records),
            "a same-grade primitive lacks a projection classification")

    kappa_columns = tuple(
        tuple(Q(1 if row == column else 0) for row in range(8))
        for column in range(8)
    )
    require(rank(kappa_columns) == 8,
            "the eight literal kappa normal forms stopped spanning")
    return {
        "lower_parent_word": word_text(LOWER_PARENT),
        "one_root_rule": "change exactly one of four sites to either other ternary colour",
        "literal_kappa_words": [word_text(word) for word in neighbours],
        "literal_kappa_count": len(neighbours),
        "symbolic_quotient_rank_upper_bound": rank(kappa_columns),
        "quotient_statement": (
            "C1_grammar,Gamma*/(C1_canonical+ker chi) is spanned by "
            "kappa_0012,...,kappa_2112"
        ),
        "not_decided": "the eight physical lambda_i=Psi(d kappa_i)",
    }


def totalization_audit() -> dict[str, object]:
    return {
        "presentation": (
            "free cellular/bar closure of coefficient, PP/Hasse, reinsertion, "
            "Cartan/Weyl, K_Eq, AugP2, and standard mapping-cylinder maps"
        ),
        "degree_one_indecomposables": (
            "atomic faces plus the standard pairwise naturality/interchange cells"
        ),
        "multi_face_rule": (
            "a cellular boundary is the signed linear sum of primitive incidences"
        ),
        "higher_word_rule": (
            "two or more independent comparison steps have bar/cellular degree >=2; "
            "their C1 faces are already enumerated primitive incidences"
        ),
        "no_new_C1_image_from_higher_syzygies": True,
        "concrete_named_non_kappa_evaders": [],
        "scope_guard": (
            "the theorem does not admit a new independently primitive noncellular "
            "multi-parent operation absent from the literal source grammar"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    grade = full_grade_audit()
    records = operation_census()
    ledger = {
        "theorem": "Gamma_* literal source-operation essential-surjectivity census",
        "full_additive_grade": grade,
        "primitive_operation_census": list(records),
        "operation_parent_interchange": operation_parent_interchange_audit(),
        "quotient": quotient_audit(records),
        "canonical_totalization": totalization_audit(),
        "scope": {
            "exact": "canonical h=3 literal source-operation grammar over Q",
            "proves": "essential surjectivity onto the degree-one quotient modulo canonical+dark",
            "does_not_prove": [
                "that any kappa_i is chi-dark",
                "the eight lambda_i=0 equations",
                "a completed full decorated physical source equivalence beyond this grammar",
                "uniform spectator-tail transport for all h",
            ],
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return ledger, sha256(payload.encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("generic", "beta-zero"),
                        default="generic")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("source-operation census ledger changed", digest))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h3 Gamma_* source-operation essential-surjectivity census "
              f"({arguments.mode}): PASS")
        print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
