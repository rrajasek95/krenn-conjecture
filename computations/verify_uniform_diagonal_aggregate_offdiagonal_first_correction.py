#!/usr/bin/env python3
"""Exact first off-diagonal correction to the 34-row diagonal aggregate lift.

The pinned diagonal identity is lifted through one ordered 01/10 internal
cell.  Singular computes the literal source lift and reduces each first
correction modulo the original 71 diagonal source rows.  No off-diagonal
support layer or full 135-variable standard basis is constructed.
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
PINS = {
    BASE_PATH:
        "d805a2d78ddf83239b2edca0598b8a88f90517296b375613030eb24defb1b2c2",
    "notes/n8-lemma-e-unary-top-diagonal-aggregate-identity.md":
        "d959fd085e6585d46000ace7a173d898e0a5f0306f03f2f476ad1890a0e24aa0",
    "computations/verify_uniform_crossed_lock_common_provenance_boundary.py":
        "862a615b9da32743964380917f178774c6725dd6390cec9ce259f021d58f3033",
    "notes/uniform-crossed-lock-common-provenance-boundary.md":
        "d7b7b6befea91d15c672fe928162aa4c54988b40a83ab2ad32f2dfdd217f5dd7",
}
EXPECTED_LEDGER_SHA256 = (
    "ae8e1687db2e12237528a64e8c92c74e5f3b4b1b6528e387725448f4edfc1bcc"
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


def load_base():
    path = ROOT / BASE_PATH
    spec = spec_from_file_location("diagonal_aggregate", path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {BASE_PATH}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def first_derivative(base, vertices, word, edge, colours):
    """Coefficient of one off-diagonal cell in a matching fibre."""
    left, right = edge
    if left not in vertices or right not in vertices:
        return "0"
    position = {site: index for index, site in enumerate(vertices)}
    if (word[position[left]], word[position[right]]) != colours:
        return "0"
    remainder = tuple(site for site in vertices if site not in edge)
    remainder_word = tuple(word[position[site]] for site in remainder)
    return base.diagonal_coefficient(remainder, remainder_word)


def generator_derivative(base, label, edge, colours):
    kind, *parts = label.split(":")
    if kind == "top":
        vertices = base.SITES
        word = tuple(map(int, parts[0]))
    else:
        holes = tuple(map(int, parts[0]))
        vertices = tuple(site for site in base.SITES if site not in holes)
        word = tuple(map(int, parts[1]))
    return first_derivative(base, vertices, word, edge, colours)


def singular_program(base, labels, generators, target, probes):
    names = ",".join(
        base.VARIABLE_NAME[variable] for variable in base.VARIABLES
    )
    code = f"ring r=0,({names}),dp;\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += f"poly T={target}; option(redSB); ideal G=std(I);\n"
    code += "matrix L=lift(I,ideal(T));\n"
    for probe_index, (edge, colours) in enumerate(probes):
        derivatives = [
            generator_derivative(base, label, edge, colours)
            for label in labels
        ]
        terms = [
            f"L[{index + 1},1]*({derivative})"
            for index, derivative in enumerate(derivatives)
            if derivative != "0"
        ]
        expression = "+".join(terms) if terms else "0"
        code += f"poly A{probe_index}={expression};\n"
        code += f"poly D{probe_index}=reduce(A{probe_index},G);\n"
        code += f'print("RAW_{probe_index}"); print(A{probe_index});\n'
        code += f'print("PROBE_{probe_index}"); print(D{probe_index});\n'
    return code


def exact_one_cell_program(base, labels, generators, target, edge, colours):
    names = ",".join(
        base.VARIABLE_NAME[variable] for variable in base.VARIABLES
    ) + ",x"
    full_generators = []
    for label, generator in zip(labels, generators):
        derivative = generator_derivative(base, label, edge, colours)
        if derivative == "0":
            full_generators.append(generator)
        else:
            full_generators.append(f"({generator})+x*({derivative})")
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


def main():
    pin_dependencies()
    base = load_base()
    _, labels, generators = base.build_generators()
    first = base.diagonal_coefficient((2, 3, 4, 5), (1, 1, 1, 1))
    second = base.diagonal_coefficient((0, 1, 4, 5), (2, 2, 2, 2))
    top = base.diagonal_coefficient(base.SITES, (0,) * 6)
    target = f"{first}*{second}*{top}"
    probes = tuple(
        (edge, colours)
        for edge in base.EDGES
        for colours in ((0, 1), (1, 0))
    )
    code = singular_program(base, labels, generators, target, probes)
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"), input=code, text=True,
        capture_output=True, check=False, timeout=60,
    )
    require(result.returncode == 0,
            f"Singular failed: {result.stderr or result.stdout}")
    lines = result.stdout.splitlines()
    remainders = []
    for index, (edge, colours) in enumerate(probes):
        raw_marker = f"RAW_{index}"
        marker = f"PROBE_{index}"
        raw_offset = lines.index(raw_marker)
        offset = lines.index(marker)
        raw = lines[raw_offset + 1]
        remainder = lines[offset + 1]
        remainders.append({
            "edge": "".join(map(str, edge)),
            "colours": "".join(map(str, colours)),
            "raw_correction": raw,
            "remainder": remainder,
        })

    exact_one_cell = []
    for edge, colours in probes:
        result = subprocess.run(
            ("/usr/local/bin/Singular", "-q"),
            input=exact_one_cell_program(
                base, labels, generators, target, edge, colours
            ),
            text=True, capture_output=True, check=False, timeout=60,
        )
        require(result.returncode == 0,
                f"one-cell Singular failed: {result.stderr or result.stdout}")
        require("SOURCE_LIFT_FAILED" not in result.stdout,
                "an exact one-cell source lift failed")
        lines = result.stdout.splitlines()
        basis_size = int(lines[lines.index("BASIS_SIZE") + 1])
        remainder = lines[lines.index("REMAINDER") + 1]
        multipliers = int(lines[lines.index("NONZERO_MULTIPLIERS") + 1])
        lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split(
            "\nEND_LIFT", 1
        )[0]
        exact_one_cell.append({
            "edge": "".join(map(str, edge)),
            "colours": "".join(map(str, colours)),
            "basis_size": basis_size,
            "remainder": remainder,
            "nonzero_multipliers": multipliers,
            "lift_sha256": sha256(lift.encode()).hexdigest(),
        })
    ledger = {
        "probes": len(probes),
        "remainders": remainders,
        "zero_remainders": sum(item["remainder"] == "0"
                               for item in remainders),
        "identically_zero_raw_corrections": sum(
            item["raw_correction"] == "0" for item in remainders
        ),
        "exact_one_cell": exact_one_cell,
        "exact_one_cell_units": sum(item["remainder"] == "0"
                                    for item in exact_one_cell),
        "verdict": (
            "all 30 ordered 01/10 one-cell lifts have zero first correction "
            "class and an exact source-row unit; any surviving decorated "
            "anchor-edge escape starts at off-diagonal filtration degree 2"
        ),
        "scope": (
            "concentrated spokes and the pinned 71-row fine-degree module; "
            "one arbitrary 01/10 internal coordinate at a time, not two "
            "simultaneous off-diagonal coordinates or multisite stars"
        ),
    }
    require(ledger["zero_remainders"] == len(probes),
            "a first correction class survived")
    require(ledger["identically_zero_raw_corrections"] == len(probes),
            "a raw first correction survived")
    require(ledger["exact_one_cell_units"] == len(probes),
            "an exact one-cell ordinary unit failed")
    require(all(item["basis_size"] == 251 for item in exact_one_cell),
            "an exact one-cell basis size changed")
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(payload)
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
