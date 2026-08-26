#!/usr/bin/env python3
"""Export an exact normalized full-fibre system for one of the 31 charts.

For a chart representative, its twelve selected pure-matching cells are
units.  In each colour the target-preserving port torus can set three of the
four selected cells to one.  The fourth is the invariant product of that
matching and is retained as a nonzero anchor.  Thus nine source variables
are removed, the literal numerical target H_c=1 is preserved, and three
quadratic Rabinowitsch equations enforce the chart.  Emptiness of all 31
exported systems is therefore equivalent to the unrestricted N=8 claim.

This exporter performs no algebraic inference.  A modular solver result is
only a screen until it is lifted/replayed in characteristic zero.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORBIT_CHECKER = ROOT / "computations" / "verify_n8_target_triple_localization_orbits.py"
SPEC = importlib.util.spec_from_file_location("chart_orbits", ORBIT_CHECKER)
CHARTS = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHARTS)

SITES = tuple(range(8))
COLOURS = tuple(range(3))


def matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            yield ((first, second),) + tail


PM8 = tuple(matchings(SITES))
assert len(PM8) == 105


def xvar(u: int, v: int, cu: int, cv: int) -> str:
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return f"x{u}{v}_{cu}{cv}"


def chart_support(chart_index: int) -> tuple[tuple[str, ...], ...]:
    rows = tuple(sorted(CHARTS.SOURCE.target_orbit_rows()))
    if not 1 <= chart_index <= len(rows):
        raise ValueError(f"chart index must lie in 1..{len(rows)}")
    mate = CHARTS.SOURCE.decode_key(rows[chart_index - 1])
    support = [set() for _colour in COLOURS]
    for first, second in CHARTS.SOURCE.mate_edges(mate):
        u, cu = divmod(first, 3)
        v, cv = divmod(second, 3)
        if cu != cv:
            raise RuntimeError("pure chart support contains a mixed-colour cell")
        support[cu].add(xvar(u, v, cu, cv))
    if tuple(map(len, support)) != (4, 4, 4):
        raise RuntimeError("chart support does not contain twelve cells")
    return tuple(tuple(sorted(part)) for part in support)


def normalized_monomial(word, matching, support: frozenset[str]) -> str:
    factors = [
        variable
        for u, v in matching
        if (variable := xvar(u, v, word[u], word[v])) not in support
    ]
    return "*".join(factors) or "1"


def fibre_rows(normalized: frozenset[str]) -> list[str]:
    rows = []
    for word in itertools.product(COLOURS, repeat=8):
        terms = [normalized_monomial(word, matching, normalized) for matching in PM8]
        if len(set(word)) == 1:
            terms.append("-1")
        rows.append("+".join(terms).replace("+-", "-"))
    if len(rows) != 3**8:
        raise RuntimeError("full fibre row count changed")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chart", type=int)
    parser.add_argument("--characteristic", type=int, default=32003)
    parser.add_argument(
        "--f4sat",
        action="store_true",
        help="append the anchor product for msolve -S instead of inverses",
    )
    parser.add_argument(
        "--order",
        choices=("natural", "carrier-first", "carrier-last"),
        default="natural",
        help="chart-25 variable order induced by its frozen 36-cell carrier",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    support_by_colour = chart_support(args.chart)
    normalized = frozenset(
        variable
        for colour_support in support_by_colour
        for variable in colour_support[:3]
    )
    anchors = tuple(colour_support[3] for colour_support in support_by_colour)
    variables = [
        xvar(u, v, cu, cv)
        for u, v in itertools.combinations(SITES, 2)
        for cu in COLOURS
        for cv in COLOURS
        if xvar(u, v, cu, cv) not in normalized
    ]
    if len(variables) != 243:
        raise RuntimeError("target-preserving chart does not have 243 source variables")
    if args.order != "natural":
        if args.chart != 25:
            raise ValueError("the frozen carrier order is currently chart-25 only")
        carrier_path = ROOT / "computations" / "verify_n8_chart25_pure_product_membership.py"
        carrier_spec = importlib.util.spec_from_file_location("chart25_carrier", carrier_path)
        carrier_module = importlib.util.module_from_spec(carrier_spec)
        assert carrier_spec.loader is not None
        carrier_spec.loader.exec_module(carrier_module)
        carrier_module.DUAL.configure_chart25()
        functional = carrier_module.expanded_dual()
        carrier = {
            xvar(*coordinate)
            for row in functional
            for coordinate in row
        }
        if len(carrier) != 36:
            raise RuntimeError("frozen chart-25 carrier changed")
        inside = [variable for variable in variables if variable in carrier]
        outside = [variable for variable in variables if variable not in carrier]
        variables = (
            inside + outside if args.order == "carrier-first" else outside + inside
        )
    rows = fibre_rows(normalized)
    if args.f4sat:
        rows.append("*".join(anchors))
    else:
        variables.extend(("sy0", "sy1", "sy2"))
        rows.extend(f"sy{colour}*{anchors[colour]}-1" for colour in COLOURS)
    output = args.output or Path(__file__).with_name(
        f"target_chart{args.chart:02d}_full_{'sat_' if args.f4sat else ''}"
        f"{args.order.replace('-', '_')}_p{args.characteristic}.ms"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w") as handle:
        handle.write(",".join(variables) + "\n")
        handle.write(str(args.characteristic) + "\n")
        for index, row in enumerate(rows):
            handle.write(row)
            handle.write(",\n" if index + 1 < len(rows) else "\n")

    print(output)
    print("chart=", args.chart)
    print("normalized=", ",".join(sorted(normalized)))
    print("anchors=", ",".join(anchors))
    print("variables=", len(variables), "equations=", len(rows))
    print("bytes=", output.stat().st_size)


if __name__ == "__main__":
    main()
