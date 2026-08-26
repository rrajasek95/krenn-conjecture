#!/usr/bin/env python3
"""Export one exact canonical triangle-blocker branch for msolve.

The equations are the literal normalized N=8,d=3 perfect-matching system,
the localization A_06[0,1] != 0, and one of the four row-span memberships
for the carrier (cap 67, residual triangle 012).  This is a producer only;
an msolve result still needs exact/source-level replay before certification.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path


SITES = tuple(range(8))
COLORS = tuple(range(3))
TRIANGLE = frozenset((0, 1, 2))
CAP = frozenset((6, 7))
BRANCHES = (
    "triangle_endpoint_colour",
    "cap_endpoint_colour",
    "third_colour",
    "direct",
)


def matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for pos in range(1, len(vertices)):
        b = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for tail in matchings(rest):
            yield ((a, b),) + tail


PM8 = tuple(matchings(SITES))


def xvar(u: int, v: int, cu: int, cv: int) -> str:
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return f"x{u}{v}_{cu}{cv}"


def lvar(a: int, b: int, ca: int, cb: int) -> str:
    assert a < b
    return f"l{a}{b}_{ca}{cb}"


def source_variables() -> list[str]:
    return [
        xvar(u, v, cu, cv)
        for u, v in itertools.combinations(SITES, 2)
        for cu in COLORS
        for cv in COLORS
    ]


def outside_edges() -> list[tuple[int, int]]:
    residual = tuple(range(6))
    return [
        (a, b)
        for a, b in itertools.combinations(residual, 2)
        if not ({a, b} <= TRIANGLE)
    ]


OUTSIDE = outside_edges()
assert len(OUTSIDE) == 12


def witness_variables() -> list[str]:
    return [
        lvar(a, b, ca, cb)
        for a, b in OUTSIDE
        for ca in COLORS
        for cb in COLORS
    ]


def matching_monomial(word: tuple[int, ...], matching) -> str:
    return "*".join(xvar(u, v, word[u], word[v]) for u, v in matching)


def fibre_rows(shell: str) -> list[str]:
    rows: list[str] = []
    for word in itertools.product(COLORS, repeat=8):
        counts = sorted((word.count(c) for c in COLORS), reverse=True)
        profile = "".join(str(x) for x in counts if x)
        off_count = 8 - counts[0]
        include = (
            shell == "full"
            or (shell == "x3" and off_count <= 3)
            or (shell == "x4" and off_count <= 4)
            or (shell == "332" and profile == "332")
        )
        if not include:
            continue
        terms = [matching_monomial(word, matching) for matching in PM8]
        if len(set(word)) == 1:
            terms.append("-1")
        rows.append("+".join(terms).replace("+-", "-"))
    return rows


def response_coefficient(
    a: int, b: int, ca: int, cb: int, i: int, j: int
) -> tuple[str, str]:
    # R_ab(ca,cb) = sum_ij K_ij(
    #   A_6a(i,ca) A_7b(j,cb) + A_6b(i,cb) A_7a(j,ca)).
    return (
        f"{xvar(6, a, i, ca)}*{xvar(7, b, j, cb)}",
        f"{xvar(6, b, i, cb)}*{xvar(7, a, j, ca)}",
    )


def blocker(branch: str, i: int, j: int) -> str | None:
    if branch == "triangle_endpoint_colour":
        return "1" if (i, j) == (0, 0) else None
    if branch == "cap_endpoint_colour":
        return "1" if (i, j) == (1, 1) else None
    if branch == "third_colour":
        return "1" if (i, j) == (2, 2) else None
    assert branch == "direct"
    return xvar(6, 7, i, j)


def membership_rows(branch: str) -> list[str]:
    rows: list[str] = []
    for i in COLORS:
        for j in COLORS:
            terms: list[str] = []
            rhs = blocker(branch, i, j)
            if rhs is not None:
                terms.append(rhs)
            for a, b in OUTSIDE:
                for ca in COLORS:
                    for cb in COLORS:
                        lam = lvar(a, b, ca, cb)
                        first, second = response_coefficient(a, b, ca, cb, i, j)
                        terms.extend((f"-{lam}*{first}", f"-{lam}*{second}"))
            rows.append("+".join(terms).replace("+-", "-") or "0")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("branch", choices=BRANCHES)
    parser.add_argument("--characteristic", type=int, default=32003)
    parser.add_argument("--shell", choices=("x3", "x4", "332", "full"), default="full")
    parser.add_argument(
        "--pair-offdiag-only",
        action="store_true",
        help=("export the equivalent full fibre on the gauge chart "
              "A_67[0,1]=1, without triangle-membership witnesses"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    tag = "pair_offdiag" if args.pair_offdiag_only else args.branch
    output = args.output or Path(__file__).with_name(
        f"canonical_triangle_{tag}_{args.shell}_p{args.characteristic}.ms"
    )
    if args.pair_offdiag_only:
        normalized = xvar(6, 7, 0, 1)
        variables = [var for var in source_variables() if var != normalized]
    else:
        normalized = None
        variables = source_variables() + witness_variables() + ["sy0"]
    rows = fibre_rows(args.shell)
    if args.pair_offdiag_only:
        # Variable names are delimiter-safe: x67_01 cannot occur as a proper
        # substring of another source variable.
        rows = [row.replace(normalized, "1") for row in rows]
        assert len(variables) == 251
    else:
        rows.extend(membership_rows(args.branch))
        rows.append(f"sy0*{xvar(0, 6, 0, 1)}-1")
        assert len(variables) == 361
    expected_fibre = {"x3": 1731, "x4": 4881, "332": 1680, "full": 6561}[args.shell]
    assert len(rows) == expected_fibre + (0 if args.pair_offdiag_only else 10)

    with output.open("w") as handle:
        handle.write(",".join(variables) + "\n")
        handle.write(str(args.characteristic) + "\n")
        for index, row in enumerate(rows):
            handle.write(row)
            handle.write(",\n" if index + 1 < len(rows) else "\n")
    print(output)
    print(f"variables={len(variables)} equations={len(rows)} bytes={output.stat().st_size}")


if __name__ == "__main__":
    main()
