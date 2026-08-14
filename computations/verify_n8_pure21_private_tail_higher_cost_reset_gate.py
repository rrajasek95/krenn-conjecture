#!/usr/bin/env python3
"""Higher-cost reset of the private-tail filtration.

The minimum-mate chase suggested q45 -> q35 -> inherited-only.  Enumerate
all independent external DQ/PS paths of cost at least two for the two
terminal rows R3=101200:00 and R5=111112:01.  Of 206 such paths, 204 create
an incremental monomial containing active q45 or q35; every cost >=3 path
does.  The smallest reset is the cost-two DQ mate of R3 obtained from a new
direct A00 and mixed edge L13.  It returns to 101222:00 and forms a coarse
three-state SCC, but its two rows have an exact torus-unit certificate.
"""

import argparse
from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


PARENT_PATH = Path(__file__).with_name(
    "verify_n8_pure21_ps00_second_external_mate_gate.py"
)
SPEC = spec_from_file_location("second_external_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
S = module_from_spec(SPEC)
SPEC.loader.exec_module(S)
E = S.E
F = S.F
N = S.N
M = S.M
B = S.B


BRANCHES = {
    3: {"word": (1, 0, 1, 2, 0, 0), "head": (0, 0)},
    5: {"word": (1, 1, 1, 1, 1, 2), "head": (0, 1)},
}
ALL_ROWS = tuple(
    (word, row, column)
    for word in product(B.COLORS, repeat=6)
    for row in B.COLORS
    for column in B.COLORS
)


def install_branch(branch):
    S.install_symbolic_parent()
    if branch == 3:
        B.FIRST[S.X3_KEY] = S.X3
    else:
        B.FIRST[S.X5_KEY] = S.X5


def enumerate_branch_paths(branch):
    install_branch(branch)
    word = BRANCHES[branch]["word"]
    row, column = BRANCHES[branch]["head"]
    paths = []
    for matching in B.matchings(B.SITES):
        additions = []
        if (row, column) not in B.DIRECT:
            additions.append(("d", (row, column)))
        additions.extend(
            ("q", (left, right, word[left], word[right]))
            for left, right in matching
            if (left, right, word[left], word[right]) not in B.Q_EDGE
        )
        paths.append(("DQ", matching, tuple(additions)))

    for p_site in B.SITES:
        for s_site in B.SITES:
            if p_site == s_site:
                continue
            rest = tuple(site for site in B.SITES if site not in (p_site, s_site))
            for matching in B.matchings(rest):
                additions = []
                p_key = (row, p_site, word[p_site])
                s_key = (column, s_site, word[s_site])
                if p_key not in B.FIRST:
                    additions.append(("p", p_key))
                if s_key not in B.SECOND:
                    additions.append(("s", s_key))
                additions.extend(
                    ("q", (left, right, word[left], word[right]))
                    for left, right in matching
                    if (left, right, word[left], word[right]) not in B.Q_EDGE
                )
                paths.append(("PS", p_site, s_site, matching, tuple(additions)))
    return tuple(paths)


PATHS = {branch: enumerate_branch_paths(branch) for branch in BRANCHES}


EXPECTED_DISTRIBUTIONS = {
    3: Counter({
        ("DQ", 2): 1, ("DQ", 3): 4, ("DQ", 4): 10,
        ("PS", 0): 1, ("PS", 2): 11, ("PS", 3): 28, ("PS", 4): 50,
    }),
    5: Counter({
        ("DQ", 1): 1, ("DQ", 2): 4, ("DQ", 3): 10,
        ("PS", 0): 1, ("PS", 1): 1, ("PS", 2): 14,
        ("PS", 3): 34, ("PS", 4): 40,
    }),
}


def audit_cost_census():
    answer = {}
    for branch, paths in PATHS.items():
        distribution = Counter((path[0], len(path[-1])) for path in paths)
        require(distribution == EXPECTED_DISTRIBUTIONS[branch],
                ("terminal branch cost distribution changed", branch, distribution))
        answer[branch] = distribution
    return answer


def install_additions(path):
    for index, (kind, key) in enumerate(path[-1]):
        table = {
            "d": B.DIRECT, "p": B.FIRST, "s": B.SECOND, "q": B.Q_EDGE,
        }[kind]
        table[key] = B.variable(f"u{index}")


def active_tail_hit(differences):
    for key in ALL_ROWS:
        word = key[0]
        if not ((word[4] == word[5] == 2) or (word[3] == word[5] == 2)):
            continue
        polynomial_value = differences(key)
        monomials = sorted(
            monomial for monomial in polynomial_value
            if "q45" in monomial or "q35" in monomial
        )
        if monomials:
            return ("".join(map(str, word)), f"{key[1]}{key[2]}", monomials[0])
    return None


def audit_all_higher_cost_resets():
    result = {}
    exceptions = {}
    for branch, paths in PATHS.items():
        install_branch(branch)
        base = {
            key: B.residual(key[1], key[2], key[0])
            for key in ALL_ROWS
        }
        counts = Counter()
        branch_exceptions = []
        first_reset = None
        for index, path in enumerate(paths):
            cost = len(path[-1])
            if cost < 2:
                continue
            install_branch(branch)
            install_additions(path)

            def difference(key):
                return B.subtract(
                    B.residual(key[1], key[2], key[0]), base[key]
                )

            hit = active_tail_hit(difference)
            counts[(cost, hit is not None)] += 1
            if hit is None:
                branch_exceptions.append((cost, index, path))
            elif first_reset is None or cost < first_reset[0]:
                first_reset = (cost, index, path, hit)
        result[branch] = counts
        exceptions[branch] = tuple(branch_exceptions)

        expected_counts = {
            3: Counter({
                (2, True): 11, (2, False): 1,
                (3, True): 32, (4, True): 60,
            }),
            5: Counter({
                (2, True): 17, (2, False): 1,
                (3, True): 44, (4, True): 40,
            }),
        }[branch]
        require(counts == expected_counts,
                ("higher-cost reset classification changed", branch, counts))
        require(first_reset is not None and first_reset[0] == 2,
                ("first reset cost moved", branch, first_reset))

    expected_exceptions = {
        3: ((
            2, 93,
            ("PS", 5, 1, ((0, 2), (3, 4)),
             (("p", (0, 5, 0)), ("q", (3, 4, 2, 0)))),
        ),),
        5: ((
            2, 5,
            ("DQ", ((0, 2), (1, 5), (3, 4)),
             (("q", (1, 5, 1, 2)), ("q", (3, 4, 1, 1)))),
        ),),
    }
    require(exceptions == expected_exceptions,
            ("non-reset exceptions changed", exceptions))
    M.reset_tables()
    return result, exceptions


def audit_smallest_reset_cycle():
    # The unique branch-3 DQ path of cost two adds A00 and L13.  On R3 it
    # uses the inherited b=q45^(0,0); on the parent row the same fine matching
    # uses active q45=q45^(2,2), resetting the prior tail state.
    install_branch(3)
    a00 = B.variable("A00")
    l13 = B.variable("L13")
    B.DIRECT[(0, 0)] = a00
    B.Q_EDGE[(1, 3, 0, 2)] = l13
    r3 = B.residual(0, 0, (1, 0, 1, 2, 0, 0))
    r0 = B.residual(0, 0, (1, 0, 1, 2, 2, 2))
    expected_r3 = B.product_polynomials((
        B.variable("b"), B.variable("c"),
        B.add(B.multiply(S.X3, B.variable("S0")), B.multiply(a00, l13)),
    ))
    expected_r0 = B.multiply(
        B.variable("c"),
        B.add(
            B.multiply(E.X, B.multiply(B.variable("S0"), B.variable("q35"))),
            B.multiply(
                B.variable("q45"),
                B.add(B.multiply(S.X3, B.variable("S0")), B.multiply(a00, l13)),
            ),
        ),
    )
    require(r3 == expected_r3, ("cost-two reset target changed", r3))
    require(r0 == expected_r0, ("cost-two reset landing changed", r0))

    left = B.subtract(
        B.multiply(B.variable("b"), r0),
        B.multiply(B.variable("q45"), r3),
    )
    right = B.product_polynomials((
        E.X, B.variable("S0"), B.variable("b"),
        B.variable("c"), B.variable("q35"),
    ))
    require(left == right, ("reset SCC unit certificate changed", left, right))
    M.reset_tables()
    return {
        "target": "101200:00",
        "mate_operation": "DQ",
        "mate_fine": "67|02|13|45",
        "new_cells": ["A00=direct(00)", "L13=q13^(0,2)"],
        "reset_landing": "101222:00",
        "reset_fine": "67|02|13|45",
        "certificate": "b*R0-q45*R3=X*S0*b*c*q35",
    }


def audit_scc_and_potential():
    # Minimum private migrations gave the first two arrows.  The cost-two
    # reset above supplies the return arrow, so tail rank is recurrent.
    states = ("T45", "T35", "T0")
    edges = (("T45", "T35"), ("T35", "T0"), ("T0", "T45"))
    reachable = {state: {state} for state in states}
    changed = True
    while changed:
        changed = False
        for source, target in edges:
            new = reachable[target] - reachable[source]
            if new:
                reachable[source].update(new)
                changed = True
    require(all(reachable[state] == set(states) for state in states),
            ("coarse tail SCC changed", reachable))
    return {
        "private_tail_well_founded": False,
        "coarse_scc": list(states),
        "cycle": "q45 -> q35 -> inherited-only -> q45",
        "all_cost_ge_3_paths_reset": True,
        "scope_boundary": "independent one-path additions; simultaneous unions not classified",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "census", "resets", "cycle", "potential"),
        default="all",
    )
    args = parser.parse_args()

    census = resets = cycle = potential = None
    if args.mode in ("all", "census"):
        census = audit_cost_census()
    if args.mode in ("all", "resets"):
        resets = audit_all_higher_cost_resets()
    if args.mode in ("all", "cycle"):
        cycle = audit_smallest_reset_cycle()
    if args.mode in ("all", "potential"):
        potential = audit_scc_and_potential()

    report = {
        "mode": args.mode,
        "terminal_rows": ["R3=101200:00", "R5=111112:01"],
        "cost_ge_2_paths": 206,
        "tail_reset_paths": 204,
        "non_reset_paths": 2,
        "all_cost_ge_3_paths_reset": True,
        "smallest_reset_cycle": cycle,
        "potential": potential,
        "scope": "all independent cost>=2 DQ/PS paths over R3 and R5",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 pure-21 private-tail higher-cost reset gate: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
