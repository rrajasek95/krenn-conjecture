#!/usr/bin/env python3
"""Verify the universal cosimplicial totalization behind the Hasse tower.

The order-six audits record unsigned positional faces.  Those faces are not
independent correction equations: before equal derivative directions are
symmetrized, they are the coproduct components of the Boolean/divided-power
Hasse coalgebra.  Coassociativity supplies a canonical cobar differential,
whose alternating signs square to zero.  Symmetrization then gives exactly

    down(L_(k+1)) = (6-k) L_k.

This checker proves the finite order-six instance and pins the physical
order-six D2 result.  The formulas are valid in every order.  It does not
construct the subsequent map from the principal-parts source resolution to
the physical augmented correction complex.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py":
        "164d67345fe7a83d0ace581ba4417b31e3166dc5a88e487bd5ee6f2a15e5c824",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "6ab3f36073cd08c1ccad97ebd6f8ed3c5f39736be82b6063436c161f176cfeb0",
}
EXPECTED_LEDGER_SHA256 = "67c53150b2e62cdd09519252c7da748cedf982ee02bcb0e608ff820fffbf5cca"

ORDER = 6


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def subsets(mask: int):
    submask = mask
    while True:
        yield submask
        if submask == 0:
            break
        submask = (submask - 1) & mask


def coproduct(mask: int) -> Counter[tuple[int, int]]:
    """Boolean Hasse coproduct, with the six occurrences still labelled."""
    answer = Counter()
    for left in subsets(mask):
        answer[(left, mask ^ left)] += 1
    return answer


def reduced_coproduct(mask: int) -> Counter[tuple[int, int]]:
    return Counter({pair: coefficient for pair, coefficient in
                    coproduct(mask).items() if pair[0] and pair[1]})


def cobar_boundary(word: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    """Desuspended reduced-cobar differential.

    All Boolean generators have the same suspended parity here.  Splitting
    the i-th tensor factor therefore has sign (-1)^i.  The two ways to split
    one mask into three ordered nonempty blocks cancel by coassociativity.
    """
    answer = Counter()
    for position, mask in enumerate(word):
        sign = -1 if position % 2 else 1
        for (left, right), coefficient in reduced_coproduct(mask).items():
            next_word = word[:position] + (left, right) + word[position + 1:]
            answer[next_word] += sign * coefficient
    return Counter({word: coefficient for word, coefficient in answer.items()
                    if coefficient})


def apply_cobar(chain: Counter[tuple[int, ...]]) -> Counter[tuple[int, ...]]:
    answer = Counter()
    for word, coefficient in chain.items():
        for next_word, value in cobar_boundary(word).items():
            answer[next_word] += coefficient * value
    return Counter({word: coefficient for word, coefficient in answer.items()
                    if coefficient})


def coassociative(mask: int) -> bool:
    left = Counter()
    right = Counter()
    for (first, rest), coefficient in coproduct(mask).items():
        for (second, third), value in coproduct(rest).items():
            left[(first, second, third)] += coefficient * value
    for (rest, third), coefficient in coproduct(mask).items():
        for (first, second), value in coproduct(rest).items():
            right[(first, second, third)] += coefficient * value
    return left == right


def monomial(exponents: tuple[int, ...]):
    return exponents


def hasse(monomial_exponents: tuple[int, ...], order: tuple[int, ...]) -> int:
    """Coefficient of epsilon^order in (x+epsilon)^exponents."""
    coefficient = 1
    for exponent, selected in zip(monomial_exponents, order, strict=True):
        if selected > exponent:
            return 0
        numerator = 1
        denominator = 1
        for value in range(selected):
            numerator *= exponent - value
            denominator *= value + 1
        coefficient *= numerator // denominator
    return coefficient


def add_multiindices(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def sub_multiindices(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple(a - b for a, b in zip(left, right, strict=True))


def bounded_hasse_leibniz_audit() -> int:
    """Exhaust the divided-power product rule in a nontrivial finite box."""
    packets = 0
    # Three variables and total exponent/order at most four already include
    # repeated directions and every coproduct phenomenon used at order six.
    indices = [entry for entry in product(range(5), repeat=3)
               if sum(entry) <= 4]
    for left in indices:
        for right in indices:
            joined = add_multiindices(left, right)
            for order in indices:
                expected = hasse(joined, order)
                actual = 0
                for first in indices:
                    if any(a > b for a, b in zip(first, order, strict=True)):
                        continue
                    second = sub_multiindices(order, first)
                    actual += hasse(left, first) * hasse(right, second)
                require(actual == expected,
                        ("Hasse Leibniz identity changed", left, right, order,
                         actual, expected))
                packets += 1
    return packets


def positional_down_factor(size: int) -> int:
    """Each labelled size-k face has exactly ORDER-k supersets."""
    counts = Counter()
    for mask in range(1 << ORDER):
        if mask.bit_count() != size + 1:
            continue
        for bit in range(ORDER):
            if mask & (1 << bit):
                counts[mask ^ (1 << bit)] += 1
    expected_masks = [mask for mask in range(1 << ORDER)
                      if mask.bit_count() == size]
    require(set(counts) == set(expected_masks),
            ("down-incidence support changed", size))
    require(set(counts.values()) == {ORDER - size},
            ("down-incidence factor changed", size, counts))
    return ORDER - size


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    masks = tuple(range(1 << ORDER))
    require(all(coassociative(mask) for mask in masks),
            "Boolean Hasse coproduct stopped being coassociative")
    for mask in masks[1:]:
        generator = Counter({(mask,): 1})
        require(not apply_cobar(apply_cobar(generator)),
                ("cobar differential stopped squaring to zero", mask))

    # Also test the derivation extension on every two-factor word.  This is
    # redundant mathematically, but guards the suspension sign convention.
    two_factor_tests = 0
    for left in masks[1:]:
        for right in masks[1:]:
            generator = Counter({(left, right): 1})
            require(not apply_cobar(apply_cobar(generator)),
                    ("cobar d^2 failed on a product", left, right))
            two_factor_tests += 1

    down_factors = [positional_down_factor(size) for size in range(ORDER)]
    leibniz_packets = bounded_hasse_leibniz_audit()

    incidence = load(
        "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py",
        "hasse_totalization_incidence",
    )
    incidence_result = incidence.audit()
    require(incidence_result["layer_nonzero_counts"]
            == {"0": 0, "1": 0, "2": 16, "3": 401,
                "4": 916, "5": 697, "6": 166},
            "physical order-six Hasse layers changed")
    require([record["factor"] for record in incidence_result["coherence"]]
            == down_factors,
            "physical down-incidence stopped being the symmetrized coproduct")

    secondary = load(
        "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py",
        "hasse_totalization_secondary",
    )
    secondary_ledger, secondary_digest = secondary.audit()
    require(secondary_digest == secondary.EXPECTED_LEDGER_SHA256,
            "order-six secondary-transfer ledger changed")
    require(secondary_ledger["hpl_identification"]["D2_value"]
            == "-delta=(-1,+1,+1,-1)",
            "secondary class stopped being minus-delta")

    ledger = {
        "theorem": "Hasse coproduct gives canonical cosimplicial totalization",
        "order": ORDER,
        "labelled_boolean_basis": len(masks),
        "coassociative_masks": len(masks),
        "cobar_generator_d2_tests": len(masks) - 1,
        "cobar_two_factor_d2_tests": two_factor_tests,
        "divided_power_leibniz_packets": leibniz_packets,
        "symmetrized_down_factors": down_factors,
        "physical_layer_counts": incidence_result["layer_nonzero_counts"],
        "physical_secondary_class": "D2=-delta=(-1,+1,+1,-1)",
        "proved_consequence": (
            "the complete order-six Hasse faces have a canonical alternating "
            "cobar/Spencer totalization in the complete principal-parts "
            "source resolution; higher layers are forced homotopies, not "
            "independent equations"
        ),
        "source_row_stability": (
            "Hasse translation is an algebra map, so complete coefficient "
            "rows and all their polynomial multiples remain in the complete "
            "principal-parts source resolution"
        ),
        "remaining_comparison": (
            "map this canonical multigraded source resolution to the physical "
            "augmented correction complex, with the ridge terminal and "
            "physical W/anchor interpretation"
        ),
        "scope": (
            "universal/source-side totalization plus the pinned physical D2; "
            "no claim that a principal-parts chain is already a physical "
            "coordinate correction or transverse clean pair"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Hasse totalization ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 Hasse coproduct cosimplicial totalization: PASS")
    print("coassociativity/cobar d^2: exact")
    print("order-six physical D2: -delta")
    print("principal-parts-to-physical augmented comparison: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
