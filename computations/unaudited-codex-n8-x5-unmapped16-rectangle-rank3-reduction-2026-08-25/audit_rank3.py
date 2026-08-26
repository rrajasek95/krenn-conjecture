#!/usr/bin/env python3
"""Exact analytic reduction of the rectangle-46/47 rank-three branch."""
from __future__ import annotations

import collections
import copy
import hashlib
import itertools
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-carrier-incidence-design-2026-08-25"
PINS = {
    PARENT / "MANIFEST.sha256": "5cb72ac4af5a3ad3decbf3ba59ec858e23dcf2810c289d586feb14aeea1e61fe",
    PARENT / "results_unmapped16_design.json": "2fe9e2a561397b58941b0f4210b3e4fb4a5457f377d4e23b7fc1dd6d0d22c008",
}
SELECTED = ["01", "15", "17", "23", "26", "46", "47"]
FORCED_INVERTIBLE = {"03", "16", "27", "45", "17", "26", "46", "47"}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def atom(block, i, j):
    return (block, i, j)


def mono(sign, *atoms):
    return (sign, tuple(sorted(atoms)))


def add(counter, sign, *atoms):
    if sign:
        key = tuple(sorted(atoms))
        counter[key] += sign
        if counter[key] == 0:
            del counter[key]


def original_expanded(word):
    """Eight supported matchings after A46=-A47*A26^T."""
    a, b, c, d, e, f, g, h = word
    out = collections.Counter()
    # 01|26|35|47
    add(out, 1, atom("01", a, b), atom("26", c, g), atom("35", d, f), atom("47", e, h))
    # 01|27|35|46
    if c == h:
        for t in range(3):
            add(out, -1, atom("01", a, b), atom("35", d, f), atom("47", e, t), atom("26", g, t))
    # 03|15|26|47 and 03|15|27|46
    if a == d:
        add(out, 1, atom("15", b, f), atom("26", c, g), atom("47", e, h))
        if c == h:
            for t in range(3):
                add(out, -1, atom("15", b, f), atom("47", e, t), atom("26", g, t))
    # 03|16|27|45 and 03|17|26|45
    if a == d and b == g and c == h and e == f:
        add(out, 1)
    if a == d and e == f:
        add(out, 1, atom("17", b, h), atom("26", c, g))
    # 04|16|27|35 and 04|17|26|35
    if b == g and c == h:
        add(out, 1, atom("04", a, e), atom("35", d, f))
    add(out, 1, atom("04", a, e), atom("17", b, h), atom("26", c, g), atom("35", d, f))
    return out


def factorized_expanded(word):
    """Expand X*Q+R*S from the report, as a signed monomial ledger."""
    a, b, c, d, e, f, g, h = word
    out = collections.Counter()
    x_terms = [(1, (atom("01", a, b), atom("35", d, f)))]
    if a == d:
        x_terms.append((1, (atom("15", b, f),)))
    q_terms = [(1, (atom("26", c, g), atom("47", e, h)))]
    if c == h:
        for t in range(3):
            q_terms.append((-1, (atom("47", e, t), atom("26", g, t))))
    for sx, xx in x_terms:
        for sq, qq in q_terms:
            add(out, sx * sq, *(xx + qq))
    r_terms = []
    if a == d and e == f:
        r_terms.append((1, ()))
    r_terms.append((1, (atom("04", a, e), atom("35", d, f))))
    s_terms = []
    if b == g and c == h:
        s_terms.append((1, ()))
    s_terms.append((1, (atom("17", b, h), atom("26", c, g))))
    for sr, rr in r_terms:
        for ss, values in s_terms:
            add(out, sr * ss, *(rr + values))
    return out


def partner_blocks(carrier):
    if carrier["common_side"] == "p":
        return {term["right_block"] for term in carrier["terms"]}
    return {term["left_block"] for term in carrier["terms"]}


def carrier_audit(record):
    injective, unresolved = [], []
    for carrier in record["two_sandwich_carriers"]:
        partners = partner_blocks(carrier)
        item = {
            "kind": carrier["kind"], "cap": carrier["cap"],
            "defining_sites": carrier["defining_sites"],
            "common_block": carrier["common_block"],
            "common_side": carrier["common_side"],
            "partner_blocks": sorted(partners),
            "identity_cap": carrier["identity_cap"],
        }
        # One full common factor and one full partner make K -> responses injective.
        if carrier["common_block"] in FORCED_INVERTIBLE and partners & FORCED_INVERTIBLE:
            item["rank3_consequence"] = "ZERO_KERNEL_FORCED_INACTIVE"
            injective.append(item)
        else:
            item["rank3_consequence"] = "NOT_DECIDED_BY_GUARD_RANK3"
            unresolved.append(item)
    return injective, unresolved


