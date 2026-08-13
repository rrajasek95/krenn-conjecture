#!/usr/bin/env python3
"""Audit the first physical face of the shifted order-two placement P2.

Work on the literal lower cut with sites (0,1,4,5), word 0112, residual
q45:12, and later reinsertion q23:21.  The exact endpoint-even B-4
preimage is

    z=-(B+6I)c_plus/24.

For every endpoint/residual move, the source-valid two-root Cartan/PP
square has two one-root Hasse faces.  We collect those faces by their
intermediate word while retaining all twelve ordered occurrence labels.
Each of the eight nonzero word faces is nonconstant.  Hence it is not in
the complete response line in that word.  The target/reduced-Eq/Koszul
triangle has no coordinates in this occurrence-private quotient, so it
does not by itself define P2.

The representative word 0102 has occurrence vector

 (-13/12,0,1/6,-13/12,1/6,0,0,1/6,5/12,1/6,0,5/12).

Thus the first absent physical column is an occurrence-local one-endpoint
PP section, before any remaining target or reduced-Eq normalization.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py":
        "47ea1f915429dc7937ef2e81037c0494136d9ae379d76e0584bb22cef8e0d390",
    "computations/verify_h2_lower_0112_bminus4_target_normal_gate.py":
        "8fffe45182c4bb304dabfbe9df568061a8049bec21949539bcae88f60f5d22e0",
    "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py":
        "09ba792f229bb3a1e930b2c59b0de2356b08a7434c648aad9573d8382c652a52",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py":
        "01e36f89b4df4bb020607d2f00871deb96775a7e58b42e85eaef76c20097e5cf",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
}
EXPECTED_LEDGER_SHA256 = (
    "9d3462fee3f24b2a73368f831240dbe6adedab8109c8716f928849b54ea8d323"
)


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


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(row) for row in zip(*columns, strict=True)]
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


def word_text(word):
    return "".join(map(str, word))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    parity = load(
        "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py",
        "p2_hasse_parity",
    )
    occurrence, abstract_values, lookup, swap, b_matrix, s_matrix = (
        parity.endpoint_data()
    )
    require(len(abstract_values) == 12, "order-two occurrence count changed")
    size = len(abstract_values)
    one = (Q(1),) * size
    marked = (0, 1, (occurrence.edge(2, 3),))
    marked_mate = swap(marked)
    c_plus = tuple(Q(6 if value in (marked, marked_mate) else 0) - 1
                   for value in abstract_values)
    z = scale(
        Q(-1, 24),
        parity.matvec(
            parity.matrix_add(b_matrix,
                              parity.matrix_scale(6, parity.identity(size))),
            c_plus,
        ),
    )
    b_minus_four = parity.matrix_add(
        b_matrix, parity.matrix_scale(-4, parity.identity(size))
    )
    require(parity.matvec(b_minus_four, z) == c_plus,
            "the exact B-4 preimage changed")
    require(parity.matvec(s_matrix, z) == z,
            "the exact B-4 preimage stopped being endpoint-even")

    # Relabel the abstract packet to the literal 0112 cut.
    physical_sites = (0, 1, 4, 5)
    physical_from_abstract = {0: 0, 1: 1, 2: 4, 3: 5}
    values = tuple((
        physical_from_abstract[p_site],
        physical_from_abstract[s_site],
        tuple(sorted((physical_from_abstract[left],
                      physical_from_abstract[right]))
              for left, right in matching),
    ) for p_site, s_site, matching in abstract_values)
    colours = {0: 0, 1: 1, 4: 1, 5: 2}
    base_word = tuple(colours[site] for site in physical_sites)
    require(word_text(base_word) == "0112", "literal lower word changed")

    # A root-decorated endpoint move has two one-root faces: recolour the
    # endpoint only, or the selected residual site only.  The occurrence
    # label is retained because a colour root does not move physical sites.
    faces = defaultdict(lambda: [Q(0)] * size)
    contributing_paths = defaultdict(int)
    root_moves = 0
    same_colour_moves = 0
    for index, (p_site, s_site, matching) in enumerate(values):
        require(len(matching) == 1, "h2 residual stopped being one edge")
        residual = matching[0]
        for endpoint in (p_site, s_site):
            for selected in residual:
                if colours[endpoint] == colours[selected]:
                    same_colour_moves += 1
                    continue
                root_moves += 1
                for changed in (endpoint, selected):
                    word = list(base_word)
                    word[physical_sites.index(changed)] = (
                        colours[selected] if changed == endpoint
                        else colours[endpoint]
                    )
                    word = tuple(word)
                    faces[word][index] += z[index]
                    contributing_paths[word] += 1

    require(root_moves == 40 and same_colour_moves == 8,
            ("endpoint/root move census changed", root_moves,
             same_colour_moves))
    face_vectors = {word: tuple(vector) for word, vector in faces.items()}
    require(len(face_vectors) == 8,
            ("one-root intermediate word count changed", face_vectors))
    require(set(map(word_text, face_vectors)) == {
        "0012", "0102", "0110", "0111",
        "0122", "0212", "1112", "2112",
    }, "one-root word support changed")
    require(set(contributing_paths.values()) == {8, 16},
            ("one-root path multiplicities changed", contributing_paths))

    representative = face_vectors[tuple(map(int, "0102"))]
    expected_representative = tuple(map(Q, (
        Q(-13, 12), 0, Q(1, 6), Q(-13, 12), Q(1, 6), 0,
        0, Q(1, 6), Q(5, 12), Q(1, 6), 0, Q(5, 12),
    )))
    require(representative == expected_representative,
            ("0102 occurrence-private face changed", representative))
    require(parity.matvec(s_matrix, representative) == representative,
            "the representative one-root face stopped being endpoint-even")

    # The complete response supplies only the constant vector in each word.
    # Every actual one-root face raises that word block rank from one to two.
    records = []
    for word in sorted(face_vectors):
        vector = face_vectors[word]
        require(rank([one, vector]) == 2,
                ("one-root face entered the complete response line", word))
        records.append({
            "word": word_text(word),
            "paths": contributing_paths[word],
            "sum": str(sum(vector, Q(0))),
            "nonzero_occurrences": sum(bool(value) for value in vector),
            "rank_with_complete_response": rank([one, vector]),
        })

    # Put each word in a separate occurrence block.  Target and Eq rows are
    # separate augmented blocks and project to zero here.  Thus all eight
    # wordwise quotient classes survive independently in the displayed cone.
    words = tuple(sorted(face_vectors))
    direct_faces = []
    complete_rows = []
    for block, word in enumerate(words):
        face = [Q(0)] * (len(words) * size)
        complete = [Q(0)] * (len(words) * size)
        start = block * size
        face[start:start + size] = face_vectors[word]
        complete[start:start + size] = one
        direct_faces.append(tuple(face))
        complete_rows.append(tuple(complete))
    require(rank(complete_rows) == 8
            and rank(complete_rows + direct_faces) == 16,
            "the direct one-root private quotient changed")

    # A primitive endpoint-even coordinate dual in the 0102 block kills the
    # complete row and detects the representative.  Abstract coordinates
    # 0<->3 and 1<->6 under endpoint transposition.
    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(size))
    require(sum(detector, Q(0)) == 0
            and parity.matvec(s_matrix, detector) == detector
            and sum(a * b for a, b in
                    zip(detector, representative, strict=True)) == Q(-13, 6),
            "the primitive 0102 private detector changed")

    ledger = {
        "theorem": "h2 P2 one-cut one-endpoint Hasse placement gate",
        "pins": PINS,
        "physical_cut": {
            "sites": list(physical_sites),
            "lower_word": "0112",
            "residual": "q45:12",
            "reinsertion": "q23:21",
            "top_word": "01211222",
            "top_grade": "labelled repeated P3+K2",
        },
        "exact_even_input": {
            "c_plus": "6(e_f+e_Sf)-1",
            "preimage": "z=-(B+6I)c_plus/24",
            "identity": "(B-4I)z=c_plus",
            "endpoint_parity": "even",
            "coordinates": [str(value) for value in z],
        },
        "one_endpoint_Hasse_faces": {
            "root_endpoint_moves": root_moves,
            "same_colour_endpoint_moves": same_colour_moves,
            "intermediate_words": records,
            "representative_word": "0102",
            "representative_occurrence_vector": [str(value)
                                                   for value in representative],
            "rank_complete_rows": rank(complete_rows),
            "rank_after_faces": rank(complete_rows + direct_faces),
            "surviving_wordwise_private_classes": 8,
        },
        "representative_dual": {
            "abstract_support": "+e0+e3-e1-e6",
            "endpoint_parity": "even",
            "kills_complete_response": True,
            "value": "-13/6",
            "physical_terminal": False,
        },
        "three_term_cone": {
            "columns": ["lower endpoint path", "even Cartan target cone",
                        "reduced-Eq Koszul/Spencer face"],
            "mixed_target_closed": True,
            "reduced_Eq_closed": True,
            "occurrence_private_projection_of_last_two_columns": 0,
            "full_source_differential_lands": False,
        },
        "first_absent_column": (
            "one occurrence-local endpoint-even one-endpoint PP section in "
            "the 0102 intermediate-word orbit whose boundary cancels the "
            "displayed private vector modulo the complete response row"
        ),
        "scope": (
            "literal 0112/q23 representative and its universal two-root "
            "one-endpoint Hasse faces.  This does not construct the absent "
            "section, its reinsertion dq23 face, or a physical terminal."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h2 P2 placement ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("h2 P2 cut: 0112/q23:21")
    print("one-root Hasse words:",
          len(ledger["one_endpoint_Hasse_faces"]["intermediate_words"]))
    print("complete-response rank 8 -> 16 after private faces")
    print("representative 0102 private dual: -13/6")
    print("three-term target/Eq cone source landing: FAILS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
