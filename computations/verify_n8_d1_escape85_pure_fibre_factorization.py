#!/usr/bin/env python3
"""Exact pure-residue factorization closure for the D1 escape-85 support."""

from __future__ import annotations

import hashlib
import importlib
import itertools
import os
import sys
from collections import Counter
from fractions import Fraction
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_RESIDUE_SHA256 = (
    "eafdf37c6546a4d548a80de0101aff4125fe25fe5e61cf9aac18c4f1e2ab28de"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_escape85_residue_family.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest() == PINNED_RESIDUE_SHA256,
            "the pinned escape-85 residue source changed")
R = importlib.import_module("verify_n8_d1_escape85_residue_family")
C, D, V = R.C, R.D, R.C.V

EXPECTED_LEDGER_SHA256 = (
    "57d81009fd03c0caf98bec255b8981da004778c3c26de899e63410ff573d8482"
)


def product(*polys):
    out = D.p_const(1)
    for poly in polys:
        out = D.p_mul(out, poly)
    return out


def build_blocks():
    _state, _extras, base_support, admissible, _stats = C.candidate_input()
    support = frozenset(set(admissible) - set(R.MISSING_RESIDUE_CELLS))
    require(len(support) == 191 and base_support <= support,
            "the escape-85 maximal support changed")
    blocks = D.sym_zero_blocks(V.SITES)
    for cell in sorted(support):
        D.sym_put(blocks, *cell,
                  D.p_var("x_%d%d_%d%d" % cell))
    return support, blocks


def record_key(poly):
    return tuple(sorted((monomial, str(coefficient))
                        for monomial, coefficient in poly.items()))


def factorization_audit(support, blocks):
    target_word = {site: 2 for site in V.RESIDUE}
    residue = D.sym_matching_sum(blocks, V.RESIDUE, target_word)
    residue_generator = D.p_sub(residue, D.p_const(1))
    require(len(residue) == 3,
            "the pure residue coefficient lost its three matching terms")

    records = C.coefficient_generators(support)
    record_index = {
        tuple((tuple(monomial), coefficient)
              for monomial, coefficient in record["terms"]):
        (index, record["families"])
        for index, record in enumerate(records)
    }
    require(record_index[record_key(residue_generator)][1]
            == ["residue_purity"],
            "the pure residue generator left its exact family")

    factorizations = []

    def audit_one(label, domain, word, boundary_cells):
        matching_sum = D.sym_matching_sum(blocks, domain, word)
        factor = product(*(D.sym_cell(blocks, *cell)
                           for cell in boundary_cells))
        require(factor and matching_sum == product(factor, residue),
                "%s lost its exact pure-residue factorization" % label)
        require(all(cell in support for cell in boundary_cells),
                "%s lost a localized boundary factor" % label)
        require(not (len(set(word.values())) == 1 if domain == V.SITES
                     else set(word.values()) == {2}),
                "%s is no longer a zero-target fibre" % label)
        key = record_key(matching_sum)
        require(key in record_index,
                "%s left the reconstructed generator list" % label)
        index, families = record_index[key]
        expected_family = ("full_exactness" if domain == V.SITES
                           else "lemma_F_six_site")
        require(families == [expected_family],
                "%s changed coefficient family" % label)

        # If g=m*R and q=R-1, then g-m*q=m.  This is an ordinary
        # localization certificate over every characteristic.
        certificate = D.p_sub(matching_sum,
                              D.p_mul(factor, residue_generator))
        require(certificate == factor,
                "%s failed its ordinary monomial certificate" % label)
        factorizations.append({
            "label": label,
            "domain": list(domain),
            "word": [word[site] for site in domain],
            "boundary_cells": [list(cell) for cell in boundary_cells],
            "record_index": index,
            "factor_degree": len(boundary_cells),
            "factorization_terms": len(matching_sum),
        })

    for colour in (0, 1):
        word = {site: 2 for site in V.W1}
        word[2] = colour
        audit_one("W1_2%d_2222" % colour, V.W1, word,
                  (V.cell(0, 2, 2, colour),))
    for colour in (0, 1):
        word = {site: 2 for site in V.W2}
        word[3] = colour
        audit_one("W2_2%d_2222" % colour, V.W2, word,
                  (V.cell(1, 3, 2, colour),))
    for left, right in itertools.product(V.COLORS, repeat=2):
        if (left, right) == (2, 2):
            continue
        word = {site: 2 for site in V.SITES}
        word[2], word[3] = left, right
        audit_one("full_22%d%d_2222" % (left, right), V.SITES, word,
                  (V.cell(0, 2, 2, left),
                   V.cell(1, 3, 2, right)))

    require(len(factorizations) == 12,
            "the zero-target pure-fibre factorization census changed")
    require(Counter(row["factor_degree"] for row in factorizations)
            == {1: 4, 2: 8},
            "the factorization-degree census changed")
    expected_indices = [
        3464, 3484, 3504, 3878, 4018, 4038,
        4058, 4432, 4572, 4592, 6612, 6632,
    ]
    require(sorted(row["record_index"] for row in factorizations)
            == expected_indices,
            "the twelve factorized record indices changed")
    # Audit the full 3^4 boundary-word universe for the {02,13}+residue
    # lift, rather than checking only the one orientation used to close the
    # support.  All 81 boundary products are localized here; exactly the
    # eight mixed words recorded above (and the one pure word) have every
    # competing full matching support-dead.
    full_word_census = Counter()
    exact_lifts = []
    for i, j, k, l in itertools.product(V.COLORS, repeat=4):
        full_word_census["boundary_words"] += 1
        mixed = (i, j, k, l) != (2, 2, 2, 2)
        full_word_census["mixed_boundary_words"] += mixed
        word = {0: i, 1: j, 2: k, 3: l,
                4: 2, 5: 2, 6: 2, 7: 2}
        factor = product(D.sym_cell(blocks, 0, 2, i, k),
                         D.sym_cell(blocks, 1, 3, j, l))
        full_word_census["localized_boundary_products"] += bool(factor)
        matching_sum = D.sym_matching_sum(blocks, V.SITES, word)
        exact = bool(factor) and matching_sum == product(factor, residue)
        full_word_census["support_dead_competing_matchings"] += exact
        full_word_census["mixed_exact_lifts"] += exact and mixed
        if exact:
            exact_lifts.append([i, j, k, l])
    require(full_word_census == {
                "boundary_words": 81,
                "mixed_boundary_words": 80,
                "localized_boundary_products": 81,
                "support_dead_competing_matchings": 9,
                "mixed_exact_lifts": 8,
            }
            and exact_lifts == [
                [2, 2, 0, 0], [2, 2, 0, 1], [2, 2, 0, 2],
                [2, 2, 1, 0], [2, 2, 1, 1], [2, 2, 1, 2],
                [2, 2, 2, 0], [2, 2, 2, 1], [2, 2, 2, 2],
            ],
            "the complete 81-word pure-lift census changed")
    return (residue, records, factorizations,
            dict(sorted(full_word_census.items())), exact_lifts)


