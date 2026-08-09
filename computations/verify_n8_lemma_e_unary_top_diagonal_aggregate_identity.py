#!/usr/bin/env python3
"""Exact aggregate translated-fibre identity for the diagonal one-bad chart.

Fix the silent ordered holes (p1,s1)=(0,1), (p2,s2)=(2,3) and restrict the
internal quadratic Q to equal-colour cells.  In the fine multidegree of

    F_01(1111) * F_23(2222) * H(000000),

the complete compatible mixed-top and cofactor-zero equations generate this
product over Q.  Since the three factors equal one in the normalized packet,
the colour-diagonal silent chart is empty, with arbitrary support and complex
cancellation.

The script asks Singular for a characteristic-zero source lift and then
checks the lifted identity exactly.  It does not address off-diagonal cells.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess


SITES = tuple(range(6))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))

EXPECTED_LEDGER_DIGEST = "257e602cc2fc463f4e8598a1e164e428ec0e90f6d06309ad081ad60dc6494839"
EXPECTED_LIFT_DIGEST = "169acdcd3fb8194b43c066cd33207b841af2823cd6a0a40ede444c438d3b3ae6"
EXPECTED_STANDARD_BASIS_SIZE = 251


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for mate in vertices[1:]:
        remainder = tuple(
            vertex for vertex in vertices if vertex not in (first, mate)
        )
        for tail in perfect_matchings(remainder):
            answer.append((tuple(sorted((first, mate))),) + tail)
    return tuple(answer)


VARIABLES = tuple((edge, colour) for edge in EDGES for colour in COLORS)
VARIABLE_NAME = {
    variable: f"q{variable[0][0]}{variable[0][1]}{variable[1]}"
    for variable in VARIABLES
}


def diagonal_coefficient(vertices, word):
    """Coefficient polynomial after retaining only equal-colour Q cells."""
    vertices = tuple(vertices)
    position = {vertex: index for index, vertex in enumerate(vertices)}
    terms = []
    for matching in perfect_matchings(vertices):
        if not all(
            word[position[left]] == word[position[right]]
            for left, right in matching
        ):
            continue
        terms.append("*".join(
            VARIABLE_NAME[(edge, word[position[edge[0]]])]
            for edge in matching
        ))
    if not terms:
        return "0"
    return "(" + "+".join(terms) + ")"


def build_generators():
    # These are exactly the colour tokens in the product of the two pure
    # four-site cofactors and the pure-zero six-site hafnian.
    tokens = {
        0: (0, 2),
        1: (0, 2),
        2: (0, 1),
        3: (0, 1),
        4: (0, 1, 2),
        5: (0, 1, 2),
    }
    generators = []
    labels = []

    # Every compatible mixed six-site coefficient of Q^[3] is zero.
    for word in product(*(tokens[site] for site in SITES)):
        if len(set(word)) == 1:
            continue
        polynomial = diagonal_coefficient(SITES, word)
        if polynomial == "0":
            continue
        labels.append("top:" + "".join(map(str, word)))
        generators.append(polynomial)

    # The first two cofactors have one nonzero pure coefficient; all other
    # coefficients vanish.  The last two are the complete off-diagonal zero
    # rows.  Only fine-degree-compatible words can enter this membership.
    packets = (
        ((0, 1), (1, 1, 1, 1)),
        ((2, 3), (2, 2, 2, 2)),
        ((0, 3), None),
        ((1, 2), None),
    )
    for holes, target in packets:
        vertices = tuple(site for site in SITES if site not in holes)
        for word in product(*(tokens[site] for site in vertices)):
            if target is not None and word == target:
                continue
            polynomial = diagonal_coefficient(vertices, word)
            if polynomial == "0":
                continue
            labels.append(
                "cofactor:" + "".join(map(str, holes)) + ":"
                + "".join(map(str, word))
            )
            generators.append(polynomial)

    require(len(generators) == len(labels) == 71,
            "the diagonal aggregate generator count changed")
    return tokens, labels, generators


def singular_program(generators, target):
    names = ",".join(VARIABLE_NAME[variable] for variable in VARIABLES)
    code = f"ring r=0,({names}),dp;\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += f"poly T={target};\n"
    code += "option(redSB); ideal G=std(I);\n"
    code += "poly R=reduce(T,G);\n"
    code += "matrix L=lift(I,ideal(T));\n"
    code += "poly C=0; int i; int nz=0;\n"
    code += (
        "for(i=1;i<=size(I);i++){ C=C+I[i]*L[i,1]; "
        "if(L[i,1]!=0){nz=nz+1;} }\n"
    )
    code += "if(C-T!=0){ print(\"SOURCE_LIFT_FAILED\"); exit(1); }\n"
    code += "print(\"BASIS_SIZE\"); print(size(G));\n"
    code += "print(\"REMAINDER\"); print(R);\n"
    code += "print(\"NONZERO_MULTIPLIERS\"); print(nz);\n"
    code += "print(\"BEGIN_LIFT\"); L; print(\"END_LIFT\");\n"
    return code


def marked_value(output, marker):
    lines = output.splitlines()
    index = lines.index(marker)
    return lines[index + 1]


def main():
    tokens, labels, generators = build_generators()
    first = diagonal_coefficient((2, 3, 4, 5), (1, 1, 1, 1))
    second = diagonal_coefficient((0, 1, 4, 5), (2, 2, 2, 2))
    top = diagonal_coefficient(SITES, (0, 0, 0, 0, 0, 0))
    target = f"{first}*{second}*{top}"
    code = singular_program(generators, target)

    singular = Path("/usr/local/bin/Singular")
    require(singular.exists(), "Singular 4.4.x is required for this checker")
    result = subprocess.run(
        (str(singular), "-q"),
        input=code,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )
    require(result.returncode == 0,
            f"Singular failed: {result.stderr or result.stdout}")
    require("SOURCE_LIFT_FAILED" not in result.stdout,
            "the source-generator lift no longer verifies")
    basis_size = int(marked_value(result.stdout, "BASIS_SIZE"))
    remainder = marked_value(result.stdout, "REMAINDER")
    multipliers = int(marked_value(result.stdout, "NONZERO_MULTIPLIERS"))
    require(basis_size == EXPECTED_STANDARD_BASIS_SIZE,
            f"the standard-basis size changed: {basis_size}")
    require(remainder == "0", f"the target acquired remainder {remainder}")
    require(multipliers == 34,
            f"the source lift multiplier count changed: {multipliers}")

    lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split(
        "\nEND_LIFT", 1
    )[0]
    lift_digest = sha256(lift.encode()).hexdigest()
    if EXPECTED_LIFT_DIGEST != "TO_BE_FILLED":
        require(lift_digest == EXPECTED_LIFT_DIGEST,
                f"the exact lift changed: {lift_digest}")

    nonzero_labels = []
    for line in lift.splitlines():
        if not line.startswith("L[") or line.endswith("=0"):
            continue
        index = int(line.split("[", 1)[1].split(",", 1)[0]) - 1
        nonzero_labels.append(labels[index])
    require(len(nonzero_labels) == multipliers,
            "the lift-label extraction changed")

    ledger = {
        "variables": len(VARIABLES),
        "generators": len(generators),
        "generator_labels": labels,
        "target": target,
        "standard_basis_size": basis_size,
        "remainder": remainder,
        "source_lift_nonzero_multipliers": multipliers,
        "source_lift_labels": nonzero_labels,
        "source_lift_sha256": lift_digest,
        "verdict": (
            "the colour-diagonal silent unary-top chart is empty over C; "
            "arbitrary support and aggregate cancellation included"
        ),
        "scope": (
            "equal-colour internal Q cells and concentrated ordered response "
            "holes (01),(23); no conclusion for off-diagonal Q cells or "
            "multisite endpoint stars"
        ),
        "fine_tokens": {str(site): list(values)
                        for site, values in tokens.items()},
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                f"the diagonal aggregate ledger changed: {digest}")

    print("N=8 unary-top diagonal aggregate identity: PASS")
    print("ring=Q[45]; zero generators=71; standard basis=251")
    print("pure-cofactor product remainder=0; source multipliers=34")
    print(f"lift sha256: {lift_digest}")
    print("full off-diagonal/multisite packet: OPEN")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
