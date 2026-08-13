#!/usr/bin/env python3
"""Verify the exact restriction/insertion law for centered occurrences.

For occurrence order r, an occurrence is an ordered endpoint pair together
with a perfect matching on the remaining 2r-2 sites.  Restriction D_e removes
a specified residual matching edge.  The centered class restricts to a lower
centered class plus the constant carrier on marked residual cuts, and to the
negative constant carrier on every other cut.  Summing insertion after
restriction reconstructs every occurrence exactly r-1 times.

This is the coefficient shadow required of a physical oriented four-cut
chain map.  The lower centered summands are a sharp obstruction to treating
all restrictions as copies of one common H0 carrier.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/uniform-centered-occurrence-endpoint-association-projector.md":
        "6be3edc16be3b429f517fe007886fd3289281f8e8acdde1f13ebebf2a20bb836",
    "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py":
        "0ef88312cead100120e4600ea3a2d0616262a96bf27726d07817610d11b43f59",
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "notes/h3-centered-occurrence-same-grade-physical-gate.md":
        "b183f3b5dab83fa79d17c3f539b9f146e3be176a96bfe52b267529148b64134a",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "notes/h3-degree4-reset-five-face-aggregate-gate.md":
        "5a19c7b8bfb21cb0c76532accb3af1f0ea4cdb6b13fa6b500124f77f61395100",
    "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py":
        "01961c9ae83b91dad31ba859ea2f8a2d5775d73d7ad591aa0a369e7d971f8079",
    "notes/scalar-unit-c0-four-cut-common-carrier-gate.md":
        "a06018da73d6a954f14706fcfdeaae5ace1c2424e02530ab87602c1e77271000",
    "computations/verify_scalar_unit_c0_four_cut_common_carrier_gate.py":
        "56421c894acd613300841b7ae41d1bafecc6d65fcc9618982dc61ac198c2fa66",
}
EXPECTED_LEDGER_SHA256 = (
    "a92134cb67e6d08ee65de51473ed6dec7cd2c11502e0855343afb4b4c53ec7b9"
)


Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Occurrence = tuple[int, int, Matching]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> Edge:
    require(left != right, "loop edge")
    return (left, right) if left < right else (right, left)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted((edge(first, second),) + tail)))
    return tuple(answer)


def occurrences(vertices: tuple[int, ...]) -> tuple[Occurrence, ...]:
    answer = []
    for p_site in vertices:
        for s_site in vertices:
            if p_site == s_site:
                continue
            rest = tuple(site for site in vertices
                         if site not in (p_site, s_site))
            for matching in perfect_matchings(rest):
                answer.append((p_site, s_site, matching))
    require(len(answer) == len(set(answer)), "duplicate occurrence")
    return tuple(answer)


def odd_double_factorial(value: int) -> int:
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def occurrence_count(order: int) -> int:
    return 2 * order * (2 * order - 1) * odd_double_factorial(2 * order - 3)


def restrict_occurrence(occurrence: Occurrence, selected: Edge) -> Occurrence | None:
    p_site, s_site, matching = occurrence
    if selected not in matching:
        return None
    return (p_site, s_site,
            tuple(candidate for candidate in matching if candidate != selected))


def component_audit(order: int) -> dict[str, object]:
    vertices = tuple(range(2 * order))
    source = occurrences(vertices)
    count = occurrence_count(order)
    require(len(source) == count,
            ("occurrence count changed", order, len(source), count))
    marked = source[0]
    marked_matching = set(marked[2])
    lower_count = occurrence_count(order - 1)
    ratio = Fraction(count, lower_count)
    expected_ratio = Fraction(order * (2 * order - 1), order - 1)
    require(ratio == expected_ratio,
            ("restriction ratio changed", order, ratio, expected_ratio))

    all_edges = tuple(edge(left, right)
                      for left in vertices for right in vertices
                      if left < right)
    marked_components = []
    unmarked_components = []
    insertion_multiplicity = {occurrence: 0 for occurrence in source}
    for selected in all_edges:
        complement = tuple(site for site in vertices if site not in selected)
        lower = occurrences(complement)
        lower_set = set(lower)
        restricted = {}
        for occurrence in source:
            image = restrict_occurrence(occurrence, selected)
            if image is None:
                continue
            require(image in lower_set,
                    ("restriction left lower occurrence module", order,
                     selected, image))
            require(image not in restricted,
                    ("restriction stopped being bijective", order, selected))
            restricted[image] = occurrence
            insertion_multiplicity[occurrence] += 1
        require(set(restricted) == lower_set,
                ("complete row did not restrict to complete lower row",
                 order, selected, len(restricted), len(lower)))
        require(len(lower) == lower_count, "lower occurrence count changed")

        marked_image = restrict_occurrence(marked, selected)
        # D_e c has coefficient N_r-1 at the marked lower coordinate when
        # the marked matching contains e, and -1 everywhere else.
        actual = {
            item: Fraction(count if item == marked_image else 0) - 1
            for item in lower
        }
        if selected in marked_matching:
            require(marked_image is not None, "lost marked restriction")
            centered_lower = {
                item: Fraction(lower_count if item == marked_image else 0) - 1
                for item in lower
            }
            expected = {
                item: ratio * centered_lower[item] + (ratio - 1)
                for item in lower
            }
            require(actual == expected,
                    ("marked centered restriction law changed", order,
                     selected))
            comparison = next(item for item in lower if item != marked_image)
            # The primitive coordinate-difference dual kills the lower
            # constant carrier and reads N_r on the restricted centered row.
            dual_value = actual[marked_image] - actual[comparison]
            require(dual_value == count,
                    ("lower centered dual changed", order, selected,
                     dual_value, count))
            marked_components.append({
                "edge": list(selected),
                "lower_centered_coefficient": str(ratio),
                "constant_coefficient": str(ratio - 1),
                "primitive_difference_dual_value": str(dual_value),
            })
        else:
            require(marked_image is None, "unmarked edge acquired marked image")
            require(all(value == -1 for value in actual.values()),
                    ("unmarked restriction stopped being -1", order,
                     selected))
            unmarked_components.append(list(selected))

    require(set(insertion_multiplicity.values()) == {order - 1},
            ("sum insertion after restriction changed", order,
             set(insertion_multiplicity.values())))
    require(len(marked_components) == order - 1,
            "wrong number of marked residual cuts")
    return {
        "order": order,
        "sites": 2 * order,
        "occurrences": count,
        "lower_occurrences_per_cut": lower_count,
        "alpha": str(ratio),
        "marked_residual_cuts": marked_components,
        "unmarked_cut_count": len(unmarked_components),
        "global_reconstruction": f"sum_e I_e D_e = {order - 1} id",
    }


def uniform_projector_audit() -> dict[str, object]:
    records = []
    for response_order in range(3, 9):
        scheme_order = response_order - 1
        matching_lambda = scheme_order ** 2 - 3 * scheme_order + 1
        endpoint_nonconstant = (-2, 2 * scheme_order - 2,
                                2 * scheme_order)
        endpoint_constant = 4 * scheme_order
        endpoint_value = 1
        for root in endpoint_nonconstant:
            endpoint_value *= endpoint_constant - root
        endpoint_denominator = (
            8 * scheme_order * (scheme_order + 1)
            * (2 * scheme_order + 1)
        )
        matching_denominator = 2 * scheme_order - 1
        require(endpoint_value == endpoint_denominator,
                ("endpoint normalization changed", response_order))
        combined = matching_denominator * endpoint_denominator
        records.append({
            "response_order": response_order,
            "scheme_order": scheme_order,
            "matching_factor": (
                f"A-{matching_lambda}I"
            ),
            "endpoint_factors": [
                "B+2I", f"B-{2 * response_order - 4}I",
                f"B-{2 * response_order - 2}I",
            ],
            "rational_denominator": combined,
        })
    require(records[0]["rational_denominator"] == 720,
            "h3 projector denominator changed")
    return {
        "uniform_numerator": (
            "(A_(r-1)-(r^2-5r+5)I)(B_(r-1)+2I)"
            "(B_(r-1)-(2r-4)I)(B_(r-1)-(2r-2)I)"
        ),
        "uniform_denominator": "(2r-3)*8(r-1)r(2r-1)",
        "records": records,
    }


def physical_scope_audit() -> dict[str, object]:
    projector = (ROOT / "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md").read_text()
    same_grade = (ROOT / "notes/h3-centered-occurrence-same-grade-physical-gate.md").read_text()
    reset = (ROOT / "notes/h3-degree4-reset-five-face-aggregate-gate.md").read_text()
    c_zero = (ROOT / "notes/scalar-unit-c0-four-cut-common-carrier-gate.md").read_text()
    require("`01211222`" in projector
            and "labelled repeated `P3+K2` grade" in projector,
            "h3 cap word/fine grade changed")
    require("90-term sum" in same_grade
            and "two independent pieces" in same_grade,
            "same-grade occurrence obstruction changed")
    require(r"h_v(H_0-u)e_{\rm Eq}" in reset
            and "word/fine/repeated-grade comparison" in reset,
            "physical reset obstruction changed")
    require("augmented carrier" in c_zero
            and "restriction--insertion/base-change comparison" in c_zero,
            "common-carrier hypothesis changed")
    return {
        "coefficient_shadow": (
            "restriction/insertion is exact and uniform, but marked cuts "
            "retain lower centered occurrence classes"
        ),
        "h3_forgotten_grade_obstruction": (
            "two marked residual cuts each carry a primitive lower class "
            "detected with value 90; common H0 constants are killed"
        ),
        "h3_physical_grade": "word 01211222, labelled repeated P3+K2",
        "first_known_physical_attempt": (
            "the degree-four cross-word reset totalizes universally only "
            "up to h_v*(H0-u)*e_Eq"
        ),
        "status_of_dual": (
            "the lower coordinate-difference covector is an associated-"
            "graded obstruction, not a physical terminal until transported "
            "through the complete augmented word/fine map"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform centered occurrence restriction/insertion gate",
        "pins": PINS,
        "components": [component_audit(order) for order in (2, 3, 4)],
        "uniform_projector": uniform_projector_audit(),
        "physical_scope": physical_scope_audit(),
        "verdict": (
            "The residual-edge restriction/insertion correspondence is an "
            "exact coefficient reconstruction: sum I_e D_e=(r-1)id.  It "
            "does not send the centered occurrence projector to copies of "
            "one common H0 carrier.  A marked residual cut contains "
            "alpha_r c_(f/e,r-1)+(alpha_r-1)1 with "
            "alpha_r=r(2r-1)/(r-1); every unmarked cut is -1.  At r=3 "
            "the two marked cuts carry (15/2)c_lower+(13/2)1 and are "
            "detected modulo constants with value 90.  Therefore the "
            "complete physical c0 map must fill these lower centered "
            "classes and transport all constant components in one "
            "word/fine/repeated-grade base-change.  Uniformity is direct "
            "in r through the displayed association polynomial and this "
            "restriction law; fixed spectator tensoring is not the law."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("restriction/insertion ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("centered residual-edge restriction/insertion: EXACT")
    print("h3 marked cuts: (15/2)c_lower+(13/2)H0")
    print("common-H0-only physical chain map: OBSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
