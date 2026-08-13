#!/usr/bin/env python3
"""Uniform factorization of the endpoint-chart H2 scalar proper face.

Expose endpoints P,S in the response hafnian on 2h+2 sites and select two
residual sites 0,1.  The three internal perfect matchings of
X={0,1,P,S} are

    A=PS*01, B=0P*1S, C=1P*0S.

Writing H_Y for the hafnian on the complementary 2h-2 sites, the zero-cross
response sector is (A+B+C)H_Y and the pointed chart-reset scalar is

    L_h=(2A-B-C)H_Y=3AH_Y-R_X.

Thus the coefficient obstruction is recursive in response order.  The
checker exhausts the literal matching/cross-sector census through h=6; the
all-order proof is the displayed disjoint-union factorization.  This does
not construct the physical monoidal PP lift: capping a lower comparison has
Leibniz faces, and isolating the fixed-chart sector is still required.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_response_h2_full_site_tag_contraction.py":
        "5709b5ba93e775d372e5caa5ba33b0c1e168177d9866ff52137245db3f1dc1c0",
    "notes/uniform-response-h2-full-site-tag-contraction.md":
        "6f83f12b94ac14db9ee4c6599ac05cbabfce7cd2a817fd2f2cc84bc7adf621ca",
    "computations/verify_h3_h2_chart_scalar_capped_c4_augmented_gate.py":
        "18cb73805ffca0a080bc061c88cb42f6c0c83d57efd60c574455b757009785b4",
    "notes/h3-h2-chart-scalar-capped-c4-augmented-gate.md":
        "baee4965bcb9315fc7e9f51693aebcf3cfb6c8a147c76144eb287f7c9c74c998",
}
EXPECTED_LEDGER_SHA256 = "6c3531c058c8c28e30f063d65905aa5b42c78212d18a89508cf50c5e2e066791"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def odd_double_factorial(value: int) -> int:
    require(value >= -1 and value % 2 == 1, value)
    if value <= 0:
        return 1
    return math.prod(range(1, value + 1, 2))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def cross_count(matching, selected: frozenset[int]) -> int:
    return sum((left in selected) != (right in selected)
               for left, right in matching)


def audit_order(h: int) -> dict[str, object]:
    site_count = 2 * h + 2
    sites = tuple(range(site_count))
    selected = frozenset((0, 1, site_count - 2, site_count - 1))
    complement = tuple(site for site in sites if site not in selected)
    matchings = tuple(perfect_matchings(sites))
    tails = tuple(perfect_matchings(complement))
    histogram = Counter(cross_count(matching, selected)
                        for matching in matchings)

    tail_count = odd_double_factorial(2 * h - 3)
    zero_cross = 3 * tail_count
    two_cross = (12 * math.comb(2 * h - 2, 2)
                 * odd_double_factorial(2 * h - 5))
    four_cross = (24 * math.comb(2 * h - 2, 4)
                  * odd_double_factorial(2 * h - 7)
                  if h >= 3 else 0)
    expected = Counter({0: zero_cross, 2: two_cross})
    if four_cross:
        expected[4] = four_cross
    require(len(matchings) == odd_double_factorial(2 * h + 1)
            and len(tails) == tail_count
            and histogram == expected,
            (h, len(matchings), len(tails), histogram, expected))

    local = tuple(matching for matching in matchings
                  if cross_count(matching, selected) == 0)
    local_coefficients = []
    P, S = site_count - 2, site_count - 1
    A = frozenset(((0, 1), (P, S)))
    B = frozenset(((0, P), (1, S)))
    C = frozenset(((0, S), (1, P)))
    for matching in local:
        internal = frozenset(edge for edge in matching
                             if edge[0] in selected)
        require(internal in (A, B, C), (h, matching, internal))
        local_coefficients.append(2 if internal == A else -1)
    require(Counter(local_coefficients)
            == Counter({2: tail_count, -1: 2 * tail_count})
            and sum(local_coefficients) == 0
            and sum(value * value for value in local_coefficients)
                == 6 * tail_count,
            (h, Counter(local_coefficients)))

    # An all-order literal response-row countermodel: retain one tail
    # matching, A=1 and B=-1.  Then R=0 but L=3.  This proves that the
    # recursive scalar is not killed by the complete response equation.
    response_value = 1 - 1
    scalar_value = 2 - (-1)
    require(response_value == 0 and scalar_value == 3,
            (response_value, scalar_value))

    return {
        "h": h,
        "response_sites": site_count,
        "complete_response_occurrences": len(matchings),
        "complement_sites": len(complement),
        "lower_hafnian_order": h - 1,
        "lower_tail_matchings": tail_count,
        "cross_sector_counts": {str(key): value
                                 for key, value in sorted(histogram.items())},
        "zero_cross_sector": "(A+B+C)*H_(h-1)",
        "chart_scalar": "(2A-B-C)*H_(h-1)",
        "chart_scalar_support": len(local_coefficients),
        "chart_scalar_augmentation": sum(local_coefficients),
        "chart_scalar_squared_norm": sum(value * value
                                           for value in local_coefficients),
        "literal_countermodel": {"response": response_value,
                                   "chart_scalar": scalar_value},
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    orders = tuple(audit_order(h) for h in range(2, 7))
    require(orders[1]["complete_response_occurrences"] == 105
            and orders[1]["cross_sector_counts"]
                == {"0": 9, "2": 72, "4": 24}
            and orders[1]["chart_scalar_support"] == 9,
            orders[1])
    ledger = {
        "theorem": "uniform recursive factorization of response-H2 chart scalar",
        "pins": PINS,
        "orders_exhaustively_audited": orders,
        "uniform_identity": {
            "selected_four_set": "X={0,1,P,S}",
            "internal_matchings": "A=01*PS, B=0P*1S, C=0S*1P",
            "complementary_tail": "H_Y=Hafnian on 2h-2 sites, order h-1",
            "zero_cross_response": "R_X=(A+B+C)H_Y",
            "pointed_chart_scalar": "L_h=(2A-B-C)H_Y=3AH_Y-R_X",
            "proof": "perfect matchings with no X--Y edge split uniquely into a matching of X and one of Y",
        },
        "physical_consequence": (
            "there is no new coefficient species at higher h: every chart "
            "proper face is a four-site direction factor times the lower-order "
            "hafnian.  A uniform proof still needs a monoidal source-valid PP "
            "cylinder; its Leibniz and fixed-chart block faces are not supplied "
            "by the coefficient factorization"
        ),
        "shortest_positive_theorem": (
            "construct the pointed endpoint-chart cylinder compatibly with "
            "disjoint-union hafnian multiplication.  Its lower factor is the "
            "order-(h-1) comparison, and its product-rule faces must land in "
            "the already classified lower C2+/C4/P2 packets with full augmented typing"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    for row in ledger["orders_exhaustively_audited"]:
        print("h={h}: response={complete_response_occurrences}, tail={lower_tail_matchings}, "
              "sectors={cross_sector_counts}, |L|={chart_scalar_support}".format(**row))
    print("uniform identity: L_h=(2A-B-C)*H_(h-1)")
    print("physical monoidal PP cylinder: STILL REQUIRED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
