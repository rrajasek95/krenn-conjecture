#!/usr/bin/env python3
"""Classify every first extra internal q cell after the minimal E14 unit.

For each of the nine bright charts of 8fe3f8b, add one previously absent
internal decorated q cell with formal coefficient x.  Compare the frozen
G11 target/zero pair.  The base difference is the ordinary unit, so the
only question is the coefficient of x in the new defect.

The complete 1,020-record census has two nonzero source-defect types:

* a pure-11 unordered-hole bracket, giving an effective alternate X1
  matching; or
* a mixed-10 unordered-hole bracket, giving a typed offdiagonal attachment.

The latter is free-active when its physical edge is outside the selected
anchor union.  Seven literal anchor-contained records remain the smallest
two-tail guard.  Rank landing is not asserted.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
E14_PATH = "computations/verify_h3_c6_e14_minimal_enlargement_unit.py"
PINS = {
    E14_PATH:
        "d5682f9134ff3dafddb4908707e5ceaacb25ff8b37632e57d9f9f3a4b62f84a8",
    "notes/h3-c6-e14-minimal-enlargement-unit.md":
        "552adf8a24410d4b8a09e61809c9a40c40274ad9c49a7ffe01b7ceb0d5ea22a7",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "9d2224d743873367284bc527a6bbbcd8fb9cd09425082f54c39a60a57e736932"
)
X = "second_tail_x"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def cofactor(e14, b4, q_cells, word, p_site, s_site):
    answer = {}
    remainder = tuple(site for site in range(6)
                      if site not in (p_site, s_site))
    for tail in b4.perfect_matchings(remainder):
        value = {(): Q(1)}
        for physical in tail:
            decoration = (word[physical[0]], word[physical[1]])
            if decoration not in q_cells.get(physical, {}):
                value = {}
                break
            value = e14.multiply(value, q_cells[physical][decoration])
        answer = e14.add(answer, value)
    return answer


def response_row(e14, b4, q_cells, word):
    answer = {}
    for p_site in e14.CORE:
        for s_site in e14.CORE:
            if p_site == s_site:
                continue
            coefficient = cofactor(
                e14, b4, q_cells, word, p_site, s_site
            )
            if coefficient:
                answer[(p_site, s_site, word[p_site], word[s_site])] = (
                    coefficient
                )
    return answer


def subtract(e14, left, right):
    answer = {endpoint: dict(value) for endpoint, value in left.items()}
    for endpoint, value in right.items():
        negative = {monomial: -coefficient
                    for monomial, coefficient in value.items()}
        answer[endpoint] = e14.add(answer.get(endpoint, {}), negative)
    return {endpoint: value for endpoint, value in answer.items() if value}


def x_coefficient(defect):
    answer = {}
    for endpoint, polynomial in defect.items():
        coefficient = defaultdict(Q)
        for monomial, scalar in polynomial.items():
            if X not in monomial:
                continue
            reduced = list(monomial)
            reduced.remove(X)
            coefficient[tuple(reduced)] += scalar
        coefficient = {monomial: scalar
                       for monomial, scalar in coefficient.items() if scalar}
        if coefficient:
            answer[endpoint] = coefficient
    return answer


def defect_json(defect):
    return [
        [list(endpoint), [
            [list(monomial), str(coefficient)]
            for monomial, coefficient in sorted(polynomial.items())
        ]]
        for endpoint, polynomial in sorted(defect.items())
    ]


def anchor_union(b4, first_index, second_index):
    return frozenset(
        set(b4.UNARY_ANCHOR)
        | {(0, 1), (3, 4)}
        | set(b4.BRIGHT_TAILS[1][first_index - 1])
        | set(b4.BRIGHT_TAILS[2][second_index - 1])
    )


def classify_defect(q_cells, physical, decoration, defect, anchors):
    if not defect:
        return "unit_persists", None

    endpoint_labels = {endpoint[2:] for endpoint in defect}
    require(len(defect) == 2,
            "a one-cell defect stopped being an unordered-hole bracket")
    endpoints = tuple(defect)
    require(endpoints[0][:2] == tuple(reversed(endpoints[1][:2])),
            "the defect orientations stopped using one physical hole")
    require(len({tuple(sorted(polynomial.items()))
                 for polynomial in defect.values()}) == 1,
            "the two hole orientations lost their common q tail")
    require(all(len(polynomial) == 1 for polynomial in defect.values()),
            "a first extension acquired a multi-term common tail")

    if decoration == (1, 1):
        require(endpoint_labels == {(1, 1)},
                "a pure-11 cell lost its pure endpoint bracket")
        kind = "pure11_unordered_hole"
        route = "effective_alternate_X1_matching"
    else:
        require(decoration == (1, 0),
                f"an unexpected decoration changed the unit: {decoration}")
        require(endpoint_labels == {(1, 0), (0, 1)},
                "a mixed-10 cell lost its mixed endpoint bracket")
        kind = "mixed10_unordered_hole"
        route = (
            "anchor_contained_two_tail_guard"
            if physical in anchors
            else "nonanchor_offdiagonal_free_carrier"
        )

    # The candidate physical edge and the unique common-tail physical edge
    # complete the four sites outside the displayed endpoint hole.  This is
    # a literal augmented perfect matching, not an abstract defect scalar.
    hole = set(endpoints[0][:2])
    require(not (hole & set(physical)),
            "the new internal cell met its endpoint hole")
    tail_vertices = set(range(6)) - hole - set(physical)
    require(len(tail_vertices) == 2,
            "the common-tail physical edge stopped being determined")
    tail_physical = tuple(sorted(tail_vertices))
    word = None
    # Recover the relevant decoration from either target or zero word using
    # the defect endpoint labels and the candidate decoration.  Its presence
    # in q_cells is independently checked below by its formal coefficient.
    q_names = {name for polynomial in defect.values()
               for monomial in polynomial for name in monomial}
    if not q_names:
        require(any(q_cells.get(tail_physical, {}).values()),
                "the fixed common q tail vanished")
    return route, {
        "normalized_source_signature": kind,
        "endpoint_hole": sorted(hole),
        "common_tail_physical_edge": list(tail_physical),
        "common_tail_formal_parameters": sorted(q_names),
    }


def exact_stabilizer(b4):
    # The rational q00 coefficients deliberately choose a chart.  Record
    # that no nontrivial physical quotient is honest on this exact fibre;
    # the useful quotient below is by normalized source-defect signature.
    core = set((0, 1, 3, 4))
    weights = b4.Q00_WEIGHTS
    stabilizer = []
    for permutation in permutations(range(6)):
        if {permutation[site] for site in core} != core:
            continue
        transported = {
            tuple(sorted((permutation[left], permutation[right]))): value
            for (left, right), value in weights.items()
        }
        if transported == weights:
            stabilizer.append(permutation)
    require(stabilizer == [tuple(range(6))],
            "the exact rational fibre acquired a physical symmetry")
    return stabilizer


def audit():
    pin_dependencies()
    e14 = load(E14_PATH, "c6_e14_second_tail")
    b4 = e14.load(e14.B4_PATH, "c6_e14_second_tail_b4")

    records = []
    chart_counts = {}
    for first_index in (1, 2, 3):
        for second_index in (1, 2, 3):
            q_cells, _added, _selected = e14.q_inventory(
                b4, first_index, second_index
            )
            anchors = anchor_union(b4, first_index, second_index)
            counts = Counter()
            for left, right in combinations(range(6), 2):
                physical = (left, right)
                for left_colour in range(3):
                    for right_colour in range(3):
                        decoration = (left_colour, right_colour)
                        if decoration in q_cells.get(physical, {}):
                            continue
                        enlarged = {edge: dict(cells)
                                    for edge, cells in q_cells.items()}
                        enlarged.setdefault(physical, {})[decoration] = {
                            (X,): Q(1)
                        }
                        zero = response_row(
                            e14, b4, enlarged, e14.ZERO_WORD[first_index]
                        )
                        target = response_row(
                            e14, b4, enlarged, (1,) * 6
                        )
                        defect = x_coefficient(subtract(e14, zero, target))
                        route, typing = classify_defect(
                            q_cells, physical, decoration, defect, anchors
                        )
                        counts[route] += 1
                        record = {
                            "X1_tail_index": first_index,
                            "X2_tail_index": second_index,
                            "physical_edge": list(physical),
                            "decoration": list(decoration),
                            "route": route,
                        }
                        if typing is not None:
                            record["typing"] = typing
                            record["normalized_defect"] = defect_json(defect)
                        records.append(record)
            chart_counts[f"{first_index},{second_index}"] = dict(
                sorted(counts.items())
            )

    require(len(records) == 1020,
            f"the first second-tail universe changed: {len(records)}")
    totals = Counter(record["route"] for record in records)
    require(totals == Counter({
        "unit_persists": 969,
        "effective_alternate_X1_matching": 36,
        "nonanchor_offdiagonal_free_carrier": 8,
        "anchor_contained_two_tail_guard": 7,
    }), f"the second-tail route split changed: {totals}")

    affected = [record for record in records
                if record["route"] != "unit_persists"]
    signatures = Counter(
        record["typing"]["normalized_source_signature"]
        for record in affected
    )
    require(signatures == Counter({
        "pure11_unordered_hole": 36,
        "mixed10_unordered_hole": 15,
    }), f"the source-signature quotient changed: {signatures}")

    guard_records = [record for record in records
                     if record["route"] == "anchor_contained_two_tail_guard"]
    require(len(guard_records) == 7,
            "the literal anchor-contained guard count changed")
    require({tuple(record["decoration"]) for record in guard_records}
            == {(1, 0)},
            "an anchor guard lost its mixed-10 typing")

    # Freeze the full 1,020-record classification without bloating the note.
    classification_stream = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    )
    ledger = {
        "pins": PINS,
        "exact_physical_stabilizer": [list(item)
                                      for item in exact_stabilizer(b4)],
        "classification_record_count": len(records),
        "classification_stream_sha256": sha256(
            classification_stream.encode()
        ).hexdigest(),
        "chart_counts": chart_counts,
        "total_routes": dict(sorted(totals.items())),
        "source_signature_quotient": dict(sorted(signatures.items())),
        "affected_record_count": len(affected),
        "anchor_contained_guard_records": guard_records,
        "theorem": (
            "every first extra internal q cell after the minimal E14 "
            "enlargement either leaves the exact two-row unit unchanged, "
            "creates an effective alternate pure-X1 matching, or is a "
            "typed mixed-10 attachment.  Nonanchor mixed attachments enter "
            "the pinned free-carrier theorem.  Exactly seven literal "
            "anchor-contained mixed-10 records remain"
        ),
        "source_identity": (
            "for a nonparallel cell x, F_zero-F_target=1+x*D.  At a source "
            "zero xD=-1, so the complete unordered-hole bracket D is "
            "nonzero.  Pure-11 D is an effective diagonal matching; mixed-"
            "10 D is a typed offdiagonal response attachment"
        ),
        "symmetry_scope": (
            "the exact rational coefficient fibre has trivial physical "
            "stabilizer.  The honest compression is therefore the two-type "
            "normalized source-signature quotient, while all seven literal "
            "guard records are retained explicitly"
        ),
        "rank_scope": (
            "this is source attachment/effectiveness only.  The eight "
            "nonanchor records inherit the proved free-active route; no "
            "four-good or clean landing is asserted for the 36 diagonal "
            "or seven anchor-contained records"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"second-tail classification ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 C6 E14 first second-tail classification: PASS (exact)")
    print(f"records={ledger['classification_record_count']}")
    print(f"routes={ledger['total_routes']}")
    print(f"source_signatures={ledger['source_signature_quotient']}")
    print("minimal residual: seven anchor-contained mixed-10 guards")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
