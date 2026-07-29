#!/usr/bin/env python3
"""Exact audit for the pure (2,2,1) common-power obstruction.

This verifier covers all cross-colour support collisions.  It imports two
deterministic builders:

* explore_two_two_one_common_power.py: 195 support orbits, exact qF RREFs,
  and the unsaturated q^[2]-F ideals;
* explore_two_two_one_responses.py: the literal nine-product equations used
  to classify all 195 support orbits.

Every enumeration and generator stream is frozen by a SHA-256 ledger.  By
default Singular replays the 143 response-unit ideals first and then all 195
common-power unit ideals.  The other 52 response orbits are checked by
explicit coordinate solutions.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from itertools import combinations, product
import time

import explore_two_two_one_common_power as common_power
import explore_two_two_one_responses as responses


EXPECTED_ORBIT_LEDGER_SHA256 = (
    "68f24f11d160d5600efec4972f314da8ee6e1ab560e08f17901a63bb7102eb12"
)
EXPECTED_COMMON_POWER_GENERATOR_LEDGER_SHA256 = (
    "1cbb10f5acc01724fff0d44e981c0dbb1d731d8eff4e6a8ac7d92afb59d70a36"
)
EXPECTED_RESPONSE_WITNESS_LEDGER_SHA256 = (
    "f787c6ae228981d10d6a53f93ffbe4da26d8c40d686dbc0642c64cc91b033145"
)
EXPECTED_RESPONSE_UNIT_LEDGER_SHA256 = (
    "79bbf6ff63fa8192b2b2b3787e93c7d4fbe9d61cebd1f7767622ff36d67038e9"
)

EXPECTED_ORBIT_SIZE_HISTOGRAM = Counter({
    45: 3, 60: 2, 90: 8, 120: 2, 180: 31, 360: 85, 720: 64,
})
EXPECTED_DISTINCT_ORBITS = Counter({2: 2, 3: 23, 4: 76, 5: 94})
EXPECTED_DISTINCT_LABELLED = Counter({
    2: 210, 3: 5460, 4: 32760, 5: 45045,
})
EXPECTED_QF_RANK_NULLITY = Counter({
    (18, 117): 2,
    (27, 108): 23,
    (33, 102): 23,
    (35, 100): 23,
    (36, 99): 30,
    (39, 96): 35,
    (41, 94): 40,
    (43, 92): 19,
})

EXPECTED_RESPONSE_WITNESS_ORBITS = (
    13, 24, 25, 32, 36, 40, 42, 43, 45, 47, 60, 71, 83, 85, 86, 94,
    97, 103, 104, 108, 111, 113, 119, 126, 127, 128, 133, 135, 136,
    137, 140, 144, 145, 146, 147, 151, 153, 161, 167, 173, 176, 180,
    181, 182, 185, 186, 187, 188, 192, 193, 194, 195,
)
EXPECTED_RESPONSE_ORBITS = Counter({
    (2, False): 2,
    (3, False): 23,
    (4, False): 64,
    (4, True): 12,
    (5, False): 54,
    (5, True): 40,
})
EXPECTED_RESPONSE_LABELLED = Counter({
    (2, False): 210,
    (3, False): 5460,
    (4, False): 27360,
    (4, True): 5400,
    (5, False): 25650,
    (5, True): 19395,
})


def audit_weight_characters():
    """Check the elementary two-character rank behind weight normalization."""
    # Work additively.  The six target-preserving site exponents satisfy
    # sum t_u=0; a missing pair sees minus the sum on its two endpoints.
    # Subtracting the sixth coordinate gives a 5-coordinate presentation.
    projected = {}
    for pair in common_power.EDGES:
        row = []
        for variable_site in range(5):
            # t_5 = -sum_{0..4} t_u.
            coefficient = int(variable_site in pair)
            if 5 in pair:
                coefficient -= 1
            row.append(coefficient)
        projected[pair] = tuple(row)

    determinants = Counter()
    for left, right in combinations(common_power.EDGES, 2):
        rows = (projected[left], projected[right])
        minors = tuple(
            rows[0][a] * rows[1][b] - rows[0][b] * rows[1][a]
            for a, b in combinations(range(5), 2)
        )
        assert any(minors), (left, right, rows)
        determinants[tuple(sorted(set(abs(value) for value in minors if value)))] += 1
    assert sum(determinants.values()) == 105
    return determinants


def audit_target_colour_separation():
    """Verify the word-level direct sum used by the response equations."""
    checked = 0
    for left_colour, right_colour in combinations(common_power.COLOURS, 2):
        for left_pair, right_pair in product(common_power.EDGES, repeat=2):
            left_words = set()
            right_words = set()
            for a, b in product(common_power.COLOURS, repeat=2):
                word = [left_colour] * len(common_power.U)
                word[left_pair[0]], word[left_pair[1]] = a, b
                left_words.add(tuple(word))
                word = [right_colour] * len(common_power.U)
                word[right_pair[0]], word[right_pair[1]] = a, b
                right_words.add(tuple(word))
            assert left_words.isdisjoint(right_words)
            assert len(set(common_power.U) - set(left_pair) - set(right_pair)) >= 2
            checked += 1
    assert checked == 3 * 15**2 == 675
    return checked


def audit_common_power_ledgers():
    support_digest = hashlib.sha256()
    generator_digest = hashlib.sha256()
    orbit_sizes = Counter()
    distinct_orbits = Counter()
    distinct_labelled = Counter()
    ranks = Counter()

    for orbit, (support, orbit_size) in enumerate(common_power.REPRESENTATIVE_DATA, 1):
        support_digest.update(f"{support}:{orbit_size}\n".encode("ascii"))
        orbit_sizes[orbit_size] += 1
        distinct = common_power.distinct_pair_count(support)
        distinct_orbits[distinct] += 1
        distinct_labelled[distinct] += orbit_size

        variables, generators, rank = common_power.equations(support)
        nullity = len(variables)
        ranks[rank, nullity] += 1
        digest = common_power.ledger_digest(generators)
        generator_digest.update(
            f"{orbit}:{support}:{rank}:{nullity}:{len(generators)}:{digest}\n".encode("ascii")
        )

    assert len(common_power.PAIR_SETS) ** 2 * len(common_power.EDGES) == 165375
    assert sum(orbit_sizes.values()) == 195
    assert sum(size * count for size, count in orbit_sizes.items()) == 83475
    assert orbit_sizes == EXPECTED_ORBIT_SIZE_HISTOGRAM
    assert distinct_orbits == EXPECTED_DISTINCT_ORBITS
    assert distinct_labelled == EXPECTED_DISTINCT_LABELLED
    assert ranks == EXPECTED_QF_RANK_NULLITY
    assert support_digest.hexdigest() == EXPECTED_ORBIT_LEDGER_SHA256
    assert (
        generator_digest.hexdigest()
        == EXPECTED_COMMON_POWER_GENERATOR_LEDGER_SHA256
    )
    return support_digest.hexdigest(), generator_digest.hexdigest(), ranks


def audit_response_ledgers():
    witness_digest = hashlib.sha256()
    unit_digest = hashlib.sha256()
    witness_orbits = []
    unit_orbits = []
    orbit_histogram = Counter()
    labelled_histogram = Counter()

    for orbit, (support, orbit_size) in enumerate(common_power.REPRESENTATIVE_DATA, 1):
        distinct = common_power.distinct_pair_count(support)
        witnesses = responses.coordinate_witnesses(support)
        feasible = bool(witnesses)
        orbit_histogram[distinct, feasible] += 1
        labelled_histogram[distinct, feasible] += orbit_size
        if feasible:
            witness = witnesses[0]
            responses.audit_coordinate_witness(support, witness)
            witness_orbits.append(orbit)
            witness_digest.update(
                f"{orbit}:{support}:{orbit_size}:{witness}\n".encode("ascii")
            )
        else:
            variables, generators = responses.response_generators(support)
            digest = responses.ledger_digest(generators)
            unit_orbits.append(orbit)
            unit_digest.update(
                f"{orbit}:{support}:{orbit_size}:{len(variables)}:{len(generators)}:{digest}\n".encode("ascii")
            )

    assert tuple(witness_orbits) == EXPECTED_RESPONSE_WITNESS_ORBITS
    assert orbit_histogram == EXPECTED_RESPONSE_ORBITS
    assert labelled_histogram == EXPECTED_RESPONSE_LABELLED
    assert witness_digest.hexdigest() == EXPECTED_RESPONSE_WITNESS_LEDGER_SHA256
    assert unit_digest.hexdigest() == EXPECTED_RESPONSE_UNIT_LEDGER_SHA256
    assert len(unit_orbits) == 143
    return (
        tuple(witness_orbits), tuple(unit_orbits),
        witness_digest.hexdigest(), unit_digest.hexdigest(),
    )


def replay(label, selected, worker_count, runner, timeout):
    outputs = []
    wall_started = time.monotonic()
    with ThreadPoolExecutor(max_workers=worker_count) as pool:
        futures = {pool.submit(runner, orbit, timeout): orbit for orbit in selected}
        for future in as_completed(futures):
            result = future.result()
            status_index = 6 if label == "common-power" else 5
            status = result[status_index]
            assert status == "UNIT", (label, result)
            outputs.append(result)
            print(
                label, "orbit", result[0], "QQ ideal [1]",
                "seconds", f"{result[status_index + 1]:.3f}", flush=True,
            )
    print(label, "parallel wall seconds:", f"{time.monotonic() - wall_started:.3f}")
    return tuple(sorted(outputs))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, action="append", help="common-power orbit")
    parser.add_argument("--response-orbit", type=int, action="append")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--skip-common-power-ideals", action="store_true")
    parser.add_argument("--skip-response-ideals", action="store_true")
    args = parser.parse_args()

    character_minors = audit_weight_characters()
    separated_word_pairs = audit_target_colour_separation()
    support_digest, common_digest, ranks = audit_common_power_ledgers()
    witness_orbits, response_unit_orbits, witness_digest, response_digest = (
        audit_response_ledgers()
    )

    print("labelled supports before colour-0/1 swap:", 165375)
    print("labelled supports modulo colour-0/1 swap:", 83475)
    print("support orbits:", 195)
    print("distinct-pair orbit counts:", dict(sorted(EXPECTED_DISTINCT_ORBITS.items())))
    print("distinct-pair labelled counts:", dict(sorted(EXPECTED_DISTINCT_LABELLED.items())))
    print("orbit-ledger sha256:", support_digest)
    print("weight-character nonzero-minor patterns:", dict(sorted(character_minors.items())))
    print("distinct-colour word-space pairs checked:", separated_word_pairs)
    print("qF rank/nullity histogram:", dict(sorted(ranks.items())))
    print("common-power generator-ledger sha256:", common_digest)
    print("coordinate-response orbits:", len(witness_orbits))
    print("coordinate-response labelled supports:", 24795)
    print("repeated-support coordinate-response orbits:", 12)
    print("repeated-support coordinate-response labelled supports:", 5400)
    print("response-witness-ledger sha256:", witness_digest)
    print("proper non-coordinate response ideals:", 0)
    print("response-unit orbits:", len(response_unit_orbits))
    print("response-unit-ledger sha256:", response_digest)

    common_selected = list(args.orbit or range(1, 196))
    if any(orbit < 1 or orbit > 195 for orbit in common_selected):
        raise SystemExit("--orbit must lie in 1..195")
    response_selected = list(args.response_orbit or response_unit_orbits)
    if any(orbit not in response_unit_orbits for orbit in response_selected):
        raise SystemExit("--response-orbit must be one of the 89 frozen unit orbits")

    if not args.skip_response_ideals:
        replay(
            "response", response_selected, args.workers,
            lambda orbit, timeout: responses.run(orbit, timeout, False),
            args.timeout,
        )
    else:
        print("response ideals skipped by request")
    if not args.skip_common_power_ideals:
        replay(
            "common-power", common_selected, args.workers,
            common_power.run, args.timeout,
        )
    else:
        print("common-power ideals skipped by request")
    print("two-two-one monomial common-power obstruction exact audit: PASS")


if __name__ == "__main__":
    main()
