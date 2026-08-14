#!/usr/bin/env python3
"""Unique external mate and migration of the first nonlinear PS_00 face.

On the twelve-cell nonlinear octagon fibre the first surviving face is
P0*S0*a*q45 at 000022:00.  This checker enumerates every DQ/PS path in that
row by missing-source-cell cost.  Apart from the original path, there is one
unique cost-one path: adjoining X=p_0(site 4, physical colour 2) gives the
mate X*S0*H*a.  Its complete response has a private PS_00 migration
X*S0*c*q35 at 101222:00.  A two-row polynomial identity makes the pair a
unit on the inherited active torus, so no recurrent minimum-cost circuit
occurs.
"""

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


PARENT_PATH = Path(__file__).with_name(
    "verify_n8_pure21_first_nonlinear_defect_complete_row_gate.py"
)
SPEC = spec_from_file_location("first_defect_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
F = module_from_spec(SPEC)
SPEC.loader.exec_module(F)
N = F.N
M = F.M
B = F.B


WORD = (0, 0, 0, 0, 2, 2)
TARGET_ROW = (WORD, 0, 0)
MIGRATION_ROW = ((1, 0, 1, 2, 2, 2), 0, 0)
X_KEY = (0, 4, 2)
X = B.variable("X")


def install_witness():
    M.reset_tables()
    for site in (0, 1, 3, 4):
        B.SECOND[(1, site, 2)] = B.constant(F.WITNESS[f"z{site}"])
    for left, right in ((0, 1), (0, 3), (0, 5), (1, 4),
                        (1, 5), (3, 4), (3, 5), (4, 5)):
        B.Q_EDGE[(left, right, 2, 2)] = B.constant(
            F.WITNESS[f"q{left}{right}"]
        )


def missing_q(left, right):
    return (left, right, WORD[left], WORD[right]) not in B.Q_EDGE


def enumerate_paths_by_cost():
    install_witness()
    paths = []
    for matching in B.matchings(B.SITES):
        additions = (("d", (0, 0)),) + tuple(
            ("q", (left, right, WORD[left], WORD[right]))
            for left, right in matching if missing_q(left, right)
        )
        paths.append(("DQ", matching, additions))

    for p_site in B.SITES:
        for s_site in B.SITES:
            if p_site == s_site:
                continue
            rest = tuple(site for site in B.SITES if site not in (p_site, s_site))
            for matching in B.matchings(rest):
                additions = []
                p_key = (0, p_site, WORD[p_site])
                s_key = (0, s_site, WORD[s_site])
                if p_key not in B.FIRST:
                    additions.append(("p", p_key))
                if s_key not in B.SECOND:
                    additions.append(("s", s_key))
                additions.extend(
                    ("q", (left, right, WORD[left], WORD[right]))
                    for left, right in matching if missing_q(left, right)
                )
                paths.append(("PS", p_site, s_site, matching, tuple(additions)))
    return tuple(paths)


PATHS = enumerate_paths_by_cost()


def path_cost(path):
    return len(path[-1])


def audit_minimal_classification():
    distribution = Counter((path[0], path_cost(path)) for path in PATHS)
    expected = Counter({
        ("DQ", 2): 2, ("DQ", 3): 5, ("DQ", 4): 8,
        ("PS", 0): 1, ("PS", 1): 1, ("PS", 2): 13,
        ("PS", 3): 33, ("PS", 4): 42,
    })
    require(distribution == expected, ("external path census changed", distribution))
    positive_minimum = min(path_cost(path) for path in PATHS if path_cost(path))
    minimal = tuple(path for path in PATHS if path_cost(path) == positive_minimum)
    expected_path = (
        "PS", 4, 1, ((0, 5), (2, 3)), (("p", X_KEY),)
    )
    require(positive_minimum == 1, ("positive minimum moved", positive_minimum))
    require(minimal == (expected_path,), ("unique external mate moved", minimal))
    M.reset_tables()
    return distribution, expected_path


def symbolic_pair():
    N.adjoin_symbolic()
    inherited_target = B.residual(0, 0, WORD)
    inherited_migration = B.residual(0, 0, MIGRATION_ROW[0])
    B.FIRST[X_KEY] = X
    target = B.residual(0, 0, WORD)
    migration = B.residual(0, 0, MIGRATION_ROW[0])
    return target, migration, inherited_target, inherited_migration


def audit_typed_migration():
    target, migration, inherited_target, inherited_migration = symbolic_pair()
    mate = B.product_polynomials((X, B.variable("S0"), B.variable("H"), B.variable("a")))
    expected_target = B.add(
        B.product_polynomials((
            B.variable("P0"), B.variable("S0"), B.variable("a"), B.variable("q45"),
        )),
        mate,
    )
    expected_migration = B.product_polynomials((
        X, B.variable("S0"), B.variable("c"), B.variable("q35"),
    ))
    require(target == expected_target, ("target mate row changed", target))
    require(not inherited_migration, "migration row was already occupied")
    require(migration == expected_migration,
            ("private migration polynomial changed", migration))
    require(B.subtract(target, inherited_target) == mate,
            "mate contribution did not isolate")

    typed = (
        ("000022", "00", "PS", "60|71|23|45", "P0*S0*a*q45"),
        ("000022", "00", "PS", "64|71|05|23", "X*S0*H*a"),
        ("101222", "00", "PS", "64|71|02|35", "X*S0*c*q35"),
    )
    M.reset_tables()
    return typed


EXPECTED_INCREMENTAL = (
    ("000022", "00", 2),
    ("020022", "01", 2),
    ("101222", "00", 2),
    ("121122", "01", 2),
    ("121222", "01", 2),
    ("121222", "02", 2),
    ("200022", "00", 2),
    ("220022", "01", 2),
    ("220022", "02", 2),
)


def audit_normalized_full_replay():
    install_witness()
    before = {
        key: B.residual(key[1], key[2], key[0])
        for key in F.ROWS
    }
    B.FIRST[X_KEY] = B.constant(2)
    after = {
        key: B.residual(key[1], key[2], key[0])
        for key in F.ROWS
    }
    incremental = tuple(
        ("".join(map(str, key[0])), f"{key[1]}{key[2]}", int(value))
        for key in F.ROWS
        if (value := M.P.evaluate(B.subtract(after[key], before[key])))
    )
    require(incremental == EXPECTED_INCREMENTAL,
            ("external mate migration ledger changed", incremental))
    require(M.P.evaluate(after[TARGET_ROW]) == 0,
            "X=2 did not cancel the original PS_00 face")
    require(M.P.evaluate(after[MIGRATION_ROW]) == 2,
            "the private migration stopped firing")
    final_nonzero = sum(bool(M.P.evaluate(after[key])) for key in F.ROWS)
    require(final_nonzero == 34, ("final full-row count moved", final_nonzero))
    M.reset_tables()
    return incremental, final_nonzero


def audit_two_row_unit_certificate():
    target, migration, _, _ = symbolic_pair()
    c_q35_target = B.multiply(
        B.multiply(B.variable("c"), B.variable("q35")), target
    )
    a_h_migration = B.multiply(
        B.multiply(B.variable("a"), B.variable("H")), migration
    )
    left = B.subtract(c_q35_target, a_h_migration)
    torus_unit = B.product_polynomials((
        B.variable("P0"), B.variable("S0"), B.variable("a"),
        B.variable("c"), B.variable("q35"), B.variable("q45"),
    ))
    require(left == torus_unit, ("two-row unit certificate changed", left, torus_unit))
    M.reset_tables()
    return (
        "c*q35*F(000022;00)-a*H*F(101222;00)="
        "P0*S0*a*c*q35*q45"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "classification", "typed", "replay", "unit"),
        default="all",
    )
    args = parser.parse_args()

    classification = typed = replay = unit = None
    if args.mode in ("all", "classification"):
        classification = audit_minimal_classification()
    if args.mode in ("all", "typed"):
        typed = audit_typed_migration()
    if args.mode in ("all", "replay"):
        replay = audit_normalized_full_replay()
    if args.mode in ("all", "unit"):
        unit = audit_two_row_unit_certificate()

    report = {
        "mode": args.mode,
        "all_operation_paths": len(PATHS),
        "minimum_positive_external_cost": 1,
        "minimum_external_mates": 1,
        "mate": "X=p0(site4,colour2)",
        "typed_rows": None if typed is None else len(typed),
        "incremental_migration_rows": None if replay is None else len(replay[0]),
        "final_nonzero_rows": None if replay is None else replay[1],
        "unit_certificate": unit,
        "minimum_external_recurrent_circuit": False,
        "scope": "unique minimum-cost external mate of 000022:00",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 pure-21 PS00 external minimal mate gate: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
