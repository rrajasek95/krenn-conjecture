#!/usr/bin/env python3
"""Abstract successor units and freeze the first arbitrary-tail contaminant.

Modulo a consistent Laurent character lattice, the twelve singleton
successor identities have core c*M with c in {1, 2, -2}.  A genuinely
support-independent cancellation is available if source provenance supplies
a parallel homogeneous row with exactly the same arbitrary tail T:

    c*M + T = 0,   u*T = 0,   c,u,M units.

Without that companion, an arbitrary term defeats the unit: c*M+N=0 is a
consistent two-class torus equation whenever N/M is a new character.

The first exact contaminant is the matching

    x03_01 * x14_00 * x25_02

in top word 000102 above support0+x25_01.  It reduces to a new Laurent class
N, raises character rank 24 to 25 with no bad dependency, and has no
parallel-N source row.  The full finite source is still empty because a
different translated target row becomes one-class; that target migration,
not an arbitrary-tail parallel collision, is the remaining mechanism.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_n8_one_bad_unit_repair_masks.py"
DEPENDENCY_SHA256 = (
    "d50ae7ab884e56cf3a1efb9a43da1cd3c9c7fa502e55113416b4c8c204c56435"
)
EXPECTED_LEDGER_SHA256 = (
    "8bb0a7d0d95969de62a1f85002873e66d37932b5ce7650d81bfe9b9ce73a5448"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


path = ROOT / DEPENDENCY
require(sha256(path.read_bytes()).hexdigest() == DEPENDENCY_SHA256,
        "the pinned repair-mask theorem changed")
spec = spec_from_file_location("one_bad_repair_masks", path)
R = module_from_spec(spec)
spec.loader.exec_module(R)
C = R.C


def add_polynomials(left, right, scalar=1):
    result = Counter(left)
    for monomial, coefficient in right.items():
        result[monomial] += Fraction(scalar) * coefficient
        if not result[monomial]:
            result.pop(monomial, None)
    return dict(result)


def scale_polynomial(polynomial, scalar):
    return {monomial: Fraction(scalar) * coefficient
            for monomial, coefficient in polynomial.items()
            if Fraction(scalar) * coefficient}


def abstract_parallel_collision(coefficient):
    coefficient = Fraction(coefficient)
    require(coefficient, "the core coefficient is not a unit")
    core = (("M", 1),)
    tail = (("T", 1),)
    first = {core: coefficient, tail: Fraction(1)}
    companion = {tail: Fraction(1)}
    difference = add_polynomials(first, companion, -1)
    require(difference == {core: coefficient},
            "the abstract parallel-tail cancellation changed")

    # With no companion, c+z=0 has the explicit torus solution z=-c.
    solution = -coefficient
    require(solution and coefficient + solution == 0,
            "the arbitrary one-tail countermodel changed")
    return {
        "core_coefficient": str(coefficient),
        "parallel_companion_conclusion": "c*M",
        "uncontrolled_tail_torus_solution": {"M": "1", "N": str(solution)},
    }


def reduced_polynomial(monomials, basis):
    result = Counter()
    traces = []
    for monomial in monomials:
        normal_form, coefficient, used = R.reduce_trace(monomial, basis)
        result[normal_form] += coefficient
        traces.append((normal_form, coefficient, used))
    return ({normal_form: coefficient
             for normal_form, coefficient in result.items() if coefficient},
            traces)


def successor_palette():
    palette = Counter()
    successor_count = 0
    for support in C.sorted_supports(1):
        identity = R.identity_data(support)
        for mask in identity["masks"]:
            if len(mask) != 1:
                continue
            successor = R.identity_data(support | mask)
            palette[
                successor["target_terms"],
                successor["trace_classes"],
                tuple(successor["trace_class_sums"]),
                successor["surviving_coefficient"],
            ] += 1
            successor_count += 1
    require(successor_count == 12 and palette == Counter({
        (3, 1, (1,), 1): 8,
        (6, 2, (-2, 0), -2): 2,
        (6, 2, (0, 2), 2): 2,
    }), "the two successor coefficient palettes changed")
    return palette


def first_contaminant_audit():
    base = C.sorted_supports(1)[0]
    first_successor = base | C.parse_support("25:01")
    identity = R.identity_data(first_successor)
    target = identity["target"]
    target_record = identity["records"][target]
    require(identity["target_label"] == ["top", [0, 0, 0, 1, 0, 2]]
            and identity["target_terms"] == 3
            and identity["trace_class_sums"] == [1],
            "the first successor trinomial changed")

    core, core_coefficient = next(iter(
        C.reduce_polynomial(target_record["live"], identity["basis"]).items()
    ))
    require(core_coefficient == 1,
            "the first successor core coefficient changed")

    mask = C.parse_support("25:02")
    require(mask in identity["masks"],
            "the first contaminating singleton mask changed")
    sources = identity["masks"][mask]
    require(len(sources) == 1 and sources[0][0] == target,
            "the contaminant stopped entering only the target row")
    contaminant = sources[0][1]
    require([C.cell_name(cell) for cell in contaminant]
            == ["03:01", "14:00", "25:02"],
            "the frozen contaminating matching changed")
    contaminant_class, contaminant_coefficient, _used = R.reduce_trace(
        contaminant, identity["basis"]
    )
    require(contaminant_coefficient == 1 and contaminant_class != core,
            "the contaminant stopped being a new positive Laurent class")

    contaminated_support = first_successor | mask
    contaminated_live = tuple(
        monomial for monomial in target_record["full"]
        if set(monomial) <= contaminated_support
    )
    contaminated_reduced, _traces = reduced_polynomial(
        contaminated_live, identity["basis"]
    )
    require(contaminated_reduced == {
        core: Fraction(1), contaminant_class: Fraction(1)
    }, "the contaminated row stopped reducing to M+N")

    binomial_rows = [C.exponent_difference(
        identity["records"][index]["live"][0],
        identity["records"][index]["live"][1],
    ) for index in identity["binomial_records"]]
    difference = Counter(dict(contaminant_class))
    difference.subtract(dict(core))
    difference = {cell: Fraction(value) for cell, value in difference.items()
                  if value}
    augmented_basis, augmented_dependencies = C.laurent_basis(
        binomial_rows + [difference]
    )
    require(len(identity["basis"]) == 24 and len(augmented_basis) == 25,
            "the contaminant relation stopped raising character rank")
    require(not any(C.character(dependency) == -1
                    for dependency in augmented_dependencies),
            "the formal M+N cancellation acquired bad holonomy")

    # Search the entire contaminated top/response source packet in the old
    # consistent quotient.  A literal parallel companion would reduce to a
    # nonzero scalar multiple of N alone.
    parallel = []
    reduction_histogram = Counter()
    for row, word, monomials in C.closure_fibres(1):
        live = tuple(monomial for monomial in monomials
                     if set(monomial) <= contaminated_support)
        if not live:
            continue
        reduced, _row_traces = reduced_polynomial(live, identity["basis"])
        reduction_histogram[len(reduced)] += 1
        if set(reduced) == {contaminant_class}:
            parallel.append([row, list(word), str(reduced[contaminant_class])])
    require(not parallel,
            "the first contaminant acquired a parallel homogeneous source row")

    # The actual finite support is nevertheless killed by another translated
    # target.  Record it to prevent promotion of this guard to a coefficient
    # counterexample.
    migrated = C.coefficient_audit(1, contaminated_support)
    require(migrated == {
        "type": "one_class_laurent_unit",
        "live_records": 109,
        "plus_binomials": 54,
        "laurent_rank": 24,
        "one_class_records": 27,
        "first_source_record": 4,
        "first_source_label": ["top", [0, 0, 2, 1, 0, 1]],
        "first_normal_form_terms": 6,
        "first_normal_form_coefficient": 1,
    }, "the translated-target migration changed")

    return {
        "base_support_cells": len(first_successor),
        "target_label": identity["target_label"],
        "target_terms_before_contamination": identity["target_terms"],
        "core_normal_form": [
            [C.cell_name(cell), exponent] for cell, exponent in core
        ],
        "contaminating_cell": "25:02",
        "contaminating_matching": [C.cell_name(cell) for cell in contaminant],
        "contaminant_normal_form": [
            [C.cell_name(cell), exponent]
            for cell, exponent in contaminant_class
        ],
        "contaminated_normal_form": "M+N",
        "base_character_rank": len(identity["basis"]),
        "augmented_character_rank": len(augmented_basis),
        "augmented_bad_dependencies": 0,
        "parallel_N_source_rows": parallel,
        "old_quotient_reduction_histogram": dict(sorted(
            reduction_histogram.items()
        )),
        "actual_source_target_migration": migrated,
    }


def main():
    palette = successor_palette()
    abstract = {
        str(coefficient): abstract_parallel_collision(coefficient)
        for coefficient in (1, 2, -2)
    }
    contaminant = first_contaminant_audit()
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "successor_palette": [
            [list(key), count] for key, count in sorted(palette.items())
        ],
        "abstract_parallel_collision": abstract,
        "first_exact_contaminant": contaminant,
        "verdict": (
            "the twelve sparse successor units share the Laurent core c*M; "
            "an arbitrary tail is removable only with a source-provenance "
            "parallel companion.  The matching x03_01*x14_00*x25_02 gives "
            "an independent class N with no such companion, so the proposed "
            "arbitrary-extra-term unit lemma is false.  The finite packet "
            "remains empty only by migration to another translated target"
        ),
        "scope": (
            "the abstract Laurent core and the first exact contaminating "
            "matching; this is not a new repair-layer census, does not claim "
            "a coefficient point, and does not exclude a stronger global "
            "identity coupling multiple translated targets"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"successor collision guard ledger changed: {digest}")

    print("N=8 one-bad successor parallel-collision guard: PASS")
    print("successor cores: 8*c=1, 2*c=2, 2*c=-2")
    print("first contaminant: x03_01*x14_00*x25_02 -> independent N")
    print("parallel N rows / augmented bad dependencies: 0 / 0")
    print("actual finite source: translated-target unit migration")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
