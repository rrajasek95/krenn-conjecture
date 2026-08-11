#!/usr/bin/env python3
"""First unary-top completion of the cofactor-invisible response packet.

The fb8d482 packet has four exact binary response rows but q^[3]=0.  At the
smallest possible additive q-support, a pure-zero unary top requires three
new 00 cells on a perfect matching.  This checker classifies all 15 such
matchings symbolically.  Exactly one has no mixed unary-top term, and its
literal response expansion is already inconsistent: it makes the previously
invisible p1@5 component removable and then leaves two nonzero crossed rows.

This is a bounded exact-support theorem.  It does not classify completions
which also introduce new endpoint-star cells or more than three q cells.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_endpoint_minor_c4_counterguard.py":
        "09deff150677bfa67f0109cb3f961d840bfc4856a759f3f8d18a99d24038b5a6",
    "computations/verify_n8_one_bad_multisite_permanent_null_defect.py":
        "94946c00fc25cd08eead06148deae85cc2ed80e0cce65c68bc37ad50384f6f53",
}
EXPECTED_LEDGER_SHA256 = (
    "e7ca3e20e83405d16576000cea84a65aa6b4bca06af91ba67cfffc85e8ee989e"
)

SITES = tuple(range(6))
PURE0 = (0,) * 6
PURE1 = (1,) * 6
PURE2 = (2,) * 6
Monomial = tuple[str, ...]
Polynomial = Counter[Monomial]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def monomial(*variables):
    return tuple(sorted(variables))


def poly_mul(left, right):
    output = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            output[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return Counter({term: coefficient for term, coefficient in output.items()
                    if coefficient})


def symbolic_matching_tensor(module, cells, vertices):
    output = defaultdict(Counter)
    for matching in module.perfect_matchings(vertices):
        choices = []
        for edge in matching:
            choices.append(tuple(
                (left_colour, right_colour, polynomial)
                for (cell_edge, left_colour, right_colour), polynomial
                in cells.items() if cell_edge == edge and polynomial
            ))
        if any(not choice for choice in choices):
            continue

        def visit(index, word, coefficient):
            if index == len(matching):
                output[tuple(word[site] for site in vertices)].update(
                    coefficient
                )
                return
            left, right = matching[index]
            for left_colour, right_colour, polynomial in choices[index]:
                next_word = list(word)
                next_word[left], next_word[right] = left_colour, right_colour
                visit(index + 1, next_word,
                      poly_mul(coefficient, polynomial))

        visit(0, [-1] * len(SITES), Counter({(): Fraction(1)}))
    return {
        word: Counter({term: coefficient for term, coefficient
                       in polynomial.items() if coefficient})
        for word, polynomial in output.items()
        if polynomial
    }


def symbolic_star_product(module, left_star, right_star, q_cells):
    output = defaultdict(Counter)
    for left_site, (left_colour, left_variable) in left_star.items():
        for right_site, (right_colour, right_variable) in right_star.items():
            if left_site == right_site:
                continue
            remaining = tuple(site for site in SITES
                              if site not in (left_site, right_site))
            cofactor = symbolic_matching_tensor(module, q_cells, remaining)
            for cofactor_word, polynomial in cofactor.items():
                word = [-1] * len(SITES)
                word[left_site] = left_colour
                word[right_site] = right_colour
                for site, colour in zip(remaining, cofactor_word, strict=True):
                    word[site] = colour
                star_factor = Counter({
                    monomial(left_variable, right_variable): Fraction(1)
                })
                output[tuple(word)].update(poly_mul(star_factor, polynomial))
    return {
        word: Counter({term: coefficient for term, coefficient
                       in polynomial.items() if coefficient})
        for word, polynomial in output.items()
        if polynomial
    }


def serial_polynomial(polynomial):
    return {
        "*".join(term) if term else "1": str(coefficient)
        for term, coefficient in sorted(polynomial.items())
    }


def serial_tensor(tensor):
    return {
        "".join(map(str, word)): serial_polynomial(polynomial)
        for word, polynomial in sorted(tensor.items())
    }


def numeric_blocks(module, completion, delete_p5):
    guard = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_c4_counterguard")
    q_cells, stars, _blocks = guard.source_packet(module)
    q_cells = Counter(q_cells)
    for edge in completion:
        q_cells[module.source_cell(*edge, 0, 0)] += 1
    if delete_p5:
        stars = {name: dict(row) for name, row in stars.items()}
        del stars["p1"][5]
    blocks = Counter(q_cells)
    for name, label, endpoint in (
            ("p1", 1, 6), ("p2", 2, 6),
            ("s1", 1, 7), ("s2", 2, 7)):
        for site, vector in stars[name].items():
            for colour, coefficient in enumerate(vector):
                if coefficient:
                    blocks[module.source_cell(
                        endpoint, site, label, colour)] += coefficient
    return guard, stars, blocks


def compatible_minor_count(module, completion, delete_p5):
    guard, _stars, blocks = numeric_blocks(module, completion, delete_p5)
    count = 0
    compatible = 0
    minors = {}
    for endpoint, label in ((6, "P"), (7, "Q")):
        left = guard.port_row(module, blocks, endpoint, 1)
        right = guard.port_row(module, blocks, endpoint, 2)
        endpoint_minors = guard.nonzero_minors(left, right)
        minors[label] = len(endpoint_minors)
        for first, second, determinant in endpoint_minors:
            for reference, alternate in ((first, second), (second, first)):
                _vertices, _cofactor, visible = guard.visible_cofactor_terms(
                    module, blocks, endpoint, reference, alternate)
                count += 1
                compatible += bool(visible)
    return minors, count, compatible


def main():
    pin_dependencies()
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    # A,B and C,D are the two fixed response matchings.  The four response
    # anchors imply A*B*p0*s1=1 and C*D*p2*s2=1, so all eight factors are
    # units.  The three new zero cells have weights u,v,w and unary top
    # u*v*w=1, so they too are units.
    old_cells = {
        module.source_cell(2, 4, 1, 1): Counter({("A",): Fraction(1)}),
        module.source_cell(3, 5, 1, 1): Counter({("B",): Fraction(1)}),
        module.source_cell(0, 5, 2, 2): Counter({("C",): Fraction(1)}),
        module.source_cell(1, 4, 2, 2): Counter({("D",): Fraction(1)}),
    }
    completion_audit = []
    clean = []
    for matching in module.perfect_matchings(SITES):
        cells = dict(old_cells)
        for edge, variable in zip(matching, ("u", "v", "w"), strict=True):
            cells[module.source_cell(*edge, 0, 0)] = Counter({
                (variable,): Fraction(1)
            })
        top = symbolic_matching_tensor(module, cells, SITES)
        require(top.get(PURE0) == Counter({monomial("u", "v", "w"): 1}),
                f"the pure unary monomial changed for {matching}")
        mixed = {word: polynomial for word, polynomial in top.items()
                 if word != PURE0}
        require(all(len(polynomial) == 1 and next(iter(polynomial.values())) == 1
                    for polynomial in mixed.values()),
                f"a first-completion mixed top can cancel for {matching}")
        completion_audit.append({
            "matching": matching,
            "mixed_top": serial_tensor(mixed),
        })
        if not mixed:
            clean.append(matching)

    unique = ((0, 3), (1, 2), (4, 5))
    require(clean == [unique],
            f"the clean first unary completion changed: {clean}")
    histogram = Counter(len(entry["mixed_top"])
                        for entry in completion_audit)
    require(histogram == Counter({0: 1, 1: 8, 2: 2, 3: 4}),
            f"the first-completion histogram changed: {histogram}")

    cells = dict(old_cells)
    for edge, variable in zip(unique, ("u", "v", "w"), strict=True):
        cells[module.source_cell(*edge, 0, 0)] = Counter({
            (variable,): Fraction(1)
        })
    stars = {
        "p1": {0: (1, "p0"), 5: (1, "p5")},
        "p2": {2: (2, "p2")},
        "s1": {1: (1, "s1")},
        "s2": {3: (2, "s2")},
    }
    responses = {
        "11": symbolic_star_product(module, stars["p1"], stars["s1"], cells),
        "12": symbolic_star_product(module, stars["p1"], stars["s2"], cells),
        "21": symbolic_star_product(module, stars["p2"], stars["s1"], cells),
        "22": symbolic_star_product(module, stars["p2"], stars["s2"], cells),
    }
    expected_responses = {
        "11": {
            PURE1: Counter({monomial("A", "B", "p0", "s1"): 1}),
            (0, 1, 1, 0, 1, 1): Counter({
                monomial("A", "p5", "s1", "u"): 1
            }),
        },
        "12": {
            (1, 0, 0, 2, 0, 0): Counter({
                monomial("p0", "s2", "v", "w"): 1
            }),
        },
        "21": {
            (0, 1, 2, 0, 0, 0): Counter({
                monomial("p2", "s1", "u", "w"): 1
            }),
        },
        "22": {
            PURE2: Counter({monomial("C", "D", "p2", "s2"): 1}),
        },
    }
    require(responses == expected_responses,
            f"the unique-completion response expansion changed: {responses}")

    # The new 11 tail forces p5=0 because A,s1,u are units.  The two crossed
    # tails do not contain p5 and remain nonzero after that forced deletion.
    crossed_unit_monomials = {
        label: next(iter(responses[label].values())).copy()
        for label in ("12", "21")
    }
    require(all(len(polynomial) == 1 and next(iter(polynomial.values())) == 1
                for polynomial in crossed_unit_monomials.values()),
            "a crossed completion tail stopped being one unit monomial")
    require(all("p5" not in next(iter(polynomial))
                for polynomial in crossed_unit_monomials.values()),
            "a crossed completion tail acquired the removable component")

    retained_minors, retained_orientations, retained_compatible = (
        compatible_minor_count(module, unique, False)
    )
    reduced_minors, reduced_orientations, reduced_compatible = (
        compatible_minor_count(module, unique, True)
    )
    require((retained_minors, retained_orientations, retained_compatible)
            == ({"P": 2, "Q": 1}, 6, 0),
            "the retained-p5 C4 audit changed")
    require((reduced_minors, reduced_orientations, reduced_compatible)
            == ({"P": 1, "Q": 1}, 4, 0),
            "the reduced-p5 C4 audit changed")

    ledger = {
        "dependencies": PINS,
        "minimality": (
            "q^[3]=X0 needs three new 00 decorated cells on one residual "
            "perfect matching; exactly these 15 additive supports are tested"
        ),
        "completion_count": len(completion_audit),
        "mixed_top_histogram": dict(sorted(histogram.items())),
        "unique_clean_top_matching": unique,
        "unique_response_expansion": {
            label: serial_tensor(tensor)
            for label, tensor in responses.items()
        },
        "unit_equations": [
            "A*B*p0*s1=1", "C*D*p2*s2=1", "u*v*w=1",
        ],
        "forced_deletion": "A*p5*s1*u=0 forces p5=0",
        "uncancellable_crossed_tails": {
            "12@100200": "p0*s2*v*w",
            "21@012000": "p2*s1*u*w",
        },
        "alternating_c4": {
            "before_p5_deletion": {
                "minors": retained_minors,
                "oriented_tests": retained_orientations,
                "compatible": retained_compatible,
            },
            "after_p5_deletion": {
                "minors": reduced_minors,
                "oriented_tests": reduced_orientations,
                "compatible": reduced_compatible,
            },
        },
        "verdict": (
            "the unique three-cell common-q unary completion forces deletion "
            "of the formerly response-invisible p1@5 component but leaves "
            "two unit crossed-response tails; hence no exact full-source "
            "guard survives on the first top-compatible support"
        ),
        "scope": (
            "additive completion of the pinned four q cells by exactly three "
            "00 cells, with the pinned endpoint-star support and arbitrary "
            "nonzero coefficients; new star cells and larger q supports are "
            "not classified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the unary completion ledger changed: {digest}")

    print("N=8 endpoint-minor first unary completion: PASS")
    print("three-cell 00 completions: 15; clean unary top: unique 03/12/45")
    print("p1@5 is forced removable; crossed unit tails remain: 2")
    print("compatible alternating-C4 cofactors: 0/6 then 0/4")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
