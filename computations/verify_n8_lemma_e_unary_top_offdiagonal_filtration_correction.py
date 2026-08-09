#!/usr/bin/env python3
"""Lift the diagonal unary-top unit identity through off-diagonal degree.

The pinned diagonal checker supplies an exact 34-row source lift

    A*B*C = sum_i m_i g_i^diag.

Replace each diagonal matching coefficient by its full 3x3-block
coefficient, but retain the same diagonal multipliers.  Scaling every
off-diagonal cell by z gives the exact corrected identity

    A*B*C + E_2 + E_3 = sum_i m_i g_i^full,

where E_j has exactly j off-diagonal internal cells.  The entire linear
correction cancels: E_1=0.  This checker asks Singular to construct and
split the correction, verifies the identity over Q, and freezes each
nonzero filtration component.  It is a first-correction theorem, not an
emptiness result for the full mixed-colour chart.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import re
import subprocess

import verify_n8_lemma_e_unary_top_diagonal_aggregate_identity as diagonal


ROOT = Path(__file__).resolve().parents[1]
PINNED_DIAGONAL_SHA256 = (
    "d805a2d78ddf83239b2edca0598b8a88f90517296b375613030eb24defb1b2c2"
)
EXPECTED_LEDGER_DIGEST = "e26d22e60cb86c3ad1cca4cfebbd51a15dfc08a9c2ae6eec1f4140cc1d68378d"
EXPECTED_COMPONENT_DIGESTS = {
    2: "32c41ca47d2d4e2d9f4f1af398a3ea61693527c4591f9c1a75f2407ee2c3eaae",
    3: "c84a01cebf993efd441d2627cbe55219db95f56562c1bdf1be2d6f072aa5c492",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependency():
    path = ROOT / (
        "computations/"
        "verify_n8_lemma_e_unary_top_diagonal_aggregate_identity.py"
    )
    require(sha256(path.read_bytes()).hexdigest() == PINNED_DIAGONAL_SHA256,
            "the diagonal aggregate-identity dependency changed")


def offdiagonal_name(edge, left, right):
    return f"o{edge[0]}{edge[1]}{left}{right}"


OFFDIAGONAL_VARIABLES = tuple(
    (edge, left, right)
    for edge in diagonal.EDGES
    for left in diagonal.COLORS
    for right in diagonal.COLORS
    if left != right
)
OFFDIAGONAL_NAME = {
    variable: offdiagonal_name(*variable)
    for variable in OFFDIAGONAL_VARIABLES
}


def full_variable(edge, left, right, scaled=False):
    if left == right:
        return diagonal.VARIABLE_NAME[(edge, left)]
    name = OFFDIAGONAL_NAME[(edge, left, right)]
    return f"z*{name}" if scaled else name


def full_coefficient(vertices, word, scaled=False):
    vertices = tuple(vertices)
    position = {vertex: index for index, vertex in enumerate(vertices)}
    terms = []
    for matching in diagonal.perfect_matchings(vertices):
        factors = []
        for edge in matching:
            factors.append(full_variable(
                edge,
                word[position[edge[0]]],
                word[position[edge[1]]],
                scaled=scaled,
            ))
        terms.append("*".join(factors))
    return "(" + "+".join(terms) + ")"


def full_generator_from_label(label, scaled=False):
    fields = label.split(":")
    if fields[0] == "top":
        word = tuple(map(int, fields[1]))
        return full_coefficient(diagonal.SITES, word, scaled=scaled)
    require(fields[0] == "cofactor" and len(fields) == 3,
            f"unrecognized source label {label}")
    holes = tuple(map(int, fields[1]))
    vertices = tuple(site for site in diagonal.SITES if site not in holes)
    word = tuple(map(int, fields[2]))
    return full_coefficient(vertices, word, scaled=scaled)


def diagonal_target():
    first = diagonal.diagonal_coefficient((2, 3, 4, 5), (1, 1, 1, 1))
    second = diagonal.diagonal_coefficient((0, 1, 4, 5), (2, 2, 2, 2))
    top = diagonal.diagonal_coefficient(
        diagonal.SITES, (0, 0, 0, 0, 0, 0)
    )
    return f"{first}*{second}*{top}"


def recover_diagonal_lift(generators, target):
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=diagonal.singular_program(generators, target),
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )
    require(result.returncode == 0,
            f"the pinned diagonal Singular lift failed: {result.stderr}")
    lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split(
        "\nEND_LIFT", 1
    )[0]
    require(sha256(lift.encode()).hexdigest()
            == diagonal.EXPECTED_LIFT_DIGEST,
            "the recovered diagonal source lift changed")
    multipliers = []
    for index, line in enumerate(lift.splitlines(), start=1):
        prefix = f"L[{index},1]="
        require(line.startswith(prefix),
                "the diagonal lift matrix format changed")
        multipliers.append(line[len(prefix):])
    require(len(multipliers) == len(generators) == 71,
            "the diagonal lift length changed")
    require(sum(value != "0" for value in multipliers) == 34,
            "the diagonal nonzero-multiplier count changed")
    return multipliers


def corrected_singular_program(labels, diagonal_generators, multipliers):
    diagonal_names = [diagonal.VARIABLE_NAME[variable]
                      for variable in diagonal.VARIABLES]
    offdiagonal_names = [OFFDIAGONAL_NAME[variable]
                         for variable in OFFDIAGONAL_VARIABLES]
    names = ",".join(diagonal_names + offdiagonal_names + ["z"])
    terms = []
    active_labels = []
    for label, old, multiplier in zip(
            labels, diagonal_generators, multipliers):
        if multiplier == "0":
            continue
        new = full_generator_from_label(label, scaled=True)
        terms.append(f"({multiplier})*(({new})-({old}))")
        active_labels.append(label)
    require(len(terms) == len(active_labels) == 34,
            "the active correction-row count changed")

    code = f"ring r=0,({names}),dp;\n"
    code += "poly Ez=" + "+".join(terms) + ";\n"
    code += "poly E0=subst(Ez,z,0);\n"
    code += "poly D1=diff(Ez,z); poly E1=subst(D1,z,0);\n"
    code += "poly D2=diff(D1,z); poly E2=subst(D2,z,0)/2;\n"
    code += "poly D3=diff(D2,z); poly E3=subst(D3,z,0)/6;\n"
    code += "poly D4=diff(D3,z);\n"
    code += (
        "if(E0!=0 || D4!=0 || Ez-z*E1-z2*E2-z3*E3!=0)"
        "{ print(\"FILTRATION_SPLIT_FAILED\"); exit(1); }\n"
    )
    code += "print(\"COMPONENT_SIZES\"); print(size(E1)); print(size(E2)); print(size(E3));\n"
    for degree in (1, 2, 3):
        code += f"print(\"BEGIN_E{degree}\"); E{degree}; print(\"END_E{degree}\");\n"
    return code, active_labels


def marked_component(output, degree):
    return output.split(f"BEGIN_E{degree}\n", 1)[1].split(
        f"\nEND_E{degree}", 1
    )[0]


def component_variable_profile(component):
    variables = re.findall(r"o[0-5][0-5][0-2][0-2]", component)
    counts = Counter(variables)
    return {
        "distinct_offdiagonal_variables": len(counts),
        "occurrence_histogram": dict(sorted(Counter(counts.values()).items())),
        "edge_histogram": dict(sorted(Counter(name[1:3]
                                              for name in counts).items())),
        "ordered_colour_histogram": dict(sorted(Counter(name[3:5]
                                                        for name in counts).items())),
    }


def component_transition_profile(component, degree):
    """Classify the colour-change graph of every correction monomial."""
    terms = [term for term in re.split(
        r"(?=[+-])", component.replace("\n", "")
    ) if term]
    signatures = Counter()
    for term in terms:
        variables = re.findall(r"o[0-5][0-5][0-2][0-2]", term)
        require(len(variables) == degree,
                f"an E{degree} monomial has the wrong off-diagonal degree")
        require(len(set(variables)) == degree,
                f"an E{degree} monomial repeated an off-diagonal cell")
        signature = tuple(sorted(
            "".join(sorted(variable[3:5]))
            for variable in variables
        ))
        signatures[signature] += 1
    return {"term_count": len(terms),
            "transition_signatures": {
                ",".join(signature): count
                for signature, count in sorted(signatures.items())
            }}


def main():
    pin_dependency()
    _tokens, labels, generators = diagonal.build_generators()
    target = diagonal_target()
    multipliers = recover_diagonal_lift(generators, target)
    program, active_labels = corrected_singular_program(
        labels, generators, multipliers
    )
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=program,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )
    require(result.returncode == 0,
            f"the full correction split failed: {result.stderr or result.stdout}")
    require("FILTRATION_SPLIT_FAILED" not in result.stdout,
            "the exact off-diagonal filtration decomposition failed")
    lines = result.stdout.splitlines()
    size_index = lines.index("COMPONENT_SIZES")
    sizes = {degree: int(lines[size_index + degree])
             for degree in (1, 2, 3)}
    components = {degree: marked_component(result.stdout, degree)
                  for degree in (1, 2, 3)}
    require(sizes[1] == 0 and components[1] == "0",
            "the linear off-diagonal cancellation changed")
    require(all(sizes[degree] > 0 and components[degree] != "0"
                for degree in (2, 3)),
            "a nonlinear off-diagonal correction component vanished")
    digests = {degree: sha256(components[degree].encode()).hexdigest()
               for degree in (1, 2, 3)}
    for degree in (2, 3):
        expected = EXPECTED_COMPONENT_DIGESTS[degree]
        if expected != "TO_BE_FILLED":
            require(digests[degree] == expected,
                    f"filtration component E{degree} changed: {digests[degree]}")

    profiles = {degree: component_variable_profile(components[degree])
                for degree in (1, 2, 3)}
    transitions = {
        degree: component_transition_profile(components[degree], degree)
        for degree in (2, 3)
    }
    require(transitions[2]["term_count"] == sizes[2]
            and transitions[2]["transition_signatures"]
            == {"01,01": 110, "02,02": 90, "12,12": 82},
            "the quadratic two-cycle classification changed")
    require(transitions[3]["term_count"] == sizes[3]
            and transitions[3]["transition_signatures"]
            == {"01,02,12": 16},
            "the cubic colour-triangle classification changed")
    ledger = {
        "pinned_diagonal_sha256": PINNED_DIAGONAL_SHA256,
        "pinned_lift_sha256": diagonal.EXPECTED_LIFT_DIGEST,
        "diagonal_variables": len(diagonal.VARIABLES),
        "offdiagonal_variables": len(OFFDIAGONAL_VARIABLES),
        "source_rows": len(labels),
        "active_source_rows": len(active_labels),
        "active_source_labels": active_labels,
        "correction_component_sizes": sizes,
        "correction_component_sha256": digests,
        "correction_variable_profiles": profiles,
        "correction_transition_profiles": transitions,
        "identity": "ABC + E2 + E3 = sum_i m_i*g_i_full; E1=0",
        "exact_solution_consequence": "E2+E3=-1",
        "verdict": (
            "the diagonal unit identity lifts through first off-diagonal "
            "order; its first nonzero correction is quadratic"
        ),
        "scope": (
            "concentrated ordered response holes only; this identifies the "
            "mixed-cell obstruction but does not prove the full chart empty"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_DIGEST,
                f"the off-diagonal correction ledger changed: {digest}")

    print("N=8 unary-top off-diagonal filtration correction: PASS")
    print("ring variables diagonal/off-diagonal: 45 / 90")
    print("active diagonal source multipliers: 34")
    print("correction term counts:", sizes)
    print("correction sha256:", digests)
    print("linear off-diagonal correction: 0")
    print("exact consequence on the full concentrated packet: E2+E3=-1")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
