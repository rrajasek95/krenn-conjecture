#!/usr/bin/env python3
"""Exact 18-row unit certificate for the arbitrary binary two-hole square.

The pinned two-hole tensor split reduces a >=3-centre target-axis kernel to
three zero binary cofactors K_0,K_1,K_2 and two pure nonzero cofactors on
the remaining holes.  Sitewise torus scaling normalizes the latter to
K_3=X_0 and K_4=X_1 (up to swapping the two colours).

For completely arbitrary ordered 2x2 cells q_uv(i,j), this checker builds
all 80 literal coefficient rows, asks Singular for a characteristic-zero
source lift of 1, verifies the lift by exact multiplication, and freezes
its 18 nonzero source multipliers and row labels.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(5))
COLOURS = tuple(range(2))
EDGES = tuple(combinations(SITES, 2))
PINNED_TENSOR_SPLIT_SHA256 = (
    "ba6fcd520d8678c081ea9192628f46bb0e700d18e6ee914b2b32790cee9d00be"
)
EXPECTED_LIFT_SHA256 = "4aafbfa5d93804089447f4667db845419ff4acd99c11051ba61c4f8eca9a272c"
EXPECTED_LEDGER_SHA256 = "9908daa3de09c9bea768c1163aba70ddc9605b3c6a68a8918f0c8b7b1b800dbf"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_target_axis_mixed_cycle_gate.py"
    )
    require(path.exists(), "the two-hole tensor-split dependency is missing")
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINNED_TENSOR_SPLIT_SHA256,
            f"the two-hole tensor-split dependency changed: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def variable_name(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return f"q{left}{right}{left_colour}{right_colour}"


VARIABLES = tuple(
    variable_name(left, right, left_colour, right_colour)
    for left, right in EDGES
    for left_colour in COLOURS
    for right_colour in COLOURS
)


def cofactor_coefficient(hole, word):
    vertices = tuple(site for site in SITES if site != hole)
    require(len(word) == len(vertices) == 4,
            "a cofactor word has the wrong length")
    colouring = dict(zip(vertices, word))
    terms = []
    for matching in perfect_matchings(vertices):
        require(len(matching) == 2,
                "a four-site matching changed size")
        terms.append("*".join(
            variable_name(left, right,
                          colouring[left], colouring[right])
            for left, right in matching
        ))
    require(len(terms) == 3,
            "a binary four-site coefficient lost a matching")
    return "(" + "+".join(terms) + ")"


def build_generators():
    generators = []
    labels = []
    targets = []
    for hole in (0, 1, 2):
        for word in product(COLOURS, repeat=4):
            generators.append(cofactor_coefficient(hole, word))
            labels.append(f"K{hole}:" + "".join(map(str, word)) + "=0")
            targets.append(0)
    for hole, target_colour in ((3, 0), (4, 1)):
        for word in product(COLOURS, repeat=4):
            polynomial = cofactor_coefficient(hole, word)
            target = int(word == (target_colour,) * 4)
            if target:
                polynomial = f"({polynomial})-1"
            generators.append(polynomial)
            labels.append(
                f"K{hole}:" + "".join(map(str, word)) + f"={target}"
            )
            targets.append(target)
    require(len(VARIABLES) == 40,
            "the arbitrary binary block variable count changed")
    require(len(generators) == len(labels) == len(targets) == 80,
            "the normalized two-hole source-row count changed")
    require(sum(targets) == 2,
            "the two pure target rows changed")
    return labels, generators


def singular_program(generators):
    code = f"ring r=0,({','.join(VARIABLES)}),dp; option(redSB);\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += "matrix L; ideal G=liftstd(I,L);\n"
    code += (
        "if(size(G)!=1 || G[1]!=1 || nrows(L)!=size(I) || ncols(L)!=1)"
        "{ print(\"UNIT_LIFT_SHAPE_FAILED\"); exit(1); }\n"
    )
    code += (
        "if(matrix(I)*L-matrix(G)!=0)"
        "{ print(\"SOURCE_IDENTITY_FAILED\"); exit(1); }\n"
    )
    code += "int i; int nz=0; for(i=1;i<=nrows(L);i++){"
    code += "if(L[i,1]!=0){nz=nz+1;}}\n"
    code += "print(\"NONZERO\"); print(nz);\n"
    code += "print(\"BEGIN_LIFT\"); L; print(\"END_LIFT\");\n"
    return code


def marked_value(output, marker):
    lines = output.splitlines()
    index = lines.index(marker)
    return lines[index + 1]


def parse_lift(lift, row_count):
    multipliers = []
    for index, line in enumerate(lift.splitlines(), start=1):
        prefix = f"L[{index},1]="
        require(line.startswith(prefix),
                "the Singular source-lift matrix format changed")
        multipliers.append(line[len(prefix):])
    require(len(multipliers) == row_count,
            "the source-lift matrix row count changed")
    return multipliers


def audit_torus_normalization():
    # A site scaling q_uv -> s_u s_v q_uv multiplies K_h by the product
    # over all sites except h.  With s0=s1=s2=1, s3=mu^-1,
    # s4=lambda^-1, a pair K3=lambda X0, K4=mu X1 becomes X0,X1.
    exponents = {
        hole: tuple(int(site != hole) for site in SITES)
        for hole in SITES
    }
    require(exponents[3] == (1, 1, 1, 0, 1)
            and exponents[4] == (1, 1, 1, 1, 0),
            "the cofactor site-torus weights changed")
    normalized = {
        "K3": "lambda*(lambda^-1)=1",
        "K4": "mu*(mu^-1)=1",
    }
    return {"cofactor_scaling_exponents": exponents,
            "chosen_site_scales": ["1", "1", "1", "mu^-1", "lambda^-1"],
            "normalized_targets": normalized}


def audit_colour_swap(labels):
    # The other allocation K3=X1,K4=X0 is carried to the checked one by
    # the involution 0<->1.  Audit that the full word set is invariant.
    def swap_word(label):
        head, equation = label.split(":", 1)
        word, target = equation.split("=")
        swapped = "".join("1" if digit == "0" else "0" for digit in word)
        return head + ":" + swapped + "=" + target

    word_sets = {
        hole: {label.split("=", 1)[0] for label in labels
               if label.startswith(f"K{hole}:")}
        for hole in SITES
    }
    for hole in SITES:
        swapped_words = {
            swap_word(label).split("=", 1)[0]
            for label in labels if label.startswith(f"K{hole}:")
        }
        require(swapped_words == word_sets[hole],
                "the binary colour involution changed a cofactor word set")
    return "the colour involution transports the swapped pure allocation"


def main():
    pin_dependency()
    labels, generators = build_generators()
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=singular_program(generators),
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    require(result.returncode == 0,
            f"Singular failed: {result.stderr or result.stdout}")
    require("UNIT_LIFT_SHAPE_FAILED" not in result.stdout
            and "SOURCE_IDENTITY_FAILED" not in result.stdout,
            "the characteristic-zero source lift failed")
    nonzero_count = int(marked_value(result.stdout, "NONZERO"))
    require(nonzero_count == 18,
            f"the unit certificate support changed: {nonzero_count}")
    lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split(
        "\nEND_LIFT", 1
    )[0]
    lift_digest = sha256(lift.encode()).hexdigest()
    if EXPECTED_LIFT_SHA256 != "TO_BE_FILLED":
        require(lift_digest == EXPECTED_LIFT_SHA256,
                f"the two-hole source lift changed: {lift_digest}")
    multipliers = parse_lift(lift, len(generators))
    active = [
        {"row": index + 1, "label": labels[index],
         "multiplier": multiplier}
        for index, multiplier in enumerate(multipliers)
        if multiplier != "0"
    ]
    require(len(active) == nonzero_count,
            "the active source-row extraction changed")
    expected_rows = [7, 11, 15, 23, 27, 31, 39, 43, 47,
                     49, 55, 59, 61, 63, 72, 76, 78, 80]
    require([record["row"] for record in active] == expected_rows,
            "the 18-row source core changed")

    torus = audit_torus_normalization()
    colour_swap = audit_colour_swap(labels)
    ledger = {
        "pinned_tensor_split_sha256": PINNED_TENSOR_SPLIT_SHA256,
        "variables": len(VARIABLES),
        "source_rows": len(generators),
        "active_certificate_rows": active,
        "source_lift_sha256": lift_digest,
        "torus_normalization": torus,
        "swapped_allocation": colour_swap,
        "verdict": (
            "the arbitrary-binary normalized two-hole ideal is the unit "
            "ideal over Q, with an exact 18-row source certificate"
        ),
        "consequence": (
            "a >=3-centre genuinely target-axis two-bad kernel cannot be "
            "rescued by mixed-colour internal cells"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the two-hole unit ledger changed: {digest}")

    print("mixed two-hole characteristic-zero unit: PASS")
    print("ring variables/source rows: 40 / 80")
    print("checked source certificate rows: 18")
    print("active row indices:", expected_rows)
    print(f"lift sha256: {lift_digest}")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
