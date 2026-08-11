#!/usr/bin/env python3
"""All-support pure-zero unary completion of the endpoint-minor packet.

Allow an arbitrary 00 cell z_ij on every residual K6 edge, while retaining
the four pinned 11/22 q cells and endpoint stars.  The eight mixed unary-top
coefficients give a small exact ideal.  Modulo that ideal the pure-zero
hafnian is z03*z12*z45.  Localizing at q^[3]=X0 therefore makes these three
factors units and forces both crossed-response cofactors to be units.

This is a structural all-support theorem for pure-zero additions.  It does
not include new mixed-colour q cells or new endpoint-star cells.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_endpoint_minor_unary_top_completion.py":
        "f0d4c5382cce1ccb8bed5a5ac0afa8cf8662c905bd0c675a56b51f2be7d0b574",
    "computations/verify_n8_one_bad_multisite_permanent_null_defect.py":
        "94946c00fc25cd08eead06148deae85cc2ed80e0cce65c68bc37ad50384f6f53",
}
EXPECTED_LEDGER_SHA256 = (
    "bb8b74e48e79728be1bafe07b3e00e2b355b2f09c79042b0aad0d1ea761d34ce"
)

SITES = tuple(range(6))
PURE0 = (0,) * 6


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def variable(name):
    return Counter({(name,): Fraction(1)})


def poly_add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def poly_scale(polynomial, coefficient):
    return Counter({term: coefficient * value
                    for term, value in polynomial.items()
                    if coefficient * value})


def product(completion, *names):
    answer = Counter({(): Fraction(1)})
    for name in names:
        answer = completion.poly_mul(answer, variable(name))
    return answer


def divide_by_variable(polynomial, name):
    answer = Counter()
    for term, coefficient in polynomial.items():
        require(name in term, f"{name} does not divide {term}")
        reduced = list(term)
        reduced.remove(name)
        answer[tuple(reduced)] += coefficient
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def pure_zero_cofactor(completion, module, cells, deleted):
    vertices = tuple(site for site in SITES if site not in deleted)
    tensor = completion.symbolic_matching_tensor(module, cells, vertices)
    return tensor.get((0,) * len(vertices), Counter())


def main():
    pin_dependencies()
    completion = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_unary_top_completion")
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    cells = {
        module.source_cell(2, 4, 1, 1): variable("A"),
        module.source_cell(3, 5, 1, 1): variable("B"),
        module.source_cell(0, 5, 2, 2): variable("C"),
        module.source_cell(1, 4, 2, 2): variable("D"),
    }
    for left in SITES:
        for right in SITES[left + 1:]:
            cells[module.source_cell(left, right, 0, 0)] = variable(
                f"z{left}{right}"
            )

    top = completion.symbolic_matching_tensor(module, cells, SITES)
    require(len(top) == 9,
            f"the arbitrary pure completion acquired new top words: {len(top)}")
    mixed_words = tuple(word for word in top if word != PURE0)
    require(tuple("".join(map(str, word)) for word in sorted(mixed_words)) == (
        "000101", "001010", "001111", "020020",
        "020121", "200002", "201012", "220022",
    ), "the eight mixed unary words changed")

    # Divide the eight mixed rows by the anchor units A,B,C,D.  The response
    # anchors A*B*p0*s1=1 and C*D*p2*s2=1 make all four q factors units.
    generators = {
        "z01": divide_by_variable(
            divide_by_variable(top[(0, 0, 1, 1, 1, 1)], "A"), "B"),
        "z02": divide_by_variable(
            divide_by_variable(top[(0, 2, 0, 1, 2, 1)], "B"), "D"),
        "z13": divide_by_variable(
            divide_by_variable(top[(2, 0, 1, 0, 1, 2)], "A"), "C"),
        "z23": divide_by_variable(
            divide_by_variable(top[(2, 2, 0, 0, 2, 2)], "C"), "D"),
        "g_24": divide_by_variable(top[(0, 0, 1, 0, 1, 0)], "A"),
        "g_35": divide_by_variable(top[(0, 0, 0, 1, 0, 1)], "B"),
        "g_05": divide_by_variable(top[(2, 0, 0, 0, 0, 2)], "C"),
        "g_14": divide_by_variable(top[(0, 2, 0, 0, 2, 0)], "D"),
    }
    expected_generators = {
        "z01": variable("z01"),
        "z02": variable("z02"),
        "z13": variable("z13"),
        "z23": variable("z23"),
        "g_24": poly_add(product(completion, "z01", "z35"),
                         product(completion, "z03", "z15"),
                         product(completion, "z05", "z13")),
        "g_35": poly_add(product(completion, "z01", "z24"),
                         product(completion, "z02", "z14"),
                         product(completion, "z04", "z12")),
        "g_05": poly_add(product(completion, "z12", "z34"),
                         product(completion, "z13", "z24"),
                         product(completion, "z14", "z23")),
        "g_14": poly_add(product(completion, "z02", "z35"),
                         product(completion, "z03", "z25"),
                         product(completion, "z05", "z23")),
    }
    require(generators == expected_generators,
            f"the normalized mixed-top ideal changed: {generators}")

    hafnian = top[PURE0]
    central = product(completion, "z03", "z12", "z45")

    # Exact source-level ideal certificate.  No radical or support argument
    # is used: haf(z)-z03*z12*z45 is this literal combination of the eight
    # normalized mixed unary rows.
    certificate = poly_add(
        completion.poly_mul(variable("z14"), generators["g_14"]),
        completion.poly_mul(variable("z24"), generators["g_24"]),
        completion.poly_mul(variable("z35"), generators["g_35"]),
        completion.poly_mul(variable("z05"), generators["g_05"]),
        completion.poly_mul(
            generators["z01"],
            poly_add(product(completion, "z23", "z45"),
                     poly_scale(product(completion, "z24", "z35"), -1),
                     product(completion, "z25", "z34"))),
        completion.poly_mul(
            generators["z02"],
            poly_add(product(completion, "z13", "z45"),
                     poly_scale(product(completion, "z14", "z35"), -1),
                     product(completion, "z15", "z34"))),
        completion.poly_mul(
            generators["z13"],
            poly_add(product(completion, "z04", "z25"),
                     poly_scale(product(completion, "z05", "z24"), -1))),
        completion.poly_mul(
            generators["z23"],
            poly_add(product(completion, "z04", "z15"),
                     poly_scale(product(completion, "z05", "z14"), -1))),
    )
    require(poly_add(hafnian, poly_scale(central, -1)) == certificate,
            "the hafnian ideal certificate changed")

    # In the quotient, the four quadratic generators reduce as displayed.
    # Since haf(z)=1, the certificate gives z03*z12*z45=1.  Hence z03 and
    # z12 are units, and the reduced quadratic rows force four extra zeros.
    localized_forced_zero = {
        "z15": "g_24=z03*z15 and z03 is a unit",
        "z25": "g_14=z03*z25 and z03 is a unit",
        "z04": "g_35=z04*z12 and z12 is a unit",
        "z34": "g_05=z12*z34 and z12 is a unit",
    }

    cofactor_03 = pure_zero_cofactor(
        completion, module, cells, frozenset((0, 3)))
    cofactor_12 = pure_zero_cofactor(
        completion, module, cells, frozenset((1, 2)))
    require(cofactor_03 == poly_add(
        product(completion, "z12", "z45"),
        product(completion, "z14", "z25"),
        product(completion, "z15", "z24")),
        "the 03-deleted pure cofactor changed")
    require(cofactor_12 == poly_add(
        product(completion, "z03", "z45"),
        product(completion, "z04", "z35"),
        product(completion, "z05", "z34")),
        "the 12-deleted pure cofactor changed")

    stars = {
        "p1": {0: (1, "p0"), 5: (1, "p5")},
        "p2": {2: (2, "p2")},
        "s1": {1: (1, "s1")},
        "s2": {3: (2, "s2")},
    }
    response_12 = completion.symbolic_star_product(
        module, stars["p1"], stars["s2"], cells)
    response_21 = completion.symbolic_star_product(
        module, stars["p2"], stars["s1"], cells)
    require(response_12[(1, 0, 0, 2, 0, 0)]
            == completion.poly_mul(
                product(completion, "p0", "s2"), cofactor_03),
            "the 12 crossed cofactor provenance changed")
    require(response_21[(0, 1, 2, 0, 0, 0)]
            == completion.poly_mul(
                product(completion, "p2", "s1"), cofactor_12),
            "the 21 crossed cofactor provenance changed")

    ledger = {
        "dependencies": PINS,
        "q_scope": "fixed four 11/22 cells plus arbitrary 15-cell 00 form z",
        "top_word_count": len(top),
        "normalized_mixed_generators": {
            name: completion.serial_polynomial(polynomial)
            for name, polynomial in generators.items()
        },
        "hafnian_terms": len(hafnian),
        "ideal_certificate_terms": len(certificate),
        "quotient_hafnian": "haf(z)=z03*z12*z45",
        "localized_equation": "z03*z12*z45=1",
        "localized_forced_zero": localized_forced_zero,
        "crossed_cofactors": {
            "delete_03": completion.serial_polynomial(cofactor_03),
            "delete_12": completion.serial_polynomial(cofactor_12),
            "localized_delete_03": "z12*z45 (a unit)",
            "localized_delete_12": "z03*z45 (a unit)",
        },
        "verdict": (
            "every arbitrary pure-zero unary completion has both crossed "
            "response coefficients nonzero; it cannot repair the pinned "
            "four-response packet, independently of alternating-C4 activity"
        ),
        "scope": (
            "all 15 pure-zero q cells with arbitrary coefficients; the four "
            "old coloured q cells and endpoint-star support are pinned; new "
            "mixed-colour q cells and new star cells are not classified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the arbitrary-pure completion ledger changed: {digest}")

    print("N=8 endpoint-minor arbitrary pure unary completion: PASS")
    print("mixed top rows: 8; exact hafnian ideal certificate replayed")
    print("localized quotient: haf(z)=z03*z12*z45=1")
    print("both crossed-response cofactors are units")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
