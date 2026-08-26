#!/usr/bin/env python3
"""Exact pure-row extension audit for the sealed X5 reciprocity guard."""

from __future__ import annotations

from collections import Counter
import functools
import hashlib
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT_MANIFEST = REPO / "computations/unaudited-codex-n8-x5-proof-side-synthesis-2026-08-25/MANIFEST.sha256"
PARENT_MANIFEST_SHA256 = "05e85e32252a31f55c85f6a8ec1e08e6aa2c02674dc98b523c6b99f56509cced"
TRIANGLE_RESULT = REPO / "computations/unaudited-codex-triangle-five-set-annihilator-2026-08-22/results_triangle_five_set_annihilator.json"
TRIANGLE_RESULT_SHA256 = "6cd93663ed6bf392a24ee74cc1546cdcaa8b8124d07012910df69920bbf9abae"
SITES = tuple(range(8))
COLORS = tuple(range(3))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield ((first, second),) + tail


PM8 = tuple(matchings(SITES))
assert len(PM8) == 105


def key(u, v, cu, cv):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return u, v, cu, cv


def put(source, u, v, cu, cv, value):
    source[key(u, v, cu, cv)] = value


def get(source, u, v, cu, cv):
    return source.get(key(u, v, cu, cv), 0)


def install_matrix(source, u, v, matrix):
    for cu in COLORS:
        for cv in COLORS:
            if matrix[cu][cv]:
                put(source, u, v, cu, cv, matrix[cu][cv])


def identity():
    return [[int(i == j) for j in COLORS] for i in COLORS]


def e00():
    return [[int(i == j == 0) for j in COLORS] for i in COLORS]


def zero_matrix():
    return [[0 for _ in COLORS] for _ in COLORS]


def amplitude_terms(source, word, vertices=SITES):
    answer = []
    for matching in matchings(tuple(vertices)):
        value = 1
        for u, v in matching:
            value *= get(source, u, v, word[u], word[v])
        if value:
            answer.append((matching, value))
    return answer


def amplitude(source, word, vertices=SITES):
    return sum(value for _matching, value in amplitude_terms(source, word, vertices))


def response(source, p, q, a, b, covector):
    answer = zero_matrix()
    for alpha in COLORS:
        for beta in COLORS:
            answer[alpha][beta] = sum(
                covector[i][j] * (
                    get(source, p, a, i, alpha) * get(source, q, b, j, beta)
                    + get(source, p, b, i, beta) * get(source, q, a, j, alpha)
                )
                for i in COLORS for j in COLORS
            )
    return answer


def pairing(covector, vector):
    return sum(covector[i][j] * vector[i][j] for i in COLORS for j in COLORS)


def original_guard():
    source = {}
    for edge in ((1, 6), (2, 7), (6, 7)):
        install_matrix(source, *edge, identity())
    for edge in ((0, 3), (4, 5)):
        install_matrix(source, *edge, e00())
    return source


def pure_normalized_extension():
    source = original_guard()
    # Four new cells, two for each missing pure colour.
    for edge in ((0, 3), (4, 5)):
        for colour in (1, 2):
            put(source, *edge, colour, colour, 1)
    return source


def one_row_cancellation_extension():
    source = pure_normalized_extension()
    # A second literal matching of 00001100, with product -1.  Both added
    # cells are residual-residual, so the cap-67 triangle response data and
    # the beta=00000 five-set functional are unchanged.
    put(source, 0, 4, 0, 1, 1)
    put(source, 3, 5, 0, 1, -1)
    return source


def word_string(word):
    return "".join(map(str, word))


def source_cells(source):
    return [
        {"edge": [u, v], "colours": [cu, cv], "value": value}
        for (u, v, cu, cv), value in sorted(source.items())
    ]


def max_matching_size(edges):
    best = 0
    for count in range(len(edges) + 1):
        for chosen in itertools.combinations(edges, count):
            endpoints = [site for edge in chosen for site in edge]
            if len(endpoints) == len(set(endpoints)):
                best = max(best, count)
    return best


