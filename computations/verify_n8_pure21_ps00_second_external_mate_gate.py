#!/usr/bin/env python3
"""Minimum mates of X*S0*c*q35 and their terminal migrations.

Retain the first external cell X=p_0(4;2).  In the private row 101222:00,
the minimum positive missing-cell cost is one and there are exactly two
mates: X3=p_0(3;2) and X5=p_0(5;2).  Their private migrations are
X3*S0*b*c at 101200:00 and X5*S1*c*e at 111112:01.  A simultaneous
three-row identity has a torus-unit right side, excluding individual and
aggregate minimum-mate cancellation.  The two migrations lie on opposite
sides of the source word lexicographically, so cost-plus-lex is not a global
well-founded potential.
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
    "verify_n8_pure21_ps00_external_minimal_mate_gate.py"
)
SPEC = spec_from_file_location("external_first_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
E = module_from_spec(SPEC)
SPEC.loader.exec_module(E)
F = E.F
N = E.N
M = E.M
B = E.B


WORD = (1, 0, 1, 2, 2, 2)
TARGET_ROW = (WORD, 0, 0)
X3_KEY = (0, 3, 2)
X5_KEY = (0, 5, 2)
X3 = B.variable("X3")
X5 = B.variable("X5")
MIGRATION3_ROW = ((1, 0, 1, 2, 0, 0), 0, 0)
MIGRATION5_ROW = ((1, 1, 1, 1, 1, 2), 0, 1)


def install_symbolic_parent():
    N.adjoin_symbolic()
    B.FIRST[E.X_KEY] = E.X


def install_normalized_parent():
    E.install_witness()
    B.FIRST[E.X_KEY] = B.constant(2)


def enumerate_paths_by_cost():
    install_symbolic_parent()
    paths = []
    for matching in B.matchings(B.SITES):
        additions = (("d", (0, 0)),) + tuple(
            ("q", (left, right, WORD[left], WORD[right]))
            for left, right in matching
            if (left, right, WORD[left], WORD[right]) not in B.Q_EDGE
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
                    for left, right in matching
                    if (left, right, WORD[left], WORD[right]) not in B.Q_EDGE
                )
                paths.append(("PS", p_site, s_site, matching, tuple(additions)))
    return tuple(paths)


PATHS = enumerate_paths_by_cost()


def audit_minimal_classification():
    distribution = Counter((path[0], len(path[-1])) for path in PATHS)
    expected = Counter({
        ("DQ", 2): 3, ("DQ", 3): 6, ("DQ", 4): 6,
        ("PS", 0): 1, ("PS", 1): 2, ("PS", 2): 15,
        ("PS", 3): 38, ("PS", 4): 34,
    })
    require(distribution == expected, ("second external cost census changed", distribution))
    positive_minimum = min(len(path[-1]) for path in PATHS if path[-1])
    minimal = tuple(path for path in PATHS if len(path[-1]) == positive_minimum)
    expected_minimal = (
        ("PS", 3, 1, ((0, 2), (4, 5)), (("p", X3_KEY),)),
        ("PS", 5, 1, ((0, 2), (3, 4)), (("p", X5_KEY),)),
    )
    require(positive_minimum == 1, ("minimum positive cost moved", positive_minimum))
    require(minimal == expected_minimal, ("second minimum orbit moved", minimal))
    M.reset_tables()
    return distribution, minimal


def symbolic_rows():
    install_symbolic_parent()
    B.FIRST[X3_KEY] = X3
    B.FIRST[X5_KEY] = X5
    return (
        B.residual(0, 0, WORD),
        B.residual(0, 0, MIGRATION3_ROW[0]),
        B.residual(0, 1, MIGRATION5_ROW[0]),
    )


def audit_typed_migrations():
    target, migration3, migration5 = symbolic_rows()
    expected_target = B.product_polynomials((
        B.variable("S0"), B.variable("c"),
        B.add(
            B.multiply(E.X, B.variable("q35")),
            B.add(
                B.multiply(X3, B.variable("q45")),
                B.multiply(X5, B.variable("q34")),
            ),
        ),
    ))
    expected3 = B.product_polynomials((
        X3, B.variable("S0"), B.variable("b"), B.variable("c"),
    ))
    expected5 = B.product_polynomials((
        X5, B.variable("S1"), B.variable("c"), B.variable("e"),
    ))
    require(target == expected_target, ("aggregate minimum-mate row changed", target))
    require(migration3 == expected3, ("X3 migration changed", migration3))
    require(migration5 == expected5, ("X5 migration changed", migration5))

    typed = (
        ("101222", "00", "PS", "64|71|02|35", "X*S0*c*q35"),
        ("101222", "00", "PS", "63|71|02|45", "X3*S0*c*q45"),
        ("101222", "00", "PS", "65|71|02|34", "X5*S0*c*q34"),
        ("101200", "00", "PS", "63|71|02|45", "X3*S0*b*c"),
        ("111112", "01", "PS", "65|73|02|14", "X5*S1*c*e"),
    )
    M.reset_tables()
    return typed


EXPECTED_REPLAYS = {
    3: (
        ("101200", "00", 1),
        ("101222", "00", -2),
        ("111212", "01", -1),
        ("111212", "02", 1),
        ("121200", "01", 1),
        ("121222", "01", -5),
        ("121222", "02", 1),
    ),
    5: (
        ("101222", "00", -2),
        ("111112", "01", -2),
        ("111212", "01", -2),
        ("121122", "01", -2),
        ("200022", "00", -2),
        ("210012", "01", -2),
    ),
}


def audit_individual_replays():
    results = {}
    for site, value, migration_row in (
        (3, Q(1), MIGRATION3_ROW),
        (5, Q(-2), MIGRATION5_ROW),
    ):
        install_normalized_parent()
        before = {
            key: B.residual(key[1], key[2], key[0])
            for key in F.ROWS
        }
        B.FIRST[(0, site, 2)] = B.constant(value)
        after = {
            key: B.residual(key[1], key[2], key[0])
            for key in F.ROWS
        }
        incremental = tuple(
            ("".join(map(str, key[0])), f"{key[1]}{key[2]}", int(entry))
            for key in F.ROWS
            if (entry := M.P.evaluate(B.subtract(after[key], before[key])))
        )
        require(incremental == EXPECTED_REPLAYS[site],
                ("individual minimum-mate replay changed", site, incremental))
        require(M.P.evaluate(after[TARGET_ROW]) == 0,
                ("minimum mate did not cancel target", site))
        require(M.P.evaluate(after[migration_row]) == value,
                ("private migration value moved", site, migration_row))
        final_nonzero = sum(bool(M.P.evaluate(after[key])) for key in F.ROWS)
        require(final_nonzero == 32, ("full residual count moved", site, final_nonzero))
        results[site] = (incremental, final_nonzero)
    M.reset_tables()
    return results


def audit_aggregate_unit_certificate():
    target, migration3, migration5 = symbolic_rows()
    first = B.multiply(
        B.product_polynomials((B.variable("S1"), B.variable("e"), B.variable("b"))),
        target,
    )
    second = B.multiply(
        B.product_polynomials((B.variable("S1"), B.variable("e"), B.variable("q45"))),
        migration3,
    )
    third = B.multiply(
        B.product_polynomials((B.variable("S0"), B.variable("b"), B.variable("q34"))),
        migration5,
    )
    left = B.subtract(B.subtract(first, second), third)
    right = B.product_polynomials((
        E.X, B.variable("S0"), B.variable("S1"), B.variable("b"),
        B.variable("c"), B.variable("e"), B.variable("q35"),
    ))
    require(left == right, ("aggregate minimum-orbit certificate changed", left, right))
    M.reset_tables()
    return (
        "S1*e*b*F(101222;00)-S1*e*q45*F(101200;00)"
        "-S0*b*q34*F(111112;01)=X*S0*S1*b*c*e*q35"
    )


def audit_potential_boundary():
    target = ("101222", "00")
    migration3 = ("101200", "00")
    migration5 = ("111112", "01")
    require(migration3 < target < migration5,
            ("lexicographic straddling changed", migration3, target, migration5))
    # Both mates have the same missing-cell cost as the preceding external
    # mate.  Therefore neither (cost,lex) orientation is monotone on both
    # branches.  Along the private-face chase only, the active new tail edge
    # moves q45 -> q35 -> no new q edge, a local filtration but not yet a
    # theorem for the whole response graph.
    return {
        "cost_lex_global": False,
        "counterexample": "101200:00 < 101222:00 < 111112:01",
        "local_private_tail_filtration": "q45 -> q35 -> inherited-only",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "classification", "typed", "replay", "unit", "potential"),
        default="all",
    )
    args = parser.parse_args()

    classification = typed = replay = unit = potential = None
    if args.mode in ("all", "classification"):
        classification = audit_minimal_classification()
    if args.mode in ("all", "typed"):
        typed = audit_typed_migrations()
    if args.mode in ("all", "replay"):
        replay = audit_individual_replays()
    if args.mode in ("all", "unit"):
        unit = audit_aggregate_unit_certificate()
    if args.mode in ("all", "potential"):
        potential = audit_potential_boundary()

    report = {
        "mode": args.mode,
        "all_operation_paths": len(PATHS),
        "minimum_positive_external_cost": 1,
        "minimum_external_mates": ["X3=p0(site3,colour2)", "X5=p0(site5,colour2)"],
        "typed_rows": None if typed is None else len(typed),
        "individual_replay_rows": None if replay is None else {
            str(site): len(value[0]) for site, value in replay.items()
        },
        "aggregate_unit_certificate": unit,
        "minimum_external_recurrent_circuit": False,
        "potential": potential,
        "scope": "complete minimum-cost orbit over private row 101222:00",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 pure-21 PS00 second external mate gate: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