def validate(result):
    assert result["schema"] == "KRENN_X5_RECTANGLE_4647_RANK3_REDUCTION_V1"
    assert result["status"] == "PASS_EXACT_REDUCTION_NO_SOLVE"
    assert result["variants"]["A12_present"]["carrier_census"] == {"total": 24, "forced_injective_inactive": 10, "guard_undecided": 14}
    assert result["variants"]["A12_absent"]["carrier_census"] == {"total": 40, "forced_injective_inactive": 22, "guard_undecided": 18}
    assert result["reduced_ideal"]["variables"] == 64 and result["reduced_ideal"]["generators"] == 6571
    assert result["scope"] == {"groebner_launches": 0, "rank3_closed": False, "transported_records": 0}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    parent = json.loads((PARENT / "results_unmapped16_design.json").read_text())
    records = [record for record in parent["records"] if record["added"] == SELECTED]
    assert len(records) == 2
    by_state = {"A12_present" if "12" in r["nonzero_variable_blocks"] else "A12_absent": r for r in records}
    assert set(by_state) == {"A12_present", "A12_absent"}
    matching_ledger = by_state["A12_present"]["supported_matchings"]
    assert matching_ledger == by_state["A12_absent"]["supported_matchings"]
    assert matching_ledger == [
        "01|26|35|47", "01|27|35|46", "03|15|26|47", "03|15|27|46",
        "03|16|27|45", "03|17|26|45", "04|16|27|35", "04|17|26|35",
    ]
    assert all("12" not in value and "23" not in value for value in matching_ledger)

    polynomial_hasher = hashlib.sha256()
    term_census = collections.Counter()
    for word in itertools.product(range(3), repeat=8):
        original = original_expanded(word)
        factorized = factorized_expanded(word)
        assert original == factorized, (word, original, factorized)
        term_census[len(original)] += 1
        serial = ["".join(map(str, word)), sorted((coefficient, monomial) for monomial, coefficient in original.items())]
        polynomial_hasher.update(json.dumps(serial, separators=(",", ":")).encode() + b"\n")

    variants = {}
    for state, record in by_state.items():
        injective, unresolved = carrier_audit(record)
        expected = (24, 10, 14) if state == "A12_present" else (40, 22, 18)
        assert (len(record["two_sandwich_carriers"]), len(injective), len(unresolved)) == expected
        variants[state] = {
            "record_index": record["record_index"],
            "support": record["support"],
            "supported_matching_ledger": matching_ledger,
            "full_x5_depends_on_A12": False,
            "full_x5_depends_on_A23": False,
            "carrier_census": {"total": expected[0], "forced_injective_inactive": expected[1], "guard_undecided": expected[2]},
            "forced_injective_carriers": injective,
            "guard_undecided_carriers": unresolved,
        }

    result = {
        "schema": "KRENN_X5_RECTANGLE_4647_RANK3_REDUCTION_V1",
        "status": "PASS_EXACT_REDUCTION_NO_SOLVE",
        "guard_rank3": {
            "original": ["A47^T+A17*A46^T=0", "A26*A47^T+A46^T=0"],
            "rank_hypothesis": "det(A47)!=0",
            "elimination": "A46=-A47*A26^T",
            "reduced_guard": "(I-A17*A26)*A47^T=0",
            "consequences": ["A17*A26=I", "A26*A17=I", "A17,A26,A46,A47 are invertible", "rank(A46)=rank(A47)=3"],
        },
        "factorization": {
            "verified_words": 6561,
            "expanded_polynomial_ledger_sha256": polynomial_hasher.hexdigest(),
            "expanded_term_count_census": dict(sorted(term_census.items())),
            "formula": "Phi=X*Q+R*S",
            "X": "A01[x0,x1]*A35[x3,x5]+delta(x0,x3)*A15[x1,x5]",
            "Q": "A26[x2,x6]*A47[x4,x7]-delta(x2,x7)*(A47*A26^T)[x4,x6]",
            "R": "delta(x0,x3)*delta(x4,x5)+A04[x0,x4]*A35[x3,x5]",
            "S": "delta(x1,x6)*delta(x2,x7)+A17[x1,x7]*A26[x2,x6]",
        },
        "reduced_ideal": {
            "equivalence": "exact projection/lift for the rank(A47)=3 branch; A46 is reconstructed and A12,A23 are free amplitude-inactive blocks",
            "retained_matrices": ["A01", "A04", "A15", "A17", "A26", "A35", "A47"],
            "dropped_free_matrices": ["A12", "A23"],
            "variables": 64,
            "variable_count": "7*9 matrix entries + one determinant saturation variable",
            "generators": 6571,
            "generator_count": "6561 factorized full-X5 amplitudes + 9 entries of A17*A26-I + det(A47)*sat-1",
            "largest_amplitude_shape": "two products X*Q+R*S rather than eight matching terms",
        },
        "carrier_no_go": {
            "guard_only_universal_carrier": False,
            "witness_specialization": "fixed,A01,A04,A12,A15,A17,A23,A26,A35,A47=I and A46=-I",
            "witness_guard_replay": ["I+I*(-I)=0", "I*I+(-I)=0"],
            "witness_effect": "every enumerated two-sandwich response contains invertible factors, hence its K-map is injective and the carrier kernel is zero",
            "witness_full_x5": "not satisfied (pure amplitude is 4, target 1); it proves only that rank3 guard algebra alone cannot select an active carrier",
        },
        "variants": variants,
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {"groebner_launches": 0, "rank3_closed": False, "transported_records": 0},
    }
    validate(result)
    tests = {
        "closure_overclaim": hostile(result, lambda x: x["scope"].__setitem__("rank3_closed", True)),
        "launch_injection": hostile(result, lambda x: x["scope"].__setitem__("groebner_launches", 1)),
        "carrier_count_mutation": hostile(result, lambda x: x["variants"]["A12_present"]["carrier_census"].__setitem__("forced_injective_inactive", 11)),
        "variable_count_mutation": hostile(result, lambda x: x["reduced_ideal"].__setitem__("variables", 63)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    temporary = HERE / "results_rank3_reduction.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_rank3_reduction.json")
    print(json.dumps({"status": result["status"], "variables": 64, "generators": 6571,
                      "factorization_words": 6561, "launches": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
