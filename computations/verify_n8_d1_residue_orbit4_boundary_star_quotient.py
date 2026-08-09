#!/usr/bin/env python3
"""Exact O4 double-quotient obstruction for a target-supported boundary star."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_ALIGNMENT_SHA256 = (
    "30095da401628a401cbdd2756b6dc3276f3c83cba62538097bd2c70c6481b26d"
)
SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_target_alignment_lemma.py"
)
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_ALIGNMENT_SHA256,
            "the pinned O4 target-alignment checker changed")
T = importlib.import_module(
    "verify_n8_d1_residue_orbit4_target_alignment_lemma"
)
F, S, C, D, V, O = T.F, T.S, T.C, T.D, T.V, T.O

EXPECTED_LEDGER_SHA256 = (
    "8e5e56eecbfd0d3ebf88a71f9598308fd16c437e0bb07662e8126f37fe84e6c9"
)


def edge_polynomial(cell, colour):
    u, v = cell
    i, j = colour
    return D.p_var("x_%d%d_%d%d" % (u, v, i, j))


def product(values):
    out = D.p_const(1)
    for value in values:
        out = D.p_mul(out, value)
    return out


def slice_audit(non_target_colour):
    c, e, _b, _d, alpha, _target, _A, _B, _D56, _blocks = S.family_data()
    words_checked = 0
    pure_rhs_words = 0
    coefficient_hashes = []
    route_histogram = {"partner4": 0, "partner5": 0, "killed": 0}
    remaining_sites = tuple(site for site in V.SITES if site != 6)
    for values in itertools.product(V.COLORS, repeat=len(remaining_sites)):
        word = dict(zip(remaining_sites, values))
        word[6] = non_target_colour
        pure_rhs_words += int(all(value == non_target_colour
                                  for value in values))
        raw = D.p_const(0)
        P = D.p_const(0)
        Q = D.p_const(0)
        for matching in V.MATCHINGS[V.SITES]:
            edge6 = next(edge for edge in matching if 6 in edge)
            partner = edge6[0] if edge6[1] == 6 else edge6[1]
            if partner not in (4, 5):
                route_histogram["killed"] += 1
                continue
            remainder = []
            for u, v in matching:
                if (u, v) == edge6:
                    continue
                remainder.append(edge_polynomial((u, v), (word[u], word[v])))
            remainder = product(remainder)
            if partner == 4:
                term = D.p_mul(
                    D.p_mul(alpha[non_target_colour], c[word[4]]),
                    remainder,
                )
                P = D.p_add(P, remainder)
                route_histogram["partner4"] += 1
            else:
                term = D.p_neg(D.p_mul(
                    D.p_mul(alpha[non_target_colour], e[word[5]]),
                    remainder,
                ))
                Q = D.p_add(Q, remainder)
                route_histogram["partner5"] += 1
            raw = D.p_add(raw, term)
        expected = D.p_mul(
            alpha[non_target_colour],
            D.p_add(D.p_mul(c[word[4]], P),
                    D.p_neg(D.p_mul(e[word[5]], Q))),
        )
        require(raw == expected,
                "the O4 boundary-star two-route factorization changed")
        words_checked += 1
        coefficient_hashes.append(D.content_hash(T.trace(raw)))

    # Each of 2,187 words has 105 matchings: fifteen through each possible
    # partner of site 6.  Five partner packets are support-dead.
    require(words_checked == 3 ** 7 and pure_rhs_words == 1
            and route_histogram == {
                "partner4": words_checked * 15,
                "partner5": words_checked * 15,
                "killed": words_checked * 75,
            }, "the full-slice matching partition changed")
    return {
        "site6_colour": non_target_colour,
        "seven_site_words_checked": words_checked,
        "pure_rhs_words": pure_rhs_words,
        "matching_routes": route_histogram,
        "factorization": (
            "alpha_a*(c(site4) tensor P-e(site5) tensor Q)"
        ),
        "coefficient_trace_sha256": D.content_hash(coefficient_hashes),
    }


def clause_audit():
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    allowed = (set(admissible) - set(O.RESIDUE_HOLES)
               - set(S.BOUNDARY_OMISSIONS))
    clauses = []
    for colour in (0, 1):
        holes = tuple(sorted(
            V.cell(boundary, 6, boundary_colour, colour)
            for boundary in range(4)
            for boundary_colour in (
                (0, 1) if boundary < 2 else V.COLORS
            )
        ))
        require(len(holes) == 10 and set(holes) <= allowed,
                "a boundary-star hole packet changed")
        for c_index in set(V.COLORS) - {colour}:
            for e_index in set(V.COLORS) - {colour}:
                witnesses = (
                    V.cell(4, 7, c_index, 2),
                    V.cell(5, 7, e_index, 2),
                )
                require(set(witnesses) <= allowed,
                        "a double-quotient witness changed")
                clauses.append({
                    "site6_colour": colour,
                    "boundary_star_holes": [list(cell) for cell in holes],
                    "quotient_witnesses": [list(cell) for cell in witnesses],
                    "cnf_clause": (
                        [list(cell) for cell in holes]
                        + [["not"] + list(cell) for cell in witnesses]
                    ),
                })
    require(len(clauses) == 8,
            "the boundary-star quotient clause census changed")
    return clauses


def build_ledger():
    return {
        "pinned_alignment_sha256": PINNED_ALIGNMENT_SHA256,
        "full_output_slices": [slice_audit(colour) for colour in (0, 1)],
        "support_clauses": clause_audit(),
        "double_quotient": (
            "quotient site4 by <c> and site5 by <e>; both two-route terms "
            "die, while the pure e_a^7 RHS survives whenever c and e each "
            "have a localized coordinate off e_a"
        ),
        "hypothesis_strength": (
            "ten boundary-to-site6 cells of one non-target site6 colour are "
            "absent and two off-line residue witnesses are localized"
        ),
        "base_ring_scope": (
            "matching factorization and quotient argument over an arbitrary "
            "localized integral domain; no division is used"
        ),
        "characteristic_scope": "every field",
        "status": "the target-supported site6 boundary-star stratum is empty",
    }


def main():
    started = monotonic()
    ledger = build_ledger()
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256:", digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the O4 boundary-star quotient ledger changed")
        print("ledger sha256 (frozen):", digest)
    print("O4 boundary-star double quotient: PASS (all characteristics)")
    print("support clauses: 8")
    print("elapsed: %.3fs" % (monotonic() - started))


if __name__ == "__main__":
    main()
