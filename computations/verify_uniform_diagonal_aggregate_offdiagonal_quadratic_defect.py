#!/usr/bin/env python3
"""Compute the bilinear 01/10 defect of the diagonal aggregate source lift.

The frozen 34-row multipliers have identically zero first derivative in each
ordered 01/10 coordinate.  This checker takes the mixed second derivative
for every pair of disjoint physical edges (180 decorated pairs) and reduces
it modulo the original 71-row diagonal source ideal.  It never constructs a
ring containing the off-diagonal coordinates.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = (
    "computations/verify_n8_lemma_e_unary_top_diagonal_aggregate_identity.py"
)
FIRST_PATH = (
    "computations/verify_uniform_diagonal_aggregate_"
    "offdiagonal_first_correction.py"
)
PINS = {
    BASE_PATH:
        "d805a2d78ddf83239b2edca0598b8a88f90517296b375613030eb24defb1b2c2",
    "notes/n8-lemma-e-unary-top-diagonal-aggregate-identity.md":
        "d959fd085e6585d46000ace7a173d898e0a5f0306f03f2f476ad1890a0e24aa0",
    FIRST_PATH:
        "3a13e198cfee69e741def7b44879e95ed4c24fabb9cf4b998e752b9419865b11",
    "notes/uniform-diagonal-aggregate-offdiagonal-first-correction.md":
        "7ea1984547d6ab1e02678dceadb472775209094ad4d8ebf30b2b5a159b3df0ca",
}
EXPECTED_LEDGER_SHA256 = (
    "7611969cf0768b162f5182f2ebd2ab701a285baa4daa725992aba4c761c4d694"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        if expected != "TO_BE_FILLED":
            require(actual == expected,
                    f"pinned dependency changed: {relative}: {actual}")


def load(path, name):
    spec = spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def row_data(base, label):
    kind, *parts = label.split(":")
    if kind == "top":
        return base.SITES, tuple(map(int, parts[0]))
    holes = tuple(map(int, parts[0]))
    vertices = tuple(site for site in base.SITES if site not in holes)
    return vertices, tuple(map(int, parts[1]))


def second_derivative(base, label, first, second):
    edge1, colours1 = first
    edge2, colours2 = second
    if set(edge1) & set(edge2):
        return "0"
    vertices, word = row_data(base, label)
    position = {site: index for index, site in enumerate(vertices)}
    if not set(edge1 + edge2) <= set(vertices):
        return "0"
    if tuple(word[position[site]] for site in edge1) != colours1:
        return "0"
    if tuple(word[position[site]] for site in edge2) != colours2:
        return "0"
    deleted = set(edge1 + edge2)
    remainder = tuple(site for site in vertices if site not in deleted)
    if not remainder:
        return "1"
    remainder_word = tuple(word[position[site]] for site in remainder)
    return base.diagonal_coefficient(remainder, remainder_word)


def probe_name(probe):
    edge, colours = probe
    return "".join(map(str, edge)) + ":" + "".join(map(str, colours))


def singular_program(base, labels, generators, target, pairs):
    names = ",".join(
        base.VARIABLE_NAME[variable] for variable in base.VARIABLES
    )
    code = f"ring r=0,({names}),dp;\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += f"poly T={target}; option(redSB); ideal G=std(I);\n"
    code += "matrix L=lift(I,ideal(T));\n"
    for index, (first, second) in enumerate(pairs):
        derivatives = [
            second_derivative(base, label, first, second)
            for label in labels
        ]
        terms = [
            f"L[{row + 1},1]*({derivative})"
            for row, derivative in enumerate(derivatives)
            if derivative != "0"
        ]
        expression = "+".join(terms) if terms else "0"
        code += f"poly A{index}={expression};\n"
        code += f"poly D{index}=reduce(A{index},G);\n"
        code += f'print("RAW_{index}"); print(A{index});\n'
        code += f'print("REM_{index}"); print(D{index});\n'
    return code


def exact_two_cell_program(
        base, first_module, labels, generators, target, first, second):
    names = ",".join(
        base.VARIABLE_NAME[variable] for variable in base.VARIABLES
    ) + ",x,y"
    full_generators = []
    for label, generator in zip(labels, generators):
        vertices, word = row_data(base, label)
        dx = first_module.first_derivative(
            base, vertices, word, first[0], first[1]
        )
        dy = first_module.first_derivative(
            base, vertices, word, second[0], second[1]
        )
        dxy = second_derivative(base, label, first, second)
        terms = [f"({generator})"]
        if dx != "0":
            terms.append(f"x*({dx})")
        if dy != "0":
            terms.append(f"y*({dy})")
        if dxy != "0":
            terms.append(f"x*y*({dxy})")
        full_generators.append("+".join(terms))
    code = f"ring r=0,({names}),dp;\n"
    code += "ideal I=" + ",".join(full_generators) + ";\n"
    code += f"poly T={target}; option(redSB); ideal G=std(I);\n"
    code += "matrix L=lift(I,ideal(T)); poly C=0; int i; int nz=0;\n"
    code += (
        "for(i=1;i<=size(I);i++){ C=C+I[i]*L[i,1]; "
        "if(L[i,1]!=0){nz=nz+1;} }\n"
    )
    code += 'if(C-T!=0){print("SOURCE_LIFT_FAILED");exit(1);}\n'
    code += 'print("BASIS_SIZE"); print(size(G));\n'
    code += 'print("REMAINDER"); print(reduce(T,G));\n'
    code += 'print("NONZERO_MULTIPLIERS"); print(nz);\n'
    code += 'print("BEGIN_LIFT"); L; print("END_LIFT");\n'
    return code


STABILIZER = (
    (0, 1, 2, 3, 4, 5),
    (1, 0, 3, 2, 4, 5),
    (0, 1, 2, 3, 5, 4),
    (1, 0, 3, 2, 5, 4),
)


def act_probe(probe, permutation):
    edge, colours = probe
    decorated = (
        (permutation[edge[0]], colours[0]),
        (permutation[edge[1]], colours[1]),
    )
    decorated = tuple(sorted(decorated))
    return ((decorated[0][0], decorated[1][0]),
            (decorated[0][1], decorated[1][1]))


def canonical_pair(pair):
    return min(
        tuple(sorted((act_probe(pair[0], permutation),
                      act_probe(pair[1], permutation))))
        for permutation in STABILIZER
    )


def main():
    pin_dependencies()
    base = load(BASE_PATH, "diagonal_aggregate")
    first_module = load(FIRST_PATH, "first_correction")
    _, labels, generators = base.build_generators()
    first = base.diagonal_coefficient((2, 3, 4, 5), (1,) * 4)
    second = base.diagonal_coefficient((0, 1, 4, 5), (2,) * 4)
    top = base.diagonal_coefficient(base.SITES, (0,) * 6)
    target = f"{first}*{second}*{top}"
    probes = tuple(
        (edge, colours) for edge in base.EDGES
        for colours in ((0, 1), (1, 0))
    )
    # Intersecting physical edges cannot coexist in a perfect matching and
    # have identically zero bilinear source coefficient.
    pairs = tuple(
        (probes[left], probes[right])
        for left in range(len(probes))
        for right in range(left + 1, len(probes))
        if not (set(probes[left][0]) & set(probes[right][0]))
    )
    require(len(pairs) == 180, f"decorated pair count changed: {len(pairs)}")
    code = singular_program(base, labels, generators, target, pairs)
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"), input=code, text=True,
        capture_output=True, check=False, timeout=60,
    )
    require(result.returncode == 0,
            f"Singular failed: {result.stderr or result.stdout}")
    lines = result.stdout.splitlines()
    records = []
    for index, pair in enumerate(pairs):
        raw = lines[lines.index(f"RAW_{index}") + 1]
        remainder = lines[lines.index(f"REM_{index}") + 1]
        records.append({
            "pair": [probe_name(pair[0]), probe_name(pair[1])],
            "raw": raw,
            "remainder": remainder,
        })
    nontrivial_pairs = [
        pairs[index] for index, record in enumerate(records)
        if record["raw"] != "0"
    ]
    exact_nontrivial = []
    for pair in nontrivial_pairs:
        result = subprocess.run(
            ("/usr/local/bin/Singular", "-q"),
            input=exact_two_cell_program(
                base, first_module, labels, generators, target,
                pair[0], pair[1]
            ),
            text=True, capture_output=True, check=False, timeout=60,
        )
        require(result.returncode == 0,
                f"two-cell Singular failed: {result.stderr or result.stdout}")
        require("SOURCE_LIFT_FAILED" not in result.stdout,
                "an exact two-cell source lift failed")
        lines = result.stdout.splitlines()
        lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split(
            "\nEND_LIFT", 1
        )[0]
        exact_nontrivial.append({
            "pair": [probe_name(pair[0]), probe_name(pair[1])],
            "basis_size": int(lines[lines.index("BASIS_SIZE") + 1]),
            "remainder": lines[lines.index("REMAINDER") + 1],
            "nonzero_multipliers": int(
                lines[lines.index("NONZERO_MULTIPLIERS") + 1]
            ),
            "lift_sha256": sha256(lift.encode()).hexdigest(),
        })
    orbit_members = {}
    for pair in pairs:
        canonical = canonical_pair(pair)
        orbit_members.setdefault(canonical, []).append(pair)
    survivor_orbits = {}
    for index, record in enumerate(records):
        if record["remainder"] == "0":
            continue
        canonical = canonical_pair(pairs[index])
        survivor_orbits.setdefault(canonical, []).append(record)
    ledger = {
        "decorated_disjoint_pairs": len(pairs),
        "raw_zero": sum(record["raw"] == "0" for record in records),
        "quotient_zero": sum(record["remainder"] == "0"
                             for record in records),
        "nonzero_records": [record for record in records
                            if record["remainder"] != "0"],
        "exact_nontrivial_charts": exact_nontrivial,
        "exact_two_cell_units": (
            180 - len(nontrivial_pairs)
            + sum(record["remainder"] == "0"
                  for record in exact_nontrivial)
        ),
        "stabilizer_order": len(STABILIZER),
        "pair_orbits": len(orbit_members),
        "pair_orbit_size_histogram": {
            str(size): sum(len(members) == size
                           for members in orbit_members.values())
            for size in sorted(set(map(len, orbit_members.values())))
        },
        "nonzero_quotient_orbits": [
            {
                "representative": [probe_name(canonical[0]),
                                   probe_name(canonical[1])],
                "members": len(members),
            }
            for canonical, members in sorted(survivor_orbits.items())
        ],
        "first_order_input": (
            "the pinned first-correction checker proves all 30 ordered "
            "linear defects vanish identically"
        ),
        "verdict": (
            "the degree-two symbol has eight monomial quotient classes in "
            "two stabilizer orbits, but every one of the 180 decorated "
            "two-cell charts has an exact ordinary source-row unit"
        ),
        "scope": (
            "ordered 01/10 cells and concentrated spokes in the pinned "
            "71-row fine-degree module; no three-cell correction, other "
            "off-diagonal colour types, or multisite-star conclusion"
        ),
    }
    require(len(nontrivial_pairs) == 40,
            f"raw nontrivial pair count changed: {len(nontrivial_pairs)}")
    require(ledger["quotient_zero"] == 172,
            "quadratic quotient-zero count changed")
    require(len(survivor_orbits) == 2,
            "quadratic survivor orbit count changed")
    require(ledger["exact_two_cell_units"] == len(pairs),
            "an exact decorated two-cell unit failed")
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(payload)
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