def main() -> None:
    assert sha256(PARENT_MANIFEST) == PARENT_MANIFEST_SHA256
    assert sha256(TRIANGLE_RESULT) == TRIANGLE_RESULT_SHA256
    triangle = json.loads(TRIANGLE_RESULT.read_text())
    assert triangle["hostile_source_guard"]["delta_beta"] == [1, 0, 0]

    original = original_guard()
    pure = pure_normalized_extension()
    cancel = one_row_cancellation_extension()
    K, L = identity(), e00()

    # Original formal guard: pure target is only colour zero.
    original_pure = [amplitude(original, (colour,) * 8) for colour in COLORS]
    assert original_pure == [1, 0, 0]

    # Minimality inside the frozen physical support.  For each of colours 1
    # and 2 the old diagonal support graph has matching number two, so any
    # pure perfect matching needs at least two newly nonzero colour-cells.
    old_colour_edges = ((1, 6), (2, 7), (6, 7))
    assert max_matching_size(old_colour_edges) == 2
    minimum_new_cells = 2 * (4 - max_matching_size(old_colour_edges))
    assert minimum_new_cells == 4
    added_pure_cells = sorted(set(pure) - set(original))
    assert len(added_pure_cells) == minimum_new_cells

    # The four-cell extension realizes all pure rows exactly.
    pure_values = [amplitude(pure, (colour,) * 8) for colour in COLORS]
    assert pure_values == [1, 1, 1]
    values = [(word, amplitude(pure, word)) for word in itertools.product(COLORS, repeat=8)]
    nonzero_mixed = [(word, value) for word, value in values if value and len(set(word)) > 1]
    assert len(nonzero_mixed) == 78
    assert {value for _word, value in nonzero_mixed} == {1}
    first_word, first_value = nonzero_mixed[0]
    assert word_string(first_word) == "00001100" and first_value == 1
    first_terms = amplitude_terms(pure, first_word)
    assert first_terms == [(((0, 3), (1, 6), (2, 7), (4, 5)), 1)]

    # The cap/five-set guard is unchanged by pure normalization.
    assert response(pure, 6, 7, 1, 2, K) == identity()
    assert pairing(L, response(pure, 6, 7, 1, 2, K)) == 1
    assert pairing(L, [[get(pure, 1, 2, i, j) for j in COLORS] for i in COLORS]) == 0
    assert [L[c][c] for c in COLORS] == [1, 0, 0]
    switched_residual = tuple(site for site in SITES if site not in (1, 2))
    switched_nonzero = {
        edge: response(pure, 1, 2, *edge, L)
        for edge in itertools.combinations(switched_residual, 2)
        if response(pure, 1, 2, *edge, L) != zero_matrix()
    }
    assert switched_nonzero == {(6, 7): e00()}
    outside = [
        edge for edge in itertools.combinations(range(6), 2)
        if not set(edge) <= {0, 1, 2}
    ]
    assert len(outside) == 12
    assert all(response(pure, 6, 7, *edge, K) == zero_matrix() for edge in outside)

    # The support-restricted contradiction can be evaded at its first mixed
    # row with only two off-support cells; this preserves the formal guard but
    # is still far from X5.
    cancel_pure = [amplitude(cancel, (colour,) * 8) for colour in COLORS]
    assert cancel_pure == [1, 1, 1]
    cancel_terms = amplitude_terms(cancel, first_word)
    assert cancel_terms == [
        (((0, 3), (1, 6), (2, 7), (4, 5)), 1),
        (((0, 4), (1, 6), (2, 7), (3, 5)), -1),
    ]
    assert sum(value for _matching, value in cancel_terms) == 0
    assert response(cancel, 6, 7, 1, 2, K) == identity()
    assert all(response(cancel, 6, 7, *edge, K) == zero_matrix() for edge in outside)
    cancel_switched_nonzero = {
        edge: response(cancel, 1, 2, *edge, L)
        for edge in itertools.combinations(switched_residual, 2)
        if response(cancel, 1, 2, *edge, L) != zero_matrix()
    }
    assert cancel_switched_nonzero == switched_nonzero
    cancel_values = [(word, amplitude(cancel, word)) for word in itertools.product(COLORS, repeat=8)]
    cancel_nonzero_mixed = [(word, value) for word, value in cancel_values if value and len(set(word)) > 1]
    assert len(cancel_nonzero_mixed) == 69
    assert word_string(cancel_nonzero_mixed[0][0]) == "00002200"

    # beta=evaluation at W-word 00000 remains an internal five-set
    # annihilator: every all-zero four-site cofactor on W={1,...,5} vanishes.
    W = (1, 2, 3, 4, 5)
    beta_cofactors = {}
    for omitted in W:
        remaining = tuple(site for site in W if site != omitted)
        word = [0] * 8
        beta_cofactors[str(omitted)] = amplitude(cancel, tuple(word), remaining)
    assert set(beta_cofactors.values()) == {0}

    result = {
        "schema": "KRENN_X5_RECIPROCITY_PURE_ROW_GUARD_AUDIT_V1",
        "status": "PASS_PURE_ROWS_SURVIVE_ACTIVITY_GUARD_SUPPORT_FULL_X5_CONTRADICTED",
        "parent_manifest_sha256": PARENT_MANIFEST_SHA256,
        "original_formal_guard": {
            "pure_amplitudes": original_pure,
            "s_L": 0,
            "kappa_L": [1, 0, 0],
            "normalized_X5": False,
        },
        "minimal_pure_normalized_extension": {
            "new_source_cells": [
                {"edge": [u, v], "colours": [cu, cv], "value": pure[(u, v, cu, cv)]}
                for u, v, cu, cv in added_pure_cells
            ],
            "minimal_new_cell_count_within_frozen_physical_support": minimum_new_cells,
            "pure_amplitudes": pure_values,
            "s_L": 0,
            "kappa_L": [1, 0, 0],
            "switched_response_support": ["67"],
            "cap_error": "zero because r is supported on one edge",
            "R_12_of_I_for_cap_67": "I3",
            "triangle_outside_responses": 0,
            "mixed_violations": len(nonzero_mixed),
            "first_mixed_violation": {
                "word": word_string(first_word),
                "amplitude": first_value,
                "sole_matching": "03|16|27|45",
            },
            "mathematical_scope": "exact pure-row countermodel only; not an X5 or conjecture source",
        },
        "support_restricted_lemma": {
            "hypotheses": (
                "physical support contained in {03,16,27,45,67}, "
                "A16[cc]=A27[cc]=1, and all three pure amplitudes equal one"
            ),
            "identities": [
                "Phi(c^8)=A03[cc]*A45[cc]=1",
                "Phi(c,c,c,c,d,d,c,c)=A03[cc]*A45[dd] for c!=d",
            ],
            "conclusion": (
                "the displayed mixed amplitude is a unit and cannot vanish; "
                "full normalized X5 is impossible in this support class"
            ),
            "proof_type": "unique literal perfect matching plus unit cancellation in an integral domain",
        },
        "first_off_support_cancellation_guard": {
            "new_source_cells": [
                {"edge": [0, 4], "colours": [0, 1], "value": 1},
                {"edge": [3, 5], "colours": [0, 1], "value": -1},
            ],
            "cancelled_word": "00001100",
            "literal_terms": ["+03|16|27|45", "-04|16|27|35"],
            "pure_amplitudes": cancel_pure,
            "formal_triangle_guard_preserved": True,
            "switched_cap_error_remains_zero": True,
            "switched_activity_remains_false": True,
            "beta_00000_cofactors": beta_cofactors,
            "remaining_mixed_violations": len(cancel_nonzero_mixed),
            "first_remaining_mixed_violation": word_string(cancel_nonzero_mixed[0][0]),
            "normalized_X5": False,
        },
        "verdict": {
            "pure_rows_exclude_s0_kappa100": False,
            "support_preserving_full_X5_routes_to_contradiction": True,
            "arbitrary_bicoloured_full_X5_routes_to_existing_terminal_theorem": False,
            "remaining_missing_input": (
                "a source-labelled identity controlling all off-support mixed-row "
                "cancellations, or proving activity for a different reciprocal covector"
            ),
        },
        "guards": {
            "degree_twelve_read": False,
            "broad_cegar": False,
            "claim_that_countermodels_satisfy_X5": False,
            "claim_that_general_bicoloured_conjecture_is_closed": False,
        },
    }
    temporary = HERE / "results_pure_row_guard.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_pure_row_guard.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
