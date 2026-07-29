#!/usr/bin/env python3
"""Exact audit of the unique-illegal-core exchange repair."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import importlib.util
import math
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k2_updated_census as census_k2


def load(filename: str, name: str):
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


partial = load(
    "verify_live_three_zero_eighth_split_one_bad_core_repair.py",
    "partial_lift_for_unique_bad",
)
dual = load(
    "verify_live_three_zero_higher_split_antiderivative_wronskian.py",
    "dual_for_unique_bad",
)


def illegal_cores(profile: tuple[int, ...], h: int):
    result = []
    for core_tuple in combinations(range(len(profile)), h):
        core = set(core_tuple)
        takes = {index: 1 for index in core}
        if not frontier.leaves_singleton(profile, takes):
            result.append(frozenset(core))
    return tuple(result)


def unique_closed_form(profile: tuple[int, ...], h: int) -> bool:
    n1 = profile.count(1)
    nhigh = sum(part >= 3 for part in profile)
    need = h - n1
    return 0 <= need <= nhigh and math.comb(nhigh, need) == 1


def check_binomial_formula() -> None:
    for h in range(3, 10):
        for total in range(h + 1, h + 10):
            for profile in frontier.partitions(total):
                if len(profile) < h:
                    continue
                n1 = profile.count(1)
                nhigh = sum(part >= 3 for part in profile)
                need = h - n1
                expected_count = math.comb(nhigh, need) if 0 <= need <= nhigh else 0
                literal = illegal_cores(profile, h)
                assert len(literal) == expected_count
                assert unique_closed_form(profile, h) == (len(literal) == 1)
                endpoints = n1 == h or n1 + nhigh == h
                assert unique_closed_form(profile, h) == endpoints


def check_special_deletions() -> None:
    examples = (
        ((3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1), 8),
        ((3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1), 8),
    )
    for profile, h in examples:
        bad = illegal_cores(profile, h)
        assert len(bad) == 1
        core = set(bad[0])
        for outside in set(range(len(profile))) - core:
            assert profile[outside] >= 2
            special = core | {outside}
            assert len(special) == h + 1
            assert not frontier.leaves_singleton(
                profile, {index: 1 for index in core}
            )
            for omitted in core:
                deletion = special - {omitted}
                assert frontier.leaves_singleton(
                    profile, {index: 1 for index in deletion}
                )


def check_imported_analytic_ingredients() -> None:
    partial.check_hermite_and_exchange_degrees()
    partial.check_cubic_gauge_and_rational_lift()
    partial.check_partial_pencil_inequalities()
    partial.check_triple_zero_in_parity_determinant()
    partial.check_upward_propagation()
    dual.check_degrees_and_injectivity()
    dual.check_local_gauge_and_weights()
    dual.check_gcd_corrected_global_inequality()


def check_h8_k2_increment() -> None:
    old = set(census_k2.EXPECTED_RESIDUALS)
    additions = {
        profile
        for profile in old
        if unique_closed_form(profile, 8)
        and 1 <= 20 - len(profile) <= 8
    }
    expected = {
        (3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1),
        (3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1),
    }
    assert additions == expected
    assert {20 - len(profile) for profile in additions} == {7, 8}


def main() -> None:
    check_binomial_formula()
    check_special_deletions()
    check_imported_analytic_ingredients()
    check_h8_k2_increment()
    print("higher-split unique-illegal-core repair: PASS")
    print("illegal-core count binomial and endpoint characterization: exact")
    print("partial h-of-(h+1) lift applies to an arbitrary unique bad core")
    print("h=8,k=2 adds exactly 3^2 2^4 1^6 and 3 2^5 1^7")


if __name__ == "__main__":
    main()
