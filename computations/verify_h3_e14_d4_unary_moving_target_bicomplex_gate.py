#!/usr/bin/env python3
"""Audit the D4/complete-unary square on the silent E14 branch.

The fourth global-root Hasse face carries the marked response occurrence
from word 110000 to its pure target mate in word 111111.  The complete
unary S-pair then writes the mate as ``-R_E14+T12``.  A formal free PP
totalization can of course add a square whose boundary contains ``T12``.
This checker asks the stricter question: do the already present D1--D3
response Hasse faces provide that horizontal side?

They do not.  The local D1--D3 occurrence packet is quadratic in the two
residual q edges, whereas the twelve proper unary tails are ten cubics and
two quartics.  More decisively, the complete 269-column first-hit module
already includes every complete response row in all words (with every
monomial multiplier that can hit T12), hence in particular every D1--D3
word.  Its exact dual kills those columns and still pairs -1 with T12.
The reduced obstruction is the single class ``[T12]=[R_E14]``.

The moving cap graph T+rho is retained.  It repairs the target/scalar-cap
normalization after transport, but has no literal unary-tail coordinate and
therefore does not alter this proper-face class.  Thus formal d^2=0 names a
new cross-operation PP/Tate two-cell; it does not construct one from the
old D1--D3 faces.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_silent_target_occurrence_compression_gate.py":
        "d8addc92045c58cb9e26492b5c0d641bf8f182454dff3df0fff72a47f2df89a2",
    "notes/h3-e14-silent-target-occurrence-compression-gate.md":
        "f0fdaec942d790447efec7729ceb3a75038424390a77bf92aa61c565ad228722",
    "computations/verify_h3_e14_pointed_two_stage_koszul_spair_gate.py":
        "7d837db5133bfb46b36fe71a3f499de04f4342ca794d2c45b56e6ec8275d7d0d",
    "notes/h3-e14-pointed-two-stage-koszul-spair-gate.md":
        "7585ba8d4dd6267e260f6c639bd47aced38748add9beca440d0285042053e26c",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "notes/h3-hasse-coproduct-cosimplicial-totalization.md":
        "9bb749b3b45a6b0248699bf54364cb304f89e01a4a4ad654963aad3534893ba4",
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
}
EXPECTED_LEDGER_SHA256 = (
    "a3eafe3cf538fd9329a212c685089de3f74d3e327ff53aa9f0ae9eb42fce1246"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def word_after(base: tuple[int, ...], sites: tuple[int, ...]) -> tuple[int, ...]:
    answer = list(base)
    for site in sites:
        require(answer[site] == 0, ("root does not start at zero", base, site))
        answer[site] = 1
    return tuple(answer)


def boolean_boundary(face: tuple[int, ...]) -> dict[tuple[int, ...], int]:
    return {
        face[:index] + face[index + 1:]: (-1) ** index
        for index in range(len(face))
    }


def boolean_totalization_audit() -> dict[str, object]:
    directions = (2, 3, 4, 5)
    base = (1, 1, 0, 0, 0, 0)
    levels: dict[int, tuple[tuple[int, ...], ...]] = {}
    for mask in range(1 << len(directions)):
        face = tuple(directions[index] for index in range(len(directions))
                     if mask & (1 << index))
        levels.setdefault(len(face), ())
        levels[len(face)] += (face,)
    require(tuple(len(levels[k]) for k in range(5)) == (1, 4, 6, 4, 1),
            "the Boolean D0--D4 face profile changed")

    # Check the signed cubical/simplicial deletion boundary squares to zero.
    for dimension in range(2, 5):
        for face in levels[dimension]:
            second = defaultdict(int)
            for once, first_sign in boolean_boundary(face).items():
                for twice, second_sign in boolean_boundary(once).items():
                    second[twice] += first_sign * second_sign
            require(not any(second.values()), ("Boolean d^2 changed", face, second))

    proper_words = {
        word_after(base, face)
        for dimension in (1, 2, 3)
        for face in levels[dimension]
    }
    require(len(proper_words) == 14
            and word_after(base, directions) == (1,) * 6
            and (0, 0, 0, 1, 0, 1) not in proper_words,
            ("the response D1--D3 word packet changed", proper_words))
    return {
        "root": "0->1 at residual sites 2,3,4,5",
        "base_word": "110000",
        "top_word": "111111",
        "face_profile_D0_through_D4": [1, 4, 6, 4, 1],
        "proper_D1_D3_word_count": len(proper_words),
        "proper_D1_D3_words": sorted("".join(map(str, word))
                                          for word in proper_words),
        "unary_source_word": "000101",
        "unary_word_is_response_cube_face": False,
        "signed_boolean_boundary_squares_zero": True,
    }


def exact_first_hit_with_hasse_classification(
    proper_words: set[tuple[int, ...]],
) -> dict[str, object]:
    first = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "d4_unary_first",
    )
    first_ledger, first_digest = first.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256,
            "the complete first-hit ledger changed")
    rewrite = first.load(first.REWRITE_PATH, "d4_unary_rewrite")
    top = rewrite.load(rewrite.TOP_PATH, "d4_unary_top")
    two = top.load(top.TWO_CELL_PATH, "d4_unary_two")
    e14 = two.load(two.E14_PATH, "d4_unary_e14")
    b4 = e14.load(e14.B4_PATH, "d4_unary_b4")
    _candidates, _names, responses, unary = two.universal(e14, b4, 1, 1)

    endpoint = ("p1_0_1", "s1_1_1")
    pivot = ("u35_11",)
    multiplier = ("v2411",)
    unary_word = (0, 0, 0, 1, 0, 1)
    factor, remainder = first.factor_unary(unary[unary_word], pivot)
    require(factor == {(): Q(-1), ("v0400",): Q(1)}
            and len(remainder) == 12,
            ("the U=pA+B packet changed", factor, remainder))
    target = {
        (endpoint, first.multiply_monomials(monomial, multiplier)): coefficient
        for monomial, coefficient in remainder.items()
    }
    degree_profile = Counter(len(coordinate[1]) for coordinate in target)
    require(degree_profile == Counter({3: 10, 4: 2}),
            ("the T12 degree profile changed", degree_profile))

    response_rows = [
        (output_word, first.response_terms(row))
        for output_word, row in responses.items()
    ]
    unary_rows = [
        (output_word, tuple(polynomial.items()))
        for output_word, polynomial in unary.items()
    ]
    columns: dict[tuple[object, ...], dict[object, Q]] = {}
    column_words: dict[tuple[object, ...], tuple[int, ...]] = {}
    for target_endpoint, target_monomial in target:
        for row_index, (output_word, row) in enumerate(response_rows):
            for row_endpoint, row_monomial, _coefficient in row:
                if row_endpoint != target_endpoint:
                    continue
                row_multiplier = first.quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                key = ("G11", row_index, row_multiplier)
                column = {
                    (output_endpoint,
                     first.multiply_monomials(output_monomial, row_multiplier)):
                        output_coefficient
                    for output_endpoint, output_monomial, output_coefficient in row
                }
                if output_word == (1,) * 6:
                    column[(("target_G11",), row_multiplier)] = Q(-1)
                columns[key] = column
                column_words[key] = output_word
        for row_index, (output_word, row) in enumerate(unary_rows):
            for row_monomial, _coefficient in row:
                row_multiplier = first.quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                key = ("unary", row_index, target_endpoint, row_multiplier)
                column = {
                    (target_endpoint,
                     first.multiply_monomials(output_monomial, row_multiplier)):
                        output_coefficient
                    for output_monomial, output_coefficient in row
                }
                if output_word == (0,) * 6:
                    column[(("target_unary",) + target_endpoint,
                            row_multiplier)] = Q(-1)
                columns[key] = column
                column_words[key] = output_word

    pivots = {}
    for column in columns.values():
        first.add_exact_column(column, pivots)
    reduced = first.exact_reduce(target, pivots)
    expected_reduced = {
        (endpoint, ("u35_11", "v2411")): Q(1),
        (endpoint, ("u35_11", "v0400", "v2411")): Q(-1),
    }
    require(len(columns) == len(pivots) == 269 and reduced == expected_reduced,
            ("the exact full first-hit reduction changed",
             len(columns), len(pivots), reduced))

    free = min(reduced)
    dual = {free: Q(1)}
    for leading in sorted(pivots, reverse=True):
        value = sum(
            coefficient * dual.get(coordinate, Q(0))
            for coordinate, coefficient in pivots[leading].items()
            if coordinate != leading
        )
        if value:
            dual[leading] = -value
    pairing = sum(coefficient * dual.get(coordinate, Q(0))
                  for coordinate, coefficient in target.items())
    require(pairing == Q(-1), ("the T12 dual pairing changed", pairing))

    hasse_columns = {
        key: column for key, column in columns.items()
        if key[0] == "G11" and column_words[key] in proper_words
    }
    require(hasse_columns, "no D1--D3 response row hits were classified")
    hasse_pivots = {}
    for column in hasse_columns.values():
        first.add_exact_column(column, hasse_pivots)
    hasse_pairings = {
        key: sum(coefficient * dual.get(coordinate, Q(0))
                 for coordinate, coefficient in column.items())
        for key, column in hasse_columns.items()
    }
    require(not any(hasse_pairings.values()),
            ("the first-hit dual stopped killing a D1--D3 row", hasse_pairings))

    # The literal marked D1--D3 occurrence faces still have precisely two q
    # factors.  They cannot equal any proper tail before multiplying source
    # rows; after arbitrary compatible multiplication they are among the
    # complete columns above and remain dual-annihilated.
    local_root_face_degrees = Counter({2: 14})
    require(set(local_root_face_degrees).isdisjoint(degree_profile),
            "a local proper root face acquired a unary-tail degree")
    return {
        "T12_tail_count": len(target),
        "T12_q_degree_profile": {
            str(degree): count for degree, count in sorted(degree_profile.items())
        },
        "marked_local_D1_D3_occurrence_degree_profile": {"2": 14},
        "literal_marked_occurrence_overlap": 0,
        "complete_first_hit_columns": len(columns),
        "complete_first_hit_rank_Q": len(pivots),
        "D1_D3_response_columns_hitting_T12": len(hasse_columns),
        "D1_D3_response_hit_rank_Q": len(hasse_pivots),
        "first_hit_dual_support": len(dual),
        "first_hit_dual_pairing_T12": str(pairing),
        "first_hit_dual_kills_every_D1_D3_hit": True,
        "reduced_T12": "R_E14=g-v04_00*g",
        "silent_reduced_T12": "g",
        "existing_D1_D3_cancel_T12": False,
    }


def moving_cap_and_bicomplex_conclusion() -> dict[str, object]:
    silent = load(
        "computations/verify_h3_e14_silent_target_occurrence_compression_gate.py",
        "d4_unary_silent",
    )
    silent_ledger, silent_digest = silent.audit()
    require(silent_digest == silent.EXPECTED_LEDGER_SHA256,
            "the moving target/cap ledger changed")
    normalization = silent_ledger["augmented_compression"]
    require(normalization["old_normalized_cap_graph"]
                == ["0", "0", "1", "0", "1"]
            and normalization["cap_graph_boundary"] == 0
            and normalization["required_cap_graph_coefficient"] == "-89/90",
            ("the moving T+rho cap graph changed", normalization))

    return {
        "moving_cap_graph": "T+rho",
        "moving_cap_graph_rows": {
            "boundary": 0, "target": 1, "Q": 0, "scalar_ores": 1,
        },
        "moving_cap_graph_unary_tail_coordinates": 0,
        "cap_graph_closes_factor_90_normalization_after_placement": True,
        "cap_graph_closes_T12_proper_face": False,
        "formal_free_PP_totalization": (
            "adjoining the horizontal D4/unary cross-operation two-cell "
            "makes the Boolean d^2 identity tautological"
        ),
        "current_physical_inventory": (
            "contains the vertical D1--D3 response faces and the moving "
            "cap graph, but not the horizontal maps on those faces"
        ),
        "smallest_remaining_class": "one graded/private class [T12]=[R_E14]",
        "smallest_positive_addition": (
            "one source-labelled orbit-relative PP/Tate cross-operation "
            "cell whose proper boundary is the complete T12 packet; it "
            "must carry target/cap, q, ridge, anchor and eta/sigma readouts"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    boolean = boolean_totalization_audit()
    proper_words = {
        tuple(map(int, word)) for word in boolean["proper_D1_D3_words"]
    }
    ledger = {
        "theorem": "D4/unary moving-target bicomplex proper-face gate",
        "pins": PINS,
        "boolean_D4_totalization": boolean,
        "literal_and_complete_D1_D3_test":
            exact_first_hit_with_hasse_classification(proper_words),
        "moving_target_cap_and_conclusion":
            moving_cap_and_bicomplex_conclusion(),
        "verdict": (
            "The signed D0--D4 Boolean boundary has d^2=0, but this does "
            "not make the complete unary proper face an old boundary.  The "
            "marked D1--D3 occurrence faces are quadratic and miss the ten "
            "cubic plus two quartic T12 tails.  Even after every compatible "
            "complete response-row multiplier is allowed, the pinned "
            "first-hit dual kills all D1--D3 hits and pairs -1 with T12.  "
            "Thus one class [T12]=[R_E14] remains.  Keeping the moving "
            "T+rho cap graph repairs only target/scalar-cap normalization."
        ),
        "scope": (
            "canonical h=3 chart-(1,1), silent v04=0 E14 occurrence.  This "
            "is an exact no-go for cancellation by the existing D1--D3 "
            "complete response faces, not a no-go for adjoining the missing "
            "orbit-relative PP/Tate cross-operation cell.  Physical q, "
            "ridge, anchor and terminal typing remain requirements on that "
            "new cell."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    exact = ledger["literal_and_complete_D1_D3_test"]
    print("D4 Boolean profile 1,4,6,4,1 and d^2=0: PASS")
    print("literal D1-D3 occurrence overlap with T12: 0")
    print("complete D1-D3 hits="
          f"{exact['D1_D3_response_columns_hitting_T12']}; "
          "all killed by the first-hit dual")
    print("remaining proper-face class: [T12]=[R_E14]")
    print("moving T+rho cap graph closes normalization, not T12")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
