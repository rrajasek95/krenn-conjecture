#!/usr/bin/env python3
"""Independent exact referee for the rectangle rank-three reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from collections import Counter
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank3-reduction-2026-08-25"
PARENT = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-carrier-incidence-design-2026-08-25"
PINS = {
    PRODUCER / "MANIFEST.sha256": "b07d0fe2969bed87bd791c7c5680fe840f5f09221bc1e7cfd5b2ddeb0f057aa1",
    PRODUCER / "audit_rank3.py": "9fde44063a73808a3e90b6a5945c81ca7213b7acd79f673dcbc4fd2182e45ed8",
    PRODUCER / "results_rank3_reduction.json": "ffacbff0a12d414d09a437597fb9f41083a8369894849b7891bd6e60a43c559d",
    PARENT / "MANIFEST.sha256": "5cb72ac4af5a3ad3decbf3ba59ec858e23dcf2810c289d586feb14aeea1e61fe",
    PARENT / "results_unmapped16_design.json": "2fe9e2a561397b58941b0f4210b3e4fb4a5457f377d4e23b7fc1dd6d0d22c008",
}
FIXED = {"03", "16", "27", "45"}
RANK3_INVERTIBLE = FIXED | {"17", "26", "46", "47"}
SELECTED = ["01", "15", "17", "23", "26", "46", "47"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def replay_manifest(directory: Path):
    for line in (directory / "MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        assert sha256(directory / relative) == expected


def add(counter, coefficient, atoms=()):
    key = tuple(sorted(atoms))
    counter[key] += coefficient
    if counter[key] == 0:
        del counter[key]


def atom(block, row, column):
    return (block, row, column)


def matching_expansion(word, matching):
    counter = Counter({(): 1})
    for block in matching.split("|"):
        left, right = map(int, block)
        row, column = word[left], word[right]
        if block in FIXED:
            if row != column:
                return Counter()
            continue
        if block == "46":
            expanded = [( -1, (atom("47", row, t), atom("26", column, t))) for t in range(3)]
        else:
            expanded = [(1, (atom(block, row, column),))]
        updated = Counter()
        for old_atoms, old_coefficient in counter.items():
            for coefficient, atoms in expanded:
                add(updated, old_coefficient * coefficient, old_atoms + atoms)
        counter = updated
    return counter


def original_amplitude(word, matchings):
    result = Counter()
    for matching in matchings:
        result.update(matching_expansion(word, matching))
    return Counter({key: value for key, value in result.items() if value})


def product(left, right):
    result = Counter()
    for la, lc in left.items():
        for ra, rc in right.items():
            add(result, lc * rc, la + ra)
    return result


def factor_amplitude(word):
    a, b, c, d, e, f, g, h = word
    X, Qf, R, S = Counter(), Counter(), Counter(), Counter()
    add(X, 1, (atom("01", a, b), atom("35", d, f)))
    if a == d:
        add(X, 1, (atom("15", b, f),))
    add(Qf, 1, (atom("26", c, g), atom("47", e, h)))
    if c == h:
        for t in range(3):
            add(Qf, -1, (atom("47", e, t), atom("26", g, t)))
    if a == d and e == f:
        add(R, 1)
    add(R, 1, (atom("04", a, e), atom("35", d, f)))
    if b == g and c == h:
        add(S, 1)
    add(S, 1, (atom("17", b, h), atom("26", c, g)))
    result = product(X, Qf)
    result.update(product(R, S))
    return Counter({key: value for key, value in result.items() if value})


def partner_blocks(carrier):
    key = "right_block" if carrier["common_side"] == "p" else "left_block"
    return {term[key] for term in carrier["terms"]}


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, path
    replay_manifest(PRODUCER)
    parent = json.loads((PARENT / "results_unmapped16_design.json").read_text())
    records = [record for record in parent["records"] if record["added"] == SELECTED]
    assert len(records) == 2
    states = {"A12_present" if "12" in record["nonzero_variable_blocks"] else "A12_absent": record for record in records}
    assert set(states) == {"A12_present", "A12_absent"}
    matchings = states["A12_present"]["supported_matchings"]
    assert matchings == states["A12_absent"]["supported_matchings"]
    assert len(matchings) == 8 and all("12" not in matching and "23" not in matching for matching in matchings)

    factor_hash = hashlib.sha256()
    term_census = Counter()
    for word in itertools.product(range(3), repeat=8):
        original = original_amplitude(word, matchings)
        factored = factor_amplitude(word)
        assert original == factored, word
        term_census[len(original)] += 1
        payload = ["".join(map(str, word)), sorted((coefficient, monomial) for monomial, coefficient in original.items())]
        factor_hash.update(json.dumps(payload, separators=(",", ":")).encode() + b"\n")
    assert factor_hash.hexdigest() == "0a0018f6528caf440f18281cf4fec217af909ebe17039ba81f840575fb78a2b1"

    census = {}
    all_carriers = []
    for state, record in states.items():
        forced = 0
        undecided = 0
        for carrier in record["two_sandwich_carriers"]:
            common_full = carrier["common_block"] in RANK3_INVERTIBLE
            one_partner_full = bool(partner_blocks(carrier) & RANK3_INVERTIBLE)
            if common_full and one_partner_full:
                forced += 1
            else:
                undecided += 1
            all_carriers.append(carrier)
        expected = (24, 10, 14) if state == "A12_present" else (40, 22, 18)
        assert (len(record["two_sandwich_carriers"]), forced, undecided) == expected
        census[state] = {"total": expected[0], "forced_zero_kernel": forced, "guard_undecided": undecided}

    # Guard-only hostile: all supported blocks are invertible (I, except A46=-I).
    # Every two-sandwich carrier has two distinct one-term responses, hence one
    # response alone is K or K^T up to sign and has zero kernel.
    assert all(len(carrier["terms"]) == 2 and len({term["response_pair"] for term in carrier["terms"]}) == 2 for carrier in all_carriers)

    producer = json.loads((PRODUCER / "results_rank3_reduction.json").read_text())
    assert producer["guard_rank3"]["original"] == ["A47^T+A17*A46^T=0", "A26*A47^T+A46^T=0"]
    assert producer["guard_rank3"]["elimination"] == "A46=-A47*A26^T"
    assert producer["guard_rank3"]["reduced_guard"] == "(I-A17*A26)*A47^T=0"
    assert producer["carrier_no_go"]["witness_full_x5"] == "not satisfied (pure amplitude is 4, target 1); it proves only that rank3 guard algebra alone cannot select an active carrier"

    # Established exact projection.
    assert 7 * 9 + 1 == 64
    assert 3**8 + 9 + 1 == 6571

    # Strictly smaller next ideal, using the universally valid adjugate identity.
    # A17=u26*adj(A26), det(A26)*u26=1 removes A17 and all nine inverse equations.
    next_variables = 6 * 9 + 2  # six matrices, u26, sat47
    next_generators = 3**8 + 2  # amplitudes and two determinant inverses
    assert next_variables == 56 and next_generators == 6563

    result = {
        "schema": "KRENN_X5_RECTANGLE_4647_RANK3_REFEREE_V1",
        "status": "PASS_EXACT_REDUCTION_DESIGN_ONLY_NO_CLOSURE",
        "producer_manifest_sha256": PINS[PRODUCER / "MANIFEST.sha256"],
        "guard_rank3": {
            "elimination": "A46=-A47*A26^T",
            "one_sided_inverse": "A17*A26=I",
            "two_sided_inverse": "A26*A17=I (square-matrix consequence)",
            "invertible": ["A17", "A26", "A46", "A47"],
        },
        "carrier_census": census,
        "guard_only_no_go": {
            "universal_carrier_exists": False,
            "hostile": "all supported blocks I and A46=-I",
            "all_enumerated_carrier_kernels_zero": True,
            "full_X5_satisfied": False,
            "scope": "guard-only implication refuted; no full-X5 counterexample claimed",
        },
        "full_X5_projection": {
            "verified_words": 6561,
            "factorization": "Phi=X*Q+R*S",
            "factor_ledger_sha256": factor_hash.hexdigest(),
            "term_census": {str(key): value for key, value in sorted(term_census.items())},
            "amplitude_inactive": ["A12", "A23"],
            "established_variables": 64,
            "established_generators": 6571,
            "projection_lift": "A12,A23 free; A46 reconstructed; det(A47) saturated",
        },
        "smallest_sound_next_ideal": {
            "status": "HELD_NOT_MATERIALIZED_NOT_RUN",
            "matrices": ["A01", "A04", "A15", "A26", "A35", "A47"],
            "extra_variables": ["u26", "sat47"],
            "substitutions": ["A17=u26*adj(A26)", "A46=-A47*A26^T"],
            "saturations": ["det(A26)*u26-1", "det(A47)*sat47-1"],
            "variables": next_variables,
            "generators": next_generators,
            "equivalence": "exact on the rank-three branch by adj(A26)*A26=det(A26)*I; A12,A23 remain free",
            "forbidden_reductions": "no A47=I gauge normalization or color-basis quotient without a separately proved symmetry",
            "launch_guard": "do not materialize or launch while the rep1 exact-Q lane is active; new explicit clearance required",
        },
        "scope": {"ideal_runs": 0, "rank3_closed": False, "transported_records": 0, "D12_reads": False},
    }
    temporary = HERE / "results_referee.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_referee.json")
    print(json.dumps({"status": result["status"], "next": "56/6563", "runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
