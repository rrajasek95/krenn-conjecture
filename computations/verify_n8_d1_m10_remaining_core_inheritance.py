#!/usr/bin/env python3
"""Certify the common 16-fibre core across the remaining m=10 branches."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED = {
    "audit_n8_d1_m10_support_frontier.py":
        "40500a706dd0ba82a25df26cea95ff8231245c367f4350b9c2d9363ff1ffb64a",
    "verify_n8_d1_m10_first_core_rup.py":
        "5b9a8f2ba5d5ce4e9a511396a78041bbd76b87b64741dd8adbc3391dfa7f97dc",
    "verify_n8_d1_m10_additional_core_rups.py":
        "7724d1f348f726fbb7015e0279512e45463dc7951f77280ea76afb50242e8f03",
}
for filename, expected in PINNED.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == expected,
                "a pinned m=10 core dependency changed: " + filename)

A = importlib.import_module("audit_n8_d1_m10_support_frontier")
R = importlib.import_module("verify_n8_d1_m10_first_core_rup")
C = importlib.import_module("verify_n8_d1_m10_additional_core_rups")
V, N, D = A.V, A.N, A.D

MODELS_PATH = os.path.join(
    HERE, "certificates", "n8_d1_m10_remaining_core_models.json.gz"
)
EXPECTED_MODELS_RAW_SHA256 = (
    "428995b49686b142468f5143d92855ea3aa74fba7f0243e4c963a9cb7266e06d"
)
EXPECTED_MODELS_GZIP_SHA256 = (
    "d4a741aed0b91e6240079cb917038e3d4c96b241b5107f292c07f34813af8728"
)
EXPECTED_PROOFS = {
    "433:46": (3449, 12563,
               "0dc01d0d42b6f5de442d627b964ddbddccea1c246c50b58efb45277c4a19b39a",
               30,
               "ed24cdb01d6761dd27bb7076b492348b8ade8d60fed38e55cea6c6e0ef90ca02",
               "ad61bbadc19a350fe59e32fb4bf6de98d591b87784f2b3cc737d18a576e6c749",
               14909),
    "433:47": (3449, 12563,
               "f52903cd240ab81827d3c444d1889a4dfc4c48bbcf94b6e7c91f40f94122177a",
               30,
               "ed24cdb01d6761dd27bb7076b492348b8ade8d60fed38e55cea6c6e0ef90ca02",
               "ad61bbadc19a350fe59e32fb4bf6de98d591b87784f2b3cc737d18a576e6c749",
               14910),
    "433:48": (3449, 12563,
               "b0cd75c8f702cbad555cfafa30b65da7611b5c32d4f9f2fc7ab28e787cd8c365",
               30,
               "ed24cdb01d6761dd27bb7076b492348b8ade8d60fed38e55cea6c6e0ef90ca02",
               "ad61bbadc19a350fe59e32fb4bf6de98d591b87784f2b3cc737d18a576e6c749",
               14910),
}
EXPECTED_LEDGER_SHA256 = (
    "7efb8044156fc1dcd6560baa9566563fd9d38532d2e0ac801a50ff39d9344a93"
)

FAMILY_SPECS = (
    ("334", "triple", "triple", 4, 132),
    ("343", "triple", "special", 3, 58),
    ("433", "special", "triple", 3, 58),
    ("442", "special", "special", 2, 23),
)
PREVIOUSLY_CLOSED_SURVIVORS = frozenset({
    ("334", 0), ("433", 0), ("442", 1),
})


def proof_path(family, index):
    return os.path.join(
        HERE, "certificates",
        "n8_d1_m10_inherited_%s_%d.glucose42.drup.gz" % (family, index),
    )


def surviving_branches():
    admissible, sigma, off_sigma, _kinds = V.reconstruct_support_domains()
    off_cells = sorted(off_sigma)
    cell_index = {entry: index for index, entry in enumerate(off_cells)}
    group = V.d1_group()
    states = {
        "triple": [N.triple_states(colour) for colour in (0, 1)],
        "special": [N.special_four_supports(colour)[0]
                    for colour in (0, 1)],
    }
    result = []
    for family, left_kind, right_kind, additions, expected_survivors in FAMILY_SPECS:
        _labelled, representatives = A.M8.state_pair_orbits(
            states[left_kind][0], states[right_kind][1], group
        )
        survivors = []
        for index, state in enumerate(representatives):
            witness, _certificate_count, _memo_states = A.repair_witness(
                state, additions, admissible, sigma, off_sigma,
                off_cells, cell_index,
            )
            if witness is not None:
                survivors.append((family, index, state))
        require(len(survivors) == expected_survivors,
                "the %s repair-DNF survivor count changed" % family)
        result.extend(survivors)
    require(len(result) == 271, "the aggregate repair-DNF frontier changed")
    remaining = [row for row in result
                 if row[:2] not in PREVIOUSLY_CLOSED_SURVIVORS]
    require(len(remaining) == 268,
            "the post-certificate m=10 frontier changed")
    return remaining, admissible, sigma, off_sigma


def build_branch_cnf(state, admissible, sigma, off_sigma):
    base, anchor_units = state
    cnf = C.build_core_cnf(base, admissible, sigma, off_sigma)
    for entry in sorted(anchor_units):
        require(("SIGMA", entry) in cnf.ids,
                "an anchor unit is outside Sigma")
        cnf.add(cnf.ids[("SIGMA", entry)])
    return cnf


def model_satisfies(cnf, positive_mask):
    require(positive_mask >= 0
            and positive_mask.bit_length() <= cnf.variable_count,
            "a model uses an out-of-range variable")
    for clause in cnf.clauses:
        if not any(((positive_mask >> (abs(literal) - 1)) & 1)
                   == (literal > 0) for literal in clause):
            return False
    return True


def audit():
    started = monotonic()
    branches, admissible, sigma, off_sigma = surviving_branches()
    with open(MODELS_PATH, "rb") as handle:
        models_compressed = handle.read()
    models_raw = gzip.decompress(models_compressed)
    models = json.loads(models_raw.decode("ascii"))
    require(hashlib.sha256(models_raw).hexdigest()
            == EXPECTED_MODELS_RAW_SHA256,
            "the inherited-core SAT model payload changed")
    require(hashlib.sha256(models_compressed).hexdigest()
            == EXPECTED_MODELS_GZIP_SHA256,
            "the inherited-core compressed SAT models changed")

    sat_rows, unsat_rows = [], []
    for family, index, state in branches:
        key = "%s:%d" % (family, index)
        cnf = build_branch_cnf(state, admissible, sigma, off_sigma)
        input_sha = hashlib.sha256(A.dimacs_bytes(cnf)).hexdigest()
        if key in models:
            positive_mask = int(models[key], 16)
            require(model_satisfies(cnf, positive_mask),
                    "the %s inherited-core SAT model is invalid" % key)
            sat_rows.append((key, cnf.variable_count, len(cnf.clauses),
                             input_sha, models[key]))
            continue
        path = proof_path(family, index)
        with open(path, "rb") as handle:
            compressed = handle.read()
        raw = gzip.decompress(compressed)
        proof = R.parse_proof(raw)
        checker = R.RUPDatabase(cnf.clauses, cnf.variable_count)
        require(not checker.root_conflict,
                "the %s core unit-refutes before its proof" % key)
        for proof_index, clause in enumerate(proof):
            require(checker.check_and_add(clause),
                    "%s proof addition %d is not RUP"
                    % (key, proof_index))
        require(proof and proof[-1] == () and checker.root_conflict,
                "the %s proof does not end in checked empty" % key)
        row = (cnf.variable_count, len(cnf.clauses), input_sha,
               len(proof), hashlib.sha256(raw).hexdigest(),
               hashlib.sha256(compressed).hexdigest(), checker.propagations)
        require(row == EXPECTED_PROOFS[key],
                "the checked %s proof ledger changed" % key)
        unsat_rows.append((key,) + row)

    require(len(sat_rows) == 265 and len(unsat_rows) == 3,
            "the common-core classification changed")
    require([row[0] for row in unsat_rows]
            == ["433:46", "433:47", "433:48"],
            "the inherited UNSAT branches changed")
    require(len({row[5] for row in unsat_rows}) == 1,
            "the three branches no longer share one RUP template")
    smallest = min(sat_rows, key=lambda row: (row[1], row[2], row[0]))
    states_by_key = {"%s:%d" % (family, index): state
                     for family, index, state in branches}
    smallest_state = states_by_key[smallest[0]]
    ledger = {
        "pinned_sources": PINNED,
        "starting_symbolic_branches": 268,
        "common_core_fibres": len(A.CORE_FIBRES),
        "checked_SAT_models": len(sat_rows),
        "checked_UNSAT_proofs": len(unsat_rows),
        "closed_branches": [row[0] for row in unsat_rows],
        "SAT_rows_sha256": D.content_hash(sat_rows),
        "UNSAT_rows": unsat_rows,
        "shared_RUP_template_raw_sha256": unsat_rows[0][5],
        "shared_RUP_template_instances": len(unsat_rows),
        "models_raw_sha256": hashlib.sha256(models_raw).hexdigest(),
        "models_gzip_sha256": hashlib.sha256(models_compressed).hexdigest(),
        "smallest_new_survivor": {
            "branch": smallest[0],
            "variables": smallest[1],
            "clauses": smallest[2],
            "dimacs_sha256": smallest[3],
            "base": [list(entry) for entry in sorted(smallest_state[0])],
            "anchor_units": [list(entry)
                             for entry in sorted(smallest_state[1])],
            "additional_off_Sigma_cells": 2,
            "verified_model": smallest[4],
        },
        "remaining_symbolic_branches": 265,
        "certificate": ("all SAT rows have directly checked models; all "
                        "UNSAT rows have independently checked deletion-free "
                        "RUP proofs ending in empty"),
    }
    digest = D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "the remaining-core inheritance ledger changed")
    return ledger, digest, smallest, monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-smallest-dimacs", metavar="PATH")
    args = parser.parse_args()
    ledger, digest, smallest, seconds = audit()
    if args.emit_smallest_dimacs:
        branches, admissible, sigma, off_sigma = surviving_branches()
        family, index = smallest[0].split(":")
        state = next(state for f, i, state in branches
                     if (f, i) == (family, int(index)))
        encoded = A.dimacs_bytes(
            build_branch_cnf(state, admissible, sigma, off_sigma)
        )
        with open(args.emit_smallest_dimacs, "wb") as handle:
            handle.write(encoded)
        print("wrote:", args.emit_smallest_dimacs)
    print("n8 D1 m=10 common-core inheritance: PASS (exact)")
    print("268 branches: 3 checked UNSAT; 265 checked SAT models")
    print("closed:", ", ".join(ledger["closed_branches"]))
    print("smallest new survivor:", ledger["smallest_new_survivor"]["branch"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
