#!/usr/bin/env python3
"""Classify the terminal ordered 01/10 cubic aggregate defect.

Three disjoint off-diagonal coordinates on six residual sites form a
physical perfect matching.  This checker evaluates the mixed third
derivative of the frozen 34-row source lift on all 15*2^3=120 decorated
matchings and reduces it modulo the original 71 diagonal source rows.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
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
QUADRATIC_PATH = (
    "computations/verify_uniform_diagonal_aggregate_"
    "offdiagonal_quadratic_defect.py"
)
PINS = {
    BASE_PATH:
        "d805a2d78ddf83239b2edca0598b8a88f90517296b375613030eb24defb1b2c2",
    FIRST_PATH:
        "3a13e198cfee69e741def7b44879e95ed4c24fabb9cf4b998e752b9419865b11",
    QUADRATIC_PATH:
        "cdf5a71f6f5dcef524c22c9790f0a29bf902ddf8e58bccb7b5233655f0359f07",
    "notes/uniform-diagonal-aggregate-offdiagonal-quadratic-defect.md":
        "9aa57c618f3ae8bca6b335fb050c881039e70449f6798240a50ba28429e667fb",
    "computations/verify_uniform_anchor_edge_offdiagonal_alternating_exit_dichotomy.py":
        "2de838ff96118a7c54df23c8df02202090a52a3b0ca83f62c400a7a8241f37b8",
    "notes/uniform-anchor-edge-offdiagonal-alternating-exit-dichotomy.md":
        "9b4d2dabf493845de4570008835d544cdb0a9591c5272758e5390f19e70bdc02",
}
EXPECTED_LEDGER_SHA256 = (
    "37353079ba50ba9706c52c6d0695e61a94b708c6cd086ed1ff10160f3455c1c5"
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


def triple_derivative(base, quadratic, label, triple):
    vertices, word = quadratic.row_data(base, label)
    sites = set()
    position = {site: index for index, site in enumerate(vertices)}
    for edge, colours in triple:
        if set(edge) & sites or not set(edge) <= set(vertices):
            return "0"
        if tuple(word[position[site]] for site in edge) != colours:
            return "0"
        sites.update(edge)
    remainder = tuple(site for site in vertices if site not in sites)
    if not remainder:
        return "1"
    remainder_word = tuple(word[position[site]] for site in remainder)
    return base.diagonal_coefficient(remainder, remainder_word)


def triple_name(triple):
    return tuple(
        "".join(map(str, edge)) + ":" + "".join(map(str, colours))
        for edge, colours in triple
    )


def singular_symbol_program(base, quadratic, labels, generators,
                            target, triples):
    names = ",".join(
        base.VARIABLE_NAME[variable] for variable in base.VARIABLES
    )
    code = f"ring r=0,({names}),dp;\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += f"poly T={target}; option(redSB); ideal G=std(I);\n"
    code += "matrix L=lift(I,ideal(T));\n"
    for index, triple in enumerate(triples):
        derivatives = [
            triple_derivative(base, quadratic, label, triple)
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


def exact_three_cell_program(base, first_module, quadratic, labels,
                             generators, target, triple):
    names = ",".join(
        base.VARIABLE_NAME[variable] for variable in base.VARIABLES
    ) + ",x,y,z"
    variables = ("x", "y", "z")
    full_generators = []
    for label, generator in zip(labels, generators):
        vertices, word = quadratic.row_data(base, label)
        terms = [f"({generator})"]
        for variable, probe in zip(variables, triple):
            derivative = first_module.first_derivative(
                base, vertices, word, probe[0], probe[1]
            )
            if derivative != "0":
                terms.append(f"{variable}*({derivative})")
        for left, right in itertools.combinations(range(3), 2):
            derivative = quadratic.second_derivative(
                base, label, triple[left], triple[right]
            )
            if derivative != "0":
                terms.append(
                    f"{variables[left]}*{variables[right]}*({derivative})"
                )
        derivative = triple_derivative(base, quadratic, label, triple)
        if derivative != "0":
            terms.append(f"x*y*z*({derivative})")
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


def canonical_triple(quadratic, triple):
    return min(
        tuple(sorted(quadratic.act_probe(probe, permutation)
                     for probe in triple))
        for permutation in quadratic.STABILIZER
    )


def anchor_incidence_census(base):
    unary = base.perfect_matchings(base.SITES)
    response1 = base.perfect_matchings((2, 3, 4, 5))
    response2 = base.perfect_matchings((0, 1, 4, 5))
    signatures = {}
    contained = 0
    total = 0
    for q0 in unary:
        for q1 in response1:
            for q2 in response2:
                selected = tuple(map(set, (q0, q1, q2)))
                union = set().union(*selected)
                for matching in unary:
                    total += 1
                    if not set(matching) <= union:
                        continue
                    contained += 1
                    signature = tuple(sorted(
                        sum(edge in chosen for chosen in selected)
                        for edge in matching
                    ))
                    signatures[signature] = signatures.get(signature, 0) + 1
    require(total == 2025 and contained == 245,
            f"anchor-incidence census changed: {total}, {contained}")
    return {
        "physical_configurations": total,
        "all_three_edges_in_anchor_union": contained,
        "with_nonanchor_edge": total - contained,
        "edge_use_multiplicity_signatures": {
            "".join(map(str, signature)): count
            for signature, count in sorted(signatures.items())
        },
        "all_edges_uniquely_used": signatures[(1, 1, 1)],
        "some_edge_multiply_used": (
            contained - signatures[(1, 1, 1)]
        ),
        "decorated_all_anchor_configurations": 8 * contained,
    }


def main():
    pin_dependencies()
    base = load(BASE_PATH, "diagonal_aggregate")
    first_module = load(FIRST_PATH, "first_correction")
    quadratic = load(QUADRATIC_PATH, "quadratic_defect")
    _, labels, generators = base.build_generators()
    first = base.diagonal_coefficient((2, 3, 4, 5), (1,) * 4)
    second = base.diagonal_coefficient((0, 1, 4, 5), (2,) * 4)
    top = base.diagonal_coefficient(base.SITES, (0,) * 6)
    target = f"{first}*{second}*{top}"
    triples = tuple(
        tuple((edge, colours) for edge, colours in zip(matching, choices))
        for matching in base.perfect_matchings(base.SITES)
        for choices in itertools.product(((0, 1), (1, 0)), repeat=3)
    )
    require(len(triples) == 120,
            f"decorated perfect-matching count changed: {len(triples)}")
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=singular_symbol_program(
            base, quadratic, labels, generators, target, triples
        ),
        text=True, capture_output=True, check=False, timeout=60,
    )
    require(result.returncode == 0,
            f"Singular failed: {result.stderr or result.stdout}")
    lines = result.stdout.splitlines()
    records = []
    for index, triple in enumerate(triples):
        raw = lines[lines.index(f"RAW_{index}") + 1]
        remainder = lines[lines.index(f"REM_{index}") + 1]
        records.append({
            "triple": triple_name(triple),
            "raw": raw,
            "remainder": remainder,
        })
    orbits = {}
    for triple in triples:
        orbits.setdefault(canonical_triple(quadratic, triple), []).append(triple)
    require(len(orbits) == 32,
            f"decorated matching orbit count changed: {len(orbits)}")
    exact_orbits = []
    for representative, members in sorted(orbits.items()):
        result = subprocess.run(
            ("/usr/local/bin/Singular", "-q"),
            input=exact_three_cell_program(
                base, first_module, quadratic, labels, generators,
                target, representative
            ),
            text=True, capture_output=True, check=False, timeout=60,
        )
        require(result.returncode == 0,
                f"three-cell Singular failed: {result.stderr or result.stdout}")
        require("SOURCE_LIFT_FAILED" not in result.stdout,
                "an exact three-cell source lift failed")
        lines = result.stdout.splitlines()
        lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split(
            "\nEND_LIFT", 1
        )[0]
        exact_orbits.append({
            "representative": triple_name(representative),
            "orbit_size": len(members),
            "basis_size": int(lines[lines.index("BASIS_SIZE") + 1]),
            "remainder": lines[lines.index("REMAINDER") + 1],
            "nonzero_multipliers": int(
                lines[lines.index("NONZERO_MULTIPLIERS") + 1]
            ),
            "lift_sha256": sha256(lift.encode()).hexdigest(),
            "lift_parameters": "".join(
                variable for variable in "xyz" if variable in lift
            ),
        })
    ledger = {
        "decorated_perfect_matchings": len(triples),
        "raw_zero": sum(record["raw"] == "0" for record in records),
        "quotient_zero": sum(record["remainder"] == "0"
                             for record in records),
        "nonzero_records": [record for record in records
                            if record["remainder"] != "0"],
        "stabilizer_order": len(quadratic.STABILIZER),
        "decorated_matching_orbits": len(orbits),
        "orbit_size_histogram": {
            str(size): sum(len(members) == size for members in orbits.values())
            for size in sorted(set(map(len, orbits.values())))
        },
        "exact_orbit_lifts": exact_orbits,
        "exact_unit_orbits": sum(record["remainder"] == "0"
                                 for record in exact_orbits),
        "lift_parameter_histogram": {
            parameters: sum(record["lift_parameters"] == parameters
                            for record in exact_orbits)
            for parameters in sorted(set(
                record["lift_parameters"] for record in exact_orbits
            ))
        },
        "selected_anchor_incidence": anchor_incidence_census(base),
        "verdict": (
            "all 120 ordered 01/10 decorated perfect matchings lie in 32 "
            "source-unit orbits; the 245 all-anchor physical incidences, "
            "including both unique-use and multiply-used types, are empty"
        ),
        "scope": (
            "one decorated perfect matching (three simultaneous 01/10 "
            "coordinates) with concentrated spokes; this does not prove "
            "compatibility for support containing multiple decorated "
            "perfect matchings or other colour sectors"
        ),
    }
    require(ledger["raw_zero"] == len(triples),
            "a raw cubic symbol survived")
    require(ledger["exact_unit_orbits"] == len(orbits),
            "an exact cubic orbit failed to have a source unit")
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(payload)
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
