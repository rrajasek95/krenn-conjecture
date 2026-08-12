#!/usr/bin/env python3
"""Close the minimal silent-C6 packet with arbitrary core endpoint ports.

Fix the exact rational unary zero-fibre used by the silent-C6 bright
completion, choose one of the three pure-11 and one of the three pure-22
residual tails, and allow every colour component of p1,p2,s1,s2 on the
four core sites 0,1,3,4.  Complete literal response expansion has a very
small certificate: a diagonal target coefficient and a mixed zero
coefficient have proportional *complete endpoint polynomials*.  The first
equals one and the second equals zero, so their difference is a source unit.

This is the complete endpoint envelope over the fixed minimal decorated q
support.  Extra internal q cells are outside the theorem.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
B4_PATH = "computations/verify_h3_silent_c6_complete_response_mate_boundary.py"
PINS = {
    B4_PATH:
        "4f4a54d210b21da1183fe2fbfbb4441cec2388111b8c9e2d966a47e1d8fdcb7d",
    "notes/h3-silent-c6-complete-response-mate-boundary.md":
        "6c2dc1826d0e9be6b01081c2b84c535f30a5a427ae9a2225f490fdd2fc9bb22e",
    "computations/verify_h3_silent_c6_core_port_affine_lock_boundary.py":
        "e3fae51dce5435a93e0cd12632ad38e46f2ed5adcf2bae6614a63ff97da84c97",
    "notes/h3-silent-c6-core-port-affine-lock-boundary.md":
        "b96a4c9e03d8198edb9526593a4767520777378d5e513d78c4aaa3d120415cde",
}
CORE = (0, 1, 3, 4)
EXPECTED_LEDGER_SHA256 = (
    "d64e35125adb27ace378d9ef6d7361928a415cb19d6df3ea170ea11784df95a2"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def response_polynomials(b4, first_tail, second_tail):
    """Return every complete response coefficient as a bilinear polynomial."""

    q_cells = {
        physical: ((0, 0, value),)
        for physical, value in b4.Q00_WEIGHTS.items()
    }
    q_cells = {physical: list(options)
               for physical, options in q_cells.items()}
    for colour, tail in ((1, first_tail), (2, second_tail)):
        for physical in tail:
            q_cells.setdefault(physical, []).append((colour, colour, Q(1)))

    polynomials = {}
    for p_index in (1, 2):
        for s_index in (1, 2):
            for p_site in CORE:
                for s_site in CORE:
                    if p_site == s_site:
                        continue
                    remaining = tuple(site for site in range(6)
                                      if site not in (p_site, s_site))
                    for tail in b4.perfect_matchings(remaining):
                        choices = [q_cells.get(physical, ())
                                   for physical in tail]
                        if any(not options for options in choices):
                            continue
                        for selected in product(*choices):
                            for p_colour in range(3):
                                for s_colour in range(3):
                                    word = [None] * 6
                                    word[p_site] = p_colour
                                    word[s_site] = s_colour
                                    coefficient = Q(1)
                                    for physical, option in zip(
                                            tail, selected, strict=True):
                                        left_colour, right_colour, value = option
                                        word[physical[0]] = left_colour
                                        word[physical[1]] = right_colour
                                        coefficient *= value
                                    key = (p_index, s_index, tuple(word))
                                    monomial = (
                                        f"p{p_index}_{p_site}_{p_colour}",
                                        f"s{s_index}_{s_site}_{s_colour}",
                                    )
                                    polynomial = polynomials.setdefault(key, {})
                                    polynomial[monomial] = (
                                        polynomial.get(monomial, Q(0))
                                        + coefficient
                                    )

    return {
        key: {monomial: coefficient
              for monomial, coefficient in polynomial.items()
              if coefficient}
        for key, polynomial in polynomials.items()
        if any(polynomial.values())
    }


def normalized(polynomial):
    require(polynomial, "cannot normalize the zero polynomial")
    pivot = sorted(polynomial)[0]
    scale = polynomial[pivot]
    vector = tuple(sorted(
        (monomial, str(coefficient / scale))
        for monomial, coefficient in polynomial.items()
    ))
    return vector, scale


def audit_bright_pair(b4, first_index, second_index):
    first_tail = b4.BRIGHT_TAILS[1][first_index - 1]
    second_tail = b4.BRIGHT_TAILS[2][second_index - 1]
    polynomials = response_polynomials(b4, first_tail, second_tail)

    groups = {}
    for key, polynomial in polynomials.items():
        vector, scale = normalized(polynomial)
        groups.setdefault(vector, []).append((key, scale, polynomial))

    certificates = []
    for vector, entries in groups.items():
        targets = []
        zeros = []
        for key, scale, polynomial in entries:
            p_index, s_index, word = key
            is_target = (
                p_index == s_index
                and word == (p_index,) * 6
            )
            record = (key, scale, polynomial)
            (targets if is_target else zeros).append(record)
        for target in targets:
            for zero in zeros:
                certificates.append((vector, target, zero))

    require(certificates,
            f"bright pair {(first_index, second_index)} lost its two-row unit")
    certificates.sort(key=lambda item: (item[1][0], item[2][0]))
    vector, target, zero = certificates[0]
    target_key, target_scale, target_polynomial = target
    zero_key, zero_scale, zero_polynomial = zero

    # If P is the normalized common polynomial, the exact response
    # generators are target_scale*P-1 and zero_scale*P.  Hence
    # (1/zero_scale) F_zero - (1/target_scale) F_target = 1.
    require(target_scale and zero_scale, "a certificate scale vanished")
    require(normalized(target_polynomial)[0]
            == normalized(zero_polynomial)[0] == vector,
            "the paired complete polynomials stopped being proportional")

    return {
        "X1_tail_index": first_index,
        "X2_tail_index": second_index,
        "complete_response_coefficient_count": len(polynomials),
        "proportional_target_zero_pair_count": len(certificates),
        "target_row": [target_key[0], target_key[1]],
        "target_word": "".join(map(str, target_key[2])),
        "zero_row": [zero_key[0], zero_key[1]],
        "zero_word": "".join(map(str, zero_key[2])),
        "target_scale": str(target_scale),
        "zero_scale": str(zero_scale),
        "common_endpoint_polynomial": [
            [list(monomial), coefficient] for monomial, coefficient in vector
        ],
        "integral_unit_identity": (
            f"(1/({zero_scale}))*F_zero"
            f"-(1/({target_scale}))*F_target=1"
        ),
    }


def audit():
    pin_dependencies()
    b4 = load(B4_PATH, "silent_c6_full_core_b4")
    records = [
        audit_bright_pair(b4, first_index, second_index)
        for first_index in (1, 2, 3)
        for second_index in (1, 2, 3)
    ]
    require(len(records) == 9, "the bright-pair inventory changed")
    require(all(record["proportional_target_zero_pair_count"] >= 1
                for record in records),
            "a bright chart lost its ordinary source unit")

    ledger = {
        "pins": PINS,
        "core_sites": CORE,
        "endpoint_variables": (
            "all 48 p_i/s_j components of colours 0,1,2 on sites 0,1,3,4"
        ),
        "records": records,
        "theorem": (
            "for every one of the nine bright-tail choices, one complete "
            "diagonal target coefficient and one complete mixed zero "
            "coefficient are nonzero scalar multiples of the same bilinear "
            "endpoint polynomial; their source generators have unit "
            "difference, so the full arbitrary-core-port endpoint envelope "
            "over the minimal decorated q support is empty"
        ),
        "superseded_local_residual": (
            "the reciprocal core-port Fitting lock survives one selected "
            "private coefficient but not the complete response packet on "
            "this fixed q support"
        ),
        "scope": (
            "the exact rational q00 silent-C6 zero fibre plus one selected "
            "pure-11 and one selected pure-22 tail, with arbitrary endpoint "
            "components on core sites.  Extra endpoint ports or extra "
            "internal decorated q cells are not silently included"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"silent C6 full-core unit changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 silent C6 full core-port unit: PASS (exact)")
    print("nine bright-tail pairs: complete target/zero proportional units")
    print("all 48 endpoint components on core sites included")
    print("reciprocal private-row Fitting residual: superseded on fixed q support")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
