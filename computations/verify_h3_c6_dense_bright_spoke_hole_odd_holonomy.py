#!/usr/bin/env python3
"""Close the dense canonical C6 spoke-to-hole branch by odd holonomy.

At z=012111 retain M,N and all six anchor-contained competitors.  Three
literal shifted response coefficients through the already selected ports,
together with the unary z coefficient, give four binomial pair equations
after every external/additional-hole mate is excluded.  One toric matching
identity turns them into twice a localized unit.

The conclusion is a full-source dichotomy on this dense branch: an external
q mate or an additional endpoint-hole term must occur.  It is not a claim
that every support-degenerate subbranch is empty.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_c6_first_transgression_selected_port_boundary.py":
        "8729c85d5af458966942e567e5e840da9fe0acf0a9d89684b846bee82b791f9a",
    "notes/h3-c6-first-transgression-selected-port-boundary.md":
        "03bed57e2a1955795806b590e586c16e3a25948e719ff1d589a462460a8684b1",
    "computations/verify_h3_c6_z_spoke_hole_koszul_boundary.py":
        "85814705ad28631cccc13728f216adcbfc4ee94f65a01846e187253497fc5bfe",
    "notes/h3-c6-z-spoke-hole-koszul-boundary.md":
        "b0f80125431d59e5f393986161136f77c7e0d0db2401c0ca6c9298e5a46f720e",
    "computations/verify_h3_c6_endpoint_visibility_augmented_map_gate.py":
        "589d88020b87c5892be832758c74c73832747c265f4139b6917069685dcd9375",
    "notes/h3-c6-endpoint-visibility-augmented-map-gate.md":
        "e9cf5650023588c7a94b37b98912898cc5120dab9968c2d860a72dce60faa48e",
}
EXPECTED_LEDGER_SHA256 = "0b0cf648b49d44e91677927413908a06280111083bfdbc95424baee750091f10"

SITES = tuple(range(6))
Z = (0, 1, 2, 1, 1, 1)
M = ((0, 1), (2, 3), (4, 5))
N = ((0, 5), (1, 2), (3, 4))
Q1 = ((0, 1), (2, 4), (3, 5))
Q2 = ((0, 2), (1, 3), (4, 5))
Q3 = ((0, 2), (1, 4), (3, 5))
Q4 = ((0, 2), (1, 5), (3, 4))
Q5 = ((0, 5), (1, 3), (2, 4))
Q6 = ((0, 5), (1, 4), (2, 3))
DENSE = (M, N, Q1, Q2, Q3, Q4, Q5, Q6)

OLD_BASE_UNION = set().union(*(set(base) for base in (
    M, Q1, Q4, N,
)))

BRIGHT_11 = (
    ((2, 3), (4, 5)),
    ((2, 4), (3, 5)),
    ((2, 5), (3, 4)),
)
BRIGHT_22 = (
    ((0, 1), (2, 5)),
    ((0, 2), (1, 5)),
    ((0, 5), (1, 2)),
)

SHIFTED_ROWS = {
    "G11_y01": {"hole": (0, 1), "colours": (1, 1),
                  "word": (1, 1, 2, 1, 1, 1)},
    "G21_y13": {"hole": (1, 3), "colours": (1, 2),
                  "word": (0, 1, 2, 2, 1, 1)},
    "G22_y34": {"hole": (3, 4), "colours": (2, 2),
                  "word": (0, 1, 2, 2, 2, 1)},
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)


def matching_name(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def q_variable(edge, word):
    return f"q{edge[0]}{edge[1]}_{word[edge[0]]}{word[edge[1]]}"


def q_monomial(matching, word=Z):
    return tuple(sorted(q_variable(edge, word) for edge in matching))


def polynomial(*terms):
    answer = Counter()
    for coefficient, monomial in terms:
        answer[tuple(sorted(monomial))] += coefficient
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def add(*scaled):
    answer = Counter()
    for scalar, value in scaled:
        for monomial, coefficient in value.items():
            answer[monomial] += scalar * coefficient
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def multiply(left, right):
    answer = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def monomial_value(matching):
    return polynomial((1, q_monomial(matching)))


def selected_q_cells(first_tail, second_tail):
    cells = {(edge, (Z[edge[0]], Z[edge[1]]))
             for matching in DENSE for edge in matching}
    cells |= {(edge, (1, 1)) for edge in first_tail}
    cells |= {(edge, (2, 2)) for edge in second_tail}
    return cells


def supported_matchings(vertices, word, cells):
    answer = []
    for matching in perfect_matchings(vertices):
        if all((edge, (word[edge[0]], word[edge[1]])) in cells
               for edge in matching):
            answer.append(matching)
    return tuple(answer)


def audit_bright_envelope():
    records = []
    expected = {
        "top_z": tuple(DENSE),
        "G11_y01": (((2, 3), (4, 5)), ((2, 4), (3, 5))),
        "G21_y13": (((0, 2), (4, 5)), ((0, 5), (2, 4))),
        "G22_y34": (((0, 2), (1, 5)), ((0, 5), (1, 2))),
    }
    for first_index, first_tail in enumerate(BRIGHT_11, 1):
        for second_index, second_tail in enumerate(BRIGHT_22, 1):
            cells = selected_q_cells(first_tail, second_tail)
            top = supported_matchings(SITES, Z, cells)
            require(set(top) == set(expected["top_z"]),
                    "a bright tail changed the dense unary z support")
            row_support = {}
            for name, data in SHIFTED_ROWS.items():
                vertices = tuple(site for site in SITES
                                 if site not in data["hole"])
                support = supported_matchings(vertices, data["word"], cells)
                require(set(support) == set(expected[name]),
                        f"a bright tail changed {name}: {support}")
                row_support[name] = support
            records.append({
                "X1_tail_index": first_index,
                "X2_tail_index": second_index,
                "top_support": top,
                "shifted_row_support": row_support,
            })
    require(len(records) == 9,
            "the sharp bright completion stopped having nine charts")
    return {
        "chart_count": len(records),
        "invariant_support": expected,
        "records": records,
        "consequence": (
            "arbitrary selected pure-11/pure-22 bright cofactor tails add "
            "no term to the four load-bearing mixed coefficients"
        ),
    }


def audit_external_terms():
    selected = set(DENSE)
    external_top = []
    for matching in MATCHINGS:
        if matching in selected:
            continue
        cells = tuple((edge, (Z[edge[0]], Z[edge[1]]))
                      for edge in matching)
        require(any(edge not in OLD_BASE_UNION
                    and colours[0] != colours[1]
                    for edge, colours in cells),
                "a nonselected top-z term stopped being an external route")
        external_top.append(matching)
    require(len(external_top) == 7,
            "the top-z external matching count changed")

    missing_tails = {
        "G11_y01": ((2, 5), (3, 4)),
        "G21_y13": ((0, 4), (2, 5)),
        "G22_y34": ((0, 1), (2, 5)),
    }
    for name, tail in missing_tails.items():
        word = SHIFTED_ROWS[name]["word"]
        require(any(edge not in OLD_BASE_UNION
                    and word[edge[0]] != word[edge[1]]
                    for edge in tail),
                f"the omitted {name} tail stopped being external")
    return {
        "top_z_external_matchings": external_top,
        "shifted_row_external_tails": missing_tails,
        "other_endpoint_holes": (
            "any further term in these full response coefficients uses an "
            "additional endpoint component and is exactly the desired "
            "spoke-to-hole/another-hole branch"
        ),
    }


def audit_odd_holonomy():
    values = {name: monomial_value(matching) for name, matching in (
        ("M", M), ("N", N),
        ("Q1", Q1), ("Q2", Q2), ("Q3", Q3),
        ("Q4", Q4), ("Q5", Q5), ("Q6", Q6),
    )}
    e01 = add((1, values["M"]), (1, values["Q1"]))
    e13 = add((1, values["Q2"]), (1, values["Q5"]))
    e34 = add((1, values["N"]), (1, values["Q4"]))
    top = add(*((1, values[name]) for name in values))
    e14 = add((1, top), (-1, e01), (-1, e13), (-1, e34))
    require(e14 == add((1, values["Q3"]), (1, values["Q6"])),
            "the fourth binomial stopped being the unary remainder")

    # Literal toric matching identity.
    left_unit = multiply(multiply(values["Q1"], values["Q2"]),
                         values["Q6"])
    right_unit = multiply(multiply(values["M"], values["Q3"]),
                          values["Q5"])
    require(left_unit == right_unit,
            "the six-base toric matching identity changed")

    # Q2*Q6*e01 - M*Q6*e13 + M*Q5*e14 = 2*unit.
    certificate = add(
        (1, multiply(multiply(values["Q2"], values["Q6"]), e01)),
        (-1, multiply(multiply(values["M"], values["Q6"]), e13)),
        (1, multiply(multiply(values["M"], values["Q5"]), e14)),
    )
    expected = Counter({monomial: 2 * coefficient
                        for monomial, coefficient in left_unit.items()})
    require(certificate == expected,
            "the integral odd-holonomy certificate changed")
    require(len(expected) == 1,
            "the certificate target stopped being one monomial")
    return {
        "normalized_source_rows": {
            "E01": "M+Q1",
            "E13": "Q2+Q5",
            "E34": "N+Q4",
            "E14": "top-E01-E13-E34=Q3+Q6",
        },
        "denominator_clearance": {
            "E01": (
                "q01:01*G11[112111]/(p1@0:1*s1@1:1) in the "
                "selected-factor localization"
            ),
            "E13": (
                "q13:11*G21[012211]/(p2@3:2*s1@1:1) in the "
                "selected-factor localization"
            ),
            "E34": (
                "q34:11*G22[012221]/(p2@3:2*s2@4:2) in the "
                "selected-factor localization"
            ),
            "polynomial_form": (
                "multiplication by the product of the three selected "
                "endpoint factors clears every denominator in E14 and "
                "the final certificate"
            ),
        },
        "toric_identity": "Q1*Q2*Q6=M*Q3*Q5",
        "integral_certificate": (
            "Q2*Q6*E01-M*Q6*E13+M*Q5*E14="
            "2*Q1*Q2*Q6"
        ),
        "target_coefficient": 2,
        "localized_unit": next(iter(expected)),
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    ledger = {
        "word": "".join(map(str, Z)),
        "dense_matching_basis": tuple(matching_name(value) for value in DENSE),
        "sharp_bright_completion": audit_bright_envelope(),
        "complete_coefficient_exits": audit_external_terms(),
        "odd_holonomy": audit_odd_holonomy(),
        "theorem": (
            "in any full characteristic-zero source containing all eight "
            "dense z monomials, the unary coefficient and the three "
            "shifted selected-port response coefficients cannot have only "
            "the displayed terms.  A complete row must supply an external "
            "q mate or an additional endpoint-hole term"
        ),
        "scope": (
            "full-source branch theorem localized at the eight dense z "
            "monomials and selected endpoint factors.  It does not exclude "
            "support-degenerate subbranches where one binomial pair is "
            "absent, and it does not claim that an arbitrary extra endpoint "
            "term is already rank-good"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"C6 dense bright holonomy ledger changed: {digest}")
    print("h3 C6 dense bright spoke-to-hole odd holonomy: PASS")
    print("nine bright charts preserve exact supports 8/2/2/2")
    print("four binomials + toric identity -> 2*localized unit")
    print("full-source exit: external q mate or additional endpoint hole")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
