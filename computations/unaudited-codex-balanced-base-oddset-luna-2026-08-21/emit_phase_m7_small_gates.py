#!/usr/bin/env python3
"""Emit tiny exact-Q(omega) torus gates for the bounded m=7 support targets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_phase_m7_support_coefficients.json"


def polynomial(terms, variables):
    pieces = []
    for term in terms:
        coefficient = term["coefficient"].replace("*", "")
        monomial = "*".join(variables[name] for name in term["monomial"]) or "1"
        pieces.append(f"({coefficient})*{monomial}")
    return "+".join(pieces) or "0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--manifest", type=Path,
                        default=HERE / "manifest_phase_m7_small_gates.json")
    parser.add_argument("--prefix", default="gate_phase_m7")
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    manifest = {}
    for label, branch in data["branches"].items():
        systems = branch["coefficient_systems"]
        if not systems:
            continue
        manifest[label] = []
        for orbit, system in enumerate(systems):
            variable_names = system["variables"]
            variables = {name: f"x{index + 1}" for index, name in enumerate(variable_names)}
            ring_variables = list(variables.values()) + ["s", "z"]
            equations = [polynomial(row["terms"], variables)
                         for row in system["equations"]]
            product = "*".join(variables.values())
            pure7 = polynomial(system["pure7"], variables)
            ideal_generators = equations + [f"s*{product}-1", f"z*({pure7})-1"]
            lines = [
                f"ring r=(0,w),({','.join(ring_variables)}),dp;",
                "minpoly=w2+w+1;",
                f"ideal I={','.join(ideal_generators)};",
                "option(redSB);",
                "ideal G=std(I);",
                'print("SENTINEL_BEGIN");',
                "size(G);",
                "vdim(G);",
                "reduce(1,G);",
                'print("SENTINEL_END");',
                "quit;",
            ]
            path = HERE / f"{args.prefix}_{label}_orbit{orbit:02d}.sing"
            path.write_text("\n".join(lines) + "\n")
            manifest[label].append({
                "orbit": orbit,
                "path": path.name,
                "variables": len(variable_names),
                "mixed_equations": len(equations),
                "localizers": 2,
            })
    args.manifest.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
