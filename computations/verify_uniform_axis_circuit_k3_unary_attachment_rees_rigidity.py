#!/usr/bin/env python3
"""Rees rigidity of the c536b88/efac2b2 unary-attachment chart.

Start with the arbitrary pure-zero slice and fixed coordinate-11 slice used
by efac2b2.  Add an independent positive-Rees-order coefficient to every
non-00 decorated cell on all 28 physical edges (224 directions, including
changes of the old 11 cells, all 22 cells, and every off-diagonal cell).

For the 22 literal rows in the integral efac2b2 unit, this checker expands
the actual deformed unary and aggregate-response coefficients.  Their Rees
degree-zero parts are the pinned source rows, so the same multipliers give

    U = 1 + B,  B in (epsilon).

Thus U is a unit in the epsilon-adic completion.  No positive-order
anchor-edge decoration or diagonal-slice deformation attaches the unary
source; a survivor must change the leading face itself.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = (
    "computations/verify_uniform_axis_circuit_k3_pure_unary_attachment_unit.py"
)
PINS = {
    BASE_PATH:
        "432b19fa7ad03a57caa64fc90243443406bc3d37bd51db3a32fe477e38394636",
    "notes/uniform-axis-circuit-k3-pure-unary-attachment-unit.md":
        "0668a5186e209a05388b73391583cb3229e1792679bba19ade69eca44b3b6a7c",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
    "computations/verify_uniform_diagonal_alternating_cycle_switch_boundary.py":
        "f99c185403bf2e86b7352c555cd02d85bfed0df668b8a87b44a725c3db7edc71",
    "notes/uniform-diagonal-alternating-cycle-switch-boundary.md":
        "1e5b1a530d782ff03805b293ccfc3e6d76db6f046c8d8ffd4224ed3f9725f9e8",
}
EXPECTED_LEDGER_SHA256 = (
    "7149416452410d3329dd0dd3ab2e975a7b152f71a1ce21fb75f8d086bcf2bf06"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_base():
    path = ROOT / BASE_PATH
    spec = spec_from_file_location("k3_pure_attachment_unit", path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {BASE_PATH}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean(poly):
    return Counter({monomial: coefficient
                    for monomial, coefficient in poly.items()
                    if coefficient})


def constant(value):
    return Counter({(): value}) if value else Counter()


def variable(*names):
    return Counter({tuple(sorted(names)): 1})


def add(left, right, scalar=1):
    output = Counter(left)
    for monomial, coefficient in right.items():
        output[monomial] += scalar * coefficient
    return clean(output)


def multiply(left, right):
    output = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            output[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient)
    return clean(output)


def rees_degree(monomial):
    return monomial.count("eps")


def degree_part(poly, degree):
    return clean(Counter({
        tuple(name for name in monomial if name != "eps"): coefficient
        for monomial, coefficient in poly.items()
        if rees_degree(monomial) == degree
    }))


def q_cell(base, edge, left_colour, right_colour):
    left, right = edge
    if (left_colour, right_colour) == (0, 0):
        return variable(base.EDGE_NAME[edge])
    output = variable(
        "eps", f"y{left}{right}_{left_colour}{right_colour}")
    if (left_colour, right_colour) == (1, 1):
        coefficient = base.ONE_SLICE.get(edge, 0)
        if coefficient:
            output = add(output, constant(coefficient))
    return output


def coefficient_on_word(base, sites, word):
    sites = tuple(sites)
    assignment = dict(zip(sites, word, strict=True))
    output = Counter()
    for matching in base.perfect_matchings(sites):
        term = constant(1)
        for edge in matching:
            term = multiply(term, q_cell(
                base, edge, assignment[edge[0]], assignment[edge[1]]))
        output = add(output, term)
    return clean(output)


def deformed_generator(base, label):
    family, word = label
    if family == "top":
        output = coefficient_on_word(base, base.SITES, word)
        if word == (0,) * 8:
            output = add(output, constant(1), -1)
        return output

    require(family == "response", f"unknown source family: {family}")
    output = Counter()
    for occupied_site in (0, 1, 2):
        if word[occupied_site] != 1 or word[7] != 1:
            continue
        remainder = tuple(site for site in base.SITES
                          if site not in (occupied_site, 7))
        remainder_word = tuple(word[site] for site in remainder)
        output = add(output, coefficient_on_word(
            base, remainder, remainder_word))
    if word == (1,) * 8:
        output = add(output, constant(1), -1)
    return clean(output)


def audit_rees_unit(base):
    base_generators = base.build_source_generators()
    deformed = {}
    family_counts = Counter()
    positive_term_histogram = Counter()
    for label in base.CERTIFICATE:
        generator = deformed_generator(base, label)
        deformed[label] = generator
        family_counts[label[0]] += 1
        require(degree_part(generator, 0) == base_generators[label],
                f"the source initial changed at {label}")
        positive_terms = sum(1 for monomial in generator
                             if rees_degree(monomial) > 0)
        positive_term_histogram[positive_terms] += 1

    unit = Counter()
    for label, multiplier_text in base.CERTIFICATE.items():
        multiplier = base.parse_polynomial(multiplier_text)
        unit = add(unit, multiply(multiplier, deformed[label]))

    require(degree_part(unit, 0) == constant(1),
            "the completed source combination lost its unit initial")
    positive_degrees = [rees_degree(monomial) for monomial in unit
                        if rees_degree(monomial) > 0]
    require(positive_degrees,
            "the deformation unexpectedly left the old identity unchanged")
    require(min(positive_degrees) == 1 and max(positive_degrees) <= 4,
            "the Rees tail left the physical hafnian degree range")
    require(all("eps" in monomial for monomial in unit if monomial),
            "a nonconstant degree-zero tail survived")

    perturbation_names = {
        f"y{left}{right}_{a}{b}"
        for left, right in base.EDGES
        for a in range(3) for b in range(3)
        if (a, b) != (0, 0)
    }
    names_seen = {name for polynomial in deformed.values()
                  for monomial in polynomial for name in monomial
                  if name.startswith("y")}
    # The selected 22 rows need not see every direction individually; the
    # inventory itself is nevertheless complete and no direction is omitted
    # from q_cell.  Record both counts rather than asserting equality.
    require(names_seen <= perturbation_names,
            "an undeclared positive-order cell entered the source rows")

    degree_histogram = Counter(rees_degree(monomial) for monomial in unit)
    return {
        "certified_rows": len(deformed),
        "certified_row_families": dict(sorted(family_counts.items())),
        "positive_row_term_histogram": dict(
            sorted(positive_term_histogram.items())),
        "positive_directions_declared": len(perturbation_names),
        "positive_directions_seen_by_certificate_rows": len(names_seen),
        "combined_unit_terms": len(unit),
        "combined_rees_degree_histogram": dict(sorted(degree_histogram.items())),
        "constant_term": 1,
        "tail_minimum_rees_degree": min(positive_degrees),
        "tail_maximum_rees_degree": max(positive_degrees),
        "formal_inverse": (
            "(1+B)^-1=sum_{n>=0}(-B)^n, valid because B is in (eps)"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    base = load_base()
    rees = audit_rees_unit(base)
    ledger = {
        "special_fibre": "efac2b2 arbitrary pure-zero attachment chart",
        "positive_deformation_inventory": (
            "all 8 non-00 ordered decorations on all 28 physical edges"
        ),
        "rees_unit": rees,
        "classification": {
            "positive_order_anchor_edge_offdiagonal": "completed unit",
            "positive_order_diagonal_11_22": "completed unit",
            "leading_nonanchor_offdiagonal": "routes by 336492c",
            "leading_diagonal_same-site_switch": (
                "anchor-safe descent iff five-row lock vanishes (f9b51a9)"
            ),
            "remaining": (
                "a leading decorated-anchor-edge/diagonal lock web with a "
                "nonzero full five-row lock"
            ),
        },
        "scope": (
            "formal/completed initial-face theorem; no affine global "
            "emptiness is inferred away from the c536b88 special fibre"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"k3 unary Rees-rigidity ledger changed: {digest}")
    print("uniform k3 unary-attachment Rees rigidity: PASS")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
