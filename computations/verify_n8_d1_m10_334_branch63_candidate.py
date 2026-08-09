#!/usr/bin/env python3
"""Freeze and check the first complete-shadow SAT support in m=10 3+3+4."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import itertools
import json
import os
import sys
from collections import Counter
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_433_SHA256 = (
    "463627051b215c4c21bf96978376aaef512a98177562bf467993dce2e340a87f"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_433_full_shadow.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest() == PINNED_433_SHA256,
            "the committed 4+3+3 closure source changed")
G = importlib.import_module("verify_n8_d1_m10_433_full_shadow")
S = importlib.import_module("verify_n8_d1_minimal_off_sigma_support_cover")
D, H, F, I, A = S.D, G.H, G.F, G.I, G.A
V = F.V

ARTIFACT_PATH = os.path.join(
    HERE, "certificates", "n8_d1_m10_334_branch63_candidate.json"
)
EXPECTED_ARTIFACT_SHA256 = (
    "da34a34cbeac0e30309088f17007b63274cb65435719e3106515b18ede9ffccd"
)
EXPECTED_LEDGER_SHA256 = (
    "52e8085fb995dd66fc1da7743cc172fac52bd8baa12da79ec46a0de1d4968c33"
)

# One deterministic CaDiCaL model was reduced to its semantic Sigma support.
# The checker below does not trust the solver or its auxiliary-variable model:
# it reevaluates all 8,100 fibres directly from these cells.
CANDIDATE_SIGMA_SUPPORT = frozenset({
    (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 1),
    (0, 2, 0, 0), (0, 2, 0, 1), (0, 2, 0, 2),
    (0, 2, 1, 0), (0, 2, 1, 1), (0, 2, 1, 2),
    (0, 2, 2, 0), (0, 2, 2, 1), (0, 2, 2, 2),
    (0, 3, 0, 0), (0, 3, 0, 1), (0, 3, 0, 2),
    (0, 3, 1, 1),
    (0, 4, 0, 2), (0, 5, 0, 2),
    (0, 6, 0, 2), (0, 6, 1, 2),
    (0, 7, 0, 2), (0, 7, 1, 2),
    (1, 2, 0, 0), (1, 2, 1, 0), (1, 2, 1, 1), (1, 2, 1, 2),
    (1, 3, 0, 0), (1, 3, 0, 1), (1, 3, 0, 2),
    (1, 3, 1, 0), (1, 3, 1, 1), (1, 3, 1, 2),
    (1, 3, 2, 0), (1, 3, 2, 1), (1, 3, 2, 2),
    (1, 4, 1, 2), (1, 5, 1, 2),
    (1, 6, 0, 2), (1, 6, 1, 2),
    (1, 7, 0, 2), (1, 7, 1, 2),
    (2, 3, 0, 0), (2, 3, 0, 1), (2, 3, 0, 2),
    (2, 3, 1, 1), (2, 3, 2, 1),
    (2, 4, 0, 2), (2, 5, 0, 2),
    (2, 6, 0, 2), (2, 6, 1, 2), (2, 6, 2, 2),
    (2, 7, 0, 2), (2, 7, 1, 2), (2, 7, 2, 2),
    (3, 4, 1, 2), (3, 5, 1, 2),
    (3, 6, 0, 2), (3, 6, 1, 2), (3, 6, 2, 2),
    (3, 7, 0, 2), (3, 7, 1, 2), (3, 7, 2, 2),
    (4, 6, 2, 2), (4, 7, 2, 2),
    (5, 6, 2, 2), (5, 7, 2, 2), (6, 7, 2, 2),
})


def family_branches():
    branches, admissible, sigma, off_sigma = I.surviving_branches()
    rows = [(index, state) for family, index, state in branches
            if family == "334"]
    require(len(rows) == 131, "the 3+3+4 symbolic frontier changed")
    return rows, admissible, sigma, off_sigma


def dynamic_residuals(state, admissible, sigma, off_sigma):
    initial, anchor_units = state
    seen, residuals = set(), set()
    stats = Counter()

    def search(base, remaining):
        key = base, remaining
        if key in seen:
            return
        seen.add(key)
        stats["nodes"] += 1
        certificate = F.choose_dynamic_repair(
            (base, anchor_units), remaining,
            admissible, sigma, off_sigma,
        )
        if certificate is not None and certificate["repair"] is None:
            stats["dynamic_unique_closures"] += 1
            return
        if remaining == 0:
            residuals.add(base)
            return
        if certificate is not None:
            stats["repair_DNF_nodes"] += 1
            for repair in certificate["repair"]:
                search(frozenset(set(base) | set(repair)),
                       remaining - len(repair))
            return
        stats["free_extension_nodes"] += 1
        for entry in sorted(off_sigma - set(base)):
            search(base | {entry}, remaining - 1)

    search(initial, 4)
    return sorted(residuals, key=lambda row: tuple(sorted(row))), stats


def candidate_input():
    branches, admissible, sigma, off_sigma = family_branches()
    state = dict(branches)[63]
    residuals, stats = dynamic_residuals(
        state, admissible, sigma, off_sigma
    )
    require(len(residuals) == 1,
            "branch 334:63 no longer has one dynamic residual")
    extras = residuals[0]
    require(len(extras) == 10 and extras <= off_sigma,
            "the branch-63 off-Sigma support changed")
    require(len(CANDIDATE_SIGMA_SUPPORT) == 67
            and CANDIDATE_SIGMA_SUPPORT <= sigma,
            "the frozen candidate Sigma support changed")
    support = set(extras) | set(CANDIDATE_SIGMA_SUPPORT)
    mandatory = (set(V.BASE_UNITS) | set(state[1])
                 | {V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2)})
    require(mandatory <= support,
            "a mandatory D1 cell is absent from the candidate")
    return state, extras, frozenset(support), admissible, stats


def support_shadow_audit(support):
    histogram = Counter()
    fibre_count = 0
    for domain in (V.SITES, V.W1, V.W2, V.RESIDUE):
        for values in itertools.product(V.COLORS, repeat=len(domain)):
            fibre_count += 1
            word = dict(zip(domain, values))
            live = 0
            for matching in V.MATCHINGS[tuple(domain)]:
                cells = tuple(V.cell(u, v, word[u], word[v])
                              for u, v in matching)
                live += all(entry in support for entry in cells)
            pure = (len(set(values)) == 1
                    if domain == V.SITES else set(values) == {2})
            require(live >= 1 if pure else live != 1,
                    "the frozen support fails an exact fibre shadow")
            bucket = str(live) if live < 5 else "5_plus"
            histogram[(len(domain), "pure" if pure else "zero", bucket)] += 1
    require(fibre_count == 8100,
            "the candidate fibre census changed")
    return {
        "fibres_checked": fibre_count,
        "live_matching_histogram": {
            "%d_%s_%s" % key: value
            for key, value in sorted(histogram.items())
        },
    }


def polynomial_key(poly):
    return tuple(sorted((monomial, str(coefficient))
                        for monomial, coefficient in poly.items()))


def coefficient_generators(support):
    blocks = D.sym_zero_blocks(V.SITES)
    for u, v, i, j in sorted(support):
        D.sym_put(blocks, u, v, i, j,
                  D.p_var("x_%d%d_%d%d" % (u, v, i, j)))
    generators = {}

    def add(poly, family):
        if not D.p_is_zero(poly):
            generators.setdefault(polynomial_key(poly), set()).add(family)

    for values in itertools.product(V.COLORS, repeat=8):
        word = dict(zip(V.SITES, values))
        target = D.p_const(1 if len(set(values)) == 1 else 0)
        add(D.p_sub(D.sym_matching_sum(blocks, V.SITES, word), target),
            "full_exactness")
    for domain in (V.W1, V.W2):
        for values in itertools.product(V.COLORS, repeat=6):
            word = dict(zip(domain, values))
            target = D.p_const(1 if set(values) == {2} else 0)
            add(D.p_sub(D.sym_matching_sum(blocks, domain, word), target),
                "lemma_F_six_site")
    for values in itertools.product(V.COLORS, repeat=4):
        word = dict(zip(V.RESIDUE, values))
        target = D.p_const(1 if set(values) == {2} else 0)
        add(D.p_sub(D.sym_matching_sum(blocks, V.RESIDUE, word), target),
            "residue_purity")
    for u, partner in sorted(D.D1_ESSENTIAL_PARTNER.items()):
        for size in (2, 4, 6, 8):
            for subset in itertools.combinations(V.SITES, size):
                if u in subset and partner not in subset:
                    add(D.sym_matching_sum(
                        blocks, subset, {site: 2 for site in subset}),
                        "a_pendant")
    h_residue = D.sym_matching_sum(
        blocks, V.RESIDUE, {site: 2 for site in V.RESIDUE}
    )
    for u, partner in sorted(D.D1_ESSENTIAL_PARTNER.items()):
        left = D.p_mul(D.sym_cell(
            blocks, u, partner, D.CHI[u], D.CHI[partner]), h_residue)
        right = D.p_const(0)
        for r in V.RESIDUE:
            for rp in V.RESIDUE:
                if r == rp:
                    continue
                rest = tuple(site for site in V.RESIDUE
                             if site not in (r, rp))
                term = D.p_mul(
                    D.p_mul(D.sym_cell(blocks, u, r, D.CHI[u], 2),
                            D.sym_cell(blocks, partner, rp,
                                       D.CHI[partner], 2)),
                    D.sym_matching_sum(
                        blocks, rest, {site: 2 for site in rest}),
                )
                right = D.p_add(right, term)
        add(D.p_add(left, right), "dagger")
    harm = D.p_sub(
        D.p_mul(D.sym_cell(blocks, 0, 2, 0, 1),
                D.sym_cell(blocks, 1, 3, 0, 1)),
        D.p_mul(D.sym_cell(blocks, 0, 1, 0, 0),
                D.sym_cell(blocks, 2, 3, 1, 1)),
    )
    add(harm, "D1_harm")

    records = [
        {
            "families": sorted(families),
            "terms": [[list(monomial), coefficient]
                      for monomial, coefficient in key],
        }
        for key, families in sorted(generators.items())
    ]
    return records


def build_artifact():
    state, extras, support, _admissible, _stats = candidate_input()
    return {
        "branch": "334:63",
        "anchor_units": [list(entry) for entry in sorted(state[1])],
        "off_sigma_support": [list(entry) for entry in sorted(extras)],
        "sigma_support": [list(entry)
                          for entry in sorted(CANDIDATE_SIGMA_SUPPORT)],
        "localized_nonzero_cells": [list(entry) for entry in sorted(support)],
        "coefficient_generators": coefficient_generators(support),
    }


def audit():
    started = monotonic()
    with open(ARTIFACT_PATH, "rb") as handle:
        raw = handle.read()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_ARTIFACT_SHA256,
            "the frozen branch-63 coefficient artifact changed")
    frozen = json.loads(raw.decode("ascii"))
    rebuilt = build_artifact()
    require(frozen == rebuilt,
            "the branch-63 support/coefficient artifact failed reconstruction")
    _state, extras, support, admissible, stats = candidate_input()
    require(support <= admissible,
            "the candidate contains an E1-forbidden cell")
    shadow = support_shadow_audit(support)
    family_counts = Counter()
    histogram = Counter()
    single_term_generators = 0
    for generator in rebuilt["coefficient_generators"]:
        for family in generator["families"]:
            family_counts[family] += 1
        terms = generator["terms"]
        single_term_generators += len(terms) == 1
        degree = max(len(term[0]) for term in terms)
        histogram[(degree, len(terms))] += 1
    require(single_term_generators == 0,
            "the candidate acquired a one-term coefficient obstruction")
    ledger = {
        "artifact_sha256": hashlib.sha256(raw).hexdigest(),
        "branch": "334:63",
        "dynamic_nodes": stats["nodes"],
        "off_sigma_cells": len(extras),
        "sigma_cells": len(CANDIDATE_SIGMA_SUPPORT),
        "localized_variables": len(support),
        "shadow": shadow,
        "coefficient_generators": len(rebuilt["coefficient_generators"]),
        "single_term_generators": single_term_generators,
        "generator_family_memberships": dict(sorted(family_counts.items())),
        "degree_term_histogram": {
            "degree_%d_terms_%d" % key: value
            for key, value in sorted(histogram.items())
        },
        "generator_sha256": D.content_hash(
            rebuilt["coefficient_generators"]),
        "status": ("verified complete-shadow SAT support; exact localized "
                   "coefficient problem remains open"),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the branch-63 candidate ledger changed")
    return ledger, digest, monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-artifact", action="store_true")
    args = parser.parse_args()
    if args.write_artifact:
        raw = json.dumps(build_artifact(), sort_keys=True,
                         separators=(",", ":")).encode("ascii")
        with open(ARTIFACT_PATH, "wb") as handle:
            handle.write(raw)
        print("wrote:", ARTIFACT_PATH)
        print("sha256:", hashlib.sha256(raw).hexdigest())
        return
    ledger, digest, seconds = audit()
    print("n8 D1 m=10 branch 334:63 candidate: PASS (exact)")
    print("support: %d Sigma + %d off-Sigma localized cells"
          % (ledger["sigma_cells"], ledger["off_sigma_cells"]))
    print("complete fibres checked:", ledger["shadow"]["fibres_checked"])
    print("coefficient generators:", ledger["coefficient_generators"])
    print("generator sha256:", ledger["generator_sha256"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