def specialize_record(record, residue_values):
    out = {}
    for monomial, coefficient in record["terms"]:
        coefficient = Fraction(coefficient)
        remaining = []
        for name in monomial:
            if name in residue_values:
                coefficient *= residue_values[name]
            else:
                remaining.append(name)
        key = tuple(remaining)
        out[key] = out.get(key, Fraction(0)) + coefficient
        if not out[key]:
            del out[key]
    return out


def specialization_discovery_audit(records, factorizations):
    point = R.explicit_residue_point_audit()["point"]
    residue_values = {
        "x_%d%d_%d%d" % tuple(cell): Fraction(value)
        for cell, value in point
    }
    raw_monomials = []
    for index, record in enumerate(records):
        specialized = specialize_record(record, residue_values)
        if len(specialized) == 1:
            monomial, coefficient = next(iter(specialized.items()))
            raw_monomials.append({
                "record_index": index,
                "families": record["families"],
                "monomial": list(monomial),
                "coefficient": str(coefficient),
            })
    expected_indices = sorted(row["record_index"] for row in factorizations)
    require(len(raw_monomials) == 12
            and [row["record_index"] for row in raw_monomials]
            == expected_indices
            and all(row["coefficient"] == "1" for row in raw_monomials),
            "the rational-point monomial discovery census changed")
    require(Counter(tuple(row["families"]) for row in raw_monomials)
            == {("full_exactness",): 8, ("lemma_F_six_site",): 4},
            "the specialized monomial family census changed")
    return raw_monomials


def audit():
    started = monotonic()
    support, blocks = build_blocks()
    (residue, records, factorizations,
     full_word_census, exact_lifts) = factorization_audit(support, blocks)
    specialized = specialization_discovery_audit(records, factorizations)
    ledger = {
        "pinned_residue_sha256": PINNED_RESIDUE_SHA256,
        "localized_support_cells": len(support),
        "coefficient_generators": len(records),
        "pure_residue_terms": len(residue),
        "zero_target_factorizations": factorizations,
        "complete_boundary_word_census": full_word_census,
        "exact_full_lifts": exact_lifts,
        "specialization_control": specialized,
        "certificate": (
            "For each factorized zero-target generator g=m*R and the pure "
            "residue generator q=R-1, the exact identity g-m*q=m puts a "
            "localized monomial in the ideal. Record 3464 alone uses "
            "m=x_02_20*x_13_20 and closes the support."
        ),
        "pure_lift_theorem": (
            "For any boundary colours (i,j,k,l) other than the all-target "
            "word, suppose x02_ik and x13_jl are localized and every full "
            "matching except {02,13} plus a residue perfect matching is "
            "support-dead. With target colour 2 on the residue, mixed full "
            "exactness is x02_ik*x13_jl*H_R(2222)=0, while residue purity is "
            "H_R(2222)=1. Hence the localized coefficient ideal is empty. "
            "The statement applies to all 80 mixed boundary words, in any "
            "support and without choosing an escape orientation."
        ),
        "characteristic_scope": "every field",
        "status": (
            "the 191-variable escape-85 maximal support is empty; one residue "
            "purity generator and one mixed full-output generator suffice"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the escape-85 pure-fibre ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 escape85 pure-fibre factorization: PASS (exact)")
    print("factorizations:", len(ledger["zero_target_factorizations"]),
          "(8 full, 4 six-site)")
    print("certificate: records 3464 and residue purity give a localized U^2")
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
